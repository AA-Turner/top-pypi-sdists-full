import logging
from collections.abc import Iterator
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock

import pytest
import structlog
from pydantic import SecretStr

from mistralai.workflows._version import __version__
from mistralai.workflows.core.auth import StaticTokenProvider
from mistralai.workflows.core.tracing import _otel_config
from mistralai.workflows.core.tracing._otel_config import (
    TELEMETRY_DISTRO_NAME_ATTRIBUTE,
    TELEMETRY_DISTRO_VERSION_ATTRIBUTE,
    WORKER_SERVICE_NAME,
    WORKFLOWS_TELEMETRY_DISTRO_NAME,
    _create_resource,
)


class _RecordingExporter:
    """Stand-in for an OTLP exporter: records construction kwargs and exposes a settable
    ``_session.auth`` so tests can verify the dynamic per-request bearer injection."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self._session = SimpleNamespace(auth=None)


def _bearer_of(exporter: _RecordingExporter) -> str | None:
    """Run the exporter's session auth against a dummy request and return the Authorization header."""
    if exporter._session.auth is None:
        return None
    request = SimpleNamespace(headers={})
    exporter._session.auth(request)
    return request.headers.get("Authorization")


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
def exporter_calls(monkeypatch: pytest.MonkeyPatch) -> Iterator[dict[str, list[Any]]]:
    """Record OTLP exporter construction without building real SDK providers or sockets.

    Each OTLP exporter is replaced with a recorder capturing its kwargs and exposing a settable
    ``_session.auth``; the providers, batch processors, reader, and log handler are stubbed so
    config_otel runs end-to-end without global side effects. Root logger handlers restored on teardown.
    """
    calls: dict[str, list[Any]] = {"span": [], "metric": [], "log": []}

    def recorder(bucket: str) -> Any:
        def _factory(*_args: Any, **kwargs: Any) -> _RecordingExporter:
            exporter = _RecordingExporter(**kwargs)
            calls[bucket].append(exporter)
            return exporter

        return _factory

    # config_otel instantiates the logging wrapper subclasses, so patch those to record construction.
    monkeypatch.setattr(_otel_config, "_LoggingOTLPSpanExporter", recorder("span"))
    monkeypatch.setattr(_otel_config, "_LoggingOTLPMetricExporter", recorder("metric"))
    monkeypatch.setattr(_otel_config, "_LoggingOTLPLogExporter", recorder("log"))
    for name in (
        "BatchSpanProcessor",
        "BatchLogRecordProcessor",
        "PeriodicExportingMetricReader",
        "TracerProvider",
        "MeterProvider",
        "LoggerProvider",
    ):
        monkeypatch.setattr(_otel_config, name, lambda *a, **k: MagicMock())
    # Span redaction wraps the raw exporter; keep the raw _RecordingExporter so _session is inspectable.
    monkeypatch.setattr(_otel_config, "_apply_span_redaction", lambda exporter, _redaction: exporter)
    # Real handler (not a MagicMock) so the root logger can compare levels when config_otel logs.
    monkeypatch.setattr(_otel_config, "LoggingHandler", lambda *a, **k: logging.NullHandler())

    root = logging.getLogger()
    original_handlers = list(root.handlers)
    yield calls
    root.handlers[:] = original_handlers


def _init_tracing_from_env(
    monkeypatch: pytest.MonkeyPatch,
    env: dict[str, str],
    *,
    client_api_key: SecretStr | None = SecretStr("test-key"),
    provider_token: str | None = None,
) -> list[dict[str, Any]]:
    """Drive the full chain: env vars -> AppConfig -> init_tracing -> config_otel -> OTLP exporters.

    Returns the structlog events captured during init_tracing so tests can assert on startup logs.
    """
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
    monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_api_key", client_api_key)
    if fresh_config.worker.agent.mistral_client_server_url is None:
        monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_server_url", "http://api.test")

    monkeypatch.setattr(
        init_tracing,
        "get_token_provider",
        lambda explicit=None: (
            StaticTokenProvider(explicit.get_secret_value() if explicit else provider_token)
            if (explicit or provider_token)
            else None
        ),
    )
    monkeypatch.setattr(init_tracing, "config", fresh_config)
    monkeypatch.setattr(init_tracing, "AsyncioInstrumentor", lambda: MagicMock())
    monkeypatch.setattr(init_tracing, "HTTPXClientInstrumentor", lambda: MagicMock())
    if init_tracing._HAS_AIOHTTP_INSTRUMENTATION:
        monkeypatch.setattr(init_tracing, "AioHttpClientInstrumentor", lambda: MagicMock())

    with structlog.testing.capture_logs() as captured:
        init_tracing.init_tracing("worker")
    return captured


