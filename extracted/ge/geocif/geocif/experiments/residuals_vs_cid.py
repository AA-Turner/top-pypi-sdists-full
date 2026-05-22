"""Compare yield-model residuals against CID anomalies.

Helps diagnose whether a CID (e.g. AUC_NDVI, PRCPTOT) carries signal the
yield model is failing to absorb.  For each (country, crop, model, stage)
combination, joins per-region residuals from the outlook DB with z-scored
CID values from the per-country statistics CSV, then reports Pearson /
Spearman correlation + OLS R² and renders scatter + heatmap diagnostics.

Two modes:
    cid="AUC_NDVI"  — single-CID deep dive (default).
    cid="all"       — rank every CID column by mean |Pearson r| across
                       stages; highlight top_k for follow-up inspection.

Usage::

    from geocif.experiments import residuals_vs_cid
    residuals_vs_cid.run(cfg)                          # AUC_NDVI default
    residuals_vs_cid.run(cfg, cid="PRCPTOT")           # single CID
    residuals_vs_cid.run(cfg, cid="all", top_k=10)     # scan + rank
"""

import ast
import logging
import os
import sqlite3
import warnings
from pathlib import Path

import arrow as ar
import numpy as np
import pandas as pd

from geocif import logger as log
from geocif import utils as ut
from geocif import yield_outlook

warnings.simplefilter(action="ignore", category=FutureWarning)

logger = logging.getLogger(__name__)

_CANON_PRED = "Predicted Yield (tn per ha)"
_CANON_OBS = "Observed Yield (tn per ha)"

# Columns that should never be treated as candidate CIDs even if numeric.
_METADATA_COLS = {
    "Country", "Region", "Region_ID", "Harvest Year",
    "Stage Name", "Stage Names", "Stage", "Stage_ID", "Stage Range",
    "Starting Stage", "Ending Stage", "Percentage Season",
    "Country Region", "Country__Region", "lat", "lon",
    "Analogous Year", "Analogous Year Yield",
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

_MONTH_ABBR = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}


def _normalize_stage_name(name):
    """Convert CSV ``Stage Names`` strings to the outlook DB convention.

    Two known divergences:
    - Pre-season rows in the CSV carry the raw Stage_ID ``PS_<n>`` /
      ``IS_<n>``; the DB stores the friendly ``Pre-Season (init <Mon>)`` /
      ``In-Season (init <Mon>)``.
    - In-season rows in the CSV use ``"Jul 1 - Jul 31"`` (spaces around the
      dash); the DB stores ``"Jul 1-Jul 31"`` (no spaces).
    """
    if not isinstance(name, str):
        return name
    s = name.strip()
    for prefix, label in (("PS_", "Pre-Season"), ("IS_", "In-Season")):
        if s.startswith(prefix):
            try:
                m = int(s.split("_", 1)[1])
            except (ValueError, IndexError):
                return s
            mon = _MONTH_ABBR.get(m)
            return f"{label} (init {mon})" if mon else s
    return s.replace(" - ", "-")


def _load_statistics_csv(dir_output, method, country, crop):
    """Load the per-country statistics CSV that feeds the ML pipeline.

    The on-disk CSV is in *long* format — one row per
    ``(Country, Region, Year, Stage, Index, Type)`` tuple, with the CID
    name in the ``Index`` string column and the CID value in the
    poorly-named ``CID`` float64 column. Pivot to wide format so each
    real CID (``MEAN_NDVI``, ``AUC_NDVI``, ``MEAN_FLDAS_*_LEAD<n>``, …)
    becomes its own column — that's what ``_resolve_cid_columns``
    downstream assumes.

    Also normalizes the stage column name (``Stage Names`` plural → DB's
    ``Stage Name`` singular) and the per-row stage strings (``PS_<n>`` →
    ``Pre-Season (init <Mon>)``, ``" - "`` → ``"-"``) so the residual /
    CID merge keys align.
    """
    path = ut.statistics_file_path(dir_output, method, country, crop)
    if not path.exists():
        logger.warning(f"Statistics CSV missing for {country} {crop}: {path}")
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "Stage Name" not in df.columns and "Stage Names" in df.columns:
        df = df.rename(columns={"Stage Names": "Stage Name"})
    if "Stage Name" in df.columns:
        df["Stage Name"] = df["Stage Name"].map(_normalize_stage_name)

    # Long → wide pivot. (Region, Year, Stage Name, Index) is the unique
    # row key in the CSV, so ``first`` is exact (not lossy averaging).
    if "Index" in df.columns and "CID" in df.columns:
        df = df.dropna(subset=["Index"])
        index_keys = ["Country", "Region", "Harvest Year", "Stage Name"]
        # Include Season when present so Gu/Deyr (Somalia) or other
        # multi-season crops don't collide on the same Stage Name.
        if "Season" in df.columns:
            index_keys.append("Season")
        index_keys = [k for k in index_keys if k in df.columns]
        df = (
            df.pivot_table(
                index=index_keys,
                columns="Index",
                values="CID",
                aggfunc="first",
            )
            .reset_index()
        )
        df.columns.name = None
    return df


