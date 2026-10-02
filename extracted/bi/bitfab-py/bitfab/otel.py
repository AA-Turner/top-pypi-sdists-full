from __future__ import annotations

import json
import logging
import os
import random
import threading
import time
from collections.abc import Callable, Mapping, Sequence
from typing import Any, NamedTuple

from opentelemetry import trace
from opentelemetry.metrics import NoOpMeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, SpanLimits, TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SpanExporter,
    SpanExportResult,
)
from opentelemetry.sdk.trace.sampling import ALWAYS_ON
from opentelemetry.trace import Status, StatusCode

from bitfab.compress import PreparedRequest, prepare_request_body
from bitfab.constants import __version__
from bitfab.payload_budget import (
    MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES,
    MAX_SPAN_CARRIER_BYTES,
    enforce_payload_budget,
)
from bitfab.serialize import encode_json
from bitfab.transport_types import (
    CarrierMeta,
    CarrierRef,
    DeliveryError,
    DirectBatchSender,
    TraceOperation,
)
from bitfab.warn_once import warn_once

logger = logging.getLogger(__name__)

_OPERATION_ATTRIBUTE = "bitfab.operation"
_PAYLOAD_ATTRIBUTE = "bitfab.payload"
_MAX_EXPORT_REQUEST_BYTES = 3_000_000
_MAX_DECOMPRESSED_REQUEST_BYTES = 8_000_000
_MAX_REQUEST_BYTES_ENV = "BITFAB_OTEL_MAX_REQUEST_BYTES"
_EXPORT_CONCURRENCY_ENV = "BITFAB_OTEL_EXPORT_CONCURRENCY"
_MAX_QUEUE_SIZE = 16_384
_DIRECT_MAX_EXPORT_BATCH_SIZE = 512
_DIRECT_MAX_REQUEST_BATCH_SIZE = 256
_DEFAULT_EXPORT_CONCURRENCY = 32
_MAX_EXPORT_CONCURRENCY = 64
_SCHEDULE_DELAY_MILLIS = 5_000
_EXPORT_TIMEOUT_MILLIS = 30_000
_RETRY_BASE_DELAY_MILLIS = 100
# The longest we will hold a batch waiting. A server asking for longer than this
# is asking for more than one export window: honoring it means not sending at
# all, never coming back early.
# Ceiling on the exponential growth of our OWN backoff. It does not bound a
# wait the server asked for: OTLP says to honor Retry-After, and calls data
# dropped while throttled the outcome to avoid. What bounds an honored wait is
# the export budget, since the processor kills an export that outlives it.
_RETRY_BACKOFF_CEILING_MILLIS = 5_000

_live_transports: set[OtelBatchTransport] = set()
_live_transports_lock = threading.Lock()


class _CarrierPayload(str):
    """A payload attribute whose Python-only state follows its carrier span."""

    __slots__ = ("ref",)

    def __new__(cls, value: str, ref: CarrierRef) -> _CarrierPayload:
        instance = super().__new__(cls, value)
        instance.ref = ref
        return instance


def _max_request_bytes_from_env() -> int:
    raw = os.environ.get(_MAX_REQUEST_BYTES_ENV)
    if raw is None:
        return _MAX_EXPORT_REQUEST_BYTES
    try:
        value = int(raw)
    except ValueError:
        value = 0
    if 0 < value <= _MAX_EXPORT_REQUEST_BYTES:
        return value
    warn_once(
        "otel-max-request-bytes-invalid",
        f"{_MAX_REQUEST_BYTES_ENV} must be a positive integer no greater than "
        f"{_MAX_EXPORT_REQUEST_BYTES}; using {_MAX_EXPORT_REQUEST_BYTES}",
    )
    return _MAX_EXPORT_REQUEST_BYTES


