import sys
import time
import threading
import os
import base64
import math
from contextlib import contextmanager
from typing import Callable, Union, List, Dict, Optional, Literal, Any
import requests
from datetime import datetime, timezone
import logging
import json
import uuid
import atexit
from pydantic import ValidationError
from threading import Timer
from raindrop.version import VERSION
from raindrop.models import (
    TrackAIEvent,
    Attachment,
    SignalEvent,
    DefaultSignal,
    FeedbackSignal,
    EditSignal,
    PartialTrackAIEvent,
    PartialAIData,
)
from raindrop.interaction import Interaction
from raindrop.local_debugger import (
    UNSET,
    resolve_local_workshop_url,
)
from raindrop.redact import perform_pii_redaction
import weakref
import urllib.parse

from traceloop.sdk import Traceloop
from traceloop.sdk.instruments import Instruments
from traceloop.sdk.tracing.tracing import (
    TracerWrapper,
    get_chained_entity_path,
    set_entity_path,
)
from opentelemetry.trace import get_current_span
from opentelemetry import trace
from opentelemetry import context as context_api
from opentelemetry.semconv_ai import SpanAttributes
from opentelemetry.trace.status import Status, StatusCode
from traceloop.sdk.utils.json_encoder import JSONEncoder
from traceloop.sdk.tracing.context_manager import get_tracer
from traceloop.sdk.decorators import (
    task as tlp_task,
    workflow as tlp_workflow,
    TraceloopSpanKindValues,
    F,
)
import re

__all__ = [
    # Configuration functions
    "set_debug_logs",
    "set_redact_pii",
    "init",
    "identify",
    "track_ai",
    "track_signal",
    "begin",
    "resume_interaction",
    "interaction",
    "task",
    "tool",
    "task_span",
    "tool_span",
    "start_span",
    "ManualSpan",
    "set_span_properties",
    "set_llm_span_io",
    "flush",
    "shutdown",
    # Re-exported from traceloop for auto-instrumentation control
    "Instruments",
]


# Library logging: never call ``logging.basicConfig`` here — that mutates the
# HOST application's root logger configuration (handlers, level, format) as an
# import side effect. Attach a ``NullHandler`` per stdlib guidance for
# libraries; warnings/errors still surface through the host's config (or
# logging's lastResort handler) and ``set_debug_logs(True)`` raises verbosity.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class _InstrumentationNoiseFilter(logging.Filter):
    """Suppress noisy warnings from third-party auto-instrumentation.

    Traceloop initializes instrumentors for every supported LLM provider
    regardless of whether the user actually uses that provider. When the
    provider package is missing or at an incompatible version, Traceloop
    logs an ERROR like ``Error initializing MistralAI instrumentor: ...``.

    Similarly, when an LLM provider SDK uses non-standard sentinel types
    (e.g. Anthropic's ``Omit``) for optional parameters, the OTel SDK
    emits a WARNING like ``Invalid type Omit for attribute ...``.

    Both are harmless noise for users who don't use those providers. This
    filter suppresses them unless debug logging is explicitly enabled.
    """

    _INSTRUMENTOR_ERROR_RE = re.compile(r"Error initializing .+? instrumentor")
    _INVALID_ATTR_TYPE_RE = re.compile(r"Invalid type \w+ for attribute")

    def filter(self, record: logging.LogRecord) -> bool:
        if debug_logs:
            return True
        msg = record.getMessage()
        if self._INSTRUMENTOR_ERROR_RE.search(msg):
            return False
        if self._INVALID_ATTR_TYPE_RE.search(msg):
            return False
        return True


_noise_filter = _InstrumentationNoiseFilter()
_filters_installed = False


def _install_instrumentation_filters() -> None:
    """Install log filters that suppress auto-instrumentation noise.

    Adds the filter to:
    - The root logger (catches direct ``logging.error()`` calls, e.g. Traceloop)
    - Each handler on the root logger (catches messages propagated from child loggers)
    - The ``opentelemetry.attributes`` logger (catches OTel attribute warnings)

    Safe to call multiple times; filters are only installed once.
    """
    global _filters_installed
    if _filters_installed:
        return
    _filters_installed = True

    root = logging.getLogger()
    root.addFilter(_noise_filter)
    for handler in root.handlers:
        handler.addFilter(_noise_filter)

    otel_attrs_logger = logging.getLogger("opentelemetry.attributes")
    otel_attrs_logger.addFilter(_noise_filter)


def _remove_instrumentation_filters() -> None:
    """Remove previously installed noise filters (used when debug_logs changes)."""
    global _filters_installed
    if not _filters_installed:
        return
    _filters_installed = False

    root = logging.getLogger()
    root.removeFilter(_noise_filter)
    for handler in root.handlers:
        handler.removeFilter(_noise_filter)

    otel_attrs_logger = logging.getLogger("opentelemetry.attributes")
    otel_attrs_logger.removeFilter(_noise_filter)

write_key = None
_wizard_session = None
api_url = "https://api.raindrop.ai/v1/"
local_workshop_url: str | None = None
max_queue_size = 10_000
upload_size = 10
upload_interval = 1.0
buffer = []
flush_lock = threading.Lock()
debug_logs = False
redact_pii = False
_tracing_enabled = False
_bypass_otel_for_tools = False
flush_thread = None
shutdown_event = threading.Event()
max_ingest_size_bytes = 1 * 1024 * 1024  # 1 MB
_direct_tool_upload_size = 50
_direct_tool_spans_buffer: list[dict[str, Any]] = []

_partial_buffers: dict[str, PartialTrackAIEvent] = {}
_partial_timers: dict[str, Timer] = {}
# Holds un-serialized PartialTrackAIEvent objects; serialization / redaction /
# size checks run on the flush thread (see _serialize_partial_event) so that
# interaction.finish() stays O(1) for the caller.
_partial_flush_queue: list[PartialTrackAIEvent] = []
_PARTIAL_TIMEOUT = 2  # 2 seconds

# --- Outbound HTTP bounds ---------------------------------------------------
# Telemetry must never wedge the host app: every cloud POST gets a finite
# timeout, retries are capped with a short backoff, and shutdown runs under an
# overall deadline so the atexit hook can never hang process exit on a dead or
# slow network.
_HTTP_CONNECT_TIMEOUT_SECONDS = 5.0
_HTTP_READ_TIMEOUT_SECONDS = 15.0
_HTTP_MAX_ATTEMPTS = 3
_HTTP_RETRY_BACKOFF_SECONDS = (0.5, 1.0)  # sleep before attempt 2 / attempt 3
_SHUTDOWN_DEADLINE_SECONDS = 10.0
# After shutdown() completes (deadline cleared, shutdown_event still set),
# stragglers send synchronously on the CALLER's thread — keep those to a
# single short-bounded attempt so a late track_ai()/finish() can never block
# a caller for the full retry schedule.
_POST_SHUTDOWN_TIMEOUT = (2.0, 5.0)
_shutdown_deadline: float | None = None  # time.monotonic() based; set by shutdown()

# --- Payload bounds ----------------------------------------------------------
# Maximum characters for a single serialized text field (ai input/output, tool
# span input/output, LLM span content). Enforced BEFORE/DURING serialization so
# the cost of an oversized payload is proportional to the cap, not the payload:
# raw strings are length-checked in O(1) and structured payloads are encoded
# incrementally with an output budget (see _dumps_bounded). Override via
# init(max_text_field_chars=...). OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT still
# applies when it is stricter.
#
# Default is 1M chars: a single ASCII field at the cap still fits under the
# 1MiB event-level ingest gate (max_ingest_size_bytes), and production data
# shows real-world fields in the 100k-1MB range that must keep round-
# tripping unchanged. The cap exists to bound CPU on pathological multi-MB
# payloads, not to shave real ones.
max_text_field_chars = 1_000_000
_TRUNCATION_MARKER = "...[truncated by raindrop]"

