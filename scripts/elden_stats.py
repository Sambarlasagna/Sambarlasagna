#!/usr/bin/env python3
"""Generates an animated, Elden-styled GitHub stats panel (overview tiles + top languages).

Usage: python3 scripts/elden_stats.py [github_user] [output.svg]
Standard library only. Uses the GitHub API (GITHUB_TOKEN env var recommended) and falls back to
scraping public pages when the API is rate limited.
"""
import datetime as dt, json, os, random, re, sys, urllib.request
from xml.sax.saxutils import escape as e

USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REPOSITORY_OWNER", "Sambarlasagna")
OUT = sys.argv[2] if len(sys.argv) > 2 else "assets/elden-stats.svg"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
GOLD, GOLDL, CREAM, GRAY = "#c8953a", "#ffe9a8", "#ecdcb0", "#9c8860"
FONT = "Georgia,'Times New Roman',serif"

def fetch(url, api=False):
    h = {"User-Agent": "Mozilla/5.0"}
    if api:
        h["Accept"] = "application/vnd.github+json"
        if TOKEN: h["Authorization"] = f"Bearer {TOKEN}"
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30).read().decode("utf-8", "ignore")
    except Exception as ex:
        print("fetch failed:", url, ex); return None

def api(path):
    t = fetch("https://api.github.com" + path, api=True)
    try:
        d = json.loads(t) if t else None
    except Exception:
        return None
    return None if (isinstance(d, dict) and "message" in d and "total_count" not in d and "login" not in d) else d

# ------------------------------------------------------------ data
stats = {"contrib": None, "commits": None, "prs": None, "issues": None, "repos": None, "stars": None}
langs = {}

html = fetch(f"https://github.com/users/{USER}/contributions") or ""
m = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", html)
if m: stats["contrib"] = int(m.group(1).replace(",", ""))

for key, q in [("prs", f"author:{USER}+type:pr"), ("issues", f"author:{USER}+type:issue")]:
    d = api(f"/search/issues?q={q}&per_page=1")
    if d: stats[key] = d.get("total_count")
d = api(f"/search/commits?q=author:{USER}&per_page=1")
if d: stats["commits"] = d.get("total_count")

user = api(f"/users/{USER}")
repos = api(f"/users/{USER}/repos?per_page=100&type=owner") if user else None
if user and isinstance(repos, list):
    stats["repos"] = user.get("public_repos", len(repos))
    stats["stars"] = sum(r.get("stargazers_count", 0) for r in repos)
    for r in [r for r in repos if not r.get("fork")][:60]:
        ld = api(f"/repos/{USER}/{r['name']}/languages")
        for k, v in (ld or {}).items():
            langs[k] = langs.get(k, 0) + v
if not langs:  # fallback: scrape the repositories tab (language by repo count)
    page = fetch(f"https://github.com/{USER}?tab=repositories") or ""
    blocks = page.split('itemprop="owns"')[1:]
    stars = 0
    for b in blocks:
        l = re.search(r'itemprop="programmingLanguage">([^<]*)<', b)
        if l and "Forked from" not in b:
            langs[l.group(1).strip()] = langs.get(l.group(1).strip(), 0) + 1
        s = re.search(r'/stargazers"[^>]*>(.*?)</a>', b, re.S)
        if s:
            n = re.sub(r"<[^>]+>", "", s.group(1)).strip().replace(",", "")
            stars += int(n) if n.isdigit() else 0
    c = re.search(r'Counter">(\d+)<', page)
    if stats["repos"] is None and c: stats["repos"] = int(c.group(1))
    if stats["stars"] is None: stats["stars"] = stars
print(stats, dict(sorted(langs.items(), key=lambda kv: -kv[1])[:6]))

# ------------------------------------------------------------ svg
W, H = 1000, 340
tot = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
def fmt(v): return "—" if v is None else (f"{v/1000:.1f}k" if v >= 10000 else f"{v:,}")

