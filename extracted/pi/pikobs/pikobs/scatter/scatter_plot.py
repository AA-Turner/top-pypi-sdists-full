#!/usr/bin/python3
"""Maps and viewer of pikobs.scatter.

Everything that draws lives here: one map per selection, the three
panels of a comparison (difference, significance, significant only), and
the HTML viewer that indexes them. What reads the observation files is in
``scatter.py``.

The split follows the other modules of pikobs, and it is what lets a
figure be reworked without touching the extraction: a colour, a title or
a colour bar is changed here and the databases are not read again.
"""

from __future__ import annotations

import inspect
import os
import sqlite3
import sys
import textwrap
import traceback
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import matplotlib.colorbar as cbar
import matplotlib.colors   as colors
import matplotlib.pyplot   as plt
from matplotlib.collections  import PatchCollection
from matplotlib.ticker       import FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy.feature
from pikobs.figures import save_figure
from pikobs.obsdb import work_db
from pikobs.stats import (bias_and_sigma as _bias_and_sigma,
                          is_significant as _is_significant,
                          moments_from_sums as _moments_from_sums,
                          paired_ttest_confidence as _paired_t_confidence,
                          sample_std as _sample_std,
                          ttest_confidence as _ttest_confidence,
                          sigma_confidence)
from pikobs.stations.stations import (StationSelector, _codtyp_name,
                                      _safe_filename)
from pikobs.configobs.special_family import (special_key_label,
                                             special_label,
                                             special_title)
import pikobs
from pikobs.configobs.style import CTL_COLOUR, EXP_COLOUR, GREY_TEXT

# what the drawing needs from the extraction side
from pikobs.scatter.scatter import (
    _layer_label,
    _special_where,
    ALPHA_TILES,
    DPI,
    FIG_SIZE,
    N_INTERVALS,
    PANEL_CONF,
    PANEL_SIGONLY,
    PANEL_VALUE,
    _BAD_RGBA,
    _CONF_BOUNDS,
    _CONF_COLORS,
    _MIN_CONFIDENCE,
    _NICE_MANTISSAS,
    _NICE_N_LEVELS,
    _NICE_PERCENTILE,
    _PAIR_Q,
    _PERCENT_FUNCS,
    _TITLE_MAX_STATIONS,
    _TITLE_WRAP_CHARS,
    _WHITE_RGBA,
    _format_scientific_adaptive,
    _get_cmap,
    _layer_display,
    _n_days,
    _surface_area_km2,
    _vc_display,
    _vc_tag,
    _vcoord_sql)


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2 -- Plot rendering
# ─────────────────────────────────────────────────────────────────────────────

_PANEL_SUFFIX = {PANEL_CONF: '_signif', PANEL_SIGONLY: '_sigonly'}


def _land_tag(task: Dict[str, Any]) -> str:
    """The surface in a file name, only when there is a filter."""
    lo = task.get('land_ocean', 'all')
    return '' if lo in (None, '', 'all') else f"_{lo}"


def _special_title(family: str, sp) -> str:
    """'Method: IR channel' on its own line of the title; nothing for
    all."""
    lab = special_label(family, sp)
    return '' if lab == 'all' else f"\n{special_title(family)}: {lab}"


def _plot_filename(task: Dict[str, Any]) -> str:
    # the special value after the region and the surface, as everywhere
    sp = special_label(task['family'], task.get('special_val'))
    sp_tag = '' if sp == 'all' else f"_{_safe_filename(sp)}"
    return (f"{task['function']}_{task['proj']}_"
            f"{_safe_filename(_layer_label(task['interval'], task.get('vcotyp', '')))}_"
            f"flag_{_safe_filename(task['flag_criteria'])}_"
            f"id_stn_{task['selector'].tag}_"
            f"{_safe_filename(task['region'])}{_land_tag(task)}{sp_tag}_"
            f"vcoord{_vc_tag(task['vcoord'])}_varno{task['varno']}"
            f"_{_safe_filename(task['comparison'].key)}"
            f"{_PANEL_SUFFIX.get(task.get('panel'), '')}.png")


def _project_polygon(proj, lat: float, lon: float,
                     dx: float, dy: float, src_crs) -> List[List[float]]:
    out: List[List[float]] = []
    for dlon, dlat in ((-dx, -dy), (-dx, dy), (dx, dy), (dx, -dy)):
        x, y = proj.transform_point(lon + dlon, lat + dlat, src_crs)
        out.append([x, y])
    return out


def _box_stats_sql(table: str, db: str, varno: int, where: str,
                   sum_str: str, sum2_str: str) -> str:
    mean = f"SUM({sum_str}) / SUM(CAST(n AS FLOAT))"
    return f"""
    CREATE TEMPORARY TABLE {table} AS
    SELECT boite,
           MIN(lat)                                        AS lat,
           MIN(lon)                                        AS lon,
           {mean}                                          AS AVG,
           SQRT(MAX(0.0, SUM({sum2_str}) / SUM(CAST(n AS FLOAT))
                         - ({mean}) * ({mean})))           AS STD,
           SUM(sumStat) / SUM(CAST(n AS FLOAT))            AS BCORR,
           SQRT(MAX(0.0, SUM(sumStat2) / SUM(CAST(n AS FLOAT))
                         - (SUM(sumStat) / SUM(CAST(n AS FLOAT)))
                         * (SUM(sumStat) / SUM(CAST(n AS FLOAT)))))  AS BCSTD,
           SUM(n)                                          AS N
    FROM {db}.moyenne
    WHERE varno = {int(varno)}{where}
    GROUP BY boite
    HAVING SUM(n) > 0;
    """


def _stations_used(conn: sqlite3.Connection, n_db: int,
                   sel: StationSelector, varno: int) -> List[str]:
    names: set = set()
    for i in range(1, n_db + 1):
        for table in ('stations', 'moyenne'):
            try:
                rows = conn.execute(
                    f"SELECT DISTINCT id_stn FROM db{i}.{table} "
                    f"WHERE varno = ? AND id_stn != 'join'{sel.sql()};",
                    (int(varno),)).fetchall()
            except sqlite3.Error:
                continue
            names.update(r[0] for r in rows if r[0] is not None)
            break
    return sorted(names)


