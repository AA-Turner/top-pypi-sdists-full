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
    key_exprs
        a pairing key of the module's own, ``(name, SQL expression)``
        pairs over ``h.`` / ``d.``, used instead of ``key`` when given: the
        radar pairs on the time of its sweep, the azimuth, the elevation
        and the range, whose column names vary from file to file.
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
        the control on the same observations. ``ctl``: the other way
        round, the criterion on the control only and the experience read
        with the place of the cell (zone: the cell of a pair is the
        control's).
    where
        an extra SQL condition every row must meet: a station selection,
        the quality gates of GPS-RO, a departure that must be there.
    exprs
        ``(name, SQL expression)`` pairs summed exactly like values: a
        departure divided by a reference profile (GPS-RO) ... The
        expression sees the header and the data of one file.
    functions
        ``(name, number of arguments, function)`` registered as SQL
        functions before reading, for the expressions that need one
        (``ro_ref``). Module-level functions: a Dask worker pickles the Ask.
    counts
        ``(name, SQL condition)`` pairs: per cell, how many rows of each
        run meet the condition (``kc_<name>``, ``ke_<name>``) -- the
        rejected, the assimilated.
    extremes
        values (or exprs) whose minimum and maximum per cell each run
        holds (``minc_<v>``, ``maxc_<v>``, ``mine_<v>``, ``maxe_<v>``).
    distinct
        an SQL expression whose distinct values per cell are counted for
        each run (``nuniqc``, ``nuniqe``): ``id_obs`` gives the profiles.
    pre
        ``(name, SQL expression)`` pairs over the data columns (bare names),
        computed once per observation and read as ``d.<name>`` by the
        groups, values, exprs, counts and where: ``("ref",
        "ro_ref(vcoord)")`` calls ro_ref once, not at every use.
    extra_sums
        reserved (the bins of histogram): raises NotImplementedError when
        not empty.

    counts, extremes and distinct are taken over each run's own rows in the
    cell, paired or not, as nallc / nalle are.
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
    exprs: Tuple[Tuple[str, str], ...] = ()
    functions: Tuple[Tuple[str, int, Any], ...] = ()
    counts: Tuple[Tuple[str, str], ...] = ()
    extremes: Tuple[str, ...] = ()
    distinct: str = ""
    pre: Tuple[Tuple[str, str], ...] = ()
    key_exprs: Tuple[Tuple[str, str], ...] = ()

    def __post_init__(self):
        for name in ("group", "exprs", "counts", "pre", "key_exprs"):
            if isinstance(getattr(self, name), dict):
                object.__setattr__(self, name, tuple(getattr(self, name).items()))
            else:
                object.__setattr__(self, name, tuple(tuple(x) for x in getattr(self, name)))
        object.__setattr__(self, "cells", tuple(self.cells))
        object.__setattr__(self, "varnos", tuple(int(v) for v in self.varnos))
        object.__setattr__(self, "values", tuple(self.values))
        object.__setattr__(self, "key", tuple(self.key))
        object.__setattr__(self, "functions", tuple(tuple(f) for f in self.functions))
        object.__setattr__(self, "extremes", tuple(self.extremes))
        if self.match not in MODES:
            raise ValueError(f"Ask.match: {self.match!r}, not one of {MODES}")
        if self.flag_on not in ("both", "exp", "ctl"):
            raise ValueError(f"Ask.flag_on: {self.flag_on!r}, not 'both', 'exp' or 'ctl'")
        if self.flag_on in ("exp", "ctl") and any(not c.place for c in self.cells):
            raise ValueError(f"Ask.flag_on={self.flag_on!r} needs cells made by cells()")
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
        vn = self.value_names
        if any(not n.isidentifier() for n in vn) or len(set(vn)) != len(vn):
            raise ValueError(f"Ask.values and Ask.exprs: distinct identifiers; got {vn}")
        cn = [n for n, _ in self.counts]
        if any(not n.isidentifier() for n in cn) or len(set(cn)) != len(cn):
            raise ValueError(f"Ask.counts: distinct identifiers; got {cn}")
        bad = [v for v in self.extremes if v not in vn]
        if bad:
            raise ValueError(f"Ask.extremes: {bad} are not values nor exprs")
        kn = [n for n, _ in self.key_exprs]
        if any(not n.isidentifier() for n in kn) or len(set(kn)) != len(kn):
            raise ValueError(f"Ask.key_exprs: distinct identifiers; got {kn}")
        if set(kn) & {n for n, _ in self.counts}:
            raise ValueError("Ask.key_exprs and Ask.counts share a name")
        if not self.cells:
            raise ValueError("Ask.cells: at least one cell")

    @property
    def group_names(self) -> List[str]:
        return [n for n, _ in self.group] + (["special"] if self.special_column else [])

    @property
    def value_names(self) -> List[str]:
        """The values summed: the columns, then the expressions."""
        return list(self.values) + [n for n, _ in self.exprs]

    @property
    def n_extra(self) -> int:
        """How many extra results one cell has, for one run."""
        return len(self.counts) + 2 * len(self.extremes) + (1 if self.distinct else 0)


_RESERVED = {"cycle", "region", "flag", "land_ocean", "special"}


class CycleSums(NamedTuple):
    """The sums of one cycle (a DataFrame, one row per cell and group) and
    what the pairing saw (observations, pairs, repeated keys)."""
    rows: pd.DataFrame
    info: Dict[str, int]


def sum_columns(ask: Ask) -> List[str]:
    """The sum columns of an Ask, in order: nc_omp, sc_omp ... nalle_oma."""
    return [f"{s}_{v}" for v in ask.value_names for s in _SUMS]


def extra_columns(ask: Ask) -> List[str]:
    """The columns of counts, extremes and distinct, in order."""
    cols = []
    for name, _ in ask.counts:
        cols += [f"kc_{name}", f"ke_{name}"]
    for v in ask.extremes:
        cols += [f"minc_{v}", f"maxc_{v}", f"mine_{v}", f"maxe_{v}"]
    if ask.distinct:
        cols += ["nuniqc", "nuniqe"]
    return cols


def columns(ask: Ask) -> List[str]:
    """Every column of the rows read_cycle returns."""
    return (["cycle", "region", "flag", "land_ocean"] + ask.group_names
            + sum_columns(ask) + extra_columns(ask))


# ─────────────────────────────────────────────────────────────────────────────
# The SQL of one run
# ─────────────────────────────────────────────────────────────────────────────

def _side_sql(conn, schema: str, ask: Ask, with_key: bool) -> Tuple[str, List[str]]:
    """SELECT giving, for every useful row of one run, its group columns
    (g_*), whether it is in each cell (in_*), its values (v_*), its counts
    (k_*), its distinct key (u_distinct) and, for the pairing, its key.
    Returns (sql, the values the file really has)."""
    FAM, VCOORD, VCOCRIT, STATB, ELEM, VCOTYP = pikobs.family(ask.family)
    varnos = ",".join(str(v) for v in ask.varnos) if ask.varnos else ELEM
    head = table_columns(conn, "header", schema)
    data = table_columns(conn, "data", schema)
    items = []
    if with_key:
        items.append(_key_items(ask))
    for name, expr in ask.group:
        items.append(f"({expr}) AS g_{name}")
    if ask.special_column:
        sp, _ = special_select(ask.family, head, True, prefix="h.")
        items.append(f"{sp} AS g_special")
    # the control read without the flag when the criterion is the experience's
    bare = (ask.flag_on == "exp" and schema == "c") or (ask.flag_on == "ctl" and schema == "e")
    for i, c in enumerate(ask.cells):
        items.append(f"(CASE WHEN {c.place if bare else c.cond} THEN 1 ELSE 0 END) AS in_{i}")
    have = [v for v in ask.values if v in data]
    for v in ask.values:
        # a departure stored as '' is not NULL and would be summed as zero
        items.append(f"(CASE WHEN typeof(d.{v}) IN ('real', 'integer') "
                     f"THEN d.{v} END) AS v_{v}" if v in have else f"NULL AS v_{v}")
    for name, expr in ask.exprs:
        items.append(f"({expr}) AS v_{name}")
    for name, cond in ask.counts:
        items.append(f"(CASE WHEN {cond} THEN 1 ELSE 0 END) AS k_{name}")
    if ask.distinct:
        items.append(f"({ask.distinct}) AS u_distinct")
    present = [f"d.{v} IS NOT NULL" for v in have] + [f"({e}) IS NOT NULL" for _, e in ask.exprs]
    # nothing summed (counts only): every row counts
    any_value = (" OR ".join(present) or "0") if (ask.values or ask.exprs) else "1"
    # only the rows in some cell: a row outside every cell is never summed,
    # but reading, indexing and pairing it cost most of the time (all the
    # channels of IASI, assimilated or not, for the few thousand that are)
    any_cell = " OR ".join(f"({c.place if bare else c.cond})" for c in ask.cells) or "0"
    data_src = f"{schema}.data"
    if ask.pre:
        # the derived columns, once per observation, in a temporary table:
        # an expression repeated in the gates and the values would call its
        # function (ro_ref) again at every use
        conn.execute(f"DROP TABLE IF EXISTS temp.pre_{schema};")
        conn.execute(f"CREATE TEMP TABLE pre_{schema} AS SELECT *, "
                     + ", ".join(f"({e}) AS {n}" for n, e in ask.pre)
                     + f" FROM {schema}.data WHERE varno IN ({varnos}) "
                       f"AND obsvalue IS NOT NULL;")
        data_src = f"temp.pre_{schema}"
    sql = (f"SELECT {', '.join(items)} "
           f"FROM {schema}.header AS h NATURAL JOIN {data_src} AS d "
           f"WHERE varno IN ({varnos}) AND obsvalue IS NOT NULL "
           f"AND ({any_value}) AND ({any_cell}) {VCOCRIT} "
           + (f"AND ({ask.where})" if ask.where.strip() else ""))
    return sql, have


def _key_items(ask: Ask) -> str:
    """The SELECT items of the pairing key, rank included."""
    if ask.key_exprs:
        from pikobs.match.match import rank_select
        return (", ".join(f"({e}) AS k_{n}" for n, e in ask.key_exprs) + ", "
                + rank_select([e for _, e in ask.key_exprs], "d.obsvalue"))
    return key_select(MatchSpec(True, ask.key), h="h", d="d")


def _key_names(ask: Ask, with_rank: bool = True) -> List[str]:
    """The key columns of a side table (and its rank)."""
    if ask.key_exprs:
        from pikobs.match.match import RANK
        names = [f"k_{n}" for n, _ in ask.key_exprs]
        return names + [RANK] if with_rank else names
    return key_aliases(MatchSpec(True, ask.key), with_rank=with_rank)


def _key_on(ask: Ask) -> str:
    """The ON clause of the pairs; IS, so a missing level pairs too."""
    if ask.key_exprs:
        return " AND ".join(f"c.{n} IS e.{n}" for n in _key_names(ask))
    return key_join(MatchSpec(True, ask.key))


def _extra_sql(ask: Ask, alias: str = "") -> List[str]:
    """The aggregates of counts, extremes and distinct, cell by cell."""
    p = f"{alias}." if alias else ""
    out = []
    for i in range(len(ask.cells)):
        for name, _ in ask.counts:
            out.append(f"SUM(CASE WHEN {p}in_{i} = 1 THEN {p}k_{name} ELSE 0 END)")
        for v in ask.extremes:
            out += [f"MIN(CASE WHEN {p}in_{i} = 1 THEN {p}v_{v} END)",
                    f"MAX(CASE WHEN {p}in_{i} = 1 THEN {p}v_{v} END)"]
        if ask.distinct:
            out.append(f"COUNT(DISTINCT CASE WHEN {p}in_{i} = 1 THEN {p}u_distinct END)")
    return out


def _g(ask: Ask, alias: str = "") -> List[str]:
    p = f"{alias}." if alias else ""
    return [f"{p}g_{n}" for n in ask.group_names]


def _group_by(cols: List[str]) -> str:
    return f"GROUP BY {', '.join(cols)}" if cols else ""


def _by_mask(ask: Ask) -> bool:
    """The sums by combination of cells, shared out in Python: not for a
    distinct count, which cannot be shared, nor beyond the bits of an int."""
    return not ask.distinct and 0 < len(ask.cells) <= 60


def _apart_by_mask(conn, sql: str, ask: Ask) -> Dict[tuple, Tuple[list, list]]:
    """What _apart gives, the sums computed once per group and combination
    of cells (bit i: cell i) and shared out to the cells with their bit."""
    g = _g(ask)
    names = ask.value_names
    nc, nv, nk, nx, me = (len(ask.cells), len(names), len(ask.counts),
                          len(ask.extremes), ask.n_extra)
    aggs = ["COUNT(*)"]
    for v in names:
        aggs += [f"SUM(v_{v} IS NOT NULL)", f"SUM(v_{v})", f"SUM(v_{v} * v_{v})"]
    aggs += [f"SUM(k_{n})" for n, _ in ask.counts]
    for v in ask.extremes:
        aggs += [f"MIN(v_{v})", f"MAX(v_{v})"]
    mask = " + ".join(f"(in_{i} << {i})" for i in range(nc))
    rows = conn.execute(f"SELECT {', '.join(g + [f'({mask}) AS cellmask'] + aggs)} "
                        f"FROM ({sql}) {_group_by(g + ['cellmask'])};").fetchall()
    k, off = len(g), 1 + 3 * nv
    out: Dict[tuple, Tuple[list, list]] = {}
    for r in rows:
        gkey, m, a = tuple(r[:k]), int(r[k] or 0), r[k + 1:]
        if gkey not in out:
            out[gkey] = ([0] + [0, None, None] * (nc * nv), [None] * (nc * me))
        vals, ext = out[gkey]
        vals[0] += a[0] or 0
        for i in range(nc):
            if not (m >> i) & 1:
                continue
            for j in range(nv):
                n, s, s2 = a[1 + 3 * j:4 + 3 * j]
                b = 1 + 3 * (i * nv + j)
                vals[b] += n or 0
                if s is not None:
                    vals[b + 1] = s if vals[b + 1] is None else vals[b + 1] + s
                if s2 is not None:
                    vals[b + 2] = s2 if vals[b + 2] is None else vals[b + 2] + s2
            e0 = i * me
            for q in range(nk):
                ext[e0 + q] = (ext[e0 + q] or 0) + (a[off + q] or 0)
            for q in range(nx):
                lo, hi = a[off + nk + 2 * q], a[off + nk + 2 * q + 1]
                p = e0 + nk + 2 * q
                if lo is not None:
                    ext[p] = lo if ext[p] is None else min(ext[p], lo)
                if hi is not None:
                    ext[p + 1] = hi if ext[p + 1] is None else max(ext[p + 1], hi)
    return out


def _apart(conn, schema: str, ask: Ask) -> Dict[tuple, Tuple[list, list]]:
    """MATCH off / no: the sums of one run, {group: ([rows, n, s, s2 per
    cell and value], [the extras per cell])}."""
    sql, _ = _side_sql(conn, schema, ask, with_key=False)
    if _by_mask(ask):
        return _apart_by_mask(conn, sql, ask)
    g = _g(ask)
    sums = ["COUNT(*)"]                 # the useful rows, whatever the cell
    for i in range(len(ask.cells)):
        for v in ask.value_names:
            ok = f"in_{i} = 1 AND v_{v} IS NOT NULL"
            sums += [f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END)",
                     f"SUM(CASE WHEN {ok} THEN v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN v_{v} * v_{v} END)"]
    extra = _extra_sql(ask)
    rows = conn.execute(f"SELECT {', '.join(g + sums + extra)} FROM ({sql}) "
                        f"{_group_by(g)};").fetchall()
    k, m = len(g), len(sums)
    return {tuple(r[:k]): (list(r[k:k + m]), list(r[k + m:])) for r in rows}


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
        raise NotImplementedError(f"extra_sums {ask.extra_sums}: not in the reader yet")
    single = exp_file is None
    if single and ask.match == "on":
        raise ValueError("MATCH on needs two runs")
    files = {"c": ctl_file} if single else {"c": ctl_file, "e": exp_file}
    for f in files.values():
        if not os.path.isfile(f):
            print(f"[{module}] missing file, cycle {cycle} skipped: {f}",
                  file=sys.stderr, flush=True)
            return None

    nv, m = len(ask.value_names), ask.n_extra
    extras: Dict[tuple, Dict[int, list]] = {}
    with work_db(attach=files) as (conn, _):
        regionsobs.register_pending(conn)
        # the polygons of the cells, by name: the cells may have been built in
        # another process (a dask worker has none of its parent's registrations)
        regionsobs.register(conn, sorted({c.region for c in ask.cells}), pathwork)
        register_surface(conn, [c.land_ocean for c in ask.cells], pathwork)
        for name, nargs, fn in ask.functions:
            conn.create_function(name, int(nargs), fn, deterministic=True)
        for s, f in files.items():
            if not (table_columns(conn, "header", s) and table_columns(conn, "data", s)):
                print(f"[{module}] no header / data table, cycle {cycle} "
                      f"skipped: {f}", file=sys.stderr, flush=True)
                return None
        if ask.match == "on":
            merged, info, extras = _paired(conn, ask)
        else:
            merged, info = {}, {}
            for s, side in (("c", 0), ("e", 1)):
                if s not in files:
                    continue
                total = 0
                for gkey, (vals, ext) in _apart(conn, s, ask).items():
                    total += vals[0] or 0
                    per = merged.setdefault(gkey, _empty(ask))
                    for i in range(len(ask.cells)):
                        for j in range(nv):
                            n, sm, s2 = vals[1 + 3 * (i * nv + j):][:3]
                            cell = per[i][j]
                            base = 0 if side == 0 else 3
                            cell[base:base + 3] = [n or 0, sm or 0.0, s2 or 0.0]
                            cell[7 + side] = n or 0
                    if m:
                        extras.setdefault(gkey, {})[side] = ext
                # counted once per row: the regions overlap, a sum over the
                # cells would count the tropics twice
                info[f"obs_{s}"] = int(total)

    nk, nx = len(ask.counts), len(ask.extremes)
    out = []
    for gkey in list(merged) + [k for k in extras if k not in merged]:
        per = merged.get(gkey) or _empty(ask)
        ext = extras.get(gkey, {})
        for i, c in enumerate(ask.cells):
            row = [x for j in range(nv) for x in per[i][j]]
            sides = [ext.get(s, [None] * (m * len(ask.cells)))[i * m:(i + 1) * m]
                     for s in (0, 1)]
            if m and single:
                sides[1] = [None] * m
            extra = []
            for q in range(nk):
                extra += [sides[0][q] or 0, sides[1][q] if single else (sides[1][q] or 0)]
            for q in range(nx):
                a, b = nk + 2 * q, nk + 2 * q + 1
                extra += [sides[0][a], sides[0][b], sides[1][a], sides[1][b]]
            if ask.distinct:
                extra += [sides[0][m - 1] or 0, sides[1][m - 1] if single else (sides[1][m - 1] or 0)]
            counted = any(row[k] for j in range(nv)
                          for k in (9 * j, 9 * j + 3, 9 * j + 7, 9 * j + 8))
            counted = counted or any(extra[q] for q in range(0, 2 * nk))
            counted = counted or bool(ask.distinct and extra[-2])
            if not counted:
                continue
            out.append([int(cycle), c.region, c.flag, c.land_ocean, *gkey, *row, *extra])
    df = pd.DataFrame(out, columns=columns(ask))
    if ask.match != "on":
        for v in ask.value_names:
            df[f"sce_{v}"] = float("nan")
    if single:
        for v in ask.value_names:
            for s in ("ne", "se", "se2", "nalle"):
                df[f"{s}_{v}"] = float("nan")
    return CycleSums(df, info)


