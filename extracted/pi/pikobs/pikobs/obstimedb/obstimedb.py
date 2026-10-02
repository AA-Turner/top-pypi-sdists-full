#!/usr/bin/env python3
"""
================================================================
pikobs.obstimedb — Observation Volume Time Diagnostics
================================================================

``obstimedb`` is the **single-experience time-series diagnostic** module
of Pikobs. Unlike ``obscountdb`` (which compares two runs), ``obstimedb``
looks at **one experience only** and tracks how its observation volume
evolves **cycle by cycle** (every 6h: 00/06/12/18).

For each family and ``id_stn`` it builds:

* A **mosaic (heatmap)**: rows = ``id_stn``, columns = date/cycle. Each
  cell is coloured based **only on Nobs** (never on Nobsprofile):
  **green** if normal, **yellow/orange/red** at increasing drop
  severity (default 10% / 15% / 20%) compared to the **mean of the same
  synoptic hour over the previous ``--window_days`` calendar days**
  (default 10 days). A total outage (Nobs=0) is always red.
  Cells with insufficient history (fewer than 3 prior same-hour cycles)
  are shown in grey.

* A **global time series**: total ``Nobs`` per family, summed over all
  stations, for every 6h cycle in the period — a single glance at the
  overall observation-volume trend.

* An **"Average Nobs profiles per 6 hours" summary table**, matching
  the reference PSMON-style report: per (family, id_stn), the number
  of profiles today/yesterday/this-week/last-week/at-run-time, each
  compared against its reference period as a percent difference, plus
  a "last 10 days, same synoptic hour as the run" comparison. See
  :func:`pikobs.obstimedb_plot._draw_profile_summary_table` for the
  exact period/percentage definitions.

* For RADIANCE families (any family whose :func:`pikobs.family` reports
  ``VCOTYP == 'CANAL'`` — AMSUA, AMSUB, MWHS2, SSMIS, IASI, CRISFSR,
  ATMS, CSR), an additional PER-CHANNEL time series (collapsed behind a
  click-to-expand section in the HTML report, since some instruments
  have hundreds of channels).

Optionally, ``--agr`` overlays the mean per-cycle departure
(``AVG(omp)`` / ``AVG(oma)``) on a secondary panel of the time series,
exactly as in ``obscountdb``.

---

1. How to run
=============

Use the bash wrapper ``run_obstimedb.sh`` (download the latest copy from
GitLab so it stays in sync):

.. code-block:: bash

   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_obstimedb.sh
   chmod +x run_obstimedb.sh

.. code-block:: bash

   # 1. Open a compute node:
   qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0

   # 2. Once on the compute node, edit the USER SETTINGS and launch:
   nano run_obstimedb.sh
   ./run_obstimedb.sh

.. warning::

   Do not run ``run_obstimedb.sh`` on a login node — always open a
   compute node first.

---

2. Configuration
================

.. code-block:: bash

   # Single experience — no control/reference needed.
   PATH_EXPERIENCE_FILES="/home/.../monitoring/"
   EXPERIENCE_NAME="experience"

   PATHWORK="/home/dlo001/sites8/pikobs_obstimedb"

   DATESTART="2026020100"
   DATEEND="2026020500"
   REGION="Monde"

   FAMILY="ai sw sf ua to_amsua_allsky iasi ..."
   FLAGS_CRITERIA="assimilee"
   N_CPU=120

   # Alert thresholds for the mosaic.
   WINDOW_DAYS=10      # look-back window (calendar days) for the baseline
   ALERT_PCT=10.0      # yellow if Nobs drops >= this % vs baseline

   # Optional departure overlay: omp / oma / "oma omp" (empty to disable).
   AGR="oma omp"

   python -c 'import pikobs; pikobs.obstimedb.arg_call()' \
          --path_experience_files "${PATH_EXPERIENCE_FILES}" \
          --experience_name "${EXPERIENCE_NAME}" \
          --pathwork "${PATHWORK}" \
          --datestart "${DATESTART}" --dateend "${DATEEND}" \
          --region ${REGION} --family ${FAMILY} \
          --flags_criteria "${FLAGS_CRITERIA}" \
          --window_days "${WINDOW_DAYS}" \
          --alert_yellow "${ALERT_YELLOW}" --alert_orange "${ALERT_ORANGE}" --alert_red "${ALERT_RED}" \
          ${AGR:+--agr ${AGR}} \
          --n_cpu "${N_CPU}"

+-----------------------------+----------------------------------------------+
| Variable                    | Description                                  |
+=============================+==============================================+
| ``PATH_EXPERIENCE_FILES``   | SQLite directory for the (single) experience |
+-----------------------------+----------------------------------------------+
| ``EXPERIENCE_NAME``         | Label for the experiment data                |
+-----------------------------+----------------------------------------------+
| ``PATHWORK``                | Output root (wiped on each run)              |
+-----------------------------+----------------------------------------------+
| ``DATESTART`` / ``DATEEND`` | Window ``YYYYMMDDHH`` (UTC, inclusive)       |
+-----------------------------+----------------------------------------------+
| ``REGION``                  | Geographic region (e.g., Monde)              |
+-----------------------------+----------------------------------------------+
| ``FAMILY``                  | Space-separated list of observation families |
+-----------------------------+----------------------------------------------+
| ``FLAGS_CRITERIA``          | Bitmask criteria (e.g., assimilee)           |
+-----------------------------+----------------------------------------------+
| ``WINDOW_DAYS``             | Baseline look-back window, in calendar days  |
+-----------------------------+----------------------------------------------+
| ``ALERT_PCT``               | Drop threshold (%) that triggers yellow      |
+-----------------------------+----------------------------------------------+
| ``AGR``                     | Departure overlay: omp / oma / "oma omp"     |
+-----------------------------+----------------------------------------------+
| ``N_CPU``                   | Number of parallel Dask workers              |
+-----------------------------+----------------------------------------------+

---

3. Report overview
==================

+-------------------------+------------------------------------------------------+
| Report element          | Content                                              |
+=========================+======================================================+
| Profile Summary Table   | Per (family, id_stn): profiles today/yesterday/this- |
|                         | week/last-week/at-run-time, each as a % difference   |
|                         | vs its reference period (see module docstring).      |
+-------------------------+------------------------------------------------------+
| Global Time Series      | Total ``Nobs`` per family, every 6h cycle, over the  |
|                         | whole period. With ``--agr``, a stacked panel adds   |
|                         | the mean AVG(omp)/AVG(oma) per cycle.                |
+-------------------------+------------------------------------------------------+
| Station Mosaic          | Heatmap per family: rows = id_stn, columns = cycle.  |
|                         | Nobs-only colour: Green=normal, Yellow/Orange/Red at |
|                         | increasing drop severity, Grey=not enough history.   |
+-------------------------+------------------------------------------------------+
| Per-channel Time Series | RADIANCE families only (VCOTYP=='CANAL'): a          |
|                         | collapsed, click-to-expand heatmap per station,      |
|                         | rows = channel, columns = cycle, coloured by Nobs.   |
+-------------------------+------------------------------------------------------+

---

4. Output layout
================

::

   $PATHWORK/
   |-- TimeSeries_<family>_<Region>_<flag>.png
   |-- Mosaic_<family>_<Region>_<flag>.png
   `-- Full_Report_<Region>_<flag>.html        <- interactive viewer

Open ``Full_Report_<Region>_<flag>.html`` in any browser — no server
required.

---

5. Support
==========

Bugs and feature requests:
   `<https://gitlab.science.gc.ca/dlo001/Pikobs/-/issues>`_
"""

