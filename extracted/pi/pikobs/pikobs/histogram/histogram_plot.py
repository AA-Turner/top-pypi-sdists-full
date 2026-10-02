#!/usr/bin/python3
"""Figures of pikobs.histogram.

Left, the distribution of each run as a density -- counts divided by the
number of observations and by the width of a bin -- so two runs with a
different number of observations compare on the same footing. The
Gaussian of the same mean and sigma is drawn thin for reference: where
the histogram rises above it in the tails, the errors are not Gaussian,
and that is what a quality control has to know. Below it, with a
control, the difference of the two densities. Right, the statistics of
each run, with the tests of pikobs.stats on the mean and the sigma.
"""

import math
import os
import re
import sys
from typing import Any, Dict, Optional

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import pikobs
from pikobs.figures import save_figure
from pikobs.obsdb import open_result
from pikobs.stats import (MIN_CONFIDENCE, is_significant, ks_from_counts,
                          paired_ttest_confidence, ttest_confidence,
                          sigma_confidence)
from pikobs.zone.zone_plot import members_text

# The look comes from one place, so blue means the control and red the
# experience in every module, and a figure of histogram sits next to one
# of profile without a jarring change of palette.
from pikobs.configobs.style import (CTL_BETTER, CTL_COLOUR, DPI, EXP_BETTER,
                                    EXP_COLOUR, GREY_TEXT as _GREY_TEXT,
                                    QC_ASSIMILATED, QC_BLUES,
                                    QC_OTHER as QC_OTHER_COLOUR, QC_PALETTE,
                                    STYLE as _STYLE)

MIN_OBS_PER_HISTOGRAM = 100


def _qc_colours(order):
    """A colour for every category, in the order they are stacked.

    One colour per bit combination: blue for bit 12 alone, grey for the
    pooled rare ones, and a colour of its own for every other combination
    -- 12+13 is not 12, and a 9+16 that has its O-P computed must be seen
    for where it sits, not merged into a diagnosis.
    """
    out, pal = {}, iter(QC_PALETTE)
    for label in order:
        bits = label.split('  ', 1)[0]
        if label == "OTHER COMBINATIONS":
            out[label] = QC_OTHER_COLOUR
        elif bits == '12':
            out[label] = QC_ASSIMILATED
        else:
            out[label] = next(pal, '#666666')
    return out


def _qc_legend_label(name: str, share: float) -> str:
    """Share first, long names over two lines, so the legend stays narrow."""
    import textwrap
    pct = "<0.1 %" if 0 < share < 0.05 else f"{share:.1f} %"
    # the bits only: what each bit means is in the table beside
    bits = "other" if name == "OTHER COMBINATIONS" else name.split('  ', 1)[0]
    body = "\n".join(textwrap.wrap(bits, 30)) or bits
    return f"{pct:>7s}  " + body.replace("\n", "\n" + " " * 10)

LABELS = {'omp': 'O-P', 'oma': 'O-A', 'omp_norm': '(O-P) / sigma_o',
          'oma_norm': '(O-A) / sigma_o', 'omp_std': 'O-P / sigma',
          'oma_std': 'O-A / sigma'}


def _safe(text: Any) -> str:
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


def figure_name(task: Dict[str, Any]) -> str:
    # the surface and the special value after the region, only when
    # they split something: the naming convention of every module
    extra = "".join(f"_{_safe(x)}" for x in (task.get('land_ocean', 'all'),
                                             task.get('special_label', 'all'))
                    if x not in (None, '', 'all'))
    return (f"histogram_{'_vs_'.join(_safe(n) for n in task['names'])}_"
            f"{_safe(task['family'])}_{task['function']}_"
            f"varno{_safe(task['varno'])}_lev{_safe(task['lkey'])}_"
            f"{_safe(task['stn_tag'])}_{_safe(task['region'])}{extra}_"
            f"{_safe(task['flag'])}.png")


def _where(task):
    return ("region = ? AND flag = ? AND land_ocean = ? AND id_stn = ? "
            "AND special IS ? AND varno = ? AND lkey = ? AND fonction = ?",
            [task['region'], task['flag'], task['land_ocean'],
             task['id_stn'], task['special'], task['varno'], task['lkey'],
             task['function']])


