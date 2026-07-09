# Changelog

Registro cronológico de versiones y cambios (resumen del historial de commits).

## 2026-07-09
- **Reorganización al formato "Avanzado" del proyecto abierto de IA**:
  - Notebooks renumerados `01`–`05`; nuevos `01_EDA_exploracion_datos` y
    `05_reportes_automaticos` (ejecutados, con salidas).
  - Pipeline extraído a `src/`: `data_pipeline/` (ingesta datos.gov.co +
    transformación), `features/`, `train.py` e `inference.py`;
    `scripts/build_db_and_model.py` queda como punto de entrada.
  - `src/campaign_ai.py` → `src/agents/citizen_agent.py`; nuevo
    `src/agents/analyst_agent.py` (reporte automático → `reports/reporte_estado.md`).
  - Modelo movido a `models/predictive/`; `models/llm_rag/` y `models/simulation/` reservados.
  - Docs nuevos: `marco_metodologico.md` (CRISP-ML), `public_impact_assessment.md`,
    `validación_guide.md` y `docs/architecture/`.
  - Infraestructura: workflows de CI y cron de datos (`.github/workflows/`),
    `CODEOWNERS`, `config/` (base, hiperparámetros, política de seguridad),
    `deployments/` (Docker api/inference, Kubernetes, serverless) y `environment.yml`.
  - Tests nuevos de integración de la API (`tests/integration`) y de equidad
    algorítmica (`tests/bias_tests`); figuras del reporte en `reports/figures/`.
  - Capturas del sitio organizadas en `RECURSOS/screenshots/` y enlazadas en el README.
  - Presentación Manim movida a `RECURSOS/presentation/`; copia del informe EDA
    como `reports/reporte_final.html`; video de presentación enlazado en el README.

## 2026-07-05
- Frontend responsive en todos los módulos.

## 2026-07-04
- Presentación Manim terminada; página de inicio actualizada.

## 2026-07-02
- "El mega sprint": mejoras generales de la web y cierre de pendientes en
  todos los módulos.

## 2026-07-01
- Reorganización del proyecto: `core/` → `src/`, nueva carpeta `docs/`
  (planteamiento, diccionario de datos, API, conclusiones, fuentes), `tests/unit`,
  `requirements.txt` exportado desde uv y este changelog.
- Eliminado el venv redundante `.venv-sanghelios/`; imágenes sueltas movidas a
  `src/static/img/`.

## 2026-06-30
- Modelo `escasez_t14` exportado a `models/escasez_model.pkl`; BD operativa
  `data/sanghelios.db` generada desde los CSV (script `scripts/build_db_and_model.py`).
- API de datos: `/api/serie-diaria`, `/api/stock`, `/api/campanas`, `/api/meta`.
- Dashboard conectado a datos reales (τ fijo p75) con caducidad de donaciones a 40 días.
- Estudio de campañas unificado (Campaña + Genera imágenes) con asistente IA
  (`/api/asistente-campana`, Gemini 2.5 Flash + fallback por reglas); generador de
  afiches multiplataforma (fuentes Windows/Linux/matplotlib).
- Navegación del sitio unificada (pestañas con delegación de eventos, estáticos no-cache).

## 2026-06-29
- Rework editorial del reporte EDA (`/sanghelios-informe-eda`): nota periodística,
  grafo interactivo de compatibilidad, matriz ABO/Rh, índice y conclusiones.
- Favicon del sitio.

## 2026-06-28
- Barra de navegación implementada e integrada en todas las páginas.

## 2026-06-27
- Mapa: vuelo de cámara al seleccionar un lugar, capa de Venezuela y correcciones.
- Interfaz web del generador de imágenes para campañas de donación.

## 2026-06-26
- Base del generador de imágenes de campañas.
- Formulario "¿puedo donar?" (validación de aptitud del donante).
- Organización inicial del frontend; notebooks y README actualizados.

## 2026-06-24 – 2026-06-25
- Series de tiempo añadidas al análisis.
- Script generador de imágenes para eventos de donación y personas.
- Ajustes de la interfaz web; avance de la presentación.

## 2026-06-22 – 2026-06-23
- Informe EDA (primera versión) e índice de notebooks.
- Inicio de la presentación en Manim.
- Fix del clustering del banco de sangre; limpieza del repo (`.gitignore`, submódulo accidental).

## 2026-06-16 – 2026-06-17
- Notebooks de EDA y clustering para el análisis del banco de sangre.

## 2026-06-06
- Primer modelo entrenado; `utils/` de notebooks añadidos.

## 2026-06-03 – 2026-06-04
- Preprocesamiento de atenciones y su serie de tiempo; fix de la serie del banco de sangre.

## 2026-05-27 – 2026-05-28
- Fix del manejo de centroides de K-Prototypes; dataset con clusters guardado.
- Información de autoría en el notebook de EDA.

## 2026-05-22
- Limpieza del banco de sangre finalizada; creación del dataset de series de tiempo.

## 2026-05-15 – 2026-05-16
- Preprocesamiento del banco de sangre e ingeniería de características.

## 2026-05-13
- Frontend básico (FastAPI + templates) y pre-commit configurado.

## 2026-05-09 – 2026-05-10
- Limpieza de banco de sangre y atenciones (faltaban defunciones).
- Primera versión web; unificación de notebooks.
- Estructura inicial del proyecto (carpetas, `pyproject.toml`, venv).

## 2026-05-08
- Commit inicial del repositorio.