import os
import re
import sys
import time
import sqlite3
import warnings
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from pikobs.pbs_submit import maybe_submit_to_pbs

# Suppress all Shapely deprecation warnings before importing cartopy/shapely
warnings.filterwarnings("ignore", ".*ShapelyDeprecationWarning.*")
import shapely
import cartopy

import numpy as np
import dask
from dask.distributed import Client

# a region is a box or a polygon; the module does not need to know
from pikobs.configobs import regionsobs
import pikobs

# Full CODTYP table, code -> display name (115 entries). Sourced from a
# comprehensive Fortran codtyp table given directly by the user 2026-08,
# which corrected 3 entries vs an earlier, smaller version of this dict:
# 157 (was 'BUFR'), 147 (was 'BUOYS' -> 'A-SHIP AUTO'), 254 (was generic
# 'SCAT' -> 'ASCAT').
#
# 157 was REVERTED back to 'BUFR' after direct evidence from a real
# production report: the SAME underlying numbers (Run time, Last 10d,
# Diff 1 day all matched exactly) appeared there labelled 'BUFR', not
# 'ACARS', within the ai family specifically -- confirming this
# production system's own established naming convention differs from
# the generic Fortran table for this code, and the report needs to
# match THAT convention, not the generic one.
#
# 147 ('A-SHIP AUTO') and 254 ('ASCAT') were changed on the SAME
# Fortran table's authority as 157 was, but have NOT been independently
# verified against a real report the way 157 just was -- given 157
# turned out to need reverting, treat these two as UNCONFIRMED until
# checked the same way (compare a real report row's numbers against
# what this dict currently labels that codtyp).
#
# A handful of entries (e.g. ICECLAKE, ICECOCEAN, SMOSSMAP) are left as
# a single unsplit word deliberately -- the word boundary wasn't
# confirmed, so no space was guessed in rather than risk an incorrect
# split.
DICT_CODTYP = {
    '12': 'SYNOP', '13': 'SHIP', '14': 'SYNOP MOBIL', '15': 'METAR',
    '16': 'SPECI', '18': 'DRIFTER', '20': 'RADOB', '22': 'RADPREP',
    '32': 'PILOT', '33': 'PILOT SHIP', '34': 'PILOT MOBIL', '35': 'TEMP',
    '36': 'TEMP SHIP', '37': 'TEMP DROP', '38': 'TEMP MOBIL', '39': 'ROCOB',
    '40': 'ROCOB SHIP', '41': 'CODAR', '42': 'AMDAR', '44': 'ICEAN',
    '45': 'IAC', '46': 'IACFLEET', '47': 'GRID', '49': 'GRAF',
    '50': 'WINTEM', '51': 'TAF', '53': 'ARFOR', '54': 'ROFOR',
    '57': 'RADOF', '61': 'MAFOR', '62': 'TRACKOB', '63': 'BATHY',
    '64': 'TESAC', '65': 'WAVEOB', '67': 'HYDRA', '68': 'HYFOR',
    '71': 'CLIMAT', '72': 'CLIMAT SHIP', '73': 'NACLI', '75': 'CLIMAT TEMP',
    '76': 'CLIMAT TEMP SHIP', '81': 'SFAZI', '82': 'SFLOC', '83': 'SFAZU',
    '85': 'SAREP', '86': 'SATEM', '87': 'SARAD', '88': 'SATOB',
    '92': 'GRIB', '94': 'BUFR', '127': 'SFCAQ', '128': 'AIREP',
    '129': 'PIREP', '130': 'PROFWIND', '131': 'SYNOPSUPEROB', '132': 'AIREPSUPEROB',
    '133': 'SA SYNOP', '134': 'PAOBS', '135': 'TEMP + PILOT', '136': 'TEMP + SYNOP',
    '137': 'PILOT SYNOP', '138': 'TEMP PILOT SYNOP', '139': 'TEMP SHIP + PILOT SHIP', '140': 'TEMP SHIP SHIP',
    '141': 'TEMPS SHIP SHIP', '142': 'PILOT SHIP SHIP', '143': 'SWOB-NONAUTO', '144': 'SWOB-AUTO',
    '145': 'Patrol ship', '146': 'ASYNOP', '147': 'A-SHIP AUTO', '148': 'SWOBNONAUTO-SPECIAL',
    '149': 'SWOBAUTO-SPECIAL', '150': 'PSEUDOSFC', '151': 'PSEUDOALT', '152': 'PSEUDOSFCREP',
    '153': 'PSEUDOALTREP', '157': 'BUFR', '158': 'HUMSAT', '159': 'TEMP PILOT MOBIL',
    '160': 'TEMP SYNOP MOBIL', '161': 'PILOT SYNOP MOBIL', '162': 'TEMP PILOT SYNOP MOBIL', '163': 'RADAR',
    '164': 'AMSUA', '167': 'SCAT', '168': 'SSMIS', '169': 'GPSRO',
    '170': 'OZONE', '171': 'METEOSAT', '172': 'SHEF', '174': 'SAR',
    '175': 'ALTIM', '177': 'ADS', '178': 'ICECLAKE', '179': 'ICECOCEAN',
    '180': 'GOES', '181': 'AMSUB', '182': 'MHS', '183': 'AIRS',
    '184': 'RADIANCE', '185': 'CSR', '186': 'IASI', '188': 'AMVS',
    '189': 'GROUND BASED GPS', '192': 'ATMS', '193': 'CRIS NSR', '194': 'SMOSSMAP',
    '195': 'constituants chimiques (remote)', '196': 'constituants chimiques (in-situ)', '198': 'NetWork of Network', '200': 'MWHS-2',
    '202': 'CRIS FSR', '204': 'SARWINDS', '254': 'ASCAT',
}

