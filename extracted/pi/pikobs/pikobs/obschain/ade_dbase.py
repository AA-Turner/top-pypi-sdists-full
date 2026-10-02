"""Build the dbase stage of a cycle from ADE, the origin of the dbase,
instead of the one PSMON converts (which lacks the RARS of ATMS and most of
the radiosondes).

    python ade_dbase.py CYCLE OUTDIR [--dry] [--retry] [--late] [--dirs PREFIX ...]
                        [--orders LOG ...]

--orders: logs of other pikobsburp2rdb runs (the conversion of cutoff, say)
to take the burp2rdb order of a name from, when this one has none.

Copies the file of CYCLE of every ADE directory below (ADE keeps two or
three days: run it soon), converts them with pikobsburp2rdb, and writes
OUTDIR/dbase/CYCLE_<name>_dbase, a name obschain gives to the right family.
Pass OUTDIR/dbase to obschain as the dbase stage.

pikobsburp2rdb adds -ade to burp2rdb only for some names (the RARS ones,
the conventional ones); a file of ADE needs it always -- without it the
global radiances and ro come out empty. So every file that comes out empty
is converted again with the same burp2rdb order plus -ade. --retry does
only that, on a work directory already there.

By default the dbase of a cycle is the file of that cycle in every ADE
directory, as it is: no window of time decides what is counted.
--late (off by default) also takes, for the conventional directories, the
two following files and keeps only the observations of the window of the
cycle -- ADE files go by the time they are received, and a late sounding
is in the file of 00 or 06.
--dirs uprair/ does only the directories starting so (into the same
OUTDIR/dbase, next to what is already there)."""
import re
import csv
import os
import shutil
import subprocess
import sys
from collections import defaultdict

ADE = os.path.expanduser("~sade200/data/ade/dbase")

# ADE directory -> the name of the same observations in cutoff (ch left out)
ADE_TO_CUTOFF = [
    ("remote/iasi", "iasi"), ("remote/crisfsr", "crisfsr"), ("remote/csr", "csr"),
    ("remote/ssmis", "ssmis"), ("remote/ascat", "sc_ascat"), ("remote/hscat", "sc_hscat"),
    ("remote/satwinds/geo", "sw_geo"), ("remote/satwinds/polar", "sw_polar"),
    ("remote/tovs1b/mhs", "to_amsub"), ("remote/tovs1b/amsua", "to_amsua"),
    ("remote/rars/mhs", "rars_amsub"), ("remote/rars/amsua", "rars_amsua"),
    ("remote/rars/mwhs2", "rars_mwhs2"), ("remote/rars/atms", "rars_atms"),
    ("remote/gpsocc", "ro"), ("remote/gpssfc", "gp"), ("remote/atms", "atms"),
    ("uprair/acars", "ai_acars"), ("uprair/amdar", "ai_amdar"),
    ("uprair/airep", "ai_airep"), ("uprair/ads", "ai_ads"),
    ("uprair/radiosonde", "ua_radiosonde"), ("uprair/radiosonde_b", "ua_radiosonde_b"),
    ("surface/synop", "sf_synop"), ("surface/synop_b", "sf_synop_b"),
    ("surface/metar", "sf_metar"),
    ("swob/ca", "sf_ca"), ("swob/winide", "sf_winide"),
    ("swob/nchwos", "sf_hwos"), ("swob/ncawos", "sf_awos"),
    ("swob/non/bcforest", "sf_drifter"), ("swob/non/cocorahs", "sf_drifter"),
    ("swob/non/bctran", "sf_drifter"), ("swob/non/mnr", "sf_drifter"),
    ("swob/non/trca", "sf_drifter"), ("swob/non/grca", "sf_drifter"),
]
# gp_b (remote/gpssfc_b) is left out: cutoff has it too, but it is another
# version that does not reach postalt, and obschain does not count it there


LATE = ("uprair/", "surface/", "swob/")     # the ones that arrive late
LATE_BINS = (0, 6, 12, 18)                 # the file of the cycle and the three after


def shift(cycle, hours):
    from datetime import datetime, timedelta
    t = datetime.strptime(cycle, "%Y%m%d%H") + timedelta(hours=hours)
    return t.strftime("%Y%m%d%H")


