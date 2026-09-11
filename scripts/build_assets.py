#!/usr/bin/env python3
"""Generate the SVG assets for the GitHub profile README in the Harbor design
system (the same tokens as admin.kulyaev.tech: sky-700 primary, OKLCH-ish
neutrals, hairline borders, radius 4, dark sidebar). Pure Python, no deps.

    python3 scripts/build_assets.py            # writes assets/*.svg
    python3 scripts/build_assets.py --preview  # also writes /tmp preview.html

GitHub serves README images through its camo proxy: no external fonts, no
scripts, but inline <style> with CSS animations works - that is what the
status pulse uses. Every text uses a font stack that degrades to the viewer's
system sans, so the layout never depends on Golos Text being installed.
"""
from __future__ import annotations

import html
import os
import sys

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

# ── Harbor tokens (frontend/src/theme/harbor.ts) ─────────────────────────────
PRIMARY = "#0369A1"
PRIMARY_INK = "#0C4A6E"
PRIMARY_SOFT = "#F0F9FF"
GROUND = "#F7FBFC"
SURFACE = "#FFFFFF"
SURFACE2 = "#EDF3F4"
SURFACE3 = "#DCE3E4"
TEXT = "#0F1516"
TEXT2 = "#869294"
TEXT3 = "#A9B3B5"
LINE = "#DCE3E4"
GOOD = "#0D9488"
WARN = "#D97706"
BAD = "#E11D48"
SIDE_BG = "#0F1E24"
SIDE_TEXT = "#B7C0D3"
VIZ = ["#0284C7", "#14B8A6", "#818CF8", "#F59E0B", "#F43F5E", "#10B981"]

UI = "'Golos Text','Inter','Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,monospace"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def svg(w: int, h: int, body: str, style: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="{UI}">\n<style>{style}</style>\n{body}\n</svg>\n'
    )


def write(name: str, content: str) -> None:
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", os.path.relpath(path))


# ── 1. Banner: the meme stays, the chrome is Harbor ───────────────────────────
def banner() -> str:
    w, h = 1200, 300
    style = f"""
    .h1 {{ font-size: 46px; font-weight: 700; fill: #fff; letter-spacing: -0.02em; }}
    .h2 {{ font-size: 46px; font-weight: 700; fill: {VIZ[0]}; letter-spacing: -0.02em; }}
    .sub {{ font-size: 16px; fill: {SIDE_TEXT}; }}
    .mono {{ font-family: {MONO}; font-size: 13px; fill: {SIDE_TEXT}; }}
    .pill {{ font-size: 12px; font-weight: 500; fill: #fff; }}
    .dot {{ animation: pulse 2s ease-in-out infinite; transform-origin: center; }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
    .grid line {{ stroke: rgba(255,255,255,.06); stroke-width: 1; }}
    .cursor {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    """
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w, 40))
    grid += "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h, 40))
    body = f"""
    <rect width="{w}" height="{h}" fill="{SIDE_BG}"/>
    <g class="grid">{grid}</g>
    <rect x="0" y="0" width="{w}" height="3" fill="{PRIMARY}"/>
    <rect x="56" y="58" width="44" height="44" rx="4" fill="{PRIMARY}"/>
    <text x="78" y="89" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">K</text>
    <text x="118" y="92" class="h1">Hello There 👋</text>
    <text x="118" y="146" class="h2">General Kenobi !<tspan class="cursor" fill="{VIZ[0]}">_</tspan></text>
    <text x="118" y="192" class="sub">Ivan Kulyaev · Senior Software Engineer</text>
    <text x="118" y="222" class="mono">React / Next.js / TypeScript / Node.js / NestJS / Express</text>
    <g transform="translate(944,60)">
      <rect x="0" y="0" width="200" height="30" rx="15" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.14)"/>
      <circle class="dot" cx="18" cy="15" r="4" fill="{GOOD}"/>
      <text x="32" y="19" class="pill">based in Vietnam</text>
    </g>
    <g transform="translate(944,102)">
      <rect x="0" y="0" width="200" height="30" rx="15" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.14)"/>
      <circle cx="18" cy="15" r="4" fill="{VIZ[2]}"/>
      <text x="32" y="19" class="pill">open to remote roles</text>
    </g>
    """
    return svg(w, h, body, style)


