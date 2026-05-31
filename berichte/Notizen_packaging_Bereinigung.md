# Notizen: Packaging-Spalten

## Übersicht

Vier Spalten zum Thema Verpackung:

- `packaging`
- `packaging_tags`
- `packaging_en`
- `packaging_text`

## Füllraten

| Spalte | Füllrate | Befüllte Zeilen |
|---|---|---|
| packaging | 8 % | 378.953 |
| packaging_tags | 8 % | 378.945 |
| packaging_en | 8 % | 378.934 |
| packaging_text | 1 % | 31.777 |

## Beschreibung der Spalten

**packaging**
Verpackungsangabe im Originalformat, verschiedene Sprachen möglich.
Beispiel: `Plastik,Karton`

**packaging_tags**
Normalisierte Verpackungsliste mit Sprachpräfix. Strukturiert, für Analysen geeignet.
Beispiel: `en:plastic,en:cardboard`

**packaging_en**
Dieselbe Liste auf Englisch, ohne Präfix. Für menschliche Lesbarkeit.
Beispiel: `Plastic,Cardboard`

**packaging_text**
Detailliertere Freitextbeschreibung der Verpackung. Mehrere Sprachen, oft mit Mengenangaben oder spezifischen Details.

## Überlappungsanalyse

`packaging`, `packaging_tags` und `packaging_en` sind fast immer gemeinsam befüllt (~378.900 Zeilen). Inhaltlich gleichwertig, nur Format unterscheidet sich.

`packaging_text` überschneidet sich kaum mit den anderen (18.915 Zeilen) und ist insgesamt selten befüllt.

## Entscheidung

- `packaging` und `packaging_en` redundant zu `packaging_tags`. Entfernen.
- `packaging_tags` behalten (strukturiertestes Format, beste Basis für Analysen)
- `packaging_text` behalten als Ergänzung, da andere Information (detaillierte Beschreibungen). Trotz niedriger Füllrate für Stichproben wertvoll.

Finale Spalten: `packaging_tags` und `packaging_text`

## Mögliche Verwendung bei Hypothesen

- Verpackungsmaterialien zählen und vergleichen → `packaging_tags`
- Korrelation Verpackung und Nachhaltigkeitslabel → `packaging_tags`
- Detailanalysen oder NLP auf Freitext → `packaging_text`

## Code zur Bereinigung

```python
df = df.drop(columns=['packaging', 'packaging_en'])
```

## Hinweis zur Datenqualität

Mit nur 8% Füllrate ist die Packaging-Information stark begrenzt. Bei Hypothesen rund um Verpackung muss berücksichtigt werden, dass Aussagen nur auf ~378.000 Produkten basieren.