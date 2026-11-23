#!/usr/bin/env python3
"""Writes the Workshop covers as SVG into covers/src/. Original geometry only, generic
fonts, and no name, mark or colours of anybody else: a pack of somebody else's skills is
named for what it does. The covers of web-builder-skills, dev-workflow-skills and
gpu-computing-skills are not rendered yet (the maintainer draws them); until covers/ has
them, they are listed without a cover and shown with the plain placeholder. The packs of
pinned/ get generated ones here: a generic title and shape, no mark of their authors.

A connector's cover names what the service is for ("Issues & cycles"), never the service:
the card already says which one it is, and its name, mark and colours are not ours to draw.

    scripts/make-covers.py && scripts/render-covers.sh
"""

import pathlib
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "covers" / "src"
W, H = 1200, 630
BG, INK, MUTED = "#0c0e13", "#f4f5f7", "#8a90a0"

# name: (title, small label, accent, shape)
COVERS = {
    "duskcode-engineering": ("Engineering", "SKILL PACK / DUSKCODE", "#f5a524", "stairs"),
    "duskcode-security": ("Security", "SKILL PACK / DUSKCODE", "#ff4d6d", "shield"),
    "duskcode-agents": ("Agents", "AGENT PACK / DUSKCODE", "#9b8cff", "orbit"),
    "ios-simulator": ("Device Simulator", "PLUGIN / DEVICES", "#38bdf8", "phone"),
    "vphone": ("Virtual Phone", "PLUGIN / DEVICES", "#e879f9", "phone2"),
    "telegram": ("Chat Bridge", "PLUGIN / CHAT", "#60a5fa", "bubbles"),
    # Packs pinned in their authors' repositories (pinned/): named for what they do.
    "office-document-skills": ("Documents", "SKILL PACK / PINNED", "#34d399", "slabs"),
    "visual-design-skills": ("Visual Design", "SKILL PACK / PINNED", "#f472b6", "rings"),
    "communication-skills": ("Comms", "SKILL PACK / PINNED", "#60a5fa", "bubbles"),
    "hosting-deploy-skills": ("Deploy", "SKILL PACK / PINNED", "#22d3ee", "stairs"),
    "team-workspace-skills": ("Workspace", "SKILL PACK / PINNED", "#a3e635", "slabs"),
    "dotnet-app-skills": ("Web & Desktop", "SKILL PACK / PINNED", "#a78bfa", "arches"),
    "speech-audio-skills": ("Speech", "SKILL PACK / PINNED", "#fb923c", "rings"),
    "repository-utility-skills": ("Repo Tools", "SKILL PACK / PINNED", "#94a3b8", "stairs"),
    "tile-kernel-skills": ("Tile Kernels", "SKILL PACK / PINNED", "#4ade80", "slabs"),
    "gpu-simulation-skills": ("Simulation", "SKILL PACK / PINNED", "#38bdf8", "orbit"),
    "multi-gpu-memory-skills": ("Multi-GPU", "SKILL PACK / PINNED", "#facc15", "arches"),
    "optimization-solver-skills": ("Solvers", "SKILL PACK / PINNED", "#f87171", "stairs"),
    "gpu-acceleration-skills": ("GPU Porting", "SKILL PACK / PINNED", "#2dd4bf", "orbit"),
    # Connectors: what the service is for, an accent of our own and a shape.
    "notion": ("Pages & databases", "CONNECTOR / DOCS", "#e2e8f0", "pages"),
    "linear": ("Issues & cycles", "CONNECTOR / ISSUES", "#f59e0b", "stack"),
    "atlassian": ("Tickets & wikis", "CONNECTOR / ISSUES", "#7dd3fc", "board"),
    "github": ("Repos & reviews", "CONNECTOR / CODE", "#a3e635", "branches"),
    "gitlab": ("Merge requests", "CONNECTOR / CODE", "#f472b6", "branches"),
    "sentry": ("Errors & traces", "CONNECTOR / MONITORING", "#c084fc", "pulse"),
    "stripe": ("Payments", "CONNECTOR / BILLING", "#5eead4", "cards"),
    "cloudflare": ("Edge & DNS", "CONNECTOR / CLOUD", "#22d3ee", "globe"),
    "cloudflare-docs": ("Edge docs", "CONNECTOR / DOCS", "#67e8f9", "book"),
    "intercom": ("Support inbox", "CONNECTOR / SUPPORT", "#86efac", "bubbles"),
    "supabase": ("Postgres projects", "CONNECTOR / DATABASE", "#93c5fd", "cylinders"),
    "neon": ("Database branches", "CONNECTOR / DATABASE", "#fcd34d", "cylinders"),
    "context7": ("Library docs", "CONNECTOR / DOCS", "#facc15", "book"),
    "hugging-face": ("Models & datasets", "CONNECTOR / ML", "#c4b5fd", "grid"),
    "deepwiki": ("Repository wikis", "CONNECTOR / DOCS", "#60a5fa", "book"),
    "microsoft-learn": ("Platform docs", "CONNECTOR / DOCS", "#a5b4fc", "book"),
    "playwright": ("Browser hands", "CONNECTOR / LOCAL", "#f87171", "window"),
    "fetch": ("Pages to text", "CONNECTOR / LOCAL", "#e879f9", "arrows"),
    "monday": ("Boards & items", "CONNECTOR / TASKS", "#fda4af", "board"),
}


