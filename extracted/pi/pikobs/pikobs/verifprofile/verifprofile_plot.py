#!/usr/bin/python3
"""Figures of pikobs.verifprofile.

A vertical profile of the departures, level by level, over a whole
region. Three panels in a row, sharing the vertical axis:

``Mean``
    the mean departure of each run, the control in black with squares and
    the experience in red with circles, around a dotted zero.
``Relative sigma``
    the change of the sigma, 100 x (sigma_exp - sigma_ctl) / sigma_ctl.
    A percentage is safe here: a sigma is never near zero, unlike a
    bias. Without a control this panel is the sigma itself.
``Observations``
    how many matched observations each level rests on, as bars.

With a control, each level of the first two panels carries a dot on the
left edge, from the test of that panel: the paired t-test for the mean,
the Pitman-Morgan test for the sigma. Red where the experience is better, blue where
the control is, hollow where the change is not larger than noise -- the
colours of the rest of Pikobs.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import pikobs
from matplotlib.ticker import MaxNLocator

from pikobs.figures import count_formatter, match_badge, save_figure, write_hover
from pikobs.stats.stats import BOOT_MIN_CYCLES, BOOT_MIN_PAIRS
from pikobs.obsdb import open_result
from pikobs.zone.zone_plot import members_text
from pikobs.stats import (MIN_CONFIDENCE, cycle_bootstrap_confidence, cycle_changes,
                          is_significant, moments_from_sums,
                          sigma_confidence,
                          ttest_confidence)

from pikobs.configobs.style import (CTL_BETTER, CTL_COLOUR, DPI, EXP_BETTER,
                                    EXP_COLOUR,
                                    GREY_TEXT, font_size)
from pikobs.obsdb import safe_name as _safe
PA_PER_HPA = 100.0
M_PER_KM = 1000.0
MIN_OBS_PER_LEVEL = 30

# Rows grow with the number of levels, so every channel keeps its label.
INCH_PER_ROW = 0.16
MIN_HEIGHT = 5.5
MAX_HEIGHT = 18.0          # past it a figure seen whole on a screen is unreadable
#: past this many channels a row is too thin for every name: one name in k,
#: thin test lines, and the channel under the mouse in the viewer
PANEL_WIDTH = 6.4
#: the lines, markers and dots, as thick as the text is big
LW, MS, DOT = 3.2, 9, 150
#: the room under each panel title, the same for all: the keys sit there
KEY_PAD = 1.7 * font_size('cell') + 6

_SINGLE_SUMS = {'omp': ('s_omp', 's2_omp'), 'oma': ('s_oma', 's2_oma'),
                'obs_error': ('s_err', 's2_err')}
# each quantity has its own count: a row without O-A still counts for O-P
_SINGLE_N = {'omp': 'n_omp', 'oma': 'n_oma', 'obs_error': 'n_err'}
_PAIR_N = {'omp': 'n', 'oma': 'n_oma'}
_PAIR_SUMS = {'omp': ('c_omp', 'c2_omp', 'e_omp', 'e2_omp', 'ce_omp'),
              'oma': ('c_oma', 'c2_oma', 'e_oma', 'e2_oma', 'ce_oma')}


def _extra(task: Dict[str, Any]) -> str:
    """_<surface>_<special> for a file name, each only when it splits
    something."""
    return "".join(f"_{_safe(x)}" for x in (task.get('land_ocean', 'all'),
                                             task.get('special_label', 'all'))
                   if x not in (None, '', 'all'))


def figure_name(task: Dict[str, Any]) -> str:
    # the surface and the special value after the region, only when
    # they split something: the naming convention of every module
    extra = _extra(task)
    return (f"verifprofile_{'_vs_'.join(_safe(n) for n in task['names'])}_"
            f"{_safe(task['family'])}_{task['function']}_"
            f"varno{_safe(task['varno'])}_{_safe(task['stn_tag'])}_"
            f"{_safe(task['region'])}{extra}_{_safe(task['flag'])}"
            f"{('_matchno' if task.get('match_mode') == 'no' else '_matchoff') if task.get('compare_off') else ''}.png")


def _axis_kind(vcotyp: str) -> str:
    lab = str(vcotyp).strip().upper()
    if lab.startswith('CANAL'):
        return 'channel'
    if lab.startswith('PRESSION'):
        return 'pressure'
    if lab.startswith('HAUTEUR'):
        return 'height'
    return 'level'


# ─────────────────────────────────────────────────────────────────────────────
# Reading: the lat bands and cycles of the extraction are summed away
# ─────────────────────────────────────────────────────────────────────────────

def _where(task) -> Tuple[str, list]:
    return ("region = ? AND flag = ? AND channel_mode = 'all' "
            "AND land_ocean = ? AND id_stn = ? AND special = ? AND varno = ?",
            [task['region'], task['flag'], task['land_ocean'],
             task['id_stn'], str(task.get('special', 'all')), task['varno']])


def _compare(task) -> bool:
    """A comparison figure: the pairs (MATCH on) or the two runs apart (off)."""
    return bool(task.get('matched') or task.get('compare_off'))


def read_profile(task) -> Optional[Dict[str, np.ndarray]]:
    if task.get('compare_off'):
        # MATCH off: the control and the experience, each with all its
        # observations, on the levels they both have
        ctl = read_profile(dict(task, compare_off=False, matched=False,
                                db_file=task['db_ctl']))
        exp = read_profile(dict(task, compare_off=False, matched=False))
        if ctl is None or exp is None:
            return None
        lev, ic, ie = np.intersect1d(ctl['lev'], exp['lev'], return_indices=True)
        if not len(lev):
            return None
        sc, se = ctl['sigma'][ic], exp['sigma'][ie]
        return {'lev': lev, 'n': np.minimum(ctl['n'][ic], exp['n'][ie]),
                'n_ctl': ctl['n'][ic], 'n_exp': exp['n'][ie],
                'mean_ctl': ctl['mean'][ic], 'mean_exp': exp['mean'][ie],
                'var_ctl': sc * sc, 'var_exp': se * se,
                'sigma_ctl': sc, 'sigma_exp': se}
    where, args = _where(task)
    with open_result(task['db_file']) as conn:
        if task['matched']:
            if task['function'] not in _PAIR_SUMS:
                return None
            c_s, c_s2, e_s, e_s2, ce = _PAIR_SUMS[task['function']]
            n_col = _PAIR_N[task['function']]
            rows = conn.execute(f"""
                SELECT vcoord, SUM({n_col}), SUM({c_s}), SUM({c_s2}), SUM({e_s}),
                       SUM({e_s2}), SUM({ce})
                FROM zone_pairs WHERE {where}
                GROUP BY vcoord ORDER BY vcoord;""", args).fetchall()
        else:
            s_c, s2_c = _SINGLE_SUMS[task['function']]
            n_col = _SINGLE_N[task['function']]
            rows = conn.execute(f"""
                SELECT vcoord, SUM({n_col}), SUM({s_c}), SUM({s2_c})
                FROM zone WHERE {where}
                GROUP BY vcoord ORDER BY vcoord;""", args).fetchall()
    rows = [r for r in rows if r[0] is not None and r[1]]
    if not rows:
        return None
    arr = np.array([[float(v) if v is not None else np.nan for v in r]
                    for r in rows])
    lev, n = arr[:, 0], arr[:, 1]
    if task['matched']:
        m_c, v_c = moments_from_sums(n, arr[:, 2], arr[:, 3])
        m_e, v_e = moments_from_sums(n, arr[:, 4], arr[:, 5])
        with np.errstate(divide='ignore', invalid='ignore'):
            cov = np.where(n > 0, arr[:, 6] / n - m_c * m_e, np.nan)
        return {'lev': lev, 'n': n, 'mean_ctl': m_c, 'mean_exp': m_e,
                'var_ctl': v_c, 'var_exp': v_e, 'cov': cov,
                'sigma_ctl': np.sqrt(v_c), 'sigma_exp': np.sqrt(v_e)}
    m, v = moments_from_sums(n, arr[:, 2], arr[:, 3])
    return {'lev': lev, 'n': n, 'mean': m, 'sigma': np.sqrt(v)}


def _no_departure(data, matched: bool) -> np.ndarray:
    """Levels where O-P is the same number for every observation.

    That is what a level the system does not use looks like: O-P stored as
    0 for every observation. There is no departure to look at, so the level
    is dropped, not drawn as a flat zero.
    """
    if matched:
        return ((np.asarray(data['sigma_ctl']) <= 0)
                & (np.asarray(data['sigma_exp']) <= 0))
    return np.asarray(data['sigma']) <= 0


def figure_extremes(task) -> Optional[Dict[str, float]]:
    """What one figure needs of each x axis, for the shared limits."""
    data = read_profile(task)
    if data is None:
        return None
    ok = ((data['n'] >= int(task.get('min_obs', MIN_OBS_PER_LEVEL)))
          & ~_no_departure(data, _compare(task)))
    if not np.any(ok):
        return None

    def _amax(values):
        # the 98th percentile: one odd level must not stretch the axis of
        # every figure of the group
        values = np.abs(np.asarray(values, float)[ok])
        values = values[np.isfinite(values)]
        return float(np.percentile(values, 98)) if values.size else None

    out = {'n': float(np.nanmax(np.fmax(data.get('n_ctl', data['n']),
                                        data.get('n_exp', data['n']))))}
    if _compare(task):
        out['mean'] = _amax(np.fmax(np.abs(data['mean_ctl']),
                                    np.abs(data['mean_exp'])))
        out['dbias'] = _amax(np.abs(data['mean_exp'])
                             - np.abs(data['mean_ctl']))
        with np.errstate(divide='ignore', invalid='ignore'):
            rel = 100.0 * (data['sigma_exp'] - data['sigma_ctl']) \
                / data['sigma_ctl']
        out['rel'] = _amax(rel)
    else:
        out['mean'] = _amax(data['mean'])
        out['sigma'] = _amax(data['sigma'])
    return {k: v for k, v in out.items() if v is not None}


#: a cycle counts in the tests on the cycles from this many pairs on
MIN_PAIRS_PER_CYCLE = BOOT_MIN_PAIRS


def cycle_level_sums(task) -> Optional[np.ndarray]:
    """(date, level, n, C, C2, E, E2, CE) of every cycle and level of a
    matched task."""
    fn = task['function']
    if fn not in _PAIR_SUMS:
        return None
    c_s, c_s2, e_s, e_s2, ce = _PAIR_SUMS[fn]
    where, args = _where(task)
    with open_result(task['db_file']) as conn:
        rows = conn.execute(f"""
            SELECT date, vcoord, SUM({_PAIR_N[fn]}), SUM({c_s}), SUM({c_s2}),
                   SUM({e_s}), SUM({e_s2}), SUM({ce})
            FROM zone_pairs WHERE {where}
            GROUP BY date, vcoord ORDER BY date, vcoord;""", args).fetchall()
    rows = [r for r in rows if r[0] is not None and r[1] is not None and r[2]]
    if not rows:
        return None
    return np.array([[float(v) if v is not None else np.nan for v in r]
                     for r in rows])



def level_cycle_tests(task, lev) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(bias confidence, sigma confidence, cycles) of every level of a
    matched figure: the change of each cycle on that level (cycles of at
    least MIN_PAIRS_PER_CYCLE pairs), and the cycle block bootstrap of its
    mean. NaN where the level has fewer cycles than the bootstrap tests;
    ``cycles`` says how many it has."""
    t_conf = np.full(len(lev), np.nan)
    f_conf = np.full(len(lev), np.nan)
    n_cyc = np.zeros(len(lev), int)
    arr = cycle_level_sums(task)
    if arr is None:
        return t_conf, f_conf, n_cyc
    for i, level in enumerate(np.asarray(lev, float)):
        k = arr[(arr[:, 1] == level) & (arr[:, 2] >= MIN_PAIRS_PER_CYCLE)]
        n_cyc[i] = len(k)
        if not len(k):
            continue
        bias, d_sigma = cycle_changes(k[:, 2], k[:, 3], k[:, 4], None, k[:, 5], k[:, 6])
        t_conf[i] = cycle_bootstrap_confidence(bias)
        f_conf[i] = cycle_bootstrap_confidence(d_sigma)
    return t_conf, f_conf, n_cyc


