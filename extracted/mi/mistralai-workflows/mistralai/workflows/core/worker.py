import asyncio
import json
import os
import signal
import threading
import time
import warnings
from contextlib import ExitStack, asynccontextmanager, contextmanager
from dataclasses import dataclass
from datetime import timedelta
from http import HTTPStatus
from types import FrameType
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Iterator, List, Sequence, Type
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from mistralai.workflows.core.graph_summaries import SummaryResult
    from mistralai.workflows.core.wire_format import AtlasWireFormat, FlatNode
import temporalio.api.workflowservice.v1 as wsv1
import tenacity
from mistralai.extra.workflows.encoding.config import PayloadEncryptionConfig as PayloadEncryptionConfigBase
from mistralai.extra.workflows.encoding.config import WorkflowEncodingConfig
from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder
from opentelemetry.instrumentation.utils import suppress_instrumentation
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.metrics import MeterProvider
from pydantic import SecretStr
from temporalio.client import Client as TemporalClient
from temporalio.client import Interceptor
from temporalio.common import VersioningBehavior, WorkerDeploymentVersion
from temporalio.converter import (
    DefaultFailureConverter,
    DefaultFailureConverterWithEncodedAttributes,
    FailureConverter,
    PayloadCodec,
    PayloadConverter,
)
from temporalio.service import RPCError, RPCStatusCode
from temporalio.worker import PollerBehaviorSimpleMaximum, Worker, WorkerDeploymentConfig
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner

from mistralai.workflows.client import translate_model
from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core._events.event_interceptor import EventInterceptor
from mistralai.workflows.core._events.event_route_publisher import EventRoutePublisher
from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core._registration.execution_registration_interceptor import (
    ExecutionRegistrationInterceptor,
)
from mistralai.workflows.core.activity import activity, get_all_temporal_activities
from mistralai.workflows.core.auth import get_token_provider
from mistralai.workflows.core.auth.header_files import get_deployment_headers
from mistralai.workflows.core.auth.startup_read import read_credential_at_startup
from mistralai.workflows.core.config import config_discovery
from mistralai.workflows.core.config.config import (
    AppConfig,
    log_configuration,
    resolve_worker_config,
    setup_default_logging,
    use_config,
)
from mistralai.workflows.core.config.config import WorkerConfig as WorkerSettings
from mistralai.workflows.core.definition._workflow_preparation import (
    _use_workflow_config_for_worker,
    configure_workflows_for_worker,
)
from mistralai.workflows.core.definition.workflow_definition import (
    get_workflow_definition,
)
from mistralai.workflows.core.dependencies.dependency_injector import DependencyInjector
from mistralai.workflows.core.encoding.fields_offloader import FieldsOffloader
from mistralai.workflows.core.execution.concurrency import ParallelExecutionWorkflow
from mistralai.workflows.core.execution.concurrency._concurrency_workflow import (
    OnBehalfOfParallelExecutionWorkflow,
)
from mistralai.workflows.core.execution.sticky_session.get_sticky_worker_session import (
    GET_STICKY_WORKER_SESSION_ACTIVITY_NAME,
)
from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import StickyWorkerSession
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.core.sandbox import (
    get_sandbox_restrictions,
    log_if_sandbox_restriction_error,
)
from mistralai.workflows.core.temporal.activity_offloading_interceptor import (
    ActivityInOutOffloadingInterceptor,
)
from mistralai.workflows.core.temporal.context_handler_interceptor import (
    ContextHandlerInterceptor,
)
from mistralai.workflows.core.temporal.payload_codec import MistralWorkflowsPayloadCodec
from mistralai.workflows.core.temporal.payload_converter import (
    MistralWorkflowsPayloadConverter,
)
from mistralai.workflows.core.temporal.runtime_metrics import build_runtime, pump_runtime_metrics
from mistralai.workflows.core.temporal.temporal_client import (
    create_temporal_client,
    refresh_temporal_credentials,
    set_worker_service_client,
)
from mistralai.workflows.core.tracing._temporal_tracing_interceptor import (
    get_span_recording_interceptors,
    get_trace_context_interceptors,
)
from mistralai.workflows.core.tracing.init_tracing import init_tracing
from mistralai.workflows.core.utils.health_server import HealthServer
from mistralai.workflows.core.worker_client import get_worker_client, share_worker_client
from mistralai.workflows.core.worker_polls import (
    WorkerConfig as WorkerConfig,
)
from mistralai.workflows.core.worker_polls import (
    estimate_connection_polls,
    format_poll_warning,
    group_activities_by_worker_config,
)
from mistralai.workflows.core.worker_registrations import (
    build_worker_registrations,
    set_worker_registrations,
)
from mistralai.workflows.core.workflow import ClassType
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.models import WorkflowSpecWithTaskQueue
from mistralai.workflows.plugins._discovery import (
    collect_plugin_interceptors,
    list_plugins,
)
from mistralai.workflows.protocol.v1.worker import PayloadEncryptionLevel
from mistralai.workflows.protocol.v1.workflow import (
    DeploymentLocation,
    WorkflowRegistrationRef,
    WorkflowSpecsRegisterResponse,
)
from mistralai.workflows.worker_client import models as wc_models
from mistralai.workflows.worker_client.errors.sdkerror import SDKError
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

logger = get_logger(__name__)


@tenacity.retry(
    retry=tenacity.retry_if_exception(lambda exc: isinstance(exc, WorkflowsException) and exc.is_transient()),
    before_sleep=lambda retry_state: logger.warning(
        "Retrying register workflow specs",
        attempt=retry_state.attempt_number,
    ),
    stop=tenacity.stop_after_attempt(15),
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=15),
    reraise=True,
)
async def _register_workflow_specs(
    worker_client: PrivateWorkerClient,
    workflow_definitions: list[WorkflowSpecWithTaskQueue],
    deployment_name: str,
    worker_name: str,
    deployment_location: DeploymentLocation | None = None,
    *,
    payload_encryption_mode: PayloadEncryptionLevel = PayloadEncryptionLevel.NONE,
) -> WorkflowSpecsRegisterResponse:
    try:
        result = await worker_client.register_workflow_definitions_async(
            # Omitting `schedules` tells the API this worker doesn't manage schedules, so it keeps the existing
            # ones. An empty list would make it delete those declared by v3 workers.
            definitions=[
                wc_models.WorkflowSpecWithTaskQueue.model_validate(d.model_dump(mode="json", exclude={"schedules"}))
                for d in workflow_definitions
            ],
            deployment_name=deployment_name,
            worker_name=worker_name,
            deployment_location=translate_model(wc_models.DeploymentLocation, deployment_location)
            if deployment_location
            else None,
            payload_encryption_mode=payload_encryption_mode.value,
        )
        return translate_model(WorkflowSpecsRegisterResponse, result)
    except Exception as exc:
        if isinstance(exc, SDKError) and exc.status_code == HTTPStatus.FORBIDDEN:
            try:
                body = json.loads(exc.body)
                # The deployment page acts on the pin; the server omits it when it cannot build it.
                remediation_url = body.get("deployment_url") or body.get("admin_panel_url")
                if body.get("code") == "WF_1104":
                    # Relay the server's reason so later server-side wording changes reach workers
                    # without an SDK upgrade.
                    logger.error(
                        "Workflow registration refused",
                        reason=body.get("detail") or "this principal is not authorized for this deployment",
                        **({"remediation_url": remediation_url} if remediation_url else {}),
                    )
            except (json.JSONDecodeError, ValueError, AttributeError, TypeError):
                pass
        raise WorkflowsException.from_api_client_error(
            exc, message="Failed to register workflow specs", code=ErrorCode.POST_WORKFLOWS_REGISTER_ERROR
        ) from exc


