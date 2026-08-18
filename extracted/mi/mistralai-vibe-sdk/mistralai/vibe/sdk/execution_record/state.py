"""Execution record state, output, and history entry types.

Defines the durable execution record data types:
- TaskOutput: discriminated union for task completion status
- HistoryEntry: the log entries (MessageEntry, StateEntry, TaskCallEntry,
  TaskResultEntry)
- TaskState: the universal task state container

All types are Pydantic v2 BaseModel — required for produce()/diff()
patch production (model_copy for structural sharing, model_dump for
JSON patch targeting).
"""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import JsonValue as JsonValue

from mistralai.vibe.sdk.execution_record.types import GenerationStatus as GenerationStatus
from mistralai.vibe.sdk.execution_record.utils import OmitFromModelContext

# ---------------------------------------------------------------------------
# TaskOutput — discriminated union for task completion status
# ---------------------------------------------------------------------------


class PendingOutput(BaseModel):
    """Task is still running."""

    status: Literal["running"] = "running"


class CompletedOutput(BaseModel):
    """Task completed successfully with a value."""

    status: Literal["completed"] = "completed"
    value: Any = None
    annotations: Annotated[
        dict[str, JsonValue] | None,
        OmitFromModelContext(extra_exclude_if=lambda value: value is None),
    ] = None


class FailedOutput(BaseModel):
    """Task failed with an error."""

    status: Literal["failed"] = "failed"
    error: str = ""


class CanceledOutput(BaseModel):
    """Task was canceled. Defined for protocol compatibility.

    Not actively used in Phase 1. Cancellation implementation is
    future work.
    """

    status: Literal["canceled"] = "canceled"


TaskOutput = PendingOutput | CompletedOutput | FailedOutput | CanceledOutput


# ---------------------------------------------------------------------------
# HistoryEntry types — the log of what happened during task execution
# ---------------------------------------------------------------------------


class BaseEntry(BaseModel):
    """Base for all history entry types.

    Provides generation_status and annotations inherited by all entry types.
    "generating" means the entry is still being built (e.g., LLM
    streaming text, subtask running). "complete" means the entry
    is finalized.
    """

    generation_status: GenerationStatus = "complete"
    annotations: dict[str, Any] | None = None


class TextContentBlock(BaseModel):
    """Plain text content block."""

    type: Literal["text"] = "text"
    text: str = ""


class ThinkingContentBlock(BaseModel):
    """Reasoning/thinking content block."""

    type: Literal["thinking"] = "thinking"
    thinking: str = ""


class ImageContentBlock(BaseModel):
    """Image content block.

    ``image_url`` is an http(s) URL or a base64 ``data:image/...;base64,...``
    data URI. Carried through history so a turn's inline image survives to the
    completion-request projection, where it is emitted as a native multimodal
    ``image_url`` part instead of being flattened to text.
    """

    type: Literal["image"] = "image"
    image_url: str = ""


ContentBlock = TextContentBlock | ThinkingContentBlock | ImageContentBlock


def content_blocks(value: str | list[ContentBlock] | None) -> list[ContentBlock]:
    """Normalize content into ACP-style content blocks."""
    if value is None:
        return []
    if isinstance(value, str):
        return [TextContentBlock(text=value)] if value else []
    return value