def _few_cycles(ax, y, conf, skip, n_cyc, x_dot) -> None:
    """A grey dash where a level has too few cycles to be tested, with the
    number of cycles it has beside it: not tested is not 'not significant'."""
    if n_cyc is None:
        return
    miss = ~np.isfinite(np.asarray(conf, float)) & ~np.asarray(skip, bool)
    if not miss.any():
        return
    yy = np.asarray(y)[miss]
    ax.scatter(np.full(int(miss.sum()), x_dot), yy, marker='_', s=2.2 * DOT,
               color='#8A9199', linewidths=3.5, zorder=6, clip_on=False)
    for yv, k in zip(yy, np.asarray(n_cyc)[miss]):
        ax.annotate(f"{int(k)}", (x_dot, yv), xytext=(16, 0), textcoords='offset points',
                    ha='left', va='center', fontsize=font_size('cell'),
                    color='#6B7280', annotation_clip=False)


# ─────────────────────────────────────────────────────────────────────────────
# Figure
# ─────────────────────────────────────────────────────────────────────────────

def _test_dots(ax, y, conf, change, x_dot, dense=False) -> Tuple[int, int]:
    """One dot per level on the left edge: red, blue or hollow -- a short
    thin line instead when the rows are too thin (many channels): dots
    would pile up into a column."""
    sig = is_significant(conf)
    better = np.asarray(change) < 0
    if dense:
        ok = np.isfinite(conf)
        yy = np.asarray(y)
        for keep, colour, width in ((ok & sig & better, EXP_BETTER, 5.0),
                                    (ok & sig & ~better, CTL_BETTER, 5.0),
                                    (ok & ~sig, '#B8BEC5', 1.6)):
            if np.any(keep):
                ax.scatter(np.full(int(keep.sum()), x_dot), yy[keep], s=(0.4 * 72) ** 2,
                           marker='_', color=colour, linewidths=width, zorder=6, clip_on=False)
        return int(np.sum(sig & better)), int(np.sum(sig & ~better))
    face = np.where(sig & better, EXP_BETTER,
                    np.where(sig & ~better, CTL_BETTER, 'white'))
    edge = np.where(sig & better, EXP_BETTER,
                    np.where(sig & ~better, CTL_BETTER, '#333333'))
    ok = np.isfinite(conf)
    ax.scatter(np.full(int(ok.sum()), x_dot), np.asarray(y)[ok], s=DOT,
               facecolors=face[ok], edgecolors=edge[ok], linewidths=2.0,
               zorder=6, clip_on=False)
    return int(np.sum(sig & better)), int(np.sum(sig & ~better))


