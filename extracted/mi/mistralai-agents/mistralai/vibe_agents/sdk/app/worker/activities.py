"""Workflow activities for Agents SDK-authored Harness capabilities.

User callables, remote MCP requests, and connector requests execute in
activities. The Workflow thread retains only serializable configuration and
binding identities.
"""

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from datetime import timedelta
from typing import cast

import temporalio.activity
import temporalio.workflow
from pydantic import BaseModel, JsonValue
from temporalio.exceptions import ActivityError, ApplicationError

import mistralai.workflows as workflows
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.capabilities import (
    CallableBoundCapabilityHandler,
    CallableRegistration,
    CallbackRegistration,
    CapabilityBindingReference,
    CapabilityInvocation,
    CapabilityInvocationFailed,
    CapabilityInvocationResult,
    CapabilityRegistrationRegistry,
    DirectCapabilityCallableAdapter,
    McpSourceConfiguration,
    McpToolCallRequest,
    McpToolCallResult,
    MistralConnectorConfiguration,
    MistralConnectorDescriptor,
    ProvidedToolInvocation,
)
from mistralai.vibe.harness.runtime.capabilities.plugins.dynamic import (
    DynamicCapabilityExecutionRequest,
    DynamicCapabilityExecutor,
    DynamicCapabilityRequest,
    DynamicCapabilityResult,
)
from mistralai.vibe.harness.runtime.capabilities.plugins.mcp import McpCapabilityHost, McpSourceUnavailableError
from mistralai.vibe.harness.runtime.capabilities.plugins.mistral_connectors import (
    MistralConnectorHost,
    MistralConnectorNotConnectedError,
    MistralConnectorNotFoundError,
)
from mistralai.vibe.harness.runtime.hosts.mcp_http import McpHttpCapabilityHost
from mistralai.vibe.harness.runtime.hosts.workflows import (
    WorkflowActivityInvoker,
    WorkflowCapabilityActivityInvoker,
    execute_dynamic_capability,
)
from mistralai.vibe.harness.runtime.hosts.workflows.harness_definition import (
    WorkflowHarnessDefinition,
)
from mistralai.vibe.harness.runtime.hosts.workflows.mcp import (
    WorkflowMcpActivities,
    WorkflowMcpCapabilityHost,
    WorkflowMcpListToolsActivityRequest,
    WorkflowMcpListToolsActivityResult,
    non_retryable_mcp_list_error,
)
from mistralai.vibe_agents.sdk.app.worker import sandbox_access
from mistralai.vibe_agents.sdk.app.worker.heartbeat import heartbeat_while_running, stop_when_cancelled
from mistralai.vibe_agents.sdk.assembly import capabilities, connectors
from mistralai.vibe_agents.sdk.assembly.stateful import SavedStateTooLargeError, StateMap

_CAPABILITY_ACTIVITY_NAME = "agents_sdk_harness_capability"
_TOOL_ACTIVITY_NAME = "agents_sdk_harness_tool"
_SANDBOX_CAPABILITY_ACTIVITY_NAME = "agents_sdk_harness_sandbox_capability"
_MCP_LIST_ACTIVITY_NAME = "agents_sdk_harness_mcp_list_tools"
_DYNAMIC_ACTIVITY_NAME = "agents_sdk_harness_dynamic_capability"
_CONNECTORS_LIST_ACTIVITY_NAME = "agents_sdk_harness_connectors_list"
_CONNECTORS_APPLY_ACTIVITY_NAME = "agents_sdk_harness_connectors_apply"
# The ApplicationError type that carries a MistralConnectorNotFoundError out of the activity.
_CONNECTOR_NOT_FOUND_ERROR_TYPE = "MistralConnectorNotFoundError"
_CONNECTOR_NOT_CONNECTED_ERROR_TYPE = "MistralConnectorNotConnectedError"

