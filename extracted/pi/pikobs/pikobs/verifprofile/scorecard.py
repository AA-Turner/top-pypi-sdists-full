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
pairs. A cell is tested on its cycles: the change of every cycle, and a
cycle block bootstrap of their mean (pikobs.stats.cycle_bootstrap_confidence),
from 20 cycles on. A CSV beside each figure holds the numbers, with the
t-test on the cycles (cycle_confidence) beside the bootstrap.
"""
import csv
import math
import os
import textwrap
from typing import Any, Dict, List, Optional, Tuple

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt                                  # noqa: E402
from matplotlib.patches import Rectangle                         # noqa: E402
import numpy as np                                               # noqa: E402

import pikobs                                                    # noqa: E402
from pikobs.figures import match_badge, save_figure              # noqa: E402
from pikobs.stats import (MIN_CONFIDENCE, cycle_bootstrap_confidence,  # noqa: E402
                          cycle_confidence, is_significant, sigma_confidence,
                          ttest_confidence)
from pikobs.obsdb import open_result                                # noqa: E402
from pikobs.stats.stats import BOOT_MIN_CYCLES                     # noqa: E402
from pikobs.configobs.style import (CTL_BETTER, CTL_COLOUR, DPI,  # noqa: E402
                                    EXP_BETTER, EXP_COLOUR, GREY_TEXT, font_size)
from pikobs.verifprofile.verifprofile_plot import (       # noqa: E402
    MIN_PAIRS_PER_CYCLE, _safe, _where, cycle_level_sums as _sums)

# the layers, in km; the pressure under them is that of a standard
# atmosphere, p = 1013.25 exp(-z / 7 km)
BANDS_KM = [(0, 2), (2, 5), (5, 10), (10, 15), (15, 20), (20, 30), (30, 40),
            (40, 60)]
SCALE_HEIGHT_KM = 7.0
MIN_OBS_PER_CELL = 30
# a cycle enters the test of a cell with at least this many pairs
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


def _cells(task, vcotyp: str) -> Optional[List[Optional[Dict[str, float]]]]:
    """One cell per layer: the change over the whole period, and its two
    confidences on the cycles -- the change of every cycle, and whether its
    mean over the cycles is away from zero: the cycle block bootstrap
    (t_conf, f_conf), and the t-test on the cycles beside it in the CSV."""
    arr = _sums(task)
    if arr is None:
        return None
    z = _height_km(arr[:, 1], vcotyp)
    if z is None:
        return None
    dates = np.unique(arr[:, 0])
    out = []
    for b, (lo, hi) in enumerate(BANDS_KM):
        # a layer holds its top edge (the first one its bottom too): a level
        # rounded onto an edge -- GPS-RO at 39.5-40 km reads 40 -- belongs
        # to the layer it came from, not to the empty one above
        sel = (((z > lo) | ((b == 0) & (z >= lo))) & (z <= hi)
               & np.isfinite(arr[:, 2:]).all(axis=1))
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
                    # the test of the figure: the cycle block bootstrap
                    't_conf': cycle_bootstrap_confidence((np.abs(kme) - np.abs(kmc)) / sc),
                    'f_conf': cycle_bootstrap_confidence(100.0 * (kse - ksc) / sc),
                    # the t-test on the cycles, beside it in the CSV
                    't_conf_cycle_t': cycle_confidence((np.abs(kme) - np.abs(kmc)) / sc),
                    'f_conf_cycle_t': cycle_confidence(100.0 * (kse - ksc) / sc),
                    'cycles': int(len(k))})
    return out if any(c is not None for c in out) else None


def _run_level_sums(task, db_file) -> Optional[np.ndarray]:
    """(level, n, sum, sum of squares, cycles) of one run, every level, over
    the whole period: the single-run table, as the MATCH off figures read it."""
    fn = task['function']
    if fn not in ('omp', 'oma'):
        return None
    where, args = _where(task)
    with open_result(db_file) as conn:
        rows = conn.execute(f"""
            SELECT vcoord, SUM(n_{fn}), SUM(s_{fn}), SUM(s2_{fn}), COUNT(DISTINCT date)
            FROM zone WHERE {where} GROUP BY vcoord;""", args).fetchall()
    rows = [r for r in rows if r[0] is not None and r[1]]
    return np.array([[float(v or 0.0) for v in r] for r in rows]) if rows else None


def _cells_off(task, vcotyp: str) -> Optional[List[Optional[Dict[str, float]]]]:
    """One cell per layer, MATCH off: every observation of each run, the
    t-test on the bias and the F-test on the sigma, as the MATCH off
    figures. A layer holds its top edge, as in _cells."""
    runs = []
    for db in (task.get('db_ctl'), task.get('db_file')):
        arr = _run_level_sums(task, db) if db else None
        if arr is None:
            return None
        z = _height_km(arr[:, 0], vcotyp)
        if z is None:
            return None
        runs.append((arr, z))
    out = []
    for b, (lo, hi) in enumerate(BANDS_KM):
        stats = []
        for arr, z in runs:
            sel = ((z > lo) | ((b == 0) & (z >= lo))) & (z <= hi)
            n, sm, s2 = arr[sel, 1].sum(), arr[sel, 2].sum(), arr[sel, 3].sum()
            stats.append((n, sm, s2, int(arr[sel, 4].max()) if sel.any() else 0))
        (nc, smc, s2c, cyc), (ne, sme, s2e, _) = stats
        if nc < MIN_OBS_PER_CELL or ne < MIN_OBS_PER_CELL:
            out.append(None)
            continue
        mc, me = smc / nc, sme / ne
        vc, ve = max(s2c / nc - mc * mc, 0.0), max(s2e / ne - me * me, 0.0)
        if vc <= 0:
            out.append(None)
            continue
        sc, se = math.sqrt(vc), math.sqrt(ve)
        out.append({'n': nc, 'mean_ctl': mc, 'mean_exp': me, 'sigma_ctl': sc,
                    'sigma_exp': se, 'd_sigma': 100.0 * (se - sc) / sc,
                    'd_bias': abs(me) - abs(mc), 'rel_bias': (abs(me) - abs(mc)) / sc,
                    't_conf': float(ttest_confidence(np.array([mc]), np.array([sc]), np.array([nc]),
                                                     np.array([me]), np.array([se]), np.array([ne]))[0]),
                    'f_conf': float(sigma_confidence(np.array([vc]), np.array([ve]),
                                                     np.array([nc]), np.array([ne]))[0]),
                    't_conf_cycle_t': float('nan'), 'f_conf_cycle_t': float('nan'),
                    'cycles': cyc})
    return out if any(c is not None for c in out) else None


def _colour(change: float, conf: float, scale: float, minimum: float):
    """(face, alpha, text colour, bold) of a cell: coloured when the test
    passes and the change is at least the minimum, grey otherwise."""
    if not bool(is_significant(np.array([conf]))[0]) or abs(change) < minimum:
        return '#D1D5DB', 0.35, '#6B7280', False
    alpha = min(0.30 + abs(change) / scale, 0.90)
    face = EXP_BETTER if change < 0 else CTL_BETTER
    return face, alpha, ('white' if alpha > 0.55 else '#1F2933'), True


def _table(ax, rows, key, conf_key, scale, fmt, minimum, bands):
    """One table: a row per (family, variable, region), a column per layer
    of ``bands`` (the indices of BANDS_KM some row reaches)."""
    n_rows = len(rows)
    for i, (_, cells) in enumerate(rows):
        y = n_rows - 1 - i
        for j, c in enumerate(cells[b] for b in bands):
            if c is None:
                ax.add_patch(Rectangle((j, y), 1, 1, fc='white', ec='#E5E7EB',
                                       lw=0.8))
                continue
            face, alpha, tc, bold = _colour(c[key], c[conf_key], scale, minimum)
            ax.add_patch(Rectangle((j, y), 1, 1, fc=face, alpha=alpha,
                                   ec='white', lw=2.5))
            ax.text(j + 0.5, y + 0.5, fmt(c[key]), ha='center', va='center',
                    fontsize=font_size('cell'), color=tc,
                    fontweight='bold' if bold else 'normal')
    ax.set_xlim(0, len(bands))
    ax.set_ylim(0, n_rows)
    ax.set_xticks([])
    ax.set_yticks([])
    # the layers over the columns: the km, and the pressure under it, smaller;
    # the units are written once, left of the first table
    for j, b in enumerate(bands):
        lo, hi = BANDS_KM[b]
        ax.text(j + 0.5, n_rows + 0.62, f"{lo}-{hi}", ha='center', va='bottom',
                fontsize=font_size('column'), color='#1F2933')
        ax.text(j + 0.5, n_rows + 0.12, f"{_p(_hpa(lo))}-{_p(_hpa(hi))}",
                ha='center', va='bottom', fontsize=0.7 * font_size('column'),
                color=GREY_TEXT)
    for side in ax.spines.values():
        side.set_visible(False)


def _figure(group, rows, out_png, family: Optional[str] = None) -> str:
    """One scorecard: the sigma on the left, the bias on the right; every
    family of the comparison, or one (``family``), sized to be read on a
    slide. The sizes are in inches from the top, so the header and the
    tables keep their room whatever the number of rows."""
    t0 = group['task']
    ctl, exp = t0['names']
    fn = {'omp': 'O-P', 'oma': 'O-A'}.get(t0['function'], t0['function'])
    head_in, cols_in, row_in, foot_in = 3.3, 1.75, 0.75, 0.3
    fig_w = 26.0
    fig_h = head_in + cols_in + row_in * len(rows) + foot_in
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor='white')

    def at(inch):
        return 1 - inch / fig_h

    body = [foot_in / fig_h, row_in * len(rows) / fig_h]
    # only the layers some row reaches: a family's own scorecard has no
    # empty column of layers it never gets to
    bands = [b for b in range(len(BANDS_KM)) if any(c[b] is not None for _, c in rows)]
    ax_s = fig.add_axes([0.265, body[0], 0.355, body[1]])
    ax_b = fig.add_axes([0.640, body[0], 0.355, body[1]])
    _table(ax_s, rows, 'd_sigma', 'f_conf', 3.0, lambda v: f"{v:+.1f}",
           MIN_CHANGE_PCT, bands)
    _table(ax_b, rows, 'rel_bias', 't_conf', 0.10, lambda v: f"{100 * v:+.1f}",
           MIN_CHANGE_PCT / 100.0, bands)
    for ax, title in ((ax_s, f"sigma of {fn}: (Exp - Ctl) / Ctl  [%]"),
                      (ax_b, f"|bias| of {fn}, in % of sigma Ctl")):
        ax.text(len(bands) / 2, len(rows) + 1.45, title, ha='center',
                va='bottom', fontsize=font_size('table_title'), fontweight='bold',
                color='#30343A', transform=ax.transData)
    # the row labels: the region on the right, the variable once per block
    n_rows = len(rows)
    lab_tr = mpl.transforms.blended_transform_factory(fig.transFigure, ax_s.transData)
    fig.text(0.258, n_rows + 0.62, "km", transform=lab_tr, ha='right', va='bottom',
             fontsize=font_size('column'), color='#1F2933')
    fig.text(0.258, n_rows + 0.12, "hPa", transform=lab_tr, ha='right', va='bottom',
             fontsize=0.7 * font_size('column'), color=GREY_TEXT)
    prev = None
    for i, (lab, _) in enumerate(rows):
        y = n_rows - i
        fig.text(0.258, y - 0.5, lab[2], transform=lab_tr, ha='right', va='center',
                 fontsize=font_size('row'), color='#1F2933')
        if lab[:2] != prev:
            for ax in (ax_s, ax_b):
                ax.axhline(y, color='#6B7280', lw=2.0, clip_on=False)
            name = lab[1] if family else f"{lab[0]}  {lab[1]}"
            fig.text(0.008, y - 0.15, "\n".join(textwrap.wrap(name, 18)),
                     transform=lab_tr, ha='left', va='top', linespacing=1.15,
                     fontsize=font_size('block'), fontweight='bold', color='#1F2933')
            prev = lab[:2]

    def _when(s):
        s = str(s)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"
    title = f"Scorecard  \u00b7  {fn}, Exp against Ctl, by layers of height"
    if family:
        title += f"  \u00b7  {family}"
    fig.text(0.012, at(0.15), title, fontsize=font_size('title'), fontweight='bold',
             color='#1F2933', va='top')
    parts = [f"{_when(t0['datestart'])} to {_when(t0['dateend'])}", f"flag {t0['flag']}",
             "all stations"]
    if t0.get('land_ocean', 'all') != 'all':
        parts.append(t0['land_ocean'])
    fig.text(0.012, at(0.85), "  \u00b7  ".join(parts), fontsize=font_size('note'),
             color=GREY_TEXT, va='top')
    t = fig.text(0.012, at(1.45), f"Ctl  {ctl}", fontsize=font_size('names'),
                 fontweight='bold', color=CTL_COLOUR, va='top')
    box = t.get_window_extent(renderer=fig.canvas.get_renderer())
    x = fig.transFigure.inverted().transform((box.x1, box.y0))[0] + 0.02
    fig.text(x, at(1.45), f"Exp  {exp}", fontsize=font_size('names'),
             fontweight='bold', color=EXP_COLOUR, va='top')
    fig.text(0.012, at(2.15), "red: Exp better  \u00b7  blue: Exp worse  \u00b7  "
             "grey: no clear change", fontsize=font_size('note'), color='#30343A',
             va='top')
    fig.text(0.012, at(2.7), f"grey also below {MIN_CHANGE_PCT:g} %; empty: the family "
             f"does not reach the layer, or fewer than {MIN_OBS_PER_CELL} observations; "
             + (f"tested from {BOOT_MIN_CYCLES} cycles" if not t0.get('compare_off') else
              "MATCH off: every observation of each run, t-test and F-test"), fontsize=0.8 * font_size('note'),
             color=GREY_TEXT, va='top')
    match_badge(fig, not t0.get('compare_off'), top_in=0.15,
                method=("t-test and F-test, 95 %" if t0.get('compare_off') else None))
    fig.add_artist(mpl.lines.Line2D([0.012, 0.993], [at(head_in - 0.12)] * 2,
                                    transform=fig.transFigure, color='#D9DDE2', lw=1.5))
    save_figure(fig, out_png, svg=t0.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out_png


def make_scorecards(plot_tasks: List[Dict[str, Any]], pathwork: str
                    ) -> Tuple[List[Dict[str, Any]], List[Optional[str]]]:
    """The scorecards of the matched figures pooled over every station
    (id_stn join): one per experience, function, criterion and surface.
    Only the families observed in profiles -- pressure or height levels: a
    family of channels (radiances) has no layers to score.
    Returns (tasks, figure paths) for the viewer."""
    groups: Dict[tuple, Dict[str, Any]] = {}
    for t in plot_tasks:
        off = bool(t.get('compare_off')) and t.get('match_mode') == 'off'
        if not (t.get('matched') or off) or str(t.get('id_stn')) != 'join' \
                or 'members' in t or str(t.get('special', 'all')) != 'all':
            continue
        if 'CANAL' in str(pikobs.family(t['family'])[5]).upper():
            continue                                  # channels: no layers
        key = (tuple(t['names']), t['function'], t['flag'], t['land_ocean'], 'off' if off else 'on')
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
            cells = _cells_off(t, vcotyp) if t.get('compare_off') else _cells(t, vcotyp)
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
                f"{t0['function']}_{_safe(t0['flag'])}_{_safe(t0['land_ocean'])}"
                f"{'_matchoff' if t0.get('compare_off') else ''}")
        png = _figure(g, rows, os.path.join(out_dir, stem + ".png"))
        with open(os.path.join(out_dir, stem + ".csv"), "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["control", "experience", "function", "flag", "family",
                         "variable", "region", "layer_km", "n", "sigma_ctl",
                         "sigma_exp", "sigma_change_pct", "sigma_conf",
                         "bias_ctl", "bias_exp", "abs_bias_change", "bias_conf",
                         "cycles", "sigma_conf_cycle_t", "bias_conf_cycle_t"])
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
                                 f"{c['t_conf']:.1f}", c['cycles'],
                                 f"{c['f_conf_cycle_t']:.1f}", f"{c['t_conf_cycle_t']:.1f}"])
            # the two tests on the cycles, cell by cell: where they agree
            n_cell = agree = sig_t = sig_b = 0
            for _, cells in rows:
                for c in cells:
                    if c is None:
                        continue
                    for a, b in ((c['t_conf_cycle_t'], c['t_conf']), (c['f_conf_cycle_t'], c['f_conf'])):
                        if not (np.isfinite(a) and np.isfinite(b)):
                            continue
                        ta, tb = a >= MIN_CONFIDENCE, b >= MIN_CONFIDENCE
                        n_cell += 1; agree += ta == tb; sig_t += ta; sig_b += tb
            if n_cell:
                print(f"[scorecard] {stem}: of {n_cell} tests (bias and sigma, every cell), "
                      f"cycle block bootstrap (the figure) {sig_b} significant, t-test on the cycles {sig_t}; "
                      f"they agree on {agree} ({100.0 * agree / n_cell:.0f} %)", flush=True)
        # it holds every region, variable, station and special value: "*"
        tasks.append(dict(t0, family='scorecard', region='*', varno='*',
                          id_stn='*', special_label='*'))
        results.append(png)
        # and one per family, each the size of a slide, in a folder named
        # as its family in the viewer (scorecard_ua ...): the viewer finds an
        # image in the folder of its family
        for fam in dict.fromkeys(lab[0] for lab, _ in rows):
            rows_f = [r for r in rows if r[0][0] == fam]
            name = f"scorecard_{_safe(fam)}"
            fam_dir = os.path.join(pathwork, name)
            os.makedirs(fam_dir, exist_ok=True)
            png_f = _figure(g, rows_f, os.path.join(fam_dir, f"{stem}_{_safe(fam)}.png"),
                            family=fam)
            tasks.append(dict(t0, family=name, region='*', varno='*',
                              id_stn='*', special_label='*'))
            results.append(png_f)
    return tasks, results
