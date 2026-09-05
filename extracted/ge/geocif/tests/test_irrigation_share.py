"""Tests for the NASS Census irrigated-share predictor (TODO 2.6, Phase A).

Context. County-mean yield and county-mean VI are blends of irrigated and
dryland production whose weights move. In the 2012 drought, US counties over
50% irrigated yielded 1.47x their dryland neighbours while the county model
predicted them only 1.04x higher. ``IRR_SHARE`` supplies the mixing weight;
``IRR_SHARE_X_STRESS`` supplies the interaction, which is the part that
matters because the sign of the irrigation effect flips between stress and
non-stress years.

The properties worth pinning are the ones a silent failure would break:
year-varying join (a Region-only join would collapse the signal to a
constant), interpolation/hold across the 5-yearly census, the non-fatal
missing-file contract, and leak-freedom of the z-score.
"""

import inspect
import pathlib

import numpy as np
import pandas as pd
import pytest

from geocif.cid import definitions as di
from geocif.cid import irrigation as irr


# --------------------------------------------------------------- fixtures
CENSUS_YEARS = [2002, 2007, 2012, 2017, 2022]


def _csv(tmp_path, rows, name="nass_census_irrigated_share.csv"):
    d = tmp_path / "irrigation"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    pd.DataFrame(rows).to_csv(p, index=False)
    return p


def _kansas_rows(shares, crop="maize", county="RICE", state="KS"):
    return [
        {"crop": crop, "state_alpha": state, "state_fips_code": "20",
         "county_ansi": "159", "fips": "20159", "county_name": county,
         "year": y, "irr_acres": 100 * s, "all_acres": 100.0, "irr_share": s}
        for y, s in zip(CENSUS_YEARS, shares)
    ]


# ------------------------------------------------------------ region keys
def test_normalize_region_bridges_the_two_naming_conventions():
    """geocif Regions are "Kansas Rice"; NASS gives KS + "RICE"."""
    assert irr.normalize_region("Kansas Rice") == "kansasrice"
    assert irr.normalize_region("kansas_rice") == "kansasrice"
    assert irr.normalize_region("  KANSAS   RICE ") == "kansasrice"


def test_normalize_region_drops_punctuation_the_sources_disagree_on():
    assert irr.normalize_region("St. Clair") == irr.normalize_region("ST CLAIR")


@pytest.mark.parametrize("shapefile,nass", [
    ("Illinois Dekalb", "illinois DE KALB"),
    ("Illinois Lasalle", "illinois LA SALLE"),
    ("Illinois Dupage", "illinois DU PAGE"),
    ("Indiana Laporte", "indiana LA PORTE"),
    ("Iowa Obrien", "iowa O BRIEN"),
])
def test_internal_spacing_disagreements_still_join(shapefile, nass):
    """These 8 counties genuinely failed to join in a live check against the
    production DB: the boundary file writes them closed up, NASS writes them
    with a space. Collapsing whitespace is what fixes them."""
    assert irr.normalize_region(shapefile) == irr.normalize_region(nass)


def test_normalize_does_not_merge_distinct_counties():
    """Guard the risk collapsing spaces introduces."""
    assert (irr.normalize_region("Wisconsin Green")
            != irr.normalize_region("Wisconsin Green Lake"))
    assert (irr.normalize_region("Kansas Kansas")
            != irr.normalize_region("Arkansas Arkansas"))


def test_state_alpha_map_covers_the_modelled_states():
    modelled = {"AR", "IA", "IL", "IN", "KS", "MN", "MO", "MS", "NE", "OH", "SD"}
    assert modelled <= set(irr.STATE_ALPHA_TO_NAME)
    assert irr.STATE_ALPHA_TO_NAME["SD"] == "south dakota"


# --------------------------------------------------------- interpolation
def test_census_years_are_returned_exactly(tmp_path):
    shares = [0.10, 0.20, 0.30, 0.40, 0.50]
    p = _csv(tmp_path, _kansas_rows(shares))
    out = irr.get_irrigation_frame(p, "maize", years=CENSUS_YEARS)
    got = out.set_index("year")["irr_share"].to_dict()
    for y, s in zip(CENSUS_YEARS, shares):
        assert got[y] == pytest.approx(s), f"census year {y} was altered"


def test_between_census_years_interpolates_linearly(tmp_path):
    p = _csv(tmp_path, _kansas_rows([0.10, 0.20, 0.30, 0.40, 0.50]))
    out = irr.get_irrigation_frame(p, "maize", years=[2012, 2014, 2017])
    got = out.set_index("year")["irr_share"].to_dict()
    # 2014 is 2/5 of the way from 2012 (0.30) to 2017 (0.40)
    assert got[2014] == pytest.approx(0.30 + 0.4 * 0.10)


