#!/usr/bin/env python
"""Check every Pikobs module against the shared conventions.

Two levels:

  static (seconds, login node is fine)
    - every module imports;
    - every wrapper has LAND_OCEAN=(all) and SPECIAL_COLUMN="off" and passes
      --land_ocean and --special_column to its module;
    - the argparse of every module has the same defaults;
    - nothing calls a function retired from special_family.py;
    - is_land_array gives what is_land_sql gives, on the real mask.

  runs (a compute node, one session): two small runs of each module on sw
  through mod_run.py (next to this file) -- the defaults, and every surface
  with the special column on -- then, on the names of the figures:
    - both runs end well, and a viewer is written;
    - by default no name carries a surface or a special value;
    - split, the names carry land, ocean and the labels (IR_channel ...),
      always as ..._<region>[_<surface>][_<special>]_..., never in an old
      form (_sp1, WIND_COMP_METHOD);
    - every _land / _ocean figure has its sister without a surface (all).

Usage (from the repository root):
    python pikobs/build_doc/check_modules.py --static        # seconds, login node
    python pikobs/build_doc/check_modules.py --submit        # everything, as a PBS job
    python pikobs/build_doc/check_modules.py                 # everything, on a compute node
    python pikobs/build_doc/check_modules.py --reuse         # check the last runs again
    python pikobs/build_doc/check_modules.py --modules zone histogram
    python pikobs/build_doc/check_modules.py --scenario multi --submit   # ro sw iasi, layers, channels

--submit writes the job script itself and sends it with qsub; the checks
write their log as they go (--log, ~/sites8/check_modules.log by default),
so tail -f follows them from the moment the job runs.
"""
import argparse
import glob
import importlib
import os
import re
import subprocess
import sys
import tempfile
import time

MODULES = ["cardio", "vdedr", "flags", "scatter", "timeserie", "zone",
           "histogram", "verifprofile", "profile", "mapobs"]
FAMILY = "sw"
REGIONS = {"mapobs": ["cyl"]}                     # mod_run: Monde Tropiques
EXTRA = {"mapobs": ["REGION=(cyl)", "PANELS=(map stations)", "INTERVAL_MIN=60"],
         # zone: all, every level on its row, and channel 32 of IASI;
         # join is dropped by zone, a section needs its levels
         "zone": ["CHANNEL=(all 32)", "FONCTION=(omp oma)",
                  'SPECIAL_COLUMN="on"'],
         # histogram: all is one histogram per layer (per channel on iasi),
         # join every level together
         "histogram": ["CHANNEL=(join all)", "FONCTION=(omp oma omp_std)"]}
SPLIT = ["LAND_OCEAN=(all land ocean)", 'SPECIAL_COLUMN="on"']
# the second scenario, --scenario multi: several families at once, with
# layers and channels. A setting goes only to a module whose wrapper has it.
MULTI_FAMILIES = ["ro", "sw", "iasi"]
MULTI_SETS = {
    "PRESSURE_LAYERS": "(1100 850 500 250 100 10 1 0)",   # hPa: sw
    "HEIGHT_LAYERS": "(0 5 10 20 30 40 60 100)",          # km:  ro
    "CHANNEL": "(join 32 33)",                            # iasi
    "PROJECTION": "(cyl robinson npolar canada)",         # flat, curved, polar, window
    "REGION": "(Monde Tropiques hrdps Boreal_CLIM)",      # two boxes, two polygons
}
RETIRED = ("has_special_col", "get_special_col_values", "special_col_sql_type",
           "iter_special_values", "special_sql_filter", "special_filename_tag",
           "special_title_tag")
SURFACES = ("land", "ocean")


class Report:
    def __init__(self):
        self.rows = []

    def add(self, where, ok, what):
        self.rows.append((where, ok, what))
        print(f"  {'ok  ' if ok else 'FAIL'}  {where:<14s} {what}", flush=True)

    def failures(self):
        return [r for r in self.rows if not r[1]]


def _safe(text):
    return re.sub(r"[^A-Za-z0-9._+-]", "_", str(text))


def wrappers(module):
    """The distributed wrappers of a module (not the operational variants)."""
    names = [f"run_{module}_cont_exp.sh", f"run_{module}_exp.sh", f"run_{module}.sh"]
    return [p for p in (os.path.join("pikobs/script", n) for n in names)
            if os.path.isfile(p)]


