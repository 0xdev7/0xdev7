"""Generate animated SVGs for the GitHub profile README (0xdev7/0xdev7/assets)."""
import sys
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BG, PANEL, LINE = "#0b0f1a", "#111827", "#1f2937"
TEXT, MUTED = "#e5e7eb", "#94a3b8"
CYAN, VIOLET, EMERALD, AMBER, ROSE, PINK = "#22d3ee", "#8b5cf6", "#34d399", "#fbbf24", "#fb7185", "#f472b6"
SANS = "'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(w, h, body, style="", defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<style>
.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
{style}
{RM}
</style>
<defs>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
</linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
<path d="M32 0H0V32" stroke="#ffffff" stroke-opacity=".045"/>
</pattern>
{defs}
</defs>
{body}
</svg>
"""


def card(w, h, rx=18):
    return (f'<rect width="{w}" height="{h}" rx="{rx}" fill="{BG}"/>'
            f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#grid)"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" stroke="{LINE}"/>')


# ---------------------------------------------------------------- header
def header():
    W, H = 1200, 360
    roles = ["Front-End Team Lead", "Senior Full-Stack Engineer", "React · Next.js · Node.js · TypeScript",
             "Fintech, KYC &amp; Payments", "Web3 &amp; DeFi Builder", "AI-Augmented Engineer"]
    n, step = len(roles), 3.0
    cyc = n * step
    on, off = 100 * 0.4 / cyc, 100 * (step - 0.3) / cyc
    style = f"""
