"""
Map styling at admin_2 (county) granularity.

Two problems at county scale, both reported 2026-08-18:

1. ``annotate_regions`` is usually inherited from ``[DEFAULT]`` rather than set
   per project (usa_admin2 picks up ``True`` from geocif.txt's DEFAULT), so
   every one of ~1,000 county polygons got a name label — an unreadable smear.
2. Only GMT border level 1 (national) was drawn, so there was nothing to tell
   one state from another under the county choropleth.

County polygon strokes are deliberately left at 0.4p black (user decision), so
the admin_1 overlay is drawn heavier than that, and AFTER the polygons.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.viz.plot import _ANNOTATE_MAX_REGIONS, effective_annotate_regions

RENDER_PY = Path(__file__).resolve().parents[1] / "geocif" / "viz" / "_pygmt_render.py"


# ------------------------------------------------- label suppression


def test_labels_suppressed_at_county_scale():
    """usa_admin2 draws ~1,000 counties."""
    assert effective_annotate_regions(True, 1004) is False
    assert effective_annotate_regions(True, 2038) is False


def test_labels_kept_at_state_scale():
    """~50 states is exactly where annotation earns its keep."""
    assert effective_annotate_regions(True, 50) is True
    assert effective_annotate_regions(True, _ANNOTATE_MAX_REGIONS) is True


def test_threshold_boundary():
    assert effective_annotate_regions(True, _ANNOTATE_MAX_REGIONS + 1) is False


def test_off_stays_off_regardless_of_count():
    assert effective_annotate_regions(False, 10) is False
    assert effective_annotate_regions(False, 5000) is False


def test_smaller_projects_are_untouched():
    """Kenya 47 counties, Malawi 28 districts, Wolayita kebeles."""
    for n in (28, 33, 47, 120):
        assert effective_annotate_regions(True, n) is True


# ------------------------------------------------- admin_1 overlay


def test_overlay_requested_only_at_fine_granularity():
    """The params flag mirrors the same polygon-count rule."""
    assert (1004 > _ANNOTATE_MAX_REGIONS) is True
    assert (50 > _ANNOTATE_MAX_REGIONS) is False


def test_overlay_is_drawn_after_the_choropleth():
    """fig.coast before the polygons would be painted over by them."""
    source = RENDER_PY.read_text(encoding="utf-8", errors="replace")
    plot_call = source.index("fig.plot(data=fp, fill=color, pen=pen)")
    overlay = source.index('if p.get("admin1_borders")')
    assert overlay > plot_call, "admin_1 overlay must come after the polygon plot"


def test_overlay_uses_border_level_2():
    """GMT: level 1 = national, level 2 = state/province."""
    source = RENDER_PY.read_text(encoding="utf-8", errors="replace")
    overlay = source.index('if p.get("admin1_borders")')
    assert 'borders="2/' in source[overlay:overlay + 300]


def test_overlay_is_heavier_than_the_county_stroke():
    """County strokes stay 0.4p black, so a lighter state line would vanish."""
    source = RENDER_PY.read_text(encoding="utf-8", errors="replace")
    assert 'pen = "0.4p,black"' in source
    overlay = source.index('if p.get("admin1_borders")')
    segment = source[overlay:overlay + 300]
    weight = float(segment.split('borders="2/')[1].split("p,")[0])
    assert weight > 0.4, "admin_1 line must read above the 0.4p county mesh"
    assert weight <= 1.0, "…but stay slim"


def test_county_strokes_are_unchanged():
    """Explicit user decision: do not lighten county borders at admin_2."""
    source = RENDER_PY.read_text(encoding="utf-8", errors="replace")
    assert 'pen = "0.4p,black" if p.get("do_borders", True) else None' in source


def test_base_coast_still_draws_national_borders_only():
    source = RENDER_PY.read_text(encoding="utf-8", errors="replace")
    assert 'fig.coast(shorelines="0.3p,gray60", borders="1/0.2p,gray70"' in source


def test_params_schema_documents_the_flag():
    source = RENDER_PY.read_text(encoding="utf-8", errors="replace")
    assert '"admin1_borders"' in source.split("The GeoJSON carries")[0]
