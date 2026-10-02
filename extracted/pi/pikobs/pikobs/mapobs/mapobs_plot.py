#!/usr/bin/python3
"""Figures of pikobs.mapobs.

The module writes one clear PNG per panel instead of forcing all views into
one crowded sheet.  The four views are:

    map
        Observations on a geographic map with longitude/latitude profiles.
    cross
        Zonal and meridional cross-sections.
    vertical
        Observation count per level or channel.
    stations
        Observation contribution by station/instrument.

Visual conventions are deliberately consistent:

* station colour is stable between figures and machines;
* dense observations are represented by smaller, more transparent points;
* panel headers live in a dedicated header band, so they cannot collide with
  axes titles;
* long station and level lists are condensed automatically;
* the combined ``all`` image preserves the natural proportions of panels.
"""

import gc
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import matplotlib as mpl
import matplotlib.patches
import matplotlib.ticker
mpl.use("Agg")

import matplotlib.gridspec as gridspec
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd

from pikobs.figures import save_figure

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    _HAS_CARTOPY = True
except ImportError:                                      # pragma: no cover
    _HAS_CARTOPY = False


# -----------------------------------------------------------------------------
# Visual configuration
# -----------------------------------------------------------------------------

DPI_HIGH = 150
DPI_LOW = 110

FONTS: Dict[str, float] = {
    "title": 15.5,
    "subtitle": 10.5,
    "meta": 8.5,
    "panel": 11.5,
    "label": 11,
    "tick": 9.5,
    "small": 8,
}

N_BINS_LON = 120
N_BINS_LAT = 60
N_BINS_VCONT = 41

# Backward-compatible constants imported by pikobs.mapobs.mapobs.
# Keep these names even when the plotting implementation does not use them
# directly; mapobs.py imports them as part of the module interface.
PAD_FACTOR_HIST = 1.2
PAD_FACTOR_STN = 1.1
VRANGE_PAD = 0.05
ANNOT_MIN_FRAC = 0.01

N_TICKS = 5

INCH_PER_LEVEL = 0.16
MIN_PANEL_HEIGHT = 5.0
MAX_PANEL_HEIGHT = 240.0
TICK_FONT_MAX = 8.0
TICK_FONT_MIN = 3.5
MAX_LEVELS_WITH_LABELS = 600
MAX_DISCRETE_LEVELS = 150

# Number of stations shown in the figure legend.  The stations panel still
# contains the complete list.
MAX_LEGEND_STATIONS = 20
LEGEND_COLUMNS = 1

# For dense figures, do not put a text label on every horizontal bar.
MAX_VALUE_LABELS = 80

# Margins reserved for the dedicated header band.
# Header space is defined in inches rather than as a fraction of figure
# height.  This is important for very tall interferometer/channel figures:
# a 10% top margin on a 100-inch figure would create a huge blank area.
# the header of the other modules, in inches from the top
HEADER_HEIGHT_IN = 1.30
HEADER_TITLE_OFFSET_IN = 0.10
HEADER_META_OFFSET_IN = 0.46      # the grey line
HEADER_EXP_OFFSET_IN = 0.74       # the run, in its colour
HEADER_RULE_OFFSET_IN = 1.05
HEADER_DETAILS_OFFSET_IN = 0.46

# Kept as a compatibility alias for callers that inspect the old constant.
PLOT_TOP = 0.875

_ROUND_PROJECTIONS = ("npolar", "spolar", "orthon", "orthos")
_SQUARE_PROJECTIONS = _ROUND_PROJECTIONS + (
    "canada", "europe", "ameriquenord", "hrdps", "reg"
)

_PRESSURE_KEYWORDS = (
    "pres", "pressure", "hpa", "mbar", "millibar", "pascal"
)
_HEIGHT_KEYWORDS = (
    "height", "altitude", "metre", "meter", " m]", "(m)",
    "agl", "asl", "geopotential"
)

_DOT_STEPS = (
    (5_000, 6.0, 0.85),
    (50_000, 3.0, 0.55),
    (200_000, 1.6, 0.35),
    (1_000_000, 0.8, 0.22),
    (float("inf"), 0.4, 0.15),
)

PANELS = ("map", "cross", "vertical", "stations")
COMBINED = "all"
ALL_PANELS = PANELS + (COMBINED,)
COMBINED_MAX_WIDTH = 2600

_FNV_OFFSET_BASIS_32 = 0x811C9DC5
_FNV_PRIME_32 = 0x01000193

_FEATURES_OK: Optional[bool] = None


# -----------------------------------------------------------------------------
# Generic helpers
# -----------------------------------------------------------------------------

def _safe(text: Any) -> str:
    return re.sub(r"[^A-Za-z0-9._+-]", "_", str(text))


def fmt_count(n: int) -> str:
    n = int(max(0, n))
    if n < 1_000_000:
        return f"{n:,}"
    if n < 1_000_000_000:
        return f"{n / 1e6:.1f}M"
    return f"{n / 1e9:.1f}B"


def nice_ticks(vmax: float, n: int = N_TICKS) -> List[int]:
    if vmax is None or vmax <= 0 or not np.isfinite(vmax):
        return [0, 1]

    rough = vmax / max(n, 1)
    magnitude = 10 ** np.floor(np.log10(rough))

    for nice in (1, 2, 5, 10):
        step = nice * magnitude
        if step >= rough:
            break

    step_int = max(1, int(step))
    upper = int(np.ceil(vmax / step_int) * step_int)
    return list(range(0, upper + step_int, step_int))


def _fnv1a_32(text: str) -> int:
    h = _FNV_OFFSET_BASIS_32
    for ch in str(text).upper():
        h = ((h ^ ord(ch)) * _FNV_PRIME_32) & 0xFFFFFFFF
    return h


