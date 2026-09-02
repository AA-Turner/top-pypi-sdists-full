import atexit
import dis
import logging
import os
import platform
import queue as _queue
import sys
import threading
import time
from collections import defaultdict
from typing import Callable, List, Optional, Tuple

import msgpack
import ulid

from .config import (
    CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE,
    resolve_flush_subtree_bytes as _resolve_flush_subtree_bytes,
)
from .db import save_v3_trace_chunks
from .filters.core import LibraryPathFilter
from .filters.kolo import kolo_filter_filename
from .git import COMMIT_SHA
from .plugins import PluginProcessor, load_plugin_data
from .serialize import (
    FramePathCache,
    dump_msgpack,
    dump_msgpack_lightweight_repr,
    user_code_call_site,
)
from .subtree_flush import TRACKING_PROBE_INTERVAL, SubtreeFlushTracker
from .threads import get_thread_id
from .trace_container import iter_v3_trace_chunks
from .utils import extract_http_trace_name, extract_test_trace_name
from .version import __version__

logger = logging.getLogger("kolo")

# Kolo uses tool ID 3 for sys.monitoring (Python 3.12+).
# IDs 0-2 and 5 are reserved for debuggers, coverage, profilers, and optimizers.
# Kolo is a tracing/observability tool, so we use an unassigned ID to avoid
# conflicts with traditional profilers (cProfile, django-debug-toolbar, etc).
KOLO_TOOL_ID = 3
SUBTREE_STACK_EVENTS = frozenset(
    {"call", "return", "resume", "yield", "unwind", "throw"}
)


def frozen_filter(filename):
    return "<frozen " in filename


def pypy_filter(filename):
    return "<builtin>/" in filename


def exec_filter(filename):
    return filename == "<string>"


def attrs_filter(filename):
    if filename:
        return filename.startswith("<attrs generated")
    else:  # pragma: no cover
        # Index of the frame in the Python stack:
        # 0: This function
        # 1: KoloMonitor.ignore method
        # 2: KoloMonitor.monitor_ method
        # 3: Attrs code with empty filename
        # 4: Attrs code that may match attr/_make.py
        # 5: Attrs code that may match attr/_make.py
        frame = sys._getframe(4)
        if frame is not None and frame.f_code.co_filename == "":
            frame = sys._getframe(5)
        return frame is not None and frame.f_code.co_filename.endswith(
            os.path.normpath("attr/_make.py")
        )


def pytest_filter(filename):
    return filename == "<pytest match expression>"


def build_frame_data(
    event,
    name,
    frame,
    frame_id,
    call_site,
    *,
    path,
    omit_return_locals=False,
):
    if omit_return_locals:
        frame_locals = None
    else:
        frame_locals = {k: v for k, v in frame.f_locals.items() if k != "__builtins__"}
    return {
        "path": path,
        "co_name": name,
        "qualname": get_qualname(frame),
        "event": event,
        "frame_id": frame_id,
        "locals": frame_locals,
        "timestamp": time.time(),
        "type": "frame",
        "user_code_call_site": call_site,
    }


def get_qualname(frame):
    qualname = frame.f_code.co_qualname
    module = frame.f_globals.get("__name__", "<unknown>")
    return f"{module}.{qualname}"


# --- async trace-point save worker --------------------------------------
#
# Trace points (functions configured in ``trace_points.on_return``) are
# saved off the calling thread on a single long-lived worker. The steady
# state is still async and cheap: the calling thread snapshots the frame
# slice and enqueues a job; the worker unpacks frames, builds the trace,
# writes sqlite + emits, and signals completion via
# ``_trace_point_save_pending``.
#
# Reliability matters more than preserving async-only behavior when the
# worker is unhealthy. If the worker is unavailable, saturated, or dies,
# the trace-point callback falls back to inline save/replay on the
# calling thread instead of silently dropping the trace or wedging the
# pending counter. The async path is therefore the fast path, not the
# only path.
#
# Process crash can still lose not-yet-finished work. The worker thread
# is daemonized so a truly wedged save path doesn't pin interpreter
# shutdown forever.
#
# **In-flight pending counter.** ``_trace_point_save_pending`` is bumped
# at the *very first line* of the trace-point entry points
# (``KoloMonitor._save_trace_point`` and ``_save_trace_point_from_rust``).
# That closes a race
# where a return callback already in flight when ``disable_monitoring``
# runs would miss the drain (which only saw queued jobs) and then escape
# teardown. With the early bump, the drain blocks until every callback
# has either successfully enqueued or synchronously finished/released its
# slot.

_TRACE_POINT_SAVE_LOCK = threading.RLock()
_TRACE_POINT_SAVE_COND = threading.Condition(_TRACE_POINT_SAVE_LOCK)
_TRACE_POINT_SAVE_QUEUE_MAXSIZE = 1024
TracePointSaveJob = Tuple[Callable[..., object], Tuple[object, ...]]


class _TracePointSaveWorker:
    def __init__(self, monitor, generation: int):
        self.monitor = monitor
        self.generation = generation
        self.queue: "_queue.Queue" = _queue.Queue(
            maxsize=_TRACE_POINT_SAVE_QUEUE_MAXSIZE
        )
        self.stop_requested = threading.Event()
        self.started = threading.Event()
        self.stopped = threading.Event()
        self.ready = False
        self.accepting_jobs = True
        self.thread = threading.Thread(
            target=_trace_point_save_worker_main,
            name=f"kolo-trace-point-save-{generation}",
            daemon=True,
            args=(self,),
        )


_trace_point_save_worker: Optional[_TracePointSaveWorker] = None
_trace_point_save_generation = 0
_trace_point_save_pending = 0
_trace_point_save_atexit_registered = threading.Event()


def _begin_pending_trace_point_save() -> None:
    """Bump the pending counter on the calling thread.

    Must be the first thing the trace-point entry point does, before any
    Python work that could yield the GIL. The drain in
    ``disable_monitoring`` waits for this counter to hit zero, so a
    callback that has begun must always pair its bump with a finish
    (either via the worker after the job runs, or inline if the worker
    path is unavailable).
    """
    global _trace_point_save_pending
    with _TRACE_POINT_SAVE_COND:
        _trace_point_save_pending += 1


def _finish_pending_trace_point_save() -> None:
    global _trace_point_save_pending
    with _TRACE_POINT_SAVE_COND:
        _trace_point_save_pending -= 1
        if _trace_point_save_pending <= 0:
            _trace_point_save_pending = 0
            _TRACE_POINT_SAVE_COND.notify_all()


def wait_for_trace_point_saves(timeout: Optional[float] = None) -> bool:
    """Block until every trace point started so far has been processed.

    Returns True if the drain completed cleanly, False if it timed out.
    Used by tests (so they can read the DB after a tracked call) and by
    ``disable_monitoring`` (so reactivation doesn't race a stale worker).
    """
    deadline = None if timeout is None else time.monotonic() + timeout
    while True:
        with _TRACE_POINT_SAVE_COND:
            if _trace_point_save_pending <= 0:
                return True

            replay_jobs = _recover_unhealthy_trace_point_save_worker_locked(
                "kolo trace-point save drain detected an unhealthy worker."
            )
            if replay_jobs:
                replay_timeout = (
                    None
                    if deadline is None
                    else max(
                        deadline - time.monotonic(),
                        0.0,
                    )
                )
            elif deadline is None:
                _TRACE_POINT_SAVE_COND.wait()
                continue
            else:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return False
                _TRACE_POINT_SAVE_COND.wait(timeout=remaining)
                continue

        if not _wait_for_trace_point_save_replay(
            replay_jobs,
            "kolo trace-point save drain switched to inline replay.",
            replay_timeout,
        ):
            return False


def _configure_trace_point_save_worker(pinned_monitor) -> None:
    if pinned_monitor is None:
        return

    rust_suspend = getattr(pinned_monitor, "set_suspend_hooks", None)
    if rust_suspend is not None:
        rust_suspend(True)

    thread_locals = getattr(pinned_monitor, "thread_locals", None)
    if thread_locals is not None:
        thread_locals.is_saving = True


def _drain_trace_point_save_jobs(
    worker: _TracePointSaveWorker,
) -> List[TracePointSaveJob]:
    jobs: List[TracePointSaveJob] = []
    while True:
        try:
            jobs.append(worker.queue.get_nowait())
        except _queue.Empty:
            return jobs


def _run_trace_point_save_inline(worker_fn, args) -> None:
    monitor = getattr(worker_fn, "__self__", None)
    thread_locals = getattr(monitor, "thread_locals", None)
    if thread_locals is None:
        worker_fn(*args)
        return

    was_saving = thread_locals.is_saving
    thread_locals.is_saving = True
    try:
        worker_fn(*args)
    finally:
        thread_locals.is_saving = was_saving


