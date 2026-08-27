"""last<N>m_<algo> models: restrict features to the TRAILING N months.

The cumulative CID stage set already contains every contiguous window, so this
is a selection problem, not a data problem. What makes it easy to get wrong is
the reverse naming: `monthly_r` writes spans harvest-first, so the trailing
window DESCENDS from the season's latest period. `8_7` is the last two months
(Aug+Jul); `5_4` is a two-month span earlier in the season and must be dropped.
"""
import re
from pathlib import Path

import pandas as pd
import pytest

from geocif.ml import stages

ROOT = Path(__file__).resolve().parents[1] / "geocif"
SRC = (ROOT / "geocif.py").read_text(encoding="utf-8")


def _frame(cols):
    return pd.DataFrame({c: [1.0, 2.0] for c in cols})


# ---------------------------------------------------------------------------
# selector
# ---------------------------------------------------------------------------

def test_keeps_only_the_trailing_two_month_span():
    df = _frame(["PRCPTOT_8_7", "PRCPTOT_8", "PRCPTOT_8_7_6", "PRCPTOT_5_4"])
    got = list(stages.select_last_n_months_features(df, 2).columns)
    assert got == ["PRCPTOT_8_7"]


def test_earlier_two_month_span_is_dropped():
    """The specific reverse-naming trap: 5_4 is 2 months but not the last 2.

    Months must be contiguous here (4-9), as real cumulative CID data is: a
    genuine gap is treated as a season boundary, which is tested separately.
    """
    df = _frame(["MAX_NDVI_9_8", "MAX_NDVI_8_7", "MAX_NDVI_7_6",
                 "MAX_NDVI_6_5", "MAX_NDVI_5_4"])
    got = list(stages.select_last_n_months_features(df, 2).columns)
    assert got == ["MAX_NDVI_9_8"]


def test_non_stage_columns_survive():
    """Real non-stage names carry no _<digit> suffix (verified against an
    actual X_train: `t -1 Yield (tn per ha)`, Region, lat/lon)."""
    keep = ["Region", "lat", "lon", "t -1 Yield (tn per ha)",
            "AEF_5", "MEAN_FLDAS_x"]
    # contiguous months only — window selection is covered by its own tests
    df = _frame(["PRCPTOT_8_7", "PRCPTOT_7_6"] + keep)
    got = set(stages.select_last_n_months_features(df, 2).columns)
    assert got == set(keep) | {"PRCPTOT_8_7"}, got


def test_month_gap_is_treated_as_a_season_boundary():
    """A real gap means two seasons, so each keeps its own trailing window.
    This is what makes the Kenya Mar-Jul / Apr-Dec split work."""
    df = _frame(["MAX_NDVI_9_8", "MAX_NDVI_5_4"])   # gap at 6-7
    got = set(stages.select_last_n_months_features(df, 2).columns)
    assert got == {"MAX_NDVI_9_8", "MAX_NDVI_5_4"}


def test_ps_is_aggregates_dropped():
    df = _frame(["PRCPTOT_8_7", "SoilMoist_PS_4", "SoilMoist_IS_3"])
    got = list(stages.select_last_n_months_features(df, 2).columns)
    assert got == ["PRCPTOT_8_7"]


@pytest.mark.parametrize("n", [-1, 0, None])
def test_disabled_is_a_no_op(n):
    cols = ["PRCPTOT_8_7", "PRCPTOT_5_4", "PRCPTOT_8"]
    df = _frame(cols)
    assert list(stages.select_last_n_months_features(df, n).columns) == cols


def test_width_absent_returns_frame_unchanged():
    """n longer than the season must not empty the frame."""
    cols = ["PRCPTOT_8_7", "PRCPTOT_8"]
    df = _frame(cols)
    assert list(stages.select_last_n_months_features(df, 9).columns) == cols


def test_single_month_window_supported():
    df = _frame(["PRCPTOT_8", "PRCPTOT_7", "PRCPTOT_8_7"])
    got = list(stages.select_last_n_months_features(df, 1).columns)
    assert got == ["PRCPTOT_8"]


def test_two_seasons_each_keep_their_own_window():
    """Kenya has Mar-Jul and Apr-Dec; neither season may be silently dropped."""
    df = _frame(["PRCPTOT_7_6", "PRCPTOT_6_5", "PRCPTOT_12_11", "PRCPTOT_11_10"])
    got = set(stages.select_last_n_months_features(df, 2).columns)
    assert got == {"PRCPTOT_7_6", "PRCPTOT_12_11"}, got


