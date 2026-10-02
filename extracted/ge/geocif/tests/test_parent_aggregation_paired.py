"""viz/aggregation.aggregate_predictions (audit B row): parent aggregation
scored national observed and predicted over DIFFERENT child sets, and one
NaN area flipped the whole parent-year to an unweighted mean.
"""
import logging

import numpy as np
import pandas as pd
import pytest

from geocif.viz.aggregation import OBS_COL, PRED_COL, aggregate_predictions

LEVEL_MAP = {"iowa adair": "Iowa", "iowa boone": "Iowa", "iowa clay": "Iowa"}


def _frame():
    rows = [
        # Region,      year, obs,    pred, area
        ("Iowa Adair", 2019, 10.0,   11.0, 100.0),
        ("Iowa Boone", 2019, np.nan, 20.0, 300.0),   # no observation
        ("Iowa Clay",  2019, 8.0,     7.0, 100.0),
        ("Iowa Adair", 2026, np.nan,  9.0, 100.0),   # forecast year: no obs anywhere
        ("Iowa Boone", 2026, np.nan, 12.0, 300.0),
        ("Iowa Clay",  2026, np.nan,  6.0, 100.0),
    ]
    df = pd.DataFrame(rows, columns=["Region", "Harvest Year", OBS_COL, PRED_COL, "Area (ha)"])
    df["Country"] = "united_states_of_america"
    return df


def _row(out, year):
    sub = out[(out["Region"] == "Iowa") & (out["Harvest Year"] == year)]
    assert len(sub) == 1
    return sub.iloc[0]


def test_hindcast_year_scores_obs_and_pred_on_the_same_children():
    out = aggregate_predictions(_frame(), LEVEL_MAP)
    r = _row(out, 2019)
    # Boone has no observation -> it is in NEITHER aggregate.
    assert r[OBS_COL] == pytest.approx((10 * 100 + 8 * 100) / 200)    # 9.0
    assert r[PRED_COL] == pytest.approx((11 * 100 + 7 * 100) / 200)   # 9.0, not 15.6
    assert r["N Units"] == 2
    assert r["Area (ha)"] == pytest.approx(200.0)
    assert r["Aggregation"] == "area-weighted"


def test_forecast_year_aggregates_every_predicted_child():
    r = _row(aggregate_predictions(_frame(), LEVEL_MAP), 2026)
    assert np.isnan(r[OBS_COL])
    assert r[PRED_COL] == pytest.approx((9 * 100 + 12 * 300 + 6 * 100) / 500)
    assert r["N Units"] == 3


def test_one_missing_weight_does_not_flip_the_group(caplog):
    df = _frame()
    df.loc[(df["Region"] == "Iowa Clay") & (df["Harvest Year"] == 2019), "Area (ha)"] = np.nan
    with caplog.at_level(logging.WARNING, logger="geocif.viz.aggregation"):
        out = aggregate_predictions(df, LEVEL_MAP)
    r = _row(out, 2019)
    # Clay (no weight) is left out of the WEIGHTED aggregate; Adair carries it.
    assert r["Aggregation"] == "area-weighted"
    assert r[OBS_COL] == pytest.approx(10.0)
    assert r[PRED_COL] == pytest.approx(11.0)
    assert r["N Units"] == 1
    assert r["N No Weight"] == 1
    assert not [rec for rec in caplog.records if "unweighted means" in rec.message]


def test_unweighted_only_when_no_usable_weight(caplog):
    df = _frame().drop(columns=["Area (ha)"])
    with caplog.at_level(logging.WARNING, logger="geocif.viz.aggregation"):
        out = aggregate_predictions(df, LEVEL_MAP)
    r = _row(out, 2019)
    assert r["Aggregation"] == "unweighted"
    assert r[OBS_COL] == pytest.approx(9.0)
    assert r[PRED_COL] == pytest.approx(9.0)
    assert np.isnan(r["Area (ha)"])
    assert len([rec for rec in caplog.records if "unweighted means" in rec.message]) == 1
