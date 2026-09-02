from __future__ import annotations

import inspect
import logging
import platform
import sys
import threading
import time
import types
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import msgpack
import ulid

from kolo.threads import get_thread_id

from .config import (
    CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE,
    resolve_flush_subtree_bytes as _resolve_flush_subtree_bytes,
)
from .db import save_v3_trace_chunks
from .filters.attrs import attrs_filter
from .filters.core import (
    FrameFilter,
    FrameProcessor,
    exec_filter,
    frozen_filter,
    get_ignore_frames,
    get_include_frames,
    library_filter,
)
from .filters.kolo import kolo_filter
from .filters.pypy import pypy_filter
from .filters.pytest import pytest_generated_filter
from .git import COMMIT_SHA
from .plugins import PluginProcessor, load_plugin_data
from .serialize import (
    FramePathCache,
    dump_msgpack,
    dump_msgpack_lightweight_repr,
    user_code_call_site,
)
from .subtree_flush import (
    FlushCandidate,
    OpenSubtree,
    SubtreeFlushTracker,
    TRACKING_PROBE_INTERVAL,
)
from .trace_container import iter_v3_trace_chunks
from .utils import extract_http_trace_name, extract_test_trace_name
from .version import __version__

logger = logging.getLogger("kolo")


class KoloLocals(threading.local):
    def __init__(self):
        self.call_frames = []
        self._frame_ids = {}


INCLUDE_FRAMES_WARNING = """\
Unexpected exception in include_frames: %s
    co_filename: %s
    co_name: %s
    event: %s
    frame locals: %s
"""
IGNORE_FRAMES_WARNING = """\
Unexpected exception in ignore_frames: %s
    co_filename: %s
    co_name: %s
    event: %s
    frame locals: %s
"""
DEFAULT_INCLUDE_FRAMES_WARNING = """\
Unexpected exception in default_include_frames: %s
    co_filename: %s
    co_name: %s
    event: %s
    frame locals: %s
"""
DEFAULT_IGNORE_FRAMES_WARNING = """\
Unexpected exception in default_ignore_frames: %s
    co_filename: %s
    co_name: %s
    event: %s
    frame locals: %s
"""
PROCESS_FRAME_WARNING = """\
Unexpected exception in KoloProfiler.process_frame
    co_filename: %s
    co_name: %s
    event: %s
    frame locals: %s
"""


