#!/usr/bin/env python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_obscountdb.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""================================================================
pikobs.obscountdb -- Observation Volume Diagnostics
================================================================

``obscountdb`` answers the first question I ask about any new experience:
did it use more observations than the control, or fewer, and where? It
counts what each run assimilated, family by family, station by station and
cycle by cycle, and puts everything in one HTML report where gains are
green and losses red.

One run covers **every region and every flag criteria at once**. The input
files are read a single time and all the combinations are computed in that
pass, so adding four regions and a second criteria costs almost nothing:
in my tests, fifteen combinations took 2.5 times the time of one, not
fifteen. The report then lets you switch between them with two rows of
buttons.

Quick start
===========

.. code-block:: bash

   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_obscountdb_cont_exp.sh
   chmod +x run_obscountdb_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_obscountdb_cont_exp.sh
   ./run_obscountdb_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(ai sw)`` and ``REGION=(Monde
   Canada)``, not strings. The wrapper passes them as ``"${FAMILY[@]}"``;
   a plain string arrives glued and ends in "missing file" errors.

A run prints its phases and finishes with the address of the report:

.. code-block:: text

   [obscountdb] runs: Control, Experience
   [obscountdb] regions: ['Monde', 'HemisphereNord', 'HemisphereSud', 'Tropiques', 'Canada']
   [obscountdb] flags_criteria: ['assimilee', 'rejets']
   [obscountdb] input check OK: 21 cycles x 2 run(s) x 8 family(ies), 336 files, 94.7 GB
   [obscountdb] extraction: 336 tasks, 80 worker(s)
   [pikobs] extraction: 336/336 (100%) 224s elapsed
   [obscountdb] extraction time: 223.8s (336/336 files)
   [obscountdb] figures: 1240 station plots
   [pikobs] figures: 1240/1240 (100%) 196s elapsed
   [obscountdb] ------------------ run time ------------------
   [obscountdb] input           94.7 GB   336 files, 21 cycles, 2 run(s)
   [obscountdb] extraction      223.8 s
   [obscountdb] figures         196.4 s
   [obscountdb] report           12.7 s
   [obscountdb] total           434.1 s   (7.2 min, 80 workers)
   Report: /home/dlo001/sites8/pikobs_obscountdb_cont_exp/pikobs_obscountdb_viewer.html
   Web:    to open it in a browser, link the folder under public_html once:
             ln -s /home/dlo001/sites8/pikobs_obscountdb_cont_exp /home/dlo001/public_html/
           then: https://goc-dx-u3.science.gc.ca/~dlo001/pikobs_obscountdb_cont_exp/pikobs_obscountdb_viewer.html

`A live reference instance <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_obscountdb/pikobs_obscountdb_viewer.html>`__.

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of both runs and every family is looked up
first. If one is missing the run stops, says which cycles are missing and
which dates the directory does hold, and leaves ``PATHWORK`` untouched, so
a typo in the dates does not erase the previous report.

**Extraction.** Each file is read once. For every (region, criteria) pair
the query carries its own conditional aggregates, so one scan feeds them
all:

.. code-block:: sql

   SUM(CASE WHEN <region> AND <criteria> THEN 1 ELSE 0 END)          -- Nobs
   COUNT(DISTINCT CASE WHEN <region> AND <criteria> THEN id_obs END) -- profiles

