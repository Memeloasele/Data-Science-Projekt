# Open Food Facts — Meilenstein 2: Grafiken-Bericht

Bericht zu den Visualisierungen rund um **Spaltenreduktion** und **Spaltenbereinigung**
des >6%-Datensatzes (`openfoodfacts_ueber6prozent.csv.zip`).
Alle Grafiken liegen im Ordner `../Grafiken Meme/`.

---

## Auf einen Blick

| Kennzahl | Wert |
|:---|---:|
| Produkte (nach Deduplikation) | **4.501.223** |
| Spalten vorher → nachher | **180 → 70** |
| Gewählte Füllgrenze | **6 %** |
| Dadurch entfernte Spalten | **110** |
| Datenverlust bei 6 % | **nur 4,71 %** |
| Häufigste NOVA-Gruppe | **4 – hochverarbeitet (63,8 %)** |
| Befüllung `product_name` | 92,6 % |
| Befüllung Tag-/NOVA-Spalten | 25–34 % |

> **Kernbotschaft:** Mit der 6%-Füllgrenze konnten 110 weitgehend leere Spalten entfernt werden, ohne nennenswert Daten zu verlieren (4,7 %). Die vier inhaltlichen Kernspalten wurden anschließend bereinigt und normalisiert. Inhaltlich dominieren hochverarbeitete Produkte (NOVA 4).

---

# Teil A — Spaltenreduktion (180 → 70)

Quelle: `notebooks/Bereinigung_spaltenreduktion.ipynb`. Getestet wurde, wie viele Spalten
bei verschiedenen Mindest-Füllgrenzen wegfallen und wie viel Information dabei verloren geht.

## A1 · Trade-off der Füllgrenze

![Trade-off der Füllgrenze](../Grafiken%20Meme/m2_reduktion_tradeoff.png)

Balken = entfernte Spalten, rote Linie = Anteil verlorener Werte am gesamten Datensatz.

| Füllgrenze | Spalten weg | Datenverlust |
|---:|---:|---:|
| 5 % | 86 | 1,06 % |
| **6 %** | **110** | **4,71 %** |
| 7 % | 117 | 5,93 % |
| 8 % | 122 | 7,00 % |
| 9 % | 124 | 7,47 % |
| 10 % | 124 | 7,47 % |
| 20 % | 129 | 9,73 % |
| 50 % | 157 | 39,44 % |

**Interpretation:** Zwischen 6 % und 10 % entfernt man kaum zusätzliche Spalten (110 → 124), zahlt aber mit steigendem Datenverlust. 6 % ist der „Sweet Spot": maximaler Aufräumeffekt bei minimalem Verlust.

## A2 · Ergebnis der Reduktion

![Spaltenreduktion Donut](../Grafiken%20Meme/m2_reduktion_donut.png)

Von **180** Spalten bleiben **70** erhalten (39 %), **110** werden entfernt (61 %). Entfernt wurden v. a. extrem selten gefüllte Nährstoff-Detailspalten (z. B. einzelne Fettsäuren, Vitamine) und Metadaten.

## A3 · Datenverlust je Füllgrenze

![Datenverlust je Füllgrenze](../Grafiken%20Meme/m2_reduktion_datenverlust.png)

**Interpretation:** Begründet, *warum nicht strenger* gefiltert wurde. Bis 10 % bleibt der Verlust unter 7,5 %; bei 50 % gingen **39,4 %** aller Werte verloren — inakzeptabel.

---

# Teil B — Bereinigung der vier Kernspalten

Quelle: `notebooks/Meilestein2_DatenBereinigung_uber6prozent.ipynb`. Bereinigt wurden
`product_name`, `ingredients_analysis_tags`, `nova_group`, `nutrient_levels_tags`.

## B1 · Befüllungsgrad nach Bereinigung

![Befüllungsgrad](../Grafiken%20Meme/m2_befuellungsgrad.png)

| Spalte | Befüllung |
|:---|---:|
| `product_name` | 92,6 % |
| `nutrient_levels_tags` | 33,8 % |
| `ingredients_analysis_tags` | 30,1 % |
| `nova_group` | 25,1 % |

