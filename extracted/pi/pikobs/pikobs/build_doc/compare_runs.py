#!/usr/bin/env python
"""Compare runs made with mod_run.py: the validation of a change to a module.

    python pikobs/build_doc/compare_runs.py names   BEFORE AFTER [NEW ...]
    python pikobs/build_doc/compare_runs.py content BEFORE AFTER
    python pikobs/build_doc/compare_runs.py sums    BEFORE AFTER

BEFORE, AFTER and NEW are the folders of the runs, <module>_<tag>, under
--out_dir (~/sites8 by default), as mod_run.py names them.

names    the same figures under the same names: how many of BEFORE are
         byte for byte in AFTER; and for each NEW run, the figures that
         BEFORE did not have -- the ones an option adds.
content  the same images whatever their names: every figure of BEFORE with
         an identical twin in AFTER, and which were renamed.
sums     the aggregated databases: the sums of moyenne and pairs per value of
         the special column (the old typed column before, 'special' after)
         -- for a change that renames figures and retitles them.
"""
import argparse
import glob
import hashlib
import math
import os
import sqlite3
import sys
from collections import Counter

OLD_SPECIAL = ("WIND_COMP_METHOD", "elevation")


def pngs(root):
    """{relative path: md5} of every figure of a run."""
    return {os.path.relpath(p, root): hashlib.md5(open(p, "rb").read()).hexdigest()
            for p in glob.glob(f"{root}/**/*.png", recursive=True)}


def cmd_names(dirs, names):
    a, b = pngs(dirs[0]), pngs(dirs[1])
    same = sum(a[k] == b.get(k) for k in a)
    print(f"{names[1]}: {len(b)} figures, {same} of {len(a)} identical to {names[0]}")
    for d, n in zip(dirs[2:], names[2:]):
        c = pngs(d)
        new = sorted(k for k in c if k not in a)
        print(f"{n}: {len(c)} figures, {len(new)} new, for example:")
        for k in new[:4]:
            print("   ", os.path.basename(k))
    return same == len(a) and len(a) == len(b)


def cmd_content(dirs, names):
    a, b = pngs(dirs[0]), pngs(dirs[1])
    twins = sum((Counter(a.values()) & Counter(b.values())).values())
    by_hash = {h: k for k, h in b.items()}
    renamed = [(k, by_hash[h]) for k, h in a.items() if k not in b and h in by_hash]
    print(f"{names[1]}: {len(b)} figures, {twins} of {len(a)} with an identical twin, "
          f"{len(renamed)} renamed")
    for old, new in renamed[:2]:
        print(f"    {os.path.basename(old)}\n -> {os.path.basename(new)}")
    return twins == len(a) == len(b)


def sums(path):
    """{(table, special value): [sums]} of one aggregated database."""
    out = {}
    with sqlite3.connect(path) as c:
        for t in ("moyenne", "pairs"):
            cols = [r[1] for r in c.execute(f"PRAGMA table_info('{t}')")]
            if not cols:
                continue
            sp = ("special" if "special" in cols
                  else next((x for x in OLD_SPECIAL if x in cols), "'all'"))
            vals = [x for x in cols if x in ("n", "sumx", "sumy")
                    or x.startswith(("n_", "sx_"))]
            if not vals:
                continue
            for row in c.execute(f"SELECT {sp}, {', '.join(f'SUM({v})' for v in vals)} "
                                 f"FROM {t} GROUP BY 1"):
                try:
                    k = float(row[0])
                except (TypeError, ValueError):
                    k = str(row[0])
                out[(t, k)] = [x or 0 for x in row[1:]]
    return out


def cmd_sums(dirs, names):
    a, b = dirs[0], dirs[1]
    files = sorted(os.path.relpath(p, a) for p in glob.glob(f"{a}/**/*.db", recursive=True))
    bad = []
    for f in files:
        if not os.path.isfile(os.path.join(b, f)):
            bad.append(f)
            continue
        x, y = sums(os.path.join(a, f)), sums(os.path.join(b, f))
        if x.keys() != y.keys() or any(
                not all(math.isclose(u, v, rel_tol=1e-9, abs_tol=1e-12)
                        for u, v in zip(x[k], y[k])) for k in x):
            bad.append(f)
    print(f"{len(files)} databases, {len(files) - len(bad)} with the same sums per special value")
    for f in bad[:5]:
        print("   differs:", f)
    return bool(files) and not bad


def main():
    ap = argparse.ArgumentParser(
        description="Compare runs made with mod_run.py.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("\n\n", 2)[2])
    ap.add_argument("mode", choices=["names", "content", "sums"])
    ap.add_argument("runs", nargs="+", metavar="RUN")
    ap.add_argument("--out_dir", default="~/sites8",
                    help="where mod_run.py put the runs (default ~/sites8)")
    a = ap.parse_args()
    if len(a.runs) < 2 or (a.mode != "names" and len(a.runs) != 2):
        ap.error(f"{a.mode} needs BEFORE AFTER" + (" [NEW ...]" if a.mode == "names" else ""))
    base = os.path.expanduser(a.out_dir)
    dirs = [os.path.join(base, r) for r in a.runs]
    missing = [d for d in dirs if not os.path.isdir(d)]
    if missing:
        sys.exit(f"no such run: {', '.join(missing)}")
    ok = {"names": cmd_names, "content": cmd_content, "sums": cmd_sums}[a.mode](dirs, a.runs)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
