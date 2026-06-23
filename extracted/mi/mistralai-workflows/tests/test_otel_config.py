import logging
from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr

from mistralai.workflows._version import __version__
from mistralai.workflows.core.tracing import _otel_config
from mistralai.workflows.core.tracing._otel_config import (
    TELEMETRY_DISTRO_NAME_ATTRIBUTE,
    TELEMETRY_DISTRO_VERSION_ATTRIBUTE,
    WORKFLOWS_TELEMETRY_DISTRO_NAME,
    _create_resource,
)


def test_workflows_telemetry_distro_resource_attributes_are_stable() -> None:
    resource = _create_resource(
        service_name="custom-worker-service",
        service_version="1.2.3",
        component="worker",
    )

    assert resource.attributes["service.name"] == "custom-worker-service"
    # This stable distro name is the collector routing key for dual-shipping Workflows telemetry.
    # If it changes, Alloy will stop receiving Workflows telemetry (Dora backend will still receive them).
    assert resource.attributes[TELEMETRY_DISTRO_NAME_ATTRIBUTE] == WORKFLOWS_TELEMETRY_DISTRO_NAME
    assert resource.attributes[TELEMETRY_DISTRO_VERSION_ATTRIBUTE] == __version__
    assert resource.attributes["component.type"] == "worker"


def test_workflows_telemetry_distro_resource_attributes_are_set_for_local_export() -> None:
    resource = _create_resource(service_name="custom-worker-service", service_version="1.2.3")

    assert resource.attributes[TELEMETRY_DISTRO_NAME_ATTRIBUTE] == WORKFLOWS_TELEMETRY_DISTRO_NAME
    assert resource.attributes[TELEMETRY_DISTRO_VERSION_ATTRIBUTE] == __version__
    assert "component.type" not in resource.attributes


@pytest.fixture
def exporter_calls(monkeypatch: pytest.MonkeyPatch) -> Iterator[dict[str, list[dict[str, Any]]]]:
    """Record OTLP exporter construction without building real SDK providers or sockets.

    Each OTLP exporter is replaced with a recorder capturing its kwargs (endpoint/headers);
    the providers, batch processors, reader, and log handler are stubbed so config_otel runs
    end-to-end without global side effects. Root logger handlers are restored on teardown.
    """
    calls: dict[str, list[dict[str, Any]]] = {"span": [], "metric": [], "log": []}

    def recorder(bucket: str) -> Any:
        def _factory(*_args: Any, **kwargs: Any) -> MagicMock:
            calls[bucket].append(kwargs)
            return MagicMock()

        return _factory

    monkeypatch.setattr(_otel_config, "OTLPSpanExporter", recorder("span"))
    monkeypatch.setattr(_otel_config, "OTLPMetricExporter", recorder("metric"))
    monkeypatch.setattr(_otel_config, "OTLPLogExporter", recorder("log"))
    for name in (
        "BatchSpanProcessor",
        "BatchLogRecordProcessor",
        "PeriodicExportingMetricReader",
        "TracerProvider",
        "MeterProvider",
        "LoggerProvider",
    ):
        monkeypatch.setattr(_otel_config, name, lambda *a, **k: MagicMock())
    # Real handler (not a MagicMock) so the root logger can compare levels when config_otel logs.
    monkeypatch.setattr(_otel_config, "LoggingHandler", lambda *a, **k: logging.NullHandler())

    root = logging.getLogger()
    original_handlers = list(root.handlers)
    yield calls
    root.handlers[:] = original_handlers


def _init_tracing_from_env(monkeypatch: pytest.MonkeyPatch, env: dict[str, str]) -> None:
    """Drive the full chain: env vars -> AppConfig -> init_tracing -> config_otel -> OTLP exporters."""
    from mistralai.workflows.core.config.config import AppConfig
    from mistralai.workflows.core.tracing import init_tracing

    monkeypatch.setenv("OTEL_ENABLED", "true")
    monkeypatch.setenv("OTEL_LOCAL", "false")
    monkeypatch.delenv("OTEL_ENDPOINT", raising=False)
    monkeypatch.delenv("OTEL_TRACES_ENDPOINT", raising=False)
    monkeypatch.delenv("OTEL_LOGS_ENDPOINT", raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    fresh_config = AppConfig()
    # Inject the API key directly (avoids the env/dotenv conflict detector on the key fields).
    monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_api_key", SecretStr("test-key"))
    if fresh_config.worker.agent.mistral_client_server_url is None:
        monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_server_url", "http://api.test")

    monkeypatch.setattr(init_tracing, "config", fresh_config)
    monkeypatch.setattr(init_tracing, "AsyncioInstrumentor", lambda: MagicMock())
    monkeypatch.setattr(init_tracing, "HTTPXClientInstrumentor", lambda: MagicMock())
    if init_tracing._HAS_AIOHTTP_INSTRUMENTATION:
        monkeypatch.setattr(init_tracing, "AioHttpClientInstrumentor", lambda: MagicMock())

    init_tracing.init_tracing("worker")


class TestIndependentExportToggles:
    def test_traces_disabled_skips_only_span_exporter(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[dict[str, Any]]]
    ) -> None:
        _init_tracing_from_env(monkeypatch, {"MISTRAL_WORKFLOWS_OTEL_TRACES_EXPORT": "false"})

        assert exporter_calls["span"] == []
        assert len(exporter_calls["metric"]) == 1
        assert len(exporter_calls["log"]) == 1

    def test_metrics_disabled_skips_only_metric_exporter(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[dict[str, Any]]]
    ) -> None:
        _init_tracing_from_env(monkeypatch, {"MISTRAL_WORKFLOWS_OTEL_METRICS_EXPORT": "false"})

        assert exporter_calls["metric"] == []
        assert len(exporter_calls["span"]) == 1
        assert len(exporter_calls["log"]) == 1

    def test_logs_disabled_skips_only_log_exporter(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[dict[str, Any]]]
    ) -> None:
        _init_tracing_from_env(monkeypatch, {"MISTRAL_WORKFLOWS_OTEL_LOGS_EXPORT": "false"})

        assert exporter_calls["log"] == []
        assert len(exporter_calls["span"]) == 1
        assert len(exporter_calls["metric"]) == 1

    def test_all_enabled_constructs_one_exporter_per_signal(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[dict[str, Any]]]
    ) -> None:
        _init_tracing_from_env(monkeypatch, {})

        assert len(exporter_calls["span"]) == 1
        assert len(exporter_calls["metric"]) == 1
        assert len(exporter_calls["log"]) == 1