def shapes(kind, c):
    x0 = 700  # the art lives on the right half
    if kind == "stairs":
        return "".join(
            f'<rect x="{x0 + 40 + i * 90}" y="{470 - i * 80}" width="80" height="{160 + i * 80}" fill="{c}" opacity="{0.25 + i * 0.15}"/>'
            for i in range(5)
        )
    if kind == "shield":
        return (
            f'<path d="M900 110 L1080 170 V340 Q1080 470 900 540 Q720 470 720 340 V170 Z" fill="none" stroke="{c}" stroke-width="14"/>'
            f'<path d="M900 190 L1010 228 V340 Q1010 420 900 466 Z" fill="{c}" opacity="0.85"/>'
            f'<path d="M900 190 L790 228 V340 Q790 420 900 466 Z" fill="{c}" opacity="0.35"/>'
        )
    if kind == "orbit":
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r in [(900, 135, 22), (1060, 330, 16), (760, 420, 26), (950, 505, 12)])
        return (
            f'<circle cx="900" cy="320" r="190" fill="none" stroke="{c}" stroke-width="6" opacity="0.5"/>'
            f'<circle cx="900" cy="320" r="120" fill="none" stroke="{c}" stroke-width="6" opacity="0.8"/>'
            f'<circle cx="900" cy="320" r="46" fill="{c}"/>' + dots
        )
    if kind == "arches":
        return "".join(
            f'<path d="M{x0 + i * 100} 520 V{300 - i * 20} A50 50 0 0 1 {x0 + i * 100 + 100} {300 - i * 20} V520 Z" fill="{c}" opacity="{0.3 + i * 0.2}"/>'
            for i in range(4)
        )
    if kind == "rings":
        return "".join(
            f'<circle cx="{900 + dx}" cy="{320 + dy}" r="120" fill="none" stroke="{c}" stroke-width="14" opacity="{o}"/>'
            for dx, dy, o in [(-70, -50, 0.9), (70, -50, 0.65), (0, 70, 0.4)]
        )
    if kind == "slabs":
        return "".join(
            f'<polygon points="{x0 + 40 + i * 30},{150 + i * 110} {x0 + 360 + i * 30},{150 + i * 110} {x0 + 400 + i * 30},{200 + i * 110} {x0 + 80 + i * 30},{200 + i * 110}" fill="{c}" opacity="{0.9 - i * 0.22}"/>'
            for i in range(4)
        )
    if kind == "phone":
        return (
            f'<rect x="770" y="90" width="260" height="450" rx="40" fill="none" stroke="{c}" stroke-width="12"/>'
            f'<rect x="800" y="130" width="200" height="300" rx="14" fill="{c}" opacity="0.2"/>'
            f'<circle cx="900" cy="480" r="22" fill="none" stroke="{c}" stroke-width="8"/>'
            f'<rect x="850" y="106" width="100" height="10" rx="5" fill="{c}"/>'
            f'<polygon points="840,180 960,260 840,340" fill="{c}"/>'
        )
    if kind == "phone2":
        return (
            f'<rect x="760" y="120" width="230" height="400" rx="40" fill="none" stroke="{c}" stroke-width="12" stroke-dasharray="26 14"/>'
            f'<rect x="830" y="90" width="230" height="400" rx="40" fill="{c}" opacity="0.28"/>'
            f'<circle cx="945" cy="290" r="64" fill="{c}"/>'
        )
    if kind == "pages":
        return "".join(
            f'<rect x="{760 + i * 40}" y="{120 + i * 40}" width="240" height="320" rx="16" fill="{c}" opacity="{0.25 + i * 0.25}"/>'
            for i in range(3)
        ) + "".join(f'<rect x="870" y="{260 + i * 36}" width="140" height="12" rx="6" fill="{BG}"/>' for i in range(4))
    if kind == "stack":
        return "".join(
            f'<rect x="{740 + i * 30}" y="{150 + i * 90}" width="320" height="64" rx="18" fill="{c}" opacity="{0.95 - i * 0.2}"/>'
            for i in range(4)
        )
    if kind == "board":
        cols = [(740, 3), (880, 2), (1020, 4)]
        return "".join(
            f'<rect x="{x}" y="{130 + j * 92}" width="120" height="76" rx="12" fill="{c}" opacity="{0.9 - j * 0.18}"/>'
            for x, n in cols for j in range(n)
        )
    if kind == "branches":
        return (
            f'<path d="M800 520 V140" stroke="{c}" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M800 420 Q800 330 960 300 V200" fill="none" stroke="{c}" stroke-width="16" stroke-linecap="round" opacity="0.6"/>'
            f'<circle cx="800" cy="140" r="34" fill="{c}"/><circle cx="800" cy="520" r="34" fill="{c}"/>'
            f'<circle cx="960" cy="180" r="34" fill="none" stroke="{c}" stroke-width="14"/>'
        )
    if kind == "pulse":
        return (
            f'<polyline points="700,330 800,330 840,200 900,470 950,260 990,330 1150,330" fill="none" stroke="{c}" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<circle cx="1000" cy="180" r="30" fill="{c}" opacity="0.4"/>'
        )
    if kind == "cards":
        return "".join(
            f'<rect x="{730 + i * 50}" y="{150 + i * 60}" width="340" height="210" rx="22" fill="{c}" opacity="{0.3 + i * 0.3}"/>'
            for i in range(3)
        ) + f'<rect x="830" y="300" width="80" height="56" rx="10" fill="{BG}"/>'
    if kind == "globe":
        return (
            f'<circle cx="910" cy="320" r="200" fill="none" stroke="{c}" stroke-width="12"/>'
            f'<ellipse cx="910" cy="320" rx="90" ry="200" fill="none" stroke="{c}" stroke-width="10" opacity="0.7"/>'
            f'<path d="M710 320 H1110 M740 220 H1080 M740 420 H1080" stroke="{c}" stroke-width="8" opacity="0.5"/>'
        )
    if kind == "book":
        return (
            f'<path d="M910 170 Q820 120 720 150 V500 Q820 470 910 520 Z" fill="{c}" opacity="0.45"/>'
            f'<path d="M910 170 Q1000 120 1100 150 V500 Q1000 470 910 520 Z" fill="{c}"/>'
            + "".join(f'<rect x="950" y="{220 + i * 50}" width="110" height="12" rx="6" fill="{BG}"/>' for i in range(5))
        )
    if kind == "cylinders":
        return "".join(
            f'<ellipse cx="{820 + i * 170}" cy="{200 + i * 60}" rx="80" ry="28" fill="{c}"/>'
            f'<path d="M{740 + i * 170} {200 + i * 60} V{420 + i * 40} A80 28 0 0 0 {900 + i * 170} {420 + i * 40} V{200 + i * 60}" fill="{c}" opacity="0.45"/>'
            for i in range(2)
        )
    if kind == "grid":
        return "".join(
            f'<rect x="{730 + x * 110}" y="{130 + y * 110}" width="90" height="90" rx="18" fill="{c}" opacity="{0.2 + ((x + y) % 4) * 0.25}"/>'
            for x in range(4) for y in range(4)
        )
    if kind == "window":
        return (
            f'<rect x="720" y="130" width="400" height="380" rx="26" fill="none" stroke="{c}" stroke-width="12"/>'
            f'<path d="M720 200 H1120" stroke="{c}" stroke-width="10"/>'
            + "".join(f'<circle cx="{760 + i * 34}" cy="166" r="10" fill="{c}"/>' for i in range(3))
            + f'<polygon points="880,300 880,440 920,400 960,470 985,458 948,388 1000,382" fill="{c}"/>'
        )
    if kind == "arrows":
        return (
            f'<rect x="720" y="150" width="170" height="330" rx="18" fill="none" stroke="{c}" stroke-width="12"/>'
            f'<path d="M900 315 H1000 M960 270 L1010 315 L960 360" fill="none" stroke="{c}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
            + "".join(f'<rect x="1030" y="{200 + i * 50}" width="{110 - (i % 2) * 40}" height="14" rx="7" fill="{c}"/>' for i in range(5))
        )
    # bubbles
    return (
        f'<path d="M740 130 H1000 Q1040 130 1040 170 V300 Q1040 340 1000 340 H850 L790 400 V340 H740 Q700 340 700 300 V170 Q700 130 740 130 Z" fill="{c}"/>'
        f'<path d="M1100 330 H1000 V400 H1090 L1130 450 V400 H1150 V360 Q1150 330 1100 330 Z" fill="{c}" opacity="0.4"/>'
        f'<rect x="740" y="180" width="200" height="14" rx="7" fill="{BG}"/><rect x="740" y="220" width="150" height="14" rx="7" fill="{BG}"/>'
        f'<rect x="740" y="260" width="230" height="14" rx="7" fill="{BG}"/>'
    )


