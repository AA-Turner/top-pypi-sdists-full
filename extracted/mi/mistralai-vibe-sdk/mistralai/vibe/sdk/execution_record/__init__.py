"""Execution Record domain exports for the Vibe SDK."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "BaseEntry",
    "CallbackHandlerTaskCallEntryPayload",
    "CallbackTaskCallEntryPayload",
    "CanceledOutput",
    "CompletedOutput",
    "ContentBlock",
    "FailedOutput",
    "GenerationStatus",
    "HistoryEntry",
    "JsonValue",
    "MessageEntry",
    "MessageEntryPayload",
    "PendingOutput",
    "StateEntry",
    "StateEntryPayload",
    "TaskCallEntry",
    "TaskCallEntryPayload",
    "TaskCallEntryPayloadVariant",
    "TaskOutput",
    "TaskResultEntry",
    "TaskResultEntryPayload",
    "TaskState",
    "TextContentBlock",
    "ThinkingContentBlock",
    "content_blocks",
    "content_text",
]

if TYPE_CHECKING:
    from mistralai.vibe.sdk.execution_record.state import (
        BaseEntry,
        CallbackHandlerTaskCallEntryPayload,
        CallbackTaskCallEntryPayload,
        CanceledOutput,
        CompletedOutput,
        ContentBlock,
        FailedOutput,
        GenerationStatus,
        HistoryEntry,
        JsonValue,
        MessageEntry,
        MessageEntryPayload,
        PendingOutput,
        StateEntry,
        StateEntryPayload,
        TaskCallEntry,
        TaskCallEntryPayload,
        TaskCallEntryPayloadVariant,
        TaskOutput,
        TaskResultEntry,
        TaskResultEntryPayload,
        TaskState,
        TextContentBlock,
        ThinkingContentBlock,
        content_blocks,
        content_text,
    )

_LAZY_EXPORTS = dict.fromkeys(__all__, "mistralai.vibe.sdk.execution_record.state")


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
