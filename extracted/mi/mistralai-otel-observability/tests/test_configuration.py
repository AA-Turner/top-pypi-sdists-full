"""Configuration helper tests."""

import pytest
from opentelemetry import trace
from opentelemetry.context import Context
from opentelemetry.sdk.trace import ReadableSpan, Span, SpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.sampling import ALWAYS_ON

from mistralai.observability.otel import ObservabilityConfig, observability
from mistralai.observability.otel.sdk import require_configured


def test_mistral_helper_configures_telemetry_endpoint_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """The Mistral helper should read authentication from the environment."""
    monkeypatch.setenv("MISTRAL_API_KEY", "test-key")
    observability.configure_mistral(service_name="agent-service", service_version="1.2.3")
    configured = require_configured()
    try:
        assert configured.config.service_name == "agent-service"
        assert configured.config.service_version == "1.2.3"
        assert configured.config.endpoint == "https://api.mistral.ai/telemetry"
        assert configured.config.protocol == "http/protobuf"
        assert configured.config.headers == {"Authorization": "Bearer test-key"}
    finally:
        observability.shutdown()


def test_mistral_helper_accepts_explicit_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Explicit Mistral auth should override environment lookup."""
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    observability.configure_mistral(
        service_name="agent-service",
        api_key="explicit-key",
        endpoint="https://example.test/telemetry",
    )
    configured = require_configured()
    try:
        assert configured.config.endpoint == "https://example.test/telemetry"
        assert configured.config.headers == {"Authorization": "Bearer explicit-key"}
    finally:
        observability.shutdown()


def test_mistral_helper_requires_authentication(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mistral configuration should fail without any authentication source."""
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    with pytest.raises(ValueError, match="MISTRAL_API_KEY"):
        observability.configure_mistral(service_name="agent-service")


class _StampingSpanProcessor(SpanProcessor):
    """Span processor that enriches every span at start."""

    def on_start(self, span: Span, parent_context: Context | None = None) -> None:
        del parent_context
        span.set_attribute("test.stamped", "yes")

    def on_end(self, span: ReadableSpan) -> None:
        del span

    def shutdown(self) -> None:
        return None

    def force_flush(self, timeout_millis: int = 30_000) -> bool:
        del timeout_millis
        return True


def test_configure_attaches_extra_span_processors() -> None:
    """Extra span processors run against spans exported by the owned provider."""
    exporter = InMemorySpanExporter()
    observability.configure(
        ObservabilityConfig(service_name="test-service"),
        span_exporter=exporter,
        span_processors=(_StampingSpanProcessor(),),
    )
    try:
        with observability.agent("agent"):
            pass
        observability.flush()
        spans = exporter.get_finished_spans()
        assert len(spans) == 1
        attributes = spans[0].attributes or {}
        assert attributes["test.stamped"] == "yes"
    finally:
        observability.shutdown()


def test_configured_sampler_records_children_of_an_unsampled_parent() -> None:
    """An explicit always-on sampler records spans whose remote parent was not sampled."""
    exporter = InMemorySpanExporter()
    observability.configure(
        ObservabilityConfig(service_name="test-service", sampler=ALWAYS_ON),
        span_exporter=exporter,
    )
    try:
        context = trace.set_span_in_context(
            trace.NonRecordingSpan(
                trace.SpanContext(
                    trace_id=int("a" * 32, 16),
                    span_id=int("b" * 16, 16),
                    is_remote=True,
                    trace_flags=trace.TraceFlags(trace.TraceFlags.DEFAULT),
                )
            )
        )
        with observability.agent("agent", context=context):
            pass
        observability.flush()
        spans = exporter.get_finished_spans()
        assert len(spans) == 1
        assert spans[0].context is not None
        assert spans[0].context.trace_id == int("a" * 32, 16)
    finally:
        observability.shutdown()


def test_default_sampler_drops_children_of_an_unsampled_parent() -> None:
    """Without a configured sampler the provider stays parent-based."""
    exporter = InMemorySpanExporter()
    observability.configure(ObservabilityConfig(service_name="test-service"), span_exporter=exporter)
    try:
        context = trace.set_span_in_context(
            trace.NonRecordingSpan(
                trace.SpanContext(
                    trace_id=int("a" * 32, 16),
                    span_id=int("b" * 16, 16),
                    is_remote=True,
                    trace_flags=trace.TraceFlags(trace.TraceFlags.DEFAULT),
                )
            )
        )
        with observability.agent("agent", context=context):
            pass
        observability.flush()
        assert exporter.get_finished_spans() == ()
    finally:
        observability.shutdown()
