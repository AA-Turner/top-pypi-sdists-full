# -*- coding: utf-8 -*-
"""PyGMT ``grdimage`` maps for the season monitor (DESIGN.md section 8).

Every other map family in ``geocif/viz`` is a vector choropleth over admin
polygons; this one paints the 0.05 degree pixel field itself, which is the
whole point of the phenology product (DESIGN section 11.2: region means
destroy the onset signal in topographically diverse regions).

Shape of the module
-------------------
* :func:`raster_map` is the ONE low-level skeleton -- basemap, NODATA land,
  CPT, grid, admin outlines, national borders, colourbar, save. It is the only
  place in this file that touches pygmt or opens a figure, so a styling fix
  lands on every map at once (same argument as ``s2s_africa._value_map``).
* Everything above it is a pure function: limits, CPT keyword building, titles,
  file stems, companion-CSV summaries. Those carry all the decisions and are
  unit-tested without GMT.
* Each public map function renders one layer and returns a
  ``(png_file, csv_file, description)`` row for
  :func:`geocif.viz.aggregation._write_lookup`; ``png_file`` is relative to the
  plots directory and ``csv_file`` to the csvs directory, matching that helper.

Conventions
-----------
* ``import pygmt`` happens INSIDE the drawing function: this module must import
  on a machine with no GMT C library (the tests below run there).
* Style constants come only from :mod:`geocif.viz._style`.
* Units: onset/cessation layers are **days since the calendar planting start**
  of the season (the phenology package's index convention), anomalies are
  **days** (positive = late), probabilities are **0..1**, percentiles
  **0..100**, ``onset_n_valid`` is a **count of years**. Grids are indexed
  ``(row, col)`` with row 0 the NORTHERNMOST row, matching
  ``geocif.phenology.inputs.pixel_centres``.
* NaN means "nothing to show here": it renders transparent over the NODATA
  grey land fill, so non-cropland and nodata read identically and neither
  reads as a value.

False starts
------------
``core.season_phenology`` counts ALL candidate episodes before onset, while
``core.onset_state`` counts only INVALIDATED episodes. This module uses the
INVALIDATED-episode meaning everywhere -- see the comment on
:data:`FALSE_START_RATE_LAYER`.
"""

from __future__ import annotations

import logging
import tempfile
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Optional, Sequence

import numpy as np
import pandas as pd
import xarray as xr

from geocif.phenology.core import SeasonState
from geocif.viz._style import (
    AREA_THRESH,
    BORDER_PEN,
    CBAR_POS,
    COAST_KW,
    NODATA,
    POLY_PEN,
)
from geocif.viz.aggregation import _display_name, _write_lookup

logger = logging.getLogger(__name__)

#: Mercator width of every map in this family.
PROJECTION: str = "M12c"

#: Raster figures need more dots than a choropleth; 350 matches the outlook maps.
DEFAULT_DPI: int = 350

#: Grid spacing in degrees, used only to pad the plot region by half a pixel.
#: Mirrors ``geocif.phenology.inputs.GRID_RES``; not imported from there because
#: that module pulls in rasterio/geopandas/openpyxl and this one stays light.
#: Only a fallback -- the spacing is inferred from the coordinates when it can be.
FALLBACK_RES: float = 0.05

#: House rule, encoded here first (DESIGN section 8): admin zone tokens never
#: reach a figure in their config spelling.
SCALE_LABEL: dict[str, str] = {"admin_1": "Admin 1", "admin_2": "Admin 2"}

#: The climatology layer counting INVALIDATED onset episodes per year, i.e. the
#: ``core.onset_state`` meaning of "false start", NOT the all-candidates count
#: that ``core.season_phenology`` reports under the same name. The name says
#: rate because the layer is episodes-per-year averaged over the record.
FALSE_START_RATE_LAYER: str = "false_start_rate"

#: Categorical palette for :class:`~geocif.phenology.core.SeasonState`.
#: BEFORE_WINDOW is deliberately NOT grey: grey is NODATA on these maps
#: (non-cropland, no data), so a grey state would be unreadable against it.
#: A pale desaturated blue reads as "nothing has happened yet" without
#: colliding with the land fill or with any of the five live states.
STATE_COLORS: dict[int, str] = {
    int(SeasonState.BEFORE_WINDOW): "#c6dbef",  # pale blue -- NOT grey
    int(SeasonState.NOT_STARTED): "#fdd49e",  # pale orange
    int(SeasonState.FALSE_START): "#e34a33",  # red
    int(SeasonState.PROVISIONAL): "#fee08b",  # yellow
    int(SeasonState.CONFIRMED): "#1a9850",  # green
    int(SeasonState.NO_ONSET): "#762a83",  # purple
}

#: Colourbar labels for the six states. No commas: GMT splits the categorical
#: colour model on commas.
STATE_LABELS: dict[int, str] = {
    int(SeasonState.BEFORE_WINDOW): "Before window",
    int(SeasonState.NOT_STARTED): "Not started",
    int(SeasonState.FALSE_START): "False start",
    int(SeasonState.PROVISIONAL): "Provisional",
    int(SeasonState.CONFIRMED): "Confirmed",
    int(SeasonState.NO_ONSET): "No onset",
}

#: Title font bounds (points) and the mean Helvetica glyph width as a fraction
#: of the font size, used to keep a long title inside the map width.
TITLE_MAX_PT: float = 14.0
TITLE_MIN_PT: float = 8.0
_CHAR_WIDTH_RATIO: float = 0.52

#: Nice tick spacings (days) for a date-labelled colourbar.
_NICE_DAY_STEPS: tuple[int, ...] = (5, 10, 15, 20, 30, 45, 60, 90, 120)


