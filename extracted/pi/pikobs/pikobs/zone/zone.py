#!/usr/bin/python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_zone.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""======================================================
pikobs.zone -- Zonal cross-sections of the departures
======================================================

A map tells you where a departure is wrong; a zonal section tells you at
which height. That is the question behind most of what goes wrong with
winds and radiances: the jet level that drifts, the lower troposphere that
a new bias correction overdoes, the stratospheric channels that nobody
looks at until they hurt. ``zone`` puts latitude on the x axis and the
vertical coordinate of the family on the y axis, and fills every cell
with the statistics of the observations that fell in it.

Given a control, it compares, and it does it on the same observations:
the two runs are matched one by one before anything is summed.

Quick start
===========

.. code-block:: bash

   # one or several experiences, each on its own figures
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_zone_exp.sh
   chmod +x run_zone_exp.sh

   # a control against one or several experiences
   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_zone_cont_exp.sh
   chmod +x run_zone_cont_exp.sh

The wrapper runs on the node you are on and never submits to PBS, so open
a compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_zone_cont_exp.sh
   ./run_zone_cont_exp.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period, of every run, in parallel.

A real run, six families and five regions against a control, over six
days:

.. code-block:: text

   [zone] control: control  |  matched observation by observation with: experience
   [zone] sw: vcoord = round(vcoord/2000.)*2000  (PRESSION)
   [zone] iasi: vcoord = vcoord  (CANAL)
   [zone] input check OK: 24 cycles x 2 run(s) x 6 family(ies), 288 files, 56.3 GB
   [zone] extraction time: 29.9s (288/288 files)
   [zone] colour scales: 18 group(s) shared (family x varno x fonction x region)
   [zone] plot time: 10.9s (597/597)
   [zone] total            62.9 s   (1.0 min, 80 workers)
   Viewer: /home/dlo001/sites8/pikobs_zone_cont_exp/pikobs_zone_viewer.html
   Web:    https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_zone_cont_exp/pikobs_zone_viewer.html

The last two lines come from the module: when a link of ``~/public_html``
already shows the folder the address goes through it, otherwise the run
prints the one ``ln -s`` that would make the page reachable.

Two live instances, both made by ``run_doc_examples.sh`` from the same
two suites over the same days, and refreshed with the documentation:

* :live:`one run on its own <pikobs_doc_zone_exp/pikobs_zone_viewer.html>`
* :live:`G0 against G2 <pikobs_doc_zone/pikobs_zone_viewer.html>`, the operational suite as the control, with the comparison panels and the tests

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of every run and family is looked up
first. If one is missing the run stops before touching ``PATHWORK``, says
which cycles are missing and which dates the directory does hold.

**One pass per file.** Each cycle is read once. Regions, criteria, levels
and the land/ocean split are all summed in that pass, as sums rather than
means, so combining cycles later is an addition and the sigma stays
exact.

**Matching, with a control.** The observations of the two runs are paired
on station, position, date, time and their rank inside the profile, and
only the pairs are kept. Both sides of a cell therefore rest on exactly
the same observations: a flag that differs between the runs cannot change
the sample under your feet. The pairs are summed cycle by cycle, which is
what the test of ``MATCH=on`` works on.

**One grid per region.** Before drawing, the module collects every level
the family has in the period and puts every figure of a region on the
same grid: the latitudes of the region in bands of ``LAT_BAND`` --
``Canada`` from 45 to 90, not a globe three quarters empty -- and the same
rows on the y axis. Two runs, or two experiences, line up band by band
when you flip between them. A polygon region is drawn on the whole globe.

**Shared colours.** Every figure of the same family, varno, function and
region gets the same colour scales: a pale red is the same value for one
station and for all of them, for one experience and for the next. The
scales follow the region rather than the most extreme one of the run, so
``Canada`` gets its own colours instead of the two darkest of the globe.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of a wrapper is meant to be edited.

.. wrapper-settings:: run_zone_exp.sh run_zone_cont_exp.sh

With ``DATESTART`` and ``DATEEND`` empty, the window is worked out from
today: it ends ``DAYS_BACK_END`` days ago and covers ``WINDOW_DAYS`` days.
That is what a daily run wants, from a source that only keeps the last
days.

----

3. Stations and instrument types
================================

+---------------------------+--------------------------------------------------------------------+
| Token                     | Figures produced                                                   |
+===========================+====================================================================+
| ``join``                  | one, every station together: the natural choice for a section      |
+---------------------------+--------------------------------------------------------------------+
| ``all``                   | one per station; on ai, sf, ua, gp and csr one per instrument type |
+---------------------------+--------------------------------------------------------------------+
| ``pilot``, ``AMDAR (42)`` | on a composite family, that instrument type                        |
+---------------------------+--------------------------------------------------------------------+
| ``CAS`` or ``"CAS*"``     | the stations whose id starts with CAS, together                    |
+---------------------------+--------------------------------------------------------------------+
| ``=NOAA20``               | that station only                                                  |
+---------------------------+--------------------------------------------------------------------+

A section is about latitude, so ``join`` is usually the right choice. On
``ai``, ``sf``, ``ua``, ``gp`` and ``csr`` a station id is one aircraft or one
radiosonde, and one figure each would say nothing: there ``all`` groups by
instrument type instead, as every module does (see :doc:`families`).

A selection that sits in a single latitude band is not drawn, and the log
lists which one and where. It is usually a geostationary satellite at the
edge of a small region, or an instrument type with very few stations.

For ``sw``, ``SPECIAL_COLUMN="on"`` splits the winds by method, infrared or
water vapour: two populations with different errors that a single figure
would average together.

----

4. Reading a figure
===================

One run gives three panels:

+-----------------------+-------------------------------------------------------------------------+
| Panel                 | What it shows                                                           |
+=======================+=========================================================================+
| Sigma                 | sigma of the departure in each cell                                     |
+-----------------------+-------------------------------------------------------------------------+
| Mean                  | the departure itself: red above zero, blue below, white within the band |
+-----------------------+-------------------------------------------------------------------------+
| Observations per cell | how many observations each cell rests on                                |
+-----------------------+-------------------------------------------------------------------------+

With a control, five, all in one row and sharing the same y axis, so a
row can be followed from one panel to the next:

+-------------------+-----------------------------------------------------------------------------------+
| Panel             | What it shows                                                                     |
+===================+===================================================================================+
| Sigma, Exp - Ctl  | sigma of Exp minus sigma of Ctl, in the units of the variable                     |
+-------------------+-----------------------------------------------------------------------------------+
| Bias, Exp - Ctl   | abs(mean Exp) - abs(mean Ctl): negative is closer to zero                         |
+-------------------+-----------------------------------------------------------------------------------+
| Test of the sigma | red or blue where the sigma change passes 95 %; dark grey: too few cycles to test |
+-------------------+-----------------------------------------------------------------------------------+
| Test of the bias  | the same for the bias                                                             |
+-------------------+-----------------------------------------------------------------------------------+
| Sample size       | matched observations per cell: the same in both runs                              |
+-------------------+-----------------------------------------------------------------------------------+

.. image:: _static/zone_comparison.png
   :alt: Five panels of a comparison, sharing the same levels
   :align: center
   :width: 100%

Everything follows the convention of Pikobs: **experience minus
control**, so a negative value is an improvement and is drawn in red;
blue is where the control was better.

The example above compares O-A, and on purpose. G0 and G2 are two passes
of the same operational cycle, G2 later and with more observations, and
they start from the same background: an observation both have gets the
same O-P in each, to the last bit, so every O-P panel of their comparison
is white. The analysis is where they part, and O-A shows it (the same
case is worked through in :doc:`scatter`).

The differences are in the units of the variable, not in percent. A
percentage of the control bias explodes wherever that bias is close to
zero: going from 0.01 to 0.07 m/s would read as +600 %, when it is six
hundredths of a metre per second. Inside ``+/- WHITE_BAND`` the cell is
white, so what is coloured is a change worth reading. By default
``WHITE_BAND=auto``: everything under a tenth of the largest change of
the panel is white, so the band suits the winds of ``sw`` as well as the
normalised departures of ``ro``, and the colour bar says how wide it is.
A number fixes it instead, in the units of the variable.

Refractivity goes further: its sigma is 3 to 5 near the ground and a
few tenths above 6 km, and on a linear scale the upper half of the
figure was one colour. When the largest sigma of a figure is more than
five times the typical one, the scales go in 1-2-5 steps -- 0.1, 0.2,
0.5, 1, 2, 5 -- and the white band is at most a tenth of the typical
sigma, so the tenths aloft and the units below both read. Winds and
temperatures, whose sigma varies little, keep their linear scales.

The sample-size panel is not a comparison. With matched observations the
count is the same in both runs; it is there to read the tests against.

----

5. The tests
============

Every cell is tested on its own, the sigma and the bias apart, and each
test has its map under the change it judges. With ``MATCH=no`` the two
test maps are left out and the section is drawn on two rows: the
changes on top, each run's counts under them.


Which observations, and which test: MATCH
-----------------------------------------

Two runs rarely keep the same observations, so ``MATCH`` decides what a
comparison is made of.

.. list-table::
   :header-rows: 1
   :widths: 10 35 35 20

   * - ``MATCH``
     - Observations
     - Test of each cell
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


Two things to keep in mind. A cell with twenty observations will rarely
pass, however good the change; and one with two thousand will pass on a
change that may not matter. The sample-size panel is there to tell the
two apart.

----

6. The vertical axis
====================

