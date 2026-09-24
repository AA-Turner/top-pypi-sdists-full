# -*- coding: utf-8 -*-
"""Machine-learning comparison against the rule-based validator and a null.

The question is the one the rule-based method answers -- what day does the
calendar say each transition happens -- so the two are directly comparable:
the rule-based remote-sensing day is a zero-parameter *prediction* of the
calendar day, and its difference is that prediction's error. Planting and
harvest have no satellite rule, so every target is also scored against an
out-of-fold **climatology** null: the circular median of the training rows'
calendar day for the same crop, hemisphere and season.

Models come from :func:`geocif.ml.trainers.auto_train`, the factory the yield
pipeline already uses, so ``catboost``, ``cubist``, ``tabpfn`` and ``tabicl``
arrive configured the way the rest of geocif configures them. Nothing here
constructs an estimator itself.

Two target encodings
--------------------
A day of year cannot be regressed directly: 1 and 365 are one day apart and a
squared-error loss treats them as 364.

``sincos``
    The target's sine and cosine are fitted by two regressors and recombined
    with ``atan2``. The length of the predicted vector (``resultant``) is kept:
    when a model cannot separate two modes (northern vs southern planting, six
    months apart) both regressors shrink toward the middle, the vector
    collapses and ``atan2`` returns an essentially arbitrary day. A short
    resultant is the only way to tell that ambiguity from a confident miss.
``anchored``
    The target is expressed as a signed circular offset from a calendar-free
    landmark of the same year -- the steepest rise of the NDVI median
    (``features.ANCHOR_FEATURE``) -- and one regressor predicts the offset.
    Planting precedes that rise and harvest follows it for every crop in both
    hemispheres, so the offset is unimodal and never near the +/-182 wrap.

Both are run and reported side by side; which is better is a result, not a
design decision.

Sample and leakage guards
-------------------------
* Features are the allow-list in :mod:`geocif.cropcal.features`; the rule-based
  satellite days are asserted absent from it before any fold is fitted.
* Median imputation is fitted on the training fold only.
* A target is masked per row rather than the row dropped, so a calendar row
  lacking one transition never shrinks another transition's comparison.
* Planting and harvest are masked for wall-to-wall calendar rows, whose
  planting day is a parser artefact (see :class:`geocif.cropcal.calendar.StageDates`).
* Every metric is circular, and the bias is **observed minus predicted** --
  calendar minus prediction -- the same sign as the ``*_diff_days`` columns.
"""
from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from typing import Optional, Sequence

import numpy as np
import pandas as pd

from geocif.cropcal import circular, cv, features, score

logger = logging.getLogger(__name__)

#: Models compared against the baselines. Names are exactly those
#: ``geocif.ml.trainers.auto_train`` dispatches on.
DEFAULT_MODELS = ("catboost", "cubist", "tabpfn", "tabicl")

#: Name reserved for the rule-based port in every results table.
BASELINE = "rule_based"

#: Name reserved for the out-of-fold climatology null.
CLIMATOLOGY = "climatology"

#: Target encodings, see the module docstring.
ENCODINGS = ("sincos", "anchored")

#: Tolerance used for the "within tolerance" share, matching score.MAX_DELTA.
TOLERANCE_DAYS = 45

#: The agreement-class edges below the tolerance, reported alongside it so the
#: model table lines up with the rule-based classes, plus the 60-day edge of
#: Franch et al. (2022)'s residual maps so the two studies bin identically.
EXTRA_THRESHOLDS = (15, 30, 60)

#: A residual beyond this is a blunder, not an error: the wrap failures of a
#: collapsed sin/cos vector live here. Franch et al. report the share > 60 d.
BLUNDER_DAYS = 60

#: Predicted season length (harvest - planting, circular) outside this range
#: is implausible for an annual crop; Franch et al. mask it in their maps. Here
#: it is a cross-target consistency metric, because the four days are
#: predicted independently.
LOS_PLAUSIBLE_DAYS = (30, 280)

#: A ``sincos`` prediction with a resultant below this is "ambiguous".
LOW_RESULTANT = 0.5

#: Climatology null: a training group is trusted when it has at least this
#: many rows and its days are at least this concentrated (mean resultant
#: length); otherwise the next, coarser level is tried.
MIN_GROUP_ROWS = 5
MIN_GROUP_CONCENTRATION = 0.3

