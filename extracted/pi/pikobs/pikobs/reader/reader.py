r"""
==============================================
pikobs.reader -- One cycle of two runs, summed
==============================================

Every comparing module used to do the same thing in its own SQL: open the
control and the experience of one cycle, keep the useful rows, pair them
or not, sum them per region and flag, and group them by channel or level.
That is about thirty queries in eleven modules, each with its own small
differences. This module does it once.

A module says what it wants in an :class:`Ask` -- the family, the cells
(region x surface x flag), the groups (name -> SQL expression), the values
(omp, oma) and the mode -- and :func:`read_cycle` gives back the standard
sums of that cycle, one row per cell and group. A period is the sum of
its cycles, so any window, any coarser grouping and any test on the cycles
can be rebuilt from these rows without reading a file again.

The sums
--------

For every value ``v`` asked (``omp``, ``oma`` ...), with c the control and
e the experience:

``nc_v``, ``ne_v``
    the counts behind the sums. With MATCH on they are the same number,
    the pairs.
``sc_v``, ``sc2_v``, ``se_v``, ``se2_v``
    the sums and the sums of squares of each run.
``sce_v``
    the sum of the products c x e, MATCH on only (NULL otherwise).
``nallc_v``, ``nalle_v``
    how many observations each run holds in the cell, paired or not.
    With MATCH off or no they equal ``nc_v`` / ``ne_v``; with MATCH on
    they give the share of each run that was matched, and the change in
    the number of observations used (more radiances passing the
    background check is a result in itself).

One run only (``exp_file=None``, MATCH off or no) fills the c columns.

The modes
---------

``on``   the observations both runs hold, paired with :mod:`pikobs.match`
         (one to one by value inside a repeated key). A pair counts in a
         cell when the observation passes the cell in both runs, each run
         with its own flag.
``off``  each run with all its observations.
``no``   the same sums as off; the module just draws no test.

What it is not, yet
-------------------

``extra_sums`` (the bins and moments 3 and 4 of histogram, the flag bits
of flags) are part of the contract and raise ``NotImplementedError`` until
a module that needs them moves here.

The rules of :mod:`pikobs.obsdb` hold: no ``sqlite3`` here, no SQL
extension. Header and data are joined with ``NATURAL JOIN``, as in every
module, so the family expressions (``ROUND(VCOORD / 2000.) * 2000``) and
the criteria (``lat``, ``flag``) keep their bare column names.
"""

import os
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Tuple

import pandas as pd

import pikobs
from pikobs.configobs import regionsobs
from pikobs.configobs.landmask import register_surface, surface_sql
from pikobs.configobs.special_family import special_select
from pikobs.match import (DEFAULT_KEY, FIELDS, MatchSpec, count_repeats,
                          key_aliases, key_join, key_select)
from pikobs.obsdb import open_result, table_columns, work_db

__all__ = ["Ask", "Cell", "CycleSums", "MODES", "cells", "done_cycles",
           "read_cycle", "sum_columns", "write_sums"]

MODES = ("on", "off", "no")

#: the data columns a value may be; anything else is refused, since it is
#: pasted into the SQL
VALUES = ("omp", "oma", "bias_corr", "obs_error", "obsvalue")

#: the sums of one value, in the order of the output columns
_SUMS = ("nc", "sc", "sc2", "ne", "se", "se2", "sce", "nallc", "nalle")


class Cell(NamedTuple):
    """One selection of a cycle: a region, a surface and a flag criterion,
    the SQL condition they make together, and the condition of the place
    alone (region and surface), for a run read without the flag."""
    region: str
    flag: str
    land_ocean: str
    cond: str
    place: str = ""


def cells(regions: Sequence[str], flags: Sequence[str],
          land_oceans: Sequence[str] = ("all",)) -> Tuple[Cell, ...]:
    """Every (region, surface, flag) of a run, with its condition.

    The same SQL as vdedr builds, so a module moving here gives the same
    numbers."""
    out = []
    for region in regions:
        latlon = regionsobs.criteria(region)
        for land_ocean in land_oceans or ("all",):
            surf = surface_sql(land_ocean)
            for flag in flags:
                out.append(Cell(region, flag, land_ocean,
                                f"((1=1 {latlon}) AND (1=1 "
                                f"{pikobs.flag_criteria(flag)}){surf})",
                                f"((1=1 {latlon}){surf})"))
    return tuple(out)


