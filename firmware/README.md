# Firmware – WLED

Die Rocker-Leuchte läuft mit [WLED](https://kno.wled.ge/) auf einem ESP32.

## Installation

1. ESP32 per USB an den PC anschliessen.
2. Im Browser (Chrome oder Edge) den [WLED Web Installer](https://install.wled.me/) öffnen.
3. Neueste Version wählen und installieren.
4. WLAN einrichten: Mit dem Netz `WLED-AP` verbinden (Passwort `wled1234`) und dein Heim-WLAN eintragen.

## Einstellungen (geplant)

| Einstellung | Wert |
|---|---|
| LED-Typ | WS2812B |
| Daten-Pin | GPIO 16 (wird beim Bau bestätigt) |
| Anzahl LEDs | folgt, sobald das Gehäuse fertig ist |
| Segmente | 1 = Wappen, 2 = Gitarrenhals |
| Stromgrenze | an das Netzteil anpassen (z. B. 2500 mA bei 3 A) |

Mit zwei Segmenten lassen sich Wappen und Gitarre getrennt einfärben – zum Beispiel Wappen warmweiss, Gitarre im Feuer-Effekt.