# --- Log rate limiting -------------------------------------------------------
# Failure-path logs (buffer overflow, send errors) fire per event / per batch;
# under sustained backpressure that floods the host's stdout. Cap each distinct
# failure family to one log line per interval.
_RATE_LIMITED_LOG_INTERVAL_SECONDS = 30.0
_rate_limited_log_last: dict[str, float] = {}
_rate_limited_log_lock = threading.Lock()


def _rate_limited_log(key: str, level: int, msg: str, *args) -> None:
    now = time.monotonic()
    with _rate_limited_log_lock:
        last = _rate_limited_log_last.get(key)
        if last is not None and (now - last) < _RATE_LIMITED_LOG_INTERVAL_SECONDS:
            return
        _rate_limited_log_last[key] = now
    logger.log(level, msg, *args)


def _shutdown_budget() -> float | None:
    """Seconds left in the shutdown flush window, or None outside shutdown."""
    if _shutdown_deadline is None:
        return None
    return _shutdown_deadline - time.monotonic()


def _redact_url_for_log(url: str) -> str:
    """Strip userinfo (and query) from a URL before logging.

    ``init(endpoint=...)`` is caller-configurable, so integrators may supply
    URLs containing credentials (``https://user:pass@host/...``); those must
    never reach application logs or downstream log aggregation.
    """
    try:
        parsed = urllib.parse.urlsplit(url)
        netloc = parsed.netloc
        if "@" in netloc:
            netloc = netloc.rsplit("@", 1)[1]
        return urllib.parse.urlunsplit((parsed.scheme, netloc, parsed.path, "", ""))
    except Exception:
        return "<unparseable-url>"


def set_debug_logs(value: bool):
    global debug_logs
    debug_logs = value
    if debug_logs:
        logger.setLevel(logging.DEBUG)
        _remove_instrumentation_filters()
    else:
        logger.setLevel(logging.INFO)
        if _tracing_enabled:
            _install_instrumentation_filters()


def set_redact_pii(value: bool):
    global redact_pii
    redact_pii = value
    if redact_pii:
        logger.info("PII redaction enabled")
    else:
        logger.info("PII redaction disabled")


def start_flush_thread():
    logger.debug("Opening flush thread")
    global flush_thread
    if flush_thread is None:
        flush_thread = threading.Thread(target=flush_loop)
        flush_thread.daemon = True
        flush_thread.start()


def flush_loop():
    while not shutdown_event.is_set():
        try:
            flush()
        except Exception as e:
            logger.error(f"Error in flush loop: {e}")
        time.sleep(upload_interval)


def flush() -> None:
    global buffer
    global _direct_tool_spans_buffer
    global _partial_flush_queue

    if buffer is None:
        logger.error("No buffer available")
        _flush_traces()
        return

    logger.debug("Starting flush")

    with flush_lock:
        current_buffer = buffer
        buffer = []
        current_direct_tool_spans = _direct_tool_spans_buffer
        _direct_tool_spans_buffer = []
        current_partials = _partial_flush_queue
        _partial_flush_queue = []

    logger.debug(f"Flushing buffer size: {len(current_buffer)}")

    grouped_events = {}
    for event in current_buffer:
        endpoint = event["type"]
        data = event["data"]
        if endpoint not in grouped_events:
            grouped_events[endpoint] = []
        grouped_events[endpoint].append(data)

    for endpoint, events_data in grouped_events.items():
        for i in range(0, len(events_data), upload_size):
            batch = events_data[i : i + upload_size]
            logger.debug(f"Sending {len(batch)} events to {endpoint}")
            send_request(endpoint, batch)

    for partial_event in current_partials:
        # Serialization / PII redaction / size checks deliberately run here,
        # on the flush thread, so interaction.finish() stays O(1) for callers.
        # Guarded per event: one unserializable payload must not discard the
        # rest of the drained batch.
        try:
            partial_data = _serialize_partial_event(partial_event)
        except Exception as e:
            _rate_limited_log(
                "partial_serialize_failed",
                logging.ERROR,
                "Failed to serialize partial event %s: %s",
                getattr(partial_event, "event_id", "<unknown>"),
                e,
            )
            continue
        if partial_data is not None:
            send_request("events/track_partial", partial_data)

    _flush_direct_tool_spans(current_direct_tool_spans)

    logger.debug("Flush complete")
    _flush_traces()


def _flush_traces() -> None:
    if not _tracing_enabled:
        return

    try:
        if TracerWrapper.verify_initialized():
            TracerWrapper().flush()
    except Exception as e:
        logger.debug(f"Could not flush TracerWrapper during flush: {e}")


def _otlp_attr_string(key: str, value: Any) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    return {"key": key, "value": {"stringValue": str(value)}}


def _otlp_attr_bool(key: str, value: bool | None) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    return {"key": key, "value": {"boolValue": bool(value)}}


def _otlp_attr_int(key: str, value: int | None) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    return {"key": key, "value": {"intValue": str(int(value))}}


def _otlp_attr_double(
    key: str, value: float | None
) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return {"key": key, "value": {"doubleValue": number}}


def _random_id_b64(num_bytes: int) -> str:
    return base64.b64encode(os.urandom(num_bytes)).decode("ascii")


def _int_id_to_b64(value: int | None, width_bytes: int) -> Optional[str]:
    if value is None or value == 0:
        return None
    try:
        return base64.b64encode(int(value).to_bytes(width_bytes, "big")).decode("ascii")
    except (OverflowError, ValueError):
        return None


def _get_active_trace_context_b64() -> tuple[Optional[str], Optional[str]]:
    """
    Read active OTEL context IDs without depending on exporter configuration.
    """
    try:
        span_context = get_current_span().get_span_context()
    except Exception:
        return None, None

    if span_context is None:
        return None, None

    trace_id = getattr(span_context, "trace_id", 0) or 0
    parent_span_id = getattr(span_context, "span_id", 0) or 0
    if trace_id == 0:
        return None, None

    return _int_id_to_b64(trace_id, 16), _int_id_to_b64(parent_span_id, 8)