@dataclass(frozen=True)
class Ask:
    """What a module wants from one cycle.

    family
        the family, as ``pikobs.family`` knows it.
    cells
        the selections, from :func:`cells`.
    group
        ``(name, SQL expression)`` pairs, the expression over the header
        and the data of one file (bare names, or ``h.`` / ``d.``): the
        channel, a layer, a latitude band, U and V as one wind ... An
        empty group sums the whole cell.
    varnos
        the BUFR codes to read; empty means the family's own.
    values
        the data columns to sum.
    match
        ``on``, ``off`` or ``no``.
    key
        the fields of the pairing key (MATCH on).
    special_column
        add the family's special column (sw method, radar elevation) as a
        group named ``special``.
    flag_on
        ``both`` (the default): a pair counts when the observation passes
        the flag criterion in both runs. ``exp``: the criterion is applied
        to the experience only, and the control is read with the place of
        the cell alone -- for a control that does not assimilate the family
        at all (no radar in its analysis), read from its bgckalt: the pairs
        are then what the experience assimilated, with the background of
        the control on the same observations.
    where
        an extra SQL condition, e.g. a station selection.
    extra_sums
        reserved: raises NotImplementedError when not empty.
    """
    family: str
    cells: Tuple[Cell, ...]
    group: Tuple[Tuple[str, str], ...] = ()
    varnos: Tuple[int, ...] = ()
    values: Tuple[str, ...] = ("omp", "oma")
    match: str = "on"
    key: Tuple[str, ...] = DEFAULT_KEY
    special_column: bool = False
    where: str = ""
    extra_sums: Tuple[str, ...] = field(default_factory=tuple)
    flag_on: str = "both"

    def __post_init__(self):
        if isinstance(self.group, dict):
            object.__setattr__(self, "group", tuple(self.group.items()))
        object.__setattr__(self, "cells", tuple(self.cells))
        object.__setattr__(self, "varnos", tuple(int(v) for v in self.varnos))
        object.__setattr__(self, "values", tuple(self.values))
        object.__setattr__(self, "key", tuple(self.key))
        if self.match not in MODES:
            raise ValueError(f"Ask.match: {self.match!r}, not one of {MODES}")
        if self.flag_on not in ("both", "exp"):
            raise ValueError(f"Ask.flag_on: {self.flag_on!r}, not 'both' or 'exp'")
        if self.flag_on == "exp" and any(not c.place for c in self.cells):
            raise ValueError("Ask.flag_on='exp' needs cells made by cells()")
        bad = [v for v in self.values if v not in VALUES]
        if bad:
            raise ValueError(f"Ask.values: {bad}; allowed: {VALUES}")
        bad = [k for k in self.key if k not in FIELDS]
        if bad:
            raise ValueError(f"Ask.key: {bad}; allowed: {tuple(FIELDS)}")
        names = [n for n, _ in self.group]
        bad = [n for n in names if not n.isidentifier() or n in _RESERVED]
        if bad or len(set(names)) != len(names):
            raise ValueError(f"Ask.group: names must be distinct identifiers, "
                             f"not {sorted(_RESERVED)}; got {names}")
        if not self.cells:
            raise ValueError("Ask.cells: at least one cell")

    @property
    def group_names(self) -> List[str]:
        return [n for n, _ in self.group] + (["special"] if self.special_column else [])


_RESERVED = {"cycle", "region", "flag", "land_ocean", "special"}


class CycleSums(NamedTuple):
    """The sums of one cycle (a DataFrame, one row per cell and group) and
    what the pairing saw (observations, pairs, repeated keys)."""
    rows: pd.DataFrame
    info: Dict[str, int]


def sum_columns(ask: Ask) -> List[str]:
    """The sum columns of an Ask, in order: nc_omp, sc_omp ... nalle_oma."""
    return [f"{s}_{v}" for v in ask.values for s in _SUMS]


def columns(ask: Ask) -> List[str]:
    """Every column of the rows read_cycle returns."""
    return (["cycle", "region", "flag", "land_ocean"] + ask.group_names
            + sum_columns(ask))


