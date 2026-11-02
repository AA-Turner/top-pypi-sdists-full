"""Streaming event contract — identical across all Matrx services.

All services emit and consume this exact set of event types. Never add
service-specific event types here; extend via the typed registries in
phases.py, operations.py, data_types.py, and tool_event_data.py.
"""

from __future__ import annotations

import time
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from matrx_connect.context.data_types import DataPayload
from matrx_connect.context.operations import CompletionPayload, InitPayload
from matrx_connect.context.phases import PhasePayload

# ---------------------------------------------------------------------------
# Event type registry
# ---------------------------------------------------------------------------


class EventType(StrEnum):
    CHUNK = "chunk"
    REASONING_CHUNK = "reasoning_chunk"
    REASONING = "reasoning"
    PHASE = "phase"
    WARNING = "warning"
    INFO = "info"
    DATA = "data"
    INIT = "init"
    COMPLETION = "completion"
    ERROR = "error"
    TOOL_EVENT = "tool_event"
    HEARTBEAT = "heartbeat"
    END = "end"
    RENDER_BLOCK = "render_block"
    RECORD_RESERVED = "record_reserved"
    RECORD_UPDATE = "record_update"
    RESOURCE_CHANGED = "resource_changed"
    CONTEXT_ANALYSIS = "context_analysis"
    STRUCTURED_OUTPUT = "structured_output"
    CONTEXT_STATE = "context_state"
    CONTEXT_TRIMMED = "context_trimmed"
    INJECTION_CONSUMED = "injection_consumed"
    PROVIDER_RETRY = "provider_retry"
    CITATION = "citation"
    CONTROL_TOKEN = "control_token"


VALID_EVENT_TYPES: frozenset[str] = frozenset(e.value for e in EventType)


# ---------------------------------------------------------------------------
# Payload models — one per EventType, validated on emit
# ---------------------------------------------------------------------------


class ChunkPayload(BaseModel):
    model_config = {"extra": "forbid"}
    text: str


class ReasoningChunkPayload(BaseModel):
    model_config = {"extra": "forbid"}
    text: str


ReasoningState = Literal["started", "stopped"]


class ReasoningPayload(BaseModel):
    """Content-LESS reasoning lifecycle signal. Fires when a provider opens or
    closes a thinking/reasoning block, INDEPENDENT of whether reasoning text is
    streamed. Every provider signals a reasoning block start even when the
    reasoning text is suppressed (Anthropic display="omitted", OpenAI
    reasoning_summary="never", Gemini include_thoughts=False) — this event
    carries that signal so the UI can show a 'thinking' state during the long
    silent gap that would otherwise look like nothing but heartbeats. The
    reasoning TEXT, when requested, still flows on the `reasoning_chunk`
    channel; this event is purely the on/off lifecycle."""

    model_config = {"extra": "forbid"}
    state: ReasoningState


WarningLevel = Literal["low", "medium", "high"]


class WarningPayload(BaseModel):
    model_config = {"extra": "forbid"}
    code: str
    system_message: str
    user_message: str | None = None
    level: WarningLevel = "medium"
    recoverable: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class InfoPayload(BaseModel):
    model_config = {"extra": "forbid"}
    code: str
    system_message: str
    user_message: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


#: The last resort — used ONLY when the server said nothing at all.
GENERIC_ERROR_MESSAGE = "Sorry. An error occurred."


# 🚨 `user_message` never silently becomes a shrug. Every client prefers
# `user_message` over `message` (correctly — it is the field named "what the
# person reads"), so a blank one that defaulted to "Sorry. An error occurred."
# SHADOWS the honest sentence the server already wrote in `message`. That is
# exactly how a Masterwork upload told a person "Sorry. An error occurred."
# while the server was saying "…isn't a kind of file we can read yet. Paste the
# text instead." (2026-09-12). So: when nobody supplied a user-facing sentence,
# `message` IS the sentence. A blunt technical line is honest; a generic apology
# that hides the remedy is not. The apology survives only when the server said
# nothing at all.
class ErrorPayload(BaseModel):
    model_config = {"extra": "forbid"}
    error_type: str
    message: str
    user_message: str = GENERIC_ERROR_MESSAGE
    code: str | None = None
    details: dict[str, Any] | None = None

    @model_validator(mode="after")
    def _never_shrug(self) -> "ErrorPayload":
        if "user_message" not in self.model_fields_set or not self.user_message.strip():
            object.__setattr__(
                self,
                "user_message",
                self.message.strip() or GENERIC_ERROR_MESSAGE,
            )
        return self


