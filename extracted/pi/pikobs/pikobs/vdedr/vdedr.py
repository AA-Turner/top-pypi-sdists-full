#!/usr/bin/python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_vdedr.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""===========================================
pikobs.vdedr -- Radiance Verification
===========================================

``vdedr`` answers the question that comes with every bias-correction or
radiative-transfer change: channel by channel, did the experience move the
departures, and can I trust what I am seeing? It compares a control with
one or several experiences and draws three figures per selection, with the
channels on the y axis so that a satellite can be read top to bottom.

The channel axis is the point of this module, so it never squeezes:
whether a family has four channels or thirteen hundred, every channel keeps
its own row and its own label, and the figure grows as tall as it needs.

Quick start
===========

.. code-block:: bash

   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_vdedr_cont_exp.sh
   chmod +x run_vdedr_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open a
compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_vdedr_cont_exp.sh
   ./run_vdedr_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(iasi cris)`` and
   ``REGION=(Monde Canada)``, not strings.

A run prints its phases and ends with the address of the viewer:

.. code-block:: text

   [vdedr] runs: control, exp1, exp2
   [vdedr] comparisons: control vs exp1, control vs exp2
   [vdedr] id_stn tokens: ['all']
   [vdedr] input check OK: 21 cycles x 3 run(s) x 2 family(ies), 126 files, 38.4 GB
   [vdedr] extraction: 126 tasks, 80 worker(s)
   [pikobs] extraction: 126/126 (100%) 96s elapsed
   [vdedr] plots: 48 tasks (144 figures)
   [vdedr] -------------------- run time --------------------
   [vdedr] input           38.4 GB   126 files, 21 cycles, 3 run(s)
   [vdedr] extraction       96.3 s
   [vdedr] compaction        4.1 s
   [vdedr] plots            71.5 s
   [vdedr] total           173.8 s   (2.9 min, 80 workers)
   Viewer: /home/dlo001/sites8/pikobs_vdedr_cont_exp/pikobs_vdedr_viewer.html
   Web:    to open it in a browser, link the folder under public_html once:
             ln -s /home/dlo001/sites8/pikobs_vdedr_cont_exp /home/dlo001/public_html/
           then: https://goc-dx-u3.science.gc.ca/~dlo001/pikobs_vdedr_cont_exp/pikobs_vdedr_viewer.html

One live instance: an experiment of the summer of 2025 against its
control, over two weeks of June. vdedr always compares, so there is no
single run to show:

:live:`the live comparison <pikobs_doc_vdedr/pikobs_vdedr_viewer.html>`

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of the control, of each experience and of
each family is looked up first. If one is missing the run stops, says which
cycles are missing and which dates the directory does hold, and leaves
``PATHWORK`` untouched.

**Extraction.** Each file is read once, grouped by station, varno and
channel. Every (region, criteria) pair carries its own conditional
aggregates in that single scan, so five regions and two criteria cost
almost the same as one of each. What is stored are the sums:

.. math::

   N,\quad \sum x,\quad \sum x^2 \quad\text{for O-B and O-A},
   \qquad
   N_{b},\quad \sum b \quad\text{for the bias correction}

Means and sigmas are derived when the figures are drawn:

.. math::

   \bar{x} = \frac{\sum x}{N},
   \qquad
   \sigma = \sqrt{\max\left(0,\ \frac{\sum x^2}{N} - \bar{x}^2\right)}

Keeping sums instead of means is what lets a figure pool several platforms
exactly, and it is also why this module no longer needs the SQLite
``STDDEV`` extension.

**Compaction.** The per-cycle rows are summed over the period and indexed
before plotting, so each figure reads a small table.

**Figures.** One task per (comparison, family, region, criteria, station
selection, varno); each task writes the three figures of that selection.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of the wrapper is meant to be edited.

.. wrapper-settings:: run_vdedr_cont_exp.sh

With several experiences, the arrays keep the same length:

.. code-block:: bash

   PATH_EXPERIENCE_FILES=(/path/to/E22 /path/to/E23)
   EXPERIENCE_NAME=(E22 E23)

which gives *control vs E22* and *control vs E23*, selectable in the viewer.

----

3. Choosing the platforms
=========================

Every token, with examples for each family (radiances, aircraft,
radiosondes, surface), is on :doc:`stations`. In short:

``ID_STN`` takes the tokens of the rest of Pikobs, and each one is its own
series of figures:

+---------------------------+--------------------------------------------------+
| Token                     | Figures produced                                 |
+===========================+==================================================+
| ``join``                  | one figure, every platform pooled                |
+---------------------------+--------------------------------------------------+
| ``all``                   | one figure per platform                          |
+---------------------------+--------------------------------------------------+
| ``METOP`` or ``"METOP*"`` | the platforms whose id starts with METOP, pooled |
+---------------------------+--------------------------------------------------+
| ``=NOAA-20``              | that platform only                               |
+---------------------------+--------------------------------------------------+
| ``N%``                    | SQL ``LIKE`` pattern on the platform id          |
+---------------------------+--------------------------------------------------+

``join`` pools the platforms by adding their moments, which is exact
because the sums are what is stored. The file names carry the selection:
``join``, ``METOP_grp`` for a prefix, ``NOAA-20_eq`` for an exact id.

----

4. Reading the figures
======================

+--------------+----------------------------------------+-----------------------------------+-----------------------------+
| Figure       | Left series                            | Right series                      | Test                        |
+==============+========================================+===================================+=============================+
| ``omp_bias`` | residual bias, ``mean(O-B)`` exp - ctl | raw bias, bias correction removed | none                        |
+--------------+----------------------------------------+-----------------------------------+-----------------------------+
| ``omp_rel``  | ``100 (σ_exp - σ_ctl) / σ_ctl`` of O-B | ``100 (N_exp - N_ctl) / N_ctl``   | sigma test: see MATCH below |
+--------------+----------------------------------------+-----------------------------------+-----------------------------+
| ``oma_rel``  | the same for O-A                       | the same count change             | sigma test: see MATCH below |
+--------------+----------------------------------------+-----------------------------------+-----------------------------+

Everything is experience minus control. For the sigma the sign says who
wins, and the colours say it too:

+--------------+--------------------------------------------------------------+
| Mark         | Meaning                                                      |
+==============+==============================================================+
| red dot      | ``% sigma`` below zero: the experience reduces the sigma     |
+--------------+--------------------------------------------------------------+
| blue dot     | ``% sigma`` above zero: the control is the better one        |
+--------------+--------------------------------------------------------------+
| green line   | ``% Nobs``: more or fewer observations, neither good nor bad |
+--------------+--------------------------------------------------------------+
| red square   | sigma test above 95 %, and the experience wins               |
+--------------+--------------------------------------------------------------+
| blue square  | sigma test above 95 %, and the control wins                  |
+--------------+--------------------------------------------------------------+
| empty square | sigma test at or below 95 %: the change can be noise         |
+--------------+--------------------------------------------------------------+

