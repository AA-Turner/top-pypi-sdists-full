#!/usr/bin/python3
"""Figures of pikobs.profile.

For every run, the same panels on the same axes: the number of
observations, the bias and the sigma with the assigned error and what
the system expects from it, and their ratio. With a control, one more
figure per experience: the change of the bias and of the sigma, level
by level, with the tests of pikobs.stats -- red where the experience is
better, blue where the control is, hollow where it is noise.

Radar draws one line per antenna elevation, each with the same colour in
every figure, against the slant range or the beam height.
"""

import os
import re
import sys
from typing import Any, Dict, List, Optional

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import pikobs
from pikobs.figures import save_figure
from pikobs.configobs.special_family import special_label
from pikobs.obsdb import open_result
from pikobs.stats import (MIN_CONFIDENCE, is_significant,
                          paired_ttest_confidence, sigma_confidence,
                          ttest_confidence)

from pikobs.configobs.style import (CTL_BETTER, CTL_COLOUR, DPI, EXP_BETTER,
                                    EXP_COLOUR, GREY_TEXT as _GREY,
                                    NEUTRAL as EXPECTED_COLOUR)
_STYLE = {"font.family": "DejaVu Sans", "axes.labelsize": 10,
          "legend.fontsize": 8.5}
_FN = {'omp': 'O-P', 'oma': 'O-A'}


def _safe(text) -> str:
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


# ─────────────────────────────────────────────────────────────────────────────
# Reading
# ─────────────────────────────────────────────────────────────────────────────

def _extra(spec) -> str:
    """The surface and the special value in a file name, only when they
    split something: with all the name is the one it always was."""
    return "".join(f"_{_safe(x)}" for x in (spec.get('surface', 'all'),
                                             spec.get('special_label', 'all'))
                   if x not in (None, '', 'all'))


def _extra_txt(spec) -> str:
    """The same in a title: ', land', ', IR channel'."""
    return "".join(f", {x}" for x in (spec.get('surface', 'all'),
                                       spec.get('special_label', 'all'))
                   if x not in (None, '', 'all'))


def _where(spec) -> tuple:
    w = ("region = ? AND flag = ? AND land_ocean = ? AND special = ? "
         "AND varno = ?" + spec['stn_sql'])
    args = [spec['region'], spec['flag'], spec.get('surface', 'all'),
            spec.get('special', 'all'), spec['varno']]
    if spec['radar'] and spec['elevation'] != 'join':
        w += " AND elev = ?"
        args.append(spec['elevation'])
    return w, args


def _axis_col(spec) -> str:
    return 'hgt' if spec['radar'] and spec['yaxis'] == 'height' else 'lev'


def read_run(spec) -> Dict[str, Dict[str, np.ndarray]]:
    """{elevation: arrays per level} of one run; 'na' when not radar."""
    fn = spec['function']
    where, args = _where(spec)
    col = _axis_col(spec)
    sel_e = "elev" if spec['radar'] else "'na'"
    with open_result(spec['db_file']) as conn:
        rows = conn.execute(
            f"SELECT {sel_e}, {col}, SUM(n_{fn}), SUM(s_{fn}), SUM(s2_{fn}), "
            f"SUM(n_err), SUM(s_err), SUM(s2_err), SUM(n_fg), SUM(s_fg2), "
            f"SUM(n_da), SUM(s_pa), SUM(s_pd), SUM(s_ad) "
            f"FROM prof WHERE {where} AND {col} IS NOT NULL "
            f"GROUP BY 1, 2 ORDER BY 1, 2;", args).fetchall()
    out: Dict[str, Dict[str, list]] = {}
    from pikobs.profile.profile import desroziers
    for e, lev, n, s, s2, ne, se, s2e, nf, sf2, nda, spa, spd, sad in rows:
        if not n:
            continue
        d = out.setdefault(str(e), {k: [] for k in
                                    ('lev', 'n', 'mean', 'std', 'oer',
                                     'expected', 'des')})
        d['des'].append(desroziers(nda, spa, spd, sad) if fn == 'omp'
                        else np.nan)
        mean = s / n
        d['lev'].append(float(lev))
        d['n'].append(float(n))
        d['mean'].append(mean)
        d['std'].append(max(s2 / n - mean * mean, 0.0) ** 0.5)
        d['oer'].append(se / ne if ne else np.nan)
        # what the sigma of O-P should be if the errors are right:
        # sqrt(sigma_o^2 + sigma_b^2), as root mean squares
        if ne and nf and fn == 'omp':
            d['expected'].append((s2e / ne + sf2 / nf) ** 0.5)
        elif ne and fn == 'omp':
            d['expected'].append(np.nan)
        else:
            d['expected'].append(np.nan)
    return {e: {k: np.asarray(v, float) for k, v in d.items()}
            for e, d in out.items()}


def _has_pair(db_file) -> bool:
    """True when the database holds the pairs of MATCH=on."""
    if not db_file or not os.path.isfile(db_file):
        return False
    try:
        with open_result(db_file) as conn:
            return bool(conn.execute(
                "SELECT 1 FROM sqlite_master WHERE name = 'pair'").fetchone())
    except Exception:
        return False


