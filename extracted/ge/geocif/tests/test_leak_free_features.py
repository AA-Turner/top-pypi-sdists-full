"""Leakage guards for engineered features (audit of 2026-08-25).

Two channels let information that is unavailable at deployment time reach
hindcast folds:

1. ``compute_median_statistics`` picked the *closest* years in either
   direction (``only_historic=False`` default of ``compute_closest_years``),
   so a 2018 row's "Median Yield" averaged 2019/2020 observations. The column
   re-entered the feature set through the ``nbr_`` neighbor wrapper even with
   ``median_yield_as_feature = False`` — it was selected by gOMP in ~every
   fold of the Kenya runs.

2. ``add_neighbor_features`` computed its per-region ``yield_medians`` from
   the frame being augmented. For a LOOCV test frame (held-out year WITH its
   observed yields) that made ``nbr_mean_yield_hist`` the weighted mean of
   the neighbors' observed yields in the very year being predicted.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.ml import feature_engineering as fe
from geocif.ml import spatial_neighbors as sn

ROOT = Path(__file__).resolve().parents[1] / "geocif"
TARGET = "Yield (tn per ha)"


# ---------------------------------------------------------------------------
# compute_median_statistics
# ---------------------------------------------------------------------------

def _median_df(years=range(2010, 2020)):
    """One region; yield encodes the year so contributions are traceable."""
    return pd.DataFrame({
        "Region": "A",
        "Harvest Year": list(years),
        TARGET: [float(y - 100) for y in years],
    })


def test_median_yield_uses_only_past_years():
    df = _median_df()
    out = fe.compute_median_statistics(df.copy(), list(range(2010, 2020)), 3, TARGET)
    got = out.loc[out["Harvest Year"] == 2015, f"Median {TARGET}"].iloc[0]
    # closest 3 strictly-before years: 2012, 2013, 2014
    assert got == np.mean([1912.0, 1913.0, 1914.0]), got


def test_median_yield_earliest_year_is_nan_not_future():
    df = _median_df()
    out = fe.compute_median_statistics(df.copy(), list(range(2010, 2020)), 3, TARGET)
    got = out.loc[out["Harvest Year"] == 2010, f"Median {TARGET}"].iloc[0]
    # no history exists; a future-only window (old behavior) would be ~1911.x
    assert np.isnan(got), got


def test_median_yield_old_behavior_reachable_but_not_default():
    """only_historic=False reproduces the future-contaminated value."""
    df = _median_df()
    past_only = np.mean([1912.0, 1913.0, 1914.0])
    out = fe.compute_median_statistics(
        df.copy(), list(range(2010, 2020)), 3, TARGET, only_historic=False
    )
    got = out.loc[out["Harvest Year"] == 2015, f"Median {TARGET}"].iloc[0]
    assert got != past_only, "closest-either-side must include a future year"


# ---------------------------------------------------------------------------
# add_neighbor_features
# ---------------------------------------------------------------------------

def _train_test_frames():
    """A and B are mutual neighbors. Train = 2010-2014 (yields ~2);
    test = held-out 2015 whose OBSERVED yields are a screaming 999."""
    rows = []
    for region, base in (("A", 2.0), ("B", 3.0)):
        for y in range(2010, 2015):
            rows.append({"Region": region, "Harvest Year": y,
                         TARGET: base, "f1": float(y)})
    df_train = pd.DataFrame(rows)
    df_test = pd.DataFrame([
        {"Region": "A", "Harvest Year": 2015, TARGET: 999.0, "f1": 2015.0},
        {"Region": "B", "Harvest Year": 2015, TARGET: 999.0, "f1": 2015.0},
    ])
    graph = {"A": [("B", 1.0)], "B": [("A", 1.0)]}
    return df_train, df_test, graph


def test_nbr_yield_hist_on_test_comes_from_train():
    df_train, df_test, graph = _train_test_frames()
    out = sn.add_neighbor_features(
        df_test, graph, ["f1"], yield_col=TARGET, df_source=df_train
    )
    a = out.loc[out["Region"] == "A", "nbr_mean_yield_hist"].iloc[0]
    assert a == 3.0, f"A's neighbor median must be B's TRAIN median, got {a}"
    assert not (out["nbr_mean_yield_hist"] == 999.0).any(), \
        "observed test-year yield leaked into nbr_mean_yield_hist"


def test_nbr_yield_hist_without_source_leaks_test_target():
    """Documents the leak channel the fix closes: df as its own source
    reproduces the old behavior — the held-out year's observed target."""
    df_train, df_test, graph = _train_test_frames()
    out = sn.add_neighbor_features(df_test, graph, ["f1"], yield_col=TARGET)
    assert (out["nbr_mean_yield_hist"] == 999.0).all()


