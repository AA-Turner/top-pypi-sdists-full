#!/usr/bin/env python
"""The run time of pikobs, measured the same way for every module.

Phase 1 -- how the time grows with the period. The base selection, the
same for every module: one family (iasi), one region (Monde), one
criterion (assimilee), ID_STN=(all), CHANNEL=(join); 1, 8, 16 and 28
six-hour cycles; each module run three ways:

    with      control against experience, with pairs   (_cont_exp, MATCH=on)
    without   control against experience, no pairs     (_cont_exp, MATCH=off)
    alone     one run on its own, no control           (_exp; mapobs, flags)

Phase 2 -- what the selection adds: one day (4 cycles), with
1 x 1 x 1, 2 x 2 x 2 and 3 x 3 x 3 families x regions x criteria.

obscountdb is apart: every family of postalt, with the departure panels
(AGR=(oma omp)) and without (AGR=()); in phase 2 only its regions and
criteria grow.

A setting a wrapper does not have (flags has no criteria) is left out and
noted. Every job writes its own CSV, so several nodes can measure at once;
"tables" reads them all and writes the three tables, and their RST.

    python pikobs/build_doc/bench_runtime.py phase1 zone cardio --csv node1
    python pikobs/build_doc/bench_runtime.py phase2 zone cardio --csv node1
    python pikobs/build_doc/bench_runtime.py tables
"""
import argparse
import csv
import datetime as dt
import glob
import os
import re
import shutil
import subprocess
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SCRIPTS = os.path.join(REPO, "pikobs", "script")
BUILD = os.path.join(REPO, "pikobs", "build_doc")
DOCS = os.path.join(REPO, "docs", "source")
WORK = os.path.expanduser("~/sites8/pikobs_runtime")
POSTALT = os.environ.get("PIKOBS_BENCH_POSTALT", os.path.expanduser(
    "~smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"))

MODULES = ["cardio", "flags", "histogram", "mapobs", "profile", "scatter",
           "timeserie", "vdedr", "verifprofile", "zone", "obscountdb"]
WRAPPERS = {
    "cardio": "run_cardio_cont_exp.sh", "flags": "run_flags.sh",
    "histogram": "run_histogram_cont_exp.sh", "mapobs": "run_mapobs.sh",
    "profile": "run_profile_cont_exp.sh", "scatter": "run_scatter_cont_exp.sh",
    "timeserie": "run_timeserie_cont_exp.sh", "vdedr": "run_vdedr_cont_exp.sh",
    "verifprofile": "run_verifprofile_cont_exp.sh", "zone": "run_zone_cont_exp.sh",
    "obscountdb": "run_obscountdb_cont_exp.sh",
}
EXP_WRAPPERS = {
    "cardio": "run_cardio_exp.sh", "histogram": "run_histogram_exp.sh",
    "profile": "run_profile_exp.sh", "scatter": "run_scatter_exp.sh",
    "timeserie": "run_timeserie_exp.sh", "verifprofile": "run_verifprofile_exp.sh",
    "zone": "run_zone_exp.sh",
}
SINGLE_RUN = {"mapobs", "flags"}          # their only wrapper is one run on its own

BASE = {"FAMILY": "(iasi)", "REGION": "(Monde)", "FLAGS_CRITERIA": "(assimilee)",
        "ID_STN": "(all)", "CHANNEL": "(join)"}
SELECTIONS = [
    ("1 x 1 x 1", {}),
    ("2 x 2 x 2", {"FAMILY": "(iasi ua)", "REGION": "(Monde HemisphereNord)",
                   "FLAGS_CRITERIA": "(assimilee rejets_qc)"}),
    ("3 x 3 x 3", {"FAMILY": "(iasi ua ai)",
                   "REGION": "(Monde HemisphereNord Tropiques)",
                   "FLAGS_CRITERIA": "(assimilee rejets_qc all)"}),
]
OBSCOUNT = [("with omp/oma", {"FAMILY": "@postalt", "AGR": "(oma omp)"}),
            ("no omp/oma", {"FAMILY": "@postalt", "AGR": "()"})]
PERIODS = [("1 day", 4), ("1 week", 28), ("1 month", 124), ("2 months", 244)]
RUN_ORDER = {"with": 0, "without": 1, "alone": 2, "-": 3}
FIELDS = ["phase", "module", "variant", "run", "selection", "cycles", "wall_s", "rc",
          "extract_s", "plot_s", "figures", "input_gb", "skipped", "peak_gb"]

