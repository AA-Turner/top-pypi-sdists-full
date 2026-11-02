"""Temporarily project legacy Vibe Agents events into Harness client read state.

Vibe Agents serves canonical catalog metadata alongside retained legacy execution
events. This module validates both, folds legacy history patches, and exposes
the resulting state through the shared Harness ``SessionClient``.
It is not a Session Runtime, a recovery model, or an event-authoring contract;
delete it when Vibe Agents serves the canonical Harness Session Protocol.

Reads are forward-compatible. A newer server may add fields, which are ignored, and
event types, history entry types and message roles, which parse to fallback models
and are logged and skipped. It may also serve canonical Session events, such as
``session_updated``, beside the legacy rows; those are skipped too. A known type with
a malformed body still raises ``RemoteProjectionError``: that is a producer bug, not
a newer producer.
"""

from datetime import datetime
from typing import Annotated, Literal, get_args
from uuid import NAMESPACE_URL, uuid5

import structlog
from pydantic import (
    AliasChoices,
    ConfigDict,
    Discriminator,
    Field,
    JsonValue,
    Tag,
    TypeAdapter,
    ValidationError,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe_agents._internal.wire_models import ForwardCompatibleModel
from mistralai.vibe_agents.sessions_client import AgentSessionResponse, AgentSessionStatus
from mistralai.vibe_agents.sessions_client.api_models import ObservedControllerEventResponse
from mistralai.vibe_agents.sessions_client.rendered_session import RenderedSession

from . import annotation_keys

_HISTORY_ID_NAMESPACE = uuid5(NAMESPACE_URL, "mistral-agents-sdk-vibe-agents-history")
_JSON_VALUE_ADAPTER: TypeAdapter[JsonValue] = TypeAdapter(JsonValue)
_CREATED_AT_ANNOTATION = "vibe_agents.created_at"
_TOOL_DISCOVERY_PROGRESS_TITLE = "Searched for relevant tools"
_LEGACY_EVENT_TYPES = frozenset({"history_update", "callback_call", "task_result"})
_LEGACY_HISTORY_ENTRY_TYPES = frozenset({"message", "task_call", "task_result", "state"})

logger = structlog.get_logger(__name__)


class _LegacyEventModel(ForwardCompatibleModel):
    model_config = ConfigDict(
        validate_by_alias=True,
        validate_by_name=True,
    )


class _LegacyTextContentBlock(_LegacyEventModel):
    type: Literal["text"]
    text: str = ""
    annotations: dict[str, JsonValue] | None = None


class _LegacyImageContentBlock(_LegacyEventModel):
    type: Literal["image"]
    uri: str = Field(validation_alias=AliasChoices("imageUrl", "image_url", "uri"))
    annotations: dict[str, JsonValue] | None = None


class _LegacyResourceLinkContentBlock(_LegacyEventModel):
    type: Literal["resource_link"]
    uri: str
    name: str | None = None
    media_type: str | None = Field(
        default=None,
        validation_alias=AliasChoices("mimeType", "mime_type"),
    )
    annotations: dict[str, JsonValue] | None = None


type _LegacyMessageContentBlock = Annotated[
    _LegacyTextContentBlock | _LegacyImageContentBlock | _LegacyResourceLinkContentBlock,
    Field(discriminator="type"),
]


class _LegacyHistoryEntryModel(_LegacyEventModel):
    id: str | None = None
    generation_status: Literal["generating", "complete"] = Field(
        default="complete",
        alias="generationStatus",
    )
    annotations: dict[str, JsonValue] | None = None


type _LegacyMessageRole = Literal["system", "user", "assistant"]


class _LegacyMessagePayload(_LegacyEventModel):
    role: _LegacyMessageRole
    content: list[_LegacyMessageContentBlock] = Field(default_factory=list)
    channel: Literal["thinking", "message"] | None = None
    meta: dict[str, JsonValue] | None = None


class _LegacyOpaqueMessagePayload(_LegacyEventModel):
    """A message whose role this client does not know. It is kept only to be skipped."""

    model_config = ConfigDict(extra="allow")

    role: str

    @property
    def kind(self) -> JsonValue:
        return (self.model_extra or {}).get("kind")


_LEGACY_MESSAGE_ROLES: frozenset[str] = frozenset(get_args(_LegacyMessageRole.__value__))


def _classify_legacy_message(value: object) -> str:
    role = value.get("role") if isinstance(value, dict) else getattr(value, "role", None)
    # A missing or non-string role is malformed, not unknown: the strict model rejects it.
    if isinstance(role, str) and role not in _LEGACY_MESSAGE_ROLES:
        return "unknown"
    return "known"


class _LegacyMessageHistoryEntry(_LegacyHistoryEntryModel):
    type: Literal["message"]
    payload: Annotated[
        Annotated[_LegacyMessagePayload, Tag("known")] | Annotated[_LegacyOpaqueMessagePayload, Tag("unknown")],
        Discriminator(_classify_legacy_message),
    ]


class _LegacyToolTaskCallPayload(_LegacyEventModel):
    type: Literal["child_task", "callback_handler"] | None = None
    id: str | None = None
    name: str | None = None
    input: JsonValue = None
    callback_id: str | None = Field(default=None, alias="callbackId")
    child_task_id: str | None = Field(default=None, alias="childTaskId")
    callback_path: list[str] = Field(default_factory=list, alias="callbackPath")


class _LegacyCallbackTaskCallPayload(_LegacyEventModel):
    type: Literal["callback"]
    id: str | None = None
    name: str | None = None
    input: JsonValue = None


type _LegacyTaskCallPayload = Annotated[
    _LegacyCallbackTaskCallPayload | _LegacyToolTaskCallPayload,
    Field(union_mode="left_to_right"),
]


class _LegacyTaskCallHistoryEntry(_LegacyHistoryEntryModel):
    type: Literal["task_call"]
    payload: _LegacyTaskCallPayload


class _LegacyTaskOutput(_LegacyEventModel):
    status: Literal["running", "failed", "completed", "canceled", "cancelled"] = "running"
    value: JsonValue = None
    error: str | None = None


class _LegacyTaskStatePayload(_LegacyEventModel):
    id: str | None = None
    input: JsonValue = None
    output: _LegacyTaskOutput = Field(default_factory=_LegacyTaskOutput)
    history: list[JsonValue] | None = None


class _LegacyTaskResultHistoryPayload(_LegacyEventModel):
    id: str | None = None
    name: str | None = None
    state: _LegacyTaskStatePayload


class _LegacyTaskResultHistoryEntry(_LegacyHistoryEntryModel):
    type: Literal["task_result"]
    payload: _LegacyTaskResultHistoryPayload


class _LegacySessionInitializedContent(_LegacyEventModel):
    application_id: str | None = Field(default=None, alias="applicationId")
    application_name: str | None = Field(default=None, alias="applicationName")
    agent_id: str | None = Field(default=None, alias="agentId")
    agent_name: str | None = Field(default=None, alias="agentName")
    source: str | None = None


class _LegacySessionInitializedPayload(_LegacyEventModel):
    type: Literal["x-vibe-agent-session-initialized"]
    content: _LegacySessionInitializedContent


class _LegacyTurnFailureError(_LegacyEventModel):
    code: str
    message: str
    retryable: bool = False


class _LegacyFailedTurnTermination(_LegacyEventModel):
    outcome: Literal["failed"]
    error: _LegacyTurnFailureError


def _failed_turn_termination_or_none(value: object, handler: ValidatorFunctionWrapHandler) -> object:
    try:
        return handler(value)
    except ValidationError:
        return None


class _LegacyWorkflowStatusContent(_LegacyEventModel):
    status: Literal["received", "running", "waiting_for_input", "snapshotting", "completed", "failed"]
    reason: str | None = None
    # Set on the waiting_for_input row that ends a failed turn. Completed, cancelled, or
    # malformed terminations read as absent, so the row still ends the turn.
    termination: Annotated[_LegacyFailedTurnTermination | None, WrapValidator(_failed_turn_termination_or_none)] = None


class _LegacyWorkflowStatusPayload(_LegacyEventModel):
    type: Literal["workflow_status"]
    content: _LegacyWorkflowStatusContent


# Rejection reasons that mean the command lost a race with the Session's Turn state: the Harness
# command rejection codes below, and `stale_turn`, which the worker writes for some of them.
_TURN_RACE_REJECTION_REASONS = frozenset(
    {
        "stale_turn",
        "stale_input",
        "out_of_order_input",
        "input_conflict",
        "invalid_state",
        "invalid_correlation",
        "invalid_command",
    }
)

# Rejection reasons that mean the Session's intake was full and it took nothing: the worker writes
# `intake_overloaded`, Harness answers `queue_full`. A resend with the same command id can still be
# accepted.
_OVERLOAD_REJECTION_REASONS = frozenset({"intake_overloaded", "queue_full"})


class _LegacyCommandOutcome(_LegacyEventModel):
    """The outcome that a legacy Session reports for one command, with the rejection reason."""

    command_id: str = Field(alias="commandId")
    outcome: Literal["accepted", "rejected"]
    turn_id: str | None = Field(default=None, alias="turnId")
    reason: str | None = None
    # Set on a rejection the sender may resend under the same command id.
    retryable: bool | None = None

    @property
    def overloaded(self) -> bool:
        """Whether the Session rejected the command because its intake was full."""

        return self.outcome == "rejected" and self.reason in _OVERLOAD_REJECTION_REASONS

    @property
    def non_race_rejection_reason(self) -> str | None:
        """The reason of a rejection that is not a Turn race, or ``None``.

        Such a rejection, for example a full intake or a reason newer than this SDK, is not a Turn
        conflict, and the caller gets the server's reason as it is. A rejection without a reason
        is a Turn conflict.
        """

        if self.outcome != "rejected" or self.reason is None or self.reason in _TURN_RACE_REJECTION_REASONS:
            return None
        return self.reason


class _LegacyCommandOutcomePayload(_LegacyEventModel):
    type: Literal["x-mistral-harness-command-outcome"]
    content: _LegacyCommandOutcome


class _LegacyCheckpointContent(_LegacyEventModel):
    checkpoint_kind: Literal["compaction", "rollback", "resume", "custom"] = Field(
        default="custom",
        alias="checkpointKind",
    )
    message: str | None = None
    details: JsonValue = None


class _LegacyCheckpointPayload(_LegacyEventModel):
    type: Literal["checkpoint"]
    content: _LegacyCheckpointContent = Field(default_factory=_LegacyCheckpointContent)


class _LegacyProgressContent(_LegacyEventModel):
    status: Literal["started", "progress", "success", "failure"]
    title: str
    content: str
    code: str | None = None


class _LegacyProgressPayload(_LegacyEventModel):
    type: Literal["progress"]
    content: _LegacyProgressContent


class _LegacyAlertContent(_LegacyEventModel):
    variant: Literal["info", "success", "warning", "error"]
    title: str
    body_md: str = Field(default="", alias="bodyMd")
    level: Literal["public", "private"] = "public"


class _LegacyAlertPayload(_LegacyEventModel):
    type: Literal["alert"]
    content: _LegacyAlertContent


class _LegacyOpaqueStatePayload(_LegacyEventModel):
    type: str
    content: JsonValue


type _LegacyStatePayload = Annotated[
    _LegacySessionInitializedPayload
    | _LegacyWorkflowStatusPayload
    | _LegacyCommandOutcomePayload
    | _LegacyCheckpointPayload
    | _LegacyProgressPayload
    | _LegacyAlertPayload
    | _LegacyOpaqueStatePayload,
    Field(union_mode="left_to_right"),
]


class _LegacyStateHistoryEntry(_LegacyHistoryEntryModel):
    type: Literal["state"]
    payload: _LegacyStatePayload


class _LegacyUnknownHistoryEntry(_LegacyHistoryEntryModel):
    """A history entry whose type this client does not know. It is kept only to be skipped."""

    type: str


def _classify_legacy_type(value: object, known: frozenset[str]) -> str | None:
    """Tag a legacy document by its ``type``: known, ``unknown`` for a newer one, or none.

    A missing or non-string type returns no tag, so validation fails: that is malformed.
    """
    value_type = value.get("type") if isinstance(value, dict) else getattr(value, "type", None)
    if value_type in known:
        return value_type
    return "unknown" if isinstance(value_type, str) else None


def _classify_legacy_entry(value: object) -> str | None:
    return _classify_legacy_type(value, _LEGACY_HISTORY_ENTRY_TYPES)


type _LegacyHistoryEntry = Annotated[
    Annotated[_LegacyMessageHistoryEntry, Tag("message")]
    | Annotated[_LegacyTaskCallHistoryEntry, Tag("task_call")]
    | Annotated[_LegacyTaskResultHistoryEntry, Tag("task_result")]
    | Annotated[_LegacyStateHistoryEntry, Tag("state")]
    | Annotated[_LegacyUnknownHistoryEntry, Tag("unknown")],
    Discriminator(_classify_legacy_entry),
]
_LEGACY_HISTORY_ENTRY_ADAPTER: TypeAdapter[_LegacyHistoryEntry] = TypeAdapter(_LegacyHistoryEntry)


class _LegacyHistoryValuePatch(_LegacyEventModel):
    op: Literal["add", "replace", "append"]
    path: str
    value: JsonValue


class _LegacyHistoryRemovePatch(_LegacyEventModel):
    op: Literal["remove"]
    path: str


type _LegacyHistoryPatch = Annotated[
    _LegacyHistoryValuePatch | _LegacyHistoryRemovePatch,
    Field(discriminator="op"),
]


class _LegacyHistoryUpdatePayload(_LegacyEventModel):
    task_id: str = Field(alias="taskId")
    patches: Annotated[list[_LegacyHistoryPatch], Field(min_length=1)]


class _LegacySessionEvent(_LegacyEventModel):
    session_id: str | None = Field(default=None, alias="sessionId")
    root_session_id: str | None = Field(default=None, alias="rootSessionId")


class _LegacyHistoryUpdateEvent(_LegacySessionEvent):
    type: Literal["history_update"]
    payload: _LegacyHistoryUpdatePayload
    annotations: dict[str, JsonValue] | None = None


class _LegacyCallbackCallPayload(_LegacyEventModel):
    id: str
    name: str
    input: JsonValue = Field(default_factory=dict)
    path: list[str] = Field(default_factory=list)
    tool_call_id: str | None = Field(default=None, alias="toolCallId")
    tool_id: str | None = Field(default=None, alias="toolId")


class _LegacyCallbackCallEvent(_LegacySessionEvent):
    type: Literal["callback_call"]
    payload: _LegacyCallbackCallPayload
    annotations: dict[str, JsonValue] | None = None


class _LegacyTerminalOutput(_LegacyEventModel):
    status: Literal["completed", "failed", "canceled", "cancelled"]
    value: JsonValue = None
    error: str | None = None
    reason: str | None = None
    # The Session limit that stopped the Session, when one did.
    cause: str | None = None


class _LegacyTaskState(_LegacyEventModel):
    id: str
    input: JsonValue = None
    output: _LegacyTerminalOutput
    history: list[JsonValue] | None = None


class _LegacyTaskResultPayload(_LegacyEventModel):
    task_id: str = Field(alias="taskId")
    result: _LegacyTaskState


class _LegacyTaskResultEvent(_LegacySessionEvent):
    type: Literal["task_result"]
    payload: _LegacyTaskResultPayload
    annotations: dict[str, JsonValue] | None = None


class _LegacyUnknownEvent(_LegacyEventModel):
    """A legacy event whose type this client does not know. It is kept only to be skipped."""

    type: str
    annotations: dict[str, JsonValue] | None = None


def _classify_legacy_event(value: object) -> str | None:
    # A canonical Session event has no top-level ``type``; its payload carries one.
    if isinstance(value, dict) and "type" not in value:
        return "canonical"
    return _classify_legacy_type(value, _LEGACY_EVENT_TYPES)


type _LegacyVibeAgentsEvent = Annotated[
    Annotated[_LegacyHistoryUpdateEvent, Tag("history_update")]
    | Annotated[_LegacyCallbackCallEvent, Tag("callback_call")]
    | Annotated[_LegacyTaskResultEvent, Tag("task_result")]
    | Annotated[_LegacyUnknownEvent, Tag("unknown")]
    | Annotated[harness_session.ClientEvent, Tag("canonical")],
    Discriminator(_classify_legacy_event),
]
_PRODUCT_EVENT_ADAPTER: TypeAdapter[_LegacyVibeAgentsEvent] = TypeAdapter(_LegacyVibeAgentsEvent)


class RemoteProjectionError(RuntimeError):
    """Raised when a product event cannot honestly satisfy Harness models."""


class VibeAgentsSessionProjection:
    """Build temporary Harness client read state from validated legacy events.

    The projection is caller-side migration code for the remote Agents SDK
    transport. It must not decide Session command legality, execute an Agent,
    or become a durable state format.
    """

    def __init__(self, product_session: AgentSessionResponse) -> None:
        self.product_session = product_session
        self.rendered = RenderedSession()
        self.history: list[harness_session.HistoryEntry] = []
        self.turns: dict[str, harness_session.TurnState] = {}
        self.active_turn_id: str | None = None
        self.active_callbacks: dict[str, harness_session.SessionCallback] = {}
        self.resolved_callback_ids: set[str] = set()
        self.command_outcomes: dict[str, _LegacyCommandOutcome] = {}
        self.initialized = False
        self.workflow_running_observed = False
        self.started_turn_ids: set[str] = set()
        self.product_cursor: str | None = None
        self._seen_sequences: set[str] = set()
        self._entry_ids: dict[int, str] = {}
        self._entry_turn_ids: dict[int, str | None] = {}
        self._entry_created_at: dict[int, int] = {}
        self._terminal_event: dict[str, object] | None = None
        self._pending_events: list[harness_session.SessionEvent] = []
        self._product_session_snapshot = build_session_from_product(product_session)
        self.session = self._product_session_snapshot
        if self.session.status == "terminated":
            self.session = self.session.model_copy(update={"status": "running", "termination": None})

    def has_seen(self, sequence: str) -> bool:
        """Whether ``apply`` already took the frame at ``sequence``."""

        return sequence in self._seen_sequences

    def apply(
        self,
        observed: ObservedControllerEventResponse,
    ) -> harness_session.SessionEvent | None:
        """Apply one product frame and return at most one canonical mutation."""

        if observed.sequence in self._seen_sequences:
            self.product_cursor = observed.sequence
            return None
        self._seen_sequences.add(observed.sequence)
        self.product_cursor = observed.sequence
        event = _parse_product_event(observed.event)
        if isinstance(event, harness_session.ClientEvent):
            return self._apply_canonical_event(event)
        if isinstance(event, _LegacyUnknownEvent):
            logger.debug("Skipping unknown Vibe Agents event type", event_type=event.type)
            return None
        if (
            event.session_id is not None
            and event.session_id != self.session.id
            or event.root_session_id is not None
            and event.root_session_id != self.session.root_session_id
        ):
            raise RemoteProjectionError("Legacy event belongs to a different Session or Session Tree")
        emitted_at = _event_time_ms(event, fallback=self.session.updated_at)

        if isinstance(event, _LegacyHistoryUpdateEvent):
            return self._apply_history_update(event, emitted_at=emitted_at)
        if isinstance(event, _LegacyCallbackCallEvent):
            return self._apply_callback_opened(event)
        return self._apply_session_terminal(event, emitted_at=emitted_at)

    def _apply_canonical_event(self, event: harness_session.ClientEvent) -> harness_session.SessionEvent | None:
        if event.session_id != self.session.id or event.root_session_id != self.session.root_session_id:
            raise RemoteProjectionError("Canonical event belongs to a different Session or Session Tree")
        if isinstance(event.payload, harness_session.UnknownEventPayload):
            logger.debug("Skipping unknown canonical event payload", payload_type=event.payload.original_type)
            return None
        if isinstance(event.payload, harness_session.CallbackOpenedEvent):
            callback = event.payload.callback
            if self.active_turn_id is not None and callback.turn_id != self.active_turn_id:
                raise RemoteProjectionError("Canonical callback does not belong to the active Turn")
            return self._retain_callback(callback)
        if isinstance(event.payload, harness_session.CallbackResolvedEvent):
            return self._resolve_callback(event.payload.callback_id, outcome=event.payload.outcome)
        return self._apply_catalog_event(event)

    def _apply_catalog_event(self, event: harness_session.ClientEvent) -> harness_session.SessionUpdatedEvent:
        if not isinstance(event.payload, harness_session.SessionUpdatedEvent):
            raise RemoteProjectionError("Only catalog session_updated events may accompany legacy history")
        summary = event.payload.session
        if (
            event.session_id != self.session.id
            or event.root_session_id != self.session.root_session_id
            or summary.id != self.session.id
            or summary.root_session_id != self.session.root_session_id
            or summary.parent_session_id != self.session.parent_session_id
        ):
            raise RemoteProjectionError("Catalog event belongs to a different Session or Session Tree")
        # Catalog writes do not change execution. A lagging status projection in
        # the metadata record must not rewind the Turn state built from history.
        metadata = {
            "title": summary.title,
            "archived_at": summary.archived_at,
            "updated_at": max(summary.updated_at, self.session.updated_at),
        }
        self.session = self.session.model_copy(update=metadata)
        self._product_session_snapshot = self._product_session_snapshot.model_copy(update=metadata)
        return harness_session.SessionUpdatedEvent(session=self.session)

    def state(self) -> harness_session.SessionState:
        return harness_session.SessionState(
            session=self.session,
            active_turn_id=self.active_turn_id,
            history=harness_session.Page(items=list(self.history)),
            turns=harness_session.Page(items=list(self.turns.values())),
            active_callbacks=list(self.active_callbacks.values()),
        )

    def take_pending_events(self) -> list[harness_session.SessionEvent]:
        pending, self._pending_events = self._pending_events, []
        return pending

    def reconcile_product_snapshot(self) -> None:
        if self._product_session_snapshot.status != "terminated" or self.session.status == "terminated":
            return
        self.session = self._product_session_snapshot
        # Execution closure proves Session loss, not the outcome of an unobserved Turn.
        self.active_turn_id = None
        self.active_callbacks.clear()

    def _apply_history_update(
        self,
        event: _LegacyHistoryUpdateEvent,
        *,
        emitted_at: int,
    ) -> harness_session.SessionEvent | None:
        patches = event.payload.patches
        root_indices = {_root_history_index(patch) for patch in patches}
        if None in root_indices or len(root_indices) != 1:
            raise RemoteProjectionError("One history_update must target exactly one root entry")
        root_index = root_indices.pop()
        if root_index is None:
            raise RemoteProjectionError("History update root index is missing")

        before_count = len(self.rendered.entries)
        repeated_root_value = _repeated_root_add_value(
            patches,
            root_index=root_index,
            rendered_entries=self.rendered.entries,
        )
        if repeated_root_value is not None:
            if repeated_root_value != self.rendered.entries[root_index]:
                raise RemoteProjectionError(f"History entry {root_index} was redelivered with different data")
            return None
        self.rendered.apply_public_session_event(event.model_dump(mode="json", by_alias=True, exclude_none=True))
        if self.rendered.invalid_patch_count:
            raise RemoteProjectionError("Vibe Agents emitted an invalid history patch")
        if root_index >= len(self.rendered.entries):
            raise RemoteProjectionError(f"History patch targets missing root entry {root_index}")
        if len(self.rendered.entries) > before_count and root_index != before_count:
            raise RemoteProjectionError("Root history additions must be append-only")

        raw_entry = self.rendered.entries[root_index]
        entry = _parse_legacy_history_entry(raw_entry, source_index=root_index)
        if isinstance(entry, _LegacyUnknownHistoryEntry):
            logger.debug("Skipping unknown legacy history entry", entry_type=entry.type, source_index=root_index)
            return None
        if isinstance(entry, _LegacyStateHistoryEntry):
            if isinstance(entry.payload, _LegacyOpaqueStatePayload):
                return None

            if isinstance(entry.payload, _LegacyProgressPayload) and (
                entry.generation_status != "complete"
                or entry.payload.content.status != "success"
                or entry.payload.content.title != _TOOL_DISCOVERY_PROGRESS_TITLE
                or entry.payload.content.content
                or entry.payload.content.code is not None
            ):
                return None

            if isinstance(
                entry.payload,
                (_LegacySessionInitializedPayload, _LegacyWorkflowStatusPayload, _LegacyCommandOutcomePayload),
            ):
                return self._apply_state_entry(entry.payload, emitted_at=emitted_at)

        callback_result = _callback_result(entry)
        if callback_result is not None:
            callback_id, callback_output = callback_result
            return self._resolve_callback(callback_id, outcome=_callback_outcome(callback_output))

        canonical = self._convert_history_entry(
            root_index,
            entry,
            emitted_at=emitted_at,
        )
        if canonical is None:
            return None
        existing_index = next(
            (index for index, candidate in enumerate(self.history) if candidate.id == canonical.id),
            None,
        )
        if existing_index is None:
            self.history.append(canonical)
            self._record_turn_history(canonical)
            self._record_command_outcome(canonical)
            return harness_session.HistoryEntryAddedEvent(entry=canonical)
        previous = self.history[existing_index]
        if previous == canonical:
            return None
        self.history[existing_index] = canonical
        self._record_turn_history(canonical)
        self._record_command_outcome(canonical)
        if previous.generation_status == "generating" and canonical.generation_status == "complete":
            return harness_session.HistoryEntryCompletedEvent(entry=canonical)
        return harness_session.HistoryEntryPatchedEvent(
            entry_id=canonical.id,
            entry_index=canonical.index,
            patches=[
                harness_session.JsonPatchReplaceOperation(
                    path="",
                    value=canonical.model_dump(mode="json", by_alias=True),
                )
            ],
        )

    def _apply_state_entry(
        self,
        payload: _LegacySessionInitializedPayload | _LegacyWorkflowStatusPayload | _LegacyCommandOutcomePayload,
        *,
        emitted_at: int,
    ) -> harness_session.SessionEvent | None:
        if isinstance(payload, _LegacySessionInitializedPayload):
            self.initialized = True
            return None
        if isinstance(payload, _LegacyCommandOutcomePayload):
            command_id = payload.content.command_id
            if not command_id:
                raise RemoteProjectionError("Harness command outcome has no commandId")
            previous = self.command_outcomes.get(command_id)
            # A command that a full intake rejected can be sent again and accepted under the same id.
            if previous is not None and previous.outcome != payload.content.outcome and not previous.overloaded:
                raise RemoteProjectionError(f"Harness command {command_id!r} has contradictory outcomes")
            self.command_outcomes[command_id] = payload.content
            return None
        content = payload.content
        status = content.status
        if status == "running":
            self.workflow_running_observed = True
            if self.session.status == "terminated":
                raise RemoteProjectionError("A terminated Session cannot return to running")
            self.session = self.session.model_copy(update={"status": "running", "updated_at": emitted_at})
            if self.active_turn_id is None:
                return harness_session.SessionUpdatedEvent(session=self.session)
            turn = self.turns[self.active_turn_id].model_copy(update={"status": "running"})
            self.turns[turn.id] = turn
            if turn.id in self.started_turn_ids:
                return None
            self.started_turn_ids.add(turn.id)
            return harness_session.TurnStartedEvent(turn=turn)
        if status == "waiting_for_input":
            self.workflow_running_observed = False
            if self.session.status == "terminated":
                raise RemoteProjectionError("A terminated Session cannot return to waiting")
            was_waiting = self.session.status == "waiting"
            self.session = self.session.model_copy(update={"status": "waiting", "updated_at": emitted_at})
            if self.active_turn_id is None:
                return None if was_waiting else harness_session.SessionUpdatedEvent(session=self.session)
            termination: harness_session.Termination
            if content.termination is not None:
                termination = harness_session.FailedTermination(
                    error=harness_session.ProtocolError(
                        code=content.termination.error.code,
                        message=content.termination.error.message,
                        retryable=content.termination.error.retryable,
                        details={"retryable": content.termination.error.retryable},
                    )
                )
            elif content.reason == "turn_interrupted":
                termination = harness_session.CancelledTermination(
                    reason="Remote Turn was interrupted",
                )
            elif content.reason == "iteration_limit":
                termination = harness_session.CompletedTermination(stop_reason="iteration_limit")
            elif content.reason == "skipped":
                termination = harness_session.CompletedTermination(stop_reason="skipped")
            else:
                termination = harness_session.CompletedTermination()
            turn = self.turns[self.active_turn_id].model_copy(
                update={
                    "status": "terminated",
                    "completed_at": emitted_at,
                    "termination": termination,
                }
            )
            self.turns[turn.id] = turn
            self.active_turn_id = None
            return harness_session.TurnTerminatedEvent(turn=turn)
        if status in {"received", "completed", "failed"}:
            return None
        raise AssertionError(f"Unhandled legacy workflow status: {status!r}")

    def _apply_callback_opened(
        self,
        event: _LegacyCallbackCallEvent,
    ) -> harness_session.CallbackOpenedEvent | None:
        callback = event.payload
        callback_input = callback.input
        prompt = ""
        if isinstance(callback_input, dict):
            raw_prompt = callback_input.get("prompt") or callback_input.get("question")
            if isinstance(raw_prompt, str):
                prompt = raw_prompt
        public = harness_session.ApprovalCallback(
            id=str(callback.id),
            turn_id=self.active_turn_id,
            tool_call_id=callback.tool_call_id or str(callback.id),
            tool_id=callback.tool_id,
            name=callback.name if callback.tool_id is not None else None,
            title=callback.name,
            description=prompt,
            input=callback_input,
        )
        return self._retain_callback(public)

    def _retain_callback(self, public: harness_session.SessionCallback) -> harness_session.CallbackOpenedEvent | None:
        existing = self.active_callbacks.get(public.id)
        if existing is not None:
            if existing != public:
                raise RemoteProjectionError(f"Callback {public.id!r} was reopened with different data")
            return None
        if public.id in self.resolved_callback_ids:
            raise RemoteProjectionError(f"Resolved callback {public.id!r} was reopened")
        self.active_callbacks[public.id] = public
        return harness_session.CallbackOpenedEvent(callback=public)

    def _resolve_callback(
        self,
        callback_id: str,
        *,
        outcome: harness_session.CallbackOutcome | None,
    ) -> harness_session.CallbackResolvedEvent | None:
        if callback_id in self.resolved_callback_ids:
            return None
        if self.active_callbacks.pop(callback_id, None) is None:
            raise RemoteProjectionError(f"Callback result {callback_id!r} has no preceding callback_call")
        self.resolved_callback_ids.add(callback_id)
        return harness_session.CallbackResolvedEvent(callback_id=callback_id, outcome=outcome)

    def _apply_session_terminal(
        self,
        event: _LegacyTaskResultEvent,
        *,
        emitted_at: int,
    ) -> harness_session.SessionTerminatedEvent | None:
        output = event.payload.result.output
        if self._terminal_event is not None:
            serialized_output = output.model_dump(mode="json", exclude_none=True)
            if self._terminal_event == serialized_output:
                return None
            raise RemoteProjectionError("Vibe Agents emitted contradictory terminal results")
        self._terminal_event = output.model_dump(mode="json", exclude_none=True)
        status = output.status
        if status == "failed":
            termination: harness_session.Termination = harness_session.FailedTermination(
                error=harness_session.ProtocolError(
                    code="remote_session_failed",
                    message=output.error or "Remote Session failed",
                )
            )
        elif status in {"canceled", "cancelled"}:
            termination = harness_session.CancelledTermination(
                reason=output.reason or "Remote Session was cancelled", cause=output.cause
            )
        else:
            termination = harness_session.CompletedTermination(output=output.value)
        self.session = self.session.model_copy(
            update={
                "status": "terminated",
                "termination": termination,
                "updated_at": emitted_at,
            }
        )
        self.active_turn_id = None
        self.active_callbacks.clear()
        return harness_session.SessionTerminatedEvent(session=self.session)

    def _convert_history_entry(
        self,
        source_index: int,
        entry: _LegacyHistoryEntry,
        *,
        emitted_at: int,
    ) -> harness_session.HistoryEntry | None:
        annotations = entry.annotations or {}
        entry_id = self._entry_ids.setdefault(
            source_index,
            _entry_id(self.session.id, source_index, entry),
        )
        turn_id = self._entry_turn_ids.get(source_index)
        if source_index not in self._entry_turn_ids:
            turn_id = _annotation_text(
                annotations,
                annotation_keys.HARNESS_TURN_ID_ANNOTATION,
            )
            if (
                turn_id is None
                and isinstance(entry, _LegacyMessageHistoryEntry)
                and isinstance(entry.payload, _LegacyMessagePayload)
                and entry.payload.role == "user"
            ):
                turn_id = entry_id
            if turn_id is None:
                turn_id = self.active_turn_id
            self._entry_turn_ids[source_index] = turn_id
        canonical_index = next(
            (candidate.index for candidate in self.history if candidate.id == entry_id),
            len(self.history),
        )
        created_at = self._entry_created_at.setdefault(source_index, emitted_at)
        generation_status = entry.generation_status
        base = {
            "id": entry_id,
            "index": canonical_index,
            "turn_id": turn_id,
            "generation_status": generation_status,
            "created_at": created_at,
            "updated_at": emitted_at,
            "annotations": annotations,
        }
        if isinstance(entry, _LegacyMessageHistoryEntry):
            message_payload = entry.payload
            if isinstance(message_payload, _LegacyOpaqueMessagePayload):
                logger.debug(
                    "Skipping legacy message with unknown role",
                    role=message_payload.role,
                    kind=message_payload.kind,
                    source_index=source_index,
                )
                return None
            content = _content_blocks(message_payload.content)
            if message_payload.channel == "thinking":
                return harness_session.ReasoningHistoryEntry(
                    **base,
                    text="\n\n".join(
                        block.text for block in content if isinstance(block, harness_session.TextContentBlock)
                    ),
                )
            return harness_session.MessageHistoryEntry(
                **base,
                role=message_payload.role,
                content=content,
            )

        if isinstance(entry, _LegacyTaskCallHistoryEntry):
            task_call_payload = entry.payload
            if isinstance(task_call_payload, _LegacyCallbackTaskCallPayload):
                return None
            tool_call_id = task_call_payload.id or entry_id
            tool_kind = _annotation_text(
                annotations,
                annotation_keys.HARNESS_TOOL_KIND_ANNOTATION,
            )
            if tool_kind is None:
                tool_kind = "plugin"
            elif tool_kind not in {"builtin", "local", "mcp", "client", "plugin", "connector"}:
                # A newer producer's tool kind: the call is still a tool call, so it is kept
                # under the kind that promises the least about where the tool runs.
                logger.debug("Reading unknown Harness tool kind as plugin", tool_kind=tool_kind)
                tool_kind = "plugin"
            return harness_session.ToolCallHistoryEntry(
                **base,
                tool_call_id=tool_call_id,
                tool_kind=tool_kind,
                name=task_call_payload.name or "tool",
                arguments=task_call_payload.input,
            )

        if isinstance(entry, _LegacyTaskResultHistoryEntry):
            task_result_payload = entry.payload
            state = task_result_payload.state
            output = state.output
            return harness_session.ToolResultHistoryEntry(
                **base,
                tool_call_id=task_result_payload.id or state.id or entry_id,
                name=task_result_payload.name,
                result=output.value,
                error=(
                    harness_session.ProtocolError(
                        code="remote_tool_failed",
                        message=output.error or "Remote tool failed",
                    )
                    if output.error is not None or output.status == "failed"
                    else None
                ),
            )

        if isinstance(entry, _LegacyStateHistoryEntry):
            if isinstance(entry.payload, _LegacyCheckpointPayload):
                checkpoint_content = entry.payload.content
                return harness_session.CheckpointHistoryEntry(
                    **base,
                    checkpoint_kind=checkpoint_content.checkpoint_kind,
                    message=checkpoint_content.message,
                    details=checkpoint_content.details,
                )

            if isinstance(entry.payload, _LegacyProgressPayload):
                return harness_session.NoticeHistoryEntry(
                    **base,
                    level="info",
                    notice_kind="tool_discovery",
                    message=entry.payload.content.title,
                )

            if isinstance(entry.payload, _LegacyAlertPayload):
                alert_content = entry.payload.content
                return harness_session.NoticeHistoryEntry(
                    **base,
                    level="info" if alert_content.variant == "success" else alert_content.variant,
                    message="\n\n".join(part for part in (alert_content.title, alert_content.body_md) if part),
                )
        raise AssertionError(f"Unhandled legacy history entry: {entry.type!r}")

    def _record_turn_history(self, entry: harness_session.HistoryEntry) -> None:
        turn_id = entry.turn_id
        if turn_id is None:
            return
        turn = self.turns.get(turn_id)
        is_new_turn = False
        if turn is None:
            is_new_turn = True
            turn = harness_session.TurnState(
                id=turn_id,
                status="running",
                started_at=entry.created_at,
            )
        entry_ids = list(turn.history_entry_ids)
        if entry.id not in entry_ids:
            entry_ids.append(entry.id)
        self.turns[turn_id] = turn.model_copy(update={"history_entry_ids": entry_ids})
        if turn.status != "terminated":
            self.active_turn_id = turn_id
        if is_new_turn and self.workflow_running_observed and turn_id not in self.started_turn_ids:
            self.started_turn_ids.add(turn_id)
            self._pending_events.append(harness_session.TurnStartedEvent(turn=self.turns[turn_id]))

    def _record_command_outcome(self, entry: harness_session.HistoryEntry) -> None:
        if isinstance(entry, harness_session.MessageHistoryEntry) and entry.role == "user":
            self.command_outcomes[entry.id] = _LegacyCommandOutcome(command_id=entry.id, outcome="accepted")


def build_session_from_product(product: AgentSessionResponse) -> harness_session.Session:
    """Describe a product session row as a Harness session, before any event is folded.

    Shared with the Session v1 projection: the product row is protocol-independent, so both
    read the session's own status the same way.
    """

    status: harness_session.SessionStatus
    termination: harness_session.Termination | None = None
    if product.status is AgentSessionStatus.WAITING:
        status = "waiting"
    elif product.status in {
        AgentSessionStatus.COMPLETED,
        AgentSessionStatus.FAILED,
        AgentSessionStatus.TERMINATED,
    }:
        status = "terminated"
        if product.status is AgentSessionStatus.FAILED:
            termination = harness_session.FailedTermination(
                error=harness_session.ProtocolError(
                    code="remote_session_failed",
                    message=product.error or "Remote Session failed",
                )
            )
        elif product.status is AgentSessionStatus.TERMINATED:
            termination = harness_session.CancelledTermination(reason=product.error, cause=_cancelled_cause(product))
        else:
            termination = harness_session.CompletedTermination()
    else:
        status = "running"
    session_id = str(product.agent_session_id)
    return harness_session.Session(
        id=session_id,
        root_session_id=str(product.root_session_id or product.agent_session_id),
        parent_session_id=str(product.parent_session_id) if product.parent_session_id is not None else None,
        title=product.title if "title" in product.model_fields_set else product.generated_title,
        archived_at=_datetime_ms(product.archived_at) if product.archived_at is not None else None,
        status=status,
        termination=termination,
        created_at=_datetime_ms(product.created_at),
        updated_at=_datetime_ms(product.updated_at),
    )


def _cancelled_cause(product: AgentSessionResponse) -> str | None:
    """The Session limit that stopped the Session, recorded on its terminal output."""

    cause = (product.terminal_output or {}).get("cause")
    return cause if isinstance(cause, str) else None


def _root_history_index(patch: _LegacyHistoryPatch) -> int | None:
    if isinstance(patch, _LegacyHistoryRemovePatch):
        raise RemoteProjectionError("Vibe Agents history removal is unsupported")
    path = patch.path
    if not path.startswith("/"):
        return None
    first = path[1:].split("/", 1)[0]
    return int(first) if first.isdigit() else None


def _repeated_root_add_value(
    patches: list[_LegacyHistoryPatch],
    *,
    root_index: int,
    rendered_entries: list[dict[str, object]],
) -> object | None:
    if len(patches) != 1 or root_index >= len(rendered_entries):
        return None
    patch = patches[0]
    if not isinstance(patch, _LegacyHistoryValuePatch) or patch.op != "add" or patch.path != f"/{root_index}":
        return None
    return patch.value


def _callback_outcome(output: _LegacyTaskOutput) -> harness_session.CallbackOutcome:
    """Map the legacy task output onto the canonical callback outcome.

    ``running`` reaches here only on a malformed result, since this is the terminal
    entry. It reads as cancelled rather than answered: nothing came back.
    """
    match output.status:
        case "completed":
            return harness_session.AnsweredCallbackOutcome(output=output.value)
        case "failed":
            return harness_session.FailedCallbackOutcome(
                error=harness_session.ProtocolError(
                    message=output.error or "The callback failed.", code="callback_failed"
                )
            )
        case _:
            return harness_session.CancelledCallbackOutcome(reason=output.error)


def _callback_result(entry: _LegacyHistoryEntry) -> tuple[str, _LegacyTaskOutput] | None:
    """Read the callback id and its outcome off a history entry, when it is a resolution."""
    if not isinstance(entry, _LegacyTaskResultHistoryEntry):
        return None
    if entry.payload.name != "callback_result" or entry.payload.id is None:
        return None
    return entry.payload.id, entry.payload.state.output


def _annotation_text(annotations: dict[str, JsonValue], key: str) -> str | None:
    value = annotations.get(key)
    return value if isinstance(value, str) and value else None


def _entry_id(session_id: str, source_index: int, entry: _LegacyHistoryEntry) -> str:
    if entry.id:
        return entry.id
    return f"history:{uuid5(_HISTORY_ID_NAMESPACE, f'{session_id}:{source_index}')}"


def _content_blocks(raw: list[_LegacyMessageContentBlock]) -> list[harness_session.ContentBlock]:
    blocks: list[harness_session.ContentBlock] = []
    for value in raw:
        if isinstance(value, _LegacyTextContentBlock):
            blocks.append(harness_session.TextContentBlock(text=value.text))
        elif isinstance(value, _LegacyImageContentBlock):
            blocks.append(harness_session.ImageContentBlock(uri=value.uri))
        else:
            blocks.append(
                harness_session.ResourceLinkContentBlock(
                    uri=value.uri,
                    name=value.name,
                    media_type=value.media_type,
                )
            )
    return blocks


def _parse_legacy_history_entry(
    raw: dict[str, object],
    *,
    source_index: int,
) -> _LegacyHistoryEntry:
    entry_type = raw.get("type")
    try:
        return _LEGACY_HISTORY_ENTRY_ADAPTER.validate_python(raw)
    except ValidationError as error:
        raise RemoteProjectionError(
            f"Malformed legacy Vibe Agents history entry {source_index} ({entry_type!r})"
        ) from error


def _event_time_ms(event: _LegacyVibeAgentsEvent, *, fallback: int) -> int:
    annotations = event.annotations
    if annotations is not None:
        value = annotations.get(_CREATED_AT_ANNOTATION)
        if isinstance(value, str):
            try:
                return _datetime_ms(datetime.fromisoformat(value.replace("Z", "+00:00")))
            except ValueError:
                pass
    return fallback


def _parse_product_event(event: dict[str, object]) -> _LegacyVibeAgentsEvent:
    try:
        return _PRODUCT_EVENT_ADAPTER.validate_python(event)
    except ValidationError as error:
        raise RemoteProjectionError(f"Malformed legacy Vibe Agents {event.get('type')!r} event") from error


def _datetime_ms(value: datetime) -> int:
    return int(value.timestamp() * 1000)


__all__ = [
    "RemoteProjectionError",
    "VibeAgentsSessionProjection",
    "build_session_from_product",
]