async def _worker_heartbeat(
    worker_client: PrivateWorkerClient,
    workflow_definitions: list[WorkflowSpecWithTaskQueue],
    workflow_registration_refs: list[WorkflowRegistrationRef],
    interval: int,
    deployment_name: str,
    worker_name: str,
    deployment_location: DeploymentLocation | None = None,
    *,
    payload_encryption_mode: PayloadEncryptionLevel = PayloadEncryptionLevel.NONE,
) -> None:
    refs = list(workflow_registration_refs)

    heartbeat_endpoint_available = True

    async def _heartbeat_succeeds() -> bool:
        nonlocal heartbeat_endpoint_available
        if not heartbeat_endpoint_available:
            return False
        try:
            with suppress_instrumentation():
                await worker_client.heartbeat_async(
                    workflow_registration_refs=[
                        translate_model(wc_models.WorkflowRegistrationRefInput, ref) for ref in refs
                    ],
                    deployment_name=deployment_name,
                    worker_name=worker_name,
                    payload_encryption_mode=payload_encryption_mode.value,
                )
            return True
        except Exception as exc:
            if isinstance(exc, SDKError) and exc.status_code in (404, 405):
                logger.warning(
                    "Heartbeat endpoint not available, disabling heartbeat and falling back to full registration",
                    **extract_error_context(exc),
                )
                heartbeat_endpoint_available = False
            else:
                logger.warning("Heartbeat failed, falling back to full registration", **extract_error_context(exc))
            return False

    try:
        while True:
            await asyncio.sleep(interval)
            if await _heartbeat_succeeds():
                continue
            try:
                response = await _register_workflow_specs(
                    worker_client,
                    workflow_definitions,
                    deployment_name=deployment_name,
                    worker_name=worker_name,
                    deployment_location=deployment_location,
                    payload_encryption_mode=payload_encryption_mode,
                )
                refs = [
                    WorkflowRegistrationRef(
                        workflow_id=ref.workflow_id,
                        workflow_registration_id=ref.workflow_registration_id,
                    )
                    for ref in response.workflow_registration_refs
                ]
                set_worker_registrations(build_worker_registrations(workflow_definitions, refs))
            except Exception as exc:
                logger.error("Full re-registration also failed", **extract_error_context(exc))
    except Exception as exc:
        logger.error("Error in heartbeat task", **extract_error_context(exc))
        raise WorkflowsException(code=ErrorCode.WORKER_REGISTRATION_ERROR, message="Fail to heartbeat worker")


def _is_deployment_controller_managed_error(exc: BaseException) -> bool:
    """Whether current-version registration was rejected because a deployment manager owns it.

    When the Temporal Worker Controller manages a deployment it claims the ManagerIdentity,
    and the server rejects SetWorkerDeploymentCurrentVersion with FAILED_PRECONDITION and a
    ManagerIdentity message. Auto-registration is meant for manual/local deployments only, so
    this is expected for controller-managed deployments and can never succeed by retrying.
    """
    return (
        isinstance(exc, RPCError) and exc.status == RPCStatusCode.FAILED_PRECONDITION and "ManagerIdentity" in str(exc)
    )


_AUTO_REGISTER_RETRY_BUDGET_SECONDS = 120


@tenacity.retry(
    # retry_if_exception_type(Exception) excludes BaseException: tenacity captures those too, and
    # retrying through the CancelledError raised on worker shutdown would stall it.
    retry=tenacity.retry_if_exception_type(Exception)
    & tenacity.retry_if_exception(lambda exc: not _is_deployment_controller_managed_error(exc)),
    before_sleep=lambda retry_state: logger.debug(
        "Waiting for worker deployment to be available",
        attempt=retry_state.attempt_number,
    ),
    stop=tenacity.stop_after_delay(_AUTO_REGISTER_RETRY_BUDGET_SECONDS),
    wait=tenacity.wait_exponential(multiplier=0.25, max=2.5),
    reraise=True,
)
async def _set_current_deployment_version(
    temporal_client: TemporalClient,
    namespace: str,
    deployment_name: str,
    build_id: str,
) -> None:
    await temporal_client.workflow_service.set_worker_deployment_current_version(
        wsv1.SetWorkerDeploymentCurrentVersionRequest(
            namespace=namespace,
            deployment_name=deployment_name,
            build_id=build_id,
        )
    )


async def _auto_register_as_current_version(
    temporal_client: TemporalClient,
    namespace: str,
    deployment_name: str,
    build_id: str,
) -> None:
    """
    Auto-register worker as current version for manual/local deployments.

    Retries until successful, as the Worker Deployment does not exist until this worker has polled
    its task queue at least once. Backoff starts short because that first poll usually lands within
    a second, and only widens if the deployment is genuinely slow to appear.

    Stands down without retrying if the deployment is owned by a manager (e.g. the Temporal Worker
    Controller), which is the expected state there.

    Args:
        temporal_client: Temporal client instance
        namespace: Temporal namespace
        deployment_name: Worker deployment name
        build_id: Build ID to set as current
    """
    try:
        await _set_current_deployment_version(temporal_client, namespace, deployment_name, build_id)
    except Exception as exc:
        if _is_deployment_controller_managed_error(exc):
            logger.info(
                "Skipping worker current-version auto-registration: deployment is controller-managed",
                deployment_name=deployment_name,
                build_id=build_id,
            )
            return

        logger.error(
            "Failed to auto-register worker as current version within the retry budget",
            **extract_error_context(exc),
            deployment_name=deployment_name,
            build_id=build_id,
            retry_budget_seconds=_AUTO_REGISTER_RETRY_BUDGET_SECONDS,
        )
        return

    logger.info(
        "Successfully auto-registered worker as current version",
        deployment_name=deployment_name,
        build_id=build_id,
    )


def _get_workflow_definitions(workflows: Sequence[Type], deployment_name: str) -> List[WorkflowSpecWithTaskQueue]:
    workflow_definitions: List[WorkflowSpecWithTaskQueue] = []
    for workflow in workflows:
        workflow_def = get_workflow_definition(workflow)
        workflow_def_with_task_queue = WorkflowSpecWithTaskQueue.model_validate(
            {
                **workflow_def.model_dump(),
                "task_queue": deployment_name,
            }
        )
        workflow_definitions.append(workflow_def_with_task_queue)
    return workflow_definitions