# The heartbeat, not the timeout, detects a lost worker, so the timeout can leave room for long tools.
_TOOL_TIMEOUT = timedelta(minutes=30)
_TOOL_HEARTBEAT_TIMEOUT = timedelta(seconds=60)
# Our own deadline ends a long tool call with a clear error before Temporal's limit is reached.
_TOOL_DEADLINE = _TOOL_TIMEOUT - timedelta(minutes=1)

# Guards the switch to the sandbox-backed capability activity so a worker upgrade cannot
# re-order the activity schedule of a Session that started before Hooks could reach the sandbox.
_SANDBOX_CAPABILITY_ACTIVITY_PATCH = "agents-sdk-harness-sandbox-capability-v1"


class CapabilityActivityResult(BaseModel):
    """The result of one authored capability call, with the value the next call of its row starts from.

    ``state`` is ``None`` when the row has no state or the call left its value unchanged.
    """

    result: CapabilityInvocationResult
    state: JsonValue | None = None


@workflows.activity(name=_CAPABILITY_ACTIVITY_NAME)
async def invoke_agent_capability(
    definition: WorkflowHarnessDefinition,
    binding_id: str,
    invocation: CapabilityInvocation,
    sandbox_connection: sandbox_access.KoyebCapabilitySandbox | None = None,
    state: JsonValue | None = None,
) -> CapabilityActivityResult:
    """Rebuild and invoke one authored Tool or Hook outside the Workflow thread.

    ``state`` is the row's saved value in the Workflow; ``None`` means the value fixed at assembly.
    """

    return await _invoke_agent_capability(definition, binding_id, invocation, sandbox_connection, state)


@workflows.activity(
    name=_TOOL_ACTIVITY_NAME,
    retry_policy_max_attempts=1,
    start_to_close_timeout=_TOOL_TIMEOUT,
    heartbeat_timeout=_TOOL_HEARTBEAT_TIMEOUT,
)
async def invoke_agent_tool(
    definition: WorkflowHarnessDefinition,
    binding_id: str,
    invocation: CapabilityInvocation,
    state: JsonValue | None = None,
) -> CapabilityActivityResult:
    """Invoke an authored Tool whose side effects must not repeat after a lost execution."""

    # An interrupt stops the tool within about a second; the worker's heartbeat alone takes up to 48 s.
    async with heartbeat_while_running(), stop_when_cancelled():
        # Race the call against the deadline: a tool that ignores cancellation must not hold the call.
        call = asyncio.create_task(_invoke_agent_capability(definition, binding_id, invocation, None, state))
        try:
            done, _ = await asyncio.wait({call}, timeout=_TOOL_DEADLINE.total_seconds())
        except asyncio.CancelledError:
            _abandon(call)
            raise
        if call in done:
            return call.result()
        _abandon(call)
        # The call did not finish, so its value is not saved.
        return CapabilityActivityResult(result=_tool_timeout(invocation))


# Abandoned tool calls stay referenced until they end, so the event loop does not drop them early.
_ABANDONED_TOOL_CALLS: set[asyncio.Task[CapabilityActivityResult]] = set()


def _abandon(call: asyncio.Task[CapabilityActivityResult]) -> None:
    """Cancel a tool call without waiting for it, and discard its late result or error."""

    call.cancel()
    _ABANDONED_TOOL_CALLS.add(call)
    call.add_done_callback(_discard_late_outcome)


def _discard_late_outcome(call: asyncio.Task[CapabilityActivityResult]) -> None:
    _ABANDONED_TOOL_CALLS.discard(call)
    if not call.cancelled():
        call.exception()


def _tool_timeout(invocation: CapabilityInvocation) -> CapabilityInvocationFailed:
    # A synchronous tool keeps running in its thread: Python cannot stop a thread, so only the wait ends.
    minutes = _TOOL_DEADLINE.total_seconds() / 60
    tool = invocation.tool.qualified_name if isinstance(invocation, ProvidedToolInvocation) else None
    return CapabilityInvocationFailed(
        error=core_protocol.ProtocolError(
            code="tool_timeout",
            message=(
                f"The tool did not finish within {minutes:g} minutes, so the call was ended."
                " It may or may not have taken effect."
            ),
            retryable=False,
            details={"tool": tool, "outcome": "unknown"},
        )
    )


