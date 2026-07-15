import sys
import time
import threading
import os
import base64
import io
import math
from contextlib import contextmanager, redirect_stdout
from itertools import groupby
from typing import Any, Callable, Dict, Iterator, List, Literal, Optional, Union
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
    TrackEvent,
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
from raindrop.model_usage import normalize_model_usage_span
from raindrop.redact import perform_pii_redaction
from raindrop._state import ClientState, ModuleBackedState, RaindropState
from raindrop import _tracing as _rd_tracing
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
from opentelemetry.sdk.trace import ReadableSpan
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
    "track",
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


def __getattr__(name: str) -> Any:
    # Convenience so ``import raindrop.analytics as raindrop`` users can reach
    # the instance-based client without a second import. Lazy to avoid a
    # circular import (client.py imports this module).
    if name == "Raindrop":
        from raindrop.client import Raindrop

        return Raindrop
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


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
project_id: str | None = None
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

# The globals above are the storage of the DEFAULT client — the one behind
# the module-level API (init / track_ai / begin / ...). Pipeline functions
# never touch them directly anymore; they go through a state object so the
# same code also serves per-instance ``raindrop.Raindrop`` clients (see
# raindrop/_state.py). ``ModuleBackedState`` proxies right back to these
# globals, so legacy reads/writes like ``analytics.max_queue_size = 500``
# keep steering the default pipeline exactly as before.
_default_state = ModuleBackedState()


def _resolve_state(state: Optional[RaindropState]) -> RaindropState:
    return _default_state if state is None else state

_partial_buffers: dict[str, PartialTrackAIEvent] = {}
_partial_timers: dict[str, Timer] = {}
# Holds un-serialized PartialTrackAIEvent objects; serialization / redaction /
# size checks run on the flush thread (see _serialize_partial_event) so that
# interaction.finish() stays O(1) for the caller.
_partial_flush_queue: list[PartialTrackAIEvent] = []
_PARTIAL_TIMEOUT = 2  # 2 seconds

# Optional first-class-projects routing. When ``project_id`` is set, every
# outbound request carries ``X-Raindrop-Project-Id: <slug>`` so the ingest
# boundary routes events to the named project; when unset, no header is sent
# and the server falls back to the org's default project (fully backward
# compatible — existing callers are byte-identical on the wire).
PROJECT_ID_HEADER = "X-Raindrop-Project-Id"
_PROJECT_ID_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def _project_id_headers(state: Optional[RaindropState] = None) -> Dict[str, str]:
    pid = _resolve_state(state).project_id
    if pid:
        return {PROJECT_ID_HEADER: pid}
    return {}


def _resolve_project_id(value: str | None) -> str | None:
    if value is None:
        return None
    trimmed = value.strip()
    if not trimmed:
        return None
    if not _PROJECT_ID_PATTERN.match(trimmed):
        logger.warning(
            "[raindrop] Ignoring invalid project_id %r: must match "
            "%s. No X-Raindrop-Project-Id header will be sent.",
            trimmed,
            _PROJECT_ID_PATTERN.pattern,
        )
        return None
    return trimmed

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

# Pipeline states of live per-instance clients (the default module client is
# NOT here; the shared atexit hook drains it directly). Holds STATES, not
# clients, and holds them STRONGLY: buffered events must survive to the
# atexit drain even when the host app dropped its last reference to the
# client object. A state leaves the registry when its flush loop exits after
# detecting the collected client (post final drain), so dropped clients don't
# leak state forever; a late enqueue re-registers via start_flush_thread.
_instance_states: set = set()


def _rate_limited_log(key: str, level: int, msg: str, *args: Any) -> None:
    now = time.monotonic()
    with _rate_limited_log_lock:
        last = _rate_limited_log_last.get(key)
        if last is not None and (now - last) < _RATE_LIMITED_LOG_INTERVAL_SECONDS:
            return
        _rate_limited_log_last[key] = now
    logger.log(level, msg, *args)


def _shutdown_budget(state: Optional[RaindropState] = None) -> float | None:
    """Seconds left in the shutdown flush window, or None outside shutdown."""
    deadline = _resolve_state(state)._shutdown_deadline
    if deadline is None:
        return None
    return deadline - time.monotonic()


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


def set_debug_logs(value: bool) -> None:
    global debug_logs
    debug_logs = value
    if debug_logs:
        logger.setLevel(logging.DEBUG)
        _remove_instrumentation_filters()
    else:
        logger.setLevel(logging.INFO)
        # The instrumentation-noise filters belong with ANY live tracing
        # pipeline in the process — the module-level client's OR one owned
        # by a Raindrop instance (module _tracing_enabled stays False then).
        if _tracing_enabled or _rd_tracing.pipeline_owner_hint() is not None:
            _install_instrumentation_filters()


def set_redact_pii(value: bool) -> None:
    global redact_pii
    redact_pii = value
    if redact_pii:
        logger.info("PII redaction enabled")
    else:
        logger.info("PII redaction disabled")


def start_flush_thread(state: Optional[RaindropState] = None) -> None:
    logger.debug("Opening flush thread")
    st = _resolve_state(state)
    if st.flush_thread is None:
        # Any instance state with a live flush loop must be visible to the
        # atexit drain — including one re-started by a late enqueue after its
        # collected-client loop exited and unregistered it.
        if isinstance(st, ClientState):
            _instance_states.add(st)
        st.flush_thread = threading.Thread(target=flush_loop, args=(st,))
        st.flush_thread.daemon = True
        st.flush_thread.start()


def flush_loop(state: Optional[RaindropState] = None) -> None:
    st = _resolve_state(state)
    with st.flush_lock:
        defer_initial_flush = any(
            event.get("_defer_initial_flush") for event in st.buffer
        )
    if defer_initial_flush:
        # Plain-track hot-path scenarios need deterministic first delivery:
        # give consecutive enqueues one interval to coalesce before the first
        # drain. This delays the first background flush of the state's entire
        # buffer by upload_interval; later iterations keep the normal cadence.
        time.sleep(st.upload_interval)

    while not st.shutdown_event.is_set():
        try:
            # Loop-driven flushes throttle the TRACE flush: the OTLP pipeline
            # is process-global, so N clients' loops would otherwise all
            # force-flush the same BatchSpanProcessor every second.
            flush(state=st, _throttle_traces=True, _background=True)
        except Exception as e:
            logger.error(f"Error in flush loop: {e}")
        # A per-instance loop whose owning client was garbage-collected has
        # no way to receive shutdown(): exit instead of keeping the dead
        # state alive forever. Clear ``flush_thread`` BEFORE the final drain
        # so a late enqueue (e.g. via a still-referenced Interaction that
        # outlived its client) either lands before the drain below or
        # restarts a fresh loop — never strands events behind a dead thread.
        ref = getattr(st, "client_ref", None)
        if ref is not None and ref() is None:
            st.flush_thread = None
            try:
                # Full shutdown-style drain: force-flush OPEN interactions
                # still sitting in the partial-merge buffers (their 2s
                # inactivity timers may not fire before process exit), then
                # drain the queues. Anything enqueued later re-registers via
                # start_flush_thread, so unregistering below loses nothing.
                for eid in list(st._partial_timers.keys()):
                    _flush_partial_event(eid, state=st)
                flush(state=st, _background=True)
            except Exception as e:
                logger.error(f"Error in flush loop: {e}")
            _instance_states.discard(st)
            logger.debug("[raindrop] flush loop exiting: client was collected")
            break
        time.sleep(st.upload_interval)