# ---------------------------------------------------------------------------
# palette specification
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class CmapSpec:
    """One CPT request.

    Args:
        cmap: a GMT master CPT name (``viridis``, ``polar``, ``hot``) or a
            comma-joined list of colours for a categorical palette.
        series: ``(min, max)`` for a continuous ramp or ``(min, max, step)``
            for discrete boxes, in the layer's own units.
        continuous: blend between colours (ignored for categorical palettes).
        reverse: flip the ramp.
    """

    cmap: str
    series: tuple[float, ...]
    continuous: bool = True
    reverse: bool = False


def makecpt_kwargs(spec: CmapSpec, categorical: Optional[Sequence[str]] = None) -> dict:
    """Keyword arguments for ``pygmt.makecpt`` from a :class:`CmapSpec`.

    Args:
        spec: the palette request.
        categorical: colourbar labels, one per discrete class. When given the
            palette is built with GMT's categorical colour model and the
            continuous/background options are dropped (they make no sense for
            classes, and ``background`` would grow out-of-range extenders on a
            bar whose classes are exhaustive).

    Returns:
        dict ready to splat into ``pygmt.makecpt``.
    """
    kwargs: dict[str, Any] = {"cmap": spec.cmap, "series": list(spec.series)}
    if categorical:
        # commas out FIRST, then gmt_safe collapses the whitespace it leaves
        labels = [gmt_safe(str(label).replace(",", " ")) for label in categorical]
        kwargs["color_model"] = "+c" + ",".join(labels)
    elif spec.continuous:
        # -Z only does something when -T carries an increment; with a bare
        # min/max GMT warns "Without inc in -T option, -Z has no effect"
        # and the ramp is continuous anyway
        if len(spec.series) >= 3:
            kwargs["continuous"] = True
        kwargs["background"] = True
    if spec.reverse:
        kwargs["reverse"] = True
    return kwargs


def colorbar_kwargs(
    cbar_label: str,
    categorical: Optional[Sequence[str]] = None,
    annot_file: Optional[Any] = None,
) -> dict:
    """Keyword arguments for ``pygmt.Figure.colorbar``.

    Args:
        cbar_label: axis label, plain text with its units.
        categorical: class labels; when given the bar carries no out-of-range
            extenders.
        annot_file: path to a GMT custom-annotation file (lines
            ``<value> a <label>``), used for the date-labelled onset bars.

    Returns:
        dict with ``position`` and ``frame``.
    """
    frame = [f"x+l{gmt_safe(str(cbar_label))}"]
    if annot_file is not None:
        frame.insert(0, f"xc{annot_file}")
    position = CBAR_POS if categorical else CBAR_POS + "+e"
    return {"position": position, "frame": frame}


def state_cmap_spec() -> tuple[CmapSpec, list[str]]:
    """Palette and labels for the six-state season monitor layer.

    Returns:
        ``(spec, labels)`` where ``spec`` holds one discrete box per
        :class:`~geocif.phenology.core.SeasonState` in code order.
    """
    codes = sorted(STATE_COLORS)
    colors = [STATE_COLORS[c] for c in codes]
    labels = [STATE_LABELS[c] for c in codes]
    spec = CmapSpec(
        cmap=",".join(colors),
        series=(float(codes[0]), float(codes[-1]), 1.0),
        continuous=False,
    )
    return spec, labels


# ---------------------------------------------------------------------------
# pure decisions: limits, ticks, text, grids
# ---------------------------------------------------------------------------
def gmt_safe(text: str) -> str:
    """Strip characters GMT renders literally or mis-parses in ``+t``/``+l``.

    A double quote inside a GMT modifier is drawn as a glyph, so a shell-style
    quoted title appears on the canvas with its quotes. Newlines would break
    the argument. Both are removed rather than escaped.

    Args:
        text: raw title or label.

    Returns:
        The same text with double quotes removed and whitespace collapsed.
    """
    cleaned = str(text).replace('"', "").replace("\n", " ").replace("\r", " ")
    return " ".join(cleaned.split())


def _projection_width_cm() -> float:
    """Map width in centimetres parsed out of :data:`PROJECTION` (``M12c``)."""
    digits = "".join(c for c in PROJECTION if c.isdigit() or c == ".")
    return float(digits) if digits else 12.0


def title_font(title: str, width_cm: float = 12.0) -> str:
    """GMT ``FONT_TITLE`` sized so the title stays inside the map width.

    ``savefig`` crops the canvas to its content, so an over-wide title widens
    the PNG rather than being cut off -- but a title running past the map frame
    reads as a mistake. Shrinking it is the cheap fix; the floor keeps it
    legible on the longest country + crop + layer combinations.

    Args:
        title: the final title text.
        width_cm: map width in centimetres (the ``M...c`` projection width).

    Returns:
        A GMT font string, e.g. ``11.5p,Helvetica,black``.
    """
    width_pt = float(width_cm) * 72.0 / 2.54
    n_chars = max(1, len(gmt_safe(title)))
    size = width_pt / (n_chars * _CHAR_WIDTH_RATIO)
    size = min(TITLE_MAX_PT, max(TITLE_MIN_PT, size))
    return f"{size:.1f}p,Helvetica,black"


def symmetric_limits(
    values: np.ndarray, minimum: float = 5.0, step: float = 5.0
) -> tuple[float, float]:
    """Symmetric limits for a diverging layer, rounded out to ``step``.

    Args:
        values: layer in its own units (days for the onset anomaly). NaN ignored.
        minimum: smallest half-range returned, so a near-flat field still gets a
            readable bar.
        step: limits are rounded outward to a multiple of this.

    Returns:
        ``(-limit, +limit)``; ``(-minimum, +minimum)`` when nothing is finite.
    """
    arr = np.asarray(values, dtype=np.float64)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        logger.warning("symmetric_limits: layer has no finite pixels; using the floor")
        return -float(minimum), float(minimum)
    peak = float(np.max(np.abs(finite)))
    limit = max(float(minimum), float(np.ceil(peak / step) * step))
    return -limit, limit