# 'ua' expanded 2026-08: 10 codtypes with a PILOT*/TEMP* name in
# DICT_CODTYP (136,137,138,140,141,142,159,160,161,162) were confirmed
# MISSING from the original hand-curated list here -- found by cross
# checking every DICT_CODTYP entry whose name starts with PILOT or
# TEMP against this list, after a real report's ua/ALL total didn't
# match a reference report (the user's own suggestion: match by name
# pattern, not just the original numeric list). Some of these
# (136/138/160/162) are combined TEMP+SYNOP/PILOT SYNOP report types
# that also contain "SYNOP" in their name -- placed here (not in 'sf')
# since their name STARTS WITH PILOT/TEMP, matching the same rule
# applied to every other code; each code maps to exactly one family in
# this dict, no dual-membership support.
FAMILY_CODES = {
    # 'ai' expanded 2026-08: 129 (PIREP -- Pilot Report, an aircraft
    # weather report) and 132 (AIREPSUPEROB -- a superobbed version of
    # 128/AIREP, already in this list) added on reasonable-confidence
    # name-pattern grounds, same method that found 'ua's gap -- NOT
    # independently confirmed against a real report the way 'ua' was.
    'ai': ['42', '128', '129', '132', '157', '177'],
    'sf': ['12', '13', '14', '15', '16', '18', '143', '144', '145', '146', '147', '148', '149', '198'],
    'gp': ['189'],
    'csr': ['185'],
    'ua': ['32', '33', '34', '35', '36', '37', '38', '135', '136', '137', '138', '139',
           '140', '141', '142', '159', '160', '161', '162']
}