ProviderRetryState = Literal["scheduled", "retrying_now", "cancelled", "suspended", "recovered"]


class ProviderRetryPayload(BaseModel):
    model_config = {"extra": "forbid"}
    state: ProviderRetryState
    provider: str
    error_type: str
    message: str
    user_message: str
    status_code: int | None = None
    model: str | None = None
    request_id: str | None = None
    conversation_id: str | None = None
    iteration: int
    failed_attempt: int = Field(
        description="1-based count of failed provider calls in this iteration."
    )
    next_attempt: int | None = Field(
        default=None, description="1-based provider call number that will run next."
    )
    max_retries: int
    retry_delay: float | None = Field(
        default=None, description="Seconds scheduled before the next retry."
    )
    retry_at: float | None = Field(
        default=None, description="Unix timestamp when the next retry is scheduled."
    )
    discard_partial_output: bool = Field(
        default=False,
        description=(
            "When true, the client must rewind text, reasoning, render blocks, "
            "and citations emitted by the failed provider attempt before "
            "rendering the next attempt."
        ),
    )
    schedule: list[float] = Field(default_factory=list)
    can_cancel: bool = True
    can_retry_now: bool = True
    actions: dict[str, str] = Field(default_factory=dict)


ToolEventType = Literal[
    "tool_started",
    "tool_progress",
    "tool_step",
    "tool_result_preview",
    "tool_completed",
    "tool_error",
    "tool_delegated",
]


class ToolEventPayload(BaseModel):
    model_config = {"extra": "forbid"}
    event: ToolEventType
    call_id: str
    tool_name: str
    timestamp: float = Field(default_factory=time.time)
    message: str | None = None
    show_spinner: bool = True
    data: dict[str, Any] = Field(default_factory=dict)


class HeartbeatPayload(BaseModel):
    model_config = {"extra": "forbid"}
    timestamp: float = Field(default_factory=time.time)
    # Monotonic per-stream tick counter. A consumer that sees seq jump
    # (3 -> 7) knows beats were lost in TRANSIT; a seq that resets to 1
    # mid-stream proves the heartbeat task DIED and was auto-restarted.
    # Added 2026-06-10 while diagnosing prod streams whose heartbeats stopped
    # after the first tick (client watchdogs then killed healthy streams).
    seq: int | None = None
    # Set when this tick fired later than 2x the configured interval —
    # direct evidence of event-loop starvation (sync work blocking the loop).
    late_by_seconds: float | None = None


# The terminal END event's `reason` vocabulary. A stream's LAST frame is the
# only thing a client can use to decide whether what it received is a result or
# a wreck, so the word must be true: "complete" is a promise that the work
# finished. `send_cancelled` already spends "cancelled"; ERROR is its sibling
# for a run that died — emitted by every `fatal_error` path so a crashed task
# can never terminate a stream with a success word (live defect, 2026-09-17:
# a task raised TypeError and the client still read `reason: complete`).
END_REASON_COMPLETE = "complete"
END_REASON_CANCELLED = "cancelled"
END_REASON_ERROR = "error"


class EndPayload(BaseModel):
    model_config = {"extra": "forbid"}
    reason: str = END_REASON_COMPLETE


class RenderBlockPayload(BaseModel):
    model_config = {"extra": "forbid", "populate_by_name": True}
    blockId: str = Field(description="Stable ID for this block, e.g. 'blk_0'")
    blockIndex: int = Field(description="Ordering position among all blocks in the message")
    type: str = Field(description="Block type key, e.g. 'text', 'timeline', 'quiz'")
    status: Literal["streaming", "complete", "error"] = Field(description="Block lifecycle status")
    content: str | None = Field(default=None, description="Raw text content (Text Channel blocks)")
    data: dict[str, Any] | None = Field(
        default=None, description="Parsed structured data (Block Channel blocks)"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Block metadata (language, isComplete, etc.)"
    )


