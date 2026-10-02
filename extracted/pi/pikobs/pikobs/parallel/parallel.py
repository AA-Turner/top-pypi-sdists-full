import os
"""Shared task runner for the Pikobs modules.

Every module that sigmas work over Dask workers goes through
``run_tasks``. It gives the same behaviour everywhere:

* a progress indicator, always: the Dask bar on a terminal, plain
  progress lines when the output is a log file (the Dask bar writes
  escape codes that make a PBS log unreadable);
* one task that fails, or whose worker is killed by the memory limit,
  does not abort the phase: it returns ``None`` and the run continues;
* the result of every task comes back in the order it was submitted, so
  the caller can match results with its own task list.

Usage::

    from pikobs.parallel import run_tasks

    results = run_tasks(my_function, [(t,) for t in tasks], client,
                        label="plots")
"""

import sys
import time
from typing import Any, Callable, List, Optional, Sequence, Tuple

# Seconds between two progress lines when writing to a log file.
LOG_PROGRESS_EVERY = 15.0


def _short(seconds: float) -> str:
    """A duration someone can read: 52s, 2m3s, 1h04m."""
    seconds = int(round(seconds))
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m{seconds % 60:02d}s"
    return f"{seconds // 3600}h{(seconds % 3600) // 60:02d}m"


def _is_terminal() -> bool:
    try:
        return bool(sys.stdout.isatty())
    except Exception:
        return False


def _dask_bar(futures) -> bool:
    try:
        from dask.distributed import progress
        progress(futures, notebook=False)
        print(flush=True)
        return True
    except Exception:
        return False


def _slots(futures) -> int:
    """How many tasks the cluster runs at once (0 if unknown)."""
    try:
        return int(sum(futures[0].client.nthreads().values()))
    except Exception:
        return 0


