"""Shared diagnostic plot functions: scatter, MAPE bar chart, MAPE choropleth map.

Used by analysis.py, yield_outlook.py, and experiments.py to avoid duplication.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

from geocif.utils import friendly_stage_label, greedy_dedup_by_mutual_corr  # noqa: F401 — re-exported for callers


# scienceplots registers the "science" matplotlib style we use for the
# publication-quality diagnostic plots (forest_yield_ci, mape_bar_chart,
# mape_box_by_region, mape_choropleth, etc.). It's broken on matplotlib
# 3.11+ because matplotlib removed the `matplotlib.style.core` submodule
# that scienceplots imports from. Until upstream catches up, fail soft:
# log once at import time, then fall back to matplotlib's default style
# inside ``_science_style_context`` so the diagnostic plots still
# produce — just with default fonts/colours instead of the "science"
# theme.
try:
    import scienceplots  # noqa: F401
    _HAS_SCIENCE_STYLE = True
except (ImportError, AttributeError) as _exc:
    _HAS_SCIENCE_STYLE = False
    logger.warning(
        f"scienceplots unavailable ({type(_exc).__name__}: {_exc}); "
        f"diagnostic plots will use matplotlib default style"
    )


def _science_style_context():
    """Return a matplotlib style context manager that uses the
    'science' + 'no-latex' theme when scienceplots is available, else
    matplotlib's default style. Use in place of
    ``plt.style.context(['science', 'no-latex'])`` so the diagnostic
    plot functions stay agnostic to whether scienceplots loaded.
    """
    if _HAS_SCIENCE_STYLE:
        return plt.style.context(["science", "no-latex"])
    return plt.style.context("default")


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


# ---------------------------------------------------------------------------
# Production-share DISPLAY toggle.
#
# Process-wide switch for whether a region's production share (its "(X.Y%)"
# label suffix, "% of Production" column, "% of national production" caption,
# etc.) is SHOWN on figures/reports. Set once per run by the driver via
# ``set_show_production_share(...)`` and read by every display site. Ordering
# regions by production (``_sort_by_production``) is deliberately NOT affected
# — only the displayed value is hidden. Defaults to True so any project that
# doesn't set the flag keeps its current output byte-for-byte.
#
# Rationale: for crops whose area statistics don't match the model's region
# scheme (e.g. Afghanistan poppy, where "Southern" isn't split into the newer
# "South-Western" region), the share is misleading and is suppressed via
# ``[ML] show_production_share = False`` in that project's geocif.txt.
# ---------------------------------------------------------------------------
_SHOW_PRODUCTION_SHARE = True


def show_production_share_from_parser(parser) -> bool:
    """Read ``[ML] show_production_share`` (default True) from a config parser."""
    try:
        return parser.getboolean("ML", "show_production_share", fallback=True)
    except Exception:
        return True


def set_show_production_share(flag: bool) -> None:
    """Set the process-wide production-share display toggle (call once per run)."""
    global _SHOW_PRODUCTION_SHARE
    _SHOW_PRODUCTION_SHARE = bool(flag)


def is_production_share_shown() -> bool:
    """Whether production share should be displayed on figures/reports."""
    return _SHOW_PRODUCTION_SHARE


def _sort_by_production(region_names, prod_pct, ascending: bool = True):
    """Return the order indices that sort ``region_names`` by production share.
    Returns None if ``prod_pct`` is empty (caller should skip ordering)."""
    if not prod_pct:
        return None
    shares = np.array([prod_pct.get(r, 0) for r in region_names])
    order = np.argsort(shares)
    return order if ascending else order[::-1]


def _label_with_pct(region_names, prod_pct):
    """Append ``(X.Y%)`` production-share suffix to each region label.

    Returns plain region names (no suffix) when production-share display is
    disabled via ``set_show_production_share(False)`` — callers keep any
    production-based ordering, they just don't show the value.
    """
    if not _SHOW_PRODUCTION_SHARE:
        return list(region_names)
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

def scatter_obs_pred(df, title, dir_out, fname, color_by="year", yield_units="Mg/ha"):
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
        with _science_style_context():
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
        f"RMSE: {rmse:.2f} {yield_units}\nMAPE: {mape:.2%}\n$r^2$: {r2:.2f}\nN: {len(df)}",
        xy=(0.05, 0.95), xycoords="axes fraction",
        fontsize=9, verticalalignment="top",
    )
    ax.set_xlabel(f"Observed Yield ({yield_units})")
    ax.set_ylabel(f"Predicted Yield ({yield_units})")
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
# Trigger-Evaluation plot (insurance-style 2×2 confusion on a yield scatter)
# ---------------------------------------------------------------------------

def _compute_trigger_confusion(df, threshold, obs_col, pred_col, year_col):
    """Return a per-year + ALL confusion-summary DataFrame.

    Quadrants are formed by `threshold` on BOTH axes:
      * correct_payout   : obs<t  AND pred<t   (predicted loss, actual loss)
      * correct_nopay    : obs>=t AND pred>=t  (predicted ok, actual ok)
      * missed_payout    : obs<t  AND pred>=t  (real loss, no trigger fired)
      * false_payout     : obs>=t AND pred<t   (trigger fired, no actual loss)

    Rates:
      * miss_rate_%         = missed_payout / n_low_yield     (recall miss)
      * false_payout_rate_% = false_payout  / (n - n_low_yield)
      * accuracy_%          = (correct_payout + correct_nopay) / n
    """
    def _row(label, sub):
        n = len(sub)
        if n == 0:
            return None
        obs_low = sub[obs_col] < threshold
        pred_low = sub[pred_col] < threshold
        n_low = int(obs_low.sum())
        n_nolow = n - n_low
        cp = int((obs_low & pred_low).sum())
        cn = int((~obs_low & ~pred_low).sum())
        mp = int((obs_low & ~pred_low).sum())
        fp = int((~obs_low & pred_low).sum())
        return {
            "period": label,
            "n": n,
            "n_low_yield": n_low,
            "correct_payout": cp,
            "correct_nopay": cn,
            "missed_payout": mp,
            "false_payout": fp,
            "miss_rate_%": round(100.0 * mp / n_low) if n_low else 0,
            "false_payout_rate_%": round(100.0 * fp / n_nolow) if n_nolow else 0,
            "accuracy_%": round(100.0 * (cp + cn) / n),
        }

    rows = []
    all_row = _row("ALL", df)
    if all_row is not None:
        rows.append(all_row)
    if year_col in df.columns:
        for yr in sorted(df[year_col].dropna().unique()):
            sub = df[df[year_col] == yr]
            r = _row(str(int(yr)), sub)
            if r is not None:
                rows.append(r)
    return pd.DataFrame(rows)


def trigger_eval_plot(
    df,
    title,
    dir_out,
    fname,
    *,
    threshold: float = 18.9,
    yield_units: str = "Mg/ha",
    year_col: str = "Harvest Year",
):
    """Trigger-evaluation scatter (index-insurance 2×2) + confusion summary.

    Reuses the standard ``Observed Yield (tn per ha)`` / ``Predicted Yield
    (tn per ha)`` column names (DataFrame internal contract; same as
    ``scatter_obs_pred``). The ``yield_units`` string is purely for display.

    Returns the per-year confusion DataFrame so the caller can save it
    alongside the PNG.
    """
    from matplotlib.patches import Rectangle

    obs_col = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"

    df = df.dropna(subset=[obs_col, pred_col]).copy()
    if len(df) < 2:
        return pd.DataFrame()

    y_obs = df[obs_col].astype(float)
    y_pred = df[pred_col].astype(float)

    # Per-year coloring (viridis); falls back to steelblue if no year col
    years = pd.to_numeric(df[year_col], errors="coerce") if year_col in df.columns else None
    if years is not None and years.notna().any():
        cmap = plt.cm.viridis
        norm = plt.Normalize(vmin=years.min(), vmax=years.max())
        colors = [cmap(norm(y)) for y in years]
    else:
        colors = "steelblue"

    confusion = _compute_trigger_confusion(df, threshold, obs_col, pred_col, year_col)

    try:
        with _science_style_context():
            fig, ax = plt.subplots(figsize=(7, 5.5))
    except OSError:
        fig, ax = plt.subplots(figsize=(7, 5.5))

    axis_max = max(y_obs.max(), y_pred.max(), threshold) * 1.1
    ax.set_xlim(0, axis_max)
    ax.set_ylim(0, axis_max)

    # Shade the two error quadrants (drawn first so they sit behind everything else).
    # Pink top-left: missed payout (obs<t & pred>=t).
    ax.add_patch(Rectangle((0, threshold), threshold, axis_max - threshold,
                           facecolor="#f4c2c2", alpha=0.35, zorder=0,
                           edgecolor="none"))
    # Yellow bottom-right: false payout (obs>=t & pred<t).
    ax.add_patch(Rectangle((threshold, 0), axis_max - threshold, threshold,
                           facecolor="#fdf5b9", alpha=0.55, zorder=0,
                           edgecolor="none"))

    # Diagonal 1:1 reference + threshold cross-hair
    ax.plot([0, axis_max], [0, axis_max], color="gray", linestyle="-",
            linewidth=0.8, zorder=1)
    ax.axhline(threshold, color="red", linestyle="--", linewidth=0.9, zorder=2)
    ax.axvline(threshold, color="red", linestyle="--", linewidth=0.9, zorder=2)

    ax.scatter(y_obs, y_pred, color=colors, s=24, zorder=3)

    # "False payout" annotation centered in the yellow region. Pink region
    # is self-evident (top-left), label is omitted to avoid clutter.
    ax.annotate(
        "False\npayout",
        xy=((threshold + axis_max) / 2, threshold / 2),
        ha="center", va="center", fontsize=8, color="#7a6500",
        zorder=4,
    )

    ax.set_xlabel(f"Observed yield ({yield_units})")
    ax.set_ylabel(f"Predicted yield ({yield_units})")
    full_title = (
        f"{title} (threshold = {threshold:g} {yield_units})"
        if title else f"Trigger Evaluation (threshold = {threshold:g} {yield_units})"
    )
    ax.set_title(full_title, fontsize=10)

    # Year legend (small, top-left of plot) when years available.
    if years is not None and years.notna().any():
        from matplotlib.lines import Line2D
        uniq_years = sorted({int(y) for y in years.dropna()})
        if len(uniq_years) <= 12:
            handles = [
                Line2D([0], [0], marker="o", linestyle="",
                       markerfacecolor=cmap(norm(y)),
                       markeredgecolor="none", markersize=5, label=str(y))
                for y in uniq_years
            ]
            ax.legend(handles=handles, title="year", loc="upper left",
                      fontsize=7, title_fontsize=7, frameon=True,
                      framealpha=0.8)

    plt.tight_layout()
    Path(dir_out).mkdir(parents=True, exist_ok=True)
    fig.savefig(Path(dir_out) / fname, dpi=250, bbox_inches="tight")
    plt.close(fig)

    return confusion


def trigger_eval_table_image(df_confusion, title, dir_out, fname):
    """Render the trigger-evaluation confusion-summary DataFrame as a PNG.

    Companion to :func:`trigger_eval_plot` — same data the CSV carries,
    rendered as a quick-glance image for slide decks / shared review.

    Layout: matplotlib ``ax.table`` with a bold header row, a highlighted
    ALL row (first row), and alternating row stripes for readability.
    """
    if df_confusion is None or df_confusion.empty:
        return

    col_labels = list(df_confusion.columns)
    cell_text = [
        [
            f"{v}" if not (isinstance(v, float) and not v.is_integer())
            else f"{v:.1f}"
            for v in row
        ]
        for row in df_confusion.itertuples(index=False, name=None)
    ]

    n_rows = len(cell_text)
    fig_h = max(2.5, 0.32 * n_rows + 1.2)
    fig_w = 0.85 * len(col_labels) + 1.5
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")

    table = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        cellLoc="center",
        colLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.0, 1.4)
    table.auto_set_column_width(col=list(range(len(col_labels))))

    # Header: bold, light-gray background
    for j in range(len(col_labels)):
        cell = table[0, j]
        cell.set_facecolor("#dcdcdc")
        cell.set_text_props(weight="bold")

    # Data rows: highlight ALL (row 1 of the matplotlib table — first data row);
    # alternate stripes for the rest.
    for r in range(1, n_rows + 1):
        is_all_row = (r == 1)
        for j in range(len(col_labels)):
            cell = table[r, j]
            if is_all_row:
                cell.set_facecolor("#f0f0f0")
                cell.set_text_props(weight="bold")
            elif r % 2 == 1:
                cell.set_facecolor("#fafafa")

    if title:
        ax.set_title(title, fontsize=10, pad=10, fontweight="bold")

    plt.tight_layout()
    Path(dir_out).mkdir(parents=True, exist_ok=True)
    fig.savefig(Path(dir_out) / fname, dpi=200, bbox_inches="tight")
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

    # Conditional cap: only clip + draw // break when at least one value
    # exceeds the cap by a LARGE amount (>= 1.5x). Below that threshold
    # the bars draw naturally and the axis label stays clean — no
    # "capped at 100" suffix on plots where nothing was actually clipped.
    MAPE_CAP = 100.0
    actual_max = float(np.nanmax(df_plot.values)) if len(df_plot) else 0.0
    do_cap = actual_max > MAPE_CAP * 1.5

    with _science_style_context():
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

    with _science_style_context():
        fig, ax = plt.subplots(
            figsize=(9, max(3.5, len(regions_sorted) * 0.42)),
        )
        bp = ax.boxplot(
            data_clipped, vert=False, tick_labels=labels,
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

    with _science_style_context():
        fig, ax = plt.subplots(
            figsize=(max(10, len(years_sorted) * 0.55), 5.5),
        )
        bp = ax.boxplot(
            data_clipped, vert=True,
            tick_labels=[str(y) for y in years_sorted],
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
                        i + 1, MAPE_CAP + 1.5, f"{ymax:.0f}",
                        ha="center", va="bottom", rotation=90, fontsize=7,
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

    with _science_style_context():
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
                            f"{val:.0f}", ha="center", va="bottom",
                            rotation=90,
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
# RMSE variants (Mg/ha, natural units, no percentage cap)
# ---------------------------------------------------------------------------

def rmse_box_by_region(
    df,
    title,
    dir_out,
    fname,
    *,
    rmse_col: str = "RMSE",
    region_col: str = "Region",
    production_pct: dict | None = None,
    ascending: bool = True,
):
    """Horizontal box plot of RMSE (Mg/ha) per region — RMSE twin of
    ``mape_box_by_region``. Same sort logic, no percentage cap.
    """
    if df.empty or rmse_col not in df.columns or region_col not in df.columns:
        return
    by_region: dict = {
        r: g[rmse_col].dropna().values for r, g in df.groupby(region_col)
    }
    by_region = {r: v for r, v in by_region.items() if len(v) > 0}
    if not by_region:
        return

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
        regions_sorted = sorted(
            by_region.keys(),
            key=lambda r: float(np.median(by_region[r])),
            reverse=True,
        )
    labels = (
        _label_with_pct(regions_sorted, production_pct)
        if production_pct else list(regions_sorted)
    )
    data = [by_region[r] for r in regions_sorted]

    with _science_style_context():
        fig, ax = plt.subplots(
            figsize=(9, max(3.5, len(regions_sorted) * 0.42)),
        )
        bp = ax.boxplot(
            data, vert=False, tick_labels=labels,
            patch_artist=True, widths=0.6, showfliers=False,
            medianprops={"color": "black", "linewidth": 1.4},
        )
        for patch in bp["boxes"]:
            patch.set_facecolor("steelblue")
            patch.set_alpha(0.35)
            patch.set_edgecolor("steelblue")

        rng = np.random.default_rng(42)
        for i, vals in enumerate(data):
            if len(vals) == 0:
                continue
            ys = (i + 1) + rng.uniform(-0.18, 0.18, size=len(vals))
            ax.scatter(
                vals, ys, s=14, color="#1f4e79", alpha=0.65,
                edgecolors="none", zorder=3,
            )
        ax.set_xlabel("RMSE (Mg/ha)")
        if title:
            ax.set_title(title, fontsize=10, fontweight="bold")
        ax.grid(True, axis="x", linestyle=":", alpha=0.4)
        ax.tick_params(axis="y", which="minor", length=0)
        plt.tight_layout()
        Path(dir_out).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(dir_out) / fname, dpi=250, bbox_inches="tight")
        plt.close(fig)


def rmse_box_by_year(
    df,
    title,
    dir_out,
    fname,
    *,
    rmse_col: str = "RMSE",
    year_col: str = "Harvest Year",
):
    """Vertical box plot of RMSE per year — RMSE twin of
    ``mape_box_by_year``. No percentage cap.
    """
    if df.empty or rmse_col not in df.columns or year_col not in df.columns:
        return
    by_year: dict = {
        int(y): g[rmse_col].dropna().values for y, g in df.groupby(year_col)
    }
    by_year = {y: v for y, v in by_year.items() if len(v) > 0}
    if not by_year:
        return

    years_sorted = sorted(by_year.keys())
    data = [by_year[y] for y in years_sorted]

    with _science_style_context():
        fig, ax = plt.subplots(
            figsize=(max(10, len(years_sorted) * 0.55), 5.5),
        )
        bp = ax.boxplot(
            data, vert=True,
            tick_labels=[str(y) for y in years_sorted],
            patch_artist=True, widths=0.55, showfliers=False,
            medianprops={"color": "black", "linewidth": 1.4},
        )
        for patch in bp["boxes"]:
            patch.set_facecolor("steelblue")
            patch.set_alpha(0.35)
            patch.set_edgecolor("steelblue")

        rng = np.random.default_rng(42)
        for i, vals in enumerate(data):
            if len(vals) == 0:
                continue
            xs = (i + 1) + rng.uniform(-0.18, 0.18, size=len(vals))
            ax.scatter(
                xs, vals, s=14, color="#1f4e79", alpha=0.65,
                edgecolors="none", zorder=3,
            )
        ax.set_ylabel("RMSE (Mg/ha)")
        ax.set_xlabel("Forecast year")
        if title:
            ax.set_title(title, fontsize=10, fontweight="bold")
        ax.grid(True, axis="y", linestyle=":", alpha=0.4)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        Path(dir_out).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(dir_out) / fname, dpi=250, bbox_inches="tight")
        plt.close(fig)


def rmse_by_year(
    df,
    title,
    dir_out,
    fname,
    *,
    year_col: str = "Harvest Year",
    rmse_col: str = "RMSE",
    obs_col: str | None = None,
    pred_col: str | None = None,
    area_col: str = "Area (ha)",
    threshold: float | None = None,
):
    """Bar chart of RMSE (Mg/ha) per year with 5-yr moving avg — RMSE twin
    of ``mape_by_year``.  When area is available, uses area-weighted
    national RMSE per year (sqrt of area-weighted squared error); otherwise
    falls back to mean of per-row ``rmse_col`` values.
    """
    if df.empty or year_col not in df.columns:
        return

    use_national = (
        obs_col is not None and pred_col is not None
        and obs_col in df.columns and pred_col in df.columns
        and area_col in df.columns and df[area_col].notna().any()
    )

    if use_national:
        d = df.dropna(subset=[obs_col, pred_col, area_col]).copy()
        d["_sqerr"] = (d[pred_col] - d[obs_col]) ** 2
        d["_wsqerr"] = d["_sqerr"] * d[area_col]
        by_year_df = d.groupby(year_col).agg(
            _wsqerr=("_wsqerr", "sum"),
            _area=(area_col, "sum"),
        )
        by_year_df = by_year_df[by_year_df["_area"] > 0]
        if by_year_df.empty:
            return
        rmse_series = np.sqrt(
            by_year_df["_wsqerr"] / by_year_df["_area"]
        ).sort_index()
    else:
        if rmse_col not in df.columns:
            return
        rmse_series = df.groupby(year_col)[rmse_col].mean().sort_index()

    if rmse_series.empty:
        return

    rolling_window = 5
    rmse_rolling = rmse_series.rolling(
        window=rolling_window, min_periods=rolling_window
    ).mean()

    with _science_style_context():
        fig, ax = plt.subplots(figsize=(10, 6))
        x_labels = [str(int(y)) for y in rmse_series.index]
        ax.bar(x_labels, rmse_series.values, color="steelblue")
        if threshold is not None:
            ax.axhline(y=threshold, color="gray", linestyle="--")
        ax.plot(
            x_labels, rmse_rolling.values,
            color="darkorange", linewidth=2, marker="o", markersize=4,
            label=f"{rolling_window}-yr moving avg", zorder=3,
        )
        ax.legend(loc="upper right", fontsize=8, frameon=False)
        ax.set_xlabel("")
        ax.set_ylabel("RMSE (Mg/ha)")
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


def metric_choropleth(dg, df, countries, annotate_regions, dir_out, fname,
                      *, col, label, vmin=None, vmax=None,
                      higher_is_better=False):
    """Choropleth map of an arbitrary per-region metric via plot.plot_map().

    Generalises :func:`mape_choropleth` to any metric column (RMSE, R², …).

    Args:
        dg: GeoDataFrame of boundaries (with a "Country Region" merge column).
        df: DataFrame with "Country Region" plus the metric column ``col``.
        countries: list of display-format country names.
        annotate_regions: bool.
        dir_out: output directory; fname: output filename.
        col: name of the metric column in ``df`` to color by.
        label: colorbar label.
        vmin/vmax: color-scale bounds. ``None`` → derived from the data
            (vmin = min, vmax = 95th percentile).
        higher_is_better: when True, use the non-reversed Bamako ramp so high
            values (good, e.g. R²) render light — matching the "good = light"
            convention of the reversed ramp used for MAPE/RMSE (low = good).
    """
    import palettable as pal
    from . import plot

    if df is None or df.empty or col not in df.columns:
        return
    df = df.copy()
    vals = df[col].dropna()
    if vals.empty:
        return

    if vmin is None:
        vmin = float(vals.min())
    if vmax is None:
        vmax = (float(vals.quantile(0.95))
                if vals.shape[0] > 1 else float(vals.max()))
    if vmin == vmax:  # degenerate scale (single region / identical values)
        vmax = vmin + 1e-6

    cmap = (pal.scientific.sequential.Bamako_20 if higher_is_better
            else pal.scientific.sequential.Bamako_20_r)

    Path(dir_out).mkdir(parents=True, exist_ok=True)
    plot.plot_map(
        dg,
        df,
        merge_col="Country Region",
        name_country=countries,
        name_col=col,
        dir_out=dir_out,
        fname=fname,
        label=label,
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        series="sequential",
        annotate_regions=annotate_regions,
        loc_legend="lower left",
    )


# ---------------------------------------------------------------------------
# CID-vs-yield diagnostic scatters (full-season span, one PNG per CID)
# ---------------------------------------------------------------------------

_CID_RANGE_RE = __import__("re").compile(
    r"^(.+?)\s+([A-Z][a-z]{2})\s+(\d+)-([A-Z][a-z]{2})\s+(\d+)$"
)

_MONTH_TO_STAGE = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}

_PEARSON_DEDUP_THRESHOLD = 0.9  # |ρ| above which two CIDs are treated
                                # as redundant for the top-N selection
                                # in pearson_summary.


def _stage_chain_length(smon: str, emon: str, method: str) -> int:
    """Number of monthly stages in the cumulative chain for the label
    ``"Mon dd-Mon dd"``. Under ``monthly_r`` the chain walks backward
    from the start month to the end month (so ``Dec→Nov`` is 2 stages,
    not 12); under ``monthly`` it walks forward. Other methods
    (biweekly/dekad) fall back to forward semantics — their stage→date
    mapping differs but the EDA picker tolerates the approximation.
    """
    s = _MONTH_TO_STAGE.get(smon)
    e = _MONTH_TO_STAGE.get(emon)
    if s is None or e is None:
        return 0
    if method.endswith("_r"):
        return (s - e) % 12 + 1
    return (e - s) % 12 + 1


def _parse_cid_column(col: str, method: str = "monthly"):
    """Parse ``"<CID> Mon day-Mon day"`` → ``(cid, chain_length_in_stages)``.

    Returns None for columns that don't match the canonical stage-renamed
    format (Pre-Season / In-Season aggregates, categorical, lag, etc.).
    """
    m = _CID_RANGE_RE.match(col)
    if m is None:
        return None
    cid, smon, _sday, emon, _eday = m.groups()
    chain = _stage_chain_length(smon, emon, method)
    if chain == 0:
        return None
    return cid, chain


# The dedup helper lives in geocif.utils now (shared with auto_select_cids).
# Imported above as ``greedy_dedup_by_mutual_corr``.


def cid_vs_yield_scatters(
    df: pd.DataFrame,
    target_col: str,
    dir_out: Path,
    country: str,
    crop: str,
    *,
    year_col: str = "Harvest Year",
    method: str = "monthly",
    season_stages: int | None = None,
) -> int:
    """One scatter per CID: x = CID value over its full planting→harvest
    cumulative span, y = observed yield. Points coloured by ``year_col``.

    Per-CID column choice: amongst all wide-format columns matching the
    canonical renamed format ``"<CID> <Mon> <day>-<Mon> <day>"``, the one
    with the longest cumulative **stage chain** wins. Chain length is
    method-aware — under ``monthly_r`` the chain walks backward, so a
    label like ``Dec 1-Nov 30`` is 2 stages (Nov+Dec) not 12 calendar
    months. ``season_stages`` (if given) caps the picker as a sanity
    guard against any over-long chain sneaking in.

    Output layout (idempotent — skips if any PNG already exists for this
    country/crop, so it's safe to call from every model run):
        {dir_out}/{country}/{crop}/{cid}.png   (+ matching .csv per geocif
                                                 plot-CSV pairing rule)

    Returns the count of CIDs plotted (0 if skipped).
    """
    out_dir = Path(dir_out) / country.lower() / crop.lower()
    if out_dir.is_dir() and any(out_dir.glob("*.png")):
        logger.info(f"  cid_vs_yield_scatters: skipping {out_dir} — already populated")
        return 0
    if target_col not in df.columns:
        logger.warning(f"  cid_vs_yield_scatters: target column {target_col!r} missing — skipping")
        return 0
    if year_col not in df.columns:
        logger.warning(f"  cid_vs_yield_scatters: {year_col!r} missing — skipping")
        return 0

    # For each parseable column, score its chain length. Then pick longest-chain per CID.
    by_cid: dict[str, tuple[str, int]] = {}  # cid → (column, chain_length)
    for col in df.columns:
        parsed = _parse_cid_column(col, method=method)
        if parsed is None:
            continue
        cid, chain = parsed
        if season_stages is not None and chain > season_stages:
            continue  # over-cap (shouldn't happen but defensive)
        prev = by_cid.get(cid)
        if prev is None or chain > prev[1]:
            by_cid[cid] = (col, chain)
    if not by_cid:
        logger.info(f"  cid_vs_yield_scatters: no parseable CID columns in {country}/{crop}")
        return 0

    max_chain = max(c for _, c in by_cid.values())
    n_at_max = sum(1 for _, c in by_cid.values() if c == max_chain)
    logger.info(
        f"  cid_vs_yield_scatters: {country}/{crop} method={method!r} "
        f"max_chain={max_chain} stages, {n_at_max}/{len(by_cid)} CIDs at max "
        f"({len(by_cid) - n_at_max} picked shorter)"
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    csv_dir = out_dir / "csvs"
    csv_dir.mkdir(parents=True, exist_ok=True)

    # Stable year colour map across all CIDs in this (country, crop).
    years_sorted = sorted(pd.to_numeric(df[year_col], errors="coerce").dropna().unique())
    cmap = plt.get_cmap("viridis")
    year_to_color = {
        int(y): cmap(i / max(1, len(years_sorted) - 1))
        for i, y in enumerate(years_sorted)
    }

    region_col = "Region" if "Region" in df.columns else None

    # Stable region colour map for the per-CID *_by_region.png companion
    # plots. Use a qualitative palette sized to the region count; cycle
    # when N > 20 (rare for admin_1; admin_2 countries may overflow but
    # the visual repetition is acceptable for EDA).
    region_to_color: dict = {}
    regions_sorted: list = []
    if region_col is not None:
        regions_sorted = sorted(df[region_col].dropna().astype(str).unique().tolist())
        if regions_sorted:
            _n_regions = len(regions_sorted)
            _palette_name = "tab10" if _n_regions <= 10 else "tab20"
            _region_cmap = plt.get_cmap(_palette_name, max(_n_regions, 1))
            region_to_color = {
                r: _region_cmap(i % _region_cmap.N)
                for i, r in enumerate(regions_sorted)
            }

    n_plotted = 0
    pearson_rows: list[tuple[str, int, float]] = []  # (cid, n, r_p) for the summary fig
    cid_series: dict[str, pd.Series] = {}            # cid → full-season values for pairwise corr
    for cid, (col, chain) in sorted(by_cid.items()):
        keep_cols = [col, target_col, year_col] + ([region_col] if region_col else [])
        sub = df[keep_cols].dropna(subset=[col, target_col, year_col])
        if sub.empty:
            continue
        # Spearman + Pearson for the annotation box. Slow methods over
        # ~1k rows is still <10ms; safe to compute every call.
        try:
            r_p = float(sub[col].corr(sub[target_col], method="pearson"))
        except (TypeError, ValueError):
            r_p = float("nan")
        try:
            r_s = float(sub[col].corr(sub[target_col], method="spearman"))
        except (TypeError, ValueError):
            r_s = float("nan")

        if np.isfinite(r_p):
            pearson_rows.append((cid, len(sub), r_p))
            cid_series[cid] = sub[col].reset_index(drop=True)

        colors = [year_to_color.get(int(y), (0.5, 0.5, 0.5, 0.7))
                  for y in sub[year_col]]

        with _science_style_context():
            fig, ax = plt.subplots(figsize=(6.5, 5))
            ax.scatter(
                sub[col], sub[target_col],
                c=colors, s=22, alpha=0.78, edgecolors="white", linewidths=0.4,
            )
            ax.set_xlabel(f"{col}   (full-season ≈ {chain} stages)", fontsize=9)
            ax.set_ylabel(target_col, fontsize=9)
            ax.set_title(
                f"{country.title().replace('_', ' ')} {crop.title().replace('_', ' ')}  —  {cid}",
                fontsize=10, fontweight="bold",
            )
            ax.grid(True, linestyle=":", alpha=0.4)
            ax.text(
                0.02, 0.98,
                f"N = {len(sub)}\nPearson r = {r_p:+.2f}\nSpearman ρ = {r_s:+.2f}",
                transform=ax.transAxes, va="top", ha="left",
                fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor="gray", alpha=0.85),
            )
            # Year colour-bar (discrete) on the right.
            if len(years_sorted) >= 2:
                import matplotlib.colors as _mcolors
                import matplotlib.cm as _mcm
                norm = _mcolors.Normalize(
                    vmin=min(years_sorted), vmax=max(years_sorted),
                )
                sm = _mcm.ScalarMappable(cmap=cmap, norm=norm)
                sm.set_array([])
                cbar = fig.colorbar(sm, ax=ax, pad=0.02)
                cbar.set_label(year_col, fontsize=8)
                cbar.ax.tick_params(labelsize=7)
            plt.tight_layout()
            # Filename: sanitise CID (drop chars that break paths on Windows).
            safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in cid)
            fig.savefig(out_dir / f"{safe}.png", dpi=200, bbox_inches="tight")
            plt.close(fig)

        # Companion plot: same scatter, coloured by Region (categorical)
        # with a per-region OLS fit line and slope/R²/n in the legend.
        # Only produced when the df carries a Region column AND we have
        # a region palette built. Regions with fewer than 3 points get
        # the scatter but no fit line (slope undefined).
        if region_col is not None and region_to_color and region_col in sub.columns:
            with _science_style_context():
                fig, ax = plt.subplots(figsize=(7.5, 5))
                x_min = float(sub[col].min())
                x_max = float(sub[col].max())
                _x_line = np.linspace(x_min, x_max, 50) if x_max > x_min else None
                for region in regions_sorted:
                    region_mask = sub[region_col].astype(str) == region
                    n_region = int(region_mask.sum())
                    if n_region == 0:
                        continue
                    rx = sub.loc[region_mask, col].to_numpy()
                    ry = sub.loc[region_mask, target_col].to_numpy()
                    label = f"{region}  (n={n_region}"
                    if n_region >= 3 and np.ptp(rx) > 0:
                        # OLS fit y = m*x + b; R² = 1 - SSres/SStot.
                        m, b = np.polyfit(rx, ry, 1)
                        y_pred = m * rx + b
                        ss_res = float(np.sum((ry - y_pred) ** 2))
                        ss_tot = float(np.sum((ry - float(np.mean(ry))) ** 2))
                        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
                        label += f", slope={m:+.2g}, R²={r2:.2f})"
                        if _x_line is not None:
                            ax.plot(_x_line, m * _x_line + b,
                                    color=region_to_color[region],
                                    linewidth=1.2, alpha=0.85)
                    else:
                        label += ", fit n/a)"
                    ax.scatter(
                        rx, ry,
                        color=region_to_color[region],
                        s=22, alpha=0.78, edgecolors="white", linewidths=0.4,
                        label=label,
                    )
                ax.set_xlabel(f"{col}   (full-season ≈ {chain} stages)", fontsize=9)
                ax.set_ylabel(target_col, fontsize=9)
                ax.set_title(
                    f"{country.title().replace('_', ' ')} {crop.title().replace('_', ' ')}  —  {cid}  (by region, OLS fits)",
                    fontsize=10, fontweight="bold",
                )
                ax.grid(True, linestyle=":", alpha=0.4)
                ax.text(
                    0.02, 0.98,
                    f"N = {len(sub)}\nPearson r = {r_p:+.2f}\nSpearman ρ = {r_s:+.2f}",
                    transform=ax.transAxes, va="top", ha="left",
                    fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                              edgecolor="gray", alpha=0.85),
                )
                ax.legend(
                    bbox_to_anchor=(1.02, 1), loc="upper left",
                    fontsize=7, title=region_col, title_fontsize=8,
                    frameon=True, borderaxespad=0.0,
                )
                plt.tight_layout()
                fig.savefig(out_dir / f"{safe}_by_region.png",
                            dpi=200, bbox_inches="tight")
                plt.close(fig)

        out_df = sub.assign(cid=cid).rename(columns={col: "cid_value"})
        ordered = (
            ([region_col] if region_col else [])
            + [year_col, "cid", "cid_value", target_col]
        )
        out_df = out_df[[c for c in ordered if c in out_df.columns]]
        out_df.to_csv(csv_dir / f"{safe}.csv", index=False)
        n_plotted += 1

    if pearson_rows:
        pearson_df = pd.DataFrame(pearson_rows, columns=["cid", "n", "pearson_r"])
        pearson_df["abs_r"] = pearson_df["pearson_r"].abs()
        pearson_df = pearson_df.sort_values("abs_r", ascending=False).reset_index(drop=True)
        pearson_df["rank_raw"] = pearson_df.index + 1

        # Row-aligned CID-value matrix for pairwise pruning. Outer-join
        # on the (region, year) index lets pandas drop NaNs natively per
        # column-pair when computing the correlation matrix.
        cid_value_df = pd.concat(
            {c: cid_series[c] for c in pearson_df["cid"] if c in cid_series},
            axis=1,
        )
        corr_abs = (
            cid_value_df.corr(method="pearson").abs()
            if cid_value_df.shape[1] >= 2
            else pd.DataFrame()
        )
        kept, pruned = greedy_dedup_by_mutual_corr(
            pearson_df["cid"].tolist(),
            corr_abs,
            _PEARSON_DEDUP_THRESHOLD,
        )
        kept_set = set(kept)
        pearson_df["kept"] = pearson_df["cid"].isin(kept_set)
        pearson_df["redundant_with"] = pearson_df["cid"].map(
            lambda c: pruned.get(c, ("", float("nan")))[0]
        )
        pearson_df["mutual_r"] = pearson_df["cid"].map(
            lambda c: pruned.get(c, ("", float("nan")))[1]
        )
        pearson_df.to_csv(csv_dir / "pearson_summary.csv", index=False)

        # Persist the pairwise |ρ| matrix so the auto-CID selector
        # (utils.auto_select_cids) can re-dedup at relaxed thresholds
        # without needing the raw per-region cid_series data again.
        if not corr_abs.empty:
            corr_abs.to_csv(csv_dir / "pearson_corr_matrix.csv")

        n_total = len(pearson_df)
        n_pruned = int((~pearson_df["kept"]).sum())
        top = pearson_df[pearson_df["kept"]].head(10)

        with _science_style_context():
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            # Left: stacked histogram, survivors blue + pruned grey.
            survivors_r = pearson_df.loc[pearson_df["kept"], "pearson_r"]
            pruned_r = pearson_df.loc[~pearson_df["kept"], "pearson_r"]
            bins = np.linspace(
                float(pearson_df["pearson_r"].min()),
                float(pearson_df["pearson_r"].max()),
                21,
            )
            ax1.hist([survivors_r, pruned_r], bins=bins, stacked=True,
                     color=["#4c72b0", "#bdbdbd"],
                     label=[f"kept ({len(survivors_r)})", f"pruned ({n_pruned})"],
                     edgecolor="white", alpha=0.9)
            ax1.axvline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
            ax1.set_xlabel("Pearson r (CID vs Yield)", fontsize=10)
            ax1.set_ylabel("Number of CIDs", fontsize=10)
            ax1.set_title(f"Distribution across {n_total} CIDs", fontsize=10)
            ax1.legend(loc="upper left", fontsize=8, frameon=True)
            ax1.grid(True, linestyle=":", alpha=0.4)

            # Right: top 10 survivors (post-dedup), largest |r| at top.
            order = top.iloc[::-1]
            bar_colors = ["#c44e52" if v < 0 else "#55a868" for v in order["pearson_r"]]
            ax2.barh(range(len(order)), order["pearson_r"],
                     color=bar_colors, edgecolor="white")
            ax2.set_yticks(range(len(order)))
            ax2.set_yticklabels(order["cid"], fontsize=9)
            ax2.axvline(0, color="black", linewidth=0.8, alpha=0.5)
            ax2.set_xlabel("Pearson r", fontsize=10)
            ax2.set_title(
                f"Top {len(order)} surviving CIDs by |Pearson r|",
                fontsize=10,
            )
            ax2.grid(True, axis="x", linestyle=":", alpha=0.4)
            for i, v in enumerate(order["pearson_r"]):
                ax2.text(v + (0.01 if v >= 0 else -0.01), i,
                         f"{v:+.2f}", va="center",
                         ha="left" if v >= 0 else "right", fontsize=8)

            fig.suptitle(
                f"{country.title().replace('_', ' ')} "
                f"{crop.title().replace('_', ' ')}  —  "
                f"CID-vs-Yield Pearson r summary  "
                f"({n_pruned} of {n_total} CIDs pruned at |ρ|>{_PEARSON_DEDUP_THRESHOLD})",
                fontsize=11, fontweight="bold",
            )
            plt.tight_layout()
            fig.savefig(out_dir / "pearson_summary.png", dpi=200, bbox_inches="tight")
            plt.close(fig)
        logger.info(
            f"  cid_vs_yield_scatters: wrote Pearson r summary "
            f"({n_total} CIDs, {n_pruned} pruned at |ρ|>{_PEARSON_DEDUP_THRESHOLD}, "
            f"{len(kept)} kept) → {out_dir / 'pearson_summary.png'}"
        )

    logger.info(
        f"  cid_vs_yield_scatters: wrote {n_plotted} CID scatters → {out_dir}"
    )
    return n_plotted