def cover(name, title, label, accent, shape):
    size = 120 if len(title) <= 8 else 100 if len(title) <= 11 else 92 if len(title) <= 13 else 64
    grid = "".join(f'<path d="M{x} 0 V{H}" stroke="#ffffff" stroke-opacity="0.04"/>' for x in range(0, W, 60))
    grid += "".join(f'<path d="M0 {y} H{W}" stroke="#ffffff" stroke-opacity="0.04"/>' for y in range(0, H, 60))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{BG}"/>
{grid}
<rect x="0" y="0" width="18" height="{H}" fill="{accent}"/>
{shapes(shape, accent)}
<g font-family="Helvetica Neue, Helvetica, Arial, sans-serif">
<text x="70" y="96" font-size="26" font-weight="700" letter-spacing="6" fill="{accent}">{label}</text>
<text x="70" y="{H - 200}" font-size="{size}" font-weight="800" fill="{INK}">{escape(title)}</text>
<text x="70" y="{H - 70}" font-size="28" font-weight="600" letter-spacing="8" fill="{MUTED}">DUSKCODE WORKSHOP</text>
</g>
</svg>
"""


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, spec in COVERS.items():
        (OUT / f"{name}.svg").write_text(cover(name, *spec))
    print(f"wrote {len(COVERS)} covers into {OUT}")