def test_non_contiguous_span_is_not_a_window():
    df = _frame(["PRCPTOT_8_6", "PRCPTOT_8_7"])
    got = list(stages.select_last_n_months_features(df, 2).columns)
    assert got == ["PRCPTOT_8_7"]


def test_year_wrap_window_is_contiguous():
    """Dec->Jan must count as adjacent for cross-year seasons."""
    df = _frame(["PRCPTOT_1_12"])
    assert list(stages.select_last_n_months_features(df, 2).columns) == ["PRCPTOT_1_12"]


# ---------------------------------------------------------------------------
# wiring
# ---------------------------------------------------------------------------

def _dispatch(name):
    """Mirror of the dispatch_name chain for the last<N>m_ branch."""
    m = re.match(r"^last(\d+)m_(.+)$", name)
    return (int(m.group(1)), m.group(2)) if m else None


def test_prefix_parses_n_and_algorithm():
    assert _dispatch("last2m_catboost") == (2, "catboost")
    assert _dispatch("last12m_tabpfn") == (12, "tabpfn")


def test_non_matching_names_fall_through():
    for name in ("catboost", "lastXm_catboost", "last_catboost", "top10_tabpfn"):
        assert _dispatch(name) is None


def test_dispatch_branch_present_in_source():
    assert '_last_match = re.match(r"^last(\\d+)m_(.+)$"' in SRC
    assert "self.dispatch_name = _last_match.group(2)" in SRC


def test_flag_defaults_to_minus_one_off():
    i = SRC.index("self.last_n_months = self._get_model_int")
    block = SRC[i - 400:i + 200]
    assert 'int(_last_m.group(1)) if _last_m else -1' in block
    assert '"last_n_months"' in block


def test_filter_guards_and_is_wired_into_chain():
    i = SRC.index("def _filter_last_n_months")
    block = SRC[i:i + 1800]
    assert "self.last_n_months < 1" in block, "must treat <1 as off"
    assert "_is_season_normalized_method()" in block
    assert "select_last_n_months_features" in block
    # precedence warning rather than a silently empty frame
    assert "overrides" in block and "monthly_only_features" in block
    # and it runs in the prepare chain
    assert "df = self._filter_last_n_months(df)" in SRC


def test_does_not_disable_feature_selection():
    """Unlike top<N>_/curated_, the window must not force selection off.

    Checked structurally: no `if _last_match:` branch may assign
    feature_selection. A forward source slice would wrongly catch the
    neighbouring top<N>_/auto_ branches, which legitimately do set it.
    """
    for m in re.finditer(r"if _last_match:", SRC):
        branch = SRC[m.start():m.start() + 300]
        assert "self.feature_selection" not in branch, \
            "last<N>m_ must not force feature_selection = none"


# ---------------------------------------------------------------------------
# trainers-side dispatch (the gap that raised "Unknown model name")
# ---------------------------------------------------------------------------

def test_trainers_strips_last_n_prefix():
    """geocif.py's dispatch_name is NOT what reaches the fitter — trainers
    strips the prefix independently, and adding last<N>m_ to only one of the
    two raised 'Unknown model name: last2m_catboost' at fit time."""
    from geocif.ml.trainers import strip_variant_prefix as f
    assert f("last2m_catboost") == "catboost"
    assert f("last12m_tabpfn") == "tabpfn"


def test_trainers_still_strips_existing_wrappers():
    from geocif.ml.trainers import strip_variant_prefix as f
    assert f("curated_gam") == "gam"
    assert f("top10_tabpfn") == "tabpfn"
    assert f("auto_tabpfn") == "tabpfn"


def test_trainers_leaves_plain_and_malformed_names_alone():
    from geocif.ml.trainers import strip_variant_prefix as f
    for name in ("catboost", "tabpfn", "lastXm_catboost", "last_catboost"):
        assert f(name) == name


def test_prefix_strip_is_not_duplicated_in_trainers():
    """Guard the de-duplication: both call sites must use the one helper."""
    src = (ROOT / "ml" / "trainers.py").read_text(encoding="utf-8")
    assert src.count("model_name = strip_variant_prefix(model_name)") == 2
    assert src.count('startswith(("curated_", "auto_"))') == 1, \
        "prefix-stripping must live in exactly one place"
    assert src.count("def strip_variant_prefix") == 1
