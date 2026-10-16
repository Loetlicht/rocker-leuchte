import os, sys, time, numpy as np, trimesh
from v1 import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stl")

def save(m, name, face):
    p = print_pose(m, face)
    mesh = p.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]; f = np.asarray(mesh.tri_verts)
    t = trimesh.Trimesh(v, f, process=False)
    t.export(f"{OUT}/{name}.stl")
    bb = t.bounds
    size = bb[1] - bb[0]
    print(f"{name:28s} status={m.status().name:8s} genus={m.genus():3d} vol={m.volume()/1000:7.1f}cm3 "
          f"size={size[0]:.1f}x{size[1]:.1f}x{size[2]:.1f} tris={len(f)} watertight={t.is_watertight}")
    return m

parts = {}
which = sys.argv[1:] or ["front", "shell", "lid", "base", "neck", "cover"]
if "front" in which: parts["front"] = save(frontplatte(), "v1_frontplatte", "front")
if "shell" in which: parts["shell"] = save(rueckschale(), "v1_rueckschale", "back")
if "lid" in which:   parts["lid"] = save(sockel_deckel(), "v1_sockel_deckel", "bottom")
if "base" in which:  parts["base"] = save(sockel_unterteil(), "v1_sockel_unterteil", "bottom")
if "neck" in which:  parts["neck"] = save(hals(), "v1_gitarrenhals", "back")
if "cover" in which: parts["cover"] = save(hals_abdeckung(), "v1_hals_abdeckleiste", "back")
