#!/usr/bin/env python
"""A small run of a module's wrapper, for checks and before/after comparisons.

    python pikobs/build_doc/mod_run.py MODULE TAG [VAR=VALUE ...] [--out_dir DIR]

Takes the module's wrapper (run_<module>_cont_exp.sh, else _exp, else
run_<module>.sh), sets one day of data a few days back, PATHWORK to
<out_dir>/<module>_<tag> and REGION to Monde Tropiques, then every VAR=VALUE
given (they win); writes that copy next to its output, <module>_<tag>.sh,
and runs it on this node -- a compute node. Prints

    MODULE TAG: rc N, log <out_dir>/<module>_<tag>.log

and exits with the same code. From the repository root:

    python pikobs/build_doc/mod_run.py zone before 'FAMILY=(sw)' 'ID_STN=(join)'
    python pikobs/build_doc/mod_run.py zone land 'LAND_OCEAN=(all land ocean)'
"""
import argparse
import datetime as dt
import os
import re
import subprocess
import sys


def wrapper(module: str, kind: str = "auto") -> str:
    """The wrapper to run: _cont_exp, else _exp, else plain -- or the
    one asked for with --wrapper."""
    names = {"cont_exp": [f"run_{module}_cont_exp.sh"],
             "exp": [f"run_{module}_exp.sh"],
             "plain": [f"run_{module}.sh"]}
    for name in names.get(kind, [f"run_{module}_cont_exp.sh",
                                 f"run_{module}_exp.sh", f"run_{module}.sh"]):
        path = os.path.join("pikobs/script", name)
        if os.path.isfile(path):
            return path
    sys.exit(f"[mod_run] no wrapper for {module} in pikobs/script")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="A small run of a module's wrapper.")
    ap.add_argument("module")
    ap.add_argument("tag")
    ap.add_argument("sets", nargs="*", metavar="VAR=VALUE",
                    help="wrapper variables to set, e.g. 'FAMILY=(sw)'")
    ap.add_argument("--out_dir", default="~/sites8",
                    help="where <module>_<tag> goes (default ~/sites8)")
    ap.add_argument("--wrapper", default="auto",
                    choices=["auto", "cont_exp", "exp", "plain"],
                    help="which wrapper: auto takes _cont_exp, else _exp, else plain")
    ap.add_argument("--days_back", type=int, default=3,
                    help="the day of data, counted back from today (default 3)")
    a = ap.parse_args()
    if not os.path.isdir("pikobs/script"):
        sys.exit("[mod_run] run from the repository root")

    day = dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=a.days_back)
    out_dir = os.path.expanduser(a.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{a.module}_{a.tag}")
    sets = {"DATESTART": f'"{day - dt.timedelta(days=1):%Y%m%d}06"',
            "DATEEND": f'"{day:%Y%m%d}00"',
            "PATHWORK": f'"{out}"', "REGION": "(Monde Tropiques)"}
    for item in a.sets:
        if "=" not in item:
            sys.exit(f"[mod_run] '{item}' is not VAR=VALUE")
        var, val = item.split("=", 1)
        sets[var] = val

    path = wrapper(a.module, a.wrapper)
    src = open(path, encoding="utf-8").read()
    for var, val in sets.items():
        src, n = re.subn(rf"(?m)^{re.escape(var)}=.*$", lambda _m: f"{var}={val}",
                         src, count=1)
        if n != 1:
            sys.exit(f"[mod_run] {os.path.basename(path)} has no {var}= line")
    with open(out + ".sh", "w", encoding="utf-8") as fh:
        fh.write(src)
    with open(out + ".log", "w") as log:
        rc = subprocess.call(["bash", out + ".sh"], stdout=log,
                             stderr=subprocess.STDOUT,
                             env=dict(os.environ, PBS_O_WORKDIR=""))
    print(f"{a.module} {a.tag}: rc {rc}, log {out}.log", flush=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
