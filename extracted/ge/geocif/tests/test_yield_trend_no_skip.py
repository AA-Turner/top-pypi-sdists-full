"""The `past`-mode yield-trend feature must never skip a region outright.

Before this, a region whose pre-forecast series was shorter than
``tseg_minlength`` was skipped with ``continue``, leaving ``Yield Trend`` NaN
for every one of its rows. At usa_admin1 that silently removed the feature
from the 2005 and 2006 folds entirely (0% selection) while later folds had
it -- a fold-to-fold inconsistency easily mistaken for a skill change.

The contract now: fit the best estimator the data supports.
  >= tseg_minlength rows -> BEAST-segmented trend
  2 .. tseg_minlength-1  -> plain OLS line
  < 2 rows               -> NaN (genuinely nothing to fit)
"""
import re
from pathlib import Path

import numpy as np
import pytest

SRC = Path(__file__).resolve().parents[1] / "geocif" / "geocif.py"
BODY = SRC.read_text(encoding="utf-8", errors="ignore")
FUNC = BODY[BODY.index("def _compute_yield_trend_feature"):]
FUNC = FUNC[:FUNC.index("\n    def ", 1)]


def test_short_series_no_longer_skips_the_region():
    """The only `continue` left must be guarded by the <2-row case."""
    assert "if len(group) < 2:" in FUNC, "the <2-row guard is gone"
    # the old unconditional skip must not come back
    assert "skipping (need >= 5 for OLS)" not in FUNC
    conts = re.findall(r"\n\s+continue", FUNC)
    # Exactly two `continue`s are legitimate: the <2-row case above, and
    # the pre-existing guard for a fit that returned a NaN intercept.
    # A third one likely means a region skip was reintroduced.
    assert len(conts) == 2, f"expected two continues, found {len(conts)}"
    assert "if np.isnan(intercept):" in FUNC


def test_short_series_falls_back_to_plain_ols():
    assert "use_beast = False" in FUNC
    assert "np.polyfit(years, yields, 1)" in FUNC, \
        "no plain-OLS fallback for short series"


def test_beast_still_used_for_long_series():
    assert "if use_beast:" in FUNC
    assert "trend.segment_aware_trend(" in FUNC


def test_per_region_warning_replaced_by_fold_summary():
    """3,465 per-region warnings in one run buried the rest of the log."""
    assert "_n_trend_ols" in FUNC and "_n_trend_none" in FUNC
    assert "region(s) used plain OLS" in FUNC


@pytest.mark.parametrize("n_rows,expect", [
    (0, "nan"), (1, "nan"), (2, "ols"), (4, "ols"), (5, "beast"), (9, "beast"),
])
def test_estimator_selection_arithmetic(n_rows, expect):
    """The branch arithmetic the patch encodes, with tseg_minlength = 5."""
    tseg_minlength = 5
    if n_rows < 2:
        got = "nan"
    elif n_rows < tseg_minlength:
        got = "ols"
    else:
        got = "beast"
    assert got == expect


def test_polyfit_matches_a_known_line():
    """A 3-point exactly-linear series must recover its slope/intercept."""
    years = np.array([2005.0, 2006.0, 2007.0])
    yields = 2.0 + 0.5 * (years - 2005.0)
    slope, intercept = np.polyfit(years, yields, 1)
    assert slope == pytest.approx(0.5)
    assert intercept + slope * 2005.0 == pytest.approx(2.0)