def _build_direct_tool_span(
    *,
    span_name: str,
    tool_name: str,
    version: int | None,
    start_ns: int,
    end_ns: int,
    duration_ms: float | int | None,
    input_value: str | None,
    output_value: str | None,
    error_message: str | None,
    association_properties: Dict[str, Any],
) -> Dict[str, Any]:
    trace_id_b64, parent_span_id_b64 = _get_active_trace_context_b64()
    if trace_id_b64 is None:
        trace_id_b64 = _random_id_b64(16)

    duration_attr: Optional[Dict[str, Any]] = None
    if duration_ms is not None:
        try:
            duration_number = float(duration_ms)
        except (TypeError, ValueError):
            duration_number = None
        if duration_number is not None and math.isfinite(duration_number):
            duration_attr = _otlp_attr_int(
                "traceloop.entity.duration_ms", math.trunc(duration_number)
            )

    attributes: list[Dict[str, Any]] = []
    for candidate in (
        _otlp_attr_string("traceloop.span.kind", "tool"),
        _otlp_attr_string(SpanAttributes.TRACELOOP_ENTITY_NAME, tool_name),
        _otlp_attr_int(SpanAttributes.TRACELOOP_ENTITY_VERSION, version),
        _otlp_attr_string(SpanAttributes.TRACELOOP_ENTITY_INPUT, input_value),
        _otlp_attr_string(SpanAttributes.TRACELOOP_ENTITY_OUTPUT, output_value),
        duration_attr,
    ):
        if candidate is not None:
            attributes.append(candidate)

    for key, value in association_properties.items():
        attr = None
        if isinstance(value, bool):
            attr = _otlp_attr_bool(f"traceloop.association.properties.{key}", value)
        elif isinstance(value, int):
            attr = _otlp_attr_int(f"traceloop.association.properties.{key}", value)
        elif isinstance(value, float):
            attr = _otlp_attr_double(f"traceloop.association.properties.{key}", value)
        else:
            attr = _otlp_attr_string(f"traceloop.association.properties.{key}", value)
        if attr is not None:
            attributes.append(attr)

    span: Dict[str, Any] = {
        "traceId": trace_id_b64,
        "spanId": _random_id_b64(8),
        "name": span_name,
        "startTimeUnixNano": str(start_ns),
        "endTimeUnixNano": str(end_ns),
        "status": (
            {"code": 2, "message": error_message}
            if error_message is not None
            else {"code": 1}  # STATUS_CODE_OK
        ),
    }
    if parent_span_id_b64 is not None:
        span["parentSpanId"] = parent_span_id_b64
    if attributes:
        span["attributes"] = attributes
    return span


def _build_direct_traces_payload(spans: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "raindrop-ai"}}
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "raindrop-ai", "version": VERSION},
                        "spans": spans,
                    }
                ],
            }
        ]
    }


_LOCAL_MIRROR_TIMEOUT_SECONDS = 2.0


def _post_local_mirror(path: str, payload: Any) -> None:
    if not local_workshop_url:
        return

    # The mirror obeys the shutdown deadline too: with Workshop mirroring
    # enabled, sequential 2s mirror POSTs during the final flush could
    # otherwise push process exit well past the shutdown bound.
    timeout = _LOCAL_MIRROR_TIMEOUT_SECONDS
    budget = _shutdown_budget()
    if budget is not None:
        if budget <= 0:
            logger.debug("Local Workshop mirror skipped: shutdown deadline exceeded")
            return
        timeout = min(timeout, budget)

    url = f"{local_workshop_url}{path}"
    # Deliberately omit Authorization: the local Workshop daemon doesn't
    # validate cloud credentials, and the mirror URL can come from env vars
    # or user input — never let a misconfigured RAINDROP_LOCAL_DEBUGGER /
    # RAINDROP_WORKSHOP host receive the cloud write key.
    headers = {"Content-Type": "application/json"}
    try:
        requests.post(url, json=payload, headers=headers, timeout=timeout)
    except Exception as exc:
        logger.debug(
            "Local Workshop mirror to %s failed: %s",
            _redact_url_for_log(url),
            type(exc).__name__,
        )