def _get_parallel_execution_workflows(workflows: Sequence[Type]) -> list[Type]:
    parallel_workflows: list[Type] = [ParallelExecutionWorkflow]
    # Registered like any other spec, so only add it where it can be used: on_behalf_of=True
    # requires a deployment that can bind a user identity.
    if any(get_workflow_definition(workflow).on_behalf_of for workflow in workflows):
        parallel_workflows.append(OnBehalfOfParallelExecutionWorkflow)
    return parallel_workflows


@dataclass(frozen=True, kw_only=True)
class _WorkerPayloadEncoding:
    payload_codec: PayloadCodec
    failure_converter: Type[FailureConverter]
    event_payload_encoder: PayloadEncoder | None
    custom_event_payload_encoder: PayloadEncoder | None


def _build_event_payload_encoder(encryption_config: PayloadEncryptionConfigBase) -> PayloadEncoder:
    # Events don't support offloading
    return PayloadEncoder(
        encoding_config=WorkflowEncodingConfig(payload_encryption=encryption_config, payload_offloading=None)
    )


def _build_worker_payload_encoding(worker_settings: WorkerSettings) -> _WorkerPayloadEncoding:
    encryption_config = worker_settings.temporal_payload_encryption
    payload_codec = MistralWorkflowsPayloadCodec(
        payload_offloading_config=worker_settings.temporal_payload_offloading,
        payload_encryption_config=encryption_config,
        payload_compression_config=worker_settings.temporal_payload_compression,
    )
    # Temporal stores failure messages and stack traces outside payloads. With full encryption they are
    # moved into an encoded attribute, so the codec encrypts them like any other payload.
    failure_converter: Type[FailureConverter] = (
        DefaultFailureConverterWithEncodedAttributes
        if worker_settings.encrypts_payloads_fully
        else DefaultFailureConverter
    )
    if encryption_config is None:
        return _WorkerPayloadEncoding(
            payload_codec=payload_codec,
            failure_converter=failure_converter,
            event_payload_encoder=None,
            custom_event_payload_encoder=None,
        )
    custom_event_payload_encoder = (
        _build_event_payload_encoder(encryption_config.custom_event_config)
        if encryption_config.custom_event_mode is not None
        else None
    )
    return _WorkerPayloadEncoding(
        payload_codec=payload_codec,
        failure_converter=failure_converter,
        event_payload_encoder=_build_event_payload_encoder(encryption_config),
        custom_event_payload_encoder=custom_event_payload_encoder,
    )


def _create_temporal_workers(
    temporal_client: TemporalClient,
    workflows: List[ClassType],
    config: AppConfig,
    task_queue: str,
    workflow_config_registrations: ExitStack,
) -> tuple[List[Worker], List[Type]]:
    """Create Temporal workers and return (workers, plugin_workflows)."""
    parallel_workflows = _get_parallel_execution_workflows(workflows)
    all_workflows: List[Type] = [*workflows, *parallel_workflows]
    pre_plugin_len = len(all_workflows)

    # Plugins can index workflow metadata while their interceptors are constructed, so apply
    # definition-time configuration before exposing the workflow classes to plugin hooks.
    configure_workflows_for_worker(all_workflows, config, workflow_config_registrations)
    for workflow_type in all_workflows:
        workflow_config_registrations.enter_context(_use_workflow_config_for_worker(workflow_type, config, task_queue))

    # Collect worker interceptors from plugins
    plugin_interceptors = collect_plugin_interceptors(all_workflows)
    plugin_workflows = all_workflows[pre_plugin_len:]

    # Hooks may append plugin-owned workflows. Configure only those additions here; the original
    # workflows were already configured before their metadata could be snapshotted.
    configure_workflows_for_worker(plugin_workflows, config, workflow_config_registrations)
    for workflow_type in plugin_workflows:
        workflow_config_registrations.enter_context(_use_workflow_config_for_worker(workflow_type, config, task_queue))

    # Get all activities (based on the imports made before running the workers)
    all_activities = get_all_temporal_activities()
    logger.info("Registered activities", activities=[act.__name__ for act in all_activities])

    # Sticky Worker Session
    random_id = uuid4().hex.replace("-", "")
    sticky_worker_session_task_queue = f"{task_queue}-sticky-worker-session-{random_id}"

    @activity(name=GET_STICKY_WORKER_SESSION_ACTIVITY_NAME, _skip_registering=True)
    async def get_sticky_worker_session() -> StickyWorkerSession:
        return StickyWorkerSession(task_queue=sticky_worker_session_task_queue)

    all_activities.append(get_sticky_worker_session)

    # Split activities into workers based on their needs (see group_activities_by_worker_config)
    activity_groups = group_activities_by_worker_config(all_activities, task_queue, sticky_worker_session_task_queue)

    versioning_cfg = config.worker.versioning
    main_task_queue = task_queue
    deployment_config: WorkerDeploymentConfig | None = None

    if versioning_cfg.enabled and versioning_cfg.deployment_name and versioning_cfg.build_id:
        if main_task_queue == "default":
            raise ValueError(
                "Versioned workers must not use DEPLOYMENT_NAME='default'. "
                "Set DEPLOYMENT_NAME to a unique, non-default name before enabling worker versioning."
            )
        default_behavior = VersioningBehavior.PINNED
        deployment_config = WorkerDeploymentConfig(
            use_worker_versioning=True,
            version=WorkerDeploymentVersion(
                deployment_name=versioning_cfg.deployment_name,
                build_id=versioning_cfg.build_id,
            ),
            default_versioning_behavior=default_behavior,
        )
        logger.info(
            "Worker deployment config created",
            deployment_name=versioning_cfg.deployment_name,
            build_id=versioning_cfg.build_id,
        )
    elif versioning_cfg.enabled:
        logger.warning("Worker versioning enabled but deployment name or build ID missing; running without versioning")

    workers: List[Worker] = []
    for group in activity_groups:
        worker_config_obj = group.worker_config
        activities = group.activities
        is_main_worker = group.is_main
        worker_kwargs: dict[str, Any] = {
            "client": temporal_client,
            "task_queue": worker_config_obj.task_queue,
            "workflows": all_workflows if is_main_worker else [],
            "activities": activities,
            "max_task_queue_activities_per_second": worker_config_obj.max_task_queue_activities_per_second,
            "workflow_failure_exception_types": [Exception]
            if config.worker.dangerously_force_fail_workflow_on_error
            else [],
            "workflow_runner": SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
            "interceptors": plugin_interceptors,
            "max_concurrent_activities": config.worker.max_concurrent_activities,
            "max_cached_workflows": config.worker.max_cached_workflows,
            "graceful_shutdown_timeout": timedelta(seconds=config.worker.graceful_shutdown_timeout_seconds),
        }
        worker_kwargs["workflow_task_poller_behavior"] = PollerBehaviorSimpleMaximum(
            maximum=config.worker.max_workflow_task_pollers
        )
        worker_kwargs["activity_task_poller_behavior"] = PollerBehaviorSimpleMaximum(
            maximum=config.worker.max_activity_task_pollers
        )

        if is_main_worker and deployment_config is not None:
            worker_kwargs["deployment_config"] = deployment_config
        else:
            # Temporal 1.24 rejects overlapping unversioned workers unless they have distinct deployment build IDs.
            worker_deployment_version = WorkerDeploymentVersion(
                deployment_name=worker_config_obj.task_queue,
                build_id=f"{config.worker.worker_name}-{worker_config_obj.task_queue}-{uuid4().hex}",
            )
            worker_kwargs["deployment_config"] = WorkerDeploymentConfig(
                version=worker_deployment_version,
                use_worker_versioning=False,
            )
            if is_main_worker:
                synthetic_deployment_version = (
                    worker_deployment_version.deployment_name,
                    worker_deployment_version.build_id,
                )
                for workflow_type in all_workflows:
                    workflow_config_registrations.enter_context(
                        _use_workflow_config_for_worker(
                            workflow_type,
                            config,
                            task_queue,
                            deployment_version_override=synthetic_deployment_version,
                        )
                    )
        try:
            workers.append(Worker(**worker_kwargs))
        except RuntimeError as e:
            log_if_sandbox_restriction_error(e, context="validation")
            raise

    poll_estimate = estimate_connection_polls(
        activity_groups,
        activity_polls_per_worker=config.worker.max_activity_task_pollers,
        workflow_polls=config.worker.max_workflow_task_pollers,
        connection_stream_limit=config.worker.connection_stream_limit,
    )
    if poll_warning := format_poll_warning(poll_estimate):
        logger.warning(
            "Worker poll count approaches the Temporal connection's stream limit",
            detail=poll_warning,
            total_polls=poll_estimate.total_polls,
            connection_stream_limit=poll_estimate.connection_stream_limit,
            threshold=poll_estimate.warning_threshold,
            headroom=poll_estimate.headroom,
            rate_limit_keys=poll_estimate.rate_limit_keys,
            activity_polls_per_worker=poll_estimate.activity_polls_per_worker,
            workflow_polls=poll_estimate.main_workflow_polls,
        )

    return workers, plugin_workflows


