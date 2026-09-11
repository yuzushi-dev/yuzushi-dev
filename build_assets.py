#!/usr/bin/env python3
"""
build_assets.py — Deterministic Asset Generator for yuzushi-dev profile
Relic Interface System (RIS v2.8), Cyber Skin & Tactical HUD.

Zero dependencies (pure Python 3 standard library).
Generates:
  - assets/header.svg (830x230 hero banner with glitch & protocol telemetry)
  - assets/divider.svg (830x12 animated jump pulse separator)
  - assets/row-relic.svg (830x64 tactical listrow card, RLC, brain icon, .ris-rec, segmeter)
  - assets/row-amber.svg (830x64 tactical listrow card, AMB, database icon, segmeter)
  - assets/row-pas.svg (830x64 tactical listrow card, PAS, book icon, segmeter)
  - assets/row-ris.svg (830x64 tactical listrow card, RIS, dashboard icon, .ris-acquiring, segmeter)
  - assets/row-session-handoff.svg (830x64 tactical listrow card, HND, arrows-left-right, .ris-rec, segmeter)
  - assets/footer.svg (830x46 hex dump & signal meter)
  - README.md (tactical profile document with updated bio & repo links)
"""

import os
import sys
import xml.etree.ElementTree as ET
from html import escape

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")
README_PATH = os.path.join(SCRIPT_DIR, "README.md")

FONT_MONO = "'JetBrains Mono','Cascadia Code','Fira Code',Consolas,ui-monospace,monospace"
FONT_DISPLAY = "'Chakra Petch','JetBrains Mono','Cascadia Code',Consolas,ui-monospace,monospace"

# 132 unified 24x24 Tabler glyphs (MIT License, Paweł Kuna)
ICONS = {
    "brain": (
        '<path d="M15.5 13a3.5 3.5 0 0 0 -3.5 3.5v1a3.5 3.5 0 0 0 7 0v-1.8"/>'
        '<path d="M8.5 13a3.5 3.5 0 0 1 3.5 3.5v1a3.5 3.5 0 0 1 -7 0v-1.8"/>'
        '<path d="M17.5 16a3.5 3.5 0 0 0 0 -7h-.5"/>'
        '<path d="M19 9.3v-2.8a3.5 3.5 0 0 0 -7 0"/>'
        '<path d="M6.5 16a3.5 3.5 0 0 1 0 -7h.5"/>'
        '<path d="M5 9.3v-2.8a3.5 3.5 0 0 1 7 0v10"/>'
    ),
    "database": (
        '<path d="M4 6a8 3 0 1 0 16 0a8 3 0 1 0 -16 0"/>'
        '<path d="M4 6v6a8 3 0 0 0 16 0v-6"/>'
        '<path d="M4 12v6a8 3 0 0 0 16 0v-6"/>'
    ),
    "book": (
        '<path d="M3 19a9 9 0 0 1 9 0a9 9 0 0 1 9 0"/>'
        '<path d="M3 6a9 9 0 0 1 9 0a9 9 0 0 1 9 0"/>'
        '<path d="M3 6l0 13"/>'
        '<path d="M12 6l0 13"/>'
        '<path d="M21 6l0 13"/>'
    ),
    "dashboard": (
        '<path d="M5 4h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-6a1 1 0 0 1 1 -1"/>'
        '<path d="M5 16h4a1 1 0 0 1 1 1v2a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-2a1 1 0 0 1 1 -1"/>'
        '<path d="M15 12h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-6a1 1 0 0 1 1 -1"/>'
        '<path d="M15 4h4a1 1 0 0 1 1 1v2a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-2a1 1 0 0 1 1 -1"/>'
    ),
    "arrows-left-right": (
        '<path d="M17 10l4 0l-4 -4"/>'
        '<path d="M7 14l-4 0l4 4"/>'
        '<path d="M21 10l-18 0"/>'
        '<path d="M3 14l18 0"/>'
    ),
}

