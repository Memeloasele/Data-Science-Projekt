# Notizen: Additives-Spalten

## Übersicht

Vier Spalten zum Thema Zusatzstoffe (E-Nummern):

- `additives_n`
- `additives_tags`
- `additives_en`
- `additives`

## Füllraten

| Spalte | Füllrate | Befüllte Zeilen |
|---|---|---|
| additives_n | 28 % | 1.280.985 |
| additives_tags | 15 % | 697.089 |
| additives_en | 15 % | 697.089 |
| additives | 0 % | 33 |

## Beschreibung der Spalten

**additives_n**
Anzahl der enthaltenen Zusatzstoffe als Zahl. Numerische Spalte, unabhängig von den anderen nutzbar.
Beispiel: `2`, `4`, `6`

**additives_tags**
Liste der Zusatzstoffe im Code-Format mit Sprachpräfix. Maschinenlesbar, gut für Filterung.
Beispiel: `en:e330,en:e955`

**additives_en**
Dieselbe Liste in lesbarer Form mit Klartextnamen. Für menschliche Lesbarkeit.
Beispiel: `E330 - Citric acid,E955 - Sucralose`

**additives**
Spalte fast vollständig leer (33 von 4,5 Mio. Zeilen). Kein analytischer Wert.

## Überlappungsanalyse

`additives_tags` und `additives_en` sind immer gemeinsam befüllt (697.089 Zeilen). Inhaltlich identisch, nur unterschiedliches Format.

`additives` überschneidet sich kaum mit den anderen (max. 33 Zeilen).

## Entscheidung

- `additives` entfernen (zu wenig Daten)
- `additives_tags` UND `additives_en` redundant. Behalten: `additives_tags` (kompakter, besser für Analysen)
- `additives_n` behalten (eigenständige Information: Anzahl)

Finale Spalten: `additives_n` und `additives_tags`

## Mögliche Verwendung bei Hypothesen

- Anzahl Zusatzstoffe pro Produkt → `additives_n`
- Vorkommen bestimmter E-Nummern → `additives_tags`
- Korrelation Zusatzstoffe und Nutri-Score → beide Spalten kombiniert

## Code zur Bereinigung

```python
df = df.drop(columns=['additives', 'additives_en'])
```