def flush(
    state: Optional[RaindropState] = None,
    _throttle_traces: bool = False,
    _background: bool = False,
) -> None:
    st = _resolve_state(state)
    # Most explicit caller-thread flushes get one bounded attempt per batch.
    # Event types that opt into durable explicit delivery use the same bounded
    # retry policy as the background worker.
    max_attempts = None if _background else 1

    if st.buffer is None:
        logger.error("No buffer available")
        _flush_traces(state=st, force=not _throttle_traces)
        return

    logger.debug("Starting flush")

    with st.flush_lock:
        current_buffer = st.buffer
        st.buffer = []
        current_direct_tool_spans = st._direct_tool_spans_buffer
        st._direct_tool_spans_buffer = []
        current_partials = st._partial_flush_queue
        st._partial_flush_queue = []

    logger.debug(f"Flushing buffer size: {len(current_buffer)}")

    grouped_events = {}
    for event in current_buffer:
        endpoint = event["type"]
        if endpoint not in grouped_events:
            grouped_events[endpoint] = []
        grouped_events[endpoint].append(event)

    for endpoint, events in grouped_events.items():
        policy_groups = groupby(
            events,
            key=lambda event: bool(event.get("_retry_on_explicit_flush")),
        )
        for retry_on_explicit_flush, policy_events in policy_groups:
            events_with_policy = list(policy_events)
            for i in range(0, len(events_with_policy), st.upload_size):
                batch_events = events_with_policy[i : i + st.upload_size]
                batch = [event["data"] for event in batch_events]
                batch_max_attempts = (
                    None
                    if _background or retry_on_explicit_flush
                    else max_attempts
                )
                logger.debug(f"Sending {len(batch)} events to {endpoint}")
                send_request(
                    endpoint,
                    batch,
                    state=st,
                    max_attempts=batch_max_attempts,
                )

    for partial_event in current_partials:
        # Serialization / PII redaction / size checks deliberately run here,
        # on the flush thread, so interaction.finish() stays O(1) for callers.
        # Guarded per event: one unserializable payload must not discard the
        # rest of the drained batch.
        try:
            partial_data = _serialize_partial_event(partial_event, state=st)
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
            send_request(
                "events/track_partial", partial_data, state=st, max_attempts=max_attempts
            )

    _flush_direct_tool_spans(
        current_direct_tool_spans, state=st, max_attempts=max_attempts
    )

    logger.debug("Flush complete")
    _flush_traces(state=st, force=not _throttle_traces)


# The OTLP trace pipeline is process-global (one TracerWrapper), while flush
# loops are per-client. Rate-limit loop-driven trace flushes so N clients
# don't all force-flush the same BatchSpanProcessor on independent 1s timers;
# explicit flush()/shutdown() calls always flush (force=True).
_TRACE_FLUSH_MIN_INTERVAL_SECONDS = 1.0
_trace_flush_lock = threading.Lock()
_trace_flush_last = 0.0


def _flush_traces(state: Optional[RaindropState] = None, force: bool = True) -> None:
    if not _resolve_state(state)._tracing_enabled:
        return

    if not force:
        global _trace_flush_last
        with _trace_flush_lock:
            now = time.monotonic()
            if now - _trace_flush_last < _TRACE_FLUSH_MIN_INTERVAL_SECONDS:
                return
            _trace_flush_last = now

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


def _post_local_mirror(path: str, payload: Any, state: Optional[RaindropState] = None) -> None:
    st = _resolve_state(state)
    if not st.local_workshop_url:
        return

    # The mirror obeys the shutdown deadline too: with Workshop mirroring
    # enabled, sequential 2s mirror POSTs during the final flush could
    # otherwise push process exit well past the shutdown bound.
    timeout = _LOCAL_MIRROR_TIMEOUT_SECONDS
    budget = _shutdown_budget(state=st)
    if budget is not None:
        if budget <= 0:
            logger.debug("Local Workshop mirror skipped: shutdown deadline exceeded")
            return
        timeout = min(timeout, budget)

    url = f"{st.local_workshop_url}{path}"
    # Deliberately omit Authorization: the local Workshop daemon doesn't
    # validate cloud credentials, and the mirror URL can come from env vars
    # or user input — never let a misconfigured RAINDROP_LOCAL_DEBUGGER /
    # RAINDROP_WORKSHOP host receive the cloud write key.
    headers = {"Content-Type": "application/json", **_project_id_headers(state=st)}
    try:
        requests.post(url, json=payload, headers=headers, timeout=timeout)
    except Exception as exc:
        logger.debug(
            "Local Workshop mirror to %s failed: %s",
            _redact_url_for_log(url),
            type(exc).__name__,
        )


