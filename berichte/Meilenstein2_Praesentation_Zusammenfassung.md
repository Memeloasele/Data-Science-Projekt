# Meilenstein 2 — Präsentations-Zusammenfassung

Folien-Gerüst mit Kernzahlen, Sprechpunkten und passender Grafik je Folie.
Alle Grafiken: `Grafiken Meme/`.

---

## Folie 1 — Überblick / Ziel

**Datengrundlage:** Open Food Facts — ~4,5 Mio. Produkte, ursprünglich 210 Spalten.

**Ziel von Meilenstein 2:** Datensatz bereinigen und auf das Wesentliche reduzieren, damit er analysierbar wird.

**Was wir gemacht haben (3 Schritte):**
1. Redundante Varianten-Spalten zusammenführen (z. B. `packaging` / `packaging_tags` / `packaging_en`)
2. Fast leere Spalten entfernen (Füllgrenze 6 %): **180 → 70 Spalten**
3. Kernspalten inhaltlich bereinigen & normalisieren

---

## Folie 2 — Spaltenreduktion: die 6%-Entscheidung
> Grafik: `m2_reduktion_tradeoff.png`

- Getestet: Füllgrenzen von 5 % bis 50 %
- **Gewählt: 6 %** → 110 Spalten entfernt, aber **nur 4,71 % der Daten verloren**
- Höhere Grenzen lohnen nicht: 50 % würde **39,4 %** der Daten kosten
- **Sweet Spot:** maximaler Aufräumeffekt bei minimalem Verlust

**Sprechsatz:** „Wir entfernen über die Hälfte der Spalten und verlieren dabei nur rund 5 % aller Werte."

---

## Folie 3 — Ergebnis der Reduktion
> Grafik: `m2_reduktion_donut.png`

- **180 → 70 Spalten** (61 % entfernt)
- Entfernt: v. a. extrem seltene Nährstoff-Details (einzelne Fettsäuren, Vitamine) und Metadaten
- Ergebnis-Datei: `openfoodfacts_ueber6prozent.csv.zip`

---

## Folie 4 — Bereinigung der 4 Kernspalten
> Grafik: `m2_befuellungsgrad.png`

Bereinigt: `product_name`, `ingredients_analysis_tags`, `nova_group`, `nutrient_levels_tags`

| Spalte | Befüllung |
|:---|---:|
| product_name | 92,6 % |
| nutrient_levels_tags | 33,8 % |
| ingredients_analysis_tags | 30,1 % |
| nova_group | 25,1 % |

**Sprechsatz:** „Nur der Produktname ist nahezu vollständig — die wertvollen Klassifikations-Spalten gibt es nur bei einem Viertel bis Drittel der Produkte."

---

## Folie 5 — Inhaltlicher Top-Befund: Verarbeitungsgrad
> Grafik: `m2_nova_verteilung.png`

- **63,8 % der klassifizierten Produkte sind NOVA 4 = hochverarbeitet**
- Nur 11,9 % unverarbeitet (NOVA 1)
- Klare Botschaft: Der Datensatz ist von Fertigprodukten dominiert

---

## Folie 6 — Nährwerte & Zutaten-Analyse
> Grafiken: `m2_naehrwert_level.png`, `m2_zutaten_analyse.png`

- **Nährwert-Level:** Zucker meist „niedrig", aber gesättigte Fettsäuren oft „hoch"
- **Zutaten-Analyse:** 57 % palmölfrei; Vegan/Vegetarier-Status oft „unbekannt" (automatische Ableitung gelingt nicht immer)

---

## Folie 7 — Produktnamen normalisiert
> Grafik: `m2_top_woerter.png`

- `product_name` getrimmt, kleingeschrieben, vereinheitlicht
- **Glossar-Normalisierung** (FR/IT/ES/DE → Englisch) per Regex: z. B. `chocolat`→`chocolate`, `poulet`→`chicken`
- Top-Begriffe: **chocolate (158k), chicken (129k), cheese (101k)**
- Hinweis: bewusst Begriffs-Vereinheitlichung, keine echte Satz-Übersetzung

---

## Folie 8 — Meme-Sektion: packaging · additives · ingredients
> Grafiken: `m2_meme_top_verpackung.png`, `m2_meme_top_zusatzstoffe.png`, `m2_meme_additive_anzahl.png`

- **Verpackung:** Plastik dominiert (130k) — vor Karton/Glas. Merge brachte +12.892 Einträge.
- **Zusatzstoffe:** E330 (Citronensäure, 223k) am häufigsten; **45,6 % der Produkte haben 0 Zusatzstoffe**
- **Zutaten:** Salz, zugesetzter Zucker, Zucker ganz oben

---

## Folie 9 — Verteilung über Länder, Marken, Labels
> Grafiken: `m2_spalten_top_laender.png`, `m2_spalten_top_labels.png`

- **Länder:** Frankreich (1,26 Mio) & USA (902k) dominieren → starke West-Schlagseite
- **Labels:** „Organic" (281k) häufigstes Label, gefolgt von „No gluten"
- Beleg dafür, dass die Datenbank regional verzerrt ist

---

## Folie 10 — Fazit

- **180 → 70 Spalten** bei nur 4,7 % Datenverlust — sauberer, analysierbarer Datensatz
- Kernspalten bereinigt, normalisiert und dokumentiert
- **Wichtigste inhaltliche Erkenntnisse:**
  - Hochverarbeitete Produkte überwiegen (NOVA 4: 63,8 %)
  - Salz & Zucker sind die häufigsten Zutaten
  - Daten regional verzerrt (Frankreich/USA)
- **Grenze der Daten:** viele Spalten sind dünn befüllt — Aussagen gelten oft nur für eine Teilmenge

---

### Anhang — Grafik-Übersicht (in `Grafiken Meme/`)

| Thema | Datei |
|:---|:---|
| Reduktion Trade-off | m2_reduktion_tradeoff.png |
| Reduktion Donut 180→70 | m2_reduktion_donut.png |
| Reduktion Datenverlust | m2_reduktion_datenverlust.png |
| Befüllung 4 Spalten | m2_befuellungsgrad.png |
| NOVA-Verteilung | m2_nova_verteilung.png |
| Nährwert-Level | m2_naehrwert_level.png |
| Zutaten-Analyse | m2_zutaten_analyse.png |
| Top-Begriffe Name | m2_top_woerter.png |
| Top Länder / Kategorien / Marken / Labels / E-Nummern | m2_spalten_top_*.png |
| Meme: Verpackung / Zutaten / Zusatzstoffe / Anzahl / Befüllung | m2_meme_*.png |

Detail-Berichte: `Meilenstein2_Grafiken_Bericht.md`, `Meilenstein2_Meme_Bericht.md`