def content_text(value: str | list[ContentBlock] | None) -> str:
    """Flatten ACP content blocks into plain text.

    Image blocks have no text form; they are skipped here and surfaced as native
    multimodal parts by the completion-request projection.
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return value

    pieces: list[str] = []
    for block in value:
        match block:
            case TextContentBlock(text=text):
                pieces.append(text)
            case ThinkingContentBlock(thinking=thinking):
                pieces.append(thinking)
    return "".join(pieces)


class StateEntryPayload(BaseModel):
    """Payload for task-owned structured state.

    type is a task-defined discriminator for the opaque JSON content value.
    Parents and transports preserve it but do not interpret it.
    """

    type: str
    content: JsonValue


class StateEntry(BaseEntry):
    """Arbitrary task-owned structured state recorded in history."""

    type: Literal["state"] = "state"
    payload: StateEntryPayload


class TaskCallEntryPayload(BaseModel):
    """Payload for a task call (subtask invocation request).

    id is the public correlation key used for callback result matching,
    upstream buffering, and pending-result maps. It must be unique within
    a workflow instance. Completion adapters may encode provider-local
    identifiers inside this value, but that is not a protocol concern.
    """

    type: Literal["child_task"] = "child_task"
    id: str = ""
    name: str = ""
    input: JsonValue = None


class CallbackTaskCallEntryPayload(BaseModel):
    """Payload for a callback task call that must be answered by a parent/user."""

    type: Literal["callback"] = "callback"
    id: str = ""
    name: str = ""
    input: JsonValue = None


class CallbackHandlerTaskCallEntryPayload(BaseModel):
    """Payload for the child-side handler that routes a callback result."""

    type: Literal["callback_handler"] = "callback_handler"
    id: str = ""
    name: str = ""
    input: JsonValue = None
    callback_id: str = ""
    child_task_id: str = ""
    callback_path: list[str] = Field(default_factory=list)


TaskCallEntryPayloadVariant = Annotated[
    TaskCallEntryPayload | CallbackTaskCallEntryPayload | CallbackHandlerTaskCallEntryPayload,
    Field(discriminator="type"),
]


class TaskCallEntry(BaseEntry):
    """A subtask invocation request.

    Records that the LLM (or programmatic logic) requested a subtask
    to be executed. The id field correlates with TaskResultEntry.payload.id.
    """

    type: Literal["task_call"] = "task_call"
    payload: TaskCallEntryPayloadVariant = Field(default_factory=TaskCallEntryPayload)


class MessageEntryPayload(BaseModel):
    """Payload for a message entry."""

    role: Literal["system", "user", "assistant"] = "user"
    content: list[ContentBlock] = Field(default_factory=list)
    channel: Literal["thinking", "message"] | None = None

    @field_validator("content", mode="before")
    @classmethod
    def _normalize_content(cls, value: Any) -> Any:
        return content_blocks(value)

    @model_validator(mode="after")
    def _default_assistant_channel(self) -> "MessageEntryPayload":
        if self.role == "assistant" and self.channel is None:
            self.channel = "message"
        if self.role != "assistant":
            self.channel = None
        return self


class MessageEntry(BaseEntry):
    """A message in the conversation history.

    Replaces separate SystemMessage, UserMessage, and AssistantMessage
    types. The payload.role field distinguishes the three. The
    generation_status and payload.tool_calls fields are primarily
    relevant for assistant messages.
    """

    type: Literal["message"] = "message"
    payload: MessageEntryPayload = Field(default_factory=MessageEntryPayload)


class TaskResultEntryPayload(BaseModel):
    """Payload for a task result (subtask completion).

    id matches the corresponding TaskCallEntryPayload.id.
    """

    id: str = ""
    name: str = ""
    state: "TaskState | None" = None


class TaskResultEntry(BaseEntry):
    """The result of a subtask execution.

    Contains the child's full TaskState (embedded). The id field
    matches the corresponding TaskCallEntry.payload.id. The name
    field records the task name for debugging/logging.
    """

    type: Literal["task_result"] = "task_result"
    payload: TaskResultEntryPayload = Field(default_factory=TaskResultEntryPayload)


HistoryEntry = MessageEntry | StateEntry | TaskCallEntry | TaskResultEntry


# ---------------------------------------------------------------------------
# TaskState — the universal task state container
# ---------------------------------------------------------------------------


class TaskState(BaseModel):
    """The universal state container for any task.

    Every task — whether an LLM agent, a tool wrapper, a sandbox, or
    a programmatic orchestrator — uses this same shape.

    Fields:
        id: Unique identifier for this task instance.
        input: What the task was asked to do (arbitrary JSON).
        output: Discriminated union — running/completed/failed/canceled.
        history: Ordered list of HistoryEntry — the log of events.
    """

    id: str = ""
    input: Any = None
    output: TaskOutput = Field(default_factory=PendingOutput)
    history: list[HistoryEntry] = Field(default_factory=list)


# Resolve forward reference "TaskState" in TaskResultEntryPayload.state
TaskResultEntryPayload.model_rebuild()

__all__ = [
    "TaskState",
    "TaskOutput",
    "PendingOutput",
    "CompletedOutput",
    "FailedOutput",
    "CanceledOutput",
    "HistoryEntry",
    "BaseEntry",
    "GenerationStatus",
    "MessageEntry",
    "MessageEntryPayload",
    "StateEntry",
    "StateEntryPayload",
    "TaskCallEntry",
    "TaskCallEntryPayload",
    "CallbackTaskCallEntryPayload",
    "CallbackHandlerTaskCallEntryPayload",
    "TaskCallEntryPayloadVariant",
    "TaskResultEntry",
    "TaskResultEntryPayload",
    "ContentBlock",
    "TextContentBlock",
    "ThinkingContentBlock",
    "ImageContentBlock",
    "JsonValue",
    "content_blocks",
    "content_text",
]
