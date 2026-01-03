#!/usr/bin/env python3
import json
import sys
from datetime import date
from textwrap import dedent


def load_data(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_currency(value: float, currency: str) -> str:
    return f"{value:,.0f} {currency}".replace(",", " ")


def calc_roas(revenue: float, spend: float) -> float:
    return revenue / spend if spend else 0.0


def render_channel_section(channels: list, currency: str) -> str:
    lines = []
    for ch in channels:
        roas = calc_roas(ch.get("revenue", 0), ch.get("spend", 0))
        lines.append(
            f"- **{ch.get('name')}** — útrata {fmt_currency(ch.get('spend', 0), currency)}, "
            f"prokliky {ch.get('clicks', 0)}, konverze {ch.get('conversions', 0)}, "
            f"obrat {fmt_currency(ch.get('revenue', 0), currency)}, ROAS {roas:.2f}. "
            f"Pozn.: {ch.get('notes', '—')}"
        )
    return "\n".join(lines)


def render_template(data: dict) -> str:
    currency = data.get("currency", "CZK")
    totals = data.get("totals", {})
    channels = data.get("channels", [])
    changes = data.get("changes_vs_prev_week", {})
    upcoming = data.get("upcoming_events", [])

    roas = calc_roas(totals.get("revenue", 0), totals.get("spend", 0))
    change_lines = []
    if changes:
        for key, label in [
            ("spend_pct", "Útrata"),
            ("conversions_pct", "Konverze"),
            ("roas_pct", "ROAS"),
        ]:
            if key in changes:
                change_lines.append(f"- {label}: {changes[key]*100:+.1f}% vs. minulý týden")

    template = f"""
# PPC Weekly Report (fallback)

**Klient:** {data.get('client', '—')}  
**Období:** {data.get('period', '—')}  
**Generováno:** {date.today().isoformat()}

## Přehled výkonu
- Zobrazení: {totals.get('impressions', 0):,}\n- Prokliky: {totals.get('clicks', 0):,}\n- Útrata: {fmt_currency(totals.get('spend', 0), currency)}\n- Konverze: {totals.get('conversions', 0)}\n- Obrat: {fmt_currency(totals.get('revenue', 0), currency)}\n- ROAS: {roas:.2f}

## Mezitýdenní vývoj
{chr(10).join(change_lines) if change_lines else '- bez dat'}

## Kanály
{render_channel_section(channels, currency) if channels else '- bez dat'}

## Shrnutí
- Tento report je fallback verze bez AI generování textu.
- Použijte make_prompt.py pro vytvoření promtu a finálního textu přes AI.

## Další kroky
- Zkontrolujte blížící se události: {', '.join(upcoming) if upcoming else '—'}
- Vyhodnoťte doporučení a domluvte jejich realizaci s klientem.
"""
    return dedent(template).strip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python render_report.py <data.json>", file=sys.stderr)
        return 1
    path = argv[1]
    data = load_data(path)
    sys.stdout.write(render_template(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
