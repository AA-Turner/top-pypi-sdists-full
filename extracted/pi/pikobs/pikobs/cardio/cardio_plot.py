#!/usr/bin/python3
"""Figures of pikobs.cardio.

Four synchronised panels per figure: mean departures, sigma, physical
values and counts. Everything is derived from the sums written by the
extraction, so a figure can merge stations or channels exactly.
"""

import json
import math
import os
import random
import re
from datetime import datetime
from typing import Any, Dict, Optional

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

import pikobs
from pikobs.figures import save_figure
from pikobs.configobs.style import (CTL_BETTER, CTL_COLOUR, EXP_BETTER,
                                    EXP_COLOUR, GREY_TEXT)
from pikobs.obsdb import open_result
from pikobs.stats import (MIN_CONFIDENCE, is_significant, moments_from_sums,
                          paired_ttest_confidence, ttest_confidence,
                          sigma_confidence)

ROUGE = '#FF9999'
ROUGEPUR = '#FF0000'
VERT = '#009900'
BLEU = '#1569C7'
NOIR = '#000000'

DPI = 110

# The comparison: the control is drawn with a solid line and the
# experience with a dashed one, so the two are told apart even in black
# and white; a circle marks the cycles where the difference passes the
# test, red when the experience wins and blue when the control does.
CTL_STYLE = '-'
EXP_STYLE = '--'
MARK_SIZE = 130
MARK_ALPHA = 0.35


def _safe(text: Any) -> str:
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


def figure_name(experience, flag, family, id_stn, region, chan, varno,
                land_ocean='all', special='all') -> str:
    """Name of the PNG; the viewer and the plot must agree on it. The land
    filter and the special value are in the name only when there is one,
    so a run without them keeps the names it always had."""
    from pikobs.configobs.special_family import special_label
    land = '' if land_ocean in (None, '', 'all') else f"_{_safe(land_ocean)}"
    # the label of the special value, as every module (IR_channel, 0.5)
    land += ('' if special in (None, '', 'all')
             else f"_{_safe(special_label(family, special))}")
    return (f"serie_{_safe(experience)}_{_safe(flag)}_{_safe(family)}_"
            f"{_safe(id_stn)}_id_stn_{_safe(region)}{land}_ch{_safe(chan)}_"
            f"varno{_safe(varno)}.png")


def parse_flexible_date(date_str: str) -> datetime:
    date_str = str(date_str).strip()
    for fmt in ('%Y%m%d%H', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y%m%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"The date format '{date_str}' is unknown.")


def get_smart_limit(pathwork: str, region: str, family: str, channel: str,
                    panel_id: str, current_data_max: float) -> float:
    """Y limit shared by every figure of a region, so they compare.

    One file per region; a larger limit replaces a smaller one, which keeps
    the panels of different criteria and experiences on the same scale.
    """
    config_file = os.path.join(pathwork, f'y_limits_{_safe(region)}.json')
    limits: Dict[str, Any] = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as fh:
                limits = json.load(fh)
        except (json.JSONDecodeError, IOError):
            limits = {}

    limits.setdefault(family, {})
    chan_key = f"ch_{channel}"
    if not isinstance(limits[family].get(chan_key), dict):
        limits[family][chan_key] = {}

    if current_data_max <= 0 or not np.isfinite(current_data_max):
        calculated = 1.0
    else:
        order = 10 ** int(math.log10(current_data_max))
        step = order / 2 if order >= 10 else 0.1
        calculated = float(math.ceil(current_data_max / step) * step * 1.15)

    existing = limits[family][chan_key].get(panel_id, 0.0)
    if calculated <= existing:
        return existing

    limits[family][chan_key][panel_id] = calculated
    tmp = f"{config_file}.tmp.{os.getpid()}.{random.randint(0, 10000)}"
    try:
        with open(tmp, 'w') as fh:
            json.dump(limits, fh, indent=4)
        os.replace(tmp, config_file)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
    return calculated