def keep_window(path, cycle):
    """Keep only the reports of the window of the cycle, -3 h to +3 h."""
    import sqlite3
    lo = int(shift(cycle, -3) + "0000")
    hi = int(shift(cycle, 3) + "0000")
    when = "(CAST(date AS INTEGER) * 1000000 + CAST(time AS INTEGER))"
    with sqlite3.connect(path) as c:
        cols = {r[1].lower() for r in c.execute("PRAGMA table_info(header)")}
        if not {"date", "time"} <= cols:
            return None
        out = f"{when} < {lo} OR {when} >= {hi}"
        gone = c.execute(f"SELECT COUNT(*) FROM header WHERE {out}").fetchone()[0]
        if gone:
            c.execute(f"DELETE FROM data WHERE id_obs IN (SELECT id_obs FROM header WHERE {out})")
            c.execute(f"DELETE FROM header WHERE {out}")
        left = c.execute("SELECT COUNT(*) FROM header").fetchone()[0]
    return gone, left


def has_reports(path):
    """A converted file with at least one report in it."""
    import sqlite3
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return False
    try:
        with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as c:
            return c.execute("SELECT 1 FROM header LIMIT 1").fetchone() is not None
    except sqlite3.Error:
        return False


def family_of(cutoff_name, table):
    for fam, stages in table.items():
        if cutoff_name in stages.get("cutoff", []):
            return fam
    return None


