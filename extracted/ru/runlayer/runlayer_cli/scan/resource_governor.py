"""Best-effort CPU + memory governor for ``aiwatch scan``.

No ``setrlimit`` / cgroups / Job Objects / CPU affinity or elevated privileges.
The Python process cooperatively checkpoints; isolated POSIX crawl-child groups
also participate through short SIGSTOP/SIGCONT duty cycles. Windows cannot stop
process groups, so crawl children instead run below normal priority.

Two mechanisms:

* **CPU** — a checkpoint sleeps to hold the cumulative duty cycle
  (``process_time`` / wall clock) at or below ``target_core_fraction`` =
  ``max(0.05, min(cpu_cores, max_cpu_percent / 100))``. The percent is a
  single-core-equivalent duty budget, not total-machine utilization; 50 means
  0.5 core on every host. With N live POSIX crawl children, the parent target
  and each child's run duty are conservatively split to ``target / (N + 1)``.
  Floored at 0.05 of a core so it can never deadlock.
* **Memory** — a daemon monitor thread samples the process's peak-RSS growth
  since ``__enter__`` (``getrusage`` on POSIX, ``GetProcessMemoryInfo`` on
  Windows) against the MB ceiling — RSS covers native buffers and allocator
  overhead that Python-heap tracing can't see. Where no RSS probe exists,
  ``tracemalloc`` heap tracing starts as the fallback (and an already-tracing
  heap peak is checked alongside RSS either way, without paying the tracing
  tax on the default path). Over budget it sets an abort flag and kills all
  active crawl-shard children, and the next :meth:`checkpoint` raises
  :class:`ScanResourceLimitExceeded`. A path-count budget in the crawl is the
  bounded-work backstop.

Standard-library + ``structlog`` only, so it stays importable inside the frozen
``aiwatch`` bundle (guarded by ``tests/test_aiwatch_imports.py``).
"""

from __future__ import annotations

import ctypes
import os
import signal
import subprocess
import sys
import threading
import time
import tracemalloc
from collections.abc import Callable
from ctypes import wintypes

try:
    import resource
except ImportError:  # pragma: no cover - Windows only
    resource = None  # ty: ignore[invalid-assignment]

import structlog

logger = structlog.get_logger(__name__)


class ScanResourceLimitExceeded(Exception):
    """Raised at a checkpoint once the scan trips a configured resource cap.

    Propagates out of ``scan_all_clients`` to the ``_run_scan`` handler, which
    reports a Detect *error* check-in and exits nonzero (same path as any other
    scan failure) rather than silently returning partial findings.
    """


# --- Cap ranges + defaults -------------------------------------------------
#
# typer's IntRange (clamp=True) in commands/scan.py is the front line; the
# clamp_* helpers here are the backstop for programmatic callers that bypass it
# (mirrors project_scanner._clamp_scan_bound). Ranges/defaults are the single
# source of truth shared by the typer flags, the MDM docs, and the packaging.

MIN_CPU_CORES = 1
MIN_CPU_PERCENT = 5
MAX_CPU_PERCENT = 100
DEFAULT_CPU_PERCENT = 50
MIN_MEMORY_LIMIT_MB = 512
MAX_MEMORY_LIMIT_MB = 8192
DEFAULT_MEMORY_LIMIT_MB = 1024

# Floor on the CPU duty cycle so a pathological cap can never sleep the scan to
# a standstill (0.05 core ⇒ at most a 20x wall-clock stretch, never a deadlock).
_MIN_CORE_FRACTION = 0.05

# A single checkpoint never sleeps longer than this; the cumulative model catches
# up over subsequent checkpoints, and keeping each sleep short bounds how long an
# abort (memory over budget) waits before the next checkpoint raises.
_MAX_CHECKPOINT_SLEEP_S = 1.0

_DEFAULT_MONITOR_INTERVAL_S = 0.5
_DEFAULT_CHILD_DUTY_PERIOD_S = 0.1
_MIN_CHILD_DUTY_PERIOD_S = 0.01
_MAX_CHILD_DUTY_PERIOD_S = 1.0
_SIGSTOP: int | None = getattr(signal, "SIGSTOP", None)
_SIGCONT: int | None = getattr(signal, "SIGCONT", None)

# Bounded-work backstop: stop collecting crawl hits past this many paths so a
# runaway ``find`` on a giant home can't grow the results list without bound.
# The memory ceiling catches real blowups sooner; this is a coarse safety net.
DEFAULT_MAX_PATHS = 1_000_000

_MB = 1024 * 1024


def _logical_cpu_count() -> int:
    """Logical core count, floored at 1 (``os.cpu_count()`` can return ``None``)."""
    return os.cpu_count() or 1