def _post_with_retries(url: str, payload: Any, log_key: str) -> None:
    """POST to the cloud API with bounded timeouts and capped retries.

    Outside shutdown: up to ``_HTTP_MAX_ATTEMPTS`` attempts with a short,
    capped backoff between them, each bounded by (connect, read) timeouts.

    During shutdown — checked fresh on EVERY attempt, so a shutdown that
    begins while a flush-thread POST is mid-retry takes effect immediately —
    no further retries or backoff sleeps happen and the (connect, read)
    timeouts are clamped so their SUM fits the remaining window (``requests``
    applies the two limits independently and sequentially). Once the window
    is exhausted, payloads are dropped with a rate-limited warning rather
    than wedging process exit.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {write_key}",
    }
    # Never log the raw URL: a caller-configured endpoint may embed userinfo
    # credentials (https://user:pass@host/...).
    safe_url = _redact_url_for_log(url)

    for attempt in range(_HTTP_MAX_ATTEMPTS):
        budget = _shutdown_budget()
        if budget is not None and budget <= 0:
            _rate_limited_log(
                f"{log_key}.shutdown_deadline",
                logging.WARNING,
                "[raindrop] shutdown flush deadline exceeded; dropping payload for %s",
                safe_url,
            )
            return

        timeout = (_HTTP_CONNECT_TIMEOUT_SECONDS, _HTTP_READ_TIMEOUT_SECONDS)
        if budget is not None:
            # Split the remaining window between connect and read so their
            # SUM stays within the budget (requests applies them in
            # sequence); give connect at most half so a slow handshake can't
            # starve the read phase.
            connect_timeout = min(_HTTP_CONNECT_TIMEOUT_SECONDS, max(0.05, budget / 2))
            read_timeout = min(
                _HTTP_READ_TIMEOUT_SECONDS,
                max(0.05, budget - connect_timeout),
            )
            timeout = (connect_timeout, read_timeout)
        elif shutdown_event.is_set():
            # shutdown() has completed and cleared the deadline; stragglers
            # send synchronously on the caller's thread. Keep them short.
            timeout = _POST_SHUTDOWN_TIMEOUT

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)
            response.raise_for_status()
            logger.debug("Request successful: %s", response.status_code)
            return
        except requests.exceptions.RequestException as e:
            # requests embeds the full request URL in exception messages;
            # scrub it the same way.
            error_text = str(e).replace(url, safe_url)
            _rate_limited_log(
                log_key,
                logging.ERROR,
                "Error sending request to %s (attempt %s/%s): %s: %s",
                safe_url,
                attempt + 1,
                _HTTP_MAX_ATTEMPTS,
                type(e).__name__,
                error_text,
            )
            # In (or after) shutdown, the remaining time is better spent on
            # other queued payloads than on retrying this one.
            if _shutdown_budget() is not None or shutdown_event.is_set():
                break
            if attempt < _HTTP_MAX_ATTEMPTS - 1:
                backoff_idx = min(attempt, len(_HTTP_RETRY_BACKOFF_SECONDS) - 1)
                time.sleep(_HTTP_RETRY_BACKOFF_SECONDS[backoff_idx])

    _rate_limited_log(
        f"{log_key}.gave_up",
        logging.ERROR,
        "Failed to send request to %s",
        safe_url,
    )


def _send_traces_request(payload: Dict[str, Any]) -> None:
    _post_local_mirror("traces", payload)

    if not write_key:
        return

    url = urllib.parse.urljoin(
        api_url if api_url.endswith("/") else f"{api_url}/", "traces"
    )
    _post_with_retries(url, payload, log_key="send.traces")


def _flush_direct_tool_spans(spans: List[Dict[str, Any]]) -> None:
    if not spans:
        return

    for i in range(0, len(spans), _direct_tool_upload_size):
        batch = spans[i : i + _direct_tool_upload_size]
        _send_traces_request(_build_direct_traces_payload(batch))


def _enqueue_direct_tool_span(span: Dict[str, Any]) -> None:
    global _direct_tool_spans_buffer

    if len(_direct_tool_spans_buffer) >= max_queue_size:
        _rate_limited_log(
            "direct_tool_span_buffer_full",
            logging.ERROR,
            "Direct tool span buffer is full. Discarding span.",
        )
        return

    if shutdown_event.is_set():
        _flush_direct_tool_spans([span])
        return

    with flush_lock:
        _direct_tool_spans_buffer.append(span)
        start_flush_thread()


def send_request(
    endpoint: str, data_entries: Union[List[Dict[str, Union[str, Dict]]], Dict[str, Any]]
) -> None:
    _post_local_mirror(endpoint, data_entries)

    if not write_key:
        return

    url = f"{api_url}{endpoint}"
    _post_with_retries(url, data_entries, log_key=f"send.{endpoint}")


def save_to_buffer(event: Dict[str, Union[str, Dict]]) -> None:
    global buffer

    if len(buffer) >= max_queue_size * 0.8:
        _rate_limited_log(
            "buffer_capacity",
            logging.WARNING,
            f"Buffer is at {len(buffer) / max_queue_size * 100:.2f}% capacity",
        )

    if len(buffer) >= max_queue_size:
        _rate_limited_log(
            "buffer_full", logging.ERROR, "Buffer is full. Discarding event."
        )
        return

    logger.debug(f"Adding event to buffer: {event}")

    if shutdown_event.is_set():
        send_request(event["type"], [event["data"]])
        return

    with flush_lock:
        buffer.append(event)
        start_flush_thread()


def identify(user_id: str, traits: Dict[str, Union[str, int, bool, float]]) -> None:
    if not _check_write_key():
        return
    data = {"user_id": user_id, "traits": traits}
    save_to_buffer({"type": "users/identify", "data": data})


def track_ai(
    user_id: str,
    event: str,
    event_id: Optional[str] = None,
    model: Optional[str] = None,
    input: Optional[str] = None,
    output: Optional[str] = None,
    convo_id: Optional[str] = None,
    properties: Optional[Dict[str, Union[str, int, bool, float]]] = None,
    timestamp: Optional[str] = None,
    attachments: Optional[List[Attachment]] = None,
) -> str:
    if not _check_write_key():
        return

    event_id = event_id or str(uuid.uuid4())

    try:
        payload = TrackAIEvent(
            event_id=event_id,
            user_id=user_id,
            event=event,
            timestamp=timestamp or _get_timestamp(),
            properties=properties or {},
            ai_data=dict(  # Pydantic will coerce to AIData
                model=model,
                input=_cap_text(input) if input is not None else None,
                output=_cap_text(output) if output is not None else None,
                convo_id=convo_id,
            ),
            attachments=attachments,
        )
    except ValidationError as err:
        logger.error(f"[raindrop] Invalid data passed to track_ai: {err}")
        return None

    if payload.properties is None:
        payload.properties = {}
    payload.properties["$context"] = _get_context()
    if _wizard_session is not None:
        payload.properties["raindrop.wizardSession"] = _wizard_session

    data = payload.model_dump(mode="json")

    # Apply PII redaction if enabled
    if redact_pii:
        data = perform_pii_redaction(data)

    size = _get_size(data)
    if size > max_ingest_size_bytes:
        logger.warning(
            f"[raindrop] Events larger than {max_ingest_size_bytes / (1024 * 1024)} MB may have properties truncated - "
            f"an event of size {size / (1024 * 1024):.2f} MB was logged"
        )
        return None  # Skip adding oversized events to buffer

    save_to_buffer({"type": "events/track", "data": data})
    return event_id


def shutdown():
    """Flush pending telemetry and stop, under a hard overall deadline.

    Registered via ``atexit``: a dead or slow network must never wedge the
    host process's exit. Every send issued after this point runs with a
    single attempt clamped to the remaining shutdown budget (see
    ``_post_with_retries``); once the budget is exhausted, remaining payloads
    are dropped with a rate-limited warning.
    """
    global _shutdown_deadline
    logger.info("Shutting down raindrop analytics")
    _shutdown_deadline = time.monotonic() + _SHUTDOWN_DEADLINE_SECONDS

    try:
        for eid in list(_partial_timers.keys()):
            _flush_partial_event(eid)

        shutdown_event.set()
        if flush_thread:
            budget = _shutdown_budget()
            flush_thread.join(timeout=max(0.1, budget if budget is not None else 10.0))
        flush()  # Final flush to ensure all events are sent
    finally:
        # Scope the deadline to this call: nothing runs after the atexit hook
        # in production, but tests (and manual callers) may keep using the
        # module after an explicit shutdown().
        _shutdown_deadline = None


def _check_write_key():
    if write_key is None and local_workshop_url is None:
        logger.warning(
            "write_key is not set and no local Workshop daemon is configured. "
            "Set RAINDROP_WRITE_KEY or RAINDROP_LOCAL_DEBUGGER (or pass "
            "`local_workshop_url=...` to init) before using raindrop analytics."
        )
        return False
    return True


def _get_context():
    return {
        "library": {
            "name": "python-sdk",
            "version": VERSION,
        },
        "metadata": {
            "pyVersion": f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        },
    }


def _get_timestamp():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _get_size(event: dict[str, any]) -> int:
    try:
        # Add default=str to handle types like datetime
        data = json.dumps(event, default=str)
        return len(data.encode("utf-8"))
    except (TypeError, OverflowError) as e:
        logger.error(f"Error serializing event for size calculation: {e}")
        return 0


def _truncate_json_if_needed(json_str: str) -> str:
    """
    Truncate JSON string if it exceeds OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT;
    truncation may yield an invalid JSON string, which is expected for logging purposes.
    """
    limit_str = os.getenv("OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT")
    if limit_str:
        try:
            limit = int(limit_str)
            if limit > 0 and len(json_str) > limit:
                return json_str[:limit]
        except ValueError:
            pass
    return json_str


def _effective_field_limit() -> int:
    """Character budget for one serialized payload field.

    The SDK default (``max_text_field_chars``) always applies; the OTel
    span-attribute limit env var additionally applies when it is stricter.
    """
    limit = max_text_field_chars
    limit_str = os.getenv("OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT")
    if limit_str:
        try:
            env_limit = int(limit_str)
            if env_limit > 0:
                limit = min(limit, env_limit)
        except ValueError:
            pass
    return limit


def _truncate_to_limit(text: str, limit: int) -> str:
    """Truncate so the RESULT (marker included) never exceeds ``limit``.

    The limit may come from ``OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT``, which
    downstream consumers treat as a hard cap — appending the marker on top of
    the slice would silently violate it. When the limit is too small to fit
    the marker, hard-slice without it.
    """
    if limit > len(_TRUNCATION_MARKER):
        return text[: limit - len(_TRUNCATION_MARKER)] + _TRUNCATION_MARKER
    return text[:limit]


def _cap_text(value: str, limit: int | None = None) -> str:
    """Cap a raw text field BEFORE any serialization.

    The length check is O(1), so multi-MB inputs/outputs cost nothing on the
    caller's thread beyond the slice that keeps the first ``limit`` chars.
    The result, truncation marker included, never exceeds ``limit``.
    """
    if not isinstance(value, str):
        return value
    if limit is None:
        limit = _effective_field_limit()
    if len(value) <= limit:
        return value
    return _truncate_to_limit(value, limit)


def _bounded_clone(obj: Any, char_budget: int, _depth: int = 0) -> Any:
    """Shallow-prune a payload to roughly ``char_budget`` characters of data.

    ``JSONEncoder.iterencode`` emits each string LEAF as a single chunk, so a
    payload shaped as one multi-MB string would still pay its full encoding
    cost before a chunk-level budget check could fire. This walk caps every
    string leaf and stops descending once the budget is consumed, so the
    clone — and therefore its encoding — is O(budget) regardless of payload
    shape. Each visited node also consumes a little budget, bounding the walk
    itself on huge collections of small values.

    Unknown / custom objects pass through untouched so a custom encoder's
    ``default()`` hook still sees them.
    """
    budget = [char_budget]

    def walk(o: Any, depth: int) -> Any:
        if budget[0] <= 0:
            return _TRUNCATION_MARKER
        if isinstance(o, str):
            if len(o) > budget[0]:
                taken = o[: max(0, budget[0])] + _TRUNCATION_MARKER
                budget[0] = 0
                return taken
            budget[0] -= max(len(o), 1)
            return o
        if o is None or isinstance(o, (bool, int, float)):
            budget[0] -= 8
            return o
        if depth >= 12:
            budget[0] -= 16
            return f"<max depth: {type(o).__name__}>"
        if isinstance(o, dict):
            out: dict = {}
            for k, v in o.items():
                if budget[0] <= 0:
                    out["..."] = _TRUNCATION_MARKER
                    break
                # Walk the key BEFORE the value: assignment evaluates the
                # RHS first, so a budget-draining value would otherwise
                # corrupt its own key.
                key = walk(k, depth + 1) if isinstance(k, str) else k
                out[key] = walk(v, depth + 1)
            return out
        if isinstance(o, (list, tuple)):
            out_list: list = []
            for v in o:
                if budget[0] <= 0:
                    out_list.append(_TRUNCATION_MARKER)
                    break
                out_list.append(walk(v, depth + 1))
            return out_list
        # Custom object: leave for the encoder's default() hook. Charge a
        # token so unbounded sequences of custom objects still terminate.
        budget[0] -= 16
        return o

    return walk(obj, _depth)


def _dumps_bounded(obj: Any, *, limit: int | None = None, cls=None) -> str:
    """JSON-serialize ``obj`` with a hard output budget.

    Unlike serialize-then-truncate, the encoding cost here is proportional to
    the budget, not the payload: the payload is first pruned by
    ``_bounded_clone`` (caps string leaves, stops walking once the budget is
    spent — a single multi-MB string leaf never reaches the encoder), and the
    encode itself still breaks early on accumulated chunk size as a second
    line of defense for content produced by custom ``default()`` hooks. So a
    multi-MB tool payload can never burn seconds of CPU (and the GIL) on the
    calling thread — which may be the host app's asyncio event loop. Matching
    ``_truncate_json_if_needed`` semantics, a truncated result may not be
    valid JSON; that is expected for display purposes.
    """
    if limit is None:
        limit = _effective_field_limit()
    if isinstance(obj, str):
        # Cap first (O(limit) dumps cost), then re-truncate: quoting and
        # escape expansion (\uXXXX) can push the encoded form past the limit.
        text = json.dumps(_cap_text(obj, limit))
        return text if len(text) <= limit else _truncate_to_limit(text, limit)

    # Slack covers JSON syntax overhead (quotes, braces, escapes) so payloads
    # near the limit don't get pruned twice.
    pruned = _bounded_clone(obj, limit + len(_TRUNCATION_MARKER) + 256)

    encoder = (cls or json.JSONEncoder)()
    chunks: list[str] = []
    total = 0
    for chunk in encoder.iterencode(pruned):
        chunks.append(chunk)
        total += len(chunk)
        if total > limit:
            break
    text = "".join(chunks)
    if total > limit:
        return _truncate_to_limit(text, limit)
    return text


def _should_send_prompts():
    return (
        os.getenv("TRACELOOP_TRACE_CONTENT") or "true"
    ).lower() == "true" or context_api.get_value("override_enable_content_tracing")


def set_llm_span_io(
    input: Any = None,
    output: Any = None,
) -> None:
    """
    Set LLM input/output content on the current span.

    Use this to add prompt/completion content to auto-instrumented spans
    that don't capture content automatically (e.g., Bedrock with aioboto3).

    Args:
        input: The input/prompt content (messages, text, etc.)
        output: The output/completion content (response text, message, etc.)

    Example:
        response = await bedrock_client.converse(modelId=model, messages=messages)
        raindrop.set_llm_span_io(
            input=messages,
            output=response["output"]["message"]["content"]
        )
    """
    if not _should_send_prompts():
        return

    span = get_current_span()
    if not span or not span.is_recording():
        logger.debug("[raindrop] set_llm_span_io called but no active span found")
        return

    try:
        if input is not None:
            input_str = (
                _dumps_bounded(input, cls=JSONEncoder)
                if not isinstance(input, str)
                else _cap_text(input)
            )
            span.set_attribute("gen_ai.prompt.0.role", "user")
            span.set_attribute("gen_ai.prompt.0.content", input_str)

        if output is not None:
            output_str = (
                _dumps_bounded(output, cls=JSONEncoder)
                if not isinstance(output, str)
                else _cap_text(output)
            )
            span.set_attribute("gen_ai.completion.0.role", "assistant")
            span.set_attribute("gen_ai.completion.0.content", output_str)
    except Exception as e:
        logger.debug(f"[raindrop] Failed to record LLM content: {e}")


# Signal types - This is now defined in models.py
# SignalType = Literal["default", "feedback", "edit"]


def track_signal(
    event_id: str,
    name: str,
    signal_type: Literal["default", "feedback", "edit"] = "default",
    timestamp: Optional[str] = None,
    properties: Optional[Dict[str, Any]] = None,
    attachment_id: Optional[str] = None,
    comment: Optional[str] = None,
    after: Optional[str] = None,
    sentiment: Optional[Literal["POSITIVE", "NEGATIVE"]] = None,
) -> None:
    """
    Track a signal event.

    Args:
        event_id: The ID of the event to attach the signal to
        name: Name of the signal (e.g. "thumbs_up", "thumbs_down")
        signal_type: Type of signal ("default", "feedback", or "edit")
        timestamp: Optional timestamp for the signal (ISO 8601 format)
        properties: Optional dictionary of additional properties.
        attachment_id: Optional ID of an attachment
        comment: Optional comment string (required and used only if signal_type is 'feedback').
        after: Optional after content string (required and used only if signal_type is 'edit').
        sentiment: Optional sentiment indicating if the signal is POSITIVE (default is NEGATIVE)
    """
    if not _check_write_key():
        return

    # Prepare the final properties dictionary
    final_properties = properties.copy() if properties else {}
    if signal_type == "feedback" and comment is not None:
        if "comment" in final_properties:
            logger.warning(
                "'comment' provided as both argument and in properties; argument value used."
            )
        final_properties["comment"] = comment
    elif signal_type == "edit" and after is not None:
        if "after" in final_properties:
            logger.warning(
                "'after' provided as both argument and in properties; argument value used."
            )
        final_properties["after"] = after

    # Prepare base arguments for all signal types
    base_args = {
        "event_id": event_id,
        "signal_name": name,
        "timestamp": timestamp or _get_timestamp(),
        "properties": final_properties,
        "attachment_id": attachment_id,
        "sentiment": sentiment,
    }

    try:
        # Construct the specific signal model based on signal_type
        if signal_type == "feedback":
            payload = FeedbackSignal(**base_args, signal_type=signal_type)
        elif signal_type == "edit":
            payload = EditSignal(**base_args, signal_type=signal_type)
        else:  # signal_type == "default"
            if comment is not None:
                logger.warning(
                    "'comment' argument provided for non-feedback signal type; ignored."
                )
            if after is not None:
                logger.warning(
                    "'after' argument provided for non-edit signal type; ignored."
                )
            payload = DefaultSignal(**base_args, signal_type=signal_type)

    except ValidationError as err:
        logger.error(f"[raindrop] Invalid data passed to track_signal: {err}")
        return None

    # model_dump handles the timestamp correctly
    data = payload.model_dump(mode="json")

    size = _get_size(data)
    if size > max_ingest_size_bytes:
        logger.warning(
            f"[raindrop] Events larger than {max_ingest_size_bytes / (1024 * 1024)} MB may have properties truncated - "
            f"an event of size {size / (1024 * 1024):.2f} MB was logged"
        )
        return  # Skip adding oversized events to buffer

    save_to_buffer({"type": "signals/track", "data": data})


INTERACTION_TRACE_ID_REGISTRY: weakref.WeakValueDictionary[int, Interaction] = (
    weakref.WeakValueDictionary()
)
INTERACTION_EVENT_ID_REGISTRY: weakref.WeakValueDictionary[str, Interaction] = (
    weakref.WeakValueDictionary()
)


def begin(
    user_id: str,
    event: str,
    event_id: str | None = None,
    properties: Optional[Dict[str, Any]] = None,
    input: Optional[str] = None,
    attachments: Optional[List[Attachment]] = None,
    convo_id: Optional[str] = None,
) -> Interaction:
    """
    Starts (or resumes) an interaction and returns a helper object.
    """
    if not isinstance(user_id, str) or not user_id.strip():
        # The API rejects events without a user_id; return a disabled
        # Interaction whose mutators/finish/span/tool calls all no-op so
        # caller code keeps running. Log the type only (never the value)
        # so non-string user_id objects can't leak PII into log sinks.
        logger.warning(
            "[raindrop] begin(): empty user_id (type=%s); returning disabled interaction.",
            type(user_id).__name__,
        )
        return Interaction(
            event_id=event_id,
            user_id=user_id if isinstance(user_id, str) else None,
            event=event,
            convo_id=convo_id,
            disabled=True,
        )

    eid = event_id or str(uuid.uuid4())

    # Instantiate ai_data if either input or convo_id is supplied so that convo_id isn't lost when input is set later
    ai_data_partial = None
    if input is not None or convo_id is not None:
        capped_input = _cap_text(input) if input is not None else None
        ai_data_partial = PartialAIData(input=capped_input, convo_id=convo_id)

    # Combine properties with initial_fields, giving precedence to initial_fields if keys clash
    final_properties = (properties or {}).copy()

    current_trace_id = _safe_current_trace_id()
    if current_trace_id is not None:
        final_properties["trace_id"] = f"{current_trace_id:032x}"

    partial_event = PartialTrackAIEvent(
        event_id=eid,
        user_id=user_id,
        event=event,
        ai_data=ai_data_partial,
        properties=final_properties
        or None,  # Pass None if empty, matching PartialTrackAIEvent defaults
        attachments=attachments,
    )

    span_attributes = {
        "user_id": user_id,
        "convo_id": convo_id,
        "event": event,
        "event_id": eid,
    }
    if _tracing_enabled:
        Traceloop.set_association_properties(
            {k: v for k, v in span_attributes.items() if v is not None}
        )

    interaction = Interaction(eid, user_id=user_id, event=event, convo_id=convo_id)
    INTERACTION_EVENT_ID_REGISTRY[eid] = interaction
    if current_trace_id is not None and current_trace_id != 0:
        INTERACTION_TRACE_ID_REGISTRY[current_trace_id] = interaction

    _track_ai_partial(partial_event)
    return interaction


@contextmanager
def _temp_env(key: str, value: str):
    """Temporarily sets an environment variable. Hacky helper to deal with traceloop's BS"""
    orig = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if orig is None:
            del os.environ[key]
        else:
            os.environ[key] = orig


