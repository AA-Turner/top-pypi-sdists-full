from __future__ import annotations

import atexit
import os
import sys
import threading
import time
import types
from collections.abc import Mapping
from contextvars import Context, ContextVar, copy_context
from functools import partial, wraps
from inspect import (
    CO_ITERABLE_COROUTINE,
    isasyncgenfunction,
    iscoroutinefunction,
    isgeneratorfunction,
)
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol, TypeVar, overload

from . import _platform_info
from .config import load_config
from .db import setup_db
from .serialize import monkeypatch_queryset_repr
from .threads import kolo_worker_thread, kolo_worker_timer

if TYPE_CHECKING:
    from .profiler import KoloProfiler

    if sys.version_info >= (3, 12):
        from .monitoring import KoloMonitor
    else:
        KoloMonitor = Any

logger = __import__("logging").getLogger("kolo")

_auto_emit_lock = threading.Lock()
_auto_emit_last_spawn: float = 0.0
_AUTO_EMIT_COOLDOWN_SECONDS: float = 0.5
_auto_emit_followup_timer: threading.Timer | None = None
_auto_emit_pending_db_paths: list[Path | None] = []
# Emit subprocesses we spawned and haven't reaped yet. An emit killed before it
# releases emit.lock (e.g. SIGKILL at its CPU limit) stays a zombie until we
# reap it, and a zombie's PID still looks alive to _lock_holder_alive, which
# would suppress every later spawn until the lock's one-hour backstop.
_auto_emit_children: list[Any] = []
_auto_emit_children_lock = threading.Lock()

# Lock to prevent TOCTOU race condition during activation.
# Without this, two concurrent requests could both pass the _is_already_active()
# check before either claims the sys.monitoring tool ID, causing a ValueError.
_activation_lock = threading.Lock()

# Enters whose exit cannot simply end the session, innermost last. A decorator
# reuses one Enabled instance for every call, so a recursive call's exit must
# not end the session the outermost call started. Kept per context, so that
# threads and asyncio tasks sharing an instance each pair their own enters
# and exits.
_nested_enters: ContextVar[tuple[tuple[Enabled, bool], ...]] = ContextVar(
    "kolo_nested_enters", default=()
)

# The profiler session of each thread, as (enabled, profiler). A profiler
# traces only the thread that started it, so threads sharing an Enabled
# instance each keep, and later end, their own.
_profiler_sessions = threading.local()


def _end_orphaned_profiler_session() -> None:
    """End this thread's profiler session if its owner finished elsewhere.

    Only this thread can clear its profile hook, so a session whose owner
    finished on another thread waits here for the thread's next activation.
    """
    session = getattr(_profiler_sessions, "session", None)
    if session is None:
        return
    enabled, profiler = session
    if profiler.orphaned:
        enabled._deactivate()


def _leave_to_wrapper(agen: object) -> None:
    """Finalizer of an async generator that kolo.enable's wrapper closes."""


def _release_idle_kolo_tool() -> None:
    """Release the sys.monitoring tool Kolo keeps armed between sessions.

    For activations that will not start a monitoring session on it, so its
    idle callbacks do not outlive the sessions that use them.
    """
    if sys.version_info < (3, 12):
        return
    from .monitoring import (  # type: ignore[attr-defined]
        kolo_tool_is_idle,
        release_kolo_tool,
    )

    if kolo_tool_is_idle():
        release_kolo_tool()


def save_trace_in_thread(
    profiler,
    auto_emit: bool = False,
    db_path: Path | None = None,
    on_trace_ready: Callable[[str], None] | None = None,
):
    def save_then_emit():
        profiler.save()
        if on_trace_ready is not None:
            on_trace_ready(profiler.trace_id)
        # Spawn subprocess AFTER save completes, so the trace is in the DB
        if auto_emit:
            _spawn_auto_emit(db_path=db_path)

    if _platform_info.machine() == "wasm32":  # pragma: no cover
        save_then_emit()
    else:
        _run_on_save_worker(save_then_emit)


SAVE_WORKER_THREAD_NAME = "kolo-save_trace_in_db"
SAVE_WORKER_REUSED_MARKER = "_kolo_reused_save_worker"

# Save workers stay non-daemon, receive submitter context, and are discarded after fork; pending-save waits skip linger.
_SAVE_WORKER_LINGER_SECONDS = 0.02
# A worker stops waiting for further saves once it is this old, so that under
# a steady stream of saves a join of it still returns.
_SAVE_WORKER_MAX_AGE_SECONDS = 1.0