def test_years_past_the_last_census_hold_flat_not_extrapolate(tmp_path):
    """The census stops at 2022 but forecasts run to 2026. A linear
    extrapolation of a rising share would drift without bound; holding flat is
    the only defensible choice, and it must not exceed 1.0 either."""
    p = _csv(tmp_path, _kansas_rows([0.10, 0.30, 0.50, 0.70, 0.90]))
    out = irr.get_irrigation_frame(p, "maize", years=[2022, 2024, 2026])
    got = out.set_index("year")["irr_share"].to_dict()
    assert got[2024] == pytest.approx(0.90)
    assert got[2026] == pytest.approx(0.90)


def test_years_before_the_first_census_hold_flat(tmp_path):
    p = _csv(tmp_path, _kansas_rows([0.40, 0.30, 0.20, 0.10, 0.05]))
    out = irr.get_irrigation_frame(p, "maize", years=[1998, 2002])
    got = out.set_index("year")["irr_share"].to_dict()
    assert got[1998] == pytest.approx(0.40)


def test_single_census_point_broadcasts(tmp_path):
    rows = _kansas_rows([0.33])[:1]
    rows[0]["year"] = 2017
    p = _csv(tmp_path, rows)
    out = irr.get_irrigation_frame(p, "maize", years=[2005, 2017, 2026])
    assert set(out["irr_share"].round(4)) == {0.33}


# ------------------------------------------------- non-fatal contract
def test_missing_file_returns_none_not_an_exception(tmp_path):
    """Mirrors cid/cci.py: an optional predictor must never fail a run."""
    assert irr.get_irrigation_frame(tmp_path / "nope.csv", "maize") is None


def test_missing_columns_returns_none(tmp_path):
    p = _csv(tmp_path, [{"crop": "maize", "year": 2012}])  # no irr_share
    assert irr.get_irrigation_frame(p, "maize") is None


def test_uncovered_crop_returns_empty_frame_not_none(tmp_path):
    """Empty (a no-op merge) is different from None (a broken file); the
    caller logs them differently."""
    p = _csv(tmp_path, _kansas_rows([0.1] * 5, crop="maize"))
    out = irr.get_irrigation_frame(p, "soybean", years=CENSUS_YEARS)
    assert out is not None and out.empty


# --------------------------------------------------------- registration
def test_annual_region_block_is_registered():
    assert set(di.dict_annual_region) == {"IRR_SHARE", "IRR_SHARE_X_STRESS"}
    assert di.ANNUAL_REGION_COL_MAP["IRR_SHARE"] == "irr_share"
    # Both share a Type so `use_cids = ['Irrigation']` selects the pair.
    assert {m[0] for m in di.dict_annual_region.values()} == {"Irrigation"}


def test_annual_region_block_is_disjoint_from_static_eo():
    assert not (set(di.dict_annual_region) & set(di.dict_static_eo))


def test_create_feature_names_force_includes_the_annual_block():
    src = (pathlib.Path(__import__("geocif").__file__).parent
           / "geocif.py").read_text(encoding="utf-8", errors="ignore")
    assert "di.dict_annual_region.items()" in src, (
        "annual region features are never added to feature_names, so gOMP "
        "can never select them"
    )
    assert "df = self._add_annual_region_features(df)" in src


# ------------------------------------------------- the year-varying join
class _Stub:
    """Minimal stand-in exposing only what the join method touches."""

    _add_annual_region_features = None  # bound below

    def __init__(self, csv_path, crop="maize", use=True):
        import configparser
        import logging

        self.parser = configparser.ConfigParser()
        self.parser.add_section("PATHS")
        self.parser.set("PATHS", "dir_metadata", str(csv_path.parent.parent))
        self.crop = crop
        self.country = "united_states_of_america"
        self.use_irrigation_share = use
        self.logger = logging.getLogger("stub")


def _run_join(stub, df):
    from geocif.geocif import Geocif

    return Geocif._add_annual_region_features(stub, df)


def _frame():
    return pd.DataFrame({
        "Region": ["Kansas Rice"] * 3 + ["Kansas Ford"] * 3,
        "Harvest Year": [2012, 2017, 2022] * 2,
    })