def stable_color_for_stn(stn_name: str) -> Tuple[float, float, float, float]:
    """The colour of a station, the same in every figure: a known satellite
    from the table of pikobs/configobs/station_colours.py, any other
    station one of twenty colours far apart, by a hash of its name."""
    from pikobs.configobs.station_colours import station_colour
    return mpl.colors.to_rgba(station_colour(stn_name))


def build_global_color_map(stations: Iterable[str]) -> Dict[str, tuple]:
    """Build a deterministic colour map for every station."""
    return {
        stn: stable_color_for_stn(stn)
        for stn in sorted(set(str(s) for s in stations))
    }


def dot_style(n_obs: int) -> Tuple[float, float]:
    """Marker size and alpha for the total observation volume."""
    for limit, size, alpha in _DOT_STEPS:
        if n_obs < limit:
            return size, alpha
    return _DOT_STEPS[-1][1], _DOT_STEPS[-1][2]


def vertical_axis_orientation(
    vcotyp: str, is_channel: bool = False
) -> str:
    """Return the semantic orientation of the vertical coordinate."""
    lab = str(vcotyp).strip().lower()

    if is_channel or lab.startswith("canal") or "channel" in lab:
        return "channel"
    if lab.startswith("pression") or any(k in lab for k in _PRESSURE_KEYWORDS):
        return "pressure"
    if (
        lab.startswith("hauteur")
        or lab.startswith("height")
        or any(k in lab for k in _HEIGHT_KEYWORDS)
    ):
        return "height"
    if lab.startswith("surface"):
        return "surface"
    if lab.startswith("latitude"):
        return "latitude"
    return "unknown"


def region_label(extent: Sequence[float]) -> str:
    lon_w, lon_e, lat_s, lat_n = extent

    def _ns(v: float) -> str:
        return f"{abs(v):.0f}{'N' if v >= 0 else 'S'}"

    def _ew(v: float) -> str:
        return f"{abs(v):.0f}{'E' if v >= 0 else 'W'}"

    return f"[{_ns(lat_s)}-{_ns(lat_n)}, {_ew(lon_w)}-{_ew(lon_e)}]"


def map_projection(proj_name: str):
    """Return Cartopy projection, extent and preferred square layout."""
    if not _HAS_CARTOPY:
        raise RuntimeError("cartopy is required; install via pikobs_env.yml")

    name = str(proj_name).lower()
    square = any(k in name for k in _SQUARE_PROJECTIONS)

    if "npolar" in name:
        return (
            ccrs.NorthPolarStereo(central_longitude=-90.5),
            [-180, 180, 50, 90],
            square,
        )
    if "spolar" in name:
        return (
            ccrs.SouthPolarStereo(central_longitude=-86),
            [-180, 180, -90, -50],
            square,
        )
    if "orthon" in name:
        return (
            ccrs.Orthographic(90.0, -80.0),
            [-180, 180, 0, 90],
            square,
        )
    if "orthos" in name:
        return (
            ccrs.Orthographic(-90.0, -80.0),
            [-180, 180, -90, 0],
            square,
        )
    if "canada" in name:
        return (
            ccrs.NorthPolarStereo(central_longitude=-105.0),
            [-150, -53, 42, 90],
            square,
        )
    if "ameriquenord" in name:
        return (
            ccrs.NorthPolarStereo(central_longitude=-105.0),
            [-170, -40, 20, 90],
            square,
        )
    if "europe" in name:
        return ccrs.NorthPolarStereo(), [-25, 45, 30, 75], square
    if "robinson" in name:
        return ccrs.Robinson(), [-180, 180, -90, 90], False

    return ccrs.PlateCarree(), [-180, 180, -90, 90], False


def is_round(proj_name: str) -> bool:
    """Whether the projection should be clipped to a circular boundary."""
    return any(k in str(proj_name).lower() for k in _ROUND_PROJECTIONS)


# -----------------------------------------------------------------------------
# Figure context
# -----------------------------------------------------------------------------

@dataclass
class PlotContext:
    """Shared plotting information for one mapobs selection."""

    proj: Any
    extent: List[float]
    lon_ext: Tuple[float, float]
    lat_ext: Tuple[float, float]
    square_map: bool
    round_map: bool
    vcoord_label: str
    var_name: str
    var_units: str
    flag_label: str
    family: str
    exp_name: str
    region: str
    color_map: Dict[str, tuple]
    v_min: float
    v_max: float
    max_counts: Tuple[int, int, int, int]
    is_channel: bool
    v_orient: str
    region_lbl: str
    levels: Sequence[float] = ()
    svg: bool = False


# -----------------------------------------------------------------------------
# Vertical-axis helpers
# -----------------------------------------------------------------------------

def _levels_of(df: pd.DataFrame, ctx: PlotContext) -> List[float]:
    """Return the discrete vertical rows used by cross/vertical panels."""
    if ctx.v_orient in ("surface", "latitude"):
        return []

    values = list(ctx.levels)

    if not values:
        if df.empty or "vcoord" not in df:
            return []
        v = df["vcoord"].dropna()
        if v.empty:
            return []
        values = sorted(v.unique().tolist())

    if ctx.is_channel:
        return [int(x) for x in values]

    if len(values) <= MAX_DISCRETE_LEVELS:
        return values

    return []


def _level_label(value: Any) -> str:
    try:
        value = float(value)
        return str(int(value)) if value.is_integer() else f"{value:g}"
    except (TypeError, ValueError):
        return str(value)


def _level_height(n_levels: int) -> float:
    return float(
        np.clip(
            2.5 + INCH_PER_LEVEL * max(n_levels, 1),
            MIN_PANEL_HEIGHT,
            MAX_PANEL_HEIGHT,
        )
    )


def _tick_font(n_levels: int, height: float) -> float:
    if n_levels <= 0:
        return TICK_FONT_MAX
    points = 0.8 * height / n_levels * 72.0 / 1.45
    return float(min(TICK_FONT_MAX, max(TICK_FONT_MIN, points)))


