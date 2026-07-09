"""Matriz de características y objetivo ``escasez_t14``.

Parte de la serie diaria consolidada (``src.data_pipeline.transform``) y
construye las variables del modelo: medias móviles, presión demanda-oferta,
rezagos, tendencias y estacionalidad. El objetivo es binario: ¿la presión
superará el umbral τ (p75 del tramo de entrenamiento) dentro de 14 días?
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.data_pipeline.transform import build_daily_series

H = 14            # horizonte de predicción (días)
TEST_FRAC = 0.2   # proporción final reservada para test


def build_model_frame() -> tuple[pd.DataFrame, list[str], float]:
    """Devuelve (frame de modelado, nombres de features, umbral τ)."""
    m = build_daily_series()

    m["demanda"] = m["hospitalizados"] + m["muertes_sangre"]
    for w in (7, 14, 28):
        m[f"don_ma{w}"] = m["donaciones"].rolling(w).mean()
        m[f"dem_ma{w}"] = m["demanda"].rolling(w).mean()
    m["don_media_7d"] = m["don_ma7"]
    m["hosp_media_7d"] = m["dem_ma7"]

    m["presion"] = m["hosp_media_7d"] - m["don_media_7d"]
    for w in (7, 14, 28):
        m[f"presion_ma{w}"] = m["presion"].rolling(w).mean()
        m[f"presion_std{w}"] = m["presion"].rolling(w).std()
    m["presion_ewm"] = m["presion"].ewm(span=14).mean()

    m["deficit_relativo"] = (
        (m["hosp_media_7d"] - m["don_media_7d"])
        / m["hosp_media_7d"].replace(0, np.nan)
    )

    for lag in (1, 3, 7, 14, 21, 28):
        m[f"presion_lag_{lag}"] = m["presion"].shift(lag)
        m[f"don_ma7_lag_{lag}"] = m["don_media_7d"].shift(lag)
        m[f"dem_ma7_lag_{lag}"] = m["hosp_media_7d"].shift(lag)
    for lag in (1, 7, 14):
        m[f"deficit_lag_{lag}"] = m["deficit_relativo"].shift(lag)

    m["tend_presion_7d"] = m["presion"] - m["presion"].shift(7)
    m["tend_presion_14d"] = m["presion"] - m["presion"].shift(14)
    m["delta_presion_1d"] = m["presion"] - m["presion"].shift(1)

    m["mes"] = m["fecha"].dt.month
    _doy = m["fecha"].dt.dayofyear
    _dow = m["fecha"].dt.dayofweek
    m["mes_sin"] = np.sin(2 * np.pi * m["mes"] / 12)
    m["mes_cos"] = np.cos(2 * np.pi * m["mes"] / 12)
    m["doy_sin"] = np.sin(2 * np.pi * _doy / 365)
    m["doy_cos"] = np.cos(2 * np.pi * _doy / 365)
    m["es_fin_semana"] = (_dow >= 5).astype(int)

    m["presion_futura"] = m["presion"].shift(-H)

    _excluir = ["fecha", "demanda", "presion_futura"]
    _cols_feat = [c for c in m.columns if c not in _excluir]
    m = m.dropna(subset=_cols_feat).reset_index(drop=True)
    m = m.drop(columns=["demanda"])

    n_obj = int(m["presion_futura"].notna().sum())
    split_tau = int(n_obj * (1 - TEST_FRAC))
    tau = float(m["presion"].iloc[:split_tau].quantile(0.75))

    m["escasez_t14"] = (m["presion_futura"] > tau).astype("Int64")
    m = m.dropna(subset=["presion_futura"]).reset_index(drop=True)
    m["escasez_t14"] = m["escasez_t14"].astype(int)
    m = m.drop(columns=["presion_futura"])

    features = [c for c in m.columns if c not in ("fecha", "escasez_t14")]
    return m, features, tau
