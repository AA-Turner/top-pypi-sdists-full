"""Isolated replay traces, including spans from existing OTel integrations."""

from __future__ import annotations

import contextvars
import json
import threading
import weakref
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Iterator

from opentelemetry import context, trace
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor, TracerProvider
from opentelemetry.exporter.otlp.proto.common.trace_encoder import encode_spans
from google.protobuf.json_format import MessageToDict

CORRELATION_ATTRIBUTE = "raindrop.eval_correlation_id"


@dataclass
class Capture:
    correlation_id: str
    attributes: dict[str, Any] = field(default_factory=dict)
    active: int = 0
    spans: list[ReadableSpan] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)


_scope: contextvars.ContextVar[Capture | None] = contextvars.ContextVar(
    "raindrop_eval_capture", default=None
)
_processors: weakref.WeakSet[Any] = weakref.WeakSet()
_lock = threading.Lock()


class CaptureProcessor(SpanProcessor):
    def __init__(self) -> None:
        self.captures: dict[int, Capture] = {}
        self.lock = threading.Lock()

    def on_start(self, span: Any, parent_context: Any = None) -> None:
        capture = _scope.get()
        if capture:
            span.set_attribute(CORRELATION_ATTRIBUTE, capture.correlation_id)
            for key, value in capture.attributes.items():
                span.set_attribute(key, value)
            with capture.lock:
                capture.active += 1
            with self.lock:
                self.captures[span.context.span_id] = capture

    def on_end(self, span: ReadableSpan) -> None:
        with self.lock:
            capture = self.captures.pop(span.context.span_id, None)
        if capture:
            with capture.lock:
                capture.spans.append(span)
                capture.active -= 1

    def shutdown(self) -> None:
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


@contextmanager
def capture_row(
    correlation_id: str, row: Any, *, attributes: dict[str, Any] | None = None
) -> Iterator[Capture]:
    with _lock:
        provider = trace.get_tracer_provider()
        if isinstance(provider, trace.ProxyTracerProvider):
            trace.set_tracer_provider(TracerProvider())
            provider = trace.get_tracer_provider()
        if not hasattr(provider, "add_span_processor"):
            raise RuntimeError("Eval replay requires an OTel SDK TracerProvider")
        if provider not in _processors:
            provider.add_span_processor(CaptureProcessor())
            _processors.add(provider)
    capture = Capture(correlation_id, attributes=attributes or {})
    token = _scope.set(capture)
    parent_token = context.attach(trace.set_span_in_context(trace.INVALID_SPAN))
    try:
        tracer = provider.get_tracer("raindrop.evals")
        with tracer.start_as_current_span(
            "raindrop.replay.row.task",
            attributes={
                "traceloop.entity.name": "raindrop.replay.row",
                "traceloop.span.kind": "task",
                "traceloop.entity.input": json.dumps(
                    {"args": [], "kwargs": row.wire()}, ensure_ascii=False
                ),
            },
        ):
            yield capture
    finally:
        context.detach(parent_token)
        _scope.reset(token)


def record_output(result: Any) -> None:
    # The application return value, rather than an intermediate model answer, owns the event.
    value = (
        result
        if isinstance(result, str)
        else json.dumps(result, ensure_ascii=False, allow_nan=False)
    )
    trace.get_current_span().set_attribute("traceloop.entity.output", value)


async def upload_capture(
    client: Any, capture: Capture, replay_id: str, ingest_url: str
) -> dict[str, Any]:
    if capture.active:
        raise RuntimeError("Replay callback returned with unfinished child spans")
    spans = list(capture.spans)
    traces = {format(span.context.trace_id, "032x") for span in spans}
    if len(traces) != 1 or not 1 <= len(spans) <= 500:
        raise RuntimeError(
            "Replay capture requires exactly one trace and 1–500 ended spans"
        )
    body = MessageToDict(encode_spans(spans))
    response = await client.request(
        "POST", "", absolute_url=ingest_url, body=body, replay_id=replay_id, retries=2
    )
    if response.get("refused", 0) or response.get("stored") != len(spans):
        raise RuntimeError("Replay ingest refused or omitted captured spans")
    return {
        "traceId": next(iter(traces)),
        "spanIds": [format(span.context.span_id, "016x") for span in spans],
    }