def test_join_is_year_varying_not_constant(tmp_path):
    """THE distinguishing property. A Region-only join (the static-EO path)
    would give one region a single constant and destroy the signal."""
    rows = _kansas_rows([0.0, 0.0, 0.20, 0.50, 0.80], county="RICE")
    rows += [dict(r, county_name="FORD", county_ansi="057", fips="20057")
             for r in _kansas_rows([0.0, 0.0, 0.90, 0.90, 0.90], county="FORD")]
    p = _csv(tmp_path, rows)
    out = _run_join(_Stub(p), _frame())
    rice = out[out.Region == "Kansas Rice"].set_index("Harvest Year")["IRR_SHARE"]
    assert rice[2012] == pytest.approx(0.20)
    assert rice[2017] == pytest.approx(0.50)
    assert rice[2022] == pytest.approx(0.80)
    assert rice.nunique() == 3, "IRR_SHARE collapsed to a per-region constant"


def test_join_keeps_regions_distinct(tmp_path):
    rows = _kansas_rows([0.1] * 5, county="RICE")
    rows += [dict(r, county_name="FORD", county_ansi="057", fips="20057",
                  irr_share=0.9) for r in _kansas_rows([0.9] * 5, county="FORD")]
    p = _csv(tmp_path, rows)
    out = _run_join(_Stub(p), _frame())
    assert out[out.Region == "Kansas Rice"]["IRR_SHARE"].mean() == pytest.approx(0.1)
    assert out[out.Region == "Kansas Ford"]["IRR_SHARE"].mean() == pytest.approx(0.9)


def test_flag_off_is_a_no_op(tmp_path):
    """Default False must leave every other project bit-for-bit unchanged."""
    p = _csv(tmp_path, _kansas_rows([0.5] * 5))
    df = _frame()
    out = _run_join(_Stub(p, use=False), df.copy())
    assert "IRR_SHARE" not in out.columns
    pd.testing.assert_frame_equal(out, df)


def test_missing_csv_leaves_the_frame_untouched(tmp_path):
    (tmp_path / "irrigation").mkdir(parents=True, exist_ok=True)
    stub = _Stub(tmp_path / "irrigation" / "absent.csv")
    df = _frame()
    out = _run_join(stub, df.copy())
    assert "IRR_SHARE" not in out.columns


def test_unmatched_regions_get_nan_not_zero(tmp_path):
    """A county absent from the census must be NaN. Zero would assert
    'this county is entirely dryland', which is a different claim."""
    p = _csv(tmp_path, _kansas_rows([0.5] * 5, county="RICE"))
    df = pd.DataFrame({"Region": ["Kansas Rice", "Kansas Nowhere"],
                       "Harvest Year": [2012, 2012]})
    out = _run_join(_Stub(p), df)
    assert out.loc[out.Region == "Kansas Rice", "IRR_SHARE"].iloc[0] == pytest.approx(0.5)
    assert pd.isna(out.loc[out.Region == "Kansas Nowhere", "IRR_SHARE"].iloc[0])


# ------------------------------------------------------- the interaction
class _IStub:
    def __init__(self, train, test, stress="MEAN_ESI4WK", use=True):
        import logging

        self.df_train = train
        self.df_test = test
        self.use_irrigation_share = use
        self.irrigation_stress_cid = stress
        self.countries_pooled = None
        self.country = "usa"
        self.crop = "maize"
        self.logger = logging.getLogger("stub")

    def _df_train_leakfree(self, df_train=None):
        return self.df_train if df_train is None else df_train


def _interaction(stub):
    from geocif.geocif import Geocif

    Geocif._add_irrigation_interaction(stub)


def _train_test(stress_train, stress_test, share=0.5):
    train = pd.DataFrame({
        "Region": ["A"] * len(stress_train),
        "Harvest Year": list(range(2010, 2010 + len(stress_train))),
        "IRR_SHARE": share,
        "MEAN_ESI4WK Jul 1-Jul 31": stress_train,
    })
    test = pd.DataFrame({
        "Region": ["A"],
        "Harvest Year": [2026],
        "IRR_SHARE": [share],
        "MEAN_ESI4WK Jul 1-Jul 31": [stress_test],
    })
    return train, test


def test_interaction_is_share_times_region_zscore():
    train, test = _train_test([1.0, 2.0, 3.0, 4.0, 5.0], 5.0, share=0.5)
    stub = _IStub(train, test)
    _interaction(stub)
    sd = np.std([1, 2, 3, 4, 5], ddof=1)
    assert stub.df_test["IRR_SHARE_X_STRESS"].iloc[0] == pytest.approx(
        0.5 * (5.0 - 3.0) / sd
    )


