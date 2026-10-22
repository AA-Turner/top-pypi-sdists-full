from __future__ import annotations

import atexit
import contextlib
import importlib
import logging
import os
import threading
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any, cast

_TRACER_NAME = "chalk_remote_call"
_TRACE_CONTEXT_METADATA_KEYS = ("traceparent", "tracestate", "baggage")
_REMOTE_FUNCTION_TRACE_POLICY_ENV_VAR = "CHALK_REMOTE_FUNCTION_TRACE_POLICY"
_REMOTE_FUNCTION_TRACE_SAMPLE_RATE_ENV_VAR = "CHALK_REMOTE_FUNCTION_TRACE_SAMPLE_RATE"
_REMOTE_FUNCTION_TRACE_OVERRIDE_KEY = "x-chalk-remote-function-tracing"
_TRACE_OVERRIDE_ON = "on"
_TRACE_OVERRIDE_OFF = "off"
_TRACE_POLICY_PARENT_BASED_ALWAYS_OFF = "parentbased_always_off"
_TRACE_POLICY_PARENT_BASED_TRACE_ID_RATIO = "parentbased_traceidratio"
_TRACE_POLICY_ALWAYS_OFF = "always_off"
_TRACE_POLICIES = frozenset(
    {
        _TRACE_POLICY_PARENT_BASED_ALWAYS_OFF,
        _TRACE_POLICY_PARENT_BASED_TRACE_ID_RATIO,
        _TRACE_POLICY_ALWAYS_OFF,
    }
)
_missing_otel_modules = object()
_missing_always_off_tracer = object()
_otel_modules: tuple[Any, Any, Any] | object | None = None
_always_off_tracer: Any | object | None = None
_runtime_tracing_configured = False
_runtime_tracer_provider: Any | None = None
_runtime_span_flusher: _BackgroundSpanFlusher | None = None
# Bounds each background flush so a stalled collector cannot wedge the flush thread.
_SPAN_FLUSH_TIMEOUT_MILLIS = 5000

_logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _TracingConfig:
    policy: str | None
    sample_rate: float | None
    otlp_endpoint: str
    service_name: str
    environment_id: str | None