def sequential_limits(
    values: np.ndarray,
    lower_pct: float = 2.0,
    upper_pct: float = 98.0,
    minimum_span: float = 1.0,
    step: Optional[float] = None,
) -> tuple[float, float]:
    """Robust limits for a sequential layer.

    Percentile clipping keeps a handful of extreme pixels from flattening the
    whole ramp (arid pixels routinely carry 100+ day onset anomalies).

    Args:
        values: layer in its own units. NaN ignored.
        lower_pct: percentile mapped to the low end of the ramp.
        upper_pct: percentile mapped to the high end.
        minimum_span: if the clipped range is narrower than this it is widened
            symmetrically about its midpoint.
        step: when given, limits are rounded outward to a multiple of it.

    Returns:
        ``(low, high)``; ``(0.0, minimum_span)`` when nothing is finite.
    """
    arr = np.asarray(values, dtype=np.float64)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        logger.warning("sequential_limits: layer has no finite pixels; using 0..span")
        return 0.0, float(minimum_span)
    low = float(np.percentile(finite, lower_pct))
    high = float(np.percentile(finite, upper_pct))
    if high - low < minimum_span:
        mid = 0.5 * (low + high)
        low, high = mid - minimum_span / 2.0, mid + minimum_span / 2.0
    if step:
        low = float(np.floor(low / step) * step)
        high = float(np.ceil(high / step) * step)
        if high - low < step:
            high = low + step
    return low, high


def nice_day_step(span: float, n_ticks: int = 6) -> int:
    """Smallest tabulated tick spacing (days) giving at most ``n_ticks`` ticks.

    Args:
        span: range of the colourbar in days.
        n_ticks: target number of annotated ticks.

    Returns:
        One of :data:`_NICE_DAY_STEPS` (the largest when none is coarse enough).
    """
    raw = max(1.0, float(span) / max(1, int(n_ticks)))
    for candidate in _NICE_DAY_STEPS:
        if candidate >= raw:
            return int(candidate)
    return int(_NICE_DAY_STEPS[-1])


def date_tick_annotations(
    low: float,
    high: float,
    reference: date,
    step: Optional[int] = None,
    n_ticks: int = 6,
) -> list[tuple[int, str]]:
    """Colourbar ticks for a layer measured in days since ``reference``.

    Args:
        low: low end of the colourbar, days since ``reference``.
        high: high end, days since ``reference``.
        reference: the day that value 0 means (the calendar planting start).
        step: tick spacing in days; inferred from the span when omitted.
        n_ticks: target tick count when ``step`` is inferred.

    Returns:
        ``[(days, "DD Mon"), ...]`` ascending, every tick inside ``[low, high]``.
    """
    step = int(step) if step else nice_day_step(high - low, n_ticks)
    first = int(np.ceil(low / step) * step)
    ticks: list[tuple[int, str]] = []
    value = first
    while value <= high + 1e-9:
        label = (reference + timedelta(days=int(value))).strftime("%d %b")
        ticks.append((int(value), label))
        value += step
    return ticks


def write_annotation_file(path: Any, ticks: Sequence[tuple[int, str]]) -> Path:
    """Write a GMT custom-annotation file (``<value> a <label>`` per line).

    Args:
        path: destination file.
        ticks: output of :func:`date_tick_annotations`.

    Returns:
        The path written.
    """
    out = Path(path)
    out.write_text(
        "".join(f"{value} a {gmt_safe(label)}\n" for value, label in ticks),
        encoding="utf-8",
    )
    return out


def grid_from_array(values: np.ndarray, lon: np.ndarray, lat: np.ndarray) -> xr.DataArray:
    """Wrap a ``(rows, cols)`` layer as an ``xarray`` grid for ``grdimage``.

    Args:
        values: layer indexed ``(row, col)``, row 0 = northernmost row, in its
            own units. Cast to float32 so NaN survives.
        lon: pixel-centre longitudes, shape ``(cols,)``, degrees east.
        lat: pixel-centre latitudes, shape ``(rows,)``, degrees north,
            north -> south (the order ``inputs.pixel_centres`` returns).

    Returns:
        ``xr.DataArray`` with dims ``("lat", "lon")``.
    """
    arr = np.asarray(values, dtype=np.float32)
    if arr.shape != (len(lat), len(lon)):
        raise ValueError(
            f"grid shape {arr.shape} does not match coordinates "
            f"({len(lat)}, {len(lon)})"
        )
    return xr.DataArray(
        arr,
        coords={
            "lat": np.asarray(lat, dtype=np.float64),
            "lon": np.asarray(lon, dtype=np.float64),
        },
        dims=("lat", "lon"),
    )


def region_from_grid(lon: np.ndarray, lat: np.ndarray) -> list[float]:
    """Plot region ``[west, east, south, north]`` padded half a pixel.

    Args:
        lon: pixel-centre longitudes, degrees east.
        lat: pixel-centre latitudes, degrees north.

    Returns:
        ``[w, e, s, n]`` in degrees, the pixel EDGES of the window.
    """
    lon = np.asarray(lon, dtype=np.float64)
    lat = np.asarray(lat, dtype=np.float64)
    dx = float(abs(lon[1] - lon[0])) if lon.size > 1 else FALLBACK_RES
    dy = float(abs(lat[1] - lat[0])) if lat.size > 1 else FALLBACK_RES
    return [
        float(lon.min() - dx / 2.0),
        float(lon.max() + dx / 2.0),
        float(lat.min() - dy / 2.0),
        float(lat.max() + dy / 2.0),
    ]