RX = {
    "extract_s": re.compile(r"(?:extraction|scan|aggregation|matching|compaction) time:\s*([\d.]+)\s*s"),
    "plot_s": re.compile(r"(?:plot|figure) time:\s*([\d.]+)\s*s"),
    "figures": re.compile(r"(?:\bplots?:\s*(?=\d+\s*tasks)|figure time:[^(\n]*\()(\d+)"),
    "input_gb": re.compile(r"input check OK:.*?([\d.]+)\s*(GB|MB)"),
}


# ─────────────────────────────────────────────────────────────────────────────
# Running
# ─────────────────────────────────────────────────────────────────────────────

def postalt_families():
    cycles = sorted({f[:10] for f in os.listdir(POSTALT) if re.match(r"\d{10}_", f)})
    return sorted(f[11:] for f in os.listdir(POSTALT)
                  if f.startswith(cycles[-2] + "_") and os.path.getsize(os.path.join(POSTALT, f)) > 0)


def expand(value):
    return "(" + " ".join(postalt_families()) + ")" if value == "@postalt" else value


def last_cycle():
    d = dt.datetime.utcnow().date() - dt.timedelta(days=3)
    return dt.datetime(d.year, d.month, d.day, 18)


def parse_log(text):
    row = {}
    for k in ("extract_s", "plot_s"):
        v = RX[k].findall(text)
        row[k] = round(sum(float(x) for x in v), 1) if v else ""
    v = RX["figures"].findall(text)
    row["figures"] = sum(int(x) for x in v) if v else ""
    v = RX["input_gb"].findall(text)
    row["input_gb"] = round(float(v[0][0]) / (1000 if v[0][1] == "MB" else 1), 3) if v else ""
    return row


def set_value(text, var, value):
    new, n = re.subn(rf"(?m)^{var}=.*$", f"{var}={value}", text, count=1)
    return new, n == 1


def run_one(wrapper, cycles, match, settings, tag):
    end = last_cycle()
    start = end - dt.timedelta(hours=6 * (cycles - 1))
    pathwork = os.path.join(WORK, tag)
    src = open(os.path.join(SCRIPTS, wrapper)).read()
    for var, val in (("DATESTART", f'"{start:%Y%m%d%H}"'), ("DATEEND", f'"{end:%Y%m%d%H}"'),
                     ("PATHWORK", f'"{pathwork}"'), ("N_CPUS", "80")):
        src, ok = set_value(src, var, val)
        if not ok and var != "N_CPUS":
            raise RuntimeError(f"{wrapper}: no {var}= line")
    if match:
        src, _ = set_value(src, "MATCH", f'"{match}"')
    skipped = []
    for var, val in settings.items():
        src, ok = set_value(src, var, expand(val))
        if not ok:
            skipped.append(var)
    logs = os.path.join(WORK, "logs")
    os.makedirs(logs, exist_ok=True)
    copy = os.path.join(logs, f"{tag}.sh")
    open(copy, "w").write(src)
    log = os.path.join(logs, f"{tag}.log")
    env = dict(os.environ, PBS_O_WORKDIR="")
    t0 = time.time()
    # the memory of the run and all its processes, every 5 s: the peak is
    # what a node must hold for this module and selection. PSS shares the
    # pages several processes map (libraries, the mapobs cache) among
    # them, so they are counted once; RSS when a process does not give it
    import psutil

    def _pss(q):
        try:
            return q.memory_full_info().pss
        except (psutil.Error, AttributeError):
            try:
                return q.memory_info().rss
            except psutil.Error:
                return 0

    peak = 0
    with open(log, "w") as fh:
        proc = subprocess.Popen(["bash", copy], stdout=fh, stderr=subprocess.STDOUT,
                                cwd=logs, env=env)
        top = psutil.Process(proc.pid)
        while proc.poll() is None:
            try:
                peak = max(peak, sum(_pss(q) for q in
                                     [top] + top.children(recursive=True)))
            except psutil.Error:
                pass
            time.sleep(5)
        rc = proc.returncode
    row = {"wall_s": round(time.time() - t0, 1), "rc": rc, "skipped": " ".join(skipped),
           "peak_gb": round(peak / 1e9, 1)}
    text = open(log, errors="replace").read()
    row.update(parse_log(text))
    if "INCOMPLETE:" in text or "tasks lost" in text:
        # the output is missing pieces, and the time is short because it
        # drew less: not a clean run
        row["rc"] = rc or 99
        row["skipped"] = (row["skipped"] + " lost-tasks").strip()
    shutil.rmtree(pathwork, ignore_errors=True)
    return row


