"""Shared diagnostic plot functions: scatter, MAPE bar chart, MAPE choropleth map.

Used by analysis.py, yield_outlook.py, and experiments.py to avoid duplication.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Scatter: Observed vs Predicted
# ---------------------------------------------------------------------------

def scatter_obs_pred(df, title, dir_out, fname):
    """Scatter plot of observed vs predicted yield, coloured by harvest year.

    Args:
        df: DataFrame with columns:
            "Observed Yield (tn per ha)", "Predicted Yield (tn per ha)", "Harvest Year"
        title: Plot title / annotation prefix
        dir_out: pathlib.Path output directory (created if missing)
        fname: output filename (e.g. "scatter_malawi_maize.png")
    """
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

    obs_col  = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"
    year_col = "Harvest Year"

    df = df.dropna(subset=[obs_col, pred_col]).copy()
    if len(df) < 2:
        return

    y_obs  = df[obs_col].astype(float)
    y_pred = df[pred_col].astype(float)
    years  = pd.to_numeric(df[year_col], errors="coerce") if year_col in df.columns else None

    cmap_y = plt.cm.viridis
    if years is not None and years.notna().any():
        norm   = plt.Normalize(vmin=years.min(), vmax=years.max())
        colors = [cmap_y(norm(y)) for y in years]
    else:
        colors = "steelblue"
        norm   = None

    rmse = np.sqrt(mean_squared_error(y_obs, y_pred))
    mape = mean_absolute_percentage_error(y_obs, y_pred)
    r2   = r2_score(y_obs, y_pred)

    try:
        with plt.style.context("science"):
            fig, ax = plt.subplots(figsize=(7, 5))
    except OSError:
        fig, ax = plt.subplots(figsize=(7, 5))

    ax.grid(True, linestyle="--", alpha=0.5)
    ax.scatter(y_obs, y_pred, color=colors, s=40, zorder=3)

    max_val = max(y_obs.max(), y_pred.max()) * 1.1
    ax.plot([0, max_val], [0, max_val], color="gray", linestyle="--", linewidth=0.8)
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)

    ax.annotate(
        f"RMSE: {rmse:.2f} tn/ha\nMAPE: {mape:.2%}\n$r^2$: {r2:.2f}\nN: {len(df)}",
        xy=(0.05, 0.95), xycoords="axes fraction",
        fontsize=9, verticalalignment="top",
    )
    ax.set_xlabel("Observed Yield (tn/ha)")
    ax.set_ylabel("Predicted Yield (tn/ha)")
    ax.set_title(title, fontsize=10)

    if norm is not None:
        sm = plt.cm.ScalarMappable(cmap=cmap_y, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, aspect=40, pad=0.02)
        cbar.set_label("Harvest Year")
        ticks = np.linspace(years.min(), years.max(), 5, dtype=int)
        cbar.set_ticks(ticks)
        cbar.ax.set_yticklabels([str(t) for t in ticks])

    plt.tight_layout()
    Path(dir_out).mkdir(parents=True, exist_ok=True)
    fig.savefig(Path(dir_out) / fname, dpi=250, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# MAPE bar chart
# ---------------------------------------------------------------------------

def mape_bar_chart(df, title, dir_out, fname):
    """Horizontal bar chart of mean MAPE by region, sorted ascending.

    Args:
        df: DataFrame with columns: "Region", "MAPE"
        title: Plot title
        dir_out: pathlib.Path output directory
        fname: output filename
    """
    if df.empty or "MAPE" not in df.columns or "Region" not in df.columns:
        return

    df_plot = (
        df.groupby("Region")["MAPE"]
        .mean()
        .sort_values(ascending=True)
    )
    if df_plot.empty:
        return

    fig, ax = plt.subplots(figsize=(8, max(3, len(df_plot) * 0.35)))
    bars = ax.barh(df_plot.index, df_plot.values, color="steelblue")
    for bar, val in zip(bars, df_plot.values):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=8)

    ax.set_xlabel("MAPE (%)")
    ax.set_title(title, fontsize=10, fontweight="bold")
    plt.tight_layout()
    Path(dir_out).mkdir(parents=True, exist_ok=True)
    fig.savefig(Path(dir_out) / fname, dpi=250, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# MAPE choropleth map
# ---------------------------------------------------------------------------

def mape_choropleth(dg, df, countries, annotate_regions, dir_out, fname):
    """Choropleth map of MAPE by region using plot.plot_map().

    Args:
        dg: GeoDataFrame of boundaries
        df: DataFrame with columns: "Country Region" (lowercase), "Mean Absolute Percentage Error"
        countries: list of display-format country names (title-cased, spaces)
        annotate_regions: bool
        dir_out: pathlib.Path output directory
        fname: output filename
    """
    import palettable as pal
    from . import plot

    col = "Mean Absolute Percentage Error"
    if df.empty or col not in df.columns:
        return

    df = df.copy()
    df.loc[df[col] > 100, col] = np.nan

    if df[col].dropna().empty:
        return

    Path(dir_out).mkdir(parents=True, exist_ok=True)
    plot.plot_map(
        dg,
        df,
        merge_col="Country Region",
        name_country=countries,
        name_col=col,
        dir_out=dir_out,
        fname=fname,
        label="MAPE (%)",
        vmin=0,
        vmax=df[col].quantile(0.95) if df[col].dropna().shape[0] > 1 else df[col].max(),
        cmap=pal.scientific.sequential.Bamako_20_r,
        series="sequential",
        annotate_regions=annotate_regions,
        loc_legend="lower left",
    )
