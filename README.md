# AI PPC Weekly Report Generator

Rychlý mini-projekt, který vyrobí vstupní prompt pro AI a fallback report z PPC dat bez externích knihoven. Cíl: aby PPC specialista připravil kvalitní týdenní report za pár minut.

## Co je uvnitř
- `data/example.json` – ukázková vstupní data (lze přepsat vlastními čísly).
- `src/make_prompt.py` – vytvoří klientsky použitelný prompt pro AI.
- `src/render_report.py` – vygeneruje základní fallback report bez AI.
- `PROMPT.txt` – prompt vygenerovaný z `example.json` (lze přepsat).
- `report.md` – hotový report v češtině podle promptu a dat.
- `report_fallback.md` – ukázka fallback reportu z šablony.
- `SUBMISSION.md` – shrnutí řešení, důkaz, dopad pro odevzdání.

## Jak použít s vlastními daty (≈10 minut)
1. **Zkopíruj JSON**: Přepiš `data/example.json` vlastními čísly (klient, období, kanály, rozpočet, konverze, poznámky, benchmarky, změny vs. předchozí týden a chystané události).
2. **Vygeneruj prompt**: `python src/make_prompt.py data/example.json > PROMPT.txt`
3. **Vytvoř AI text**: Pošli obsah `PROMPT.txt` do vybraného modelu (např. GPT-4o) a výstup ulož do `report.md`.
4. **Fallback varianta**: `python src/render_report.py data/example.json > report_fallback.md` – použij, když není k dispozici AI.
5. **Hotovo**: `report.md` odevzdej klientovi, případně uprav doporučení a otázky podle feedbacku.

## Předpoklady
- Python 3.11+ (bez dalších balíčků).
- Soubor JSON ve struktuře podobné `data/example.json`.

## Poznámky k úpravám
- Počet doporučení, rizik a dotazů je pevně dán promptem (5/3/5).
- Vstupní data se zobrazují v promptu, aby model pracoval s čísly, která opravdu máme.
- Fallback report drží jasnou strukturu, takže je použitelný bez modelu.
