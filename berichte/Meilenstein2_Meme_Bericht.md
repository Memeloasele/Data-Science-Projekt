# Meilenstein 2 — Bereinigung „Meme": packaging · additives · ingredients · manufacturing

Bericht zu den Spalten der **Meme-Sektion** aus `notebooks/Meilestein2_DatenBereinigung.ipynb`.
Grafiken liegen in `../Grafiken Meme/` (Präfix `m2_meme_`).

---

## Auf einen Blick

| Spalte | Befüllung | durch Merge gewonnen | Status |
|:---|---:|---:|:---|
| `ingredients_tags` | 28,5 % (1.280.931) | +3.299 | behalten |
| `additives_n` | 28,5 % (1.280.916) | – | behalten |
| `additives_tags` | 15,5 % (697.049) | +0 | behalten |
| `packaging_en` | 8,4 % (378.941) | +12.892 | behalten |
| `manufacturing_places` | 4,9 % | +64 | **bei 6%-Grenze entfernt** |

> **Kernbotschaft:** Die vier Verpackungs-Varianten-Spalten wurden zu *einer* (`packaging_en`) zusammengeführt — das brachte mit +12.892 Einträgen den größten Merge-Gewinn der Sektion. `additives` und `ingredients` wurden ebenfalls auf je eine Tag-Spalte konsolidiert. `manufacturing_places` blieb selbst nach dem Merge zu leer (4,9 %) und fiel bei der 6%-Füllgrenze weg.

---

## Methodik der Bereinigung (die „Meme"-Sektion)

Pro Thema gab es mehrere redundante Spalten (Rohtext, Tags, englische Variante, Freitext).
Diese wurden per `fillna()`-Kaskade zusammengeführt und die überflüssigen Spalten gelöscht:

- **Packaging:** `packaging_en` ← `packaging` ← `packaging_tags` ← `packaging_text`
- **Additives:** `additives_tags` ← `additives_en` (zusätzlich `additives_n` als Zähler)
- **Ingredients:** `ingredients_tags` ← `ingredients_text`
- **Manufacturing:** `manufacturing_places_tags` ← `manufacturing_places`

---

## 1 · Befüllungsgrad der Meme-Spalten

![Befüllungsgrad Meme](../Grafiken%20Meme/m2_meme_befuellung.png)

**Interpretation:** Selbst die am besten gefüllten Spalten (ingredients/additives_n) erreichen nur ~28 %. Verpackung ist mit 8,4 % dünn, `manufacturing_places` (4,9 %, grau) wurde bei der 6%-Grenze entfernt. Aussagen aus diesen Spalten gelten also nur für eine Minderheit der Produkte.

## 2 · Top 15 Verpackungsarten (`packaging_en`)

![Top Verpackung](../Grafiken%20Meme/m2_meme_top_verpackung.png)

| Verpackung | Produkte |
|:---|---:|
| Plastic | 130.254 |
| Cardboard | 41.223 |
| Glass | 34.678 |
| Bag | 33.408 |
| Bottle | 23.848 |

**Interpretation:** **Plastik** dominiert deutlich (mehr als 3× so häufig wie Karton). Hinweis: Die Spalte ist mehrsprachig (z. B. `fr:`-Tags), daher sind seltene Werte teils sprachgemischt.

## 3 · Top 15 Zutaten (`ingredients_tags`)

![Top Zutaten](../Grafiken%20Meme/m2_meme_top_zutaten.png)

| Zutat | Produkte |
|:---|---:|
| salt | 637.401 |
| added sugar | 610.809 |
| disaccharide | 549.387 |
| sugar | 526.715 |
| oil and fat | 453.113 |

**Interpretation:** Salz und (zugesetzter) Zucker stehen ganz oben — passt zum Befund, dass hochverarbeitete Produkte (NOVA 4) überwiegen. Die Tags sind normalisiert (`en:`-Präfix entfernt).

## 4 · Top 15 Zusatzstoffe / E-Nummern (`additives_tags`)

![Top Zusatzstoffe](../Grafiken%20Meme/m2_meme_top_zusatzstoffe.png)

| E-Nummer | Bedeutung | Produkte |
|:---|:---|---:|
| E330 | Citronensäure | 222.682 |
| E322 | Lecithine | 146.676 |
| E322i | Lecithin | 119.529 |
| E500 | Natriumcarbonate | 93.748 |
| E415 | Xanthan | 77.648 |

**Interpretation:** Citronensäure (E330) ist mit Abstand der häufigste Zusatzstoff. Es dominieren funktionale Stoffe (Säuerung, Emulgatoren, Verdickung) — keine „exotischen" Zusätze an der Spitze.

## 5 · Anzahl Zusatzstoffe pro Produkt (`additives_n`)

![Zusatzstoffe pro Produkt](../Grafiken%20Meme/m2_meme_additive_anzahl.png)

- Produkte mit Angabe: **1.280.916**
- **0 Zusatzstoffe: 583.867 (45,6 %)**
- Median: **1**, Mittelwert: **1,87**, Maximum: **319**

**Interpretation:** Fast die Hälfte der Produkte (mit Angabe) enthält **keine** Zusatzstoffe; die Verteilung fällt steil ab. Einzelne Ausreißer haben sehr viele Zusätze (max. 319).

---

## Methodische Hinweise

- Berechnet auf dem bereinigten >6%-Datensatz `openfoodfacts_ueber6prozent.csv.zip` (4.501.223 Zeilen). Für die hier gezeigten Spalten sind die Verteilungen identisch zur Vollversion in `Meilestein2_DatenBereinigung.ipynb`.
- **`manufacturing_places`** ist im >6%-Datensatz nicht mehr enthalten (bei der Füllgrenze entfernt) und kann daher nicht als Inhalts-Grafik dargestellt werden — nur der Befüllungsgrad ist (aus der Reduktion) bekannt.
- Mehrfachwerte (Komma-getrennt) wurden aufgesplittet und gezählt; Sprachpräfixe (`en:`, `fr:` …) bei der Anzeige entfernt.
- Die Merge-Gewinne (z. B. packaging +12.892) stammen aus den `merge_report`-Ausgaben des Bereinigungs-Notebooks.
