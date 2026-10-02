#!/usr/bin/env python
"""Where cardio's extraction spends its time, on one real file.

cardio reads each file once: one GROUP BY with, for every region and
criterion, ~18 conditional aggregates and two COUNT(DISTINCT id_obs). This
times four versions of that query on one postalt file of G2:

    A  the GROUP BY alone (COUNT(*))
    B  A + the conditional sums, minima and maxima
    C  A + the COUNT(DISTINCT ...) columns
    D  everything, as cardio runs it
    E  B, each condition evaluated once per row in a subquery
    F  D, the same way
    G  F, with the profiles counted in two steps -- per id_obs, then summed --
       instead of COUNT(DISTINCT id_obs)

B - A is what the conditions cost, C - A what the DISTINCT counts cost;
F against D is what evaluating each condition once would save.

    python pikobs/build_doc/cardio_sql_timing.py            # iasi
    python pikobs/build_doc/cardio_sql_timing.py ai
"""
import glob
import os
import re
import sqlite3
import sys
import time

import pikobs
from pikobs.cardio import cardio as C

POSTALT = "/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"
REGIONS = ["Monde", "HemisphereNord", "HemisphereSud", "Tropiques", "Canada"]
FLAGS = ["assimilee"]


def main():
    family = sys.argv[1] if len(sys.argv) > 1 else "iasi"
    files = sorted(glob.glob(os.path.join(POSTALT, f"??????????_{family}")))
    path = files[-2]                                   # the last may be incomplete
    print(f"file: {path} ({os.path.getsize(path) / 1e9:.2f} GB)")

    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    vcoord = (VCOORD or "").strip() or "9999"
    combos = C._combinations(REGIONS, FLAGS)
    print(f"{len(combos)} region x criterion combination(s)")

    conn = sqlite3.connect(":memory:")
    conn.execute(f"ATTACH DATABASE 'file:{path}?mode=ro' AS db;")
    # the functions a region or a surface may need, as cardio registers them
    for name in ("register", "_register"):
        f = getattr(C, name, None)
        if callable(f):
            try:
                f(conn, REGIONS, "/tmp")
            except Exception:
                pass
    head = [r[1].lower() for r in conn.execute("PRAGMA db.table_info('HEADER');")]
    cod = "codtyp" if "codtyp" in head else "NULL"

    def aggregates(k, r):
        """The aggregates of combination (k, r): conditions as SQL text."""
        out = [f"SUM(CASE WHEN {k} THEN (flag & 512) = 512 ELSE 0 END)",
               f"SUM(CASE WHEN {k} THEN (flag & 4096) = 4096 ELSE 0 END)"]
        for col in ("omp", "oma", "obsvalue"):
            ok = f"{k} AND {col} IS NOT NULL"
            out += [f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END)",
                    f"SUM(CASE WHEN {ok} THEN {col} END)"]
            if col != "obsvalue":
                out += [f"SUM(CASE WHEN {ok} THEN {col}*{col} END)",
                        f"MIN(CASE WHEN {ok} THEN {col} END)",
                        f"MAX(CASE WHEN {ok} THEN {col} END)"]
        return out, [f"COUNT(DISTINCT CASE WHEN {k} THEN id_obs END)",
                     f"COUNT(DISTINCT CASE WHEN {r} THEN id_obs END)"]

    # precomputed: each condition once per row, as a column of a subquery
    # that LIMIT -1 keeps SQLite from flattening back into the aggregates
    pre_cols, pre_sums, pre_dist = [], [], []
    for i, c in enumerate(combos):
        pre_cols += [f"({c['cond']}) AS k{i}", f"({c['region_cond']}) AS r{i}"]
        a, d = aggregates(f"k{i}", f"r{i}")
        pre_sums += a
        pre_dist += d
    pre_from = (f"(SELECT id_stn, {cod} AS cod, varno, {vcoord} AS chan, id_obs, "
                f"flag, omp, oma, obsvalue, {', '.join(pre_cols)} "
                f"FROM db.header NATURAL JOIN db.data "
                f"WHERE varno IN ({element}) {VCOCRIT} LIMIT -1)")

    sums, distincts = [], []
    for i, c in enumerate(combos):
        cond, rc = c["cond"], c["region_cond"]
        sums += [f"SUM(CASE WHEN {cond} THEN (flag & 512) = 512 ELSE 0 END)",
                 f"SUM(CASE WHEN {cond} THEN (flag & 4096) = 4096 ELSE 0 END)"]
        for col in ("omp", "oma", "obsvalue"):
            ok = f"{cond} AND {col} IS NOT NULL"
            sums += [f"SUM(CASE WHEN {ok} THEN 1 ELSE 0 END)",
                     f"SUM(CASE WHEN {ok} THEN {col} END)"]
            if col != "obsvalue":
                sums += [f"SUM(CASE WHEN {ok} THEN {col}*{col} END)",
                         f"MIN(CASE WHEN {ok} THEN {col} END)",
                         f"MAX(CASE WHEN {ok} THEN {col} END)"]
        distincts += [f"COUNT(DISTINCT CASE WHEN {cond} THEN id_obs END)",
                      f"COUNT(DISTINCT CASE WHEN {rc} THEN id_obs END)"]

    def run(label, extra, pre=False):
        cols = ", ".join(["COUNT(*)"] + extra)
        if pre:
            sql = (f"SELECT id_stn, cod, varno, chan, {cols} FROM {pre_from} "
                   f"GROUP BY id_stn, cod, varno, chan;")
        else:
            sql = (f"SELECT id_stn, {cod}, varno, {vcoord}, {cols} "
                   f"FROM db.header NATURAL JOIN db.data "
                   f"WHERE varno IN ({element}) {VCOCRIT} "
                   f"GROUP BY id_stn, {cod}, varno, {vcoord};")
        t = time.time()
        n = len(conn.execute(sql).fetchall())
        dt = time.time() - t
        print(f"  {label:44s} {dt:7.1f} s   ({n} groups, {len(extra)} aggregates)")
        return dt

    print("\nplan of the full query:")
    for row in conn.execute("EXPLAIN QUERY PLAN SELECT id_stn, varno, "
                            + ", ".join(distincts[:1]) +
                            f" FROM db.header NATURAL JOIN db.data WHERE varno IN "
                            f"({element}) GROUP BY id_stn, varno;"):
        print("   ", row[-1])
    print()
    a = run("A  GROUP BY alone", [])
    b = run("B  + conditional sums, min, max", sums)
    c = run("C  + COUNT(DISTINCT ...)", distincts)
    d = run("D  everything (as cardio)", sums + distincts)
    e = run("E  B, conditions once per row", pre_sums, pre=True)
    f = run("F  D, conditions once per row", pre_sums + pre_dist, pre=True)

    # G: per id_obs first -- its sums, extremes, and whether any of its rows
    # meets each condition -- then per station, varno and channel, where the
    # count of distinct id_obs is the sum of those flags
    inner, outer = ["COUNT(*) AS a_n"], ["SUM(a_n)"]
    for j, agg in enumerate(pre_sums):
        fn = agg.split("(", 1)[0]
        inner.append(f"{agg} AS a{j}")
        outer.append(f"{ {'SUM': 'SUM', 'MIN': 'MIN', 'MAX': 'MAX'}[fn] }(a{j})")
    for i in range(len(combos)):
        inner += [f"MAX(k{i}) AS pk{i}", f"MAX(r{i}) AS pr{i}"]
    for i in range(len(combos)):
        outer += [f"SUM(pk{i})", f"SUM(pr{i})"]
    g_sql = (f"SELECT id_stn, cod, varno, chan, {', '.join(outer)} FROM "
             f"(SELECT id_stn, cod, varno, chan, id_obs, {', '.join(inner)} "
             f"FROM {pre_from} GROUP BY id_stn, cod, varno, chan, id_obs) "
             f"GROUP BY id_stn, cod, varno, chan")
    t = time.time()
    g_rows = conn.execute(g_sql + " ORDER BY 1, 2, 3, 4;").fetchall()
    g = time.time() - t
    print(f"  {'G  F, profiles counted in two steps':44s} {g:7.1f} s   ({len(g_rows)} groups)")
    # the same columns in the same order as F: COUNT(*), the sums, then per
    # combination the two distinct counts
    f_sql = (f"SELECT id_stn, cod, varno, chan, COUNT(*), "
             + ", ".join(pre_sums + pre_dist) +
             f" FROM {pre_from} GROUP BY id_stn, cod, varno, chan ORDER BY 1, 2, 3, 4;")
    f_rows = conn.execute(f_sql).fetchall()
    import math
    def close(a, b):
        return len(a) == len(b) and all(
            (x is None and y is None) or (x is not None and y is not None and
             (x == y or (isinstance(x, float) or isinstance(y, float)) and
              math.isclose(x, y, rel_tol=1e-12, abs_tol=1e-9)))
            for x, y in zip(a, b))
    print(f"  G gives the numbers of F: "
          f"{len(g_rows) == len(f_rows) and all(close(a, b) for a, b in zip(g_rows, f_rows))}")
    same = (conn.execute(f"SELECT id_stn, {cod}, varno, {vcoord}, "
                         + ", ".join(sums + distincts) +
                         f" FROM db.header NATURAL JOIN db.data WHERE varno IN "
                         f"({element}) {VCOCRIT} GROUP BY id_stn, {cod}, varno, "
                         f"{vcoord} ORDER BY 1, 2, 3, 4;").fetchall()
            == conn.execute(f"SELECT id_stn, cod, varno, chan, "
                            + ", ".join(pre_sums + pre_dist) +
                            f" FROM {pre_from} GROUP BY id_stn, cod, varno, chan "
                            f"ORDER BY 1, 2, 3, 4;").fetchall())
    print(f"\n  F gives the same numbers as D: {same}")
    print(f"  D -> F saves ~{d - f:6.1f} s of {d:.1f} s")
    print(f"\n  conditions cost      ~{b - a:6.1f} s")
    print(f"  DISTINCT counts cost ~{c - a:6.1f} s")
    print(f"  together             ~{d - a:6.1f} s (+ {a:.1f} s to read and group)")


if __name__ == "__main__":
    main()