def _in_hpa(ctx) -> bool:
    """A family on pressure levels: its levels shown in hPa, as elsewhere."""
    return "[Pa]" in str(ctx.vcoord_label)


def _vlabel(ctx) -> str:
    """The name of the vertical axis, in hPa for a pressure."""
    return str(ctx.vcoord_label).replace("[Pa]", "[hPa]")


def _set_vertical_axis(
    ax, levels: Sequence[float], ctx: PlotContext, tick_fs: float
) -> None:
    """Set a stable vertical coordinate without double inversion."""
    if levels:
        idx = np.arange(len(levels))
        step = max(1, int(np.ceil(len(levels) / MAX_LEVELS_WITH_LABELS)))

        shown_idx = idx[::step]
        shown_levels = levels[::step]

        ax.set_yticks(shown_idx)
        ax.set_yticklabels(
            [_level_label(v / 100.0 if _in_hpa(ctx) else v)
             for v in shown_levels],
            fontsize=tick_fs,
        )
        ax.set_ylim(-0.5, len(levels) - 0.5)
        ax.tick_params(axis="y", pad=3, length=2)

        if ctx.v_orient == "pressure":
            ax.invert_yaxis()
        return

    vmin = float(ctx.v_min)
    vmax = float(ctx.v_max)

    if not np.isfinite(vmin) or not np.isfinite(vmax) or vmin == vmax:
        center = vmin if np.isfinite(vmin) else 0.0
        span = max(abs(center) * 0.05, 1.0)
        vmin, vmax = center - span, center + span

    ax.set_ylim(vmin, vmax)
    ax.tick_params(axis="y", labelsize=FONTS["tick"])
    if _in_hpa(ctx):
        ax.yaxis.set_major_formatter(
            mpl.ticker.FuncFormatter(lambda v, _: f"{v / 100:g}"))

    if ctx.v_orient == "pressure":
        ax.invert_yaxis()


# -----------------------------------------------------------------------------
# Header and annotation helpers
# -----------------------------------------------------------------------------

