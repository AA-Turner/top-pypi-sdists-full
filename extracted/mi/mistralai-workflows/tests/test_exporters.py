"""Parity tests for the public OTLP exporter factory (tracing/exporters.py).

These lock down the behavior external hosts rely on: endpoint resolution per signal, the
Mistral service-account bearer attached only on the default endpoint, CUMULATIVE metric
temporality, None when a signal is disabled or unconfigured, and the config precedence in
``resolve_otlp_export_options`` (deprecated ``otel_endpoint`` vs per-signal override vs default).
"""

from types import SimpleNamespace
from typing import Any

import pytest
import structlog
from pydantic import SecretStr

from mistralai.workflows.core.auth import StaticTokenProvider
from mistralai.workflows.core.tracing import exporters
from mistralai.workflows.core.tracing.exporters import (
    OtelExportOptions,
    build_otlp_log_exporter,
    build_otlp_metric_exporter,
    build_otlp_span_exporter,
)


class _RecordingExporter(exporters._OTLPExporterBase):
    """Stand-in for an OTLP exporter: records the kwargs ``build`` constructs it with."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.kwargs = kwargs
        exporters._OTLPExporterBase.__init__(
            self,
            status_recorder=kwargs.get("status_recorder"),
            token_provider=kwargs.get("token_provider"),
        )


def _bearer_of(exporter: _RecordingExporter) -> str | None:
    """Run the injected session's auth against a dummy request and return the Authorization header."""
    auth = exporter.kwargs["session"].auth
    if auth is None:
        return None
    request = SimpleNamespace(headers={})
    auth(request)
    return request.headers.get("Authorization")


