# SUBMISSION

## Popis řešení
- Mini nástroj generuje prompt pro AI z PPC dat a přidává fallback šablonu bez AI.
- Struktura výstupu je pevně definovaná (shrnutí, plusy/mínusy, 5 doporučení s prioritou, 3 rizika, 5 dotazů), takže report je konzistentní a klient-ready.
- Data se propisují přímo do promptu i fallbacku, aby nedocházelo k domýšlení čísel.

## Důkaz
- Ukaž screenshoty / soubory: `PROMPT.txt`, `report.md`, `data/example.json`, `report_fallback.md`.
- Přilož výpis příkazů:
  - `python src/make_prompt.py data/example.json > PROMPT.txt`
  - `python src/render_report.py data/example.json > report_fallback.md`

## Dopad
- Příprava týdenního reportu z ~60 minut na ~15 minut díky hotovému promptu a šabloně (−75 % času) + konzistentní struktura výstupu.
- Lze použít i v režimu bez AI (fallback), takže reporting neblokuje nedostupnost modelu.

## Checklist k odevzdání
- [ ] Aktualizován JSON s reálnými čísly klienta.
- [ ] Znovu spuštěn `make_prompt.py` a uložen prompt do `PROMPT.txt`.
- [ ] Vygenerován finální report přes AI do `report.md` (nebo fallback `report_fallback.md`).
- [ ] Přiloženy screenshoty/soubory dle sekce Důkaz.