class CitationPayload(BaseModel):
    """One citation attached to the streaming answer, live.

    Emitted the moment a provider delivers citation data mid-stream (Anthropic
    ``citations_delta``, OpenAI ``response.output_text.annotation.added``) or
    at stream settle for providers that only deliver it terminally (Gemini
    grounding metadata). ``citation`` is a ``NormalizedCitation`` dict — the
    canonical cross-provider shape owned by ``matrx_ai.config.citations``
    (matrx-connect cannot depend on matrx-ai, so the wire field is a dict; the
    generated TS still gets the full interface from TextPart.citations).
    ``block_index`` is the provider's content-block index the citation attaches
    to (Anthropic), or None when the provider doesn't scope citations to a
    block."""

    model_config = {"extra": "forbid"}
    block_index: int | None = None
    citation: dict[str, Any]


RecordStatus = Literal["pending", "active", "completed", "failed"]

CxMessageRole = Literal["user", "assistant", "system", "tool"]


class CxMessageReservedParentRefs(BaseModel):
    model_config = {"extra": "allow"}
    conversation_id: str
    user_request_id: str


class CxMessageReservedMetadata(BaseModel):
    model_config = {"extra": "allow"}
    role: CxMessageRole
    position: int


class CxRequestReservedParentRefs(BaseModel):
    model_config = {"extra": "allow"}
    conversation_id: str
    user_request_id: str


class CxRequestReservedMetadata(BaseModel):
    model_config = {"extra": "allow"}
    iteration: int


class CxToolCallReservedParentRefs(BaseModel):
    model_config = {"extra": "allow"}
    conversation_id: str
    user_request_id: str
    call_id: str


class CxToolCallReservedMetadata(BaseModel):
    model_config = {"extra": "allow"}
    tool_name: str
    call_id: str
    iteration: int


class RecordReservedPayload(BaseModel):
    model_config = {"extra": "forbid"}
    db_project: str
    table: str
    record_id: str
    status: Literal["pending"] = "pending"
    parent_refs: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = Field(
        default=None,
        description=(
            "ISO-8601 instant the row stores as its own created_at, when the server "
            "knows it (message rows). The client uses it as the row's time so a live "
            "turn and a reloaded turn draw the same durations."
        ),
    )


class CxMessageReservedPayload(RecordReservedPayload):
    table: Literal["message"]  # type: ignore[assignment]
    parent_refs: CxMessageReservedParentRefs  # type: ignore[assignment]
    metadata: CxMessageReservedMetadata  # type: ignore[assignment]


class CxRequestReservedPayload(RecordReservedPayload):
    table: Literal["request"]  # type: ignore[assignment]
    parent_refs: CxRequestReservedParentRefs  # type: ignore[assignment]
    metadata: CxRequestReservedMetadata  # type: ignore[assignment]


class CxToolCallReservedPayload(RecordReservedPayload):
    table: Literal["tool_call"]  # type: ignore[assignment]
    parent_refs: CxToolCallReservedParentRefs  # type: ignore[assignment]
    metadata: CxToolCallReservedMetadata  # type: ignore[assignment]


class RecordUpdatePayload(BaseModel):
    model_config = {"extra": "forbid"}
    db_project: str
    table: str
    record_id: str
    status: Literal["active", "completed", "failed"]
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = Field(
        default=None,
        description=(
            "ISO-8601 instant the row stores as its own created_at, when this update "
            "is the moment the server writes it (message rows going active)."
        ),
    )


# ---------------------------------------------------------------------------
# RESOURCE_CHANGED — generic "something the client may care about changed"
# ---------------------------------------------------------------------------
#
# Generic invalidation/refresh hint. Any server-side code that mutates a
# resource the client might be displaying or caching emits one of these so
# the client can decide whether to refetch, refresh, or ignore. Distinct
# from RECORD_UPDATE (which is matrx-orm-record-specific) and DATA (which
# carries actual payload, not change notifications).
#
# `kind` is namespaced and intentionally open-ended so any package can emit
# without modifying matrx-connect — register your own kinds in your code
# and document them per consumer. Examples currently in use or planned:
#
#   fs.file        — a file inside a sandbox / agent's workspace changed
#   fs.directory   — many files at/under this path changed (batch/coalesced)
#   cld_files      — an AI Dream cloud_files row changed (size, version, …)
#   sandbox.cwd    — agent's working directory shifted
#   cache.<key>    — explicit cache invalidation hint (kind keys are free-form)
#
# `resource_id` is the kind-local identifier (path / UUID / composite). For
# move/rename operations, set `resource_id` to the NEW location and add the
# previous identifier to `metadata.previous_id`.

