"""[ML] stress_switch — fit a LOOCV fold without detrending when the national
Jun-Aug NDVI predicts a collapse year (ml/stress_switch.py). Validated for
United States maize only."""
from configparser import ConfigParser
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

from geocif.geocif import Geocif
from geocif.ml import stress_switch as sw

ROOT = Path(__file__).resolve().parents[1] / "geocif"
TARGET = "Yield (tn per ha)"
YEARS = list(range(2001, 2026))
COLLAPSE = 2012
# Deterministic national NDVI signal: ordinary years within about +-1.5 sd, 2012 a -4 sd drought.
Z = {y: (-4.0 if y == COLLAPSE else 1.2 * np.sin(1.7 * y)) for y in YEARS}


def _panel(n_regions=12):
    """Regions whose yield anomaly tracks the national NDVI signal (3% per sd)
    around a linear trend; area constant per region."""
    rng = np.random.default_rng(0)
    rows = []
    for i in range(n_regions):
        for y in YEARS:
            trend = 6.0 + 0.1 * i + 0.12 * (y - 2001)
            rows.append({"Region": f"R{i}", "Harvest Year": y,
                         TARGET: trend * (1 + 0.03 * Z[y] + rng.normal(0, 0.005)),
                         "Area (ha)": 1000.0 + 50 * i,
                         "ndvi": 0.7 + 0.05 * Z[y] + rng.normal(0, 0.002)})
    return pd.DataFrame(rows)


def _series(df, col):
    return df.set_index(["Region", "Harvest Year"])[col].astype(float)


def _decide(year, df=None, drop_ndvi_year=None):
    df = _panel() if df is None else df
    train = df[df["Harvest Year"] != year]
    ndvi = _series(df, "ndvi")
    if drop_ndvi_year is not None:
        ndvi = ndvi[ndvi.index.get_level_values(1) != drop_ndvi_year]
    return sw.predict_shock(_series(train, TARGET), _series(df, "Area (ha)"), ndvi, year)


# ---------------------------------------------------------------------------
# the rule
# ---------------------------------------------------------------------------

def test_fires_in_the_collapse_year():
    r = _decide(COLLAPSE)
    assert r["fired"], r
    assert r["s_hat"] < -r["tau"]


def test_quiet_in_ordinary_years():
    fired = [y for y in range(2005, 2026) if y != COLLAPSE and _decide(y)["fired"]]
    assert fired == [], f"false alarms in {fired}"


def test_held_out_yield_is_never_used():
    """Passing the held-out year's observed yield (even absurd) changes nothing."""
    df = _panel()
    base = _decide(COLLAPSE, df)
    leaky = df.copy()
    leaky.loc[leaky["Harvest Year"] == COLLAPSE, TARGET] = 999.0
    r = sw.predict_shock(_series(leaky, TARGET), _series(df, "Area (ha)"), _series(df, "ndvi"), COLLAPSE)
    assert r["s_hat"] == base["s_hat"] and r["tau"] == base["tau"]


def test_missing_signal_for_the_year_keeps_trend_on():
    r = _decide(COLLAPSE, drop_ndvi_year=COLLAPSE)
    assert not r["fired"] and "signal" in r["reason"]


def test_too_few_training_years_keeps_trend_on():
    df = _panel()
    df = df[df["Harvest Year"] >= 2019]
    r = _decide(2022, df)
    assert not r["fired"] and r["reason"]


# ---------------------------------------------------------------------------
# signal extraction
# ---------------------------------------------------------------------------

def _long(stage_ids=("8_7_6", "10_9_8_7_6_5_4")):
    rows = []
    for s in stage_ids:
        for idx in ("MEAN_NDVI", "MAX_NDVI"):
            rows.append({"Region": "R0", "Harvest Year": 2012, "Index": idx, "Stage_ID": s,
                         "CID": 0.5 if (idx == "MEAN_NDVI" and s == "8_7_6") else 9.0})
    return pd.DataFrame(rows)


def test_extract_signal_picks_mean_ndvi_jun_aug():
    s = sw.extract_signal(_long())
    assert s.loc[("R0", 2012)] == 0.5 and len(s) == 1


def test_extract_signal_none_when_stage_lacks_the_window():
    """A July stage has no 8_7_6 rows: the switch cannot read August NDVI."""
    assert sw.extract_signal(_long(stage_ids=("7_6_5",))) is None


def test_extract_signal_keeps_missing_values_missing():
    d = _long()
    d.loc[(d["Index"] == "MEAN_NDVI") & (d["Stage_ID"] == "8_7_6"), "CID"] = np.nan
    assert sw.extract_signal(d) is None, "a missing NDVI must never become 0"


# ---------------------------------------------------------------------------
# US maize only
# ---------------------------------------------------------------------------

def test_validated_only_for_us_maize():
    assert sw.is_validated("united_states_of_america", "maize")
    assert sw.is_validated("United States Of America", "Maize")
    assert not sw.is_validated("united_states_of_america", "soybean")
    assert not sw.is_validated("kenya", "maize")
    assert not sw.is_validated("pooled", "maize")


def _parser(**ml):
    p = ConfigParser()
    p["ML"] = {k: str(v) for k, v in ml.items()}
    return p


def test_settings_default_on_for_us_maize():
    assert sw.settings(_parser()) == (True, ["united_states_of_america"], ["maize"])


def test_settings_read_and_normalise_the_lists():
    on, countries, crops = sw.settings(_parser(
        stress_switch=False, stress_switch_countries="['United States Of America', 'Kenya']",
        stress_switch_crops="['Maize']"))
    assert on is False
    assert countries == ["united_states_of_america", "kenya"] and crops == ["maize"]