+----------------------------+----------------------------------------------------------------------------+
| VCOTYP of the family       | The y axis                                                                 |
+============================+============================================================================+
| ``CANAL``                  | one row per channel, first channel at the top, every one labelled          |
+----------------------------+----------------------------------------------------------------------------+
| ``PRESSION``               | hPa, ground at the bottom; one row per level while there are fewer than 60 |
+----------------------------+----------------------------------------------------------------------------+
| ``HAUTEUR(metres)``        | metres, upwards                                                            |
+----------------------------+----------------------------------------------------------------------------+
| ``SURFACE`` / ``LATITUDE`` | no vertical axis: these families are not drawn as sections                 |
+----------------------------+----------------------------------------------------------------------------+

The level comes from the ``VCOORD`` of the family, not from the raw
column: ``sw`` and ``ua`` round their pressure, and reading the column
directly would give thousands of levels where every other module has a
few tens. A family that rounds its pressure puts everything above its
first bin into the bin 0, which is labelled ``< 100`` rather than a 0 hPa
that does not exist.

With many channels the figure grows in height, 0.14 inch per row, so
that every channel keeps its number.

----

7. The viewer
=============

``pikobs_zone_viewer.html`` has one selector per dimension: Experience,
Family, Fonction, Region, Criteria, Station, Special, Channel, Land/ocean
and Varno. With several experiences each is its own comparison, ``A120 vs
CTL`` and ``A125 vs CTL``, and **Flip** switches between them on the same
grid and the same colours. Tall figures are shown at the full width of the
page; **W** switches between fitting the width and fitting the screen.

----

8. Output layout
================

::

   $PATHWORK/
   ├── pikobs_zone_viewer.html
   ├── zone_timing.json
   └── <family>/
       ├── zone_<tag>_<selection>_<start>_<end>_<family>.db
       └── zone_<runs>_<family>_<fonction>_varno<N>_<station>_<region>[_<surface>][_<special>]_<flag>_ch<mode>.png

The databases hold the sums per region, criteria, station, level,
latitude band and cycle, and can be queried with any SQLite client.

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation.

----

9. Support
==========

Bugs and feature requests:
   `<https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`_
"""

import json
import os
import re
import sys
import time
import traceback
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

# a region is a box or a polygon; the module does not need to know
import pikobs
from pikobs.figures import svg_enabled
from pikobs.obsdb import (
    check_input_files,
    combine as _combine_rows,
    cycle_path,
    cycles as _cycles,
    fmt_bytes,
    input_size,
    open_result,
    table_columns,
    work_db,
)
from pikobs.obsdb.obsdb import split_tokens as _split_tokens  # shared, once
from pikobs.parallel import run_tasks
from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.stations.stations import expand_station_selectors, parse_station_tokens
from pikobs.web.viewer import generate_web
from pikobs.web.runs import runs_block
from pikobs.zone.zone_plot import (
    zone_plot_task,
    zone_scale_task,
    scale_group,
    LAND_OCEAN_CHOICES,
    MIN_OBS_PER_CELL,
    WHITE_BAND,
)
from pikobs.zone.zone_plot import level_selector_label

CYCLE_HOURS = 6

# One row per (region, flag, channel mode, land/ocean, station, varno,
# level, latitude band, cycle). Sums, never means: any later grouping is
# then an addition, and the sigma stays exact.
_SINGLE_COLS = (
    "region, flag, channel_mode, land_ocean, id_stn, special, "
    "varno, vcoord, lat, date, n, n_omp, n_oma, n_err, "
    "s_omp, s2_omp, s_oma, s2_oma, s_obs, s2_obs, "
    "s_bcorr, s2_bcorr, s_err, s2_err, nrej, nacc, nprofile"
)

_DDL_SINGLE = """
    CREATE TABLE IF NOT EXISTS zone (
        region TEXT, flag TEXT, channel_mode TEXT, land_ocean TEXT,
        id_stn TEXT, special TEXT, varno INTEGER, vcoord FLOAT, lat FLOAT,
        date INTEGER, n INTEGER, n_omp INTEGER, n_oma INTEGER,
        n_err INTEGER,
        s_omp FLOAT, s2_omp FLOAT, s_oma FLOAT, s2_oma FLOAT,
        s_obs FLOAT, s2_obs FLOAT, s_bcorr FLOAT, s2_bcorr FLOAT,
        s_err FLOAT, s2_err FLOAT,
        nrej INTEGER, nacc INTEGER, nprofile INTEGER
    );
"""

# The matched table carries both runs plus the cross sums, which is what
# makes a paired test possible later: without sum(x*y) the covariance of
# the two runs is lost and only the cautious Welch form is left.
_PAIR_COLS = (
    "region, flag, channel_mode, land_ocean, id_stn, special, "
    "varno, vcoord, lat, date, n, n_oma, n_err, "
    "c_omp, c2_omp, e_omp, e2_omp, ce_omp, "
    "c_oma, c2_oma, e_oma, e2_oma, ce_oma, "
    "c_obs, e_obs, c_err, e_err"
)

_DDL_PAIRS = """
    CREATE TABLE IF NOT EXISTS zone_pairs (
        region TEXT, flag TEXT, channel_mode TEXT, land_ocean TEXT,
        id_stn TEXT, special TEXT, varno INTEGER, vcoord FLOAT, lat FLOAT,
        date INTEGER, n INTEGER, n_oma INTEGER, n_err INTEGER,
        c_omp FLOAT, c2_omp FLOAT, e_omp FLOAT, e2_omp FLOAT, ce_omp FLOAT,
        c_oma FLOAT, c2_oma FLOAT, e_oma FLOAT, e2_oma FLOAT, ce_oma FLOAT,
        c_obs FLOAT, e_obs FLOAT, c_err FLOAT, e_err FLOAT
    );
