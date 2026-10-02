#!/usr/bin/python3
"""Figures of pikobs.timeserie.

For every run: the observations of every cycle, stacked by what the
quality control did with them, and -- only when the files carry them --
the mean and the sigma of the departures, the assigned error and the
bias correction. With a control, one more figure with every run on the
same axes and the change of the number of assimilated observations.
"""

import os
import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.dates as mdates
import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np

import pikobs
from pikobs.figures import save_figure
from pikobs.obsdb import open_result
from pikobs.stats import (MIN_CONFIDENCE, is_significant,
                          paired_ttest_confidence, sigma_confidence)

from pikobs.configobs.style import (CTL_COLOUR, DPI, EXP_COLOUR, EXP_COLOURS,
                                    GREY_TEXT as _GREY, QC_ASSIMILATED,
                                    QC_BLUES, QC_OTHER, QC_PALETTE,
                                    STATION_CMAP, STYLE)
# every combination that carries bit 12 (the observation entered the
# analysis) is drawn in blues, from light to dark; everything else in
# its own colour, so a glance separates what was used from what was not
MAX_DIAGNOSES = 8
_STYLE = STYLE


def _safe(text) -> str:
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


def _pct(share: float) -> str:
    """'<0.1 %' instead of a 0.0 % that looks like nothing at all."""
    if share <= 0:
        return "0 %"
    return "<0.1 %" if share < 0.05 else f"{share:.1f} %"


def _bits(sig: int) -> str:
    return "+".join(str(b) for b in range(24) if int(sig) >> b & 1) or "none"


def _reason(sig: int) -> str:
    try:
        from pikobs.configobs.flags_criteria import flag_reason
        return (flag_reason(int(sig)) or "NO QC FLAG").title()
    except Exception:                                      # pragma: no cover
        return f"flag {sig}"


# ─────────────────────────────────────────────────────────────────────────────
# Reading
# ─────────────────────────────────────────────────────────────────────────────

def _sp_tag(spec) -> str:
    """The special value in a file name, only when there is one."""
    sp = spec.get('special_label', 'all')
    return '' if sp in (None, '', 'all') else f"_{_safe(sp)}"


def _sp_txt(spec) -> str:
    """The special value in a title, only when there is one."""
    sp = spec.get('special_label', 'all')
    return '' if sp in (None, '', 'all') else f"   •   {sp}"


def _layer_units(family):
    """(factor from the unit of the layers to that of lev, unit name) for a
    family whose levels are pressures or heights; None for channels. The
    same as scatter, which owns the layers."""
    from pikobs.scatter.scatter import _layer_unit, _vcotyp, needs_layers
    from pikobs.scatter.scatter import layer_unit_scale
    vcotyp = _vcotyp(family)
    if not needs_layers(vcotyp):
        return None
    return layer_unit_scale(vcotyp), _layer_unit(vcotyp)


def _layer_bounds(spec):
    """(low, high) of lev for a layer level such as '2 | 850-500 hPa', else
    None. A layer keeps its larger number, as in scatter: low < lev <= high."""
    units = _layer_units(spec['family'])
    m = re.fullmatch(r"\d+ \| ([0-9.]+)-([0-9.]+) (hPa|km)", str(spec['level']))
    if not units or not m:
        return None
    a, b = float(m.group(1)) * units[0], float(m.group(2)) * units[0]
    return min(a, b), max(a, b)


def _where(spec) -> Tuple[str, list]:
    w = ("region = ? AND flag = ? AND land_ocean = ? AND special = ? "
         "AND varno = ?" + spec['stn_sql'])
    args = [spec['region'], spec['flag'], spec['surface'],
            spec.get('special', 'all'), spec['varno']]
    layer = _layer_bounds(spec)
    if layer:
        # a layer keeps its larger number, as in scatter: low < lev <= high
        w += " AND lev > ? AND lev <= ?"
        args += list(layer)
    elif spec['level'] != 'join':
        w += " AND lev = ?"
        args.append(float(spec['level']))
    return w, args


def read_counts(spec, db):
    """(cycles, {combination: per cycle}, assimilated, {combination: n})."""
    where, args = _where(spec)
    with open_result(db) as conn:
        rows = conn.execute(f"SELECT cycle, sig, SUM(n) FROM ts_qc WHERE "
                            f"{where} GROUP BY cycle, sig;", args).fetchall()
    cycles = spec['cycles']
    idx = {c: i for i, c in enumerate(cycles)}
    by: Dict[int, np.ndarray] = {}
    combos: Dict[int, float] = {}
    assim = np.zeros(len(cycles))
    for cyc, sig, n in rows:
        if cyc not in idx:
            continue
        by.setdefault(int(sig), np.zeros(len(cycles)))[idx[cyc]] += n or 0
        combos[int(sig)] = combos.get(int(sig), 0.0) + (n or 0)
        if int(sig) & 4096:
            assim[idx[cyc]] += n or 0
    return cycles, by, assim, combos


def _member_key(spec, db) -> str:
    """What a member is here: the instrument type on a composite family
    when the data holds more than one, the station otherwise."""
    if spec.get('member_word') != 'type':
        return 'id_stn'
    where, args = _where(spec)
    try:
        with open_result(db) as conn:
            n = conn.execute(f"SELECT COUNT(DISTINCT codtyp) FROM ts_qc "
                             f"WHERE {where};", args).fetchone()[0]
    except Exception:
        return 'id_stn'
    return 'codtyp' if (n or 0) > 1 else 'id_stn'


def _member_name(col: str, key) -> str:
    if col != 'codtyp':
        return str(key)
    from pikobs.stations.stations import _codtyp_name
    return f"{_codtyp_name(int(key))} ({int(key)})"


def read_by_station(spec, db, top: int = 10):
    """Over the whole period, per member: how many observations it brings
    and what quality control did with them. [(member, n, {diag: n})]."""
    where, args = _where(spec)
    col = _member_key(spec, db)
    with open_result(db) as conn:
        rows = conn.execute(f"SELECT {col}, sig, SUM(n) FROM ts_qc WHERE "
                            f"{where} GROUP BY {col}, sig;", args).fetchall()
    per: Dict[str, Dict[str, float]] = {}
    for key, sig, n in rows:
        stn = _member_name(col, key)
        per.setdefault(stn, {})
        d = per[stn]
        lab = _reason(sig)
        d[lab] = d.get(lab, 0.0) + (n or 0)
    out = sorted(((stn, sum(d.values()), d) for stn, d in per.items()),
                 key=lambda t: -t[1])
    return out[:top], out[top:]