ResourceAction = Literal[
    "created",
    "modified",
    "deleted",
    "moved",
    "renamed",
    # 'invalidated' is the "I changed something under this scope but I'm not
    # going to enumerate every individual mutation" hint. Use it for batch
    # operations (large `git checkout`, `mtx aidream reset`, etc.).
    "invalidated",
]


class ResourceChangedPayload(BaseModel):
    """Tell the client a server-side resource changed; client decides whether
    to refetch, refresh, or ignore.

    See the module docstring above the model for the full namespace
    convention. Don't reach for this when there's a more specific event
    (RECORD_UPDATE for matrx-orm rows, TOOL_EVENT for tool lifecycle); use
    it when no other event captures the "you may want to refetch X" intent.
    """

    model_config = {"extra": "forbid"}

    kind: str = Field(
        description=(
            "Namespaced category for the resource — e.g. 'fs.file', "
            "'fs.directory', 'cld_files', 'sandbox.cwd'. Free-form: define "
            "your own kinds in your code and document them where the client "
            "cares about them."
        ),
    )
    action: ResourceAction = Field(
        description=(
            "What kind of change occurred. 'invalidated' is the batch/"
            "coalesced hint for 'something under this scope changed but I'm "
            "not enumerating it'."
        ),
    )
    resource_id: str = Field(
        description=(
            "Kind-local identifier — a path for fs, a UUID for db rows, etc. "
            "On 'moved'/'renamed' set this to the NEW identifier; put the "
            "previous one in metadata.previous_id."
        ),
    )
    sandbox_id: str | None = Field(
        default=None,
        description="Set when the resource lives inside a specific sandbox.",
    )
    user_id: str | None = Field(
        default=None,
        description="Owning user when relevant — usually inferred from request context.",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Kind-specific extras. For fs.file: {size, checksum, mtime, "
            "previous_id?}. For cld_files: {version, mime_type}. Free-form "
            "per kind; clients ignore fields they don't recognize."
        ),
    )


# ---------------------------------------------------------------------------
# CONTEXT_ANALYSIS — wire-level snapshot of an outbound provider HTTP request
# ---------------------------------------------------------------------------
#
# Emitted only when ``AppContext.snapshot=True``. Captures the literal HTTP
# request bytes a provider SDK is about to put on the wire (URL + method +
# headers + parsed JSON body). The capture sits inside an ``httpx`` request
# event-hook so the payload is the *real* serialized request, not the
# pre-SDK Python config dict.
#
# This is a debug / agentic-context-management primitive: it exists so the
# operator can answer "what exactly did the model see on iteration N?" with
# zero ambiguity and no provider-specific reconstruction.
#
# Auth headers (``authorization``, ``x-api-key``, ``x-goog-api-key``,
# ``proxy-authorization``, ``anthropic-api-key``) are redacted by the
# emitter side before the event is built — never store secrets in events.


class ContextAnalysisPayload(BaseModel):
    """Wire-level snapshot of one outbound provider HTTP request.

    Fired from the httpx request event-hook in
    ``matrx_ai.providers.outbound_capture`` whenever
    ``AppContext.snapshot=True``. The body is the JSON-parsed request body
    when possible, or the raw decoded string when the body isn't JSON.
    """

    model_config = {"extra": "forbid"}

    provider: str = Field(description="Matrx-side provider key (openai, anthropic, google, ...).")
    model: str | None = Field(
        default=None,
        description="Matrx-side model name configured for this call, if known.",
    )
    iteration: int | None = Field(
        default=None,
        description="Executor iteration this call belongs to, if available.",
    )
    conversation_id: str | None = Field(
        default=None,
        description="AppContext.conversation_id at emit time.",
    )
    request_id: str | None = Field(
        default=None,
        description="AppContext.request_id at emit time.",
    )
    attempt: int = Field(
        default=1,
        description="SDK retry attempt counter (1 = first attempt).",
    )
    is_streaming: bool = Field(
        default=False,
        description="True when the SDK call was issued with stream=True.",
    )

    method: str = Field(description="HTTP method, e.g. POST.")
    url: str = Field(description="Full URL, including path and query string.")
    headers: dict[str, str] = Field(
        description="Request headers. Auth-bearing headers are redacted to '<redacted>'.",
    )
    body: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Parsed JSON body when the request body was JSON-decodable. "
            "None when there was no body or the body was non-JSON (in "
            "which case ``body_raw`` is set)."
        ),
    )
    body_raw: str | None = Field(
        default=None,
        description=(
            "UTF-8-decoded raw body text. Set only when the body could not "
            "be parsed as JSON; otherwise None."
        ),
    )
    body_size_bytes: int = Field(
        default=0,
        description="Original body byte length, before any parsing or redaction.",
    )

    timestamp: float = Field(
        default_factory=time.time,
        description="Wall-clock time the hook fired (Unix seconds).",
    )