def _load_tracing_config() -> _TracingConfig:
    """Read and normalize the tracing environment once for an invocation."""
    raw_policy = os.environ.get(_REMOTE_FUNCTION_TRACE_POLICY_ENV_VAR, "")
    policy = raw_policy.strip().lower()
    raw_rate = os.environ.get(_REMOTE_FUNCTION_TRACE_SAMPLE_RATE_ENV_VAR)
    sample_rate = None
    if raw_rate is not None:
        with contextlib.suppress(ValueError):
            sample_rate = float(raw_rate)
        if sample_rate is not None and (sample_rate < 0.0 or sample_rate > 1.0):
            sample_rate = None

    return _TracingConfig(
        policy=policy if policy in _TRACE_POLICIES else None,
        sample_rate=sample_rate,
        otlp_endpoint=os.environ.get("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
        or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", ""),
        service_name=os.environ.get("CHALK_SERVICE") or _TRACER_NAME,
        environment_id=os.environ.get("CHALK_ENVIRONMENT_ID") or None,
    )


class _BackgroundSpanFlusher:
    """Runs a tracer provider's ``force_flush`` on one daemon thread, off the request path.

    Function pods outlive invocations, so without a flush an invocation's ended spans wait
    for the batch processor's schedule delay before export. Requests coalesce: every request
    made before a flush starts is satisfied by that flush, while a request made after a flush
    starts schedules another, because spans ended after the flush began may have missed it.
    """

    def __init__(self, flush: Callable[[int], object], timeout_millis: int) -> None:
        super().__init__()
        self._flush = flush
        self._timeout_millis = timeout_millis
        self._cond = threading.Condition()
        # Monotonic counters: requests made, the request count covered by the latest flush to
        # start, and the request count covered by the latest flush to finish.
        self._requested = 0
        self._started = 0
        self._completed = 0
        self._thread: threading.Thread | None = None

    def request(self) -> None:
        with self._cond:
            self._requested += 1
            # is_alive (rather than None) also restarts the worker in a forked child.
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(
                    target=self._run,
                    name="chalk-remote-call-span-flush",
                    daemon=True,
                )
                self._thread.start()
            self._cond.notify_all()

    def wait_until_idle(self, timeout: float) -> bool:
        """Block until every request made so far is covered by a finished flush."""
        with self._cond:
            return self._cond.wait_for(lambda: self._completed >= self._requested, timeout)

    def _run(self) -> None:
        while True:
            with self._cond:
                self._cond.wait_for(lambda: self._started < self._requested)
                target = self._requested
                self._started = target
            try:
                if self._flush(self._timeout_millis) is False:
                    _logger.debug("Span flush did not finish within %d ms", self._timeout_millis)
            except Exception:
                _logger.warning("Span flush failed", exc_info=True)
            with self._cond:
                self._completed = target
                self._cond.notify_all()


def _request_span_flush() -> None:
    flusher = _runtime_span_flusher
    if flusher is None:
        return
    try:
        flusher.request()
    except Exception:
        # Flushing is best effort; it must never fail the invocation it follows.
        _logger.debug("Could not schedule span flush", exc_info=True)


def _raw_metadata(context_metadata: Any) -> Mapping[str, Any] | None:
    if not isinstance(context_metadata, Mapping):
        return None

    raw = context_metadata.get("metadata", context_metadata)
    if isinstance(raw, Mapping):
        return raw
    return None


def _collect_trace_metadata(
    context_metadata: Any,
) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None]:
    if isinstance(context_metadata, Mapping):
        first = _raw_metadata(context_metadata)
        if first is not None and first.get("traceparent"):
            return first, first
        return first, None

    first: Mapping[str, Any] | None = None
    if isinstance(context_metadata, Sequence) and not isinstance(context_metadata, str | bytes):
        for item in context_metadata:
            metadata = _raw_metadata(item)
            if metadata is None:
                continue

            if first is None:
                first = metadata
            if metadata.get("traceparent"):
                return first, metadata

    return first, None


def _runtime_resource_attributes(config: _TracingConfig) -> dict[str, str]:
    attributes = {"service.name": config.service_name}
    if config.environment_id:
        attributes["chalk.environment_id"] = config.environment_id
    return attributes


def _configure_runtime_tracing(config: _TracingConfig, sample_rate: float) -> None:
    global _runtime_tracing_configured, _runtime_tracer_provider, _runtime_span_flusher
    if _runtime_tracing_configured:
        return

    try:
        resources = importlib.import_module("opentelemetry.sdk.resources")
        sdk_trace = importlib.import_module("opentelemetry.sdk.trace")
        sdk_sampling = importlib.import_module("opentelemetry.sdk.trace.sampling")
        trace_api = importlib.import_module("opentelemetry.trace")
    except Exception:
        _runtime_tracing_configured = True
        return

    try:
        provider = sdk_trace.TracerProvider(
            resource=resources.Resource.create(_runtime_resource_attributes(config)),
            sampler=sdk_sampling.ParentBased(sdk_sampling.TraceIdRatioBased(sample_rate)),
        )

        if config.otlp_endpoint:
            try:
                otlp_exporter = importlib.import_module("opentelemetry.exporter.otlp.proto.grpc.trace_exporter")
                sdk_export = importlib.import_module("opentelemetry.sdk.trace.export")
                # gRPC otherwise derives an invalid HTTP/2 authority from the Unix socket path.
                channel_options = (
                    (("grpc.default_authority", "localhost"),) if config.otlp_endpoint.startswith("unix:") else None
                )
                exporter = otlp_exporter.OTLPSpanExporter(
                    endpoint=config.otlp_endpoint, channel_options=channel_options
                )
                provider.add_span_processor(sdk_export.BatchSpanProcessor(exporter))
                _runtime_span_flusher = _BackgroundSpanFlusher(provider.force_flush, _SPAN_FLUSH_TIMEOUT_MILLIS)
            except Exception:
                pass

        trace_api.set_tracer_provider(provider)
        _runtime_tracer_provider = provider
        atexit.register(provider.shutdown)
    except Exception:
        pass
    _runtime_tracing_configured = True