def test_nbr_same_year_feature_lookup_still_from_df():
    """The legitimate channel must survive: nbr_f1 for a 2015 test row is the
    neighbor's 2015 value (in-season EO is observable), not a train average."""
    df_train, df_test, graph = _train_test_frames()
    out = sn.add_neighbor_features(
        df_test, graph, ["f1"], yield_col=TARGET, df_source=df_train
    )
    assert (out["nbr_f1"] == 2015.0).all()


def test_train_side_call_unchanged():
    """df_source=None (train-side call) keeps df as its own source."""
    df_train, _, graph = _train_test_frames()
    out = sn.add_neighbor_features(df_train, graph, ["f1"], yield_col=TARGET)
    a = out.loc[out["Region"] == "A", "nbr_mean_yield_hist"].iloc[0]
    assert a == 3.0


def test_call_site_passes_train_as_source():
    """Guard the wiring: geocif.py's df_test call must pass df_source.

    The invariant is that the test frame's neighbour yield stats are sourced
    from the TRAIN frame, never from df_test itself (which holds the held-out
    year's observed yields). The source may legitimately be wrapped — it is
    currently ``_leakfree(self.df_train)``, which additionally strips rows
    promoted from the forecast year — so match on ``self.df_train`` appearing
    as the df_source argument rather than on one exact spelling.
    """
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("self.df_test = sn.add_neighbor_features")
    block = " ".join(src[i:i + 400].split())
    assert "df_source=" in block, "df_source must be passed explicitly"
    j = block.index("df_source=")
    arg = block[j:j + 60]
    assert "self.df_train" in arg, \
        f"test-side add_neighbor_features must source yield stats from df_train, got: {arg}"
    assert "self.df_test" not in arg, \
        f"df_source must never be the test frame, got: {arg}"


# ---------------------------------------------------------------------------
# compute_last_year_yield — was a verbatim copy of the target
# ---------------------------------------------------------------------------

def _ly_df(years=(2018, 2019, 2020, 2021)):
    return pd.DataFrame({
        "Region": ["A"] * len(years),
        "Harvest Year": list(years),
        TARGET: [float(i + 1) for i in range(len(years))],
    })


def test_last_year_yield_is_actually_lagged():
    out = fe.compute_last_year_yield(_ly_df())
    got = out.set_index("Harvest Year")[f"Last Year {TARGET}"]
    assert got.loc[2019] == 1.0
    assert got.loc[2020] == 2.0
    assert got.loc[2021] == 3.0


def test_last_year_yield_is_not_the_target():
    """The exact defect: column equalled target_col row-for-row."""
    out = fe.compute_last_year_yield(_ly_df())
    same = (out[f"Last Year {TARGET}"] == out[TARGET])
    assert not same.any(), "Last Year Yield must never equal the current year"


def test_last_year_yield_earliest_year_is_nan():
    out = fe.compute_last_year_yield(_ly_df())
    got = out.set_index("Harvest Year")[f"Last Year {TARGET}"]
    assert np.isnan(got.loc[2018])


def test_last_year_yield_tolerates_gaps():
    """A missing 2020 -> 2021 looks back to 2019, not NaN."""
    df = pd.DataFrame({
        "Region": ["A"] * 3,
        "Harvest Year": [2018, 2019, 2021],
        TARGET: [1.0, 2.0, 4.0],
    })
    out = fe.compute_last_year_yield(df)
    assert out.set_index("Harvest Year")[f"Last Year {TARGET}"].loc[2021] == 2.0


