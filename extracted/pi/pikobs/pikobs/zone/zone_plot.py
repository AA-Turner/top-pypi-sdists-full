#!/usr/bin/python3
"""Figures of pikobs.zone.

A zonal cross-section: latitude on the x axis, the vertical coordinate of
the family on the y axis, one cell per latitude band and level.

With a control there are four panels, and they are read in this order:
the change of sigma, the change of the mean, the significance of the
sigma change, and the number of matched observations behind each cell.
Without one, three panels show the statistics themselves.

Everything follows the convention of the rest of Pikobs: the difference
is **experience minus control**, so a negative value is an improvement
and is drawn in **red**; blue means the control was better. The earlier
version of this module used the opposite sign, and a positive value in
warm colours, which is why two figures of the same experiment could look
contradictory depending on which module drew them.
"""

import os
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap

import pikobs
from pikobs.figures import save_figure
from pikobs.obsdb import open_result
from pikobs.stats import (MIN_CONFIDENCE, is_significant, moments_from_sums,
                          paired_ttest_confidence, sigma_confidence)

LAND_OCEAN_CHOICES = ('all', 'land', 'ocean')

# A cell with one or two observations has no sigma worth drawing: sigma
# of a single value is zero, and the mesh paints that flat band exactly
# like a cell built on two hundred observations. Below this the cell is
# left empty in the statistics panels; the count panel still shows it.
MIN_OBS_PER_CELL = 5

# Pressure reads in hPa, the way every vertical section does, and as a
# list of rows while the levels are few enough to be named.
PA_PER_HPA = 100.0

# Changes smaller than this, in the units of the variable, are drawn
# white: a difference of a few hundredths is not something to look at,
# and a scale split exactly at zero paints it as if it were.
WHITE_BAND = 0.1

# Rows grow with the number of levels, as in vdedr and mapobs, so every
# channel keeps its label: a fixed panel height would squash three
# hundred IASI channels into lines too thin to name.
INCH_PER_ROW = 0.14
MIN_PANEL_HEIGHT = 5.5
MAX_PANEL_HEIGHT = 60.0
LABEL_FONT_MAX = 9.0
LABEL_FONT_MIN = 3.5
MAX_LABELLED_ROWS = 800

# Past this many rows the panels go side by side instead of in a grid:
# they share the same levels, so stacking them only multiplies the
# height, and a figure five times taller than wide is unreadable in a
# browser, which fits it to the screen.
SIDE_BY_SIDE_ROWS = 40
PANEL_WIDTH_SIDE = 6.0
# a figure of levels (not channels) with this many rows or fewer is drawn
# larger: wider and taller panels, every text a quarter larger
BIG_MAX_ROWS = 80
BIG_SCALE = 1.4
BIG_PANEL_HEIGHT = 9.0

# The steps of the difference scale, as in scatter: the scale grows to
# the first step above the data, so the colours keep their meaning.
_STEPS = (0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 7.5, 10.0)
MAX_DISCRETE_LEVELS = 60

from pikobs.configobs.style import (CTL_BETTER, CTL_COLOUR, DPI, EXP_BETTER,
                                    EXP_COLOUR, GREY_TEXT)

# Sums of each function, in the single-run and in the matched table.
_SINGLE_SUMS = {'omp': ('s_omp', 's2_omp'), 'oma': ('s_oma', 's2_oma'),
                'obs_error': ('s_err', 's2_err')}
# each quantity has its own count: a row without O-A still counts for O-P
_SINGLE_N = {'omp': 'n_omp', 'oma': 'n_oma', 'obs_error': 'n_err'}
_PAIR_N = {'omp': 'n', 'oma': 'n_oma'}
_PAIR_SUMS = {'omp': ('c_omp', 'c2_omp', 'e_omp', 'e2_omp', 'ce_omp'),
              'oma': ('c_oma', 'c2_oma', 'e_oma', 'e2_oma', 'ce_oma')}


def group_members(db_file: str, label: str) -> List[str]:
    """The stations a group label stood for, sorted; empty if unknown."""
    try:
        with open_result(db_file) as conn:
            return [r[0] for r in conn.execute(
                "SELECT member FROM members WHERE label = ? ORDER BY member;",
                (label,))]
    except Exception:
        return []


def members_text(db_file: str, label: str, limit: int = 8) -> str:
    """'C% -> COSMIC2-E1, COSMIC2-E2, ... (+N more)' for a title."""
    found = group_members(db_file, label)
    if not found:
        return str(label)
    shown = ", ".join(found[:limit])
    more = f" (+{len(found) - limit} more)" if len(found) > limit else ""
    return f"{label} -> {shown}{more}"


def level_selector_label(families) -> str:
    """The caption of the level selector of a viewer.

    Channel on radiance families, Vcoord on families on pressure or height,
    where "channel" means nothing, and both when a run mixes them.
    """
    kinds = set()
    for fam in families:
        try:
            vcotyp = str(pikobs.family(fam)[5]).strip().upper()
        except Exception:
            vcotyp = ""
        kinds.add('channel' if vcotyp.startswith('CANAL') else 'vcoord')
    if kinds == {'channel'}:
        return "Channel"
    if kinds == {'vcoord'}:
        return "Vcoord"
    return "Channel / vcoord"


