"""Tests for forecast-year region promotion (geocif/ml/region_selection.py).

The feature deliberately puts a slice of the forecast year into training to ask
"what is early-reporting data worth?". Two properties keep that honest and are
what these tests defend:

  * a promoted region is REMOVED from the scored set (it is in training, so
    scoring it would be self-congratulatory);
  * promoted rows are tagged so every downstream statistic can exclude them —
    the per-region detrend in particular, where including one would let the
    retrend step reconstruct the very value being predicted.

The `none` arm must also be a bit-for-bit no-op, otherwise every historical
comparison shifts under us.
"""

import numpy as np
import pandas as pd
import pytest

from geocif.ml.neighbor_leakage import LEAK_COLUMN
from geocif.ml.region_selection import (
    apply_region_promotion,
    n_to_promote,
    select_regions,
)

TARGET = "Yield (tn per ha)"
YEAR = 2024


def _panel(n_regions=20, years=range(2015, 2025), missing_forecast=()):
    """Rectangular region x year panel with a known yield everywhere."""
    rows = []
    rng = np.random.default_rng(0)
    for i in range(n_regions):
        r = f"region_{i:02d}"
        for y in years:
            val = 2.0 + 0.05 * (y - 2015) + rng.normal(0, 0.1)
            if y == YEAR and r in missing_forecast:
                val = np.nan
            rows.append({"Region": r, "Harvest Year": y, TARGET: val})
    return pd.DataFrame(rows)


def _split(df):
    m = df["Harvest Year"] == YEAR
    return df[~m].copy(), df[m].copy()


# ---------------------------------------------------------------- cardinality

@pytest.mark.parametrize("n,frac,exp", [
    (100, 0.05, 5), (20, 0.05, 1), (10, 0.05, 1),   # never silently rounds to 0
    (100, 0.0, 0), (1, 0.5, 0),                      # nothing to hold out
    (100, 1.0, 99),                                  # always keep >=1 scored
])
def test_n_to_promote(n, frac, exp):
    assert n_to_promote(n, frac) == exp


def test_random_selection_is_reproducible_and_sized():
    cands = [f"r{i}" for i in range(40)]
    a = select_regions(cands, 0.05, mode="random", seed=7)
    b = select_regions(cands, 0.05, mode="random", seed=7)
    c = select_regions(cands, 0.05, mode="random", seed=8)
    assert a == b and len(a) == 2
    assert a != c, "different seeds must give different subsets"
    assert set(a) <= set(cands)


def test_explicit_mode_ignores_unknown_regions():
    got = select_regions(["a", "b", "c"], 0.5, mode="explicit",
                         explicit=["b", "zzz"])
    assert got == ["b"]


def test_invalid_mode_raises():
    with pytest.raises(ValueError):
        select_regions(["a"], 0.1, mode="bogus")


# ------------------------------------------------------------------- promotion

def test_none_mode_is_a_bitwise_noop():
    df = _panel()
    tr, te = _split(df)
    tr2, te2, promoted = apply_region_promotion(
        tr, te, df, YEAR, TARGET, fraction=0.05, mode="none")
    assert promoted == []
    pd.testing.assert_frame_equal(tr, tr2)
    pd.testing.assert_frame_equal(te, te2)
    assert LEAK_COLUMN not in tr2.columns


def test_promoted_regions_leave_the_test_set():
    df = _panel(n_regions=20)
    tr, te = _split(df)
    tr2, te2, promoted = apply_region_promotion(
        tr, te, df, YEAR, TARGET, fraction=0.25, mode="random", seed=3)
    assert len(promoted) == 5
    scored = set(te2["Region"])
    assert scored.isdisjoint(promoted), "a promoted region must never be scored"
    assert len(te2) == len(te) - len(promoted)


def test_promoted_rows_are_tagged_and_added_to_train():
    df = _panel(n_regions=20)
    tr, te = _split(df)
    tr2, _, promoted = apply_region_promotion(
        tr, te, df, YEAR, TARGET, fraction=0.25, mode="random", seed=3)
    added = tr2[tr2[LEAK_COLUMN].notna()]
    assert len(added) == len(promoted)
    assert set(added["Region"]) == set(promoted)
    assert (added["Harvest Year"] == YEAR).all()
    # everything else stays untagged, so a leak-free view recovers the original
    assert len(tr2[tr2[LEAK_COLUMN].isna()]) == len(tr)