# ---------------------------------------------------------------------------
# STRUCTURED_OUTPUT — agent's final assistant text parsed against its schema
# ---------------------------------------------------------------------------
#
# Emitted automatically by ``matrx_ai.agents.Agent.execute`` whenever the
# agent has an ``output_schema`` declared and the loop has just produced its
# final assistant message. Carries the schema AND the parsed payload so the
# client can render the structured result without re-running extraction or
# re-fetching the agent record.
#
# - Fires AFTER all token chunks have streamed (prose-first behavior preserved).
# - Fires whether extraction succeeded or failed — ``success=False`` is the
#   useful signal that "this agent was supposed to produce structured output
#   and the parser couldn't find it" so the FE can surface the gap instead of
#   silently dropping it.
# - Fires once per agent completion. Sub-agents emit their own events, tagged
#   with the matching ``operation_id`` so the FE can attribute them.


class StructuredOutputPayload(BaseModel):
    """Final structured payload extracted from an agent's text output.

    The schema is included verbatim so the FE can drive generic renderers
    (tables, forms, type-checked accessors) without an extra round-trip to
    fetch the agent record.
    """

    model_config = {"extra": "forbid"}

    schema_name: str | None = Field(
        default=None,
        description=(
            "Optional name from the agent's ``output_schema.name`` field. "
            "Used for human-readable identification in UIs and logs."
        ),
    )
    json_schema: dict[str, Any] = Field(
        description=(
            "The JSON Schema the agent declared (typically "
            "``agent.output_schema['schema']``). Full schema, not a hint — "
            "FE can use it for typed rendering and runtime validation."
        ),
    )
    data: dict[str, Any] | list[Any] | None = Field(
        default=None,
        description=(
            "Parsed payload after schema-aware normalization. "
            "``None`` when extraction failed — check ``success`` and ``reason``."
        ),
    )
    success: bool = Field(
        description=(
            "True when the parser produced a value matching the schema. "
            "False means the agent declared a schema but the response could "
            "not be parsed against it; ``data`` will be None."
        ),
    )
    reason: str = Field(
        default="",
        description="Human-readable failure reason; empty string on success.",
    )
    match_count: int = Field(
        default=0,
        description="Number of schema-matching JSON candidates found in the response.",
    )
    agent_name: str | None = Field(
        default=None,
        description="The agent's display name, when available — provenance.",
    )
    operation_id: str | None = Field(
        default=None,
        description=(
            "When emitted from a sub-agent, the ``operation_id`` of the "
            "init/completion pair so the FE can attribute the event."
        ),
    )
    kind: str | None = Field(
        default=None,
        description="Canonical content_ir.kind_definition slug for this output.",
    )
    kind_version: int | None = Field(
        default=None,
        description="Kind version used for the validation verdict.",
    )
    kind_checked: bool = Field(
        default=False,
        description="True when kind/schema validation actually ran; false is skipped, not pass.",
    )
    kind_errors: list[str] = Field(
        default_factory=list,
        description="Per-contract validation errors; empty only means pass when kind_checked is true.",
    )


