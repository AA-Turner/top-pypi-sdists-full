#!/usr/bin/env python
"""timeserie, before and after a change: every table, compared.

    python pikobs/build_doc/compare_timeserie.py before   # old code
    (apply the change)
    python pikobs/build_doc/compare_timeserie.py after    # new code
    python pikobs/build_doc/compare_timeserie.py compare

before/after run the comparison wrapper of timeserie on one cycle, with
iasi, ua and ai, three regions and three criteria, no pairs (the path of
create_ts), into ~/sites8/ts_cmp_<label>, and say how long it took;
compare checks every table of every database the two runs wrote, row by
row (sums to 1 part in 10^12).
"""
import math
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
WRAPPER = os.path.join(REPO, "pikobs", "script", "run_timeserie_cont_exp.sh")
OUT = os.path.expanduser("~/sites8/ts_cmp_{}")
CYCLE = os.environ.get("PIKOBS_CMP_CYCLE") or (__import__("datetime").datetime.utcnow().date()
         - __import__("datetime").timedelta(days=4)).strftime("%Y%m%d") + "00"
SETTINGS = {"DATESTART": f'"{CYCLE}"', "DATEEND": f'"{CYCLE}"', "MATCH": '"off"',
            "FAMILY": "(iasi ua ai)", "REGION": "(Monde HemisphereNord Tropiques)",
            "FLAGS_CRITERIA": "(assimilee rejets_qc all)", "ID_STN": "(all)",
            "CHANNEL": "(join)", "N_CPUS": "80"}


def run(label):
    out = OUT.format(label)
    shutil.rmtree(out, ignore_errors=True)       # nothing left from an earlier run
    src = open(WRAPPER).read()
    src = re.sub(r'(?m)^PATHWORK=.*$', f'PATHWORK="{out}"', src, count=1)
    for var, val in SETTINGS.items():
        src = re.sub(rf'(?m)^{var}=.*$', f'{var}={val}', src, count=1)
    copy = out + ".sh"
    open(copy, "w").write(src)
    env = dict(os.environ, PIKOBS_TIMING="1", PBS_O_WORKDIR="")
    t = time.time()
    with open(out + ".log", "w") as fh:
        rc = subprocess.call(["bash", copy], stdout=fh, stderr=subprocess.STDOUT, env=env)
    log = open(out + ".log", errors="replace").read()
    open(out + ".rc", "w").write(str(rc))
    print(f"[{label}] {time.time() - t:.0f} s (rc {rc})")
    if rc != 0:
        print(f"[{label}] THE RUN FAILED -- the end of its log:")
        for line in log.strip().splitlines()[-5:]:
            print(f"   {line}")
    for line in log.splitlines():
        if "extraction time" in line:
            print(f"   {line.strip()}")


def dbs(root):
    out = {}
    for d, _, files in os.walk(root):
        for f in files:
            if f.endswith(".db"):
                p = os.path.join(d, f)
                out[os.path.relpath(p, root)] = p
    return out


def same(a, b):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if isinstance(x, float) or isinstance(y, float):
            if x is None or y is None:
                if not (x is None and y is None):
                    return False
            elif not math.isclose(x, y, rel_tol=1e-12, abs_tol=1e-12):
                return False
        elif x != y:
            return False
    return True


def compare():
    for label in ("before", "after"):
        rc_file = OUT.format(label) + ".rc"
        rc = open(rc_file).read().strip() if os.path.isfile(rc_file) else "missing"
        if rc != "0":
            sys.exit(f"the {label} run did not succeed (rc {rc}): nothing to compare")
    a, b = dbs(OUT.format("before")), dbs(OUT.format("after"))
    if not a or not b:
        sys.exit("no database in one of the two runs: nothing to compare")
    ok = set(a) == set(b)
    if not ok:
        print("different databases:", sorted(set(a) ^ set(b)))
    for rel in sorted(set(a) & set(b)):
        ca, cb = sqlite3.connect(a[rel]), sqlite3.connect(b[rel])
        for (t,) in ca.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            ra = sorted(ca.execute(f"SELECT * FROM {t}").fetchall(), key=repr)
            rb = sorted(cb.execute(f"SELECT * FROM {t}").fetchall(), key=repr)
            diff = sum(1 for x, y in zip(ra, rb) if not same(x, y)) + abs(len(ra) - len(rb))
            if diff or t in ("ts_qc", "ts_val"):
                print(f"{rel:50s} {t:10s} {len(ra):8d} / {len(rb):8d} rows "
                      f"{'identical' if not diff else f'{diff} DIFFER'}")
            ok &= not diff or t == '_pikobs_done'      # when it finished: always differs
    print("\nthe same output before and after" if ok else "\nTHE OUTPUT CHANGED")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what in ("before", "after"):
        run(what)
    elif what == "compare":
        compare()
    else:
        sys.exit(__doc__)
