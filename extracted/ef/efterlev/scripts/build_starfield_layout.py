"""Regenerate the frozen KSI starfield layout.

Computes node positions ONCE (phyllotaxis theme anchors + a light
force-directed de-overlap pass — the algorithm validated by the
2026-05-22 visual spike) over the real FRMR catalog, and writes them to
`src/efterlev/studio/starfield_layout.json`. Deterministic (seeded), so
re-running on the same catalog reproduces the same map.

Run when the KSI catalog changes:
    uv run python scripts/build_starfield_layout.py
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

from efterlev.cli.plan import load_baseline_landscape

SEED = 7
OUT = (
    Path(__file__).resolve().parent.parent / "src" / "efterlev" / "studio" / "starfield_layout.json"
)
BASELINE = "fedramp-20x-moderate"


def _shared_control_edges(
    ksi_controls: dict[str, set[str]], min_shared: int = 3
) -> list[tuple[str, str, int]]:
    ids = list(ksi_controls)
    edges: list[tuple[str, str, int]] = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            w = len(ksi_controls[ids[i]] & ksi_controls[ids[j]])
            if w >= min_shared:
                edges.append((ids[i], ids[j], w))
    return edges


def compute_layout() -> dict[str, dict[str, object]]:
    doc, _covered, _procedural = load_baseline_landscape(BASELINE)
    rng = random.Random(SEED)
    golden = math.pi * (3.0 - math.sqrt(5.0))

    theme_of = {k: ind.theme for k, ind in doc.indicators.items()}
    ksi_controls = {k: {c.lower() for c in ind.controls} for k, ind in doc.indicators.items()}
    pos: dict[str, list[float]] = {}

    by_theme: dict[str, list[str]] = {}
    for k, t in theme_of.items():
        by_theme.setdefault(t, []).append(k)

    # 1) theme anchors via phyllotaxis (fills a disk evenly incl. center),
    #    largest constellations placed first → roomier central positions.
    themes = sorted(by_theme, key=lambda t: -len(by_theme[t]))
    nt = len(themes)
    anchor: dict[str, tuple[float, float]] = {}
    for i, t in enumerate(themes):
        a = i * golden
        rr = math.sqrt((i + 0.5) / nt)
        anchor[t] = (0.5 + 0.46 * rr * math.cos(a), 0.5 + 0.46 * rr * math.sin(a))

    # 2) seed each theme's stars as a small cluster around its anchor.
    for t, members in by_theme.items():
        ax, ay = anchor[t]
        m = len(members)
        crad = 0.045 + 0.022 * math.sqrt(m)
        members_sorted = sorted(members)  # deterministic order
        for j, k in enumerate(members_sorted):
            a = j * golden + rng.uniform(-0.25, 0.25)
            rr = math.sqrt((j + 0.5) / max(m, 1)) * crad
            pos[k] = [ax + rr * math.cos(a), ay + rr * math.sin(a)]

    # 3) light force pass: de-overlap, hold near own theme anchor, whisper of
    #    shared-control attraction.
    edges = _shared_control_edges(ksi_controls)
    ids = sorted(pos)
    k_rep, k_anchor, k_edge = 0.00018, 0.06, 0.004
    for step in range(140):
        cool = 1.0 - step / 140
        fx: dict[str, float] = {k: 0.0 for k in ids}
        fy: dict[str, float] = {k: 0.0 for k in ids}
        for ii in range(len(ids)):
            for jj in range(ii + 1, len(ids)):
                a, b = ids[ii], ids[jj]
                dx = pos[a][0] - pos[b][0]
                dy = pos[a][1] - pos[b][1]
                d2 = dx * dx + dy * dy + 1e-4
                f = k_rep / d2
                fx[a] += f * dx
                fy[a] += f * dy
                fx[b] -= f * dx
                fy[b] -= f * dy
        for k in ids:
            ax, ay = anchor[theme_of[k]]
            fx[k] += k_anchor * (ax - pos[k][0])
            fy[k] += k_anchor * (ay - pos[k][1])
        for a, b, w in edges:
            dx = pos[b][0] - pos[a][0]
            dy = pos[b][1] - pos[a][1]
            f = k_edge * min(w, 6) / 6.0
            fx[a] += f * dx
            fy[a] += f * dy
            fx[b] -= f * dx
            fy[b] -= f * dy
        for k in ids:
            pos[k][0] += fx[k] * cool * 3.0
            pos[k][1] += fy[k] * cool * 3.0
            pos[k][0] = min(0.97, max(0.03, pos[k][0]))
            pos[k][1] = min(0.97, max(0.03, pos[k][1]))

    return {
        k: {"theme": theme_of[k], "x": round(pos[k][0], 5), "y": round(pos[k][1], 5)}
        for k in sorted(pos)
    }


def main() -> None:
    nodes = compute_layout()
    payload = {
        "baseline": BASELINE,
        "_comment": "Frozen KSI starfield layout. Regenerate via the builder script.",
        "nodes": nodes,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(nodes)} nodes)")


if __name__ == "__main__":
    main()