_GRAPH_PAYLOAD_VERSION = 3
# Graph analysis holds the GIL: running it in parallel only starves the workflow task threads.
_GRAPH_BUILD_CONCURRENCY = 1
_GRAPH_SUMMARY_CONCURRENCY = 4
_GRAPH_SUMMARY_REQUEST_TIMEOUT_S = 60.0
_GRAPH_SUMMARY_MAX_ATTEMPTS = 3
# A 429 carries the limiter's moving-window reset, so at worker startup — when every hit
# lands within a few seconds — retry-after is close to the window length itself. Waiting
# that out is the only way a workspace with more workflows than the per-minute allowance
# gets summaries for all of them; a shorter budget drops every request past the burst.
# Values far beyond one window (the daily limit's reset) are still not worth waiting for.
_GRAPH_SUMMARY_MAX_RETRY_DELAY_S = 65.0
# Budget for one workflow's summary, entered once its concurrency slot is held: every
# attempt plus the waits between them. The wait for a slot stays outside the budget, so a
# workflow queued behind several waves is not cancelled before it sends its first request.
_GRAPH_SUMMARY_LIFECYCLE_TIMEOUT_S = (
    _GRAPH_SUMMARY_MAX_ATTEMPTS * _GRAPH_SUMMARY_REQUEST_TIMEOUT_S
    + (_GRAPH_SUMMARY_MAX_ATTEMPTS - 1) * _GRAPH_SUMMARY_MAX_RETRY_DELAY_S
)
_GRAPH_SUMMARY_RETRYABLE_STATUSES = {
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
}
_GRAPH_SUMMARY_UNAVAILABLE_STATUSES = {HTTPStatus.NOT_FOUND, HTTPStatus.METHOD_NOT_ALLOWED}


def _summaries_enabled(config: AppConfig | None = None) -> bool:
    config = config if config is not None else resolve_worker_config(None)
    return config.worker.graph.graph_summarise_enabled and get_token_provider(app_config=config) is not None


async def _request_graph_summaries(
    *,
    base_url: str,
    workflow_identifier: str,
    workflow_registration_id: UUID,
    graph_data: "AtlasWireFormat",
    extra_nodes: list["FlatNode"] | None,
    http_client: Any,
) -> "SummaryResult":
    from mistralai.workflows.core.graph_summaries import (
        GraphSummaryOutput,
        SummaryResult,
        prepare_graph_summary_input,
    )

    summary_input = prepare_graph_summary_input(graph_data, extra_nodes)
    url = f"{base_url}/v1/workflows/{workflow_identifier}/graphs/{workflow_registration_id}/summaries"
    response = None
    for attempt in range(_GRAPH_SUMMARY_MAX_ATTEMPTS):
        request = http_client.build_request(
            "POST",
            url,
            json=summary_input.model_dump(mode="json"),
            timeout=_GRAPH_SUMMARY_REQUEST_TIMEOUT_S,
        )
        response = await http_client.send(request)
        if response.status_code in _GRAPH_SUMMARY_UNAVAILABLE_STATUSES:
            return SummaryResult(status="disabled", summaries={})
        if response.status_code not in _GRAPH_SUMMARY_RETRYABLE_STATUSES or attempt == _GRAPH_SUMMARY_MAX_ATTEMPTS - 1:
            break

        retry_after = response.headers.get("retry-after")
        try:
            retry_delay = float(retry_after) if retry_after is not None else 2**attempt
        except ValueError:
            retry_delay = 2**attempt
        if retry_delay > _GRAPH_SUMMARY_MAX_RETRY_DELAY_S:
            break
        await asyncio.sleep(max(0.0, retry_delay))

    assert response is not None
    response.raise_for_status()
    output = GraphSummaryOutput.model_validate(response.json())
    return SummaryResult(status="ready", summaries=output.summaries, workflow_summary=output.workflow_summary)