def _post_with_retries(
    url: str,
    payload: Any,
    log_key: str,
    state: Optional[RaindropState] = None,
    max_attempts: Optional[int] = None,
) -> None:
    """POST to the cloud API with bounded timeouts and capped retries.

    Outside shutdown: up to ``max_attempts`` (default ``_HTTP_MAX_ATTEMPTS``)
    attempts with a short, capped backoff between them, each bounded by
    (connect, read) timeouts. Explicit ``flush()`` batches normally pass
    ``max_attempts=1``; plain ``track()`` batches opt into the default bounded
    retry schedule and may therefore sleep in backoff on the caller thread.

    During shutdown — checked fresh on EVERY attempt, so a shutdown that
    begins while a flush-thread POST is mid-retry takes effect immediately —
    no further retries or backoff sleeps happen and the (connect, read)
    timeouts are clamped so their SUM fits the remaining window (``requests``
    applies the two limits independently and sequentially). Once the window
    is exhausted, payloads are dropped with a rate-limited warning rather
    than wedging process exit.
    """
    st = _resolve_state(state)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.write_key}",
        **_project_id_headers(state=st),
    }
    # Never log the raw URL: a caller-configured endpoint may embed userinfo
    # credentials (https://user:pass@host/...).
    safe_url = _redact_url_for_log(url)

    attempts = max_attempts if max_attempts is not None else _HTTP_MAX_ATTEMPTS
    for attempt in range(attempts):
        budget = _shutdown_budget(state=st)
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
        elif st.shutdown_event.is_set():
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
                attempts,
                type(e).__name__,
                error_text,
            )
            # In (or after) shutdown, the remaining time is better spent on
            # other queued payloads than on retrying this one.
            if _shutdown_budget(state=st) is not None or st.shutdown_event.is_set():
                break
            status_code = e.response.status_code if e.response is not None else None
            if (
                status_code is not None
                and 400 <= status_code < 500
                and status_code != 429
            ):
                break
            if attempt < attempts - 1:
                backoff_idx = min(attempt, len(_HTTP_RETRY_BACKOFF_SECONDS) - 1)
                time.sleep(_HTTP_RETRY_BACKOFF_SECONDS[backoff_idx])

    _rate_limited_log(
        f"{log_key}.gave_up",
        logging.ERROR,
        "Failed to send request to %s",
        safe_url,
    )


def _send_traces_request(
    payload: Dict[str, Any],
    state: Optional[RaindropState] = None,
    max_attempts: Optional[int] = None,
) -> None:
    st = _resolve_state(state)
    _post_local_mirror("traces", payload, state=st)

    if not st.write_key:
        return

    url = urllib.parse.urljoin(
        st.api_url if st.api_url.endswith("/") else f"{st.api_url}/", "traces"
    )
    _post_with_retries(
        url, payload, log_key="send.traces", state=st, max_attempts=max_attempts
    )


def _flush_direct_tool_spans(
    spans: List[Dict[str, Any]],
    state: Optional[RaindropState] = None,
    max_attempts: Optional[int] = None,
) -> None:
    if not spans:
        return

    for i in range(0, len(spans), _direct_tool_upload_size):
        batch = spans[i : i + _direct_tool_upload_size]
        _send_traces_request(
            _build_direct_traces_payload(batch), state=state, max_attempts=max_attempts
        )


def _enqueue_direct_tool_span(span: Dict[str, Any], state: Optional[RaindropState] = None) -> None:
    st = _resolve_state(state)

    if len(st._direct_tool_spans_buffer) >= st.max_queue_size:
        _rate_limited_log(
            "direct_tool_span_buffer_full",
            logging.ERROR,
            "Direct tool span buffer is full. Discarding span.",
        )
        return

    if st.shutdown_event.is_set():
        _flush_direct_tool_spans([span], state=st)
        return

    with st.flush_lock:
        st._direct_tool_spans_buffer.append(span)
        start_flush_thread(state=st)


def send_request(
    endpoint: str,
    data_entries: Union[List[Dict[str, Union[str, Dict]]], Dict[str, Any]],
    state: Optional[RaindropState] = None,
    max_attempts: Optional[int] = None,
) -> None:
    st = _resolve_state(state)
    _post_local_mirror(endpoint, data_entries, state=st)

    if not st.write_key:
        return

    url = f"{st.api_url}{endpoint}"
    _post_with_retries(
        url, data_entries, log_key=f"send.{endpoint}", state=st, max_attempts=max_attempts
    )


def save_to_buffer(event: Dict[str, Union[str, Dict]], state: Optional[RaindropState] = None) -> None:
    st = _resolve_state(state)

    if len(st.buffer) >= st.max_queue_size * 0.8:
        _rate_limited_log(
            "buffer_capacity",
            logging.WARNING,
            f"Buffer is at {len(st.buffer) / st.max_queue_size * 100:.2f}% capacity",
        )

    if len(st.buffer) >= st.max_queue_size:
        _rate_limited_log(
            "buffer_full", logging.ERROR, "Buffer is full. Discarding event."
        )
        return

    logger.debug(f"Adding event to buffer: {event}")

    if st.shutdown_event.is_set():
        send_request(event["type"], [event["data"]], state=st)
        return

    with st.flush_lock:
        st.buffer.append(event)
        start_flush_thread(state=st)


def identify(
    user_id: str,
    traits: Dict[str, Union[str, int, bool, float]],
    state: Optional[RaindropState] = None,
) -> None:
    st = _resolve_state(state)
    if not _check_write_key(state=st):
        return
    data = {"user_id": user_id, "traits": traits}
    save_to_buffer({"type": "users/identify", "data": data}, state=st)


def track(
    user_id: str,
    event: str,
    event_id: Optional[str] = None,
    timestamp: Optional[str] = None,
    properties: Optional[Dict[str, Any]] = None,
    attachments: Optional[List[Attachment]] = None,
    state: Optional[RaindropState] = None,
) -> str | None:
    """Track a plain, non-AI event.

    Plain events have no conversation association: dawn's ingest
    ``TrackEventSchema`` is ``.strict()`` with no ``convo_id`` field, so there
    is no server-side home for one here. To group events into a conversation,
    use ``track_ai`` / ``begin`` (partials), which carry ``convo_id`` on the
    AI-data branch.
    """
    try:
        st = _resolve_state(state)
        if not _check_write_key(state=st):
            return None

        event_id = event_id or str(uuid.uuid4())
        payload = TrackEvent(
            event_id=event_id,
            user_id=user_id,
            event=event,
            timestamp=timestamp or _get_timestamp(),
            properties=properties or {},
            attachments=attachments,
        )
        payload.properties["$context"] = _get_context()
        if st._wizard_session is not None:
            payload.properties["raindrop.wizardSession"] = st._wizard_session

        data = payload.model_dump(mode="json")

        if st.redact_pii:
            data = perform_pii_redaction(data)

        size = _get_size(data)
        if size > max_ingest_size_bytes:
            logger.warning(
                f"[raindrop] Events larger than {max_ingest_size_bytes / (1024 * 1024)} MB may have properties truncated - "
                f"an event of size {size / (1024 * 1024):.2f} MB was logged"
            )
            return None

        save_to_buffer(
            {
                "type": "events/track",
                "data": data,
                "_defer_initial_flush": True,
                "_retry_on_explicit_flush": True,
            },
            state=st,
        )
        return event_id
    except ValidationError:
        logger.error(
            "[raindrop] Invalid data passed to track; event was not queued."
        )
        return None
    except Exception as err:
        logger.error(
            "[raindrop] track failed (%s: %s); event was not queued.",
            type(err).__name__,
            err,
        )
        return None


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
    state: Optional[RaindropState] = None,
) -> str:
    st = _resolve_state(state)
    if not _check_write_key(state=st):
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
                input=_cap_text(input, state=st) if input is not None else None,
                output=_cap_text(output, state=st) if output is not None else None,
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
    if st._wizard_session is not None:
        payload.properties["raindrop.wizardSession"] = st._wizard_session

    data = payload.model_dump(mode="json")
    data["ai_data"] = payload.ai_data.model_dump(mode="json", exclude_none=True)

    # Apply PII redaction if enabled
    if st.redact_pii:
        data = perform_pii_redaction(data)

    size = _get_size(data)
    if size > max_ingest_size_bytes:
        logger.warning(
            f"[raindrop] Events larger than {max_ingest_size_bytes / (1024 * 1024)} MB may have properties truncated - "
            f"an event of size {size / (1024 * 1024):.2f} MB was logged"
        )
        return None  # Skip adding oversized events to buffer

    save_to_buffer({"type": "events/track", "data": data}, state=st)
    return event_id


