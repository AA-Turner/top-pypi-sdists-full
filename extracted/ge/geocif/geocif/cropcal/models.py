# -*- coding: utf-8 -*-
"""Machine-learning comparison against the rule-based validator.

The question is the same one the rule-based method answers -- what day does the
calendar say each transition happens -- so the two are directly comparable: the
rule-based remote-sensing day is a zero-parameter *prediction* of the calendar
day, and its ``delta`` is that prediction's error.

Models come from :func:`geocif.ml.trainers.auto_train`, the factory the yield
pipeline already uses, so ``catboost``, ``cubist``, ``tabpfn`` and ``tabicl``
arrive configured the way the rest of geocif configures them. Nothing here
constructs an estimator itself.

Circular targets
----------------
A day of year cannot be regressed directly: 1 and 365 are one day apart and a
squared-error loss treats them as 364. Each target is therefore split into its
sine and cosine, one regressor is fitted to each, and the pair is recombined
with ``atan2``. Every metric is likewise circular.
"""
from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from typing import Optional, Sequence

import numpy as np
import pandas as pd

from geocif.cropcal import circular, cv, features

logger = logging.getLogger(__name__)

#: Models compared against the rule-based baseline. Names are exactly those
#: ``geocif.ml.trainers.auto_train`` dispatches on.
DEFAULT_MODELS = ("catboost", "cubist", "tabpfn", "tabicl")

#: Name reserved for the rule-based port in every results table.
BASELINE = "rule_based"

#: Tolerance used for the "within tolerance" share, matching score.MAX_DELTA.
TOLERANCE_DAYS = 45


# --------------------------------------------------------------------------
# Metrics
# --------------------------------------------------------------------------
def circular_metrics(
    predicted: Sequence[float], observed: Sequence[float], tolerance: int = TOLERANCE_DAYS
) -> dict:
    """Circular error statistics for predicted vs. observed days of year."""
    pred = np.asarray(list(predicted), dtype=float)
    obs = np.asarray(list(observed), dtype=float)
    keep = np.isfinite(pred) & np.isfinite(obs)
    pred, obs = pred[keep], obs[keep]
    if pred.size == 0:
        return {"n": 0, "mae_days": np.nan, "rmse_days": np.nan,
                "bias_days": np.nan, f"pct_within_{tolerance}d": np.nan}

    gaps = np.array([circular.circular_gap(p, o) for p, o in zip(pred, obs)])
    signed = np.array([circular.signed_difference(p, o) for p, o in zip(pred, obs)])
    return {
        "n": int(pred.size),
        "mae_days": float(np.mean(gaps)),
        "rmse_days": float(np.sqrt(np.mean(gaps**2))),
        "bias_days": float(np.mean(signed)),
        f"pct_within_{tolerance}d": float(100.0 * np.mean(gaps <= tolerance)),
    }


