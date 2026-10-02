#!/usr/bin/python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_cardio.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""====================================================
pikobs.cardio -- Observation Cardiogram Time Series
====================================================

``cardio`` is the module I open first when a suite misbehaves. It draws the
heartbeat of an experience: for every cycle of the period, the bias, the
sigma, the physical values, the number of observations and the extremes
of the departures, one panel above the other and sharing the same time
axis, so a gap in the data and a jump in the departures line up at a
glance.

Give it a control and it stops being a description and becomes a
comparison: the two runs share every panel and each cycle is tested.

It takes several experiences in one run, each with its own time series, and
the viewer switches between them. Regions and flag criteria are computed in
a single pass over the input files, so asking for five regions costs almost
what one costs.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_cardio_exp.sh
   chmod +x run_cardio_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_cardio_cont_exp.sh
   chmod +x run_cardio_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open a
compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_cardio_cont_exp.sh
   ./run_cardio_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(ai sw)`` and ``ID_STN=(join all)``,
   not strings. Quote any token with a ``*`` or a space:
   ``ID_STN=(join "CAS*" "AMDAR (42)")``.

A run prints its phases and ends with the address of the viewer:

.. code-block:: text

   [cardio] runs: E22, E23
   [cardio] id_stn tokens: ['join', 'all']
   [cardio] channel tokens: ['join']
   [cardio] input check OK: 41 cycles x 2 run(s) x 6 family(ies), 492 files, 121.5 GB
   [cardio] extraction: 492 tasks, 80 worker(s)
   [pikobs] extraction: 492/492 (100%) 287s elapsed
   [cardio] plots: 640 tasks
   [cardio] -------------------- run time --------------------
   [cardio] input          121.5 GB   492 files, 41 cycles, 2 run(s)
   [cardio] extraction      287.4 s
   [cardio] plots           212.9 s
   [cardio] total           507.8 s   (8.5 min, 80 workers)
   Viewer: /home/dlo001/sites8/pikobs_cardio_cont_exp/pikobs_cardio_viewer.html
   Web:    https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_cardio_cont_exp/pikobs_cardio_viewer.html

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* `one run on its own <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_cardio_exp/pikobs_cardio_viewer.html>`__
* `G0 against G2 <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_cardio/pikobs_cardio_viewer.html>`__, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of every run and family is looked up first.
A missing one does not stop the run: a time series with a hole is still a
time series. The suites keep about ten days and delete from the front,
so a period chosen in the morning can lose its first cycle by the
afternoon. The run goes on with the files there are, the log says which
cycles are missing for which run and family, and the viewer says it where
it is seen: *input incomplete* in its title and an orange box at the head
of its About. Only a period without a single file stops the run.

**Extraction.** Each file is read once, grouped by station, varno and
channel, with one set of conditional aggregates per (region, criteria)
pair. What is stored are sums, never means:

.. math::

   N,\quad \sum x,\quad \sum x^2 \quad\text{for O-P, O-A and the
   observation},
   \qquad
   N_{b},\quad \sum b \quad\text{for the bias correction}

plus the rejected and accepted counts, the profiles and the locations of
the region. A figure that pools stations or channels then adds sums, which
is exact; averaging per-cycle means and sigmas would not be. This is also
why the module no longer needs the SQLite ``STDDEV`` extension.

**Figures.** One task per (run, family, region, criteria, station
selection, channel, varno), spread over the workers.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_cardio_exp.sh run_cardio_cont_exp.sh

----

3. Choosing the stations and channels
=====================================

``ID_STN`` takes the tokens of the rest of Pikobs, and each one is its own
series of figures:

+-----------------------------+---------------------------------------------------------------------+
| Token                       | Figures produced                                                    |
+=============================+=====================================================================+
| ``join``                    | one figure, every station pooled                                    |
+-----------------------------+---------------------------------------------------------------------+
| ``all``                     | one figure per station, per instrument type for ai, sf, ua, gp, csr |
+-----------------------------+---------------------------------------------------------------------+
| ``CAS`` or ``"CAS*"``       | the stations whose id starts with CAS, pooled                       |
+-----------------------------+---------------------------------------------------------------------+
| ``=NENE``                   | that station only                                                   |
+-----------------------------+---------------------------------------------------------------------+
| ``C%``                      | SQL ``LIKE`` pattern on the station id                              |
+-----------------------------+---------------------------------------------------------------------+
| ``pilot``, ``"AMDAR (42)"`` | instrument types, for the codtyp families                           |
+-----------------------------+---------------------------------------------------------------------+

``CHANNEL`` works the same way: ``join`` merges every channel or level into
one figure, ``all`` gives one figure per channel, and an explicit list
keeps only those. The two combine: ``ID_STN=(all)`` with ``CHANNEL=(all)``
is one figure per station and channel, which is where the count of figures
grows fastest.

----

4. Reading a figure
===================

Four panels share the same time axis:

+-----------+---------------------------------------------+--------------------------------------------+
| Panel     | Lines                                       | Read it for                                |
+===========+=============================================+============================================+
| Bias      | O-P, O-A and the bias correction, per cycle | a drift of the bias, a jump after a change |
+-----------+---------------------------------------------+--------------------------------------------+
| Sigma     | sigma of O-P and O-A per cycle              | a run getting noisier or calmer            |
+-----------+---------------------------------------------+--------------------------------------------+
| Obsvalue  | observation, trial and analysis             | whether the values themselves moved        |
+-----------+---------------------------------------------+--------------------------------------------+
| Counts    | Ndata and Nlocs per cycle                   | data lost or gained, gaps in the suite     |
+-----------+---------------------------------------------+--------------------------------------------+
| O-P range | the minimum and the maximum of each cycle   | one bad observation that a mean hides      |
+-----------+---------------------------------------------+--------------------------------------------+
| O-A range | the same for O-A                            | the same, after the analysis               |
+-----------+---------------------------------------------+--------------------------------------------+

.. image:: _static/cardio_panels.png
   :alt: The four panels of a cardiogram
   :align: center
   :width: 100%

The line above each panel repeats the numbers of the whole period,
weighted by the number of observations of each cycle, one run after the
other.

The last two panels are the ones worth a second look before trusting a
mean. They show the extreme departure of every cycle, the lowest and the
highest, with the interval shaded. A cycle whose maximum jumps far away
from its neighbours almost always means one bad observation got through,
not that the background changed; the mean of that cycle will barely
move, and the sigma will.

Comparing with a control
------------------------

Fill ``PATH_CONTROL_FILES`` and every experience is drawn on the same
panels as the control. **Red is the experience and blue the control**,
in a single run as well; the line says the quantity: O-P and the trial
solid, O-A and the analysis dashed, the observation dash-dot in black,
the bias correction dotted. One key at the top of the figure says it for
every panel, so no legend sits on the curves. With two
experiences you get two figures, each against the same control, and the
viewer switches between them.

Then every cycle is tested, and the ones where the change is more than
noise get a **transparent circle**: red when the experience wins, blue
when the control does. The count is in the header, something like
``14 in this figure``.