@keyframes role{{0%{{opacity:0;transform:translateY(12px)}}{on:.2f}%{{opacity:1;transform:translateY(0)}}{off:.2f}%{{opacity:1;transform:translateY(0)}}{off+2:.2f}%{{opacity:0;transform:translateY(-12px)}}100%{{opacity:0}}}}
.role{{opacity:0;animation:role {cyc}s infinite}}
@keyframes up{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:none}}}}
.up{{opacity:0;animation:up .8s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.pulse{{animation:pulse 1.6s infinite}}
@keyframes ring{{0%{{r:5;opacity:.8}}100%{{r:14;opacity:0}}}}
.ring{{animation:ring 1.6s infinite}}
@keyframes drift1{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(120px,40px)}}}}
@keyframes drift2{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-140px,-30px)}}}}
.o1{{animation:drift1 14s ease-in-out infinite}} .o2{{animation:drift2 18s ease-in-out infinite}}
@keyframes blink{{50%{{opacity:0}}}} .caret{{animation:blink 1s steps(1) infinite}}
"""
    # deploy.log panel: rows appear one by one, then the cycle restarts
    events = [("01", "BUILD", "passing", "RUN", EMERALD), ("02", "LEDGER", "14 yrs settled", "LDG", CYAN),
              ("03", "INCIDENT", "resolved", "INC", AMBER), ("04", "AGENT", "reviewed by human", "PR", VIOLET),
              ("05", "DEPLOY", "ready", "REL", PINK)]
    LOOP = 11.0
    px, py, pw, ph = 772, 46, 384, 250
    rows = []
    for i, (num, kind, msg, tag, col) in enumerate(events):
        t0 = 100 * (0.6 + i * 1.0) / LOOP
        style += (f"@keyframes ev{i}{{0%,{t0:.2f}%{{opacity:0;transform:translateX(-10px)}}"
                  f"{t0+4:.2f}%,92%{{opacity:1;transform:none}}100%{{opacity:0}}}}"
                  f".ev{i}{{opacity:0;animation:ev{i} {LOOP}s infinite}}\n")
        y = py + 66 + i * 34
        rows.append(f'''<g class="ev{i}">
<text x="{px+20}" y="{y}" class="mono" font-size="12" fill="{MUTED}">[{num}]</text>
<text x="{px+62}" y="{y}" class="mono" font-size="13" font-weight="700" fill="{col}">{kind}</text>
<text x="{px+150}" y="{y}" class="mono" font-size="13" fill="{TEXT}">{msg}</text>
<rect x="{px+pw-62}" y="{y-14}" width="42" height="19" rx="6" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>
<text x="{px+pw-41}" y="{y}" class="mono" font-size="11" font-weight="700" fill="{col}" text-anchor="middle">{tag}</text>
</g>''')
    panel = f'''<g class="up" style="animation-delay:.5s">
<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{PANEL}" fill-opacity=".85" stroke="{LINE}"/>
<circle cx="{px+20}" cy="{py+20}" r="5" fill="{ROSE}"/><circle cx="{px+38}" cy="{py+20}" r="5" fill="{AMBER}"/><circle cx="{px+56}" cy="{py+20}" r="5" fill="{EMERALD}"/>
<text x="{px+pw/2}" y="{py+24}" class="mono" font-size="12" fill="{MUTED}" text-anchor="middle">~/devang/deploy.log</text>
<line x1="{px}" y1="{py+38}" x2="{px+pw}" y2="{py+38}" stroke="{LINE}"/>
{''.join(rows)}
<text x="{px+20}" y="{py+ph-18}" class="mono" font-size="13" fill="{CYAN}">$ <tspan class="caret" fill="{TEXT}">▍</tspan></text>
</g>'''

    # tech ticker along the bottom, scrolls forever
    items = ["React 19", "Next.js 16", "TypeScript", "Node.js", "Express", "tRPC", "PostgreSQL", "MongoDB", "MySQL",
             "MSSQL", "Redis", "Docker", "GitHub Actions", "Azure Container Apps", "AWS KMS", "wagmi · viem",
             "Reown AppKit", "Safe SDK", "e-KYC", "Payment gateways", "WebAssembly", "Tailwind", "Claude Code"]
    s = "   ◆   ".join(items) + "   ◆   "
    fs, cw = 13, 13 * 0.6
    tw = len(s) * cw
    style += f"@keyframes tick{{from{{transform:translateX(0)}}to{{transform:translateX(-{tw:.1f}px)}}}} .tick{{animation:tick 45s linear infinite}}\n"
    ty = H - 22
    ticker = f'''<clipPath id="tclip"><rect x="1" y="{H-50}" width="{W-2}" height="49" rx="17"/></clipPath>
<line x1="0" y1="{H-50}" x2="{W}" y2="{H-50}" stroke="{LINE}"/>
<g clip-path="url(#tclip)"><rect y="{H-50}" width="{W}" height="50" fill="{PANEL}" fill-opacity=".6"/>
<g class="tick">
<text x="24" y="{ty}" class="mono" font-size="{fs}" fill="{MUTED}" xml:space="preserve">{esc(s)}</text>
<text x="{24+tw:.1f}" y="{ty}" class="mono" font-size="{fs}" fill="{MUTED}" xml:space="preserve">{esc(s)}</text>
</g></g>'''

    role_txt = "".join(
        f'<text x="88" y="214" class="mono role" font-size="24" font-weight="600" fill="{TEXT}" '
        f'style="animation-delay:{i*step}s">{r}</text>' for i, r in enumerate(roles))

    defs = f'''<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
<linearGradient id="name" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox" spreadMethod="reflect">
<stop offset="0" stop-color="{TEXT}"/><stop offset=".45" stop-color="{CYAN}"/><stop offset=".75" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="10s" repeatCount="indefinite"/>
</linearGradient>
<clipPath id="all"><rect width="{W}" height="{H}" rx="18"/></clipPath>'''

    body = f'''<g clip-path="url(#all)">
{card(W, H)}
<circle class="o1" cx="200" cy="80" r="160" fill="{CYAN}" fill-opacity=".16" filter="url(#blur)"/>
<circle class="o2" cx="980" cy="260" r="180" fill="{VIOLET}" fill-opacity=".18" filter="url(#blur)"/>
<g class="up" style="animation-delay:.05s"><text x="56" y="82" class="mono" font-size="15" fill="{CYAN}">// hello, world. I'm</text></g>
<g class="up" style="animation-delay:.2s"><text x="54" y="152" class="sans" font-size="66" font-weight="800" letter-spacing="-1.5" fill="url(#name)">Devang Parekh</text></g>
<g class="up" style="animation-delay:.4s"><text x="56" y="214" class="mono" font-size="24" font-weight="700" fill="{CYAN}">▸</text>{role_txt}</g>
<g class="up" style="animation-delay:.6s"><text x="56" y="252" class="sans" font-size="16" fill="{MUTED}">14 years · 25+ products · fintech, payments, e-KYC &amp; Web3 · Ahmedabad, India</text></g>
<g class="up" style="animation-delay:.8s">
<rect x="56" y="270" width="438" height="30" rx="15" fill="{EMERALD}" fill-opacity=".08" stroke="{EMERALD}" stroke-opacity=".45"/>
<circle class="ring" cx="76" cy="285" r="5" fill="none" stroke="{EMERALD}"/>
<circle class="pulse" cx="76" cy="285" r="4.5" fill="{EMERALD}"/>
<text x="92" y="290" class="sans" font-size="13.5" fill="{TEXT}">Open to senior / lead roles · remote, hybrid or on-site</text>
</g>
{panel}
{ticker}
</g>'''
    return svg(W, H, body, style, defs)


# ---------------------------------------------------------------- terminal
def terminal():
    W = 1200
    lines = [
        ("cmd", "whoami"),
        ("out", f"<tspan fill='{TEXT}' font-weight='700'>devang-parekh</tspan>  front-end team lead · senior full-stack engineer"),
        ("cmd", "cat career.txt"),
        ("out", "14 years · banking → wallets → exchanges → Web3 · leading a team of 6"),
        ("cmd", "ls domains/"),
        ("out", f"<tspan fill='{CYAN}'>exchanges/  money-transfer/  e-wallets/  digital-banking/  e-kyc/  defi/  trading/</tspan>"),
        ("cmd", "cat stack.txt"),
        ("out", "React · Next.js · TypeScript │ Node.js · tRPC · Postgres │ Docker · GitHub Actions · Azure │ wagmi · viem"),
        ("cmd", "git log --author=devang --oneline | wc -l"),
        ("out", f"<tspan fill='{VIOLET}'>2000+</tspan> AI-assisted commits, every one reviewed and tested by a human"),
        ("cmd", "status"),
        ("out", f"<tspan fill='{EMERALD}'>●</tspan> open to senior / lead roles · remote · hybrid · on-site"),
    ]
    import re
    top, lh, x0, cw = 78, 27, 32, 14 * 0.6
    H = top + lh * len(lines) + 46
    style = "@keyframes blink{50%{opacity:0}} .caret{animation:blink 1s steps(1) infinite}"
    defs, body_lines = [], []
    t = 0.4
    for i, (kind, txt) in enumerate(lines):
        y = top + i * lh
        plain = re.sub(r"<[^>]+>", "", txt).replace("&amp;", "&")
        if kind == "cmd":
            prefix = f"<tspan fill='{EMERALD}'>devang</tspan><tspan fill='{MUTED}'>@github</tspan> <tspan fill='{CYAN}'>~</tspan> <tspan fill='{MUTED}'>$</tspan> "
            plen = len("devang@github ~ $ ")
            content = prefix + f"<tspan fill='{TEXT}'>{txt}</tspan>"
            w0, w1 = plen * cw, (plen + len(plain)) * cw + 4
            dur = max(0.3, len(plain) * 0.03)
        else:
            content = f"<tspan fill='{MUTED}'>{txt}</tspan>"
            w0, w1, dur = 0, len(plain) * cw + 40, 0.25
        defs.append(f'''<clipPath id="l{i}"><rect x="{x0-2}" y="{y-18}" height="{lh}" width="0">
<animate attributeName="width" values="0;{w0:.1f}" dur="0.01s" begin="{t:.2f}s" fill="freeze"/>
<animate attributeName="width" from="{w0:.1f}" to="{w1:.1f}" dur="{dur:.2f}s" begin="{t+0.05:.2f}s" fill="freeze"/>
</rect></clipPath>''')
        body_lines.append(f'<text x="{x0}" y="{y}" class="mono" font-size="14" clip-path="url(#l{i})" xml:space="preserve">{content}</text>')
        t += dur + (0.25 if kind == "cmd" else 0.35)
    yc = top + len(lines) * lh
    caret = (f'<g opacity="0"><animate attributeName="opacity" to="1" dur="0.01s" begin="{t:.2f}s" fill="freeze"/>'
             f'<text x="{x0}" y="{yc}" class="mono" font-size="14" xml:space="preserve"><tspan fill="{EMERALD}">devang</tspan><tspan fill="{MUTED}">@github</tspan> <tspan fill="{CYAN}">~</tspan> <tspan fill="{MUTED}">$</tspan> <tspan class="caret" fill="{TEXT}">▍</tspan></text></g>')
    body = f'''{card(W, H)}
<rect x="1" y="1" width="{W-2}" height="40" rx="17" fill="{PANEL}"/><rect x="1" y="24" width="{W-2}" height="17" fill="{PANEL}"/>
<line x1="0" y1="41" x2="{W}" y2="41" stroke="{LINE}"/>
<circle cx="26" cy="21" r="6" fill="{ROSE}"/><circle cx="46" cy="21" r="6" fill="{AMBER}"/><circle cx="66" cy="21" r="6" fill="{EMERALD}"/>
<text x="{W/2}" y="26" class="mono" font-size="13" fill="{MUTED}" text-anchor="middle">devang@github: ~ (zsh)</text>
{''.join(body_lines)}
{caret}'''
    return svg(W, H, body, style, "".join(defs))


# ---------------------------------------------------------------- stats
def stats():
    W, H = 1200, 150
    data = [("14", "years in fintech", "&amp; web", CYAN), ("25+", "products", "delivered", VIOLET),
            ("15+", "payment gateways", "integrated", EMERALD), ("5+", "KYC / identity", "providers", AMBER),
            ("20+", "security audit", "findings fixed", ROSE), ("6", "engineers", "led", PINK)]
    gap = 16
    tw = (W - gap * 5) / 6
    style = """@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.t{opacity:0;animation:up .7s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes bar{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.bar{transform:scaleX(0);transform-box:fill-box;transform-origin:left;animation:bar 1.2s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes glow{0%,100%{stroke-opacity:.25}50%{stroke-opacity:.8}}
.g{animation:glow 3s ease-in-out infinite}"""
    tiles = []
    for i, (v, l1, l2, c) in enumerate(data):
        x = i * (tw + gap)
        d = 0.12 * i
        tiles.append(f'''<g class="t" style="animation-delay:{d:.2f}s">
<rect x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{H-1}" rx="16" fill="{BG}"/>
<rect x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{H-1}" rx="16" fill="url(#grid)"/>
<rect class="g" x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{H-1}" rx="16" stroke="{c}" style="animation-delay:{i*0.5:.1f}s"/>
<text x="{x+20:.1f}" y="64" class="sans" font-size="44" font-weight="800" letter-spacing="-1" fill="{c}">{v}</text>
<text x="{x+20:.1f}" y="94" class="sans" font-size="13.5" fill="{TEXT}">{l1}</text>
<text x="{x+20:.1f}" y="112" class="sans" font-size="13.5" fill="{MUTED}">{l2}</text>
<rect x="{x+20:.1f}" y="128" width="{tw-40:.1f}" height="3" rx="1.5" fill="{LINE}"/>
<rect class="bar" x="{x+20:.1f}" y="128" width="{tw-40:.1f}" height="3" rx="1.5" fill="{c}" style="animation-delay:{0.4+d:.2f}s"/>
</g>''')
    return svg(W, H, "".join(tiles), style)


# ---------------------------------------------------------------- timeline
def timeline():
    W, H = 1200, 330
    y0, xa, xb = 165, 70, 1130
    X = lambda yr: xa + (yr - 2012) / 14 * (xb - xa)
    roles = [
        (2012, 2016, "Oct 2012 – Dec 2015", "PHP Developer", "Cantech · Bhavnagar", "E-commerce, SaaS &amp; enterprise web", CYAN, "below"),
        (2016, 2020, "Jan 2016 – Mar 2020", "PHP Developer → Principal Consultant", "Joshi Biztech Solution · Bhavnagar", "Exchanges, money transfer, wallets · Person of the Year 2018/19", VIOLET, "above"),
        (2020, 2023, "Apr 2020 – 2022", "Principal Consultant, Frontend", "Bankai Infotech · Bankai Group", "Digital banking, e-wallets &amp; e-KYC (MobiFin)", EMERALD, "below"),
        (2023, 2026, "2023 – present", "Front-End Team Lead", "Bankai Infotech · Bankai Group", "Web3, DeFi &amp; trading · team of 6", PINK, "above"),
    ]
    L = xb - xa
    DRAW = 3.0
    style = f"""@keyframes draw{{to{{stroke-dashoffset:0}}}}
.seg{{stroke-dasharray:{L};stroke-dashoffset:{L};animation:draw {DRAW}s cubic-bezier(.4,0,.2,1) forwards}}
@keyframes pop{{0%{{opacity:0;transform:scale(0)}}70%{{transform:scale(1.25)}}100%{{opacity:1;transform:scale(1)}}}}
.pop{{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .5s ease-out forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(var(--dy))}}to{{opacity:1;transform:none}}}}
.c{{opacity:0;animation:up .6s ease-out forwards}}
@keyframes ring{{0%{{r:7;opacity:.9}}100%{{r:22;opacity:0}}}} .ring{{animation:ring 1.8s ease-out infinite}}"""
    parts = [card(W, H)]
    parts.append(f'<line x1="{xa}" y1="{y0}" x2="{xb}" y2="{y0}" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>')
    parts.append(f'<line class="seg" x1="{xa}" y1="{y0}" x2="{xb}" y2="{y0}" stroke="url(#tl)" stroke-width="4" stroke-linecap="round"/>')
    for yr in range(2012, 2027, 2):
        parts.append(f'<text x="{X(yr):.1f}" y="{y0+4+ (0)}" dy="22" class="mono" font-size="11" fill="{MUTED}" fill-opacity=".55" text-anchor="middle">{yr}</text>'
                     if False else "")
    for (a, b, per, role, comp, focus, c, side) in roles:
        x = X(a)
        delay = (x - xa) / L * DRAW
        parts.append(f'<circle class="pop" cx="{x:.1f}" cy="{y0}" r="9" fill="{BG}" stroke="{c}" stroke-width="3" style="animation-delay:{delay:.2f}s"/>')
        parts.append(f'<circle class="pop" cx="{x:.1f}" cy="{y0}" r="3.5" fill="{c}" style="animation-delay:{delay+.1:.2f}s"/>')
        if side == "above":
            ty, dy, ly1, ly2 = 52, "12px", y0 - 12, 128
        else:
            ty, dy, ly1, ly2 = 214, "-12px", y0 + 12, 196
        tx = x - 4
        parts.append(f'''<g class="c" style="--dy:{dy};animation-delay:{delay+.25:.2f}s">
<line x1="{x:.1f}" y1="{ly1}" x2="{x:.1f}" y2="{ly2}" stroke="{c}" stroke-opacity=".5" stroke-dasharray="3 4"/>
<text x="{tx:.1f}" y="{ty}" class="mono" font-size="12" font-weight="600" fill="{c}">{per}</text>
<text x="{tx:.1f}" y="{ty+24}" class="sans" font-size="17" font-weight="700" fill="{TEXT}">{role}</text>
<text x="{tx:.1f}" y="{ty+44}" class="sans" font-size="13" fill="{TEXT}" fill-opacity=".8">{comp}</text>
<text x="{tx:.1f}" y="{ty+63}" class="sans" font-size="12.5" fill="{MUTED}">{focus}</text>
</g>''')
    # "now" marker at the end of the line
    parts.append(f'''<g class="pop" style="animation-delay:{DRAW:.2f}s">
<circle cx="{xb}" cy="{y0}" r="7" fill="{PINK}"/></g>
<circle class="ring" cx="{xb}" cy="{y0}" r="7" fill="none" stroke="{PINK}" stroke-width="2" style="animation-delay:{DRAW:.2f}s"/>
<g class="c" style="--dy:-8px;animation-delay:{DRAW+.2:.2f}s"><text x="{xb}" y="{y0+36}" class="mono" font-size="12" font-weight="700" fill="{PINK}" text-anchor="end">NOW</text></g>
''')
    defs = (f'<linearGradient id="tl" x1="{xa}" y1="0" x2="{xb}" y2="0" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{CYAN}"/><stop offset=".3" stop-color="{VIOLET}"/><stop offset=".65" stop-color="{EMERALD}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>')
    return svg(W, H, "".join(parts), style, defs)


# ---------------------------------------------------------------- AI workflow
def ai_flow():
    W, H = 1200, 232
    steps = [("01", "Spec", "written spec +", "data model", CYAN), ("02", "Plan", "step-by-step plan,", "resumable sessions", VIOLET),
             ("03", "Implement", "Claude Code subagents", "in parallel worktrees", PINK), ("04", "Review", "human review", "+ tests on every change", AMBER),
             ("05", "Ship", "staged rollout", "UAT → prod", EMERALD)]
    bw, bh, top = 196, 104, 34
    gap = (W - 64 - 5 * bw) / 4
    CYC = 6.0
    style = f"""@keyframes flow{{to{{stroke-dashoffset:-20}}}} .flow{{stroke-dasharray:6 4;animation:flow .8s linear infinite}}
@keyframes act{{0%,22%{{stroke-opacity:1;fill-opacity:.14}}30%,100%{{stroke-opacity:.3;fill-opacity:.04}}}}
.box{{stroke-opacity:.3;fill-opacity:.04;animation:act {CYC}s infinite}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}} .u{{opacity:0;animation:up .6s ease-out forwards}}
@keyframes dot{{0%{{offset-distance:0%;opacity:0}}5%{{opacity:1}}95%{{opacity:1}}100%{{offset-distance:100%;opacity:0}}}}"""
    parts = [card(W, H)]
    for i, (num, title, d1, d2, c) in enumerate(steps):
        x = 32 + i * (bw + gap)
        parts.append(f'''<g class="u" style="animation-delay:{i*0.15:.2f}s">
<rect class="box" x="{x:.1f}" y="{top}" width="{bw}" height="{bh}" rx="14" fill="{c}" stroke="{c}" stroke-width="1.5" style="animation-delay:{i*CYC/5:.2f}s"/>
<text x="{x+18:.1f}" y="{top+28}" class="mono" font-size="12" font-weight="700" fill="{c}">{num}</text>
<text x="{x+18:.1f}" y="{top+54}" class="sans" font-size="20" font-weight="800" fill="{TEXT}">{title}</text>
<text x="{x+18:.1f}" y="{top+76}" class="sans" font-size="12.5" fill="{MUTED}">{d1}</text>
<text x="{x+18:.1f}" y="{top+93}" class="sans" font-size="12.5" fill="{MUTED}">{d2}</text>
</g>''')
        if i < 4:
            x1, x2, yy = x + bw + 4, x + bw + gap - 4, top + bh / 2
            parts.append(f'<line class="flow" x1="{x1:.1f}" y1="{yy}" x2="{x2-6:.1f}" y2="{yy}" stroke="{c}" stroke-width="2"/>'
                         f'<path d="M{x2-8:.1f} {yy-5} L{x2:.1f} {yy} L{x2-8:.1f} {yy+5}" stroke="{c}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    nums = [("2,000+", "AI-assisted commits", CYAN), ("150+", "Claude Code sessions", VIOLET), ("15+", "repos", PINK), ("10", "custom subagents", EMERALD)]
    cx = 32
    cy = top + bh + 34
    for i, (v, l, c) in enumerate(nums):
        w = len(v) * 10.5 + len(l) * 7.9 + 46
        parts.append(f'''<g class="u" style="animation-delay:{0.9+i*0.12:.2f}s">
<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="34" rx="17" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-opacity=".45"/>
<text x="{cx+18:.1f}" y="{cy+22}" class="sans" font-size="14"><tspan font-weight="800" fill="{c}">{v}</tspan><tspan fill="{TEXT}" dx="6">{l}</tspan></text>
</g>''')
        cx += w + 12
    return svg(W, H, "".join(parts), style)


# ---------------------------------------------------------------- divider
def divider():
    W, H = 1200, 6
    defs = f'''<linearGradient id="d" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="repeat">
<stop offset="0" stop-color="{CYAN}" stop-opacity=".1"/><stop offset=".25" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset=".75" stop-color="{PINK}"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".1"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{W} 0" dur="6s" repeatCount="indefinite"/>
</linearGradient>'''
    return svg(W, H, f'<rect width="{W}" height="{H}" rx="3" fill="url(#d)"/>', "", defs)


for name, fn in [("header", header), ("terminal", terminal), ("stats", stats), ("timeline", timeline),
                 ("ai-flow", ai_flow), ("divider", divider)]:
    (OUT / f"{name}.svg").write_text(fn())
    print("wrote", name)
