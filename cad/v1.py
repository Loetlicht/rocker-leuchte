"""Rocker-Leuchte V1 – parametrische Geometrie (manifold3d + shapely).

Koordinaten im zusammengebauten Zustand (mm):
  x = Breite (rechts +), z = Höhe (oben +), y = Tiefe (Frontfläche y=0, nach hinten +).
Jedes Teil wird für den Druck in eine flache Lage gedreht (Funktion print_pose).
"""
import math
import numpy as np
import manifold3d as mf
from shapely.geometry import Polygon, Point, box as sbox
from shapely import affinity
from shapely.ops import unary_union

mf.set_circular_segments(64)

# ------------------------------------------------------------------ Parameter
FRONT_T = 8.0          # Dicke Frontplatte
FRONT_SKIN = 2.4       # Material vor der Panel-Nut
GROOVE = 3.4           # Nutbreite (Panel 3.0 + Spiel)
PANEL_T = 3.0          # max. Panel-Dicke
PANEL_MIN = 0.8        # Lithophan dünnste Stelle
CLR = 0.3              # Spiel Panel-Kontur
WALL = 2.4             # Wandstärke Rückschale
SHELL_DEPTH = 45.0     # Innentiefe Rückschale
BACK_T = 2.4           # Rückwand
Y_SHELL0 = FRONT_T
Y_BACK = FRONT_T + SHELL_DEPTH + BACK_T          # Rückseite Schale (55.4)
NECK_T = 12.0
BASE_TOP = -95.0
BASE_SPLIT = -125.0
BASE_BOT = -150.0
BASE_Y0, BASE_Y1 = -12.0, 74.0
BASE_X = 82.0


# ------------------------------------------------------------------ 2D-Konturen (x, z)
def wappen():
    r = [(0, 122), (18, 112), (40, 104), (70, 100), (92, 118), (88, 88), (93, 62),
         (85, 40), (87, 0), (84, -40), (70, -78), (40, -104), (0, -125)]
    pts = r + [(-x, y) for x, y in reversed(r[1:-1])]
    p = Polygon(pts)
    return p.buffer(-3).buffer(3).buffer(1.5).buffer(-1.5)


def panel_shape():
    return Polygon([(-70, 98), (70, 98), (70, -30), (62, -70), (34, -92), (0, -104),
                    (-34, -92), (-62, -70), (-70, -30)])


W2 = wappen()
P2 = panel_shape()
WIN2 = W2.buffer(-11).intersection(P2.buffer(-4)).intersection(sbox(-99, -91, 99, 200))
WIN2 = WIN2.buffer(-1).buffer(1)          # Ecken leicht runden
GROOVE2 = P2.buffer(CLR, join_style=2)
TAB2 = sbox(-18, 97, 18, 128).buffer(3).intersection(sbox(-30, 97, 30, 140))


def screw_points(n=8):
    """Schraubpunkte im Rand zwischen Panel-Nut und Aussenkontur."""
    ring = W2.buffer(-7.5).exterior
    cand = []
    L = ring.length
    for t in np.linspace(0, L, 900, endpoint=False):
        p = ring.interpolate(t)
        if p.distance(GROOVE2.exterior) >= 4.2 and not GROOVE2.contains(p) and p.y < 95:
            cand.append((t, p))
    # gleichmässig verteilen
    pts = []
    target = np.linspace(0, L, n, endpoint=False) + L / (2 * n)
    for tt in target:
        best = min(cand, key=lambda c: min(abs(c[0] - tt), L - abs(c[0] - tt)))
        pts.append((round(best[1].x, 2), round(best[1].y, 2)))
    # symmetrisch machen
    pts = sorted(set(pts))
    return pts


def sym_screws():
    """Feste, symmetrische Schraubpunkte (geprüft gegen Nut und Kontur)."""
    base = [(80.5, 60.0), (78.0, 10.0), (72.0, -52.0), (50.0, -86.0)]
    pts = []
    for x, z in base:
        pts += [(x, z), (-x, z)]
    return pts


SCREWS = sym_screws()


