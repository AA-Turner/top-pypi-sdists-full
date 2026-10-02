"""The scorecard of a comparison: where the experience is better or worse,
by layers of height.

One figure per experience, function and criterion: a row for every family,
variable and region of the comparison, a column for every layer of height,
and in every cell the change of the experience against the control --
the sigma in percent on the left, the bias on the right. Red where the
experience is better and the test passes, blue where it is worse, grey
where the change is not larger than noise, empty where the family does not
reach that layer.

The layers are the same for every family -- in km, with the pressure of a
standard atmosphere under them -- so radiosondes (pressure), GPS-RO
(height) and MLS (pressure, up to 0.02 hPa) share one table, and two
scorecards compare with each other. A layer pools its levels exactly: the
counts, the sums, the sums of squares and of products of the matched
pairs, then the same tests as the figures (paired t-test on the mean,
Pitman-Morgan on sigma). A CSV beside each figure holds the numbers.
"""
import csv
import math
import os
from typing import Any, Dict, List, Optional, Tuple

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt                                  # noqa: E402
from matplotlib.patches import Rectangle                         # noqa: E402
import numpy as np                                               # noqa: E402

import pikobs                                                    # noqa: E402
from pikobs.figures import save_figure                           # noqa: E402
from pikobs.obsdb import open_result                             # noqa: E402
from pikobs.stats import (MIN_CONFIDENCE, cycle_confidence,      # noqa: E402
                          is_significant)
from pikobs.configobs.style import (CTL_BETTER, CTL_COLOUR, DPI,  # noqa: E402
                                    EXP_BETTER, EXP_COLOUR)
from pikobs.verifprofile.verifprofile_plot import (_PAIR_N,      # noqa: E402
                                                   _PAIR_SUMS, _safe,
                                                   _where)

# the layers, in km; the pressure under them is that of a standard
# atmosphere, p = 1013.25 exp(-z / 7 km)
BANDS_KM = [(0, 2), (2, 5), (5, 10), (10, 15), (15, 20), (20, 30), (30, 40),
            (40, 60)]
SCALE_HEIGHT_KM = 7.0
MIN_OBS_PER_CELL = 30
# a cycle enters the test of a cell with at least this many pairs
MIN_PAIRS_PER_CYCLE = 10
# a cell is coloured only when its test passes AND the change reaches this,
# in percent: with a summer of observations the tests call 0.1 % real
MIN_CHANGE_PCT = 0.5


def _hpa(z_km: float) -> float:
    return 1013.25 * math.exp(-z_km / SCALE_HEIGHT_KM)


def _p(value: float) -> str:
    """A pressure as one reads it: 1013, 58, 13.9, 3.3, 0.19."""
    if value >= 100:
        return f"{value:.0f}"
    if value >= 10:
        return f"{value:.0f}" if value >= 20 else f"{value:.1f}"
    if value >= 1:
        return f"{value:.1f}"
    return f"{value:.2g}"


def _height_km(lev: np.ndarray, vcotyp: str) -> Optional[np.ndarray]:
    """The height of each level in km, or None when the vertical axis is not
    a height (channels)."""
    kind = str(vcotyp).strip().upper()
    if kind.startswith('PRESSION'):
        p = np.asarray(lev, float)
        with np.errstate(divide='ignore', invalid='ignore'):
            return -SCALE_HEIGHT_KM * np.log(p / 101325.0)
    if kind.startswith('HAUTEUR'):
        return np.asarray(lev, float) / 1000.0
    return None


def _sums(task) -> Optional[np.ndarray]:
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


