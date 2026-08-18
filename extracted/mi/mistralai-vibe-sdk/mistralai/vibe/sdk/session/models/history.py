"""Retained public history entries for one Session."""

from typing import Annotated, Literal, Self

from pydantic import Field, JsonValue, TypeAdapter, model_validator

from .base import JsonSchema, SessionModel
from .common import (
    AbsolutePath,
    GenerationStatus,
    HistoryEntryId,
    MessageRole,
    ProtocolError,
    ToolCallId,
    ToolKind,
    TurnId,
    UnixMs,
    Uri,
)
from .content import ContentBlock

type FileChangeStatus = Literal["proposed", "approved", "denied", "applied", "failed"]
type NoticeLevel = Literal["info", "warning"]
type CheckpointKind = Literal["compaction", "rollback", "resume", "custom"]


class HistoryImportMessage(SessionModel):
    type: Literal["message"] = "message"
    role: MessageRole
    content: list[ContentBlock] = Field(default_factory=list)


class HistoryImportReasoning(SessionModel):
    type: Literal["reasoning"] = "reasoning"
    text: str


class HistoryImportToolCall(SessionModel):
    type: Literal["tool_call"] = "tool_call"
    tool_call_id: ToolCallId
    tool_kind: ToolKind = "local"
    name: str
    arguments: JsonValue = None


class HistoryImportToolResult(SessionModel):
    type: Literal["tool_result"] = "tool_result"
    tool_call_id: ToolCallId
    name: str | None = None
    result: JsonValue = None
    error: ProtocolError | None = None
    annotations: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_result(self) -> Self:
        if self.error is not None and self.result is not None:
            raise ValueError("Imported tool results cannot contain both result and error")
        return self


class HistoryImportSnapshot(SessionModel):
    type: Literal["snapshot"] = "snapshot"
    task_name: str
    snapshot_type: str
    value: JsonValue = None


type HistoryImportEntry = Annotated[
    HistoryImportMessage
    | HistoryImportReasoning
    | HistoryImportToolCall
    | HistoryImportToolResult
    | HistoryImportSnapshot,
    Field(discriminator="type"),
]


class HistoryEntryBase(SessionModel):
    """Fields shared by every retained public history entry."""

    id: HistoryEntryId
    index: int = Field(ge=0)
    turn_id: TurnId | None = None
    generation_status: GenerationStatus
    created_at: UnixMs
    updated_at: UnixMs
    annotations: dict[str, JsonValue] = Field(default_factory=dict)


class MessageHistoryEntry(HistoryEntryBase):
    type: Literal["message"] = "message"
    role: MessageRole
    content: list[ContentBlock] = Field(default_factory=list)


class ReasoningHistoryEntry(HistoryEntryBase):
    type: Literal["reasoning"] = "reasoning"
    summary: list[str] = Field(default_factory=list)
    text: str = ""


class PlanItem(SessionModel):
    id: str
    text: str
    status: Literal["pending", "generating", "complete"]


class PlanHistoryEntry(HistoryEntryBase):
    type: Literal["plan"] = "plan"
    items: list[PlanItem] = Field(default_factory=list)
    text: str | None = None


class ToolCallHistoryEntry(HistoryEntryBase):
    type: Literal["tool_call"] = "tool_call"
    tool_call_id: ToolCallId
    tool_kind: ToolKind
    name: str
    arguments: JsonValue = None
    input_schema: JsonSchema | None = None
    output_schema: JsonSchema | None = None


class ToolResultHistoryEntry(HistoryEntryBase):
    type: Literal["tool_result"] = "tool_result"
    tool_call_id: ToolCallId
    name: str | None = None
    result: JsonValue = None
    error: ProtocolError | None = None
    duration_ms: int | None = Field(default=None, ge=0)


class FileChange(SessionModel):
    path: AbsolutePath
    kind: Literal["create", "modify", "delete", "rename"]
    old_path: AbsolutePath | None = None
    diff: str | None = None


class FileChangeHistoryEntry(HistoryEntryBase):
    type: Literal["file_change"] = "file_change"
    changes: list[FileChange] = Field(default_factory=list)
    status: FileChangeStatus


class ResourceHistoryEntry(HistoryEntryBase):
    type: Literal["resource"] = "resource"
    uri: Uri
    title: str | None = None
    media_type: str | None = None


class CheckpointHistoryEntry(HistoryEntryBase):
    type: Literal["checkpoint"] = "checkpoint"
    checkpoint_kind: CheckpointKind
    message: str | None = None
    details: JsonValue = None


class ErrorHistoryEntry(HistoryEntryBase):
    type: Literal["error"] = "error"
    error: ProtocolError


class NoticeHistoryEntry(HistoryEntryBase):
    type: Literal["notice"] = "notice"
    level: NoticeLevel
    message: str
    details: JsonValue = None


type HistoryEntry = Annotated[
    MessageHistoryEntry
    | ReasoningHistoryEntry
    | PlanHistoryEntry
    | ToolCallHistoryEntry
    | ToolResultHistoryEntry
    | FileChangeHistoryEntry
    | ResourceHistoryEntry
    | CheckpointHistoryEntry
    | ErrorHistoryEntry
    | NoticeHistoryEntry,
    Field(discriminator="type"),
]

HistoryEntryAdapter: TypeAdapter[HistoryEntry] = TypeAdapter(HistoryEntry)
