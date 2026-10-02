#!/usr/bin/python3
# GENERATED -- this docstring is written by pikobs/build_doc/build_flags.py.
# Edit that file and run ./pikobs_doc.sh; a change made here is lost.
r"""=========================================================
pikobs.flags -- Distribution of the quality-control flags
=========================================================

Every observation carries a 24-bit flag that says what quality control did
with it: bias corrected, blacklisted, rejected by the background check,
affected by clouds, assimilated. ``flags`` reads those bits and shows, for
every 6-h cycle, what share of the data ended up in each state. It is the
module to open when a suite suddenly assimilates less and nobody knows
why.

There is no ``FLAGS_CRITERIA`` here, on purpose: filtering by criteria is
what the other modules do, and this one exists to show the whole spectrum
at once.

Quick start
===========

.. code-block:: bash

   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_flags.sh
   chmod +x run_flags.sh

The wrapper runs on the node you are on and never submits to PBS, so open a
compute node first, edit the ``USER SETTINGS`` block and launch:

.. code-block:: bash

   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
   nano run_flags.sh
   ./run_flags.sh

.. warning::

   Do not run the wrapper on a login node: the extraction opens every 6-h
   file of the period in parallel.

.. important::

   Lists are **bash arrays**: ``FAMILY=(iasi cris)`` and
   ``ID_STN=(join all)``, not strings.

A run prints its phases and ends with the address of the viewer:

.. code-block:: text

   [flags] runs: experience
   [flags] id_stn tokens: ['join', 'all']
   [flags] channel tokens: ['join']
   [flags] input check OK: 29 cycles x 1 run(s) x 4 family(ies), 116 files, 31.8 GB
   [flags] extraction: 116 tasks, 80 worker(s)
   [pikobs] extraction: 116/116 (100%) 78s elapsed
   [flags] plots: 34 tasks
   [flags] -------------------- run time --------------------
   [flags] input           31.8 GB   116 files, 29 cycles, 1 run(s)
   [flags] extraction       78.4 s
   [flags] plots            41.2 s
   [flags] total           122.9 s   (2.0 min, 80 workers)
   Viewer: /home/dlo001/sites8/pikobs_flags/pikobs_flags_viewer.html
   Web:    to open it in a browser, link the folder under public_html once:
             ln -s /home/dlo001/sites8/pikobs_flags /home/dlo001/public_html/
           then: https://goc-dx-u3.science.gc.ca/~dlo001/pikobs_flags/pikobs_flags_viewer.html

`A live reference instance <https://goc-dx-u3.science.gc.ca/~dlo001/sites8/pikobs_doc_flags/pikobs_flags_viewer.html>`__.

How long a run takes, and how big a node to ask for: :doc:`runtime`.

----

1. How it works
===============

**Input check.** Every 6-h file of every run and family is looked up first.
If one is missing the run stops, says which cycles are missing and which
dates the directory does hold, and leaves ``PATHWORK`` untouched.

**Extraction.** Each file is read once and counted by station, varno,
channel and flag value; every region is a conditional sum inside that
single scan, so five regions cost almost what one costs. No criteria is
applied: the flag itself is the subject.

**Figures.** One task per (run, family, region, station selection,
channel, varno), spread over the workers.

----

2. Configuration
================

Only the ``USER SETTINGS`` block of the wrapper is meant to be edited.

.. wrapper-settings:: run_flags.sh

----

3. Choosing the stations and channels
=====================================

``ID_STN`` takes the tokens of the rest of Pikobs, and each one is its own
figure:

+---------------------------+---------------------------------------------------------------------+
| Token                     | Figures produced                                                    |
+===========================+=====================================================================+
| ``join``                  | one figure, every station pooled                                    |
+---------------------------+---------------------------------------------------------------------+
| ``all``                   | one figure per station, per instrument type for ai, sf, ua, gp, csr |
+---------------------------+---------------------------------------------------------------------+
| ``METOP`` or ``"METOP*"`` | the stations whose id starts with METOP, pooled                     |
+---------------------------+---------------------------------------------------------------------+
| ``=METOP-1``              | that station only                                                   |
+---------------------------+---------------------------------------------------------------------+
| ``N%``                    | SQL ``LIKE`` pattern on the station id                              |
+---------------------------+---------------------------------------------------------------------+

``CHANNEL`` works the same way: ``join`` merges every channel into one
figure, ``all`` gives one figure per channel, and an explicit list keeps
only those. For a first look at a radiance family, ``ID_STN=(all)`` with
``CHANNEL=(join)`` is usually the right pair: one figure per satellite,
every channel together.

----

4. Reading a figure
===================

+--------------+----------------------------------------------------------------------------------------------------------------------------+
| Block        | What it shows                                                                                                              |
+==============+============================================================================================================================+
| Header       | the variable, the period, the family, region, stations and channel, and the run                                            |
+--------------+----------------------------------------------------------------------------------------------------------------------------+
| Stacked bars | one bar per 6-h cycle, the share of each flag combination                                                                  |
+--------------+----------------------------------------------------------------------------------------------------------------------------+
| Legend       | per combination: its bits, their meaning, its share of the period and its observations per cycle                           |
+--------------+----------------------------------------------------------------------------------------------------------------------------+
| Table        | every observation once: assimilated with its combinations, not assimilated with its reasons, 100 % in all, with the counts |
+--------------+----------------------------------------------------------------------------------------------------------------------------+
| Group lists  | each line of the table opened: its flag combinations, largest first, with a bar and the numbers                            |
+--------------+----------------------------------------------------------------------------------------------------------------------------+

.. image:: _static/flags_plot.png
   :alt: Flag distribution: bars, legend, table and group lists
   :align: center
   :width: 100%

The **bars** are normalised, so each cycle adds up to 100 %: what matters
is the share of each state, not the volume, and a sudden change of colour
in one cycle is what you are looking for. The bar width follows the
period: four months are 480 bars, and the figure grows accordingly, which
is why it is meant to be opened full size in the viewer.

The **colour of a flag combination is always the same**, in every figure
and every family, because it is derived from the flag value itself. Two
figures of the same satellite can therefore be compared by colour alone.

The **table** answers the question people actually come with: of what came
in, how much was used, and why was the rest not. Every observation is counted
once. With bit 12 set it is assimilated, and the table lists the combinations
it came with -- on ``sw`` almost all of it is plain 12, some 12+13 (the O-P
rogue check at level 1), and a handful 9+12+17: observations QC-Var kept with
a reduced weight. Without bit 12 an observation gets a reason, the first one
of the list that matches, so the reasons add up to what is not assimilated
and the whole table to 100 %.

An observation often carries several reasons at once, rejected and
erroneous, unselected and cloudy. That is what the second column is for.
*first reason* counts each observation under one reason only, the first in
the order of the list; *carries it* counts every observation that has the
reason, whatever came first. On IASI the first column puts most of the loss
on clouds, while the second shows that nearly everything not assimilated also
carries bit 11. Both are true: they answer different questions.

For a radiance the blacklist (bit 8) is taken out before anything else. Most
IASI channels are never meant to be assimilated, and counting them would
squash every other share to nothing, so the line above the table says how
many observations were left out and the shares are over the channels in use.
Tiny shares are written in scientific notation instead of being rounded to
0.00 %, and the ``obs`` column gives the counts, so any other ratio can be
worked out by hand.

The **group lists** under the table open each of its lines: ASSIMILATED and
every reason present, each split into its flag combinations, largest first,
with a bar as long as its share of the group and the numbers written beside
it. They replace the pies of the earlier versions, which had no way of
showing a slice of 0.02 % next to one of 80 %.

Groups and bits
---------------

The meaning of the 24 bits, and the reasons with their order, live in
``pikobs/configobs/flag_groups.py``, not in the plotting code.
``REASONS_RADIANCE`` serves the families on channels and ``REASONS_DEFAULT``
the others. Each entry is a combination and its title, and the order
matters: the first entry that matches is the reason of an observation.

.. code-block:: python

   REASONS_DEFAULT = _titled([
       ((0, 'or', 2, 'or', 9, 'n16'), "ERRONEOUS DATA"),
       ((8,),                         "BLACKLISTED"),
       ((9, 16),                      "BACKGROUND CHECK (O-P INNOVATION ROGUE CHECK)"),
       ((18,),                        "REJECTED OVER LAND DUE TO HIGHER TOPOGRAPHY"),
       ((11,),                        "REJECTED BY THINNING"),
       ((9, 'or', 17),                "REJECTED BY OVERALL QUALITY CONTROL"),
   ])

A combination is read as sets of conditions: ``(9, 16)`` means both bits,
``(0, 'or', 7)`` means either of them, and ``(9, 16, 'n8')`` adds that bit
8 must not be set. An observation with no bit at all goes to NO BIT SET, and
one that no reason explains to OTHER, NOT ASSIMILATED; if OTHER grows, a
reason is missing from the list.

What each of the 24 bits means, and which bits the criteria of the other
modules require (``assimilee``, ``bgckalt``, ``postalt`` ...), is on
:doc:`flags_criteria`.

----

5. The viewer
=============

``pikobs_flags_viewer.html`` has six dropdowns: Experience, Family, Region,
Station, Varno and Channel; each one only offers what exists for the
choices on its left. **Flip** (key ``F``) swaps between the current figure
and the previous one, and a click opens the figure at full size, which is
how a four-month bar chart is read.

Move the mouse over a band of the bars or a row of a group list and a box
says what it is: the cycle, the flag and its bits, what each bit means, how
many observations. This needs the viewer opened through its web address; a
page opened straight from the disk cannot read the small map file that sits
beside each figure.

----

6. Output layout
================

::

   $PATHWORK/
   ├── pikobs_flags_viewer.html
   ├── flags_timing.json
   └── <family>/
       ├── flags_<run>_<start>_<end>_<family>.db
       ├── flags_<run>_<family>_<region>[_<surface>][_<special>]_<stn>_ch<chan>_varno<varno>.png
       └── flags_<...>.png.map.json

Beside each figure, ``.map.json`` holds where every band of the bars and
every row of the group lists is in the image, with its text: it is what the
box under the mouse reads.

With ``SVG="on"`` each figure is written again as ``.svg`` beside its PNG,
for editing before a presentation: in Inkscape or Illustrator the titles,
the legends and the colours stay editable. The viewer always uses the PNG,
so turning it on changes nothing else. An SVG keeps every element of the
figure, so ask for it on the one or two figures you actually need.

The ``.db`` files hold one row per (region, station, varno, channel, flag,
cycle) in the table ``flag_observations`` and can be queried with
``sqlite3``, which is the quickest way to answer "how many observations had
bit 9 set last Tuesday".

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
from pikobs.figures import svg_enabled
from pikobs.flags.flags_plot import (flags_plot_task, flags_viewer_items,
                                     figure_name)
from pikobs.obsdb import (check_input_files,
                          combine as _combine_rows,
                          open_result, table_columns, work_db)
from pikobs.obsdb.obsdb import split_tokens as _split_tokens, cycles as _cycles, input_size as _input_size  # shared, once
from pikobs.parallel import run_tasks
from pikobs.pbs_submit import maybe_submit_to_pbs
from pikobs.stations.stations import (expand_station_selectors,
                                      parse_station_tokens)
from pikobs.web.viewer import generate_web
from pikobs.web.runs import runs_block

CYCLE_HOURS = 6

_OBS_COLS = ("region, land_ocean, special, id_stn, CODTYP, varno, vcoord, "
             "date, flag, n")

_DDL = """
    CREATE TABLE IF NOT EXISTS flag_observations (
        region TEXT,
        land_ocean TEXT,
        special TEXT,
        id_stn TEXT,
        CODTYP INTEGER,
        varno  INTEGER,
        vcoord FLOAT,
        date   INTEGER,
        flag   INTEGER,
        n      INTEGER
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


def db_path(work_path, family, name, date_start, date_end) -> str:
    """One database per run and family; the region is a column."""
    return os.path.join(work_path, family,
                        f"flags_{_safe(name)}_{date_start}_{date_end}_"
                        f"{family}.db")


# ─────────────────────────────────────────────────────────────────────────────
# Input check
# ─────────────────────────────────────────────────────────────────────────────

def create_table_if_not_exists(cursor) -> None:
    cursor.execute(_DDL)


def _region_conditions(regions, land_oceans=('all',)) -> List[Dict[str, str]]:
    """Every (region, surface): the surface is part of the region's
    condition, which for all is the same as before."""
    out = []
    for region in regions:
        latlon = regionsobs.criteria(region)
        for land_ocean in land_oceans or ('all',):
            out.append({'region': region, 'land_ocean': land_ocean,
                        'cond': f"(1=1 {latlon}{surface_sql(land_ocean)})"})
    return out


def _special_values(path, region, land_ocean, sel) -> List[str]:
    """The special values of a selection, 'all' when it has none."""
    return [r[0] for r in _query_distinct(
        path, "SELECT DISTINCT special FROM flag_observations "
              "WHERE region = ? AND land_ocean = ?" + sel.sql() + ";",
        [region, land_ocean])] or ['all']


def create_flag_observations(family: str, new_db_filename: str,
                             existing_db_filename: str,
                             regions: Sequence[str],
                             varnos: Sequence[str] = (),
                             land_oceans: Sequence[str] = ('all',),
                             pathwork: str = '.',
                             special_on: bool = False) -> Optional[int]:
    """Count the observations of every flag in one RDB file.

    Grouped by station, varno, channel and flag; each region is a
    conditional sum in the same scan, so the file is read once. No flag
    criteria is applied: the whole 24-bit spectrum is what the module is
    about.
    """
    if not os.path.isfile(existing_db_filename):
        print(f"[flags] missing file, skipped: {existing_db_filename}",
              file=sys.stderr, flush=True)
        return None
    date_match = re.search(r'(\d{10})', os.path.basename(existing_db_filename))
    if not date_match:
        raise ValueError(f"No 10-digit date in: {existing_db_filename}")
    date_int = int(date_match.group(1))

    conds = _region_conditions(regions, land_oceans)
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    if varnos:
        element = ",".join(str(v) for v in varnos)
    vcoord_expr = (VCOORD or '').strip() or '9999'

    with work_db(attach={'db': existing_db_filename}) as (conn, mem_uri):
        conn.execute("PRAGMA db.mmap_size = 536870912;")
        register_surface(conn, land_oceans, pathwork)
        head_cols = table_columns(conn, 'HEADER', 'db')
        if not head_cols:
            print(f"[flags] no HEADER table in {existing_db_filename}",
                  file=sys.stderr, flush=True)
            return None
        cod = "codtyp" if 'codtyp' in head_cols else "NULL"

        sp_sel, _ = special_select(family, head_cols, special_on)
        selects = ["id_stn AS stn", f"{cod} AS cod", "varno AS varno",
                   f"{vcoord_expr} AS chan", "flag AS flag",
                   f"{sp_sel} AS special"]
        selects += [f"SUM(CASE WHEN {c['cond']} THEN 1 ELSE 0 END) AS c{i}"
                    for i, c in enumerate(conds)]

        rows = conn.execute(f"""
            SELECT {", ".join(selects)}
            FROM db.header NATURAL JOIN db.data
            WHERE varno IN ({element})
              {VCOCRIT}
            GROUP BY id_stn, {cod}, varno, {vcoord_expr}, flag, special;
        """).fetchall()

        out_rows = []
        for row in rows:
            stn, codtyp, varno, chan, flag, special = row[:6]
            for i, c in enumerate(conds):
                n = row[6 + i]
                if not n:
                    continue
                out_rows.append((c['region'], c['land_ocean'], special,
                                 stn, codtyp, varno, chan,
                                 date_int, flag, n))

        create_table_if_not_exists(conn)
        conn.executemany(
            f"INSERT INTO flag_observations ({_OBS_COLS}) "
            f"VALUES ({', '.join('?' * 10)});", out_rows)
        _combine_rows(new_db_filename, mem_uri, 'flag_observations',
                      _OBS_COLS, ddl=_DDL, module='flags')
        return len(out_rows)


def _extract_task(task: Dict[str, Any]) -> Optional[int]:
    try:
        return create_flag_observations(task['family'], task['db_new'],
                                        task['filein'], task['regions'],
                                        task['varnos'],
                                        task.get('land_oceans') or ('all',),
                                        task.get('pathwork') or '.',
                                        bool(task.get('special_on')))
    except Exception:
        print(f"[flags] extraction failed for {task['filein']}:\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def create_data_list(date_start, date_end, families, runs, work_path,
                     regions, varnos, land_oceans=('all',),
                     special_on=False) -> List[Dict[str, Any]]:
    tasks = []
    for cycle in _cycles(date_start, date_end):
        for family in families:
            for name, path in runs:
                tasks.append({
                    'family': family,
                    'filein': os.path.join(path, f'{cycle}_{family}'),
                    'db_new': db_path(work_path, family, name, date_start,
                                      date_end),
                    'regions': list(regions), 'varnos': list(varnos),
                    'land_oceans': list(land_oceans), 'pathwork': work_path,
                    'special_on': special_on,
                })
    return tasks


def _index_task(path: str) -> Optional[str]:
    try:
        with open_result(path) as conn:
            conn.execute("CREATE INDEX IF NOT EXISTS idx_flags ON "
                         "flag_observations (region, land_ocean, special, varno, "
                         "id_stn, vcoord);")
        return path
    except Exception as exc:
        print(f"[flags] indexing {path} failed: {exc}", file=sys.stderr,
              flush=True)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Plot tasks
# ─────────────────────────────────────────────────────────────────────────────

def _query_distinct(path, sql, params=()) -> List[tuple]:
    if not os.path.isfile(path):
        return []
    try:
        with open_result(path) as conn:
            return conn.execute(sql, params).fetchall()
    except Exception as exc:
        print(f"[flags] query failed on {os.path.basename(path)}: {exc}",
              file=sys.stderr, flush=True)
        return []


def _channel_items(path, where, args, chan_tokens) -> List[Any]:
    items: List[Any] = []
    explicit = []
    have = None
    for tok in chan_tokens:
        if tok == 'join':
            items.append('join')
        elif tok == 'all':
            have = have if have is not None else [
                r[0] for r in _query_distinct(
                    path, f"SELECT DISTINCT vcoord FROM flag_observations "
                          f"WHERE {where};", args)]
            items += have
        else:
            explicit.append(tok)
    if explicit:
        have = have if have is not None else [
            r[0] for r in _query_distinct(
                path, f"SELECT DISTINCT vcoord FROM flag_observations "
                      f"WHERE {where};", args)]
        for chan in have:
            for tok in explicit:
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
        if str(it) not in seen:
            seen.add(str(it))
            out.append(it)
    return out


def create_data_list_plot(date_start, date_end, families, runs, work_path,
                          regions, stn_tokens, chan_tokens,
                          land_oceans=('all',)) -> List[Dict[str, Any]]:
    tasks = []
    for name, _ in runs:
        for family in families:
            path = db_path(work_path, family, name, date_start, date_end)
            if not os.path.isfile(path):
                continue
            selectors = expand_station_selectors([path], stn_tokens, family,
                                                 table='flag_observations')
            for region, land_ocean in [(r, s) for r in regions
                                       for s in land_oceans]:
                for sel, special in [
                        (s, v) for s in selectors
                        for v in _special_values(path, region, land_ocean, s)]:
                    where = ("region = ? AND land_ocean = ? AND special = ?"
                             + sel.sql())
                    args = [region, land_ocean, special]
                    varnos = [r[0] for r in _query_distinct(
                        path, f"SELECT DISTINCT varno FROM flag_observations "
                              f"WHERE {where};", args)]
                    chans = _channel_items(path, where, args, chan_tokens)
                    for varno in varnos:
                        for chan in chans:
                            tasks.append({
                                'pathwork': work_path, 'db_file': path,
                                'experience': name, 'family': family,
                                'region': region, 'selector': sel,
                                'land_ocean': land_ocean,
                                'special': special,
                                'special_label': special_label(family,
                                                               special),
                                'id_stn': sel.display, 'stn_sql': sel.sql(),
                                'stn_tag': sel.tag, 'varno': varno,
                                'vcoord': chan, 'datestart': date_start,
                                'dateend': date_end,
                            })
    return tasks


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def _report_timing(timing: Dict[str, Any], pathwork: str) -> None:
    sec = timing['seconds']
    print("[flags] -------------------- run time --------------------",
          flush=True)
    print(f"[flags] input        {_fmt_bytes(timing['input_bytes']):>10s}"
          f"   {timing['input_files']} files, {timing['cycles']} cycles, "
          f"{timing['runs']} run(s)", flush=True)
    for phase in ('extraction', 'plots'):
        if phase in sec:
            print(f"[flags] {phase:<12s} {sec[phase]:>8.1f} s", flush=True)
    print(f"[flags] total        {sec['total']:>8.1f} s   "
          f"({sec['total'] / 60:.1f} min, {timing['n_cpus']} workers)",
          flush=True)
    try:
        with open(os.path.join(pathwork, "flags_timing.json"), "w") as fh:
            json.dump(timing, fh, indent=1)
    except OSError as exc:
        print(f"[flags] could not write flags_timing.json: {exc}",
              file=sys.stderr, flush=True)


def make_flags(runs, pathwork, datestart, dateend, regions, families,
               id_stn, channel, n_cpu, varnos=(), svg: bool = False,
               land_ocean=('all',), special_column='off') -> int:
    regions = _split_tokens(regions)
    stn_tokens = parse_station_tokens(id_stn)
    chan_tokens = _split_tokens(channel) or ['join']
    land_oceans = _split_tokens(land_ocean) or ['all']
    bad = [s for s in land_oceans if s not in ('all', 'land', 'ocean')]
    if bad:
        raise ValueError(f"LAND_OCEAN takes all, land and ocean, not {bad}")
    special_on = str(special_column).strip().lower() in ('on', 'true', '1', 'yes')

    print(f"[flags] runs: {', '.join(n for n, _ in runs)}", flush=True)
    print(f"[flags] regions: {regions}", flush=True)
    print(f"[flags] land_ocean: {land_oceans}  |  special column: "
          f"{'on' if special_on else 'off'}", flush=True)
    print(f"[flags] id_stn tokens: {stn_tokens}", flush=True)
    print(f"[flags] channel tokens: {chan_tokens}", flush=True)

    if not check_input_files(runs, families, datestart, dateend,
                             'flags'):
        return 1

    t_start = time.time()
    cycles = _cycles(datestart, dateend)
    n_input, input_bytes = _input_size(runs, families, cycles)
    timing: Dict[str, Any] = {
        'datestart': datestart, 'dateend': dateend, 'cycles': len(cycles),
        'families': list(families), 'runs': len(runs), 'regions': regions,
        'id_stn': stn_tokens, 'channel': chan_tokens, 'n_cpus': n_cpu,
        'land_ocean': land_oceans, 'special_column': special_on,
        'svg': svg,
        'input_files': n_input, 'input_bytes': input_bytes, 'seconds': {},
    }

    for family in families:
        pikobs.delete_create_folder(pathwork, family)

    tasks = create_data_list(datestart, dateend, families, runs, pathwork,
                             regions, varnos, land_oceans, special_on)

    client = None
    dask_dir = None
    if n_cpu > 1:
        os.environ["DASK_LOGGING__DISTRIBUTED"] = "error"
        base = os.environ.get("TMPDIR") or None
        dask_dir = tempfile.mkdtemp(prefix="pikobs_flags_dask_", dir=base)
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
        print(f"[flags] extraction: {len(tasks)} tasks, {n_cpu} worker(s)",
              flush=True)
        res = run_tasks(_extract_task, [(t,) for t in tasks], client,
                        label='extraction')
        timing['seconds']['extraction'] = time.time() - t0
        print(f"[flags] extraction time: "
              f"{timing['seconds']['extraction']:.1f}s "
              f"({sum(r is not None for r in res)}/{len(tasks)} files)",
              flush=True)

        dbs = sorted({t['db_new'] for t in tasks})
        run_tasks(_index_task, [(d,) for d in dbs], client, label='indexing')

        plot_tasks = create_data_list_plot(datestart, dateend, families, runs,
                                           pathwork, regions, stn_tokens,
                                           chan_tokens, land_oceans)
        for t in plot_tasks:
            t['svg'] = svg
        if not plot_tasks:
            print("[flags] WARNING: nothing to plot, check the selectors.",
                  file=sys.stderr, flush=True)
            return 1
        t0 = time.time()
        print(f"[flags] plots: {len(plot_tasks)} tasks", flush=True)
        results = run_tasks(flags_plot_task, [(t,) for t in plot_tasks],
                            client, label='plots')
        timing['seconds']['plots'] = time.time() - t0
        print(f"[flags] plot time: {timing['seconds']['plots']:.1f}s "
              f"({sum(r is not None for r in results)}/{len(plot_tasks)})",
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

    items = flags_viewer_items(plot_tasks, results)
    if not items:
        print("[flags] ERROR: no figure was produced, viewer not written.",
              file=sys.stderr, flush=True)
        return 1
    keys = ["experience", "family", "region", "land_ocean", "id_stn",
            "special", "varno", "vcoord"]
    print(f"[flags] viewer selectors: {keys}", flush=True)
    generate_web(
        items, keys, os.path.join(pathwork, "pikobs_flags_viewer.html"),
        title="Pikobs Flags Viewer",
        subtitle="What quality control did with each observation, cycle by "
                 "cycle. Every flag is shown; there is no criteria filter."
                 + runs_block(runs, None, (datestart, dateend)),
        image_subdir_key="family",
        key_labels={"vcoord": "Channel", "experience": "Experience",
                    "special": special_key_label(families)},
        issues_url="https://gitlab.science.gc.ca/dlo001/Pikobs",
        enable_play=False,
    )

    timing['seconds']['total'] = time.time() - t_start
    _report_timing(timing, pathwork)
    print(f"[flags] done -- output in: {pathwork}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def arg_call() -> None:
    import argparse

    p = argparse.ArgumentParser(
        prog="pikobs-flags",
        description="Distribution of the quality-control flags.")
    p.add_argument('--path_experience_files', nargs='+', default=[])
    p.add_argument('--experience_name', nargs='+', default=[])
    p.add_argument('--pathwork', default=None)
    p.add_argument('--datestart', default=None)
    p.add_argument('--dateend', default=None)
    p.add_argument('--region', nargs='+', default=['Monde'])
    p.add_argument('--family', nargs='+', default=[])
    p.add_argument('--id_stn', nargs='+', default=['join'],
                   help="Tokens, one figure each: join, all, PREFIX, "
                        "LIKE%%pattern, =EXACT, 'NAME (codtyp)'.")
    p.add_argument('--channel', '--vcoord', dest='channel', nargs='+',
                   default=['join'],
                   help="join (all channels merged), all (one each), or an "
                        "explicit list.")
    p.add_argument('--varnos', nargs='*', default=[])
    p.add_argument('--land_ocean', nargs='+', default=['all'],
                   choices=['all', 'land', 'ocean'],
                   help="all (no filter), land, ocean: one series of figures "
                        "each; land and ocean read the land mask.")
    p.add_argument('--special_column', default='off', choices=['on', 'off'],
                   help="on: one series of figures per value of the family's "
                        "special column; off: all together (default).")
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
    maybe_submit_to_pbs(args)
    sys.exit(make_flags(runs, args.pathwork, args.datestart, args.dateend,
                        args.region, _split_tokens(args.family), args.id_stn,
                        args.channel, args.n_cpus,
                        _split_tokens(args.varnos), svg_enabled(args.svg),
                        land_ocean=args.land_ocean,
                        special_column=args.special_column))


if __name__ == '__main__':
    arg_call()