"""

# The land mask is shared: histogram, timeserie and the maps of the
# regions read the same grid, so it lives in configobs and this module
# only keeps the names it already used.
from pikobs.configobs.landmask import (
    LAND_MASK_CACHE_SUBDIR as _LAND_MASK_CACHE_SUBDIR,
    is_land_function as _is_land_function,
    mmap_land_mask as _mmap_land_mask,
)

# ─────────────────────────────────────────────────────────────────────────────
# Extraction
# ─────────────────────────────────────────────────────────────────────────────

# GPS-RO: every departure is divided by a reference refractivity profile
# before it is summed, B_ref = 300 exp(-h / 6500), so a level near the
# ground, where refractivity is hundreds of times larger, does not flatten
# the stratosphere; and a profile passes the quality gates of the
# operational verification before it counts.
from pikobs.configobs.landmask import RO_FAMILIES  # noqa: F401 -- defined once, in configobs

# the land mask package, found without importing it: its import loads a
# 0.93 GB grid in every process, and every Dask worker imports pikobs
import importlib.util as _ilu
from pikobs.obsdb import safe_name as _safe
from pikobs.parallel import start_workers, stop_workers
from pikobs.selection import (  # shared with histogram and verifprofile
    is_composite as _is_composite,
    num as _num,
    is_num as _is_num,
    distinct as _distinct,
    combinations as _combinations,
    selections as _selections,
    station_select as _station_select,
    special as _special,
    special_label as _special_label,
    ro_ref as _ro_ref,
    save_members as _save_members,
)
from pikobs.obsdb import run_db_path

_HAS_LAND_MASK = _ilu.find_spec("global_land_mask") is not None


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def db_path(work_path: str, family: str, tag: str, date_start: str, date_end: str) -> str:
    """One database per comparison and family; the rest are columns."""
    return run_db_path("zone", work_path, family, tag, date_start, date_end)


# ─────────────────────────────────────────────────────────────────────────────
# Land / ocean
# ─────────────────────────────────────────────────────────────────────────────


def _ro_terms(alias: str, has_err: bool, has_oma: bool) -> Dict[str, str]:
    """Normalised values and quality gates of one side, as SQL."""
    ref = f"ro_ref({alias}.vcoord)"
    gates = (
        f" AND {alias}.vcoord > -1000 AND {alias}.vcoord < 100000"
        f" AND ({alias}.obsvalue - {alias}.omp) > 0"
        f" AND ({alias}.obsvalue - {alias}.omp) < 500"
        f" AND {alias}.obsvalue / {ref} > 0.3"
        f" AND {alias}.obsvalue / {ref} < 3"
        f" AND {alias}.omp / {ref} > -0.05"
        f" AND {alias}.omp / {ref} < 0.05"
    )
    if has_err:
        gates += (
            f" AND ({alias}.obs_error IS NULL OR "
            f"({alias}.obs_error / {ref} > 0 AND "
            f"{alias}.obs_error / {ref} < 1))"
        )
    oma = (
        (
            f"CASE WHEN {_is_num(f'{alias}.oma')} AND {alias}.oma / {ref} "
            f"> -0.05 AND {alias}.oma / {ref} < 0.05 THEN {alias}.oma / {ref} "
            f"END"
        )
        if has_oma
        else "NULL"
    )
    return {
        "omp": f"({alias}.omp / {ref})",
        "oma": oma,
        "obs": f"({alias}.obsvalue / {ref})",
        "err": (f"({_num(f'{alias}.obs_error')} / {ref})" if has_err else "NULL"),
        "gates": gates,
    }


def _bin_lat(expr: str, lat_band: float) -> str:
    return f"floor({expr} / {lat_band}) * {lat_band} + {lat_band} / 2."


def create_zone_single(
    family: str,
    new_db: str,
    cycle_file: str,
    regions,
    flags,
    channels,
    land_oceans,
    id_stn_sql: str,
    varnos,
    lat_band: float,
    pathwork: str,
    stn_label: Optional[str] = None,
    special_on: bool = True,
    gpsro: bool = False,
) -> Optional[int]:
    """One run: read a cycle once and sum every selection of it."""
    if not os.path.isfile(cycle_file):
        print(f"[zone] missing file, skipped: {cycle_file}", file=sys.stderr, flush=True)
        return None
    date_match = re.search(r"(\d{10})", os.path.basename(cycle_file))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {cycle_file}")
    date_int = int(date_match.group(1))

    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    vcoord_expr = (VCOORD or "").strip() or "vcoord"
    if varnos:
        element = ",".join(str(v) for v in varnos)
    combos = _combinations(regions, flags, channels, land_oceans, vcoord_expr)

    with work_db(attach={"db": cycle_file}) as (conn, mem_uri):
        if any(c["land_ocean"] != "all" for c in combos):
            if not _HAS_LAND_MASK:
                raise ImportError(
                    "--land_ocean needs the 'global_land_mask' "
                    "package, which is not installed here"
                )
            conn.create_function("is_land_sql", 2, _is_land_function(pathwork))
        # optional columns: a family without OMA, a stage without the
        # bias correction or the observation error must not fail the run
        cols = table_columns(conn, "DATA", "db")
        head_cols = table_columns(conn, "HEADER", "db")
        sp_sel, sp_group = _special(family, head_cols, special_on)

        def _col(name):
            return _num(name) if name in cols else "NULL"

        oma, bcorr, err = _col("oma"), _col("bias_corr"), _col("obs_error")
        omp, obs, ro_gates = "omp", "obsvalue", ""
        if gpsro:
            conn.create_function("ro_ref", 1, _ro_ref, deterministic=True)
            terms = _ro_terms("db.data", "obs_error" in cols, "oma" in cols)
            omp, oma, obs, err = (terms["omp"], terms["oma"], terms["obs"], terms["err"])
            ro_gates = terms["gates"]

        conn.execute(_DDL_SINGLE)
        codtyp_col = "codtyp" if "codtyp" in head_cols else "NULL"
        stn_sel, stn_group = _station_select(stn_label, family, codtyp_col)
        if stn_group == "NULL":
            stn_group = ""
        rows_written = 0
        for c in combos:
            chan_sel = "'join'" if c["channel"] == "join" else vcoord_expr
            terms = [t for t in (stn_group, sp_group, "varno", chan_sel, "lat_bin") if t]
            group = "GROUP BY " + ", ".join(terms)
            conn.execute(f"""
                INSERT INTO zone ({_SINGLE_COLS})
                SELECT '{c['region']}', '{c['flag']}', '{c['channel']}',
                       '{c['land_ocean']}', {stn_sel}, {sp_sel}, varno,
                       {chan_sel},
                       {_bin_lat('lat', lat_band)} AS lat_bin, {date_int},
                       COUNT(*), COUNT(*),
                       SUM(CASE WHEN {oma} IS NOT NULL THEN 1 ELSE 0 END),
                       SUM(CASE WHEN {err} IS NOT NULL THEN 1 ELSE 0 END),
                       SUM({omp}), SUM({omp}*{omp}),
                       SUM({oma}), SUM({oma}*{oma}),
                       SUM({obs}), SUM({obs}*{obs}),
                       SUM({bcorr}), SUM({bcorr}*{bcorr}),
                       SUM({err}), SUM({err}*{err}),
                       SUM(CASE WHEN (flag & 512) = 512 THEN 1 ELSE 0 END),
                       SUM(CASE WHEN (flag & 4096) = 4096 THEN 1 ELSE 0 END),
                       COUNT(DISTINCT id_obs)
                FROM db.header NATURAL JOIN db.data
                WHERE varno IN ({element})
                  AND {_is_num('obsvalue')} AND {_is_num('omp')}
                  {VCOCRIT}
                  {ro_gates}
                  {id_stn_sql}
                  AND {c['cond']}
                {group};
            """)
            rows_written += conn.total_changes
        _combine_rows(new_db, mem_uri, "zone", _SINGLE_COLS, ddl=_DDL_SINGLE, module="zone")
        if stn_label and stn_label != "join" and not _is_composite(family):
            _save_members(
                new_db,
                stn_label,
                conn.execute(
                    f"SELECT DISTINCT id_stn FROM db.header WHERE 1=1 " f"{id_stn_sql};"
                ).fetchall(),
            )
        return rows_written


def create_zone_matched(
    family: str,
    new_db: str,
    ctl_file: str,
    exp_file: str,
    regions,
    flags,
    channels,
    land_oceans,
    id_stn_sql: str,
    varnos,
    lat_band: float,
    pathwork: str,
    stn_label: Optional[str] = None,
    special_on: bool = True,
    gpsro: bool = False,
    match_fields=(),
    names=None,
):
    """Control and experience, matched observation by observation.

    The pair is what makes the comparison honest: both sides of a box
    come from the same observations, so a flag that differs between the
    runs cannot silently change the sample. The cross sums are kept as
    well, which is what a paired test needs later.
    """
    for path in (ctl_file, exp_file):
        if not os.path.isfile(path):
            print(f"[zone] missing file, skipped: {path}", file=sys.stderr, flush=True)
            return None
    date_match = re.search(r"(\d{10})", os.path.basename(ctl_file))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {ctl_file}")
    date_int = int(date_match.group(1))

    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    vcoord_expr = (VCOORD or "").strip() or "vcoord"
    from pikobs.match import (
        DEFAULT_KEY,
        MatchSpec,
        count_repeats,
        key_aliases,
        key_join,
        key_select,
    )

    spec = MatchSpec(True, tuple(match_fields) or DEFAULT_KEY)
    kc = key_select(spec, "ch", "cd")
    ke = key_select(spec, "eh", "ed")
    join_on = key_join(spec, "e", "c")
    names = tuple(names or ("control", "experience"))
    if varnos:
        element = ",".join(str(v) for v in varnos)
    combos = _combinations(regions, flags, channels, land_oceans, "c.vcoord_b", prefix="c")

    with work_db(attach={"ctl": ctl_file, "exp": exp_file}) as (conn, mem_uri):
        if any(c["land_ocean"] != "all" for c in combos):
            if not _HAS_LAND_MASK:
                raise ImportError(
                    "--land_ocean needs the 'global_land_mask' "
                    "package, which is not installed here"
                )
            conn.create_function("is_land_sql", 2, _is_land_function(pathwork))
        ctl_cols = table_columns(conn, "DATA", "ctl")
        exp_cols = table_columns(conn, "DATA", "exp")
        c_err = "cd.obs_error" if "obs_error" in ctl_cols else "NULL"
        e_err = "ed.obs_error" if "obs_error" in exp_cols else "NULL"
        c_oma = "cd.oma" if "oma" in ctl_cols else "NULL"
        e_oma = "ed.oma" if "oma" in exp_cols else "NULL"
        # the special column comes from the control, as the flag does
        ctl_head = table_columns(conn, "HEADER", "ctl")
        sp_sel_ctl, _ = _special(family, ctl_head, special_on, "ch.")
        c_codtyp = "ch.codtyp" if "codtyp" in ctl_head else "NULL"
        # Each run is read once into its own temporary table, with the
        # reference refractivity computed once per observation when the
        # family is GPS-RO, and the experience indexed on the whole key.
        # Joining the two files directly let SQLite index the experience
        # on (varno, vcoord) only, so every control observation walked
        # through every observation of its channel: close to quadratic.
        ref_c = "ro_ref(cd.vcoord)" if gpsro else "1.0"
        ref_e = "ro_ref(ed.vcoord)" if gpsro else "1.0"
        if gpsro:
            conn.create_function("ro_ref", 1, _ro_ref, deterministic=True)
        c_err_col = _num("cd.obs_error") if "obs_error" in ctl_cols else "NULL"
        e_err_col = _num("ed.obs_error") if "obs_error" in exp_cols else "NULL"
        c_oma_col = _num("cd.oma") if "oma" in ctl_cols else "NULL"
        e_oma_col = _num("ed.oma") if "oma" in exp_cols else "NULL"
        conn.execute(f"""
            CREATE TEMP TABLE c AS
            SELECT {kc}, ch.id_stn AS id_stn, ROUND(ch.lat, 4) AS klat,
                   ROUND(ch.lon, 4) AS klon, ch.lat AS lat, ch.lon AS lon,
                   ch.DATE AS date, ch.TIME AS time,
                   cd.varno AS varno, cd.vcoord AS vraw,
                   {vcoord_expr} AS vcoord_b,
                   {sp_sel_ctl} AS special, {c_codtyp} AS codtyp,
                   cd.flag AS flag, cd.omp AS omp, {c_oma_col} AS oma,
                   cd.obsvalue AS obs, {c_err_col} AS err, {ref_c} AS ref
            FROM ctl.header ch JOIN ctl.DATA cd USING(id_obs)
            WHERE cd.varno IN ({element}) AND {_is_num('cd.omp')}
              AND {_is_num('cd.obsvalue')}
              {VCOCRIT};
        """)
        conn.execute(f"""
            CREATE TEMP TABLE e AS
            SELECT {ke}, eh.id_stn AS id_stn, ROUND(eh.lat, 4) AS klat,
                   ROUND(eh.lon, 4) AS klon, eh.DATE AS date,
                   eh.TIME AS time, ed.varno AS varno, ed.vcoord AS vraw,
                   ed.omp AS omp, {e_oma_col} AS oma, ed.obsvalue AS obs,
                   {e_err_col} AS err, {ref_e} AS ref
            FROM exp.header eh JOIN exp.DATA ed USING(id_obs)
            WHERE ed.varno IN ({element}) AND {_is_num('ed.omp')}
              AND {_is_num('ed.obsvalue')};
        """)
        conn.execute(f"CREATE INDEX e_key ON e " f"({', '.join(key_aliases(spec))});")
        repeats = {
            names[0]: count_repeats(conn, "c", spec),
            names[1]: count_repeats(conn, "e", spec),
        }

        def _terms(x: str) -> Tuple[str, str, str, str, str]:
            """omp, oma, obs, err and quality gates of one side."""
            if not gpsro:
                return (f"{x}.omp", f"{x}.oma", f"{x}.obs", f"{x}.err", "")
            gates = (
                f" AND {x}.vraw > -1000 AND {x}.vraw < 100000"
                f" AND ({x}.obs - {x}.omp) > 0"
                f" AND ({x}.obs - {x}.omp) < 500"
                f" AND {x}.obs / {x}.ref > 0.3"
                f" AND {x}.obs / {x}.ref < 3"
                f" AND {x}.omp / {x}.ref > -0.05"
                f" AND {x}.omp / {x}.ref < 0.05"
                f" AND ({x}.err IS NULL OR ({x}.err / {x}.ref > 0"
                f" AND {x}.err / {x}.ref < 1))"
            )
            oma = (
                f"CASE WHEN {x}.oma / {x}.ref > -0.05 AND "
                f"{x}.oma / {x}.ref < 0.05 THEN {x}.oma / {x}.ref END"
            )
            return (
                f"({x}.omp / {x}.ref)",
                oma,
                f"({x}.obs / {x}.ref)",
                f"({x}.err / {x}.ref)",
                gates,
            )

        c_omp, c_oma, c_obs, c_err, c_gates = _terms("c")
        e_omp, e_oma, e_obs, e_err, e_gates = _terms("e")
        # An observation is the same in both runs when its station,
        # position, time, varno AND level agree -- the key scatter uses.
        # Matching by rank inside the profile, as this module once did,
        # pairs the wrong levels as soon as one run drops a level the
        # other keeps, and loses the top of every profile.
        conn.execute(f"""
            CREATE TEMP TABLE pairs AS
            SELECT c.id_stn AS id_stn, c.lat AS lat, c.lon AS lon,
                   c.varno AS varno, c.vcoord_b AS vcoord_b, c.flag AS flag,
                   c.special AS special, c.codtyp AS codtyp,
                   {c_omp} AS c_omp, {e_omp} AS e_omp,
                   {c_oma} AS c_oma, {e_oma} AS e_oma,
                   {c_obs} AS c_obs, {e_obs} AS e_obs,
                   {c_err} AS c_err, {e_err} AS e_err
            FROM c JOIN e ON {join_on}
            WHERE 1=1 {c_gates} {e_gates};
        """)
        n_pairs = conn.execute("SELECT COUNT(*) FROM pairs;").fetchone()[0]
        if not n_pairs:
            return {"pairs": 0, "repeats": repeats}

        conn.execute(_DDL_PAIRS)
        stn_sel, stn_group = _station_select(stn_label, family, "codtyp")
        # O-A is compared only where both runs have it, and counted apart:
        # a pair missing its O-A still counts fully for O-P
        both_oma = "c_oma IS NOT NULL AND e_oma IS NOT NULL"
        both_err = "c_err IS NOT NULL AND e_err IS NOT NULL"
        for combo in combos:
            cond = combo["cond"].replace("c.lat", "lat").replace("c.lon", "lon")
            cond = cond.replace("c.flag", "flag").replace("c.vcoord_b", "vcoord_b")
            chan_sel = "'join'" if combo["channel"] == "join" else "vcoord_b"
            terms = [t for t in (stn_group, "special", "varno", chan_sel, "lat_bin") if t]
            conn.execute(f"""
                INSERT INTO zone_pairs ({_PAIR_COLS})
                SELECT '{combo['region']}', '{combo['flag']}',
                       '{combo['channel']}', '{combo['land_ocean']}',
                       {stn_sel}, special, varno, {chan_sel},
                       {_bin_lat('lat', lat_band)} AS lat_bin, {date_int},
                       COUNT(*),
                       SUM(CASE WHEN {both_oma} THEN 1 ELSE 0 END),
                       SUM(CASE WHEN {both_err} THEN 1 ELSE 0 END),
                       SUM(c_omp), SUM(c_omp*c_omp),
                       SUM(e_omp), SUM(e_omp*e_omp), SUM(c_omp*e_omp),
                       SUM(CASE WHEN {both_oma} THEN c_oma END),
                       SUM(CASE WHEN {both_oma} THEN c_oma*c_oma END),
                       SUM(CASE WHEN {both_oma} THEN e_oma END),
                       SUM(CASE WHEN {both_oma} THEN e_oma*e_oma END),
                       SUM(CASE WHEN {both_oma} THEN c_oma*e_oma END),
                       SUM(c_obs), SUM(e_obs),
                       SUM(CASE WHEN {both_err} THEN c_err END),
                       SUM(CASE WHEN {both_err} THEN e_err END)
                FROM pairs
                WHERE 1=1 {id_stn_sql} AND {cond}
                GROUP BY {", ".join(terms)};
            """)
        _combine_rows(new_db, mem_uri, "zone_pairs", _PAIR_COLS, ddl=_DDL_PAIRS, module="zone")
        if stn_label and stn_label != "join" and not _is_composite(family):
            _save_members(
                new_db,
                stn_label,
                conn.execute(
                    f"SELECT DISTINCT id_stn FROM pairs WHERE 1=1 " f"{id_stn_sql};"
                ).fetchall(),
            )
        return {"pairs": n_pairs, "repeats": repeats}


# ─────────────────────────────────────────────────────────────────────────────
# The same two tables, read by the unified reader (pikobs.reader)
# ─────────────────────────────────────────────────────────────────────────────

def _use_reader() -> bool:
    """The unified reader, unless PIKOBS_ZONE_OLD_SQL=1 asks for zone's own
    SQL (kept for one release, to compare)."""
    return os.environ.get("PIKOBS_ZONE_OLD_SQL", "") != "1"


def _zone_single(*args, **kwargs):
    return (create_zone_single_reader if _use_reader() else create_zone_single)(*args, **kwargs)


def _zone_matched(*args, **kwargs):
    return (create_zone_matched_reader if _use_reader() else create_zone_matched)(*args, **kwargs)


def _columns_of(path):
    """(header columns, data columns) of one file, lower case; empty sets
    when it cannot be read."""
    try:
        with work_db(attach={"db": path}) as (conn, _):
            return ({str(c).lower() for c in table_columns(conn, "HEADER", "db")},
                    {str(c).lower() for c in table_columns(conn, "DATA", "db")})
    except Exception:
        return set(), set()


def _zv(x):
    """A value of the reader's rows as zone stores it: NULL for NaN."""
    return None if x is None or (isinstance(x, float) and x != x) else x


