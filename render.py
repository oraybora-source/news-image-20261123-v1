#!/usr/bin/env python3
"""Render the front page for Monday 23 November 2026 (news-image-20261123 V1).

Fresh code written in this session. Flat geometric illustration, no human
figures, no third-party assets. Deterministic: same bytes every run.
Reads nothing at runtime except the fonts below (build time only).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16  # margin
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

# ---------- palette ----------
PAPER = (246, 241, 229)
INK = (25, 25, 25)
NAVY = (22, 48, 79)
NAVY_D = (16, 36, 60)
BRICK = (142, 42, 32)
CREAM_LINE = (217, 201, 163)
WHITE = (255, 255, 255)
GREY = (90, 90, 86)
LIGHT_GREY = (120, 118, 110)
SKY = (216, 226, 232)
SEA = (30, 58, 95)
SAND = (222, 205, 170)
SAGE = (138, 154, 123)

REGION = {  # dark chips, white text on them reads >= 4.5:1
    "AF": (138, 90, 18), "ME": (142, 42, 32), "AM": (23, 89, 79),
    "AS": (90, 46, 92), "EU": (22, 48, 79), "OC": (71, 99, 44),
    "WORLD": (62, 76, 89),
}
STATUS_C = {"CONFIRMED": (46, 125, 50), "REPORTED": (146, 93, 14), "CLAIM": (169, 50, 38)}

# ---------- stories: (n, region, field, place, title, deck, status, bignum, archetype, lon, lat, dx, dy)
LEADS = [
    (1, "AF", "CONFLICT", "BENGHAZI, LIBYA",
     "Ukraine claims it sank a Russian warship off Libya",
     "Seven naval drones hit the corvette Merkury and the cargo ship Angara, Kyiv says.",
     "CLAIM", "7", "sea"),
    (2, "ME", "CONFLICT", "STRAIT OF HORMUZ",
     "Iran vows to fight the US blockade",
     "Tehran says it shot down a US drone; blasts reported in the Strait of Hormuz.",
     "CLAIM", "1", "strait"),
    (3, "AM", "BUSINESS", "SILICON VALLEY, USA",
     "Nvidia brings back Jensen Huang",
     "Shares jump 33% and Wall Street rallies as the CEO returns 11 days after resigning.",
     "CONFIRMED", "+33%", "chip"),
]
MIDS = [
    (4, "OC", "CLIMATE", "ANTALYA, TURKEY",
     "COP31 fallout: Australia blames, Pacific despairs",
     "REPORTED", "0", "climate"),
    (5, "EU", "CONFLICT", "KYIV, UKRAINE",
     "153 drones in one night; Dymer toll 11",
     "CONFIRMED", "153", "drones"),
    (6, "EU", "CONFLICT", "WARSAW, POLAND",
     "NATO to send AWACS jets to Poland",
     "CONFIRMED", "3", "awacs"),
    (7, "EU", "POLITICS", "BRUSSELS, BELGIUM",
     "EU proposes 22nd Russia sanctions",
     "CONFIRMED", "22ND", "sanctions"),
    (8, "AM", "POLITICS", "WASHINGTON, USA",
     "Democrats take 258 seats, most since 1992",
     "CONFIRMED", "258", "capitol"),
    (10, "AS", "POLITICS", "JAKARTA, INDONESIA",
     "Prabowo names Amran & Sugiono as VP picks",
     "CONFIRMED", "2", "podium"),
    (11, "AS", "DISASTER", "CIKANDE, INDONESIA",
     "Factory fire: 24 dead, 30 missing",
     "CONFIRMED", "24", "factory"),
    (12, "AM", "JUSTICE", "SINALOA, MEXICO",
     "\u2018El Chapo Isidro\u2019 captured in Sinaloa",
     "CONFIRMED", "11", "capture"),
]
# briefs: (n, region, title, status, lon, lat, dx, dy)
BRIEFS = [
    (9, "AS", "Trump calls Putin \u2018my friend\u2019", "REPORTED", 114.1, 22.5, 0, 0),
    (13, "AS", "India gives Nepal $1.62bn aid", "CONFIRMED", 77.2, 28.6, -10, 12),
    (14, "AS", "Asia Power Index: India ranks 3rd", "CONFIRMED", 151.2, -33.9, 0, 0),
    (15, "OC", "NZ\u2013India Test drawn at Wellington", "CONFIRMED", 174.8, -41.3, 2, -8),
    (16, "AF", "Mali beats Belgium 2\u20131, U17 World Cup", "CONFIRMED", 51.5, 25.3, -20, 2),
    (17, "AS", "Sri Lanka A tops Group A", "CONFIRMED", 79.9, 6.9, -12, 4),
    (18, "WORLD", "BepiColombo safe in Mercury orbit", "CONFIRMED", 8.6, 49.9, -6, -16),
    (19, "AS", "Ancient star reveals early universe", "CONFIRMED", 77.6, 13.0, 14, 2),
    (20, "AM", "Ariane 6 Leo launch halted", "CONFIRMED", -52.8, 5.2, 0, 0),
    (21, "EU", "Germany to use Kyiv\u2019s Delta tool", "CONFIRMED", 13.4, 52.5, 4, -14),
    (22, "AS", "Seoul names new FM, spy chief", "CONFIRMED", 127.0, 37.5, -18, -12),
    (23, "ME", "US sanctions Iran shadow banks", "CONFIRMED", 51.4, 35.7, 6, -6),
    (24, "AS", "Indonesia names 6 treason suspects", "REPORTED", 106.8, -6.2, 14, 8),
    (25, "AM", "Bolsonaro taken to ICU", "CONFIRMED", -47.9, -15.8, 0, 0),
    (26, "AM", "Colombia fuel fund owes 11.4tn pesos", "REPORTED", -74.1, 4.7, 0, 0),
    (27, "AS", "China official sentenced to death", "REPORTED", 116.4, 39.9, 0, 0),
    (28, "AF", "Omo-Agege survives attack; 4 die", "REPORTED", 6.0, 5.5, 0, 0),
    (29, "AF", "Libya seeks UN probe of Benghazi strike", "CONFIRMED", 20.1, 32.1, -8, -18),
    (30, "AF", "Sudan intercepts drones from Ethiopia", "REPORTED", 32.5, 15.6, 0, 14),
    (31, "ME", "Hamas executes \u2018collaborator\u2019", "REPORTED", 34.5, 31.5, 14, 8),
    (32, "ME", "Israeli strikes kill 3 in Gaza", "REPORTED", 34.5, 31.5, -16, -2),
    (33, "ME", "UNRWA staffer killed in Gaza", "REPORTED", 34.5, 31.5, -16, 16),
    (34, "ME", "Houthi attacks in Taiz kill 2", "REPORTED", 44.0, 13.6, 8, 6),
    (35, "EU", "Murmansk governor held for graft", "REPORTED", 33.1, 69.0, 16, -10),
    (36, "EU", "Finland backs border tank barriers", "CONFIRMED", 24.9, 60.2, 8, -14),
    (37, "EU", "Yamal out of Barcelona UCL trip", "CONFIRMED", 2.2, 41.4, -18, 12),
    (38, "AS", "Gill: lift saliva ban", "REPORTED", 174.8, -41.3, -12, 8),
    (39, "AS", "SK hynix shares +20%", "CONFIRMED", 127.4, 37.2, 14, 8),
    (40, "AM", "Trump halts lead-azide blasts", "CONFIRMED", -93.6, 41.6, 0, 0),
    (41, "AS", "Bisleri water fails safety test", "CONFIRMED", 77.2, 28.6, 14, -8),
]
# lead/mid pin positions (lon, lat) — same numbering as stories
PINS = {
    1: (20.1, 32.1), 2: (56.5, 26.6), 3: (-122.0, 37.4), 4: (30.7, 36.9),
    5: (30.5, 50.5), 6: (21.0, 52.2), 7: (4.35, 50.85), 8: (-77.0, 38.9),
    10: (106.8, -6.2), 11: (106.2, -6.2), 12: (-107.4, 24.8),
}
for _b in BRIEFS:
    PINS[_b[0]] = (_b[4], _b[5])
PIN_DXDY = {b[0]: (b[6], b[7]) for b in BRIEFS}
PIN_DXDY.update({1: (-14, 10), 2: (16, -12), 6: (20, -2), 7: (-16, 8), 10: (-20, -4), 11: (-8, 14)})

NUMBERS = [  # (big, label, story no.)
    ("153", "DRONES IN ONE NIGHT", 5),
    ("7", "NAVAL DRONES", 1),
    ("33%", "NVIDIA SHARE JUMP", 3),
    ("258", "HOUSE SEATS", 8),
    ("24", "DEAD IN FACTORY FIRE", 11),
    ("$1.62bn", "AID FOR NEPAL", 13),
]
TIMELINE = [  # (utc hour float, label) — labels alternate above/below the line
    (6.0, "06:00 \u00b7 153 DRONES"),
    (7.0, "07:00 \u00b7 BENGHAZI CLAIM"),
    (10.0, "10:00 \u00b7 POWER INDEX"),
    (11.0, "11:00 \u00b7 VP PICKS"),
    (13.5, "13:30 \u00b7 COP31 BACKLASH"),
    (14.0, "14:00 \u00b7 HUANG RETURNS"),
]
REGION_COUNTS = [("AF", 5), ("ME", 6), ("AM", 7), ("AS", 13), ("EU", 7), ("OC", 2), ("WORLD", 1)]

# coarse world map: row -> list of (col_start, col_end), 96 cols x 48 rows
MAP_ROWS = {
    2: [(33, 40)], 3: [(30, 42), (58, 80)], 4: [(10, 20), (32, 42), (55, 95)],
    5: [(5, 22), (31, 41), (55, 95)], 6: [(3, 28), (41, 43), (55, 95)],
    7: [(4, 30), (41, 43), (45, 58), (60, 95)],
    8: [(6, 32), (46, 48), (48, 60), (62, 95)],
    9: [(8, 32), (45, 62), (64, 95)], 10: [(10, 32), (44, 64), (66, 95)],
    11: [(14, 30), (44, 64), (66, 90)], 12: [(14, 30), (45, 60), (62, 86)],
    13: [(15, 29), (45, 58), (56, 64), (66, 86)],
    14: [(16, 29), (43, 60), (66, 72), (74, 84)],
    15: [(17, 28), (43, 61), (66, 71), (73, 76), (78, 84)],
    16: [(18, 27), (44, 52), (56, 62), (66, 71), (73, 76)],
    17: [(20, 27), (56, 62), (66, 70), (73, 76)],
    18: [(22, 27), (56, 61), (66, 70), (73, 75)],
    19: [(26, 30), (56, 60), (67, 69)], 20: [(26, 33), (43, 61), (57, 59)],
    21: [(27, 34), (44, 61)], 22: [(27, 35), (45, 61)],
    23: [(28, 35), (45, 60), (73, 85)], 24: [(28, 35), (46, 60), (74, 84)],
    25: [(28, 35), (47, 59), (78, 89)], 26: [(29, 34), (48, 58), (78, 89)],
    27: [(29, 34), (48, 58), (78, 88)], 28: [(30, 34), (49, 57), (79, 88)],
    29: [(30, 33), (49, 56), (79, 87)], 30: [(30, 33), (50, 56), (80, 86)],
    31: [(30, 33), (50, 55), (81, 86)], 32: [(31, 33), (51, 54), (82, 85), (92, 94)],
    33: [(31, 32), (52, 54), (83, 84), (92, 93)], 34: [(31, 32), (83, 84), (92, 93)],
    35: [(31, 31), (92, 92)], 36: [(31, 31)],
}

# ---------- helpers ----------
def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def text(d, x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

def num_chip(d, x, y, n, region, size=17):
    """Story number in a region-coloured square (in the TEXT block, never on the art)."""
    d.rectangle([x, y, x + size, y + size], fill=REGION[region])
    t = str(n)
    f = F_SANS_B(10 if len(t) < 2 else 9)
    tw = d.textlength(t, font=f)
    d.text((x + (size - tw) / 2, y + size / 2 - 6), t, font=f, fill=WHITE)

def starburst(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)

# ---------- illustration archetypes (flat, geometric; no human figures) ----------
def illu_sea(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=(44, 62, 86))          # night sky
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(232, 214, 170))  # moon
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)         # sea
    d.rectangle([x, y + h * 0.62, x + w, y + h * 0.62 + 3], fill=(120, 150, 180))
    # warship silhouette
    hx, hy = x + w * 0.30, y + h * 0.66
    d.polygon([(hx, hy), (hx + 150, hy), (hx + 132, hy + 22), (hx + 12, hy + 22)], fill=(16, 20, 28))
    d.rectangle([hx + 52, hy - 20, hx + 92, hy], fill=(16, 20, 28))
    d.rectangle([hx + 66, hy - 34, hx + 76, hy - 20], fill=(16, 20, 28))
    starburst(d, hx + 108, hy - 8, 16, (255, 176, 32))             # blast
    for i in range(7):                                             # drone boats
        bx = x + 14 + i * 18
        by = y + h - 16 - (i % 2) * 8
        d.ellipse([bx, by, bx + 9, by + 5], fill=WHITE)
        d.line([bx - 12, by + 3, bx, by + 3], fill=(160, 190, 210), width=1)
    text(d, x + w - 8, y + h - 34, big, F_SANS_B(30), fill=WHITE, anchor="ra")

def illu_strait(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 46, y + 6, x + w - 16, y + 36], fill=(178, 62, 44))  # red sun
    d.polygon([(x, y + h), (x, y + 26), (x + 62, y + h * 0.55), (x + 62, y + h)], fill=SAND)
    d.polygon([(x + w, y + h), (x + w, y + 34), (x + w - 58, y + h * 0.55), (x + w - 58, y + h)], fill=SAND)
    d.polygon([(x + 62, y + h * 0.55), (x + w - 58, y + h * 0.55), (x + w - 58, y + h), (x + 62, y + h)], fill=(52, 96, 128))  # strait
    tx, ty = x + w * 0.36, y + h * 0.66
    d.rectangle([tx, ty, tx + 92, ty + 12], fill=(20, 26, 34))     # tanker
    d.rectangle([tx + 62, ty - 12, tx + 74, ty], fill=(20, 26, 34))
    d.line([x + 70, y + h * 0.52, x + w - 66, y + h * 0.52], fill=BRICK, width=2)
    for i in range(5):
        d.line([x + 78 + i * 30, y + h * 0.52 - 4, x + 78 + i * 30, y + h * 0.52 + 4], fill=BRICK, width=2)
    text(d, x + 10, y + 6, big, F_SANS_B(30), fill=INK)

def illu_chip(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=(18, 38, 26))           # dark board
    for i in range(4):                                             # circuit traces
        yy = y + 12 + i * 16
        d.line([x + 8, yy, x + w - 60, yy], fill=(64, 120, 70), width=2)
        d.ellipse([x + w - 62, yy - 3, x + w - 56, yy + 3], fill=(118, 185, 0))
    cx, cy = x + w * 0.30, y + h * 0.52
    d.rectangle([cx - 34, cy - 26, cx + 34, cy + 26], fill=(30, 58, 40), outline=(118, 185, 0), width=2)
    d.rectangle([cx - 18, cy - 13, cx + 18, cy + 13], fill=(118, 185, 0))
    text(d, cx, cy - 2, "NV", F_SANS_B(15), fill=(18, 38, 26), anchor="mm")
    d.polygon([(x + w - 96, y + h - 22), (x + w - 52, y + h - 52), (x + w - 26, y + h - 30), (x + w - 8, y + h - 44)],
              fill=None, outline=(255, 255, 255), width=3)
    d.polygon([(x + w - 8, y + h - 44), (x + w - 22, y + h - 44), (x + w - 8, y + h - 30)], fill=WHITE)
    text(d, x + w - 10, y + 4, big, F_SANS_B(26), fill=(150, 220, 90), anchor="ra")

def illu_climate(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    d.ellipse([x + w - 40, y + 4, x + w - 16, y + 28], fill=(214, 148, 32))  # sun
    tx, ty = x + 20, y + 6
    d.rounded_rectangle([tx, ty, tx + 14, ty + 30], radius=7, fill=WHITE, outline=INK, width=2)
    d.rectangle([tx + 3, ty + 14, tx + 11, ty + 27], fill=BRICK)
    d.ellipse([tx - 2, ty + 26, tx + 16, ty + 42], fill=BRICK)
    for i in range(3):
        d.line([tx + 18, ty + 6 + i * 9, tx + 26, ty + 6 + i * 9], fill=INK, width=2)
    d.polygon([(x + 64, y + h - 6), (x + 110, y + h - 6), (x + 87, y + h - 26)], fill=(91, 122, 58))
    text(d, x + w - 8, y + h - 26, big, F_SANS_B(22), fill=BRICK, anchor="ra")

def illu_drones(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(214, 138, 44))   # dusk
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(58, 44, 74))
    d.polygon([(x, y + h), (x, y + h - 26), (x + 40, y + h - 40), (x + 80, y + h - 26), (x + w, y + h - 18), (x + w, y + h)], fill=(30, 30, 40))
    for i, (dx_, dy_) in enumerate([(30, 16), (90, 30), (150, 12), (190, 26)]):
        d.ellipse([x + dx_, y + dy_, x + dx_ + 14, y + dy_ + 6], fill=(25, 25, 30))
        d.line([x + dx_ + 2, y + dy_ + 3, x + dx_ - 12, y + dy_ + 3], fill=(25, 25, 30), width=2)
    starburst(d, x + w - 40, y + 22, 12, (255, 220, 120))
    text(d, x + 8, y + h - 36, big, F_SANS_B(28), fill=WHITE)

def illu_awacs(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 228))
    d.ellipse([x + 12, y + 8, x + 44, y + 26], fill=WHITE)
    d.ellipse([x + w - 70, y + 26, x + w - 34, y + 40], fill=WHITE)
    cx, cy = x + w * 0.5, y + h * 0.52
    d.ellipse([cx - 16, cy - 26, cx + 16, cy - 12], fill=(40, 48, 60))  # radar dome
    d.rectangle([cx - 3, cy - 12, cx + 3, cy - 4], fill=(40, 48, 60))
    d.polygon([(cx - 78, cy), (cx + 78, cy + 4), (cx + 70, cy + 12), (cx - 70, cy + 12)], fill=(40, 48, 60))
    d.polygon([(cx - 46, cy + 4), (cx + 30, cy + 4), (cx + 44, cy + 20), (cx - 58, cy + 20)], fill=(40, 48, 60))
    d.polygon([(cx + 40, cy + 2), (cx + 78, cy - 16), (cx + 84, cy - 8), (cx + 52, cy + 8)], fill=(40, 48, 60))
    text(d, x + w - 8, y + 4, big, F_SANS_B(28), fill=NAVY, anchor="ra")

def illu_sanctions(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 96))           # EU blue
    import math
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = x + 52 + 26 * math.cos(ang), y + h * 0.5 + 20 * math.sin(ang)
        starburst(d, sx, sy, 4, (255, 204, 0))
    d.rectangle([x + 108, y + 8, x + w - 14, y + h - 8], fill=WHITE)
    d.rectangle([x + 118, y + 14, x + w - 24, y + 19], fill=NAVY)
    for i in range(2):
        d.line([x + 118, y + 26 + i * 8, x + w - 24 - i * 22, y + 26 + i * 8], fill=(150, 150, 150), width=2)
    text(d, x + w - 18, y + h - 24, big, F_SANS_B(20), fill=NAVY, anchor="ra")

def illu_capitol(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    cx = x + w * 0.42
    d.pieslice([cx - 22, y + 2, cx + 22, y + 20], 180, 360, fill=(90, 100, 112))
    d.rectangle([cx - 46, y + 12, cx + 46, y + 17], fill=(70, 80, 92))
    for i in range(5):
        d.rectangle([cx - 42 + i * 18, y + 17, cx - 35 + i * 18, y + 40], fill=(90, 100, 112))
    d.rectangle([cx - 52, y + 40, cx + 52, y + 48], fill=(70, 80, 92))
    text(d, x + w - 10, y + 6, big, F_SANS_B(26), fill=NAVY, anchor="ra")

def illu_podium(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=(232, 224, 200))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 90, 60))
    for fx in (x + 20, x + w - 96):                                  # two flags, red over white
        d.line([fx + 12, y + 6, fx + 12, y + h - 14], fill=INK, width=2)
        d.rectangle([fx + 12, y + 6, fx + 40, y + 18], fill=(200, 40, 30))
        d.rectangle([fx + 12, y + 18, fx + 40, y + 30], fill=WHITE)
    px, py = x + w * 0.5 - 24, y + h - 36
    d.polygon([(px, py + 22), (px + 48, py + 22), (px + 40, py), (px + 8, py)], fill=(70, 58, 44))
    d.rectangle([px + 8, py + 8, px + 40, py + 16], fill=WHITE)
    text(d, x + w - 8, y + 2, big, F_SANS_B(26), fill=BRICK, anchor="ra")

def illu_factory(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 46))
    for i in range(4):
        d.ellipse([x + 20 + i * 26, y + 6 + (i % 2) * 6, x + 44 + i * 26, y + 22 + (i % 2) * 6], fill=(120, 120, 128))
    bx, by = x + 16, y + h - 40
    d.polygon([(bx, by), (bx + 90, by), (bx + 90, by + 26), (bx, by + 26)], fill=(90, 88, 84))
    d.rectangle([bx + 96, by - 14, bx + 108, by + 26], fill=(90, 88, 84))
    for i, fx in enumerate((bx + 8, bx + 40, bx + 72)):
        d.polygon([(fx, by - 4), (fx + 10, by - 26), (fx + 20, by - 4)], fill=(255, 176, 32) if i != 1 else (255, 110, 20))
    d.rectangle([bx + 116, by + 4, bx + 150, by + 26], fill=(60, 58, 54))
    text(d, x + w - 10, y + h - 34, big, F_SANS_B(28), fill=(255, 176, 32), anchor="ra")

def illu_capture(d, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=(24, 30, 38))
    for i in range(6):
        bx = x + 12 + i * 20
        d.rectangle([bx, y, bx + 7, y + h], fill=(70, 78, 88))
    starburst(d, x + w * 0.5, y + h * 0.42, 20, (212, 172, 44))
    text(d, x + w * 0.5, y + h * 0.42 - 8, "\u2605", F_SANS_B(18), fill=(24, 30, 38), anchor="mm")
    text(d, x + w - 10, y + h - 34, big, F_SANS_B(28), fill=WHITE, anchor="ra")

ILLU = {"sea": illu_sea, "strait": illu_strait, "chip": illu_chip, "climate": illu_climate,
        "drones": illu_drones, "awacs": illu_awacs, "sanctions": illu_sanctions,
        "capitol": illu_capitol, "podium": illu_podium, "factory": illu_factory,
        "capture": illu_capture}

# ---------- map ----------
def draw_map(d, x0, y0, w, h):
    cw, chh = w / 96.0, h / 48.0
    for r, spans in MAP_ROWS.items():
        for c1, c2 in spans:
            for c in range(c1, c2 + 1):
                cx, cy = x0 + c * cw + cw / 2, y0 + r * chh + chh / 2
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=SAGE)
    def proj(lon, lat):
        return (x0 + (lon + 180) / 360.0 * w, y0 + (90 - lat) / 180.0 * h)
    # region of each story number
    reg = {}
    for s in LEADS + MIDS:
        reg[s[0]] = s[1]
    for b in BRIEFS:
        reg[b[0]] = b[1]
    for n in sorted(PINS):
        lon, lat = PINS[n]
        px, py = proj(lon, lat)
        dx, dy = PIN_DXDY.get(n, (0, 0))
        if dx or dy:
            d.line([px, py, px + dx, py + dy], fill=GREY, width=1)
            px, py = px + dx, py + dy
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=REGION[reg[n]], outline=WHITE, width=1)
        t = str(n)
        f = F_SANS_B(8 if len(t) == 1 else 7)
        tw = d.textlength(t, font=f)
        d.text((px - tw / 2, py - 5), t, font=f, fill=WHITE)

# ---------- layout ----------
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = M, W - M
    cw = x1 - x0

    # --- masthead ---
    text(d, x0, 8, "THE WORLD, CHECKED", F_SANS_B(13), fill=INK)
    text(d, x1, 8, "PRESS TIME 24:00 UTC", F_SANS_B(13), fill=BRICK, anchor="ra")
    d.line([x0, 28, x1, 28], fill=INK, width=2)
    date_s = "MONDAY 23 NOVEMBER 2026"
    df = F_SERIF_B(56)
    assert d.textlength(date_s, font=df) <= cw, "date too wide"
    text(d, x0, 32, date_s, df, fill=INK)
    sub = "War spreads to a new sea.  A blockade tightens.  A CEO comes back."
    text(d, x0, 102, sub, F_SANS(19), fill=BRICK)

    # --- counts bar ---
    y = 134
    text(d, x0, y, "41 STORIES  \u00b7  7 REGIONS  \u00b7  ALL DATED MONDAY 23 NOVEMBER 2026",
         F_SANS_B(13), fill=NAVY)
    rx = x1
    for code, cnt in reversed(REGION_COUNTS):
        s = f"{code} {cnt}"
        f = F_SANS_B(11)
        tw = d.textlength(s, font=f)
        rx -= tw
        d.rectangle([rx - 16, y - 1, rx - 4, y + 13], fill=REGION[code])
        d.text((rx - 15, y), str(cnt), font=F_SANS_B(9), fill=WHITE)
        text(d, rx, y, code, f, fill=INK)
        rx -= 10
    d.line([x0, 158, x1, 158], fill=CREAM_LINE, width=1)

    # --- UTC strip (labels alternate above / below the line, each ONE line) ---
    y = 164
    text(d, x0, y, "THE DAY IN UTC", F_SANS_B(11), fill=GREY)
    line_y = y + 26
    tx0, tx1 = x0 + 8, x1 - 8
    d.line([tx0, line_y, tx1, line_y], fill=INK, width=2)
    d.line([tx0, line_y - 4, tx0, line_y + 4], fill=INK, width=2)
    d.line([tx1, line_y - 4, tx1, line_y + 4], fill=BRICK, width=3)
    text(d, tx0, line_y + 8, "00:00", F_SANS_B(10), fill=GREY)
    text(d, tx1, line_y - 22, "24:00 PRESS TIME", F_SANS_B(10), fill=BRICK, anchor="ra")
    for i, (hr, label) in enumerate(TIMELINE):
        px = tx0 + (hr / 24.0) * (tx1 - tx0)
        d.line([px, line_y - 5, px, line_y + 5], fill=INK, width=2)
        d.ellipse([px - 3, line_y - 3, px + 3, line_y + 3], fill=INK)
        f = F_SANS_B(10)
        assert d.textlength(label, font=f) <= 150, f"timeline label too long: {label}"
        if i % 2 == 0:
            text(d, px, line_y - 20, label, f, fill=INK, anchor="ma")
        else:
            text(d, px, line_y + 8, label, f, fill=INK, anchor="ma")

    # --- numbers ribbon (dark strip; numbers are the page's big figures) ---
    y = 212
    d.rectangle([x0, y, x1, y + 56], fill=NAVY_D)
    cell_w = cw / 6.0
    for i, (big, label, sno) in enumerate(NUMBERS):
        cx = x0 + i * cell_w
        if i:
            d.line([cx, y + 8, cx, y + 48], fill=(70, 90, 120), width=1)
        bf = F_SANS_B(30 if len(big) > 5 else 34)
        text(d, cx + 10, y + 2, big, bf, fill=WHITE)
        lf = F_SANS_B(10)
        text(d, cx + 10, y + 38, label, lf, fill=(190, 205, 220))
        text(d, x0 + (i + 1) * cell_w - 10, y + 4, f"#{sno}", F_SANS_B(10),
             fill=(255, 200, 90), anchor="ra")

    # --- lead cards ---
    y = 274
    lead_w = (cw - 2 * 12) // 3
    lead_h = 212
    for i, (n, reg, field, place, title, deck, status, big, arch) in enumerate(LEADS):
        cx = x0 + i * (lead_w + 12)
        d.rectangle([cx, y, cx + lead_w, y + lead_h], outline=(190, 180, 160), width=1, fill=WHITE)
        ILLU[arch](d, cx + 1, y + 1, lead_w - 2, 96, big)
        ty = y + 102
        num_chip(d, cx + 10, ty, n, reg, size=17)
        text(d, cx + 32, ty + 1, f"{place} \u00b7 {field}", F_SANS_B(11), fill=INK)
        lines = wrap(d, title, F_SANS_B(18), lead_w - 20)
        ly = ty + 22
        for ln in lines[:2]:
            text(d, cx + 10, ly, ln, F_SANS_B(18), fill=INK)
            ly += 22
        dlines = wrap(d, deck, F_SANS(11), lead_w - 20)
        dy_ = ty + 68
        for ln in dlines[:2]:
            text(d, cx + 10, dy_, ln, F_SANS(11), fill=GREY)
            dy_ += 13
        sc = STATUS_C[status]
        d.ellipse([cx + 10, y + lead_h - 13, cx + 17, y + lead_h - 6], fill=sc)
        text(d, cx + 22, y + lead_h - 15, status, F_SANS_B(10), fill=sc)

    # --- mid cards (4 x 2) ---
    y = 494
    mid_w = (cw - 3 * 12) // 4
    mid_h = 128
    for i, (n, reg, field, place, title, status, big, arch) in enumerate(MIDS):
        r, c = divmod(i, 4)
        cx = x0 + c * (mid_w + 12)
        cy = y + r * (mid_h + 8)
        d.rectangle([cx, cy, cx + mid_w, cy + mid_h], outline=(190, 180, 160), width=1, fill=WHITE)
        ILLU[arch](d, cx + 1, cy + 1, mid_w - 2, 56, big)
        ty = cy + 60
        num_chip(d, cx + 8, ty, n, reg, size=15)
        text(d, cx + 27, ty, f"{place} \u00b7 {field}", F_SANS_B(9), fill=INK)
        lines = wrap(d, title, F_SANS_B(14), mid_w - 16)
        ly = ty + 17
        for ln in lines[:2]:
            text(d, cx + 8, ly, ln, F_SANS_B(14), fill=INK)
            ly += 17
        sc = STATUS_C[status]
        d.ellipse([cx + 8, cy + mid_h - 12, cx + 15, cy + mid_h - 5], fill=sc)
        text(d, cx + 19, cy + mid_h - 14, status, F_SANS_B(9), fill=sc)

    # --- bottom zone: map + numbered brief list ---
    y = 766
    map_w = 320
    text(d, x0, y, "WHERE IT HAPPENED", F_SANS_B(11), fill=GREY)
    text(d, x0 + map_w + 12, y, "ALSO ON MONDAY \u2014 30 MORE STORIES, NUMBERED AS ON THE MAP",
         F_SANS_B(11), fill=GREY)
    draw_map(d, x0, y + 18, map_w, 184)
    bx = x0 + map_w + 12
    bw = x1 - bx
    col_w = (bw - 12) // 2
    bf = F_SANS(10)
    for i, (n, reg, title, status, _lon, _lat, _dx, _dy) in enumerate(BRIEFS):
        col, row = divmod(i, 15)
        lx = bx + col * (col_w + 12)
        ly = y + 18 + row * 12
        text(d, lx, ly, f"{n:02d}.", F_SANS_B(10), fill=REGION[reg])
        t = f"{title} \u00b7 {reg}"
        assert d.textlength(t, font=bf) <= col_w - 30, f"brief too long: {t}"
        text(d, lx + 24, ly, t, bf, fill=INK)
        d.ellipse([lx + col_w - 8, ly + 2, lx + col_w - 1, ly + 9], fill=STATUS_C[status])

    # --- DATE CHECK bar (its own box, visually separate from everything above) ---
    y = 976
    d.rectangle([x0, y, x1, y + 38], fill=NAVY_D)
    text(d, x0 + 10, y + 4,
         "DATE CHECK \u2014 Every story above is dated Monday 23 November 2026.  Press time 24:00 UTC.",
         F_SANS_B(12), fill=WHITE)
    lx = x0 + 10
    for st in ("CONFIRMED", "REPORTED", "CLAIM"):
        d.ellipse([lx, y + 24, lx + 7, y + 31], fill=STATUS_C[st])
        lab = {"CONFIRMED": "CONFIRMED \u2014 verified by two sources or an official statement",
               "REPORTED": "REPORTED \u2014 reported, single source",
               "CLAIM": "CLAIM \u2014 one side\u2019s claim, not confirmed"}[st]
        text(d, lx + 11, y + 22, lab, F_SANS(10), fill=(210, 220, 232))
        lx += d.textlength(lab, font=F_SANS(10)) + 30

    return img

if __name__ == "__main__":
    out = os.environ.get("OUT", "entry.png")
    build().save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