# ─────────────────────────────────────────────────────────────────────────────
# The SQL of one run
# ─────────────────────────────────────────────────────────────────────────────

def _side_sql(conn, schema: str, ask: Ask, with_key: bool) -> Tuple[str, List[str]]:
    """SELECT giving, for every useful row of one run, its group columns
    (g_*), whether it is in each cell (in_*), its values (v_*) and, for the
    pairing, its key. Returns (sql, the values the file really has)."""
    FAM, VCOORD, VCOCRIT, STATB, ELEM, VCOTYP = pikobs.family(ask.family)
    varnos = ",".join(str(v) for v in ask.varnos) if ask.varnos else ELEM
    head = table_columns(conn, "header", schema)
    data = table_columns(conn, "data", schema)
    items = []
    if with_key:
        items.append(key_select(MatchSpec(True, ask.key), h="h", d="d"))
    for name, expr in ask.group:
        items.append(f"({expr}) AS g_{name}")
    if ask.special_column:
        sp, _ = special_select(ask.family, head, True, prefix="h.")
        items.append(f"{sp} AS g_special")
    # the control read without the flag when the criterion is the experience's
    bare = ask.flag_on == "exp" and schema == "c"
    for i, c in enumerate(ask.cells):
        items.append(f"(CASE WHEN {c.place if bare else c.cond} THEN 1 ELSE 0 END) AS in_{i}")
    have = [v for v in ask.values if v in data]
    for v in ask.values:
        # a departure stored as '' is not NULL and would be summed as zero
        items.append(f"(CASE WHEN typeof(d.{v}) IN ('real', 'integer') "
                     f"THEN d.{v} END) AS v_{v}" if v in have else f"NULL AS v_{v}")
    any_value = " OR ".join(f"d.{v} IS NOT NULL" for v in have) or "0"
    sql = (f"SELECT {', '.join(items)} "
           f"FROM {schema}.header AS h NATURAL JOIN {schema}.data AS d "
           f"WHERE varno IN ({varnos}) AND obsvalue IS NOT NULL "
           f"AND ({any_value}) {VCOCRIT} "
           + (f"AND ({ask.where})" if ask.where.strip() else ""))
    return sql, have


def _g(ask: Ask, alias: str = "") -> List[str]:
    p = f"{alias}." if alias else ""
    return [f"{p}g_{n}" for n in ask.group_names]


def _group_by(cols: List[str]) -> str:
    return f"GROUP BY {', '.join(cols)}" if cols else ""


def _apart(conn, schema: str, ask: Ask) -> Dict[tuple, List[float]]:
    """MATCH off / no: the sums of one run, {group: [n, s, s2] per cell
    and value}."""
    sql, _ = _side_sql(conn, schema, ask, with_key=False)
    g = _g(ask)
    sums = ["COUNT(*)"]                 # the useful rows, whatever the cell
    for i in range(len(ask.cells)):
        for v in ask.values:
            ok = f"in_{i} = 1 AND v_{v} IS NOT NULL"
            sums += [f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END)",
                     f"SUM(CASE WHEN {ok} THEN v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN v_{v} * v_{v} END)"]
    rows = conn.execute(f"SELECT {', '.join(g + sums)} FROM ({sql}) "
                        f"{_group_by(g)};").fetchall()
    k = len(g)
    return {tuple(r[:k]): list(r[k:]) for r in rows}   # [rows, n, s, s2, n, s, s2 ...]


# ─────────────────────────────────────────────────────────────────────────────
# The cycle
# ─────────────────────────────────────────────────────────────────────────────

