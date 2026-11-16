"""Miles' session server (`rollout/session/core.py`, `v2/core.py` at radixark/miles@bb18e6ab7811), wrapped: each chat
call's GPU readings come off the engine's reply in `extract_completion` into the call's session (`SessionGpu`), and
`_session_metadata` hands the session's readings to the rollout in `/samples` only (never `GET /sessions/{id}`). A
call that ends without readings, or a generation sent through the generic proxy (its reply stripped), marks the session
incomplete. Why: DESIGN.md beside this file."""

from __future__ import annotations

import functools
import inspect
import json
import logging
import threading
from collections import OrderedDict
from contextvars import ContextVar
from typing import Any

from probe.sdk.hardware.trace import GpuTrace

from .serving import GPU_FIELD

log = logging.getLogger(__name__)

#: Readings held across every session (~1.5 KB each in memory: about 400 MB at most), and sessions held (empty ones
#: count). 256 running sessions each at their own cap fit; the least recently used session goes first.
MAX_READINGS = 262_144
MAX_SESSIONS = 16_384
#: Evicted session ids remembered until `delete_session`, so their later calls stay incomplete.
EVICTED_REMEMBERED = 262_144
#: One session's readings (a try's own cap, `../live/rollout.py`).
MAX_SESSION_READINGS = 1_024
#: Generic-proxy routes that generate (`sessions.py:265`): their readings never reach `extract_completion`.
GENERATING_SUFFIXES = ("completions", "generate")
_MARK = "__probe_wrapped__"
#: The chat call in progress in this task: its session id and whether its readings arrived.
_CALL: ContextVar[tuple[str, dict] | None] = ContextVar("probe_miles_session_call", default=None)
#: Set while Miles builds a `/samples` reply: only that reply's metadata carries the session's readings, never
#: `GET /sessions/{id}`, which the agent and Probe's watcher poll. Set in `collect_samples` (an older Miles builds the
#: reply there) and again in `_collect_samples` (bb18 runs it on a worker thread, which never inherits the flag).
_COLLECTING: ContextVar[bool] = ContextVar("probe_miles_session_collecting", default=False)
_warned: set[str] = set()


class SessionGpu:
    """Each open session's GPU trace, bounded by readings (least recently used session evicted first). Thread-safe:
    Miles builds `/samples` replies on a worker thread (`core.py:337`)."""

    def __init__(self, max_readings: int = MAX_READINGS, max_sessions: int = MAX_SESSIONS) -> None:
        self._max_readings = max_readings
        self._max_sessions = max_sessions
        self._traces: OrderedDict[str, GpuTrace] = OrderedDict()
        self._evicted: OrderedDict[str, None] = OrderedDict()
        self._readings = 0
        self._lock = threading.Lock()
        self._has_logged_eviction = False

    def add(self, session_id: str, trace: dict) -> None:
        with self._lock:
            found = self._find(session_id)
            before = len(found.readings)
            found.extend(trace)
            self._readings += len(found.readings) - before
            self._drop_oldest()

    def mark_incomplete(self, session_id: str) -> None:
        with self._lock:
            self._find(session_id).is_incomplete = True
            self._drop_oldest()

    def get(self, session_id: str) -> dict:
        """The session's readings so far; an evicted session's say incomplete, an unseen one's are empty."""
        with self._lock:
            found = self._traces.get(session_id)
            if found is not None:
                trace = found.to_dict()
                return {**trace, "readings": list(trace["readings"])}
            return {"readings": [], "dropped": 0, "incomplete": session_id in self._evicted}

    def forget(self, session_id: str) -> None:
        with self._lock:
            found = self._traces.pop(session_id, None)
            if found is not None:
                self._readings -= len(found.readings)
            self._evicted.pop(session_id, None)

    def _find(self, session_id: str) -> GpuTrace:
        """The session's trace, made on first use, and moved to the newest end (eviction takes the least recent)."""
        found = self._traces.get(session_id)
        if found is None:
            found = self._traces[session_id] = GpuTrace(MAX_SESSION_READINGS)
            found.is_incomplete = session_id in self._evicted
        self._traces.move_to_end(session_id)
        return found

    def _drop_oldest(self) -> None:
        while self._traces and (self._readings > self._max_readings or len(self._traces) > self._max_sessions):
            session_id, trace = self._traces.popitem(last=False)
            self._readings -= len(trace.readings)
            self._evicted[session_id] = None
            while len(self._evicted) > EVICTED_REMEMBERED:
                self._evicted.popitem(last=False)
            if not self._has_logged_eviction:
                self._has_logged_eviction = True
                log.warning("Probe's session GPU store is full; the least recently used sessions' readings are dropped "
                            "and those rollouts say their GPU capture is incomplete")


SESSIONS = SessionGpu()


def install_session(module: Any) -> None:
    """`miles.rollout.session.core` or `.v2.core` as it loads: its core class and its `extract_completion` binding
    (v2 imports it by name, `v2/core.py:10-19`)."""
    extract = getattr(module, "extract_completion", None)
    if callable(extract) and not getattr(extract, _MARK, False):
        module.extract_completion = _wrap_extract(extract)
    for name in ("SessionCore", "SessionCoreV2"):
        core = module.__dict__.get(name)
        if isinstance(core, type):
            _wrap_core(core)


def _wrap_extract(original: Any) -> Any:
    @functools.wraps(original)
    def extract_reply(result: dict) -> tuple:
        extracted = original(result)
        _call_quietly("read a reply", _take_reply_trace, extracted[1])
        return extracted

    setattr(extract_reply, _MARK, True)
    return extract_reply