class _SaveWorker:
    __slots__ = ("job", "wake")

    def __init__(self, job: Callable[[], None]) -> None:
        self.job: Callable[[], None] | None = job
        # Held while the worker has no job; released to hand it one.
        self.wake = threading.Lock()
        self.wake.acquire()


def _stop_save_worker() -> None:
    """The job that tells a waiting save worker to exit."""


_save_workers_lock = threading.Lock()
_save_workers_changed = threading.Condition(_save_workers_lock)
_save_workers_idle: list[_SaveWorker] = []
_save_workers_pending = 0
# Bumped in a forked child, where the parent's workers and saves do not exist.
_save_workers_generation = 0
_save_workers_pid = os.getpid()
_save_workers_linger: bool | None = (
    False if os.environ.get("KOLO_REUSE_SAVE_WORKERS") == "0" else None
)


def _forget_save_workers_of_another_process() -> None:
    if _save_workers_pid != os.getpid():
        # Forked without Python's fork hooks running: the workers, and
        # whoever held the lock, are the parent's.
        _reset_save_workers_after_fork()


def _stop_idle_save_workers() -> None:
    """Runs when threading shuts down, before it joins its threads."""
    global _save_workers_linger

    _forget_save_workers_of_another_process()
    with _save_workers_lock:
        _save_workers_linger = False
        idle = list(_save_workers_idle)
        _save_workers_idle.clear()
        for worker in idle:
            worker.job = _stop_save_worker
            worker.wake.release()


def _enable_save_worker_linger() -> bool:
    register = getattr(threading, "_register_atexit", None)
    if register is None:  # pragma: no cover - Python 3.8
        return False
    try:
        register(_stop_idle_save_workers)
    except RuntimeError:  # pragma: no cover - threading is shutting down
        return False
    return True


def _reset_save_workers_after_fork() -> None:
    global _save_workers_lock, _save_workers_changed, _save_workers_idle
    global _save_workers_pending, _save_workers_generation, _save_workers_pid

    _save_workers_pid = os.getpid()
    # Another thread of the parent may have held the lock during the fork.
    _save_workers_lock = threading.Lock()
    _save_workers_changed = threading.Condition(_save_workers_lock)
    _save_workers_idle = []
    _save_workers_pending = 0
    _save_workers_generation += 1


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_save_workers_after_fork)


def _save_worker_main(worker: _SaveWorker, generation: int) -> None:
    global _save_workers_pending

    job = worker.job
    started = time.monotonic()
    while True:
        assert job is not None
        worker.job = None
        try:
            job()
        except BaseException:
            _forget_save_workers_of_another_process()
            with _save_workers_lock:
                if generation == _save_workers_generation:
                    _save_workers_pending -= 1
                    _save_workers_changed.notify_all()
            raise
        _forget_save_workers_of_another_process()
        with _save_workers_lock:
            if generation != _save_workers_generation:
                return
            # In one step, so whoever waited for this save finds the worker
            # ready for the next.
            _save_workers_pending -= 1
            _save_workers_changed.notify_all()
            if (
                not _save_workers_linger
                or time.monotonic() - started >= _SAVE_WORKER_MAX_AGE_SECONDS
            ):
                return
            _save_workers_idle.append(worker)
        if not worker.wake.acquire(timeout=_SAVE_WORKER_LINGER_SECONDS):
            with _save_workers_lock:
                if generation != _save_workers_generation:
                    return
                if worker.job is None:
                    _save_workers_idle.remove(worker)
                    return
            # Handed a job as the wait ran out: take the wake-up it sent.
            worker.wake.acquire()
        job = worker.job
        if job is _stop_save_worker:
            return


def _in_new_thread_context(job: Callable[[], None]) -> Callable[[], None]:
    """``job``, run in the context variables a thread started now would see."""
    if getattr(sys.flags, "thread_inherit_context", False):
        context = copy_context()
    else:
        context = Context()

    def run_in_context() -> None:
        context.run(job)

    return run_in_context


