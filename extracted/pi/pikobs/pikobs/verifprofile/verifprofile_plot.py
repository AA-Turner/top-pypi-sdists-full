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
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import pikobs
from pikobs.figures import save_figure
from pikobs.obsdb import open_result
from pikobs.zone.zone_plot import members_text
from pikobs.stats import (MIN_CONFIDENCE, is_significant, moments_from_sums,
                          paired_ttest_confidence, sigma_confidence)

from pikobs.configobs.style import (CTL_BETTER, CTL_COLOUR, DPI, EXP_BETTER,
                                    EXP_COLOUR)
PA_PER_HPA = 100.0
M_PER_KM = 1000.0
MIN_OBS_PER_LEVEL = 30

# Rows grow with the number of levels, so every channel keeps its label.
INCH_PER_ROW = 0.16
MIN_HEIGHT = 5.5
MAX_HEIGHT = 60.0
PANEL_WIDTH = 4.6

_SINGLE_SUMS = {'omp': ('s_omp', 's2_omp'), 'oma': ('s_oma', 's2_oma'),
                'obs_error': ('s_err', 's2_err')}
# each quantity has its own count: a row without O-A still counts for O-P
_SINGLE_N = {'omp': 'n_omp', 'oma': 'n_oma', 'obs_error': 'n_err'}
_PAIR_N = {'omp': 'n', 'oma': 'n_oma'}
_PAIR_SUMS = {'omp': ('c_omp', 'c2_omp', 'e_omp', 'e2_omp', 'ce_omp'),
              'oma': ('c_oma', 'c2_oma', 'e_oma', 'e2_oma', 'ce_oma')}


def _safe(text: Any) -> str:
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


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
            f"{_safe(task['region'])}{extra}_{_safe(task['flag'])}.png")


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


def read_profile(task) -> Optional[Dict[str, np.ndarray]]:
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
          & ~_no_departure(data, task['matched']))
    if not np.any(ok):
        return None

    def _amax(values):
        # the 98th percentile: one odd level must not stretch the axis of
        # every figure of the group
        values = np.abs(np.asarray(values, float)[ok])
        values = values[np.isfinite(values)]
        return float(np.percentile(values, 98)) if values.size else None

    out = {'n': float(np.nanmax(data['n']))}
    if task['matched']:
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


# ─────────────────────────────────────────────────────────────────────────────
# Figure
# ─────────────────────────────────────────────────────────────────────────────

