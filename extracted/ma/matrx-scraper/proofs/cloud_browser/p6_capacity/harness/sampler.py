"""Host + per-unit resource sampler. Phase-0 proof harness (NOT shipped code).

Reads /proc directly rather than depending on psutil, because the target hosts (a live
EC2 sandbox box and a hosted 8-core/32-GiB VPS) must be able to run this with nothing
installed. Everything here is a delta between two /proc reads at a fixed interval.

What it records, per sample (PLAN.md "Record per-run p50/p95/p99 CPU, resident memory,
disk I/O ..."):

  cpu_busy_pct    host CPU excluding idle AND iowait (iowait is not CPU work)
  cpu_steal_pct   hypervisor steal -- on a burstable host this is the tell for throttling
  mem_used_pct    (MemTotal - MemAvailable) / MemTotal
  disk_util_pct   max over physical devices of io_time delta / wall delta
  disk_read_bps / disk_write_bps aggregate over physical devices
  psi_*           /proc/pressure avg10 where the kernel exposes it (best signal we get)
  unit_rss_bytes  summed VmRSS over every tracked unit's whole process tree
  unit_procs      process count in those trees

Attribution honesty: unit RSS is summed RSS, which double-counts shared pages between
Chromium processes. It is an upper bound on per-unit memory, and the host-level
mem_used_pct is the number the guardrail actually keys on.
"""

from __future__ import annotations

import os
import threading
import time
from pathlib import Path

PROC = Path("/proc")
_SKIP_DEV_PREFIX = ("loop", "ram", "zram", "sr", "fd", "md")


def _read(path: Path) -> str:
    try:
        return path.read_text()
    except OSError:
        return ""


def _cpu_totals() -> tuple[float, float, float]:
    """(busy_jiffies, steal_jiffies, total_jiffies) from /proc/stat line 'cpu '."""
    for line in _read(PROC / "stat").splitlines():
        if line.startswith("cpu "):
            f = [float(x) for x in line.split()[1:]]
            # user nice system idle iowait irq softirq steal guest guest_nice
            while len(f) < 10:
                f.append(0.0)
            idle = f[3] + f[4]
            total = sum(f[:8])
            return total - idle, f[7], total
    return 0.0, 0.0, 0.0


def _mem() -> tuple[int, int]:
    total = avail = 0
    for line in _read(PROC / "meminfo").splitlines():
        if line.startswith("MemTotal:"):
            total = int(line.split()[1]) * 1024
        elif line.startswith("MemAvailable:"):
            avail = int(line.split()[1]) * 1024
        if total and avail:
            break
    return total, avail


def _diskstats() -> dict[str, tuple[int, int, int]]:
    """dev -> (read_sectors, write_sectors, io_time_ms) for physical-looking devices."""
    out: dict[str, tuple[int, int, int]] = {}
    for line in _read(PROC / "diskstats").splitlines():
        parts = line.split()
        if len(parts) < 14:
            continue
        name = parts[2]
        if name.startswith(_SKIP_DEV_PREFIX):
            continue
        # a partition (nvme0n1p1, sda1) is already counted by its parent device
        if name[-1].isdigit() and not name.startswith(("nvme", "mmcblk")):
            continue
        try:
            out[name] = (int(parts[5]), int(parts[9]), int(parts[12]))
        except ValueError:
            continue
    return out


def _psi(resource: str) -> float | None:
    txt = _read(PROC / "pressure" / resource)
    for line in txt.splitlines():
        if line.startswith("some"):
            for tok in line.split():
                if tok.startswith("avg10="):
                    try:
                        return float(tok.split("=", 1)[1])
                    except ValueError:
                        return None
    return None


def _children(pid: int) -> list[int]:
    kids: list[int] = []
    tasks = PROC / str(pid) / "task"
    try:
        for task in tasks.iterdir():
            for tok in _read(task / "children").split():
                try:
                    kids.append(int(tok))
                except ValueError:
                    pass
    except OSError:
        pass
    return kids


