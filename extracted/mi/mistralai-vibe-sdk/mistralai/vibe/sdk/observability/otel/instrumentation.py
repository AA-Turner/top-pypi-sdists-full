"""Optional OpenTelemetry facade used by SDK-owned instrumentation."""

import traceback
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from importlib import import_module
from typing import Any, cast


class StatusCode:
    UNSET = "UNSET"
    ERROR = "ERROR"


class Status:
    def __init__(
        self, status_code: object = StatusCode.UNSET, description: str | None = None
    ) -> None:
        self.status_code = status_code
        self.description = description


class Span:
    def is_recording(self) -> bool:
        return False

    def add_event(
        self,
        name: str,
        attributes: Mapping[str, object] | None = None,
    ) -> None:
        pass

    def record_exception(self, exception: Exception) -> None:
        pass

    def set_attribute(self, key: str, value: object) -> None:
        pass

    def set_attributes(self, attributes: Mapping[str, object]) -> None:
        pass

    def set_status(
        self,
        status: Status | StatusCode,
        description: str | None = None,
    ) -> None:
        pass

    def end(self) -> None:
        pass


class _NoopTracer:
    def start_span(
        self,
        name: str,
        **kwargs: Any,
    ) -> Span:
        return _NOOP_SPAN

    @contextmanager
    def start_as_current_span(
        self,
        name: str,
        **kwargs: Any,
    ) -> Iterator[Span]:
        yield _NOOP_SPAN


class _NoopTrace:
    def get_tracer(self, name: str) -> _NoopTracer:
        return _NoopTracer()

    def get_current_span(self) -> Span:
        return _NOOP_SPAN


_NOOP_SPAN = Span()
trace: Any = _NoopTrace()

try:
    _otel_trace = import_module("opentelemetry.trace")
except ModuleNotFoundError as exc:
    if exc.name is not None and not exc.name.startswith("opentelemetry"):
        raise
else:
    trace = _otel_trace
    Span = _otel_trace.Span  # type: ignore[misc]
    Status = _otel_trace.Status  # type: ignore[misc]
    StatusCode = _otel_trace.StatusCode  # type: ignore[misc]

type SpanAttribute = str | bool | int | float

TRACER_NAME = "mistralai.vibe.sdk"
SDK_ATTRIBUTE_PREFIX = "vibe.sdk."
_OTEL_STANDARD_ATTRIBUTE_PREFIXES = (
    "client.",
    "db.",
    "error.",
    "exception.",
    "gen_ai.",
    "http.",
    "network.",
    "process.",
    "server.",
    "service.",
    "telemetry.",
    "url.",
)
_tracer_provider: Any | None = None
_mistral_client_tracer_provider: Any | None = None
_UNSET: Any = object()


def configure_tracing(
    *,
    tracer_provider: object | None = _UNSET,
    mistral_client_tracer_provider: object | None = _UNSET,
) -> None:
    """Register host-owned OpenTelemetry providers for SDK instrumentation.

    The SDK never installs these providers globally. ``tracer_provider`` is used
    for SDK-owned spans, while ``mistral_client_tracer_provider`` is attached to
    internally-created Mistral clients so GenAI spans can use a separate export
    path. Omitted keyword arguments keep their current registration. Passing
    ``None`` clears that registration. Calling with no arguments is a no-op.
    """
    global _tracer_provider, _mistral_client_tracer_provider

    if tracer_provider is not _UNSET:
        _tracer_provider = tracer_provider
    if mistral_client_tracer_provider is not _UNSET:
        _mistral_client_tracer_provider = mistral_client_tracer_provider


def get_tracer() -> Any:
    """Return the SDK tracer from the registered provider or global fallback."""
    if _tracer_provider is not None:
        return _tracer_provider.get_tracer(TRACER_NAME)
    return trace.get_tracer(TRACER_NAME)


def configure_mistral_client_telemetry(client: Any) -> Any:
    """Attach the configured Mistral-client tracer provider, if any."""
    if _mistral_client_tracer_provider is None:
        return client

    try:
        from mistralai.extra.observability import configure_telemetry

        configure_telemetry(
            client,
            provider=_mistral_client_tracer_provider,
            # Vibe still redacts spans before export; redaction is installed on
            # host-owned exporters so each telemetry destination can choose its
            # own policy. Disable the Mistral SDK client wrapper's extra
            # creation-time redaction to avoid a misleading setup warning here.
            redaction=False,
        )
    except Exception as exc:
        raise RuntimeError("Cannot configure Mistral client telemetry") from exc

    return client


def otel_attributes(attributes: Mapping[str, object]) -> dict[str, SpanAttribute]:
    """Return SDK-prefixed attributes normalized for OpenTelemetry span creation."""
    prefixed_attributes = _prefix_sdk_attributes(attributes)
    otel_compatible_attributes: dict[str, SpanAttribute] = {}
    for key, value in prefixed_attributes.items():
        if isinstance(value, str | bool | int | float):
            otel_compatible_attributes[key] = value
            continue
        otel_compatible_attributes[key] = str(value)
    return otel_compatible_attributes


def _prefix_sdk_attributes(attributes: Mapping[str, object]) -> dict[str, object]:
    prefixed: dict[str, object] = {}
    for key, value in attributes.items():
        if value is None:
            continue
        prefixed[_attribute_key(key)] = value
    return prefixed


def _attribute_key(key: str) -> str:
    if key.startswith(SDK_ATTRIBUTE_PREFIX):
        return key
    if key.startswith(_OTEL_STANDARD_ATTRIBUTE_PREFIXES):
        return key
    return f"{SDK_ATTRIBUTE_PREFIX}{key}"


def add_event(
    span: Span,
    name: str,
    *,
    priority: str,
    attributes: Mapping[str, object] | None = None,
) -> None:
    span.add_event(
        name,
        attributes=otel_attributes(
            {
                "priority": priority,
                **(attributes or {}),
            }
        ),
    )


@contextmanager
def start_span(
    name: str,
    attributes: Mapping[str, object] | None = None,
    **span_kwargs: Any,
) -> Iterator[Span]:
    """Start an SDK span with configured attributes and consistent exception status."""
    with get_tracer().start_as_current_span(
        name,
        attributes=otel_attributes(attributes or {}),
        record_exception=False,
        set_status_on_exception=False,
        **span_kwargs,
    ) as span:
        try:
            yield span
        except Exception as exc:
            record_exception(span, exc)
            raise


def current_span() -> Span:
    return cast(Span, trace.get_current_span())


def span_context(span: Span | None) -> object | None:
    if span is None:
        return None
    set_span_in_context = getattr(trace, "set_span_in_context", None)
    if set_span_in_context is None:
        return None
    return cast(object | None, set_span_in_context(span))


def record_exception(span: Span, exc: Exception) -> None:
    span.set_status(Status(StatusCode.ERROR))
    span.set_attributes(
        otel_attributes(
            {
                "status": "failed",
                "error.type": _exception_type(exc),
            }
        )
    )
    span.add_event(
        "exception",
        attributes=otel_attributes(
            {
                "exception.type": _exception_type(exc),
                "exception.message": str(exc),
                "exception.stacktrace": "".join(
                    traceback.format_exception(type(exc), exc, exc.__traceback__)
                ),
            }
        ),
    )


def _exception_type(exc: Exception) -> str:
    exc_type = type(exc)
    if exc_type.__module__ == "builtins":
        return exc_type.__qualname__
    return f"{exc_type.__module__}.{exc_type.__qualname__}"
