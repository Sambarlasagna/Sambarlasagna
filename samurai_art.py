"""Original samurai figure (SVG group) built from joints, so the pose is easy to tweak."""
import math

INK, GOLD, GOLDL, RED = "#0a0705", "#c8953a", "#ffe9a8", "#8f2b1d"

def _cap(p, q, w0, w1, fill=INK, rim=0.55, extra=""):
    dx, dy = q[0]-p[0], q[1]-p[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy/L, dx/L
    r0, r1 = w0/2, w1/2
    a = (p[0]+nx*r0, p[1]+ny*r0); b = (q[0]+nx*r1, q[1]+ny*r1)
    c = (q[0]-nx*r1, q[1]-ny*r1); d = (p[0]-nx*r0, p[1]-ny*r0)
    path = (f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f} A{r1},{r1} 0 0 1 {c[0]:.1f},{c[1]:.1f} "
            f"L{d[0]:.1f},{d[1]:.1f} A{r0},{r0} 0 0 1 {a[0]:.1f},{a[1]:.1f} Z")
    return f'<path d="{path}" fill="{fill}" stroke="{GOLDL}" stroke-opacity="{rim}" stroke-width="1" stroke-linejoin="round" {extra}/>'

def _poly(pts, fill=INK, rim=0.55, w=1.0, extra=""):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{s}" fill="{fill}" stroke="{GOLDL}" stroke-opacity="{rim}" stroke-width="{w}" stroke-linejoin="round" {extra}/>'