def _read_unmatched(spec) -> Dict[str, Dict[str, np.ndarray]]:
    """MATCH=off: each run with all its observations, compared level by
    level on the levels both have; Welch on the mean, F on the sigma."""
    spec['unmatched'] = True
    fn = spec['function']
    where, args = _where(spec)
    col = _axis_col(spec)
    sel_e = "elev" if spec['radar'] else "'na'"
    sides = []
    for db in (spec['db_ctl'], spec['db_exp']):
        with open_result(db) as conn:
            rows = conn.execute(
                f"SELECT {sel_e}, {col}, SUM(n_{fn}), SUM(s_{fn}), SUM(s2_{fn}) "
                f"FROM prof WHERE {where} AND {col} IS NOT NULL "
                f"GROUP BY 1, 2;", args).fetchall()
        sides.append({(str(e), float(lev)): (n, s, s2)
                      for e, lev, n, s, s2 in rows if n})
    out: Dict[str, Dict[str, list]] = {}
    for key in sorted(set(sides[0]) & set(sides[1])):
        e, lev = key
        (nc, sc, s2c), (ne, se, s2e) = sides[0][key], sides[1][key]
        mc, me = sc / nc, se / ne
        d = out.setdefault(e, {k: [] for k in ('lev', 'n', 'n_c', 'n_e', 'mc',
                                               'me', 'sc', 'se', 'cov')})
        d['lev'].append(lev)
        d['n'].append(float(min(nc, ne)))
        d['n_c'].append(float(nc))
        d['n_e'].append(float(ne))
        d['mc'].append(mc)
        d['me'].append(me)
        d['sc'].append(max(s2c / nc - mc * mc, 0.0) ** 0.5)
        d['se'].append(max(s2e / ne - me * me, 0.0) ** 0.5)
        d['cov'].append(np.nan)
    res = {}
    for e, d in out.items():
        a = {k: np.asarray(v, float) for k, v in d.items()}
        a['t_conf'] = ttest_confidence(a['mc'], a['sc'], a['n_c'],
                                       a['me'], a['se'], a['n_e'])
        a['f_conf'] = sigma_confidence(a['sc'] ** 2, a['se'] ** 2, a['n_c'],
                                       a['n_e'])
        res[e] = a
    return res


def read_diff(spec) -> Dict[str, Dict[str, np.ndarray]]:
    """{elevation: arrays per level} of the matched runs, with the tests."""
    if not _has_pair(spec.get('db_file')) and spec.get('db_ctl'):
        return _read_unmatched(spec)
    fn = spec['function']
    n_col = 'n' if fn == 'omp' else 'n_a'
    where, args = _where(spec)
    col = _axis_col(spec)
    sel_e = "elev" if spec['radar'] else "'na'"
    with open_result(spec['db_file']) as conn:
        rows = conn.execute(
            f"SELECT {sel_e}, {col}, SUM({n_col}), SUM(c_{fn}), SUM(c2_{fn}), "
            f"SUM(e_{fn}), SUM(e2_{fn}), SUM(ce_{fn}) FROM pair "
            f"WHERE {where} AND {col} IS NOT NULL "
            f"GROUP BY 1, 2 ORDER BY 1, 2;", args).fetchall()
    out: Dict[str, Dict[str, list]] = {}
    for e, lev, n, c, c2, x, x2, cx in rows:
        if not n:
            continue
        d = out.setdefault(str(e), {k: [] for k in
                                    ('lev', 'n', 'mc', 'me', 'sc', 'se',
                                     'cov')})
        mc, me = c / n, x / n
        d['lev'].append(float(lev))
        d['n'].append(float(n))
        d['mc'].append(mc)
        d['me'].append(me)
        d['sc'].append(max(c2 / n - mc * mc, 0.0) ** 0.5)
        d['se'].append(max(x2 / n - me * me, 0.0) ** 0.5)
        d['cov'].append(cx / n - mc * me)
    res = {}
    for e, d in out.items():
        a = {k: np.asarray(v, float) for k, v in d.items()}
        a['t_conf'] = paired_ttest_confidence(a['mc'], a['me'], a['sc'] ** 2,
                                              a['se'] ** 2, a['cov'], a['n'])
        # the sigma: Pitman-Morgan, with the covariance of the pairs
        a['f_conf'] = sigma_confidence(a['sc'] ** 2, a['se'] ** 2, a['n'],
                                       cov=a['cov'])
        res[e] = a
    return res


# In the figure of every elevation, an elevation with less than this share
# of the observations of the selection is hidden: a short, noisy line that
# covers the ones that matter. It keeps its own figure.
MIN_ELEVATION_SHARE = 0.01
# the radar always on the same frame, whatever the data
RADAR_MAX_HEIGHT_KM = 14.0
# the error curves of a run figure, each in its own colour
OER_COLOUR = '#4B5563'        # OBS_ERROR used in the assimilation
DES_COLOUR = '#2CA02C'        # Desroziers
MODEL_COLOUR = '#111111'      # error model (radar_obs_error)
FIT_COLOUR = '#E69F00'        # fitted on this run (FIT_RADAR)
RADAR_MAX_RANGE_KM = 250.0


def _drop_rare_elevations(data: Dict[str, Dict[str, np.ndarray]]):
    """(kept, number hidden) for the figure of every elevation."""
    if len(data) <= 1:
        return data, 0
    total = sum(float(d['n'].sum()) for d in data.values())
    kept = {e: d for e, d in data.items()
            if float(d['n'].sum()) >= MIN_ELEVATION_SHARE * total}
    return kept, len(data) - len(kept)


