"""Task Protocol payload models used by session workflows.

These models are the shared wire contract for history entries emitted through
``WorkflowSessionEvent``. They intentionally stay dependency-light so runtimes
can import them from workflow sandboxes without pulling in the vibe_agents
service or ``mistralai.workflows``.
"""

import typing
from enum import StrEnum
from typing import Annotated, Final, Literal, Self
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Field,
    JsonValue,
    TypeAdapter,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel

from mistralai.vibe_agents.session_workflow.commands import (
    MessagePart,
    SessionWorkflowCommand,
    validate_image_url,
)
from mistralai.vibe_agents.session_workflow.toolsets import ToolsetInput

type JsonObject = dict[str, JsonValue]

MESSAGE_HISTORY_ENTRY_TYPE: Final[Literal["message"]] = "message"
STATE_HISTORY_ENTRY_TYPE: Final[Literal["state"]] = "state"
TASK_CALL_HISTORY_ENTRY_TYPE: Final[Literal["task_call"]] = "task_call"
TASK_RESULT_HISTORY_ENTRY_TYPE: Final[Literal["task_result"]] = "task_result"
RESERVED_HISTORY_ENTRY_TYPES: Final[frozenset[str]] = frozenset(
    {
        MESSAGE_HISTORY_ENTRY_TYPE,
        STATE_HISTORY_ENTRY_TYPE,
        TASK_CALL_HISTORY_ENTRY_TYPE,
        TASK_RESULT_HISTORY_ENTRY_TYPE,
    }
)


class _TaskProtocolModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        validate_by_name=True,
        validate_by_alias=True,
    )


class GenerationStatus(StrEnum):
    GENERATING = "generating"
    COMPLETE = "complete"


class OpenHistoryEntry(_TaskProtocolModel):
    """Fallback entry for runtime-defined history variants outside the closed union."""

    type: str | None = None
    generation_status: GenerationStatus | str | None = GenerationStatus.COMPLETE
    annotations: JsonObject | None = None
    payload: JsonValue = None

    @model_validator(mode="after")
    def reject_known_history_entry_type(self) -> Self:
        if self.type in RESERVED_HISTORY_ENTRY_TYPES:
            raise ValueError(f"{self.type!r} is a reserved HistoryEntry type")
        return self


class MessageTextContentBlock(_TaskProtocolModel):
    type: Literal["text"] = "text"
    text: str
    annotations: JsonObject | None = Field(default=None, exclude_if=lambda value: value is None)


class MessageResourceLinkContentBlock(_TaskProtocolModel):
    type: Literal["resource_link"] = "resource_link"
    uri: str
    name: str | None = None
    mime_type: str | None = Field(default=None, exclude_if=lambda value: value is None)
    annotations: JsonObject | None = Field(default=None, exclude_if=lambda value: value is None)


class MessageImageContentBlock(_TaskProtocolModel):
    type: Literal["image"] = "image"
    image_url: str
    annotations: JsonObject | None = Field(default=None, exclude_if=lambda value: value is None)

    @field_validator("image_url")
    @classmethod
    def _validate_image_url(cls, value: str) -> str:
        return validate_image_url(value)


type MessageContentBlock = Annotated[
    MessageTextContentBlock | MessageImageContentBlock | MessageResourceLinkContentBlock | JsonObject,
    Field(union_mode="left_to_right"),
]


class MessageMeta(_TaskProtocolModel):
    source: str | None = None
    kind: str | None = None
    display_label: str | None = None


class MessageHistoryEntryPayload(_TaskProtocolModel):
    role: Literal["system", "user", "assistant"]
    content: list[MessageContentBlock] = Field(default_factory=list)
    channel: Literal["thinking", "message"] | None = None
    meta: MessageMeta | JsonObject | None = Field(default=None, union_mode="left_to_right")


class MessageHistoryEntry(_TaskProtocolModel):
    type: Literal["message"] = MESSAGE_HISTORY_ENTRY_TYPE
    id: str | None = None
    generation_status: GenerationStatus | str = GenerationStatus.COMPLETE
    annotations: JsonObject | None = None
    payload: MessageHistoryEntryPayload


