"""HTTP client utilities for Bitfab API requests.

This module provides:
- HttpClient class for making API requests
- A bounded background sender for fire-and-forget operations
"""

from __future__ import annotations

import atexit
import itertools
import json
import logging
import math
import os
import threading
import time
import weakref
from collections.abc import Callable
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, NamedTuple, Union

import requests
from requests.adapters import HTTPAdapter

from bitfab.compress import PreparedRequest, prepare_request_body
from bitfab.constants import DEFAULT_SERVICE_URL, __version__
from bitfab.git_state import is_empty_git_state, resolved_git_state
from bitfab.otel import _MAX_EXPORT_CONCURRENCY
from bitfab.payload_budget import (
    MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES,
    MAX_SPAN_CARRIER_BYTES,
    enforce_payload_budget,
)
from bitfab.replay_invocation import ReplayInvocation
from bitfab.serialize import encode_json, to_json_safe_report
from bitfab.simulation_plan import (
    DECLARED_IN_CODE_FIELD,
    NO_API_KEY_FOR_SIM_PLAN,
    ROOT_TRACE_FUNCTION_KEY_FIELD,
    plan_wait_slice,
)
from bitfab.simulation_plan import (
    READ_TIMEOUT_SECONDS as SIM_PLAN_READ_TIMEOUT_SECONDS,
)
from bitfab.trace_completion import TraceCompletion
from bitfab.trace_metadata import merge_caller_metadata_into_trace_payload
from bitfab.transport import (
    create_trace_transport,
    flush_trace_transports,
    shutdown_trace_transports,
)
from bitfab.transport_types import (
    CarrierMeta,
    CarrierRef,
    DeliveryError,
    TraceTransport,
)
from bitfab.warn_once import warn_once

logger = logging.getLogger(__name__)

_OTLP_TRACES_ENDPOINT = "/api/sdk/otel/v1/traces"
_REPLAY_DB_BRANCH_REQUEST_TIMEOUT_SECONDS = 300
_REPLAY_COMPLETE_REQUEST_TIMEOUT_SECONDS = 120
_REPLAY_INTERRUPT_REQUEST_TIMEOUT_SECONDS = 5
_REPLAY_HEARTBEAT_REQUEST_TIMEOUT_SECONDS = 5
_EXIT_FLUSH_SECONDS = 4.0
_HTTP_POOL_MAXSIZE = _MAX_EXPORT_CONCURRENCY

# How the API key is supplied: a literal string, or a function resolved each
# time the key is needed (at request time). The function form defers key
# resolution past construction so an env var loaded after the client is built
# is still picked up.
ApiKeyInput = Union[str, Callable[[], str | None]]


def _encode_payload(
    payload: dict[str, Any], max_carrier_bytes: int = MAX_SPAN_CARRIER_BYTES
) -> tuple[Any, str, list[str]]:
    """Encode a request body to JSON-safe primitives, without ever raising and
    within the per-span byte budget.

    Returns ``(safe_payload, body, dropped)``. ``body`` is the encoded form the
    caller sends, so the encode that proves the payload is serializable is the
    only encode it costs. ``dropped`` lists the type names that had to be
    stubbed, so the caller can warn loudly rather than ship a degraded payload
    in silence.

    Upstream serialization (``serialize_value`` / ``to_json_safe``) should
    already have flattened user data, so the common case is a clean payload.
    The slow paths below run only when something non-serializable slipped
    through, and stub the stray rather than letting the wire-side encoder raise
    and drop the whole span/trace silently.
    """
    safe, body, dropped = _encode_payload_unbounded(payload)
    safe, body, trimmed = enforce_payload_budget(
        safe, body, encode_json, max_carrier_bytes
    )
    if trimmed:
        warn_once(
            "payload-over-budget",
            f"a span payload exceeded the {max_carrier_bytes}-byte carrier budget; its "
            f"largest field(s) ({', '.join(dict.fromkeys(trimmed))}) were "
            "replaced with placeholders so the span still ships. The span is "
            "incomplete and may not be replayable.",
        )
    # `dropped` names values that could not be encoded, which drives the
    # "non-serializable value(s)" warning. A budget trim is a size decision, not
    # an encoding failure, and already has its own warning and payload_budget
    # error entry, so it must not be reported as one.
    return safe, body, dropped


def _encode_payload_unbounded(payload: dict[str, Any]) -> tuple[Any, str, list[str]]:
    try:
        return payload, encode_json(payload), []
    except (TypeError, ValueError):
        pass

    dropped: list[str] = []

    def record_drop(name: str) -> None:
        if name not in dropped:
            dropped.append(name)

    def _fallback(value: Any) -> str:
        # When the stray value is itself a class (the common case: a Pydantic
        # model class / ModelMetaclass used as a tool's args_schema), report the
        # class's own name, not its metaclass ("type"), so the warning names the
        # real culprit.
        described = value if isinstance(value, type) else type(value)
        name = getattr(described, "__qualname__", None) or described.__name__
        record_drop(name)
        return f"<unserializable: {name}>"

    try:
        body = json.dumps(
            payload, default=_fallback, separators=(",", ":"), allow_nan=False
        )
        return json.loads(body), body, dropped
    except Exception:
        # default= can't rescue some structures (a cycle, or a non-string dict
        # key) - json raises before/regardless of default. Fall back to the
        # shared walker so bad leaves are stubbed and siblings survive, instead
        # of discarding the whole span. Reuse its loss report so warnings name
        # the actual degraded values rather than a generic structure error.
        dropped.clear()
        found_non_finite = False
        try:
            json.dumps(payload, default=lambda _value: "<unserializable>")
        except Exception:
            has_unreported_structure_loss = True
        else:
            has_unreported_structure_loss = False
        safe, walker_dropped = to_json_safe_report(payload)
        for name in walker_dropped:
            record_drop(name)

        def replace_non_finite(value: Any) -> Any:
            nonlocal found_non_finite
            if isinstance(value, float) and not math.isfinite(value):
                found_non_finite = True
                return "<unserializable: non_finite_float>"
            if isinstance(value, dict):
                return {key: replace_non_finite(item) for key, item in value.items()}
            if isinstance(value, list):
                return [replace_non_finite(item) for item in value]
            return value

        safe = replace_non_finite(safe)
        if found_non_finite:
            record_drop("non_finite_float")
        if has_unreported_structure_loss and not walker_dropped:
            record_drop("unserializable_structure")
        try:
            body = encode_json(safe)
            return json.loads(body), body, dropped
        except Exception as e:
            # Truly pathological. Still never drop silently: send a marker body.
            marker = {"error": f"payload_encode_failed: {e}"}
            return marker, encode_json(marker), dropped


