"""
validation.py — compute validation metrics (rRMSEp, sMAPE, R²) and produce
geocif-style diagnostic plots for AquaCrop yield predictions.

Metrics match geocif's yield_outlook reporting:
    - RMSE (t/ha)
    - sMAPE (symmetric MAPE — robust on near-zero observed values;
      replaces vanilla MAPE per the open work item)
    - R² per-region and pooled
    - rRMSEp = RMSE / pooled_obs_mean × 100 (paper-conformant)

Plots match ``geocif.viz.diagnostics.scatter_obs_pred`` conventions.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Symmetric MAPE. Robust against near-zero y_true.

    sMAPE = mean( 2 * |y - y'| / (|y| + |y'|) ) * 100

    Returns percent; NaN if no finite paired values.
    """
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    if not mask.any():
        return np.nan
    y_t = y_true[mask]
    y_p = y_pred[mask]
    denom = np.abs(y_t) + np.abs(y_p)
    # Avoid 0/0; treat as perfect when both are zero
    safe = np.where(denom == 0, 1.0, denom)
    return float(np.mean(2.0 * np.abs(y_t - y_p) / safe) * 100.0)


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root mean squared error in input units."""
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    if not mask.any():
        return np.nan
    return float(np.sqrt(np.mean((y_true[mask] - y_pred[mask]) ** 2)))


def rrmsep(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Paper-conformant rRMSEp = RMSE / pooled_obs_mean × 100.

    This is the comparison metric of choice in geocif.
    """
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    if not mask.any():
        return np.nan
    pooled_mean = float(np.mean(y_true[mask]))
    if pooled_mean == 0:
        return np.nan
    return float(rmse(y_true[mask], y_pred[mask]) / pooled_mean * 100.0)


def r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Coefficient of determination R²."""
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    if mask.sum() < 2:
        return np.nan
    y_t = y_true[mask]
    y_p = y_pred[mask]
    ss_res = float(np.sum((y_t - y_p) ** 2))
    ss_tot = float(np.sum((y_t - np.mean(y_t)) ** 2))
    if ss_tot == 0:
        return np.nan
    return 1.0 - ss_res / ss_tot


def compute_metrics(
    df: pd.DataFrame,
    *,
    pred_col: str = "Predicted Yield (tn per ha)",
    obs_col: str = "Observed Yield (tn per ha)",
    groupby: Optional[list[str]] = None,
) -> pd.DataFrame:
    """Compute (RMSE, sMAPE, R², rRMSEp, N) per group.

    If ``groupby`` is None, returns one pooled-result row.
    """
    if groupby is None:
        y = df[obs_col].to_numpy()
        p = df[pred_col].to_numpy()
        return pd.DataFrame([{
            "RMSE (t/ha)": rmse(y, p),
            "sMAPE (%)": smape(y, p),
            "R2": r_squared(y, p),
            "rRMSEp (%)": rrmsep(y, p),
            "N": int(np.sum(np.isfinite(y) & np.isfinite(p))),
        }])

    rows = []
    for keys, group in df.groupby(groupby):
        y = group[obs_col].to_numpy()
        p = group[pred_col].to_numpy()
        row = dict(zip(groupby, keys if isinstance(keys, tuple) else (keys,)))
        row.update({
            "RMSE (t/ha)": rmse(y, p),
            "sMAPE (%)": smape(y, p),
            "R2": r_squared(y, p),
            "rRMSEp (%)": rrmsep(y, p),
            "N": int(np.sum(np.isfinite(y) & np.isfinite(p))),
        })
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Diagnostic plots
# ---------------------------------------------------------------------------

def scatter_obs_pred(
    df: pd.DataFrame,
    out_path: Path,
    *,
    pred_col: str = "Predicted Yield (tn per ha)",
    obs_col: str = "Observed Yield (tn per ha)",
    title: str = "",
    annotate: bool = True,
) -> Optional[Path]:
    """Observed vs predicted scatter with metrics annotation.

    Mirrors ``geocif.viz.diagnostics.scatter_obs_pred`` style: 1:1 diagonal,
    metrics box (RMSE, sMAPE, R², N) in the corner.

    Args:
        df: Frame with paired obs and pred columns.
        out_path: PNG output path.
        title: Plot title.

    Returns:
        out_path on success, None if matplotlib unavailable.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning("matplotlib not available — skipping scatter plot")
        return None

    y = df[obs_col].to_numpy()
    p = df[pred_col].to_numpy()
    mask = np.isfinite(y) & np.isfinite(p)
    if mask.sum() == 0:
        logger.warning("No paired (obs, pred) data — skipping scatter")
        return None

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(y[mask], p[mask], s=18, alpha=0.7, edgecolor="k", linewidth=0.3)

    lim = max(np.nanmax(y[mask]), np.nanmax(p[mask])) * 1.05
    ax.plot([0, lim], [0, lim], "k--", linewidth=1, alpha=0.6)
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_xlabel(obs_col)
    ax.set_ylabel(pred_col)
    ax.set_title(title or "AquaCrop: Observed vs Predicted")
    ax.set_aspect("equal", "box")

    if annotate:
        m = {
            "RMSE": rmse(y, p),
            "sMAPE": smape(y, p),
            "R²": r_squared(y, p),
            "N": int(mask.sum()),
        }
        text = (
            f"RMSE: {m['RMSE']:.2f} t/ha\n"
            f"sMAPE: {m['sMAPE']:.1f}%\n"
            f"R²: {m['R²']:.3f}\n"
            f"N: {m['N']}"
        )
        ax.text(
            0.04, 0.96, text, transform=ax.transAxes, va="top", ha="left",
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="gray"),
        )

    fig.tight_layout()
    fig.savefig(out_path, dpi=110)
    plt.close(fig)
    return out_path


