import asyncio
import traceback
import warnings
from collections import defaultdict
from http import HTTPStatus
from typing import Any, Callable, DefaultDict, List, Type
from uuid import uuid4

import structlog
import temporalio.api.workflowservice.v1 as wsv1
import tenacity
from pydantic import BaseModel, SecretStr
from temporalio.client import Client as TemporalClient
from temporalio.client import Interceptor
from temporalio.common import VersioningBehavior, WorkerDeploymentVersion
from temporalio.converter import PayloadCodec, PayloadConverter
from temporalio.worker import PollerBehaviorSimpleMaximum, Worker, WorkerDeploymentConfig
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner

from mistralai.workflows.client import translate_model
from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core._events.event_interceptor import EventInterceptor
from mistralai.workflows.core.activity import activity, get_all_temporal_activities
from mistralai.workflows.core.config import config_discovery
from mistralai.workflows.core.config.config import AppConfig, config
from mistralai.workflows.core.definition.workflow_definition import (
    get_workflow_definition,
)
from mistralai.workflows.core.dependencies.dependency_injector import DependencyInjector
from mistralai.workflows.core.encoding.fields_offloader import FieldsOffloader
from mistralai.workflows.core.execution.concurrency import ParallelExecutionWorkflow
from mistralai.workflows.core.execution.sticky_session.get_sticky_worker_session import (
    GET_STICKY_WORKER_SESSION_ACTIVITY_NAME,
)
from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import (
    StickyWorkerSession,
    check_activity_is_sticky_to_worker,
)
from mistralai.workflows.core.rate_limiting.rate_limit import get_rate_limit
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
from mistralai.workflows.core.temporal.temporal_client import create_temporal_client
from mistralai.workflows.core.tracing.init_tracing import init_tracing
from mistralai.workflows.core.utils.health_server import HealthServer
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.core.workflow import ClassType
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.models import WorkflowSpecWithTaskQueue
from mistralai.workflows.plugins._discovery import (
    collect_plugin_interceptors,
    list_plugins,
)
from mistralai.workflows.protocol.v1.workflow import (
    DeploymentLocation,
    WorkflowRegistrationRef,
    WorkflowSpecsRegisterResponse,
)
from mistralai.workflows.worker_client import models as wc_models
from mistralai.workflows.worker_client.errors.sdkerror import SDKError
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

logger = structlog.get_logger(__name__)


class WorkerConfig(BaseModel):
    task_queue: str
    max_task_queue_activities_per_second: float | None = None

    def __hash__(self) -> int:
        return hash((self.task_queue, self.max_task_queue_activities_per_second))


@tenacity.retry(
    # Retry on transient errors (502, 503, 504)
    retry=tenacity.retry_if_exception(
        lambda exc: (
            isinstance(exc, WorkflowsException)
            and exc.status
            in [
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.GATEWAY_TIMEOUT,
                HTTPStatus.SERVICE_UNAVAILABLE,
            ]
        )
    ),
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
    deployment_name: str | None = None,
    worker_name: str | None = None,
    deployment_location: DeploymentLocation | None = None,
) -> WorkflowSpecsRegisterResponse:
    try:
        result = await worker_client.register_workflow_definitions_async(
            definitions=[translate_model(wc_models.WorkflowSpecWithTaskQueue, d) for d in workflow_definitions],
            deployment_name=deployment_name,
            worker_name=worker_name,
            deployment_location=translate_model(wc_models.DeploymentLocation, deployment_location)
            if deployment_location
            else None,
        )
        return translate_model(WorkflowSpecsRegisterResponse, result)
    except Exception as exc:
        raise WorkflowsException.from_api_client_error(
            exc, message="Failed to register workflow specs", code=ErrorCode.POST_WORKFLOWS_REGISTER_ERROR
        ) from exc


