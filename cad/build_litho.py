"""Lithophan-Einschub aus einem Logo-Bild erzeugen.

Aufruf:  python3 build_litho.py <logo.png> <ausgabe_name>
Das Logo wird im Fenster zentriert und maximal gross eingepasst.
Transparenter Hintergrund wird als Weiss behandelt.
"""
import os, sys, numpy as np, trimesh
from PIL import Image, ImageOps
from v1 import lithophan, print_pose, FRONT_SKIN, CLR

src = sys.argv[1]
name = sys.argv[2] if len(sys.argv) > 2 else "v1_logo"

im = Image.open(src).convert("RGBA")
a = np.asarray(im)
bb = Image.fromarray(((a[..., 3] >= 40) * 255).astype(np.uint8)).getbbox() or (0, 0, im.width, im.height)
white = Image.new("RGBA", im.size, (255, 255, 255, 255))
g = Image.alpha_composite(white, im).convert("L").crop(bb)
g = ImageOps.autocontrast(g, cutoff=1)
gray = np.asarray(g, np.float32) / 255

hm, clip, logo_box = lithophan(gray, pitch=0.3)
panel = (hm ^ clip).translate([0, FRONT_SKIN + 0.2, 0])
panel = panel.simplify(0.02)
p = print_pose(panel, "front")
mesh = p.to_mesh()
v = np.asarray(mesh.vert_properties)[:, :3]; f = np.asarray(mesh.tri_verts)
t = trimesh.Trimesh(v, f, process=False)
t.export(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stl", f"{name}.stl"))
sz = t.bounds[1] - t.bounds[0]
print(f"{name}: status={panel.status().name} watertight={t.is_watertight} tris={len(f)} "
      f"size={sz[0]:.1f}x{sz[1]:.1f}x{sz[2]:.2f} logo_box={[round(x,1) for x in logo_box]}")