def read_flag_combinations(task):
    """({sig: n} with O-P, {sig: n} without) for this selection."""
    try:
        with open_result(task['db_file']) as conn:
            rows = conn.execute(
                "SELECT has_omp, sig, SUM(n), SUM(sx), SUM(sxx) "
                "FROM flagcomb WHERE region = ? "
                "AND flag = ? AND land_ocean = ? AND id_stn = ? "
                "AND special IS ? AND varno = ? AND lkey = ? "
                "GROUP BY has_omp, sig;",
                (task['region'], task['flag'], task['land_ocean'],
                 task['id_stn'], task['special'], task['varno'],
                 task['lkey'])).fetchall()
    except Exception:
        return {}, {}
    inside, outside = {}, {}
    for has, sig, n, sx, sxx in rows:
        n = float(n or 0)
        # mean and sigma of O-P over that combination, when it has one
        mean = sigma = None
        if sx is not None and n > 0:
            mean = float(sx) / n
            if sxx is not None:
                var = float(sxx) / n - mean * mean
                sigma = math.sqrt(var) if var > 0 else 0.0
        (inside if has else outside)[int(sig)] = (n, mean, sigma)
    return inside, outside


def _bits(sig: int) -> str:
    return "+".join(str(b) for b in range(24) if sig >> b & 1) or "none"