# ── 2. KPI tiles (kui-kpi) ────────────────────────────────────────────────────
TILES = [
    ("years in dev", "5.5", "since 2021", PRIMARY_INK),
    ("live products", "6", "bots · PWA · sites", GOOD),
    ("stack", "TS · Node", "React / Next.js / NestJS", TEXT),
    ("cats", "2", "Arnold & Sebastian", TEXT),
    ("Star Wars fan", "18 yrs", "hence the greeting", WARN),
]


def tiles() -> str:
    w, h = 1200, 118
    n = len(TILES)
    gap = 12
    tw = (w - gap * (n - 1)) / n
    style = f"""
    .l {{ font-size: 11px; font-weight: 600; letter-spacing: .06em; fill: {TEXT2}; text-transform: uppercase; }}
    .v {{ font-size: 28px; font-weight: 700; letter-spacing: -0.02em; }}
    .d {{ font-size: 12px; fill: {TEXT2}; }}
    """
    body = ""  # transparent: sits on GitHub's light OR dark page background
    for i, (label, value, note, color) in enumerate(TILES):
        x = i * (tw + gap)
        body += f"""
        <g transform="translate({x:.1f},0)">
          <rect x="0.5" y="0.5" width="{tw - 1:.1f}" height="{h - 1}" rx="6" fill="{SURFACE}" stroke="{LINE}"/>
          <text x="16" y="30" class="l">{esc(label.upper())}</text>
          <text x="16" y="70" class="v" fill="{color}">{esc(value)}</text>
          <text x="16" y="96" class="d">{esc(note)}</text>
        </g>"""
    return svg(w, h, body, style)


# ── 3. Stack carousel (kui-pill chips, CSS marquee) ──────────────────────────
# The list mirrors memory/cv/ivan-cv-en.md "Skills" - keep them in sync.
STACK = [
    ("TypeScript", VIZ[0]), ("JavaScript", VIZ[3]), ("React 18", VIZ[0]), ("Next.js", TEXT),
    ("Redux Toolkit", VIZ[2]), ("RTK Query", VIZ[2]), ("Node.js", VIZ[5]), ("NestJS", VIZ[4]),
    ("Express", TEXT), ("REST", VIZ[1]), ("GraphQL", VIZ[4]), ("PostgreSQL", VIZ[2]),
    ("TypeORM", VIZ[2]), ("Keycloak · OAuth2 / OIDC", VIZ[3]), ("Docker", VIZ[0]), ("CI/CD", VIZ[1]),
    ("nginx", VIZ[5]), ("Grafana · Faro", VIZ[3]), ("Feature-Sliced Design", VIZ[0]),
    ("e2e · unit tests", VIZ[1]), ("SQL", VIZ[2]), ("React Native", VIZ[0]),
]


def stack() -> str:
    """One row of chips that scrolls forever (marquee). The row is drawn twice
    back to back and translated by exactly one row width, so the loop is
    seamless. Hover pauses it."""
    w, row_h, pad = 1200, 36, 12
    chips, x = [], 0
    for name, color in STACK:
        cw = int(len(name) * 7.6) + 42
        chips.append((x, cw, name, color))
        x += cw + pad
    row_w = x
    dur = max(20, int(row_w / 40))  # ~40 px/s
    style = f"""
    .t {{ font-size: 13px; font-weight: 500; fill: {TEXT}; }}
    .track {{ animation: slide {dur}s linear infinite; }}
    svg:hover .track {{ animation-play-state: paused; }}
    @keyframes slide {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{row_w}px); }} }}
    """
    def row(offset: int) -> str:
        out = []
        for cx, cw, name, color in chips:
            out.append(f"""
        <g transform="translate({cx + offset},0)">
          <rect x="0.5" y="0.5" width="{cw - 1}" height="{row_h - 1}" rx="{row_h / 2}" fill="{SURFACE}" stroke="{LINE}"/>
          <circle cx="17" cy="{row_h / 2}" r="4" fill="{color}"/>
          <text x="30" y="{row_h / 2 + 5}" class="t">{esc(name)}</text>
        </g>""")
        return "".join(out)
    fade = f"""
    <defs><linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="fr" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient></defs>"""
    body = f'<g class="track">{row(0)}{row(row_w)}</g><rect x="0" y="0" width="48" height="{row_h}" fill="url(#fl)" opacity=".9"/><rect x="{w - 48}" y="0" width="48" height="{row_h}" fill="url(#fr)" opacity=".9"/>'
    return svg(w, row_h, fade + body, style)