class CallbackRequestedBody(_TaskProtocolModel):
    action: str | None = None
    question: str | None = None
    description: str | None = None


class CallbackRequestedStateContent(_TaskProtocolModel):
    callback_id: str
    callback_type: str | None = None
    body: CallbackRequestedBody | JsonValue = Field(default=None, union_mode="left_to_right")


class CallbackRequestedStatePayload(_TaskProtocolModel):
    type: Literal["callback_requested"] = "callback_requested"
    content: CallbackRequestedStateContent

    @property
    def callback_id(self) -> str:
        return self.content.callback_id

    @property
    def structured_body(self) -> CallbackRequestedBody | None:
        if isinstance(self.content.body, CallbackRequestedBody):
            return self.content.body
        return None


class TurnFailureError(_TaskProtocolModel):
    """Why a turn failed: a stable ``code`` for clients to render, plus English ``message``."""

    code: str
    # English fallback for clients that do not know ``code``; never provider-supplied text.
    message: str
    retryable: bool = False


class FailedTurnTermination(_TaskProtocolModel):
    """The turn that just ended failed; the Session stays open for the next message.

    Same shape as the Session v1 ``turn_terminated`` failed termination, so a client reads
    turn failures from both streams the same way.
    """

    outcome: Literal["failed"] = "failed"
    error: TurnFailureError


class WorkflowStatusStateContent(_TaskProtocolModel):
    status: Literal["received", "running", "waiting_for_input", "snapshotting", "completed", "failed"]
    # Set on the ``waiting_for_input`` row that ends a failed turn.
    termination: FailedTurnTermination | None = None


class WorkflowStatusStatePayload(_TaskProtocolModel):
    type: Literal["workflow_status"] = "workflow_status"
    content: WorkflowStatusStateContent


class ProgressStateContent(_TaskProtocolModel):
    status: Literal["started", "progress", "success", "failure"]
    title: str
    content: str
    code: str | None = None


class ProgressStatePayload(_TaskProtocolModel):
    type: Literal["progress"] = "progress"
    content: ProgressStateContent


class QuotaStatusStateContent(_TaskProtocolModel):
    status: Literal["granted", "queued", "denied"]
    title: str
    message: str


class QuotaStatusStatePayload(_TaskProtocolModel):
    type: Literal["quota_status"] = "quota_status"
    content: QuotaStatusStateContent


class CallbackResolvedStateContent(_TaskProtocolModel):
    callback_id: str
    output: JsonValue = None
    error: str | None = None


class CallbackResolvedStatePayload(_TaskProtocolModel):
    type: Literal["callback_resolved"] = "callback_resolved"
    content: CallbackResolvedStateContent


class AlertStateContent(_TaskProtocolModel):
    variant: Literal["info", "success", "warning", "error"]
    title: str
    body_md: str = ""
    level: Literal["public", "private"] = "public"
    # The notice's data, such as a connector's status and reason, as in a Session API notice.
    details: JsonValue = Field(default=None, exclude_if=lambda value: value is None)


class AlertStatePayload(_TaskProtocolModel):
    type: Literal["alert"] = "alert"
    content: AlertStateContent


class OAuthStateContent(_TaskProtocolModel):
    provider: str
    status: Literal["waiting", "connected", "timed_out"]
    oauth_url: str | None = None
    message: str = ""


class OAuthStatePayload(_TaskProtocolModel):
    type: Literal["oauth"] = "oauth"
    content: OAuthStateContent


class SessionUrlStateContent(_TaskProtocolModel):
    label: str
    url: str
    source: str = ""


class SessionUrlStatePayload(_TaskProtocolModel):
    type: Literal["session_url"] = "session_url"
    content: SessionUrlStateContent


class SubscriptionStateContent(_TaskProtocolModel):
    provider: str
    routing_key: str


SubscriptionAction = Literal["added", "removed"]


class SubscriptionUpdateStateContent(_TaskProtocolModel):
    action: SubscriptionAction
    subscriptions: list[SubscriptionStateContent] = Field(default_factory=list)


