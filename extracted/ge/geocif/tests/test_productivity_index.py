"""Tests for the MSU/USFS Productivity Index (PI) static feature.

PI is an ordinal 0-19 soil-productivity rank (Schaetzl, Krist & Miller 2012),
240 m, CONUS-only, derived from SSURGO 2012. It rides the existing static
per-region machinery (``dict_static_eo`` / ``STATIC_EO_COL_MAP`` ->
``geocif._add_static_eo_features``), so the tests here pin the wiring and the
three data hazards found while ingesting the raster:

1. Source CRS is EPSG:5070, but ``get_common_bounds_and_shape`` reconciles
   resolution and extent only -- it assumes raster and geometry share a CRS.
   Hence the ingestion warp to EPSG:4326.
2. The shipped ``.ovr`` pyramid was built with AVERAGING, so a decimated read
   returns values 20-29 that are not in the legend. Nearest resampling only,
   no overviews, and a legend guard at the point of use.
3. The legend carries a ``-1`` class alongside 0-19 that is NOT a productivity
   value. ``Resampling.average`` in ``_soil_band_on_afi_grid`` excludes only
   the declared nodata, so ``-1`` is folded into ``-128`` at ingestion.
"""

import pathlib

import numpy as np
import pandas as pd
import pytest

from geocif.cid import definitions as di

GEOPREPARE = (pathlib.Path(__file__).resolve().parents[2] / "geoprepare"
              / "geoprepare")


# ------------------------------------------------------------ registration
def test_pi_registered_as_static_feature():
    assert "PI" in di.dict_static_eo
    assert di.STATIC_EO_COL_MAP["PI"] == "pi"
    assert di.dict_pi["PI"][0] == "Soil", (
        "PI must share the 'Soil' Type so use_cids = ['Soil'] admits it"
    )


def test_pi_declares_its_source_dataset():
    """STATIC_COLUMN_SOURCE is what turns a missing column into an accurate
    diagnosis instead of sending someone after a re-extract for the wrong
    dataset."""
    assert di.STATIC_COLUMN_SOURCE["pi"] == "pi"


def test_pi_is_static_not_annual():
    """PI is one value per region forever (SSURGO 2012 vintage). If it ever
    lands in dict_annual_region it would be joined on Harvest Year too and
    silently duplicated."""
    assert "PI" not in di.dict_annual_region
    assert not (set(di.dict_static_eo) & set(di.dict_annual_region))


def test_existing_static_features_are_untouched():
    """Guard against a merge that drops aridity or soilgrids."""
    assert {"AI", "SOIL_SAND", "SOIL_CLAY", "SOIL_SOC", "SOIL_BDOD"} <= set(
        di.dict_static_eo
    )


# ------------------------------------------------------- feature admission
def test_bare_pi_column_survives_the_cid_filter():
    """usa_admin2 runs correlation_plots = False, which takes the branch that
    REPLACES feature_names with get_cid_column_names(df_train) and never
    reaches the force-include block. If PI did not survive that filter it
    would be silently dropped and the A/B arms would come out identical --
    the bug that wasted the CCI arms."""
    from geocif import utils

    df = pd.DataFrame({
        "Region": ["a"], "Harvest Year": [2012], "Yield (tn per ha)": [1.0],
        "MEAN_NDVI Jul 1-Jul 31": [0.5], "PI": [12.5],
    })
    cols = utils.filter_cid_columns(
        df, ["Region", "Harvest Year"], "Yield (tn per ha)", []
    )
    assert "PI" in cols


def test_static_eo_join_is_driven_by_the_col_map():
    """_add_static_eo_features iterates STATIC_EO_COL_MAP, so registering PI
    there is the whole integration -- no geocif.py change. Pin that."""
    src = (pathlib.Path(__import__("geocif").__file__).parent
           / "geocif.py").read_text(encoding="utf-8", errors="ignore")
    assert "for cid_name, raw_col in di.STATIC_EO_COL_MAP.items():" in src
    assert "for _name, _meta in di.dict_static_eo.items():" in src


