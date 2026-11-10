"""CallObserver: turns what passed through the proxy into the rollout's progress snapshot and, while watched, its
turns, on a thread of its own. The forward path only drops events into a bounded queue (dropped when full), so it
never waits on Probe."""

from __future__ import annotations

import json
import logging
import queue
import threading
import zlib
from dataclasses import dataclass

from ......generated.samples import AttemptOutcome, AttemptPhase
from .dialect import Dialect, Reply, ToolCall
from .routes import Route
from .sse import read_frames

log = logging.getLogger("probe.samples.proxy")

#: Events waiting at most, and their bodies' bytes; past either the forward path drops them (counted on `dropped`).
QUEUE_MAX = 4096
QUEUE_MAX_BYTES = 256 * 1024 * 1024
#: Why a rollout ended `error` when the proxy it went through stopped under it.
PROXY_ERROR_REASON = "probe_proxy"
_TOOL_ARGUMENTS_CHARS = 400
_STOP = object()


@dataclass(frozen=True)
class CallStarted:
    route: Route


@dataclass(frozen=True)
class CallEnded:
    """One model call's end. `body` is the response as received (still content-encoded), cut at the tee's cap."""

    route: Route
    dialect: Dialect
    request: bytes
    status: int
    content_type: str
    content_encoding: str
    body: bytes
    failure: str | None = None


@dataclass(frozen=True)
class WatchStarted:
    route: Route


@dataclass(frozen=True)
class RouteFailed:
    route: Route


class CallObserver:
    """One per proxy. Its SDK calls (`attempt_progress`, `log_turns`, `attempt_end`) journal to the outbox; a slow
    disk or a down server slows only this thread."""

    def __init__(self) -> None:
        self._queue: queue.Queue = queue.Queue(maxsize=QUEUE_MAX)
        self._thread = threading.Thread(target=self._run, name="probe-proxy-observer", daemon=True)
        self._lock = threading.Lock()
        self._waiting_bytes = 0
        self.dropped = 0
        self.failures = 0

    def start(self) -> None:
        self._thread.start()

    def submit(self, event: object) -> None:
        """From the forward path: never blocks; a full queue (by count or bytes) drops the event."""
        size = _get_size(event)
        with self._lock:
            if self._waiting_bytes + size > QUEUE_MAX_BYTES:
                self.dropped += 1
                return
            try:
                self._queue.put_nowait(event)
            except queue.Full:
                self.dropped += 1
                return
            self._waiting_bytes += size

    def submit_waiting(self, event: object, timeout: float = 1.0) -> None:
        """From a command handler or a stop: waits a little for room, then drops."""
        try:
            self._queue.put(event, timeout=timeout)
        except queue.Full:
            self.dropped += 1

    def stop(self, timeout: float = 5.0) -> None:
        """Handle what is queued, then end."""
        if not self._thread.is_alive():
            return
        self.submit_waiting(_STOP, timeout=timeout)
        self._thread.join(timeout)

    def _run(self) -> None:
        while True:
            event = self._queue.get()
            if event is _STOP:
                return
            with self._lock:
                self._waiting_bytes -= _get_size(event)
            try:
                self._handle(event)
            except Exception as exc:  # noqa: BLE001 -- one bad event never ends the observer
                self.failures += 1
                log.debug("probe: the proxy could not record a call (%s: %s)", type(exc).__name__, exc)

    def _handle(self, event: object) -> None:
        if isinstance(event, CallStarted):
            route = event.route
            route.calls_started += 1
            if not route.is_ended:
                route.samples.attempt_progress(route.attempt_key, phase=AttemptPhase.GENERATING,
                                               activity=f"model call {route.calls_started}")  # fmt: skip
        elif isinstance(event, CallEnded):
            self._record_call(event)
        elif isinstance(event, WatchStarted):
            self._send_snapshot(event.route)
        elif isinstance(event, RouteFailed):
            route = event.route
            route.samples.attempt_end(
                route.attempt_key, AttemptOutcome.ERROR, error_reason=PROXY_ERROR_REASON,
                error_message="the Probe rollout proxy stopped while this sample's model calls went through it")  # fmt: skip

    # -- a call's end: progress, then turns while watched -----------------------------------------
    def _record_call(self, event: CallEnded) -> None:
        route = event.route
        if route.is_ended:
            return
        number = route.calls_done + 1
        if event.failure is not None or not 200 <= event.status < 300:
            why = event.failure or f"HTTP {event.status}"
            route.samples.attempt_progress(route.attempt_key, activity=f"model call {number} failed: {why}")
            return
        reply = _read_reply(event) or Reply()  # an answer read here cannot parse still counts as a call
        route.calls_done = number
        route.tokens += reply.output_tokens or 0
        phase = AttemptPhase.TOOL if reply.tool_calls else AttemptPhase.GENERATING
        route.samples.attempt_progress(route.attempt_key, phase=phase, turns=number, tokens=route.tokens,
                                       activity=_describe(reply))  # fmt: skip
        self._send_turns(event, reply)

    def _send_turns(self, event: CallEnded, reply: Reply) -> None:
        route = event.route
        if not route.samples.is_watched(route.attempt_key):
            route.covered = None
            route.replied = (event.request, reply.turns, reply.history_items)
            return
        request = _load_json(event.request)
        history = event.dialect.read_history(request)
        start = route.covered or 0
        if not event.dialect.is_whole_history(request):
            start = 0
        new = history[start:] if len(history) >= start else history[-1:]
        route.samples.log_turns(route.attempt_key, [*new, *reply.turns])
        route.covered = (len(history) + reply.history_items) if event.dialect.is_whole_history(request) else 0
        route.replied = (event.request, reply.turns, reply.history_items)

    # -- a watch's first snapshot: the newest request's history (+ its reply, when it came) -------------
    def _send_snapshot(self, route: Route) -> None:
        if route.covered is not None or route.is_ended:
            return  # this watch is fed already
        last = route.last_request
        if last is None:
            route.covered = 0
            return
        dialect, body = last
        history = dialect.read_history(_load_json(body))
        turns = list(history)
        covered = len(history)
        if route.replied is not None and route.replied[0] is body:
            turns += route.replied[1]
            covered += route.replied[2]
        route.samples.log_turns(route.attempt_key, turns)
        route.covered = covered