.. image:: _static/vdedr_omp_rel.png
   :alt: Sigma change per channel, with the sigma-test column
   :align: center
   :width: 100%

The columns on the right of each figure hold, in order: the test of each
channel -- a filled circle where it passes, red when the experience wins
and blue when the control does, a grey dash with its number of cycles
where there are too few to test -- and the number of observations, one
column per run, or a single ``N pairs`` with ``MATCH=on``. Above them, the
count of channels each run wins, for example ``Exp better 25 · Ctl better 0``.

With many channels (IASI, CrIS) a row would be too thin for its text, so
the figure stops growing: the axis names one channel in a few, the tests
become thin lines, and the counts move to the mouse -- in the viewer,
pointing at a row shows its channel, its counts and its test.
With ``MATCH=on`` the second curve of the sigma figures is the share of
each run's observations that is matched, instead of the change of their
number.

The bias figure keeps its two series, residual and raw. There the sign does
not tell who wins, since a difference of means can move towards or away
from zero depending on where each run started, so the marks keep their own
colour:

.. image:: _static/vdedr_omp_bias.png
   :alt: Residual and raw bias per channel
   :align: center
   :width: 100%

The tests
---------


Which observations, and which test: MATCH
-----------------------------------------

Two runs rarely keep the same observations, so ``MATCH`` decides what a
comparison is made of.

.. list-table::
   :header-rows: 1
   :widths: 10 35 35 20

   * - ``MATCH``
     - Observations
     - Test of each channel
     - On the figure
   * - ``on``
     - those both runs hold, paired one by one
     - a cycle block bootstrap: the change of every cycle, then whether their mean is more than the cycles' own scatter. It needs 20 cycles; with fewer, the cell is drawn grey with its number of cycles, not tested
     - green **MATCH ON**
   * - ``off``
     - every observation of each run
     - the t-test on the bias, the F-test on the sigma
     - orange **MATCH OFF**
   * - ``no``
     - every observation of each run
     - none
     - no badge, no test

**How a pair is found.** An observation is known by where and when it was
taken: station, date, time, latitude, longitude, ``varno`` and level. No
two observations of one run share all seven, so the same seven in the
control and in the experience are one observation, seen by both runs.
With ``on`` it is compared only when it passes the flags of the figure in
both runs:

.. list-table::
   :header-rows: 1
   :widths: 12 12 22 12 12 12 18

   * - station
     - time
     - lat, lon
     - level
     - Ctl O-P
     - Exp O-P
     - with ``on``
   * - 71119
     - 00 UTC
     - 53.55, -114.10
     - 500 hPa
     - 0.8
     - 0.5
     - a pair
   * - 71119
     - 00 UTC
     - 53.55, -114.10
     - 850 hPa
     - -0.2
     - rejected
     - left out
   * - 72201
     - 00 UTC
     - 24.55, -81.75
     - 500 hPa
     - --
     - 1.1
     - left out: Exp only

The rare report that a run holds twice is paired one to one, by value,
and counted in the log.

Start with ``on``: the change then comes from the experience, not from a
different sample. ``off`` is for an experience that changes which
observations go in (a new instrument, another quality control). Ask for
several, ``MATCH="on off no"``, and the viewer's **Match** selector flips
between them; the files of ``off`` and ``no`` end in ``_matchoff`` and
``_matchno``. The tests are explained in :doc:`stats`.


----

5. The viewer
=============

``pikobs_vdedr_viewer.html`` has seven dropdowns: Comparison, Metric,
Family, Region, Criteria, Station and Varno. Each one only offers what
exists for the choices on its left. **Flip** (key ``F``) swaps between the
current figure and the previous one, which is the quickest way to compare
two experiences on the same channel set, and a click opens the figure at
full size, which is how a 1300-channel figure is read.

----

6. Output layout
================

::

   $PATHWORK/
   ├── pikobs_vdedr_viewer.html
   ├── vdedr_timing.json
   └── <family>/
       ├── vdedr_<run>_<start>_<end>_<family>.db
       └── <metric>_<family>_<stn>_<ctl>-<exp>_<region>[_<surface>][_<special>]_<flag>_varno<varno>.png

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else. An SVG keeps every element of the
figure, so ask for it on the one or two figures you actually need.

The ``.db`` files hold one row per (region, criteria, station, varno,
channel) in the table ``serie_vdedr`` and can be queried with ``sqlite3``.

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
import time
import traceback
import warnings
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

warnings.filterwarnings("ignore", ".*ShapelyDeprecationWarning.*")


# a region is a box or a polygon; the module does not need to know
from pikobs.configobs import regionsobs
from pikobs.configobs.landmask import register_surface, surface_sql
from pikobs.configobs.special_family import special_key_label, special_label, special_select
from pikobs.web.runs import runs_block
import pikobs
from pikobs.figures import svg_enabled
from pikobs.obsdb import check_input_files, combine as _combine_rows, open_result, work_db
from pikobs.obsdb.obsdb import (
    split_tokens as _split_tokens,
    cycles as _cycles,
    input_size as _input_size,
)  # shared, once
from pikobs.parallel import run_tasks
from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.stations.stations import expand_station_selectors, parse_station_tokens
from pikobs.vdedr.vdedr_plot import vdedr_plot_task, vdedr_viewer_items, METRICS
from pikobs.obsdb import fmt_bytes as _fmt_bytes
from pikobs.parallel import start_workers, stop_workers
from pikobs.obsdb import run_db_path
from pikobs.obsdb import pair_db_path as _pair_db_path
from pikobs.obsdb import query_distinct

CYCLE_HOURS = 6

# One row per (region, flag, station, varno, channel, cycle). Sums are kept
# instead of mean / std so that any later grouping recombines exactly, and
# so that no SQLite extension is needed for STDDEV.
_SERIE_COLS = (
    "region, flag, land_ocean, special, id_stn, CODTYP, varno, "
    "vcoord, date, Ntot, "
    "s_omp, s2_omp, s_oma, s2_oma, n_bcorr, s_bcorr"
)

# The pairs: the same keys as serie_vdedr, and per quantity the sums of
# the observations the two runs share. One row per channel and cycle, so
# a period recombines by adding, exactly as the moments do.
_PAIR_COLS = (
    "region, flag, land_ocean, special, id_stn, CODTYP, varno, "
    "vcoord, date, "
    "n_omp, sx_omp, sy_omp, sxx_omp, syy_omp, sxy_omp, "
    "n_oma, sx_oma, sy_oma, sxx_oma, syy_oma, sxy_oma, "
    "nx_bcorr, sx_bcorr, ny_bcorr, sy_bcorr"
)
# x the control, y the experience: with MATCH on the raw bias is drawn from
# the pairs too, so each side's bias correction is summed on them
_PAIR_SUMS_PER_COMBO = 16

