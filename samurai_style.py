"""Stylised samurai drawing: smooth gradient shapes, soft rim light, glowing half-drawn katana.
Canvas is 600x600, facing right, leaning forward, head bent, conical hat tilted forward.
Change PALETTE to 'teal' for cyan lighting instead of the gold/ember lighting."""
import math

PALETTE = "ember"
PALS = {
    "ember": dict(a0="#322b25", a1="#0b0907", a2="#443a31", rim="#ffd98a", glow="#fff1c4", glow2="#ffb347", acc="#ee7a2f", acc2="#a8401a", c0="#241e19", c1="#080606"),
    "teal":  dict(a0="#24465a", a1="#08121a", a2="#34596d", rim="#6fefff", glow="#c4fbff", glow2="#19d3ee", acc="#ee7a2f", acc2="#a8401a", c0="#17303c", c1="#060d12"),
}

def capsule(p, q, w0, w1, fill):
    dx, dy = q[0]-p[0], q[1]-p[1]; L = math.hypot(dx, dy) or 1
    nx, ny = -dy/L, dx/L; r0, r1 = w0/2, w1/2
    a = (p[0]+nx*r0, p[1]+ny*r0); b = (q[0]+nx*r1, q[1]+ny*r1); c = (q[0]-nx*r1, q[1]-ny*r1); d = (p[0]-nx*r0, p[1]-ny*r0)
    return (f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f} A{r1},{r1} 0 0 1 {c[0]:.1f},{c[1]:.1f} '
            f'L{d[0]:.1f},{d[1]:.1f} A{r0},{r0} 0 0 1 {a[0]:.1f},{a[1]:.1f} Z" fill="{fill}"/>')

def glove(cx, cy, ang, w=34, h=22, thumb=True):
    out = f'<g transform="translate({cx},{cy}) rotate({ang})">'
    out += f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="8" fill="#0d0b09"/>'
    out += f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="8" fill="none" stroke="#ffd98a" stroke-opacity="0.35" stroke-width="1.2"/>'
    for i in range(4):
        x = -w/2 + 5 + i * (w-10)/3
        out += f'<path d="M{x:.1f},{-h/2+2} L{x:.1f},{h/2-2}" stroke="#ffd98a" stroke-opacity="0.45" stroke-width="1.4" stroke-linecap="round"/>'
    out += f'<rect x="{-w/2}" y="{-h/2}" width="7" height="{h}" rx="3" fill="url(#sm-acc)"/>'   # cuff in the accent colour
    if thumb:
        out += f'<path d="M{-w/2+9},{-h/2+1} L{w/2-4},{-h/2-3}" stroke="#0d0b09" stroke-width="7" stroke-linecap="round"/>'
        out += f'<path d="M{-w/2+9},{-h/2-2} L{w/2-4},{-h/2-6}" stroke="#ffd98a" stroke-opacity="0.35" stroke-width="1.1" stroke-linecap="round"/>'
    return out + '</g>'

