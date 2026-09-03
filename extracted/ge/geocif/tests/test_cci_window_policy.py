"""Tests for the CCI window policy (geocif/ml/stages.py).

Background: at usa_admin2 county scale, offering every CCI stage window
(28 windows x 3 stats by October) both overfits and lets sparse April/May
windows — ~10% coverage, zero-filled downstream — act as region-identity
proxies. Measured on 2010-2019 LOYO ridge (within-year anomalies), the single
cutoff-month CCI beat the full window set at every cutoff from July onward.

``cci_windows = current`` keeps only the cutoff-month single-month CCI window
per fold. Default is "all" (historical behaviour, exact no-op).
"""

import numpy as np
import pytest

from geocif.ml.stages import cutoff_month_of, keep_cci_window


# --------------------------------------------------------------- cutoff month

def test_cutoff_is_first_element_of_longest_array():
    stages = [np.array([9, 8, 7, 6, 5, 4]), np.array([9]), np.array([5]),
              np.array([9, 8]), np.array([6, 5])]
    assert cutoff_month_of(stages) == 9


def test_cutoff_handles_wrapped_seasons():
    # poppy-style Nov..Aug season, cutoff August: element-wise max would say 12.
    stages = [np.array([8, 7, 6, 5, 4, 3, 2, 1, 12, 11]), np.array([8]),
              np.array([12]), np.array([8, 7])]
    assert cutoff_month_of(stages) == 8


def test_cutoff_of_empty_is_none():
    assert cutoff_month_of([]) is None


# ------------------------------------------------------------------ policy

def test_all_policy_is_a_noop_for_everything():
    assert keep_cci_window("MAX_CCI", np.array([5]), 9, "all")
    assert keep_cci_window("MAX_CCI", np.array([9, 8, 7]), 9, "all")
    assert keep_cci_window("PRCPTOT", np.array([5]), 9, "all")


def test_current_keeps_only_cutoff_month_single_window():
    cutoff = 9
    assert keep_cci_window("MAX_CCI", np.array([9]), cutoff, "current")
    # other single months are dropped — the May proxy in particular
    assert not keep_cci_window("MAX_CCI", np.array([5]), cutoff, "current")
    # cumulative spans are dropped even when they end at the cutoff
    assert not keep_cci_window("MAX_CCI", np.array([9, 8]), cutoff, "current")
    assert not keep_cci_window("MIN_CCI", np.array([9, 8, 7, 6, 5, 4]), cutoff, "current")


@pytest.mark.parametrize("stat", ["MAX_CCI", "MIN_CCI", "MEAN_CCI", "STD_CCI", "AUC_CCI"])
def test_current_applies_to_every_cci_statistic(stat):
    assert keep_cci_window(stat, np.array([7]), 7, "current")
    assert not keep_cci_window(stat, np.array([5]), 7, "current")


def test_non_cci_cids_always_pass():
    for cid in ("PRCPTOT", "CDD", "MAX_NDVI", "STD_ESI4WK", "KDD", "H-INDEX_Precip"):
        assert keep_cci_window(cid, np.array([5]), 9, "current"), cid
        assert keep_cci_window(cid, np.array([9, 8, 7]), 9, "current"), cid


def test_unknown_cutoff_fails_open():
    """If the cutoff cannot be resolved, do not silently drop features."""
    assert keep_cci_window("MAX_CCI", np.array([5]), None, "current")


def test_wrapped_season_current_window():
    # poppy at the August cutoff: keep Aug, drop Nov/Dec singles and spans
    assert keep_cci_window("MAX_CCI", np.array([8]), 8, "current")
    assert not keep_cci_window("MAX_CCI", np.array([11]), 8, "current")
    assert not keep_cci_window("MAX_CCI", np.array([12, 11]), 8, "current")


def test_malformed_stage_fails_open():
    assert keep_cci_window("MAX_CCI", np.array([]), 9, "current") in (True, False)
    # non-numeric stage content must not raise
    assert keep_cci_window("MAX_CCI", ["x"], 9, "current")


# ---------------------------------------------- name-based final-list filter

from geocif.ml.stages import filter_feature_names_cci


NAMES = [
    "MAX_CCI Sep 1-Sep 30",        # cutoff single  (keep at cm=9)
    "MAX_CCI May 1-May 31",        # other single   (drop)
    "MIN_CCI Sep 1-Apr 30",        # cumulative     (drop)
    "MEAN_CCI Jun 1-May 31",       # cumulative     (drop)
    "PRCPTOT May 1-May 31",        # non-CCI        (keep)
    "STD_ESI4WK Sep 1-Apr 30",     # non-CCI        (keep)
    "t -1 Yield (tn per ha)",      # engineered     (keep)
    "Yield Trend",                 # engineered     (keep)
    "lat",                         # coordinate     (keep)
]


