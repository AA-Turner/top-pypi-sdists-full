"""Typed wire-event models the TUI receives from the runtime server.

This is a discriminated Pydantic union mirroring the subset of
:class:`dreadnode.agents.events.AgentEvent` subclasses the TUI actually
consumes, plus the two server-synthetic envelopes (``cancelled``,
``error``) and the hand-built ``userinputrequired`` shape. It is the
single entry point for the TUI's event pipeline — replaces the
defensive string-key digging that used to live in the now-deleted
``event_contract.normalize_event`` with a single
:class:`pydantic.TypeAdapter` parse at the SSE boundary.

Why a TUI-local union rather than importing the server's events:

1. ``dreadnode.agents.events`` imports :mod:`rigging.generator`,
   :mod:`dreadnode.generators.message`, :mod:`rich`,
   :mod:`dreadnode.core.metric` and a lot more. Pulling any of it
   into ``app/tui/`` would drag Generator/Message/MetricSeries into
   widget code.
2. The server's events carry many fields the TUI never reads
   (``MetricSeries``, ``Usage`` with input/output splits, full
   ``Message`` history, ``Generator`` objects). ``AgentEvent.as_dict()``
   already narrows to a wire envelope with a bespoke ``data`` dict per
   subclass via ``_get_data()``. This module mirrors exactly that wire
   envelope, nothing more.
3. The server emits **three** distinct wire shapes (not one):

   * Most events go through ``AgentEvent.as_dict()`` — envelope with
     ``{type, timestamp, agent_id, agent_name, status, data}`` and a
     subclass-specific ``data`` payload.
   * ``userinputrequired`` is hand-built in ``app.py:_human_prompt_handler``
     as ``{"type": "userinputrequired", "data": prompt.model_dump()}``
     where ``prompt`` is an :class:`HumanPrompt`. The ``data`` is a full
     ``HumanPrompt`` dump, *not* what ``UserInputRequired._get_data()``
     returns.
   * ``cancelled`` / ``error`` are synthetic dicts built in the server's
     turn-handling except blocks. ``cancelled`` uses the envelope shape
     but ``error`` puts the error string at the top level with no
     ``data`` field at all.

   The typed union models all three shapes explicitly so unknown fields
   become loud validation failures instead of silent defaults.

``extra="ignore"`` on every model lets unknown fields pass through
without failing — important because a newer server version may emit
extra fields the TUI doesn't know about yet. The common ``_Envelope``
base carries the metadata fields every typed event shares.
"""

import typing as t

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from dreadnode.app.api.models import HumanPrompt

# =============================================================================
# Common pieces
# =============================================================================


class _Envelope(BaseModel):
    """Metadata fields present on every ``AgentEvent.as_dict()`` envelope."""

    model_config = ConfigDict(extra="ignore")

    timestamp: str | None = None
    agent_id: str | None = None
    agent_name: str | None = None
    status: str | None = None


class WireToolCall(BaseModel):
    """Slim TUI view of a tool call.

    ``arguments`` is ``dict`` when the server could parse the LLM's JSON,
    ``str`` when it couldn't (we wrap the raw string downstream), or
    ``None`` for events that don't carry arguments (``toolend``,
    ``toolerror``, ``toolstep``).
    """

    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    name: str | None = None
    arguments: dict[str, t.Any] | str | None = None


class WireUsage(BaseModel):
    """Token usage snapshot carried on generation events."""

    model_config = ConfigDict(extra="ignore")

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    # Estimated USD cost for this generation. ``None`` when the model
    # rate is unavailable. Populated by the SDK runtime on per-step
    # events; the reducer accumulates it into the session-cumulative
    # cost displayed in the TUI footer.
    cost_usd: float | None = None


# =============================================================================
# AgentStart / AgentEnd / AgentError / AgentStalled
# =============================================================================


class _EmptyData(BaseModel):
    model_config = ConfigDict(extra="ignore")


class AgentStart(_Envelope):
    type: t.Literal["agentstart"]
    data: _EmptyData = Field(default_factory=_EmptyData)


class AgentEndData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    stop_reason: str | None = None
    error: str | None = None
    error_type: str | None = None
    status_code: int | None = None
    """Forward-compat: the server doesn't currently emit this inside
    agent events, but the TUI's error-handling path feeds it into
    :func:`enrich_error_body` when present. Left as an optional pickup
    so a future server version can attach HTTP status codes without a
    TUI change."""


class AgentEnd(_Envelope):
    type: t.Literal["agentend"]
    data: AgentEndData = Field(default_factory=AgentEndData)


class AgentErrorData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    error: str | None = None
    error_type: str | None = None
    status_code: int | None = None


class AgentError(_Envelope):
    type: t.Literal["agenterror"]
    data: AgentErrorData = Field(default_factory=AgentErrorData)