def _safe(text: Any) -> str:
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


def figure_name(task: Dict[str, Any]) -> str:
    # the surface and the special value after the region, only when
    # they split something: the naming convention of every module
    extra = "".join(f"_{_safe(x)}" for x in (task.get('land_ocean', 'all'),
                                             _special_text(task))
                    if x not in (None, '', 'all'))
    return (f"zone_{'_vs_'.join(_safe(n) for n in task['names'])}_"
            f"{_safe(task['family'])}_{task['function']}_"
            f"varno{_safe(task['varno'])}_{_safe(task['stn_tag'])}_"
            f"{_safe(task['region'])}{extra}_{_safe(task['flag'])}_"
            f"ch{_safe(task['channel_mode'])}.png")


def _mask_thin_cells(data: Dict[str, np.ndarray],
                     min_obs: int) -> Tuple[Dict[str, np.ndarray], int]:
    """Blank the statistics of cells built on too few observations."""
    n = data['n']
    thin = n < max(int(min_obs), 1)
    if not np.any(thin):
        return data, 0
    out = dict(data)
    for key, values in data.items():
        if key in ('lat', 'lev', 'n'):
            continue
        masked = np.array(values, dtype=float)
        masked[thin] = np.nan
        out[key] = masked
    return out, int(np.sum(thin))


def _level_label(value: float, levels, kind: str) -> str:
    """The name of a level row.

    A family that rounds its pressure -- ``ua`` to 20000 Pa -- puts
    everything above the first bin into the bin 0. That is not "0 hPa",
    which does not exist; it is "above half a bin", so it is said so.
    """
    if kind == 'pressure' and float(value) == 0.0 and len(levels) > 1:
        bins = np.diff(np.sort(np.asarray(levels, float)))
        half = float(np.min(bins[bins > 0])) / 2.0 if np.any(bins > 0) else 0
        return f"< {half:g}" if half else "top"
    return f"{value:g}"


def _axis_kind(vcotyp: str) -> Tuple[str, bool]:
    """(label kind, invert) from the VCOTYP of the family."""
    lab = str(vcotyp).strip().upper()
    if lab.startswith('CANAL'):
        return 'channel', False
    if lab.startswith('PRESSION'):
        return 'pressure', True
    if lab.startswith('HAUTEUR'):
        return 'height', False
    if lab.startswith('LATITUDE'):
        return 'latitude', False
    return 'level', False


# ─────────────────────────────────────────────────────────────────────────────
# Reading
# ─────────────────────────────────────────────────────────────────────────────

def _where(task: Dict[str, Any]) -> Tuple[str, list]:
    return ("region = ? AND flag = ? AND channel_mode = ? AND land_ocean = ? "
            "AND id_stn = ? AND special = ? AND varno = ?",
            [task['region'], task['flag'], task['channel_mode'],
             task['land_ocean'], task['id_stn'],
             str(task.get('special', 'all')), task['varno']])


def _member_word(family: str) -> str:
    """'type' on a composite family, whose groups are instrument types."""
    try:
        from pikobs.configobs.special_family import has_codtyp_groups
        return "type" if has_codtyp_groups(family) else "station"
    except Exception:
        return "station"


def _special_text(task: Dict[str, Any]) -> str:
    from pikobs.configobs.special_family import special_label
    label = special_label(task['family'], task.get('special', 'all'))
    return '' if label == 'all' else label


def _read_single(task) -> Optional[Dict[str, np.ndarray]]:
    s_col, s2_col = _SINGLE_SUMS[task['function']]
    where, args = _where(task)
    with open_result(task['db_file']) as conn:
        n_col = _SINGLE_N[task['function']]
        rows = conn.execute(f"""
            SELECT lat, vcoord, SUM({n_col}), SUM({s_col}), SUM({s2_col})
            FROM zone WHERE {where}
            GROUP BY lat, vcoord HAVING SUM({n_col}) > 0;""",
                            args).fetchall()
    if not rows:
        return None
    arr = np.array([[float(r[0]), _level(r[1]), float(r[2] or 0),
                     float(r[3] or np.nan), float(r[4] or np.nan)]
                    for r in rows])
    mean, var = moments_from_sums(arr[:, 2], arr[:, 3], arr[:, 4])
    return {'lat': arr[:, 0], 'lev': arr[:, 1], 'n': arr[:, 2],
            'mean': mean, 'sigma': np.sqrt(var)}