def _elevation_legend(ax, handles, title, hidden):
    """The elevation key under the other keys, in two columns if long."""
    if not handles:
        return
    if hidden:
        title += f"\n{hidden} with < {MIN_ELEVATION_SHARE:.0%} of the " \
                 f"observations hidden\n(each has its own figure)"
    ax.legend(handles=handles, loc='lower left', bbox_to_anchor=(0, 0),
              fontsize=9.5 if len(handles) > 12 else 10,
              ncol=2 if len(handles) > 12 else 1, columnspacing=0.8,
              handlelength=1.4, title=title, title_fontsize=10,
              frameon=True, edgecolor='#DDDDDD')


def _keep(d, min_obs):
    """Drop the levels resting on too few observations, and those where
    the departure is the same number everywhere."""
    std = d['std'] if 'std' in d else d['sc']
    ok = (d['n'] >= min_obs) & (std > 0)
    return {k: (v[ok] if hasattr(v, '__len__') and len(v) == len(ok) else v)
            for k, v in d.items()}


# ─────────────────────────────────────────────────────────────────────────────
# Planning: which figures, and their shared axes
# ─────────────────────────────────────────────────────────────────────────────

def _distinct(db_file, sql) -> List[tuple]:
    try:
        with open_result(db_file) as conn:
            return conn.execute(sql).fetchall()
    except Exception:
        return []


def elevation_colours(elevations) -> Dict[str, Any]:
    """The same colour for an elevation in every figure of a family."""
    vals = sorted({e for e in elevations if e not in ('na', 'join')},
                  key=float)
    cmap = mpl.colormaps.get_cmap('tab20' if len(vals) <= 20
                                  else 'nipy_spectral')
    return {e: cmap(i / max(len(vals) - 1, 1)) for i, e in enumerate(vals)}


def _network(sel) -> Optional[str]:
    """The radar network of a selection (C, U ...), or None if it mixes
    networks or cannot be told."""
    value = str(sel.value or '')
    if sel.kind in ('station', 'exact', 'prefix'):
        return value[:1].upper() or None
    if sel.kind == 'like' and value[:1] not in ('%', '_', ''):
        return value[:1].upper()
    return None


def plan_figures(family, all_runs, control, runs, selectors, regions, flags,
                 functions, pathwork, datestart, dateend, db_path, radar,
                 min_obs, svg, obs_error_model) -> List[Dict[str, Any]]:
    _, _, _, _, _, vcotyp = pikobs.family(family)
    figs = []
    run_dbs = {n: db_path(pathwork, family, n, datestart, dateend)
               for n, _ in all_runs}
    elevations = sorted({str(r[0]) for db in run_dbs.values()
                         for r in _distinct(db, "SELECT DISTINCT elev FROM "
                                                "prof;")} - {'na'},
                        key=lambda e: float(e)) if radar else []
    colours = elevation_colours(elevations)
    word = "type" if family in ('ai', 'sf', 'ua', 'gp', 'csr') else "station"

    def base(sel, region, flag, varno, fn, elevation, yaxis,
             surface='all', special='all'):
        return {'family': family, 'vcotyp': str(vcotyp), 'radar': radar,
                'stn_sql': sel.sql(), 'stn_label': sel.display,
                # the error model depends on the radar network (the first
                # letter, C or U) and the elevation, not on the radar: it
                # is drawn for a station or a group of one network, never
                # for one that mixes them
                'model_network': _network(sel),
                'stn_tag': sel.tag, 'member_word': word, 'region': region,
                'flag': flag, 'varno': varno, 'function': fn,
                'surface': surface, 'special': special,
                'special_label': special_label(family, special),
                'elevation': elevation, 'yaxis': yaxis,
                'colours': colours, 'pathwork': pathwork,
                'datestart': datestart, 'dateend': dateend,
                'min_obs': min_obs, 'svg': svg,
                'obs_error_model': obs_error_model,
                'group': (family, sel.tag, region, surface, special, flag,
                          varno, fn,
                          elevation, yaxis)}

    first_db = next(iter(run_dbs.values()))
    combos = _distinct(first_db, "SELECT DISTINCT region, land_ocean, special, flag, varno "
                                 "FROM prof ORDER BY 1, 2, 3, 4, 5;")
    views = ([('join', 'range'), ('join', 'height')]
             + [(e, ax) for e in elevations for ax in ('range', 'height')]
             if radar else [('na', None)])
    for sel in selectors:
        for region, surface, special, flag, varno in combos:
            for fn in functions:
                for elevation, yaxis in views:
                    for name, _ in all_runs:
                        spec = base(sel, region, flag, varno, fn, elevation,
                                    yaxis, surface, special)
                        spec.update(mode='run', name=name,
                                    colour=(CTL_COLOUR if control and
                                            name == control[0]
                                            else EXP_COLOUR),
                                    db_file=run_dbs[name])
                        figs.append(spec)
                    if control:
                        for name, _ in runs:
                            spec = base(sel, region, flag, varno, fn,
                                        elevation, yaxis, surface, special)
                            spec.update(
                                mode='diff', name=name, control=control[0],
                                db_ctl=run_dbs[control[0]],
                                db_exp=run_dbs[name],
                                db_file=db_path(pathwork, family,
                                                f"{control[0]}_vs_{name}",
                                                datestart, dateend))
                            figs.append(spec)
    for f in figs:
        label = (f"{f['name']} vs {f['control']}" if f['mode'] == 'diff'
                 else f['name'])
        f['viewer'] = {'experience': label, 'family': family,
                       'fonction': f['function'], 'region': f['region'],
                       'flag_criteria': f['flag'], 'id_stn': f['stn_label'],
                       'land_ocean': f['surface'],
                       'special': f['special_label'],
                       'varno': str(f['varno']),
                       'elevation': f['elevation'] if radar else 'na',
                       'yaxis': f['yaxis'] or 'na'}
    return figs