def state_to_float(state: np.ndarray, nodata: int = -1) -> np.ndarray:
    """Int8 :class:`~geocif.phenology.core.SeasonState` codes -> float with NaN.

    Args:
        state: ``(rows, cols)`` int array of state codes.
        nodata: code meaning "no state"; anything outside the enum is also NaN.

    Returns:
        float32 array, NaN where the pixel has no state.
    """
    arr = np.asarray(state)
    out = arr.astype(np.float32)
    codes = sorted(STATE_LABELS)
    bad = (arr == nodata) | (arr < codes[0]) | (arr > codes[-1])
    out[bad] = np.nan
    return out


def mask_display(values: np.ndarray, keep: Optional[np.ndarray]) -> np.ndarray:
    """Blank pixels outside the display mask (``mask_to_cropland``).

    Every layer is COMPUTED on all land pixels and masked here, so the mask can
    change without recomputing (DESIGN section 8.1).

    Args:
        values: layer in its own units.
        keep: boolean ``(rows, cols)``; True = show. ``None`` = show everything.

    Returns:
        float32 copy with NaN outside ``keep``.
    """
    out = np.array(values, dtype=np.float32, copy=True)
    if keep is None:
        return out
    out[~np.asarray(keep, dtype=bool)] = np.nan
    return out


# ---------------------------------------------------------------------------
# naming
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MapContext:
    """Everything the maps of one (country, crop, season) run share.

    Args:
        lon: pixel-centre longitudes, degrees east, shape ``(cols,)``.
        lat: pixel-centre latitudes, degrees north, shape ``(rows,)``,
            north -> south.
        dir_plots: directory for the PNGs.
        dir_csvs: directory for the companion CSVs.
        country: config token (``kenya``).
        crop: config token (``maize``).
        season: season number from the crop calendar.
        asof: last observed day for the monitor maps; ``None`` for climatology.
        years: ``(first, last)`` harvest year of the climatology; ``None`` for
            the monitor maps.
        admin_gdf: admin outlines in EPSG:4326, or ``None``.
        scale: admin zone token, keyed into :data:`SCALE_LABEL`.
        dpi: raster resolution of the saved PNG.
    """

    lon: np.ndarray
    lat: np.ndarray
    dir_plots: Any
    dir_csvs: Any
    country: str
    crop: str
    season: int
    harvest_year: Optional[int] = None
    asof: Optional[date] = None
    years: Optional[tuple[int, int]] = None
    admin_gdf: Any = None
    scale: str = "admin_1"
    dpi: int = DEFAULT_DPI


def scale_label(scale: str) -> str:
    """Display form of an admin zone token (``admin_1`` -> ``Admin 1``)."""
    token = str(scale).strip().lower()
    if token in SCALE_LABEL:
        return SCALE_LABEL[token]
    return _display_name(token)


def through_text(ctx: MapContext) -> str:
    """The data-vintage clause every title carries.

    Returns:
        ``data through 14 Sep 2026`` for a monitor map, ``1981-2025`` for a
        climatology map, ``""`` when the context states neither.
    """
    if ctx.asof is not None:
        return f"data through {ctx.asof.day} {ctx.asof.strftime('%b %Y')}"
    if ctx.years is not None:
        return f"{int(ctx.years[0])}-{int(ctx.years[1])}"
    return ""


def map_stem(layer: str, ctx: MapContext) -> str:
    """File stem shared by a map and its companion CSV.

    ``{layer}_{country}_{crop}_s{season}[_hy{YEAR}]_asof{YYYYMMDD}``;
    climatology maps carry the year span instead of an as-of date.

    ``harvest_year`` is part of a monitor stem because two harvest years of one
    season can be active on the same as-of date, and without it the second run
    overwrites the first's maps and companion CSVs. It matches the raster stem
    built by ``geocif.season_monitor.file_stem``.
    """
    base = f"{layer}_{ctx.country}_{ctx.crop}_s{int(ctx.season)}"
    if ctx.harvest_year is not None:
        base = f"{base}_hy{int(ctx.harvest_year)}"
    if ctx.asof is not None:
        return f"{base}_asof{ctx.asof.strftime('%Y%m%d')}"
    if ctx.years is not None:
        return f"{base}_{int(ctx.years[0])}_{int(ctx.years[1])}"
    return base


def map_title(layer_label: str, ctx: MapContext) -> str:
    """Short factual title: what, where, when. No prose, no quotes.

    Example: ``Kenya Maize Season State, Admin 1, data through 14 Sep 2026``.
    """
    parts = [
        f"{_display_name(ctx.country)} {_display_name(ctx.crop)} {layer_label}",
        scale_label(ctx.scale),
    ]
    through = through_text(ctx)
    if through:
        parts.append(through)
    return gmt_safe(", ".join(parts))


# ---------------------------------------------------------------------------
# companion tables
# ---------------------------------------------------------------------------
def pixel_summary(values: np.ndarray, units: str = "") -> pd.DataFrame:
    """Per-pixel distribution of a layer, for maps with no zonal table.

    Args:
        values: the plotted layer (already display-masked), in its own units.
        units: units string carried into the table.

    Returns:
        Long DataFrame ``statistic, value, units``: pixel counts, the valid
        share, the 0/10/25/50/75/90/100 percentiles and the mean.
    """
    arr = np.asarray(values, dtype=np.float64)
    finite = arr[np.isfinite(arr)]
    n_total = int(arr.size)
    n_valid = int(finite.size)
    stats: list[tuple[str, float]] = [
        ("n_pixels", float(n_total)),
        ("n_valid", float(n_valid)),
        ("n_nodata", float(n_total - n_valid)),
        ("valid_share", (n_valid / n_total) if n_total else float("nan")),
    ]
    names = ("minimum", "p10", "p25", "median", "p75", "p90", "maximum")
    quantiles = (0.0, 10.0, 25.0, 50.0, 75.0, 90.0, 100.0)
    for name, q in zip(names, quantiles):
        stats.append(
            (name, float(np.percentile(finite, q)) if n_valid else float("nan"))
        )
    stats.append(("mean", float(finite.mean()) if n_valid else float("nan")))
    return pd.DataFrame(
        {
            "statistic": [s for s, _ in stats],
            "value": [v for _, v in stats],
            "units": [units] * len(stats),
        }
    )