# ─────────────────────────────────────────────────────────────────────────────
# Static
# ─────────────────────────────────────────────────────────────────────────────

def check_static(modules, rep):
    print("static:", flush=True)
    for m in modules:
        for name in (f"pikobs.{m}.{m}", f"pikobs.{m}.{m}_plot"):
            if name.endswith("_plot") and not os.path.isfile(name.replace(".", "/") + ".py"):
                continue
            try:
                importlib.import_module(name)
                rep.add(m, True, f"imports {name.split('.')[-1]}")
            except Exception as exc:
                rep.add(m, False, f"import {name}: {exc}")

        src = open(f"pikobs/{m}/{m}.py", encoding="utf-8").read()
        lo = re.search(r"add_argument\('--land_ocean'[^)]*?default=\['all'\]", src, re.S)
        sp = re.search(r"add_argument\('--special_column',\s*default='off'", src)
        rep.add(m, bool(lo and sp), "argparse defaults: land_ocean all, special_column off"
                if lo and sp else f"argparse defaults: land_ocean {'ok' if lo else 'NOT all'}, "
                f"special_column {'ok' if sp else 'NOT off'}")

        ws = wrappers(m)
        if not ws:
            rep.add(m, False, "no wrapper found")
        for w in ws:
            t = open(w, encoding="utf-8").read()
            probs = []
            if not re.search(r"(?m)^LAND_OCEAN=\(all\)\s*(#.*)?$", t):
                probs.append("LAND_OCEAN not (all)")
            if not re.search(r'(?m)^SPECIAL_COLUMN="off"\s*(#.*)?$', t):
                probs.append('SPECIAL_COLUMN not "off"')
            for opt in ("--land_ocean", "--special_column"):
                if opt not in t:
                    probs.append(f"{opt} not passed")
            if re.search(r'(?m)^\s*echo "Viewer:', t):
                probs.append("prints the viewer link itself (the module does)")
            rep.add(m, not probs, f"{os.path.basename(w)}: " + ("defaults and options"
                                                                if not probs else ", ".join(probs)))

    # the retired special-column API
    pat = re.compile(r"\b(" + "|".join(RETIRED) + r")\b")
    hits = []
    for p in glob.glob("pikobs/**/*.py", recursive=True):
        if "/build_doc/" in p or p.endswith("special_family.py"):
            continue
        found = set(pat.findall(open(p, encoding="utf-8", errors="replace").read()))
        if found:
            hits.append(f"{p}: {sorted(found)}")
    rep.add("special", not hits, "no call to a retired function" if not hits
            else "retired functions still called: " + "; ".join(hits))

    # the land mask: the column version against the row version
    try:
        import numpy as np
        from pikobs.configobs.landmask import is_land_array, is_land_function
        work = tempfile.mkdtemp(prefix="pikobs_check_")
        rng = np.random.default_rng(0)
        lat = rng.uniform(-92, 92, 20000)
        lon = rng.uniform(-185, 185, 20000)
        vec = is_land_array(lat, lon, work)
        f = is_land_function(work)
        bad = sum(int(vec[k]) != f(float(lat[k]), float(lon[k])) for k in range(len(lat)))
        rep.add("landmask", bad == 0, f"is_land_array = is_land_sql on 20000 points"
                if not bad else f"is_land_array differs on {bad} of 20000 points")
    except Exception as exc:
        rep.add("landmask", False, f"could not compare the two masks: {exc}")


# ─────────────────────────────────────────────────────────────────────────────
# Runs
# ─────────────────────────────────────────────────────────────────────────────

def run(mod_run, out_dir, module, tag, extra, rep, wrapper=None):
    args = ([sys.executable, mod_run, module, tag, f"FAMILY=({FAMILY})", "ID_STN=(join)"]
            + extra + ["--out_dir", out_dir]
            + (["--wrapper", wrapper] if wrapper else []))
    t0 = time.time()
    res = subprocess.run(args, capture_output=True, text=True)
    out = (res.stdout or "") + (res.stderr or "")
    m = re.search(r"rc (\d+)", out)
    rc = int(m.group(1)) if m else res.returncode
    rep.add(module, rc == 0, f"run {tag}: rc {rc} ({time.time() - t0:.0f} s)")
    return rc == 0


