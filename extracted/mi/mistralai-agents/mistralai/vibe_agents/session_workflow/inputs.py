"""Session workflow start input and related types."""

from typing import Final, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator
from pydantic.json_schema import SkipJsonSchema

from mistralai.vibe_agents.session_workflow.commands import (
    CommandMetadata,
    JsonObject,
    ReasoningEffort,
    SessionWorkflowCommand,
)
from mistralai.vibe_agents.session_workflow.identity import OrgTier, Principal
from mistralai.vibe_agents.session_workflow.providers import normalize_provider_name
from mistralai.vibe_agents.session_workflow.skills import RequestedSkillInput
from mistralai.vibe_agents.session_workflow.toolsets import ToolsetInput

SESSION_ADDITIONAL_INSTRUCTIONS_MAX_LENGTH: Final = 8_000
# The Concurrent Child Turn Limit of a subagent policy that does not set one.
DEFAULT_CONCURRENT_CHILD_TURN_LIMIT: Final = 10
DEFAULT_MAX_SUBAGENT_DEPTH: Final = 2


class SessionWorkflowSubscription(BaseModel):
    # This is the tolerant SDK boundary: routing/storage code must call
    # require_provider_name before treating a provider as supported.
    provider: str
    routing_key: str

    @field_validator("provider", mode="before")
    @classmethod
    def _normalize_provider(cls, provider: object) -> object:
        return normalize_provider_name(provider)


class SessionAgentCustomization(BaseModel):
    """Caller-owned Agent customization for one Session."""

    # Strict on purpose: a request model the control plane validates. Clients read
    # sessions through forward-compatible models (``_internal.wire_models``) instead.
    model_config = ConfigDict(extra="forbid")

    additional_instructions: str = Field(default="", max_length=SESSION_ADDITIONAL_INSTRUCTIONS_MAX_LENGTH)
    model: str | None = Field(default=None, min_length=1, exclude_if=lambda value: value is None)
    reasoning_effort: ReasoningEffort | None = Field(default=None, exclude_if=lambda value: value is None)

    @model_validator(mode="after")
    def reject_null_overrides(self) -> "SessionAgentCustomization":
        if self.model is None and "model" in self.model_fields_set:
            raise ValueError("model cannot be null")
        if self.reasoning_effort is None and "reasoning_effort" in self.model_fields_set:
            raise ValueError("reasoning_effort cannot be null")
        return self

    def apply_to_instructions(self, base: str) -> str:
        if not self.additional_instructions:
            return base
        if not base:
            return self.additional_instructions
        return f"{base}\n\n{self.additional_instructions}"


class SubagentPolicy(BaseModel):
    """Subagent limits for one Session Tree, chosen when its root Session starts.

    The control plane stores the root's policy and copies it to every child, so a child's
    request cannot raise the limit. A Session with no policy cannot create subagents.
    Prompts are not part of it: they belong to the Agent definition on the worker.
    """

    model_config = ConfigDict(frozen=True)

    # How many child Turns may run at once across the whole Session Tree.
    concurrent_child_turn_limit: int = Field(default=DEFAULT_CONCURRENT_CHILD_TURN_LIMIT, ge=1)
    # The deepest level below the root Session (depth 0) a child may sit at; it cannot spawn.
    max_depth: int = Field(default=DEFAULT_MAX_SUBAGENT_DEPTH, ge=1)
    # Whether an agent message from a parent may start a Turn in an idle direct child.
    idle_message_starts: Literal["direct_children", "none"] = "direct_children"


class WorkflowUserMessage(BaseModel):
    """A user message in a Workflow input: the Harness ``UserMessageInput`` fields, as JSON.

    Untyped so that a block this Worker cannot read refuses that message instead of failing to
    decode the whole input, and because this package's ``__init__`` imports no Harness module.
    ``session_workflow.user_message.read_user_message`` reads it.
    """

    message: list[dict[str, JsonValue]] = Field(min_length=1)
    # Only the model reads them.
    context_messages: list[dict[str, JsonValue]] = Field(default_factory=list)
    # Set by the control plane: the correlation id and the tracing the policy resolved.
    metadata: CommandMetadata | None = None


class SessionWorkflowInitialTurn(WorkflowUserMessage):
    """The first user message of a Session, which the Workflow runs as the first Turn."""

    # Chosen by the control plane, so it can return the ID before the Workflow runs.
    turn_id: str = Field(min_length=1)


