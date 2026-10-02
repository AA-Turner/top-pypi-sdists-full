#!/usr/bin/env python
"""The name of every family at each stage, cutoff to postalt, as a CSV.

Reads one cycle -- the latest present in every stage -- and writes
pikobs/configobs/cutoff_to_postalt.csv: one row per family, and for each
stage the files it has there. cutoff and derialt come from the banco of
the suite, the only place they are; evalalt, bgckalt and postalt from
monitoring/banco, the SQLite files the modules read -- where a RARS
broadcast keeps files of its own (mwhs2_rars next to mwhs2). The Families
page reads the CSV; run this again when the chain changes (banco need not
be reachable where the documentation is built).

A file belongs to the family its name starts with:
  ai_acars, ai_amdar ...      -> ai
  ..._qc, ..._b, ..._allsky   -> the same family
  sf2, gp2                    -> sf, gp
  rars_amsua, rars_amsub      -> to_amsua, to_amsub; rars_<x> -> <x>
  crisfsr, crisfsr1_qc        -> cris
  tar_ch_...                  -> ch

    python pikobs/build_doc/make_chain_csv.py            # G2
    python pikobs/build_doc/make_chain_csv.py g0
"""
import csv
import os
import re
import sys

STAGES = ("cutoff", "derialt", "evalalt", "bgckalt", "postalt")
FROM_MONITORING = ("evalalt", "bgckalt", "postalt")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "configobs",
                   "cutoff_to_postalt.csv")


def family_of(name):
    n = name.lower()
    n = re.sub(r"(_qc|_b)$", "", n)
    n = re.sub(r"(_qc|_b)$", "", n)
    if n.startswith("rars_"):
        inst = n[5:]
        return {"amsua": "to_amsua", "amsub": "to_amsub"}.get(inst, inst)
    if n.startswith("tar_ch"):
        return "ch"
    if n.startswith("crisfsr") or n == "cris":
        return "cris"
    parts = n.split("_")
    if parts[0] == "to" and len(parts) > 1:
        return "_".join(parts[:2])
    return {"sf2": "sf", "gp2": "gp"}.get(parts[0], parts[0])


def main():
    suite = sys.argv[1] if len(sys.argv) > 1 else "g2"
    suite_banco = os.path.expanduser(f"~smco500/maestro_suites/gdps/{suite}/hub/ppp7/banco")
    monitoring = os.path.expanduser(f"~smco500/.suites/gdps/{suite}/hub/ppp7/monitoring/banco")
    where = {}
    for st in STAGES:
        first = monitoring if st in FROM_MONITORING else suite_banco
        for base in (first, suite_banco):
            if os.path.isdir(os.path.join(base, st)):
                where[st] = os.path.join(base, st)
                break
    missing = [s for s in STAGES if s not in where]
    if missing:
        print(f"[chain] stages not found: {' '.join(missing)}")
    sets = [{f[:10] for f in os.listdir(d) if re.match(r"\d{10}_", f)} for d in where.values()]
    common = sorted(set.intersection(*sets))
    if not common:
        sys.exit("[chain] no cycle present in every stage")
    cycle = common[-1]
    chain, order = {}, []
    for st, d in where.items():
        for f in sorted(os.listdir(d)):
            if not f.startswith(cycle + "_"):
                continue
            name = f[len(cycle) + 1:]
            fam = family_of(name)
            if fam not in chain:
                chain[fam] = {s: [] for s in STAGES}
                order.append(fam)
            if name not in chain[fam][st]:
                chain[fam][st].append(name)
    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["family"] + list(STAGES))
        for fam in sorted(order):
            w.writerow([fam] + [" ".join(chain[fam][s]) for s in STAGES])
    print(f"[chain] {suite} cycle {cycle}: {len(order)} families -> {os.path.normpath(OUT)}")
    for st in STAGES:
        if st in where:
            print(f"  {st:8s} {where[st]}")


if __name__ == "__main__":
    main()
