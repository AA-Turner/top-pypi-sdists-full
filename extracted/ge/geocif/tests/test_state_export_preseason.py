"""``_write_state_export``: a pre-season row must never be exported as the
latest row of a (crop, state, year) (audit B, yield_outlook.py ~1689-1693).

Pre-season rows carry no parseable ``Stage Window Display`` so their
step was NaN; ``sort_values`` puts NaN LAST and ``.tail(1)`` then picked the
pre-season forecast over the in-season one.
"""
import numpy as np
import pandas as pd

from geocif.yield_outlook import _write_state_export

PRED = "Predicted Yield (tn per ha)"
OBS = "Observed Yield (tn per ha)"


def _frame():
    rows = [
        # Region, year, Stage Name,               SWD,              pred
        ("Iowa", 2024, "Pre-Season (init Feb)", "Pre-Season (init Feb)", 1.0),
        ("Iowa", 2024, "Apr 1-Mar 31",          "Mar 1-Apr 30",          2.0),
        ("Iowa", 2024, "Jul 1-Mar 31",          "Mar 1-Jul 31",          3.0),
        ("Iowa", 2023, "Jul 1-Mar 31",          "Mar 1-Jul 31",          4.0),
        ("Iowa", 2023, "Pre-Season (init Feb)", "Pre-Season (init Feb)", 5.0),
    ]
    df = pd.DataFrame(rows, columns=["Region", "Harvest Year", "Stage Name",
                                     "Stage Window Display", PRED])
    df["Country"] = "united_states_of_america"
    df[OBS] = np.nan
    df["lower CI"] = df[PRED] - 0.5
    df["upper CI"] = df[PRED] + 0.5
    df["alpha"] = 0.2
    return df


def test_pre_season_row_never_wins(tmp_path):
    store = {("united_states_of_america", "maize", "tabpfn"): _frame()}
    written = _write_state_export(store, None, tmp_path, parser=None)
    assert len(written) == 1
    out = pd.read_csv(written[0])
    assert len(out) == 2
    got = dict(zip(out["year"], out["predicted_yield"]))
    assert got == {2024: 3.0, 2023: 4.0}
    assert out["state_fips"].astype(str).str.zfill(2).tolist() == ["19", "19"]