def _zn(x) -> int:
    x = _zv(x)
    return int(x) if x is not None else 0


def _zone_asks(family, regions, flags, channels, land_oceans, id_stn_sql, varnos, lat_band,
               stn_label, special_on, gpsro, head, data, match, key=()):
    """The Asks of one zone pass -- one without the channel when 'join' is
    asked, one by channel for 'all' and the single channels -- and the
    names of the five values (omp, oma, obs, bcorr, err) in their rows."""
    from pikobs.reader.reader import Ask, cells
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    vcoord_expr = (VCOORD or "").strip() or "vcoord"
    codtyp_col = "codtyp" if "codtyp" in head else "NULL"
    stn_sel, stn_group = _station_select(stn_label, family, codtyp_col)
    group = [("stn", stn_sel)]
    if stn_group and stn_group not in ("NULL", stn_sel):
        group.append(("stn_key", stn_group))        # one row per codtyp, as zone groups
    group.append(("varno", "varno"))
    lat_bin = ("lat_bin", _bin_lat("lat", lat_band))
    where = f"{_is_num('obsvalue')} AND {_is_num('omp')}"
    values = ("obsvalue", "omp", "oma", "bias_corr", "obs_error")
    names = {"omp": "omp", "oma": "oma", "obs": "obsvalue", "bcorr": "bias_corr", "err": "obs_error"}
    exprs, functions, pre = (), (), ()
    if gpsro:
        # ro_ref once per observation (pre), read as d.ref everywhere
        t = {k: v.replace("ro_ref(d.vcoord)", "d.ref")
             for k, v in _ro_terms("d", "obs_error" in data, "oma" in data).items()}
        pre = (("ref", "ro_ref(vcoord)"),)
        where += t["gates"]
        exprs = (("omp_r", t["omp"]), ("oma_r", t["oma"]), ("obs_r", t["obs"]), ("err_r", t["err"]))
        functions = (("ro_ref", 1, _ro_ref),)
        values = ("bias_corr",)
        names = {"omp": "omp_r", "oma": "oma_r", "obs": "obs_r", "bcorr": "bias_corr", "err": "err_r"}
    if id_stn_sql and id_stn_sql.strip():
        where += f" {id_stn_sql}"
    common = dict(family=family, cells=cells(regions, flags, land_oceans or ("all",)),
                  varnos=tuple(int(v) for v in varnos or ()), values=values, exprs=exprs,
                  functions=functions, match=match, special_column=bool(special_on), where=where,
                  pre=pre)
    if key:
        common["key"] = tuple(key)
    if match == "on":
        common["flag_on"] = "ctl"            # zone: the cell of a pair is the control's
    else:
        common.update(counts=(("all", "1 = 1"), ("rej", "(flag & 512) = 512"),
                              ("acc", "(flag & 4096) = 4096")),
                      distinct="id_obs")
    asks = {"join": None, "chan": None}
    if "join" in channels:
        asks["join"] = Ask(group=tuple(group + [lat_bin]), **common)
    if any(c != "join" for c in channels):
        asks["chan"] = Ask(group=tuple(group + [("vcoord_b", vcoord_expr), lat_bin]), **common)
    return asks, names


