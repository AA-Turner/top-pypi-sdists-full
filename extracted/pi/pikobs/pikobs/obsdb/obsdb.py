r"""Where Pikobs touches the observation files.

Every module reads the same thing: one file per 6-h cycle and family,
holding a ``header`` table and a ``data`` table. This module is the only
place that knows how those files are named, how they are opened and how
results are written back, so the day the format changes, this is what has
to be rewritten and nothing else.

What lives here
---------------

``naming``
    where the file of a cycle is and how it is called.
``check_input_files``
    every cycle of every run and family is there, reported as ranges
    before anything is wiped.
``open_cycle``
    a read-only connection to one cycle.
``work_db`` and ``combine``
    the private in-memory database a task aggregates into, and how its
    rows land in the output file.
``attach``
    two cycles open at once, which is what matching control and
    experience observation by observation needs.
``columns``
    the names of the tables and columns, and which optional ones a file
    actually has.

What does NOT live here
-----------------------

The aggregation queries of each module: the conditional sums per region
and criteria, the groupings by station and channel, the pairing join.
Those are the science, they stay with their module, and they are plain
SQL over ``header`` and ``data``.

Changing the format
-------------------

Write a second backend beside ``sqlite``: it has to return, from
``open_cycle``, something that answers ``execute`` over tables named
``header`` and ``data``. If the new format speaks SQL, the modules'
queries keep working untouched; if it does not, the backend converts on
open. Either way the change is confined to this package.

Two rules keep that promise, and they are worth enforcing with a grep:

* no ``import sqlite3`` outside ``pikobs/obsdb``;
* no SQL extension in a module's query (``STDDEV`` and ``isodatetime``
  were removed for this reason).
"""

import hashlib
import os
import re
import sqlite3
import sys
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

CYCLE_HOURS = 6

# The two tables a cycle file holds, and the columns the modules use.
TABLE_HEADER = "header"
TABLE_DATA = "data"

COL = {
    'id_obs':    'id_obs',
    'id_stn':    'id_stn',
    'codtyp':    'codtyp',
    'lat':       'lat',
    'lon':       'lon',
    'date':      'date',
    'time':      'time',
    'varno':     'varno',
    'vcoord':    'vcoord',
    'obsvalue':  'obsvalue',
    'omp':       'omp',
    'oma':       'oma',
    'bias_corr': 'bias_corr',
    'flag':      'flag',
}

__all__ = ["CYCLE_HOURS", "COL", "TABLE_DATA", "TABLE_HEADER", "attach",
           "available_cycles", "check_input_files", "combine", "cycle_path",
           "cycle_ranges", "cycles", "has_columns", "input_size", "open_cycle",
           "split_tokens", "table_columns", "work_db"]


def split_tokens(raw: Any) -> List[str]:
    """Command-line values as a token list: a string or a list of strings,
    split on whitespace, each token once, in order (``"Monde Canada"`` and
    ``["Monde", "Canada Monde"]`` both give ``['Monde', 'Canada']``)."""
    if raw is None:
        return []
    if isinstance(raw, str):
        raw = [raw]
    out: List[str] = []
    for item in raw:
        out.extend(str(item).split())
    seen, uniq = set(), []
    for tok in out:
        if tok and tok not in seen:
            seen.add(tok)
            uniq.append(tok)
    return uniq


# ─────────────────────────────────────────────────────────────────────────────
# Naming: where a cycle lives
# ─────────────────────────────────────────────────────────────────────────────

def cycles(date_start: str, date_end: str) -> List[str]:
    """Every ``YYYYMMDDHH`` of the window, both ends included."""
    cur = datetime.strptime(date_start, '%Y%m%d%H')
    end = datetime.strptime(date_end, '%Y%m%d%H')
    out = []
    while cur <= end:
        out.append(cur.strftime('%Y%m%d%H'))
        cur += timedelta(hours=CYCLE_HOURS)
    return out