def _resolve_cid_columns(df, target, stat_cols, requested):
    """Resolve the ``cid`` argument to a concrete list of CID column names.

    requested may be: "all" | "<name>" | list[str].
    """
    fixed_cols = list(_METADATA_COLS) + [target] + list(stat_cols)
    if isinstance(requested, str) and requested.lower() == "all":
        return ut.filter_cid_columns(df, fixed_cols, target, stat_cols)
    names = [requested] if isinstance(requested, str) else list(requested)
    missing = [n for n in names if n not in df.columns]
    if missing:
        raise ValueError(
            f"Requested CID column(s) not in statistics CSV: {missing}"
        )
    return names


def _compute_cid_anomaly(df, cid_cols):
    """Z-score each CID within (Region, Stage Name) groups across years.

    Groups with fewer than 3 valid years or zero std contribute NaN.
    Returns a DataFrame with the same index as ``df`` and one ``_anomaly``
    column per CID.
    """
    anom_cols = {}
    grouped = df.groupby(["Region", "Stage Name"], dropna=False)
    for cid in cid_cols:
        # Per-group z-score; .transform preserves the original row order.
        def _z(s):
            s = pd.to_numeric(s, errors="coerce")
            if s.notna().sum() < 3:
                return pd.Series(np.nan, index=s.index)
            sigma = s.std(ddof=0)
            if not np.isfinite(sigma) or sigma == 0:
                return pd.Series(np.nan, index=s.index)
            return (s - s.mean()) / sigma
        anom_cols[f"{cid}__anom"] = grouped[cid].transform(_z)
    return pd.DataFrame(anom_cols, index=df.index)


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def _correlations(x, y):
    """Return dict with n, pearson_r, p_value, spearman_rho, slope, intercept, r2.

    NaNs in either array are dropped pairwise.  Falls back to NaN values
    when n < 3 or all-constant.
    """
    from scipy import stats as sps

    mask = np.isfinite(x) & np.isfinite(y)
    n = int(mask.sum())
    out = {
        "n": n, "pearson_r": np.nan, "p_value": np.nan,
        "spearman_rho": np.nan, "slope": np.nan, "intercept": np.nan,
        "r2": np.nan,
    }
    if n < 3:
        return out
    xv, yv = x[mask], y[mask]
    if xv.std() == 0 or yv.std() == 0:
        return out
    try:
        r, p = sps.pearsonr(xv, yv)
        out["pearson_r"] = float(r)
        out["p_value"] = float(p)
    except Exception:
        pass
    try:
        rho, _ = sps.spearmanr(xv, yv)
        out["spearman_rho"] = float(rho)
    except Exception:
        pass
    try:
        lr = sps.linregress(xv, yv)
        out["slope"] = float(lr.slope)
        out["intercept"] = float(lr.intercept)
        out["r2"] = float(lr.rvalue ** 2)
    except Exception:
        pass
    return out


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------

def _region_palette(regions):
    """Categorical palette keyed by region — same convention as yield_outlook
    (tab20 for ≤20, tab20b+tab20c stacked beyond)."""
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    unique = sorted(set(regions))
    n = len(unique)
    if n <= 20:
        cmap = plt.cm.get_cmap("tab20", max(n, 1))
        palette = [cmap(i) for i in range(n)]
    else:
        stacked = np.vstack([
            plt.cm.tab20b(np.linspace(0, 1, 20)),
            plt.cm.tab20c(np.linspace(0, 1, 20)),
        ])
        palette = [stacked[i % len(stacked)] for i in range(n)]
    return dict(zip(unique, palette))


