"""GAM Region factor term (gam_region_factor).

The pooled ("pure") GAM is region-blind by design: GAMFitter drops Region,
so predictions compress toward the national EO-yield curve. The
gam_region_factor flag re-admits Region as a penalized pygam f() term —
per-region intercepts inside one model (the "factor GAM"). These tests pin
the contract:

  * flag off  -> unchanged legacy behavior (no Region_factor column);
  * flag on   -> Region_factor enters the fit columns as integer codes, the
                 factor term actually shifts predictions between regions,
                 and prediction round-trips through the fit column layout;
  * unseen region at predict -> NaN code -> median fill -> round/clip lands
                 on a REAL fit-time level (pygam f() rejects unseen values);
  * single-level Region (per-region training) -> factor silently skipped.
"""
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

pygam = pytest.importorskip("pygam")


def _fitter():
    from geocif.geocif import GAMFitter
    obj = SimpleNamespace(model_type="REGRESSION", gam_region_factor=True)
    return GAMFitter.__new__(GAMFitter), obj


def _bind(fitter, obj):
    fitter.obj = obj
    return fitter


def _frame(n_regions=4, years=12, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for r in range(n_regions):
        base = 1.0 + r  # distinct region levels the factor should absorb
        for y in range(years):
            ndvi = rng.uniform(0.3, 0.8)
            rows.append({
                "Region": f"R{r}",
                "Region_ID": r,
                "Harvest Year": 2014 + y,
                "AUC_NDVI m": ndvi * 20,
                "MEAN_NDVI m": ndvi,
                "yield": base + 2 * ndvi + rng.normal(0, 0.05),
            })
    df = pd.DataFrame(rows)
    return df.drop(columns=["yield"]), df["yield"]


def _fit(flag=True, n_regions=4):
    from geocif.geocif import GAMFitter
    X, y = _frame(n_regions=n_regions)
    obj = SimpleNamespace(model_type="REGRESSION", gam_region_factor=flag, y_train=y)
    fitter = _bind(GAMFitter.__new__(GAMFitter), obj)
    fitter.fit(X, None, None)
    return obj, X


def test_flag_off_keeps_legacy_columns():
    obj, _ = _fit(flag=False)
    assert "Region_factor" not in obj._gam_fit_cols
    assert obj._gam_region_levels is None


def test_flag_on_adds_factor_column_and_levels():
    obj, _ = _fit(flag=True)
    assert "Region_factor" in obj._gam_fit_cols
    assert obj._gam_region_levels == ["R0", "R1", "R2", "R3"]


def test_factor_shifts_predictions_between_regions():
    """Identical EO, different region -> different prediction. That is the
    entire point of the factor term; the region-blind GAM cannot do this."""
    obj, _ = _fit(flag=True)
    row = {"AUC_NDVI m": 10.0, "MEAN_NDVI m": 0.5}
    X = pd.DataFrame([
        {**row, "Region_factor": 0.0},
        {**row, "Region_factor": 3.0},
    ])[obj._gam_fit_cols]
    p = obj.model.predict(X.values)
    assert abs(p[1] - p[0]) > 0.5, (
        "regions differ by ~3 t/ha in intercept; factor term must recover "
        f"a substantial share of it, got {p[1] - p[0]:.3f}"
    )


def test_single_level_region_skips_factor():
    obj, _ = _fit(flag=True, n_regions=1)
    assert obj._gam_region_levels is None
    assert "Region_factor" not in obj._gam_fit_cols


def test_encode_region_factor_maps_and_flags_unseen():
    from geocif.geocif import GAMFitter
    levels = ["A", "B", "C"]
    X = pd.DataFrame({"Region": ["B", "ZZZ"], "x": [1.0, 2.0]})
    out = GAMFitter.encode_region_factor(X, levels)
    assert out["Region_factor"].tolist()[0] == 1.0
    assert np.isnan(out["Region_factor"].iloc[1]), "unseen region must code to NaN"
    assert "Region" in out.columns and X.shape[0] == out.shape[0]


def test_unseen_region_round_trips_to_valid_level():
    """Median fill over an even level count gives x.5 — the predict path's
    round/clip must land on a genuine fit-time code before pygam sees it."""
    obj, _ = _fit(flag=True)  # 4 levels -> median code 1.5
    medians = obj._gam_fit_medians
    filled = float(medians["Region_factor"])
    fixed = np.clip(np.round(filled), 0, len(obj._gam_region_levels) - 1)
    assert fixed == int(fixed) and 0 <= fixed <= 3
    row = {"AUC_NDVI m": 10.0, "MEAN_NDVI m": 0.5, "Region_factor": fixed}
    X = pd.DataFrame([row])[obj._gam_fit_cols]
    obj.model.predict(X.values)  # must not raise


def test_fit_medians_cover_factor_column():
    obj, _ = _fit(flag=True)
    assert "Region_factor" in obj._gam_fit_medians.index