def _station_title(sel: StationSelector, stations: List[str]) -> str:
    if not sel.is_group:
        return f"id_stn: {sel.display}"
    head = f"id_stn: {sel.display} ({len(stations)} stn)"
    if sel.kind == 'codtyp' and len(sel.codes) > 1:
        types = ", ".join(f"{_codtyp_name(c)} ({c})" for c in sel.codes)
        head += "\n" + "\n".join(
            textwrap.wrap("codtyp: " + types, _TITLE_WRAP_CHARS))
    if not stations:
        return head
    shown = stations[:_TITLE_MAX_STATIONS]
    txt   = ", ".join(shown)
    if len(stations) > len(shown):
        txt += f", ... (+{len(stations) - len(shown)})"
    return head + "\n" + "\n".join(textwrap.wrap(txt, _TITLE_WRAP_CHARS))


def _nice_levels(values: np.ndarray,
                 cap: Optional[float] = None) -> np.ndarray:
    """Symmetric boundaries -L..-l, l..L from the 1-2-3-5 sequence.

    L is the smallest nice number above the 95th percentile of |values|;
    the _NICE_N_LEVELS nice numbers up to L are kept, so the white band
    (-l, l) scales with the map.
    """
    seq = [round(m * 10.0 ** e, 10)
           for e in range(-6, 8) for m in _NICE_MANTISSAS]
    a = np.abs(values[np.isfinite(values)])
    p = float(np.percentile(a, _NICE_PERCENTILE)) if a.size else 0.0
    if p <= 0:
        p = seq[_NICE_N_LEVELS - 1]
    if cap is not None:
        p = min(p, cap)
    vmax = next((x for x in seq if x >= p * (1 - 1e-9)), seq[-1])
    pos  = [x for x in seq if x <= vmax * (1 + 1e-9)][-_NICE_N_LEVELS:]
    return np.array([-x for x in reversed(pos)] + pos)


def _signed_cmap_and_norm(bounds: np.ndarray, negative_red: bool = False
                          ) -> Tuple[colors.ListedColormap, colors.BoundaryNorm]:
    """Blue (negative) - white (|x| < first level) - red (positive).

    negative_red swaps the colours: used for the departure scores, where a
    negative change (experience closer to zero) is the good one.
    """
    n_side = (len(bounds) - 2) // 2
    base   = _get_cmap('RdBu' if negative_red else 'RdBu_r')
    neg    = [base(x) for x in np.linspace(0.05, 0.40, n_side)]
    pos    = [base(x) for x in np.linspace(0.60, 0.95, n_side)]
    cmap   = colors.ListedColormap(neg + [_WHITE_RGBA] + pos)
    cmap.set_under(base(0.0))
    cmap.set_over(base(1.0))
    cmap.set_bad(_BAD_RGBA)
    return cmap, colors.BoundaryNorm(bounds, cmap.N)


def _relative_pct(num: np.ndarray, ref: np.ndarray) -> np.ndarray:
    """(num - ref) / ref * 100, NaN where ref is 0 or missing."""
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(ref > 0, (num - ref) * 100.0 / ref, np.nan)


def _paired_metric(fonction: str, N, SX, SY, SXX, SYY, SXY
                   ) -> Tuple[np.ndarray, np.ndarray,
                              Dict[str, np.ndarray], str]:
    """Box score on the observations common to both runs.

    x = control (reference), y = experience. Changes are experience minus
    reference:
      omp/oma        |bias_exp| - |bias_ref|           (negative = better)
      stdomp/stdoma  100 (s_exp - s_ref) / s_ref       (negative = better)
    Tests: Pitman-Morgan on the sigma, paired t-test on the mean; both come
    from pikobs.stats, which documents them.
    """
    mx, vx = _moments_from_sums(N, SX, SXX)
    my, vy = _moments_from_sums(N, SY, SYY)
    with np.errstate(divide='ignore', invalid='ignore'):
        cxy = np.where(np.asarray(N, float) > 0,
                       np.asarray(SXY, float) / np.asarray(N, float)
                       - mx * my, np.nan)
    with np.errstate(divide='ignore', invalid='ignore'):

        s_ref  = _sample_std(np.sqrt(vx), N)
        s_exp  = _sample_std(np.sqrt(vy), N)
        # matched boxes: Pitman-Morgan, with the covariance of the pairs
        f_conf = sigma_confidence(vx, vy, N, cov=cxy)
        if fonction in ('stdomp', 'stdoma'):
            values = np.where(s_ref > 0, (s_exp - s_ref) / s_ref * 100.0,
                              np.nan)
            return values, _is_significant(f_conf), {'F': f_conf}, 'improve'

        t_conf = _paired_t_confidence(mx, my, vx, vy, cxy, N)
        values = np.abs(my) - np.abs(mx)
        signif, confs = _bias_and_sigma(values, s_exp - s_ref, t_conf,
                                         f_conf)
        return values, signif, confs, 'improve'


