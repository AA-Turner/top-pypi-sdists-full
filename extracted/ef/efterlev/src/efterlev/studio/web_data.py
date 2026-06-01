"""Assemble the JSON payload the browser Studio renders.

Pulls together the frozen layout, shared-control edges, and per-KSI
verdicts. Verdicts come from the workspace's gap-classification claims
when present (real posture); otherwise a clearly-labeled keyless DEMO
fills in plausible sample verdicts so first-touch always looks complete.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# Verdict palette shared with the browser renderer.
VERDICT_COLORS: dict[str, str] = {
    "implemented": "#54e6a6",
    "partial": "#f4c560",
    "not_implemented": "#f0716e",
    "not_applicable": "#5b6789",
    "evidence_layer_inapplicable": "#a98bf5",
}
SOURCES = [
    ["Terraform", "#54e6a6"],
    ["CloudFormation", "#f4c560"],
    ["GitHub workflows", "#41b6e6"],
    ["Security Hub", "#a98bf5"],
    ["Evidence manifests", "#f0716e"],
]
_VALID = set(VERDICT_COLORS)


def _real_verdicts(root: Path, baseline_ksis: set[str]) -> dict[str, str]:
    """Per-KSI gap-classification verdicts from the store, or {} if none."""
    if not (root / ".efterlev").is_dir():
        return {}
    from efterlev.primitives.readiness.score import load_latest_claim_statuses

    statuses = load_latest_claim_statuses(root, baseline_ksi_ids=baseline_ksis)
    return {k: v for k, v in statuses.items() if v in _VALID}


def build_studio_data(
    root: Path | None = None,
    *,
    seed: int = 23,
    verdicts: dict[str, str] | None = None,
    mode: str | None = None,
) -> dict[str, Any]:
    """Build the Studio render payload for `root` (or a demo if root is None).

    Pass `verdicts` to render a fixed per-KSI verdict map (e.g. the precomputed
    govnotes sample) instead of reading the store or filling a demo; `mode`
    then labels the payload (defaults to "sample").
    """
    import random

    from efterlev.cli.plan import classify_ksi, load_baseline_landscape
    from efterlev.studio.demo import demo_events
    from efterlev.studio.starfield_layout import load_starfield_layout

    layout = load_starfield_layout()
    doc, covered, procedural = load_baseline_landscape()
    categories: dict[str, str] = {
        k: str(classify_ksi(k, covered, procedural)) for k in doc.indicators
    }
    baseline_ksis = set(doc.indicators)

    if verdicts is not None:
        mode = mode or "sample"
    else:
        verdicts = _real_verdicts(root, baseline_ksis) if root is not None else {}
        mode = "live" if verdicts else "demo"
        if mode == "demo":
            for e in demo_events(categories, seed=seed):
                if e.kind == "ksi_classified":
                    verdicts[e.ksi] = e.status  # type: ignore[attr-defined]

    ids = sorted(layout.nodes)
    idx = {k: i for i, k in enumerate(ids)}
    controls = {k: {c.lower() for c in ind.controls} for k, ind in doc.indicators.items()}
    rng = random.Random(7)
    names = {k: ind.name for k, ind in doc.indicators.items()}
    nodes = [
        {
            "k": k,
            "n": names.get(k, ""),
            "x": round(layout.nodes[k].x, 5),
            "y": round(layout.nodes[k].y, 5),
            "t": layout.nodes[k].theme,
            "s": verdicts.get(k, "not_applicable"),
            "src": rng.randrange(len(SOURCES)),
        }
        for k in ids
    ]
    edges = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if len(controls[ids[i]] & controls[ids[j]]) >= 3:
                edges.append([idx[ids[i]], idx[ids[j]]])
    edges = edges[:46]

    counts: dict[str, int] = {}
    by_theme: dict[str, dict[str, int]] = {}
    for k in ids:
        s = verdicts.get(k, "not_applicable")
        counts[s] = counts.get(s, 0) + 1
        bt = by_theme.setdefault(layout.nodes[k].theme, {})
        bt[s] = bt.get(s, 0) + 1
    readiness = round(
        100 * (counts.get("implemented", 0) + 0.5 * counts.get("partial", 0)) / max(1, len(ids))
    )

    theme_names = {tid: t.name for tid, t in doc.themes.items()}

    return {
        "mode": mode,
        "baseline": "FedRAMP 20x Moderate",
        "nodes": nodes,
        "edges": edges,
        "colors": VERDICT_COLORS,
        "sources": SOURCES,
        "counts": counts,
        "byTheme": by_theme,
        "themes": sorted(by_theme),
        "themeNames": theme_names,
        "readiness": readiness,
        "total": len(ids),
    }


def sample_dir() -> Path:
    """Filesystem path to the bundled govnotes sample workspace."""
    import importlib.resources

    return Path(str(importlib.resources.files("efterlev").joinpath("samples", "govnotes")))


def load_sample_studio_data() -> dict[str, Any]:
    """The precomputed govnotes sample payload (`studio --sample`, instant + keyless)."""
    import importlib.resources
    import json

    text = (
        importlib.resources.files("efterlev")
        .joinpath("samples", "govnotes", "posture.json")
        .read_text(encoding="utf-8")
    )
    return json.loads(text)
