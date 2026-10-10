from __future__ import annotations

import contextlib
import logging
import os
import sys
import threading
import types
from typing import Any, Callable

logger = logging.getLogger("kolo")

# Set on every Thread Kolo starts for its own background work, before start,
# so the pure-Python monitor can recognise it from its first event.
KOLO_WORKER_THREAD_MARKER = "_kolo_worker_thread"


_TYPE_MODULE = vars(type)["__module__"]


def _is_kolo_profiler(profiler: object) -> bool:
    # Only types are inspected, never attributes of the (possibly foreign)
    # profiler object itself, so its __getattr__ or __class__ can't run.
    # threading installs the Rust profiler as its bound
    # register_threading_profiler until the thread's first event swaps in the
    # profiler itself.
    bound = type(profiler) in (types.MethodType, types.BuiltinMethodType)
    owner = profiler.__self__ if bound else profiler  # type: ignore[attr-defined]
    owner_type = type(owner)
    # Read __module__ through `type`'s own descriptor, so a foreign
    # metaclass's __getattribute__ can't run either.
    if _TYPE_MODULE.__get__(owner_type, type) == "kolo._kolo":
        return True
    # Any pure-Python KoloProfiler, subclasses included. If kolo.profiler
    # isn't imported, no such profiler exists.
    # (A partially imported kolo.profiler may not define it yet.)
    kolo_profiler = getattr(sys.modules.get("kolo.profiler"), "KoloProfiler", None)
    return isinstance(kolo_profiler, type) and issubclass(owner_type, kolo_profiler)


def _mark_current_thread_as_kolo_worker() -> None:
    # sys.monitoring is interpreter-global, so a worker belonging to one trace
    # keeps running while a later trace records. Mark the native thread for
    # the rest of its life (including exception hooks and Timer waits): the
    # mark lives in the per-thread hook state the Rust monitor and profiler
    # already read first on every event, so it costs them nothing.
    try:
        from ._kolo import set_current_thread_kolo_worker
    except ImportError:  # pragma: no cover - PyPy and source-only installs
        pass
    else:
        set_current_thread_kolo_worker(True)
    # sys.setprofile profilers are per-thread. Dropping the Kolo profiler
    # threading.setprofile installed for this worker keeps the pure-Python
    # profiler (which has no per-event worker check) off it. Anyone else's
    # profiler stays.
    profiler = sys.getprofile()
    # Detection must never cost the worker its job either.
    is_kolo = False
    with contextlib.suppress(Exception):
        is_kolo = profiler is not None and _is_kolo_profiler(profiler)
    if not is_kolo:
        return
    try:
        sys.setprofile(None)
    except Exception as e:  # e.g. an audit hook denying sys.setprofile
        # The worker's own job matters more than keeping it out of a trace,
        # so not even a failing log handler may stop it.
        with contextlib.suppress(Exception):
            logger.warning(
                "Kolo could not stop profiling its own %s thread, so it may "
                "appear in the trace: %r",
                threading.current_thread().name,
                e,
            )


def _forget_worker_mark_after_fork() -> None:
    # A forked child's only thread is its main thread, even when a Kolo
    # worker forked (e.g. from an on_trace_ready callback): Kolo must trace
    # it again, so clear the native mark and the pure-Python monitor's
    # marker on the Thread object threading keeps for it.
    # It never calls threading.current_thread(), which applications may
    # wrap: by now threading has re-registered the child's only thread.
    with contextlib.suppress(Exception):
        try:
            from ._kolo import _reset_thread_hooks_after_fork
        except ImportError:  # PyPy and source-only installs
            pass
        else:
            _reset_thread_hooks_after_fork()
    with contextlib.suppress(Exception):
        active = getattr(threading, "_active", {})
        current = active.get(threading.get_ident())
        if getattr(current, KOLO_WORKER_THREAD_MARKER, False):
            setattr(current, KOLO_WORKER_THREAD_MARKER, False)


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_forget_worker_mark_after_fork)


class _KoloWorkerThread(threading.Thread):
    def run(self) -> None:
        _mark_current_thread_as_kolo_worker()
        super().run()


class _KoloWorkerTimer(threading.Timer):
    def run(self) -> None:
        _mark_current_thread_as_kolo_worker()
        super().run()


def kolo_worker_thread(
    target: Callable[..., Any],
    *,
    name: str,
    daemon: bool,
    args: tuple = (),
) -> threading.Thread:
    """Create (but don't start) a Thread for Kolo's own background work."""
    thread = _KoloWorkerThread(target=target, args=args, name=name, daemon=daemon)
    setattr(thread, KOLO_WORKER_THREAD_MARKER, True)
    return thread


def kolo_worker_timer(
    delay: float,
    target: Callable[..., Any],
    *,
    name: str,
    daemon: bool,
    args: tuple = (),
) -> threading.Timer:
    """Create (but don't start) a Timer for Kolo's own background work."""
    timer = _KoloWorkerTimer(delay, target, args=args)
    timer.name = name
    timer.daemon = daemon
    setattr(timer, KOLO_WORKER_THREAD_MARKER, True)
    return timer


def get_thread_id(thread):  # pragma: no cover
    native_id = getattr(thread, "native_id", None)
    ident = getattr(thread, "ident", None)

    if native_id:
        return f"native_{native_id}"
    elif ident:
        return f"ident_{ident}"
    else:
        print(f"Kolo warning: thread has no id: {getattr(thread, 'name', 'unknown')}")
        return "no_thread_id"