REPOS = [
    {
        "filename": "row-relic.svg",
        "callsign": "RLC",
        "title": "RELIC",
        "desc": "Longitudinal personality modeling for reflective agents. With provenance.",
        "tags": "PYTHON · GUMI RUNTIME · LIVE DEMO",
        "url": "https://github.com/yuzushi-dev/Relic",
        "icon": "brain",
        "beacon": "rec",
        "segmeter_level": 5,
        "alt": "Relic: longitudinal personality modeling for reflective agents. With provenance.",
    },
    {
        "filename": "row-amber.svg",
        "callsign": "AMB",
        "title": "AMBER",
        "desc": "Hybrid GraphRAG: Milvus vector search fused with Neo4j knowledge graph.",
        "tags": "GRAPH RAG · 5 RETRIEVAL MODES",
        "url": "https://github.com/yuzushi-dev/Amber",
        "icon": "database",
        "beacon": "idle",
        "segmeter_level": 4,
        "alt": "Amber: hybrid GraphRAG: Milvus vector search fused with Neo4j knowledge graph.",
    },
    {
        "filename": "row-pas.svg",
        "callsign": "PAS",
        "title": "PRIVATE AGENT SYSTEMS",
        "desc": "Official companion repo: book templates, source register & supplements.",
        "tags": "BOOK COMPANION · ARCHITECTURE",
        "url": "https://github.com/yuzushi-dev/Private-Agent-Systems",
        "icon": "book",
        "beacon": "idle",
        "segmeter_level": 5,
        "alt": "Private Agent Systems: official companion repo: book templates, source register & supplements.",
    },
    {
        "filename": "row-ris.svg",
        "callsign": "RIS",
        "title": "RELIC INTERFACE SYSTEM",
        "desc": "Brutalist tactical HUD & telemetry system: Web, React, Tailwind & Compose.",
        "tags": "v2.8.0 · DESIGN TOKENS · MIT",
        "url": "https://github.com/yuzushi-dev/relic-interface-system",
        "icon": "dashboard",
        "beacon": "acquiring",
        "segmeter_level": 5,
        "alt": "Relic Interface System: brutalist tactical HUD & telemetry system: Web, React, Tailwind & Compose.",
    },
    {
        "filename": "row-session-handoff.svg",
        "callsign": "HND",
        "title": "SESSION-HANDOFF",
        "desc": "Migrate active agent sessions & create handoffs: Claude Code & Codex.",
        "tags": "CLI & MCP · LOCAL-FIRST · RECOVERY",
        "url": "https://github.com/yuzushi-dev/session-handoff",
        "icon": "arrows-left-right",
        "beacon": "rec",
        "segmeter_level": 4,
        "alt": "session-handoff: migrate active agent sessions & create handoffs: Claude Code & Codex.",
    },
]

COMMON_DEFS = """<defs>
<radialGradient id="crimson" cx="0.5" cy="-0.12" r="1.1">
  <stop offset="0" stop-color="#ff003c" stop-opacity="0.20"/>
  <stop offset="0.6" stop-color="#ff003c" stop-opacity="0"/>
</radialGradient>
<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse">
  <rect y="2" width="4" height="1" fill="#ff003c" opacity="0.05"/>
</pattern>
<filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
  <feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope="0.05"/></feComponentTransfer>
  <feComposite operator="in" in2="SourceGraphic"/></filter>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
  <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#ff003c" flood-opacity="0.45"/>
</filter>
<filter id="glowC" x="-60%" y="-60%" width="220%" height="220%">
  <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#3df0ff" flood-opacity="0.55"/>
</filter>
<filter id="glowY" x="-60%" y="-60%" width="220%" height="220%">
  <feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#ffe23a" flood-opacity="0.5"/>
</filter>
</defs>"""

