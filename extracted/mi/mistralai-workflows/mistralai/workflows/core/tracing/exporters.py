"""Authenticated OTLP exporters and the export-config resolution Workflows telemetry uses.

Low-level layer: owns the OTLP exporter primitives (throttled ``_LoggingOTLP*`` exporters, their
dynamic bearer auth, endpoint resolution) and the public builders/resolver on top of them.
Returned exporters are pre-redaction; callers wrap them with their own redaction.
"""

import logging
import time
from dataclasses import dataclass
from typing import Any, Self, Sequence

import requests
import structlog
from opentelemetry.exporter.otlp.proto.http._log_exporter import DEFAULT_LOGS_EXPORT_PATH, OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import DEFAULT_METRICS_EXPORT_PATH, OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import DEFAULT_TRACES_EXPORT_PATH, OTLPSpanExporter
from opentelemetry.sdk._logs import ReadableLogRecord
from opentelemetry.sdk._logs.export import LogRecordExporter, LogRecordExportResult
from opentelemetry.sdk.metrics._internal.instrument import Counter, Histogram
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    MetricExporter,
    MetricExportResult,
    MetricsData,
)
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

from mistralai.workflows.core.auth import TokenProvider, get_token_provider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.logging import extract_error_context

logger = structlog.getLogger(__name__)

_EXPORT_WARN_INTERVAL_SECONDS = 30.0
_TOKEN_ERROR_LOG_INTERVAL_SECONDS = 60.0

_OTLP_404_HINT = (
    "the telemetry endpoint does not seem to exist (not found). If you configured a custom OTEL "
    "endpoint, check that it is correct; if you are using the default endpoint, your organization may "
    "not have access to telemetry export"
)