def figures(path):
    return {os.path.relpath(p, path) for p in glob.glob(f"{path}/**/*.png", recursive=True)}


def labels():
    from pikobs.configobs.special_family import FAMILY_SPECIAL_COL
    return sorted({_safe(v) for v in
                   (FAMILY_SPECIAL_COL.get(FAMILY, {}).get("labels") or {}).values()},
                  key=len, reverse=True)


def parts(name, labs):
    """(surface, label) a file name carries, None when it does not."""
    b = os.path.basename(name)[:-4] + "_"
    surf = next((s for s in SURFACES if f"_{s}_" in b), None)
    lab = next((l for l in labs if f"_{l}_" in b), None)
    return surf, lab


def check_names(module, default_dir, split_dir, rep):
    labs = labels()
    regions = REGIONS.get(module, ["Monde", "Tropiques"])
    d, s = figures(default_dir), figures(split_dir)
    rep.add(module, bool(d) and bool(s), f"figures: {len(d)} by default, {len(s)} split")
    if not d or not s:
        return
    for run_dir in (default_dir, split_dir):
        html = glob.glob(f"{run_dir}/pikobs_*viewer*.html")
        rep.add(module, bool(html), f"viewer in {os.path.basename(run_dir)}"
                if html else f"no viewer in {os.path.basename(run_dir)}")
        log = run_dir + ".log"
        said = (os.path.isfile(log)
                and "Viewer: " in open(log, errors="replace").read())
        rep.add(module, said, f"{os.path.basename(log)} names the viewer"
                if said else f"no 'Viewer:' line in {os.path.basename(log)}")

    marked = [n for n in d if any(parts(n, labs))]
    rep.add(module, not marked, "defaults: no surface or special value in the names"
            if not marked else f"defaults: {len(marked)} names carry one, e.g. {os.path.basename(marked[0])}")

    surf_seen = {parts(n, labs)[0] for n in s} - {None}
    lab_seen = {parts(n, labs)[1] for n in s} - {None}
    rep.add(module, surf_seen == set(SURFACES) and bool(lab_seen),
            f"split: surfaces {sorted(surf_seen) or 'none'}, labels {sorted(lab_seen) or 'none'}")

    old = [n for n in s if re.search(r"_sp\d", os.path.basename(n))
           or "WIND_COMP_METHOD" in n or n.endswith("_all_all.png")]
    rep.add(module, not old, "no name in an old form" if not old
            else f"{len(old)} names in an old form, e.g. {os.path.basename(old[0])}")

    misplaced = []
    for n in s:
        surf, lab = parts(n, labs)
        if not surf and not lab:
            continue
        b = os.path.basename(n)[:-4] + "_"
        want = [f"_{r}" + (f"_{surf}" if surf else "") + (f"_{lab}" if lab else "") + "_"
                for r in regions]
        if not any(w in b for w in want):
            misplaced.append(n)
    rep.add(module, not misplaced, "order ..._<region>[_<surface>][_<special>]_..."
            if not misplaced else f"{len(misplaced)} names out of order, e.g. "
            f"{os.path.basename(misplaced[0])}")

    orphans = []
    for n in s:
        surf, _ = parts(n, labs)
        if surf:
            head, base = os.path.split(n)
            twin = os.path.join(head, base.replace(f"_{surf}", "", 1))
            if twin not in s:
                orphans.append(n)
    rep.add(module, not orphans, "every land/ocean figure has its sister for all"
            if not orphans else f"{len(orphans)} without a sister, e.g. {os.path.basename(orphans[0])}")


JOB = """#!/bin/bash
#PBS -N pikobs_check
#PBS -l select=1:ncpus=80:mem=185gb
#PBS -l walltime={walltime}
#PBS -j oe
#PBS -o {log}.pbs
unset PIKOBS_ENV_PATH PIKOBS_PROJECT_DIR PYTHONPATH
{env}
cd {repo}
# the checks write their log as they go: tail -f works from the start
python -u pikobs/build_doc/check_modules.py {args} > {log} 2>&1
"""