# ------------------------------------------------------------------ 3D-Helfer
def cs_from_shapely(geom):
    contours = []
    geoms = getattr(geom, "geoms", [geom])
    for g in geoms:
        ext = list(g.exterior.coords)[:-1]
        if Polygon(ext).exterior.is_ccw is False:
            ext = ext[::-1]
        contours.append(ext)
        for h in g.interiors:
            hh = list(h.coords)[:-1]
            if Polygon(hh).exterior.is_ccw:
                hh = hh[::-1]
            contours.append(hh)
    return mf.CrossSection(contours, mf.FillRule.EvenOdd)


def ext_y(geom, y0, y1):
    """2D-Kontur (x,z) zwischen Tiefe y0..y1 extrudieren."""
    m = mf.Manifold.extrude(cs_from_shapely(geom), y1 - y0)
    # extrudiert entlang +Z(lokal) -> drehen: (x, v, w) -> (x, w, v)
    m = m.rotate([90, 0, 0])            # (x, v, w) -> (x, -w, v)
    return m.translate([0, y1, 0])      # w in [0,d] -> y in [y1-d, y1]


def ext_z(geom2_xy, z0, z1):
    """2D-Kontur (x,y) zwischen Höhe z0..z1 extrudieren."""
    return mf.Manifold.extrude(cs_from_shapely(geom2_xy), z1 - z0).translate([0, 0, z0])


def cube(x0, x1, y0, y1, z0, z1):
    return mf.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def cyl_y(x, z, r, y0, y1, seg=48):
    return mf.Manifold.cylinder(y1 - y0, r, r, seg).rotate([-90, 0, 0]).translate([x, y0, z])


def cyl_z(x, y, r, z0, z1, seg=48):
    return mf.Manifold.cylinder(z1 - z0, r, r, seg).translate([x, y, z0])


# ------------------------------------------------------------------ Teile
def frontplatte():
    m = ext_y(W2, 0, FRONT_T)
    # Zierlinie (graviert) 4 mm innen
    line = W2.buffer(-4).difference(W2.buffer(-5.2))
    m -= ext_y(line, -0.1, 0.8)
    # Fenster
    m -= ext_y(WIN2, -1, FRONT_T + 1)
    # Panel-Nut inkl. Ausgang nach oben
    slot = unary_union([GROOVE2, sbox(-70 - CLR, 90, 70 + CLR, 200)])
    m -= ext_y(slot, FRONT_SKIN, FRONT_SKIN + GROOVE)
    # Zugriff-Ausschnitt oben (Lasche greifen)
    grip = sbox(-22, 101, 22, 200).buffer(4)
    m -= ext_y(grip, FRONT_SKIN, FRONT_T + 1)
    # Schraublöcher (Nieten-Optik: Linsenkopfschrauben M3)
    for x, z in SCREWS:
        m -= cyl_y(x, z, 1.7, -1, FRONT_T + 1)
    return m


def rueckschale():
    y0, y1 = Y_SHELL0, Y_BACK
    outer = ext_y(W2, y0, y1)
    inner = ext_y(W2.buffer(-WALL), y0 - 1, y1 - BACK_T)
    m = outer - inner
    # Schraubdome
    for x, z in SCREWS:
        dome = cyl_y(x, z, 4.6, y0, y1 - BACK_T + 0.01)
        m += dome ^ (ext_y(W2.buffer(-0.5), y0, y1))
        m -= cyl_y(x, z, 1.3, y0 - 1, y0 + 14)     # Ø2.6 für M3-Schneidschraube
    # Halsbefestigung (4 Löcher Ø3.4 durch die Rückwand) + Kabeldurchführung
    for x, z in ((-14, 55), (14, 55), (-14, 100), (14, 100)):
        m -= cyl_y(x, z, 1.7, y1 - BACK_T - 1, y1 + 1)
    m -= cyl_y(0, 45, 4.0, y1 - BACK_T - 1, y1 + 1)
    # Kabelloch unten in der Spitze (senkrecht)
    yc = (y0 + y1) / 2
    m -= cyl_z(0, yc, 3.0, -140, -100)
    return m