class _DropOtelExportDiagnosticsFilter(logging.Filter):
    """Keep OTLP export diagnostics out of the OTel log-export pipeline.

    Our export-failure warnings (emitted on this module's logger) and the OTel SDK's own exporter
    error logs would otherwise be bridged back into the log exporter; if the log endpoint is the
    broken one, each failed export emits a log that gets queued for export and fails again. These
    records still reach stdout via structlog.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        return record.name != __name__ and not record.name.startswith("opentelemetry.")


class _ExportStatusRecorder:
    """Record the last export response's HTTP status via a public requests response hook.

    The exporter collapses failures into a bare FAILURE result, so the status (needed for the 404
    hint) is captured on the ``requests.Session`` we inject through the exporters' public
    ``session`` constructor kwarg.
    """

    def __init__(self) -> None:
        self.last_status_code: int | None = None

    def record(self, response: Any, *_args: Any, **_kwargs: Any) -> Any:
        self.last_status_code = response.status_code
        return response

    def reset(self) -> None:
        self.last_status_code = None


class _OTLPExporterBase:
    """Shared machinery for the ``_LoggingOTLP*`` exporters: authenticated construction, failure warnings.

    ``build`` injects our ``requests.Session`` via the public ``session`` constructor kwarg. The OTLP
    exporters freeze their ``headers`` mapping at construction, so rotating tokens cannot ride in
    headers. Instead the session's ``auth`` callable re-reads the bearer on every request (public
    requests API), and its ``response`` hook records the last export's HTTP status for the throttled
    warning. Both mechanisms work on every supported opentelemetry layout (1.30 through 1.45+), which
    all send through the injected session.

    On export failure, subclasses warn via structlog with the last captured HTTP status (404 gets a
    hint). First failure logs immediately, then at most once per interval per signal (reporting
    suppressed count).
    """

    _status_recorder: _ExportStatusRecorder | None = None
    _last_export_warn: float | None = None
    _suppressed_export_warns: int = 0
    _last_token_error_log: float = 0.0
    _token_provider: TokenProvider | None = None

    def __init__(
        self,
        *args: Any,
        status_recorder: _ExportStatusRecorder | None = None,
        token_provider: TokenProvider | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._status_recorder = status_recorder
        self._token_provider = token_provider

    def _read_token(self) -> str | None:
        """Read the bearer on every export, throttling the read-failure log (this runs per request)."""
        provider = self._token_provider
        if provider is None:
            return None
        try:
            return provider.get_token()
        except Exception as exc:
            now = time.monotonic()
            if now - self._last_token_error_log >= _TOKEN_ERROR_LOG_INTERVAL_SECONDS:
                self._last_token_error_log = now
                logger.warning(
                    "Failed to read token for OTLP telemetry auth; "
                    "exporting unauthenticated until the token is readable again",
                    **extract_error_context(exc),
                )
            return None

    @classmethod
    def build(
        cls,
        *,
        endpoint: str,
        token_provider: TokenProvider | None = None,
        use_api_key: bool = True,
        **extra_kwargs: Any,
    ) -> Self:
        recorder = _ExportStatusRecorder()
        session = requests.Session()
        session.hooks["response"].append(recorder.record)

        exporter = cls(
            endpoint=endpoint,
            session=session,
            status_recorder=recorder,
            token_provider=token_provider if use_api_key else None,
            **extra_kwargs,
        )

        if use_api_key and token_provider is not None:

            def _inject(request: Any) -> Any:
                token = exporter._read_token()
                if token:
                    request.headers["Authorization"] = f"Bearer {token}"
                return request

            session.auth = _inject

        return exporter

    def _reset_export_status(self) -> None:
        if self._status_recorder is not None:
            self._status_recorder.reset()

    def _warn_export_failure(self, signal: str, endpoint: str | None, exc: Exception | None = None) -> None:
        now = time.monotonic()
        if self._last_export_warn is not None and now - self._last_export_warn < _EXPORT_WARN_INTERVAL_SECONDS:
            self._suppressed_export_warns += 1
            return
        status_code = self._status_recorder.last_status_code if self._status_recorder is not None else None
        extra: dict[str, Any] = dict(extract_error_context(exc)) if exc is not None else {}
        if status_code is not None:
            extra["status_code"] = status_code
        if self._suppressed_export_warns:
            extra["suppressed_failures"] = self._suppressed_export_warns
        message = f"Failed to export OpenTelemetry {signal}"
        if status_code == 404:
            message = f"{message}: {_OTLP_404_HINT}"
        logger.warning(message, endpoint=endpoint, **extra)
        self._last_export_warn = now
        self._suppressed_export_warns = 0


class _LoggingOTLPSpanExporter(_OTLPExporterBase, OTLPSpanExporter):
    """OTLP span exporter that warns via structlog when export fails.

    The upstream exporter swallows export failures (e.g. an invalid endpoint returning 404) and only
    emits a raw stdlib log, so we surface a throttled structured warning instead of failing silently.
    """

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        self._reset_export_status()
        try:
            result = super().export(spans)
        except Exception as exc:
            self._warn_export_failure("traces", self._endpoint, exc)
            return SpanExportResult.FAILURE
        if result is SpanExportResult.FAILURE:
            self._warn_export_failure("traces", self._endpoint)
        return result


class _LoggingOTLPMetricExporter(_OTLPExporterBase, OTLPMetricExporter):
    """OTLP metric exporter that warns via structlog when export fails."""

    def export(
        self, metrics_data: MetricsData, timeout_millis: float | None = 10_000, **kwargs: Any
    ) -> MetricExportResult:
        self._reset_export_status()
        try:
            result = super().export(metrics_data, timeout_millis, **kwargs)
        except Exception as exc:
            self._warn_export_failure("metrics", self._endpoint, exc)
            return MetricExportResult.FAILURE
        if result is MetricExportResult.FAILURE:
            self._warn_export_failure("metrics", self._endpoint)
        return result


class _LoggingOTLPLogExporter(_OTLPExporterBase, OTLPLogExporter):
    """OTLP log exporter that warns via structlog when export fails.

    The warning is emitted on the internal structlog logger only (not routed through the OTel logging
    handler) so a broken log endpoint cannot feed its own failures back into the export pipeline.
    """

    def export(self, batch: Sequence[ReadableLogRecord]) -> LogRecordExportResult:
        self._reset_export_status()
        try:
            result = super().export(batch)
        except Exception as exc:
            self._warn_export_failure("logs", self._endpoint, exc)
            return LogRecordExportResult.FAILURE
        if result is LogRecordExportResult.FAILURE:
            self._warn_export_failure("logs", self._endpoint)
        return result


@dataclass(frozen=True)
class OtelExportOptions:
    """Per-export-type options for an OTLP exporter (traces, metrics, or logs).

    endpoint: OTLP base endpoint; export is skipped when unset.
    enabled: whether to export this telemetry type at all.
    use_api_key: whether to authenticate the exporter with the Mistral API key.
    """

    endpoint: str | None = None
    enabled: bool = True
    use_api_key: bool = True


def _resolve_endpoint(options: OtelExportOptions, export_path: str) -> str:
    assert options.endpoint is not None
    return options.endpoint.removesuffix("/") + "/" + export_path


def build_otlp_span_exporter(
    options: OtelExportOptions, token_provider: TokenProvider | None = None
) -> SpanExporter | None:
    """Build an authenticated OTLP span exporter, or None when traces export is off or unconfigured."""
    if not (options.enabled and options.endpoint):
        return None
    return _LoggingOTLPSpanExporter.build(
        endpoint=_resolve_endpoint(options, DEFAULT_TRACES_EXPORT_PATH),
        token_provider=token_provider,
        use_api_key=options.use_api_key,
    )


def build_otlp_metric_exporter(
    options: OtelExportOptions, token_provider: TokenProvider | None = None
) -> MetricExporter | None:
    """Build an OTLP metric exporter (CUMULATIVE temporality), or None when metrics export is off."""
    if not (options.enabled and options.endpoint):
        return None
    preferred_temporality: dict[type, AggregationTemporality] = {
        Histogram: AggregationTemporality.CUMULATIVE,
        Counter: AggregationTemporality.CUMULATIVE,
    }
    return _LoggingOTLPMetricExporter.build(
        endpoint=_resolve_endpoint(options, DEFAULT_METRICS_EXPORT_PATH),
        token_provider=token_provider,
        use_api_key=options.use_api_key,
        preferred_temporality=preferred_temporality,
    )


def build_otlp_log_exporter(
    options: OtelExportOptions, token_provider: TokenProvider | None = None
) -> LogRecordExporter | None:
    """Build an authenticated OTLP log exporter, or None when logs export is off or unconfigured."""
    if not (options.enabled and options.endpoint):
        return None
    return _LoggingOTLPLogExporter.build(
        endpoint=_resolve_endpoint(options, DEFAULT_LOGS_EXPORT_PATH),
        token_provider=token_provider,
        use_api_key=options.use_api_key,
    )


def _build_export_options(
    endpoint_override: str | None, default_endpoint: str | None, enabled: bool
) -> OtelExportOptions:
    # Authenticate with the Mistral key only on the default endpoint; an explicit override carries
    # its own auth via the conventional OTLP env vars (e.g. OTEL_EXPORTER_OTLP_HEADERS).
    return OtelExportOptions(
        endpoint=endpoint_override or default_endpoint,
        enabled=enabled,
        use_api_key=not endpoint_override,
    )


@dataclass(frozen=True)
class ResolvedOtlpExports:
    """Per-signal OTLP options plus the shared token provider, resolved from config."""

    trace: OtelExportOptions
    metric: OtelExportOptions
    log: OtelExportOptions
    token_provider: TokenProvider | None


def resolve_otlp_export_options() -> ResolvedOtlpExports:
    """Resolve per-signal OTLP export options and the shared token provider from the global config.

    Per signal, the endpoint precedence is: the deprecated ``otel_endpoint`` (all signals, no auth);
    else a per-signal override (own auth); else the default ``<mistral_server_url>/telemetry`` ingest
    with the Mistral service-account bearer. When neither an override nor a server URL is configured,
    the resolved endpoint is None and callers skip that exporter.
    """
    common = config.common
    if common.otel_endpoint:
        logger.warning(
            "otel_endpoint is deprecated, use otel_traces_endpoint and otel_metrics_endpoint instead",
        )
        return ResolvedOtlpExports(
            trace=_build_export_options(common.otel_endpoint, None, common.mistral_workflows_otel_traces_export),
            metric=_build_export_options(common.otel_endpoint, None, common.mistral_workflows_otel_metrics_export),
            log=_build_export_options(common.otel_endpoint, None, common.mistral_workflows_otel_logs_export),
            token_provider=None,
        )

    server_url = config.worker.agent.mistral_client_server_url
    default_endpoint = f"{server_url.rstrip('/')}/telemetry" if server_url else None
    token_provider = get_token_provider(config.worker.agent.mistral_client_api_key) if server_url else None
    return ResolvedOtlpExports(
        trace=_build_export_options(
            common.otel_traces_endpoint, default_endpoint, common.mistral_workflows_otel_traces_export
        ),
        metric=_build_export_options(
            common.otel_metrics_endpoint, default_endpoint, common.mistral_workflows_otel_metrics_export
        ),
        log=_build_export_options(
            common.otel_logs_endpoint, default_endpoint, common.mistral_workflows_otel_logs_export
        ),
        token_provider=token_provider,
    )