def _cells(task, vcotyp: str) -> Optional[List[Optional[Dict[str, float]]]]:
    """One cell per layer: the change over the whole period, and its two
    confidences on the cycles -- the change of every cycle, and whether its
    mean over the cycles is away from zero (cycle_confidence)."""
    arr = _sums(task)
    if arr is None:
        return None
    z = _height_km(arr[:, 1], vcotyp)
    if z is None:
        return None
    dates = np.unique(arr[:, 0])
    out = []
    for lo, hi in BANDS_KM:
        sel = (z >= lo) & (z < hi) & np.isfinite(arr[:, 2:]).all(axis=1)
        if not sel.any():
            out.append(None)
            continue
        # the sums of the layer, cycle by cycle: n, C, C2, E, E2, CE
        per = np.zeros((len(dates), 6))
        np.add.at(per, np.searchsorted(dates, arr[sel, 0]), arr[sel, 2:8])
        n, c, c2, e, e2, ce = per.sum(axis=0)
        if n < MIN_OBS_PER_CELL:
            out.append(None)
            continue
        mc, me = c / n, e / n
        vc, ve = max(c2 / n - mc * mc, 0.0), max(e2 / n - me * me, 0.0)
        if vc <= 0:
            out.append(None)
            continue
        sc, se = math.sqrt(vc), math.sqrt(ve)
        # the change of each cycle that holds a few pairs, in units of the
        # sigma of the control over the period
        k = per[per[:, 0] >= MIN_PAIRS_PER_CYCLE]
        with np.errstate(divide='ignore', invalid='ignore'):
            kmc, kme = k[:, 1] / k[:, 0], k[:, 3] / k[:, 0]
            ksc = np.sqrt(np.maximum(k[:, 2] / k[:, 0] - kmc * kmc, 0.0))
            kse = np.sqrt(np.maximum(k[:, 4] / k[:, 0] - kme * kme, 0.0))
        out.append({'n': n, 'mean_ctl': mc, 'mean_exp': me, 'sigma_ctl': sc,
                    'sigma_exp': se, 'd_sigma': 100.0 * (se - sc) / sc,
                    'd_bias': abs(me) - abs(mc),
                    'rel_bias': (abs(me) - abs(mc)) / sc,
                    't_conf': cycle_confidence((np.abs(kme) - np.abs(kmc)) / sc),
                    'f_conf': cycle_confidence(100.0 * (kse - ksc) / sc),
                    'cycles': int(len(k))})
    return out if any(c is not None for c in out) else None


def _colour(change: float, conf: float, scale: float, minimum: float):
    """(face, alpha, text colour, bold) of a cell: coloured when the test
    passes and the change is at least the minimum, grey otherwise."""
    if not bool(is_significant(np.array([conf]))[0]) or abs(change) < minimum:
        return '#D1D5DB', 0.35, '#6B7280', False
    alpha = min(0.30 + abs(change) / scale, 0.90)
    face = EXP_BETTER if change < 0 else CTL_BETTER
    return face, alpha, ('white' if alpha > 0.55 else '#1F2933'), True


def _table(ax, rows, key, conf_key, scale, fmt, minimum):
    n_rows = len(rows)
    for i, (_, cells) in enumerate(rows):
        y = n_rows - 1 - i
        for j, c in enumerate(cells):
            if c is None:
                ax.add_patch(Rectangle((j, y), 1, 1, fc='white', ec='#E5E7EB',
                                       lw=0.8))
                continue
            face, alpha, tc, bold = _colour(c[key], c[conf_key], scale, minimum)
            ax.add_patch(Rectangle((j, y), 1, 1, fc=face, alpha=alpha,
                                   ec='white', lw=1.5))
            ax.text(j + 0.5, y + 0.5, fmt(c[key]), ha='center', va='center',
                    fontsize=9.5, color=tc,
                    fontweight='bold' if bold else 'normal')
    ax.set_xlim(0, len(BANDS_KM))
    ax.set_ylim(0, n_rows)
    ax.set_xticks(np.arange(len(BANDS_KM)) + 0.5)
    ax.set_xticklabels([f"{lo}-{hi} km\n{_p(_hpa(lo))}-{_p(_hpa(hi))} hPa"
                        for lo, hi in BANDS_KM], fontsize=8.8)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)