class TestIndependentExportToggles:
    @pytest.mark.parametrize(
        ("disable_env", "disabled_bucket"),
        [
            ("MISTRAL_WORKFLOWS_OTEL_TRACES_EXPORT", "span"),
            ("MISTRAL_WORKFLOWS_OTEL_METRICS_EXPORT", "metric"),
            ("MISTRAL_WORKFLOWS_OTEL_LOGS_EXPORT", "log"),
        ],
    )
    def test_disabling_one_signal_skips_only_its_exporter(
        self,
        monkeypatch: pytest.MonkeyPatch,
        exporter_calls: dict[str, list[Any]],
        disable_env: str,
        disabled_bucket: str,
    ) -> None:
        _init_tracing_from_env(monkeypatch, {disable_env: "false"})

        # The worker builds two metric exporters: app metrics + the dedicated temporal runtime-metrics one.
        expected = {"span": 1, "metric": 2, "log": 1}
        assert exporter_calls[disabled_bucket] == []
        for bucket in ("span", "metric", "log"):
            if bucket != disabled_bucket:
                assert len(exporter_calls[bucket]) == expected[bucket]

    def test_all_enabled_constructs_expected_exporters_per_signal(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[Any]]
    ) -> None:
        _init_tracing_from_env(monkeypatch, {})

        assert len(exporter_calls["span"]) == 1
        # app metrics + dedicated temporal runtime-metrics exporter (worker_id-free provider)
        assert len(exporter_calls["metric"]) == 2
        assert len(exporter_calls["log"]) == 1


class TestApiKeyScoping:
    def test_explicit_endpoint_env_does_not_send_api_key(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[Any]]
    ) -> None:
        _init_tracing_from_env(
            monkeypatch,
            {
                "OTEL_TRACES_ENDPOINT": "http://custom-traces:4318",
                "OTEL_METRICS_ENDPOINT": "http://custom-metrics:4318",
                "OTEL_LOGS_ENDPOINT": "http://custom-logs:4318",
            },
        )

        # Explicit endpoints authenticate via OTEL_EXPORTER_OTLP_HEADERS; we attach no dynamic auth.
        assert exporter_calls["span"][0].kwargs["endpoint"].startswith("http://custom-traces:4318")
        assert exporter_calls["span"][0]._session.auth is None
        assert exporter_calls["metric"][0].kwargs["endpoint"].startswith("http://custom-metrics:4318")
        assert exporter_calls["metric"][0]._session.auth is None
        assert exporter_calls["log"][0].kwargs["endpoint"].startswith("http://custom-logs:4318")
        assert exporter_calls["log"][0]._session.auth is None

    def test_default_endpoint_env_sends_api_key_for_all_signals(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[Any]]
    ) -> None:
        _init_tracing_from_env(monkeypatch, {})

        # The bearer is injected per-request via session.auth (so a rotated token stays fresh).
        assert _bearer_of(exporter_calls["span"][0]) == "Bearer test-key"
        assert _bearer_of(exporter_calls["log"][0]) == "Bearer test-key"
        # Metrics mirror traces/logs: default endpoint derived from the Mistral server URL.
        assert exporter_calls["metric"][0].kwargs["endpoint"].endswith("/telemetry/v1/metrics")
        assert _bearer_of(exporter_calls["metric"][0]) == "Bearer test-key"

    def test_falls_back_to_token_provider_when_no_client_key(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[Any]]
    ) -> None:
        # SA-only deployment: no MISTRAL_CLIENT_API_KEY, but a service-account token is available.
        _init_tracing_from_env(monkeypatch, {}, client_api_key=None, provider_token="sa-token")

        assert _bearer_of(exporter_calls["span"][0]) == "Bearer sa-token"
        assert _bearer_of(exporter_calls["metric"][0]) == "Bearer sa-token"
        assert _bearer_of(exporter_calls["log"][0]) == "Bearer sa-token"

    def test_dynamic_auth_rereads_token_each_export(self) -> None:
        # The auth hook must call the provider on every request so rotation is picked up.
        tokens = iter(["first-token", "rotated-token"])

        class _RotatingProvider:
            def get_token(self) -> str:
                return next(tokens)

        exporter = _RecordingExporter(endpoint="http://api.test/telemetry/v1/traces")
        _otel_config._attach_dynamic_auth(exporter, _RotatingProvider())

        assert _bearer_of(exporter) == "Bearer first-token"
        assert _bearer_of(exporter) == "Bearer rotated-token"


