#!/usr/bin/env python
"""Do the comparing modules count the same pairs?

Every comparing module pairs the two runs through pikobs.match and stores,
per selection, the number of pairs and five sums. For one family, region
and flag criterion over the same period, the totals must therefore be the
same whichever module computed them: timeserie summed over its cycles,
cardio over its cycles, zone over its latitude bands, profile over its
levels, scatter over its boxes, vdedr over its channels. A module whose
totals differ filters something differently -- a level, a varno, a
criterion -- and nothing else would show it.

Reads the pair tables of the reference runs; runs nothing.

    python coherence.py                        # every pikobs_doc_*
    python coherence.py --q oma                # O-A instead of O-P
    python coherence.py /path/to/runs ...

For every (family, region, criterion) present in two modules or more it
prints each module's N, mean of the control, mean of the experience and
sigma of each, and marks the rows that disagree with the first one.
"""
import argparse
import glob
import math
import os
import re
import sqlite3
from collections import defaultdict

# the GPS-RO families, where verifprofile normalises (as in configobs)
RO_FAMILIES = ('ro', 'ro_qc', 'gpsocc')


def scatter_name(base, family):
    """(region, flag) from a scatter pair file name; the family is known."""
    m = re.search(r"_(?P<region>[A-Za-z]+)_\d{10}_\d{10}_bx[\d.]+_by[\d.]+_"
                  r"(?P<flag>.+)_" + re.escape(family) + r"\.db$", base)
    return (m["region"], m["flag"]) if m else None


def layout(cols, q):
    """(n, sx, sy, sxx, syy, sxy) column names of quantity q, or None."""
    c = set(cols)
    for n in (f"n_{q}", f"n{q}"):
        names = (n, f"sx_{q}", f"sy_{q}", f"sxx_{q}", f"syy_{q}", f"sxy_{q}")
        if set(names) <= c:
            return names
    # histogram: moments per fonction -- n, c1 c2 (control), e1 e2, ce
    if {'fonction', 'n', 'c1', 'c2', 'e1', 'e2', 'ce'} <= c:
        return ('n', 'c1', 'e1', 'c2', 'e2', 'ce')
    counts = {'omp': ('n_p', 'n_omp', 'n'), 'oma': ('n_a', 'n_oma')}[q]
    sums = (f"c_{q}", f"e_{q}", f"c2_{q}", f"e2_{q}", f"ce_{q}")
    if set(sums) <= c:
        n = next((k for k in counts if k in c), None)
        if n:
            return (n,) + sums
    return None


def one_value(con, table, col, prefer):
    """Restrict col to `prefer` if that value exists, else to nothing."""
    vals = [r[0] for r in con.execute(f'SELECT DISTINCT "{col}" FROM "{table}"')]
    if prefer in vals:
        return f'"{col}" = \'{prefer}\''
    if col == 'channel_mode' and vals:           # never sum two modes
        return f'"{col}" = \'{vals[0]}\''
    return None


