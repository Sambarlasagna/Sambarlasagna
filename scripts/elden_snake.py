#!/usr/bin/env python3
"""Generates an Elden-style animated contribution snake (a gold wyrm sweeping the grid).

Usage: python3 scripts/elden_snake.py [github_user] [output.svg]
Only needs the Python standard library; reads the public contribution calendar.
Optional: --preview-t SECONDS renders one static frame (used for checking the layout).
"""
import datetime as dt, math, os, re, sys, urllib.request
from xml.sax.saxutils import escape as e

args = [a for a in sys.argv[1:] if not a.startswith("--")]
USER = args[0] if args else os.environ.get("GITHUB_REPOSITORY_OWNER", "Sambarlasagna")
OUT = args[1] if len(args) > 1 else "assets/elden-snake.svg"
PREVIEW = None
if "--preview-t" in sys.argv:
    PREVIEW = float(sys.argv[sys.argv.index("--preview-t") + 1])
    args = [a for a in args if a != str(PREVIEW)]

GOLD, GOLDL, CREAM, GRAY = "#c8953a", "#ffe9a8", "#ecdcb0", "#9c8860"
LEVELS = ["#1a1409", "#4a3716", "#8a6320", "#c8953a", "#ffe9a8"]
FONT = "Georgia,'Times New Roman',serif"

# ---------------------------------------------------------------- data
req = urllib.request.Request(f"https://github.com/users/{USER}/contributions", headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
days = sorted(set(re.findall(r'<td[^>]*data-date="([\d-]+)"[^>]*data-level="(\d)"', html)))
if not days:
    sys.exit("no contribution data found")
m = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", html)
total = m.group(1) if m else "0"

cells = {}
first = dt.date.fromisoformat(days[0][0])
sunday = first - dt.timedelta(days=(first.weekday() + 1) % 7)
for ds, lv in days:
    d = dt.date.fromisoformat(ds)
    cells[((d - sunday).days // 7, (d.weekday() + 1) % 7)] = (d, int(lv))
ncols = max(c for c, _ in cells) + 1

# ---------------------------------------------------------------- geometry
W = 1000
pitch = min(17.0, 900.0 / ncols)
cs = pitch - 3
left = (W - ncols * pitch + 3) / 2
y0 = 104
H = y0 + 7 * pitch + 78

def center(c, r):
    return (left + c * pitch + cs / 2, y0 + r * pitch + cs / 2)

# zig-zag route: down one column, up the next ...
order = []
for c in range(ncols):
    rows = sorted(r for (cc, r) in cells if cc == c)
    if c % 2:
        rows.reverse()
    order += [(c, r) for r in rows]
pts = [center(*k) for k in order]
lead = [(pts[0][0] - pitch * i, pts[0][1]) for i in range(6, 0, -1)]
tail = [(pts[-1][0] + pitch * i, pts[-1][1]) for i in range(1, 7)]
route = lead + pts + tail
seg = [math.dist(route[i], route[i + 1]) for i in range(len(route) - 1)]
cum = [0.0]
for s in seg:
    cum.append(cum[-1] + s)
TOT = cum[-1]
SPEED = 0.11 / pitch                      # seconds per pixel
D = TOT * SPEED                           # one full loop
path_d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in route)

def pos_at(dist):
    dist = max(0, min(TOT, dist))
    for i in range(len(seg)):
        if dist <= cum[i + 1]:
            f = (dist - cum[i]) / (seg[i] or 1)
            a, b = route[i], route[i + 1]
            return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])))
    return (*route[-1], 0)

# ---------------------------------------------------------------- svg
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}">',
     f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0906"/><stop offset="1" stop-color="#17110a"/></linearGradient>'
     f'<radialGradient id="gl" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffe9a8" stop-opacity="0.9"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>'
     f'<linearGradient id="gold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a87a2a"/><stop offset="0.5" stop-color="{GOLDL}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient></defs>',
     f'<style>text{{font-family:{FONT}}}</style>',
     f'<rect width="{W}" height="{H:.0f}" fill="url(#bg)"/>',
     f'<rect x="10" y="10" width="{W-20}" height="{H-20:.0f}" fill="none" stroke="{GOLD}" stroke-opacity="0.55" stroke-width="1.5"/>',
     f'<rect x="18" y="18" width="{W-36}" height="{H-36:.0f}" fill="none" stroke="{GOLD}" stroke-opacity="0.22"/>']
for (x, y) in [(10, 10), (W-10, 10), (10, H-10), (W-10, H-10)]:
    o.append(f'<polygon points="{x},{y-6} {x+6},{y} {x},{y+6} {x-6},{y}" fill="{GOLDL}"/>')

