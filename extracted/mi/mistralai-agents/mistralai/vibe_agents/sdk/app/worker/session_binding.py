"""Agents SDK product binding for Workflow-hosted Harness Sessions.

The decorated Workflow owns Vibe Agents inputs, signals, continuation, and
legacy event envelopes. ``WorkflowSessionHost`` owns Session execution.
"""

import asyncio
import functools
import time
from collections.abc import Awaitable, Callable, Mapping, Sequence
from contextlib import AbstractAsyncContextManager
from dataclasses import replace
from datetime import timedelta
from enum import Enum
from types import MappingProxyType
from typing import Literal, assert_never
from uuid import UUID, uuid4

import structlog
import temporalio.exceptions
import temporalio.workflow
from pydantic import JsonValue, ValidationError
from temporalio.exceptions import ApplicationError, TemporalError

import mistralai.workflows as workflows
from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.app_server.session.models.common import HistoryEntryId
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.agents.commands import SESSION_FAILED_ERROR_CODE, session_end_message
from mistralai.vibe.harness.runtime.agents.control_plane import SendCommandRequest
from mistralai.vibe.harness.runtime.agents.execution import AgentRuntimeBinding
from mistralai.vibe.harness.runtime.agents.models import (
    AgentTopology,
    ChildLineage,
    RootSandboxReference,
    StartSessionRequest,
)
from mistralai.vibe.harness.runtime.agents.policy import SubagentPolicy
from mistralai.vibe.harness.runtime.capabilities import MistralConnectorNotFoundError
from mistralai.vibe.harness.runtime.completion.config import parse_completion_config
from mistralai.vibe.harness.runtime.content import to_core_content, to_session_content
from mistralai.vibe.harness.runtime.errors import (
    HarnessCommandRejectedError,
    HarnessCompletionFailedError,
)
from mistralai.vibe.harness.runtime.genai import GenAIAgentIdentity, GenAIRootTraceParent
from mistralai.vibe.harness.runtime.hosts.local import LocalDeterminismSource
from mistralai.vibe.harness.runtime.hosts.local.conditions import AsyncioSessionConditionWaiter
from mistralai.vibe.harness.runtime.hosts.workflows import (
    SessionV1HarnessEventPublisher,
    TemporalWorkflowConditionWaiter,
    WorkflowCapabilityCallbackPort,
    WorkflowConditionWaiter,
    WorkflowDeterminismSource,
    WorkflowHostedSession,
    WorkflowSandboxResource,
    WorkflowSessionHost,
    workflow_is_replaying,
)
from mistralai.vibe.harness.runtime.hosts.workflows.action_executor import (
    CompletionObservationContext,
    observation_context_factory,
)
from mistralai.vibe.harness.runtime.hosts.workflows.harness_definition import (
    WorkflowHarnessDefinition,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_definitions import NoSandboxDefinition
from mistralai.vibe.harness.runtime.observability import ObservationContext
from mistralai.vibe.harness.runtime.session.active_turn import (
    ActiveTurnCommandAdmission,
    determine_active_turn_command_admission,
)
from mistralai.vibe.harness.runtime.session.callbacks import public_callback_id
from mistralai.vibe.harness.runtime.session.commands import (
    TURN_NOT_ACTIVE_CODE,
    AgentMessageCommand,
    ContextMessage,
    InterruptTurnCommand,
    SendMessageCommand,
    SessionCommandAccepted,
    SessionCommandRejected,
    SessionCommandResult,
    StartTurnCommand,
    SteerTurnCommand,
)
from mistralai.vibe.harness.runtime.session.conditions import SessionConditionWaiter
from mistralai.vibe.harness.runtime.session.configuration import BASH_MAX_TIMEOUT
from mistralai.vibe.harness.runtime.session.events.publisher import SessionEventPublisher
from mistralai.vibe.harness.runtime.session.initial_turn import (
    InitialTurnRefusalReason,
    InitialTurnRefusedError,
    raise_if_initial_turn_refused,
)
from mistralai.vibe.harness.runtime.session.intake import (
    DEFAULT_SESSION_INTAKE_LIMITS,
    PendingSessionCommand,
    SessionCommandQueueFullError,
    SessionIntakeLimits,
    pending_command_bytes,
)
from mistralai.vibe.harness.runtime.session.model_wait import DEFAULT_MODEL_WAIT_POLICY, ModelWaitPolicy
from mistralai.vibe.harness.runtime.session.programs import DEFAULT_PROGRAM_EXECUTION_POLICY, ProgramExecutionPolicy
from mistralai.vibe.harness.runtime.session.runtime import SessionRuntime
from mistralai.vibe.harness.runtime.session.state import RuntimeSessionState
from mistralai.vibe.harness.runtime.session.turn_policy import DEFAULT_TURN_EXECUTION_POLICY, TurnExecutionPolicy
from mistralai.vibe.harness.runtime.session.turns import TurnCompleted, TurnFailed, TurnRunResult
from mistralai.vibe.harness.session_values import CancelledTermination, ProtocolError
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.app.worker import (
    active_turn,
    activities,
    continuation,
    customer_metadata,
    events,
    lifecycle,
    message_receipts,
    runtime_metrics,
    sandbox_access,
    session_caller,
    session_limits,
    start_input,
    usage_telemetry,
)
from mistralai.vibe_agents.sdk.app.worker import callbacks as worker_callbacks
from mistralai.vibe_agents.sdk.app.worker import control_plane as worker_control_plane
from mistralai.vibe_agents.sdk.app.worker import observability as turn_observability
from mistralai.vibe_agents.sdk.app.worker import skills as worker_skills
from mistralai.vibe_agents.sdk.app.worker.sandbox_coordinator import WorkflowSandboxCoordinator
from mistralai.vibe_agents.sdk.app.worker.sandbox_lifecycle import SandboxLifecycle, SandboxLifecycleFactory
from mistralai.vibe_agents.sdk.assembly import assemble, sandbox_skills, shared_worker
from mistralai.vibe_agents.sdk.assembly import sandbox as sandbox_assembly
from mistralai.vibe_agents.sdk.assembly import session_inputs as session_input_assembly
from mistralai.vibe_agents.sdk.assembly import subagents as subagent_assembly
from mistralai.vibe_agents.sdk.assembly.stateful import StateMap
from mistralai.vibe_agents.sdk.authoring import agent as sdk_agent
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring.errors import (
    UnsupportedAgentFeatureError,
)
from mistralai.vibe_agents.sdk.sandbox.koyeb import open_borrowed_koyeb_sandbox
from mistralai.vibe_agents.sdk.sandbox.refusal import sandbox_create_refusal
from mistralai.vibe_agents.session_workflow import session_v1_wire
from mistralai.vibe_agents.session_workflow.command_ids import message_command_id
from mistralai.vibe_agents.session_workflow.initial_turn import build_start_input_turn_command
from mistralai.vibe_agents.session_workflow.update_inputs import (
    MessageUpdateInput,
    SendMessageInput,
    StartTurnInput,
    SteerTurnInput,
)
from mistralai.vibe_agents.session_workflow.user_message import read_user_message
from mistralai.workflows.core.config.config import config as workflow_config

from .. import config

logger = structlog.get_logger(__name__)

_AGENT_WORKFLOW_TAG = "agents"
_SANDBOX_METRICS = runtime_metrics.WorkerSandboxMetrics()
_MAX_CARRIED_COMMAND_IDS = 1000
_LIMIT_STOP_REASONS: dict[wire.SessionLimitCause, str] = {
    wire.SessionLimitCause.LIFETIME_LIMIT: "The Session reached its maximum lifetime",
    wire.SessionLimitCause.IDLE_LIMIT: "The Session was idle for too long",
}


def _initial_message_too_large(limit: int) -> str:
    return f"The initial message exceeds the Session's command intake budget of {limit} bytes"


def _limit_cause(command: wire.SystemCommand) -> wire.SessionLimitCause | None:
    """Return the Session limit a stop names, ignoring causes this worker does not know."""
    if command.action != "stop" or command.cause is None:
        return None
    try:
        return wire.SessionLimitCause(command.cause)
    except ValueError:
        return None


def _interrupt_cause(command: wire.SystemCommand) -> str | None:
    """Return the cause a command gives the Turn it interrupts.

    A stop ends the session, so its Turn reads "cancelled", or the Session limit the stop names.
    """
    if command.action != "stop":
        return None
    return _limit_cause(command) or "cancelled"


_BACKGROUND_PROCESSES_PATCH = "agents-sdk.background-processes.v1"
_LARGE_OUTPUT_PATCH = "agents-sdk.large-output-files.v1"
_IDLE_STOP_PATCH = "agents-sdk.idle-stop-ends-session.v1"
ROOT_SANDBOX_NOT_LENDABLE_ERROR_TYPE = "RootSandboxNotLendable"

AdmittedWorkflowMessage = continuation.AdmittedWorkflowMessage
CommandPublication = continuation.CommandPublication
MessageCommandPublication = continuation.MessageCommandPublication
UserMessagePublication = continuation.UserMessagePublication
ScopedInterruptPublication = continuation.ScopedInterruptPublication
UnscopedInterruptPublication = continuation.UnscopedInterruptPublication
WorkflowContinuationState = continuation.WorkflowContinuationState
WorkflowPublicationState = continuation.WorkflowPublicationState


class _WorkflowRuntimeStateSink:
    """Retain every committed Runtime state for the next Continue-As-New run."""

    def __init__(self, restored_state: RuntimeSessionState | None) -> None:
        self._state = restored_state

    def commit(self, state: RuntimeSessionState) -> None:
        self._state = state

    def latest_or(self, state: RuntimeSessionState) -> RuntimeSessionState:
        return self._state if self._state is not None else state


def _background_processes_enabled() -> bool:
    return not temporalio.workflow.in_workflow() or temporalio.workflow.patched(_BACKGROUND_PROCESSES_PATCH)


def _large_output_enabled() -> bool:
    return not temporalio.workflow.in_workflow() or temporalio.workflow.patched(_LARGE_OUTPUT_PATCH)


def _idle_stop_ends_session() -> bool:
    # An earlier worker handed an idle stop to the Runtime, which refused it; its histories replay that way.
    return not temporalio.workflow.in_workflow() or temporalio.workflow.patched(_IDLE_STOP_PATCH)


class SessionInputsUnresolvedError(ValueError):
    """The deployed Agent declares Session inputs this Session was never given."""


class InitialMessageRejectedError(ValueError):
    """The Session refused its first message, so the first Turn will never run."""


def _root_sandbox_reference(resource: WorkflowSandboxResource, session_id: str) -> RootSandboxReference | None:
    """The Sandbox a root lends its children, refused when they could not borrow it.

    A root names a Sandbox it creates after its Workflow ID, and a child proves ownership
    against its root Session ID, so the two must be the same value. The controller always
    starts a Session under its Session ID; only a hand-made Workflow start can differ.
    """
    reference = resource.root_reference()
    execution_id = workflows.get_execution_id()
    if reference is not None and execution_id is not None and execution_id != session_id:
        raise ApplicationError(
            "Subagents can share this Session's sandbox only when its Workflow ID is its Session ID",
            type=ROOT_SANDBOX_NOT_LENDABLE_ERROR_TYPE,
            non_retryable=True,
        )
    return reference


class WorkflowSessionBinding:
    """Own one Workflow Host, Runtime, callback store, and Sandbox resource."""

    def __init__(
        self,
        *,
        host: WorkflowSessionHost,
        runtime: SessionRuntime,
        sandbox: WorkflowSandboxResource,
        callbacks: worker_callbacks.WorkflowCallbackStore,
        session_id: str,
        session_v1: bool,
        condition_waiter: SessionConditionWaiter | None = None,
        publications: WorkflowPublicationState | None = None,
        runtime_state_sink: _WorkflowRuntimeStateSink | None = None,
        completion_http_headers: Mapping[str, str] | None = None,
        harness_observability: turn_observability.HarnessTurnObservability | None = None,
        intake_limits: SessionIntakeLimits = DEFAULT_SESSION_INTAKE_LIMITS,
        genai_agent: GenAIAgentIdentity | None = None,
        sandbox_lifecycle: SandboxLifecycle | None = None,
        stateful_values: StateMap | None = None,
    ) -> None:
        self.host = host
        self.runtime = runtime
        self.sandbox = sandbox
        self.callbacks = callbacks
        # The Runtime's own waiter, so a Host wait wakes on the same changes the Runtime reports.
        self.condition_waiter = condition_waiter or (
            TemporalWorkflowConditionWaiter() if temporalio.workflow.in_workflow() else AsyncioSessionConditionWaiter()
        )
        self.session_id = session_id
        self.session_v1 = session_v1
        self.publications = publications or WorkflowPublicationState()
        # The capability registrations update this map after each successful stateful call.
        self.stateful_values = stateful_values if stateful_values is not None else StateMap()
        self._intake_limits = intake_limits
        self._genai_agent = genai_agent
        self._sandbox_coordinator = WorkflowSandboxCoordinator(
            runtime, self.condition_waiter, sandbox_lifecycle, sandbox=sandbox
        )
        self._runtime_state_sink = runtime_state_sink or _WorkflowRuntimeStateSink(None)
        self._session = WorkflowHostedSession(host=host, runtime=runtime, sandbox=sandbox)
        self._turn_scope_binder = turn_observability.TurnScopeBinder(
            harness_observability or turn_observability.get_harness_turn_observability(),
            completion_http_headers,
        )
        self.runtime_metrics = runtime_metrics.WorkflowRuntimeMetrics(
            now_unix_ms=_workflow_time_unix_ms,
            session_created_at_unix_ms=lambda: runtime.state.event_producer.session_created_at,
            turns_to_drive=lambda: runtime.state.turns_to_drive,
            active_turn_id=lambda: runtime.inspection.active_turn_id,
        )
        runtime.bind_command_observer(self._publish_command_result)
        runtime.bind_turn_scope(self._turn_scope)

    async def watch_sandbox_idle(self) -> None:
        await self._sandbox_coordinator.watch_idle()

    def sandbox_durability(self) -> dict[str, JsonValue] | None:
        return self._sandbox_coordinator.durability()

    @classmethod
    async def open(
        cls,
        *,
        definition: WorkflowHarnessDefinition,
        sandbox: contracts.Sandbox,
        principal: wire.Principal | None,
        session_id: str,
        restored: WorkflowContinuationState | None = None,
        session_inputs: dict[str, JsonValue] | None = None,
        event_publisher: SessionEventPublisher | None = None,
        session_v1: bool = False,
        condition_waiter: WorkflowConditionWaiter | None = None,
        completion_http_headers: Mapping[str, str] | None = None,
        skills: sandbox_skills.SandboxSkillFiles | None = None,
        completion_http_headers_provider: Callable[[], Awaitable[Mapping[str, str]]] | None = None,
        completion_observation_context: CompletionObservationContext | None = None,
        subagent_policy: SubagentPolicy | None = None,
        control_plane: worker_control_plane.ActivitySessionControlPlane | None = None,
        child_session: StartSessionRequest | None = None,
        lineage: ChildLineage | None = None,
        program_policy: ProgramExecutionPolicy = DEFAULT_PROGRAM_EXECUTION_POLICY,
        wait_policy: ModelWaitPolicy = DEFAULT_MODEL_WAIT_POLICY,
        turn_policy: TurnExecutionPolicy = DEFAULT_TURN_EXECUTION_POLICY,
        intake_limits: SessionIntakeLimits = DEFAULT_SESSION_INTAKE_LIMITS,
        callback_timeout: timedelta = config.DEFAULT_CALLBACK_TIMEOUT,
        sandbox_provisioning_timeout: timedelta = config.DEFAULT_SANDBOX_PROVISIONING_TIMEOUT,
        genai_agent: GenAIAgentIdentity | None = None,
        sandbox_lifecycle: SandboxLifecycle | None = None,
        agent_id: UUID | None = None,
        application_id: UUID | None = None,
        correlation_id: str | None = None,
        telemetry_enabled: bool = True,
    ) -> "WorkflowSessionBinding":
        definition = definition.for_session(session_id)
        # Rebuilt from the start input on every run, so a continue-as-new keeps attributing to the same Session.
        attribution = usage_telemetry.completion_attribution(
            session_id=session_id,
            principal=principal,
            parent_session_id=child_session.parent_session_id if child_session is not None else None,
            root_session_id=child_session.root_session_id if child_session is not None else None,
            agent_id=agent_id,
            application_id=application_id,
            correlation_id=correlation_id,
        )
        sandbox_adapter = sandbox_assembly.compile_sandbox(
            sandbox,
            proxy_identity=_sandbox_proxy_identity(principal),
            session_id=session_id,
            terminal_hook_failures=True,
            lifecycle=sandbox_lifecycle,
            metrics=_SANDBOX_METRICS,
        )
        # Checked before the Sandbox is provisioned: a Session missing a declared
        # input can never run, so it must fail without side effects. A restored
        # Session uses its journaled inputs, which are authoritative.
        _bind_declared_session_inputs(
            definition,
            sandbox_adapter,
            restored.hosted.runtime.session_inputs if restored is not None else (session_inputs or {}),
            # A child borrows its root's live sandbox, and a sandbox restored with provider state
            # does not run on_create again. A Session continued onto a version that adds a
            # sandbox does, so its inputs are checked.
            sandbox_is_live=child_session is not None
            or (restored is not None and restored.hosted.sandbox.provider_state is not None),
        )
        # The bash maximum this Session's Host runs, resolved once: the sandbox checks it
        # as it opens and the Host is built with it, so they never check different numbers.
        bash_max_timeout = BASH_MAX_TIMEOUT
        # A child borrows its root's environment through the root's open path; the
        # root alone owns that Sandbox's lifecycle.
        sandbox_resource = (
            await open_borrowed_koyeb_sandbox(
                child_session.sandbox,
                sandbox,
                sandbox_adapter,
                # The controller starts a child only under its owned parent's tree root; a direct
                # Workflow start can still choose this value (AGE-2410).
                root_session_id=child_session.root_session_id,
                restored=restored.hosted.sandbox if restored is not None else None,
                bash_max_timeout=bash_max_timeout,
            )
            if child_session is not None and child_session.sandbox is not None
            else await WorkflowSandboxResource.open(
                NoSandboxDefinition(),
                restored=restored.hosted.sandbox if restored is not None else None,
                host=sandbox_adapter,
                bash_max_timeout=bash_max_timeout,
            )
            if child_session is not None
            else await sandbox_assembly.open_sandbox_resource(
                sandbox_adapter,
                bash_max_timeout=bash_max_timeout,
                restored=restored.hosted.sandbox if restored is not None else None,
                provisioning_timeout_seconds=sandbox_provisioning_timeout.total_seconds(),
            )
        )
        if child_session is None and sandbox_assembly.needs_sandbox_at_open(sandbox):
            await sandbox_resource.provision_at_open()
        runtime: SessionRuntime | None = None
        try:
            definition = definition.with_runtime_sandbox(
                sandbox=sandbox_resource.config,
                workdir=sandbox_resource.workspace,
            )
            # Served before the children's definition is taken, so a child inherits the catalog
            # and reads its parent's skill files instead of writing them again.
            definition, session_skill_host = await worker_skills.serve_skills(
                definition,
                sandbox_resource,
                skills,
                restored.hosted.runtime if restored is not None else None,
                child=child_session is not None,
                session_id=session_id,
            )
            agents_binding = None
            if subagent_policy is not None:
                if control_plane is None:
                    raise ValueError("Subagents require a Session-control-plane binding")
                inherited_definition = _definition_children_inherit(definition)
                agents_binding = AgentRuntimeBinding(
                    control_plane=control_plane,
                    topology=AgentTopology(
                        session_id=UUID(session_id),
                        root_session_id=child_session.root_session_id if child_session else UUID(session_id),
                        parent_session_id=child_session.parent_session_id if child_session else None,
                        agent_path=child_session.agent_path if child_session else "/root",
                    ),
                    policy=replace(
                        subagent_policy, concurrent_child_turn_limit=child_session.concurrent_child_turn_limit
                    )
                    if child_session
                    else subagent_policy,
                    definition=inherited_definition,
                    sandbox=child_session.sandbox
                    if child_session
                    else _root_sandbox_reference(sandbox_resource, session_id),
                    lineage=lineage or ChildLineage(),
                )
            callbacks = worker_callbacks.WorkflowCallbackStore()
            session_condition_waiter = condition_waiter or (
                TemporalWorkflowConditionWaiter()
                if temporalio.workflow.in_workflow()
                else AsyncioSessionConditionWaiter()
            )
            callback_port = WorkflowCapabilityCallbackPort(
                event_port=callbacks,
                signal_port=callbacks,
                time_unix_ms=_workflow_time_unix_ms,
            )
            # A child on its root's Sandbox hands capability activities the same connection as the root.
            has_sandbox = child_session is None or child_session.sandbox is not None
            stateful_values = StateMap(restored.stateful_values if restored is not None else None)
            registrations = activities.build_workflow_registrations(
                definition,
                sandbox_connection=(
                    sandbox_access.from_workflow_sandbox(sandbox, sandbox_resource) if has_sandbox else None
                ),
                prepare_sandbox=(
                    sandbox_adapter.prepare_capability_sandbox_access
                    if has_sandbox and isinstance(sandbox, contracts.MistralSandbox) and sandbox.header_bindings
                    else None
                ),
                values=stateful_values,
            )
            mcp_host = activities.build_workflow_mcp_host(definition)
            connector_host = activities.build_workflow_connector_host(definition)
            process_composition = sandbox_assembly.compose_background_process_session(
                sandbox_resource,
                sandbox_adapter,
                enabled=(
                    _background_processes_enabled()
                    and (
                        restored is None
                        or restored.hosted.runtime.config.settings.tools.background_processes.mode == "enabled"
                    )
                ),
            )
            # A restored Session keeps the policy its journal recorded: the Harness refuses a changed config.
            # A history from before the patch keeps the old policy, so its replay schedules no file writes.
            large_output_policy: core_protocol.LargeOutputPolicy
            if restored is not None:
                large_output_policy = restored.hosted.runtime.config.settings.tools.large_output
            elif _large_output_enabled():
                large_output_policy = sandbox_assembly.default_large_output_policy(sandbox_resource)
            else:
                large_output_policy = core_protocol.DisabledLargeOutputPolicy()
            large_output = sandbox_assembly.compose_large_output(
                sandbox_resource, large_output_policy, session_id=session_id
            )
            runtime_state_sink = _WorkflowRuntimeStateSink(None)
            harness_observability = turn_observability.get_harness_turn_observability()
            genai_observer = harness_observability.session_genai_observer()
            host = WorkflowSessionHost(
                restored_state=restored.hosted.runtime if restored is not None else None,
                event_publisher=(
                    event_publisher if event_publisher is not None else events.LegacyTaskSessionEventPublisher()
                ),
                determinism=_build_determinism_source(),
                runtime_builtin_tools=sandbox_skills.with_skill_file_hints(
                    process_composition.runtime_builtin_tools, definition.agent_config.skills
                ),
                callback_port=callback_port,
                callback_timeout=callback_timeout,
                # worker_callbacks.WorkflowCallbackStore already derives this id and maps it back in
                # submit_result; the canonical events must name the same one.
                public_callback_id=public_callback_id,
                mcp_host=mcp_host,
                connector_host=connector_host,
                skill_host=session_skill_host,
                activity_invoker=activities.AgentsSdkCapabilityActivityInvoker(),
                command_environment=sandbox_resource.command_environment,
                large_output=large_output.policy,
                bash_max_timeout=bash_max_timeout,
                filesystem=large_output.filesystem,
                condition_waiter=session_condition_waiter,
                completion_http_headers=completion_http_headers,
                # Off drops our attribution; the turn context still puts Session and Turn ids in the request.
                completion_metadata=attribution.metadata if telemetry_enabled else None,
                completion_observation_context=_session_observation_context(
                    attribution.observation_context if telemetry_enabled else None,
                    completion_observation_context,
                ),
                background_process_handler=process_composition.handler,
                completion_http_headers_provider=completion_http_headers_provider,
                runtime_state_commit_sink=(
                    runtime_state_sink.commit if process_composition.handler is not None else None
                ),
                genai_observer=genai_observer,
                # Replayed history must not re-emit spans already exported on the
                # first execution; the host skips the observer while replaying.
                genai_observer_skip_on_replay=True,
                agents=agents_binding,
                program_policy=program_policy,
                wait_policy=wait_policy,
                turn_policy=turn_policy,
                intake_limits=intake_limits,
            )
            restored_turn_scope = turn_observability.TurnScopeBinder(
                harness_observability, completion_http_headers
            ).scope(eligible=_restored_turn_traced(restored))
            async with restored_turn_scope:
                runtime = await host.open(
                    agent_config=definition.agent_config,
                    registrations=registrations,
                    session_id=session_id,
                    conversation=child_session.conversation if child_session is not None and restored is None else None,
                    session_inputs=session_inputs,
                )
            return cls(
                host=host,
                runtime=runtime,
                sandbox=sandbox_resource,
                callbacks=callbacks,
                condition_waiter=session_condition_waiter,
                session_id=session_id,
                session_v1=session_v1,
                publications=restored.publications if restored is not None else None,
                runtime_state_sink=runtime_state_sink,
                completion_http_headers=completion_http_headers,
                harness_observability=harness_observability,
                intake_limits=intake_limits,
                genai_agent=genai_agent,
                sandbox_lifecycle=sandbox_lifecycle,
                stateful_values=stateful_values,
            )
        except BaseException as setup_error:
            if runtime is not None:
                try:
                    await runtime.dispose()
                except BaseException as cleanup_error:
                    setup_error.add_note(f"Runtime cleanup failed: {cleanup_error!r}")
            if restored is not None:
                # A restored Session's sandbox holds its workspace. Keep it, so that a retry on a
                # fixed worker resumes the Session instead of losing its files.
                sandbox_resource.prepare_continuation()
            try:
                await sandbox_resource.close()
            except BaseException as cleanup_error:
                setup_error.add_note(f"Sandbox cleanup failed: {cleanup_error!r}")
            raise

    async def run_message(self, command: wire.MessageCommand) -> str:
        admitted = await self.admit_message(command)
        if isinstance(admitted, SessionCommandRejected):
            raise HarnessCommandRejectedError(admitted.rejection)
        return await self.run_admitted_message(admitted)

    async def admit_message(
        self,
        command: wire.MessageCommand,
    ) -> AdmittedWorkflowMessage | SessionCommandRejected:
        """Translate one product Start and let Harness decide durable admission."""

        command_id, portable = self._prepare_command(command)
        try:
            result = await self.runtime.receive_command(command_id, portable)
        except SessionCommandQueueFullError:
            self.publications.commands.pop(command_id, None)
            raise
        if isinstance(result, SessionCommandRejected):
            return result
        if result.turn_id is None:
            raise RuntimeError("Runtime accepted a Start without a Turn identity")
        return AdmittedWorkflowMessage(
            turn_id=result.turn_id,
            idempotency_key=command_id,
        )

    async def run_admitted_message(self, admitted: AdmittedWorkflowMessage) -> str:
        """Drive a product Start that Harness already committed."""

        output = await self.runtime.run_until_turn_terminal(admitted.turn_id)
        return "".join(block.text for block in output if isinstance(block, core_protocol.TextContentBlock))

    def _turn_tracing_enabled(self, turn_id: str | None) -> bool:
        # Admission persists the GenAI parent only for eligible Turns. This remains
        # authoritative after Continue-As-New, when in-memory command state is gone.
        return turn_id is not None and self.runtime.has_genai_trace(turn_id)

    def _turn_scope(self, turn_id: str) -> AbstractAsyncContextManager[None]:
        self.runtime_metrics.turn_seen(turn_id)
        return self._turn_scope_binder.scope(eligible=self._turn_tracing_enabled(turn_id))

    def _prepare_command(
        self, command: wire.MessageCommand | wire.SystemCommand, *, source_id: str | None = None
    ) -> tuple[str, StartTurnCommand | SteerTurnCommand | InterruptTurnCommand]:
        command_id = source_id or _command_id(command) or str(workflows.workflow.uuid4())
        known = self.runtime.has_command(command_id)
        # A retry the Runtime already answered starts no Turn, so it never replaces the sandbox; a pending one
        # still may once admitted, so it checks the sandbox as a new Start does.
        answered = self.runtime.get_command_result(command_id) is not None
        self._sandbox_coordinator.command_received(
            starts_turn=isinstance(command, wire.MessageCommand) and command.expected_turn_id is None and not answered
        )
        if isinstance(command, wire.MessageCommand):
            turn_id = command.expected_turn_id or command_id
            content = active_turn.command_content(command)
            message_entry_id = str(command.command_id) if command.command_id is not None else None
            context_messages = [
                *active_turn.context_messages(command),
                *(self._sandbox_coordinator.context_messages() if not known else []),
            ]
            portable: StartTurnCommand | SteerTurnCommand | InterruptTurnCommand
            if command.expected_turn_id is None:
                portable = StartTurnCommand(
                    turn_id=turn_id,
                    content=content,
                    message_entry_id=message_entry_id,
                    context_messages=context_messages,
                    idempotency_key=command_id,
                    genai_trace_parent=_genai_trace_parent(
                        command.metadata, self.session_id, turn_id, self._genai_agent
                    ),
                )
            else:
                portable = SteerTurnCommand(
                    turn_id=turn_id,
                    content=content,
                    message_entry_id=message_entry_id,
                    context_messages=context_messages,
                    idempotency_key=command_id,
                )
            publication: CommandPublication = MessageCommandPublication(
                type="steer_message" if command.expected_turn_id is not None else "start_message",
                command=command,
                turn_id=turn_id,
            )
        else:
            portable = self.runtime.build_interrupt_command(
                command_id,
                expected_turn_id=command.expected_turn_id,
                reason=command.reason,
                cause=_interrupt_cause(command),
            )
            publication = (
                ScopedInterruptPublication() if command.expected_turn_id is not None else UnscopedInterruptPublication()
            )
        # Skipped when the Session holds the id already: a retry has its row, and another command's
        # answer must not publish one for this command.
        if not self.runtime.has_command(command_id):
            self.publications.commands.setdefault(command_id, publication)
        return command_id, portable

    async def receive_message(
        self,
        message: MessageUpdateInput,
        *,
        content: list[core_protocol.ContentBlock],
        context_messages: list[ContextMessage],
        command_id: str,
        message_entry_id: HistoryEntryId,
    ) -> SessionCommandResult | wire.SessionCommandVerdictReason:
        """Hand Harness one message Update's message and wait for its admission.

        ``content`` and ``context_messages`` are the message's blocks, already converted to Runtime
        content. ``command_id`` names any Turn the message starts. Returns the Runtime's admission,
        or why full intake refused the message. Joins the command that already holds ``command_id``,
        if any. The receipt row is published once, when the Runtime admits the message, from the
        content of the admitted command.
        """

        known = self.runtime.has_command(command_id)
        # A steer, or a retry the Runtime already answered, starts no Turn, so it never replaces the sandbox.
        self._sandbox_coordinator.command_received(
            starts_turn=not isinstance(message, SteerTurnInput) and self.runtime.get_command_result(command_id) is None
        )
        portable = self._message_command(
            message,
            content=content,
            command_id=command_id,
            message_entry_id=message_entry_id,
            context_messages=[
                *context_messages,
                *(self._sandbox_coordinator.context_messages() if not known else []),
            ],
        )
        if not known:
            self.publications.commands.setdefault(command_id, UserMessagePublication())
        result = await self.runtime.receive_command(command_id, portable)
        if isinstance(result, SessionCommandRejected) and isinstance(
            result.rejection, core_protocol.QueueFullRejection
        ):
            # The Runtime answers a full intake, or a message over its byte budget, with a queue-full
            # rejection it does not retain, so nothing of the message is held.
            self.publications.commands.pop(command_id, None)
            return await self._publish_overload(command_id, portable)
        return result

    async def steer_active_turn(
        self,
        message: SteerTurnInput,
        *,
        content: list[core_protocol.ContentBlock],
        context_messages: list[ContextMessage],
        command_id: str,
        message_entry_id: HistoryEntryId,
    ) -> SessionCommandResult | wire.SessionCommandVerdictReason:
        """Steer the Turn ``message`` names only while it is active, then publish its user row.

        The Runtime compares and commits under its input lock, so a Turn that ends first is
        rejected with ``turn_not_active`` and nothing is applied. A direct commit runs no command
        observer, so this publishes the row; a replayed commit publishes it again under the same
        task id. Raises ``ActivityError`` when the row is not published: the steer is committed.
        """

        self._sandbox_coordinator.command_received()
        command = _steer_command(
            message,
            content=content,
            command_id=command_id,
            message_entry_id=message_entry_id,
            context_messages=[*context_messages, *self._sandbox_coordinator.context_messages()],
        )
        if self._exceeds_intake_budget(command_id, command):
            # Bounded as a buffered message is, though nothing is buffered.
            return wire.SessionCommandVerdictReason.MESSAGE_TOO_LARGE
        async with self._turn_scope(message.expected_turn_id):
            result = await self.runtime.submit_active_turn_command(command)
        if isinstance(result, SessionCommandAccepted):
            self._sandbox_coordinator.context_accepted(command)
            await lifecycle.emit_v1_message_receipt(
                message_entry_id,
                task_id=command_id,
                turn_id=message.expected_turn_id,
                content=to_session_content(command.content),
                annotations={},
                session_id=self.session_id,
            )
        return result

    def _message_command(
        self,
        message: MessageUpdateInput,
        *,
        content: list[core_protocol.ContentBlock],
        command_id: str,
        message_entry_id: HistoryEntryId,
        context_messages: list[ContextMessage],
    ) -> SendMessageCommand | StartTurnCommand | SteerTurnCommand:
        match message:
            case SteerTurnInput():
                return _steer_command(
                    message,
                    content=content,
                    command_id=command_id,
                    message_entry_id=message_entry_id,
                    context_messages=context_messages,
                )
            case StartTurnInput():
                return StartTurnCommand(
                    turn_id=command_id,
                    content=content,
                    message_entry_id=message_entry_id,
                    context_messages=context_messages,
                    idempotency_key=command_id,
                    genai_trace_parent=_genai_trace_parent(
                        message.metadata, self.session_id, command_id, self._genai_agent
                    ),
                )
            case SendMessageInput():
                return SendMessageCommand(
                    new_turn_id=command_id,
                    content=content,
                    message_entry_id=message_entry_id,
                    context_messages=context_messages,
                    idempotency_key=command_id,
                    genai_trace_parent=_genai_trace_parent(
                        message.metadata, self.session_id, command_id, self._genai_agent
                    ),
                )
            case _:
                assert_never(message)

    def submit_callback_result(
        self, result: harness_session.CallbackResult
    ) -> worker_callbacks.CallbackSubmission | worker_callbacks.CallbackRejection:
        self._sandbox_coordinator.command_received()
        return self.callbacks.submit_result(result)

    async def receive_agent_command(
        self, command_id: str, command: AgentMessageCommand | InterruptTurnCommand
    ) -> SessionCommandResult:
        self._sandbox_coordinator.command_received()
        return await self.runtime.receive_command(command_id, command)

    async def deliver_command(
        self, command: wire.MessageCommand | wire.SystemCommand, *, source_id: str | None = None
    ) -> wire.SessionCommandVerdictReason | None:
        """Deliver one command; return why full intake refused it, or None once delivered."""

        command_id, portable = self._prepare_command(command, source_id=source_id)
        try:
            await self.runtime.deliver_command(command_id, portable)
        except SessionCommandQueueFullError:
            self.publications.commands.pop(command_id, None)
            return await self._publish_overload(command_id, portable)
        return None

    async def buffer_command(
        self, command: wire.MessageCommand | wire.SystemCommand
    ) -> wire.SessionCommandVerdictReason | None:
        """Buffer one command; return why full intake refused it, or None once buffered."""

        command_id, portable = self._prepare_command(command)
        try:
            await self.runtime.buffer_command(command_id, portable)
        except SessionCommandQueueFullError:
            self.publications.commands.pop(command_id, None)
            return await self._publish_overload(command_id, portable)
        return None

    async def reject_initial_message(self, rejected: SessionCommandRejected) -> None:
        """Publish the non-retryable refusal of an initial message the intake cannot hold."""

        if rejected.turn_id is None:
            raise RuntimeError("Runtime rejected a Start without a Turn identity")
        # A Start's Turn is named after its command, so the Turn id is the command id.
        await lifecycle.emit_command_outcome(
            rejected.turn_id,
            outcome="rejected",
            turn_id=rejected.turn_id,
            reason=wire.SessionCommandVerdictReason.MESSAGE_TOO_LARGE.value,
            session_v1=self.session_v1,
        )

    async def start_initial_turn(self, initial_turn: wire.SessionWorkflowInitialTurn) -> None:
        """Start the Session's first Turn with the Turn ID from the start input.

        On refusal, publish the Turn as failed and raise ``InitialMessageRejectedError``. Failing
        is better than idling until the inactivity timeout: the caller waits for this Turn, and
        nothing else tells it that the Turn will never run.
        """

        turn_id = initial_turn.turn_id
        if not self.session_v1:
            # Only Session v1 history rows carry Session content blocks. The controller checks this too.
            raise InitialMessageRejectedError("initial_turn requires the Session v1 protocol")
        try:
            command = build_start_input_turn_command(
                initial_turn,
                genai_trace_parent=_genai_trace_parent(
                    initial_turn.metadata, self.session_id, turn_id, self._genai_agent
                ),
            )
            self.publications.commands[turn_id] = UserMessagePublication()
            raise_if_initial_turn_refused(await self.runtime.receive_command(turn_id, command))
        except InitialTurnRefusedError as error:
            message = await self._publish_initial_turn_refused(turn_id, error.reason)
            raise InitialMessageRejectedError(message) from error

    async def _publish_initial_turn_refused(self, turn_id: str, reason: InitialTurnRefusalReason) -> str:
        """Publish the first Turn as failed, and return the failure message."""

        match reason:
            case "too_large":
                code = wire.SessionCommandVerdictReason.MESSAGE_TOO_LARGE
                message = _initial_message_too_large(self._intake_limits.pending_bytes)
            case "rejected":
                code = wire.SessionCommandVerdictReason.MESSAGE_REJECTED
                message = "The Session cannot run the initial message"
            case _:
                assert_never(reason)
        await lifecycle.emit_v1_turn_refused(
            self.session_id,
            turn_id=turn_id,
            error=session_v1_wire.ProtocolError(message=message, code=code.value),
        )
        return message

    async def _publish_overload(
        self,
        command_id: str,
        command: StartTurnCommand | SteerTurnCommand | InterruptTurnCommand | SendMessageCommand,
    ) -> wire.SessionCommandVerdictReason:
        # A command over the byte budget on its own can never fit, so it is refused for good
        # rather than as a retryable overload.
        too_large = self._exceeds_intake_budget(command_id, command)
        reason = (
            wire.SessionCommandVerdictReason.MESSAGE_TOO_LARGE
            if too_large
            else wire.SessionCommandVerdictReason.INTAKE_OVERLOADED
        )
        await lifecycle.emit_command_outcome(
            command_id,
            outcome="rejected",
            turn_id=None if isinstance(command, SendMessageCommand) else command.turn_id,
            reason=reason.value,
            session_v1=self.session_v1,
            retryable=not too_large,
        )
        return reason

    def _exceeds_intake_budget(
        self,
        command_id: str,
        command: StartTurnCommand | SteerTurnCommand | InterruptTurnCommand | SendMessageCommand,
    ) -> bool:
        # Measured as the Runtime measures a pending command.
        size = pending_command_bytes(PendingSessionCommand(command_id=command_id, command=command))
        return size > self._intake_limits.pending_bytes

    async def _publish_command_result(self, entry: PendingSessionCommand, result: SessionCommandResult) -> None:
        if isinstance(result, SessionCommandAccepted):
            # Admission, not buffering: a buffered Start can still be rejected and the model never see it.
            self._sandbox_coordinator.context_accepted(entry.command)
        command_id = entry.command_id
        publication = self.publications.commands.get(command_id)
        if publication is None:
            return
        if isinstance(result, SessionCommandAccepted) and isinstance(publication, MessageCommandPublication):
            await lifecycle.emit_command_receipt(
                publication.command,
                turn_id=result.turn_id or publication.turn_id,
                session_id=self.session_id,
                session_v1=self.session_v1,
            )
        elif isinstance(result, SessionCommandAccepted) and isinstance(publication, UserMessagePublication):
            if not isinstance(entry.command, SendMessageCommand | StartTurnCommand):
                # Only `send_message`, `start_turn` and the first Turn publish a user message row.
                # Any other command here is a bug.
                raise RuntimeError(
                    f"Command {command_id!r} publishes a user message row but holds a {entry.command.type} command"
                )
            await lifecycle.emit_v1_message_receipt(
                command_id if entry.command.message_entry_id is None else entry.command.message_entry_id,
                task_id=command_id,
                turn_id=result.turn_id,
                content=to_session_content(entry.command.content),
                annotations={},
                session_id=self.session_id,
            )
        elif isinstance(result, SessionCommandRejected) or isinstance(publication, ScopedInterruptPublication):
            outcome: Literal["accepted", "rejected"] = (
                "rejected" if isinstance(result, SessionCommandRejected) else "accepted"
            )
            reason: str | None = result.rejection.code if isinstance(result, SessionCommandRejected) else None
            if publication.type not in {"start_message", "send_message"} and reason in {
                "invalid_command",
                "invalid_state",
            }:
                reason = "stale_turn"
            await lifecycle.emit_command_outcome(
                command_id,
                outcome=outcome,
                turn_id=result.turn_id,
                reason=reason,
                session_v1=self.session_v1,
            )
        del self.publications.commands[command_id]

    async def close_for_continuation(
        self,
        *,
        settle_inbound: Callable[[], Awaitable[None]] | None = None,
    ) -> WorkflowContinuationState:
        """Close the Runtime before reading the state carried to the next run."""

        hosted = await self._session.export_continuation(settle_inbound=settle_inbound)
        # The sink holds the live state; keep the empty cache from export_continuation().
        runtime = self._runtime_state_sink.latest_or(hosted.runtime).model_copy(
            update={"model_input_cache": hosted.runtime.model_input_cache}
        )
        hosted = hosted.model_copy(update={"runtime": runtime})
        return WorkflowContinuationState(
            hosted=hosted,
            publications=self.publications.model_copy(deep=True),
            sandbox_lifecycle=self._sandbox_coordinator.durability(),
            stateful_values=self.stateful_values.values(),
        )

    async def close(self) -> None:
        await self._session.close()


class _WorkflowPhase(Enum):
    STARTING = "starting"
    ACCEPTING_COMMANDS = "accepting_commands"
    CONTINUING = "continuing"
    TERMINAL = "terminal"


class _UnifiedHarnessControlPlaneWorkflow(workflows.InteractiveWorkflow):
    def __init__(self) -> None:
        super().__init__()
        self._binding: WorkflowSessionBinding | None = None
        self._command_handlers_in_flight = 0
        self._stop_requested = False
        # The Session limit that stopped this Session, if one did.
        self._end_cause: wire.SessionLimitCause | None = None
        self._phase = _WorkflowPhase.STARTING
        self._single_turn = False
        # The message Updates in flight, counted apart from command handlers: continuation waits
        # for these only after closing the binding, which ends their wait for admission.
        self._message_handlers_in_flight = 0
        # Serializes the receipt lookup, the Runtime admission, and the receipt update of
        # send_message, so a concurrent retry of one command sees the first receipt instead of
        # admitting again.
        self._send_message_lock = asyncio.Lock()
        self._message_receipts = message_receipts.MessageReceiptLedger()
        # Names each send_message after its idempotency key. Kept past the binding, as receipts are.
        self._session_id: str | None = None
        # The binding's carried processed callback ids, kept past the binding, so a retry of an
        # accepted answer is answered after the Session ends.
        self._processed_callback_ids: list[str] = []

    @workflows.workflow.query(name="sandbox_durability")
    def sandbox_durability(self) -> dict[str, JsonValue] | None:
        binding = self._binding
        if binding is None:
            return None
        return binding.sandbox_durability()

    @workflows.workflow.update(name="admit_command")
    async def admit_command(self, request: SendCommandRequest) -> SessionCommandResult:
        await workflows.workflow.wait_condition(lambda: self._phase is not _WorkflowPhase.STARTING)
        binding = self._binding
        if binding is None or self._phase is not _WorkflowPhase.ACCEPTING_COMMANDS:
            # The Workflows API maps this type to HTTP 500 for ordinary sender
            # Activity retry; a RuntimeError would fail and replay this Task.
            raise ApplicationError("Session is not accepting command Updates", type="INTERNAL_ERROR")
        if str(request.recipient_session_id) != binding.runtime.state.session_id:
            raise _invalid_command_update("Command recipient does not identify this Session")
        self._command_handlers_in_flight += 1
        try:
            command = request.command
            if isinstance(command, AgentMessageCommand):
                if (
                    command.message.source.session_id != request.sender_session_id
                    or command.message.recipient.session_id != request.recipient_session_id
                ):
                    raise _invalid_command_update("Agent message identities do not match authenticated routing")
            elif isinstance(command, InterruptTurnCommand):
                if command.parent_session_id != request.sender_session_id or command.idempotency_key != str(
                    request.command_id
                ):
                    raise _invalid_command_update("Parent interruption identities do not match authenticated routing")
            else:
                raise _invalid_command_update(
                    "This Session procedure accepts resolved agent input or parent interruption"
                )
            command_id = str(request.command_id)
            return await binding.receive_agent_command(command_id, command)
        finally:
            self._command_handlers_in_flight -= 1

    @workflows.workflow.update(name="submit_command_for_verdict")
    async def submit_command_for_verdict(self, command: wire.SessionWorkflowCommand) -> wire.SessionCommandVerdict:
        """Accept or refuse a compare-and-set command or a Start, and say which.

        The Session is the only authority on which Turn is running, so the caller cannot be
        told whether its ``expected_turn_id`` still holds by anything outside this Workflow.
        Answering here rather than through a later event is what lets a refused steer be a
        refusal instead of silence, on either session protocol.

        A Start (a message naming no Turn) is refused while a Turn runs. The Runtime decides
        that as it admits the Start, which it always does during delivery, so the answer read
        back here is the Runtime's own and has no window. Session v1 publishes no entry for a
        refused Start, so this answer is the only one its caller gets. That refusal depends on
        timing, not on the Start, so it is forgotten once answered here: the same id starts a
        Turn after the running one ends, as a strict local start does. A Start delivered by
        signal keeps its refusal, so a redelivery by signal stays refused. On Session v1 a later
        Start through this Update with that id is decided again, since nothing was published
        for the signal's refusal; the legacy protocol published it, so the refusal stands there.

        The comparison is made before the command is delivered, so a refused command is never
        applied. When the Runtime resolves the command immediately, its own verdict is read
        back and wins over the comparison. Other than that Start, an exact retry of a command
        the Runtime refused gets the same refusal again.

        One window remains and is not covered: a Turn that ends between the comparison and a
        deferred resolution is reported accepted. The Runtime rejects it later, and on the
        legacy protocol the command-outcome entry still carries that; Session v1 has no such
        entry, so a late rejection is not reported there.
        """

        while self._phase is _WorkflowPhase.STARTING:
            await workflows.workflow.wait_condition(lambda: self._phase is not _WorkflowPhase.STARTING)
        binding = self._binding
        if binding is None or self._phase is _WorkflowPhase.TERMINAL:
            return wire.SessionCommandVerdict(
                accepted=False,
                reason=wire.SessionCommandVerdictReason.SESSION_NOT_ACCEPTING_COMMANDS,
            )
        command_id = _command_id(command)
        if (refused := _runtime_refusal(binding, command, command_id)) is not None:
            # The Runtime keeps its answer for the id, so a retry is refused as the first attempt
            # was, rather than reported as a command already taken. A Start refused here because a
            # Turn was running was delivered by signal. Session v1 published nothing for that
            # refusal, so this caller is the first to hear of it: the Start is decided again now.
            # The legacy protocol published the refusal, so it stands there.
            if not (
                binding.session_v1
                and command_id is not None
                and refused.reason == wire.SessionCommandVerdictReason.TURN_ACTIVE
            ):
                return refused
            await binding.runtime.forget_running_start_refusal(command_id)
            # Read again: another Update for this id may have forgotten the refusal first, while
            # this one waited for the Runtime, and started the Turn. The refusal read above is
            # then stale, and the checks below report that Start as taken.
            if (refused := _runtime_refusal(binding, command, command_id)) is not None:
                return refused
        if _command_was_observed(binding, command_id):
            # Checked before the phase: an exact retry of a command already taken is idempotent
            # whatever the Session is doing now, and reporting it refused would make a steer that
            # landed look like it did not.
            return wire.SessionCommandVerdict(
                accepted=True,
                reason=wire.SessionCommandVerdictReason.ALREADY_OBSERVED,
            )
        if self._phase is _WorkflowPhase.CONTINUING:
            # A continue-as-new is in flight, so this command would be handed to the next run
            # and applied there without its Turn ever being compared. Refuse rather than
            # report an acceptance the comparison did not actually back.
            return wire.SessionCommandVerdict(
                accepted=False,
                reason=wire.SessionCommandVerdictReason.SESSION_CONTINUING,
            )

        expected_turn_id = (
            command.expected_turn_id if isinstance(command, wire.MessageCommand | wire.SystemCommand) else None
        )
        active_turn_id = binding.runtime.inspection.active_turn_id
        if expected_turn_id is not None and expected_turn_id != active_turn_id:
            return wire.SessionCommandVerdict(
                accepted=False,
                reason=wire.SessionCommandVerdictReason.STALE_TURN,
                active_turn_id=active_turn_id,
            )

        refusal = await self._submit(command)
        if refusal is not None:
            # Full intake dropped the command and published its rejection; reporting the
            # comparison alone would call a command that was never applied accepted.
            return wire.SessionCommandVerdict(
                accepted=False,
                reason=refusal,
                active_turn_id=binding.runtime.inspection.active_turn_id,
            )
        if (refused := _runtime_refusal(binding, command, command_id)) is not None:
            # The Runtime resolved the command while it was being delivered and refused it, which
            # happens when resolution is immediate, and always for a Start. Reporting the
            # comparison alone would call that accepted.
            if refused.reason == wire.SessionCommandVerdictReason.TURN_ACTIVE and command_id is not None:
                # The caller is told now, so the id stays free for a retry once the Turn ends.
                await binding.runtime.forget_running_start_refusal(command_id)
            return refused
        return wire.SessionCommandVerdict(accepted=True, active_turn_id=active_turn_id)

    @workflows.workflow.update(name=wire.SEND_MESSAGE_UPDATE_NAME)
    async def send_message(self, message: SendMessageInput) -> wire.SessionMessageVerdict:
        """Start a Turn or steer the running one with one message, and name that Turn.

        While Harness cannot take user input, the Update waits a bounded time, then refuses
        the message as busy with nothing applied, so the caller retries the same key.
        A retry of an accepted message gets the original Turn back. A single-turn Session
        refuses every message, steers included.
        """

        return await self._take_message(message)

    @workflows.workflow.update(name=wire.START_TURN_UPDATE_NAME)
    async def start_turn(self, message: StartTurnInput) -> wire.SessionMessageVerdict:
        """Start a Turn named after ``command_id``, only while no Turn runs.

        The Runtime decides at admission, so a running Turn answers ``turn_active`` and nothing
        is kept: the same id starts the Turn once the running one ends, as a strict local start
        does. A retry of an accepted start replays its Turn, as does a start the ``/commands``
        path took under the same id. The same id with another message conflicts.
        """

        return await self._take_message(message)

    @workflows.workflow.update(name=wire.STEER_TURN_UPDATE_NAME)
    async def steer_turn(self, message: SteerTurnInput) -> wire.SessionMessageVerdict:
        """Steer ``expected_turn_id``, only while it is the active Turn.

        The Runtime compares and commits under its input lock, so a Turn that ends first answers
        ``stale_turn`` and nothing is applied. While Harness cannot take user input, it answers
        ``session_busy`` at once, as the local runtime does. A retry of an accepted steer replays
        it, as does a steer the ``/commands`` path took under the same id.
        """

        return await self._take_message(message)

    async def _take_message(self, message: MessageUpdateInput) -> wire.SessionMessageVerdict:
        # Every outcome is a verdict: an ApplicationError would read as the input schema's refusal,
        # which the control plane takes as nothing applied.
        # Counted from the start, so the Workflow does not return before this Update answers.
        self._message_handlers_in_flight += 1
        try:
            while self._phase is _WorkflowPhase.STARTING:
                await workflows.workflow.wait_condition(lambda: self._phase is not _WorkflowPhase.STARTING)
            if self._session_id is None:
                # The Session failed before it could take commands.
                return _refuse_message(wire.SessionCommandVerdictReason.SESSION_NOT_ACCEPTING_COMMANDS)
            # Taken before the lock, so the lock wait counts against the SDK's busy wait too.
            busy_deadline = asyncio.get_running_loop().time() + wire.SEND_MESSAGE_BUSY_WAIT_SECONDS
            if isinstance(message, SendMessageInput):
                command_id = message_command_id(self._session_id, message.idempotency_key)
                digest = message_receipts.build_message_digest(message)
                # Holding the lock while busy keeps concurrent messages in arrival order.
                async with self._send_message_lock:
                    return await self._decide_message(
                        message, command_id=command_id, digest=digest, busy_deadline=busy_deadline
                    )
            # A start keeps its digest, so its key reused for another message conflicts, as for
            # send_message; a steer replays by id alone (ADR 0038). Neither waits, so both skip the
            # lock a busy send_message holds, as on the local runtime. The Runtime dedupes a
            # concurrent retry by id.
            start_digest = (
                message_receipts.build_message_digest(message) if isinstance(message, StartTurnInput) else None
            )
            return await self._decide_message(
                message, command_id=str(message.command_id), digest=start_digest, busy_deadline=busy_deadline
            )
        finally:
            self._message_handlers_in_flight -= 1

    async def _decide_message(
        self,
        message: MessageUpdateInput,
        *,
        command_id: str,
        digest: str | None,
        busy_deadline: float,
    ) -> wire.SessionMessageVerdict:
        message_entry_id = command_id if message.message_entry_id is None else message.message_entry_id
        content: list[core_protocol.ContentBlock] | None
        context_messages: list[ContextMessage] = []
        try:
            blocks, contexts = read_user_message(message)
            content = to_core_content(blocks)
            context_messages = [ContextMessage(content=to_core_content(context.content)) for context in contexts]
        except ValueError:
            content = None
        while True:
            # Before the stop check, so a retry of an accepted message is not refused for a later stop.
            receipt = self._message_receipts.get(command_id)
            if receipt is not None:
                # TODO(after 1.1.0): compare always. A start receipt carried across Continue-As-New
                # from an older worker has no digest, so its retry replays.
                if receipt.digest is not None and receipt.digest != digest:
                    return _refuse_message(wire.SessionCommandVerdictReason.IDEMPOTENCY_CONFLICT)
                if receipt.refused:
                    return _refuse_message(wire.SessionCommandVerdictReason.SESSION_NOT_ACCEPTING_COMMANDS)
                if receipt.rejected:
                    return _refuse_message(wire.SessionCommandVerdictReason.MESSAGE_REJECTED)
                if receipt.turn_id is not None:
                    return _accept_message(message_entry_id, turn_id=receipt.turn_id, steered=receipt.steered)
            binding = self._binding
            # A single-turn Session admits only its initial message, before any handler runs.
            if binding is None or self._session_stopping or self._single_turn:
                return _refuse_message(wire.SessionCommandVerdictReason.SESSION_NOT_ACCEPTING_COMMANDS)
            if not binding.session_v1:
                # Only Session v1 rows carry Session content blocks; the controller checks this first.
                # The Session is open but can never take this message: final, but not closed.
                return _refuse_message(wire.SessionCommandVerdictReason.MESSAGE_REJECTED)
            if content is None:
                # After the replay and the stop check, so an accepted key keeps its answer and a
                # closed Session answers as closed, and before any wait, since no Turn can run it.
                # The rejected receipt reserves the key: an exact retry is rejected again and other
                # content conflicts, as for a message Harness rejects.
                if receipt is None:
                    receipt = self._message_receipts.begin(command_id, digest=digest)
                receipt.rejected = True
                return _refuse_message(wire.SessionCommandVerdictReason.MESSAGE_REJECTED)
            if receipt is None and _command_was_observed(binding, command_id):
                if isinstance(message, SendMessageInput):
                    # Another command path took this id, so there is no content to compare.
                    return _refuse_message(wire.SessionCommandVerdictReason.IDEMPOTENCY_CONFLICT)
                # The same start or steer, sent first through /commands or before Continue-As-New:
                # join it for its answer.
                break
            if self._phase is _WorkflowPhase.CONTINUING:
                return _refuse_message(wire.SessionCommandVerdictReason.SESSION_CONTINUING)
            # Only send_message waits: a start would be refused while a Turn runs, and a steer
            # answers busy at once, as the local runtime does.
            if not isinstance(message, SendMessageInput) or not _session_is_busy(binding):
                break
            # Busy: nothing is buffered, so a refusal leaves no trace.
            if not await self._wait_out_busy_session(binding, busy_deadline):
                return _refuse_message(wire.SessionCommandVerdictReason.SESSION_BUSY)

        if receipt is None:
            # Stored before admission, so a message carried across Continue-As-New keeps its digest.
            receipt = self._message_receipts.begin(command_id, digest=digest)
        if isinstance(message, SteerTurnInput) and not binding.runtime.has_command(command_id):
            # One the Runtime holds, buffered by /commands in this run or carried from the last, is
            # joined below instead, so it applies once.
            return await self._commit_steer(
                binding,
                message,
                content=content,
                context_messages=context_messages,
                command_id=command_id,
                message_entry_id=message_entry_id,
                receipt=receipt,
            )
        try:
            result = await binding.receive_message(
                message,
                content=content,
                context_messages=context_messages,
                command_id=command_id,
                message_entry_id=message_entry_id,
            )
        except RuntimeError:
            # Closing the binding ends the wait for admission.
            if self._phase is _WorkflowPhase.CONTINUING:
                # The next run admits a message still buffered; a retry there gets its Turn.
                return _refuse_message(wire.SessionCommandVerdictReason.MESSAGE_CARRIED_OVER)
            if self._phase is _WorkflowPhase.TERMINAL:
                return _refuse_message(wire.SessionCommandVerdictReason.SESSION_NOT_ACCEPTING_COMMANDS)
            raise
        except temporalio.exceptions.ActivityError as error:
            # A row of the admission pass failed to publish: this message's or another command's.
            # The Runtime keeps an admitted message pending and publishes its row in the driver's
            # next admission pass; a retry with the same id replays the admission.
            logger.warning(
                "Message receipt row not published; a retry replays the admission",
                command_id=command_id,
                error_type=type(error).__name__,
            )
            return _refuse_message(wire.SessionCommandVerdictReason.RECEIPT_UNPUBLISHED)
        if isinstance(result, wire.SessionCommandVerdictReason):
            # Full intake took nothing, so the same message can be sent again.
            return self._refuse_unapplied(command_id, result)
        if isinstance(result, SessionCommandRejected) and isinstance(message, StartTurnInput):
            if _is_running_start_refusal(result.rejection):
                # Named so the caller can wait for that Turn and retry. The Runtime took it at
                # admission: the Turn can end before this handler resumes.
                active_turn_id = result.active_turn_id
                if active_turn_id is None:
                    # A refusal replayed from its receipt names no Turn. The replay did not yield,
                    # so the running Turn read now is the one that blocks this id, as on /commands.
                    active_turn_id = binding.runtime.inspection.active_turn_id
                # The caller is told now, so the id starts a Turn once the running one ends.
                await binding.runtime.forget_running_start_refusal(command_id)
                return self._refuse_unapplied(
                    command_id, wire.SessionCommandVerdictReason.TURN_ACTIVE, active_turn_id=active_turn_id
                )
        if isinstance(result, SessionCommandRejected) and isinstance(message, SteerTurnInput):
            # Only a steer /commands took gets here; that path reports Core's refusal as stale too.
            return self._refuse_unapplied(command_id, wire.SessionCommandVerdictReason.STALE_TURN)
        if not isinstance(result, SessionCommandAccepted):
            # Harness applied nothing and keeps this answer for the command id, so a retry is
            # rejected the same way rather than refused as an id another command took. Only
            # Core's invalid_command gets here: the Runtime waits out the pre-agent Hook, then
            # picks the start or steer the Session state allows.
            receipt.rejected = True
            return _refuse_message(wire.SessionCommandVerdictReason.MESSAGE_REJECTED)
        return self._accept_admitted(message, command_id, result, message_entry_id=message_entry_id, receipt=receipt)

    async def _commit_steer(
        self,
        binding: WorkflowSessionBinding,
        message: SteerTurnInput,
        *,
        content: list[core_protocol.ContentBlock],
        context_messages: list[ContextMessage],
        command_id: str,
        message_entry_id: HistoryEntryId,
        receipt: continuation.MessageReceiptRecord,
    ) -> wire.SessionMessageVerdict:
        """Steer the named Turn under the Runtime's input lock, and answer the commit.

        The Runtime keeps no answer for a steer it refuses here, so the ledger keeps none either.
        A committed steer keeps its receipt, even when its row is not published.
        """

        try:
            result = await binding.steer_active_turn(
                message,
                content=content,
                context_messages=context_messages,
                command_id=command_id,
                message_entry_id=message_entry_id,
            )
        except RuntimeError:
            # Closing the binding refuses the commit. Nothing was buffered, so no run holds the steer.
            if self._phase is _WorkflowPhase.CONTINUING:
                return self._refuse_unapplied(command_id, wire.SessionCommandVerdictReason.SESSION_CONTINUING)
            if self._phase is _WorkflowPhase.TERMINAL:
                return self._refuse_unapplied(
                    command_id, wire.SessionCommandVerdictReason.SESSION_NOT_ACCEPTING_COMMANDS
                )
            raise
        except temporalio.exceptions.ActivityError as error:
            # The steer is committed but its row is not. The receipt stays, so /commands sees the
            # id as taken: the Runtime keys a direct commit apart from what has_command reads. Its
            # Turn stays unset, so a retry commits again, which the Runtime replays, and publishes
            # the row.
            receipt.committed = True
            self._message_receipts.keep(command_id, receipt)
            logger.warning(
                "Steer receipt row not published; a retry publishes it",
                command_id=command_id,
                error_type=type(error).__name__,
            )
            return _refuse_message(wire.SessionCommandVerdictReason.RECEIPT_UNPUBLISHED)
        if isinstance(result, wire.SessionCommandVerdictReason):
            return self._refuse_unapplied(command_id, result)
        if isinstance(result, SessionCommandAccepted):
            return self._accept_admitted(
                message, command_id, result, message_entry_id=message_entry_id, receipt=receipt
            )
        if (
            isinstance(result, SessionCommandRejected)
            and isinstance(result.rejection, core_protocol.InvalidCommandRejection)
            and result.rejection.error.code == TURN_NOT_ACTIVE_CODE
        ):
            return self._refuse_unapplied(command_id, wire.SessionCommandVerdictReason.STALE_TURN)
        if _session_is_busy(binding):
            # A pre-agent Hook started after the busy check: refused for now only.
            return self._refuse_unapplied(command_id, wire.SessionCommandVerdictReason.SESSION_BUSY)
        return self._refuse_unapplied(command_id, wire.SessionCommandVerdictReason.MESSAGE_REJECTED)

    def _accept_admitted(
        self,
        message: MessageUpdateInput,
        command_id: str,
        result: SessionCommandAccepted,
        *,
        message_entry_id: HistoryEntryId,
        receipt: continuation.MessageReceiptRecord,
    ) -> wire.SessionMessageVerdict:
        # A concurrent copy of this start or steer may have been refused and dropped the receipt.
        self._message_receipts.keep(command_id, receipt)
        # A steer, or a send the Runtime joined to the active Turn, is committed into that running
        # Turn and its row is published, so it stays accepted while the Session stops: the
        # controller reads that row once the Session ended and accepts it too.
        joined_running_turn = isinstance(message, SteerTurnInput) or result.steered
        if self._session_stopping and not joined_running_turn:
            # The Session began to stop while the message that starts a Turn was admitted. The
            # Runtime may already have started that Turn and published its rows, as on the signal
            # path, but the stopping Session does not run it to its end. A retry stays refused.
            receipt.refused = True
            return _refuse_message(wire.SessionCommandVerdictReason.SESSION_NOT_ACCEPTING_COMMANDS)
        if result.turn_id is None:
            raise RuntimeError("Runtime accepted a message without a Turn identity")
        receipt.turn_id = result.turn_id
        receipt.steered = joined_running_turn
        return _accept_message(message_entry_id, turn_id=result.turn_id, steered=joined_running_turn)

    def _refuse_unapplied(
        self, command_id: str, reason: wire.SessionCommandVerdictReason, *, active_turn_id: str | None = None
    ) -> wire.SessionMessageVerdict:
        """Refuse a message that left no answer behind, dropping its receipt so a retry starts over."""

        self._message_receipts.discard_unanswered(command_id)
        return _refuse_message(reason, active_turn_id=active_turn_id)

    @workflows.workflow.update(name=wire.SUBMIT_CALLBACK_RESULT_UPDATE_NAME)
    async def submit_callback_result(self, result: harness_session.CallbackResult) -> wire.SessionCommandVerdict:
        """Answer one callback, named by its public id, and say what became of the answer.

        The callback id names the answer (ADR 0038): an id already accepted replays as accepted,
        also after the Session ended, and outputs are not compared. Otherwise the callback store
        decides. Every outcome is a verdict, as for the message Updates. Once the Session started,
        nothing awaits between the checks, so the handler needs no lock and no handler count.
        """

        while self._phase is _WorkflowPhase.STARTING:
            await workflows.workflow.wait_condition(lambda: self._phase is not _WorkflowPhase.STARTING)
        if result.callback_id in self._processed_callback_ids:
            return wire.SessionCommandVerdict(accepted=True, reason=wire.SessionCommandVerdictReason.ALREADY_OBSERVED)
        binding = self._binding
        if binding is None or self._phase is _WorkflowPhase.TERMINAL:
            return wire.SessionCommandVerdict(
                accepted=False, reason=wire.SessionCommandVerdictReason.SESSION_NOT_ACCEPTING_COMMANDS
            )
        submission = binding.submit_callback_result(result)
        if isinstance(submission, worker_callbacks.CallbackRejection):
            return wire.SessionCommandVerdict(
                accepted=False, reason=wire.SessionCommandVerdictReason.CALLBACK_REJECTED, message=submission.reason
            )
        if submission is not worker_callbacks.CallbackSubmission.ACCEPTED:
            return wire.SessionCommandVerdict(accepted=False, reason=_CALLBACK_REFUSAL_REASONS[submission])
        # Session v1 publishes no receipt row for an answer: the Runtime publishes its resolution.
        _record_processed_callback(self._processed_callback_ids, result.callback_id)
        return wire.SessionCommandVerdict(accepted=True)

    async def _wait_out_busy_session(self, binding: WorkflowSessionBinding, deadline: float) -> bool:
        """Return True if the busy wait ended before ``deadline``.

        Only a wake hint: the next attempt checks admission again.
        """

        # The Workflow event loop clock is the deterministic Workflow time.
        remaining = deadline - asyncio.get_running_loop().time()
        if remaining <= 0:
            return False
        try:
            await workflows.workflow.wait_condition(
                lambda: (
                    self._phase is not _WorkflowPhase.ACCEPTING_COMMANDS
                    or self._stop_requested
                    or not _session_is_busy(binding)
                ),
                timeout=remaining,
            )
        except TimeoutError:
            return False
        return True

    @workflows.workflow.signal(name="submit_command")
    async def submit_command(self, command: wire.SessionWorkflowCommand) -> None:
        await self._submit(command)

    async def _submit(self, command: wire.SessionWorkflowCommand) -> wire.SessionCommandVerdictReason | None:
        """Handle one command; return why full intake refused it, or None otherwise."""

        while self._phase is _WorkflowPhase.STARTING:
            await workflows.workflow.wait_condition(lambda: self._phase is not _WorkflowPhase.STARTING)
        binding = self._binding
        if binding is None or self._phase is _WorkflowPhase.TERMINAL:
            return None
        command_id = _command_id(command)
        self._command_handlers_in_flight += 1
        try:
            return await self._handle_command(binding, command, command_id=command_id)
        finally:
            self._command_handlers_in_flight -= 1

    async def _handle_command(
        self,
        binding: WorkflowSessionBinding,
        command: wire.SessionWorkflowCommand,
        *,
        command_id: str | None,
    ) -> wire.SessionCommandVerdictReason | None:
        stopping = isinstance(command, wire.SystemCommand) and command.action == "stop"
        stop_requested = self._stop_requested
        end_cause = self._end_cause
        if stopping:
            # Set while the stop is delivered, so a Turn boundary meanwhile does not continue as new.
            self._stop_requested = True
            if self._end_cause is None and isinstance(command, wire.SystemCommand):
                # A parent that ended at a limit stops its children with the same cause.
                self._end_cause = _limit_cause(command)
                if self._end_cause is not None:
                    binding.condition_waiter.notify_changed()
        if not isinstance(
            command,
            wire.MessageCommand | wire.CallbackResultCommand | wire.SystemCommand,
        ):
            return None
        if isinstance(command, wire.SystemCommand) and command.action != "interrupt":
            if command.action != "stop":
                return None

        if isinstance(command, wire.CallbackResultCommand):
            processed = binding.publications.processed_callback_ids
            if command_id is not None and command_id in processed:
                return None
            try:
                result = worker_callbacks.callback_result_from_command(command)
            except ValueError as error:
                # An answer with an invalid content block is refused; a signal has no reply, so the reason is logged.
                logger.warning(
                    "Refused a callback result; the callback stays open",
                    callback_id=str(command.callback_id),
                    reason=str(error),
                )
                return None
            submission = binding.submit_callback_result(result)
            if submission is not worker_callbacks.CallbackSubmission.ACCEPTED:
                return None

            await lifecycle.emit_command_receipt(
                command,
                session_id=binding.session_id,
                session_v1=binding.session_v1,
            )
            if command_id is not None:
                _record_processed_callback(processed, command_id)
            return None
        if (
            stopping
            and isinstance(command, wire.SystemCommand)
            and command.expected_turn_id is None
            and self._phase is _WorkflowPhase.ACCEPTING_COMMANDS
            and not binding.runtime.turn_in_progress
            and _idle_stop_ends_session()
        ):
            # No Turn to interrupt: the stop ends the serve loop and is accepted, as a stop at a limit is.
            binding.condition_waiter.notify_changed()
            return None
        if self._phase is _WorkflowPhase.CONTINUING:
            refusal = await binding.buffer_command(command)
        else:
            # The product command id is the Runtime identity, so retries and receipts match it.
            refusal = await binding.deliver_command(command, source_id=command_id)
        if stopping and refusal is not None:
            # A full intake refused the stop, and the client is told so: the Workflow keeps running.
            self._stop_requested = stop_requested
            if self._end_cause != end_cause:
                # The limit watch waits for a limit again.
                self._end_cause = end_cause
                binding.condition_waiter.notify_changed()
        return refusal

    async def stop_at_limit(self, cause: wire.SessionLimitCause) -> None:
        """Stop the Session because it reached `cause`, as a stop command would."""

        self._end_cause = cause
        binding = self._binding
        if binding is not None:
            if not binding.runtime.turn_in_progress:
                # No Turn to interrupt: end the serve loop without a command outcome for a client.
                self._stop_requested = True
                binding.condition_waiter.notify_changed()
                return
        await self._submit(
            wire.SystemCommand(
                # Deterministic in a Workflow; tests drive the binding outside one.
                command_id=workflows.workflow.uuid4() if temporalio.workflow.in_workflow() else uuid4(),
                action="stop",
                reason=_LIMIT_STOP_REASONS[cause],
                cause=cause.value,
            )
        )

    def begin_continuation(self) -> None:
        """Route new signals into the serialized handoff before cleanup awaits."""

        if self._phase is not _WorkflowPhase.ACCEPTING_COMMANDS:
            raise RuntimeError(f"Cannot continue a Workflow in phase {self._phase.value!r}")
        self._phase = _WorkflowPhase.CONTINUING

    def attach_binding(self, binding: WorkflowSessionBinding, *, single_turn: bool = False) -> None:
        if self._phase is not _WorkflowPhase.STARTING:
            raise RuntimeError(f"Cannot attach a binding in phase {self._phase.value!r}")
        self._binding = binding
        self._single_turn = single_turn
        self._session_id = binding.session_id
        # Kept past the binding, so a retry of an accepted message is answered after the Session ends.
        self._message_receipts = message_receipts.MessageReceiptLedger(binding.publications.message_receipts)
        self._processed_callback_ids = binding.publications.processed_callback_ids
        self._phase = _WorkflowPhase.ACCEPTING_COMMANDS

    def mark_terminal(self) -> None:
        self._phase = _WorkflowPhase.TERMINAL
        self._binding = None

    @property
    def continuation_started(self) -> bool:
        return self._phase is _WorkflowPhase.CONTINUING

    @property
    def terminal(self) -> bool:
        return self._phase is _WorkflowPhase.TERMINAL

    @property
    def command_handlers_idle(self) -> bool:
        return self._command_handlers_in_flight == 0

    async def drain_command_handlers(self) -> None:
        await workflows.workflow.wait_condition(lambda: self.command_handlers_idle)

    @property
    def message_handlers_idle(self) -> bool:
        return self._message_handlers_in_flight == 0

    @property
    def _session_stopping(self) -> bool:
        return self._phase is _WorkflowPhase.TERMINAL or self._stop_requested


def _invalid_command_update(message: str) -> ApplicationError:
    # An ApplicationError rejects only this Update (the Workflows API answers 422); any other
    # exception would fail the Workflow Task and replay it, stalling the Session.
    return ApplicationError(message, type="INVALID_COMMAND_UPDATE", non_retryable=True)


def _runtime_refusal(
    binding: WorkflowSessionBinding,
    command: wire.SessionWorkflowCommand,
    command_id: str | None,
) -> wire.SessionCommandVerdict | None:
    """The refusal of a message or interrupt the Runtime rejected, or None if it did not."""

    if command_id is None or not isinstance(command, wire.MessageCommand | wire.SystemCommand):
        return None
    result = binding.runtime.get_command_result(command_id)
    if not isinstance(result, SessionCommandRejected):
        return None
    reason = wire.SessionCommandVerdictReason.STALE_TURN
    if isinstance(command, wire.MessageCommand) and command.expected_turn_id is None:
        # A Start is refused because a Turn is running, or otherwise for good.
        reason = (
            wire.SessionCommandVerdictReason.TURN_ACTIVE
            if _is_running_start_refusal(result.rejection)
            else wire.SessionCommandVerdictReason.MESSAGE_REJECTED
        )
    return wire.SessionCommandVerdict(
        accepted=False,
        reason=reason,
        active_turn_id=binding.runtime.inspection.active_turn_id,
    )


def _steer_command(
    message: SteerTurnInput,
    *,
    content: list[core_protocol.ContentBlock],
    command_id: str,
    message_entry_id: HistoryEntryId,
    context_messages: list[ContextMessage],
) -> SteerTurnCommand:
    return SteerTurnCommand(
        turn_id=message.expected_turn_id,
        content=content,
        message_entry_id=message_entry_id,
        context_messages=context_messages,
        idempotency_key=command_id,
    )


def _is_running_start_refusal(rejection: core_protocol.CommandRejection) -> bool:
    return isinstance(rejection, core_protocol.InvalidStateRejection) and rejection.state == "running"


_CALLBACK_REFUSAL_REASONS: dict[worker_callbacks.CallbackSubmission, wire.SessionCommandVerdictReason] = {
    worker_callbacks.CallbackSubmission.SETTLED: wire.SessionCommandVerdictReason.CALLBACK_SETTLED,
    worker_callbacks.CallbackSubmission.UNKNOWN: wire.SessionCommandVerdictReason.CALLBACK_UNKNOWN,
}


def _record_processed_callback(processed: list[str], callback_id: str) -> None:
    """Remember an accepted answer by its id, within the carried window, so a retry replays."""

    processed.append(callback_id)
    del processed[:-_MAX_CARRIED_COMMAND_IDS]


def _session_is_busy(binding: WorkflowSessionBinding) -> bool:
    """Whether Harness takes no user input now, while a pre-agent Hook runs."""

    return (
        determine_active_turn_command_admission(binding.runtime.inspection) is ActiveTurnCommandAdmission.INTERRUPT_ONLY
    )


def _command_was_observed(binding: WorkflowSessionBinding, command_id: str | None) -> bool:
    if command_id is None:
        return False
    return (
        command_id in binding.publications.commands
        # Pending too: a command buffered without a publication, such as an agent message, holds the id.
        or binding.runtime.has_command(command_id)
        or command_id in binding.publications.processed_callback_ids
        or command_id in binding.publications.message_receipts
    )


def build_workflow_class(
    *,
    name: str,
    agent: sdk_agent.AgentAuthoring,
    harness: contracts.Harness,
    subagent_policy: SubagentPolicy | None = None,
    session_control_plane: worker_control_plane.WorkflowSessionControlPlaneBinding | None = None,
    program_policy: ProgramExecutionPolicy = DEFAULT_PROGRAM_EXECUTION_POLICY,
    wait_policy: ModelWaitPolicy = DEFAULT_MODEL_WAIT_POLICY,
    turn_policy: TurnExecutionPolicy = DEFAULT_TURN_EXECUTION_POLICY,
    intake_limits: SessionIntakeLimits = DEFAULT_SESSION_INTAKE_LIMITS,
    sandbox_lifecycle_factory: SandboxLifecycleFactory | None = None,
) -> type:
    """Build the decorated control-plane Workflow around a Harness Session Host."""

    # A static policy has nothing to call without a binding. Every deployed worker has a binding,
    # but only an agent with subagents or a subagent policy serves them: anyone who can start the
    # Workflow writes the start input's policy and child Session, so they cannot enable subagents.
    if subagent_policy is not None and session_control_plane is None:
        raise ValueError("A subagent policy requires a Session-control-plane binding")
    declares_subagents = agent._to_agent_config().effective_subagent_policy() is not None
    serves_subagents = session_control_plane is not None and (subagent_policy is not None or declares_subagents)
    if serves_subagents:
        _reject_unborrowable_subagent_sandbox(harness.sandbox)
    if isinstance(harness.sandbox, contracts.MistralSandbox):
        from mistralai.vibe_agents.sdk.sandbox.koyeb import (  # noqa: PLC0415
            register_koyeb_sandbox_activities,
        )

        register_koyeb_sandbox_activities()
    settings = config.get_app_settings()
    # Only a Workflow that serves subagents looks its binding up. The second check only narrows the type.
    if serves_subagents and session_control_plane is not None:
        worker_control_plane.register_control_plane_binding(name, session_control_plane)
    frozen_agent = agent.model_copy()
    frozen_harness = harness.copy_for_isolation()
    # Run before _reject_stateful_workflow_hooks: assembly names specific unsupported hooks (e.g.
    # ExecutorCredentials) precisely, instead of the generic "stateful hook" message.
    frozen_assembly = assemble.assemble_agent(
        frozen_agent._to_agent_config(),
        frozen_harness,
        permission_mode=frozen_agent.permission_mode,
        subagents=frozen_agent.subagents,
        capability_provider_id=name,
        tool_errors=frozen_agent.tool_errors,
    )
    frozen_definition = frozen_assembly.harness_definition
    on_behalf_of = contracts.requires_on_behalf_of(frozen_harness, frozen_agent.subagents)
    # Before any Session starts: a Session's sandbox write resolves its references through the
    # resolver this registers and the local skill bytes it keeps in this process.
    frozen_skills = worker_skills.prepare(frozen_assembly.skills)
    _reject_stateful_workflow_hooks(frozen_harness, frozen_agent.subagents)
    frozen_sandbox = frozen_harness.sandbox

    async def run(
        self: _UnifiedHarnessControlPlaneWorkflow,
        params: wire.SessionWorkflowStartInput,
    ) -> wire.SessionWorkflowOutput:
        return await _serve(
            self,
            frozen_definition,
            frozen_sandbox,
            params,
            settings,
            session_input_classes=frozen_assembly.session_input_classes,
            skills=frozen_skills,
            subagent_policy=subagent_policy,
            control_plane_binding_id=name if serves_subagents else None,
            program_policy=program_policy,
            wait_policy=wait_policy,
            turn_policy=turn_policy,
            intake_limits=intake_limits,
            # The authored description, not the generated workflow description fallback.
            agent_description=frozen_agent.description,
            sandbox_lifecycle_factory=sandbox_lifecycle_factory,
            on_behalf_of=on_behalf_of,
        )

    return _define_session_workflow(run, name=name, on_behalf_of=on_behalf_of, settings=settings)


def build_shared_worker_workflow_class(*, on_behalf_of: bool) -> type:
    """Build the Session Workflow that runs the data-only Agent named by each Session's input.

    A Session pins its Agent through the start input, which continue-as-new and resurrection
    carry forward, so a redeploy of the Agent only changes the Sessions that start after it.
    """

    name = wire.shared_worker_workflow_name(on_behalf_of=on_behalf_of)
    settings = config.get_app_settings()

    async def run(
        self: _UnifiedHarnessControlPlaneWorkflow,
        params: wire.SessionWorkflowStartInput,
    ) -> wire.SessionWorkflowOutput:
        definition, sandbox = _compile_shared_worker_agent(params, name=name, on_behalf_of=on_behalf_of)
        # Validated by the compile above. Names the Agent in GenAI traces, as a code-defined Agent's description does.
        description = wire.SharedWorkerAgentSpec.model_validate(params.shared_worker_agent).agent.description
        return await _serve(
            self, definition, sandbox, params, settings, agent_description=description, on_behalf_of=on_behalf_of
        )

    return _define_session_workflow(
        run,
        name=_name_before_configured_prefix(name),
        on_behalf_of=on_behalf_of,
        settings=settings,
    )


def _name_before_configured_prefix(name: str) -> str:
    # A shared worker usually runs with WORKFLOW_NAME_PREFIX=__shared- so that the Workflow SDK's own
    # Workflows get the prefix a reserved namespace requires. The SDK then prefixes every defined
    # name, so the name is defined without the prefix it already carries.
    prefix = workflow_config.worker.workflow_name_prefix
    if not prefix:
        return name
    if not name.startswith(prefix):
        raise ValueError(f"WORKFLOW_NAME_PREFIX {prefix!r} would rename {name!r}; the control plane routes to {name!r}")
    return name.removeprefix(prefix)


def _compile_shared_worker_agent(
    params: wire.SessionWorkflowStartInput,
    *,
    name: str,
    on_behalf_of: bool,
) -> tuple[WorkflowHarnessDefinition, contracts.Sandbox]:
    # Every failure here is permanent for this input, so it fails the execution instead of a
    # Workflow task that Temporal would retry forever.
    if params.shared_worker_agent is None:
        raise _invalid_shared_worker_agent(f"Agent {params.agent_name!r} has no shared worker definition")
    # A spec from a newer control plane can carry a field this worker does not know, which the
    # spec refuses.
    try:
        spec = wire.SharedWorkerAgentSpec.model_validate(params.shared_worker_agent)
    except ValidationError as error:
        raise _invalid_shared_worker_agent(
            f"Agent {params.agent_name!r} cannot run on the shared worker: {error}"
        ) from error
    # Checked here, not only at deploy: anyone can start the shared Workflow with any spec.
    if egress_issues := wire.shared_worker_egress_issues(spec):
        raise _invalid_shared_worker_agent(
            f"Agent {params.agent_name!r} cannot run on the shared worker: {'; '.join(egress_issues)}"
        )
    # The shared worker authenticates with identity headers, which the Sandbox Proxy bootstrap does
    # not take yet.
    if isinstance(spec.sandbox, wire.SharedWorkerMistralSandbox) and spec.sandbox.sandbox_proxy is not None:
        raise _invalid_shared_worker_agent(
            f"Agent {params.agent_name!r} cannot run on the shared worker: it does not run Sandbox Proxy yet"
        )
    # The SDK's own rules on a valid spec raise ValueError (SdkError included). Anything else is
    # a worker defect, left to fail the Workflow task where it shows.
    try:
        definition, sandbox = shared_worker.compile_shared_worker_spec(
            spec,
            agent_name=params.agent_name,
            capability_provider_id=name,
            session_id=str(params.session_id),
        )
    except ValueError as error:
        raise _invalid_shared_worker_agent(
            f"Agent {params.agent_name!r} cannot run on the shared worker: {error}"
        ) from error
    if spec.requires_on_behalf_of() and not on_behalf_of:
        raise _invalid_shared_worker_agent(
            f"Agent {params.agent_name!r} needs the executing user's credentials; route it to "
            f"{wire.SHARED_WORKER_ON_BEHALF_OF_WORKFLOW_NAME}"
        )
    return definition, sandbox


def _invalid_shared_worker_agent(message: str) -> temporalio.exceptions.ApplicationError:
    return temporalio.exceptions.ApplicationError(message, type="InvalidSharedWorkerAgent", non_retryable=True)


def _define_session_workflow(
    run: Callable[[_UnifiedHarnessControlPlaneWorkflow, wire.SessionWorkflowStartInput], Awaitable[object]],
    *,
    name: str,
    on_behalf_of: bool,
    settings: config.AppSettings,
) -> type:
    run.__name__ = "run"
    run.__qualname__ = "UnifiedHarnessControlPlaneWorkflow.run"
    cls = type(
        "UnifiedHarnessControlPlaneWorkflow",
        (_UnifiedHarnessControlPlaneWorkflow,),
        {"run": workflows.workflow.entrypoint(run), "__plugin_metadata__": {"tags": [_AGENT_WORKFLOW_TAG]}},
    )
    return workflows.workflow.define(
        name=name,
        enforce_determinism=False,
        execution_timeout=settings.execution_timeout,
        on_behalf_of=on_behalf_of,
    )(cls)


def _bind_declared_session_inputs(
    definition: WorkflowHarnessDefinition,
    sandbox: sandbox_assembly.AgentsSdkSandbox,
    session_inputs: Mapping[str, JsonValue],
    *,
    sandbox_is_live: bool,
) -> None:
    try:
        session_input_assembly.bind_session_inputs(
            definition.agent_config, sandbox, session_inputs, sandbox_is_live=sandbox_is_live
        )
    except ValueError as error:
        raise SessionInputsUnresolvedError(str(error)) from error


def _session_observation_context(
    attribution: ObservationContext | None,
    turn_context: CompletionObservationContext | None,
) -> CompletionObservationContext | None:
    if attribution is None or turn_context is None:
        return attribution or turn_context
    turn_factory = observation_context_factory(turn_context)

    def for_turn(turn_id: str | None) -> ObservationContext:
        turn = turn_factory(turn_id)
        return ObservationContext(attributes={**attribution.attributes, **(turn.attributes if turn else {})})

    return for_turn


def _sandbox_proxy_identity(principal: wire.Principal | None) -> dict[str, str] | None:
    if principal is None or principal.user_id is None:
        return None
    return {
        "customer_id": str(principal.customer_id),
        "user_id": str(principal.user_id),
        "workspace_id": str(principal.workspace_id),
        "organization_id": str(principal.organization_id),
    }


def _reject_unborrowable_subagent_sandbox(sandbox: contracts.Sandbox) -> None:
    """Fail the build when a Workflow with subagents has a Sandbox its children cannot share.

    Any such Sandbox would otherwise fail when the root Session opens, not when it is built.
    """

    if contracts.subagents_can_share_sandbox(sandbox):
        return
    raise UnsupportedAgentFeatureError(
        "subagents_with_unborrowable_sandbox",
        (
            f"a Workflow with subagents cannot use {type(sandbox).__name__}: child Sessions share the "
            "root's Sandbox, and only MistralSandbox can be shared today. Use MistralSandbox or "
            "NoSandbox, or build the Workflow without a subagent policy"
        ),
    )


def _reject_stateful_workflow_hooks(
    harness: contracts.Harness,
    subagents: Sequence[assemble.AuthoredSubagent] = (),
) -> None:
    """Reject Hooks that keep state outside their fields.

    An activity rebuilds each Hook from its class and saved fields, so anything else is lost. Every
    ``agents.Subagent`` in the tree, nested ones included, runs its Hooks through the same
    activities as the root, so each level is checked. Assembly has already checked that each Hook
    can be rebuilt.
    """

    layers: list[tuple[tuple[str, ...], Sequence[contracts.Hook]]] = [
        ((), (*harness.guardrails, *harness.hooks)),
        *((path, layer.hooks or ()) for path, layer in subagent_assembly.authored_subagent_layers(subagents)),
    ]
    for path, hooks in layers:
        for hook in hooks:
            owner = f" on subagent {'/'.join(path)!r}" if path else ""
            reason = contracts.legacy_hook_reason(hook)
            if reason is not None:
                raise UnsupportedAgentFeatureError(
                    "stateful_workflow_hook",
                    (
                        f"stateful Hook {type(hook).__name__}{owner} cannot run through Workflow activities: "
                        f"{reason}; declare it as a field or PrivateAttr"
                    ),
                )


async def _resolve_session_caller(settings: config.AppSettings, *, on_behalf_of: bool) -> wire.Principal | None:
    """The attested caller, or None for a Workflow that acts for no user and forwards no identity.

    Identity headers make internal services act as the caller, so they need it attested: resolving it
    fails the Session when the execution does not run on behalf of a user.
    """
    if not on_behalf_of and not settings.use_identity_headers:
        return None
    return await session_caller.resolve_session_caller()


def _build_event_publisher(
    params: wire.SessionWorkflowStartInput,
    *,
    session_v1: bool,
) -> SessionEventPublisher:
    if session_v1:
        return SessionV1HarnessEventPublisher(session_id=str(params.session_id))
    return events.LegacyTaskSessionEventPublisher()


def _definition_children_inherit(definition: WorkflowHarnessDefinition) -> WorkflowHarnessDefinition:
    """The definition a Session derives its children from: no sandbox, and a normalized completion.

    Typed provider settings retain environment references, never resolved API keys.
    """

    completion = parse_completion_config(definition.agent_config.completion)
    inherited = definition.with_runtime_sandbox(sandbox=None, workdir=definition.agent_config.workdir)
    return inherited.model_copy(
        update={
            "agent_config": inherited.agent_config.model_copy(update={"completion": completion.model_dump(mode="json")})
        }
    )


async def _serve(
    workflow: _UnifiedHarnessControlPlaneWorkflow,
    definition: WorkflowHarnessDefinition,
    sandbox: contracts.Sandbox,
    params: wire.SessionWorkflowStartInput,
    settings: config.AppSettings,
    *,
    # Empty for a data-only Agent, which has no Session input classes.
    session_input_classes: Mapping[str, type[contracts.SessionInput]] = MappingProxyType({}),
    skills: sandbox_skills.SandboxSkillFiles | None = None,
    subagent_policy: SubagentPolicy | None = None,
    control_plane_binding_id: str | None = None,
    program_policy: ProgramExecutionPolicy = DEFAULT_PROGRAM_EXECUTION_POLICY,
    wait_policy: ModelWaitPolicy = DEFAULT_MODEL_WAIT_POLICY,
    turn_policy: TurnExecutionPolicy = DEFAULT_TURN_EXECUTION_POLICY,
    intake_limits: SessionIntakeLimits = DEFAULT_SESSION_INTAKE_LIMITS,
    agent_description: str | None = None,
    sandbox_lifecycle_factory: SandboxLifecycleFactory | None = None,
    on_behalf_of: bool = False,
) -> wire.SessionWorkflowOutput:
    restored = continuation.build_continuation_state(params)
    carried_limits = restored.limits if restored is not None else None

    def observation_context_for_turn(turn_id: str | None) -> ObservationContext:
        attributes = {"session_id": str(params.session_id)}
        if turn_id is not None:
            attributes["first_message_id"] = turn_id
        return ObservationContext(attributes=attributes)

    if restored is not None:
        workflow._stop_requested = restored.stop_requested
        if carried_limits is not None and carried_limits.end_cause is not None:
            workflow._end_cause = wire.SessionLimitCause(carried_limits.end_cause)
    started_at_unix_ms = carried_limits.started_at_unix_ms if carried_limits is not None else _workflow_time_unix_ms()
    limits = session_limits.SessionLimits(
        lifetime_deadline_unix_ms=started_at_unix_ms + int(settings.lifetime_limit_seconds * 1000),
        # Worker configuration only: the per-Session `inactive_timeout_seconds` is for the VCW Workflow.
        idle_limit_ms=int(settings.idle_timeout_seconds * 1000),
        grace_seconds=settings.limit_grace_seconds,
    )
    limit_clock: session_limits.SessionLimitClock | None = None
    binding: WorkflowSessionBinding | None = None
    last_message: str | None = None
    failure_message: str | None = None
    termination = wire.TerminationReason.COMPLETED
    primary_error: BaseException | None = None
    turn_finished = False
    # A stop carried across Continue-As-New still owes the carried Turns their interrupt outcome.
    carried_turn_ids: set[str] = set()

    def record_turn_result(turn_id: str, result: TurnRunResult) -> None:
        nonlocal last_message, turn_finished
        turn_finished = True
        carried_turn_ids.discard(turn_id)
        if binding is not None:
            binding.runtime_metrics.turn_finished(turn_id, result)
        if isinstance(result, TurnCompleted):
            last_message = "".join(
                block.text for block in result.output if isinstance(block, core_protocol.TextContentBlock)
            )
        elif isinstance(result, TurnFailed):
            if _single_turn(params):
                raise HarnessCompletionFailedError(result.error)

    try:
        accepted = start_input.read_start_input(
            params,
            definition,
            static_subagent_policy=subagent_policy,
            bound=control_plane_binding_id is not None,
            skill_files=skills,
        )
        definition, child_session, subagent_policy = (
            accepted.definition,
            accepted.child_session,
            accepted.subagent_policy,
        )
        lineage, session_v1 = accepted.lineage, accepted.session_v1
        # Never from the start input, which the caller writes. Resolved on every run: each run has
        # its own execution token, which the Workflows API attests for the user who started the first.
        principal = await _resolve_session_caller(settings, on_behalf_of=on_behalf_of)
        completion_http_headers: dict[str, str] | None = None
        completion_http_headers_provider: Callable[[], Awaitable[Mapping[str, str]]] | None = None
        if settings.use_identity_headers and principal is not None:
            completion_http_headers = assemble.build_completion_http_headers(
                principal, correlation_id=params.correlation_id
            )
            completion_http_headers_provider = functools.partial(
                customer_metadata.fetch_customer_completion_headers, str(principal.customer_id)
            )
        control_plane = (
            worker_control_plane.ActivitySessionControlPlane(
                control_plane_binding_id, execution_token=worker_control_plane.workflow_execution_token()
            )
            if control_plane_binding_id is not None
            else None
        )
        if child_session is not None:
            if control_plane is None:
                # read_start_input already refuses an unbound child; never let one skip the check.
                raise start_input.reject_start_input(
                    params,
                    start_input.StartInputRefusal(
                        "Child Session requires the configured Session-control-plane binding"
                    ),
                )
            # Before anything opens: no sandbox is attached and no tool runs for a child the
            # Agents API did not start.
            await start_input.verify_child_session(params, child_session, control_plane)
        sandbox_lifecycle = (
            sandbox_lifecycle_factory(params, principal, restored.sandbox_lifecycle if restored is not None else None)
            if sandbox_lifecycle_factory is not None and child_session is None and subagent_policy is None
            else None
        )
        try:
            binding = await WorkflowSessionBinding.open(
                definition=definition,
                sandbox=sandbox,
                principal=principal,
                session_id=str(params.session_id),
                session_inputs=session_input_assembly.with_omitted_optional_inputs(
                    session_input_classes, params.session_inputs or {}
                ),
                restored=restored,
                skills=skills,
                event_publisher=_build_event_publisher(params, session_v1=session_v1),
                session_v1=session_v1,
                subagent_policy=subagent_policy,
                control_plane=control_plane,
                child_session=child_session,
                lineage=lineage,
                program_policy=program_policy,
                wait_policy=wait_policy,
                turn_policy=turn_policy,
                intake_limits=intake_limits,
                callback_timeout=settings.callback_timeout,
                sandbox_provisioning_timeout=timedelta(seconds=settings.sandbox_provisioning_timeout_seconds),
                completion_http_headers_provider=completion_http_headers_provider,
                completion_observation_context=observation_context_for_turn,
                completion_http_headers=completion_http_headers,
                genai_agent=_genai_agent(params, child_session, agent_description),
                sandbox_lifecycle=sandbox_lifecycle,
                agent_id=params.agent_id,
                application_id=params.application_id,
                correlation_id=params.correlation_id,
                telemetry_enabled=settings.telemetry_enabled,
            )
        except ValueError as error:
            # A child's start request carries fields its caller wrote (conversation, sandbox, context,
            # Session inputs), which the binding reads as it opens: refuse them as the start input is
            # refused. A Session input error has its own answer, which names only identifiers.
            if child_session is None or isinstance(error, SessionInputsUnresolvedError):
                raise
            raise start_input.reject_start_input(params, error) from error
        if restored is not None:
            bootstrap_pending = restored.bootstrap_metric_pending
        else:
            bootstrap_pending = (
                isinstance(params.initial_command, wire.MessageCommand) or params.initial_turn is not None
            )
        binding.runtime_metrics.run_started(
            enabled=settings.runtime_metrics_enabled, bootstrap_pending=bootstrap_pending
        )
        if restored is None:
            await lifecycle.emit_session_started(params)
            if isinstance(params.initial_command, wire.MessageCommand):
                admitted = await binding.admit_message(params.initial_command)
                if isinstance(admitted, SessionCommandRejected) and isinstance(
                    admitted.rejection, core_protocol.QueueFullRejection
                ):
                    # The intake is empty at start, so this message alone exceeds it and no retry
                    # can fit. Fail the Session rather than idle until the inactivity timeout.
                    await binding.reject_initial_message(admitted)
                    raise InitialMessageRejectedError(_initial_message_too_large(intake_limits.pending_bytes))
            elif params.initial_turn is not None:
                await binding.start_initial_turn(params.initial_turn)
        elif restored.stop_requested:
            carried_turn_ids.update(binding.runtime.state.turns_to_drive)
        workflow.attach_binding(binding, single_turn=_single_turn(params))
        runtime = binding.runtime

        def stop_requested() -> bool:
            if _single_turn(params) and turn_finished:
                return True
            if not workflow._stop_requested:
                return False
            # Wait only for carried Turns still to be driven: a finished Turn the Runtime drops from
            # turns_to_drive without driving it never reaches on_turn_finished.
            return not carried_turn_ids or carried_turn_ids.isdisjoint(runtime.state.turns_to_drive)

        callbacks = binding.callbacks
        limit_clock = session_limits.SessionLimitClock(
            limits,
            is_idle=lambda: session_limits.session_is_idle(runtime, callbacks),
            stopped_by=lambda: workflow._end_cause,
            now_unix_ms=_workflow_time_unix_ms,
            condition_waiter=binding.condition_waiter,
            idle_since_unix_ms=carried_limits.idle_since_unix_ms if carried_limits is not None else None,
        )
        checkpointing = asyncio.create_task(binding.watch_sandbox_idle()) if sandbox_lifecycle is not None else None
        try:
            result = await _serve_within_limits(
                workflow,
                binding,
                limit_clock,
                limits,
                binding.runtime.serve(
                    on_turn_finished=record_turn_result,
                    stop_requested=stop_requested,
                    continuation_policy=_WorkflowContinuationPolicy(lambda: workflow._stop_requested),
                ),
            )
        finally:
            if checkpointing is not None:
                checkpointing.cancel()
                await asyncio.gather(checkpointing, return_exceptions=True)
        if result == "continuation":
            bootstrap_metric_pending = binding.runtime_metrics.continuation_requested()
            workflow.begin_continuation()
            await workflow.drain_command_handlers()
            state = await binding.close_for_continuation(settle_inbound=workflow.drain_command_handlers)
            state.stop_requested = workflow._stop_requested
            state.bootstrap_metric_pending = bootstrap_metric_pending
            state.limits = continuation.SessionLimitState(
                started_at_unix_ms=started_at_unix_ms,
                idle_since_unix_ms=limit_clock.idle_since_unix_ms,
                end_cause=workflow._end_cause,
            )
            # Closing ended every message Update's wait for admission; each one answers in this run.
            await _drain_message_handlers(workflow)
            workflows.workflow.continue_as_new(continuation.build_continue_as_new_input(params, state))
            raise RuntimeError("continue_as_new returned instead of restarting the Workflow")
        if result == "forced_end":
            # The stop at a limit did not end the Session within its grace period. The Turns it
            # leaves unfinished are cancelled, so the parent's child operations do not stay running.
            termination = wire.TerminationReason.STOPPED
            cause = workflow._end_cause
            await binding.runtime.report_session_end_to_parent(
                CancelledTermination(reason=_LIMIT_STOP_REASONS[cause] if cause else None, cause=cause)
            )
        elif workflow._stop_requested:
            termination = wire.TerminationReason.STOPPED
    except asyncio.CancelledError as error:
        primary_error = error
        termination = wire.TerminationReason.STOPPED
    except HarnessCompletionFailedError as error:
        primary_error = error
        termination = wire.TerminationReason.FAILED
        failure_message = error.error.message or None
    except InitialMessageRejectedError as error:
        primary_error = error
        termination = wire.TerminationReason.FAILED
        failure_message = str(error)
    except (SessionInputsUnresolvedError, sandbox_assembly.SandboxHookFailedError) as error:
        # A Workflow-code exception would otherwise retry the Workflow task forever, so a
        # Session that cannot resolve its inputs or run its sandbox hooks fails. The message
        # names only identifiers. Only a hook failure is logged with its cause and any sandbox
        # delete note: an input error's cause can carry the rejected input value.
        if isinstance(error, sandbox_assembly.SandboxHookFailedError) and not workflow_is_replaying():
            logger.warning("Sandbox hook on_create failed", exc_info=error)
        primary_error = error
        termination = wire.TerminationReason.FAILED
        failure_message = str(error)
    except start_input.StartInputRejectedError as error:
        primary_error = error
        termination = wire.TerminationReason.FAILED
        failure_message = str(error)
    except MistralConnectorNotFoundError as error:
        # No retry fixes a wrong connector name, so the Session fails with a message that names it.
        # The Agents SDK's connector resource reports a wrong name as an unsupported connector
        # instead; this is for a resource that still raises it.
        primary_error = error
        termination = wire.TerminationReason.FAILED
        failure_message = str(error)
        if binding is not None:
            await binding.runtime.report_session_failure_to_parent(
                ProtocolError(message=failure_message, code=SESSION_FAILED_ERROR_CODE)
            )
    except Exception as error:
        primary_error = error
        sandbox_refusal = sandbox_create_refusal(error)
        if sandbox_refusal is not None:
            # No retry creates the sandbox, and the refusal says what to fix: the Session's
            # error carries it, where Temporal would give only "Activity task failed".
            if not workflow_is_replaying():
                logger.warning(
                    "session_sandbox_create_refused", session_id=str(params.session_id), error_message=sandbox_refusal
                )
        elif _ends_workflow_through_temporal(error):
            raise
        elif not workflow_is_replaying():
            # Temporal would retry the Workflow task until the execution timeout, holding the
            # child's slot and ignoring interrupts. End the Session failed instead.
            # Rendering a traceback on the workflow thread can outlast Temporal's 2s deadlock check.
            logger.error(
                "session_workflow_failed_unexpectedly",
                session_id=str(params.session_id),
                error_type=type(error).__name__,
                error_message=str(error),
            )
        termination = wire.TerminationReason.FAILED
        # The Session's error is the plain reason; the parent's results word it.
        failure_message = sandbox_refusal or str(error) or None
        if binding is not None:
            await binding.runtime.report_session_failure_to_parent(
                ProtocolError(message=session_end_message("failed", failure_message), code=SESSION_FAILED_ERROR_CODE)
            )
    except BaseException as error:
        primary_error = error
        raise
    finally:
        workflow.mark_terminal()
        if binding is not None:
            binding.runtime_metrics.run_ended(failed=_run_failed(termination, primary_error))
        try:
            if binding is not None:
                await _close_workflow_binding(binding, primary_error=primary_error)
        finally:
            # After the close, which ends every message Update's wait for admission, so none waits forever.
            try:
                await _drain_message_handlers(workflow)
            except asyncio.CancelledError:
                pass  # A late cancel keeps the termination already chosen.
    end_cause = workflow._end_cause if termination is wire.TerminationReason.STOPPED else None
    return wire.SessionWorkflowOutput(
        # A failed Session reports its error, or none, never its last answer.
        final_message=failure_message if termination is wire.TerminationReason.FAILED else last_message,
        public_final_message=_public_final_message(termination, end_cause),
        termination_reason=termination,
        end_cause=end_cause,
    )


async def _serve_within_limits(
    workflow: _UnifiedHarnessControlPlaneWorkflow,
    binding: WorkflowSessionBinding,
    clock: session_limits.SessionLimitClock,
    limits: session_limits.SessionLimits,
    serve: Awaitable[Literal["stopped", "continuation"]],
) -> Literal["stopped", "continuation", "forced_end"]:
    """Serve the Session until it ends, stopping it at its lifetime or idle limit.

    A stop at a limit ends the Session through its normal terminal path. If it has not ended
    after the grace period, for example because a step ignores cancellation, serving is
    cancelled and the result is `forced_end`. If the stop itself fails, serving is cancelled and
    the error is raised, so the Session fails. Serving stays on this task, so it admits carried
    commands before any other Workflow task runs, as it did without the limits.
    """

    serving_task = asyncio.current_task()
    if serving_task is None:
        raise RuntimeError("A Session is served from an asyncio task")
    forced = False
    watch_error: Exception | None = None

    async def stop_and_wait_for_grace() -> None:
        while True:
            if workflow._end_cause is None:
                cause = await clock.wait_for_limit()
                if workflow._end_cause is None:
                    logger.info("session_limit_reached", session_id=binding.session_id, cause=cause.value)
                    await workflow.stop_at_limit(cause)
            # A stop that names a limit, from this clock or from an ending parent, has the same grace.
            # A Session that ends within the grace period cancels this wait. A refused stop from a
            # parent clears the cause, so the clock waits for a limit again.
            cause_cleared = await binding.condition_waiter.wait_for_condition(
                lambda: workflow._end_cause is None, timeout_seconds=limits.grace_seconds
            )
            if not cause_cleared:
                return

    async def watch() -> None:
        nonlocal forced, watch_error
        try:
            await stop_and_wait_for_grace()
        except Exception as error:
            # Serving must not outlive a failed limit stop: only Temporal's timeout would end it.
            watch_error = error
        else:
            logger.warning("session_limit_stop_timed_out", session_id=binding.session_id, cause=workflow._end_cause)
            forced = True
        serving_task.cancel()

    watching = asyncio.ensure_future(watch())
    try:
        return await serve
    except asyncio.CancelledError:
        if watch_error is not None:
            serving_task.uncancel()
            raise watch_error from None
        if not forced:
            raise
        serving_task.uncancel()
        return "forced_end"
    finally:
        watching.cancel()


def _ends_workflow_through_temporal(error: Exception) -> bool:
    """Whether Temporal itself handles `error`, so the Session must not catch it.

    A Temporal failure (an activity, child Workflow, or application error, or a
    cancellation) and `asyncio.TimeoutError` already fail the Workflow execution.
    The other Temporal errors, such as non-determinism, are the SDK's own signals.
    """

    return isinstance(error, TemporalError | asyncio.TimeoutError)


async def _close_workflow_binding(
    binding: WorkflowSessionBinding,
    *,
    primary_error: BaseException | None,
) -> None:
    """Keep an active Workflow failure primary if binding cleanup also fails."""

    if isinstance(primary_error, GeneratorExit):
        # Coroutine finalization cannot await cleanup or act in another Workflow's context.
        return
    try:
        await binding.close()
    except BaseException as cleanup_error:
        if primary_error is None:
            raise
        primary_error.add_note(f"Workflow binding cleanup failed: {cleanup_error!r}")


async def _drain_message_handlers(workflow: _UnifiedHarnessControlPlaneWorkflow) -> None:
    if not workflow.message_handlers_idle:
        await workflows.workflow.wait_condition(lambda: workflow.message_handlers_idle)


def _public_final_message(reason: wire.TerminationReason, end_cause: wire.SessionLimitCause | None = None) -> str:
    if end_cause is wire.SessionLimitCause.LIFETIME_LIMIT:
        return "This session ended after reaching its maximum duration. Feel free to start a new one!"
    if end_cause is wire.SessionLimitCause.IDLE_LIMIT:
        return "This session ended after being inactive."
    if reason == wire.TerminationReason.STOPPED:
        return "This session has ended. Feel free to start a new one!"
    if reason == wire.TerminationReason.FAILED:
        return "This session failed. Please start a new one."
    return "This session completed."


def _accept_message(message_entry_id: HistoryEntryId, *, turn_id: str, steered: bool) -> wire.SessionMessageVerdict:
    return wire.SessionMessageVerdict(
        accepted=True, message_entry_id=message_entry_id, turn_id=turn_id, steered=steered
    )


def _refuse_message(
    reason: wire.SessionCommandVerdictReason, *, active_turn_id: str | None = None
) -> wire.SessionMessageVerdict:
    return wire.SessionMessageVerdict(accepted=False, reason=reason, active_turn_id=active_turn_id)


def _command_id(command: wire.SessionWorkflowCommand) -> str | None:
    return str(command.command_id) if command.command_id is not None else None


def _genai_agent(
    params: wire.SessionWorkflowStartInput,
    child_session: StartSessionRequest | None,
    agent_description: str | None,
) -> GenAIAgentIdentity | None:
    """The agent a Session's Turns run as, for their `invoke_agent` spans."""
    # A child Session carries its root's agent fields. Its Turns are started by its
    # parent's agent tool calls, whose trace parent names the subagent instead.
    if child_session is not None:
        return None
    return GenAIAgentIdentity.of(name=params.agent_name, id=str(params.agent_id), description=agent_description)


def _genai_trace_parent(
    metadata: wire.CommandMetadata | None,
    session_id: str,
    turn_id: str,
    agent: GenAIAgentIdentity | None,
) -> GenAIRootTraceParent | None:
    """Map an eligible command's serialized trace context to its Turn's GenAI parent."""
    return turn_observability.genai_trace_parent(
        metadata.observability if metadata is not None else None,
        session_id=session_id,
        turn_id=turn_id,
        agent=agent,
    )


def _restored_turn_traced(restored: WorkflowContinuationState | None) -> bool:
    if restored is None:
        return False
    state = restored.hosted.runtime
    active_turn = state.event_producer.active_turn
    return active_turn is not None and active_turn.turn_id in state.genai_agent_operations


def _single_turn(params: wire.SessionWorkflowStartInput) -> bool:
    return isinstance(params.app_context, dict) and params.app_context.get("single_turn") is True


def _continue_as_new_suggested() -> bool:
    try:
        return temporalio.workflow.info().is_continue_as_new_suggested()
    except Exception:
        return False


class _WorkflowContinuationPolicy:
    """Continue-As-New when Temporal suggests it, unless a stop already owes its outcome here."""

    def __init__(self, stop_requested: Callable[[], bool] = lambda: False) -> None:
        self._stop_requested = stop_requested

    def continuation_requested(self) -> bool:
        # A stopping Workflow drives its interrupted Turn to an outcome instead of carrying it.
        return not self._stop_requested() and _continue_as_new_suggested()


def _build_determinism_source() -> LocalDeterminismSource | WorkflowDeterminismSource:
    if not temporalio.workflow.in_workflow():
        return LocalDeterminismSource()
    return WorkflowDeterminismSource(
        time_unix_ms=_workflow_time_unix_ms,
        random_seed=lambda: temporalio.workflow.random().getrandbits(32),
    )


def _run_failed(termination: wire.TerminationReason, primary_error: BaseException | None) -> bool:
    if termination is wire.TerminationReason.FAILED:
        return True
    return isinstance(primary_error, Exception) and not _caused_by_cancellation(primary_error)


def _caused_by_cancellation(error: BaseException) -> bool:
    # Mirrors Nuage's contains_cancellation so both engines label the same Turns cancelled.
    seen: set[int] = set()
    current: BaseException | None = error
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if isinstance(current, asyncio.CancelledError) or temporalio.exceptions.is_cancelled_exception(current):
            return True
        current = current.__cause__
    return False


def _workflow_time_unix_ms() -> int:
    if temporalio.workflow.in_workflow():
        return int(temporalio.workflow.now().timestamp() * 1000)
    return int(time.time() * 1000)


__all__ = [
    "AdmittedWorkflowMessage",
    "WorkflowContinuationState",
    "WorkflowPublicationState",
    "WorkflowSessionBinding",
    "build_workflow_class",
]
