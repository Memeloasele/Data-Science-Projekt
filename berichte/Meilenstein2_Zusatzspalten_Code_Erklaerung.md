# Code-Erklärung: `Meilestein2_DatenBereinigung_Zusatzspalten.ipynb`

Schritt-für-Schritt-Begleittext zum Mitlesen. Geh den Code Zelle für Zelle durch und lies hier
parallel die Erklärung der jeweiligen Zelle. Reihenfolge der Zellen = Reihenfolge in diesem Dokument.

---

## Überblick: was macht das Notebook?

Es bereinigt eine **Spaltengruppe** des Open-Food-Facts-Datensatzes (4.501.357 Produkte) und leitet
am Ende fehlende **NOVA-Gruppen** ab. Es besteht aus **13 Code-Zellen** (jeweils mit einer
Markdown-Erklärung davor) in zwei großen Blöcken:

1. **Bereinigung + Diagnostik** (Zellen 1–7): säubert `product_name`, `packaging`, `additives`,
   `ingredients`, `manufacturing_places`, `ingredients_analysis_tags`, `nova_group`,
   `nutrient_levels_tags`, `cities_tags`, `owner`, `traces`/`traces_tags`/`traces_en`; danach ein
   paar Diagnose-Zellen.
2. **NOVA-Ableitung** (Zellen 8–13, IDs `nova_*`): leitet für Produkte ohne NOVA-Gruppe eine
   Gruppe 1–4 ab (Port der echten OFF-Logik).

### Alles in EINEM `df`
Die CSV wird **einmal** geladen (Zelle `clean`); der NOVA-Teil lädt **nicht** neu, sondern arbeitet auf
demselben `df` weiter. Am Ende enthält `df` die gereinigten Zusatzspalten **und** `nova_group_derived`
+ `nova_group_source`.

Damit das funktioniert, bleiben in `clean` zwei Tag-Spalten erhalten, die der NOVA-Teil braucht:
- **`additives_tags`** (E-Nummern, z. B. `en:e621`) — wird **nicht** gelöscht. (Die Spalte `additives`
  ist die *lesbare* Form `E330 - Citric acid` und taugt **nicht** fürs E-Nummern-Matching.)
- **`categories_tags`** (roh geladen).
- Für Zutaten genügt die bereits umbenannte Tag-Spalte **`ingredients`** (= das gereinigte
  `ingredients_tags`) — sie wird direkt verwendet.

Die Zuordnung „Logik-Begriff → echte Spalte" steht im Klassifikator als `NOVA_COLS`.

---

## Wiederkehrende Bausteine (einmal verstehen, gilt überall)

- **`clean_series(s)`** — der zentrale Säuberer für Text-/Tag-Spalten. Schritte:
  1. `s.astype("string").str.strip()` → in pandas' *nullable* String-Typ wandeln, Leerzeichen am Rand weg.
  2. `.replace("", pd.NA)` → leere Strings werden zu „fehlend" (`pd.NA`).
  3. `.where(~s.str.lower().isin(INVALID), pd.NA)` → bekannte Müll-Platzhalter (`?`, `na`, `none`,
     `null`, `en:null`, …) werden zu `pd.NA`. `~` heißt „nicht", `.isin(...)` prüft Zugehörigkeit.
  4. `.str.fullmatch(r"[?,.\-/ ]+")` → Werte, die **nur** aus Satzzeichen/Leerzeichen bestehen, → `pd.NA`.
  - Wichtig: **Präfixe wie `en:`/`fr:` bleibt erhalten** (werden nicht entfernt).
- **`pd.NA` / `"string"` / `"Int64"`** — pandas' „nullable" Typen. `pd.NA` ist ein sauberes „fehlend",
  das in String- und Integer-Spalten funktioniert (anders als `NaN`, das nur in Float lebt).
- **`.str.replace(r"...", "...", regex=True)`** — Suchen/Ersetzen per regulärem Ausdruck pro Zelle.
  Häufig genutzt: `r"\s*,\s*"` → `","` (Leerzeichen um Kommas vereinheitlichen) und `r"\s+"` → `" "`
  (Mehrfach-Leerzeichen zu einem).