def _series(task: Dict[str, Any],
            db_file: Optional[str] = None
            ) -> Optional[Dict[str, np.ndarray]]:
    """Per-cycle statistics of one selection, from the stored sums."""
    db_file = db_file or task['db_file']
    where = ["region = ?", "flag = ?", "land_ocean = ?", "special = ?",
             "varno = ?"]
    args = [task['region'], task['flag_criteria'],
            task.get('land_ocean', 'all'), task.get('special', 'all'),
            task['varno']]
    if str(task['vcoord']) != 'join':
        where.append("Chan = ?")
        args.append(task['vcoord'])
    clause = " AND ".join(where) + task.get('stn_sql', '')

    with open_result(db_file) as conn:
        rows = conn.execute(f"""
            SELECT date, SUM(Nrej), SUM(Nacc), SUM(Nprofile), SUM(Nloc),
                   SUM(n_omp), SUM(s_omp), SUM(s2_omp),
                   SUM(n_oma), SUM(s_oma), SUM(s2_oma),
                   SUM(n_obs), SUM(s_obs), SUM(n_bcorr), SUM(s_bcorr),
                   MIN(min_omp), MAX(max_omp), MIN(min_oma), MAX(max_oma)
            FROM serie_cardio
            WHERE {clause}
            GROUP BY date ORDER BY date;
        """, args).fetchall()
    if not rows:
        return None

    arr = np.array([[r[0]] + [float(v) if v is not None else np.nan
                              for v in r[1:]] for r in rows], dtype=float)

    def mean(n_col, s_col):
        n, s = arr[:, n_col], arr[:, s_col]
        with np.errstate(divide='ignore', invalid='ignore'):
            return np.where(n > 0, s / n, np.nan)

    def std(n_col, s_col, q_col):
        n, s, q = arr[:, n_col], arr[:, s_col], arr[:, q_col]
        with np.errstate(divide='ignore', invalid='ignore'):
            m = np.where(n > 0, s / n, np.nan)
            return np.sqrt(np.maximum(np.where(n > 0, q / n - m * m, np.nan),
                                      0.0))

    return {
        'dates': [str(int(d)) for d in arr[:, 0]],
        'nrej': arr[:, 1], 'nacc': arr[:, 2],
        'nprofile': arr[:, 3], 'nloc': arr[:, 4],
        'ndata': arr[:, 5],
        'avg_omp': mean(5, 6), 'std_omp': std(5, 6, 7),
        'avg_oma': mean(8, 9), 'std_oma': std(8, 9, 10),
        'avg_obs': mean(11, 12),
        'n_bcorr': arr[:, 13], 'avg_bcorr': mean(13, 14),
        'min_omp': arr[:, 15], 'max_omp': arr[:, 16],
        'min_oma': arr[:, 17], 'max_oma': arr[:, 18],
    }


def _align(ref: Dict[str, np.ndarray], exp: Dict[str, np.ndarray]):
    """Keep the cycles both runs have, in order."""
    common = [d for d in exp['dates'] if d in set(ref['dates'])]
    if not common:
        return None, None
    i_ref = [ref['dates'].index(d) for d in common]
    i_exp = [exp['dates'].index(d) for d in common]

    def _take(src, idx):
        out = {'dates': common}
        for k, v in src.items():
            if k == 'dates':
                continue
            out[k] = np.asarray(v)[idx]
        return out

    return _take(ref, i_ref), _take(exp, i_exp)


def _pairs(task, dates) -> Optional[Dict[str, np.ndarray]]:
    """The sums of the matched observations of this selection, per cycle.

    Returns None when the run has no pair database -- an older output, or
    a run without a control -- and the caller falls back on Welch.
    """
    path = task.get('db_pairs')
    if not path or not os.path.isfile(path):
        return None
    where = ["region = ?", "flag = ?", "land_ocean = ?", "special = ?",
             "varno = ?"]
    params = [task['region'], task['flag_criteria'],
              task.get('land_ocean', 'all'), task.get('special', 'all'),
              task['varno']]
    if str(task['vcoord']) != 'join':
        where.append("Chan = ?")
        params.append(task['vcoord'])
    where = " AND ".join(where) + task.get('stn_sql', '')
    try:
        with open_result(path) as conn:
            rows = conn.execute(
                f"SELECT date, "
                f"SUM(n_omp), SUM(sx_omp), SUM(sy_omp), SUM(sxx_omp), "
                f"SUM(syy_omp), SUM(sxy_omp), "
                f"SUM(n_oma), SUM(sx_oma), SUM(sy_oma), SUM(sxx_oma), "
                f"SUM(syy_oma), SUM(sxy_oma) "
                f"FROM pairs_cardio WHERE {where} GROUP BY date;",
                params).fetchall()
    except Exception:
        return None
    if not rows:
        return None
    by_date = {int(r[0]): r[1:] for r in rows}
    out = {}
    for j, tag in enumerate(('omp', 'oma')):
        base = j * 6
        for k, name in enumerate(('n', 'sx', 'sy', 'sxx', 'syy', 'sxy')):
            out[f'{name}_{tag}'] = np.array(
                [float(by_date.get(int(d), [np.nan] * 12)[base + k] or 0.0)
                 for d in dates], dtype=float)
    return out


