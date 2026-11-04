from __future__ import annotations

import asyncio
import contextlib
import logging
from collections.abc import Callable

import httpx
from pydantic import BaseModel, ConfigDict
from temporalio.api.enums.v1 import TaskQueueType
from temporalio.api.taskqueue.v1 import TaskQueue
from temporalio.api.workflowservice.v1 import DescribeTaskQueueRequest

import mistralai.workflows as workflows
from mistralai.client import Mistral
from mistralai.client.errors import SDKError
from mistralai.client.utils import BackoffStrategy, RetryConfig
from mistralai.vibe_agents.agents_client import AgentResponse, AgentsClient
from mistralai.vibe_agents.agents_client.api_models import AgentConfigurationRequest, SessionInputSchemas
from mistralai.vibe_agents.sdk.app import code_version, config, deployment, entrypoint
from mistralai.vibe_agents.sdk.app.deploy import PublishedConfig, published_config
from mistralai.vibe_agents.sdk.app.loader import AgentApp, declared_session_input_schemas, declared_subagent_policy
from mistralai.vibe_agents.sdk.app.worker import runner, usage_telemetry
from mistralai.vibe_agents.sdk.app.worker.studio_tracing import (
    StudioRunMode,
    configure_managed_studio_tracing,
    shutdown_studio_genai_tracing,
)
from mistralai.vibe_agents.sdk.transport import telemetry
from mistralai.vibe_agents.session_workflow.inputs import SubagentPolicy
from mistralai.workflows.client import get_mistral_client
from mistralai.workflows.core.config.config import config as workflow_config
from mistralai.workflows.core.temporal.temporal_client import create_temporal_client
from mistralai.workflows.protocol.v1.workflow import MANAGED_K8S_CLUSTER_SENTINEL, LocationType

logger = logging.getLogger(__name__)

# Well under the client's 30s default: announce sits between the banner and `await task`, so an
# unreachable control plane would otherwise stall every startup for half a minute.
_ANNOUNCE_TIMEOUT_SECONDS = 5.0
# A registration that sends the configuration makes the control plane call the Integrations API and the
# AI Registry first, each with its own timeout. A client timeout below their sum ends a registration
# that was about to succeed, and `serve` exits without trying again.
_ANNOUNCE_WITH_CONFIGURATION_TIMEOUT_SECONDS = 30.0
_REGISTER_POLL_INTERVAL_SECONDS = 0.5
_REGISTER_POLL_TIMEOUT_SECONDS = 60.0
# What an older control plane refuses as unknown when a registration sends its configuration.
_CONFIGURATION_FIELDS = frozenset(AgentConfigurationRequest.model_fields) | {
    "makes_own_sandbox",
    "code_version",
    "code_version_source",
}


class RegistrationError(Exception):
    """Raised when the control plane did not register this worker's agent binding."""

    def __init__(self, detail: str, *, control_plane_url: str) -> None:
        super().__init__(detail)
        self.control_plane_url = control_plane_url


class ServeReady(BaseModel):
    """What a caller can show once the worker polls and the agent is routable."""

    model_config = ConfigDict(frozen=True)

    agent_name: str
    deployment_name: str
    # The control plane sends the links of its environment; a managed worker does not register, so it has none.
    chat_url: str | None = None
    debug_url: str | None = None


async def serve(
    app: AgentApp,
    name: str | None = None,
    *,
    on_ready: Callable[[ServeReady], None] | None = None,
    send_config: bool = True,
) -> None:
    """Run the agent as a self-hosted worker and register it, until cancelled.

    ``on_ready`` is called once, after the worker polls its task queue and the agent is bound.
    With ``send_config``, the registration carries the agent's configuration, as `agents deploy` sends it.
    """
    # `--name` overrides the agent-defined name (the deployed/routable workflow name), matching deploy.
    agent_name = entrypoint.resolve_agent_name(app.name, name)
    workflow = runner.build_workflow(app.agent, name=agent_name, harness=app.harness)
    definition = workflows.get_workflow_definition(workflow)
    assert definition is not None
    # Bind before the worker starts, so a name conflict fails before the slow startup. Temporal keeps a
    # session's tasks on the queue until the worker polls it. Registration also tells the worker its queue.
    # TODO(AGE-1771): a worker that fails to start leaves the agent registered with no worker.
    registered = await _bind_agent(
        definition.name,
        declared_session_input_schemas(app.agent, app.harness),
        default_subagent_policy=declared_subagent_policy(app.agent),
        configuration=published_config(app) if send_config else None,
        # Hashing the project reads its files, so it runs off the event loop.
        code=await asyncio.to_thread(code_version.code_identity, app) if send_config else None,
    )
    if registered is not None:
        deployment_name = registered.deployment_name
    else:
        deployment_name = await deployment.resolve_worker_deployment_name(definition.name)
    runner.use_deployment_name(deployment_name)
    task: asyncio.Task[None] | None = None
    try:
        configure_managed_studio_tracing(run_mode=StudioRunMode.SERVE, redaction=app.agent._redaction())
        async with usage_telemetry.worker_usage_telemetry():
            try:
                # Run detached so startup can verify this task queue's Temporal poller before showing the banner.
                task = await workflows.run_worker([workflow], detach=True)
                assert task is not None
                await _await_ready(task, definition.name, deployment_name)
                if on_ready is not None:
                    on_ready(
                        ServeReady(
                            agent_name=definition.name,
                            deployment_name=deployment_name,
                            chat_url=registered.chat_url if registered is not None else None,
                            debug_url=registered.console_url if registered is not None else None,
                        )
                    )
                await task
            finally:
                if task is not None:
                    if not task.done():
                        task.cancel()
                    with contextlib.suppress(asyncio.CancelledError):
                        await task
    finally:
        shutdown_studio_genai_tracing()


