"""Geocif-level fixes from the 2026-09-30 audit (A2-A6, A10, B items).

Every test builds the object with ``Geocif.__new__`` and only the
attributes the method under test reads, so no config / data directory is
needed.
"""
import configparser
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif import geocif as geocif_mod
from geocif import utils
from geocif.geocif import Geocif, ModelTrainer, _NAN_NATIVE_MODELS

TARGET = "Yield (tn per ha)"


def _geo(**attrs):
    obj = Geocif.__new__(Geocif)
    obj.logger = logging.getLogger("test_audit_fixes_geocif")
    obj.target = TARGET
    obj.forecast_season = 2020
    obj.country = "kenya"
    obj.crop = "maize"
    obj.model_name = "catboost"
    for name, value in attrs.items():
        setattr(obj, name, value)
    return obj


# --------------------------------------------------------------------------
# held-out season helpers, region filters, clustering (A6 + region filters)
# --------------------------------------------------------------------------
def test_heldout_season_helpers():
    obj = _geo()
    df = pd.DataFrame({"Harvest Year": [2018, 2019, 2020], TARGET: [1.0, 2.0, 3.0]})
    assert obj._exclude_heldout_season(df)["Harvest Year"].tolist() == [2018, 2019]
    masked = obj._mask_heldout_target(df)
    assert np.isnan(masked[TARGET].iloc[2])
    assert masked[TARGET].iloc[:2].tolist() == [1.0, 2.0]
    assert df[TARGET].iloc[2] == 3.0  # caller's frame untouched
    obj.forecast_season = None
    assert len(obj._exclude_heldout_season(df)) == 3


def test_low_production_filter_ignores_the_heldout_year():
    obj = _geo()
    prod = {"R1": 100, "R2": 90, "R3": 80, "R4": 70, "R5": 10}
    rows = []
    for region, p in prod.items():
        for yr in range(2015, 2020):
            rows.append({"Region": region, "Harvest Year": yr, "Area (ha)": 10.0, TARGET: p / 10.0})
        # held-out 2020: R5 is enormous, every other region tiny. Deciding
        # on all years would keep R5 and drop R4 instead.
        rows.append({"Region": region, "Harvest Year": 2020, "Area (ha)": 10.0,
                     TARGET: 1000.0 if region == "R5" else 0.1})
    out = obj._filter_low_production_regions(pd.DataFrame(rows))
    assert set(out["Region"]) == {"R1", "R2", "R3", "R4"}
    assert 2020 in set(out["Harvest Year"])


def test_yield_clustering_never_sees_the_heldout_yield(monkeypatch):
    seen = {}

    def fake_detect(df, target):
        seen["heldout"] = df.loc[df["Harvest Year"] == 2020, target].tolist()
        return pd.DataFrame({"Region": ["a", "b"], "Region_ID": [0, 1]})

    monkeypatch.setattr(geocif_mod.fe, "detect_clusters", fake_detect)
    obj = _geo(cluster_strategy="auto_detect")
    df = pd.DataFrame({
        "Region": ["a", "a", "b", "b"], "Harvest Year": [2019, 2020, 2019, 2020],
        TARGET: [1.0, 9.0, 2.0, 8.0],
    })
    out = obj._add_region_clusters(df.copy())
    assert seen["heldout"] and all(np.isnan(v) for v in seen["heldout"])
    assert sorted(out[TARGET].tolist()) == [1.0, 2.0, 8.0, 9.0]  # data untouched

    obj._cluster_by_crop_calendar = lambda d: pd.DataFrame({"Region": ["a", "b"], "Region_ID": [0, 0]})
    seen.clear()
    obj._cluster_by_calendar_then_yield(df.copy())
    assert seen["heldout"] and all(np.isnan(v) for v in seen["heldout"])


# --------------------------------------------------------------------------
# FLDAS / S2S forward-looking rows (A0c) and stale-row pruning (B)
# --------------------------------------------------------------------------
def test_forward_forecast_rows_are_keyed_on_the_latest_init_month():
    obj = _geo(
        simulation_stages=[np.array([7, 6, 5])], use_cids=["all"],
        _remaining_season_months=[9], _latest_covered_month=7,
    )
    obj.df_inputs = pd.DataFrame({
        "Stage_ID": ["7_6_5", "7", "9", "7", "6"],
        "Type": ["ICCLIM", "FLDAS", "FLDAS", "FLDAS", "S2S"],
        "Index": [
            "TG",
            "FLDAS_TotalPrecip_LEAD2",  # init Jul, targets Sep: fresh -> admitted
            "FLDAS_TotalPrecip_LEAD2",  # init Sep: after the cutoff (old code admitted it)
            "FLDAS_TotalPrecip_LEAD3",  # init Jul, targets Oct: not a remaining month
            "S2S_tprate_LEAD3",         # init Jun, targets Sep: stale init
        ],
    })
    out = obj._filter_by_simulation_stages()
    assert out.index.tolist() == [0, 1]