_DDL_PAIRS = """
    CREATE TABLE IF NOT EXISTS pairs_vdedr (
        region TEXT, flag TEXT, land_ocean TEXT, special TEXT,
        id_stn TEXT, CODTYP INTEGER,
        varno INTEGER, vcoord FLOAT, date INTEGER,
        n_omp INTEGER, sx_omp FLOAT, sy_omp FLOAT,
        sxx_omp FLOAT, syy_omp FLOAT, sxy_omp FLOAT,
        n_oma INTEGER, sx_oma FLOAT, sy_oma FLOAT,
        sxx_oma FLOAT, syy_oma FLOAT, sxy_oma FLOAT,
        nx_bcorr INTEGER, sx_bcorr FLOAT, ny_bcorr INTEGER, sy_bcorr FLOAT
    );
"""


_DDL_SERIE = """
    CREATE TABLE IF NOT EXISTS serie_vdedr (
        region  TEXT,
        flag    TEXT,
        land_ocean TEXT,
        special TEXT,
        id_stn  TEXT,
        CODTYP  INTEGER,
        varno   INTEGER,
        vcoord  FLOAT,
        date    INTEGER,
        Ntot    NUMERIC,
        s_omp   FLOAT, s2_omp FLOAT,
        s_oma   FLOAT, s2_oma FLOAT,
        n_bcorr NUMERIC, s_bcorr FLOAT
    );
"""


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def db_path(work_path, family, name, date_start, date_end) -> str:
    return run_db_path("vdedr", work_path, family, name, date_start, date_end)


@dataclass(frozen=True)
class Comparison:
    """One entry of the viewer 'comparison' selector."""

    key: str
    control: str
    experience: str

    @property
    def label(self) -> str:
        return f"{self.control} vs {self.experience}"


def build_comparisons(
    control: Tuple[str, str], experiments: Sequence[Tuple[str, str]]
) -> List[Comparison]:
    return [Comparison(f"{control[0]}_vs_{name}", control[0], name) for name, _ in experiments]


# ─────────────────────────────────────────────────────────────────────────────
# Input check
# ─────────────────────────────────────────────────────────────────────────────


def create_table_if_not_exists(cursor) -> None:
    cursor.execute(_DDL_SERIE)


def _combinations(regions, flags, land_oceans=("all",)) -> List[Dict[str, str]]:
    """Every (region, surface, criteria), all read in the same pass."""
    combos = []
    for region in regions:
        latlon = regionsobs.criteria(region)
        for land_ocean in land_oceans or ("all",):
            surf = surface_sql(land_ocean)
            for flag in flags:
                flag_sql = pikobs.flag_criteria(flag)
                combos.append(
                    {
                        "region": region,
                        "flag": flag,
                        "land_ocean": land_ocean,
                        "cond": f"((1=1 {latlon}) AND (1=1 {flag_sql}){surf})",
                    }
                )
    return combos


def create_serie_vdedr(
    family: str,
    new_db_filename: str,
    existing_db_filename: str,
    regions: Sequence[str],
    flags: Sequence[str],
    varnos: Sequence[str] = (),
    land_oceans: Sequence[str] = ("all",),
    pathwork: str = ".",
    special_on: bool = False,
) -> Optional[int]:
    """Read one RDB file once and store the per-channel moments.

    Grouped by station, varno and channel; every (region, criteria) pair is
    a set of conditional aggregates, so the file is scanned a single time.
    """
    if not os.path.isfile(existing_db_filename):
        print(
            f"[vdedr] missing file, skipped: {existing_db_filename}", file=sys.stderr, flush=True
        )
        return None
    date_match = re.search(r"(\d{10})", os.path.basename(existing_db_filename))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {existing_db_filename}")
    date_int = int(date_match.group(1))

    combos = _combinations(regions, flags, land_oceans)
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if varnos:
        element = ",".join(str(v) for v in varnos)

    with work_db(attach={"db": existing_db_filename}) as (conn, mem_uri):
        register_surface(conn, land_oceans, pathwork)

        data_cols = [r[1].lower() for r in conn.execute("PRAGMA db.table_info('DATA');")]
        if not data_cols:
            print(f"[vdedr] no DATA table in {existing_db_filename}", file=sys.stderr, flush=True)
            return None
        has_bc = "bias_corr" in data_cols

        head_cols = [r[1].lower() for r in conn.execute("PRAGMA db.table_info('HEADER');")]
        cod = "codtyp" if "codtyp" in head_cols else "NULL"
        sp_sel, _ = special_select(family, head_cols, special_on)
        selects = [
            "id_stn AS stn",
            f"{cod} AS cod",
            "varno AS varno",
            f"{VCOORD} AS vcoord",
            f"{sp_sel} AS special",
        ]
        for i, c in enumerate(combos):
            cond = c["cond"]
            ok_omp = f"{cond} AND omp IS NOT NULL"
            ok_oma = f"{cond} AND oma IS NOT NULL"
            selects += [
                f"SUM(CASE WHEN {cond} THEN 1 ELSE 0 END) AS c{i}_n",
                f"SUM(CASE WHEN {ok_omp} THEN omp END) AS c{i}_somp",
                f"SUM(CASE WHEN {ok_omp} THEN omp*omp END) AS c{i}_qomp",
                f"SUM(CASE WHEN {ok_oma} THEN oma END) AS c{i}_soma",
                f"SUM(CASE WHEN {ok_oma} THEN oma*oma END) AS c{i}_qoma",
            ]
            if has_bc:
                ok_bc = f"{cond} AND bias_corr IS NOT NULL"
                selects += [
                    f"SUM(CASE WHEN {ok_bc} THEN 1 ELSE 0 END) AS c{i}_nbc",
                    f"SUM(CASE WHEN {ok_bc} THEN bias_corr END) AS c{i}_sbc",
                ]
            else:
                selects += [f"NULL AS c{i}_nbc", f"NULL AS c{i}_sbc"]

        rows = conn.execute(f"""
            SELECT {", ".join(selects)}
            FROM db.header NATURAL JOIN db.data
            WHERE varno IN ({element})
              AND obsvalue IS NOT NULL
              {VCOCRIT}
            GROUP BY id_stn, {cod}, varno, {VCOORD}, special;
        """).fetchall()

        per_combo = 7
        out_rows = []
        for row in rows:
            stn, codtyp, varno, vcoord = row[0], row[1], row[2], row[3]
            special = row[4]
            for i, c in enumerate(combos):
                base = 5 + i * per_combo
                n = row[base]
                if not n:
                    continue
                out_rows.append(
                    (
                        c["region"],
                        c["flag"],
                        c["land_ocean"],
                        special,
                        stn,
                        codtyp,
                        varno,
                        vcoord,
                        date_int,
                        n,
                        *row[base + 1 : base + per_combo],
                    )
                )

        create_table_if_not_exists(conn)
        conn.executemany(
            f"INSERT INTO serie_vdedr ({_SERIE_COLS}) " f"VALUES ({', '.join('?' * 16)});",
            out_rows,
        )
        _combine_rows(
            new_db_filename, mem_uri, "serie_vdedr", _SERIE_COLS, ddl=_DDL_SERIE, module="vdedr"
        )
        return len(out_rows)