@pytest.fixture
def recording_exporters(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("_LoggingOTLPSpanExporter", "_LoggingOTLPMetricExporter", "_LoggingOTLPLogExporter"):
        monkeypatch.setattr(exporters, name, _RecordingExporter)


class TestBuilders:
    def test_span_builder_resolves_endpoint_and_attaches_bearer_on_default(self, recording_exporters: None) -> None:
        exporter = build_otlp_span_exporter(
            OtelExportOptions(endpoint="http://api.test/telemetry"), StaticTokenProvider("tok")
        )

        assert isinstance(exporter, _RecordingExporter)
        assert exporter.kwargs["endpoint"] == "http://api.test/telemetry/v1/traces"
        assert _bearer_of(exporter) == "Bearer tok"

    def test_metric_builder_resolves_endpoint_and_bakes_cumulative_temporality(self, recording_exporters: None) -> None:
        from opentelemetry.sdk.metrics.export import AggregationTemporality

        exporter = build_otlp_metric_exporter(
            OtelExportOptions(endpoint="http://api.test/telemetry"), StaticTokenProvider("tok")
        )

        assert isinstance(exporter, _RecordingExporter)
        assert exporter.kwargs["endpoint"] == "http://api.test/telemetry/v1/metrics"
        assert set(exporter.kwargs["preferred_temporality"].values()) == {AggregationTemporality.CUMULATIVE}

    def test_log_builder_resolves_endpoint(self, recording_exporters: None) -> None:
        exporter = build_otlp_log_exporter(OtelExportOptions(endpoint="http://api.test/telemetry"))

        assert isinstance(exporter, _RecordingExporter)
        assert exporter.kwargs["endpoint"] == "http://api.test/telemetry/v1/logs"

    def test_no_bearer_when_use_api_key_false(self, recording_exporters: None) -> None:
        # An explicit override brings its own auth via OTEL env vars; the builder attaches none.
        exporter = build_otlp_span_exporter(
            OtelExportOptions(endpoint="http://custom:4318", use_api_key=False), StaticTokenProvider("tok")
        )

        assert isinstance(exporter, _RecordingExporter)
        assert _bearer_of(exporter) is None

    @pytest.mark.parametrize(
        "options", [OtelExportOptions(endpoint=None), OtelExportOptions(endpoint="x", enabled=False)]
    )
    def test_builders_return_none_when_disabled_or_unconfigured(
        self, recording_exporters: None, options: OtelExportOptions
    ) -> None:
        assert build_otlp_span_exporter(options, StaticTokenProvider("tok")) is None
        assert build_otlp_metric_exporter(options, StaticTokenProvider("tok")) is None
        assert build_otlp_log_exporter(options, StaticTokenProvider("tok")) is None


def _resolve(
    monkeypatch: pytest.MonkeyPatch,
    env: dict[str, str],
    *,
    server_url: str | None = "http://api.test",
    api_key: SecretStr | None = SecretStr("client-key"),
) -> exporters.ResolvedOtlpExports:
    """Drive resolve_otlp_export_options from env vars with an injected config and token provider."""
    from mistralai.workflows.core.config.config import AppConfig

    monkeypatch.setenv("OTEL_ENABLED", "true")
    for key in ("OTEL_ENDPOINT", "OTEL_TRACES_ENDPOINT", "OTEL_METRICS_ENDPOINT", "OTEL_LOGS_ENDPOINT"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    fresh_config = AppConfig()
    # Inject directly to avoid the env/dotenv conflict detector on the key fields.
    monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_api_key", api_key)
    monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_server_url", server_url)
    monkeypatch.setattr(exporters, "config", fresh_config)
    monkeypatch.setattr(
        exporters,
        "get_token_provider",
        lambda explicit=None: StaticTokenProvider(explicit.get_secret_value()) if explicit else None,
    )
    return exporters.resolve_otlp_export_options()


class TestResolveOtlpExportOptions:
    def test_default_endpoint_authenticates_every_signal(self, monkeypatch: pytest.MonkeyPatch) -> None:
        resolution = _resolve(monkeypatch, {})

        for options in (resolution.trace, resolution.metric, resolution.log):
            assert options.endpoint == "http://api.test/telemetry"
            assert options.use_api_key is True
            assert options.enabled is True
        assert resolution.token_provider is not None
        assert resolution.token_provider.get_token() == "client-key"

    def test_deprecated_otel_endpoint_applies_to_all_signals_without_auth(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        with structlog.testing.capture_logs() as captured:
            resolution = _resolve(monkeypatch, {"OTEL_ENDPOINT": "http://deprecated:4318"})

        for options in (resolution.trace, resolution.metric, resolution.log):
            assert options.endpoint == "http://deprecated:4318"
            assert options.use_api_key is False
        assert resolution.token_provider is None
        assert any("otel_endpoint is deprecated" in entry.get("event", "") for entry in captured)

    def test_per_signal_override_replaces_only_that_signal(self, monkeypatch: pytest.MonkeyPatch) -> None:
        resolution = _resolve(monkeypatch, {"OTEL_TRACES_ENDPOINT": "http://custom-traces:4318"})

        assert resolution.trace.endpoint == "http://custom-traces:4318"
        assert resolution.trace.use_api_key is False
        assert resolution.metric.endpoint == "http://api.test/telemetry"
        assert resolution.metric.use_api_key is True
        assert resolution.log.endpoint == "http://api.test/telemetry"
        assert resolution.token_provider is not None

    def test_per_signal_toggle_disables_only_that_signal(self, monkeypatch: pytest.MonkeyPatch) -> None:
        resolution = _resolve(monkeypatch, {"MISTRAL_WORKFLOWS_OTEL_LOGS_EXPORT": "false"})

        assert resolution.log.enabled is False
        assert resolution.trace.enabled is True
        assert resolution.metric.enabled is True

    def test_no_server_url_and_no_override_yields_no_endpoint(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Assert-free: callers skip exporters whose endpoint is None instead of crashing.
        resolution = _resolve(monkeypatch, {}, server_url=None)

        assert resolution.trace.endpoint is None
        assert resolution.metric.endpoint is None
        assert resolution.log.endpoint is None
        assert resolution.token_provider is None
