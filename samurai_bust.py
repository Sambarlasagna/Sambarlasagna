"""Samurai bust (head to hip), profile facing right, head bent, one hand on the tip of his conical hat,
katana sheathed at the hip. Local origin = hip centre; up is negative y."""
import math

INK, GOLD, GOLDL, RED, ORANGE, CREAM = "#0a0705", "#c8953a", "#ffe9a8", "#8f2b1d", "#d2622a", "#d9cfb4"

def P(d, fill="url(#steel)", rim=0.6, w=1.0, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{GOLDL}" stroke-opacity="{rim}" stroke-width="{w}" stroke-linejoin="round" {extra}/>'

def poly(pts, fill="url(#steel)", rim=0.6, w=1.0):
    return P("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z", fill, rim, w)

def line(d, col=GOLD, op=0.4, w=0.9):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"/>'

def limb(p, q, w0, w1, fill="url(#steel)", rim=0.65):
    dx, dy = q[0]-p[0], q[1]-p[1]; L = math.hypot(dx, dy) or 1
    nx, ny = -dy/L, dx/L; r0, r1 = w0/2, w1/2
    a = (p[0]+nx*r0, p[1]+ny*r0); b = (q[0]+nx*r1, q[1]+ny*r1); c = (q[0]-nx*r1, q[1]-ny*r1); d = (p[0]-nx*r0, p[1]-ny*r0)
    body = (f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f} A{r1},{r1} 0 0 1 {c[0]:.1f},{c[1]:.1f} L{d[0]:.1f},{d[1]:.1f} A{r0},{r0} 0 0 1 {a[0]:.1f},{a[1]:.1f} Z" fill="{fill}"/>')
    t = 0.12
    sides = (f'<path d="M{a[0]+(b[0]-a[0])*t:.1f},{a[1]+(b[1]-a[1])*t:.1f} L{b[0]:.1f},{b[1]:.1f} M{d[0]+(c[0]-d[0])*t:.1f},{d[1]+(c[1]-d[1])*t:.1f} L{c[0]:.1f},{c[1]:.1f}" '
             f'fill="none" stroke="{GOLDL}" stroke-opacity="{rim}" stroke-width="1" stroke-linecap="round"/>')
    return body + sides

def lamellar(rows, front, back):
    """horizontal armour bands between a back contour and a front contour"""
    out = ""
    for (y0, y1) in rows:
        pts = [(back(y0), y0), (front(y0), y0), (front(y1), y1), (back(y1), y1)]
        out += poly(pts, rim=0.5, w=0.9)
        xs = [back(y1) + (front(y1) - back(y1)) * f for f in (0.12, 0.3, 0.5, 0.7, 0.88)]
        out += f'<path d="M{back(y1)+3:.1f},{y1-1.2:.1f} L{front(y1)-3:.1f},{y1-1.2:.1f}" stroke="{ORANGE}" stroke-opacity="0.85" stroke-width="2.1" stroke-dasharray="2.2 2.2"/>'
    return out

def sode(cx, cy, ang, w, h, n):
    out = f'<g transform="translate({cx},{cy}) rotate({ang})">'
    ph = h / n
    for i in range(n):
        y = i * ph * 0.92; top = w * (0.8 + 0.2 * i / max(1, n-1)); bot = w * (0.84 + 0.2 * (i+1) / n)
        out += poly([(-top/2, y), (top/2, y), (bot/2, y+ph), (-bot/2, y+ph)], rim=0.65, w=1)
        for xf in (-0.36, -0.12, 0.12, 0.36):
            out += f'<path d="M{bot*xf:.1f},{y+1:.1f} L{bot*xf*1.04:.1f},{y+ph-1:.1f}" stroke="{ORANGE}" stroke-opacity="0.55" stroke-width="1.1"/>'
        out += f'<path d="M{-bot/2+1:.1f},{y+ph-3.2:.1f} L{bot/2-1:.1f},{y+ph-3.2:.1f}" stroke="{ORANGE}" stroke-opacity="0.9" stroke-width="2.4"/>'
    # orange hem on the lowest plate, like the reference
    out += poly([(-w*0.52, h*0.88), (w*0.52, h*0.88), (w*0.54, h+3), (-w*0.54, h+3)], fill=ORANGE, rim=0.7)
    out += f'<path d="M{-w*0.45:.1f},{h*0.95:.1f} L{w*0.45:.1f},{h*0.95:.1f}" stroke="#fff3c9" stroke-opacity="0.45" stroke-width="1" stroke-dasharray="2 3"/>'
    return out + "</g>"

def samurai_bust():
    g = []
    g.append('<defs><linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a231b"/><stop offset="1" stop-color="#0e0b08"/></linearGradient>'
             '<linearGradient id="skinp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a1b11"/><stop offset="1" stop-color="#5a402b"/></linearGradient></defs>')

    # ============ everything below breathes together (pivot = the hip at 0,0)
    body = []
    # --- scarf tail fluttering behind the neck
    s1 = "M0,-128 C-20,-130 -38,-122 -58,-132 L-56,-118 C-40,-110 -22,-116 0,-114 Z"
    s2 = "M0,-128 C-20,-122 -40,-134 -62,-124 L-60,-112 C-42,-120 -22,-108 0,-114 Z"
    body.append(f'<path d="{s1}" fill="{RED}" stroke="{GOLDL}" stroke-opacity="0.6" stroke-width="1"><animate attributeName="d" values="{s1};{s2};{s1}" dur="3s" repeatCount="indefinite"/></path>')

    # --- raised far arm, partly behind the hat (it ends at the hat tip)
    body.append(limb((2, -126), (-14, -160), 19, 15))
    body.append(limb((-14, -160), (20, -196), 15, 11))

    # --- torso (do), belt and skirt plates
    front = lambda y: [(-130, 20), (-112, 25), (-96, 31), (-80, 33), (-60, 30), (-36, 25), (-14, 22), (6, 21)]
    def interp(tbl):
        def f(y):
            for (y0, v0), (y1, v1) in zip(tbl, tbl[1:]):
                if y0 <= y <= y1: return v0 + (v1 - v0) * (y - y0) / (y1 - y0)
            return tbl[-1][1] if y > tbl[-1][0] else tbl[0][1]
        return f
    fr = interp([(-130, 20), (-112, 25), (-96, 31), (-80, 33), (-60, 30), (-36, 25), (-14, 22), (6, 21)])
    bk = interp([(-130, -14), (-112, -24), (-96, -31), (-80, -33), (-60, -30), (-36, -26), (-14, -24), (6, -24)])
    body.append(P("M-24,6 C-31,-30 -34,-70 -30,-104 C-28,-118 -20,-128 -6,-134 L12,-134 C22,-128 30,-114 32,-92 C34,-70 28,-40 22,-16 L21,6 Z", "url(#steel)", 0.7, 1.2))
    body.append(lamellar([(-112, -100), (-100, -88), (-88, -76), (-76, -64), (-64, -52), (-52, -40), (-40, -28)], fr, bk))
    body.append(line("M2,-128 C6,-112 8,-90 6,-30", GOLD, 0.25))
    # collar plate and neck
    body.append(P("M-6,-136 C2,-142 16,-142 24,-134 L26,-124 C16,-128 4,-128 -8,-124 Z", "url(#steel)", 0.75))
    # kusazuri (skirt) hanging under the belt, fading out at the crop
    for i, x in enumerate(range(-26, 24, 10)):
        body.append(poly([(x, -2), (x+11, -2), (x+12, 26), (x+1, 26)], rim=0.5, w=0.9))
        body.append(f'<path d="M{x+1},{12} L{x+12},{12}" stroke="{ORANGE}" stroke-opacity="0.7" stroke-width="1.8" stroke-dasharray="2 2"/>')
    # belt (obi) with cord and knot
    body.append(poly([(-27, -24), (24, -24), (24, -4), (-27, -4)], "#14100b", 0.8, 1.1))
    body.append(line("M-26,-20 L23,-20 M-26,-8 L23,-8", GOLD, 0.45, 0.8))
    body.append(f'<path d="M-26,-14 L23,-14" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="3 3" opacity="0.9"/>')
    body.append(f'<circle cx="18" cy="-14" r="5" fill="{RED}" stroke="{GOLDL}" stroke-opacity="0.7"/>')
    t1 = "M18,-10 C20,0 16,12 20,24 L25,24 C22,12 24,0 23,-10 Z"
    t2 = "M18,-10 C24,0 22,12 28,24 L33,22 C28,10 28,0 23,-10 Z"
    body.append(f'<path d="{t1}" fill="{RED}" stroke="{GOLDL}" stroke-opacity="0.6" stroke-width="0.9"><animate attributeName="d" values="{t1};{t2};{t1}" dur="2.8s" repeatCount="indefinite"/></path>')

    # --- head group: bent forward, bobs a little on its own
    head = []
    head.append(f'<g transform="rotate(15 12 -128)">'
                '<path d="M2,-138 L16,-142 L26,-128 L8,-122 Z" fill="url(#skinp)" stroke="#fff3c9" stroke-opacity="0.3"/>'
                '<path d="M4,-172 C14,-179 30,-176 34,-166 L35,-160 L40,-153 L36,-150 L37,-145 L34,-142 L35,-138 C33,-132 27,-128 19,-128 C9,-128 3,-137 3,-149 C3,-159 3,-167 4,-172 Z" fill="url(#skinp)" stroke="#fff3c9" stroke-opacity="0.45" stroke-width="1"/>'
                '<path d="M29,-157 L36,-156" stroke="#120b06" stroke-width="1.6" stroke-linecap="round"/>'            # lowered eye
                '<path d="M25,-160 L37,-159" stroke="#120b06" stroke-width="1.2" opacity="0.8"/>'                      # brow
                '<path d="M31,-141 L36,-141" stroke="#120b06" stroke-width="1.2" stroke-linecap="round"/>'            # mouth
                '<path d="M20,-136 C26,-132 31,-134 34,-138" fill="none" stroke="#120b06" stroke-opacity="0.45" stroke-width="1"/>'
                '<ellipse cx="11" cy="-150" rx="4" ry="6" fill="#241810" stroke="#fff3c9" stroke-opacity="0.25"/></g>')
    # the conical hat, tilted forward with the head
    head.append('<g transform="rotate(24 14 -166)">'
                f'<ellipse cx="14" cy="-169" rx="41" ry="7" fill="{INK}" stroke="{GOLDL}" stroke-opacity="0.8" stroke-width="1.1"/>'
                f'<path d="M-27,-169 L14,-202 L55,-169 Q14,-161 -27,-169 Z" fill="{INK}" stroke="{GOLDL}" stroke-opacity="0.85" stroke-width="1.2" stroke-linejoin="round"/>'
                f'<path d="M14,-202 L-16,-168 M14,-202 L-2,-165 M14,-202 L14,-164 M14,-202 L30,-165 M14,-202 L42,-168" stroke="{GOLD}" stroke-opacity="0.4" stroke-width="0.9" fill="none"/>'
                f'<path d="M-20,-179 Q14,-172 46,-179 M-10,-189 Q14,-184 36,-189" stroke="{GOLD}" stroke-opacity="0.35" stroke-width="0.9" fill="none"/>'
                f'<path d="M14,-202 L44,-171" stroke="#fff3c9" stroke-opacity="0.5" stroke-width="1.1"/></g>')
    head.append(f'<path d="M-18,-160 C-14,-140 -4,-128 12,-124" stroke="{RED}" stroke-width="1.8" fill="none" opacity="0.0"/>')
    head.append(f'<path d="M6,-158 C10,-146 14,-136 22,-130" stroke="{RED}" stroke-width="1.8" fill="none"/>')     # chin cord
    # hand gripping the tip of the hat (drawn over the apex)
    ax, ay = 25, -196
    head.append(f'<g transform="translate({ax},{ay}) scale(0.82) translate({-ax},{-ay})">')
    head.append(f'<path d="M{ax-12},{ay+8} C{ax-8},{ay+2} {ax-5},{ay-1} {ax-2},{ay-3}" stroke="url(#steel)" stroke-width="9" stroke-linecap="round" fill="none"/>')
    head.append(P(f"M{ax-9},{ay-1} C{ax-9},{ay-9} {ax+1},{ay-12} {ax+8},{ay-7} C{ax+12},{ay-3} {ax+11},{ay+5} {ax+4},{ay+7} C{ax-3},{ay+8} {ax-9},{ay+5} {ax-9},{ay-1} Z", "url(#steel)", 0.9, 1.1))
    head.append(line(f"M{ax-5},{ay-5} L{ax-3},{ay+5} M{ax},{ay-7} L{ax+2},{ay+6} M{ax+5},{ay-6} L{ax+6},{ay+4}", GOLDL, 0.5, 1))
    head.append(f'<path d="M{ax-8},{ay+1} L{ax-3},{ay-6}" stroke="{ORANGE}" stroke-width="1.8" opacity="0.8"/>')
    head.append('</g>')
    body.append('<g>'
                '<animateTransform attributeName="transform" type="translate" values="0 0;0.8 1.6;0 0" dur="4.4s" begin="0.3s" repeatCount="indefinite"/>'
                + "".join(head) + '</g>')

    # --- katana, sheathed at the hip (hilt forward, scabbard running back)
    tsuba, pommel = (28, -46), (58, -61)
    ux, uy = (tsuba[0]-pommel[0]), (tsuba[1]-pommel[1]); L = math.hypot(ux, uy); ux, uy = ux/L, uy/L
    tail = (tsuba[0]+ux*130, tsuba[1]+uy*130)
    nx, ny = -uy, ux
    # scabbard
    sa, sb = (tsuba[0]+ux*6, tsuba[1]+uy*6), tail
    sw = 5.5
    body.append(poly([(sa[0]+nx*sw, sa[1]+ny*sw), (sb[0]+nx*3.6, sb[1]+ny*3.6), (sb[0]-nx*3.6, sb[1]-ny*3.6), (sa[0]-nx*sw, sa[1]-ny*sw)], "#120d09", 0.85, 1.1))
    body.append(f'<path d="M{sa[0]+ux*10+nx*2:.1f},{sa[1]+uy*10+ny*2:.1f} L{sb[0]-ux*6+nx*1.2:.1f},{sb[1]-uy*6+ny*1.2:.1f}" stroke="#fff3c9" stroke-opacity="0.35" stroke-width="0.9"/>')
    for t in (10, 22, 78):   # gold bands on the scabbard
        cx, cy = sa[0]+ux*t, sa[1]+uy*t
        body.append(f'<path d="M{cx+nx*sw:.1f},{cy+ny*sw:.1f} L{cx-nx*sw:.1f},{cy-ny*sw:.1f}" stroke="{GOLDL}" stroke-opacity="0.8" stroke-width="2"/>')
    # hilt with diamond wrap
    hw = 4
    body.append(poly([(tsuba[0]+nx*hw, tsuba[1]+ny*hw), (pommel[0]+nx*hw, pommel[1]+ny*hw), (pommel[0]-nx*hw, pommel[1]-ny*hw), (tsuba[0]-nx*hw, tsuba[1]-ny*hw)], CREAM, 0.9, 0.9))
    k = 0
    for t in range(2, int(L)-1, 5):
        cx, cy = tsuba[0]-ux*t, tsuba[1]-uy*t
        body.append(f'<path d="M{cx:.1f},{cy:.1f} l{ux*-2.5+nx*2.6:.1f},{uy*-2.5+ny*2.6:.1f} l{ux*-2.5-nx*2.6:.1f},{uy*-2.5-ny*2.6:.1f} l{ux*2.5-nx*2.6:.1f},{uy*2.5-ny*2.6:.1f} Z" fill="#2a1d12" opacity="0.85"/>')
    body.append(f'<circle cx="{pommel[0]}" cy="{pommel[1]}" r="4.4" fill="{GOLD}" stroke="{GOLDL}" stroke-width="0.8"/>')
    body.append(f'<g transform="translate({tsuba[0]},{tsuba[1]}) rotate({math.degrees(math.atan2(uy, ux)):.1f})"><ellipse rx="2.8" ry="10.5" fill="{GOLD}" stroke="{GOLDL}" stroke-width="1"/><ellipse rx="1.2" ry="7" fill="#3a2a10"/></g>')

    # --- near arm resting on the hilt, big shoulder plate (sode) over it
    body.append(limb((-8, -92), (6, -58), 18, 15))
    body.append(limb((6, -58), (26, -42), 15, 12))
    body.append(line("M8,-56 L24,-45", ORANGE, 0.75, 1.8))
    body.append(P("M20,-50 C20,-56 30,-58 36,-52 C40,-46 36,-38 28,-37 C20,-37 18,-44 20,-50 Z", "url(#steel)", 0.9, 1.1))   # gauntlet on the hilt
    body.append(line("M25,-50 L25,-40 M30,-52 L30,-39 M35,-50 L34,-40", GOLDL, 0.55, 1))
    body.append(sode(-10, -124, 3, 50, 62, 5))
    body.append(line("M-34,-126 C-30,-118 -14,-114 4,-122", GOLDL, 0.35, 1))
    # reddish collar cloth at the neck
    body.append(P("M-8,-130 C2,-136 14,-134 22,-128 L20,-120 C10,-124 0,-122 -10,-118 Z", RED, 0.7, 1))

    g.append('<g><animateTransform attributeName="transform" type="scale" values="1 1;1.012 1.022;1 1" dur="4.4s" repeatCount="indefinite"/>' + "".join(body) + '</g>')
    return "".join(g)

if __name__ == "__main__":
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-110 -230 220 270" width="880" height="1080">'
           '<defs><linearGradient id="blade"><stop offset="0" stop-color="#fff3c9"/><stop offset="1" stop-color="#b8862f"/></linearGradient></defs>'
           '<rect x="-110" y="-230" width="220" height="270" fill="#2a2013"/>' + samurai_bust() + '</svg>')
    open("/tmp/bust.svg", "w").write(svg)
