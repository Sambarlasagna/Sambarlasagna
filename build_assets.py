"""Regenerates every SVG in ./assets. Edit the DATA sections and run: python3 build_assets.py"""
import json, math, textwrap, os, random
from samurai_art import samurai
from samurai_bust import samurai_bust
from samurai_style import samurai_drawing
from xml.sax.saxutils import escape as e

OUT = "assets"
os.makedirs(OUT, exist_ok=True)
ICONS = json.load(open("icons.json"))

GOLD, GOLDL, CREAM, GRAY = "#c8953a", "#ffe9a8", "#ecdcb0", "#9c8860"
FONT = "Georgia,'Times New Roman',serif"

DEFS = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0906"/><stop offset="1" stop-color="#17110a"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a87a2a"/><stop offset="0.5" stop-color="{GOLDL}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
<linearGradient id="gm" x1="-0.6" y1="0" x2="0.4" y2="0"><stop offset="0" stop-color="#a87a2a"/><stop offset="0.5" stop-color="#fff6d8"/><stop offset="1" stop-color="#c8953a"/><animate attributeName="x1" values="-0.6;1;1" keyTimes="0;0.6;1" dur="6s" repeatCount="indefinite"/><animate attributeName="x2" values="0.4;2;2" keyTimes="0;0.6;1" dur="6s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a6320"/><stop offset="1" stop-color="#ffe08a"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset="0.5" stop-color="{GOLDL}"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>
<linearGradient id="blade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff3c9"/><stop offset="1" stop-color="#b8862f"/></linearGradient>
<linearGradient id="glint" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff6d8" stop-opacity="0.9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffe9a8" stop-opacity="0"/><stop offset="0.5" stop-color="#ffe9a8" stop-opacity="0.14"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></linearGradient>
<radialGradient id="gl" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffe9a8" stop-opacity="0.9"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
</defs>
<style>text{{font-family:{FONT}}}</style>"""

def svg(w, h, body, bg=True):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{DEFS}'
    if bg:
        s += f'<rect width="{w}" height="{h}" fill="url(#bg)"/>'
    return s + body + "</svg>"

def frame(w, h):
    b = f'<rect x="10" y="10" width="{w-20}" height="{h-20}" fill="none" stroke="{GOLD}" stroke-opacity="0.55" stroke-width="1.5"/>'
    b += f'<rect x="18" y="18" width="{w-36}" height="{h-36}" fill="none" stroke="{GOLD}" stroke-opacity="0.22"/>'
    for (x, y) in [(10, 10), (w-10, 10), (10, h-10), (w-10, h-10)]:
        b += f'<polygon points="{x},{y-6} {x+6},{y} {x},{y+6} {x-6},{y}" fill="{GOLDL}"/>'
    return b

def T(x, y, s, size=14, fill=CREAM, anchor="start", weight="normal", style="normal", spacing=0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}" letter-spacing="{spacing}">{e(s)}</text>')

def para(x, y, s, chars, lh, size=14, fill=CREAM, style="normal"):
    out = ""
    for ln in textwrap.wrap(s, chars):
        out += T(x, y, ln, size, fill, style=style); y += lh
    return out, y

def sword(x, y, rot, scale=1.0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({scale})">'
            f'<polygon points="0,-24 3,-18 3,6 -3,6 -3,-18" fill="url(#blade)"/>'
            f'<rect x="-9" y="6" width="18" height="3" fill="{GOLDL}"/>'
            f'<rect x="-1.8" y="9" width="3.6" height="9" fill="#a87a2a"/>'
            f'<circle cx="0" cy="20" r="2.6" fill="{GOLDL}"/></g>')

def crossed(x, y, scale=1.0):
    return sword(x, y, 48, scale) + sword(x, y, -48, scale)

def save(name, content):
    open(f"{OUT}/{name}", "w").write(content)

# ------------------------------------------------------------------ headings
def heading(slug, title):
    w, h = 1000, 72
    tw = len(title) * 27
    lx, rx = 500 - tw/2 - 42, 500 + tw/2 + 42
    b = f'<line x1="30" y1="36" x2="{lx-24}" y2="36" stroke="url(#fade)" stroke-width="1.5"/>'
    b += f'<line x1="{rx+24}" y1="36" x2="970" y2="36" stroke="url(#fade)" stroke-width="1.5"/>'
    b += f'<g opacity="0.85"><animate attributeName="opacity" values="0.65;1;0.65" dur="3s" repeatCount="indefinite"/>' + crossed(lx, 36, 0.9) + crossed(rx, 36, 0.9) + '</g>'
    b += (f'<circle cy="36" r="2.4" fill="#fff3c9"><animate attributeName="cx" values="30;{lx-24}" dur="3.6s" repeatCount="indefinite"/>'
          '<animate attributeName="opacity" values="0;1;0" dur="3.6s" repeatCount="indefinite"/></circle>')
    b += (f'<circle cy="36" r="2.4" fill="#fff3c9"><animate attributeName="cx" values="970;{rx+24}" dur="3.6s" begin="1.2s" repeatCount="indefinite"/>'
          '<animate attributeName="opacity" values="0;1;0" dur="3.6s" begin="1.2s" repeatCount="indefinite"/></circle>')
    b += T(500, 46, title, 27, "url(#gm)", "middle", "bold", spacing=8)
    save(f"h_{slug}.svg", svg(w, h, b))

for slug, title in [("about", "ABOUT"), ("skills", "SKILLS"), ("journey", "JOURNEY"), ("tech", "TECH STACK"),
                    ("projects", "PROJECTS"), ("experience", "EXPERIENCE"), ("education", "EDUCATION"),
                    ("connect", "CONNECT"), ("activity", "ACTIVITY"), ("stats", "GITHUB STATS")]:
    heading(slug, title)

# ------------------------------------------------------------------ about
def about():
    w, h = 1000, 226
    b = frame(w, h)
    b += f'<ellipse cx="880" cy="60" rx="260" ry="120" fill="url(#gl)" opacity="0.18"><animate attributeName="opacity" values="0.1;0.28;0.1" dur="6s" repeatCount="indefinite"/></ellipse>'
    b += T(50, 62, "Jayashuriya J", 32, "url(#gm)", weight="bold", spacing=2)
    b += T(50, 90, "B.Tech Computer Science with AI & ML  ·  VIT Chennai", 15, GRAY, style="italic")
    p, _ = para(50, 124, "I build machine learning systems end to end: data pipelines, model training, serving APIs, "
                          "deployment and monitoring, from raw data to a containerised, monitored service.", 100, 24, 17)
    b += p
    x = 50
    for ti, tag in enumerate(["Machine Learning", "Deep Learning", "GenAI", "MLOps", "Data Engineering"]):
        cw = len(tag)*7.4 + 26
        b += (f'<rect x="{x}" y="172" width="{cw}" height="26" rx="3" fill="#1a1409" stroke="{GOLD}" stroke-opacity="0.5"><animate attributeName="stroke-opacity" values="0.3;1;0.3" dur="4s" begin="{ti*0.7:.1f}s" repeatCount="indefinite"/></rect>'
              + T(x+cw/2, 190, tag, 13, GOLDL, "middle", spacing=0.5))
        x += cw + 10
    random.seed(3)
    for i in range(16):
        ex = 600 + random.random()*370; r = 0.9 + random.random()*1.8; d = 4 + random.random()*5; bg = -random.random()*d
        b += (f'<circle cx="{ex:.0f}" cy="{h-24}" r="{r:.1f}" fill="#ffd980"><animate attributeName="cy" values="{h-24};26" dur="{d:.1f}s" begin="{bg:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;0.8;0" dur="{d:.1f}s" begin="{bg:.1f}s" repeatCount="indefinite"/></circle>')
    save("about.svg", svg(w, h, b))
about()

# ------------------------------------------------------------------ skills
def skills():
    w, h = 1000, 470
    b = frame(w, h)
    b += T(50, 58, "FOCUS AREAS", 14, GOLD, spacing=5)
    b += f'<line x1="50" y1="70" x2="600" y2="70" stroke="{GOLD}" stroke-opacity="0.5"/>'
    b += T(660, 58, "PROFILE", 14, GOLD, spacing=5)
    b += f'<line x1="660" y1="70" x2="950" y2="70" stroke="{GOLD}" stroke-opacity="0.5"/>'
    rows = [("Machine Learning", "PyTorch · TensorFlow · Scikit-Learn", 85),
            ("GenAI & LLMs", "RAG · LangChain · Whisper · Llama", 75),
            ("MLOps & DevOps", "MLflow · Docker · Kubernetes · Airflow", 75),
            ("Data Engineering", "PySpark · Kafka · PostgreSQL", 70),
            ("Backend", "FastAPI · Express.js · REST", 70),
            ("Frontend", "React · JavaScript", 60),
            ("Languages", "Python · SQL · C · C++ · Java", 80)]
    y = 108
    for i, (lab, sub, v) in enumerate(rows):
        b += T(50, y, lab, 18, CREAM, spacing=1)
        b += T(510, y, sub, 12.5, GRAY, "end", style="italic")
        b += f'<rect x="50" y="{y+10}" width="460" height="6" fill="#2a2113"/>'
        b += (f'<rect x="50" y="{y+10}" width="{460*v/100:.0f}" height="6" fill="url(#bar)"><animate attributeName="width" from="0" to="{460*v/100:.0f}" '
              f'dur="1.6s" begin="0s" fill="freeze"/></rect>')
        bwid = 460*v/100
        b += f'<clipPath id="sb{i}"><rect x="50" y="{y+10}" width="{bwid:.0f}" height="6"/></clipPath>'
        b += (f'<g clip-path="url(#sb{i})"><rect x="10" y="{y+10}" width="46" height="6" fill="url(#glint)"><animate attributeName="x" values="10;{50+bwid:.0f}" dur="2.6s" begin="{1.6+i*0.45:.2f}s" repeatCount="indefinite"/></rect></g>')
        b += (f'<circle cx="{50+bwid:.0f}" cy="{y+13}" r="3" fill="#fff3c9"><animate attributeName="r" values="2;5;2" dur="2.4s" begin="{i*0.3:.1f}s" repeatCount="indefinite"/></circle>')
        b += T(560, y+2, str(v), 18, GOLDL, "end", "bold")
        y += 50
    prof = [("Role", "ML Engineer"), ("University", "VIT Chennai"), ("Degree", "B.Tech CSE (AI & ML)"),
            ("Graduating", "2028"), ("Focus", "ML · GenAI · MLOps"), ("Clubs", "MS Innovations, AI, Open Source")]
    y = 108
    for k, v in prof:
        b += T(660, y, k, 16, CREAM)
        b += T(950, y, v, 16 if len(v) < 22 else 13, GOLDL, "end", "bold")
        y += 44
    b += f'<polygon points="805,420 815,430 805,440 795,430" fill="{GOLDL}"><animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/></polygon>'
    b += f'<line x1="660" y1="430" x2="785" y2="430" stroke="{GOLD}" stroke-opacity="0.6"/><line x1="825" y1="430" x2="950" y2="430" stroke="{GOLD}" stroke-opacity="0.6"/>'
    save("skills.svg", svg(w, h, b))
skills()

# ------------------------------------------------------------------ journey map
def catmull(pts):
    d = f"M{pts[0][0]} {pts[0][1]}"
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P)-2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        c1 = (p1[0] + (p2[0]-p0[0])/6, p1[1] + (p2[1]-p0[1])/6)
        c2 = (p2[0] - (p3[0]-p1[0])/6, p2[1] - (p3[1]-p1[1])/6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]} {p2[1]}"
    return d

def journey():
    w, h = 1000, 560
    nodes = [  # x, y, title, sub, label position
        (150, 440, "Foundations", "Python · C · C++ · Java · SQL", "below"),
        (250, 335, "Data & ML", "NumPy · Pandas · Scikit-Learn · PySpark", "above"),
        (385, 425, "Deep Learning", "PyTorch · TensorFlow", "below"),
        (500, 305, "GenAI", "LLMs · RAG · LangChain · Whisper", "rightbelow"),
        (630, 215, "Backend & UI", "FastAPI · React", "leftabove"),
        (790, 160, "MLOps", "Docker · Kubernetes · MLflow · Airflow · Terraform", "above"),
        (885, 275, "Observability", "Prometheus · Grafana", "belowright"),
    ]
    tree = (690, 380)
    b = f'<defs></defs><rect width="{w}" height="{h}" fill="#0d0a06"/>'
    b += '<rect width="1000" height="560" fill="url(#bg)" opacity="0.7"/>'
    b += frame(w, h)
    b += T(500, 52, "FROM FIRST SCRIPT TO PRODUCTION", 13, GOLD, "middle", spacing=6)
    b += '<ellipse cx="170" cy="430" rx="150" ry="90" fill="#6c9a4a" opacity="0.10"/>'
    b += '<ellipse cx="500" cy="420" rx="150" ry="90" fill="#b5301f" opacity="0.10"/>'
    b += '<ellipse cx="800" cy="170" rx="150" ry="90" fill="#9fc4e8" opacity="0.10"/>'
    b += (f'<ellipse cx="{tree[0]}" cy="{tree[1]}" rx="190" ry="140" fill="url(#gl)" opacity="0.28">'
          '<animate attributeName="opacity" values="0.15;0.4;0.15" dur="6s" repeatCount="indefinite"/></ellipse>')
    b += ('<path d="M90 400 C70 330 110 250 190 230 C230 160 330 120 420 140 C470 90 570 80 640 110 C720 70 840 80 890 150 '
          'C940 220 940 300 900 340 C910 400 850 470 770 480 C700 530 560 530 480 500 C400 530 280 520 220 480 C150 490 100 460 90 400 Z" '
          f'fill="#17110a" fill-opacity="0.85" stroke="{GOLD}" stroke-opacity="0.7" stroke-width="2"/>')
    b += ('<path d="M110 395 C95 335 128 265 200 248 C238 185 335 140 420 160 C476 112 570 104 636 130 C716 92 826 100 870 160 '
          'C914 224 918 296 882 330 C890 386 838 450 764 460 C698 506 566 506 482 478 C402 506 290 498 226 460 C158 470 118 446 110 395 Z" '
          f'fill="none" stroke="{GOLD}" stroke-opacity="0.2" stroke-dasharray="2 6"/>')
    b += f'<g stroke="{GOLD}" stroke-opacity="0.35" fill="none" stroke-width="1.2"><path d="M905 200 l14 -22 l14 22 M928 208 l12 -18 l12 18 M860 205 l12 -18 l12 18"/></g>'
    pts = [(n[0], n[1]) for n in nodes] + [tree]
    b += (f'<path d="{catmull(pts)}" fill="none" stroke="{GOLDL}" stroke-opacity="0.85" stroke-width="2" stroke-dasharray="7 9" stroke-linecap="round">'
          '<animate attributeName="stroke-dashoffset" from="0" to="-64" dur="3s" repeatCount="indefinite"/></path>')
    # tree
    tx, ty = tree
    b += (f'<g transform="translate({tx},{ty})"><circle r="46" fill="url(#gl)"><animate attributeName="r" values="40;54;40" dur="5s" repeatCount="indefinite"/></circle>'
          f'<g stroke="{GOLDL}" fill="none" stroke-linecap="round"><path d="M0 18 C0 4 0 -6 0 -18" stroke-width="3"/>'
          '<path d="M0 6 C-10 2 -18 -4 -22 -14 M0 6 C10 2 18 -4 22 -14 M0 -6 C-6 -12 -10 -20 -12 -28 M0 -6 C6 -12 10 -20 12 -28 M0 -18 L0 -34" stroke-width="2"/></g></g>')
    b += T(tx, ty+52, "Production", 17, GOLDL, "middle", "bold", spacing=1)
    b += T(tx, ty+70, "reliable, monitored ML systems", 12.5, GRAY, "middle", style="italic")
    for i, (x, y, t, s, pos) in enumerate(nodes):
        b += (f'<g transform="translate({x},{y})"><circle r="16" fill="url(#gl)"><animate attributeName="opacity" values="0.5;1;0.5" '
              f'dur="{3+i*0.2:.1f}s" repeatCount="indefinite"/></circle><polygon points="0,-7 6,0 0,7 -6,0" fill="#fff3c9"/></g>')
        anc, lx = "middle", x
        if pos == "above": ty1, ty2 = y-34, y-17
        elif pos == "below": ty1, ty2 = y+34, y+51
        elif pos == "leftabove": ty1, ty2, anc, lx = y-26, y-9, "end", x-24
        elif pos == "rightbelow": ty1, ty2, anc, lx = y+8, y+25, "start", x+28
        else: ty1, ty2, anc, lx = y+46, y+63, "end", 958
        b += T(lx, ty1, t, 17, GOLDL, anc, "bold", spacing=1)
        b += T(lx, ty2, s, 12.5, GRAY, anc, style="italic")
    b += (f'<g transform="translate(92,92)" stroke="{GOLD}" fill="none" stroke-opacity="0.8"><circle r="26" stroke-opacity="0.4"/>'
          f'<path d="M0 -34 L5 0 L0 34 L-5 0 Z" fill="{GOLD}" fill-opacity="0.25"/><path d="M-34 0 L0 -5 L34 0 L0 5 Z" fill="{GOLD}" fill-opacity="0.15"/></g>')
    rd = catmull(pts)
    b += (f'<g><circle r="11" fill="url(#gl)"><animateMotion dur="18s" repeatCount="indefinite" path="{rd}"/></circle>'
          f'<circle r="3.6" fill="#fff6d8"><animateMotion dur="18s" repeatCount="indefinite" path="{rd}"/></circle></g>')
    random.seed(5)
    for i in range(22):
        ex = 130 + random.random()*760; r = 0.9 + random.random()*1.8; d = 6 + random.random()*8; bg = -random.random()*d
        b += (f'<circle cx="{ex:.0f}" cy="520" r="{r:.1f}" fill="#ffd980"><animate attributeName="cy" values="520;80" dur="{d:.1f}s" begin="{bg:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;0.6;0" dur="{d:.1f}s" begin="{bg:.1f}s" repeatCount="indefinite"/></circle>')
    save("map.svg", svg(w, h, b, bg=False))
journey()

# ------------------------------------------------------------------ tech stack
def tech():
    groups = [
        ("Programming", [("Python","python"),("SQL",None),("C","c"),("C++","cplusplus"),("Java","openjdk"),("JavaScript","javascript"),("HTML","html5"),("CSS","css3")]),
        ("ML & Big Data", [("PyTorch","pytorch"),("TensorFlow","tensorflow"),("Scikit-Learn","scikitlearn"),("PySpark","apachespark"),("Spark MLlib","apachespark"),("NumPy","numpy"),("Pandas","pandas"),("SHAP",None)]),
        ("AI / GenAI", [("LLMs",None),("RAG",None),("ChromaDB",None),("Sentence Transformers",None),("LangChain","langchain"),("Whisper","openai"),("Llama","meta")]),
        ("MLOps & DevOps", [("MLflow","mlflow"),("Docker","docker"),("Kubernetes","kubernetes"),("Airflow","apacheairflow"),("Terraform","terraform"),("Git","git"),("NGINX","nginx")]),
        ("Data & Streaming", [("Kafka","apachekafka"),("PostgreSQL","postgresql"),("MySQL","mysql"),("SQLite","sqlite"),("AWS S3","amazons3")]),
        ("Backend & Monitoring", [("FastAPI","fastapi"),("React","react"),("Prometheus","prometheus"),("Grafana","grafana"),("Hugging Face","huggingface")]),
    ]
    mono = {"SQL":"SQL","SHAP":"SHAP","LLMs":"LLM","RAG":"RAG","ChromaDB":"CDB","Sentence Transformers":"ST"}
    TW, TH, GAP = 86, 92, 8
    top, w = 44, 1000
    rowh = TH + 14
    h = top + len(groups)*rowh + 26
    b = frame(w, h)
    y = top
    for gi, (gname, items) in enumerate(groups):
        # label column
        lines = gname.replace(" & ", " &|").replace(" / ", " /|").split("|")
        ly = y + TH/2 - (len(lines)-1)*10 + 5
        for l in lines:
            b += T(50, ly, l.strip(), 15, GOLD, spacing=2); ly += 20
        b += f'<line x1="200" y1="{y}" x2="200" y2="{y+TH}" stroke="{GOLD}" stroke-opacity="0.35"/>'
        x = 218
        for ti, (name, key) in enumerate(items):
            c = TW/2
            b += (f'<polygon points="{x+8},{y} {x+TW-8},{y} {x+TW},{y+8} {x+TW},{y+TH-8} {x+TW-8},{y+TH} {x+8},{y+TH} {x},{y+TH-8} {x},{y+8}" '
                  f'fill="#14100a" stroke="{GOLD}" stroke-opacity="0.4"><animate attributeName="stroke-opacity" values="0.3;0.95;0.3" dur="5s" begin="{gi*0.5+ti*0.22:.2f}s" repeatCount="indefinite"/></polygon>')
            b += f'<ellipse cx="{x+c}" cy="{y+34}" rx="26" ry="22" fill="url(#gl)" opacity="0.10"><animate attributeName="opacity" values="0.05;0.3;0.05" dur="5s" begin="{gi*0.5+ti*0.22:.2f}s" repeatCount="indefinite"/></ellipse>'
            if key and ICONS.get(key):
                b += f'<g transform="translate({x+c-15},{y+14}) scale(1.25)" fill="#e6c06a"><path d="{ICONS[key]}"/></g>'
            else:
                b += T(x+c, y+42, mono.get(name, name[:3].upper()), 17, "#e6c06a", "middle", "bold", spacing=1)
            if len(name) > 11 and " " in name:
                a, bb = name.split(" ", 1)
                b += T(x+c, y+70, a, 11.5, CREAM, "middle") + T(x+c, y+83, bb, 11.5, CREAM, "middle")
            else:
                b += T(x+c, y+76, name, 12 if len(name) < 12 else 11, CREAM, "middle")
            x += TW + GAP
        y += rowh
    b += (f'<clipPath id="tp"><rect x="20" y="30" width="{w-40}" height="{h-60}"/></clipPath><g clip-path="url(#tp)"><rect x="-200" y="30" width="150" height="{h-60}" fill="url(#sweep)" transform="skewX(-18)">'
          '<animate attributeName="x" values="-200;1100;1100" keyTimes="0;0.55;1" dur="9s" repeatCount="indefinite"/></rect></g>')
    save("tech.svg", svg(w, h, b))
tech()

# ------------------------------------------------------------------ projects
def glyph(kind):
    g = f'<g stroke="{GOLDL}" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    if kind == "pulse":      # a heartbeat trace with a pulse running along it
        pl = "-34,0 -18,0 -10,-22 2,24 12,-12 20,0 34,0"
        g += f'<polyline points="{pl}" stroke-opacity="0.3"/>'
        g += (f'<polyline points="{pl}" pathLength="100" stroke-dasharray="22 78" stroke="#fff6d8" stroke-width="2.8">'
              '<animate attributeName="stroke-dashoffset" values="22;-100" dur="2.4s" repeatCount="indefinite"/></polyline>')
    elif kind == "wheel":    # a steering wheel turning left and right
        g += ('<g><animateTransform attributeName="transform" type="rotate" values="-28;28;-28" dur="5s" repeatCount="indefinite"/>'
              '<circle r="26"/><circle r="6"/><line x1="-26" y1="0" x2="-6" y2="0"/><line x1="6" y1="0" x2="26" y2="0"/><line x1="0" y1="6" x2="0" y2="26"/></g>')
    elif kind == "wave":     # audio bars dancing
        for i, hh in enumerate([8, 18, 30, 14, 36, 22, 10, 26, 12]):
            x = -32 + i*8
            g += (f'<g><animateTransform attributeName="transform" type="scale" values="1 0.35;1 1;1 0.35" dur="{1.1+i*0.13:.2f}s" begin="{i*0.12:.2f}s" repeatCount="indefinite"/>'
                  f'<line x1="{x}" y1="{-hh/2}" x2="{x}" y2="{hh/2}"/></g>')
    elif kind == "bars":     # a bar chart that grows over and over
        g += '<line x1="-30" y1="26" x2="30" y2="26"/>'
        for i, (x, hh) in enumerate([(-26, 22), (-5, 38), (16, 52)]):
            g += (f'<rect x="{x}" y="{26-hh}" width="10" height="{hh}"><animate attributeName="height" values="0;{hh};{hh};0" keyTimes="0;0.4;0.85;1" dur="4s" begin="{i*0.35:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="y" values="26;{26-hh};{26-hh};26" keyTimes="0;0.4;0.85;1" dur="4s" begin="{i*0.35:.2f}s" repeatCount="indefinite"/></rect>')
    elif kind == "eye":      # an eye scanning left and right
        g += '<path d="M-36 0 C-18 -24 18 -24 36 0 C18 24 -18 24 -36 0 Z"/>'
        g += ('<g><animateTransform attributeName="transform" type="translate" values="-9 0;9 0;-9 0" dur="4.5s" repeatCount="indefinite"/>'
              f'<circle r="9"/><circle r="2.5" fill="{GOLDL}"><animate attributeName="r" values="2;4;2" dur="2s" repeatCount="indefinite"/></circle></g>')
    return g + "</g>"

def project(idx, title, sub, bullets, stats, chips, kind):
    w = 1000
    # layout measures
    y = 112
    body = ""
    for bl in bullets:
        lines = textwrap.wrap(bl, 74)
        body += f'<polygon points="182,{y-9} 187,{y-4} 182,{y+1} 177,{y-4}" fill="{GOLD}"/>'
        for ln in lines:
            body += T(196, y, ln, 14, CREAM); y += 20
        y += 6
    chip_svg, cx, cy = "", 180, y + 12
    for c in chips:
        cw = len(c)*6.6 + 20
        if cx + cw > 968:
            cx = 180; cy += 30
        chip_svg += (f'<rect x="{cx}" y="{cy-15}" width="{cw}" height="22" rx="3" fill="#1a1409" stroke="{GOLD}" stroke-opacity="0.45"/>'
                     + T(cx+cw/2, cy, c, 11.5, GOLDL, "middle"))
        cx += cw + 8
    h = (cy + 30) if chips else (y + 24)
    h = max(h, 190)
    b = frame(w, h)
    b += f'<ellipse cx="95" cy="{h/2}" rx="90" ry="110" fill="url(#gl)" opacity="0.16"><animate attributeName="opacity" values="0.08;0.24;0.08" dur="6s" repeatCount="indefinite"/></ellipse>'
    gy = h/2
    b += (f'<polygon points="95,{gy-62} 147,{gy} 95,{gy+62} 43,{gy}" fill="#120e08" stroke="{GOLD}" stroke-opacity="0.7" stroke-width="1.5"/>'
          f'<polygon points="95,{gy-52} 137,{gy} 95,{gy+52} 53,{gy}" fill="none" stroke="{GOLD}" stroke-opacity="0.3"/>'
          f'<g transform="translate(95,{gy})">{glyph(kind)}</g>')
    b += T(180, 52, title, 25, "url(#gold)", weight="bold", spacing=1)
    b += T(180, 76, sub, 14, GRAY, style="italic")
    b += f'<line x1="180" y1="86" x2="780" y2="86" stroke="url(#fade)"/>'
    b += body + chip_svg
    sy = 66
    for big, lab in stats:
        b += T(968, sy, big, 27, GOLDL, "end", "bold")
        b += T(968, sy+18, lab, 11.5, GRAY, "end", style="italic")
        sy += 54
    b += (f'<clipPath id="pc"><rect x="20" y="20" width="{w-40}" height="{h-40}"/></clipPath><g clip-path="url(#pc)"><rect x="-200" y="20" width="140" height="{h-40}" fill="url(#sweep)" transform="skewX(-18)">'
          f'<animate attributeName="x" values="-200;1100;1100" keyTimes="0;0.5;1" dur="{9+idx}s" begin="{idx*1.3:.1f}s" repeatCount="indefinite"/></rect></g>')
    save(f"project_{idx}.svg", svg(w, h, b))

project(1, "Connected Fleet Telemetry", "Predictive maintenance and real-time ML platform",
        ["Distributed PySpark pipeline over 876,000 telemetry rows from 5 vehicle datasets, with rolling 3h/24h sensor features.",
         "Spark MLlib Random Forest trained on a chronological split to prevent leakage, served through FastAPI with SHAP explainability.",
         "FleetGuard React dashboard, Airflow retraining, Terraform on AWS and Kubernetes, Prometheus and Grafana monitoring."],
        [("0.97", "AUC-ROC"), ("89.6%", "failure recall"), ("876K", "rows processed")],
        ["PySpark","Kafka","FastAPI","PostgreSQL","MLflow","Docker","Kubernetes","Airflow","Terraform","Prometheus","Grafana","React","SHAP","AWS"], "pulse")

project(2, "End-to-End Autonomous Steering", "Behavioral cloning with a CNN",
        ["NVIDIA-style CNN in PyTorch that predicts continuous steering angles from monocular road images.",
         "Cropping, YUV conversion, blur and normalization, plus flip, brightness and translation augmentation.",
         "Offline inference with steering-vector overlay and temporal smoothing, evaluated on a chronological train/val/test split."],
        [("CNN", "image to steering angle"), ("Temporal", "smoothed inference")],
        ["PyTorch","OpenCV","NumPy","Matplotlib"], "wheel")

project(3, "AutoNotes-Pro", "Lecture audio to notes, quizzes and resources",
        ["Transcribes 1h+ lectures and generates structured notes, quizzes and curated resources with Llama 3.1.",
         "RAG pipeline on ChromaDB and Sentence Transformers for context-grounded Q&A with less hallucination.",
         "Audio chunking and CPU/GPU isolation for stable on-device inference, exposed over a FastAPI REST API with PDF export."],
        [("1h+", "lecture audio"), ("RAG", "grounded Q&A"), ("PDF", "notes and quizzes")],
        ["FastAPI","Llama 3.1","Whisper","ChromaDB","Sentence Transformers","FPDF"], "wave")

project(4, "CineScope", "Movie sentiment analysis platform",
        ["CNN and LSTM sentiment classifiers trained on 50K IMDb reviews; best model deployed with FastAPI.",
         "Hugging Face bert-base-uncased tokenization, weighted loss for class imbalance, systematic hyperparameter tuning.",
         "MLflow experiment tracking, Prometheus and Grafana monitoring, PostgreSQL storage, one-command Docker Compose deployment."],
        [("89.5%", "CNN accuracy"), ("88.5%", "LSTM accuracy"), ("50K", "IMDb reviews")],
        ["PyTorch","FastAPI","PostgreSQL","Docker","Prometheus","Grafana","MLflow","Hugging Face"], "bars")

project(5, "Counterfactual Vision Auditor", "Auditing shortcut learning in image classifiers",
        ["Reproducible tool that checks whether classifiers rely on background context instead of the foreground object, using the Waterbirds benchmark.",
         "Background modification flips predictions about 47% of the time, while suppressing the actual bird flips only about 9%.",
         "Compares intervention-derived audit scores (flip rate, JSD) against per-group error under distribution shift; 46 unit and smoke tests."],
        [("47%", "background flip rate"), ("~9%", "foreground flip rate"), ("24.5%", "worst-group accuracy")],
        ["PyTorch","ResNet-18","DeepLabV3","Waterbirds","Counterfactuals","JSD"], "eye")

# ------------------------------------------------------------------ experience
def experience():
    w = 1000
    entries = [
        ("Full-Stack Engineer Intern", "Sona BLW Precision Forgings Ltd. (Comstar Automotive)", "May 2026 – Jun 2026",
         ["Built a React and Express.js product database portal with interactive dashboards for automotive motor spec analysis.",
          "Migrated a legacy PHP backend to a RESTful API with optimized SQL; ran an OWASP VAPT and shipped critical security patches.",
          "Filterable data-table views across 500+ product entries cut manual lookup time by about 70%."]),
        ("Machine Learning Team Member", "Microsoft Innovations Club, VIT Chennai", "Oct 2025 – Present",
         ["Developed ML solutions for inter-college technical competitions."]),
        ("Technical Team Member", "Artificial Intelligence Club, VIT Chennai", "Feb 2025 – Present",
         ["Organized hackathons for students.",
          "Built technical solutions for competitions."]),
        ("Technical Team Member", "Open Source Programming Club, VIT Chennai", "",
         ["Built a hackathon teammate-finding portal in modern React where VIT students find teammates through listed skills, resumes and more.",
          "Contribute to open source repositories.",
          "Organize technical events."]),
    ]
    body, y = "", 62
    ys = []
    for role, org, date, bl in entries:
        ys.append(y)
        body += (f'<polygon points="62,{y-14} 70,{y-6} 62,{y+2} 54,{y-6}" fill="{GOLDL}"><animate attributeName="opacity" values="0.55;1;0.55" dur="3s" begin="{len(ys)*0.6:.1f}s" repeatCount="indefinite"/></polygon>'
                 f'<circle cx="62" cy="{y-6}" r="4" fill="none" stroke="{GOLDL}"><animate attributeName="r" values="4;16" dur="3s" begin="{len(ys)*0.6:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0" dur="3s" begin="{len(ys)*0.6:.1f}s" repeatCount="indefinite"/></circle>')
        body += T(90, y, role, 20, "url(#gold)", weight="bold", spacing=1)
        if date: body += T(950, y, date, 14, GOLD, "end", style="italic")
        body += T(90, y+24, org, 15, CREAM)
        yy = y + 52
        for t in bl:
            for i, ln in enumerate(textwrap.wrap(t, 112)):
                if i == 0:
                    body += f'<polygon points="94,{yy-8} 98,{yy-4} 94,{yy} 90,{yy-4}" fill="{GOLD}"/>'
                body += T(108, yy, ln, 14, CREAM); yy += 20
            yy += 4
        y = yy + 22 if bl else y + 66
    h = y + 6
    b = frame(w, h) + f'<line x1="62" y1="{ys[0]}" x2="62" y2="{ys[-1]}" stroke="{GOLD}" stroke-opacity="0.5" stroke-dasharray="3 5"><animate attributeName="stroke-dashoffset" from="0" to="-16" dur="1.2s" repeatCount="indefinite"/></line>' + body
    save("experience.svg", svg(w, h, b))
experience()

def education():
    w, h = 1000, 170
    b = frame(w, h)
    rows = [("Vellore Institute of Technology, Chennai", "B.Tech Computer Science with AI & ML", "2024 – Expected 2028"),
            ("Bala Vidya Mandir, Adyar", "Computer Science (Class XII)", "2014 – 2024")]
    y = 62
    for name, deg, date in rows:
        b += (f'<polygon points="62,{y-14} 70,{y-6} 62,{y+2} 54,{y-6}" fill="{GOLDL}"><animate attributeName="opacity" values="0.55;1;0.55" dur="3s" begin="{y/100:.1f}s" repeatCount="indefinite"/></polygon>'
              f'<circle cx="62" cy="{y-6}" r="4" fill="none" stroke="{GOLDL}"><animate attributeName="r" values="4;16" dur="3s" begin="{y/100:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0" dur="3s" begin="{y/100:.1f}s" repeatCount="indefinite"/></circle>')
        b += T(90, y, name, 19, "url(#gold)", weight="bold", spacing=1)
        b += T(950, y, date, 14, GOLD, "end", style="italic")
        b += T(90, y+24, deg, 15, CREAM)
        y += 66
    save("education.svg", svg(w, h, b))
education()

# ------------------------------------------------------------------ link buttons
def button(slug, label, key):
    w, h = 220, 56
    b = (f'<polygon points="10,1 210,1 219,10 219,46 210,55 10,55 1,46 1,10" fill="#14100a" stroke="{GOLD}" stroke-opacity="0.7" stroke-width="1.5"/>'
         f'<polygon points="12,5 208,5 215,12 215,44 208,51 12,51 5,44 5,12" fill="none" stroke="{GOLD}" stroke-opacity="0.25"/>')
    b += (f'<rect x="3" y="3" width="214" height="50" rx="8" fill="none" stroke="#fff3c9" stroke-width="2" pathLength="100" stroke-dasharray="9 91">'
          '<animate attributeName="stroke-dashoffset" from="0" to="-100" dur="3.6s" repeatCount="indefinite"/></rect>')
    if ICONS.get(key):
        b += f'<g transform="translate(26,15) scale(1.1)" fill="#e6c06a"><path d="{ICONS[key]}"/><animate attributeName="opacity" values="0.65;1;0.65" dur="2.8s" repeatCount="indefinite"/></g>'
    b += T(122, 34, label, 17, GOLDL, "middle", "bold", spacing=1)
    save(f"btn_{slug}.svg", svg(w, h, b, bg=False))
for slug, label, key in [("github", "GitHub", "github"), ("linkedin", "LinkedIn", "linkedin"), ("leetcode", "LeetCode", "leetcode"), ("hackerrank", "HackerRank", "hackerrank")]:
    button(slug, label, key)

# ------------------------------------------------------------------ banner (original swordsman silhouette)
import random
def banner():
    random.seed(11)
    w, h = 1000, 320
    b = frame(w, h)
    b += ('<defs><linearGradient id="fadeb" gradientUnits="userSpaceOnUse" x1="0" y1="268" x2="0" y2="312"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
          '<mask id="mb" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="320"><rect width="1000" height="320" fill="url(#fadeb)"/></mask></defs>')
    b += '<ellipse cx="850" cy="185" rx="250" ry="175" fill="url(#gl)" opacity="0.45"><animate attributeName="opacity" values="0.3;0.6;0.3" dur="6s" repeatCount="indefinite"/></ellipse>'
    # rising golden specks
    for i in range(22):
        x = 560 + random.random()*430; r = 0.9 + random.random()*2.0
        d = 5 + random.random()*7; bg = -random.random()*d; x2 = x + (random.random()-0.5)*40
        b += (f'<circle cx="{x:.0f}" cy="312" r="{r:.1f}" fill="#ffd980"><animate attributeName="cy" values="312;30" dur="{d:.1f}s" begin="{bg:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="cx" values="{x:.0f};{x2:.0f}" dur="{d:.1f}s" begin="{bg:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;0.85;0" dur="{d:.1f}s" begin="{bg:.1f}s" repeatCount="indefinite"/></circle>')
    # drifting blossom petals
    PET = "M0,0 C3,-5 9,-3 8,3 C6,8 -1,7 0,0 Z"
    for i in range(16):
        x0 = 520 + random.random()*480; dur = 7 + random.random()*6; bg = -random.random()*dur
        col = random.choice(["#e8845a", "#f2a98a", "#d2622a", "#f6c4ae"]); sc = 0.8 + random.random()*0.9
        dx = -60 - random.random()*120
        path = f"M{x0:.0f},-12 C{x0+40:.0f},70 {x0+dx-50:.0f},150 {x0+dx*0.6:.0f},215 S{x0+dx:.0f},300 {x0+dx*1.2:.0f},335"
        b += (f'<g><animateMotion dur="{dur:.1f}s" begin="{bg:.1f}s" repeatCount="indefinite" path="{path}"/>'
              f'<g transform="scale({sc:.2f})"><path d="{PET}" fill="{col}"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="{3+random.random()*3:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;0.9;0.9;0" keyTimes="0;0.1;0.85;1" dur="{dur:.1f}s" begin="{bg:.1f}s" repeatCount="indefinite"/></path></g></g>')
    # the samurai: slides in from the left with a fade, then breathes
    b += ('<g mask="url(#mb)"><g transform="translate(566,-72) scale(0.76)">'
          '<g><animateTransform attributeName="transform" type="translate" from="-640 0" to="0 0" dur="1.6s" begin="0s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.16 1 0.3 1"/>'
          '<animate attributeName="opacity" values="0;0.25;1" keyTimes="0;0.45;1" dur="1.4s" begin="0s" fill="freeze"/>'
          f'{samurai_drawing()}</g></g></g>')
    # text
    b += T(60, 78, "— MACHINE LEARNING ENGINEER —", 15, GOLD, spacing=6)
    b += T(60, 152, "JAYASHURIYA", 66, "url(#gold)", weight="bold", spacing=7)
    b += f'<line x1="62" y1="176" x2="560" y2="176" stroke="url(#gold)" stroke-width="1.5"/><polygon points="311,170 317,176 311,182 305,176" fill="{GOLDL}"/>'
    b += T(60, 214, "DEEP LEARNING  ·  GENAI  ·  MLOPS", 20, CREAM, spacing=3)
    b += T(60, 256, "Building ML systems from data pipeline to production.", 17, GRAY, style="italic")
    save("banner.svg", svg(w, h, b))
banner()

# ------------------------------------------------------------------ footer text
f = open(f"{OUT}/footer.svg").read()
f = f.replace("REST AT THE GRACE", "THANKS FOR STOPPING BY").replace("May the gradients guide thee, Tarnished.", "Always happy to talk ML, MLOps and building things that ship.")
open(f"{OUT}/footer.svg", "w").write(f)
print("built")