ICON = {
 "contrib": '<path d="M12 2 L21 12 L12 22 L3 12 Z"/><path d="M12 8 L16 12 L12 16 L8 12 Z"/>',
 "commits": '<circle cx="12" cy="12" r="4.5"/><path d="M2 12 H7.5 M16.5 12 H22"/>',
 "prs": '<circle cx="6" cy="5" r="2.6"/><circle cx="6" cy="19" r="2.6"/><circle cx="18" cy="19" r="2.6"/><path d="M6 7.6 V16.4 M18 16.4 V10 C18 7 16 5 13 5"/>',
 "issues": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="1.6" fill="#ffe9a8"/>',
 "repos": '<path d="M5 4 H17 A2 2 0 0 1 19 6 V20 H7 A2 2 0 0 1 5 18 Z"/><path d="M5 18 A2 2 0 0 1 7 16 H19"/>',
 "stars": '<polygon points="12,2.5 14.8,9 21.5,9.5 16.4,14 18,21 12,17.3 6,21 7.6,14 2.5,9.5 9.2,9"/>',
}
tiles = [("contrib", "Contributions", "past year"), ("commits", "Commits", "all time"), ("prs", "Pull Requests", "opened"),
         ("issues", "Issues", "opened"), ("repos", "Repositories", "public"), ("stars", "Stars", "earned")]

random.seed(7)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
defs = (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0906"/><stop offset="1" stop-color="#17110a"/></linearGradient>'
        f'<linearGradient id="gold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a87a2a"/><stop offset="0.5" stop-color="{GOLDL}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>'
        f'<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a6320"/><stop offset="1" stop-color="#ffe08a"/></linearGradient>'
        f'<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset="0.5" stop-color="{GOLDL}"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffe9a8" stop-opacity="0"/><stop offset="0.5" stop-color="#ffe9a8" stop-opacity="0.16"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="glint" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff6d8" stop-opacity="0.9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="gl" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffe9a8" stop-opacity="0.9"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>')