def shared_limits(figs: List[Dict[str, Any]]) -> None:
    """The same axes for every run of a group, and for every change."""
    groups: Dict[tuple, Dict[str, float]] = {}
    for f in figs:
        g = groups.setdefault((f['group'], f['mode']), {})
        try:
            data = read_run(f) if f['mode'] == 'run' else read_diff(f)
        except Exception:
            continue
        for d in data.values():
            d = _keep(d, f['min_obs'])
            if not len(d['n']):
                continue
            g['n'] = max(g.get('n', 0), float(np.nanmax(d['n'])))
            g['lev_lo'] = min(g.get('lev_lo', np.inf), float(np.min(d['lev'])))
            g['lev_hi'] = max(g.get('lev_hi', -np.inf),
                              float(np.max(d['lev'])))
            if f['mode'] == 'run':
                vals = np.concatenate([np.abs(d['mean']), d['std'],
                                       d['oer'][np.isfinite(d['oer'])]])
                g['x'] = max(g.get('x', 0), float(np.nanmax(vals)))
            else:
                db = np.abs(np.abs(d['me']) - np.abs(d['mc']))
                ds = np.abs(100 * (d['se'] - d['sc']) / d['sc'])
                g['db'] = max(g.get('db', 0), float(np.nanmax(db)))
                g['ds'] = max(g.get('ds', 0), float(np.nanmax(ds)))
    for f in figs:
        f['limits'] = groups.get((f['group'], f['mode']), {})


# ─────────────────────────────────────────────────────────────────────────────
# Axes
# ─────────────────────────────────────────────────────────────────────────────

def _nice(v: float) -> float:
    if not v or not np.isfinite(v) or v <= 0:
        return 1.0
    mag = 10 ** np.floor(np.log10(v))
    for m in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if m * mag >= v:
            return m * mag
    return 10 * mag


def _style(ax) -> None:
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#B0B0B0")
    ax.tick_params(labelsize=11, colors="#333333")
    ax.grid(True, ls="--", lw=0.7, alpha=0.25)
    ax.set_axisbelow(True)


def _vertical(spec):
    """(transform of a level to the axis, label, invert, log)."""
    if spec['radar']:
        return ((lambda v: v),
                "beam height MSL [km]" if spec['yaxis'] == 'height'
                else "slant range [km]", False, False)
    kind = spec['vcotyp'].strip().upper()
    if kind.startswith('PRESSION'):
        lo, hi = spec['limits'].get('lev_lo', 1), spec['limits'].get('lev_hi',
                                                                     1)
        return ((lambda v: v / 100.0), "pressure [hPa]", True,
                lo > 0 and hi / lo > 15)
    if kind.startswith('HAUTEUR'):
        return (lambda v: v / 1000.0), "height [km]", False, False
    if kind.startswith('CANAL'):
        return (lambda v: v), "channel", True, False
    return (lambda v: v), "level", False, False


def _fig_height(spec) -> float:
    """9 inches; a channel axis grows so that every channel has its label."""
    n = len(spec.get('_channels') or [])
    return max(9.0, 2.4 + 0.16 * n)


def _fy(fig, y) -> float:
    """A height given for the 9-inch figure, kept in inches from the top."""
    return 1.0 - (1.0 - y) * 9.0 / fig.get_figheight()


def _is_channel(spec) -> bool:
    return (not spec.get('radar')
            and str(spec.get('vcotyp', '')).strip().upper().startswith('CANAL'))


def _channel_axis(spec, levels):
    """The channels of a figure, one place each: only those there are,
    kept in spec['_channels'] for the ticks."""
    chans = sorted({float(v) for lev in levels for v in np.atleast_1d(lev)})
    pos = {c: i for i, c in enumerate(chans)}
    spec['_channels'] = chans
    return lambda v: np.array([pos.get(float(x), np.nan) for x in np.atleast_1d(v)])


