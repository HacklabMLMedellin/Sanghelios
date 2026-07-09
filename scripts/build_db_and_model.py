"""Exporta el modelo de escasez y construye la base de datos operativa.

Punto de entrada histórico; la implementación vive ahora en el paquete
``src`` siguiendo la estructura del proyecto:

- ``src/data_pipeline/transform.py``  → serie diaria consolidada
- ``src/features/build_features.py``  → features + objetivo ``escasez_t14``
- ``src/train.py``                    → entrenamiento, modelo y BD SQLite

Uso:  ``uv run python scripts/build_db_and_model.py``
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.train import main  # noqa: E402

if __name__ == "__main__":
    main()
