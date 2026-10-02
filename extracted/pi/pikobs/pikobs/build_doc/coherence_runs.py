#!/usr/bin/env python
"""Do the modules count the same observations in each run?

coherence.py compares the pairs, the observations both runs share. This
compares each run on its own: for the control and for the experience
separately, one family, region and criterion must give the same number of
observations with a departure, the same mean and the same sigma, whichever
module counted them. That brings in the modules that do not pair --
obscountdb first -- next to those that do.

Every module is limited to the variables of the family (the varno list
the extraction uses), so a module that keeps every varno of the file --
obscountdb, a census -- is compared on the same ones.

Any table holding n_<q>, s_<q> and s2_<q> with a region and a flag column
is read: timeserie's ts_val, cardio's serie_cardio, obscountdb's moyenne,
and any other module that keeps its per-run sums the same way. Which run a
file belongs to is read from its name (G0 / control, G2 / experience).

    python coherence_runs.py /home/$USER/sites8/pikobs_coh_*
    python coherence_runs.py --q oma /home/$USER/sites8/pikobs_coh_*
"""
import argparse
import glob
import math
import os
import re
import sqlite3
from collections import defaultdict

CONTROL = {"G0", "control"}
EXPERIENCE = {"G2", "experience"}


def role(base):
    tokens = set(re.split(r"[_.]", base))
    if "vs" in tokens:
        return None                      # a pair file: coherence.py's job
    if tokens & CONTROL:
        return "control"
    if tokens & EXPERIENCE:
        return "experience"
    return None


def prefer(con, table, col, value):
    vals = [r[0] for r in con.execute(f'SELECT DISTINCT "{col}" FROM "{table}"')]
    return f'"{col}" = \'{value}\'' if value in vals else None


def family_elements(family):
    """The varnos a family is extracted on ('' if pikobs cannot say)."""
    try:
        import pikobs
        return str(pikobs.family(family)[4] or "")
    except Exception:
        return ""


def totals(path, family, q):
    out = {}
    elements = family_elements(family)
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' "
                            "AND name NOT LIKE '_pikobs%'").fetchall():
        cols = {r[1] for r in con.execute(f'PRAGMA table_info("{t}")')}
        need = {f"n_{q}", f"s_{q}", f"s2_{q}", "region", "flag"}
        if not need <= cols:
            continue
        where = ["1=1"]
        # the variables of the family, as the extraction of every module
        # takes them: a module that stores every varno of the file
        # (obscountdb, a census) is compared on the same ones
        if 'varno' in cols and elements:
            where.append(f"varno IN ({elements})")
        for col, value in (('land_ocean', 'all'), ('id_stn', 'join'),
                           ('channel_mode', 'join'), ('special', 'all'),
                           ('lkey', 'join')):
            if col in cols:
                w = prefer(con, t, col, value)
                if w:
                    where.append(w)
        for region, flag, n, s, s2 in con.execute(
                f'SELECT region, flag, SUM(n_{q}), SUM(s_{q}), SUM(s2_{q}) '
                f'FROM "{t}" WHERE {" AND ".join(where)} GROUP BY region, flag'):
            out[(family, region, flag)] = (n or 0, s or 0.0, s2 or 0.0)
    con.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*")
    ap.add_argument("--q", default="omp", choices=("omp", "oma"))
    ap.add_argument("--tol", type=float, default=1e-6)
    args = ap.parse_args()
    dirs = [d for d in (args.dirs or glob.glob(
        f"/home/{os.environ.get('USER', '')}/sites8/pikobs_coh_*")) if os.path.isdir(d)]

    table = defaultdict(dict)
    for d in sorted(dirs):
        module = re.sub(r"^pikobs_(doc|coh)_", "", os.path.basename(os.path.normpath(d)))
        for path in sorted(glob.glob(os.path.join(d, "*", "*.db"))):
            r = role(os.path.basename(path))
            if not r:
                continue
            family = os.path.basename(os.path.dirname(path))
            try:
                got = totals(path, family, args.q)
            except sqlite3.DatabaseError as exc:
                print(f"unreadable {path}: {exc}")
                continue
            for key, v in got.items():
                table[key + (r,)][module] = v

    shared = {k: v for k, v in table.items() if len(v) > 1}
    bad = 0
    for key in sorted(shared):
        fam, region, flag, r = key
        print(f"\n{fam}  {region}  {flag}  {r}   ({args.q})")
        print(f"   {'module':<14} {'N':>12} {'mean':>11} {'sigma':>10}")
        ref = None
        for module, (n, s, s2) in sorted(shared[key].items()):
            mean = s / n if n else math.nan
            sig = math.sqrt(max(s2 / n - mean * mean, 0)) if n else math.nan
            mark = ""
            if ref is None:
                ref = (n, mean, sig)
            elif any(abs(a - b) > args.tol * max(1.0, abs(a), abs(b))
                     for a, b in zip(ref, (n, mean, sig))
                     if not (math.isnan(a) or math.isnan(b))):
                mark = "   <-- differs"
                bad += 1
            print(f"   {module:<14} {n:12.0f} {mean:11.5f} {sig:10.5f}{mark}")
    print(f"\n{len(shared)} selection(s) x run counted by two modules or more; "
          f"{bad} row(s) disagree")
    only = sorted({m for v in table.values() for m in v})
    print(f"modules read: {', '.join(only)}")


if __name__ == "__main__":
    main()