The bias goes through the paired t-test and the sigma through the
Pitman-Morgan test, both from :mod:`pikobs.stats`, which explains them.
cardio pairs the two runs observation by observation before it sums
anything, so both tests look at the very same observations on each side,
and that is why a small but steady change shows up. A cycle where the
runs share nothing falls back on Welch and the F-test, which only see each
run's own moments and are far more cautious. With ``MATCH=off`` every
cycle goes that way.

A circle says the change is real, not that it is large: on a cycle with
half a million observations a difference of two hundredths passes
easily. Read the circle together with the line.

The y limits are shared by every figure of a region through
``y_limits_<region>.json``: a larger limit replaces a smaller one, so the
same channel of two experiences, or of two criteria, can be compared
without rescaling by eye. Delete that file to recompute the limits from
scratch.

----

5. The viewer
=============

``pikobs_cardio_viewer.html`` has seven dropdowns: Experience, Criteria,
Family, Region, Station, Varno and Channel; each one only offers what
exists for the choices on its left. **Flip** (key ``F``) swaps between the
current figure and the previous one, which is how two experiences are
compared on the same station, and a click opens the figure at full size.

----

6. Output layout
================

::

   $PATHWORK/
   ├── pikobs_cardio_viewer.html
   ├── cardio_timing.json
   ├── y_limits_<region>.json
   └── <family>/
       ├── cardio_<run>_<start>_<end>_<family>.db
       └── serie_<run>_<flag>_<family>_<stn>_id_stn_<region>[_<surface>][_<special>]_ch<chan>_varno<varno>.png

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else. An SVG keeps every element of the
figure, so ask for it on the one or two figures you actually need.

The ``.db`` files hold one row per (region, criteria, station, varno,
channel, cycle) in the table ``serie_cardio`` and can be queried with
``sqlite3``.

----

7. Support
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
from typing import Any, Dict, List, Optional, Sequence, Tuple

import dask
from dask.distributed import Client

# a region is a box or a polygon; the module does not need to know
from pikobs.configobs import regionsobs
from pikobs.configobs.landmask import register_surface, surface_sql
from pikobs.configobs.special_family import (special_key_label,
                                             special_label, special_select)
import pikobs
from pikobs.cardio.cardio_plot import cardio_plot
from pikobs.figures import svg_enabled
from pikobs.obsdb import (check_input_files,
                          combine as _combine_rows,
                          open_result, table_columns, work_db)
from pikobs.obsdb.obsdb import split_tokens as _split_tokens, cycles as _cycles, cycle_ranges as _cycle_ranges, input_size as _input_size  # shared, once
from pikobs.parallel import run_tasks
from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.web.viewer import generate_web
from pikobs.web.runs import runs_block

from pikobs.stations.stations import (expand_station_selectors,
                                      parse_station_tokens)

CYCLE_HOURS = 6

# One row per (region, flag, station, varno, channel, cycle). Sums are kept
# instead of mean / std: any later grouping is then a plain addition, and
# no SQLite extension is needed for STDDEV.
_SERIE_COLS = ("region, flag, land_ocean, special, id_stn, CODTYP, varno, Chan, date, "
               "Nrej, Nacc, Nprofile, Nloc, "
               "n_omp, s_omp, s2_omp, min_omp, max_omp, "
               "n_oma, s_oma, s2_oma, min_oma, max_oma, "
               "n_obs, s_obs, n_bcorr, s_bcorr")

# The pairs: the same keys as serie_cardio, and per quantity the sums of
# the matched observations. A cycle has one row per selection, so the
# period recombines by adding, exactly as the moments do.
_PAIR_COLS = ("region, flag, land_ocean, special, id_stn, CODTYP, varno, Chan, date, "
              "n_omp, sx_omp, sy_omp, sxx_omp, syy_omp, sxy_omp, "
              "n_oma, sx_oma, sy_oma, sxx_oma, syy_oma, sxy_oma")

_DDL_PAIRS = """
    CREATE TABLE IF NOT EXISTS pairs_cardio (
        region TEXT, flag TEXT, land_ocean TEXT, special TEXT, id_stn TEXT,
        CODTYP INTEGER,
        varno INTEGER, Chan FLOAT, date INTEGER,
        n_omp INTEGER, sx_omp FLOAT, sy_omp FLOAT,
        sxx_omp FLOAT, syy_omp FLOAT, sxy_omp FLOAT,
        n_oma INTEGER, sx_oma FLOAT, sy_oma FLOAT,
        sxx_oma FLOAT, syy_oma FLOAT, sxy_oma FLOAT
    );
"""


_DDL_SERIE = """
    CREATE TABLE IF NOT EXISTS serie_cardio (
        region   TEXT,
        flag     TEXT,
        land_ocean TEXT,
        special  TEXT,
        id_stn   TEXT,
        CODTYP   INTEGER,
        varno    INTEGER,
        Chan     FLOAT,
        date     INTEGER,
        Nrej     INTEGER,
        Nacc     INTEGER,
        Nprofile INTEGER,
        Nloc     INTEGER,
        n_omp    INTEGER, s_omp FLOAT, s2_omp FLOAT,
        min_omp  FLOAT, max_omp FLOAT,
        n_oma    INTEGER, s_oma FLOAT, s2_oma FLOAT,
        min_oma  FLOAT, max_oma FLOAT,
        n_obs    INTEGER, s_obs FLOAT,
        n_bcorr  INTEGER, s_bcorr FLOAT
    );
"""


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _safe(text: Any) -> str:
    return re.sub(r'[^A-Za-z0-9._+-]', '_', str(text))


def _fmt_bytes(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}"
        n /= 1024.0


def _missing_input(runs, families, date_start, date_end):
    """{(run, family): [missing cycles]}, said in the log as it is found;
    None when there is not a single file in the period."""
    cycles = _cycles(date_start, date_end)
    out, found = {}, False
    for name, path in runs:
        for family in families:
            miss = [c for c in cycles
                    if not os.path.isfile(f"{path}/{c}_{family}")]
            if len(miss) < len(cycles):
                found = True
            if miss:
                out[(name, family)] = miss
                ranges = _cycle_ranges(miss)
                print(f"[cardio] WARNING: {name} {family}: {len(miss)}/"
                      f"{len(cycles)} cycles missing, drawn without them: "
                      f"{', '.join(ranges[:4])}{' ...' if len(ranges) > 4 else ''}",
                      flush=True)
    return out if found else None