def _cycle_tests(ref, exp, pairs=None) -> Dict[str, Dict[str, np.ndarray]]:
    """Per cycle, does the change of bias or sigma pass the test?

    The sigma always goes through the F-test. The bias goes through the
    paired t-test when the run matched the observations of the two runs,
    which is what ``pairs`` holds, and through Welch when it did not --
    an older output, or a cycle where the two runs share nothing. The
    paired form sees changes the other cannot: two runs of the same suite
    agree on almost every observation, and pairing removes everything
    they share rather than drowning the change in it.

    Both come from :mod:`pikobs.stats`, so a cycle of cardio and a box of
    scatter answer the same question the same way.
    """
    out: Dict[str, Dict[str, np.ndarray]] = {}
    for metric in ('omp', 'oma'):
        n1, n2 = ref[f'n_{metric}'] if f'n_{metric}' in ref else ref['ndata'], \
            exp[f'n_{metric}'] if f'n_{metric}' in exp else exp['ndata']
        m1, m2 = ref[f'avg_{metric}'], exp[f'avg_{metric}']
        s1, s2 = ref[f'std_{metric}'], exp[f'std_{metric}']
        t_conf = None
        pm_conf = None
        if pairs is not None:
            n = pairs.get(f'n_{metric}')
            if n is not None and np.any(n > 1):
                mx, vx = moments_from_sums(n, pairs[f'sx_{metric}'],
                                           pairs[f'sxx_{metric}'])
                my, vy = moments_from_sums(n, pairs[f'sy_{metric}'],
                                           pairs[f'syy_{metric}'])
                with np.errstate(divide='ignore', invalid='ignore'):
                    cxy = np.where(n > 0,
                                   pairs[f'sxy_{metric}'] / n - mx * my,
                                   np.nan)
                t_conf = paired_ttest_confidence(mx, my, vx, vy, cxy, n)
                pm_conf = sigma_confidence(vx, vy, n, cov=cxy)
                # a cycle with no pair falls back on the cautious test
                gap = ~np.isfinite(t_conf)
                if np.any(gap):
                    welch = ttest_confidence(m1, s1, n1, m2, s2, n2)
                    t_conf = np.where(gap, welch, t_conf)
        if t_conf is None:
            t_conf = ttest_confidence(m1, s1, n1, m2, s2, n2)
        # the sigma: Pitman-Morgan where the cycle has pairs (matched runs
        # are correlated and the F-test misses their changes), the F-test
        # on each run's own moments where it has none -- as the bias does
        f_conf = sigma_confidence(s1 ** 2, s2 ** 2, n1, n2)
        if pm_conf is not None:
            f_conf = np.where(np.isfinite(pm_conf), pm_conf, f_conf)
        out[metric] = {
            # for the bias, better means closer to zero
            'mean': {'conf': t_conf, 'side': np.abs(m2) - np.abs(m1)},
            'std': {'conf': f_conf, 'side': s2 - s1},
        }
    return out


def _mark_significant(ax, x, values, conf, side) -> int:
    """Circle the cycles where the change passes the test."""
    ok = is_significant(conf) & np.isfinite(values) & np.isfinite(side)
    if not np.any(ok):
        return 0
    colours = np.where(side[ok] < 0, EXP_BETTER, CTL_BETTER)
    ax.scatter(np.asarray(x)[ok], np.asarray(values)[ok], s=MARK_SIZE,
               facecolors=colours, edgecolors=colours, alpha=MARK_ALPHA,
               linewidths=1.2, zorder=5)
    return int(np.sum(ok))


