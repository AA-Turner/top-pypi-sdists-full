#!/usr/bin/env python
"""The data of the BUFR element search on the Varno page.

For every element of the CMC table B (table_b_bufr_e, table_b_bufr_f): its
code, its name in English and in French, its unit, the WMO name when
eccodes has it, and -- from configobs/postalt_varnos.csv -- the families
that assimilate it and those that only carry it, read in the data table
of the last complete postalt cycles (and configobs/postalt_varnos.csv). Written once to
docs/source/_static/varno_search.js (a plain script, so the search works
from any copy of the pages, even opened from disk) and kept in the
repository: building the documentation never needs the tables.

Run it again when the tables or the families change:

    python pikobs/build_doc/make_varno_search.py [--table-dir DIR]

The CMC tables are looked for in --table-dir, $PIKOBS_TABLE_B,
$AFSISIO/datafiles/constants, $CMCCONST and the operational copy,
/home/smco502/datafiles/constants, in that order.
"""
import argparse
import csv
import glob
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
VARNOS = os.path.join(REPO, "pikobs", "configobs", "postalt_varnos.csv")
CUTOFF = os.path.join(REPO, "pikobs", "configobs", "cutoff_varnos.csv")
OUT = os.path.join(REPO, "docs", "source", "_static", "varno_search.js")


def table_dir(given):
    for d in (given, os.environ.get("PIKOBS_TABLE_B"),
              os.path.join(os.environ.get("AFSISIO", ""), "datafiles", "constants"),
              os.environ.get("CMCCONST"),
              "/home/smco502/datafiles/constants"):         # the operational copy
        if d and os.path.isfile(os.path.join(d, "table_b_bufr_e")):
            return d
    sys.exit("table_b_bufr_e not found: give its folder with --table-dir "
             "or $PIKOBS_TABLE_B")


def read_cmc(path):
    """code -> (name, unit), from the fixed-width CMC table B."""
    out = {}
    for line in open(path, encoding="latin-1"):
        if line.startswith("*") or len(line) < 8 or not line[:6].isdigit():
            continue
        code = line[:6]
        name = line[8:52].strip()
        unit = line[52:65].strip()
        out[code] = (name, unit)
    return out


def read_wmo():
    """code -> name, from the WMO table B that eccodes ships (optional)."""
    try:
        import eccodes
        base = eccodes.codes_definition_path()
    except Exception:
        base = os.environ.get("ECCODES_DEFINITION_PATH", "")
    tables = sorted(glob.glob(os.path.join(base, "bufr", "tables", "0", "wmo", "*",
                                           "element.table")),
                    key=lambda p: int(os.path.basename(os.path.dirname(p)))
                    if os.path.basename(os.path.dirname(p)).isdigit() else -1)
    if not tables:
        return {}, None
    out = {}
    for line in open(tables[-1], encoding="utf-8", errors="replace"):
        parts = line.rstrip("\n").split("|")
        if len(parts) > 3 and parts[0].isdigit():
            out[parts[0].zfill(6)] = parts[3].strip()
    return out, os.path.basename(os.path.dirname(tables[-1]))


def read_families():
    """varno -> (families that assimilate it, families that carry it only)."""
    used, carried = {}, {}
    for row in csv.DictReader(open(VARNOS)):
        v = str(row["varno"]).zfill(6)
        # obs and assimilated are counts: a family that assimilated none of
        # its observations of an element only carries it
        def count(k):
            try:
                return float(row.get(k) or 0)
            except ValueError:
                return 0.0
        if count("obs") <= 0 and count("assimilated") <= 0:
            continue
        yes = count("assimilated") > 0
        (used if yes else carried).setdefault(v, set()).add(row["family"])
    return used, carried


POSTALT = "/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"


