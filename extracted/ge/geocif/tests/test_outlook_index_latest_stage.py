"""``_compute_outlook_index``: chronological latest stage (audit A7, the
``yield_outlook.py:371`` site) and the per-region minimum-history guard
(audit B: "no per-region minimum history for the outlook index").
"""
import logging

import numpy as np
import pandas as pd
import pytest

from geocif.yield_outlook import _compute_outlook_index

PRED = "Predicted Yield (tn per ha)"
OBS = "Observed Yield (tn per ha)"


def _df():
    rows = []
    # Region "a": four history years + the forecast year, three stages each.
    # "May 1-Mar 31" is the LEXICAL max, "Jul 1-Mar 31" the latest.
    for year in (2020, 2021, 2022, 2023, 2024):
        for stage, pred in (("Apr 1-Mar 31", 1.0), ("May 1-Mar 31", 100.0),
                            ("Jul 1-Mar 31", 2.0 if year < 2024 else 3.0)):
            rows.append(("usa", "a", year, stage, pred))
    # Region "b": a single history year only.
    for stage, pred in (("Apr 1-Mar 31", 1.0), ("Jul 1-Mar 31", 2.0)):
        rows.append(("usa", "b", 2023, stage, pred))
        rows.append(("usa", "b", 2024, stage, pred + 1))
    df = pd.DataFrame(rows, columns=["Country", "Region", "Harvest Year", "Stage Name", PRED])
    df[OBS] = np.nan
    return df


def test_latest_stage_is_chronological_not_lexical():
    out = _compute_outlook_index(_df(), 2024, 10, "mean", min_hist_years=1)
    a = out[out["Region"] == "a"].iloc[0]
    assert a["current_predicted"] == pytest.approx(3.0)   # Jul, not May (100)
    assert a["hist_predicted"] == pytest.approx(2.0)
    assert a["outlook_index"] == pytest.approx(50.0)


def test_min_history_guard_drops_short_regions_and_logs(caplog):
    with caplog.at_level(logging.WARNING, logger="geocif.yield_outlook"):
        out = _compute_outlook_index(_df(), 2024, 10, "mean")   # default = 3
    assert set(out["Region"]) == {"a"}
    assert any("fewer than 3 historical" in r.message for r in caplog.records)
    # Lowering the guard keeps the one-year region (index from one year).
    out1 = _compute_outlook_index(_df(), 2024, 10, "mean", min_hist_years=1)
    assert set(out1["Region"]) == {"a", "b"}
    b = out1[out1["Region"] == "b"].iloc[0]
    assert b["current_predicted"] == pytest.approx(3.0)
    assert b["hist_predicted"] == pytest.approx(2.0)