def test_last_year_yield_is_per_region():
    df = pd.concat([_ly_df(), _ly_df().assign(Region="B", **{TARGET: [10.0, 20.0, 30.0, 40.0]})])
    out = fe.compute_last_year_yield(df.reset_index(drop=True))
    b = out[out["Region"] == "B"].set_index("Harvest Year")[f"Last Year {TARGET}"]
    assert b.loc[2020] == 20.0, "regions must not bleed into each other"


# ---------------------------------------------------------------------------
# compute_lag_yield — held-out season reached later TRAINING rows (2026-09-29)
# ---------------------------------------------------------------------------
#
# Lags are built on the full table before the LOOCV split. Each row only
# looks backwards, but in the 2015 fold the 2016/2017/2018 TRAINING rows
# carried 2015's observed yield as t -1 / t -2 / t -3 (and Harvest Year +
# Region_ID are model features, so a model could line the rows up).

HELD = 2015
LAGS = [f"t -{k} {TARGET}" for k in (1, 2, 3)]


def _lag_df(years=range(2010, 2020)):
    """One region; yield encodes the year so every lag value is traceable."""
    return pd.DataFrame({
        "Region": "A",
        "Harvest Year": list(years),
        TARGET: [float(y - 100) for y in years],
    })


def _lags(df, forecast_season=HELD, seasons=range(2010, 2020)):
    out = fe.compute_lag_yield(df.copy(), list(seasons), forecast_season, 3, TARGET)
    return out.set_index("Harvest Year")[LAGS]


def test_lag_yield_hides_held_out_season_from_later_rows():
    got = _lags(_lag_df())
    assert np.isnan(got.loc[2016, LAGS[0]])
    assert np.isnan(got.loc[2017, LAGS[1]])
    assert np.isnan(got.loc[2018, LAGS[2]])


def test_lag_yield_held_out_value_appears_nowhere():
    got = _lags(_lag_df())
    assert not (got == HELD - 100.0).any().any(), "held-out yield leaked into a lag column"


def test_lag_yield_other_lags_untouched():
    """Only the lag that points AT the held-out season is blanked."""
    got = _lags(_lag_df())
    assert got.loc[2016, LAGS[1]] == 1914.0 and got.loc[2016, LAGS[2]] == 1913.0
    assert got.loc[2019, LAGS[0]] == 1918.0  # beyond the 3-year reach: unchanged


def test_lag_yield_held_out_row_keeps_its_own_history():
    """The forecast row's own lags are earlier years — always observable."""
    got = _lags(_lag_df())
    assert got.loc[HELD].tolist() == [1914.0, 1913.0, 1912.0]


def test_lag_yield_gap_fallback_excludes_held_out():
    """A year the region did not report (other regions did, so it is still in
    all_seasons_with_yield) falls back to the mean of the closest years — that
    mean must not include the held-out season either. 2017's closest years are
    2016 (absent for A), 2015 (held out), 2014 -> fallback = 2014's yield alone
    (before the fix: mean(1915, 1914) = 1914.5)."""
    df = _lag_df([y for y in range(2010, 2020) if y != 2016])
    got = _lags(df)
    assert got.loc[2017, LAGS[0]] == 1914.0, got.loc[2017].tolist()
    assert np.isnan(got.loc[2017, LAGS[1]])


def test_lag_yield_without_forecast_season_documents_the_channel():
    """forecast_season=None keeps every observed yield: the 2016 row's t -1
    is the 2015 yield — exactly what the held-out fold must not see."""
    got = _lags(_lag_df(), forecast_season=None)
    assert got.loc[2016, LAGS[0]] == 1915.0