def _workflows_client() -> Mistral:
    # The base get_mistral_client() ships without a retry policy, so a single transient transport blip
    # (ReadTimeout, connect drop, pooled-connection teardown) on a Workflows API call fails outright.
    # The agents SDK reaches that API over the public internet for serve registration, so it configures
    # connection-error retries here. Real API errors (4XX/5XX bodies, workflow status) are returned as
    # data, not retried away.
    #
    # Owned here rather than imported from nuage_v2.sdk._internal.workflows_client (its historical
    # home): serve runs on both runtimes, and its settings model already lives in this SDK, so the
    # Nuage copy was the last thing keeping the default serve path bound to the optional extra.
    settings = config.WorkflowsClientSettings()
    client = get_mistral_client()
    client.sdk_configuration.retry_config = RetryConfig(
        strategy="backoff",
        backoff=BackoffStrategy(
            initial_interval=settings.retry_initial_interval_ms,
            max_interval=settings.retry_max_interval_ms,
            exponent=settings.retry_exponent,
            max_elapsed_time=settings.retry_max_elapsed_time_ms,
        ),
        retry_connection_errors=True,
    )
    return client


async def _await_ready(task: asyncio.Task[None], workflow_name: str, deployment_name: str) -> None:
    client = _workflows_client()
    temporal_client = await create_temporal_client(namespace=workflow_config.temporal.namespace)
    workflow_registered = False
    timeout = asyncio.timeout(_REGISTER_POLL_TIMEOUT_SECONDS)
    try:
        async with timeout:
            while True:
                if task.done():
                    await task
                    raise RuntimeError("serve worker exited during startup")
                try:
                    if not workflow_registered:
                        await client.workflows.get_workflow_async(workflow_identifier=workflow_name)
                        workflow_registered = True
                except SDKError as exc:
                    if exc.raw_response.status_code != httpx.codes.NOT_FOUND:
                        raise
                else:
                    task_queue = await temporal_client.workflow_service.describe_task_queue(
                        DescribeTaskQueueRequest(
                            namespace=temporal_client.namespace,
                            task_queue=TaskQueue(name=deployment_name),
                            task_queue_type=TaskQueueType.TASK_QUEUE_TYPE_WORKFLOW,
                            report_pollers=True,
                        )
                    )
                    if any(poller.identity == temporal_client.identity for poller in task_queue.pollers):
                        return
                await asyncio.sleep(_REGISTER_POLL_INTERVAL_SECONDS)
    except TimeoutError:
        if not timeout.expired():
            raise
        raise RuntimeError("serve worker did not start polling within the startup timeout") from None


async def _bind_agent(
    agent_name: str,
    session_input_schemas: SessionInputSchemas,
    *,
    default_subagent_policy: SubagentPolicy | None = None,
    configuration: PublishedConfig | None = None,
    code: code_version.CodeIdentity | None = None,
) -> AgentResponse | None:
    if _is_managed_worker():
        # `agents deploy` already bound the agent. Images built before `run-worker` existed still start
        # the worker with `serve`, so this check stays until they are rebuilt.
        logger.warning(
            "`agents serve` is deprecated in a managed deployment. "
            'Change the Dockerfile CMD to ["agents", "run-worker"].'
        )
        return None
    return await _announce_agent(
        agent_name,
        session_input_schemas,
        default_subagent_policy=default_subagent_policy,
        configuration=configuration,
        code=code,
    )


def _is_managed_worker() -> bool:
    location = workflow_config.worker.deployment_location
    return location.location_type == LocationType.managed or location.k8s_cluster == MANAGED_K8S_CLUSTER_SENTINEL