def _read_matched(task) -> Optional[Dict[str, np.ndarray]]:
    if task['function'] not in _PAIR_SUMS:
        return None
    c_s, c_s2, e_s, e_s2, ce = _PAIR_SUMS[task['function']]
    where, args = _where(task)
    with open_result(task['db_file']) as conn:
        n_col = _PAIR_N[task['function']]
        rows = conn.execute(f"""
            SELECT lat, vcoord, SUM({n_col}), SUM({c_s}), SUM({c_s2}),
                   SUM({e_s}), SUM({e_s2}), SUM({ce})
            FROM zone_pairs WHERE {where}
            GROUP BY lat, vcoord HAVING SUM({n_col}) > 0;""",
                            args).fetchall()
    if not rows:
        return None
    arr = np.array([[float(r[0]), _level(r[1])] +
                    [float(v) if v is not None else np.nan for v in r[2:]]
                    for r in rows])
    n = arr[:, 2]
    m_ctl, v_ctl = moments_from_sums(n, arr[:, 3], arr[:, 4])
    m_exp, v_exp = moments_from_sums(n, arr[:, 5], arr[:, 6])
    with np.errstate(divide='ignore', invalid='ignore'):
        cov = np.where(n > 0, arr[:, 7] / n - m_ctl * m_exp, np.nan)
    return {'lat': arr[:, 0], 'lev': arr[:, 1], 'n': n,
            'mean_ctl': m_ctl, 'mean_exp': m_exp,
            'sigma_ctl': np.sqrt(v_ctl), 'sigma_exp': np.sqrt(v_exp),
            'var_ctl': v_ctl, 'var_exp': v_exp, 'cov': cov}


