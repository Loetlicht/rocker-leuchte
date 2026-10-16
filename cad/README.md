# CAD-Quellcode

Alle Teile der Rocker-Leuchte werden per Python erzeugt (parametrisch).

```
pip install manifold3d shapely trimesh numpy pillow
python3 build_v1.py                         # alle Gehäuseteile + Hals -> ../stl
python3 build_litho.py ../docs/megawatt.png v1_logo_megawatt   # Logo als Lithophan-Einschub
```

| Datei | Inhalt |
|---|---|
| `v1.py` | Geometrie und Parameter (Masse, Wandstärken, Spiel) |
| `build_v1.py` | Exportiert alle Gehäuseteile als STL |
| `build_litho.py` | Logo → Lithophan-Einschub |
| `../docs/megawatt.png` | Erstes Logo (Megawatt) |