def runs_of(m):
    """(wrapper, MATCH value, run label) of every way the module is run."""
    wrapper = WRAPPERS[m]
    has_match = re.search(r"(?m)^MATCH=", open(os.path.join(SCRIPTS, wrapper)).read())
    if m in SINGLE_RUN:
        runs = [(wrapper, None, "alone")]
    elif has_match:
        runs = [(wrapper, "on", "with"), (wrapper, "off", "without")]
    else:
        runs = [(wrapper, None, "-")]
    if m in EXP_WRAPPERS:
        runs.append((EXP_WRAPPERS[m], None, "alone"))
    return runs


def measure(phase, modules, csv_name, cycles_list):
    path = os.path.join(BUILD, f"bench_runtime.{csv_name}.csv")
    new = not os.path.isfile(path)
    with open(path, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for m in modules:
            variants = OBSCOUNT if m == "obscountdb" else [("", {})]
            for variant, vset in variants:
                for sel_name, sel in (SELECTIONS if phase == 2 else SELECTIONS[:1]):
                    settings = {**BASE, **sel, **vset}
                    if m == "obscountdb":
                        settings["FAMILY"] = "@postalt"      # always every family
                    for wrapper, match, run in runs_of(m):
                        for n in cycles_list:
                            tag = re.sub(r"[^\w.-]+", "_",
                                         f"p{phase}_{m}_{variant}_{run}_{sel_name}_{n}")
                            print(f"[runtime] phase {phase} {m:12s} {variant:13s} {run:7s} "
                                  f"{sel_name} {n:2d} cycle(s) ...", flush=True)
                            r = run_one(wrapper, n, match, settings, tag)
                            r.update(phase=phase, module=m, variant=variant, run=run,
                                     selection=sel_name, cycles=n)
                            w.writerow(r)
                            fh.flush()
                            print(f"[runtime]   {r['wall_s']:.0f} s (rc {r['rc']}), extract "
                                  f"{r['extract_s']} s, plot {r['plot_s']} s, {r['figures']} figures"
                                  + (f", no {r['skipped']} in the wrapper" if r['skipped'] else ""),
                                  flush=True)


# ─────────────────────────────────────────────────────────────────────────────
# Tables
# ─────────────────────────────────────────────────────────────────────────────

def duration(sec):
    if sec < 90:
        return f"{sec:.0f} s"
    if sec < 90 * 60:
        return f"{sec / 60:.0f} min"
    return f"{sec / 3600:.1f} h"


def fit(points):
    n = len(points)
    sx = sum(x for x, _ in points); sy = sum(y for _, y in points)
    sxx = sum(x * x for x, _ in points); sxy = sum(x * y for x, y in points)
    if n < 2 or n * sxx - sx * sx == 0:
        return None
    b = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    a = (sy - b * sx) / n
    worst = max((abs(a + b * x - y) / y for x, y in points if y), default=0.0)
    return a, b, worst


def rst_table(head, rows, note=None):
    out = [".. list-table::", "   :header-rows: 1", ""]
    for r in [head] + rows:
        out.append(f"   * - {r[0]}")
        out += [f"     - {str(c).replace('*', chr(92) + '*')}" for c in r[1:]]
    if note:
        out += ["", note]
    return "\n".join(out) + "\n"


def show(title, head, rows):
    widths = [max(len(str(r[i])) for r in [head] + rows) for i in range(len(head))]
    print(f"\n{title}")
    for r in [head] + rows:
        print("  " + "  ".join(str(c).ljust(w) for c, w in zip(r, widths)))


def tables():
    rows = []
    for p in sorted(glob.glob(os.path.join(BUILD, "bench_runtime.*.csv"))):
        rows += list(csv.DictReader(open(p)))
    ok = [r for r in rows if r["rc"] == "0" and r["wall_s"]]
    failed = [r for r in rows if r["rc"] != "0"]
    measured = max((int(r["cycles"]) for r in ok if r["phase"] == "1"), default=0)

    def period_rows(sel):
        groups = {}
        for r in ok:
            if r["phase"] == "1" and sel(r):
                groups.setdefault((r["module"], r["variant"], r["run"]), []).append(
                    (int(r["cycles"]), float(r["wall_s"])))
        out = []
        for (m, v, run), pts in sorted(groups.items(),
                                       key=lambda kv: (kv[0][0], kv[0][1], RUN_ORDER.get(kv[0][2], 9))):
            longer = [p for p in pts if p[0] > 1]
            f = fit(sorted(longer if len(longer) >= 2 else pts))
            if not f:
                continue
            a, b, worst = f
            cells = [duration(max(a + b * n, 0)) + ("*" if n > measured else "") for _, n in PERIODS]
            out.append((max(a + b * PERIODS[-1][1], 0),
                        [m if not v else f"{m}, {v}", run, duration(max(a, 0)), f"{b:.1f} s"]
                        + cells + [f"{worst:.0%}"]))
        # the slowest first, by the longest period
        return [row for _, row in sorted(out, key=lambda t: -t[0])]

    head = ["Module", "Run", "Fixed", "Per 6-h cycle"] + [p for p, _ in PERIODS] + ["Fit error"]
    note = (f"\\* beyond the {measured} six-hour cycles measured: the straight line "
            "carried on, not a measurement.")
    t1 = period_rows(lambda r: r["module"] != "obscountdb")
    t2 = period_rows(lambda r: r["module"] == "obscountdb")
    show("Phase 1 -- iasi, Monde, assimilee: how the time grows with the period", head, t1)
    show("obscountdb -- every postalt family, Monde, assimilee", head, t2)
    open(os.path.join(DOCS, "runtime_time.rst"), "w").write(rst_table(head, t1, note))
    open(os.path.join(DOCS, "runtime_obscountdb.rst"), "w").write(rst_table(head, t2, note))

    sel = {}
    for r in ok:
        if r["phase"] == "2":
            sel[(r["module"], r["variant"], r["run"], r["selection"])] = float(r["wall_s"])
    t3 = []
    keys = sorted({k[:3] for k in sel}, key=lambda k: (k[0], k[1], RUN_ORDER.get(k[2], 9)))
    for m, v, run in keys:
        times = [sel.get((m, v, run, s)) for s, _ in SELECTIONS]
        ratio = (f"x {times[2] / times[0]:.1f}" if times[0] and times[2] else "--")
        t3.append((max([t for t in times if t is not None] or [0]),
                   [m if not v else f"{m}, {v}", run]
                   + [duration(t) if t is not None else "--" for t in times] + [ratio]))
    # the slowest first; obscountdb counts every family whatever the
    # selection, so its growth is told on its own, not in this table
    t3 = [row for _, row in sorted(t3, key=lambda t: -t[0])
          if not row[0].startswith("obscountdb")]
    head3 = ["Module", "Run"] + [s for s, _ in SELECTIONS] + ["3 x 3 x 3 / 1 x 1 x 1"]
    show("Phase 2 -- one day: families x regions x criteria", head3, t3)
    open(os.path.join(DOCS, "runtime_selection_growth.rst"), "w").write(rst_table(
        head3, t3, "One day (four 6-h cycles). Families: iasi, then ua, then ai; regions: "
                   "Monde, then HemisphereNord, then Tropiques; criteria: assimilee, then "
                   "rejets_qc, then all. obscountdb always reads every family."))
    if failed:
        print(f"\n{len(failed)} run(s) failed, left out of the tables:")
        for r in failed:
            print(f"  phase {r['phase']} {r['module']} {r['variant']} {r['run']} "
                  f"{r['selection']} {r['cycles']} cycle(s): rc {r['rc']}")
    notes = sorted({(r["module"], r["skipped"]) for r in rows if r.get("skipped")})
    for m, s in notes:
        print(f"  {m}: no {s} in its wrapper, measured without it")
    print(f"\nRST written: runtime_time.rst, runtime_obscountdb.rst, runtime_selection_growth.rst")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=("phase1", "phase2", "tables"))
    ap.add_argument("modules", nargs="*")
    ap.add_argument("--csv", default="all", help="name of this job's CSV (bench_runtime.<name>.csv)")
    ap.add_argument("--cycles", nargs="+", type=int)
    args = ap.parse_args()
    if args.what == "tables":
        tables()
        return
    modules = args.modules or MODULES
    unknown = [m for m in modules if m not in WRAPPERS]
    if unknown:
        sys.exit(f"[runtime] unknown module(s): {' '.join(unknown)}")
    if args.what == "phase1":
        measure(1, modules, args.csv, args.cycles or [1, 8, 16, 28])
    else:
        measure(2, modules, args.csv, args.cycles or [4])


if __name__ == "__main__":
    main()