def _empty(ask: Ask) -> List[List[List[float]]]:
    """[cell][value] -> the nine sums, zero."""
    return [[[0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0] for _ in ask.value_names]
            for _ in ask.cells]


def _paired(conn, ask: Ask) -> Tuple[Dict[tuple, list], Dict[str, int], Dict[tuple, Dict[int, list]]]:
    """MATCH on: the pairs of the two runs, each run's own count and, when
    asked, each run's counts, extremes and distinct in each cell."""
    spec = MatchSpec(True, ask.key)
    info: Dict[str, int] = {}
    for s in ("c", "e"):
        sql, _ = _side_sql(conn, s, ask, with_key=True)
        conn.execute(f"CREATE TEMP TABLE side_{s} AS {sql};")
        conn.execute(f"CREATE INDEX temp.idx_{s} ON side_{s} "
                     f"({', '.join(_key_names(ask))});")
        k, r = count_repeats(conn, f"side_{s}", _key_names(ask, with_rank=False))
        info[f"obs_{s}"] = conn.execute(f"SELECT COUNT(*) FROM side_{s};").fetchone()[0]
        info[f"rep_keys_{s}"], info[f"rep_rows_{s}"] = k, r
    info["pairs"] = conn.execute(
        f"SELECT COUNT(*) FROM side_c AS c JOIN side_e AS e ON {_key_on(ask)};"
    ).fetchone()[0]

    merged: Dict[tuple, list] = {}
    extras: Dict[tuple, Dict[int, list]] = {}
    names = ask.value_names
    nv = len(names)
    extra = _extra_sql(ask)
    # each run's own count (and extras), paired or not
    for side, s in enumerate(("c", "e")):
        if _by_mask(ask):
            for gkey, (vals, ext) in _apart_by_mask(conn, f"SELECT * FROM side_{s}", ask).items():
                per = merged.setdefault(gkey, _empty(ask))
                for i in range(len(ask.cells)):
                    for j in range(nv):
                        per[i][j][7 + side] = vals[1 + 3 * (i * nv + j)] or 0
                if extra:
                    extras.setdefault(gkey, {})[side] = ext
            continue
        g = _g(ask)
        cnt = [f"SUM(CASE WHEN in_{i} = 1 AND v_{v} IS NOT NULL THEN 1 ELSE 0 END)"
               for i in range(len(ask.cells)) for v in names]
        for r in conn.execute(f"SELECT {', '.join(g + cnt + extra)} FROM side_{s} "
                              f"{_group_by(g)};"):
            gkey = tuple(r[:len(g)])
            per = merged.setdefault(gkey, _empty(ask))
            for i in range(len(ask.cells)):
                for j in range(nv):
                    per[i][j][7 + side] = r[len(g) + i * nv + j] or 0
            if extra:
                extras.setdefault(gkey, {})[side] = list(r[len(g) + len(cnt):])
    # the pairs, grouped as the control has them
    g = _g(ask, "c")
    nc = len(ask.cells)
    if 0 < nc <= 60:
        # once per combination of the cells both observations fall in
        pmask = " + ".join(f"((c.in_{i} * e.in_{i}) << {i})" for i in range(nc))
        aggs = []
        for v in names:
            ok = f"c.v_{v} IS NOT NULL AND e.v_{v} IS NOT NULL"
            aggs += [f"SUM({ok})",
                     f"SUM(CASE WHEN {ok} THEN c.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN c.v_{v} * c.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN e.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN e.v_{v} * e.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN c.v_{v} * e.v_{v} END)"]
        for r in conn.execute(f"SELECT {', '.join(g + [f'({pmask}) AS pairmask'] + aggs)} "
                              f"FROM side_c AS c JOIN side_e AS e ON {_key_on(ask)} "
                              f"{_group_by(g + ['pairmask'])};"):
            gkey, m, a = tuple(r[:len(g)]), int(r[len(g)] or 0), r[len(g) + 1:]
            if not m:
                continue
            per = merged.setdefault(gkey, _empty(ask))
            for i in range(nc):
                if not (m >> i) & 1:
                    continue
                for j in range(nv):
                    n, sc, sc2, se, se2, sce = a[6 * j:6 * j + 6]
                    cell = per[i][j]
                    cell[0] += n or 0
                    cell[1] += sc or 0.0
                    cell[2] += sc2 or 0.0
                    cell[3] += n or 0
                    cell[4] += se or 0.0
                    cell[5] += se2 or 0.0
                    cell[6] += sce or 0.0
        for s in ("c", "e"):
            conn.execute(f"DROP TABLE side_{s};")
        return merged, info, extras
    sums = []
    for i in range(len(ask.cells)):
        for v in names:
            ok = (f"c.in_{i} = 1 AND e.in_{i} = 1 "
                  f"AND c.v_{v} IS NOT NULL AND e.v_{v} IS NOT NULL")
            sums += [f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END)",
                     f"SUM(CASE WHEN {ok} THEN c.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN c.v_{v} * c.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN e.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN e.v_{v} * e.v_{v} END)",
                     f"SUM(CASE WHEN {ok} THEN c.v_{v} * e.v_{v} END)"]
    if sums:
        for r in conn.execute(f"SELECT {', '.join(g + sums)} FROM side_c AS c "
                              f"JOIN side_e AS e ON {_key_on(ask)} {_group_by(g)};"):
            per = merged.setdefault(tuple(r[:len(g)]), _empty(ask))
            for i in range(len(ask.cells)):
                for j in range(nv):
                    n, sc, sc2, se, se2, sce = r[len(g) + 6 * (i * nv + j):][:6]
                    n = n or 0
                    per[i][j][:7] = [n, sc or 0.0, sc2 or 0.0, n, se or 0.0,
                                     se2 or 0.0, sce or 0.0]
    for s in ("c", "e"):
        conn.execute(f"DROP TABLE side_{s};")
    return merged, info, extras


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