def _level(value) -> float:
    """The level of a row; 'join' rows share a single band."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Grid
# ─────────────────────────────────────────────────────────────────────────────

def _grid(lat, lev, values, lats=None, levels=None):
    """Put the cells on a grid of latitude bands and levels.

    With ``lats`` and ``levels`` given, that grid is used as it is: the
    same for every figure of a family, so a cell has the same size in all
    of them. Values outside it are dropped, which only happens with data
    outside the region.
    """
    lats = np.unique(lat) if lats is None else np.asarray(lats, float)
    levels = np.unique(lev) if levels is None else np.asarray(levels, float)
    grid = np.full((len(levels), len(lats)), np.nan)
    lat_idx = {round(float(v), 6): i for i, v in enumerate(lats)}
    lev_idx = {round(float(v), 6): i for i, v in enumerate(levels)}
    for la, le, val in zip(lat, lev, values):
        i = lev_idx.get(round(float(le), 6))
        j = lat_idx.get(round(float(la), 6))
        if i is not None and j is not None:
            grid[i, j] = val
    return lats, levels, grid


def _band_centres(lat_range, box_y: float) -> np.ndarray:
    """The centres of every latitude band of the region.

    The same formula as the extraction, floor(lat / box) * box + box / 2,
    so each band of the data lands exactly on one of these.
    """
    lo, hi = lat_range
    box = float(box_y)
    first = np.floor(lo / box) * box + box / 2.0
    last = np.floor(min(hi, 90.0 - 1e-9) / box) * box + box / 2.0
    return np.round(np.arange(first, last + box / 2.0, box), 6)


def _edges(values):
    values = np.asarray(values, float)
    if len(values) == 1:
        return np.array([values[0] - 0.5, values[0] + 0.5])
    mids = (values[:-1] + values[1:]) / 2.0
    return np.concatenate(([values[0] - (values[1] - values[0]) / 2], mids,
                           [values[-1] + (values[-1] - values[-2]) / 2]))


def _nice_bounds(vmax: float, target: int = 8) -> np.ndarray:
    """0 .. vmax in round steps: 0.1, 0.2, 0.25, 0.5 times a power of ten.

    A colour bar reads 0, 0.2, 0.4 ... or 0, 100000, 200000 ..., not
    0.1063 or 60106: the eye has to be able to name a colour.
    """
    vmax = max(float(vmax), 1e-9)
    raw = vmax / target
    mag = 10 ** np.floor(np.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    top = np.ceil(vmax / step) * step
    return np.round(np.arange(0.0, top + step / 2, step), 10)


def _sequential(vmax: float, name: str = 'viridis', n: int = 8):
    """A scale from zero to vmax, with one extra colour for the overflow.

    BoundaryNorm counts the extension as a bin, so the colormap needs one
    colour more than there are intervals.
    """
    bounds = _nice_bounds(vmax, n)
    n = len(bounds) - 1
    cmap = ListedColormap(plt.get_cmap(name)(np.linspace(0, 1, n + 1)))
    cmap.set_over(cmap(cmap.N - 1))
    return cmap, BoundaryNorm(bounds, cmap.N, extend='max'), bounds


def _white_for(vmax, white: float = WHITE_BAND):
    """(the white band, the scale of the colour steps) for data of size vmax.

    WHITE_BAND is in the units of the variable, which suits winds and
    temperatures. On a variable whose values are a few hundredths -- the
    departures of ro -- it would swallow everything and leave the panel
    white. When the band is more than half of the data, both follow the
    data: the steps are scaled to its order of magnitude and the band
    becomes a tenth of it.
    """
    white = abs(float(white)) or 0.1
    vmax = abs(float(vmax)) if vmax else 0.0
    if vmax <= 0 or white < vmax / 2:
        return white, 1.0
    scale = 10.0 ** np.floor(np.log10(vmax))
    return 0.1 * scale, scale


# a figure whose largest sigma is more than this many times its typical
# one spans an order of magnitude (ro, with height) and gets 1-2-5 steps
WIDE_RANGE = 5.0


def _nice_down(x: float) -> float:
    """The largest of 1, 2, 5 times a power of ten not above x."""
    x = abs(float(x))
    if x <= 0:
        return 0.1
    e = np.floor(np.log10(x))
    return max(m * 10 ** e for m in (1, 2, 5) if m * 10 ** e <= x * (1 + 1e-9))


def _log_steps(lo: float, hi: float) -> list:
    """1-2-5 steps from lo up to the first one at or above hi."""
    lo, hi = _nice_down(lo), max(float(hi), float(lo))
    out, e = [], int(np.floor(np.log10(lo)))
    while True:
        for m in (1, 2, 5):
            v = round(m * 10.0 ** e, 12)
            if v >= lo * (1 - 1e-9):
                out.append(v)
                if v >= hi * (1 - 1e-9):
                    return out
        e += 1


def _sigma_range(sigma):
    """(typical, largest) sigma of a figure: its median and 98th percentile."""
    s = np.asarray(sigma, float)
    s = s[np.isfinite(s) & (s > 0)]
    if not s.size:
        return None, None
    return float(np.median(s)), float(np.percentile(s, 98))


def _wide(typical, top) -> bool:
    """True when the sigma spans an order of magnitude or so."""
    return bool(typical and top and top / typical > WIDE_RANGE)


def _sequential_log(vmax: float, typical: float, name: str = 'viridis'):
    """0, then 1-2-5 steps from a fifth of the typical value to vmax."""
    bounds = np.array([0.0] + _log_steps(typical / 5.0, vmax))
    n = len(bounds) - 1
    cmap = ListedColormap(plt.get_cmap(name)(np.linspace(0, 1, n + 1)))
    cmap.set_over(cmap(cmap.N - 1))
    return cmap, BoundaryNorm(bounds, cmap.N, extend='max'), bounds


def _band(vmax, white: float = WHITE_BAND, typical_sigma=None) -> float:
    """The white band a scale really uses, for the label of its colour bar."""
    white = abs(float(white)) or 0.1
    if typical_sigma:
        return min(white, _nice_down(0.1 * typical_sigma))
    return _white_for(vmax, white)[0]


def _diverging_white(vmax: float, white: float = WHITE_BAND,
                     red_above: bool = False, typical_sigma=None):
    """A difference scale with a white band around zero.

    Bounds: -L ... -white, +white ... +L, with L the first step above
    the data; everything inside the band is white, so what is coloured
    is a change worth reading. A difference (Exp - Ctl) is red below zero,
    where Exp is better; a departure of one run (red_above) is red above
    zero and blue below, as in scatter. With typical_sigma -- a figure whose
    sigma spans an order of magnitude -- the band is at most a tenth of it
    and the steps go 1-2-5 up to the data.
    """
    if typical_sigma:
        white = _band(vmax, white, typical_sigma)
        # the steps start above the band, never on its edge
        outer = [v for v in _log_steps(white, max(float(vmax), 4 * white))
                 if v > white * (1 + 1e-9)][-6:]
    else:
        white, scale = _white_for(vmax, white)
        steps = ([st * scale for st in _STEPS if st * scale > white]
                 or [white * 2])
        idx = next((i for i, st in enumerate(steps) if st >= vmax),
                   len(steps) - 1)
        # at least four steps on each side, so the colour goes from light
        # next to the white band to dark at the ends even when the changes
        # are small; at most five, or the colours stop being told apart
        outer = steps[:max(idx + 1, 4)][-5:]
    bounds = np.array([-v for v in reversed(outer)] + [-white, white]
                      + list(outer))
    n_side = len(outer)
    dark_to_light_red = plt.get_cmap('RdBu')(np.linspace(0.02, 0.42, n_side))
    light_to_dark_blue = plt.get_cmap('RdBu')(np.linspace(0.58, 0.98, n_side))
    if red_above:
        below = light_to_dark_blue[::-1]          # dark blue far below zero
        above = dark_to_light_red[::-1]           # dark red far above
        under, over = '#053061', '#67001F'
    else:
        below, above = dark_to_light_red, light_to_dark_blue
        under, over = '#67001F', '#053061'
    colours = list(below) + [(1, 1, 1, 1)] + list(above)
    cmap = ListedColormap(colours)
    cmap.set_under(under)
    cmap.set_over(over)
    return cmap, BoundaryNorm(bounds, cmap.N + 0, extend='neither'), bounds


def _diverging(vmax: float, n: int = 8):
    """A red-to-blue scale centred on zero, red for the experience."""
    bounds = np.linspace(-vmax, vmax, n + 1)
    # n intervals plus the two extensions: n + 2 colours
    cmap = ListedColormap(plt.get_cmap('RdBu')(np.linspace(0, 1, n + 2)))
    cmap.set_under('#67001F')
    cmap.set_over('#053061')
    return cmap, BoundaryNorm(bounds, cmap.N, extend='both'), bounds


# ─────────────────────────────────────────────────────────────────────────────
# Figure
# ─────────────────────────────────────────────────────────────────────────────

def _lat_ticks(lo: float, hi: float) -> np.ndarray:
    """Latitude marks a reader names: every 30 degrees on a wide section, so
    a global one reads -90 to 90 and not -80 to 80; every 10 or 5 on a
    narrow one."""
    span = hi - lo
    step = 30 if span >= 120 else 10 if span >= 30 else 5
    first = np.ceil(lo / step - 1e-9) * step
    return np.arange(first, hi + 1e-9, step)


def zone_plot(task: Dict[str, Any]) -> Optional[str]:
    """Draw one cross-section; returns the path of the PNG."""
    data = (_read_matched(task) if task['matched'] else _read_single(task))
    if data is None:
        return None

    family = task['family']
    _, _, _, _, _, vcotyp = pikobs.family(family)
    kind, invert = _axis_kind(vcotyp)
    var_name, units, _ = pikobs.type_varno(str(task['varno']))
    label = {'omp': 'O-P', 'oma': 'O-A',
             'obs_error': 'obs error'}[task['function']]
    if kind == 'pressure':
        # hPa: nobody reads a vertical section in pascals
        data = dict(data)
        data['lev'] = data['lev'] / PA_PER_HPA
    y_label = {'channel': 'Channel', 'pressure': 'Pressure [hPa]',
               'height': 'Height [m]', 'latitude': 'Latitude band',
               'level': 'Level'}[kind]

    n_levels = (len(task['family_levels']) if task.get('family_levels')
                else len(np.unique(data['lev'])))
    # a short list of levels reads better as rows, evenly spaced and
    # each one named, than squeezed onto a continuous axis
    as_rows = kind == 'channel' or n_levels <= MAX_DISCRETE_LEVELS

    min_obs = int(task.get('min_obs', MIN_OBS_PER_CELL))
    data, n_thin = _mask_thin_cells(data, min_obs)

    if task['matched']:
        panels = _matched_panels(data, task, label, units)
    else:
        panels = _single_panels(data, label, units,
                                float(task.get('white_band', WHITE_BAND)),
                                task.get('scales'))

    n = len(panels)
    cols = 2 if n > 2 else n
    rows = int(np.ceil(n / cols))
    n_rows_axis = (len(task['family_levels']) if task.get('family_levels')
                   else len(np.unique(data['lev'])))
    # a figure of levels, not of channels, with few rows has room: wider
    # and taller panels and larger texts. The sizes were set for the 150
    # channels of IASI, and looked lost on the 40 levels of sw or ua
    big = kind != 'channel' and (n_rows_axis <= BIG_MAX_ROWS or not as_rows)
    fs = BIG_SCALE if big else 1.0
    pw = PANEL_WIDTH_SIDE * (1.35 if big else 1.0)
    panel_h = (float(np.clip(1.5 + INCH_PER_ROW * n_rows_axis,
                             MIN_PANEL_HEIGHT, MAX_PANEL_HEIGHT))
               if as_rows else 6.4)
    if big:
        panel_h = max(panel_h, BIG_PANEL_HEIGHT)
    # the label size follows the real height of one row
    row_pts = 0.78 * panel_h / max(n_rows_axis, 1) * 72.0
    label_fs = float(np.clip(row_pts / 1.35, LABEL_FONT_MIN,
                             LABEL_FONT_MAX * fs))
    # always one row: the panels share the same levels, so the eye can run
    # along a row from one panel to the next, and the height is paid once.
    # The header and the colour bars get fixed room in inches, so nothing
    # overlaps whatever the number of levels.
    side_by_side = True
    n_notes = (1 if task['matched'] else 0) + (1 if n_thin else 0)
    # title, subtitle, the runs and the dates, the notes, the panel titles
    header_in = ((1.50 if task['matched'] else 1.27) + 0.22 * n_notes
                 + 0.55) * fs
    footer_in = 1.55 * fs                         # x label + colour bar
    fig_h = panel_h + header_in + footer_in
    fig = plt.figure(figsize=(pw * n + 1.2, fig_h),
                     facecolor='white')
    fig.subplots_adjust(left=0.9 / (pw * n + 1.2),
                        right=0.99, wspace=0.10,
                        top=1.0 - header_in / fig_h,
                        bottom=footer_in / fig_h)
    gs = fig.add_gridspec(1, n)
    axes = [fig.add_subplot(gs[0, 0])]
    for i in range(1, n):
        axes.append(fig.add_subplot(gs[0, i], sharey=axes[0]))

    # the grid of the family, not of this figure: the whole region in
    # bands of BOXSIZEY, and every level the family has in the period
    lats_fixed = (_band_centres(task['lat_range'], task['box_y'])
                  if task.get('lat_range') and task.get('box_y') else None)
    levels_fixed = None
    if task.get('family_levels'):
        levels_fixed = np.asarray(task['family_levels'], float)
        if kind == 'pressure':
            levels_fixed = levels_fixed / PA_PER_HPA
        levels_fixed = np.unique(np.round(levels_fixed, 6))
    lats, levels, _ = _grid(data['lat'], data['lev'], data['n'],
                            lats_fixed, levels_fixed)
    y_pos = np.arange(len(levels)) if as_rows else levels
    y_edges = (np.arange(-0.5, len(levels), 1.0) if as_rows
               else _edges(levels))
    x_edges = _edges(lats)

    for ax, panel in zip(axes, panels):
        _, _, grid = _grid(data['lat'], data['lev'], panel['values'],
                           lats, levels)
        mesh = ax.pcolormesh(x_edges, y_edges, grid, cmap=panel['cmap'],
                             norm=panel['norm'], shading='flat')
        # the colour bar sits under the panel, below its x label, at a
        # fixed distance in inches whatever the height of the panel
        ph = panel_h
        cax = ax.inset_axes([0.04, -0.62 * fs / ph, 0.92, 0.16 * fs / ph])
        cb = fig.colorbar(mesh, cax=cax, orientation='horizontal',
                          ticks=panel.get('ticks'),
                          extend=panel.get('extend', 'both'))
        cb.set_label(panel['cbar'], fontsize=9 * fs, labelpad=2)
        if panel.get('tick_labels'):
            cb.set_ticklabels(panel['tick_labels'])
        cb.ax.tick_params(labelsize=8 * fs, length=2)
        ticks = panel.get('ticks')
        if ticks is not None and len(ticks) > 7:
            for lab in cb.ax.get_xticklabels():
                lab.set_rotation(45)
                lab.set_ha('right')

        ax.set_xlim(x_edges[0], x_edges[-1])
        ax.set_xticks(_lat_ticks(x_edges[0], x_edges[-1]))
        ax.tick_params(axis='x', labelsize=10 * fs)
        ax.set_title(panel['title'], fontsize=10.5 * fs, fontweight='bold',
                     pad=6)
        ax.set_xlabel('Latitude', fontsize=11 * fs)
        ax.set_ylabel(y_label, fontsize=11 * fs)
        ax.grid(True, alpha=0.3, linestyle=':')
        if as_rows:
            # every row named, up to a limit no figure should reach
            step = max(1, int(np.ceil(len(levels) / MAX_LABELLED_ROWS)))
            ax.set_yticks(y_pos[::step])
            ax.set_yticklabels([_level_label(v, levels, kind)
                                for v in levels[::step]], fontsize=label_fs)
            ax.tick_params(axis='y', length=2, pad=2)
            ax.set_ylim(-0.5, len(levels) - 0.5)
            # pressure with the ground at the bottom; channels with the
            # first one at the top, as they are listed everywhere else
            if invert or kind == 'channel':
                ax.invert_yaxis()
        else:
            ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=8))
            if invert:
                ax.set_ylim(y_edges.max(), y_edges.min())
        # the levels are named once, on the first panel; the others share
        # the axis and are read along the same rows
        if ax is not axes[0]:
            ax.tick_params(axis='y', labelleft=False)
            ax.set_ylabel('')

    # the header, as in scatter: the variable, a grey line with what the
    # figure holds, the runs in their colours (Exp red, Ctl blue), the
    # dates, and the notes small
    names = task['names']

    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    surface = task.get('land_ocean', 'all')
    region_text = (task['region'] if surface in (None, '', 'all')
                   else f"{task['region']} ({surface})")
    word = 'channels' if kind == 'channel' else 'levels'
    parts = [family, region_text, f"flag {task['flag']}",
             f"{_member_word(family)} "
             f"{members_text(task['db_file'], task['id_stn'])}",
             f"{word} joined" if str(task['channel_mode']) == 'join'
             else f"all {word}"]
    if _special_text(task):
        parts.append(f"method {_special_text(task)}")

    def _y(inch: float) -> float:
        return 1.0 - inch * fs / fig_h

    x0 = 0.9 / (pw * n + 1.2)
    fig.text(0.5, _y(0.12), f"{var_name} {units}  ·  {label}", ha='center',
             va='top', fontsize=14 * fs, fontweight='bold', color='#1F2933')
    fig.text(0.5, _y(0.45), "  ·  ".join(parts), ha='center', va='top',
             fontsize=10.5 * fs, color=GREY_TEXT)
    # a light rule, as in scatter: what the figure is above, the runs
    # and the dates below
    from matplotlib.lines import Line2D
    fig.add_artist(Line2D([x0, 0.99], [_y(0.71)] * 2, color='#c8c8c8',
                          linewidth=0.9, transform=fig.transFigure))
    runs = ([("Exp", names[1], EXP_COLOUR), ("Ctl", names[0], CTL_COLOUR)]
            if task['matched'] else [("Exp", names[0], EXP_COLOUR)])
    y_in = 0.80
    for word_run, name, colour in runs:
        fig.text(x0, _y(y_in), f"{word_run}  {name}", ha='left', va='top',
                 fontsize=11 * fs, fontweight='bold', color=colour)
        y_in += 0.23
    fig.text(x0, _y(y_in), f"{_when(task['datestart'])}  to  "
             f"{_when(task['dateend'])}", ha='left', va='top', fontsize=9.5 * fs,
             color=GREY_TEXT)
    y_in += 0.25
    notes = []
    if task['matched']:
        notes.append(f"Exp - Ctl: negative is better and red; a cell counts "
                     f"when its test passes {MIN_CONFIDENCE:.0f} %")
    if n_thin:
        notes.append(f"{n_thin} cells left empty: fewer than {min_obs} "
                     f"observations, where a sigma means nothing")
    for note in notes:
        fig.text(x0, _y(y_in), note, ha='left', va='top', fontsize=8.5 * fs,
                 color=GREY_TEXT)
        y_in += 0.22
    # room already reserved above: no tight_layout, which would move the
    # panels under the header again

    out_dir = os.path.join(task['pathwork'], family)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, figure_name(task))
    save_figure(fig, out_file, svg=task.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out_file


def _single_panels(data, label, units, white: float = WHITE_BAND,
                   scales: Optional[Dict[str, float]] = None
                   ) -> List[Dict[str, Any]]:
    """One run: the sigma, the mean, and how many observations."""
    panels = []
    shared = scales or {}
    sigma = data['sigma']
    vmax = shared.get('sigma') or (_p98(sigma) or 1.0)
    typ, top = (shared.get('sigma_typ'), shared.get('sigma_top'))
    if typ is None:
        typ, top = _sigma_range(sigma)
    wide = typ if _wide(typ, top) else None
    cmap, norm, bounds = (_sequential_log(vmax, wide) if wide
                          else _sequential(vmax))
    panels.append(dict(values=sigma, cmap=cmap, norm=norm,
                       ticks=bounds, extend='max',
                       title=f"Sigma of {label}",
                       cbar=f"sigma {label} {units}"))

    # a departure is read against zero: the scale is symmetric, and a
    # mean within the white band is no bias worth reading, so it is white
    # instead of the faint colour a scale split at zero would give it
    mean = data['mean']
    m = shared.get('mean') or (_p98(mean) or 1.0)
    cmap2, norm2, b2 = _diverging_white(m, white, red_above=True,
                                        typical_sigma=wide)
    panels.append(dict(values=mean, cmap=cmap2, norm=norm2, ticks=b2,
                       extend='both',
                       title=f"Mean of {label}",
                       cbar=f"mean {label} {units}\n"
                            f"red above zero, white within "
                            f"+/-{_band(m, white, wide):g}"))

    n = data['n']
    nmax = shared.get('n') or (float(np.nanmax(n))
                               if np.isfinite(n).any() else 1.0)
    cmap3, norm3, bounds3 = _sequential(nmax, 'cividis')
    panels.append(dict(values=n, cmap=cmap3, norm=norm3,
                       ticks=bounds3, extend='max',
                       title="Observations per cell",
                       cbar="observations"))
    return panels


def _matched_panels(data, task, label, units) -> List[Dict[str, Any]]:
    """Control against experience, on the same observations.

    The two changes are shown as a percentage of the control, which is
    what makes cells of different magnitude comparable, and the test of
    the sigma gets its own panel: a percentage says how much moved, the
    test says whether it moved at all.
    """
    n = data['n']
    s_ctl, s_exp = data['sigma_ctl'], data['sigma_exp']
    m_ctl, m_exp = data['mean_ctl'], data['mean_exp']

    # differences in the units of the variable, as scatter does: a
    # percentage of the control bias explodes wherever that bias is near
    # zero, and 0.01 -> 0.07 m/s would read as +600 %
    d_sigma = s_exp - s_ctl
    d_mean = np.abs(m_exp) - np.abs(m_ctl)
    white = float(task.get('white_band', WHITE_BAND))

    shared = task.get('scales') or {}
    typ, top = (shared.get('sigma_typ'), shared.get('sigma_top'))
    if typ is None:
        typ, top = _sigma_range(s_ctl)
    wide = typ if _wide(typ, top) else None

    def _vmax(values, key):
        return shared.get(key) or (_p98(values) or 1.0)

    cmap, norm, bounds = _diverging_white(_vmax(d_sigma, 'd_sigma'), white,
                                          typical_sigma=wide)
    panels = [dict(values=d_sigma, cmap=cmap, norm=norm, ticks=bounds,
                   extend='both',
                   title=f"Sigma of {label}: Exp - Ctl",
                   cbar=f"σ Exp - σ Ctl {units}\n"
                        f"negative / red = Exp better")]

    cmap2, norm2, bounds2 = _diverging_white(_vmax(d_mean, 'd_mean'), white,
                                             typical_sigma=wide)
    panels.append(dict(values=d_mean, cmap=cmap2, norm=norm2, ticks=bounds2,
                       extend='both',
                       title=f"Bias of {label}: Exp - Ctl",
                       cbar=f"|mean Exp| - |mean Ctl| {units}\n"
                            f"negative / red = Exp bias closer to zero"))

    # the tests, both from pikobs.stats: Pitman-Morgan on the sigma, and
    # a paired t
    # on the bias -- paired because both sides of a cell are the same
    # observations, which is what makes it the sharp form of the test
    f_conf = sigma_confidence(data['var_ctl'], data['var_exp'], n,
                              cov=data['cov'])
    t_conf = paired_ttest_confidence(m_ctl, m_exp, data['var_ctl'],
                                     data['var_exp'], data['cov'], n)
    panels.append(_test_panel(f_conf, d_sigma, task,
                              f"Pitman-Morgan test on the sigma"))
    panels.append(_test_panel(t_conf, d_mean, task,
                              f"Paired t-test on the bias"))

    # not a comparison: with matched observations the count is the same
    # in both runs. It is the sample behind each cell, and it is what the
    # two tests above should be read against
    nmax = shared.get('n') or (float(np.nanmax(n))
                               if np.isfinite(n).any() else 1.0)
    cmap4, norm4, bounds4 = _sequential(nmax, 'cividis')
    panels.append(dict(values=n, cmap=cmap4, norm=norm4,
                       ticks=bounds4, extend='max',
                       title="Sample size: observations compared per cell\n"
                             "(the same in both runs, not a comparison)",
                       cbar="matched observations"))
    return panels


def _test_panel(conf, change, task, name) -> Dict[str, Any]:
    """A significance map: red where the experience wins, blue where the
    control does, grey where the change is not larger than noise."""
    code = np.full(np.shape(conf), np.nan)
    sig = is_significant(conf)
    code[sig] = np.where(np.asarray(change)[sig] < 0, -1.0, 1.0)
    code[~sig & np.isfinite(conf)] = 0.0
    cmap = ListedColormap([EXP_BETTER, '#f2f2f2', CTL_BETTER])
    norm = BoundaryNorm([-1.5, -0.5, 0.5, 1.5], cmap.N)
    n_better = int(np.nansum(code == -1))
    n_worse = int(np.nansum(code == 1))
    return dict(values=code, cmap=cmap, norm=norm, ticks=[-1, 0, 1],
                extend='neither',
                tick_labels=["Exp better", "not significant", "Ctl better"],
                title=f"{name}, above {MIN_CONFIDENCE:.0f} %  "
                      f"({n_better} red, {n_worse} blue)",
                cbar="significance")


def _p98(values) -> Optional[float]:
    values = np.abs(np.asarray(values, float))
    values = values[np.isfinite(values)]
    return float(np.percentile(values, 98)) if values.size else None


def figure_extremes(task: Dict[str, Any]) -> Optional[Dict[str, float]]:
    """What one figure would need of each colour scale.

    The figures of a group then take the largest of these, so a colour
    means the same value in every one of them. The 98th percentile, not
    the maximum: one odd cell should not flatten every other figure.
    """
    data = (_read_matched(task) if task['matched'] else _read_single(task))
    if data is None:
        return None
    data, _ = _mask_thin_cells(data, int(task.get('min_obs',
                                                  MIN_OBS_PER_CELL)))
    n = data['n']
    # the 98th percentile, as for the other scales: the fullest cell alone
    # should not leave every other one in the first colour
    out = {'n': _p98(n)}
    if task['matched']:
        out['d_sigma'] = _p98(data['sigma_exp'] - data['sigma_ctl'])
        out['d_mean'] = _p98(np.abs(data['mean_exp'])
                             - np.abs(data['mean_ctl']))
    else:
        out['sigma'] = _p98(data['sigma'])
        out['mean'] = _p98(data['mean'])
    # whether the figures of a group need 1-2-5 steps: the largest
    # typical and largest sigma of the group decide, for all of them
    out['sigma_typ'], out['sigma_top'] = _sigma_range(
        data['sigma_ctl'] if task['matched'] else data['sigma'])
    return {k: v for k, v in out.items() if v is not None}


def scale_group(task: Dict[str, Any]) -> tuple:
    """The figures that share their colours: one family, varno, function
    and region -- the same between runs and experiences of a region, and
    fitted to it, not to the most extreme region of the run."""
    return (task['family'], str(task['varno']), task['function'],
            bool(task['matched']), task['region'])


def zone_scale_task(task: Dict[str, Any]) -> Optional[Dict[str, float]]:
    try:
        return figure_extremes(task)
    except Exception:
        import traceback
        print(f"[zone] scale failed for {task.get('family')} "
              f"{task.get('id_stn')}:\n{traceback.format_exc()}",
              file=sys.stderr, flush=True)
        return None


def zone_plot_task(task: Dict[str, Any]) -> Optional[str]:
    import traceback
    try:
        return zone_plot(task)
    except Exception:
        print(f"[zone] plot failed for {task.get('family')} "
              f"{task.get('function')} {task.get('id_stn')}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        plt.close('all')
        return None