def _zone_rows(got, kind, channels):
    """(channel token, row) of one Ask's rows, a single channel kept only
    where it is that channel."""
    recs = got.rows.to_dict("records")
    tokens = ["join"] if kind == "join" else [c for c in channels if c != "join"]
    for tok in tokens:
        for r in recs:
            if kind == "chan" and tok != "all":
                vb = _zv(r["vcoord_b"])
                if vb is None or float(vb) != float(tok):
                    continue
            yield tok, r


_ZONE_COLS_IN = ("region, flag, channel_mode, land_ocean, id_stn, special, varno, vcoord, lat, "
                 "date, n, n_omp, n_oma, n_err, s_omp, s2_omp, s_oma, s2_oma, s_obs, s2_obs, "
                 "s_bcorr, s2_bcorr, s_err, s2_err, nrej, nacc, nprofile")
_ZONE_PAIR_COLS_IN = ("region, flag, channel_mode, land_ocean, id_stn, special, varno, vcoord, "
                      "lat, date, n, n_oma, n_err, c_omp, c2_omp, e_omp, e2_omp, ce_omp, "
                      "c_oma, c2_oma, e_oma, e2_oma, ce_oma, c_obs, e_obs, c_err, e_err")


def create_zone_single_reader(
    family: str,
    new_db: str,
    cycle_file: str,
    regions,
    flags,
    channels,
    land_oceans,
    id_stn_sql: str,
    varnos,
    lat_band: float,
    pathwork: str,
    stn_label: Optional[str] = None,
    special_on: bool = True,
    gpsro: bool = False,
) -> Optional[int]:
    """create_zone_single, read by pikobs.reader: the same rows of zone."""
    from pikobs.reader.reader import read_cycle
    if not os.path.isfile(cycle_file):
        print(f"[zone] missing file, skipped: {cycle_file}", file=sys.stderr, flush=True)
        return None
    date_match = re.search(r"(\d{10})", os.path.basename(cycle_file))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {cycle_file}")
    date_int = int(date_match.group(1))
    head, data = _columns_of(cycle_file)
    if not data:
        print(f"[zone] no DATA table in {cycle_file}", file=sys.stderr, flush=True)
        return None
    asks, nm = _zone_asks(family, regions, flags, channels, land_oceans, id_stn_sql, varnos,
                          lat_band, stn_label, special_on, gpsro, head, data, "off")
    out = []
    for kind, ask in asks.items():
        if ask is None:
            continue
        got = read_cycle(cycle_file, None, ask, date_int, pathwork=pathwork, module="zone")
        if got is None:
            return None
        for tok, r in _zone_rows(got, kind, channels):
            n = _zn(r["kc_all"])
            if not n:
                continue

            def s(name, p):
                col = nm[name]
                return _zv(r[f"{p}_{col}"]) if _zn(r[f"nc_{col}"]) else None

            out.append((r["region"], r["flag"], tok, r["land_ocean"], r["stn"],
                        r["special"] if special_on else "all", _zv(r["varno"]),
                        "join" if kind == "join" else _zv(r["vcoord_b"]), _zv(r["lat_bin"]),
                        date_int, n, n, _zn(r[f"nc_{nm['oma']}"]), _zn(r[f"nc_{nm['err']}"]),
                        s("omp", "sc"), s("omp", "sc2"), s("oma", "sc"), s("oma", "sc2"),
                        s("obs", "sc"), s("obs", "sc2"), s("bcorr", "sc"), s("bcorr", "sc2"),
                        s("err", "sc"), s("err", "sc2"),
                        _zn(r["kc_rej"]), _zn(r["kc_acc"]), _zn(r["nuniqc"])))
    with work_db(attach={"db": cycle_file}) as (conn, mem_uri):
        conn.execute(_DDL_SINGLE)
        conn.executemany(f"INSERT INTO zone ({_ZONE_COLS_IN}) VALUES ({', '.join('?' * 27)});", out)
        _combine_rows(new_db, mem_uri, "zone", _SINGLE_COLS, ddl=_DDL_SINGLE, module="zone")
        if stn_label and stn_label != "join" and not _is_composite(family):
            _save_members(
                new_db,
                stn_label,
                conn.execute(
                    f"SELECT DISTINCT id_stn FROM db.header WHERE 1=1 " f"{id_stn_sql};"
                ).fetchall(),
            )
    return len(out)


def _zone_join_of(rows):
    """The 'join' rows of a matched pass from its rows by channel: every
    count and sum added over the channels."""
    import pandas as pd
    sums = [c for c in rows.columns
            if re.match(r"^(nc|sc|sc2|ne|se|se2|sce|nallc|nalle)_", c)]
    keys = [c for c in rows.columns if c not in sums and c != "vcoord_b"]
    if rows.empty:
        return []
    g = rows.fillna({c: 0 for c in sums}).groupby(keys, dropna=False, sort=False)[sums].sum()
    return g.reset_index().to_dict("records")


def create_zone_matched_reader(
    family: str,
    new_db: str,
    ctl_file: str,
    exp_file: str,
    regions,
    flags,
    channels,
    land_oceans,
    id_stn_sql: str,
    varnos,
    lat_band: float,
    pathwork: str,
    stn_label: Optional[str] = None,
    special_on: bool = True,
    gpsro: bool = False,
    match_fields=(),
    names=None,
):
    """create_zone_matched, read by pikobs.reader: the same rows of
    zone_pairs and the same report of the pairing."""
    from pikobs.reader.reader import read_cycle
    for path in (ctl_file, exp_file):
        if not os.path.isfile(path):
            print(f"[zone] missing file, skipped: {path}", file=sys.stderr, flush=True)
            return None
    date_match = re.search(r"(\d{10})", os.path.basename(ctl_file))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {ctl_file}")
    date_int = int(date_match.group(1))
    names = tuple(names or ("control", "experience"))
    head_c, data_c = _columns_of(ctl_file)
    head_e, data_e = _columns_of(exp_file)
    if not data_c or not data_e:
        return None
    # a column in the expressions only when both runs have it
    asks, nm = _zone_asks(family, regions, flags, channels, land_oceans, id_stn_sql, varnos,
                          lat_band, stn_label, special_on, gpsro, head_c & head_e,
                          data_c & data_e, "on", key=match_fields)
    # one read: with pairs everything is a sum, so 'join' is the sum of the channels
    derive_join = asks["join"] is not None and asks["chan"] is not None
    if derive_join:
        asks = {"join": None, "chan": asks["chan"]}
    out, info = [], {}
    for kind, ask in asks.items():
        if ask is None:
            continue
        got = read_cycle(ctl_file, exp_file, ask, date_int, pathwork=pathwork, module="zone")
        if got is None:
            return None
        info = got.info or info
        pieces = [(tok, r) for tok, r in _zone_rows(got, kind, channels)]
        if derive_join:
            pieces += [("join", r) for r in _zone_join_of(got.rows)]
        for tok, r in pieces:
            kind = "join" if tok == "join" else "chan"
            n = _zn(r[f"nc_{nm['omp']}"])
            if not n:
                continue
            no, ne = _zn(r[f"nc_{nm['oma']}"]), _zn(r[f"nc_{nm['err']}"])

            def g(name, p, cnt):
                return _zv(r[f"{p}_{nm[name]}"]) if cnt else None

            out.append((r["region"], r["flag"], tok, r["land_ocean"], r["stn"],
                        r["special"] if special_on else "all", _zv(r["varno"]),
                        "join" if kind == "join" else _zv(r["vcoord_b"]), _zv(r["lat_bin"]),
                        date_int, n, no, ne,
                        g("omp", "sc", n), g("omp", "sc2", n), g("omp", "se", n),
                        g("omp", "se2", n), g("omp", "sce", n),
                        g("oma", "sc", no), g("oma", "sc2", no), g("oma", "se", no),
                        g("oma", "se2", no), g("oma", "sce", no),
                        g("obs", "sc", n), g("obs", "se", n), g("err", "sc", ne), g("err", "se", ne)))
    repeats = {names[0]: (info.get("rep_keys_c", 0), info.get("rep_rows_c", 0)),
               names[1]: (info.get("rep_keys_e", 0), info.get("rep_rows_e", 0))}
    n_pairs = int(info.get("pairs", 0) or 0)
    if not n_pairs or not out:
        return {"pairs": 0, "repeats": repeats}
    with work_db(attach={"db": ctl_file}) as (conn, mem_uri):
        conn.execute(_DDL_PAIRS)
        conn.executemany(f"INSERT INTO zone_pairs ({_ZONE_PAIR_COLS_IN}) "
                         f"VALUES ({', '.join('?' * 27)});", out)
        _combine_rows(new_db, mem_uri, "zone_pairs", _PAIR_COLS, ddl=_DDL_PAIRS, module="zone")
        if stn_label and stn_label != "join" and not _is_composite(family):
            # the control's stations of the selection (zone kept those with a pair)
            _save_members(
                new_db,
                stn_label,
                conn.execute(
                    f"SELECT DISTINCT id_stn FROM db.header WHERE 1=1 " f"{id_stn_sql};"
                ).fetchall(),
            )
    return {"pairs": n_pairs, "repeats": repeats}