def _tree(pid: int, seen: set[int] | None = None) -> list[int]:
    seen = seen if seen is not None else set()
    if pid in seen:
        return []
    seen.add(pid)
    out = [pid]
    for kid in _children(pid):
        out.extend(_tree(kid, seen))
    return out


def _rss(pid: int) -> int:
    for line in _read(PROC / str(pid) / "status").splitlines():
        if line.startswith("VmRSS:"):
            try:
                return int(line.split()[1]) * 1024
            except (IndexError, ValueError):
                return 0
    return 0


class Sampler:
    """Background sampler. Start it, register unit pids as they appear, stop, read series."""

    def __init__(self, interval: float = 1.0) -> None:
        self.interval = interval
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._pids_lock = threading.Lock()
        self._unit_pids: dict[str, int] = {}
        self.samples: list[dict[str, float | int | None]] = []
        self.ncpu = os.cpu_count() or 1

    # -- unit registration -------------------------------------------------
    def track_unit(self, unit_id: str, pid: int) -> None:
        with self._pids_lock:
            self._unit_pids[unit_id] = pid

    def untrack_unit(self, unit_id: str) -> None:
        with self._pids_lock:
            self._unit_pids.pop(unit_id, None)

    # -- lifecycle ---------------------------------------------------------
    def start(self) -> None:
        self._stop.clear()
        self.samples = []
        self._thread = threading.Thread(target=self._loop, name="p6-sampler", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=self.interval * 3)
            self._thread = None

    def mark(self) -> int:
        """Index of the next sample -- used to slice off the stabilization window."""
        return len(self.samples)

    def window(self, start_index: int) -> list[dict]:
        return self.samples[start_index:]

    # -- loop --------------------------------------------------------------
    def _loop(self) -> None:
        prev_busy, prev_steal, prev_total = _cpu_totals()
        prev_disk = _diskstats()
        prev_t = time.monotonic()
        while not self._stop.wait(self.interval):
            now = time.monotonic()
            dt = max(now - prev_t, 1e-6)
            busy, steal, total = _cpu_totals()
            d_total = max(total - prev_total, 1e-9)
            cpu_busy_pct = 100.0 * (busy - prev_busy) / d_total
            cpu_steal_pct = 100.0 * (steal - prev_steal) / d_total
            prev_busy, prev_steal, prev_total = busy, steal, total

            disk = _diskstats()
            util = 0.0
            read_b = write_b = 0.0
            for dev, (r, w, io_ms) in disk.items():
                pr, pw, pio = prev_disk.get(dev, (r, w, io_ms))
                util = max(util, 100.0 * (io_ms - pio) / (dt * 1000.0))
                read_b += (r - pr) * 512 / dt
                write_b += (w - pw) * 512 / dt
            prev_disk = disk

            mem_total, mem_avail = _mem()
            mem_used_pct = 100.0 * (mem_total - mem_avail) / mem_total if mem_total else 0.0

            with self._pids_lock:
                pids = dict(self._unit_pids)
            unit_rss = 0
            unit_procs = 0
            per_unit: dict[str, int] = {}
            for unit_id, pid in pids.items():
                tree = _tree(pid)
                rss = sum(_rss(p) for p in tree)
                per_unit[unit_id] = rss
                unit_rss += rss
                unit_procs += len(tree)

            self.samples.append(
                {
                    "t": time.time(),
                    "cpu_busy_pct": round(min(cpu_busy_pct, 100.0), 3),
                    "cpu_steal_pct": round(cpu_steal_pct, 3),
                    "mem_used_pct": round(mem_used_pct, 3),
                    "mem_used_bytes": mem_total - mem_avail,
                    "disk_util_pct": round(min(util, 100.0), 3),
                    "disk_read_bps": round(read_b, 1),
                    "disk_write_bps": round(write_b, 1),
                    "psi_cpu_avg10": _psi("cpu"),
                    "psi_io_avg10": _psi("io"),
                    "psi_mem_avg10": _psi("memory"),
                    "unit_rss_bytes": unit_rss,
                    "unit_count": len(pids),
                    "unit_procs": unit_procs,
                    "per_unit_rss_bytes": per_unit,
                }
            )
            prev_t = now
