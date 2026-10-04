"""Feature selection must see the training gaps for every model (2026-10-03).

Since 0.4.1063 CID NaN is no longer zero-filled. For models outside
``_NAN_NATIVE_MODELS`` (kumo, ngboost, linear, ...) ``_setup_training_data``
median-filled ``self.X_train`` BEFORE ``_select_features``, and the selector
reads that frame, so ``select_features``' NaN gate (drop columns more than 20 %
missing) never fired. Calendar-structural windows (a March-start window missing
for 89 % of US maize counties every year) survived as near-constant columns and
displaced heat features: county maize 2012 R2 0.642 -> 0.695 once the gate
worked. The train medians must still reach the fitted matrix and the test rows.
"""
import configparser
import logging

import numpy as np
import pandas as pd

from geocif.geocif import Geocif, ModelTrainer

TARGET = "Yield (tn per ha)"


def _frame(n=40, seed=0):
    rng = np.random.default_rng(seed)
    y = rng.normal(5.0, 1.0, n)
    df = pd.DataFrame({f"noise{i}": rng.normal(size=n) for i in range(20)})
    # predictive where present but missing for half the rows: median-filled it
    # still correlates with y (r ~ 0.7), so only the NaN gate keeps it out
    df["sparse"] = np.where(np.arange(n) % 2 == 0, y, np.nan)
    # predictive and 10 % missing: passes the gate, must reach the fit filled
    df["dense"] = np.where(np.arange(n) % 10 == 0, np.nan, y + rng.normal(0, 0.1, n))
    df["Region"] = "A"
    df["Harvest Year"] = np.arange(1990, 1990 + n)
    df[TARGET] = y
    return df


def _geo(dispatch_name, df):
    obj = Geocif.__new__(Geocif)
    obj.logger = logging.getLogger("test_feature_selection_nan_gate")
    parser = configparser.ConfigParser()
    parser["ML"] = {"cache_feature_selection": "False"}
    attrs = dict(
        parser=parser, dispatch_name=dispatch_name, model_name=dispatch_name, df_train=df,
        feature_names=[c for c in df.columns if c.startswith(("noise", "sparse", "dense"))],
        target=TARGET, target_column=TARGET, target_mode="absolute",
        check_yield_trend=False, cat_features=["Region"], feature_selection="SelectKBest",
        include_lat_lon_as_feature=False, country="united_states_of_america",
        crop="maize", forecast_season=2030,
    )
    for name, value in attrs.items():
        setattr(obj, name, value)
    return obj


def test_selector_sees_the_gaps_and_the_fit_gets_the_train_medians(tmp_path):
    df = _frame()
    obj = _geo("kumo", df)
    obj._setup_training_data(df)
    # the selection frame keeps its NaN; the train medians are recorded
    assert obj.X_train["sparse"].isna().sum() == 20
    assert obj._nan_fill_values["dense"] == df["dense"].median()

    obj.apply_feature_selector(0, tmp_path)
    assert "sparse" not in obj.selected_features, "50 % missing must be gated out"
    assert "dense" in obj.selected_features

    X = ModelTrainer(obj)._prepare_training_data(df)
    assert not X[obj.selected_features].isna().any().any()
    assert X.loc[0, "dense"] == df["dense"].median()
    X_test = obj._preprocess_test_data(df.loc[[0], obj.selected_features], None)
    assert X_test["dense"].iloc[0] == df["dense"].median()


def test_selection_does_not_depend_on_nan_handling(tmp_path):
    """Selection is model-independent (apply_feature_selector caches it across
    models on that premise): kumo must pick what catboost picks."""
    df = _frame()
    picked = {}
    for name in ("kumo", "catboost"):
        obj = _geo(name, df)
        obj._setup_training_data(df)
        obj.apply_feature_selector(0, tmp_path)
        picked[name] = obj.selected_features
    assert obj._nan_fill_values == {}   # catboost: NaN-native, nothing recorded
    assert picked["kumo"] == picked["catboost"]
