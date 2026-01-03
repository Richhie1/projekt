#!/usr/bin/env python3
import json
import sys
from textwrap import dedent


def load_data(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_currency(value: float, currency: str) -> str:
    return f"{value:,.0f} {currency}".replace(",", " ")


def build_prompt(data: dict) -> str:
    client = data.get("client", "Klient")
    period = data.get("period", "")
    currency = data.get("currency", "CZK")
    totals = data.get("totals", {})
    channels = data.get("channels", [])
    benchmarks = data.get("benchmarks", {})
    changes = data.get("changes_vs_prev_week", {})
    upcoming = data.get("upcoming_events", [])

    lines = []
    lines.append(f"Generuj týdenní PPC report pro {client} (období {period}).")
    lines.append("Piš česky, stručně, obchodně a věcně.")
    lines.append("Rozsah: max 6 vět shrnutí, body pro další sekce.")
    lines.append("Zahrň čísla přímo v textu, nepřidávej data, která nemáme.")
    lines.append("")
    lines.append("Dostupná data (souhrn):")
    lines.append(f"- Zobrazení: {totals.get('impressions', 0):,}".replace(",", " "))
    lines.append(f"- Prokliky: {totals.get('clicks', 0):,}".replace(",", " "))
    lines.append(f"- Útrata: {format_currency(totals.get('spend', 0), currency)}")
    lines.append(f"- Konverze: {totals.get('conversions', 0)}")
    if totals.get("revenue") is not None:
        lines.append(f"- Obrat: {format_currency(totals.get('revenue', 0), currency)}")

    if changes:
        lines.append("- Mezitýdenní vývoj:")
        for key, label in [
            ("spend_pct", "Útrata"),
            ("conversions_pct", "Konverze"),
            ("roas_pct", "ROAS"),
        ]:
            if key in changes:
                pct = changes[key] * 100
                lines.append(f"  - {label}: {pct:+.1f}% vs. minulý týden")

    if channels:
        lines.append("")
        lines.append("Kanály:")
        for ch in channels:
            lines.append(
                f"- {ch.get('name')}: útrata {format_currency(ch.get('spend', 0), currency)}, "
                f"prokliky {ch.get('clicks', 0)}, konverze {ch.get('conversions', 0)}, "
                f"obrat {format_currency(ch.get('revenue', 0), currency)}. "
                f"Pozn.: {ch.get('notes', '—')}"
            )

    if benchmarks:
        lines.append("")
        lines.append("Interní benchmarky (pro kontext, ne jako KPI):")
        for key, label in [
            ("click_through_rate", "CTR"),
            ("conversion_rate", "CR"),
            ("cost_per_conversion", "CPCo"),
            ("roas", "ROAS"),
        ]:
            if key in benchmarks:
                value = benchmarks[key]
                if key in {"click_through_rate", "conversion_rate", "roas"}:
                    lines.append(f"- {label}: {value}")
                else:
                    lines.append(f"- {label}: {format_currency(value, currency)}")

    if upcoming:
        lines.append("")
        lines.append("Blížící se události:")
        for item in upcoming:
            lines.append(f"- {item}")

    lines.append("")
    lines.append(dedent(
        """
        Struktura výstupu:
        1) Shrnutí (max 6 vět).
        2) Co šlo dobře / co nefungovalo.
        3) 5 doporučení, každé uveď jako: [P1–P3] Doporučení — očekávaný dopad.
        4) 3 rizika/varování s krátkým kontextem.
        5) Max 5 dotazů na klienta.
        Styl: konkrétně, bez výplně, uváděj data a trendy, zdůrazni priority.
        """
    ).strip())

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python make_prompt.py <data.json>", file=sys.stderr)
        return 1
    data_path = argv[1]
    data = load_data(data_path)
    prompt = build_prompt(data)
    sys.stdout.write(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
