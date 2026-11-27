"""Parity tests for the public OTLP exporter factory (tracing/exporters.py).

These lock down the behavior external hosts rely on: endpoint resolution per signal, the
Mistral service-account bearer attached only on the default endpoint, CUMULATIVE metric
temporality, None when a signal is disabled or unconfigured, and the config precedence in
``resolve_otlp_export_options`` (per-signal override vs default).
"""

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
import structlog
from pydantic import SecretStr

from mistralai.workflows.core.auth import StaticTokenProvider
from mistralai.workflows.core.tracing import exporters
from mistralai.workflows.core.tracing.exporters import (
    OtelExportOptions,
    OtelTransportOptions,
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

    def test_builder_passes_worker_specific_transport_options(self, recording_exporters: None) -> None:
        exporter = build_otlp_span_exporter(
            OtelExportOptions(
                endpoint="https://collector.test",
                transport=OtelTransportOptions(
                    certificate_file="/worker/ca.pem",
                    client_certificate_file="/worker/client.pem",
                    client_key_file="/worker/client.key",
                    authorization_bearer=SecretStr("worker-token"),
                ),
            )
        )

        assert isinstance(exporter, _RecordingExporter)
        assert exporter.kwargs["certificate_file"] == "/worker/ca.pem"
        assert exporter.kwargs["client_certificate_file"] == "/worker/client.pem"
        assert exporter.kwargs["client_key_file"] == "/worker/client.key"
        assert exporter.kwargs["headers"] == {"Authorization": "Bearer worker-token"}

    def test_builder_leaves_transport_unset_for_standard_env_fallback(self, recording_exporters: None) -> None:
        exporter = build_otlp_span_exporter(OtelExportOptions(endpoint="https://collector.test"))

        assert isinstance(exporter, _RecordingExporter)
        assert exporter.kwargs["certificate_file"] is None
        assert exporter.kwargs["client_certificate_file"] is None
        assert exporter.kwargs["client_key_file"] is None
        assert exporter.kwargs["headers"] is None

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
    common_api_key: SecretStr | None = None,
    ca_bundle: str | None = None,
    client_identity: tuple[str, str] | None = None,
) -> exporters.ResolvedOtlpExports:
    """Drive resolve_otlp_export_options from env vars with an injected config and token provider."""
    from mistralai.workflows.core.config.config import AppConfig

    monkeypatch.setenv("OTEL_ENABLED", "true")
    for key in (
        "OTEL_ENDPOINT",
        "otel_endpoint",
        "OTEL_TRACES_ENDPOINT",
        "OTEL_METRICS_ENDPOINT",
        "OTEL_LOGS_ENDPOINT",
        "OTEL_EXPORTER_OTLP_CERTIFICATE",
        "OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE",
        "OTEL_EXPORTER_OTLP_CLIENT_KEY",
        "OTEL_EXPORTER_OTLP_HEADERS",
        "OTEL_EXPORTER_OTLP_TRACES_CERTIFICATE",
        "OTEL_EXPORTER_OTLP_TRACES_CLIENT_CERTIFICATE",
        "OTEL_EXPORTER_OTLP_TRACES_CLIENT_KEY",
        "OTEL_EXPORTER_OTLP_TRACES_HEADERS",
        "OTEL_EXPORTER_OTLP_METRICS_CERTIFICATE",
        "OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE",
        "OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY",
        "OTEL_EXPORTER_OTLP_METRICS_HEADERS",
        "OTEL_EXPORTER_OTLP_LOGS_CERTIFICATE",
        "OTEL_EXPORTER_OTLP_LOGS_CLIENT_CERTIFICATE",
        "OTEL_EXPORTER_OTLP_LOGS_CLIENT_KEY",
        "OTEL_EXPORTER_OTLP_LOGS_HEADERS",
    ):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    fresh_config = AppConfig()
    # Inject directly to avoid the env/dotenv conflict detector on the key fields.
    monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_api_key", api_key)
    monkeypatch.setattr(fresh_config.worker.agent, "mistral_client_server_url", server_url)
    monkeypatch.setattr(fresh_config.common, "mistral_api_key", common_api_key)
    monkeypatch.setattr(fresh_config.common, "ca_bundle", ca_bundle)
    monkeypatch.setattr(
        fresh_config.common,
        "mtls_client_cert_path",
        client_identity[0] if client_identity is not None else None,
    )
    monkeypatch.setattr(
        fresh_config.common,
        "mtls_client_key_path",
        client_identity[1] if client_identity is not None else None,
    )
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

    def test_removed_otel_endpoint_is_ignored_with_a_warning(self, monkeypatch: pytest.MonkeyPatch) -> None:
        with structlog.testing.capture_logs() as captured:
            resolution = _resolve(monkeypatch, {"OTEL_ENDPOINT": "http://legacy:4318"})

        for options in (resolution.trace, resolution.metric, resolution.log):
            assert options.endpoint == "http://api.test/telemetry"
        [warning] = [entry for entry in captured if "OTEL_ENDPOINT is set but no longer used" in entry["event"]]
        assert warning["otel_endpoint"] == "http://legacy:4318"

    def test_removed_otel_endpoint_in_lowercase_env_var_is_warned(self, monkeypatch: pytest.MonkeyPatch) -> None:
        with structlog.testing.capture_logs() as captured:
            _resolve(monkeypatch, {"otel_endpoint": "http://lower-legacy:4318"})

        [warning] = [entry for entry in captured if "OTEL_ENDPOINT is set but no longer used" in entry["event"]]
        assert warning["otel_endpoint"] == "http://lower-legacy:4318"

    @pytest.mark.parametrize("key", ["OTEL_ENDPOINT", "otel_endpoint"])
    def test_removed_otel_endpoint_in_env_file_is_warned(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, key: str
    ) -> None:
        env_file = tmp_path / ".env"
        env_file.write_text(f"{key}=http://dotenv-legacy:4318\n")
        monkeypatch.setattr(exporters, "env_file", str(env_file))

        with structlog.testing.capture_logs() as captured:
            _resolve(monkeypatch, {})

        [warning] = [entry for entry in captured if "OTEL_ENDPOINT is set but no longer used" in entry["event"]]
        assert warning["otel_endpoint"] == "http://dotenv-legacy:4318"

    def test_no_warning_without_otel_endpoint(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setattr(exporters, "env_file", str(tmp_path / "missing.env"))
        with structlog.testing.capture_logs() as captured:
            _resolve(monkeypatch, {})

        assert not [entry for entry in captured if "OTEL_ENDPOINT" in entry["event"]]

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

    def test_worker_credentials_and_tls_are_scoped_to_each_exporter(self, monkeypatch: pytest.MonkeyPatch) -> None:
        resolution = _resolve(
            monkeypatch,
            {},
            common_api_key=SecretStr("worker-token"),
            ca_bundle="/worker/ca.pem",
            client_identity=("/worker/client.pem", "/worker/client.key"),
        )

        for options in (resolution.trace, resolution.metric, resolution.log):
            assert options.transport == OtelTransportOptions(
                certificate_file="/worker/ca.pem",
                client_certificate_file="/worker/client.pem",
                client_key_file="/worker/client.key",
                authorization_bearer=SecretStr("worker-token"),
            )

    def test_signal_environment_keeps_precedence_over_worker_transport(self, monkeypatch: pytest.MonkeyPatch) -> None:
        resolution = _resolve(
            monkeypatch,
            {
                "OTEL_EXPORTER_OTLP_TRACES_CERTIFICATE": "/signal/ca.pem",
                "OTEL_EXPORTER_OTLP_TRACES_CLIENT_CERTIFICATE": "/signal/client.pem",
                "OTEL_EXPORTER_OTLP_TRACES_CLIENT_KEY": "/signal/client.key",
                "OTEL_EXPORTER_OTLP_TRACES_HEADERS": "Authorization=Bearer signal-token",
            },
            common_api_key=SecretStr("worker-token"),
            ca_bundle="/worker/ca.pem",
            client_identity=("/worker/client.pem", "/worker/client.key"),
        )

        assert resolution.trace.transport == OtelTransportOptions()
        assert resolution.metric.transport.authorization_bearer == SecretStr("worker-token")
        assert resolution.metric.transport.certificate_file == "/worker/ca.pem"

    def test_generic_environment_keeps_precedence_over_worker_transport(self, monkeypatch: pytest.MonkeyPatch) -> None:
        resolution = _resolve(
            monkeypatch,
            {
                "OTEL_EXPORTER_OTLP_CERTIFICATE": "/generic/ca.pem",
                "OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE": "/generic/client.pem",
                "OTEL_EXPORTER_OTLP_CLIENT_KEY": "/generic/client.key",
                "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer generic-token",
            },
            common_api_key=SecretStr("worker-token"),
            ca_bundle="/worker/ca.pem",
            client_identity=("/worker/client.pem", "/worker/client.key"),
        )

        assert resolution.trace.transport == OtelTransportOptions()
        assert resolution.metric.transport == OtelTransportOptions()
        assert resolution.log.transport == OtelTransportOptions()

    def test_custom_endpoint_uses_only_custom_otel_authorization(self, monkeypatch: pytest.MonkeyPatch) -> None:
        resolution = _resolve(
            monkeypatch,
            {
                "OTEL_TRACES_ENDPOINT": "https://custom-collector.test",
                "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer custom-token",
            },
            common_api_key=SecretStr("worker-token"),
        )

        assert resolution.trace.use_api_key is False
        assert resolution.trace.transport.authorization_bearer is None
        assert resolution.metric.transport.authorization_bearer is None

    def test_no_server_url_and_no_override_yields_no_endpoint(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Assert-free: callers skip exporters whose endpoint is None instead of crashing.
        resolution = _resolve(monkeypatch, {}, server_url=None)

        assert resolution.trace.endpoint is None
        assert resolution.metric.endpoint is None
        assert resolution.log.endpoint is None
        assert resolution.token_provider is None