def read_cycle(ctl_file: str, exp_file: Optional[str], ask: Ask, cycle,
               pathwork: str = ".", module: str = "reader") -> Optional[CycleSums]:
    """The standard sums of one cycle, one row per cell and group.

    ``ctl_file`` / ``exp_file`` are the files of that cycle (any stage:
    the caller may give a bgckalt for one run and a postalt for the
    other). ``exp_file=None`` reads one run, MATCH off or no. Returns None
    when a file is missing or holds no header / data table; the caller
    says so and carries on with the other cycles.
    """
    if ask.extra_sums:
        raise NotImplementedError(f"extra_sums {ask.extra_sums}: not in reader v0")
    single = exp_file is None
    if single and ask.match == "on":
        raise ValueError("MATCH on needs two runs")
    files = {"c": ctl_file} if single else {"c": ctl_file, "e": exp_file}
    for f in files.values():
        if not os.path.isfile(f):
            print(f"[{module}] missing file, cycle {cycle} skipped: {f}",
                  file=sys.stderr, flush=True)
            return None

    with work_db(attach=files) as (conn, _):
        regionsobs.register_pending(conn)
        # the polygons of the cells, by name: the cells may have been built in
        # another process (a dask worker has none of its parent's registrations)
        regionsobs.register(conn, sorted({c.region for c in ask.cells}), pathwork)
        register_surface(conn, [c.land_ocean for c in ask.cells], pathwork)
        for s, f in files.items():
            if not (table_columns(conn, "header", s) and table_columns(conn, "data", s)):
                print(f"[{module}] no header / data table, cycle {cycle} "
                      f"skipped: {f}", file=sys.stderr, flush=True)
                return None
        if ask.match == "on":
            merged, info = _paired(conn, ask)
        else:
            merged, info = {}, {}
            for s, side in (("c", 0), ("e", 1)):
                if s not in files:
                    continue
                total = 0
                for gkey, vals in _apart(conn, s, ask).items():
                    total += vals[0] or 0
                    per = merged.setdefault(gkey, _empty(ask))
                    for i in range(len(ask.cells)):
                        for j in range(len(ask.values)):
                            n, sm, s2 = vals[1 + 3 * (i * len(ask.values) + j):][:3]
                            cell = per[i][j]
                            base = 0 if side == 0 else 3
                            cell[base:base + 3] = [n or 0, sm or 0.0, s2 or 0.0]
                            cell[7 + side] = n or 0
                # counted once per row: the regions overlap, a sum over the
                # cells would count the tropics twice
                info[f"obs_{s}"] = int(total)

    out = []
    for gkey, per in merged.items():
        for i, c in enumerate(ask.cells):
            row = [x for j in range(len(ask.values)) for x in per[i][j]]
            if not any(row[k] for j in range(len(ask.values))
                       for k in (9 * j, 9 * j + 3, 9 * j + 7, 9 * j + 8)):
                continue
            out.append([int(cycle), c.region, c.flag, c.land_ocean, *gkey, *row])
    df = pd.DataFrame(out, columns=columns(ask))
    if ask.match != "on":
        for v in ask.values:
            df[f"sce_{v}"] = float("nan")
    if single:
        for v in ask.values:
            for s in ("ne", "se", "se2", "nalle"):
                df[f"{s}_{v}"] = float("nan")
    return CycleSums(df, info)


def _empty(ask: Ask) -> List[List[List[float]]]:
    """[cell][value] -> the nine sums, zero."""
    return [[[0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0] for _ in ask.values]
            for _ in ask.cells]


