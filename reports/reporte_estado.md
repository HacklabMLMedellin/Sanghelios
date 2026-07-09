# Reporte de estado — Banco de Sangre HGM

*Generado automáticamente por `src/agents/analyst_agent.py` el 2026-07-09 19:05 UTC (datos hasta 2025-06-13).*

## Situación general: 🟢 Normal

- **Presión actual** (demanda − oferta, media 7d): 8.3 frente a un umbral τ = 28.6.
- **Riesgo de escasez a 14 días**: 0.1%.
- Presión media de los últimos 30 días: 11.3; días en alerta del modelo: 0 de 30.
- Donaciones del último día registrado: 20.

## Stock por grupo sanguíneo

| Tipo | Unidades | Mínimo seguro | Estado |
|---|--:|--:|---|
| O+ | 752 | 263 | OK |
| A+ | 357 | 124 | OK |
| O- | 126 | 44 | OK |
| B+ | 90 | 31 | OK |
| A- | 39 | 20 | OK |
| AB+ | 22 | 20 | OK |
| B- | 11 | 20 | ⚠️ bajo mínimo |
| AB- | 3 | 20 | ⚠️ bajo mínimo |

## Campañas registradas

| Fecha | Comuna | Campaña | Estado |
|---|---|---|---|
| 2025-06-18 | Bello | Jornada móvil — parque principal | programada |
| 2025-06-22 | Robledo | Universidad — semana de donación | programada |
| 2025-06-29 | Belén | Empresas — convocatoria O- | borrador |

---
*Sanghelios · reporte reproducible: los números salen de `data/sanghelios.db`,* *reconstruible con `scripts/build_db_and_model.py`.*
