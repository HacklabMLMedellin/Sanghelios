<div align="center">

<img src="../RECURSOS/presentation/assets/logo.png" alt="Sanghelios" width="300">

# Guía de validación

**Cómo reproducir y verificar los resultados, paso a paso**

[README](../README.md) · [Marco metodológico](marco_metodologico.md) · [API](api_spec.md) · [Conclusiones](conclusiones.md)

</div>

---

Todo el proyecto es reproducible desde los CSV versionados en `data/`.
Requisitos: Python 3.13 y [uv](https://docs.astral.sh/uv/).

## 1. Instalar dependencias

```bash
git clone https://github.com/HacklabMLMedellin/Sanghelios
cd Sanghelios
uv sync
```

## 2. (Opcional) Refrescar los datos crudos

Descarga los tres conjuntos desde datos.gov.co a `data/raw/`:

```bash
uv run python -m src.data_pipeline.ingest
```

> Los CSV crudos ya están versionados como espejo, así que este paso solo es
> necesario si se quiere validar contra la fuente viva.

## 3. Reconstruir modelo y base de datos

```bash
uv run python scripts/build_db_and_model.py
```

Salida esperada (semilla fija, resultados deterministas):

```
Construyendo dataset de modelado…
  filas=1169  features=50  τ=28.57
Entrenando XGBoost…
  umbral OOF (F2)=0.008  positivos_reales=234
  modelo guardado en models/predictive/escasez_model.pkl
  base de datos escrita en data/sanghelios.db (1169 días, 10 columnas)
```

## 4. Ejecutar las pruebas

```bash
uv run pytest tests -v          # unitarias + integración + sesgo
uv run ruff check src scripts tests
```

Debe pasar todo: pruebas del asistente de campañas (`tests/unit`), de la API
(`tests/integration`) y de equidad del modelo (`tests/bias_tests`).

## 5. Verificar una predicción

```bash
uv run python -m src.inference
# → {'fecha': '2025-06-13', 'prob_escasez': ..., 'alerta': ..., 'umbral': ..., 'horizonte_dias': 14}
```

## 6. Levantar la aplicación web

```bash
uv run uvicorn src.app:app --port 8000
```

| Verificar | URL |
|---|---|
| Inicio | http://localhost:8000/ |
| Dashboard con datos reales | http://localhost:8000/dashboard |
| Serie diaria (JSON) | http://localhost:8000/api/serie-diaria |
| Metadatos del modelo (τ, umbral) | http://localhost:8000/api/meta |
| Informe EDA | http://localhost:8000/sanghelios-informe-eda |

> El asistente de campañas usa Gemini si `GEMINI_API_KEY` está en `.env`;
> sin la clave funciona el generador por reglas (así lo validan los tests).

## 7. Validar los notebooks

Los notebooks se ejecutan en orden: `01_EDA_exploracion_datos` →
`02_limpieza_transformacion` → `03_analisis_descriptivo` →
`04_modelo_predictivo` → `05_reportes_automaticos`. Cada uno parte de los
archivos que deja el anterior en `data/processed/`.

---

<div align="center"><sub>Sanghelios · Hospital General de Medellín · 2026</sub></div>