HEADER_STYLE = """<style>.boot{animation:boot .16s steps(2,end) both}.d1{animation-delay:.12s}.d2{animation-delay:.24s}.d3{animation-delay:.36s}.blink{animation:blink 1.1s steps(1,end) infinite}.gr{animation:gr 5s steps(1,end) infinite}.gc{animation:gc 5s steps(1,end) infinite}.tear{animation:tear 5s steps(1,end) infinite}.tear2{animation:tear2 5s steps(1,end) infinite}.jit{animation:jit 5s steps(1,end) infinite}.jump{animation:jump 4s steps(1,end) infinite}@keyframes boot{from{opacity:0}to{opacity:1}}@keyframes blink{0%,54%{opacity:1}55%,100%{opacity:0}}@keyframes gr{0%,37%{transform:none;opacity:0}38%{transform:translate(-4px,2px);opacity:.9}40%{transform:translate(3px,-1px);opacity:.85}42%,87%{transform:none;opacity:0}88%{transform:translate(5px,-2px);opacity:.9}90%{transform:translate(-3px,1px);opacity:.85}92%{transform:translate(2px,0);opacity:.6}93%,100%{transform:none;opacity:0}}@keyframes gc{0%,37%{transform:none;opacity:0}38%{transform:translate(4px,-2px);opacity:.9}40%{transform:translate(-3px,1px);opacity:.85}42%,87%{transform:none;opacity:0}88%{transform:translate(-5px,2px);opacity:.9}90%{transform:translate(3px,-1px);opacity:.85}92%{transform:translate(-2px,0);opacity:.6}93%,100%{transform:none;opacity:0}}@keyframes tear{0%,37%,42%,87%,93%,100%{transform:none;opacity:0}38%{transform:translateX(9px);opacity:1}40%{transform:translateX(-7px);opacity:1}88%{transform:translateX(-9px);opacity:1}91%{transform:translateX(8px);opacity:1}}@keyframes tear2{0%,39%,44%,89%,95%,100%{transform:none;opacity:0}40%{transform:translateX(-8px);opacity:1}42%{transform:translateX(6px);opacity:1}90%{transform:translateX(7px);opacity:1}93%{transform:translateX(-5px);opacity:1}}@keyframes jit{0%,38%,41%,88%,91%,100%{transform:none}39%{transform:translateX(3px)}89%{transform:translateX(-3px)}}@keyframes jump{0%,55%,100%{transform:none}56%,71%{transform:translateX(180px)}72%,88%{transform:translateX(-140px)}89%{transform:translateX(40px)}}@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>"""

DIVIDER_STYLE = """<style>.jump{animation:jump 4s steps(1,end) infinite}@keyframes jump{0%,55%,100%{transform:none}56%,71%{transform:translateX(180px)}72%,88%{transform:translateX(-140px)}89%{transform:translateX(40px)}}@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>"""

FOOTER_STYLE = """<style>@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>"""