class KoloProfiler:
    """
    Collect runtime information about code to view in VSCode.

    include_frames can be passed to enable profiling of standard library
    or third party code.

    ignore_frames can also be passed to disable profiling of a user's
    own code.

    The list should contain fragments of the path to the relevant files.
    For example, to include profiling for the json module the include_frames
    could look like ["/json/"].

    The list may also contain frame filters. A frame filter is a function
    (or other callable) that takes the same arguments as the profilefunc
    passed to sys.setprofile and returns a boolean representing whether
    to allow or block the frame.

    include_frames takes precedence over ignore_frames. A frame that
    matches an entry in each list will be profiled.

    Rough order of operations in profiler (ideally kolo could natively make such a list!)
    1. __call__ is the sys registered profile callback which then calls calls push_frame_data
    2. push_frame_data adds to self.frames_by_thread
    3. save_trace_in_thread
    4. KoloProfiler.save
    5. build_trace
    """

    def __init__(
        self,
        db_path: Path,
        config=None,
        one_trace_per_test=False,
        *,
        source,
        name: Optional[str] = None,
    ) -> None:
        self.db_path = db_path
        self.source = source
        self.one_trace_per_test = one_trace_per_test
        trace_id = ulid.new()
        self.trace_id = f"trc_{trace_id}"
        self._explicit_trace_name = name
        self.trace_name = name
        self.start_test_indices: Dict[str, int] = {}
        self.config = config if config is not None else {}
        self.include_frames = get_include_frames(config)
        self.ignore_frames = get_ignore_frames(config)

        self.default_include_frames: Dict[str, List[FrameProcessor]] = {}
        for plugin_data in load_plugin_data(self.config):
            processor = PluginProcessor(plugin_data, self.config)
            for co_name in plugin_data["co_names"]:
                self.default_include_frames.setdefault(co_name, []).append(processor)

        self.default_ignore_frames: List[FrameFilter] = [
            library_filter,
            frozen_filter,
            pypy_filter,
            kolo_filter,
            exec_filter,
            attrs_filter,
            pytest_generated_filter,
        ]
        self.thread_locals = KoloLocals()
        self.timestamp = time.time()
        self.rust_profiler = None
        self.omit_return_locals = self.config.get("omit_return_locals", False)
        self.flush_subtree_bytes = _resolve_flush_subtree_bytes(self.config)
        self.root_trace_id = self.trace_id
        self._subtree_flush = SubtreeFlushTracker(self.flush_subtree_bytes)
        self._subtree_stack = self._subtree_flush.subtree_stack
        self._thread_cumulative_bytes = self._subtree_flush.thread_cumulative_bytes
        self._flush_in_progress = self._subtree_flush.flush_in_progress
        self._subtree_flush_lock = threading.RLock()

        # Key is the thread id, value is the native python thread object
        self.threads: Dict[str, threading.Thread] = {}

        # Key is the thread id, value is a list of frames for that thread
        self.frames_by_thread: Dict[str, List[bytes]] = defaultdict(list)

        self.current_thread_id = get_thread_id(threading.current_thread())
        self._frame_paths = FramePathCache()
        if self.config.get("lightweight_repr", False):
            self.dump_msgpack = dump_msgpack_lightweight_repr
        else:
            self.dump_msgpack = dump_msgpack

    def _build_trace_meta(self):
        config = {
            k: v
            for k, v in self.config.items()
            if k not in CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE
        }
        config["use_monitoring"] = False
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

    def _low_water_bytes(self) -> int:
        return self._subtree_flush.low_water_bytes()

    def _co_name_from_packed_frames(self, frames: List[bytes]) -> str:
        fallback = "<unknown>"
        for packed_frame in frames:
            frame_data = msgpack.unpackb(packed_frame, strict_map_key=False)
            if frame_data.get("type") == "frame":
                return frame_data.get("co_name", "<unknown>")
            if fallback == "<unknown>" and "co_name" in frame_data:
                fallback = frame_data.get("co_name", "<unknown>")
        return fallback

    def _select_flush_candidate(
        self, thread_id: str
    ) -> tuple[OpenSubtree, FlushCandidate] | None:
        return self._subtree_flush.select_flush_candidate(thread_id)

    def _shift_flush_state_after_flush(
        self,
        thread_id: str,
        *,
        start_index: int,
        end_index: int,
        resident_delta: int,
    ) -> None:
        self._subtree_flush.shift_flush_state_after_flush(
            thread_id,
            start_index=start_index,
            end_index=end_index,
            resident_delta=resident_delta,
        )

    def _maybe_flush_segments(self, thread_id: str) -> None:
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
                self.frames_by_thread if frames_by_thread is None else frames_by_thread
            )
            frames_snapshot = {
                thread_id: list(frames) for thread_id, frames in source.items()
            }
            threads = dict(self.threads)
            trace_name = self._resolve_trace_name(frames_snapshot)
        return frames_snapshot, threads, trace_name

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> None:
        if event in ["c_call", "c_return", "c_exception"]:
            return

        co_name = frame.f_code.co_name

        frames = []
        frame_types = []

        try:
            # Execute only the filters listening for this co_name
            for processor in self.default_include_frames.get(co_name, ()):
                try:
                    if processor(frame, event, arg):
                        frame_data = processor.process(
                            frame, event, arg, self.thread_locals.call_frames
                        )
                        if frame_data:  # pragma: no branch
                            data = self.dump_msgpack(frame_data)
                            frames.append(data)
                            frame_types.append(frame_data["type"])
                except Exception as e:
                    logger.warning(
                        DEFAULT_INCLUDE_FRAMES_WARNING,
                        processor,
                        frame.f_code.co_filename,
                        frame.f_code.co_name,
                        event,
                        dict(
                            frame.f_locals
                        ),  # Convert for Python 3.13+ FrameLocalsProxy
                        exc_info=e,
                    )
                    continue

            for frame_filter in self.include_frames:
                try:
                    if frame_filter(frame, event, arg):
                        frames.append(self.process_frame(frame, event, arg))
                        frame_types.append("frame")
                        return
                except Exception as e:
                    logger.warning(
                        INCLUDE_FRAMES_WARNING,
                        frame_filter,
                        frame.f_code.co_filename,
                        frame.f_code.co_name,
                        event,
                        dict(
                            frame.f_locals
                        ),  # Convert for Python 3.13+ FrameLocalsProxy
                        exc_info=e,
                    )
                    continue

            for frame_filter in self.default_ignore_frames:
                try:
                    if frame_filter(frame, event, arg):
                        return
                except Exception as e:
                    logger.warning(
                        DEFAULT_IGNORE_FRAMES_WARNING,
                        frame_filter,
                        frame.f_code.co_filename,
                        frame.f_code.co_name,
                        event,
                        dict(
                            frame.f_locals
                        ),  # Convert for Python 3.13+ FrameLocalsProxy
                        exc_info=e,
                    )
                    continue

            for frame_filter in self.ignore_frames:
                try:
                    if frame_filter(frame, event, arg):
                        return
                except Exception as e:
                    logger.warning(
                        IGNORE_FRAMES_WARNING,
                        frame_filter,
                        frame.f_code.co_filename,
                        frame.f_code.co_name,
                        event,
                        dict(
                            frame.f_locals
                        ),  # Convert for Python 3.13+ FrameLocalsProxy
                        exc_info=e,
                    )
                    continue

            try:
                frames.append(self.process_frame(frame, event, arg))
                frame_types.append("frame")
            except Exception as e:
                logger.warning(
                    PROCESS_FRAME_WARNING,
                    frame.f_code.co_filename,
                    frame.f_code.co_name,
                    event,
                    dict(frame.f_locals),  # Convert for Python 3.13+ FrameLocalsProxy
                    exc_info=e,
                )

        finally:
            if frames:
                if event == "return":
                    frames.reverse()
                    frame_types.reverse()

                if self.one_trace_per_test:  # pragma: no branch
                    for index, frame_type in enumerate(frame_types):  # pragma: no cover
                        if frame_type == "start_test":
                            before, frames = frames[:index], frames[index:]
                            before_types, frame_types = (
                                frame_types[:index],
                                frame_types[index:],
                            )

                            self.push_frame_data(
                                before,
                                event=event if "frame" in before_types else None,
                            )

                            self.start_test()

                        elif frame_type == "end_test":
                            before, frames = frames[: index + 1], frames[index + 1 :]
                            before_types, frame_types = (
                                frame_types[: index + 1],
                                frame_types[index + 1 :],
                            )

                            self.push_frame_data(
                                before,
                                event=event if "frame" in before_types else None,
                            )

                            self.end_test()

                self.push_frame_data(
                    frames,
                    event=event if "frame" in frame_types else None,
                )

    def push_frame_data(self, data, event=None):
        if not data:
            return

        current_thread = threading.current_thread()
        thread_id = get_thread_id(current_thread)
        with self._subtree_flush_lock:
            if thread_id not in self.threads:
                self.threads[thread_id] = current_thread

            if thread_id not in self.frames_by_thread:
                self.frames_by_thread[thread_id] = []

            thread_frames = self.frames_by_thread[thread_id]
            frame_start_index = len(thread_frames)
            thread_frames.extend(data)
            frame_end_index = len(thread_frames)

        if self.flush_subtree_bytes is None:
            return

        batch_bytes = (
            len(data[0]) if len(data) == 1 else sum(len(frame) for frame in data)
        )
        tracker = self._subtree_flush
        current_bytes = tracker.thread_cumulative_bytes.get(thread_id, 0)
        flush_tracking_armed = False
        added_bytes = 0

        if (
            thread_id in tracker.flush_tracking_armed
            or tracker._tracking_start_bytes == 0
        ):
            current_bytes += batch_bytes
            tracker.thread_cumulative_bytes[thread_id] = current_bytes
            tracker.flush_tracking_armed.add(thread_id)
            flush_tracking_armed = True
            added_bytes = batch_bytes
        else:
            current_bytes += batch_bytes
            tracker.thread_cumulative_bytes[thread_id] = current_bytes
            if current_bytes >= tracker._tracking_start_bytes:
                tracker.flush_tracking_armed.add(thread_id)
                flush_tracking_armed = True
                added_bytes = batch_bytes
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

        if not flush_tracking_armed:
            return

        if event == "call":
            co_name = self._co_name_from_packed_frames(data)
            self._subtree_flush.push_open_subtree(
                thread_id,
                start_index=frame_start_index,
                start_bytes=max(0, current_bytes - added_bytes),
                co_name=co_name,
            )
        elif event == "return":
            subtree = self._subtree_flush.pop_open_subtree(thread_id)
            if subtree is not None:
                subtree_bytes = current_bytes - subtree.start_bytes
                self._subtree_flush.record_closed_segment(
                    thread_id,
                    start_index=subtree.start_index,
                    end_index=frame_end_index,
                    resident_bytes=subtree_bytes,
                    co_name=subtree.co_name,
                )
        else:
            self._subtree_flush.record_closed_segment(
                thread_id,
                start_index=frame_start_index,
                end_index=frame_end_index,
                resident_bytes=added_bytes,
                co_name=self._co_name_from_packed_frames(data),
            )

        self._maybe_flush_segments(thread_id)

    def _flush_subtree(
        self,
        thread_id: str,
        owner: OpenSubtree,
        candidate: FlushCandidate,
    ) -> bool:
        """Save a flushable closed segment and replace it with a placeholder."""
        with self._subtree_flush_lock:
            frames = self.frames_by_thread[thread_id]
            subtree_frames = list(frames[candidate.start_index : candidate.end_index])
            flushed_bytes = sum(len(frame) for frame in subtree_frames)
            subtrace_id = f"trc_{ulid.new()}"
            thread = self.threads.get(thread_id, threading.current_thread())
            trace_name = self._resolve_trace_name({thread_id: subtree_frames})
            chunks = iter_v3_trace_chunks(
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

    def _save_subtrace_chunks(self, subtrace_id: str, chunks) -> None:
        # Runs under _subtree_flush_lock. Suspend sys.setprofile on the current
        # thread while saving so the hot callback path stays free of save guards.
        # NOTE (#2535 item 4): we deliberately do NOT mirror KoloMonitor's
        # `thread_locals.is_saving` guard here. The two backends use different
        # APIs — sys.setprofile supports per-thread unregister with zero hot-path
        # cost, while sys.monitoring does not, which is why the monitor needs an
        # in-band re-entrance flag. Adding the same flag to the profiler costs a
        # threading.local lookup on every callback (~12% slowdown on
        # benchmark_chaos_exclude[with_python_profiler] when measured), so the
        # unification is not worth it.
        timeout = self.config.get("sqlite_busy_timeout", 60)
        db_path = self.db_path

        previous_profiler = sys.getprofile()
        sys.setprofile(None)
        try:
            save_v3_trace_chunks(
                subtrace_id,
                chunks,
                db_path=db_path,
                ignore_errors=False,
                timeout=timeout,
            )
        finally:
            sys.setprofile(previous_profiler)

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

    def end_test(self):
        with self._subtree_flush_lock:
            frames_by_thread = {
                thread_id: list(frames[self.start_test_indices.get(thread_id, 0) :])
                for thread_id, frames in self.frames_by_thread.items()
            }
        self.save(frames_by_thread=frames_by_thread)
        with self._subtree_flush_lock:
            self._subtree_flush.reset(self.frames_by_thread)

    def __enter__(self) -> None:
        if self.config.get("use_rust", True):
            try:
                from ._kolo import register_profiler
            except ImportError as e:  # pragma: no cover
                # Useful for PyPy, which doesn't do Rust
                logger.debug(
                    "Rust profiler import failed (%s), using Python profiler", e
                )
                sys.setprofile(self)
                threading.setprofile(self)
            else:
                register_profiler(self)
        else:
            sys.setprofile(self)
            threading.setprofile(self)

    def __exit__(self, *exc) -> None:
        sys.setprofile(None)
        threading.setprofile(None)

    def build_trace(self, frames_by_thread=None):
        # frames_by_thread is only passed when called by end_test.

        if self.rust_profiler:
            data = self.rust_profiler.build_trace()
            self.trace_id = self.rust_profiler.trace_id
            self.root_trace_id = self.rust_profiler.root_trace_id
            return data

        return b"".join(self._iter_trace_chunks(frames_by_thread))

    def _iter_trace_chunks(self, frames_by_thread=None):
        frames_by_thread, threads, trace_name = self._snapshot_trace_inputs(
            frames_by_thread
        )
        return iter_v3_trace_chunks(
            command_line_args=sys.argv,
            current_commit_sha=COMMIT_SHA,
            current_thread_id=self.current_thread_id,
            meta=self._build_trace_meta(),
            timestamp=self.timestamp,
            trace_id=self.trace_id,
            trace_name=trace_name,
            root_trace_id=self.root_trace_id,
            threads=threads,
            frames_by_thread=frames_by_thread,
        )

    def save(self, frames_by_thread=None) -> None:
        """
        frames_by_thread is only passed when called from end_test,
        because end_test cuts off some frames and saves directly.
        """

        if self.rust_profiler:
            self.rust_profiler.save()
            self.trace_id = self.rust_profiler.trace_id
            self.root_trace_id = self.rust_profiler.root_trace_id
            return

        timeout = self.config.get("sqlite_busy_timeout", 60)
        chunks = self._iter_trace_chunks(frames_by_thread)
        save_v3_trace_chunks(
            self.trace_id,
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

        trace_name = extract_test_trace_name(frames_by_thread, self.current_thread_id)
        if trace_name:
            self.trace_name = trace_name
            return

        trace_name = extract_http_trace_name(frames_by_thread, self.current_thread_id)
        if trace_name:
            self.trace_name = trace_name

    def _resolve_trace_name(self, frames_by_thread=None):
        if self.trace_name is None:
            self._set_trace_name(frames_by_thread)
        return self.trace_name

    def process_frame(self, frame: types.FrameType, event: str, arg: object) -> bytes:
        if event == "call":
            frame_id = f"frm_{ulid.new()}"
            self.thread_locals._frame_ids[id(frame)] = frame_id
        elif event == "return":  # pragma: no branch
            frame_id = self.thread_locals._frame_ids[id(frame)]

        user_code_call_site_ = user_code_call_site(
            self.thread_locals.call_frames, frame_id
        )

        if event == "call":
            self.thread_locals.call_frames.append((frame, frame_id))
        elif event == "return":  # pragma: no branch
            self.thread_locals.call_frames.pop()

        if self.omit_return_locals and event == "return":
            frame_locals = None
        else:
            frame_locals = {
                k: v for k, v in frame.f_locals.items() if k != "__builtins__"
            }

        frame_data = {
            "path": self._frame_paths.format(frame),
            "co_name": frame.f_code.co_name,
            "qualname": get_qualname(frame),
            "event": event,
            "frame_id": frame_id,
            "arg": arg,
            "locals": frame_locals,
            "timestamp": time.time(),
            "type": "frame",
            "user_code_call_site": user_code_call_site_,
        }
        return self.dump_msgpack(frame_data)


def get_qualname(frame: types.FrameType) -> str | None:
    try:
        qualname = frame.f_code.co_qualname  # type: ignore[attr-defined]
    except AttributeError:
        pass
    else:
        module = frame.f_globals.get("__name__", "<unknown>")
        return f"{module}.{qualname}"

    co_name = frame.f_code.co_name
    if co_name == "<module>":  # pragma: no cover
        module = frame.f_globals.get("__name__", "<unknown>")
        return f"{module}.<module>"

    try:
        outer_frame = frame.f_back
        assert outer_frame
        try:
            function = outer_frame.f_locals[co_name]
        except KeyError:
            try:
                self = frame.f_locals["self"]
            except KeyError:
                cls = frame.f_locals.get("cls")
                if isinstance(cls, type):
                    function = inspect.getattr_static(cls, co_name)
                else:
                    try:
                        qualname = frame.f_locals["__qualname__"]
                    except KeyError:
                        function = frame.f_globals[co_name]
                    else:  # pragma: no cover
                        module = frame.f_globals.get("__name__", "<unknown>")
                        return f"{module}.{qualname}"
            else:
                function = inspect.getattr_static(self, co_name)
                if isinstance(function, property):
                    function = function.fget

        return f"{function.__module__}.{function.__qualname__}"
    except Exception:
        return None