def sockel_deckel():
    z0, z1 = BASE_SPLIT, BASE_TOP
    foot = sbox(-BASE_X, BASE_Y0, BASE_X, BASE_Y1)
    m = ext_z(foot, z0, z1)
    # Fasen vorne/seitlich oben (45°)
    cham = 8
    cut = mf.Manifold.cube([2 * BASE_X + 20, cham * 1.5, cham * 1.5]).rotate([45, 0, 0])
    m -= cut.translate([-BASE_X - 10, BASE_Y0, z1 - cham * 1.06])
    # Tasche für die Wappenspitze (verjüngt -> Spitze verkeilt sich)
    tip = W2.intersection(sbox(-200, -200, 200, BASE_TOP + 0.01)).buffer(CLR)
    pocket = ext_y(tip, -CLR, Y_BACK + CLR)
    m -= pocket ^ (cube(-200, 200, -200, 200, z0 - 1, z1 + 1))
    # Kabeldurchführung von der Spitze in den Sockel
    m -= cyl_z(0, (Y_SHELL0 + Y_BACK) / 2, 4.0, z0 - 1, z0 + 12)
    # Schraublöcher Deckel (Ø3.4 + Senkung für Kopf)
    for x, y in BASE_SCREWS:
        m -= cyl_z(x, y, 1.7, z0 - 1, z1 + 1)
        m -= cyl_z(x, y, 3.2, z1 - 3.5, z1 + 1)
    return m


BASE_SCREWS = [(-BASE_X + 7, BASE_Y0 + 7), (BASE_X - 7, BASE_Y0 + 7),
               (-BASE_X + 7, BASE_Y1 - 7), (BASE_X - 7, BASE_Y1 - 7)]


def sockel_unterteil():
    z0, z1 = BASE_BOT, BASE_SPLIT
    m = cube(-BASE_X, BASE_X, BASE_Y0, BASE_Y1, z0, z1)
    w = 3.0
    m -= cube(-BASE_X + w, BASE_X - w, BASE_Y0 + w, BASE_Y1 - w, z0 + w, z1 + 1)
    for x, y in BASE_SCREWS:
        m += cyl_z(x, y, 5.0, z0, z1)
        m -= cyl_z(x, y, 1.3, z1 - 14, z1 + 1)      # M3-Schneidschraube
    # USB-Ausschnitt hinten
    m -= cube(-8, 8, BASE_Y1 - w - 1, BASE_Y1 + 1, z0 + w + 5, z0 + w + 13)
    # Amp-Grill vorne (Rillen)
    for i in range(4):
        zz = z0 + 5 + i * 4.5
        m -= cube(-BASE_X + 14, BASE_X - 14, BASE_Y0 - 1, BASE_Y0 + 1.0, zz, zz + 2)
    return m


# ------------------------------------------------------------------ Gitarrenhals
NECK_Y0 = Y_BACK
NECK_Y1 = Y_BACK + NECK_T
NUT_Z = 175.0


def kopfplatte2():
    hs = Polygon([(10, 176), (13, 194), (11, 232), (24, 262), (5, 264), (-17, 252),
                  (-22, 238), (-20, 188), (-10, 176)])
    return hs.buffer(2.5).buffer(-2.5)


TUNERS = [(-12.0, z) for z in np.linspace(188, 246, 6)]