For ``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` the rows are grouped by
``codtyp`` and named after the instrument type (AMDAR, TEMP, SYNOP...);
the other families are grouped by ``id_stn``.

**What is stored.** One row per (region, criteria, station, varno,
cycle), with the raw moments of the departures when ``AGR`` asks for them:
:math:`N`, :math:`\sum x`, :math:`\sum x^2`, plus the minimum and the
maximum of the cycle. Next to them sits one row per station holding the
counts of every varno together: the profiles of a station cannot be added
over varnos, since the same ``id_obs`` carries several of them, so they
are counted once there. Means and standard deviations are derived when the
report is built:

.. math::

   \bar{x} = \frac{\sum x}{N},
   \qquad
   \sigma = \sqrt{\max\left(0,\ \frac{\sum x^2}{N} - \bar{x}^2\right)}

Keeping the sums instead of the means is what makes any later grouping
exact: several ``codtyp`` rows folding into one instrument label, or a
whole period folding into one number, are simple additions.

**Figures.** One task per (region, criteria, family, station), spread over
the workers. Each writes its PNG in ``figures/``; the report links them
instead of embedding them, which keeps the HTML at a few hundred kB
instead of hundreds of MB.

**Report.** One ``pikobs_obscountdb_viewer.html`` with the selectors, plus the same
tables as CSV in ``tables/``.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of the wrapper is meant to be edited.
obscountdb always compares, so the control is not optional: without it
the run stops on the first line.

.. wrapper-settings:: run_obscountdb_cont_exp.sh

----

3. The report
=============

+-------------------+--------------------------------------------------------------------------+
| Section           | Content                                                                  |
+===================+==========================================================================+
| Selectors         | Region and Criteria; the choice is kept in the page address              |
+-------------------+--------------------------------------------------------------------------+
| Overall Summary   | Nobs and profiles per family, difference and percentage, mean per 6 h    |
+-------------------+--------------------------------------------------------------------------+
| Station Breakdown | The same per station (per instrument type for ai, sf, ua, gp, csr)       |
+-------------------+--------------------------------------------------------------------------+
| Time series       | One card per station with Nobs and profiles per cycle                    |
+-------------------+--------------------------------------------------------------------------+
| Departures        | With ``AGR``: one card per station and varno, with its own Varno buttons |
+-------------------+--------------------------------------------------------------------------+

The **Region** and **Criteria** buttons sit at the top of the page and
stay there while you scroll. The current choice is written in the page
address, so a link like ``pikobs_obscountdb_viewer.html#Canada|assimilee`` opens
straight on that panel, which is handy in an email.

Everything below the buttons is what the report always showed: the
summary per family, the breakdown per station, and the time-series cards.
Gains are green, losses red, and the mean columns are the totals divided
by the number of 6-h cycles in the period.

Station cards
-------------

Each family has one or two blocks of cards, each card a station framed in
its own colour.

The first block, **Nobs and profiles per station**, is always there, with
or without ``AGR``. The second, **Departures per station and varno**,
appears when ``AGR`` asks for ``omp`` or ``oma``, and above it sits a row
of **Varno** buttons listing the varnos that family really has for the
region and criteria selected at the top of the page. Pressing one changes
the departure cards of that family only; the general cards stay where they
are, and every family keeps its own buttons.

+-----------------------+-----------------------------------------------------------------------+
| Card                  | Rows                                                                  |
+=======================+=======================================================================+
| General, always       | observations per cycle, then profiles per cycle                       |
+-----------------------+-----------------------------------------------------------------------+
| Departures, per varno | mean (solid / dashed) and std (thin dotted, hollow markers) per cycle |
+-----------------------+-----------------------------------------------------------------------+
|                       | max (solid) and min (dashed) of the cycle, with the interval shaded   |
+-----------------------+-----------------------------------------------------------------------+

REF is always blue and EXP always red, in every row. The line above the
card repeats the numbers of the period on two lines, one per metric: mean
and std of each run, and the interval in which the departures stayed.

.. image:: _static/obscountdb_station.png
   :alt: Station card: Nobs, departures and extremes
   :align: center
   :width: 100%

Why the varnos are separate: a family such as ``ua`` carries temperatures
in K, winds in m/s and pressures in Pa, so a mean over all of them means
nothing. The counts are different, and they stay together: ``Nobs`` and
the tables add every varno of the station.

The extremes are worth a look before trusting a mean: a cycle whose
minimum or maximum jumps far away from the others usually means a bad
observation got through, not that the background changed.

----

4. Output layout
================

::

   $PATHWORK/
   ├── pikobs_obscountdb_viewer.html                  <- the report, with the selectors
   ├── obscountdb_timing.json            <- settings and time of each phase
   ├── figures/
   │   └── <region>_<flag>_<family>_<varno>_<station>.png
   ├── tables/
   │   ├── Overall_<region>_<flag>.csv
   │   └── Stations_<family>_<region>_<flag>.csv
   └── <family>/
       └── <run>_<start>_<end>_<family>.db

The ``.db`` files hold one row per (region, criteria, station, varno,
cycle) in the table ``moyenne``, where ``varno = -1`` marks the row with
the counts of the whole station, and can be queried with ``sqlite3``. The CSV files
hold exactly the numbers of the HTML tables, ready for a spreadsheet or a
presentation.

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else.

----

5. Support
==========

Bugs and feature requests:
   `<https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`_
"""

import json
import os
import re
import shutil
import sys
import tempfile
import time
import traceback
import uuid
import warnings
from typing import Any, Dict, List, Optional, Sequence, Tuple

from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.figures import svg_enabled
from pikobs.obsdb import (check_input_files,
                          combine as _combine_rows,
                          open_result, table_columns, work_db)
from pikobs.obsdb.obsdb import split_tokens as _split_tokens, cycles as _cycles, cycle_ranges as _cycle_ranges, input_size as _input_size  # shared, once
from pikobs.parallel import run_tasks
# imported from the sibling module, not from the pikobs namespace, so the
# module works whatever pikobs/__init__.py re-exports
from pikobs.obscountdb.obscountdb_plot import (
    obscountdb_figure_tasks, obscountdb_report, obscountdb_station_figure)

warnings.filterwarnings("ignore", ".*ShapelyDeprecationWarning.*")

import dask
from dask.distributed import Client

# a region is a box or a polygon; the module does not need to know
from pikobs.configobs import regionsobs
import pikobs

CYCLE_HOURS = 6

DICT_CODTYP = {
    '12': 'SYNOP', '13': 'SHIP', '14': 'SYNOP MOBIL', '15': 'METAR', '16': 'SPECI',
    '18': 'DRIFTER', '32': 'PILOT', '33': 'PILOT SHIP', '34': 'PILOT MOBIL',
    '35': 'TEMP', '36': 'TEMP SHIP', '37': 'TEMP DROP', '38': 'TEMP MOBIL',
    '42': 'AMDAR', '128': 'AIREP', '134': 'PAOBS', '135': 'TEMP + PILOT',
    '136': 'TEMP + SYNOP', '139': 'TEMP SHIP + PILOT SHIP', '143': 'SWOB-NONAUTO',
    '144': 'SWOB-AUTO', '145': 'Patrol ship', '146': 'ASYNOP', '147': 'BUOYS',
    '148': 'SWOBNONAUTO-SPECIAL', '149': 'SWOBAUTO-SPECIAL', '157': 'BUFR',
    '159': 'TEMP PILOT MOBIL', '163': 'RADAR', '164': 'AMSUA', '168': 'SSMIS',
    '169': 'GPSRO', '177': 'ADS', '181': 'AMSUB', '182': 'MHS', '183': 'AIRS',
    '185': 'CSR', '186': 'IASI', '188': 'AMVS', '189': 'GROUND BASED GPS',
    '192': 'ATMS', '193': 'CRIS NSR', '195': 'constituants chimiques (remote)',
    '196': 'constituants chimiques (in-situ)', '198': 'NetWork of Network',
    '200': 'MWHS-2', '202': 'CRIS FSR', '254': 'SCAT',
}

FAMILY_CODES = {
    'ai':  ['42', '128', '157', '177'],
    'sf':  ['12', '13', '14', '15', '16', '18', '143', '144', '145', '146',
            '147', '148', '149', '198'],
    'gp':  ['189'],
    'csr': ['185'],
    'ua':  ['32', '33', '34', '35', '36', '37', '38', '135', '139'],
}

# Departure metrics that --agr may request.
AGR_METRICS = ('omp', 'oma')

# One row per (region, flag, station, varno, cycle). Sums are kept instead
# of mean / std so that any later grouping recombines exactly.
# varno = TOTAL_VARNO holds the counts of the station over every varno:
# profiles cannot be summed over varnos (the same id_obs carries several),
# so they are counted once in that row. The other rows carry the departure
# moments of one varno, and only when --agr asks for them.
TOTAL_VARNO = -1

_MOYENNE_COLS = ("region, flag, id_stn, varno, date, Nobsdata, Nobsprofile, "
                 "n_omp, s_omp, s2_omp, min_omp, max_omp, "
                 "n_oma, s_oma, s2_oma, min_oma, max_oma")

_DDL_MOYENNE = """
    CREATE TABLE IF NOT EXISTS moyenne (
        region      TEXT,
        flag        TEXT,
        id_stn      TEXT,
        varno       INTEGER,
        date        INTEGER,
        Nobsdata    NUMERIC,
        Nobsprofile NUMERIC,
        n_omp       NUMERIC, s_omp NUMERIC, s2_omp NUMERIC,
        min_omp     NUMERIC, max_omp NUMERIC,
        n_oma       NUMERIC, s_oma NUMERIC, s2_oma NUMERIC,
        min_oma     NUMERIC, max_oma NUMERIC
    );
"""


# ─────────────────────────────────────────────────────────────────────────────
# Small helpers
# ─────────────────────────────────────────────────────────────────────────────

def _norm_agr(agr) -> List[str]:
    """Ordered, de-duplicated list of valid metrics ('omp', 'oma')."""
    if agr is None:
        return []
    if isinstance(agr, str):
        agr = [agr]
    out = []
    for a in agr:
        a = str(a).strip().lower()
        if a in AGR_METRICS and a not in out:
            out.append(a)
    return out


def _fmt_bytes(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}"
        n /= 1024.0


def db_path(work_path: str, family: str, name: str,
            date_start: str, date_end: str) -> str:
    """One database per run and family; region and flag are columns."""
    safe = str(name).replace(' ', '_').replace('/', '_')
    return os.path.join(work_path, family,
                        f"{safe}_{date_start}_{date_end}_{family}.db")


# ─────────────────────────────────────────────────────────────────────────────
# Input check
# ─────────────────────────────────────────────────────────────────────────────

def create_table_if_not_exists(cursor) -> None:
    cursor.execute(_DDL_MOYENNE)


def _combinations(regions: Sequence[str],
                  flags: Sequence[str]) -> List[Dict[str, str]]:
    """(region, flag) pairs with the SQL condition of each."""
    combos = []
    for region in regions:
        latlon = regionsobs.criteria(region)
        for flag in flags:
            flag_sql = pikobs.flag_criteria(flag)
            combos.append({
                'region': region,
                'flag': flag,
                # the fragments start with AND, so wrap them in 1=1 ...
                'cond': f"((1=1 {latlon}) AND (1=1 {flag_sql}))",
            })
    return combos


def create_and_populate_moyenne_table(
        family: str,
        new_db_filename: str,
        existing_db_filename: str,
        regions: Sequence[str],
        flags: Sequence[str],
        agr: Optional[Sequence[str]] = None) -> Optional[int]:
    """Read one RDB file once and store the counts of every region and flag.

    Each (region, flag) pair becomes a set of conditional aggregates in a
    single GROUP BY, so the file is scanned once no matter how many
    regions or criteria are asked for.
    """
    if not os.path.isfile(existing_db_filename):
        # silent here: the input check named them all before the run, and
        # the summary after the extraction groups them by family
        return None

    date_match = re.search(r'(\d{10})', os.path.basename(existing_db_filename))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {existing_db_filename}")
    date_int = int(date_match.group(1))

    agr_list = _norm_agr(agr)
    combos = _combinations(regions, flags)

    with work_db(attach={'db': existing_db_filename}) as (conn, mem_uri):

        data_cols = [r[1].lower() for r in
                     conn.execute("PRAGMA db.table_info('DATA');")]
        if not data_cols:
            print(f"[obscountdb] no DATA table in {existing_db_filename}",
                  file=sys.stderr, flush=True)
            return None
        metrics = [m for m in agr_list if m in data_cols]
        for m in agr_list:
            if m not in metrics:
                print(f"[obscountdb] column '{m}' not in "
                      f"{os.path.basename(existing_db_filename)}, stored as "
                      f"NULL", file=sys.stderr, flush=True)

        FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)

        if family in FAMILY_CODES:
            case = ["CASE CAST(codtyp AS TEXT)"]
            case += [f"WHEN '{code}' THEN '{name}'"
                     for code, name in DICT_CODTYP.items()]
            case.append("ELSE CAST(codtyp AS TEXT) END")
            id_stn_expr = " ".join(case)
            codes = ", ".join(f"'{c}'" for c in FAMILY_CODES[family])
            family_filter = f"AND CAST(codtyp AS TEXT) IN ({codes})"
            group_col = "codtyp"
        else:
            id_stn_expr = "id_stn"
            family_filter = ""
            group_col = "id_stn"

        by_varno = bool(metrics)
        # each condition once per row: the subquery computes them as k<i>,
        # with what both passes group and sum, and LIMIT -1 keeps SQLite
        # from folding them back into every aggregate
        pre_cols = [f"({c['cond']}) AS k{i}" for i, c in enumerate(combos)]
        metric_cols = "".join(f", {m}" for m in metrics)
        pre_from = (f"(SELECT {id_stn_expr} AS stn, {group_col} AS grp, varno, "
                    f"id_obs{metric_cols}, {', '.join(pre_cols)} "
                    f"FROM db.header NATURAL JOIN db.DATA "
                    f"WHERE obsvalue IS NOT NULL {VCOCRIT} {family_filter} "
                    f"LIMIT -1)")
        selects = ["stn AS stn"]
        if by_varno:
            selects.append("varno AS varno")
        for i, c in enumerate(combos):
            cond = f"k{i}"
            selects.append(f"SUM(CASE WHEN {cond} THEN 1 ELSE 0 END) AS c{i}_nd")
            selects.append(f"COUNT(DISTINCT CASE WHEN {cond} THEN id_obs END) "
                           f"AS c{i}_np")
            for m in AGR_METRICS:
                if m in metrics:
                    ok = f"{cond} AND {m} IS NOT NULL"
                    selects.append(
                        f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END) AS c{i}_n{m}")
                    selects.append(
                        f"SUM(CASE WHEN {ok} THEN {m} END) AS c{i}_s{m}")
                    selects.append(
                        f"SUM(CASE WHEN {ok} THEN {m}*{m} END) AS c{i}_q{m}")
                    selects.append(
                        f"MIN(CASE WHEN {ok} THEN {m} END) AS c{i}_m{m}")
                    selects.append(
                        f"MAX(CASE WHEN {ok} THEN {m} END) AS c{i}_x{m}")
                else:
                    selects += [f"NULL AS c{i}_n{m}", f"NULL AS c{i}_s{m}",
                                f"NULL AS c{i}_q{m}", f"NULL AS c{i}_m{m}",
                                f"NULL AS c{i}_x{m}"]

        group_by = "grp, varno" if by_varno else "grp"
        query = f"""
            SELECT {", ".join(selects)}
            FROM {pre_from}
            GROUP BY {group_by};
        """
        import time as _time
        _t0 = _time.time()
        rows = conn.execute(query).fetchall()
        _t1 = _time.time()

        # Station totals: with several varnos the profiles of one station
        # cannot be summed over them (one id_obs carries several varnos),
        # so they are counted once here.
        totals = {}
        # a station with a single varno -- every radiance -- has its totals
        # in its own row; the second pass over the file is only for the
        # stations whose profiles carry several varnos
        _nv = {}
        for row in (rows if by_varno else ()):
            _nv[row[0]] = _nv.get(row[0], 0) + 1
        if by_varno and _nv and all(v == 1 for v in _nv.values()):
            _per = 2 + 5 * len(AGR_METRICS)
            for row in rows:
                totals[row[0]] = tuple(
                    x for i in range(len(combos))
                    for x in row[2 + i * _per:2 + i * _per + 2])
        elif by_varno:
            tot_selects = ["stn AS stn"]
            for i, c in enumerate(combos):
                cond = f"k{i}"
                tot_selects.append(
                    f"SUM(CASE WHEN {cond} THEN 1 ELSE 0 END) AS c{i}_nd")
                tot_selects.append(
                    f"COUNT(DISTINCT CASE WHEN {cond} THEN id_obs END) "
                    f"AS c{i}_np")
            for row in conn.execute(f"""
                SELECT {", ".join(tot_selects)}
                FROM {pre_from}
                GROUP BY grp;
            """):
                totals[row[0]] = row[1:]

        if os.environ.get("PIKOBS_TIMING"):
            print(f"[obscountdb timing] {family}: main pass {_t1 - _t0:.1f}s "
                  f"({len(rows)} rows), totals {_time.time() - _t1:.1f}s",
                  file=sys.stderr, flush=True)
        # unpivot: one row per (region, flag, station, varno)
        n_per_combo = 2 + 5 * len(AGR_METRICS)
        n_stats = 5 * len(AGR_METRICS)
        out_rows = []
        for row in rows:
            stn = row[0]
            varno = int(row[1]) if by_varno else TOTAL_VARNO
            offset = 2 if by_varno else 1
            for i, c in enumerate(combos):
                base = offset + i * n_per_combo
                nd, np_ = row[base], row[base + 1]
                if not nd:
                    continue
                vals = row[base + 2:base + n_per_combo]
                out_rows.append((c['region'], c['flag'], stn, varno, date_int,
                                 nd, np_, *vals))
        for stn, tot in totals.items():
            for i, c in enumerate(combos):
                nd, np_ = tot[2 * i], tot[2 * i + 1]
                if not nd:
                    continue
                out_rows.append((c['region'], c['flag'], stn, TOTAL_VARNO,
                                 date_int, nd, np_, *([None] * n_stats)))

        create_table_if_not_exists(conn)
        conn.executemany(
            f"INSERT INTO moyenne ({_MOYENNE_COLS}) "
            f"VALUES ({', '.join('?' * (7 + 5 * len(AGR_METRICS)))});",
            out_rows)
        _combine_rows(new_db_filename, mem_uri, 'moyenne',
                      _MOYENNE_COLS, ddl=_DDL_MOYENNE,
                      module='obscountdb')
        return len(out_rows)


# one traceback is enough to explain a failure; the ones that follow are
# the same error again, and the summary counts them all
_SHOWN_TRACEBACK = []


def _extract_task(task: Dict[str, Any]) -> Optional[int]:
    try:
        return create_and_populate_moyenne_table(
            task['family'], task['db_new'], task['filein'],
            task['regions'], task['flags'], task['agr'])
    except Exception as exc:
        if not _SHOWN_TRACEBACK:
            _SHOWN_TRACEBACK.append(True)
            print(f"[obscountdb] extraction failed for {task['filein']}:\n"
                  f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        else:
            print(f"[obscountdb] extraction failed for "
                  f"{os.path.basename(task['filein'])}: {exc}",
                  file=sys.stderr, flush=True)
        return None


def create_data_list(date_start: str, date_end: str, families: List[str],
                     runs: Sequence[Tuple[str, str]], work_path: str,
                     regions: List[str], flags: List[str],
                     agr: List[str]) -> List[Dict[str, Any]]:
    """One task per (cycle, family, run): every region and flag at once."""
    tasks = []
    for cycle in _cycles(date_start, date_end):
        for family in families:
            for name, path in runs:
                tasks.append({
                    'family': family,
                    'filein': os.path.join(path, f'{cycle}_{family}'),
                    'db_new': db_path(work_path, family, name,
                                      date_start, date_end),
                    'regions': list(regions),
                    'flags': list(flags),
                    'agr': list(agr),
                })
    return tasks


def _index_task(path: str) -> Optional[str]:
    """Index each output database on the columns the report filters on."""
    try:
        with open_result(path) as conn:
            # a family with no file at all leaves an empty database: there
            # is nothing to index, and nothing to complain about
            if not conn.execute("SELECT 1 FROM sqlite_master WHERE type = "
                                "'table' AND name = 'moyenne';").fetchone():
                return path
            conn.execute("CREATE INDEX IF NOT EXISTS idx_moyenne "
                         "ON moyenne (region, flag, varno, id_stn, date);")
        return path
    except Exception as exc:
        print(f"[obscountdb] indexing {path} failed: {exc}",
              file=sys.stderr, flush=True)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def _run(func, arg_tuples: List[tuple], client, label=None) -> List[Any]:
    """Thin wrapper over the shared runner (progress + fault tolerance)."""
    return run_tasks(func, arg_tuples, client, label=label)


def _report_timing(timing: Dict[str, Any], pathwork: str) -> None:
    sec = timing['seconds']
    print("[obscountdb] ------------------ run time ------------------",
          flush=True)
    print(f"[obscountdb] input        {_fmt_bytes(timing['input_bytes']):>10s}"
          f"   {timing['input_files']} files, {timing['cycles']} cycles, "
          f"{timing['runs']} run(s)", flush=True)
    for phase in ('extraction', 'figures', 'report'):
        if phase in sec:
            print(f"[obscountdb] {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(f"[obscountdb] total        {sec['total']:>8.1f} s"
          f"   ({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
          flush=True)
    try:
        with open(os.path.join(pathwork, "obscountdb_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError as exc:
        print(f"[obscountdb] could not write obscountdb_timing.json: {exc}",
              file=sys.stderr, flush=True)


def make_obscountdb(files_in: List[str], names_in: List[str], pathwork: str,
                 datestart: str, dateend: str, regions: List[str],
                 families: List[str], flag_criteria: List[str], n_cpu: int,
                 agr: Optional[List[str]] = None,
                 svg: bool = False) -> int:
    """Extract the counts, draw the figures and write the HTML report."""
    runs = list(zip(names_in, files_in))
    regions = _split_tokens(regions)
    flags = _split_tokens(flag_criteria)
    agr_list = _norm_agr(agr)

    print(f"[obscountdb] runs: {', '.join(n for n, _ in runs)}", flush=True)
    print(f"[obscountdb] regions: {regions}", flush=True)
    print(f"[obscountdb] flags_criteria: {flags}", flush=True)
    if agr_list:
        print(f"[obscountdb] departures: {agr_list}", flush=True)

    # a missing cycle is a warning, not a stop: the run goes on and those
    # cycles count zero, so a gap in one archive still gives a report
    check_input_files(runs, families, datestart, dateend, 'obscountdb',
                      strict=False)

    t_start = time.time()
    cycles = _cycles(datestart, dateend)
    n_input, input_bytes = _input_size(runs, families, cycles)
    timing: Dict[str, Any] = {
        'datestart': datestart, 'dateend': dateend, 'cycles': len(cycles),
        'families': list(families), 'runs': len(runs),
        'regions': regions, 'flags': flags, 'agr': agr_list,
        'n_cpus': n_cpu, 'svg': svg,
        'input_files': n_input, 'input_bytes': input_bytes, 'seconds': {},
    }

    for family in families:
        pikobs.delete_create_folder(pathwork, family)

    tasks = create_data_list(datestart, dateend, families, runs, pathwork,
                             regions, flags, agr_list)
    skipped: Dict[tuple, List[str]] = {}

    parallel = n_cpu > 1
    client = None
    dask_dir = None
    if parallel:
        os.environ["DASK_LOGGING__DISTRIBUTED"] = "error"
        base = os.environ.get("TMPDIR") or None
        dask_dir = tempfile.mkdtemp(prefix="pikobs_obscount_dask_", dir=base)
        os.environ["DASK_TEMPORARY_DIRECTORY"] = dask_dir
        dask.config.set({"temporary-directory": dask_dir,
                         "logging.distributed": "error"})
        client = Client(processes=True, threads_per_worker=1, n_workers=n_cpu,
                        silence_logs=50, dashboard_address=None)
    try:
        t0 = time.time()
        print(f"[obscountdb] extraction: {len(tasks)} tasks, "
              f"{n_cpu} worker(s)", flush=True)
        res = _run(_extract_task, [(t,) for t in tasks], client,
                   label='extraction')
        timing['seconds']['extraction'] = time.time() - t0
        print(f"[obscountdb] extraction time: "
              f"{timing['seconds']['extraction']:.1f}s "
              f"({sum(r is not None for r in res)}/{len(tasks)} files)",
              flush=True)
        # what could not be read, so the report can say it: a file that is
        # not there, and a file that is there but failed
        for task, out in zip(tasks, res):
            if out is not None:
                continue
            run_name = os.path.basename(os.path.dirname(task['db_new']))
            key = ('missing' if not os.path.isfile(task['filein'])
                   else 'failed')
            skipped.setdefault((key, task['family']), []).append(
                os.path.basename(task['filein'])[:10])
        timing['skipped'] = {f"{k[0]} {k[1]}": sorted(v)
                             for k, v in skipped.items()}
        for (kind, family), cyc in sorted(skipped.items()):
            print(f"[obscountdb] WARNING: {len(cyc)} {kind} file(s) for "
                  f"'{family}', counted as zero: "
                  f"{', '.join(_cycle_ranges(sorted(set(cyc))))}",
                  file=sys.stderr, flush=True)

        dbs = sorted({t['db_new'] for t in tasks})
        _run(_index_task, [(d,) for d in dbs], client, label='indexing')

        # Figures: one task per (region, flag, family, station)
        t0 = time.time()
        fig_tasks = obscountdb_figure_tasks(
            pathwork, families, names_in, regions, flags,
            datestart, dateend, agr_list)
        for t in fig_tasks:
            t['svg'] = svg
        print(f"[obscountdb] figures: {len(fig_tasks)} station plots",
              flush=True)
        cells = _run(obscountdb_station_figure,
                     [(t,) for t in fig_tasks], client, label='figures')
        timing['seconds']['figures'] = time.time() - t0
        print(f"[obscountdb] figure time: {timing['seconds']['figures']:.1f}s "
              f"({sum(c is not None for c in cells)}/{len(fig_tasks)})",
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

    t0 = time.time()
    obscountdb_report(
        pathwork=pathwork, families=families, names_in=names_in,
        paths_in=files_in, regions=regions, flags=flags,
        datestart=datestart, dateend=dateend, agr=agr_list,
        figures=[c for c in cells if c], skipped=skipped)
    timing['seconds']['report'] = time.time() - t0
    timing['seconds']['total'] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"[obscountdb] done -- output in: {pathwork}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

_UNSET = ('', 'undefined', None)


def arg_call() -> None:
    import argparse

    p = argparse.ArgumentParser(
        prog="pikobs-obscountdb",
        description="Observation volume, control vs experience.")
    p.add_argument('--path_control_files', default='')
    p.add_argument('--control_name', default='')
    p.add_argument('--path_experience_files', default='')
    p.add_argument('--experience_name', default='')
    p.add_argument('--pathwork', default=None)
    p.add_argument('--datestart', default=None)
    p.add_argument('--dateend', default=None)
    p.add_argument('--region', nargs='+', default=None)
    p.add_argument('--family', nargs='+', default=None)
    p.add_argument('--flags_criteria', nargs='+', default=None,
                   help="One or more criteria, e.g. assimilee rejets all.")
    p.add_argument('--agr', nargs='+', default=None, choices=['omp', 'oma'],
                   help="Add a departure panel per cycle (mean and std) to "
                        "the station time series.")
    p.add_argument('--svg', default='off', choices=['on', 'off'],
                   help="Also write each figure as SVG, next to the PNG, for "
                        "editing before a presentation (default off).")
    p.add_argument('--n_cpus', '--n_cpu', default=1, type=int, dest='n_cpus')
    p.add_argument('--no_submit', action='store_true',
                   help="Skip PBS auto-submission and run locally.")

    args = p.parse_args()
    for attr in ('region', 'family', 'flags_criteria', 'agr'):
        val = getattr(args, attr)
        if isinstance(val, list):
            setattr(args, attr, _split_tokens(val))

    for arg in vars(args):
        print(f'--{arg} {getattr(args, arg)}', flush=True)

    for attr, flag in [('pathwork', '--pathwork'),
                       ('datestart', '--datestart'),
                       ('dateend', '--dateend'),
                       ('region', '--region'),
                       ('family', '--family'),
                       ('flags_criteria', '--flags_criteria')]:
        if getattr(args, attr) in (None, [], 'undefined', ''):
            raise ValueError(f"{flag} is required")

    if args.path_experience_files in _UNSET:
        raise ValueError("--path_experience_files is required")
    if args.experience_name in _UNSET:
        raise ValueError("--experience_name is required")
    if args.path_control_files in _UNSET:
        raise ValueError("--path_control_files is required "
                         "(obscountdb compares two runs)")
    if args.control_name in _UNSET:
        raise ValueError("--control_name is required")

    files_in = [args.path_control_files.rstrip('/') or '/',
                args.path_experience_files.rstrip('/') or '/']
    names_in = [args.control_name, args.experience_name]

    maybe_submit_to_pbs(args)

    sys.exit(make_obscountdb(
        files_in=files_in, names_in=names_in, pathwork=args.pathwork,
        datestart=args.datestart, dateend=args.dateend, regions=args.region,
        families=args.family, flag_criteria=args.flags_criteria,
        n_cpu=args.n_cpus, agr=args.agr, svg=svg_enabled(args.svg)))


if __name__ == "__main__":
    arg_call()