def _fit(shared_value, own_values) -> float:
    """The shared limit of the group, widened if this figure needs more.

    A curve must never leave its frame: the shared limit comes from the
    98th percentile of the group, so a figure holding one of the extreme
    levels would have its line cut. The limit stays shared everywhere else.
    """
    own = np.abs(np.asarray(own_values, float))
    own = own[np.isfinite(own)]
    own_max = float(own.max()) if own.size else 0.0
    return _nice_limit(max(float(shared_value or 0.0), own_max * 1.05))


_SUPERSCRIPT = str.maketrans("-0123456789", "\u207b\u2070\u00b9\u00b2"
                             "\u00b3\u2074\u2075\u2076\u2077\u2078\u2079")


def _scale_of(limit: float) -> Tuple[float, str]:
    """(factor, text) for an axis whose values are very small or large.

    Matplotlib puts '1e-7' alone in a corner, where nobody sees it. Here
    the values are divided by the power of ten and the unit says so:
    [10^-7 mol/mol].
    """
    if not limit or not np.isfinite(limit):
        return 1.0, ""
    exp = int(np.floor(np.log10(abs(limit))))
    if -2 <= exp <= 3:
        return 1.0, ""
    return 10.0 ** exp, "10" + str(exp).translate(_SUPERSCRIPT) + " "