async def _upload_workflow_graphs(
    refs: list[WorkflowRegistrationRef],
    classes: list[ClassType],
    client: PrivateWorkerClient,
    config: AppConfig | None = None,
) -> None:
    config = config if config is not None else resolve_worker_config(None)
    # Deferred import: _graph pulls in ast/inspect/textwrap at module level, adding startup
    # cost to every worker process even when graph upload is disabled. Keep it lazy here.
    from mistralai.workflows.core._graph import build_graph_dynamically
    from mistralai.workflows.core.wire_format import FlatNode

    base_url = client.sdk_configuration.server_url.rstrip("/")
    http_client = client.sdk_configuration.async_client
    if http_client is None:
        logger.warning("Worker HTTP client unavailable, skipping graph upload")
        return

    summaries_enabled = _summaries_enabled(config)
    build_semaphore = asyncio.Semaphore(_GRAPH_BUILD_CONCURRENCY)
    summary_semaphore = asyncio.Semaphore(_GRAPH_SUMMARY_CONCURRENCY)

    async def _upload_one(ref: WorkflowRegistrationRef, cls: ClassType) -> None:
        if ref.workflow_registration_id is None:
            logger.warning("Workflow registration has no id, skipping graph upload", workflow=cls.__name__)
            return

        graph_data = None
        error: str | None = None
        views: list[dict[str, Any]] | None = None
        extra_nodes: list[FlatNode] | None = None
        async with build_semaphore:
            try:
                graph_data = await asyncio.to_thread(build_graph_dynamically, cls)
            except Exception as exc:
                error = type(exc).__name__
                logger.warning("Failed to build workflow graph", workflow=cls.__name__, **extract_error_context(exc))

            if graph_data is not None and config.worker.graph.dataflow_views_enabled:
                # Imported here, not at function top, so the kill-switch also avoids
                # paying libcst's import cost.
                from mistralai.workflows.core._dataflow import dataflow_only_nodes, expand_views

                # libcst parsing is CPU-bound and this task runs on the worker's loop
                # while Temporal pollers are starting; keep it off the loop.
                cf_dict = graph_data.to_dict(include_sources=True)
                views = await asyncio.to_thread(expand_views, cf_dict)
                # Built before summarising so the summariser can describe the nodes
                # that only exist in the data-flow views — transforms and fan-out
                # groups — which would otherwise fall back to a generic label.
                extra_nodes = [FlatNode(**n) for n in dataflow_only_nodes(cf_dict, views)]

        workflow_identifier = get_workflow_definition(cls).name
        if graph_data is not None and summaries_enabled:
            try:
                async with summary_semaphore:
                    async with asyncio.timeout(_GRAPH_SUMMARY_LIFECYCLE_TIMEOUT_S):
                        result = await _request_graph_summaries(
                            base_url=base_url,
                            workflow_identifier=workflow_identifier,
                            workflow_registration_id=ref.workflow_registration_id,
                            graph_data=graph_data,
                            extra_nodes=extra_nodes,
                            http_client=http_client,
                        )
                if result.summaries:
                    summaries = {nid: summary.to_dict() for nid, summary in result.summaries.items()}
                    # The control-flow payload keeps everything except the nodes
                    # only the data-flow views have; each data-flow view takes
                    # the subset matching its own nodes.
                    df_only_ids = {n.id for n in extra_nodes or ()}
                    graph_data.node_summaries = {k: v for k, v in summaries.items() if k not in df_only_ids}
                    if views is not None:
                        from mistralai.workflows.core._dataflow import attach_summaries

                        views[0]["node_summaries"] = graph_data.node_summaries
                        attach_summaries(views[1:], summaries)
                if result.workflow_summary is not None:
                    graph_data.workflow_summary = result.workflow_summary.to_dict()
                    for view in views or ():
                        view["workflow_summary"] = graph_data.workflow_summary
            except Exception as exc:
                error = f"Graph summary generation failed ({type(exc).__name__})"
                response = getattr(exc, "response", None)
                logger.warning(
                    "Failed to generate node summaries",
                    workflow=cls.__name__,
                    error_type=type(exc).__name__,
                    http_status=str(getattr(response, "status_code", "unknown")),
                )

        graph_payload = None
        if graph_data is not None and views is None:
            graph_payload = graph_data.to_dict()
        elif graph_data is not None and views is not None:
            # The analyser needs the source text; the graphs API must never see it.
            for view in views:
                view.pop("sources", None)
            # The control-flow view stays at the top level for clients that predate
            # `views`; `views` carries only the additional renderings, so the
            # control-flow graph is not serialised twice.
            control_flow, *extra_views = views
            graph_payload = {**control_flow, "views": extra_views}

        payload = {
            "workflow_registration_id": str(ref.workflow_registration_id),
            "version": _GRAPH_PAYLOAD_VERSION,
            "graph_data": graph_payload,
            "error": error,
        }

        try:
            url = f"{base_url}/v1/workflows/{workflow_identifier}/graphs"
            request = http_client.build_request("POST", url, json=payload)
            response = await http_client.send(request)
            response.raise_for_status()
        except Exception as exc:
            logger.warning("Failed to upload workflow graph", workflow=cls.__name__, **extract_error_context(exc))

    await asyncio.gather(*[_upload_one(ref, cls) for ref, cls in zip(refs, classes)])


async def _safe_upload_workflow_graphs(
    refs: list[WorkflowRegistrationRef],
    classes: list[ClassType],
    client: PrivateWorkerClient,
    config: AppConfig | None = None,
) -> None:
    # Runs as a sibling task inside the worker's TaskGroup. Graph upload is best-effort
    # metadata, so swallow every exception here: an unhandled error would otherwise cancel
    # the TaskGroup and crash the worker.
    try:
        await _upload_workflow_graphs(refs=refs, classes=classes, client=client, config=config)
    except Exception as exc:
        logger.warning("Workflow graph upload failed", **extract_error_context(exc))


def _check_payload_encryption_requirement(config: AppConfig, required: PayloadEncryptionLevel) -> None:
    configured = config.worker.payload_encryption_level
    if configured.satisfies(required):
        return
    reason = (
        f"The server requires payload encryption mode '{required}' or stronger, but this worker is "
        f"configured with '{configured}'. Set TEMPORAL_PAYLOAD_ENCRYPTION__MODE={required} and "
        "TEMPORAL_PAYLOAD_ENCRYPTION__MAIN_KEY."
    )
    # The worker's terminal-error report only names the error, so the remediation is logged here.
    logger.error("Payload encryption requirement not met", reason=reason)
    raise WorkflowsException(
        code=ErrorCode.WORKER_PAYLOAD_ENCRYPTION_REQUIRED,
        message=reason,
    )


def _api_key_hint(api_key: SecretStr | None) -> str:
    if api_key is None:
        return "<not set>"
    value = api_key.get_secret_value()
    return f"...{value[-4:]}" if len(value) >= 4 else "<not set>"


def _log_authentication_failure(exc: WorkflowsException, config: AppConfig) -> None:
    error_context = extract_error_context(exc)
    error_context["http_status"] = exc.status.value
    if str(exc.code) == ErrorCode.TEMPORAL_CONNECTION_ERROR and config.temporal.api_key:
        logger.error(
            "Authentication failed. Check your TEMPORAL_API_KEY.",
            api_key_hint=_api_key_hint(config.temporal.api_key),
            **error_context,
        )
        return
    if config.common.mistral_sa_token_path:
        logger.error(
            "Authentication failed. Check the service-account token.",
            sa_token_path=config.common.mistral_sa_token_path,
            **error_context,
        )
        return
    logger.error(
        "Authentication failed. Check your MISTRAL_API_KEY.",
        api_key_hint=_api_key_hint(config.common.mistral_api_key),
        **error_context,
    )


