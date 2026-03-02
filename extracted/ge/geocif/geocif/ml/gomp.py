"""
gomp.py — Generalised Orthogonal Matching Pursuit (gOMP) for feature selection.

Based on:
    Tsagris, M., Papadovasilakis, Z., Lakiotaki, K. & Tsamardinos, I. (2020).
    "A generalised OMP algorithm for feature selection with application to
    gene expression data." arXiv:2004.00281v1.

Implements Algorithm 2 from the paper with support for:
  - Continuous outcomes  (linear regression, raw residuals)
  - Binary outcomes      (logistic regression, raw residuals)
  - Time-to-event        (Cox PH via lifelines, martingale residuals)
  - Mixed feature types  (continuous + categorical via p-value unification)
  - Multiple stopping criteria (BIC, adjusted-R², likelihood-ratio / chi²)

Designed to drop in alongside scikit-learn workflows.
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from scipy import stats as sp_stats

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums for configuration
# ---------------------------------------------------------------------------

class OutcomeType(Enum):
    CONTINUOUS = auto()
    BINARY = auto()
    SURVIVAL = auto()


class StoppingCriterion(Enum):
    """Which criterion controls when to stop adding features."""
    BIC = auto()           # stop when BIC does not improve by >= bic_delta
    ADJUSTED_R2 = auto()   # stop when adj-R² improvement < threshold
    LRT_CHISQ = auto()     # stop when LRT p-value > alpha (chi² test)
    MAX_FEATURES = auto()  # stop after k features


class AssociationType(Enum):
    """How to measure residual–feature association."""
    PEARSON = auto()
    SPEARMAN = auto()
    AUTO = auto()  # Pearson for continuous, ANOVA F-test for categorical


# ---------------------------------------------------------------------------
# Helper: safe log-p computation
# ---------------------------------------------------------------------------

def _safe_log_pvalue(pvalue: float) -> float:
    """Return log10(p) handling p==0 by clamping to machine epsilon."""
    if pvalue <= 0:
        return -300.0  # ~log10(5e-324)
    return np.log10(pvalue)


# ---------------------------------------------------------------------------
# Association functions  (return -log10 p-value, higher = stronger)
# ---------------------------------------------------------------------------

def _pearson_neg_log_p(residuals: np.ndarray, feature: np.ndarray) -> float:
    """Pearson correlation test → -log10(p)."""
    mask = np.isfinite(residuals) & np.isfinite(feature)
    if mask.sum() < 4 or np.std(feature[mask]) < 1e-12:
        return 0.0
    _, pval = sp_stats.pearsonr(residuals[mask], feature[mask])
    return -_safe_log_pvalue(pval)


def _spearman_neg_log_p(residuals: np.ndarray, feature: np.ndarray) -> float:
    """Spearman rank correlation test → -log10(p)."""
    mask = np.isfinite(residuals) & np.isfinite(feature)
    if mask.sum() < 4:
        return 0.0
    _, pval = sp_stats.spearmanr(residuals[mask], feature[mask])
    return -_safe_log_pvalue(pval)


def _anova_neg_log_p(residuals: np.ndarray, feature: np.ndarray) -> float:
    """One-way ANOVA F-test for a categorical feature → -log10(p)."""
    groups = {}
    for val, res in zip(feature, residuals):
        if np.isfinite(res):
            groups.setdefault(val, []).append(res)
    group_arrays = [np.array(v) for v in groups.values() if len(v) >= 2]
    if len(group_arrays) < 2:
        return 0.0
    _, pval = sp_stats.f_oneway(*group_arrays)
    return -_safe_log_pvalue(pval)


# ---------------------------------------------------------------------------
# Model wrappers  (fit, predict, residuals, log-likelihood, df)
# ---------------------------------------------------------------------------

class _LinearModel:
    """OLS wrapper that exposes residuals, log-likelihood, and df."""

    def __init__(self):
        self.coef_ = None
        self.intercept_ = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray):
        if X.shape[1] == 0:
            self.coef_ = np.array([])
            self.intercept_ = np.mean(y)
            return self
        X_b = np.column_stack([np.ones(len(X)), X])
        beta, *_ = np.linalg.lstsq(X_b, y, rcond=None)
        self.intercept_ = beta[0]
        self.coef_ = beta[1:]
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if X.shape[1] == 0:
            return np.full(len(X), self.intercept_)
        return X @ self.coef_ + self.intercept_

    def residuals(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        return y - self.predict(X)

    def log_likelihood(self, X: np.ndarray, y: np.ndarray) -> float:
        resid = self.residuals(X, y)
        n = len(y)
        sigma2 = np.sum(resid ** 2) / n
        if sigma2 < 1e-30:
            sigma2 = 1e-30
        return -0.5 * n * (np.log(2 * np.pi * sigma2) + 1)

    def df(self, X: np.ndarray) -> int:
        """Degrees of freedom = number of estimated parameters."""
        return X.shape[1] + 2  # betas + intercept + sigma²


class _LogisticModel:
    """Simple logistic regression via sklearn (thin wrapper)."""

    def __init__(self):
        from sklearn.linear_model import LogisticRegression
        self._model = LogisticRegression(
            solver="lbfgs", max_iter=2000, penalty=None
        )
        self._intercept_only = False

    def fit(self, X: np.ndarray, y: np.ndarray):
        if X.shape[1] == 0:
            self._intercept_only = True
            self._p_mean = np.mean(y)
            return self
        self._intercept_only = False
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._model.fit(X, y)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self._intercept_only:
            return np.full(len(X), self._p_mean)
        return self._model.predict_proba(X)[:, 1]

    def residuals(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Raw residuals: y - p̂  (as in Lozano et al. 2011)."""
        return y - self.predict_proba(X)

    def log_likelihood(self, X: np.ndarray, y: np.ndarray) -> float:
        p = np.clip(self.predict_proba(X), 1e-15, 1 - 1e-15)
        return np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))

    def df(self, X: np.ndarray) -> int:
        return X.shape[1] + 1  # betas + intercept