def init(
    api_key: str | None = None,
    wizard_session: str | None = None,
    tracing_enabled: bool = False,
    auto_instrument: bool = True,
    bypass_otel_for_tools: bool = False,
    endpoint: str | None = None,
    local_workshop_url: Any = UNSET,
    max_text_field_chars: int | None = None,
    **traceloop_kwargs,
):
    """Initialize Raindrop with Traceloop integration.

    Args:
        api_key: Raindrop API key. When ``None`` or empty, cloud telemetry is
            skipped and the SDK only fans out to ``local_workshop_url`` (if
            resolved). Useful for local-only Workshop debugging.
        tracing_enabled: Enable OpenTelemetry tracing.
        auto_instrument: If True (default), Traceloop will auto-instrument
            detected LLM client libraries (OpenAI, Anthropic, etc). Set to
            False to disable all auto-instrumentation. Manual tracing
            (@task, @tool, begin/finish) works regardless of this setting.
        bypass_otel_for_tools: If True, ``interaction.track_tool()`` emits OTLP
            tool spans directly to ``/v1/traces`` instead of relying on the
            configured OTEL exporter pipeline.
        endpoint: Override the cloud API endpoint (defaults to
            ``https://api.raindrop.ai/v1/``). Rarely needed.
        local_workshop_url: Optional Raindrop Workshop daemon URL to mirror
            partial events and trace exports to in addition to the cloud.
            ``str`` forces the URL; ``None`` opts out (suppresses env +
            auto-detect); omitted falls through to ``RAINDROP_LOCAL_DEBUGGER`` /
            ``RAINDROP_WORKSHOP`` env vars and a TCP probe of localhost:5899.
        max_text_field_chars: Per-field character cap applied to ai
            input/output and serialized tool/LLM span content BEFORE (or
            during) serialization, so oversized payloads cost the cap — not
            the payload — on the calling thread. Defaults to 1,000,000.
        **traceloop_kwargs: Extra kwargs forwarded to Traceloop.init().
            Can include ``instruments`` or ``block_instruments`` for
            fine-grained control over which libraries are instrumented.
    """
    if max_text_field_chars is not None:
        if max_text_field_chars > 0:
            globals()["max_text_field_chars"] = max_text_field_chars
        else:
            logger.warning(
                "[raindrop] init(max_text_field_chars=%r) ignored; must be > 0",
                max_text_field_chars,
            )

    resolved_local = resolve_local_workshop_url(local_workshop_url)

    global write_key
    write_key = api_key or None

    global api_url
    if endpoint is not None:
        api_url = endpoint if endpoint.endswith("/") else f"{endpoint}/"

    globals()["local_workshop_url"] = resolved_local

    global _wizard_session
    _wizard_session = wizard_session

    global _tracing_enabled
    _tracing_enabled = tracing_enabled

    global _bypass_otel_for_tools
    _bypass_otel_for_tools = bool(bypass_otel_for_tools and tracing_enabled)

    if not _tracing_enabled:
        _remove_instrumentation_filters()
        return

    # Traceloop's OTEL exporter sends to the cloud endpoint and authenticates
    # with the cloud API key. With no key we'd either see export-time auth
    # errors or silently dropped spans, so disable tracing entirely until the
    # caller supplies one. Local-only Workshop mode still gets manual events
    # (track_ai, identify, signals) via the analytics fan-out path.
    if not write_key:
        _tracing_enabled = False
        _bypass_otel_for_tools = False
        logger.warning(
            "[raindrop] tracing_enabled=True requires api_key for OTEL export; "
            "disabling auto-instrumentation. Pass api_key=... or unset "
            "tracing_enabled to silence this warning."
        )
        _remove_instrumentation_filters()
        return

    if not debug_logs:
        _install_instrumentation_filters()

    # When auto_instrument is False (default), disable all auto-instrumentation
    # unless the caller explicitly passed `instruments` or `block_instruments`.
    if not auto_instrument and "instruments" not in traceloop_kwargs:
        traceloop_kwargs["instruments"] = set()

    parsed_url = urllib.parse.urlparse(api_url)
    api_endpoint = f"{parsed_url.scheme}://{parsed_url.netloc}"

    with _temp_env("TRACELOOP_METRICS_ENABLED", "false"):
        Traceloop.init(
            api_endpoint=api_endpoint,
            api_key=api_key,
            telemetry_enabled=False,
            **traceloop_kwargs,
        )


