# Meilenstein 2 — Überarbeitung der „Meme"-Bereinigung (packaging · additives · ingredients · manufacturing)

Dokumentiert **was** an der Meme-Sektion in `notebooks/Meilestein2_DatenBereinigung.ipynb`
geändert wurde und **warum**. Stand: 2026-06-13.

---

## Kurzfassung

Die ursprüngliche Bereinigung sah ordentlich aus, war es aber nicht: drei der vier Merges
brachten nahezu nichts, und der einzige mit spürbarem Effekt (`packaging_en`) **beschädigte**
ausgerechnet die einzige Spalte, die später analytisch genutzt wird. Die Logik wurde auf
**Reinheit statt Befüllungsquote** umgestellt.

| Merge (vorher) | Zeilen-Gewinn | Befüllung | Problem |
|:---|---:|---:|:---|
| `additives_tags ← additives_en` | **+0** | 15,5 % | No-op. `additives_en` liefert nichts, was `additives_tags` nicht schon hat. |
| `manufacturing_places_tags ← manufacturing_places` | +64 | 4,9 % | Wird stromabwärts bei der 6%-Grenze ohnehin gelöscht — Arbeit für die Tonne. |
| `ingredients_tags ← ingredients_text` | +3.299 | 28,5 % | +0,07 Prozentpunkte — und zerstört dabei die einzige NLP-taugliche Spalte. |
| `packaging_en ← packaging ← packaging_tags ← packaging_text` | +12.892 | 8,4 % | +0,3 PP **und korrumpiert die einzige tatsächlich genutzte Spalte.** |

---

## Was vorher falsch war

1. **Format-Vermischung (der gravierendste Punkt).**
   In Open Food Facts sind das verschiedene Wertewelten:
   - `packaging_en` → sauberes Englisch (`"Plastic"`)
   - `packaging_tags` → normalisierte Taxonomie (`en:plastic`)
   - `packaging_text` → roher, mehrsprachiger Freitext (`"boîte en carton"`)

   Werden sie per `fillna` in eine Spalte gefüllt, bekommt **ein** Konzept mehrere
   Schreibweisen. `packaging_en` ist die **einzige** der vier Spalten, die downstream
   wirklich verwendet wird (Cramérs V in `Assoziationsanalyse.ipynb`) — `value_counts`
   und Assoziationsmaße auf einer so vermischten Spalte sind unzuverlässig.
   *Der bisherige `Meilenstein2_Meme_Bericht.md` gibt das selbst zu:* „Die Spalte ist
   mehrsprachig (z. B. `fr:`-Tags), daher sind seltene Werte teils sprachgemischt." Genau
   dieses Symptom wird hier behoben. Dasselbe galt für `ingredients` (Taxonomie vs. Prosa).

2. **Inkonsistenz mit dem eigenen Vorgehen.**
   Die Sektionen Ozan/Bogomil/Deniz rufen vor jedem Merge `clean_series()` auf, um
   Platzhalter-Müll (`?`, `n-a`, `en:null`, …) zu entfernen. Die Meme-Sektion tat das nicht
   — Müllwerte wurden ungefiltert in die behaltene Spalte gefüllt.

3. **Reihenfolge widersprach dem Kommentar.**
   Der Kommentar sagte „prefer structured English values", die Kaskade bevorzugte aber das
   rohe Legacy-Feld `packaging` **vor** den normalisierten `packaging_tags`.

---

## Getroffene Entscheidungen (mit dem Nutzer abgestimmt)

- **packaging & ingredients_tags → Reinheit statt Abdeckung.** Nur formatgleiche,
  strukturierte Quellen mergen; vorher `clean_series`; `en:`-Präfixe normalisieren.
- **ingredients_text → erhalten.** Die einzige NLP-taugliche Quelle wird **nicht** mehr in
  die spärlichen Tags gefaltet und gelöscht, sondern als eigene Spalte behalten.
- **additives → Survivor gedreht auf `additives_en`** (lesbar, `E330 - Citric acid`),
  Backfill aus `additives_tags`, danach Tags verwerfen.
- **manufacturing_places → unverändert** belassen (bewusste Entscheidung; Hinweis: fällt
  downstream bei der 6%-Grenze ohnehin weg).

---

## Was konkret geändert wurde

Neuer Helfer `normalize_tags()` (Taxonomie-Tags → lesbare Form, baut auf `clean_series` auf):

| Spalte | vorher | nachher | überlebende Spalte / Format |
|:---|:---|:---|:---|
| **packaging** | `en ← packaging ← tags ← text` (alle Formate gemischt) | `en ← normalize_tags(tags)`, vorher `clean_series`; Roh + Freitext verworfen | `packaging_en` → umbenannt `packaging`, format-rein |
| **additives** | Survivor `additives_tags`, gefüllt aus `_en` (+0) | Survivor `additives_en`, gefüllt aus `tags`; `clean_series` | `additives_en` → umbenannt `additives`, lesbar |
| **ingredients** | `tags ← text`, danach `text` gelöscht | `tags` nur `clean_series` (kein Freitext-Merge); `text` bleibt | `ingredients_tags` → `ingredients` **und** `ingredients_text` (erhalten) |
| **manufacturing** | `tags ← manufacturing_places` | unverändert | `manufacturing_places_tags` |

Zusätzlich angepasst: der **Rename-Block** am Zellenende — `additives_en → additives`
(statt vorher `additives_tags → additives`), damit das Umbenennen nicht ins Leere greift.

---

## Auswirkungen / bekannte Trade-offs

- **`packaging`-Befüllung sinkt unter 8,4 %** (Freitext-Zeilen werden nicht mehr mitgezählt).
  Das ist der gewollte Tausch: die verbleibenden Werte sind formatkonsistent und für
  `value_counts` / Cramérs V valide. **→ Zahl im `Meilenstein2_Meme_Bericht.md` und ggf. die
  Grafik `m2_meme_befuellung.png` / `m2_meme_top_verpackung.png` müssen neu erzeugt werden.**
- **`additives` mischt bei Backfill-Zeilen weiterhin Formate** (`E330 - Citric acid` vs.
  `en:e330`). Akzeptabel, weil der Additive-Report E-Nummern per Regex extrahiert (funktioniert
  auf beiden Formen) statt roher `value_counts`. Wechselt der Report je auf rohe Counts, muss
  auch hier `normalize_tags` auf die Tag-Quelle angewandt werden.
- **Eine Spalte mehr als vorher** (`ingredients_text` bleibt erhalten).

---

## Verifikation

1. `notebooks/Meilestein2_DatenBereinigung.ipynb` Zelle 0 + Zelle 1 von oben nach unten laufen
   lassen — kein `KeyError` (insb. im Rename-Block).
2. `merge_report`-Ausgabe prüfen: `packaging_en` niedriger-aber-sauber; `additives_en` ≈ 15,5 %.
3. `df.filter(like="packaging").columns` → nur `packaging` übrig;
   `df.filter(like="additives").columns` → nur `additives` übrig;
   `"ingredients" in df.columns` **und** `"ingredients_text" in df.columns` → beide vorhanden.
4. `df["packaging"].value_counts().head(10)` → keine `en:`-Präfixe, keine Freitext-Sätze
   (Werte wie `"Plastic"`, `"Glass"`, nicht `"boîte en carton"`).
