"""Agente analista: reportes automáticos basados en los datos operativos.

Lee la base ``data/sanghelios.db`` y redacta un informe Markdown con el
estado del banco de sangre: presión demanda−oferta de los últimos 30 días
frente al umbral τ, riesgo del modelo ``escasez_t14``, stock por grupo
sanguíneo y campañas registradas.

Uso:  ``uv run python -m src.agents.analyst_agent``  → ``reports/reporte_estado.md``
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "sanghelios.db"
REPORT_PATH = PROJECT_ROOT / "reports" / "reporte_estado.md"


def _query(sql: str, params: tuple = ()) -> list[dict]:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in con.execute(sql, params).fetchall()]
    finally:
        con.close()


def build_report() -> str:
    meta = {r["clave"]: r["valor"] for r in _query("SELECT clave, valor FROM meta")}
    tau = float(meta["tau"])
    horizonte = meta["horizonte_dias"]

    serie = _query(
        "SELECT fecha, donaciones, presion, prob_escasez, escasez_pred "
        "FROM serie_diaria ORDER BY fecha DESC LIMIT 30"
    )
    ultimo = serie[0]
    presion_media = sum(r["presion"] for r in serie) / len(serie)
    dias_alerta = sum(r["escasez_pred"] for r in serie)

    stock = _query("SELECT tipo, unidades, min_unidades FROM stock ORDER BY unidades DESC")
    criticos = [r["tipo"] for r in stock if r["unidades"] <= r["min_unidades"]]
    campanas = _query("SELECT fecha, comuna, titulo, estado FROM campanas ORDER BY fecha")

    estado = "🔴 ALERTA" if ultimo["escasez_pred"] else "🟢 Normal"
    lineas = [
        "# Reporte de estado — Banco de Sangre HGM",
        "",
        f"*Generado automáticamente por `src/agents/analyst_agent.py` el "
        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} "
        f"(datos hasta {ultimo['fecha']}).*",
        "",
        f"## Situación general: {estado}",
        "",
        f"- **Presión actual** (demanda − oferta, media 7d): {ultimo['presion']:.1f} "
        f"frente a un umbral τ = {tau:.1f}.",
        f"- **Riesgo de escasez a {horizonte} días**: {ultimo['prob_escasez']:.1%}.",
        f"- Presión media de los últimos 30 días: {presion_media:.1f}; "
        f"días en alerta del modelo: {dias_alerta} de {len(serie)}.",
        f"- Donaciones del último día registrado: {ultimo['donaciones']:.0f}.",
        "",
        "## Stock por grupo sanguíneo",
        "",
        "| Tipo | Unidades | Mínimo seguro | Estado |",
        "|---|--:|--:|---|",
    ]
    for r in stock:
        marca = "⚠️ bajo mínimo" if r["tipo"] in criticos else "OK"
        lineas.append(f"| {r['tipo']} | {r['unidades']} | {r['min_unidades']} | {marca} |")

    lineas += ["", "## Campañas registradas", ""]
    if campanas:
        lineas += ["| Fecha | Comuna | Campaña | Estado |", "|---|---|---|---|"]
        lineas += [
            f"| {c['fecha']} | {c['comuna']} | {c['titulo']} | {c['estado']} |"
            for c in campanas
        ]
    else:
        lineas.append("Sin campañas registradas.")

    lineas += [
        "",
        "---",
        "*Sanghelios · reporte reproducible: los números salen de `data/sanghelios.db`,*"
        " *reconstruible con `scripts/build_db_and_model.py`.*",
        "",
    ]
    return "\n".join(lineas)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(), encoding="utf-8")
    print(f"Reporte escrito en {REPORT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