class _CoxModel:
    """Cox PH wrapper using lifelines."""

    def __init__(self):
        self._fitted = None
        self._baseline = 0.0

    def fit(self, X: np.ndarray, y_time: np.ndarray, y_event: np.ndarray):
        try:
            from lifelines import CoxPHFitter
        except ImportError:
            raise ImportError(
                "lifelines is required for survival outcomes: "
                "pip install lifelines"
            )

        df = pd.DataFrame(X, columns=[f"x{i}" for i in range(X.shape[1])])
        df["T"] = y_time
        df["E"] = y_event

        if X.shape[1] == 0:
            self._fitted = None
            self._baseline = 0.0
            return self

        cph = CoxPHFitter(penalizer=0.01)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cph.fit(df, duration_col="T", event_col="E")
        self._fitted = cph
        return self

    def residuals(
        self, X: np.ndarray, y_time: np.ndarray, y_event: np.ndarray
    ) -> np.ndarray:
        """Martingale residuals: E_i - H_0(t_i)*exp(X_i @ beta)."""
        if self._fitted is None:
            # intercept-only: approximate martingale residuals
            n = len(y_time)
            order = np.argsort(y_time)
            baseline_cum_hazard = np.zeros(n)
            for i, idx in enumerate(order):
                at_risk = n - i
                baseline_cum_hazard[i] = 1.0 / at_risk if at_risk > 0 else 0
            cum_haz = np.cumsum(baseline_cum_hazard)
            H0 = np.zeros(n)
            for rank, idx in enumerate(order):
                H0[idx] = cum_haz[rank]
            return y_event - H0

        df = pd.DataFrame(X, columns=[f"x{i}" for i in range(X.shape[1])])
        df["T"] = y_time
        df["E"] = y_event
        resid_df = self._fitted.compute_residuals(df, kind="martingale")
        return resid_df["martingale"].values

    def log_likelihood(
        self, X: np.ndarray, y_time: np.ndarray, y_event: np.ndarray
    ) -> float:
        if self._fitted is None:
            return 0.0
        return self._fitted.log_likelihood_

    def df(self, X: np.ndarray) -> int:
        return X.shape[1]


# ---------------------------------------------------------------------------
# BIC / adjusted-R² helpers
# ---------------------------------------------------------------------------

def _bic(log_lik: float, k: int, n: int) -> float:
    """Bayesian Information Criterion: -2*LL + k*ln(n)."""
    return -2 * log_lik + k * np.log(n)


def _adjusted_r2(y: np.ndarray, residuals: np.ndarray, p: int) -> float:
    """Adjusted R² for p predictors."""
    n = len(y)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    if ss_tot < 1e-30 or n <= p + 1:
        return 0.0
    r2 = 1 - ss_res / ss_tot
    return 1 - (1 - r2) * (n - 1) / (n - p - 1)


# ---------------------------------------------------------------------------
# Main gOMP class
# ---------------------------------------------------------------------------