def main():
    argv = sys.argv[1:]
    extra_logs = []
    if "--orders" in argv:
        i = argv.index("--orders")
        j = i + 1
        while j < len(argv) and not argv[j].startswith("--"):
            extra_logs.append(os.path.expanduser(argv[j])); j += 1
        argv = argv[:i] + argv[j:]
    dirs_only = []
    if "--dirs" in argv:
        i = argv.index("--dirs")
        dirs_only = [a for a in argv[i + 1:] if not a.startswith("--")]
        argv = argv[:i] + [a for a in argv[i + 1:] if a.startswith("--")]
    args = [a for a in argv if not a.startswith("--")]
    dry = "--dry" in sys.argv
    use_late = "--late" in sys.argv
    retry = "--retry" in sys.argv
    cycle, out = args[0], os.path.abspath(os.path.expanduser(args[1]))
    import pikobs
    from pikobs.obschain.obschain import chain_table, dbase_family
    table = chain_table()
    families = list(table)
    work = os.path.join(out, "ade_work")
    dbase = os.path.join(out, "dbase")
    # several ADE directories give one cutoff name (sf_drifter): each keeps
    # its own file, named after its directory
    by_name = defaultdict(list)
    for d, name in ADE_TO_CUTOFF:
        if dirs_only and not any(d.startswith(p) for p in dirs_only):
            continue
        by_name[name].append(d)
    plan = []
    for name, dirs in by_name.items():
        fam = family_of(name, table)
        if fam is None:
            print(f"[ade] {name}: no family in cutoff_to_postalt.csv, skipped")
            continue
        for d in dirs:
            out_name = name if len(dirs) == 1 else f"{name}_{d.rsplit('/', 1)[-1]}"
            if dbase_family(out_name, families) != fam:
                out_name = f"{fam}_{out_name}"
            late = use_late and d.startswith(LATE)
            for h in (LATE_BINS if late else (0,)):
                src = os.path.join(ADE, d, f"{shift(cycle, h)}_")
                tag = d.replace("/", "-") + (f"-p{h}" if h else "")
                plan.append(dict(src=src, tag=tag, name=name, fam=fam, window=late,
                                 out=out_name + (f"_p{h}" if h else "")))
    for p in plan:
        ok = os.path.exists(p["src"])
        print(f"[ade] {p['src']:70s} -> {p['out']}_dbase ({p['fam']})"
              f"{'' if ok else '   MISSING in ADE'}")
    if dry:
        return
    # 1. copy, before ADE drops the cycle
    for p in ([] if retry else plan):
        if not os.path.exists(p["src"]):
            continue
        d = os.path.join(work, "in", p["tag"])
        os.makedirs(d, exist_ok=True)
        shutil.copy2(p["src"], os.path.join(d, f"{cycle}_{p['name']}"))
    # 2. convert, one experience per ADE directory
    done = [p for p in plan if os.path.exists(os.path.join(work, "in", p["tag"]))]
    cmd = [sys.executable, "-c", "import pikobs; pikobs.pikobsburp2rdb.arg_call()",
           "--path_experience_files"] + [os.path.join(work, "in", p["tag"]) for p in done] + \
          ["--experience_name"] + [p["tag"] for p in done] + \
          ["--pathwork", os.path.join(work, "out"), "--datestart", cycle, "--dateend", cycle,
           "--family"] + sorted({p["name"] for p in done}) + \
          ["--n_cpus", "40", "--no_submit"]
    if not retry:
        with open(os.path.join(work, "convert.log"), "w") as log:
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
    # 2b. what came out empty, again with -ade
    orders, other = {}, {}
    for log_path, into in [(os.path.join(work, "convert.log"), orders)] + \
                          [(x, other) for x in extra_logs]:
        if not os.path.exists(log_path):
            continue
        with open(log_path, errors="replace") as fh:
            for line in fh:
                if "burp2rdb -in " in line:
                    m = re.search(r"-out (\S+?)(\.tmp)?(\s|$)", line)
                    if m:
                        into[m.group(1)] = line.strip()
    # the order burp2rdb got for each cutoff name (any of its directories):
    # a file pikobsburp2rdb did not convert at all (the late ones) gets the
    # same order, with its own input and output
    by_name = {}
    for out_path, order in list(orders.items()) + list(other.items()):
        m = re.search(r"/" + re.escape(cycle) + r"_(\S+?)$", out_path)
        if m:
            by_name.setdefault(m.group(1), order)
    redo = []
    for p in done:
        f = os.path.join(work, "out", p["tag"], f"{cycle}_{p['name']}")
        src = os.path.join(work, "in", p["tag"], f"{cycle}_{p['name']}")
        if has_reports(f):
            continue
        base_order = orders.get(f) or by_name.get(p["name"])
        if not base_order or (f in orders and " -ade" in orders[f]):
            continue
        order = re.sub(r"-in \S+", f"-in {src}", base_order)
        order = re.sub(r"-out \S+", f"-out {f}", order)
        if " -ade" not in order:
            order += " -ade"
        os.makedirs(os.path.dirname(f), exist_ok=True)
        if os.path.exists(f):
            os.remove(f)
        redo.append((p["out"], order))
    if redo:
        print(f"[ade] {len(redo)} file(s) empty or not converted, converted (again) with -ade: "
              + " ".join(n for n, _ in redo), flush=True)
        from concurrent.futures import ThreadPoolExecutor
        def run(item):
            name, order = item
            with open(os.path.join(work, f"retry_{name}.log"), "w") as log:
                return name, subprocess.run(order, shell=True, stdout=log,
                                            stderr=subprocess.STDOUT).returncode
        with ThreadPoolExecutor(max_workers=16) as ex:
            for name, rc in ex.map(run, redo):
                if rc:
                    print(f"[ade] {name}: burp2rdb -ade returned {rc}, see {work}/retry_{name}.log")
    # 3. place them as the dbase stage
    os.makedirs(dbase, exist_ok=True)
    for p in done:
        f = os.path.join(work, "out", p["tag"], f"{cycle}_{p['name']}")
        target = os.path.join(dbase, f"{cycle}_{p['out']}_dbase")
        if os.path.exists(f) and os.path.getsize(f) > 0:
            shutil.copy2(f, target)
            note = ""
            if p.get("window"):
                w = keep_window(target, cycle)
                if w:
                    note = f"   {w[1]:,d} reports in the window, {w[0]:,d} outside dropped"
            print(f"[ade] {os.path.basename(target):45s} {os.path.getsize(target) / 2**20:8.1f} MB{note}")
        else:
            print(f"[ade] {p['out']}: the conversion gave nothing, see {work}/convert.log")
    print(f"[ade] dbase stage: {dbase}")


if __name__ == "__main__":
    main()
