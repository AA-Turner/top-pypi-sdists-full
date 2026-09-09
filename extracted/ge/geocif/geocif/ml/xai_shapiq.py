"""shapiq-based XAI for TabPFN-family models.

Maps the 4 explanation questions from the user's spec to the shapiq API:

| Question | Function |
|---|---|
| Why did the model predict this for this sample? | ``explain_local`` (per-sample SHAP via ``shapiq.TabPFNExplainer``) |
| Which feature pairs interact most? | ``explain_interactions`` (k-SII at order=2) |
| How does feature X affect predictions globally? | ``explain_pdp`` (partial dependence) |
| SHAP values compatible with other models | ``explain_shap_compat`` (``shapiq.TabPFNImputationExplainer`` → SHAP-compatible values) |

All four functions return numpy arrays / pandas frames + side-effect
plot files into the supplied output dir. They no-op (returning ``None``)
when shapiq is not installed, so the parent xai.explain caller can
fall back to plain SHAP without exception handling.

Dispatch from xai.explain: any tabpfn-family model (tabpfn, tabpfn_ft,
curated_tabpfn, top10_tabpfn, auto_tabpfn) routes here when
``xai_tabpfn_method = shapiq`` (default).
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def _shapiq_available() -> bool:
    """Whether shapiq can be imported (some envs may lack it)."""
    try:
        import shapiq  # noqa: F401
        return True
    except ImportError:
        return False


def _sanitize(name: str) -> str:
    """Sanitize a string for use in a filename."""
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in str(name))


def _as_scalar(x) -> float:
    """float() for values that may arrive as size-1 arrays.

    NumPy >= 2.3 removed the implicit size-1-array -> scalar coercion, so
    ``float(np.array([1.5]))`` raises TypeError. Every scalar extraction in
    this module goes through here instead.
    """
    arr = np.asarray(x, dtype=float).reshape(-1)
    if arr.size != 1:
        raise ValueError(f"expected a scalar-like value, got size {arr.size}")
    return float(arr[0])


def _numpy_dropped_size1_coercion() -> bool:
    """True when float(size-1 ndarray) raises (NumPy >= 2.3 behavior)."""
    import warnings

    with warnings.catch_warnings():
        # older NumPy emits a DeprecationWarning for the same coercion;
        # silence it -- the probe only cares whether it raises
        warnings.simplefilter("ignore", DeprecationWarning)
        try:
            float(np.ones(1))
            return False
        except TypeError:
            return True


def _ensure_shapiq_numpy2_compat() -> None:
    """Patch shapiq's TabPFNImputer for NumPy >= 2.3.

    ``shapiq.imputer.tabpfn_imputer.TabPFNImputer.value_function`` (<= 1.4.x)
    ends each coalition with ``float(self.predict(...))`` on a length-1
    array. Under NumPy >= 2.3 that raises ``TypeError: only 0-dimensional
    arrays can be converted to Python scalars`` for EVERY coalition, so every
    ``explain()`` call fails, the per-sample except blocks swallow it, and
    the SHAP matrix silently stays all-zeros — the run "succeeds" with empty
    explanations (observed 2026-09-08: 636 failures, beeswarm of zeros).

    shapiq >= 1.5 fixes this but requires Python >= 3.12; the cluster env is
    3.11, so patch in place. No-op when the coercion works (older NumPy) or
    shapiq is absent; idempotent via a marker attribute.
    """
    if not _numpy_dropped_size1_coercion():
        return  # NumPy still coerces size-1 arrays; stock shapiq is fine
    try:
        from shapiq.imputer import tabpfn_imputer as _ti
    except ImportError:
        return
    if getattr(_ti.TabPFNImputer.value_function, "_np2_patched", False):
        return

    def value_function(self, coalitions):
        """Re-implementation of TabPFNImputer.value_function (shapiq 1.4.1)
        with the scalar extraction made NumPy-2-safe. Mirrors the original
        remove-and-contextualize loop exactly, including the final refit."""
        output = np.zeros(len(coalitions), dtype=float)
        for i, coalition in enumerate(coalitions):
            if np.sum(coalition) == 0:
                output[i] = _as_scalar(self.empty_prediction)
                continue
            x_train_coal = self.x_train[:, coalition]
            x_explain_coal = self.x[:, coalition]
            try:
                self.model.fit(x_train_coal, self.y_train)
                output[i] = _as_scalar(self.predict(x_explain_coal))
            except Exception as exc:  # noqa: BLE001
                # TabPFN refuses to fit when the sampled coalition selects
                # only constant features ("All features are constant and
                # would have been removed!"). Such a coalition carries no
                # information, which is precisely what empty_prediction
                # represents -- fall back to it instead of letting one
                # degenerate coalition abort the whole sample's explain()
                # (observed 2026-09-08: 47/240 samples lost this way).
                if "constant" not in str(exc).lower():
                    raise
                output[i] = _as_scalar(self.empty_prediction)
        # refit on the full training data so the model leaves in a
        # consistent state (same contract as the original)
        self.model.fit(self.x_train, self.y_train)
        return output

    value_function._np2_patched = True
    _ti.TabPFNImputer.value_function = value_function
    logger.info(
        "shapiq TabPFNImputer.value_function patched for NumPy>=2.3 "
        "(size-1 array scalar coercion removed upstream)"
    )


# ---------------------------------------------------------------------------
# Q1: Why did the model predict this for this sample?
# ---------------------------------------------------------------------------

def explain_local(
    model,
    X_background: pd.DataFrame,
    y_background: pd.Series | np.ndarray,
    X_test: pd.DataFrame,
    feature_names: list[str],
    out_dir: Path,
    region_name: str,
    forecast_season,
    *,
    max_evals: int = 256,
):
    """Per-sample local explanation using ``shapiq.TabPFNExplainer``.

    Renders one waterfall PNG per row in ``X_test`` showing each
    feature's contribution to that prediction. Returns the (n_test,
    n_features) array of SHAP values for downstream DB storage.

    No-op (returns None) when shapiq is unavailable.
    """
    if not _shapiq_available():
        logger.debug("shapiq not installed; skipping local TabPFN explainer")
        return None
    import shapiq

    _ensure_shapiq_numpy2_compat()

    try:
        explainer = shapiq.TabPFNExplainer(
            model=model,
            data=X_background.to_numpy(),
            labels=np.asarray(y_background),
            index="SV",          # standard Shapley values for "local" Q
            max_order=1,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"shapiq.TabPFNExplainer (SV) init failed: {exc}")
        return None

    out_dir.mkdir(parents=True, exist_ok=True)
    n_test = len(X_test)
    shap_array = np.zeros((n_test, len(feature_names)), dtype=float)

    for i, (_, row) in enumerate(X_test.iterrows()):
        try:
            iv = explainer.explain(row.to_numpy(), budget=max_evals)
            sv = np.asarray(iv.get_n_order_values(1)).reshape(-1)
            shap_array[i, :len(sv)] = sv
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"  shapiq local explain failed for sample {i}: {exc}")
            continue
        _render_waterfall(
            sv=shap_array[i],
            feature_names=feature_names,
            feature_values=row.to_numpy(),
            base_value=_as_scalar(iv.baseline_value) if hasattr(iv, "baseline_value") else 0.0,
            out_path=out_dir / f"shapiq_local_{_sanitize(region_name)}_{forecast_season}_{i}.png",
            title=f"shapiq local — {region_name} {forecast_season} sample {i}",
        )
    return shap_array


# ---------------------------------------------------------------------------
# Q2: Which feature pairs interact most?
# ---------------------------------------------------------------------------

def explain_interactions(
    model,
    X_background: pd.DataFrame,
    y_background: pd.Series | np.ndarray,
    X_test: pd.DataFrame,
    feature_names: list[str],
    out_dir: Path,
    region_name: str,
    forecast_season,
    *,
    max_order: int = 2,
    top_n_pairs: int = 15,
    max_evals: int = 256,
):
    """Pairwise feature-interaction explanation via k-SII (Shapley
    Interaction Index, k=max_order). Renders a heatmap of the top N
    pairs by ``|k-SII|`` aggregated across rows in ``X_test``.

    Returns a (top_n_pairs, 3) DataFrame ``[feat_a, feat_b, k_sii]``.
    No-op (returns None) when shapiq is unavailable.
    """
    if not _shapiq_available():
        logger.debug("shapiq not installed; skipping interaction explainer")
        return None
    import shapiq

    _ensure_shapiq_numpy2_compat()

    try:
        explainer = shapiq.TabPFNExplainer(
            model=model,
            data=X_background.to_numpy(),
            labels=np.asarray(y_background),
            index="k-SII",
            max_order=max_order,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"shapiq.TabPFNExplainer (k-SII) init failed: {exc}")
        return None

    n_feats = len(feature_names)
    pair_sum = np.zeros((n_feats, n_feats), dtype=float)
    pair_count = 0
    for _, row in X_test.iterrows():
        try:
            iv = explainer.explain(row.to_numpy(), budget=max_evals)
            order2 = np.asarray(iv.get_n_order_values(2))  # symmetric matrix
            pair_sum += np.abs(order2)
            pair_count += 1
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"  shapiq interactions failed for one row: {exc}")
            continue
    if pair_count == 0:
        return None
    pair_mean = pair_sum / pair_count

    # Extract top pairs (upper triangle only)
    iu, ju = np.triu_indices(n_feats, k=1)
    flat = pair_mean[iu, ju]
    order_idx = np.argsort(-flat)[:top_n_pairs]
    top = pd.DataFrame({
        "feat_a": [feature_names[iu[k]] for k in order_idx],
        "feat_b": [feature_names[ju[k]] for k in order_idx],
        "k_sii_abs_mean": flat[order_idx],
    })

    out_dir.mkdir(parents=True, exist_ok=True)
    top.to_csv(out_dir / f"shapiq_interactions_{_sanitize(region_name)}_{forecast_season}.csv", index=False)
    _render_interactions(
        top, out_dir / f"shapiq_interactions_{_sanitize(region_name)}_{forecast_season}.png",
        title=f"Top {top_n_pairs} feature interactions (k-SII) — {region_name} {forecast_season}",
    )
    return top


# ---------------------------------------------------------------------------
# Q3: How does feature X affect predictions globally?
# ---------------------------------------------------------------------------

def explain_pdp(
    model,
    X_background: pd.DataFrame,
    feature_names: list[str],
    out_dir: Path,
    country: str,
    crop: str,
    *,
    top_n_features: int = 5,
    n_grid: int = 30,
    feature_importance: np.ndarray | None = None,
):
    """Partial dependence plots for the top-N features by importance.

    Uses sklearn's ``partial_dependence`` over the background data.
    Writes one PNG (one panel per feature) plus a CSV with the grid +
    average prediction per grid point.

    ``feature_importance`` (e.g. mean |SHAP|) picks the top N; falls
    back to "highest variance" if not supplied.
    """
    try:
        from sklearn.inspection import partial_dependence
    except ImportError:
        logger.warning("sklearn.inspection.partial_dependence not available; skipping PDP")
        return None

    n_feats = len(feature_names)
    if feature_importance is not None and len(feature_importance) == n_feats:
        rank = np.argsort(-np.abs(feature_importance))
    else:
        rank = np.argsort(-X_background.var(axis=0).to_numpy())
    picks = rank[:top_n_features]

    pdp_rows = []
    fig, axes = plt.subplots(
        1, len(picks), figsize=(3.2 * len(picks), 3.5), squeeze=False,
    )
    for ax, idx in zip(axes[0], picks):
        feat = feature_names[idx]
        try:
            pd_res = partial_dependence(
                model, X_background, [idx], grid_resolution=n_grid,
                kind="average",
            )
            grid = np.asarray(pd_res["grid_values"][0])
            avg = np.asarray(pd_res["average"])[0]
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"  PDP failed for feature {feat}: {exc}")
            ax.set_visible(False)
            continue
        ax.plot(grid, avg, color="#4c72b0", linewidth=1.5)
        ax.set_xlabel(feat, fontsize=8)
        ax.set_ylabel("Predicted yield")
        ax.grid(True, linestyle=":", alpha=0.4)
        for g, a in zip(grid, avg):
            pdp_rows.append({"feature": feat, "x": float(g), "y": float(a)})

    fig.suptitle(
        f"Partial dependence — {country.title()} {crop.title()} (top {len(picks)} features)",
        fontsize=10, fontweight="bold",
    )
    plt.tight_layout()
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / "shapiq_pdp.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    pdp_df = pd.DataFrame(pdp_rows)
    pdp_df.to_csv(out_dir / "shapiq_pdp.csv", index=False)
    return pdp_df


# ---------------------------------------------------------------------------
# Q4: SHAP-compatible values (drop-in for downstream SHAP plots)
# ---------------------------------------------------------------------------

def explain_shap_compat(
    model,
    X_background: pd.DataFrame,
    y_background: pd.Series | np.ndarray,
    X_test: pd.DataFrame,
    feature_names: list[str],
    *,
    max_evals: int = 256,
):
    """Standard SHAP values via ``shapiq.TabPFNImputationExplainer``.

    Returns a ``shap.Explanation``-compatible structure (with .values,
    .base_values, .data, .feature_names) so the existing beeswarm /
    waterfall / DB-storage paths in xai.explain can consume them
    without modification. No-op (returns None) when shapiq unavailable.
    """
    if not _shapiq_available():
        logger.debug("shapiq not installed; skipping SHAP-compat explainer")
        return None
    import shap as _shap
    import shapiq

    _ensure_shapiq_numpy2_compat()

    # shapiq 1.4.1's actual public API for SHAP-compatible values is the
    # same TabPFNExplainer with index="SV" (standard Shapley values).
    # TabPFNImputer exists but is a feature-imputer building block, not
    # an explainer — wrong abstraction for this question.
    try:
        explainer = shapiq.TabPFNExplainer(
            model=model,
            data=X_background.to_numpy(),
            labels=np.asarray(y_background),
            index="SV",
            max_order=1,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"shapiq.TabPFNExplainer (SHAP-compat / SV) init failed: {exc}")
        return None

    n_test = len(X_test)
    n_feats = len(feature_names)
    values = np.zeros((n_test, n_feats), dtype=float)
    base = np.zeros(n_test, dtype=float)
    for i, (_, row) in enumerate(X_test.iterrows()):
        try:
            iv = explainer.explain(row.to_numpy(), budget=max_evals)
            sv = np.asarray(iv.get_n_order_values(1)).reshape(-1)
            values[i, :len(sv)] = sv
            base[i] = _as_scalar(getattr(iv, "baseline_value", 0.0))
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"  shapiq SHAP-compat failed for sample {i}: {exc}")
            continue

    return _shap.Explanation(
        values=values,
        base_values=base,
        data=X_test.to_numpy(),
        feature_names=feature_names,
    )


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------

def _render_waterfall(sv, feature_names, feature_values, base_value, out_path, title):
    """Compact horizontal-bar waterfall for one sample's SHAP values."""
    n = len(sv)
    order = np.argsort(-np.abs(sv))[:min(20, n)]  # top 20 by |contribution|
    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(7, max(3, len(order) * 0.25)))
        colors = ["#c44e52" if v < 0 else "#55a868" for v in sv[order]]
        ax.barh(range(len(order)), sv[order][::-1],
                color=colors[::-1], edgecolor="white")
        labels = [
            f"{feature_names[i]} = {feature_values[i]:.3g}" for i in order[::-1]
        ]
        ax.set_yticks(range(len(order)))
        ax.set_yticklabels(labels, fontsize=7)
        ax.axvline(0, color="black", linewidth=0.7, alpha=0.5)
        ax.set_xlabel(
            f"SHAP value (base={base_value:.3g})", fontsize=8,
        )
        ax.set_title(title, fontsize=9, fontweight="bold")
        ax.grid(True, axis="x", linestyle=":", alpha=0.4)
        plt.tight_layout()
        fig.savefig(out_path, dpi=200, bbox_inches="tight")
        plt.close(fig)


def _render_interactions(top_df, out_path, title):
    """Horizontal bar of top feature-pair k-SII magnitudes."""
    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(8, max(3, len(top_df) * 0.3)))
        labels = [f"{r.feat_a}  ×  {r.feat_b}" for r in top_df.itertuples()]
        ax.barh(range(len(top_df)),
                top_df["k_sii_abs_mean"][::-1],
                color="#4c72b0", edgecolor="white")
        ax.set_yticks(range(len(top_df)))
        ax.set_yticklabels(labels[::-1], fontsize=7)
        ax.set_xlabel("|k-SII| (mean over test samples)", fontsize=8)
        ax.set_title(title, fontsize=9, fontweight="bold")
        ax.grid(True, axis="x", linestyle=":", alpha=0.4)
        plt.tight_layout()
        fig.savefig(out_path, dpi=200, bbox_inches="tight")
        plt.close(fig)
