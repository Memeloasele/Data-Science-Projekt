# Notizen: Ingredients-Spalten

## Übersicht

Drei Spalten zum Thema Inhaltsstoffe, die unterschiedliche Information liefern:

- `ingredients_text`
- `ingredients_tags`
- `ingredients_analysis_tags`

## Beschreibung der Spalten

**ingredients_text**
Originaltext der Zutatenliste, wie sie auf der Verpackung steht. Verschiedene Sprachen (Deutsch, Französisch, Englisch, Polnisch, Spanisch). Freitextformat, unstrukturiert.
Beispiel: "Weizenmehl, Rapsöl, Speisesalz, 1,7% Meersalz..."

**ingredients_tags**
Normalisierte Zutatenliste mit Sprachpräfix (z.B. `en:`, `fr:`, `es:`). Strukturiertes Format, kommasepariert. Eignet sich für Häufigkeitsanalysen und Filterung.
Beispiel: `en:weizenmehl,en:rapsol,en:speisesalz`

**ingredients_analysis_tags**
Abgeleitete Eigenschaften der Zutatenliste. Enthält Aussagen zu Palmöl, Vegan- und Vegetarier-Status.
Beispiel: `en:palm-oil-free,en:non-vegan,en:vegetarian`

## Entscheidung

Keine Zusammenführung. Die drei Spalten sind nicht redundant, sondern haben jeweils einen anderen Zweck:

- Text = Rohdaten für Menschen lesbar
- Tags = strukturierte Daten für Analysen
- Analysis = bereits vorverarbeitete Erkenntnisse

## Datenqualität

[Hier eigene Füllraten eintragen, z.B.:]
- ingredients_text: 28 %
- ingredients_tags: 28 %
- ingredients_analysis_tags: 30 %

## Mögliche Verwendung bei Hypothesen

- Vegan-/Vegetarier-Analysen → `ingredients_analysis_tags`
- Zutaten-Häufigkeiten oder Allergen-Suche → `ingredients_tags`
- Originaltext für Stichproben oder NLP → `ingredients_text`

## Bereinigung

Zeilen ohne jegliche Zutateninfo wurden geprüft. Bei Bedarf können diese aussortiert werden mit:

`df[df[cols].notna().any(axis=1)]`