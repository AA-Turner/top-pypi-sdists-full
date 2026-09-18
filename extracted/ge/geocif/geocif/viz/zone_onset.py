# -*- coding: utf-8 -*-
"""Charts for the per-zone start-of-season report (geocif.phenology.zone_report).

Two figures, each with a companion CSV:

* :func:`window_dotplot` -- one panel per calendar zone, every year in the
  record as a dot on the window axis, the current season marked. The window is
  shaded, so "started on time" is read as "inside the band". A distribution over
  years is what a map cannot show, which is why this is a chart.
* :func:`in_window_bars` -- how often each zone starts inside the window, with
  the current season overlaid when its window has closed.

Both take the frames :mod:`geocif.phenology.zone_report` produces and draw only
what those frames carry: a censored share is shown as a hatched fraction rather
than silently folded into "started on time".

Style comes from :mod:`geocif.viz._style` (house rule, and
``tests/test_viz_style.py`` scans every module in this package). No prose on the
canvas: the caveats live in the companion CSV and the caller's write-up.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd

from geocif.viz._style import despine, style_ctx

logger = logging.getLogger(__name__)

#: Colour of the shaded window band.
WINDOW_FILL: str = "#dfe7f2"

#: Past years, current season, and the zone's typical start.
PAST_COLOR: str = "#4a6fa5"
CURRENT_COLOR: str = "#c0392b"
MEDIAN_COLOR: str = "#1a1a1a"

#: Bar colour for the share that starts inside the window.
BAR_COLOR: str = "#4a6fa5"

#: The search boundary: values sitting on it are floors, not measurements.
CENSOR_COLOR: str = "#8a6d3b"

DPI: int = 300


def _display(token: Any) -> str:
    """``rift_valley`` -> ``Rift Valley`` (house casing for figure text)."""
    return str(token).replace("_", " ").title()


def _save(fig, out_stem: Path) -> Path:
    """Save a PNG next to its companion CSV and return the image path."""
    out_stem = Path(out_stem)
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    png = out_stem.with_suffix(".png")
    fig.savefig(png, dpi=DPI, bbox_inches="tight")
    return png


def window_dotplot(
    history: pd.DataFrame,
    current: Optional[pd.DataFrame],
    out_stem: Any,
    *,
    window_days: int = 30,
    search_lead_days: Optional[int] = None,
    title: str = "",
) -> tuple[Path, Path]:
    """One panel per zone: every year's median onset on the window axis.

    Args:
        history: the per-(zone, year) frame from
            :func:`geocif.phenology.zone_report.zone_history`.
        current: the running season's frame from ``current_vs_history``, or
            ``None``. Zones whose window has not opened are drawn without a
            current-season marker.
        out_stem: path without a suffix; ``.png`` and ``.csv`` are written.
        window_days: half-width of the shaded band.
        search_lead_days: where the onset search opened. Drawn as a dashed rule
            so a dot sitting on it is read as "at the limit of observation"
            rather than as a measured date -- the distinction that matters in
            zones whose rains routinely beat the search window.
        title: figure title; kept short and factual.

    Returns:
        ``(png_path, csv_path)``.
    """
    import matplotlib.pyplot as plt

    if history.empty:
        raise ValueError("window_dotplot: empty history")

    zones = sorted(history["zone"].unique())
    cur_by_zone = {}
    if current is not None and not current.empty:
        cur_by_zone = {r["zone"]: r for _, r in current.iterrows()}

    # The axis must be wider than the window, or the shaded band fills the panel
    # and stops reading as a band -- and anything that started outside the window
    # has nowhere to be drawn. Take the span from the data and pad it.
    plot_column = ("onset_median_all_days" if "onset_median_all_days" in history
                   else "onset_median_days")
    finite = history[plot_column].to_numpy(dtype="float64")
    finite = finite[np.isfinite(finite)]
    span = max(float(window_days) * 1.25, 5.0)
    if finite.size:
        span = max(span, float(np.abs(finite).max()) * 1.08)
    xlim = (-span, span)

    with style_ctx():
        fig, axes = plt.subplots(
            len(zones), 1, figsize=(7.2, 1.15 * len(zones) + 1.0), sharex=True
        )
        axes = np.atleast_1d(axes)
        for ax, zone in zip(axes, zones):
            grp = history[history["zone"] == zone].sort_values("harvest_year")
            # Plot the median over EVERYTHING that started, not just the part
            # inside the window: in a zone that mostly starts outside it, the
            # in-window median speaks for a minority and drifts toward the band
            # edge, which reads as "started on time" when it did not.
            med = grp[plot_column].to_numpy(dtype="float64")
            years = grp["harvest_year"].to_numpy()
            ok = np.isfinite(med)

            ax.axvspan(-window_days, window_days, color=WINDOW_FILL, zorder=0)
            ax.axvline(0.0, color="gray", lw=0.8, zorder=1)
            if search_lead_days is not None:
                ax.axvline(-float(search_lead_days), color=CENSOR_COLOR, lw=1.0,
                           ls="--", zorder=2)
            # jitter-free strip: y carries no meaning, so keep every dot on one line
            ax.scatter(med[ok], np.zeros(ok.sum()), s=18, color=PAST_COLOR,
                       alpha=0.65, zorder=3, label="Past years")
            if ok.any():
                ax.scatter([np.median(med[ok])], [0.0], marker="|", s=420,
                           color=MEDIAN_COLOR, zorder=4, linewidths=1.6,
                           label="Record median")

            row = cur_by_zone.get(zone)
            if row is not None:
                value = row.get("onset_median_all_days", np.nan)
                if not np.isfinite(value):
                    value = row.get("onset_median_days", np.nan)
                if np.isfinite(value):
                    ax.scatter([value], [0.0], s=70, marker="D",
                               color=CURRENT_COLOR, zorder=5,
                               label=f"{int(row['harvest_year'])}")

            ax.set_yticks([])
            ax.set_ylabel(_display(zone), rotation=0, ha="right", va="center",
                          fontsize=9)
            ax.set_ylim(-1, 1)
            ax.set_xlim(*xlim)
            n_ok = int(ok.sum())
            ax.text(0.995, 0.80, f"{n_ok}/{len(grp)} yr", transform=ax.transAxes,
                    ha="right", va="center", fontsize=7, color="gray")
            despine(ax, sides=("top", "right", "left"))

        axes[-1].set_xlabel(f"Onset relative to the calendar planting date (days)")
        handles, labels = axes[0].get_legend_handles_labels()
        seen, uniq = set(), []
        for h, l in zip(handles, labels):
            if l not in seen:
                seen.add(l)
                uniq.append((h, l))
        if uniq:
            fig.legend([h for h, _ in uniq], [l for _, l in uniq],
                       loc="lower center", ncol=len(uniq), frameon=False,
                       bbox_to_anchor=(0.5, -0.02), fontsize=8)
        if title:
            fig.suptitle(title, fontsize=11)
        fig.tight_layout()
        png = _save(fig, Path(out_stem))
        plt.close(fig)

    csv = Path(out_stem).with_suffix(".csv")
    history.to_csv(csv, index=False)
    return png, csv


def in_window_bars(
    climatology: pd.DataFrame,
    current: Optional[pd.DataFrame],
    out_stem: Any,
    *,
    title: str = "",
) -> tuple[Path, Path]:
    """How often each zone starts inside the window, with the current season.

    The censored share is drawn hatched on top of the bar: where it is large the
    bar is a floor, because an onset pinned at the search boundary cannot be
    told from one that happened earlier.

    Args:
        climatology: the per-zone frame from
            :func:`geocif.phenology.zone_report.zone_climatology`.
        current: the running season's frame, or ``None``.
        out_stem: path without a suffix.
        title: figure title.

    Returns:
        ``(png_path, csv_path)``.
    """
    import matplotlib.pyplot as plt

    if climatology.empty:
        raise ValueError("in_window_bars: empty climatology")

    frame = climatology.sort_values("share_in_window_mean", ascending=False)
    zones = [_display(z) for z in frame["zone"]]
    share = frame["share_in_window_mean"].to_numpy(dtype="float64") * 100.0
    censored = frame["share_censored_mean"].to_numpy(dtype="float64") * 100.0
    y = np.arange(len(zones))

    cur_by_zone = {}
    if current is not None and not current.empty:
        cur_by_zone = {r["zone"]: r for _, r in current.iterrows()}

    with style_ctx():
        fig, ax = plt.subplots(figsize=(6.6, 0.52 * len(zones) + 1.6))
        ax.barh(y, share, color=BAR_COLOR, height=0.62, zorder=2)
        # censored portion, drawn at the left where the uncertainty lives
        for i, c in enumerate(censored):
            if np.isfinite(c) and c > 0:
                ax.barh(y[i], min(c, share[i]), color="none", height=0.62,
                        edgecolor="white", hatch="///", linewidth=0.0, zorder=3)

        for i, zone in enumerate(frame["zone"]):
            row = cur_by_zone.get(zone)
            if row is None:
                continue
            val = row.get("share_in_window")
            if row.get("window_status") == "complete" and np.isfinite(val):
                ax.scatter([val * 100.0], [y[i]], s=70, marker="D",
                           color=CURRENT_COLOR, zorder=5,
                           label=f"{int(row['harvest_year'])}")

        ax.set_yticks(y)
        ax.set_yticklabels(zones, fontsize=9)
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xlabel("Cropland starting inside the window (%)")
        for i, n in enumerate(frame["n_years_with_onset"]):
            ax.text(1.5, y[i], f"n={int(n)}", va="center", ha="left",
                    fontsize=7, color="white", zorder=6)
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend([handles[0]], [labels[0]], loc="lower right", frameon=False,
                      fontsize=8)
        if title:
            ax.set_title(title, fontsize=11)
        despine(ax)
        fig.tight_layout()
        png = _save(fig, Path(out_stem))
        plt.close(fig)

    csv = Path(out_stem).with_suffix(".csv")
    frame.to_csv(csv, index=False)
    return png, csv
