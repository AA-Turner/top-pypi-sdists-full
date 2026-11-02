"""bound what a report and the log carry: texts and facts cut to size, at most N full tracebacks per key per window."""

from __future__ import annotations
import collections
import json
import threading
import time
from collections.abc import Callable, Mapping
from probe.service.watch.settings import WINDOW_S
#: The facts of an incident: each text cut to this (a traceback keeps its END),
#: the whole to MAX_FACTS_BYTES (the contract's 64 KiB), the last KEEP_EVENTS
#: events of a counted family.
MAX_FACT_TEXT = 4096
MAX_FACTS_BYTES = 64 * 1024
MAX_TRACEBACK = 16 * 1024
#: `service_error`'s tracebacks in service.log: this many per (site, exception
#: type) in WINDOW_S, one line each after that (the log rotates only at start).
TRACEBACKS_PER_WINDOW = 3


def bounded(value: object, depth: int = 0, *, key: str = "") -> object:
    """`value` as JSON can carry it: texts cut to MAX_FACT_TEXT (a traceback,
    by its key, keeps its END: the exception is its last line), at most 64 keys
    and 32 items a level, 6 levels deep."""
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value[-MAX_FACT_TEXT:] if "traceback" in key else value[:MAX_FACT_TEXT]
    if depth >= 6:
        return "..."
    if isinstance(value, Mapping):
        return {str(k)[:64]: bounded(v, depth + 1, key=str(k)) for k, v in list(value.items())[:64]}
    if isinstance(value, (list, tuple, set, frozenset, collections.deque)):
        return [bounded(v, depth + 1, key=key) for v in list(value)[:32]]
    return repr(value)[:MAX_FACT_TEXT]


def bounded_facts(facts: Mapping | None) -> dict:
    """The facts a report carries, within MAX_FACTS_BYTES."""
    out = bounded(dict(facts or {}))
    assert isinstance(out, dict)
    if len(json.dumps(out)) > MAX_FACTS_BYTES:
        return {"truncated": True, "keys": sorted(out)[:64]}
    return out


class TracebackGate:
    """At most TRACEBACKS_PER_WINDOW full tracebacks per key in WINDOW_S
    (`log_traceback`'s `gate`). Thread-safe."""

    def __init__(self, monotonic: Callable[[], float] = time.monotonic) -> None:
        self.monotonic = monotonic
        self._lock = threading.Lock()
        self._seen: dict = {}

    def allow(self, key: object) -> bool:
        now = self.monotonic()
        with self._lock:
            for old in [k for k, times in self._seen.items() if not times or now - times[-1] > WINDOW_S]:
                del self._seen[old]
            times = self._seen.setdefault(key, collections.deque())
            while times and now - times[0] > WINDOW_S:
                times.popleft()
            if len(times) >= TRACEBACKS_PER_WINDOW:
                return False
            times.append(now)
            return True


def log_traceback(
    log: Callable[[str], None], header: str, text: str, *, gate: TracebackGate | None = None, key: object = None,
) -> None:
    """`header`, then the traceback a line at a time, each with the service's
    prefix (the report keeps only the service's own lines of service.log). With
    `gate`: past its TRACEBACKS_PER_WINDOW for `key`, the header alone."""
    if gate is not None and text and not gate.allow(key):
        log(f"{header} (its traceback was logged {TRACEBACKS_PER_WINDOW} times in the last 15 min)")
        return
    log(header)
    for line in (text or "").rstrip().splitlines()[-200:]:
        log(f"  {line}")