#: Southern-hemisphere days are shifted by this before pooling with the north.
HEMISPHERE_SHIFT_DAYS = 182

#: Targets whose value is meaningless on a wall-to-wall calendar row.
WALL_TO_WALL_MASKED_TARGETS = ("planting", "harvest")

#: Paired cluster bootstrap (over spatial tiles) for the skill interval.
BOOTSTRAP_RESAMPLES = 500
BOOTSTRAP_LEVEL = 0.90


# --------------------------------------------------------------------------
# Metrics
# --------------------------------------------------------------------------
def _unwrap(days: np.ndarray, reference: float) -> np.ndarray:
    """Days as signed offsets from a reference day, in ``(-182, 182]``.

    The general form of Franch et al. (2022)'s linearisation, which shifted
    DOYs above a crop-specific threshold by -365 so the two hemispheres' clusters
    lie on one line. Unwrapping around the observed circular mean does the same
    without a per-crop constant.
    """
    return np.array([circular.signed_difference(d, reference) for d in days], dtype=float)


def circular_metrics(
    predicted: Sequence[float],
    observed: Sequence[float],
    tolerance: int = TOLERANCE_DAYS,
    resultant: Optional[Sequence[float]] = None,
) -> dict:
    """Circular error statistics for predicted vs. observed days of year.

    ``bias_days`` is observed minus predicted (positive: the calendar is later
    than the prediction), matching the sign of the frame's ``*_diff_days``.
    ``rmse_debiased_days`` is the circular standard deviation of the signed
    residuals -- the scatter left once that systematic offset is removed --
    reported NEXT TO the raw RMSE, never instead of it.

    ``calibration_slope`` / ``calibration_intercept_days`` come from regressing
    the observed day on the predicted day, both unwrapped around the observed
    circular mean (Franch et al.'s ``y = ax + b``). Slope 1, intercept 0 is
    calibrated; slope > 1 means the predictions are shrunk toward the mean.

    ``r2_linearised`` is Franch et al.'s Eq. 11 on the same unwrapped days --
    it is inflated by any population that spans both hemispheres, since
    telling north from south is most of its variance. ``r2_circular`` is the
    squared Jammalamadaka-Sarma circular correlation and has no such artefact.
    Quote skill against the climatology null before either.

    ``pct_low_resultant`` is the share of rows whose ``sincos`` prediction was
    ambiguous; NaN when the encoding has no resultant. ``pct_blunders`` is the
    share of residuals beyond :data:`BLUNDER_DAYS`.
    """
    pred = np.asarray(list(predicted), dtype=float)
    obs = np.asarray(list(observed), dtype=float)
    keep = np.isfinite(pred) & np.isfinite(obs)
    thresholds = tuple(sorted(set(EXTRA_THRESHOLDS) | {int(tolerance)}))
    empty = {
        "n": 0, "mae_days": np.nan, "median_ae_days": np.nan, "rmse_days": np.nan,
        "rmse_debiased_days": np.nan, "bias_days": np.nan, "pct_blunders": np.nan,
        "calibration_slope": np.nan, "calibration_intercept_days": np.nan,
        "r2_linearised": np.nan, "r2_circular": np.nan, "pct_low_resultant": np.nan,
    }
    for t in thresholds:
        empty[f"pct_within_{t}d"] = np.nan
    if not keep.any():
        return empty

    pred, obs = pred[keep], obs[keep]
    gaps = np.array([circular.circular_gap(p, o) for p, o in zip(pred, obs)])
    signed = np.array([circular.signed_difference(o, p) for p, o in zip(pred, obs)])
    bias = float(np.mean(signed))
    out = {
        "n": int(pred.size),
        "mae_days": float(np.mean(gaps)),
        "median_ae_days": float(np.median(gaps)),
        "rmse_days": float(np.sqrt(np.mean(gaps**2))),
        "rmse_debiased_days": float(np.sqrt(np.mean((signed - bias) ** 2))),
        "bias_days": bias,
        "pct_blunders": float(100.0 * np.mean(gaps > BLUNDER_DAYS)),
        "calibration_slope": np.nan,
        "calibration_intercept_days": np.nan,
        "r2_linearised": np.nan,
        "r2_circular": np.nan,
        "pct_low_resultant": np.nan,
    }
    for t in thresholds:
        out[f"pct_within_{t}d"] = float(100.0 * np.mean(gaps <= t))

    if pred.size >= 3:
        angles = 2.0 * np.pi * obs / circular.DAYS_IN_YEAR
        centre = float((np.arctan2(np.sin(angles).mean(), np.cos(angles).mean()) % (2 * np.pi))
                       * circular.DAYS_IN_YEAR / (2 * np.pi))
        obs_u, pred_u = _unwrap(obs, centre), _unwrap(pred, centre)
        ss_tot = float(np.sum((obs_u - obs_u.mean()) ** 2))
        if ss_tot > 0:
            out["r2_linearised"] = float(1.0 - np.sum(signed**2) / ss_tot)
        if np.var(pred_u) > 0:
            slope, intercept = np.polyfit(pred_u, obs_u, 1)
            out["calibration_slope"] = float(slope)
            out["calibration_intercept_days"] = float(intercept)
        r2, _p = score.circular_r2(pred, obs)
        out["r2_circular"] = float(r2) if np.isfinite(r2) else np.nan

    if resultant is not None:
        res = np.asarray(list(resultant), dtype=float)[keep]
        if np.isfinite(res).any():
            out["pct_low_resultant"] = float(100.0 * np.nanmean(res < LOW_RESULTANT))
    return out