def _candidates(run_path: str, cycle: str, family: str) -> List[str]:
    """The names a cycle file may have, in the order they are tried."""
    return [os.path.join(run_path, f"{cycle}_{family}"),
            os.path.join(run_path, f"{cycle}_{family}.db")]


def cycle_path(run_path: str, cycle: str, family: str) -> str:
    """Path of one cycle; the first candidate when none exists yet."""
    for cand in _candidates(run_path, cycle, family):
        if os.path.isfile(cand):
            return cand
    return _candidates(run_path, cycle, family)[0]


def cycle_exists(run_path: str, cycle: str, family: str) -> bool:
    return any(os.path.isfile(c) for c in _candidates(run_path, cycle, family))


def available_cycles(run_path: str, family: str) -> List[str]:
    """Which cycles of a family the directory really holds."""
    try:
        pat = re.compile(rf'^(\d{{10}})_{re.escape(family)}(\.db)?$')
        return sorted(m.group(1) for m in
                      (pat.match(e.name) for e in os.scandir(run_path)) if m)
    except OSError:
        return []


def input_size(runs: Sequence[Tuple[str, str]], families: Sequence[str],
               cycle_list: Sequence[str]) -> Tuple[int, int]:
    """How many files the run will read, and how much they weigh."""
    n, size = 0, 0
    for _, path in runs:
        for family in families:
            for cycle in cycle_list:
                for cand in _candidates(path, cycle, family):
                    if os.path.isfile(cand):
                        size += os.path.getsize(cand)
                        n += 1
                        break
    return n, size


def fmt_bytes(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}"
        n /= 1024.0


# ─────────────────────────────────────────────────────────────────────────────
# Input check
# ─────────────────────────────────────────────────────────────────────────────

def cycle_ranges(missing: Sequence[str]) -> List[str]:
    """Consecutive cycles collapsed into ranges, for a readable report."""
    step = timedelta(hours=CYCLE_HOURS)
    out, start, prev = [], None, None
    for c in sorted(missing):
        t = datetime.strptime(c, '%Y%m%d%H')
        if start is not None and t - prev == step:
            prev = t
            continue
        if start is not None:
            out.append(_fmt_range(start, prev, step))
        start = prev = t
    if start is not None:
        out.append(_fmt_range(start, prev, step))
    return out


def _fmt_range(a: datetime, b: datetime, step: timedelta) -> str:
    if a == b:
        return a.strftime('%Y%m%d%H')
    n = int((b - a) / step) + 1
    return f"{a:%Y%m%d%H} .. {b:%Y%m%d%H} ({n} cycles)"