def _safe_current_trace_id() -> int | None:
    """Return current trace id or None if unavailable."""
    try:
        trace_id = get_current_span().get_span_context().trace_id
    except Exception:
        return None
    return trace_id if trace_id else None


def interaction(
    name: Optional[str] = None,
    version: Optional[int] = None,
    method_name: Optional[str] = None,
) -> Callable[[F], F]:
    return tlp_workflow(
        name=name,
        version=version,
        method_name=method_name,
        tlp_span_kind=TraceloopSpanKindValues.WORKFLOW,
    )


def task(
    name: Optional[str] = None,
    version: Optional[int] = None,
    method_name: Optional[str] = None,
    tlp_span_kind: Optional[TraceloopSpanKindValues] = TraceloopSpanKindValues.TASK,
) -> Callable[[F], F]:
    return tlp_task(
        name=name,
        version=version,
        method_name=method_name,
        tlp_span_kind=tlp_span_kind,
    )


def tool(
    name: Optional[str] = None,
    version: Optional[int] = None,
    method_name: Optional[str] = None,
) -> Callable[[F], F]:
    return tlp_task(
        name=name,
        version=version,
        method_name=method_name,
        tlp_span_kind=TraceloopSpanKindValues.TOOL,
    )


def set_span_properties(properties: Dict[str, Any]) -> None:
    """
    Set association properties on the current span for tracing.

    Args:
        properties: Dictionary of properties to associate with the current span
    """
    if not _tracing_enabled:
        return

    Traceloop.set_association_properties(properties)


