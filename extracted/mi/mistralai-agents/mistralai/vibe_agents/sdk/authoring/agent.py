from __future__ import annotations

import hashlib
import json
import warnings
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable, Callable, Iterator, Mapping, Sequence
from contextlib import asynccontextmanager, contextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, Literal, Protocol, Self, cast, overload
from uuid import UUID, uuid4

import temporalio.workflow
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    SerializeAsAny,
    SerializerFunctionWrapHandler,
    SkipValidation,
    TypeAdapter,
    field_validator,
    model_serializer,
    model_validator,
)
from typing_extensions import deprecated

from mistralai.observability.otel import OperationDataTransformer
from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.app_server.session import McpHttpSourceConfiguration
from mistralai.vibe.harness.app_server.session.models.common import HistoryEntryId
from mistralai.vibe.harness.runtime.completion import CompletionConfig, CompletionProvider
from mistralai.vibe_agents.agents_client.api_models import is_reserved_agent_name, reserved_agent_name_message
from mistralai.vibe_agents.sdk.assembly import assemble
from mistralai.vibe_agents.sdk.assembly import session_inputs as session_input_assembly
from mistralai.vibe_agents.sdk.assembly import subagents as subagent_assembly
from mistralai.vibe_agents.sdk.client import approval_requests, approvals, handles, sign_ins
from mistralai.vibe_agents.sdk.client.content import UserContentLike
from mistralai.vibe_agents.sdk.client.events import EventHandler
from mistralai.vibe_agents.sdk.client.records import Blocked, Busy, Running, TurnState
from mistralai.vibe_agents.sdk.client.turn_reads import typed
from mistralai.vibe_agents.sdk.client.turn_waits import WaitBudget
from mistralai.vibe_agents.sdk.transport import client_tools as client_tools_registry
from mistralai.vibe_agents.sdk.transport import local
from mistralai.vibe_agents.sdk.transport import remote as remote_transport
from mistralai.vibe_agents.sdk.transport.session_journal import JsonFileSessionJournal
from mistralai.vibe_agents.session_workflow import SessionAgentCustomization, SubagentPolicy
from mistralai.vibe_agents.session_workflow.skills import RequestedSkillInput
from mistralai.vibe_agents.sessions_client import IdempotencyKey

from . import builtin_declarations, contracts, mcp_sources
from . import tool as tool_authoring
from . import types as authoring_types
from .errors import SdkError, UnsupportedAgentFeatureError, public_errors
from .experimental import warn_experimental
from .permissions import PermissionPolicy as AuthoringPermissionPolicy
from .permissions import always_denies
from .redaction import Redaction, resolve_redaction
from .secrets import SecretOrigin
from .skills import AllRegistrySkills, SandboxWorkspaceSkills
from .subagent import Subagent
from .tool_errors import DEFAULT_TOOL_ERRORS, ToolErrors

if TYPE_CHECKING:
    from mistralai.vibe.sdk.agent import config as vibe_agent_config
    from mistralai.vibe_agents.sdk import testing
    from mistralai.vibe_agents.sdk.client.api_client import Client
    from mistralai.workflows.plugins.nuage_v2.core.environment import environment as environment_base
    from mistralai.workflows.plugins.nuage_v2.integrations.github import github_models
    from mistralai.workflows.plugins.nuage_v2.integrations.skill_state_manager import (
        skill_state_manager_models,
    )
    from mistralai.workflows.plugins.nuage_v2.models import workflow as workflow_models
    from mistralai.workflows.plugins.nuage_v2.sdk._internal import harness as sdk_harness
    from mistralai.workflows.plugins.nuage_v2.sdk._internal import session as sdk_session

type WorkflowType = Literal["chat", "session"]


class LegacySessionAgent(Protocol):
    """Agent operations required by the retained Nuage Session runtime."""

    def model_copy(self, *, update: Mapping[str, object] | None = None, deep: bool = False) -> Self: ...

    def _open_session(
        self,
        *,
        harness: sdk_harness.Harness | None = None,
        state: dict[str, object] | None = None,
        sandbox_union: environment_base.Sandbox | None = None,
        github: github_models.GitHubParams | None = None,
        control_plane: bool = False,
        platform_requested_skills: Sequence[RequestedSkillInput] = (),
        requested_skill_source: skill_state_manager_models.RequestedSkillInputSource | None = None,
        control_plane_identity: workflow_models.WorkflowIdentity | None = None,
        inherited_skill_states: sdk_session.InheritedSkillStates | None = None,
    ) -> sdk_session.Session: ...


class _LegacyResumedState(Protocol):
    harness: object
    history: object
    platform_requested_skills: Sequence[RequestedSkillInput]


# Default model for a remote deployment handle, whose real config lives on the control plane.
_DEFAULT_MODEL = "mistral-large-4"

# Sentinel Agent.name when unset: serve/deploy reject it and require an explicit workflow name.
DEFAULT_AGENT_NAME = "default_agent"

_HISTORY_ENTRIES: TypeAdapter[list[harness_session.HistoryImportEntry]] = TypeAdapter(
    list[harness_session.HistoryImportEntry]
)

_reserved_agent_name_allowed: ContextVar[bool] = ContextVar("reserved_agent_name_allowed", default=False)


@contextmanager
def allow_reserved_agent_name() -> Iterator[None]:
    """Let the platform's own agents take a reserved name.

    Not part of the public SDK. The control plane still refuses to register a reserved name, so
    this only lifts the early check for code that the platform serves itself.
    """
    token = _reserved_agent_name_allowed.set(True)
    try:
        yield
    finally:
        _reserved_agent_name_allowed.reset(token)


class _ProviderUnset:
    # `provider` defaults to LLMProvider.MISTRAL, so comparing against that default cannot tell an
    # omitted provider from an explicit provider="mistral" — and the completion/provider mutual
    # exclusion below has to reject the explicit one. Hence a sentinel default rather than a value.
    __slots__ = ()


_PROVIDER_UNSET = _ProviderUnset()
type _ProviderArgument = authoring_types.LLMProvider | str | _ProviderUnset


def _resolve_provider_argument(
    provider: _ProviderArgument, *, completion: CompletionConfig | None
) -> authoring_types.LLMProvider | str:
    """Reject provider= passed alongside completion=, then fill in the default."""

    if isinstance(provider, _ProviderUnset):
        return authoring_types.LLMProvider.MISTRAL
    if completion is not None:
        raise SdkError("Pass either provider or completion, not both")
    return provider


class _AgentBundle(BaseModel):
    # The runtime-only slots an Agent carries but never serializes into a subagent snapshot: the
    # constructor harness (caller-owned, used verbatim so live state like a Permission prompter
    # survives) and a lazy control-plane deployment handle. Merged into ONE model so clone/copy carry
    # them as a unit and no loose parallel attributes drift.
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")
    harness: contracts.Harness | None = None
    remote_deployment: remote_transport.RemoteAgentDeployment | None = None
    local_runtime: local._AgentsSdkLocalRuntime | None = None
    completion_provider: CompletionProvider | None = None
    redaction: SkipValidation[tuple[OperationDataTransformer, ...] | None] = None