def read_postalt(postalt, n_cycles):
    """varno -> ({family: assimilated}, {family: observations}), from the
    data table of the last complete cycles: what the files really carry,
    not only what pikobs expects of each family."""
    import sqlite3
    from collections import defaultdict
    names = [f for f in os.listdir(postalt) if len(f) > 11 and f[:10].isdigit() and f[10] == "_"]
    cycles = sorted({f[:10] for f in names})[-(n_cycles + 1):-1]     # the last may be incomplete
    obs, ass = defaultdict(lambda: defaultdict(int)), defaultdict(lambda: defaultdict(int))
    for f in sorted(names):
        if f[:10] not in cycles:
            continue
        family = f[11:]
        try:
            con = sqlite3.connect(f"file:{os.path.join(postalt, f)}?mode=ro", uri=True)
            rows = con.execute("SELECT varno, COUNT(*), SUM((flag & 4096) = 4096) "
                               "FROM data GROUP BY varno;").fetchall()
            con.close()
        except sqlite3.Error as exc:
            print(f"  {f}: {exc}", file=sys.stderr)
            continue
        for varno, n, a in rows:
            if varno is None:
                continue
            code = str(int(varno)).zfill(6)
            obs[code][family] += n or 0
            ass[code][family] += a or 0
    print(f"postalt: {len(cycles)} cycles ({cycles[0] if cycles else '-'} to "
          f"{cycles[-1] if cycles else '-'}), {len(obs)} varnos in the files")
    return ass, obs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table-dir")
    ap.add_argument("--postalt", default="",
                    help="also read the families from this postalt folder "
                         "(by default the CSV of make_varno_csv.py is enough)")
    ap.add_argument("--cycles", type=int, default=4,
                    help="how many of its last complete cycles (default 4, a day)")
    args = ap.parse_args()
    d = table_dir(args.table_dir)
    en = read_cmc(os.path.join(d, "table_b_bufr_e"))
    fr = read_cmc(os.path.join(d, "table_b_bufr_f")) if os.path.isfile(
        os.path.join(d, "table_b_bufr_f")) else {}
    used, carried = read_families()
    if args.postalt and os.path.isdir(args.postalt):
        ass, obs = read_postalt(args.postalt, args.cycles)
        for code, fams in obs.items():
            for fam, n in fams.items():
                if ass[code][fam] > 0:
                    used.setdefault(code, set()).add(fam)
                elif n > 0:
                    carried.setdefault(code, set()).add(fam)
    cutoff = {}
    if os.path.isfile(CUTOFF):               # make_cutoff_varnos.py
        for r in csv.DictReader(open(CUTOFF)):
            cutoff.setdefault(str(r["varno"]).zfill(6), set()).add(r["family"])
    # only what is observed, as on the page: the rest becomes header columns
    in_post = set(used) | set(carried)
    cutoff = {c: f for c, f in cutoff.items() if c in in_post or int(c) // 1000 in {11, 12, 13, 14, 15, 20, 21, 22, 40}}
    wmo, wmo_version = read_wmo()
    if not wmo:
        # no eccodes here: the WMO names pikobs already keeps for its varnos
        try:
            sys.path.insert(0, REPO)
            from pikobs.configobs.type_varno import type_varno
            for code in set(used) | set(carried):
                name = str(type_varno(int(code))[0]).split(":", 1)[-1].strip()
                if name and not name.isdigit():
                    wmo[code] = name
            wmo_version = "as pikobs names them"
        except Exception as exc:
            print(f"no WMO names from pikobs either: {exc}", file=sys.stderr)
    rows = []
    for code in sorted(set(en) | set(used) | set(carried) | set(cutoff)):
        name, unit = en.get(code, ("", ""))
        rows.append({
            "code": code, "varno": int(code),
            "en": name, "fr": fr.get(code, ("", ""))[0], "unit": unit,
            "wmo": wmo.get(code, ""),
            "used": sorted(used.get(code, ())),
            "carried": sorted(carried.get(code, set()) - used.get(code, set())),
            "cutoff": sorted(cutoff.get(code, set()) - used.get(code, set())
                             - carried.get(code, set())),
        })
    meta = {"cmc": d, "wmo": f"WMO table B version {wmo_version}" if wmo_version else "",
            "elements": len(rows)}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("// GENERATED by pikobs/build_doc/make_varno_search.py -- do not edit\n")
        fh.write(f"window.PIKOBS_VARNOS = {json.dumps(rows, ensure_ascii=False, separators=(',', ':'))};\n")
        fh.write(f"window.PIKOBS_VARNOS_META = {json.dumps(meta, ensure_ascii=False)};\n")
    n_used = sum(1 for r in rows if r["used"])
    print(f"{OUT}: {len(rows)} elements, {n_used} assimilated by some family, "
          f"{sum(1 for r in rows if r['fr'])} with a French name, "
          f"{sum(1 for r in rows if r['wmo'])} with a WMO name "
          f"({os.path.getsize(OUT) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
