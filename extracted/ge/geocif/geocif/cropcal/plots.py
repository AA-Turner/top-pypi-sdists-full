# -*- coding: utf-8 -*-
"""Figures for the crop-calendar validation.

Two families, following the house split:

* ``plots/`` -- per-region **diagnostics**: the fitted curve against the median
  NDVI with both difference spans shaded, the derivative against the calendar
  marks, and the individual years behind the median. This is how a disagreement
  is actually read.
* ``maps/`` -- **choropleths** of the signed difference, rendered through
  :func:`geocif.viz.plot.plot_map` so they get the shared PyGMT furniture.

Every figure ships the exact frame behind it to ``csvs/``, mirroring the plot
tree, and ``lookup_plots_csvs.csv`` maps each figure to its companion.

The **signed** difference is what gets mapped, never the legacy ``delta_*``:
that column's wrap branch forces roughly half the population positive, so its
mean is not a bias. All numeric detail lives in the CSVs, not on the canvas.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import pandas as pd

from geocif.viz._style import MONTHS, despine, style_ctx

logger = logging.getLogger(__name__)

DPI = 300

#: First day-of-year of each month in a non-leap year, for a DOY axis.
MONTH_STARTS = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]

#: Colours for the two transitions, used identically on charts and maps.
GREENUP_COLOUR = "#1b7837"
GREENDOWN_COLOUR = "#b8860b"

#: Rendered as-is on the canvas. Slugs stay in the CSV columns.
DISPLAY_NAMES = {
    "maize": "Maize",
    "rice": "Rice",
    "soybean": "Soybean",
    "sorghum": "Sorghum",
    "millet": "Millet",
    "teff": "Teff",
    "beans": "Beans",
    "winter_wheat": "Winter Wheat",
    "spring_wheat": "Spring Wheat",
    "rangelands": "Rangelands",
    "midgreenup": "Mid Greenup",
    "midgreendown": "Mid Greendown",
}


def display(token: str) -> str:
    """Canvas spelling for a config slug."""
    key = str(token).strip().lower()
    if key in DISPLAY_NAMES:
        return DISPLAY_NAMES[key]
    return str(token).replace("_", " ").title()


# --------------------------------------------------------------------------
# Output tree
# --------------------------------------------------------------------------
class FigureSet:
    """Writes figures and their companion CSVs, and keeps the lookup."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.rows: list[dict] = []

    def _csv_path(self, kind: str, stem: str) -> Path:
        return self.root / "csvs" / kind / f"{stem}.csv"

    def path(self, kind: str, stem: str) -> Path:
        directory = self.root / kind
        directory.mkdir(parents=True, exist_ok=True)
        return directory / f"{stem}.png"

    def record(self, kind: str, stem: str, frame: pd.DataFrame) -> Path:
        """Write the companion CSV and register the pair."""
        csv_path = self._csv_path(kind, stem)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(csv_path, index=False)
        self.rows.append(
            {
                "plot": f"{kind}/{stem}.png",
                "csv": f"csvs/{kind}/{stem}.csv",
                "rows": len(frame),
            }
        )
        return csv_path

    def write_lookup(self) -> Optional[Path]:
        if not self.rows:
            return None
        path = self.root / "lookup_plots_csvs.csv"
        pd.DataFrame(self.rows).to_csv(path, index=False)
        return path


# --------------------------------------------------------------------------
# Per-region diagnostic
# --------------------------------------------------------------------------
def _month_axis(ax) -> None:
    ax.set_xticks(MONTH_STARTS)
    ax.set_xticklabels(MONTHS)
    ax.set_xlim(0, 365)


def _shade_difference(ax, calendar_day, satellite_day, colour, label) -> None:
    """Shade between the two days, taking the short way round the year."""
    if not (np.isfinite(calendar_day) and np.isfinite(satellite_day)):
        return
    lo, hi = min(calendar_day, satellite_day), max(calendar_day, satellite_day)
    if hi - lo > 180:
        ax.axvspan(hi, 365, color=colour, alpha=0.25, lw=0, label=label)
        ax.axvspan(0, lo, color=colour, alpha=0.25, lw=0)
    else:
        ax.axvspan(lo, hi, color=colour, alpha=0.25, lw=0, label=label)