def mape_by_year_bar(
    df: pd.DataFrame,
    out_path: Path,
    *,
    pred_col: str = "Predicted Yield (tn per ha)",
    obs_col: str = "Observed Yield (tn per ha)",
    title: str = "",
) -> Optional[Path]:
    """Bar chart of sMAPE per Harvest Year — geocif workhorse diagnostic."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    per_year = compute_metrics(df, pred_col=pred_col, obs_col=obs_col,
                               groupby=["Harvest Year"])
    if per_year.empty:
        return None

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(per_year["Harvest Year"].astype(int).astype(str),
           per_year["sMAPE (%)"], color="#3b6db5")
    ax.set_xlabel("Harvest Year")
    ax.set_ylabel("sMAPE (%)")
    ax.set_title(title or "AquaCrop sMAPE by Harvest Year")
    fig.tight_layout()
    fig.savefig(out_path, dpi=110)
    plt.close(fig)
    return out_path


def mape_by_region_bar(
    df: pd.DataFrame,
    out_path: Path,
    *,
    pred_col: str = "Predicted Yield (tn per ha)",
    obs_col: str = "Observed Yield (tn per ha)",
    title: str = "",
    top_n: int = 25,
) -> Optional[Path]:
    """Bar chart of sMAPE per Region — workhorse diagnostic.

    Shows the top_n worst-performing regions (highest sMAPE).
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    per_region = compute_metrics(df, pred_col=pred_col, obs_col=obs_col,
                                 groupby=["Region"])
    if per_region.empty:
        return None
    per_region = per_region.sort_values("sMAPE (%)", ascending=False).head(top_n)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, max(4, top_n * 0.25)))
    ax.barh(per_region["Region"], per_region["sMAPE (%)"], color="#b53b3b")
    ax.invert_yaxis()
    ax.set_xlabel("sMAPE (%)")
    ax.set_title(title or f"AquaCrop: Top {top_n} regions by sMAPE")
    fig.tight_layout()
    fig.savefig(out_path, dpi=110)
    plt.close(fig)
    return out_path


def run_full_diagnostics(
    df: pd.DataFrame,
    out_dir: Path,
    *,
    label: str = "aquacrop",
    pred_col: str = "Predicted Yield (tn per ha)",
    obs_col: str = "Observed Yield (tn per ha)",
) -> dict:
    """Produce the full diagnostic suite and return a summary dict.

    Writes scatter + MAPE-by-year + MAPE-by-region PNGs under out_dir.

    Returns:
        Summary dict with 'pooled', 'per_region', 'per_year' tables and
        the list of plot paths.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pooled = compute_metrics(df, pred_col=pred_col, obs_col=obs_col)
    per_region = compute_metrics(df, pred_col=pred_col, obs_col=obs_col,
                                 groupby=["Region"])
    per_year = compute_metrics(df, pred_col=pred_col, obs_col=obs_col,
                               groupby=["Harvest Year"])

    plots = []
    p = scatter_obs_pred(df, out_dir / f"{label}_scatter.png",
                         pred_col=pred_col, obs_col=obs_col,
                         title=f"{label}: Observed vs Predicted")
    if p: plots.append(p)

    p = mape_by_year_bar(df, out_dir / f"{label}_mape_by_year.png",
                        pred_col=pred_col, obs_col=obs_col,
                        title=f"{label}: sMAPE by year")
    if p: plots.append(p)

    p = mape_by_region_bar(df, out_dir / f"{label}_mape_by_region.png",
                          pred_col=pred_col, obs_col=obs_col,
                          title=f"{label}: top regions by sMAPE")
    if p: plots.append(p)

    return {
        "pooled": pooled,
        "per_region": per_region,
        "per_year": per_year,
        "plots": plots,
    }
