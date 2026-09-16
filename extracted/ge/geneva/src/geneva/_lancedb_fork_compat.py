# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Defer LanceDB's background-loop restart until after ``fork()`` returns.

Ray launches POSIX processes with ``Popen(preexec_fn=...)``, so Python runs
child-atfork callbacks before each exec. LanceDB 0.37.1 starts a Python thread
from that callback, which can corrupt glibc's inherited thread-stack cache.
Keep the existing fork-child behavior, but perform its thread creation lazily
when the child first uses the synchronous LanceDB bridge.
"""

from __future__ import annotations

import functools
import os
import threading
from typing import Any

_IN_FORK = False
_FORKING_PID: int | None = None
_RESTART_LOCK: Any | None = None
_RESTART_LOCK_PID: int | None = None
_PATCH_MARKER = "_geneva_lancedb_fork_compat"
_DEFERRED_MARKER = "_geneva_lancedb_start_deferred"


def _has_unsafe_child_reset(background_loop: Any) -> bool:
    """Return whether LanceDB's child hook directly restarts its event loop."""
    callback = getattr(background_loop, "_reset_after_fork", None)
    code = getattr(callback, "__code__", None)
    callback_globals = getattr(callback, "__globals__", {})
    return bool(
        code is not None
        and "LOOP" in code.co_names
        and "_start" in code.co_names
        and callback_globals.get("LOOP") is getattr(background_loop, "LOOP", None)
    )


def _before_fork() -> None:
    global _FORKING_PID, _IN_FORK
    _FORKING_PID = os.getpid()
    _IN_FORK = True


def _after_fork() -> None:
    global _FORKING_PID, _IN_FORK
    _IN_FORK = False
    _FORKING_PID = None


def _child_restart_lock() -> Any:
    """Return a lock created in this process, never inherited from its parent."""
    global _RESTART_LOCK, _RESTART_LOCK_PID
    pid = os.getpid()
    if pid != _RESTART_LOCK_PID:
        _RESTART_LOCK = threading.Lock()
        _RESTART_LOCK_PID = pid
    return _RESTART_LOCK


def install() -> bool:
    """Install the compatibility shim when the imported LanceDB needs it.

    Returns ``True`` when the unsafe LanceDB callback was found and is patched.
    The structural check deliberately makes this a no-op after LanceDB stops
    calling ``LOOP._start()`` from its child atfork callback.
    """
    if not hasattr(os, "register_at_fork"):
        return False

    import lancedb.background_loop as background_loop

    loop_type = getattr(background_loop, "BackgroundEventLoop", None)
    if loop_type is None or not _has_unsafe_child_reset(background_loop):
        return False

    current_start = loop_type._start
    if getattr(current_start, _PATCH_MARKER, False):
        return True

    original_start = current_start
    original_run = loop_type.run

    @functools.wraps(original_start)
    def safe_start(self: Any, *args: Any, **kwargs: Any) -> None:
        if _IN_FORK and os.getpid() != _FORKING_PID:
            setattr(self, _DEFERRED_MARKER, True)
            return
        original_start(self, *args, **kwargs)
        setattr(self, _DEFERRED_MARKER, False)

    @functools.wraps(original_run)
    def run_with_lazy_restart(self: Any, *args: Any, **kwargs: Any) -> Any:
        if getattr(self, _DEFERRED_MARKER, False):
            # This runs after os.fork() returns. Build the lock lazily in the
            # current PID so a lock held by a vanished parent thread can never
            # deadlock the child.
            with _child_restart_lock():
                if getattr(self, _DEFERRED_MARKER, False):
                    self._start()
        return original_run(self, *args, **kwargs)

    setattr(safe_start, _PATCH_MARKER, True)
    loop_type._start = safe_start
    loop_type.run = run_with_lazy_restart
    # Pre-seed the only per-loop state the child callback mutates. The callback
    # then flips an existing bool instead of adding an attribute after fork.
    setattr(background_loop.LOOP, _DEFERRED_MARKER, False)

    # ``before`` callbacks run newest-first, while child callbacks run in
    # registration order. LanceDB's child callback was registered by the import
    # above, so it sees our flag and defers; our child callback then clears it
    # before os.fork() returns to application code.
    os.register_at_fork(
        before=_before_fork,
        after_in_parent=_after_fork,
        after_in_child=_after_fork,
    )
    return True
