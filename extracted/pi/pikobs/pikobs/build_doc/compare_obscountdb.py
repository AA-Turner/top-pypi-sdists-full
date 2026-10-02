#!/usr/bin/env python
"""obscountdb before and after a change: the whole output of one file, compared.

    python pikobs/build_doc/compare_obscountdb.py before     # with the old code
    (apply the change)
    python pikobs/build_doc/compare_obscountdb.py after      # with the new code
    python pikobs/build_doc/compare_obscountdb.py compare

before/after run create_and_populate_moyenne_table on the last complete postalt file of
G2 for iasi and ua, into ~/sites8/obscountdb_cmp_<label>_<family>.db, and say
how long each took; compare checks every table, row by row.
"""
import glob
import math
import os
import sqlite3
import sys
import time

from pikobs.obscountdb import obscountdb as O

POSTALT = "/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"
REGIONS = ["Monde", "HemisphereNord", "HemisphereSud", "Tropiques", "Canada"]
FLAGS = ["assimilee", "rejets_qc"]
AGR = ["oma", "omp"]
FAMILIES = ("iasi", "ua", "ai")
OUT = os.path.expanduser("~/sites8/obscountdb_cmp_{}_{}.db")


def run(label):
    for fam in FAMILIES:
        path = sorted(glob.glob(os.path.join(POSTALT, f"??????????_{fam}")))[-2]
        out = OUT.format(label, fam)
        if os.path.exists(out):
            os.remove(out)
        t = time.time()
        O.create_and_populate_moyenne_table(fam, out, path, REGIONS, FLAGS, AGR)
        print(f"[{label}] {fam:5s} {time.time() - t:6.1f} s  {os.path.basename(path)} -> {out}")


def same(a, b):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if isinstance(x, float) or isinstance(y, float):
            if x is None or y is None or not math.isclose(x, y, rel_tol=1e-12, abs_tol=1e-12):
                if not (x is None and y is None):
                    return False
        elif x != y:
            return False
    return True


def compare():
    ok = True
    for fam in FAMILIES:
        a, b = sqlite3.connect(OUT.format("before", fam)), sqlite3.connect(OUT.format("after", fam))
        tables = [r[0] for r in a.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        for t in tables:
            ra = sorted(a.execute(f"SELECT * FROM {t}").fetchall(), key=repr)
            rb = sorted(b.execute(f"SELECT * FROM {t}").fetchall(), key=repr)
            diff = sum(1 for x, y in zip(ra, rb) if not same(x, y)) + abs(len(ra) - len(rb))
            print(f"{fam:5s} {t:20s} {len(ra):8d} rows before, {len(rb):8d} after, "
                  f"{'identical' if not diff else f'{diff} rows DIFFER'}")
            ok &= not diff
    print("\nthe same output before and after" if ok else "\nTHE OUTPUT CHANGED")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what in ("before", "after"):
        run(what)
    elif what == "compare":
        compare()
    else:
        sys.exit(__doc__)