# Departure metrics that --agr may request. Each maps to a dedicated
# column in the moyenne table (avg_omp / avg_oma).
AGR_METRICS = ('omp', 'oma')

DEFAULT_WINDOW_DAYS = 10
DEFAULT_ALERT_YELLOW = 10.0
DEFAULT_ALERT_ORANGE = 15.0
DEFAULT_ALERT_RED = 20.0
DEFAULT_ALERT_HIGH = 10.0


def _norm_agr(agr) -> List[str]:
    """Normalise the --agr argument into an ordered, de-duplicated list
    containing only valid metrics ('omp', 'oma'). Accepts None, a single
    string, or a list/tuple of strings."""
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


def create_table_if_not_exists(cursor: sqlite3.Cursor) -> None:
    # avg_omp / avg_oma hold AVG(omp) / AVG(oma) per (id_stn, date) when
    # requested via --agr; they stay NULL otherwise or when the underlying
    # column is empty. channel holds the vertical-coordinate (channel
    # number) ONLY for radiance families (VCOTYP=='CANAL' in
    # pikobs.family()) -- NULL for every other family, so a single
    # shared schema covers both cases without a second table.
    query = """
        CREATE TABLE IF NOT EXISTS moyenne (
            Nobsdata NUMERIC,
            Nobsprofile NUMERIC,
            avg_omp NUMERIC,
            avg_oma NUMERIC,
            id_stn TEXT,
            channel NUMERIC,
            date integer
        );
    """
    cursor.execute(query)


