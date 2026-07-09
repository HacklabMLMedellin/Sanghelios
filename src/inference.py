"""Pipeline de inferencia: carga el modelo entrenado y predice escasez.

Uso programático::

    from src.inference import predict_latest
    print(predict_latest())

Uso por consola:  ``uv run python -m src.inference``
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "predictive" / "escasez_model.pkl"


def load_bundle(path: Path = MODEL_PATH) -> dict:
    """Carga el bundle {model, features, tau, threshold, horizonte_dias}."""
    return joblib.load(path)


def predict_proba(frame: pd.DataFrame, bundle: dict | None = None) -> pd.Series:
    """Probabilidad de escasez a ``horizonte_dias`` para cada fila del frame."""
    if bundle is None:
        bundle = load_bundle()
    proba = bundle["model"].predict_proba(frame[bundle["features"]])[:, 1]
    return pd.Series(proba, index=frame.index, name="prob_escasez")


def predict_latest() -> dict:
    """Predicción para el día más reciente disponible en la serie."""
    from src.features.build_features import build_model_frame

    bundle = load_bundle()
    m, features, _ = build_model_frame()
    last = m.iloc[[-1]]
    prob = float(bundle["model"].predict_proba(last[features])[:, 1][0])
    return {
        "fecha": str(last["fecha"].iloc[0].date()),
        "prob_escasez": round(prob, 4),
        "alerta": bool(prob >= bundle["threshold"]),
        "umbral": round(float(bundle["threshold"]), 4),
        "horizonte_dias": int(bundle["horizonte_dias"]),
    }


if __name__ == "__main__":
    print(predict_latest())