def _paired(conn, ask: Ask) -> Tuple[Dict[tuple, list], Dict[str, int]]:
    """MATCH on: the pairs of the two runs and each run's own count."""
    spec = MatchSpec(True, ask.key)
    info: Dict[str, int] = {}
    for s in ("c", "e"):
        sql, _ = _side_sql(conn, s, ask, with_key=True)
        conn.execute(f"CREATE TEMP TABLE side_{s} AS {sql};")
        conn.execute(f"CREATE INDEX temp.idx_{s} ON side_{s} "
                     f"({', '.join(key_aliases(spec))});")
        k, r = count_repeats(conn, f"side_{s}", spec)
        info[f"obs_{s}"] = conn.execute(f"SELECT COUNT(*) FROM side_{s};").fetchone()[0]
        info[f"rep_keys_{s}"], info[f"rep_rows_{s}"] = k, r
    info["pairs"] = conn.execute(
        f"SELECT COUNT(*) FROM side_c AS c JOIN side_e AS e ON {key_join(spec)};"
    ).fetchone()[0]

    merged: Dict[tuple, list] = {}
    nv = len(ask.values)
    # each run's own count, paired or not
    for side, s in enumerate(("c", "e")):
        g = _g(ask)
        cnt = [f"SUM(CASE WHEN in_{i} = 1 AND v_{v} IS NOT NULL THEN 1 ELSE 0 END)"
               for i in range(len(ask.cells)) for v in ask.values]
        for r in conn.execute(f"SELECT {', '.join(g + cnt)} FROM side_{s} "
                              f"{_group_by(g)};"):
            per = merged.setdefault(tuple(r[:len(g)]), _empty(ask))
            for i in range(len(ask.cells)):
                for j in range(nv):
                    per[i][j][7 + side] = r[len(g) + i * nv + j] or 0
    # the pairs, grouped as the control has them
    g = _g(ask, "c")
    sums = []
    for i in range(len(ask.cells)):
        for v in ask.values:
            ok = (f"c.in_{i} = 1 AND e.in_{i} = 1 "
                  f"AND c.v_{v} IS NOT NULL AND e.v_{v} IS NOT NULL")
            sums += [f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END)",
                     f"SUM(CASE WHEN {ok} THEN c.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN c.v_{v} * c.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN e.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN e.v_{v} * e.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN c.v_{v} * e.v_{v} END)"]
    for r in conn.execute(f"SELECT {', '.join(g + sums)} FROM side_c AS c "
                          f"JOIN side_e AS e ON {key_join(spec)} {_group_by(g)};"):
        per = merged.setdefault(tuple(r[:len(g)]), _empty(ask))
        for i in range(len(ask.cells)):
            for j in range(nv):
                n, sc, sc2, se, se2, sce = r[len(g) + 6 * (i * nv + j):][:6]
                n = n or 0
                per[i][j][:7] = [n, sc or 0.0, sc2 or 0.0, n, se or 0.0,
                                 se2 or 0.0, sce or 0.0]
    for s in ("c", "e"):
        conn.execute(f"DROP TABLE side_{s};")
    return merged, info


# ─────────────────────────────────────────────────────────────────────────────
# Keeping the sums of every cycle
# ─────────────────────────────────────────────────────────────────────────────

_DONE = ("CREATE TABLE IF NOT EXISTS _reader_cycles "
         "(tbl TEXT, cycle INTEGER, n_rows INTEGER, PRIMARY KEY (tbl, cycle));")


def write_sums(sums: CycleSums, out_path: str, table: str, cycle) -> int:
    """Store the rows of one cycle in ``table`` of ``out_path``, replacing
    what that cycle had: running a cycle again never counts it twice. The
    cycle is recorded as done, even when it gave no row, so a longer
    period only reads the cycles it does not have yet."""
    df = sums.rows
    cols = list(df.columns)

    def sql_type(col: str) -> str:
        # by the name, never by the data: the first cycle written may have
        # no row, and an empty frame would make every column TEXT, and
        # every number stored after it a string. A group column has no
        # type, so it keeps what it is given (a varno, a level, a name).
        if col == "cycle":
            return "INTEGER"
        if col in ("region", "flag", "land_ocean"):
            return "TEXT"
        if col.split("_", 1)[0] in _SUMS:
            return "REAL"
        return ""
    ddl = (f"CREATE TABLE IF NOT EXISTS {table} ("
           + ", ".join(f"{c} {sql_type(c)}".strip() for c in cols) + ");")
    with open_result(out_path) as conn:
        conn.execute(ddl)
        conn.execute(_DONE)
        conn.execute("BEGIN IMMEDIATE;")
        try:
            conn.execute(f"DELETE FROM {table} WHERE cycle = ?;", (int(cycle),))
            if len(df):
                conn.executemany(
                    f"INSERT INTO {table} ({', '.join(cols)}) "
                    f"VALUES ({', '.join('?' * len(cols))});",
                    [tuple(None if pd.isna(x) else x for x in r)
                     for r in df.itertuples(index=False)])
            conn.execute("INSERT OR REPLACE INTO _reader_cycles VALUES (?, ?, ?);",
                         (table, int(cycle), len(df)))
            conn.execute("COMMIT;")
        except BaseException:
            conn.execute("ROLLBACK;")
            raise
    return len(df)


def done_cycles(out_path: str, table: str) -> List[int]:
    """The cycles already stored in ``table``."""
    if not os.path.isfile(out_path):
        return []
    with open_result(out_path) as conn:
        conn.execute(_DONE)
        return [r[0] for r in conn.execute(
            "SELECT cycle FROM _reader_cycles WHERE tbl = ? ORDER BY cycle;",
            (table,))]