def test_lag_yield_future_season_is_a_no_op():
    """Operational forecast: the forecast season has no observed yield, so
    hiding it changes nothing."""
    df = _lag_df(range(2010, 2021))
    df.loc[df["Harvest Year"] == 2020, TARGET] = np.nan
    seasons = range(2010, 2020)
    a = fe.compute_lag_yield(df.copy(), list(seasons), 2020, 3, TARGET)[LAGS]
    b = fe.compute_lag_yield(df.copy(), list(seasons), None, 3, TARGET)[LAGS]
    pd.testing.assert_frame_equal(a, b)


def test_lag_yield_call_site_passes_forecast_season():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("fe.compute_lag_yield(")
    assert "self.forecast_season" in src[i:i + 200]


# ---------------------------------------------------------------------------
# Last Year / Median Yield — same held-out channel as the lags (2026-09-29)
# ---------------------------------------------------------------------------

SCREAM = 9999.0  # held-out season's observed yield: any trace of it is a leak


def _screaming_df(years=range(2010, 2020)):
    df = _lag_df(years)
    df.loc[df["Harvest Year"] == HELD, TARGET] = SCREAM
    return df


def test_last_year_yield_hides_held_out_season():
    """2016 looks back past the held-out 2015, like an unreported year."""
    out = fe.compute_last_year_yield(_screaming_df(), TARGET, forecast_season=HELD)
    got = out.set_index("Harvest Year")[f"Last Year {TARGET}"]
    assert got.loc[2016] == 1914.0
    assert not (got == SCREAM).any()


def test_last_year_yield_held_out_row_keeps_its_own_history():
    out = fe.compute_last_year_yield(_screaming_df(), TARGET, forecast_season=HELD)
    assert out.set_index("Harvest Year")[f"Last Year {TARGET}"].loc[HELD] == 1914.0


def test_last_year_yield_without_forecast_season_documents_the_channel():
    out = fe.compute_last_year_yield(_screaming_df(), TARGET)
    assert out.set_index("Harvest Year")[f"Last Year {TARGET}"].loc[2016] == SCREAM


def test_median_yield_hides_held_out_season():
    out = fe.compute_median_statistics(
        _screaming_df(), list(range(2010, 2020)), 3, TARGET, forecast_season=HELD
    )
    got = out.set_index("Harvest Year")[f"Median {TARGET}"]
    # 2016's window is 2013-2015; 2015 is held out -> mean(2013, 2014)
    assert got.loc[2016] == np.mean([1913.0, 1914.0]), got.loc[2016]
    assert (got.dropna() < 3000).all(), "held-out yield averaged into a median"


def test_median_yield_held_out_row_keeps_its_own_window():
    out = fe.compute_median_statistics(
        _screaming_df(), list(range(2010, 2020)), 3, TARGET, forecast_season=HELD
    )
    got = out.set_index("Harvest Year")[f"Median {TARGET}"].loc[HELD]
    assert got == np.mean([1912.0, 1913.0, 1914.0])


def test_median_yield_without_forecast_season_documents_the_channel():
    out = fe.compute_median_statistics(
        _screaming_df(), list(range(2010, 2020)), 3, TARGET
    )
    assert out.set_index("Harvest Year")[f"Median {TARGET}"].loc[2016] > 3000


def test_history_call_sites_pass_forecast_season():
    """Both yield-history calls hide the held-out season; the area median
    (not the target) keeps every value."""
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("def _add_engineered_features")
    block = src[i:src.index("return df", i)]
    j = block.index("fe.compute_last_year_yield(")
    assert "forecast_season=self.forecast_season" in block[j:j + 150]
    k = block.index("fe.compute_median_statistics(")
    assert "forecast_season=self.forecast_season" in block[k:k + 200]
    a = block.index('"Area (ha)"')
    assert "forecast_season" not in block[a:a + 80]


def test_user_median_windows_excluded_from_neighbor_features():
    """Fixed-window reference medians must not become nbr_ candidates."""
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("def _add_spatial_neighbor_features")
    block = src[i:i + 3000]
    assert 'f"Median {self.target} (2018-2022)"' in block
    assert 'f"Median {self.target} (2013-2017)"' in block