def _run_on_save_worker(job: Callable[[], None]) -> None:
    global _save_workers_pending, _save_workers_linger

    job = _in_new_thread_context(job)
    _forget_save_workers_of_another_process()
    with _save_workers_lock:
        if _save_workers_linger is None:
            _save_workers_linger = _enable_save_worker_linger()
        _save_workers_pending += 1
        if _save_workers_idle:
            worker = _save_workers_idle.pop()
            worker.job = job
            worker.wake.release()
            return
        generation = _save_workers_generation
    worker = _SaveWorker(job)
    # daemon=False explicitly: Thread inherits the daemon flag, and CPython won't wait for a daemon
    # save at shutdown, re-exposing the C-extension-teardown race.
    thread = kolo_worker_thread(
        _save_worker_main,
        name=SAVE_WORKER_THREAD_NAME,
        daemon=False,
        args=(worker, generation),
    )
    setattr(thread, SAVE_WORKER_REUSED_MARKER, True)
    try:
        thread.start()
    except BaseException:
        with _save_workers_lock:
            if generation == _save_workers_generation:
                _save_workers_pending -= 1
                _save_workers_changed.notify_all()
        raise


def wait_for_pending_saves(timeout: float | None = None) -> bool:
    """Wait until every trace handed to a save worker has been saved.

    Returns False if ``timeout`` (seconds) ran out first. Joining the
    ``kolo-save_trace_in_db`` threads waits for the same saves, but a worker
    stays around briefly for the next one, so the join returns later.
    """
    _forget_save_workers_of_another_process()
    with _save_workers_lock:
        return _save_workers_changed.wait_for(
            lambda: _save_workers_pending == 0, timeout
        )


def _build_emit_subprocess_kwargs(db_path: Path | None) -> dict[str, Any]:
    import os
    import subprocess

    env = os.environ.copy()
    # Use the system local timezone in the subprocess. Django often sets
    # TZ=UTC, which would otherwise leak into emitted folder timestamps.
    env.pop("TZ", None)
    # Prevent the auto-emit subprocess from tracing itself when KOLO=1 is set.
    # Belt-and-suspenders: disable tracing and remove activation triggers.
    env["KOLO_DISABLE"] = "1"
    env.pop("KOLO", None)

    if db_path is not None:
        env["KOLO_PATH"] = str(db_path.parent.parent.parent)

    popen_kwargs: dict[str, Any] = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "env": env,
    }

    if sys.platform == "win32":  # pragma: no cover
        # CREATE_NO_WINDOW, not DETACHED_PROCESS: venv launcher shims relaunch python.exe, which would
        # open a visible console. The flags are mutually exclusive.
        CREATE_NO_WINDOW = 0x08000000
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        popen_kwargs["creationflags"] = CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True
        popen_kwargs["close_fds"] = True

    return popen_kwargs


def _emit_in_flight(db_path: Path | None) -> bool:
    """Return True if a live emit already holds emit.lock for db_path's store.

    Used to skip spawning a redundant emit subprocess. "In flight" uses the same
    live-holder predicate the single-flight lock itself uses, so it can't diverge
    from the lock's actual lifetime (no separate grace window). When db_path is
    None we can't resolve the lock path, so we don't skip (the in-process
    single-flight lock still bounds concurrency).
    """
    if db_path is None:
        return False
    from ._emit_auto import _lock_holder_alive

    return _lock_holder_alive(db_path.parent / "emit.lock")


def _spawn_auto_emit_subprocess(db_path: Path | None) -> None:
    import subprocess

    with _auto_emit_children_lock:
        # poll() reaps exited children.
        _auto_emit_children[:] = [p for p in _auto_emit_children if p.poll() is None]

        if _emit_in_flight(db_path):
            logger.debug("Skipping auto-emit spawn: an emit is already in flight")
            return

        try:
            child = subprocess.Popen(
                [sys.executable, "-m", "kolo._emit_auto"],
                **_build_emit_subprocess_kwargs(db_path),
            )
        except (OSError, ValueError) as e:
            logger.debug("Failed to spawn auto-emit subprocess: %s", e)
            return
        _auto_emit_children.append(child)


def _schedule_auto_emit_followup_locked(delay: float, db_path: Path | None) -> None:
    global _auto_emit_followup_timer

    if db_path not in _auto_emit_pending_db_paths:
        _auto_emit_pending_db_paths.append(db_path)

    if _auto_emit_followup_timer is not None and _auto_emit_followup_timer.is_alive():
        return

    # Do not inherit a daemon request thread here. A throttled follow-up still
    # needs to survive shutdown long enough to run or be flushed synchronously.
    timer = kolo_worker_timer(
        delay, _run_auto_emit_followup, name="kolo-auto-emit-followup", daemon=False
    )
    _auto_emit_followup_timer = timer
    timer.start()


