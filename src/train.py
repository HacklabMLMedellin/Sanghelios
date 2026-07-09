"""Entrenamiento del modelo de escasez y construcción de la BD operativa.

Reproduce el pipeline del notebook ``04_modelo_predictivo`` (Parte 4 — Series
de Tiempo) a partir de las features de ``src.features.build_features`` y:

1. entrena el clasificador XGBoost del objetivo ``escasez_t14`` (¿la presión
   demanda-oferta superará el umbral τ dentro de 14 días?),
2. guarda el modelo + metadatos en ``models/predictive/escasez_model.pkl``,
3. escribe una base SQLite ``data/sanghelios.db`` con la serie diaria (incluida
   la probabilidad de escasez predicha), el stock por grupo sanguíneo y las
   campañas, que el backend expone en ``/api/*``.

Uso:  ``uv run python -m src.train``  (o ``scripts/build_db_and_model.py``)
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import fbeta_score
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBClassifier

from src.features.build_features import H, TEST_FRAC, build_model_frame

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models" / "predictive"
DB_PATH = PROJECT_ROOT / "data" / "sanghelios.db"

BETA = 2.0  # prioriza recall (perder una alerta cuesta más que una falsa)


# ── 1. Entrenamiento + umbral out-of-fold ────────────────────────────────────
def umbral_oof(estimador, X: pd.DataFrame, y: pd.Series, beta: float = BETA) -> float:
    tscv = TimeSeriesSplit(n_splits=5)
    oof = np.full(len(X), np.nan)
    for tr_i, va_i in tscv.split(X):
        e = clone(estimador).fit(X.iloc[tr_i], y.iloc[tr_i])
        oof[va_i] = e.predict_proba(X.iloc[va_i])[:, 1]
    mask = ~np.isnan(oof)
    ys, ss = y.to_numpy()[mask], oof[mask]
    grid = np.quantile(ss, np.linspace(0.30, 0.99, 80))
    best_fb, best_t = -1.0, 0.5
    for t in grid:
        fb = fbeta_score(ys, (ss >= t).astype(int), beta=beta, zero_division=0)
        if fb > best_fb:
            best_fb, best_t = fb, float(t)
    return best_t


def train(m: pd.DataFrame, features: list[str]) -> tuple[XGBClassifier, float]:
    split = int(len(m) * (1 - TEST_FRAC))
    X_train, y_train = m[features].iloc[:split], m["escasez_t14"].iloc[:split]
    spw = (y_train == 0).sum() / max(1, (y_train == 1).sum())
    model = XGBClassifier(
        n_estimators=400, max_depth=3, learning_rate=0.04,
        subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0,
        random_state=42, eval_metric="logloss", scale_pos_weight=spw,
    )
    model.fit(X_train, y_train)
    threshold = umbral_oof(model, X_train, y_train)
    # Reentrenar con toda la serie para servir predicciones actualizadas.
    model.fit(m[features], m["escasez_t14"])
    return model, threshold


# ── 2. Stock y campañas semilla (proporción de grupos del EDA) ───────────────
def seed_stock() -> pd.DataFrame:
    # Proporción de donantes por grupo (EDA) → unidades disponibles de referencia.
    share = {
        "O+": 0.537, "A+": 0.255, "O-": 0.090, "B+": 0.064,
        "A-": 0.028, "AB+": 0.016, "B-": 0.008, "AB-": 0.002,
    }
    total = 1400
    rows = []
    for tipo, s in share.items():
        unidades = int(round(s * total))
        minimo = max(20, int(unidades * 0.35))
        rows.append({"tipo": tipo, "unidades": unidades, "min_unidades": minimo})
    return pd.DataFrame(rows)


def seed_campanas(last_date: pd.Timestamp) -> pd.DataFrame:
    base = last_date.normalize()
    rows = [
        (base + pd.Timedelta(days=5), "Bello", "Jornada móvil — parque principal", "programada"),
        (base + pd.Timedelta(days=9), "Robledo", "Universidad — semana de donación", "programada"),
        (base + pd.Timedelta(days=16), "Belén", "Empresas — convocatoria O-", "borrador"),
    ]
    return pd.DataFrame(rows, columns=["fecha", "comuna", "titulo", "estado"]).assign(
        fecha=lambda d: d["fecha"].dt.strftime("%Y-%m-%d")
    )


# ── 3. Persistencia ──────────────────────────────────────────────────────────
def write_db(serie: pd.DataFrame, tau: float, threshold: float) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        serie.to_sql("serie_diaria", con, if_exists="replace", index=False)
        seed_stock().to_sql("stock", con, if_exists="replace", index=False)
        seed_campanas(pd.to_datetime(serie["fecha"]).max()).to_sql(
            "campanas", con, if_exists="replace", index=False
        )
        meta = pd.DataFrame(
            {
                "clave": ["tau", "threshold", "horizonte_dias", "actualizado"],
                "valor": [
                    f"{tau:.4f}", f"{threshold:.4f}", str(H),
                    datetime.now(timezone.utc).isoformat(timespec="seconds"),
                ],
            }
        )
        meta.to_sql("meta", con, if_exists="replace", index=False)
        con.execute("CREATE INDEX IF NOT EXISTS ix_serie_fecha ON serie_diaria(fecha)")


def main() -> None:
    print("Construyendo dataset de modelado…")
    m, features, tau = build_model_frame()
    print(f"  filas={len(m)}  features={len(features)}  τ={tau:.2f}")

    print("Entrenando XGBoost…")
    model, threshold = train(m, features)
    prob = model.predict_proba(m[features])[:, 1]
    pred = (prob >= threshold).astype(int)
    print(f"  umbral OOF (F{BETA:g})={threshold:.3f}  positivos_reales={int(m['escasez_t14'].sum())}")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    bundle = {
        "model": model, "features": features, "tau": tau,
        "threshold": threshold, "horizonte_dias": H,
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    model_path = MODELS_DIR / "escasez_model.pkl"
    joblib.dump(bundle, model_path)
    print(f"  modelo guardado en {model_path.relative_to(PROJECT_ROOT)}")

    serie = pd.DataFrame({
        "fecha": m["fecha"].dt.strftime("%Y-%m-%d"),
        "donaciones": m["donaciones"].round(2),
        "hospitalizados": m["hospitalizados"].round(2),
        "muertes_sangre": m["muertes_sangre"].round(2),
        "don_ma7": m["don_media_7d"].round(3),
        "dem_ma7": m["hosp_media_7d"].round(3),
        "presion": m["presion"].round(3),
        "prob_escasez": prob.round(4),
        "escasez_pred": pred,
        "escasez_real": m["escasez_t14"].astype(int),
    })
    write_db(serie, tau, threshold)
    print(f"  base de datos escrita en {DB_PATH.relative_to(PROJECT_ROOT)} "
          f"({len(serie)} días, {serie.shape[1]} columnas)")
    print("Listo.")


if __name__ == "__main__":
    main()