def _span_metadata(
    first_metadata: Mapping[str, Any] | None,
    traceparent_metadata: Mapping[str, Any] | None,
    config: _TracingConfig,
) -> tuple[Mapping[str, Any] | None, Any | None, Any]:
    if traceparent_metadata is not None:
        carrier = _trace_carrier(traceparent_metadata)
        if not carrier:
            return None, None, None

        otel_modules = _get_otel_modules()
        if otel_modules is None:
            return None, None, None
        _, propagate, trace = otel_modules

        parent_context = propagate.extract(carrier)
        parent_span_context = trace.get_current_span(parent_context).get_span_context()
        if not parent_span_context.is_valid:
            return None, None, None

        sample_rate = 0.0 if config.policy == _TRACE_POLICY_PARENT_BASED_ALWAYS_OFF else config.sample_rate
        if sample_rate is None:
            return None, None, None
        _configure_runtime_tracing(config, sample_rate)
        return traceparent_metadata, parent_context, otel_modules

    if config.policy != _TRACE_POLICY_PARENT_BASED_TRACE_ID_RATIO:
        return None, None, None

    sample_rate = config.sample_rate
    if sample_rate is None:
        return None, None, None

    _configure_runtime_tracing(config, sample_rate)
    otel_modules = _get_otel_modules()
    if otel_modules is None:
        return None, None, None
    return first_metadata, None, otel_modules


def _force_sampled_traceparent(metadata: Mapping[str, Any]) -> Mapping[str, Any]:
    parts = str(metadata.get("traceparent") or "").split("-")
    if len(parts) != 4 or len(parts[3]) != 2:
        return metadata
    try:
        parts[3] = f"{int(parts[3], 16) | 1:02x}"
    except ValueError:
        return metadata
    return {**metadata, "traceparent": "-".join(parts)}


def _always_off_span_metadata(
    first_metadata: Mapping[str, Any] | None,
    traceparent_metadata: Mapping[str, Any] | None,
) -> tuple[Mapping[str, Any] | None, Any | None, Any | None, Any | None]:
    otel_modules = _get_otel_modules()
    if otel_modules is None:
        return None, None, None, None
    _, propagate, trace = otel_modules

    parent_context = None
    if traceparent_metadata is not None:
        carrier = _trace_carrier(traceparent_metadata)
        if carrier:
            extracted_context = propagate.extract(carrier)
            parent_span_context = trace.get_current_span(extracted_context).get_span_context()
            if parent_span_context.is_valid:
                parent_context = extracted_context

    tracer = _get_always_off_tracer()
    if tracer is None:
        return None, None, None, None
    return traceparent_metadata or first_metadata, parent_context, otel_modules, tracer


def _trace_carrier(metadata: Mapping[str, Any]) -> dict[str, str]:
    return {
        str(key).lower(): str(value)
        for key, value in metadata.items()
        if str(key).lower() in _TRACE_CONTEXT_METADATA_KEYS and value
    }


def _function_name(context_metadata: Any) -> str:
    if isinstance(context_metadata, Mapping):
        return str(context_metadata.get("function_name") or "") or "unknown"

    if isinstance(context_metadata, Sequence) and not isinstance(context_metadata, str | bytes):
        for item in context_metadata:
            if isinstance(item, Mapping):
                function_name = str(item.get("function_name") or "")
                if function_name:
                    return function_name

    return "unknown"


def _get_tracer(trace_api: Any) -> Any:
    return trace_api.get_tracer(_TRACER_NAME)