def region_diagnostic(
    figures: FigureSet, context, diagnostics: dict, row: pd.Series
) -> Optional[Path]:
    """Three-panel diagnostic for one region, plus its companion CSV."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fitted = diagnostics["fitted"]
    masked = diagnostics["masked"]
    climatology = diagnostics["climatology"]
    geoglam = diagnostics["geoglam"]
    peaks, valleys = diagnostics["peaks"], diagnostics["valleys"]
    doy = np.arange(len(fitted))

    stem = (
        f"diagnostic_{context.country_slug}_{context.region}"
        f"_{context.crop}_s{context.season}"
    )

    with style_ctx():
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8.0, 9.0), sharex=True)

        # (A) the comparison itself
        _shade_difference(ax1, geoglam["midgreenup"], row["doy_RS_midgreenup"],
                          GREENUP_COLOUR, "Mid Greenup Difference")
        _shade_difference(ax1, geoglam["midgreendown"], row["doy_RS_midgreendown"],
                          GREENDOWN_COLOUR, "Mid Greendown Difference")
        ax1.plot(doy, climatology.ndvi, color="0.55", lw=1.0, label="Median NDVI")
        ax1.plot(doy, fitted, color="black", lw=1.6, label="Fitted")
        ax1.plot(doy, masked, color="#2166ac", lw=1.3, ls="--", label="In Season")
        if len(peaks):
            ax1.plot(peaks, fitted[peaks], "D", ms=5, color="#2166ac", label="Peak")
        if len(valleys):
            ax1.plot(valleys, fitted[valleys], "D", ms=5, color="#b2182b", label="Valley")
        ax1.set_ylabel("NDVI", fontsize=11)
        ax1.legend(loc="upper left", ncol=2, fontsize=9, frameon=False)
        ax1.set_title(
            f"{display(context.crop)} Season {context.season} - "
            f"{display(context.region)}, {context.country}",
            fontsize=12,
        )

        # (B) derivative, with the calendar's four days
        ax2.plot(doy[:-1], np.diff(masked), color="black", lw=1.2)
        for day, colour, label in (
            (geoglam["plant"], "0.45", "Planting"),
            (geoglam["midgreenup"], GREENUP_COLOUR, "Mid Greenup"),
            (geoglam["midgreendown"], GREENDOWN_COLOUR, "Mid Greendown"),
            (geoglam["harvest"], "#8c510a", "Harvest"),
        ):
            ax2.axvline(day, color=colour, lw=1.3, ls="--", label=label)
        ax2.axhline(0, color="0.8", lw=0.7)
        ax2.set_ylabel("d(NDVI)/dt", fontsize=11)
        ax2.legend(loc="upper left", ncol=2, fontsize=9, frameon=False)

        # (C) the years behind the median
        for column in climatology.ndvi_years.columns:
            ax3.plot(climatology.ndvi_years.index, climatology.ndvi_years[column],
                     lw=1.1, label=str(column))
        ax3.set_ylabel("NDVI", fontsize=11)
        ax3.set_xlabel("Day of Year", fontsize=11)
        ax3.legend(loc="upper left", ncol=4, fontsize=9, frameon=False)

        for ax in (ax1, ax2, ax3):
            _month_axis(ax)
            ax.tick_params(labelsize=10)
            ax.grid(True, ls=":", alpha=0.5)
        despine(ax1, ax2, ax3)
        fig.tight_layout()

        path = figures.path("plots", stem)
        fig.savefig(path, dpi=DPI, bbox_inches="tight")
        plt.close(fig)

    figures.record(
        "plots",
        stem,
        pd.DataFrame(
            {
                "doy": doy,
                "ndvi_median": climatology.ndvi,
                "ndvi_fitted": fitted,
                "ndvi_in_season": masked,
                "gdd": climatology.gdd,
            }
        ),
    )
    return path


# --------------------------------------------------------------------------
# Choropleths
# --------------------------------------------------------------------------
def difference_map(
    figures: FigureSet,
    scored: pd.DataFrame,
    boundary_file: Optional[Path],
    *,
    column: str,
    transition: str,
    crop: Optional[str] = None,
) -> Optional[Path]:
    """World choropleth of a signed difference, with its companion CSV.

    Returns ``None`` when the boundary file or GMT is unavailable -- the CSV is
    written either way, because a missing map must not cost the numbers.
    """
    frame = scored if crop is None else scored[scored["crop"] == crop]
    table = (
        frame.groupby("key", dropna=False)[column]
        .mean()
        .reset_index()
        .rename(columns={column: "value"})
        .dropna(subset=["value"])
    )
    stem = f"delta_{transition}_world" if crop is None else f"delta_{transition}_{crop}"
    figures.record("maps", stem, table)

    if table.empty:
        logger.warning(f"{stem}: nothing to map")
        return None
    if boundary_file is None or not Path(boundary_file).is_file():
        logger.warning(f"{stem}: no boundary file; CSV written without a map")
        return None

    try:
        import geopandas as gpd

        from geocif.viz.plot import plot_map
    except Exception as exc:  # noqa: BLE001 - maps are optional, numbers are not
        logger.warning(f"{stem}: mapping unavailable ({exc}); CSV written")
        return None

    try:
        regions = gpd.read_file(boundary_file, engine="pyogrio")
        regions = regions.rename(columns={"Key": "key"})
        # A symmetric scale, so zero is the midpoint of the diverging ramp and
        # "calendar earlier" and "calendar later" are visually comparable.
        limit = float(np.clip(np.nanpercentile(np.abs(table["value"]), 98), 10.0, 180.0))
        title = f"{display(transition)} Difference"
        if crop:
            title = f"{display(crop)} {title}"

        plot_map(
            regions,
            table,
            merge_col="key",
            name_country="world",
            name_col="value",
            dir_out=str((figures.root / "maps").resolve()),
            fname=f"{stem}.png",
            title=title,
            label="Days (Calendar minus Satellite)",
            vmin=-limit,
            vmax=limit,
            series="diverging",
            annotate_regions=False,
        )
        path = figures.root / "maps" / f"{stem}.png"
        return path if path.is_file() else None
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"{stem}: map failed ({exc}); CSV written")
        return None


def agreement_by_crop(figures: FigureSet, summary: pd.DataFrame) -> Optional[Path]:
    """Bar chart of the pass rate per crop, full frame against the subset."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    frame = summary[summary["crop"] != "All"].copy()
    if frame.empty:
        return None
    frame = frame.sort_values("pct_works", ascending=True)
    stem = "agreement_crop"

    with style_ctx():
        fig, ax = plt.subplots(figsize=(7.5, 0.5 * len(frame) + 2.0))
        y = np.arange(len(frame))
        ax.barh(y - 0.2, frame["pct_works"], height=0.38,
                color="#4393c3", label="All Regions")
        ax.barh(y + 0.2, frame["pct_works_subset"], height=0.38,
                color="#1b7837", label="Peak Inside Stage 2")
        ax.set_yticks(y)
        ax.set_yticklabels([display(c) for c in frame["crop"]], fontsize=10)
        ax.set_xlabel("Regions Within 45 Days (%)", fontsize=11)
        ax.set_xlim(0, 100)
        ax.tick_params(labelsize=10)
        ax.legend(loc="lower right", fontsize=9, frameon=False)
        ax.set_title("Calendar and Satellite Agreement by Crop", fontsize=12)
        ax.grid(True, axis="x", ls=":", alpha=0.5)
        despine(ax)
        fig.tight_layout()
        path = figures.path("plots", stem)
        fig.savefig(path, dpi=DPI, bbox_inches="tight")
        plt.close(fig)

    figures.record("plots", stem, frame)
    return path


