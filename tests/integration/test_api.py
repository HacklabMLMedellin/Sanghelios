"""Pruebas de integración: la API FastAPI contra la BD operativa real.

Requieren ``data/sanghelios.db`` (versionada; se reconstruye con
``scripts/build_db_and_model.py``). Se ejecutan desde la raíz del repo.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi.testclient import TestClient  # noqa: E402

from src.app import app  # noqa: E402

client = TestClient(app)


def test_inicio_responde():
    assert client.get("/").status_code == 200


def test_serie_diaria_devuelve_columnas_del_modelo():
    r = client.get("/api/serie-diaria", params={"desde": "2025-01-01"})
    assert r.status_code == 200
    filas = r.json()
    assert filas, "la serie no debe venir vacía"
    esperadas = {"fecha", "donaciones", "presion", "prob_escasez", "escasez_pred"}
    assert esperadas.issubset(filas[0].keys())
    fechas = [f["fecha"] for f in filas]
    assert fechas == sorted(fechas), "la serie debe venir ordenada por fecha"


def test_stock_cubre_los_ocho_grupos():
    r = client.get("/api/stock")
    assert r.status_code == 200
    tipos = {fila["tipo"] for fila in r.json()}
    assert tipos == {"O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"}


def test_meta_expone_parametros_del_modelo():
    r = client.get("/api/meta")
    assert r.status_code == 200
    meta = r.json()
    assert {"tau", "threshold", "horizonte_dias"}.issubset(meta.keys())
    assert float(meta["tau"]) > 0
    assert int(meta["horizonte_dias"]) == 14


def test_asistente_campana_funciona_sin_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    r = client.post("/api/asistente-campana", json={"comuna": "Robledo", "tipo": "O-"})
    assert r.status_code == 200
    out = r.json()
    assert out["mensaje"]
