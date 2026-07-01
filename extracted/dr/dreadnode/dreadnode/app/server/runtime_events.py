import asyncio
import typing as t
from collections import deque
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from loguru import logger
from pydantic import BaseModel, Field

from dreadnode.app.api.models import HumanPrompt

# ---------------------------------------------------------------------------
# Event kind constants
# ---------------------------------------------------------------------------

# Turn lifecycle (session-scoped)
EVENT_TURN_ACCEPTED = "turn.accepted"
EVENT_TURN_STARTED = "turn.started"
EVENT_TURN_COMPLETED = "turn.completed"
EVENT_TURN_FAILED = "turn.failed"
EVENT_TURN_CANCELLED = "turn.cancelled"
EVENT_TURN_EVENT = "turn.event"

# Prompts / interaction (session-scoped)
EVENT_PROMPT_REQUIRED = "prompt.required"

# Transport (session-scoped)
EVENT_TRANSPORT_HEARTBEAT = "transport.heartbeat"

# Session-level
EVENT_SESSION_WARNING = "session.warning"

# Runtime-level
EVENT_SESSION_CREATED = "session.created"
EVENT_SESSION_DELETED = "session.deleted"
EVENT_CAPABILITIES_RELOADED = "capabilities.reloaded"
EVENT_COMPONENT_STATE_CHANGED = "component.state_changed"

# Terminal turn kinds — events that signal end-of-turn
TERMINAL_TURN_KINDS = frozenset(
    {
        EVENT_TURN_COMPLETED,
        EVENT_TURN_FAILED,
        EVENT_TURN_CANCELLED,
    }
)

# Reserved kind prefixes — only the runtime may publish these. External
# callers (workers, third-party clients) are rejected if they attempt to
# inject under these namespaces, so they can't forge lifecycle events the
# TUI and other subscribers treat as authoritative.
RESERVED_KIND_PREFIXES: tuple[str, ...] = (
    "turn.",
    "prompt.",
    "session.",
    "transport.",
    "capabilities.",
    "component.",
)


def is_reserved_kind(kind: str) -> bool:
    """Return True if ``kind`` is in a runtime-reserved namespace."""
    return any(kind.startswith(prefix) for prefix in RESERVED_KIND_PREFIXES)


# Control envelope kinds (not part of the session event stream)
CONTROL_HELLO_ACK = "hello.ack"
CONTROL_PONG = "pong"
CONTROL_COMMAND_ACK = "command.ack"
CONTROL_COMMAND_ERROR = "command.error"
CONTROL_SESSION_SNAPSHOT = "session.snapshot"
CONTROL_TRANSPORT_RESYNC = "transport.resync_required"
CONTROL_FORWARDER_FAILED = "transport.forwarder_failed"


class RuntimeCommandEnvelope(BaseModel):
    """Client-to-server command envelope for interactive runtime transport."""

    schema_version: int = 2
    command_id: str
    op: str
    session_id: str | None = None
    payload: dict[str, t.Any] = Field(default_factory=dict)


class SubscribeCommandPayload(BaseModel):
    """Subscribe to a session stream starting after an optional sequence."""

    after_seq: int | None = None


class TurnStartCommandPayload(BaseModel):
    """Start a turn on an existing or auto-created session."""

    message: str
    model: str | None = None
    agent: str | None = None
    reset: bool = False
    generate_params_extra: dict[str, t.Any] | None = None


class TurnCancelCommandPayload(BaseModel):
    """Cancel the active turn for a session."""

    turn_id: str | None = None


class PromptRespondCommandPayload(BaseModel):
    """Respond to a pending human-input or permission prompt.

    Two shapes flow through this single command:
    - human-input: ``{request_id, action: "submit"|"cancel", answers}``
    - permission: ``{request_id, decision: "allow"|"allow_session"|"deny"}``

    The server routes on the presence of ``action`` vs ``decision`` —
    they are mutually exclusive.
    """

    request_id: str
    action: t.Literal["submit", "cancel"] | None = None
    answers: list[dict[str, t.Any]] | None = None
    decision: t.Literal["allow", "allow_session", "deny"] | None = None


