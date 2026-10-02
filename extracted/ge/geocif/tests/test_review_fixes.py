"""Fixes from the 2026-10-01 review of the audit batch (stage ranking,
per-season aggregation, FDW calendar join)."""
import numpy as np
import pandas as pd
import pytest

from geocif.ml import stage_labels as sl


def test_sub_monthly_windows_do_not_tie():
    # Stage Window Display path (dekad_r windows ending in the same month)
    swd = ["Mar 1-Apr 9", "Mar 1-Apr 19", "Mar 1-Apr 29"]
    ranks = [sl.stage_rank("x", swd=s) for s in swd]
    assert ranks == sorted(ranks)
    assert len(set(ranks)) == 3
    # Stage Name path, reverse (_r) labels: the as-of day breaks the tie
    names = ["Apr 10-Mar 1", "Apr 20-Mar 1", "Apr 30-Mar 1"]
    ranks = [sl.stage_rank(n) for n in names]
    assert ranks == sorted(ranks)
    assert len(set(ranks)) == 3
    df = pd.DataFrame({"Region": "R", "Stage Name": names, "v": [1, 2, 3]})
    assert sl.latest_stage_rows(df, by=["Region"])["v"].tolist() == [3]
    # monthly labels are unchanged by the day term
    assert sl.stage_rank("Jun 1-Mar 31") > sl.stage_rank("May 1-Mar 31")


def test_in_season_inits_after_planting_rank_above_pre_season():
    names = [
        "Pre-Season (init Sep)", "Pre-Season (init Oct)",
        "In-Season (init Nov)", "In-Season (init Dec)", "In-Season (init Jan)",
    ]
    assert sl.infer_planting_month(names) == 11
    assert sl.sort_stage_names(list(reversed(names))) == names
    df = pd.DataFrame({"Region": "R", "Stage Name": names, "v": range(5)})
    assert sl.latest_stage_rows(df, by=["Region"])["v"].tolist() == [4]


def test_parent_aggregation_keeps_seasons_apart():
    from geocif.viz import aggregation as agg

    df = pd.DataFrame({
        "Region": ["bay", "bay"], "Harvest Year": [2024, 2024], "Season": [1, 2],
        agg.OBS_COL: [1.0, 0.4], agg.PRED_COL: [1.1, 0.5], "Area (ha)": [10.0, 10.0],
    })
    out = agg.aggregate_predictions(df, {"bay": "somalia"})
    assert len(out) == 2
    assert sorted(out["Season"].tolist()) == [1, 2]
    by_season = out.set_index("Season")
    assert by_season.loc[1, agg.OBS_COL] == pytest.approx(1.0)
    assert by_season.loc[2, agg.PRED_COL] == pytest.approx(0.5)
    assert by_season["N Units"].tolist() == [1, 1]


def test_fdw_calendar_join_uses_the_countrys_own_season_names():
    from geocif import fdw_export as fx

    hv = pd.DataFrame({
        "country": ["Kenya", "Kenya", "Somalia", "Somalia"],
        "fnid": ["KE1", "KE1", "SO1", "SO1"],
        "season_name": ["Long", "Short", "Gu", "Deyr"],
        "planting_month": [3, 10, 4, 10],
        "harvest_month": [8, 1, 8, 1],
    })
    df = pd.DataFrame({
        "Country": ["Somalia", "Somalia"], "ADM_ID": ["SO1", "SO1"], "Season": [1, 2],
    })
    out = fx._join_hvstat_calendar(df, hv)
    assert out["season_name"].tolist() == ["Gu", "Deyr"]
    assert out["planting_month"].tolist() == [4, 10]