def _drain_auto_emit_followup_locked() -> list[Path | None]:
    global _auto_emit_followup_timer

    pending_db_paths = list(_auto_emit_pending_db_paths)
    _auto_emit_pending_db_paths.clear()
    _auto_emit_followup_timer = None
    return pending_db_paths


def _run_auto_emit_followup() -> None:
    import time

    global _auto_emit_last_spawn

    with _auto_emit_lock:
        pending_db_paths = _drain_auto_emit_followup_locked()
        if not pending_db_paths:
            return
        _auto_emit_last_spawn = time.monotonic()

    for db_path in pending_db_paths:
        _spawn_auto_emit_subprocess(db_path)


def _flush_auto_emit_followup_on_shutdown() -> None:
    timer: threading.Timer | None

    with _auto_emit_lock:
        timer = _auto_emit_followup_timer
        if timer is not None:
            timer.cancel()
        pending_db_paths = _drain_auto_emit_followup_locked()

    if timer is not None:
        timer.join()

    for db_path in pending_db_paths:
        _spawn_auto_emit_subprocess(db_path)


atexit.register(_flush_auto_emit_followup_on_shutdown)


def _spawn_auto_emit(db_path: Path | None = None) -> None:
    """
    Spawn a subprocess to auto-emit the latest traces.

    This runs `python -m kolo._emit_auto` in a completely separate process,
    ensuring zero impact on the Django process (no GIL, no shared memory).
    The subprocess is fire-and-forget - we don't wait for it to complete.

    Uses a lightweight entry point that avoids importing heavy dependencies
    (httpx, click, django) for faster subprocess startup.

    Throttled to max once per 500ms to prevent fork-bombing under high load.
    Cooldown hits schedule one trailing follow-up so a burst still gets a
    final reconciliation after the cooldown window closes.

    If db_path is provided, KOLO_PATH is set in the subprocess environment
    so setup_db() resolves to the same .kolo directory the trace was saved
    to (important when the caller passed an explicit _db_path override).
    """
    import time

    global _auto_emit_followup_timer, _auto_emit_last_spawn

    if _platform_info.machine() == "wasm32":  # pragma: no cover
        from ._emit_auto import auto_emit

        try:
            auto_emit(db_path=db_path)
        except Exception:
            logger.debug("auto-emit failed", exc_info=True)
        return

    if not sys.executable:
        logger.debug(
            "Cannot spawn auto-emit: sys.executable is not set (embedded Python?)"
        )
        return

    db_paths_to_spawn = [db_path]

    with _auto_emit_lock:
        now = time.monotonic()
        elapsed = now - _auto_emit_last_spawn
        if elapsed < _AUTO_EMIT_COOLDOWN_SECONDS:
            logger.debug("Deferring auto-emit spawn: cooldown active")
            _schedule_auto_emit_followup_locked(
                _AUTO_EMIT_COOLDOWN_SECONDS - elapsed, db_path
            )
            return

        if _auto_emit_pending_db_paths:
            db_paths_to_spawn = list(_auto_emit_pending_db_paths)
            _auto_emit_pending_db_paths.clear()
            if db_path not in db_paths_to_spawn:
                db_paths_to_spawn.append(db_path)

        if _auto_emit_followup_timer is not None:
            _auto_emit_followup_timer.cancel()
            _auto_emit_followup_timer = None

        _auto_emit_last_spawn = now

    for pending_db_path in db_paths_to_spawn:
        _spawn_auto_emit_subprocess(pending_db_path)


def upload_trace_in_thread(
    profiler,
    upload_token,
    on_trace_ready: Callable[[str], None] | None = None,
):
    def upload():
        import httpx

        trace = profiler.build_trace()
        if on_trace_ready is not None:
            on_trace_ready(profiler.trace_id)
        try:
            from .upload import upload_to_dashboard

            response = upload_to_dashboard(trace, upload_token)
            response.raise_for_status()
        except httpx.HTTPError:
            logger.exception("Failed to upload trace to Kolo dashboard.")

    if _platform_info.machine() == "wasm32":  # pragma: no cover
        upload()
    else:
        name = "kolo-upload_to_dashboard"
        kolo_worker_thread(
            upload, name=name, daemon=threading.current_thread().daemon
        ).start()