class TraceEntitySpan:
    def __init__(self, span):
        self._span = span

    def record_input(self, data: Any) -> None:
        if self._span and _should_send_prompts():
            try:
                truncated = _dumps_bounded({"args": [data]}, cls=JSONEncoder)
                self._span.set_attribute(
                    SpanAttributes.TRACELOOP_ENTITY_INPUT, truncated
                )
            except TypeError as e:
                logger.debug(f"[raindrop] Could not serialize input for span: {e}")

    def record_output(self, data: Any) -> None:
        if self._span and _should_send_prompts():
            try:
                truncated = _dumps_bounded(data, cls=JSONEncoder)
                self._span.set_attribute(
                    SpanAttributes.TRACELOOP_ENTITY_OUTPUT, truncated
                )
            except TypeError as e:
                logger.debug(f"[raindrop] Could not serialize output for span: {e}")

    def set_properties(self, props: Dict[str, Any]) -> None:
        if _tracing_enabled and props:
            Traceloop.set_association_properties(props)


class ManualSpan:
    """
    A manually-controlled span for async/distributed operations.
    Unlike context-managed spans, this requires explicit .end() calls.
    """

    def __init__(self, span, kind: str, name: str, event_id: str | None = None):
        self._span = span
        self._kind = kind
        self._name = name
        self._event_id = event_id
        self._ended = False

    @property
    def event_id(self) -> str | None:
        return self._event_id

    def record_input(self, data: Any) -> None:
        if self._span and _should_send_prompts():
            try:
                truncated = _dumps_bounded({"args": [data]}, cls=JSONEncoder)
                self._span.set_attribute(
                    SpanAttributes.TRACELOOP_ENTITY_INPUT, truncated
                )
            except TypeError as e:
                logger.debug(f"[raindrop] Could not serialize input for span: {e}")

    def record_output(self, data: Any) -> None:
        if self._span and _should_send_prompts():
            try:
                truncated = _dumps_bounded(data, cls=JSONEncoder)
                self._span.set_attribute(
                    SpanAttributes.TRACELOOP_ENTITY_OUTPUT, truncated
                )
            except TypeError as e:
                logger.debug(f"[raindrop] Could not serialize output for span: {e}")

    def set_properties(self, props: Dict[str, Any]) -> None:
        if self._span and props:
            for key, value in props.items():
                if value is not None:
                    self._span.set_attribute(
                        f"traceloop.association.properties.{key}", value
                    )

    def end(self, error: Exception | None = None) -> None:
        if self._ended or not self._span:
            return
        self._ended = True
        if error is not None:
            self._span.set_status(Status(StatusCode.ERROR, str(error)))
            self._span.record_exception(error)
        self._span.end()


class _EntitySpanContext:
    def __init__(self, kind: Literal["task", "tool"], name: str, version: int | None):
        self._kind = kind
        self._name = name
        self._version = version
        self._span = None
        self._ctx_token = None
        self._span_cm = None
        self._helper = TraceEntitySpan(None)

    # internal start/finish
    def _start(self) -> None:
        if not _tracing_enabled or not TracerWrapper.verify_initialized():
            return
        tlp_kind = (
            TraceloopSpanKindValues.TASK
            if self._kind == "task"
            else TraceloopSpanKindValues.TOOL
        )
        span_name = f"{self._name}.{tlp_kind.value}"
        with get_tracer() as tracer:
            self._span_cm = tracer.start_as_current_span(span_name)
            span = self._span_cm.__enter__()

        if tlp_kind in [TraceloopSpanKindValues.TASK, TraceloopSpanKindValues.TOOL]:
            entity_path = get_chained_entity_path(self._name)
            set_entity_path(entity_path)

        span.set_attribute(SpanAttributes.TRACELOOP_SPAN_KIND, tlp_kind.value)
        span.set_attribute(SpanAttributes.TRACELOOP_ENTITY_NAME, self._name)
        if self._version is not None:
            span.set_attribute(SpanAttributes.TRACELOOP_ENTITY_VERSION, self._version)

        self._span = span
        self._helper = TraceEntitySpan(span)

    def _end(self, exc_type, exc, tb) -> bool:
        if not self._span:
            return False
        try:
            if exc is not None:
                self._span.set_status(Status(StatusCode.ERROR, str(exc)))
                self._span.record_exception(exc)
            return False
        finally:
            if self._span_cm is not None:
                self._span_cm.__exit__(exc_type, exc, tb)

    # sync
    def __enter__(self) -> TraceEntitySpan:
        self._start()
        return self._helper

    def __exit__(self, exc_type, exc, tb) -> bool:
        return self._end(exc_type, exc, tb)

    # async
    async def __aenter__(self) -> TraceEntitySpan:
        self._start()
        return self._helper

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        return self._end(exc_type, exc, tb)


def task_span(name: str, version: int | None = None) -> _EntitySpanContext:
    return _EntitySpanContext("task", name, version)


def tool_span(name: str, version: int | None = None) -> _EntitySpanContext:
    return _EntitySpanContext("tool", name, version)