def build_header_svg() -> str:
    """Hero banner with glitch animations, protocol stamps, and telemetry."""
    left_ticks = "".join(
        f'<rect x="10" y="{y}" width="6" height="1" fill="#8f1f30" opacity="0.6"/>'
        for y in range(34, 215, 7)
    )
    right_ticks = "".join(
        f'<rect x="814" y="{y}" width="6" height="1" fill="#8f1f30" opacity="0.6"/>'
        for y in range(34, 215, 13)
    )

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 230" width="830" height="230" role="img" aria-label="yuzushi — private agent systems: memory, governance, provenance">'
        + HEADER_STYLE
        + COMMON_DEFS
        + '<clipPath id="frame"><polygon points="0,0 814,0 830,16 830,230 16,230 0,214"/></clipPath>'
        + '<polygon points="0.5,0.5 814,0.5 829.5,16 829.5,229.5 16,229.5 0.5,214" fill="#0a0608" stroke="#6e2d38" stroke-width="1"/>'
        + '<g clip-path="url(#frame)">'
        + '<rect width="830" height="230" fill="url(#crimson)"/>'
        + '<rect width="830" height="230" fill="url(#scan)"/>'
        + '<rect width="830" height="230" fill="#808080" filter="url(#noise)"/>'
        + '<rect x="1" y="1" width="812" height="1.5" fill="#ff003c" filter="url(#glow)"/>'
        + '</g>'
        + '<path d="M3,11 V3 H11" stroke="#ff003c" stroke-width="1.5" fill="none" filter="url(#glow)"/>'
        + '<path d="M819,3 H827 V11" stroke="#ff003c" stroke-width="1.5" fill="none" filter="url(#glow)"/>'
        + '<path d="M827,219 V227 H819" stroke="#ff003c" stroke-width="1.5" fill="none" filter="url(#glow)"/>'
        + '<path d="M11,227 H3 V219" stroke="#ff003c" stroke-width="1.5" fill="none" filter="url(#glow)"/>'
        + left_ticks
        + right_ticks
        + f'<text x="28" y="32" font-family="{FONT_MONO}" font-size="9" fill="#8f1f30" letter-spacing="2" text-anchor="start" font-weight="500" class="boot">PROTOCOL 6520-A44 <tspan fill="#ff4d62">//</tspan> TRN_YZSH_8D0095</text>'
        + f'<text x="800" y="32" font-family="{FONT_MONO}" font-size="9" fill="#8f1f30" letter-spacing="2" text-anchor="end" font-weight="500" class="boot">ACCESS: PUBLIC</text>'
        + f'<g transform="rotate(90 794 60)"><text x="794" y="60" font-family="{FONT_MONO}" font-size="8.5" fill="#1f8a99" letter-spacing="1.5" text-anchor="start" font-weight="500" opacity="0.6">1001 0110 1101 0010</text></g>'
        + f'<text x="258" y="122" font-family="{FONT_DISPLAY}" font-size="46" fill="#ff003c" letter-spacing="14" text-anchor="start" font-weight="700" class="gr" opacity="0">YUZUSHI</text>'
        + f'<text x="258" y="122" font-family="{FONT_DISPLAY}" font-size="46" fill="#3df0ff" letter-spacing="14" text-anchor="start" font-weight="700" class="gc" opacity="0">YUZUSHI</text>'
        + f'<g class="boot d1"><text x="258" y="122" font-family="{FONT_DISPLAY}" font-size="46" fill="#f3eef0" letter-spacing="14" text-anchor="start" font-weight="700">YUZUSHI</text></g>'
        + '<clipPath id="slice"><rect x="0" y="98" width="830" height="11"/></clipPath>'
        + '<clipPath id="slice2"><rect x="0" y="112" width="830" height="7"/></clipPath>'
        + f'<g clip-path="url(#slice)" class="tear" opacity="0"><text x="258" y="122" font-family="{FONT_DISPLAY}" font-size="46" fill="#f3eef0" letter-spacing="14" text-anchor="start" font-weight="700">YUZUSHI</text></g>'
        + f'<g clip-path="url(#slice2)" class="tear2" opacity="0"><text x="258" y="122" font-family="{FONT_DISPLAY}" font-size="46" fill="#f3eef0" letter-spacing="14" text-anchor="start" font-weight="700">YUZUSHI</text></g>'
        + '<rect x="541.2" y="86" width="18" height="38" fill="#ffe23a" filter="url(#glowY)" class="blink"/>'
        + f'<g class="jit"><text x="415.0" y="156" font-family="{FONT_MONO}" font-size="13" fill="#3df0ff" letter-spacing="6" text-anchor="middle" font-weight="600" class="boot d2">PRIVATE AGENT SYSTEMS</text></g>'
        + f'<text x="415.0" y="180" font-family="{FONT_MONO}" font-size="10" fill="#b09aa0" letter-spacing="3" text-anchor="middle" font-weight="500" class="boot d3">MEMORY · GOVERNANCE · PROVENANCE · LOCAL-FIRST</text>'
        + f'<text x="28" y="212" font-family="{FONT_MONO}" font-size="9" fill="#8f1f30" letter-spacing="2" text-anchor="start" font-weight="500">SYS.CHECK: OK | SKIN: CYBER</text>'
        + f'<text x="800" y="212" font-family="{FONT_MONO}" font-size="9" fill="#8f1f30" letter-spacing="2" text-anchor="end" font-weight="500">NODE: GITHUB // UPLINK: STABLE</text>'
        + '</svg>'
    )


