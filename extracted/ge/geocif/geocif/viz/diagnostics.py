"""Shared diagnostic plot functions: scatter, MAPE bar chart, MAPE choropleth map.

Used by analysis.py, yield_outlook.py, and experiments.py to avoid duplication.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

from geocif.utils import friendly_stage_label  # noqa: F401 — re-exported for callers


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
    # Compute per-column character widths from the longest cell text so
    # columns size proportionally to content. Without this, long region
    # names like "Matabeleland North/South" or "Mashonaland West (13.3%)"
    # get truncated because matplotlib defaults to equal-width columns.
    col_char_widths = []
    for j in range(n_cols):
        header_len = len(str(display_cols[j]))
        body_max = max((len(rows[i][j]) for i in range(n_rows)), default=0)
        # Pad 2 chars for breathing room
        col_char_widths.append(max(header_len, body_max) + 2)
    total_chars = max(1, sum(col_char_widths))

    # Figure width scales with total character budget at ~0.08 in/char,
    # floor at 6 in so small tables stay readable, ceiling at 18 in to
    # avoid runaway widths on huge configs.
    fig_h = max(2.0, 0.32 * (n_rows + 1))
    fig_w = max(6.0, min(18.0, 0.08 * total_chars + 1.5))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")

    table = ax.table(
        cellText=rows,
        colLabels=display_cols,
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[w / total_chars for w in col_char_widths],
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


def _draw_axis_break(ax, axis: str = "y", position: float = 100.0,
                     d: float = 0.008, gap: float = 0.014) -> None:
    """Draw `//` break marks on a spine to indicate axis clipping at ``position``.

    Two short parallel diagonals straddle the spine at the data-coordinate
    ``position``, with a white masking line behind them so the spine
    appears broken. Standard convention for visually flagging a clipped
    axis — readers see at a glance that the axis isn't linear past this
    point.

    Args:
        ax: matplotlib Axes.
        axis: 'y' (mark on left spine) or 'x' (mark on bottom spine).
        position: data-coordinate value where the axis is clipped.
        d: diagonal half-length in axes-fraction units (default 0.008).
        gap: vertical/horizontal spacing between the two parallel slashes
            (default 0.014, in axes-fraction units).

    No-op if ``position`` is outside the current axis limits.
    """
    if axis == "y":
        ymin, ymax = ax.get_ylim()
        if not (ymin < position < ymax):
            return
        y_frac = (position - ymin) / (ymax - ymin)
        # Mask the spine between the two slashes with a white line so the
        # break is visually unambiguous.
        ax.plot(
            [0, 0], [y_frac - gap, y_frac + gap],
            transform=ax.transAxes, color="white", linewidth=2.5,
            clip_on=False, zorder=8,
        )
        # Two parallel diagonals
        for y_center in (y_frac - gap / 2, y_frac + gap / 2):
            ax.plot(
                [-d, d], [y_center - d, y_center + d],
                transform=ax.transAxes, color="black", linewidth=1.2,
                clip_on=False, zorder=10, solid_capstyle="round",
            )
    elif axis == "x":
        xmin, xmax = ax.get_xlim()
        if not (xmin < position < xmax):
            return
        x_frac = (position - xmin) / (xmax - xmin)
        ax.plot(
            [x_frac - gap, x_frac + gap], [0, 0],
            transform=ax.transAxes, color="white", linewidth=2.5,
            clip_on=False, zorder=8,
        )
        for x_center in (x_frac - gap / 2, x_frac + gap / 2):
            ax.plot(
                [x_center - d, x_center + d], [-d, d],
                transform=ax.transAxes, color="black", linewidth=1.2,
                clip_on=False, zorder=10, solid_capstyle="round",
            )


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

def scatter_obs_pred(df, title, dir_out, fname, color_by="year"):
    """Scatter plot of observed vs predicted yield.

    Args:
        df: DataFrame with columns:
            "Observed Yield (tn per ha)", "Predicted Yield (tn per ha)", "Harvest Year"
            (plus "Region" when ``color_by="region"``).
        title: Plot title / annotation prefix
        dir_out: pathlib.Path output directory (created if missing)
        fname: output filename (e.g. "scatter_malawi_maize.png")
        color_by: ``"year"`` (default) colors points by Harvest Year via a
            viridis colorbar — the right choice for multi-year scatters.
            ``"region"`` colors by Region with a categorical palette + legend —
            the right choice for per-year scatters where Harvest Year is
            constant across all points.
    """
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

    obs_col  = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"
    year_col = "Harvest Year"
    region_col = "Region"

    df = df.dropna(subset=[obs_col, pred_col]).copy()
    if len(df) < 2:
        return

    y_obs  = df[obs_col].astype(float)
    y_pred = df[pred_col].astype(float)

    use_region = (color_by == "region") and (region_col in df.columns)
    years  = pd.to_numeric(df[year_col], errors="coerce") if year_col in df.columns else None

    cmap_y = plt.cm.viridis
    norm = None
    region_colors = None  # {region -> rgba} when use_region

    if use_region:
        regions = df[region_col].astype(str).tolist()
        unique_regions = sorted(set(regions))
        n_regions = len(unique_regions)
        if n_regions <= 20:
            cat_cmap = plt.cm.get_cmap("tab20", max(n_regions, 1))
            palette = [cat_cmap(i) for i in range(n_regions)]
        else:
            import matplotlib.colors as mcolors
            stacked = np.vstack([
                plt.cm.tab20b(np.linspace(0, 1, 20)),
                plt.cm.tab20c(np.linspace(0, 1, 20)),
            ])
            palette = [stacked[i % len(stacked)] for i in range(n_regions)]
        region_colors = dict(zip(unique_regions, palette))
        colors = [region_colors[r] for r in regions]
    elif years is not None and years.notna().any():
        norm   = plt.Normalize(vmin=years.min(), vmax=years.max())
        colors = [cmap_y(norm(y)) for y in years]
    else:
        colors = "steelblue"

    rmse = np.sqrt(mean_squared_error(y_obs, y_pred))
    mape = mean_absolute_percentage_error(y_obs, y_pred)
    r2   = r2_score(y_obs, y_pred)

    try:
        with plt.style.context(["science", "no-latex"]):
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

    if region_colors is not None:
        from matplotlib.lines import Line2D
        handles = [
            Line2D([0], [0], marker="o", linestyle="",
                   markerfacecolor=c, markeredgecolor=c,
                   markersize=6, label=r)
            for r, c in region_colors.items()
        ]
        ncol = 2 if len(region_colors) > 10 else 1
        ax.legend(handles=handles, title="Region",
                  bbox_to_anchor=(1.02, 1), loc="upper left",
                  fontsize=7, title_fontsize=8, ncol=ncol,
                  frameon=False)
    elif norm is not None:
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

    import scienceplots  # noqa: F401

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

    # Conditional cap: only clip + draw // break when at least one value
    # exceeds the cap by a LARGE amount (>= 1.5x). Below that threshold
    # the bars draw naturally and the axis label stays clean — no
    # "capped at 100" suffix on plots where nothing was actually clipped.
    MAPE_CAP = 100.0
    actual_max = float(np.nanmax(df_plot.values)) if len(df_plot) else 0.0
    do_cap = actual_max > MAPE_CAP * 1.5

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(8, max(3, len(df_plot) * 0.35)))
        plotted = np.minimum(df_plot.values, MAPE_CAP) if do_cap else df_plot.values
        bars = ax.barh(df_plot.index, plotted, color="steelblue")
        for bar, val in zip(bars, df_plot.values):
            if do_cap and val > MAPE_CAP:
                ax.text(MAPE_CAP + 0.5, bar.get_y() + bar.get_height() / 2,
                        f"{val:.0f}% →", va="center", fontsize=8,
                        fontweight="bold", color="#b53b3b")
            else:
                ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                        f"{val:.1f}%", va="center", fontsize=8)
        if do_cap:
            ax.set_xlim(0, MAPE_CAP + 8)
            _draw_axis_break(ax, axis="x", position=MAPE_CAP)

        ax.set_xlabel("Mean Absolute Percentage Error (%)")
        if title:
            ax.set_title(title, fontsize=10, fontweight="bold")
        ax.tick_params(axis='y', which='minor', length=0)
        plt.tight_layout()
        Path(dir_out).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(dir_out) / fname, dpi=250, bbox_inches="tight")
        plt.close(fig)


# ---------------------------------------------------------------------------
# MAPE distribution per region (box + jitter)
# ---------------------------------------------------------------------------

def mape_box_by_region(
    df,
    title,
    dir_out,
    fname,
    *,
    mape_col: str = "MAPE",
    region_col: str = "Region",
    production_pct: dict | None = None,
    ascending: bool = True,
):
    """Horizontal box plot of MAPE per region with jittered individual points.

    Each box = distribution of MAPE for that region across all forecast
    years (median line, IQR box, 1.5×IQR whiskers). Dots = individual
    (region, year) MAPE values, jittered vertically so overlap is visible
    instead of stacking. Reveals year-to-year variability that the mean
    bar chart hides — a region with mean MAPE 25% could be a steady
    20-30% (predictable) or a bimodal 5% normal / 80% drought (volatile).

    Same MAPE_CAP=100 as mape_bar_chart; box whiskers + dots truncated at
    the cap, and per-region max annotated when > cap.
    """
    if df.empty or mape_col not in df.columns or region_col not in df.columns:
        return

    import scienceplots  # noqa: F401

    by_region: dict = {
        r: g[mape_col].dropna().values for r, g in df.groupby(region_col)
    }
    by_region = {r: v for r, v in by_region.items() if len(v) > 0}
    if not by_region:
        return

    MAPE_CAP = 100.0
    overall_max = float(max(
        (np.nanmax(v) for v in by_region.values() if len(v)),
        default=0.0,
    ))
    do_cap = overall_max > MAPE_CAP * 1.5

    if production_pct:
        order = _sort_by_production(
            list(by_region.keys()), production_pct, ascending=ascending,
        )
        if order is not None:
            keys = list(by_region.keys())
            regions_sorted = [keys[i] for i in order]
        else:
            regions_sorted = sorted(by_region.keys())
    else:
        # Sort by median MAPE ascending so best regions are at the top
        regions_sorted = sorted(
            by_region.keys(),
            key=lambda r: float(np.median(by_region[r])),
            reverse=True,
        )
    labels = (
        _label_with_pct(regions_sorted, production_pct)
        if production_pct else list(regions_sorted)
    )
    data_clipped = [
        (np.minimum(by_region[r], MAPE_CAP) if do_cap else by_region[r])
        for r in regions_sorted
    ]

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(
            figsize=(9, max(3.5, len(regions_sorted) * 0.42)),
        )
        bp = ax.boxplot(
            data_clipped, vert=False, labels=labels,
            patch_artist=True, widths=0.6, showfliers=False,
            medianprops={"color": "black", "linewidth": 1.4},
        )
        for patch in bp["boxes"]:
            patch.set_facecolor("steelblue")
            patch.set_alpha(0.35)
            patch.set_edgecolor("steelblue")

        rng = np.random.default_rng(42)
        for i, vals in enumerate(data_clipped):
            if len(vals) == 0:
                continue
            ys = (i + 1) + rng.uniform(-0.18, 0.18, size=len(vals))
            ax.scatter(
                vals, ys, s=14, color="#1f4e79", alpha=0.65,
                edgecolors="none", zorder=3,
            )

        # Annotate clipped maxima per region (only when capping is on)
        if do_cap:
            for i, r in enumerate(regions_sorted):
                rmax = float(np.max(by_region[r]))
                if rmax > MAPE_CAP:
                    ax.text(
                        MAPE_CAP + 1, i + 1, f"max={rmax:.0f}% →",
                        va="center", fontsize=7, color="#b53b3b",
                        fontweight="bold",
                    )
            ax.set_xlim(0, MAPE_CAP + 18)
            _draw_axis_break(ax, axis="x", position=MAPE_CAP)
        ax.set_xlabel("MAPE (%)")
        if title:
            ax.set_title(title, fontsize=10, fontweight="bold")
        ax.grid(True, axis="x", linestyle=":", alpha=0.4)
        ax.tick_params(axis="y", which="minor", length=0)
        plt.tight_layout()
        Path(dir_out).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(dir_out) / fname, dpi=250, bbox_inches="tight")
        plt.close(fig)


# ---------------------------------------------------------------------------
# MAPE distribution per year (box + jitter)
# ---------------------------------------------------------------------------

def mape_box_by_year(
    df,
    title,
    dir_out,
    fname,
    *,
    mape_col: str = "MAPE",
    year_col: str = "Harvest Year",
):
    """Vertical box plot of MAPE per year with jittered individual points.

    Each box = distribution of MAPE for that year across all regions. Dots
    = individual (region, year) MAPE values, jittered horizontally. Reveals
    which years are uniformly easy/hard vs which have huge cross-region
    spread (e.g. localized drought hitting one region only).

    Capped at 100; per-year max annotated when > cap.
    """
    if df.empty or mape_col not in df.columns or year_col not in df.columns:
        return

    import scienceplots  # noqa: F401

    by_year: dict = {
        int(y): g[mape_col].dropna().values for y, g in df.groupby(year_col)
    }
    by_year = {y: v for y, v in by_year.items() if len(v) > 0}
    if not by_year:
        return

    MAPE_CAP = 100.0
    years_sorted = sorted(by_year.keys())
    overall_max = float(max(
        (np.nanmax(v) for v in by_year.values() if len(v)),
        default=0.0,
    ))
    do_cap = overall_max > MAPE_CAP * 1.5
    data_clipped = [
        (np.minimum(by_year[y], MAPE_CAP) if do_cap else by_year[y])
        for y in years_sorted
    ]

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(
            figsize=(max(10, len(years_sorted) * 0.55), 5.5),
        )
        bp = ax.boxplot(
            data_clipped, vert=True,
            labels=[str(y) for y in years_sorted],
            patch_artist=True, widths=0.55, showfliers=False,
            medianprops={"color": "black", "linewidth": 1.4},
        )
        for patch in bp["boxes"]:
            patch.set_facecolor("steelblue")
            patch.set_alpha(0.35)
            patch.set_edgecolor("steelblue")

        rng = np.random.default_rng(42)
        for i, vals in enumerate(data_clipped):
            if len(vals) == 0:
                continue
            xs = (i + 1) + rng.uniform(-0.18, 0.18, size=len(vals))
            ax.scatter(
                xs, vals, s=14, color="#1f4e79", alpha=0.65,
                edgecolors="none", zorder=3,
            )

        if do_cap:
            for i, y in enumerate(years_sorted):
                ymax = float(np.max(by_year[y]))
                if ymax > MAPE_CAP:
                    ax.text(
                        i + 1, MAPE_CAP + 1.5, f"{ymax:.0f}↑",
                        ha="center", va="bottom", fontsize=7,
                        color="#b53b3b", fontweight="bold",
                    )
            ax.set_ylim(0, MAPE_CAP + 12)
            _draw_axis_break(ax, axis="y", position=MAPE_CAP)
        ax.set_ylabel("MAPE (%)")
        ax.set_xlabel("Forecast year")
        if title:
            ax.set_title(title, fontsize=10, fontweight="bold")
        ax.grid(True, axis="y", linestyle=":", alpha=0.4)
        plt.xticks(rotation=45, ha="right")
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
    obs_col: str | None = None,
    pred_col: str | None = None,
    area_col: str = "Area (ha)",
    threshold: float | None = 20.0,
):
    """Bar chart of MAPE per year with optional dashed reference line.

    When ``obs_col``, ``pred_col``, and ``area_col`` are all present in
    ``df``, the bars show the **area-weighted national MAPE** per year
    (sum of yield*area per year aggregated to a national observed and
    predicted, then |err|/obs * 100).  Matches the National line in
    `_plot_metric_progression` so the two diagnostic plots reconcile.

    Otherwise falls back to the legacy unweighted mean of ``mape_col``.
    """
    if df.empty or year_col not in df.columns:
        return

    import scienceplots  # noqa: F401

    use_national = (
        obs_col is not None and pred_col is not None
        and obs_col in df.columns and pred_col in df.columns
        and area_col in df.columns and df[area_col].notna().any()
    )

    if use_national:
        d = df.dropna(subset=[obs_col, pred_col, area_col]).copy()
        d = d[d[obs_col] != 0]
        d["_prod_obs"] = d[obs_col] * d[area_col]
        d["_prod_pred"] = d[pred_col] * d[area_col]
        nat = d.groupby(year_col).agg(
            _prod_obs=("_prod_obs", "sum"),
            _prod_pred=("_prod_pred", "sum"),
            _area=(area_col, "sum"),
        )
        nat = nat[nat["_area"] > 0]
        if nat.empty:
            return
        nat["_obs_nat"] = nat["_prod_obs"] / nat["_area"]
        nat["_pred_nat"] = nat["_prod_pred"] / nat["_area"]
        mape_series = (
            (nat["_pred_nat"] - nat["_obs_nat"]).abs()
            / nat["_obs_nat"] * 100
        ).sort_index()
    else:
        if mape_col not in df.columns:
            return
        mape_series = df.groupby(year_col)[mape_col].mean().sort_index()

    if mape_series.empty:
        return

    # 5-year moving-window mean.  Require a full window (min_periods=
    # rolling_window) so the leading years don't show misleading averages
    # of 1-4 years.  Matplotlib skips NaN points; the line starts at the
    # first year where 5 prior years are available.
    rolling_window = 5
    mape_rolling = mape_series.rolling(
        window=rolling_window, min_periods=rolling_window
    ).mean()

    with plt.style.context(["science", "no-latex"]):
        MAPE_CAP = 100.0
        actual_max = float(np.nanmax(mape_series.values))
        do_cap = actual_max > MAPE_CAP * 1.5

        fig, ax = plt.subplots(figsize=(10, 6))
        x_labels = [str(int(y)) for y in mape_series.index]
        bar_vals = (
            np.minimum(mape_series.values, MAPE_CAP) if do_cap
            else mape_series.values
        )
        bars = ax.bar(x_labels, bar_vals, color="steelblue")
        if do_cap:
            for bar, val in zip(bars, mape_series.values):
                if val > MAPE_CAP:
                    ax.text(bar.get_x() + bar.get_width() / 2,
                            MAPE_CAP + 1.5,
                            f"{val:.0f}%↑", ha="center", va="bottom",
                            fontsize=8, fontweight="bold", color="#b53b3b")
        if threshold is not None:
            ax.axhline(y=threshold, color="gray", linestyle="--")
        rolling_clip = (
            np.minimum(mape_rolling.values, MAPE_CAP) if do_cap
            else mape_rolling.values
        )
        ax.plot(
            x_labels, rolling_clip,
            color="darkorange", linewidth=2, marker="o", markersize=4,
            label=f"{rolling_window}-yr moving avg", zorder=3,
        )
        if do_cap:
            ax.set_ylim(0, MAPE_CAP + 8)
            _draw_axis_break(ax, axis="y", position=MAPE_CAP)
        ax.legend(loc="upper right", fontsize=8, frameon=False)
        ax.set_xlabel("")
        _ylabel = (
            f"{mape_col} (%)" if mape_col != "MAPE"
            else "Mean Absolute Percentage Error (%)"
        )
        ax.set_ylabel(_ylabel)
        if title:
            ax.set_title(title, fontsize=10, fontweight="bold")
        ax.tick_params(axis='x', which='minor', length=0)
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
        label="Mean Absolute Percentage Error (%)",
        vmin=0,
        vmax=df[col].quantile(0.95) if df[col].dropna().shape[0] > 1 else df[col].max(),
        cmap=pal.scientific.sequential.Bamako_20_r,
        series="sequential",
        annotate_regions=annotate_regions,
        loc_legend="lower left",
    )