class Enabled:
    """
    User-facing context manager and decorator for Kolo profiling.

    This class is used via kolo.enable() and can be used as:
    - Context manager: with kolo.enable(): ...
    - Decorator: @kolo.enable or @kolo.enable(config={...})

    Only one session runs at a time. An enable entered while a session is
    already running joins it: its config and name are ignored, it neither
    starts nor ends a trace, and the outermost enable keeps owning the session.

    A decorated coroutine function is traced from its first step until it
    returns. A decorated generator or async generator function is traced from
    its first item until it is exhausted, closed or garbage collected, which
    includes the code its consumer runs between items. Whether it starts a
    session or joins a running one is decided once, at its first item.

    For automatic .pth file activation, use _AutoEnabled instead.
    """

    def __init__(
        self,
        config: Mapping[str, Any] | None,
        source: str,
        one_trace_per_test: bool,
        save_in_thread: bool,
        upload_token: Optional[str],
        db_path: Optional[Path] = None,
        name: Optional[str] = None,
        inline: bool = False,
        inline_returns: bool = False,
    ):
        if config is None:
            config = {}
        self.config = load_config(config)
        self._monitor: Optional[KoloMonitor] = None
        self.source = source
        self.one_trace_per_test = one_trace_per_test
        self.save_in_thread = save_in_thread
        self.upload_token = upload_token
        self.db_path = db_path
        self.name = name
        self.trace_id: Optional[str] = None
        self.inline = inline
        self.inline_returns = inline_returns

    @property
    def _profiler(self) -> Optional[KoloProfiler]:
        session = getattr(_profiler_sessions, "session", None)
        if session is None or session[0] is not self:
            return None
        return session[1]

    @_profiler.setter
    def _profiler(self, profiler: Optional[KoloProfiler]) -> None:
        if profiler is not None:
            _profiler_sessions.session = (self, profiler)
        elif self._profiler is not None:
            _profiler_sessions.session = None

    def __call__(self, func):
        # The session lives in the wrapper's frame, not _nested_enters: a generator can be resumed
        # or finalized from a different context than the one that started it.
        if iscoroutinefunction(func):

            @wraps(func)
            async def coroutine_inner(*args, **kwargs):
                session = self._start_session()
                try:
                    return await func(*args, **kwargs)
                finally:
                    self._end_session(session)

            return coroutine_inner

        if isasyncgenfunction(func):

            @wraps(func)
            async def async_generator_inner(*args, **kwargs):
                session = self._start_session()
                try:
                    agen = func(*args, **kwargs)
                    # Only the wrapper is loop-registered; during loop shutdown or GC finalization it closes the inner generator itself.
                    hooks = sys.get_asyncgen_hooks()
                    sys.set_asyncgen_hooks(None, _leave_to_wrapper)
                    try:
                        first = agen.__anext__()
                    finally:
                        sys.set_asyncgen_hooks(*hooks)
                    try:
                        value = await first
                        while True:
                            try:
                                sent = yield value
                            except BaseException as exc:
                                value = await agen.athrow(exc)
                            else:
                                value = await agen.asend(sent)
                    except StopAsyncIteration:
                        return
                finally:
                    self._end_session(session)

            return async_generator_inner

        if isgeneratorfunction(func):

            @wraps(func)
            def generator_inner(*args, **kwargs):
                session = self._start_session()
                try:
                    return (yield from func(*args, **kwargs))
                finally:
                    self._end_session(session)

            function = func
            while isinstance(function, partial):
                function = function.func
            code = getattr(function, "__code__", None)
            if code is not None and code.co_flags & CO_ITERABLE_COROUTINE:
                # A generator-based coroutine has to stay awaitable.
                return types.coroutine(generator_inner)
            return generator_inner

        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return inner

    def _start_session(self) -> Any:
        """Start a session for a decorated coroutine or generator.

        Returns the session to pass to _end_session, or None when the
        function joined a running session and has nothing to end.
        """
        if not self._activate():
            return None
        profiler = self._profiler
        return self._monitor if profiler is None else profiler

    def _end_session(self, session: Any) -> None:
        if session is None:
            return
        if session is self._monitor or session is self._profiler:
            self._deactivate(*sys.exc_info())
            return
        # Only reachable with the profiler: its session can only be ended
        # from the thread it traces, and this thread may have its own.
        if not session.thread.is_alive():
            session.__exit__()
            session.save()
            if self.config.get("auto_emit", True):
                _spawn_auto_emit(db_path=session.db_path)
            return
        session.orphaned = True
        logger.warning(
            "A function decorated with kolo.enable (%s) finished on a "
            "different thread than it started on. The thread it started on "
            "stays traced, and its trace unsaved, until that thread next "
            "uses kolo.enable.",
            self.source,
        )

    def _is_already_active(self) -> bool:
        """
        Check if Kolo profiling/monitoring is already active.

        This checks multiple sources:
        - sys.monitoring (Python 3.12+)
        - sys.getprofile()
        - threading.getprofile() (Python < 3.12)

        Returns:
            True if profiling is active, False otherwise
        """
        default_use_monitoring = sys.version_info >= (3, 12)
        use_monitoring = self.config.get("use_monitoring", default_use_monitoring)

        if sys.version_info >= (3, 12):
            from .monitoring import (  # type: ignore[attr-defined]
                KOLO_TOOL_ID,
                kolo_tool_is_idle,
            )

            tool_name = sys.monitoring.get_tool(KOLO_TOOL_ID)  # type: ignore[attr-defined]
            if tool_name and not (tool_name == "kolo" and kolo_tool_is_idle()):
                if use_monitoring:
                    if tool_name != "kolo":
                        logger.warning(
                            "Tool ID %d is in use by %r (expected 'kolo'). "
                            "Another tool may be using Kolo's reserved tool ID.",
                            KOLO_TOOL_ID,
                            tool_name,
                        )
                    return True
                # A running monitoring session also blocks an enable asking
                # for the profiler, which would otherwise trace alongside it.
                # A tool ID Kolo could not release has no events and does not.
                if tool_name == "kolo" and sys.monitoring.get_events(KOLO_TOOL_ID):  # type: ignore[attr-defined]
                    return True

        if sys.getprofile() is not None:
            return True

        if sys.version_info < (3, 12) or not use_monitoring:
            try:
                thread_profiler = threading.getprofile()  # type: ignore[attr-defined]
            except AttributeError:
                thread_profiler = threading._profile_hook
            if thread_profiler:
                return True

        return False

    def _activate(self) -> bool:
        """
        Internal activation logic.

        Activates Kolo profiling/monitoring. If already active, logs a message
        and returns early.

        Uses a lock to prevent TOCTOU race conditions where two threads could
        both pass the _is_already_active() check before either claims the
        sys.monitoring tool ID.

        Returns:
            True if activation succeeded, False if already active or failed.
        """
        with _activation_lock:
            _end_orphaned_profiler_session()
            if self._is_already_active():
                _release_idle_kolo_tool()
                logger.debug(
                    "Kolo already active, skipping duplicate activation from %s",
                    self.source,
                )
                return False

            try:
                from ._kolo import writer_circuit_open
            except ImportError:  # pragma: no cover - PyPy and source-only installs
                pass
            else:
                if writer_circuit_open():
                    _release_idle_kolo_tool()
                    logger.warning(
                        "Cannot activate Kolo: the trace writer circuit breaker "
                        "is open. Restart the process to resume tracing."
                    )
                    return False

            # Resolve once (absolute) so _deactivate uses the same path if cwd/KOLO_PATH change; not on
            # self.db_path so reused instances (the decorator) re-resolve each call.
            if self.db_path is not None:
                self._active_db_path = self.db_path.resolve()
            else:
                self._active_db_path = setup_db()
            db_path = self._active_db_path

            monkeypatch_queryset_repr()

            default_use_monitoring = sys.version_info >= (3, 12)
            use_monitoring = self.config.get("use_monitoring", default_use_monitoring)
            if sys.version_info >= (3, 12) and use_monitoring:
                from .monitoring import activate_monitoring

                monitor = self.register_monitor(db_path)
                if activate_monitoring(monitor):
                    self._monitor = monitor
                    self.trace_id = monitor.trace_id
                else:
                    return False
            else:
                from .profiler import KoloProfiler

                _release_idle_kolo_tool()
                profiler = KoloProfiler(
                    db_path,
                    config=self.config,
                    source=self.source,
                    one_trace_per_test=self.one_trace_per_test,
                    name=self.name,
                )
                self._profiler = profiler
                profiler.__enter__()
                self.trace_id = profiler.trace_id

            return True

    def __enter__(self):
        activated = self._activate()
        nested = _nested_enters.get()
        # An enter that started a session is only recorded when an earlier
        # enter of this instance is waiting on its exit, to tell them apart.
        if not activated or any(enabled is self for enabled, _ in nested):
            _nested_enters.set((*nested, (self, activated)))
        return self

    def register_monitor(self, db_path):
        if self.config.get("use_rust", True):
            try:
                from ._kolo import register_monitor
            except ImportError as e:  # pragma: no cover
                logger.debug("Rust monitor import failed (%s), using Python monitor", e)
            else:
                return register_monitor(
                    str(db_path),
                    config=self.config,
                    source=self.source,
                    one_trace_per_test=self.one_trace_per_test,
                    name=self.name,
                )

        from .monitoring import KoloMonitor  # type: ignore[attr-defined]

        return KoloMonitor(
            db_path,
            config=self.config,
            source=self.source,
            one_trace_per_test=self.one_trace_per_test,
            name=self.name,
        )

    @property
    def _save_sync(self) -> bool:
        """Whether this Enabled instance should save synchronously.

        Inline output reads the trace by id from the db immediately after
        deactivation, so a background save would race against it and
        produce either a missing trace or TraceNotFoundError. We force
        synchronous save whenever the caller asked for inline output.
        """
        return not self.save_in_thread or self.inline

    def save_trace_profiler(self):
        assert self._profiler is not None

        if self.one_trace_per_test:
            return

        if self._save_sync:
            self._profiler.save()
            self.trace_id = self._profiler.trace_id
            return

        if self.upload_token:
            upload_trace_in_thread(
                self._profiler,
                self.upload_token,
                on_trace_ready=self._set_trace_id,
            )
        else:
            auto_emit = self.config.get("auto_emit", True)
            save_trace_in_thread(
                self._profiler,
                auto_emit=auto_emit,
                db_path=self._active_db_path,
                on_trace_ready=self._set_trace_id,
            )

    def save_trace_monitor(self):
        assert self._monitor is not None

        if self.one_trace_per_test:
            return

        if self._save_sync:
            self._monitor.save()
            self.trace_id = self._monitor.trace_id
            return

        if self.upload_token:
            upload_trace_in_thread(
                self._monitor,
                self.upload_token,
                on_trace_ready=self._set_trace_id,
            )
        else:
            auto_emit = self.config.get("auto_emit", True)
            save_trace_in_thread(
                self._monitor,
                auto_emit=auto_emit,
                db_path=self._active_db_path,
                on_trace_ready=self._set_trace_id,
            )

    def _set_trace_id(self, trace_id: str) -> None:
        self.trace_id = trace_id

    def _deactivate(self, *exc) -> None:
        """
        Internal deactivation logic.

        Deactivates profiling/monitoring, saves traces, and handles inline output.
        """
        did_deactivate = False
        trace_abandoned = False

        if self._profiler is not None:
            self._profiler.__exit__(*exc)
            rust_profiler = self._profiler.rust_profiler
            trace_abandoned = rust_profiler is not None and rust_profiler.panicked
            if not trace_abandoned:
                self.save_trace_profiler()
            self._profiler = None
            did_deactivate = True

        if self._monitor is not None:
            from .monitoring import disable_monitoring  # type: ignore[attr-defined]

            disable_monitoring(self._monitor)
            trace_abandoned = getattr(self._monitor, "panicked", False)
            if not trace_abandoned:
                self.save_trace_monitor()
            self._monitor = None
            did_deactivate = True

        if trace_abandoned:
            self.trace_id = None

        if did_deactivate and self._save_sync and not trace_abandoned:
            if self.config.get("auto_emit", True):
                _spawn_auto_emit(db_path=self._active_db_path)

        if self.inline and did_deactivate and not trace_abandoned:
            assert self.trace_id is not None
            self._output_inline_trace()

    def __exit__(self, *exc) -> None:
        nested = _nested_enters.get()
        for index in range(len(nested) - 1, -1, -1):
            enabled, activated = nested[index]
            if enabled is self:
                _nested_enters.set(nested[:index] + nested[index + 1 :])
                if not activated:
                    return
                break
        self._deactivate(*exc)

    def _output_inline_trace(self):
        """Output the compact trace representation to stderr."""
        import click

        from .cli_mcp_shared import get_compact_traces

        assert self._active_db_path is not None
        db_path = self._active_db_path

        results = get_compact_traces(
            db_path,
            trace_id=self.trace_id,
            returns=self.inline_returns,
        )
        if results:
            trace_id, compact_repr = results[0]
            click.echo(compact_repr, err=True)