def test_leakfree_view_excludes_exactly_the_promoted_rows():
    """Mirrors geocif._df_train_leakfree — the guard every hazard site uses."""
    df = _panel(n_regions=20)
    tr, te = _split(df)
    tr2, _, promoted = apply_region_promotion(
        tr, te, df, YEAR, TARGET, fraction=0.25, mode="random", seed=1)
    leakfree = tr2[tr2[LEAK_COLUMN].isna()]
    assert YEAR not in set(leakfree["Harvest Year"]), \
        "no forecast-year row may survive the leak-free view"
    pd.testing.assert_frame_equal(
        leakfree.drop(columns=[LEAK_COLUMN]).reset_index(drop=True),
        tr.reset_index(drop=True),
    )


def test_realtime_forecast_year_is_a_noop():
    """No known yields at the forecast year -> nothing to promote."""
    regions = [f"region_{i:02d}" for i in range(20)]
    df = _panel(n_regions=20, missing_forecast=set(regions))
    tr, te = _split(df)
    tr2, te2, promoted = apply_region_promotion(
        tr, te, df, YEAR, TARGET, fraction=0.25, mode="random", seed=0)
    assert promoted == []
    pd.testing.assert_frame_equal(te, te2)


def test_only_regions_with_known_yield_are_promotable():
    unknown = {"region_00", "region_01", "region_02"}
    df = _panel(n_regions=20, missing_forecast=unknown)
    tr, te = _split(df)
    _, _, promoted = apply_region_promotion(
        tr, te, df, YEAR, TARGET, fraction=0.9, mode="random", seed=0)
    assert set(promoted).isdisjoint(unknown)


def test_explicit_mode_feeds_a_ga_candidate():
    df = _panel(n_regions=20)
    tr, te = _split(df)
    want = ["region_03", "region_11"]
    tr2, te2, promoted = apply_region_promotion(
        tr, te, df, YEAR, TARGET, fraction=0.05, mode="explicit", explicit=want)
    assert promoted == sorted(want)
    assert set(te2["Region"]).isdisjoint(want)
    assert set(tr2[tr2[LEAK_COLUMN].notna()]["Region"]) == set(want)


def test_both_frames_keep_aligned_schemas():
    """Regression: LEAK_COLUMN must land on df_test too.

    `_get_common_columns` derives the per-region column whitelist from df_train
    and `_extract_region_subset` applies it to BOTH frames, so a column present
    only on df_train raised KeyError("['__leaked_from_year__'] not in index")
    on every fold of the first live run.
    """
    df = _panel(n_regions=20)
    tr, te = _split(df)
    tr2, te2, promoted = apply_region_promotion(
        tr, te, df, YEAR, TARGET, fraction=0.25, mode="random", seed=5)
    assert promoted
    assert LEAK_COLUMN in tr2.columns and LEAK_COLUMN in te2.columns
    # test rows were never promoted, so the tag must be entirely null there
    assert te2[LEAK_COLUMN].isna().all()
    # the whitelist derived from train must be selectable on test
    common = [c for c in tr2.columns if c in te2.columns]
    te2[common]  # must not raise
    assert LEAK_COLUMN in common


def test_promoted_rows_must_remain_usable_as_training_rows():
    """Regression: promoted rows need a target value, or X/y desync.

    An earlier version leak-filtered the per-region detrend loop. Promoted rows
    then got no ``Detrended <target>``, so _setup_training_data dropped them
    from y but not X and every fold died with "Found input variables with
    inconsistent numbers of samples". Detrending is per-region and promoted
    regions are never scored, so there is no leakage path to justify it.
    """
    df = _panel(n_regions=20)
    tr, te = _split(df)
    tr2, _, promoted = apply_region_promotion(
        tr, te, df, YEAR, TARGET, fraction=0.25, mode="random", seed=2)
    promoted_rows = tr2[tr2["Region"].isin(promoted) & (tr2["Harvest Year"] == YEAR)]
    assert len(promoted_rows) == len(promoted)
    # the target must be present on every promoted row — that is what makes it
    # a usable training example rather than a row that silently vanishes from y
    assert promoted_rows[TARGET].notna().all()