class SubscriptionUpdateStatePayload(_TaskProtocolModel):
    type: Literal["subscription_update"] = "subscription_update"
    content: SubscriptionUpdateStateContent


class SessionInitializedStateContent(_TaskProtocolModel):
    application_id: UUID
    application_name: str
    agent_id: UUID
    agent_name: str
    source: str | None = None


class SessionInitializedStatePayload(_TaskProtocolModel):
    type: Literal["x-vibe-agent-session-initialized"] = "x-vibe-agent-session-initialized"
    content: SessionInitializedStateContent


type _ToolsetType = typing.Literal["connector"]


class _ToolsetBase(_TaskProtocolModel):
    type: _ToolsetType
    name: str
    description: str
    agent_exposure: str
    authentication: str


class _Connector(_ToolsetBase):
    type: _ToolsetType = "connector"
    id: UUID


type _Toolset = Annotated[_Connector, Discriminator("type")]
type ToolsetDiscoveryMode = Literal["allowlist", "all"]


class ToolsetStateSnapshotContent(_TaskProtocolModel):
    toolsets: list[_Toolset] = Field(default_factory=list)
    requested_toolsets: list[ToolsetInput] = Field(default_factory=list)
    discovery_mode: ToolsetDiscoveryMode = "allowlist"


class ToolsetStateSnapshotPayload(_TaskProtocolModel):
    type: Literal["toolset_state_snapshot"] = "toolset_state_snapshot"
    content: ToolsetStateSnapshotContent


type KnownStateHistoryEntryPayload = Annotated[
    WorkflowStatusStatePayload
    | ProgressStatePayload
    | QuotaStatusStatePayload
    | CallbackResolvedStatePayload
    | AlertStatePayload
    | OAuthStatePayload
    | SessionUrlStatePayload
    | SubscriptionUpdateStatePayload
    | SessionInitializedStatePayload
    | ToolsetStateSnapshotPayload,
    Field(discriminator="type"),
]


class StateHistoryEntryPayload(_TaskProtocolModel):
    type: str
    content: JsonValue


type AnyStateHistoryEntryPayload = Annotated[
    KnownStateHistoryEntryPayload | StateHistoryEntryPayload,
    Field(union_mode="left_to_right"),
]


class StateHistoryEntry(_TaskProtocolModel):
    type: Literal["state"] = STATE_HISTORY_ENTRY_TYPE
    id: str | None = None
    generation_status: GenerationStatus | str = GenerationStatus.COMPLETE
    annotations: JsonObject | None = None
    payload: AnyStateHistoryEntryPayload


class TaskCallHistoryEntryPayload(_TaskProtocolModel):
    type: Literal["child_task"] = "child_task"
    id: str = ""
    name: str = ""
    input: JsonValue = None


class CallbackTaskCallHistoryEntryPayload(_TaskProtocolModel):
    type: Literal["callback"] = "callback"
    id: UUID
    name: str = ""
    input: JsonValue = None
    tool_call_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    tool_id: str | None = Field(default=None, exclude_if=lambda value: value is None)


class CallbackHandlerTaskCallHistoryEntryPayload(_TaskProtocolModel):
    type: Literal["callback_handler"] = "callback_handler"
    id: str = ""
    name: str = ""
    input: JsonValue = None
    callback_id: str = ""
    child_task_id: str = ""
    callback_path: list[str] = Field(default_factory=list)


type AnyTaskCallHistoryEntryPayload = Annotated[
    TaskCallHistoryEntryPayload | CallbackTaskCallHistoryEntryPayload | CallbackHandlerTaskCallHistoryEntryPayload,
    Field(discriminator="type"),
]


class TaskCallHistoryEntry(_TaskProtocolModel):
    type: Literal["task_call"] = TASK_CALL_HISTORY_ENTRY_TYPE
    generation_status: GenerationStatus | str = GenerationStatus.COMPLETE
    annotations: JsonObject | None = None
    payload: AnyTaskCallHistoryEntryPayload = Field(default_factory=TaskCallHistoryEntryPayload)


class TaskOutputPayload(_TaskProtocolModel):
    status: Literal["running", "failed", "completed", "canceled"] | str = "running"
    value: JsonValue = None
    error: str | None = None


