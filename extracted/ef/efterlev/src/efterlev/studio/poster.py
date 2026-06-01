"""Render the Studio compliance map as a shareable poster SVG.

A standalone, frame-worthy image of a workspace's posture — the KSIs laid
out as a theme-grouped grid of verdict-colored tiles, a readiness ring, and
a legend. SVG so it's resolution-independent; `efterlev studio --poster
out.svg` writes it. The viral/3PAO-handoff artifact.
"""

from __future__ import annotations

import math
import random
from pathlib import Path
from typing import Any

FONT = "Inter, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif"
_LABELS = {
    "implemented": "implemented",
    "partial": "partial",
    "not_implemented": "gap",
    "evidence_layer_inapplicable": "procedural",
    "not_applicable": "n/a",
}
BCOLS, BROWS, TPR = 4, 3, 5  # theme-block cols/rows; tiles-per-row in a block


def _ring(cx: float, cy: float, rr: float, frac: float) -> str:
    a0 = -math.pi / 2
    a1 = a0 + 2 * math.pi * max(0.0, min(1.0, frac))
    large = 1 if frac > 0.5 else 0
    sx, sy = cx + rr * math.cos(a0), cy + rr * math.sin(a0)
    ex, ey = cx + rr * math.cos(a1), cy + rr * math.sin(a1)
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{rr + 22}" fill="#070b16" opacity="0.82"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#1c2540" stroke-width="9"/>'
        f'<path d="M{sx:.1f},{sy:.1f} A{rr},{rr} 0 {large} 1 {ex:.1f},{ey:.1f}" fill="none" '
        f'stroke="url(#ring)" stroke-width="9" stroke-linecap="round" filter="url(#glow)"/>'
        f'<text x="{cx}" y="{cy + 9:.0f}" fill="#eef2ff" font-size="28" font-weight="600" '
        f'text-anchor="middle">{round(frac * 100)}%</text>'
        f'<text x="{cx}" y="{cy + rr + 26:.0f}" fill="#7e8bb0" font-size="13" letter-spacing="2" '
        f'text-anchor="middle">READINESS</text>'
    )


def render_poster_svg(data: dict[str, Any], *, width: int = 1680, height: int = 1040) -> str:
    """Return a standalone poster SVG for a `build_studio_data` payload."""
    cw, ch = width, height
    colors = data["colors"]
    nodes = data["nodes"]
    counts = data["counts"]
    # KSIs grouped by theme, biggest theme first (mirrors the web layout)
    order = sorted({n["t"] for n in nodes}, key=lambda t: -sum(1 for n in nodes if n["t"] == t))
    by_theme = {t: [n for n in nodes if n["t"] == t] for t in order}

    gx0, gy0, gx1, gy1 = 70, 150, cw - 70, ch - 96
    cellw = (gx1 - gx0) / BCOLS
    cellh = min((gy1 - gy0) / BROWS, 240)
    yoff = ((gy1 - gy0) - BROWS * cellh) / 2
    pad, labelh, gap = 16, 28, 11
    ts = min(30.0, (cellw - 2 * pad - (TPR - 1) * gap) / TPR)

    rng = random.Random(3)
    p: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{cw}" height="{ch}" '
        f'viewBox="0 0 {cw} {ch}" font-family="{FONT}">'
    ]
    p.append("<defs>")
    p.append(
        '<radialGradient id="bg" cx="38%" cy="30%" r="95%">'
        '<stop offset="0%" stop-color="#141a2e"/><stop offset="55%" stop-color="#0a0e1c"/>'
        '<stop offset="100%" stop-color="#05060d"/></radialGradient>'
    )
    p.append(
        '<filter id="glow" x="-200%" y="-200%" width="500%" height="500%">'
        '<feGaussianBlur stdDeviation="5" result="b"/><feMerge>'
        '<feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    )
    p.append(
        '<filter id="soft" x="-300%" y="-300%" width="700%" height="700%">'
        '<feGaussianBlur stdDeviation="13"/></filter>'
    )
    p.append(
        '<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#54e6a6"/>'
        '<stop offset="100%" stop-color="#41b6e6"/></linearGradient>'
    )
    p.append("</defs>")
    p.append(f'<rect width="{cw}" height="{ch}" fill="url(#bg)"/>')
    for _ in range(120):
        dx, dy = rng.uniform(0, cw), rng.uniform(0, ch)
        dr, do = rng.uniform(0.4, 1.3), rng.uniform(0.04, 0.14)
        p.append(
            f'<circle cx="{dx:.0f}" cy="{dy:.0f}" r="{dr:.1f}" fill="#9fb0ff" opacity="{do:.2f}"/>'
        )
    # theme blocks: label + verdict tiles
    for ti, t in enumerate(order):
        bx = gx0 + (ti % BCOLS) * cellw
        by = gy0 + yoff + (ti // BCOLS) * cellh
        p.append(
            f'<text x="{bx + pad:.0f}" y="{by + 14:.0f}" fill="#8ea0c8" font-size="14" '
            f'letter-spacing="2" font-weight="600">{t}</text>'
        )
        for j, n in enumerate(by_theme[t]):
            s = n["s"]
            col = colors.get(s, "#5b6789")
            pos = s in ("implemented", "partial")
            tx = bx + pad + (j % TPR) * (ts + gap)
            ty = by + labelh + (j // TPR) * (ts + gap)
            p.append(
                f'<rect x="{tx - 6:.0f}" y="{ty - 6:.0f}" width="{ts + 12:.0f}" '
                f'height="{ts + 12:.0f}" rx="9" fill="{col}" '
                f'opacity="{0.34 if pos else 0.13}" filter="url(#soft)"/>'
            )
            p.append(
                f'<rect x="{tx:.0f}" y="{ty:.0f}" width="{ts:.0f}" height="{ts:.0f}" '
                f'rx="6" fill="{col}" filter="url(#glow)"/>'
            )
    # title
    p.append(
        '<text x="64" y="76" fill="#eef2ff" font-size="33" font-weight="600">efterlev '
        '<tspan fill="#54e6a6">studio</tspan></text>'
    )
    sub = "FedRAMP 20x Moderate · compliance posture"
    if data.get("mode") == "demo":
        sub += " · sample data"
    p.append(f'<text x="66" y="105" fill="#7e8bb0" font-size="16" letter-spacing="2">{sub}</text>')
    # readiness ring
    p.append(_ring(cw - 150, 110, 52, data["readiness"] / 100))
    # legend
    lx, ly = 64, ch - 26
    for s in ("implemented", "partial", "not_implemented", "evidence_layer_inapplicable"):
        n_ct = counts.get(s, 0)
        p.append(
            f'<rect x="{lx - 6}" y="{ly - 11}" width="12" height="12" rx="3" fill="{colors[s]}" '
            f'filter="url(#glow)"/>'
            f'<text x="{lx + 14}" y="{ly}" fill="#9aa6c8" font-size="14">{_LABELS[s]} {n_ct}</text>'
        )
        lx += 150
    p.append("</svg>")
    return "".join(p)


def write_poster(root: Path | None, out_path: Path) -> Path:
    """Build the workspace's poster and write it to `out_path` (as SVG)."""
    from efterlev.studio.web_data import build_studio_data

    svg = render_poster_svg(build_studio_data(root))
    out_path.write_text(svg, encoding="utf-8")
    return out_path