def _flag_table(ax, inside, outside, max_rows: int = 10) -> None:
    """The flag combinations of the selection, and what their bits mean.

    One line per combination -- its share of all the observations of the
    selection and its bits -- in two blocks, in the histogram and left out
    for having no O-P. Below, every bit that appears, once, with its
    meaning from flag_groups: the same words as the flags module, and a
    table short enough to be read.
    """
    try:
        from pikobs.configobs.flag_groups import BIT_DESCRIPTIONS
    except Exception:                                      # pragma: no cover
        BIT_DESCRIPTIONS = {}
    total = (sum(v[0] for v in inside.values())
             + sum(v[0] for v in outside.values()))
    if not total:
        return
    _panel_title(ax, "Flag combinations",
                 "share of the selection, and the O-P of each one")
    lines = []
    seen_bits = set()

    def block(title, counts):
        n = sum(v[0] for v in counts.values())
        lines.append(f"{title}  {100.0 * n / total:.1f} %")
        lines.append(f"  {'share':>7s}  {'N':>9s} {'mean':>7s} {'sigma':>7s}"
                     f"  bits")
        top = sorted(counts.items(), key=lambda kv: -kv[1][0])
        for sig, (c, mean, sigma) in top[:max_rows]:
            share = 100.0 * c / total
            pct = "<0.1 %" if share < 0.05 else f"{share:.1f} %"
            stat = (f"{mean:7.3f} {sigma:7.3f}"
                    if mean is not None and sigma is not None
                    else f"{'--':>7s} {'--':>7s}")
            lines.append(f"  {pct:>7s}  {int(c):>9d} {stat}  {_bits(sig)}")
            seen_bits.update(b for b in range(24) if sig >> b & 1)
        if len(top) > max_rows:
            rest = sum(v[0] for _, v in top[max_rows:])
            pct = "<0.1 %" if 0 < 100.0 * rest / total < 0.05 \
                else f"{100.0 * rest / total:.1f} %"
            lines.append(f"  {pct:>7s}  {int(rest):>9d} {'':15s}  "
                         f"{len(top) - max_rows} more")
        lines.append("")

    block("IN THE HISTOGRAM (O-P)", inside)
    if outside:
        block("LEFT OUT (no O-P)", outside)
    lines.append("BITS")
    for b in sorted(seen_bits):
        lines.append(f"  {b:2d}  {BIT_DESCRIPTIONS.get(b, '')[:34]}")
    try:
        from pikobs.histogram.histogram import QC_INFO_BITS
    except Exception:                                      # pragma: no cover
        QC_INFO_BITS = (5, 6, 10)
    lines.append(f"  ({', '.join(map(str, QC_INFO_BITS))} not counted: "
                 f"not decisions)")
    # large type; smaller only when the table would not fit otherwise
    size = float(np.clip(12.0 * 40 / max(len(lines), 40), 8.5, 12.0))
    ax.text(0.0, 0.91, "\n".join(lines), fontsize=size, family='monospace',
            va='top', color='#222222', transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.5', fc='#f7f7f7', ec='#bbbbbb'))


def _read_one(db_file, task, where, args):
    """Counts and power sums of one run, from its own base."""
    with open_result(db_file) as conn:
        spec = conn.execute(
            "SELECT w, kmin, kmax FROM binspec WHERE family = ? AND "
            "fonction = ? AND varno = ? AND lkey = ?;",
            (task['family'], task.get('source_function', task['function']),
             task['varno'],
             task['lkey'])).fetchone()
        rows = conn.execute(f"SELECT bin, SUM(n_ctl) FROM hist WHERE {where} "
                            f"GROUP BY bin;", args).fetchall()
        mom = conn.execute(f"SELECT SUM(n), SUM(c1), SUM(c2), SUM(c3), "
                           f"SUM(c4) FROM moments WHERE {where};",
                           args).fetchone()
    return spec, rows, [float(x) if x is not None else 0.0 for x in mom]


def read_histogram(task) -> Optional[Dict[str, Any]]:
    where, args = _where(task)
    if task.get('db_ctl'):
        # each run with all its observations and its own flags: two bases,
        # the same bins, and a different N on each side
        spec_c, rows_c, mom_c = _read_one(task['db_ctl'], task, where, args)
        spec_e, rows_e, mom_e = _read_one(task['db_exp'], task, where, args)
        spec = spec_c or spec_e
        if not spec:
            return None
        w, kmin, kmax = spec
        k = np.arange(kmin - 1, kmax + 2)
        ctl, exp = np.zeros(len(k)), np.zeros(len(k))
        for rows, arr in ((rows_c, ctl), (rows_e, exp)):
            for b, n in rows:
                i = int(b) - (kmin - 1)
                if 0 <= i < len(k):
                    arr[i] += n or 0
        return {'w': float(w), 'k': k, 'ctl': ctl, 'exp': exp, 'qc': {},
                'n_c': mom_c[0], 'n_e': mom_e[0], 'mc': mom_c[1:5],
                'me': mom_e[1:5], 'ce': None, 'paired': False}
    with open_result(task['db_file']) as conn:
        spec = conn.execute(
            "SELECT w, kmin, kmax FROM binspec WHERE family = ? AND "
            "fonction = ? AND varno = ? AND lkey = ?;",
            (task['family'], task.get('source_function', task['function']),
             task['varno'],
             task['lkey'])).fetchone()
        if not spec:
            return None
        rows = conn.execute(f"SELECT bin, qc, SUM(n_ctl), SUM(n_exp) FROM "
                            f"hist WHERE {where} GROUP BY bin, qc;",
                            args).fetchall()
        mom = conn.execute(f"SELECT SUM(n), SUM(c1), SUM(c2), SUM(c3), "
                           f"SUM(c4), SUM(e1), SUM(e2), SUM(e3), SUM(e4), "
                           f"SUM(ce) FROM moments WHERE {where};",
                           args).fetchone()
    w, kmin, kmax = spec
    k = np.arange(kmin - 1, kmax + 2)
    ctl = np.zeros(len(k))
    exp = np.zeros(len(k))
    by_qc: Dict[str, np.ndarray] = {}
    for b, qc, nc, ne in rows:
        i = int(b) - (kmin - 1)
        if 0 <= i < len(k):
            ctl[i] += nc or 0
            exp[i] += ne or 0
            if qc and qc != 'all':
                by_qc.setdefault(qc, np.zeros(len(k)))[i] += nc or 0
    mom = [float(x) if x is not None else np.nan for x in mom]
    return {'w': float(w), 'k': k, 'ctl': ctl, 'exp': exp, 'qc': by_qc,
            'n_c': mom[0], 'n_e': mom[0], 'mc': mom[1:5], 'me': mom[5:9],
            'ce': mom[9], 'paired': True}


def _merged(counts, k, w, n, m=None):
    """Coarser bins for the drawing when there are few observations.

    The extraction keeps fine bins, one twentieth of a sigma, which a
    season of data fills well. A few thousand observations sigma over
    them look like noise, so the inner bins are merged to about
    2 N^(1/3) of them (the Rice rule); the two overflow bins stay apart.
    The statistics are untouched: they come from the exact values.
    """
    inner = counts[1:-1]
    if m is None:
        target = max(20.0, 2.0 * n ** (1.0 / 3.0))
        m = max(1, int(np.ceil(len(inner) / target)))
    idx = np.arange(0, len(inner), m)
    merged = np.add.reduceat(inner, idx)
    kmin, kmax = int(k[1]), int(k[-2])
    inner_edges = np.append((kmin + idx) * w, (kmax + 1) * w)
    edges = np.concatenate(([(kmin - 1) * w], inner_edges, [(kmax + 2) * w]))
    return np.concatenate(([counts[0]], merged, [counts[-1]])), edges, m


def _moments(n, s1, s2, s3, s4):
    """Mean, sigma, skewness and excess kurtosis from power sums."""
    m = s1 / n
    var = max(s2 / n - m * m, 0.0)
    sd = np.sqrt(var)
    if sd <= 0:
        return m, 0.0, np.nan, np.nan
    m3 = s3 / n - 3 * m * s2 / n + 2 * m ** 3
    m4 = s4 / n - 4 * m * s3 / n + 6 * m * m * s2 / n - 3 * m ** 4
    return m, sd, m3 / sd ** 3, m4 / sd ** 4 - 3.0


def _beyond(counts, k, w, mean, sd, n_sig=3.0):
    """Share of observations more than n_sig sigmas from the mean."""
    centres = (k + 0.5) * w
    far = np.abs(centres - mean) > n_sig * sd
    total = counts.sum()
    return 100.0 * counts[far].sum() / total if total else np.nan


def _scale_of(limit: float):
    if not limit or not np.isfinite(limit):
        return 1.0, ""
    exp = int(np.floor(np.log10(abs(limit))))
    if -2 <= exp <= 3:
        return 1.0, ""
    sup = str.maketrans("-0123456789", "\u207b\u2070\u00b9\u00b2\u00b3"
                        "\u2074\u2075\u2076\u2077\u2078\u2079")
    return 10.0 ** exp, "10" + str(exp).translate(sup) + " "


# ─────────────────────────────────────────────────────────────────────────────
# Style: clean axes, a header, tables instead of loose text
# ─────────────────────────────────────────────────────────────────────────────

def _style_axes(ax) -> None:
    """Light frame, soft grid, grid under the data."""
    ax.set_facecolor("white")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#B0B0B0")
    ax.tick_params(axis="both", which="both", labelsize=11.5, colors="#333333")
    ax.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.25)
    ax.set_axisbelow(True)


