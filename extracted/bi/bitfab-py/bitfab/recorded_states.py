from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger("bitfab")


@dataclass
class _Recorded:
    holder: Any
    snapshot: Callable[[Any], Any]
    write: Callable[[Any, int], Any]
    version: int = 0
    dirty: bool = False
    finished: bool = False


@dataclass
class _Registry:
    lock: threading.Condition = field(default_factory=threading.Condition)
    entries: dict[tuple[str, str], _Recorded] = field(default_factory=dict)
    writing: bool = False


_registry = _Registry()


def update_recorded_state(
    trace_id: str,
    sandbox: str,
    create: Callable[[], Any],
    change: Callable[[Any], None],
    snapshot: Callable[[Any], Any],
    write: Callable[[Any, int], Any],
) -> None:
    with _registry.lock:
        key = (trace_id, sandbox)
        entry = _registry.entries.get(key)
        if entry is None or entry.finished:
            entry = _Recorded(create(), snapshot, write)
            _registry.entries[key] = entry
        change(entry.holder)
        entry.version += 1
        entry.dirty = True
        if not _registry.writing:
            _registry.writing = True
            threading.Thread(target=_write_while_dirty, daemon=True).start()


def recorded_state_versions(trace_id: str) -> dict[str, int] | None:
    with _registry.lock:
        versions = {
            sandbox: entry.version
            for (owner, sandbox), entry in _registry.entries.items()
            if owner == trace_id and not entry.finished
        }
    return versions or None


def trace_finished(trace_id: str) -> None:
    with _registry.lock:
        for (owner, sandbox), entry in list(_registry.entries.items()):
            if owner != trace_id:
                continue
            entry.finished = True
            if not entry.dirty and not _registry.writing:
                del _registry.entries[(owner, sandbox)]


def _next_dirty() -> tuple[tuple[str, str], _Recorded, Any, int] | None:
    for key, entry in _registry.entries.items():
        if entry.dirty:
            entry.dirty = False
            return key, entry, entry.snapshot(entry.holder), entry.version
    return None


def _write_while_dirty() -> None:
    while True:
        with _registry.lock:
            found = _next_dirty()
            if found is None:
                for key, entry in list(_registry.entries.items()):
                    if entry.finished:
                        del _registry.entries[key]
                _registry.writing = False
                _registry.lock.notify_all()
                return
        key, entry, state, version = found
        try:
            entry.write(state, version)
        except Exception:
            logger.debug(
                "Bitfab: the %s sandbox's state for trace %s could not be saved",
                key[1],
                key[0],
                exc_info=True,
            )


def flush_recorded_states(timeout: float) -> bool:
    deadline = time.monotonic() + max(timeout, 0.0)
    with _registry.lock:
        while _registry.writing:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return False
            _registry.lock.wait(remaining)
    return True