class SessionStartIntent(BaseModel):
    # TODO: Clarify Principal's authority in the workflow contract. It
    # currently travels as durable caller/tenant identity, while dispatch also
    # sends identity headers; document which layer workflows and activities
    # should trust for user, system, and integration-started sessions.
    principal: Principal
    initial_command: SessionWorkflowCommand | None = None
    # Selects the event protocol for this session. None or "legacy_task_protocol"
    # uses the existing SessionEventChannel; "session_v1" uses the new
    # SessionProtocolChannel emitting canonical session_protocol events.
    # Once set, the protocol is immutable for the session's lifetime.
    session_protocol: Literal["session_v1", "legacy_task_protocol"] | None = None
    # TODO: Keep app_context as app-specific extension data only. Shared Nuage
    # runtime controls should move to typed first-class workflow input fields or
    # a dedicated Nuage runtime input model, not accrete inside the generic
    # vibe_agents <-> Nuage contract.
    app_context: object | None = None
    # Caller-supplied Harness Session inputs keyed by input ID, fixed
    # for the Session lifetime and delivered only to declared tool/hook
    # consumers. Never model-visible; carried verbatim to the Workflow host.
    session_inputs: JsonObject | None = None
    # Runtime-specific durable binding for the initial command. Nuage uses this
    # to replay Slack starts with the same legacy/connector integration selected
    # at ingress time.
    initial_command_workflow_integration_id: str | None = None
    initial_subscriptions: list[SessionWorkflowSubscription] = Field(default_factory=list)
    # Optional per-session business timeout for inactivity between user inputs, read only by the
    # Vibe Code web (nuage_v2) Workflow. SDK Sessions ignore it: their idle limit is worker
    # configuration (`AGENTS_SDK_IDLE_TIMEOUT_SECONDS`). When set, the nuage_v2 workflow uses this
    # value as its multi-turn idle timeout instead of the runtime default. When None, it falls
    # back to the nuage runtime setting.
    #
    # Owned by the workflow on purpose: hitting this timer must exit the
    # workflow cleanly so the SDK interceptor publishes a terminal event and
    # the workflow's finally blocks release sandbox and quota. Temporal's
    # execution_timeout stays in place strictly as a last-resort fallback.
    inactive_timeout_seconds: float | None = Field(default=None, gt=0.0)
    toolsets: list[ToolsetInput] = Field(default_factory=list)
    requested_skills: list[RequestedSkillInput] = Field(default_factory=list)
    agent: SessionAgentCustomization | None = None


class SessionWorkflowStartInput(SessionStartIntent):
    # validate_by_name so the control plane can set the resurrection marker by its
    # Python name while its wire key stays the explicit __-prefixed alias (see the
    # field below), the same convention nuage's app-context carriers use.
    model_config = ConfigDict(validate_by_name=True)

    # The completion gateway band this Session's model calls are scheduled in, resolved by
    # the producer from the caller's customer record at start time.
    #
    # Declared on the workflow payload rather than on SessionStartIntent so that no
    # client-reachable model can carry it: SessionStartIntent is the base of
    # StartAgentSessionInput, and Principal -- the other candidate home -- is a client-supplied
    # request field checked only for tenant-id equality. A caller that could name its own band
    # could name its own scheduling priority.
    #
    # Resolved once, so a tier change mid-Session only takes effect on the next Session.
    # None means the producer did not resolve one; the runtime then uses DEFAULT_ORG_TIER.
    org_tier: OrgTier | None = None
    session_id: UUID
    application_id: UUID
    application_name: str
    agent_id: UUID
    agent_name: str
    correlation_id: str | None = None
    created_at: str
    # Trusted Session-control-plane creation only; not part of public SessionStartIntent.
    child_session: dict[str, JsonValue] | None = None
    # The Session Tree's subagent policy, resolved by the control plane: the Agent's default for
    # a root; children get the root's value. Server-owned like ``org_tier``. None means this
    # Session cannot create subagents.
    subagent_policy: SubagentPolicy | None = None
    # Marks a fresh workflow execution as a resurrection of a Session whose prior
    # execution died (see the nuage session_rehydration module). Server-owned, like
    # ``org_tier`` above: only the control plane (vibe_agents) sets it, when it
    # rebuilds a start input from a durable session row for a send that found the
    # prior execution dead. No client-reachable model carries it - SessionStartIntent
    # is the base of StartAgentSessionInput, and the transport-side boundary
    # (vibe_agents start API schemas) never exposes this field. SkipJsonSchema only
    # hides it from generated schemas; the actual protection is that no public start
    # request model has the field. The __-prefixed serialization alias mirrors
    # nuage's other server-owned wire keys (``__temporary_session_state``).
    is_session_resurrection: SkipJsonSchema[bool] = Field(
        default=False,
        alias="__is_session_resurrection",
    )
    # The ``SharedWorkerAgentSpec`` a shared worker runs for this Session, as JSON. Server-owned
    # for the same reason as ``org_tier``: the control plane builds it from the Agent the Session
    # was started on, so the Session keeps that definition across continue-as-new and resurrection
    # even after the Agent is redeployed. Untyped here so that a spec this worker cannot read
    # fails the Session when the worker validates it, instead of failing to decode the whole
    # input. None for every Agent whose definition lives in its worker's code.
    shared_worker_agent: SkipJsonSchema[dict[str, JsonValue] | None] = None
    # A Worker that predates this field ignores it and starts idle. The control plane never sets
    # it together with initial_command.
    initial_turn: SessionWorkflowInitialTurn | None = None


__all__ = [
    "DEFAULT_CONCURRENT_CHILD_TURN_LIMIT",
    "DEFAULT_MAX_SUBAGENT_DEPTH",
    "SESSION_ADDITIONAL_INSTRUCTIONS_MAX_LENGTH",
    "SessionAgentCustomization",
    "RequestedSkillInput",
    "SessionStartIntent",
    "SubagentPolicy",
    "SessionWorkflowInitialTurn",
    "SessionWorkflowStartInput",
    "SessionWorkflowSubscription",
    "ToolsetInput",
    "WorkflowUserMessage",
]
