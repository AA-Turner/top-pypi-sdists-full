"""Regression tests for ``Stage Window Display`` / as-of month derivation.

Bug (found 2026-08-31, brazil_mt + brazil admin_1): the calendar-order display
label was swapped only when ``int(start_stage) > int(end_stage)``. For a
reverse-cumulative (``_r``) season that WRAPS the new year the comparison is
inverted, so the swap was skipped:

    Stage_ID 4_3_2_1_12_11_10_9  ->  Sep..Apr window, as-of April
    start=4, end=9  ->  4 <= 9  ->  swap skipped
    Stage Window Display = "Apr 1-Sep 30"    (WRONG, should be "Sep 1-Apr 30")

Because ``yield_outlook._add_calendar_columns`` reads the as-of month as the
POSITIONAL right endpoint of that string, every Brazil outlook then reported
``Prediction Month = Sep`` — the PLANTING month, ~7 months earlier than the real
data cutoff, making the forecast look far more anticipatory than it was.
USA (Mar->Sep, non-wrapping) was unaffected.
"""

import pytest

from geocif.ml.stages import get_stage_information_dict
from geocif.yield_outlook import _window_bounds

# NOTE: stage strings are CID-prefixed ("PRCPTOT_...") because
# get_stage_information_dict treats the first token as the CID name.
# (stage_id, method, expected Stage Name, expected Stage Window Display, expected as-of month)
CASES = [
    # Brazil soybean: wraps the new year (Sep -> Apr). THE REGRESSION.
    ("PRCPTOT_4_3_2_1_12_11_10_9", "monthly_r", "Apr 1-Sep 30", "Sep 1-Apr 30", 4),
    # USA maize: non-wrapping (Mar -> Aug). Must be unchanged by the fix.
    ("PRCPTOT_8_7_6_5_4_3", "monthly_r", "Aug 1-Mar 31", "Mar 1-Aug 31", 8),
    ("PRCPTOT_4_3", "monthly_r", "Apr 1-Mar 31", "Mar 1-Apr 30", 4),
    # Single month: both endpoints identical, swap is a no-op.
    ("PRCPTOT_3", "monthly_r", "Mar 1-Mar 31", "Mar 1-Mar 31", 3),
    # Wrapping, shorter: Nov -> Feb.
    ("PRCPTOT_2_1_12_11", "monthly_r", "Feb 1-Nov 30", "Nov 1-Feb 28", 2),
]


@pytest.mark.parametrize("stage_id,method,exp_name,exp_swd,exp_asof", CASES)
def test_stage_window_display(stage_id, method, exp_name, exp_swd, exp_asof):
    info = get_stage_information_dict(stage_id, method)
    # The raw Stage Name convention is load-bearing and must NOT change.
    assert info["Stage Name"] == exp_name
    # The display label must be calendar-ordered: earliest month first.
    assert info["Stage Window Display"] == exp_swd


@pytest.mark.parametrize("stage_id,method,exp_name,exp_swd,exp_asof", CASES)
def test_asof_month_is_right_endpoint(stage_id, method, exp_name, exp_swd, exp_asof):
    """The as-of month must be the display label's RIGHT endpoint.

    This is exactly how ``_add_calendar_columns`` derives ``Prediction Month``,
    so it is the property that actually reached the CSVs.
    """
    info = get_stage_information_dict(stage_id, method)
    assert _window_bounds(info["Stage Window Display"])[1] == exp_asof


def test_wrapped_asof_is_not_the_planting_month():
    """Guard the specific symptom: as-of must not collapse onto planting.

    For the Brazil stage, planting is Sep (9) and the cutoff is Apr (4). The bug
    made both report Sep, which is impossible for a window carrying 8 months of
    data.
    """
    info = get_stage_information_dict("PRCPTOT_4_3_2_1_12_11_10_9", "monthly_r")
    start, end = _window_bounds(info["Stage Window Display"])
    assert start == 9, "window should START at the planting month (Sep)"
    assert end == 4, "window should END at the data cutoff (Apr)"
    assert start != end


def test_forward_method_display_equals_raw():
    """Forward-order methods keep display == raw; only ``_r`` gets swapped."""
    info = get_stage_information_dict("PRCPTOT_3_4_5", "monthly")
    assert info["Stage Window Display"] == info["Stage Name"]