def build_divider_svg() -> str:
    """Animated neon pulse divider."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 12" width="830" height="12" role="img" aria-label="section divider">'
        + DIVIDER_STYLE
        + '<rect x="0" y="6" width="830" height="1" fill="#6e2d38"/>'
        + '<g class="jump"><rect x="290" y="5" width="90" height="3" fill="#ff003c" filter="url(#glow)"/></g>'
        + COMMON_DEFS
        + '</svg>'
    )


def build_footer_svg() -> str:
    """Chamfered terminal footer card with hex dump and signal meter."""
    signal_bars = []
    for idx in range(12):
        bx = 690 + idx * 9
        fill_color = "#34f08c" if idx < 9 else "#241318"
        signal_bars.append(f'<rect x="{bx}" y="20" width="7" height="8" fill="{fill_color}"/>')
    sig_svg = "".join(signal_bars)

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 46" width="830" height="46" role="img" aria-label="end of transmission">'
        + FOOTER_STYLE
        + COMMON_DEFS
        + '<polygon points="0.5,0.5 822,0.5 829.5,8 829.5,45.5 8,45.5 0.5,38" fill="#0a0608" stroke="#6e2d38" stroke-width="1"/>'
        + f'<text x="20" y="28" font-family="{FONT_MONO}" font-size="9" fill="#8f1f30" letter-spacing="1.5" text-anchor="start" font-weight="500">0x00 79 75 7A 75 73 68 69</text>'
        + f'<text x="415.0" y="28" font-family="{FONT_MONO}" font-size="9" fill="#b09aa0" letter-spacing="3" text-anchor="middle" font-weight="500">// END OF TRANSMISSION //</text>'
        + f'<text x="682" y="28" font-family="{FONT_MONO}" font-size="9" fill="#b09aa0" letter-spacing="2" text-anchor="end" font-weight="500">SIG</text>'
        + sig_svg
        + '</svg>'
    )


def build_row_svg(repo: dict, index: int, total_rows: int = 5) -> str:
    """
    Builds an 830x64 tactical listrow card adhering to RIS v2.8 geometry:
    - 45° chamfered polygon container with 1px structural stroke
    - Staggered scan cycle (10s period, each row active for 20%)
    - Embedded Tabler 24x24 icon & callsign plate
    - Telemetry status beacon (.ris-rec or .ris-acquiring)
    - 5-bar discrete segmented energy meter (.ris-segmeter)
    - Fully accessible motion fallback under prefers-reduced-motion
    """
    cycle_time = 10.0
    slice_pct = 100.0 / total_rows
    start_pct = index * slice_pct
    end_pct = (index + 1) * slice_pct

    is_first = (index == 0)

    # Initial static attributes (matches frame 0)
    init_card_fill = "#ff003c" if is_first else "#120a0d"
    init_card_stroke = "#ff003c" if is_first else "#6e2d38"
    init_card_glow = "1" if is_first else "0"
    init_th_fill = "#0a0608" if is_first else "#241318"
    init_th_stroke = "#ff003c" if is_first else "#6e2d38"
    init_title_fill = "#0a0608" if is_first else "#3df0ff"
    init_desc_fill = "#0a0608" if is_first else "#c8b9bd"
    init_tag_fill = "#0a0608" if is_first else "#ff4d62"

    # Staggered scan cycle keyframes
    if is_first:
        kbg = f"0%{{fill:#ff003c;stroke:#ff003c}}{end_pct:.1f}%{{fill:#120a0d;stroke:#6e2d38}}100%{{fill:#120a0d;stroke:#6e2d38}}"
        kglow = f"0%{{opacity:1}}{end_pct:.1f}%{{opacity:0}}100%{{opacity:0}}"
        kti = f"0%{{fill:#0a0608}}{end_pct:.1f}%{{fill:#3df0ff}}100%{{fill:#3df0ff}}"
        kde = f"0%{{fill:#0a0608}}{end_pct:.1f}%{{fill:#c8b9bd}}100%{{fill:#c8b9bd}}"
        kme = f"0%{{fill:#0a0608}}{end_pct:.1f}%{{fill:#ff4d62}}100%{{fill:#ff4d62}}"
        kth = f"0%{{fill:#0a0608;stroke:#ff003c}}{end_pct:.1f}%{{fill:#241318;stroke:#6e2d38}}100%{{fill:#241318;stroke:#6e2d38}}"
    else:
        kbg = f"0%{{fill:#120a0d;stroke:#6e2d38}}{start_pct:.1f}%{{fill:#ff003c;stroke:#ff003c}}{end_pct:.1f}%{{fill:#120a0d;stroke:#6e2d38}}100%{{fill:#120a0d;stroke:#6e2d38}}"
        kglow = f"0%{{opacity:0}}{start_pct:.1f}%{{opacity:1}}{end_pct:.1f}%{{opacity:0}}100%{{opacity:0}}"
        kti = f"0%{{fill:#3df0ff}}{start_pct:.1f}%{{fill:#0a0608}}{end_pct:.1f}%{{fill:#3df0ff}}100%{{fill:#3df0ff}}"
        kde = f"0%{{fill:#c8b9bd}}{start_pct:.1f}%{{fill:#0a0608}}{end_pct:.1f}%{{fill:#c8b9bd}}100%{{fill:#c8b9bd}}"
        kme = f"0%{{fill:#ff4d62}}{start_pct:.1f}%{{fill:#0a0608}}{end_pct:.1f}%{{fill:#ff4d62}}100%{{fill:#ff4d62}}"
        kth = f"0%{{fill:#241318;stroke:#6e2d38}}{start_pct:.1f}%{{fill:#0a0608;stroke:#ff003c}}{end_pct:.1f}%{{fill:#241318;stroke:#6e2d38}}100%{{fill:#241318;stroke:#6e2d38}}"

    # Beacon styles & markup
    beacon_type = repo.get("beacon", "idle")
    beacon_css = ""
    beacon_svg = ""

    if beacon_type == "rec":
        beacon_css = "@keyframes ris-rec{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.3;transform:scale(0.85)}}.ris-rec{animation:ris-rec 1.4s ease-in-out infinite;transform-origin:114px 22px}"
        beacon_svg = '<circle class="ris-rec" cx="114" cy="22" r="3.5" fill="#ff003c" filter="url(#glow)"/>'
    elif beacon_type == "acquiring":
        beacon_css = "@keyframes ris-acq{0%,100%{opacity:1;transform:scale(1.15)}50%{opacity:0.35;transform:scale(0.85)}}.ris-acq{animation:ris-acq 2.2s ease-in-out infinite;transform-origin:114px 22px}@keyframes ris-acq-glow{0%,100%{stroke-opacity:0.75}50%{stroke-opacity:0.2}}.racq-border{animation:ris-acq-glow 2.2s ease-in-out infinite}"
        beacon_svg = '<circle class="ris-acq" cx="114" cy="22" r="3.5" fill="#3df0ff" filter="url(#glowC)"/>'
    else:
        beacon_svg = '<circle cx="114" cy="22" r="2" fill="#6e2d38"/>'

    # Segmeter markup (5 discrete LED bars at x=760..802, y=20, h=8)
    seg_level = repo.get("segmeter_level", 5)
    segmeter_bars = []
    seg_active_color = "#3df0ff" if beacon_type == "acquiring" else "#34f08c"
    for b_idx in range(5):
        bx = 760 + b_idx * 9
        b_color = seg_active_color if b_idx < seg_level else "#241318"
        segmeter_bars.append(f'<rect x="{bx}" y="20" width="6" height="8" fill="{b_color}"/>')
    segmeter_svg = f'<g role="meter" aria-label="System status" aria-valuenow="{seg_level}" aria-valuemin="0" aria-valuemax="5">{"".join(segmeter_bars)}</g>'


    # Extra breathing cyan border for RIS
    ris_extra_border = ""
    if beacon_type == "acquiring":
        ris_extra_border = '<polygon class="racq-border" points="0.5,0.5 822,0.5 829.5,8 829.5,63.5 8,63.5 0.5,56" fill="none" stroke="#3df0ff" stroke-width="1" filter="url(#glowC)" opacity="0.6"/>'

    escaped_title = escape(repo["title"])
    escaped_desc = escape(repo["desc"])
    escaped_tags = escape(repo["tags"])
    escaped_callsign = escape(repo["callsign"])
    aria_label = escape(f"{repo['title']} — {repo['desc']}")

    row_style = (
        f'<style>'
        f'.rbg{{animation:kbg {cycle_time:.0f}s steps(1,end) infinite}}'
        f'.rglow{{animation:kglow {cycle_time:.0f}s steps(1,end) infinite}}'
        f'.rti{{animation:kti {cycle_time:.0f}s steps(1,end) infinite}}'
        f'.rde{{animation:kde {cycle_time:.0f}s steps(1,end) infinite}}'
        f'.rme{{animation:kme {cycle_time:.0f}s steps(1,end) infinite}}'
        f'.rth{{animation:kth {cycle_time:.0f}s steps(1,end) infinite}}'
        f'@keyframes kbg{{{kbg}}}'
        f'@keyframes kglow{{{kglow}}}'
        f'@keyframes kti{{{kti}}}'
        f'@keyframes kde{{{kde}}}'
        f'@keyframes kme{{{kme}}}'
        f'@keyframes kth{{{kth}}}'
        f'{beacon_css}'
        f'@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}'
        f'</style>'
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 64" width="830" height="64" role="img" aria-label="{aria_label}">'
        + row_style
        + COMMON_DEFS
        + f'<polygon class="rbg" points="0.5,0.5 822,0.5 829.5,8 829.5,63.5 8,63.5 0.5,56" fill="{init_card_fill}" stroke="{init_card_stroke}" stroke-width="1"/>'
        + f'<polygon class="rglow" points="0.5,0.5 822,0.5 829.5,8 829.5,63.5 8,63.5 0.5,56" fill="none" stroke="#ff003c" stroke-width="1" filter="url(#glow)" opacity="{init_card_glow}"/>'
        + ris_extra_border
        + '<clipPath id="rc"><polygon points="0,0 822,0 830,8 830,64 8,64 0,56"/></clipPath>'
        + '<g clip-path="url(#rc)"><rect width="830" height="64" fill="url(#scan)"/></g>'
        + f'<rect class="rth" x="10" y="9" width="84" height="46" fill="{init_th_fill}" stroke="{init_th_stroke}" stroke-width="1"/>'
        + '<path d="M12,17 V11 H18 M86,53 H92 V47" stroke="#ff4d62" stroke-width="1" fill="none" opacity="0.8"/>'
        + f'<text x="52" y="38" font-family="{FONT_MONO}" font-size="15" fill="#ff4d62" letter-spacing="3" text-anchor="middle" font-weight="700">{escaped_callsign}</text>'
        + beacon_svg
        + f'<text x="126" y="27" font-family="{FONT_MONO}" font-size="14.5" fill="{init_title_fill}" letter-spacing="2" text-anchor="start" font-weight="700" class="rti">{escaped_title}</text>'
        + f'<text x="126" y="47" font-family="{FONT_MONO}" font-size="11" fill="{init_desc_fill}" letter-spacing="0.2" text-anchor="start" font-weight="500" class="rde">{escaped_desc}</text>'
        + f'<text x="748" y="27" font-family="{FONT_MONO}" font-size="9.5" fill="{init_tag_fill}" letter-spacing="1.5" text-anchor="end" font-weight="600" class="rme">{escaped_tags}</text>'
        + segmeter_svg
        + '</svg>'
    )


def build_readme_md(repos: list) -> str:
    """Assembles profile README.md referencing generated rows and updated bio."""
    rows_markup = []
    for r in repos:
        rows_markup.append(
            f'  <a href="{r["url"]}"><img src="assets/{r["filename"]}" width="830" alt="{escape(r["alt"])}"></a>'
        )
    rows_joined = "\n".join(rows_markup)

    return f"""<!-- assets generated by build_assets.py (Relic Interface System, skin cyber) -->
