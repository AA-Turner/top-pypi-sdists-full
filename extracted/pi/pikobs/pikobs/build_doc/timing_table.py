#!/usr/bin/env python
"""One table of how fast every module runs, from the timing files they write.

Each module leaves <module>_timing.json in its output directory: the input
volume, the number of files and workers, and the seconds of each phase.
This gathers them into one table and normalises by volume, so modules that
read different families can still be compared: GB per minute of the whole
run, and seconds of extraction per GB.

    python timing_table.py                                  # every pikobs_doc_*
    python timing_table.py /home/$USER/sites8/pikobs_doc_zone ...
    python timing_table.py --csv timing.csv                 # also as CSV

Keep one of these tables: a change that makes a module twice as slow shows
up the next time it is run.
"""
import argparse
import glob
import json
import os
import sys

PHASES = ("extraction", "match", "matching", "indexing", "compaction",
          "aggregation", "plots")


def load(path):
    with open(path) as fh:
        t = json.load(fh)
    module = os.path.basename(path).replace("_timing.json", "")
    d = os.path.basename(os.path.dirname(path))
    mode = "one run" if d.endswith("_exp") else "compare"
    sec = t.get("seconds", {}) or {}
    gb = (t.get("input_bytes") or 0) / 1e9
    files = t.get("input_files") or t.get("n_files") or 0
    cpus = t.get("n_cpus") or t.get("n_cpu") or t.get("workers") or 0
    total = sec.get("total") or sum(v for k, v in sec.items()
                                    if isinstance(v, (int, float)))
    row = dict(module=module, mode=mode, gb=gb, files=files, cpus=cpus,
               total=total, dir=os.path.dirname(path))
    row["extraction"] = sec.get("extraction")
    row["match"] = sec.get("match", sec.get("matching"))
    row["plots"] = sec.get("plots")
    other = {k: v for k, v in sec.items()
             if k not in ("total", "extraction", "match", "matching", "plots")
             and isinstance(v, (int, float))}
    row["other"] = sum(other.values()) if other else None
    row["gb_per_min"] = gb / (total / 60.0) if total and gb else None
    row["s_per_gb_ext"] = (row["extraction"] / gb
                           if row["extraction"] and gb else None)
    return row


def fmt(v, spec):
    width = int(spec.split(".")[0].rstrip("df") or 0)
    if isinstance(v, (int, float)) and v is not None:
        return format(v, spec)
    return "-".rjust(width)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*")
    ap.add_argument("--csv")
    args = ap.parse_args()
    dirs = args.dirs or sorted(glob.glob(
        os.path.expanduser(f"/home/{os.environ.get('USER', '')}/sites8/pikobs_doc_*")))
    files = [f for d in dirs for f in glob.glob(os.path.join(d, "*_timing.json"))]
    if not files:
        sys.exit("no *_timing.json found")
    rows = sorted((load(f) for f in files),
                  key=lambda r: (r["mode"], -(r["gb_per_min"] or 0)))

    head = (f"{'module':<13} {'mode':<8} {'GB':>7} {'files':>6} {'cpu':>4} "
            f"{'extract':>8} {'match':>7} {'plots':>7} {'other':>7} "
            f"{'total':>8} {'GB/min':>7} {'s/GB ext':>9}")
    print(head)
    print("-" * len(head))
    for r in rows:
        print(f"{r['module']:<13} {r['mode']:<8} {fmt(r['gb'], '7.1f')} "
              f"{fmt(r['files'], '6d')} {fmt(r['cpus'], '4d')} "
              f"{fmt(r['extraction'], '8.1f')} {fmt(r['match'], '7.1f')} "
              f"{fmt(r['plots'], '7.1f')} {fmt(r['other'], '7.1f')} "
              f"{fmt(r['total'], '8.1f')} {fmt(r['gb_per_min'], '7.2f')} "
              f"{fmt(r['s_per_gb_ext'], '9.1f')}")
    print("\nseconds per phase; 'other' is indexing, compaction, aggregation...;"
          "\nGB/min over the whole run, s/GB ext for the extraction alone.")

    if args.csv:
        keys = ["module", "mode", "gb", "files", "cpus", "extraction", "match",
                "plots", "other", "total", "gb_per_min", "s_per_gb_ext", "dir"]
        with open(args.csv, "w") as fh:
            fh.write(",".join(keys) + "\n")
            for r in rows:
                fh.write(",".join("" if r[k] is None else str(r[k]) for k in keys) + "\n")
        print(f"\nwritten {args.csv}")


if __name__ == "__main__":
    main()
