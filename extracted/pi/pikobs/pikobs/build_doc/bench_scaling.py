#!/usr/bin/env python
"""How the run time grows with the input, module by module.

Every module runs its comparison wrapper as it is downloaded -- G0 against
G2, its default families, regions and figures -- and only three settings
change: the period (1, 4, 8 and 16 six-hour cycles, every period ending
on the same cycle), MATCH (on: pairs; off: every observation of each run) and
the output folder, wiped after each run. Modules without MATCH run once
per number of files.

For every run it keeps the wall time and what the module logs: extraction
time, plotting time, figures, input files and GB. The rows go to
bench_scaling.csv; at the end, per module and MATCH, a straight line
fits time = fixed + per_file * N.

Run it on a compute node, 80 CPUs and 185 GB (a PBS job: see
bench_scaling.pbs). It takes hours.

    python pikobs/build_doc/bench_scaling.py                     # every module
    python pikobs/build_doc/bench_scaling.py zone scatter        # some
    python pikobs/build_doc/bench_scaling.py --files 1 2 --summary-only
"""
import argparse
import csv
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SCRIPTS = os.path.join(REPO, "pikobs", "script")
OUT_CSV = os.path.join(REPO, "pikobs", "build_doc", "bench_scaling.csv")
WORK = os.path.expanduser("~/sites8/pikobs_bench")

WRAPPERS = {                       # the comparison wrapper of each module
    "cardio": "run_cardio_cont_exp.sh",
    "histogram": "run_histogram_cont_exp.sh",
    "profile": "run_profile_cont_exp.sh",
    "scatter": "run_scatter_cont_exp.sh",
    "timeserie": "run_timeserie_cont_exp.sh",
    "verifprofile": "run_verifprofile_cont_exp.sh",
    "zone": "run_zone_cont_exp.sh",
    "vdedr": "run_vdedr_cont_exp.sh",
    "mapobs": "run_mapobs.sh",
    "obscountdb": "run_obscountdb_cont_exp.sh",
    "flags": "run_flags.sh",
}

RX = {
    "extract_s": re.compile(r"(?:extraction|scan|aggregation|matching|compaction) time:\s*([\d.]+)\s*s"),
    "plot_s": re.compile(r"(?:plot|figure) time:\s*([\d.]+)\s*s"),
    "figures": re.compile(r"(?:\bplots?:\s*(?=\d+\s*tasks)|figure time:[^(\n]*\()(\d+)"),
    "files": re.compile(r"input check OK:.*?(\d+)\s*files"),
    "input_gb": re.compile(r"input check OK:.*?([\d.]+)\s*(GB|MB)"),
}
PERIODS = [("1 day", 4), ("1 week", 28), ("1 month", 124), ("2 months", 244)]
RST = os.path.join(REPO, "docs", "source", "runtime_estimates.rst")
RST_SELECTION = os.path.join(REPO, "docs", "source", "runtime_selection.rst")
RST_FAMILIES = os.path.join(REPO, "docs", "source", "runtime_family_sizes.rst")
POSTALT = os.environ.get("PIKOBS_BENCH_POSTALT", os.path.expanduser(
    "~smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"))


def parse_log(text):
    """What a module logs about its run: times, figures, input."""
    row = {}
    for k, rx in RX.items():
        vals = rx.findall(text)
        if k in ("extract_s", "plot_s"):
            row[k] = round(sum(float(v) for v in vals), 1) if vals else ""
        elif k == "figures":
            row[k] = sum(int(v) for v in vals) if vals else ""
        elif k == "input_gb":
            row[k] = (round(float(vals[0][0]) / (1000 if vals[0][1] == "MB" else 1), 3)
                      if vals else "")
        else:
            row[k] = vals[0] if vals else ""
    return row


def set_value(text, var, value):
    """VAR=... at the start of a line becomes VAR=value (the first one)."""
    new, n = re.subn(rf"(?m)^{var}=.*$", f"{var}={value}", text, count=1)
    return new, n == 1


def last_cycle():
    """18 UTC three days ago: every period ends there, and grows backwards,
    so the longest one still lies in what both suites keep."""
    d = dt.datetime.utcnow().date() - dt.timedelta(days=3)
    return dt.datetime(d.year, d.month, d.day, 18)


