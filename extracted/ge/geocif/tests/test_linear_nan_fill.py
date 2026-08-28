"""Scaled models (linear/gpr/george) must never see NaN.

The per-split ``_fill_missing_values`` mutates only ``self.X_train``;
``ModelTrainer._prepare_training_data`` re-slices ``df_region`` fresh, so the
fill never reached the fitted matrix. Lag features are NaN for the earliest
training years BY CONSTRUCTION, StandardScaler passes NaN through, and LassoCV
raises "Input X contains NaN" — every fold of the first last9m_linear run died
this way while the NaN-native models (catboost/tabpfn) hid the bug for months.
"""
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1] / "geocif"
SRC = (ROOT / "geocif.py").read_text(encoding="utf-8")


def _trainer_with(cat_features):
    from geocif.geocif import ModelTrainer
    obj = SimpleNamespace(cat_features=cat_features)
    t = ModelTrainer.__new__(ModelTrainer)   # avoid full Geocif init
    t.obj = obj
    return t, obj


def _frame():
    rng = np.random.default_rng(0)
    return pd.DataFrame({
        "PRCPTOT w": rng.random(40),
        "MAX_NDVI w": rng.random(40),
        "t -1 Yield (tn per ha)": [np.nan] + list(rng.random(39)),  # earliest-year NaN
        "Harvest Year": list(range(2005, 2025)) * 2,
        "Region_ID": [1] * 40,
        "Region": ["A"] * 40,
    })


def test_scaled_matrix_has_no_nan():
    from sklearn.preprocessing import StandardScaler
    t, obj = _trainer_with(["Harvest Year", "Region_ID", "Region"])
    Xs = t._scale_if_needed(_frame(), StandardScaler())
    assert not np.isnan(Xs).any(), "NaN must be imputed before the scaler"


def test_lassocv_fits_on_the_scaled_output():
    """The exact chain that killed the run must now fit."""
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LassoCV
    t, obj = _trainer_with(["Harvest Year", "Region_ID", "Region"])
    Xs = t._scale_if_needed(_frame(), StandardScaler())
    LassoCV(cv=5, random_state=42).fit(Xs, np.random.default_rng(1).random(40))


def test_fill_medians_stored_for_predict():
    from sklearn.preprocessing import StandardScaler
    t, obj = _trainer_with(["Harvest Year", "Region_ID", "Region"])
    t._scale_if_needed(_frame(), StandardScaler())
    fill = obj._scaled_model_fill
    assert "t -1 Yield (tn per ha)" in fill.index
    assert np.isfinite(fill["t -1 Yield (tn per ha)"])


def test_no_scaler_passthrough_unchanged():
    t, obj = _trainer_with(["Harvest Year", "Region_ID", "Region"])
    df = _frame()
    out = t._scale_if_needed(df, None)
    assert out is df, "NaN-native models must be untouched"
    assert not hasattr(obj, "_scaled_model_fill")


def test_predict_side_uses_train_fill():
    src_i = SRC.index('if self.dispatch_name in ("linear", "gpr", "george"):\n            X_test = X_test.drop')
    block = SRC[src_i:src_i + 700]
    assert '_scaled_model_fill' in block, "test rows must be filled with TRAIN medians"
    assert "X_test.fillna(_fill)" in block


def test_linear_feature_branch_keys_on_dispatch_name():
    """last9m_linear / curated_linear must take the same path as plain linear."""
    i = SRC.index('"""Create feature names based on model type and region."""')
    block = SRC[i:i + 1400]
    assert 'self.dispatch_name == "linear"' in block
    assert 'self.model_name == "linear"' not in block


def test_linear_branch_survives_empty_best_cid_dict():
    """correlation_plots = False -> dict_best_cid == {} -> the top-3 branch
    used to raise KeyError on region_id. It must fall back to standard
    selection instead of dying on a plotting flag (48 errors, run 2)."""
    i = SRC.index('if self.dispatch_name == "linear" and region_id in dict_best_cid')
    block = SRC[i:i + 900]
    assert 'len(dict_best_cid[region_id])' in block
    assert 'elif self.dispatch_name == "linear":' in block, "explicit fallback branch"
    assert "falling back" in block, "fallback must be logged, not silent"
    assert "dict_selected_features.get(region_id)" in block


# ---------------------------------------------------------------------------
# create_feature_names must accept a LIST of CID names (linear top-3 path)
# ---------------------------------------------------------------------------

def _cfn_stub(train_cols, keys):
    import logging
    return SimpleNamespace(
        logger=logging.getLogger("t"),
        df_train=pd.DataFrame({c: [1.0] for c in train_cols}),
        combined_keys=keys,
        method="monthly_r", model_name="last9m_linear",
        country="kenya", crop="maize",
        is_pre_season=False, forecast_season=2026,
        get_cid_column_names=lambda df: [c for c in df.columns
                                         if any(k in c for k in keys)],
        use_single_time_period_as_feature=False, lag_yield_as_feature=False,
        median_yield_as_feature=False, median_area_as_feature=False,
        analogous_year_yield_as_feature=False, use_outlook_as_feature=False,
        include_lat_lon_as_feature=False, use_spatial_neighbors=False,
        last_year_yield_as_feature=False, use_yield_trend_as_feature=None,
        use_trend_all_as_feature=False, number_lag_years=3,
        all_seasons_with_yield=[], region_zscore_cids=[],
        monthly_only_features=False, monthly_plus_fullseason_features=False,
        last_n_months=-1,
    )


def test_create_feature_names_accepts_list_of_cids():
    """The linear top-3 branch passes a LIST; the CID loop indexed it as a
    DataFrame ('CID' column) -> TypeError per candidate (~212k log lines),
    swallowed, producing a CID-less model. A list must now filter correctly."""
    from geocif.geocif import Geocif
    # column names derived from the SAME function the code uses
    from geocif.ml import stages as st
    stage = [np.arange(12, 3, -1)]                     # 12..4, harvest-first
    name = st.get_stage_information_dict("PRCPTOT_12_11_10_9_8_7_6_5_4",
                                         "monthly_r")["Stage Name"]
    cols = [f"PRCPTOT {name}", f"MAX_NDVI {name}", f"KDD {name}",
            "Yield (tn per ha)", "Region", "Harvest Year"]
    fake = _cfn_stub(cols, ["PRCPTOT", "MAX_NDVI", "KDD"])
    Geocif.create_feature_names(fake, stage, ["MAX_NDVI", "PRCPTOT"])
    assert f"PRCPTOT {name}" in fake.feature_names
    assert f"MAX_NDVI {name}" in fake.feature_names
    assert f"KDD {name}" not in fake.feature_names, \
        "a list must FILTER to the named CIDs, not pass everything"


def test_create_feature_names_dataframe_input_unchanged():
    """The existing DataFrame path must keep working identically."""
    from geocif.geocif import Geocif
    from geocif.ml import stages as st
    stage = [np.arange(12, 3, -1)]
    name = st.get_stage_information_dict("PRCPTOT_12_11_10_9_8_7_6_5_4",
                                         "monthly_r")["Stage Name"]
    cols = [f"PRCPTOT {name}", f"KDD {name}",
            "Yield (tn per ha)", "Region", "Harvest Year"]
    fake = _cfn_stub(cols, ["PRCPTOT", "KDD"])
    Geocif.create_feature_names(fake, stage, pd.DataFrame({"CID": ["PRCPTOT"]}))
    assert f"PRCPTOT {name}" in fake.feature_names
    assert f"KDD {name}" not in fake.feature_names
