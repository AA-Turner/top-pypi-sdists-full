"""Shared diagnostic plot functions: scatter, MAPE bar chart, MAPE choropleth map.

Used by analysis.py, yield_outlook.py, and experiments.py to avoid duplication.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Forest plot: predicted yield with CI, optional reference markers
# ---------------------------------------------------------------------------

def yield_table(
    df: pd.DataFrame,
    out_path: Path,
    *,
    title: str,
    region_col: str = "Region",
    columns: list | None = None,
    float_fmt: str = "{:.2f}",
    font_size: int = 10,
) -> bool:
    """Render a tabular PNG summarizing per-region yield forecasts.

    ``df`` must be pre-ordered how the table should read top-to-bottom.
    ``columns`` is a list of display columns after ``region_col`` (e.g.
    ``["Predicted Yield", "Median Yield (2021-2025)", "lower CI", "upper CI"]``);
    defaults to every column in ``df`` other than ``region_col``.
    """
    if df.empty:
        return False
    if columns is None:
        columns = [c for c in df.columns if c != region_col]

    display_cols = [region_col] + list(columns)
    rows = []
    for _, r in df.iterrows():
        row = [str(r[region_col])]
        for c in columns:
            v = r[c]
            if pd.isna(v):
                row.append("")
            elif isinstance(v, (int, np.integer)):
                row.append(str(int(v)))
            elif isinstance(v, (float, np.floating)):
                row.append(float_fmt.format(v))
            else:
                row.append(str(v))
        rows.append(row)

    n_rows = len(rows)
    n_cols = len(display_cols)
    fig_h = max(2.0, 0.32 * (n_rows + 1))
    fig_w = max(6.0, 1.4 * n_cols)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")

    table = ax.table(
        cellText=rows,
        colLabels=display_cols,
        cellLoc="center",
        colLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    table.scale(1, 1.2)

    # Bold + shaded header row
    for j in range(n_cols):
        cell = table[(0, j)]
        cell.set_text_props(weight="bold")
        cell.set_facecolor("#e8eef7")

    # First column (region names) left-aligned + shaded; zebra body rows
    for i in range(1, n_rows + 1):
        table[(i, 0)].set_text_props(ha="left")
        table[(i, 0)].PAD = 0.02
        bg = "#ffffff" if i % 2 else "#f7f7f7"
        for j in range(n_cols):
            table[(i, j)].set_facecolor(bg)

    if title:
        ax.set_title(title, fontsize=font_size + 1, fontweight="bold", pad=6)
    plt.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=250, bbox_inches="tight")
    plt.close(fig)
    return True


def _sort_by_production(region_names, prod_pct, ascending: bool = True):
    """Return the order indices that sort ``region_names`` by production share.
    Returns None if ``prod_pct`` is empty (caller should skip ordering)."""
    if not prod_pct:
        return None
    shares = np.array([prod_pct.get(r, 0) for r in region_names])
    order = np.argsort(shares)
    return order if ascending else order[::-1]


def _label_with_pct(region_names, prod_pct):
    """Append ``(X.Y%)`` production-share suffix to each region label."""
    return [f"{r} ({prod_pct.get(r, 0):.1f}%)" for r in region_names]


def forest_yield_ci(
    df: pd.DataFrame,
    predicted_col: str,
    out_path: Path,
    *,
    title: str,
    region_col: str = "Region",
    lower_ci_col: str = "lower CI",
    upper_ci_col: str = "upper CI",
    reference_df: pd.DataFrame | None = None,
    reference_value_col: str = "Observed Yield (tn per ha)",
    reference_group_col: str | None = None,
    reference_label: str = "Observed",
    reference_cmap: str = "tab10",
    production_pct: dict | None = None,
) -> bool:
    """Horizontal forest plot: steelblue error bars per region + diamond markers.

    Reference modes:
    - Single-color (default): ``reference_group_col=None`` → black markers,
      one legend entry using ``reference_label``.
    - Color-by-group: ``reference_group_col`` set → one color per unique
      group value (from ``reference_cmap``), one legend entry per group.

    When ``production_pct`` is supplied, rows are reordered so the largest
    producer sits at the top of the plot and region labels are suffixed
    with ``(X.Y%)``.  Otherwise ``df`` is used as-passed (caller sorts).

    ``df`` must contain ``region_col``, ``predicted_col``, ``lower_ci_col``,
    ``upper_ci_col``.  Returns False if CI columns are missing or empty.
    """
    if lower_ci_col not in df.columns or upper_ci_col not in df.columns:
        logger.warning(f"forest_yield_ci: CI columns missing, skipping {out_path.name}")
        return False
    df = df.dropna(subset=[lower_ci_col, upper_ci_col])
    if df.empty:
        logger.warning(f"forest_yield_ci: no rows with CI data, skipping {out_path.name}")
        return False

    # Optional production-share ordering — ascending on the df so the last
    # row (largest producer) renders at the top of the horizontal plot.
    if production_pct:
        order = _sort_by_production(df[region_col].tolist(), production_pct, ascending=True)
        if order is not None:
            df = df.iloc[order].reset_index(drop=True)
        display_labels = _label_with_pct(df[region_col].tolist(), production_pct)
    else:
        display_labels = df[region_col].tolist()

    fig, ax = plt.subplots(figsize=(8, max(4, len(df) * 0.4)))
    y = np.arange(len(df))

    xerr_low = df[predicted_col].values - df[lower_ci_col].values
    xerr_high = df[upper_ci_col].values - df[predicted_col].values
    ax.errorbar(
        df[predicted_col].values, y,
        xerr=[xerr_low, xerr_high],
        fmt="o", color="steelblue", capsize=3, label="Predicted \u00b1 CI",
    )

    if reference_df is not None and not reference_df.empty:
        region_to_y = {r: i for i, r in enumerate(df[region_col].values)}

        if reference_group_col is None:
            ref = reference_df[reference_df[region_col].isin(region_to_y)]
            y_ref = ref[region_col].map(region_to_y).values
            ax.scatter(
                ref[reference_value_col].values, y_ref,
                marker="D", color="black", s=25, alpha=0.7, zorder=5,
                label=reference_label,
            )
        else:
            groups = sorted(reference_df[reference_group_col].dropna().unique())
            cmap = plt.get_cmap(reference_cmap)
            for i, g in enumerate(groups):
                sub = reference_df[reference_df[reference_group_col] == g]
                sub = sub[sub[region_col].isin(region_to_y)]
                if sub.empty:
                    continue
                y_ref = sub[region_col].map(region_to_y).values
                color = cmap(i % 10) if reference_cmap == "tab10" else cmap(i / max(1, len(groups) - 1))
                ax.scatter(
                    sub[reference_value_col].values, y_ref,
                    marker="D", color=color, s=25, alpha=0.8, zorder=5,
                    label=str(int(g) if isinstance(g, (int, np.integer, float)) and float(g).is_integer() else g),
                )

    ax.set_yticks(list(y))
    ax.set_yticklabels(display_labels, fontsize=8)
    ax.set_xlabel("Yield (tn per ha)")
    ax.set_title(title, fontsize=11, fontweight="bold")

    handles, labels = ax.get_legend_handles_labels()
    ncol = 2 if len(labels) >= 6 else 1
    ax.legend(handles, labels, fontsize=8, loc="lower right", ncol=ncol)
    plt.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=250)
    plt.close(fig)
    return True


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

def _compute_share_pct(
    df: pd.DataFrame,
    country: str,
    value_series: pd.Series,
    *,
    country_col: str = "Country",
    region_col: str = "Region",
    year_col: str = "Harvest Year",
    n_years: int = 5,
) -> dict:
    """Shared core: return {region -> % share} of ``value_series`` summed per
    total over the last ``n_years`` mean.  ``value_series`` must align to
    the rows of ``df`` (same index)."""
    df_c = df[df[country_col] == country].copy()
    if df_c.empty:
        return {}
    df_c["_val"] = value_series.loc[df_c.index]
    df_c = df_c.dropna(subset=["_val", year_col])
    if df_c.empty:
        return {}

    last_years = sorted(df_c[year_col].unique())[-n_years:]
    df_c = df_c[df_c[year_col].isin(last_years)]

    mean_by_region = df_c.groupby(region_col)["_val"].mean()
    total = mean_by_region.sum()
    if total <= 0:
        return {}
    return (mean_by_region / total * 100).to_dict()


def compute_production_pct(
    df: pd.DataFrame, country: str, *,
    area_col: str = "Area (ha)",
    obs_col: str = "Observed Yield (tn per ha)",
    **kwargs,
) -> dict:
    """Region -> % share of national production (area * observed yield),
    last ``n_years`` mean.  Empty dict if required columns missing."""
    if area_col not in df.columns or obs_col not in df.columns:
        return {}
    return _compute_share_pct(df, country, df[area_col] * df[obs_col], **kwargs)


def compute_area_pct(
    df: pd.DataFrame, country: str, *,
    area_col: str = "Area (ha)",
    **kwargs,
) -> dict:
    """Region -> % share of national crop area, last ``n_years`` mean.
    Empty dict if ``area_col`` missing."""
    if area_col not in df.columns:
        return {}
    return _compute_share_pct(df, country, df[area_col], **kwargs)


def mape_bar_chart(
    df,
    title,
    dir_out,
    fname,
    *,
    production_pct: dict | None = None,
    ascending: bool = True,
):
    """Horizontal bar chart of mean MAPE by region.

    Default: sorted ascending by MAPE (best regions at top).

    If ``production_pct`` is provided, regions are sorted by production
    share with ``ascending=True`` (smallest producer at top, largest at
    bottom — convention used in experiments.py so horizontal bar charts
    read bottom-up for descending production). Region labels are suffixed
    with ``(X.Y%)``.

    Args:
        df: DataFrame with columns "Region", "MAPE".
        title: Plot title.
        dir_out: output directory.
        fname: output filename.
        production_pct: optional {region -> % share} dict.
        ascending: sort direction for production-share sort.
    """
    if df.empty or "MAPE" not in df.columns or "Region" not in df.columns:
        return

    df_plot = df.groupby("Region")["MAPE"].mean()
    if df_plot.empty:
        return

    if production_pct:
        order = _sort_by_production(df_plot.index.tolist(), production_pct, ascending=ascending)
        if order is not None:
            df_plot = df_plot.iloc[order]
        df_plot.index = _label_with_pct(df_plot.index, production_pct)
    else:
        df_plot = df_plot.sort_values(ascending=True)

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
# MAPE by year
# ---------------------------------------------------------------------------

def mape_by_year(
    df,
    title,
    dir_out,
    fname,
    *,
    year_col: str = "Harvest Year",
    mape_col: str = "MAPE",
    threshold: float | None = 20.0,
):
    """Bar chart of mean MAPE per year with optional dashed reference line.

    Args:
        df: DataFrame with ``year_col`` and ``mape_col``.
        title: Plot title (pass empty string to suppress).
        dir_out: output directory.
        fname: output filename.
        year_col: name of the year column.
        mape_col: name of the MAPE column (e.g. ``"MAPE"`` or
            ``"Mean Absolute Percentage Error"``).
        threshold: y-value for horizontal reference line (default 20.0).
            Set to None to omit.
    """
    if df.empty or year_col not in df.columns or mape_col not in df.columns:
        return

    mape_series = df.groupby(year_col)[mape_col].mean().sort_index()
    if mape_series.empty:
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        [str(int(y)) for y in mape_series.index],
        mape_series.values,
        color="steelblue",
    )
    if threshold is not None:
        ax.axhline(y=threshold, color="gray", linestyle="--")
    ax.set_xlabel("")
    ax.set_ylabel(f"{mape_col} (%)" if mape_col != "MAPE" else "MAPE (%)")
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold")
    plt.xticks(rotation=0)
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