def _missing_note(missing, n_cycles: int) -> str:
    """The box at the head of the viewer's About when cycles were missing."""
    if not missing:
        return ""
    import html
    rows = []
    for (run, family), cyc in sorted(missing.items()):
        ranges = _cycle_ranges(cyc)
        rows.append(f"<li>{html.escape(str(run))} &middot; {html.escape(family)}: "
                    f"{len(cyc)} of {n_cycles} cycles "
                    f"({html.escape(', '.join(ranges[:4]))}"
                    f"{' &hellip;' if len(ranges) > 4 else ''})</li>")
    return ('<div style="margin:0 0 10px;padding:8px 12px;border-left:4px solid '
            '#d9822b;background:#fff4e5;color:#7a4510"><b>Input incomplete.</b> '
            'The run went on without these files; their cycles are missing '
            'from the curves.<ul style="margin:6px 0 0 18px">'
            + "".join(rows) + '</ul></div>')


def db_path(work_path: str, family: str, name: str, date_start: str,
            date_end: str) -> str:
    """One database per run and family; region and criteria are columns."""
    return os.path.join(work_path, family,
                        f"cardio_{_safe(name)}_{date_start}_{date_end}_"
                        f"{family}.db")


def figure_name(experience, flag, family, id_stn, region, chan, varno,
                land_ocean='all', special='all') -> str:
    """Name of the PNG; the viewer and the plot must agree on it. The land
    filter and the special value are in the name only when there is one,
    so a run without them keeps the names it always had."""
    from pikobs.configobs.special_family import special_label
    land = '' if land_ocean in (None, '', 'all') else f"_{_safe(land_ocean)}"
    # the label of the special value, as every module (IR_channel, 0.5)
    land += ('' if special in (None, '', 'all')
             else f"_{_safe(special_label(family, special))}")
    return (f"serie_{_safe(experience)}_{_safe(flag)}_{_safe(family)}_"
            f"{_safe(id_stn)}_id_stn_{_safe(region)}{land}_ch{_safe(chan)}_"
            f"varno{_safe(varno)}.png")


# ─────────────────────────────────────────────────────────────────────────────
# Input check
# ─────────────────────────────────────────────────────────────────────────────

def create_table_if_not_exists(cursor) -> None:
    cursor.execute(_DDL_SERIE)


def _combinations(regions, flags, land_oceans=('all',)) -> List[Dict[str, str]]:
    """Every (region, surface, criteria): the surface is part of the region,
    so the locations of the region are counted on it too."""
    combos = []
    for region in regions:
        latlon = regionsobs.criteria(region)
        for land_ocean in land_oceans or ('all',):
            surf = surface_sql(land_ocean)
            for flag in flags:
                flag_sql = pikobs.flag_criteria(flag)
                combos.append({
                    'region': region, 'flag': flag, 'land_ocean': land_ocean,
                    'region_cond': f"((1=1 {latlon}){surf})",
                    'cond': f"((1=1 {latlon}) AND (1=1 {flag_sql}){surf})",
                })
    return combos


def create_serie_cardio(family: str, new_db_filename: str,
                        existing_db_filename: str, regions: Sequence[str],
                        flags: Sequence[str],
                        varnos: Sequence[str] = (),
                        land_oceans: Sequence[str] = ('all',),
                        pathwork: str = '.',
                        special_on: bool = False) -> Optional[int]:
    """Read one RDB file once and store the moments of every selection.

    Grouped by station, varno and channel; every (region, criteria) pair is
    a set of conditional aggregates, so the file is scanned a single time.
    """
    if not os.path.isfile(existing_db_filename):
        print(f"[cardio] missing file, skipped: {existing_db_filename}",
              file=sys.stderr, flush=True)
        return None
    date_match = re.search(r'(\d{10})', os.path.basename(existing_db_filename))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {existing_db_filename}")
    date_int = int(date_match.group(1))

    combos = _combinations(regions, flags, land_oceans)
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if varnos:
        element = ",".join(str(v) for v in varnos)
    vcoord_expr = (VCOORD or '').strip() or '9999'

    with work_db(attach={'db': existing_db_filename}) as (conn, mem_uri):
        conn.execute("PRAGMA db.mmap_size = 536870912;")
        register_surface(conn, land_oceans, pathwork)

        data_cols = [r[1].lower() for r in
                     conn.execute("PRAGMA db.table_info('DATA');")]
        head_cols = [r[1].lower() for r in
                     conn.execute("PRAGMA db.table_info('HEADER');")]
        if not data_cols or not head_cols:
            print(f"[cardio] no HEADER/DATA in {existing_db_filename}",
                  file=sys.stderr, flush=True)
            return None
        has_bc = 'bias_corr' in data_cols
        cod = "codtyp" if 'codtyp' in head_cols else "NULL"
        sp_sel, _ = special_select(family, head_cols, special_on)

        # each condition once per row: the subquery below computes them as
        # k<i> (region and criteria) and r<i> (region only), and LIMIT -1
        # keeps SQLite from folding them back into every aggregate -- a
        # third less time on a file of iasi, the same numbers
        pre_cols = []
        for i, c in enumerate(combos):
            pre_cols += [f"({c['cond']}) AS k{i}",
                         f"({c['region_cond']}) AS r{i}"]
        selects = ["id_stn AS stn", "cod AS cod", "varno AS varno",
                   "chan AS chan", "special AS special"]
        for i, c in enumerate(combos):
            cond, region_cond = f"k{i}", f"r{i}"
            selects += [
                f"SUM(CASE WHEN {cond} THEN (flag & 512) = 512 ELSE 0 END) "
                f"AS c{i}_nrej",
                f"SUM(CASE WHEN {cond} THEN (flag & 4096) = 4096 ELSE 0 END) "
                f"AS c{i}_nacc",
                f"COUNT(DISTINCT CASE WHEN {cond} THEN id_obs END) "
                f"AS c{i}_nprof",
                # locations of the region, whatever the flag criteria
                f"COUNT(DISTINCT CASE WHEN {region_cond} THEN id_obs END) "
                f"AS c{i}_nloc",
            ]
            for tag, col in (('omp', 'omp'), ('oma', 'oma'),
                             ('obs', 'obsvalue')):
                ok = f"{cond} AND {col} IS NOT NULL"
                selects.append(f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END) "
                               f"AS c{i}_n{tag}")
                selects.append(f"SUM(CASE WHEN {ok} THEN {col} END) "
                               f"AS c{i}_s{tag}")
                if tag != 'obs':
                    selects.append(f"SUM(CASE WHEN {ok} THEN {col}*{col} END) "
                                   f"AS c{i}_q{tag}")
                    # the extremes of the cycle: a departure far from the
                    # rest is usually one bad observation, not a change
                    # of the background, and a mean will not show it
                    selects.append(f"MIN(CASE WHEN {ok} THEN {col} END) "
                                   f"AS c{i}_min{tag}")
                    selects.append(f"MAX(CASE WHEN {ok} THEN {col} END) "
                                   f"AS c{i}_max{tag}")
            if has_bc:
                ok = f"{cond} AND bias_corr IS NOT NULL"
                selects += [
                    f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END) AS c{i}_nbc",
                    f"SUM(CASE WHEN {ok} THEN bias_corr END) AS c{i}_sbc"]
            else:
                selects += [f"NULL AS c{i}_nbc", f"NULL AS c{i}_sbc"]

        bc_col = ", bias_corr" if has_bc else ""
        rows = conn.execute(f"""
            SELECT {", ".join(selects)}
            FROM (SELECT id_stn, {cod} AS cod, varno, {vcoord_expr} AS chan,
                         {sp_sel} AS special,
                         id_obs, flag, omp, oma, obsvalue{bc_col},
                         {", ".join(pre_cols)}
                  FROM db.header NATURAL JOIN db.data
                  WHERE varno IN ({element})
                    {VCOCRIT}
                  LIMIT -1)
            GROUP BY id_stn, cod, varno, chan, special;
        """).fetchall()

        per_combo = 4 + 5 + 5 + 2 + 2   # counts, omp, oma, obs, bcorr
        out_rows = []
        for row in rows:
            stn, codtyp, varno, chan = row[0], row[1], row[2], row[3]
            special = row[4]
            for i, c in enumerate(combos):
                base = 5 + i * per_combo
                block = row[base:base + per_combo]
                nrej, nacc, nprof, nloc = block[0], block[1], block[2], block[3]
                n_omp, s_omp, q_omp, min_omp, max_omp = block[4:9]
                n_oma, s_oma, q_oma, min_oma, max_oma = block[9:14]
                n_obs, s_obs = block[14], block[15]
                n_bc, s_bc = block[16], block[17]
                if not (nprof or n_omp or n_obs):
                    continue
                out_rows.append((c['region'], c['flag'], c['land_ocean'],
                                 special, stn, codtyp, varno,
                                 chan, date_int, nrej, nacc, nprof, nloc,
                                 n_omp, s_omp, q_omp, min_omp, max_omp,
                                 n_oma, s_oma, q_oma, min_oma, max_oma,
                                 n_obs, s_obs, n_bc, s_bc))

        create_table_if_not_exists(conn)
        conn.executemany(
            f"INSERT INTO serie_cardio ({_SERIE_COLS}) "
            f"VALUES ({', '.join('?' * 27)});", out_rows)
        _combine_rows(new_db_filename, mem_uri, 'serie_cardio',
                      _SERIE_COLS, ddl=_DDL_SERIE,
                      module='cardio')
        return len(out_rows)