def _legend_layout(fig, ctx) -> Tuple[int, int, float]:
    """(columns, rows, height in inches) of the station legend on top: as
    many columns as the width holds, from every station of the period, so
    that the play never changes it."""
    names = sorted(ctx.color_map)
    n = min(len(names), MAX_LEGEND_STATIONS) + (len(names) > MAX_LEGEND_STATIONS)
    if n == 0:
        return 1, 0, 0.0
    width = max(len(str(s)) for s in names)
    entry_in = (width + 22) * FONTS["small"] * 0.62 / 72 + 0.40
    ncol = max(1, min(n, int(fig.get_figwidth() * 0.93 // entry_in)))
    rows = -(-n // ncol)
    return ncol, rows, 0.42 + rows * FONTS["small"] * 1.65 / 72


def _legend_place(fig, ctx) -> Dict[str, Any]:
    """Where the legend goes: under the rule of the header, from the left."""
    height = max(float(fig.get_figheight()), 1.0)
    ncol = _legend_layout(fig, ctx)[0]
    return dict(loc="upper left", ncol=ncol,
                bbox_to_anchor=(0.03, 1.0 - (HEADER_RULE_OFFSET_IN + 0.05) / height))


def _plot_top(fig, ctx=None) -> float:
    """The top of the axes: below the header, and below the station legend
    when the figure has one."""
    height = max(float(fig.get_figheight()), 1.0)
    band = _legend_layout(fig, ctx)[2] if ctx is not None else 0.0
    return float(np.clip(1.0 - (HEADER_HEIGHT_IN + band) / height, 0.40, 0.985))


def _header(
    fig,
    ctx: PlotContext,
    dt_start,
    dt_end,
    n_obs: int,
    panel: str,
) -> None:
    """The header of the other modules, in inches from the top: the variable
    and the panel, the dates, a grey line with where and how, the run in its
    colour, a light rule."""
    from pikobs.configobs.style import EXP_COLOUR
    height = max(float(fig.get_figheight()), 1.0)

    def at(inch):
        return 1.0 - inch / height

    what = {"map": "observations on the map",
            "cross-sections": "cross-sections",
            "vertical distribution": "observations per level",
            "contributions": "observations per station"}.get(panel, panel)
    variable = f"{ctx.var_name} {ctx.var_units}".strip()
    fig.text(0.035, at(HEADER_TITLE_OFFSET_IN), f"{variable}  \u00b7  {what}",
             ha="left", va="top", fontsize=FONTS["title"], fontweight="bold",
             color="#1F2933")
    same_day = f"{dt_start:%Y%m%d}" == f"{dt_end:%Y%m%d}"
    when = (f"{dt_start:%Y-%m-%d %H:%M} to {dt_end:%H:%M} UTC" if same_day
            else f"{dt_start:%Y-%m-%d %H:%M} to {dt_end:%Y-%m-%d %H:%M} UTC")
    fig.text(0.965, at(HEADER_TITLE_OFFSET_IN + 0.02), when, ha="right",
             va="top", fontsize=FONTS["subtitle"], color="#52606D")
    fig.text(0.035, at(HEADER_META_OFFSET_IN),
             "  \u00b7  ".join([str(ctx.family), str(ctx.region),
                                f"flags {ctx.flag_label}",
                                f"{fmt_count(n_obs)} observations"]),
             ha="left", va="top", fontsize=FONTS["subtitle"], color="#52606D")
    fig.text(0.035, at(HEADER_EXP_OFFSET_IN), f"Exp  {ctx.exp_name}",
             ha="left", va="top", fontsize=FONTS["subtitle"] + 2,
             fontweight="bold", color=EXP_COLOUR)
    fig.lines.append(mpl.lines.Line2D(
        [0.035, 0.965], [at(HEADER_RULE_OFFSET_IN)] * 2,
        transform=fig.transFigure, lw=0.8, color="#D9DDE2"))
    # an invisible rectangle over the whole figure: the crop of the saving
    # always takes all of it, and every image of a group has one size
    fig.patches.append(mpl.patches.Rectangle(
        (0, 0), 1, 1, transform=fig.transFigure, fill=False,
        linewidth=0, zorder=-10))


def _panel_title(ax, title: str, subtitle: Optional[str] = None) -> None:
    """No title above a panel: the header of the figure says what it is,
    and its axes say the rest."""
    return None


def _station_counts(
    df: pd.DataFrame,
    color_map: Dict[str, tuple],
) -> pd.Series:
    if df.empty or "id_stn" not in df:
        return pd.Series(dtype=int)

    counts = df["id_stn"].value_counts()
    return counts[counts.index.isin(color_map)]


def _vertical_offsets(
    stations: Sequence[str],
    is_discrete: bool,
    v_min: float,
    v_max: float,
) -> Dict[str, float]:
    """Small vertical offsets that reveal overlapping station samples within a level.
    
    The offset creates parallel 'lanes' within the same level/channel
    so that different stations do not completely hide each other vertically.
    Latitudes and Longitudes (X-axis) remain at their exact values.
    """
    stations = list(stations)
    if len(stations) <= 1:
        return {station: 0.0 for station in stations}

    if is_discrete:
        # Discrete indices are exactly 1.0 apart (0, 1, 2...).
        # A band of 0.75 uses most of the vertical space between ticks without touching.
        total_band = 0.75
    else:
        # For continuous axes (like raw height), spread across 2% of the total vertical range.
        span = abs(float(v_max) - float(v_min))
        if not np.isfinite(span) or span <= 0:
            total_band = 0.0
        else:
            total_band = 0.02 * span

    positions = np.linspace(-0.5 * total_band, 0.5 * total_band, len(stations))

    return {
        station: float(offset)
        for station, offset in zip(stations, positions)
    }


def _station_badge(ax, counts: pd.Series, loc=(0.985, 0.985)) -> None:
    """Compact station/observation summary that replaces unnecessary legends."""
    total = int(counts.sum())
    n_stations = int(len(counts))

    text = f"{fmt_count(total)} obs  •  {n_stations} station"
    if n_stations != 1:
        text += "s"

    ax.text(
        loc[0],
        loc[1],
        text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=FONTS["small"],
        color="#444444",
        bbox=dict(
            boxstyle="round,pad=0.30",
            fc="white",
            ec="#C7CCD1",
            lw=0.7,
            alpha=0.92,
        ),
        zorder=20,
    )


def _station_legend(
    fig,
    ctx: PlotContext,
    counts: pd.Series,
    x: float = 0.98,
    y: float = 0.50,
) -> None:
    """Draw the station legend. Every station of the period, in one order
    and with its count here, in its colour even at 0, every line of the
    same width: the legend, and the image, hold still from one slot to the
    next; ranked by count only
    when there are more stations than the legend holds."""
    stations = sorted(ctx.color_map)
    if 0 < len(stations) <= MAX_LEGEND_STATIONS:
        total = float(counts.sum()) if not counts.empty else 0.0
        width = max(len(str(s)) for s in stations)
        handles = []
        for station in stations:
            n = int(counts.get(station, 0)) if not counts.empty else 0
            share = 100.0 * n / total if total else 0.0
            label = f"{str(station):<{width}s} {n:>9,d} {share:5.1f}%"
            handles.append(plt.Line2D(
                [], [], marker="o", linestyle="none", markersize=6.5,
                color=ctx.color_map.get(station, "gray"),
                label=label))
        fig.legend(
            handles=handles, **_legend_place(fig, ctx),
            frameon=False,
            prop={"family": "monospace", "size": FONTS["small"]},
            title="Station / instrument",
            title_fontsize=FONTS["small"],
            borderpad=0.7, handletextpad=0.7, labelspacing=0.55)
        return
    if counts.empty:
        return

    ranked = counts.sort_values(ascending=False)
    shown = ranked.iloc[:MAX_LEGEND_STATIONS]

    handles = []
    for station, count in shown.items():
        share = 100.0 * float(count) / float(ranked.sum())
        handles.append(
            plt.Line2D(
                [],
                [],
                marker="o",
                linestyle="none",
                markersize=6.5,
                color=ctx.color_map.get(station, "gray"),
                label=f"{station}  {fmt_count(int(count))} ({share:.1f}%)",
            )
        )

    extra = len(ranked) - len(shown)
    if extra > 0:
        handles.append(
            plt.Line2D(
                [],
                [],
                marker="",
                linestyle="none",
                label=f"+ {extra} other stations",
            )
        )

    fig.legend(
        handles=handles,
        **_legend_place(fig, ctx),
        frameon=False,
        fontsize=FONTS["small"],
        title="Station / instrument",
        title_fontsize=FONTS["small"],
        borderpad=0.7,
        handletextpad=0.7,
        labelspacing=0.55,
    )


def _no_data_message(ax, text: str = "No observations") -> None:
    ax.text(
        0.5,
        0.5,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=16,
        color="#888888",
        fontweight="bold",
    )


# -----------------------------------------------------------------------------
# Cartopy helpers
# -----------------------------------------------------------------------------

def _features_available() -> bool:
    """Check coastline availability once, without triggering network access."""
    global _FEATURES_OK

    if _FEATURES_OK is None:
        try:
            next(iter(cfeature.COASTLINE.geometries()))
            _FEATURES_OK = True
        except Exception as exc:
            _FEATURES_OK = False
            print(
                f"[mapobs] coastlines not drawn ({exc}); the cartopy cache "
                f"is empty and this node cannot download them",
                file=sys.stderr,
                flush=True,
            )

    return _FEATURES_OK


def _add_map_features(ax) -> None:
    if not _features_available():
        return

    ax.add_feature(
        cfeature.LAND,
        facecolor="#F6F7F8",
        edgecolor="none",
        zorder=0,
    )
    ax.add_feature(
        cfeature.OCEAN,
        facecolor="#EAF2F7",
        edgecolor="none",
        zorder=0,
    )
    ax.add_feature(
        cfeature.COASTLINE,
        lw=0.55,
        color="#90979D",
        zorder=1,
    )
    try:
        ax.add_feature(
            cfeature.BORDERS,
            lw=0.35,
            edgecolor="#B3B8BC",
            zorder=1,
        )
    except Exception:
        pass


# -----------------------------------------------------------------------------
# Panel: map
# -----------------------------------------------------------------------------

def _profiles(
    ax_hx,
    ax_hy,
    df,
    ctx: PlotContext,
    stations,
    pinned: bool,
):
    """Draw the longitude and latitude marginal profiles."""
    max_c_lon = max(int(ctx.max_counts[0]), 1)
    max_c_lat = max(int(ctx.max_counts[1]), 1)

    b_lon = np.linspace(ctx.lon_ext[0], ctx.lon_ext[1], N_BINS_LON)
    b_lat = np.linspace(ctx.lat_ext[0], ctx.lat_ext[1], N_BINS_LAT)

    colors = [ctx.color_map[s] for s in stations]
    ticks_lon = nice_ticks(max_c_lon)
    ticks_lat = nice_ticks(max_c_lat)

    if not df.empty and stations:
        lon_values = [
            df.loc[df["id_stn"] == station, "lon"].dropna()
            for station in stations
        ]
        lat_values = [
            df.loc[df["id_stn"] == station, "lat"].dropna()
            for station in stations
        ]

        ax_hx.hist(
            lon_values,
            bins=b_lon,
            color=colors,
            stacked=True,
            histtype="stepfilled",
            edgecolor="none",
            alpha=0.88,
        )

        if pinned:
            ax_hy.hist(
                lat_values,
                bins=b_lat,
                color=colors,
                stacked=True,
                orientation="horizontal",
                histtype="stepfilled",
                edgecolor="none",
                alpha=0.88,
            )
        else:
            ax_hy.hist(
                lat_values,
                bins=b_lat,
                color=colors,
                stacked=True,
                histtype="stepfilled",
                edgecolor="none",
                alpha=0.88,
            )

    ax_hx.set_xlim(ctx.lon_ext)
    ax_hx.set_ylim(0, ticks_lon[-1])
    ax_hx.set_yticks(ticks_lon)
    ax_hx.set_yticklabels(
        [fmt_count(t) for t in ticks_lon],
        fontsize=FONTS["tick"],
    )
    _panel_title(ax_hx, "Longitude profile")
    ax_hx.grid(axis="y", ls="--", alpha=0.28)
    ax_hx.tick_params(axis="x", labelsize=FONTS["tick"])

    if pinned:
        ax_hx.tick_params(labelbottom=False)

        ax_hy.set_ylim(ctx.lat_ext)
        ax_hy.set_xlim(0, ticks_lat[-1])
        ax_hy.set_xticks([ticks_lat[-1]])
        ax_hy.set_xticklabels(
            [fmt_count(ticks_lat[-1])],
            fontsize=FONTS["tick"],
        )
        ax_hy.tick_params(labelleft=False)
        ax_hy.grid(axis="x", ls="--", alpha=0.28)
    else:
        ax_hx.set_xlabel(
            "Longitude",
            fontsize=FONTS["label"],
            fontweight="bold",
        )

        ax_hy.set_xlim(ctx.lat_ext)
        ax_hy.set_ylim(0, ticks_lat[-1])
        ax_hy.set_yticks(ticks_lat)
        ax_hy.set_yticklabels(
            [fmt_count(t) for t in ticks_lat],
            fontsize=FONTS["tick"],
        )
        ax_hy.set_xlabel(
            "Latitude",
            fontsize=FONTS["label"],
            fontweight="bold",
        )
        ax_hy.tick_params(axis="x", labelsize=FONTS["tick"])
        ax_hy.grid(axis="y", ls="--", alpha=0.28)

    _panel_title(ax_hy, "Latitude profile")


def _panel_map(
    df,
    ctx: PlotContext,
    dt_start,
    dt_end,
    out_png: str,
    dpi: int,
) -> str:
    """Draw the geographic map with marginal longitude/latitude profiles."""
    counts = _station_counts(df, ctx.color_map)
    stations = counts.index.tolist()

    if ctx.square_map:
        fig = plt.figure(figsize=(12.8, 14.4), facecolor="white")

        gs = gridspec.GridSpec(
            2,
            2,
            figure=fig,
            height_ratios=[3.0, 0.80],
            wspace=0.18,
            hspace=0.18,
            left=0.06,
            right=0.97,
            top=_plot_top(fig, ctx),
            bottom=0.055,
        )

        ax_sc = fig.add_subplot(gs[0, :], projection=ctx.proj)
        ax_hx = fig.add_subplot(gs[1, 0])
        ax_hy = fig.add_subplot(gs[1, 1])
        pinned = False
    else:
        fig = plt.figure(figsize=(17.5, 9.6), facecolor="white")

        gs = gridspec.GridSpec(
            2,
            2,
            figure=fig,
            height_ratios=[0.20, 2.25],
            width_ratios=[4.8, 0.48],
            wspace=0.055,
            hspace=0.14,
            left=0.055,
            right=0.97,
            top=_plot_top(fig, ctx),
            bottom=0.065,
        )

        ax_hx = fig.add_subplot(gs[0, 0])
        ax_sc = fig.add_subplot(gs[1, 0], projection=ctx.proj)
        ax_hy = fig.add_subplot(gs[1, 1])
        pinned = True

    ax_sc.set_extent(ctx.extent, crs=ccrs.PlateCarree())

    if ctx.round_map:
        theta = np.linspace(0, 2 * np.pi, 240)
        boundary = np.column_stack(
            [
                0.5 + 0.5 * np.sin(theta),
                0.5 + 0.5 * np.cos(theta),
            ]
        )
        ax_sc.set_boundary(
            mpath.Path(boundary),
            transform=ax_sc.transAxes,
        )

    ax_sc.set_aspect("equal" if ctx.square_map else "auto")
    _add_map_features(ax_sc)

    gl = ax_sc.gridlines(
        draw_labels=True,
        linewidth=0.45,
        color="#8A9299",
        alpha=0.42,
        linestyle="--",
        x_inline=False,
        y_inline=ctx.round_map,
    )

    try:
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {"size": FONTS["tick"]}
        gl.ylabel_style = {"size": FONTS["tick"]}
    except Exception:                                  # pragma: no cover
        pass

    if df.empty:
        _no_data_message(ax_sc)
    else:
        s, alpha = dot_style(len(df))

        for station in stations:
            sub = df[df["id_stn"] == station]

            ax_sc.scatter(
                sub["lon"],
                sub["lat"],
                c=[ctx.color_map[station]],
                s=s,
                alpha=alpha,
                linewidths=0,
                transform=ccrs.PlateCarree(),
                rasterized=True,
                zorder=3,
            )

    _station_badge(ax_sc, counts)
    _profiles(ax_hx, ax_hy, df, ctx, stations, pinned)

    # For one station the colour key is obvious and a full legend adds noise.
    # For several stations, use the ranked compact legend.
    if len(stations) > 1:
        _station_legend(fig, ctx, counts)

    # Keep profile axes visually subordinate to the map.
    for profile_ax in (ax_hx, ax_hy):
        profile_ax.spines["top"].set_visible(False)
        profile_ax.spines["right"].set_visible(False)

    _header(fig, ctx, dt_start, dt_end, len(df), "map")

    save_figure(
        fig,
        out_png,
        svg=ctx.svg,
        dpi=dpi,
        facecolor="white",
    )
    plt.close(fig)
    return out_png


# -----------------------------------------------------------------------------
# Panel: cross-sections
# -----------------------------------------------------------------------------

def _panel_cross(
    df,
    ctx: PlotContext,
    dt_start,
    dt_end,
    out_png: str,
    dpi: int,
) -> str:
    """Draw zonal and meridional cross-sections."""
    levels = _levels_of(df, ctx)
    height = _level_height(len(levels)) if levels else 7.5
    tick_fs = _tick_font(len(levels), height)

    stations = _station_counts(df, ctx.color_map).index.tolist()
    s, alpha = dot_style(len(df))

    # --- CALCULATE VERTICAL OFFSETS ONCE ---
    # Al desplazar ligeramente los puntos hacia arriba o abajo en el eje Y,
    # logramos que no se tapen entre sí cuando comparten exactamente la misma
    # coordenada geográfica y el mismo canal/nivel.
    is_discrete = bool(levels)
    y_offsets = _vertical_offsets(stations, is_discrete, ctx.v_min, ctx.v_max)

    fig, (ax_z, ax_m) = plt.subplots(
        1,
        2,
        figsize=(16.5, height),
        facecolor="white",
    )

    if df.empty:
        _no_data_message(ax_z)
        _no_data_message(ax_m)
    else:
        row_of = {lev: i for i, lev in enumerate(levels)}

        def _y(sub):
            if not levels:
                return sub["vcoord"]

            key = (
                sub["vcoord"].astype(int)
                if ctx.is_channel
                else sub["vcoord"]
            )
            return key.map(row_of)

        for ax, coord, title, xlim in (
            (ax_z, "lat", "Zonal cross-section", ctx.lat_ext),
            (ax_m, "lon", "Meridional cross-section", ctx.lon_ext),
        ):
            for station in stations:
                sub = df[df["id_stn"] == station]

                # Las observaciones se dibujan en su Lat/Lon exacto (X).
                # El desplazamiento es únicamente vertical (Y) dentro de su propio nivel.
                x = sub[coord]
                y = _y(sub) + y_offsets[station]

                ax.scatter(
                    x,
                    y,
                    c=[ctx.color_map[station]],
                    s=s,
                    alpha=alpha,
                    linewidths=0,
                    rasterized=True,
                )

            ax.set_xlim(xlim)
            _set_vertical_axis(ax, levels, ctx, tick_fs)

            ax.set_xlabel(
                "Latitude" if coord == "lat" else "Longitude",
                fontsize=FONTS["label"],
                fontweight="bold",
            )
            ax.set_ylabel(
                _vlabel(ctx),
                fontsize=FONTS["label"],
                fontweight="bold",
            )
            _panel_title(ax, title)
            ax.tick_params(axis="x", labelsize=FONTS["tick"])
            ax.grid(True, ls="--", alpha=0.30)

    _station_badge(ax_z, _station_counts(df, ctx.color_map))

    if len(stations) > 1:
        _station_legend(fig, ctx, _station_counts(df, ctx.color_map))

    _header(fig, ctx, dt_start, dt_end, len(df), "cross-sections")

    # Explicitly reserve the header band.  This is critical for tall channel
    # figures where Matplotlib otherwise pushes the axes title upward.
    top = _plot_top(fig, ctx)
    bottom = min(0.075, 0.9 / height)

    fig.subplots_adjust(
        left=0.065,
        right=0.97,
        top=top,
        bottom=bottom,
        wspace=0.25,
    )

    save_figure(
        fig,
        out_png,
        svg=ctx.svg,
        dpi=dpi,
        facecolor="white",
    )
    plt.close(fig)
    return out_png


# -----------------------------------------------------------------------------
# Panel: vertical distribution
# -----------------------------------------------------------------------------

def _panel_vertical(
    df,
    ctx: PlotContext,
    dt_start,
    dt_end,
    out_png: str,
    dpi: int,
) -> str:
    """Draw observation count per level or channel."""
    levels = _levels_of(df, ctx)
    height = _level_height(len(levels)) if levels else 7.5
    tick_fs = _tick_font(len(levels), height)

    max_c_v = max(int(ctx.max_counts[2]), 1)

    stations = _station_counts(df, ctx.color_map).index.tolist()

    fig, ax = plt.subplots(
        figsize=(13.5, height),
        facecolor="white",
    )

    if df.empty:
        _no_data_message(ax)
    elif levels:
        key = (
            df["vcoord"].astype(int)
            if ctx.is_channel
            else df["vcoord"]
        )

        pivot = pd.crosstab(
            key,
            df["id_stn"],
        ).reindex(
            index=levels,
            fill_value=0,
        )

        rows = np.arange(len(levels))
        left = np.zeros(len(levels))

        totals = pivot.sum(axis=1).to_numpy()

        for i, (row, total) in enumerate(zip(rows, totals)):
            if i % 2 == 0:
                ax.axhspan(
                    row - 0.5,
                    row + 0.5,
                    facecolor="#F5F6F7",
                    edgecolor="none",
                    zorder=0,
                )

        for station in stations:
            if station not in pivot.columns:
                continue

            values = pivot[station].to_numpy()

            ax.barh(
                rows,
                values,
                left=left,
                height=0.78,
                color=ctx.color_map[station],
                edgecolor="none",
                alpha=0.90,
                zorder=2,
            )
            left += values

        if len(levels) <= MAX_VALUE_LABELS:
            label_step = 1
        else:
            label_step = max(
                1,
                int(np.ceil(len(levels) / MAX_VALUE_LABELS)),
            )

        annotation_limit = max(max_c_v, int(np.nanmax(totals)))
        for row, total in zip(rows[::label_step], totals[::label_step]):
            total = int(total)
            if total <= 0:
                continue

            # Add labels outside the bar only when there is enough visual
            # headroom; otherwise the x-axis carries the exact value.
            ax.text(
                total + annotation_limit * 0.012,
                row,
                fmt_count(total),
                va="center",
                fontsize=max(tick_fs, 6.0),
                color="#333333",
                clip_on=False,
            )

    else:
        bins = np.linspace(
            float(ctx.v_min),
            float(ctx.v_max),
            N_BINS_VCONT,
        )

        values = [
            df.loc[df["id_stn"] == station, "vcoord"].dropna()
            for station in stations
        ]

        ax.hist(
            values,
            bins=bins,
            stacked=True,
            orientation="horizontal",
            color=[ctx.color_map[s] for s in stations],
            edgecolor="none",
            alpha=0.90,
        )

    actual_max = max_c_v
    if not df.empty:
        actual_max = max(
            actual_max,
            int(df.shape[0]),
            1,
        )

    ticks = nice_ticks(actual_max)
    ax.set_xlim(0, ticks[-1])
    ax.set_xticks(ticks)
    ax.set_xticklabels(
        [fmt_count(t) for t in ticks],
        fontsize=FONTS["tick"],
    )

    _set_vertical_axis(ax, levels, ctx, tick_fs)

    ax.set_xlabel(
        "Observation count",
        fontsize=FONTS["label"],
        fontweight="bold",
    )
    ax.set_ylabel(
        _vlabel(ctx),
        fontsize=FONTS["label"],
        fontweight="bold",
    )

    _panel_title(
        ax,
        "Observation count by level" if levels else "Vertical distribution",
    )

    ax.grid(
        True,
        axis="x",
        ls="--",
        alpha=0.30,
        zorder=1,
    )

    counts = _station_counts(df, ctx.color_map)
    _station_badge(ax, counts)

    if len(stations) > 1:
        _station_legend(fig, ctx, counts)

    _header(fig, ctx, dt_start, dt_end, len(df), "vertical distribution")

    top = _plot_top(fig, ctx)
    bottom = min(0.075, 0.9 / height)

    fig.subplots_adjust(
        left=0.10,
        right=0.97,
        top=top,
        bottom=bottom,
    )

    save_figure(
        fig,
        out_png,
        svg=ctx.svg,
        dpi=dpi,
        facecolor="white",
    )
    plt.close(fig)
    return out_png


# -----------------------------------------------------------------------------
# Panel: station contributions
# -----------------------------------------------------------------------------

def _panel_stations(
    df,
    ctx: PlotContext,
    dt_start,
    dt_end,
    out_png: str,
    dpi: int,
) -> str:
    """Draw station/instrument observation contributions."""
    counts = _station_counts(df, ctx.color_map)
    # every station of the period, in one order (by name, the first on top),
    # a bar of 0 when it has nothing here: in the play the panel holds still,
    # its bars in place and its height the same
    names = sorted(ctx.color_map, reverse=True) or ["No observations"]
    values = [int(counts.get(n, 0)) if not counts.empty else 0 for n in names]

    height = float(
        np.clip(
            2.8 + 0.48 * len(names),
            4.3,
            40.0,
        )
    )

    fig, ax = plt.subplots(
        figsize=(13.0, height),
        facecolor="white",
    )

    colors = [
        ctx.color_map.get(name, "#B5BBC0")
        for name in names
    ]

    ax.barh(
        names,
        values,
        color=colors,
        edgecolor="none",
        height=0.70,
        alpha=0.92,
    )

    max_value = max(
        max(values) if values else 1,
        int(ctx.max_counts[3]),
        1,
    )

    ticks = nice_ticks(max_value)
    x_upper = ticks[-1]

    if max(values, default=0) > 0:
        # Leave enough room for the annotation after the final bar.
        annotation_target = int(
            np.ceil(max(values) * 1.14)
        )
        x_upper = max(x_upper, nice_ticks(annotation_target)[-1])

    ax.set_xlim(0, x_upper)
    ax.set_xticks(nice_ticks(x_upper)[::1])
    ax.set_xticklabels(
        [fmt_count(t) for t in ax.get_xticks()],
        fontsize=FONTS["tick"],
    )

    ax.tick_params(
        axis="y",
        labelsize=FONTS["tick"],
    )

    ax.set_xlabel(
        "Total observations",
        fontsize=FONTS["label"],
        fontweight="bold",
    )

    _panel_title(
        ax,
        "Observation contribution by station / instrument",
    )

    ax.grid(
        True,
        axis="x",
        ls="--",
        alpha=0.30,
    )

    total = sum(values)

    for i, value in enumerate(values):
        if value <= 0 or total <= 0:
            continue

        percentage = 100.0 * value / total

        label = (
            f"{fmt_count(value)}  ({percentage:.1f}%)"
        )

        # Place large-bar labels inside the bar.  This avoids a very long
        # empty right-hand margin when one station dominates.
        if x_upper > 0 and value / x_upper >= 0.22:
            ax.text(
                value * 0.985,
                i,
                label,
                va="center",
                ha="right",
                fontsize=FONTS["tick"],
                fontweight="bold",
                color="white",
            )
        else:
            ax.text(
                value + x_upper * 0.012,
                i,
                label,
                va="center",
                fontsize=FONTS["tick"],
                fontweight="bold",
                color="#333333",
            )

    ax.text(
        0.995,
        0.015,
        f"Total = {fmt_count(total)}",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=FONTS["small"],
        color="#666666",
    )

    _header(fig, ctx, dt_start, dt_end, len(df), "contributions")

    fig.subplots_adjust(
        left=0.17,
        right=0.93,
        top=_plot_top(fig),
        bottom=0.10,
    )

    save_figure(
        fig,
        out_png,
        svg=ctx.svg,
        dpi=dpi,
        facecolor="white",
    )
    plt.close(fig)
    return out_png


# -----------------------------------------------------------------------------
# Combined output
# -----------------------------------------------------------------------------

def _combine_panels(
    paths: Sequence[str],
    out_png: str,
) -> Optional[str]:
    """Stack panels while preserving their natural aspect ratios."""
    try:
        from PIL import Image
    except ImportError:                                  # pragma: no cover
        print(
            "[mapobs] the combined panel needs pillow; skipped",
            file=sys.stderr,
            flush=True,
        )
        return None

    images = []

    try:
        for path in paths:
            if not os.path.isfile(path):
                continue

            im = Image.open(path).convert("RGB")

            if im.width != COMBINED_MAX_WIDTH:
                height = round(
                    im.height * COMBINED_MAX_WIDTH / im.width
                )
                im = im.resize(
                    (COMBINED_MAX_WIDTH, height),
                    resample=Image.Resampling.LANCZOS,
                )

            images.append(im)

        if not images:
            return None

        total_height = sum(im.height for im in images)

        sheet = Image.new(
            "RGB",
            (COMBINED_MAX_WIDTH, total_height),
            "white",
        )

        y = 0
        for im in images:
            sheet.paste(im, (0, y))
            y += im.height
            im.close()

        sheet.save(
            out_png,
            optimize=True,
        )
        sheet.close()

        return out_png

    except Exception as exc:
        print(
            f"[mapobs] could not combine the panels: {exc}",
            file=sys.stderr,
            flush=True,
        )
        return None


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------

_PANEL_FUNCS = {
    "map": _panel_map,
    "cross": _panel_cross,
    "vertical": _panel_vertical,
    "stations": _panel_stations,
}


def plot_panels(
    df: pd.DataFrame,
    dt_start,
    dt_end,
    out_dir: str,
    stem: str,
    ctx: PlotContext,
    is_total: bool = False,
    panels: Sequence[str] = PANELS,
) -> Dict[str, str]:
    """Write one PNG per requested panel and optionally the combined image.

    The public interface is intentionally unchanged.
    """
    dpi = DPI_HIGH if is_total else DPI_LOW

    os.makedirs(out_dir, exist_ok=True)

    wanted = [
        panel
        for panel in panels
        if panel in PANELS
    ]

    combine = COMBINED in panels

    if combine and not wanted:
        wanted = list(PANELS)

    out: Dict[str, str] = {}

    for panel in wanted:
        path = os.path.join(
            out_dir,
            f"{panel}_{stem}.png",
        )

        out[panel] = _PANEL_FUNCS[panel](
            df,
            ctx,
            dt_start,
            dt_end,
            path,
            dpi,
        )

    if combine:
        sheet = _combine_panels(
            [
                out[panel]
                for panel in PANELS
                if panel in out
            ],
            os.path.join(
                out_dir,
                f"{COMBINED}_{stem}.png",
            ),
        )

        if sheet:
            out[COMBINED] = sheet

        # Panels used only to construct the combined output are removed when
        # they were not explicitly requested.
        for panel in list(out):
            if panel != COMBINED and panel not in panels:
                try:
                    os.remove(out.pop(panel))
                except OSError:
                    pass

    gc.collect()
    return out


def plot_empty_map(ctx: PlotContext, path: str, dt_start, dt_end,
                   message: str) -> str:
    """The map of a projection with nothing on it: a region that has no
    observation there. The header of the other figures, the coasts, and the
    message in the middle."""
    fig = plt.figure(figsize=(16, 9))
    top = _plot_top(fig)
    if _HAS_CARTOPY and ctx.proj is not None:
        ax = fig.add_axes([0.05, 0.05, 0.90, top - 0.08], projection=ctx.proj)
        ax.set_extent(ctx.extent, crs=ccrs.PlateCarree())
        _add_map_features(ax)
    else:
        ax = fig.add_axes([0.05, 0.05, 0.90, top - 0.08])
        ax.set_xticks([])
        ax.set_yticks([])
    ax.text(0.5, 0.5, message, transform=ax.transAxes, ha="center",
            va="center", fontsize=14, color="#52606D",
            bbox=dict(boxstyle="round,pad=0.7", fc="white", ec="#D9DDE2"))
    _header(fig, ctx, dt_start, dt_end, 0, "map")
    fig.savefig(path, dpi=DPI_LOW)
    plt.close(fig)
    return path