class _AutoEnabled:
    """
    Internal class for automatic .pth file activation.

    Not a context manager - uses explicit activate/cleanup methods.
    Designed for one-way activation with atexit cleanup.

    This class should only be used internally for KOLO=1 auto-activation.
    User code should use the Enabled context manager instead.
    """

    def __init__(
        self,
        config: Mapping[str, Any] | None,
        source: str,
        one_trace_per_test: bool,
        save_in_thread: bool,
        upload_token: Optional[str],
        db_path: Optional[Path] = None,
        name: Optional[str] = None,
        inline: bool = False,
        inline_returns: bool = False,
    ):
        self._enabled = Enabled(
            config=config,
            source=source,
            one_trace_per_test=one_trace_per_test,
            save_in_thread=save_in_thread,
            upload_token=upload_token,
            db_path=db_path,
            name=name,
            inline=inline,
            inline_returns=inline_returns,
        )
        self._activated = False
        self.trace_id: Optional[str] = None

    def activate(self) -> bool:
        """
        Activate Kolo profiling.

        Returns:
            True if activation succeeded, False if already active or failed
        """
        if self._enabled._is_already_active():
            logger.debug("KOLO=1: Tracing already active, skipping auto-activation")
            return False

        if not self._enabled._activate():
            return False

        self._activated = True

        self.trace_id = self._enabled.trace_id

        return True

    def cleanup(self) -> None:
        """
        Cleanup and save trace.

        Called by atexit handler. Includes error handling to prevent
        crashes during interpreter shutdown.
        """
        if not self._activated:
            return

        try:
            self._enabled._deactivate(None, None, None)
            if self._enabled.trace_id is None:
                self.trace_id = None
                return
            if self._enabled.config.get("auto_emit", True):
                self._print_kolotxt_path()
        except Exception as e:  # pragma: no cover
            import sys

            print(f"Kolo cleanup error during shutdown: {e}", file=sys.stderr)
            import traceback

            traceback.print_exc(file=sys.stderr)

    def _print_kolotxt_path(self):
        """
        Print the kolo.txt path to stderr.

        Note: kolo.txt is updated by the auto-emit subprocess spawned in
        _deactivate(). The file may not exist yet (subprocess is
        fire-and-forget), but it will be created shortly.
        """
        assert self._enabled._active_db_path is not None
        kolotxt_path = self._enabled._active_db_path.parent.parent / "kolo.txt"
        print(
            f"\nTrace captured using KOLO=1\n{kolotxt_path.absolute()}",
            file=sys.stderr,
        )


