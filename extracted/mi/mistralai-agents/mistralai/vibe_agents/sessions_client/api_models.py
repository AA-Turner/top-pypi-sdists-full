"""Pydantic boundary models for the vibe_agents sessions HTTP API.

These mirror ``vibe_agents/api/schemas/session.py`` field-for-field, but command
sources default to the SDK's origin rather than the server's VCW default. They
are intentionally separate from the workflow contract types in
``mistralai.vibe_agents.session_workflow.*``: the workflow types describe
the runtime contract a workflow implements; these describe the wire
format of the control-plane HTTP API.
"""

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, Literal
from uuid import UUID

import structlog
from pydantic import ConfigDict, Field, StringConstraints
from pydantic.json_schema import SkipJsonSchema

from mistralai.vibe_agents._internal.wire_models import ForwardCompatibleModel
from mistralai.vibe_agents.session_workflow import (
    AGENTS_SDK_COMMAND_SOURCE,
    CallbackResultPayload,
    CommandMetadata,
    JsonObject,
    MessageInput,
    Principal,
    SessionAgentCustomization,
    SessionWorkflowCommand,
    SessionWorkflowSubscription,
    ToolsetInput,
)

logger = structlog.get_logger(__name__)

# Idempotency key of the control-plane requests (session start, message send), shared with the
# controller schemas. Any string is accepted, but callers should send a UUID (or a similar random value), as the IETF
# Idempotency-Key draft suggests: a predictable key can collide with the same caller's other requests.
IdempotencyKey = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=256)]


class _APIModel(ForwardCompatibleModel):
    # ``populate_by_name`` keeps validation symmetric with the server schema,
    # which uses ``serialization_alias`` (server accepts both forms). Without
    # it, a Python caller passing the snake_case kwarg for an aliased field
    # would hit a misleading ``Field required: <alias>`` error.
    model_config = ConfigDict(populate_by_name=True)


class SessionProtocol(StrEnum):
    """Session event format, chosen once at creation and immutable thereafter."""

    LEGACY_TASK_PROTOCOL = "legacy_task_protocol"
    SESSION_V1 = "session_v1"


class StartAgentSessionRequest(_APIModel):
    # FIXME(slack-legacy): mirrors the server-owned workflow binding while
    # legacy Slack and Slack Connector coexist. Public SDK calls intentionally
    # omit it, and generated request schemas should not advertise it.
    initial_command_workflow_integration_id: SkipJsonSchema[None] = Field(default=None, exclude=True)
    idempotency_key: IdempotencyKey
    agent_name: str | None = None
    agent: SessionAgentCustomization | None = Field(default=None, exclude_if=lambda value: value is None)
    initial_command: SessionWorkflowCommand | None = None
    app_context: JsonObject | None = None
    initial_subscriptions: list[SessionWorkflowSubscription] = Field(default_factory=list)
    # Read only by the Vibe Code web Workflow; SDK Sessions take their idle limit from worker
    # configuration. Kept off the generated schema so the SDK does not advertise it.
    inactive_timeout_seconds: SkipJsonSchema[float | None] = Field(
        default=None, gt=0.0, exclude_if=lambda value: value is None
    )
    toolsets: list[ToolsetInput] = Field(default_factory=list)
    session_protocol: SessionProtocol | None = None
    # Harness Session inputs keyed by input ID: fixed for the Session
    # lifetime, delivered only to declared tool/hook consumers, never visible
    # to the model.
    session_inputs: JsonObject | None = None
    # Harness ``InitialTurn`` as JSON, so importing this module does not load the Harness. Left
    # out when unset: a control plane that predates the field refuses it.
    initial_turn: JsonObject | None = Field(default=None, exclude_if=lambda value: value is None)


class AgentSessionStatus(StrEnum):
    """A session's product status, as the server reports it.

    ``UNKNOWN`` stands for a status a newer server reports and this SDK does not know.
    Readers treat it as a live session; a non-string status is still rejected.
    """

    STARTING = "starting"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    TERMINATED = "terminated"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value: object) -> "AgentSessionStatus | None":
        if not isinstance(value, str):
            return None
        logger.debug("Reading unknown agent session status", status=value)
        return cls.UNKNOWN


class SessionToolset(_APIModel):
    """A toolset as a session response reports it.

    The read-side counterpart of ``ToolsetInput``, which stays strict because it checks
    what a client sends. ``type`` is ``"connector"`` today and is kept as a plain string,
    so a toolset type or field from a newer server does not fail the response.
    """

    type: str
    id: UUID | None = None
    name: str | None = None