def create_pairs_cardio(family: str, pair_db: str, ctl_file: str,
                        exp_file: str, regions: Sequence[str],
                        flags: Sequence[str],
                        varnos: Sequence[str] = (),
                        match_fields: Sequence[str] = (),
                        names=None,
                        land_oceans: Sequence[str] = ('all',),
                        pathwork: str = '.',
                        special_on: bool = False) -> Optional[Dict[str, int]]:
    """Match the two runs observation by observation, one cycle at a time.

    cardio used to test its cycles with Welch, because by the time a
    figure was drawn there were only moments left. This pass keeps, per
    selection and per cycle, the sums of the observations the two runs
    share, which is what a paired test needs -- the same thing scatter
    does per box, and it makes the two modules say the same about the
    same experiment.

    An observation belongs to a pair only when it passes the criteria in
    both runs: each run's flags are read on its own data. The key and
    what happens when it repeats are pikobs.match's: a repeated key is
    paired one to one by value and counted, never dropped.
    """
    for f in (ctl_file, exp_file):
        if not os.path.isfile(f):
            print(f"[cardio] missing file, pairs skipped: {f}",
                  file=sys.stderr, flush=True)
            return None
    date_match = re.search(r'(\d{10})', os.path.basename(ctl_file))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {ctl_file}")
    date_int = int(date_match.group(1))

    combos = _combinations(regions, flags, land_oceans)
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if varnos:
        element = ",".join(str(v) for v in varnos)
    vcoord_expr = (VCOORD or '').strip() or '9999'
    from pikobs.match import (DEFAULT_KEY, MatchSpec, count_repeats,
                              key_aliases, key_join, key_select)
    spec = MatchSpec(True, tuple(match_fields) or DEFAULT_KEY)
    ksel = key_select(spec)
    join_on = key_join(spec)

    with work_db(attach={'c': ctl_file, 'e': exp_file}) as (conn, mem_uri):
        regionsobs.register_pending(conn)
        register_surface(conn, land_oceans, pathwork)

        def cols(schema, table):
            return [r[1].lower() for r in
                    conn.execute(f"PRAGMA {schema}.table_info('{table}');")]

        if not all(cols(s, t) for s in ('c', 'e') for t in ('HEADER', 'DATA')):
            return None
        cod = "codtyp" if 'codtyp' in cols('c', 'HEADER') else "NULL"
        sp_sel, _ = special_select(family, cols('c', 'HEADER'), special_on)

        counts: Dict[str, int] = {}
        for schema in ('c', 'e'):
            conn.execute(f"""
            CREATE TABLE raw_{schema} AS
            SELECT {ksel},
                   id_stn AS stn, {cod} AS cod, varno AS varno,
                   {vcoord_expr} AS chan, {sp_sel} AS special,
                   lat AS lat, lon AS lon, flag AS flag,
                   omp AS omp, oma AS oma
            FROM {schema}.header AS h NATURAL JOIN {schema}.data AS d
            WHERE varno IN ({element}) AND obsvalue IS NOT NULL
                  -- a row with no departure can never be half of a pair:
                  -- the sums only count observations both runs have a
                  -- value for. On the radiances that is most of the file
                  -- (only what was assimilated gets an O-P), so dropping
                  -- them here is the difference between joining 24
                  -- million rows and joining one.
                  AND (omp IS NOT NULL OR oma IS NOT NULL) {VCOCRIT};
            """)
            key = ", ".join(key_aliases(spec))
            # a repeated key is not dropped any more: the rank inside it
            # pairs its observations one to one (pikobs.match)
            n_keys, n_rows = count_repeats(conn, f"raw_{schema}", spec)
            counts[f'obs_{schema}'] = conn.execute(
                f"SELECT COUNT(*) FROM raw_{schema};").fetchone()[0]
            counts[f'rep_keys_{schema}'] = n_keys
            counts[f'rep_rows_{schema}'] = n_rows
            conn.execute(f"ALTER TABLE raw_{schema} RENAME TO key_{schema};")
            conn.execute(f"CREATE INDEX idx_{schema} ON key_{schema} ({key});")

        # One pass over the join, every selection as a conditional sum,
        # exactly the shape the moments already use.
        selects = ["c.stn AS stn", "c.cod AS cod", "c.varno AS varno",
                   "c.chan AS chan", "c.special AS special"]
        for i, combo in enumerate(combos):
            # the region is read on the control's position (they match to
            # 1e-4 degree by construction) and the criteria on each run's
            # own flags: a pair exists only where both runs kept it
            cond = combo['cond'].replace('lat', 'c.lat').replace('lon', 'c.lon')
            cond_c = cond.replace('flag', 'c.flag')
            cond_e = cond.replace('flag', 'e.flag')
            both = f"(({cond_c}) AND ({cond_e}))"
            for tag in ('omp', 'oma'):
                ok = (f"{both} AND c.{tag} IS NOT NULL "
                      f"AND e.{tag} IS NOT NULL")
                selects += [
                    f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END) AS c{i}_n{tag}",
                    f"SUM(CASE WHEN {ok} THEN c.{tag} END) AS c{i}_sx{tag}",
                    f"SUM(CASE WHEN {ok} THEN e.{tag} END) AS c{i}_sy{tag}",
                    f"SUM(CASE WHEN {ok} THEN c.{tag}*c.{tag} END) "
                    f"AS c{i}_sxx{tag}",
                    f"SUM(CASE WHEN {ok} THEN e.{tag}*e.{tag} END) "
                    f"AS c{i}_syy{tag}",
                    f"SUM(CASE WHEN {ok} THEN c.{tag}*e.{tag} END) "
                    f"AS c{i}_sxy{tag}",
                ]

        # how many observations the two runs actually share, counted on
        # the join itself. Counting them per selection instead would add
        # up the regions, and the regions overlap -- the tropics sit
        # inside both hemispheres -- so the total came out larger than
        # the number of observations, which is nonsense on its face.
        counts['pairs'] = conn.execute(
            f"""SELECT COUNT(*) FROM key_c AS c
                JOIN key_e AS e ON {join_on};"""
        ).fetchone()[0]

        rows = conn.execute(f"""
            SELECT {', '.join(selects)}
            FROM key_c AS c JOIN key_e AS e ON {join_on}
            GROUP BY c.stn, c.cod, c.varno, c.chan, c.special;
        """).fetchall()

        out_rows = []
        per_combo = 12                       # 2 quantities x 6 sums
        for row in rows:
            stn, cod_v, varno_v, chan = row[0], row[1], row[2], row[3]
            special = row[4]
            for i, combo in enumerate(combos):
                base = 5 + i * per_combo
                block = row[base:base + per_combo]
                if not (block[0] or block[6]):
                    continue                 # nothing matched here
                out_rows.append((combo['region'], combo['flag'],
                                 combo['land_ocean'], special, stn, cod_v,
                                 varno_v, chan, date_int) + tuple(block))

        if out_rows:
            conn.execute(_DDL_PAIRS)
            conn.executemany(
                f"INSERT INTO pairs_cardio ({_PAIR_COLS}) "
                f"VALUES ({', '.join('?' * 21)});", out_rows)
        for t in ('key_c', 'key_e'):
            conn.execute(f"DROP TABLE {t};")
        conn.execute("DETACH DATABASE c;")
        conn.execute("DETACH DATABASE e;")
        if out_rows:
            _combine_rows(pair_db, mem_uri, 'pairs_cardio', _PAIR_COLS,
                          ddl=_DDL_PAIRS, module='cardio')
        return counts