@contextmanager
def _report_worker_errors(
    *,
    config: AppConfig,
    exit_on_terminal_error: bool,
    unexpected_error_message: str,
) -> Iterator[None]:
    try:
        yield
    except WorkflowsException as exc:
        if exc.status == HTTPStatus.UNAUTHORIZED:
            _log_authentication_failure(exc, config)
            if exit_on_terminal_error:
                raise SystemExit(1) from None
            raise
        label = exc.terminal_label()
        if label:
            ctx = extract_error_context(exc)
            logger.error(label, api_error_code=ctx.get("api_error_code"), http_status=ctx.get("http_status"))
            if exit_on_terminal_error:
                raise SystemExit(1) from None
        raise

    except Exception as exc:
        logger.error(unexpected_error_message, **extract_error_context(exc))
        raise


# Stop requests of the attached run_worker calls in this process. The first call installs _on_sigterm; the last
# one to leave puts SIG_DFL back.
_sigterm_stop_requests: list[Callable[[], None]] = []


def _on_sigterm(_signum: int, _frame: FrameType | None) -> None:
    for request_stop in list(_sigterm_stop_requests):
        request_stop()


def _reset_sigterm_in_fork_child() -> None:
    # A forked child (multiprocessing, a subprocess helper) runs no worker. With _on_sigterm it would ignore SIGTERM,
    # so Pool.terminate() would hang.
    _sigterm_stop_requests.clear()
    if signal.getsignal(signal.SIGTERM) is _on_sigterm:
        signal.signal(signal.SIGTERM, signal.SIG_DFL)


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_sigterm_in_fork_child)


@contextmanager
def _sigterm_requests_stop(*, enabled: bool) -> Iterator[asyncio.Event | None]:
    """Yield an event that SIGTERM sets, the way asyncio.Runner handles SIGINT, or None if SIGTERM is not taken.

    SIGTERM is taken only from the main thread and only while nobody else owns it: the handler is still SIG_DFL, or
    it is already ours because another run_worker in this process installed it.
    """
    current_handler = signal.getsignal(signal.SIGTERM)
    if not (
        enabled
        and threading.current_thread() is threading.main_thread()
        and (current_handler is signal.SIG_DFL or current_handler is _on_sigterm)
    ):
        yield None
        return

    loop = asyncio.get_running_loop()
    stop_requested = asyncio.Event()

    def set_stop_requested() -> None:
        # Later SIGTERMs are ignored. The handler stays installed until run_worker returns, so they cannot kill the
        # drain or the telemetry flush.
        if stop_requested.is_set():
            return
        logger.info("Received SIGTERM, stopping worker")
        stop_requested.set()

    def request_stop() -> None:
        # Runs in a signal handler: call_soon_threadsafe is safe there and wakes a loop blocked in select().
        loop.call_soon_threadsafe(set_stop_requested)

    # Registered before the install and removed after the restore, so _on_sigterm never runs with an empty registry.
    _sigterm_stop_requests.append(request_stop)
    installed = True
    if current_handler is signal.SIG_DFL:
        try:
            signal.signal(signal.SIGTERM, _on_sigterm)
        except ValueError:
            # Like asyncio.Runner: an embedded interpreter can refuse signal handlers even in the main thread.
            installed = False
    if not installed:
        _sigterm_stop_requests.remove(request_stop)
        yield None
        return

    try:
        yield stop_requested
    finally:
        # A handler the caller installed meanwhile stays.
        if _sigterm_stop_requests == [request_stop] and signal.getsignal(signal.SIGTERM) is _on_sigterm:
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
        _sigterm_stop_requests.remove(request_stop)


@asynccontextmanager
async def _stop_workers_when_requested(
    stop_requested: asyncio.Event | None, workers: Sequence[Worker], health_server: HealthServer | None
) -> AsyncIterator[None]:
    if stop_requested is None:
        yield
        return

    async def stop() -> None:
        await stop_requested.wait()
        # shutdown() instead of a cancel of run(), because temporalio documents that a cancel can also cancel the
        # shutdown.
        await asyncio.gather(*[worker.shutdown() for worker in workers])
        if health_server is not None:
            await asyncio.get_running_loop().run_in_executor(None, health_server.shutdown)

    stop_task = asyncio.create_task(stop())
    try:
        yield
    finally:
        # The body's cleanup has already stopped every worker. A worker whose run() was cancelled during its
        # shutdown never reports the shutdown complete, so waiting for the stop task could hang.
        stop_task.cancel()


async def _run_worker(
    workflows: List[ClassType],
    config: AppConfig | None = None,
    *,
    exit_on_terminal_error: bool = True,
    stop_requested: asyncio.Event | None = None,
) -> None:
    config = config if config is not None else resolve_worker_config(None)
    with use_config(config):
        await _run_worker_with_config(
            workflows, config, exit_on_terminal_error=exit_on_terminal_error, stop_requested=stop_requested
        )