def samurai_drawing(palette=None):
    pal = PALS[palette or PALETTE]
    R, G1, G2, AC = pal["rim"], pal["glow"], pal["glow2"], pal["acc"]
    g = []
    g.append(f'''<defs>
<linearGradient id="sm-arm" x1="0.2" y1="0" x2="0.6" y2="1"><stop offset="0" stop-color="{pal['a0']}"/><stop offset="1" stop-color="{pal['a1']}"/></linearGradient>
<linearGradient id="sm-arm2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{pal['a2']}"/><stop offset="1" stop-color="{pal['a0']}"/></linearGradient>
<linearGradient id="sm-cloth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{pal['c0']}"/><stop offset="1" stop-color="{pal['c1']}"/></linearGradient>
<linearGradient id="sm-acc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{AC}"/><stop offset="1" stop-color="{pal['acc2']}"/></linearGradient>
<linearGradient id="sm-hat" x1="0" y1="0" x2="0.9" y2="1"><stop offset="0" stop-color="{pal['a2']}"/><stop offset="0.55" stop-color="{pal['a0']}"/><stop offset="1" stop-color="{pal['a1']}"/></linearGradient>
<linearGradient id="sm-blade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="0.5" stop-color="{G1}"/><stop offset="1" stop-color="{G2}"/></linearGradient>
<pattern id="sm-weave" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><path d="M0,0 L0,12 M6,0 L6,12" stroke="{R}" stroke-opacity="0.10" stroke-width="1"/></pattern>
<filter id="sm-rim" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="0.9"/></filter>
<filter id="sm-soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="sm-halo" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
</defs>''')

    def rim(d, op=0.6, w=1.5):
        return f'<path d="{d}" fill="none" stroke="{R}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round" filter="url(#sm-rim)"/>'
    def edge(d, op=0.18, w=1.2):
        return f'<path d="{d}" fill="none" stroke="{R}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"/>'

    body = []
    # ---------------------------------------------------------------- ribbon streaming from the hat (behind)
    for (r1, r2, dur, k) in [
        ("M266,174 C244,160 224,138 190,142 C176,144 168,136 154,132 C174,126 198,130 218,142 C238,154 252,164 272,168 Z",
         "M266,174 C244,172 220,158 190,162 C178,164 168,160 156,158 C176,150 200,150 218,160 C238,168 252,172 272,168 Z", 2.6, 0),
        ("M268,182 C250,178 234,168 214,174 C202,178 192,172 180,178 C194,162 214,160 232,164 C248,168 258,176 272,178 Z",
         "M268,182 C250,184 232,176 214,184 C202,188 192,184 182,190 C196,174 214,174 232,176 C248,178 258,182 272,178 Z", 3.1, 0.4)]:
        body.append(f'<path d="{r1}" fill="url(#sm-acc)"><animate attributeName="d" values="{r1};{r2};{r1}" dur="{dur}s" begin="{k}s" repeatCount="indefinite"/></path>')

    # ---------------------------------------------------------------- lower body (hakama) with weave texture
    HK = "M258,396 C252,440 238,512 212,604 L398,604 C382,524 366,456 356,402 Z"
    body.append(f'<path d="{HK}" fill="url(#sm-cloth)"/><path d="{HK}" fill="url(#sm-weave)"/>')
    body.append(edge("M286,410 C282,470 268,540 250,604 M312,410 C314,480 314,540 318,604 M338,410 C344,470 354,540 372,604", 0.14))
    body.append(rim("M258,396 C252,440 238,512 212,604", 0.4, 1.6))

    # ---------------------------------------------------------------- torso leaning forward
    body.append('<path d="M212,270 C228,248 262,238 296,244 C326,250 346,274 350,312 C354,346 354,374 352,400 L260,396 C246,350 226,308 212,270 Z" fill="url(#sm-arm)"/>')
    body.append('<path d="M262,284 C290,270 322,274 338,300 C342,330 338,360 332,386 L284,386 C276,350 268,318 262,284 Z" fill="url(#sm-arm2)" opacity="0.85"/>')
    body.append(edge("M268,304 C292,296 318,298 338,310 M272,330 C296,324 318,326 340,336 M276,356 C298,352 320,354 338,360", 0.2))
    body.append(f'<path d="M300,314 L308,322 L300,330 L292,322 Z" fill="{G2}" opacity="0.8"><animate attributeName="opacity" values="0.4;0.95;0.4" dur="3s" repeatCount="indefinite"/></path>')
    body.append(rim("M214,268 C226,250 258,240 294,246", 0.55, 1.6))
    body.append(rim("M350,314 C352,346 348,372 344,396", 0.25, 1.2))
    # collar
    body.append('<path d="M286,248 C300,236 328,236 342,250 L338,270 C318,262 300,264 284,272 Z" fill="url(#sm-arm2)"/>')
    body.append(f'<path d="M288,252 C302,242 326,242 338,254" fill="none" stroke="{AC}" stroke-width="2.4" stroke-linecap="round"/>')
    # belt, cord and hanging sash tail
    body.append('<path d="M254,390 L358,396 L356,416 L252,410 Z" fill="url(#sm-arm2)"/>')
    body.append(f'<path d="M254,400 L357,406" stroke="{AC}" stroke-width="3" stroke-dasharray="4 4" opacity="0.9"/>')
    body.append(f'<circle cx="272" cy="408" r="7" fill="url(#sm-acc)"/>')
    t1 = "M266,412 C260,442 270,464 260,492 L272,494 C282,464 276,440 280,414 Z"
    t2 = "M266,412 C266,442 280,462 276,490 L288,488 C292,462 284,440 280,414 Z"
    body.append(f'<path d="{t1}" fill="url(#sm-acc)"><animate attributeName="d" values="{t1};{t2};{t1}" dur="2.8s" repeatCount="indefinite"/></path>')

    # ---------------------------------------------------------------- head: neck, mask, glowing visor
    body.append('<path d="M318,238 L350,232 L352,264 L314,268 Z" fill="url(#sm-cloth)"/>')
    body.append('<path d="M316,212 C324,205 348,203 359,212 C362,228 357,244 346,252 C334,258 322,252 316,240 Z" fill="url(#sm-arm2)"/>')
    body.append(rim("M359,214 C362,228 357,244 346,252", 0.5, 1.4))
    body.append(f'<path d="M324,227 L348,222" stroke="{G2}" stroke-width="7" stroke-linecap="round" opacity="0.55" filter="url(#sm-soft)"><animate attributeName="opacity" values="0.35;0.7;0.35" dur="3.4s" repeatCount="indefinite"/></path>')
    body.append(f'<path d="M325,227 L347,222.5" stroke="{G1}" stroke-width="2.6" stroke-linecap="round"/>')

    # ---------------------------------------------------------------- the conical hat, tilted forward
    hat = []
    hat.append('<ellipse cx="324" cy="200" rx="84" ry="15" transform="rotate(30 324 200)" fill="#07060a"/>')
    hat.append('<path d="M250,158 L360,136 L398,244 C352,228 290,204 250,158 Z" fill="url(#sm-hat)"/>')
    hat.append('<path d="M250,158 L360,136 L332,198 C300,188 270,174 250,158 Z" fill="' + pal['a2'] + '" opacity="0.45"/>')
    hat.append(edge("M360,136 L262,168 M360,136 L300,198 M360,136 L350,218 M360,136 L382,234", 0.13))
    hat.append(f'<path d="M258,166 C292,196 340,216 394,238" fill="none" stroke="url(#sm-acc)" stroke-width="7" stroke-linecap="round"/>')
    hat.append(f'<path d="M262,166 C294,194 340,212 390,233" fill="none" stroke="#ffd0a0" stroke-opacity="0.35" stroke-width="1.4" stroke-linecap="round"/>')
    hat.append(rim("M250,158 L360,136", 0.75, 1.8))
    hat.append(rim("M360,136 L398,244", 0.35, 1.3))
    hat.append(f'<circle cx="360" cy="136" r="3" fill="{R}" opacity="0.9"/>')
    body.append('<g><animateTransform attributeName="transform" type="rotate" values="0 324 200;-1.3 324 200;0 324 200" dur="5s" repeatCount="indefinite"/>' + "".join(hat) + '</g>')

    # front upper arm sits BEHIND the sword so the guard and hilt stay readable
    body.append(capsule((316, 272), (440, 342), 32, 26, "url(#sm-arm)"))
    body.append(rim("M326,256 C356,268 400,300 434,328", 0.4, 1.4))
    # ---------------------------------------------------------------- the katana, half drawn
    PM, TS, MO, EN = (530, 252), (410, 316), (296, 378), (84, 520)
    # scabbard
    ux, uy = EN[0]-MO[0], EN[1]-MO[1]; L = math.hypot(ux, uy); ux, uy = ux/L, uy/L; nx, ny = -uy, ux
    sc = [(MO[0]+nx*6, MO[1]+ny*6), (EN[0]+nx*3.5, EN[1]+ny*3.5), (EN[0]-nx*3.5, EN[1]-ny*3.5), (MO[0]-nx*6, MO[1]-ny*6)]
    body.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in sc) + ' Z" fill="#0d0a08"/>')
    body.append(f'<path d="M{MO[0]+nx*3.2+ux*8:.1f},{MO[1]+ny*3.2+uy*8:.1f} L{EN[0]+nx*1.6-ux*10:.1f},{EN[1]+ny*1.6-uy*10:.1f}" stroke="{R}" stroke-opacity="0.5" stroke-width="1.3" filter="url(#sm-rim)"/>')
    for t in (10, 26, 200):
        cx, cy = MO[0]+ux*t, MO[1]+uy*t
        body.append(f'<path d="M{cx+nx*6.4:.1f},{cy+ny*6.4:.1f} L{cx-nx*6.4:.1f},{cy-ny*6.4:.1f}" stroke="{R}" stroke-opacity="0.75" stroke-width="2.4"/>')
    # glowing exposed blade
    bx, by = MO[0]-TS[0], MO[1]-TS[1]; bl = math.hypot(bx, by); bx, by = bx/bl, by/bl; bnx, bny = -by, bx
    blade = [(TS[0]+bnx*4, TS[1]+bny*4), (MO[0]+bnx*4, MO[1]+bny*4), (MO[0]-bnx*4, MO[1]-bny*4), (TS[0]-bnx*4, TS[1]-bny*4)]
    bp = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in blade) + " Z"
    body.append(f'<path d="{bp}" fill="{G2}" opacity="0.7" filter="url(#sm-halo)"><animate attributeName="opacity" values="0.45;0.9;0.45" dur="2.6s" repeatCount="indefinite"/></path>')
    body.append(f'<path d="{bp}" fill="url(#sm-blade)"/>')
    body.append(f'<path d="M{TS[0]+bx*6:.1f},{TS[1]+by*6:.1f} L{MO[0]-bx*4:.1f},{MO[1]-by*4:.1f}" stroke="#ffffff" stroke-width="1.4" opacity="0.9"/>')
    # hilt: ivory wrap with dark diamonds, big gold guard and pommel (kept clear of the forearm)
    hx, hy = TS[0]-PM[0], TS[1]-PM[1]; hl = math.hypot(hx, hy); hx, hy = hx/hl, hy/hl; hnx, hny = -hy, hx
    hilt = [(PM[0]+hnx*6, PM[1]+hny*6), (TS[0]+hnx*6, TS[1]+hny*6), (TS[0]-hnx*6, TS[1]-hny*6), (PM[0]-hnx*6, PM[1]-hny*6)]
    body.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in hilt) + ' Z" fill="#e6dbbd"/>')
    body.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in hilt) + ' Z" fill="none" stroke="#7a6a48" stroke-width="1"/>')
    for t in range(9, int(hl)-6, 11):
        cx, cy = PM[0]+hx*t, PM[1]+hy*t
        body.append(f'<path d="M{cx-hx*5:.1f},{cy-hy*5:.1f} L{cx+hnx*5.4:.1f},{cy+hny*5.4:.1f} L{cx+hx*5:.1f},{cy+hy*5:.1f} L{cx-hnx*5.4:.1f},{cy-hny*5.4:.1f} Z" fill="#2a1d12" opacity="0.9"/>')
    body.append(f'<circle cx="{PM[0]}" cy="{PM[1]}" r="8" fill="{R}"/><circle cx="{PM[0]}" cy="{PM[1]}" r="4" fill="#3a2a10"/>')
    body.append(f'<g transform="translate({TS[0]},{TS[1]}) rotate({math.degrees(math.atan2(hy, hx)):.1f})"><ellipse rx="5" ry="17" fill="{R}"/><ellipse rx="2.4" ry="12" fill="#2b2013"/></g>')
    body.append(f'<g transform="translate({TS[0]+bx*10:.1f},{TS[1]+by*10:.1f}) rotate({math.degrees(math.atan2(by, bx)):.1f})"><rect x="-3" y="-5.5" width="7" height="11" rx="1.5" fill="{R}"/></g>')

    # ---------------------------------------------------------------- rear arm with layered pauldron, hand at the scabbard mouth
    body.append(capsule((214, 284), (160, 350), 36, 30, "url(#sm-arm)"))
    body.append(capsule((160, 350), (260, 392), 30, 23, "url(#sm-arm2)"))
    body.append(edge("M184,340 C204,356 230,372 252,382", 0.25))
    body.append(rim("M200,268 C184,288 168,318 146,344", 0.45, 1.4))
    body.append(f'<path d="M178,350 L192,358 M194,356 L208,364" stroke="{AC}" stroke-width="3" stroke-linecap="round" opacity="0.9"/>')
    pa = ['<g transform="translate(216,266) rotate(22)">']
    pa.append(f'<path d="M-30,6 C-30,-8 30,-8 30,6 L30,10 L-30,10 Z" fill="url(#sm-arm)"/>')    # rounded shoulder cap
    for i in range(4):
        y = 6 + i * 13
        w = 62 - i * 3
        pa.append(f'<rect x="{-w/2}" y="{y}" width="{w}" height="12.5" rx="4.5" fill="url(#sm-arm2)"/>')
        for xx in (-w*0.32, -4, w*0.2):
            pa.append(f'<rect x="{xx:.1f}" y="{y+2.5}" width="8" height="7" rx="2" fill="url(#sm-acc)" opacity="0.92"/>')
    pa.append(f'<path d="M-30,4 C-20,-6 20,-6 30,4" fill="none" stroke="{R}" stroke-opacity="0.6" stroke-width="1.5" filter="url(#sm-rim)"/></g>')
    body.append("".join(pa))
    body.append(glove(278, 391, -33.8, 36, 22, thumb=True))

    # ---------------------------------------------------------------- front arm up to the hilt
    body.append(capsule((440, 342), (478, 288), 26, 20, "url(#sm-arm2)"))
    body.append(f'<path d="M450,332 L464,314 M458,322 L472,304" stroke="{AC}" stroke-width="3" stroke-linecap="round" opacity="0.9"/>')
    hand = (TS[0] + (PM[0]-TS[0]) * 0.62, TS[1] + (PM[1]-TS[1]) * 0.62)
    body.append(glove(hand[0], hand[1], -28.4, 34, 24, thumb=True))

    # ---------------------------------------------------------------- sparks off the blade
    for i, (x, y) in enumerate([(380, 322), (352, 340), (326, 360), (400, 312), (338, 350)]):
        body.append(f'<circle cx="{x}" cy="{y}" r="{1.6 + (i%3)*0.6:.1f}" fill="{G1}"><animate attributeName="cy" values="{y};{y-46}" dur="{2.4+i*0.5:.1f}s" begin="{i*0.6:.1f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values="0;1;0" dur="{2.4+i*0.5:.1f}s" begin="{i*0.6:.1f}s" repeatCount="indefinite"/></circle>')

    # the whole upper body breathes (pivot at the waist)
    g.append('<g transform="translate(330 420)"><g><animateTransform attributeName="transform" type="scale" values="1 1;1.01 1.018;1 1" dur="4.4s" repeatCount="indefinite"/>'
             '<g transform="translate(-330 -420)">' + "".join(body) + '</g></g></g>')
    return "".join(g)

if __name__ == "__main__":
    open("/tmp/style.svg", "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 100 540 520" width="1080" height="1040"><rect x="0" y="0" width="700" height="700" fill="#2d241a"/>' + samurai_drawing() + '</svg>')