def submit(args):
    """Write the job script and send it; the checks run on the node."""
    import shlex
    load = os.path.expanduser(args.load)
    env = (f"source {shlex.quote(load)}" if os.path.isfile(load) else
           f"export PATH={shlex.quote(os.path.dirname(sys.executable))}:$PATH")
    passed = ["--modules", *args.modules, "--mod_run", args.mod_run,
              "--out_dir", os.path.expanduser(args.out_dir)]
    if args.reuse:
        passed.append("--reuse")
    passed += ["--scenario", args.scenario]
    log = os.path.abspath(os.path.expanduser(args.log))
    os.makedirs(os.path.dirname(log), exist_ok=True)
    for old in (log, log + ".pbs"):
        if os.path.exists(old):
            os.remove(old)             # the log of the last check is not this one
    job = JOB.format(walltime=args.walltime, log=log, env=env,
                     repo=shlex.quote(os.getcwd()),
                     args=" ".join(shlex.quote(a) for a in passed))
    fd, path = tempfile.mkstemp(prefix="pikobs_check_", suffix=".job")
    with os.fdopen(fd, "w") as fh:
        fh.write(job)
    try:
        res = subprocess.run(["qsub", path], capture_output=True, text=True)
    finally:
        os.remove(path)                # qsub keeps its own copy
    if res.returncode != 0:
        sys.exit(f"qsub failed: {(res.stderr or res.stdout).strip()}")
    print(f"submitted: {res.stdout.strip()}")
    print(f"follow it:   qstat -u $USER")
    print(f"watch it:    tail -f {log}   (once the job runs)")
    print(f"the result:  the last lines of the same log; PBS writes its own in {log}.pbs")


def wrapper_of(module):
    """The wrapper mod_run.py runs: _cont_exp, else _exp, else plain."""
    for name in (f"run_{module}_cont_exp.sh", f"run_{module}_exp.sh",
                 f"run_{module}.sh"):
        path = os.path.join("pikobs/script", name)
        if os.path.isfile(path):
            return path
    return None


def multi_sets(module, path=None):
    """(the VAR=VALUE of the multi scenario, the variables applied)."""
    w = path or wrapper_of(module)
    text = open(w, encoding="utf-8").read() if w else ""
    sets = [f"FAMILY=({' '.join(MULTI_FAMILIES)})"]
    applied = []
    own = {e.split("=", 1)[0] for e in EXTRA.get(module, [])}
    for var, val in MULTI_SETS.items():
        if var in own:
            continue                    # the module sets it itself (EXTRA)
        if var == "REGION" and module in REGIONS:
            continue                    # mapobs: a region is a projection
        if re.search(rf"(?m)^{var}=", text):
            sets.append(f"{var}={val}")
            applied.append(var)
    return sets, applied