def _get_otel_modules() -> tuple[Any, Any, Any] | None:
    global _otel_modules
    if _otel_modules is None:
        try:
            _otel_modules = (
                importlib.import_module("opentelemetry.context"),
                importlib.import_module("opentelemetry.propagate"),
                importlib.import_module("opentelemetry.trace"),
            )
        except ImportError:
            _otel_modules = _missing_otel_modules

    if _otel_modules is _missing_otel_modules:
        return None
    return cast(tuple[Any, Any, Any], _otel_modules)


def _get_always_off_tracer() -> Any | None:
    global _always_off_tracer
    if _always_off_tracer is None:
        try:
            sdk_trace = importlib.import_module("opentelemetry.sdk.trace")
            sdk_sampling = importlib.import_module("opentelemetry.sdk.trace.sampling")
        except ImportError:
            _always_off_tracer = _missing_always_off_tracer
        else:
            # Keep always-off local to this invocation instead of replacing the
            # process-wide tracer provider.
            provider = sdk_trace.TracerProvider(sampler=sdk_sampling.ALWAYS_OFF)
            _always_off_tracer = provider.get_tracer(_TRACER_NAME)

    if _always_off_tracer is _missing_always_off_tracer:
        return None
    return _always_off_tracer


@contextlib.contextmanager
def remote_function_invocation_span(
    context_metadata: Any,
    coalesced_count: int | None = None,
) -> Iterator[None]:
    config = _load_tracing_config()
    first_metadata, traceparent_metadata = _collect_trace_metadata(context_metadata)
    override = str((first_metadata or {}).get(_REMOTE_FUNCTION_TRACE_OVERRIDE_KEY) or "").strip().lower()
    if override == _TRACE_OVERRIDE_ON:
        config = replace(config, policy=_TRACE_POLICY_PARENT_BASED_TRACE_ID_RATIO, sample_rate=1.0)
    elif override == _TRACE_OVERRIDE_OFF:
        config = replace(config, policy=_TRACE_POLICY_ALWAYS_OFF)
    if config.policy is None:
        yield
        return

    force_trace = override == _TRACE_OVERRIDE_ON
    if force_trace and traceparent_metadata is not None:
        traceparent_metadata = _force_sampled_traceparent(traceparent_metadata)
    if config.policy == _TRACE_POLICY_PARENT_BASED_ALWAYS_OFF and traceparent_metadata is None:
        yield
        return

    if config.policy == _TRACE_POLICY_ALWAYS_OFF:
        _metadata, parent_context, otel_modules, tracer = _always_off_span_metadata(
            first_metadata,
            traceparent_metadata,
        )
    else:
        _metadata, parent_context, otel_modules = _span_metadata(
            first_metadata,
            traceparent_metadata,
            config,
        )
        tracer = _get_tracer(otel_modules[2]) if otel_modules is not None else None

    if otel_modules is None:
        yield
        return
    if tracer is None:
        yield
        return
    otel_context, _, trace = otel_modules

    SpanKind = trace.SpanKind
    Status = trace.Status
    StatusCode = trace.StatusCode
    function_name = _function_name(context_metadata)
    span_kwargs: dict[str, Any] = {"kind": SpanKind.SERVER}
    if parent_context is not None:
        span_kwargs["context"] = parent_context

    # The always-off tracer exports nothing, so only runtime-provider spans need a flush.
    flush_after = config.policy != _TRACE_POLICY_ALWAYS_OFF
    try:
        with tracer.start_as_current_span("chalkcompute.remote_function.invoke", **span_kwargs) as span:
            span.set_attribute("chalk.remote_function.name", function_name)
            if coalesced_count is not None:
                span.set_attribute(
                    "chalk.remote_function.coalesced_count",
                    coalesced_count,
                )
            if parent_context is not None and not span.get_span_context().is_valid:
                token = otel_context.attach(parent_context)
                try:
                    yield
                finally:
                    otel_context.detach(token)
                return
            try:
                yield
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR, str(exc)))
                raise
    finally:
        # Runs after the invocation span (and any span the handler opened inside it) has
        # ended, so the flush it schedules covers this invocation's spans.
        if flush_after:
            _request_span_flush()