def _warn_for_dropped_values(dropped: list[str]) -> None:
    if not dropped:
        return
    warn_once(
        "request-body-stubbed",
        "a request body held non-serializable value(s) (e.g. "
        f"{', '.join(sorted(set(dropped)))}); they were stubbed so the "
        "span still sends, but the trace may be incomplete or not "
        "replayable. Capture a JSON-safe projection of this input to "
        "make it replayable.",
    )


_live_http_clients: weakref.WeakSet[HttpClient] = weakref.WeakSet()
_live_http_clients_lock = threading.Lock()


def _reset_http_globals_after_fork() -> None:
    global _live_http_clients_lock
    _live_http_clients_lock = threading.Lock()
    for client in list(_live_http_clients):
        client._trace_transport_lock = threading.Lock()
        client._delivery_lock = threading.Lock()
        client._session_lock = threading.Lock()
        client._session = None
        client._trace_deliveries = {}
        client.trace_completion = TraceCompletion()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_http_globals_after_fork)


def _build_session() -> requests.Session:
    session = requests.Session()
    adapter = HTTPAdapter(pool_maxsize=_HTTP_POOL_MAXSIZE)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def _release_held_external_spans(timeout: float) -> bool:
    deadline = time.monotonic() + max(timeout, 0.0)
    with _live_http_clients_lock:
        clients = list(_live_http_clients)
    released = True
    for client in clients:
        release = client.release_held_external_spans
        if release is not None:
            result = release(max(0.0, deadline - time.monotonic()))
            released = result is not False and released
    return released


def _stop_simulation_plans() -> None:
    with _live_http_clients_lock:
        clients = list(_live_http_clients)
    for client in clients:
        stop = client.stop_simulation_plan
        if stop is not None:
            stop()


def _wait_for_pending_traces() -> None:
    """Flush and shut down trace transports.

    This is registered as an atexit handler to ensure traces are delivered
    before the process exits.
    """
    _release_held_external_spans(SIM_PLAN_READ_TIMEOUT_SECONDS)
    _stop_simulation_plans()
    shutdown_trace_transports(_EXIT_FLUSH_SECONDS)


# Register the atexit handler
atexit.register(_wait_for_pending_traces)


def flush_traces(timeout: float = 30.0) -> bool:
    """Wait for all pending traces to reach the server.

    Call this method before exiting if you want to ensure all traces
    are sent to the server. This is automatically called via atexit,
    but can be called explicitly if needed.

    Args:
        timeout: Maximum total seconds to wait (default: 30.0)

    Returns:
        True when all pending traces were delivered within the deadline,
        or False when delivery failed or requests were still running.
    """
    deadline = time.monotonic() + max(timeout, 0)
    released = _release_held_external_spans(plan_wait_slice(timeout))
    flushed = flush_trace_transports(max(0.0, deadline - time.monotonic()))
    return released and flushed


class DeliveryReport(NamedTuple):
    """What a caller learns about one tracked trace once it takes it back."""

    span_count: int
    # A closing carrier was submitted, so the expected set is final.
    closed: bool
    # Every carrier submitted under this trace came back accepted.
    delivered: bool
    # The server's assigned traces.id, read back off the OTLP ingest response.
    # None when the server predates this field or nothing was acked yet.
    server_trace_id: str | None = None


class _TraceDelivery:
    def __init__(self) -> None:
        self.submitted_span_ids: set[str] = set()
        self.acked_span_ids: set[str] = set()
        self.closed = False
        self.closing_acked = False
        self.server_trace_id: str | None = None


def _parse_retry_after_ms(header: str | None) -> float | None:
    """``Retry-After`` as milliseconds.

    The header is either a delay in seconds or an HTTP date; both forms appear
    in the wild, so both are read. Anything else, or a date already in the past,
    yields None so the caller falls back to its own backoff.
    """
    if not isinstance(header, str) or not header:
        return None
    try:
        seconds = float(header)
    except (TypeError, ValueError):
        pass
    else:
        return seconds * 1_000 if seconds >= 0 else None
    try:
        at = parsedate_to_datetime(header)
    except (TypeError, ValueError):
        return None
    if at is None:
        return None
    if at.tzinfo is None:
        at = at.replace(tzinfo=timezone.utc)
    return max(0.0, (at - datetime.now(timezone.utc)).total_seconds() * 1_000)


def _carrier_meta(
    operation: str, payload: dict[str, Any], ref: CarrierRef | None
) -> CarrierMeta:
    """Everything the transport needs to know about a carrier, derived here
    because this is where the payload shape is owned. The transport applies
    these and never looks inside a payload itself.
    """
    return CarrierMeta(
        ref=ref,
        name=_carrier_name(operation, payload),
        start_time_ns=_payload_timestamp_ns(payload, "started_at"),
        end_time_ns=_payload_timestamp_ns(payload, "ended_at"),
        errored=_payload_has_error(payload),
    )


def _carrier_name(operation: str, payload: dict[str, Any]) -> str:
    if operation == "external_span":
        raw_span = payload.get("rawSpan")
        if isinstance(raw_span, dict):
            span_data = raw_span.get("span_data")
            if isinstance(span_data, dict) and isinstance(span_data.get("name"), str):
                return span_data["name"]
    if isinstance(payload.get("traceFunctionKey"), str):
        return payload["traceFunctionKey"]
    return f"bitfab.{operation}"


