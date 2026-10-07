"""Bounded, isolated delivery of mirrored metric events to River Console.

Everything here is best effort: delivery runs on a daemon thread, memory is
bounded, and no failure is ever raised to the caller. Losing River metrics is
acceptable; disturbing training is not.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import UTC, datetime
import ipaddress
import json
import logging
import os
import random
import threading
import time
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
import urllib.request

_logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://console.river.ai"
MAX_BATCH_VALUES = 1_000
MAX_BATCH_BYTES = 1 << 20
MAX_NAME_BYTES = 512
# River Console accepts at most this many metric definitions per revision.
MAX_DEFINITIONS_PER_REVISION = 1_000
MAX_PENDING_VALUES = 10_000
MAX_PENDING_BYTES = 8 << 20
FLUSH_INTERVAL_S = 2.0
HTTP_TIMEOUT_S = 5.0
RETRY_INITIAL_S = 0.5
RETRY_MAX_S = 30.0
CLOSE_DRAIN_S = 1.0

# Bytes of the JSON envelope around the stream, definitions and events.
_ENVELOPE_BYTES = 64
_RETRYABLE_STATUSES = frozenset({408, 429})

_warned: set[str] = set()
_warned_lock = threading.Lock()


def warn_once(cause: str, message: str) -> None:
    """Emit one diagnostic per cause and process; never raises."""
    try:
        with _warned_lock:
            if cause in _warned:
                return
            _warned.add(cause)
        _logger.warning(message)
    except Exception:
        pass


def events_url(training_run_id: str, base_url: str | None = None) -> str | None:
    """Return the ingestion URL, or ``None`` when the destination is unsafe."""
    base = (base_url or os.environ.get("RIVER_CONSOLE_URL") or DEFAULT_BASE_URL).rstrip(
        "/"
    )
    parts = urlsplit(base)
    if parts.scheme != "https" and not (
        parts.scheme == "http" and _is_loopback(parts.hostname)
    ):
        return None
    return f"{base}/api/metrics/runs/{quote(training_run_id, safe='')}/events"


def _is_loopback(host: str | None) -> bool:
    if host == "localhost":
        return True
    try:
        return host is not None and ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def format_timestamp(seconds: float) -> str:
    return (
        datetime.fromtimestamp(seconds, UTC)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def encode(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), allow_nan=False).encode("utf-8")


@dataclass(frozen=True)
class _Event:
    body: bytes
    values: int
    definition_version: int | None
    enqueued_at: float


@dataclass(frozen=True)
class _Batch:
    body: bytes
    definition_versions: frozenset[int]


class _RejectRedirects(urllib.request.HTTPRedirectHandler):
    """Never forward the River API key to a redirect target."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = urllib.request.build_opener(_RejectRedirects)


def post_batch(url: str, api_key: str, user_agent: str, body: bytes) -> int | None:
    """POST one batch; return its HTTP status, or ``None`` on transport failure."""
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": user_agent,
        },
        method="POST",
    )
    try:
        with _opener.open(request, timeout=HTTP_TIMEOUT_S) as response:
            return response.getcode()
    except HTTPError as error:
        try:
            error.read()
        except Exception:
            pass
        return error.code
    except Exception:
        return None


