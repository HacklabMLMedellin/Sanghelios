"""Ingesta: descarga los datos abiertos del HGM desde datos.gov.co.

Deja una copia espejo de los tres conjuntos publicados por el Hospital
General de Medellín en ``data/raw`` (mismo formato que la descarga manual
del portal, para que ``notebooks/01_preprocesamiento`` funcione sin cambios).

Uso:  ``uv run python -m src.data_pipeline.ingest``
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW = PROJECT_ROOT / "data" / "raw"

# Identificadores Socrata de los conjuntos en datos.gov.co.
DATASETS = {
    "banco_sangre.csv": "65is-zhxx",   # Banco de sangre HGM
    "atenciones.csv": "xm8g-qeac",     # Población atendida HGM
    "defunciones.csv": "hwwv-mhse",    # Defunciones ocurridas en el HGM
}
BASE_URL = "https://www.datos.gov.co/api/views/{id}/rows.csv?accessType=DOWNLOAD"


def download_all(dest: Path = RAW) -> None:
    """Descarga los tres conjuntos crudos al directorio ``dest``."""
    dest.mkdir(parents=True, exist_ok=True)
    for filename, dataset_id in DATASETS.items():
        url = BASE_URL.format(id=dataset_id)
        target = dest / filename
        print(f"Descargando {dataset_id} → {target.relative_to(PROJECT_ROOT)}")
        urllib.request.urlretrieve(url, target)
    print("Ingesta completa.")


if __name__ == "__main__":
    download_all()