# ---------------------------------------------------------------------------
# CONTEXT_STATE / CONTEXT_TRIMMED — Model Context insight (Phase 3)
# ---------------------------------------------------------------------------
#
# Emitted by ``matrx_ai.db.persistence.persist_completed_request`` after each
# completed turn. The FE consumes these into a ``context-state`` Redux slice
# that drives the Model Context tab in the Creator Panel and the header
# context gauge. CONTEXT_STATE is the canonical "what did the model just see"
# snapshot; CONTEXT_TRIMMED is the audit of any in-memory trim that ran,
# including the "eligible-but-skipped" case when the cache-aware gate fires.


class ContextStatePayload(BaseModel):
    """Snapshot of the model's context after the most recent persisted turn.

    Sent live via the response stream and also returned from the
    ``GET /conversations/{id}/context-state`` endpoint for initial FE
    hydration. Token figures come from the real provider ``usage`` block
    of the last iteration; character figures aggregate the message-row
    columns ``content_chars`` and ``tool_results_chars``.
    """

    model_config = {"extra": "forbid"}

    conversation_id: str
    last_request_input_tokens: int = Field(
        default=0,
        description="Non-cached input tokens reported by the provider on the last iteration.",
    )
    last_request_cached_tokens: int = Field(
        default=0,
        description="Cache-read tokens on the last iteration (Anthropic cache_read_input_tokens, OpenAI cached_tokens, Gemini cached_content_token_count).",
    )
    last_request_output_tokens: int = Field(default=0)
    total_chars_visible_to_model: int = Field(
        default=0,
        description="Sum of content_chars + tool_results_chars across messages where is_visible_to_model is true.",
    )
    message_count_visible: int = Field(default=0)
    cache_state: dict[str, Any] = Field(
        default_factory=dict,
        description="Verbatim cx_conversation.cache_state JSONB at the time of measurement.",
    )
    measured_at: str = Field(description="ISO timestamp of the measurement.")


class ContextTrimmedPayload(BaseModel):
    """Audit of a context_trim pass.

    Fires whenever ``trim_messages_context`` either rewrote at least one
    block OR was skipped because of the cache-aware gate. The FE shows
    this in the "What just happened" section of the Model Context tab.
    """

    model_config = {"extra": "forbid"}

    conversation_id: str
    request_id: str | None = Field(
        default=None,
        description="cx_request UUID that this trim audit lives on (when known).",
    )
    trim_summary: dict[str, Any] = Field(
        description="Verbatim cx_request.trim_summary — see TrimReport.to_dict() in matrx_ai.config.context_trim.",
    )
    measured_at: str


# ---------------------------------------------------------------------------
# Registry — maps EventType -> expected payload class
# ---------------------------------------------------------------------------


class ConsumedInjection(BaseModel):
    """One inbox item that was drained into a running conversation."""

    model_config = {"extra": "forbid"}

    injection_id: str
    kind: str
    text: str | None = Field(
        default=None,
        description="The injected message text, echoed so a client that didn't originate "
        "the queue (reopened panel, another device) can render the delivered bubble.",
    )
    is_visible_to_user: bool = Field(
        default=True,
        description="Whether this item should appear in the user's transcript.",
    )
    position: int | None = Field(
        default=None,
        description="0-based index of the injected message in the conversation (when it produced a message).",
    )
    message_id: str | None = Field(
        default=None,
        description="The cx_message id the item became, when resolvable (best-effort).",
    )


class InjectionConsumedPayload(BaseModel):
    """Tell the client that queued Turn-Boundary Inbox item(s) were drained into
    the running conversation at a natural turn boundary — so the FE can reflect
    'your queued message was delivered' without polling. Batched: one event per
    non-empty drain, carrying every item consumed in that drain."""

    model_config = {"extra": "forbid"}

    conversation_id: str
    items: list[ConsumedInjection]
    count: int


class ControlTokenPayload(BaseModel):
    """A DECLARED machine line a mandate asked the model to emit, taken out of
    the visible text at the streaming source and routed here instead.

    The line never reaches the person's screen (wall W9 tail, 2026-09-15:
    ``WRAP_RATING: 4`` was printed into someone's own interview). Consumers that
    genuinely need the value — a stage machine, a run recorder — read it from
    this event; nothing parses the visible text for it, ever. The registry of
    declared tokens lives in ``matrx_connect.emitters.control_tokens``.
    """

    model_config = {"extra": "forbid"}
    #: The declared token name, e.g. ``WRAP_RATING``.
    name: str
    #: The value as the model wrote it, whitespace-trimmed. Always a string:
    #: typing is the declaring consumer's job, not the wire's.
    value: str
    #: The mandate/contract that declares this token.
    declared_by: str | None = None