F = TypeVar("F", bound=Callable[..., Any])


class CallableContextManager(Protocol):
    def __call__(self, func: F) -> F: ...  # pragma: no cover

    def __enter__(self) -> None: ...  # pragma: no cover

    def __exit__(self, *exc) -> None: ...  # pragma: no cover


@overload
def enable(_func: F) -> F:
    """Stub"""


@overload
def enable(
    config: Mapping[str, Any] | None = None,
    name: Optional[str] = None,
    source: str = "kolo.enable",
    _one_trace_per_test: bool = False,
    _save_in_thread: bool = True,
    _upload_token: Optional[str] = None,
    _db_path: Optional[Path] = None,
    _inline: bool = False,
    _inline_returns: bool = False,
) -> CallableContextManager:
    """Stub"""


def enable(
    config=None,
    *,
    name=None,
    source="kolo.enable",
    _one_trace_per_test=False,
    _save_in_thread=True,
    _upload_token=None,
    _db_path=None,
    _inline=False,
    _inline_returns=False,
):
    if config is None or isinstance(config, Mapping):
        function = None
    else:
        # Treat as a decorator called on a function
        function = config
        config = None

    enabled = Enabled(
        config=config,
        source=source,
        name=name,
        one_trace_per_test=_one_trace_per_test,
        save_in_thread=_save_in_thread,
        upload_token=_upload_token,
        db_path=_db_path,
        inline=_inline,
        inline_returns=_inline_returns,
    )

    if function is None:
        return enabled
    return enabled(function)


enabled = enable