# Import-time constants for the typer flag ``max=`` / default (evaluated on the
# scanning host, which is exactly where the core count matters).
MAX_CPU_CORES = _logical_cpu_count()
DEFAULT_CPU_CORES = max(MIN_CPU_CORES, MAX_CPU_CORES // 2)


def default_cpu_cores() -> int:
    """Default CPU-core cap: half the machine's logical cores (min 1)."""
    return DEFAULT_CPU_CORES


def clamp_cpu_cores(value: object, *, cpu_count: int | None = None) -> int:
    """Clamp a core cap into ``[1, cpu_count]``; non-int/bool ⇒ half-cores default."""
    maximum = cpu_count if cpu_count is not None else MAX_CPU_CORES
    if not isinstance(value, int) or isinstance(value, bool):
        return max(MIN_CPU_CORES, maximum // 2)
    return max(MIN_CPU_CORES, min(value, maximum))


def clamp_cpu_percent(value: object) -> int:
    """Clamp a CPU-percent cap into ``[5, 100]``; non-int/bool ⇒ default 50."""
    if not isinstance(value, int) or isinstance(value, bool):
        return DEFAULT_CPU_PERCENT
    return max(MIN_CPU_PERCENT, min(value, MAX_CPU_PERCENT))


def clamp_memory_limit_mb(value: object) -> int:
    """Clamp a memory ceiling into ``[512, 8192]`` MB; non-int/bool ⇒ default 1024."""
    if not isinstance(value, int) or isinstance(value, bool):
        return DEFAULT_MEMORY_LIMIT_MB
    return max(MIN_MEMORY_LIMIT_MB, min(value, MAX_MEMORY_LIMIT_MB))


def compute_target_core_fraction(
    cpu_cores: int, max_cpu_percent: int, *, cpu_count: int | None = None
) -> float:
    """Single-core-equivalent target: ``max(0.05, min(cores, pct / 100))``."""
    del cpu_count  # Retained for compatibility; host size does not scale this budget.
    return max(
        _MIN_CORE_FRACTION,
        min(float(cpu_cores), max_cpu_percent / 100.0),
    )


def _tracemalloc_peak_bytes() -> int:
    """Python-heap high-water mark in bytes (``0`` when tracing is off)."""
    if not tracemalloc.is_tracing():
        return 0
    return tracemalloc.get_traced_memory()[1]


class _PROCESS_MEMORY_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("PageFaultCount", wintypes.DWORD),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
    ]


def _windows_peak_working_set_bytes() -> int:  # pragma: no cover - win32 only
    try:
        counters = _PROCESS_MEMORY_COUNTERS()
        counters.cb = ctypes.sizeof(_PROCESS_MEMORY_COUNTERS)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # ty: ignore[unresolved-attribute]
        psapi = ctypes.WinDLL("psapi", use_last_error=True)  # ty: ignore[unresolved-attribute]
        handle = kernel32.GetCurrentProcess()
        ok = psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb)
        return int(counters.PeakWorkingSetSize) if ok else 0
    except Exception:
        return 0


def _default_rss_peak_bytes() -> int:
    """Process peak RSS in bytes; ``0`` when unavailable (never raises).

    Stdlib-only by design (frozen-bundle constraint): ``getrusage`` on POSIX
    (``ru_maxrss`` is bytes on macOS, kilobytes on Linux), psapi's
    ``GetProcessMemoryInfo`` peak working set via ctypes on Windows.
    """
    if sys.platform == "win32":
        return _windows_peak_working_set_bytes()
    if resource is None:
        return 0
    try:
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception:
        return 0
    return int(peak) if sys.platform == "darwin" else int(peak) * 1024


def terminate_process(proc: subprocess.Popen) -> None:
    """Best-effort hard kill of a crawl child; never raises.

    POSIX children are started in their own session (``start_new_session=True``)
    so ``killpg`` reaps the whole ``find`` process group (find + any subshell).
    Guards against killing our *own* group if a caller registered a
    non-session-isolated child. Windows falls back to ``proc.kill()``.
    """
    try:
        if proc.poll() is not None:
            return
    except Exception:
        pass

    killed = False
    if os.name == "posix":
        try:
            pgid = os.getpgid(proc.pid)
            if pgid != os.getpgid(0):
                os.killpg(pgid, signal.SIGKILL)
                killed = True
        except (ProcessLookupError, PermissionError, OSError):
            killed = False
    if not killed:
        try:
            proc.kill()
        except Exception:
            pass