def create_pairs_vdedr(
    family: str,
    pair_db: str,
    ctl_file: str,
    exp_file: str,
    regions: Sequence[str],
    flags: Sequence[str],
    varnos: Sequence[str] = (),
    match_fields: Sequence[str] = (),
    names=None,
    land_oceans: Sequence[str] = ("all",),
    pathwork: str = ".",
    special_on: bool = False,
) -> Optional[Dict[str, int]]:
    """Match the two runs channel by channel, one cycle at a time.

    vdedr used to test its channels with Welch, for want of anything to
    match: only moments per channel survived the extraction. This pass
    keeps, per channel and cycle, the sums of the observations both runs
    hold, which is what the paired test needs.

    It matters most here. Two suites differing in one detail agree on
    nearly every radiance, so the difference that matters is small
    against a sigma of a few kelvin -- and that is exactly the case a
    paired test sees and an independent one cannot.

    A pair exists only where the observation passes the criteria in both
    runs; each run's flags are read on its own data. The key and what
    happens when it repeats are pikobs.match's: a repeated key is paired
    one to one by value and counted, never dropped.
    """
    for f in (ctl_file, exp_file):
        if not os.path.isfile(f):
            print(f"[vdedr] missing file, pairs skipped: {f}", file=sys.stderr, flush=True)
            return None
    date_match = re.search(r"(\d{10})", os.path.basename(ctl_file))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {ctl_file}")
    date_int = int(date_match.group(1))

    combos = _combinations(regions, flags, land_oceans)
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if varnos:
        element = ",".join(str(v) for v in varnos)

    from pikobs.match import (
        DEFAULT_KEY,
        MatchSpec,
        count_repeats,
        key_aliases,
        key_join,
        key_select,
    )

    spec = MatchSpec(True, tuple(match_fields) or DEFAULT_KEY)
    ksel = key_select(spec)
    join_on = key_join(spec)

    with work_db(attach={"c": ctl_file, "e": exp_file}) as (conn, mem_uri):
        regionsobs.register_pending(conn)
        register_surface(conn, land_oceans, pathwork)

        def cols(schema, table):
            return [r[1].lower() for r in conn.execute(f"PRAGMA {schema}.table_info('{table}');")]

        if not all(cols(sc, t) for sc in ("c", "e") for t in ("HEADER", "DATA")):
            return None
        cod = "codtyp" if "codtyp" in cols("c", "HEADER") else "NULL"
        sp_sel, _ = special_select(family, cols("c", "HEADER"), special_on)

        counts: Dict[str, int] = {}
        for schema in ("c", "e"):
            # the bias correction of each run, where its file has one
            bc = "bias_corr" if "bias_corr" in cols(schema, "DATA") else "NULL"
            conn.execute(f"""
            CREATE TABLE raw_{schema} AS
            SELECT {ksel},
                   id_stn AS stn, {cod} AS cod, varno AS varno,
                   {VCOORD} AS vcoord, {sp_sel} AS special,
                   lat AS lat, lon AS lon,
                   flag AS flag, omp AS omp, oma AS oma, {bc} AS bc
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
            counts[f"obs_{schema}"] = conn.execute(
                f"SELECT COUNT(*) FROM raw_{schema};"
            ).fetchone()[0]
            counts[f"rep_keys_{schema}"] = n_keys
            counts[f"rep_rows_{schema}"] = n_rows
            conn.execute(f"ALTER TABLE raw_{schema} RENAME TO key_{schema};")
            conn.execute(f"CREATE INDEX idx_{schema} ON key_{schema} ({key});")

        selects = [
            "c.stn AS stn",
            "c.cod AS cod",
            "c.varno AS varno",
            "c.vcoord AS vcoord",
            "c.special AS special",
        ]
        for i, combo in enumerate(combos):
            cond = combo["cond"].replace("lat", "c.lat").replace("lon", "c.lon")
            both = (
                f"(({cond.replace('flag', 'c.flag')}) AND " f"({cond.replace('flag', 'e.flag')}))"
            )
            for tag in ("omp", "oma"):
                ok = f"{both} AND c.{tag} IS NOT NULL " f"AND e.{tag} IS NOT NULL"
                selects += [
                    f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END) AS c{i}_n{tag}",
                    f"SUM(CASE WHEN {ok} THEN c.{tag} END) AS c{i}_sx{tag}",
                    f"SUM(CASE WHEN {ok} THEN e.{tag} END) AS c{i}_sy{tag}",
                    f"SUM(CASE WHEN {ok} THEN c.{tag}*c.{tag} END) " f"AS c{i}_sxx{tag}",
                    f"SUM(CASE WHEN {ok} THEN e.{tag}*e.{tag} END) " f"AS c{i}_syy{tag}",
                    f"SUM(CASE WHEN {ok} THEN c.{tag}*e.{tag} END) " f"AS c{i}_sxy{tag}",
                ]
            # each side's bias correction, on the pairs of the O-P sums
            ok = f"{both} AND c.omp IS NOT NULL AND e.omp IS NOT NULL"
            selects += [
                f"SUM(CASE WHEN {ok} AND c.bc IS NOT NULL THEN 1 ELSE 0 END) AS c{i}_nxbc",
                f"SUM(CASE WHEN {ok} AND c.bc IS NOT NULL THEN c.bc END) AS c{i}_sxbc",
                f"SUM(CASE WHEN {ok} AND e.bc IS NOT NULL THEN 1 ELSE 0 END) AS c{i}_nybc",
                f"SUM(CASE WHEN {ok} AND e.bc IS NOT NULL THEN e.bc END) AS c{i}_sybc",
            ]

        # how many observations the two runs actually share, counted on
        # the join itself. Counting them per selection instead would add
        # up the regions, and the regions overlap -- the tropics sit
        # inside both hemispheres -- so the total came out larger than
        # the number of observations, which is nonsense on its face.
        counts["pairs"] = conn.execute(f"""SELECT COUNT(*) FROM key_c AS c
                JOIN key_e AS e ON {join_on};""").fetchone()[0]

        rows = conn.execute(f"""
            SELECT {', '.join(selects)}
            FROM key_c AS c JOIN key_e AS e ON {join_on}
            GROUP BY c.stn, c.cod, c.varno, c.vcoord, c.special;
        """).fetchall()

        out_rows = []
        per_combo = _PAIR_SUMS_PER_COMBO
        for row in rows:
            stn, cod_v, varno_v, vcoord = row[0], row[1], row[2], row[3]
            special = row[4]
            for i, combo in enumerate(combos):
                base = 5 + i * per_combo
                block = row[base : base + per_combo]
                if not (block[0] or block[6]):
                    continue
                out_rows.append(
                    (
                        combo["region"],
                        combo["flag"],
                        combo["land_ocean"],
                        special,
                        stn,
                        cod_v,
                        varno_v,
                        vcoord,
                        date_int,
                    )
                    + tuple(block)
                )

        if out_rows:
            conn.execute(_DDL_PAIRS)
            conn.executemany(
                f"INSERT INTO pairs_vdedr ({_PAIR_COLS}) "
                f"VALUES ({', '.join('?' * (9 + _PAIR_SUMS_PER_COMBO))});",
                out_rows,
            )
        for t in ("key_c", "key_e"):
            conn.execute(f"DROP TABLE {t};")
        conn.execute("DETACH DATABASE c;")
        conn.execute("DETACH DATABASE e;")
        if out_rows:
            _combine_rows(
                pair_db, mem_uri, "pairs_vdedr", _PAIR_COLS, ddl=_DDL_PAIRS, module="vdedr"
            )
        return counts


def _pairs_task(task: Dict[str, Any]) -> Optional[Dict[str, int]]:
    try:
        return create_pairs_vdedr(
            task["family"],
            task["pair_db"],
            task["ctl_file"],
            task["exp_file"],
            task["regions"],
            task["flags"],
            task["varnos"],
            task.get("match_fields") or (),
            task.get("names"),
            task.get("land_oceans") or ("all",),
            task.get("pathwork") or ".",
            bool(task.get("special_on")),
        )
    except Exception:
        print(
            f"[vdedr] pairing failed for {task['exp_file']}:\n" f"{traceback.format_exc()}",
            file=sys.stderr,
            flush=True,
        )
        return None


def _extract_task(task: Dict[str, Any]) -> Optional[int]:
    try:
        return create_serie_vdedr(
            task["family"],
            task["db_new"],
            task["filein"],
            task["regions"],
            task["flags"],
            task["varnos"],
            task.get("land_oceans") or ("all",),
            task.get("pathwork") or ".",
            bool(task.get("special_on")),
        )
    except Exception:
        print(
            f"[vdedr] extraction failed for {task['filein']}:\n" f"{traceback.format_exc()}",
            file=sys.stderr,
            flush=True,
        )
        return None


def create_data_list(
    date_start,
    date_end,
    families,
    runs,
    work_path,
    regions,
    flags,
    varnos,
    land_oceans=("all",),
    special_on=False,
) -> List[Dict[str, Any]]:
    """One task per (cycle, family, run): every region and criteria at once."""
    tasks = []
    for cycle in _cycles(date_start, date_end):
        for family in families:
            for name, path in runs:
                tasks.append(
                    {
                        "family": family,
                        "filein": os.path.join(path, f"{cycle}_{family}"),
                        "db_new": db_path(work_path, family, name, date_start, date_end),
                        "regions": list(regions),
                        "flags": list(flags),
                        "varnos": list(varnos),
                        "land_oceans": list(land_oceans),
                        "pathwork": work_path,
                        "special_on": special_on,
                    }
                )
    return tasks


def pair_db_path(work_path, family, ctl, exp, date_start, date_end) -> str:
    return _pair_db_path(work_path, family, ctl, exp, date_start, date_end)


def create_pairs_list(
    date_start,
    date_end,
    families,
    control,
    experiments,
    work_path,
    regions,
    flags,
    varnos,
    land_oceans=("all",),
    special_on=False,
) -> List[Dict]:
    """One pairing task per (cycle, family, experience)."""
    ctl_name, ctl_path = control
    tasks = []
    for cycle in _cycles(date_start, date_end):
        for family in families:
            for name, path in experiments:
                tasks.append(
                    {
                        "family": family,
                        "ctl_file": os.path.join(ctl_path, f"{cycle}_{family}"),
                        "exp_file": os.path.join(path, f"{cycle}_{family}"),
                        "exp_name": name,
                        "names": (ctl_name, name),
                        "pair_db": pair_db_path(
                            work_path, family, ctl_name, name, date_start, date_end
                        ),
                        "regions": list(regions),
                        "flags": list(flags),
                        "varnos": list(varnos),
                        "land_oceans": list(land_oceans),
                        "pathwork": work_path,
                        "special_on": special_on,
                    }
                )
    return tasks


def _report_pairing(tasks, results, elapsed: float) -> None:
    """How much of each run the comparison covers, per family."""
    summary: Dict[tuple, Dict[str, int]] = {}
    failed = 0
    for t, r in zip(tasks, results):
        if r is None:
            failed += 1
            continue
        acc = summary.setdefault((t["family"], t["exp_name"]), {})
        for k, v in r.items():
            acc[k] = acc.get(k, 0) + int(v or 0)
    print(
        f"[vdedr] matching time: {elapsed:.1f}s " f"({len(tasks) - failed}/{len(tasks)} tasks)",
        flush=True,
    )
    for (family, exp_name), acc in summary.items():
        ctl, exp = acc.get("obs_c", 0), acc.get("obs_e", 0)
        pairs = acc.get("pairs", 0)
        print(
            f"[vdedr]   {family} {exp_name}: {pairs} common obs "
            f"({pairs / ctl * 100 if ctl else 0:.1f}% of control, "
            f"{pairs / exp * 100 if exp else 0:.1f}% of experience)",
            flush=True,
        )
        if pairs == 0 and (ctl or exp):
            print(
                f"[vdedr]   WARNING {family}: no common observation; the "
                f"channels will be tested as independent samples",
                file=sys.stderr,
                flush=True,
            )
        # the key was not unique somewhere: say so once
        from pikobs.match import DEFAULT_KEY, MatchSpec, repeat_warning

        t0 = next((t for t in tasks if t["family"] == family), {})
        spec = MatchSpec(True, tuple(t0.get("match_fields") or DEFAULT_KEY))
        ctl_name = (t0.get("names") or ("control",))[0]
        msg = repeat_warning(
            "vdedr",
            f"{family} ({exp_name})",
            spec,
            {
                ctl_name: (acc.get("rep_keys_c", 0), acc.get("rep_rows_c", 0)),
                exp_name: (acc.get("rep_keys_e", 0), acc.get("rep_rows_e", 0)),
            },
        )
        if msg:
            print(msg, file=sys.stderr, flush=True)


def _compact_task(path: str, tmp_dir: str) -> Optional[str]:
    """Sum the per-cycle rows over the period and index the result."""
    if not os.path.isfile(path):
        return None
    os.makedirs(tmp_dir, exist_ok=True)
    os.environ["SQLITE_TMPDIR"] = tmp_dir
    new = path + ".compact"
    try:
        if os.path.exists(new):
            os.remove(new)
        with open_result(new) as conn:
            conn.execute("PRAGMA journal_mode = OFF;")
            conn.execute("PRAGMA synchronous = OFF;")
            conn.execute("PRAGMA temp_store = FILE;")
            conn.execute("ATTACH DATABASE ? AS src;", (path,))
            conn.execute(_DDL_SERIE)
            conn.execute("""
                INSERT INTO serie_vdedr
                SELECT region, flag, land_ocean, special, id_stn, CODTYP,
                       varno, vcoord,
                       MIN(date), SUM(Ntot), SUM(s_omp), SUM(s2_omp),
                       SUM(s_oma), SUM(s2_oma), SUM(n_bcorr), SUM(s_bcorr)
                FROM src.serie_vdedr
                GROUP BY region, flag, land_ocean, special, id_stn, CODTYP,
                         varno, vcoord;
            """)
            conn.execute(
                "CREATE INDEX idx_serie ON serie_vdedr "
                "(region, flag, land_ocean, special, varno, id_stn, "
                "vcoord);"
            )
            conn.execute("DETACH DATABASE src;")
        os.replace(new, path)
        return path
    except Exception:
        print(
            f"[vdedr] compaction failed for {path}:\n" f"{traceback.format_exc()}",
            file=sys.stderr,
            flush=True,
        )
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────


def _report_timing(timing: Dict[str, Any], pathwork: str) -> None:
    sec = timing["seconds"]
    print("[vdedr] -------------------- run time --------------------", flush=True)
    print(
        f"[vdedr] input        {_fmt_bytes(timing['input_bytes']):>10s}"
        f"   {timing['input_files']} files, {timing['cycles']} cycles, "
        f"{timing['runs']} run(s)",
        flush=True,
    )
    for phase in ("extraction", "compaction", "plots"):
        if phase in sec:
            print(f"[vdedr] {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(
        f"[vdedr] total        {sec['total']:>8.1f} s   "
        f"({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
        flush=True,
    )
    try:
        with open(os.path.join(pathwork, "vdedr_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError as exc:
        print(f"[vdedr] could not write vdedr_timing.json: {exc}", file=sys.stderr, flush=True)


def _vdedr_options(
    control, experiments, regions, flag_criteria, id_stn, land_ocean, special_column, match
):
    """The runs, comparisons and selections, cleaned and said once in the log."""

    runs = [control] + list(experiments)
    regions = _split_tokens(regions)
    flags = _split_tokens(flag_criteria)
    comparisons = build_comparisons(control, experiments)
    stn_tokens = parse_station_tokens(id_stn)
    land_oceans = _split_tokens(land_ocean) or ["all"]
    bad = [s for s in land_oceans if s not in ("all", "land", "ocean")]
    if bad:
        raise ValueError(f"LAND_OCEAN takes all, land and ocean, not {bad}")
    special_on = str(special_column).strip().lower() in ("on", "true", "1", "yes")

    print(f"[vdedr] runs: {', '.join(n for n, _ in runs)}", flush=True)

    if control is not None:

        print(
            f"[vdedr] control: {control[0]}  |  "
            + (
                "matched observation by observation"
                if match
                else "compared, NOT matched: each run with all its "
                "observations, t-test and F-test"
            ),
            flush=True,
        )
    print(f"[vdedr] comparisons: " f"{', '.join(c.label for c in comparisons)}", flush=True)
    print(f"[vdedr] regions: {regions}", flush=True)
    print(f"[vdedr] flags_criteria: {flags}", flush=True)
    print(
        f"[vdedr] land_ocean: {land_oceans}  |  special column: "
        f"{'on' if special_on else 'off'}",
        flush=True,
    )
    print(f"[vdedr] id_stn tokens: {stn_tokens}", flush=True)

    return runs, regions, flags, comparisons, stn_tokens, land_oceans, special_on


def _extract_vdedr(tasks, n_cpu, client, timing):
    """Extraction: every cycle of every run into its database."""

    t0 = time.time()
    print(f"[vdedr] extraction: {len(tasks)} tasks, {n_cpu} worker(s)", flush=True)
    res = run_tasks(_extract_task, [(t,) for t in tasks], client, label="extraction")
    timing["seconds"]["extraction"] = time.time() - t0
    print(
        f"[vdedr] extraction time: "
        f"{timing['seconds']['extraction']:.1f}s "
        f"({sum(r is not None for r in res)}/{len(tasks)} files)",
        flush=True,
    )


def _pair_vdedr(
    match,
    datestart,
    dateend,
    families,
    control,
    experiments,
    pathwork,
    regions,
    flags,
    varnos,
    land_oceans,
    special_on,
    match_spec,
    client,
    timing,
):
    """Control and experience matched, observation by observation."""

    # The pairs: vdedr always has a control, so this always runs.
    # One task per cycle, family and experience, like the extraction.
    # matching is the normal mode; MATCH=off skips it and the
    # figures fall back on the independent tests
    pair_tasks = (
        []
        if not match
        else create_pairs_list(
            datestart,
            dateend,
            families,
            control,
            experiments,
            pathwork,
            regions,
            flags,
            varnos,
            land_oceans,
            special_on,
        )
    )
    t0 = time.time()
    for t in pair_tasks:
        t["match_fields"] = match_spec.fields
    print(f"[vdedr] matching control and experience: " f"{len(pair_tasks)} tasks", flush=True)
    pair_res = run_tasks(_pairs_task, [(t,) for t in pair_tasks], client, label="matching")
    timing["seconds"]["matching"] = time.time() - t0
    _report_pairing(pair_tasks, pair_res, timing["seconds"]["matching"])


def _compact_vdedr(tasks, pathwork, client, timing):
    """Each database compacted."""

    t0 = time.time()
    dbs = sorted({t["db_new"] for t in tasks})
    tmp_dir = os.path.join(pathwork, ".sqlite_tmp")
    run_tasks(_compact_task, [(d, tmp_dir) for d in dbs], client, label="compaction")
    shutil.rmtree(tmp_dir, ignore_errors=True)
    timing["seconds"]["compaction"] = time.time() - t0


def _draw_vdedr(
    pathwork,
    families,
    comparisons,
    regions,
    flags,
    stn_tokens,
    datestart,
    dateend,
    land_oceans,
    svg,
    client,
    timing,
    match: bool = True,
    both: bool = False,
    modes=("on",),
):
    """The figures of each comparison, drawn: MATCH on from the pairs, off
    from each run with all its observations; both, each figure twice."""

    plot_tasks = build_plot_tasks(
        pathwork,
        families,
        comparisons,
        regions,
        flags,
        stn_tokens,
        datestart,
        dateend,
        land_oceans,
    )
    # every comparison once per asked mode (on needs its pairs)
    plot_tasks = [dict(t, svg=svg, match_mode=m) for t in plot_tasks for m in modes
                  if m != "on" or t.get("db_pairs")]
    t0 = time.time()
    print(
        f"[vdedr] plots: {len(plot_tasks)} tasks " f"({len(plot_tasks) * len(METRICS)} figures)",
        flush=True,
    )
    results = run_tasks(vdedr_plot_task, [(t,) for t in plot_tasks], client, label="plots")
    timing["seconds"]["plots"] = time.time() - t0
    print(
        f"[vdedr] plot time: {timing['seconds']['plots']:.1f}s "
        f"({sum(r is not None for r in results)}/{len(plot_tasks)})",
        flush=True,
    )

    return plot_tasks, results


def make_vdedr(
    experiments: Sequence[Tuple[str, str]],
    control: Tuple[str, str],
    pathwork: str,
    datestart: str,
    dateend: str,
    regions: List[str],
    families: List[str],
    flag_criteria: List[str],
    id_stn: Any = "join",
    varnos: Sequence[str] = (),
    n_cpu: int = 1,
    svg: bool = False,
    match: bool = True,
    land_ocean=("all",),
    special_column="off",
) -> int:
    """Extract the per-channel statistics, draw the plots, write the viewer."""
    # MATCH: on, off, or the fields of the key -- pikobs.match decides.
    # Past this point match is True / False as before; the key travels
    # in match_spec.
    from pikobs.match import parse_modes

    # MATCH: on, off, no (or empty: no test), several at once -- each asked
    # mode is drawn, a switch in the viewer between them
    modes, match_spec = parse_modes(match)
    match = "on" in modes
    both = len(modes) > 1

    runs, regions, flags, comparisons, stn_tokens, land_oceans, special_on = _vdedr_options(
        control, experiments, regions, flag_criteria, id_stn, land_ocean, special_column, match
    )

    if not check_input_files(runs, families, datestart, dateend, "vdedr"):
        return 1

    t_start = time.time()
    cycles = _cycles(datestart, dateend)
    n_input, input_bytes = _input_size(runs, families, cycles)
    timing: Dict[str, Any] = {
        "datestart": datestart,
        "dateend": dateend,
        "cycles": len(cycles),
        "families": list(families),
        "runs": len(runs),
        "comparisons": [c.label for c in comparisons],
        "regions": regions,
        "flags": flags,
        "id_stn": stn_tokens,
        "land_ocean": land_oceans,
        "special_column": special_on,
        "n_cpus": n_cpu,
        "svg": svg,
        "input_files": n_input,
        "input_bytes": input_bytes,
        "seconds": {},
    }

    for family in families:
        pikobs.delete_create_folder(pathwork, family)

    tasks = create_data_list(
        datestart,
        dateend,
        families,
        runs,
        pathwork,
        regions,
        flags,
        varnos,
        land_oceans,
        special_on,
    )

    client, dask_dir = start_workers(n_cpu, "vdedr")
    plot_tasks: List[Dict[str, Any]] = []
    results: List[Any] = []
    try:

        _extract_vdedr(tasks, n_cpu, client, timing)
        _pair_vdedr(
            match,
            datestart,
            dateend,
            families,
            control,
            experiments,
            pathwork,
            regions,
            flags,
            varnos,
            land_oceans,
            special_on,
            match_spec,
            client,
            timing,
        )
        _compact_vdedr(tasks, pathwork, client, timing)
        plot_tasks, results = _draw_vdedr(
            pathwork,
            families,
            comparisons,
            regions,
            flags,
            stn_tokens,
            datestart,
            dateend,
            land_oceans,
            svg,
            client,
            timing,
            match=match,
            both=both,
            modes=modes,
        )
    finally:
        stop_workers(client, dask_dir)

    items = vdedr_viewer_items(plot_tasks, results)
    if not items:
        print(
            "[vdedr] ERROR: no figure was produced, viewer not written.",
            file=sys.stderr,
            flush=True,
        )
        return 1
    _write_viewer(
        items,
        pathwork,
        ([control] if control else []) + list(experiments),
        control,
        (datestart, dateend),
    )

    timing["seconds"]["total"] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"[vdedr] done -- output in: {pathwork}", flush=True)
    return 0


def build_plot_tasks(
    pathwork,
    families,
    comparisons,
    regions,
    flags,
    stn_tokens,
    datestart,
    dateend,
    land_oceans=("all",),
) -> List[Dict[str, Any]]:
    """One task per (comparison, family, region, criteria, selection, varno).

    The station selection follows the tokens of --id_stn, with the same
    meaning as in scatter: join, all, a prefix, =exact, a LIKE pattern or a
    codtyp label. Each task writes the three figures of that selection.
    """
    tasks = []
    for family in families:
        dbs = {
            name: db_path(pathwork, family, name, datestart, dateend)
            for name in {c.control for c in comparisons} | {c.experience for c in comparisons}
        }
        present = [p for p in dbs.values() if os.path.isfile(p)]
        if not present:
            continue
        selectors = expand_station_selectors(present, stn_tokens, family, table="serie_vdedr")
        rows = _query_distinct(
            present,
            "SELECT DISTINCT region, flag, land_ocean, " "special, varno FROM serie_vdedr;",
        )
        for comp in comparisons:
            files = [dbs[comp.control], dbs[comp.experience]]
            if not all(os.path.isfile(f) for f in files):
                continue
            for region, flag, land_ocean, special, varno in rows:
                if region not in regions or flag not in flags or land_ocean not in land_oceans:
                    continue
                for sel in selectors:
                    # the matched observations, when the run made them;
                    # without the file the figure falls back on Welch
                    pdb = pair_db_path(
                        pathwork, family, comp.control, comp.experience, datestart, dateend
                    )
                    tasks.append(
                        {
                            "pathwork": pathwork,
                            "family": family,
                            "files_in": files,
                            "db_pairs": pdb if os.path.isfile(pdb) else None,
                            "names_in": [comp.control, comp.experience],
                            "comparison": comp.label,
                            "comparison_key": comp.key,
                            "region": region,
                            "flag": flag,
                            "land_ocean": land_ocean,
                            "special": special,
                            "special_label": special_label(family, special),
                            "selector": sel,
                            "id_stn": sel.display,
                            "stn_sql": sel.sql(),
                            "stn_tag": sel.tag,
                            "varno": int(varno),
                            "datestart": datestart,
                            "dateend": dateend,
                        }
                    )
    return tasks


def _query_distinct(db_paths, sql) -> List[tuple]:
    return query_distinct(db_paths, sql, label="vdedr")


def _write_viewer(
    items: List[Dict[str, Any]], pathwork: str, runs=(), control=None, period=None
) -> None:
    import inspect

    keys = [
        "comparison",
        "metric",
        "family",
        "region",
        "land_ocean",
        "flag",
        "id_stn",
        "special",
        "varno",
    ] + (["match"] if len({it.get("match") for it in items} - {"", None}) > 1 else [])
    key_labels = {
        "metric": "Metric",
        "flag": "Criteria",
        "varno": "Varno",
        "comparison": "Comparison",
        "match": "Match",
        "special": special_key_label({it.get("family") for it in items}),
    }
    from pikobs.web.viewer import generate_web

    params = inspect.signature(generate_web).parameters
    kwargs = {}
    for name, value in (
        ("title", "Pikobs VDEDR Viewer"),
        ("key_labels", key_labels),
        (
            "subtitle",
            "Channel statistics of the control "
            "against each experience." + runs_block(runs, control, period),
        ),
        ("enable_play", False),
    ):
        if name in params:
            kwargs[name] = value
    print(f"[vdedr] viewer selectors: {keys}", flush=True)
    generate_web(items, keys, os.path.join(pathwork, "pikobs_vdedr_viewer.html"), **kwargs)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

_UNSET = ("", "undefined", None)


def arg_call() -> None:
    import argparse

    p = argparse.ArgumentParser(
        prog="pikobs-vdedr", description="Radiance verification, control vs experience(s)."
    )
    p.add_argument("--path_control_files", default="")
    p.add_argument("--control_name", default="")
    p.add_argument(
        "--path_experience_files",
        nargs="+",
        default=[],
        help="One or more RDB directories (exp1 exp2 ...).",
    )
    p.add_argument(
        "--experience_name", nargs="+", default=[], help="One label per experience, same order."
    )
    p.add_argument("--pathwork", default=None)
    p.add_argument("--datestart", default=None)
    p.add_argument("--dateend", default=None)
    p.add_argument("--region", nargs="+", default=None)
    p.add_argument("--family", nargs="+", default=None)
    p.add_argument("--flags_criteria", nargs="+", default=None)
    p.add_argument(
        "--land_ocean",
        nargs="+",
        default=["all"],
        choices=["all", "land", "ocean"],
        help="all (no filter), land, ocean: one series of figures "
        "each; land and ocean read the land mask.",
    )
    p.add_argument(
        "--special_column",
        default="off",
        choices=["on", "off"],
        help="on: one series of figures per value of the family's "
        "special column; off: all together (default).",
    )
    p.add_argument(
        "--id_stn",
        nargs="+",
        default=["join"],
        help="Tokens, one series of figures each: join, all, "
        "PREFIX, LIKE%%pattern, =EXACT, 'NAME (codtyp)'.",
    )
    p.add_argument(
        "--varnos", nargs="+", default=[], help="Optional varno list; empty = the family default."
    )
    p.add_argument(
        "--match",
        nargs="+",
        default=["on"],
        help=("on: only the observations both runs hold, paired one by one. "
             "off: every observation of each run (t-test and F-test). "
             "no: every observation, no test. Several at once draw each, "
             "with a Match switch in the viewer: on off no."),
    )
    p.add_argument(
        "--svg",
        default="off",
        choices=["on", "off"],
        help="Also write each figure as SVG, next to the PNG, for "
        "editing before a presentation (default off).",
    )
    p.add_argument("--n_cpus", "--n_cpu", default=1, type=int, dest="n_cpus")
    p.add_argument(
        "--no_submit", action="store_true", help="Skip PBS auto-submission and run locally."
    )

    args = p.parse_args()
    # blank control values are no control: an empty variable in the
    # wrapper must not become a directory called ' '
    for _attr in ("path_control_files", "control_name"):
        _val = getattr(args, _attr, None)
        if isinstance(_val, str) and not _val.strip():
            setattr(args, _attr, None)
    for attr in ("region", "family", "flags_criteria", "varnos"):
        val = getattr(args, attr)
        if isinstance(val, list):
            setattr(args, attr, _split_tokens(val))
    for arg in vars(args):
        print(f"--{arg} {getattr(args, arg)}", flush=True)

    for attr, flag in [
        ("pathwork", "--pathwork"),
        ("datestart", "--datestart"),
        ("dateend", "--dateend"),
        ("region", "--region"),
        ("family", "--family"),
        ("flags_criteria", "--flags_criteria"),
    ]:
        if getattr(args, attr) in (None, [], "undefined", ""):
            raise ValueError(f"{flag} is required")

    paths = [p_ for p_ in _split_tokens(args.path_experience_files) if p_ not in _UNSET]
    names = [n for n in _split_tokens(args.experience_name) if n not in _UNSET]
    if not paths:
        raise ValueError("--path_experience_files is required")
    if len(paths) != len(names):
        raise ValueError(
            f"--path_experience_files ({len(paths)}) and "
            f"--experience_name ({len(names)}) must have the "
            f"same number of entries"
        )
    if args.path_control_files in _UNSET or args.control_name in _UNSET:
        raise ValueError(
            "--path_control_files and --control_name are "
            "required (vdedr compares against a control)"
        )

    control = (args.control_name, args.path_control_files.rstrip("/") or "/")
    experiments = [(n, p_.rstrip("/") or "/") for n, p_ in zip(names, paths)]
    all_names = [control[0]] + [n for n, _ in experiments]
    if len(set(all_names)) != len(all_names):
        raise ValueError(f"run names must be unique: {all_names}")

    maybe_submit_to_pbs(args)

    sys.exit(
        make_vdedr(
            experiments,
            control,
            args.pathwork,
            args.datestart,
            args.dateend,
            args.region,
            args.family,
            args.flags_criteria,
            id_stn=args.id_stn,
            varnos=args.varnos,
            n_cpu=args.n_cpus,
            svg=svg_enabled(args.svg),
            match=args.match,
            land_ocean=args.land_ocean,
            special_column=args.special_column,
        )
    )


if __name__ == "__main__":
    arg_call()