class AgentAuthoring(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: str
    instructions: str | None = None
    provider: authoring_types.LLMProvider = authoring_types.LLMProvider.MISTRAL
    completion: SerializeAsAny[CompletionConfig] | None = None
    name: str = DEFAULT_AGENT_NAME
    max_iterations: Annotated[int | None, Field(gt=0)] = None
    first_output_timeout_seconds: float | None = None
    builtins: authoring_types.Builtins = Field(default_factory=authoring_types.Builtins)
    permission_mode: authoring_types.PermissionMode = "auto"
    permission_policy: AuthoringPermissionPolicy | None = None
    # None leaves the threshold to the model's profile; compaction is always on.
    auto_compact_threshold: Annotated[int | None, Field(gt=0)] = None
    description: str | None = None
    reasoning_effort: authoring_types.ReasoningEffort | None = None
    temperature: float | None = None
    # The final answer of every Turn must match this model. A Subagent never inherits it.
    output_type: type[BaseModel] | None = None
    # An agents.Subagent carries live functions, so it stays authored here and is compiled into a
    # SubagentConfig by _to_agent_config.
    subagents: list[Subagent] = Field(default_factory=list)
    subagent_policy: SubagentPolicy | None = None
    # What the model sees when a tool, a client tool's answer or on_client_tool raises anything but
    # agents.ToolError: a generic message ("hide"), "<type>: <message>" ("show"), or the turn fails
    # ("raise"). It covers the agent's whole tree and the client tools of its Sessions.
    tool_errors: ToolErrors = DEFAULT_TOOL_ERRORS

    _bundle: _AgentBundle = PrivateAttr(default_factory=_AgentBundle)

    @model_validator(mode="after")
    def _validate_completion_model(self) -> Self:
        if self.completion is not None and self.completion.model != self.model:
            raise ValueError(f"completion.model {self.completion.model!r} must match Agent.model {self.model!r}")
        return self

    @model_validator(mode="after")
    def _validate_permission_configuration(self) -> Self:
        if self.permission_policy is not None and self.permission_mode != "auto":
            raise ValueError("A custom permission policy cannot be combined with permission_mode='ask' or 'deny'")
        return self

    @field_validator("permission_policy", mode="before")
    @classmethod
    def _reject_unknown_permission_policy_fields(cls, value: object) -> object:
        if value is None or isinstance(value, AuthoringPermissionPolicy):
            return value

        if isinstance(value, harness_session.PermissionPolicy):
            raise ValueError("Session permission policies cannot be used for authoring; use agents.PermissionPolicy")

        return AuthoringPermissionPolicy.model_validate(value)

    @model_serializer(mode="wrap")
    def _serialize_without_a_redundant_provider(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
        # A completion= config replaces provider entirely, so the field holds nothing but its own
        # default. Emitting it would make every snapshot look like the caller passed provider AND
        # completion, which __init__ rejects, so the agent could never be restored.
        payload = handler(self)
        if self.completion is not None:
            payload.pop("provider", None)
        return payload

    def __init__(
        self,
        *,
        model: str,
        instructions: str | None = None,
        provider: _ProviderArgument = _PROVIDER_UNSET,
        completion: CompletionConfig | None = None,
        name: str = DEFAULT_AGENT_NAME,
        max_iterations: int | None = None,
        first_output_timeout_seconds: float | None = None,
        builtins: authoring_types.Builtins | None = None,
        permission_mode: authoring_types.PermissionMode = "auto",
        permission_policy: AuthoringPermissionPolicy | None = None,
        auto_compact_threshold: int | None = None,
        description: str | None = None,
        reasoning_effort: authoring_types.ReasoningEffort | None = None,
        temperature: float | None = None,
        output_type: type[BaseModel] | None = None,
        subagents: Sequence[Subagent] = (),
        subagent_policy: SubagentPolicy | None = None,
        tool_errors: ToolErrors = DEFAULT_TOOL_ERRORS,
        tools: object = None,
    ) -> None:
        # Tools are capabilities, which Agent holds apart from this configuration; accepting the kwarg
        # rejects it with a clear error instead of an opaque "unexpected keyword".
        if tools is not None:
            raise SdkError("AgentAuthoring takes no tools; pass them to Agent(tools=[...]).")
        if is_reserved_agent_name(name) and not _reserved_agent_name_allowed.get():
            raise SdkError(f"{reserved_agent_name_message(name)}. Choose another name.")
        if max_iterations is not None and max_iterations <= 0:
            raise SdkError("Agent max_iterations must be greater than 0; omit it for no limit")
        if auto_compact_threshold is not None and auto_compact_threshold <= 0:
            raise SdkError("Agent auto_compact_threshold must be greater than 0; omit it to use the model's default")
        authoring_types.check_temperature(temperature, owner=f"Agent {name!r}")
        # completion carries a full custom Completion Provider config; it replaces
        # provider entirely, so the two are mutually exclusive.
        super().__init__(
            model=model,
            instructions=instructions,
            provider=_resolve_provider_argument(provider, completion=completion),
            completion=completion,
            name=name,
            max_iterations=max_iterations,
            first_output_timeout_seconds=first_output_timeout_seconds,
            builtins=authoring_types.Builtins() if builtins is None else builtins,
            permission_mode=permission_mode,
            permission_policy=permission_policy,
            auto_compact_threshold=auto_compact_threshold,
            description=description,
            reasoning_effort=reasoning_effort,
            temperature=temperature,
            output_type=output_type,
            subagents=list(subagents),
            subagent_policy=subagent_policy,
            tool_errors=tool_errors,
        )
        builtin_declarations.refuse_subagents_without_their_builtins(
            self.name, self.builtins, self.subagents, self.subagent_policy
        )
        if (
            self.subagents
            and self.permission_policy is not None
            and always_denies(self.permission_policy, "agents.spawn")
        ):
            warnings.warn(
                "This agent declares subagents, but its permission policy denies 'agents.spawn', so the "
                "model cannot start them. Put a PermissionRule that allows or asks for 'agents.spawn' before "
                "the first rule that matches it, or change that rule; if no rule matches, change the policy "
                "default from 'deny'.",
                stacklevel=2,
            )

    def _to_agent_config(self, *, output_type: type[BaseModel] | None = None) -> harness_session.AgentConfig:
        """Compile this Agent into the portable Harness Agent Configuration.

        ``output_type`` overrides the Agent's own ``output_type`` for this configuration only.
        """

        config = assemble.build_agent_config(
            model=self.model,
            provider=str(self.provider),
            completion=self.completion,
            name=self.name,
            instructions=self.instructions,
            max_iterations=self.max_iterations,
            first_output_timeout_seconds=self.first_output_timeout_seconds,
            permission_policy=self.permission_policy,
            builtins=authoring_types.builtins_to_config(self.builtins),
            auto_compact_threshold=self.auto_compact_threshold,
            response_format=output_type if output_type is not None else self.output_type,
            reasoning_effort=self.reasoning_effort,
            temperature=self.temperature,
        )
        if not self.subagents and self.subagent_policy is None:
            return config
        return config.model_copy(
            update=subagent_assembly.compile_subagents(config, self.subagents, policy=self.subagent_policy),
            deep=True,
        )

    def _to_nuage_agent_config(self) -> vibe_agent_config.AgentConfig:
        """Translate retained authoring into the legacy Nuage configuration."""

        from mistralai.vibe.sdk.agent import config as vibe_agent_config  # noqa: PLC0415
        from mistralai.vibe.sdk.providers.completion.config import MistralCompletionConfig  # noqa: PLC0415

        return vibe_agent_config.AgentConfig(
            completion=MistralCompletionConfig(model=self.model, reasoning_effort=self.reasoning_effort),
            name=self.name,
            system_prompt=self.instructions,
            max_iterations=self.max_iterations,
        )

    def model_copy(self, *, update: Mapping[str, object] | None = None, deep: bool = False) -> Self:
        # Carry the runtime-only bundle (a PrivateAttr, which pydantic's copy does not touch).
        copied = super().model_copy(update=dict(update) if update is not None else None, deep=deep)
        copied._bundle = self._bundle.model_copy(deep=deep)
        return cast(Self, copied)


def _check_mcp_sources(harness: contracts.Harness, builtins: authoring_types.Builtins | None) -> None:
    """Refuse the agent's MCP sources, by the rules assembly applies, once ``harness`` has validated its arguments."""

    builtins_config = authoring_types.builtins_to_config(builtins or authoring_types.Builtins())
    mcp_sources.check_mcp_sources(harness.mcps, programmatic=builtins_config.programmatic_enabled)
    # The same tools assembly checks: the agent's own, then those its guardrails and hooks carry.
    authored_tools = [
        *harness.tools,
        *(tool for hook in [*harness.guardrails, *harness.hooks] for tool in hook.tools),
    ]
    mcp_sources.refuse_tool_namespaces(authored_tools, harness.mcps)


class Agent(AgentAuthoring):
    """An agent: a model and its instructions, with the tools, sandbox, connectors, MCP servers, skills,
    hooks and subagents it can use.

    ``Agent.run()`` runs one turn in a new session, ``Agent.start_session()`` starts a session for many
    turns, and ``Agent.session(session_id)`` binds a handle to a session that exists. ``Agent.load_from()``
    reaches an agent you deployed.

    Args:
        model: The model, such as ``"mistral-large-4"``.
        instructions: Your instructions to the model, added to the agent loop's default system prompt.
        provider: The built-in completion provider: ``"mistral"``, the default, ``"openai"`` or ``"anthropic"``.
            It tries a model call up to 5 times when the call fails with a rate limit, a server error such
            as a 503, or a network error, and waits as long as a ``Retry-After`` header asks.
        completion: A completion configuration, built-in or your own, used instead of ``provider``.
        name: The agent's name. ``agents serve`` and ``agents deploy`` register the agent under it, and
            your app loads it by it. A name with a dot is reserved for Mistral's own agents.
        max_iterations: The most steps of the agent loop in one turn. ``None`` sets no limit.
        first_output_timeout_seconds: How long one model call waits for its first output. Defaults to 720
            seconds. A call stopped this way, or after 300 seconds without output once it started, is
            retried once.
        builtins: The built-in features to turn off, such as subagents or background processes.
        permission_mode: Which tool calls need an approval: ``"auto"`` runs every call that
            ``permission_policy`` allows (every call without one), ``"ask"`` opens an approval for each call,
            and ``"deny"`` refuses them.
        permission_policy: Rules that decide per tool, and per argument, whether a call runs, asks or is
            refused. It needs ``permission_mode="auto"``.
        auto_compact_threshold: The number of tokens at which the loop summarizes older turns. Defaults to
            a value set from the model's context window.
        description: What the agent does, in a sentence. A deployed agent shows it, and its traces record it.
        reasoning_effort: How much the model reasons, from ``"off"`` to ``"max"``. Defaults to the model's
            own.
        temperature: The sampling temperature, from ``0`` to ``2``. Defaults to the model's own.
        output_type: A Pydantic model that the final answer of every turn must match.
        subagents: The child agents that the agent can start, each an ``agents.Subagent``.
        subagent_policy: Limits on the subagents of a session tree: how many turns run at once and how
            deep the tree goes.
        tool_errors: What the model reads when a tool raises an unexpected error: ``"hide"``, the
            default, a generic message, ``"show"`` the exception's type and message, and ``"raise"``
            fails the turn; for a client tool, with ``"raise"``, the exception raises in your program
            instead, and the call stays open.
        tools: Your functions, each a plain or ``@agents.tool`` function, and client tools.
        environment: The sandbox where the agent runs shell commands and edits files. Defaults to
            ``NoSandbox()``: no shell and no files.
        connectors: The connectors your workspace set up in Studio, each with ``agents.connector(name)``.
        mcps: MCP servers that are not Studio connectors, by name.
        skills: Instructions that the agent loads only when it needs them.
        hooks: Code that runs before a turn, around model and tool calls, or after the answer.
        guardrails: Hooks for safety checks, which run before ``hooks`` at every hook point.
        secrets: The credentials that the agent reads, by name, each with where its value comes from.
        redaction: How the agent's traces mask secrets and personal data: a redaction policy, a
            ``(key, value)`` function, or a list of them, applied in order. ``[]`` turns redaction off.
    """

    def __init__(
        self,
        *,
        model: str,
        instructions: str | None = None,
        provider: _ProviderArgument = _PROVIDER_UNSET,
        completion: CompletionConfig | None = None,
        name: str = DEFAULT_AGENT_NAME,
        max_iterations: int | None = None,
        first_output_timeout_seconds: float | None = None,
        builtins: authoring_types.Builtins | None = None,
        permission_mode: contracts.PermissionMode = "auto",
        permission_policy: AuthoringPermissionPolicy | None = None,
        auto_compact_threshold: int | None = None,
        description: str | None = None,
        reasoning_effort: authoring_types.ReasoningEffort | None = None,
        temperature: float | None = None,
        output_type: type[BaseModel] | None = None,
        subagents: Sequence[Subagent] = (),
        subagent_policy: SubagentPolicy | None = None,
        tool_errors: ToolErrors = DEFAULT_TOOL_ERRORS,
        tools: contracts.HarnessTools | None = None,
        environment: contracts.Sandbox | None = None,
        connectors: Sequence[contracts.HarnessConnector] | None = None,
        mcps: dict[str, McpHttpSourceConfiguration] | None = None,
        skills: Sequence[contracts.HarnessSkill | SandboxWorkspaceSkills | AllRegistrySkills] | None = None,
        hooks: Sequence[contracts.Hook] | None = None,
        guardrails: Sequence[contracts.Hook] | None = None,
        secrets: Mapping[str, SecretOrigin] | None = None,
        redaction: Redaction | None = None,
    ) -> None:
        super().__init__(
            model=model,
            instructions=instructions,
            provider=provider,
            completion=completion,
            name=name,
            max_iterations=max_iterations,
            first_output_timeout_seconds=first_output_timeout_seconds,
            builtins=builtins,
            permission_mode=permission_mode,
            permission_policy=permission_policy,
            auto_compact_threshold=auto_compact_threshold,
            description=description,
            reasoning_effort=reasoning_effort,
            temperature=temperature,
            output_type=output_type,
            subagents=subagents,
            subagent_policy=subagent_policy,
            tool_errors=tool_errors,
        )
        if any(
            value is not None for value in (tools, environment, connectors, mcps, skills, hooks, guardrails, secrets)
        ):
            harness = contracts.Harness(
                tools=tools,
                sandbox=environment,
                connectors=connectors,
                mcps=mcps,
                skills=skills,
                hooks=hooks,
                guardrails=guardrails,
                secrets=secrets,
            )
            if mcps is not None:
                _check_mcp_sources(harness, builtins)
            builtin_declarations.refuse_skills_without_their_builtin(self.name, self.builtins, harness)
            self._bundle.harness = harness
        if redaction is not None:
            self._bundle.redaction = resolve_redaction(redaction)

    @overload
    async def run[T: BaseModel](
        self,
        content: UserContentLike,
        *,
        output_type: type[T],
        on_approval: approvals.ApprovalHandler | None = None,
        on_sign_in: sign_ins.SignInHandler | None = None,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
        on_event: EventHandler | None = None,
        idempotency_key: None = None,
        timeout: float | None = None,
    ) -> TurnState[T]: ...

    # With a key, a server older than MAIS 2026.11 can return Busy.
    @overload
    async def run[T: BaseModel](
        self,
        content: UserContentLike,
        *,
        output_type: type[T],
        on_approval: approvals.ApprovalHandler | None = None,
        on_sign_in: sign_ins.SignInHandler | None = None,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
        on_event: EventHandler | None = None,
        idempotency_key: str,
        timeout: float | None = None,
    ) -> TurnState[T] | Busy: ...

    # Without the argument, the Agent's own output_type may apply, so the output type is unknown.
    @overload
    async def run(
        self,
        content: UserContentLike,
        *,
        output_type: None = None,
        on_approval: approvals.ApprovalHandler | None = None,
        on_sign_in: sign_ins.SignInHandler | None = None,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
        on_event: EventHandler | None = None,
        idempotency_key: None = None,
        timeout: float | None = None,
    ) -> TurnState[Any]: ...

    @overload
    async def run(
        self,
        content: UserContentLike,
        *,
        output_type: None = None,
        on_approval: approvals.ApprovalHandler | None = None,
        on_sign_in: sign_ins.SignInHandler | None = None,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
        on_event: EventHandler | None = None,
        idempotency_key: str,
        timeout: float | None = None,
    ) -> TurnState[Any] | Busy: ...

    @public_errors
    async def run(
        self,
        content: UserContentLike,
        *,
        output_type: type[BaseModel] | None = None,
        on_approval: approvals.ApprovalHandler | None = None,
        on_sign_in: sign_ins.SignInHandler | None = None,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
        on_event: EventHandler | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> TurnState[Any] | Busy:
        """Start a session, run one turn in it, and return the turn's record.

        The record is a value, never raised: ``Completed``, ``Blocked``, ``Interrupted``, ``Failed``,
        ``Running``, or ``UnknownOutcome`` for an outcome added after your SDK version. With ``output_type=T``, it is
        a ``TurnState[T]``. Its ``session_id`` and ``turn_id`` reach the session and the turn again, as in
        ``agent.session(state.session_id)``.

        On a deployed agent, ``output_type`` only parses the answer, and the model gets the deployed
        agent's format. ``output`` is ``InvalidOutput`` when the answer does not validate, and ``None``
        when the turn ended early.

        A callback with no handler for it, or one whose handler returns ``KeepCallbackOpen()``, makes
        the run return ``Blocked``. Answer it with
        ``agent.session(state.session_id).turn(state.turn_id).answer(cb.id, ...)``. An approval or
        sign-in handler that raises makes the run raise its error. An approval handler that returns
        anything else, ``None`` included, raises ``SdkError``. A sign-in handler that returns ``None``,
        ``KeepCallbackOpen()``, or an answer that leaves a source out raises ``SdkError``. A client
        tool answer that cannot be sent raises ``ClientToolAnswerError``. In each case the callback
        stays open and the turn keeps running. A client tool answer or ``on_client_tool`` handler
        that raises follows the agent's ``tool_errors``: by default the model reads that the call
        failed and the run goes on. With ``"raise"``, the run raises the error and the call stays
        open: the turn stays blocked on it, and the session takes no new turn, until the callback
        times out (one hour by default).

        Args:
            content: The user's message: a string, or a list of content blocks.
            output_type: A Pydantic model that this run's answer must match, instead of the agent's own
                ``output_type``; ``Completed.output`` is validated against it.
            on_approval: A plain or async function that answers each approval of the session and its
                subagents with ``AllowApproval`` or ``DenyApproval``.
            on_sign_in: A function that answers each connector sign-in of the session and its subagents
                with a ``SignInAnswer``.
            on_client_tool: A function that answers each client tool call of the session and its
                subagents, or an ``agents.ClientToolAnswers``.
            on_event: A function that gets each event of the turn as it comes. When the turn has ended,
                the last event is ``TurnEnded``.
            idempotency_key: A key of 1 to 256 characters that makes the run safe to retry: a second run with
                the same key returns the same turn's record, even once the turn has ended. The same key with
                another message or other agent settings raises ``SessionIdempotencyConflictError``. Generate
                it once per request, for example as a UUID. A run with a key can return ``Busy`` while
                another turn runs.
            timeout: How long the run waits for the turn, in seconds. An ``on_approval`` or ``on_sign_in``
                handler's time counts; your client-tool code does not. Then the run returns ``Running`` or
                ``Blocked``, and the turn keeps running. ``None`` waits until the turn ends or waits on you.
        """

        # An empty message raises ``SdkError`` before a Session opens, as on a session handle.
        initial_turn = harness_session.InitialTurn(message=handles.checked_message(content))
        key = handles.checked_idempotency_key(idempotency_key)
        output_format = output_type if output_type is not None else self.output_type
        # Bad client tool answers fail before a session starts.
        client_tool_registry = self._client_tool_registry(on_client_tool)
        # The start carries the message as the session's initial turn: one request starts both.
        if self._bundle.remote_deployment is None and key is None:
            run_runtime: local._AgentsSdkLocalRuntime | None = None
            if (
                on_approval is None
                and on_sign_in is None
                and self._bundle.local_runtime is None
                and self._to_agent_config().effective_subagent_policy() is None
            ):
                # Its record is all the caller gets, so its session ends with its turn.
                run_runtime = local._process_runtime()
            # The attached client keeps the session, and answers its client tools, while the handle
            # waits on its turn; once both are gone and the tree is idle, the local runtime closes it.
            async with await self._create_session(
                output_type=output_type,
                initial_turn=initial_turn,
                client_tools=client_tool_registry,
            ) as client:
                if run_runtime is not None:
                    run_runtime.close_after_turns(client.session_id)
                session = self.session(client.session_id, on_approval=on_approval, on_sign_in=on_sign_in)
                turns = client.state.turns.items if client.state.turns is not None else []
                turn_id = turns[0].id if turns else None
                async with client_tools_registry.raising_answer_failures(client):
                    with handles.host_wait_budget(client, timeout) as budget:
                        # With tool_errors="raise", a client tool's exception raises here; its call stays open.
                        state = await _raising_from_client_tools(
                            client,
                            _run_initial_turn(
                                session,
                                turn_id,
                                content,
                                output_format,
                                None,
                                budget,
                                on_event,
                                client_tool_registry,
                            ),
                        )
                    state = await _raising_from_client_tools(
                        client,
                        handles.with_running_answers_sent(
                            client,
                            self.session(session.id),
                            state,
                            output_format,
                            on_event,
                            client_tool_registry,
                        ),
                    )
            if run_runtime is not None and not isinstance(state, Running | Blocked):
                # Ended before the record is returned, sandbox included.
                await run_runtime.end_finished_tree(client.session_id)
            return state
        session, turn_id = await self._start_session(
            idempotency_key=key,
            on_approval=on_approval,
            on_sign_in=on_sign_in,
            output_type=output_type,
            initial_turn=initial_turn,
        )
        async with (
            self._answering_client_tools(session.id, client_tool_registry) as answering,
            client_tools_registry.raising_answer_failures(answering),
        ):
            if turn_id is None and key is not None:
                # A repeated key: the session's first turn is the one its first start began.
                turn_id = await _first_turn_id(session)
            with handles.host_wait_budget(answering, timeout) as budget:
                # With tool_errors="raise", a client tool's exception raises here; its call stays open.
                state = await _raising_from_client_tools(
                    answering,
                    _run_initial_turn(
                        session, turn_id, content, output_format, key, budget, on_event, client_tool_registry
                    ),
                )
            return await _raising_from_client_tools(
                answering,
                handles.with_running_answers_sent(
                    answering, self.session(session.id), state, output_format, on_event, client_tool_registry
                ),
            )

    @deprecated(
        "Agent.local_runtime() is deprecated; agent.run(), agent.start_session() and agent.session(id) use "
        "the event loop's local runtime. Set program_timeout_seconds= with "
        "async with agents.local_runtime(program_timeout_seconds=...). event_log_directory= has no new place "
        "yet: keep local_runtime() to set it.",
        category=DeprecationWarning,
    )
    @asynccontextmanager
    async def local_runtime(
        self,
        *,
        program_timeout_seconds: float | None = None,
        event_log_directory: Path | str | None = None,
        journal_factory: Callable[[str], JsonFileSessionJournal] | None = None,
    ) -> AsyncIterator[Agent]:
        """Bind an Agent to application-owned local Sessions until context exit.

        Deprecated: ``agent.run``, ``agent.start_session`` and ``agent.session(id)`` use the event
        loop's local runtime. This method still works as before, but warns. Set
        ``program_timeout_seconds`` for every local session of the event loop with
        ``async with agents.local_runtime(program_timeout_seconds=...)``. This method is still the only place to set
        ``event_log_directory``.

        Closing an attached client only detaches it. Context exit shuts down
        all workers, then their shared root workspace. Each Session Tree takes its
        subagent policy from the root agent's ``subagent_policy``.

        ``program_timeout_seconds`` sets the time budget of each program, the code the model runs
        with ``run_typescript``, in every Session of this runtime. It defaults to 60 seconds. The
        budget applies to the whole program, not to each tool call: a running tool call is never
        cut short, but once the budget is used up the program stops before its next step and the
        model gets a ``ProgramBudgetExceeded`` error. Time spent waiting for approvals and hooks
        does not count. It must be greater than 0 and at most 4 hours (14400 seconds).

        ``event_log_directory`` keeps an audit log of each Session, its subagents included: every
        committed event is appended as one JSON line to ``<event_log_directory>/<session id>/events.jsonl``,
        and the file stays after the process stops. Without it, no file is written.
        ``journal_factory`` is experimental: a minor release may change it, and passing it warns
        ``ExperimentalWarning`` once per process. It returns the journal of each Session from its ID.
        Without it, Sessions are kept in memory, so they end with the process. With
        ``experimental.JsonFileSessionJournal.in_directory(path)``, each root Session is saved on
        disk, and ``get_session(session_id)`` or ``session(session_id)`` in a later process reopens
        it with the same Agent. Only one process at a time can write a saved Session: the process
        that holds it open keeps a file lock until context exit, and another process gets
        ``SessionInUseError``. The lock needs POSIX; subagent Sessions are not reopened.
        """
        if journal_factory is not None:
            # The body runs in the block's __aenter__, which the caller's async with line awaits.
            warn_experimental("journal_factory=", stacklevel=3)
        runtime = local._AgentsSdkLocalRuntime(
            completion_provider=self._bundle.completion_provider,
            program_policy=local._program_policy(program_timeout_seconds),
            event_log_directory=event_log_directory,
            journal_factory=journal_factory,
        )
        async with self._bind_local_runtime(runtime) as bound:
            yield bound

    @asynccontextmanager
    async def _bind_local_runtime(self, runtime: local._AgentsSdkLocalRuntime) -> AsyncIterator[Agent]:
        if self._bundle.remote_deployment is not None or self._bundle.local_runtime is not None:
            await runtime.close()
            raise SdkError("local_runtime requires an unbound local Agent")
        bound = self.model_copy()
        bound._bundle.local_runtime = runtime
        try:
            yield bound
        finally:
            await runtime.close()

    def override(self, *, model: testing.ScriptedModel) -> Self:
        """Return a copy of this agent that sends its model calls to ``model``. This agent is unchanged.

        Call it on a local agent: on a deployed agent, it raises ``SdkError``.

        Args:
            model: The scripted model that answers the copy's model calls, in tests.
        """
        if self._bundle.remote_deployment is not None:
            raise SdkError("Agent.override works only on a local Agent, not on a deployment handle")
        if self._bundle.local_runtime is not None:
            raise SdkError("Call Agent.override before local_runtime(), then call local_runtime() on the copy")
        overridden = self.model_copy()
        overridden._bundle.completion_provider = model
        return overridden

    def _require_real_model(self) -> None:
        if self._bundle.completion_provider is not None:
            raise UnsupportedAgentFeatureError(
                "testing.ScriptedModel",
                "it answers model calls only in the test process. agents serve, agents deploy and "
                "to_workflow() need a real model. Use override() in tests only.",
            )

    @deprecated(
        "Agent.get_session() is deprecated; use agent.session(session_id), which returns an agents.Session "
        "handle, then session_protocol.attach(session) from mistralai.agents.experimental for the raw client.",
        category=DeprecationWarning,
    )
    @public_errors
    async def get_session(
        self,
        session_id: str,
        *,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
    ) -> harness_session.SessionClient:
        """Attach by Session ID to a local Session that is still known in this process.

        Deprecated: use ``agent.session(session_id)``. This method still works as before and
        returns the raw Session client, but warns, and so does the client's ``run_turn``.

        That is a Session of an Agent with subagents, one of its children, or a Session started
        in the bound `async with agent.local_runtime()`. A Session that an earlier process saved
        through that runtime's ``journal_factory`` is reopened from its journal. It keeps the
        configuration it was created with, including the ``create_session`` options such as
        ``permission_mode``; this Agent must have the same tools, hooks, MCP servers, connectors
        and sandbox. Bind a handle to a deployment-backed Session with
        `Agent.load_from(agent_name=...).session(session_id)`.

        ``on_client_tool`` answers the Session's client tools, as in ``create_session``.
        """
        if self._bundle.remote_deployment is not None:
            raise SdkError(
                "Agent.get_session attaches only to local Sessions; "
                "bind a handle to a deployment-backed Session with "
                "Agent.load_from(agent_name=...).session(session_id)"
            )
        runtime = self._bundle.local_runtime
        if runtime is None:
            if self._to_agent_config().effective_subagent_policy() is None:
                raise SdkError(
                    "Agent.get_session attaches only to the Sessions of an Agent with subagents; "
                    "use agent.session(session_id) for a local Session of an Agent without subagents"
                )
            local._refuse_if_freed_by_block_exit(session_id)
            runtime = local._process_runtime()
        return _deprecated_run_turn(
            await runtime.get_session(
                session_id,
                client_tools=self._client_tool_registry(on_client_tool),
                reassemble=lambda: self._reassemble_local_root(runtime, session_id),
            )
        )

    @public_errors
    async def start_session(
        self,
        *,
        history: Sequence[harness_session.HistoryImportEntry] | None = None,
        session_inputs: Mapping[str, contracts.SessionInput] | None = None,
        agent: SessionAgentCustomization | Mapping[str, object] | None = None,
        idempotency_key: IdempotencyKey | None = None,
        on_approval: approvals.ApprovalHandler | None = None,
        on_sign_in: sign_ins.SignInHandler | None = None,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
    ) -> handles.Session:
        """Start a session and return its handle.

        A local session runs in this process until its event loop shuts down, and its handle binds
        again only inside that event loop. A session of a deployed agent is kept by Mistral, and its
        handle binds again from any process.

        A second call with the same ``idempotency_key`` and the same options returns the same
        session, even once it is running a turn or has ended. The same key with other
        ``session_inputs`` or ``agent``, or from an agent with other settings such as
        ``permission_mode``, raises ``agents.SessionIdempotencyConflictError``; another ``history`` is
        not checked, and returns the first session. Generate the key once per request, for example
        as a UUID, and reuse it only on that request's retries.

        The handlers stay in this process: they are not part of the start, so the same
        ``idempotency_key`` takes other ones. An answer to a stub that is not a tool of this agent, of
        its guardrails and hooks, or of its subagents raises ``SdkError`` before the start.

        The handle keeps this agent's ``output_type``: ``session.run()``, ``turn.get()`` and
        ``turn.result()`` parse a ``Completed`` output with it when given none.

        Args:
            history: Existing entries that seed the conversation. Only a local session takes it.
            session_inputs: The session inputs, keyed by each value's ``input_id``. They are fixed for the
                session's lifetime and delivered only to the tools, hooks and sandbox hooks that declare
                them with ``agents.Depends()``.
            agent: Changes to this agent for this session only, as an ``agents.SessionAgentCustomization``
                or the same keys as a dict: ``additional_instructions`` append to its instructions, and
                ``model`` and ``reasoning_effort`` override its completion defaults. A deployment keeps its
                saved agent unchanged. Permissions are not customized per session: set ``permission_mode=``
                or ``permission_policy=`` on the agent.
            idempotency_key: A key of 1 to 256 characters that makes the start safe to retry.
            on_approval: Answers approvals while a call waits on the handle (see ``Session``).
            on_sign_in: Answers sign-ins while a call waits on the handle, as on ``run``.
            on_client_tool: Answers client tool calls while a call waits on the handle, as on ``run``.
        """
        session, _turn_id = await self._start_session(
            history=history,
            session_inputs=session_inputs,
            agent=agent,
            idempotency_key=idempotency_key,
            on_approval=on_approval,
            on_sign_in=on_sign_in,
            client_tools=self._client_tool_registry(on_client_tool),
        )
        return session

    async def _start_session(
        self,
        *,
        history: Sequence[harness_session.HistoryImportEntry] | None = None,
        session_inputs: Mapping[str, contracts.SessionInput] | None = None,
        agent: SessionAgentCustomization | Mapping[str, object] | None = None,
        idempotency_key: str | None = None,
        on_approval: approvals.ApprovalHandler | None = None,
        on_sign_in: sign_ins.SignInHandler | None = None,
        client_tools: client_tools_registry.ClientToolRegistry = client_tools_registry.NO_CLIENT_TOOLS,
        output_type: type[BaseModel] | None = None,
        initial_turn: harness_session.InitialTurn | None = None,
    ) -> tuple[handles.Session, str | None]:
        # start_session, plus what ``run`` needs: a local session's output_type override, and
        # ``initial_turn`` started in the same request. Returns the session and the ID of its initial
        # turn when the start names it. A deployed Agent fixes its completion config, so a deployed
        # start ignores the override: ``run`` parses the reply. The handle's waits answer
        # ``client_tools``.
        key = handles.checked_idempotency_key(idempotency_key)
        customization = SessionAgentCustomization.model_validate(agent) if agent is not None else None
        deployment = self._bundle.remote_deployment
        if deployment is not None:
            if history:
                raise remote_transport.RemoteSessionProcedureUnsupportedError(
                    method="Agent.start_session(history=...)",
                    backend="vibe_agents",
                    reason="the current Vibe Agents start contract cannot import canonical history",
                )
            session_id, turn_id = await remote_transport._start_remote_run(
                deployment,
                idempotency_key=key,
                agent=customization,
                session_inputs=session_input_assembly.serialize_session_inputs(session_inputs) or None,
                initial_turn=initial_turn,
            )
            return (
                self._session(session_id, on_approval=on_approval, on_sign_in=on_sign_in, client_tools=client_tools),
                turn_id,
            )
        runtime = self._bundle.local_runtime or local._process_runtime()
        agent_config = self._to_agent_config(output_type=output_type)
        history_entries = _HISTORY_ENTRIES.validate_python(list(history or ()))

        async def start() -> tuple[str, str | None]:
            session_id = str(uuid4())
            assembly = self._local_root_assembly(
                runtime,
                session_id,
                agent_config,
                permission_mode=self.permission_mode,
                customization=customization,
            )
            turn_id = await runtime.start_kept_session(
                assembly,
                session_id=session_id,
                history=history_entries,
                session_inputs=session_inputs,
                completion_provider=self._bundle.completion_provider,
                initial_turn=initial_turn,
            )
            return session_id, turn_id

        if key is None:
            session_id, turn_id = await start()
        else:
            fingerprint = self._start_fingerprint(agent_config, session_inputs, customization, initial_turn)
            # A repeated key returns the first start's session and initial turn: the fingerprint
            # holds the initial turn, so it is this call's too.
            session_id, turn_id = await runtime.start_once(key, start, fingerprint=fingerprint)
        return (
            self._session(session_id, on_approval=on_approval, on_sign_in=on_sign_in, client_tools=client_tools),
            turn_id,
        )

    def _start_fingerprint(
        self,
        agent_config: harness_session.AgentConfig,
        session_inputs: Mapping[str, contracts.SessionInput] | None,
        customization: SessionAgentCustomization | None,
        initial_turn: harness_session.InitialTurn | None = None,
    ) -> str:
        """A digest of what a local start asks for: two starts under one key must ask for the same.

        The history is not in it: the client is trusted with it, as the Agent Controller does. The
        initial turn is, as the Agent Controller's: a run retried with another prompt is a conflict.
        """
        customized = customization.model_dump(mode="json", exclude_none=True) if customization is not None else {}
        fields: dict[str, object] = {
            "agent": agent_config.model_dump(mode="json"),
            "permission_mode": self.permission_mode,
            "tools": sorted(tool.name for tool in self._bundle.harness.tools) if self._bundle.harness else [],
            "session_inputs": session_input_assembly.serialize_session_inputs(session_inputs),
            "customization": customized,
        }
        if initial_turn is not None:
            # Only a start with an initial turn has it, so a start_session key keeps its digest.
            fields["initial_turn"] = initial_turn.model_dump(mode="json", exclude_none=True)
        request = json.dumps(fields, sort_keys=True, separators=(",", ":"))
        # The runtime keeps the fingerprint as long as the key: a fixed-size digest, not the request.
        return hashlib.sha256(request.encode()).hexdigest()

    @asynccontextmanager
    async def _answering_client_tools(
        self, session_id: str, client_tools: client_tools_registry.ClientToolRegistry
    ) -> AsyncIterator[harness_session.SessionClient | None]:
        """Answer the client tools of a started session from this process until context exit.

        Yields the client that answers them, or ``None`` without client tools.
        """

        if not client_tools:
            yield None
            return
        deployment = self._bundle.remote_deployment
        if deployment is not None:
            client = await remote_transport._get_remote_session(deployment, session_id, client_tools=client_tools)
        else:
            runtime = self._bundle.local_runtime or local._process_runtime()
            client = await runtime.get_session(session_id, client_tools=client_tools)
        async with client:
            yield client

    def session(
        self,
        session_id: str,
        *,
        on_approval: approvals.ApprovalHandler | None = None,
        on_sign_in: sign_ins.SignInHandler | None = None,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
    ) -> handles.Session:
        """Return the handle of one of this agent's sessions by its ID. Sends no request.

        For a deployed agent, an ID that is not a UUID raises ``SdkError`` at once. An unknown ID
        binds too: the first request through the handle raises ``SessionNotFoundError``. The handle
        keeps this agent's ``output_type``, as ``start_session()``'s does. An answer to a stub that
        is not a tool of this agent, of its guardrails and hooks, or of its subagents raises
        ``SdkError`` here.

        In an ``async with agents.local_runtime(journal_factory=...)`` block, a local session that
        an earlier process saved there reopens on the handle's first request, and keeps running in
        this process until the block exits. It must be a session of this agent: one with other
        tools, hooks, MCP servers, connectors or sandbox raises ``SessionConfigMismatchError``,
        and one that another process holds open raises ``SessionInUseError``.

        Args:
            session_id: The ID of the session.
            on_approval: Answers approvals while a call waits on the handle (see ``Session``).
            on_sign_in: Answers sign-ins while a call waits on the handle, as on ``run``.
            on_client_tool: Answers client tool calls while a call waits on the handle, as on ``run``.
        """
        return self._session(
            session_id,
            on_approval=on_approval,
            on_sign_in=on_sign_in,
            client_tools=self._client_tool_registry(on_client_tool),
        )

    def _client_tool_registry(
        self, on_client_tool: client_tools_registry.OnClientTool | None
    ) -> client_tools_registry.ClientToolRegistry:
        """``on_client_tool`` checked against this Agent's tools, as the session answers it."""
        if self._bundle.remote_deployment is None and isinstance(
            on_client_tool, client_tools_registry.ClientToolAnswers
        ):
            # A deployment-backed Agent has no tool objects: its tools are on the deployment.
            client_tools_registry.check_answered_tools(on_client_tool, self._tool_objects())
        return client_tools_registry.build_client_tool_registry(on_client_tool, tool_errors=self.tool_errors)

    def _session(
        self,
        session_id: str,
        *,
        on_approval: approvals.ApprovalHandler | None,
        on_sign_in: sign_ins.SignInHandler | None = None,
        client_tools: client_tools_registry.ClientToolRegistry = client_tools_registry.NO_CLIENT_TOOLS,
    ) -> handles.Session:
        """``session(session_id)``, whose waits answer ``client_tools``."""
        handler = self._with_tools(on_approval)
        tools = approval_requests.tools_by_id(self._tool_objects())
        if self._bundle.remote_deployment is not None:
            return handles.remote_session(
                self._bundle.remote_deployment,
                session_id,
                on_approval=handler,
                on_sign_in=on_sign_in,
                output_type=self.output_type,
                tools=tools,
                client_tools=client_tools,
            )
        return handles.local_session(
            self._bundle.local_runtime,
            session_id,
            on_approval=handler,
            on_sign_in=on_sign_in,
            output_type=self.output_type,
            tools=tools,
            client_tools=client_tools,
            reassemble=self._reassemble_local_root,
            completion_provider=self._bundle.completion_provider,
        )

    def _with_tools(self, handler: approvals.ApprovalHandler | None) -> approvals.ApprovalHandler | None:
        """``handler``, whose requests carry the tool objects of this Agent, of its guardrails and
        hooks, and of its subagents, at any depth."""
        return approvals.with_tools(handler, self._tool_objects())

    def _tool_objects(self) -> list[approval_requests._Tool]:
        """The tool objects the model can call in a session of this Agent: its own, its guardrails'
        and hooks', and those of its subagents, at any depth."""
        harness = self._bundle.harness
        tools: list[contracts.HarnessTool] = []
        if harness is not None:
            tools.extend(harness.tools)
            tools.extend(tool for hook in [*harness.guardrails, *harness.hooks] for tool in hook.tools)
        pending = list(self.subagents)
        while pending:
            subagent = pending.pop()
            tools.extend(subagent.tools or ())
            tools.extend(tool for hook in subagent.hooks or () for tool in hook.tools)
            pending.extend(subagent.subagents or ())
        return [tool_authoring.author_tool(tool) for tool in tools]

    def _reassemble_local_root(self, runtime: local._AgentsSdkLocalRuntime, session_id: str) -> assemble.AgentAssembly:
        # A saved Session keeps the configuration it was saved with; this builds the resources
        # that this process supplies again, which must match the saved ones.
        return self._local_root_assembly(
            runtime, session_id, self._to_agent_config(), permission_mode=self.permission_mode
        )

    def _local_root_assembly(
        self,
        runtime: local._AgentsSdkLocalRuntime,
        session_id: str,
        agent_config: harness_session.AgentConfig,
        *,
        permission_mode: authoring_types.PermissionMode,
        customization: SessionAgentCustomization | None = None,
    ) -> assemble.AgentAssembly:
        # Children are rebuilt from the durable definition, so their worker callables must be
        # resolvable through the runtime's resolver under this Session's provider ID.
        return assemble.assemble_agent(
            agent_config,
            self._resolve_harness(None),
            permission_mode=permission_mode,
            subagents=self.subagents,
            session_id=session_id,
            capability_provider_id=session_id,
            capability_resolver=runtime.capability_resolver,
            customization=customization,
            tool_errors=self.tool_errors,
        )

    def to_workflow(
        self,
        name: str | None = None,
        *,
        type: WorkflowType = "session",
    ) -> type:
        # Promote this agent to one durable Vibe Agents Session Workflow. Public type="chat" remains
        # unsupported in this migration. Retained Nuage workers call their private assembly path
        # directly. The builders are imported lazily to avoid an agent<->app import cycle.
        # The Workflow calls the Agents API with the worker's own credential, so its Sessions can run
        # the subagents their start input allows.
        from mistralai.vibe_agents.sdk.app.worker.control_plane import (  # noqa: PLC0415
            WorkflowSessionControlPlaneBinding,
        )
        from mistralai.vibe_agents.sdk.assembly.workflow import build_workflow  # noqa: PLC0415

        return build_workflow(
            self,
            name=name,
            harness=None,
            type=type,
            session_control_plane=WorkflowSessionControlPlaneBinding.from_worker_credential(),
        )

    async def run_worker(
        self,
        *,
        workflow_name: str | None = None,
        deployment_name: str | None = None,
    ) -> None:
        """Run this agent as a durable worker until cancelled, without registering it.

        Something else must route sessions to the worker: `agents deploy`, `agents serve`, or the
        platform that runs it. The worker polls the task queue named by `deployment_name`, else by
        DEPLOYMENT_NAME, else the queue the control plane registered for the agent's name.

        The workflow takes the agent name unless `workflow_name` is given, for a platform that
        dispatches sessions to another workflow name.
        """
        from mistralai.vibe_agents.sdk.app.worker import runner  # noqa: PLC0415

        await runner.run_worker(self, workflow_name=workflow_name, deployment_name=deployment_name)

    def _resolve_harness(self, harness: contracts.Harness | None) -> contracts.Harness:
        # Resolution order: a per-call session harness= wins, then the agent's constructor harness,
        # else the default.
        if harness is not None:
            return harness
        if self._bundle.harness is not None:
            return self._bundle.harness
        return _default_harness()

    def _resolve_nuage_harness(self, harness: object | None) -> object:
        from mistralai.workflows.plugins.nuage_v2.sdk._internal import harness as sdk_harness  # noqa: PLC0415

        if harness is None and self._bundle.harness is not None:
            harness = self._bundle.harness
        if harness is None:
            return sdk_harness.Harness()
        if isinstance(harness, sdk_harness.Harness):
            return harness
        raise SdkError("the retained Nuage session accepts only its legacy Harness authoring")

    def _open_session(
        self,
        *,
        harness: sdk_harness.Harness | None = None,
        state: dict[str, object] | None = None,
        sandbox_union: environment_base.Sandbox | None = None,
        github: github_models.GitHubParams | None = None,
        control_plane: bool = False,
        platform_requested_skills: Sequence[RequestedSkillInput] = (),
        requested_skill_source: skill_state_manager_models.RequestedSkillInputSource | None = None,
        control_plane_identity: workflow_models.WorkflowIdentity | None = None,
        inherited_skill_states: sdk_session.InheritedSkillStates | None = None,
    ) -> sdk_session.Session:
        # Retained Nuage-only factory: build its legacy Session or resume it from a continue-as-new
        # snapshot. Public start_session()/run() use the Harness Session Protocol instead.
        from mistralai.workflows.plugins.nuage_v2.sdk._internal import session as sdk_session  # noqa: PLC0415

        _require_unsandboxed_workflow()
        if self.builtins != authoring_types.Builtins():
            raise SdkError("the retained Nuage session cannot turn off builtins")
        if self.output_type is not None:
            raise SdkError("the retained Nuage session does not support output_type")
        if state is not None:
            resumed = _resume_from_state(state)
            resolved, history = resumed.harness, resumed.history
            platform_requested_skills = [*resumed.platform_requested_skills, *platform_requested_skills]
        else:
            resolved = self._resolve_nuage_harness(harness)
            history = None
        session = sdk_session.Session._create_for_agent(
            self,
            harness=resolved,
            github=github,
            control_plane=control_plane,
            platform_requested_skills=platform_requested_skills,
            requested_skill_source=requested_skill_source,
            control_plane_identity=control_plane_identity,
            inherited_skill_states=inherited_skill_states,
            history=history,
            # This session takes 0 for "not set".
            auto_compact_threshold=self.auto_compact_threshold or 0,
            sandbox_union=sandbox_union,
        )
        remote = self._bundle.remote_deployment
        session._deployment_id = (
            str(remote.agent_deployment_id or remote.agent_deployment_name) if remote is not None else None
        )
        return session

    @classmethod
    def load_from(
        cls,
        *,
        agent_name: str | None = None,
        agent_id: str | None = None,
        server_url: str | None = None,
        api_key: str | None = None,
        client: Client | None = None,
    ) -> Agent:
        """Build a lazy handle to a deployed agent, by its name or its ID.

        Pass exactly one of ``agent_name`` or ``agent_id``, of an agent deployed with Studio,
        self-hosted or Mistral-managed. To continue a session, bind a handle to it with ``.session(session_id)``.

        Without ``client``, ``server_url`` and ``api_key`` build one with no shared connection pool:
        each session then opens its own, which closes with the session and serves the event loop
        that opened it. Pass either ``client`` or them, not both.

        Args:
            agent_name: The name the agent was deployed under.
            agent_id: The ID of the deployed agent, a UUID.
            server_url: The Mistral API root, as ``agents.Client`` takes it.
            api_key: The API key, as ``agents.Client`` takes it.
            client: The client that the agent and its sessions send their requests through.
        """
        if (agent_name is None) == (agent_id is None):
            raise SdkError("Pass exactly one of agent_name or agent_id")
        try:
            parsed_agent_id = UUID(agent_id) if agent_id is not None else None
        except ValueError as error:
            raise SdkError("agent_id must be a UUID") from error
        control_plane = _control_plane_client(client, server_url=server_url, api_key=api_key)
        # A handle only addresses an agent the control plane already serves, so it may name a builtin.
        with allow_reserved_agent_name():
            agent = cls(model=_DEFAULT_MODEL, name=agent_name or DEFAULT_AGENT_NAME)
        agent._bundle.remote_deployment = control_plane._agent_deployment(
            agent_deployment_id=parsed_agent_id, agent_deployment_name=agent_name
        )
        return agent

    @deprecated(
        "Agent.create_session() is deprecated; use Agent.start_session(), which takes the same history=, "
        "session_inputs= and agent= options and returns an agents.Session handle.",
        category=DeprecationWarning,
    )
    @public_errors
    async def create_session(
        self,
        *,
        permission_mode: authoring_types.PermissionMode | None = None,
        history: list[harness_session.HistoryImportEntry] | None = None,
        output_type: type[BaseModel] | None = None,
        agent: SessionAgentCustomization | dict[str, str] | None = None,
        session_inputs: Mapping[str, contracts.SessionInput] | None = None,
        idempotency_key: IdempotencyKey | None = None,
        initial_turn: harness_session.InitialTurn | None = None,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
    ) -> harness_session.SessionClient:
        """Create an attached local or deployment-backed Harness Session.

        Deprecated: use ``Agent.start_session``. This method still works as before and returns the
        raw Session client, but warns, and so does the client's ``run_turn``. ``permission_mode``
        overrides the agent's permission mode for a local session and is deprecated too: set
        ``permission_mode=`` or ``permission_policy=`` on the Agent.

        A deployment-backed Session speaks the Session v1 stream, which serves history entries,
        turns, session status and callbacks, but no ``notice`` or ``error`` event.

        ``agent`` customizes the saved Agent for this Session only, leaving the deployment unchanged:
        ``additional_instructions`` append to the base instructions, and ``model`` and
        ``reasoning_effort`` override the saved completion defaults. A custom completion provider rejects
        the ``model`` and ``reasoning_effort`` overrides; configure that provider directly instead.

        ``session_inputs`` supplies the Session inputs keyed by each value's ``input_id``;
        they are fixed for the Session's lifetime and delivered only to the tools, hooks and
        sandbox hooks that declare them with ``agents.Depends()``.

        ``idempotency_key`` (1 to 256 characters) makes a deployment-backed start safe to retry:
        a retry by the same caller with the same key returns the original Session, and a different
        request with the same key raises ``agents.SessionIdempotencyConflictError``. Use a UUID (or a similar
        random value) generated once per request and reused on each retry.
        A retry that reaches a Session already in a turn waits for that turn to end; one that
        reaches an ended Session fails. An in-process Session lives only in this process, so the
        key has no effect there.

        ``initial_turn`` starts the Session with that message as its first Turn, which the client
        state holds once this returns. A deployment-backed Session needs Session v1. A control plane
        or an Agent that predates ``initial_turn`` starts the Session idle, with no Turn.

        ``on_client_tool`` answers the agent's client tools for every turn run with ``run_turn``, its
        subagents' included. A function takes an ``agents.ClientToolCall`` and returns the result
        the model reads, synchronously or not. ``agents.ClientToolAnswers`` holds one answer per
        tool, each bound with ``<tool>.answer(function)``, and a ``default`` function for every other
        call. If an answer raises, the model gets a failed tool call. Neither gets a call of a tool the
        host provides, such as the connector sign-in (``connectors.ask_enable_connector``).
        """
        if permission_mode is not None:
            warnings.warn(
                "Agent.create_session(permission_mode=...) is deprecated: a Session cannot override the "
                "Agent's permissions. Set permission_mode= or permission_policy= on the Agent instead.",
                DeprecationWarning,
                # The caller's line: past this method and its ``public_errors`` wrapper.
                stacklevel=3,
            )
        client = await self._create_session(
            permission_mode=permission_mode,
            history=history,
            output_type=output_type,
            agent=agent,
            session_inputs=session_inputs,
            idempotency_key=idempotency_key,
            initial_turn=initial_turn,
            client_tools=self._client_tool_registry(on_client_tool),
        )
        return _deprecated_run_turn(client)

    async def _create_session(
        self,
        *,
        permission_mode: authoring_types.PermissionMode | None = None,
        history: list[harness_session.HistoryImportEntry] | None = None,
        output_type: type[BaseModel] | None = None,
        agent: SessionAgentCustomization | dict[str, str] | None = None,
        session_inputs: Mapping[str, contracts.SessionInput] | None = None,
        idempotency_key: IdempotencyKey | None = None,
        initial_turn: harness_session.InitialTurn | None = None,
        client_tools: client_tools_registry.ClientToolRegistry = client_tools_registry.NO_CLIENT_TOOLS,
    ) -> harness_session.SessionClient:
        # create_session without its deprecation warnings, for the SDK's own callers. Closing the
        # client of a local session that has no work left ends it before the close returns, as when
        # it ran in a runtime of its own.
        # The session's client answers ``client_tools``.
        if self.permission_policy is not None and permission_mode not in (None, "auto"):
            raise SdkError("permission_mode cannot override an Agent custom permission policy")
        client_tool_registry = client_tools
        selected_permission_mode = permission_mode if permission_mode is not None else self.permission_mode
        if selected_permission_mode not in ("auto", "ask", "deny"):
            raise SdkError(f"invalid permission_mode {selected_permission_mode!r}; expected 'auto', 'ask', or 'deny'")
        # Checked in both run modes, so a key that a deployment would refuse also fails in-process.
        handles.checked_idempotency_key(idempotency_key)
        customization = SessionAgentCustomization.model_validate(agent) if agent is not None else None
        if self._bundle.remote_deployment is not None:
            if permission_mode is not None:
                raise remote_transport.RemoteSessionProcedureUnsupportedError(
                    method="Agent.create_session(permission_mode=...)",
                    backend="vibe_agents",
                    reason=(
                        "a deployment-backed Session uses the permission mode pinned in its "
                        "deployed Agent configuration"
                    ),
                )
            if output_type is not None:
                raise remote_transport.RemoteSessionProcedureUnsupportedError(
                    method="Agent.create_session(output_type=...)",
                    backend="vibe_agents",
                    reason="a deployment-backed Session uses the completion config pinned in its deployed Agent",
                )
            serialized_inputs = session_input_assembly.serialize_session_inputs(session_inputs) or None
            if customization is None:
                return await remote_transport._create_remote_session(
                    self._bundle.remote_deployment,
                    history=history,
                    idempotency_key=idempotency_key,
                    session_inputs=serialized_inputs,
                    initial_turn=initial_turn,
                    client_tools=client_tool_registry,
                )
            return await remote_transport._create_remote_session(
                self._bundle.remote_deployment,
                history=history,
                idempotency_key=idempotency_key,
                agent=customization,
                session_inputs=serialized_inputs,
                initial_turn=initial_turn,
                client_tools=client_tool_registry,
            )
        session_id = str(uuid4())
        agent_config = self._to_agent_config(output_type=output_type)
        # Without a bound runtime, the session runs in the event loop's runtime, as every local session
        # does: it is listed, agent.session(id) reaches it, and an agents.local_runtime() block's exit
        # stops it. Closing the client detaches it; the runtime ends the tree once it is idle.
        local_runtime = self._bundle.local_runtime or local._process_runtime()
        bound_assembly = self._local_root_assembly(
            local_runtime,
            session_id,
            agent_config,
            permission_mode=selected_permission_mode,
            customization=customization,
        )
        return await local_runtime.create_session(
            bound_assembly,
            history=history,
            session_id=session_id,
            session_inputs=session_inputs,
            completion_provider=self._bundle.completion_provider,
            initial_turn=initial_turn,
            client_tools=client_tool_registry,
            end_idle_tree_on_close=True,
        )

    @classmethod
    @deprecated(
        "Agent.load_session() is deprecated; use Agent.load_from(agent_name=...).session(session_id), which "
        "returns an agents.Session handle, then session_protocol.attach(session) from "
        "mistralai.agents.experimental for the raw client.",
        category=DeprecationWarning,
    )
    @public_errors
    async def load_session(
        cls,
        session_id: str,
        *,
        server_url: str | None = None,
        api_key: str | None = None,
        client: Client | None = None,
        on_client_tool: client_tools_registry.OnClientTool | None = None,
    ) -> harness_session.SessionClient:
        """Reattach to a durable session by its ID alone, without the agent's code or name.

        Deprecated: use ``Agent.load_from(agent_name=...).session(session_id)``. This method still
        works as before and returns the raw Session client, but warns, and so does the client's
        ``run_turn``.

        ``on_client_tool`` answers the Session's client tools, as in ``create_session``.

        ``client``, ``server_url`` and ``api_key`` are those of ``Agent.load_from``.
        """
        control_plane = _control_plane_client(client, server_url=server_url, api_key=api_key)
        return _deprecated_run_turn(
            await remote_transport._get_remote_session(
                control_plane._agent_deployment(),
                session_id,
                # No agent here: its client tools take the default tool_errors.
                client_tools=client_tools_registry.build_client_tool_registry(on_client_tool),
            )
        )

    def _redaction(self) -> tuple[OperationDataTransformer, ...] | None:
        """The policies a worker applies to this Agent's telemetry, or ``None`` for the worker's default."""

        return self._bundle.redaction


class _DeprecatedRunTurnClient(client_tools_registry.ClientToolSessionClient):
    """The raw Session client of the deprecated Agent methods: its ``run_turn`` warns.

    ``agent.run`` and ``agents chat`` keep the plain client, so they do not warn.
    """

    @deprecated(
        "SessionClient.run_turn() is deprecated; use agents.Session: session.run() runs a turn and "
        "turn.iter_events() gives its events.",
        category=DeprecationWarning,
    )
    def run_turn(
        self,
        message: list[harness_session.ContentBlock],
        *,
        message_entry_id: HistoryEntryId | None = None,
        idempotency_key: str | None = None,
        context_messages: list[harness_session.ContextMessage] | None = None,
    ) -> AsyncGenerator[harness_session.ClientEvent]:
        return super().run_turn(
            message,
            message_entry_id=message_entry_id,
            idempotency_key=idempotency_key,
            context_messages=context_messages,
        )


def _deprecated_run_turn(client: harness_session.SessionClient) -> harness_session.SessionClient:
    # The client is built deep in the transports, which also serve the SDK's own callers; its class
    # is swapped here instead. It adds no state, so the swap keeps the client as it is.
    if type(client) is client_tools_registry.ClientToolSessionClient:
        client.__class__ = _DeprecatedRunTurnClient
    return client


def _control_plane_client(client: Client | None, *, server_url: str | None, api_key: str | None) -> Client:
    """The ``agents.Client`` of ``load_from`` and ``load_session``: ``client``, else one without a pool
    built from ``server_url`` and ``api_key``."""
    from mistralai.vibe_agents.sdk.client.api_client import Client  # noqa: PLC0415

    if client is None:
        return Client._per_call(api_key=api_key, server_url=server_url)
    if not isinstance(client, Client):
        raise SdkError(f"client must be an agents.Client or None, got {type(client).__name__}")
    if server_url is not None or api_key is not None:
        raise SdkError("Pass client= or server_url= and api_key=, not both: the client has its own")
    return client


def _require_unsandboxed_workflow(error_type: type[Exception] = SdkError) -> None:
    # Fail fast instead of hanging. An agent does legit non-deterministic work (env reads, asyncio tasks)
    # in the workflow thread; under Temporal's determinism sandbox that work wedges silently before the
    # agent loop, so a worker workflow that forgot enforce_determinism=False just times out with no
    # signal. Local runs and activities return False here, so this only fires on a misconfigured worker.
    if temporalio.workflow.unsafe.in_sandbox():
        raise error_type(
            "The Agents SDK is running inside Temporal's determinism sandbox, which blocks the agent "
            "runtime and will hang. Define the workflow with enforce_determinism=False, e.g. "
            "@workflows.workflow.define(name=..., enforce_determinism=False). See the worker docs."
        )


def _default_harness() -> contracts.Harness:
    return contracts.Harness()


def _resume_from_state(state: dict[str, object]) -> _LegacyResumedState:
    from mistralai.workflows.plugins.nuage_v2.sdk._internal import session as sdk_session  # noqa: PLC0415

    return cast(_LegacyResumedState, sdk_session.Session.from_state_parts(state))


async def _first_turn_id(session: handles.Session) -> str | None:
    async with session._connect() as raw:
        page = (
            await raw.request(
                "app_server/session/turns/list",
                harness_session.SessionTurnsListParams(
                    session_id=session.id, page=harness_session.PageRequest(direction="forward", limit=1)
                ),
                harness_session.SessionTurnsListResponse,
            )
        ).page
    return page.items[0].id if page.items else None


async def _raising_from_client_tools[T](client: harness_session.SessionClient | None, waiting: Awaitable[T]) -> T:
    """Await ``waiting``, unless a client tool answer raises first with tool_errors="raise"."""

    if client is None:
        return await waiting
    return await client_tools_registry.raise_from_client_tools(client, waiting)


async def _run_initial_turn(
    session: handles.Session,
    turn_id: str | None,
    content: UserContentLike,
    output_type: type[BaseModel] | None,
    idempotency_key: str | None,
    timeout: WaitBudget,
    on_event: EventHandler | None,
    client_tools: client_tools_registry.ClientToolRegistry,
) -> TurnState[Any] | Busy:
    """Wait for the session's initial turn, or start the turn when the session started without one.

    A call of ``client_tools``, which the caller answers meanwhile, is not a reason to return ``Blocked``.
    """
    if turn_id is not None:
        state = await session.turn(turn_id)._result(
            after=None, timeout=timeout, on_event=on_event, start=None, client_tools=client_tools
        )
        return state if output_type is None else typed(state, output_type)
    # FIXME: delete once MAIS 2026.11 is released and the control plane's minimum Agents SDK version
    # runs initial_turn. A control plane or an Agent that predates it starts the session idle.
    return await session._run(
        content,
        output_type=output_type,
        idempotency_key=idempotency_key,
        timeout=timeout,
        on_event=on_event,
        client_tools=client_tools,
    )