async def _run_worker_with_config(
    workflows: List[ClassType],
    config: AppConfig,
    *,
    exit_on_terminal_error: bool,
    stop_requested: asyncio.Event | None,
) -> None:
    with (
        _report_worker_errors(
            config=config,
            exit_on_terminal_error=exit_on_terminal_error,
            unexpected_error_message="Worker stopped due to unhandled exception",
        ),
        ExitStack() as workflow_config_registrations,
    ):
        logger.info("Worker config", config=config.common.model_dump())
        config.validate_for_worker_startup()
        deployment_name = config.get_effective_task_queue()
        worker_name = config.worker.worker_name
        deployment_location = config.worker.deployment_location

        # Build the worker's runtime + MetricBuffer, drained by pump_runtime_metrics below.
        runtime, metric_buffer = build_runtime()

        logger.info(
            "Deployment location",
            location_type=deployment_location.location_type,
            k8s_cluster=deployment_location.k8s_cluster,
            k8s_namespace=deployment_location.k8s_namespace,
        )

        token_provider = get_token_provider(app_config=config)
        worker_client = get_worker_client(
            base_url=config.worker.server_url,
            timeout=config.http.timeout,
            token_provider=token_provider,
            headers=get_deployment_headers(),
        )
        # Its own connection pool, so event traffic filling the shared one can't starve the heartbeat.
        heartbeat_client = get_worker_client(
            base_url=config.worker.server_url,
            timeout=config.http.timeout,
            token_provider=token_provider,
            headers=get_deployment_headers(),
        )

        # Initialize OpenTelemetry tracing for the worker component
        meter_provider, tracer_provider, logger_provider, runtime_metrics_meter_provider = init_tracing(
            "worker", deployment_name=deployment_name, worker_name=worker_name
        )
        if meter_provider and tracer_provider:
            logger.info("OpenTelemetry tracing initialized for worker")

        # Always use custom payload converter and codec for context propagation
        # Offloading and encryption are controlled by their respective configs
        payload_converter: Type[PayloadConverter] = MistralWorkflowsPayloadConverter
        payload_encoding = _build_worker_payload_encoding(config.worker)

        # Order matters: ContextHandler first (unwraps context), ExecutionRegistration before
        # Event (sets the token Event needs). Trace-context wraps both so their internal local
        # activities are traced; span-recording is innermost to serialize unwrapped/restored args.
        extra_interceptors: List[Interceptor] = [
            ContextHandlerInterceptor(),
            *get_trace_context_interceptors(),
            ExecutionRegistrationInterceptor(),
            EventInterceptor(),
            ActivityInOutOffloadingInterceptor(
                offloader=FieldsOffloader(offloading_config=config.worker.activity_attributes_offloading)
            ),
            *get_span_recording_interceptors(),
        ]

        temporal_client = await create_temporal_client(
            namespace=config.temporal.namespace,
            runtime=runtime,
            payload_codec=payload_encoding.payload_codec,
            payload_converter=payload_converter,
            extra_interceptors=extra_interceptors,
            add_tracing_interceptors=False,
            failure_converter=payload_encoding.failure_converter,
        )
        # Publish the connection whose credentials refresh_temporal_credentials keeps current, so DI-provided
        # clients (plugin activities) ride it instead of opening an unrefreshed parallel connection.
        set_worker_service_client(temporal_client.service_client)

        # Log installed contributions
        plugins = list_plugins()
        logger.info(
            f"Discovered {len(plugins)} package(s) at mistralai.workflows.plugins",
            plugins=plugins,
        )

        # Initialize dependency injector
        dependency_injector = DependencyInjector.get_singleton_instance()

        # Create Temporal workers (also discovers plugin-contributed workflows)
        workers, plugin_workflows = _create_temporal_workers(
            temporal_client=temporal_client,
            workflows=workflows,
            config=config,
            task_queue=deployment_name,
            workflow_config_registrations=workflow_config_registrations,
        )

        # Get workflow definitions for custom workflows + internal workflows
        workflow_definitions = _get_workflow_definitions(workflows, deployment_name)
        workflow_definitions += _get_workflow_definitions(_get_parallel_execution_workflows(workflows), deployment_name)
        if plugin_workflows:
            workflow_definitions += _get_workflow_definitions(plugin_workflows, deployment_name)

        # Build deployment location from config
        location_proto = DeploymentLocation(
            location_type=deployment_location.location_type,
            k8s_cluster=deployment_location.k8s_cluster,
            k8s_namespace=deployment_location.k8s_namespace,
        )

        # Register workflows to Workflows API
        response = await _register_workflow_specs(
            worker_client,
            workflow_definitions,
            deployment_name=deployment_name,
            worker_name=worker_name,
            deployment_location=location_proto,
            payload_encryption_mode=config.worker.payload_encryption_level,
        )
        if response.has_conflicts and not config.worker.allow_multiple_workers:
            raise ValueError(
                "Some workflows are already registered by another worker. "
                "Use a different DEPLOYMENT_NAME or set ALLOW_MULTIPLE_WORKERS=True."
            )
        set_worker_registrations(build_worker_registrations(workflow_definitions, response.workflow_registration_refs))
        event_route_publisher = EventRoutePublisher(worker_client)
        async with (
            worker_client,
            heartbeat_client,
            share_worker_client(worker_client),
            asyncio.TaskGroup() as tg,
            dependency_injector.with_dependencies(),
            EventContext(
                event_route_publisher,
                payload_encoder=payload_encoding.event_payload_encoder,
                custom_event_payload_encoder=payload_encoding.custom_event_payload_encoder,
                worker_client=worker_client,
                route_token_manager=event_route_publisher.route_token_manager,
            ),
        ):
            register_task = tg.create_task(
                _worker_heartbeat(
                    worker_client=heartbeat_client,
                    workflow_definitions=workflow_definitions,
                    workflow_registration_refs=response.workflow_registration_refs,
                    interval=10,
                    deployment_name=deployment_name,
                    worker_name=worker_name,
                    deployment_location=location_proto,
                    payload_encryption_mode=config.worker.payload_encryption_level,
                )
            )

            # Auto-register as current version if enabled (for manual/local deployments)
            auto_register_task = None
            if (
                config.worker.versioning.auto_register_as_current
                and config.worker.versioning.enabled
                and config.worker.versioning.deployment_name
                and config.worker.versioning.build_id
            ):
                auto_register_task = tg.create_task(
                    _auto_register_as_current_version(
                        temporal_client=temporal_client,
                        namespace=config.temporal.namespace,
                        deployment_name=config.worker.versioning.deployment_name,
                        build_id=config.worker.versioning.build_id,
                    )
                )

            # Graph + LLM summary generation is non-critical metadata and may retry on
            # transient 429s, so it runs as a background task: the Temporal worker starts
            # polling immediately instead of waiting on graph upload to finish.
            graph_upload_task = None
            if config.worker.graph.upload_graph:
                # Refs are returned in submission order; internal workflows
                # (ParallelExecutionWorkflow, plugin workflows) are appended after
                # user workflows, so [:len(workflows)] excludes them.
                refs = response.workflow_registration_refs
                if len(refs) >= len(workflows):
                    graph_upload_task = tg.create_task(
                        _safe_upload_workflow_graphs(
                            refs=refs[: len(workflows)],
                            classes=workflows,
                            client=worker_client,
                            config=config,
                        )
                    )
                else:
                    logger.warning(
                        "Fewer registration refs than workflows; skipping graph upload",
                        expected=len(workflows),
                        got=len(refs),
                    )

            token_refresh_task = tg.create_task(refresh_temporal_credentials(temporal_client.service_client))

            # Drain the runtime MetricBuffer and re-emit through its dedicated provider (worker_id-free
            # resource). Both are present only on the worker with metrics enabled.
            pump_task = None
            if metric_buffer is not None and runtime_metrics_meter_provider is not None:
                pump_task = tg.create_task(
                    pump_runtime_metrics(
                        metric_buffer,
                        runtime_metrics_meter_provider.get_meter("mistralai.workflows.temporal_runtime"),
                        interval_s=config.common.temporal_runtime_metrics_drain_interval_s,
                        buffer_size=config.common.temporal_runtime_metrics_buffer_size,
                    )
                )

            # A SIGTERM during startup skips polling. The cleanup below still runs, so run_worker returns None.
            polled_workers = workers
            health_server = None
            if stop_requested is not None and stop_requested.is_set():
                logger.info("SIGTERM received during startup, the worker does not start polling")
                polled_workers = []
            else:
                logger.info(
                    "Starting Temporal worker",
                    deployment_name=deployment_name,
                    namespace=config.temporal.namespace,
                    location_type=deployment_location.location_type,
                )
                if config.worker.health_server_port:
                    health_server = HealthServer(config.worker.health_server_host, config.worker.health_server_port)
            async with _stop_workers_when_requested(stop_requested, polled_workers, health_server):
                workers_and_health_server = (
                    polled_workers + [health_server] if health_server is not None else polled_workers
                )
                runs = [asyncio.create_task(worker.run()) for worker in workers_and_health_server]
                try:
                    await asyncio.gather(*runs)
                finally:
                    logger.info("Worker shutting down, cleaning up resources")
                    set_worker_service_client(None)
                    set_worker_registrations({})
                    register_task.cancel()
                    if auto_register_task:
                        auto_register_task.cancel()
                    if graph_upload_task:
                        graph_upload_task.cancel()
                    token_refresh_task.cancel()
                    try:
                        await register_task
                    except asyncio.CancelledError:
                        pass
                    if auto_register_task:
                        try:
                            await auto_register_task
                        except asyncio.CancelledError:
                            pass
                    if graph_upload_task:
                        try:
                            await graph_upload_task
                        except asyncio.CancelledError:
                            pass
                    try:
                        await token_refresh_task
                    except asyncio.CancelledError:
                        pass
                    # Stop the workers first (core stops emitting), then final-drain the pump so teardown metrics
                    # are captured before the provider is shut down.
                    # Wait only for workers still running: one whose run() was cancelled during its shutdown never
                    # reports the shutdown complete. zip stops at the last Temporal worker, before the health server.
                    await asyncio.gather(
                        *[worker.shutdown() for worker, run in zip(polled_workers, runs) if not run.done()]
                    )
                    if pump_task:
                        pump_task.cancel()
                        try:
                            await pump_task
                        except asyncio.CancelledError:
                            pass
                    telemetry_deadline = time.monotonic() + _TELEMETRY_SHUTDOWN_TIMEOUT_SECONDS
                    if runtime_metrics_meter_provider is not None:
                        _flush_runtime_metrics(
                            runtime_metrics_meter_provider,
                            shared=runtime_metrics_meter_provider is meter_provider,
                            deadline=telemetry_deadline,
                        )
                    if health_server is not None:
                        await asyncio.get_running_loop().run_in_executor(None, health_server.shutdown)
                    if logger_provider is not None:
                        _shutdown_logs(logger_provider, deadline=telemetry_deadline)
                    logger.info("Worker shutdown complete")