def shutdown(state: Optional[RaindropState] = None, _deadline: float | None = None) -> None:
    """Flush pending telemetry and stop, under a hard overall deadline.

    Registered via ``atexit``: a dead or slow network must never wedge the
    host process's exit. Every send issued after this point runs with a
    single attempt clamped to the remaining shutdown budget (see
    ``_post_with_retries``); once the budget is exhausted, remaining payloads
    are dropped with a rate-limited warning.

    ``_deadline`` (monotonic) lets the shared atexit hook drain SEVERAL
    clients under one overall budget instead of one full deadline each.
    """
    st = _resolve_state(state)
    logger.info("Shutting down raindrop analytics")
    st._shutdown_deadline = (
        _deadline
        if _deadline is not None
        else time.monotonic() + _SHUTDOWN_DEADLINE_SECONDS
    )

    try:
        for eid in list(st._partial_timers.keys()):
            _flush_partial_event(eid, state=st)

        st.shutdown_event.set()
        if st.flush_thread:
            budget = _shutdown_budget(state=st)
            st.flush_thread.join(
                timeout=max(0.1, budget if budget is not None else 10.0)
            )
        flush(state=st)  # Final flush to ensure all events are sent
    finally:
        # Scope the deadline to this call: nothing runs after the atexit hook
        # in production, but tests (and manual callers) may keep using the
        # module after an explicit shutdown().
        st._shutdown_deadline = None
        # An explicitly shut-down instance is fully drained: drop it from the
        # atexit registry so its state doesn't outlive its usefulness.
        if isinstance(st, ClientState):
            _instance_states.discard(st)


def _check_write_key(state: Optional[RaindropState] = None) -> bool:
    st = _resolve_state(state)
    if st.write_key is None and st.local_workshop_url is None:
        logger.warning(
            "write_key is not set and no local Workshop daemon is configured. "
            "Set RAINDROP_WRITE_KEY or RAINDROP_LOCAL_DEBUGGER (or pass "
            "`local_workshop_url=...` to init) before using raindrop analytics."
        )
        return False
    return True


def _get_context() -> Dict[str, Any]:
    return {
        "library": {
            "name": "python-sdk",
            "version": VERSION,
        },
        "metadata": {
            "pyVersion": f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        },
    }


def _get_timestamp() -> str:
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


def _effective_field_limit(state: Optional[RaindropState] = None) -> int:
    """Character budget for one serialized payload field.

    Per-client override first (``Raindrop(max_text_field_chars=...)``), then
    the process-wide default (module global, settable via module ``init()``);
    the OTel span-attribute limit env var additionally applies when it is
    stricter.
    """
    limit = getattr(_resolve_state(state), "max_text_field_chars", None)
    if limit is None:
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


def _cap_text(
    value: str, limit: int | None = None, state: Optional[RaindropState] = None
) -> str:
    """Cap a raw text field BEFORE any serialization.

    The length check is O(1), so multi-MB inputs/outputs cost nothing on the
    caller's thread beyond the slice that keeps the first ``limit`` chars.
    The result, truncation marker included, never exceeds ``limit``.
    """
    if not isinstance(value, str):
        return value
    if limit is None:
        limit = _effective_field_limit(state)
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


def _dumps_bounded(
    obj: Any,
    *,
    limit: int | None = None,
    cls: Any = None,
    state: Optional[RaindropState] = None,
) -> str:
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
        limit = _effective_field_limit(state)
    if isinstance(obj, str):
        # Cap first (O(limit) dumps cost), then re-truncate: quoting and
        # escape expansion (\uXXXX) can push the encoded form past the limit.
        text = json.dumps(_cap_text(obj, limit, state=state))
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