def _figure(group, rows, out_png) -> str:
    """One scorecard: the sigma on the left, the bias on the right."""
    t0 = group['task']
    ctl, exp = t0['names']
    fn = {'omp': 'O-P', 'oma': 'O-A'}.get(t0['function'], t0['function'])
    fig_h = 3.3 + 0.36 * len(rows)
    fig = plt.figure(figsize=(24, fig_h), facecolor='white')
    top = 1 - 2.75 / fig_h           # the tables below the header, with air
    ax_s = fig.add_axes([0.19, 0.03, 0.375, top - 0.03])
    ax_b = fig.add_axes([0.605, 0.03, 0.375, top - 0.03])
    _table(ax_s, rows, 'd_sigma', 'f_conf', 3.0, lambda v: f"{v:+.1f}",
           MIN_CHANGE_PCT)
    _table(ax_b, rows, 'rel_bias', 't_conf', 0.10, lambda v: f"{100 * v:+.1f}",
           MIN_CHANGE_PCT / 100.0)
    ax_s.set_title(f"sigma of {fn}: 100 x (Exp - Ctl) / Ctl  [%]",
                   fontsize=11.5, pad=34, color='#30343A')
    ax_b.set_title(f"|bias| of {fn}: (|Exp| - |Ctl|) / sigma Ctl  [%]",
                   fontsize=11.5, pad=34, color='#30343A')
    # the row labels: the region, and the family and variable once per block
    n_rows = len(rows)
    ax_s.set_yticks(np.arange(n_rows) + 0.5)
    ax_s.set_yticklabels([lab[2] for lab, _ in rows][::-1], fontsize=9.5)
    ax_b.set_yticks([])
    prev = None
    for i, (lab, _) in enumerate(rows):
        if lab[:2] != prev:
            y = n_rows - i
            for ax in (ax_s, ax_b):
                ax.axhline(y, color='#6B7280', lw=1.1)
            # the family and the variable, from the left edge of the figure
            ax_s.text(0.012, y - 0.1, f"{lab[0]}  {lab[1]}",
                      transform=mpl.transforms.blended_transform_factory(
                          fig.transFigure, ax_s.transData),
                      ha='left', va='top', fontsize=10.5, fontweight='bold',
                      color='#1F2933')
            prev = lab[:2]

    def at(inch):
        return 1 - inch / fig_h

    def _when(s):
        s = str(s)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"
    grey = '#5F6B76'
    fig.text(0.02, at(0.12), f"Scorecard  \u00b7  {fn}, change of Exp against "
             f"Ctl, by layers of height", fontsize=15, fontweight='bold',
             color='#1F2933', va='top')
    fig.text(0.985, at(0.14), f"{_when(t0['datestart'])}  to  "
             f"{_when(t0['dateend'])}", ha='right', va='top', fontsize=10.5,
             color=grey)
    parts = [f"flag {t0['flag']}", "all stations"]
    if t0.get('land_ocean', 'all') != 'all':
        parts.append(t0['land_ocean'])
    fig.text(0.02, at(0.44), "  \u00b7  ".join(parts), fontsize=11, color=grey,
             va='top')
    t = fig.text(0.02, at(0.70), f"Ctl  {ctl}", fontsize=13, fontweight='bold',
                 color=CTL_COLOUR, va='top')
    box = t.get_window_extent(renderer=fig.canvas.get_renderer())
    x = fig.transFigure.inverted().transform((box.x1, box.y0))[0] + 0.015
    fig.text(x, at(0.70), f"Exp  {exp}", fontsize=13, fontweight='bold',
             color=EXP_COLOUR, va='top')
    fig.text(0.02, at(0.96), f"red: Exp better, blue: Exp worse, grey: no "
             f"clear change (tested on the cycles, {MIN_CONFIDENCE:.0f} %) "
             f"or less than "
             f"{MIN_CHANGE_PCT:g} %, empty: the family does "
             f"not reach the layer or fewer than {MIN_OBS_PER_CELL} "
             f"observations", fontsize=10.5, color=grey, va='top')
    # MATCH on its own line, as in every module
    fig.text(0.02, at(1.2), "MATCH on: the same observations in both runs, "
             "compared pair by pair", fontsize=10.5, fontweight='semibold',
             color='#30343A', va='top')
    rule = 1.44
    fig.add_artist(mpl.lines.Line2D([0.02, 0.985], [at(rule), at(rule)],
                                    transform=fig.transFigure,
                                    color='#D9DDE2', lw=0.9))
    save_figure(fig, out_png, svg=t0.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out_png


def make_scorecards(plot_tasks: List[Dict[str, Any]], pathwork: str
                    ) -> Tuple[List[Dict[str, Any]], List[Optional[str]]]:
    """The scorecards of the matched figures pooled over every station
    (id_stn join): one per experience, function, criterion and surface.
    Returns (tasks, figure paths) for the viewer."""
    groups: Dict[tuple, Dict[str, Any]] = {}
    for t in plot_tasks:
        if not t.get('matched') or str(t.get('id_stn')) != 'join' \
                or 'members' in t or str(t.get('special', 'all')) != 'all':
            continue
        key = (tuple(t['names']), t['function'], t['flag'], t['land_ocean'])
        g = groups.setdefault(key, {'task': t, 'members': []})
        g['members'].append(t)
    out_dir = os.path.join(pathwork, 'scorecard')
    tasks, results = [], []
    # the families and the regions in the order they were asked for
    fam_order = {f: i for i, f in enumerate(dict.fromkeys(t['family'] for t in plot_tasks))}
    reg_order = {r: i for i, r in enumerate(dict.fromkeys(t['region'] for t in plot_tasks))}
    for key, g in groups.items():
        rows = []
        for t in sorted(g['members'], key=lambda t: (fam_order[t['family']],
                                                     str(t['varno']),
                                                     reg_order[t['region']])):
            vcotyp = pikobs.family(t['family'])[5]
            cells = _cells(t, vcotyp)
            if cells is None:
                continue
            name = pikobs.type_varno(str(t['varno']))[0]
            name = name.split(': ', 1)[-1].lower()
            if 'column' in name:
                # a quantity of the whole column has no height to sit at
                continue
            rows.append(((t['family'], name, t['region']), cells))
        if not rows:
            continue
        os.makedirs(out_dir, exist_ok=True)
        t0 = g['task']
        stem = (f"scorecard_{_safe(t0['names'][1])}_vs_{_safe(t0['names'][0])}_"
                f"{t0['function']}_{_safe(t0['flag'])}_{_safe(t0['land_ocean'])}")
        png = _figure(g, rows, os.path.join(out_dir, stem + ".png"))
        with open(os.path.join(out_dir, stem + ".csv"), "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["control", "experience", "function", "flag", "family",
                         "variable", "region", "layer_km", "n", "sigma_ctl",
                         "sigma_exp", "sigma_change_pct", "sigma_conf",
                         "bias_ctl", "bias_exp", "abs_bias_change", "bias_conf",
                         "cycles"])
            for (fam, var, reg), cells in rows:
                for (lo, hi), c in zip(BANDS_KM, cells):
                    if c is None:
                        continue
                    wr.writerow([t0['names'][0], t0['names'][1], t0['function'],
                                 t0['flag'], fam, var, reg, f"{lo}-{hi}",
                                 int(c['n']), f"{c['sigma_ctl']:.6g}",
                                 f"{c['sigma_exp']:.6g}", f"{c['d_sigma']:.3f}",
                                 f"{c['f_conf']:.1f}", f"{c['mean_ctl']:.6g}",
                                 f"{c['mean_exp']:.6g}", f"{c['d_bias']:.6g}",
                                 f"{c['t_conf']:.1f}", c['cycles']])
        # it holds every region, variable, station and special value: "*"
        tasks.append(dict(t0, family='scorecard', region='*', varno='*',
                          id_stn='*', special_label='*'))
        results.append(png)
    return tasks, results