class SessionAgentConfiguration(_APIModel):
    """The agent configuration a session response reports.

    The read-side counterpart of ``AgentConfiguration``. ``reasoning_effort`` is kept as
    a plain string for the same reason as ``SessionToolset.type``.
    """

    toolsets: list[SessionToolset] = Field(default_factory=list)
    additional_instructions: str = ""
    model: str | None = None
    reasoning_effort: str | None = None


class AgentSessionResponse(_APIModel):
    agent_session_id: UUID
    parent_session_id: UUID | None = None
    root_session_id: UUID | None = None
    agent_path: str | None = None
    config_name: str | None = None
    application_id: UUID
    application_name: str
    agent_id: UUID
    agent_name: str
    agent_configuration: SessionAgentConfiguration = Field(default_factory=SessionAgentConfiguration)
    status: AgentSessionStatus
    error: str | None = None
    generated_title: str | None = Field(default=None, max_length=255)
    title: str | None = Field(default=None, max_length=255)
    archived_at: datetime | None = None
    principal: Principal
    workflow_name: str
    deployment_name: str
    app_context: JsonObject | None = None
    # The control plane's record of how the Session ended; `cause` names the Session limit that
    # stopped it.
    terminal_output: JsonObject | None = None
    # Defaulted, not required: a control plane older than this field still answers without it, and
    # every session it knows about predates Session v1.
    session_protocol: SessionProtocol = SessionProtocol.LEGACY_TASK_PROTOCOL
    last_event_insert_seq: int
    created_at: datetime
    updated_at: datetime


class _CatalogScopeInput(_APIModel):
    # The client builds a scope and sends it as query parameters; it never reads one.
    model_config = ConfigDict(extra="forbid")


class RootsScopeInput(_CatalogScopeInput):
    scope: Literal["roots"] = "roots"


class DirectChildrenScopeInput(_CatalogScopeInput):
    scope: Literal["direct_children"] = "direct_children"
    parent_session_id: UUID


class TreeScopeInput(_CatalogScopeInput):
    scope: Literal["tree"] = "tree"
    root_session_id: UUID


type SessionCatalogScopeInput = Annotated[
    RootsScopeInput | DirectChildrenScopeInput | TreeScopeInput, Field(discriminator="scope")
]


class ListSessionsResult(_APIModel):
    items: list[AgentSessionResponse]
    next_cursor: str | None = Field(default=None, alias="next")


class RenameSessionRequest(_APIModel):
    title: str | None = Field(max_length=255)


class ArchiveSessionRequest(_APIModel):
    archived: bool


class InitialTurnResponse(_APIModel):
    """A start's initial Turn, only its ID, chosen by the control plane."""

    id: str


class StartAgentSessionResponse(_APIModel):
    agent_session: AgentSessionResponse
    # Present only when the start carried initial_turn.
    initial_turn: InitialTurnResponse | None = None


class ObservedControllerEventResponse(_APIModel):
    sequence: str
    event: dict[str, Any]


class SessionEventsHistoryResponse(_APIModel):
    events: list[ObservedControllerEventResponse]
    next_cursor: str | None = Field(alias="nextCursor")


class SubmitAgentMessageRequest(_APIModel):
    type: Literal["message"] = "message"
    command_id: UUID
    source: str = AGENTS_SDK_COMMAND_SOURCE
    message: MessageInput
    metadata: CommandMetadata | None = None
    expected_turn_id: str | None = Field(default=None, exclude_if=lambda value: value is None)


class InterruptAgentSessionRequest(_APIModel):
    type: Literal["interrupt_session"] = "interrupt_session"
    command_id: UUID
    source: str = AGENTS_SDK_COMMAND_SOURCE
    reason: str = "interrupt requested"
    expected_turn_id: str


class CancelAgentSessionRequest(_APIModel):
    type: Literal["cancel_session"] = "cancel_session"
    command_id: UUID
    source: str = AGENTS_SDK_COMMAND_SOURCE
    reason: str = "cancel requested"


class SubmitAgentMessageResponse(_APIModel):
    agent_session_id: UUID
    command_id: UUID


class SubmitCallbackResultRequest(_APIModel):
    result: CallbackResultPayload


class SubmitCallbackResultResponse(_APIModel):
    agent_session_id: UUID
    callback_id: UUID


__all__ = [
    "AgentSessionResponse",
    "AgentSessionStatus",
    "CancelAgentSessionRequest",
    "InterruptAgentSessionRequest",
    "ObservedControllerEventResponse",
    "SessionAgentConfiguration",
    "SessionEventsHistoryResponse",
    "SessionProtocol",
    "SessionToolset",
    "StartAgentSessionRequest",
    "StartAgentSessionResponse",
    "SubmitAgentMessageRequest",
    "SubmitAgentMessageResponse",
    "SubmitCallbackResultRequest",
    "SubmitCallbackResultResponse",
]