def _should_send_prompts() -> Any:
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
    state: Optional[RaindropState] = None,
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
    st = _resolve_state(state)
    if not _check_write_key(state=st):
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

    save_to_buffer({"type": "signals/track", "data": data}, state=st)


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
    model: Optional[str] = None,
    state: Optional[RaindropState] = None,
) -> Interaction:
    """
    Starts (or resumes) an interaction and returns a helper object.

    ``model`` is nested under ``ai_data`` on the wire (the partial-ai-fields
    nested contract), matching the TS ``begin()`` model parameter. Use
    ``Interaction.set_model()`` to attach or change the model mid-lifecycle.

    Note: ``model`` alone is metadata, not AI text. An interaction opened with
    only ``model`` (no ``input``) and then finished with no ``output`` is
    dropped by the empty-AI-event gate (see ``_should_drop_empty_ai_event``,
    which mirrors the Rust SDK) with a warning — it would otherwise render as
    a phantom ``ai_generation`` row. Provide ``input`` and/or ``output`` for
    the event to ship.
    """
    st = _resolve_state(state)
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
            state=st,
        )

    eid = event_id or str(uuid.uuid4())

    # Instantiate ai_data if any AI field (input / convo_id / model) is
    # supplied so none is lost when another is set later.
    ai_data_partial = None
    if input is not None or convo_id is not None or model is not None:
        capped_input = _cap_text(input, state=st) if input is not None else None
        ai_data_partial = PartialAIData(
            model=model, input=capped_input, convo_id=convo_id
        )

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
    if st._tracing_enabled:
        Traceloop.set_association_properties(
            {k: v for k, v in span_attributes.items() if v is not None}
        )

    # Bind this client's routing identity (project + key hint) to the current
    # execution context so auto-instrumented spans emitted after begin()
    # returns are stamped for the same project as the interaction.
    # Concurrency-safe: contextvars are per-thread and per-asyncio-task.
    # Lifecycle: the binding rides on the Interaction and finish() removes it
    # (identity-based, non-LIFO safe); the Interaction is also the binding's
    # weakly-held OWNER, so an abandoned interaction (exception or return
    # without finish, then dropped) stops routing the moment it is collected
    # — a reused worker thread can't inherit it indefinitely. Bound LAST —
    # after everything fallible above — with the guarded tail below, so no
    # exception can escape begin() with a binding leaked.
    bound_ctx = None
    try:
        interaction = Interaction(
            eid,
            user_id=user_id,
            event=event,
            convo_id=convo_id,
            state=st,
        )
        bound_ctx = _rd_tracing.bind_current(
            st.project_id, st.auth_hint, owner=interaction
        )
        interaction._bound_ctx = bound_ctx
        st.INTERACTION_EVENT_ID_REGISTRY[eid] = interaction
        if current_trace_id is not None and current_trace_id != 0:
            st.INTERACTION_TRACE_ID_REGISTRY[current_trace_id] = interaction

        _track_ai_partial(partial_event, state=st)
    except Exception:
        # Crash protection (AGENTS.md): telemetry setup must never take the
        # host app down. Degrade like the invalid-user_id path — clean up
        # the binding and hand back a disabled no-op Interaction so caller
        # code (mutators/finish/spans) keeps running.
        _rd_tracing.unbind_current(bound_ctx)
        logger.error(
            "[raindrop] begin() failed; returning disabled interaction.",
            exc_info=True,
        )
        return Interaction(
            event_id=eid,
            user_id=user_id,
            event=event,
            convo_id=convo_id,
            disabled=True,
            state=st,
        )
    except BaseException:
        # KeyboardInterrupt/SystemExit: clean up but never swallow.
        _rd_tracing.unbind_current(bound_ctx)
        raise
    return interaction


@contextmanager
def _suppress_traceloop_banner() -> Iterator[None]:
    """Swallow Traceloop's stdout init banner without touching tracing.

    ``Traceloop.init`` unconditionally prints ``Traceloop exporting traces to
    <url>`` via a raw ``print()`` (not the logging module), so the
    instrumentation log filters can't catch it and it surfaces once per init.
    Redirect stdout only for the duration of the init call so the banner is
    hidden while tracing is fully set up. ``set_debug_logs(True)`` keeps it
    visible for troubleshooting.
    """
    if debug_logs:
        yield
        return
    with redirect_stdout(io.StringIO()):
        yield