def _unit_label(prefix: str, units: str, scale_text: str) -> str:
    """'O-P [10^-7 mol/mol]' from 'O-P', '[mol/mol]' and the scale."""
    u = str(units).strip()
    if u.startswith('[') and u.endswith(']'):
        u = u[1:-1]
    return f"{prefix} [{scale_text}{u}]" if (u or scale_text) else prefix


def _nice_limit(value: float) -> float:
    if not value or not np.isfinite(value):
        return 1.0
    mag = 10 ** np.floor(np.log10(value))
    for m in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if m * mag >= value:
            return float(m * mag)
    return float(10 * mag)


def verifprofile_plot(task: Dict[str, Any]) -> Optional[str]:
    data = read_profile(task)
    if data is None:
        return None
    min_obs = int(task.get('min_obs', MIN_OBS_PER_LEVEL))
    few = data['n'] < min_obs
    flat_all = _no_departure(data, _compare(task))
    keep = ~few & ~flat_all
    n_thin = int(np.sum(few))
    n_empty = int(np.sum(flat_all & ~few))
    if not np.any(keep):
        return None
    data = {k: np.asarray(v)[keep] for k, v in data.items()}

    family = task['family']
    _, _, _, _, _, vcotyp = pikobs.family(family)
    kind = _axis_kind(vcotyp)
    var_name, units, _ = pikobs.type_varno(str(task['varno']))
    label = {'omp': 'O-P', 'oma': 'O-A',
             'obs_error': 'obs error'}[task['function']]
    gpsro = bool(task.get('gpsro'))
    # GPS-RO departures are normalised by the reference refractivity
    x_label = f"({label}) / B_ref" if gpsro else f"{label} {units}"
    if gpsro:
        units = "[-]"

    # the vertical axis: values for pressure and height, rows for channels
    lev = data['lev']
    if kind == 'pressure':
        y, y_label, invert = lev / PA_PER_HPA, 'Pressure [hPa]', True
    elif kind == 'height':
        y, y_label, invert = lev / M_PER_KM, 'Height [km]', False
    elif kind == 'channel':
        y, y_label, invert = np.arange(len(lev)), 'Channel', False   # small channels at the bottom
    else:
        y, y_label, invert = lev, 'Level', False
    as_rows = kind == 'channel'
    # a pressure axis spanning more than a decade is read on a log scale,
    # as every stratospheric profile is: MLS goes from 260 hPa to 0.02
    log_p = (kind == 'pressure' and np.all(y > 0)
             and np.nanmax(y) / max(np.nanmin(y), 1e-12) > 15)

    n_levels = len(lev)
    height = float(np.clip(1.8 + INCH_PER_ROW * n_levels, MIN_HEIGHT,
                           MAX_HEIGHT)) if as_rows else 10.0
    # one channel name in `step`: as many as the rows hold at the size of
    # the other numbers; dense when not every name fits
    step = 1
    if as_rows:
        row_pt = 0.78 * height * 72.0 / max(n_levels, 1)
        step = max(1, int(np.ceil(1.35 * font_size('tick') / max(row_pt, 1e-6))))
    dense = step > 1
    # the header grows with its lines (see the end); the x labels hold two
    # lines of big text and the numbers of the axis under them
    header_in = ((4.1 if task.get('match_mode') != 'no' else 2.9) if _compare(task) else 2.9) \
        + 0.4 * (bool(n_thin) + bool(n_empty))
    if _compare(task):
        # a level with no sigma in the control is known only once drawn:
        # its note line is kept free whenever the control has a flat level
        with np.errstate(invalid='ignore'):
            header_in += 0.4 * bool(np.any(np.asarray(data['sigma_ctl']) <= 0))
    footer_in = 3.3
    fig_h = height + header_in + footer_in
    # with a control a fourth panel, the change of the bias: the two mean
    # curves often sit on top of each other, and the difference that the
    # test is about is a hundred times smaller than the values
    n_pan = 4 if _compare(task) else 3
    fig_w = PANEL_WIDTH * n_pan + 1.4
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor='white')
    fig.subplots_adjust(left=2.6 / fig_w, right=0.985, wspace=0.22,
                        top=1.0 - header_in / fig_h,
                        bottom=footer_in / fig_h)
    gs = fig.add_gridspec(1, n_pan)
    ax1 = fig.add_subplot(gs[0, 0])
    if _compare(task):
        axb = fig.add_subplot(gs[0, 1], sharey=ax1)
        ax2 = fig.add_subplot(gs[0, 2], sharey=ax1)
        ax3 = fig.add_subplot(gs[0, 3], sharey=ax1)
    else:
        axb = None
        ax2 = fig.add_subplot(gs[0, 1], sharey=ax1)
        ax3 = fig.add_subplot(gs[0, 2], sharey=ax1)
    shared = task.get('scales') or {}
    names = task['names']
    counts = {}
    n_flat = 0

    # ---- panel 1: the mean of each run -------------------------------------
    if _compare(task):
        xm = _fit(shared.get('mean'),
                  np.concatenate([data['mean_ctl'], data['mean_exp']]))
        f1, s1 = (1.0, "") if gpsro else _scale_of(xm)
        ax1.plot(data['mean_ctl'] / f1, y, '-s', color=CTL_COLOUR, lw=LW,
                 ms=MS, label='Ctl')
        ax1.plot(data['mean_exp'] / f1, y, '-.o', color=EXP_COLOUR, lw=LW,
                 ms=MS, label='Exp')
        change = np.abs(data['mean_exp']) - np.abs(data['mean_ctl'])
        # MATCH on: the cycle block bootstrap, level by level, on the
        # change of every cycle (the same test as the scorecard)
        if task['matched']:
            t_conf, f_conf_boot, n_cyc = level_cycle_tests(task, data['lev'])
        elif task.get('match_mode') == 'no':
            # MATCH no: the two runs side by side, and no test at all
            t_conf = np.full(len(y), np.nan)
            f_conf_boot = np.full(len(y), np.nan)
            n_cyc = None
        else:
            # MATCH off: each run with all its observations, Welch on the
            # mean and the F-test on the sigma
            t_conf = ttest_confidence(data['mean_ctl'], data['sigma_ctl'], data['n_ctl'],
                                      data['mean_exp'], data['sigma_exp'], data['n_exp'])
            f_conf_boot = sigma_confidence(data['var_ctl'], data['var_exp'],
                                           data['n_ctl'], data['n_exp'])
            n_cyc = None                       # no cycles behind Welch and F
        # a level with no sigma cannot be tested: a grey cross, not a
        # hollow dot that would read as "tested, not significant"
        flat_t = np.asarray(data['sigma_ctl']) <= 0
        t_conf = np.where(flat_t, np.nan, t_conf)

        # ---- panel 2: the change of the bias, at its own scale ----------
        # never narrower than 1 % of the bias itself: a change that small
        # is numerical noise, and a scale built on it would magnify it
        xb = max(_fit(shared.get('dbias'), change), _nice_limit(0.01 * xm))
        fb, sb = _scale_of(xb)
        xs_b = xb / fb
        axb.plot(change / fb, y, '-o', color='#555555', lw=LW, ms=MS)
        axb.axvline(0, color='black', ls=':', lw=2.2)
        axb.axvspan(-xs_b, 0, color=EXP_BETTER, alpha=0.05, zorder=0)
        axb.axvspan(0, xs_b, color=CTL_BETTER, alpha=0.05, zorder=0)
        counts['t'] = _test_dots(axb, y, t_conf, change, -xs_b * 0.9, dense)
        _few_cycles(axb, y, t_conf, flat_t, n_cyc, -xs_b * 0.9)
        if np.any(flat_t):
            axb.scatter(np.full(int(flat_t.sum()), -xs_b * 0.9),
                        np.asarray(y)[flat_t], marker='x', s=DOT,
                        color='#7f8c8d', linewidths=2.5, zorder=6,
                        clip_on=False)
        axb.set_xlim(-xs_b, xs_b)
        axb.set_title("Bias change" + (" / B_ref" if gpsro else ""), fontsize=font_size('table_title'), pad=KEY_PAD)
        axb.set_xlabel(_unit_label("|Exp| - |Ctl|", "[-]" if gpsro else units, sb)
                       + "\nleft = Exp closer to zero", fontsize=font_size('axis_label'))
    else:
        xm = _fit(shared.get('mean'), data['mean'])
        f1, s1 = (1.0, "") if gpsro else _scale_of(xm)
        ax1.plot(data['mean'] / f1, y, '-o', color=CTL_COLOUR, lw=LW, ms=MS,
                 label=names[0])
    ax1.axvline(0, color='black', ls=':', lw=2.2)
    ax1.set_xlim(-xm / f1, xm / f1)
    ax1.set_title(f"Mean ({label})" + (" / B_ref" if gpsro else ""), fontsize=font_size('table_title'),
                  pad=KEY_PAD)          # room for the key under it
    ax1.set_xlabel(x_label if gpsro else _unit_label(label, units, s1),
                   fontsize=font_size('axis_label'))
    ax1.set_ylabel(y_label, fontsize=font_size('axis_label'))
    # the key above the panel, under its title: inside, it would cover the curves
    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False,
               fontsize=font_size('cell'), borderaxespad=0.15, handlelength=1.8,
               columnspacing=1.2)

    # ---- panel 2: the sigma -------------------------------------------------
    if _compare(task):
        with np.errstate(divide='ignore', invalid='ignore'):
            rel = 100.0 * (data['sigma_exp'] - data['sigma_ctl']) \
                / data['sigma_ctl']
        # levels where the control has no sigma at all: O-P is the same
        # number for every observation, usually 0 on levels the system
        # does not use. The ratio does not exist there; say so
        flat = np.asarray(data['sigma_ctl']) <= 0
        n_flat = int(np.sum(flat))
        ax2.plot(rel, y, '-o', color=EXP_COLOUR, lw=LW, ms=MS,
                 label="Exp - Ctl")
        if n_flat:
            # the level is still there: marked on zero, so both panels keep
            # exactly the same levels and the eye pairs the rows correctly
            ax2.scatter(np.zeros(n_flat), np.asarray(y)[flat], marker='x',
                        s=DOT, color='#7f8c8d', linewidths=2.5, zorder=5,
                        label="no sigma in the control")
        # never narrower than +/-0.5 %: below that a change of the sigma
        # is noise, and the axis would magnify rounding errors
        xr = max(_fit(shared.get('rel'), rel), 0.5)
        # the cycle block bootstrap of the sigma change (level_cycle_tests)
        f_conf = f_conf_boot
        f_conf = np.where(flat, np.nan, f_conf)
        counts['F'] = _test_dots(ax2, y, f_conf, rel, -xr * 0.9, dense)
        _few_cycles(ax2, y, f_conf, flat, n_cyc, -xr * 0.9)
        if n_flat:
            ax2.scatter(np.full(n_flat, -xr * 0.9), np.asarray(y)[flat],
                        marker='x', s=DOT, color='#7f8c8d', linewidths=2.5,
                        zorder=6, clip_on=False)
        ax2.axvline(0, color='black', ls=':', lw=2.2)
        ax2.set_xlim(-xr, xr)
        ax2.set_title(f"Relative sigma ({label})" +
                      (" / B_ref" if gpsro else ""), fontsize=font_size('table_title'), pad=KEY_PAD)
        ax2.set_xlabel("(Exp - Ctl) / Ctl  [%]", fontsize=font_size('axis_label'))
        # no key: one curve, and its axis says what it is (Exp - Ctl) / Ctl
    else:
        ax2.plot(data['sigma'], y, '-o', color=CTL_COLOUR, lw=1.8, ms=5)
        xs = _fit(shared.get('sigma'), data['sigma'])
        ax2.set_xlim(0, xs)
        ax2.set_title(f"Sigma ({label})" + (" / B_ref" if gpsro else ""), fontsize=font_size('table_title'), pad=KEY_PAD)
        ax2.set_xlabel(f"sigma {x_label}", fontsize=font_size('axis_label'))

    # ---- panel 3: the sample behind each level --------------------------------
    # each bar as thick as its own level: the minimum spacing made every
    # bar a hairline as soon as two levels sat close together
    two = bool(task.get('compare_off'))      # MATCH off: each run its own count
    if as_rows or len(y) < 2:
        if two:
            ax3.barh(np.asarray(y) - 0.18, data['n_ctl'], height=0.35, color=CTL_COLOUR,
                     edgecolor='none', label='Ctl')
            ax3.barh(np.asarray(y) + 0.18, data['n_exp'], height=0.35, color=EXP_COLOUR,
                     edgecolor='none', label='Exp')
        else:
            ax3.barh(y, data['n'], height=0.7, color='#7f8c8d',
                     edgecolor='none')
    else:
        order = np.argsort(y)
        ys = np.asarray(y, float)[order]
        if log_p:
            ly = np.log10(ys)
            mids = 10 ** ((ly[:-1] + ly[1:]) / 2.0)
            lo = np.concatenate(([ys[0] / (mids[0] / ys[0])], mids))
            hi = np.concatenate((mids, [ys[-1] * (ys[-1] / mids[-1])]))
        else:
            mids = (ys[:-1] + ys[1:]) / 2.0
            lo = np.concatenate(([ys[0] - (mids[0] - ys[0])], mids))
            hi = np.concatenate((mids, [ys[-1] + (ys[-1] - mids[-1])]))
        span = hi - lo
        if two:
            ax3.barh(lo + 0.15 * span, np.asarray(data['n_ctl'])[order],
                     height=0.35 * span, align='edge', color=CTL_COLOUR,
                     edgecolor='none', label='Ctl')
            ax3.barh(lo + 0.5 * span, np.asarray(data['n_exp'])[order],
                     height=0.35 * span, align='edge', color=EXP_COLOUR,
                     edgecolor='none', label='Exp')
        else:
            ax3.barh(lo + 0.15 * span, np.asarray(data['n'])[order],
                     height=0.7 * span, align='edge', color='#7f8c8d',
                     edgecolor='none')
    n_top = np.fmax(data['n_ctl'], data['n_exp']) if two else data['n']
    # the counts at the figure's own scale, not the group's: one region
    # can hold a hundred times the observations of another, and a shared
    # limit leaves the small one with bars too thin to read
    ax3.set_xlim(0, _fit(None, n_top))
    if two:
        # the key of the two bars above the panel, under its title: inside it,
        # with a bar on every level, it would always cover some of them
        for xk, name, colour in ((0.3, "Ctl", CTL_COLOUR), (0.7, "Exp", EXP_COLOUR)):
            ax3.text(xk, 1.012, f"\u25a0 {name}", transform=ax3.transAxes, ha='center',
                     va='bottom', fontsize=font_size('cell'), fontweight='bold', color=colour)
    ax3.set_title("Observations" + (" (matched)" if task['matched'] else ""),
                  fontsize=font_size('table_title'),
                  pad=KEY_PAD)
    ax3.set_xlabel("per level", fontsize=font_size('axis_label'))
    ax3.xaxis.set_major_formatter(count_formatter())

    # ---- shared vertical axis --------------------------------------------------
    for ax in [a for a in (ax1, axb, ax2, ax3) if a is not None]:
        ax.grid(True, ls='--', alpha=0.4)
        ax.tick_params(labelsize=font_size('tick'), width=1.8, length=8)
        # a few numbers on each axis, none on its two ends: big text, and
        # the ends of two panels side by side would run into each other
        ax.xaxis.set_major_locator(MaxNLocator(5, prune='both'))
    # counts start at 0, and that 0 stays
    ax3.xaxis.set_major_locator(MaxNLocator(5, prune='upper'))
    if as_rows:
        fs = font_size('tick') if dense else float(np.clip(
            0.78 * height / max(n_levels, 1) * 72 / 1.35, 3.5, font_size('tick')))
        ax1.set_yticks(y[::step])
        ax1.set_yticklabels([f"{v:g}" for v in list(lev)[::step]], fontsize=fs)
        ax1.set_ylim(-0.5, n_levels - 0.5)
    if log_p:
        ax1.set_yscale('log')
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda v, _: f"{v:g}"))
    if invert:
        ax1.invert_yaxis()
    for ax in [a for a in (axb, ax2, ax3) if a is not None]:
        ax.tick_params(axis='y', labelleft=False)

    # ---- header ---------------------------------------------------------------
    # on the left, a line each, in inches from the top; the MATCH badge on
    # the right: what is compared, and how, read first on a slide
    where = (f"{task['datestart']} to {task['dateend']}  \u00b7  region {task['region']}"
             f"  \u00b7  flags {task['flag']}  \u00b7  {task.get('member_word', 'station')} "
             f"{members_text(task['db_file'], task['id_stn'])}  \u00b7  {task['land_ocean']}")
    if task.get('special_label') and task['special_label'] != 'all':
        where += f"  \u00b7  method {task['special_label']}"
    notes = []
    if n_thin:
        notes.append(f"{n_thin} level(s) dropped: fewer than {min_obs} observations")
    if n_empty:
        notes.append(f"{n_empty} level(s) dropped: O-P identical for every observation, "
                     f"no departure there (a level the system does not use)")
    if _compare(task) and n_flat:
        notes.append(f"{n_flat} level(s) with no sigma in the control only: no ratio there")

    def at(inch):
        return 1 - inch / fig_h
    x0 = 0.012
    fig.text(x0, at(0.15), f"{family}  \u00b7  {var_name} {units}",
             fontsize=font_size('title'), fontweight='bold', color='#1F2933', va='top')
    if _compare(task):
        t = fig.text(x0, at(0.85), f"Ctl  {names[0]}", fontsize=font_size('names'),
                     fontweight='bold', color=CTL_COLOUR, va='top')
        box = t.get_window_extent(renderer=fig.canvas.get_renderer())
        xe = fig.transFigure.inverted().transform((box.x1, box.y0))[0] + 0.02
        fig.text(xe, at(0.85), f"Exp  {names[1]}", fontsize=font_size('names'),
                 fontweight='bold', color=EXP_COLOUR, va='top')
    else:
        fig.text(x0, at(0.85), names[0], fontsize=font_size('names'), fontweight='bold',
                 color=CTL_COLOUR, va='top')
    fig.text(x0, at(1.45), where, fontsize=font_size('note'), color=GREY_TEXT, va='top')
    y_in = 1.95
    if _compare(task) and task.get('match_mode') != 'no':
        tr, tb = counts.get('t', (0, 0))
        fr, fb = counts.get('F', (0, 0))
        few = (f"  \u00b7  grey dash: fewer than {BOOT_MIN_CYCLES} cycles, "
               f"the number beside it" if task['matched'] else "")
        fig.text(x0, at(y_in), (f"lines: red = Exp better  \u00b7  blue = Ctl better  \u00b7  "
                                f"grey = not significant ({MIN_CONFIDENCE:.0f} %){few}" if dense else
                                f"dots: red = Exp better  \u00b7  blue = Ctl better  \u00b7  "
                                f"hollow = not significant ({MIN_CONFIDENCE:.0f} %){few}"),
                 fontsize=font_size('note'), color='#30343A', va='top')
        fig.text(x0, at(y_in + 0.5), f"bias: {tr} red, {tb} blue  \u00b7  sigma: {fr} red, "
                 f"{fb} blue", fontsize=font_size('note'), color='#30343A', va='top')
        y_in += 1.0
        match_badge(fig, task['matched'], top_in=0.15)
    for note in notes:
        fig.text(x0, at(y_in), note, fontsize=0.8 * font_size('note'), color=GREY_TEXT,
                 va='top')
        y_in += 0.4

    out_dir = os.path.join(task['pathwork'], family)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, figure_name(task))
    save_figure(fig, out_file, svg=task.get('svg', False), dpi=DPI)
    if as_rows:            # the channel under the mouse, in the viewer
        write_hover(fig, out_file, ax1, [(yi, f"{v:g}") for yi, v in zip(y, lev)],
                    word="channel", dpi=DPI)
    plt.close(fig)
    return out_file