def read_counts_by_member(spec, db):
    """The observations per cycle of every station -- or of every
    instrument type, on ai, ua, sf, gp and csr, where a station is one
    report and the type is what the eye follows."""
    col = _member_key(spec, db)
    where, args = _where(spec)
    with open_result(db) as conn:
        rows = conn.execute(f"SELECT cycle, {col}, SUM(n) FROM ts_qc WHERE "
                            f"{where} GROUP BY cycle, {col};",
                            args).fetchall()
    cycles = spec['cycles']
    idx = {c: i for i, c in enumerate(cycles)}
    by: Dict[str, np.ndarray] = {}
    for cyc, key, n in rows:
        if cyc not in idx:
            continue
        by.setdefault(_member_name(col, key),
                      np.zeros(len(cycles)))[idx[cyc]] += n or 0
    return by


def read_values(spec, db) -> Optional[Dict[str, np.ndarray]]:
    """Per cycle: mean and sigma of O-P and O-A, mean assigned error,
    mean bias correction; None if the files carry none of them."""
    where, args = _where(spec)
    with open_result(db) as conn:
        rows = conn.execute(
            f"SELECT cycle, SUM(n_omp), SUM(s_omp), SUM(s2_omp), SUM(n_oma), "
            f"SUM(s_oma), SUM(s2_oma), SUM(n_err), SUM(s_err), SUM(n_bc), "
            f"SUM(s_bc) FROM ts_val WHERE {where} GROUP BY cycle;",
            args).fetchall()
    if not rows:
        return None
    cycles = spec['cycles']
    idx = {c: i for i, c in enumerate(cycles)}
    keys = ('m_omp', 's_omp', 'm_oma', 's_oma', 'm_err', 'm_bc')
    out = {k: np.full(len(cycles), np.nan) for k in keys}
    found = False
    for cyc, np_, sp, s2p, na, sa, s2a, ne, se, nb, sb in rows:
        if cyc not in idx:
            continue
        i = idx[cyc]
        if np_:
            m = sp / np_
            out['m_omp'][i] = m
            out['s_omp'][i] = max(s2p / np_ - m * m, 0) ** 0.5
            found = True
        if na:
            m = sa / na
            out['m_oma'][i] = m
            out['s_oma'][i] = max(s2a / na - m * m, 0) ** 0.5
            found = True
        if ne:
            out['m_err'][i] = se / ne
            found = True
        if nb:
            out['m_bc'][i] = sb / nb
            found = True
    return out if found else None


def read_shared(spec, db):
    """(shared, only in the control, only in the experience) over the
    period, or None when the runs were not matched."""
    where, args = _where(spec)
    try:
        with open_result(db) as conn:
            if not conn.execute("SELECT 1 FROM sqlite_master WHERE type = "
                                "'table' AND name = 'ts_pair';").fetchone():
                return None
            row = conn.execute(f"SELECT SUM(n_both), SUM(n_ctl_only), "
                               f"SUM(n_exp_only) FROM ts_pair WHERE "
                               f"{where};", args).fetchone()
    except Exception:
        return None
    if not row or not row[0]:
        return None
    return tuple(float(v or 0) for v in row)


def read_matched(spec, db):
    """Per cycle, over the observations both runs have: the mean and the
    sigma of each of them, and the confidence of the paired tests."""
    _f = spec.get('function', 'omp')          # the sums of O-P or of O-A
    _n = 'n_a' if _f == 'oma' else 'n_p'
    where, args = _where(spec)
    try:
        with open_result(db) as conn:
            if not conn.execute("SELECT 1 FROM sqlite_master WHERE type = "
                                "'table' AND name = 'ts_pair';").fetchone():
                return None
            rows = conn.execute(
                f"SELECT cycle, SUM({_n}), SUM(c_{_f}), SUM(c2_{_f}), "
                f"SUM(e_{_f}), SUM(e2_{_f}), SUM(ce_{_f}) FROM ts_pair "
                f"WHERE {where} GROUP BY cycle;", args).fetchall()
    except Exception:
        return None
    cycles = spec['cycles']
    idx = {c: i for i, c in enumerate(cycles)}
    keys = ('n', 'mc', 'sc', 'me', 'se', 'cov')
    out = {k: np.full(len(cycles), np.nan) for k in keys}
    for cyc, n, c, c2, e, e2, ce in rows:
        if cyc not in idx or not n:
            continue
        i = idx[cyc]
        mc, me = c / n, e / n
        out['n'][i] = n
        out['mc'][i] = mc
        out['me'][i] = me
        out['sc'][i] = max(c2 / n - mc * mc, 0) ** 0.5
        out['se'][i] = max(e2 / n - me * me, 0) ** 0.5
        out['cov'][i] = ce / n - mc * me
    if not np.any(np.isfinite(out['n'])):
        return None
    ok = np.isfinite(out['n'])
    out['t_conf'] = np.full(len(cycles), np.nan)
    out['f_conf'] = np.full(len(cycles), np.nan)
    out['t_conf'][ok] = paired_ttest_confidence(
        out['mc'][ok], out['me'][ok], out['sc'][ok] ** 2, out['se'][ok] ** 2,
        out['cov'][ok], out['n'][ok])
    # matched runs: Pitman-Morgan, which uses the covariance the pairs
    # carry (the F-test assumes independent samples and misses almost
    # every change of sigma between two correlated runs)
    out['f_conf'][ok] = sigma_confidence(
        out['sc'][ok] ** 2, out['se'][ok] ** 2, out['n'][ok],
        cov=out['cov'][ok])
    return out


def alerts_of(counts: np.ndarray, cycles, pct: float, days: int = 4):
    """Cycles that bring far fewer observations than they usually do.

    Every cycle is compared with the median of the SAME hour on the days
    before it. A family like ua lives on a synoptic rhythm -- thousands of
    observations at 00 and 12 UTC, a handful at 06 and 18 -- so comparing
    a cycle with the ones just before it would flag every 06 and every 18,
    day after day, and say nothing.

    [(index, n, median of the same hour, drop %)]
    """
    out = []
    if pct <= 0:
        return out
    hours = [str(c)[8:10] for c in cycles]
    for i in range(len(counts)):
        before = [counts[j] for j in range(i) if hours[j] == hours[i]]
        if len(before) < 2:
            continue                      # not enough history at that hour
        med = float(np.median(before[-days:]))
        if med > 0 and counts[i] < med * (1 - pct / 100.0):
            out.append((i, float(counts[i]), med,
                        100.0 * (1 - counts[i] / med)))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Planning
