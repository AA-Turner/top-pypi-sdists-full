"""SHAP for cubist and kumo: the mixed-type permutation branch of ml/xai.

Both models are fitted on frames that mix a string Region column with numeric
CIDs, and their predict needs every fitted column back. Before this branch,
cubist and kumo fell through to TreeExplainer, which rejects non-tree models,
and the plain permutation branch drops string columns, which neither model's
predict accepts.
"""

import sqlite3

import numpy as np
import pandas as pd
import pytest

from geocif.ml import xai


def _frame(n_years=8, seed=0):
    rng = np.random.RandomState(seed)
    regions = ["Eastern", "Southern", "Western"]
    rows = []
    for y in range(2012, 2012 + n_years):
        for i, r in enumerate(regions):
            rows.append({
                "MIN_ESI4WK Feb-Mar": rng.normal(40, 8),
                "PRCPTOT Jan-Mar": rng.normal(150, 30),
                "Harvest Year": y,
                "Region_ID": i,
                "Region": r,
            })
    df = pd.DataFrame(rows)
    df["Region_ID"] = df["Region_ID"].astype("category")
    df.loc[3, "PRCPTOT Jan-Mar"] = np.nan
    effect = {"Eastern": 5.0, "Southern": -3.0, "Western": 0.0}
    df["Yield (tn per ha)"] = (
        0.5 * df["MIN_ESI4WK Feb-Mar"].fillna(40) + df["Region"].map(effect)
        + rng.normal(0, 0.5, len(df))
    )
    return df


FEATURES = ["MIN_ESI4WK Feb-Mar", "PRCPTOT Jan-Mar", "Harvest Year", "Region_ID", "Region"]


class _StrictModel:
    """Predicts like the fitted cubist/kumo do: refuses a frame that lacks a
    fitted column or carries Region as anything but its string level."""

    effect = {"Eastern": 5.0, "Southern": -3.0, "Western": 0.0}

    def predict(self, X):
        assert isinstance(X, pd.DataFrame), "predict needs a DataFrame"
        assert list(X.columns) == FEATURES, list(X.columns)
        assert X["Region"].map(lambda v: isinstance(v, str)).all(), "Region must be a string level"
        assert isinstance(X["Region_ID"].dtype, pd.CategoricalDtype)
        return (0.5 * X["MIN_ESI4WK Feb-Mar"].fillna(40) + X["Region"].map(self.effect)).to_numpy()


def test_codec_round_trip_keeps_values_and_dtypes():
    df = _frame()
    tr, te = df.iloc[:-3][FEATURES], df.iloc[-3:][FEATURES]
    tr_c, te_c, decode = xai._mixed_type_codec(tr, te)
    assert all(pd.api.types.is_float_dtype(t) for t in tr_c.dtypes)
    back = decode(tr_c.to_numpy())
    pd.testing.assert_frame_equal(back, tr.reset_index(drop=True))
    back_te = decode(te_c)  # shap may also pass a DataFrame
    pd.testing.assert_frame_equal(back_te, te.reset_index(drop=True))


@pytest.mark.parametrize("model_name", ["kumo", "cubist"])
def test_explain_mixed_type_model(tmp_path, model_name):
    df = _frame()
    df_train, df_test = df[df["Harvest Year"] < 2019].copy(), df[df["Harvest Year"] == 2019].copy()
    model = _StrictModel()  # no feature_names_in_: features come from kwargs
    expected = model.predict(df_test[FEATURES])  # explain() casts df_test's Region_ID in place
    db = tmp_path / "outlook.db"
    xai.explain(
        df_train, df_test,
        model=model, model_name=model_name, forecast_season=2019,
        crop="poppy", country="afghanistan", analysis_dir=tmp_path, db_path=db,
        feature_names=FEATURES, predict_fn=model.predict,
    )
    con = sqlite3.connect(db)
    shap_df = pd.read_sql("select * from shap_values", con)
    imp = pd.read_sql("select * from feature_importance", con)
    con.close()

    assert len(shap_df) == len(df_test)
    assert set(imp["Feature"]) == set(FEATURES)  # the target never becomes a feature
    # Permutation SHAP is exact-additive: base + sum(SHAP) = f(x).
    shap_sum = shap_df[[f"SHAP_{f}" for f in FEATURES]].sum(axis=1) + shap_df["Base Value"]
    np.testing.assert_allclose(shap_sum, expected, atol=1e-6)
    # Region drives the prediction, so it must get credit; Harvest Year cannot.
    assert shap_df["SHAP_Region"].abs().max() > 1.0
    np.testing.assert_allclose(shap_df["SHAP_Harvest Year"], 0, atol=1e-9)
    # Feature values sit next to their SHAP values for dependence plots.
    np.testing.assert_allclose(shap_df["VALUE_MIN_ESI4WK Feb-Mar"], df_test["MIN_ESI4WK Feb-Mar"])


def test_folds_and_models_do_not_overwrite_each_other(tmp_path):
    """shap_values / feature_importance used a positional 0..n-1 key, so each
    fold's upsert replaced the previous fold's rows (7 rows left after a run)."""
    df = _frame()
    db = tmp_path / "outlook.db"
    model = _StrictModel()
    for name in ("kumo", "cubist"):
        for year in (2018, 2019):
            tr, te = df[df["Harvest Year"] != year].copy(), df[df["Harvest Year"] == year].copy()
            xai.explain(
                tr, te, model=model, model_name=name, forecast_season=year, crop="poppy",
                country="afghanistan", analysis_dir=tmp_path, db_path=db,
                feature_names=FEATURES, predict_fn=model.predict,
            )
    con = sqlite3.connect(db)
    shap_df = pd.read_sql("select * from shap_values", con)
    imp = pd.read_sql("select * from feature_importance", con)
    con.close()
    assert len(shap_df) == 2 * 2 * 3  # models x folds x zones
    assert shap_df.groupby(["Model", "Harvest Year"]).size().eq(3).all()
    assert len(imp) == 2 * 2 * len(FEATURES)


def test_explain_real_cubist(tmp_path):
    cubist = pytest.importorskip("cubist")
    df = _frame(n_years=10)
    df["Region_ID"] = df["Region_ID"].astype(int)
    df_train, df_test = df[df["Harvest Year"] < 2021].copy(), df[df["Harvest Year"] == 2021].copy()
    m = cubist.Cubist(n_committees=1, random_state=0)
    m.fit(df_train[FEATURES], df_train["Yield (tn per ha)"])
    xai.explain(
        df_train, df_test,
        model=m, model_name="cubist", forecast_season=2021,
        crop="poppy", country="afghanistan", analysis_dir=tmp_path, db_path=tmp_path / "o.db",
        feature_names=FEATURES, predict_fn=m.predict,
    )
    con = sqlite3.connect(tmp_path / "o.db")
    shap_df = pd.read_sql("select * from shap_values", con)
    con.close()
    feats = [c for c in shap_df.columns if c.startswith("SHAP_")]
    shap_sum = shap_df[feats].sum(axis=1) + shap_df["Base Value"]
    np.testing.assert_allclose(shap_sum, m.predict(df_test[FEATURES]), rtol=1e-5, atol=1e-5)
