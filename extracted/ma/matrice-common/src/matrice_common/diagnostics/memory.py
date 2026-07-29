"""Memory snapshot helpers.

``snapshot()`` returns a ``MemorySnapshot`` carrying every reading we found
useful while diagnosing the Jetson-Thor unified-memory leak: parsed
``/proc/meminfo``, cgroup ``memory.current``, process RSS, NvMap clients,
tegrastats line, ``nvidia-smi --query-gpu=memory.used``, and CuPy default-pool
sizes. Each source is best-effort — a missing file or absent binary just leaves
that field ``None``.

``delta(before, after)`` returns the per-field difference as a snapshot —
useful for "what released" reports around shutdown sequences.

``format_table(snap)`` returns a human-readable string for log emission.

All functions are pure read; no writes, no side effects on the system.
"""

from __future__ import annotations

import dataclasses
import logging
import os
import shutil
import subprocess
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class MemorySnapshot:
    """A point-in-time memory reading from multiple sources. All sizes in bytes."""

    meminfo: Dict[str, int] = dataclasses.field(default_factory=dict)
    cgroup_current: Optional[int] = None
    process_rss: Optional[int] = None
    process_vms: Optional[int] = None
    nvmap_clients_total: Optional[int] = None
    tegrastats_line: Optional[str] = None
    gpu_memory_used: Optional[List[int]] = None  # one entry per GPU
    cupy_default_pool_used: Optional[int] = None
    cupy_default_pool_total: Optional[int] = None
    cupy_pinned_pool_used: Optional[int] = None
    cupy_pinned_pool_total: Optional[int] = None

    def to_dict(self) -> Dict[str, object]:
        return dataclasses.asdict(self)


def snapshot() -> MemorySnapshot:
    """Capture memory state from every available source."""
    s = MemorySnapshot()
    s.meminfo = _read_meminfo()
    s.cgroup_current = _read_cgroup_current()
    s.process_rss, s.process_vms = _read_process_mem()
    s.nvmap_clients_total = _read_nvmap_clients_total()
    s.tegrastats_line = _read_tegrastats_line()
    s.gpu_memory_used = _read_nvidia_smi_used()
    pool_used, pool_total, pinned_used, pinned_total = _read_cupy_pools()
    s.cupy_default_pool_used = pool_used
    s.cupy_default_pool_total = pool_total
    s.cupy_pinned_pool_used = pinned_used
    s.cupy_pinned_pool_total = pinned_total
    return s


def delta(before: MemorySnapshot, after: MemorySnapshot) -> MemorySnapshot:
    """Return ``after - before`` per field. Missing fields stay None."""
    out = MemorySnapshot()
    out.meminfo = {
        k: after.meminfo.get(k, 0) - before.meminfo.get(k, 0) for k in set(before.meminfo) | set(after.meminfo)
    }
    out.cgroup_current = _sub(after.cgroup_current, before.cgroup_current)
    out.process_rss = _sub(after.process_rss, before.process_rss)
    out.process_vms = _sub(after.process_vms, before.process_vms)
    out.nvmap_clients_total = _sub(after.nvmap_clients_total, before.nvmap_clients_total)
    if before.gpu_memory_used and after.gpu_memory_used and len(before.gpu_memory_used) == len(after.gpu_memory_used):
        out.gpu_memory_used = [a - b for a, b in zip(after.gpu_memory_used, before.gpu_memory_used)]
    out.cupy_default_pool_used = _sub(after.cupy_default_pool_used, before.cupy_default_pool_used)
    out.cupy_default_pool_total = _sub(after.cupy_default_pool_total, before.cupy_default_pool_total)
    out.cupy_pinned_pool_used = _sub(after.cupy_pinned_pool_used, before.cupy_pinned_pool_used)
    out.cupy_pinned_pool_total = _sub(after.cupy_pinned_pool_total, before.cupy_pinned_pool_total)
    return out


def format_table(snap: MemorySnapshot) -> str:
    """Render a snapshot as a human-readable multi-line table."""
    lines: List[str] = []
    lines.append("memory snapshot:")
    if snap.meminfo:
        keys = (
            "MemTotal",
            "MemFree",
            "MemAvailable",
            "Buffers",
            "Cached",
            "Slab",
            "SReclaimable",
            "SUnreclaim",
            "Shmem",
            "AnonPages",
        )
        for k in keys:
            v = snap.meminfo.get(k)
            if v is not None:
                lines.append(f"  meminfo.{k:<14} {_fmt_bytes(v)}")
    if snap.cgroup_current is not None:
        lines.append(f"  cgroup_current   {_fmt_bytes(snap.cgroup_current)}")
    if snap.process_rss is not None:
        lines.append(f"  process_rss      {_fmt_bytes(snap.process_rss)}")
    if snap.process_vms is not None:
        lines.append(f"  process_vms      {_fmt_bytes(snap.process_vms)}")
    if snap.nvmap_clients_total is not None:
        lines.append(f"  nvmap_clients    {_fmt_bytes(snap.nvmap_clients_total)}")
    if snap.gpu_memory_used:
        for idx, used in enumerate(snap.gpu_memory_used):
            lines.append(f"  gpu[{idx}].used      {_fmt_bytes(used)}")
    if snap.cupy_default_pool_used is not None:
        lines.append(
            f"  cupy_default     used={_fmt_bytes(snap.cupy_default_pool_used)} "
            f"total={_fmt_bytes(snap.cupy_default_pool_total or 0)}"
        )
    if snap.cupy_pinned_pool_used is not None:
        lines.append(
            f"  cupy_pinned      used={_fmt_bytes(snap.cupy_pinned_pool_used)} "
            f"total={_fmt_bytes(snap.cupy_pinned_pool_total or 0)}"
        )
    if snap.tegrastats_line:
        lines.append(f"  tegrastats       {snap.tegrastats_line.strip()}")
    return "\n".join(lines)


