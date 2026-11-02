"""Studio GenAI tracing wiring for harness workers.

``configure_studio_genai_tracing`` is the core shared by both hosts: it configures
the isolated Observability SDK provider and installs the GenAI observers that feed
it. The host injects the pieces that differ as already-built OpenTelemetry types:
the span exporter (and optional processors), the redaction transformers, and the
``HarnessTurnObservability`` that owns identity binding and the observer.

``configure_managed_studio_tracing`` is the managed-worker entrypoint: it exports
to the public ``/telemetry`` ingest with a service-account bearer and binds no
per-turn identity scope.
"""

from collections.abc import Sequence
from enum import StrEnum
from typing import TYPE_CHECKING, override

import structlog
from opentelemetry.sdk._logs.export import LogRecordExporter, LogRecordExportResult
from opentelemetry.sdk.metrics.export import MetricExporter, MetricExportResult
from opentelemetry.sdk.trace import SpanProcessor
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.trace.sampling import ALWAYS_ON

from mistralai.vibe.harness.runtime.hosts.workflows import register_workflow_activity_genai_observer
from mistralai.vibe_agents import __version__
from mistralai.vibe_agents.sdk.app.config import (
    MANAGED_AGENT_SERVICE_NAME,
    AppSettings,
    OtelRedactionMode,
    get_app_settings,
)
from mistralai.vibe_agents.sdk.app.worker.observability import (
    HarnessTurnObservability,
    ObserverOnlyTurnObservability,
    register_harness_turn_observability,
)
from mistralai.workflows.core.config.config import config as workflow_config
from mistralai.workflows.core.tracing.exporters import (
    build_otlp_log_exporter,
    build_otlp_span_exporter,
    resolve_otlp_export_options,
)
from mistralai.workflows.protocol.v1.workflow import DeploymentLocation, LocationType

if TYPE_CHECKING:
    from mistralai.observability.otel import ObservabilityConfig, OperationDataTransformer

logger = structlog.get_logger(__name__)

RUN_MODE_ATTRIBUTE = "mistral.agents.run_mode"
DEPLOYMENT_LOCATION_ATTRIBUTE = "mistral.agents.deployment_location"


class StudioRunMode(StrEnum):
    SERVE = "serve"
    RUN_WORKER = "run_worker"


# Whether this module owns the process-global Studio provider. Set when we configure it; checked on
# shutdown so we never tear down a provider the embedding application configured on its own.
_provider_configured_here = False


class _DropMetricExporter(MetricExporter):
    @override
    def export(self, metrics_data: object, timeout_millis: float = 10_000, **kwargs: object) -> MetricExportResult:
        return MetricExportResult.SUCCESS

    @override
    def force_flush(self, timeout_millis: float = 10_000) -> bool:
        return True

    @override
    def shutdown(self, timeout_millis: float = 30_000, **kwargs: object) -> None:
        return None


class _DropLogExporter(LogRecordExporter):
    @override
    def export(self, batch: object) -> LogRecordExportResult:
        return LogRecordExportResult.SUCCESS

    @override
    def force_flush(self, timeout_millis: float = 10_000) -> bool:
        return True

    @override
    def shutdown(self) -> None:
        return None


def configure_studio_genai_tracing(
    *,
    observability_config: "ObservabilityConfig",
    span_exporter: SpanExporter,
    turn_observability: HarnessTurnObservability,
    span_processors: Sequence[SpanProcessor] = (),
    operation_data_transformers: Sequence["OperationDataTransformer"] = (),
    metric_exporter: MetricExporter | None = None,
    log_exporter: LogRecordExporter | None = None,
) -> None:
    """Configure the isolated Studio provider and install the GenAI observers.

    The provider is never made global: operational spans stay on the ``init_otel``
    global provider while this one carries only GenAI operations. ``metric_exporter``
    and ``log_exporter`` default to drops, so a host exports only the signals it
    passes. The installed ``turn_observability`` owns identity binding and supplies
    the workflow-side observer; a ``None`` observer installs nothing.
    """
    from mistralai.observability.otel import observability

    observability.configure(
        observability_config,
        operation_data_transformers=tuple(operation_data_transformers),
        span_exporter=span_exporter,
        span_processors=tuple(span_processors),
        metric_exporter=metric_exporter or _DropMetricExporter(),
        log_exporter=log_exporter or _DropLogExporter(),
    )
    register_harness_turn_observability(turn_observability)
    observer = turn_observability.session_genai_observer()
    if observer is not None:
        register_workflow_activity_genai_observer(observer)
    global _provider_configured_here
    _provider_configured_here = True