- **`section_header(titel)`** — druckt nur eine hübsche Überschrift (Linien aus `═`/`─`).
- **`merge_report` / `clean_report`** — drucken eine Fortschrittszeile mit Balken: Befüllungs-Prozent
  und wie viele Werte dazu kamen (`+…`) bzw. entfernt wurden (`entfernt …`). Reines Logging.
- **`normalize_tags(s)`** — Sonderfall **nur für packaging**: macht aus Taxonomie-Tags lesbaren Text
  und **entfernt** dabei die Präfixe (`en:plastic-bottle` → `Plastic Bottle`). Bewusste Ausnahme.

---

## Zelle 1 — `imports`
Lädt `pandas`, `numpy`, `matplotlib` und stellt `display.max_columns = None` (alle Spalten anzeigen).
Reines Setup, keine Daten.

## Zelle 2 — `clean` (das Herzstück der Bereinigung)
Eine große Zelle. Vier Abschnitte:

**(a) Laden + Helper.** `CSV_PATH` zeigt auf die **volle** CSV. `COLS` listet nur die benötigten
Spalten (`usecols` spart Speicher). Bewusst die volle Datei, weil `cities_tags`/`owner`/`traces*`
unter der 6%-Grenze liegen und im reduzierten Datensatz fehlen. Danach werden die o. g. Helper definiert.

**(b) TEIL A — Reproduktion bereits gereinigter Spalten** (Logik aus dem Hauptnotebook):
- `product_name`: erst mit `abbreviated_product_name`, dann `generic_name` auffüllen (`fillna`-Kette),
  dann säubern (lowercase, Leerraum normalisieren). Ergebnis ~**92,6 %** befüllt.
- `packaging`: nur strukturierte Quellen, Präfixe → lesbar (`normalize_tags`). ~8,4 %.
- `additives`: lesbare englische Spalte (`additives_en`) als Survivor, aus `additives_tags`
  aufgefüllt; Tag-Spalten verworfen. ~15,5 %.
- `ingredients`: `ingredients_tags` sauber halten **und** `ingredients_text` als eigene Spalte behalten.
- `manufacturing_places`: Tag-Spalte aus Rohtext auffüllen. ~4,9 %.

**(c) TEIL B — >6%-Spalten** (Präfixe behalten):
- `ingredients_analysis_tags` & `nutrient_levels_tags`: säubern, lowercase, Komma-Abstände normalisieren.
- `nova_group`: **`pd.to_numeric(..., errors="coerce")`** zwingt zu Zahl (Ungültiges → `NaN`), dann nur
  Werte **1–4** behalten, Typ `Int64`. Ergebnis ~**25,1 %** (1.129.053).

**(d) TEIL C (neu) — `cities_tags`, `owner`, `traces`-Trio:**
- Tag-Spalten (`cities_tags`, `traces`, `traces_tags`, `traces_en`): säubern, lowercase, Komma-Abstände
  vereinheitlichen — **Präfixe bleiben** (`en:milk,en:nuts`).
- `owner`: nur säubern + Whitespace zusammenfassen — **kein** Kleinschreiben, **kein** Komma-Split
  (es ist eine ID/Organisations-Kennung, kein Tag-Listenfeld).

**(e)** `df.rename(...)`: benennt die gemergten Survivor um (`packaging_en→packaging`,
`additives_en→additives`, `ingredients_tags→ingredients`, `manufacturing_places_tags→manufacturing_places`).
`cities_tags`/`owner`/`traces*` behalten ihre Namen. Zum Schluss „Zwischenstand": **15 Spalten**.

> Hinweis: `categories_tags` wird hier mitgeladen (für die Diagnose-Zellen weiter unten), aber in
> Teil C **nicht** gesäubert — es bleibt roh.

## Zelle 3 — `sample`
Baut eine kleine Übersichtstabelle (`dtype`, Befüllung in %, ein Beispielwert je Spalte) und zeigt
zusätzlich pro Spalte die ersten 10 echten Werte. Dient der Sichtprüfung (Präfixe erhalten? sauber?).