def _extract_task(task: Dict[str, Any]) -> Optional[int]:
    try:
        if task.get("ctl_file"):
            return _zone_matched(
                task["family"],
                task["db_new"],
                task["ctl_file"],
                task["exp_file"],
                task["regions"],
                task["flags"],
                task["channels"],
                task["land_oceans"],
                task["id_stn_sql"],
                task["varnos"],
                task["lat_band"],
                task["pathwork"],
                task["stn_label"],
                task.get("special_on", True),
                task.get("gpsro", False),
                task.get("match_fields") or (),
                task.get("names"),
            )
        return _zone_single(
            task["family"],
            task["db_new"],
            task["filein"],
            task["regions"],
            task["flags"],
            task["channels"],
            task["land_oceans"],
            task["id_stn_sql"],
            task["varnos"],
            task["lat_band"],
            task["pathwork"],
            task["stn_label"],
            task.get("special_on", True),
            task.get("gpsro", False),
        )
    except Exception:
        print(
            f"[zone] extraction failed for "
            f"{task.get('filein') or task.get('ctl_file')}:\n"
            f"{traceback.format_exc()}",
            file=sys.stderr,
            flush=True,
        )
        return None


def _index_task(path: str) -> Optional[str]:
    try:
        with open_result(path) as conn:
            for table in ("zone", "zone_pairs"):
                try:
                    conn.execute(
                        f"CREATE INDEX IF NOT EXISTS idx_{table} ON {table} "
                        f"(region, flag, channel_mode, land_ocean, varno, "
                        f"id_stn);"
                    )
                except Exception:
                    pass
        return path
    except Exception as exc:
        print(f"[zone] indexing {path} failed: {exc}", file=sys.stderr, flush=True)
        return None


# zone's extraction, which verifprofile uses as it is: its public names
extract_task = _extract_task
index_task = _index_task


# ─────────────────────────────────────────────────────────────────────────────
# Plot tasks
# ─────────────────────────────────────────────────────────────────────────────


def _region_lat_range(region: str) -> Tuple[float, float]:
    """The latitude span of a region: the x axis of all its figures."""
    try:
        lat1, lat2, _, _ = pikobs.regions(region)
        lo, hi = sorted((float(lat1), float(lat2)))
        return max(lo, -90.0), min(hi, 90.0)
    except Exception:
        return -90.0, 90.0


def family_levels(work_path, family, tags, date_start, date_end, matched: bool) -> List[float]:
    """Every level the family has in the period, over every selection.

    The figures of a family share this list, so a level sits on the same
    row in all of them and the cells keep the same size; a level with no
    data in one figure is simply left empty there.
    """
    table = "zone_pairs" if matched else "zone"
    levels = set()
    for tag in tags:
        path = db_path(work_path, family, tag, date_start, date_end)
        for (v,) in _distinct(
            path, table, f"SELECT DISTINCT vcoord FROM {table} " f"WHERE channel_mode != 'join';"
        ):
            try:
                levels.add(float(v))
            except (TypeError, ValueError):
                pass
    return sorted(levels)


def create_plot_tasks(
    work_path,
    families,
    tag,
    date_start,
    date_end,
    selectors,
    functions,
    matched: bool,
    names: Sequence[str],
    svg: bool,
    min_obs: int = MIN_OBS_PER_CELL,
    lat_band: float = 2.0,
    levels_by_family: Optional[Dict[str, List[float]]] = None,
    white_band=WHITE_BAND,
) -> List[Dict[str, Any]]:
    """One task per (family, selection, varno, function), read back from
    what the extraction really produced."""
    table = "zone_pairs" if matched else "zone"
    tasks = []
    for family in families:
        path = db_path(work_path, family, tag, date_start, date_end)
        # a zonal section needs at least two latitude bands: a single
        # radiosonde sits at one point, and its "section" is one column
        # stretched across the figure, which says nothing
        rows = _distinct(
            path,
            table,
            f"SELECT region, flag, channel_mode, land_ocean, "
            f"id_stn, special, varno, COUNT(DISTINCT lat) "
            f"FROM {table} GROUP BY region, flag, channel_mode, "
            f"land_ocean, id_stn, special, varno;",
        )
        single = [r for r in rows if (r[7] or 0) < 2]
        if single:
            word = "type" if _is_composite(family) else "station"
            print(
                f"[zone] {family}: {len(single)} selection(s) skipped, "
                f"a single latitude band is not a section; "
                f"ID_STN=(join) or a prefix groups them:",
                flush=True,
            )
            for r in single[:15]:
                region, flag, chan, lo, id_stn, special, varno = r[:7]
                sp = _special_label(family, special)
                extra = f"  method {sp}" if sp != "all" else ""
                print(
                    f"[zone]     {word} {id_stn:<24s} region {region}  "
                    f"flags {flag}  varno {varno}{extra}",
                    flush=True,
                )
            if len(single) > 15:
                print(f"[zone]     ... (+{len(single) - 15} more)", flush=True)
        rows = [r[:7] for r in rows if (r[7] or 0) >= 2]
        for region, flag, chan, lo, id_stn, special, varno in rows:
            for function in functions:
                tasks.append(
                    {
                        "pathwork": work_path,
                        "db_file": path,
                        "family": family,
                        "region": region,
                        "flag": flag,
                        "channel_mode": chan,
                        "land_ocean": lo,
                        "id_stn": id_stn,
                        "special": special if special is not None else "all",
                        "stn_tag": _safe(id_stn),
                        "varno": varno,
                        "function": function,
                        "datestart": date_start,
                        "dateend": date_end,
                        "names": list(names),
                        "matched": matched,
                        "svg": svg,
                        "min_obs": min_obs,
                        "lat_band": lat_band,
                        "white_band": white_band,
                        # the latitudes of the region: Canada from 45 to 90,
                        # not on a globe three quarters empty. Runs and
                        # experiences of a region share that frame, band by
                        # band (a polygon falls back to the whole globe)
                        "lat_range": _region_lat_range(region),
                        "family_levels": (levels_by_family or {}).get(family, []),
                    }
                )
    return tasks


def viewer_items(tasks, results) -> List[Dict[str, str]]:
    items = []
    for task, path in zip(tasks, results):
        if not path:
            continue
        items.append(
            {
                "experience": task.get("experience", task["names"][-1]),
                "family": task["family"],
                "fonction": task["function"],
                "region": task["region"],
                "flag_criteria": task["flag"],
                "id_stn": task["id_stn"],
                "channel": str(task["channel_mode"]),
                "land_ocean": task["land_ocean"],
                "varno": str(task["varno"]),
                "special": _special_label(task["family"], task["special"]),
                "match": task.get("match_mode", ""),
                "filename": os.path.basename(path),
            }
        )
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────