def shutdown_studio_genai_tracing() -> None:
    """Flush and shut down the Studio provider on graceful worker exit.

    The provider disables OTel's atexit auto-flush, so without this call buffered
    spans are dropped. A no-op unless this module configured the provider, so the
    unconditional worker-exit call never tears down one the embedding app owns.
    """
    global _provider_configured_here
    if not _provider_configured_here:
        return
    _provider_configured_here = False

    # Reaching here means configure_studio_genai_tracing ran, so the extra imported fine.
    from mistralai.observability.otel import observability

    observability.shutdown()


def _deployment_location() -> LocationType:
    location = workflow_config.worker.deployment_location
    return DeploymentLocation(location_type=location.location_type, k8s_cluster=location.k8s_cluster).location_type


def configure_managed_studio_tracing(
    *,
    run_mode: StudioRunMode,
    redaction: Sequence["OperationDataTransformer"] | None = None,
) -> bool:
    """Wire Studio GenAI tracing for a deployed managed-agent worker.

    Returns whether the provider was configured. On by default, off with
    ``AGENTS_SDK_STUDIO_TRACING_ENABLED=0``; also a no-op when Workflows span export
    is disabled or no Mistral server URL is configured. A setup failure is logged and the
    worker runs untraced. Exports to the public
    ``/telemetry`` ingest with the worker's service-account bearer; identity is
    attributed ingest-side from that token, so no per-turn scope is bound.
    ``redaction`` comes from ``Agent(redaction=...)`` and replaces the
    ``AGENTS_SDK_STUDIO_TRACING_REDACTION`` policy.
    """
    # Tracing is auxiliary; guard against setup failures.
    try:
        # Two independent off switches: Agents SDK and Workflows (Agent SDK telemetry configuration is
        # built on workflows helpers).
        settings = get_app_settings()
        if not settings.studio_tracing_enabled:
            logger.info("Studio tracing disabled: AGENTS_SDK_STUDIO_TRACING_ENABLED is off")
            return False
        from mistralai.observability.otel import ObservabilityConfig

        if not workflow_config.common.otel_enabled:
            logger.info("Studio tracing disabled: Workflows OTel export is off")
            return False

        # Reuse Workflows' helpers to build telemetry exporters. Redaction is applied via the Obs SDK.
        otlp_exports = resolve_otlp_export_options()
        span_exporter = build_otlp_span_exporter(otlp_exports.trace, otlp_exports.token_provider)
        if span_exporter is None:
            logger.warning("Studio tracing disabled: no traces endpoint resolved or traces export disabled")
            return False

        from mistralai.vibe.harness.runtime.genai_telemetry_observer import GenAITelemetryObserver

        observer = GenAITelemetryObserver(include_content=settings.studio_tracing_include_content)
        configure_studio_genai_tracing(
            observability_config=ObservabilityConfig(
                service_name=MANAGED_AGENT_SERVICE_NAME,
                service_version=__version__,
                resource_attributes={
                    RUN_MODE_ATTRIBUTE: run_mode.value,
                    DEPLOYMENT_LOCATION_ATTRIBUTE: _deployment_location().value,
                },
                # Studio spans parent on the operational turn span, which an upstream ratio
                # decision may drop; always sample so they are never lost.
                sampler=ALWAYS_ON,
            ),
            span_exporter=span_exporter,
            turn_observability=ObserverOnlyTurnObservability(observer),
            operation_data_transformers=_resolve_redaction(settings, redaction),
            # No metric exporter: the Studio telemetry platform does not fully support metrics yet.
            log_exporter=build_otlp_log_exporter(otlp_exports.log, otlp_exports.token_provider),
        )
    except Exception:
        logger.warning("Studio tracing disabled: setup failed; worker continues without it", exc_info=True)
        return False

    logger.info(
        "Studio tracing configured for managed worker",
        redaction="custom" if redaction is not None else settings.studio_tracing_redaction.value,
        include_content=settings.studio_tracing_include_content,
    )
    return True


def _resolve_redaction(
    settings: AppSettings, redaction: Sequence["OperationDataTransformer"] | None
) -> Sequence["OperationDataTransformer"]:
    if redaction is None:
        return redaction_transformers(settings.studio_tracing_redaction)
    if "studio_tracing_redaction" in settings.model_fields_set:
        logger.warning(
            "AGENTS_SDK_STUDIO_TRACING_REDACTION is ignored: the agent sets its own redaction",
            ignored=settings.studio_tracing_redaction.value,
        )
    return redaction


def redaction_transformers(mode: OtelRedactionMode) -> Sequence["OperationDataTransformer"]:
    """Map a redaction mode to the Obs SDK transformers applied before span export."""
    from mistralai.observability.otel import AttributeRedactionPolicy, RegexRedactionPolicy

    if mode is OtelRedactionMode.NONE:
        return ()
    if mode is OtelRedactionMode.STRICT:
        return (AttributeRedactionPolicy(),)
    return (RegexRedactionPolicy(),)