# ─────────────────────────────────────────────────────────────────────────────

def plan_figures(family, all_runs, control, selectors, regions, flags,
                 channels, pathwork, datestart, dateend, db_path, svg,
                 alert_pct, match='off',
                 functions=('omp',), pressure_layers=(),
                 height_layers=()) -> List[Dict[str, Any]]:
    from pikobs.obsdb import cycles as _cycles
    from pikobs.configobs.special_family import special_label
    cycles = _cycles(datestart, dateend)
    dbs = {n: db_path(pathwork, family, n, datestart, dateend)
           for n, _ in all_runs}
    # what to draw comes from every run, not from the first one: a varno
    # or a region present in one run only still gets its figures
    combos, levels = set(), set()
    for db in dbs.values():
        try:
            with open_result(db) as conn:
                combos.update(conn.execute(
                    "SELECT DISTINCT region, flag, land_ocean, special, varno "
                    "FROM ts_qc;"))
                levels.update(r[0] for r in conn.execute(
                    "SELECT DISTINCT lev FROM ts_qc WHERE lev IS NOT NULL;"))
        except Exception:
            continue
    if not combos:
        return []
    combos = sorted(combos, key=lambda c: (str(c[0]), str(c[1]), str(c[2]),
                                           str(c[3]), c[4]))
    levels = sorted(levels)
    lv = []
    for c in channels:
        if c == 'join':
            lv.append('join')
        elif c == 'all':
            lv += [f"{v:g}" for v in levels]
        else:
            # a number is a channel, for the radiances; a family on levels
            # takes it only when that level is in its data
            try:
                known = _layer_units(family) is None or float(c) in levels
            except ValueError:
                known = False
            if known:
                lv.append(c)
    # the layers of pressure or of height, one series each, beside CHANNEL
    # the layers of scatter: same edges, same rank, same label
    from pikobs.scatter.scatter import family_layers, _layer_display, _vcotyp
    for iv in family_layers(family, pressure_layers, height_layers)[1:]:
        lv.append(_layer_display(iv, _vcotyp(family)))
    word = "type" if family in ('ai', 'sf', 'ua', 'gp', 'csr') else "station"
    figs = []
    for sel in selectors:
        for region, flag, surface, special, varno in combos:
            for level in dict.fromkeys(lv):
                base = {'family': family, 'region': region, 'flag': flag,
                        'surface': surface, 'varno': varno, 'level': level,
                        'special': special,
                        'special_label': special_label(family, special),
                        'stn_sql': sel.sql(), 'stn_label': sel.display,
                        'stn_tag': sel.tag, 'member_word': word,
                        'cycles': cycles, 'pathwork': pathwork,
                        'datestart': datestart, 'dateend': dateend,
                        'svg': svg, 'alert_pct': alert_pct,
                        'pooled': sel.kind in ('join', 'prefix', 'like',
                                               'codtyp_group')}
                for name, _ in all_runs:
                    figs.append(dict(base, mode='run', name=name,
                                     db_file=dbs[name],
                                     control=control[0] if control else None))
                if control:
                    # off: each run with all of its own; on: the same
                    # observations; all: both, and the viewer switches
                    views = {'off': [False], 'on': [True],
                             'all': [False, True]}[str(match)]
                    for fn in functions:
                        for use_matched in views:
                            figs.append(dict(base, mode='all', function=fn,
                                             control=control[0],
                                             runs=[n for n, _ in all_runs],
                                             dbs=dbs, matched=use_matched))
    for f in figs:
        if f['mode'] == 'run':
            label = f['name']
        else:
            label = ("all runs, same observations" if f.get('matched')
                     else "all runs, each with its own")
        f['viewer'] = {'experience': label, 'family': family,
                       # one run draws O-P and O-A together: both
                       'fonction': ('*' if f['mode'] == 'run'
                                    else f['function']),
                       'region': f['region'], 'flag_criteria': f['flag'],
                       'land_ocean': f['surface'],
                       'special': f.get('special_label', 'all'),
                       'id_stn': f['stn_label'], 'varno': str(f['varno']),
                       # a layer in its own section, as in scatter
                       'layer': (f['level'] if _layer_bounds(f)
                                 else 'layer_all'),
                       'channel': ('join' if _layer_bounds(f)
                                   else f['level'])}
    return figs


# ─────────────────────────────────────────────────────────────────────────────
# Figures
# ─────────────────────────────────────────────────────────────────────────────

def _style(ax) -> None:
    """Common presentation style for all time-series panels."""
    ax.set_facecolor('#FCFCFC')
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#AEB4BA")
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(labelsize=11.5, colors="#333333", width=0.8, length=3.5)
    ax.grid(True, ls="--", lw=0.6, color="#AAB2B9", alpha=0.20)
    ax.set_axisbelow(True)
    ax.yaxis.label.set_size(12)
    ax.yaxis.label.set_color('#30343A')

def _dates(cycles):
    return np.array([datetime.strptime(c, '%Y%m%d%H') for c in cycles])


def members_text(spec, db, limit: int = 6) -> str:
    """'join -> GOES18, METOP-1, NOAA20 (+2 more)': a pooled selection
    should say what it pooled, not just that it pooled something."""
    label = str(spec['stn_label'])
    if not spec.get('pooled'):
        return label
    try:
        top, rest = read_by_station(spec, db, top=limit)
    except Exception:
        return label
    names = [str(n) for n, _, _ in top]
    if not names:
        return label
    more = f" (+{len(rest)} more)" if rest else ""
    return f"{label} -> {', '.join(names)}{more}"


