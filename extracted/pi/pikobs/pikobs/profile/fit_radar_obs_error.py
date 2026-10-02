#!/usr/bin/python3
"""Fit the radial-velocity observation-error model to profile's table.

    python -m pikobs.profile.fit_radar_obs_error \\
        $PATHWORK/radar/radar_obs_error_calibration.csv \\
        --run experience --region Monde --criteria assimilee

Reads radar_obs_error_calibration.csv, written by pikobs.profile, and for
every radar network (C, U) and every elevation class of the current model
(radar_obs_error.py) fits the same form,

    sigma_o(h) = base + slope dh + accel dh^2,   dh = max(0, h - onset)

by least squares weighted by the number of observations, trying onsets
from 0.5 to 9.5 km and keeping the best. slope and accel are kept >= 0,
so the error never shrinks with height.

The target, --target:
  desroziers   (default) the error the analysis sees in the data,
               sqrt(E[(O-A)(O-P)]) -- Desroziers et al. (2005)
  conservative the sigma of O-P itself, which holds the background error
               too: sigma_o >= the real sigma, as the current model was
               calibrated

Writes, next to the table unless --out says otherwise:
  radar_obs_error_fit.csv       the coefficients, old and new, per class
  radar_obs_error_fitted.py     the table in the format of
                                radar_obs_error.py, ready to paste
  radar_obs_error_fit_<net>.png one panel per class: the target per height
                                (dot size ~ N), the current model, the fit
"""

import argparse
import csv
import math
import os
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np

from pikobs.profile.radar_obs_error import _TABLE

ONSETS = np.arange(0.5, 10.0, 1.0)
BOUNDS = ([1.0, 0.0, 0.0], [16.0, 5.0, 1.0])     # base, slope, accel


def _class_of(net: str, elevation: float):
    tenths = int(round(float(elevation) * 10.0))
    for i, ((lo, hi), coef) in enumerate(_TABLE.get(net, [])):
        if lo <= tenths <= hi:
            return i, (lo, hi), coef
    return None


def _model(coef, h):
    base, onset, slope, accel = coef
    dh = np.maximum(0.0, np.asarray(h, float) - onset)
    return np.clip(base + slope * dh + accel * dh * dh, 2.0, 16.0)


def read_table(path, run, region, criteria, target, min_obs):
    """{(net, class): {height: [sum w*t^2, sum w]}} and the class ranges."""
    pooled = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
    ranges = {}
    with open(path, newline='') as fh:
        for row in csv.DictReader(fh):
            if run and row['run'] != run:
                continue
            if region and row['region'] != region:
                continue
            if criteria and row['criteria'] != criteria:
                continue
            net = row['station'][:1].upper()
            found = _class_of(net, float(row['elevation']))
            if not found:
                continue
            idx, rng, coef = found
            if target == 'desroziers':
                n = float(row.get('n_desroziers') or 0)
                t = float(row.get('obs_err_desroziers') or 'nan')
            else:
                n = float(row['n'])
                t = float(row['std'])
            if n < min_obs or not math.isfinite(t):
                continue
            h = float(row['height_km'])
            # pool the variances of every station of the network
            acc = pooled[(net, idx)][h]
            acc[0] += n * t * t
            acc[1] += n
            ranges[(net, idx)] = (rng, coef)
    return pooled, ranges


