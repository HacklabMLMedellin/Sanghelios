# Reports — resultados visibles

Todo lo que hay aquí es **generado y reproducible**:

| Artefacto | Cómo se genera |
|---|---|
| `figures/distribuciones.png` | [`notebooks/05_reportes_automaticos`](../notebooks/05_reportes_automaticos.ipynb) — distribución de oferta, demanda y presión |
| `figures/correlaciones.png` | ídem — correlaciones entre las series diarias |
| `figures/matriz_confusion.png` | ídem — desempeño del modelo en el 20 % final (test temporal) |
| `reporte_estado.md` | `uv run python -m src.agents.analyst_agent` — estado del banco desde la BD operativa |
| `reporte_final.html` | Copia del informe EDA editorial (autocontenido, se abre en el navegador; en la app vive en `/sanghelios-informe-eda`) |