class AgentStalledData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    reason: str | None = None


class AgentStalled(_Envelope):
    type: t.Literal["agentstalled"]
    data: AgentStalledData = Field(default_factory=AgentStalledData)


# =============================================================================
# Heartbeat / Compaction / GenerationRetry
# =============================================================================


class HeartbeatData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    message: str | None = None


class Heartbeat(_Envelope):
    type: t.Literal["heartbeat"]
    data: HeartbeatData = Field(default_factory=HeartbeatData)


class CompactionData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    trigger: str | None = None
    compaction_status: str | None = None
    reason: str | None = None
    messages_before: int = 0
    messages_after: int = 0


class Compaction(_Envelope):
    type: t.Literal["compactionevent"]
    data: CompactionData = Field(default_factory=CompactionData)


class GenerationRetryData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    step: int | None = None
    attempt: int | None = None
    max_attempts: int | None = None
    wait_seconds: float | None = None
    error_type: str | None = None
    error_message: str | None = None


class GenerationRetry(_Envelope):
    type: t.Literal["generationretry"]
    data: GenerationRetryData = Field(default_factory=GenerationRetryData)


# =============================================================================
# Generation lifecycle
# =============================================================================


class GenerationStartData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    model: str | None = None
    step: int | None = None


class GenerationStart(_Envelope):
    type: t.Literal["generationstart"]
    data: GenerationStartData = Field(default_factory=GenerationStartData)


class GenerationStepData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    step: int | None = None
    content: str | None = None
    tool_calls: list[WireToolCall] = Field(default_factory=list)
    usage: WireUsage = Field(default_factory=WireUsage)
    stop_reason: str | None = None
    model: str | None = None
    failed: bool = False
    extra: dict[str, t.Any] = Field(default_factory=dict)


class GenerationStep(_Envelope):
    type: t.Literal["generationstep"]
    data: GenerationStepData = Field(default_factory=GenerationStepData)


class GenerationEndData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    step: int | None = None
    content: str | None = None
    tool_calls: list[WireToolCall] = Field(default_factory=list)
    usage: WireUsage = Field(default_factory=WireUsage)
    stop_reason: str | None = None
    model: str | None = None


class GenerationEnd(_Envelope):
    type: t.Literal["generationend"]
    data: GenerationEndData = Field(default_factory=GenerationEndData)


class GenerationContentData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    step: int | None = None
    content: str | None = None
    tool_calls: list[WireToolCall] = Field(default_factory=list)
    extra: dict[str, t.Any] = Field(default_factory=dict)


class GenerationContent(_Envelope):
    type: t.Literal["generationcontent"]
    data: GenerationContentData = Field(default_factory=GenerationContentData)


class GenerationErrorData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    model: str | None = None
    error: str | None = None
    error_type: str | None = None
    step: int | None = None
    status_code: int | None = None


class GenerationError(_Envelope):
    type: t.Literal["generationerror"]
    data: GenerationErrorData = Field(default_factory=GenerationErrorData)


# =============================================================================
# Tool lifecycle
# =============================================================================


class ToolStartData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    tool_call: WireToolCall = Field(default_factory=WireToolCall)


class ToolStart(_Envelope):
    type: t.Literal["toolstart"]
    data: ToolStartData = Field(default_factory=ToolStartData)


class ToolEndData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    tool_call: WireToolCall = Field(default_factory=WireToolCall)
    result: str | None = None
    output_file: str | None = None
    stop: bool = False
    # Set when the tool ran to completion but reported a failure (bash
    # non-zero exit, ``@tool(catch=True)`` swallowed exception, MCP
    # ``isError=true``). Renderers should treat this as an errored call;
    # uncaught exceptions still arrive as :class:`ToolError` instead.
    error: str | None = None
    error_type: str | None = None
    # Estimated USD cost contributed by this tool call (e.g. sub-agent
    # LLM spend). ``None`` for ordinary tools. The TUI accumulates this
    # into a separate sub-agent cost display, not the main session cost.
    cost_usd: float | None = None


class ToolEnd(_Envelope):
    type: t.Literal["toolend"]
    data: ToolEndData = Field(default_factory=ToolEndData)


class ToolErrorData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    tool_call: WireToolCall = Field(default_factory=WireToolCall)
    error: str | None = None
    error_type: str | None = None


class ToolError(_Envelope):
    type: t.Literal["toolerror"]
    data: ToolErrorData = Field(default_factory=ToolErrorData)


class ToolStepData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    tool_call: WireToolCall = Field(default_factory=WireToolCall)
    step: int | None = None
    stop: bool = False
    error: str | None = None


class ToolStep(_Envelope):
    type: t.Literal["toolstep"]
    data: ToolStepData = Field(default_factory=ToolStepData)


