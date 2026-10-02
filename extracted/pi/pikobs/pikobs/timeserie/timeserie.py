#!/usr/bin/python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_timeserie.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""======================================================================
pikobs.timeserie -- Availability and quality control, cycle by cycle
======================================================================

The first thing I want to know about a run is not how good the
observations are, but how many arrived and what the system did with them.
A channel goes on the blacklist, a satellite drops for a day, thinning is
tightened: none of that shows in a mean or a sigma, and all of it changes
what the analysis had to work with.

``timeserie`` draws that, every 6-h cycle: the observations stacked by
their flag combination, who brings them, and -- when the files carry
departures -- the mean and the sigma of O-P and O-A with the error the
system assigned. A file without O-P still gives the counts: the figure
draws what the data has, and says what it does not.

With a control, one more figure puts the runs side by side and adds the
change of the mean and of sigma, cycle by cycle.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_timeserie_exp.sh
   chmod +x run_timeserie_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_timeserie_cont_exp.sh
   chmod +x run_timeserie_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_timeserie_cont_exp.sh
   ./run_timeserie_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period, of every run, in parallel.

.. code-block:: text

   [timeserie] runs: control, experience  |  control: control
   [timeserie] regions: ['Monde']  |  flags: ['all']  |  id_stn: ['join']  |  channel: ['join']  |  land_ocean: ['all']
   [timeserie] match: the figures keep every observation of every run; the change of each cycle is tested on the ones the runs share with control
   [timeserie] extraction time: 41.2s (192/192 files)
   [timeserie] plots: 18 tasks
   [timeserie] alerts: 2 cycle(s): .../timeserie_alerts.csv

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* `one run on its own <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_timeserie_exp/pikobs_timeserie_viewer.html>`__
* `G0 against G2 <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_timeserie/pikobs_timeserie_viewer.html>`__, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**One pass per file, every selection at once.** Regions, criteria,
surfaces, stations and levels come out of the same scan, so adding four
regions costs almost nothing.

**The flags are grouped in SQL.** The counts are kept per flag
combination -- a few dozen values -- and the diagnosis of ``flag_reason``
is attached later, when the figure is drawn. Calling it per observation
would mean tens of millions of Python calls on a family like IASI.

**Only numbers count.** A departure enters the sums when it is a number;
an empty field is not a zero, and each quantity keeps its own count, so a
file with O-P and no O-A still gives its O-P statistics.

**Matching** happens only with ``MATCH="on"``, and only to test: an
observation is the same in both runs when its station, position, time,
varno and level agree.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_timeserie_exp.sh run_timeserie_cont_exp.sh

----

3. A run
========

+-------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| Panel             | What it shows                                                                                                                         |
+===================+=======================================================================================================================================+
| Flag combinations | the observations of every cycle, stacked by their flag combination: the ones carrying bit 12 in blues, the others in their own colour |
+-------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| By station        | with a pooled selection, the same counts stacked by station -- or by instrument type on ai, sf, ua, gp and csr                        |
+-------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| Mean              | the mean of O-P and O-A, and the bias correction, per cycle                                                                           |
+-------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| Sigma             | their sigma, and the mean assigned observation error                                                                                  |
+-------------------+---------------------------------------------------------------------------------------------------------------------------------------+

.. image:: _static/timeserie_run.png
   :alt: One run: counts by flag combination, by station, and the departures
   :align: center
   :width: 100%

The colours of the top panel are the flag combinations themselves, not a
summary of them: every combination that carries **bit 12** is a shade of
blue, from light to dark, and everything else has its own colour. So the
blue is what entered the analysis and the rest is what the quality
control stopped, with ``12+13`` -- assimilated, but the rogue check
raised a level-1 warning -- separate from a plain ``12``. The key below
the legend gives the meaning of every bit that appears, and nothing more:
the combinations themselves are already in the legend.

With a pooled selection (``join``, or a group such as ``C%``) the second
panel shows who brings the observations, and the header lists them:
``station join -> GOES18, METOP-1, NOAA20``.

----

4. Comparing with a control
===========================

+-------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Panel                               | What it shows                                                                                                                                                                                    |
+=====================================+==================================================================================================================================================================================================+
| Observations                        | every run, its assimilated observations thick and its total faint; the control solid, the experiences dashed                                                                                     |
+-------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Assimilated, exp - control          | how many more, or fewer, each cycle brings                                                                                                                                                       |
+-------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Mean and sigma                      | one curve per run, every run with all of its own observations; the value of each run over the period above the panel                                                                             |
+-------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Change of the mean, change of sigma | experience minus control, cycle by cycle; the bar is filled when the test says the change is real, pale when it is not. Above each, the change over the period and how many cycles pass the test |
+-------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. image:: _static/timeserie_comparison.png
   :alt: An experience against a control
   :align: center
   :width: 100%

The curves always hold **every observation of every run**, so what you
see is the system as it really is, quality and quantity together. The
control is solid and the experiences dashed: where two curves agree, one
would otherwise hide the other.

+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| MATCH   | What changes                                                                                                                                                                                                                                         |
+=========+======================================================================================================================================================================================================================================================+
| ``off`` | the bars of the change panels are drawn pale: the change is shown, not judged                                                                                                                                                                        |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``on``  | the change of every cycle is tested on the observations the two runs share -- paired t-test on the mean, Pitman-Morgan on sigma (see :doc:`stats`) -- and the bars are filled accordingly. The summary also says how much of the data the runs share |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