@dataclass
class GOMP:
    """
    Generalised Orthogonal Matching Pursuit feature selector.

    Parameters
    ----------
    outcome_type : OutcomeType
        CONTINUOUS, BINARY, or SURVIVAL.
    stopping : StoppingCriterion
        When to stop adding features.
    association : AssociationType
        How to score residual–feature pairs.  AUTO picks Pearson for
        continuous features and ANOVA for categoricals.
    max_features : int
        Hard cap on selected features (also the stop for MAX_FEATURES).
    alpha : float
        Significance threshold for LRT_CHISQ stopping (default 0.01).
    bic_delta : float
        Minimum BIC improvement to keep adding features (default 2.0).
    adj_r2_delta : float
        Minimum adjusted-R² improvement for ADJUSTED_R2 stopping.
    categorical_cols : list[str] | None
        Column names that are categorical (p-value via ANOVA).
    verbose : bool
        Whether to log progress.

    Attributes (after fit)
    ----------------------
    selected_features_ : list[str]
        Names of selected features in order of selection.
    selected_indices_ : list[int]
        Column indices of selected features.
    n_features_ : int
        Number of selected features.
    """

    outcome_type: OutcomeType = OutcomeType.CONTINUOUS
    stopping: StoppingCriterion = StoppingCriterion.BIC
    association: AssociationType = AssociationType.AUTO
    max_features: int = 30
    alpha: float = 0.01
    bic_delta: float = 2.0
    adj_r2_delta: float = 0.005
    categorical_cols: Optional[List[str]] = None
    verbose: bool = False

    # --- fitted state ---
    selected_features_: List[str] = field(
        default_factory=list, init=False, repr=False
    )
    selected_indices_: List[int] = field(
        default_factory=list, init=False, repr=False
    )
    n_features_: int = field(default=0, init=False, repr=False)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fit(
        self,
        X: pd.DataFrame,
        y: Union[np.ndarray, pd.Series],
        y_event: Optional[np.ndarray] = None,
    ) -> "GOMP":
        """
        Run gOMP feature selection.

        Parameters
        ----------
        X : DataFrame  (n_samples × p_features)
        y : array-like
            For CONTINUOUS / BINARY: the outcome vector.
            For SURVIVAL: the time-to-event vector.
        y_event : array-like or None
            For SURVIVAL: event indicator (1=event, 0=censored).

        Returns
        -------
        self
        """
        X_arr, feature_names, cat_mask = self._prepare_X(X)
        y_arr = np.asarray(y, dtype=float)
        n, p = X_arr.shape

        if self.outcome_type == OutcomeType.SURVIVAL and y_event is None:
            raise ValueError(
                "y_event is required for SURVIVAL outcome_type"
            )

        y_ev = (
            np.asarray(y_event, dtype=float) if y_event is not None else None
        )

        # --- initialise model and residuals (intercept-only) ---
        model, residuals, prev_ll = self._init_model(X_arr, y_arr, y_ev, n)

        selected: List[int] = []
        remaining = set(range(p))
        prev_bic = _bic(
            prev_ll,
            model.df(np.empty((n, 0))),
            n,
        )
        prev_adj_r2 = 0.0

        for step in range(min(self.max_features, p)):
            if not remaining:
                break

            # --- find best candidate ---
            best_idx, best_score = self._best_candidate(
                residuals, X_arr, remaining, cat_mask
            )
            if best_idx is None:
                break

            # tentatively add
            candidate_set = selected + [best_idx]
            cand_model, cand_resid, cand_ll = self._fit_model(
                X_arr[:, candidate_set], y_arr, y_ev
            )

            # --- check stopping criterion ---
            stop = self._check_stop(
                n=n,
                prev_ll=prev_ll,
                cand_ll=cand_ll,
                prev_bic=prev_bic,
                cand_model=cand_model,
                cand_set=candidate_set,
                X_arr=X_arr,
                y_arr=y_arr,
                cand_resid=cand_resid,
                prev_adj_r2=prev_adj_r2,
                step=step,
            )

            if stop:
                if self.verbose:
                    logger.info(
                        f"gOMP stopping at step {step}: criterion met"
                    )
                break

            # accept
            selected.append(best_idx)
            remaining.discard(best_idx)
            residuals = cand_resid
            prev_ll = cand_ll
            prev_bic = _bic(
                cand_ll, cand_model.df(X_arr[:, selected]), n
            )
            if self.outcome_type == OutcomeType.CONTINUOUS:
                prev_adj_r2 = _adjusted_r2(
                    y_arr, cand_resid, len(selected)
                )

            if self.verbose:
                logger.info(
                    f"  step {step}: selected '{feature_names[best_idx]}' "
                    f"(score={best_score:.2f})"
                )

        self.selected_indices_ = selected
        self.selected_features_ = [feature_names[i] for i in selected]
        self.n_features_ = len(selected)

        if self.verbose:
            logger.info(
                f"gOMP selected {self.n_features_} features: "
                f"{self.selected_features_}"
            )

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Return X with only the selected features."""
        return X[self.selected_features_]

    def fit_transform(
        self,
        X: pd.DataFrame,
        y: Union[np.ndarray, pd.Series],
        y_event: Optional[np.ndarray] = None,
    ) -> pd.DataFrame:
        self.fit(X, y, y_event=y_event)
        return self.transform(X)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _prepare_X(
        self, X: pd.DataFrame
    ) -> Tuple[np.ndarray, List[str], np.ndarray]:
        """Convert DataFrame → numpy and identify categorical columns."""
        feature_names = list(X.columns)
        cat_cols = set(self.categorical_cols or [])
        cat_mask = np.array(
            [c in cat_cols for c in feature_names], dtype=bool
        )

        # encode categoricals as integer codes for ANOVA
        X_arr = np.empty((len(X), len(feature_names)), dtype=float)
        for j, col in enumerate(feature_names):
            if cat_mask[j]:
                X_arr[:, j] = pd.Categorical(X[col]).codes.astype(float)
            else:
                X_arr[:, j] = X[col].values.astype(float)

        return X_arr, feature_names, cat_mask

    def _init_model(self, X_arr, y_arr, y_ev, n):
        """Fit the intercept-only model and return (model, resid, ll)."""
        empty = np.empty((n, 0))
        return self._fit_model(empty, y_arr, y_ev)

    def _fit_model(self, X_sel, y_arr, y_ev):
        """Fit model on selected columns → (model, residuals, log_lik)."""
        if self.outcome_type == OutcomeType.CONTINUOUS:
            m = _LinearModel().fit(X_sel, y_arr)
            return (
                m,
                m.residuals(X_sel, y_arr),
                m.log_likelihood(X_sel, y_arr),
            )

        elif self.outcome_type == OutcomeType.BINARY:
            m = _LogisticModel().fit(X_sel, y_arr)
            return (
                m,
                m.residuals(X_sel, y_arr),
                m.log_likelihood(X_sel, y_arr),
            )

        elif self.outcome_type == OutcomeType.SURVIVAL:
            m = _CoxModel()
            m.fit(X_sel, y_arr, y_ev)
            return (
                m,
                m.residuals(X_sel, y_arr, y_ev),
                m.log_likelihood(X_sel, y_arr, y_ev),
            )

        raise ValueError(f"Unknown outcome_type: {self.outcome_type}")

    def _best_candidate(
        self,
        residuals: np.ndarray,
        X_arr: np.ndarray,
        remaining: set,
        cat_mask: np.ndarray,
    ) -> Tuple[Optional[int], float]:
        """Find the feature most associated with current residuals."""
        if not remaining:
            return None, -np.inf

        remaining_list = sorted(remaining)

        # Fast vectorised path: all-continuous + Pearson/AUTO
        has_cats = cat_mask[remaining_list].any()
        use_fast = (
            not has_cats
            and self.association in (AssociationType.PEARSON, AssociationType.AUTO)
        )

        if use_fast:
            X_sub = X_arr[:, remaining_list]  # (n, k)
            r = residuals
            mask = np.isfinite(r)
            r_m = r[mask]
            X_m = X_sub[mask]

            n = len(r_m)
            if n < 4:
                return None, -np.inf

            # vectorised Pearson r and t-test p-value
            r_mean = r_m.mean()
            r_std = r_m.std(ddof=0)
            if r_std < 1e-12:
                return None, -np.inf

            X_mean = X_m.mean(axis=0)
            X_std = X_m.std(axis=0, ddof=0)
            X_std[X_std < 1e-12] = np.inf  # zero-variance → zero corr

            corr = ((X_m - X_mean) * (r_m - r_mean)[:, None]).mean(axis=0) / (X_std * r_std)
            corr = np.clip(corr, -1 + 1e-10, 1 - 1e-10)

            # t-statistic → p-value
            t_stat = corr * np.sqrt((n - 2) / (1 - corr**2))
            log_pvals = sp_stats.t.logsf(np.abs(t_stat), df=n - 2) + np.log(2)
            neg_log_p = -log_pvals / np.log(10)  # convert ln→log10

            best_local = int(np.argmax(neg_log_p))
            return remaining_list[best_local], neg_log_p[best_local]

        # Slow per-feature path (mixed types or Spearman)
        best_idx = None
        best_score = -np.inf

        for j in remaining:
            if cat_mask[j]:
                score = _anova_neg_log_p(residuals, X_arr[:, j])
            elif self.association == AssociationType.SPEARMAN:
                score = _spearman_neg_log_p(residuals, X_arr[:, j])
            else:
                score = _pearson_neg_log_p(residuals, X_arr[:, j])

            if score > best_score:
                best_score = score
                best_idx = j

        return best_idx, best_score

    def _check_stop(
        self,
        *,
        n,
        prev_ll,
        cand_ll,
        prev_bic,
        cand_model,
        cand_set,
        X_arr,
        y_arr,
        cand_resid,
        prev_adj_r2,
        step,
    ) -> bool:
        """Evaluate whether to stop before accepting the candidate."""

        if self.stopping == StoppingCriterion.MAX_FEATURES:
            return step >= self.max_features

        elif self.stopping == StoppingCriterion.BIC:
            cand_bic = _bic(
                cand_ll, cand_model.df(X_arr[:, cand_set]), n
            )
            return (prev_bic - cand_bic) < self.bic_delta

        elif self.stopping == StoppingCriterion.ADJUSTED_R2:
            if self.outcome_type != OutcomeType.CONTINUOUS:
                # fall back to BIC for non-continuous
                cand_bic = _bic(
                    cand_ll, cand_model.df(X_arr[:, cand_set]), n
                )
                return (prev_bic - cand_bic) < self.bic_delta
            cand_adj_r2 = _adjusted_r2(
                y_arr, cand_resid, len(cand_set)
            )
            return (cand_adj_r2 - prev_adj_r2) < self.adj_r2_delta

        elif self.stopping == StoppingCriterion.LRT_CHISQ:
            # Likelihood ratio test: -2*(LL_prev - LL_cand) ~ chi²(1)
            lr_stat = -2 * (prev_ll - cand_ll)
            if lr_stat < 0:
                lr_stat = 0.0
            pval = sp_stats.chi2.sf(lr_stat, df=1)
            return pval > self.alpha

        return False


# ---------------------------------------------------------------------------
# Convenience function (sklearn-style)
# ---------------------------------------------------------------------------

def gomp_select(
    X: pd.DataFrame,
    y: Union[np.ndarray, pd.Series],
    *,
    outcome: str = "continuous",
    stopping: str = "bic",
    association: str = "auto",
    max_features: int = 30,
    alpha: float = 0.01,
    bic_delta: float = 2.0,
    adj_r2_delta: float = 0.005,
    categorical_cols: Optional[List[str]] = None,
    verbose: bool = False,
    y_event: Optional[np.ndarray] = None,
) -> Tuple[GOMP, pd.DataFrame, List[str]]:
    """
    Convenience wrapper matching the (selector, X_sel, features) return
    signature used in feature_selection.py.

    Parameters
    ----------
    X : pd.DataFrame
    y : array-like
    outcome : str  {"continuous", "binary", "survival"}
    stopping : str {"bic", "adjusted_r2", "lrt", "max_features"}
    association : str {"pearson", "spearman", "auto"}
    max_features : int
    alpha, bic_delta, adj_r2_delta : float  (stopping thresholds)
    categorical_cols : list[str] | None
    verbose : bool
    y_event : array-like | None  (for survival)

    Returns
    -------
    selector : fitted GOMP object
    X_selected : pd.DataFrame with selected columns
    selected_features : list[str]
    """
    outcome_map = {
        "continuous": OutcomeType.CONTINUOUS,
        "binary": OutcomeType.BINARY,
        "survival": OutcomeType.SURVIVAL,
    }
    stop_map = {
        "bic": StoppingCriterion.BIC,
        "adjusted_r2": StoppingCriterion.ADJUSTED_R2,
        "lrt": StoppingCriterion.LRT_CHISQ,
        "max_features": StoppingCriterion.MAX_FEATURES,
    }
    assoc_map = {
        "pearson": AssociationType.PEARSON,
        "spearman": AssociationType.SPEARMAN,
        "auto": AssociationType.AUTO,
    }

    selector = GOMP(
        outcome_type=outcome_map[outcome],
        stopping=stop_map[stopping],
        association=assoc_map[association],
        max_features=max_features,
        alpha=alpha,
        bic_delta=bic_delta,
        adj_r2_delta=adj_r2_delta,
        categorical_cols=categorical_cols,
        verbose=verbose,
    )

    selector.fit(X, y, y_event=y_event)
    X_sel = selector.transform(X)

    return selector, X_sel, selector.selected_features_