def start_span(
    kind: Literal["task", "tool"],
    name: str,
    version: int | None = None,
    event_id: str | None = None,
    user_id: str | None = None,
    event: str | None = None,
    convo_id: str | None = None,
) -> ManualSpan:
    """
    Create a manual span that must be explicitly ended with .end().

    Use this for async/distributed operations where the span lifecycle
    extends beyond a single context manager scope.

    Args:
        kind: Type of span - "task" or "tool"
        name: Name of the span
        version: Optional version number
        event_id: Optional event_id for tracing association
        user_id: Optional user_id for tracing association
        event: Optional event name for tracing association
        convo_id: Optional conversation ID for tracing association

    Returns:
        ManualSpan instance (safe to use even if tracing is disabled)
    """
    if not _tracing_enabled or not TracerWrapper.verify_initialized():
        return ManualSpan(None, kind, name, event_id)

    tlp_kind = (
        TraceloopSpanKindValues.TASK if kind == "task" else TraceloopSpanKindValues.TOOL
    )
    span_name = f"{name}.{tlp_kind.value}"

    with get_tracer() as tracer:
        span = tracer.start_span(span_name)

    span.set_attribute(SpanAttributes.TRACELOOP_SPAN_KIND, tlp_kind.value)
    span.set_attribute(SpanAttributes.TRACELOOP_ENTITY_NAME, name)
    if version is not None:
        span.set_attribute(SpanAttributes.TRACELOOP_ENTITY_VERSION, version)

    # Set association properties directly on the span (not on current context)
    association_props = {
        "event_id": event_id,
        "user_id": user_id,
        "event": event,
        "convo_id": convo_id,
    }
    for key, value in association_props.items():
        if value is not None:
            span.set_attribute(f"traceloop.association.properties.{key}", value)

    return ManualSpan(span, kind, name, event_id)


def resume_interaction(event_id: str | None = None) -> Interaction:
    """Return an Interaction associated with the current trace or given event_id."""

    if event_id is not None:
        if (interaction := INTERACTION_EVENT_ID_REGISTRY.get(event_id)) is not None:
            return interaction
        return Interaction(event_id)

    if (trace_id := _safe_current_trace_id()) is not None:
        if (interaction := INTERACTION_TRACE_ID_REGISTRY.get(trace_id)) is not None:
            return interaction

    # Fallback: create a fresh Interaction when no identifiers are available
    # TODO: Return No-Op interaction if event_id is None
    logger.debug("No interaction found, creating a new one")
    return Interaction()


def _track_ai_partial(event: PartialTrackAIEvent) -> None:
    """
    Merge the incoming patch into an in-memory doc and flush to backend:
      • on `.finish()`  (is_pending == False)
      • or after 20 s of inactivity
    """
    eid = event.event_id

    # 1. merge
    existing = _partial_buffers.get(eid, PartialTrackAIEvent(event_id=eid))
    existing.is_pending = (
        existing.is_pending if existing.is_pending is not None else True
    )
    merged_dict = existing.model_dump(exclude_none=True)
    incoming = event.model_dump(exclude_none=True)

    # deep merge ai_data / properties
    def _deep(d: dict, u: dict):
        for k, v in u.items():
            d[k] = (
                _deep(d.get(k, {}) if isinstance(v, dict) else v, v)
                if isinstance(v, dict)
                else v
            )
        return d

    merged = _deep(merged_dict, incoming)
    merged_obj = PartialTrackAIEvent(**merged)

    _partial_buffers[eid] = merged_obj

    # 2. timer handling
    if t := _partial_timers.get(eid):
        t.cancel()
    if merged_obj.is_pending is False:
        _flush_partial_event(eid)
    else:
        _partial_timers[eid] = Timer(_PARTIAL_TIMEOUT, _flush_partial_event, args=[eid])
        _partial_timers[eid].daemon = True
        _partial_timers[eid].start()

    if debug_logs:
        logger.debug(
            f"[raindrop] updated partial {eid}: {merged_obj.model_dump(exclude_none=True)}"
        )


def _should_drop_empty_ai_event(evt: PartialTrackAIEvent) -> bool:
    """Drop finalized ``events/track_partial`` payloads with no AI text body.

    Mirrors the Rust SDK's ``should_drop_empty_ai_event`` gate
    (`raindrop-ai/raindrop-rust#12 <https://github.com/raindrop-ai/raindrop-rust/pull/12>`_).
    A wrapper that calls ``begin()`` with only ``convo_id`` / ``model`` /
    token-usage ``properties`` and then ``finish()`` with no ``output``
    produces a finalized payload whose ``ai_data`` (after
    ``model_dump(exclude_none=True)``) carries neither ``input`` nor
    ``output`` — these show up in the dashboard as phantom ``ai_generation``
    rows with empty input/output columns. Drop them at the buffer level with
    a single ``logger.warning`` rather than shipping.

    Pending intermediates (``is_pending`` not explicitly ``False``) always
    ship — a still-in-flight interaction with no input yet is expected.
    Events with attachments also always ship — an attachment-only upload is
    a real payload regardless of whether ``ai_data`` text fields are
    populated.

    To record an errored generation, populate at least one of ``input`` /
    ``output`` (e.g. ship the prompt as ``input`` and set the error in
    ``properties``) so the event lands in the dashboard.
    """
    if evt.is_pending is not False:
        return False
    if evt.attachments:
        return False
    ai = evt.ai_data
    if ai is None:
        return True
    return not ai.input and not ai.output


def _serialize_partial_event(evt: PartialTrackAIEvent) -> Optional[Dict[str, Any]]:
    """Serialize a buffered partial event for ``events/track_partial``.

    Runs on the background flush thread (or synchronously during shutdown) —
    NOT on the caller's thread. Returns ``None`` when the event should be
    skipped (oversized).
    """
    # convert to ordinary TrackAIEvent-ish dict before send
    data = evt.model_dump(mode="json", exclude_none=True)

    # Inject wizard session if set
    if _wizard_session is not None:
        if "properties" not in data or data["properties"] is None:
            data["properties"] = {}
        data["properties"]["raindrop.wizardSession"] = _wizard_session

    # Apply PII redaction if enabled
    if redact_pii:
        data = perform_pii_redaction(data)

    size = _get_size(data)
    if size > max_ingest_size_bytes:
        logger.warning(f"[raindrop] partial event {evt.event_id} > 1 MB; skipping")
        return None

    return data


def _flush_partial_event(event_id: str) -> None:
    """
    Enqueue the accumulated patch for asynchronous send to `events/track_partial`.

    The caller — often a request hot path or an asyncio event loop — only pops
    the buffer and enqueues the model object; serialization, PII redaction,
    and size checks all run on the background ``flush_loop`` thread (see
    ``_serialize_partial_event``), so ``interaction.finish()`` is O(1) for the
    caller regardless of payload size. During shutdown the event is serialized
    and sent synchronously under the shutdown deadline.
    """
    if t := _partial_timers.pop(event_id, None):
        t.cancel()

    evt = _partial_buffers.pop(event_id, None)
    if not evt:
        return

    if _should_drop_empty_ai_event(evt):
        logger.warning(
            "[raindrop] dropping finalized track_partial with empty ai_input "
            "and ai_output (event_id=%s, event=%r). Populate input/output via "
            "begin()/finish() or ship the prompt as input on errored "
            "generations so the event lands in the dashboard.",
            event_id,
            evt.event,
        )
        return

    if shutdown_event.is_set():
        # Synchronous send on the caller's thread (e.g. a late finish()
        # during atexit ordering). Guarded like the flush-thread path: a
        # serialization failure must never propagate into caller code.
        try:
            data = _serialize_partial_event(evt)
        except Exception as e:
            _rate_limited_log(
                "partial_serialize_failed",
                logging.ERROR,
                "Failed to serialize partial event %s: %s",
                event_id,
                e,
            )
            return
        if data is not None:
            send_request("events/track_partial", data)
        return

    with flush_lock:
        if len(_partial_flush_queue) >= max_queue_size:
            _rate_limited_log(
                "partial_queue_full",
                logging.ERROR,
                "Partial queue is full. Discarding event.",
            )
            return
        _partial_flush_queue.append(evt)
        start_flush_thread()


atexit.register(shutdown)