def _panel_title(ax, title: str, subtitle: str = "", y: float = 0.995):
    ax.text(0.0, y, title, transform=ax.transAxes, ha="left", va="top",
            fontsize=13, fontweight="bold", color="#222222")
    if subtitle:
        ax.text(0.0, y - 0.04, subtitle, transform=ax.transAxes, ha="left",
                va="top", fontsize=9.5, color=_GREY_TEXT)


def _stat_words(cnt, stt, k, w) -> str:
    """One run's statistics, each number with what it says."""
    s, kurt = stt[2], stt[3]
    if not np.isfinite(s):
        skew = "skewness -"
    elif abs(s) < 0.2:
        skew = f"skewness {s:.2f} (symmetric)"
    else:
        skew = (f"skewness {s:.2f} (longer tail to the "
                f"{'right' if s > 0 else 'left'})")
    if not np.isfinite(kurt):
        kur = "excess kurtosis -"
    elif abs(kurt) < 0.5:
        kur = f"excess kurtosis {kurt:.2f} (tails like a Gaussian)"
    else:
        kur = (f"excess kurtosis {kurt:.2f} ("
               f"{'heavier' if kurt > 0 else 'lighter'} tails than a Gaussian)")
    b = _beyond(cnt, k, w, stt[0], stt[1])
    ratio = b / 0.27
    far = (f"beyond 3 sigma {b:.2f} % ({ratio:.1f}x a Gaussian's 0.27 %)"
           if ratio >= 1.5 or ratio <= 0.67 else
           f"beyond 3 sigma {b:.2f} % (a Gaussian: 0.27 %)")
    return "   ".join([skew, kur, far])


def _stat_table(ax, runs, k, w, fmt, top: float, height: float) -> None:
    """The statistics of each run, as a table in the run colours."""
    rows = [("N", [f"{int(r[1].sum()):,}" for r in runs]),
            ("mean", [fmt(r[2][0]) for r in runs]),
            ("sigma", [fmt(r[2][1]) for r in runs]),
            ("skewness", [f"{r[2][2]:.2f}" if np.isfinite(r[2][2]) else "-"
                          for r in runs]),
            ("excess kurtosis", [f"{r[2][3]:.2f}" if np.isfinite(r[2][3])
                                 else "-" for r in runs]),
            ("beyond 3 sigma",
             [f"{_beyond(r[1], k, w, r[2][0], r[2][1]):.2f} %"
              for r in runs])]
    table = ax.table(cellText=[[lab] + vals for lab, vals in rows],
                     colLabels=[""] + [r[0] for r in runs],
                     cellLoc="left", colLoc="left",
                     bbox=[0.0, top - height, 0.98, height],
                     colWidths=[0.44] + [0.54 / len(runs)] * len(runs))
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#E3E3E3")
        cell.set_linewidth(0.6)
        cell.PAD = 0.06
        if row == 0:
            cell.set_facecolor("#F3F5F7")
            colour = runs[col - 1][3] if col > 0 else "#222222"
            cell.set_text_props(fontweight="bold", color=colour)
        else:
            cell.set_facecolor("white")
            cell.set_text_props(color="#333333",
                                fontweight="bold" if col == 0 else "normal")