async def _announce_agent(
    agent_name: str,
    session_input_schemas: SessionInputSchemas,
    *,
    default_subagent_policy: SubagentPolicy | None = None,
    configuration: PublishedConfig | None = None,
    code: code_version.CodeIdentity | None = None,
) -> AgentResponse:
    # Self-register with the control plane so the agent becomes routable. Registration is what binds
    # a task queue to the agent name, so a worker that cannot register receives no Session, ever.
    # Failing here beats polling an unbound queue behind a banner that says the agent is serving.
    # The control plane chooses the queue, unless the operator named one in DEPLOYMENT_NAME.
    explicit_deployment_name = deployment.explicit_deployment_name()
    settings = config.ControlPlaneSettings()
    try:
        async with AgentsClient(
            base_url=settings.deploy_control_plane_url,
            api_key=settings.api_key,
            timeout_seconds=(
                _ANNOUNCE_TIMEOUT_SECONDS if configuration is None else _ANNOUNCE_WITH_CONFIGURATION_TIMEOUT_SECONDS
            ),
        ) as client:
            # A start that sends the configuration stores a new snapshot of it, unless it declares the
            # same configuration and code version as the agent it joins. Once an agent stores one, the
            # control plane refuses a start without it until the agent is shut down.
            async def register(sent: PublishedConfig | dict[str, object]) -> AgentResponse:
                return await client.register_agent(
                    agent_name=agent_name,
                    workflow_name=agent_name,
                    deployment_name=explicit_deployment_name,
                    session_input_schemas=session_input_schemas,
                    default_subagent_policy=default_subagent_policy,
                    **sent,
                )

            if configuration is None:
                return await register({})
            # The worker runs the configuration from its code, sandbox included, so it says so with the
            # configuration it sends. A control plane that predates the code version ignores it.
            declared: dict[str, object] = {**configuration, "makes_own_sandbox": True}
            if code is not None:
                declared |= {"code_version": code.version, "code_version_source": code.source}
            try:
                return await register(declared)
            except httpx.HTTPStatusError as exc:
                # The configuration is shown with the agent, but the agent runs without it: a control
                # plane that refuses it must not keep the worker from serving. Any other failure
                # exits: the control plane may have stored it, and refuses a start without it then.
                if not _configuration_was_refused(exc):
                    raise
                logger.warning(
                    "The control plane did not store the agent's configuration (%s). "
                    "The agent is registered without it.",
                    _error_detail(exc),
                )
                return await register({})
    except httpx.HTTPStatusError as exc:
        await telemetry.agent_registration_failed(
            exc, agent_name=agent_name, workflow_name=agent_name, worker_hosting="self_hosted"
        )
        if exc.response.status_code == httpx.codes.CONFLICT:
            # A conflict has several causes, and the control plane names the one it found.
            raise RegistrationError(
                _conflict_detail(exc) or f"the name {agent_name} is already bound to another workflow or deployment",
                control_plane_url=settings.deploy_control_plane_url,
            ) from exc
        raise RegistrationError(_error_detail(exc), control_plane_url=settings.deploy_control_plane_url) from exc
    except Exception as exc:
        await telemetry.agent_registration_failed(
            exc, agent_name=agent_name, workflow_name=agent_name, worker_hosting="self_hosted"
        )
        raise RegistrationError(str(exc), control_plane_url=settings.deploy_control_plane_url) from exc


def _configuration_was_refused(exc: httpx.HTTPStatusError) -> bool:
    """Whether the control plane refused the configuration itself, so the agent can register without it.

    An older control plane refuses the configuration fields as unknown, and a newer SDK can send a value
    that a control plane does not know. Both are a 422 on a configuration field. A 5xx is no refusal:
    it is a service that storing the configuration needs, such as the AI Registry, being down, and
    the configuration the control plane already stores is still the right one.
    """
    if exc.response.status_code != httpx.codes.UNPROCESSABLE_ENTITY:
        return False
    with contextlib.suppress(Exception):
        errors = exc.response.json()["detail"]
        return bool(errors) and all(error["loc"][1] in _CONFIGURATION_FIELDS for error in errors)
    return False


def _conflict_detail(exc: httpx.HTTPStatusError) -> str | None:
    with contextlib.suppress(Exception):
        detail = exc.response.json()["detail"]
        if isinstance(detail, str) and detail:
            return detail
    return None


def _error_detail(exc: httpx.HTTPStatusError) -> str:
    # The control plane owns agent-name validation, so surface its own message (a 422 detail is a
    # list of per-field errors) instead of restating the rule here.
    with contextlib.suppress(Exception):
        detail = exc.response.json()["detail"]
        if isinstance(detail, list):
            return "; ".join(_field_error(item) for item in detail)
        return str(detail)
    return f"HTTP {exc.response.status_code}"


def _field_error(item: dict[str, object]) -> str:
    # Without the field, "Extra inputs are not permitted" leaves the user guessing what to remove.
    loc = item.get("loc")
    path = [str(part) for part in loc if part != "body"] if isinstance(loc, list) else []
    return f"{'.'.join(path)}: {item['msg']}" if path else str(item["msg"])