def _header(fig, spec, head, extra: str = ""):
    """The header of every module, kept in inches from the top: the
    variable, the dates top right, a grey line with what the figure holds,
    the runs in their colours, a note, the rule."""
    var_name, units, _ = pikobs.type_varno(str(spec['varno']))
    try:
        channels = str(pikobs.family(spec['family'])[5]).strip().upper() \
            .startswith('CANAL')
    except Exception:
        channels = False
    if spec['level'] == 'join':
        lev = "all channels" if channels else "whole column"
    else:
        lev = f"{'channel' if channels else 'level'} {spec['level']}"
        if _layer_bounds(spec):
            lev = f"layer {spec['level']}"
    db = spec.get('db_file') or next(iter(spec.get('dbs', {}).values()), '')
    label, word = str(spec['stn_label']), spec['member_word']
    pooled = str(members_text(spec, db) if db else label)
    names = pooled.split(' -> ', 1)[1] if ' -> ' in pooled else ""
    who = f"all {word}s" if label == 'join' else f"{word} {label}"
    if names:
        who += f": {names}"

    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    parts = [spec['family'], spec['region'], f"flag {spec['flag']}"]
    if spec.get('surface', 'all') != 'all':
        parts.append(spec['surface'])
    sp = _sp_txt(spec).strip(" \u2022|,")
    if sp:
        parts.append(sp)
    parts.append(who)

    h = fig.get_figheight()

    def at(inch):
        return 1 - inch / h

    fig.text(0.055, at(0.12), f"{var_name} {units}  \u00b7  {lev}", ha='left',
             va='top', fontsize=17, fontweight='bold', color='#1F2933')
    fig.text(0.985, at(0.14), f"{_when(spec['datestart'])}  to  "
             f"{_when(spec['dateend'])}", ha='right', va='top', fontsize=12,
             color=_GREY)
    fig.text(0.055, at(0.47), "  \u00b7  ".join(parts), ha='left', va='top',
             fontsize=12, color=_GREY)
    # the runs in their colours, on one line
    if spec.get('mode') == 'all':
        ctl = spec['control']
        exps = [r for r in spec['runs'] if r != ctl]
        runs = [("Ctl", ctl, CTL_COLOUR)] + [
            ("Exp", r, EXP_COLOURS[i % len(EXP_COLOURS)])
            for i, r in enumerate(exps)]
    else:
        is_ctl = bool(spec.get('control')) and spec['name'] == spec['control']
        runs = [("Ctl" if is_ctl else "Exp", spec['name'],
                 CTL_COLOUR if is_ctl else EXP_COLOUR)]
    renderer = fig.canvas.get_renderer()
    x = 0.055
    for word_, name, colour in runs:
        t = fig.text(x, at(0.74), f"{word_}  {name}", ha='left', va='top',
                     fontsize=14, fontweight='bold', color=colour)
        box = t.get_window_extent(renderer=renderer)
        x = fig.transFigure.inverted().transform((box.x1, box.y0))[0] + 0.02
    note = str(extra or "").strip().replace("\n", "  \u00b7  ")
    if note:
        fig.text(0.055, at(1.0), note, ha='left', va='top', fontsize=12,
                 fontweight='semibold', color='#30343A')
    rule = at(1.24 if note else 1.0)
    fig.add_artist(mpl.lines.Line2D([0.055, 0.985], [rule, rule],
                                    transform=fig.transFigure,
                                    color='#D9DDE2', lw=0.9))
    return units

def _finish_x(ax, dates):
    loc = mdates.AutoDateLocator(minticks=5, maxticks=14)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
    ax.set_xlim(dates[0], dates[-1])
    ax.tick_params(axis='x', labelsize=11.5, pad=5)

def _lo_tag(spec) -> str:
    """The surface in a file name, only when there is a filter: the
    naming convention of every module."""
    lo = spec.get('surface', 'all')
    return '' if lo in (None, '', 'all') else f"_{_safe(lo)}"


def _out(spec, what) -> str:
    d = os.path.join(spec['pathwork'], spec['family'])
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"timeserie_{_safe(what)}_{spec['family']}_"
                           f"varno{_safe(spec['varno'])}_"
                           f"lev{_safe(spec['level'])}_"
                           f"{_safe(spec['stn_tag'])}_{_safe(spec['region'])}"
                           f"{_lo_tag(spec)}{_sp_tag(spec)}_"
                           f"{_safe(spec['flag'])}.png")


def _stack_combinations(ax, dates, by_sig: Dict[int, np.ndarray]):
    """Every flag combination, stacked: the ones that carry bit 12 in
    blues from light to dark, the others in their own colour."""
    order = sorted(by_sig, key=lambda k: -by_sig[k].sum())
    top, rest = order[:MAX_DIAGNOSES], order[MAX_DIAGNOSES:]
    total = sum(v.sum() for v in by_sig.values()) or 1.0
    used = [s for s in top if int(s) & 4096]
    blues = iter(QC_BLUES if len(used) <= len(QC_BLUES)
                 else [mpl.colormaps.get_cmap('Blues')(0.35 + 0.6 * i /
                                                       max(len(used) - 1, 1))
                       for i in range(len(used))])
    pal = iter(QC_PALETTE)
    bottom = np.zeros(len(dates))
    layers = [(s, by_sig[s]) for s in top]
    if rest:
        layers.append((None, sum(by_sig[s] for s in rest)))
    for sig, vals in layers:
        if sig is None:
            colour, label = QC_OTHER, f"{len(rest)} more"
        else:
            # the bits only: what each one means is in the key below
            colour = (next(blues, QC_ASSIMILATED) if int(sig) & 4096
                      else next(pal, '#666666'))
            label = _bits(sig)
        ax.fill_between(dates, bottom, bottom + vals, step='mid',
                        color=colour, alpha=0.9, lw=0,
                        label=f"{_pct(100 * vals.sum() / total):>7s}  "
                              f"{label}")
        bottom = bottom + vals
    ax.step(dates, bottom, where='mid', color='#333333', lw=1.0)
    return bottom


def _stack_members(ax, dates, by: Dict[str, np.ndarray], top_n: int = 12):
    """Every station -- or instrument type -- stacked, one colour each."""
    order = sorted(by, key=lambda k: -by[k].sum())
    total = sum(v.sum() for v in by.values()) or 1.0
    cmap = mpl.colormaps.get_cmap(STATION_CMAP)
    bottom = np.zeros(len(dates))
    layers = [(k, by[k]) for k in order[:top_n]]
    if order[top_n:]:
        layers.append((f"{len(order) - top_n} more",
                       sum(by[k] for k in order[top_n:])))
    for i, (name, vals) in enumerate(layers):
        colour = (QC_OTHER if name.endswith("more") and i == len(layers) - 1
                  and len(order) > top_n else cmap(i % 20))
        ax.fill_between(dates, bottom, bottom + vals, step='mid',
                        color=colour, alpha=0.9, lw=0,
                        label=f"{_pct(100 * vals.sum() / total):>7s}  "
                              f"{str(name)[:18]}")
        bottom = bottom + vals
    ax.step(dates, bottom, where='mid', color='#333333', lw=1.0)