def _export_concurrency_from_env() -> int:
    raw = os.environ.get(_EXPORT_CONCURRENCY_ENV)
    if raw is None:
        return _DEFAULT_EXPORT_CONCURRENCY
    try:
        value = int(raw)
    except ValueError:
        value = 0
    if 0 < value <= _MAX_EXPORT_CONCURRENCY:
        return value
    warn_once(
        "otel-export-concurrency-invalid",
        f"{_EXPORT_CONCURRENCY_ENV} must be a positive integer no greater than "
        f"{_MAX_EXPORT_CONCURRENCY}; using {_DEFAULT_EXPORT_CONCURRENCY}",
    )
    return _DEFAULT_EXPORT_CONCURRENCY


def _reset_transports_after_fork() -> None:
    global _live_transports_lock
    _live_transports_lock = threading.Lock()
    for transport in list(_live_transports):
        transport._reset_state_after_fork()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_transports_after_fork)


def _otlp_value(value: Any) -> dict[str, Any]:
    if isinstance(value, bool):
        return {"boolValue": value}
    if isinstance(value, int):
        return {"intValue": str(value)}
    if isinstance(value, float):
        return {"doubleValue": value}
    if isinstance(value, str):
        return {"stringValue": value}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return {"arrayValue": {"values": [_otlp_value(item) for item in value]}}
    return {"stringValue": str(value)}