# ── 4. Product cards (one SVG each so markdown can link them) ─────────────────
PRODUCTS = [
    ("sumlify-web", "Sumlify · web", "sumlify.pro: landing + MiniApp for shared budgets - Next.js, Ant Design, Yandex.Metrika funnels, SEO articles.", "sumlify.pro", "live", GOOD),
    ("sumlify-bot", "@sumlify_bot", "The Telegram bot behind Sumlify: log a spend in one message, LLM categorisation, family mode, Platega payments.", "t.me/sumlify_bot", "live", GOOD),
    ("channel", "@ivan_kulyaev", "Telegram channel: frontend, career moves, relocation, building products with AI agents. In Russian.", "t.me/ivan_kulyaev", "posting", WARN),
]


def card(key: str, name: str, desc: str, url: str, status: str, color: str) -> str:
    w, h = 384, 156
    style = f"""
    .n {{ font-size: 18px; font-weight: 700; fill: {TEXT}; letter-spacing: -0.01em; }}
    .d {{ font-size: 12.5px; fill: {TEXT2}; }}
    .u {{ font-family: {MONO}; font-size: 12px; fill: {PRIMARY}; }}
    .s {{ font-size: 11px; font-weight: 500; fill: {TEXT}; }}
    """
    # naive word wrap for the description (SVG has no text flow)
    words, lines, cur = desc.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > 52:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    lines.append(cur)
    desc_svg = "".join(f'<text x="20" y="{64 + i * 17}" class="d">{esc(l)}</text>' for i, l in enumerate(lines[:3]))
    sw = len(status) * 7 + 26
    # The accent bar is clipped by the card's rounded outline, otherwise its
    # square corners poke out of the radius (Ivan's dark-mode screenshot, 11.09).
    body = f"""
    <defs><clipPath id="c{key}"><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="6"/></clipPath></defs>
    <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="6" fill="{SURFACE}" stroke="{LINE}"/>
    <rect x="0" y="0" width="5" height="{h}" fill="{PRIMARY}" clip-path="url(#c{key})"/>
    <text x="20" y="36" class="n">{esc(name)}</text>
    <g transform="translate({w - sw - 16},20)">
      <rect x="0.5" y="0.5" width="{sw - 1}" height="23" rx="12" fill="{SURFACE2}" stroke="{LINE}"/>
      <circle cx="12" cy="12" r="3.5" fill="{color}"/>
      <text x="21" y="16" class="s">{esc(status)}</text>
    </g>
    {desc_svg}
    <text x="20" y="{h - 18}" class="u">↗ {esc(url)}</text>
    """
    return svg(w, h, body, style)


def preview() -> None:
    """A GitHub-ish page with the README pieces, for a headless screenshot."""
    cards = "".join(
        f'<a href="#"><img src="assets/card-{k}.svg" width="384"></a>' for k, *_ in PRODUCTS
    )
    page = f"""<!doctype html><meta charset="utf-8"><title>profile preview</title>
    <style>body{{margin:0;background:#fff;font-family:{UI};color:#1f2328}} .wrap{{max-width:1012px;margin:32px auto;padding:0 32px}}
    img{{max-width:100%}} h2{{font-size:20px;border-bottom:1px solid #d1d9e0;padding-bottom:6px;margin:28px 0 12px}}
    .cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}} .cards img{{width:100%}}
    .gifs{{display:flex;gap:12px;margin:12px 0}} .gifs div{{width:300px;height:175px;background:#eee;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#888}}
    p{{font-size:15px;line-height:1.5}}</style>
    <div class="wrap">
    <img src="assets/banner.svg" width="1200">
    <img src="assets/hello-there.gif" width="1200">
    <img src="assets/tiles.svg" width="1200">
    <h2>What I build</h2><div class="cards">{cards}</div>
    <h2>Stack</h2><img src="assets/stack.svg" width="1200">
    <h2>Contact</h2><p>Telegram: @takemeright · channel @ivan_kulyaev</p>
    </div>"""
    with open(os.path.join(OUT, "..", "preview.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote preview.html")


if __name__ == "__main__":
    write("banner.svg", banner())
    write("tiles.svg", tiles())
    write("stack.svg", stack())
    for key, name, desc, url, status, color in PRODUCTS:
        write(f"card-{key}.svg", card(key, name, desc, url, status, color))
    if "--preview" in sys.argv:
        preview()