class EventUploader:
    """Deliver one stream's events in bounded, retried, ordered batches."""

    def __init__(
        self,
        *,
        url: str,
        api_key: str,
        user_agent: str,
        stream: dict[str, Any],
        send=post_batch,
        flush_interval_s: float = FLUSH_INTERVAL_S,
    ) -> None:
        self._url = url
        self._api_key = api_key
        self._user_agent = user_agent
        self._stream = encode(stream)
        self._send = send
        self._flush_interval_s = flush_interval_s
        # Unacknowledged revisions. Only the latest can be referenced by future
        # events, so older ones are kept only while a pending event needs them.
        self._definitions: dict[int, bytes] = {}
        self._latest_definition: int | None = None
        self._references: dict[int, int] = {}
        self._acknowledged: set[int] = set()
        self._pending: deque[_Event] = deque()
        self._pending_values = 0
        self._pending_bytes = 0
        self._condition = threading.Condition()
        self._closing = False
        self._stopped = False
        self._thread: threading.Thread | None = None

    def add_definition(self, version: int, definition: dict[str, Any]) -> None:
        body = encode({"version": version, **definition})
        with self._condition:
            if self._stopped:
                return
            previous, self._latest_definition = self._latest_definition, version
            self._definitions[version] = body
            self._pending_bytes += len(body)
            if previous is not None:
                self._release_definition(previous)

    def submit(self, event: dict[str, Any]) -> None:
        body = encode(event)
        values = len(event["values"]) + len(event["axes"])
        version = event["definition_version"]
        with self._condition:
            if self._stopped or self._closing:
                return
            definition = self._definitions.get(version, b"") if version else b""
            if (
                values > MAX_BATCH_VALUES
                or self._batch_bytes(len(body), len(definition)) > MAX_BATCH_BYTES
            ):
                warn_once(
                    "oversized event",
                    "River metrics skipped a W&B history row that exceeds one "
                    "ingestion batch",
                )
                return
            self._pending.append(_Event(body, values, version, time.monotonic()))
            self._pending_values += values
            self._pending_bytes += len(body)
            if version:
                self._references[version] = self._references.get(version, 0) + 1
            while (
                self._pending_values > MAX_PENDING_VALUES
                or self._pending_bytes > MAX_PENDING_BYTES
            ) and self._pending:
                self._drop_oldest()
                warn_once(
                    "full buffer",
                    "River metrics buffer is full; dropping the oldest events",
                )
            if self._thread is None:
                self._thread = threading.Thread(
                    target=self._run, name="river-metric-events", daemon=True
                )
                self._thread.start()
            self._condition.notify()

    def close(self, timeout_s: float = CLOSE_DRAIN_S) -> None:
        """Deliver what fits into ``timeout_s``, then abandon the rest."""
        with self._condition:
            if self._closing:
                return
            self._closing = True
            thread = self._thread
            self._condition.notify()
        if thread is not None:
            thread.join(timeout_s)
        with self._condition:
            abandoned = bool(self._pending) or (
                thread is not None and thread.is_alive()
            )
            self._stop()
        if abandoned:
            warn_once(
                "close timeout",
                "River metrics stopped before delivering every buffered event",
            )

    def _batch_bytes(self, event_bytes: int, definition_bytes: int) -> int:
        return len(self._stream) + _ENVELOPE_BYTES + event_bytes + definition_bytes

    def _drop_oldest(self) -> None:
        """Remove the oldest pending event (dropped, or taken into a batch)."""
        event = self._pending.popleft()
        self._pending_values -= event.values
        self._pending_bytes -= len(event.body)
        version = event.definition_version
        if version:
            remaining = self._references.get(version, 0) - 1
            if remaining > 0:
                self._references[version] = remaining
            else:
                self._references.pop(version, None)
                self._release_definition(version)

    def _release_definition(self, version: int) -> None:
        """Forget a superseded revision that no pending event references.

        A batch that already carries it keeps its own copy of the bytes.
        """
        if version == self._latest_definition or self._references.get(version):
            return
        body = self._definitions.pop(version, b"")
        self._pending_bytes -= len(body)

    def _stop(self) -> None:
        self._stopped = True
        self._pending.clear()
        self._pending_values = 0
        self._pending_bytes = 0
        self._definitions.clear()
        self._references.clear()
        self._condition.notify_all()

    def _run(self) -> None:
        while True:
            with self._condition:
                batch = self._next_batch()
            if batch is None:
                return
            self._deliver(batch)

    def _next_batch(self) -> _Batch | None:
        while True:
            if self._stopped:
                return None
            if not self._pending:
                if self._closing:
                    return None
                self._condition.wait()
                continue
            waited = time.monotonic() - self._pending[0].enqueued_at
            if (
                self._closing
                or self._batch_is_full()
                or waited >= self._flush_interval_s
            ):
                return self._take_batch()
            self._condition.wait(self._flush_interval_s - waited)

    def _batch_is_full(self) -> bool:
        return (
            self._pending_values >= MAX_BATCH_VALUES
            or self._pending_bytes >= MAX_BATCH_BYTES
        )

    def _take_batch(self) -> _Batch:
        events: list[bytes] = []
        versions: dict[int, bytes] = {}
        values = 0
        size = len(self._stream) + _ENVELOPE_BYTES
        while self._pending:
            event = self._pending[0]
            version = event.definition_version
            definition = b""
            if (
                version
                and version not in versions
                and version not in self._acknowledged
            ):
                definition = self._definitions.get(version, b"")
            added = len(event.body) + len(definition) + 2
            if events and (
                values + event.values > MAX_BATCH_VALUES
                or size + added > MAX_BATCH_BYTES
            ):
                break
            self._drop_oldest()
            events.append(event.body)
            if definition:
                versions[version] = definition
            values += event.values
            size += added
        body = b"".join(
            [
                b'{"version":1,"stream":',
                self._stream,
                b',"definitions":[',
                b",".join(versions.values()),
                b'],"events":[',
                b",".join(events),
                b"]}",
            ]
        )
        return _Batch(body, frozenset(versions))

    def _deliver(self, batch: _Batch) -> None:
        delay = RETRY_INITIAL_S
        while True:
            status = self._send(self._url, self._api_key, self._user_agent, batch.body)
            with self._condition:
                if status is not None and 200 <= status < 300:
                    self._acknowledged.update(batch.definition_versions)
                    for version in batch.definition_versions:
                        body = self._definitions.pop(version, b"")
                        self._pending_bytes -= len(body)
                    return
                if status is not None and not (
                    status in _RETRYABLE_STATUSES or status >= 500
                ):
                    self._stop()
                    warn_once(
                        f"rejected {status}",
                        f"River Console rejected mirrored metrics with HTTP {status}; "
                        "River mirroring is disabled for this run",
                    )
                    return
                # New events notify the condition; keep the backoff anyway so an
                # outage never turns logging into a request storm.
                deadline = time.monotonic() + delay * random.uniform(0.5, 1.5)
                while (
                    not self._stopped and (remaining := deadline - time.monotonic()) > 0
                ):
                    self._condition.wait(remaining)
                if self._stopped:
                    return
            delay = min(delay * 2, RETRY_MAX_S)