def fit_class(points: Dict[float, List[float]]):
    """(base, onset, slope, accel), weighted rms of the fit, N."""
    from scipy.optimize import lsq_linear
    h = np.array(sorted(points))
    w = np.array([points[k][1] for k in h])
    t = np.sqrt(np.array([points[k][0] / points[k][1] for k in h]))
    best = None
    for onset in ONSETS:
        dh = np.maximum(0.0, h - onset)
        a = np.column_stack([np.ones_like(h), dh, dh * dh])
        sw = np.sqrt(w / w.sum())
        res = lsq_linear(a * sw[:, None], t * sw, bounds=BOUNDS)
        rms = float(np.sqrt(np.sum(w * (a @ res.x - t) ** 2) / w.sum()))
        if best is None or rms < best[1]:
            best = ((float(res.x[0]), float(onset), float(res.x[1]),
                     float(res.x[2])), rms)
    return best[0], best[1], h, t, w


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument('table')
    ap.add_argument('--run', default='')
    ap.add_argument('--region', default='Monde')
    ap.add_argument('--criteria', default='')
    ap.add_argument('--target', default='desroziers',
                    choices=['desroziers', 'conservative'])
    ap.add_argument('--min_obs', type=int, default=30,
                    help="a height bin of a station with fewer is ignored")
    ap.add_argument('--min_heights', type=int, default=4,
                    help="a class with fewer heights keeps its old "
                         "coefficients")
    ap.add_argument('--out', default='')
    args = ap.parse_args(argv)

    out = args.out or os.path.dirname(os.path.abspath(args.table))
    os.makedirs(out, exist_ok=True)
    pooled, ranges = read_table(args.table, args.run, args.region,
                                args.criteria, args.target, args.min_obs)
    if not pooled:
        print("[fit] nothing to fit: check --run, --region, --criteria, "
              "and that the table has obs_err_desroziers", file=sys.stderr)
        return 1

    rows, fitted = [], defaultdict(dict)
    for (net, idx) in sorted(pooled):
        (lo, hi), old = ranges[(net, idx)]
        pts = pooled[(net, idx)]
        if len(pts) < args.min_heights:
            fitted[net][idx] = (old, None)
            rows.append([net, lo / 10, hi / 10, len(pts), '', *old,
                         *old, '', '', 'kept: too few heights'])
            continue
        coef, rms, h, t, w = fit_class(pts)
        old_rms = float(np.sqrt(np.sum(w * (_model(old, h) - t) ** 2)
                                / w.sum()))
        fitted[net][idx] = (coef, (h, t, w, old))
        rows.append([net, lo / 10, hi / 10, len(pts), int(w.sum()), *old,
                     *coef, f"{old_rms:.3f}", f"{rms:.3f}", 'fitted'])
        print(f"[fit] {net} {lo / 10:5.1f}..{hi / 10:5.1f} deg  "
              f"{len(pts):2d} heights  N={int(w.sum()):>8,}  rms "
              f"{old_rms:5.2f} -> {rms:5.2f} m/s", flush=True)

    with open(os.path.join(out, 'radar_obs_error_fit.csv'), 'w',
              newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['network', 'elev_from', 'elev_to', 'heights', 'n',
                     'old_base', 'old_onset', 'old_slope', 'old_accel',
                     'new_base', 'new_onset', 'new_slope', 'new_accel',
                     'old_rms', 'new_rms', 'status'])
        wr.writerows(rows)

    # the table, in the format of radar_obs_error.py
    lines = [f"# fitted by fit_radar_obs_error.py, target {args.target}, "
             f"run {args.run or 'all'}, region {args.region}",
             "_TABLE = {"]
    for net in sorted(_TABLE):
        lines.append(f"    '{net}': [")
        for idx, ((lo, hi), old) in enumerate(_TABLE[net]):
            coef = fitted.get(net, {}).get(idx, (old, None))[0]
            tag = "fitted" if fitted.get(net, {}).get(idx, (0, None))[1] \
                is not None else "unchanged"
            lines.append(f"        (({lo}, {hi}), ({coef[0]:.6f}, "
                         f"{coef[1]:.1f}, {coef[2]:.6f}, {coef[3]:.6f})),"
                         f"    # {tag}")
        lines.append("    ],")
    lines.append("}")
    with open(os.path.join(out, 'radar_obs_error_fitted.py'), 'w') as fh:
        fh.write("\n".join(lines) + "\n")

    _plot(fitted, ranges, out, args.target)
    print(f"[fit] written in {out}: radar_obs_error_fit.csv, "
          f"radar_obs_error_fitted.py, radar_obs_error_fit_<net>.png")
    return 0


def _plot(fitted, ranges, out, target):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    for net, classes in fitted.items():
        shown = [(i, c) for i, c in sorted(classes.items()) if c[1]]
        if not shown:
            continue
        ncol = 5
        nrow = int(math.ceil(len(shown) / ncol))
        fig, axes = plt.subplots(nrow, ncol, figsize=(3.4 * ncol,
                                                      3.0 * nrow + 0.8),
                                 sharex=True, sharey=True, squeeze=False)
        for ax in axes.flat[len(shown):]:
            ax.axis('off')
        for ax, (idx, (coef, (h, t, w, old))) in zip(axes.flat, shown):
            (lo, hi), _ = ranges[(net, idx)]
            hh = np.linspace(0, 14.0, 200)       # the frame of the radar
            ax.scatter(t, h, s=12 + 60 * w / w.max(), color='#555555',
                       alpha=0.7, zorder=3, label=target)
            ax.plot(_model(old, hh), hh, color='#2166AC', lw=1.6,
                    label='current model')
            ax.plot(_model(coef, hh), hh, color='#D62728', lw=1.8,
                    label='fit')
            ax.set_title(f"{lo / 10:g} to {hi / 10:g} deg  "
                         f"(N {int(w.sum()):,})", fontsize=9)
            ax.grid(True, ls='--', alpha=0.3)
        for ax in axes[:, 0]:
            ax.set_ylabel("beam height [km]")
            ax.set_ylim(0.0, 14.0)
        for ax in axes[-1, :]:
            ax.set_xlabel("sigma_o [m/s]")
        axes.flat[0].legend(fontsize=8, loc='upper left')
        fig.suptitle(f"radar network {net}: observation error by height "
                     f"and elevation class, target {target}",
                     fontsize=12, fontweight='bold')
        fig.tight_layout(rect=(0, 0, 1, 0.96))
        fig.savefig(os.path.join(out, f"radar_obs_error_fit_{net}.png"),
                    dpi=130)
        plt.close(fig)


if __name__ == '__main__':
    sys.exit(main())