def verifprofile_plot_task(task: Dict[str, Any]) -> Optional[str]:
    import traceback
    try:
        return verifprofile_plot(task)
    except Exception:
        print(f"[verifprofile] plot failed for {task.get('family')} "
              f"{task.get('id_stn')} varno {task.get('varno')}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        plt.close('all')
        return None


def verifprofile_scale_task(task: Dict[str, Any]) -> Optional[Dict[str, float]]:
    try:
        return figure_extremes(task)
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Every experience against the same control, on one figure
# ─────────────────────────────────────────────────────────────────────────────

# Okabe-Ito: told apart by colour-blind readers too, and none of them is the
# red or blue of the significance code.
OVERLAY_COLOURS = ['#E69F00', '#56B4E9', '#009E73', '#CC79A7', '#0072B2',
                   '#D55E00', '#F0E442', '#000000']


def overlay_name(task: Dict[str, Any]) -> str:
    return (f"verifprofile_ratio_{_safe(task['control'])}_"
            f"{_safe(task['family'])}_{task['function']}_"
            f"varno{_safe(task['varno'])}_{_safe(task['stn_tag'])}_"
            f"{_safe(task['region'])}{_extra(task)}_{_safe(task['flag'])}.png")


def verifprofile_overlay(task: Dict[str, Any]) -> Optional[str]:
    """sigma_exp / sigma_ctl against the level, one curve per experience.

    The ratio is 1 where nothing changed and below 1 where the experience
    fits the observations better. A filled marker is a level where the
    sigma test passes; a hollow one is within the noise.
    """
    min_obs = int(task.get('min_obs', MIN_OBS_PER_LEVEL))
    family = task['family']
    _, _, _, _, _, vcotyp = pikobs.family(family)
    kind = _axis_kind(vcotyp)
    label = {'omp': 'O-P', 'oma': 'O-A',
             'obs_error': 'obs error'}[task['function']]
    gpsro = bool(task.get('gpsro'))

    curves = []
    for member in task['members']:
        sub = dict(task, db_file=member['db_file'], matched=True)
        data = read_profile(sub)
        if data is None:
            continue
        keep = (data['n'] >= min_obs) & ~_no_departure(data, True)
        if not np.any(keep):
            continue
        data = {k: np.asarray(v)[keep] for k, v in data.items()}
        with np.errstate(divide='ignore', invalid='ignore'):
            ratio = data['sigma_exp'] / data['sigma_ctl']
        # the sigma of each level: the cycle block bootstrap of the pairs,
        # as on the profiles (NaN where a level has too few cycles)
        _, conf, _ = level_cycle_tests(sub, data['lev'])
        curves.append((member['name'], data['lev'], ratio, conf))
    if not curves:
        return None

    all_lev = np.unique(np.concatenate([c[1] for c in curves]))
    if kind == 'pressure':
        to_y, y_label, invert = (lambda v: v / PA_PER_HPA), 'Pressure [hPa]', \
            True
    elif kind == 'height':
        to_y, y_label, invert = (lambda v: v / M_PER_KM), 'Height [km]', \
            False
    elif kind == 'channel':
        index = {v: i for i, v in enumerate(all_lev)}
        to_y = (lambda v: np.array([index[x] for x in v], float))
        y_label, invert = 'Channel', False   # small channels at the bottom
    else:
        to_y, y_label, invert = (lambda v: v), 'Level', False

    n_levels = len(all_lev)
    height = (float(np.clip(1.8 + INCH_PER_ROW * n_levels, MIN_HEIGHT,
                            MAX_HEIGHT)) if kind == 'channel' else 8.0)
    fig_h = height + 1.5
    fig, ax = plt.subplots(figsize=(7.5, fig_h), facecolor='white')
    fig.subplots_adjust(left=0.16, right=0.96, top=1.0 - 1.3 / fig_h,
                        bottom=0.7 / fig_h)

    span = 0.0
    for i, (name, lev, ratio, conf) in enumerate(curves):
        colour = OVERLAY_COLOURS[i % len(OVERLAY_COLOURS)]
        y = to_y(lev)
        ax.plot(ratio, y, '-', color=colour, lw=1.6, label=name)
        sig = is_significant(conf)
        ax.scatter(ratio[sig], np.asarray(y)[sig], s=22, color=colour,
                   zorder=4)
        ax.scatter(ratio[~sig], np.asarray(y)[~sig], s=22,
                   facecolors='white', edgecolors=colour, zorder=4)
        finite = np.abs(ratio[np.isfinite(ratio)] - 1.0)
        if finite.size:
            span = max(span, float(np.percentile(finite, 98)))
    span = task.get('ratio_span') or span
    half = _nice_limit(max(span, 0.005))
    ax.axvline(1.0, color='black', ls=':', lw=2.2)
    ax.set_xlim(1.0 - half, 1.0 + half)
    ax.set_xlabel(f"sigma_exp / sigma_ctl   ({label}"
                  + (" / B_ref" if gpsro else "") + ")", fontsize=10)
    ax.set_ylabel(y_label, fontsize=11)
    ax.grid(True, ls='--', alpha=0.4)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    if kind == 'channel':
        row_pt = 0.78 * height * 72.0 / max(n_levels, 1)
        o_step = max(1, int(np.ceil(1.35 * 9 / max(row_pt, 1e-6))))
        fs = 9 if o_step > 1 else float(np.clip(row_pt / 1.35, 3.5, 9))
        ax.set_yticks(np.arange(n_levels)[::o_step])
        ax.set_yticklabels([f"{v:g}" for v in list(all_lev)[::o_step]], fontsize=fs)
        ax.set_ylim(-0.5, n_levels - 0.5)
    yv = to_y(all_lev) if kind != 'channel' else None
    if kind == 'pressure' and yv is not None and np.all(yv > 0) \
            and yv.max() / max(yv.min(), 1e-12) > 15:
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    if invert:
        ax.invert_yaxis()

    var_name, units, _ = pikobs.type_varno(str(task['varno']))
    head = f"Sigma ratio against {task['control']}"
    sub = (f"{family}  |  {var_name}  |  {task['datestart']} to "
           f"{task['dateend']}\nregion {task['region']}  |  flags "
           f"{task['flag']}  |  {task.get('member_word', 'station')} "
           f"{task['id_stn']}  |  {task['land_ocean']}\n"
           f"below 1 = the experience fits better; filled = sigma test above "
           f"{MIN_CONFIDENCE:.0f} %")
    fig.suptitle(f"{head}\n{sub}", fontsize=10.5, fontweight='bold',
                 y=1.0 - 0.1 / fig_h, va='top')

    out_dir = os.path.join(task['pathwork'], family)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, overlay_name(task))
    save_figure(fig, out_file, svg=task.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out_file


def verifprofile_overlay_task(task: Dict[str, Any]) -> Optional[str]:
    import traceback
    try:
        return verifprofile_overlay(task)
    except Exception:
        print(f"[verifprofile] ratio figure failed for {task.get('family')} "
              f"{task.get('id_stn')}:\n{traceback.format_exc()}",
              file=sys.stderr, flush=True)
        plt.close('all')
        return None