def state_summary(state: np.ndarray) -> pd.DataFrame:
    """Pixel count and share per :class:`~geocif.phenology.core.SeasonState`.

    Args:
        state: the plotted state layer as float codes with NaN nodata
            (:func:`state_to_float` output).

    Returns:
        DataFrame ``state_code, state, n_pixels, share`` with one row per state
        plus a ``nodata`` row; ``share`` is of ALL pixels, so the column sums
        to 1.
    """
    arr = np.asarray(state, dtype=np.float64)
    n_total = int(arr.size)
    rows = []
    for code in sorted(STATE_LABELS):
        n = int(np.count_nonzero(arr == code))
        rows.append(
            {
                "state_code": code,
                "state": STATE_LABELS[code],
                "n_pixels": n,
                "share": (n / n_total) if n_total else float("nan"),
            }
        )
    n_nodata = int(np.count_nonzero(~np.isfinite(arr)))
    rows.append(
        {
            "state_code": -1,
            "state": "nodata",
            "n_pixels": n_nodata,
            "share": (n_nodata / n_total) if n_total else float("nan"),
        }
    )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# the one drawing skeleton
# ---------------------------------------------------------------------------
def raster_map(
    grid_da: xr.DataArray,
    *,
    out_path: Any,
    region: Sequence[float],
    title: str,
    cbar_label: str,
    cmap_spec: CmapSpec,
    admin_gdf: Any = None,
    categorical: Optional[Sequence[str]] = None,
    annot_file: Optional[Any] = None,
    dpi: int = DEFAULT_DPI,
) -> Path:
    """Render one pixel layer. The only pygmt call site in this module.

    Draw order matters: NODATA land goes down FIRST so the transparent NaN
    pixels of the grid read as excluded ground rather than as ocean, and the
    national borders go on LAST so the country outline stays legible over a
    dense raster.

    Args:
        grid_da: the layer, dims ``("lat", "lon")`` on pixel centres.
        out_path: PNG destination.
        region: ``[west, east, south, north]`` in degrees.
        title: short factual title, already Title-Cased by the caller.
        cbar_label: colourbar label including units.
        cmap_spec: palette request.
        admin_gdf: admin outlines (EPSG:4326) drawn over the raster, or None.
        categorical: class labels; makes the bar a set of labelled boxes.
        annot_file: GMT custom-annotation file for a date-labelled bar.
        dpi: raster resolution of the PNG.

    Returns:
        The written PNG path.
    """
    import pygmt

    safe_title = gmt_safe(title)
    fig = pygmt.Figure()
    pygmt.config(FONT_TITLE=title_font(safe_title, _projection_width_cm()))
    fig.basemap(
        region=list(region),
        projection=PROJECTION,
        frame=["af", f"+t{safe_title}"],
    )
    # land FIRST: NaN pixels above it read as excluded ground, never as water
    fig.coast(land=NODATA, water="white", **COAST_KW)
    pygmt.makecpt(**makecpt_kwargs(cmap_spec, categorical))
    fig.grdimage(grid=grid_da, cmap=True, nan_transparent=True)
    if admin_gdf is not None and len(admin_gdf) > 0:
        fig.plot(data=admin_gdf, pen=POLY_PEN)
    fig.coast(borders=BORDER_PEN, area_thresh=AREA_THRESH)
    fig.colorbar(**colorbar_kwargs(cbar_label, categorical, annot_file))
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out), dpi=int(dpi))
    logger.info(f"phenology map written: {out}")
    return out


def _render_layer(
    values: np.ndarray,
    ctx: MapContext,
    *,
    layer: str,
    layer_label: str,
    cbar_label: str,
    cmap_spec: CmapSpec,
    description: str,
    table: Optional[pd.DataFrame] = None,
    categorical: Optional[Sequence[str]] = None,
    date_reference: Optional[date] = None,
    units: str = "",
) -> tuple[str, str, str]:
    """Write one map plus its companion CSV and return the manifest row.

    The companion CSV is the caller's zonal table when it has one, otherwise a
    per-pixel summary of exactly the array that was plotted.
    """
    dir_plots = Path(ctx.dir_plots)
    dir_csvs = Path(ctx.dir_csvs)
    dir_plots.mkdir(parents=True, exist_ok=True)
    dir_csvs.mkdir(parents=True, exist_ok=True)

    stem = map_stem(layer, ctx)
    png_name, csv_name = f"{stem}.png", f"{stem}.csv"

    if table is not None:
        table.to_csv(dir_csvs / csv_name, index=False)
    elif categorical:
        state_summary(values).to_csv(dir_csvs / csv_name, index=False)
    else:
        pixel_summary(values, units=units).to_csv(dir_csvs / csv_name, index=False)

    grid = grid_from_array(values, ctx.lon, ctx.lat)
    with tempfile.TemporaryDirectory() as tmp:
        annot_file = None
        if date_reference is not None:
            ticks = date_tick_annotations(
                float(cmap_spec.series[0]), float(cmap_spec.series[1]), date_reference
            )
            annot_file = write_annotation_file(Path(tmp) / f"{layer}.txt", ticks)
        raster_map(
            grid,
            out_path=dir_plots / png_name,
            region=region_from_grid(ctx.lon, ctx.lat),
            title=map_title(layer_label, ctx),
            cbar_label=cbar_label,
            cmap_spec=cmap_spec,
            admin_gdf=ctx.admin_gdf,
            categorical=categorical,
            annot_file=annot_file,
            dpi=ctx.dpi,
        )
    return png_name, csv_name, description