def _pairs_task(task: Dict[str, Any]) -> Optional[Dict[str, int]]:
    try:
        return create_pairs_cardio(task['family'], task['pair_db'],
                                   task['ctl_file'], task['exp_file'],
                                   task['regions'], task['flags'],
                                   task['varnos'],
                                   task.get('match_fields') or (),
                                   task.get('names'),
                                   task.get('land_oceans') or ('all',),
                                   task.get('pathwork') or '.',
                                   bool(task.get('special_on')))
    except Exception:
        print(f"[cardio] pairing failed for {task['exp_file']}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def _extract_task(task: Dict[str, Any]) -> Optional[int]:
    try:
        return create_serie_cardio(task['family'], task['db_new'],
                                   task['filein'], task['regions'],
                                   task['flags'], task['varnos'],
                                   task.get('land_oceans') or ('all',),
                                   task.get('pathwork') or '.',
                                   bool(task.get('special_on')))
    except Exception:
        print(f"[cardio] extraction failed for {task['filein']}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def create_data_list_cardio(date_start, date_end, families, runs, work_path,
                            regions, flags, varnos,
                            land_oceans=('all',),
                            special_on=False) -> List[Dict[str, Any]]:
    """One task per (cycle, family, run): every region and criteria at once."""
    tasks = []
    for cycle in _cycles(date_start, date_end):
        for family in families:
            for name, path in runs:
                tasks.append({
                    'family': family,
                    'filein': os.path.join(path, f'{cycle}_{family}'),
                    'db_new': db_path(work_path, family, name, date_start,
                                      date_end),
                    'regions': list(regions), 'flags': list(flags),
                    'varnos': list(varnos),
                    'land_oceans': list(land_oceans), 'pathwork': work_path,
                    'special_on': special_on,
                })
    return tasks


def pair_db_path(work_path: str, family: str, ctl: str, exp: str,
                 date_start: str, date_end: str) -> str:
    return os.path.join(work_path, family,
                        f"pairs_{_safe(ctl)}_vs_{_safe(exp)}_"
                        f"{date_start}_{date_end}_{family}.db")


def create_pairs_list(date_start, date_end, families, control, runs,
                      work_path, regions, flags, varnos,
                      land_oceans=('all',), special_on=False) -> List[Dict]:
    """One pairing task per (cycle, family, experience)."""
    ctl_name, ctl_path = control
    tasks = []
    for cycle in _cycles(date_start, date_end):
        for family in families:
            for name, path in runs:
                if name == ctl_name:
                    continue
                tasks.append({
                    'family': family,
                    'ctl_file': os.path.join(ctl_path, f'{cycle}_{family}'),
                    'exp_file': os.path.join(path, f'{cycle}_{family}'),
                    'exp_name': name,
                    'pair_db': pair_db_path(work_path, family, ctl_name,
                                            name, date_start, date_end),
                    'regions': list(regions), 'flags': list(flags),
                    'varnos': list(varnos),
                    'land_oceans': list(land_oceans), 'pathwork': work_path,
                    'special_on': special_on,
                })
    return tasks


def _index_task(path: str) -> Optional[str]:
    """Index the columns the plots filter on."""
    try:
        with open_result(path) as conn:
            conn.execute("CREATE INDEX IF NOT EXISTS idx_serie ON "
                         "serie_cardio (region, flag, land_ocean, special, varno, id_stn, Chan);")
        return path
    except Exception as exc:
        print(f"[cardio] indexing {path} failed: {exc}", file=sys.stderr,
              flush=True)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Plot tasks
# ─────────────────────────────────────────────────────────────────────────────

def _query_distinct(db_paths, sql, params=()) -> List[tuple]:
    seen: Dict[tuple, None] = {}
    for path in db_paths:
        if not os.path.isfile(path):
            continue
        try:
            with open_result(path) as conn:
                rows = conn.execute(sql, params).fetchall()
        except Exception as exc:
            print(f"[cardio] query failed on {os.path.basename(path)}: {exc}",
                  file=sys.stderr, flush=True)
            continue
        for r in rows:
            seen.setdefault(tuple(r), None)
    return list(seen)


def _channel_items(db_paths, where, chan_tokens) -> List[Any]:
    """Channels to plot: 'join' merges them, 'all' gives one each."""
    items: List[Any] = []
    requested = []
    for tok in chan_tokens:
        if tok == 'join':
            items.append('join')
        elif tok == 'all':
            items += [r[0] for r in _query_distinct(
                db_paths, f"SELECT DISTINCT Chan FROM serie_cardio {where};")]
        else:
            requested.append(tok)
    if requested:
        have = [r[0] for r in _query_distinct(
            db_paths, f"SELECT DISTINCT Chan FROM serie_cardio {where};")]
        for chan in have:
            for tok in requested:
                try:
                    if abs(float(chan) - float(tok)) < 1e-5:
                        items.append(chan)
                        break
                except (TypeError, ValueError):
                    if str(chan).strip() == tok:
                        items.append(chan)
                        break
    out, seen = [], set()
    for it in items:
        key = str(it)
        if key not in seen:
            seen.add(key)
            out.append(it)
    return out


def _special_values(path, where) -> List[str]:
    """The special values of a selection, 'all' when it has none."""
    return [r[0] for r in _query_distinct(
        [path], f"SELECT DISTINCT special FROM serie_cardio {where};")] or ['all']


def create_data_list_plot(date_start, date_end, families, runs, work_path,
                          regions, flags, stn_tokens, chan_tokens,
                          plot_type, control=None, land_oceans=('all',),
                          special_on=False
                          ) -> List[Dict[str, Any]]:
    """One task per (run, family, region, criteria, selection, channel, varno).

    With a control, each experience carries it along: the two are drawn
    on the same panels and every cycle is tested, so an improvement is
    visible where it happens instead of only in the totals.
    """
    tasks = []
    ctl_name = control[0] if control else None
    for name, _ in runs:
        if ctl_name is not None and name == ctl_name:
            continue
        for family in families:
            path = db_path(work_path, family, name, date_start, date_end)
            if not os.path.isfile(path):
                continue
            selectors = expand_station_selectors([path], stn_tokens, family,
                                                 table='serie_cardio')
            for region, land_ocean in [(r, s) for r in regions
                                       for s in land_oceans]:
                for flag in flags:
                    base = (f"WHERE region = '{region}' AND flag = '{flag}' "
                            f"AND land_ocean = '{land_ocean}'")
                    for sel, special in [
                            (s, v) for s in selectors
                            for v in (_special_values(path, base + s.sql())
                                      if special_on else ['all'])]:
                        where = (base + sel.sql()
                                 + f" AND special = '{special}'")
                        chans = _channel_items([path], where, chan_tokens)
                        varnos = [r[0] for r in _query_distinct(
                            [path], f"SELECT DISTINCT varno FROM serie_cardio "
                                    f"{where};")]
                        for chan in chans:
                            for varno in varnos:
                                task = {
                                    'pathwork': work_path,
                                    'datestart': date_start,
                                    'dateend': date_end,
                                    'experience': name, 'family': family,
                                    'region': region, 'flag_criteria': flag,
                                    'land_ocean': land_ocean,
                                    'special': special,
                                    'special_label': special_label(
                                        family, special),
                                    'selector': sel, 'id_stn': sel.display,
                                    'stn_sql': sel.sql(), 'stn_tag': sel.tag,
                                    'vcoord': chan, 'varno': varno,
                                    'plot_type': plot_type,
                                    'db_file': path,
                                    'control': None, 'db_control': None,
                                    'db_pairs': None,
                                }
                                if ctl_name is not None:
                                    ctl_db = db_path(work_path, family,
                                                     ctl_name, date_start,
                                                     date_end)
                                    if os.path.isfile(ctl_db):
                                        task['control'] = ctl_name
                                        task['db_control'] = ctl_db
                                        # the matched observations, when
                                        # the run made them; the figure
                                        # falls back on Welch without it
                                        pdb = pair_db_path(
                                            work_path, family, ctl_name,
                                            name, date_start, date_end)
                                        if os.path.isfile(pdb):
                                            task['db_pairs'] = pdb
                                tasks.append(task)
    return tasks


def _plot_task(task: Dict[str, Any]) -> Optional[str]:
    try:
        return cardio_plot(task)
    except Exception:
        print(f"[cardio] plot failed for {task['family']} "
              f"{task['experience']} {task['id_stn']}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def build_viewer_items(tasks, results) -> List[Dict[str, str]]:
    """One viewer entry per figure actually written."""
    items = []
    for task, rel in zip(tasks, results):
        if not rel:
            continue
        items.append({
            # a comparison says both runs, as in the other viewers
            'experience': (f"{task['experience']} vs {task['control']}"
                           if task.get('control') else task['experience']),
            'flag_criteria': task['flag_criteria'],
            'family': task['family'],
            'region': task['region'],
            'land_ocean': task.get('land_ocean', 'all'),
            'special': task.get('special_label', 'all'),
            'id_stn': task['id_stn'],
            'varno': str(task['varno']),
            'vcoord': _chan_text(task['vcoord']),
            'filename': os.path.basename(rel),
        })
    return items


def _chan_text(v) -> str:
    """A channel or a level as it is read: 23, not 23.0; join as it is."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    return str(int(f)) if f.is_integer() else f"{f:g}"


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def _report_timing(timing: Dict[str, Any], pathwork: str) -> None:
    sec = timing['seconds']
    print("[cardio] -------------------- run time --------------------",
          flush=True)
    print(f"[cardio] input        {_fmt_bytes(timing['input_bytes']):>10s}"
          f"   {timing['input_files']} files, {timing['cycles']} cycles, "
          f"{timing['runs']} run(s)", flush=True)
    for phase in ('extraction', 'plots'):
        if phase in sec:
            print(f"[cardio] {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(f"[cardio] total        {sec['total']:>8.1f} s   "
          f"({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
          flush=True)
    try:
        with open(os.path.join(pathwork, "cardio_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError as exc:
        print(f"[cardio] could not write cardio_timing.json: {exc}",
              file=sys.stderr, flush=True)


def _report_pairing(tasks, results, elapsed: float) -> None:
    """Say how much of each run the comparison actually covers.

    Two suites fed the same observations sit near 100 %. A low figure is
    not a failure -- it means the runs do not hold the same data, and the
    tested part of the figure is only what they share.
    """
    summary: Dict[tuple, Dict[str, int]] = {}
    failed = 0
    for t, r in zip(tasks, results):
        if r is None:
            failed += 1
            continue
        acc = summary.setdefault((t['family'], t['exp_name']), {})
        for k, v in r.items():
            acc[k] = acc.get(k, 0) + int(v or 0)
    print(f"[cardio] matching time: {elapsed:.1f}s "
          f"({len(tasks) - failed}/{len(tasks)} tasks)", flush=True)
    for (family, exp_name), acc in summary.items():
        ctl, exp = acc.get('obs_c', 0), acc.get('obs_e', 0)
        pairs = acc.get('pairs', 0)
        print(f"[cardio]   {family} {exp_name}: {pairs} common obs "
              f"({pairs / ctl * 100 if ctl else 0:.1f}% of control, "
              f"{pairs / exp * 100 if exp else 0:.1f}% of experience)",
              flush=True)
        if pairs == 0 and (ctl or exp):
            print(f"[cardio]   WARNING {family}: no common observation; the "
                  f"cycles will be tested as independent samples",
                  file=sys.stderr, flush=True)
        # the key was not unique somewhere: say so once
        from pikobs.match import DEFAULT_KEY, MatchSpec, repeat_warning
        t0 = next((t for t in tasks if t['family'] == family), {})
        spec = MatchSpec(True, tuple(t0.get('match_fields') or DEFAULT_KEY))
        ctl_name = (t0.get('names') or ('control',))[0]
        msg = repeat_warning(
            'cardio', f"{family} ({exp_name})", spec,
            {ctl_name: (acc.get('rep_keys_c', 0), acc.get('rep_rows_c', 0)),
             exp_name: (acc.get('rep_keys_e', 0), acc.get('rep_rows_e', 0))})
        if msg:
            print(msg, file=sys.stderr, flush=True)


def make_cardio(runs, pathwork, datestart, dateend, regions, families,
                flag_criterias, id_stn, channel, plot_type, n_cpu,
                varnos, svg: bool = False, control=None,
                 match: bool = True, land_ocean=('all',),
                 special_column='off') -> int:
    # MATCH: on, off, or the fields of the key -- pikobs.match decides.
    # Past this point match is True / False as before; the key travels
    # in match_spec.
    from pikobs.match import parse_match
    if match is True or match is False:
        match = 'on' if match else 'off'
    match_spec = parse_match(match)
    match = match_spec.enabled
    regions = _split_tokens(regions)
    flags = _split_tokens(flag_criterias)
    stn_tokens = parse_station_tokens(id_stn)
    chan_tokens = _split_tokens(channel) or ['join']
    land_oceans = _split_tokens(land_ocean) or ['all']
    bad = [s for s in land_oceans if s not in ('all', 'land', 'ocean')]
    if bad:
        raise ValueError(f"LAND_OCEAN takes all, land and ocean, not {bad}")
    special_on = str(special_column).strip().lower() in ('on', 'true', '1', 'yes')

    all_runs = ([control] if control else []) + list(runs)
    print(f"[cardio] runs: {', '.join(n for n, _ in all_runs)}", flush=True)
    if control is not None:
        print(f"[cardio] control: {control[0]}  |  "
              + ("matched observation by observation"
                 if match else
                 "compared, NOT matched: each run with all its "
                 "observations, Welch and F tests"), flush=True)
    if control:
        print(f"[cardio] control: {control[0]}  |  compared with: "
              f"{', '.join(n for n, _ in runs)}", flush=True)
    print(f"[cardio] regions: {regions}", flush=True)
    print(f"[cardio] flags_criteria: {flags}", flush=True)
    print(f"[cardio] land_ocean: {land_oceans}", flush=True)
    print(f"[cardio] special column: {'on' if special_on else 'off'}", flush=True)
    print(f"[cardio] id_stn tokens: {stn_tokens}", flush=True)
    print(f"[cardio] channel tokens: {chan_tokens}", flush=True)

    # a missing 6-h file is a gap in a time series, not a reason to draw
    # nothing: as in obscountdb the run goes on with the files there are,
    # and the log and the viewer say which cycles were missing
    missing_input = _missing_input(all_runs, families, datestart, dateend)
    if missing_input is None:
        print("[cardio] ERROR: not a single input file in the period, "
              "nothing was run (PATHWORK left untouched).", flush=True)
        return 1

    t_start = time.time()
    cycles = _cycles(datestart, dateend)
    n_input, input_bytes = _input_size(all_runs, families, cycles)
    timing: Dict[str, Any] = {
        'datestart': datestart, 'dateend': dateend, 'cycles': len(cycles),
        'families': list(families), 'runs': len(all_runs),
        'regions': regions,
        'flags': flags, 'id_stn': stn_tokens, 'channel': chan_tokens,
        'land_ocean': land_oceans, 'special_column': special_on,
        'n_cpus': n_cpu, 'svg': svg,
        'input_files': n_input, 'input_bytes': input_bytes,
        'seconds': {},
    }

    for family in families:
        pikobs.delete_create_folder(pathwork, family)

    tasks = create_data_list_cardio(datestart, dateend, families,
                                    all_runs, pathwork, regions,
                                    flags, varnos, land_oceans, special_on)

    parallel = n_cpu > 1
    client = None
    dask_dir = None
    if parallel:
        os.environ["DASK_LOGGING__DISTRIBUTED"] = "error"
        base = os.environ.get("TMPDIR") or None
        dask_dir = tempfile.mkdtemp(prefix="pikobs_cardio_dask_", dir=base)
        os.environ["DASK_TEMPORARY_DIRECTORY"] = dask_dir
        os.environ["SQLITE_TMPDIR"] = dask_dir
        dask.config.set({"temporary-directory": dask_dir,
                         "logging.distributed": "error"})
        client = Client(processes=True, threads_per_worker=1, n_workers=n_cpu,
                        silence_logs=50, dashboard_address=None)
    plot_tasks: List[Dict[str, Any]] = []
    results: List[Any] = []
    try:
        t0 = time.time()
        print(f"[cardio] extraction: {len(tasks)} tasks, {n_cpu} worker(s)",
              flush=True)
        res = run_tasks(_extract_task, [(t,) for t in tasks], client,
                        label='extraction')
        timing['seconds']['extraction'] = time.time() - t0
        print(f"[cardio] extraction time: "
              f"{timing['seconds']['extraction']:.1f}s "
              f"({sum(r is not None for r in res)}/{len(tasks)} files)",
              flush=True)

        # The pairs, when there is a control: the same observations in
        # both runs, so each cycle can be tested the way scatter tests a
        # box. Without a control there is nothing to pair.
        # matching is the normal mode; MATCH=off skips it and the
        # figures fall back on the independent tests
        if control is not None and match:
            pair_tasks = create_pairs_list(datestart, dateend, families,
                                           control, runs, pathwork, regions,
                                           flags, varnos, land_oceans,
                                           special_on)
            t0 = time.time()
            for t in pair_tasks:
                t['match_fields'] = match_spec.fields
                t['names'] = (control[0], t['exp_name'])
            print(f"[cardio] matching control and experience: "
                  f"{len(pair_tasks)} tasks", flush=True)
            pair_res = run_tasks(_pairs_task, [(t,) for t in pair_tasks],
                                 client, label='matching')
            timing['seconds']['matching'] = time.time() - t0
            _report_pairing(pair_tasks, pair_res,
                            timing['seconds']['matching'])

        dbs = sorted({t['db_new'] for t in tasks})
        run_tasks(_index_task, [(d,) for d in dbs], client, label='indexing')

        plot_tasks = create_data_list_plot(datestart, dateend, families,
                                           all_runs, pathwork, regions, flags,
                                           stn_tokens, chan_tokens, plot_type,
                                           control, land_oceans, special_on)
        for t in plot_tasks:
            t['svg'] = svg
        if not plot_tasks:
            print("[cardio] WARNING: nothing to plot, check the selectors.",
                  file=sys.stderr, flush=True)
            return 1
        t0 = time.time()
        print(f"[cardio] plots: {len(plot_tasks)} tasks", flush=True)
        results = run_tasks(_plot_task, [(t,) for t in plot_tasks], client,
                            label='plots')
        timing['seconds']['plots'] = time.time() - t0
        print(f"[cardio] plot time: {timing['seconds']['plots']:.1f}s "
              f"({sum(r is not None for r in results)}/{len(plot_tasks)} "
              f"plots)", flush=True)
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

    items = build_viewer_items(plot_tasks, results)
    if not items:
        print("[cardio] ERROR: no figure was produced, viewer not written.",
              file=sys.stderr, flush=True)
        return 1
    keys = ["experience", "flag_criteria", "family", "region", "land_ocean",
            "id_stn", "special",
            "varno", "vcoord"]
    print(f"[cardio] viewer selectors: {keys}", flush=True)
    from pikobs.zone.zone_plot import level_selector_label
    generate_web(
        items, keys,
        os.path.join(pathwork, "pikobs_cardio_viewer.html"),
        title=("Pikobs Cardio Viewer"
               + (f"   \u26a0 input incomplete: "
                  f"{sum(len(v) for v in missing_input.values())} file(s) "
                  f"missing, see About" if missing_input else "")),
        subtitle=(_missing_note(missing_input, len(_cycles(datestart, dateend)))
                  + "How did the departures move, cycle after cycle? One figure "
                  "per selection, the cycles across: the bias and the sigma of "
                  "O-P (solid) and O-A (dashed), the values, the number of "
                  "observations and the extremes of each cycle. <b>Red is the "
                  "experience, blue the control.</b> With a control, a circle "
                  "marks a cycle where the change passes the test: red where "
                  "Exp is better, blue where Ctl is."
                  + runs_block(all_runs, control, (datestart, dateend))),
        image_subdir_key="family",
        key_labels={"flag_criteria": "Criteria",
                    "vcoord": level_selector_label(families),
                    "land_ocean": "Surface",
                    "special": special_key_label(families),
                    "experience": "Experience"},
        issues_url="https://gitlab.science.gc.ca/dlo001/Pikobs",
        enable_play=False,
    )

    timing['seconds']['total'] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"[cardio] done -- output in: {pathwork}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def arg_call() -> None:
    import argparse

    p = argparse.ArgumentParser(
        prog="pikobs-cardio",
        description="Cardiogram time series of one or more experiences.")
    p.add_argument('--path_control_files', default=None,
                   help="Directory of the control run; with one, every "
                        "experience is drawn against it and each cycle is "
                        "tested.")
    p.add_argument('--control_name', default=None)
    p.add_argument('--path_experience_files', nargs='+', default=[])
    p.add_argument('--experience_name', nargs='+', default=[])
    p.add_argument('--pathwork', default=None)
    p.add_argument('--datestart', default=None)
    p.add_argument('--dateend', default=None)
    p.add_argument('--region', nargs='+', default=['Monde'])
    p.add_argument('--family', nargs='+', default=[])
    p.add_argument('--flags_criteria', nargs='+', default=['all'])
    p.add_argument('--land_ocean', nargs='+', default=['all'],
                   choices=['all', 'land', 'ocean'],
                   help="all (no filter), land, ocean: one series of figures "
                        "each; land and ocean read the land mask.")
    p.add_argument('--special_column', default='off', choices=['on', 'off'],
                   help="on: one series of figures per value of the family's "
                        "special column (the method of sw, the elevation of "
                        "the radar); off: all together (default).")
    p.add_argument('--id_stn', nargs='+', default=['join'],
                   help="Tokens, one series of figures each: join, all, "
                        "PREFIX, LIKE%%pattern, =EXACT, 'NAME (codtyp)'.")
    p.add_argument('--channel', '--vcoord', dest='channel', nargs='+',
                   default=['join'],
                   help="join (all channels merged), all (one each), or an "
                        "explicit list.")
    p.add_argument('--plot_type', default='wide', choices=['wide', 'narrow'])
    p.add_argument('--varnos', nargs='*', default=[])
    p.add_argument('--match', nargs='+', default=['on'],
                     help="on: with a control, the same observations in both "
                         "runs, paired tests. off: each run with all its "
                         "observations and its own flags, Welch and F tests.")
    p.add_argument('--svg', default='off', choices=['on', 'off'],
                   help="Also write each figure as SVG, next to the PNG, for "
                        "editing before a presentation (default off).")
    p.add_argument('--n_cpus', '--n_cpu', default=1, type=int, dest='n_cpus')
    p.add_argument('--no_submit', action='store_true')

    args = p.parse_args()
    for arg in vars(args):
        print(f'--{arg} {getattr(args, arg)}', flush=True)

    paths = _split_tokens(args.path_experience_files)
    names = _split_tokens(args.experience_name)
    if not paths or not names or len(paths) != len(names):
        raise ValueError("--path_experience_files and --experience_name must "
                         "have the same number of entries")
    if len(set(names)) != len(names):
        raise ValueError(f"experience names must be unique: {names}")
    for attr, flag in [('pathwork', '--pathwork'),
                       ('datestart', '--datestart'),
                       ('dateend', '--dateend'), ('family', '--family')]:
        if getattr(args, attr) in (None, [], 'undefined', ''):
            raise ValueError(f"{flag} is required")

    runs = [(n, p_.rstrip('/') or '/') for n, p_ in zip(names, paths)]

    control = None
    # a blank value ("" or " ") is no control: an empty variable in
    # the wrapper must not turn into a directory called ' '
    if args.path_control_files and args.path_control_files.strip():
        ctl_name = args.control_name or 'control'
        if ctl_name in names:
            raise ValueError(f"the control and an experience share the name "
                             f"'{ctl_name}'; they would write the same "
                             f"database")
        control = (ctl_name,
                   args.path_control_files.strip().rstrip('/') or '/')
    elif args.control_name and args.control_name.strip():
        # a name with no path is left over from a wrapper whose control was
        # emptied: no reason to stop the run for it
        print(f"[{'zone' if 'zone' in __name__ else 'cardio'}] note: "
              f"--control_name '{args.control_name}' ignored, there is no "
              f"--path_control_files", flush=True)

    maybe_submit_to_pbs(args)
    sys.exit(make_cardio(runs, args.pathwork, args.datestart, args.dateend,
                         args.region, _split_tokens(args.family),
                         args.flags_criteria, args.id_stn, args.channel,
                         args.plot_type, args.n_cpus,
                         _split_tokens(args.varnos), svg_enabled(args.svg),
                         control,
                 match=args.match, land_ocean=args.land_ocean,
                 special_column=args.special_column))


if __name__ == '__main__':
    arg_call()
