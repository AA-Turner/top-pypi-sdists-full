from unittest.mock import MagicMock

import pytest
from mistralai.extra.observability import DEFAULT_REDACTED_VALUE, RedactingSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from mistralai.workflows import client as client_module
from mistralai.workflows.core.config.config import OtelRedactionMode
from mistralai.workflows.core.tracing._otel_config import _apply_span_redaction

_SENSITIVE_KEY = "gen_ai.input.messages"
_SAFE_KEY = "gen_ai.request.model"
_SECRET = "Bearer sk-abcdefghijklmnopqrstuvwx"


def _export_span_through(mode: OtelRedactionMode) -> dict[str, object]:
    memory = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(_apply_span_redaction(memory, mode)))

    tracer = provider.get_tracer(__name__)
    span = tracer.start_span("chat")
    span.set_attribute(_SENSITIVE_KEY, f"question {_SECRET}")
    span.set_attribute(_SAFE_KEY, "mistral-large")
    span.end()
    provider.force_flush()

    finished = memory.get_finished_spans()
    assert len(finished) == 1
    return dict(finished[0].attributes or {})


class TestApplySpanRedaction:
    def test_none_returns_exporter_unwrapped(self) -> None:
        exporter = InMemorySpanExporter()
        assert _apply_span_redaction(exporter, OtelRedactionMode.NONE) is exporter

    @pytest.mark.parametrize("mode", [OtelRedactionMode.DEFAULT, OtelRedactionMode.STRICT])
    def test_non_none_wraps_with_redacting_exporter(self, mode: OtelRedactionMode) -> None:
        wrapped = _apply_span_redaction(InMemorySpanExporter(), mode)
        assert isinstance(wrapped, RedactingSpanExporter)


class TestRedactionBehavior:
    def test_none_leaves_attributes_intact(self) -> None:
        attributes = _export_span_through(OtelRedactionMode.NONE)
        assert attributes[_SENSITIVE_KEY] == f"question {_SECRET}"
        assert attributes[_SAFE_KEY] == "mistral-large"

    def test_default_scrubs_secret_but_keeps_key_and_structure(self) -> None:
        attributes = _export_span_through(OtelRedactionMode.DEFAULT)
        # Content-oriented policy: the matched secret substring is masked in place,
        # the surrounding text survives, and safe attributes are untouched.
        assert attributes[_SENSITIVE_KEY] == f"question {DEFAULT_REDACTED_VALUE}"
        assert attributes[_SAFE_KEY] == "mistral-large"

    def test_strict_drops_whole_sensitive_value(self) -> None:
        attributes = _export_span_through(OtelRedactionMode.STRICT)
        # Key-oriented policy: sensitive-keyed values are replaced wholesale, while
        # a known-safe attribute is preserved.
        assert attributes[_SENSITIVE_KEY] == DEFAULT_REDACTED_VALUE
        assert attributes[_SAFE_KEY] == "mistral-large"


class TestClientTelemetryConfiguration:
    def test_configures_global_provider_without_redaction_when_otel_enabled(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        recorded = MagicMock()
        monkeypatch.setattr(client_module, "configure_telemetry", recorded)
        monkeypatch.setattr(client_module.config.common, "otel_enabled", True)

        client = MagicMock()
        client_module._configure_client_telemetry(client)

        recorded.assert_called_once_with(client, provider="global", redaction=False)

    def test_noop_when_otel_disabled(self, monkeypatch: pytest.MonkeyPatch) -> None:
        recorded = MagicMock()
        monkeypatch.setattr(client_module, "configure_telemetry", recorded)
        monkeypatch.setattr(client_module.config.common, "otel_enabled", False)

        client_module._configure_client_telemetry(MagicMock())

        recorded.assert_not_called()

    def test_telemetry_failure_does_not_propagate(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _boom(*_args: object, **_kwargs: object) -> None:
            raise ValueError("no hooks")

        monkeypatch.setattr(client_module, "configure_telemetry", _boom)
        monkeypatch.setattr(client_module.config.common, "otel_enabled", True)

        client_module._configure_client_telemetry(MagicMock())
