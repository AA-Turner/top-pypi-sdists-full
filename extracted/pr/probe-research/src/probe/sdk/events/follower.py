"""EventStream: the live events a query follows, in seq order and once each, across dropped connections: it
reconnects with `Last-Event-ID` and the server replays what it missed (twin: app/live)."""

from __future__ import annotations

import logging
import random
import threading
from collections.abc import Iterator

import httpx
from pydantic import ValidationError

from ... import errors
from ...generated.live import LAST_EVENT_ID_HEADER, RETRY_MILLISECONDS, LiveEvent, LiveQuery
from ..delivery.transport.streams import cut_stream
from ..delivery.transport.transport import Transport
from .query import to_query_parameters
from .sse import SseFrame, read_frames

log = logging.getLogger("probe.events")

#: The live SSE route (CONTRACT.md "Live events").
STREAM_PATH = "/v1/live/events"

#: A read waits this long for a frame: the server sends a keepalive every 15 s, so silence past it is a dead link.
READ_TIMEOUT_S = 45.0
#: Reconnect waits double from the server's `retry:` up to this.
MAX_BACKOFF_S = 30.0
#: Failures in a row past which a drop is logged as a warning.
REPEATED_FAILURES = 3
#: Statuses worth a reconnect (the server is busy, full, draining or behind a proxy blip). Any other refusal
#: (a bad credential, an unknown run, a malformed query) would only be refused again.
RETRYABLE_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})


class EventStream:
    """Iterate it for `LiveEvent`s (`resync` and `lagged` included: they are about the stream). `cursor` is the
    last seq it reached. Another thread may `close()` it: the iteration then ends."""

    def __init__(self, transport: Transport, query: LiveQuery, *, since: int | None = None,
                 read_timeout: float = READ_TIMEOUT_S) -> None:
        self.transport = transport
        self.query = query
        self.cursor = since if since is not None else query.since
        self.read_timeout = read_timeout
        #: Set while a connection is open and has sent its first frame (the server registered the stream).
        self.connected = threading.Event()
        self.reconnects = 0
        self._failures = 0
        self._retry_s = RETRY_MILLISECONDS / 1000
        self._closed = threading.Event()
        self._response: httpx.Response | None = None
        self._lock = threading.Lock()

    def __iter__(self) -> Iterator[LiveEvent]:
        return self._follow()

    def __enter__(self) -> EventStream:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    @property
    def is_closed(self) -> bool:
        return self._closed.is_set()

    def close(self) -> None:
        """Stop following: a reader blocked on the connection wakes and the iteration ends."""
        self._closed.set()
        with self._lock:
            response = self._response
        if response is not None:
            cut_stream(response)

    def _follow(self) -> Iterator[LiveEvent]:
        while not self.is_closed:
            try:
                yield from self._read_one_connection()
                # A connection that ended before its first frame counts as a failure: a server that answers and
                # hangs up at once must not be asked again every `retry:`.
                delay = self._retry_s if self._failures == 0 else self._get_backoff()
            except Exception as exc:  # noqa: BLE001 -- a close() from another thread may surface as anything
                if self.is_closed:
                    return
                delay = self._get_reconnect_delay(exc)
            if self._closed.wait(delay):
                return
            self.reconnects += 1

    def _get_reconnect_delay(self, exc: Exception) -> float:
        """How long to wait before reconnecting after `exc`; re-raises what a reconnect cannot fix."""
        if isinstance(exc, errors.RosError) and not isinstance(exc, errors.TransportError):
            if not _is_retryable(exc):
                raise exc
            delay = max(exc.retry_after or 0.0, self._get_backoff())
            log.warning("probe.events: the live server answered %s; reconnecting in %.0f s", exc.status, delay)
            return delay
        if isinstance(exc, (errors.TransportError, httpx.HTTPError, OSError)):
            delay = self._get_backoff()
            # One drop is ordinary (a pod drained); the same failure again and again is something to see.
            level = logging.WARNING if self._failures >= REPEATED_FAILURES else logging.INFO
            log.log(level, "probe.events: the live connection dropped (%s: %s); reconnecting in %.1f s",
                    type(exc).__name__, str(exc)[:200], delay)
            return delay
        raise exc

    def _read_one_connection(self) -> Iterator[LiveEvent]:
        self._failures += 1  # cleared by the first frame
        headers = {LAST_EVENT_ID_HEADER: str(self.cursor)} if self.cursor is not None else {}
        parameters = to_query_parameters(self.query.model_copy(update={"since": None}))
        try:
            with self.transport.open_stream(STREAM_PATH, read_timeout=self.read_timeout, parameters=parameters,
                                            headers=headers) as response:
                with self._lock:
                    self._response = response
                if self.is_closed:
                    return
                for frame in read_frames(response.iter_lines()):
                    if not self.connected.is_set():
                        self.connected.set()
                        self._failures = 0
                    event = self._take(frame)
                    if event is not None:
                        yield event
                    if self.is_closed:
                        return
        finally:
            self.connected.clear()
            with self._lock:
                self._response = None

    def _take(self, frame: SseFrame) -> LiveEvent | None:
        """Move the cursor past `frame`; the event it carries, unless already delivered."""
        if frame.retry_ms is not None:
            self._retry_s = max(0.1, frame.retry_ms / 1000)
        position = frame.get_position()
        if frame.data is None:
            if position is not None:
                self.cursor = position
            return None
        try:
            event = LiveEvent.model_validate_json(frame.data)
        except ValidationError as exc:
            log.warning("probe.events: skipped an event this client cannot read (%s)", exc.errors()[0]["msg"])
            if position is not None:
                self.cursor = position
            return None
        if event.is_control():
            # `resync` moves the cursor wherever the server says (even back, for a cursor it never issued).
            self.cursor = event.seq
            return event
        if self.cursor is not None and event.seq <= self.cursor:
            return None
        self.cursor = event.seq
        return event

    def _get_backoff(self) -> float:
        base = min(MAX_BACKOFF_S, self._retry_s * 2 ** max(0, self._failures - 1))
        return base * random.uniform(0.8, 1.2)


def _is_retryable(exc: errors.RosError) -> bool:
    return exc.status in RETRYABLE_STATUSES or (exc.status is not None and exc.status >= 500)
