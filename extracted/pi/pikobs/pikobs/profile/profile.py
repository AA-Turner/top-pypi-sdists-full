#!/usr/bin/python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_profile.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""===================================================
pikobs.profile -- Vertical profiles, level by level
===================================================

Every observation carries an error the system assigns to it, and the whole
analysis rests on that number being right. A profile is where you see
whether it is: level by level, the sigma of the departures against the
error the system expects.

``profile`` draws, for every run and every level: how many observations
there are, the bias and the sigma of the departures, the assigned
observation error, and their ratio.

With a control, each experience gets one more figure with the change of
the bias and of the sigma, level by level, the runs matched observation by
observation and every level tested.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_profile_exp.sh
   chmod +x run_profile_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_profile_cont_exp.sh
   chmod +x run_profile_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_profile_cont_exp.sh
   ./run_profile_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period, of every run, in parallel.

.. code-block:: text

   [profile] input check OK: 17 cycles x 1 run(s) x 1 family(ies), 17 files, 2.0 GB
   [profile] extraction time: 10.4s (17/17 files)
   [profile] plots: 168 tasks
   [profile] plot time: 91.4s (168/168)

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* `one run on its own <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_profile_exp/pikobs_profile_viewer.html>`__
* `G0 against G2 <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_profile/pikobs_profile_viewer.html>`__, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**One pass per file.** Every 6-h file is read once and the sums of every
station, level and varno come out of that single scan. Only
numbers count: an empty field is not a zero, and each quantity keeps its
own count, so an observation without O-A still counts for O-P.

**The levels.** Each family uses its own vertical coordinate, as
``family.py`` defines it; see :doc:`families`.

**Matching.** With a control, an observation is the same in both runs when
its key agrees: the station, position, time and level, as in every module
(see :doc:`match`).

**The same axes everywhere.** The limits of every panel are computed once
across all the runs of a group, so flipping between them in the viewer
never makes the axes jump.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_profile_exp.sh run_profile_cont_exp.sh

----

3. A run
========

+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Panel        | What it shows                                                                                                                                 |
+==============+===============================================================================================================================================+
| Observations | how many observations every level rests on                                                                                                    |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Departure    | the bias (thin) and the sigma (thick) of each level, with the assigned observation error (dotted) and the Desroziers estimate of it (crosses) |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| Key          | the lines, and the elevations with their number of observations                                                                               |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------+

.. image:: _static/profile_run.png
   :alt: One run: observations, departure and ratio
   :align: center
   :width: 100%

Read the sigma against the two errors beside it. The assigned error is
what the system gives each observation; the Desroziers estimate,
sqrt(E[(O-A)(O-P)]), is the error the analysis actually sees in the data
(Desroziers et al., 2005). Where the two part, the assigned error is off.

For radar, ``FIT_RADAR="on"`` goes one step further: after the run, profile
fits the error model of the radar -- per network, C or U, and per class of
elevation, the form base + slope dh + accel dh^2 above an onset -- to the
Desroziers estimate of that run. It leaves in ``<family>/fit_<run>/`` the
coefficients, the table ready to paste into ``radar_obs_error.py`` and one
figure of the fit per network, and on the figures of one elevation against
height it draws the fitted error (long dashes) beside the current model
(dash-dot). Off by default: it is a calibration, not a daily diagnostic.

``FIT_RADAR_TARGET`` says what the fit aims at: ``desroziers`` (the
default, which needs O-A; without it the fit falls back on the sigma of
O-P, and says so), ``sigma`` (the sigma of O-P), or ``sigma3`` -- the sigma
of O-P within 3 sigma of its cell, a network, an elevation and one vcoord,
each on its own: the sums of the run give every cell its mean and sigma,
the radar files are read a second time and what lies beyond 3 sigma is
left out. The table ``radar_obs_error_calibration_sigma3_<run>.csv`` says
how much.

A missing or empty file does not stop a run: the log and the viewer say
which cycles, and the figures are drawn without them.

The OBS_ERROR the assimilation used is always drawn, beside the sigma and
the bias. ``ERROR_CURVES`` adds other error curves: ``desroziers``, and on
radar ``model`` and ``model_fit``. The
viewer gives the formula of those drawn, and of those only.

----

4. Comparing with a control
===========================

Each experience gets one more figure with the change, the runs matched
observation by observation:

+--------------+-------------------------------------------------------------------------------------------------------+
| Panel        | What it shows                                                                                         |
+==============+=======================================================================================================+
| Bias change  | abs(bias of the experience) - abs(bias of the control): left of zero the experience is closer to zero |
+--------------+-------------------------------------------------------------------------------------------------------+
| Sigma change | 100 x (sigma_exp - sigma_ctl) / sigma_ctl, in percent: left of zero the experience is narrower        |
+--------------+-------------------------------------------------------------------------------------------------------+

.. image:: _static/profile_change.png
   :alt: An experience against a control
   :align: center
   :width: 100%

The tests come from :doc:`stats`: the paired t-test on the bias, the Pitman-Morgan test
on the sigma. With one elevation, every level carries its mark on the left
edge; with several, the mark sits on the point itself:

+------------+------------------------------------------------------------------+
| Mark       | Meaning                                                          |
+============+==================================================================+
| red dot    | the experience is better at that level, and the test passes 95 % |
+------------+------------------------------------------------------------------+
| blue dot   | the control is better, and the test passes 95 %                  |
+------------+------------------------------------------------------------------+
| hollow dot | the change is not larger than noise (one elevation at a time)    |
+------------+------------------------------------------------------------------+

The background is tinted on the side where each run wins, and the header
counts the levels: ``bias: 3 red, 1 blue   sigma: 12 red, 0 blue``.

----

5. Stations and instrument types
================================

+------------+--------------------------------------------------------------------+
| Token      | Figures produced                                                   |
+============+====================================================================+
| ``join``   | one, every station together                                        |
+------------+--------------------------------------------------------------------+
| ``all``    | one per station; on ai, sf, ua, gp and csr one per instrument type |
+------------+--------------------------------------------------------------------+
| ``C%``     | the stations whose id starts with C, together                      |
+------------+--------------------------------------------------------------------+
| ``=cashr`` | that station only                                                  |
+------------+--------------------------------------------------------------------+