## Zelle 4 — `68e303f4` (Detail-Profil `traces_tags` & `traces_en`)
Funktion `spalte_info(col)` druckt je Spalte: dtype, Befüllung/fehlend, Anzahl einzigartiger Werte,
und auf **Tag-Ebene** (an Kommas gesplittet): Gesamt-/einzigartige Einzel-Tags, Tags pro Eintrag
(min/median/max/ø), Top-15-Werte, Top-15-Einzel-Tags, 15 Beispiele.
**Erkenntnis aus dem Lauf:** beide ~5,07 % befüllt, ~2,8 Tags/Eintrag; häufigste Allergene
`en:nuts`, `en:milk`, `en:soybeans`. `traces_en` ist dasselbe wie `traces_tags`, nur ohne `en:`-Präfix.

## Zelle 5 — `637ba358` (Traces-Kreuztabelle + Identität)
Untersucht das Verhältnis der drei traces-Spalten:
- **Befüllungs-Muster** (welche Kombination ist befüllt): 166.328 haben alle drei; 62.008 haben
  `traces_tags`+`traces_en` aber kein rohes `traces`.
- **Identität über alle 3**: wörtlich gleich nur 1.304 (wegen Präfix-Unterschieden), aber
  **semantisch** (Präfixe weg, sortiert) **155.791**.
- **Paarweise**: `traces_tags` == `traces_en` zu **100,0 %** → es ist dieselbe Information in zwei
  Formaten. (Begründet, warum man die drei nicht naiv mischen sollte.)
Technik hier: `df[...].notna()`, `value_counts()`, `pd.crosstab(...)`, und eine `normiere()`-Hilfsfunktion
(Präfixe entfernen, Tags sortieren), um „semantische" Gleichheit zu messen.

## Zelle 6 — `91b1b696` (Diagnose: wie viele Produkte sind überhaupt klassifizierbar?)
Zählt Produkte mit `ingredients` **und** `categories_tags` befüllt → **23,9 %**. Das ist die Obergrenze
dessen, was eine regelbasierte NOVA-Ableitung theoretisch abdecken kann.

## Zelle 7 — `ee4c7a84` (Diagnose: neue Kandidaten)
Zählt Produkte, die **kein** `nova_group` haben, **aber** Zutaten + Kategorie → **117.709** (2,6 %).
Das ist die realistische Menge, die wir im NOVA-Teil neu befüllen könnten.

---

## NOVA-Ableitung (Zellen 8–13)

## Zelle 8 — `nova_imports`
Wie Zelle 1, plus `Counter` (für Häufigkeitszählungen). Der NOVA-Block ist bewusst eigenständig.

## Zelle 9 — `nova_load` (NOVA-Vorbereitung, KEIN Neuladen)
Lädt **nicht** neu, sondern normalisiert auf dem bestehenden `df` nur die Matching-Spalten in Tag-Form:
`categories_tags` (roh) und `additives_tags` (roh behalten) → lowercase + Komma-Abstände, Präfixe
bleiben. Die Zutaten kommen aus der bereits gereinigten Spalte `ingredients`. `nova_group` ist schon
aus Teil B sauber (1–4).

## Zelle 10 — `nova_markers`
Das **Wörterbuch `NOVA_MARKER`** (327 Einträge), 1:1 aus Open Food Facts portiert
(`Config_off.pm` + Taxonomien, Stand 2026-06-21). Aufbau: Schlüssel `"tagtype/tagid"` → NOVA-Gruppe.
- **30 Kategorien**, **57 Zutaten**, **240 Additive** (Additive **direkt per E-Nummer**, z. B.
  `additives/en:e621 → 4`; **kein** Umweg über Additiv-Klassen).
- Gruppen-Verteilung der Marker: 8×Gruppe 2, 42×Gruppe 3, 277×Gruppe 4.