def _telemetry_enabled_signals(captured: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    events = [entry for entry in captured if entry.get("event") == "Telemetry enabled"]
    assert len(events) == 1, f"expected exactly one 'Telemetry enabled' log, got {len(events)}"
    event = events[0]
    return {signal: event[signal] for signal in ("traces", "metrics", "logs")}


class TestTelemetryEnabledLog:
    def test_combined_log_endpoint_is_mistral_url_for_default_endpoint(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[Any]]
    ) -> None:
        signals = _telemetry_enabled_signals(_init_tracing_from_env(monkeypatch, {}))

        for entry in signals.values():
            assert entry["enabled"] is True
            assert entry["mode"] == "mistral"
            assert entry["endpoint"].endswith("/telemetry")

    def test_combined_log_endpoint_is_custom_url_for_overridden_signal(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[Any]]
    ) -> None:
        signals = _telemetry_enabled_signals(
            _init_tracing_from_env(monkeypatch, {"OTEL_TRACES_ENDPOINT": "http://custom-traces:4318"})
        )

        assert signals["traces"]["mode"] == "custom"
        assert signals["traces"]["endpoint"] == "http://custom-traces:4318"
        assert signals["metrics"]["mode"] == "mistral"
        assert signals["logs"]["mode"] == "mistral"

    def test_combined_log_marks_disabled_signal_not_enabled(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[Any]]
    ) -> None:
        signals = _telemetry_enabled_signals(
            _init_tracing_from_env(monkeypatch, {"MISTRAL_WORKFLOWS_OTEL_LOGS_EXPORT": "false"})
        )

        assert signals["logs"]["enabled"] is False
        assert signals["traces"]["enabled"] is True
        assert signals["metrics"]["enabled"] is True

    def test_combined_log_endpoint_is_none_for_local_mode(
        self, monkeypatch: pytest.MonkeyPatch, exporter_calls: dict[str, list[Any]]
    ) -> None:
        signals = _telemetry_enabled_signals(_init_tracing_from_env(monkeypatch, {"OTEL_LOCAL": "true"}))

        assert signals["traces"] == {"mode": "local", "endpoint": None, "enabled": True}
        assert signals["metrics"] == {"mode": "local", "endpoint": None, "enabled": True}
        assert signals["logs"] == {"mode": "local", "endpoint": None, "enabled": False}