class TestApiKeyScoping:
    def test_explicit_endpoint_env_does_not_send_api_key(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[dict[str, Any]]]
    ) -> None:
        _init_tracing_from_env(
            monkeypatch,
            {
                "OTEL_TRACES_ENDPOINT": "http://custom-traces:4318",
                "OTEL_METRICS_ENDPOINT": "http://custom-metrics:4318",
                "OTEL_LOGS_ENDPOINT": "http://custom-logs:4318",
            },
        )

        assert exporter_calls["span"][0]["endpoint"].startswith("http://custom-traces:4318")
        assert exporter_calls["span"][0]["headers"] is None
        assert exporter_calls["metric"][0]["endpoint"].startswith("http://custom-metrics:4318")
        assert exporter_calls["metric"][0]["headers"] is None
        assert exporter_calls["log"][0]["endpoint"].startswith("http://custom-logs:4318")
        assert exporter_calls["log"][0]["headers"] is None

    def test_default_endpoint_env_sends_api_key_for_all_signals(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[dict[str, Any]]]
    ) -> None:
        _init_tracing_from_env(monkeypatch, {})

        assert exporter_calls["span"][0]["headers"] == {"Authorization": "Bearer test-key"}
        assert exporter_calls["log"][0]["headers"] == {"Authorization": "Bearer test-key"}
        # Metrics now mirror traces/logs: the default endpoint is derived from the Mistral
        # server URL (shared /telemetry base) and authenticated with the API key.
        assert exporter_calls["metric"][0]["endpoint"].endswith("/telemetry/v1/metrics")
        assert exporter_calls["metric"][0]["headers"] == {"Authorization": "Bearer test-key"}


class TestTemporalRuntimeMetricsToggle:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("metrics_export_env", "expected_otel_configs"),
        [("true", 1), ("false", 0)],
    )
    async def test_runtime_metrics_follow_metrics_env_toggle(
        self, monkeypatch: pytest.MonkeyPatch, metrics_export_env: str, expected_otel_configs: int
    ) -> None:
        from mistralai.workflows.core.config.config import AppConfig
        from mistralai.workflows.core.temporal import temporal_client

        monkeypatch.setenv("OTEL_ENABLED", "true")
        monkeypatch.setenv("MISTRAL_WORKFLOWS_OTEL_METRICS_EXPORT", metrics_export_env)
        fresh_config = AppConfig()
        monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_server_url", "http://api.test")
        monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_api_key", SecretStr("test-key"))

        otel_configs: list[dict[str, Any]] = []

        def record_otel_config(**kwargs: Any) -> MagicMock:
            otel_configs.append(kwargs)
            return MagicMock()

        async def fake_connect(_config: Any) -> MagicMock:
            return MagicMock()

        monkeypatch.setattr(temporal_client, "config", fresh_config)
        monkeypatch.setattr(temporal_client, "Runtime", lambda *a, **k: MagicMock())
        monkeypatch.setattr(temporal_client, "TelemetryConfig", lambda *a, **k: MagicMock())
        monkeypatch.setattr(temporal_client, "OpenTelemetryConfig", record_otel_config)
        monkeypatch.setattr(temporal_client.TemporalServiceClient, "connect", fake_connect)

        await temporal_client.create_temporal_service_client()

        assert len(otel_configs) == expected_otel_configs
        # When enabled, runtime metrics target the Mistral-derived endpoint with API key auth.
        if expected_otel_configs:
            assert otel_configs[0]["url"] == "http://api.test/telemetry/v1/metrics"
            assert otel_configs[0]["headers"] == {"Authorization": "Bearer test-key"}
