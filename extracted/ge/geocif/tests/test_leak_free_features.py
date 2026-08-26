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
    """Guard the wiring: geocif.py's df_test call must pass df_source."""
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("self.df_test = sn.add_neighbor_features")
    block = src[i:i + 400]
    assert "df_source=self.df_train" in block, \
        "test-side add_neighbor_features must source yield stats from df_train"


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


def test_user_median_windows_excluded_from_neighbor_features():
    """Fixed-window reference medians must not become nbr_ candidates."""
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    i = src.index("def _add_spatial_neighbor_features")
    block = src[i:i + 3000]
    assert 'f"Median {self.target} (2018-2022)"' in block
    assert 'f"Median {self.target} (2013-2017)"' in block
