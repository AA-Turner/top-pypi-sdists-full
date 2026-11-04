"""Events: what happened in a session, in the order it happened, as immutable values.

Each event has the ``id`` of its position in the session's log: read again after it with
``session.iter_events(after=event.id)``. A few events are typed. An event of a type this SDK does
not know is an :class:`UnknownEvent` with its type name and the host's data. The other events this
SDK knows but does not type, such as a notice, are not delivered: their position still moves
``after=``, and a debug log line names them (shown with ``AGENTS_SDK_DEBUG=1``). The raw protocol
client, ``session_protocol.attach(session).events()``, yields every event. Changes to history
entries (an entry added, patched or completed) are not delivered yet.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable, Callable, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Literal

import structlog
from pydantic import JsonValue

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.app_server.session import SessionClient as _RawSession
from mistralai.vibe.harness.app_server.session import SessionTransport
from mistralai.vibe_agents.sdk.authoring.errors import mark_caller_error
from mistralai.vibe_agents.sdk.client.approval_requests import NO_TOOLS, _Tool
from mistralai.vibe_agents.sdk.client.records import (
    Blocked,
    Completed,
    Failed,
    Interrupted,
    ObservationLost,
    OpenCallback,
    Running,
    TurnState,
    UnknownOutcome,
)
from mistralai.vibe_agents.sdk.client.turn_reads import open_callback, read_turn
from mistralai.vibe_agents.sdk.transport.client_tools import callback_turn_id
from mistralai.vibe_agents.sdk.transport.remote import VibeAgentsSessionTransport

__all__ = [
    "CallbackOpened",
    "CallbackResolved",
    "Event",
    "EventHandler",
    "SessionUpdated",
    "TurnEnded",
    "TurnStarted",
    "TurnUpdated",
    "UnknownEvent",
]

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class Event:
    """One event of a session.

    ``id`` is its position in the session's log. ``turn_id`` is the turn it happened in, or
    ``None`` when it happened between turns or the turn is not known.
    """

    id: str
    session_id: str
    turn_id: str | None


@dataclass(frozen=True, slots=True, kw_only=True)
class TurnStarted(Event):
    """A turn started."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class TurnEnded(Event):
    """A turn ended. ``state`` is its record.

    When the session's end ends the turn, ``TurnEnded`` comes first, with the ``id`` of the session's
    end: after that ``id``, the session's end is not read again. To read on, use ``after=`` its
    ``id``: ``state.cursor`` is where the turn was read, which can be later.
    """

    __match_args__ = ("state",)

    state: Completed[str] | Interrupted | Failed | UnknownOutcome


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class CallbackOpened(Event):
    """The turn waits on a callback, such as an approval."""

    __match_args__ = ("callback",)

    callback: OpenCallback


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class CallbackResolved(Event):
    """A callback was answered or closed."""

    __match_args__ = ("callback_id",)

    callback_id: str


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class TurnUpdated(Event):
    """A turn's status changed while it runs: ``"blocked"`` when it waits on a callback, such as an
    approval, ``"running"`` when it runs again. ``turn_id`` is always that turn's id.

    The turn's end is :class:`TurnEnded`, which has its record.
    """

    __match_args__ = ("turn_id", "status")

    turn_id: str
    status: Literal["running", "blocked", "terminated"]


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class SessionUpdated(Event):
    """The session changed: its status, or its title, or it was archived.

    ``status`` is ``"running"`` while a turn is active, ``"waiting"`` when no turn is, and
    ``"terminated"`` once the session has ended. ``title`` is the session's title, or ``None`` when
    it has none yet. ``archived`` is whether the session is archived.
    """

    __match_args__ = ("status",)

    status: Literal["running", "waiting", "terminated"]
    title: str | None
    archived: bool


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class UnknownEvent(Event):
    """An event with no type of its own here. ``type`` is the host's name for it, ``raw`` its data.

    New event types are added in minor versions. Ignore the event types that you do not know.
    """

    __match_args__ = ("type",)

    type: str
    raw: dict[str, JsonValue] = field(default_factory=dict, repr=False, compare=False)