def _bits_key(ax, combos: Dict[int, float], y_top: float,
              y_bottom: float) -> None:
    """Explain the active flag bits in a compact presentation card."""
    try:
        from pikobs.configobs.flag_groups import BIT_DESCRIPTIONS
    except Exception:                                      # pragma: no cover
        BIT_DESCRIPTIONS = {}

    used = sorted({
        b for sig in combos for b in range(24)
        if int(sig) >> b & 1
    })
    if not used:
        return

    lines = [
        f"{b:2d}   {BIT_DESCRIPTIONS.get(b, '')}"
        for b in used
    ]
    box = ax.get_window_extent()
    inches = max(y_top - y_bottom, 0.05) * box.height / ax.get_figure().dpi
    size = float(np.clip(inches * 72.0 / (1.45 * (len(lines) + 1)),
                         8.0, 11.5))

    ax.text(
        0.0, y_top, "BITS USED",
        transform=ax.transAxes, va='top',
        fontsize=min(size + 1.0, 12.5),
        fontweight='bold', color='#1F2933'
    )
    ax.text(
        0.0, y_top - 0.035, "\n".join(lines),
        transform=ax.transAxes, va='top',
        fontsize=size, family='monospace', color='#30343A',
        linespacing=1.35,
        bbox=dict(
            boxstyle='round,pad=0.55',
            fc='#F7F8FA', ec='#D1D5D9', lw=0.8
        )
    )

def _top_key(ax, handles, labels, title=None, ncol=None) -> None:
    """A key in one or two rows just above its panel."""
    if not handles:
        return
    ax.legend(handles, labels, loc='lower left', bbox_to_anchor=(0, 1.0),
              ncol=ncol or min(len(handles), 8),
              prop={'family': 'monospace', 'size': 10.5}, title=title,
              title_fontsize=11, alignment='left', frameon=False,
              borderaxespad=0.25, columnspacing=1.8, handlelength=1.6)


def _bits_line(fig, combos, y) -> None:
    """The meaning of every bit that appears, on a line under the figure."""
    try:
        from pikobs.configobs.flag_groups import BIT_DESCRIPTIONS
    except Exception:                                      # pragma: no cover
        BIT_DESCRIPTIONS = {}
    used = sorted({b for sig in combos for b in range(24) if int(sig) >> b & 1})
    if not used:
        return
    fig.text(0.055, y, "BITS   " + "   \u00b7   ".join(
        f"{b} {BIT_DESCRIPTIONS.get(b, '')}".strip() for b in used),
        fontsize=10.5, color='#30343A', va='bottom', wrap=True)