@contextmanager
def _temp_env(key: str, value: str) -> Iterator[None]:
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
    project_id: str | None = None,
    **traceloop_kwargs: Any,
) -> None:
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
        project_id: Optional Raindrop project slug. When set, every outbound
            request attaches an ``X-Raindrop-Project-Id`` header so events
            route to the named project instead of the org default. Slugs must
            match ``^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$``; invalid values
            are logged as a warning and ignored (no exception, no header).
            Omitting it is fully backward compatible: no header is sent and
            the server falls back to the default project.
        **traceloop_kwargs: Extra kwargs forwarded to Traceloop.init().
            Can include ``instruments`` or ``block_instruments`` for
            fine-grained control over which libraries are instrumented.
    """
    _configure(
        _default_state,
        api_key=api_key,
        wizard_session=wizard_session,
        tracing_enabled=tracing_enabled,
        auto_instrument=auto_instrument,
        bypass_otel_for_tools=bypass_otel_for_tools,
        endpoint=endpoint,
        local_workshop_url=local_workshop_url,
        max_text_field_chars=max_text_field_chars,
        project_id=project_id,
        # The module-level client keeps its historical re-init semantics:
        # every init() call re-runs Traceloop.init (a de-facto no-op after
        # the first thanks to TracerWrapper's singleton), so repeated
        # configuration in tests and notebooks behaves exactly as before.
        _always_init_traceloop=True,
        **traceloop_kwargs,
    )


def _configure(
    st: RaindropState,
    *,
    api_key: str | None,
    wizard_session: str | None,
    tracing_enabled: bool,
    auto_instrument: bool,
    bypass_otel_for_tools: bool,
    endpoint: str | None,
    local_workshop_url: Any,
    max_text_field_chars: int | None,
    project_id: str | None,
    _always_init_traceloop: bool = False,
    **traceloop_kwargs: Any,
) -> None:
    """Shared configuration for the module-level client and Raindrop instances."""
    if max_text_field_chars is not None:
        if max_text_field_chars > 0:
            if st is _default_state:
                # Module-level init() keeps its historical process-wide
                # semantics (the module global is the inherited default).
                globals()["max_text_field_chars"] = max_text_field_chars
            else:
                # Instances cap ONLY themselves — constructing a client must
                # not mutate another client's (or the default's) field cap.
                st.max_text_field_chars = max_text_field_chars
        else:
            logger.warning(
                "[raindrop] init(max_text_field_chars=%r) ignored; must be > 0",
                max_text_field_chars,
            )

    resolved_local = resolve_local_workshop_url(local_workshop_url)

    st.write_key = api_key or None

    # Every configured credential registers — tracing-enabled or not. Global
    # auto-instrumentation traces a non-tracing client's code paths all the
    # same, so the export guard must know a second key exists in the process
    # even when that client never touches the tracing pipeline itself.
    _rd_tracing.register_client_key(_rd_tracing.auth_hint_for_key(st.write_key))

    resolved_project_id = _resolve_project_id(project_id)
    st.project_id = resolved_project_id

    if endpoint is not None:
        st.api_url = endpoint if endpoint.endswith("/") else f"{endpoint}/"

    st.local_workshop_url = resolved_local

    st._wizard_session = wizard_session

    st._tracing_enabled = tracing_enabled

    st._bypass_otel_for_tools = bool(bypass_otel_for_tools and tracing_enabled)

    if not st._tracing_enabled:
        if st is _default_state:
            _remove_instrumentation_filters()
        return

    # Traceloop's OTEL exporter sends to the cloud endpoint and authenticates
    # with the cloud API key. With no key we'd either see export-time auth
    # errors or silently dropped spans, so disable tracing entirely until the
    # caller supplies one. Local-only Workshop mode still gets manual events
    # (track_ai, identify, signals) via the analytics fan-out path.
    if not st.write_key:
        st._tracing_enabled = False
        st._bypass_otel_for_tools = False
        logger.warning(
            "[raindrop] tracing_enabled=True requires api_key for OTEL export; "
            "disabling auto-instrumentation. Pass api_key=... or unset "
            "tracing_enabled to silence this warning."
        )
        if st is _default_state:
            _remove_instrumentation_filters()
        return

    if not debug_logs:
        _install_instrumentation_filters()

    # When auto_instrument is False (default), disable all auto-instrumentation
    # unless the caller explicitly passed `instruments` or `block_instruments`.
    if not auto_instrument and "instruments" not in traceloop_kwargs:
        traceloop_kwargs["instruments"] = set()

    parsed_url = urllib.parse.urlparse(st.api_url)
    api_endpoint = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Route auto-instrumented OTEL spans to the same project as manual events.
    if resolved_project_id:
        caller_headers = traceloop_kwargs.get("headers")
        if not caller_headers:
            # No caller headers: Traceloop only synthesizes the bearer
            # ``Authorization`` header when none are supplied, so we re-add it
            # alongside the project header. The no-project path stays
            # byte-identical (we don't touch ``headers`` at all there).
            traceloop_kwargs["headers"] = {
                "Authorization": f"Bearer {api_key}",
                PROJECT_ID_HEADER: resolved_project_id,
            }
        elif isinstance(caller_headers, dict):
            # Merge into caller-owned headers so OTEL spans route consistently
            # with manual events. A copy (not in-place mutation) avoids
            # surprising the caller's dict; their own values win, so an
            # explicit project/Authorization header passed by the caller is
            # left untouched.
            traceloop_kwargs["headers"] = {
                PROJECT_ID_HEADER: resolved_project_id,
                **caller_headers,
            }

    caller_span_postprocess = traceloop_kwargs.pop(
        "span_postprocess_callback", None
    )

    def span_postprocess_callback(span: ReadableSpan) -> None:
        if caller_span_postprocess is not None:
            caller_span_postprocess(span)
        normalize_model_usage_span(span)

    traceloop_kwargs["span_postprocess_callback"] = span_postprocess_callback

    # --- One span pipeline per process --------------------------------------
    # OTel/Traceloop is a process singleton: one tracer provider, one OTLP
    # exporter authenticating with ONE key. The first tracing-enabled client
    # owns it. Later tracing-enabled clients share the pipeline: same key is
    # business as usual (spans route per-project via the raindrop.project_id
    # attribute), a different key is unsupported — its spans are dropped by
    # the export guard rather than silently delivered to the owner's org.
    #
    # The claim -> init -> (release on failure) sequence runs under one lock
    # so a client constructed concurrently with the claimer waits for the
    # claimer's OUTCOME: if that init failed and released the claim, the
    # waiter claims and initializes cleanly instead of sharing a phantom
    # pipeline.
    auth_hint = _rd_tracing.auth_hint_for_key(st.write_key)
    with _rd_tracing.pipeline_init_lock:
        claimed = _rd_tracing.claim_pipeline(auth_hint, resolved_project_id)
        owner_hint = _rd_tracing.pipeline_owner_hint()
        if not claimed and auth_hint != owner_hint:
            # From this point on the process contains code paths belonging to
            # a different key/org, so unstamped spans are no longer provably
            # the owner's: the export guard flips to positive attribution
            # (only spans stamped with the owner's hint export). See
            # _GuardedSpanExporter._partition.
            _rd_tracing.mark_foreign_client()
            logger.warning(
                "[raindrop] The OTel tracing pipeline is already initialized "
                "with a DIFFERENT api_key. One process supports one tracing "
                "key/org: auto-instrumented spans from this client will be "
                "dropped at export, and spans not bound to any client "
                "(no begin()/as_current()) will be dropped as unattributable "
                "(manual events are unaffected and route normally). Run this "
                "client in its own process for tracing."
            )

        if claimed or _always_init_traceloop:
            # Build the span exporter ourselves — byte-identical to the one
            # Traceloop would build (same endpoint join + headers) — wrapped
            # in the cross-key export guard. Only the CLAIMING init builds
            # one: on a legacy module-level re-init, Traceloop's TracerWrapper
            # singleton ignores any new exporter/headers, so the original
            # guarded exporter (and its credential) provably stays in place.
            #
            # FAIL CLOSED: the guard is a security control (it is what makes
            # "a different key's spans are dropped, never exported under the
            # wrong org" true). If it cannot be installed — unsupported
            # headers type or exporter construction failure — tracing is
            # disabled for this init rather than running unguarded.
            if claimed:
                try:
                    caller_exporter = traceloop_kwargs.get("exporter")
                    if caller_exporter is not None:
                        # BYO exporter keeps its transport but not an exemption
                        # from the security control: wrap it in the guard.
                        traceloop_kwargs["exporter"] = (
                            _rd_tracing._GuardedSpanExporter(
                                caller_exporter, owner_hint
                            )
                        )
                    else:
                        exporter_headers = traceloop_kwargs.get("headers")
                        if isinstance(exporter_headers, str):
                            # Same parser Traceloop.init applies to str headers.
                            from opentelemetry.util.re import parse_env_headers

                            exporter_headers = parse_env_headers(exporter_headers)
                        if exporter_headers is None:
                            exporter_headers = {
                                "Authorization": f"Bearer {api_key}"
                            }
                        if not isinstance(exporter_headers, dict):
                            raise TypeError(
                                "unsupported traceloop headers type: "
                                f"{type(exporter_headers).__name__}"
                            )
                        traceloop_kwargs["exporter"] = (
                            _rd_tracing.build_guarded_exporter(
                                api_endpoint, exporter_headers, owner_hint
                            )
                        )
                except Exception as exc:
                    st._tracing_enabled = False
                    st._bypass_otel_for_tools = False
                    _rd_tracing.release_pipeline_claim()
                    logger.warning(
                        "[raindrop] could not install the guarded span "
                        "exporter (%s: %s); disabling tracing rather than "
                        "running an unguarded pipeline. Manual events are "
                        "unaffected.",
                        type(exc).__name__,
                        exc,
                    )
                    return

            try:
                with _temp_env(
                    "TRACELOOP_METRICS_ENABLED", "false"
                ), _suppress_traceloop_banner():
                    Traceloop.init(
                        api_endpoint=api_endpoint,
                        api_key=api_key,
                        telemetry_enabled=False,
                        **traceloop_kwargs,
                    )
            except Exception as e:
                # Never crash the host app over telemetry setup: continue
                # with tracing disabled; manual events (track_ai/begin/
                # signals) still work through the analytics pipeline.
                st._tracing_enabled = False
                st._bypass_otel_for_tools = False
                if claimed:
                    # Don't leave a phantom claim: the next tracing-enabled
                    # client should get a clean init attempt.
                    _rd_tracing.release_pipeline_claim()
                logger.warning(
                    "[raindrop] tracing initialization failed (%s: %s); "
                    "continuing with tracing disabled.",
                    type(e).__name__,
                    e,
                )
                return
        else:
            logger.debug(
                "[raindrop] tracing pipeline already initialized; sharing it "
                "(spans from this client route via the raindrop.project_id "
                "span attribute)."
            )

    _register_context_span_processor()


_context_span_processor_added = False


def _register_context_span_processor() -> None:
    """Attach the per-span project/key stamper to the active tracer provider.

    Idempotent per process: OTel rejects duplicate provider setup and
    Traceloop.init() is effectively a singleton, so we register the processor
    at most once. Best-effort — a missing provider (e.g. a no-op
    ProxyTracerProvider without ``add_span_processor``) or any error must
    never crash init().
    """
    global _context_span_processor_added
    if _context_span_processor_added:
        return
    try:
        provider = trace.get_tracer_provider()
        add_processor = getattr(provider, "add_span_processor", None)
        if add_processor is None:
            return
        add_processor(_rd_tracing._RaindropContextSpanProcessor())
        _context_span_processor_added = True
    except Exception as exc:
        logger.debug(
            "[raindrop] could not register context span processor: %s", exc
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


def set_span_properties(
    properties: Dict[str, Any], state: Optional[RaindropState] = None
) -> None:
    """
    Set association properties on the current span for tracing.

    Gates on the DEFAULT (module-level) client's tracing flag when called
    without a state — it is the module-level API. Instance users should call
    ``Raindrop.set_span_properties``, which gates on that client's flag.

    Args:
        properties: Dictionary of properties to associate with the current span
    """
    if not _resolve_state(state)._tracing_enabled:
        return

    Traceloop.set_association_properties(properties)


class TraceEntitySpan:
    def __init__(self, span: Any, state: Optional[RaindropState] = None) -> None:
        self._span = span
        # Owning client's state: set_properties must gate on the OWNER's
        # tracing flag, not the module default's — an instance-only-tracing
        # process has the module flag off while instance spans are live.
        self._state = state

    def record_input(self, data: Any) -> None:
        if self._span and _should_send_prompts():
            try:
                truncated = _dumps_bounded(
                    {"args": [data]}, cls=JSONEncoder, state=self._state
                )
                self._span.set_attribute(
                    SpanAttributes.TRACELOOP_ENTITY_INPUT, truncated
                )
            except TypeError as e:
                logger.debug(f"[raindrop] Could not serialize input for span: {e}")

    def record_output(self, data: Any) -> None:
        if self._span and _should_send_prompts():
            try:
                truncated = _dumps_bounded(data, cls=JSONEncoder, state=self._state)
                self._span.set_attribute(
                    SpanAttributes.TRACELOOP_ENTITY_OUTPUT, truncated
                )
            except TypeError as e:
                logger.debug(f"[raindrop] Could not serialize output for span: {e}")

    def set_properties(self, props: Dict[str, Any]) -> None:
        if _resolve_state(self._state)._tracing_enabled and props:
            Traceloop.set_association_properties(props)


class ManualSpan:
    """
    A manually-controlled span for async/distributed operations.
    Unlike context-managed spans, this requires explicit .end() calls.
    """

    def __init__(
        self,
        span: Any,
        kind: str,
        name: str,
        event_id: str | None = None,
        state: Optional[RaindropState] = None,
    ) -> None:
        self._span = span
        self._kind = kind
        self._name = name
        self._event_id = event_id
        # Owning client's state: sizes record_input/record_output payload
        # caps with that client's max_text_field_chars.
        self._state = state
        self._ended = False

    @property
    def event_id(self) -> str | None:
        return self._event_id

    def record_input(self, data: Any) -> None:
        if self._span and _should_send_prompts():
            try:
                truncated = _dumps_bounded(
                    {"args": [data]}, cls=JSONEncoder, state=self._state
                )
                self._span.set_attribute(
                    SpanAttributes.TRACELOOP_ENTITY_INPUT, truncated
                )
            except TypeError as e:
                logger.debug(f"[raindrop] Could not serialize input for span: {e}")

    def record_output(self, data: Any) -> None:
        if self._span and _should_send_prompts():
            try:
                truncated = _dumps_bounded(data, cls=JSONEncoder, state=self._state)
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
    def __init__(
        self,
        kind: Literal["task", "tool"],
        name: str,
        version: int | None,
        state: Optional[RaindropState] = None,
    ) -> None:
        self._kind = kind
        self._name = name
        self._version = version
        self._state = state
        self._span = None
        self._ctx_token = None
        self._span_cm = None
        self._helper = TraceEntitySpan(None, state=state)

    # internal start/finish
    def _start(self) -> None:
        st = _resolve_state(self._state)
        if not st._tracing_enabled or not TracerWrapper.verify_initialized():
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

        # Pin the owning client's routing identity, like start_span/track_tool:
        # an instance's task/tool span must route to that instance's project
        # even without an ambient begin()/as_current() binding. The context
        # processor still covers spans from the default (project-less) client.
        _rd_tracing.stamp_span(span, st.project_id, st.auth_hint)

        self._span = span
        self._helper = TraceEntitySpan(span, state=self._state)

    def _end(self, exc_type: Any, exc: Any, tb: Any) -> bool:
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

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        return self._end(exc_type, exc, tb)

    # async
    async def __aenter__(self) -> TraceEntitySpan:
        self._start()
        return self._helper

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        return self._end(exc_type, exc, tb)


def task_span(
    name: str, version: int | None = None, state: Optional[RaindropState] = None
) -> _EntitySpanContext:
    return _EntitySpanContext("task", name, version, state=state)


def tool_span(
    name: str, version: int | None = None, state: Optional[RaindropState] = None
) -> _EntitySpanContext:
    return _EntitySpanContext("tool", name, version, state=state)


def start_span(
    kind: Literal["task", "tool"],
    name: str,
    version: int | None = None,
    event_id: str | None = None,
    user_id: str | None = None,
    event: str | None = None,
    convo_id: str | None = None,
    state: Optional[RaindropState] = None,
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
    st = _resolve_state(state)
    if not st._tracing_enabled or not TracerWrapper.verify_initialized():
        return ManualSpan(None, kind, name, event_id, state=st)

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

    # Pin the owning client's routing identity on the span itself: a manual
    # span may be created/ended from a different task/thread than the one
    # that bound the context, so the on-start context stamp alone isn't
    # sufficient.
    _rd_tracing.stamp_span(span, st.project_id, st.auth_hint)

    return ManualSpan(span, kind, name, event_id, state=st)


def resume_interaction(event_id: str | None = None, state: Optional[RaindropState] = None) -> Interaction:
    """Return an Interaction associated with the current trace or given event_id."""
    st = _resolve_state(state)

    if event_id is not None:
        if (interaction := st.INTERACTION_EVENT_ID_REGISTRY.get(event_id)) is not None:
            return interaction
        return Interaction(event_id, state=st)

    if (trace_id := _safe_current_trace_id()) is not None:
        if (interaction := st.INTERACTION_TRACE_ID_REGISTRY.get(trace_id)) is not None:
            return interaction

    # Fallback: create a fresh Interaction when no identifiers are available
    # TODO: Return No-Op interaction if event_id is None
    logger.debug("No interaction found, creating a new one")
    return Interaction(state=st)


def _track_ai_partial(event: PartialTrackAIEvent, state: Optional[RaindropState] = None) -> None:
    """
    Merge the incoming patch into an in-memory doc and flush to backend:
      • on `.finish()`  (is_pending == False)
      • or after 20 s of inactivity
    """
    st = _resolve_state(state)
    eid = event.event_id

    # 1. merge
    existing = st._partial_buffers.get(eid, PartialTrackAIEvent(event_id=eid))
    existing.is_pending = (
        existing.is_pending if existing.is_pending is not None else True
    )
    merged_dict = existing.model_dump(exclude_none=True)
    incoming = event.model_dump(exclude_none=True)

    # deep merge ai_data / properties
    def _deep(d: dict, u: dict) -> dict:
        for k, v in u.items():
            d[k] = (
                _deep(d.get(k, {}) if isinstance(v, dict) else v, v)
                if isinstance(v, dict)
                else v
            )
        return d

    merged = _deep(merged_dict, incoming)
    merged_obj = PartialTrackAIEvent(**merged)

    st._partial_buffers[eid] = merged_obj

    # 2. timer handling
    if t := st._partial_timers.get(eid):
        t.cancel()
    if merged_obj.is_pending is False:
        _flush_partial_event(eid, state=st)
    else:
        st._partial_timers[eid] = Timer(
            _PARTIAL_TIMEOUT, _flush_partial_event, args=[eid], kwargs={"state": st}
        )
        st._partial_timers[eid].daemon = True
        st._partial_timers[eid].start()

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


def _serialize_partial_event(
    evt: PartialTrackAIEvent, state: Optional[RaindropState] = None
) -> Optional[Dict[str, Any]]:
    """Serialize a buffered partial event for ``events/track_partial``.

    Runs on the background flush thread (or synchronously during shutdown) —
    NOT on the caller's thread. Returns ``None`` when the event should be
    skipped (oversized).
    """
    st = _resolve_state(state)
    # convert to ordinary TrackAIEvent-ish dict before send
    data = evt.model_dump(mode="json", exclude_none=True)

    # Inject wizard session if set
    if st._wizard_session is not None:
        if "properties" not in data or data["properties"] is None:
            data["properties"] = {}
        data["properties"]["raindrop.wizardSession"] = st._wizard_session

    # Apply PII redaction if enabled
    if st.redact_pii:
        data = perform_pii_redaction(data)

    size = _get_size(data)
    if size > max_ingest_size_bytes:
        logger.warning(f"[raindrop] partial event {evt.event_id} > 1 MB; skipping")
        return None

    return data


def _flush_partial_event(event_id: str, state: Optional[RaindropState] = None) -> None:
    """
    Enqueue the accumulated patch for asynchronous send to `events/track_partial`.

    The caller — often a request hot path or an asyncio event loop — only pops
    the buffer and enqueues the model object; serialization, PII redaction,
    and size checks all run on the background ``flush_loop`` thread (see
    ``_serialize_partial_event``), so ``interaction.finish()`` is O(1) for the
    caller regardless of payload size. During shutdown the event is serialized
    and sent synchronously under the shutdown deadline.
    """
    st = _resolve_state(state)
    if t := st._partial_timers.pop(event_id, None):
        t.cancel()

    evt = st._partial_buffers.pop(event_id, None)
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

    if st.shutdown_event.is_set():
        # Synchronous send on the caller's thread (e.g. a late finish()
        # during atexit ordering). Guarded like the flush-thread path: a
        # serialization failure must never propagate into caller code.
        try:
            data = _serialize_partial_event(evt, state=st)
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
            send_request("events/track_partial", data, state=st)
        return

    with st.flush_lock:
        if len(st._partial_flush_queue) >= st.max_queue_size:
            _rate_limited_log(
                "partial_queue_full",
                logging.ERROR,
                "Partial queue is full. Discarding event.",
            )
            return
        st._partial_flush_queue.append(evt)
        start_flush_thread(state=st)


def _shutdown_all() -> None:
    """atexit hook: drain the default client and all live instance states.

    ALL clients — default included — share ONE overall deadline, so a
    process with several clients and a dead network exits within the same
    ``_SHUTDOWN_DEADLINE_SECONDS`` bound as a single-client process. Iterates
    STATES (held strongly while their pipeline is live) rather than client
    objects, so buffered events survive to exit even when the host app
    dropped its last reference to the client itself.
    """
    deadline = time.monotonic() + _SHUTDOWN_DEADLINE_SECONDS
    shutdown(_deadline=deadline)
    for st in list(_instance_states):
        try:
            shutdown(state=st, _deadline=deadline)
        except Exception as e:
            logger.debug("[raindrop] instance shutdown failed: %s", e)

    # Final PROCESS-GLOBAL trace flush: the OTLP pipeline outlives the client
    # that initialized it (auto-instrumentation keeps producing spans after
    # that client is shut down or collected), and the per-client flushes
    # above only run _flush_traces for clients whose own tracing flag is
    # set. Flush the shared TracerWrapper directly so spans buffered after
    # the owner disappeared aren't dropped at exit. Gated on pipeline
    # ownership: in never-traced processes, TracerWrapper.verify_initialized
    # PRINTS a not-initialized warning to stdout — never pollute exits.
    if _rd_tracing.pipeline_owner_hint() is None:
        return
    try:
        if TracerWrapper.verify_initialized():
            TracerWrapper().flush()
    except Exception as e:
        logger.debug("[raindrop] final global trace flush failed: %s", e)


atexit.register(_shutdown_all)
