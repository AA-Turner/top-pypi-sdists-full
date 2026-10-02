"""FDW export (audit A7 at fdw_export.py 357/560/856 and the B row "FDW
forecast export collapses multi-season countries to one season per
region-year").
"""
import numpy as np
import pandas as pd
import pytest

from geocif.fdw_export import (
    _hvstat_calendar_row,
    _join_hvstat_calendar,
    _latest_stage_per,
)

PRED = "Predicted Yield (tn per ha)"


def _pred_frame():
    rows = [
        # Country, Region, Season, year, Stage Name, pred
        ("somalia", "Bay", 1, 2026, "May 1-Mar 31", 1.0),   # lexical max
        ("somalia", "Bay", 1, 2026, "Jul 1-Mar 31", 2.0),   # latest (Gu)
        ("somalia", "Bay", 2, 2026, "Nov 1-Sep 30", 3.0),
        ("somalia", "Bay", 2, 2026, "Dec 1-Sep 30", 4.0),   # latest (Deyr)
        ("somalia", "Bay", 1, 2025, "Jul 1-Mar 31", 5.0),
    ]
    return pd.DataFrame(rows, columns=["Country", "Region", "Season",
                                       "Harvest Year", "Stage Name", PRED])


def test_latest_stage_per_keeps_each_season_and_is_chronological():
    out = _latest_stage_per(_pred_frame(), ["Country", "Region", "Season", "Harvest Year"])
    got = {(s, y): v for s, y, v in out[["Season", "Harvest Year", PRED]].itertuples(index=False)}
    assert got == {(1, 2026): 2.0, (2, 2026): 4.0, (1, 2025): 5.0}
    # Single-season DB (all-NaN Season) still yields one row per region-year.
    single = _pred_frame()
    single["Season"] = np.nan
    single = single[single["Season"].isna()].drop_duplicates(
        subset=["Country", "Region", "Harvest Year", "Stage Name"])
    out1 = _latest_stage_per(single, ["Country", "Region", "Season", "Harvest Year"])
    assert len(out1) == 2


def _hvstat():
    return pd.DataFrame({
        "fnid": ["SO1", "SO1", "SO2"],
        "product": ["Maize"] * 3,
        "season_name": ["Gu", "Deyr", "Gu"],
        "planting_month": [4, 10, 4],
        "harvest_month": [8, 1, 8],
    })


def test_join_hvstat_calendar_per_season():
    merged = pd.DataFrame({
        "ADM_ID": ["SO1", "SO1", "SO2"], "Season": [1, 2, 1], PRED: [2.0, 4.0, 1.0],
    })
    out = _join_hvstat_calendar(merged, _hvstat())
    got = {(a, s): (p, n) for a, s, p, n in
           out[["ADM_ID", "Season", "planting_month", "season_name"]].itertuples(index=False)}
    assert got[("SO1", 1)] == (4, "Gu")
    assert got[("SO1", 2)] == (10, "Deyr")   # its OWN calendar, not Gu's
    assert got[("SO2", 1)] == (4, "Gu")


def test_join_hvstat_calendar_single_season_prefers_primary():
    merged = pd.DataFrame({"ADM_ID": ["SO1"], "Season": [np.nan], PRED: [2.0]})
    out = _join_hvstat_calendar(merged, _hvstat())
    assert len(out) == 1
    assert out["season_name"].iloc[0] == "Gu"
    assert out["planting_month"].iloc[0] == 4


def test_hvstat_calendar_row_resolves_season():
    assert _hvstat_calendar_row(_hvstat(), 2) == (10, 1, "Deyr")
    assert _hvstat_calendar_row(_hvstat(), 1) == (4, 8, "Gu")
    assert _hvstat_calendar_row(_hvstat(), None) == (4, 8, "Gu")
    assert _hvstat_calendar_row(_hvstat(), np.nan) == (4, 8, "Gu")