def _get_size(event: object) -> int:
    """The bytes an event holds while it waits (a call's request and answer)."""
    return len(event.request) + len(event.body) if isinstance(event, CallEnded) else 0


def _read_reply(event: CallEnded) -> Reply | None:
    text = _decode(event.body, event.content_encoding)
    if text is None:
        return None
    if "text/event-stream" in event.content_type:
        return event.dialect.read_stream(read_frames(text))
    body = _load_json(text)
    return event.dialect.read_reply(body) if body else None


def _decode(body: bytes, encoding: str) -> str | None:
    """The body as text, undoing gzip or deflate; None for an encoding read here cannot undo (it is still passed on
    as it came)."""
    encoding = encoding.strip().lower()
    try:
        if encoding in ("gzip", "x-gzip"):
            body = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(body)
        elif encoding == "deflate":
            body = _decode_deflate(body)
        elif encoding not in ("", "identity"):
            return None
    except zlib.error:
        return None
    return body.decode("utf-8", errors="replace")


def _decode_deflate(body: bytes) -> bytes:
    """HTTP `deflate`: zlib-wrapped, as the RFC says, or raw, as some servers send it."""
    try:
        return zlib.decompressobj().decompress(body)
    except zlib.error:
        return zlib.decompressobj(-zlib.MAX_WBITS).decompress(body)


def _load_json(value: bytes | str) -> dict:
    try:
        loaded = json.loads(value)
    except ValueError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _describe(reply: Reply) -> str:
    """The activity line: the tool the model asked for (`tool bash: pytest -x`), else how it finished."""
    if reply.tool_calls:
        more = len(reply.tool_calls) - 1
        return _describe_tool(reply.tool_calls[0]) + (f" (+{more} more)" if more else "")
    tokens = f", {reply.output_tokens} tokens" if reply.output_tokens is not None else ""
    return f"model replied ({reply.finish_reason or 'unknown finish'}{tokens})"


def _describe_tool(call: ToolCall) -> str:
    arguments = call.arguments[:_TOOL_ARGUMENTS_CHARS]
    loaded = _load_json(call.arguments) if call.arguments.startswith("{") else {}
    if len(loaded) == 1 and isinstance(next(iter(loaded.values())), str):
        arguments = next(iter(loaded.values()))[:_TOOL_ARGUMENTS_CHARS]
    return f"tool {call.name}: {arguments}" if arguments else f"tool {call.name}"