def combine(pathfileout: str, filememory: str) -> None:
    # Made idempotent: DELETE any existing rows in the target for the
    # SAME date(s) about to be inserted, before inserting. Without this,
    # re-running the extraction for a date already in the accumulator
    # (a retried/resumed job, or two separate --datestart/--dateend runs
    # with an overlapping date range writing to the same output db)
    # silently DUPLICATES that date's rows -- confirmed directly:
    # extracting the same file twice into the same accumulator produced
    # the SAME (date, id_stn) row twice, doubling every downstream sum
    # for that date (and, since different runs can overlap different
    # date spans by different amounts, this produces INCONSISTENT
    # inflation across periods -- e.g. Today off by one factor, This
    # week by another -- rather than one uniform, easy-to-spot scale
    # error). This delete makes a re-run REPLACE that date's data
    # instead of stacking a duplicate on top of it.
    delete_sql = """
        DELETE FROM moyenne
        WHERE date IN (SELECT DISTINCT date FROM this_avg_db.moyenne);
    """
    insert_sql = """
        INSERT INTO moyenne (Nobsdata, Nobsprofile, avg_omp, avg_oma, id_stn, channel, date)
        SELECT Nobsdata, Nobsprofile, avg_omp, avg_oma, id_stn, channel, date
        FROM this_avg_db.moyenne;
    """
    with sqlite3.connect(pathfileout, uri=True, isolation_level=None, timeout=9999) as conn:
        try:
            conn.execute("PRAGMA journal_mode=OFF;")
            conn.execute("PRAGMA synchronous=OFF;")
            create_table_if_not_exists(conn)

            conn.execute(f"ATTACH DATABASE '{filememory}' AS this_avg_db;")
            conn.execute(delete_sql)
            conn.execute(insert_sql)
            conn.commit()
            conn.execute("DETACH DATABASE this_avg_db;")
        except sqlite3.Error as e:
            print(f"[ERROR] Combining SQLite files failed: {e}", flush=True)
            raise


def dedupe_moyenne_table(db_path: str) -> None:
    """Safety net, run once per family AFTER all its extraction/combine()
    calls finish (both serial and parallel mode), right before plotting.

    combine()'s delete-then-insert already stops a re-run of the SAME
    date from stacking a duplicate on top of an existing one -- but in
    parallel mode, if two Dask workers happen to combine() the SAME
    date concurrently (a retried/resumed task racing the original), a
    delete-then-insert on each side can still both succeed and both
    insert, leaving a duplicate despite that per-call protection. This
    pass is the final, unconditional guarantee: for every (date,
    id_stn, channel) combination, keep exactly one row (the smallest
    SQLite rowid) and drop the rest -- whatever the cause, by the time
    plotting reads this file, it can't contain duplicates.

    Cheap and safe to run even when there's nothing to clean (a single
    GROUP BY scan plus a DELETE that matches zero rows), so it isn't
    gated behind any "was this run risky" check -- it always runs.
    """
    if not os.path.exists(db_path):
        return
    conn = sqlite3.connect(db_path, timeout=9999)
    try:
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='moyenne';")]
        if not tables:
            return
        before = conn.execute("SELECT COUNT(*) FROM moyenne").fetchone()[0]
        conn.execute("""
            DELETE FROM moyenne
            WHERE rowid NOT IN (
                SELECT MIN(rowid) FROM moyenne GROUP BY date, id_stn, channel
            );
        """)
        conn.commit()
        after = conn.execute("SELECT COUNT(*) FROM moyenne").fetchone()[0]
        if before != after:
            print(f"[WARNING] dedupe_moyenne_table: removed {before - after} "
                  f"duplicate row(s) from {os.path.basename(db_path)} "
                  f"(likely a retried/re-run extraction task -- see "
                  f"combine()'s docstring). Downstream sums for the "
                  f"affected dates were inflated until this ran.",
                  flush=True)
    finally:
        conn.close()