type EventHandler = Callable[[Event], Awaitable[None] | None]
"""A plain or async function that receives each event."""

# How long a reader waits before it reads a turn again when its events showed the turn's end and the
# read still says it runs. Each later try waits twice as long, up to ``_LAGGED_END_MAX_SECONDS``.
_LAGGED_END_RETRY_SECONDS = 0.05
_LAGGED_END_MAX_SECONDS = 1.0


# Their content is the streaming design, still open; they come later as types of their own.
_ENTRY_CHANGES = frozenset({"history_entry_added", "history_entry_patched", "history_entry_completed"})

# The event types this SDK knows. An event of any other type is an UnknownEvent; one of these that
# has no type of its own here is left out of the typed stream, with a debug line.
_KNOWN_TYPES = _ENTRY_CHANGES | {
    "turn_started",
    "turn_updated",
    "turn_terminated",
    "session_updated",
    "session_terminated",
    "callback_opened",
    "callback_resolved",
    "prompt_suggested",
    "artifact_created",
    "notice",
    "error",
}


async def deliver(on_event: EventHandler | None, event: Event) -> None:
    if on_event is None:
        return
    try:
        if (pending := on_event(event)) is not None:
            await pending
    except Exception as error:
        # The handler's error reaches the caller as it is, even an httpx error of its own request.
        mark_caller_error(error)
        raise


def active_turn_at(after: TurnState[object] | str | None, turn_id: str | None) -> str | None:
    """The turn running at the position ``after``: a record says it; a cursor is taken to be ``turn_id``'s.

    Only taken: the turn may have ended at or before the cursor. ``follow`` gets ``active_known=False`` then.
    """
    if isinstance(after, Running | Blocked):
        return after.turn_id
    return turn_id if isinstance(after, str) else None


def ended_record(after: TurnState[object] | str | None, turn_id: str) -> bool:
    """Whether ``after`` is a record of the turn that says it ended: no event of it comes after."""
    return not isinstance(after, str | None | Running | Blocked) and after.turn_id == turn_id