class TaskStatePayload(_TaskProtocolModel):
    id: str = ""
    input: JsonValue = None
    output: TaskOutputPayload | JsonObject = Field(default_factory=TaskOutputPayload, union_mode="left_to_right")
    history: list["HistoryEntry"] | None = None


class TaskResultHistoryEntryPayload(_TaskProtocolModel):
    id: str = ""
    name: str = ""
    state: TaskStatePayload | None = None


class TaskResultHistoryEntry(_TaskProtocolModel):
    type: Literal["task_result"] = TASK_RESULT_HISTORY_ENTRY_TYPE
    generation_status: GenerationStatus | str = GenerationStatus.COMPLETE
    annotations: JsonObject | None = None
    payload: TaskResultHistoryEntryPayload = Field(default_factory=TaskResultHistoryEntryPayload)


type ClosedHistoryEntry = Annotated[
    MessageHistoryEntry | StateHistoryEntry | TaskCallHistoryEntry | TaskResultHistoryEntry,
    Field(discriminator="type"),
]
type HistoryEntry = Annotated[ClosedHistoryEntry | OpenHistoryEntry, Field(union_mode="left_to_right")]

HistoryEntryAdapter: TypeAdapter[HistoryEntry] = TypeAdapter(HistoryEntry)


class WorkflowWaitingForInputPayload(_TaskProtocolModel):
    status: Literal["waiting_for_input"] = "waiting_for_input"
    callback_id: str
    label: str | None = None
    input_schema: JsonValue = None


class WorkflowCompletedPayload(_TaskProtocolModel):
    status: Literal["completed"] = "completed"
    result: JsonValue = None


class WorkflowFailedPayload(_TaskProtocolModel):
    status: Literal["failed"] = "failed"
    error: str | None = None


type WorkflowStatusEventPayload = Annotated[
    WorkflowWaitingForInputPayload | WorkflowCompletedPayload | WorkflowFailedPayload,
    Field(discriminator="status"),
]
WorkflowStatusEventPayloadAdapter: TypeAdapter[WorkflowStatusEventPayload] = TypeAdapter(WorkflowStatusEventPayload)


class WaitForInputTaskPayload(_TaskProtocolModel):
    label: str | None = None
    input_schema: JsonValue = None


class AssistantMessagePayload(BaseModel):
    parts: list[MessagePart] = Field(default_factory=list)


class ObservedCommandPayload(BaseModel):
    command: SessionWorkflowCommand


TaskStatePayload.model_rebuild()
TaskResultHistoryEntryPayload.model_rebuild()
HistoryEntryAdapter.rebuild()

# Nuage-session aliases. They keep existing upstream names while pointing at
# the shared contract classes above.
TextPart = MessageTextContentBlock
MessageContentPart = MessageTextContentBlock
MessageEntryPayload = MessageHistoryEntryPayload
MessageEntry = MessageHistoryEntry
WorkflowStatusContent = WorkflowStatusStateContent
WorkflowStatusPayload = WorkflowStatusStatePayload
ProgressContent = ProgressStateContent
ProgressPayload = ProgressStatePayload
QuotaStatusContent = QuotaStatusStateContent
QuotaStatusPayload = QuotaStatusStatePayload
CallbackRequestedContent = CallbackRequestedStateContent
CallbackRequestedPayload = CallbackRequestedStatePayload
CallbackResolvedContent = CallbackResolvedStateContent
CallbackResolvedPayload = CallbackResolvedStatePayload
AlertContent = AlertStateContent
AlertPayload = AlertStatePayload
OAuthContent = OAuthStateContent
OAuthPayload = OAuthStatePayload
SessionUrlContent = SessionUrlStateContent
SessionUrlPayload = SessionUrlStatePayload
SubscriptionUpdateContent = SubscriptionUpdateStateContent
SubscriptionUpdatePayload = SubscriptionUpdateStatePayload
ToolsetStateSnapshotContent = ToolsetStateSnapshotContent
ToolsetStateSnapshotPayload = ToolsetStateSnapshotPayload
StateEntryPayload = AnyStateHistoryEntryPayload
StateEntry = StateHistoryEntry
CallbackHandlerTaskCallPayload = CallbackHandlerTaskCallHistoryEntryPayload
CallbackTaskCallPayload = CallbackTaskCallHistoryEntryPayload
TaskCallPayload = TaskCallHistoryEntryPayload
TaskCallEntry = TaskCallHistoryEntry
TaskOutput = TaskOutputPayload
TaskStateRef = TaskStatePayload
TaskResultPayload = TaskResultHistoryEntryPayload
TaskResultEntry = TaskResultHistoryEntry