def _test_rows(names, data, stats_ctl, stats_exp, paired, normalised, n):
    """[(name, confidence, verdict, colour)] of the three tests."""
    m_c, s_c = stats_ctl[0], stats_ctl[1]
    m_e, s_e = stats_exp[0], stats_exp[1]
    n_c, n_e = data['n_c'], data['n_e']
    if paired:
        cov = data['ce'] / n - m_c * m_e
        t_conf = float(paired_ttest_confidence(
            np.array([m_c]), np.array([m_e]), np.array([s_c ** 2]),
            np.array([s_e ** 2]), np.array([cov]), np.array([n]))[0])
    else:
        t_conf = float(ttest_confidence(
            np.array([m_c]), np.array([s_c]), np.array([n_c]),
            np.array([m_e]), np.array([s_e]), np.array([n_e]))[0])
    # the sigma: Pitman-Morgan on the pairs (the covariance the paired
    # t-test uses), the F-test when the runs were not matched --
    # stats.sigma_confidence decides from whether a covariance is given
    if paired:
        f_conf = float(sigma_confidence(
            np.array([s_c ** 2]), np.array([s_e ** 2]), np.array([n]),
            cov=np.array([cov]))[0])
    else:
        f_conf = float(sigma_confidence(
            np.array([s_c ** 2]), np.array([s_e ** 2]), np.array([n_c]),
            np.array([n_e]))[0])
    # a normalised sigma is better the closer it is to 1
    sigma_better = (abs(s_e - 1.0) < abs(s_c - 1.0)) if normalised \
        else (s_e < s_c)
    out = []
    for name, conf, better in (
            ("mean, " + ("paired t" if paired else "Welch t"), t_conf,
             abs(m_e) < abs(m_c)),
            ("sigma, " + ("Pitman-Morgan" if paired else "F"), f_conf,
             sigma_better)):
        if is_significant(np.array([conf]))[0]:
            out.append((name, conf,
                        "Exp better" if better else "Ctl better",
                        EXP_BETTER if better else CTL_BETTER))
        else:
            out.append((name, conf, "not significant", "#777777"))
    d_ks, ks_conf = ks_from_counts(data['ctl'], data['exp'])
    differ = bool(is_significant(np.array([ks_conf]))[0])
    out.append(("shape, KS", ks_conf,
                (f"shapes differ, D = {d_ks:.3f}" if differ
                 else f"same shape, D = {d_ks:.3f}"),
                "#333333" if differ else "#777777"))
    return out


def histogram_plot(task: Dict[str, Any]) -> Optional[str]:
    with plt.rc_context(_STYLE):
        return _histogram_plot(task)


