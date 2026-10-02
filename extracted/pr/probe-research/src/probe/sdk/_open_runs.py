"""Every run handle open in this process (lineage plan 3, F5).

The read recorder binds the Python workers a process spawns to its run only
while that run is the ONLY one open here: with a second one -- recording or
not, disabled included -- a worker's reads belong to neither for sure. This
module keeps that count. Stdlib only, in memory, no I/O: a disabled run
registers here too, and it touches neither the network nor the disk.

A handle registers when it is made (`Client._wrap_run`, an offline run, a
disabled run) and leaves when its close is over (`Run._settled`,
`DisabledRun.finish`). A handle nobody holds any more is gone (weak
references); one closed by a bare final status is no longer open. The
recorder listens (`listen`) and re-decides its binding at every change.
"""

from __future__ import annotations

import weakref
from typing import Any, Callable

#: id(handle) -> weakref to it.
_handles: dict[int, Any] = {}
_listeners: list[Callable[[], None]] = []
#: A handle nobody closed was collected since the last `take_collected`:
#: the recorder re-decides its binding then (from its hasher's thread, never
#: from inside the garbage collector).
_collected = False
#: A process opening runs for others (a service) keeps this many at most:
#: past it, the closed and the collected ones are forgotten.
MAX_HANDLES = 4096


def listen(callback: Callable[[], None]) -> None:
    """Call ``callback()`` after every open or close (the read recorder's
    `_rebind`). Once per callback."""
    if callback not in _listeners:
        _listeners.append(callback)


def _changed() -> None:
    for callback in list(_listeners):
        try:
            callback()
        except Exception:  # noqa: BLE001 -- bookkeeping never fails a run
            pass


def _on_collect(_ref: Any) -> None:
    # Runs inside the garbage collector: a flag, nothing else (no lock, no
    # change to `_handles`, which another thread may be iterating).
    global _collected
    _collected = True


def take_collected() -> bool:
    """Whether an open handle was collected since the last call (a run that
    was never finished -- a handle dropped, an init that failed after the
    handle was made): then no longer open, and the binding may change."""
    global _collected
    was, _collected = _collected, False
    return was


def opened(handle: Any) -> None:
    """A run handle was made in this process. Never raises."""
    try:
        _handles[id(handle)] = weakref.ref(handle, _on_collect)
        if len(_handles) > MAX_HANDLES:
            for key, ref in list(_handles.items()):
                live = ref()
                if live is None or not is_open(live):
                    _handles.pop(key, None)
    except Exception:  # noqa: BLE001
        return
    _changed()


def closed(handle: Any) -> None:
    """A run handle's close is over. Never raises."""
    _handles.pop(id(handle), None)
    _changed()


def is_open(handle: Any) -> bool:
    """Whether a run handle is still open: no ``finish()`` called on it, no
    final status sent (a disabled run: still ``running``). Unsure counts as
    open, which only ever keeps workers unbound."""
    try:
        from .disabled import DisabledRun

        if isinstance(handle, DisabledRun):
            return handle.status == "running"
        if getattr(handle, "_closed_status", None) is not None:
            return False
        called = getattr(handle, "_finish_called", None)
        return not (callable(called) and called())
    except Exception:  # noqa: BLE001
        return True


def another_open(run_id: str) -> bool:
    """Whether a run other than ``run_id`` is open in this process."""
    for ref in list(_handles.values()):
        handle = ref()
        if handle is None or not is_open(handle):
            continue
        if str(getattr(handle, "id", "")) != str(run_id):
            return True
    return False


def clear() -> None:
    """Forget every handle (a forked child's copies of its parent's; tests)."""
    _handles.clear()
