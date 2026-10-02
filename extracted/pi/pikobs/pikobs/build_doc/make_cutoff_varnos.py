#!/usr/bin/env python
"""What each family brings into the chain: the BUFR codes of its cutoff files.

The postalt files say what is left at the end and what is assimilated;
the cutoff files say what arrives. This takes one complete cycle of cutoff,
converts every file with burp2rdb -- the same way pikobsburp2rdb does,
type and -ade included -- reads the codes it holds, and writes
pikobs/configobs/cutoff_varnos.csv: for every family and code, the
observations, with the cutoff names translated to the pikobs family by the
chain table (configobs/cutoff_to_postalt.csv). The families of ch and asr
are skipped: burp2rdb reads no data from their cutoff files, whatever the
type it is given.

Converting iasi and cris takes a while, so pikobs_doc.sh does not run this;
run it when the chain changes, on a compute node:

    python pikobs/build_doc/make_cutoff_varnos.py            # G2
    python pikobs/build_doc/make_cutoff_varnos.py g0
"""
import csv
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CHAIN = os.path.join(REPO, "pikobs", "configobs", "cutoff_to_postalt.csv")
OUT = os.path.join(REPO, "pikobs", "configobs", "cutoff_varnos.csv")
DOMAIN = "cmd/cmda/utils/20260202/burp2rdb_5.25_rhel-9-amd64-64"     # its libraries
SKIP = {"ch", "asr"}           # cutoff files burp2rdb cannot read, whatever the -type


def burp2rdb():
    sys.path.insert(0, REPO)
    # the module itself: the package exports a name like it, which
    # 'import a.b.c as B' would pick up instead
    import importlib
    B = importlib.import_module("pikobs.pikobsburp2rdb.pikobsburp2rdb")
    return B, B._resolve_burp2rdb()


def convert(B, binary, path, name, tmp):
    """The codes of one cutoff file: {varno: observations}, or an error text."""
    out = os.path.join(tmp, os.path.basename(path) + ".db")
    args = [binary, "-in", path, "-type", B.get_burp_type(name)]
    if B.needs_ade_from_path(path, name):
        args.append("-ade")
    args += ["-out", out]
    # the binary itself, with its libraries loaded -- not the burp2rdb alias,
    # which slips an empty argument in
    cmd = ["bash", "-c", f'. r.load.dot "{DOMAIN}" < /dev/null > /dev/null 2>&1; exec "$@"',
           "burp2rdb"] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        if r.returncode != 0 or not os.path.isfile(out):
            tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or ["no output"]
            return f"burp2rdb failed: {tail[0][:120]}"
        con = sqlite3.connect(out)
        rows = con.execute("SELECT varno, COUNT(*) FROM data GROUP BY varno").fetchall()
        con.close()
        return {int(v): n for v, n in rows if v is not None}
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"
    finally:
        if os.path.isfile(out):
            os.remove(out)


def main():
    suite = sys.argv[1] if len(sys.argv) > 1 else "g2"
    cutoff = os.path.expanduser(f"~smco500/maestro_suites/gdps/{suite}/hub/ppp7/banco/cutoff")
    if not os.path.isdir(cutoff):
        sys.exit(f"[cutoff] {cutoff} not reachable: the CSV of the repository is kept")
    names = [f for f in os.listdir(cutoff) if re.match(r"\d{10}_", f)]
    cycles = sorted({f[:10] for f in names})
    if len(cycles) < 2:
        sys.exit(f"[cutoff] no complete cycle in {cutoff}")
    cycle = cycles[-2]                         # the last one may still be written
    chain = list(csv.DictReader(open(CHAIN)))
    B, binary = burp2rdb()
    if not binary:
        sys.exit("[cutoff] burp2rdb not found: the CSV of the repository is kept")
    jobs = []
    for row in chain:
        fam = row["family"]
        if fam in SKIP:
            continue
        for name in row["cutoff"].split():
            path = os.path.join(cutoff, f"{cycle}_{name}")
            if os.path.isfile(path):
                jobs.append((fam, name, path))
    print(f"[cutoff] {suite} cycle {cycle}: converting {len(jobs)} files "
          f"({', '.join(sorted(SKIP))} skipped)", flush=True)
    tmp = tempfile.mkdtemp(prefix="pikobs_cutoff_")
    obs = defaultdict(lambda: defaultdict(int))
    failed = []
    try:
        with ThreadPoolExecutor(max_workers=min(16, len(jobs) or 1)) as pool:
            futures = {pool.submit(convert, B, binary, p, n, tmp): (f, n) for f, n, p in jobs}
            for fut, (fam, name) in futures.items():
                res = fut.result()
                if isinstance(res, str):
                    failed.append(f"{name}: {res}")
                    continue
                for v, n in res.items():
                    obs[fam][v] += n
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if not obs:
        sys.exit("[cutoff] nothing converted: the CSV of the repository is kept")
    rows = [[fam, v, n] for fam in sorted(obs) for v, n in sorted(obs[fam].items())]
    with open(OUT + ".tmp", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["family", "varno", "obs"])
        w.writerows(rows)
    os.replace(OUT + ".tmp", OUT)
    print(f"[cutoff] {len(obs)} families, {len(rows)} codes -> {OUT}")
    for f in failed:
        print(f"[cutoff]   not converted: {f}")


if __name__ == "__main__":
    main()