def check_input_files(runs: Sequence[Tuple[str, str]],
                      families: Sequence[str], date_start: str,
                      date_end: str, module: str = "pikobs",
                      strict: bool = True) -> bool:
    """Is every 6-h file of the window there?

    Called before the output directory is wiped: a typo in the dates used
    to erase the previous report and only then fail. When something is
    missing it prints the gaps as ranges and the dates the directory does
    hold.

    strict=True (the default) returns False and the module stops: every
    number would rest on a different set of cycles. strict=False only
    warns and returns True, for a module that can carry on with the
    cycles it has -- the missing ones simply count zero.
    """
    cycle_list = cycles(date_start, date_end)
    problems: List[str] = []

    for name, path in runs:
        if not os.path.isdir(path):
            problems += [f"run '{name}'  ({path})", "    directory not found"]
            continue
        for family in families:
            missing = [c for c in cycle_list
                       if not cycle_exists(path, c, family)]
            if not missing:
                continue
            problems.append(f"run '{name}'  family '{family}'  ({path})")
            problems.append(f"    missing {len(missing)}/{len(cycle_list)} "
                            f"cycles:")
            ranges = cycle_ranges(missing)
            problems += [f"      {r}" for r in ranges[:10]]
            if len(ranges) > 10:
                problems.append(f"      ... (+{len(ranges) - 10} more gaps)")
            avail = available_cycles(path, family)
            if avail:
                problems.append(f"    available for '{family}': {avail[0]} .. "
                                f"{avail[-1]} ({len(avail)} files)")
            else:
                problems.append(f"    no '*_{family}' file in this directory")

    if not problems:
        n_files, n_bytes = input_size(runs, families, cycle_list)
        print(f"[{module}] input check OK: {len(cycle_list)} cycles x "
              f"{len(runs)} run(s) x {len(families)} family(ies), "
              f"{n_files} files, {fmt_bytes(n_bytes)}", flush=True)
        # will it fit the job? a warning only, never a stop
        try:
            from pikobs.parallel.parallel import memory_advice
            memory_advice(module, [
                os.path.getsize(p) for p in
                (os.path.join(path, f"{c}_{family}")
                 for _, path in runs for family in families
                 for c in cycle_list)
                if os.path.isfile(p)])
        except Exception:
            pass
        # and how long it may take, roughly: one line, never a stop
        try:
            from pikobs.parallel.parallel import time_estimate
            time_estimate(module, n_bytes, len(runs))
        except Exception:
            pass
        return True

    bar = "=" * 70
    head = ("ERROR: missing 6-h input files, nothing was run "
            "(PATHWORK left untouched)." if strict else
            "WARNING: some 6-h input files are missing; the run goes on "
            "and those cycles count zero.")
    tail = ("Fix DATESTART / DATEEND or the input paths and run again."
            if strict else
            "Check DATESTART / DATEEND or the input paths if this is not "
            "expected.")
    for line in ([bar, head,
                  f"Window {date_start} .. {date_end} = {len(cycle_list)} "
                  f"cycles", ""] + problems + ["", tail, bar]):
        print(f"[{module}] {line}", file=sys.stderr, flush=True)
    return not strict


# ─────────────────────────────────────────────────────────────────────────────
# Connections
# ─────────────────────────────────────────────────────────────────────────────

@contextmanager
def open_cycle(path: str, read_only: bool = True, mmap: bool = True):
    """A connection to one cycle file, closed whatever happens.

    ``path`` is what :func:`cycle_path` returned. The connection answers
    ``execute`` over the ``header`` and ``data`` tables; that is the whole
    contract a module may rely on.
    """
    uri = f"file:{path}?mode=ro" if read_only else path
    conn = sqlite3.connect(uri, uri=read_only, isolation_level=None,
                           timeout=9_999)
    try:
        if mmap:
            try:
                conn.execute("PRAGMA mmap_size = 536870912;")
            except sqlite3.Error:
                pass
        yield conn
    finally:
        conn.close()


@contextmanager
def work_db(attach: Optional[Dict[str, str]] = None):
    """A private in-memory database for one task.

    The name is unique per call and the connection is always closed. Both
    matter: a shared name with no close is what made one worker carry its
    rows into the next file and double the counts, twice, in two
    different modules.

    ``attach`` maps a schema name to a file to attach, e.g.
    ``{'db': cycle_path}``.
    """
    uri = f"file:pikobs_{uuid.uuid4().hex}?mode=memory&cache=shared"
    conn = sqlite3.connect(uri, uri=True, isolation_level=None,
                           timeout=9_999_999)
    try:
        conn.execute("PRAGMA journal_mode = MEMORY;")
        conn.execute("PRAGMA synchronous = OFF;")
        conn.execute("PRAGMA temp_store = MEMORY;")
        for schema, path in (attach or {}).items():
            conn.execute(f"ATTACH DATABASE ? AS {schema};", (path,))
        # a query may hold the mask of an irregular region; the module
        # that built the condition does not have to register it here
        try:
            from pikobs.configobs import regionsobs
            regionsobs.register_pending(conn)
        except Exception:
            pass
        yield conn, uri
    finally:
        conn.close()


