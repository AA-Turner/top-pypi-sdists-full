#!/usr/bin/env python
"""Run a command and record how long it took and how much memory it used.

    python bench_run.py --out run_mem.json -- bash run_timeserie_exp.sh

Every half second the whole process tree is sampled: the module's main
process and its dask workers. Recorded:

  peak_total_gb     the largest sum over the tree, in PSS -- shared pages
                    (the Python libraries every worker loads) are split
                    between the processes instead of counted once per
                    worker, which is what summing RSS would do
  peak_process_gb   the largest single process: a worker that blows up
                    alone is not helped by more memory per node, only by
                    fewer workers
  cgroup_peak_gb    what the PBS job's cgroup saw, when the node exposes it
                    (that is the number PBS kills on)
  busy_workers      the mean and the peak number of processes using a CPU,
                    to see whether a module keeps its workers busy
  wall_s            the elapsed time

Needs psutil (dask brings it).
"""
import argparse
import json
import os
import subprocess
import sys
import time

import psutil


def tree(proc):
    try:
        return [proc] + proc.children(recursive=True)
    except psutil.NoSuchProcess:
        return []


def pss(p):
    try:
        return p.memory_full_info().pss
    except (psutil.AccessDenied, psutil.NoSuchProcess, AttributeError):
        try:
            return p.memory_info().rss
        except psutil.NoSuchProcess:
            return 0


def cgroup_bytes():
    """Current and peak memory of this job's cgroup, if readable (v2, v1)."""
    try:
        rel = open("/proc/self/cgroup").read().strip().splitlines()
    except OSError:
        return None, None
    for line in rel:
        parts = line.split(":", 2)
        if len(parts) != 3:
            continue
        path = parts[2]
        for base, cur, peak in (("/sys/fs/cgroup", "memory.current", "memory.peak"),
                                ("/sys/fs/cgroup/memory", "memory.usage_in_bytes",
                                 "memory.max_usage_in_bytes")):
            d = base + path
            try:
                c = int(open(os.path.join(d, cur)).read())
            except (OSError, ValueError):
                continue
            try:
                pk = int(open(os.path.join(d, peak)).read())
            except (OSError, ValueError):
                pk = None
            return c, pk
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--interval", type=float, default=0.5)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args()
    cmd = args.cmd[1:] if args.cmd and args.cmd[0] == "--" else args.cmd
    if not cmd:
        sys.exit("no command given")

    t0 = time.time()
    child = subprocess.Popen(cmd)
    root = psutil.Process(child.pid)
    peak_total = peak_proc = 0
    busy_samples, busy_peak = [], 0
    cg_peak_seen = 0
    cpu_seen = {}
    last_t = time.time()
    while child.poll() is None:
        now = time.time()
        dt, last_t = max(now - last_t, 1e-3), now
        procs = tree(root)
        total = 0
        busy = 0
        for p in procs:
            m = pss(p)
            total += m
            peak_proc = max(peak_proc, m)
            try:
                t = p.cpu_times()
                used = t.user + t.system
                last = cpu_seen.get(p.pid)
                cpu_seen[p.pid] = used
                # busy: at least a quarter of a CPU since the last sample
                if last is not None and used - last > 0.25 * dt:
                    busy += 1
            except psutil.NoSuchProcess:
                pass
        peak_total = max(peak_total, total)
        busy_samples.append(busy)
        busy_peak = max(busy_peak, busy)
        cur, _ = cgroup_bytes()
        if cur:
            cg_peak_seen = max(cg_peak_seen, cur)
        time.sleep(args.interval)
    wall = time.time() - t0
    _, cg_peak = cgroup_bytes()

    gb = 1024 ** 3
    res = {
        "cmd": " ".join(cmd),
        "returncode": child.returncode,
        "wall_s": round(wall, 1),
        "peak_total_gb": round(peak_total / gb, 2),
        "peak_process_gb": round(peak_proc / gb, 2),
        "cgroup_peak_gb": round((cg_peak or cg_peak_seen) / gb, 2) if (cg_peak or cg_peak_seen) else None,
        "busy_workers_mean": round(sum(busy_samples) / max(len(busy_samples), 1), 1),
        "busy_workers_peak": busy_peak,
    }
    with open(args.out, "w") as fh:
        json.dump(res, fh, indent=1)
    print(f"[bench] {res['wall_s']} s, peak {res['peak_total_gb']} GB total "
          f"({res['peak_process_gb']} GB largest process), "
          f"workers busy {res['busy_workers_mean']} mean / {res['busy_workers_peak']} peak",
          flush=True)
    sys.exit(child.returncode)


if __name__ == "__main__":
    main()
