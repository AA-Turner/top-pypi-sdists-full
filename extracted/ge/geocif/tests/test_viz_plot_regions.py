"""Regression tests for the geocif/viz/plot.py region-drawing fixes.

Three bugs, one test class each:

1. Excluded (NaN) regions were never drawn on the matplotlib path: the old
   loop computed the gray fc in one branch but only reached ``add_feature``
   inside the colormapped ``elif key:`` branch, so the "excluded region"
   silhouette the pygmt path renders (``#d9d9d9``) silently vanished on the
   matplotlib fallback. The fill decision now lives in the pure helper
   ``_region_fill`` and a feature is added whenever a fill is returned.
2. ``elif key:`` used truthiness, so a metric value of exactly 0 (or a
   qualitative key 0) was skipped on the matplotlib path while the pygmt
   path rendered it.
3. ``_plot_map_pygmt`` leaked one ``pygmt_map_*`` temp dir (GeoJSON +
   params.json) per rendered map; it is now removed in a ``finally``.

The tests avoid cartopy and pygmt entirely: the drawing loop is exercised
with fake ``cartopy`` modules injected into ``sys.modules``, and the pygmt
path with a fake ``geocif.viz._pygmt_render`` whose ``render`` is a spy.
"""
import os
import sys
import types
import tempfile

import matplotlib

matplotlib.use("Agg", force=True)  # plot.py imports pyplot at module import

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from matplotlib.colors import Normalize, to_hex
from shapely.geometry import Polygon

from geocif.viz import plot


# ---------------------------------------------------------------------------
# Shared stubs / fixtures
# ---------------------------------------------------------------------------

class _CmapStub:
    """Palettable-like: ``.mpl_colormap`` (sequential) / ``.colors`` (qualitative)."""

    def __init__(self, mpl_colormap=None, colors=None):
        if mpl_colormap is not None:
            self.mpl_colormap = mpl_colormap
        if colors is not None:
            self.colors = colors


@pytest.fixture
def seq_cmap():
    return _CmapStub(mpl_colormap=matplotlib.colormaps["viridis"])


@pytest.fixture
def norm():
    return Normalize(vmin=0.0, vmax=10.0)


def _square(x0):
    return Polygon([(x0, 0), (x0 + 1, 0), (x0 + 1, 1), (x0, 1)])


# ---------------------------------------------------------------------------
# BUG 1 + BUG 2 — pure fill-decision logic (_region_fill)
# ---------------------------------------------------------------------------