def _test_dots(ax, y, conf, change, x_dot) -> Tuple[int, int]:
    """One dot per level on the left edge: red, blue or hollow."""
    sig = is_significant(conf)
    better = np.asarray(change) < 0
    face = np.where(sig & better, EXP_BETTER,
                    np.where(sig & ~better, CTL_BETTER, 'white'))
    edge = np.where(sig & better, EXP_BETTER,
                    np.where(sig & ~better, CTL_BETTER, '#333333'))
    ok = np.isfinite(conf)
    ax.scatter(np.full(int(ok.sum()), x_dot), np.asarray(y)[ok], s=34,
               facecolors=face[ok], edgecolors=edge[ok], linewidths=1.0,
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
    flat_all = _no_departure(data, task['matched'])
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
        y, y_label, invert = np.arange(len(lev)), 'Channel', True
    else:
        y, y_label, invert = lev, 'Level', False
    as_rows = kind == 'channel'
    # a pressure axis spanning more than a decade is read on a log scale,
    # as every stratospheric profile is: MLS goes from 260 hPa to 0.02
    log_p = (kind == 'pressure' and np.all(y > 0)
             and np.nanmax(y) / max(np.nanmin(y), 1e-12) > 15)

    n_levels = len(lev)
    height = float(np.clip(1.8 + INCH_PER_ROW * n_levels, MIN_HEIGHT,
                           MAX_HEIGHT)) if as_rows else 7.0
    header_in = 1.4 if task['matched'] else 1.1
    footer_in = 0.9
    fig_h = height + header_in + footer_in
    # with a control a fourth panel, the change of the bias: the two mean
    # curves often sit on top of each other, and the difference that the
    # test is about is a hundred times smaller than the values
    n_pan = 4 if task['matched'] else 3
    fig_w = PANEL_WIDTH * n_pan + 1.4
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor='white')
    fig.subplots_adjust(left=1.1 / fig_w, right=0.985, wspace=0.12,
                        top=1.0 - header_in / fig_h,
                        bottom=footer_in / fig_h)
    gs = fig.add_gridspec(1, n_pan)
    ax1 = fig.add_subplot(gs[0, 0])
    if task['matched']:
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
    if task['matched']:
        xm = _fit(shared.get('mean'),
                  np.concatenate([data['mean_ctl'], data['mean_exp']]))
        f1, s1 = (1.0, "") if gpsro else _scale_of(xm)
        ax1.plot(data['mean_ctl'] / f1, y, '-s', color=CTL_COLOUR, lw=1.8,
                 ms=5, label=names[0])
        ax1.plot(data['mean_exp'] / f1, y, '-.o', color=EXP_COLOUR, lw=1.8,
                 ms=5, label=names[1])
        change = np.abs(data['mean_exp']) - np.abs(data['mean_ctl'])
        t_conf = paired_ttest_confidence(data['mean_ctl'], data['mean_exp'],
                                         data['var_ctl'], data['var_exp'],
                                         data['cov'], data['n'])
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
        axb.plot(change / fb, y, '-o', color='#555555', lw=1.6, ms=4.5)
        axb.axvline(0, color='black', ls=':', lw=1.4)
        axb.axvspan(-xs_b, 0, color=EXP_BETTER, alpha=0.05, zorder=0)
        axb.axvspan(0, xs_b, color=CTL_BETTER, alpha=0.05, zorder=0)
        counts['t'] = _test_dots(axb, y, t_conf, change, -xs_b * 0.9)
        if np.any(flat_t):
            axb.scatter(np.full(int(flat_t.sum()), -xs_b * 0.9),
                        np.asarray(y)[flat_t], marker='x', s=34,
                        color='#7f8c8d', linewidths=1.4, zorder=6,
                        clip_on=False)
        axb.set_xlim(-xs_b, xs_b)
        axb.set_title("Bias change" + (" / B_ref" if gpsro else ""),
                      fontsize=12)
        axb.set_xlabel(_unit_label("|mean_exp| - |mean_ctl|",
                                   "[-]" if gpsro else units, sb)
                       + f"\nleft = {names[1]} closer to zero", fontsize=9.5)
    else:
        xm = _fit(shared.get('mean'), data['mean'])
        f1, s1 = (1.0, "") if gpsro else _scale_of(xm)
        ax1.plot(data['mean'] / f1, y, '-o', color=CTL_COLOUR, lw=1.8, ms=5,
                 label=names[0])
    ax1.axvline(0, color='black', ls=':', lw=1.4)
    ax1.set_xlim(-xm / f1, xm / f1)
    ax1.set_title(f"Mean ({label})" + (" / B_ref" if gpsro else ""),
                  fontsize=12)
    ax1.set_xlabel(x_label if gpsro else _unit_label(label, units, s1),
                   fontsize=10)
    ax1.set_ylabel(y_label, fontsize=11)
    ax1.legend(loc='lower right', fontsize=9, framealpha=0.9)

    # ---- panel 2: the sigma -------------------------------------------------
    if task['matched']:
        with np.errstate(divide='ignore', invalid='ignore'):
            rel = 100.0 * (data['sigma_exp'] - data['sigma_ctl']) \
                / data['sigma_ctl']
        # levels where the control has no sigma at all: O-P is the same
        # number for every observation, usually 0 on levels the system
        # does not use. The ratio does not exist there; say so
        flat = np.asarray(data['sigma_ctl']) <= 0
        n_flat = int(np.sum(flat))
        ax2.plot(rel, y, '-o', color=EXP_COLOUR, lw=1.8, ms=5,
                 label=f"{names[1]} - {names[0]}")
        if n_flat:
            # the level is still there: marked on zero, so both panels keep
            # exactly the same levels and the eye pairs the rows correctly
            ax2.scatter(np.zeros(n_flat), np.asarray(y)[flat], marker='x',
                        s=40, color='#7f8c8d', linewidths=1.6, zorder=5,
                        label="no sigma in the control")
        # never narrower than +/-0.5 %: below that a change of the sigma
        # is noise, and the axis would magnify rounding errors
        xr = max(_fit(shared.get('rel'), rel), 0.5)
        # Pitman-Morgan when the pairs carry their covariance, the
        # F-test otherwise -- stats.sigma_confidence decides
        f_conf = sigma_confidence(np.square(data['sigma_ctl']),
                                  np.square(data['sigma_exp']),
                                  data['n'], cov=data.get('cov'))
        f_conf = np.where(flat, np.nan, f_conf)
        counts['F'] = _test_dots(ax2, y, f_conf, rel, -xr * 0.9)
        if n_flat:
            ax2.scatter(np.full(n_flat, -xr * 0.9), np.asarray(y)[flat],
                        marker='x', s=34, color='#7f8c8d', linewidths=1.4,
                        zorder=6, clip_on=False)
        ax2.axvline(0, color='black', ls=':', lw=1.4)
        ax2.set_xlim(-xr, xr)
        ax2.set_title(f"Relative sigma ({label})" +
                      (" / B_ref" if gpsro else ""), fontsize=12)
        ax2.set_xlabel("100 x (sigma_exp - sigma_ctl) / sigma_ctl  [%]",
                       fontsize=10)
        ax2.legend(loc='lower right', fontsize=9, framealpha=0.9)
    else:
        ax2.plot(data['sigma'], y, '-o', color=CTL_COLOUR, lw=1.8, ms=5)
        xs = _fit(shared.get('sigma'), data['sigma'])
        ax2.set_xlim(0, xs)
        ax2.set_title(f"Sigma ({label})" + (" / B_ref" if gpsro else ""),
                      fontsize=12)
        ax2.set_xlabel(f"sigma {x_label}", fontsize=10)

    # ---- panel 3: the sample behind each level --------------------------------
    # each bar as thick as its own level: the minimum spacing made every
    # bar a hairline as soon as two levels sat close together
    if as_rows or len(y) < 2:
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
        ax3.barh(lo + 0.15 * span, np.asarray(data['n'])[order],
                 height=0.7 * span, align='edge', color='#7f8c8d',
                 edgecolor='none')
    ax3.set_xlim(0, _fit(shared.get('n'), data['n']))
    ax3.set_title("Observations" + (" (matched)" if task['matched'] else ""),
                  fontsize=12)
    ax3.set_xlabel("per level", fontsize=10)
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(
        lambda v, _: f"{v / 1e6:g}M" if v >= 1e6 else
        (f"{v / 1e3:g}k" if v >= 1e3 else f"{v:g}")))

    # ---- shared vertical axis --------------------------------------------------
    for ax in [a for a in (ax1, axb, ax2, ax3) if a is not None]:
        ax.grid(True, ls='--', alpha=0.4)
        ax.tick_params(labelsize=9)
    if as_rows:
        fs = float(np.clip(0.78 * height / max(n_levels, 1) * 72 / 1.35,
                           3.5, 9))
        ax1.set_yticks(y)
        ax1.set_yticklabels([f"{v:g}" for v in lev], fontsize=fs)
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
    head = f"{names[1]} vs {names[0]}" if task['matched'] else names[0]
    sub = (f"{family}  |  {var_name} {units}  |  {task['datestart']} to "
           f"{task['dateend']}\nregion {task['region']}  |  flags "
           f"{task['flag']}  |  {task.get('member_word', 'station')} "
           f"{members_text(task['db_file'], task['id_stn'])}  |  "
           f"{task['land_ocean']}")
    if task.get('special_label') and task['special_label'] != 'all':
        sub += f"  |  method {task['special_label']}"
    if task['matched']:
        tr, tb = counts.get('t', (0, 0))
        fr, fb = counts.get('F', (0, 0))
        sub += (f"\ndots: red = {names[1]} better, blue = {names[0]} better, "
                f"hollow = not significant ({MIN_CONFIDENCE:.0f} %)   |   "
                f"bias: {tr} red, {tb} blue   sigma: {fr} red, {fb} blue")
    if n_thin:
        sub += f"\n{n_thin} level(s) dropped: fewer than {min_obs} observations"
    if n_empty:
        sub += (f"\n{n_empty} level(s) dropped: O-P identical for every "
                f"observation, no departure there (a level the system "
                f"does not use)")
    if task['matched'] and n_flat:
        sub += (f"\n{n_flat} level(s) with no sigma in the control only: "
                f"no ratio there")
    fig.suptitle(f"{head}\n{sub}", fontsize=11, fontweight='bold',
                 y=1.0 - 0.1 / fig_h, va='top')

    out_dir = os.path.join(task['pathwork'], family)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, figure_name(task))
    save_figure(fig, out_file, svg=task.get('svg', False), dpi=DPI)
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
        conf = sigma_confidence(np.square(data['sigma_ctl']),
                                np.square(data['sigma_exp']),
                                data['n'], cov=data.get('cov'))
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
        y_label, invert = 'Channel', True
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
    ax.axvline(1.0, color='black', ls=':', lw=1.4)
    ax.set_xlim(1.0 - half, 1.0 + half)
    ax.set_xlabel(f"sigma_exp / sigma_ctl   ({label}"
                  + (" / B_ref" if gpsro else "") + ")", fontsize=10)
    ax.set_ylabel(y_label, fontsize=11)
    ax.grid(True, ls='--', alpha=0.4)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    if kind == 'channel':
        fs = float(np.clip(0.78 * height / max(n_levels, 1) * 72 / 1.35,
                           3.5, 9))
        ax.set_yticks(np.arange(n_levels))
        ax.set_yticklabels([f"{v:g}" for v in all_lev], fontsize=fs)
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
