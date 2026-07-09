<div align="center">

<img src="../RECURSOS/presentation/assets/logo.png" alt="Sanghelios" width="300">

# Marco metodológico

**CRISP-ML(Q) aplicado al ciclo de vida del modelo `escasez_t14`**

[README](../README.md) · [Planteamiento](planteamiento_problema.md) · [Fuentes](fuentes_datos.md) · [Impacto público](public_impact_assessment.md) · [Validación](validación_guide.md)

</div>

---

El proyecto sigue **CRISP-ML(Q)** (Cross-Industry Standard Process for Machine
Learning with Quality assurance): seis fases con criterios de calidad por fase,
cada una con artefactos verificables en este repositorio.

| Fase | Qué se hizo | Artefacto |
|---|---|---|
| **1. Entendimiento del negocio y de los datos** | Pregunta central (¿anticipar la escasez con 14 días?), inventario de los 3 conjuntos abiertos del HGM y auditoría de calidad (huecos 2024, colapso 2023) | [planteamiento_problema.md](planteamiento_problema.md) · [fuentes_datos.md](fuentes_datos.md) |
| **2. Preparación de datos** | Limpieza, deduplicación, imputación del hueco enero–mayo 2024 y construcción de las tres series diarias | [`notebooks/02_limpieza_transformacion`](../notebooks/02_limpieza_transformacion.ipynb) · `data/processed/` · [`src/data_pipeline/`](../src/data_pipeline/) |
| **3. Ingeniería de características** | Presión demanda−oferta (media móvil 7d), rezagos, tendencias, estacionalidad cíclica y objetivo binario `escasez_t14` (50 features) | [`src/features/build_features.py`](../src/features/build_features.py) · [data_dictionary.md](data_dictionary.md) |
| **4. Modelado** | Regresión logística como línea base y **XGBoost** como modelo final; comparación en el notebook de modelado | [`notebooks/04_modelo_predictivo`](../notebooks/04_modelo_predictivo.ipynb) · [`src/train.py`](../src/train.py) |
| **5. Evaluación** | Validación temporal (`TimeSeriesSplit`, 5 folds), umbral de decisión out-of-fold optimizado con **F2** (prioriza recall) y pruebas automatizadas de equidad | [conclusiones.md](conclusiones.md) · [`tests/bias_tests/`](../tests/bias_tests/) |
| **6. Despliegue y monitoreo** | Modelo + BD operativa servidos por FastAPI (`/api/*`), imagen Docker y reentrenamiento programado por CI | [`src/app.py`](../src/app.py) · [`deployments/docker/`](../deployments/docker/) · [`.github/workflows/`](../.github/workflows/) |

## Decisiones metodológicas clave

- **Validación temporal, nunca aleatoria.** Las particiones respetan el orden
  cronológico (el 20 % final se reserva para test); mezclar fechas filtraría
  información del futuro.
- **El umbral τ se calcula solo con el tramo de entrenamiento** (percentil 75
  de la presión) para evitar fuga de datos hacia el objetivo.
- **F2 en lugar de F1**: en un banco de sangre, no detectar una escasez cuesta
  más que una falsa alarma; el umbral de decisión se elige out-of-fold
  maximizando F-beta con β = 2.
- **Reentrenamiento reproducible**: `uv run python scripts/build_db_and_model.py`
  reconstruye modelo y base de datos desde los CSV procesados con semilla fija.

---

<div align="center"><sub>Sanghelios · Hospital General de Medellín · 2026</sub></div>