@workflows.activity(name=_SANDBOX_CAPABILITY_ACTIVITY_NAME, retry_policy_max_attempts=1)
async def invoke_sandbox_capability(
    definition: WorkflowHarnessDefinition,
    binding_id: str,
    invocation: CapabilityInvocation,
    sandbox_connection: sandbox_access.KoyebCapabilitySandbox,
    state: JsonValue | None = None,
) -> CapabilityActivityResult:
    """Invoke sandbox-backed authoring without retrying side effects."""

    return await _invoke_agent_capability(definition, binding_id, invocation, sandbox_connection, state)


async def _invoke_agent_capability(
    definition: WorkflowHarnessDefinition,
    binding_id: str,
    invocation: CapabilityInvocation,
    sandbox_connection: sandbox_access.KoyebCapabilitySandbox | None,
    state: JsonValue | None = None,
) -> CapabilityActivityResult:

    if definition.session_id is None:
        workflow_id = temporalio.activity.info().workflow_id
        if workflow_id is None:
            raise RuntimeError("Workflow capability activity has no Workflow ID")
        definition = definition.for_session(workflow_id)

    sandbox = await sandbox_access.open_activity_sandbox(sandbox_connection)
    resolver = capabilities.workflow_capability_resolver
    # This activity's one row reads its value from, and saves it to, a map of its own.
    state_key = resolver.state_key(definition, binding_id)
    values = StateMap({state_key: state} if state_key is not None and state is not None else None)
    # Build only the requested row: a row whose function this worker lacks must not fail calls to
    # the others. Registration happens at worker boot on a pinned chain, so a retry cannot help.
    try:
        registration = resolver.build_capability_registration(definition, binding_id, sandbox=sandbox, values=values)
    except capabilities.CapabilityNotRegisteredError as error:
        return CapabilityActivityResult(result=_missing_capability_binding(str(error)))
    if not isinstance(registration, CallableRegistration):
        return CapabilityActivityResult(
            result=_missing_capability_binding(f"No callable capability is registered for {binding_id!r}")
        )
    handler = CallableBoundCapabilityHandler(DirectCapabilityCallableAdapter(registration.callable))
    result = await handler.invoke(invocation)
    saved = values.get(state_key) if state_key is not None else None
    return CapabilityActivityResult(result=result, state=saved if saved != state else None)


def _missing_capability_binding(message: str) -> CapabilityInvocationFailed:
    return CapabilityInvocationFailed.model_validate(
        {"error": {"code": "missing_capability_binding", "message": message, "retryable": False}}
    )


class AgentsSdkCapabilityActivityInvoker(WorkflowCapabilityActivityInvoker):
    """Pass complete invocations to the single Agents SDK capability activity."""

    async def invoke_provided_tool(
        self,
        activity: Callable[..., Awaitable[object]],
        invocation: ProvidedToolInvocation,
    ) -> object:
        return await self.invoke(activity, invocation)

    async def invoke(
        self,
        activity: Callable[..., Awaitable[object]],
        *activity_args: object,
        **activity_kwargs: object,
    ) -> object:
        return await activity(*activity_args, **activity_kwargs)


def _use_sandbox_capability_activity() -> bool:
    if not temporalio.workflow.in_workflow():
        return True
    return temporalio.workflow.patched(_SANDBOX_CAPABILITY_ACTIVITY_PATCH)