On ``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` the tokens name instrument
types rather than stations -- ``pilot``, ``=TEMP``, ``35`` -- the same
way in every module; see :doc:`families`.

----

6. The viewer
=============

``pikobs_profile_viewer.html`` has one selector per dimension: Experience,
Family, Fonction, Region, Criteria, Station, Varno, Elevation and Axis.
Each run is its own entry, and with a control the change of each experience
is another, so **Flip** moves between them on the same axes.

----

7. Output layout
================

::

   $PATHWORK/
   ├── pikobs_profile_viewer.html
   ├── profile_timing.json
   └── <family>/
       ├── profile_<run>_<start>_<end>_<family>.db
       └── profile_<run>_<family>_<fonction>_varno<N>_<station>_<region>[_<surface>][_<special>]_<flag>[_elev<E>_<axis>].png

----

8. Support
==========

Bugs and feature requests:
   `<https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`_
"""

import csv
import json
import os
import shutil
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

import dask
from dask.distributed import Client

# a region is a box or a polygon; the module does not need to know
from pikobs.configobs import regionsobs
from pikobs.configobs.landmask import register_surface, surface_sql
from pikobs.configobs.special_family import (radar_elevation_column,
                                             radar_elevation_select,
                                             special_key_label,
                                             special_select)
import pikobs
from pikobs.figures import svg_enabled
from pikobs.obsdb import (check_input_files, combine as _combine_rows,
                          cycle_path, cycles as _cycles, fmt_bytes,
                          input_size, open_result, table_columns, work_db)
from pikobs.obsdb.obsdb import split_tokens as _split_tokens  # shared, once
from pikobs.parallel import run_tasks
from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.stations.stations import (expand_station_selectors,
                                      parse_station_tokens)
from pikobs.web.viewer import generate_web
from pikobs.web.runs import runs_block

RADAR_FAMILIES = ('ra', 'radar')
FUNCTIONS = ('omp', 'oma')
MIN_OBS_PER_LEVEL = 30

# Radar: 1-km height bins; the range comes in its own superobservation
# steps (10 km in the operational files) and is kept as it is.
RADAR_HEIGHT_BIN_M = 1000.0

# n_da, s_pa, s_pd, s_ad: over the observations that have both O-P and
# O-A -- the Desroziers estimate of the observation error,
# sigma_o^2 = E[(O-A)(O-P)], taken as their covariance
_SUMS = ("n_omp, s_omp, s2_omp, n_oma, s_oma, s2_oma, n_err, s_err, s2_err, "
         "n_fg, s_fg2, n_obs, n_rej, n_acc, n_da, s_pa, s_pd, s_ad")
_PROF_COLS = ("region, flag, land_ocean, special, id_stn, codtyp, varno, "
              "elev, lev, hgt, " + _SUMS)
_DDL_PROF = """
    CREATE TABLE IF NOT EXISTS prof (
        region TEXT, flag TEXT, land_ocean TEXT, special TEXT, id_stn TEXT,
        codtyp INTEGER, varno INTEGER,
        elev TEXT, lev REAL, hgt REAL,
        n_omp INTEGER, s_omp FLOAT, s2_omp FLOAT,
        n_oma INTEGER, s_oma FLOAT, s2_oma FLOAT,
        n_err INTEGER, s_err FLOAT, s2_err FLOAT,
        n_fg INTEGER, s_fg2 FLOAT, n_obs INTEGER, n_rej INTEGER,
        n_acc INTEGER, n_da INTEGER, s_pa FLOAT, s_pd FLOAT, s_ad FLOAT
    );
"""
# With a control: the same observations in both runs, summed together so
# the paired tests can be run on each level.
_PAIR_COLS = ("region, flag, land_ocean, special, id_stn, codtyp, varno, "
              "elev, lev, hgt, n, "
              "c_omp, c2_omp, e_omp, e2_omp, ce_omp, n_a, c_oma, c2_oma, "
              "e_oma, e2_oma, ce_oma")
_DDL_PAIR = """
    CREATE TABLE IF NOT EXISTS pair (
        region TEXT, flag TEXT, land_ocean TEXT, special TEXT, id_stn TEXT,
        codtyp INTEGER, varno INTEGER,
        elev TEXT, lev REAL, hgt REAL, n INTEGER,
        c_omp FLOAT, c2_omp FLOAT, e_omp FLOAT, e2_omp FLOAT, ce_omp FLOAT,
        n_a INTEGER, c_oma FLOAT, c2_oma FLOAT, e_oma FLOAT, e2_oma FLOAT,
        ce_oma FLOAT
    );
"""


def _num(col: str) -> str:
    """The column when it holds a number, NULL otherwise: an empty field
    is not a zero."""
    return f"(CASE WHEN typeof({col}) IN ('real', 'integer') THEN {col} END)"


def _safe(text) -> str:
    import re
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


def is_radar(family: str) -> bool:
    return family in RADAR_FAMILIES


def db_path(work_path: str, family: str, tag: str, date_start: str,
            date_end: str) -> str:
    return os.path.join(work_path, family,
                        f"profile_{_safe(tag)}_{date_start}_{date_end}_"
                        f"{family}.db")



def _cells(regions, surfaces, flags):
    """[(region, surface, flag, SQL condition)] of every region, surface
    and criteria.

    The surface goes right after the region box; all adds nothing, so a
    run without a surface filter reads the same condition as before.
    """
    out = []
    for region in regions:
        latlon = regionsobs.criteria(region)
        for lo in surfaces:
            for flag in flags:
                out.append((region, lo, flag,
                            f"1=1 {latlon}{surface_sql(lo)} "
                            f"{pikobs.flag_criteria(flag)}"))
    return out


def _level_exprs(family: str, head_cols, alias_h: str = "",
                 alias_d: str = ""):
    """(elev, lev, hgt) SQL of a family.

    Radar: the nominal PPI elevation to a tenth of a degree, the slant
    range in km as the files give it, and the beam height binned to 1 km
    (centre of the bin). Other families: the vertical coordinate of
    family.py, with no elevation and no height.
    """
    h = f"{alias_h}." if alias_h else ""
    d = f"{alias_d}." if alias_d else ""
    if is_radar(family):
        # the elevation is defined once, in special_family.py
        elev = radar_elevation_select(head_cols, h)
        lev = f"ROUND({d}range / 1000.0, 3)"
        hgt = (f"(CAST({d}vcoord / {RADAR_HEIGHT_BIN_M} AS INTEGER) + 0.5) "
               f"* {RADAR_HEIGHT_BIN_M / 1000.0}")
        return elev, lev, hgt
    _, vcoord, _, _, _, _ = pikobs.family(family)
    expr = (vcoord or '').strip() or 'vcoord'
    if d and expr != 'vcoord':
        expr = expr.replace('vcoord', f'{d}vcoord')
    elif d:
        expr = f'{d}vcoord'
    return "'na'", expr, "NULL"


# ─────────────────────────────────────────────────────────────────────────────
# Extraction
# ─────────────────────────────────────────────────────────────────────────────

def create_prof_single(task: Dict[str, Any]) -> Optional[int]:
    """Sums of one run, per station, level, height and elevation."""
    family, path = task['family'], task['filein']
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        print(f"[profile] missing or empty file, skipped: {path}",
              file=sys.stderr, flush=True)
        return None
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if task['varnos']:
        element = ",".join(str(v) for v in task['varnos'])
    with work_db(attach={'db': path}) as (conn, mem_uri):
        conn.execute(_DDL_PROF)
        dcols = {c.lower() for c in table_columns(conn, 'DATA', 'db')}
        hcols = table_columns(conn, 'HEADER', 'db')
        elev, lev, hgt = _level_exprs(family, hcols)
        codtyp = "codtyp" if 'codtyp' in {c.lower() for c in hcols} else "0"
        # the special column, or the constant 'all': grouping by a
        # constant changes no group. Radar is split by its elevation
        # already, a level of its own here.
        sp_sel, _ = special_select(family, hcols,
                                   bool(task.get('special_on'))
                                   and not is_radar(family))
        surfaces = list(task.get('land_oceans') or ['all'])
        register_surface(conn, surfaces, task.get('pathwork'))
        # a polygon region (hrdps, the EMET domains) is an SQL function
        # of its own: without it a polygon stopped the extraction
        import inspect
        kw = ({'pathwork': task.get('pathwork')} if 'pathwork' in
              inspect.signature(regionsobs.register).parameters else {})
        regionsobs.register(conn, list(task.get('regions') or []), **kw)
        # a file without an analysis has no O-A: that column is NULL then
        omp, obs = _num('omp'), _num('obsvalue')
        oma = _num('oma') if 'oma' in dcols else "NULL"
        err = _num('obs_error') if 'obs_error' in dcols else "NULL"
        fg = _num('fg_error') if 'fg_error' in dcols else "NULL"
        # every region x criterion from one grouping of the file, as in
        # timeserie: the rows are grouped once by station, levels, flag value
        # and the regions they fall in (bits), and each combination is read
        # from those groups -- the criteria only look at flag. The loop below
        # read the whole file once per combination; it stays for a criterion
        # that would look at another column.
        import re as _re
        _plain = {"and", "or", "not", "flag", "in", "between", "is", "null"}
        only_flag = all(
            set(_re.findall(r"[a-z_]\w*", pikobs.flag_criteria(f).lower()))
            <= _plain for f in task['flags'])
        regions = list(task['regions'])
        # a region on a surface is one bit; with all alone the bits are the
        # regions, and their conditions the same text as before
        cells = [(r, lo) for r in regions for lo in surfaces]
        if only_flag and len(cells) <= 60:
            rb = " + ".join(
                f"(CASE WHEN {_cells([r], [lo], ['all'])[0][3]} THEN {1 << k} ELSE 0 END)"
                for k, (r, lo) in enumerate(cells))
            # only the rows at least one criterion keeps: the others go into
            # no combination, and grouping them cost as much as the rest
            anyflag = " OR ".join(f"(1=1 {pikobs.flag_criteria(f)})"
                                  for f in task['flags'])
            conn.execute(f"""
                CREATE TEMP TABLE pre AS
                SELECT id_stn, {codtyp} AS cod, varno, {elev} AS e, {lev} AS l,
                       {sp_sel} AS sp,
                       {hgt} AS h, flag, ({rb}) AS rb,
                       COUNT({omp}) AS n_omp, SUM({omp}) AS s_omp,
                       SUM({omp}*{omp}) AS q_omp,
                       COUNT({oma}) AS n_oma, SUM({oma}) AS s_oma,
                       SUM({oma}*{oma}) AS q_oma,
                       COUNT({err}) AS n_err, SUM({err}) AS s_err,
                       SUM({err}*{err}) AS q_err,
                       COUNT({fg}) AS n_fg, SUM({fg}*{fg}) AS q_fg,
                       COUNT({obs}) AS n_obs,
                       SUM((flag & 512) = 512) AS n_rej,
                       SUM((flag & 4096) = 4096) AS n_ass,
                       COUNT({omp}*{oma}) AS n_pa, SUM({omp}*{oma}) AS s_pa,
                       SUM(CASE WHEN {oma} IS NOT NULL THEN {omp} END) AS s_p,
                       SUM(CASE WHEN {omp} IS NOT NULL THEN {oma} END) AS s_a
                FROM db.header NATURAL JOIN db.data
                WHERE varno IN ({element}) {VCOCRIT} AND ({anyflag})
                GROUP BY id_stn, cod, varno, e, l, h, flag, rb, sp;""")
            for k, (region, surf) in enumerate(cells):
                for flag in task['flags']:
                    w = f"(rb & {1 << k}) != 0 {pikobs.flag_criteria(flag)}"
                    conn.execute(f"""
                        INSERT INTO prof ({_PROF_COLS})
                        SELECT '{region}', '{flag}', '{surf}', sp, id_stn, cod,
                               varno, e, l, h,
                               SUM(n_omp), SUM(s_omp), SUM(q_omp),
                               SUM(n_oma), SUM(s_oma), SUM(q_oma),
                               SUM(n_err), SUM(s_err), SUM(q_err),
                               SUM(n_fg), SUM(q_fg), SUM(n_obs),
                               SUM(n_rej), SUM(n_ass),
                               SUM(n_pa), SUM(s_pa), SUM(s_p), SUM(s_a)
                        FROM pre WHERE {w}
                        GROUP BY id_stn, cod, varno, e, l, h, sp;""")
        else:
            for region, surf, flag, cond in _cells(task['regions'], surfaces,
                                                   task['flags']):
                conn.execute(f"""
                    INSERT INTO prof ({_PROF_COLS})
                    SELECT '{region}', '{flag}', '{surf}', {sp_sel} AS sp,
                           id_stn, {codtyp}, varno,
                           {elev} AS e, {lev} AS l, {hgt} AS h,
                           COUNT({omp}), SUM({omp}), SUM({omp}*{omp}),
                           COUNT({oma}), SUM({oma}), SUM({oma}*{oma}),
                           COUNT({err}), SUM({err}), SUM({err}*{err}),
                           COUNT({fg}), SUM({fg}*{fg}), COUNT({obs}),
                           SUM((flag & 512) = 512), SUM((flag & 4096) = 4096),
                           COUNT({omp}*{oma}), SUM({omp}*{oma}),
                           SUM(CASE WHEN {oma} IS NOT NULL THEN {omp} END),
                           SUM(CASE WHEN {omp} IS NOT NULL THEN {oma} END)
                    FROM db.header NATURAL JOIN db.data
                    WHERE varno IN ({element}) {VCOCRIT} AND {cond}
                    GROUP BY id_stn, {codtyp}, varno, e, l, h, sp;""")
        _combine_rows(task['db_new'], mem_uri, 'prof', _PROF_COLS,
                      ddl=_DDL_PROF, module='profile')
    return 1


def _key(family: str, hcols) -> List[str]:
    """What makes an observation the same one in two runs.

    Radar: the station, the time of the sweep, the azimuth, the elevation
    and the range -- the latitude and longitude of the header are those of
    the antenna, shared by every observation of a station. Others: the
    station, position, time and level, as in scatter.
    """
    if is_radar(family):
        cols = {c.upper() for c in hcols}
        ecol = radar_elevation_column(cols)
        az = 'CENTER_AZIMUTH' if 'CENTER_AZIMUTH' in cols else None
        tcol = 'TIME_START' if 'TIME_START' in cols else 'TIME'
        key = [("id_stn", "h.id_stn"), ("t", f"h.{tcol}"), ("dt", "h.date")]
        if az:
            key.append(("az", f"ROUND(h.{az}, 3)"))
        if ecol:
            key.append(("el", f"ROUND(h.{ecol}, 2)"))
        key.append(("rg", "d.range"))
        key.append(("vn", "d.varno"))
        return key
    return [("id_stn", "h.id_stn"), ("klat", "ROUND(h.lat, 4)"),
            ("klon", "ROUND(h.lon, 4)"), ("dt", "h.date"), ("t", "h.time"),
            ("vn", "d.varno"), ("vr", "d.vcoord")]


def create_prof_matched(task: Dict[str, Any]) -> Optional[int]:
    """Both runs on the same observations, summed for the paired tests."""
    family = task['family']
    for p in (task['ctl_file'], task['exp_file']):
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            print(f"[profile] missing or empty file, skipped: {p}",
                  file=sys.stderr, flush=True)
            return None
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if task['varnos']:
        element = ",".join(str(v) for v in task['varnos'])
    with work_db(attach={'ctl': task['ctl_file'],
                         'exp': task['exp_file']}) as (conn, mem_uri):
        conn.execute(_DDL_PAIR)
        hcols = table_columns(conn, 'HEADER', 'ctl')
        c_oma = ({c.lower() for c in table_columns(conn, 'DATA', 'ctl')}
                 >= {'oma'})
        e_oma = ({c.lower() for c in table_columns(conn, 'DATA', 'exp')}
                 >= {'oma'})
        elev, lev, hgt = _level_exprs(family, hcols, 'h', 'd')
        codtyp = "h.codtyp" if 'codtyp' in {c.lower() for c in hcols} else "0"
        sp_sel, _ = special_select(family, hcols,
                                   bool(task.get('special_on'))
                                   and not is_radar(family), prefix='h.')
        surfaces = list(task.get('land_oceans') or ['all'])
        register_surface(conn, surfaces, task.get('pathwork'))
        # a polygon region (hrdps, the EMET domains) is an SQL function
        # of its own: without it a polygon stopped the extraction
        import inspect
        kw = ({'pathwork': task.get('pathwork')} if 'pathwork' in
              inspect.signature(regionsobs.register).parameters else {})
        regionsobs.register(conn, list(task.get('regions') or []), **kw)
        key = _key(family, hcols)
        # MATCH=on keeps profile's own key (it knows radar pairs on
        # range, not vcoord); a field list from MATCH replaces it for
        # the join. Either way pikobs.match's rank pairs a repeated key
        # one to one.
        from pikobs.match import (DEFAULT_KEY, FIELDS, MatchSpec,
                                  count_repeats, rank_select)
        fields = tuple(task.get('match_fields') or ())
        spec = MatchSpec(True, fields or DEFAULT_KEY)
        names_run = tuple(task.get('names') or ('control', 'experience'))
        jkey = ([(f"k_{f}", FIELDS[f].format(h='h', d='d'))
                 for f in fields] if fields else key)
        key_sel = ", ".join(f"{expr} AS {name}" for name, expr in key)
        if fields:
            key_sel += ", " + ", ".join(f"{e} AS {n}" for n, e in jkey)
        key_sel += ", " + rank_select([e for _, e in jkey], "d.obsvalue")
        crit = VCOCRIT.replace('vcoord', 'd.vcoord')
        # only rows that can be half of a pair: without an O-P or an O-A a
        # row adds nothing to the sums below, and on the radiances that is
        # most of the file (iasi: about one row in twenty has a departure)
        c_dep = "AND (d.omp IS NOT NULL" + (" OR d.oma IS NOT NULL)" if c_oma else ")")
        e_dep = "AND (d.omp IS NOT NULL" + (" OR d.oma IS NOT NULL)" if e_oma else ")")
        conn.execute(f"""
            CREATE TEMP TABLE c AS
            SELECT {key_sel}, h.lat AS lat, h.lon AS lon, d.flag AS flag,
                   {codtyp} AS codtyp, {sp_sel} AS sp, {elev} AS elev,
                   {lev} AS lev,
                   {hgt} AS hgt, {_num('d.omp')} AS omp,
                   {_num('d.oma') if c_oma else 'NULL'} AS oma
            FROM ctl.header h JOIN ctl.data d USING(id_obs)
            WHERE d.varno IN ({element}) {crit} {c_dep};""")
        conn.execute(f"""
            CREATE TEMP TABLE e AS
            SELECT {key_sel}, {_num('d.omp')} AS omp,
                   {_num('d.oma') if e_oma else 'NULL'} AS oma
            FROM exp.header h JOIN exp.data d USING(id_obs)
            WHERE d.varno IN ({element}) {crit} {e_dep};""")
        jnames = [n for n, _ in jkey]
        names = jnames + ['k_rank']
        conn.execute(f"CREATE INDEX e_key ON e ({', '.join(names)});")
        on = " AND ".join(f"e.{n} = c.{n}" for n in names)
        repeats = {names_run[0]: count_repeats(conn, 'c', jnames,
                                     where="omp IS NOT NULL OR oma IS NOT NULL"),
                   names_run[1]: count_repeats(conn, 'e', jnames,
                                     where="omp IS NOT NULL OR oma IS NOT NULL")}
        conn.execute(f"""
            CREATE TEMP TABLE pairs AS
            SELECT c.id_stn AS id_stn, c.codtyp AS codtyp, c.vn AS varno,
                   c.lat AS lat, c.lon AS lon, c.flag AS flag,
                   c.sp AS sp, c.elev AS elev, c.lev AS lev, c.hgt AS hgt,
                   c.omp AS c_omp, e.omp AS e_omp,
                   c.oma AS c_oma, e.oma AS e_oma
            FROM c JOIN e ON {on};""")
        n_pairs = conn.execute("SELECT COUNT(*) FROM pairs;").fetchone()[0]
        if not n_pairs:
            return {'pairs': 0, 'repeats': repeats}
        both_p = "c_omp IS NOT NULL AND e_omp IS NOT NULL"
        both_a = "c_oma IS NOT NULL AND e_oma IS NOT NULL"
        for region, surf, flag, cond in _cells(task['regions'], surfaces,
                                               task['flags']):
            conn.execute(f"""
                INSERT INTO pair ({_PAIR_COLS})
                SELECT '{region}', '{flag}', '{surf}', sp, id_stn, codtyp,
                       varno, elev,
                       lev, hgt,
                       SUM({both_p}),
                       SUM(CASE WHEN {both_p} THEN c_omp END),
                       SUM(CASE WHEN {both_p} THEN c_omp*c_omp END),
                       SUM(CASE WHEN {both_p} THEN e_omp END),
                       SUM(CASE WHEN {both_p} THEN e_omp*e_omp END),
                       SUM(CASE WHEN {both_p} THEN c_omp*e_omp END),
                       SUM({both_a}),
                       SUM(CASE WHEN {both_a} THEN c_oma END),
                       SUM(CASE WHEN {both_a} THEN c_oma*c_oma END),
                       SUM(CASE WHEN {both_a} THEN e_oma END),
                       SUM(CASE WHEN {both_a} THEN e_oma*e_oma END),
                       SUM(CASE WHEN {both_a} THEN c_oma*e_oma END)
                FROM pairs WHERE {cond}
                GROUP BY id_stn, codtyp, varno, elev, lev, hgt, sp;""")
        _combine_rows(task['db_new'], mem_uri, 'pair', _PAIR_COLS,
                      ddl=_DDL_PAIR, module='profile')
    return {'pairs': n_pairs, 'repeats': repeats}


def _extract_task(task) -> Optional[int]:
    import traceback
    try:
        if task.get('ctl_file'):
            return create_prof_matched(task)
        return create_prof_single(task)
    except Exception:
        print(f"[profile] extraction failed for "
              f"{task.get('filein') or task.get('ctl_file')}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def _index_task(path: str) -> Optional[str]:
    try:
        with open_result(path) as conn:
            for t in ('prof', 'pair'):
                if conn.execute("SELECT 1 FROM sqlite_master WHERE type = "
                                "'table' AND name = ?;", (t,)).fetchone():
                    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{t} ON {t} "
                                 f"(region, flag, land_ocean, special, varno, elev);")
        return path
    except Exception as exc:
        print(f"[profile] indexing {path} failed: {exc}", file=sys.stderr,
              flush=True)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# The radar calibration table
# ─────────────────────────────────────────────────────────────────────────────

def desroziers(n, s_pa, s_p, s_a) -> float:
    """sigma_o from E[(O-A)(O-P)] -- Desroziers et al. (2005).

    Taken as the covariance of O-A and O-P, so a bias does not enter it.
    It holds when the analysis weighs the observations with errors close to
    the real ones; iterate it -- estimate, re-run the cycle, estimate again.
    NaN when there is no O-A, or when the covariance is not positive.
    """
    if not n or s_pa is None or s_p is None or s_a is None:
        return float('nan')
    cov = s_pa / n - (s_p / n) * (s_a / n)
    return cov ** 0.5 if cov > 0 else float('nan')


def write_radar_calibration(db_file: str, run: str, out_csv: str,
                            with_model: bool, min_obs: int,
                            surface: str = 'all') -> int:
    """Per station, elevation and 1-km height: the real sigma of O-P, the
    mean assigned error, the background error, what the system expects,
    and -- with the model on -- the theoretical error and its margin."""
    from pikobs.profile.radar_obs_error import model_obs_error
    rows_out = 0
    try:
        with open_result(db_file) as conn:
            rows = conn.execute(
                "SELECT region, flag, id_stn, elev, hgt, SUM(n_omp), "
                "SUM(s_omp), SUM(s2_omp), SUM(n_err), SUM(s_err), "
                "SUM(s2_err), SUM(n_fg), SUM(s_fg2), SUM(n_da), SUM(s_pa), "
                "SUM(s_pd), SUM(s_ad) FROM prof "
                "WHERE elev != 'na' AND land_ocean = ? "
                "GROUP BY region, flag, id_stn, elev, hgt "
                "ORDER BY region, flag, id_stn, CAST(elev AS REAL), hgt;", (surface,)
            ).fetchall()
    except Exception as exc:
        print(f"[profile] calibration table skipped: {exc}", file=sys.stderr,
              flush=True)
        return 0
    new = not os.path.exists(out_csv)
    with open(out_csv, 'a', newline='') as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["run", "region", "criteria", "station", "elevation",
                        "height_km", "n", "bias", "std", "obs_err_mean",
                        "fg_err_rms", "expected_std", "std_over_expected",
                        "n_desroziers", "obs_err_desroziers"]
                       + (["obs_err_model", "margin_model_minus_std"]
                          if with_model else []))
        for (region, flag, stn, elev, hgt, n, s, s2, ne, se, s2e,
             nf, sf2, nda, spa, spd, sad) in rows:
            if not n or n < min_obs:
                continue
            mean = s / n
            std = max(s2 / n - mean * mean, 0.0) ** 0.5
            oer = se / ne if ne else float('nan')
            oer_rms = (s2e / ne) ** 0.5 if ne else float('nan')
            fg_rms = (sf2 / nf) ** 0.5 if nf else float('nan')
            expected = ((oer_rms ** 2 + fg_rms ** 2) ** 0.5
                        if ne and nf else float('nan'))
            ratio = std / expected if expected == expected and expected \
                else float('nan')
            des = desroziers(nda, spa, spd, sad)
            line = [run, region, flag, stn, elev, f"{hgt:g}", int(n),
                    f"{mean:.4f}", f"{std:.4f}", f"{oer:.4f}",
                    f"{fg_rms:.4f}", f"{expected:.4f}", f"{ratio:.4f}",
                    int(nda or 0), f"{des:.4f}"]
            if with_model:
                m = float(model_obs_error([hgt], float(elev), stn)[0])
                line += [f"{m:.4f}", f"{m - std:+.4f}"]
            w.writerow(line)
            rows_out += 1
    return rows_out


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def _report_timing(timing, pathwork) -> None:
    sec, p = timing['seconds'], "[profile]"
    print(f"{p} -------------------- run time --------------------",
          flush=True)
    print(f"{p} input        {fmt_bytes(timing['input_bytes']):>10s}   "
          f"{timing['input_files']} files, {timing['cycles']} cycles, "
          f"{timing['runs']} run(s)", flush=True)
    for phase in ('extraction', 'plots'):
        if phase in sec:
            print(f"{p} {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(f"{p} total        {sec['total']:>8.1f} s   "
          f"({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
          flush=True)
    try:
        with open(os.path.join(pathwork, "profile_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError:
        pass


def _missing_input(runs, families, date_start, date_end):
    """{(run, family): [cycles missing or empty]}, said in the log as found;
    None when not a single file holds data in the period."""
    cycles = _cycles(date_start, date_end)
    out, found = {}, False
    for name, path in runs:
        for family in families:
            miss = []
            for c in cycles:
                f = cycle_path(path, c, family)
                if os.path.isfile(f) and os.path.getsize(f) > 0:
                    found = True
                else:
                    miss.append(c)
            if miss:
                out[(name, family)] = miss
                print(f"[profile] WARNING: {name} {family}: {len(miss)}/"
                      f"{len(cycles)} cycles missing or empty, drawn without "
                      f"them: {miss[0]} .. {miss[-1]}", flush=True)
    return out if found else None


def _missing_note(missing, n_cycles: int) -> str:
    """The box at the head of the viewer's About when cycles were missing."""
    if not missing:
        return ""
    import html
    rows = "".join(
        f"<li>{html.escape(str(run))} &middot; {html.escape(fam)}: {len(cyc)} of "
        f"{n_cycles} cycles ({cyc[0]} .. {cyc[-1]})</li>"
        for (run, fam), cyc in sorted(missing.items()))
    return ('<div style="margin:0 0 10px;padding:8px 12px;border-left:4px solid '
            '#d9822b;background:#fff4e5;color:#7a4510"><b>Input incomplete.</b> '
            'The run went on without these files, missing or empty.'
            f'<ul style="margin:6px 0 0 18px">{rows}</ul></div>')


def _sigma3_file(args):
    """Pass two of sigma3, one file: per region, criteria, network,
    elevation and height, the count, and the sums of what lies within
    +/-3 sigma of that cell."""
    path, family, regions, flags, varnos, bounds_db, pathwork = args
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        return []
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if varnos:
        element = ",".join(str(v) for v in varnos)
    out = []
    with work_db(attach={'db': path, 'b': bounds_db}) as (conn, mem_uri):
        hcols = table_columns(conn, 'HEADER', 'db')
        elev, _lev, hgt = _level_exprs(family, hcols)
        import inspect
        kw = ({'pathwork': pathwork} if 'pathwork' in
              inspect.signature(regionsobs.register).parameters else {})
        regionsobs.register(conn, list(regions), **kw)
        omp = _num('omp')
        for region, _surf, flag, cond in _cells(regions, ['all'], flags):
            rows = conn.execute(f"""
                SELECT q.net, q.e, q.h, COUNT(q.v),
                       SUM(q.v BETWEEN b.lo AND b.hi),
                       SUM(CASE WHEN q.v BETWEEN b.lo AND b.hi THEN q.v END),
                       SUM(CASE WHEN q.v BETWEEN b.lo AND b.hi
                                THEN q.v * q.v END)
                FROM (SELECT substr(id_stn, 1, 1) AS net, {elev} AS e,
                             {hgt} AS h, {omp} AS v
                      FROM db.header NATURAL JOIN db.data
                      WHERE varno IN ({element}) {VCOCRIT} AND {cond}
                        AND {omp} IS NOT NULL) q
                JOIN b.bounds b ON b.region = ? AND b.flag = ?
                     AND b.net = q.net AND b.elev = q.e AND b.hgt = q.h
                GROUP BY q.net, q.e, q.h""", (region, flag)).fetchall()
            out += [(region, flag) + tuple(r) for r in rows]
    return out


def radar_sigma3(run, family, run_db, files, regions, flags, varnos,
                 pathwork, client) -> str:
    """The sigma of O-P within 3 sigma of its cell -- network, elevation,
    vcoord -- in a table the fit reads; returns its path."""
    import math
    import sqlite3
    out_dir = os.path.join(pathwork, family)
    os.makedirs(out_dir, exist_ok=True)
    bounds_db = os.path.join(out_dir, f"sigma3_bounds_{_safe(run)}.db")
    with open_result(run_db) as conn:
        rows = conn.execute(
            "SELECT region, flag, substr(id_stn, 1, 1), elev, hgt, SUM(n_omp), "
            "SUM(s_omp), SUM(s2_omp) FROM prof WHERE elev != 'na' AND "
            "land_ocean = 'all' GROUP BY region, flag, substr(id_stn, 1, 1), "
            "elev, hgt").fetchall()
    bounds = []
    for region, flag, net, e, h, n, s, q in rows:
        if not n or n < 2:
            continue
        m = s / n
        sd = math.sqrt(max(q / n - m * m, 0.0))
        bounds.append((region, flag, net, e, h, m - 3 * sd, m + 3 * sd))
    if os.path.exists(bounds_db):
        os.remove(bounds_db)
    with sqlite3.connect(bounds_db) as b:
        b.execute("CREATE TABLE bounds (region TEXT, flag TEXT, net TEXT, "
                  "elev TEXT, hgt REAL, lo REAL, hi REAL)")
        b.executemany("INSERT INTO bounds VALUES (?, ?, ?, ?, ?, ?, ?)", bounds)
    parts = run_tasks(_sigma3_file,
                      [((f, family, regions, flags, varnos, bounds_db,
                         pathwork),) for f in files], client, label='sigma3')
    acc = {}
    for part in parts:
        for region, flag, net, e, h, n_all, n3, s3, q3 in (part or []):
            a = acc.setdefault((region, flag, net, e, h), [0, 0, 0.0, 0.0])
            a[0] += n_all or 0
            a[1] += n3 or 0
            a[2] += s3 or 0.0
            a[3] += q3 or 0.0
    out_csv = os.path.join(out_dir, f"radar_obs_error_calibration_sigma3_"
                           f"{_safe(run)}.csv")
    import csv
    kept = total = 0
    with open(out_csv, "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["run", "region", "criteria", "station", "elevation",
                     "height_km", "n", "std", "n_all", "share_cut"])
        for (region, flag, net, e, h), (n_all, n3, s3, q3) in sorted(acc.items()):
            total += n_all
            if n3 < 2:
                continue
            kept += n3
            m = s3 / n3
            sd = math.sqrt(max(q3 / n3 - m * m, 0.0))
            wr.writerow([run, region, flag, net, e, h, n3, f"{sd:.6f}", n_all,
                         f"{(n_all - n3) / n_all:.5f}" if n_all else ""])
    cut = 100.0 * (total - kept) / total if total else 0.0
    print(f"[profile] {family} {run}: sigma3, {cut:.2f} % of the observations "
          f"beyond 3 sigma of their cell: {out_csv}", flush=True)
    return out_csv


def _curves_note(curves, fit_radar=False, target='desroziers') -> str:
    """The lines of the figures with their formulas, for the About of the
    viewer: the sigma and the bias, and only the error curves drawn."""
    aim = {'desroziers': 'the Desroziers estimate',
           'sigma': 'the sigma of O-P',
           'sigma3': ('the sigma of O-P within &plusmn;3&sigma; of its cell '
                      '(network, elevation, vcoord)')}.get(target, target)
    rows = ["<li><b>sigma</b> of the departure d (O-P or O-A) of each level: "
            "&sigma; = &radic;(mean(d&sup2;) &minus; mean(d)&sup2;); "
            "<b>bias</b>: mean(d).</li>"]
    # the error the assimilation used: always drawn
    rows.append("<li><b>OBS_ERROR used in the assimilation</b>: the mean, "
                    "per level, of the OBS_ERROR column of the files, over the "
                    "observations that were given one.</li>")
    if 'desroziers' in curves:
        rows.append("<li><b>Desroziers</b> (Desroziers et al., 2005): "
                    "&sigma;<sub>o</sub> &asymp; &radic;(E[(O&minus;A)(O&minus;P)] "
                    "&minus; E[O&minus;A]&middot;E[O&minus;P]), per level; it "
                    "needs O-A.</li>")
    if 'model' in curves:
        rows.append("<li><b>error model</b>, radar (radar_obs_error.py, the "
                    "calc_radvel_obs_error of the assimilation): "
                    "&sigma;<sub>o</sub>(h) = base + slope&middot;&Delta;h + "
                    "accel&middot;&Delta;h&sup2;, &Delta;h = max(0, h &minus; "
                    "onset), between 2 and 16 m/s; four coefficients per "
                    "network (C, U) and class of elevation.</li>")
    if 'model_fit' in curves and fit_radar:
        rows.append(f"<li><b>fitted on this run</b>, radar (FIT_RADAR): the same "
                    f"form, its coefficients fitted to {aim}, weighted by the "
                    f"number of observations; the table in "
                    f"&lt;family&gt;/fit_&lt;run&gt;/radar_obs_error_fitted.py.</li>")
    return ('<div style="margin:10px 0"><b>The lines of the figures</b>'
            '<ul style="margin:4px 0 0 18px">' + "".join(rows) + "</ul></div>")


def make_profile(runs, pathwork, datestart, dateend, regions, families,
                 flags_criteria, functions, varnos, id_stn, n_cpu,
                 control=None, svg: bool = False,
                 min_obs: int = MIN_OBS_PER_LEVEL,
                 obs_error_model: bool = False,
                 match: bool = True, land_ocean=('all',),
                 fit_radar: bool = False,
                 fit_radar_target: str = 'desroziers',
                 error_curves=('obs_error',),
                 special_column: str = 'off') -> int:
    # MATCH: on, off, or the fields of the key -- pikobs.match decides.
    # Past this point match is True / False as before; the key travels
    # in match_spec.
    from pikobs.match import parse_match
    if match is True or match is False:
        match = 'on' if match else 'off'
    match_spec = parse_match(match)
    match = match_spec.enabled
    from pikobs.profile.profile_plot import (plot_task, plan_figures,
                                             shared_limits)
    p = "[profile]"
    regions = _split_tokens(regions) or ['Monde']
    flags = _split_tokens(flags_criteria) or ['all']
    land_oceans = [lo for lo in (_split_tokens(land_ocean) or ['all'])
                   if lo in ('all', 'land', 'ocean')] or ['all']
    special_on = str(special_column).strip().lower() in ('on', 'true', '1',
                                                         'yes')
    # the radar calibration table holds one surface: all when asked
    calib_surface = 'all' if 'all' in land_oceans else land_oceans[0]
    functions = [f for f in (_split_tokens(functions) or ['omp'])
                 if f in FUNCTIONS] or ['omp']
    stn_tokens = parse_station_tokens(id_stn)
    varnos = _split_tokens(varnos)
    # with the option off the task never gets a control file, so the
    # extraction takes its unmatched branch and nothing else changes
    matched = control is not None and match
    all_runs = ([control] if control else []) + list(runs)

    print(f"{p} runs: {', '.join(n for n, _ in all_runs)}", flush=True)
    if matched:
        print(f"{p} control: {control[0]}  |  matched observation by "
              f"observation with: {', '.join(n for n, _ in runs)}",
              flush=True)
    print(f"{p} regions: {regions}  |  flags: {flags}  |  fonction: "
          f"{functions}  |  id_stn: {stn_tokens}", flush=True)
    print(f"{p} surface: {land_oceans}  |  special column: "
          f"{'on' if special_on else 'off'}", flush=True)
    for fam in families:
        if is_radar(fam):
            print(f"{p} {fam}: one line per antenna elevation, against the "
                  f"slant range and the beam height (1-km bins)"
                  + ("; theoretical error model drawn" if obs_error_model
                     else ""), flush=True)
        else:
            _, vc, _, _, _, vt = pikobs.family(fam)
            print(f"{p} {fam}: vcoord = {vc.strip()}  ({vt})", flush=True)

    # a missing or empty 6-h file is a warning, as in cardio: the run goes
    # on with the files there are, and the log and the viewer say it
    missing_input = _missing_input(all_runs, families, datestart, dateend)
    if missing_input is None:
        print("[profile] ERROR: not a single input file with data in the "
              "period, nothing was run (PATHWORK left untouched).", flush=True)
        return 1
    t_start = time.time()
    cycle_list = _cycles(datestart, dateend)
    n_input, input_bytes = input_size(all_runs, families, cycle_list)
    timing: Dict[str, Any] = {
        'datestart': datestart, 'dateend': dateend,
        'cycles': len(cycle_list), 'families': list(families),
        'runs': len(all_runs), 'regions': regions, 'flags': flags,
        'fonction': functions, 'id_stn': stn_tokens, 'matched': matched,
        'min_obs': min_obs, 'obs_error_model': obs_error_model, 'svg': svg,
        'curves': list(error_curves),
        'land_ocean': land_oceans, 'special_column': special_on,
        'n_cpus': n_cpu, 'input_files': n_input, 'input_bytes': input_bytes,
        'seconds': {},
    }
    for family in families:
        pikobs.delete_create_folder(pathwork, family)

    # every run on its own (one figure each); with a control, also every
    # experience matched against it (the change figure)
    tasks = []
    for name, path in all_runs:
        for cycle in cycle_list:
            for family in families:
                tasks.append({'family': family, 'regions': regions,
                              'flags': flags, 'varnos': varnos,
                              'land_oceans': land_oceans,
                              'special_on': special_on,
                              'pathwork': pathwork,
                              'filein': cycle_path(path, cycle, family),
                              'db_new': db_path(pathwork, family, name,
                                                datestart, dateend)})
    if matched:
        for name, path in runs:
            for cycle in cycle_list:
                for family in families:
                    tasks.append({
                        'family': family, 'regions': regions, 'flags': flags,
                        'varnos': varnos,
                        'land_oceans': land_oceans, 'special_on': special_on,
                        'pathwork': pathwork,
                        'ctl_file': cycle_path(control[1], cycle, family),
                        'match_fields': match_spec.fields,
                        'names': (control[0], 'experience'),
                        'exp_file': cycle_path(path, cycle, family),
                        'db_new': db_path(pathwork, family,
                                          f"{control[0]}_vs_{name}",
                                          datestart, dateend)})

    client, dask_dir = None, None
    if n_cpu > 1:
        os.environ["DASK_LOGGING__DISTRIBUTED"] = "error"
        dask_dir = tempfile.mkdtemp(prefix="pikobs_profile_dask_",
                                    dir=os.environ.get("TMPDIR") or None)
        os.environ["DASK_TEMPORARY_DIRECTORY"] = dask_dir
        os.environ["SQLITE_TMPDIR"] = dask_dir
        dask.config.set({"temporary-directory": dask_dir,
                         "logging.distributed": "error"})
        client = Client(processes=True, threads_per_worker=1, n_workers=n_cpu,
                        silence_logs=50, dashboard_address=None)
    figures: List[Dict[str, Any]] = []
    results: List[Any] = []
    try:
        t0 = time.time()
        print(f"{p} extraction: {len(tasks)} tasks, {n_cpu} worker(s)",
              flush=True)
        res = run_tasks(_extract_task, [(t,) for t in tasks], client,
                        label='extraction')
        # one line per family when the pairing key was not unique
        from pikobs.match import add_counts, repeat_warning
        repeats = {}
        for t, r in zip(tasks, res):
            if isinstance(r, dict):
                add_counts(repeats.setdefault(t['family'], {}),
                           r.get('repeats'))
        for fam in sorted(repeats):
            msg = repeat_warning('profile', fam, match_spec, repeats[fam])
            if msg:
                print(msg, file=sys.stderr, flush=True)
        timing['seconds']['extraction'] = time.time() - t0
        print(f"{p} extraction time: {timing['seconds']['extraction']:.1f}s "
              f"({sum(r is not None for r in res)}/{len(tasks)} files)",
              flush=True)
        dbs = sorted({t['db_new'] for t in tasks})
        run_tasks(_index_task, [(d,) for d in dbs], client, label='indexing')

        # the radar calibration table, one per run
        for family in families:
            if not is_radar(family):
                continue
            out_csv = os.path.join(pathwork, family,
                                   "radar_obs_error_calibration.csv")
            n_rows = sum(write_radar_calibration(
                db_path(pathwork, family, name, datestart, dateend), name,
                out_csv, obs_error_model, min_obs, calib_surface)
                for name, _ in all_runs)
            print(f"{p} {family}: calibration table, {n_rows} rows: "
                  f"{out_csv}", flush=True)

        for family in families:
            dbs_f = [db_path(pathwork, family, n, datestart, dateend)
                     for n, _ in all_runs]
            selectors = expand_station_selectors(dbs_f, stn_tokens, family,
                                                 table='prof')
            figures += plan_figures(
                family, all_runs, control, runs, selectors, regions, flags,
                functions, pathwork, datestart, dateend, db_path,
                is_radar(family), min_obs, svg, obs_error_model)
        if not figures:
            print(f"{p} WARNING: nothing to plot, check the selectors.",
                  file=sys.stderr, flush=True)
            return 1
        # ERROR_CURVES reaches every figure (it was only in the timing)
        for f in figures:
            f['curves'] = list(error_curves)
        # FIT_RADAR: the error model fitted on each run, from the table
        # just written; its figures then draw it beside the current model
        if fit_radar:
            from pikobs.profile import fit_radar_obs_error as _fit
            crit = 'assimilee' if 'assimilee' in flags else flags[0]
            fitted, fit_used = {}, {}
            words = {'desroziers': 'Desroziers', 'sigma': 'sigma of O-P',
                     'sigma3': 'sigma of O-P within 3 sigma'}
            for family in families:
                if not is_radar(family):
                    continue
                table = os.path.join(pathwork, family,
                                     "radar_obs_error_calibration.csv")
                for name, _ in all_runs:
                    out_fit = os.path.join(pathwork, family, f"fit_{name}")
                    try:
                        tbl, tgt, used = table, 'desroziers', fit_radar_target
                        if fit_radar_target in ('sigma', 'sigma3'):
                            tgt = 'conservative'
                        if fit_radar_target == 'sigma3':
                            run_db = db_path(pathwork, family, name,
                                             datestart, dateend)
                            files = [t['filein'] for t in tasks
                                     if t.get('filein') and t['family'] == family
                                     and t['db_new'] == run_db]
                            tbl = radar_sigma3(name, family, run_db, files,
                                               regions, flags, varnos,
                                               pathwork, client)
                        args_fit = [tbl, '--run', name, '--region', regions[0],
                                    '--criteria', crit, '--out', out_fit]
                        rc = _fit.main(args_fit + ['--target', tgt])
                        if rc != 0 and tgt == 'desroziers':
                            # no O-A: a stage before the analysis (bgckalt)
                            print(f"{p} {family} {name}: no O-A for Desroziers, "
                                  f"FIT_RADAR falls back on the sigma of O-P",
                                  flush=True)
                            rc = _fit.main(args_fit + ['--target', 'conservative'])
                            used = 'sigma'
                        fit_used[(family, name)] = words[used]
                    except Exception as exc:               # never fatal
                        print(f"{p} {family} {name}: FIT_RADAR failed: {exc}",
                              file=sys.stderr, flush=True)
                        continue
                    path = os.path.join(out_fit, 'radar_obs_error_fitted.py')
                    if rc == 0 and os.path.isfile(path):
                        fitted[(family, name)] = path
                        print(f"{p} {family} {name}: fitted obs error in "
                              f"{out_fit}", flush=True)
            for f in figures:
                if f.get('mode') == 'run' and f.get('radar'):
                    f['fit_table'] = fitted.get((f['family'], f.get('name')))
                    f['fit_target'] = fit_used.get((f['family'], f.get('name')))
        shared_limits(figures)

        t0 = time.time()
        print(f"{p} plots: {len(figures)} tasks", flush=True)
        results = run_tasks(plot_task, [(f,) for f in figures], client,
                            label='plots')
        timing['seconds']['plots'] = time.time() - t0
        n_drawn = sum(r is not None for r in results)
        print(f"{p} plot time: {timing['seconds']['plots']:.1f}s "
              f"({n_drawn}/{len(figures)})", flush=True)
        # A figure that comes back empty is not a failure: the selection
        # had nothing in it (a station that did not report, a varno the
        # family does not carry, an empty region). Same line as timeserie.
        n_empty = len(figures) - n_drawn
        if n_empty:
            print(f"{p} {n_empty} figure(s) not drawn: the selection held "
                  f"no observation in the period (a station that did not "
                  f"report, a varno absent from the family, an empty "
                  f"region). Any real failure is in the traceback above.",
                  flush=True)
    finally:
        if client is not None:
            try:
                client.close(timeout=30)
            except Exception:
                pass
            try:
                client.shutdown()
            except Exception:
                pass
        if dask_dir:
            shutil.rmtree(dask_dir, ignore_errors=True)

    items = [dict(f['viewer'], filename=os.path.basename(r))
             for f, r in zip(figures, results) if r]
    if not items:
        print(f"{p} ERROR: no figure was produced.", file=sys.stderr,
              flush=True)
        return 1
    keys = ["experience", "family", "fonction", "region", "land_ocean", "flag_criteria",
            "id_stn", "special", "varno", "elevation", "yaxis"]
    generate_web(
        items, keys, os.path.join(pathwork, "pikobs_profile_viewer.html"),
        title=("Pikobs Profile Viewer"
               + (f"   \u26a0 input incomplete: "
                  f"{sum(len(v) for v in missing_input.values())} file(s) "
                  f"missing or empty, see About" if missing_input else "")),
        subtitle=(
            _missing_note(missing_input, len(_cycles(datestart, dateend))) +
            "Bias, sigma, assigned error and number of observations, level "
            "by level; for radar one line per antenna elevation. Every run "
            "on the same axes, so flipping between them moves nothing." +
            (f" With <b>{control[0]}</b> as control, the change of each "
             "experience is its own entry, the runs matched observation by "
             "observation: <b>red</b> where the experience is better, "
             "<b>blue</b> where the control is." if matched else "")) + _curves_note(error_curves, fit_radar, fit_radar_target) + runs_block(all_runs, control, (datestart, dateend)),
        image_subdir_key="family",
        key_labels={"flag_criteria": "Criteria", "yaxis": "Axis",
                    "land_ocean": "Surface",
                    "special": special_key_label(families)},
        issues_url="https://gitlab.science.gc.ca/dlo001/Pikobs")
    timing['seconds']['total'] = time.time() - t_start
    _report_timing(timing, pathwork)
    # A whole family with nothing drawn is another matter: a few empty
    # selections are normal, an empty family almost never is (wrong path,
    # wrong period, a flag criterion that keeps nothing).
    per_fam = {}
    for f, r in zip(figures, results):
        fam = f['viewer'].get('family', '?')
        tot, ok = per_fam.get(fam, (0, 0))
        per_fam[fam] = (tot + 1, ok + (r is not None))
    empty_fams = sorted(fam for fam, (tot, ok) in per_fam.items() if ok == 0)
    for fam in empty_fams:
        print(f"{p} WARNING: family {fam}: none of its {per_fam[fam][0]} "
              f"figure(s) was drawn -- check the path, the period and the "
              f"flag criteria for this family.", file=sys.stderr, flush=True)
    if empty_fams:
        print(f"{p} done, with empty famil"
              f"{'y' if len(empty_fams) == 1 else 'ies'} "
              f"{', '.join(empty_fams)} -- output in: {pathwork}", flush=True)
    else:
        print(f"{p} done -- output in: {pathwork}", flush=True)
    return 0


def arg_call() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        prog="pikobs-profile",
        description="Vertical profiles, conventional and radar.")
    ap.add_argument('--path_control_files', nargs='*', default=None)
    ap.add_argument('--control_name', nargs='*', default=None)
    ap.add_argument('--path_experience_files', nargs='+', default=[])
    ap.add_argument('--experience_name', nargs='+', default=[])
    ap.add_argument('--pathwork', default=None)
    ap.add_argument('--datestart', default=None)
    ap.add_argument('--dateend', default=None)
    ap.add_argument('--region', nargs='+', default=['Monde'])
    ap.add_argument('--family', nargs='+', default=[])
    ap.add_argument('--flags_criteria', nargs='+', default=['all'])
    ap.add_argument('--fonction', nargs='+', default=['omp'],
                    choices=list(FUNCTIONS))
    ap.add_argument('--varnos', nargs='*', default=[])
    ap.add_argument('--id_stn', nargs='+', default=['join'])
    ap.add_argument('--min_obs', default=MIN_OBS_PER_LEVEL, type=int)
    ap.add_argument('--error_curves', nargs='*', default=[],
                    choices=['obs_error', 'desroziers', 'model', 'model_fit'],
                    help="error curves beside the OBS_ERROR of the files, always "
                         "drawn: desroziers, and on radar model and model_fit.")
    ap.add_argument('--fit_radar_target', default='desroziers',
                    choices=['desroziers', 'sigma', 'sigma3'],
                    help="what FIT_RADAR fits: Desroziers (needs O-A), the "
                         "sigma of O-P, or it within 3 sigma of its cell.")
    ap.add_argument('--fit_radar', default='off', choices=['on', 'off'],
                    help="on: radar, fit the observation-error model on "
                         "each run (fit_radar_obs_error.py) and draw it "
                         "beside the current one.")
    ap.add_argument('--obs_error_model', default='off', choices=['on', 'off'],
                    help="on: radar, draw the theoretical error model of "
                         "radar_obs_error.py and add it to the calibration "
                         "table.")
    ap.add_argument('--land_ocean', nargs='+', default=['all'],
                    choices=['all', 'land', 'ocean'],
                    help="all: no filter; land, ocean: one series of "
                         "figures each (radar: the surface under the "
                         "antenna).")
    ap.add_argument('--special_column', default='off', choices=['on', 'off'],
                    help="on: one series of figures per value of the "
                         "family's special column (radar is always split "
                         "by elevation); off: all together (default).")
    ap.add_argument('--match', nargs='+', default=['on'],
                      help="on: with a control, the same observations in both "
                         "runs, paired tests. off: each run with all its "
                         "observations and its own flags, Welch and F tests.")
    ap.add_argument('--svg', default='off', choices=['on', 'off'])
    ap.add_argument('--n_cpus', '--n_cpu', default=1, type=int,
                    dest='n_cpus')
    ap.add_argument('--no_submit', action='store_true')
    # options of the old module, accepted so its wrappers keep working
    ap.add_argument('--channel', '--vcoord', dest='channel', default=None,
                    help=argparse.SUPPRESS)

    args = ap.parse_args()
    for arg in vars(args):
        print(f'--{arg} {getattr(args, arg)}', flush=True)
    paths = _split_tokens(args.path_experience_files)
    names = _split_tokens(args.experience_name)
    if not paths or not names or len(paths) != len(names):
        raise ValueError("--path_experience_files and --experience_name must "
                         "have the same number of entries")
    for attr, flag in [('pathwork', '--pathwork'),
                       ('datestart', '--datestart'),
                       ('dateend', '--dateend'), ('family', '--family')]:
        if getattr(args, attr) in (None, [], 'undefined', ''):
            raise ValueError(f"{flag} is required")
    runs = [(n, p_.rstrip('/') or '/') for n, p_ in zip(names, paths)]
    control = None
    cpaths = [c for c in _split_tokens(args.path_control_files)
              if c != 'undefined']
    if cpaths:
        cname = (_split_tokens(args.control_name) or ['control'])[0]
        if cname in names:
            raise ValueError(f"the control and an experience share the name "
                             f"'{cname}'")
        control = (cname, cpaths[0].rstrip('/') or '/')

    maybe_submit_to_pbs(args)
    sys.exit(make_profile(
        runs, args.pathwork, args.datestart, args.dateend, args.region,
        _split_tokens(args.family), args.flags_criteria, args.fonction,
        _split_tokens(args.varnos), args.id_stn, args.n_cpus, control,
        svg_enabled(args.svg), args.min_obs,
        args.obs_error_model == 'on' or 'model' in args.error_curves,
                 match=args.match, land_ocean=args.land_ocean,
                 fit_radar=args.fit_radar == 'on',
                 fit_radar_target=args.fit_radar_target,
                 error_curves=args.error_curves,
                 special_column=args.special_column))


if __name__ == '__main__':
    arg_call()