def _run_figure(spec) -> Optional[Tuple[str, list]]:
    cycles, by, assim, combos = read_counts(spec, spec['db_file'])
    if not by or sum(v.sum() for v in by.values()) == 0:
        return None
    vals = read_values(spec, spec['db_file'])
    dates = _dates(cycles)
    has_mean = vals is not None and (np.any(np.isfinite(vals['m_omp']))
                                     or np.any(np.isfinite(vals['m_bc'])))
    has_sigma = vals is not None and (np.any(np.isfinite(vals['s_omp']))
                                       or np.any(np.isfinite(vals['m_err'])))
    # one panel more when the selection pools several stations or types:
    # who brings the observations, cycle by cycle
    members = (read_counts_by_member(spec, spec['db_file'])
               if spec.get('pooled') else {})
    if len(members) < 2:
        members = {}
    n_rows = 1 + bool(members) + has_mean + has_sigma
    heights = ([2.4, 1.75] if members else [2.45]) + [1.45] * (
        n_rows - 1 - bool(members)
    )
    # no column on the right: the keys sit above their panels
    fig_h = 5.9 + 2.75 * n_rows
    fig = plt.figure(figsize=(22, fig_h), facecolor='white')
    gs = fig.add_gridspec(
        n_rows, 1,
        height_ratios=heights,
        hspace=0.45,
        left=0.055,
        right=0.985,
        top=1 - 2.05 / fig_h,
        bottom=1.3 / fig_h,
    )
    ax0 = fig.add_subplot(gs[0, 0])
    axes = [ax0] + [fig.add_subplot(gs[i, 0], sharex=ax0)
                    for i in range(1, n_rows)]
    for ax in axes:
        _style(ax)
    total = _stack_combinations(ax0, dates, by)
    ax0.set_ylabel(
        "observations per cycle\nby flag combination",
        fontsize=12.5, fontweight='semibold'
    )
    fmt_k = mpl.ticker.FuncFormatter(
        lambda v, _: f"{v / 1000:g}k" if v >= 1000 else f"{v:g}")
    ax0.yaxis.set_major_formatter(fmt_k)
    ax_m = None
    if members:
        ax_m = axes[1]
        _stack_members(ax_m, dates, members)
        ax_m.set_ylabel("by " + ('type' if _member_key(
            spec, spec['db_file']) == 'codtyp' else 'station'))
        ax_m.yaxis.set_major_formatter(fmt_k)

    alerts = []
    for i, n, med, drop in alerts_of(total, cycles, spec['alert_pct']):
        ax0.scatter(
            [dates[i]], [n], marker='v', s=78,
            color='#202428', edgecolor='white', linewidth=0.5, zorder=6
        )
        alerts.append([spec['name'], spec['family'], spec['region'],
                       spec['flag'], spec['stn_label'], spec['varno'],
                       spec['level'], cycles[i], int(n), int(med),
                       f"{drop:.1f}"])

    units = _header(fig, spec, spec['name'])
    # the run in its colour: red for an experience, blue for the control
    rc = CTL_COLOUR if spec.get('control') and spec['name'] == spec['control'] \
        else EXP_COLOUR
    row = 1 + bool(members)
    style_keys = []
    if has_mean:
        ax = axes[row]
        if np.any(np.isfinite(vals['m_omp'])):
            ax.plot(dates, vals['m_omp'], '-', color=rc, lw=2.0)
            style_keys.append(("-", "O-P", '#333333'))
        if np.any(np.isfinite(vals['m_oma'])):
            ax.plot(dates, vals['m_oma'], '--', color=rc, lw=1.6)
            style_keys.append(("--", "O-A", '#333333'))
        if np.any(np.isfinite(vals['m_bc'])):
            ax.plot(dates, vals['m_bc'], ':', color='#8C510A', lw=1.8)
            style_keys.append((":", "bias correction", '#8C510A'))
        ax.axhline(0, color='#444444', ls=':', lw=0.9)
        ax.set_ylabel(f"mean  {units}")
        row += 1
    if has_sigma:
        ax = axes[row]
        if np.any(np.isfinite(vals['s_omp'])):
            ax.plot(dates, vals['s_omp'], '-', color=rc, lw=2.0)
        if np.any(np.isfinite(vals['s_oma'])):
            ax.plot(dates, vals['s_oma'], '--', color=rc, lw=1.6)
        if np.any(np.isfinite(vals['m_err'])):
            ax.plot(dates, vals['m_err'], color='#4B5563', lw=2.2,
                    ls=(0, (1, 1.6)))
            style_keys.append((":", "OBS_ERROR used in the assimilation",
                               '#4B5563'))
        ax.set_ylabel(f"sigma  {units}")
        ax.set_ylim(bottom=0)
    for ax in axes[:-1]:
        ax.tick_params(axis='x', labelbottom=False)
    _finish_x(axes[-1], dates)

    # the keys, above the panels they explain: every panel the whole width
    h, l = ax0.get_legend_handles_labels()
    _top_key(ax0, h, l, "FLAG COMBINATIONS (bits)  --  blue = entered the "
             "analysis (bit 12)")
    if ax_m is not None:
        hm, lm = ax_m.get_legend_handles_labels()
        _top_key(ax_m, hm, lm, "by " + ('type' if _member_key(
            spec, spec['db_file']) == 'codtyp' else 'station'))
    if style_keys:
        _top_key(axes[1 + bool(members)],
                 [mpl.lines.Line2D([0], [0], color=c, ls=s, lw=1.6)
                  for s, t, c in style_keys],
                 [t for s, t, c in style_keys], "DEPARTURES")
    else:
        fig.text(0.985, 0.62 / fig_h, "no departures in the files: counts only",
                 ha='right', va='bottom', fontsize=10.5, color=_GREY)
    _bits_line(fig, combos, 0.62 / fig_h)
    if alerts:
        fig.text(0.055, 0.22 / fig_h,
                 f"v  {len(alerts)} cycle(s) more than {spec['alert_pct']:g} % "
                 f"below the median of the same hour on the days before",
                 fontsize=10.5, color='#202428', va='bottom',
                 bbox=dict(boxstyle='round,pad=0.35', fc='#FFF8E6',
                           ec='#E5C56A'))
    out = _out(spec, spec['name'])
    save_figure(fig, out, svg=spec.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out, alerts


def _units_of(spec) -> str:
    try:
        _, units, _ = pikobs.type_varno(str(spec['varno']))
        return str(units)
    except Exception:                                      # pragma: no cover
        return ""


def _run_values(ax, parts) -> None:
    """One line above a panel, each run in its colour, as in cardio:
    'Ctl name: sigma 2.529  .  Exp name: sigma 2.534'."""
    renderer = ax.figure.canvas.get_renderer()
    x = 0.0

    def put(text, colour, weight):
        t = ax.text(x, 1.03, text, transform=ax.transAxes, fontsize=11.5,
                    fontweight=weight, color=colour, va='bottom')
        box = t.get_window_extent(renderer=renderer)
        return ax.transAxes.inverted().transform((box.x1, box.y0))[0]

    for k, (text, colour) in enumerate(parts):
        if k:
            x = put("   \u00b7   ", '#6B7280', 'normal')
        x = put(text, colour, 'semibold')


def _all_figure(spec) -> Optional[Tuple[str, list]]:
    """Draw the control/experience comparison figure.

    The panels are deliberately organised in pairs so that every time series
    is immediately followed by its difference with respect to the control:

        observations
        assimilated difference
        mean O-P
        mean O-P difference
        sigma O-P
        sigma O-P difference

    This makes the comparison much easier to read than putting both
    difference panels at the bottom of the figure.
    """
    runs = spec['runs']
    fn = spec.get('function', 'omp')           # O-P or O-A
    MK, SK = f"m_{fn}", f"s_{fn}"
    FN = {'omp': 'O-P', 'oma': 'O-A'}[fn]
    colours = {runs[0]: CTL_COLOUR}

    # The control is drawn solid and every experience dashed.  Where two
    # curves agree, different line styles keep both runs identifiable.
    styles = {runs[0]: '-'}
    dashes = ['--', '-.', (0, (3, 1, 1, 1, 1, 1)), ':']
    for i, r in enumerate(runs[1:]):
        colours[r] = EXP_COLOURS[i % len(EXP_COLOURS)]
        styles[r] = dashes[i % len(dashes)]

    data, matched = {}, {}
    for r in runs:
        cycles, by, assim, _ = read_counts(spec, spec['dbs'][r])
        if not by:
            continue

        total = sum(by.values())
        data[r] = (total, assim, read_values(spec, spec['dbs'][r]))

        if r != spec['control'] and spec.get('matched'):
            m = read_matched(spec, spec['dbs'][r])
            if m is not None:
                matched[r] = m

    ctl = spec['control']
    if ctl not in data or len(data) < 2:
        return None

    dates = _dates(spec['cycles'])
    has_vals = any(
        v[2] is not None and np.any(np.isfinite(v[2][MK]))
        for v in data.values()
    )

    # Panel order:
    #   0 observations
    #   1 assimilated difference
    #   2 mean O-P
    #   3 mean O-P difference
    #   4 sigma O-P
    #   5 sigma O-P difference
    #
    # If the files do not contain departure statistics, only the first two
    # panels are produced.
    n_rows = 6 if has_vals else 2
    height_ratios = (
        [2.35, 0.95, 1.55, 0.95, 1.55, 0.95]
        if has_vals else
        [2.35, 0.95]
    )

    # Keep the comparison figure compact enough that a browser does not
    # shrink the whole image excessively.  The previous 22-inch canvas made
    # the text look small once the PNG was fitted to the viewer width.
    # A narrower canvas + larger fonts gives substantially better on-screen
    # readability while preserving enough vertical room for the six panels.
    fig_w = 18.0
    # the runs above the first panel, the numbers above their panels
    fig_h = (15.8 if has_vals else 7.6) + 0.5
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor='white')
    gs = fig.add_gridspec(
        n_rows, 1,
        height_ratios=height_ratios,
        hspace=0.25,
        left=0.09,
        right=0.985,
        top=1 - 1.95 / fig_h,
        bottom=0.9 / fig_h,
    )

    ax_obs = fig.add_subplot(gs[0, 0])
    axes = [ax_obs] + [
        fig.add_subplot(gs[i, 0], sharex=ax_obs)
        for i in range(1, n_rows)
    ]

    ax_obs_diff = axes[1]
    if has_vals:
        ax_mean = axes[2]
        ax_mean_diff = axes[3]
        ax_sigma = axes[4]
        ax_sigma_diff = axes[5]
    else:
        ax_mean = ax_mean_diff = ax_sigma = ax_sigma_diff = None

    for ax in axes:
        _style(ax)
        # Comparison figures need to remain readable after the PNG is scaled
        # in the web viewer.  Use larger tick/axis text than the single-run
        # figures and slightly heavier axes/lines.
        ax.tick_params(axis='both', labelsize=13.0, width=0.9, length=4.0)
        ax.yaxis.label.set_size(13.5)
        ax.yaxis.labelpad = 12
        for side in ("left", "bottom"):
            ax.spines[side].set_linewidth(0.9)

    # ------------------------------------------------------------------
    # 1) Observations + observation difference directly underneath
    # ------------------------------------------------------------------
    for r, (total, assim, vals) in data.items():
        # The colour identifies the run.  The thick line is assimilated
        # observations; the thin/pale line is all observations.
        if np.any(total > assim):
            ax_obs.step(
                dates, total, where='mid',
                color=colours[r], lw=1.65,
                ls=styles[r], alpha=0.42
            )

        ax_obs.step(
            dates, assim, where='mid',
            color=colours[r], lw=2.75,
            ls=styles[r]
        )

        if r != ctl:
            diff = assim - data[ctl][1]
            ok = np.isfinite(diff)
            ax_obs_diff.bar(
                dates[ok], diff[ok], width=0.20,
                color=np.where(diff[ok] >= 0, colours[r], CTL_COLOUR),
                alpha=0.75,
                zorder=3,
            )

        if has_vals and vals is not None:
            # Every run is always drawn with all of its own observations.
            # MATCH changes the statistical test used for the bars below,
            # not the curves themselves.
            ax_mean.plot(
                dates, vals[MK],
                ls=styles[r], color=colours[r], lw=2.35
            )
            ax_sigma.plot(
                dates, vals[SK],
                ls=styles[r], color=colours[r], lw=2.35
            )

    ax_obs.set_ylabel(
        "observations per cycle",
        fontsize=14.0, fontweight='semibold', labelpad=13
    )
    ax_obs.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(
        lambda v, _: f"{v / 1000:g}k" if v >= 1000 else f"{v:g}"
    ))

    ax_obs_diff.axhline(0, color='#333333', lw=0.9)
    ax_obs_diff.set_ylabel(
        "assimilated\nExp - Ctl",
        fontsize=13.5, labelpad=12
    )

    # ------------------------------------------------------------------
    # 2) Mean O-P + mean difference directly underneath
    # 3) Sigma O-P + sigma difference directly underneath
    # ------------------------------------------------------------------
    units_label = _units_of(spec)
    exps = [r for r in data if r != ctl]

    if has_vals:
        width = 0.20 / max(len(exps), 1)

        for k, r in enumerate(exps):
            v_c = data[ctl][2]
            v_e = data[r][2]
            if v_c is None or v_e is None:
                continue

            m = matched.get(r)

            # Several experiences are put side by side.  Width/offset are in
            # Matplotlib date units (days), hence timedelta(days=off).
            off = (k - (len(exps) - 1) / 2) * width
            x = np.array([d + timedelta(days=off) for d in dates])

            mean_vals = v_e[MK] - v_c[MK]
            sigma_vals = v_e[SK] - v_c[SK]

            mean_better = np.abs(v_e[MK]) < np.abs(v_c[MK])
            sigma_better = v_e[SK] < v_c[SK]

            mean_conf = None if m is None else m['t_conf']
            sigma_conf = None if m is None else m['f_conf']

            for ax, vals, better, conf in (
                (ax_mean_diff, mean_vals, mean_better, mean_conf),
                (ax_sigma_diff, sigma_vals, sigma_better, sigma_conf),
            ):
                bar_colour = np.where(better, colours[r], CTL_COLOUR)
                sig = (
                    is_significant(np.nan_to_num(conf))
                    if conf is not None
                    else np.zeros(len(dates), bool)
                )
                ok = np.isfinite(vals)

                # Filled = statistically significant when MATCH is available.
                ax.bar(
                    x[sig & ok], vals[sig & ok],
                    width=width,
                    color=bar_colour[sig & ok],
                    zorder=3,
                )

                # Pale = not significant, or MATCH=off.
                ax.bar(
                    x[~sig & ok], vals[~sig & ok],
                    width=width,
                    color=bar_colour[~sig & ok],
                    alpha=0.25,
                    zorder=2,
                )

        who = exps[0] if len(exps) == 1 else "experience"

        # Main series and its difference are adjacent by construction.
        ax_mean.axhline(0, color='#444444', ls=':', lw=0.9)
        ax_mean.set_ylabel(f"mean {FN}  {units_label}", fontsize=13.5, labelpad=12)
        ax_mean_diff.axhline(0, color='#333333', lw=1.0)
        ax_mean_diff.set_ylabel(
            f"mean: Exp - Ctl\n{units_label}",
            fontsize=13.5, labelpad=12
        )

        ax_sigma.set_ylabel(f"sigma {FN}  {units_label}", fontsize=13.5, labelpad=12)
        ax_sigma.set_ylim(bottom=0)
        ax_sigma_diff.axhline(0, color='#333333', lw=1.0)
        ax_sigma_diff.set_ylabel(
            f"sigma: Exp - Ctl\n{units_label}",
            fontsize=13.5, labelpad=12
        )

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------
    head = f"all runs against {ctl}"
    units = _header(
        fig, spec, head,
        ("MATCH on: the same observations in both runs, the change of "
         "each cycle tested pair by pair" if spec.get('matched') else
         "MATCH off: each run with all its observations; the change is "
         "shown, not tested")
    )

    # _header() is also the authoritative source of the display units.  Keep
    # the labels in sync with it in case type_varno() returns a prettier unit.
    if has_vals:
        ax_mean.set_ylabel(f"mean {FN}  {units}", fontsize=13.5, labelpad=12)
        ax_mean_diff.set_ylabel(
            f"mean: Exp - Ctl\n{units}", fontsize=13.5, labelpad=12
        )
        ax_sigma.set_ylabel(f"sigma {FN}  {units}", fontsize=13.5, labelpad=12)
        ax_sigma_diff.set_ylabel(
            f"sigma: Exp - Ctl\n{units}", fontsize=13.5, labelpad=12
        )

    # Only the bottom panel carries date labels; all panels still share x.
    for ax in axes[:-1]:
        ax.tick_params(axis='x', labelbottom=False)
    _finish_x(axes[-1], dates)
    axes[-1].tick_params(axis='x', labelsize=13.0, pad=6)

    # ------------------------------------------------------------------
    # Right-side key / legend
    # ------------------------------------------------------------------
    handles = [
        mpl.lines.Line2D(
            [0], [0], color=colours[r], lw=2.0,
            ls=styles[r], label=r
        )
        for r in data
    ]
    handles += [
        mpl.lines.Line2D(
            [0], [0], color='#555555', lw=2.0,
            label="assimilated (bit 12)"
        ),
        mpl.lines.Line2D(
            [0], [0], color='#555555', lw=1.1,
            alpha=0.45, label="all observations"
        ),
    ]
    handles.append(mpl.patches.Patch(
        facecolor='#555555',
        label=(
            f"filled: paired test above {MIN_CONFIDENCE:.0f} %"
            if matched else
            "MATCH=off: no test"
        )
    ))
    handles.append(mpl.patches.Patch(
        facecolor='#555555', alpha=0.25,
        label="pale: not significant"
    ))

    ax_obs.legend(handles=handles, loc='lower left', bbox_to_anchor=(0, 1.0),
                  ncol=len(handles), fontsize=11, frameon=False,
                  borderaxespad=0.25, columnspacing=1.8)

    # ------------------------------------------------------------------
    # Period summary
    # ------------------------------------------------------------------
    # ---- the numbers of the period, each above the panel it is about -----
    role = {r: ('Ctl' if r == ctl else 'Exp') for r in data}
    per_run = {}
    for r, (total, assim, vals) in data.items():
        if vals is not None and np.any(np.isfinite(vals[MK])):
            per_run[r] = (float(np.nanmean(vals[MK])),
                          float(np.nanmean(vals[SK])))
    # above the change of the counts: what each run assimilated, and how
    # much of the data they share
    parts = [(f"{role[r]} {r}: {int(np.nansum(v[1])):,} assimilated",
              colours[r]) for r, v in data.items()]
    for r in data:
        if r == ctl:
            continue
        sh = read_shared(dict(spec, db_file=spec['dbs'][r]), spec['dbs'][r])
        if sh:
            both, only_c, only_e = sh
            tot = both + only_c + only_e
            parts.append((f"{'' if len(data) == 2 else r + ' '}shares "
                          f"{100 * both / tot:.1f} % (only Ctl "
                          f"{100 * only_c / tot:.1f} %, only Exp "
                          f"{100 * only_e / tot:.1f} %)", '#30343A'))
    _run_values(ax_obs_diff, parts)
    if has_vals and per_run:
        _run_values(ax_mean, [(f"{role[r]} {r}: bias {v[0]:+.3f}", colours[r])
                              for r, v in per_run.items()])
        _run_values(ax_sigma, [(f"{role[r]} {r}: sigma {v[1]:.3f}", colours[r])
                               for r, v in per_run.items()])
        c_m, c_s = per_run.get(ctl, (float('nan'), float('nan')))
        ctl_vals = data[ctl][2]
        mean_parts, sigma_parts = [], []
        for r, (total, assim, vals) in data.items():
            if r == ctl or r not in per_run or ctl_vals is None:
                continue
            m, sd = per_run[r]
            tag = "" if len(data) == 2 else f"{r}: "
            d_bias = (abs(m) - abs(c_m)) / abs(c_m) * 100 if c_m else float('nan')
            d_spr = (sd - c_s) / c_s * 100 if c_s else float('nan')
            ok = np.isfinite(vals[SK]) & np.isfinite(ctl_vals[SK])
            narrower = int(np.sum(vals[SK][ok] < ctl_vals[SK][ok]))
            mean_parts.append((f"{tag}|bias| Exp against Ctl {d_bias:+.1f} %",
                               '#30343A'))
            sigma_parts.append((f"{tag}sigma Exp against Ctl {d_spr:+.1f} %, "
                                f"narrower in {narrower}/{int(ok.sum())} cycles",
                                '#30343A'))
            mm = matched.get(r)
            if mm is not None:
                t_ok = is_significant(np.nan_to_num(mm['t_conf']))
                f_ok = is_significant(np.nan_to_num(mm['f_conf']))
                n_cyc = int(np.sum(np.isfinite(mm['n'])))
                closer = np.abs(mm['me']) < np.abs(mm['mc'])
                mean_parts.append((
                    f"same observations: bias "
                    f"{float(np.nanmean(np.abs(mm['me']) - np.abs(mm['mc']))):+.4f}, "
                    f"the test passes in {int(np.sum(t_ok & closer))}/{n_cyc} "
                    f"cycles for Exp, {int(np.sum(t_ok & ~closer))} for Ctl",
                    '#30343A'))
                narrow = mm['se'] < mm['sc']
                sigma_parts.append((
                    f"same observations: "
                    f"{float(np.nanmean(100 * (mm['se'] - mm['sc']) / mm['sc'])):+.1f} %, "
                    f"the test passes in {int(np.sum(f_ok & narrow))}/{n_cyc} "
                    f"for Exp, {int(np.sum(f_ok & ~narrow))} for Ctl", '#30343A'))
        if not matched:
            mean_parts.append(("each run with all its own observations; "
                               "MATCH on adds the paired test", _GREY))
        _run_values(ax_mean_diff, mean_parts)
        _run_values(ax_sigma_diff, sigma_parts)

    out = _out(spec, f"all_vs_{ctl}" + ("" if fn == 'omp' else f"_{fn}"))
    save_figure(fig, out, svg=spec.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out, []

def plot_task(spec: Dict[str, Any]):
    import traceback
    try:
        with plt.rc_context(_STYLE):
            if spec['mode'] == 'all':
                return _all_figure(spec)
            return _run_figure(spec)
    except Exception:
        print(f"[timeserie] plot failed for {spec.get('family')} "
              f"{spec.get('stn_label')} {spec.get('mode')}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        plt.close('all')
        return None