def _histogram_plot(task: Dict[str, Any]) -> Optional[str]:
    data = read_histogram(task)
    if data is None:
        return None
    matched = task['matched']
    n_c, n_e = data['n_c'], data['n_e']
    min_obs = int(task.get('min_obs', MIN_OBS_PER_HISTOGRAM))
    if not n_c or n_c < min_obs or (matched and (not n_e or n_e < min_obs)):
        return None
    n = n_c
    w, k = data['w'], data['k']
    edges = np.append(k, k[-1] + 1) * w
    stats_ctl = _moments(n_c, *data['mc'])
    stats_exp = _moments(n_e, *data['me']) if matched else None
    if stats_ctl[1] <= 0:
        return None                     # O-P identical everywhere: no shape
    paired = bool(data.get('paired', True))

    family = task['family']
    var_name, units, _ = pikobs.type_varno(str(task['varno']))
    gpsro = bool(task.get('gpsro'))
    label = LABELS[task['function']]
    normalised = task['function'].endswith('_norm')
    unit = "[-]" if (gpsro or normalised) else units
    f, st = _scale_of(max(abs(edges[0]), abs(edges[-1])))
    if task['function'].endswith('_std'):
        # in sigmas of the control (of the run itself when alone): the
        # unit factor becomes that sigma, the bins stay the same
        f, st, unit = stats_ctl[1], "", "[sigma]"
    u = str(unit).strip().strip('[]')
    x_label = (f"({label}) / B_ref" if gpsro and not normalised else label) \
        + (f"  [{st}{u}]" if (u or st) and u != '-' else "")

    # ---- layout: the histogram, its statistics, and the flags ---------------
    with_flags = bool(task.get('qc_split')) and not matched
    fig = plt.figure(figsize=(19.5 if with_flags else 17.0, 10.0),
                     facecolor='white')
    # the header holds the statistics, one line per run; the right column
    # holds the flag table of a single run, or the tests of a comparison
    head = 0.215 if matched else 0.175
    gs = fig.add_gridspec(2 if matched else 1, 2,
                          height_ratios=[3.3, 1.1] if matched else [1],
                          width_ratios=([2.35, 1.35] if with_flags
                                        else [2.8, 1.2]),
                          hspace=0.06, wspace=0.08, left=0.055, right=0.985,
                          top=1.0 - head, bottom=0.075)
    ax = fig.add_subplot(gs[0, 0])
    axd = fig.add_subplot(gs[1, 0], sharex=ax) if matched else None
    axt = fig.add_subplot(gs[:, 1])
    axt.axis('off')
    axf = axt if with_flags else None
    _style_axes(ax)
    if axd is not None:
        _style_axes(axd)

    names = task['names']
    # without a control the single run is an experience, so it is red
    # Ctl and Exp in the legend, the table and the tests; the names of the
    # runs once, in the header
    runs = [("Ctl" if matched else "Exp", data['ctl'], stats_ctl,
             CTL_COLOUR if matched else EXP_COLOUR)]
    if matched:
        runs.append(("Exp", data['exp'], stats_exp, EXP_COLOUR))
    xs = np.linspace(edges[0], edges[-1], 700)
    # one grouping of the bins for both runs, from the smaller of the two,
    # so their densities sit on the same bins and can be subtracted
    totals = [r[1].sum() for r in runs]
    _, _, m_common = _merged(data['ctl'], k, w, max(1.0, min(totals)))

    # ---- the QC split: one colour per flag combination ----------------------
    qc_counts = data['qc'] if with_flags else {}
    if qc_counts:
        total = data['ctl'].sum()
        _, e_q, _ = _merged(data['ctl'], k, w, total, m_common)
        widths_q = np.diff(e_q)
        bottom = np.zeros(len(widths_q))
        order = task.get('qc_order') or sorted(qc_counts)
        colours = _qc_colours(order)
        for name in order:
            if name not in qc_counts:
                continue
            c_q, _, _ = _merged(qc_counts[name], k, w, total, m_common)
            d_q = c_q / (total * widths_q)
            share = 100.0 * qc_counts[name].sum() / total
            ax.stairs((bottom + d_q) * f, e_q / f, baseline=bottom * f,
                      fill=True, color=colours[name], alpha=0.8,
                      linewidth=0, label=_qc_legend_label(name, share))
            bottom = bottom + d_q

    # ---- the runs and their Gaussians ------------------------------------------
    dens, e_m, merge = {}, edges, 1
    for name, counts, (m, sd, sk, ku), colour in runs:
        total = counts.sum()
        c_m, e_m, merge = _merged(counts, k, w, total, m_common)
        d = c_m / (total * np.diff(e_m)) if total else c_m
        dens[name] = d
        if not qc_counts:
            ax.stairs(d * f, e_m / f, color=colour, alpha=0.08, fill=True,
                      linewidth=0)
        ax.stairs(d * f, e_m / f, color=colour, lw=1.9, label=name,
                  zorder=6)
        if sd > 0:
            g = np.exp(-0.5 * ((xs - m) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
            ax.plot(xs / f, g * f, color=colour, lw=1.1, ls='--', alpha=0.8,
                    zorder=5)
    xmin, xmax = edges[0] / f, edges[-1] / f
    if xmin <= 0 <= xmax:
        ax.axvline(0, color='#444444', ls=':', lw=1.0, zorder=4)

    # +/-3 sigma of the reference run: a Gaussian leaves 0.27 % outside
    m_ref, sd_ref = runs[0][2][0], runs[0][2][1]
    if sd_ref > 0:
        lo3, hi3 = (m_ref - 3 * sd_ref) / f, (m_ref + 3 * sd_ref) / f
        share3 = _beyond(runs[0][1], k, w, m_ref, sd_ref)
        ax.axvline(lo3, color='#8C510A', lw=1.2, ls='-.', alpha=0.9,
                   label=f"+/-3 sigma: {share3:.2f} % outside "
                         f"(Gaussian 0.27 %)")
        ax.axvline(hi3, color='#8C510A', lw=1.2, ls='-.', alpha=0.9)
        ax.axvspan(xmin, lo3, color='#8C510A', alpha=0.045, zorder=0)
        ax.axvspan(hi3, xmax, color='#8C510A', alpha=0.045, zorder=0)
    if normalised:
        g1 = np.exp(-0.5 * xs ** 2) / np.sqrt(2 * np.pi)
        ax.plot(xs / f, g1 * f, color='#2CA02C', lw=2.0, alpha=0.85,
                label="N(0, 1): errors as assigned")

    log_scale = task.get('log_scale', True)
    if log_scale:
        ax.set_yscale('log')
        top = max(np.nanmax(v * f) for v in dens.values())
        positive = [np.min(v[v > 0] * f) for v in dens.values()
                    if np.any(v > 0)]
        low = min(positive) if positive else top * 1e-5
        ax.set_ylim(max(low * 0.4, top * 1e-7), top * 3)
    ax.set_ylabel("density" + (" (log scale: each line x10)" if log_scale
                               else ""), fontsize=12.5)
    ax.set_xlim(xmin, xmax)
    # said in the notes of the right column, where it covers no data
    bin_note = "first and last bins: everything beyond 6 sigmas"
    if merge > 1:
        bin_note += f"\nbins merged by {merge} for {int(n):,} observations"

    # ---- the difference of the densities ---------------------------------------
    if matched:
        diff = (dens["Exp"] - dens["Ctl"]) * f
        top_d = float(np.nanmax(np.abs(diff))) if np.any(diff) else 1.0
        fd, sd_txt = _scale_of(top_d)
        axd.bar(e_m[:-1] / f, diff / fd, width=np.diff(e_m) / f,
                align='edge', linewidth=0, alpha=0.75,
                color=np.where(diff > 0, EXP_COLOUR, CTL_COLOUR))
        axd.axhline(0, color='#333333', lw=0.9)
        axd.set_ylabel("Exp - Ctl"
                       + (f"\n[{sd_txt.strip()}]" if sd_txt else ""),
                       fontsize=11)
        axd.set_xlabel(x_label, fontsize=12.5)
        ax.tick_params(axis='x', labelbottom=False)
    else:
        ax.set_xlabel(x_label, fontsize=12.5)

    # ---- the right column: the tests or the flag table, then the legend --------
    handles, labels = ax.get_legend_handles_labels()
    legend_title = ("flag bits of each colour, share of the histogram\n"
                    "(meaning of the bits in the table above)\n"
                    "dashed: Gaussian of the same mean and sigma"
                    if qc_counts else
                    "dashed: Gaussian of the same mean and sigma")
    legend_at = 0.97
    if matched:
        y = 0.995
        _panel_title(axt, "Tests (pikobs.stats)",
                     f"a change counts above {MIN_CONFIDENCE:.0f} %", y=y)
        y -= 0.095
        for name, conf, verdict, colour in _test_rows(
                names, data, stats_ctl, stats_exp, paired, normalised, n):
            axt.text(0.0, y, name, transform=axt.transAxes, fontsize=12.5,
                     fontweight='bold', color='#333333', va='top')
            axt.text(0.98, y, f"{conf:.1f} %", transform=axt.transAxes,
                     fontsize=12.5, color='#333333', va='top', ha='right')
            axt.text(0.0, y - 0.042, verdict, transform=axt.transAxes,
                     fontsize=12, fontweight='bold', color=colour, va='top')
            y -= 0.115
        axt.text(0.0, y - 0.005,
                 "significant is not the same as large: D is the share of the\n"
                 "observations on the other side, 0.01 = 1 %. "
                 + ("Matched samples:\nKS is a screening, see pikobs.stats."
                    if paired else
                    "Independent\nsamples: the tests are the cautious forms."),
                 transform=axt.transAxes, fontsize=9.5, va='top',
                 color=_GREY_TEXT, linespacing=1.35)
        legend_at = y - 0.12
    if axf is not None:
        inside, outside = read_flag_combinations(task)
        _flag_table(axf, inside, outside)
    # off the curves, in the right column: under the tests, under the flag
    # table (at the bottom of the column), or at its top
    axt.legend(handles, labels, loc=('lower left' if axf is not None
                                      else 'upper left'),
               bbox_to_anchor=((0, 0) if axf is not None else (0, legend_at)),
               fontsize=11, framealpha=0.97, edgecolor='#DDDDDD',
               title=legend_title, title_fontsize=10)

    # ---- the header, as in scatter, zone and cardio ---------------------------
    # the variable in bold, a grey line with what the figure holds, the runs
    # in their colours, the dates top right, the note small, then the rule
    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    if task['lkey'] == 'join':
        try:
            radiance = str(pikobs.family(family)[5]).upper() == 'CANAL'
        except Exception:
            radiance = False
        lev = "all channels" if radiance else "whole column"
    elif ' | ' in str(task['lkey']):
        lev = f"layer {str(task['lkey']).split(' | ', 1)[1]}"
    else:
        lev = f"level {task['lkey']}"
    surface = task.get('land_ocean', 'all')
    # join is every station (or type) together: said in words
    word_m = task.get('member_word', 'station')
    member = members_text(task['db_file'], task['id_stn'])
    parts = [family,
             task['region'] if surface in (None, '', 'all')
             else f"{task['region']} ({surface})",
             f"flag {task['flag']}",
             (f"all {word_m}s" if member == 'join' else f"{word_m} {member}"),
             lev]
    if task.get('special_label') and task['special_label'] != 'all':
        parts.append(f"method {task['special_label']}")
    fig.text(0.055, 0.978, f"{var_name} "
             f"{units if task['function'].endswith('_std') else unit}  ·  "
             f"{label}", ha='left',
             va='top', fontsize=15, fontweight='bold', color='#1F2933')
    fig.text(0.985, 0.975, f"{_when(task['datestart'])}  to  "
             f"{_when(task['dateend'])}", ha='right', va='top', fontsize=10,
             color=_GREY_TEXT)
    fig.text(0.055, 0.944, "  ·  ".join(parts), ha='left', va='top',
             fontsize=10.5, color=_GREY_TEXT)
    who = ([("Exp", names[1], EXP_COLOUR), ("Ctl", names[0], CTL_COLOUR)]
           if matched else [("Exp", names[0], EXP_COLOUR)])
    y_run = 0.914
    for word, name, colour in who:
        fig.text(0.055, y_run, f"{word}  {name}", ha='left', va='top',
                 fontsize=11.5, fontweight='bold', color=colour)
        y_run -= 0.026
    # the statistics, one line per run in its colour: they were a table in
    # the right column, which is now the flags' or the tests'
    def _num(v):
        if not np.isfinite(v):
            return "-"
        return f"{v / f:.3g}" if f != 1 else f"{v:.3g}"

    y_st = 0.914
    for (word, name, colour), run in zip(who, ([runs[1], runs[0]] if matched
                                               else runs)):
        cnt, stt = run[1], run[2]
        fig.text(0.20, y_st - 0.002,
                 f"N {int(cnt.sum()):,}   mean {_num(stt[0])}   "
                 f"sigma {_num(stt[1])}   " + _stat_words(cnt, stt, k, w),
                 ha='left', va='top', fontsize=11, color=colour)
        y_st -= 0.026
    notes = ["a Gaussian: skewness 0, kurtosis 0, 0.27 % beyond 3 sigma",
             bin_note]
    if normalised:
        notes.append("sigma 1 = the assigned errors are right")
    if (st or u) and u != '-':
        notes.append(f"units: {st}{u}")
    if matched:
        change = 100.0 * (n_e - n_c) / n_c if n_c else float('nan')
        notes.insert(0, "the same observations in both runs" if paired else
                     f"each run with all its observations ({change:+.1f} % in Exp)")
    fig.text(0.055, y_st - 0.004, "   ·   ".join(notes), ha='left', va='top',
             fontsize=9.5, color=_GREY_TEXT)
    rule = 1.0 - head + 0.018
    fig.add_artist(mpl.lines.Line2D([0.055, 0.985], [rule, rule],
                                    transform=fig.transFigure,
                                    color='#D9DDE2', lw=0.9))

    out_dir = os.path.join(task['pathwork'], family)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, figure_name(task))
    save_figure(fig, out_file, svg=task.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out_file


def histogram_plot_task(task: Dict[str, Any]) -> Optional[str]:
    import traceback
    try:
        return histogram_plot(task)
    except Exception:
        print(f"[histogram] plot failed for {task.get('family')} "
              f"{task.get('id_stn')} varno {task.get('varno')} level "
              f"{task.get('lkey')}:\n{traceback.format_exc()}",
              file=sys.stderr, flush=True)
        plt.close('all')
        return None
