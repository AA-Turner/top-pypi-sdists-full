"""Tests for the frozen KSI starfield layout (Efterlev Studio Phase 0).

The layout is computed once and frozen to a shipped data file. These pin
that it covers the current catalog exactly, stays in-bounds, and that the
builder is deterministic (re-running reproduces the frozen file) — so the
map a user sees is stable across runs and platforms.
"""

from __future__ import annotations

from efterlev.cli.plan import load_baseline_landscape
from efterlev.studio.starfield_layout import StarNode, load_starfield_layout


def test_layout_covers_the_whole_catalog() -> None:
    layout = load_starfield_layout()
    doc, _covered, _procedural = load_baseline_landscape()
    catalog_ksis = set(doc.indicators)
    assert set(layout.nodes) == catalog_ksis
    assert len(layout) == 60


def test_layout_positions_in_bounds() -> None:
    layout = load_starfield_layout()
    for node in layout.nodes.values():
        assert isinstance(node, StarNode)
        assert 0.0 <= node.x <= 1.0
        assert 0.0 <= node.y <= 1.0


def test_layout_themes_match_catalog() -> None:
    layout = load_starfield_layout()
    doc, _covered, _procedural = load_baseline_landscape()
    for ksi, node in layout.nodes.items():
        assert node.theme == doc.indicators[ksi].theme


def test_layout_fills_the_field_not_a_donut() -> None:
    # Spread across both axes (the spike's first bug was an empty-center
    # donut clinging to the perimeter); assert real coverage of the canvas.
    layout = load_starfield_layout()
    xs = [n.x for n in layout.nodes.values()]
    ys = [n.y for n in layout.nodes.values()]
    assert max(xs) - min(xs) > 0.6
    assert max(ys) - min(ys) > 0.6
    # at least a few stars live near the middle (not all flung to the edge)
    central = [n for n in layout.nodes.values() if 0.3 < n.x < 0.7 and 0.3 < n.y < 0.7]
    assert len(central) >= 5


def test_builder_is_deterministic() -> None:
    # Re-running the builder must reproduce the frozen file byte-for-byte
    # (seeded). Guards against silent layout drift on regeneration.
    import json

    from scripts.build_starfield_layout import compute_layout

    fresh = compute_layout()
    shipped = {
        ksi: {"theme": n.theme, "x": n.x, "y": n.y}
        for ksi, n in load_starfield_layout().nodes.items()
    }
    # compare rounded coords (the file rounds to 5 dp)
    fresh_norm = {
        k: {"theme": v["theme"], "x": round(float(v["x"]), 5), "y": round(float(v["y"]), 5)}
        for k, v in fresh.items()
    }
    assert json.dumps(fresh_norm, sort_keys=True) == json.dumps(shipped, sort_keys=True)