def _take_reply_trace(choice: Any) -> None:
    """Pop the engine's readings off the reply (so neither the records nor the agent hold them) into the call's
    session."""
    meta = choice.get("meta_info") if isinstance(choice, dict) else None
    trace = meta.pop(GPU_FIELD, None) if isinstance(meta, dict) else None
    call = _CALL.get()
    if call is not None and isinstance(trace, dict):
        SESSIONS.add(call[0], trace)
        call[1]["has_trace"] = True


def _wrap_core(core: type) -> None:
    for name, make in (("chat_completions", _make_chat), ("_session_metadata", _make_metadata),
                       ("collect_samples", _make_collect), ("_collect_samples", _make_collect),
                       ("delete_session", _make_delete),
                       ("proxy", _make_proxy)):  # fmt: skip
        original = core.__dict__.get(name)
        if callable(original) and not getattr(original, _MARK, False):
            wrapped = make(original)
            setattr(wrapped, _MARK, True)
            setattr(core, name, wrapped)


def _make_chat(original: Any) -> Any:
    @functools.wraps(original)
    async def run_chat(self: Any, session_id: str, *args: Any, **kwargs: Any) -> Any:
        call: dict = {"has_trace": False}
        token = _CALL.set((session_id, call))
        try:
            response = await original(self, session_id, *args, **kwargs)
        except BaseException:
            _call_quietly("count a call", SESSIONS.mark_incomplete, session_id)
            raise
        finally:
            _CALL.reset(token)
        if not call["has_trace"]:  # non-200, a 502 transport error, or a reply without readings
            _call_quietly("count a call", SESSIONS.mark_incomplete, session_id)
        return response

    return run_chat


def _make_metadata(original: Any) -> Any:
    @functools.wraps(original)
    def build_metadata(self: Any, session_id: str, session: Any) -> dict:
        metadata = original(self, session_id, session)
        if not _COLLECTING.get():  # `GET /sessions/{id}`: never the readings
            return metadata
        trace = _call_quietly("hand over a session", SESSIONS.get, session_id)
        if isinstance(metadata, dict) and trace is not None:
            metadata[GPU_FIELD] = trace
        return metadata

    return build_metadata


def _make_collect(original: Any) -> Any:
    if inspect.iscoroutinefunction(original):
        @functools.wraps(original)
        async def collect_samples(self: Any, *args: Any, **kwargs: Any) -> Any:
            token = _COLLECTING.set(True)
            try:
                return await original(self, *args, **kwargs)
            finally:
                _COLLECTING.reset(token)

        return collect_samples

    @functools.wraps(original)
    def build_samples(self: Any, *args: Any, **kwargs: Any) -> Any:
        token = _COLLECTING.set(True)
        try:
            return original(self, *args, **kwargs)
        finally:
            _COLLECTING.reset(token)

    return build_samples


def _make_delete(original: Any) -> Any:
    @functools.wraps(original)
    async def delete_session(self: Any, session_id: str, *args: Any, **kwargs: Any) -> Any:
        try:
            return await original(self, session_id, *args, **kwargs)
        finally:
            _call_quietly("drop a session", SESSIONS.forget, session_id)

    return delete_session


def _make_proxy(original: Any) -> Any:
    @functools.wraps(original)
    async def send_proxied(self: Any, session_id: str, path: str, *args: Any, **kwargs: Any) -> Any:
        is_generating = (str(kwargs.get("method", "")).upper() == "POST"
                         and str(path).rstrip("/").endswith(GENERATING_SUFFIXES))  # fmt: skip
        if is_generating:
            _call_quietly("count a call", SESSIONS.mark_incomplete, session_id)
        response = await original(self, session_id, path, *args, **kwargs)
        if is_generating:
            _call_quietly("strip a proxied reply", strip_proxied_trace, response)
        return response

    return send_proxied


def strip_proxied_trace(response: Any) -> None:
    """Take the engine's readings off a proxied generation's reply, so the agent never holds them: a JSON body
    (`/generate`: one reply or a list; `/v1/completions`: each choice), or a streamed one Miles buffered whole (each
    `data:` event). The body is re-rendered in place."""
    body = getattr(response, "body", None)
    if not isinstance(body, bytes) or f'"{GPU_FIELD}"'.encode() not in body:
        return
    try:
        stripped = _render_stripped(json.loads(body))
    except ValueError:  # not one JSON document: server-sent events
        lines = body.split(b"\n")
        for index, line in enumerate(lines):
            if line.startswith(b"data:") and GPU_FIELD.encode() in line:
                try:
                    lines[index] = b"data: " + _render_stripped(json.loads(line[5:]))
                except ValueError:
                    continue
        stripped = b"\n".join(lines)
    response.body = stripped
    response.headers["content-length"] = str(len(stripped))


def _render_stripped(data: Any) -> bytes:
    replies = data if isinstance(data, list) else [data, *(data.get("choices") or [])] if isinstance(data, dict) else []
    for reply in replies:
        meta = reply.get("meta_info") if isinstance(reply, dict) else None
        if isinstance(meta, dict):
            meta.pop(GPU_FIELD, None)
    return json.dumps(data, separators=(",", ":")).encode()


def _call_quietly(what: str, call: Any, *args: Any) -> Any:
    try:
        return call(*args)
    except Exception:  # noqa: BLE001 -- fail open: the session server runs as if Probe were absent
        if what not in _warned:
            _warned.add(what)
            log.warning("Probe could not %s for GPU readings; the session server continues", what, exc_info=True)
        return None