# =============================================================================
# Human input — server bypasses as_dict() and dumps HumanPrompt directly
# =============================================================================


class UserInputRequired(_Envelope):
    """``data`` is a full :class:`HumanPrompt` dump, not a ``_get_data()``
    payload — the server hand-builds this envelope in
    ``_human_prompt_handler``. Reusing the existing :class:`HumanPrompt`
    Pydantic model means we get every field it defines
    (``allow_free_text``, ``default_option``, ``severity``,
    ``source_tool_name``, ``source_tool_call_id``, ``details``) for free.
    """

    type: t.Literal["userinputrequired"]
    data: HumanPrompt


# =============================================================================
# Server-synthetic events
# =============================================================================


class CancelledData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    reason: str | None = None


class Cancelled(_Envelope):
    """Synthetic envelope emitted from the server's turn cancel path."""

    type: t.Literal["cancelled"]
    data: CancelledData = Field(default_factory=CancelledData)


class RuntimeErrorData(BaseModel):
    """Optional ``data`` payload for a ``RuntimeErrorEvent``.

    The server's raw error envelope omits ``data`` entirely — the error
    text lives at the top level — so this is mostly a compat path for
    transport-layer 401s. ``data.status_code`` triggers re-authentication
    when seen here, letting auth failures flowing through ``handle_event``
    surface as a defence.
    """

    model_config = ConfigDict(extra="ignore")
    error: str | None = None
    status: int | None = None
    status_code: int | None = None


class RuntimeErrorEvent(BaseModel):
    """Raw error envelope emitted from the server's turn except-block.

    Unlike every other event type this shape puts the error string at
    the top level instead of inside ``data`` — the server builds it as
    ``{"type": "error", "error": str(exc)}`` and publishes it to the raw
    turn stream before the ``turn.failed`` terminal envelope fires.
    """

    model_config = ConfigDict(extra="ignore")
    type: t.Literal["error"]
    error: str | None = None
    data: RuntimeErrorData = Field(default_factory=RuntimeErrorData)


# =============================================================================
# Discriminated union + parser
# =============================================================================


WireEvent = t.Annotated[
    t.Union[  # noqa: UP007 — pydantic TypeAdapter needs the Union form
        AgentStart,
        AgentEnd,
        AgentError,
        AgentStalled,
        Heartbeat,
        Compaction,
        GenerationRetry,
        GenerationStart,
        GenerationStep,
        GenerationEnd,
        GenerationContent,
        GenerationError,
        ToolStart,
        ToolEnd,
        ToolError,
        ToolStep,
        UserInputRequired,
        Cancelled,
        RuntimeErrorEvent,
    ],
    Field(discriminator="type"),
]


_ADAPTER: TypeAdapter[WireEvent] = TypeAdapter(WireEvent)

# Server-emitted event types the TUI knows about but deliberately drops.
# The server forwards every ``AgentEvent`` subclass from ``agent.stream()``
# to the wire (``server/app.py`` emit loop); the TUI whitelist above
# intentionally excludes these because no TUI state reacts to them.
# Listing them here avoids one WARNING per occurrence during normal runs.
_IGNORED_WIRE_TYPES: frozenset[str] = frozenset({"reactstep"})


def parse_wire_event(raw: dict[str, t.Any]) -> WireEvent | None:
    """Parse a wire envelope into the typed :data:`WireEvent` union.

    Lowercases the ``type`` discriminator before dispatching so callers
    can pass either the server's lowercased wire form (``toolstart``)
    or a PascalCase class name (``ToolStart``) — the old
    ``normalize_event`` accepted both and some tests rely on the
    case-insensitive path.

    Returns ``None`` for envelopes with unknown ``type`` values or
    structurally-invalid payloads — logs a warning either way. Callers
    should treat ``None`` as "drop this event" to match the behaviour
    the old ``normalize_event`` pipeline had when it saw an ``unknown``
    type. Types listed in :data:`_IGNORED_WIRE_TYPES` drop silently.
    """
    if not isinstance(raw, dict):
        logger.warning("wire event dropped | non-dict envelope")
        return None
    # Lowercase the discriminator without mutating the caller's dict.
    event_type = raw.get("type")
    if isinstance(event_type, str) and event_type != event_type.lower():
        raw = {**raw, "type": event_type.lower()}
        event_type = event_type.lower()
    if isinstance(event_type, str) and event_type in _IGNORED_WIRE_TYPES:
        return None
    try:
        return _ADAPTER.validate_python(raw)
    except ValidationError as exc:
        logger.warning(
            "wire event dropped | type={} | errors={}",
            raw.get("type"),
            [(".".join(str(p) for p in e["loc"]), e["msg"]) for e in exc.errors()[:3]],
        )
        return None