# OTLP HTTP exporters wait out their 10 s timeout on an endpoint that does not answer. This caps the total
# wait on metrics and logs at stop.
_TELEMETRY_SHUTDOWN_TIMEOUT_SECONDS = 3.0


def _flush_runtime_metrics(provider: MeterProvider, *, shared: bool, deadline: float) -> None:
    if shared:
        # The shared local provider exports to the console and lives on after the worker.
        provider.force_flush()
        return
    # force_flush cannot be bounded: the OTLP HTTP exporter ignores its timeout. shutdown stops waiting at the deadline.
    provider.shutdown(timeout_millis=_remaining_millis(deadline))


def _shutdown_logs(provider: LoggerProvider, *, deadline: float) -> None:
    # LoggerProvider.shutdown takes no timeout. Run it in a daemon thread and stop waiting at the deadline.
    shutdown = threading.Thread(target=provider.shutdown, name="otel-log-shutdown", daemon=True)
    shutdown.start()
    wait_s = _remaining_millis(deadline) / 1000
    shutdown.join(wait_s)
    if shutdown.is_alive():
        logger.warning("OpenTelemetry logs not exported before worker stop; pending logs dropped", timeout_s=wait_s)


def _remaining_millis(deadline: float) -> float:
    return max(0.0, (deadline - time.monotonic()) * 1000)


async def run_worker(
    workflows: List[ClassType],
    detach: bool = False,
    api_key: str | None = None,
    namespace: str | None = None,
    enable_config_discovery: bool | None = None,
    *,
    config: AppConfig | None = None,
) -> asyncio.Task | None:
    """
    Initialize and run a Temporal worker with the specified workflows.

    Args:
        workflows: List of workflow classes to register with the worker
        detach: If True, run the worker in a detached thread
        api_key: Optional API key for the Mistral API authentication (sent as Bearer token)
        namespace: Optional namespace to use for the worker
        config: Explicit SDK configuration. When omitted, environment variables are resolved at call time.

    When attached (``detach=False``) and no other ``SIGTERM`` handler is installed, ``SIGTERM`` stops the worker:
    it stops polling, waits up to ``graceful_shutdown_timeout_seconds`` for running activities, cancels the rest,
    and returns ``None``. A ``SIGTERM`` during startup lets startup finish, then returns ``None`` without polling.
    Several attached ``run_worker`` calls in one process share the handler, and one ``SIGTERM`` stops them all.
    """
    uses_legacy_config = config is None
    resolved_config = resolve_worker_config(config)
    original_config = resolved_config.model_copy(deep=True) if uses_legacy_config else None
    setup_default_logging(resolved_config)
    log_configuration(resolved_config)

    def _restore_legacy_config() -> None:
        if original_config is not None:
            resolved_config.__dict__.update(original_config.__dict__)

    with use_config(resolved_config), _sigterm_requests_stop(enabled=not detach) as stop_requested:
        # Every later read keeps the last good value, so only this first read needs the retry.
        try:
            with _report_worker_errors(
                config=resolved_config,
                exit_on_terminal_error=not detach,
                unexpected_error_message="Failed to read worker header files",
            ):
                await read_credential_at_startup(lambda: get_deployment_headers(resolved_config.worker), "header files")
        except BaseException:
            _restore_legacy_config()
            raise
        enable_config_discovery = (
            enable_config_discovery
            if enable_config_discovery is not None
            else resolved_config.worker.enable_config_discovery
        )
        if not enable_config_discovery:
            warnings.warn("Disabling automatic config discovery")
            if namespace is not None:
                resolved_config.temporal.namespace = namespace
            if api_key is not None:
                resolved_config.common.mistral_api_key = SecretStr(api_key)
        else:
            if namespace is not None:
                warnings.warn("Namespace provided but config discovery is enabled. Ignoring namespace.")
            try:
                with _report_worker_errors(
                    config=resolved_config,
                    exit_on_terminal_error=not detach,
                    unexpected_error_message="Worker config discovery failed",
                ):
                    runtime_config = await config_discovery.apply_worker_runtime_config(config=resolved_config)
                    if runtime_config is not None:
                        _check_payload_encryption_requirement(
                            resolved_config, runtime_config.required_payload_encryption_mode
                        )
            except BaseException:
                _restore_legacy_config()
                raise
        if detach:
            task = asyncio.create_task(_run_worker(workflows, resolved_config, exit_on_terminal_error=False))
            task.add_done_callback(lambda _task: _restore_legacy_config())
            return task

        try:
            await _run_worker(workflows, resolved_config, stop_requested=stop_requested)
            return None
        finally:
            _restore_legacy_config()
