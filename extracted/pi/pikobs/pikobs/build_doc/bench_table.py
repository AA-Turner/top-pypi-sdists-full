#!/usr/bin/env python
"""The table: how long each module takes per GB, how much memory, which node.

Reads what bench_modules.sh left: bench_<module>_<n>d_mem.json (time and
memory, from bench_run.py) and <module>_timing.json in each output
directory (volume read, files, workers).

For each module, the two volumes give a straight line, seconds = a + b x GB:
a is the fixed cost (starting the workers, the viewer), b the seconds per
GB, and together they estimate any period. The memory does not grow with
the period -- every worker holds one cycle at a time -- so the node is
chosen from the peak, with a quarter more as margin.

    python bench_table.py                 # the benchmark in ~/sites8
    python bench_table.py --csv bench.csv
"""
import argparse
import glob
import json
import math
import os
import re

NODES = (185, 400)            # the memory the PBS queue offers per node, GB
MARGIN = 1.25


def disk_gb(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total / 1024 ** 3


def node_for(peak_gb):
    need = peak_gb * MARGIN
    for n in NODES:
        if need <= n:
            return f"{n} GB"
    return f"> {NODES[-1]} GB: fewer workers"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=f"/home/{os.environ.get('USER', '')}/sites8")
    ap.add_argument("--csv")
    args = ap.parse_args()

    rows = []
    for mem_path in sorted(glob.glob(os.path.join(args.base, "bench_*_*d_mem.json"))):
        m = re.match(r"bench_(.+)_(\d+)d_mem\.json$", os.path.basename(mem_path))
        if not m:
            continue
        module, days = m.group(1), int(m.group(2))
        mem = json.load(open(mem_path))
        out = os.path.join(args.base, f"pikobs_bench_{module}_{days}d")
        tim = {}
        for f in glob.glob(os.path.join(out, "*_timing.json")):
            tim = json.load(open(f))
            break
        gb = (tim.get("input_bytes") or 0) / 1e9
        wall = mem.get("wall_s") or 0
        # the processes' own memory (PSS) during this run; the job cgroup
        # peak only grows over a whole batch job and counts the page cache
        peak = mem.get("peak_total_gb") or 0
        rows.append(dict(
            module=module, days=days, gb=gb,
            files=tim.get("input_files") or 0,
            workers=tim.get("n_cpus") or tim.get("n_cpu") or 0,
            wall=wall, gb_min=gb / (wall / 60) if wall and gb else None,
            peak=peak, peak_proc=mem.get("peak_process_gb") or 0,
            busy=mem.get("busy_workers_mean") or 0,
            disk=disk_gb(out) if os.path.isdir(out) else 0,
            ok=mem.get("returncode") == 0))

    if not rows:
        print("no bench_*_mem.json found -- run bench_modules.sh first")
        return

    print(f"{'module':<13} {'days':>4} {'GB':>6} {'files':>5} {'time s':>7} "
          f"{'GB/min':>7} {'peak GB':>8} {'1 proc':>7} {'busy':>5} {'disk GB':>8}  ok")
    print("-" * 88)
    for r in sorted(rows, key=lambda r: (r['module'], r['days'])):
        print(f"{r['module']:<13} {r['days']:>4} {r['gb']:6.1f} {r['files']:5d} "
              f"{r['wall']:7.0f} {(r['gb_min'] or 0):7.2f} {r['peak']:8.1f} "
              f"{r['peak_proc']:7.2f} {r['busy']:5.0f} {r['disk']:8.2f}  "
              f"{'yes' if r['ok'] else 'NO'}")

    print(f"\n{'module':<13} {'fixed s':>8} {'s per GB':>9} {'peak GB':>8}  node to ask for")
    print("-" * 64)
    by_mod = {}
    for r in rows:
        by_mod.setdefault(r['module'], []).append(r)
    for mod in sorted(by_mod):
        rs = sorted(by_mod[mod], key=lambda r: r['gb'])
        peak = max(r['peak'] for r in rs)
        if len(rs) >= 2 and rs[-1]['gb'] > rs[0]['gb']:
            b = (rs[-1]['wall'] - rs[0]['wall']) / (rs[-1]['gb'] - rs[0]['gb'])
            a = rs[0]['wall'] - b * rs[0]['gb']
            fit = f"{max(a, 0):8.0f} {max(b, 0):9.2f}"
        else:
            fit = f"{'-':>8} {'-':>9}"
        print(f"{mod:<13} {fit} {peak:8.1f}  {node_for(peak)}")
    print("\ntime = fixed + (s per GB) x GB for the same number of workers;"
          "\nthe peak grows with the workers busy at once (up to N_CPUS), not with the GB;"
          f"\nnode = peak x {MARGIN}, rounded up to {', '.join(f'{n} GB' for n in NODES)}.")

    if args.csv:
        keys = list(rows[0])
        with open(args.csv, "w") as fh:
            fh.write(",".join(keys) + "\n")
            for r in rows:
                fh.write(",".join("" if r[k] is None else str(r[k]) for k in keys) + "\n")
        print(f"\nwritten {args.csv}")


if __name__ == "__main__":
    main()