def _what(ctx: MapContext) -> str:
    """``Kenya Maize season 1`` -- the subject clause of every description."""
    return (
        f"{_display_name(ctx.country)} {_display_name(ctx.crop)} "
        f"season {int(ctx.season)}"
    )


# ---------------------------------------------------------------------------
# monitor maps (DESIGN section 8, items 1-6)
# ---------------------------------------------------------------------------
def season_state_map(
    state: np.ndarray, ctx: MapContext, *, table: Optional[pd.DataFrame] = None
) -> tuple[str, str, str]:
    """Categorical map of the six monitor states.

    Args:
        state: ``(rows, cols)`` state codes, int8 with -1 nodata or float with
            NaN nodata.
        ctx: shared map context.
        table: zonal status-area table; a per-state pixel count is written when
            omitted.

    Returns:
        ``(png_file, csv_file, description)``.
    """
    spec, labels = state_cmap_spec()
    return _render_layer(
        state_to_float(state),
        ctx,
        layer="season_state",
        layer_label="Season State",
        cbar_label="Season state",
        cmap_spec=spec,
        categorical=labels,
        table=table,
        description=f"Onset state per pixel, {_what(ctx)}, {through_text(ctx)}",
    )


def onset_anomaly_map(
    anomaly_days: np.ndarray,
    ctx: MapContext,
    *,
    table: Optional[pd.DataFrame] = None,
) -> tuple[str, str, str]:
    """Confirmed onset minus the climatological median, in days.

    Diverging on zero with a symmetric range so early and late are equally
    visible; GMT ``polar`` runs blue -> white -> red, so POSITIVE (late) is red.

    Args:
        anomaly_days: ``(rows, cols)`` days; positive = later than the median.
        ctx: shared map context.
        table: zonal table; per-pixel summary when omitted.

    Returns:
        ``(png_file, csv_file, description)``.
    """
    low, high = symmetric_limits(anomaly_days)
    return _render_layer(
        anomaly_days,
        ctx,
        layer="onset_anomaly_days",
        layer_label="Onset Anomaly",
        cbar_label="Onset anomaly (days, positive = late)",
        cmap_spec=CmapSpec(cmap="polar", series=(low, high)),
        units="days",
        table=table,
        description=(
            f"Onset anomaly vs the climatological median, {_what(ctx)}, "
            f"{through_text(ctx)}"
        ),
    )


def days_past_median_map(
    days: np.ndarray, ctx: MapContext, *, table: Optional[pd.DataFrame] = None
) -> tuple[str, str, str]:
    """How far past the median onset date a still-unstarted pixel is.

    Only NOT_STARTED pixels carry a value (the caller blanks the rest), so the
    ramp is sequential and reversed ``hot``: the longer the wait, the darker.

    Args:
        days: ``(rows, cols)`` days since the climatological median onset.
        ctx: shared map context.
        table: zonal table; per-pixel summary when omitted.

    Returns:
        ``(png_file, csv_file, description)``.
    """
    low, high = sequential_limits(
        days, lower_pct=0.0, upper_pct=98.0, minimum_span=5.0, step=5.0
    )
    return _render_layer(
        days,
        ctx,
        layer="days_past_median",
        layer_label="Days Past Median Onset",
        cbar_label="Days past median onset",
        cmap_spec=CmapSpec(cmap="hot", series=(low, high), reverse=True),
        units="days",
        table=table,
        description=(
            f"Days past median onset where onset has not started, {_what(ctx)}, "
            f"{through_text(ctx)}"
        ),
    )


def p_onset_map(
    probability: np.ndarray,
    ctx: MapContext,
    *,
    horizon_days: int = 28,
    table: Optional[pd.DataFrame] = None,
) -> tuple[str, str, str]:
    """Conditional probability that onset arrives in the next ``horizon_days``.

    Fixed 0..1 range: a probability map that rescales to its own data cannot be
    compared with the previous week's.

    Args:
        probability: ``(rows, cols)`` probability 0..1.
        ctx: shared map context.
        horizon_days: the conditioning horizon, used in the layer name.
        table: zonal table; per-pixel summary when omitted.

    Returns:
        ``(png_file, csv_file, description)``.
    """
    return _render_layer(
        probability,
        ctx,
        layer=f"p_onset_{int(horizon_days)}d",
        layer_label=f"Onset Probability Next {int(horizon_days)} Days",
        cbar_label=f"P(onset within {int(horizon_days)} days)",
        cmap_spec=CmapSpec(cmap="viridis", series=(0.0, 1.0)),
        units="probability",
        table=table,
        description=(
            f"Climatological probability of onset within {int(horizon_days)} "
            f"days, {_what(ctx)}, {through_text(ctx)}"
        ),
    )


