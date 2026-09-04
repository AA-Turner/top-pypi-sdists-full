"""Process-wide startup timeline for the runtime.

Every mark is seconds since the process started, so the timeline a platform
reads off ``/api/health`` covers interpreter start and the import chain, not
just the part that runs after the server module loaded. On Linux the kernel's
own process start time is used, which also covers the console script shim.
Elsewhere the anchor is the moment the ``dreadnode`` package began importing,
which is why ``dreadnode/__init__`` imports this module before anything that
costs time.

The store is module-level so code that runs before the server exists, or that
must not import it (scope validation, TLS trust, the litellm import), can still
record where its time went. The server's ``StartupState`` reads from here.
"""

import contextlib
import os
import time
import typing as t
from pathlib import Path

_IMPORT_MONOTONIC = time.monotonic()


def _linux_process_start_monotonic() -> float | None:
    stat = Path("/proc/self/stat").read_text(encoding="utf-8")
    uptime = float(Path("/proc/uptime").read_text(encoding="utf-8").split()[0])
    # ``comm`` may contain spaces or parentheses; every field after the last
    # ``)`` is positional. ``starttime`` is field 22 of the whole line, so it
    # sits at index 19 once pid, comm and state are stripped.
    fields = stat.rsplit(")", 1)[1].split()
    start_ticks = float(fields[19])
    ticks_per_second = os.sysconf("SC_CLK_TCK")
    age = uptime - start_ticks / ticks_per_second
    if age < 0:
        return None
    return time.monotonic() - age


def _resolve_anchor() -> tuple[float, str]:
    try:
        anchored = _linux_process_start_monotonic()
    except (OSError, ValueError, IndexError, AttributeError):
        anchored = None
    if anchored is None:
        return _IMPORT_MONOTONIC, "import"
    return anchored, "process"


PROCESS_STARTED_AT, ANCHOR = _resolve_anchor()

_marks: dict[str, float] = {}
_durations: dict[str, float] = {}


def process_start_monotonic() -> float:
    """Monotonic timestamp of process start, best effort."""
    return PROCESS_STARTED_AT


def process_start_source() -> str:
    """What the marks count from: ``process`` (kernel start time) or ``import``."""
    return ANCHOR


def mark(name: str) -> None:
    """Record when ``name`` happened, as seconds since process start.

    First write wins, so a mark set from a retry or a reload keeps the
    original cold-start value.
    """
    if name in _marks:
        return
    _marks[name] = round(time.monotonic() - PROCESS_STARTED_AT, 3)


def record_duration(name: str, seconds: float) -> None:
    """Record how long a named step took, independent of when it ran."""
    _durations[name] = round(_durations.get(name, 0.0) + seconds, 3)


@contextlib.contextmanager
def timed(name: str) -> t.Iterator[None]:
    """Record the wall time of the enclosed block as ``name``."""
    started = time.perf_counter()
    try:
        yield
    finally:
        record_duration(name, time.perf_counter() - started)


def marks() -> dict[str, float]:
    return dict(_marks)


def durations() -> dict[str, float]:
    return dict(_durations)


def reset() -> None:
    """Forget every mark and duration. For a runtime restarted in-process, and tests."""
    _marks.clear()
    _durations.clear()