<div align="center">
  <img src="assets/header.svg" width="830" alt="yuzushi: private agent systems. Memory, governance, provenance, local-first.">
</div>

**I build private agent systems.** The model is the easy part; my work is the harness around it: memory that survives the session, retrieval that cites its sources, and governance you can actually inspect. Local-first where the data is personal, cloud where it isn't.

The book, [*Private Agent Systems*](https://www.amazon.com/dp/B0H4RQMJG3), is out on Amazon. It treats agents as production software, not prompt experiments. The code is here: **Relic** models who you are over time, so a reflective agent can carry your context forward without pretending to be you, while **Amber** answers over large document collections by fusing vector search with knowledge-graph reasoning. **Relic Interface System** provides the brutalist tactical HUD and telemetry design system, and **session-handoff** migrates active agent sessions between Claude Code and Codex.

<div align="center">
  <img src="assets/divider.svg" width="830" alt="">
</div>

<div align="center">
{rows_joined}
</div>

<div align="center">
  <a href="https://www.amazon.com/dp/B0H4RQMJG3"><img src="https://img.shields.io/badge/BOOK-Private_Agent_Systems-ff003c?style=flat-square&amp;labelColor=120a0d" alt="Private Agent Systems on Amazon"></a>
  <a href="https://yuzushi-dev.github.io/Relic/"><img src="https://img.shields.io/badge/LIVE-Relic_demo-00e5ff?style=flat-square&amp;labelColor=120a0d" alt="Relic live demo"></a>
  <a href="https://github.com/yuzushi-dev/Relic/stargazers"><img src="https://img.shields.io/github/stars/yuzushi-dev/Relic?style=flat-square&amp;label=RELIC&amp;color=ffe23a&amp;labelColor=120a0d" alt="Relic stars"></a>
  <a href="https://github.com/yuzushi-dev/relic-interface-system"><img src="https://img.shields.io/badge/HUD-RIS_v2.8.0-3df0ff?style=flat-square&amp;labelColor=120a0d" alt="Relic Interface System"></a>
</div>

<div align="center">
  <img src="assets/footer.svg" width="830" alt="end of transmission">
</div>
"""


def validate_xml(content: str, label: str) -> None:
    """Verifies that the SVG string parses as valid XML without errors."""
    try:
        ET.fromstring(content)
    except ET.ParseError as e:
        print(f"[ERROR] XML parse error in {label}: {e}", file=sys.stderr)
        raise


def main() -> None:
    os.makedirs(ASSETS_DIR, exist_ok=True)

    # Clean up obsolete legacy rows
    legacy_files = ["row-whispir.svg", "row-nfc-gate.svg"]
    for legacy in legacy_files:
        legacy_path = os.path.join(ASSETS_DIR, legacy)
        if os.path.exists(legacy_path):
            os.remove(legacy_path)
            print(f"Removed legacy asset: {legacy}")

    # 1. Header
    header_svg = build_header_svg()
    validate_xml(header_svg, "assets/header.svg")
    header_path = os.path.join(ASSETS_DIR, "header.svg")
    with open(header_path, "w", encoding="utf-8") as f:
        f.write(header_svg)
    print(f"Generated: {header_path} ({len(header_svg)} bytes)")

    # 2. Divider
    divider_svg = build_divider_svg()
    validate_xml(divider_svg, "assets/divider.svg")
    divider_path = os.path.join(ASSETS_DIR, "divider.svg")
    with open(divider_path, "w", encoding="utf-8") as f:
        f.write(divider_svg)
    print(f"Generated: {divider_path} ({len(divider_svg)} bytes)")

    # 3. Tactical Listrow Cards (5 repositories)
    for idx, repo in enumerate(REPOS):
        row_svg = build_row_svg(repo, idx, total_rows=len(REPOS))
        validate_xml(row_svg, f"assets/{repo['filename']}")
        row_path = os.path.join(ASSETS_DIR, repo["filename"])
        with open(row_path, "w", encoding="utf-8") as f:
            f.write(row_svg)
        print(f"Generated: {row_path} ({len(row_svg)} bytes)")

    # 4. Footer
    footer_svg = build_footer_svg()
    validate_xml(footer_svg, "assets/footer.svg")
    footer_path = os.path.join(ASSETS_DIR, "footer.svg")
    with open(footer_path, "w", encoding="utf-8") as f:
        f.write(footer_svg)
    print(f"Generated: {footer_path} ({len(footer_svg)} bytes)")

    # 5. Profile README.md
    readme_content = build_readme_md(REPOS)
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"Generated: {README_PATH} ({len(readme_content)} bytes)")

    print("\n[SUCCESS] All assets and README.md generated deterministically.")


if __name__ == "__main__":
    main()