def build_workflow_registrations(
    definition: WorkflowHarnessDefinition,
    *,
    sandbox_connection: sandbox_access.KoyebCapabilitySandbox | None = None,
    prepare_sandbox: Callable[[], Awaitable[None]] | None = None,
    values: StateMap | None = None,
) -> CapabilityRegistrationRegistry:
    """Replace direct Python callables with activity-scheduling bindings.

    Only binding identities are needed here, so no worker function is built: a function this
    worker lacks fails its own calls (``missing_capability_binding``), not the whole Session.
    ``values`` holds the Workflow run's saved values: each activity of a stateful row starts from
    its row's value there, and a successful call's new value replaces it. Calls of one row run one
    at a time.
    """

    run_values = values if values is not None else StateMap()
    resolver = capabilities.workflow_capability_resolver
    registrations: list[CallableRegistration | CallbackRegistration] = []
    sandbox_bindings = {capability.binding_id for capability in definition.capabilities if capability.kind == "hook"}
    for capability in resolver.bound_capabilities(definition):
        reference = CapabilityBindingReference(id=capability.binding_id)
        if capability.kind == "callback":
            registrations.append(CallbackRegistration(reference=reference))
            continue
        state_key = resolver.state_key(definition, capability.binding_id)
        if capability.kind == "tool":
            # The SDK cannot know whether an authored tool is safe to run twice, so a lost call is not run again.
            async def call_tool(
                binding_id: str, invocation: CapabilityInvocation, state: JsonValue | None
            ) -> CapabilityActivityResult:
                return await invoke_agent_tool(definition, binding_id, invocation, state)

            call = call_tool
        else:

            async def call_hook(
                binding_id: str,
                invocation: CapabilityInvocation,
                state: JsonValue | None,
                *,
                connection: sandbox_access.KoyebCapabilitySandbox | None = (
                    sandbox_connection if reference.id in sandbox_bindings else None
                ),
            ) -> CapabilityActivityResult:
                if connection is not None and _use_sandbox_capability_activity():
                    if prepare_sandbox is not None:
                        await prepare_sandbox()
                    return await invoke_sandbox_capability(definition, binding_id, invocation, connection, state)
                # Temporal drops all argument types when the input count differs from the declared parameters.
                return await invoke_agent_capability(definition, binding_id, invocation, None, state)

            call = call_hook
        registrations.append(
            CallableRegistration(
                reference=reference,
                callable=_stateful_activity_call(reference.id, call, state_key, run_values),
            )
        )
    return CapabilityRegistrationRegistry(registrations)


def _stateful_activity_call(
    binding_id: str,
    call: Callable[[str, CapabilityInvocation, JsonValue | None], Awaitable[CapabilityActivityResult]],
    state_key: str | None,
    values: StateMap,
) -> Callable[[CapabilityInvocation], Awaitable[CapabilityInvocationResult]]:
    async def invoke(invocation: CapabilityInvocation) -> CapabilityInvocationResult:
        if state_key is None:
            return (await call(binding_id, invocation, None)).result
        async with values.lock(state_key):
            outcome = await call(binding_id, invocation, values.get(state_key))
            if outcome.state is not None:
                try:
                    values.set(state_key, outcome.state)
                except SavedStateTooLargeError as error:
                    # The call does not count: the previous value stays, and the call fails.
                    return CapabilityInvocationFailed(
                        error=core_protocol.ProtocolError(
                            code="capability_execution_failed",
                            message=f"Capability callable failed: {error}",
                            retryable=False,
                            details=None,
                        )
                    )
            return outcome.result

    return invoke


class WorkflowHarnessDefinitionActivityInvoker(WorkflowActivityInvoker):
    """Prepend one immutable Vibe Harness definition to a Workflow activity call."""

    def __init__(self, definition: WorkflowHarnessDefinition) -> None:
        self._definition = definition

    async def invoke(
        self,
        activity: Callable[..., Awaitable[object]],
        *activity_args: object,
        **activity_kwargs: object,
    ) -> object:
        return await activity(self._definition, *activity_args, **activity_kwargs)