async def follow(
    raw: _RawSession,
    transport: SessionTransport,
    session_id: str,
    *,
    after: str | None,
    active_turn_id: str | None,
    active_known: bool = True,
    turn_id: str | None = None,
    ends: Mapping[str, TurnState[str]] | None = None,
    reconnect: bool = True,
    reread: bool = True,
    tools: Mapping[str, _Tool] = NO_TOOLS,
) -> AsyncGenerator[tuple[str, Event | None]]:
    """Yield each position of the session's log after ``after``, with its event or ``None``.

    ``None`` is a position whose event is not delivered: an entry change, a frame the transport
    could not read, or, with ``turn_id``, another turn's event. With ``turn_id``, this ends after
    that turn's ``TurnEnded``. A turn's end reads it (2 requests) unless ``ends`` has its record, and,
    with ``reread``, reads it again while the read lags the events.
    ``active_turn_id`` is the turn running at ``after``; without ``active_known``, it is only taken
    to run there, as a turn's reader after a bare cursor does. When the session ends before an
    event told which turn runs after the cursor ``after``, the session's last turn is read (one
    more request): it ended with the session if it has no end of its own. A turn that ended before
    ``after`` thus gets no second end. Without ``reconnect``, a deployment's stream that drops
    raises at once instead of reconnecting. ``tools`` are the agent's tool objects by tool id, for
    the requests of approvals.

    Raises:
        ObservationLost: The session's events could not be read again.
    """
    # Only a session's reader looks the running turn up at the session's end.
    known = turn_id is not None or after is None or active_turn_id is not None
    turns = _Turns(active_turn_id, known=known and active_known)
    cursor = after
    params = harness_session.EventsReadParams(session_id=session_id, after_event_id=after)
    if isinstance(transport, VibeAgentsSessionTransport):
        read = transport.read_events(params, reconnect_budget_seconds=None if reconnect else 0)
    else:
        read = transport.read_events(params)
    try:
        # Both transports return an async generator: close it when the reader stops.
        async with contextlib.aclosing(read) as stream:  # type: ignore[type-var]
            async for item in stream:
                if isinstance(item, harness_session.TransportHeartbeat) and item.latest_event_id is not None:
                    # A frame the host sent that carries no event: only its position moves.
                    cursor = item.latest_event_id
                    yield cursor, None
                    continue
                for event in _events(item):
                    cursor = event.event_id
                    running = turns.active
                    owner = turns.owner(event.payload)
                    if turn_id is not None and owner != turn_id:
                        yield cursor, None
                        continue
                    terminated = isinstance(event.payload, harness_session.TurnTerminatedEvent)
                    # A turn ends with its turn_terminated event, or with the session's end.
                    ending = owner if terminated else None
                    if isinstance(event.payload, harness_session.SessionTerminatedEvent):
                        ending = running if turns.known else await _ended_with_session(raw, session_id)
                    if ending is not None:
                        state = (ends or {}).get(ending) or await read_turn(raw, session_id, ending, tools=tools)
                        if reread:
                            # The turn's end, or the session's: no turn of an ended session runs.
                            state = await _read_ended(raw, session_id, ending, state, tools=tools)
                        # Without ``reread``, a read that still says the turn runs: its end is not given.
                        if not isinstance(state, Running | Blocked):
                            yield cursor, TurnEnded(id=cursor, session_id=session_id, turn_id=ending, state=state)
                            if turn_id is not None:
                                return
                            if terminated:
                                continue
                    yield cursor, None if terminated else _event(event, owner, tools)
    except harness_session.SessionEventStreamLostError as error:
        raise ObservationLost(session_id, cursor) from error


async def _read_ended(
    raw: _RawSession,
    session_id: str,
    turn_id: str,
    state: TurnState[str],
    *,
    tools: Mapping[str, _Tool],
) -> TurnState[str]:
    """Read the turn again until the record shows the end its events showed.

    The events can show the turn's end before the session read does, and the session stays open
    after a turn: no later event would give its end. Like the wait for the end itself, this has no
    limit of its own: a wait's ``timeout`` bounds it, and a reader with none waits.
    """
    delay = _LAGGED_END_RETRY_SECONDS
    while isinstance(state, Running | Blocked):
        await asyncio.sleep(delay)
        delay = min(delay * 2, _LAGGED_END_MAX_SECONDS)
        state = await read_turn(raw, session_id, turn_id, tools=tools)
    return state


async def up_to[T](events: AsyncIterator[tuple[str, T]], position: str) -> AsyncGenerator[tuple[str, T]]:
    """The items of ``follow`` up to ``position``, a record's: the host has them already.

    Every frame gives its position, the ones the SDK cannot read too, so this stops there, or at
    the stream's end.
    """
    async for item in events:
        yield item
        if item[0] == position:
            return


async def up_to_end(
    events: AsyncGenerator[tuple[str, Event | None]], *, after: str | None, state: TurnState[str]
) -> AsyncIterator[Event]:
    """The events of a turn that ended, ``state`` its record, from ``follow``ing it after ``after``.

    They are read up to the record's position, as ``up_to`` does, and given once the turn's
    ``TurnEnded`` is among them. None comes when the turn ended at or before ``after``: the record's
    position then comes before any ``TurnEnded``, or is ``after`` itself and nothing is read.

    Raises:
        ObservationLost: The events could not be read again, at ``after``: none of them was given.
    """
    held: list[Event] = []
    async with contextlib.aclosing(events) as stream:
        if after is not None and after == state.cursor:
            return
        try:
            async with contextlib.aclosing(up_to(stream, state.cursor)) as items:
                async for _, event in items:
                    if event is not None:
                        held.append(event)
                    if isinstance(event, TurnEnded):
                        break
                else:
                    # After a cursor, an event that names no turn is taken as this turn's: past the
                    # turn's end, it is another's. The end did not come: it was at or before ``after``.
                    return
        except ObservationLost as error:
            # ``follow`` raises at the last position it read, past the events held here.
            raise ObservationLost(error.session_id, after) from error.__cause__
    for event in held:
        yield event