__all__ = [
    "AlertContent",
    "AlertPayload",
    "AlertStateContent",
    "AlertStatePayload",
    "AnyStateHistoryEntryPayload",
    "AnyTaskCallHistoryEntryPayload",
    "AssistantMessagePayload",
    "CallbackResolvedContent",
    "CallbackResolvedPayload",
    "CallbackResolvedStateContent",
    "CallbackResolvedStatePayload",
    "CallbackHandlerTaskCallHistoryEntryPayload",
    "CallbackHandlerTaskCallPayload",
    "CallbackTaskCallHistoryEntryPayload",
    "CallbackTaskCallPayload",
    "ClosedHistoryEntry",
    "FailedTurnTermination",
    "GenerationStatus",
    "HistoryEntry",
    "HistoryEntryAdapter",
    "JsonObject",
    "JsonValue",
    "KnownStateHistoryEntryPayload",
    "MESSAGE_HISTORY_ENTRY_TYPE",
    "MessageContentBlock",
    "MessageContentPart",
    "MessageEntry",
    "MessageEntryPayload",
    "MessageHistoryEntry",
    "MessageHistoryEntryPayload",
    "MessageImageContentBlock",
    "MessageMeta",
    "MessageResourceLinkContentBlock",
    "MessageTextContentBlock",
    "OAuthContent",
    "OAuthPayload",
    "OAuthStateContent",
    "OAuthStatePayload",
    "ObservedCommandPayload",
    "OpenHistoryEntry",
    "ProgressContent",
    "ProgressPayload",
    "ProgressStateContent",
    "ProgressStatePayload",
    "QuotaStatusContent",
    "QuotaStatusPayload",
    "QuotaStatusStateContent",
    "QuotaStatusStatePayload",
    "RESERVED_HISTORY_ENTRY_TYPES",
    "SessionInitializedStateContent",
    "SessionInitializedStatePayload",
    "SessionUrlContent",
    "SessionUrlPayload",
    "SessionUrlStateContent",
    "SessionUrlStatePayload",
    "StateEntry",
    "StateEntryPayload",
    "STATE_HISTORY_ENTRY_TYPE",
    "StateHistoryEntry",
    "StateHistoryEntryPayload",
    "SubscriptionAction",
    "SubscriptionStateContent",
    "SubscriptionUpdateContent",
    "SubscriptionUpdatePayload",
    "SubscriptionUpdateStateContent",
    "SubscriptionUpdateStatePayload",
    "TaskCallEntry",
    "TASK_CALL_HISTORY_ENTRY_TYPE",
    "TaskCallHistoryEntry",
    "TaskCallHistoryEntryPayload",
    "TaskCallPayload",
    "TaskOutput",
    "TaskOutputPayload",
    "TaskResultEntry",
    "TASK_RESULT_HISTORY_ENTRY_TYPE",
    "TaskResultHistoryEntry",
    "TaskResultHistoryEntryPayload",
    "TaskResultPayload",
    "TaskStatePayload",
    "TaskStateRef",
    "TextPart",
    "TurnFailureError",
    "ToolsetStateSnapshotContent",
    "ToolsetStateSnapshotPayload",
    "WaitForInputTaskPayload",
    "WorkflowCompletedPayload",
    "WorkflowFailedPayload",
    "WorkflowStatusEventPayload",
    "WorkflowStatusContent",
    "WorkflowStatusEventPayloadAdapter",
    "WorkflowStatusPayload",
    "WorkflowStatusStateContent",
    "WorkflowStatusStatePayload",
    "WorkflowWaitingForInputPayload",
]