@asynccontextmanager
async def _open_connector_resource(
    definition: WorkflowHarnessDefinition,
) -> AsyncIterator[
    tuple[
        connectors.AgentsSdkConnectorResource,
        MistralConnectorConfiguration,
    ]
    | None
]:
    resolver = capabilities.workflow_capability_resolver
    slots = resolver.build_connector_slots(definition)
    discovery = resolver.build_connector_discovery(definition)
    if not slots and discovery is None:
        yield None
        return

    connector_config = definition.connectors
    if connector_config is None:
        raise RuntimeError("connector resources require Harness connector configuration")
    runtime_connector_config = MistralConnectorConfiguration.model_validate(
        connector_config.model_dump(mode="json", by_alias=False)
    )
    connector_resource = connectors.AgentsSdkConnectorResource.from_workflow_context(
        slots,
        discovery=discovery,
        configuration=runtime_connector_config,
    )
    try:
        yield connector_resource, runtime_connector_config
    finally:
        await connector_resource.close()


@asynccontextmanager
async def _open_mcp_host(
    definition: WorkflowHarnessDefinition,
    source: McpSourceConfiguration,
) -> AsyncIterator[McpCapabilityHost]:
    if not connectors.is_agents_sdk_connector_source(source):
        yield McpHttpCapabilityHost()
        return

    async with _open_connector_resource(definition) as opened:
        if opened is None:
            raise RuntimeError(f"No authored connector can route source {source.id!r}")
        connector_resource, connector_config = opened
        await connector_resource.restore_source_binding(source, connector_config)
        yield connector_resource


@workflows.activity(name=_MCP_LIST_ACTIVITY_NAME)
async def list_mcp_tools(
    definition: WorkflowHarnessDefinition,
    request: WorkflowMcpListToolsActivityRequest,
) -> WorkflowMcpListToolsActivityResult:
    async with _open_mcp_host(definition, request.source) as host:
        try:
            catalog = await host.list_tools(request.source)
        except McpSourceUnavailableError as error:
            final = non_retryable_mcp_list_error(error)
            if final is None:
                raise
            raise final from error
    return WorkflowMcpListToolsActivityResult(tools=catalog.tools, instructions=catalog.instructions)


class _ActivityDynamicCapabilityExecutor(DynamicCapabilityExecutor):
    def __init__(self, host: McpCapabilityHost) -> None:
        self._host = host

    async def invoke_dynamic_capability(
        self,
        request: DynamicCapabilityExecutionRequest,
    ) -> McpToolCallResult:
        return await self._host.call_tool(
            McpToolCallRequest(
                action_id=request.invocation.action_id,
                turn_id=request.invocation.turn_id,
                source=request.route.source,
                remote_tool_name=request.route.remote_tool_name,
                arguments=request.invocation.arguments,
                call_id=request.invocation.call_id,
                mcp_app=request.route.mcp_app,
            )
        )


@workflows.activity(
    name=_DYNAMIC_ACTIVITY_NAME,
    retry_policy_max_attempts=1,
    start_to_close_timeout=_TOOL_TIMEOUT,
    heartbeat_timeout=_TOOL_HEARTBEAT_TIMEOUT,
)
async def invoke_dynamic_capability(
    definition: WorkflowHarnessDefinition,
    request: DynamicCapabilityRequest,
) -> DynamicCapabilityResult:
    """Call an MCP or connector tool, whose side effects must not repeat after a lost execution."""

    async with (
        heartbeat_while_running(),
        stop_when_cancelled(),
        _open_mcp_host(definition, request.route.source) as host,
    ):
        return await execute_dynamic_capability(
            _ActivityDynamicCapabilityExecutor(host),
            request,
        )


def build_workflow_mcp_host(
    definition: WorkflowHarnessDefinition,
) -> WorkflowMcpCapabilityHost:
    return WorkflowMcpCapabilityHost(
        activities=WorkflowMcpActivities(list_tools=list_mcp_tools),
        dynamic_activity=invoke_dynamic_capability,
        activity_invoker=WorkflowHarnessDefinitionActivityInvoker(definition),
    )