def _otlp_attributes(attributes: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    if attributes is None:
        return []
    return [
        {"key": key, "value": _otlp_value(value)} for key, value in attributes.items()
    ]


def _span_to_otlp(span: ReadableSpan) -> dict[str, Any]:
    context = span.context
    parent = span.parent
    result: dict[str, Any] = {
        "traceId": trace.format_trace_id(context.trace_id),
        "spanId": trace.format_span_id(context.span_id),
        "name": span.name,
        "kind": span.kind.value + 1,
        "startTimeUnixNano": str(span.start_time or 0),
        "endTimeUnixNano": str(span.end_time or 0),
        "attributes": _otlp_attributes(span.attributes),
        "droppedAttributesCount": span.dropped_attributes,
        "droppedEventsCount": span.dropped_events,
        "droppedLinksCount": span.dropped_links,
        "status": {
            "code": int(span.status.status_code.value),
            **({"message": span.status.description} if span.status.description else {}),
        },
        "flags": int(context.trace_flags),
    }
    if parent is not None and parent.span_id:
        result["parentSpanId"] = trace.format_span_id(parent.span_id)
    if context.trace_state:
        result["traceState"] = context.trace_state.to_header()
    return result


class _EncodedSpan(NamedTuple):
    """A span encoded exactly as it goes on the wire, carrying its byte count.

    Encoding once and remembering the size is what keeps request packing linear:
    sizing a candidate batch by re-encoding the whole request re-escapes every
    carrier's ``bitfab.payload`` string on every span considered.
    """

    encoded: str
    size: int
    ref: CarrierRef | None = None


class _RequestEnvelope(NamedTuple):
    """The invariant head and tail of an OTLP request for one export window.

    Key order matches what :func:`encode_json` emits for the equivalent dict, so
    a body assembled by concatenation is byte-identical to encoding that dict.
    """

    head: str
    tail: str
    size: int


class _RequestBatch(NamedTuple):
    spans: list[_EncodedSpan]
    encoded_size: int


# The comma that joins adjacent spans in the request's span list.
_SPAN_SEPARATOR_BYTES = 1


def _encode_span(span: ReadableSpan) -> _EncodedSpan:
    encoded = encode_json(_span_to_otlp(span))
    payload = (span.attributes or {}).get(_PAYLOAD_ATTRIBUTE)
    return _EncodedSpan(
        encoded,
        len(encoded.encode("utf-8")),
        payload.ref if isinstance(payload, _CarrierPayload) else None,
    )


def _request_envelope(first: ReadableSpan) -> _RequestEnvelope:
    scope = first.instrumentation_scope
    resource = encode_json({"attributes": _otlp_attributes(first.resource.attributes)})
    scope_json = encode_json({"name": scope.name, "version": scope.version or ""})
    head = (
        '{"resourceSpans":[{"resource":'
        + resource
        + ',"scopeSpans":[{"scope":'
        + scope_json
        + ',"spans":['
    )
    tail = "]}]}]}"
    return _RequestEnvelope(head, tail, len((head + tail).encode("utf-8")))


def _encode_request(envelope: _RequestEnvelope, spans: Sequence[_EncodedSpan]) -> str:
    return envelope.head + ",".join(span.encoded for span in spans) + envelope.tail


def _trim_encoded_span(span: _EncodedSpan) -> _EncodedSpan | None:
    try:
        carrier = json.loads(span.encoded)
        attributes = carrier.get("attributes", [])
        attribute = next(
            entry for entry in attributes if entry.get("key") == _PAYLOAD_ATTRIBUTE
        )
        value = attribute["value"]
        payload = json.loads(value["stringValue"])
        _, body, _ = enforce_payload_budget(
            payload, encode_json(payload), encode_json, MAX_SPAN_CARRIER_BYTES
        )
        value["stringValue"] = body
        encoded = encode_json(carrier)
        return _EncodedSpan(encoded, len(encoded.encode("utf-8")))
    except (KeyError, StopIteration, TypeError, ValueError):
        return None


def _is_retryable(error: BaseException) -> bool:
    """Only what the sender classified. Anything else reaching here is a fault
    in the sender itself, and retrying a deterministic bug just delays it."""
    return isinstance(error, DeliveryError) and error.retryable


def _is_oversized(error: BaseException) -> bool:
    return isinstance(error, DeliveryError) and error.oversized


def _retry_wait_seconds(
    error: BaseException, attempt: int, remaining_seconds: float
) -> float | None:
    """How long to wait before the next attempt, or None when the wait cannot be
    served inside ``remaining_seconds`` and the batch has to be given up.

    A server that sent ``Retry-After`` told us when it wants us back, so that
    wait is honored whole rather than shortened: coming back early is the one
    thing it asked us not to do. It is refused only when it outlasts the budget,
    where waiting would mean being killed mid-wait and losing the batch anyway.

    Half the budget, not all of it: a wait is only worth taking if what is left
    afterwards can still carry the request.

    Absent an instruction, back off exponentially so a struggling server is not
    hit on a fixed cadence, and jitter it so every client in a fleet does not
    return in lockstep.
    """
    affordable = remaining_seconds / 2
    requested = error.retry_after_ms if isinstance(error, DeliveryError) else None
    if requested is not None:
        return requested / 1_000 if requested / 1_000 < affordable else None
    backoff = min(_RETRY_BASE_DELAY_MILLIS * 2**attempt, _RETRY_BACKOFF_CEILING_MILLIS)
    jittered = (backoff / 2 + random.random() * (backoff / 2)) / 1_000
    return jittered if jittered < affordable else None


class BitfabSpanExporter(SpanExporter):
    def __init__(
        self,
        direct_sender: DirectBatchSender,
        max_request_bytes: int,
        max_request_batch_size: int,
        export_concurrency: int,
        on_delivered: Callable[[list[CarrierRef]], None] | None = None,
        # The same budget the processor enforces around this export, so a
        # configured timeout and the deadline a wait is judged by cannot drift.
        export_timeout_millis: int = _EXPORT_TIMEOUT_MILLIS,
    ):
        self._direct_sender = direct_sender
        self._max_request_bytes = max_request_bytes
        self._max_request_batch_size = max_request_batch_size
        self._export_concurrency = export_concurrency
        self._on_delivered = on_delivered
        self._export_timeout_millis = export_timeout_millis
        # Epoch (monotonic) until which the server has asked us to stay away.
        self._throttled_until = 0.0
        self._throttle_lock = threading.Lock()

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        if not spans:
            return SpanExportResult.SUCCESS
        try:
            encoded_spans = [_encode_span(span) for span in spans]
            envelope = _request_envelope(spans[0])
        except Exception:
            logger.exception("Bitfab: failed to encode an OpenTelemetry span batch")
            return SpanExportResult.FAILURE

        batches = self._build_request_batches(envelope, encoded_spans)
        next_batch_index = 0
        index_lock = threading.Lock()
        results = [False] * len(batches)

        def worker() -> None:
            nonlocal next_batch_index
            while True:
                with index_lock:
                    batch_index = next_batch_index
                    if batch_index >= len(batches):
                        return
                    next_batch_index += 1
                results[batch_index] = self._send(
                    envelope,
                    batches[batch_index],
                )

        workers = [
            threading.Thread(
                target=worker,
                name="bitfab-otel-export",
                daemon=True,
            )
            for _ in range(min(self._export_concurrency, len(batches)))
        ]
        for worker_thread in workers:
            worker_thread.start()
        for worker_thread in workers:
            worker_thread.join()

        succeeded = all(results)
        return SpanExportResult.SUCCESS if succeeded else SpanExportResult.FAILURE

    def _build_request_batches(
        self,
        envelope: _RequestEnvelope,
        spans: Sequence[_EncodedSpan],
    ) -> list[_RequestBatch]:
        batches: list[_RequestBatch] = []
        current: list[_EncodedSpan] = []
        current_size = envelope.size

        for span in spans:
            addition = span.size + (_SPAN_SEPARATOR_BYTES if current else 0)
            if current and (
                len(current) >= self._max_request_batch_size
                or current_size + addition > self._max_request_bytes
            ):
                batches.append(_RequestBatch(current, current_size))
                current = []
                current_size = envelope.size
                addition = span.size
            current.append(span)
            current_size += addition

        if current:
            batches.append(_RequestBatch(current, current_size))
        return batches

    def _send(
        self,
        envelope: _RequestEnvelope,
        batch: _RequestBatch,
    ) -> bool:
        spans = batch.spans
        try:
            request_spans = list(spans)
            request_raw_bytes = batch.encoded_size
            already_trimmed = False
            while True:
                if request_raw_bytes <= _MAX_DECOMPRESSED_REQUEST_BYTES:
                    prepared = prepare_request_body(
                        _encode_request(envelope, request_spans)
                    )
                    if prepared.wire_bytes <= self._max_request_bytes:
                        self._send_with_retries(prepared)
                        # Refs come from the original spans: trimming rebuilds a
                        # span without one, and a trimmed carrier still reached
                        # the server under its own identity.
                        self._report_delivered(spans)
                        return True

                if len(spans) != 1:
                    logger.error(
                        "Bitfab: an OpenTelemetry span batch exceeded the configured "
                        "request-size target and could not be exported"
                    )
                    return False
                if already_trimmed:
                    logger.error(
                        "Bitfab: a single OpenTelemetry span exceeded the configured "
                        "request-size target after trimming"
                    )
                    return False
                trimmed = _trim_encoded_span(spans[0])
                if trimmed is None:
                    logger.error(
                        "Bitfab: a single OpenTelemetry span exceeded the configured "
                        "request-size target and could not be trimmed"
                    )
                    return False
                request_spans = [trimmed]
                request_raw_bytes = envelope.size + trimmed.size
                already_trimmed = True
        except Exception as error:
            if _is_oversized(error):
                if len(spans) == 1:
                    logger.error(
                        "Bitfab: a single OpenTelemetry span exceeded the ingestion "
                        "request limit and could not be exported"
                    )
                else:
                    logger.error(
                        "Bitfab: an OpenTelemetry span batch exceeded the ingestion "
                        "request limit and could not be exported"
                    )
                return False
            logger.exception("Bitfab: failed to export an OpenTelemetry span batch")
            return False

    def _record_throttle(self, error: BaseException) -> None:
        """Remember a throttle the server asked for, so the requests fanned out
        alongside this one respect it too. Delaying only the request that was
        refused leaves the other seven in the window hitting a server that just
        asked for room.
        """
        requested = error.retry_after_ms if isinstance(error, DeliveryError) else None
        if requested is not None:
            with self._throttle_lock:
                self._throttled_until = max(
                    self._throttled_until, time.monotonic() + requested / 1_000
                )

    def _await_throttle(self, deadline: float) -> None:
        """Waits out an active throttle, or reports the batch undeliverable when
        the throttle outlasts the export budget. Either way nothing is sent
        while the server has asked us to stay away.
        """
        with self._throttle_lock:
            remaining = self._throttled_until - time.monotonic()
        if remaining <= 0:
            return
        # Waited out, not refused: OTLP asks the client to hold off until the
        # window passes. Only a throttle outliving what the budget can serve is
        # refused, because the processor would kill the wait before it sent.
        if remaining >= (deadline - time.monotonic()) / 2:
            raise DeliveryError(
                f"OTLP ingestion is throttled for another {remaining:.1f}s, "
                "longer than the export budget"
            )
        time.sleep(remaining)

    def _send_with_retries(self, request: PreparedRequest) -> None:
        # One budget for the whole exchange, waits included: the processor kills
        # the export at this deadline, so a wait past it cannot be served.
        deadline = time.monotonic() + self._export_timeout_millis / 1_000
        for attempt in range(3):
            try:
                self._await_throttle(deadline)
                self._direct_sender(request, max(0.0, deadline - time.monotonic()))
                return
            except Exception as error:
                self._record_throttle(error)
                if _is_oversized(error):
                    raise
                if attempt == 2 or not _is_retryable(error):
                    raise
                logger.debug(
                    "OTLP request attempt %s failed, retrying: %s",
                    attempt + 1,
                    error,
                )
                wait = _retry_wait_seconds(error, attempt, deadline - time.monotonic())
                if wait is None:
                    raise
                time.sleep(wait)

    def _report_delivered(self, spans: Sequence[_EncodedSpan]) -> None:
        """Announce the carriers a request delivered. Wrapped because a listener
        that raises must never turn a delivered batch into a failed export."""
        if self._on_delivered is None:
            return
        refs = [span.ref for span in spans if span.ref is not None]
        if not refs:
            return
        try:
            self._on_delivered(refs)
        except Exception:
            logger.exception("Bitfab: a delivery listener raised")

    def shutdown(self, timeout_millis: int = 30_000) -> None:
        del timeout_millis

    def force_flush(self, timeout_millis: int = 30_000) -> bool:
        del timeout_millis
        return True


class _DeliveryTrackingExporter(SpanExporter):
    def __init__(self, exporter: SpanExporter):
        self._exporter = exporter
        self._lock = threading.Lock()
        self._failed_exports = 0

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        try:
            result = self._exporter.export(spans)
        except Exception:
            with self._lock:
                self._failed_exports += 1
            raise
        if result != SpanExportResult.SUCCESS:
            with self._lock:
                self._failed_exports += 1
        return result

    def take_failed_exports(self) -> int:
        with self._lock:
            failed_exports = self._failed_exports
            self._failed_exports = 0
        return failed_exports

    def reset_after_fork(self, exporter: SpanExporter) -> None:
        self._exporter = exporter
        self._lock = threading.Lock()
        self._failed_exports = 0

    def shutdown(self, timeout_millis: int = 30_000) -> None:
        try:
            self._exporter.shutdown(timeout_millis=timeout_millis)
        except TypeError:
            self._exporter.shutdown()

    def force_flush(self, timeout_millis: int = 30_000) -> bool:
        try:
            return self._exporter.force_flush(timeout_millis=timeout_millis)
        except TypeError:
            return self._exporter.force_flush(timeout_millis)


class OtelBatchTransport:
    def __init__(
        self,
        *,
        direct_sender: DirectBatchSender,
        max_export_batch_size: int | None = None,
        max_request_batch_size: int = _DIRECT_MAX_REQUEST_BATCH_SIZE,
        max_queue_size: int = _MAX_QUEUE_SIZE,
        export_concurrency: int = _DEFAULT_EXPORT_CONCURRENCY,
        max_request_bytes: int | None = None,
        on_delivered: Callable[[list[CarrierRef]], None] | None = None,
    ):
        self._direct_sender = direct_sender
        self._on_delivered = on_delivered
        self._max_export_batch_size = (
            max_export_batch_size
            if max_export_batch_size is not None
            else _DIRECT_MAX_EXPORT_BATCH_SIZE
        )
        if max_request_batch_size <= 0:
            raise ValueError("max_request_batch_size must be a positive integer")
        self._max_queue_size = max_queue_size
        self._export_concurrency = export_concurrency
        self._max_request_batch_size = max_request_batch_size
        self._max_request_bytes = (
            _MAX_EXPORT_REQUEST_BYTES
            if max_request_bytes is None
            else max_request_bytes
        )
        self._pid = os.getpid()
        self._state_lock = threading.RLock()
        self._flush_lock = threading.Lock()
        self._closed = False
        self._provider: TracerProvider | None = None
        self._processor: BatchSpanProcessor | None = None
        self._delivery_tracker: _DeliveryTrackingExporter | None = None
        self._tracer: trace.Tracer | None = None
        self._create_pipeline()
        with _live_transports_lock:
            _live_transports.add(self)

    def _reset_state_after_fork(self) -> None:
        self._state_lock = threading.RLock()
        self._flush_lock = threading.Lock()
        if self._delivery_tracker is not None:
            self._delivery_tracker.reset_after_fork(self._create_exporter())
        self._pid = os.getpid()

    def _ensure_process(self) -> None:
        current_pid = os.getpid()
        if self._pid == current_pid and self._processor is not None:
            return
        if self._closed:
            return
        self._pid = current_pid
        self._create_pipeline()
        with _live_transports_lock:
            _live_transports.add(self)

    def _create_exporter(self) -> SpanExporter:
        return BitfabSpanExporter(
            self._direct_sender,
            self._max_request_bytes,
            self._max_request_batch_size,
            self._export_concurrency,
            self._on_delivered,
        )

    def _create_pipeline(self) -> None:
        meter_provider = NoOpMeterProvider()
        delivery_tracker = _DeliveryTrackingExporter(self._create_exporter())
        provider = TracerProvider(
            sampler=ALWAYS_ON,
            resource=Resource(
                {
                    "service.name": "bitfab-python-sdk",
                    "service.version": __version__,
                }
            ),
            shutdown_on_exit=False,
            span_limits=SpanLimits(
                max_span_attributes=2,
                max_span_attribute_length=None,
            ),
            meter_provider=meter_provider,
        )
        provider._disabled = False
        processor = BatchSpanProcessor(
            delivery_tracker,
            max_queue_size=self._max_queue_size,
            schedule_delay_millis=_SCHEDULE_DELAY_MILLIS,
            max_export_batch_size=self._max_export_batch_size,
            export_timeout_millis=_EXPORT_TIMEOUT_MILLIS,
            meter_provider=meter_provider,
        )
        provider.add_span_processor(processor)
        self._provider = provider
        self._processor = processor
        self._delivery_tracker = delivery_tracker
        self._tracer = provider.get_tracer("bitfab", __version__)

    def submit(
        self,
        operation: TraceOperation,
        payload: dict[str, Any],
        encoded_payload: str | None = None,
        meta: CarrierMeta | None = None,
    ) -> None:
        meta = meta or CarrierMeta()
        with self._state_lock:
            if self._closed:
                warn_once(
                    "otel-submit-after-shutdown",
                    "OpenTelemetry transport is shut down; dropping spans",
                )
                return
            self._ensure_process()
            try:
                if encoded_payload is None:
                    # A caller that pre-encoded already went through the budget
                    # in _encode_payload; one that did not still must not build
                    # a carrier the exporter would drop for being oversized.
                    payload, encoded_payload, _ = enforce_payload_budget(
                        payload,
                        encode_json(payload),
                        encode_json,
                        MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES,
                    )
                tracer = self._tracer
                if tracer is None:
                    raise RuntimeError("OpenTelemetry transport is not available")
                span = tracer.start_span(
                    meta.name or f"bitfab.{operation}",
                    attributes={
                        _OPERATION_ATTRIBUTE: operation,
                        _PAYLOAD_ATTRIBUTE: (
                            _CarrierPayload(encoded_payload, meta.ref)
                            if meta.ref is not None
                            else encoded_payload
                        ),
                    },
                    start_time=meta.start_time_ns or time.time_ns(),
                )
                if meta.errored:
                    span.set_status(Status(StatusCode.ERROR))
                span.end(end_time=meta.end_time_ns or time.time_ns())
            except Exception:
                logger.exception("Bitfab: failed to queue an OpenTelemetry span")

    def _force_flush(self, timeout: float | None) -> bool:
        with self._state_lock:
            self._ensure_process()
            processor = self._processor
            delivery_tracker = self._delivery_tracker
        if processor is None:
            return True
        timeout_millis = None if timeout is None else max(0, int(timeout * 1_000))
        result: list[bool] = []

        def force_flush() -> None:
            with self._flush_lock:
                try:
                    flushed = processor.force_flush(timeout_millis=timeout_millis)
                except Exception:
                    logger.exception("Bitfab: failed to flush OpenTelemetry spans")
                    flushed = False
                failed_exports = (
                    delivery_tracker.take_failed_exports()
                    if delivery_tracker is not None
                    else 0
                )
                result.append(flushed and failed_exports == 0)

        if timeout is None:
            force_flush()
        else:
            flush_thread = threading.Thread(target=force_flush, daemon=True)
            flush_thread.start()
            flush_thread.join(max(timeout, 0))
            if flush_thread.is_alive():
                return False
        return result == [True]

    def flush(self, timeout: float = 30.0) -> bool:
        return self._force_flush(timeout)

    def shutdown(self, timeout: float = 30.0) -> bool:
        deadline = time.monotonic() + max(timeout, 0)
        with self._state_lock:
            self._closed = True
        flushed = self.flush(max(0.0, deadline - time.monotonic()))
        with self._state_lock:
            processor = self._processor
            self._processor = None
            self._provider = None
            self._delivery_tracker = None
            self._tracer = None
        if processor is None:
            with _live_transports_lock:
                _live_transports.discard(self)
            return flushed

        shutdown_thread = threading.Thread(target=processor.shutdown, daemon=True)
        shutdown_thread.start()
        shutdown_thread.join(max(0.0, deadline - time.monotonic()))
        with self._state_lock:
            if self._processor is None:
                with _live_transports_lock:
                    _live_transports.discard(self)
        if shutdown_thread.is_alive():
            return False
        return flushed


def create_otel_transport(
    *,
    direct_sender: DirectBatchSender,
    on_delivered: Callable[[list[CarrierRef]], None] | None = None,
) -> OtelBatchTransport:
    return OtelBatchTransport(
        direct_sender=direct_sender,
        export_concurrency=_export_concurrency_from_env(),
        max_request_bytes=_max_request_bytes_from_env(),
        on_delivered=on_delivered,
    )


def _current_process_transports() -> list[OtelBatchTransport]:
    current_pid = os.getpid()
    with _live_transports_lock:
        return [
            transport
            for transport in list(_live_transports)
            if transport._pid == current_pid
        ]


def flush_otel_transports(timeout: float = 30.0) -> bool:
    deadline = time.monotonic() + max(timeout, 0)
    succeeded = True
    for transport in _current_process_transports():
        succeeded = transport.flush(max(0.0, deadline - time.monotonic())) and succeeded
    return succeeded


def shutdown_otel_transports(timeout: float = 30.0) -> bool:
    deadline = time.monotonic() + max(timeout, 0)
    succeeded = True
    for transport in _current_process_transports():
        succeeded = (
            transport.shutdown(max(0.0, deadline - time.monotonic())) and succeeded
        )
    return succeeded