def _payload_timestamp_ns(payload: dict[str, Any], field: str) -> int | None:
    raw: Any = None
    raw_span = payload.get("rawSpan")
    if isinstance(raw_span, dict):
        raw = raw_span.get(field)
    if raw is None:
        raw_trace = payload.get("externalTrace") or payload.get("rawTrace")
        if isinstance(raw_trace, dict):
            raw = raw_trace.get(field)
    if isinstance(raw, str):
        try:
            return int(
                datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp() * 1e9
            )
        except (OverflowError, TypeError, ValueError):
            pass
    return None


def _payload_has_error(payload: dict[str, Any]) -> bool:
    raw_span = payload.get("rawSpan")
    if isinstance(raw_span, dict):
        span_data = raw_span.get("span_data")
        if isinstance(span_data, dict) and span_data.get("error") is not None:
            return True
    errors = payload.get("errors")
    if not isinstance(errors, list):
        return bool(errors)
    # Entries the SDK wrote about itself (a budget trim, a stubbed value) report
    # an incomplete capture, not a failed operation, so they must not mark the
    # carrier errored: a large payload is normal traffic, and flagging it would
    # turn every oversized span into an error in the user's dashboards. The
    # payload still carries the entry, which is what tells the server the trace
    # is incomplete.
    return any(
        not (isinstance(entry, dict) and entry.get("source") == "sdk")
        for entry in errors
    )


# itertools.count, not a bare int: `+= 1` on a module global is a
# read-modify-write that two submitting threads can interleave, minting the same
# id twice. Two carriers sharing an id collapse into one ledger entry, so a
# single ack would mark both delivered. Its __next__ is atomic, which is what
# Ruby spends a mutex on.
_carrier_seq = itertools.count(1)


def _carrier_ref(payload: dict[str, Any]) -> CarrierRef | None:
    """The delivery identity of a carrier, read from the payload here because
    this is where the payload shape is owned. The transport is handed the result
    and never looks inside a payload itself.
    """
    trace_id = payload.get("sourceTraceId")
    if not isinstance(trace_id, str):
        raw_trace = payload.get("externalTrace") or payload.get("rawTrace")
        trace_id = raw_trace.get("id") if isinstance(raw_trace, dict) else None
    if not isinstance(trace_id, str):
        return None

    raw_span = payload.get("rawSpan")
    if raw_span is None:
        return CarrierRef(trace_id)
    span_id = raw_span.get("id") if isinstance(raw_span, dict) else None
    if not isinstance(span_id, str):
        span_id = f"submission-{next(_carrier_seq)}"
    return CarrierRef(trace_id, span_id)