@workflows.activity(name=_CONNECTORS_LIST_ACTIVITY_NAME)
async def list_connectors(
    definition: WorkflowHarnessDefinition,
    configuration: MistralConnectorConfiguration,
) -> list[MistralConnectorDescriptor]:
    async with _open_connector_resource(definition) as opened:
        if opened is None:
            return []
        host, _ = opened
        try:
            return await host.list_connectors(configuration)
        except MistralConnectorNotFoundError as error:
            # A wrong name stays wrong, so Temporal must not retry the activity. The Agents SDK's
            # connector resource reports a wrong name as an unsupported connector instead; this
            # is for a resource that still raises it.
            raise ApplicationError(
                str(error),
                error.connector_name,
                list(error.close_matches),
                type=_CONNECTOR_NOT_FOUND_ERROR_TYPE,
                non_retryable=True,
            ) from error


@workflows.activity(name=_CONNECTORS_APPLY_ACTIVITY_NAME)
async def apply_connected_connectors(
    definition: WorkflowHarnessDefinition,
    connector_ids: list[str],
) -> None:
    async with _open_connector_resource(definition) as opened:
        if opened is None:
            return
        host, _ = opened
        try:
            await host.apply_connected_connectors(connector_ids)
        except MistralConnectorNotConnectedError as error:
            # The user has to connect again; a retry would only repeat the same answer.
            raise ApplicationError(
                str(error),
                list(error.connector_ids),
                type=_CONNECTOR_NOT_CONNECTED_ERROR_TYPE,
                non_retryable=True,
            ) from error


class WorkflowConnectorCapabilityHost(MistralConnectorHost):
    """Run connector discovery and authentication effects through activities."""

    def __init__(self, definition: WorkflowHarnessDefinition) -> None:
        self._invoker = WorkflowHarnessDefinitionActivityInvoker(definition)

    async def list_connectors(
        self,
        configuration: MistralConnectorConfiguration,
    ) -> list[MistralConnectorDescriptor]:
        try:
            result = await self._invoker.invoke(list_connectors, configuration)
        except ActivityError as error:
            not_found = _connector_not_found(error)
            if not_found is None:
                raise
            raise not_found from error
        return cast(list[MistralConnectorDescriptor], result)

    async def apply_connected_connectors(self, connector_ids: list[str]) -> None:
        try:
            await self._invoker.invoke(apply_connected_connectors, connector_ids)
        except ActivityError as error:
            not_connected = _connector_not_connected(error)
            if not_connected is None:
                raise
            raise not_connected from error


def _connector_not_found(error: ActivityError) -> MistralConnectorNotFoundError | None:
    """Rebuild the not-found error the activity raised, so the Session fails with its message."""

    cause = error.cause
    if not isinstance(cause, ApplicationError) or cause.type != _CONNECTOR_NOT_FOUND_ERROR_TYPE:
        return None
    match cause.details:
        case (str() as connector_name, list() as close_matches):
            return MistralConnectorNotFoundError(connector_name, close_matches=[str(name) for name in close_matches])
        case _:
            return None


def _connector_not_connected(error: ActivityError) -> MistralConnectorNotConnectedError | None:
    """Rebuild the not-connected error the activity raised, so the Harness reports a failed sign-in."""

    cause = error.cause
    if not isinstance(cause, ApplicationError) or cause.type != _CONNECTOR_NOT_CONNECTED_ERROR_TYPE:
        return None
    match cause.details:
        case (list() as connector_ids,):
            return MistralConnectorNotConnectedError([str(connector_id) for connector_id in connector_ids])
        case _:
            return None


def build_workflow_connector_host(
    definition: WorkflowHarnessDefinition,
) -> WorkflowConnectorCapabilityHost | None:
    """Build the connector host when the Harness has any connector to resolve.

    A discovered set counts as much as an authored one: a Harness whose only connector
    declaration is ``all_connectors()`` still resolves its connectors through this host.
    """

    if not definition.connector_resources and definition.connector_discovery is None:
        return None
    return WorkflowConnectorCapabilityHost(definition)


__all__ = [
    "AgentsSdkCapabilityActivityInvoker",
    "CapabilityActivityResult",
    "WorkflowConnectorCapabilityHost",
    "build_workflow_connector_host",
    "build_workflow_registrations",
    "build_workflow_mcp_host",
    "WorkflowHarnessDefinitionActivityInvoker",
]