async def _ended_with_session(raw: _RawSession, session_id: str) -> str | None:
    """The session's last turn, if it ended with the session: a turn's own end is an event, after
    the reader's cursor (seen) or before it (the turn ended then)."""
    read = await raw.request(
        "app_server/session/read",
        harness_session.SessionReadParams(
            session_id=session_id,
            history=harness_session.PageRequest(limit=1),
            turns=harness_session.PageRequest(limit=1, direction="backward"),
        ),
        harness_session.SessionReadResponse,
    )
    last = read.state.turns.items if read.state.turns is not None else []
    return last[0].id if last and last[0].status != "terminated" else None


class _Turns:
    """Which turn each event belongs to: the one it names, else the one running.

    ``known`` says whether ``active`` is known: after a cursor, a session's reader learns it at the
    next turn's start or end.
    """

    def __init__(self, active: str | None, *, known: bool) -> None:
        self.active = active
        self.known = known
        self._callbacks: dict[str, str] = {}

    def owner(self, payload: object) -> str | None:
        match payload:
            case harness_session.TurnStartedEvent(turn=turn):
                self.active, self.known = turn.id, True
                return turn.id
            case harness_session.TurnTerminatedEvent(turn=turn):
                self.active, self.known = None, True
                return turn.id
            case harness_session.TurnUpdatedEvent(turn=turn):
                # As the session's state does: an update says whether its turn runs.
                self.active = turn.id if turn.status in {"running", "blocked"} else None
                self.known = True
                return turn.id
            case harness_session.CallbackOpenedEvent(callback=callback):
                owner = callback_turn_id(callback)
                self._callbacks[callback.id] = owner
                return owner
            case harness_session.CallbackResolvedEvent(callback_id=callback_id):
                return self._callbacks.pop(callback_id, None) or self.active
            case _:
                return self.active


def _event(event: harness_session.Event, turn_id: str | None, tools: Mapping[str, _Tool]) -> Event | None:
    base = {"id": event.event_id, "session_id": event.session_id, "turn_id": turn_id}
    match payload := event.payload:
        case harness_session.TurnStartedEvent():
            return TurnStarted(**base)
        case harness_session.CallbackOpenedEvent(callback=callback):
            return CallbackOpened(**base, callback=open_callback(callback, event.session_id, tools))
        case harness_session.CallbackResolvedEvent(callback_id=callback_id):
            return CallbackResolved(**base, callback_id=callback_id)
        case harness_session.TurnUpdatedEvent(turn=turn):
            return TurnUpdated(**{**base, "turn_id": turn.id}, status=turn.status)
        case harness_session.SessionUpdatedEvent(session=session):
            return SessionUpdated(
                **base, status=session.status, title=session.title, archived=session.archived_at is not None
            )
        case harness_session.UnknownEventPayload(original_type=event_type, raw=raw) if event_type not in _KNOWN_TYPES:
            return UnknownEvent(**base, type=event_type, raw=raw)
        case _:
            # A known type whose content is newer than this SDK comes as unknown, under its own type.
            event_type = (
                payload.original_type if isinstance(payload, harness_session.UnknownEventPayload) else payload.type
            )
            if event_type not in _ENTRY_CHANGES:
                # One line per event; the raw protocol client yields the event itself.
                logger.debug(
                    "Skipped an event this SDK version does not type", event_type=event_type, event_id=event.event_id
                )
            return None


def _events(item: harness_session.ClientTransportStreamItem) -> Iterable[harness_session.Event]:
    match item:
        case harness_session.EventBatch(events=events):
            return events
        case harness_session.Event():
            return (item,)
        case _:
            return ()