def test_final_list_filter_keeps_only_cutoff_single_cci():
    out = filter_feature_names_cci(NAMES, 9)
    assert "MAX_CCI Sep 1-Sep 30" in out
    assert "MAX_CCI May 1-May 31" not in out
    assert "MIN_CCI Sep 1-Apr 30" not in out
    assert "MEAN_CCI Jun 1-May 31" not in out
    # every non-CCI name survives untouched, order preserved
    for keep in ("PRCPTOT May 1-May 31", "STD_ESI4WK Sep 1-Apr 30",
                 "t -1 Yield (tn per ha)", "Yield Trend", "lat"):
        assert keep in out
    assert out == [f for f in NAMES if f in out]


def test_final_list_filter_none_cutoff_is_noop():
    assert filter_feature_names_cci(NAMES, None) == NAMES


def test_final_list_filter_fails_open_on_weird_cci_name():
    # a CCI feature with no parseable window must be kept, not dropped
    out = filter_feature_names_cci(["MAX_CCI", "MAX_CCI_zreg"], 9)
    assert out == ["MAX_CCI", "MAX_CCI_zreg"]


def test_final_list_filter_handles_december_wrap():
    names = ["MAX_CCI Dec 1-Dec 31", "MAX_CCI Dec 1-Nov 30", "MAX_CCI Aug 1-Aug 31"]
    out = filter_feature_names_cci(names, 12)
    assert out == ["MAX_CCI Dec 1-Dec 31"]


def test_final_list_filter_empty_list():
    assert filter_feature_names_cci([], 9) == []


# ------------------------------------------------------- delta column pairing

from geocif.ml.stages import cci_delta_columns


COLS = [
    "MEAN_CCI Aug 1-Aug 31", "MEAN_CCI Jul 1-Jul 31",
    "MAX_CCI Aug 1-Aug 31", "MAX_CCI Jul 1-Jul 31",
    "MIN_CCI Aug 1-Aug 31",                     # no Jul partner -> no delta
    "MEAN_CCI Aug 1-Apr 30",                    # cumulative -> ignored
    "PRCPTOT Aug 1-Aug 31", "PRCPTOT Jul 1-Jul 31",  # non-CCI -> ignored
    "Region", "Harvest Year",
]


def test_delta_pairs_cutoff_with_previous_month():
    pairs = cci_delta_columns(COLS, 8)
    d = {n: (c, p) for n, c, p in pairs}
    assert d == {
        "DELTA_MAX_CCI Aug": ("MAX_CCI Aug 1-Aug 31", "MAX_CCI Jul 1-Jul 31"),
        "DELTA_MEAN_CCI Aug": ("MEAN_CCI Aug 1-Aug 31", "MEAN_CCI Jul 1-Jul 31"),
    }


def test_delta_requires_both_months():
    # MIN has Aug but no Jul -> excluded
    assert not any("MIN" in n for n, _, _ in cci_delta_columns(COLS, 8))


def test_delta_ignores_non_cci_and_cumulative():
    names = [n for n, _, _ in cci_delta_columns(COLS, 8)]
    assert all("CCI" in n for n in names)


def test_delta_december_january_wrap():
    cols = ["MEAN_CCI Jan 1-Jan 31", "MEAN_CCI Dec 1-Dec 31"]
    pairs = cci_delta_columns(cols, 1)
    assert pairs == [("DELTA_MEAN_CCI Jan",
                      "MEAN_CCI Jan 1-Jan 31", "MEAN_CCI Dec 1-Dec 31")]


def test_delta_none_cutoff_empty():
    assert cci_delta_columns(COLS, None) == []


def test_filter_keeps_delta_names():
    """DELTA_* names carry 'CCI' but no window suffix -> must fail open."""
    out = filter_feature_names_cci(
        ["DELTA_MEAN_CCI Aug", "MAX_CCI May 1-May 31", "MAX_CCI Aug 1-Aug 31"], 8)
    assert out == ["DELTA_MEAN_CCI Aug", "MAX_CCI Aug 1-Aug 31"]


# ------------------------------------------------------------ G+E policy

GE_NAMES = [
    "MEAN_CCIGE Sep 1-Sep 30", "MEAN_CCI Sep 1-Sep 30",
    "MAX_CCIGE May 1-May 31", "MAX_CCIGE Sep 1-Apr 30",
    "PRCPTOT Sep 1-Sep 30", "Yield Trend",
]


def test_current_ge_swaps_weighted_for_ge():
    out = filter_feature_names_cci(GE_NAMES, 9, "current_ge")
    assert out == ["MEAN_CCIGE Sep 1-Sep 30", "PRCPTOT Sep 1-Sep 30", "Yield Trend"]


def test_current_excludes_ge_for_reproducibility():
    """Runs made before CCIGE existed must stay bit-reproducible: policy
    'current' may never pick up the new GE columns."""
    out = filter_feature_names_cci(GE_NAMES, 9, "current")
    assert out == ["MEAN_CCI Sep 1-Sep 30", "PRCPTOT Sep 1-Sep 30", "Yield Trend"]


def test_current_ge_still_enforces_cutoff_window():
    out = filter_feature_names_cci(GE_NAMES, 5, "current_ge")
    assert out == ["MAX_CCIGE May 1-May 31", "PRCPTOT Sep 1-Sep 30", "Yield Trend"]
