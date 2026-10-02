#!/usr/bin/env python
"""What each family carries in its files, varno by varno, as a CSV.

Reads the last complete cycles of a suite's monitoring files -- bgckalt and
postalt, the files the modules read -- and writes
pikobs/configobs/postalt_varnos.csv: for every family and varno, the
observations, how many are assimilated, and the range of the vertical
coordinate. A varno counts as carried if it is in either stage; it counts
as assimilated from postalt only, the only stage where bit 12 of the flag
is set. The Varno page and its search read the CSV; pikobs_doc.sh runs this
every time, so a new varno or family shows up by itself.

    python pikobs/build_doc/make_varno_csv.py                 # G2, 4 cycles
    python pikobs/build_doc/make_varno_csv.py g0 --cycles 8
"""
import argparse
import csv
import os
import re
import sqlite3
import sys
from collections import defaultdict

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                    "configobs", "postalt_varnos.csv"))
# postalt only: what the modules read. The earlier stages can hold more
# (the bending angle of ro is in cutoff and is dropped in derialt), and
# the Varno page says so
STAGES = ("postalt",)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("suite", nargs="?", default="g2")
    ap.add_argument("--force", action="store_true",
                    help="rewrite the CSV even when only the counts changed")
    ap.add_argument("--cycles", type=int, default=4,
                    help="the last complete cycles to read (default 4, a day)")
    args = ap.parse_args()
    base = os.path.expanduser(f"~smco500/.suites/gdps/{args.suite}/hub/ppp7/monitoring/banco")
    post = os.path.join(base, "postalt")
    if not os.path.isdir(post):
        sys.exit(f"[varno] {post} not reachable: the CSV of the repository is kept")
    cycles = sorted({f[:10] for f in os.listdir(post) if re.match(r"\d{10}_", f)})
    cycles = cycles[-(args.cycles + 1):-1]          # the last one may still be written
    if not cycles:
        sys.exit(f"[varno] no complete cycle in {post}: the CSV of the repository is kept")
    # (family, varno) -> per stage: observations, assimilated; and the vcoord range
    n = defaultdict(lambda: {s: 0 for s in STAGES})
    assim = defaultdict(int)
    lo, hi = {}, {}
    for stage in STAGES:
        d = os.path.join(base, stage)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f[:10] not in cycles or len(f) < 12 or f[10] != "_":
                continue
            fam = f[11:]
            try:
                con = sqlite3.connect(f"file:{os.path.join(d, f)}?mode=ro", uri=True)
                for v, k, a, vmin, vmax in con.execute(
                        "SELECT varno, COUNT(*), SUM((flag & 4096) = 4096), "
                        "MIN(vcoord), MAX(vcoord) FROM data GROUP BY varno"):
                    if v is None:
                        continue
                    key = (fam, int(v))
                    n[key][stage] += k or 0
                    if stage == "postalt":
                        assim[key] += a or 0
                    if vmin is not None:
                        lo[key] = min(lo.get(key, vmin), vmin)
                    if vmax is not None:
                        hi[key] = max(hi.get(key, vmax), vmax)
                con.close()
            except sqlite3.Error as exc:
                print(f"[varno] {stage}/{f}: {exc}", file=sys.stderr)
    if not n:
        sys.exit("[varno] nothing read: the CSV of the repository is kept")
    rows = []
    for (fam, v), per in sorted(n.items()):
        obs = per["postalt"] or per["bgckalt"]       # postalt when it has them
        rows.append([fam, v, obs, assim[(fam, v)],
                     "" if (fam, v) not in lo else f"{lo[(fam, v)]:.6g}",
                     "" if (fam, v) not in hi else f"{hi[(fam, v)]:.6g}"])
    # the documentation reads which family carries which varno and whether
    # it is assimilated; the counts of the day change every time and are
    # not by themselves a reason to rewrite the file (--force is)
    shape = {(str(r[0]), int(r[1]), int(r[3]) > 0) for r in rows}
    if not args.force and os.path.isfile(OUT):
        try:
            with open(OUT, newline="") as fh:
                old = {(r["family"], int(r["varno"]), int(r["assimilated"]) > 0)
                       for r in csv.DictReader(fh)}
        except (OSError, KeyError, ValueError):
            old = None
        if old == shape:
            print(f"[varno] {args.suite}, {len(cycles)} cycles ({cycles[0]} to "
                  f"{cycles[-1]}): the same {len(rows)} varnos, assimilated as "
                  f"before -> {OUT} unchanged")
            return
    tmp = OUT + ".tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["family", "varno", "obs", "assimilated", "vcoord_min", "vcoord_max"])
        w.writerows(rows)
    os.replace(tmp, OUT)
    carried = [r for r in rows if r[3] == 0]
    fams = sorted({r[0] for r in rows})
    print(f"[varno] {args.suite}, {len(cycles)} cycles ({cycles[0]} to {cycles[-1]}), "
          f"{', '.join(STAGES)}: {len(fams)} families, {len(rows)} varnos, "
          f"{len(carried)} of them carried but never assimilated -> {OUT}")


if __name__ == "__main__":
    main()