def check_multi(module, run_dir, applied, rep):
    figs = figures(run_dir)
    by_fam = {}
    for f in figs:
        top = f.split(os.sep)[0]
        for fam in MULTI_FAMILIES:
            if top == fam or top.startswith(fam + "_"):
                by_fam.setdefault(fam, []).append(os.path.basename(f))
    rep.add(module, True, f"multi: settings applied: {', '.join(applied) or 'none'}")
    for fam in MULTI_FAMILIES:
        n = len(by_fam.get(fam, []))
        rep.add(module, n > 0, f"multi: {n} figures for {fam}" if n
                else f"multi: no figure for {fam}")
    html = glob.glob(f"{run_dir}/pikobs_*viewer*.html")
    rep.add(module, bool(html), "multi: viewer written" if html else "multi: no viewer")
    names = [os.path.basename(f) for f in figs]
    old = [n for n in names if re.search(r"_sp\d", n) or "WIND_COMP_METHOD" in n
           or n.endswith("_all_all.png")]
    rep.add(module, not old, "multi: no name in an old form" if not old
            else f"multi: {len(old)} names in an old form, e.g. {old[0]}")
    if "PRESSURE_LAYERS" in applied:
        ok = any("hPa" in n for n in by_fam.get("sw", []))
        rep.add(module, ok, "multi: sw split in hPa layers" if ok
                else "multi: no hPa layer in the sw names")
    if "HEIGHT_LAYERS" in applied:
        ok = any("km" in n for n in by_fam.get("ro", []))
        rep.add(module, ok, "multi: ro split in km layers" if ok
                else "multi: no km layer in the ro names")
    if "CHANNEL" in applied:
        seen = sorted({m.group(1) for n in by_fam.get("iasi", [])
                       for m in [re.search(r"(?:vcoord_?|_ch|lev|channel_)(32|33)(?=[_.])", n)]
                       if m})
        rep.add(module, True, "multi: iasi channels 32/33 in the names: "
                f"{', '.join(seen) or 'none'} (information)")
    for var, what in (("PROJECTION", "projections"), ("REGION", "regions")):
        if var not in applied:
            continue
        wanted = MULTI_SETS[var].strip("()").split()
        missing = [w for w in wanted if not any(f"_{w}_" in n for n in names)]
        rep.add(module, not missing, f"multi: every one of the {what} drawn "
                f"({', '.join(wanted)})" if not missing
                else f"multi: {what} missing from the names: {', '.join(missing)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--static", action="store_true", help="the static checks only")
    ap.add_argument("--reuse", action="store_true",
                    help="check the folders of the last runs, without running again")
    ap.add_argument("--modules", nargs="+", default=MODULES)
    ap.add_argument("--scenario", default="basic", choices=["basic", "multi", "all"],
                    help="basic: sw, defaults and every surface split; multi: ro sw "
                         "iasi with layers and channels; all: both")
    ap.add_argument("--mod_run",
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "mod_run.py"))
    ap.add_argument("--out_dir", default="~/sites8",
                    help="where the runs go, as <module>_chk_default and _chk_split")
    ap.add_argument("--submit", action="store_true",
                    help="send the whole check to PBS as a job of its own")
    ap.add_argument("--log", default="~/sites8/check_modules.log",
                    help="with --submit: where the job writes its result")
    ap.add_argument("--load", default="~/pikobs_install/load_pikobs.sh",
                    help="with --submit: the script that loads the environment")
    ap.add_argument("--walltime", default="2:00:00",
                    help="with --submit: the walltime of the job")
    args = ap.parse_args()
    if not os.path.isdir("pikobs/script"):
        sys.exit("run from the repository root")
    if args.submit:
        submit(args)
        return
    rep = Report()
    check_static(args.modules, rep)
    if not args.static:
        host = os.uname().nodename
        if "login" in host:
            sys.exit(f"the runs need a compute node ({host} is a login node); "
                     f"use --static here")
        print("runs:", flush=True)
        out = os.path.expanduser(args.out_dir)
        for m in args.modules if args.scenario in ("basic", "all") else []:
            dd = os.path.join(out, f"{m}_chk_default")
            sd = os.path.join(out, f"{m}_chk_split")
            if not args.reuse:
                ok1 = run(args.mod_run, args.out_dir, m, "chk_default",
                          EXTRA.get(m, []), rep)
                ok2 = run(args.mod_run, args.out_dir, m, "chk_split",
                          EXTRA.get(m, []) + SPLIT, rep)
                if not (ok1 and ok2):
                    continue
            check_names(m, dd, sd, rep)
        for m in args.modules if args.scenario in ("multi", "all") else []:
            sets, applied = multi_sets(m)
            md = os.path.join(out, f"{m}_chk_multi")
            if args.reuse or run(args.mod_run, args.out_dir, m, "chk_multi",
                                 EXTRA.get(m, []) + sets, rep):
                check_multi(m, md, applied, rep)
            # the same through the _exp wrapper: one experience alone
            exp_w = os.path.join("pikobs/script", f"run_{m}_exp.sh")
            if os.path.isfile(exp_w) and wrapper_of(m) != exp_w:
                sets_e, applied_e = multi_sets(m, exp_w)
                me = os.path.join(out, f"{m}_chk_multi_exp")
                if args.reuse or run(args.mod_run, args.out_dir, m, "chk_multi_exp",
                                     EXTRA.get(m, []) + sets_e, rep, wrapper="exp"):
                    check_multi(f"{m} exp", me, applied_e, rep)
    bad = rep.failures()
    print(f"\n{len(rep.rows)} checks, {len(bad)} failed")
    for where, _, what in bad:
        print(f"  FAIL  {where:<14s} {what}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