class HttpClient:
    """HTTP client for Bitfab API requests.

    Provides methods for different API endpoints with proper error handling,
    timeouts, and authentication.
    """

    def __init__(
        self,
        api_key: ApiKeyInput | None = None,
        service_url: str | None = None,
        timeout: float = 120.0,
    ):
        """Initialize the HTTP client.

        Args:
            api_key: The API key for authentication, either a string or a
                function resolved at request time (never read at construction).
            service_url: The base URL for the Bitfab API
            timeout: Default request timeout in seconds
        """
        self.api_key = api_key
        self.service_url = (service_url or DEFAULT_SERVICE_URL).rstrip("/")
        self.timeout = timeout
        self._trace_transport_lock = threading.Lock()
        # Only traces a caller asked about are tracked, so ordinary tracing stores
        # nothing here. Written from exporter threads, hence the lock.
        self.trace_completion = TraceCompletion()
        self._delivery_lock = threading.Lock()
        self._trace_deliveries: dict[str, _TraceDelivery] = {}
        self._trace_transport: TraceTransport | None = None
        self._closed = False
        self._close_result = True
        self._close_complete = threading.Event()
        self._session_lock = threading.Lock()
        self._session: requests.Session | None = None
        self._session_pid = os.getpid()
        self.external_span_sender: (
            Callable[[dict[str, Any], Callable[[dict[str, Any]], None]], None] | None
        ) = None
        self.external_trace_sender: (
            Callable[[dict[str, Any], Callable[[dict[str, Any]], None]], None] | None
        ) = None
        self.release_held_external_spans: Callable[[float], bool | None] | None = None
        self.stop_simulation_plan: Callable[[], None] | None = None
        with _live_http_clients_lock:
            _live_http_clients.add(self)

    def wait_for_pending_requests(self, timeout: float = 30.0) -> bool:
        """Wait for requests started by this client within one total deadline."""
        deadline = time.monotonic() + max(timeout, 0)
        release = self.release_held_external_spans
        released = (
            release(plan_wait_slice(timeout)) is not False
            if release is not None
            else True
        )
        with self._trace_transport_lock:
            transport = self._trace_transport
        if transport is None:
            return released
        flushed = transport.flush(max(0.0, deadline - time.monotonic()))
        return released and flushed

    def close(self, timeout: float = 30.0) -> bool:
        """Flush and permanently close this client's tracing transports."""
        deadline = time.monotonic() + max(timeout, 0)
        release = self.release_held_external_spans
        released = True
        if release is not None and not self._closed:
            released = release(plan_wait_slice(timeout)) is not False
        if not self._closed:
            stop = self.stop_simulation_plan
            if stop is not None:
                stop()
            self.external_span_sender = None
            self.external_trace_sender = None
            self.release_held_external_spans = None
            self.stop_simulation_plan = None
        if not self._trace_transport_lock.acquire(
            timeout=max(0.0, deadline - time.monotonic())
        ):
            return False
        try:
            if self._closed:
                close_complete = self._close_complete
                transport = None
                already_closed = True
            else:
                self._closed = True
                close_complete = self._close_complete
                transport = self._trace_transport
                self._trace_transport = None
                already_closed = False
        finally:
            self._trace_transport_lock.release()

        if already_closed:
            if not close_complete.wait(max(0.0, deadline - time.monotonic())):
                return False
            return self._close_result

        succeeded = True
        try:
            if transport is not None:
                succeeded = transport.shutdown(max(0.0, deadline - time.monotonic()))
        except Exception:
            logger.exception("Bitfab: failed to close tracing resources")
            succeeded = False
        finally:
            self._close_session()
            self._close_result = released and succeeded
            close_complete.set()
        return self._close_result

    def _http_session(self) -> requests.Session:
        current_pid = os.getpid()
        with self._session_lock:
            if self._session is not None and self._session_pid == current_pid:
                return self._session
            self._session = _build_session()
            self._session_pid = current_pid
            return self._session

    def _close_session(self) -> None:
        with self._session_lock:
            session = self._session
            owned_here = self._session_pid == os.getpid()
            self._session = None
        if session is not None and owned_here:
            session.close()

    def _get_trace_transport(self) -> TraceTransport:
        with self._trace_transport_lock:
            if self._closed:
                raise RuntimeError("Bitfab client is closed")
            if self._trace_transport is None:
                self._trace_transport = create_trace_transport(
                    direct_sender=self._deliver_carriers,
                    on_delivered=self._record_delivered_carriers,
                )
            return self._trace_transport

    def _deliver_carriers(self, request: PreparedRequest, timeout: float) -> None:
        """Post one encoded batch and decide what the server's answer means, so
        the transport never reads a response. Rejections and permanent statuses
        come back as a non-retryable DeliveryError; anything the server might
        still accept on a second try comes back retryable.
        """
        try:
            # send_prepared, not send_encoded: the exporter already encoded this
            # batch to size the request, and re-encoding would do it twice.
            response = self.send_prepared(
                _OTLP_TRACES_ENDPOINT,
                request,
                timeout=timeout,
                max_retries=1,
                # The transport owns retries and reports export failures, so a
                # second log line here would double-report every rejection.
                log_errors=False,
            )
        except requests.exceptions.RequestException as error:
            status = error.response.status_code if error.response is not None else None
            if status is None:
                # No verdict from the server (a network fault): worth retrying.
                raise DeliveryError(
                    f"OTLP ingestion failed: {error}", retryable=True
                ) from error
            headers = getattr(error.response, "headers", None) or {}
            raise DeliveryError(
                f"OTLP ingestion failed with HTTP {status}",
                # OTLP's retryable set, plus 500. Every other 4xx is the
                # server's verdict on the payload and will be the same next
                # time.
                #
                # 500 is a deliberate deviation: OTLP treats it as the app
                # being broken, which assumes a collector that fails
                # deterministically. Bitfab ingestion answers every unhandled
                # error with 500, so a connection blip or a cold start arrives
                # here indistinguishable from a real fault, and giving up on
                # the first one drops spans a second attempt would deliver.
                retryable=status in {429, 500, 502, 503, 504},
                oversized=status == 413,
                retry_after_ms=_parse_retry_after_ms(headers.get("Retry-After")),
            ) from error

        server_trace_ids = response.get("traceIds")
        if isinstance(server_trace_ids, dict):
            self._record_server_trace_ids(server_trace_ids)

        partial_success = response.get("partialSuccess", {})
        rejected = partial_success.get("rejectedSpans")
        if rejected not in {None, "0", 0}:
            # The server's verdict on the payload, not a transient fault.
            raise DeliveryError(
                f"OTLP ingestion rejected {rejected} span(s): "
                f"{partial_success.get('errorMessage', 'no reason provided')}"
            )

    def track_trace_deliveries(self, trace_ids: list[str]) -> None:
        """Start tracking delivery for trace_ids. Nothing is recorded for a
        trace that was never tracked, so ordinary tracing costs no bookkeeping.
        """
        with self._delivery_lock:
            for trace_id in trace_ids:
                self._trace_deliveries.setdefault(trace_id, _TraceDelivery())

    def has_closed_deliveries(self, trace_ids: list[str]) -> bool:
        """Whether any tracked trace has had its closing carrier submitted."""
        with self._delivery_lock:
            return any(
                self._trace_deliveries[trace_id].closed
                for trace_id in trace_ids
                if trace_id in self._trace_deliveries
            )

    def take_trace_deliveries(self, trace_ids: list[str]) -> dict[str, DeliveryReport]:
        """Report what each tracked trace submitted and whether the server
        confirmed it, and stop tracking them. Every id passed is freed, so a
        caller cannot leak a record for a trace that never closed.

        ``delivered`` is only meaningful once a flush has settled: acks land
        before an export returns, so a flush that reported success has already
        collected every ack it is going to collect.
        """
        reports: dict[str, DeliveryReport] = {}
        with self._delivery_lock:
            for trace_id in trace_ids:
                delivery = self._trace_deliveries.pop(trace_id, None)
                if delivery is None:
                    continue
                reports[trace_id] = DeliveryReport(
                    len(delivery.submitted_span_ids),
                    delivery.closed,
                    delivery.closing_acked
                    and delivery.submitted_span_ids.issubset(delivery.acked_span_ids),
                    delivery.server_trace_id,
                )
        return reports

    def peek_server_trace_id(self, trace_id: str) -> str | None:
        """The server's assigned traces.id for a tracked trace if it has already
        been read back off an ingest response, without stopping tracking. Lets a
        replay surface the id mid-run for items whose spans already landed.
        """
        with self._delivery_lock:
            delivery = self._trace_deliveries.get(trace_id)
            return delivery.server_trace_id if delivery is not None else None

    def _record_server_trace_ids(self, mapping: dict[str, object]) -> None:
        """Record the server's assigned traces.id for each tracked source trace,
        read back off the OTLP ingest response. Keyed by source trace id, the
        same key the delivery ledger uses. Untracked ids are ignored.

        Called on exporter threads, hence the lock.
        """
        with self._delivery_lock:
            for source_trace_id, server_trace_id in mapping.items():
                if not isinstance(server_trace_id, str):
                    continue
                delivery = self._trace_deliveries.get(source_trace_id)
                if delivery is None:
                    continue
                delivery.server_trace_id = server_trace_id

    def _record_submitted_carrier(self, ref: CarrierRef | None) -> None:
        if ref is None:
            return
        with self._delivery_lock:
            delivery = self._trace_deliveries.get(ref.trace_id)
            if delivery is None:
                return
            if ref.span_id is None:
                delivery.closed = True
            else:
                delivery.submitted_span_ids.add(ref.span_id)

    def _record_delivered_carriers(self, refs: list[CarrierRef]) -> None:
        """Ingestion commits every carrier in a request before it answers, so a
        delivered ref is proof its row exists: the same fact the replay status
        endpoint would report, already in hand.

        Called on exporter threads, hence the lock.
        """
        with self._delivery_lock:
            for ref in refs:
                delivery = self._trace_deliveries.get(ref.trace_id)
                if delivery is None:
                    continue
                if ref.span_id is None:
                    delivery.closing_acked = True
                else:
                    delivery.acked_span_ids.add(ref.span_id)

    def _recorded_meta(
        self, operation: str, payload: dict[str, Any], ref: CarrierRef | None
    ) -> CarrierMeta:
        """Build a carrier's meta and record what it adds to its expected set."""
        self._record_submitted_carrier(ref)
        return _carrier_meta(operation, payload, ref)

    def _resolve_api_key(self) -> str | None:
        """Resolve the API key at the moment it is needed (request time),
        invoking the function form if one was supplied. Never read at
        construction."""
        return self.api_key() if callable(self.api_key) else self.api_key

    def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
        max_retries: int = 1,
        retry_delay: float = 0.1,
        method: str = "POST",
        log_errors: bool = True,
    ) -> dict[str, Any]:
        """Make an HTTP request to the Bitfab API. Defaults to POST.

        Args:
            endpoint: The API endpoint (without base URL)
            payload: The request body
            timeout: Request timeout in seconds (uses default if not specified)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            method: HTTP verb (POST, PATCH, PUT). Defaults to POST.
            log_errors: Whether to log the final request error before raising.

        Returns:
            The parsed JSON response

        Raises:
            ValueError: If the response contains an error
            requests.exceptions.RequestException: If the request fails
        """
        # Sanitize once, before the retry loop, so a stray non-serializable
        # value can never abort the send (which would drop the span and leave
        # the trace silently non-replayable). A degraded payload warns loudly.
        _, body, dropped = _encode_payload(payload)
        _warn_for_dropped_values(dropped)
        return self.send_encoded(
            endpoint,
            body,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            method=method,
            log_errors=log_errors,
        )

    def send_encoded(
        self,
        endpoint: str,
        body: str,
        timeout: float | None = None,
        max_retries: int = 1,
        retry_delay: float = 0.1,
        method: str = "POST",
        log_errors: bool = True,
    ) -> dict[str, Any]:
        """Send an already-encoded request body.

        The span transport encodes its own batches, so routing them back through
        :meth:`request` would encode the same data twice.
        """
        return self.send_prepared(
            endpoint,
            prepare_request_body(body),
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            method=method,
            log_errors=log_errors,
        )

    def send_prepared(
        self,
        endpoint: str,
        prepared: PreparedRequest,
        timeout: float | None = None,
        max_retries: int = 1,
        retry_delay: float = 0.1,
        method: str = "POST",
        log_errors: bool = True,
    ) -> dict[str, Any]:
        """Send bytes that have already been compressed and sized."""
        url = f"{self.service_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._resolve_api_key() or ''}",
        }
        request_timeout = timeout if timeout is not None else self.timeout
        if prepared.content_encoding is not None:
            headers["Content-Encoding"] = prepared.content_encoding

        last_exception: Exception | None = None

        for attempt in range(max_retries):
            try:
                session = self._http_session()
                if method == "POST":
                    response = session.post(
                        url,
                        data=prepared.body,
                        headers=headers,
                        timeout=request_timeout,
                    )
                else:
                    response = session.request(
                        method,
                        url,
                        data=prepared.body,
                        headers=headers,
                        timeout=request_timeout,
                    )
                response.raise_for_status()

                result = response.json()

                # Check for errors in the response
                if "error" in result:
                    if "url" in result:
                        raise ValueError(
                            f"{result['error']} Configure it at: {self.service_url}{result['url']}"
                        )
                    raise ValueError(result["error"])

                return result

            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < max_retries - 1:
                    logger.debug(f"Request attempt {attempt + 1} failed, retrying: {e}")
                    time.sleep(retry_delay)
                elif log_errors:
                    logger.error(f"Request failed after {max_retries} attempts: {e}")
                    if hasattr(e, "response") and e.response is not None:
                        logger.error(f"Response: {e.response.text[:500]}")

        if last_exception:
            raise last_exception
        raise RuntimeError("Unexpected error in request")

    def get(
        self,
        endpoint: str,
        timeout: float | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP GET request to the Bitfab API.

        Args:
            endpoint: The API endpoint (without base URL)
            timeout: Request timeout in seconds (uses default if not specified)
            extra_headers: Additional headers to send with this one request

        Returns:
            The parsed JSON response

        Raises:
            ValueError: If the response contains an error
            requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.service_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._resolve_api_key() or ''}",
            **(extra_headers or {}),
        }
        request_timeout = timeout if timeout is not None else self.timeout

        response = self._http_session().get(
            url,
            headers=headers,
            timeout=request_timeout,
        )
        response.raise_for_status()

        result = response.json()

        if "error" in result:
            if "url" in result:
                raise ValueError(
                    f"{result['error']} Configure it at: {self.service_url}{result['url']}"
                )
            raise ValueError(result["error"])

        return result

    def lookup_function(self, name: str) -> dict[str, Any]:
        """Look up a function by name.

        Blocks until complete - needed for function execution.

        Args:
            name: The function name to look up

        Returns:
            Function version data including BAML prompt and providers
        """
        return self.request("/api/sdk/functions/lookup", {"name": name})

    def get_simulation_plan(self) -> dict[str, Any]:
        # Without a key the server answers 401, so skip the request entirely.
        if not (self._resolve_api_key() or "").strip():
            raise ValueError(NO_API_KEY_FOR_SIM_PLAN)
        return self.get(
            "/api/sdk/sim-plan",
            timeout=SIM_PLAN_READ_TIMEOUT_SECONDS,
        )

    def send_internal_trace(
        self,
        function_id: str,
        payload: dict[str, Any],
    ) -> None:
        """Send an internal trace (from BAML execution).

        Fire-and-forget through this client's bounded trace transport.

        Args:
            function_id: The function ID
            payload: The trace payload (result, inputs, rawCollector, source)
        """
        safe_payload, body, dropped = _encode_payload(
            {
                **payload,
                "functionId": function_id,
                "sdkVersion": __version__,
            },
            MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES,
        )
        _warn_for_dropped_values(dropped)
        self._get_trace_transport().submit(
            "internal_trace",
            safe_payload,
            body,
            _carrier_meta("internal_trace", safe_payload, None),
        )

    def send_external_span(self, payload: dict[str, Any]) -> None:
        """Send an external span (from span decorator or OpenAI tracing).

        Fire-and-forget through this client's bounded trace transport.

        Args:
            payload: The span payload

        """
        ref = _carrier_ref(payload)
        if ref is not None and ref.span_id is not None:
            self.trace_completion.record(ref.trace_id, ref.span_id)
        sender = self.external_span_sender
        if sender is not None:
            sender(payload, self.submit_external_span)
            return
        self.submit_external_span(payload)

    def submit_external_span(self, payload: dict[str, Any]) -> None:
        wire = {**payload, "sdkVersion": __version__}
        wire.pop(ROOT_TRACE_FUNCTION_KEY_FIELD, None)
        wire.pop(DECLARED_IN_CODE_FIELD, None)
        safe_payload, body, dropped = _encode_payload(
            wire,
            MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES,
        )
        _warn_for_dropped_values(dropped)
        self._get_trace_transport().submit(
            "external_span",
            safe_payload,
            body,
            self._recorded_meta("external_span", payload, _carrier_ref(payload)),
        )

    def start_replay(
        self,
        trace_function_key: str,
        limit: int | None,
        *,
        trace_ids: list[str] | None = None,
        name: str | None = None,
        notes: str | None = None,
        metadata: dict[str, str] | None = None,
        code_change_description: str | None = None,
        code_change_files: list[dict[str, str]] | None = None,
        experiment_group_id: str | None = None,
        include_db_branch_lease: bool = False,
        include_original_metadata: bool = False,
        dataset_ids: list[str] | None = None,
        grader_ids: list[str] | None = None,
        db_branch_settings: dict[str, Any] | None = None,
        only_with_assertions: bool = False,
        skip_assertion_judging: bool = False,
        attempts: int = 1,
        experimental_selective_replay: dict[str, Any] | None = None,
        dry_run: bool = False,
        invocation: ReplayInvocation | None = None,
    ) -> dict[str, Any]:
        """Start a replay session by fetching historical traces.

        Blocking call. Creates an experiment and returns lightweight item references.

        Args:
            trace_function_key: The trace function key to replay
            limit: Maximum number of traces to replay. Pass ``None`` with
                ``trace_ids`` (the ID list determines the count and the field
                is omitted from the request).
            trace_ids: Optional list of trace IDs to filter which traces are replayed
            name: What this run is testing, in a few words, such as
                'baseline' or 'shorter system prompt'. Bitfab records the
                commit, branch, tree state, datasets, and who ran it with every
                experiment, so do not repeat them here.
            notes: Run conditions Bitfab cannot see on its own, such as an
                environment override or a forced feature flag. Kept on the
                experiment next to its name.
            metadata: Caller-owned tags on the experiment, such as which
                schedule launched it. Read back and filtered on through
                ``client.experiments``.
            code_change_description: Optional rationale for the code change being
                tested in this replay. Stored on the resulting experiment.
            code_change_files: Optional list of files edited as part of this code
                change, each as ``{"path": str, "before": str, "after": str}``.
                Use empty strings for newly created (``before``) or deleted
                (``after``) files.
            experiment_group_id: Optional UUID that groups multiple replay runs
                into a single experiment batch. The experiments page can stream
                results live by filtering on this ID.
            include_db_branch_lease: When True, the server resolves each root
                span's ``db_snapshot_ref`` into a per-item ``dbBranchLease``
                (Neon snapshot + restore) before returning. Set when the caller
                passes ``db_branch`` to ``replay``.
            include_original_metadata: When True, each item carries the
                original trace's stored metadata as ``originalMetadata``. Set
                when the caller passes ``adapt_inputs``, which is the only
                reader; the server pays one raw-trace read per item for it.
            dataset_ids: Optional dataset UUIDs this replay runs against. The
                run replays the union of their traces, graded by the union of
                their graders, and is attributed to every one of them. A single
                id travels as ``datasetId`` so a new SDK keeps working against a
                server that predates ``datasetIds``. Validated server-side
                against the org.
            grader_ids: Optional list of grader UUIDs attached directly to this
                experiment (max 100). At completion they are graded as the union
                with the dataset's runnable graders. Use it to grade a single run
                with a check you don't want to add permanently. Each must be an
                active/live grader in the same org and trace function, or the
                server rejects the replay.
            only_with_assertions: When True, the server narrows whatever the
                other selectors chose to the traces carrying at least one
                approved assertion (sent only when True). An assertion awaiting
                review is not checked on a replay and does not qualify a trace.
            attempts: How many times each source trace replays in this run (sent only when above 1).
            experimental_selective_replay: Optional wire-format mustRun
                manifest for the server-owned selective replay plan.
            dry_run: When True, the server selects the items and creates no
                experiment, answering with a null experimentId and
                experimentUrl (sent only when True).

        Returns:
            Dict with experimentId, experimentUrl, and items array
            (each item has traceId and externalSpanId)
        """
        payload: dict[str, Any] = {
            "traceFunctionKey": trace_function_key,
        }
        if limit is not None:
            payload["limit"] = limit
        if trace_ids is not None:
            payload["traceIds"] = trace_ids
        if name is not None:
            payload["name"] = name
        if notes is not None:
            payload["notes"] = notes
        if metadata is not None:
            payload["metadata"] = metadata
        if code_change_description is not None:
            payload["codeChangeDescription"] = code_change_description
        if code_change_files is not None:
            payload["codeChangeFiles"] = code_change_files
        if experiment_group_id is not None:
            payload["experimentGroupId"] = experiment_group_id
        if include_db_branch_lease:
            payload["includeDbBranchLease"] = True
            payload["lazyDbBranchLease"] = True
        if include_original_metadata:
            payload["includeOriginalMetadata"] = True
        if dataset_ids is not None:
            if len(dataset_ids) == 1:
                payload["datasetId"] = dataset_ids[0]
            else:
                payload["datasetIds"] = dataset_ids
        if grader_ids is not None:
            payload["graderIds"] = grader_ids
        if db_branch_settings is not None:
            payload["dbBranchSettings"] = db_branch_settings
        if not skip_assertion_judging:
            payload["judgeAssertions"] = True
        if only_with_assertions:
            payload["onlyWithAssertions"] = True
        if attempts > 1:
            payload["attempts"] = attempts
        if experimental_selective_replay is not None:
            payload["experimentalSelectiveReplay"] = experimental_selective_replay
        if dry_run:
            payload["dryRun"] = True
        if invocation is not None:
            payload["invocation"] = invocation
        git_state = resolved_git_state()
        if git_state is not None and not is_empty_git_state(git_state):
            payload["git"] = git_state

        # When DB branching is on, the server resolves a Neon preview branch per
        # item (snapshot + restore + poll), which can run several seconds each,
        # and runs any warm-up SQL against each branch on a 240s budget of its
        # own. The server gives up at 280s and answers, so this is a backstop
        # for a reply that never comes rather than the thing that normally
        # fires; it sits above the server's own ceiling so the server's error
        # is the one callers see.
        timeout = (
            _REPLAY_DB_BRANCH_REQUEST_TIMEOUT_SECONDS if include_db_branch_lease else 30
        )
        return self.request(
            "/api/sdk/replay/start",
            payload,
            timeout=timeout,
        )

    def resume_replay(
        self,
        experiment_id: str,
        trace_function_key: str,
        *,
        code_change_files: list[dict[str, str]] | None = None,
        force: bool = False,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "experimentId": experiment_id,
            "traceFunctionKey": trace_function_key,
            "lazyDbBranchLease": True,
        }
        if code_change_files is not None:
            payload["codeChangeFiles"] = code_change_files
        if force:
            payload["force"] = True
        git_state = resolved_git_state()
        if git_state is not None and not is_empty_git_state(git_state):
            payload["git"] = git_state
        return self.request(
            "/api/sdk/replay/resume",
            payload,
            timeout=_REPLAY_DB_BRANCH_REQUEST_TIMEOUT_SECONDS,
        )

    def get_external_span(
        self, span_id: str, *, replay_view: bool = False
    ) -> dict[str, Any]:
        """Fetch an external span by ID.

        Blocking call using GET request.

        Args:
            span_id: The external span ID
            replay_view: Limit rawData to input/output serialization fields.

        Returns:
            The external span data including rawData. ``replay_view=True``
            limits rawData to the input/output serialization fields replay uses.
        """
        query = "?view=replay" if replay_view else ""
        return self.get(
            f"/api/sdk/externalSpans/{span_id}{query}",
            timeout=30,
        )

    def get_span_tree(
        self,
        external_span_id: str,
        include_outputs: bool = True,
        include_root_output: bool = True,
    ) -> dict[str, Any]:
        """Fetch the span tree rooted at an external span.

        Blocking GET request. Used by replay when a mock strategy is active
        so child spans can be matched against their historical outputs.

        Args:
            external_span_id: The external span ID at the root of the tree
            include_outputs: When False, request a payload-free tree
                (``?includeOutputs=false``): structure plus each node's
                ``externalSpanId`` but no recorded ``output``/``outputMeta``, so
                replay pulls only the outputs it actually mocks, lazily, rather
                than dragging down every span's recorded output. Defaults to
                True (outputs inline).
            include_root_output: When False, omit the root's output. Replay
                already fetches the root input/output separately and never
                mocks the root span.

        Returns:
            A dict shaped ``{"root": SpanTreeNode}`` where each node has
            ``sourceSpanId``, ``externalSpanId``, ``traceFunctionKey``,
            ``spanName``, ``type``, ``children``, and (when
            ``include_outputs``) ``output`` plus optional ``outputMeta``.
        """
        query_params: list[str] = []
        if not include_outputs:
            query_params.append("includeOutputs=false")
        if not include_root_output:
            query_params.append("includeRootOutput=false")
        query = f"?{'&'.join(query_params)}" if query_params else ""
        return self.get(
            f"/api/sdk/replay/spanTree/{external_span_id}{query}",
            timeout=30,
        )

    def complete_replay(self, experiment_id: str) -> dict[str, Any]:
        """Mark a replay experiment as completed.

        Blocking call.

        Args:
            experiment_id: The experiment ID to complete

        Returns:
            The parsed JSON response
        """
        return self.request(
            "/api/sdk/replay/complete",
            {"experimentId": experiment_id, "testRunId": experiment_id},
            timeout=_REPLAY_COMPLETE_REQUEST_TIMEOUT_SECONDS,
        )

    def interrupt_replay(self, experiment_id: str) -> bool:
        try:
            self.request(
                "/api/sdk/replay/interrupt",
                {"experimentId": experiment_id, "testRunId": experiment_id},
                timeout=_REPLAY_INTERRUPT_REQUEST_TIMEOUT_SECONDS,
                log_errors=False,
            )
        except Exception:
            logger.debug(
                "Bitfab: could not mark replay experiment %s interrupted",
                experiment_id,
                exc_info=True,
            )
            return False
        return True

    def heartbeat_replay(self, experiment_id: str) -> None:
        try:
            self.request(
                "/api/sdk/replay/heartbeat",
                {"experimentId": experiment_id, "testRunId": experiment_id},
                timeout=_REPLAY_HEARTBEAT_REQUEST_TIMEOUT_SECONDS,
                log_errors=False,
            )
        except Exception:
            logger.debug(
                "Bitfab: could not send a heartbeat for replay experiment %s",
                experiment_id,
                exc_info=True,
            )

    def get_reseed_source(self, trace_id: str) -> dict[str, Any]:
        return self.get(f"/api/sdk/traces/{trace_id}/reseedSource", timeout=30)

    def reseed_trace(self, trace_id: str, run_trace_id: str) -> dict[str, Any]:
        return self.request(
            f"/api/sdk/traces/{trace_id}/reseed",
            {"runTraceId": run_trace_id},
            timeout=30,
        )

    def get_replay_status(
        self,
        experiment_id: str,
        expected_span_counts: dict[str, int],
    ) -> dict[str, Any]:
        """Read replay traces that the server has fully persisted."""
        return self.request(
            "/api/sdk/replay/status",
            {
                "experimentId": experiment_id,
                "testRunId": experiment_id,
                "expectedSpanCounts": expected_span_counts,
            },
            timeout=30,
        )

    def release_db_branch_lease(self, neon_branch_id: str) -> None:
        """Release a previously-resolved DB branch by deleting its Neon branch.

        Blocking call. Idempotent server-side (a missing branch is treated as
        already released).

        Args:
            neon_branch_id: The Neon branch id from the item's ``dbBranchLease``.
        """
        self.request(
            "/api/sdk/replay/releaseDbBranchLease",
            {"neonBranchId": neon_branch_id},
            timeout=30,
        )

    def resolve_db_branch_lease(
        self,
        experiment_id: str,
        trace_id: str,
        db_branch_settings: dict[str, Any] | None = None,
        attempt: int = 0,
    ) -> dict[str, Any]:
        """Resolve one replay source into a temporary database branch."""
        payload: dict[str, Any] = {
            "experimentId": experiment_id,
            "testRunId": experiment_id,
            "traceId": trace_id,
        }
        if db_branch_settings is not None:
            payload["dbBranchSettings"] = db_branch_settings
        if attempt > 0:
            payload["attempt"] = attempt
        return self.request(
            "/api/sdk/replay/resolveDbBranchLease",
            payload,
            timeout=_REPLAY_DB_BRANCH_REQUEST_TIMEOUT_SECONDS,
        )

    def send_external_trace(self, payload: dict[str, Any]) -> None:
        """Send an external trace (from OpenAI tracing).

        Fire-and-forget through the trace transport.

        Args:
            payload: The trace payload

        """
        payload = merge_caller_metadata_into_trace_payload(payload)
        ref = _carrier_ref(payload)
        if payload.get("completed") is True and ref is not None:
            self.trace_completion.close(
                ref.trace_id,
                lambda count: self._send_counted_external_trace(
                    {**payload, "expectedSpanCount": count}
                ),
                dropped=payload.get("dropped") is True,
            )
            return
        if ref is not None:
            self.trace_completion.open(ref.trace_id)
        self._send_counted_external_trace(payload)

    def _send_counted_external_trace(self, payload: dict[str, Any]) -> None:
        try:
            sender = self.external_trace_sender
            if sender is not None:
                sender(payload, self.submit_external_trace)
                return
            self.submit_external_trace(payload)
        except Exception:
            logger.warning(
                "Bitfab: trace completion could not be queued", exc_info=True
            )

    def submit_external_trace(self, payload: dict[str, Any]) -> None:
        safe_payload, body, dropped = _encode_payload(
            {
                **payload,
                "sdkVersion": __version__,
            },
            MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES,
        )
        _warn_for_dropped_values(dropped)
        self._get_trace_transport().submit(
            "external_trace",
            safe_payload,
            body,
            self._recorded_meta(
                "external_trace",
                payload,
                _carrier_ref(payload) if payload.get("completed") is True else None,
            ),
        )

    def patch_trace(
        self,
        trace_id: str,
        payload: dict[str, Any],
    ) -> None:
        """Partial update of an existing trace identified by its Bitfab ID.

        Used by the detached ``client.get_trace(id)`` handle. Blocking, like
        the other trace-API calls: it returns once the server has applied the
        change and raises if the server rejected it.

        Args:
            trace_id: The canonical Bitfab trace ID (will be URL-encoded)
            payload: ``{appendContexts?: list[dict], mergeMetadata?: dict, setSessionId?: str}``

        Raises:
            ValueError: If the server reports the trace could not be updated
            requests.exceptions.RequestException: If the request fails
        """
        from urllib.parse import quote

        encoded_id = quote(trace_id, safe="")
        self.request(
            f"/api/sdk/traces/{encoded_id}",
            payload,
            timeout=10,
            method="PATCH",
        )

    def get_trace_span(
        self,
        trace_id: str,
        *,
        id: str | None = None,
        name: str | None = None,
        occurrence: Union[str, int] = "last",
    ) -> dict[str, Any] | None:
        """Fetch one persisted span without loading the full trace."""
        from urllib.parse import quote, urlencode

        query: dict[str, str] = {}
        if id is not None:
            query["id"] = id
        elif name is not None:
            query["name"] = name
            query["occurrence"] = str(occurrence)

        encoded_id = quote(trace_id, safe="")
        result = self.get(
            f"/api/sdk/traces/{encoded_id}/span?{urlencode(query)}",
            timeout=30,
        )
        span = result.get("span")
        return span if isinstance(span, dict) else None

    def get_span(self, span_id: str) -> dict[str, Any] | None:
        from urllib.parse import quote

        encoded_id = quote(span_id, safe="")
        result = self.get(f"/api/sdk/spans/{encoded_id}", timeout=30)
        span = result.get("span")
        return span if isinstance(span, dict) else None