def hals():
    y0, y1 = NECK_Y0, NECK_Y1
    neck = sbox(-10, 40, 10, 178)
    tab = sbox(-20, 40, 20, 110).buffer(3).intersection(sbox(-30, 40, 30, 115))
    outline = unary_union([neck, tab, kopfplatte2()])
    m = ext_y(outline, y0, y1)
    # LED-Kanal hinten (11 breit, 4 tief) + Kabelloch nach vorne
    chan = sbox(-5.6, 42, 5.6, 252)
    chan = chan.intersection(kopfplatte2().buffer(-3).union(sbox(-5.6, 40, 5.6, 200)))
    m -= ext_y(chan, y1 - 5.0, y1 + 1)
    m -= cyl_y(0, 45, 4.0, y0 - 1, y1 + 1)
    # Falz für Abdeckleiste (0.8 breiter, 1.6 tief)
    m -= ext_y(chan.buffer(0.8, join_style=2), y1 - 1.6, y1 + 1)
    # Befestigungslöcher (M3 Schneidschraube von innen durch die Rückwand)
    for x, z in ((-14, 55), (14, 55), (-14, 100), (14, 100)):
        m -= cyl_y(x, z, 1.3, y0 - 1, y0 + 9)
    # Front-Details: Bünde (graviert), Punkte, Sattel (erhaben)
    for z in np.arange(121, NUT_Z, 9):
        m -= cube(-10.5, 10.5, y0 - 1, y0 + 0.8, z, z + 1.0)
    for z in (139 + 4.5, 157 + 4.5):
        m -= cyl_y(0, z, 1.6, y0 - 1, y0 + 0.8)
    m += cube(-10.5, 10.5, y0 - 1.5, y0 + 0.01, NUT_Z, NUT_Z + 3)
    # Wirbel: Achsen vorne + Flügel seitlich (liegen auf dem Druckbett auf)
    for x, z in TUNERS:
        m += cyl_y(x, z, 3.0, y0 - 4, y0 + 0.01)
        m += cyl_y(x, z, 1.4, y0 - 5.5, y0 - 3.99)
        edge_x = kopfplatte2().intersection(sbox(-60, z - 0.5, 0, z + 0.5)).bounds[0]
        m += cube(edge_x - 7, edge_x + 1, y0 + 4, y1, z - 1.6, z + 1.6)          # Welle
        key = Polygon([(edge_x - 7, z - 4.5), (edge_x - 13, z - 3.5), (edge_x - 13, z + 3.5),
                       (edge_x - 7, z + 4.5)]).buffer(1.2)
        m += ext_y(key, y0 + 2, y1)
    return m


def hals_abdeckung():
    chan = sbox(-5.6, 42, 5.6, 252)
    chan = chan.intersection(kopfplatte2().buffer(-3).union(sbox(-5.6, 40, 5.6, 200)))
    strip = chan.buffer(0.8 - 0.15, join_style=2)
    return ext_y(strip, NECK_Y1 - 1.5, NECK_Y1)


# ------------------------------------------------------------------ Lithophan
def lithophan(gray, pitch=0.3, margin_scale=-7.0):
    """gray: 2D-Array 0..1 (1 = weiss). Liefert das Einschub-Panel."""
    from PIL import Image
    panel = P2.union(TAB2)
    bx0, bz0, bx1, bz1 = panel.bounds
    nx = int(math.ceil((bx1 - bx0) / pitch)) + 1
    nz = int(math.ceil((bz1 - bz0) / pitch)) + 1
    xs = bx0 + np.arange(nx) * pitch
    zs = bz0 + np.arange(nz) * pitch
    T = np.full((nz, nx), PANEL_T, np.float32)

    # Logo-Fläche: zentriert im Fenster, maximal gross
    wx0, wz0, wx1, wz1 = WIN2.bounds
    cx, cz = (wx0 + wx1) / 2, (wz0 + wz1) / 2
    h_img, w_img = gray.shape
    asp = w_img / h_img
    lo, hi = 10, 400
    for _ in range(40):
        hh = (lo + hi) / 2
        r = sbox(cx - hh * asp / 2, cz - hh / 2, cx + hh * asp / 2, cz + hh / 2)
        if r.within(WIN2.buffer(-margin_scale)):
            lo = hh
        else:
            hi = hh
    hh = lo
    ww = hh * asp
    LX0, LZ1 = cx - ww / 2, cz + hh / 2

    # Fenster-Maske im Raster
    from shapely import vectorized
    X, Z = np.meshgrid(xs, zs)
    inwin = vectorized.contains(WIN2.buffer(1.0), X, Z)
    # Bildwerte abtasten (bilinear)
    img = Image.fromarray((gray * 255).astype(np.uint8))
    px_w = max(2, int(round(ww / pitch)))
    px_h = max(2, int(round(hh / pitch)))
    imgr = np.asarray(img.resize((px_w, px_h), Image.LANCZOS), np.float32) / 255
    G = np.ones_like(T)
    ix0 = int(round((LX0 - bx0) / pitch))
    iz1 = int(round((LZ1 - bz0) / pitch))
    for j in range(px_h):
        zi = iz1 - j
        if 0 <= zi < nz:
            a, b = max(0, ix0), min(nx, ix0 + px_w)
            if b > a:
                G[zi, a:b] = imgr[j, a - ix0:b - ix0]
    t_win = PANEL_MIN + (1 - G) * (PANEL_T - PANEL_MIN)
    T = np.where(inwin, t_win, T).astype(np.float32)
    hm = heightmap_solid(T, bx0, bz0, pitch)
    clip = ext_y(panel, -1, 10).translate([0, 0, 0])
    return hm, clip, (LX0, cz - hh / 2, LX0 + ww, LZ1)


