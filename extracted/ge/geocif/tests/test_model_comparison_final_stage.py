"""Audit A9 (blend pseudo-models scored at the final stage while real models
were pooled across all stages in the same scorecard) and the B row "the
fair-year intersection is bypassed when empty".
"""
import inspect

import numpy as np
import pandas as pd

from geocif import yield_outlook as yo

OBS = "Observed Yield (tn per ha)"
PRED = "Predicted Yield (tn per ha)"


def _model_df(years, stages):
    rows = [("a", y, s, 1.0, 1.1) for y in years for s in stages]
    return pd.DataFrame(rows, columns=["Region", "Harvest Year", "Stage Name", OBS, PRED])


def test_common_years_distinguishes_empty_from_unknown():
    a = _model_df([2019, 2020], ["Jul 1-Mar 31"])
    b = _model_df([2021, 2022], ["Jul 1-Mar 31"])
    assert yo._common_years({"a": a, "b": b}, OBS, PRED) == set()       # disjoint: EMPTY
    assert yo._common_years({"a": a, "c": a.copy()}, OBS, PRED) == {2019, 2020}
    empty = a.iloc[0:0]
    assert yo._common_years({"a": empty}, OBS, PRED) is None            # nobody scorable
    # A model with no scorable rows does not shrink the intersection.
    assert yo._common_years({"a": a, "e": empty}, OBS, PRED) == {2019, 2020}
    assert yo._model_year_ranges({"a": a, "e": empty}, OBS, PRED) == {
        "a": "2019-2020 (2)", "e": "none"}


def test_model_comparison_scores_latest_stage_and_honours_empty_intersection():
    src = inspect.getsource(yo._generate_model_comparison)
    # Every model is reduced to the chronologically latest stage per
    # region-year before any metric is computed (A9).
    assert "_latest_stage_rows(d, by=[\"Region\", \"Season\", \"Harvest Year\"])" in src
    # The empty intersection is handled explicitly instead of `if common_years:`
    # falling through to per-model years.
    assert "common_years is not None and not common_years" in src
    assert "_common_years(model_dfs, obs_col, pred_col)" in src


def test_blend_rows_get_the_latest_stage_label():
    """The blend's Stage Name is copied from the source model's LATEST stage
    per region-year, not from the first-inserted row."""
    src = inspect.getsource(yo.run)
    assert "_latest_stage_rows(\n                    src_df, by=join_cols, keep=\"last\"\n                )" in src


def test_latest_stage_reduction_matches_a_single_stage_blend():
    """What A9 buys: a real model with 3 stages and a blend holding only the
    final stage end up on identical (region, year, stage) samples."""
    real = pd.DataFrame({
        "Region": ["a"] * 3, "Harvest Year": [2020] * 3,
        "Stage Name": ["Apr 1-Mar 31", "May 1-Mar 31", "Jul 1-Mar 31"],
        OBS: [2.0] * 3, PRED: [1.0, 9.0, 2.5],
    })
    blend = real.iloc[[2]].copy()
    reduced = yo._latest_stage_rows(real, by=["Region", "Season", "Harvest Year"])
    assert reduced[["Region", "Harvest Year", "Stage Name", PRED]].values.tolist() == \
        blend[["Region", "Harvest Year", "Stage Name", PRED]].values.tolist()
