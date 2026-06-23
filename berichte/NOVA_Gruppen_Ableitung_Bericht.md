# NOVA-Gruppen für fehlende Produkte ableiten — Bericht

Notebook: `notebooks/NOVA_Gruppen_Ableitung.ipynb`. Ziel: für Produkte **ohne** `nova_group`
(NaN) eine NOVA-Gruppe **1–4** aus `categories`, `ingredients`, `additives` ableiten — als
**treuer Nachbau** der echten Open-Food-Facts-Logik (`compute_nova_group`).

---

## Was wurde gemacht?

Die offizielle Spalte `nova_group` ist nur zu **25,1 %** befüllt (1.129.053 von 4,5 Mio Produkten).
Wir leiten für einen Teil der fehlenden Produkte eine Gruppe ab und schreiben sie in **zwei neue
Spalten** — die offizielle Spalte bleibt **unangetastet**:

| Spalte | Inhalt |
|:---|:---|
| `nova_group` | offiziell, **unverändert** |
| `nova_group_derived` | von uns abgeleiteter Wert (1–4), sonst `<NA>` |
| `nova_group_source` | `off_precomputed` (offiziell) / `rule_derived` (abgeleitet) / `<NA>` |

Wer den zusammengeführten Blick braucht: `nova_group.fillna(nova_group_derived)`. Für
hochsichere Analysen einfach auf `nova_group_source == "off_precomputed"` filtern.

## Wie funktioniert die NOVA-Logik (originalgetreu)?

NOVA startet bei **Gruppe 1** und wird durch „Marker" hochgestuft. Ein Marker ist ein bestimmter
Kategorie-, Zutaten- oder Additiv-Tag, der einer Gruppe zugeordnet ist. Regel (aus `Food.pm`):

- **Gruppe 4** (hochverarbeitet) schlägt alles.
- Eine **Gruppe-2**-Markierung (z. B. „Zucker", „Salz" als *Kategorie*) bleibt **Gruppe 2** und wird
  **nicht** von einer Gruppe-3-Zutat hochgestuft (Beispiel: reiner Haushaltszucker bleibt 2).
- Sonst **Gruppe 3**, sonst **Gruppe 1**.

**Marker-Quelle (327 Marker insgesamt):**
- `Config_off.pm` → `nova_groups_tags` (Kern): 26 Kategorien, 43 Zutaten, 240 Additive **je E-Nummer**.
- Taxonomie `nova:en:` aus `categories.txt` (21) und `ingredients.txt` (18): +18 neue Marker.
- Gruppen-Verteilung der Marker: **2 → 8 · 3 → 42 · 4 → 277**.

**Abstinenz-Gates** (kein Ergebnis): kein Eintrag bei Zutaten **oder** kein Eintrag bei Kategorie →
keine Gruppe. Non-Food-Produkte werden ausgeschlossen.

## Korrekturen gegenüber dem ursprünglichen Plan (quellenbelegt)

Beim Lesen des echten OFF-Quellcodes mussten drei Annahmen korrigiert werden:

1. **`Config_off.pm` ist nicht veraltet, sondern die primäre Marker-Quelle.** `compute_nova_group`
   liest *zwei* Quellen (Config zuerst, dann Taxonomie). Additive sind dort **direkt per E-Nummer**
   verschlüsselt (`additives/en:e621 → 4`).
2. **Kein E-Nummer→Klassen-Umweg.** Die Additiv-**Klassen**-Marker in der Taxonomie sind dort
   **auskommentiert/inaktiv**. Ein Klassen-Umweg hätte das Additiv-Signal komplett verpuffen lassen
   (und fast alle Gruppe-4-Fälle fälschlich auf 3 gedrückt). Wir matchen Additive direkt per E-Nummer.
3. **Gruppe-2-Regel.** Original: `{2,3} → 2` (Gruppe 2 ist vor Hochstufung geschützt) — **nicht**
   `→ 3`. So im Notebook umgesetzt.

## Validierung — ehrlich als Obergrenze

Der Klassifikator wird auf die **bereits offiziell gelabelten** Zeilen angewandt und mit der echten
NOVA verglichen (Konfusionsmatrix, Accuracy vs. Mehrheits-Baseline „immer 4", Precision/Recall je
Gruppe, Abstinenzrate). **Diese Accuracy ist ein optimistischer Oberwert**, weil gelabelte Produkte
sauberere Eingaben haben als die Zielprodukte ohne NOVA.

**Kill-Bedingung (vor dem Lauf festgelegt):**
- (a) Gesamt-Accuracy muss die Baseline um **≥ 10 Prozentpunkte** schlagen — sonst werden **keine**
  abgeleiteten Werte ausgeliefert (nur Diagnose).
- (b) Eine Gruppe wird nur ausgeliefert, wenn ihre **Precision ≥ 80 %** ist; Gruppen darunter bleiben
  `<NA>`. (Erwartung: Gruppe 1 fällt meist durch — „kein Marker gefunden" ist oft nur Untererkennung,
  nicht echtes Gruppe 1.)

### Ergebnisse (aus dem Notebook-Lauf einzutragen)
> Diese Zahlen liefert der Lauf im Jupyter-Kernel (volle CSV); hier eintragen:
- Kandidaten (NaN + Gates): **~117k** (exakt: ____)
- Accuracy / Baseline / Delta: ____ / ____ / ____
- Precision je Gruppe (1/2/3/4): ____
- Ausgelieferte Gruppen (Precision ≥ 80 %): ____
- Abgeleitete Werte gesamt: ____ → NOVA-Abdeckung 25,1 % → **____ %**

## Bekannte Grenzen (für den Kunden)

- **Systematische Gruppe-4-Untererkennung** durch fehlende Taxonomie-**Hierarchie** und
  **Sprachabdeckung**: Wir matchen nur exakte Tags; OFF matcht zusätzlich über Kind-Tags. Marker wie
  „modifizierte Stärke", „Glukosesirup", „Glucose-Fructose-Sirup" werden nicht erkannt → eigentlich
  hochverarbeitete Produkte landen in Gruppe 3 statt 4. Konkret dokumentiert in **OFF-Issue #10415**.
- **Das „≥ 50 % unbekannte Zutaten"-Gate** wird nicht repliziert (kein Zutaten-Parser) — wir vergeben
  evtl. Gruppen, wo OFF abstinent bliebe. Die Validierung quantifiziert die Abweichung.
- **Wasser-/Gruppe-2-Ausnahme ohne Zutaten** wird nicht angewandt (wir verlangen Zutaten **und**
  Kategorie) → etwas konservativer als OFF.
- Näherung ≠ offizielle NOVA. Für belastbare Aussagen `nova_group_source == "off_precomputed"` nutzen.

## Quellen
- OFF `lib/ProductOpener/Food.pm` (`compute_nova_group`), `lib/ProductOpener/Config_off.pm`
  (`nova_groups_tags`), `taxonomies/food/{categories,ingredients}.txt` (Stand 2026-06-21).
- NOVA-Definition: Monteiro et al., „NOVA. The star shines bright", World Nutrition 2016.
