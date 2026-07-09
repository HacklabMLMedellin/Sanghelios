# Serverless

Reservado para funciones lambda de reportes automatizados. El candidato
natural es `src/agents/analyst_agent.py`, que ya genera el reporte de estado
(`reports/reporte_estado.md`) como función pura sobre la BD operativa; hoy se
orquesta con GitHub Actions ([data-update-cron.yml](../../.github/workflows/data-update-cron.yml)).