def _replay_trace_point_save_jobs(jobs: List[TracePointSaveJob], reason: str) -> None:
    if not jobs:
        return

    logger.warning("%s Replaying %d queued saves inline.", reason, len(jobs))
    for worker_fn, args in jobs:
        try:
            _run_trace_point_save_inline(worker_fn, args)
        except (GeneratorExit, KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            logger.debug("inline trace point replay failed", exc_info=True)
        finally:
            _finish_pending_trace_point_save()


def _wait_for_trace_point_save_replay(
    jobs: List[TracePointSaveJob],
    reason: str,
    timeout: Optional[float],
) -> bool:
    if not jobs:
        return True
    if timeout is None:
        _replay_trace_point_save_jobs(jobs, reason)
        return True

    replay_thread = threading.Thread(
        target=_replay_trace_point_save_jobs,
        name="kolo-trace-point-replay",
        daemon=True,
        args=(jobs, reason),
    )
    replay_thread.start()
    replay_thread.join(timeout=timeout)
    return not replay_thread.is_alive()


def _recover_unhealthy_trace_point_save_worker_locked(
    reason: str,
) -> List[TracePointSaveJob]:
    global _trace_point_save_worker

    worker = _trace_point_save_worker
    if worker is None:
        return []
    if worker.accepting_jobs and worker.ready and worker.thread.is_alive():
        return []

    _trace_point_save_worker = None
    worker.accepting_jobs = False
    worker.stop_requested.set()
    jobs = _drain_trace_point_save_jobs(worker)
    if jobs:
        logger.warning(
            "%s Recovering %d queued saves from worker generation %d.",
            reason,
            len(jobs),
            worker.generation,
        )
    elif not worker.thread.is_alive():
        logger.warning(
            "kolo trace-point save worker generation %d exited unexpectedly;"
            " future saves will run inline until the next activation cycle.",
            worker.generation,
        )
    return jobs


def _recover_crashed_trace_point_save_worker(
    worker: _TracePointSaveWorker,
) -> List[TracePointSaveJob]:
    global _trace_point_save_worker

    with _TRACE_POINT_SAVE_LOCK:
        if _trace_point_save_worker is worker:
            _trace_point_save_worker = None
        worker.accepting_jobs = False
        worker.stop_requested.set()
        return _drain_trace_point_save_jobs(worker)


def _trace_point_save_worker_main(worker: _TracePointSaveWorker) -> None:
    """Long-lived worker body, pinned to the monitor that spawned it.

    Spawned by ``activate_monitoring`` BEFORE ``sys.monitoring.set_events``
    arms callbacks. That ordering matters: spawning after the monitor is
    active pumps bytecodes through ``Thread.start`` / ``Event.wait`` /
    ``threading._bootstrap`` that fire monitor callbacks on the new
    thread before the worker has suspended hooks on itself, which under
    rapid trace-point load has been observed to deadlock
    ``Thread.start().wait()`` against the main thread.
    """
    global _trace_point_save_worker

    try:
        _configure_trace_point_save_worker(worker.monitor)
        worker.ready = True
        worker.started.set()

        while True:
            try:
                if worker.stop_requested.is_set():
                    try:
                        job = worker.queue.get_nowait()
                    except _queue.Empty:
                        return
                else:
                    job = worker.queue.get(timeout=0.1)
            except _queue.Empty:
                continue

            worker_fn, args = job
            try:
                worker_fn(*args)
            except (GeneratorExit, KeyboardInterrupt, SystemExit):
                raise
            except BaseException:
                logger.debug("async trace point save failed", exc_info=True)
            finally:
                _finish_pending_trace_point_save()
    except Exception:
        logger.warning(
            "kolo trace-point save worker generation %d crashed;"
            " queued saves will be replayed inline.",
            worker.generation,
            exc_info=True,
        )
        jobs = _recover_crashed_trace_point_save_worker(worker)
        _replay_trace_point_save_jobs(
            jobs,
            f"kolo trace-point save worker generation {worker.generation} crashed.",
        )
    except (GeneratorExit, KeyboardInterrupt, SystemExit):
        logger.warning(
            "kolo trace-point save worker generation %d crashed;"
            " queued saves will be replayed inline.",
            worker.generation,
            exc_info=True,
        )
        jobs = _recover_crashed_trace_point_save_worker(worker)
        _replay_trace_point_save_jobs(
            jobs,
            f"kolo trace-point save worker generation {worker.generation} crashed.",
        )
        raise
    finally:
        worker.started.set()
        worker.stopped.set()


def _ensure_trace_point_save_worker(pinned_monitor) -> None:
    """Spawn a fresh worker thread for this activation cycle.

    Called from ``activate_monitoring`` BEFORE ``sys.monitoring.set_events``
    arms callbacks. The previous cycle's worker (if any) is asked to stop
    and joined; we wait briefly so the cross-cycle handoff is clean. A
    failed handoff (worker won't stop) is logged but not fatal — the new
    worker is already up.
    """
    global _trace_point_save_generation, _trace_point_save_worker

    _trace_point_save_generation += 1
    new_worker = _TracePointSaveWorker(pinned_monitor, _trace_point_save_generation)
    with _TRACE_POINT_SAVE_LOCK:
        old_worker = _trace_point_save_worker
        _trace_point_save_worker = new_worker
    new_worker.thread.start()
    new_worker.started.wait(timeout=5.0)
    if not new_worker.ready or not new_worker.thread.is_alive():
        with _TRACE_POINT_SAVE_LOCK:
            if _trace_point_save_worker is new_worker:
                _trace_point_save_worker = None
            new_worker.accepting_jobs = False
            new_worker.stop_requested.set()
        logger.warning(
            "kolo trace-point save worker generation %d failed to start cleanly;"
            " saves will run inline until the next activation cycle.",
            new_worker.generation,
        )

    if old_worker is not None:
        old_worker.accepting_jobs = False
        old_worker.stop_requested.set()
        old_worker.thread.join(timeout=5.0)
        if old_worker.thread.is_alive():
            replay_jobs: List[TracePointSaveJob] = []
            if getattr(old_worker, "queue", None) is not None:
                replay_jobs = _drain_trace_point_save_jobs(old_worker)
            logger.warning(
                "kolo trace-point save worker from previous activation cycle"
                " did not exit within 5s. The old worker may still be running"
                " against its pinned monitor."
            )
            if replay_jobs:
                _replay_trace_point_save_jobs(
                    replay_jobs,
                    "kolo trace-point save worker from previous activation cycle"
                    " could not finish queued saves before handoff.",
                )


def _stop_trace_point_save_worker() -> None:
    """Request shutdown of the active worker and join it.

    Called from ``disable_monitoring`` after the drain. Idempotent: a
    no-op when no worker is running. Always nulls out the global worker
    handle so the next ``activate_monitoring`` cycle starts from a clean
    slate. Logs a warning if the worker fails to exit within the join
    timeout — surfacing wedged sqlite/emit so async-only failures
    aren't silent.
    """
    global _trace_point_save_worker
    with _TRACE_POINT_SAVE_LOCK:
        worker = _trace_point_save_worker
        if worker is None:
            return
        _trace_point_save_worker = None
        worker.accepting_jobs = False
        worker.stop_requested.set()
    if worker.thread.is_alive():
        worker.thread.join(timeout=5.0)
        if worker.thread.is_alive():
            logger.warning(
                "kolo trace-point save worker did not exit within 5s of"
                " disable_monitoring; sqlite or emit may be wedged."
            )


def _route_trace_point_save(fn, args) -> Tuple[bool, List[TracePointSaveJob]]:
    with _TRACE_POINT_SAVE_LOCK:
        replay_jobs = _recover_unhealthy_trace_point_save_worker_locked(
            "kolo trace-point save worker became unavailable."
        )
        worker = _trace_point_save_worker
        if worker is None:
            logger.debug(
                "trace-point save submitted with no active worker; saving inline"
            )
            return False, replay_jobs

        try:
            worker.queue.put_nowait((fn, args))
            return True, replay_jobs
        except _queue.Full:
            logger.warning(
                "kolo trace-point save queue full (maxsize=%d); saving inline."
                " Async saves are saturated — slower sqlite or higher trace"
                " point cadence than the worker can keep up with.",
                _TRACE_POINT_SAVE_QUEUE_MAXSIZE,
            )
            return False, replay_jobs


def _enqueue_trace_point_save(worker_fn, build_args) -> None:
    args = None
    replay_jobs: List[TracePointSaveJob] = []
    submitted = False
    try:
        args = build_args()
        submitted, replay_jobs = _route_trace_point_save(worker_fn, args)
        if replay_jobs:
            _replay_trace_point_save_jobs(
                replay_jobs,
                "kolo trace-point save worker unavailable.",
            )
        if submitted:
            return
        _run_trace_point_save_inline(worker_fn, args)
    finally:
        if not submitted:
            _finish_pending_trace_point_save()


def _ensure_trace_point_atexit() -> None:
    with _TRACE_POINT_SAVE_LOCK:
        if _trace_point_save_atexit_registered.is_set():
            return
        _trace_point_save_atexit_registered.set()

    def _atexit_drain():
        if not wait_for_trace_point_saves(timeout=5.0):
            logger.debug(
                "kolo trace-point drain at process exit timed out;"
                " some saves may be lost."
            )
        _stop_trace_point_save_worker()

    atexit.register(_atexit_drain)


# --- end async trace-point save worker ----------------------------------
def _registered_current_thread():
    """Return the current Thread without creating a ``_DummyThread``.

    ``sys.monitoring`` can invoke Kolo while ``Thread._bootstrap`` is still
    running, before CPython registers the new thread in ``threading._active``.
    Calling ``threading.current_thread()`` in that window manufactures a
    ``_DummyThread``. On Python 3.13, retaining that dummy until interpreter
    shutdown also emits a noisy ``_DeleteDummyThreadOnDel`` exception.

    ``threading.enumerate()`` only returns real thread objects already known to
    the module (active or starting), so it lets us recognize Kolo's marked save
    worker without creating a synthetic thread. A starting thread becomes
    matchable as soon as CPython assigns its identifier; until then we retry.
    """
    current_ident = threading.get_ident()
    return next(
        (thread for thread in threading.enumerate() if thread.ident == current_ident),
        None,
    )


class KoloLocals(threading.local):
    def __init__(self):
        from .core import _TRACE_SAVE_THREAD_MARKER

        self.call_frames = []
        self._frame_ids = {}
        self.line_frame = None
        self.line_frame_data = None
        self.variable = None
        self.opname = None
        current_thread = _registered_current_thread()
        self._save_thread_marker_checked = current_thread is not None
        self.is_saving = bool(
            current_thread is not None
            and getattr(current_thread, _TRACE_SAVE_THREAD_MARKER, False)
        )

    def is_saving_subtrace(self):
        """Resolve the save-thread marker once CPython registers the thread."""
        if self.is_saving or self._save_thread_marker_checked:
            return self.is_saving

        current_thread = _registered_current_thread()
        if current_thread is None:
            return False

        from .core import _TRACE_SAVE_THREAD_MARKER

        self._save_thread_marker_checked = True
        self.is_saving = bool(getattr(current_thread, _TRACE_SAVE_THREAD_MARKER, False))
        return self.is_saving


class InstructionCache:
    """Session-scoped assignment metadata indexed by code object and offset."""

    def __init__(self):
        # Each entry stores its code object strongly beside the identity key. This
        # prevents identity reuse and bounds metadata to one monitoring session.
        self._codes = {}

    def get(self, code, offset):
        code_id = id(code)
        try:
            _, filename, name, instructions = self._codes[code_id]
        except KeyError:
            instructions = {}
            for instruction in dis.get_instructions(code):
                if instruction.opname not in (
                    "STORE_FAST",
                    "STORE_GLOBAL",
                    "STORE_DEREF",
                ):
                    continue
                variable = instruction.argval
                if variable is not None and variable.startswith("@"):
                    continue
                instructions[instruction.offset] = (instruction.opname, variable)
            filename = code.co_filename
            name = code.co_name
            self._codes[code_id] = code, filename, name, instructions

        cached_instruction = instructions.get(offset)
        if cached_instruction is None:
            return None
        opname, variable = cached_instruction
        return filename, name, opname, variable


if sys.version_info >= (3, 12):
    PY_START = sys.monitoring.events.PY_START
    PY_RETURN = sys.monitoring.events.PY_RETURN
    PY_UNWIND = sys.monitoring.events.PY_UNWIND
    PY_RESUME = sys.monitoring.events.PY_RESUME
    PY_YIELD = sys.monitoring.events.PY_YIELD
    PY_THROW = sys.monitoring.events.PY_THROW
    INSTRUCTION = sys.monitoring.events.INSTRUCTION
    NO_EVENTS = sys.monitoring.events.NO_EVENTS
    FLUSH_THREAD_NAME = "kolo-flush_trace"

    class KoloMonitor:
        def __init__(
            self,
            db_path,
            *,
            config=None,
            one_trace_per_test=False,
            source,
            name: Optional[str] = None,
        ):
            self.tool_id = KOLO_TOOL_ID
            self.active = False
            self.timestamp = None
            self.db_path = db_path
            self.config = config if config is not None else {}
            self.source = source
            self.one_trace_per_test = one_trace_per_test
            self.omit_return_locals = self.config.get("omit_return_locals", False)
            self._explicit_trace_name = name
            self.flush_subtree_bytes = _resolve_flush_subtree_bytes(self.config)
            self.root_trace_id = f"trc_{ulid.new()}"
            self.trace_id = self.root_trace_id
            self.trace_name = name
            self._subtree_flush = SubtreeFlushTracker(self.flush_subtree_bytes)
            self._subtree_stack = self._subtree_flush.subtree_stack
            self._thread_cumulative_bytes = self._subtree_flush.thread_cumulative_bytes
            self._flush_in_progress = self._subtree_flush.flush_in_progress
            self._subtree_flush_lock = threading.RLock()

            filters = self.config.get("filters", {})
            self.include_frames = [
                os.path.normpath(f) for f in filters.get("include_frames", [])
            ]
            self.ignore_frames = [
                os.path.normpath(f) for f in filters.get("ignore_frames", [])
            ]

            self.default_include_frames = {}
            for plugin_data in load_plugin_data(self.config):
                processor = PluginProcessor(plugin_data, self.config)
                for co_name in plugin_data["co_names"]:
                    self.default_include_frames.setdefault(co_name, []).append(
                        processor
                    )

            self.default_ignore_frames = [
                LibraryPathFilter().filter,
                frozen_filter,
                pypy_filter,
                kolo_filter_filename,
                exec_filter,
                attrs_filter,
                pytest_filter,
            ]
            self.thread_locals = KoloLocals()
            self.line_events = self.config.get("line_events", False)
            self._instruction_cache = InstructionCache()

            current_thread = threading.current_thread()
            self._current_thread = current_thread
            self._current_thread_ident = current_thread.ident
            self._thread_state_lock_required = self.one_trace_per_test

            # Key is the thread id, value is a list of frames for that thread
            self.frames_by_thread = defaultdict(list)

            self.current_thread_id = get_thread_id(current_thread)
            self._frame_paths = FramePathCache()
            # Key is the thread id, value is the native python thread object
            self.threads = {}
            if self.config.get("lightweight_repr", False):
                self.dump_msgpack = dump_msgpack_lightweight_repr
            else:
                self.dump_msgpack = dump_msgpack

            # Trace points: save a standalone trace when one of the configured
            # functions returns. Each invocation of a listed function produces
            # its own top-level trace — Kolo's way of extracting discrete units
            # of work (HTTP requests, tests, library calls, etc.) out of a
            # broader run.
            trace_point_config = self.config.get("trace_points", {})
            self._trace_point_return_targets = set(
                trace_point_config.get("on_return", [])
            )
            # thread_id -> stack of frame-list start indices
            self._trace_point_markers: dict[str, list[int]] = {}

        def _build_trace_meta(self):
            config = {
                k: v
                for k, v in self.config.items()
                if k not in CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE
            }
            config["use_monitoring"] = True
            config["use_rust"] = False

            return {
                "version": __version__,
                "source": self.source,
                "environment": {
                    "py_version": platform.python_version(),
                    "py_version_full": sys.version,
                    "platform": platform.platform(),
                    "system": platform.system(),
                    "machine": platform.machine(),
                    "processor": platform.processor(),
                },
                "config": config,
            }

        def ignore(self, filename):
            for ignore in self.default_ignore_frames:
                if ignore(filename):
                    return True
            return False

        def include(self, processor, event, filename, name, arg):
            try:
                if not processor.matches(filename, name):
                    return None

                # Index of the frame in the Python stack:
                # 0: This method
                # 1: KoloMonitor.monitor_ method
                # 2: The frame we want
                frame = sys._getframe(2)
                if processor.call_extra is not None and not processor.call_extra(
                    frame, event, arg, processor.context
                ):
                    return None

                return processor.process(
                    frame, event, arg, self.thread_locals.call_frames
                )
            except Exception as e:
                logger.warning(
                    "Unexpected exception in default_include_frames: %s",
                    processor,
                    exc_info=e,
                )
                return None

        def start_test(self):
            with self._subtree_flush_lock:
                self.trace_id = f"trc_{ulid.new()}"
                self.root_trace_id = self.trace_id
                self.trace_name = self._explicit_trace_name
                self.start_test_indices = {
                    thread_id: len(frames)
                    for thread_id, frames in self.frames_by_thread.items()
                }
                self._subtree_flush.reset(self.frames_by_thread)
                self._trace_point_markers.clear()

        def end_test(self):
            with self._subtree_flush_lock:
                frames_by_thread = {
                    thread_id: list(frames[self.start_test_indices.get(thread_id, 0) :])
                    for thread_id, frames in self.frames_by_thread.items()
                }
            self.save(frames_by_thread=frames_by_thread)
            with self._subtree_flush_lock:
                self._subtree_flush.reset(self.frames_by_thread)
                self._trace_point_markers.clear()

        def monitor_pystart(self, code, instruction_offset):  # pragma: no cover
            if self._is_saving_subtrace():
                return
            if self.thread_locals.opname is not None:
                self.process_assignment()

            filename = code.co_filename
            name = code.co_name

            frames = []
            frame_types = []
            appended_target_frame = False

            try:
                if name in self.default_include_frames:
                    processors = self.default_include_frames[name]
                    for processor in processors:
                        frame_data = self.include(
                            processor, "call", filename, name, None
                        )
                        if frame_data is not None:
                            frames.append(frame_data)
                            frame_types.append(frame_data["type"])

                for path in self.include_frames:
                    if path in filename:
                        frames.append(self.process_pystart(filename, name))
                        frame_types.append("frame")
                        appended_target_frame = True
                        return

                if self.ignore(filename):
                    if frames:
                        return  # Don't disable if a default processor matched
                    return sys.monitoring.DISABLE

                for path in self.ignore_frames:
                    if path in filename:
                        if frames:
                            return  # Don't disable if a default processor matched
                        return sys.monitoring.DISABLE

                frames.append(self.process_pystart(filename, name))
                frame_types.append("frame")
                appended_target_frame = True
            finally:
                self.push_frames_call(frames, frame_types)

                if (
                    self._trace_point_return_targets
                    and name in self._trace_point_return_targets
                    and appended_target_frame
                ):
                    thread_id = get_thread_id(threading.current_thread())
                    self._push_trace_point_marker(thread_id)

        def monitor_pyreturn(
            self, code, instruction_offset, retval
        ):  # pragma: no cover
            if self._is_saving_subtrace():
                return
            if self.thread_locals.opname is not None:
                self.process_assignment()

            filename = code.co_filename
            name = code.co_name

            frames = []
            frame_types = []
            appended_target_frame = False
            is_trace_point_return = (
                bool(self._trace_point_return_targets)
                and name in self._trace_point_return_targets
            )
            defer_subtree_flush = (
                self.flush_subtree_bytes is not None and is_trace_point_return
            )

            try:
                if name in self.default_include_frames:
                    processors = self.default_include_frames[name]
                    for processor in processors:
                        frame_data = self.include(
                            processor, "return", filename, name, retval
                        )
                        if frame_data is not None:
                            frames.append(frame_data)
                            frame_types.append(frame_data["type"])

                for path in self.include_frames:
                    if path in filename:
                        frame_data = self.process_pyreturn(filename, name, retval)
                        if frame_data is not None:
                            frames.append(frame_data)
                            frame_types.append("frame")
                            appended_target_frame = True
                        return

                if self.ignore(filename):
                    if frames:
                        return  # Don't disable if a default processor matched
                    return sys.monitoring.DISABLE

                for path in self.ignore_frames:
                    if path in filename:
                        if frames:
                            return  # Don't disable if a default processor matched
                        return sys.monitoring.DISABLE

                frame_data = self.process_pyreturn(filename, name, retval)
                if frame_data is not None:
                    frames.append(frame_data)
                    frame_types.append("frame")
                    appended_target_frame = True
            finally:
                # A subtree flush can replace the tracked frame range with a
                # placeholder and invalidate its trace-point marker. Close the
                # subtree now, but defer the actual flush until the independent
                # trace-point snapshot has copied the complete range.
                # A pytest end_test processor owns its save/reset boundary and
                # must keep the existing inline-flush order instead of carrying
                # a candidate across that reset.
                defer_subtree_flush = (
                    defer_subtree_flush and "end_test" not in frame_types
                )
                self.push_frames_return(
                    frames,
                    frame_types,
                    defer_subtree_flush=defer_subtree_flush,
                )

                if is_trace_point_return and frames:
                    thread_id = get_thread_id(threading.current_thread())
                    try:
                        if appended_target_frame:
                            start = self._pop_trace_point_marker(thread_id)
                            if start is not None:
                                all_frames = self.frames_by_thread[thread_id]
                                trace_point_frames = list(all_frames[start:])
                                self._save_trace_point(
                                    thread_id,
                                    trace_point_frames,
                                    source=name,
                                    trace_name=name,
                                )
                    finally:
                        if defer_subtree_flush:
                            self._maybe_flush_segments(thread_id)

        def monitor_pyunwind(
            self, code, instruction_offset, exception
        ):  # pragma: no cover
            if self._is_saving_subtrace():
                return
            if self.thread_locals.opname is not None:
                self.process_assignment()

            filename = code.co_filename
            name = code.co_name

            frames = []
            frame_types = []
            appended_target_frame = False

            try:
                if name in self.default_include_frames:
                    processors = self.default_include_frames[name]
                    for processor in processors:
                        frame_data = self.include(
                            processor, "unwind", filename, name, exception
                        )
                        if frame_data is not None:
                            frames.append(frame_data)
                            frame_types.append(frame_data["type"])

                for path in self.include_frames:
                    if path in filename:
                        frame_data = self.process_pyunwind(filename, name, exception)
                        if frame_data is not None:
                            frames.append(frame_data)
                            frame_types.append("frame")
                            appended_target_frame = True
                        return

                if self.ignore(filename):
                    # We would like to return `sys.monitoring.DISABLE` here, but
                    # `PY_UNWIND` events cannot be disabled, so we do the next best
                    # thing and return asap.
                    return

                for path in self.ignore_frames:
                    if path in filename:
                        # We would like to return `sys.monitoring.DISABLE` here, but
                        # `PY_UNWIND` events cannot be disabled, so we do the next best
                        # thing and return asap.
                        return

                frame_data = self.process_pyunwind(filename, name, exception)
                if frame_data is not None:
                    frames.append(frame_data)
                    frame_types.append("frame")
                    appended_target_frame = True
            finally:
                self.push_frames_return(frames, frame_types)

                if (
                    self._trace_point_return_targets
                    and name in self._trace_point_return_targets
                    and appended_target_frame
                ):
                    thread_id = get_thread_id(threading.current_thread())
                    self._pop_trace_point_marker(thread_id)

        def monitor_pyresume(self, code, instruction_offset):  # pragma: no cover
            if self._is_saving_subtrace():
                return
            if self.thread_locals.opname is not None:
                self.process_assignment()

            filename = code.co_filename
            name = code.co_name

            frames = []
            frame_types = []

            try:
                if name in self.default_include_frames:
                    processors = self.default_include_frames[name]
                    for processor in processors:
                        frame_data = self.include(
                            processor, "resume", filename, name, None
                        )
                        if frame_data is not None:
                            frames.append(frame_data)
                            frame_types.append(frame_data["type"])

                for path in self.include_frames:
                    if path in filename:
                        frames.append(self.process_pyresume(filename, name))
                        frame_types.append("frame")
                        return

                if self.ignore(filename):
                    if frames:
                        return  # Don't disable if a default processor matched
                    return sys.monitoring.DISABLE

                for path in self.ignore_frames:
                    if path in filename:
                        if frames:
                            return  # Don't disable if a default processor matched
                        return sys.monitoring.DISABLE

                frames.append(self.process_pyresume(filename, name))
                frame_types.append("frame")
            finally:
                self.push_frames_call(frames, frame_types)

        def monitor_pyyield(self, code, instruction_offset, retval):  # pragma: no cover
            if self._is_saving_subtrace():
                return
            if self.thread_locals.opname is not None:
                self.process_assignment()

            filename = code.co_filename
            name = code.co_name

            frames = []
            frame_types = []

            try:
                if name in self.default_include_frames:
                    processors = self.default_include_frames[name]
                    for processor in processors:
                        frame_data = self.include(
                            processor, "yield", filename, name, retval
                        )
                        if frame_data is not None:
                            frames.append(frame_data)
                            frame_types.append(frame_data["type"])

                for path in self.include_frames:
                    if path in filename:
                        frame_data = self.process_pyyield(filename, name, retval)
                        if frame_data is not None:
                            frames.append(frame_data)
                            frame_types.append("frame")
                            return

                if self.ignore(filename):
                    if frames:
                        return  # Don't disable if a default processor matched
                    return sys.monitoring.DISABLE

                for path in self.ignore_frames:
                    if path in filename:
                        if frames:
                            return  # Don't disable if a default processor matched
                        return sys.monitoring.DISABLE

                frame_data = self.process_pyyield(filename, name, retval)
                if frame_data is not None:
                    frames.append(frame_data)
                    frame_types.append("frame")
            finally:
                self.push_frames_return(frames, frame_types)

        def monitor_pythrow(
            self, code, instruction_offset, exception
        ):  # pragma: no cover
            if self._is_saving_subtrace():
                return
            if self.thread_locals.opname is not None:
                self.process_assignment()

            filename = code.co_filename
            name = code.co_name

            frames = []
            frame_types = []

            try:
                if name in self.default_include_frames:
                    processors = self.default_include_frames[name]
                    for processor in processors:
                        frame_data = self.include(
                            processor, "throw", filename, name, exception
                        )
                        if frame_data is not None:
                            frames.append(frame_data)
                            frame_types.append(frame_data["type"])

                for path in self.include_frames:
                    if path in filename:
                        frames.append(self.process_pythrow(filename, name, exception))
                        frame_types.append("frame")
                        return

                if self.ignore(filename):
                    # We would like to return `sys.monitoring.DISABLE` here, but
                    # `PY_UNWIND` events cannot be disabled, so we do the next best
                    # thing and return asap.
                    return

                for path in self.ignore_frames:
                    if path in filename:
                        # We would like to return `sys.monitoring.DISABLE` here, but
                        # `PY_UNWIND` events cannot be disabled, so we do the next best
                        # thing and return asap.
                        return

                frames.append(self.process_pythrow(filename, name, exception))
                frame_types.append("frame")
            finally:
                self.push_frames_call(frames, frame_types)

        def monitor_instruction(self, code, instruction_offset):  # pragma: no cover
            if self._is_saving_subtrace():
                return
            if self.thread_locals.opname is not None:
                self.process_assignment()

            instruction = self._instruction_cache.get(code, instruction_offset)
            if instruction is None:
                return sys.monitoring.DISABLE
            filename, name, opname, variable = instruction

            for path in self.include_frames:
                if path in filename:
                    self.process_instruction(filename, name, opname, variable)
                    return

            if self.ignore(filename):
                return sys.monitoring.DISABLE

            for path in self.ignore_frames:
                if path in filename:
                    return sys.monitoring.DISABLE

            self.process_instruction(filename, name, opname, variable)

        def process_pystart(self, filename, name):  # pragma: no cover
            # Index of the frame in the Python stack:
            # 0: This function
            # 1: KoloMonitor.monitor_pystart method
            # 2: The frame we want
            frame = sys._getframe(2)
            frame_id = f"frm_{ulid.new()}"
            self.thread_locals._frame_ids[id(frame)] = frame_id

            user_code_call_site_ = user_code_call_site(
                self.thread_locals.call_frames, frame_id
            )

            self.thread_locals.call_frames.append((frame, frame_id))

            data = build_frame_data(
                "call",
                name,
                frame,
                frame_id,
                user_code_call_site_,
                path=self._frame_paths.format(frame),
            )
            data["arg"] = None
            return data

        def _end_frame(self, frame):  # pragma: no cover
            """Close a recorded frame without corrupting the active call stack."""
            frame_id = self.thread_locals._frame_ids.get(id(frame))
            if frame_id is None:
                return None

            call_frames = self.thread_locals.call_frames
            if not call_frames or call_frames[-1][1] != frame_id:
                return None

            call_site = user_code_call_site(call_frames, frame_id)
            call_frames.pop()
            return frame_id, call_site

        def process_pyreturn(self, filename, name, retval):  # pragma: no cover
            # Index of the frame in the Python stack:
            # 0: This function
            # 1: KoloMonitor.monitor_pyreturn method
            # 2: The frame we want
            frame = sys._getframe(2)
            end_frame = self._end_frame(frame)
            if end_frame is None:
                return None
            frame_id, user_code_call_site_ = end_frame

            data = build_frame_data(
                "return",
                name,
                frame,
                frame_id,
                user_code_call_site_,
                path=self._frame_paths.format(frame),
                omit_return_locals=self.omit_return_locals,
            )
            data["arg"] = retval
            return data

        def process_pyunwind(self, filename, name, exception):  # pragma: no cover
            # Index of the frame in the Python stack:
            # 0: This function
            # 1: KoloMonitor.monitor_pyunwind method
            # 2: The frame we want
            frame = sys._getframe(2)
            end_frame = self._end_frame(frame)
            if end_frame is None:
                return None
            frame_id, user_code_call_site_ = end_frame

            data = build_frame_data(
                "unwind",
                name,
                frame,
                frame_id,
                user_code_call_site_,
                path=self._frame_paths.format(frame),
            )
            data["exception"] = exception
            return data

        def process_pyresume(self, filename, name):  # pragma: no cover
            # Index of the frame in the Python stack:
            # 0: This function
            # 1: KoloMonitor.monitor_pyresume method
            # 2: The frame we want
            frame = sys._getframe(2)
            frame_id = f"frm_{ulid.new()}"
            self.thread_locals._frame_ids[id(frame)] = frame_id

            user_code_call_site_ = user_code_call_site(
                self.thread_locals.call_frames, frame_id
            )

            self.thread_locals.call_frames.append((frame, frame_id))

            data = build_frame_data(
                "resume",
                name,
                frame,
                frame_id,
                user_code_call_site_,
                path=self._frame_paths.format(frame),
            )
            data["arg"] = None
            return data

        def process_pyyield(self, filename, name, retval):  # pragma: no cover
            # Index of the frame in the Python stack:
            # 0: This function
            # 1: KoloMonitor.monitor_pyyield method
            # 2: The frame we want
            frame = sys._getframe(2)
            end_frame = self._end_frame(frame)
            if end_frame is None:
                return
            frame_id, user_code_call_site_ = end_frame

            data = build_frame_data(
                "yield",
                name,
                frame,
                frame_id,
                user_code_call_site_,
                path=self._frame_paths.format(frame),
                omit_return_locals=self.omit_return_locals,
            )
            data["arg"] = retval
            return data

        def process_pythrow(self, filename, name, exception):  # pragma: no cover
            # Index of the frame in the Python stack:
            # 0: This function
            # 1: KoloMonitor.monitor_pythrow method
            # 2: The frame we want
            frame = sys._getframe(2)
            frame_id = f"frm_{ulid.new()}"
            self.thread_locals._frame_ids[id(frame)] = frame_id

            user_code_call_site_ = user_code_call_site(
                self.thread_locals.call_frames, frame_id
            )

            self.thread_locals.call_frames.append((frame, frame_id))

            data = build_frame_data(
                "throw",
                name,
                frame,
                frame_id,
                user_code_call_site_,
                path=self._frame_paths.format(frame),
            )
            data["exception"] = exception
            return data

        def process_instruction(
            self, filename, name, opname, variable
        ):  # pragma: no cover
            # Index of the frame in the Python stack:
            # 0: This function
            # 1: KoloMonitor.monitor_instruction method
            # 2: The frame we want
            frame = sys._getframe(2)
            frame_id = self.thread_locals._frame_ids.get(id(frame))

            self.thread_locals.variable = variable
            self.thread_locals.opname = opname
            self.thread_locals.line_frame = frame
            self.thread_locals.line_frame_data = {
                "path": self._frame_paths.format(frame),
                "co_name": name,
                "qualname": get_qualname(frame),
                "event": "line",
                "frame_id": frame_id,
                "timestamp": time.time(),
                "type": "frame",
            }

        def process_assignment(self):  # pragma: no cover
            frame = self.thread_locals.line_frame
            variable = self.thread_locals.variable
            opname = self.thread_locals.opname
            frame_data = self.thread_locals.line_frame_data

            if opname == "STORE_FAST":
                frame_data["assign"] = (variable, frame.f_locals[variable])
            elif opname == "STORE_GLOBAL":
                frame_data["assign"] = (variable, frame.f_globals[variable])
            elif opname == "STORE_DEREF":  # nonlocal
                frame_data["assign"] = (variable, frame.f_locals[variable])

            self.push_frame_data(frame_data)

            self.thread_locals.line_frame = None
            self.thread_locals.variable = None
            self.thread_locals.opname = None
            self.thread_locals.line_frame_data = None

        def _low_water_bytes(self):
            return self._subtree_flush.low_water_bytes()

        def _select_flush_candidate(self, thread_id):
            return self._subtree_flush.select_flush_candidate(thread_id)

        def _shift_flush_state_after_flush(
            self, thread_id, *, start_index, end_index, resident_delta
        ):
            self._subtree_flush.shift_flush_state_after_flush(
                thread_id,
                start_index=start_index,
                end_index=end_index,
                resident_delta=resident_delta,
            )

        def _maybe_flush_segments(self, thread_id):
            if not self._subtree_flush.begin_flush(thread_id):
                return

            try:
                low_water_bytes = self._subtree_flush.low_water_bytes()
                while self._subtree_flush.current_bytes(thread_id) > low_water_bytes:
                    selected = self._select_flush_candidate(thread_id)
                    if selected is None:
                        break
                    owner, candidate = selected
                    if not self._flush_subtree(thread_id, owner, candidate):
                        break
            finally:
                self._subtree_flush.finish_flush(thread_id)

        def _snapshot_trace_inputs(self, frames_by_thread=None):
            with self._subtree_flush_lock:
                source = (
                    self.frames_by_thread
                    if frames_by_thread is None
                    else frames_by_thread
                )
                frames_snapshot = {
                    thread_id: list(frames) for thread_id, frames in source.items()
                }
                threads = dict(self.threads)
                trace_name = self._resolve_trace_name(frames_snapshot)
            return frames_snapshot, threads, trace_name

        def _append_frame_data(self, data):
            """Append a single frame to the per-thread buffer and update
            subtree-flush byte tracking.

            Shared hot-path helper used by both `push_frame_data` (the
            single-frame path that also records a closed leaf segment) and
            the batch push paths (`_push_frames_call_batch` /
            `_push_frames_return_batch`) that handle subtree bookkeeping
            themselves and do not want a per-frame closed-leaf entry.

            Returns the same 6-tuple shape that `push_frame_data` used to
            return: (thread_id, frame_start_index, frame_end_index,
            added_bytes, current_bytes, flush_tracking_armed).
            """
            if isinstance(data, dict):
                data = self.dump_msgpack(data)

            current_thread_ident = threading.get_ident()
            if (
                not self._thread_state_lock_required
                and current_thread_ident == self._current_thread_ident
            ):
                thread_id = self.current_thread_id
                if thread_id not in self.threads:
                    self.threads[thread_id] = self._current_thread
                thread_frames = self.frames_by_thread[thread_id]
                frame_start_index = len(thread_frames)
                thread_frames.append(data)
                frame_end_index = len(thread_frames)
            else:
                with self._subtree_flush_lock:
                    if current_thread_ident == self._current_thread_ident:
                        thread_id = self.current_thread_id
                        if thread_id not in self.threads:
                            self.threads[thread_id] = self._current_thread
                    else:
                        current_thread = threading.current_thread()
                        thread_id = get_thread_id(current_thread)
                        if thread_id not in self.threads:
                            self.threads[thread_id] = current_thread
                        self._thread_state_lock_required = True

                    thread_frames = self.frames_by_thread[thread_id]
                    frame_start_index = len(thread_frames)
                    thread_frames.append(data)
                    frame_end_index = len(thread_frames)

            if self.flush_subtree_bytes is None:
                return thread_id, frame_start_index, frame_end_index, 0, 0, False

            tracker = self._subtree_flush
            current_bytes = tracker.thread_cumulative_bytes.get(thread_id, 0)
            flush_tracking_armed = False
            added_bytes = 0
            frame_bytes = len(data)

            if (
                thread_id in tracker.flush_tracking_armed
                or tracker._tracking_start_bytes == 0
            ):
                added_bytes = frame_bytes
                current_bytes += added_bytes
                tracker.thread_cumulative_bytes[thread_id] = current_bytes
                tracker.flush_tracking_armed.add(thread_id)
                flush_tracking_armed = True
            else:
                current_bytes += frame_bytes
                tracker.thread_cumulative_bytes[thread_id] = current_bytes
                if current_bytes >= tracker._tracking_start_bytes:
                    added_bytes = frame_bytes
                    tracker.flush_tracking_armed.add(thread_id)
                    flush_tracking_armed = True
                else:
                    next_probe = tracker._next_tracking_probe.get(
                        thread_id,
                        TRACKING_PROBE_INTERVAL,
                    )
                    if frame_end_index >= next_probe:
                        tracker._probed_frame_index[thread_id] = frame_end_index
                        tracker._next_tracking_probe[thread_id] = (
                            frame_end_index + TRACKING_PROBE_INTERVAL
                        )

            return (
                thread_id,
                frame_start_index,
                frame_end_index,
                added_bytes,
                current_bytes,
                flush_tracking_armed,
            )

        def push_frame_data(self, data):
            if isinstance(data, dict):
                frame_data = data
            else:
                frame_data = msgpack.unpackb(data, strict_map_key=False)

            push_result = self._append_frame_data(data)

            if not push_result[5]:  # not flush_tracking_armed
                return push_result

            if frame_data.get("event") in SUBTREE_STACK_EVENTS:
                return push_result

            thread_id, frame_start_index, frame_end_index, added_bytes, _, _ = (
                push_result
            )
            self._subtree_flush.record_closed_segment(
                thread_id,
                start_index=frame_start_index,
                end_index=frame_end_index,
                resident_bytes=added_bytes,
                co_name=frame_data.get("co_name", "<unknown>"),
            )
            self._maybe_flush_segments(thread_id)
            return push_result

        def _flush_subtree(self, thread_id, owner, candidate):
            """Save a flushable closed segment and replace it with a placeholder."""
            with self._subtree_flush_lock:
                frames = self.frames_by_thread[thread_id]
                subtree_frames = list(
                    frames[candidate.start_index : candidate.end_index]
                )
                flushed_bytes = sum(len(frame) for frame in subtree_frames)
                subtrace_id = f"trc_{ulid.new()}"
                chunks = self._iter_subtree_trace_chunks(
                    thread_id, subtree_frames, subtrace_id
                )
                try:
                    self._save_subtrace_chunks(subtrace_id, chunks)
                except Exception:
                    logger.warning(
                        "Failed to save flushed subtree %s; leaving frames resident",
                        subtrace_id,
                        exc_info=True,
                    )
                    return False

                placeholder = {
                    "type": "subtree_flushed",
                    "frame_id": f"frm_{ulid.new()}",
                    "co_name": candidate.co_name,
                    "flushed_trace_id": subtrace_id,
                    "flushed_bytes": flushed_bytes,
                    "flushed_segment_count": candidate.segment_count,
                    "timestamp": time.time(),
                }
                placeholder_data = self.dump_msgpack(placeholder)

                del frames[candidate.start_index : candidate.end_index]
                frames.insert(candidate.start_index, placeholder_data)
                self._shift_trace_point_markers_after_flush(
                    thread_id,
                    start_index=candidate.start_index,
                    end_index=candidate.end_index,
                )
                resident_delta = len(placeholder_data) - flushed_bytes
                self._thread_cumulative_bytes[thread_id] += resident_delta

                self._subtree_flush.clear_flush_candidate(thread_id, owner)

                self._shift_flush_state_after_flush(
                    thread_id,
                    start_index=candidate.start_index,
                    end_index=candidate.end_index,
                    resident_delta=resident_delta,
                )
            return True

        def _is_saving_subtrace(self):
            # Bare returns avoid persisting save-path disable decisions globally.
            return self.thread_locals.is_saving_subtrace()

        def _save_subtrace_chunks(self, subtrace_id, chunks):
            # Runs under _subtree_flush_lock. The thread-local flag suppresses
            # sys.monitoring callbacks while save_trace() runs on this thread.
            timeout = self.config.get("sqlite_busy_timeout", 60)
            db_path = self.db_path

            if platform.machine() == "wasm32":  # pragma: no cover
                suspended_events = None
                if self.active:
                    suspended_events = (
                        PY_START
                        | PY_RETURN
                        | PY_UNWIND
                        | PY_RESUME
                        | PY_YIELD
                        | PY_THROW
                    )
                    if self.line_events:
                        suspended_events |= INSTRUCTION
                    sys.monitoring.set_events(self.tool_id, NO_EVENTS)
                    sys.monitoring.restart_events()

                try:
                    save_v3_trace_chunks(
                        subtrace_id,
                        chunks,
                        db_path=db_path,
                        ignore_errors=False,
                        timeout=timeout,
                    )
                finally:
                    if suspended_events is not None:
                        sys.monitoring.set_events(self.tool_id, suspended_events)
                        sys.monitoring.restart_events()
                return

            self.thread_locals.is_saving = True
            try:
                save_v3_trace_chunks(
                    subtrace_id,
                    chunks,
                    db_path=db_path,
                    ignore_errors=False,
                    timeout=timeout,
                )
            finally:
                self.thread_locals.is_saving = False

        def _iter_subtree_trace_chunks(self, thread_id, subtree_frames, subtrace_id):
            """Yield a trace payload from a subtree without joining it."""
            thread = self.threads.get(thread_id, threading.current_thread())
            trace_name = self._resolve_trace_name({thread_id: subtree_frames})
            return iter_v3_trace_chunks(
                command_line_args=sys.argv,
                current_commit_sha=COMMIT_SHA,
                current_thread_id=thread_id,
                meta=self._build_trace_meta(),
                timestamp=time.time(),
                trace_id=subtrace_id,
                trace_name=trace_name,
                root_trace_id=self.root_trace_id,
                threads={thread_id: thread},
                frames_by_thread={thread_id: subtree_frames},
            )

        def push_frames_call(self, frames, frame_types):
            if not frames:
                return

            if self.one_trace_per_test:
                for index, frame_type in enumerate(frame_types):
                    if frame_type == "start_test":
                        self._push_frames_call_batch(
                            frames[:index], frame_types[:index]
                        )
                        self.start_test()
                        self._push_frames_call_batch(
                            frames[index:], frame_types[index:]
                        )
                        return

            self._push_frames_call_batch(frames, frame_types)

        def push_frames_return(self, frames, frame_types, *, defer_subtree_flush=False):
            if not frames:
                return

            frames.reverse()
            frame_types.reverse()

            if self.one_trace_per_test:
                for index, frame_type in enumerate(frame_types):
                    if frame_type == "end_test":
                        self._push_frames_return_batch(
                            frames[: index + 1],
                            frame_types[: index + 1],
                            defer_subtree_flush=defer_subtree_flush,
                        )
                        self.end_test()
                        self._push_frames_return_batch(
                            frames[index + 1 :],
                            frame_types[index + 1 :],
                            defer_subtree_flush=defer_subtree_flush,
                        )
                        return

            self._push_frames_return_batch(
                frames,
                frame_types,
                defer_subtree_flush=defer_subtree_flush,
            )

        def _push_frames_call_batch(self, frames, frame_types):
            if not frames:
                return

            if self.flush_subtree_bytes is not None and "frame" in frame_types:
                batch_result = None
                batch_added_bytes = 0
                batch_start_index = None
                batch_co_name = None
                for offset, (frame_data, frame_type) in enumerate(
                    zip(frames, frame_types)
                ):
                    batch_result = self._append_frame_data(frame_data)
                    if not batch_result[5]:
                        continue
                    # If tracking arms mid-batch, only the suffix from the
                    # first armed frame onward belongs to the new open subtree.
                    if batch_start_index is None:
                        batch_start_index = batch_result[1]
                    if batch_co_name is None and frame_type == "frame":
                        batch_co_name = frame_data.get("co_name", "<unknown>")
                    batch_added_bytes += batch_result[3]
                if batch_result is None or batch_start_index is None:
                    return
                if batch_co_name is None:
                    batch_co_name = "<unknown>"
                self._subtree_flush.push_open_subtree(
                    batch_result[0],
                    start_index=batch_start_index,
                    start_bytes=max(0, batch_result[4] - batch_added_bytes),
                    co_name=batch_co_name,
                )
                self._maybe_flush_segments(batch_result[0])
                return

            for frame_data in frames:
                self.push_frame_data(frame_data)

        def _push_frames_return_batch(
            self, frames, frame_types, *, defer_subtree_flush=False
        ):
            if not frames:
                return

            if self.flush_subtree_bytes is not None and "frame" in frame_types:
                batch_result = None
                for frame_data in frames:
                    batch_result = self._append_frame_data(frame_data)

                if batch_result is None or not batch_result[5]:
                    return

                thread_id = batch_result[0]
                subtree = self._subtree_flush.pop_open_subtree(thread_id)
                if subtree is not None:
                    subtree_bytes = batch_result[4] - subtree.start_bytes
                    self._subtree_flush.record_closed_segment(
                        thread_id,
                        start_index=subtree.start_index,
                        end_index=batch_result[2],
                        resident_bytes=subtree_bytes,
                        co_name=subtree.co_name,
                    )

                if not defer_subtree_flush:
                    self._maybe_flush_segments(thread_id)
                return

            for frame_data in frames:
                self.push_frame_data(frame_data)

        def _push_trace_point_marker(self, thread_id):
            frames = self.frames_by_thread.get(thread_id)
            if not frames:
                return
            self._trace_point_markers.setdefault(thread_id, []).append(len(frames) - 1)

        def _pop_trace_point_marker(self, thread_id):
            markers = self._trace_point_markers.get(thread_id)
            if not markers:
                return None
            start = markers.pop()
            if not markers:
                self._trace_point_markers.pop(thread_id, None)
            return start

        def _shift_trace_point_markers_after_flush(
            self, thread_id, *, start_index, end_index
        ):
            """Fix up trace point markers after the byte-based flush drains frames.

            A range [start_index, end_index) is removed from
            frames_by_thread[thread_id] and replaced with a single placeholder.
            Any marker whose start index falls inside the drained range is
            invalid and must be dropped; markers past the range need to shift
            down to account for the placeholder.
            """
            markers = self._trace_point_markers.get(thread_id)
            if not markers:
                return
            shift = (end_index - start_index) - 1
            new_markers = []
            for marker in markers:
                if marker < start_index:
                    new_markers.append(marker)
                elif marker >= end_index:
                    new_markers.append(marker - shift)
                # markers within the drained range are dropped
            if new_markers:
                self._trace_point_markers[thread_id] = new_markers
            else:
                self._trace_point_markers.pop(thread_id, None)

        def _save_trace_point(self, thread_id, frames_slice, source, trace_name=None):
            """Snapshot a trace point and enqueue it on the daemon save worker.

            Always async: the sqlite save runs on a single long-lived
            daemon worker so the calling request thread returns
            immediately. If auto-emit is enabled, the worker spawns a
            detached exact-trace emitter subprocess after persistence.
            See the worker module-level docstring for the reliability
            contract: the healthy path is async, but
            unavailable/saturated worker states fall back inline instead
            of silently losing the trace.

            Bumps the in-flight pending counter as the FIRST line so the
            drain in ``disable_monitoring`` waits for this callback to
            complete (or release its slot) before tearing down the worker.
            """
            _begin_pending_trace_point_save()

            def build_args():
                # Snapshot inputs on the calling thread — once we hand off
                # to the worker, ``threading.current_thread()`` would
                # return the worker, not the request handler.
                current_thread = threading.current_thread()
                save_timestamp = time.time()
                frames_snapshot = list(frames_slice)
                parent_trace_id = self.trace_id

                return (
                    thread_id,
                    frames_snapshot,
                    current_thread,
                    source,
                    trace_name,
                    parent_trace_id,
                    save_timestamp,
                )

            _enqueue_trace_point_save(self._do_python_trace_point_save, build_args)

        def _do_python_trace_point_save(
            self,
            thread_id,
            frames_snapshot,
            snapshotted_thread,
            source,
            trace_name,
            parent_trace_id,
            save_timestamp,
        ):
            """Worker-thread target for ``_save_trace_point``.

            Runs on the daemon save worker thread, which has set
            ``thread_locals.is_saving = True`` once at startup for its
            lifetime — so any sqlite/msgpack/emit work re-entering monitor
            callbacks on this thread is short-circuited. We deliberately
            do NOT touch ``is_saving`` here: the lifetime flag set by the
            worker is what protects us, and clobbering it would defeat
            that protection on every save after the first.
            """
            from .core import _spawn_auto_emit

            trace_point_id = f"trc_{ulid.new()}"
            meta_overrides = {
                "trace_point": {
                    "auto_generated": True,
                    "source": source,
                    "parent_trace_id": parent_trace_id,
                }
            }

            # root_trace_id is set to the trace_point's own id because
            # kolo.trace.Trace treats any non-self root_trace_id as
            # "flushed segment of root trace" — which is not what a
            # first-class trace point is. Lineage lives in
            # meta.trace_point.parent_trace_id instead.
            self.save(
                frames_by_thread={thread_id: frames_snapshot},
                trace_id=trace_point_id,
                trace_name=trace_name,
                threads={thread_id: snapshotted_thread},
                current_thread_id=thread_id,
                root_trace_id=trace_point_id,
                timestamp=save_timestamp,
                meta_overrides=meta_overrides,
            )

            if self.config.get("auto_emit", True):
                _spawn_auto_emit(db_path=self.db_path)

        def build_trace(
            self,
            frames_by_thread=None,
            *,
            trace_id=None,
            trace_name=None,
            threads=None,
            current_thread_id=None,
            root_trace_id=None,
            timestamp=None,
            meta_overrides=None,
        ):
            return b"".join(
                self._iter_trace_chunks(
                    frames_by_thread=frames_by_thread,
                    trace_id=trace_id,
                    trace_name=trace_name,
                    threads=threads,
                    current_thread_id=current_thread_id,
                    root_trace_id=root_trace_id,
                    timestamp=timestamp,
                    meta_overrides=meta_overrides,
                )
            )

        def _iter_trace_chunks(
            self,
            frames_by_thread=None,
            *,
            trace_id=None,
            trace_name=None,
            threads=None,
            current_thread_id=None,
            root_trace_id=None,
            timestamp=None,
            meta_overrides=None,
        ):
            # frames_by_thread is passed by end_test (cut frames) and by
            # _save_trace_point (single-thread slice). Every keyword override
            # lets _save_trace_point route through this one builder so trace
            # points get the same full meta/thread payload as regular saves.
            if frames_by_thread is None or threads is None or trace_name is None:
                snap_frames, snap_threads, snap_trace_name = (
                    self._snapshot_trace_inputs(frames_by_thread)
                )
                if frames_by_thread is None:
                    frames_by_thread = snap_frames
                if threads is None:
                    threads = snap_threads
                if trace_name is None:
                    trace_name = snap_trace_name

            meta = self._build_trace_meta()
            if meta_overrides:
                meta.update(meta_overrides)

            return iter_v3_trace_chunks(
                command_line_args=sys.argv,
                current_commit_sha=COMMIT_SHA,
                current_thread_id=(
                    current_thread_id
                    if current_thread_id is not None
                    else self.current_thread_id
                ),
                meta=meta,
                timestamp=timestamp if timestamp is not None else self.timestamp,
                trace_id=trace_id if trace_id is not None else self.trace_id,
                trace_name=trace_name,
                root_trace_id=(
                    root_trace_id if root_trace_id is not None else self.root_trace_id
                ),
                threads=threads,
                frames_by_thread=frames_by_thread,
            )

        def save(
            self,
            frames_by_thread=None,
            *,
            trace_id=None,
            trace_name=None,
            threads=None,
            current_thread_id=None,
            root_trace_id=None,
            timestamp=None,
            meta_overrides=None,
        ):
            """
            frames_by_thread is only passed when called from end_test
            (end_test cuts off some frames) or from _save_trace_point
            (single-thread slice).

            The keyword overrides let trace-point saves reuse this same
            entry point so trace points land with the same meta/thread
            payload as a regular save.
            """

            chunks = self._iter_trace_chunks(
                frames_by_thread=frames_by_thread,
                trace_id=trace_id,
                trace_name=trace_name,
                threads=threads,
                current_thread_id=current_thread_id,
                root_trace_id=root_trace_id,
                timestamp=timestamp,
                meta_overrides=meta_overrides,
            )
            effective_trace_id = trace_id if trace_id is not None else self.trace_id
            timeout = self.config.get("sqlite_busy_timeout", 60)
            save_v3_trace_chunks(
                effective_trace_id,
                chunks,
                db_path=self.db_path,
                timeout=timeout,
            )

        def _set_trace_name(self, frames_by_thread=None):
            """
            Extract test name or HTTP request/response information from frames to set the trace name.
            """
            if frames_by_thread is None:
                frames_by_thread = self.frames_by_thread

            trace_name = extract_test_trace_name(
                frames_by_thread, self.current_thread_id
            )
            if trace_name:
                self.trace_name = trace_name
                return

            trace_name = extract_http_trace_name(
                frames_by_thread, self.current_thread_id
            )
            if trace_name:
                self.trace_name = trace_name

        def _resolve_trace_name(self, frames_by_thread=None):
            if self.trace_name is None:
                self._set_trace_name(frames_by_thread)
            return self.trace_name

    logger = logging.getLogger("kolo")

    def _set_monitor_active(monitor, value):
        # The Rust KoloMonitor exposes `set_active` (see rust/src/monitoring.rs)
        # because PyO3-generated attribute setters would require an exclusive
        # borrow on the pyclass's PyCell, which conflicts with shared borrows
        # held by other threads still running Python-level monitoring callbacks
        # (e.g. a background save thread). The pure-Python KoloMonitor in this
        # file uses a plain attribute.
        set_active = getattr(monitor, "set_active", None)
        if set_active is not None:
            set_active(value)
        else:
            monitor.active = value

    def _set_monitor_timestamp(monitor, value):
        # See `_set_monitor_active` for rationale.
        set_timestamp = getattr(monitor, "set_timestamp", None)
        if set_timestamp is not None:
            set_timestamp(value)
        else:
            monitor.timestamp = value

    def _monitor_has_trace_points(monitor) -> bool:
        """Return True if the monitor was configured with at least one
        ``trace_points.on_return`` target. Works for both the Python
        monitor (reads ``self.config``) and the Rust monitor (which
        exposes ``has_trace_points`` via PyO3)."""
        rust_flag = getattr(monitor, "has_trace_points", None)
        if rust_flag is not None:
            return bool(rust_flag)
        config = getattr(monitor, "config", None) or {}
        trace_points = config.get("trace_points", {}) or {}
        targets = trace_points.get("on_return", []) or []
        return bool(targets)

    def activate_monitoring(monitor):
        if getattr(monitor, "writer_circuit_open", False) is True:
            logger.warning(
                "Cannot activate Kolo monitoring: the trace writer circuit "
                "breaker is open. Restart the process to resume tracing."
            )
            return False
        tool_id = monitor.tool_id
        existing_tool = sys.monitoring.get_tool(tool_id)
        if existing_tool:  # pragma: no cover
            logger.warning(
                "Cannot activate Kolo monitoring: tool ID %d is already in use by %r. "
                "This may happen when another profiler (e.g., ddtrace, cProfile) is active.",
                tool_id,
                existing_tool,
            )
            return False

        try:
            sys.monitoring.use_tool_id(tool_id, "kolo")
        except ValueError as e:
            # Race condition: tool ID was claimed between our check and claim
            logger.warning(
                "Cannot activate Kolo monitoring: %s. "
                "This may happen due to concurrent activation.",
                e,
            )
            return False

        # Spawn the trace-point save worker BEFORE arming sys.monitoring
        # callbacks. The worker bootstrap (Thread.start /
        # threading._bootstrap / Event.wait) pumps bytecodes that would
        # fire monitor callbacks on the new thread before the worker has
        # called set_suspend_hooks(True) on itself, and under rapid
        # trace-point load that has been observed to deadlock
        # Thread.start().wait() against the main thread. Spawning here
        # means the worker's bootstrap runs under zero monitor events.
        if _monitor_has_trace_points(monitor):
            _ensure_trace_point_save_worker(monitor)
            _ensure_trace_point_atexit()

        _set_monitor_active(monitor, True)
        all_events = PY_START | PY_RETURN | PY_UNWIND | PY_RESUME | PY_YIELD | PY_THROW

        sys.monitoring.register_callback(tool_id, PY_START, monitor.monitor_pystart)
        sys.monitoring.register_callback(tool_id, PY_RETURN, monitor.monitor_pyreturn)
        sys.monitoring.register_callback(tool_id, PY_UNWIND, monitor.monitor_pyunwind)
        sys.monitoring.register_callback(tool_id, PY_RESUME, monitor.monitor_pyresume)
        sys.monitoring.register_callback(tool_id, PY_YIELD, monitor.monitor_pyyield)
        sys.monitoring.register_callback(tool_id, PY_THROW, monitor.monitor_pythrow)

        if monitor.line_events:
            all_events |= INSTRUCTION
            sys.monitoring.register_callback(
                tool_id, INSTRUCTION, monitor.monitor_instruction
            )

        _set_monitor_timestamp(monitor, time.time())
        sys.monitoring.set_events(tool_id, all_events)
        return True

    def disable_monitoring(monitor):
        if not monitor.active:
            return

        _set_monitor_active(monitor, False)
        sys.monitoring.set_events(monitor.tool_id, NO_EVENTS)
        sys.monitoring.register_callback(monitor.tool_id, PY_START, None)
        sys.monitoring.register_callback(monitor.tool_id, PY_RETURN, None)
        sys.monitoring.register_callback(monitor.tool_id, PY_UNWIND, None)
        sys.monitoring.register_callback(monitor.tool_id, PY_RESUME, None)
        sys.monitoring.register_callback(monitor.tool_id, PY_YIELD, None)
        sys.monitoring.register_callback(monitor.tool_id, PY_THROW, None)
        if monitor.line_events:
            sys.monitoring.register_callback(monitor.tool_id, INSTRUCTION, None)
        sys.monitoring.free_tool_id(monitor.tool_id)
        sys.monitoring.restart_events()
        # Drain any in-flight trace-point saves before tearing down the
        # worker. The drain waits for both queued jobs AND in-flight
        # callbacks (the pending counter is bumped at the entry-point of
        # _save_trace_point / _save_trace_point_from_rust, not at submit
        # time) so a callback racing with disable can't escape teardown.
        # If the worker died, wait_for_trace_point_saves() replays its
        # queued jobs inline before we continue. Skipped silently on
        # timeout so tests don't hang on a wedged sqlite/emit path — the
        # warning below surfaces the wedge.
        if not wait_for_trace_point_saves(timeout=5.0):
            logger.warning(
                "kolo trace-point save drain timed out at disable_monitoring;"
                " up to %d in-flight saves may be lost.",
                _trace_point_save_pending,
            )
        _stop_trace_point_save_worker()


def _save_trace_point_from_rust(
    thread_id: str,
    frames_bytes: list,
    func_name: str,
    db_path_str: str,
    source: str,
    lightweight_repr: bool,
    parent_trace_id: str,
    config_snapshot: dict,
    sqlite_busy_timeout: int,
    value_table_bytes=(),
):
    """Bridge from the Rust KoloMonitor to the async save worker.

    Always async: snapshots the minimum needed on the calling thread
    (thread metadata, save timestamp, and the raw msgpack frame bytes
    handed up by Rust) and pushes the heavy work — frame unpack + dict
    construction + sqlite write — onto the daemon save worker.
    If auto-emit is enabled, the save worker spawns a detached exact-
    trace emitter subprocess after persistence succeeds.
    Deliberately does NOT call ``msgpack.unpackb`` on the calling
    thread; that work happens inside the worker target so the request
    handler returns as fast as possible. If the worker is unavailable,
    the helper falls back inline before returning to Rust so the trace
    still persists.

    Calls ``_begin_pending_trace_point_save`` as the first executable
    statement so the drain in ``disable_monitoring`` waits for this
    callback to complete (or release its slot) before tearing down the
    worker — closing the in-flight-callback-vs-shutdown race.

    ``parent_trace_id`` is the trace currently being captured by the
    Rust monitor; it is surfaced inside ``meta["trace_point"]`` so
    consumers can tell a trace point from a regular capture and link
    back to the parent. Deliberately does NOT set a top-level
    ``root_trace_id`` because ``kolo.trace.Trace`` treats any non-self
    ``root_trace_id`` as "flushed segment of root trace".
    """
    _begin_pending_trace_point_save()

    def build_args():
        from pathlib import Path

        db_path = Path(db_path_str)
        thread = threading.current_thread()
        thread_meta = {
            "name": thread.name,
            "ident": getattr(thread, "ident", None),
            "native_id": getattr(thread, "native_id", None),
            "daemon": thread.daemon,
            "is_alive": thread.is_alive(),
        }
        save_timestamp = time.time()
        return (
            thread_id,
            frames_bytes,
            func_name,
            db_path,
            source,
            lightweight_repr,
            parent_trace_id,
            dict(config_snapshot),
            sqlite_busy_timeout,
            thread_meta,
            save_timestamp,
            list(value_table_bytes),
        )

    _enqueue_trace_point_save(_do_rust_trace_point_save, build_args)


def _do_rust_trace_point_save(
    thread_id: str,
    frames_bytes: list,
    func_name: str,
    db_path,
    source: str,
    lightweight_repr: bool,
    parent_trace_id: str,
    config_snapshot: dict,
    sqlite_busy_timeout: int,
    thread_meta: dict,
    save_timestamp: float,
    value_table_bytes=(),
):
    """Worker-thread target for ``_save_trace_point_from_rust``.

    Runs on the daemon save worker, which has called
    ``set_suspend_hooks(True)`` on its own Rust thread-local at startup
    so any callbacks fired here are short-circuited. The worker thread
    is not the request thread — that's why the request thread had to
    snapshot ``thread_meta`` and ``save_timestamp`` before submitting.
    """
    from .core import _spawn_auto_emit
    from .serialize import load_msgpack_value

    trace_point_id = f"trc_{ulid.new()}"
    chunks = iter_v3_trace_chunks(
        trace_id=trace_point_id,
        timestamp=save_timestamp,
        command_line_args=sys.argv,
        current_commit_sha=COMMIT_SHA,
        current_thread_id=thread_id,
        trace_name=func_name,
        meta={
            "version": __version__,
            "source": source,
            "environment": {
                "py_version": platform.python_version(),
                "py_version_full": sys.version,
                "platform": platform.platform(),
                "system": platform.system(),
                "machine": platform.machine(),
                "processor": platform.processor(),
            },
            "config": dict(config_snapshot),
            "trace_point": {
                "auto_generated": True,
                "source": func_name,
                "parent_trace_id": parent_trace_id,
            },
        },
        threads={thread_id: thread_meta},
        frames_by_thread={thread_id: frames_bytes},
        value_table={
            value_id: load_msgpack_value(value) for value_id, value in value_table_bytes
        },
    )
    save_v3_trace_chunks(
        trace_point_id,
        chunks,
        db_path=db_path,
        timeout=sqlite_busy_timeout,
    )
    if config_snapshot.get("auto_emit", True):
        _spawn_auto_emit(db_path=db_path)