# --- internals ---------------------------------------------------------------


def _read_meminfo(path: str = "/proc/meminfo") -> Dict[str, int]:
    out: Dict[str, int] = {}
    try:
        with open(path, "r", encoding="ascii") as f:
            for line in f:
                key, _, rest = line.partition(":")
                if not rest:
                    continue
                rest = rest.strip()
                parts = rest.split()
                if not parts:
                    continue
                try:
                    value = int(parts[0])
                except ValueError:
                    continue
                if len(parts) > 1 and parts[1].lower() == "kb":
                    value *= 1024
                out[key.strip()] = value
    except OSError:
        return {}
    return out


def _read_cgroup_current() -> Optional[int]:
    # cgroup v2 unified path
    for path in ("/sys/fs/cgroup/memory.current", "/sys/fs/cgroup/memory/memory.usage_in_bytes"):
        try:
            with open(path, "r", encoding="ascii") as f:
                return int(f.read().strip())
        except OSError:
            continue
        except ValueError:
            continue
    return None


def _read_process_mem():
    try:
        import psutil  # type: ignore
    except Exception:  # noqa: BLE001
        return None, None
    try:
        proc = psutil.Process()
        info = proc.memory_info()
        return int(info.rss), int(info.vms)
    except Exception:  # noqa: BLE001
        return None, None


def _read_nvmap_clients_total() -> Optional[int]:
    """Sum the SIZE column from /sys/kernel/debug/nvmap/iovmm/clients (if readable)."""
    path = "/sys/kernel/debug/nvmap/iovmm/clients"
    try:
        with open(path, "r", encoding="ascii", errors="replace") as f:
            text = f.read()
    except OSError:
        return None
    total = 0
    found = False
    for line in text.splitlines()[1:]:  # skip header
        parts = line.split()
        if len(parts) < 4:
            continue
        # Last numeric column is typically the size; be permissive.
        for cell in reversed(parts):
            if cell.isdigit():
                total += int(cell)
                found = True
                break
    return total if found else None


def _read_tegrastats_line(timeout: float = 1.5) -> Optional[str]:
    binary = shutil.which("tegrastats")
    if not binary:
        return None
    try:
        result = subprocess.run(  # noqa: S603 - binary from shutil.which
            [binary, "--interval", "1000", "--count", "1"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    line = (result.stdout or result.stderr or "").splitlines()
    return line[0] if line else None


def _read_nvidia_smi_used() -> Optional[List[int]]:
    binary = shutil.which("nvidia-smi")
    if not binary:
        return None
    try:
        result = subprocess.run(  # noqa: S603 - binary from shutil.which
            [
                binary,
                "--query-gpu=memory.used",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=2.0,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode != 0:
        return None
    used: List[int] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            used.append(int(line) * 1024 * 1024)  # MiB -> bytes
        except ValueError:
            continue
    return used or None


def _read_cupy_pools():
    try:
        import cupy  # type: ignore
    except Exception:  # noqa: BLE001
        return None, None, None, None
    used = total = pinned_used = pinned_total = None
    try:
        pool = cupy.get_default_memory_pool()
        used = int(pool.used_bytes())
        total = int(pool.total_bytes())
    except Exception:  # noqa: BLE001
        pass
    try:
        ppool = cupy.get_default_pinned_memory_pool()
        pinned_used = int(ppool.used_bytes()) if hasattr(ppool, "used_bytes") else None
        pinned_total = int(ppool.total_bytes()) if hasattr(ppool, "total_bytes") else None
    except Exception:  # noqa: BLE001
        pass
    return used, total, pinned_used, pinned_total


def _sub(a, b):
    if a is None or b is None:
        return None
    return a - b


def _fmt_bytes(n: int) -> str:
    if n is None:
        return "n/a"
    sign = "-" if n < 0 else ""
    size: float = float(abs(n))
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if size < 1024 or unit == "TiB":
            return f"{sign}{size:.2f} {unit}" if unit != "B" else f"{sign}{int(size)} B"
        size /= 1024.0
    return f"{sign}{size:.2f} TiB"