def _path(d, fill=INK, rim=0.55, w=1.0, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{GOLDL}" stroke-opacity="{rim}" stroke-width="{w}" stroke-linejoin="round" {extra}/>'

def _line(d, op=0.35, w=0.9, col=GOLD):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"/>'

def _stack(cx, cy, ang, w, h, n, taper=0.06, rim=0.6):
    out = f'<g transform="translate({cx},{cy}) rotate({ang})">'
    for i in range(n):
        ww = w * (1 - i * taper); y = i * h * 0.82
        out += _poly([(-ww/2, y), (ww/2, y), (ww/2*0.94, y+h), (-ww/2*0.94, y+h)], rim=rim)
        out += _line(f"M{-ww/2+3},{y+h*0.5} L{ww/2-3},{y+h*0.5}", 0.25)
    return out + "</g>"

def _arm(p, q, w0, w1, rim=0.7):
    """Filled tapered limb with outline only along its sides (no joint circles)."""
    dx, dy = q[0]-p[0], q[1]-p[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy/L, dx/L
    r0, r1 = w0/2, w1/2
    a = (p[0]+nx*r0, p[1]+ny*r0); b = (q[0]+nx*r1, q[1]+ny*r1)
    c = (q[0]-nx*r1, q[1]-ny*r1); d = (p[0]-nx*r0, p[1]-ny*r0)
    fill = (f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f} A{r1},{r1} 0 0 1 {c[0]:.1f},{c[1]:.1f} '
            f'L{d[0]:.1f},{d[1]:.1f} A{r0},{r0} 0 0 1 {a[0]:.1f},{a[1]:.1f} Z" fill="url(#skin)"/>')
    t0 = 0.38
    a2 = (a[0]+(b[0]-a[0])*t0, a[1]+(b[1]-a[1])*t0); d2 = (d[0]+(c[0]-d[0])*t0, d[1]+(c[1]-d[1])*t0)
    sides = (f'<path d="M{a2[0]:.1f},{a2[1]:.1f} L{b[0]:.1f},{b[1]:.1f} M{d2[0]:.1f},{d2[1]:.1f} L{c[0]:.1f},{c[1]:.1f}" '
             f'fill="none" stroke="{GOLDL}" stroke-opacity="{rim}" stroke-width="1" stroke-linecap="round"/>')
    return fill + sides

def _katana(hand, tip, glint_dur=3.4, glint_begin=0.0):
    ux, uy = tip[0]-hand[0], tip[1]-hand[1]; L = math.hypot(ux, uy); ux, uy = ux/L, uy/L
    nx, ny = -uy, ux
    pom = (hand[0]-ux*22, hand[1]-uy*22); gd = (hand[0]+ux*9, hand[1]+uy*9)
    out = _cap(pom, gd, 5.6, 5.6, "#1a120a", 0.6)
    for t in (3, 8, 13, 18):
        cx, cy = pom[0]+ux*t, pom[1]+uy*t
        out += f'<path d="M{cx-nx*3.2-ux*2:.1f},{cy-ny*3.2-uy*2:.1f} L{cx+nx*3.2+ux*2:.1f},{cy+ny*3.2+uy*2:.1f}" stroke="{GOLD}" stroke-opacity="0.55" stroke-width="0.8"/>'
    out += f'<circle cx="{pom[0]:.1f}" cy="{pom[1]:.1f}" r="3.4" fill="{GOLDL}"/>'
    bw = 3.4
    blade = [(gd[0]+nx*bw, gd[1]+ny*bw), (tip[0]+nx*0.6, tip[1]+ny*0.6), tip, (gd[0]-nx*bw, gd[1]-ny*bw)]
    out += _poly(blade, "url(#blade)", 0.9, 0.7)
    out += f'<line x1="{gd[0]+ux*4:.1f}" y1="{gd[1]+uy*4:.1f}" x2="{tip[0]-ux*6:.1f}" y2="{tip[1]-uy*6:.1f}" stroke="#fff6d8" stroke-opacity="0.8" stroke-width="0.8"/>'
    out += f'<g transform="translate({gd[0]:.1f},{gd[1]:.1f}) rotate({math.degrees(math.atan2(uy, ux)):.1f})"><ellipse rx="2.4" ry="9.5" fill="{INK}" stroke="{GOLDL}" stroke-width="1.1"/></g>'
    out += (f'<circle r="2.4" fill="#fff6d8"><animateMotion dur="{glint_dur}s" begin="{glint_begin}s" repeatCount="indefinite" path="M{gd[0]:.0f},{gd[1]:.0f} L{tip[0]:.0f},{tip[1]:.0f}"/>'
            f'<animate attributeName="opacity" values="0;1;0" dur="{glint_dur}s" begin="{glint_begin}s" repeatCount="indefinite"/></circle>')
    return out

def samurai():
    """Back view: bare muscular warrior, conical hat, topknot, two katanas held low and angled out."""
    g = []
    SK = "url(#skin)"
    g.append('<defs><linearGradient id="skin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0c0805"/><stop offset="0.5" stop-color="#22160c"/><stop offset="1" stop-color="#0c0805"/></linearGradient>'
             '<linearGradient id="cloth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14100c"/><stop offset="1" stop-color="#0a0806"/></linearGradient></defs>')
    def skin(d, rim=0.6, w=1.0):
        return f'<path d="{d}" fill="{SK}" stroke="{GOLDL}" stroke-opacity="{rim}" stroke-width="{w}" stroke-linejoin="round"/>'
    def cloth(d, rim=0.5, w=1.0, fill="url(#cloth)"):
        return f'<path d="{d}" fill="{fill}" stroke="{GOLDL}" stroke-opacity="{rim}" stroke-width="{w}" stroke-linejoin="round"/>'
    # ground haze
    g.append(f'<ellipse cx="0" cy="0" rx="86" ry="7" fill="{GOLD}" opacity="0.12"><animate attributeName="opacity" values="0.07;0.2;0.07" dur="4s" repeatCount="indefinite"/></ellipse>')

    # ---------------- trailing cloth strips + sash tails (behind the legs)
    st1 = "M-9,-100 C-12,-82 -9,-64 -14,-44 L-7,-42 C-3,-62 -3,-82 -3,-100 Z"
    st2 = "M-9,-100 C-8,-82 -14,-64 -10,-44 L-3,-46 C-6,-64 0,-82 -3,-100 Z"
    st3 = "M4,-100 C6,-80 12,-62 10,-38 L17,-38 C16,-62 12,-80 10,-100 Z"
    st4 = "M4,-100 C2,-80 6,-62 14,-40 L20,-44 C14,-62 14,-80 10,-100 Z"
    g.append(f'<path d="{st1}" fill="url(#cloth)" stroke="{GOLDL}" stroke-opacity="0.45" stroke-width="0.9"><animate attributeName="d" values="{st1};{st2};{st1}" dur="3.2s" repeatCount="indefinite"/></path>')
    g.append(f'<path d="{st3}" fill="url(#cloth)" stroke="{GOLDL}" stroke-opacity="0.45" stroke-width="0.9"><animate attributeName="d" values="{st3};{st4};{st3}" dur="2.8s" repeatCount="indefinite"/></path>')

    # ---------------- hakama (wide trousers) + feet
    g.append(cloth("M-25,-104 L25,-104 C31,-72 42,-38 47,-6 L12,-6 C8,-30 4,-46 0,-62 C-4,-46 -8,-30 -12,-6 L-47,-6 C-42,-38 -31,-72 -25,-104 Z", 0.55))
    g.append(_line("M-20,-96 C-26,-66 -34,-36 -39,-8 M-12,-96 C-16,-66 -20,-36 -24,-8 M12,-96 C16,-66 20,-36 24,-8 M20,-96 C26,-66 34,-36 39,-8 M0,-100 L0,-64", 0.22))
    g.append(f'<ellipse cx="-30" cy="-3" rx="17" ry="5.5" fill="{INK}" stroke="{GOLDL}" stroke-opacity="0.55"/><ellipse cx="30" cy="-3" rx="17" ry="5.5" fill="{INK}" stroke="{GOLDL}" stroke-opacity="0.55"/>')

    # ---------------- back and torso: strong V-taper (wide shoulders, narrow waist)
    TORSO = ("M-10,-168 C-24,-166 -40,-162 -52,-155 C-60,-150 -61,-142 -57,-136 C-53,-131 -49,-127 -47,-122 "
             "C-40,-113 -28,-106 -19,-100 L19,-100 C28,-106 40,-113 47,-122 C49,-127 53,-131 57,-136 "
             "C61,-142 60,-150 52,-155 C40,-162 24,-166 10,-168 Z")
    g.append(skin(TORSO, 0.8, 1.3))

    # arms (drawn before the shoulder muscles so the deltoids cap them)
    LS, LE, LH = (-53, -134), (-67, -114), (-71, -93)
    RS, RE, RH = (53, -134), (69, -116), (79, -96)
    g.append(_arm(LS, LE, 30, 22)); g.append(_arm(LE, LH, 22, 13)); g.append(f'<circle cx="{LE[0]}" cy="{LE[1]}" r="10.5" fill="url(#skin)"/>')
    g.append(_arm(RS, RE, 30, 22)); g.append(_arm(RE, RH, 22, 13)); g.append(f'<circle cx="{RE[0]}" cy="{RE[1]}" r="10.5" fill="url(#skin)"/>')
    g.append(_line("M-61,-130 C-66,-124 -68,-118 -67,-110 M-73,-126 C-75,-118 -75,-110 -73,-102", 0.3, 1))      # triceps / forearm
    g.append(_line("M61,-130 C67,-124 71,-118 69,-110 M75,-128 C77,-120 78,-112 76,-104", 0.3, 1))
    g.append(_line(f"M{LE[0]-8},{LE[1]+10} L{LE[0]+5},{LE[1]+12} M{RE[0]-6},{RE[1]+10} L{RE[0]+8},{RE[1]+12}", 0.45, 1.3))   # wrist wraps

    # each muscle group as its own shape (left side; mirrored for the right)
    def mus(d, op=0.14, edge=0.45):
        return (f'<path d="{d}" fill="#ffd980" fill-opacity="{op*1.35:.2f}" stroke="#050302" stroke-opacity="0.8" stroke-width="1.1" stroke-linejoin="round"/>'
                f'<path d="{d}" fill="none" stroke="{GOLDL}" stroke-opacity="{edge}" stroke-width="0.7"/>')
    left = [
        mus("M-8,-168 C-22,-165 -38,-160 -50,-154 C-36,-151 -18,-145 0,-135 L0,-168 Z", 0.12),                               # trapezius
        mus("M-46,-157 C-57,-157 -64,-148 -61,-138 C-58,-130 -50,-128 -46,-133 C-42,-141 -42,-151 -46,-157 Z", 0.18),        # rear deltoid
        mus("M-6,-146 C-18,-149 -32,-144 -37,-134 C-34,-124 -22,-120 -12,-124 C-8,-130 -6,-138 -6,-146 Z", 0.16),            # infraspinatus / scapula
        mus("M-41,-132 C-45,-128 -45,-122 -41,-120 C-35,-122 -31,-126 -31,-130 C-35,-134 -39,-134 -41,-132 Z", 0.18),        # teres major
        mus("M-46,-123 C-40,-112 -30,-106 -20,-101 C-14,-108 -12,-118 -12,-126 C-24,-120 -36,-117 -46,-123 Z", 0.13),        # latissimus (the wing)
        mus("M-3,-128 C-10,-120 -11,-108 -7,-101 L-3,-101 Z", 0.16),                                                          # erector spinae
        mus("M-23,-110 C-21,-106 -20,-103 -19,-101 L-27,-104 C-28,-107 -26,-109 -23,-110 Z", 0.14),                           # obliques
    ]
    for d in left:
        g.append(d)
        g.append(f'<g transform="scale(-1,1)">{d}</g>')
    g.append(f'<path d="M0,-167 L0,-101" stroke="#050302" stroke-opacity="0.8" stroke-width="2.2"/><path d="M0,-167 L0,-101" stroke="{GOLDL}" stroke-opacity="0.25" stroke-width="0.7"/>')
    g.append(_line("M-12,-100 C-6,-98 6,-98 12,-100", 0.3, 1))
    # rim light along the shoulders and lats (backlit)
    g.append(f'<path d="M-58,-146 C-50,-158 -28,-166 -9,-168 M58,-146 C50,-158 28,-166 9,-168" fill="none" stroke="#fff3c9" stroke-opacity="0.55" stroke-width="1.7" stroke-linecap="round"><animate attributeName="stroke-opacity" values="0.3;0.75;0.3" dur="4s" repeatCount="indefinite"/></path>')
    g.append(f'<path d="M-47,-122 C-40,-113 -28,-106 -19,-100 M47,-122 C40,-113 28,-106 19,-100" fill="none" stroke="#fff3c9" stroke-opacity="0.3" stroke-width="1.2" stroke-linecap="round"/>')

    # ---------------- katanas and hands
    g += [_katana(LH, (-130, -4), 3.6, 0.0), _katana(RH, (148, -6), 3.6, 1.4)]
    g.append(f'<circle cx="{LH[0]}" cy="{LH[1]}" r="7" fill="{SK}" stroke="{GOLDL}" stroke-opacity="0.7"/><circle cx="{RH[0]}" cy="{RH[1]}" r="7" fill="{SK}" stroke="{GOLDL}" stroke-opacity="0.7"/>')

    # ---------------- belt and red sash with knot
    g.append(_poly([(-25, -110), (25, -110), (25, -97), (-25, -97)], RED, 0.75))
    g.append(_line("M-20,-104 L20,-104", 0.35, 1))
    g.append(f'<ellipse cx="0" cy="-103" rx="7" ry="8" fill="{RED}" stroke="{GOLDL}" stroke-opacity="0.7"/>')
    r1 = "M-3,-96 C-8,-82 -6,-68 -12,-54 L-5,-52 C0,-66 0,-82 0,-96 Z"
    r2 = "M-3,-96 C-12,-84 -12,-70 -18,-56 L-10,-52 C-3,-66 0,-82 0,-96 Z"
    r3 = "M3,-96 C8,-84 12,-70 20,-58 L24,-64 C16,-76 10,-86 6,-96 Z"
    r4 = "M3,-96 C12,-86 20,-74 28,-66 L30,-72 C22,-80 12,-88 6,-96 Z"
    g.append(f'<path d="{r1}" fill="{RED}" stroke="{GOLDL}" stroke-opacity="0.6" stroke-width="0.9"><animate attributeName="d" values="{r1};{r2};{r1}" dur="2.6s" repeatCount="indefinite"/></path>')
    g.append(f'<path d="{r3}" fill="{RED}" stroke="{GOLDL}" stroke-opacity="0.6" stroke-width="0.9"><animate attributeName="d" values="{r3};{r4};{r3}" dur="2.2s" repeatCount="indefinite"/></path>')

    # ---------------- neck, hair, conical hat
    g.append(skin("M-8,-182 L8,-182 L10,-162 L-10,-162 Z", 0.5))
    g.append(f'<ellipse cx="0" cy="-176" rx="12" ry="11" fill="#07050a" stroke="{GOLDL}" stroke-opacity="0.5"/>')
    k1 = "M3,-184 C16,-186 24,-176 22,-160 C20,-170 14,-174 6,-172 Z"
    k2 = "M3,-184 C18,-184 28,-172 28,-156 C22,-168 14,-174 6,-172 Z"
    g.append(f'<path d="{k1}" fill="#07050a" stroke="{GOLDL}" stroke-opacity="0.55" stroke-width="0.9"><animate attributeName="d" values="{k1};{k2};{k1}" dur="3s" repeatCount="indefinite"/></path>')
    g.append(f'<g transform="rotate(-4 0 -184)">'
             f'<ellipse cx="0" cy="-186" rx="35" ry="6.5" fill="{INK}" stroke="{GOLDL}" stroke-opacity="0.8" stroke-width="1.1"/>'
             f'<path d="M-35,-186 L1,-224 L35,-186 Q0,-178 -35,-186 Z" fill="{INK}" stroke="{GOLDL}" stroke-opacity="0.85" stroke-width="1.2" stroke-linejoin="round"/>'
             f'<path d="M1,-224 L-24,-184 M1,-224 L-10,-180 M1,-224 L6,-180 M1,-224 L21,-184 M1,-224 L31,-187" stroke="{GOLD}" stroke-opacity="0.4" stroke-width="0.9" fill="none"/>'
             f'<path d="M-28,-194 Q1,-188 29,-194 M-18,-206 Q1,-201 19,-206" stroke="{GOLD}" stroke-opacity="0.35" stroke-width="0.9" fill="none"/>'
             f'<path d="M1,-224 L24,-190" stroke="#fff3c9" stroke-opacity="0.55" stroke-width="1.2"/></g>')
    return "".join(g)

if __name__ == "__main__":
    import sys
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-170 -245 340 262" width="1020" height="786">'
           f'<defs><linearGradient id="blade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff3c9"/><stop offset="1" stop-color="#b8862f"/></linearGradient></defs>'
           f'<rect x="-170" y="-245" width="340" height="262" fill="#2a2013"/><g>{samurai()}</g></svg>')
    open("/tmp/sam.svg", "w").write(svg)