def difference_distribution(figures: FigureSet, scored: pd.DataFrame) -> Optional[Path]:
    """Signed-difference distribution per crop, both transitions."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    crops = sorted(scored["crop"].dropna().unique())
    if not crops:
        return None
    stem = "difference_distribution_crop"

    with style_ctx():
        # sharex matters: without it each panel autoscales to its own spread
        # and an equal-width box means a different number of days on the left
        # than on the right, which is exactly the comparison the figure is for.
        fig, axes = plt.subplots(1, 2, figsize=(11.0, 0.42 * len(crops) + 2.6),
                                 sharey=True, sharex=True)
        for ax, (column, transition, colour) in zip(
            axes,
            (
                ("delta_midgreenup_signed", "midgreenup", GREENUP_COLOUR),
                ("delta_midgreendown_signed", "midgreendown", GREENDOWN_COLOUR),
            ),
        ):
            data = [scored.loc[scored["crop"] == c, column].dropna().to_numpy()
                    for c in crops]
            parts = ax.boxplot(data, vert=False, widths=0.6, patch_artist=True,
                               showfliers=False)
            for box in parts["boxes"]:
                box.set(facecolor=colour, alpha=0.45, edgecolor="black", lw=0.8)
            for whisker in parts["whiskers"] + parts["caps"]:
                whisker.set(color="black", lw=0.8)
            for median in parts["medians"]:
                median.set(color="black", lw=1.4)
            ax.axvline(0, color="0.4", lw=1.0)
            ax.set_yticks(np.arange(1, len(crops) + 1))
            ax.set_yticklabels([display(c) for c in crops], fontsize=10)
            ax.set_xlabel("Days (Calendar minus Satellite)", fontsize=11)
            ax.set_title(f"{display(transition)}", fontsize=12)
            ax.tick_params(labelsize=10)
            ax.grid(True, axis="x", ls=":", alpha=0.5)
            despine(ax)
        fig.tight_layout()
        path = figures.path("plots", stem)
        fig.savefig(path, dpi=DPI, bbox_inches="tight")
        plt.close(fig)

    figures.record(
        "plots",
        stem,
        scored[["key", "country", "region", "crop", "season",
                "delta_midgreenup_signed", "delta_midgreendown_signed"]],
    )
    return path


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------
def render_all(
    out_dir: Path,
    scored: pd.DataFrame,
    diagnostics: Sequence[tuple],
    *,
    summary: Optional[pd.DataFrame] = None,
    boundary_file: Optional[Path] = None,
    max_region_figures: Optional[int] = None,
) -> dict:
    """Render every figure and write ``lookup_plots_csvs.csv``.

    ``max_region_figures`` caps the per-region diagnostics; they are drawn
    worst-disagreement first, which is the order anyone actually wants them in.
    """
    figures = FigureSet(Path(out_dir))
    made = {"plots": 0, "maps": 0}

    if summary is not None and agreement_by_crop(figures, summary):
        made["plots"] += 1
    if difference_distribution(figures, scored):
        made["plots"] += 1

    for column, transition in (
        ("delta_midgreenup_signed", "midgreenup"),
        ("delta_midgreendown_signed", "midgreendown"),
    ):
        if column not in scored.columns:
            continue
        if difference_map(figures, scored, boundary_file,
                          column=column, transition=transition):
            made["maps"] += 1
        for crop in sorted(scored["crop"].dropna().unique()):
            if difference_map(figures, scored, boundary_file, column=column,
                              transition=transition, crop=crop):
                made["maps"] += 1

    indexed = scored.set_index(["key", "crop", "season"], drop=False)
    ordered = sorted(
        diagnostics,
        key=lambda item: -_combined_delta(indexed, item[0]),
    )
    if max_region_figures is not None:
        ordered = ordered[:max_region_figures]

    for context, payload in ordered:
        key = (context.key, context.crop, context.season)
        if key not in indexed.index:
            continue
        row = indexed.loc[key]
        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]
        try:
            if region_diagnostic(figures, context, payload, row):
                made["plots"] += 1
        except Exception as exc:  # noqa: BLE001 - one bad figure is not fatal
            logger.warning(f"diagnostic failed for {context.key}/{context.crop}: {exc}")

    figures.write_lookup()
    logger.info(f"figures: {made['plots']} plots, {made['maps']} maps in {out_dir}")
    return made


def _combined_delta(indexed: pd.DataFrame, context) -> float:
    key = (context.key, context.crop, context.season)
    if key not in indexed.index:
        return 0.0
    value = indexed.loc[key, "combined_delta"]
    if isinstance(value, pd.Series):
        value = value.iloc[0]
    return float(value) if np.isfinite(value) else 0.0
