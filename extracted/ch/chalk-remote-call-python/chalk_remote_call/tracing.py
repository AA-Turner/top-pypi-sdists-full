from __future__ import annotations

import atexit
import contextlib
import importlib
import os
from collections.abc import Iterator, Mapping, Sequence
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


def _trace_policy() -> str | None:
    raw_policy = os.environ.get(_REMOTE_FUNCTION_TRACE_POLICY_ENV_VAR)
    if raw_policy is None:
        return None

    policy = raw_policy.strip().lower()
    if policy in _TRACE_POLICIES:
        return policy
    return None


def _trace_sample_rate(force_trace: bool) -> float | None:
    if force_trace:
        return 1.0
    raw_rate = os.environ.get(_REMOTE_FUNCTION_TRACE_SAMPLE_RATE_ENV_VAR)
    if raw_rate is None:
        return None

    try:
        rate = float(raw_rate)
    except ValueError:
        return None

    if rate < 0.0 or rate > 1.0:
        return None
    return rate


def _otel_exporter_configured() -> bool:
    return bool(os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT") or os.environ.get("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"))


def _runtime_resource_attributes() -> dict[str, str]:
    attributes = {"service.name": os.environ.get("CHALK_SERVICE") or _TRACER_NAME}
    if environment_id := os.environ.get("CHALK_ENVIRONMENT_ID"):
        attributes["chalk.environment_id"] = environment_id
    return attributes


def _configure_runtime_tracing(sample_rate: float) -> None:
    global _runtime_tracing_configured, _runtime_tracer_provider
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
            resource=resources.Resource.create(_runtime_resource_attributes()),
            sampler=sdk_sampling.ParentBased(sdk_sampling.TraceIdRatioBased(sample_rate)),
        )

        if _otel_exporter_configured():
            try:
                otlp_exporter = importlib.import_module("opentelemetry.exporter.otlp.proto.grpc.trace_exporter")
                sdk_export = importlib.import_module("opentelemetry.sdk.trace.export")
                provider.add_span_processor(sdk_export.BatchSpanProcessor(otlp_exporter.OTLPSpanExporter()))
            except Exception:
                pass

        trace_api.set_tracer_provider(provider)
        _runtime_tracer_provider = provider
        atexit.register(provider.shutdown)
    except Exception:
        pass
    _runtime_tracing_configured = True


def _sample_rate_for_inherited_parent(policy: str, force_trace: bool) -> float | None:
    if policy == _TRACE_POLICY_PARENT_BASED_ALWAYS_OFF:
        return 0.0
    if policy == _TRACE_POLICY_PARENT_BASED_TRACE_ID_RATIO:
        return _trace_sample_rate(force_trace)
    return None


def _span_metadata(
    first_metadata: Mapping[str, Any] | None,
    traceparent_metadata: Mapping[str, Any] | None,
    policy: str,
    force_trace: bool,
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

        sample_rate = _sample_rate_for_inherited_parent(policy, force_trace)
        if sample_rate is None:
            return None, None, None
        _configure_runtime_tracing(sample_rate)
        return traceparent_metadata, parent_context, otel_modules

    if policy != _TRACE_POLICY_PARENT_BASED_TRACE_ID_RATIO:
        return None, None, None

    sample_rate = _trace_sample_rate(force_trace)
    if sample_rate is None:
        return None, None, None

    _configure_runtime_tracing(sample_rate)
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
    first_metadata, traceparent_metadata = _collect_trace_metadata(context_metadata)
    override = str((first_metadata or {}).get(_REMOTE_FUNCTION_TRACE_OVERRIDE_KEY) or "").strip().lower()
    if override == _TRACE_OVERRIDE_ON:
        policy = _TRACE_POLICY_PARENT_BASED_TRACE_ID_RATIO
    elif override == _TRACE_OVERRIDE_OFF:
        policy = _TRACE_POLICY_ALWAYS_OFF
    else:
        policy = _trace_policy()
    if policy is None:
        yield
        return

    force_trace = override == _TRACE_OVERRIDE_ON
    if force_trace and traceparent_metadata is not None:
        traceparent_metadata = _force_sampled_traceparent(traceparent_metadata)
    if policy == _TRACE_POLICY_PARENT_BASED_ALWAYS_OFF and traceparent_metadata is None:
        yield
        return

    if policy == _TRACE_POLICY_ALWAYS_OFF:
        _metadata, parent_context, otel_modules, tracer = _always_off_span_metadata(
            first_metadata,
            traceparent_metadata,
        )
    else:
        _metadata, parent_context, otel_modules = _span_metadata(
            first_metadata,
            traceparent_metadata,
            policy,
            force_trace,
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
