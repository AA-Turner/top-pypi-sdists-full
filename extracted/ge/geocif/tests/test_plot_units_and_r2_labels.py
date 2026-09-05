"""Regression tests: RMSE plot units, and the R2-vs-r2 label convention.

BUG 1 (units). ``yield_outlook`` converts yields to the crop's DISPLAY units
via ``_convert_yield_columns`` (bu/ac for maize/soybean) BEFORE building
``df_mape``. The three RMSE plotters in viz/diagnostics.py nonetheless
hardcoded ``"RMSE (Mg/ha)"`` on their axes, so a soybean RMSE-by-year chart
showed 1.4-3.7 labelled Mg/ha when soybean yields are only ~2.7-4.3 Mg/ha --
i.e. an implied >100% error. The values were bu/ac all along.

BUG 2 (label). ``scatter_obs_pred`` and one annotation in analysis.py compute
``r2_score`` -- the COEFFICIENT OF DETERMINATION, 1 - SSres/SStot, which
charges for bias and slope -- but printed ``$r^2$``, which conventionally
means squared Pearson correlation. The two differ whenever the fit departs
from 1:1 (on the 2026 state scatter: 0.9422 vs 0.9739 for corn). Sites that
genuinely compute pearson**2 keep the lowercase label.
"""

import inspect
import pathlib

import pytest

from geocif.viz import diagnostics as diag

RMSE_FNS = ["rmse_by_year", "rmse_box_by_year", "rmse_box_by_region"]


# ------------------------------------------------------------------ units
@pytest.mark.parametrize("fn", RMSE_FNS)
def test_rmse_plotters_accept_yield_units(fn):
    sig = inspect.signature(getattr(diag, fn))
    assert "yield_units" in sig.parameters, f"{fn} cannot be told its units"


@pytest.mark.parametrize("fn", RMSE_FNS)
def test_rmse_yield_units_defaults_to_mg_ha(fn):
    """Default preserves old behaviour for callers that do not pass units."""
    sig = inspect.signature(getattr(diag, fn))
    assert sig.parameters["yield_units"].default == "Mg/ha"


@pytest.mark.parametrize("fn", RMSE_FNS)
def test_rmse_axis_label_is_not_hardcoded(fn):
    src = inspect.getsource(getattr(diag, fn))
    assert '"RMSE (Mg/ha)"' not in src, (
        f"{fn} still hardcodes Mg/ha on its axis")
    assert 'RMSE ({yield_units})' in src, (
        f"{fn} does not interpolate yield_units into its axis label")


def test_yield_outlook_passes_display_units_to_all_three():
    """The call sites must forward the crop's display label, otherwise the
    plots silently fall back to the Mg/ha default while holding bu/ac data."""
    src = (pathlib.Path(__import__("geocif").__file__).parent
           / "yield_outlook.py").read_text(encoding="utf-8", errors="ignore")
    assert src.count("yield_units=_yield_display_for(parser, crop)[0]") >= 3, (
        "fewer than 3 RMSE call sites forward the display units")


# ------------------------------------------------------------------ labels
def test_scatter_obs_pred_labels_coefficient_of_determination():
    src = inspect.getsource(diag.scatter_obs_pred)
    assert "r2_score(" in src, "assumption changed: no longer uses r2_score"
    assert "$R^2$" in src, "computes r2_score but does not label it R^2"
    assert "$r^2$" not in src, "still carries the lowercase r^2 label"


def test_analysis_lowercase_r2_only_where_pearson_squared():
    """analysis.py legitimately uses BOTH conventions. Every '$r^2$' left in
    the file must belong to the pearsonr(...)**2 metric, not to r2_score."""
    src = (pathlib.Path(__import__("geocif").__file__).parent
           / "analysis.py").read_text(encoding="utf-8", errors="ignore")
    # the metrics Series built from pearsonr(...)**2 keeps "$r^2$" as a KEY;
    # what must not exist is an r2_score value annotated as $r^2$
    assert 'f"$r^2$: {r2:.2f}\\n"' not in src, (
        "an r2_score value is still annotated as $r^2$")
    assert "pearsonr" in src, "assumption changed: pearson r2 no longer used"


def test_the_two_conventions_actually_differ():
    """Guard the premise: if they were interchangeable the fix would be moot.
    Uses the real 2026 corn numbers -- slope 0.825 away from 1:1."""
    import numpy as np
    from scipy import stats
    from sklearn.metrics import r2_score

    usda = np.array([212.05, 205.99, 216.03, 126.02, 197.07,
                     180.03, 183.06, 195.01, 151.03, 184.01])
    pred = np.array([208.52, 200.88, 211.56, 134.97, 196.66,
                     181.94, 194.24, 199.55, 161.84, 185.40])
    cod = r2_score(usda, pred)
    pear = stats.pearsonr(usda, pred)[0] ** 2
    assert pear > cod, "expected pearson^2 to flatter a biased/off-slope fit"
    assert pear - cod > 0.02, (
        f"conventions nearly identical here ({cod:.4f} vs {pear:.4f}) -- "
        f"pick a sharper example")