async def _worker_heartbeat(
    worker_client: PrivateWorkerClient,
    workflow_definitions: list[WorkflowSpecWithTaskQueue],
    workflow_registration_refs: list[WorkflowRegistrationRef],
    interval: int,
    deployment_name: str | None = None,
    worker_name: str | None = None,
    deployment_location: DeploymentLocation | None = None,
) -> None:
    refs = list(workflow_registration_refs)

    heartbeat_endpoint_available = True

    async def _heartbeat_succeeds() -> bool:
        nonlocal heartbeat_endpoint_available
        if not heartbeat_endpoint_available:
            return False
        try:
            await worker_client.heartbeat_async(
                workflow_registration_refs=[
                    translate_model(wc_models.WorkflowRegistrationRefInput, ref) for ref in refs
                ],
                deployment_name=deployment_name,
                worker_name=worker_name,
            )
            return True
        except Exception as exc:
            if isinstance(exc, SDKError) and exc.status_code in (404, 405):
                logger.warning(
                    "Heartbeat endpoint not available, disabling heartbeat and falling back to full registration",
                    error=traceback.format_exc(),
                )
                heartbeat_endpoint_available = False
            else:
                logger.warning("Heartbeat failed, falling back to full registration", error=traceback.format_exc())
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
                )
                refs = [
                    WorkflowRegistrationRef(
                        workflow_id=ref.workflow_id,
                        workflow_registration_id=ref.workflow_registration_id,
                    )
                    for ref in response.workflow_registration_refs
                ]
            except Exception:
                logger.error("Full re-registration also failed", error=traceback.format_exc())
    except Exception:
        logger.error("Error in heartbeat task", error=traceback.format_exc())
        raise WorkflowsException(code=ErrorCode.WORKER_REGISTRATION_ERROR, message="Fail to heartbeat worker")


async def _auto_register_as_current_version(
    temporal_client: TemporalClient,
    namespace: str,
    deployment_name: str,
    build_id: str,
) -> None:
    """
    Auto-register worker as current version for manual/local deployments.

    Retries until successful, as the Worker Deployment may not exist yet when the worker first starts.
    Once registered successfully, the task completes.

    Args:
        temporal_client: Temporal client instance
        namespace: Temporal namespace
        deployment_name: Worker deployment name
        build_id: Build ID to set as current
    """
    retry_count = 0
    max_retries = 48  # 2 minutes worth of retries (2.5s intervals)

    while retry_count < max_retries:
        try:
            await asyncio.sleep(2.5)  # Wait 2.5s before each attempt

            set_request = wsv1.SetWorkerDeploymentCurrentVersionRequest(
                namespace=namespace,
                deployment_name=deployment_name,
                build_id=build_id,
            )
            await temporal_client.workflow_service.set_worker_deployment_current_version(set_request)

            logger.info(
                "Successfully auto-registered worker as current version",
                deployment_name=deployment_name,
                build_id=build_id,
                retry_count=retry_count,
            )
            return  # Success - exit the function

        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                logger.error(
                    "Failed to auto-register worker as current version after max retries",
                    error=str(e),
                    deployment_name=deployment_name,
                    build_id=build_id,
                    max_retries=max_retries,
                )
                return

            logger.debug(
                "Waiting for worker deployment to be available",
                deployment_name=deployment_name,
                build_id=build_id,
                retry_count=retry_count,
                max_retries=max_retries,
                error=str(e),
            )


def _get_workflow_definitions(workflows: list[ClassType], task_queue: str) -> List[WorkflowSpecWithTaskQueue]:
    workflow_definitions: List[WorkflowSpecWithTaskQueue] = []
    for workflow in workflows:
        workflow_def = get_workflow_definition(workflow)
        workflow_def_with_task_queue = WorkflowSpecWithTaskQueue.model_validate(
            {
                **workflow_def.model_dump(),
                "task_queue": task_queue,
            }
        )
        workflow_definitions.append(workflow_def_with_task_queue)
    return workflow_definitions