class TestRegionFill:
    def test_nan_is_excluded_gray(self, seq_cmap, norm):
        fc = plot._region_fill(float("nan"), "sequential", None, False, seq_cmap, norm)
        assert fc == (0.85, 0.85, 0.85, 1.0)

    def test_nan_gray_matches_pygmt_hex(self, seq_cmap, norm):
        # _plot_map_pygmt's _fill_for paints excluded regions "#d9d9d9";
        # 0.85 * 255 rounds to 0xd9, so the two backends agree exactly.
        fc = plot._region_fill(np.nan, "sequential", None, False, seq_cmap, norm)
        assert to_hex(fc) == "#d9d9d9"

    def test_zero_value_is_drawn(self, seq_cmap, norm):
        # BUG 2: `elif key:` skipped an exact-0 metric value.
        fc = plot._region_fill(0.0, "sequential", None, False, seq_cmap, norm)
        assert fc is not None
        assert fc == seq_cmap.mpl_colormap(norm(0.0))

    def test_valid_value_uses_colormap(self, seq_cmap, norm):
        fc = plot._region_fill(5.0, "sequential", None, False, seq_cmap, norm)
        assert fc == seq_cmap.mpl_colormap(norm(5.0))

    def test_qualitative_match_by_key(self):
        cmap = [(255, 0, 0), (0, 255, 0)]
        fc = plot._region_fill(2, "qualitative", {1: "low", 2: "high"}, True, cmap, None)
        assert fc == (0.0, 1.0, 0.0)

    def test_qualitative_match_by_label(self):
        cmap = [(255, 0, 0), (0, 255, 0)]
        fc = plot._region_fill("low", "qualitative", {1: "low", 2: "high"}, False, cmap, None)
        assert fc == (1.0, 0.0, 0.0)

    def test_qualitative_key_zero_is_found(self):
        # BUG 2 (qualitative flavor): key 0 is falsy, so the found-flag must
        # be explicit. Color index (0 - 1) % len wraps, same as the pygmt path.
        cmap = [(255, 0, 0), (0, 0, 255)]
        fc = plot._region_fill(0, "qualitative", {0: "none", 1: "low"}, True, cmap, None)
        assert fc == (0.0, 0.0, 1.0)

    def test_qualitative_no_match_returns_none(self):
        # Parity: _fill_for returns None for unmatched values and the row is
        # dropped; the matplotlib loop must skip them too (the old code fell
        # through with key == last dict key and painted the wrong color).
        cmap = [(255, 0, 0), (0, 255, 0)]
        fc = plot._region_fill("bogus", "qualitative", {1: "low", 2: "high"}, False, cmap, None)
        assert fc is None

    def test_qualitative_palettable_colors_attr(self):
        cmap = _CmapStub(colors=[(255, 0, 0), (0, 255, 0)])
        fc = plot._region_fill(1, "qualitative", {1: "low", 2: "high"}, True, cmap, None)
        assert fc == (1.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# BUG 1 + BUG 2 — the drawing loop actually adds features for NaN / 0
# ---------------------------------------------------------------------------

class _FakeAx:
    def __init__(self):
        self.features = []

    def add_feature(self, feature, **kwargs):
        self.features.append(feature)


def _install_fake_cartopy(monkeypatch):
    """Inject minimal cartopy stand-ins so _draw_regions runs without cartopy."""

    class FakeShapelyFeature:
        def __init__(self, geom, crs, **kwargs):
            self.geom = geom
            self.crs = crs
            self.kwargs = kwargs

    crs_mod = types.ModuleType("cartopy.crs")
    crs_mod.PlateCarree = lambda: "platecarree"
    feature_mod = types.ModuleType("cartopy.feature")
    feature_mod.ShapelyFeature = FakeShapelyFeature
    cartopy_mod = types.ModuleType("cartopy")
    cartopy_mod.crs = crs_mod
    cartopy_mod.feature = feature_mod
    monkeypatch.setitem(sys.modules, "cartopy", cartopy_mod)
    monkeypatch.setitem(sys.modules, "cartopy.crs", crs_mod)
    monkeypatch.setitem(sys.modules, "cartopy.feature", feature_mod)


class TestDrawRegions:
    def test_nan_and_zero_regions_are_drawn(self, monkeypatch, seq_cmap, norm):
        _install_fake_cartopy(monkeypatch)
        ax = _FakeAx()
        df_comb = gpd.GeoDataFrame(
            {
                "adm1_name": ["a", "b", "c"],
                "val": [np.nan, 0.0, 5.0],
                "geometry": [_square(0), _square(2), _square(4)],
            }
        )
        plot._draw_regions(
            ax, df_comb, "adm1_name", "val", "sequential", None, False,
            seq_cmap, norm, 1.0, True, False, "ADM1_NAME",
        )
        # BUG 1 + BUG 2: previously only the 5.0 region reached add_feature.
        assert len(ax.features) == 3
        fcs = [f.kwargs["facecolor"] for f in ax.features]
        assert fcs[0] == (0.85, 0.85, 0.85, 1.0)  # NaN -> excluded gray
        assert fcs[1] == seq_cmap.mpl_colormap(norm(0.0))  # 0 -> colormapped
        assert fcs[2] == seq_cmap.mpl_colormap(norm(5.0))

    def test_drawn_regions_keep_border_style(self, monkeypatch, seq_cmap, norm):
        # Behaviour preservation: the excluded silhouette keeps the normal
        # black border so the country outline stays complete.
        _install_fake_cartopy(monkeypatch)
        ax = _FakeAx()
        df_comb = gpd.GeoDataFrame(
            {"adm1_name": ["a"], "val": [np.nan], "geometry": [_square(0)]}
        )
        plot._draw_regions(
            ax, df_comb, "adm1_name", "val", "sequential", None, False,
            seq_cmap, norm, 1.0, True, False, "ADM1_NAME",
        )
        (feat,) = ax.features
        assert feat.kwargs["edgecolor"] == "black"
        assert feat.kwargs["linewidth"] == 0.5

    def test_qualitative_unmatched_region_is_skipped(self, monkeypatch):
        _install_fake_cartopy(monkeypatch)
        ax = _FakeAx()
        df_comb = gpd.GeoDataFrame(
            {
                "adm1_name": ["a", "b"],
                "val": ["low", "bogus"],
                "geometry": [_square(0), _square(2)],
            }
        )
        plot._draw_regions(
            ax, df_comb, "adm1_name", "val", "qualitative",
            {1: "low", 2: "high"}, False,
            [(255, 0, 0), (0, 255, 0)], None, 1.0, True, False, "ADM1_NAME",
        )
        assert len(ax.features) == 1
        assert ax.features[0].kwargs["facecolor"] == (1.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# BUG 3 — _plot_map_pygmt temp-dir cleanup
# ---------------------------------------------------------------------------

def _pygmt_inputs(tmp_path, seq_cmap):
    attribute_df = gpd.GeoDataFrame(
        {"adm1_name": ["a", "b"], "geometry": [_square(0), _square(2)]},
        crs="EPSG:4326",
    )
    df = pd.DataFrame({"adm1_name": ["a", "b"], "val": [1.0, 2.0]})
    return dict(
        attribute_df=attribute_df, df=df, dict_lup=None,
        merge_col="adm1_name", name_country=None, name_col="val",
        dir_out=str(tmp_path / "maps"), fname="map.png",
        title="t", label="l", vmin=0.0, vmax=10.0,
        cmap=seq_cmap, series="sequential", do_borders=True,
        annotate_regions=False, annotate_region_column="ADM1_NAME",
        continuous_colorbar=True, classify_by="region",
        fixed_range=True,  # keeps _compute_norm off the mapclassify path
        use_key=False,
    )


class TestPygmtTempdirCleanup:
    @staticmethod
    def _spy_mkdtemp(monkeypatch):
        made = []
        real_mkdtemp = tempfile.mkdtemp

        def spy(*args, **kwargs):
            path = real_mkdtemp(*args, **kwargs)
            made.append(path)
            return path

        monkeypatch.setattr(tempfile, "mkdtemp", spy)
        return made

    def test_tmpdir_removed_after_inprocess_render(self, monkeypatch, tmp_path, seq_cmap):
        made = self._spy_mkdtemp(monkeypatch)
        calls = []

        fake_render_mod = types.ModuleType("geocif.viz._pygmt_render")

        def render(gj, params):
            # The handoff files must exist WHILE the renderer runs...
            pj = os.path.join(os.path.dirname(gj), "params.json")
            calls.append((os.path.exists(gj), os.path.exists(pj), "out_path" in params))

        fake_render_mod.render = render
        # Cover both `from . import` resolution orders: the parent-package
        # attribute (if the real module was already imported) and sys.modules.
        monkeypatch.setitem(sys.modules, "geocif.viz._pygmt_render", fake_render_mod)
        import geocif.viz as viz_pkg
        monkeypatch.setattr(viz_pkg, "_pygmt_render", fake_render_mod, raising=False)
        monkeypatch.setattr(plot, "_gmt_available", lambda: True)

        plot._plot_map_pygmt(**_pygmt_inputs(tmp_path, seq_cmap))

        assert calls == [(True, True, True)]
        assert len(made) == 1
        assert os.path.basename(made[0]).startswith("pygmt_map_")
        # ...and the whole dir must be gone AFTER the render (BUG 3).
        assert not os.path.exists(made[0])

    def test_tmpdir_removed_when_bridge_fails(self, monkeypatch, tmp_path, seq_cmap):
        import subprocess

        made = self._spy_mkdtemp(monkeypatch)
        monkeypatch.setattr(plot, "_gmt_available", lambda: False)
        monkeypatch.setattr(
            subprocess, "run",
            lambda *a, **k: types.SimpleNamespace(returncode=1, stderr="boom", stdout=""),
        )

        with pytest.raises(RuntimeError):
            plot._plot_map_pygmt(**_pygmt_inputs(tmp_path, seq_cmap))

        # Cleanup must run on the failure path too (try/finally).
        assert len(made) == 1
        assert not os.path.exists(made[0])