def run_one(module, wrapper, n_files, match, end, log_dir, extra=None, tag=None):
    start = end - dt.timedelta(hours=6 * (n_files - 1))
    tag = tag or f"{module}_{match or 'nomatch'}_{n_files}"
    pathwork = os.path.join(WORK, tag)
    src = open(os.path.join(SCRIPTS, wrapper)).read()
    for var, val in (("DATESTART", f'"{start:%Y%m%d%H}"'), ("DATEEND", f'"{end:%Y%m%d%H}"'),
                     ("PATHWORK", f'"{pathwork}"'), ("N_CPUS", "80")):
        src, ok = set_value(src, var, val)
        if not ok and var != "N_CPUS":
            raise RuntimeError(f"{wrapper}: no {var}= line")
    if match:
        src, _ = set_value(src, "MATCH", f'"{match}"')
    for var, val in (extra or {}).items():
        src, ok = set_value(src, var, val)
        if not ok:
            raise RuntimeError(f"{wrapper}: no {var}= line")
    copy = os.path.join(log_dir, f"{tag}.sh")
    open(copy, "w").write(src)
    log = os.path.join(log_dir, f"{tag}.log")
    t0 = time.time()
    with open(log, "w") as fh:
        rc = subprocess.call(["bash", copy], stdout=fh, stderr=subprocess.STDOUT, cwd=log_dir)
    wall = time.time() - t0
    text = open(log, errors="replace").read()
    row = {"module": module, "match": match or "-", "n_files": n_files,
           "first_cycle": f"{start:%Y%m%d%H}", "wall_s": round(wall, 1), "rc": rc}
    row.update(parse_log(text))
    shutil.rmtree(pathwork, ignore_errors=True)
    return row


def fit(points):
    """Least squares time = a + b N; returns (a, b, worst relative misfit)."""
    n = len(points)
    if n < 2:
        return None
    sx = sum(x for x, _ in points); sy = sum(y for _, y in points)
    sxx = sum(x * x for x, _ in points); sxy = sum(x * y for x, y in points)
    if n * sxx - sx * sx == 0:
        return None
    b = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    a = (sy - b * sx) / n
    worst = max((abs(a + b * x - y) / y for x, y in points if y), default=0.0)
    return a, b, worst


def duration(sec):
    if sec < 90:
        return f"{sec:.0f} s"
    if sec < 90 * 60:
        return f"{sec / 60:.0f} min"
    return f"{sec / 3600:.1f} h"


def reparse(path):
    """Fill what the first parsing missed, from the logs of every run."""
    rows = list(csv.DictReader(open(path)))
    log_dir = os.path.join(WORK, "logs")
    for r in rows:
        tag = f"{r['module']}_{'nomatch' if r['match'] == '-' else r['match']}_{r['n_files']}"
        log = os.path.join(log_dir, f"{tag}.log")
        if os.path.isfile(log):
            for k, v in parse_log(open(log, errors="replace").read()).items():
                if v != "":
                    r[k] = v
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"[bench] {len(rows)} rows re-read from their logs")


def estimates(path, rst=None):
    """Fixed cost, cost per cycle, and the time of usual periods."""
    rows = list(csv.DictReader(open(path)))
    groups = {}
    for r in rows:
        if r["rc"] == "0" and r["wall_s"]:
            groups.setdefault((r["module"], r["match"]), []).append(
                (int(r["n_files"]), float(r["wall_s"])))
    measured = max((n for pts in groups.values() for n, _ in pts), default=0)
    pairs = {"on": "with", "off": "without", "-": "--"}
    table = []
    for (m, match), pts in sorted(groups.items()):
        # the 1-cycle run comes first in its series and pays the warm-up;
        # the line is fitted on the longer ones when there are two of them
        longer = [p for p in pts if p[0] > 1]
        f = fit(sorted(longer if len(longer) >= 2 else pts))
        if not f:
            continue
        a, b, worst = f
        cells = []
        for _, n in PERIODS:
            t = duration(max(a + b * n, 0))
            cells.append(t + ("*" if n > measured else ""))
        table.append([m, pairs.get(match, match), duration(max(a, 0)), f"{b:.1f} s"] + cells
                     + [f"{worst:.0%}"])
    head = ["Module", "Pairs", "Fixed", "Per 6-h cycle"] + [p for p, _ in PERIODS] + ["Fit error"]
    widths = [max(len(str(r[i])) for r in [head] + table) for i in range(len(head))]
    print()
    for r in [head] + table:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths)))
    print(f"\n* beyond the {measured} cycles measured: a straight line carried on")
    if rst:
        out = [".. list-table::", "   :header-rows: 1", ""]
        for r in [head] + table:
            out.append(f"   * - {r[0]}")
            out += [f"     - {str(c).replace('*', chr(92) + '*')}" for c in r[1:]]
        out += ["", f"\\* Beyond the {measured} six-hour cycles measured: the straight "
                "line carried on, not a measurement.", ""]
        open(rst, "w").write("\n".join(out))
        print(f"[bench] RST table written: {rst}")