def _log_progress(futures, label: str, every: float) -> None:
    """Plain progress lines, for a PBS log: no escape codes."""
    from dask.distributed import as_completed
    total = len(futures)
    slots = _slots(futures)
    done = 0
    last = time.time()
    t0 = last
    for _ in as_completed(futures):
        done += 1
        now = time.time()
        if done == total or now - last >= every:
            last = now
            pct = 100.0 * done / total
            # No estimate until a few tasks are in. On one task out of
            # forty-eight the rate is whatever that task happened to
            # cost, and the line reads "~814s left" for a run that takes
            # fifty seconds -- alarming and wrong, which is worse than
            # saying nothing.
            enough = done >= max(4, total // 20)
            rate = done / max(now - t0, 1e-9)
            eta = (total - done) / rate if rate > 0 else 0.0
            left = (f", ~{_short(eta)} left"
                    if done < total and enough else "")
            # Once every remaining task is already running, the time
            # left is the slowest of them, which no rate can tell:
            # the quick ones finish first. Say what is known instead.
            if slots and 0 < total - done <= slots:
                left = f", {total - done} still running"
            print(f"[pikobs] {label}: {done}/{total} ({pct:.0f}%) "
                  f"{_short(now - t0)} elapsed" + left, flush=True)


def run_tasks(func: Callable, arg_tuples: Sequence[Tuple], client,
              label: Optional[str] = None,
              progress_every: float = LOG_PROGRESS_EVERY) -> List[Any]:
    """Run ``func(*args)`` for every tuple, in parallel when a client is given.

    Returns one result per input tuple, ``None`` where the task failed.
    """
    name = label or getattr(func, '__name__', 'tasks')
    arg_tuples = list(arg_tuples)
    if not arg_tuples:
        return []

    if client is None:
        out = []
        total = len(arg_tuples)
        t0 = last = time.time()
        for i, args in enumerate(arg_tuples, start=1):
            try:
                out.append(func(*args))
            except Exception as exc:
                out.append(None)
                print(f"[pikobs] {name}: task {i} failed: {exc!r}",
                      file=sys.stderr, flush=True)
            now = time.time()
            if i == total or now - last >= progress_every:
                last = now
                print(f"[pikobs] {name}: {i}/{total} "
                      f"({100.0 * i / total:.0f}%) {now - t0:.0f}s elapsed",
                      flush=True)
        return out

    from dask.distributed import wait
    futures = [client.submit(func, *args, pure=False) for args in arg_tuples]

    if _is_terminal():
        _dask_bar(futures)
    else:
        try:
            _log_progress(futures, name, progress_every)
        except Exception:
            pass
    wait(futures)

    out, errors = [], []
    for fut in futures:
        try:
            # a result held by a dead worker is recomputed here
            out.append(fut.result())
        except Exception as exc:
            out.append(None)
            errors.append(exc)
    if errors:
        print(f"[pikobs] WARNING: {len(errors)}/{len(futures)} {name} tasks "
              f"lost, first error: {errors[0]!r}", file=sys.stderr, flush=True)
        _LOST.append((name, len(errors), len(futures), repr(errors[0])[:160]))
    client.cancel(futures)
    return out


# ---------------------------------------------------------------------------
# A clean end: the clients the modules opened are closed before Dask's own
# exit handlers run, the workers before the scheduler, so no heartbeat is
# left knocking at a closed door (a CommClosedError traceback in the log).
# ---------------------------------------------------------------------------
import atexit as _atexit
import distributed as _distributed        # noqa: F401 -- its exit handlers first


def _close_clients():
    """Close every open client, then its cluster; never raise at exit."""
    try:
        from distributed.client import _global_clients
        clients = list(_global_clients.values())
    except Exception:                     # pragma: no cover
        return
    for client in clients:
        cluster = getattr(client, "cluster", None)
        for thing in (client, cluster):
            if thing is None:
                continue
            try:
                thing.close(timeout=30)
            except Exception:             # pragma: no cover
                pass


# the phases that lost tasks, said again at the very end of the run: a
# WARNING in the middle of a long log is easy to miss, and the output of
# such a run is missing pieces (mapobs lost a quarter of its dashboards)
_LOST: list = []


def _report_lost():
    """At exit, after the clusters are closed: were any tasks lost?"""
    if not _LOST:
        return
    n = sum(k for _, k, _, _ in _LOST)
    line = "[pikobs] " + "=" * 64
    msg = [line, f"[pikobs] INCOMPLETE: {n} task(s) lost -- the output is "
                 f"missing pieces"]
    msg += [f"[pikobs]   {name}: {k} of {total} lost, first error: {err}"
            for name, k, total, err in _LOST]
    msg += ["[pikobs]   KilledWorker means workers killed for memory: ask the "
            "job for more memory, or fewer workers (N_CPUS).", line]
    for m in msg:
        print(m, file=sys.stderr, flush=True)
        print(m, flush=True)


# registered first so that it runs last (atexit runs in reverse order)
_atexit.register(_report_lost)
_atexit.register(_close_clients)


# ─────────────────────────────────────────────────────────────────────────────
# Memory of the job
# ─────────────────────────────────────────────────────────────────────────────

def job_memory() -> int:
    """The memory this job may use, in bytes.

    PBS puts each job in a cgroup whose memory.max is what the job asked
    for (199 GB for mem=185gb); Dask only sees the physical memory of the
    node (810 GB on ppp7), and sizes its workers from it. The tightest
    memory.max above this process wins; without one, the physical memory.
    """
    import psutil
    limits = [psutil.virtual_memory().total]
    try:
        cg = open("/proc/self/cgroup").read().strip().splitlines()[-1]
        path = "/sys/fs/cgroup" + cg.split(":")[-1]
        while path.startswith("/sys/fs/cgroup"):
            p = os.path.join(path, "memory.max")
            if os.path.isfile(p):
                v = open(p).read().strip()
                if v.isdigit():
                    limits.append(int(v))
            path = os.path.dirname(path)
        p = "/sys/fs/cgroup/memory/memory.limit_in_bytes"      # cgroup v1
        if os.path.isfile(p):
            limits.append(int(open(p).read().strip()))
    except (OSError, ValueError, IndexError):
        pass
    return min(limits)


def drawing_client(client, n_workers: int, per_worker_gb: float = 2.5,
                   share: float = 0.85, **kwargs):
    """A fresh cluster for drawing, held to the job's real memory.

    The workers of the extraction come out holding memory they do not give
    back, and drawing in long-lived processes keeps adding to it: 80 of
    them reached the job's limit (scatter, pairs, 3 regions x 3 criteria).
    This closes the old cluster and starts as many workers as fit at about
    per_worker_gb each, within share of the job's memory; each is held to
    its part -- Dask restarts one that goes over and gives its figure to
    another. Returns (client, number of workers).
    """
    import dask
    from dask.distributed import Client
    try:
        client.close(timeout=30)
    except Exception:
        pass
    per_worker_gb = float(os.environ.get('PIKOBS_DRAW_GB', per_worker_gb))
    budget = share * job_memory()
    n = max(1, min(n_workers, int(budget // (per_worker_gb * 1e9))))
    kwargs.setdefault("silence_logs", 50)
    try:
        with dask.config.set({"distributed.worker.memory.target": False,
                              "distributed.worker.memory.spill": False,
                              "distributed.worker.memory.pause": False,
                              "distributed.worker.memory.terminate": 0.95,
                              "distributed.scheduler.allowed-failures": 10}):
            new = Client(processes=True, threads_per_worker=1, n_workers=n,
                         memory_limit=int(budget / n), **kwargs)
    except Exception:
        new = Client(processes=True, threads_per_worker=1, n_workers=n,
                     **kwargs)
    return new, n


# ─────────────────────────────────────────────────────────────────────────────
# Memory advice: will this selection fit the job?
# ─────────────────────────────────────────────────────────────────────────────

#: GB of memory a module needs: base + factor x GB of the files its workers
#: read at once. Measured by pikobs/build_doc/bench_runtime.py (September
#: 2026, iasi, 1 to 28 cycles, peak PSS of the run and all its processes).
MEMORY_MODEL = {
    "mapobs": (5.0, 7.75), "cardio": (5.0, 1.92), "flags": (6.0, 1.56),
    "vdedr": (5.0, 1.28), "timeserie": (6.0, 0.42), "zone": (5.0, 0.37),
    "scatter": (6.5, 0.36), "verifprofile": (5.0, 0.35),
    "profile": (5.5, 0.34), "histogram": (5.0, 0.34),
    "obscountdb": (11.0, 0.24),
}


def memory_advice(module: str, sizes, n_workers: int = 0,
                  mem_bytes: int = 0, share: float = 0.85) -> bool:
    """Warn when a selection may not fit the job's memory.

    ``sizes`` are the sizes in bytes of the input files; the workers read
    the largest ones at once. Returns True when it warned. Never raises.
    """
    try:
        import math
        base, factor = MEMORY_MODEL[module]
        sizes = sorted((s for s in sizes if s), reverse=True)
        if not sizes:
            return False
        n_workers = n_workers or int(os.environ.get("NCPUS") or os.cpu_count() or 1)
        # in GiB, as PBS counts mem= and as the input check prints
        mem_gb = (mem_bytes or job_memory()) / 2**30
        top = sizes[:max(1, n_workers)]
        at_once = sum(top) / 2**30
        need = base + factor * at_once
        if need <= share * mem_gb:
            return False
        per_task = factor * at_once / len(top)
        fit = max(1, int((share * mem_gb - base) / per_task)) if per_task else n_workers
        ask = int(math.ceil(need / share / 50.0) * 50)
        node = 690                    # GiB, the most mem= a ppp7 node takes
        todo = (f"Ask for mem={ask}gb (a ppp7 node has about {node} GB), "
                f"or set N_CPUS={fit}." if ask <= node else
                f"That is more than a ppp7 node has (about {node} GB): "
                f"set N_CPUS={fit}, or split the period.")
        print(f"[{module}] WARNING: this selection may need more memory than "
              f"this job has.\n"
              f"[{module}]   Its {len(top)} largest files, read at once by "
              f"{len(top)} workers, come to {at_once:.1f} GB: about "
              f"{need:.0f} GB of memory,\n"
              f"[{module}]   for a job of {mem_gb:.0f} GB. {todo}",
              file=sys.stderr, flush=True)
        return True
    except Exception:
        return False


#: Run time of a module: fixed seconds + seconds per GiB of input, by mode.
#: Measured by pikobs/build_doc/bench_runtime.py (September 2026, iasi,
#: one region and one criterion, 1 to 28 cycles, a ppp7 node of 80 cores).
TIME_MODEL = {
    "cardio": {"alone": (42, 0.18), "with": (51, 0.69), "without": (42, 0.11)},
    "flags": {"alone": (34, 0.47)},
    "histogram": {"alone": (32, 0.89), "with": (33, 0.14), "without": (23, 0.99)},
    "mapobs": {"alone": (68, 4.33)},
    "obscountdb": {"alone": (29, 1.13)},
    "profile": {"alone": (19, 0.22), "with": (29, 0.29), "without": (21, 0.15)},
    "scatter": {"alone": (27, 0.18), "with": (39, 0.30), "without": (26, 0.24)},
    "timeserie": {"alone": (20, 0.26), "with": (40, 0.16), "without": (25, 0.00)},
    "vdedr": {"with": (54, 0.29), "without": (45, 0.13)},
    "verifprofile": {"alone": (19, 0.21), "with": (30, 0.00), "without": (20, 0.16)},
    "zone": {"alone": (22, 0.18), "with": (29, 0.13), "without": (25, 0.00)},
}


def _about(seconds: float) -> str:
    """A duration as a person would say it: no false precision."""
    if seconds < 90:
        return "about a minute"
    minutes = seconds / 60
    if minutes < 55:
        return f"about {int(round(minutes))} min"
    hours, rest = divmod(int(round(minutes / 5) * 5), 60)
    return f"about {hours} h" + (f" {rest:02d}" if rest else "")


def time_estimate(module: str, n_bytes: int, n_runs: int = 1) -> str:
    """Print, and return, a rough estimate of the run time. Never raises."""
    try:
        modes = TIME_MODEL[module]
        gib = n_bytes / 2**30
        if n_runs <= 1 or len(modes) == 1:
            fixed, per = modes.get("alone") or next(iter(modes.values()))
            t = fixed + per * gib
        else:
            t = max(f + p * gib for mode, (f, p) in modes.items() if mode != "alone")
        line = (f"[{module}] expected: {_about(t)} for {gib:.1f} GB with one "
                f"region and one criterion; more of them take longer")
        print(line, flush=True)
        return line
    except Exception:
        return ""