def _scatter_residual_vs_anomaly(
    df, cid, stage_name, title, out_path, stats,
):
    """One scatter PNG: x = CID anomaly, y = residual, colored by Region."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    import scienceplots  # noqa: F401

    x = df[f"{cid}__anom"].values
    y = df["Residual"].values
    regions = df["Region"].astype(str).tolist()
    palette = _region_palette(regions)
    colors = [palette[r] for r in regions]

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.axhline(0, color="gray", linewidth=0.8)
        ax.axvline(0, color="gray", linewidth=0.8)
        ax.scatter(x, y, color=colors, s=40, zorder=3)

        # OLS fit line if available
        if np.isfinite(stats.get("slope", np.nan)):
            xs = np.linspace(np.nanmin(x), np.nanmax(x), 50)
            ax.plot(xs, stats["intercept"] + stats["slope"] * xs,
                    color="black", linewidth=1.2, linestyle="--")

        ax.set_xlabel(f"{cid} anomaly (z-score, per Region·Stage)")
        ax.set_ylabel("Residual (Observed − Predicted, tn/ha)")
        ax.set_title(title, fontsize=10)

        ann = (
            f"n: {stats['n']}\n"
            f"Pearson r: {stats['pearson_r']:.2f}\n"
            f"p: {stats['p_value']:.3f}\n"
            f"slope: {stats['slope']:.3f}\n"
            f"R²: {stats['r2']:.2f}"
        )
        ax.annotate(ann, xy=(0.05, 0.95), xycoords="axes fraction",
                    fontsize=9, verticalalignment="top",
                    bbox=dict(facecolor="white", edgecolor="gray", alpha=0.8))

        handles = [
            Line2D([0], [0], marker="o", linestyle="",
                   markerfacecolor=c, markeredgecolor=c, markersize=6, label=r)
            for r, c in palette.items()
        ]
        ncol = 2 if len(palette) > 10 else 1
        ax.legend(handles=handles, title="Region",
                  bbox_to_anchor=(1.02, 1), loc="upper left",
                  fontsize=7, title_fontsize=8, ncol=ncol, frameon=False)
        plt.tight_layout()
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=250, bbox_inches="tight")
        plt.close(fig)


def _correlation_heatmap_stage_region(detail_df, title, out_path):
    """Stage × Region heatmap of Pearson r.

    Stage Name rows are sorted chronologically (pre-season inits first via
    ``yield_outlook._stage_sort_key``). Cells carry a light gray border
    matching the CID × Stage ranking heatmap.
    """
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    if detail_df.empty:
        return
    pivot = detail_df.pivot_table(
        index="Stage Name", columns="Region", values="pearson_r",
    )
    if pivot.empty:
        return

    # Chronological row ordering.
    stage_names = list(pivot.index)
    planting_month = yield_outlook._infer_planting_month(stage_names)
    sorted_stages = sorted(
        stage_names,
        key=lambda s: yield_outlook._stage_sort_key(s, planting_month),
    )
    pivot = pivot.reindex(index=sorted_stages)

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(
            figsize=(max(8, pivot.shape[1] * 0.6),
                     max(4, pivot.shape[0] * 0.5))
        )
        im = ax.imshow(pivot.values, cmap="RdBu_r", vmin=-1, vmax=1,
                       aspect="auto", interpolation="nearest")
        ax.set_xticks(range(pivot.shape[1]))
        ax.set_xticklabels(pivot.columns, rotation=45, ha="right", fontsize=8)
        ax.set_yticks(range(pivot.shape[0]))
        ax.set_yticklabels(pivot.index, fontsize=8)
        ax.tick_params(axis="both", which="both", length=0)

        # Light gridlines around each cell.
        for i in range(pivot.shape[0] + 1):
            ax.axhline(y=i - 0.5, color="#e0e0e0", linewidth=0.4)
        for j in range(pivot.shape[1] + 1):
            ax.axvline(x=j - 0.5, color="#e0e0e0", linewidth=0.4)

        for i in range(pivot.shape[0]):
            for j in range(pivot.shape[1]):
                v = pivot.values[i, j]
                if np.isfinite(v):
                    ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                            fontsize=7,
                            color="white" if abs(v) > 0.5 else "black")
        plt.colorbar(im, ax=ax, label="Pearson r", shrink=0.8)
        ax.set_title(title, fontsize=10)
        plt.tight_layout()
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=250, bbox_inches="tight")
        plt.close(fig)


def _ranking_bar(pooled_df, title, out_path, max_bars=30):
    """Horizontal bar chart of CIDs ranked by mean |r|, colored by sign of mean r."""
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    if pooled_df.empty:
        return
    top = pooled_df.head(max_bars).iloc[::-1]  # so largest sits at the top
    colors = ["#1f77b4" if v >= 0 else "#d62728" for v in top["mean_r"].values]

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(8, max(4, 0.3 * len(top))))
        bars = ax.barh(top["cid"].values, top["mean_abs_r"].values, color=colors)
        for bar, r, n_st in zip(bars, top["mean_r"].values, top["n_stages"].values):
            ax.text(bar.get_width() + 0.005,
                    bar.get_y() + bar.get_height() / 2,
                    f"r̄={r:+.2f} (k={int(n_st)})",
                    va="center", fontsize=7)
        ax.set_xlabel("Mean |Pearson r| across stages")
        ax.set_title(title, fontsize=10)
        ax.set_xlim(0, max(top["mean_abs_r"].max() * 1.25, 0.1))
        # Legend for sign
        from matplotlib.patches import Patch
        ax.legend(handles=[
            Patch(color="#1f77b4", label="mean r > 0 (under-predicts in high-CID years)"),
            Patch(color="#d62728", label="mean r < 0 (over-predicts in high-CID years)"),
        ], fontsize=7, loc="lower right", frameon=False)
        plt.tight_layout()
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=250, bbox_inches="tight")
        plt.close(fig)


def _ranking_heatmap_cid_stage(ranking_df, title, out_path, max_cids=30):
    """CID × Stage Name heatmap of Pearson r for the top-N CIDs by mean |r|.

    Stage Names on the x-axis are sorted chronologically — pre-season inits
    first (planting-month-aware via ``yield_outlook._stage_sort_key``),
    then in-season cumulative stages. Cells carry a light gray border and
    are annotated with the Pearson r value to two decimal places.
    """
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    if ranking_df.empty:
        return
    pooled = (
        ranking_df.assign(abs_r=ranking_df["pearson_r"].abs())
        .groupby("cid")["abs_r"].mean().sort_values(ascending=False)
    )
    top_cids = pooled.head(max_cids).index.tolist()
    sub = ranking_df[ranking_df["cid"].isin(top_cids)]
    pivot = sub.pivot_table(index="cid", columns="Stage Name", values="pearson_r")
    if pivot.empty:
        return

    # Chronological stage ordering: pre-season inits first, then in-season.
    stage_names = list(pivot.columns)
    planting_month = yield_outlook._infer_planting_month(stage_names)
    sorted_stages = sorted(
        stage_names,
        key=lambda s: yield_outlook._stage_sort_key(s, planting_month),
    )
    pivot = pivot.reindex(index=top_cids, columns=sorted_stages)

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(
            figsize=(max(8, pivot.shape[1] * 0.7),
                     max(4, pivot.shape[0] * 0.35))
        )
        im = ax.imshow(pivot.values, cmap="RdBu_r", vmin=-1, vmax=1,
                       aspect="auto", interpolation="nearest")
        ax.set_xticks(range(pivot.shape[1]))
        ax.set_xticklabels(pivot.columns, rotation=45, ha="right", fontsize=7)
        ax.set_yticks(range(pivot.shape[0]))
        ax.set_yticklabels(pivot.index, fontsize=7)
        ax.tick_params(axis="both", which="both", length=0)

        # Light gridlines around each cell.
        for i in range(pivot.shape[0] + 1):
            ax.axhline(y=i - 0.5, color="#e0e0e0", linewidth=0.4)
        for j in range(pivot.shape[1] + 1):
            ax.axvline(x=j - 0.5, color="#e0e0e0", linewidth=0.4)

        # Annotate each cell with Pearson r (2dp).
        for i in range(pivot.shape[0]):
            for j in range(pivot.shape[1]):
                v = pivot.values[i, j]
                if np.isfinite(v):
                    ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                            fontsize=6,
                            color="white" if abs(v) > 0.5 else "black")

        plt.colorbar(im, ax=ax, label="Pearson r", shrink=0.8)
        ax.set_title(title, fontsize=10)
        plt.tight_layout()
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=250, bbox_inches="tight")
        plt.close(fig)


# ---------------------------------------------------------------------------
# Per-model processing
# ---------------------------------------------------------------------------

def _models_in_table(db_path, table):
    """List Model values present for the 'outlook' experiment in this table."""
    if not db_path.exists():
        return []
    con = sqlite3.connect(db_path)
    try:
        return pd.read_sql(
            f'SELECT DISTINCT Model FROM "{table}" '
            f'WHERE "Experiment Name" = ? ORDER BY Model',
            con, params=("outlook",),
        )["Model"].tolist()
    except Exception:
        return []
    finally:
        con.close()


def _residuals_for_model(db_path, table, model):
    df = yield_outlook._query_predictions(db_path, table, model,
                                          experiment_name="outlook")
    if df.empty:
        return df
    df = df.dropna(subset=[_CANON_PRED, _CANON_OBS]).copy()
    df["Residual"] = df[_CANON_OBS] - df[_CANON_PRED]
    df["Harvest Year"] = df["Harvest Year"].astype(int)
    return df


def _join_residuals_with_cid(df_resid, df_stats_with_anom, cid_cols):
    """Inner-join on (Country, Region, Harvest Year, Stage Name)."""
    keep_stats = (
        ["Country", "Region", "Harvest Year", "Stage Name"]
        + cid_cols
        + [f"{c}__anom" for c in cid_cols]
    )
    keep_stats = [c for c in keep_stats if c in df_stats_with_anom.columns]
    rhs = df_stats_with_anom[keep_stats].copy()
    # Country in the DB may be lower/_underscore; in stats CSV it's title case.
    rhs["Country"] = rhs["Country"].astype(str).str.lower().str.replace(" ", "_")
    lhs = df_resid.copy()
    lhs["Country"] = lhs["Country"].astype(str).str.lower().str.replace(" ", "_")
    return lhs.merge(
        rhs, on=["Country", "Region", "Harvest Year", "Stage Name"],
        how="inner",
    )


def _summarise_per_stage(df, cid, planting_month):
    """Per (Stage Name) correlation between residual and CID anomaly,
    pooled across regions/years."""
    rows = []
    for stage, sub in df.groupby("Stage Name"):
        s = _correlations(
            sub[f"{cid}__anom"].values.astype(float),
            sub["Residual"].values.astype(float),
        )
        s.update({"Stage Name": stage, "cid": cid})
        rows.append(s)
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["_order"] = out["Stage Name"].apply(
        lambda s: yield_outlook._stage_sort_key(s, planting_month)
    )
    return out.sort_values("_order").drop(columns="_order")


def _summarise_per_stage_region(df, cid):
    """Per (Stage, Region) correlation — feeds the Stage × Region heatmap."""
    rows = []
    for (stage, region), sub in df.groupby(["Stage Name", "Region"]):
        s = _correlations(
            sub[f"{cid}__anom"].values.astype(float),
            sub["Residual"].values.astype(float),
        )
        s.update({"Stage Name": stage, "Region": region, "cid": cid})
        rows.append(s)
    return pd.DataFrame(rows)


def _process_single_cid(
    df_joined, cid, country, crop, model, out_root, planting_month,
):
    """Single-CID mode: scatter per stage + Stage×Region heatmap + CSVs."""
    df = df_joined.dropna(subset=[f"{cid}__anom", "Residual"]).copy()
    if df.empty:
        logger.warning(
            f"No matched (residual, {cid}) rows for {country} {crop} {model}"
        )
        return

    cid_dir = out_root / f"{country}_{crop}" / model / cid
    cid_dir.mkdir(parents=True, exist_ok=True)

    summary = _summarise_per_stage(df, cid, planting_month)
    summary = summary.drop(columns=["cid"])
    summary.to_csv(cid_dir / f"residual_vs_{cid}_summary.csv", index=False)

    detail = _summarise_per_stage_region(df, cid).drop(columns=["cid"])
    detail.to_csv(cid_dir / f"residual_vs_{cid}_detail.csv", index=False)

    df_join_out = df[[
        "Country", "Region", "Harvest Year", "Stage Name",
        _CANON_PRED, _CANON_OBS, "Residual", cid, f"{cid}__anom",
    ]].rename(columns={f"{cid}__anom": f"{cid}_anomaly_z"})
    df_join_out.to_csv(cid_dir / f"residual_vs_{cid}_joined.csv", index=False)

    base_title = (
        f"{country.title().replace('_', ' ')} "
        f"{crop.title().replace('_', ' ')} ({model})"
    )
    for stage, sub in df.groupby("Stage Name"):
        if sub.empty:
            continue
        stats = _correlations(
            sub[f"{cid}__anom"].values.astype(float),
            sub["Residual"].values.astype(float),
        )
        if stats["n"] < 3:
            continue
        stage_safe = (
            yield_outlook.friendly_stage_label(stage)
            .replace(" - ", "-").replace(" ", "_")
        )
        title = f"Residual vs {cid} anomaly — {base_title} — {yield_outlook.friendly_stage_label(stage)}"
        _scatter_residual_vs_anomaly(
            sub, cid, stage, title,
            cid_dir / f"scatter_{stage_safe}.png", stats,
        )

    _correlation_heatmap_stage_region(
        detail,
        f"Pearson r(residual, {cid} anomaly) — {base_title}",
        cid_dir / "correlation_heatmap.png",
    )
    logger.info(f"  [{model}] single-CID '{cid}' → {cid_dir}")
    return summary


def _process_all_cids(
    df_joined, cid_cols, country, crop, model, out_root, top_k,
    planting_month,
):
    """All-CIDs mode: rank by mean |r| across stages, emit top_k detail folders."""
    base_dir = out_root / f"{country}_{crop}" / model / "all_cids"
    base_dir.mkdir(parents=True, exist_ok=True)

    per_cid_summaries = []
    for cid in cid_cols:
        anom_col = f"{cid}__anom"
        if anom_col not in df_joined.columns:
            continue
        sub = df_joined.dropna(subset=[anom_col, "Residual"])
        if sub.empty:
            continue
        s = _summarise_per_stage(sub, cid, planting_month)
        if s.empty:
            continue
        per_cid_summaries.append(s)

    if not per_cid_summaries:
        logger.warning(
            f"No usable CIDs for {country} {crop} {model} in all-CIDs mode"
        )
        return None

    ranking = pd.concat(per_cid_summaries, ignore_index=True)
    ranking["abs_r"] = ranking["pearson_r"].abs()
    # Per (cid, stage) ordered table
    ranking_sorted = ranking.sort_values("abs_r", ascending=False)
    ranking_sorted.to_csv(base_dir / "ranking.csv", index=False)

    # Pooled per-cid table: mean |r| across stages, mean r (signed), max |r|, best stage
    def _pool(g):
        best_idx = g["abs_r"].idxmax()
        return pd.Series({
            "n_stages": int(g["abs_r"].notna().sum()),
            "mean_abs_r": float(g["abs_r"].mean()),
            "mean_r": float(g["pearson_r"].mean()),
            "max_abs_r": float(g["abs_r"].max()),
            "best_stage": g.loc[best_idx, "Stage Name"]
                if pd.notna(best_idx) else "",
            "best_r": float(g["pearson_r"].loc[best_idx])
                if pd.notna(best_idx) else np.nan,
            "best_p": float(g["p_value"].loc[best_idx])
                if pd.notna(best_idx) else np.nan,
        })
    pooled = (
        ranking.groupby("cid").apply(_pool)
        .reset_index().sort_values("mean_abs_r", ascending=False)
    )
    pooled.to_csv(base_dir / "ranking_pooled.csv", index=False)

    base_title = (
        f"{country.title().replace('_', ' ')} "
        f"{crop.title().replace('_', ' ')} ({model})"
    )
    _ranking_bar(
        pooled,
        f"CID ranking by residual-coupling — {base_title}",
        base_dir / "ranking_bar_pooled.png",
    )
    _ranking_heatmap_cid_stage(
        ranking,
        f"Pearson r(residual, CID anomaly) — {base_title}",
        base_dir / "ranking_heatmap.png",
    )

    # Top-K detail folders — scatter + per-(cid,stage) detail CSV.
    top = ranking_sorted.head(top_k).reset_index(drop=True)
    for rank, row in top.iterrows():
        cid = row["cid"]
        stage = row["Stage Name"]
        stage_safe = (
            yield_outlook.friendly_stage_label(stage)
            .replace(" - ", "-").replace(" ", "_")
        )
        sub = df_joined.dropna(subset=[f"{cid}__anom", "Residual"])
        sub = sub[sub["Stage Name"] == stage]
        if sub.empty:
            continue
        stats = _correlations(
            sub[f"{cid}__anom"].values.astype(float),
            sub["Residual"].values.astype(float),
        )
        rank_dir = base_dir / "top_k" / f"{rank+1:02d}_{cid}_{stage_safe}"
        rank_dir.mkdir(parents=True, exist_ok=True)
        title = (
            f"Rank {rank+1}: {cid} @ {yield_outlook.friendly_stage_label(stage)} "
            f"— {base_title}"
        )
        _scatter_residual_vs_anomaly(
            sub, cid, stage, title, rank_dir / "scatter.png", stats,
        )
        detail_one = _summarise_per_stage_region(sub, cid)
        detail_one.to_csv(rank_dir / "detail.csv", index=False)

    logger.info(f"  [{model}] all-CIDs ranking → {base_dir}")
    return pooled


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(
    path_config_files=None,
    *,
    cid="AUC_NDVI",
    top_k=10,
    outlook_db=None,
    parser=None,
    logger_obj=None,
):
    """Compare yield-model residuals against CID anomalies per stage.

    Args:
        path_config_files: List of config file paths (geobase / countries /
            crops / geocif). Ignored when ``parser`` is supplied.
        cid: "all" → scan every CID column; "<name>" → single CID
            (default "AUC_NDVI"); list[str] → exact set.
        top_k: only used when ``cid="all"`` — number of top-coupled
            (CID, Stage) pairs to render detailed scatter for.
        outlook_db: optional explicit path to the outlook SQLite DB. When
            None, uses ``{dir_output}/{project}/ml/db/{[DEFAULT]db}``.
    """
    if parser is None:
        if path_config_files is None:
            path_config_files = [Path("../config/geocif.txt")]
        logger_obj, parser = log.setup_logger_parser(path_config_files)

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_output = Path(parser.get("PATHS", "dir_output")) / project_name
    db_name = outlook_db or parser.get("DEFAULT", "db")
    db_path = Path(outlook_db) if outlook_db and os.sep in str(outlook_db) \
        else dir_output / "ml" / "db" / db_name

    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
    out_root = dir_output / "ml" / "analysis" / today / "explore" / "residuals_vs_cid"
    out_root.mkdir(parents=True, exist_ok=True)

    target = parser.get(
        "ML", "target", fallback="Yield (tn per ha)"
    )
    try:
        stat_cols = ast.literal_eval(
            parser.get("ML", "statistics_columns", fallback="[]")
        )
    except (ValueError, SyntaxError):
        stat_cols = []

    mode_label = "all-CIDs" if (isinstance(cid, str) and cid.lower() == "all") \
        else f"single-CID '{cid}'"
    logger.info(
        f"residuals_vs_cid — mode={mode_label}, db={db_path}, out={out_root}"
    )

    if not db_path.exists():
        raise FileNotFoundError(f"Outlook DB not found: {db_path}")

    pooled_per_combo = []

    for country in countries:
        try:
            crops = ast.literal_eval(parser.get(country, "crops"))
        except Exception:
            continue
        method = parser.get(country, "method", fallback="monthly_r")

        for crop in crops:
            table = f"{country}_{crop}"
            df_stats = _load_statistics_csv(dir_output, method, country, crop)
            if df_stats.empty:
                logger.warning(f"Skipping {country} {crop}: no statistics CSV")
                continue

            try:
                cid_cols = _resolve_cid_columns(
                    df_stats, target, stat_cols, cid,
                )
            except ValueError as e:
                logger.error(f"{country} {crop}: {e}")
                continue

            if not cid_cols:
                logger.warning(f"{country} {crop}: no CID columns resolved")
                continue
            logger.info(
                f"{country} {crop}: {len(cid_cols)} CID column(s) under test"
            )

            anom_df = _compute_cid_anomaly(df_stats, cid_cols)
            df_stats_with_anom = pd.concat([df_stats, anom_df], axis=1)

            models = _models_in_table(db_path, table)
            if not models:
                logger.warning(f"{country} {crop}: no models in DB")
                continue

            # Planting-month-aware stage ordering for heatmaps / sorts.
            stage_names = df_stats_with_anom["Stage Name"].dropna().unique()
            planting_month = yield_outlook._infer_planting_month(stage_names)

            for model in models:
                df_resid = _residuals_for_model(db_path, table, model)
                if df_resid.empty:
                    continue
                df_joined = _join_residuals_with_cid(
                    df_resid, df_stats_with_anom, cid_cols,
                )
                if df_joined.empty:
                    # Loud diagnostic: show key cardinalities so the user
                    # can tell whether the silent zero came from a country
                    # mismatch, a stage-name mismatch, or a year mismatch.
                    resid_stages = sorted(
                        df_resid["Stage Name"].dropna().unique().tolist()
                    )[:5]
                    csv_stages = sorted(
                        df_stats_with_anom["Stage Name"].dropna().unique().tolist()
                    )[:5]
                    logger.warning(
                        f"  [{model}] no joined rows for {country} {crop} — "
                        f"resid n={len(df_resid)} stages(sample)={resid_stages} "
                        f"| csv n={len(df_stats_with_anom)} stages(sample)={csv_stages}"
                    )
                    continue
                logger.info(
                    f"  [{model}] joined {len(df_joined)} rows "
                    f"({df_joined['Stage Name'].nunique()} stages, "
                    f"{df_joined['Region'].nunique()} regions, "
                    f"{df_joined['Harvest Year'].nunique()} years)"
                )

                if isinstance(cid, str) and cid.lower() == "all":
                    pooled = _process_all_cids(
                        df_joined, cid_cols, country, crop, model, out_root,
                        top_k, planting_month,
                    )
                    if pooled is not None:
                        pooled["Country"] = country
                        pooled["Crop"] = crop
                        pooled["Model"] = model
                        pooled_per_combo.append(pooled)
                else:
                    for cname in cid_cols:
                        _process_single_cid(
                            df_joined, cname, country, crop, model, out_root,
                            planting_month,
                        )

    # Top-line README summarising best (CID, Stage) per (country, crop, model)
    if pooled_per_combo:
        all_pooled = pd.concat(pooled_per_combo, ignore_index=True)
        verdict_rows = []
        for (country, crop, model), g in all_pooled.groupby(
            ["Country", "Crop", "Model"]
        ):
            # idxmax returns the index *label*, so use .loc, not .iloc —
            # post-concat(ignore_index=True) the labels are 0..N-1 but after
            # groupby the per-group rows keep their original labels, which
            # break positional indexing once the group doesn't start at 0.
            best = g.loc[g["mean_abs_r"].idxmax()]
            verdict_rows.append(
                f"- **{country} {crop} ({model})**: top CID = "
                f"`{best['cid']}` "
                f"(mean |r|={best['mean_abs_r']:.2f}, "
                f"best stage={best['best_stage']}, "
                f"best r={best['best_r']:+.2f}, p={best['best_p']:.3f})"
            )
        readme = out_root / "README.md"
        readme.write_text(
            "# residuals_vs_cid — top-line verdict\n\n"
            "Best residual-coupled CID per (country, crop, model):\n\n"
            + "\n".join(verdict_rows)
            + "\n\n"
            "See `ranking_bar_pooled.png` and `ranking_heatmap.png` per combo "
            "for the full picture, and `top_k/` for scatter detail on the "
            "strongest-coupled (CID, Stage) pairs.\n"
        )
        logger.info(f"Top-line verdict written to {readme}")

    logger.info(f"residuals_vs_cid done → {out_root}")
    return out_root