o.append(f'<text x="50" y="56" font-size="20" fill="url(#gold)" font-weight="bold" letter-spacing="1">{e(total)} contributions in the last year</text>')
o.append(f'<text x="950" y="56" font-size="13" fill="{GRAY}" font-style="italic" text-anchor="end">@{e(USER)}</text>')

# month labels
last_m, last_x = None, -99
for c in range(ncols):
    ds = [cells[(c, r)][0] for r in range(7) if (c, r) in cells]
    if not ds:
        continue
    d = min(ds)
    x = left + c * pitch
    if d.month != last_m and x - last_x > 3 * pitch:
        o.append(f'<text x="{x:.1f}" y="{y0-10}" font-size="11" fill="{GRAY}">{d.strftime("%b")}</text>')
        last_m, last_x = d.month, x

# cells
eat_t = {}
for i, k in enumerate(order):
    eat_t[k] = cum[6 + i] / TOT
head_dist = None
if PREVIEW is not None:
    head_dist = (PREVIEW / D) * TOT
for (c, r), (d, lv) in sorted(cells.items()):
    x = left + c * pitch; y = y0 + r * pitch
    stroke = f' stroke="{GOLD}" stroke-opacity="0.18"' if lv == 0 else ""
    base = f'<rect x="{x:.1f}" y="{y:.1f}" width="{cs:.1f}" height="{cs:.1f}" rx="3" fill="{LEVELS[lv]}"{stroke}'
    if PREVIEW is not None:
        eaten = lv > 0 and head_dist is not None and cum[6 + order.index((c, r))] <= head_dist
        o.append(base + (' opacity="0.22"/>' if eaten else "/>"))
    elif lv == 0:
        o.append(base + "/>")
    else:
        t = min(eat_t[(c, r)], 0.995)
        o.append(base + f'><animate attributeName="opacity" values="1;1;0.22;1" keyTimes="0;{t:.4f};{t+0.002:.4f};1" dur="{D:.2f}s" repeatCount="indefinite"/></rect>')

# the wyrm
N = 12                                  # head + body segments
LAG = 1.45 * pitch                      # distance between segments
def lerp(a, b, f): return int(a + (b - a) * f)
def body_color(f):
    return "#%02x%02x%02x" % (lerp(0xff, 0x8a, f), lerp(0xd9, 0x63, f), lerp(0x80, 0x20, f))
HEAD = ('<g><circle r="15" fill="url(#gl)" opacity="0.8"/>'
        f'<polygon points="11,0 4,-3 6,-8 0,-5 -6,-6 -8,0 -6,6 0,5 6,8 4,3" fill="{GOLDL}" stroke="#a87a2a" stroke-width="0.8"/>'
        '<circle cx="1" cy="-2.3" r="1.3" fill="#b5301f"/><circle cx="1" cy="2.3" r="1.3" fill="#b5301f"/></g>')
for k in reversed(range(N)):
    f = k / (N - 1)
    rad = 6.4 - 3.6 * f
    shape = HEAD if k == 0 else f'<circle r="{rad:.1f}" fill="{body_color(f)}" stroke="#2a1d0a" stroke-width="0.8"/>'
    if PREVIEW is not None:
        x, y, ang = pos_at(head_dist - k * LAG)
        rot = f" rotate({ang:.0f})" if k == 0 else ""
        o.append(f'<g transform="translate({x:.1f},{y:.1f}){rot}">{shape}</g>')
    else:
        b = k * LAG * SPEED
        o.append(f'<g>' + (f'<set attributeName="display" to="none" begin="0s" end="{b:.2f}s"/>' if k else "") +
                 f'<animateMotion dur="{D:.2f}s" begin="{b:.2f}s" repeatCount="indefinite" path="{path_d}"' +
                 (' rotate="auto"' if k == 0 else "") + f'/>{shape}</g>')

# legend
lx = 950 - 5 * (cs + 3) - 90
o.append(f'<text x="{lx:.0f}" y="{H-34:.0f}" font-size="11" fill="{GRAY}" text-anchor="end">Less</text>')
for i, col in enumerate(LEVELS):
    o.append(f'<rect x="{lx+10+i*(cs+3):.1f}" y="{H-44:.0f}" width="{cs:.1f}" height="{cs:.1f}" rx="3" fill="{col}" stroke="{GOLD}" stroke-opacity="0.18"/>')
o.append(f'<text x="{lx+16+5*(cs+3):.0f}" y="{H-34:.0f}" font-size="11" fill="{GRAY}">More</text>')
o.append("</svg>")
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(o))
print(f"wrote {OUT}: {len(order)} cells, loop {D:.1f}s, {os.path.getsize(OUT)//1024} KB")