def test_zscore_is_fitted_on_training_rows_only():
    """Leak guard. The forecast year's own stress must not enter the mean or
    sd that standardises it -- the class of bug fixed in 0.4.939."""
    train, test = _train_test([1.0, 2.0, 3.0, 4.0, 5.0], 500.0)
    a = _IStub(train.copy(), test.copy())
    _interaction(a)
    # Same training rows, wildly different forecast-year value: the training
    # rows' own interaction values must be identical either way.
    train2, test2 = _train_test([1.0, 2.0, 3.0, 4.0, 5.0], -500.0)
    b = _IStub(train2, test2)
    _interaction(b)
    pd.testing.assert_series_equal(
        a.df_train["IRR_SHARE_X_STRESS"], b.df_train["IRR_SHARE_X_STRESS"]
    )


def test_interaction_flips_sign_with_the_season():
    """The whole point: a stress year and a good year must produce opposite
    signs at the same irrigated share, which a main effect cannot."""
    train, test = _train_test([1.0, 2.0, 3.0, 4.0, 5.0], 5.0)
    good = _IStub(train.copy(), test.copy())
    _interaction(good)
    train2, test2 = _train_test([1.0, 2.0, 3.0, 4.0, 5.0], 1.0)
    bad = _IStub(train2, test2)
    _interaction(bad)
    assert good.df_test["IRR_SHARE_X_STRESS"].iloc[0] > 0
    assert bad.df_test["IRR_SHARE_X_STRESS"].iloc[0] < 0


def test_constant_stress_does_not_produce_infinities():
    train, test = _train_test([2.0, 2.0, 2.0], 2.0)
    stub = _IStub(train, test)
    _interaction(stub)
    assert np.isfinite(stub.df_test["IRR_SHARE_X_STRESS"]).all()
    assert np.isfinite(stub.df_train["IRR_SHARE_X_STRESS"]).all()


def test_missing_stress_cid_keeps_irr_share_and_skips_interaction():
    train, test = _train_test([1.0, 2.0, 3.0], 2.0)
    stub = _IStub(train, test, stress="NOT_A_CID")
    _interaction(stub)
    assert "IRR_SHARE_X_STRESS" not in stub.df_train.columns
    assert "IRR_SHARE" in stub.df_train.columns


def test_interaction_skipped_when_flag_off():
    train, test = _train_test([1.0, 2.0, 3.0], 2.0)
    stub = _IStub(train, test, use=False)
    _interaction(stub)
    assert "IRR_SHARE_X_STRESS" not in stub.df_train.columns


def test_interaction_runs_after_every_split_filter():
    """It must sit at the END of _prepare_train_test_split: the z-score is
    fitted on the FINAL training set, after the min-years and region-anomaly
    filters have dropped regions from both frames."""
    from geocif.geocif import Geocif

    src = inspect.getsource(Geocif._prepare_train_test_split)
    assert "self._add_irrigation_interaction()" in src
    tail = src[src.index("self._add_irrigation_interaction()"):]
    assert "self.df_train = self.df_train[" not in tail, (
        "a df_train filter runs AFTER the interaction is built"
    )


# ------------------------------------------------------------ downloader
def test_downloader_filters_the_two_things_that_break_the_sum():
    """domaincat_desc repeats each county's acreage by farm-size domain, and
    OTHER (COMBINED) COUNTIES rows carry no county identity. Missing either
    filter silently multiplies or misattributes acres."""
    import importlib.util

    p = (pathlib.Path(__file__).resolve().parents[2] / "geoprepare" /
         "geoprepare" / "datasets" / "NASS_IRRIGATION.py")
    if not p.exists():
        pytest.skip("geoprepare checkout not alongside geocif")
    spec = importlib.util.spec_from_file_location("nass_irr", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    recs = [
        {"county_ansi": "159", "domaincat_desc": "NOT SPECIFIED", "Value": "1,000",
         "year": "2022", "state_alpha": "KS", "state_fips_code": "20",
         "county_name": "RICE"},
        {"county_ansi": "159", "domaincat_desc": "AREA OPERATED: (1.0 TO 9.9 ACRES)",
         "Value": "400", "year": "2022", "state_alpha": "KS",
         "state_fips_code": "20", "county_name": "RICE"},
        {"county_ansi": "", "domaincat_desc": "NOT SPECIFIED", "Value": "500",
         "year": "2022", "state_alpha": "KS", "state_fips_code": "20",
         "county_name": "OTHER (COMBINED) COUNTIES"},
    ]
    out = mod._records_to_frame(recs, "maize")
    assert len(out) == 1, "domain or combined-county rows leaked into the sum"
    assert out["acres"].iloc[0] == 1000.0