def create_and_populate_moyenne_table(
    family: str, new_db_filename: str, existing_db_filename: str,
    selected_region: str, selected_flags: str, agr: Optional[List[str]] = None
) -> None:
    date_match = re.search(r'(\d{10})', existing_db_filename)
    if not date_match:
        raise ValueError(f"No 10-digit sequence found in: {existing_db_filename}")

    agr_list = _norm_agr(agr)
    in_memory_db = "file::memory:?cache=shared"

    with sqlite3.connect(in_memory_db, uri=True, isolation_level=None, timeout=9999999) as mem_conn:
        cursor = mem_conn.cursor()

        FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
        LATLONCRIT = regionsobs.criteria(selected_region)
        flag_criteria = pikobs.flag_criteria(selected_flags)

        cursor.execute("PRAGMA journal_mode = MEMORY;")
        cursor.execute("PRAGMA synchronous = OFF;")
        cursor.execute("PRAGMA foreign_keys = OFF;")

        cursor.execute(f"ATTACH DATABASE '{existing_db_filename}' AS db;")
        create_table_if_not_exists(cursor)

        avg_omp_expr = "AVG(omp)" if "omp" in agr_list else "NULL"
        avg_oma_expr = "AVG(oma)" if "oma" in agr_list else "NULL"

        if family in FAMILY_CODES:
            case_lines = ["CASE CAST(codtyp AS TEXT)"]
            for code, name in DICT_CODTYP.items():
                case_lines.append(f"WHEN '{code}' THEN '{name}'")
            case_lines.append("ELSE CAST(codtyp AS TEXT) END")

            id_stn_expr = " ".join(case_lines)

            codes_str = ", ".join([f"'{c}'" for c in FAMILY_CODES[family]])
            family_filter = f"AND CAST(codtyp AS TEXT) IN ({codes_str})"
            group_col = "codtyp"
        else:
            id_stn_expr = "id_stn"
            family_filter = ""
            group_col = "id_stn"

        # ------------------------------------------------------------------
        # RADIANCE families (VCOTYP=='CANAL') additionally get a per-channel
        # breakdown: group by the channel number (vcoord) TOO, and select
        # it into its own column. Every other family leaves `channel` as
        # a literal NULL and groups exactly as before -- this is a pure
        # addition, the non-radiance extraction path is unchanged.
        #
        # CRITICAL: the per-channel rows must NEVER be the only rows
        # inserted for a radiance family. The SAME id_obs (profile)
        # appears in MANY channel rows (one per channel it reports), so
        # summing Nobsdata/Nobsprofile ACROSS channel rows -- exactly
        # what every consumer of `moyenne` that isn't channel-aware does
        # (the main Nobs/Nobsprofile series behind the mosaic, global
        # time series, and profile summary table) -- silently multiplies
        # the true profile count by roughly the number of channels
        # reported (confirmed directly: a 10-profile/15-channel test
        # case summed to 150, not 10). The fix is to ALSO insert a
        # SEPARATE, non-channel-split row (channel=NULL) with the
        # correct, ungrouped-by-channel counts, so every consumer that
        # filters `WHERE channel IS NULL` (the main series) gets the
        # right numbers, while `WHERE channel IS NOT NULL` (the
        # per-channel breakdown) still works exactly as before.
        # ------------------------------------------------------------------
        is_radiance = (VCOTYP == 'CANAL')
        if is_radiance:
            passes = [("NULL", group_col), ("vcoord", f"{group_col}, vcoord")]
        else:
            passes = [("NULL", group_col)]

        for channel_expr, group_by_clause in passes:
            insert_query = f"""
                INSERT INTO moyenne (Nobsdata, Nobsprofile, avg_omp, avg_oma, id_stn, channel, date)
                SELECT
                    count(DISTINCT(id_data)),
                    count(DISTINCT(id_obs)),
                    {avg_omp_expr},
                    {avg_oma_expr},
                    {id_stn_expr},
                    {channel_expr},
                    {date_match.group(1)}
                FROM db.header
                NATURAL JOIN db.DATA
                WHERE obsvalue IS NOT NULL
                    {flag_criteria}
                    {LATLONCRIT}
                    {VCOCRIT}
                    {family_filter}
                GROUP BY {group_by_clause};
            """

            try:
                cursor.execute(insert_query)
            except sqlite3.OperationalError as err:
                msg = str(err).lower()
                fb_query = insert_query
                for metric in agr_list:
                    if metric in msg:
                        print(f"[WARNING] Column '{metric}' not found in "
                              f"{os.path.basename(existing_db_filename)}; storing NULL.",
                              flush=True)
                        fb_query = fb_query.replace(f"AVG({metric})", "NULL")
                if fb_query != insert_query:
                    cursor.execute(fb_query)
                else:
                    raise
        mem_conn.commit()

        try:
            combine(new_db_filename, in_memory_db)
        except sqlite3.Error as error:
            print(f"[ERROR] Creating single sqlite file: {os.path.basename(in_memory_db)} -- {error}", flush=True)