def totals(path, family, module, q):
    """{(family, region, flag): (n, sx, sy, sxx, syy, sxy)} of one database."""
    out = {}
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")]
    m = scatter_name(os.path.basename(path), family)
    for t in tables:
        cols = [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')]
        names = layout(cols, q)
        if not names:
            continue
        where = ["1=1"]
        if 'fonction' in cols:
            where.append(f"fonction = '{q}'")
        for col, prefer in (('land_ocean', 'all'), ('channel_mode', 'join'),
                            ('special', 'all'), ('id_stn', 'join'),
                            ('lkey', 'join')):
            if col in cols:
                w = one_value(con, t, col, prefer)
                if w:
                    where.append(w)
        if 'region' in cols and 'flag' in cols:
            q_sql = (f'SELECT region, flag, {", ".join(f"SUM({x})" for x in names)} '
                     f'FROM "{t}" WHERE {" AND ".join(where)} GROUP BY region, flag')
            for region, flag, *s in con.execute(q_sql):
                out[(family, region, flag)] = s
        elif m:
            s = con.execute(f'SELECT {", ".join(f"SUM({x})" for x in names)} '
                            f'FROM "{t}" WHERE {" AND ".join(where)}').fetchone()
            out[(family, m[0], m[1])] = list(s)
    con.close()
    return out


def moments(s):
    n, sx, sy, sxx, syy, sxy = (float(v or 0) for v in s)
    if n <= 0:
        return n, math.nan, math.nan, math.nan, math.nan
    mx, my = sx / n, sy / n
    return (n, mx, my, math.sqrt(max(sxx / n - mx * mx, 0)),
            math.sqrt(max(syy / n - my * my, 0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*")
    ap.add_argument("--q", default="omp", choices=("omp", "oma"))
    ap.add_argument("--tol", type=float, default=1e-6)
    args = ap.parse_args()
    dirs = args.dirs or sorted(d for d in glob.glob(
        f"/home/{os.environ.get('USER', '')}/sites8/pikobs_doc_*")
        if not d.endswith("_exp"))

    table = defaultdict(dict)
    scatter_layers = defaultdict(dict)
    for d in dirs:
        module = re.sub(r"^pikobs_(doc|coh)_", "", os.path.basename(os.path.normpath(d)))
        for path in sorted(glob.glob(os.path.join(d, "*", "*.db"))):
            family = os.path.basename(os.path.dirname(path))
            try:
                got = totals(path, family, module, args.q)
            except sqlite3.DatabaseError as exc:
                print(f"unreadable {path}: {exc}")
                continue
            tag = module
            base = os.path.basename(path)
            if module in ('zone', 'verifprofile'):
                tag += "[join]" if "_join_" in base else "[all]"
            # on the GPS-RO families only, verifprofile divides the departure
            # by the reference refractivity and applies the GPS-RO quality
            # gates: another quantity, compared with itself only. Any other
            # family (ch, MLS) is the ordinary departure and is compared.
            if module == 'verifprofile':
                got = {((f"{k[0]} (/ref, QC gates)",) + k[1:]
                        if k[0] in RO_FAMILIES else k): v
                       for k, v in got.items()}
            # scatter writes one database per layer; keep them apart here
            layer = re.match(r"scatter_pair_layer_(all|[\d.]+_[\d.]+(?:hPa|km))_", base)
            for key, s in got.items():
                if module == 'scatter' and layer:
                    scatter_layers[key][layer.group(1)] = s
                else:
                    table[key][tag] = s

    # scatter: the 'all' layer when it holds pairs, otherwise the sum of the
    # layers -- which also tests that the layers do not overlap at their edges
    for key, layers in scatter_layers.items():
        whole = layers.get('all')
        if whole and (whole[0] or 0) > 0:
            table[key]['scatter'] = whole
        else:
            parts = [v for k, v in layers.items() if k != 'all']
            if parts:
                table[key][f"scatter[{len(parts)} layers]"] = [
                    sum((p[i] or 0) for p in parts) for i in range(6)]

    shared = {k: v for k, v in table.items() if len(v) > 1}
    if not shared:
        print("no (family, region, criterion) is computed by two modules")
        return
    bad = 0
    for key in sorted(shared):
        fam, region, flag = key
        rows = shared[key]
        print(f"\n{fam}  {region}  {flag}   ({args.q})")
        print(f"   {'module':<18} {'N':>12} {'mean ctl':>11} {'mean exp':>11} "
              f"{'sigma ctl':>10} {'sigma exp':>10}")
        ref = None
        for tag, s in sorted(rows.items()):
            n, mx, my, sx_, sy_ = moments(s)
            mark = ""
            if ref is None:
                ref = (n, mx, my, sx_, sy_)
            else:
                off = [abs(a - b) > args.tol * max(1.0, abs(a), abs(b))
                       for a, b in zip(ref, (n, mx, my, sx_, sy_))
                       if not (math.isnan(a) or math.isnan(b))]
                if any(off):
                    mark = "   <-- differs"
                    bad += 1
            print(f"   {tag:<18} {n:12.0f} {mx:11.5f} {my:11.5f} "
                  f"{sx_:10.5f} {sy_:10.5f}{mark}")
    print(f"\n{len(shared)} selection(s) computed by two modules or more; "
          f"{bad} row(s) disagree")


if __name__ == "__main__":
    main()