class TestTemporalRuntimeMetricsBuffer:
    """build_runtime (worker-only) attaches a MetricBuffer; clients use build_client_runtime (direct OTLP)."""

    @staticmethod
    def _build(monkeypatch: pytest.MonkeyPatch, *, metrics_export: str) -> tuple[list[dict[str, Any]], Any]:
        from mistralai.workflows.core.config.config import AppConfig
        from mistralai.workflows.core.temporal import runtime_metrics

        monkeypatch.setenv("OTEL_ENABLED", "true")
        monkeypatch.setenv("MISTRAL_WORKFLOWS_OTEL_METRICS_EXPORT", metrics_export)
        fresh_config = AppConfig()
        monkeypatch.setattr(fresh_config.common, "app_version", "1.2.3")

        telemetry_configs: list[dict[str, Any]] = []
        monkeypatch.setattr(runtime_metrics, "config", fresh_config)
        monkeypatch.setattr(runtime_metrics, "Runtime", lambda *a, **k: MagicMock())
        monkeypatch.setattr(
            runtime_metrics, "TelemetryConfig", lambda **kwargs: telemetry_configs.append(kwargs) or MagicMock()
        )
        return telemetry_configs, runtime_metrics.build_runtime()

    def test_worker_runtime_builds_buffer(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from temporalio.runtime import MetricBuffer

        telemetry_configs, bundle = self._build(monkeypatch, metrics_export="true")
        assert isinstance(bundle.metric_buffer, MetricBuffer)
        assert isinstance(telemetry_configs[-1]["metrics"], MetricBuffer)
        assert telemetry_configs[-1]["attach_service_name"] is False
        assert telemetry_configs[-1]["global_tags"] == {
            "service.name": WORKER_SERVICE_NAME,
            "service.version": "1.2.3",
            "component.type": "worker",
            TELEMETRY_DISTRO_NAME_ATTRIBUTE: WORKFLOWS_TELEMETRY_DISTRO_NAME,
            TELEMETRY_DISTRO_VERSION_ATTRIBUTE: __version__,
        }

    def test_worker_runtime_has_no_buffer_when_metrics_disabled(self, monkeypatch: pytest.MonkeyPatch) -> None:
        telemetry_configs, bundle = self._build(monkeypatch, metrics_export="false")
        assert bundle.metric_buffer is None
        assert telemetry_configs[-1].get("metrics") is None

    @staticmethod
    def _build_client(monkeypatch: pytest.MonkeyPatch, provider: Any, **overrides: Any) -> list[dict[str, Any]]:
        """Capture the OpenTelemetryConfig kwargs build_client_runtime would export with (empty list = none)."""
        from mistralai.workflows.core.config.config import AppConfig
        from mistralai.workflows.core.temporal import runtime_metrics

        monkeypatch.setenv("OTEL_ENABLED", "true")
        monkeypatch.setenv("MISTRAL_WORKFLOWS_OTEL_METRICS_EXPORT", "true")
        fresh_config = AppConfig()
        monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_server_url", "http://api.test")
        monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_api_key", None)
        for attr, value in overrides.items():
            monkeypatch.setattr(fresh_config.common, attr, value)

        otel_configs: list[dict[str, Any]] = []
        monkeypatch.setattr(runtime_metrics, "config", fresh_config)
        monkeypatch.setattr(runtime_metrics, "get_token_provider", lambda *a, **k: provider)
        monkeypatch.setattr(runtime_metrics, "Runtime", lambda *a, **k: MagicMock())
        monkeypatch.setattr(runtime_metrics, "TelemetryConfig", lambda **k: MagicMock())
        monkeypatch.setattr(runtime_metrics, "OpenTelemetryConfig", lambda **k: otel_configs.append(k))
        runtime_metrics.build_client_runtime()
        return otel_configs

    def test_client_static_credential_exports_via_direct_otlp(self, monkeypatch: pytest.MonkeyPatch) -> None:
        otel_configs = self._build_client(monkeypatch, StaticTokenProvider("api-key"))
        assert otel_configs[0]["url"] == "http://api.test/telemetry/v1/metrics"
        assert otel_configs[0]["headers"] == {"Authorization": "Bearer api-key"}

    def test_client_rotating_credential_disables_metrics(self, monkeypatch: pytest.MonkeyPatch) -> None:
        class _Rotating:
            def get_token_with_max_age(self) -> tuple[str, float]:
                return ("tok", 3600.0)  # finite reuse window -> rotating, can't bake a durable header

        assert self._build_client(monkeypatch, _Rotating()) == []

    def test_client_explicit_endpoint_exports_without_baked_auth(self, monkeypatch: pytest.MonkeyPatch) -> None:
        otel_configs = self._build_client(
            monkeypatch, StaticTokenProvider("api-key"), otel_metrics_endpoint="http://collector:4318"
        )
        assert otel_configs[0]["url"] == "http://collector:4318/v1/metrics"
        assert otel_configs[0]["headers"] is None


def test_real_otlp_exporters_expose_session_for_dynamic_auth() -> None:
    # _attach_dynamic_auth relies on the exporter's private ``_session`` (a requests.Session) to recompute
    # the bearer per export. The dynamic-auth unit tests use a stand-in exporter, so this guards the real
    # dependency layout: a bump that drops/renames ``_session`` must fail here rather than silently ship
    # unauthenticated telemetry.
    import requests
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter as RealLog
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter as RealMetric
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as RealSpan

    for exporter in (
        RealSpan(endpoint="http://api.test/v1/traces"),
        RealMetric(endpoint="http://api.test/v1/metrics"),
        RealLog(endpoint="http://api.test/v1/logs"),
    ):
        assert isinstance(getattr(exporter, "_session", None), requests.Session)