That separation matters. An experience that assimilates 20 % more
observations often shows a slightly larger sigma, and the question is
whether it got worse or whether the observations it added are harder.
``MATCH="on"`` answers it: the bars are filled only where the change
holds on the data both runs share, and the summary says what that share
is.

----

5. Reading it
=============

+-----------------------------------------+------------------------------------------------------------------------------------------------+
| What you see                            | What it usually means                                                                          |
+=========================================+================================================================================================+
| a step in the stack, one colour growing | a decision of the quality control changed: a channel blacklisted, thinning tightened           |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| a cycle far below the others            | a satellite missing, a late file, a failed retrieval -- ALERT_PCT marks them                   |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| more observations and a larger sigma    | the experience assimilates more, and the ones it adds are harder; MATCH=on tells the two apart |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| the assigned error far from sigma       | the errors the system assigns do not match the data; see profile for the same by level         |
+-----------------------------------------+------------------------------------------------------------------------------------------------+

----

6. Stations and instrument types
================================

+--------------+--------------------------------------------------------------------+
| Token        | Series produced                                                    |
+==============+====================================================================+
| ``join``     | one, every station together, with the panel by station             |
+--------------+--------------------------------------------------------------------+
| ``all``      | one per station; on ai, sf, ua, gp and csr one per instrument type |
+--------------+--------------------------------------------------------------------+
| ``C%``       | the stations whose id starts with C, together                      |
+--------------+--------------------------------------------------------------------+
| ``=METOP-1`` | that station only                                                  |
+--------------+--------------------------------------------------------------------+

