"""Typed data models for each tool_event sub-type.

Each ToolEventType value has a corresponding data model. The TS generator
produces a discriminated union keyed on the `event` field.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, JsonValue


class ToolStartedData(BaseModel):
    model_config = {"extra": "forbid"}
    arguments: dict[str, Any] = Field(default_factory=dict)
    #: The human name a card shows for this call when the as-called name is opaque (a projected agent
    #: tool is ``custom_tool_N``; an Orchestra member reads "<role title> · <agent name>"). None = the
    #: client derives a label from the tool name as before.
    display_name: str | None = None


class ToolProgressData(BaseModel):
    model_config = {"extra": "forbid"}
    percent: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolStepData(BaseModel):
    model_config = {"extra": "forbid"}
    step: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolResultPreviewData(BaseModel):
    model_config = {"extra": "forbid"}
    preview: str


class ToolCompletedData(BaseModel):
    model_config = {"extra": "forbid"}
    # Tool results travel over JSON and may be any JSON value. In particular,
    # calculator/predicate tools legitimately return numbers or booleans and
    # collection tools may return a top-level list.
    # Per-tool typed output models (ToolOutput layer) are a planned addition.
    result: JsonValue = None
    # Lazy tool calls: when a non-pinned tool's result is over the inline cap the
    # frame carries a preview instead and `result_omitted` is true; the client reads
    # the full result from chat.tool_call.output by `tool_call_id` on click.
    result_omitted: bool = False
    result_preview: str | None = None
    output_chars: int | None = None
    tool_call_id: str | None = None


class ToolErrorData(BaseModel):
    model_config = {"extra": "forbid"}
    error_type: str
    detail: str | None = None


class ToolDelegatedData(BaseModel):
    model_config = {"extra": "forbid"}
    arguments: dict[str, Any] = Field(default_factory=dict)


TOOL_EVENT_DATA_REGISTRY: dict[str, type[BaseModel]] = {
    "tool_started": ToolStartedData,
    "tool_progress": ToolProgressData,
    "tool_step": ToolStepData,
    "tool_result_preview": ToolResultPreviewData,
    "tool_completed": ToolCompletedData,
    "tool_error": ToolErrorData,
    "tool_delegated": ToolDelegatedData,
}


# ---------------------------------------------------------------------------
# Typed ToolEvent models — narrow ToolEventPayload per event type
# Imported here lazily to avoid a circular import with events.py
# ---------------------------------------------------------------------------


def _make_tool_event_models() -> dict[str, type[BaseModel]]:
    """Build typed ToolEvent models on first call, avoiding circular imports."""
    from matrx_connect.context.events import ToolEventPayload  # noqa: PLC0415

    class ToolStartedToolEvent(ToolEventPayload):
        event: Literal["tool_started"]  # type: ignore[assignment]
        data: ToolStartedData  # type: ignore[assignment]

    class ToolProgressToolEvent(ToolEventPayload):
        event: Literal["tool_progress"]  # type: ignore[assignment]
        data: ToolProgressData  # type: ignore[assignment]

    class ToolStepToolEvent(ToolEventPayload):
        event: Literal["tool_step"]  # type: ignore[assignment]
        data: ToolStepData  # type: ignore[assignment]

    class ToolResultPreviewToolEvent(ToolEventPayload):
        event: Literal["tool_result_preview"]  # type: ignore[assignment]
        data: ToolResultPreviewData  # type: ignore[assignment]

    class ToolCompletedToolEvent(ToolEventPayload):
        event: Literal["tool_completed"]  # type: ignore[assignment]
        data: ToolCompletedData  # type: ignore[assignment]

    class ToolErrorToolEvent(ToolEventPayload):
        event: Literal["tool_error"]  # type: ignore[assignment]
        data: ToolErrorData  # type: ignore[assignment]

    class ToolDelegatedToolEvent(ToolEventPayload):
        event: Literal["tool_delegated"]  # type: ignore[assignment]
        data: ToolDelegatedData  # type: ignore[assignment]

    return {
        "tool_started":        ToolStartedToolEvent,
        "tool_progress":       ToolProgressToolEvent,
        "tool_step":           ToolStepToolEvent,
        "tool_result_preview": ToolResultPreviewToolEvent,
        "tool_completed":      ToolCompletedToolEvent,
        "tool_error":          ToolErrorToolEvent,
        "tool_delegated":      ToolDelegatedToolEvent,
    }


# Populated on first access by the TS generator — avoids circular import at module load.
TOOL_EVENT_REGISTRY: dict[str, type[BaseModel]] = {}