def _report_timing(timing: Dict[str, Any], pathwork: str) -> None:
    sec = timing["seconds"]
    print("[zone] -------------------- run time --------------------", flush=True)
    print(
        f"[zone] input        {fmt_bytes(timing['input_bytes']):>10s}"
        f"   {timing['input_files']} files, {timing['cycles']} cycles, "
        f"{timing['runs']} run(s)",
        flush=True,
    )
    for phase in ("extraction", "scales", "plots"):
        if phase in sec:
            print(f"[zone] {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(
        f"[zone] total        {sec['total']:>8.1f} s   "
        f"({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
        flush=True,
    )
    try:
        with open(os.path.join(pathwork, "zone_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError as exc:
        print(f"[zone] could not write zone_timing.json: {exc}", file=sys.stderr, flush=True)


def _zone_options(
    regions,
    flags_criteria,
    functions,
    channel,
    land_ocean,
    id_stn,
    varnos,
    control,
    runs,
    match,
    min_obs,
    special_on,
    families,
):
    """The selections, cleaned and said once in the log."""

    regions = _split_tokens(regions)
    flags = _split_tokens(flags_criteria)
    functions = _split_tokens(functions) or ["omp"]
    channels = _split_tokens(channel) or ["all"]
    # a zonal section needs the levels on its y axis: 'join' collapses
    # them into one row, and the figure would be a single stripe
    if "join" in channels:
        print(
            "[zone] note: CHANNEL 'join' dropped, a section needs its "
            "levels on the y axis; use 'all' or a list of levels",
            flush=True,
        )
        channels = [c for c in channels if c != "join"] or ["all"]
    land_oceans = [
        lo for lo in (_split_tokens(land_ocean) or ["all"]) if lo in LAND_OCEAN_CHOICES
    ] or ["all"]
    stn_tokens = parse_station_tokens(id_stn)
    varnos = _split_tokens(varnos)

    all_runs = ([control] if control else []) + list(runs)
    # with the option off the task never gets a control file, so the
    # extraction takes its unmatched branch and nothing else changes
    matched = control is not None and match
    names = ([control[0]] if control else []) + [n for n, _ in runs]

    print(f"[zone] runs: {', '.join(n for n, _ in all_runs)}", flush=True)

    if control is not None:
        how = (
            "matched observation by observation"
            if match
            else "compared, NOT matched: each run keeps all its observations, " "t-test and F-test"
        )
        print(
            f"[zone] control: {control[0]}  |  {how} with: " f"{', '.join(n for n, _ in runs)}",
            flush=True,
        )
    print(f"[zone] regions: {regions}", flush=True)
    print(f"[zone] flags_criteria: {flags}", flush=True)
    print(f"[zone] fonction: {functions}", flush=True)
    print(f"[zone] id_stn tokens: {stn_tokens}", flush=True)
    print(f"[zone] channel tokens: {channels}", flush=True)
    print(f"[zone] land_ocean: {land_oceans}", flush=True)
    print(f"[zone] cells with fewer than {min_obs} observations are left " f"empty", flush=True)
    print(
        f"[zone] special column: {'on' if special_on else 'off'} "
        f"(sw: one figure per wind method, IR / WV)",
        flush=True,
    )
    for fam in families:
        _, vcoord, _, _, _, vcotyp = pikobs.family(fam)
        print(f"[zone] {fam}: vcoord = {vcoord.strip()}  ({vcotyp})", flush=True)

    return regions, flags, functions, channels, land_oceans, stn_tokens, varnos, all_runs, matched


def _zone_tasks(
    runs,
    matched,
    control,
    families,
    stn_tokens,
    cycle_list,
    pathwork,
    datestart,
    dateend,
    regions,
    flags,
    channels,
    land_oceans,
    special_on,
    varnos,
    lat_band,
    match_spec,
    off_cmp: bool = False,
    off_modes=("off",),
):
    """The comparisons, and one extraction task per run, cycle and family."""

    # one comparison per experience against the control: MATCH on (its
    # pairs) and / or off (the two runs, each with all its observations);
    # without a control, each run on its own
    comparisons = []
    if matched:
        comparisons += [{"label": f"{name} vs {control[0]}", "tag": f"{control[0]}_vs_{name}",
                         "names": [control[0], name], "path": path, "mode": "on"}
                        for name, path in runs]
    if off_cmp:
        # off and no draw the same two runs apart; no without any test
        comparisons += [{"label": f"{name} vs {control[0]}", "tag": name, "ctl_tag": control[0],
                         "names": [control[0], name], "path": path, "mode": mode}
                        for mode in off_modes
                        for name, path in runs]
    if control is None:
        comparisons = [{"label": name, "tag": name, "names": [name], "path": path, "mode": ""}
                       for name, path in runs]
    # what is extracted: the pairs of each MATCH on comparison, and every run
    # alone -- the control too -- for MATCH off
    extractions = [(c["tag"], c["path"], True) for c in comparisons if c["mode"] == "on"]
    singles = ([control] + list(runs)) if off_cmp else (list(runs) if control is None else [])
    extractions += [(name, path, False) for name, path in singles]

    # the station selections: 'all' is one group per station, found in
    # the data itself; every other token is one group under its own name
    # resolved per family: the same token means an instrument type on
    # ai or ua and a station everywhere else
    selectors_by_family = {f: _selections(stn_tokens, f) for f in families}

    tasks = []
    for ext_tag, ext_path, paired in extractions:
        for cycle in cycle_list:
            for family in families:
                for sel in selectors_by_family[family]:
                    base = {
                        "family": family,
                        "db_new": db_path(
                            pathwork, family, f"{ext_tag}_{sel.tag}", datestart, dateend
                        ),
                        "regions": regions,
                        "flags": flags,
                        "channels": channels,
                        "land_oceans": land_oceans,
                        "id_stn_sql": sel.sql(),
                        "stn_label": sel.label,
                        "special_on": special_on,
                        "varnos": varnos,
                        "lat_band": lat_band,
                        "pathwork": pathwork,
                    }
                    if paired:
                        base["ctl_file"] = cycle_path(control[1], cycle, family)
                        base["match_fields"] = match_spec.fields
                        base["names"] = (control[0], "experience")
                        base["exp_file"] = cycle_path(ext_path, cycle, family)
                    else:
                        base["filein"] = cycle_path(ext_path, cycle, family)
                    tasks.append(base)

    return comparisons, selectors_by_family, tasks


def _zone_viewer(items, pathwork, matched, all_runs, control, datestart, dateend, families,
                 both: bool = False):
    """The viewer: one page over every cross-section written."""

    keys = [
        "experience",
        "family",
        "fonction",
        "region",
        "flag_criteria",
        "id_stn",
        "special",
        "channel",
        "land_ocean",
        "varno",
    ] + (["match"] if both else [])
    print(f"[zone] viewer selectors: {keys}", flush=True)
    from pikobs.configobs.special_family import special_key_label
    from pikobs.web.viewer import docs_url

    generate_web(
        items,
        keys,
        os.path.join(pathwork, "pikobs_zone_viewer.html"),
        title="Pikobs Zone Cross-Section Viewer",
        subtitle=(
            (
                "Did the experience change anything, and at which latitude and "
                "height? Each cell is <b>Exp minus Ctl</b> on the same "
                "observations, matched one by one before anything is summed. "
                "<b>Red means Exp is better, blue that Ctl is</b>; white is a "
                "change inside the white band, and the two test panels say "
                "whether a change is larger than noise (how the tests work: "
                f"<a href=\"{docs_url('stats.html')}\" style=\"color:var(--accent)\">"
                "the statistics page</a>). The last panel is the sample behind "
                "each cell, the same in both runs."
                if matched
                else "Where are the departures of a run large, biased, or thin? "
                "Latitude across, the vertical coordinate of the family down, "
                "and in each cell the sigma, the mean -- red above zero, blue "
                "below, white inside the white band -- and the number of "
                "observations. Cells with too few observations stay empty."
            )
            + runs_block(all_runs, control, (datestart, dateend))
        ),
        image_subdir_key="family",
        key_labels={
            "channel": level_selector_label(families),
            "land_ocean": "Surface",
            "special": special_key_label(families),
        },
        issues_url="https://gitlab.science.gc.ca/dlo001/Pikobs",
    )


def _extract_zone(tasks, n_cpu, client, timing, match_spec):
    """Extraction: every cycle of every run into its database, then indexed."""

    t0 = time.time()
    print(f"[zone] extraction: {len(tasks)} tasks, {n_cpu} worker(s)", flush=True)
    res = run_tasks(_extract_task, [(t,) for t in tasks], client, label="extraction")
    timing["seconds"]["extraction"] = time.time() - t0
    print(
        f"[zone] extraction time: "
        f"{timing['seconds']['extraction']:.1f}s "
        f"({sum(r is not None for r in res)}/{len(tasks)} files)",
        flush=True,
    )
    # one line per family when the pairing key was not unique
    from pikobs.match import add_counts, repeat_warning

    repeats = {}
    for t, r in zip(tasks, res):
        if isinstance(r, dict):
            add_counts(repeats.setdefault(t["family"], {}), r.get("repeats"))
    for fam in sorted(repeats):
        msg = repeat_warning("zone", fam, match_spec, repeats[fam])
        if msg:
            print(msg, file=sys.stderr, flush=True)

    dbs = sorted({t["db_new"] for t in tasks})
    run_tasks(_index_task, [(d,) for d in dbs], client, label="indexing")


def _plan_zone_figures(
    families,
    pathwork,
    comparisons,
    selectors_by_family,
    datestart,
    dateend,
    matched,
    functions,
    svg,
    min_obs,
    lat_band,
    white_band,
    plot_tasks,
):
    """The cross-sections to draw, of each comparison or run."""

    # one grid per family: the same latitude bands and the same levels
    # in every figure, so a cell has the same size everywhere and two
    # figures can be compared by flipping between them
    # the grid of a family is shared by every experience as well, so
    # two comparisons can be flipped against each other cell by cell
    # MATCH on and off share the axis too: the levels of both, so a level
    # sits on the same row when the viewer flips between them
    def _levels(f):
        sel = selectors_by_family[f]
        on = [f"{c['tag']}_{s.tag}" for c in comparisons if c["mode"] == "on" for s in sel]
        alone = [f"{t}_{s.tag}" for c in comparisons if c["mode"] != "on"
                 for t in [c["tag"]] + ([c["ctl_tag"]] if c.get("ctl_tag") else []) for s in sel]
        return sorted(set(family_levels(pathwork, f, on, datestart, dateend, True) if on else [])
                      | set(family_levels(pathwork, f, alone, datestart, dateend, False)
                            if alone else []))

    levels_by_family = {f: _levels(f) for f in families}
    for comp in comparisons:
        for family in families:
            for sel in selectors_by_family[family]:
                new = create_plot_tasks(
                    pathwork,
                    [family],
                    f"{comp['tag']}_{sel.tag}",
                    datestart,
                    dateend,
                    [sel],
                    functions,
                    comp["mode"] == "on",
                    comp["names"],
                    svg,
                    min_obs,
                    lat_band,
                    levels_by_family,
                    white_band,
                )
                for t in new:
                    t["experience"] = comp["label"]
                    t["match_mode"] = comp["mode"]
                    if comp["mode"] in ("off", "no"):
                        # the experience's figure reads the control's cells
                        # too, from its own database
                        t["compare_off"] = True
                        t["db_ctl"] = db_path(pathwork, family, f"{comp['ctl_tag']}_{sel.tag}",
                                              datestart, dateend)
                plot_tasks += new

    return plot_tasks


def _shared_scales(plot_tasks, client, timing):
    """One colour scale per group of figures that are read together."""

    # the colour scales of a group are shared: every figure of the
    # same family, varno and function takes the largest need of the
    # group, so a colour means the same value in all of them
    t0 = time.time()
    extremes = run_tasks(zone_scale_task, [(t,) for t in plot_tasks], client, label="scales")
    groups: Dict[tuple, Dict[str, float]] = {}
    for task, ext in zip(plot_tasks, extremes):
        if not ext:
            continue
        g = groups.setdefault(scale_group(task), {})
        for key, value in ext.items():
            g[key] = max(g.get(key, 0.0), float(value))
    for task in plot_tasks:
        task["scales"] = groups.get(scale_group(task), {})
    timing["seconds"]["scales"] = time.time() - t0
    print(
        f"[zone] colour scales: {len(groups)} group(s) shared "
        f"(family x varno x fonction x region), "
        f"{timing['seconds']['scales']:.1f}s",
        flush=True,
    )


def _draw_zone_figures(plot_tasks, client, timing):
    """Draw the cross-sections."""

    t0 = time.time()
    print(f"[zone] plots: {len(plot_tasks)} tasks", flush=True)
    results = run_tasks(zone_plot_task, [(t,) for t in plot_tasks], client, label="plots")
    timing["seconds"]["plots"] = time.time() - t0
    print(
        f"[zone] plot time: {timing['seconds']['plots']:.1f}s "
        f"({sum(r is not None for r in results)}/{len(plot_tasks)})",
        flush=True,
    )

    return results


def make_zone(
    runs,
    pathwork,
    datestart,
    dateend,
    regions,
    families,
    flags_criteria,
    functions,
    varnos,
    lat_band,
    id_stn,
    channel,
    land_ocean,
    n_cpu,
    control=None,
    svg: bool = False,
    min_obs: int = MIN_OBS_PER_CELL,
    special_on: bool = True,
    white_band=WHITE_BAND,
    match: bool = True,
) -> int:
    """Read the cycles, aggregate, draw the cross-sections."""
    # MATCH: on, off, or the fields of the key -- pikobs.match decides.
    # Past this point match is True / False as before; the key travels
    # in match_spec.
    from pikobs.match import parse_modes

    # MATCH: on, off, no (or empty: no test), several at once -- each asked
    # mode is drawn, a switch in the viewer between them
    modes, match_spec = parse_modes(match)
    match = "on" in modes
    both = len(modes) > 1

    regions, flags, functions, channels, land_oceans, stn_tokens, varnos, all_runs, matched = (
        _zone_options(
            regions,
            flags_criteria,
            functions,
            channel,
            land_ocean,
            id_stn,
            varnos,
            control,
            runs,
            match,
            min_obs,
            special_on,
            families,
        )
    )
    if not check_input_files(all_runs, families, datestart, dateend, "zone"):
        return 1
    t_start = time.time()
    cycle_list = _cycles(datestart, dateend)
    n_input, input_bytes = input_size(all_runs, families, cycle_list)
    timing: Dict[str, Any] = {
        "datestart": datestart,
        "dateend": dateend,
        "cycles": len(cycle_list),
        "families": list(families),
        "runs": len(all_runs),
        "regions": regions,
        "flags": flags,
        "fonction": functions,
        "id_stn": stn_tokens,
        "channel": channels,
        "land_ocean": land_oceans,
        "lat_band": lat_band,
        "matched": matched,
        "svg": svg,
        "min_obs": min_obs,
        "special_column": special_on,
        "n_cpus": n_cpu,
        "input_files": n_input,
        "input_bytes": input_bytes,
        "seconds": {},
    }
    for family in families:
        pikobs.delete_create_folder(pathwork, family)
    # MATCH off with a control: each run alone, every observation of it,
    # and the control beside each experience (Welch and F)
    off_cmp = control is not None and ("off" in modes or "no" in modes)
    comparisons, selectors_by_family, tasks = _zone_tasks(
        runs,
        matched,
        control,
        families,
        stn_tokens,
        cycle_list,
        pathwork,
        datestart,
        dateend,
        regions,
        flags,
        channels,
        land_oceans,
        special_on,
        varnos,
        lat_band,
        match_spec,
        off_cmp,
        tuple(m for m in ("off", "no") if m in modes),
    )
    client, dask_dir = start_workers(n_cpu, "zone")
    plot_tasks: List[Dict[str, Any]] = []
    results: List[Any] = []
    try:

        _extract_zone(tasks, n_cpu, client, timing, match_spec)
        plot_tasks = _plan_zone_figures(
            families,
            pathwork,
            comparisons,
            selectors_by_family,
            datestart,
            dateend,
            matched,
            functions,
            svg,
            min_obs,
            lat_band,
            white_band,
            plot_tasks,
        )
        if not plot_tasks:
            print(
                "[zone] WARNING: nothing to plot, check the selectors.",
                file=sys.stderr,
                flush=True,
            )
            return 1
        _shared_scales(plot_tasks, client, timing)
        results = _draw_zone_figures(plot_tasks, client, timing)
    finally:
        stop_workers(client, dask_dir)
    items = viewer_items(plot_tasks, results)
    if not items:
        print("[zone] ERROR: no figure was produced.", file=sys.stderr, flush=True)
        return 1
    _zone_viewer(items, pathwork, matched, all_runs, control, datestart, dateend, families,
                 both=both)

    timing["seconds"]["total"] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"[zone] done -- output in: {pathwork}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def arg_call() -> None:
    import argparse

    p = argparse.ArgumentParser(
        prog="pikobs-zone", description="Zonal cross-sections: latitude against the vertical."
    )
    p.add_argument("--path_control_files", default=None)
    p.add_argument("--control_name", default=None)
    p.add_argument("--path_experience_files", nargs="+", default=[])
    p.add_argument("--experience_name", nargs="+", default=[])
    p.add_argument("--pathwork", default=None)
    p.add_argument("--datestart", default=None)
    p.add_argument("--dateend", default=None)
    p.add_argument("--region", nargs="+", default=["Monde"])
    p.add_argument("--family", nargs="+", default=[])
    p.add_argument("--flags_criteria", nargs="+", default=["all"])
    p.add_argument("--fonction", nargs="+", default=["omp"], choices=["omp", "oma", "obs_error"])
    p.add_argument("--varnos", nargs="*", default=[])
    p.add_argument(
        "--lat_band", default=2.0, type=float, help="Width of the latitude bands, in degrees."
    )
    # the name it had before (BOXSIZEY, from scatter's boxes): still accepted
    p.add_argument("--boxsizey", dest="lat_band", type=float, help=argparse.SUPPRESS)
    p.add_argument(
        "--id_stn",
        nargs="+",
        default=["join"],
        help="Tokens, one series of figures each: join, all, "
        "PREFIX, LIKE%%pattern, =EXACT, 'NAME (codtyp)'.",
    )
    p.add_argument(
        "--channel",
        "--vcoord",
        dest="channel",
        nargs="+",
        default=["all"],
        help="all (every level on the y axis), join (all levels "
        "in one row), or explicit levels.",
    )
    p.add_argument("--land_ocean", nargs="+", default=["all"], choices=list(LAND_OCEAN_CHOICES))
    p.add_argument(
        "--special_column",
        default="off",
        choices=["on", "off"],
        help="on: one figure per value of the family's special "
        "column (sw: wind method, IR / WV), as in scatter.",
    )
    p.add_argument(
        "--white_band",
        default=WHITE_BAND,
        help="Changes drawn white in the comparison: 'auto' (the "
        "default) whites everything under a tenth of the largest "
        "change of each panel, whatever the variable; a number fixes "
        "it, in the units of the variable.",
    )
    p.add_argument(
        "--min_obs",
        default=MIN_OBS_PER_CELL,
        type=int,
        help="A cell with fewer observations than this is left "
        "empty in the statistics panels: the sigma of one "
        "or two values is not a sigma. The count panel "
        "still shows them.",
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
    p.add_argument("--no_submit", action="store_true")

    args = p.parse_args()

    if "--boxsizey" in sys.argv:

        print(
            "[zone] --boxsizey is now --lat_band (LAT_BAND in the wrapper); "
            "the old name still works"
        )

    for arg in vars(args):
        print(f"--{arg} {getattr(args, arg)}", flush=True)

    paths = _split_tokens(args.path_experience_files)
    names = _split_tokens(args.experience_name)
    if not paths or not names or len(paths) != len(names):
        raise ValueError(
            "--path_experience_files and --experience_name must " "have the same number of entries"
        )
    for attr, flag in [
        ("pathwork", "--pathwork"),
        ("datestart", "--datestart"),
        ("dateend", "--dateend"),
        ("family", "--family"),
    ]:
        if getattr(args, attr) in (None, [], "undefined", ""):
            raise ValueError(f"{flag} is required")

    runs = [(n, p_.rstrip("/") or "/") for n, p_ in zip(names, paths)]
    control = None
    # a blank value ("" or " ") is no control: an empty variable in
    # the wrapper must not turn into a directory called ' '
    if args.path_control_files and args.path_control_files.strip():
        ctl_name = args.control_name or "control"
        if ctl_name in names:
            raise ValueError(f"the control and an experience share the name " f"'{ctl_name}'")
        control = (ctl_name, args.path_control_files.strip().rstrip("/") or "/")
    elif args.control_name and args.control_name.strip():
        # a name with no path is left over from a wrapper whose control was
        # emptied: no reason to stop the run for it
        print(
            f"[{'zone' if 'zone' in __name__ else 'cardio'}] note: "
            f"--control_name '{args.control_name}' ignored, there is no "
            f"--path_control_files",
            flush=True,
        )

    maybe_submit_to_pbs(args)
    sys.exit(
        make_zone(
            runs,
            args.pathwork,
            args.datestart,
            args.dateend,
            args.region,
            _split_tokens(args.family),
            args.flags_criteria,
            args.fonction,
            _split_tokens(args.varnos),
            args.lat_band,
            args.id_stn,
            args.channel,
            args.land_ocean,
            args.n_cpus,
            control,
            svg_enabled(args.svg),
            args.min_obs,
            args.special_column == "on",
            args.white_band,
            match=args.match,
        )
    )


if __name__ == "__main__":
    arg_call()