def signal_process_group(proc: subprocess.Popen, sig: int) -> bool:
    """Signal an isolated POSIX child group without ever signaling our own."""
    if os.name != "posix":
        return False
    try:
        if proc.poll() is not None:
            return False
        pgid = os.getpgid(proc.pid)
        if pgid == os.getpgid(0):
            return False
        os.killpg(pgid, sig)
        return True
    except Exception:
        return False


class ResourceGovernor:
    """CPU/memory governor; use as a context manager around the scan.

    On ``__enter__`` it captures a peak-RSS baseline for the default RSS
    sampler (starting ``tracemalloc`` only as the fallback where no RSS probe
    exists, and never when custom samplers are supplied) and a daemon monitor
    thread plus the POSIX crawl-child duty controller; on ``__exit__`` it stops
    both and resumes any paused children. Between them, the
    scan calls :meth:`checkpoint` to throttle CPU and surface a memory abort,
    and :meth:`register_child` / :meth:`unregister_child` to share the CPU target
    with live crawl shards and kill them all on a memory abort.

    The clocks / sleep / memory sampler are injectable purely so the behavior is
    unit-testable without burning real CPU or allocating real memory.
    """

    def __init__(
        self,
        *,
        cpu_cores: int,
        max_cpu_percent: int,
        memory_limit_mb: int,
        cpu_count: int | None = None,
        max_paths: int = DEFAULT_MAX_PATHS,
        monitor_interval_s: float = _DEFAULT_MONITOR_INTERVAL_S,
        monotonic=time.monotonic,
        process_time=time.process_time,
        sleep=time.sleep,
        memory_sampler=None,
        rss_sampler=None,
        posix_child_control: bool | None = None,
        child_duty_period_s: float = _DEFAULT_CHILD_DUTY_PERIOD_S,
        process_group_signaler: Callable[[subprocess.Popen, int], bool] | None = None,
    ) -> None:
        total = cpu_count if cpu_count is not None else MAX_CPU_CORES
        self.cpu_cores = clamp_cpu_cores(cpu_cores, cpu_count=total)
        self.max_cpu_percent = clamp_cpu_percent(max_cpu_percent)
        self.memory_limit_mb = clamp_memory_limit_mb(memory_limit_mb)
        self._memory_limit_bytes = self.memory_limit_mb * _MB
        self.target_core_fraction = compute_target_core_fraction(
            self.cpu_cores, self.max_cpu_percent, cpu_count=total
        )
        self.max_paths = max_paths
        self._monitor_interval_s = monitor_interval_s
        self._monotonic = monotonic
        self._process_time = process_time
        self._sleep = sleep
        self._memory_sampler = memory_sampler
        self._rss_sampler = rss_sampler
        self._posix_child_control = (
            os.name == "posix" and _SIGSTOP is not None and _SIGCONT is not None
            if posix_child_control is None
            else posix_child_control
        )
        self._child_duty_period_s = min(
            max(child_duty_period_s, _MIN_CHILD_DUTY_PERIOD_S),
            _MAX_CHILD_DUTY_PERIOD_S,
        )
        self._process_group_signaler = process_group_signaler or signal_process_group

        self._abort = threading.Event()
        self._abort_reason: str | None = None
        self._stop = threading.Event()
        self._monitor: threading.Thread | None = None
        self._child_controller: threading.Thread | None = None
        self._duty_wake = threading.Event()
        self._checkpoint_lock = threading.Lock()
        self._child_lock = threading.Lock()
        self._children: set[subprocess.Popen] = set()
        self._paused_children: set[subprocess.Popen] = set()
        self._pause_phase = False
        self._started_tracemalloc = False
        self._start_wall = 0.0
        self._start_cpu = 0.0

    # --- context management ------------------------------------------------

    def __enter__(self) -> ResourceGovernor:
        self._start_wall = self._monotonic()
        self._start_cpu = self._process_time()
        baseline = 0
        if self._rss_sampler is None:
            baseline = _default_rss_peak_bytes()
            if baseline:
                # Peak-RSS growth since enter approximates the scan's own
                # footprint. The probes report lifetime high-water marks, so
                # the delta can under-count only if the process peaked before
                # enter — the governor wraps the scan from near process start,
                # where the baseline is just the startup footprint (logged
                # below for field diagnosis).
                self._rss_sampler = lambda: max(0, _default_rss_peak_bytes() - baseline)
        if self._memory_sampler is None:
            if self._rss_sampler is None:
                # No RSS probe on this platform: heap tracing is the only
                # memory signal left, worth tracemalloc's per-allocation tax.
                if not tracemalloc.is_tracing():
                    tracemalloc.start()
                    self._started_tracemalloc = True
            # Inert (returns 0) unless tracing is on — the fallback above, or
            # a caller that already traces — so the scan doesn't pay the
            # tracemalloc tax when RSS covers it.
            self._memory_sampler = _tracemalloc_peak_bytes
        self._stop.clear()
        self._duty_wake.clear()
        self._monitor = threading.Thread(
            target=self._monitor_loop,
            name="scan-resource-governor",
            daemon=True,
        )
        self._monitor.start()
        if self._posix_child_control:
            self._child_controller = threading.Thread(
                target=self._child_cpu_loop,
                name="scan-crawl-cpu-governor",
                daemon=True,
            )
            self._child_controller.start()
        logger.debug(
            "scan_resource_governor_started",
            cpu_cores=self.cpu_cores,
            max_cpu_percent=self.max_cpu_percent,
            memory_limit_mb=self.memory_limit_mb,
            # Pre-enter peak RSS. Diagnoses both sampler edge cases in the
            # field: a surprising abort (RSS growth > old heap ceiling) and
            # under-counting behind a pre-enter transient peak.
            memory_baseline_mb=baseline // _MB,
            target_core_fraction=round(self.target_core_fraction, 3),
        )
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self._stop.set()
        self._duty_wake.set()
        controller = self._child_controller
        if controller is not None:
            controller.join(timeout=max(1.0, self._child_duty_period_s * 4))
        self._child_controller = None
        self._resume_all_children()
        monitor = self._monitor
        if monitor is not None:
            monitor.join(timeout=self._monitor_interval_s * 4)
        self._monitor = None
        if self._started_tracemalloc:
            tracemalloc.stop()
            self._started_tracemalloc = False
        return False  # never suppress the scan's own exceptions

    # --- checkpoint (CPU throttle + abort surface) -------------------------

    def checkpoint(self) -> None:
        """Throttle CPU and raise if a resource cap has been tripped.

        Raises :class:`ScanResourceLimitExceeded` when the memory monitor has
        flagged an abort; otherwise sleeps as needed to hold the CPU duty cycle.
        Abort is checked both before and after the (bounded) sleep so a memory
        blowup during a throttle sleep still surfaces on this same call.
        """
        with self._checkpoint_lock:
            self._raise_if_aborted()
            sleep_for = self._throttle_sleep_duration()
        # Serialize the shared snapshot, not the wait: phase sleeps may overlap.
        if sleep_for > 0:
            self._sleep(sleep_for)
        with self._checkpoint_lock:
            self._raise_if_aborted()

    def _raise_if_aborted(self) -> None:
        if self._abort.is_set():
            raise ScanResourceLimitExceeded(
                self._abort_reason or "scan resource limit exceeded"
            )

    def _throttle_sleep_duration(self) -> float:
        elapsed = self._monotonic() - self._start_wall
        cpu_used = self._process_time() - self._start_cpu
        if elapsed <= 0 or cpu_used <= 0:
            return 0.0
        # Hold cumulative process_time / wall <= target_core_fraction:
        #   cpu_used / (elapsed + sleep) <= target  =>  sleep >= cpu_used/target - elapsed
        required_wall = cpu_used / self.effective_parent_core_fraction
        sleep_for = required_wall - elapsed
        return min(max(sleep_for, 0.0), _MAX_CHECKPOINT_SLEEP_S)

    @property
    def effective_parent_core_fraction(self) -> float:
        """Parent duty budget after sharing the target with live crawl children."""
        with self._child_lock:
            live_children = len(self._live_children_locked())
            return self.target_core_fraction / (live_children + 1)

    # --- POSIX crawl-child CPU duty controller -----------------------------

    def _live_children_locked(self) -> list[subprocess.Popen]:
        live: list[subprocess.Popen] = []
        for proc in list(self._children):
            try:
                alive = proc.poll() is None
            except Exception:
                alive = True
            if alive:
                live.append(proc)
            else:
                self._children.discard(proc)
                self._paused_children.discard(proc)
        return live

    def _set_child_paused_locked(self, proc: subprocess.Popen, *, paused: bool) -> None:
        if paused:
            if proc in self._paused_children or _SIGSTOP is None:
                return
            try:
                signaled = self._process_group_signaler(proc, _SIGSTOP)
            except Exception:
                signaled = False
            if signaled:
                self._paused_children.add(proc)
            return

        if proc not in self._paused_children:
            return
        resumed = _SIGCONT is None
        if _SIGCONT is not None:
            try:
                resumed = self._process_group_signaler(proc, _SIGCONT)
            except Exception:
                resumed = False
        if not resumed:
            try:
                resumed = proc.poll() is not None
            except Exception:
                resumed = False
        if resumed:
            self._paused_children.discard(proc)

    def _resume_all_children(self) -> None:
        if not self._posix_child_control:
            return
        with self._child_lock:
            self._pause_phase = False
            for proc in list(self._paused_children):
                self._set_child_paused_locked(proc, paused=False)

    def _wait_for_duty_phase(self, duration: float) -> None:
        if duration <= 0 or self._stop.is_set():
            return
        self._duty_wake.clear()
        if not self._stop.is_set():
            self._duty_wake.wait(duration)

    def _child_cpu_loop(self) -> None:
        """SIGSTOP/SIGCONT child groups so parent + children stay under target."""
        try:
            while not self._stop.is_set():
                with self._child_lock:
                    children = self._live_children_locked()
                    self._pause_phase = False
                    for proc in list(self._paused_children):
                        self._set_child_paused_locked(proc, paused=False)

                if not children:
                    self._wait_for_duty_phase(self._child_duty_period_s)
                    continue

                child_fraction = self.target_core_fraction / (len(children) + 1)
                run_duration = self._child_duty_period_s * min(
                    max(child_fraction, 0.0), 1.0
                )
                self._wait_for_duty_phase(run_duration)
                if self._stop.is_set():
                    break

                with self._child_lock:
                    self._pause_phase = True
                    for proc in self._live_children_locked():
                        self._set_child_paused_locked(proc, paused=True)
                self._wait_for_duty_phase(self._child_duty_period_s - run_duration)
        finally:
            self._resume_all_children()

    # --- memory monitor ----------------------------------------------------

    def _monitor_loop(self) -> None:
        while not self._stop.wait(self._monitor_interval_s):
            self._sample_memory_once()

    def _sample_memory_once(self) -> bool:
        """Sample peak memory once; abort + kill child if over budget. Test seam.

        Both peaks are held to the same ``memory_limit_mb`` cap: tracemalloc
        for the Python heap, RSS for everything the OS actually charges the
        process (native buffers, allocator overhead).
        """
        if self._abort.is_set():
            return False
        for label, sampler in (
            ("python-heap", self._memory_sampler),
            ("rss", self._rss_sampler),
        ):
            if sampler is None:
                continue
            try:
                peak = sampler()
            except Exception:
                continue
            if peak > self._memory_limit_bytes:
                self._trigger_abort(
                    f"memory ({label}) high-water {peak // _MB} MB "
                    f"exceeded cap {self.memory_limit_mb} MB"
                )
                return True
        return False

    def _trigger_abort(self, reason: str) -> None:
        self._abort_reason = reason
        self._abort.set()
        logger.warning("scan_resource_limit_tripped", reason=reason)
        self._kill_children()

    # --- crawl child registration + kill-on-abort --------------------------

    def register_child(self, proc: subprocess.Popen) -> None:
        """Track a crawl child for aggregate CPU governance and memory abort."""
        with self._child_lock:
            self._children.add(proc)
            if self._posix_child_control and self._pause_phase:
                self._set_child_paused_locked(proc, paused=True)
        self._duty_wake.set()
        # Lost the race with an abort that already fired: kill immediately.
        if self._abort.is_set():
            terminate_process(proc)

    def unregister_child(self, proc: subprocess.Popen) -> None:
        with self._child_lock:
            if self._posix_child_control:
                self._set_child_paused_locked(proc, paused=False)
            self._children.discard(proc)
        self._duty_wake.set()

    def _kill_children(self) -> None:
        with self._child_lock:
            children = list(self._children)
        for proc in children:
            terminate_process(proc)


def build_governor(
    *,
    cpu_cores: int | None = None,
    max_cpu_percent: int | None = None,
    memory_limit_mb: int | None = None,
    cpu_count: int | None = None,
    max_paths: int = DEFAULT_MAX_PATHS,
) -> ResourceGovernor:
    """Construct a governor from optional caps, filling defaults for any unset.

    ``None`` for a cap means "use the default"; every value is then clamped to
    its supported range by :class:`ResourceGovernor` (the typer flags clamp
    first, so this only bites programmatic callers). Centralizes the ``None`` →
    default policy instead of repeating it at each call site.
    """
    return ResourceGovernor(
        cpu_cores=cpu_cores if cpu_cores is not None else default_cpu_cores(),
        max_cpu_percent=(
            max_cpu_percent if max_cpu_percent is not None else DEFAULT_CPU_PERCENT
        ),
        memory_limit_mb=(
            memory_limit_mb if memory_limit_mb is not None else DEFAULT_MEMORY_LIMIT_MB
        ),
        cpu_count=cpu_count,
        max_paths=max_paths,
    )