def _diff_metric(fonction: str, avg1, avg2, std1, std2, bc1, bc2, n1, n2,
                 bcs1=None, bcs2=None
                 ) -> Tuple[np.ndarray, Optional[np.ndarray],
                            Dict[str, np.ndarray], str]:
    """Box score of experience (2) against control (1), all observations.

    Used for obs / nobs / dens, and for the tested functions when no pair
    database is available. Same direction as _paired_metric; 'improve'
    means that a negative value is an improvement.
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        if fonction in ('nobs', 'NOBSHDR', 'dens', 'dens%'):
            # the box area cancels out for the density
            return _relative_pct(n2, n1), None, {}, 'change'

        if fonction == 'obs':
            return avg2 - avg1, None, {}, 'change'

        if fonction == 'bcorr':
            # like nobs: change in percent over all observations, no test;
            # magnitudes, since a correction can be negative
            b1, b2 = np.abs(bc1), np.abs(bc2)
            values = np.where(b1 > 0, (b2 - b1) / b1 * 100.0, np.nan)
            return values, None, {}, 'change'

        s_ref  = _sample_std(std1, n1)
        s_exp  = _sample_std(std2, n2)
        # no pairs: the F-test on each run's own sigma
        f_conf = sigma_confidence(np.square(std1), np.square(std2), n1, n2)

        if fonction in ('stdomp', 'stdoma'):
            values = np.where(s_ref > 0, (s_exp - s_ref) / s_ref * 100.0,
                              np.nan)
            return values, _is_significant(f_conf), {'F': f_conf}, 'improve'

        t_conf = _ttest_confidence(avg1, std1, n1, avg2, std2, n2)
        values = np.abs(avg2) - np.abs(avg1)
        signif, confs = _bias_and_sigma(values, s_exp - s_ref, t_conf,
                                         f_conf)
        return values, signif, confs, 'improve'


_CBAR_DIFF: Dict[str, str] = {
    # the whole formula, the absolute value on each term: a bias can be
    # negative, and what matters is how close to zero each run gets
    'omp':    '|mean OMP| Exp - |mean OMP| Ctl {units}\n'
              'negative / red = Exp bias closer to zero',
    'oma':    '|mean OMA| Exp - |mean OMA| Ctl {units}\n'
              'negative / red = Exp bias closer to zero',
    'stdomp': 'σ(OMP) change [%], (σ Exp - σ Ctl) / σ Ctl\n'
              'negative / red = Exp better',
    'stdoma': 'σ(OMA) change [%], (σ Exp - σ Ctl) / σ Ctl\n'
              'negative / red = Exp better',
    'nobs':   'Nobs change [%], (Exp - Ctl) / Ctl\nred = more observations',
    'dens':   'Density change [%], (Exp - Ctl) / Ctl\nred = more observations',
    'obs':    '{var} Exp - Ctl {units}\nred = higher value in Exp',
    'bcorr':  '(|bcorr| Exp - |bcorr| Ctl) / |bcorr| Ctl [%]\n'
              'red = larger correction in Exp',
}
_CBAR_SINGLE: Dict[str, str] = {
    'dens':   'Density [obs/km²/day]',
    'nobs':   'Nobs/day',
    'omp':    'OMP {units}',
    'oma':    'OMA {units}',
    'obs':    '{var} {units}',
    'bcorr':  'Bias Correction {units}',
    'stdomp': 'σ(OMP) {units}',
    'stdoma': 'σ(OMA) {units}',
}


def _layer_words(interval, vcotyp) -> str:
    """The layer as a reader says it: "whole column", not "layer_all"."""
    text = _layer_display(interval, vcotyp)
    if str(text).strip().lower() in ('layer_all', 'all', 'layer all', ''):
        return 'whole column'
    return text


def _num(v) -> str:
    """A number for the box of a map: 0.152 when that reads, 3.02×10⁻⁴ when
    three decimals would round it to 0.000, or when it runs long. Written
    for mathtext, inside $...$."""
    v = float(v)
    if not np.isfinite(v):
        return "nan"
    if v == 0 or 1e-2 <= abs(v) < 1e4:
        return f"{v:.3f}"
    mant, exp = f"{v:.2e}".split("e")
    return f"{mant}\\times10^{{{int(exp)}}}"


_TEST_TEXT = {
    'omp':    "t-test (bias) + F-test (σ) on O-B, same sign",
    'oma':    "t-test (bias) + F-test (σ) on O-A, same sign",
    'stdomp': "F-test on σ(O-B)",
    'stdoma': "F-test on σ(O-A)",
}


_TEST_TEXT_PAIRED = {
    'omp':    "paired t-test (bias) + Pitman-Morgan (σ) on O-B, same sign",
    'oma':    "paired t-test (bias) + Pitman-Morgan (σ) on O-A, same sign",
    'stdomp': "Pitman-Morgan on σ(O-B) of the common observations",
    'stdoma': "Pitman-Morgan on σ(O-A) of the common observations",
}


def _info_text(panel, fonction, is_diff, kind, confs, values, diff_values,
               signif, in_axes, boundaries, on_map_obs, on_map_ref, n_days,
               avg=None, std=None, n_black=0, n_pairs=None,
               n_mixed=0) -> str:
    """Text of the box at the top right of a map.

    Four lines at most, wide rather than tall, so the box stays in the
    header and never reaches the map or its colour bar.
    """
    if not is_diff:
        nobs = f'{int(on_map_obs):,} obs in {n_days:.2f} days'
        if fonction in ('dens', 'nobs'):
            return nobs
        return (f'$\\bar{{\\mu}}={_num(np.nanmean(avg))}$   '
                f'$\\bar{{\\sigma}}={_num(np.nanmean(std))}$\n{nobs}')

    pct = ((on_map_obs - on_map_ref) / on_map_ref * 100.0
           if on_map_ref > 0 else float('nan'))
    nobs_line = (f'obs exp {int(on_map_obs):,}  ·  ctl {int(on_map_ref):,} '
                 f'({pct:+.1f} %, {n_days:.2f} d)')
    tests = _TEST_TEXT
    if n_pairs is not None:
        tests = _TEST_TEXT_PAIRED
        share = (n_pairs / on_map_ref * 100.0) if on_map_ref > 0 else 0.0
        nobs_line += f'  ·  compared {int(n_pairs):,} ({share:.0f} %)'

    box = in_axes & np.isfinite(diff_values)
    n_box = int(box.sum())
    n_sig = int((box & signif).sum())
    counts = f'significant at {_MIN_CONFIDENCE:.0f} %: {n_sig:,} of {n_box:,} boxes'
    if kind == 'change' and confs:
        n_up = int((box & signif & (diff_values > 0)).sum())
        n_dn = int((box & signif & (diff_values < 0)).sum())
        counts += f'  ·  {n_up:,} larger (red), {n_dn:,} smaller (blue)'
    if kind == 'improve':
        n_bet = int((box & signif & (diff_values < 0)).sum())
        n_wor = int((box & signif & (diff_values > 0)).sum())
        counts += f'  ·  {n_bet:,} better (red), {n_wor:,} worse (blue)'

    # the rare cases share one line
    extra = []
    if n_black:
        extra.append(f'black: {n_black:,} boxes, no '
                     + ('common observation' if n_pairs is not None
                        else 'counterpart'))
    if n_mixed:
        extra.append(f'{"xxx" if panel == PANEL_CONF else "mixed"}: '
                     f'{n_mixed:,} boxes, bias and σ opposite')
    extra = ['  ·  '.join(extra)] if extra else []

    test = tests.get(fonction, '')
    if panel == PANEL_SIGONLY:
        return '\n'.join([f'only the boxes above {_MIN_CONFIDENCE:.0f} % are drawn',
                          counts, nobs_line] + extra)
    if panel == PANEL_CONF:
        return '\n'.join(([test] if test else []) + [counts, nobs_line] + extra)
    return '\n'.join([nobs_line] + ([counts] if confs else []) + extra)


def _render_tile_map(task: Dict[str, Any],
                     common: Dict[str, Any]) -> Optional[str]:
    """Draw one map. Returns its path relative to pathwork, or None."""
    try:
        return _render_tile_map_impl(task, common)
    except Exception:
        print(f"[scatter] plot failed for {_plot_filename(task)}:\n"
              f"{traceback.format_exc()}", file=sys.stderr)
        plt.close('all')
        return None

def _render_tile_map_impl(task: Dict[str, Any],
                          common: Dict[str, Any]) -> Optional[str]:
    """Draw one map. Returns its path relative to pathwork, or None.

    The scientific calculations and colour scales are kept unchanged.
    This function focuses on the visual composition of the PNG/SVG:
    - dedicated header area above the map;
    - larger map area;
    - readable typography for projection/web viewing;
    - cleaner colour bar;
    - reduced visual weight of geographic features;
    - clearer experiment/reference information.
    """
    family    = task['family']
    fonction  = task['function']
    proj      = task['proj']
    sel       = task['selector']
    vcoord    = task['vcoord']
    varno     = int(task['varno'])
    sp_val    = task['special_val']
    interval  = task['interval']
    files_in  = task['files_in']
    names     = task['comparison'].names
    is_diff   = len(files_in) == 2

    if not all(os.path.isfile(f) for f in files_in):
        return None

    datestart, dateend = common['datestart'], common['dateend']
    boxsizex, boxsizey = float(common['boxsizex']), float(common['boxsizey'])
    deltax, deltay     = boxsizex / 2.0, boxsizey / 2.0
    n_days             = _n_days(datestart, dateend)

    FNAM, FNAMP, SUM_STR, SUM2_STR = pikobs.type_boxes(fonction)
    where = (sel.sql() + _vcoord_sql(vcoord)
             + _special_where(sp_val))

    pair_db = task.get('pair_db')
    paired  = bool(is_diff and fonction in _PAIR_Q and pair_db
                   and os.path.isfile(pair_db))
    totals: List[np.ndarray] = []

    # ─────────────────────────────────────────────────────────────────────
    # Query
    # ─────────────────────────────────────────────────────────────────────
    attached = {f"db{i}": path for i, path in enumerate(files_in, 1)}
    if paired:
        attached['dbp'] = pair_db

    with work_db(attach=attached) as (conn, _):
        for i, path in enumerate(files_in, 1):
            conn.execute(
                _box_stats_sql(
                    f"B{i}",
                    f"db{i}",
                    varno,
                    where,
                    SUM_STR,
                    SUM2_STR))

        if paired:
            q = _PAIR_Q[fonction]

            conn.execute(f"""
                CREATE TEMPORARY TABLE P AS
                SELECT boite, MIN(lat) AS lat, MIN(lon) AS lon,
                       SUM(n_{q}) AS N,
                       SUM(sx_{q}) AS SX,
                       SUM(sy_{q}) AS SY,
                       SUM(sxx_{q}) AS SXX,
                       SUM(syy_{q}) AS SYY,
                       SUM(sxy_{q}) AS SXY
                FROM dbp.pairs
                WHERE varno = {varno}{where}
                GROUP BY boite
                HAVING SUM(n_{q}) > 0;
            """)

            rows = conn.execute("""
                SELECT P.lat, P.lon, P.N, P.SX, P.SY, P.SXX, P.SYY, P.SXY
                FROM P;
            """).fetchall()

            exclusive = conn.execute("""
                SELECT lat, lon FROM
                  (SELECT boite, lat, lon FROM B1
                   UNION SELECT boite, lat, lon FROM B2)
                WHERE boite NOT IN (SELECT boite FROM P);
            """).fetchall()

            for b in ('B1', 'B2'):
                totals.append(
                    np.array(
                        conn.execute(
                            f"SELECT lat, lon, N FROM {b};"
                        ).fetchall(),
                        dtype=float
                    ).reshape(-1, 3)
                )

        elif is_diff:
            rows = conn.execute("""
                SELECT B1.lat, B1.lon,
                       B1.AVG, B2.AVG,
                       B1.STD, B2.STD,
                       B1.BCORR, B2.BCORR,
                       B1.N, B2.N,
                       B1.BCSTD, B2.BCSTD
                FROM B1 JOIN B2 USING (boite);
            """).fetchall()

            exclusive = conn.execute("""
                SELECT lat, lon FROM B1
                WHERE boite NOT IN (SELECT boite FROM B2)

                UNION ALL

                SELECT lat, lon FROM B2
                WHERE boite NOT IN (SELECT boite FROM B1);
            """).fetchall()

        else:
            rows = conn.execute(
                "SELECT lat, lon, AVG, STD, BCORR, N FROM B1;"
            ).fetchall()
            exclusive = []

        stations = _stations_used(conn, len(files_in), sel, varno)

    if not rows:
        return None

    arr = np.array(rows, dtype=float)
    lat, lon = arr[:, 0], arr[:, 1]

    if paired:
        n_pair, SX, SY, SXX, SYY, SXY = arr[:, 2:8].T
        n_obs = n_pair

    elif is_diff:
        avg1, avg2, std1, std2, bc1, bc2, n1, n2, bcs1, bcs2 = \
            arr[:, 2:12].T
        n_obs = n2

    else:
        avg, std, bcorr, n_obs = arr[:, 2:6].T

    areas = _surface_area_km2(
        lat - deltay,
        lat + deltay,
        lon - deltax,
        lon + deltax)

    # ─────────────────────────────────────────────────────────────────────
    # Values and colour scale
    # ─────────────────────────────────────────────────────────────────────
    signif = None
    confs: Dict[str, np.ndarray] = {}
    kind   = None

    if paired:
        values, signif, confs, kind = _paired_metric(
            fonction,
            n_pair,
            SX,
            SY,
            SXX,
            SYY,
            SXY)

    elif is_diff:
        values, signif, confs, kind = _diff_metric(
            fonction,
            avg1,
            avg2,
            std1,
            std2,
            bc1,
            bc2,
            n1,
            n2,
            bcs1,
            bcs2)

    else:
        with np.errstate(divide='ignore', invalid='ignore'):

            if fonction in ('dens', 'dens%'):
                values = np.where(
                    areas > 0,
                    n_obs / areas,
                    0.0) / n_days
                cmap_name = 'viridis'

            elif fonction in ('nobs', 'NOBSHDR'):
                values = n_obs / n_days
                cmap_name = 'viridis'

            elif fonction == 'bcorr':
                values = bcorr
                cmap_name = 'coolwarm'

            elif fonction in ('stdomp', 'stdoma'):
                values = std
                cmap_name = 'magma_r'

            else:
                values = avg
                cmap_name = 'coolwarm'

    panel = task.get('panel', PANEL_VALUE)

    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return None

    if signif is None:
        signif = np.ones(len(values), dtype=bool)

    mixed = confs.pop('mixed', None) if confs else None
    if mixed is None:
        mixed = np.zeros(len(values), dtype=bool)

    # Combined confidence: the weakest test decides.
    conf = None
    if confs:
        stack = np.vstack(list(confs.values()))
        conf = np.where(
            np.isfinite(stack).all(axis=0),
            stack.min(axis=0),
            np.nan)

    signed = False

    if panel == PANEL_CONF:

        if conf is None:
            return None

        shown = values
        values = conf

        boundaries = np.array(_CONF_BOUNDS, dtype=float)

        cmap = colors.ListedColormap(list(_CONF_COLORS))
        cmap.set_over(_CONF_COLORS[-1])
        cmap.set_under(_CONF_COLORS[0])
        cmap.set_bad(_BAD_RGBA)

        norm = colors.BoundaryNorm(boundaries, cmap.N)
        extend = 'neither'

    elif is_diff or fonction in ('omp', 'oma'):

        signed = True

        # Scale on significant boxes when enough are available.
        # Difference and significant-only maps share the same scale.
        use = signif & np.isfinite(values)

        cap = (
            100.0
            if (is_diff and fonction in _PERCENT_FUNCS)
            else None
        )

        boundaries = _nice_levels(
            values[use] if (confs and use.sum() >= 3) else values,
            cap=cap)

        cmap, norm = _signed_cmap_and_norm(
            boundaries,
            negative_red=(is_diff and kind == 'improve'))

        extend = 'both'

    else:

        vmin = float(finite.min())
        vmax = float(finite.max())

        if vmin == vmax:
            vmax = vmin + 1.0

        # round steps (0.02, 0.05, 1e-3 ...), not ten equal parts of the
        # range: a colour bar reads 0.02 0.04 0.06, not 0.0045 0.0199
        from matplotlib.ticker import MaxNLocator
        boundaries = MaxNLocator(
            nbins=N_INTERVALS,
            steps=[1, 2, 2.5, 5, 10]).tick_values(vmin, vmax)

        cmap = _get_cmap(cmap_name, len(boundaries) - 1)
        norm = colors.BoundaryNorm(boundaries, cmap.N)
        extend = 'neither'

    ticks = list(boundaries)

    facecolors = np.asarray(cmap(norm(values)))
    facecolors[~np.isfinite(values)] = _BAD_RGBA

    # ─────────────────────────────────────────────────────────────────────
    # Figure
    # ─────────────────────────────────────────────────────────────────────
    plt.close('all')

    # Keep the existing global figure size so PNG/SVG dimensions remain
    # compatible with the rest of PIKOBS.
    fig = plt.figure(figsize=FIG_SIZE)

    # Slightly stronger axes boundary, but the map itself remains visually
    # light and uncluttered.
    plt.rcParams['axes.linewidth'] = 1.0

    ax, fig, lat_pos, proj_obj, pc = pikobs.type_projection(proj)

    # Reserve a dedicated header area above the map.
    #
    # The important point is that the header is placed in figure coordinates,
    # not in axes coordinates. This prevents long station/channel titles from
    # ever overlapping the map.
    fig.subplots_adjust(
        left=0.055,
        right=0.875,
        bottom=0.085,
        top=0.745)

    # ─────────────────────────────────────────────────────────────────────
    # Project points and determine which boxes are visible
    # ─────────────────────────────────────────────────────────────────────
    pts_xy = proj_obj.transform_points(
        pc, lon, lat)[:, :2]

    ax_xy = ax.transAxes.inverted().transform(
        ax.transData.transform(pts_xy))

    in_axes = (
        (ax_xy[:, 0] >= -0.01) &
        (ax_xy[:, 0] <= 1.01) &
        (ax_xy[:, 1] >= -0.01) &
        (ax_xy[:, 1] <= 1.01) &
        np.isfinite(ax_xy).all(axis=1)
    )

    def _on_map(points: np.ndarray) -> float:
        if points.size == 0:
            return 0.0

        xy = proj_obj.transform_points(
            pc,
            points[:, 1],
            points[:, 0])[:, :2]

        ax_p = ax.transAxes.inverted().transform(
            ax.transData.transform(xy))

        inside = (
            (ax_p[:, 0] >= -0.01) &
            (ax_p[:, 0] <= 1.01) &
            (ax_p[:, 1] >= -0.01) &
            (ax_p[:, 1] <= 1.01) &
            np.isfinite(ax_p).all(axis=1)
        )

        return float(np.nansum(points[inside, 2]))

    n_pairs_on_map = None

    if paired:
        # All observations of each run, not only common observations.
        on_map_ref = _on_map(totals[0])
        on_map_obs = _on_map(totals[1])
        n_pairs_on_map = float(n_obs[in_axes].sum())

    else:
        on_map_obs = float(n_obs[in_axes].sum())
        on_map_ref = (
            float(n1[in_axes].sum())
            if is_diff
            else 0.0
        )

    # ─────────────────────────────────────────────────────────────────────
    # Observation boxes
    # ─────────────────────────────────────────────────────────────────────
    patches = []
    patch_colors = []
    patches_mixed = []

    for i in np.flatnonzero(in_axes):

        if panel == PANEL_SIGONLY and not signif[i]:
            continue

        # Explicit observation numbers.
        if common['Points'] == 'ON':
            ax.text(
                pts_xy[i, 0],
                pts_xy[i, 1],
                int(np.floor(n_obs[i])),
                color="black",
                fontsize=12,
                zorder=6,
                ha='center',
                va='center',
                weight='bold')

            continue

        # For large boxes, show their value in the centre.
        # The old fontsize=5 was difficult to read on a projector.
        if boxsizex >= 10:

            if panel == PANEL_CONF:
                label = (
                    f"{np.floor(values[i]):.0f}%"
                    if np.isfinite(values[i])
                    else ""
                )
            else:
                label = _format_scientific_adaptive(values[i])

            if boxsizex >= 20:
                label_size = 8
            elif boxsizex >= 15:
                label_size = 7
            else:
                label_size = 6

            ax.text(
                pts_xy[i, 0],
                pts_xy[i, 1],
                label,
                color="black",
                fontsize=label_size,
                zorder=6,
                ha='center',
                va='center',
                weight='bold')

        polygon = plt.Polygon(
            _project_polygon(
                proj_obj,
                lat[i],
                lon[i],
                deltax,
                deltay,
                pc))

        patches.append(polygon)
        patch_colors.append(facecolors[i])

        if panel == PANEL_CONF and mixed[i]:
            patches_mixed.append(
                plt.Polygon(
                    _project_polygon(
                        proj_obj,
                        lat[i],
                        lon[i],
                        deltax,
                        deltay,
                        pc)))

    if patches:
        ax.add_collection(
            PatchCollection(
                patches,
                facecolors=patch_colors,
                edgecolors='#8c8c8c',
                linewidths=0.15,
                alpha=ALPHA_TILES,
                zorder=4))

    if patches_mixed:
        # Both tests pass, but bias and sigma moved in opposite directions.
        ax.add_collection(
            PatchCollection(
                patches_mixed,
                facecolors='none',
                edgecolors='#333333',
                linewidths=0.45,
                hatch='xxx',
                zorder=5))

    if exclusive:
        ax.add_collection(
            PatchCollection(
                [
                    plt.Polygon(
                        _project_polygon(
                            proj_obj,
                            lt,
                            ln,
                            deltax,
                            deltay,
                            pc))
                    for lt, ln in exclusive
                ],
                facecolors=(0, 0, 0, 1),
                edgecolors='black',
                linewidths=0.8,
                alpha=1.0,
                zorder=5))

    # ─────────────────────────────────────────────────────────────────────
    # Geographic background
    # ─────────────────────────────────────────────────────────────────────
    res = '50m'

    ax.add_feature(
        cartopy.feature.NaturalEarthFeature(
            'physical',
            'ocean',
            res,
            edgecolor='#9aa5aa',
            facecolor='#e7f2f5'),
        zorder=0)

    ax.add_feature(
        cartopy.feature.NaturalEarthFeature(
            'physical',
            'land',
            res,
            edgecolor='#c8c8c8',
            facecolor='#f4f3f0'),
        zorder=1)

    ax.add_feature(
        cartopy.feature.NaturalEarthFeature(
            'physical',
            'coastline',
            res,
            edgecolor='#4a4a4a',
            facecolor='none',
            linewidth=0.7),
        zorder=10)

    ax.add_feature(
        cartopy.feature.NaturalEarthFeature(
            'cultural',
            'admin_0_boundary_lines_land',
            res,
            edgecolor='#777777',
            facecolor='none',
            linewidth=0.4),
        zorder=10)

    # Grid is deliberately subtle so that it does not compete with the
    # observation boxes.
    ax.gridlines(
        color='#8a8a8a',
        linestyle='--',
        linewidth=0.5,
        xlocs=range(-180, 190, 20),
        ylocs=lat_pos,
        draw_labels=False,
        zorder=2,
        alpha=0.28)

    # ─────────────────────────────────────────────────────────────────────
    # Colour bar
    # ─────────────────────────────────────────────────────────────────────
    var_name, units, vcoord_type = pikobs.type_varno(varno)

    cax = make_axes_locatable(ax).append_axes(
        "right",
        size="5.5%",
        pad=0.08,
        axes_class=plt.Axes)

    cb = cbar.ColorbarBase(
        cax,
        cmap=cmap,
        norm=norm,
        orientation='vertical',
        drawedges=True,
        extend=extend,
        ticks=ticks,
        boundaries=boundaries,
        alpha=1.0)

    # Make the colour-bar labels projector-friendly.
    cb.ax.tick_params(
        labelsize=10,
        length=4,
        width=0.8,
        pad=4)

    if panel == PANEL_CONF:

        cb.ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, p: f'{x:g}'))

        cb.ax.axhline(
            _MIN_CONFIDENCE,
            color='black',
            linewidth=2.0)

        cb.ax.set_ylabel(
            f"Test confidence (1 - p) × 100 [%]\n"
            f"> {_MIN_CONFIDENCE:.0f}% = significant",
            fontsize=11,
            rotation=90,
            labelpad=14)

    elif signed:

        cb.ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, p: f'{x:g}'))

    elif fonction == 'dens':

        cb.ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, p: f'{x:.1e}'))

    tmpl = (
        _CBAR_DIFF if is_diff else _CBAR_SINGLE
    ).get(fonction)

    if tmpl and panel != PANEL_CONF:

        cb.ax.set_ylabel(
            tmpl.format(
                ref=names[0],
                exp=names[-1],
                var=var_name,
                units=units),
            fontsize=10 if is_diff else 11,
            rotation=90,
            labelpad=14)

    # ─────────────────────────────────────────────────────────────────────
    # Header
    #
    # Everything below is figure-relative rather than axes-relative.
    # This gives the header a fixed amount of space and prevents overlap
    # with the map regardless of station/channel title length.
    # ─────────────────────────────────────────────────────────────────────
    special_tag = _special_title(family, sp_val)

    station_text = _station_title(sel, stations)

    layer_text = _layer_display(
        interval,
        task.get('vcotyp', ''))

    vcoord_text = _vc_display(vcoord)

    # what a reader needs, not the internal tags: "METOP-1", not
    # "id_stn: METOP-1"; "all channels", not "vcoord/channel: join";
    # no layer line when the map holds the whole column
    station_text = station_text.replace("id_stn: ", "", 1)
    # a group lists its stations under its name: that list goes to the
    # third line, cut to one line, so the title never runs into the rule
    station_lines = [s.strip() for s in station_text.split("\n") if s.strip()]
    station_head = station_lines[0] if station_lines else ""
    station_rest = ", ".join(station_lines[1:])
    if len(station_rest) > 110:
        station_rest = station_rest[:107].rsplit(",", 1)[0] + ", ..."
    surface = task.get('land_ocean', 'all')
    region_text = (task['region'] if surface in (None, '', 'all')
                   else f"{task['region']} ({surface})")
    channels = str(task.get('vcotyp', '')).strip().upper().startswith('CANAL')
    if str(vcoord) in ('join', 'None', ''):
        vcoord_words = 'all channels' if channels else 'all levels'
    else:
        vcoord_words = (f'channel {vcoord_text}' if channels
                        else f'level {vcoord_text}')
    if str(layer_text).strip().lower() in ('layer_all', 'all', 'layer all', ''):
        # the whole column; a radiance names its channels in the subtitle
        layer_text = '' if channels else 'whole column'

    # Main title.
    title_main = f"{var_name} {units}"

    # Keep channel/vcoord on a separate visual line. This is particularly
    # useful when many channels are displayed successively.
    title_secondary = "  ·  ".join(
        t for t in (station_head, vcoord_words, region_text,
                    f"flag {task['flag_criteria']}") if t)

    title_third = "  ·  ".join(
        t for t in (layer_text, special_tag.strip(), station_rest) if t)

    # ─────────────────────────────────────────────────────────────────────
    # Main title
    # ─────────────────────────────────────────────────────────────────────
    fig.text(
        0.465,
        0.965,
        title_main,
        ha='center',
        va='top',
        fontsize=17,
        fontweight='bold',
        color='#20252a')

    fig.text(
        0.465,
        0.928,
        title_secondary,
        ha='center',
        va='top',
        fontsize=11.5,
        color='#42484d')

    fig.text(
        0.465,
        0.898,
        title_third,
        ha='center',
        va='top',
        fontsize=10.5,
        color='#62686c')

    # Thin separator under the title area.
    fig.lines.append(
        plt.Line2D(
            [0.055, 0.875],
            [0.875, 0.875],
            transform=fig.transFigure,
            color='#b8bdc1',
            linewidth=0.8))

    # ─────────────────────────────────────────────────────────────────────
    # Experiment / reference information
    # ─────────────────────────────────────────────────────────────────────
    # the runs in the colours every module gives them: the experience
    # red, the control blue (configobs.style); a single run is an
    # experience, so red too
    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    runs = ([("Exp", names[1], EXP_COLOUR),
             ("Ctl", names[0], CTL_COLOUR)] if is_diff
            else [("Exp", names[0], EXP_COLOUR)])
    y_run = 0.852
    for word, name, colour in runs:
        fig.text(0.055, y_run, f"{word}  {name}", ha='left', va='top',
                 fontsize=11, fontweight='bold', color=colour)
        y_run -= 0.028
    fig.text(0.055, y_run, f"{_when(datestart)}  to  {_when(dateend)}",
             ha='left', va='top', fontsize=10, color=GREY_TEXT)

    # ─────────────────────────────────────────────────────────────────────
    # Information/statistics box
    # ─────────────────────────────────────────────────────────────────────
    textstr = _info_text(
        panel,
        fonction,
        is_diff,
        kind,
        confs,
        values,
        shown if panel == PANEL_CONF else values,
        signif,
        in_axes,
        boundaries,
        on_map_obs,
        on_map_ref,
        n_days,
        avg if not is_diff else None,
        std if not is_diff else None,
        n_black=len(exclusive),
        n_pairs=n_pairs_on_map,
        n_mixed=int((mixed & in_axes).sum()))

    # one light box on every map: the significance map says what it tests
    # in its first line and needs no colour of its own
    info_face = '#f3f4f5'
    info_edge = '#c5c9cc'

    fig.text(
        0.865,
        0.862,
        textstr,
        ha='right',
        va='top',
        fontsize=8.5,
        color='#303438',
        linespacing=1.35,
        multialignment='left',
        bbox=dict(
            boxstyle='round,pad=0.45',
            facecolor=info_face,
            edgecolor=info_edge,
            linewidth=0.8,
            alpha=0.92))

    # ─────────────────────────────────────────────────────────────────────
    # Save
    # ─────────────────────────────────────────────────────────────────────
    fname = _plot_filename(task)

    out_path = os.path.join(
        common['pathwork'],
        family,
        fname)

    save_figure(
        fig,
        out_path,
        svg=task.get('svg', False),
        dpi=DPI)

    plt.close('all')

    return f"{family}/{fname}"

def _build_viewer_items(tasks: List[Dict[str, Any]],
                        results: List[Optional[str]]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for task, rel in zip(tasks, results):
        if not rel:
            continue
        fam    = str(task['family']).strip()
        sp_val = task.get('special_val')
        items.append({
            _RUN_KEY:      task['comparison'].label,
            'family':      fam,
            'region':      str(task['region']).strip(),
            'land_ocean':  str(task.get('land_ocean', 'all')),
            'flag':        str(task['flag_criteria']).strip(),
            'function':    str(task['function']).strip(),
            'panel':       task.get('panel', PANEL_VALUE),
            'layer':       _layer_words(task['interval'],
                                          task.get('vcotyp', '')),
            'varno':       str(task['varno']).strip(),
            'vcoord':      _vc_display(task['vcoord']),
            'proj':        str(task['proj']).strip(),
            'id_stn':      task['selector'].display,
            'id_stn_safe': task['selector'].tag,
            'special':     special_label(fam, sp_val),
            'filename':    rel,
        })
    return items


_RUN_KEY = 'experience'

# Explanation shown at the top of the viewer. One list entry = one
# paragraph. Rendered by the generic viewer through ``subtitle``, which is
# inserted as raw HTML inside the page header.
_INTRO_SINGLE = [
    "A global score says how a run does; these maps say <b>where</b>. Every "
    "observation of {ds} to {de} falls in a {bx}° x {by}° box, and the box "
    "takes the colour of the statistic picked in <b>Function</b>.",

    "<b>omp</b> and <b>oma</b> are the mean O-B and O-A of the box: red above "
    "zero, blue below, white when the box is unbiased. Each map sets its own "
    "scale, so read the colour bar before comparing two maps; 0.03 K on one "
    "can be 3 K on another. <b>stdomp</b> and <b>stdoma</b> are their sigma. "
    "<b>obs</b> is the mean observed value, <b>bcorr</b> the mean bias "
    "correction (radiances only), <b>nobs</b> the observations per day in the "
    "box and <b>dens</b> the same per km².",

    "The box at the top right gives the mean over the boxes of the map (μ, σ) "
    "and how many observations it holds. When the station is a group (join, a "
    "prefix, a pattern, a codtyp) the title names the stations that went in. "
    "With LAND_OCEAN and SPECIAL_COLUMN the maps split further, and "
    "<b>Surface</b> and the special column (Method for sw) get a selector.",
]

_INTRO_DIFF = [
    "Did the experience do better than the control, and where? Each box is "
    "<b>Exp minus Ctl</b> over {ds} to {de} ({bx}° x {by}° boxes); the two "
    "runs are named at the top left of every map. For omp, oma, stdomp and "
    "stdoma only the observations both runs kept are counted.",

    "For those four, <b>red means Exp is better, blue that it is worse</b>: "
    "omp and oma show |bias Exp| - |bias Ctl|, stdomp and stdoma 100 (σ Exp - "
    "σ Ctl) / σ Ctl. nobs, dens, bcorr and obs are plain changes with no test "
    "(red = more, larger, higher).",

    "<b>Difference / Significance</b>: <b>difference</b> draws every box, "
    "<b>significance</b> how sure the test is (orange above 95 %, red above "
    "99 %), <b>significant only</b> the boxes above 95 %. With thousands of "
    "boxes about one in twenty passes by chance, so trust a region, not a lone "
    "box. <b>Black</b> boxes share no observation. How the tests work: "
    "<a href=\"{stats}\" style=\"color:var(--accent)\">the statistics page</a>. "
    "Flip (F) switches between the last two maps.",
]


def _intro_html(paragraphs: List[str], heading: str,
                common: Dict[str, Any]) -> str:
    """Left-aligned readable block for the viewer header.

    Uses <span style=display:block> because the viewer wraps the text in
    a <p>, where <div> is not allowed.
    """
    from pikobs.web.viewer import docs_url
    fmt = dict(bx=common['boxsizex'], by=common['boxsizey'],
               ds=common['datestart'], de=common['dateend'],
               stats=docs_url("stats.html"))
    block = ('<span style="display:block;margin:10px 0 0 0;'
             'font-size:14px;color:inherit;font-weight:bold;">'
             f'{heading}</span>')
    for par in paragraphs:
        block += ('<span style="display:block;margin:6px 0 0 0;'
                  'line-height:1.5;">' + par.format(**fmt) + '</span>')
    return ('<span style="display:block;max-width:1100px;margin:0 auto;'
            'text-align:left;font-size:13.5px;color:#d5dbdf;">'
            f'{block}</span>')


def _write_viewer(items: List[Dict[str, Any]], pathwork: str,
                  is_diff: bool, common: Dict[str, Any]) -> None:
    # the two halves of the map together, the projection first
    keys = [_RUN_KEY, "family", "proj", "region", "land_ocean", "flag", "function"]
    if any(it['panel'] == PANEL_CONF for it in items):
        keys.append("panel")
    keys += ["layer", "varno", "vcoord", "id_stn"]
    if any(it['special'] != 'all' for it in items):
        keys.append("special")

    key_labels = {
        _RUN_KEY: ("Comparison (control vs experience)"
                   if is_diff else "Experience"),
        "panel":   "Difference / Significance",
        "vcoord":  "Vcoord / Channel",
        "proj":    "Projection",
        "special": special_key_label({it.get("family") for it in items}),
    }
    if is_diff:
        intro = _intro_html(_INTRO_DIFF,
                            "How to read these maps: control vs experience",
                            common)
    else:
        intro = _intro_html(_INTRO_SINGLE,
                            "How to read these maps: single experience",
                            common)

    print(f"[scatter] viewer selectors: {keys}")
    _call_generate_web(
        items, keys,
        os.path.join(pathwork, "pikobs_scatter_viewer.html"),
        title=("Pikobs Scatter Viewer - control vs experience"
               if is_diff else "Pikobs Scatter Viewer"),
        subtitle=intro,
        key_labels=key_labels,
        enable_play=False,
    )


def _generic_generate_web():
    """Return pikobs.web.viewer.generate_web.

    ``pikobs.generate_web`` is shadowed by spatial.generate_web (the
    correlogram viewer), so the generic viewer is imported explicitly.
    """
    try:
        from pikobs.web.viewer import generate_web
        return generate_web
    except ImportError as exc:
        raise RuntimeError(
            "generic viewer pikobs.web.viewer.generate_web not found "
            f"({exc})") from exc


def _call_generate_web(items, keys, out_html, **optional) -> None:
    """Call the generic viewer, dropping keywords an older copy lacks."""
    fn     = _generic_generate_web()
    params = inspect.signature(fn).parameters
    kwargs = {k: v for k, v in optional.items() if k in params}
    dropped = sorted(set(optional) - set(kwargs))
    if dropped:
        print(f"[scatter] viewer does not accept {dropped}, "
              f"called without them", file=sys.stderr)
    fn(items, keys, out_html, **kwargs)