def create_data_list(
    date_start: str, date_end: str, families: List[str], input_path: str,
    name: str, work_path: str, flag_criteria: str, regions: List[str]
) -> List[Dict[str, Any]]:
    """Single-experience version of obscountdb's create_data_list: no
    control/experience pairing, just one input path/name."""
    data_list = []
    dt_start = datetime.strptime(date_start, '%Y%m%d%H')
    dt_end = datetime.strptime(date_end, '%Y%m%d%H')
    delta = timedelta(hours=6)

    current_date = dt_start

    while current_date <= dt_end:
        formatted_date = current_date.strftime('%Y%m%d%H')
        for family in families:
            filename = f'{formatted_date}_{family}'
            filein = os.path.join(input_path, filename)

            if not os.path.exists(filein):
                print(f"[WARNING] Missing file for family '{family}': {filein}", flush=True)
                current_date_local = current_date
            else:
                for region in regions:
                    db_new = os.path.join(
                        work_path, family,
                        f'{name}_{region}_{date_start}_{date_end}_{flag_criteria}_{family}.db')

                    data_list.append({
                        'family': family, 'filein': filein, 'db_new': db_new,
                        'region': region, 'flag_criteria': flag_criteria,
                    })
        current_date += delta
    return data_list


def make_scatter(
    file_in: str, name_in: str, pathwork: str, datestart: str,
    dateend: str, regions: List[str], families: List[str], flag_criteria: str,
    n_cpu: int, agr: Optional[List[str]] = None,
    window_days: int = DEFAULT_WINDOW_DAYS,
    alert_yellow: float = DEFAULT_ALERT_YELLOW,
    alert_orange: float = DEFAULT_ALERT_ORANGE,
    alert_red: float = DEFAULT_ALERT_RED,
    alert_high: float = DEFAULT_ALERT_HIGH,
) -> None:

    agr_list = _norm_agr(agr)

    for family in families:
        pikobs.delete_create_folder(pathwork, family)

    data_list = create_data_list(datestart, dateend, families, file_in, name_in, pathwork, flag_criteria, regions)

    t0 = time.time()

    if n_cpu == 1:
        print(f'[INFO] Serial mode: {len(data_list)} files used in calculating statistics for {name_in}', flush=True)
        for data_ in data_list:
            create_and_populate_moyenne_table(
                data_['family'], data_['db_new'], data_['filein'], data_['region'], data_['flag_criteria'], agr_list
            )
    else:
        print(f'[INFO] Parallel mode: {len(data_list)} files used for {name_in} with {n_cpu} workers.', flush=True)
        with Client(processes=True, threads_per_worker=1, n_workers=n_cpu, silence_logs=50):
            delayed_funcs = [
                dask.delayed(create_and_populate_moyenne_table)(
                    data_['family'], data_['db_new'], data_['filein'], data_['region'], data_['flag_criteria'], agr_list
                ) for data_ in data_list
            ]
            dask.compute(*delayed_funcs)

    tn = time.time()
    print(f'[TIMER] Total time for DB Extraction: {tn - t0:.2f} seconds', flush=True)

    # ---------------- DEDUPE SAFETY NET ----------------
    # Run once per family, unconditionally, right after extraction and
    # before plotting reads any of these files -- see
    # dedupe_moyenne_table()'s docstring for why this is needed even
    # with combine()'s own delete-then-insert protection.
    unique_db_paths = sorted({data_['db_new'] for data_ in data_list})
    for db_path in unique_db_paths:
        dedupe_moyenne_table(db_path)

    # ---------------- PLOTTING SECTION ----------------
    t0 = time.time()
    if n_cpu == 1:
        print(f'[INFO] Serial mode: Generating plots for {len(regions)} regions.', flush=True)
        for region in regions:
            pikobs.obstimedb_plot(
                region, families, datestart, dateend, pathwork, name_in, flag_criteria,
                agr_list, file_in, window_days, alert_yellow, alert_orange, alert_red, alert_high)
    else:
        print(f"[INFO] Parallel mode: Generating plots for {len(regions)} regions.", flush=True)
        with Client(processes=True, threads_per_worker=1, n_workers=n_cpu, silence_logs=50):
            delayed_funcs = [
                dask.delayed(pikobs.obstimedb_plot)(
                    region, families, datestart, dateend, pathwork, name_in, flag_criteria,
                    agr_list, file_in, window_days, alert_yellow, alert_orange, alert_red, alert_high
                ) for region in regions
            ]
            dask.compute(*delayed_funcs)

    print(f'[TIMER] Total time for Plotting: {time.time() - t0:.2f} seconds', flush=True)
    print(f'[SUCCESS] Check outputs in: {pathwork}', flush=True)


