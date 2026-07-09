"""Transformación: series procesadas → serie diaria consolidada.

Une las tres series de ``data/processed`` (donaciones, hospitalizaciones y
defunciones asociadas a sangre) en un DataFrame diario continuo, que es la
entrada de la ingeniería de características (``src.features``).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = PROJECT_ROOT / "data" / "processed"

DATE_START = "2022-01-02"
DATE_END = "2025-06-27"


def build_daily_series() -> pd.DataFrame:
    """Serie diaria continua: donaciones, hospitalizados y muertes por sangre."""
    don = pd.read_csv(PROCESSED / "df_banco_sangre_times_series.csv")
    hosp = pd.read_csv(PROCESSED / "df_hospitalizados_time_series.csv")
    muertes = pd.read_csv(PROCESSED / "df_defunciones_sangre_time_series.csv")

    idx = pd.date_range(DATE_START, DATE_END, freq="D", name="fecha")

    def daily(df: pd.DataFrame, fecha_col: str, val_col: str, name: str) -> pd.Series:
        s = df.assign(fecha=pd.to_datetime(df[fecha_col]))
        return (
            s.set_index("fecha")[val_col].resample("D").sum()
            .reindex(idx, fill_value=0).rename(name)
        )

    ser_don = daily(don, "fecha_extraccion", "donaciones_diarias", "donaciones")
    ser_hosp = daily(hosp, "fecha_atencion", "hospitalizaciones_diarias", "hospitalizados")
    ser_mue = daily(muertes, "fecha_defuncion", "defunciones_diarias", "muertes_sangre")

    return pd.concat([ser_don, ser_hosp, ser_mue], axis=1).reset_index()
