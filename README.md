<h1 align="center">🎸 Rocker-Leuchte</h1>

<p align="center">
  <b>Wappen-Leuchte mit wechselbarem Band-Logo und leuchtendem Gitarrenhals.</b><br>
  ESP32 · WS2812B · WLED · 3D-Druck – ein Projekt von <a href="https://github.com/Loetlicht">Lötlicht</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-in_Arbeit-F0A030?style=flat-square" alt="Status: in Arbeit">
  <img src="https://img.shields.io/badge/ESP32-WLED-E7352C?style=flat-square&logo=espressif&logoColor=white" alt="ESP32 + WLED">
  <img src="https://img.shields.io/badge/Drucker-Bambu_Lab_P2S-00AE42?style=flat-square" alt="Bambu Lab P2S">
  <img src="https://img.shields.io/badge/Lizenz-CC_BY--NC--SA_4.0-lightgrey?style=flat-square" alt="Lizenz: CC BY-NC-SA 4.0">
</p>

<p align="center">
  <img src="docs/v1_eingeschaltet.png" alt="Rocker-Leuchte V1 eingeschaltet" width="400">
  <img src="docs/v1_explosion.png" alt="Rocker-Leuchte V1 Explosionsansicht" width="430">
</p>

---

## Die Idee

Eine Leuchte in Wappenform für das Logo deiner Lieblingsband. Das Logo sitzt als **Lithophan** auf einer Platte, die von oben eingeschoben wird. So lässt es sich in Sekunden austauschen. Hinter der Leuchte ragt ein **Gitarrenhals** mittig nach oben heraus, der ebenfalls leuchtet.

Gesteuert wird alles von einem **ESP32 mit WLED**: Farben, Effekte und Helligkeit stellst du bequem am Handy ein.

### Zwei Varianten

| Variante | Besonderheit |
|---|---|
| **V1 Rocker** | Wappen-Gehäuse mit Nieten-Optik, Einschub-Logo, leuchtender Gitarrenhals, Sockel mit Platz für den ESP32 |
| **V2 Art-Deco** | Gestufte Spitzbogen-Form, komplette Frontplatte mit Magneten (6 × 3 mm) zum Wechseln |

---

## Teileliste (geplant)

| Teil | Menge | Hinweis |
|---|---|---|
| ESP32 (Mini oder WROOM) | 1 | WLED-Firmware |
| WS2812B LED-Streifen, 60 LED/m | ca. 1 m | umlaufend im Gehäuse + Gitarrenhals |
| Netzteil 5 V, min. 3 A | 1 | je nach LED-Anzahl |
| Kondensator 1000 µF / 10 V | 1 | über die 5-V-Versorgung des Streifens |
| Widerstand 330 Ω | 1 | in der Datenleitung |
| Neodym-Magnete 6 × 3 mm | 4 | nur V2 |
| Filament PETG/PLA (schwarz) | – | Gehäuse |
| Filament weiss | – | Lithophan-Platte |
| Filament transparent | – | Gitarrenhals |

---

## Projektstand

- [x] Konzept und Design ([Konzeptbild](docs/konzept.jpg))
- [x] STL-Dateien Gehäuse V1 Rocker
- [x] STL-Dateien Gitarrenhals
- [x] Logo-Lithophan-Platte (Megawatt als erstes Logo)
- [ ] STL-Dateien V2 Art-Deco mit Magnet-Front
- [x] Generator-Skript: eigenes Logo → Lithophan-Platte
- [ ] WLED-Konfiguration und Verdrahtung
- [ ] Bauanleitung mit Fotos

---

## Ordner

| Ordner | Inhalt |
|---|---|
| [`stl/`](stl/) | Druckdateien, Kleinteile und Zusammenbau |
| [`cad/`](cad/) | Python-Quellcode der Teile und Logo-Generator |
| [`firmware/`](firmware/) | WLED-Einrichtung und Pinbelegung |
| [`docs/`](docs/) | Bilder und Anleitungen |

---

## Hinweis zu Logos

Band-Logos sind geschützt. Lade hier nur Logos hoch, die du verwenden darfst – für deine eigene Leuchte zu Hause kannst du mit dem Generator jedes Logo selbst in eine Platte umwandeln.

---

## Lizenz

Dieses Projekt steht unter der [Creative Commons Namensnennung – Nicht kommerziell – Weitergabe unter gleichen Bedingungen 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.de) (CC BY-NC-SA 4.0). Du darfst es nachbauen, verändern und teilen, solange du Lötlicht nennst, es nicht kommerziell nutzt und Abwandlungen unter derselben Lizenz weitergibst. Den vollständigen Text findest du in [`LICENSE`](LICENSE).

Die Lizenz gilt für das eigene Design, den Code und die Anleitungen. Band-Logos wie das Megawatt-Logo in `stl/v1_logo_megawatt.stl` gehören ihren jeweiligen Rechteinhabern und sind davon ausgenommen.

<p align="center"><i>Mehr Projekte auf TikTok: <a href="https://www.tiktok.com/@loetlicht">@loetlicht</a> 🔥</i></p>