# --------------------------------------------------------------------------
# Design matrix preparation
# --------------------------------------------------------------------------
def encode(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Numeric design matrix: one-hot the categoricals, median-fill the rest.

    One encoding serves every model. CatBoost could take the raw categoricals,
    but TabPFN, TabICL and Cubist cannot, and keeping a single matrix means the
    comparison is not quietly confounded by different inputs per model.
    """
    columns = features.feature_columns(frame)
    X = frame[columns].copy()

    categorical = [c for c in features.CATEGORICAL_FEATURES if c in X.columns]
    if categorical:
        X = pd.get_dummies(X, columns=categorical, dummy_na=False, dtype=float)

    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median(numeric_only=True)).fillna(0.0)
    return X, list(X.columns)


# --------------------------------------------------------------------------
# Fitting
# --------------------------------------------------------------------------
def _fit_one(model_name: str, X_train: pd.DataFrame, y_train: pd.Series, feature_names):
    """Build a regressor through the shared geocif factory, then fit it.

    ``auto_train`` **constructs and configures** the estimator; it does not fit.
    The yield pipeline fits separately through its ``BaseFitter`` hierarchy, and
    omitting that step here produced an unfitted model whose ``predict`` raised
    ``NotFittedError`` for every model in the roster.

    ``transform_output`` is a **global** sklearn setting, so it is pinned and
    restored around the fit rather than set once: TabICL and TabPFN need the
    plain-ndarray default, and leaking that to the rest of the process is a
    known geocif hazard (fixed once already in 0.4.995).
    """
    import sklearn

    from geocif.ml import trainers

    df_train = X_train.copy()
    df_train["__target__"] = y_train.to_numpy()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _hyper, model = trainers.auto_train(
            "single",
            model_name,
            "REGRESSION",
            False,
            "__target__",
            df_train,
            X_train,
            y_train,
            feature_names=list(feature_names),
            target_col="__target__",
            optimize=False,
            cat_features=[],
        )

        previous = sklearn.get_config()["transform_output"]
        sklearn.set_config(transform_output="default")
        try:
            model.fit(X_train, np.asarray(y_train).ravel())
        finally:
            sklearn.set_config(transform_output=previous)
    return model


def predict_days(
    model_name: str,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    sin_train: pd.Series,
    cos_train: pd.Series,
    feature_names,
) -> np.ndarray:
    """Predict a day of year by regressing its sine and cosine separately."""
    sin_model = _fit_one(model_name, X_train, sin_train, feature_names)
    cos_model = _fit_one(model_name, X_train, cos_train, feature_names)
    sin_pred = np.asarray(sin_model.predict(X_test), dtype=float).ravel()
    cos_pred = np.asarray(cos_model.predict(X_test), dtype=float).ravel()
    return np.array(
        [features.circle_to_day(s, c) for s, c in zip(sin_pred, cos_pred)], dtype=float
    )


# --------------------------------------------------------------------------
# Evaluation
# --------------------------------------------------------------------------
@dataclass
class Evaluation:
    """Per-row out-of-fold predictions plus the metric tables."""

    predictions: pd.DataFrame
    metrics: pd.DataFrame
    failures: list[str] = field(default_factory=list)


def evaluate(
    frame: pd.DataFrame,
    *,
    models: Sequence[str] = DEFAULT_MODELS,
    targets: Sequence[str] = features.TARGETS,
    schemes: Optional[dict[str, cv.CVScheme]] = None,
    baseline_columns: Optional[dict[str, str]] = None,
    tolerance: int = TOLERANCE_DAYS,
    n_splits: int = cv.DEFAULT_N_SPLITS,
    block_degrees: float = cv.DEFAULT_BLOCK_DEGREES,
    seed: int = 0,
) -> Evaluation:
    """Out-of-fold predictions and metrics for every model x target x CV scheme.

    Args:
        frame: the design matrix from :func:`geocif.cropcal.features.design_matrix`.
        models: model names for ``auto_train``.
        targets: which transitions to predict.
        schemes: prebuilt CV schemes; built from ``frame`` when omitted.
        baseline_columns: ``{target: column}`` holding the rule-based
            remote-sensing day, added to the tables as the ``rule_based`` model.
        tolerance: days for the "within tolerance" share.

    Metrics are reported overall and broken out by crop and by ``cm_group`` --
    the AMIS/EW split matters because the original method was only ever
    exercised on AMIS countries.
    """
    if frame.empty:
        return Evaluation(pd.DataFrame(), pd.DataFrame(), ["empty design matrix"])

    if schemes is None:
        schemes = cv.build_schemes(
            frame, n_splits=n_splits, block_degrees=block_degrees, seed=seed
        )

    X, feature_names = encode(frame)
    rows, failures = [], []

    for target in targets:
        observed = frame[f"target_{target}"].to_numpy(dtype=float)
        sin_col = frame[f"target_{target}_sin"]
        cos_col = frame[f"target_{target}_cos"]

        # The rule-based port needs no folds: it does not learn anything.
        if baseline_columns and target in baseline_columns:
            column = baseline_columns[target]
            if column in frame.columns:
                rows.append(
                    pd.DataFrame(
                        {
                            "model": BASELINE,
                            "target": target,
                            "scheme": "none",
                            "key": frame["key"],
                            "crop": frame["crop"],
                            "cm_group": frame["cm_group"],
                            "predicted": frame[column].to_numpy(dtype=float),
                            "observed": observed,
                        }
                    )
                )

        for scheme_name, scheme in schemes.items():
            for model_name in models:
                prediction = np.full(len(frame), np.nan)
                try:
                    for train_idx, test_idx in scheme.splits:
                        prediction[test_idx] = predict_days(
                            model_name,
                            X.iloc[train_idx],
                            X.iloc[test_idx],
                            sin_col.iloc[train_idx],
                            cos_col.iloc[train_idx],
                            feature_names,
                        )
                except Exception as exc:  # noqa: BLE001 - one model must not sink the run
                    message = f"{model_name}/{target}/{scheme_name}: {exc}"
                    logger.warning(f"model failed, skipping -- {message}")
                    failures.append(message)
                    continue

                rows.append(
                    pd.DataFrame(
                        {
                            "model": model_name,
                            "target": target,
                            "scheme": scheme_name,
                            "key": frame["key"],
                            "crop": frame["crop"],
                            "cm_group": frame["cm_group"],
                            "predicted": prediction,
                            "observed": observed,
                        }
                    )
                )

    if not rows:
        return Evaluation(pd.DataFrame(), pd.DataFrame(), failures or ["no model produced predictions"])

    predictions = pd.concat(rows, ignore_index=True)
    metrics = summarise_predictions(predictions, tolerance=tolerance)
    return Evaluation(predictions, metrics, failures)


def summarise_predictions(
    predictions: pd.DataFrame, *, tolerance: int = TOLERANCE_DAYS
) -> pd.DataFrame:
    """Metric table, overall and split by crop and by CM group."""
    records = []
    keys = ["model", "target", "scheme"]

    def _add(group_by: str, label, sub: pd.DataFrame) -> None:
        for values, part in sub.groupby(keys, dropna=False):
            record = dict(zip(keys, values))
            record["split"] = group_by
            record["split_value"] = label if label is not None else "all"
            record.update(circular_metrics(part["predicted"], part["observed"], tolerance))
            records.append(record)

    _add("overall", "all", predictions)
    for crop, part in predictions.groupby("crop", dropna=False):
        _add("crop", str(crop), part)
    for group, part in predictions.groupby("cm_group", dropna=False):
        _add("cm_group", str(group), part)

    out = pd.DataFrame(records)
    return out.sort_values(["target", "split", "split_value", "mae_days"]).reset_index(drop=True)