def test_prune_stale_forecast_rows_uses_the_target_month():
    obj = _geo(method="monthly_r")
    df = pd.DataFrame({
        "Type": ["ICCLIM", "FLDAS", "FLDAS", "S2S", "S2S", "FLDAS"],
        # forecast rows are stamped with the window that EMITTED them
        "Stage_ID": ["7_6_5", "7", "7", "5", "5", "7"],
        "Index": [
            "TG",
            "FLDAS_TotalPrecip_LEAD0",   # init Jul -> Jul: observed -> stale
            "FLDAS_TotalPrecip_LEAD1",   # init Jul -> Aug: keep
            "S2S_tprate_LEAD2",          # init May -> Jul: observed -> stale
            "S2S_tprate_LEAD3",          # init May -> Aug: keep
            "MEAN_FLDAS_SoilMoist",      # not a lead row
        ],
        "Region": "R", "Harvest Year": 2020,
    })
    out = obj._prune_stale_forecast_rows(df)
    assert out["Index"].tolist() == [
        "TG", "FLDAS_TotalPrecip_LEAD1", "S2S_tprate_LEAD3", "MEAN_FLDAS_SoilMoist",
    ]
    # Sharing the emitting window's label with observed rows is never, by
    # itself, "stale" (that reading deleted every forecast row).
    obj.method = "dekad_r"
    assert len(obj._prune_stale_forecast_rows(df)) == len(df)


def test_training_matrix_gets_the_same_fills_as_the_test_rows():
    obj = _geo(
        dispatch_name="ngboost", model_name="ngboost",
        selected_features=["a", "b"], cat_features=["Region"],
    )
    obj._nan_fill_values = {"a": 2.0, "b": 7.0}
    df_region = pd.DataFrame({
        "a": [1.0, np.nan], "b": [np.nan, 3.0], "Region": ["x", "x"], TARGET: [1.0, 2.0],
    })
    obj.y_train = df_region[TARGET]
    X = ModelTrainer(obj)._prepare_training_data(df_region)
    assert X["a"].tolist() == [1.0, 2.0]
    assert X["b"].tolist() == [7.0, 3.0]
    # NaN-native families record no fills and keep their NaN
    obj.dispatch_name = "catboost"
    obj.model_name = "catboost"
    obj._nan_fill_values = {}
    X = ModelTrainer(obj)._prepare_training_data(df_region)
    assert X["a"].isna().sum() == 1


def test_conformal_years_come_from_the_region_frame_not_df_train():
    obj = _geo(model=None, df_train=pd.DataFrame({"Harvest Year": [1990, 1991, 1992, 1993]}))
    mt = ModelTrainer(obj)
    y = pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2])  # region-local labels
    years = np.array([2015, 2016, 2017])
    assert mt._training_years(np.zeros((3, 2)), y, years=years).tolist() == [2015.0, 2016.0, 2017.0]
    # an ndarray without explicit years is unrecoverable: df_train is never read
    assert mt._training_years(np.zeros((3, 2)), y) is None
    X = pd.DataFrame({"x": [0, 0, 0], "Harvest Year": [2001, 2002, 2003]})
    assert mt._training_years(X, y).tolist() == [2001, 2002, 2003]


# --------------------------------------------------------------------------
# CID screens must not see the held-out season (A2, A3)
# --------------------------------------------------------------------------
def test_pearson_screen_uses_training_years_only(monkeypatch, tmp_path):
    obj = _geo(dir_analysis=tmp_path, method="monthly_r", simulation_stages=None)
    explore = tmp_path / "explore" / "cid_vs_yield" / "kenya" / "maize" / "csvs"
    explore.mkdir(parents=True)
    (explore / "pearson_summary.csv").write_text("cid,r\nSTALE,0.9\n")
    (explore / "pearson_corr_matrix.csv").write_text(",STALE\nSTALE,1.0\n")
    seen = {}

    def fake_pivot(df_long, target):
        seen["years"] = sorted(df_long["Harvest Year"].unique())
        return df_long

    def fake_summary(wide, target_col, method, season_stages):
        return pd.DataFrame({"cid": ["FRESH"], "r": [0.5]}).set_index("cid"), pd.DataFrame()

    monkeypatch.setattr(utils, "pivot_long_for_pearson", fake_pivot)
    monkeypatch.setattr(utils, "compute_pearson_summary", fake_summary)
    df_long = pd.DataFrame({"Harvest Year": [2018, 2019, 2020], "x": [1, 2, 3]})
    pearson_df, _ = obj._load_or_compute_pearson_summary(df_long)
    assert seen["years"] == [2018, 2019]
    assert list(pearson_df.index) == ["FRESH"]  # the all-years file was not used
    assert (explore / "pearson_summary.csv").read_text().startswith("cid,r\nSTALE")  # nor overwritten