class RuntimeControlEnvelope(BaseModel):
    """Out-of-band runtime transport message for commands and snapshots."""

    schema_version: int = 2
    connection_id: str | None = None
    command_id: str | None = None
    session_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    kind: str
    payload: dict[str, t.Any] = Field(default_factory=dict)


class RuntimeDraftState(BaseModel):
    """Compact draft-related state for session snapshots."""

    text_visible: bool = False
    last_generation_input_tokens: int | None = None


class RuntimeSessionSyncStatus(BaseModel):
    """Compact platform-sync health state for a runtime session."""

    state: t.Literal["ok", "degraded", "disabled"]
    last_error: str | None = None
    last_attempt_at: datetime | None = None


class RuntimeSessionSnapshot(BaseModel):
    """Compact snapshot used for subscription bootstrap and resync."""

    schema_version: int = 2
    session_id: str
    latest_seq: int
    active_turn_id: str | None = None
    turn_phase: str | None = None
    pending_prompt: HumanPrompt | None = None
    sync_status: RuntimeSessionSyncStatus = Field(
        default_factory=lambda: RuntimeSessionSyncStatus(state="disabled")
    )
    draft_state: RuntimeDraftState = Field(default_factory=RuntimeDraftState)


class RuntimeEventEnvelope(BaseModel):
    """Server-to-client event envelope for interactive runtime transport."""

    schema_version: int = 2
    connection_id: str | None = None
    session_id: str | None = None
    turn_id: str | None = None
    event_id: str = Field(default_factory=lambda: uuid4().hex)
    seq: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    kind: str
    replay: bool = False
    terminal: bool = False
    payload: dict[str, t.Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Unified EventBus — replaces per-session brokers
# ---------------------------------------------------------------------------


@dataclass(eq=False)
class EventBusSubscription:
    """A filtered subscription to the runtime event bus.

    Uses identity-based equality so instances can live in a set.
    """

    queue: asyncio.Queue[RuntimeEventEnvelope]
    session_filter: str | None = None
    kind_filter: frozenset[str] | None = None
    include_runtime: bool = False
    after_seq: int | None = None
    needs_resync: bool = False


class EventBus:
    """Unified runtime event bus with per-session replay buffers.

    Replaces per-session ``SessionEventBroker`` instances with a single bus
    that routes events to filtered subscribers. Maintains per-session replay
    buffers internally so reconnecting clients can catch up.
    """

    def __init__(
        self,
        *,
        max_events_per_session: int = 500,
        max_bytes_per_session: int = 2_000_000,
        max_runtime_events: int = 50,
        max_runtime_bytes: int = 200_000,
    ) -> None:
        self._max_events_per_session = max_events_per_session
        self._max_bytes_per_session = max_bytes_per_session
        self._max_runtime_events = max_runtime_events
        self._max_runtime_bytes = max_runtime_bytes

        self._seq = 0
        self._session_buffers: dict[str, deque[RuntimeEventEnvelope]] = {}
        self._session_buffer_bytes: dict[str, int] = {}
        self._runtime_buffer: deque[RuntimeEventEnvelope] = deque()
        self._runtime_buffer_bytes = 0
        self._subscribers: set[EventBusSubscription] = set()
        self._dropped_sessions: set[str] = set()
        self._lock = asyncio.Lock()

        # Stats
        self._trimmed_event_count = 0
        self._replay_request_count = 0
        self._replay_hit_count = 0
        self._replay_miss_count = 0
        self._stale_subscriber_count = 0

    # -- Stats (read outside the lock; counters only increase) ---------------

    @property
    def trimmed_event_count(self) -> int:
        return self._trimmed_event_count

    @property
    def replay_request_count(self) -> int:
        return self._replay_request_count

    @property
    def replay_hit_count(self) -> int:
        return self._replay_hit_count

    @property
    def replay_miss_count(self) -> int:
        return self._replay_miss_count

    @property
    def stale_subscriber_count(self) -> int:
        return self._stale_subscriber_count

    # -- Publish -------------------------------------------------------------

    async def publish(
        self,
        *,
        kind: str,
        session_id: str | None = None,
        turn_id: str | None = None,
        payload: dict[str, t.Any] | None = None,
        terminal: bool = False,
    ) -> RuntimeEventEnvelope | None:
        """Publish an event. ``session_id=None`` for runtime-level events.

        Returns ``None`` if the session has been dropped (tombstoned).
        """
        if session_id is not None and session_id in self._dropped_sessions:
            logger.debug(
                "Event bus rejected publish to dropped session | session={} kind={}",
                session_id,
                kind,
            )
            return None

        async with self._lock:
            self._seq += 1
            envelope = RuntimeEventEnvelope(
                session_id=session_id,
                turn_id=turn_id,
                seq=self._seq,
                kind=kind,
                terminal=terminal,
                payload=payload or {},
            )
            envelope_size = _estimate_size(envelope)

            if session_id is not None:
                buf = self._session_buffers.setdefault(session_id, deque())
                buf.append(envelope)
                self._session_buffer_bytes[session_id] = (
                    self._session_buffer_bytes.get(session_id, 0) + envelope_size
                )
                self._trim_session_buffer(session_id)
            else:
                self._runtime_buffer.append(envelope)
                self._runtime_buffer_bytes += envelope_size
                self._trim_runtime_buffer()

            matching = [sub for sub in self._subscribers if self._matches(sub, envelope)]

        stale: list[EventBusSubscription] = []
        for sub in matching:
            try:
                sub.queue.put_nowait(envelope)
            except asyncio.QueueFull:
                stale.append(sub)

        if stale:
            async with self._lock:
                for sub in stale:
                    self._subscribers.discard(sub)
                self._stale_subscriber_count += len(stale)
            logger.warning(
                "Event bus subscriber(s) dropped due to backpressure | count={}",
                len(stale),
            )

        return envelope

    # -- Subscribe / Unsubscribe ---------------------------------------------

    async def subscribe(
        self,
        *,
        session_id: str | None = None,
        kinds: frozenset[str] | None = None,
        include_runtime: bool = False,
        after_seq: int | None = None,
        queue_maxsize: int = 256,
    ) -> EventBusSubscription:
        """Subscribe with optional filters. Returns subscription with replay.

        Replay events are drained into the queue under the lock so ordering
        is preserved against concurrent publishes (same guarantee as the old
        ``SessionEventBroker.subscribe``).
        """
        async with self._lock:
            needs_resync = False
            replay_events: list[RuntimeEventEnvelope] = []

            if after_seq is not None:
                self._replay_request_count += 1

            if session_id is not None:
                buf = self._session_buffers.get(session_id, deque())
                if after_seq is not None and buf:
                    oldest = buf[0].seq
                    if after_seq < (oldest - 1):
                        needs_resync = True
                        self._replay_miss_count += 1
                        logger.warning(
                            "Event bus replay miss | session={} after_seq={} oldest_buffered={} latest={}",
                            session_id,
                            after_seq,
                            oldest,
                            self._seq,
                        )
                replay_events = [
                    event.model_copy(update={"replay": True})
                    for event in buf
                    if after_seq is None or event.seq > after_seq
                ]
            elif include_runtime:
                replay_events = [
                    event.model_copy(update={"replay": True})
                    for event in self._runtime_buffer
                    if after_seq is None or event.seq > after_seq
                ]

            if after_seq is not None and replay_events:
                self._replay_hit_count += 1

            effective_maxsize = len(replay_events) + queue_maxsize
            queue: asyncio.Queue[RuntimeEventEnvelope] = asyncio.Queue(
                maxsize=effective_maxsize,
            )

            subscription = EventBusSubscription(
                queue=queue,
                session_filter=session_id,
                kind_filter=kinds,
                include_runtime=include_runtime if session_id is not None else True,
                after_seq=after_seq,
                needs_resync=needs_resync,
            )

            for event in replay_events:
                queue.put_nowait(event)

            self._subscribers.add(subscription)

        return subscription

    async def unsubscribe(self, subscription: EventBusSubscription) -> None:
        """Remove a subscriber."""
        async with self._lock:
            self._subscribers.discard(subscription)

    # -- Session lifecycle ---------------------------------------------------

    def drop_session(self, session_id: str) -> None:
        """Evict a session's replay buffer and tombstone the session ID.

        Safe to call from sync contexts. After this call, any publish
        targeting this session_id is silently rejected — prevents zombie
        buffers when a cancelled turn processor publishes cleanup events
        after session deletion.
        """
        self._session_buffers.pop(session_id, None)
        self._session_buffer_bytes.pop(session_id, None)
        self._dropped_sessions.add(session_id)

    # -- Snapshot (for websocket reconnect) ----------------------------------

    async def snapshot(
        self,
        session_id: str,
        *,
        active_turn_id: str | None = None,
        turn_phase: str | None = None,
        pending_prompt: HumanPrompt | None = None,
        sync_status: RuntimeSessionSyncStatus | None = None,
        draft_state: RuntimeDraftState | None = None,
    ) -> RuntimeSessionSnapshot:
        """Build a snapshot for a specific session, reading seq under lock."""
        async with self._lock:
            buf = self._session_buffers.get(session_id, deque())
            latest_seq = buf[-1].seq if buf else 0

        return RuntimeSessionSnapshot(
            session_id=session_id,
            latest_seq=latest_seq,
            active_turn_id=active_turn_id,
            turn_phase=turn_phase,
            pending_prompt=pending_prompt,
            sync_status=sync_status or RuntimeSessionSyncStatus(state="disabled"),
            draft_state=draft_state or RuntimeDraftState(),
        )

    def session_oldest_buffered_seq(self, session_id: str) -> int | None:
        """Oldest buffered seq for a session. Used by websocket resync info."""
        buf = self._session_buffers.get(session_id)
        if not buf:
            return None
        return buf[0].seq

    # -- Internal ------------------------------------------------------------

    @staticmethod
    def _matches(sub: EventBusSubscription, envelope: RuntimeEventEnvelope) -> bool:
        if envelope.session_id is None:
            if not sub.include_runtime:
                return False
        elif sub.session_filter is not None and envelope.session_id != sub.session_filter:
            return False

        return sub.kind_filter is None or envelope.kind in sub.kind_filter

    def _trim_session_buffer(self, session_id: str) -> None:
        buf = self._session_buffers.get(session_id)
        if buf is None:
            return
        buf_bytes = self._session_buffer_bytes.get(session_id, 0)
        trimmed = 0
        while buf and (
            len(buf) > self._max_events_per_session or buf_bytes > self._max_bytes_per_session
        ):
            dropped = buf.popleft()
            buf_bytes = max(0, buf_bytes - _estimate_size(dropped))
            trimmed += 1
            self._trimmed_event_count += 1
        self._session_buffer_bytes[session_id] = buf_bytes
        if trimmed and buf:
            logger.debug(
                "Event bus session buffer trimmed | session={} trimmed={} oldest_seq={} latest_seq={}",
                session_id,
                trimmed,
                buf[0].seq,
                self._seq,
            )

    def _trim_runtime_buffer(self) -> None:
        trimmed = 0
        while self._runtime_buffer and (
            len(self._runtime_buffer) > self._max_runtime_events
            or self._runtime_buffer_bytes > self._max_runtime_bytes
        ):
            dropped = self._runtime_buffer.popleft()
            self._runtime_buffer_bytes = max(
                0, self._runtime_buffer_bytes - _estimate_size(dropped)
            )
            trimmed += 1
            self._trimmed_event_count += 1


def _estimate_size(event: RuntimeEventEnvelope) -> int:
    """Fast size estimation using orjson."""
    import orjson

    return len(orjson.dumps(event.model_dump(mode="json")))
