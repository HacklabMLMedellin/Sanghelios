"""Pruebas automatizadas de equidad y sesgo algorítmico.

Verifican las políticas de ``config/security_policy.json``:

1. El modelo ``escasez_t14`` no usa atributos sensibles ni demográficos —
   sus features son transformaciones de series agregadas.
2. Los datos procesados no contienen identificadores directos de personas.
"""

import json
from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "predictive" / "escasez_model.pkl"
PROCESSED = PROJECT_ROOT / "data" / "processed"
POLICY = PROJECT_ROOT / "config" / "security_policy.json"

# Atributos que jamás deben entrar al modelo predictivo.
ATRIBUTOS_SENSIBLES = (
    "edad", "sexo", "genero", "comuna", "barrio", "estrato",
    "raza", "etnia", "rh", "imc", "eps", "ocupacion", "grupo_sang",
)


def test_features_del_modelo_sin_atributos_sensibles():
    bundle = joblib.load(MODEL_PATH)
    for feature in (f.lower() for f in bundle["features"]):
        culpables = [a for a in ATRIBUTOS_SENSIBLES if a in feature]
        assert not culpables, (
            f"la feature '{feature}' contiene el atributo sensible {culpables}"
        )


def test_datos_procesados_sin_identificadores_directos():
    prohibidas = json.loads(POLICY.read_text(encoding="utf-8"))[
        "anonimizacion"
    ]["columnas_prohibidas"]
    for csv in PROCESSED.glob("*.csv"):
        columnas = pd.read_csv(csv, nrows=0).columns.str.lower()
        for col in columnas:
            culpables = [p for p in prohibidas if p in col]
            assert not culpables, (
                f"{csv.name}: la columna '{col}' parece un identificador {culpables}"
            )