def _finish_y(ax, spec, to_y):
    if spec.get('radar'):
        # always 0-14 km of beam height, 0-250 km of range: every radar
        # figure on the same frame
        ax.set_ylim(0.0, RADAR_MAX_HEIGHT_KM if spec['yaxis'] == 'height'
                    else RADAR_MAX_RANGE_KM)
        return
    chans = spec.get('_channels')
    if chans:
        # channels: one place each, the real number on the ticks, at most
        # about 40 of them; the lowest channel on top
        n = len(chans)
        step = 1                      # every channel: the figure grows
        if n > 40:
            ax.tick_params(axis='y', labelsize=8.5)
        ticks = list(range(0, n, step))
        ax.set_yticks(ticks)
        ax.set_yticklabels([f"{chans[i]:g}" for i in ticks])
        ax.set_ylim(n - 0.5, -0.5)
        return
    lim = spec['limits']
    if 'lev_lo' in lim:
        lo, hi = to_y(lim['lev_lo']), to_y(lim['lev_hi'])
        pad = 0.04 * (hi - lo) if hi > lo else 1.0
        _, _, invert, log = _vertical(spec)
        if log:
            ax.set_yscale('log')
            ax.set_ylim(lo * 0.85, hi * 1.15)
            ax.yaxis.set_major_formatter(
                mpl.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        else:
            ax.set_ylim(lo - pad, hi + pad)
        if invert:
            ax.invert_yaxis()


# ─────────────────────────────────────────────────────────────────────────────
# Figures
# ─────────────────────────────────────────────────────────────────────────────

def _members(spec) -> List[str]:
    """The stations that hold data in a figure of a group of stations."""
    where, args = _where(spec)
    dbs = ([spec.get('db_ctl'), spec.get('db_exp')] if spec.get('mode') == 'diff'
           else [spec.get('db_file')])
    names = set()
    for db in dbs:
        if not db or not os.path.isfile(db):
            continue
        try:
            with open_result(db) as conn:
                names |= {str(r[0]) for r in conn.execute(
                    f"SELECT DISTINCT id_stn FROM prof WHERE {where}", args)}
        except Exception:
            pass
    return sorted(names)


def _members_line(spec) -> str:
    """'stations: a, b, c' up to 20; beyond, the first 10 and the total."""
    member = str(spec.get('stn_label', ''))
    # every figure that holds several stations: join, a group (c%),
    # an instrument type; one station alone says its name already
    single = (spec.get('member_word') == 'station' and member != 'join'
              and '%' not in member)
    if single:
        return ""
    names = _members(spec)
    if not names:
        return ""
    if len(names) <= 20:
        return f"{len(names)} station{'s' if len(names) > 1 else ''}: " + ", ".join(names)
    return (f"{len(names)} stations: " + ", ".join(names[:10])
            + f" ...  (10 of {len(names)} shown)")


def _header(fig, spec, head, extra=""):
    """The header of every module: the variable and the quantity, the dates
    top right, a grey line with what the figure holds, the runs in their
    colours, the notes small, then the rule."""
    var_name, units, _ = pikobs.type_varno(str(spec['varno']))

    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    member = str(spec['stn_label'])
    parts = [spec['family'], f"{spec['region']}{_extra_txt(spec)}",
             f"flag {spec['flag']}",
             f"all {spec['member_word']}s" if member == 'join'
             else f"{spec['member_word']} {member}"]
    if spec['radar']:
        parts.append("all elevations" if spec['elevation'] == 'join'
                     else f"elevation {spec['elevation']} deg")
        parts.append(f"against the "
                     f"{'beam height' if spec['yaxis'] == 'height' else 'slant range'}")
    fig.text(0.05, _fy(fig, 0.978), f"{var_name} {units}  \u00b7  {_FN[spec['function']]}",
             ha='left', va='top', fontsize=16, fontweight='bold', color='#1F2933')
    fig.text(0.985, _fy(fig, 0.975), f"{_when(spec['datestart'])}  to  "
             f"{_when(spec['dateend'])}", ha='right', va='top', fontsize=10.5,
             color=_GREY)
    fig.text(0.05, _fy(fig, 0.945), "  \u00b7  ".join(parts), ha='left', va='top',
             fontsize=11, color=_GREY)
    # a group of stations: which ones, on a line of its own
    members = _members_line(spec)
    dy = 0.0
    if members:
        fig.text(0.05, _fy(fig, 0.918), members, ha='left', va='top', fontsize=10,
                 color=_GREY)
        dy = 0.026
    # the runs in their colours, on one line
    if spec.get('mode') == 'diff':
        who = [("Exp", spec['name'], EXP_COLOUR), ("Ctl", spec['control'], CTL_COLOUR)]
    else:
        who = [("Ctl" if spec.get('colour') == CTL_COLOUR else "Exp", head,
                spec.get('colour', EXP_COLOUR))]
    renderer = fig.canvas.get_renderer()
    x = 0.05
    for word, name, colour in who:
        t = fig.text(x, _fy(fig, 0.912 - dy), f"{word}  {name}", ha='left', va='top',
                     fontsize=13, fontweight='bold', color=colour)
        box = t.get_window_extent(renderer=renderer)
        x = fig.transFigure.inverted().transform((box.x1, box.y0))[0] + 0.03
    note = extra.strip().replace("  |  ", "  \u00b7  ")
    if note:
        fig.text(0.05, _fy(fig, 0.880 - dy), note, ha='left', va='top', fontsize=10.5,
                 color=_GREY)
    rule = _fy(fig, (0.858 if note else 0.878) - dy)
    fig.add_artist(mpl.lines.Line2D([0.05, 0.985], [rule, rule],
                                    transform=fig.transFigure,
                                    color='#D9DDE2', lw=0.9))
    return units


def _out(spec) -> str:
    what = (f"{_safe(spec['control'])}_vs_{_safe(spec['name'])}"
            if spec['mode'] == 'diff' else _safe(spec['name']))
    view = ""
    if spec['radar']:
        view = f"_elev{_safe(spec['elevation'])}_{spec['yaxis']}"
    d = os.path.join(spec['pathwork'], spec['family'])
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"profile_{what}_{spec['family']}_"
                           f"{spec['function']}_varno{_safe(spec['varno'])}_"
                           f"{_safe(spec['stn_tag'])}_{_safe(spec['region'])}{_extra(spec)}_"
                           f"{_safe(spec['flag'])}{view}.png")