def arg_call() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Pikobs ObsTimeDB Single-Experience Time Diagnostics")
    parser.add_argument('--path_experience_files', default='undefined', type=str)
    parser.add_argument('--experience_name', default='undefined', type=str)

    parser.add_argument('--pathwork', default='undefined', type=str)
    parser.add_argument('--datestart', default='undefined', type=str)
    parser.add_argument('--dateend', default='undefined', type=str)
    parser.add_argument('--region', nargs="+", default='undefined', type=str)
    parser.add_argument('--family', nargs="+", default='undefined', type=str)
    parser.add_argument('--flags_criteria', default='undefined', type=str)
    parser.add_argument('--agr', nargs="+", default=None, choices=['omp', 'oma'],
                   help="Overlay AVG(omp) and/or AVG(oma) on the time series "
                        "(secondary Y-axis). Use one or both, e.g. --agr oma omp. "
                        "Omit to disable.")
    parser.add_argument('--window_days', default=DEFAULT_WINDOW_DAYS, type=int,
                   help="Baseline look-back window in calendar days for the "
                        "same synoptic hour (default: 10).")
    parser.add_argument('--alert_yellow', default=DEFAULT_ALERT_YELLOW, type=float,
                   help="Drop threshold (percent) that flags a cycle YELLOW "
                        "vs the same-hour baseline (default: 10.0).")
    parser.add_argument('--alert_orange', default=DEFAULT_ALERT_ORANGE, type=float,
                   help="Drop threshold (percent) that flags a cycle ORANGE "
                        "(default: 15.0).")
    parser.add_argument('--alert_red', default=DEFAULT_ALERT_RED, type=float,
                   help="Drop threshold (percent) that flags a cycle RED — "
                        "also covers a total outage, Nobs=0 (default: 20.0).")
    parser.add_argument('--alert_high', default=DEFAULT_ALERT_HIGH, type=float,
                   help="Rise threshold (percent ABOVE the baseline) that "
                        "flags a cycle DARK GREEN, e.g. 10.0 -> Nobs >= 110%% "
                        "of baseline (default: 10.0).")
    parser.add_argument('--n_cpus', '--n_cpu', default=1, type=int, dest='n_cpus')
    parser.add_argument('--no_submit', action='store_true',
                   help="Skip PBS auto-submission and run locally.")

    args = parser.parse_args()

    if args.agr is not None:
        args.agr = [f for tok in args.agr for f in str(tok).split()]

    for arg in vars(args):
        print(f'--{arg} {getattr(args, arg)}', flush=True)

    if args.path_experience_files == 'undefined': raise ValueError('Missing --path_experience_files')
    if args.experience_name == 'undefined': raise ValueError('Missing --experience_name')
    if args.pathwork == 'undefined': raise ValueError('Missing --pathwork')
    if args.datestart == 'undefined': raise ValueError('Missing --datestart')
    if args.dateend == 'undefined': raise ValueError('Missing --dateend')
    if args.region == 'undefined': raise ValueError('Missing --region')
    if args.family == 'undefined': raise ValueError('Missing --family')
    if args.flags_criteria == 'undefined': raise ValueError('Missing --flags_criteria')

    maybe_submit_to_pbs(args)

    make_scatter(
        file_in=args.path_experience_files, name_in=args.experience_name, pathwork=args.pathwork,
        datestart=args.datestart, dateend=args.dateend, regions=args.region,
        families=args.family, flag_criteria=args.flags_criteria, n_cpu=args.n_cpus,
        agr=args.agr, window_days=args.window_days,
        alert_yellow=args.alert_yellow, alert_orange=args.alert_orange, alert_red=args.alert_red,
        alert_high=args.alert_high
    )


if __name__ == "__main__":
    arg_call()