# --------------------------------------------------------- the legend guard
LEGEND_CASES = [
    (-128.0, False, "nodata sentinel"),
    (-1.0, False, "the not-rated class"),
    (0.0, True, "least productive, a REAL value"),
    (5.0, True, "mid legend"),
    (12.5, True, "fractional, from area-averaging 240 m into a 5 km cell"),
    (19.0, True, "most productive, upper bound inclusive"),
    (20.0, False, "just past the legend"),
    (25.0, False, "the averaged-overview artifact"),
]


@pytest.mark.parametrize("value,keep,why", LEGEND_CASES)
def test_legend_guard_selects_exactly_the_valid_range(value, keep, why):
    """The predicate process_pi applies before taking the mean."""
    band = np.array([[value]], dtype="float32")
    crop_valid = np.array([[True]])
    valid = ~np.isnan(band) & crop_valid & (band >= 0) & (band <= 19)
    assert bool(valid[0, 0]) is keep, f"{value} ({why})"


def test_legend_guard_drops_nan():
    band = np.array([[np.nan]], dtype="float32")
    valid = ~np.isnan(band) & np.array([[True]]) & (band >= 0) & (band <= 19)
    assert not valid.any()


def test_legend_guard_respects_the_crop_mask():
    """A perfectly valid PI value outside cropland must not enter the mean --
    that is the whole reason PI is cropland-weighted rather than a plain
    polygon mean like aridity."""
    band = np.array([[12.0, 12.0]], dtype="float32")
    crop_valid = np.array([[True, False]])
    valid = ~np.isnan(band) & crop_valid & (band >= 0) & (band <= 19)
    assert valid.tolist() == [[True, False]]


def test_mean_over_guarded_pixels_ignores_sentinels():
    """End-to-end arithmetic: sentinels must not drag the mean."""
    band = np.array([[-128.0, -1.0, 10.0, 14.0, 25.0]], dtype="float32")
    crop_valid = np.ones_like(band, dtype=bool)
    valid = ~np.isnan(band) & crop_valid & (band >= 0) & (band <= 19)
    assert float(np.nanmean(band[valid])) == pytest.approx(12.0)


# ------------------------------------------------------- geoprepare wiring
@pytest.mark.skipif(not GEOPREPARE.exists(),
                    reason="geoprepare checkout not alongside geocif")
def test_process_pi_exists_and_is_dispatched():
    src = (GEOPREPARE / "extract" / "extract_EO.py").read_text(
        encoding="utf-8", errors="ignore")
    assert "def process_pi(" in src
    assert 'if var == "pi":' in src
    assert "process_pi(params, country, crop, scale, afi_file, df_country)" in src


@pytest.mark.skipif(not GEOPREPARE.exists(),
                    reason="geoprepare checkout not alongside geocif")
def test_process_pi_is_cropland_weighted_and_crs_safe():
    """Two design commitments worth pinning: PI goes through
    build_crop_valid_mask (cropland weighting, unlike aridity) and through
    _soil_band_on_afi_grid (which reprojects onto the AFI window and so
    tolerates the differing source grid)."""
    src = (GEOPREPARE / "extract" / "extract_EO.py").read_text(
        encoding="utf-8", errors="ignore")
    body = src[src.index("def process_pi("):]
    body = body[:body.index("\ndef ", 1)]
    assert "build_crop_valid_mask" in body, "PI is not cropland-weighted"
    assert "_soil_band_on_afi_grid" in body, "PI is not reprojected onto the AFI grid"
    assert "(band >= 0) & (band <= 19)" in body, "legend guard missing"
    assert 'pi_4326.tif' in body, "PI must read the WARPED raster, not the 5070 source"


@pytest.mark.skipif(not GEOPREPARE.exists(),
                    reason="geoprepare checkout not alongside geocif")
def test_geomerge_treats_pi_as_a_static_left_join():
    """pi has no time dimension, so it must be ordered with the other statics
    and LEFT-joined -- an outer join would multiply rows."""
    src = (GEOPREPARE / "geomerge.py").read_text(encoding="utf-8", errors="ignore")
    assert '1 if v in ("aef", "soilgrids", "aridity", "pi")' in src
    assert 'elif var == "pi":' in src
    assert '["country", "region", "region_id", "pi"]' in src
    assert '"aridity", "pi") else "left"' in src