def rain_percentile_map(
    percentile: np.ndarray,
    ctx: MapContext,
    *,
    window_days: int = 30,
    table: Optional[pd.DataFrame] = None,
) -> tuple[str, str, str]:
    """Trailing rainfall total as a percentile of the same window in the record.

    Diverging on the median: reversed ``polar`` puts DRY (low percentile) in
    red and wet in blue, the same sense a rainfall anomaly map has elsewhere.

    Args:
        percentile: ``(rows, cols)`` percentile 0..100.
        ctx: shared map context.
        window_days: length of the trailing accumulation window.
        table: zonal table; per-pixel summary when omitted.

    Returns:
        ``(png_file, csv_file, description)``.
    """
    return _render_layer(
        percentile,
        ctx,
        layer=f"rain_{int(window_days)}d_percentile",
        layer_label=f"Rainfall Percentile Last {int(window_days)} Days",
        cbar_label=f"{int(window_days)}-day rainfall percentile",
        cmap_spec=CmapSpec(cmap="polar", series=(0.0, 100.0), reverse=True),
        units="percentile",
        table=table,
        description=(
            f"{int(window_days)}-day rainfall total as a percentile of the "
            f"climatological record, {_what(ctx)}, {through_text(ctx)}"
        ),
    )


def fcst_trigger_map(
    days_to_trigger: Optional[np.ndarray],
    ctx: MapContext,
    *,
    table: Optional[pd.DataFrame] = None,
) -> Optional[tuple[str, str, str]]:
    """Days until the CHIRPS-GEFS forecast meets the onset trigger.

    Rendered only when a forecast exists: returns ``None`` for a missing or
    all-NaN layer rather than publishing an empty map, because a blank forecast
    map and a forecast of no rain look identical on the wall.

    Args:
        days_to_trigger: ``(rows, cols)`` days from the as-of date, or None.
        ctx: shared map context.
        table: zonal table; per-pixel summary when omitted.

    Returns:
        ``(png_file, csv_file, description)``, or ``None`` when nothing to draw.
    """
    if days_to_trigger is None:
        logger.info("fcst_trigger map skipped: no forecast cube for this issue")
        return None
    arr = np.asarray(days_to_trigger, dtype=np.float32)
    if not np.any(np.isfinite(arr)):
        logger.info("fcst_trigger map skipped: no pixel triggers inside the forecast")
        return None
    low, high = sequential_limits(
        arr, lower_pct=0.0, upper_pct=100.0, minimum_span=2.0, step=1.0
    )
    return _render_layer(
        arr,
        ctx,
        layer="fcst_trigger_days",
        layer_label="Forecast Onset Trigger",
        cbar_label="Days to forecast trigger",
        cmap_spec=CmapSpec(cmap="viridis", series=(low, high), reverse=True),
        units="days",
        table=table,
        description=(
            f"Days until the forecast meets the onset trigger, {_what(ctx)}, "
            f"{through_text(ctx)}"
        ),
    )


def monitor_maps(
    ctx: MapContext,
    *,
    state: np.ndarray,
    onset_anomaly_days: Optional[np.ndarray] = None,
    days_past_median: Optional[np.ndarray] = None,
    p_onset: Optional[np.ndarray] = None,
    rain_percentile: Optional[np.ndarray] = None,
    fcst_trigger_days: Optional[np.ndarray] = None,
    horizon_days: int = 28,
    rain_window_days: int = 30,
    tables: Optional[dict] = None,
) -> list[tuple[str, str, str]]:
    """Render the current-season map set and write the lookup manifest.

    Layers other than ``state`` are optional; a missing one is skipped with a
    log line rather than drawn empty.

    Args:
        ctx: shared map context (``asof`` must be set).
        state: six-state monitor layer.
        onset_anomaly_days: days, positive = late.
        days_past_median: days, NOT_STARTED pixels only.
        p_onset: probability 0..1 over ``horizon_days``.
        rain_percentile: 0..100 over ``rain_window_days``.
        fcst_trigger_days: days to the forecast trigger, or None.
        horizon_days: conditioning horizon of ``p_onset``.
        rain_window_days: accumulation window of ``rain_percentile``.
        tables: optional ``{layer_key: DataFrame}`` companion tables, keyed by
            ``state``, ``onset_anomaly_days``, ``days_past_median``,
            ``p_onset``, ``rain_percentile``, ``fcst_trigger_days``.

    Returns:
        The manifest rows, in render order.
    """
    tables = tables or {}
    rows: list[tuple[str, str, str]] = [
        season_state_map(state, ctx, table=tables.get("state"))
    ]
    if onset_anomaly_days is not None:
        rows.append(
            onset_anomaly_map(
                onset_anomaly_days, ctx, table=tables.get("onset_anomaly_days")
            )
        )
    if days_past_median is not None:
        rows.append(
            days_past_median_map(
                days_past_median, ctx, table=tables.get("days_past_median")
            )
        )
    if p_onset is not None:
        rows.append(
            p_onset_map(
                p_onset, ctx, horizon_days=horizon_days, table=tables.get("p_onset")
            )
        )
    if rain_percentile is not None:
        rows.append(
            rain_percentile_map(
                rain_percentile,
                ctx,
                window_days=rain_window_days,
                table=tables.get("rain_percentile"),
            )
        )
    forecast_row = fcst_trigger_map(
        fcst_trigger_days, ctx, table=tables.get("fcst_trigger_days")
    )
    if forecast_row is not None:
        rows.append(forecast_row)
    write_manifest(rows, ctx)
    logger.info(f"season monitor: {len(rows)} maps for {_what(ctx)}")
    return rows