TX, TY, TW, TH, GAP = 44, 92, 140, 104, 12
clips = ""
for i in range(6):
    x = TX + (i % 3) * (TW + GAP); y = TY + (i // 3) * (TH + GAP)
    clips += f'<clipPath id="t{i}"><rect x="{x}" y="{y}" width="{TW}" height="{TH}"/></clipPath>'
clips += '<clipPath id="lp"><rect x="30" y="70" width="450" height="250"/></clipPath>'
o.append(defs + clips + "</defs>")
o.append(f'<style>text{{font-family:{FONT}}}</style>')
o.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
o.append(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="{GOLD}" stroke-opacity="0.55" stroke-width="1.5"/>')
o.append(f'<rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" stroke="{GOLD}" stroke-opacity="0.22"/>')
for (x, y) in [(10, 10), (W-10, 10), (10, H-10), (W-10, H-10)]:
    o.append(f'<polygon points="{x},{y-6} {x+6},{y} {x},{y+6} {x-6},{y}" fill="{GOLDL}"/>')

def head(x, title):
    return (f'<text x="{x}" y="58" font-size="14" fill="{GOLD}" letter-spacing="5">{title}</text>'
            f'<g transform="translate({x-18},52)"><polygon points="0,-6 6,0 0,6 -6,0" fill="{GOLDL}"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/></polygon></g>')
o.append(head(50, "OVERVIEW")); o.append(head(560, "TOP LANGUAGES"))
o.append(f'<line x1="44" y1="70" x2="470" y2="70" stroke="url(#fade)"/><line x1="556" y1="70" x2="956" y2="70" stroke="url(#fade)"/>')
o.append(f'<line x1="500" y1="40" x2="500" y2="{H-40}" stroke="url(#fade)" transform="rotate(0)"/>')

for i, (key, label, sub) in enumerate(tiles):
    x = TX + (i % 3) * (TW + GAP); y = TY + (i // 3) * (TH + GAP)
    o.append(f'<g>')
    o.append(f'<polygon points="{x+9},{y} {x+TW-9},{y} {x+TW},{y+9} {x+TW},{y+TH-9} {x+TW-9},{y+TH} {x+9},{y+TH} {x},{y+TH-9} {x},{y+9}" fill="#14100a" stroke="{GOLD}" stroke-opacity="0.5">'
             f'<animate attributeName="stroke-opacity" values="0.3;0.95;0.3" dur="{4+i*0.5:.1f}s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/></polygon>')
    o.append(f'<g clip-path="url(#t{i})">')
    for j in range(5):  # rising golden specks
        ex = x + 10 + random.random() * (TW - 20); r = 0.9 + random.random() * 1.6
        d = 3.5 + random.random() * 4; b = random.random() * 5
        o.append(f'<circle cx="{ex:.0f}" cy="{y+TH+4}" r="{r:.1f}" fill="#ffd980"><animate attributeName="cy" values="{y+TH+4};{y-6}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0.9;0" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')
    o.append('</g>')
    o.append(f'<g transform="translate({x+14},{y+12}) scale(1.05)" fill="none" stroke="{GOLDL}" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round">{ICON[key]}</g>')
    o.append(f'<text x="{x+TW-14}" y="{y+30}" font-size="11" fill="{GRAY}" font-style="italic" text-anchor="end">{e(sub)}</text>')
    o.append(f'<text x="{x+14}" y="{y+72}" font-size="31" fill="{GOLDL}" font-weight="bold">{fmt(stats[key])}'
             f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{0.05+i*0.02:.2f};{0.2+i*0.02:.2f}" dur="1.4s" fill="freeze"/></text>')
    o.append(f'<text x="{x+14}" y="{y+93}" font-size="13" fill="{CREAM}" letter-spacing="1">{e(label)}</text>')
    o.append('</g>')
# light sweep across the overview panel
o.append('<g clip-path="url(#lp)"><rect x="-200" y="70" width="140" height="250" fill="url(#sweep)" transform="skewX(-18)">'
         '<animate attributeName="x" values="-200;520;520" keyTimes="0;0.5;1" dur="7s" repeatCount="indefinite"/></rect></g>')

# languages
by = 106
for i, (name, v) in enumerate(top):
    pct = v / tot * 100
    bw = max(6, 400 * pct / 100 * (1 if top[0][1] / tot < 0.5 else 0.8 / (top[0][1] / tot)) * 1.0) if False else 400 * (v / top[0][1]) * 0.92
    y = by + i * 44
    o.append(f'<text x="560" y="{y}" font-size="16" fill="{CREAM}" letter-spacing="1">{e(name)}</text>')
    o.append(f'<text x="960" y="{y}" font-size="16" fill="{GOLDL}" font-weight="bold" text-anchor="end">{pct:.1f}%</text>')
    o.append(f'<clipPath id="b{i}"><rect x="560" y="{y+10}" width="{bw:.0f}" height="8"/></clipPath>')
    o.append(f'<rect x="560" y="{y+10}" width="400" height="8" fill="#2a2113"/>')
    o.append(f'<rect x="560" y="{y+10}" width="{bw:.0f}" height="8" fill="url(#bar)"><animate attributeName="width" from="0" to="{bw:.0f}" dur="1.6s" begin="{i*0.15:.2f}s" fill="freeze"/></rect>')
    o.append(f'<g clip-path="url(#b{i})"><rect x="520" y="{y+10}" width="46" height="8" fill="url(#glint)"><animate attributeName="x" values="520;{560+bw:.0f}" dur="2.6s" begin="{1.8+i*0.5:.1f}s" repeatCount="indefinite"/></rect></g>')
    o.append(f'<circle cx="{560+bw:.0f}" cy="{y+14}" r="3.5" fill="#fff3c9"><animate attributeName="r" values="2.5;5;2.5" dur="2.4s" begin="{i*0.3:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0;1" keyTimes="0;0.6;1" dur="1.8s" begin="{i*0.15:.2f}s" fill="freeze"/></circle>')
o.append(f'<text x="960" y="{H-32}" font-size="11" fill="{GRAY}" font-style="italic" text-anchor="end">@{e(USER)}  ·  updated {dt.date.today().strftime("%b %d, %Y")}</text>')
o.append("</svg>")
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(o))
print(f"wrote {OUT} ({os.path.getsize(OUT)//1024} KB)")