def heightmap_solid(T, x0, z0, pitch):
    """Geschlossener Körper: y von 0 (flache Front) bis T(x,z)."""
    nz, nx = T.shape
    n = nx * nz
    xs = x0 + np.arange(nx) * pitch
    zs = z0 + np.arange(nz) * pitch
    X, Z = np.meshgrid(xs, zs)
    top = np.stack([X.ravel(), T.ravel(), Z.ravel()], 1)
    bot = np.stack([X.ravel(), np.zeros(n), Z.ravel()], 1)
    V = np.vstack([top, bot]).astype(np.float32)
    idx = np.arange(n).reshape(nz, nx)
    a = idx[:-1, :-1].ravel(); b = idx[:-1, 1:].ravel()
    c = idx[1:, :-1].ravel(); d = idx[1:, 1:].ravel()
    # Rückseite (y=T) Normale +y ; Front (y=0) Normale -y
    t_top = np.concatenate([np.stack([a, c, b], 1), np.stack([b, c, d], 1)])
    t_bot = np.concatenate([np.stack([a, b, c], 1), np.stack([b, d, c], 1)]) + n
    # Ränder
    side = []
    def edge(seq, flip):
        for i in range(len(seq) - 1):
            p, q = seq[i], seq[i + 1]
            tri1 = [p, q, q + n]; tri2 = [p, q + n, p + n]
            if flip:
                tri1 = tri1[::-1]; tri2 = tri2[::-1]
            side.append(tri1); side.append(tri2)
    edge(idx[0, :], False)          # unten (z min)
    edge(idx[-1, :], True)          # oben
    edge(idx[:, 0], True)           # links
    edge(idx[:, -1], False)         # rechts
    F = np.vstack([t_top, t_bot, np.array(side)]).astype(np.uint32)
    mesh = mf.Mesh(vert_properties=V, tri_verts=F)
    m = mf.Manifold(mesh)
    if m.status() != mf.Error.NoError:
        # Orientierung der Seitenwände ggf. umdrehen
        side2 = [s[::-1] for s in side]
        F = np.vstack([t_top, t_bot, np.array(side2)]).astype(np.uint32)
        m = mf.Manifold(mf.Mesh(vert_properties=V, tri_verts=F))
    return m


# ------------------------------------------------------------------ Drucklage
def print_pose(m, face):
    """Dreht ein Teil so, dass die angegebene Fläche auf dem Bett liegt und zentriert."""
    if face == "front":       # Fläche y=min nach unten
        m = m.rotate([90, 0, 0])     # z' = y
    elif face == "back":      # Fläche y=max nach unten
        m = m.rotate([-90, 0, 0])    # z' = -y
    elif face == "bottom":
        pass
    (x0, y0, z0), (x1, y1, z1) = [np.array(v) for v in (m.bounding_box()[:3], m.bounding_box()[3:])]
    return m.translate([-(x0 + x1) / 2, -(y0 + y1) / 2, -z0])
