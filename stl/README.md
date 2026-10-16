# STL-Dateien – Rocker-Leuchte V1

Alle Teile liegen bereits in der richtigen Drucklage und passen auf einen **Bambu Lab P2S** (256 × 256 mm). Stützen sind nicht nötig.

| Nr. | Datei | Filament | Masse (mm) | Hinweise |
|---|---|---|---|---|
| 1 | `v1_frontplatte.stl` | PETG schwarz | 186 × 246 × 8 | Front liegt auf dem Bett (glatte Sichtseite) |
| 2 | `v1_logo_megawatt.stl` | PLA/PETG **weiss** | 140 × 235 × 3 | Lithophan, **100 % Füllung**, 0,12 mm Schicht |
| 3 | `v1_rueckschale.stl` | PETG schwarz | 186 × 246 × 47 | Rückwand auf dem Bett |
| 4 | `v1_gitarrenhals.stl` | PETG **transparent** | 60 × 224 × 18 | Rückseite (LED-Kanal) auf dem Bett, 100 % Füllung |
| 5 | `v1_hals_abdeckleiste.stl` | PETG schwarz | 13 × 211 × 1,5 | deckt den LED-Kanal hinten ab |
| 6 | `v1_sockel_deckel.stl` | PETG schwarz | 164 × 86 × 30 | 15 % Gyroid reicht |
| 7 | `v1_sockel_unterteil.stl` | PETG schwarz | 164 × 86 × 25 | Platz für den ESP32 |

**Empfehlung für die schwarzen Teile:** 0,2 mm Schicht, 3 Wände, 15 % Füllung.

## Kleinteile

| Teil | Menge | Wofür |
|---|---|---|
| Linsenkopfschraube M3 × 16 (ISO 7380, schwarz) | 8 | Frontplatte → Rückschale (sichtbar als „Nieten“) |
| Schraube M3 × 12 | 4 | Gitarrenhals von innen an die Rückschale |
| Schraube M3 × 16 | 4 | Sockel-Deckel → Unterteil |
| WS2812B, 60 LED/m | ca. 40 LEDs (Schale) + 12 LEDs (Hals) | Beleuchtung |
| ESP32 (Mini oder WROOM-DevKit) | 1 | WLED |
| Widerstand 330 Ω, Kondensator 1000 µF | je 1 | Datenleitung / 5-V-Puffer |
| 3-adrige Litze | ca. 1 m | Verbindung |

Die M3-Schrauben schneiden ihr Gewinde direkt in die 2,6-mm-Löcher, Gewindeeinsätze sind nicht nötig.

## Zusammenbau

1. **LEDs Schale:** Streifen innen umlaufend an die Seitenwände der Rückschale kleben (LEDs zeigen nach innen). Kabel unten durch das Loch in der Spitze führen.
2. **LEDs Hals:** 12er-Stück mit den LEDs **nach vorne** in den Kanal legen, Kabel durch das Loch unten in die Schale führen, Abdeckleiste einkleben.
3. **Hals montieren:** von innen mit 4 × M3 × 12 durch die Rückwand anschrauben.
4. **Frontplatte** aufsetzen und mit den 8 Linsenkopfschrauben verschrauben.
5. **Logo** von oben in den Schlitz einschieben – fertig. Zum Wechseln an der Lasche herausziehen.
6. **Sockel:** ESP32 ins Unterteil, Kabel durch den Deckel, Deckel verschrauben. Das Wappen wird mit der Spitze in die Tasche gesteckt und verkeilt sich selbst.

## Eigenes Logo

Im Ordner [`../cad`](../cad) liegt der Generator:

```
python3 build_litho.py mein_logo.png v1_logo_meinband
```

Das Logo wird automatisch im Fenster zentriert und maximal gross eingepasst. Transparenter Hintergrund wird als Weiss behandelt (= hell).