# --------------------------------------------------------------------------
# Design matrix preparation
# --------------------------------------------------------------------------
def encode(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Numeric design matrix: one-hot the categoricals, coerce the rest.

    One encoding serves every model. CatBoost could take the raw categoricals,
    but TabPFN, TabICL and Cubist cannot, and keeping a single matrix means the
    comparison is not quietly confounded by different inputs per model.

    No imputation happens here -- that is fitted per fold in :func:`impute`.
    The allow-list is checked against the baselines and the target/calendar
    prefixes so a leak cannot be reintroduced by a rename.
    """
    columns = features.feature_columns(frame)
    baselines = set(features.BASELINE_COLUMNS.values())
    offending = [c for c in columns if c in baselines or c.startswith(("target_", "calendar_", "satellite_"))]
    if offending:
        raise ValueError(f"feature allow-list contains non-features: {offending}")

    X = frame[columns].copy()
    categorical = [c for c in features.CATEGORICAL_FEATURES if c in X.columns]
    if categorical:
        X = pd.get_dummies(X, columns=categorical, dummy_na=False, dtype=float)
    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf, -np.inf], np.nan)
    return X, list(X.columns)


def impute(X_train: pd.DataFrame, X_test: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Median-fill both folds with medians fitted on the TRAINING fold only.

    Filling on the whole matrix leaked the test fold's feature marginals into
    training, and with the NaN-prone moisture groups that leak grows with every
    region that lacks a variable. The ``*_available`` indicators tell the model
    when a fill is a fill.
    """
    medians = X_train.median(numeric_only=True)
    return X_train.fillna(medians).fillna(0.0), X_test.fillna(medians).fillna(0.0)


# --------------------------------------------------------------------------
# Climatology null
# --------------------------------------------------------------------------
def _shifted(days: np.ndarray, hemisphere: np.ndarray) -> np.ndarray:
    shift = np.where(np.asarray(hemisphere).astype(str) == "S", HEMISPHERE_SHIFT_DAYS, 0)
    return (np.asarray(days, dtype=float) + shift) % circular.DAYS_IN_YEAR


def _unshift(day: float, hemisphere: str) -> float:
    if not np.isfinite(day):
        return day
    shift = HEMISPHERE_SHIFT_DAYS if str(hemisphere) == "S" else 0
    return float((day - shift) % circular.DAYS_IN_YEAR)


def _group_estimate(days: np.ndarray) -> tuple[float, int, float]:
    """``(circular median, n, concentration)`` of a training group."""
    arr = np.asarray(days, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan"), 0, float("nan")
    angles = 2.0 * np.pi * arr / circular.DAYS_IN_YEAR
    concentration = float(np.hypot(np.sin(angles).mean(), np.cos(angles).mean()))
    return features.circular_median_day(arr), int(arr.size), concentration


def climatology_predict(
    train: pd.DataFrame, test: pd.DataFrame, target: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Out-of-fold climatology null for one target.

    For each test row the first trusted level wins, coarsest last:

    1. ``crop_hemisphere_season`` -- circular median of training rows with the
       same crop, hemisphere and season. Kenya's maize seasons 1 and 2 are six
       months apart; pooled, their median is meaningless.
    2. ``crop_hemisphere``
    3. ``crop_shifted`` -- same crop, both hemispheres, southern days shifted
       by half a year before pooling and the estimate shifted back. A whole
       (crop, S) population can sit in one or two spatial tiles and be held
       out entirely; a hemisphere-blind fallback would then predict a northern
       planting day, ~180 days wrong, and make every model look skilful.
    4. ``all_shifted`` -- every training row, shifted; accepted at any size.

    A level is trusted when it has :data:`MIN_GROUP_ROWS` rows and its days
    have mean resultant length >= :data:`MIN_GROUP_CONCENTRATION`.

    Returns ``(days, level, n_group, concentration)`` aligned with ``test``.
    """
    column = f"target_{target}"
    t = train[np.isfinite(train[column].to_numpy(dtype=float))]
    tr_days = t[column].to_numpy(dtype=float)
    tr_crop = t["crop"].astype(str).to_numpy()
    tr_hemi = t["hemisphere"].astype(str).to_numpy()
    tr_season = t["season"].astype(str).to_numpy()
    tr_shifted = _shifted(tr_days, tr_hemi)

    cache: dict = {}

    def estimate(level: str, crop: str, hemi: str, season: str):
        key = (level, crop, hemi, season)
        if key in cache:
            return cache[key]
        if level == "crop_hemisphere_season":
            sel = (tr_crop == crop) & (tr_hemi == hemi) & (tr_season == season)
            value = _group_estimate(tr_days[sel])
        elif level == "crop_hemisphere":
            sel = (tr_crop == crop) & (tr_hemi == hemi)
            value = _group_estimate(tr_days[sel])
        elif level == "crop_shifted":
            sel = tr_crop == crop
            value = _group_estimate(tr_shifted[sel])
        else:
            value = _group_estimate(tr_shifted)
        cache[key] = value
        return value

    levels = ("crop_hemisphere_season", "crop_hemisphere", "crop_shifted", "all_shifted")
    n = len(test)
    days = np.full(n, np.nan)
    chosen = np.array([""] * n, dtype=object)
    n_group = np.zeros(n, dtype=int)
    concentration = np.full(n, np.nan)

    te_crop = test["crop"].astype(str).to_numpy()
    te_hemi = test["hemisphere"].astype(str).to_numpy()
    te_season = test["season"].astype(str).to_numpy()
    for i in range(n):
        for level in levels:
            median, count, conc = estimate(level, te_crop[i], te_hemi[i], te_season[i])
            trusted = count >= MIN_GROUP_ROWS and np.isfinite(conc) and conc >= MIN_GROUP_CONCENTRATION
            if trusted or (level == levels[-1] and count > 0):
                days[i] = _unshift(median, te_hemi[i]) if level.endswith("_shifted") else median
                chosen[i], n_group[i], concentration[i] = level, count, conc
                break
    return days, chosen, n_group, concentration


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
    df_train["__target__"] = np.asarray(y_train, dtype=float)
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
            model.fit(X_train, np.asarray(y_train, dtype=float).ravel())
        finally:
            sklearn.set_config(transform_output=previous)
    return model


def predict_days_sincos(
    model_name: str,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    sin_train: Sequence[float],
    cos_train: Sequence[float],
    feature_names,
) -> tuple[np.ndarray, np.ndarray]:
    """Predict a day by regressing its sine and cosine separately.

    Returns ``(days, resultant)``; the resultant is ``hypot(sin, cos)`` of the
    prediction and is short when the model is torn between two modes.
    """
    sin_model = _fit_one(model_name, X_train, sin_train, feature_names)
    cos_model = _fit_one(model_name, X_train, cos_train, feature_names)
    sin_pred = np.asarray(sin_model.predict(X_test), dtype=float).ravel()
    cos_pred = np.asarray(cos_model.predict(X_test), dtype=float).ravel()
    days = np.array(
        [features.circle_to_day(s, c) for s, c in zip(sin_pred, cos_pred)], dtype=float
    )
    return days, np.hypot(sin_pred, cos_pred)


def predict_days_anchored(
    model_name: str,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    offset_train: Sequence[float],
    anchor_test: Sequence[float],
    feature_names,
) -> np.ndarray:
    """Predict a day as landmark + regressed signed offset."""
    model = _fit_one(model_name, X_train, offset_train, feature_names)
    offsets = np.asarray(model.predict(X_test), dtype=float).ravel()
    return np.array(
        [features.anchored_to_day(a, o) for a, o in zip(anchor_test, offsets)], dtype=float
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
    consistency: pd.DataFrame = field(default_factory=pd.DataFrame)


def _prediction_block(frame, model, target, scheme, encoding, predicted, observed, **extra) -> pd.DataFrame:
    block = pd.DataFrame(
        {
            "model": model,
            "target": target,
            "scheme": scheme,
            "encoding": encoding,
            "row_id": np.arange(len(frame)),
            "key": frame["key"].to_numpy(),
            "crop": frame["crop"].astype(str).to_numpy(),
            "cm_group": frame["cm_group"].astype(str).to_numpy(),
            "tile": frame["_tile"].to_numpy(),
            "predicted": np.asarray(predicted, dtype=float),
            "observed": np.asarray(observed, dtype=float),
        }
    )
    for name, values in extra.items():
        block[name] = values
    return block


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
    encodings: Sequence[str] = ENCODINGS,
    bootstrap_resamples: int = BOOTSTRAP_RESAMPLES,
    scheme_models: Optional[dict] = None,
) -> Evaluation:
    """Out-of-fold predictions and metrics for every model x target x scheme x encoding.

    Args:
        frame: the design matrix from :func:`geocif.cropcal.features.design_matrix`.
        models: model names for ``auto_train``.
        targets: which transitions to predict.
        schemes: prebuilt CV schemes; built from ``frame`` when omitted.
        baseline_columns: ``{target: column}`` holding the rule-based satellite
            day, scored as the ``rule_based`` model with no folds. Defaults to
            :data:`features.BASELINE_COLUMNS`.
        tolerance: days for the "within tolerance" share.
        encodings: which target encodings to run.
        scheme_models: ``{scheme: [models]}`` -- under that scheme run only
            those models (the climatology null always runs). Lets the 145-fold
            leave-one-country-out scheme run for a cheap model without paying
            for tabpfn/tabicl on it.

    The ``climatology`` null is scored under every scheme for every target.
    Metrics are reported overall and broken out by crop and by ``cm_group``,
    and for two samples: every row, and only the rows the rule-based method
    could score (``rule_scored`` -- a property of the region, so it is the
    same subset for all four targets), so the models and the rule are compared
    on a common footing as well as on the models' larger sample.
    """
    if frame.empty:
        return Evaluation(pd.DataFrame(), pd.DataFrame(), ["empty design matrix"])
    if baseline_columns is None:
        baseline_columns = dict(features.BASELINE_COLUMNS)

    if schemes is None:
        schemes = cv.build_schemes(
            frame, n_splits=n_splits, block_degrees=block_degrees, seed=seed
        )

    frame = frame.reset_index(drop=True).copy()
    frame["_tile"] = cv.spatial_blocks(frame["lat"], frame["lon"], block_degrees)
    X_raw, feature_names = encode(frame)
    for column in baseline_columns.values():
        assert column not in feature_names, f"baseline {column} is in the feature set"

    # "The rule-based method could score this region" is a property of the
    # region, not of the target, so the same subset serves planting and harvest
    # (which have no satellite rule) as the two interior transitions.
    any_baseline = [c for c in baseline_columns.values() if c in frame.columns]
    rule_scored = (
        np.isfinite(frame[any_baseline[0]].to_numpy(dtype=float))
        if any_baseline
        else np.zeros(len(frame), bool)
    )

    wall = frame.get("calendar_wall_to_wall")
    wall = wall.fillna(False).astype(bool).to_numpy() if wall is not None else np.zeros(len(frame), bool)
    anchor_all = frame[features.ANCHOR_FEATURE].to_numpy(dtype=float) if features.ANCHOR_FEATURE in frame else np.full(len(frame), np.nan)

    rows, failures = [], []

    for target in targets:
        column = f"target_{target}"
        if column not in frame.columns:
            failures.append(f"{target}: no target column")
            continue
        observed = frame[column].to_numpy(dtype=float).copy()
        if target in WALL_TO_WALL_MASKED_TARGETS:
            observed[wall] = np.nan
        valid = np.isfinite(observed)
        logger.info(f"{target}: {int(valid.sum())} of {len(frame)} rows carry a target")

        rule_col = baseline_columns.get(target)
        # The rule-based port needs no folds: it does not learn anything.
        if rule_col and rule_col in frame.columns:
            rows.append(
                _prediction_block(
                    frame, BASELINE, target, "none", "none",
                    frame[rule_col].to_numpy(dtype=float), observed,
                    resultant=np.nan, null_level="", rule_scored=rule_scored,
                )
            )

        for scheme_name, scheme in schemes.items():
            # Climatology null, out of fold.
            clim = np.full(len(frame), np.nan)
            level = np.array([""] * len(frame), dtype=object)
            for train_idx, test_idx in scheme.splits:
                train_rows = frame.iloc[train_idx][valid[train_idx]]
                if train_rows.empty:
                    continue
                days, chosen, _n, _c = climatology_predict(train_rows, frame.iloc[test_idx], target)
                clim[test_idx], level[test_idx] = days, chosen
            rows.append(
                _prediction_block(
                    frame, CLIMATOLOGY, target, scheme_name, "none", clim, observed,
                    resultant=np.nan, null_level=level, rule_scored=rule_scored,
                )
            )

            allowed = models if not scheme_models or scheme_name not in scheme_models else [
                m for m in models if m in set(scheme_models[scheme_name])
            ]
            for model_name in allowed:
                for encoding in encodings:
                    prediction = np.full(len(frame), np.nan)
                    resultant = np.full(len(frame), np.nan)
                    try:
                        for train_idx, test_idx in scheme.splits:
                            fit_idx = train_idx[valid[train_idx]]
                            if fit_idx.size == 0:
                                continue
                            X_train, X_test = impute(X_raw.iloc[fit_idx], X_raw.iloc[test_idx])
                            if encoding == "sincos":
                                days, res = predict_days_sincos(
                                    model_name, X_train, X_test,
                                    frame[f"{column}_sin"].iloc[fit_idx],
                                    frame[f"{column}_cos"].iloc[fit_idx],
                                    feature_names,
                                )
                                prediction[test_idx], resultant[test_idx] = days, res
                            elif encoding == "anchored":
                                offsets = frame[f"{column}_anchored"].iloc[fit_idx]
                                ok = np.isfinite(offsets.to_numpy(dtype=float))
                                prediction[test_idx] = predict_days_anchored(
                                    model_name, X_train[ok], X_test,
                                    offsets[ok], anchor_all[test_idx], feature_names,
                                )
                            else:
                                raise ValueError(f"unknown encoding {encoding!r}")
                    except Exception as exc:  # noqa: BLE001 - one model must not sink the run
                        message = f"{model_name}/{target}/{scheme_name}/{encoding}: {exc}"
                        logger.warning(f"model failed, skipping -- {message}")
                        failures.append(message)
                        continue

                    rows.append(
                        _prediction_block(
                            frame, model_name, target, scheme_name, encoding, prediction, observed,
                            resultant=resultant, null_level="", rule_scored=rule_scored,
                        )
                    )

    if not rows:
        return Evaluation(pd.DataFrame(), pd.DataFrame(), failures or ["no model produced predictions"])

    predictions = pd.concat(rows, ignore_index=True)
    metrics = summarise_predictions(
        predictions, tolerance=tolerance, seed=seed, bootstrap_resamples=bootstrap_resamples
    )
    consistency = summarise_consistency(predictions, frame)
    return Evaluation(predictions, metrics, failures, consistency)


# --------------------------------------------------------------------------
# Metric tables
# --------------------------------------------------------------------------
def _reference_scheme(scheme: str, available: Sequence[str]) -> Optional[str]:
    """Which climatology scheme a model's cell is compared against."""
    if scheme in available:
        return scheme
    for preferred in ("spatial_block", "country_block", "country"):
        if preferred in available:
            return preferred
    return available[0] if len(available) else None


def _paired_skill(
    model_part: pd.DataFrame, clim_part: pd.DataFrame, *, seed: int, resamples: int
) -> dict:
    """``1 - MAE_model / MAE_climatology`` on common rows, with a tile bootstrap.

    The bootstrap resamples spatial tiles (not rows) with replacement, so the
    interval respects the clustering that makes neighbouring regions
    non-independent. Both MAEs are recomputed on each resample from the same
    tiles, so the interval is for the PAIRED difference.
    """
    # Pair on the design-matrix row, never on ``key``: the calendar-region key
    # repeats once per crop sheet and per season, and an inner merge on it is a
    # cartesian product that pairs a maize prediction with a wheat null.
    merged = model_part[["row_id", "tile", "predicted", "observed"]].merge(
        clim_part[["row_id", "predicted"]].rename(columns={"predicted": "clim"}), on="row_id", how="inner"
    )
    merged = merged[np.isfinite(merged["predicted"]) & np.isfinite(merged["clim"]) & np.isfinite(merged["observed"])]
    out = {"skill_vs_climatology": np.nan, "skill_ci_low": np.nan, "skill_ci_high": np.nan, "n_skill": int(len(merged))}
    if merged.empty:
        return out
    gap_m = np.array([circular.circular_gap(p, o) for p, o in zip(merged["predicted"], merged["observed"])])
    gap_c = np.array([circular.circular_gap(p, o) for p, o in zip(merged["clim"], merged["observed"])])
    mae_c = gap_c.mean()
    if mae_c <= 0:
        return out
    out["skill_vs_climatology"] = float(1.0 - gap_m.mean() / mae_c)

    tiles, tile_id = np.unique(merged["tile"].to_numpy(), return_inverse=True)
    n_tiles = tiles.size
    if n_tiles < 2 or resamples <= 0:
        return out
    sum_m = np.bincount(tile_id, weights=gap_m, minlength=n_tiles)
    sum_c = np.bincount(tile_id, weights=gap_c, minlength=n_tiles)
    count = np.bincount(tile_id, minlength=n_tiles).astype(float)
    rng = np.random.default_rng(seed)
    weights = rng.multinomial(n_tiles, np.full(n_tiles, 1.0 / n_tiles), size=resamples).astype(float)
    with np.errstate(all="ignore"):
        boot_m = (weights @ sum_m) / (weights @ count)
        boot_c = (weights @ sum_c) / (weights @ count)
        skills = 1.0 - boot_m / boot_c
    skills = skills[np.isfinite(skills)]
    if skills.size:
        alpha = (1.0 - BOOTSTRAP_LEVEL) / 2.0
        out["skill_ci_low"] = float(np.quantile(skills, alpha))
        out["skill_ci_high"] = float(np.quantile(skills, 1.0 - alpha))
    return out


def summarise_predictions(
    predictions: pd.DataFrame,
    *,
    tolerance: int = TOLERANCE_DAYS,
    seed: int = 0,
    bootstrap_resamples: int = BOOTSTRAP_RESAMPLES,
) -> pd.DataFrame:
    """Metric table: overall, by crop and by CM group; all rows and rule-scored rows.

    Every cell also carries ``skill_vs_climatology`` -- ``1 - MAE / MAE_null``
    on the rows both have -- with a paired tile-bootstrap interval, and the
    name of the climatology scheme used as the reference. For ``rule_based``
    (which has no scheme) the reference is the spatial-block climatology when
    present. A cell whose interval excludes zero is a real difference from the
    null; the calendar's half-month bins put the resolution floor of the truth
    itself at roughly 7-8 days, so differences below that are not real either.
    """
    records = []
    keys = ["model", "target", "scheme", "encoding"]
    clim = predictions[predictions["model"] == CLIMATOLOGY]

    def _cells(sample_name: str, sub: pd.DataFrame, split: str, label) -> None:
        clim_sub = clim[clim.index.isin(sub.index)]
        for values, part in sub.groupby(keys, dropna=False, observed=True):
            record = dict(zip(keys, values))
            record.update({"split": split, "split_value": label, "sample": sample_name})
            record.update(circular_metrics(part["predicted"], part["observed"], tolerance, part.get("resultant")))
            if record["model"] != CLIMATOLOGY:
                target_clim = clim_sub[clim_sub["target"] == record["target"]]
                reference = _reference_scheme(record["scheme"], list(target_clim["scheme"].unique()))
                record["skill_reference"] = reference or ""
                ref_part = target_clim[target_clim["scheme"] == reference] if reference else target_clim.iloc[0:0]
                record.update(_paired_skill(part, ref_part, seed=seed, resamples=bootstrap_resamples))
            else:
                record.update({"skill_reference": "", "skill_vs_climatology": np.nan,
                               "skill_ci_low": np.nan, "skill_ci_high": np.nan, "n_skill": np.nan})
            records.append(record)

    samples = {"all": predictions}
    if "rule_scored" in predictions.columns:
        samples["rule_scored"] = predictions[predictions["rule_scored"].astype(bool)]
    for sample_name, sample in samples.items():
        _cells(sample_name, sample, "overall", "all")
        for crop, part in sample.groupby("crop", dropna=False, observed=True):
            _cells(sample_name, part, "crop", str(crop))
        for group, part in sample.groupby("cm_group", dropna=False, observed=True):
            _cells(sample_name, part, "cm_group", str(group))

    out = pd.DataFrame(records)
    return out.sort_values(["target", "sample", "split", "split_value", "mae_days"]).reset_index(drop=True)


# --------------------------------------------------------------------------
# Cross-target consistency
# --------------------------------------------------------------------------
def season_consistency(planting, midgreenup, midgreendown, harvest) -> tuple[np.ndarray, np.ndarray]:
    """``(los_days, ordered)`` for four predicted days, per row.

    ``los_days`` is harvest minus planting the forward way round the year.
    ``ordered`` is True when, walking forward from planting, mid-greenup comes
    before mid-greendown comes before harvest -- the season order the calendar
    guarantees by construction and that four independent regressions do not.
    """
    p, up, down, h = (np.asarray(list(v), dtype=float) for v in (planting, midgreenup, midgreendown, harvest))
    period = circular.DAYS_IN_YEAR
    los = (h - p) % period
    a, b = (up - p) % period, (down - p) % period
    finite = np.isfinite(p) & np.isfinite(up) & np.isfinite(down) & np.isfinite(h)
    ordered = finite & (a < b) & (b < los)
    los = np.where(finite, los, np.nan)
    return los, ordered


def summarise_consistency(predictions: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    """One row per (model, scheme, encoding): season order and length of the
    four predicted days, with the calendar itself as the reference row.

    Franch et al. (2022) mask predicted seasons shorter than 30 or longer than
    280 days as implausible; here that share is a metric, because a model that
    predicts each transition well in isolation can still place them out of
    order or a week apart.
    """
    needed = set(features.TARGETS)
    records = []

    def _record(label, scheme, encoding, days: dict) -> None:
        if not needed <= set(days):
            return
        los, ordered = season_consistency(*(days[t] for t in features.TARGETS))
        finite = np.isfinite(los)
        if not finite.any():
            return
        lo, hi = LOS_PLAUSIBLE_DAYS
        records.append({
            "model": label, "scheme": scheme, "encoding": encoding,
            "n": int(finite.sum()),
            "median_los_days": float(np.nanmedian(los)),
            "pct_los_plausible": float(100.0 * np.mean((los[finite] >= lo) & (los[finite] <= hi))),
            "pct_ordered": float(100.0 * ordered[finite].mean()),
        })

    # The calendar's own four days, as the reference.
    calendar_days = {t: frame[f"target_{t}"].to_numpy(dtype=float) for t in features.TARGETS if f"target_{t}" in frame}
    _record("calendar", "none", "none", calendar_days)

    for (model, scheme, encoding), part in predictions.groupby(["model", "scheme", "encoding"], observed=True):
        wide = part.pivot_table(index="row_id", columns="target", values="predicted", aggfunc="first")
        _record(model, scheme, encoding, {t: wide[t].to_numpy(dtype=float) for t in wide.columns})

    return pd.DataFrame(records)