## Zelle 11 — `nova_classifier` (die eigentliche Logik)
Drei Funktionen:
- **`entscheide(groups)`** — Kernregel (treu zu OFF `compute_nova_group`): aus der Menge gefundener
  Marker-Gruppen ergibt sich: **4 schlägt alles** → sonst **eine Gruppe-2-Markierung bleibt 2**
  (wird *nicht* von Gruppe 3 hochgestuft — „Zucker bleibt Gruppe 2") → sonst **3** → sonst **1**.
- **`_matched(frame, col, tagtype)`** — splittet eine Tag-Spalte an Kommas (`explode`), setzt den
  Schlüssel `"tagtype/tag"` zusammen und schlägt ihn im `NOVA_MARKER`-Dict nach (`.map`, schnell);
  liefert je Treffer die Gruppe.
- **`klassifiziere(frame)`** — wendet `_matched` auf die drei Spalten an, sammelt **je Produkt** die
  Menge der Treffer-Gruppen (`groupby(level=0)` = gruppieren nach Zeilen-Index) und lässt `entscheide`
  entscheiden. Kein Treffer → Gruppe 1.
- **`gate(frame)`** — die **Abstinenz-Gates**: nur Produkte mit **Zutaten UND Kategorie** und ohne
  „non-food" werden bewertet. (Zwei OFF-Sonderfälle werden bewusst *nicht* nachgebaut — siehe Bericht.)

## Zelle 12 — `nova_validation` (Ehrlichkeitsprüfung)
Wendet den Klassifikator auf Produkte an, die **bereits** eine offizielle NOVA haben, und vergleicht:
- **Konfusionsmatrix** (`pd.crosstab`), **Accuracy** vs. **Baseline** („immer die häufigste Gruppe"),
  **Precision/Recall** je Gruppe, **Abstinenzrate**.
- **Kill-Bedingung (vorab festgelegt!):** (a) Accuracy muss die Baseline um **≥ 10 Prozentpunkte**
  schlagen, sonst wird gar nichts ausgeliefert; (b) eine Gruppe wird nur ausgeliefert, wenn ihre
  **Precision ≥ 80 %** ist. → die Variablen `kill_a` und `allowed` steuern Zelle 13.
- Wichtig: Diese Accuracy ist eine **Obergrenze** (gelabelte Produkte haben sauberere Eingaben).

## Zelle 13 — `nova_apply` (Ergebnis schreiben)
Legt zwei neue Spalten an und füllt sie:
- **`nova_group`** bleibt unangetastet (offiziell).
- **`nova_group_derived`** — von uns abgeleiteter Wert, **nur** für Kandidaten (NaN + Gates) und
  **nur** für Gruppen, die die Precision-Hürde bestanden (`allowed`).
- **`nova_group_source`** — `off_precomputed` / `rule_derived` / `<NA>`, damit man jederzeit auf
  hochsichere Werte filtern kann (`== "off_precomputed"`).
Danach Konsistenz-Checks (`assert …`), Gesamtabdeckung (offiziell → inkl. abgeleitet) und eine
Stichprobe je abgeleiteter Gruppe.

---

## Wo finde ich was?
- **Was/Warum der Bereinigung** (fachlich, für Kunden): `berichte/Meilenstein2_Bereinigung_Zusatzspalten_Bericht.md`
- **NOVA-Methodik, Korrekturen, Grenzen, Validierung**: `berichte/NOVA_Gruppen_Ableitung_Bericht.md`
- **Diese Datei**: technische Zelle-für-Zelle-Begleitung zum Code.

## Mini-Glossar
- **Tag / Taxonomie-Tag**: standardisierter Wert mit Sprachpräfix, z. B. `en:milk`. Maschinenlesbar,
  eindeutig.
- **`explode()`**: macht aus einer Liste-pro-Zelle viele Zeilen (eine je Listenelement).
- **`groupby(level=0)`**: gruppiert nach dem Zeilen-Index (= je Produkt zusammenfassen).
- **`fillna(other)`**: fehlende Werte aus einer anderen Spalte/Quelle auffüllen.
- **Befüllung/Füllrate**: Anteil nicht-fehlender Werte einer Spalte.
- **Precision/Recall**: Präzision = „wie oft ist eine vergebene Gruppe richtig"; Recall = „wie viele
  echte Fälle einer Gruppe finden wir".
