<div align="center">

<img src="../../RECURSOS/presentation/assets/logo.png" alt="Sanghelios" width="300">

# Arquitectura

**Del dato abierto a la campaña: pipeline batch + API + asistente generativo**

[README](../../README.md) · [Marco metodológico](../marco_metodologico.md) · [API](../api_spec.md) · [Diccionario](../data_dictionary.md)

</div>

---

## Vista general

```mermaid
flowchart LR
    subgraph Ingesta y preparación
        A[datos.gov.co<br>3 conjuntos HGM]:::dato -->|src/data_pipeline/ingest.py| B[data/raw]:::dato
        B -->|notebooks/02_limpieza_transformacion| C[data/processed<br>series diarias]:::dato
    end
    subgraph Modelado batch
        C -->|src/data_pipeline/transform.py| D[Serie consolidada]:::proceso
        D -->|src/features/build_features.py| E[50 features + escasez_t14]:::proceso
        E -->|src/train.py| F[models/predictive/<br>escasez_model.pkl]:::dato
        E -->|src/train.py| G[(data/sanghelios.db<br>SQLite)]:::dato
    end
    subgraph Servicio
        F -.->|src/inference.py| H[API FastAPI<br>src/app.py]:::api
        G --> H
        H --> I[Dashboard]:::producto
        H --> J[Mapa 3D]:::producto
        H --> K[Estudio de campañas]:::producto
        L[Gemini 2.5 Flash]:::externo <-->|src/agents/citizen_agent.py| H
    end

    classDef dato fill:#F6EFE4,stroke:#BF1212,color:#1a1714
    classDef proceso fill:#ffffff,stroke:#8a837a,color:#1a1714
    classDef api fill:#1F2937,stroke:#1F2937,color:#ffffff
    classDef producto fill:#BF1212,stroke:#BF1212,color:#ffffff
    classDef externo fill:#e8eaf6,stroke:#1F2937,color:#1a1714
```

## Componentes

| Componente | Ruta | Responsabilidad |
|---|---|---|
| **Ingesta** | `src/data_pipeline/ingest.py` | Espejo local de los conjuntos de datos.gov.co (Socrata) |
| **Transformación** | `src/data_pipeline/transform.py` | Series procesadas → serie diaria continua consolidada |
| **Features** | `src/features/build_features.py` | Presión, rezagos, estacionalidad y objetivo `escasez_t14` |
| **Entrenamiento** | `src/train.py` | XGBoost + umbral F2 out-of-fold; exporta modelo y BD |
| **Inferencia** | `src/inference.py` | Carga el bundle y predice probabilidad de escasez |
| **API + web** | `src/app.py` · `src/templates/` · `src/static/` | Rutas HTML y `/api/*` (serie, stock, campañas, meta) |
| **Agente ciudadano** | `src/agents/citizen_agent.py` | Asistente conversacional de campañas (Gemini + reglas de respaldo) y búsqueda de lugares |
| **Agente analista** | `src/agents/analyst_agent.py` | Reporte automático del estado del banco a partir de la BD operativa |
| **Flyers** | `src/tools/write_images.py` | Relleno de plantillas de afiches (PIL) |
| **Presentación** | `RECURSOS/presentation/` | Diapositivas Manim del proyecto |

## Decisiones de arquitectura

- **Batch, no streaming**: los datos abiertos se actualizan con baja frecuencia;
  un pipeline batch reproducible (`scripts/build_db_and_model.py`) es más simple
  y auditable que un flujo en tiempo real. `data/realtime/` queda reservado para
  una futura integración con el sistema transfusional del hospital.
- **SQLite como BD operativa**: una sola tabla diaria + stock + campañas; sin
  servidor de BD que administrar, ideal para réplica en otros hospitales.
- **Degradación elegante de la IA**: si no hay `GEMINI_API_KEY`, el asistente
  cae a un generador por reglas — la aplicación nunca depende de un servicio
  externo para funcionar.

---

<div align="center"><sub>Sanghelios · Hospital General de Medellín · 2026</sub></div>