_FITTED_CACHE: Dict[str, Dict[str, list]] = {}


def _fitted_model(path: str, height_km, elevation_deg: float,
                  network: str) -> np.ndarray:
    """sigma_o of the table FIT_RADAR wrote (radar_obs_error_fitted.py), in
    the form of radar_obs_error: base + slope dh + accel dh^2."""
    h = np.asarray(height_km, float)
    if path not in _FITTED_CACHE:
        ns: Dict[str, Any] = {}
        try:
            exec(open(path).read(), ns)
        except Exception:                                  # pragma: no cover
            ns = {}
        _FITTED_CACHE[path] = ns.get('_TABLE', {})
    tenths = int(round(float(elevation_deg) * 10.0))
    for (lo, hi), (base, onset, slope, accel) in \
            _FITTED_CACHE[path].get(str(network)[:1].upper(), []):
        if lo <= tenths <= hi:
            dh = np.maximum(0.0, h - onset)
            return np.clip(base + slope * dh + accel * dh * dh, 2.0, 16.0)
    return np.full_like(h, np.nan)


def _run_figure(spec) -> Optional[str]:
    data = {e: _keep(d, spec['min_obs']) for e, d in read_run(spec).items()}
    data = {e: d for e, d in data.items() if len(d['n'])}
    if not data:
        return None
    data, hidden = _drop_rare_elevations(data) if spec['radar'] \
        else (data, 0)
    to_y, y_label, _, _ = _vertical(spec)
    if _is_channel(spec):
        to_y = _channel_axis(spec, [d['lev'] for d in data.values()])
    lim = spec['limits']
    radar = spec['radar']
    fig = plt.figure(figsize=(15.5, _fig_height(spec)), facecolor='white')
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 3.0, 0.95],
                          wspace=0.10, left=0.06, right=0.985, top=_fy(fig, 0.83),
                          bottom=0.08 * 9.0 / fig.get_figheight())
    ax_n = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1], sharey=ax_n)
    ax_k = fig.add_subplot(gs[0, 2])
    ax_k.axis('off')
    for ax in (ax_n, ax_b):
        _style(ax)
    ax_b.tick_params(axis='y', labelleft=False)

    model_drawn = False
    model_max = 0.0
    drew_oer = drew_des = fit_drawn = False
    # several radar elevations: the sigma and the bias of each, the error
    # curves in the figure of each elevation
    errors_on = not (radar and len(data) > 1)
    curves = set(spec.get('curves') or ['obs_error'])     # ERROR_CURVES
    handles = []
    n_total: Dict[float, float] = {}
    for e, d in sorted(data.items(), key=lambda kv: (kv[0] == 'na',
                                                     float(kv[0]) if kv[0]
                                                     != 'na' else 0)):
        y = to_y(d['lev'])
        # one elevation: the colour of the run; several: one per elevation
        colour = spec['colours'].get(e, spec['colour']) \
            if radar and not errors_on else spec['colour']
        for yy, nn in zip(y, d['n']):
            n_total[yy] = n_total.get(yy, 0) + nn
        ax_b.plot(d['mean'], y, '-', color=colour, lw=1.3, alpha=0.95)
        ax_b.plot(d['std'], y, '-', color=colour, lw=2.2)
        # the error the assimilation used: always, in every family
        if errors_on and np.any(np.isfinite(d['oer'])):
            ax_b.plot(d['oer'], y, color=OER_COLOUR, lw=2.2, ls=(0, (1, 1.6)))
            drew_oer = True
        if errors_on and 'desroziers' in curves \
                and np.any(np.isfinite(d['des'])):
            # the error the analysis sees in the data: the target of a
            # calibration
            ax_b.plot(d['des'], y, color=DES_COLOUR, lw=1.4, marker='x',
                      ms=5)
            drew_des = True
        if errors_on and radar \
                and ('model' in curves
                     or ('model_fit' in curves and spec.get('fit_table'))) \
                and spec['yaxis'] == 'height' \
                and e != 'na' and spec.get('model_network'):
            from pikobs.profile.radar_obs_error import model_obs_error
            if 'model' in curves:
                m = model_obs_error(d['lev'], float(e), spec['model_network'])
                ax_b.plot(m, y, '-.', color=MODEL_COLOUR, lw=1.8)
                model_max = max(model_max, float(np.nanmax(m)))
                model_drawn = True
            # FIT_RADAR: the error fitted on this run, beside the model
            if spec.get('fit_table') and 'model_fit' in curves:
                mf = _fitted_model(spec['fit_table'], d['lev'], float(e),
                                   spec['model_network'])
                if np.any(np.isfinite(mf)):
                    ax_b.plot(mf, y, color=FIT_COLOUR, lw=2.4)
                    model_max = max(model_max, float(np.nanmax(mf)))
                    fit_drawn = True
        if radar:
            handles.append(mpl.lines.Line2D(
                [0], [0], color=colour, lw=2.5,
                label=f"{float(e):.1f} deg  ({int(d['n'].sum()):,})"))
    ys = np.array(sorted(n_total))
    step = np.diff(ys).min() * 0.8 if len(ys) > 1 else 1.0
    ax_n.barh(ys, [n_total[v] for v in ys], height=step,
              color=spec['colour'] if not radar else '#7F8C8D', alpha=0.75)
    ax_n.set_xlim(0, _nice(lim.get('n', max(n_total.values())) * 1.05))
    ax_n.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(
        lambda v, _: f"{v / 1000:g}k" if v >= 1000 else f"{v:g}"))
    ax_n.set_xlabel("observations per level", fontsize=12)
    ax_n.set_ylabel(y_label, fontsize=12)

    units = _header(fig, spec, spec['name'])
    # wide enough for the model too, when it is drawn
    xm = _nice(max(lim.get('x', 1.0), model_max) * 1.05)
    ax_b.set_xlim(-xm * 0.35, xm)
    ax_b.axvline(0, color='#444444', ls=':', lw=1)
    ax_b.set_xlabel(f"{_FN[spec['function']]}  {units}", fontsize=12)
    _finish_y(ax_n, spec, to_y)

    # only what is on the figure
    style_keys = [
        mpl.lines.Line2D([0], [0], color='#333333', lw=2.2,
                         label="sigma of the departure"),
        mpl.lines.Line2D([0], [0], color='#333333', lw=1.3,
                         label="bias (mean)")]
    if drew_oer:
        style_keys.append(mpl.lines.Line2D([0], [0], color=OER_COLOUR, lw=2.2,
                                           ls=(0, (1, 1.6)),
                                           label="OBS_ERROR used in the\n"
                                                 "assimilation (files)"))
    if drew_des:
        style_keys.append(mpl.lines.Line2D(
            [0], [0], color=DES_COLOUR, lw=1.4, marker='x', ms=5,
            label="obs error, Desroziers"))
    if model_drawn:
        style_keys.append(mpl.lines.Line2D([0], [0], color=MODEL_COLOUR, lw=1.8,
                                           ls='-.', label="error model (current,\n"
                                           "radar_obs_error)"))
    if fit_drawn:
        style_keys.append(mpl.lines.Line2D([0], [0], color=FIT_COLOUR, lw=2.4,
                                           label="fitted on this run:\n"
                                           f"{spec.get('fit_target') or 'FIT_RADAR'}"))
    # top: what the lines are, and how to read the ratio; bottom: the
    # elevations -- never on top of each other
    leg1 = ax_k.legend(handles=style_keys, loc='upper left',
                       bbox_to_anchor=(0, 1), fontsize=10, title="lines",
                       title_fontsize=10.5, frameon=True, edgecolor='#DDDDDD')
    ax_k.add_artist(leg1)
    if not errors_on:
        ax_k.text(0.0, 0.74, "error curves: in the figure\nof each elevation",
                  transform=ax_k.transAxes, fontsize=9.5, color=_GREY,
                  va='top', linespacing=1.35)
    _elevation_legend(ax_k, handles, "elevation (observations)", hidden)
    out = _out(spec)
    save_figure(fig, out, svg=spec.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out


def _test_marks(ax, x, y, conf, better, x_mark):
    sig = is_significant(conf)
    for yy, s, b in zip(y, sig, better):
        if s:
            ax.scatter([x_mark], [yy], s=36, zorder=5, clip_on=False,
                       color=EXP_BETTER if b else CTL_BETTER)
        else:
            ax.scatter([x_mark], [yy], s=36, zorder=5, clip_on=False,
                       facecolors='white', edgecolors='#777777')


def _diff_figure(spec) -> Optional[str]:
    data = {e: _keep(d, spec['min_obs']) for e, d in read_diff(spec).items()}
    data = {e: d for e, d in data.items() if len(d['n'])}
    if not data:
        return None
    data, hidden = _drop_rare_elevations(data) if spec['radar'] \
        else (data, 0)
    to_y, y_label, _, _ = _vertical(spec)
    if _is_channel(spec):
        to_y = _channel_axis(spec, [d['lev'] for d in data.values()])
    lim = spec['limits']
    radar = spec['radar']
    fig = plt.figure(figsize=(15.5, _fig_height(spec)), facecolor='white')
    gs = fig.add_gridspec(1, 3, width_ratios=[2.0, 2.0, 0.95], wspace=0.10,
                          left=0.06, right=0.985, top=_fy(fig, 0.83), bottom=0.08 * 9.0 / fig.get_figheight())
    ax_b = fig.add_subplot(gs[0, 0])
    ax_s = fig.add_subplot(gs[0, 1], sharey=ax_b)
    ax_k = fig.add_subplot(gs[0, 2])
    ax_k.axis('off')
    for ax in (ax_b, ax_s):
        _style(ax)
    ax_s.tick_params(axis='y', labelleft=False)
    xb = _nice(lim.get('db', 0.1) * 1.1)
    xs = max(0.5, _nice(lim.get('ds', 1.0) * 1.1))
    counts = {'t': [0, 0], 'f': [0, 0]}
    handles = []
    single = len(data) == 1
    for e, d in sorted(data.items(), key=lambda kv: (kv[0] == 'na',
                                                     float(kv[0]) if kv[0]
                                                     != 'na' else 0)):
        y = to_y(d['lev'])
        colour = spec['colours'].get(e, '#555555') if radar else '#555555'
        dbias = np.abs(d['me']) - np.abs(d['mc'])
        dspr = 100.0 * (d['se'] - d['sc']) / d['sc']
        marker = '-o' if single else '-'
        ax_b.plot(dbias, y, marker, color=colour, lw=1.5, ms=3.5)
        ax_s.plot(dspr, y, marker, color=colour, lw=1.5, ms=3.5)
        if single:
            # the tests on the left edge: one row of dots per level
            _test_marks(ax_b, dbias, y, d['t_conf'], dbias < 0, -xb * 0.92)
            _test_marks(ax_s, dspr, y, d['f_conf'], dspr < 0, -xs * 0.92)
        else:
            # several elevations: each point filled in the colour of the
            # winner when its test passes, hollow otherwise
            for ax, vals, conf in ((ax_b, dbias, d['t_conf']),
                                   (ax_s, dspr, d['f_conf'])):
                sig = is_significant(conf)
                better = vals < 0
                ax.scatter(vals[sig & better], y[sig & better], s=42,
                           color=EXP_BETTER, edgecolors='white',
                           linewidths=0.8, zorder=5)
                ax.scatter(vals[sig & ~better], y[sig & ~better], s=42,
                           color=CTL_BETTER, edgecolors='white',
                           linewidths=0.8, zorder=5)
        for key, vals, conf in (('t', dbias, d['t_conf']),
                                ('f', dspr, d['f_conf'])):
            sig = is_significant(conf)
            counts[key][0] += int(np.sum(sig & (vals < 0)))
            counts[key][1] += int(np.sum(sig & (vals >= 0)))
        if radar:
            handles.append(mpl.lines.Line2D(
                [0], [0], color=colour, lw=2.5,
                label=f"{float(e):.1f} deg  ({int(d['n'].sum()):,})"))
    for ax, x in ((ax_b, xb), (ax_s, xs)):
        ax.set_xlim(-x, x)
        ax.axvline(0, color='#333333', ls=':', lw=1.2)
        ax.axvspan(-x, 0, color=EXP_BETTER, alpha=0.05, zorder=0)
        ax.axvspan(0, x, color=CTL_BETTER, alpha=0.05, zorder=0)
    units = _header(fig, spec, f"{spec['name']} vs {spec['control']}",
                    ("\nMATCH off: each run with all its observations  |  "
                     if spec.get('unmatched') else
                     "\nMATCH on: the same observations in both runs  |  ") +
                    f"bias: {counts['t'][0]} red, {counts['t'][1]} blue   "
                    f"sigma: {counts['f'][0]} red, {counts['f'][1]} blue")
    ax_b.set_xlabel(f"|bias| Exp - |bias| Ctl  {units}\n"
                    f"left = Exp closer to zero", fontsize=12)
    ax_s.set_xlabel("100 x (sigma Exp - sigma Ctl) / sigma Ctl  [%]\n"
                    "left = Exp narrower", fontsize=12)
    ax_b.set_ylabel(y_label, fontsize=12)
    _finish_y(ax_b, spec, to_y)
    keys = [mpl.lines.Line2D([0], [0], marker='o', lw=0, color=EXP_BETTER,
                             label="Exp better"),
            mpl.lines.Line2D([0], [0], marker='o', lw=0, color=CTL_BETTER,
                             label="Ctl better"),
            mpl.lines.Line2D([0], [0], marker='o', lw=0, markerfacecolor='w',
                             markeredgecolor='#777777',
                             label="not significant"
                             + (" (no dot with several elevations)"
                                if not single else ""))]
    leg = ax_k.legend(handles=keys, loc='upper left', bbox_to_anchor=(0, 1),
                      fontsize=10,
                      title=f"tests (pikobs.stats), {MIN_CONFIDENCE:.0f} %",
                      title_fontsize=10.5, frameon=True, edgecolor='#DDDDDD')
    ax_k.add_artist(leg)
    ax_k.text(0.0, 0.82, ("bias: Welch t-test on the mean\nsigma: F-test"
                          if spec.get('unmatched') else
                          "bias: paired t-test on the mean\nsigma: Pitman-Morgan") +
              "\nsignificant is not the same as large", transform=ax_k.transAxes,
              fontsize=9.5, color=_GREY, va='top', linespacing=1.35)
    _elevation_legend(ax_k, handles, "elevation" + ("" if spec.get('unmatched')
                                                  else " (matched)"), hidden)
    out = _out(spec)
    save_figure(fig, out, svg=spec.get('svg', False), dpi=DPI)
    plt.close(fig)
    return out


def plot_task(spec: Dict[str, Any]) -> Optional[str]:
    import traceback
    try:
        with plt.rc_context(_STYLE):
            if spec['mode'] == 'diff':
                return _diff_figure(spec)
            return _run_figure(spec)
    except Exception:
        print(f"[profile] plot failed for {spec.get('family')} "
              f"{spec.get('stn_label')} {spec.get('mode')} "
              f"{spec.get('elevation')}:\n{traceback.format_exc()}",
              file=sys.stderr, flush=True)
        plt.close('all')
        return None