def test_correlation_preselection_excludes_the_heldout_season(monkeypatch, tmp_path):
    obj = _geo(correlation_plots=True)
    obj._build_correlation_kwargs = lambda: {"dir_output": tmp_path}
    obj._correlation_cache_path = lambda d: tmp_path / "c.pkl"
    obj._load_correlation_cache = lambda p: None
    obj._save_correlation_cache = lambda p, r: None
    seen = {}

    def fake(df, **kwargs):
        seen["years"] = sorted(df["Harvest Year"].unique())
        return {}, {}

    monkeypatch.setattr(geocif_mod.correlations, "all_correlated_feature_by_time", fake)
    df = pd.DataFrame({"Harvest Year": [2018, 2019, 2020], TARGET: [1.0, 2.0, 3.0]})
    obj._generate_correlation_plots(df)
    assert seen["years"] == [2018, 2019]


# --------------------------------------------------------------------------
# NaN handling (A5)
# --------------------------------------------------------------------------
def test_update_column_names_keeps_nan(monkeypatch):
    obj = _geo(method="monthly_r")
    monkeypatch.setattr(geocif_mod.stages, "update_feature_names", lambda df, method: df)
    df = pd.DataFrame({"MEAN_ESI4WK Jul": [0.2, np.nan], "Region": ["a", "b"]})
    out = obj._update_column_names(df)
    assert np.isnan(out["MEAN_ESI4WK Jul"].iloc[1])


def test_train_only_imputation_is_applied_to_test_rows():
    obj = _geo(dispatch_name="ngboost", model_name="ngboost", cat_features=[])
    obj.X_train = pd.DataFrame({
        "a": [1.0, 3.0, np.nan], "b": [np.nan, 2.0, 2.0], "Region": ["x", "y", "z"],
    })
    obj._record_nan_fills()
    assert obj._nan_fill_values["a"] == 2.0
    assert obj._nan_fill_values["b"] == 2.0
    # the feature-selection frame keeps its gaps (test_feature_selection_nan_gate)
    assert obj.X_train[["a", "b"]].isna().sum().tolist() == [1, 1]
    X_test = pd.DataFrame({"a": [np.nan], "b": [5.0], "Region": ["x"]})
    out = obj._preprocess_test_data(X_test, None)
    assert out["a"].iloc[0] == 2.0
    assert out["b"].iloc[0] == 5.0


def test_nan_native_models_skip_imputation():
    assert {"catboost", "tabpfn", "cubist", "tabicl"} <= _NAN_NATIVE_MODELS
    assert not ({"ngboost", "linear", "gam", "pygrf", "merf"} & _NAN_NATIVE_MODELS)

    obj = _geo(
        dispatch_name="catboost", feature_names=["a"], target_column=TARGET,
        target_mode="absolute", check_yield_trend=False,
    )
    obj._clean_training_features = lambda X: X
    calls = []
    obj._record_nan_fills = lambda: calls.append("fill")
    df = pd.DataFrame({
        "a": [1.0, np.nan], "Region": ["x", "x"], "Harvest Year": [2018, 2019],
        TARGET: [1.0, 2.0],
    })
    obj._setup_training_data(df)
    assert calls == []
    assert obj.X_train["a"].isna().sum() == 1
    obj.dispatch_name = "ngboost"
    obj._setup_training_data(df)
    assert calls == ["fill"]


# --------------------------------------------------------------------------
# B items: FCST flag, DB write errors, optuna target column
# --------------------------------------------------------------------------
def test_use_outlook_as_feature_never_appends_fcst():
    src = Path(geocif_mod.__file__).read_text(encoding="utf-8")
    assert 'append("FCST")' not in src
    assert "use_outlook_as_feature is not implemented" in src


