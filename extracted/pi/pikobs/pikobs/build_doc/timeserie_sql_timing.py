#!/usr/bin/env python
"""Where timeserie's extraction spends its time, on one real file.

create_ts loops over the region x criterion combinations and, in each,
groups the rows of the whole file twice (ts_qc and ts_val): a row is
grouped once per combination it meets. This times that loop against
grouping first:

    old   the loop, as create_ts runs it
    new   one pass that groups by station, varno, level, flag value and
          the regions the row falls in (bits), then every combination read
          from those groups -- the criteria only look at flag

and checks the two give the same ts_qc and ts_val.

    python pikobs/build_doc/timeserie_sql_timing.py            # iasi
    python pikobs/build_doc/timeserie_sql_timing.py ua
"""
import glob
import math
import os
import sqlite3
import sys
import tempfile
import time

import pikobs
from pikobs.timeserie import timeserie as T
from pikobs.configobs import regionsobs as regionlib

POSTALT = "/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"
REGIONS = ["Monde", "HemisphereNord", "Tropiques"]
FLAGS = ["assimilee", "rejets_qc", "all"]


def close(a, b):
    return len(a) == len(b) and all(
        x == y or (isinstance(x, float) and isinstance(y, float)
                   and math.isclose(x, y, rel_tol=1e-12, abs_tol=1e-9))
        for x, y in zip(a, b))


def main():
    family = sys.argv[1] if len(sys.argv) > 1 else "iasi"
    path = sorted(glob.glob(os.path.join(POSTALT, f"??????????_{family}")))[-2]
    print(f"file: {path} ({os.path.getsize(path) / 1e9:.2f} GB), "
          f"{len(REGIONS)} regions x {len(FLAGS)} criteria")
    tmp = tempfile.mkdtemp()
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    lev = (VCOORD or "").strip() or "vcoord"
    conn = sqlite3.connect(":memory:")
    conn.execute(f"ATTACH DATABASE 'file:{path}?mode=ro' AS db;")
    T.register_land(conn, ["all"], tmp)
    regionlib.register(conn, REGIONS, tmp)
    dcols = {r[1].lower() for r in conn.execute("PRAGMA db.table_info('DATA');")}
    hcols = {r[1].lower() for r in conn.execute("PRAGMA db.table_info('HEADER');")}
    codtyp = "codtyp" if "codtyp" in hcols else "0"
    num = lambda c: T._num(c) if c in dcols else "NULL"
    omp, oma, err, bc = num("omp"), num("oma"), num("obs_error"), num("bias_corr")
    vals = (f"COUNT({omp}), SUM({omp}), SUM({omp}*{omp}), COUNT({oma}), SUM({oma}), "
            f"SUM({oma}*{oma}), COUNT({err}), SUM({err}), COUNT({bc}), SUM({bc}), SUM({bc}*{bc})")
    QC = T.QC_MASK

    # old: the loop of create_ts
    t = time.time()
    old_qc, old_val = [], []
    for region, flag, surf, cond in T._combos(REGIONS, FLAGS, ("all",), tmp):
        old_qc += conn.execute(
            f"SELECT '{region}', '{flag}', id_stn, {codtyp}, varno, {lev} AS l, "
            f"(flag & {QC}) AS sg, COUNT(*) FROM db.header NATURAL JOIN db.data "
            f"WHERE varno IN ({element}) {VCOCRIT} AND {cond} "
            f"GROUP BY id_stn, {codtyp}, varno, l, sg;").fetchall()
        old_val += conn.execute(
            f"SELECT '{region}', '{flag}', id_stn, {codtyp}, varno, {lev} AS l, {vals} "
            f"FROM db.header NATURAL JOIN db.data "
            f"WHERE varno IN ({element}) {VCOCRIT} AND {cond} "
            f"GROUP BY id_stn, {codtyp}, varno, l;").fetchall()
    t_old = time.time() - t
    print(f"  old  the loop, {2 * len(REGIONS) * len(FLAGS)} passes        {t_old:7.1f} s")

    # new: group once by flag value and region bits, then the combinations
    t = time.time()
    regsql = [f"1=1 {T._region_sql(r, tmp, 'lat', 'lon')}" for r in REGIONS]
    rb = " + ".join(f"(CASE WHEN {q} THEN {1 << k} ELSE 0 END)" for k, q in enumerate(regsql))
    conn.execute(f"""
        CREATE TEMP TABLE pre AS
        SELECT id_stn, {codtyp} AS cod, varno, {lev} AS l, flag, ({rb}) AS rb,
               COUNT(*) AS n,
               COUNT({omp}) AS n_omp, SUM({omp}) AS s_omp, SUM({omp}*{omp}) AS s2_omp,
               COUNT({oma}) AS n_oma, SUM({oma}) AS s_oma, SUM({oma}*{oma}) AS s2_oma,
               COUNT({err}) AS n_err, SUM({err}) AS s_err,
               COUNT({bc}) AS n_bc, SUM({bc}) AS s_bc, SUM({bc}*{bc}) AS s2_bc
        FROM db.header NATURAL JOIN db.data
        WHERE varno IN ({element}) {VCOCRIT}
        GROUP BY id_stn, cod, varno, l, flag, rb;""")
    t_pre = time.time() - t
    new_qc, new_val = [], []
    for k, region in enumerate(REGIONS):
        for flag in FLAGS:
            w = f"(rb & {1 << k}) != 0 {pikobs.flag_criteria(flag)}"
            new_qc += conn.execute(
                f"SELECT '{region}', '{flag}', id_stn, cod, varno, l, (flag & {QC}) AS sg, "
                f"SUM(n) FROM pre WHERE {w} GROUP BY id_stn, cod, varno, l, sg;").fetchall()
            new_val += conn.execute(
                f"SELECT '{region}', '{flag}', id_stn, cod, varno, l, SUM(n_omp), SUM(s_omp), "
                f"SUM(s2_omp), SUM(n_oma), SUM(s_oma), SUM(s2_oma), SUM(n_err), SUM(s_err), "
                f"SUM(n_bc), SUM(s_bc), SUM(s2_bc) FROM pre WHERE {w} "
                f"GROUP BY id_stn, cod, varno, l;").fetchall()
    t_new = time.time() - t
    n_pre = conn.execute("SELECT COUNT(*) FROM pre;").fetchone()[0]
    print(f"  new  group once ({n_pre} groups), then the combinations"
          f"  {t_new:7.1f} s  (the pass {t_pre:.1f} s)")

    same_qc = sorted(old_qc, key=repr) == sorted(new_qc, key=repr)
    same_val = len(old_val) == len(new_val) and all(
        close(a, b) for a, b in zip(sorted(old_val, key=repr), sorted(new_val, key=repr)))
    print(f"\n  ts_qc  {len(old_qc)} rows, the same: {same_qc}")
    print(f"  ts_val {len(old_val)} rows, the same: {same_val}")
    print(f"  old -> new: {t_old:.0f} s -> {t_new:.0f} s")


if __name__ == "__main__":
    main()