def rst_table(head, table, note=None):
    out = [".. list-table::", "   :header-rows: 1", ""]
    for r in [head] + table:
        out.append(f"   * - {r[0]}")
        out += [f"     - {str(c).replace('*', chr(92) + '*')}" for c in r[1:]]
    if note:
        out += ["", note]
    return "\n".join(out) + "\n"


def print_table(head, table):
    widths = [max(len(str(r[i])) for r in [head] + table) for i in range(len(head))]
    print()
    for r in [head] + table:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths)))


def wrapper_counts(module):
    """How many regions, criteria and families the wrapper asks for."""
    text = open(os.path.join(SCRIPTS, WRAPPERS[module])).read()
    out = {}
    for var in ("REGION", "FLAGS_CRITERIA", "FAMILY"):
        m = re.search(rf"(?m)^{var}=\(([^)]*)\)", text)
        out[var] = len(m.group(1).split()) if m else None
    return out


def selection(path, rst=None):
    """What one more region, criterion or GB costs, module by module."""
    rows = [r for r in csv.DictReader(open(path)) if r["rc"] == "0"]
    groups = {}
    for r in rows:
        groups.setdefault((r["module"], r["match"]), []).append(r)
    pairs = {"on": "with", "off": "without", "-": "--"}
    table = []
    for (m, match), rs in sorted(groups.items()):
        per_fig = sorted(float(r["plot_s"]) / int(r["figures"]) for r in rs
                         if r["plot_s"] and r["figures"] and int(r["figures"]) > 0)
        s_fig = per_fig[len(per_fig) // 2] if per_fig else None
        big = max(rs, key=lambda r: int(r["n_files"]))
        figs = int(big["figures"]) if big["figures"] else None
        c = wrapper_counts(m) if m in WRAPPERS else {}
        reg, cri, fam = c.get("REGION"), c.get("FLAGS_CRITERIA"), c.get("FAMILY")
        combos = (reg or 1) * (cri or 1)
        per_combo = figs / combos if figs else None
        pts = [(float(r["input_gb"]), float(r["extract_s"])) for r in rs
               if r["input_gb"] and r["extract_s"]]
        f = fit(sorted(pts)) if len(pts) > 1 else None
        words = (("region", "regions"), ("criterion", "criteria"), ("family", "families"))
        default = " x ".join(f"{n} {w[0] if n == 1 else w[1]}"
                             for n, w in zip((reg, cri, fam), words) if n)
        table.append([m, pairs.get(match, match),
                      f"{s_fig:.2f} s" if s_fig is not None else "--",
                      str(figs) if figs else "--",
                      default or "--",
                      f"{per_combo:.0f}" if per_combo else "--",
                      f"{f[1]:.2f} s" if f else "--"])
    head = ["Module", "Pairs", "Per figure", "Figures (default)", "Default selection",
            "Figures per region and criterion", "Extraction per GB"]
    print_table(head, table)
    if rst:
        open(rst, "w").write(rst_table(head, table))
        print(f"[bench] RST table written: {rst}")


def family_sizes(rst=None, n_cycles=8):
    """GB per 6-h cycle of every postalt family: what a family more costs to read."""
    if not os.path.isdir(POSTALT):
        print(f"[bench] {POSTALT} not reachable -- no family sizes")
        return
    cycles = sorted({f[:10] for f in os.listdir(POSTALT) if re.match(r"\d{10}_", f)})
    cycles = cycles[-(n_cycles + 1):-1]            # the last one may be incomplete
    sizes = {}
    for f in os.listdir(POSTALT):
        if f[:10] in cycles:
            sizes.setdefault(f[11:], []).append(os.path.getsize(os.path.join(POSTALT, f)) / 1e9)
    table = []
    for fam, v in sorted(sizes.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
        gb = sum(v) / len(v)
        table.append([fam, f"{gb:.3f}" if gb < 0.1 else f"{gb:.2f}",
                      f"{4 * gb:.2f}" if gb < 0.1 else f"{4 * gb:.1f}", f"{124 * gb:.0f}"])
    head = ["Family", "GB per 6-h cycle", "GB per day", "GB per month"]
    print_table(head, table)
    print(f"\n  mean of {len(cycles)} cycles of {POSTALT}")
    if rst:
        open(rst, "w").write(rst_table(head, table,
            f"The mean of {len(cycles)} cycles of the G2 ``postalt`` files, one run."))
        print(f"[bench] RST table written: {rst}")


FAMILY_MODULES = ["zone", "scatter", "cardio", "timeserie", "histogram",
                  "profile", "vdedr", "verifprofile"]
FAMILY_CSV = os.path.join(REPO, "pikobs", "build_doc", "bench_families.csv")
RST_BY_FAMILY = os.path.join(REPO, "docs", "source", "runtime_by_family.rst")


def postalt_families():
    """The families of the last complete cycle of postalt, empty files left out."""
    cycles = sorted({f[:10] for f in os.listdir(POSTALT) if re.match(r"\d{10}_", f)})
    cycle = cycles[-2]
    return sorted(f[11:] for f in os.listdir(POSTALT)
                  if f.startswith(cycle + "_") and os.path.getsize(os.path.join(POSTALT, f)) > 0)


def by_family(modules, families, cycles):
    """Each module, one family at a time, the same day, with pairs."""
    end = last_cycle()
    log_dir = os.path.join(WORK, "logs")
    os.makedirs(log_dir, exist_ok=True)
    fields = ["module", "family", "n_files", "wall_s", "rc", "extract_s", "plot_s",
              "figures", "files", "input_gb"]
    new_file = not os.path.isfile(FAMILY_CSV)
    with open(FAMILY_CSV, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        if new_file:
            w.writeheader()
        for m in modules:
            wrapper = WRAPPERS[m]
            has_match = re.search(r"(?m)^MATCH=", open(os.path.join(SCRIPTS, wrapper)).read())
            for fam in families:
                print(f"[bench] {m:12s} family={fam} ...", flush=True)
                row = run_one(m, wrapper, cycles, "on" if has_match else None, end, log_dir,
                              extra={"FAMILY": f"({fam})"}, tag=f"{m}_family_{fam}")
                out = {k: row.get(k, "") for k in fields}
                out["family"] = fam
                w.writerow(out)
                fh.flush()
                print(f"[bench]   {row['wall_s']:.0f} s (rc {row['rc']}), "
                      f"{row['figures']} figures, {row['input_gb']} GB", flush=True)


def family_table(rst=None):
    """Module x family: the time of one day, and the figures, or -- if refused."""
    rows = list(csv.DictReader(open(FAMILY_CSV)))
    modules = [m for m in FAMILY_MODULES if any(r["module"] == m for r in rows)]
    fams = sorted({r["family"] for r in rows})
    cell = {}
    for r in rows:
        if r["rc"] == "0" and r["wall_s"]:
            figs = f", {r['figures']} fig." if r["figures"] else ""
            cell[(r["family"], r["module"])] = f"{duration(float(r['wall_s']))}{figs}"
        else:
            cell[(r["family"], r["module"])] = "--"
    head = ["Family"] + modules
    table = [[f] + [cell.get((f, m), "") for m in modules] for f in fams]
    print_table(head, table)
    print("\n  one day (4 cycles), with pairs; -- : the module does not take that family")
    if rst:
        open(rst, "w").write(rst_table(head, table,
            "One day (four 6-h cycles) of G2 against G0, with pairs, one family at a "
            "time; ``--`` where the module does not take that family."))
        print(f"[bench] RST table written: {rst}")


CHECK_CSV = os.path.join(REPO, "pikobs", "build_doc", "bench_checks.csv")


def _median(v):
    v = sorted(v)
    return v[len(v) // 2] if v else None


def _family_gb():
    """GB per 6-h cycle of each postalt family (mean of 8 cycles)."""
    cycles = sorted({f[:10] for f in os.listdir(POSTALT) if re.match(r"\d{10}_", f)})[-9:-1]
    sizes = {}
    for f in os.listdir(POSTALT):
        if f[:10] in cycles:
            sizes.setdefault(f[11:], []).append(os.path.getsize(os.path.join(POSTALT, f)) / 1e9)
    return {k: sum(v) / len(v) for k, v in sizes.items()}


def model(module, match):
    """fixed, extraction constant, s per GB, s per figure -- from the runs."""
    rows = [r for r in csv.DictReader(open(OUT_CSV))
            if r["module"] == module and r["match"] == match and r["rc"] == "0"
            and int(r["n_files"]) > 1]
    if not rows:
        sys.exit(f"[predict] no measured run of {module} with match={match}")
    core = _median([float(r["wall_s"]) - float(r["extract_s"] or 0) - float(r["plot_s"] or 0)
                    for r in rows])
    pts = [(float(r["input_gb"]), float(r["extract_s"])) for r in rows
           if r["input_gb"] and r["extract_s"]]
    f = fit(sorted(pts)) if len(pts) > 1 else None
    e0, per_gb = (max(f[0], 0), max(f[1], 0)) if f else (_median([p[1] for p in pts]) or 0, 0)
    per_fig = _median([float(r["plot_s"]) / int(r["figures"]) for r in rows
                       if r["plot_s"] and r["figures"] and int(r["figures"]) > 0]) or 0
    return core, e0, per_gb, per_fig


def figures_per_rc(module, family, match):
    """Figures of one region and one criterion for one family."""
    c = wrapper_counts(module)
    rc = (c.get("REGION") or 1) * (c.get("FLAGS_CRITERIA") or 1)
    if os.path.isfile(FAMILY_CSV):
        for r in csv.DictReader(open(FAMILY_CSV)):
            if r["module"] == module and r["family"] == family and r["rc"] == "0" and r["figures"]:
                return int(r["figures"]) / rc, "measured"
    rows = [r for r in csv.DictReader(open(OUT_CSV)) if r["module"] == module
            and r["match"] == match and r["rc"] == "0" and r["figures"]]
    if not rows:
        return 0, "unknown"
    big = max(rows, key=lambda r: int(r["n_files"]))
    return int(big["figures"]) / (rc * (c.get("FAMILY") or 1)), "wrapper default"


def predict(module, families, regions, criteria, cycles, pairs, quiet=False):
    match = pairs if re.search(r"(?m)^MATCH=", open(os.path.join(SCRIPTS, WRAPPERS[module])).read()) else "-"
    runs = 2 if "cont_exp" in WRAPPERS[module] else 1
    core, e0, per_gb, per_fig = model(module, match)
    gb_cycle = _family_gb()
    missing = [f for f in families if f not in gb_cycle]
    gb = sum(gb_cycle.get(f, 0) for f in families) * cycles * runs
    figs, how = 0, set()
    for fam in families:
        n, h = figures_per_rc(module, fam, match)
        figs += n * regions * criteria
        how.add(h)
    read = e0 + per_gb * gb
    draw = per_fig * figs
    total = core + read + draw
    if not quiet:
        print(f"\n{module}, {'with' if match == 'on' else 'without' if match == 'off' else 'no'} pairs: "
              f"{' '.join(families)} x {regions} region(s) x {criteria} criterion(a), "
              f"{cycles} cycles, {runs} run(s)")
        print(f"  fixed    {duration(core):>8}")
        print(f"  reading  {duration(read):>8}   {gb:.1f} GB at {per_gb:.2f} s/GB + {e0:.0f} s")
        print(f"  drawing  {duration(draw):>8}   {figs:.0f} figures at {per_fig:.3f} s "
              f"(figures per family: {', '.join(sorted(how))})")
        print(f"  total    {duration(total):>8}")
        if missing:
            print(f"  no size for {' '.join(missing)} in {POSTALT}: counted as 0 GB")
        if cycles > 28:
            print("  beyond the 28 cycles measured: a straight line carried on")
    return {"fixed": core, "reading": read, "drawing": draw, "total": total, "gb": gb,
            "figures": figs}


def check(module, families, regions, criteria, cycles, pairs, region_names, criteria_names):
    """Run the selection for real and set it beside the prediction."""
    text = open(os.path.join(SCRIPTS, WRAPPERS[module])).read()
    def names(var, given, n):
        pool = given or (re.search(rf"(?m)^{var}=\(([^)]*)\)", text) or [None, ""])[1].split()
        if len(pool) < n:
            sys.exit(f"[check] {n} {var} asked, {len(pool)} known: give them with "
                     f"--{'region' if var == 'REGION' else 'criteria'}-names")
        return pool[:n]
    reg = names("REGION", region_names, regions)
    cri = names("FLAGS_CRITERIA", criteria_names, criteria)
    guess = predict(module, families, regions, criteria, cycles, pairs)
    has_match = re.search(r"(?m)^MATCH=", text)
    log_dir = os.path.join(WORK, "logs")
    os.makedirs(log_dir, exist_ok=True)
    tag = f"check_{module}_{'-'.join(families)}_{regions}r{criteria}c_{cycles}"
    row = run_one(module, WRAPPERS[module], cycles, pairs if has_match else None, last_cycle(),
                  log_dir, tag=tag, extra={"FAMILY": f"({' '.join(families)})",
                                           "REGION": f"({' '.join(reg)})",
                                           "FLAGS_CRITERIA": f"({' '.join(cri)})"})
    if row["rc"] != 0:
        sys.exit(f"[check] the run failed (rc {row['rc']}): {os.path.join(log_dir, tag + '.log')}")
    ext, plot = float(row["extract_s"] or 0), float(row["plot_s"] or 0)
    measured = {"fixed": row["wall_s"] - ext - plot, "reading": ext, "drawing": plot,
                "total": row["wall_s"]}
    print(f"\n  {'':8s} {'predicted':>10s} {'measured':>10s}")
    for k in ("fixed", "reading", "drawing", "total"):
        print(f"  {k:8s} {duration(guess[k]):>10s} {duration(measured[k]):>10s}")
    print(f"  figures  {guess['figures']:>10.0f} {row['figures'] or '-':>10}")
    print(f"  GB       {guess['gb']:>10.1f} {row['input_gb'] or '-':>10}")
    new = not os.path.isfile(CHECK_CSV)
    with open(CHECK_CSV, "a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["module", "families", "regions", "criteria", "cycles", "pairs",
                        "predicted_s", "measured_s", "pred_read", "meas_read",
                        "pred_draw", "meas_draw", "figures", "gb"])
        w.writerow([module, " ".join(families), regions, criteria, cycles, pairs,
                    round(guess["total"], 1), row["wall_s"], round(guess["reading"], 1), ext,
                    round(guess["drawing"], 1), plot, row["figures"], row["input_gb"]])


def summary(path):
    rows = list(csv.DictReader(open(path)))
    groups = {}
    for r in rows:
        if r["rc"] != "0" or not r["wall_s"]:
            continue
        groups.setdefault((r["module"], r["match"]), []).append(
            (int(r["n_files"]), float(r["wall_s"])))
    sizes = sorted({n for pts in groups.values() for n, _ in pts})
    print(f"\n{'module':13s} {'match':6s} " + " ".join(f"{k:>7d}" for k in sizes)
          + f" {'fixed':>8s} {'per cycle':>10s} {'misfit':>7s}")
    for (m, match), pts in sorted(groups.items()):
        by_n = dict(pts)
        cells = " ".join(f"{by_n[k]:7.0f}" if k in by_n else f"{'-':>7s}" for k in sizes)
        f = fit(sorted(pts))
        tail = f"{f[0]:8.0f} {f[1]:10.1f} {f[2]:6.0%}" if f else ""
        print(f"{m:13s} {match:6s} {cells} {tail}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modules", nargs="*", help="default: every module")
    ap.add_argument("--files", nargs="+", type=int, default=[1, 4, 8, 16],
                    help="numbers of 6-h cycles (default 1 4 8 16)")
    ap.add_argument("--summary-only", action="store_true")
    ap.add_argument("--variant", metavar="NAME",
                    help="save the rows as module:NAME (with --set)")
    ap.add_argument("--set", nargs="+", default=[], metavar="VAR=VALUE",
                    help="settings to change; FAMILY=@postalt: every postalt family")
    ap.add_argument("--predict", metavar="MODULE", help="the time of a selection, from the measurements")
    ap.add_argument("--check", metavar="MODULE", help="run a selection and compare with the prediction")
    ap.add_argument("--families", nargs="+", default=[])
    ap.add_argument("--regions", type=int, default=1)
    ap.add_argument("--criteria", type=int, default=1)
    ap.add_argument("--cycles", type=int, default=4)
    ap.add_argument("--pairs", choices=("on", "off"), default="on")
    ap.add_argument("--region-names", nargs="+")
    ap.add_argument("--criteria-names", nargs="+")
    ap.add_argument("--by-family", action="store_true",
                    help="each module, one postalt family at a time, one day")
    ap.add_argument("--family-table", action="store_true",
                    help="the module x family table of --by-family (and its RST)")
    ap.add_argument("--estimates", action="store_true",
                    help="re-read the logs, then the table of usual periods (and its RST)")
    args = ap.parse_args()
    if args.summary_only:
        summary(OUT_CSV)
        return
    if args.predict or args.check:
        m = args.predict or args.check
        if m not in WRAPPERS:
            sys.exit(f"[predict] unknown module {m}")
        fams = args.families or (re.search(r"(?m)^FAMILY=\(([^)]*)\)",
                                           open(os.path.join(SCRIPTS, WRAPPERS[m])).read())
                                 or [None, ""])[1].split()
        if args.check:
            check(m, fams, args.regions, args.criteria, args.cycles, args.pairs,
                  args.region_names, args.criteria_names)
        else:
            predict(m, fams, args.regions, args.criteria, args.cycles, args.pairs)
        return
    if args.family_table:
        family_table(RST_BY_FAMILY)
        return
    if args.by_family:
        modules = args.modules or FAMILY_MODULES
        unknown = [m for m in modules if m not in WRAPPERS]
        if unknown:
            sys.exit(f"[bench] unknown module(s): {' '.join(unknown)}")
        by_family(modules, postalt_families(), 4)
        family_table(RST_BY_FAMILY)
        return
    if args.estimates:
        reparse(OUT_CSV)
        estimates(OUT_CSV, RST)
        selection(OUT_CSV, RST_SELECTION)
        family_sizes(RST_FAMILIES)
        return
    modules = args.modules or list(WRAPPERS)
    unknown = [m for m in modules if m not in WRAPPERS]
    if unknown:
        sys.exit(f"[bench] unknown module(s): {' '.join(unknown)}")
    end = last_cycle()
    log_dir = os.path.join(WORK, "logs")
    os.makedirs(log_dir, exist_ok=True)
    extra = {}
    for item in args.set:
        var, _, val = item.partition("=")
        if val == "@postalt":
            val = "(" + " ".join(postalt_families()) + ")"
        extra[var] = val
    if extra and not args.variant:
        sys.exit("[bench] --set needs --variant NAME, to keep those rows apart")
    if extra:
        print(f"[bench] variant {args.variant}: " + " ".join(f"{k}={v}" for k, v in extra.items()))
    fields = ["module", "match", "n_files", "first_cycle", "wall_s", "rc",
              "extract_s", "plot_s", "figures", "files", "input_gb"]
    new_file = not os.path.isfile(OUT_CSV)
    with open(OUT_CSV, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        if new_file:
            w.writeheader()
        for m in modules:
            wrapper = WRAPPERS[m]
            has_match = re.search(r"(?m)^MATCH=", open(os.path.join(SCRIPTS, wrapper)).read())
            for match in (("on", "off") if has_match else (None,)):
                for n in args.files:
                    print(f"[bench] {m + (':' + args.variant if args.variant else ''):12s} match={match or '-':3s} files={n} ...", flush=True)
                    label = f"{m}:{args.variant}" if args.variant else m
                    row = run_one(m, wrapper, n, match, end, log_dir, extra=extra,
                                  tag=f"{label}_{match or 'nomatch'}_{n}")
                    row["module"] = label
                    w.writerow(row)
                    fh.flush()
                    print(f"[bench]   {row['wall_s']:.0f} s (rc {row['rc']}), "
                          f"extract {row['extract_s']} s, plot {row['plot_s']} s, "
                          f"{row['figures']} figures, {row['input_gb']} GB", flush=True)
    summary(OUT_CSV)


if __name__ == "__main__":
    main()