def _create_temporal_workers(
    temporal_client: TemporalClient,
    workflows: List[ClassType],
    config: AppConfig,
    task_queue: str,
) -> List[Worker]:
    all_workflows: List[Type] = [*workflows, ParallelExecutionWorkflow]

    # Collect worker interceptors from plugins
    plugin_interceptors = collect_plugin_interceptors(all_workflows)

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

    # Split activities into workers based on their needs
    # 1. Sticky activities go to a dedicated task queue
    # 2. Rate limited activities go to a dedicated task queue (one task queue per rate limit)
    activities_per_worker_config: DefaultDict[WorkerConfig, list[Callable]] = defaultdict(list)

    for act in all_activities:
        if check_activity_is_sticky_to_worker(act):  # 1.
            worker_config = WorkerConfig(task_queue=sticky_worker_session_task_queue)
        elif rate_limit := get_rate_limit(act):  # 2.
            max_task_queue_activities_per_second = (
                rate_limit.max_execution / rate_limit.time_window_in_sec
                # * config.temporal.temporal_frontend_num_task_queue_partitions
            )
            worker_config = WorkerConfig(
                task_queue=rate_limit.task_queue,
                max_task_queue_activities_per_second=max_task_queue_activities_per_second,
            )
        else:
            continue

        activities_per_worker_config[worker_config].append(act)

    # 3. We also register all acitvities on the main worker
    #    in order to be able to execute them as local activities
    #    see `run_activities_locally`.
    main_worker_config = WorkerConfig(task_queue=task_queue)
    activities_per_worker_config[main_worker_config] = all_activities

    versioning_cfg = config.worker.versioning
    main_task_queue = task_queue
    deployment_config: WorkerDeploymentConfig | None = None

    if versioning_cfg.enabled and versioning_cfg.deployment_name and versioning_cfg.build_id:
        if main_task_queue == "default":
            raise ValueError(
                "Versioned workers must not use the 'default' task queue. "
                "Temporal deployment versioning is task-queue-scoped: registering a versioned worker on 'default' "
                "permanently pins it and blocks all unversioned workers. "
                "Set DEPLOYMENT_NAME to a non-default value."
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
    for worker_config_obj, activities in activities_per_worker_config.items():
        is_main_worker = worker_config_obj.task_queue == main_task_queue
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
            worker_kwargs["deployment_config"] = WorkerDeploymentConfig(
                version=WorkerDeploymentVersion(
                    deployment_name=worker_config_obj.task_queue,
                    build_id=f"{config.worker.worker_name}-{worker_config_obj.task_queue}-{uuid4().hex}",
                ),
                use_worker_versioning=False,
            )
        try:
            workers.append(Worker(**worker_kwargs))
        except RuntimeError as e:
            log_if_sandbox_restriction_error(e, context="validation")
            raise
    return workers


async def _run_worker(workflows: List[ClassType]) -> None:
    try:
        config.validate_for_worker_startup()
        task_queue = config.get_effective_task_queue(raise_on_conflict=True)
        deployment_name = task_queue
        worker_name = config.worker.worker_name
        deployment_location = config.worker.deployment_location

        logger.info(
            "Deployment location",
            location_type=deployment_location.location_type,
            k8s_cluster=deployment_location.k8s_cluster,
            k8s_namespace=deployment_location.k8s_namespace,
        )

        api_key = config.common.mistral_api_key.get_secret_value() if config.common.mistral_api_key else None
        worker_client = get_worker_client(
            base_url=config.worker.server_url,
            api_key=api_key or None,
            headers=config.worker.mistral_api_headers,
        )

        # Initialize OpenTelemetry tracing for the worker component
        meter_provider, tracer_provider = init_tracing("worker")
        if meter_provider and tracer_provider:
            logger.info("OpenTelemetry tracing initialized for worker")

        # Always use custom payload converter and codec for context propagation
        # Offloading and encryption are controlled by their respective configs
        payload_converter: Type[PayloadConverter] = MistralWorkflowsPayloadConverter
        payload_codec: PayloadCodec = MistralWorkflowsPayloadCodec(
            payload_offloading_config=config.worker.temporal_payload_offloading,
            payload_encryption_config=config.worker.temporal_payload_encryption,
        )
        extra_interceptors: List[Interceptor] = [
            ContextHandlerInterceptor(),
            EventInterceptor(),
        ]

        extra_interceptors.append(
            ActivityInOutOffloadingInterceptor(
                offloader=FieldsOffloader(offloading_config=config.worker.activity_attributes_offloading)
            )
        )

        # Create Temporal client (with tracing interceptor if enabled)
        temporal_client = await create_temporal_client(
            namespace=config.temporal.namespace,
            payload_codec=payload_codec,
            payload_converter=payload_converter,
            extra_interceptors=extra_interceptors,
        )

        # Log installed contributions
        plugins = list_plugins()
        logger.info(
            f"Discovered {len(plugins)} package(s) at mistralai.workflows.plugins",
            plugins=plugins,
        )

        # Initialize dependency injector
        dependency_injector = DependencyInjector.get_singleton_instance()

        # Get workflow definitions for custom workflows + internal workflows
        workflow_definitions = _get_workflow_definitions(workflows, task_queue)
        workflow_definitions += _get_workflow_definitions([ParallelExecutionWorkflow], task_queue)

        # Create Temporal workers
        workers = _create_temporal_workers(
            temporal_client=temporal_client,
            workflows=workflows,
            config=config,
            task_queue=task_queue,
        )

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
        )
        if response.has_conflicts and not config.worker.allow_multiple_workers:
            raise ValueError(
                "Some workflows are already registered by another worker. "
                "Please use a custom task queue or set `ALLOW_MULTIPLE_WORKERS` to True"
            )
        async with (
            worker_client,
            asyncio.TaskGroup() as tg,
            dependency_injector.with_dependencies(),
            EventContext(
                worker_client.events,
                worker_client,
                events_api_version=config.worker.events_api_version,
            ),
        ):
            register_task = tg.create_task(
                _worker_heartbeat(
                    worker_client=worker_client,
                    workflow_definitions=workflow_definitions,
                    workflow_registration_refs=response.workflow_registration_refs,
                    interval=10,
                    deployment_name=deployment_name,
                    worker_name=worker_name,
                    deployment_location=location_proto,
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

            logger.info(
                "Starting Temporal worker",
                task_queue=task_queue,
                namespace=config.temporal.namespace,
                location_type=deployment_location.location_type,
            )
            health_server = (
                HealthServer(config.worker.health_server_host, config.worker.health_server_port)
                if config.worker.health_server_port
                else None
            )
            try:
                workers_and_health_server = workers + [health_server] if health_server is not None else workers
                await asyncio.gather(*[worker.run() for worker in workers_and_health_server])
            except Exception:
                logger.error("Error running worker", error=traceback.format_exc())
                raise
            finally:
                logger.info("Worker shutting down, cleaning up resources")
                register_task.cancel()
                if auto_register_task:
                    auto_register_task.cancel()
                try:
                    await register_task
                except asyncio.CancelledError:
                    pass
                if auto_register_task:
                    try:
                        await auto_register_task
                    except asyncio.CancelledError:
                        pass
                await asyncio.gather(*[worker.shutdown() for worker in workers])
                if health_server is not None:
                    await asyncio.get_running_loop().run_in_executor(None, health_server.shutdown)
                logger.info("Worker shutdown complete")

    except Exception:
        logger.error("Error in worker", error=traceback.format_exc())
        raise


async def run_worker(
    workflows: List[ClassType],
    detach: bool = False,
    api_key: str | None = None,
    namespace: str | None = None,
    enable_config_discovery: bool | None = None,
) -> asyncio.Task | None:
    """
    Initialize and run a Temporal worker with the specified workflows.

    Args:
        workflows: List of workflow classes to register with the worker
        detach: If True, run the worker in a detached thread
        api_key: Optional API key for the Mistral API authentication (sent as Bearer token)
        namespace: Optional namespace to use for the worker
    """
    original_config = config.model_copy(deep=True)

    def _revert_config() -> None:
        config.__dict__.update(original_config.__dict__)

    enable_config_discovery = (
        enable_config_discovery if enable_config_discovery is not None else config.worker.enable_config_discovery
    )
    if not enable_config_discovery:
        warnings.warn("Disabling automatic config discovery")
        if namespace is not None:
            config.temporal.namespace = namespace
        if api_key is not None:
            config.common.mistral_api_key = SecretStr(api_key)
    else:
        if namespace is not None:
            warnings.warn("Namespace provided but config discovery is enabled. Ignoring namespace.")
        await config_discovery.apply_worker_runtime_config(api_key)
    logger.info("Worker config", config=config.common.model_dump())
    if detach:
        task = asyncio.create_task(_run_worker(workflows))

        def _on_worker_done(_: asyncio.Task) -> None:
            _revert_config()

        task.add_done_callback(_on_worker_done)
        return task
    else:
        try:
            await _run_worker(workflows)
        finally:
            _revert_config()
        return None