def test_store_results_reraises_db_failures(monkeypatch, tmp_path):
    obj = _geo(
        ml_model=False, parser=configparser.ConfigParser(),
        db_path=tmp_path / "x.db", estimate_ci=False,
    )

    def boom(*args, **kwargs):
        raise RuntimeError("to_db failed for table exp")

    monkeypatch.setattr(geocif_mod.output, "store", boom)
    with pytest.raises(RuntimeError, match="to_db failed"):
        obj._store_results("exp", pd.DataFrame({"x": [1]}))


def test_optuna_frame_carries_raw_and_detrended_target(monkeypatch):
    det = f"Detrended {TARGET}"
    obj = _geo(
        selected_features=["a"], cat_features=["Region"], target_column=det,
        cluster_strategy="individual", model_type="REGRESSION", optimize=True,
        fraction_loocv=0.2, y_train=pd.Series([0.1, -0.1]),
    )
    mt = ModelTrainer(obj)
    seen = {}

    def fake_auto_train(*args, **kwargs):
        seen["cols"] = list(args[5].columns)
        return {}, None

    monkeypatch.setattr(geocif_mod.trainers, "auto_train", fake_auto_train)
    df_region = pd.DataFrame({
        "a": [1.0, 2.0], "Region": ["x", "x"], TARGET: [1.0, 2.0], det: [0.1, -0.1],
    })
    mt._train_base_model(df_region, df_region[["a"]])
    assert seen["cols"] == ["a", "Region", TARGET, det]
    obj.target_column = TARGET
    mt._train_base_model(df_region, df_region[["a"]])
    assert seen["cols"] == ["a", "Region", TARGET]


# --------------------------------------------------------------------------
# conformal intervals calibrated out-of-fold (A4)
# --------------------------------------------------------------------------
def _tree_wrapper(n_years):
    from crepes import WrapRegressor
    from sklearn.tree import DecisionTreeRegressor

    rng = np.random.default_rng(0)
    n = n_years * 8
    X = pd.DataFrame({
        "x1": rng.normal(size=n), "x2": rng.normal(size=n),
        "Harvest Year": np.repeat(np.arange(2010, 2010 + n_years), 8),
    })
    y = pd.Series(3 * X["x1"].values + rng.normal(scale=1.0, size=n))
    model = WrapRegressor(DecisionTreeRegressor(random_state=0))
    model.fit(X, y)
    return model, X, y


def test_conformal_calibration_uses_out_of_fold_residuals():
    model, X, y = _tree_wrapper(10)
    mt = ModelTrainer(_geo(model=model, df_train=None))
    mt._calibrate_crepes_oof(X, y)
    assert model.calibrated
    lo_hi = model.predict_int(X.iloc[:8], confidence=0.8)
    width_oof = float((lo_hi[:, 1] - lo_hi[:, 0]).mean())

    # In-sample calibration of a fully grown tree: residuals ~0, zero width.
    ref, X2, y2 = _tree_wrapper(10)
    ref.calibrate(X2, y2)
    lo_hi_in = ref.predict_int(X2.iloc[:8], confidence=0.8)
    width_in = float((lo_hi_in[:, 1] - lo_hi_in[:, 0]).mean())
    assert width_in < 1e-6
    assert width_oof > 1.0


def test_conformal_oof_refit_declares_catboost_categoricals(caplog):
    pytest.importorskip("catboost")
    from catboost import CatBoostRegressor
    from crepes import WrapRegressor

    rng = np.random.default_rng(1)
    n = 80
    X = pd.DataFrame({
        "x1": rng.normal(size=n),
        "Region": rng.choice(["a", "b", "c"], size=n),
        "Harvest Year": np.repeat(np.arange(2010, 2020), 8),
    })
    y = pd.Series(2 * X["x1"].values + rng.normal(scale=0.5, size=n))
    model = WrapRegressor(CatBoostRegressor(iterations=40, verbose=False, random_state=0))
    model.fit(X, y, cat_features=["Region"])
    obj = _geo(model=model, df_train=None, cat_features=["Region", "Harvest Year"])
    with caplog.at_level(logging.INFO, logger="test_audit_fixes_geocif"):
        ModelTrainer(obj)._calibrate_crepes_oof(X, y)
    assert "out-of-fold residuals" in caplog.text
    assert "calibrating in-sample" not in caplog.text
    assert model.calibrated


def test_conformal_calibration_falls_back_in_sample_with_too_few_years():
    model, X, y = _tree_wrapper(2)
    calls = []
    orig = model.calibrate
    model.calibrate = lambda *a, **k: (calls.append(1), orig(*a, **k))[1]
    mt = ModelTrainer(_geo(model=model, df_train=None))
    mt._calibrate_crepes_oof(X, y)
    assert calls == [1]
    assert model.calibrated