On ``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` the tokens name instrument
types rather than stations -- ``pilot``, ``=TEMP``, ``35`` -- the same
way in every module; see :doc:`families`.

----

7. Levels and layers
====================

``CHANNEL`` decides what a series holds in the vertical: ``join`` pools the
whole column, ``all`` gives one series per level or channel, and a list
picks some of them. For radiances one series per channel is what you want.
For radiosondes or GPS-RO it is not: ``all`` gives dozens of levels, many of
them with a handful of observations, and ``join`` puts the boundary layer
and the stratosphere in the same number.

Layers sit in between, as in scatter. ``PRESSURE_LAYERS`` takes bounds in
hPa for the families on pressure levels, ``HEIGHT_LAYERS`` bounds in km for
those on heights, and every two consecutive bounds make a series, beside
what ``CHANNEL`` asks for:

.. code-block:: bash

   CHANNEL=(join)
   PRESSURE_LAYERS=(1100 850 500 250 100 10)   # ua, ai, ...: five layers
   HEIGHT_LAYERS=(0 5 10 20 30 40)             # ro, radar: five layers

They are the layers of scatter, the same edges and the same rule: a level
on an edge belongs to the layer where it is the larger number, so 500 hPa
falls in 500-250 and 5 km in 0-5, never in two layers at once. Channel
families ignore both settings. The layers are read from the levels already
extracted, so adding or changing them costs the figures and nothing else.
Each is labelled with its rank from the ground, ``2 | 850-500 hPa``, so that
the viewer lists them by height and not alphabetically.

----

8. Alerts
=========

``ALERT_PCT`` marks the cycles that bring far fewer observations than
they usually do, with a triangle on the figure and a line in
``timeserie_alerts.csv``: the run, the family, the region, the criteria,
the station, the cycle, the count, the median it was compared with and
the drop in percent.

Each cycle is compared with the median of the **same hour** on the days
before it, up to four. A family like ``ua`` brings thousands of
observations at 00 and 12 UTC and a handful at 06 and 18; comparing a
cycle with the ones just before it would flag every 06 and every 18, day
after day, and say nothing.

----

9. Output layout
================

::

   $PATHWORK/
   ├── pikobs_timeserie_viewer.html
   ├── timeserie_timing.json
   ├── timeserie_alerts.csv                (with ALERT_PCT)
   └── <family>/
       ├── timeserie_<run>_<start>_<end>_<family>.db
       └── timeserie_<run>_<family>_varno<N>_lev<level>_<station>_<region>[_<surface>][_<special>]_<flag>.png

``<level>`` is ``join``, a level or a channel, or a layer, written
``2___850-500_hPa`` for ``2 | 850-500 hPa``.

----

10. Support
===========

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
from typing import Any, Dict, List, Optional

import dask
from dask.distributed import Client

import pikobs
from pikobs.configobs import regionsobs as regionlib
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

# Bits that record what was done to a value, not a quality decision: left
# out of the flag combination, or bit 6 alone would split every radiance
# combination in two.
QC_INFO_BITS = (5, 6, 10)
QC_MASK = sum(1 << b for b in range(24) if b not in QC_INFO_BITS)

_QC_COLS = ("region, flag, land_ocean, special, id_stn, codtyp, varno, lev, "
            "cycle, "
            "sig, n")
_DDL_QC = """
    CREATE TABLE IF NOT EXISTS ts_qc (
        region TEXT, flag TEXT, land_ocean TEXT, special TEXT, id_stn TEXT,
        codtyp INTEGER, varno INTEGER, lev REAL, cycle TEXT, sig INTEGER,
        n INTEGER
    );
"""
# How much of the two runs is the same observation, cycle by cycle: the
# matched tests of histogram and profile speak of the shared part only,
# and this says how big that part is.
_PAIR_COLS = ("region, flag, land_ocean, special, id_stn, codtyp, varno, "
              "lev, "
              "cycle, "
              "n_both, n_ctl_only, n_exp_only, "
              "n_p, c_omp, c2_omp, e_omp, e2_omp, ce_omp, "
              "n_a, c_oma, c2_oma, e_oma, e2_oma, ce_oma")
_DDL_PAIR = """
    CREATE TABLE IF NOT EXISTS ts_pair (
        region TEXT, flag TEXT, land_ocean TEXT, special TEXT, id_stn TEXT,
        codtyp INTEGER, varno INTEGER, lev REAL, cycle TEXT,
        n_both INTEGER, n_ctl_only INTEGER,
        n_exp_only INTEGER,
        n_p INTEGER, c_omp FLOAT, c2_omp FLOAT, e_omp FLOAT, e2_omp FLOAT,
        ce_omp FLOAT,
        n_a INTEGER, c_oma FLOAT, c2_oma FLOAT, e_oma FLOAT, e2_oma FLOAT,
        ce_oma FLOAT
    );
"""

_VAL_COLS = ("region, flag, land_ocean, special, id_stn, codtyp, varno, lev, "
             "cycle, "
             "n_omp, s_omp, s2_omp, n_oma, s_oma, s2_oma, "
             "n_err, s_err, n_bc, s_bc, s2_bc")
_DDL_VAL = """
    CREATE TABLE IF NOT EXISTS ts_val (
        region TEXT, flag TEXT, land_ocean TEXT, special TEXT, id_stn TEXT,
        codtyp INTEGER, varno INTEGER, lev REAL, cycle TEXT,
        n_omp INTEGER, s_omp FLOAT, s2_omp FLOAT,
        n_oma INTEGER, s_oma FLOAT, s2_oma FLOAT,
        n_err INTEGER, s_err FLOAT,
        n_bc INTEGER, s_bc FLOAT, s2_bc FLOAT
    );
"""


def _num(col: str) -> str:
    """The column when it holds a number, NULL otherwise."""
    return f"(CASE WHEN typeof({col}) IN ('real', 'integer') THEN {col} END)"


def _safe(text) -> str:
    import re
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


def db_path(work_path, family, run, date_start, date_end) -> str:
    return os.path.join(work_path, family,
                        f"timeserie_{_safe(run)}_{date_start}_{date_end}_"
                        f"{family}.db")


def _surface_sql(land_ocean: str, lat: str = 'lat', lon: str = 'lon') -> str:
    """Land, ocean, or everything -- the mask is the one zone uses."""
    if land_ocean == 'land':
        return f" AND is_land_sql({lat}, {lon}) = 1"
    if land_ocean == 'ocean':
        return f" AND is_land_sql({lat}, {lon}) = 0"
    return ""


def register_land(conn, land_oceans, pathwork) -> None:
    if any(lo != 'all' for lo in land_oceans):
        from pikobs.configobs.landmask import is_land_function
        conn.create_function("is_land_sql", 2, is_land_function(pathwork))


def _region_sql(region: str, pathwork: str, lat: str, lon: str) -> str:
    """The condition of a region, box or polygon: configobs.regions
    knows which it is."""
    from pikobs.configobs import regionsobs as regionlib
    if regionlib.is_polygon(region):
        return regionlib.criteria(region, pathwork, lat, lon)
    crit = regionlib.criteria(region)
    return crit.replace('lat', lat).replace('lon', lon) if lat != 'lat' \
        else crit


def _combos(regions, flags, land_oceans=('all',), pathwork='.',
            lat='lat', lon='lon'):
    """(region, criteria, surface) with the SQL condition of each."""
    out = []
    for region in regions:
        latlon = _region_sql(region, pathwork, lat, lon)
        for flag in flags:
            for surface in land_oceans:
                out.append((region, flag, surface,
                            f"1=1 {latlon} {pikobs.flag_criteria(flag)}"
                            f"{_surface_sql(surface, lat, lon)}"))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Extraction
# ─────────────────────────────────────────────────────────────────────────────

def create_ts(task: Dict[str, Any]) -> Optional[int]:
    """Counts per flag combination, and the departures when there are
    any, per station, level and varno, for one cycle of one run."""
    family, path, cycle = task['family'], task['filein'], task['cycle']
    import time as _time
    _t0 = _time.time()
    if not os.path.isfile(path):
        print(f"[timeserie] missing file, skipped: {path}", file=sys.stderr,
              flush=True)
        return None
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if task['varnos']:
        element = ",".join(str(v) for v in task['varnos'])
    lev = (VCOORD or '').strip() or 'vcoord'
    with work_db(attach={'db': path}) as (conn, mem_uri):
        conn.execute(_DDL_QC)
        conn.execute(_DDL_VAL)
        dcols = {c.lower() for c in table_columns(conn, 'DATA', 'db')}
        hcols = {c.lower() for c in table_columns(conn, 'HEADER', 'db')}
        codtyp = "codtyp" if 'codtyp' in hcols else "0"
        # the special column, or the constant 'all': grouping by a
        # constant changes no group
        from pikobs.configobs.special_family import special_select
        sp_sel, _ = special_select(family, hcols, bool(task.get('special_on')))
        has = {c: c in dcols for c in ('omp', 'oma', 'obs_error',
                                       'bias_corr')}
        omp = _num('omp') if has['omp'] else "NULL"
        oma = _num('oma') if has['oma'] else "NULL"
        err = _num('obs_error') if has['obs_error'] else "NULL"
        bc = _num('bias_corr') if has['bias_corr'] else "NULL"
        register_land(conn, task['land_oceans'], task['pathwork'])
        regionlib.register(conn, task['regions'], task['pathwork'])
        # every combination from one grouping of the file: the rows are
        # grouped once by station, varno, level, flag value and the regions
        # (and surfaces) they fall in, as bits, and each region x criterion
        # x surface is read from those groups -- the criteria only look at
        # flag. The loop below grouped the whole file once per combination
        # (a file of iasi, 3 x 3: 79 s against 25 s); it stays for a
        # criterion that would look at another column.
        import re as _re
        _plain = {"and", "or", "not", "flag", "in", "between", "is", "null"}
        only_flag = all(
            set(_re.findall(r"[a-z_]\w*", pikobs.flag_criteria(f).lower()))
            <= _plain for f in task['flags'])
        places = [(r, s) for r in task['regions'] for s in task['land_oceans']]
        # grouping first pays with three combinations or more; with one or
        # two, the loop below reads less (iasi, 1 region, 1 criterion:
        # 29 s with the loop, 63 s grouping first)
        n_combos = len(places) * len(task['flags'])
        if only_flag and 3 <= n_combos and len(places) <= 60:
            rb = " + ".join(
                f"(CASE WHEN 1=1 {_region_sql(r, task['pathwork'], 'lat', 'lon')}"
                f"{_surface_sql(s)} THEN {1 << k} ELSE 0 END)"
                for k, (r, s) in enumerate(places))
            # only the rows at least one criterion keeps: the others go into
            # no combination, and grouping them cost as much as the rest
            anyflag = " OR ".join(f"(1=1 {pikobs.flag_criteria(f)})"
                                  for f in task['flags'])
            conn.execute(f"""
                CREATE TEMP TABLE pre AS
                SELECT id_stn, {codtyp} AS cod, varno, {lev} AS l, flag,
                       {sp_sel} AS sp,
                       ({rb}) AS rb, COUNT(*) AS n,
                       COUNT({omp}) AS n_omp, SUM({omp}) AS s_omp,
                       SUM({omp}*{omp}) AS s2_omp,
                       COUNT({oma}) AS n_oma, SUM({oma}) AS s_oma,
                       SUM({oma}*{oma}) AS s2_oma,
                       COUNT({err}) AS n_err, SUM({err}) AS s_err,
                       COUNT({bc}) AS n_bc, SUM({bc}) AS s_bc,
                       SUM({bc}*{bc}) AS s2_bc
                FROM db.header NATURAL JOIN db.data
                WHERE varno IN ({element}) {VCOCRIT} AND ({anyflag})
                GROUP BY id_stn, cod, varno, l, flag, rb, sp;""")
            for k, (region, surf) in enumerate(places):
                for flag in task['flags']:
                    w = f"(rb & {1 << k}) != 0 {pikobs.flag_criteria(flag)}"
                    conn.execute(f"""
                        INSERT INTO ts_qc ({_QC_COLS})
                        SELECT '{region}', '{flag}', '{surf}', sp, id_stn,
                               cod, varno, l, '{cycle}',
                               (flag & {QC_MASK}) AS sg, SUM(n)
                        FROM pre WHERE {w}
                        GROUP BY id_stn, cod, varno, l, sg, sp;""")
                    if any(has.values()):
                        conn.execute(f"""
                            INSERT INTO ts_val ({_VAL_COLS})
                            SELECT '{region}', '{flag}', '{surf}', sp,
                                   id_stn, cod, varno, l, '{cycle}',
                                   SUM(n_omp), SUM(s_omp), SUM(s2_omp),
                                   SUM(n_oma), SUM(s_oma), SUM(s2_oma),
                                   SUM(n_err), SUM(s_err),
                                   SUM(n_bc), SUM(s_bc), SUM(s2_bc)
                            FROM pre WHERE {w}
                            GROUP BY id_stn, cod, varno, l, sp;""")
        else:
            for region, flag, surf, cond in _combos(task['regions'],
                                                    task['flags'],
                                                    task['land_oceans'],
                                                    task['pathwork']):
                conn.execute(f"""
                    INSERT INTO ts_qc ({_QC_COLS})
                    SELECT '{region}', '{flag}', '{surf}', {sp_sel} AS sp,
                           id_stn, {codtyp}, varno,
                           {lev} AS l, '{cycle}', (flag & {QC_MASK}) AS sg,
                           COUNT(*)
                    FROM db.header NATURAL JOIN db.data
                    WHERE varno IN ({element}) {VCOCRIT} AND {cond}
                    GROUP BY id_stn, {codtyp}, varno, l, sg, sp;""")
                if any(has.values()):
                    conn.execute(f"""
                        INSERT INTO ts_val ({_VAL_COLS})
                        SELECT '{region}', '{flag}', '{surf}', {sp_sel} AS sp,
                               id_stn, {codtyp}, varno,
                               {lev} AS l, '{cycle}',
                               COUNT({omp}), SUM({omp}), SUM({omp}*{omp}),
                               COUNT({oma}), SUM({oma}), SUM({oma}*{oma}),
                               COUNT({err}), SUM({err}),
                               COUNT({bc}), SUM({bc}), SUM({bc}*{bc})
                        FROM db.header NATURAL JOIN db.data
                        WHERE varno IN ({element}) {VCOCRIT} AND {cond}
                        GROUP BY id_stn, {codtyp}, varno, l, sp;""")
        _combine_rows(task['db_new'], mem_uri, 'ts_qc', _QC_COLS,
                      ddl=_DDL_QC, module='timeserie')
        _combine_rows(task['db_new'], mem_uri, 'ts_val', _VAL_COLS,
                      ddl=_DDL_VAL, module='timeserie')
        if os.environ.get('PIKOBS_TIMING'):
            _n = conn.execute('SELECT COUNT(*) FROM ts_qc').fetchone()[0]
            print(f"[timeserie timing] {family} {os.path.basename(path)}: "
                  f"{_time.time() - _t0:.1f}s, {_n} ts_qc rows", file=sys.stderr, flush=True)
    return 1


def create_matched(task: Dict[str, Any]) -> Optional[int]:
    """The two runs on the same observations, cycle by cycle.

    How many observations with a departure they share and how many each
    one has alone (a row with neither O-P nor O-A can never be half of a
    pair, and on the radiances it is most of the file), and
    -- over the shared ones -- the sums both runs need for the paired
    tests, so a change of the mean or of the sigma can be told from
    noise without the number of observations getting in the way.
    """
    family = task['family']
    for p_ in (task['ctl_file'], task['exp_file']):
        if not os.path.isfile(p_):
            return None
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if task['varnos']:
        element = ",".join(str(v) for v in task['varnos'])
    lev = (VCOORD or '').strip() or 'vcoord'
    cycle = task['cycle']
    from pikobs.match import (DEFAULT_KEY, MatchSpec, count_repeats,
                              key_aliases, key_join, key_select)
    spec = MatchSpec(True, tuple(task.get('match_fields') or DEFAULT_KEY))
    ksel = key_select(spec)
    names = task.get('names') or ('control', 'experience')
    with work_db(attach={'ctl': task['ctl_file'],
                         'exp': task['exp_file']}) as (conn, mem_uri):
        conn.execute(_DDL_PAIR)
        hcols = {c.lower() for c in table_columns(conn, 'HEADER', 'ctl')}
        codtyp = "h.codtyp" if 'codtyp' in hcols else "0"
        from pikobs.configobs.special_family import special_select
        sp_sel, _ = special_select(family, hcols, bool(task.get('special_on')),
                                   prefix='h.')
        crit = VCOCRIT.replace('vcoord', 'd.vcoord')
        lev_d = lev.replace('vcoord', 'd.vcoord') if lev != 'vcoord' \
            else 'd.vcoord'
        for side in ('c', 'e'):
            db = 'ctl' if side == 'c' else 'exp'
            dcols = {c.lower() for c in table_columns(conn, 'DATA', db)}
            omp = _num('d.omp') if 'omp' in dcols else "NULL"
            oma = _num('d.oma') if 'oma' in dcols else "NULL"
            # keep only rows that can be half of a pair
            has_dep = [f"d.{t} IS NOT NULL" for t in ('omp', 'oma')
                       if t in dcols]
            dep = f"AND ({' OR '.join(has_dep)})" if has_dep else ""
            conn.execute(f"""
                CREATE TEMP TABLE {side} AS
                SELECT {ksel}, h.id_stn AS id_stn, {codtyp} AS codtyp,
                       {sp_sel} AS sp,
                       ROUND(h.lat, 4) AS klat, ROUND(h.lon, 4) AS klon,
                       h.date AS dt, h.time AS tm, d.varno AS varno,
                       d.vcoord AS vraw, {lev_d} AS lev, h.lat AS lat,
                       h.lon AS lon, d.flag AS flag, {omp} AS omp,
                       {oma} AS oma
                FROM {db}.header h JOIN {db}.data d USING(id_obs)
                WHERE d.varno IN ({element}) {dep} {crit};""")
        keys = ", ".join(key_aliases(spec))
        conn.execute(f"CREATE INDEX e_key ON e ({keys});")
        conn.execute(f"CREATE INDEX c_key ON c ({keys});")
        on = key_join(spec, 'e', 'c')
        repeats = {names[0]: count_repeats(conn, 'c', spec),
                   names[1]: count_repeats(conn, 'e', spec)}
        register_land(conn, task['land_oceans'], task['pathwork'])
        regionlib.register(conn, task['regions'], task['pathwork'])
        # One join for every selection. The selections below (region x
        # flag x surface) only filter its rows, so joining again for each
        # one repeated the same work.
        conn.execute(f"""
            CREATE TEMP TABLE pair_rows AS
            SELECT c.id_stn AS id_stn, c.codtyp AS codtyp, c.sp AS sp,
                   c.varno AS varno, c.lev AS lev, c.lat AS lat,
                   c.lon AS lon, c.flag AS flag,
                   (e.id_stn IS NOT NULL) AS both,
                   (e.id_stn IS NULL) AS ctl_only, 0 AS exp_only,
                   -- the sums of the paired tests, over the
                   -- observations both runs have with a departure
                   (c.omp IS NOT NULL AND e.omp IS NOT NULL) AS has_p,
                   (CASE WHEN e.omp IS NOT NULL THEN c.omp END) AS cp,
                   (CASE WHEN c.omp IS NOT NULL THEN e.omp END) AS ep,
                   (c.oma IS NOT NULL AND e.oma IS NOT NULL) AS has_a,
                   (CASE WHEN e.oma IS NOT NULL THEN c.oma END) AS ca,
                   (CASE WHEN c.oma IS NOT NULL THEN e.oma END) AS ea
            FROM c LEFT JOIN e ON {on}
            UNION ALL
            SELECT e.id_stn, e.codtyp, e.sp, e.varno, e.lev, e.lat,
                   e.lon, e.flag, 0, 0, 1, 0, NULL, NULL, 0, NULL,
                   NULL
            FROM e LEFT JOIN c ON {on}
            WHERE c.id_stn IS NULL;""")
        conn.execute("DROP TABLE c;")
        conn.execute("DROP TABLE e;")
        for region, flag, surf, cond in _combos(task['regions'],
                                                task['flags'],
                                                task['land_oceans'],
                                                task['pathwork']):
            conn.execute(f"""
                INSERT INTO ts_pair ({_PAIR_COLS})
                SELECT '{region}', '{flag}', '{surf}', sp, id_stn, codtyp,
                       varno, lev,
                       '{cycle}',
                       SUM(both), SUM(ctl_only), SUM(exp_only),
                       SUM(has_p), SUM(cp), SUM(cp*cp), SUM(ep),
                       SUM(ep*ep), SUM(cp*ep),
                       SUM(has_a), SUM(ca), SUM(ca*ca), SUM(ea),
                       SUM(ea*ea), SUM(ca*ea)
                FROM pair_rows
                WHERE {cond}
                GROUP BY id_stn, codtyp, varno, lev, sp;""")
        _combine_rows(task['db_new'], mem_uri, 'ts_pair', _PAIR_COLS,
                      ddl=_DDL_PAIR, module='timeserie')
    return repeats


def _matched_task(task) -> Optional[int]:
    import traceback
    try:
        return create_matched(task)
    except Exception:
        print(f"[timeserie] matching failed for {task.get('ctl_file')}:"
              f"\n{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def _extract_task(task) -> Optional[int]:
    import traceback
    try:
        return create_ts(task)
    except Exception:
        print(f"[timeserie] extraction failed for {task.get('filein')}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def _index_task(path: str) -> Optional[str]:
    try:
        with open_result(path) as conn:
            for t in ('ts_qc', 'ts_val'):
                conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{t} ON {t} "
                             f"(region, flag, varno, cycle);")
            # every figure with pairs reads ts_pair too: without an index
            # each one scanned the whole table, which grows with the period
            if conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' "
                            "AND name = 'ts_pair';").fetchone():
                conn.execute("CREATE INDEX IF NOT EXISTS idx_ts_pair ON ts_pair "
                             "(region, flag, land_ocean, special, varno, lev, cycle);")
        return path
    except Exception as exc:
        print(f"[timeserie] indexing {path} failed: {exc}", file=sys.stderr,
              flush=True)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def _report_timing(timing, pathwork) -> None:
    sec, p = timing['seconds'], "[timeserie]"
    print(f"{p} -------------------- run time --------------------",
          flush=True)
    print(f"{p} input        {fmt_bytes(timing['input_bytes']):>10s}   "
          f"{timing['input_files']} files, {timing['cycles']} cycles, "
          f"{timing['runs']} run(s)", flush=True)
    for phase in ('extraction', 'match', 'plots'):
        if phase in sec:
            print(f"{p} {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(f"{p} total        {sec['total']:>8.1f} s   "
          f"({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
          flush=True)
    try:
        with open(os.path.join(pathwork, "timeserie_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError:
        pass


from pikobs.configobs.special_family import special_key_label  # noqa: E402


def _functions(values):
    """omp, oma or both, in the order given; omp when nothing is given."""
    out = [v for v in dict.fromkeys(_split_tokens(values or [])) if v]
    bad = [v for v in out if v not in ('omp', 'oma')]
    if bad:
        sys.exit(f"[timeserie] FONCTION: {bad} -- omp or oma")
    return out or ['omp']


def make_timeserie(runs, pathwork, datestart, dateend, regions, families,
                   flags_criteria, varnos, id_stn, channel, land_ocean,
                   n_cpu,
                   control=None, svg: bool = False,
                   alert_pct: float = 0.0, match=True,
                   special_column='off', functions=('omp',),
                   pressure_layers=(), height_layers=()) -> int:
    from pikobs.timeserie.timeserie_plot import plan_figures, plot_task
    p = "[timeserie]"
    regions = _split_tokens(regions) or ['Monde']
    flags = _split_tokens(flags_criteria) or ['all']
    stn_tokens = parse_station_tokens(id_stn)
    channels = _split_tokens(channel) or ['join']
    land_oceans = [lo for lo in (_split_tokens(land_ocean) or ['all'])
                   if lo in ('all', 'land', 'ocean')] or ['all']
    special_on = str(special_column).strip().lower() in ('on', 'true', '1', 'yes')
    varnos = _split_tokens(varnos)
    all_runs = ([control] if control else []) + list(runs)

    print(f"{p} runs: {', '.join(n for n, _ in all_runs)}"
          + (f"  |  control: {control[0]}" if control else ""), flush=True)
    poly = [r for r in regions if regionlib.is_polygon(r)]
    if poly:
        print(f"{p} regions drawn as polygons: "
              f"{', '.join(poly)}", flush=True)
    print(f"{p} regions: {regions}  |  flags: {flags}  |  id_stn: "
          f"{stn_tokens}  |  channel: {channels}  |  land_ocean: "
          f"{land_oceans}  |  special column: "
          f"{'on' if special_on else 'off'}", flush=True)
    if alert_pct > 0:
        print(f"{p} alerts: a cycle whose observations fall more than "
              f"{alert_pct:g} % below the median of the same hour on the "
              f"days before it", flush=True)
    if not check_input_files(all_runs, families, datestart, dateend,
                             'timeserie'):
        return 1
    t_start = time.time()
    cycle_list = _cycles(datestart, dateend)
    n_input, input_bytes = input_size(all_runs, families, cycle_list)
    timing: Dict[str, Any] = {
        'datestart': datestart, 'dateend': dateend,
        'cycles': len(cycle_list), 'families': list(families),
        'runs': len(all_runs), 'regions': regions, 'flags': flags,
        'id_stn': stn_tokens, 'channel': channels,
        'land_ocean': land_oceans, 'alert_pct': alert_pct,
        'match': match,
        'svg': svg, 'n_cpus': n_cpu, 'input_files': n_input,
        'input_bytes': input_bytes, 'seconds': {},
    }
    for family in families:
        pikobs.delete_create_folder(pathwork, family)
    # MATCH: on, off, or the fields of the key -- pikobs.match decides.
    # A bool still works for anyone calling this directly. Past this
    # point match is 'on' / 'off' as before; the key travels in spec.
    from pikobs.match import MatchSpec, parse_match
    if match is True or match is False:
        match = 'on' if match else 'off'
    spec = parse_match(match)
    if not control:
        spec = MatchSpec(False, ())
    match = 'on' if spec.enabled else 'off'
    if match != 'off':
        print(f"{p} match: the figures keep every observation of every "
              f"run; the change of each cycle is tested on the ones the "
              f"runs share with {control[0]} (key: {spec.label})",
              flush=True)
    tasks = [{'family': family, 'regions': regions, 'flags': flags,
              'land_oceans': land_oceans, 'pathwork': pathwork,
              'special_on': special_on,
              'varnos': varnos, 'cycle': cycle,
              'filein': cycle_path(path, cycle, family),
              'db_new': db_path(pathwork, family, name, datestart, dateend)}
             for name, path in all_runs for cycle in cycle_list
             for family in families]

    client, dask_dir = None, None
    if n_cpu > 1:
        os.environ["DASK_LOGGING__DISTRIBUTED"] = "error"
        dask_dir = tempfile.mkdtemp(prefix="pikobs_timeserie_dask_",
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
        timing['seconds']['extraction'] = time.time() - t0
        print(f"{p} extraction time: {timing['seconds']['extraction']:.1f}s "
              f"({sum(r is not None for r in res)}/{len(tasks)} files)",
              flush=True)
        if match != 'off':
            pair_tasks = [
                {'family': family, 'regions': regions, 'flags': flags,
                 'land_oceans': land_oceans, 'pathwork': pathwork,
                 'special_on': special_on,
                 'varnos': varnos, 'cycle': cycle,
                 'ctl_file': cycle_path(control[1], cycle, family),
                 'exp_file': cycle_path(path, cycle, family),
                 'match_fields': spec.fields,
                 'names': (control[0], name),
                 'db_new': db_path(pathwork, family, name, datestart,
                                   dateend)}
                for name, path in runs for cycle in cycle_list
                for family in families]
            t0 = time.time()
            print(f"{p} matching: {len(pair_tasks)} tasks", flush=True)
            rp = run_tasks(_matched_task, [(t,) for t in pair_tasks], client,
                           label='match')
            timing['seconds']['match'] = time.time() - t0
            print(f"{p} match time: "
                  f"{timing['seconds']['match']:.1f}s "
                  f"({sum(r is not None for r in rp)}/{len(pair_tasks)})",
                  flush=True)
            # one line per family when the key was not unique somewhere
            from pikobs.match import add_counts, repeat_warning
            repeats: Dict[str, Dict[str, List[int]]] = {}
            for t, r in zip(pair_tasks, rp):
                if isinstance(r, dict):
                    add_counts(repeats.setdefault(t['family'], {}), r)
            for fam in families:
                msg = repeat_warning('timeserie', fam, spec,
                                     repeats.get(fam, {}))
                if msg:
                    print(msg, file=sys.stderr, flush=True)
        dbs = sorted({t['db_new'] for t in tasks})
        run_tasks(_index_task, [(d,) for d in dbs], client, label='indexing')

        for family in families:
            dbs_f = [db_path(pathwork, family, n, datestart, dateend)
                     for n, _ in all_runs]
            selectors = expand_station_selectors(dbs_f, stn_tokens, family,
                                                 table='ts_qc')
            figures += plan_figures(family, all_runs, control, selectors,
                                    regions, flags, channels, pathwork,
                                    datestart, dateend, db_path, svg,
                                    alert_pct, match,
                                    functions=functions,
                                    pressure_layers=pressure_layers,
                                    height_layers=height_layers)
        if not figures:
            print(f"{p} WARNING: nothing to plot, check the selectors.",
                  file=sys.stderr, flush=True)
            return 1
        t0 = time.time()
        print(f"{p} plots: {len(figures)} tasks", flush=True)
        results = run_tasks(plot_task, [(f,) for f in figures], client,
                            label='plots')
        timing['seconds']['plots'] = time.time() - t0
        n_drawn = sum(r is not None for r in results)
        print(f"{p} plot time: {timing['seconds']['plots']:.1f}s "
              f"({n_drawn}/{len(figures)})", flush=True)
        # A figure that comes back empty is not a failure: the selection
        # simply had nothing in it -- a station that did not report in
        # the period, a varno the family does not carry, a region with no
        # observation. Saying so costs one line and saves the reader
        # wondering which figures went missing and why.
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

    # the alerts of every figure, one table
    if alert_pct > 0:
        alerts = [a for r in results if r for a in r[1]]
        out_csv = os.path.join(pathwork, "timeserie_alerts.csv")
        with open(out_csv, 'w', newline='') as fh:
            w = csv.writer(fh)
            w.writerow(["run", "family", "region", "criteria", "station",
                        "varno", "level", "cycle", "n", "median_same_hour",
                        "drop_pct"])
            w.writerows(alerts)
        print(f"{p} alerts: {len(alerts)} cycle(s): {out_csv}", flush=True)

    items = [dict(f['viewer'], filename=os.path.basename(r[0]))
             for f, r in zip(figures, results) if r]
    if not items:
        print(f"{p} ERROR: no figure was produced.", file=sys.stderr,
              flush=True)
        return 1
    kinds = {str(pikobs.family(f)[5]).strip().upper().startswith('CANAL')
             for f in families}
    level_label = ("Channel" if kinds == {True} else
                   "Vcoord" if kinds == {False} else "Channel / vcoord")
    generate_web(
        items, ["experience", "family", "fonction", "region", "flag_criteria",
                "land_ocean", "id_stn", "special", "layer", "varno", "channel"],
        os.path.join(pathwork, "pikobs_timeserie_viewer.html"),
        title="Pikobs Time Series Viewer",
        subtitle=(
            "Every 6-h cycle: how many observations come in, stacked by what "
            "the quality control did with them (the diagnosis of "
            "flag_reason, as in the flags module), and -- when the files "
            "carry them -- the mean and sigma of the departures, the "
            "assigned error and the bias correction." +
            (f" <b>all runs</b> puts every run on the same axes, "
             f"{control[0]} in blue, with the change of the number of "
             f"observations below." if control else "")) + runs_block(all_runs, control, (datestart, dateend)),
        image_subdir_key="family",
        key_labels={"flag_criteria": "Criteria", "channel": level_label,
                    "layer": "Layer",
                    "land_ocean": "Surface",
                    "special": special_key_label(families)},
        issues_url="https://gitlab.science.gc.ca/dlo001/Pikobs")
    timing['seconds']['total'] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"{p} done -- output in: {pathwork}", flush=True)
    return 0


def arg_call() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        prog="pikobs-timeserie",
        description="Availability and quality control, cycle by cycle.")
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
    ap.add_argument('--varnos', nargs='*', default=[])
    ap.add_argument('--id_stn', nargs='+', default=['join'])
    ap.add_argument('--channel', '--vcoord', dest='channel', nargs='+',
                    default=['join'])
    ap.add_argument('--land_ocean', nargs='+', default=['all'],
                    help="all, land, ocean: one series each, counted in the "
                         "same pass. land and ocean need the "
                         "global_land_mask package.")
    ap.add_argument('--special_column', default='off', choices=['on', 'off'],
                    help="on: one series of figures per value of the family's "
                         "special column; off: all together (default).")
    ap.add_argument('--match', nargs='+', default=['off'],
                    help="on: with a control, test the change of every "
                         "cycle on the observations the two runs share, "
                         "and fill the bars of the change panels "
                         "accordingly. The curves always keep every "
                         "observation of every run.")
    ap.add_argument('--alert_pct', type=float, default=0.0,
                    help="0: no alerts. X: mark every cycle whose number of "
                         "observations falls more than X %% below the median "
                         "of the 8 cycles before it.")
    ap.add_argument('--svg', default='off', choices=['on', 'off'])
    ap.add_argument('--n_cpus', '--n_cpu', default=1, type=int,
                    dest='n_cpus')
    ap.add_argument('--no_submit', action='store_true')
    # the comparison in O-P (omp, the default), O-A (oma), or both
    ap.add_argument('--fonction', nargs='*', default=None)
    # one series per layer: pressure families in hPa, height ones in km
    ap.add_argument('--pressure_layers', nargs='*', default=[])
    ap.add_argument('--height_layers', nargs='*', default=[])

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
        control = (cname, cpaths[0].rstrip('/') or '/')
    maybe_submit_to_pbs(args)
    sys.exit(make_timeserie(
        runs, args.pathwork, args.datestart, args.dateend, args.region,
        _split_tokens(args.family), args.flags_criteria,
        _split_tokens(args.varnos), args.id_stn, args.channel,
        args.land_ocean, args.n_cpus,
        control, svg_enabled(args.svg), args.alert_pct, args.match,
        special_column=args.special_column,
        functions=_functions(args.fonction),
        pressure_layers=[float(x) for x in _split_tokens(args.pressure_layers)],
        height_layers=[float(x) for x in _split_tokens(args.height_layers)]))


if __name__ == '__main__':
    arg_call()
