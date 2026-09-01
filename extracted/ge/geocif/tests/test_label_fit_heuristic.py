"""Tests for the geometry-aware region-label suppression heuristic.

Motivating failure (2026-08-31): a Kenya admin_2 MAPE map drew a name label on
every one of ~90 sub-counties. The old rule was a pure COUNT cap
(_ANNOTATE_MAX_REGIONS = 200), so 90 slipped under it — yet the western cluster
of counties is tiny in map units and the labels became an unreadable smear,
while big northern counties (Turkana, Wajir) labelled fine.

The heuristic therefore has to discriminate on polygon size RELATIVE to the map
extent, not on count: Kenya admin_2 must suppress, US admin_1 (a similar count
of much larger polygons) must keep.
"""

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import box

from geocif.viz import plot


def _grid(n_x, n_y, cell, names, x0=0.0, y0=0.0):
    """n_x*n_y square polygons of side ``cell`` degrees, cycling ``names``."""
    geoms, labels = [], []
    for i in range(n_x):
        for j in range(n_y):
            geoms.append(box(x0 + i * cell, y0 + j * cell,
                             x0 + (i + 1) * cell, y0 + (j + 1) * cell))
            labels.append(names[len(geoms) % len(names)])
    return gpd.GeoDataFrame({"ADM_NAME": labels}, geometry=geoms, crs="EPSG:4326")


@pytest.fixture(autouse=True)
def _reset_flag():
    plot.set_auto_label_fit(True)
    yield
    plot.set_auto_label_fit(True)


def test_large_polygons_keep_labels():
    """~50 US-state-sized polygons: a few % of map width each, names fit."""
    gdf = _grid(7, 7, 8.0, ["Iowa", "Ohio", "Texas"])  # 56deg-wide map
    frac = plot.label_fit_fraction(gdf, "ADM_NAME")
    assert frac == pytest.approx(1.0)
    assert plot.effective_annotate_regions(True, len(gdf), gdf=gdf,
                                           label_col="ADM_NAME") is True


def test_small_dense_polygons_suppress_labels():
    """Kenya-shaped: a dense cluster of small counties inside a wide extent.

    Real numbers this mimics (measured on ken_adm2.shp / brazil_mt): a ~8 deg
    wide country whose populated cluster has ~0.3 deg counties. Verified fit:
    Kenya admin_2 9%, brazil_mt admin_2 17% — both well under the threshold.
    """
    small = _grid(7, 6, 0.3, ["Vihiga", "Nyamira", "Trans Nzoia",
                              "Elgeyo-Marakwet"], x0=0.0)
    # a few large outlying regions widen the extent, exactly as Turkana/Wajir do
    big = _grid(2, 2, 1.6, ["Turkana", "Wajir"], x0=5.0)
    gdf = gpd.GeoDataFrame(pd.concat([small, big], ignore_index=True),
                           crs="EPSG:4326")
    frac = plot.label_fit_fraction(gdf, "ADM_NAME")
    assert frac < plot._MIN_LABEL_FIT_FRACTION, f"fit={frac}"
    assert plot.effective_annotate_regions(True, len(gdf), gdf=gdf,
                                           label_col="ADM_NAME") is False


def test_one_far_outlier_does_not_suppress_a_labellable_map():
    """Robust extent: an Alaska-like outlier must not sink the whole map.

    With total_bounds this returned 6% for US Level_1 (359 deg extent) and
    wrongly suppressed labels; the 2.5/97.5 percentile span gives 57%.
    """
    main = _grid(7, 7, 8.0, ["Iowa", "Ohio", "Texas"], x0=0.0)
    outlier = _grid(1, 1, 8.0, ["Alaska"], x0=300.0)
    gdf = gpd.GeoDataFrame(pd.concat([main, outlier], ignore_index=True),
                           crs="EPSG:4326")
    assert plot.label_fit_fraction(gdf, "ADM_NAME") >= plot._MIN_LABEL_FIT_FRACTION
    assert plot.effective_annotate_regions(True, len(gdf), gdf=gdf,
                                           label_col="ADM_NAME") is True


def test_count_cap_still_applies():
    """Above the polygon-count cap, suppress regardless of fit."""
    gdf = _grid(21, 21, 8.0, ["A"])          # 441 polygons, all easily fit
    assert plot.label_fit_fraction(gdf, "ADM_NAME") == pytest.approx(1.0)
    assert len(gdf) > plot._ANNOTATE_MAX_REGIONS
    assert plot.effective_annotate_regions(True, len(gdf), gdf=gdf,
                                          label_col="ADM_NAME") is False


def test_flag_false_forces_labels_on():
    """[ML] annotate_regions_auto = False honours annotate_regions literally."""
    gdf = _grid(10, 9, 0.25, ["Elgeyo-Marakwet"])
    assert plot.effective_annotate_regions(True, len(gdf), gdf=gdf,
                                          label_col="ADM_NAME") is False
    plot.set_auto_label_fit(False)
    assert plot.effective_annotate_regions(True, len(gdf), gdf=gdf,
                                          label_col="ADM_NAME") is True
    # ...but never overrides an explicit annotate_regions = False
    assert plot.effective_annotate_regions(False, len(gdf), gdf=gdf,
                                          label_col="ADM_NAME") is False


def test_label_length_matters_not_just_size():
    """Same geometry, longer names -> fewer fit. Guards against a size-only rule."""
    # cells span ~1/30 of the extent (0.033): a 2-char name needs 0.014 and
    # fits, a 22-char one needs 0.154 and does not. Identical geometry, so only
    # the label length can change the verdict.
    short = _grid(30, 3, 1.0, ["Ab"])
    long_ = _grid(30, 3, 1.0, ["Elgeyo-Marakwet County"])
    f_short = plot.label_fit_fraction(short, "ADM_NAME")
    f_long = plot.label_fit_fraction(long_, "ADM_NAME")
    assert f_short > f_long, f"short={f_short} long={f_long}"
    assert f_short >= plot._MIN_LABEL_FIT_FRACTION
    assert f_long < plot._MIN_LABEL_FIT_FRACTION


def test_annotate_regions_false_short_circuits():
    assert plot.effective_annotate_regions(False, 5) is False


def test_missing_geometry_or_labels_is_not_fatal():
    """No gdf / no label column -> fall back to the count rule, never raise."""
    assert plot.label_fit_fraction(None) is None
    gdf = _grid(3, 3, 5.0, ["Ok"]).drop(columns=["ADM_NAME"])
    assert plot.label_fit_fraction(gdf, "ADM_NAME") is None
    # small count, unknown fit -> labels kept
    assert plot.effective_annotate_regions(True, len(gdf), gdf=gdf,
                                          label_col="ADM_NAME") is True
