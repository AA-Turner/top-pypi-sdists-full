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
    #: The tool's ``tool.definition.category`` ("internal" = the platform's own work, not the person's). A client
    #: that speaks in the owner's words reads it; None = the tool has no category (never guessed from the name).
    category: str | None = None
    #: True on the one event sent the moment the model finished writing THIS call's input, while it is
    #: still writing the rest of its reply: ``arguments`` is the whole input and the call has not been
    #: dispatched yet (its ``tool_delegated`` / executor ``tool_started`` follows when the reply ends).
    #: A page that applies an agent's edit shows it now and answers the call when it is dispatched.
    args_ready: bool = False


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
    #: Self-corrected slips: ``call_id``s of EARLIER failed calls in this turn that THIS successful call
    #: recovers (same tool, same ``action``, different arguments - decided by the server's turn ledger,
    #: ``matrx_ai.tools.turn_ledger.claim_superseded``). A client counts failures still standing as
    #: failed calls whose id no ``supersedes`` has named. Empty on every other completion.
    supersedes: list[str] = Field(default_factory=list)
    #: The held stream (RESUME-AND-RECOVERY 1a): this client-run call's result landed while the turn waited
    #: for it in its open stream, and the turn continues here. ``waited_ms`` is that wait.
    held: bool = False
    waited_ms: int | None = None


class ToolErrorData(BaseModel):
    model_config = {"extra": "forbid"}
    error_type: str
    detail: str | None = None
    #: The held stream: the client reported this failure while the turn waited in its open stream.
    held: bool = False
    waited_ms: int | None = None


class ToolDelegatedHold(BaseModel):
    """The server waits for this call's result IN THIS STREAM until ``until`` (RESUME-AND-RECOVERY 1a)."""

    model_config = {"extra": "forbid"}
    until: str
    #: Why the stream waits: a client-run tool (section 1a) or a person answering a parked ask (section 1b).
    reason: Literal["client_tool", "person"] = "client_tool"


class DelegatedHoldWaitingInfo(BaseModel):
    """``info`` code ``delegated_hold_waiting``: a call parked on a PERSON is waited for IN THIS STREAM until
    ``until`` (RESUME-AND-RECOVERY section 1b rule P4). The client keeps reading; the answer arrives as
    ``tool_completed`` / ``tool_error`` with ``data.held``, or ``delegated_hold_released`` ends the wait."""

    model_config = {"extra": "forbid"}
    call_id: str
    tool_name: str
    reason: Literal["person"] = "person"
    until: str
    action_request_id: str


class ToolDelegatedData(BaseModel):
    model_config = {"extra": "forbid"}
    arguments: dict[str, Any] = Field(default_factory=dict)
    #: The call's own deadline when its tool declares one (``max_client_wait_seconds``), ISO-8601.
    step_deadline_at: str | None = None
    execution_authorization: dict[str, Any] | None = None
    target_instance_id: str | None = None
    #: Present when the stream stays open for the result: the client posts it and keeps reading; absent
    #: means the stream ends and the turn continues by ``/resume``.
    hold: ToolDelegatedHold | None = None


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
