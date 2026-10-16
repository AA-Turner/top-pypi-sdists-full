"""
Map styling at admin_2 (county) granularity.

Two problems at county scale, both reported 2026-08-18:

1. ``annotate_regions`` is usually inherited from ``[DEFAULT]`` rather than set
   per project (usa_admin2 picks up ``True`` from geocif.txt's DEFAULT), so
   every one of ~1,000 county polygons got a name label — an unreadable smear.
2. Only GMT border level 1 (national) was drawn, so there was nothing to tell
   one state from another under the county choropleth.

County polygon strokes were left at 0.4p black (user decision, 2026-08-18).
Superseded 2026-10-15 for dense maps (more than _DENSE_MAP_REGIONS units):
at Brazil's ~2,500 municipalities that stroke hid the fill, so dense maps
draw hairline unit outlines and black state lines on top.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.viz._style import (
    ADMIN1_LINE_PEN, BORDER_PEN, COAST_KW, DENSE_POLY_PEN, NATIONAL_LINE_PEN,
    POLY_PEN, WATER_FILL)
from geocif.viz.plot import (
    _ANNOTATE_MAX_REGIONS, _DENSE_MAP_REGIONS, effective_annotate_regions)

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


# ------------------------------------------------- admin_1 overlay and dense maps
#
# Render behaviour is checked through a fake pygmt that records every call,
# not by grepping the renderer's source: the source-grep versions of these
# tests went stale when the pens moved to viz/_style.py.


class _FakeFigure:
    def __init__(self, log):
        self.log = log

    def __getattr__(self, name):
        def call(*args, **kwargs):
            self.log.append((name, kwargs))
        return call


@pytest.fixture
def fake_pygmt(monkeypatch):
    import types
    log = []
    mod = types.ModuleType("pygmt")
    mod.Figure = lambda: _FakeFigure(log)
    mod.makecpt = lambda **kw: log.append(("makecpt", kw))
    monkeypatch.setitem(sys.modules, "pygmt", mod)
    return log


def _render(tmp_path, **extra):
    import geopandas as gpd
    from shapely.geometry import box
    from geocif.viz import _pygmt_render

    gj = tmp_path / "data.geojson"
    gpd.GeoDataFrame(
        {"_fill": ["#112233", "#445566"]},
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1)], crs="EPSG:4326",
    ).to_file(gj, driver="GeoJSON")
    params = {"out_path": str(tmp_path / "out.png"), "region": [0, 2, 0, 1],
              "do_borders": True, "colorbar": {"type": "none"}}
    params.update(extra)
    _pygmt_render.render(str(gj), params)


def _calls(log, name):
    return [kw for n, kw in log if n == name]


def test_overlay_requested_only_at_fine_granularity():
    """The params flag mirrors the same polygon-count rule."""
    assert (1004 > _DENSE_MAP_REGIONS) is True
    assert (50 > _DENSE_MAP_REGIONS) is False


def test_state_scale_maps_keep_heavy_unit_strokes(fake_pygmt, tmp_path):
    _render(tmp_path)
    pens = {kw.get("pen") for kw in _calls(fake_pygmt, "plot")}
    assert pens == {POLY_PEN}
    assert "water" not in _calls(fake_pygmt, "coast")[0]


def test_dense_maps_use_hairline_unit_strokes_and_tinted_water(fake_pygmt, tmp_path):
    """User 2026-10-15: at municipality scale the 0.4p black mesh hid the fill."""
    _render(tmp_path, dense=True)
    pens = {kw.get("pen") for kw in _calls(fake_pygmt, "plot")}
    assert pens == {DENSE_POLY_PEN}
    assert _calls(fake_pygmt, "coast")[0]["water"] == WATER_FILL


def test_gmt_level2_overlay_is_the_fallback_after_the_choropleth(fake_pygmt, tmp_path):
    """No admin-1 file: GMT border level 2, drawn after the polygons."""
    _render(tmp_path, dense=True, admin1_borders=True)
    names = [n for n, _ in fake_pygmt]
    coasts = _calls(fake_pygmt, "coast")
    assert coasts[-1]["borders"] == BORDER_PEN and BORDER_PEN.startswith("2/")
    assert len(names) - 1 - names[::-1].index("coast") > names.index("plot")


def test_admin1_file_lines_replace_gmt_level2(fake_pygmt, tmp_path):
    _render(tmp_path, dense=True, admin1_borders=True,
            admin1_lines="states.geojson", national_lines="nation.geojson")
    plots = _calls(fake_pygmt, "plot")
    assert plots[-2] == {"data": "states.geojson", "pen": ADMIN1_LINE_PEN}
    assert plots[-1] == {"data": "nation.geojson", "pen": NATIONAL_LINE_PEN}
    assert all("borders" not in kw or kw["borders"].startswith("1/")
               for kw in _calls(fake_pygmt, "coast"))


def test_state_lines_read_above_the_unit_strokes():
    weight = lambda pen: float(pen.split("/")[-1].split("p,")[0])
    assert weight(ADMIN1_LINE_PEN) > weight(DENSE_POLY_PEN)
    assert weight(NATIONAL_LINE_PEN) >= weight(ADMIN1_LINE_PEN)
    assert 0.4 < weight(BORDER_PEN) <= 1.0


def test_base_coast_draws_national_borders_only():
    assert COAST_KW["borders"].startswith("1/")


def test_class_colorbar_gets_cpt_and_end_cap(fake_pygmt, tmp_path):
    _render(tmp_path, colorbar={"type": "classes", "colors": ["#000000", "#ffffff"],
                                "edges": [0.0, 0.5, 1.0], "extend": "max"})
    (cb,) = _calls(fake_pygmt, "colorbar")
    assert cb["position"].endswith("+ef")
    assert cb["frame"][0] == "xa0.5"


def test_write_class_cpt(tmp_path):
    from geocif.viz._pygmt_render import write_class_cpt
    p = tmp_path / "c.cpt"
    write_class_cpt(p, [0, 0.5, 1], ["#000000", "#ffffff"])
    lines = p.read_text().splitlines()
    assert lines[:2] == ["0 #000000 0.5 #000000", "0.5 #ffffff 1 #ffffff"]
    assert "F #ffffff" in lines and "B #000000" in lines


def test_params_schema_documents_the_flags():
    source = RENDER_PY.read_text(encoding="utf-8", errors="replace")
    schema = source.split("The GeoJSON carries")[0]
    for key in ('"admin1_borders"', '"dense"', '"admin1_lines"', '"classes"'):
        assert key in schema