PAYLOAD_REGISTRY: dict[EventType, type[BaseModel]] = {
    EventType.CHUNK: ChunkPayload,
    EventType.REASONING_CHUNK: ReasoningChunkPayload,
    EventType.REASONING: ReasoningPayload,
    EventType.PHASE: PhasePayload,
    EventType.WARNING: WarningPayload,
    EventType.INFO: InfoPayload,
    EventType.DATA: DataPayload,
    EventType.INIT: InitPayload,
    EventType.COMPLETION: CompletionPayload,
    EventType.ERROR: ErrorPayload,
    EventType.TOOL_EVENT: ToolEventPayload,
    EventType.HEARTBEAT: HeartbeatPayload,
    EventType.END: EndPayload,
    EventType.RENDER_BLOCK: RenderBlockPayload,
    EventType.RECORD_RESERVED: RecordReservedPayload,
    EventType.RECORD_UPDATE: RecordUpdatePayload,
    EventType.RESOURCE_CHANGED: ResourceChangedPayload,
    EventType.CONTEXT_ANALYSIS: ContextAnalysisPayload,
    EventType.STRUCTURED_OUTPUT: StructuredOutputPayload,
    EventType.CONTEXT_STATE: ContextStatePayload,
    EventType.CONTEXT_TRIMMED: ContextTrimmedPayload,
    EventType.INJECTION_CONSUMED: InjectionConsumedPayload,
    EventType.PROVIDER_RETRY: ProviderRetryPayload,
    EventType.CITATION: CitationPayload,
    EventType.CONTROL_TOKEN: ControlTokenPayload,
}


# ---------------------------------------------------------------------------
# Compact wire format — high-frequency chunk events (90%+ of stream traffic)
# e = event type ("c" = chunk, "r" = reasoning_chunk), t = text content
# ---------------------------------------------------------------------------


class CompactChunkEvent(BaseModel):
    model_config = {"extra": "forbid"}
    e: Literal["c"]
    t: str


class CompactReasoningChunkEvent(BaseModel):
    model_config = {"extra": "forbid"}
    e: Literal["r"]
    t: str


# ---------------------------------------------------------------------------
# StreamEvent — the wire format
# ---------------------------------------------------------------------------


class StreamEvent(BaseModel):
    model_config = {"extra": "forbid"}
    event: EventType
    data: dict[str, Any]

    def to_jsonl(self) -> str:
        return self.model_dump_json() + "\n"


class InvalidEventError(Exception):
    pass


# ---------------------------------------------------------------------------
# Constructors — always prefer these over building StreamEvent directly
# ---------------------------------------------------------------------------


def build_event(event_type: EventType, payload: BaseModel) -> StreamEvent:
    expected_cls = PAYLOAD_REGISTRY.get(event_type)
    if expected_cls is None:
        raise InvalidEventError(
            f"[EMITTER ERROR] Unknown event type: '{event_type}'. "
            f"Valid types: {', '.join(VALID_EVENT_TYPES)}"
        )

    if not isinstance(payload, expected_cls):
        raise InvalidEventError(
            f"[EMITTER ERROR] Event '{event_type}' expects payload type "
            f"'{expected_cls.__name__}', got '{type(payload).__name__}'"
        )

    return StreamEvent(
        event=event_type,
        data=payload.model_dump(),
    )


def validate_event_dict(event_name: str, data: dict[str, Any]) -> StreamEvent:
    if event_name not in VALID_EVENT_TYPES:
        raise InvalidEventError(
            f"[EMITTER ERROR] Unsupported event type: '{event_name}'. "
            f"Valid types: {', '.join(sorted(VALID_EVENT_TYPES))}"
        )

    event_type = EventType(event_name)
    payload_cls = PAYLOAD_REGISTRY[event_type]

    try:
        payload_cls.model_validate(data)
    except Exception as e:
        raise InvalidEventError(
            f"[EMITTER ERROR] Invalid payload for event '{event_name}': {e}"
        ) from e

    return StreamEvent(event=event_type, data=data)