# ---------------------------------------------------------------------------
# climatology maps (DESIGN section 8, item 7)
# ---------------------------------------------------------------------------
def climatology_maps(
    ctx: MapContext,
    *,
    planting_reference: date,
    onset_median: Optional[np.ndarray] = None,
    onset_p75_minus_p25: Optional[np.ndarray] = None,
    eos_median: Optional[np.ndarray] = None,
    lgs_median: Optional[np.ndarray] = None,
    false_start_rate: Optional[np.ndarray] = None,
    onset_n_valid: Optional[np.ndarray] = None,
    tables: Optional[dict] = None,
) -> list[tuple[str, str, str]]:
    """Render the six climatology maps and write the lookup manifest.

    ``onset_median`` is the only one whose colourbar is labelled with calendar
    DATES: the underlying values are days since the calendar planting start, and
    ``planting_reference`` is the date that value 0 means. A median onset of
    "day 23" is unreadable on a wall; "7 Nov" is not.

    ``false_start_rate`` is invalidated onset EPISODES per year -- the
    ``core.onset_state`` sense, not the all-candidates count that
    ``core.season_phenology`` returns under the same key.

    Args:
        ctx: shared map context (``years`` must be set).
        planting_reference: the calendar date that day 0 of the season means.
        onset_median: median onset, days since planting start.
        onset_p75_minus_p25: onset interquartile spread, days.
        eos_median: median cessation, days since planting start.
        lgs_median: median length of growing season, days.
        false_start_rate: invalidated episodes per year.
        onset_n_valid: number of years with a valid onset (count).
        tables: optional ``{layer: DataFrame}`` companion tables keyed by layer
            name.

    Returns:
        The manifest rows, in render order.
    """
    tables = tables or {}
    rows: list[tuple[str, str, str]] = []
    span = f"{_what(ctx)}, {through_text(ctx)}"

    if onset_median is not None:
        low, high = sequential_limits(
            onset_median, lower_pct=2.0, upper_pct=98.0, minimum_span=15.0, step=5.0
        )
        rows.append(
            _render_layer(
                onset_median,
                ctx,
                layer="onset_median",
                layer_label="Median Onset Date",
                cbar_label="Median onset date",
                cmap_spec=CmapSpec(cmap="viridis", series=(low, high)),
                units="days since planting start",
                date_reference=planting_reference,
                table=tables.get("onset_median"),
                description=f"Median onset date, {span}",
            )
        )
    if onset_p75_minus_p25 is not None:
        low, high = sequential_limits(
            onset_p75_minus_p25,
            lower_pct=0.0,
            upper_pct=98.0,
            minimum_span=5.0,
            step=5.0,
        )
        rows.append(
            _render_layer(
                onset_p75_minus_p25,
                ctx,
                layer="onset_p75_minus_p25",
                layer_label="Onset Spread",
                cbar_label="Onset p75 minus p25 (days)",
                cmap_spec=CmapSpec(cmap="hot", series=(low, high), reverse=True),
                units="days",
                table=tables.get("onset_p75_minus_p25"),
                description=f"Interquartile spread of onset, {span}",
            )
        )
    if eos_median is not None:
        low, high = sequential_limits(
            eos_median, lower_pct=2.0, upper_pct=98.0, minimum_span=15.0, step=5.0
        )
        rows.append(
            _render_layer(
                eos_median,
                ctx,
                layer="eos_median",
                layer_label="Median Cessation",
                cbar_label="Median cessation (days since planting start)",
                cmap_spec=CmapSpec(cmap="viridis", series=(low, high)),
                units="days since planting start",
                table=tables.get("eos_median"),
                description=f"Median cessation, {span}",
            )
        )
    if lgs_median is not None:
        low, high = sequential_limits(
            lgs_median, lower_pct=2.0, upper_pct=98.0, minimum_span=15.0, step=5.0
        )
        rows.append(
            _render_layer(
                lgs_median,
                ctx,
                layer="lgs_median",
                layer_label="Median Season Length",
                cbar_label="Median length of growing season (days)",
                cmap_spec=CmapSpec(cmap="viridis", series=(low, high)),
                units="days",
                table=tables.get("lgs_median"),
                description=f"Median length of growing season, {span}",
            )
        )
    if false_start_rate is not None:
        low, high = sequential_limits(
            false_start_rate, lower_pct=0.0, upper_pct=98.0, minimum_span=0.5
        )
        rows.append(
            _render_layer(
                false_start_rate,
                ctx,
                layer=FALSE_START_RATE_LAYER,
                layer_label="False Start Rate",
                # climatology.summarize_years divides the COUNT OF YEARS with
                # at least one invalidated episode by the usable years, so this
                # is a share in [0, 1], not a rate. A pixel that false-starts
                # three times every year reads 1.0.
                cbar_label="Share of years with a false start",
                cmap_spec=CmapSpec(cmap="hot", series=(low, high), reverse=True),
                units="share of years with at least one invalidated candidate, 0..1",
                table=tables.get(FALSE_START_RATE_LAYER),
                description=f"Share of years with at least one false start, {span}",
            )
        )
    if onset_n_valid is not None:
        low, high = sequential_limits(
            onset_n_valid, lower_pct=0.0, upper_pct=100.0, minimum_span=5.0, step=5.0
        )
        rows.append(
            _render_layer(
                onset_n_valid,
                ctx,
                layer="onset_n_valid",
                layer_label="Years With Onset",
                cbar_label="Years with a valid onset",
                cmap_spec=CmapSpec(cmap="viridis", series=(low, high)),
                units="years",
                table=tables.get("onset_n_valid"),
                description=f"Years with a valid onset, {span}",
            )
        )

    write_manifest(rows, ctx)
    logger.info(f"season climatology: {len(rows)} maps for {_what(ctx)}")
    return rows


def write_manifest(rows: Sequence[tuple[str, str, str]], ctx: MapContext) -> None:
    """Write ``lookup_plots_csvs.csv`` into both directories of ``ctx``.

    Args:
        rows: ``(png_file, csv_file, description)`` rows.
        ctx: the context whose ``dir_plots`` / ``dir_csvs`` were written to.
    """
    if not rows:
        logger.warning(f"no phenology maps to record for {_what(ctx)}")
        return
    _write_lookup(list(rows), Path(ctx.dir_plots), Path(ctx.dir_csvs))