**Interpretation:** Nur der Produktname ist nahezu vollständig. Die analytisch wertvollen Tag- und Klassifikationsspalten sind nur bei einem Viertel bis Drittel der Produkte vorhanden — wichtig für die Aussagekraft späterer Auswertungen.

## B2 · NOVA-Verarbeitungsgrad

![NOVA-Verteilung](../Grafiken%20Meme/m2_nova_verteilung.png)

| NOVA-Gruppe | Anzahl | Anteil |
|:---|---:|---:|
| 1 · unverarbeitet | 134.418 | 11,9 % |
| 2 · Küchenzutaten | 65.181 | 5,8 % |
| 3 · verarbeitet | 209.048 | 18,5 % |
| **4 · hochverarbeitet** | **720.343** | **63,8 %** |

*(Anteile bezogen auf die 1.128.990 Produkte mit NOVA-Angabe.)*

**Interpretation:** Fast zwei Drittel der klassifizierten Produkte sind hochverarbeitet (NOVA 4) — der deutlichste inhaltliche Befund.

## B3 · Nährwert-Level je Nährstoff

![Nährwert-Level](../Grafiken%20Meme/m2_naehrwert_level.png)

Aus `nutrient_levels_tags` (1.520.527 Produkte mit Angabe) abgeleitet.

| Nährstoff | niedrig | mittel | hoch |
|:---|---:|---:|---:|
| Fett | 554.306 | 544.717 | 406.902 |
| ges. Fettsäuren | 653.170 | 328.527 | 464.024 |
| Zucker | 807.232 | 186.217 | 478.417 |
| Salz | 618.655 | 527.596 | 283.716 |

**Interpretation:** Zucker ist am häufigsten „niedrig" eingestuft, hat aber eine klare Gruppe mit „hohem" Gehalt (U-Verteilung). Gesättigte Fettsäuren fallen vergleichsweise oft in die Kategorie „hoch".

## B4 · Zutaten-Analyse (vegan / vegetarisch / Palmöl)

![Zutaten-Analyse](../Grafiken%20Meme/m2_zutaten_analyse.png)

Aus `ingredients_analysis_tags` (1.356.120 Produkte mit Angabe).

| Eigenschaft | ja | nein | unbekannt/evtl. |
|:---|---:|---:|---:|
| Vegan | 22,2 % | 39,6 % | 38,1 % |
| Vegetarisch | 29,0 % | 13,9 % | 57,2 % |
| Palmöl-frei | 57,1 % | 8,1 % | 34,8 % |

**Interpretation:** Über die Hälfte der Produkte mit Angabe ist palmölfrei. Beim Vegan-/Vegetarier-Status ist der Anteil „unbekannt/evtl." sehr hoch — die automatische Ableitung aus den Zutaten gelingt oft nicht eindeutig.

## B5 · Top-20 Begriffe in `product_name`

![Top-20 Begriffe](../Grafiken%20Meme/m2_top_woerter.png)

Nach Glossar-Normalisierung (FR/IT/ES/DE → Englisch).

**Interpretation:** `chocolate` (158.182), `chicken` (128.834) und `cheese` (100.947) führen. Die Grafik zeigt zugleich den Nutzen der Normalisierung: ohne sie wären `chocolate`/`chocolat` bzw. `chicken`/`poulet` getrennt gezählt worden.

---

## Methodische Hinweise

- Die Werte in **Teil A** stammen direkt aus den (deterministischen) Simulations-Ausgaben des Reduktions-Notebooks; die mehrere GB große Roh-CSV wurde dafür nicht erneut geladen.
- Die Werte in **Teil B** wurden auf dem bereinigten >6%-Datensatz (4.501.223 Zeilen) berechnet.
- Die Begriffs-Normalisierung in B5 ist eine **wörterbuchbasierte Ersetzung** (Regex), keine echte Übersetzung — sie vereinheitlicht häufige Lebensmittelbegriffe, lässt Unbekanntes aber unverändert.