def _chan_text(v) -> str:
    """A channel or a level as it is read: 23, not 23.0; join as it is."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    return str(int(f)) if f.is_integer() else f"{f:g}"


def cardio_plot(task: Dict[str, Any]) -> Optional[str]:
    """Draw the cardiogram; returns the path of the PNG.

    With a control in the task, the two runs share every panel: the
    control solid, the experience dashed, and a circle on each cycle
    where the difference passes the test.
    """
    exp = _series(task)
    if exp is None:
        return None
    ref = None
    if task.get('db_control'):
        ref = _series(task, task['db_control'])
        if ref is not None:
            ref, exp = _align(ref, exp)
            if ref is None:
                return None
    pairs = _pairs(task, exp['dates']) if ref is not None else None
    tests = (_cycle_tests(ref, exp, pairs)
             if ref is not None else {})

    pathwork = task['pathwork']
    family, region = task['family'], task['region']
    flag, varno = task['flag_criteria'], task['varno']
    channel, id_stn = task['vcoord'], task['id_stn']
    exp_name = task['experience']
    ctl_name = task.get('control')

    runs = ([(ctl_name, ref, CTL_STYLE)] if ref is not None else []) + \
        [(exp_name, exp, EXP_STYLE if ref is not None else CTL_STYLE)]

    # The colour says which run, the line style which quantity: red the
    # experience and blue the control, in a single run too; O-P and the
    # trial solid, O-A and the analysis dashed. Every figure reads the same.
    def _look(style, colour, dash):
        own = CTL_COLOUR if (ref is not None and style == CTL_STYLE) else EXP_COLOUR
        return dict(linestyle=dash, color=own)

    is_oma = any(np.isfinite(d['avg_oma']).any() for _, d, _ in runs)
    is_bcor = any(np.isfinite(d['avg_bcorr']).any() for _, d, _ in runs)

    fig_size = (15.0, 20.0) if task.get('plot_type') == 'wide' else (10.0, 21.0)
    # the header: title, subtitle, rule, runs, dates, the key, the note
    header_in = 2.75 if tests else 2.45
    fig = plt.figure(figsize=fig_size, facecolor='white')
    n_rows = 6
    # the header carries two lines with a control, so the panels start
    # lower than they would for a single run
    top = 1.0 - header_in / fig_size[1] - 0.100
    axes = [fig.add_axes([0.10, top - i * 0.142, 0.80, 0.100])
            for i in range(n_rows)]
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    variable_name, unit, _ = pikobs.type_varno(f"{varno}")
    x = mdates.date2num([parse_flexible_date(d) for d in exp['dates']])
    xmi = mdates.date2num(parse_flexible_date(task['datestart']))
    xma = mdates.date2num(parse_flexible_date(task['dateend']))
    if xmi == xma:
        xmi, xma = xmi - 0.25, xma + 0.25
    for ax in axes:
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3,
                                                          maxticks=8))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %HZ'))
        ax.set_xlim([xmi, xma])
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.grid(True, linestyle=':', color='grey')

    # ── panel 1: mean departures ──
    for name, d, style in runs:
        bcor = np.nan_to_num(d['avg_bcorr']) if is_bcor else np.zeros_like(
            d['avg_omp'])
        ax1.plot(x, d['avg_omp'], **_look(style, ROUGEPUR, '-'), lw=2,
                 label=f'O-P {name}')
        if is_oma:
            ax1.plot(x, d['avg_oma'], **_look(style, BLEU, '--'), lw=2,
                     label=f'O-A {name}')
        if is_bcor:
            ax1.plot(x, bcor, **_look(style, VERT, ':'), lw=1.5,
                     label=f'bcor {name}')
    n_marks = 0
    if tests:
        n_marks += _mark_significant(ax1, x, exp['avg_omp'],
                                     tests['omp']['mean']['conf'],
                                     tests['omp']['mean']['side'])
        if is_oma:
            n_marks += _mark_significant(ax1, x, exp['avg_oma'],
                                         tests['oma']['mean']['conf'],
                                         tests['oma']['mean']['side'])
    ax1.axhline(0, color=NOIR, lw=1.2, zorder=1)
    ax1.set_ylabel(f'Bias {unit}', fontsize=12)
    ax1.set_title(_summary_line(runs, 'avg', is_oma, is_bcor), fontsize=11,
                  loc='left')

    # ── panel 2: sigma ──
    for name, d, style in runs:
        ax2.plot(x, d['std_omp'], **_look(style, ROUGEPUR, '-'), lw=2,
                 label=f'O-P {name}')
        if is_oma:
            ax2.plot(x, d['std_oma'], **_look(style, BLEU, '--'), lw=2,
                     label=f'O-A {name}')
    if tests:
        n_marks += _mark_significant(ax2, x, exp['std_omp'],
                                     tests['omp']['std']['conf'],
                                     tests['omp']['std']['side'])
        if is_oma:
            n_marks += _mark_significant(ax2, x, exp['std_oma'],
                                         tests['oma']['std']['conf'],
                                         tests['oma']['std']['side'])
    ax2.set_ylabel(f'Sigma {unit}', fontsize=12)
    ax2.set_title(_summary_line(runs, 'std', is_oma, False), fontsize=11,
                  loc='left')

    # ── panel 3: physical values ──
    for name, d, style in runs:
        if name == exp_name:    # the same observations in both runs: once, in black
            ax3.plot(x, d['avg_obs'], color=NOIR, linestyle='-.', lw=1.4,
                     label='observation')
        ax3.plot(x, d['avg_obs'] - d['avg_omp'], **_look(style, ROUGEPUR, '-'),
                 label=f'Trial {name}')
        if is_oma:
            ax3.plot(x, d['avg_obs'] - d['avg_oma'], **_look(style, BLEU, '--'),
                     label=f'Anal {name}')
    ax3.set_ylabel(f'Obsvalue {unit}', fontsize=12)

    # ── panel 4: counts ──
    for name, d, style in runs:
        ax4.plot(x, d['ndata'], **_look(style, NOIR, '-'), label=f'Ndata {name}')
        ax4.plot(x, d['nloc'], **_look(style, '#888888', '--'), lw=1.2,
                 label=f'Nlocs {name}')
    ax4.set_ylabel('Observations', fontsize=12)
    # no legend on the curves: a title line, as the extremes have
    ax4.set_title('Ndata (solid): observations  \u00b7  Nlocs (dashed): locations',
                  fontsize=10, loc='left', color='#555555')

    # ── panels 5 and 6: the extremes of each cycle ──
    for ax, metric, colour in ((ax5, 'omp', ROUGEPUR), (ax6, 'oma', BLEU)):
        drawn = False
        for name, d, style in runs:
            lo, hi = d[f'min_{metric}'], d[f'max_{metric}']
            if not (np.isfinite(lo).any() or np.isfinite(hi).any()):
                continue
            drawn = True
            dash = '-' if metric == 'omp' else '--'
            ax.plot(x, hi, **_look(style, colour, dash), lw=1.6, label=f'max {name}')
            ax.plot(x, lo, **_look(style, colour, dash), lw=1.6, alpha=0.65,
                    label=f'min {name}')
            if style == CTL_STYLE:
                ax.fill_between(x, lo, hi, alpha=0.10,
                                color=_look(style, colour, dash)['color'])
        ax.axhline(0, color=NOIR, lw=1.0, zorder=1)
        what = 'O-P' if metric == 'omp' else 'O-A'
        ax.set_ylabel(f'{what} range {unit}', fontsize=12)
        if not drawn:
            ax.text(0.5, 0.5, f'no {metric.upper()} in this selection',
                    transform=ax.transAxes, ha='center', va='center',
                    color='#999999', fontsize=11)
        ax.set_title(f'Extremes of {what} per cycle: one value far '
                     f'from the rest is usually a bad observation',
                     fontsize=10, loc='left', color='#555555')

    fig.autofmt_xdate()

    # the header, as in scatter and zone: the variable, a grey line with
    # what the figure holds, a light rule, the runs in their colours, the
    # dates, one key for every panel, the note of the circles small
    from matplotlib.lines import Line2D

    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    def _y(inch: float) -> float:
        return 1.0 - inch / fig_size[1]

    land = task.get('land_ocean', 'all')
    sp = task.get('special_label', 'all')
    try:
        is_channel = str(pikobs.family(family)[5]).upper() == 'CANAL'
    except Exception:
        is_channel = False
    word = 'channel' if is_channel else 'level'
    parts = [family,
             region if land in (None, '', 'all') else f"{region} ({land})",
             f"flag {flag}", f"station {id_stn}",
             f"all {word}s" if str(channel) == 'join'
             else f"{word} {_chan_text(channel)}"]
    if sp not in (None, '', 'all'):
        parts.append(f"method {sp}")
    x0 = 0.10
    fig.text(0.5, _y(0.18), f"{variable_name} {unit}", ha='center', va='top',
             fontsize=15, fontweight='bold', color='#1F2933')
    fig.text(0.5, _y(0.52), "  ·  ".join(parts), ha='center', va='top',
             fontsize=11, color=GREY_TEXT)
    fig.add_artist(Line2D([x0, 0.90], [_y(0.80)] * 2, color='#c8c8c8',
                          linewidth=0.9, transform=fig.transFigure))
    y_in = 0.92
    who = ([("Exp", exp_name, EXP_COLOUR), ("Ctl", ctl_name, CTL_COLOUR)]
           if ref is not None else [("Exp", exp_name, EXP_COLOUR)])
    for label, name, colour in who:
        fig.text(x0, _y(y_in), f"{label}  {name}", ha='left', va='top',
                 fontsize=12, fontweight='bold', color=colour)
        y_in += 0.25
    fig.text(x0, _y(y_in), f"{_when(task['datestart'])}  to  "
             f"{_when(task['dateend'])}", ha='left', va='top', fontsize=10,
             color=GREY_TEXT)
    y_in += 0.24
    # one key for every panel: the colour says the run, the line the quantity
    key = [Line2D([], [], color='#444444', ls='-', lw=2, label='O-P, trial, Ndata'),
           Line2D([], [], color='#444444', ls='--', lw=2, label='O-A, analysis, Nlocs'),
           Line2D([], [], color=NOIR, ls='-.', lw=1.4, label='observation')]
    if is_bcor:
        key.append(Line2D([], [], color='#444444', ls=':', lw=1.5,
                          label='bias correction'))
    if tests:
        key.append(Line2D([], [], color='#888888', ls='', marker='o',
                          markersize=9, alpha=0.4,
                          label=f'change above {MIN_CONFIDENCE:.0f} %'))
    fig.legend(handles=key, loc='upper left', ncol=len(key), frameon=False,
               fontsize=10, handlelength=3, borderaxespad=0,
               bbox_to_anchor=(x0 - 0.008, _y(y_in)))
    y_in += 0.30
    if tests:
        fig.text(x0, _y(y_in), f"circles: a change above {MIN_CONFIDENCE:.0f} % "
                 f"confidence, red where Exp is better, blue where Ctl is  "
                 f"({n_marks} in this figure)", ha='left', va='top',
                 fontsize=9.5, color=GREY_TEXT)

    out_dir = os.path.join(pathwork, family)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, figure_name(
        exp_name, flag, family, task.get('stn_tag', id_stn), region, channel,
        varno, task.get('land_ocean', 'all'), task.get('special_label', 'all')))
    save_figure(fig, out_file, svg=task.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out_file


def _summary_line(runs, kind: str, is_oma: bool, is_bcor: bool) -> str:
    """The numbers of the whole period, one run after the other."""
    bits = []
    for name, d, style in runs:
        who = 'Ctl' if (len(runs) > 1 and style == CTL_STYLE) else 'Exp'
        n = d['ndata']
        tot = np.nansum(n) or 1.0

        def _w(values):
            return float(np.nansum(np.where(np.isfinite(values), values, 0.0)
                                   * n) / tot)

        if kind == 'avg':
            part = f"{who}: O-P {_w(d['avg_omp']):.3f}"
            if is_oma:
                part += f"  O-A {_w(d['avg_oma']):.3f}"
            if is_bcor:
                part += f"  bcor {_w(d['avg_bcorr']):.3f}"
        else:
            part = f"{who}: sigma O-P {_w(d['std_omp']):.3f}"
            if is_oma:
                part += f"  O-A {_w(d['std_oma']):.3f}"
        bits.append(part)
    return "   |   ".join(bits)