def test_applies_needs_both_country_and_crop():
    c, k = ["united_states_of_america"], ["maize"]
    assert sw.applies("United States Of America", "maize", c, k)
    assert not sw.applies("united_states_of_america", "soybean", c, k)
    assert not sw.applies("kenya", "maize", c, k)


# ---------------------------------------------------------------------------
# wiring in Geocif
# ---------------------------------------------------------------------------

class _Log:
    def __init__(self):
        self.lines = []

    def info(self, m):
        self.lines.append(m)

    warning = info


def _stub(country="united_states_of_america", crop="maize", year=COLLAPSE, **kw):
    df = _panel()
    long = df.assign(Index="MEAN_NDVI", Stage_ID="8_7_6", CID=df["ndvi"])
    o = SimpleNamespace(
        stress_switch=True, ml_model=True, check_yield_trend=True, model_type="REGRESSION",
        target=TARGET, target_column=f"Detrended {TARGET}", country=country, crop=crop,
        forecast_season=year, df_train=df[df["Harvest Year"] != year].copy(),
        df_test=df[df["Harvest Year"] == year].copy(), _stress_ndvi=sw.extract_signal(long),
        _stress_switched=False, logger=_Log(), use_yield_trend_as_feature="all",
        use_trend_all_as_feature=True,
        stress_switch_countries=list(sw.DEFAULT_COUNTRIES), stress_switch_crops=list(sw.DEFAULT_CROPS),
    )
    o._refresh_target_column = lambda: Geocif._refresh_target_column(o)
    for k, v in kw.items():
        setattr(o, k, v)
    return o


def test_switch_turns_detrending_off_for_the_fold():
    o = _stub()
    Geocif._apply_stress_switch(o)
    assert o._stress_switched and o.check_yield_trend is False
    assert o.target_column == TARGET
    assert any("SWITCH" in m for m in o.logger.lines)


def test_ordinary_year_keeps_detrending():
    o = _stub(year=2015)
    Geocif._apply_stress_switch(o)
    assert not o._stress_switched and o.check_yield_trend is True


def test_soybean_not_switched_by_default():
    o = _stub(crop="soybean")
    Geocif._apply_stress_switch(o)
    assert not o._stress_switched and o.check_yield_trend is True


def test_other_country_not_switched_by_default():
    o = _stub(country="kenya")
    Geocif._apply_stress_switch(o)
    assert not o._stress_switched and o.check_yield_trend is True


def test_configured_unvalidated_pair_runs_with_a_warning():
    o = _stub(country="kenya", stress_switch_countries=["kenya"])
    Geocif._apply_stress_switch(o)
    assert o._stress_switched
    assert any("NOT validated" in m for m in o.logger.lines)


def test_flag_off_does_nothing():
    o = _stub(stress_switch=False)
    Geocif._apply_stress_switch(o)
    assert not o._stress_switched and o.check_yield_trend is True


def test_baselines_are_never_switched():
    o = _stub(ml_model=False)
    Geocif._apply_stress_switch(o)
    assert not o._stress_switched


def test_stage_without_window_keeps_detrending():
    o = _stub(_stress_ndvi=None)
    Geocif._apply_stress_switch(o)
    assert not o._stress_switched and o.check_yield_trend is True


def test_switched_fold_gets_no_trend_features():
    """The validated fallback had no trend feature, even when the config
    turns use_yield_trend_as_feature / use_trend_all_as_feature on."""
    o = _stub()
    Geocif._apply_stress_switch(o)
    Geocif._compute_yield_trend_feature(o)
    Geocif._compute_trend_all_feature(o)
    assert "Yield Trend" not in o.df_train.columns
    assert "Trend All" not in o.df_train.columns


def test_restore_runs_before_the_split_reads_the_flag():
    """A switched stage must hand the next stage check_yield_trend=True before
    _prepare_train_test_split reads it (region_anomaly branch)."""
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("def _prepare_train_test_split")
    block = src[i:src.index("def ", i + 10)]
    r = block.index('if getattr(self, "_stress_switched", False):')
    assert r < block.index('mask = df["Harvest Year"] == self.forecast_season')
    assert r < block.index("and not self.check_yield_trend")


def test_switch_runs_after_the_trend_diagnostic():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("def _compute_detrended_yield")
    block = src[i:src.index("def _apply_stress_switch", i)]
    assert block.index("check_yield_trend_diagnostic") < block.index("self._apply_stress_switch()")


def test_first_year_of_record_keeps_its_weight():
    """No area before the record starts (usa_admin1 begins in 2002): the first
    year falls back to the earliest-3-year mean instead of dropping out of the
    fit — dropping usa_admin1's 2002 drought hid the 2012 signal in 0.4.1060."""
    area = {("A", 2002): 10.0, ("A", 2003): 20.0, ("A", 2004): 30.0, ("A", 2005): 40.0}
    first = {"A": 20.0}
    assert sw._trailing_area(area, "A", 2002, first) == 20.0
    assert sw._trailing_area(area, "A", 2005, first) == 20.0  # 2002-2004 trailing mean
    assert sw._trailing_area(area, "A", 2004, first) == 15.0  # 2002-2003
    assert np.isnan(sw._trailing_area(area, "B", 2002, first))


def test_record_start_year_still_counts_toward_the_signal():
    """Dropping the area of the first year must not change the decision."""
    df = _panel()
    df = df[df["Harvest Year"] >= 2002]
    train = df[df["Harvest Year"] != COLLAPSE]
    r = sw.predict_shock(_series(train, TARGET), _series(df, "Area (ha)"), _series(df, "ndvi"), COLLAPSE)
    assert r["fired"], r