@contextmanager
def attach(paths: Dict[str, str]):
    """Several cycles open at once, under the schema names given.

    Used by the matching of control and experience, where two files have
    to be joined observation by observation.
    """
    with work_db(attach=paths) as (conn, _):
        yield conn


def combine(out_path: str, source_uri: str, table: str, columns: str,
            ddl: Optional[str] = None, module: str = "pikobs") -> None:
    """Move the rows a task produced into the output database, once.

    Serialised by SQLite itself: every worker writes to the same file, so
    the insert runs inside ``BEGIN IMMEDIATE``. Two things make it safe
    when dask re-runs a task whose worker died:

    * the journal is on, so a transaction cut half-way is rolled back
      whole and leaves no partial rows behind;
    * each delivery is fingerprinted (sha1 of its rows) and recorded in
      ``_pikobs_done`` in the same transaction. A delivery already there
      is skipped and the log says so. With the journal off and no record,
      a retried task used to put its rows in twice: whole cycles counted
      double, silently.
    """
    conn = sqlite3.connect(out_path, uri=True, isolation_level=None,
                           timeout=9_999)
    try:
        conn.execute("PRAGMA journal_mode=DELETE;")
        conn.execute("PRAGMA synchronous=OFF;")
        if ddl:
            conn.execute(ddl)
        conn.execute("CREATE TABLE IF NOT EXISTS _pikobs_done "
                     "(tbl TEXT, digest TEXT, n INTEGER, "
                     "PRIMARY KEY (tbl, digest));")
        conn.execute("ATTACH DATABASE ? AS src;", (source_uri,))
        digest, n = hashlib.sha1(), 0
        for row in conn.execute(f"SELECT {columns} FROM src.{table};"):
            digest.update(repr(row).encode())
            n += 1
        digest = digest.hexdigest()
        conn.execute("BEGIN IMMEDIATE;")
        try:
            done = conn.execute("SELECT 1 FROM _pikobs_done "
                                "WHERE tbl = ? AND digest = ?;",
                                (table, digest)).fetchone()
            if done:
                conn.execute("ROLLBACK;")
                if n:
                    print(f"[{module}] {n} rows already combined into "
                          f"{os.path.basename(out_path)} ({table}), skipped "
                          f"(a retried task)", file=sys.stderr, flush=True)
            else:
                conn.execute(f"INSERT INTO {table} ({columns}) "
                             f"SELECT {columns} FROM src.{table};")
                conn.execute("INSERT INTO _pikobs_done VALUES (?, ?, ?);",
                             (table, digest, n))
                conn.execute("COMMIT;")
        except BaseException:
            try:
                conn.execute("ROLLBACK;")
            except sqlite3.Error:
                pass
            raise
        conn.execute("DETACH DATABASE src;")
    except sqlite3.Error as exc:
        print(f"[{module}] combining into {os.path.basename(out_path)} "
              f"failed: {exc}", file=sys.stderr, flush=True)
        raise
    finally:
        conn.close()


@contextmanager
def open_result(path: str, ddl: Optional[str] = None):
    """A connection to a database this run produced (read or write)."""
    conn = sqlite3.connect(path, isolation_level=None, timeout=9_999)
    try:
        if ddl:
            conn.execute(ddl)
        yield conn
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# Columns
# ─────────────────────────────────────────────────────────────────────────────

def table_columns(conn, table: str, schema: str = "") -> List[str]:
    """Lower-cased column names of a table, empty when it is not there."""
    prefix = f"{schema}." if schema else ""
    try:
        return [r[1].lower() for r in
                conn.execute(f"PRAGMA {prefix}table_info('{table}');")]
    except sqlite3.Error:
        return []


def has_columns(conn, table: str, names: Iterable[str],
                schema: str = "") -> Dict[str, bool]:
    """Which optional columns this file has, e.g. BIAS_CORR or CODTYP."""
    present = set(table_columns(conn, table, schema))
    return {n: n.lower() in present for n in names}


_cycle_ranges = cycle_ranges        # the old private name, for the callers that still use it
