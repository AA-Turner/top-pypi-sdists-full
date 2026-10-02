#!/usr/bin/env python
"""obscountdb: the time of one day as regions are added, with two criteria.

obscountdb counts every family whatever the selection, so what a user
really changes is the regions and the criteria. This runs its wrapper as it
comes (five regions, two criteria), keeping the first 1, 2, 3, 4 and 5
regions of its list, with the departures (omp, oma) and without, on one day
(four cycles). Each run is timed whole, as bench_runtime.py does.

It writes pikobs/build_doc/bench_obscountdb_regions.csv and
docs/source/runtime_obscountdb_regions.rst, included by the run time page.
Run it on a compute node (about 20 minutes):

    python pikobs/build_doc/bench_obscountdb_regions.py
    python pikobs/build_doc/bench_obscountdb_regions.py table     # only the table, from the CSV
"""
import csv
import datetime as dt
import os
import re
import subprocess
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
WRAPPER = os.path.join(REPO, "pikobs", "script", "run_obscountdb_cont_exp.sh")
CSV = os.path.join(REPO, "pikobs", "build_doc", "bench_obscountdb_regions.csv")
RST = os.path.join(REPO, "docs", "source", "runtime_obscountdb_regions.rst")
WORK = os.path.expanduser("~/sites8/bench_obscountdb_regions")
VARIANTS = (("with omp/oma", "(oma omp)"), ("no omp/oma", "()"))


def wrapper_list(src, var):
    m = re.search(rf"(?m)^{var}=\((.*?)\)", src)
    return m.group(1).split() if m else []


def duration(s):
    return f"{s:.0f} s" if s < 180 else f"{s / 60:.0f} min" if s < 3600 else f"{s / 3600:.1f} h"


def measure():
    src = open(WRAPPER).read()
    regions = wrapper_list(src, "REGION")
    flags = wrapper_list(src, "FLAGS_CRITERIA")
    day = dt.datetime.utcnow().date() - dt.timedelta(days=3)
    start, end = f"{day - dt.timedelta(days=1):%Y%m%d}06", f"{day:%Y%m%d}00"
    os.makedirs(WORK, exist_ok=True)
    rows = []
    print(f"[bench] obscountdb, {start} to {end}, criteria {' '.join(flags)}, "
          f"regions {' '.join(regions)}", flush=True)
    for label, agr in VARIANTS:
        for n in range(1, len(regions) + 1):
            tag = f"{label.split()[0]}_{n}"
            out = os.path.join(WORK, tag)
            s = src
            for var, val in {"DATESTART": f'"{start}"', "DATEEND": f'"{end}"',
                             "PATHWORK": f'"{out}"', "REGION": f"({' '.join(regions[:n])})",
                             "AGR": agr}.items():
                s = re.sub(rf"(?m)^{var}=.*$", f"{var}={val}", s, count=1)
            script = out + ".sh"
            open(script, "w").write(s)
            t0 = time.time()
            with open(out + ".log", "w") as log:
                rc = subprocess.call(["bash", script], stdout=log, stderr=subprocess.STDOUT,
                                     env=dict(os.environ, PBS_O_WORKDIR=""))
            wall = time.time() - t0
            text = open(out + ".log", errors="replace").read()
            if rc == 0 and ("INCOMPLETE" in text or "tasks lost" in text):
                rc = 99
            rows.append({"variant": label, "regions": n, "criteria": len(flags),
                         "wall_s": round(wall, 1), "rc": rc})
            print(f"[bench]   {label:13s} {n} region(s): {wall:6.0f} s (rc {rc})", flush=True)
    with open(CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def table():
    rows = [r for r in csv.DictReader(open(CSV)) if r["rc"] == "0"]
    if not rows:                     # every run failed: keep the table there is
        sys.exit("[bench] no run succeeded -- the table of the page is left as it is "
                 "(on a login node pikobs does not run: use a compute node)")
    ns = sorted({int(r["regions"]) for r in rows})
    head = ["Run"] + [f"{n} region{'s' if n > 1 else ''}" for n in ns]
    body = []
    for label, _ in VARIANTS:
        t = {int(r["regions"]): float(r["wall_s"]) for r in rows if r["variant"] == label}
        body.append([label] + [duration(t[n]) if n in t else "--" for n in ns])
    crit = rows[0]["criteria"] if rows else "2"
    lines = [".. list-table::", "   :header-rows: 1", ""]
    for i, r in enumerate([head] + body):
        lines.append("   * - " + r[0])
        lines += [f"     - {c}" for c in r[1:]]
    lines += ["", f"One day (four 6-h cycles), every family, {crit} criteria; regions added "
                  "in the order of the wrapper."]
    open(RST, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if sys.argv[1:] != ["table"]:
        measure()
    table()
