from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import threading

_MEBIBYTE = 1024 * 1024
_GIBIBYTE = 1024 * _MEBIBYTE
DEFAULT_CHILD_BUDGET_BYTES = 2 * _GIBIBYTE
DEFAULT_FLOOR_BYTES = 2 * _GIBIBYTE
DEFAULT_MAX_SWAP_USED_RATIO = 0.85
MACOS_CRITICAL_PRESSURE_LEVEL = 4
LINUX_CRITICAL_FULL_STALL_PERCENT = 10.0
_LINUX_STALL_FILES = ("/sys/fs/cgroup/memory.pressure", "/proc/pressure/memory")
DEFAULT_ADMISSION_POLL_SECONDS = 2.0
_READ_TIMEOUT_SECONDS = 5.0
_DISABLED_VALUES = frozenset({"0", "off", "false", "no"})


def _env_bytes(name: str, fallback: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return fallback
    try:
        megabytes = int(raw)
    except ValueError:
        return fallback
    return megabytes * _MEBIBYTE if megabytes > 0 else fallback


def throttle_disabled_by_env() -> bool:
    raw = os.environ.get("BITFAB_REPLAY_MEMORY_THROTTLE")
    return raw is not None and raw.strip().lower() in _DISABLED_VALUES


def _run_read(argv: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=_READ_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return completed.stdout if completed.returncode == 0 else None


def _sysctl_int(name: str) -> int | None:
    raw = _run_read(["sysctl", "-n", name])
    if raw is None:
        return None
    text = raw.strip()
    return int(text) if text.lstrip("-").isdigit() else None


def total_memory_bytes() -> int | None:
    try:
        return os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE")
    except (AttributeError, OSError, ValueError):
        return None


def _available_from_meminfo() -> int | None:
    try:
        with open("/proc/meminfo", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
    except (IndexError, OSError, ValueError):
        return None
    return None


def _available_from_memorystatus() -> int | None:
    free_percent = _sysctl_int("kern.memorystatus_level")
    total = total_memory_bytes()
    if free_percent is None or total is None:
        return None
    return total * min(max(free_percent, 0), 100) // 100


def available_memory_bytes() -> int | None:
    if sys.platform == "darwin":
        return _available_from_memorystatus()
    return _available_from_meminfo()


def _swap_used_ratio_from_swapusage() -> float | None:
    raw = _run_read(["sysctl", "-n", "vm.swapusage"])
    if raw is None:
        return None
    fields: dict[str, float] = {}
    key: str | None = None
    for part in raw.replace("=", " ").split():
        lowered = part.lower()
        if lowered in ("total", "used", "free"):
            key = lowered
            continue
        if key is None:
            continue
        scale = {"k": 1024.0, "m": _MEBIBYTE, "g": float(_GIBIBYTE)}.get(lowered[-1:])
        with contextlib.suppress(ValueError):
            fields[key] = float(lowered[:-1] if scale else lowered) * (scale or 1.0)
        key = None
    total = fields.get("total")
    used = fields.get("used")
    if total is None or used is None or total <= 0:
        return None
    return used / total


def _swap_used_ratio_from_meminfo() -> float | None:
    values: dict[str, int] = {}
    try:
        with open("/proc/meminfo", encoding="utf-8") as handle:
            for line in handle:
                label, _, rest = line.partition(":")
                if label in ("SwapTotal", "SwapFree"):
                    values[label] = int(rest.split()[0])
    except (IndexError, OSError, ValueError):
        return None
    total = values.get("SwapTotal")
    free = values.get("SwapFree")
    if total is None or free is None or total <= 0:
        return None
    return (total - free) / total


def swap_used_ratio() -> float | None:
    if sys.platform == "darwin":
        return _swap_used_ratio_from_swapusage()
    return _swap_used_ratio_from_meminfo()


def pressure_critical_from_level(raw: str | None) -> bool | None:
    text = (raw or "").strip()
    if not text.isdigit() or int(text) < 1:
        return None
    return int(text) >= MACOS_CRITICAL_PRESSURE_LEVEL


def pressure_critical_from_stall(raw: str | None) -> bool | None:
    for line in (raw or "").splitlines():
        fields = line.split()
        if not fields or fields[0] != "full":
            continue
        for field in fields[1:]:
            name, _, value = field.partition("=")
            if name != "avg10":
                continue
            try:
                return float(value) >= LINUX_CRITICAL_FULL_STALL_PERCENT
            except ValueError:
                return None
    return None


def _pressure_critical_from_stall_files() -> bool | None:
    for path in _LINUX_STALL_FILES:
        try:
            with open(path, encoding="utf-8") as handle:
                critical = pressure_critical_from_stall(handle.read())
        except OSError:
            continue
        if critical is not None:
            return critical
    return None


def memory_pressure_critical() -> bool | None:
    if sys.platform == "darwin":
        return pressure_critical_from_level(
            _run_read(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"])
        )
    if sys.platform.startswith("linux"):
        return _pressure_critical_from_stall_files()
    return None


def process_rss_bytes(pid: int) -> int | None:
    if sys.platform != "darwin":
        try:
            with open(f"/proc/{pid}/statm", encoding="utf-8") as handle:
                resident_pages = int(handle.read().split()[1])
            return resident_pages * os.sysconf("SC_PAGE_SIZE")
        except (AttributeError, IndexError, OSError, ValueError):
            return None
    raw = _run_read(["ps", "-o", "rss=", "-p", str(pid)])
    if raw is None:
        return None
    kilobytes = raw.strip()
    return int(kilobytes) * 1024 if kilobytes.isdigit() else None


class ReplayMemoryThrottle:
    def __init__(
        self,
        *,
        child_budget_bytes: int | None = None,
        floor_bytes: int | None = None,
        max_swap_used_ratio: float = DEFAULT_MAX_SWAP_USED_RATIO,
        poll_seconds: float = DEFAULT_ADMISSION_POLL_SECONDS,
    ) -> None:
        self._initial_budget = child_budget_bytes or _env_bytes(
            "BITFAB_REPLAY_CHILD_MEMORY_MB", DEFAULT_CHILD_BUDGET_BYTES
        )
        self._floor = floor_bytes or _env_bytes(
            "BITFAB_REPLAY_MEMORY_FLOOR_MB", DEFAULT_FLOOR_BYTES
        )
        self._max_swap_used_ratio = max_swap_used_ratio
        self._poll_seconds = poll_seconds
        self._condition = threading.Condition()
        self._resident: dict[int, int] = {}
        self._measured_peak = 0

    def _budget(self) -> int:
        in_flight = max(self._resident.values(), default=0)
        if self._measured_peak > 0:
            return max(self._measured_peak, in_flight)
        return max(self._initial_budget, in_flight)

    @property
    def child_budget_bytes(self) -> int:
        with self._condition:
            return self._budget()

    def _swap_exhausted(self) -> bool:
        ratio = swap_used_ratio()
        return ratio is not None and ratio >= self._max_swap_used_ratio

    def _memory_under_strain(self) -> bool:
        critical = memory_pressure_critical()
        if critical is not None:
            return critical
        return self._swap_exhausted()

    def _would_run_alone(self) -> bool:
        return not self._resident

    def _has_headroom(self) -> bool:
        if self._would_run_alone():
            return True
        if self._memory_under_strain():
            return False
        available = available_memory_bytes()
        if available is None:
            return True
        budget = self._budget()
        unrealized = sum(
            max(0, budget - resident) for resident in self._resident.values()
        )
        return available - unrealized - budget >= self._floor

    def admit(self, index: int, cancel: threading.Event) -> float:
        waited = 0.0
        with self._condition:
            while not self._has_headroom():
                if cancel.is_set():
                    return waited
                self._condition.wait(timeout=self._poll_seconds)
                waited += self._poll_seconds
            self._resident[index] = 0
        return waited

    def observe(self, index: int, resident_bytes: int) -> None:
        with self._condition:
            if index not in self._resident:
                return
            if resident_bytes <= self._resident[index]:
                return
            self._resident[index] = resident_bytes
            self._condition.notify_all()

    def release(self, index: int) -> None:
        with self._condition:
            resident = self._resident.pop(index, None)
            if resident is None:
                return
            self._measured_peak = max(self._measured_peak, resident)
            self._condition.notify_all()

    def wake_all(self) -> None:
        with self._condition:
            self._condition.notify_all()
