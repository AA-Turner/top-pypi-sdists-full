"""Events: what happened in a session, in the order it happened, as immutable values.

Each event has the ``id`` of its position in the session's log: read again after it with
``session.iter_events(after=event.id)``. A few events are typed. An event of a type this SDK does
not know is an :class:`UnknownEvent` with its type name and the host's data. The other events this
SDK knows but does not type, such as a prompt suggestion, are not delivered: their position still
moves ``after=``, and a debug log line names them (shown with ``AGENTS_SDK_DEBUG=1``). The raw
protocol client, ``session_protocol.attach(session).events()``, yields every event.

Each history entry comes as :class:`EntryAdded` when the host adds it, then as
:class:`EntryCompleted` when it is complete, once each, also when the host adds it complete: a
message (a :class:`ContextMessage` too), a tool call or a tool's result, or an :class:`UnknownEntry`
for any other entry. While the model writes a message, its text comes as :class:`TextDelta` events
between the two, live. A notice comes as :class:`Notice`.
"""

from __future__ import annotations

import asyncio
import contextlib
import re
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
from mistralai.vibe_agents.sdk.client.entries import (
    Entry,
    context_message,
    message_entry,
    tool_call_entry,
    tool_result_entry,
    unknown_entry,
)
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
from mistralai.vibe_agents.sdk.client.unknown_values import UnknownValue, read_value
from mistralai.vibe_agents.sdk.transport.client_tools import callback_turn_id
from mistralai.vibe_agents.sdk.transport.remote import VibeAgentsSessionTransport

__all__ = [
    "CallbackOpened",
    "CallbackResolved",
    "EntryAdded",
    "EntryCompleted",
    "Event",
    "EventHandler",
    "Notice",
    "SessionUpdated",
    "TextDelta",
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
    ``None`` between turns or when the event does not name its turn.
    """

    id: str
    """The event's position in the session's log."""
    session_id: str
    """The ID of the session."""
    turn_id: str | None
    """The ID of the turn the event happened in, or ``None`` when it happened between turns or the turn is
    not known."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TurnStarted(Event):
    """A turn started."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class TurnEnded(Event):
    """A turn ended. Sent once, when the turn ends; ``state`` is the final turn record.

    To read the events after it, pass ``after=`` its ``id``, not ``state.cursor``, which can be later.
    """

    __match_args__ = ("state",)

    state: Completed[str] | Interrupted | Failed | UnknownOutcome
    """The turn's record."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class CallbackOpened(Event):
    """The turn waits on a callback, such as an approval."""

    __match_args__ = ("callback",)

    callback: OpenCallback
    """The callback that the turn waits on."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class CallbackResolved(Event):
    """A callback was answered or closed.

    ``turn_id`` is the turn that opened the callback, or ``None`` when the resolution does not name
    its turn.
    """

    __match_args__ = ("callback_id",)

    callback_id: str
    """The ID of the callback."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class Notice(Event):
    """A notice for the developer, which the model does not get.

    For example, a connector or an MCP server whose tools cannot be used now, or a guessed context
    window. ``level`` is ``"info"``, ``"warning"`` or ``"error"``, or an :class:`UnknownValue` for a
    level added after your SDK version. ``source`` names what the notice is about, such as
    ``"mistral_connectors:notion"`` for one connector, or is ``None``.
    ``details`` is its data, such as ``{"source_id": "mistral_connectors:notion",
    "connector": "notion", "status": "unavailable", "reason": "..."}`` for a connector; do not
    change it, copy it first. For an MCP server that cannot be used, ``source`` is the server's ID
    and ``details["reason"]`` says why: ``"credential_rejected"`` (HTTP 401 or 403),
    ``"credential_unavailable"``, ``"unreachable"``, ``"timeout"``, ``"invalid_catalog"`` or
    ``"request_failed"``. A failure of another kind has no ``reason``. ``turn_id`` is the turn this
    notice belongs to, or ``None``: the same in every read.
    """

    __match_args__ = ("message",)

    message: str
    """The notice's text."""
    level: Literal["info", "warning", "error"] | UnknownValue
    """How serious the notice is: ``"info"``, ``"warning"`` or ``"error"``, or an :class:`UnknownValue`
    for a level added after your SDK version."""
    source: str | None
    """What the notice is about, such as ``"mistral_connectors:notion"`` for one connector, or
    ``None``."""
    details: JsonValue = field(default=None, repr=False, compare=False)
    """The notice's data, such as ``{"source_id": "mistral_connectors:notion",
    "connector": "notion", "status": "unavailable", "reason": "..."}`` for a connector. Do not change
    it, copy it first."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class EntryAdded(Event):
    """An entry was added to the session's history: a message, a tool call, a tool's result, or
    another entry.

    ``entry`` is the entry as it was first added: a :class:`MessageEntry` (the user's input,
    the model's text, a :class:`ContextMessage` the model got with the input), a
    :class:`ToolCallEntry`, a :class:`ToolResultEntry` (its ``tool_call_id`` is the call's, a
    client tool's too), or an :class:`UnknownEntry` for an entry of a type added after your SDK
    version, or one this version reads only as raw data, such as a checkpoint. It can be
    incomplete: a message the model is writing has its first text, a tool's result added while the
    tool runs has no content yet. The whole entry comes as :class:`EntryCompleted`, after it.
    ``turn_id`` is the entry's, the same in every read.
    """

    __match_args__ = ("entry",)

    entry: Entry
    """The entry as it was first added, possibly incomplete."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class EntryCompleted(Event):
    """An entry of the session's history is complete: ``entry`` is the whole entry, final.

    Every entry comes as :class:`EntryAdded` first, then once as ``EntryCompleted``, also one
    added complete, such as the user's message or a tool call. ``entry`` and ``turn_id`` are as in
    :class:`EntryAdded`. A reader that starts after an entry's ``EntryAdded`` gets only its
    ``EntryCompleted``.
    """

    __match_args__ = ("entry",)

    entry: Entry
    """The whole entry, final."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class TextDelta(Event):
    """Text the model just wrote, while it writes a message.

    ``entry_id`` is the ID of the message's entry: the deltas come after its :class:`EntryAdded`
    and before its :class:`EntryCompleted`, which has all the text. The text the message was
    added with comes right after its ``EntryAdded``, with the same ``entry_id``. ``text`` is the new text:
    the deltas of one entry, joined, are its text so far, when none was missed. Keep the completed
    entry's text: when the model's call is retried, the message can be written again from its
    start, under the same ID. Deltas are live only: a reader that joins late or reads again after
    a cursor can miss some, or all, of a message's deltas, never its entry events. Once the turn
    ends, read the message's entry, not its deltas.
    """

    __match_args__ = ("text",)

    entry_id: str
    """The ID of the message's entry."""
    text: str
    """The new text."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class TurnUpdated(Event):
    """A turn's status changed: ``"blocked"`` when it waits on a callback, such as an approval,
    ``"running"`` when it runs again, ``"terminated"`` once it has ended, and an :class:`UnknownValue`
    for a status added after your SDK version, with which the turn still runs. ``turn_id`` is always that turn's ID.

    An open callback comes as :class:`CallbackOpened`, and the turn's end as :class:`TurnEnded`, which has
    its record.
    """

    __match_args__ = ("turn_id", "status")

    turn_id: str
    """The ID of the turn, always set."""
    status: Literal["running", "blocked", "terminated"] | UnknownValue
    """``"blocked"`` when the turn waits on a callback, such as an approval, ``"running"`` when it runs
    again, ``"terminated"`` once it has ended (:class:`TurnEnded` has its record), or an
    :class:`UnknownValue` for a status added after your SDK version, such as ``"paused"``, with which the
    turn still runs."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class SessionUpdated(Event):
    """The session changed: its status, or its title, or it was archived.

    ``status`` is ``"running"`` while a turn is active, ``"waiting"`` when no turn is, and
    ``"terminated"`` once the session has ended, and an :class:`UnknownValue` for a status added
    after your SDK version. ``title`` is the session's title, or ``None`` when it has none yet. ``archived`` is
    whether the session is archived. ``turn_id`` is always ``None``: a change of the session belongs
    to no turn, even one made while a turn runs.
    """

    __match_args__ = ("status",)

    status: Literal["running", "waiting", "terminated"] | UnknownValue
    """``"running"`` while a turn is active, ``"waiting"`` when no turn is, ``"terminated"`` once the
    session has ended, or an :class:`UnknownValue` for a status added after your SDK version, such as
    ``"paused"``."""
    title: str | None
    """The session's title, or ``None`` when it has none yet."""
    archived: bool
    """Whether the session is archived."""


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class UnknownEvent(Event):
    """An event type added after your SDK version. ``type`` names it, and ``raw`` holds its data.

    New event types are added in minor versions. Ignore the event types that you do not know.
    ``turn_id`` is always ``None``; read ``raw`` for the event's data.
    """

    __match_args__ = ("type",)

    type: str
    """The event's type."""
    raw: dict[str, JsonValue] = field(default_factory=dict, repr=False, compare=False)
    """The event's data, unparsed."""


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
    A cursor, or a record's, can also precede the turn's start: a reader named it before it read the
    turn running. Whether a reader read its turn is not taken from here.
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
    start: str | None,
    active_turn_id: str | None,
    active_known: bool = True,
    turn_id: str | None = None,
    ends: Mapping[str, TurnState[str]] | None = None,
    reconnect: bool = True,
    reread: bool = True,
    tools: Mapping[str, _Tool] = NO_TOOLS,
    confirmed: bool = False,
) -> AsyncGenerator[tuple[str, Event | None]]:
    """Yield each position of the session's log after ``after``, with its event or ``None``.

    ``None`` is a position whose event is not delivered: an entry change, a frame the transport
    could not read, or, with ``turn_id``, another turn's event. With ``turn_id``, the events that
    name no turn while none runs, such as a notice or the previous turn's ``SessionUpdated``, are
    the next turn's: they come at this turn's start, if it is that next turn, as the session has
    them (no ``turn_id``). This ends after this turn's ``TurnEnded``. A turn's end reads it (2
    requests) unless ``ends`` has its record, and, with ``reread``, reads it again while the read
    lags the events.
    ``start`` is where the reader started: with ``turn_id``, until the reader reads that turn
    running, ``ObservationLost`` names it, since a position before the turn's start would not say
    which turn ran there. ``active_turn_id`` is the turn running at ``after``; without
    ``active_known``, it is only taken to run there, as a turn's reader after a bare cursor does.
    When the session ends before an event told which turn runs after the cursor ``after``, the
    session's last turn is read (one more request): it ended with the session if it has no end of
    its own. A turn that ended before ``after`` thus gets no second end. Without ``reconnect``, a
    deployment's stream that drops raises at once instead of reconnecting. ``tools`` are the
    agent's tool objects by tool ID, for the requests of approvals. ``confirmed`` says that the host
    confirmed ``turn_id`` (see ``read_turn_and_start``): its end reads it so too, since the session
    can end before the host lists the turn.

    Raises:
        ObservationLost: The session's events could not be read again.
    """
    # Only a session's reader looks the running turn up at the session's end.
    known = turn_id is not None or after is None or active_turn_id is not None
    turns = _Turns(active_turn_id, known=known and active_known)
    cursor = after
    # A turn's reader holds the positions it reads while no turn runs: their events are the next
    # turn's. They come at its start if it is this one, else with no event.
    held: list[tuple[str, harness_session.Event | None]] = []
    # Whether the reader read an event of its turn: before, ``ObservationLost`` names ``start``.
    # Not taken from ``active_turn_id``: a cursor this reader named in the previous turn says the
    # same turn runs there.
    reached = turn_id is None
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
                    if held:
                        held.append((item.latest_event_id, None))
                        continue
                    cursor = item.latest_event_id
                    yield cursor, None
                    continue
                for event in _events(item):
                    running = turns.active
                    owner = turns.owner(event.payload)
                    terminated = isinstance(event.payload, harness_session.TurnTerminatedEvent)
                    ending_session = isinstance(event.payload, harness_session.SessionTerminatedEvent)
                    if turn_id is not None and owner is None and not ending_session:
                        held.append((event.event_id, event))
                        continue
                    if held and owner != turn_id and turns.active is None and not (terminated or ending_session):
                        # A late event of an ended turn, such as a callback's answer: still no turn runs.
                        held.append((event.event_id, None))
                        continue
                    reached = reached or owner == turn_id
                    # A turn started or ended, or the session: the held events are this turn's if it started.
                    for position, waiting in held:
                        cursor = position
                        for typed in (
                            () if waiting is None or owner != turn_id else _event(waiting, None, tools, turns)
                        ) or (None,):
                            yield cursor, typed
                    held.clear()
                    cursor = event.event_id
                    if turn_id is not None and owner != turn_id:
                        yield cursor, None
                        continue
                    # A turn ends with its turn_terminated event, or with the session's end.
                    ending = owner if terminated else None
                    if ending_session:
                        ending = running if turns.known else await _ended_with_session(raw, session_id)
                    if ending is not None:
                        own = confirmed and ending == turn_id
                        state = (ends or {}).get(ending) or await read_turn(
                            raw, session_id, ending, tools=tools, confirmed=own
                        )
                        if reread:
                            # The turn's end, or the session's: no turn of an ended session runs.
                            state = await _read_ended(raw, session_id, ending, state, tools=tools, confirmed=own)
                        # Without ``reread``, a read that still says the turn runs: its end is not given.
                        if not isinstance(state, Running | Blocked):
                            yield cursor, TurnEnded(id=cursor, session_id=session_id, turn_id=ending, state=state)
                            if turn_id is not None:
                                return
                            if terminated:
                                continue
                    for typed in (() if terminated else _event(event, owner, tools, turns)) or (None,):
                        yield cursor, typed
    except harness_session.SessionEventStreamLostError as error:
        raise ObservationLost(session_id, cursor if reached else start) from error


async def _read_ended(
    raw: _RawSession,
    session_id: str,
    turn_id: str,
    state: TurnState[str],
    *,
    tools: Mapping[str, _Tool],
    confirmed: bool = False,
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
        state = await read_turn(raw, session_id, turn_id, tools=tools, confirmed=confirmed)
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
        # The model's messages being written, by entry id, with their turns: their patches are deltas.
        self.streams: dict[str, str | None] = {}

    def owner(self, payload: object) -> str | None:
        match payload:
            case harness_session.TurnStartedEvent(turn=turn):
                self.active, self.known = turn.id, True
                return turn.id
            case harness_session.TurnTerminatedEvent(turn=turn):
                self.active, self.known = None, True
                return turn.id
            case harness_session.TurnUpdatedEvent(turn=turn):
                # As the session's state does: an update says whether its turn runs. A turn runs
                # until it terminates, also with a status a newer host added.
                self.active = turn.id if turn.status != "terminated" else None
                self.known = True
                return turn.id
            case harness_session.CallbackOpenedEvent(callback=callback):
                owner = callback_turn_id(callback)
                self._callbacks[callback.id] = owner
                return owner
            case harness_session.CallbackResolvedEvent(callback_id=callback_id, turn_id=turn_id):
                opened = self._callbacks.pop(callback_id, None)
                # Which reader gives it: an older host does not name the turn on the resolution.
                # TODO: drop `opened or self.active`, and `_callbacks` with it, once every host names the
                # turn on callback_resolved (Agent Controller and Harness of this release deployed).
                return turn_id or opened or self.active
            case (
                harness_session.HistoryEntryAddedEvent(entry=entry)
                | harness_session.HistoryEntryCompletedEvent(entry=entry)
            ):
                if _writing(entry):
                    self.streams[entry.id] = entry.turn_id
                else:
                    self.streams.pop(entry.id, None)
                # The host writes the turn an entry belongs to: every read gives the same one.
                return entry.turn_id if entry.turn_id is not None else self.active
            case harness_session.HistoryEntryPatchedEvent(entry_id=entry_id) if entry_id in self.streams:
                return self.streams[entry_id] or self.active
            case _:
                return self.active


def _writing(entry: harness_session.HistoryEntry) -> bool:
    """Whether ``entry`` is a message the model is still writing: its patches add its text."""
    return (
        isinstance(entry, harness_session.MessageHistoryEntry)
        and entry.role == "assistant"
        and entry.generation_status == "generating"
    )


def _event(
    event: harness_session.Event, turn_id: str | None, tools: Mapping[str, _Tool], turns: _Turns
) -> tuple[Event, ...]:
    """The typed events for ``event``, in order: none, one, or two for an entry's change."""
    match event.payload:
        case harness_session.HistoryEntryCompletedEvent(entry=harness_session.NoticeHistoryEntry()):
            # Given as a Notice when added.
            return ()
        case harness_session.HistoryEntryAddedEvent(entry=entry) if not isinstance(
            entry, harness_session.NoticeHistoryEntry
        ):
            return _added(event, entry, turn_id)
        case harness_session.HistoryEntryCompletedEvent(entry=entry):
            return (
                EntryCompleted(
                    id=event.event_id, session_id=event.session_id, turn_id=entry.turn_id, entry=_entry(entry)
                ),
            )
        case _:
            typed = _other_event(event, turn_id, tools, turns.streams)
            return () if typed is None else (typed,)


def _added(event: harness_session.Event, entry: harness_session.HistoryEntry, turn_id: str | None) -> tuple[Event, ...]:
    """An entry added: its :class:`EntryAdded`, then a message's first text."""
    added = EntryAdded(id=event.event_id, session_id=event.session_id, turn_id=entry.turn_id, entry=_entry(entry))
    if not _writing(entry):
        return (added,)
    # The message's first text: the rest comes as patches, the whole as its completed entry.
    delta = _delta(event, turn_id, entry.id, _text(entry.content))
    return (added,) if delta is None else (added, delta)


def _other_event(
    event: harness_session.Event,
    turn_id: str | None,
    tools: Mapping[str, _Tool],
    streams: Mapping[str, str | None],
) -> Event | None:
    """The typed event for ``event``, not an entry's addition or completion, or ``None``.
    ``streams`` has the IDs of the messages the model is writing: a patch of one of them is a
    :class:`TextDelta`."""
    base = {"id": event.event_id, "session_id": event.session_id, "turn_id": turn_id}
    match payload := event.payload:
        case harness_session.TurnStartedEvent():
            return TurnStarted(**base)
        case harness_session.CallbackOpenedEvent(callback=callback):
            return CallbackOpened(**base, callback=open_callback(callback, event.session_id, tools))
        case harness_session.CallbackResolvedEvent(callback_id=callback_id, turn_id=resolved_turn_id):
            # The turn the host names on the resolution, wherever the read started: none from an older host.
            return CallbackResolved(**{**base, "turn_id": resolved_turn_id}, callback_id=callback_id)
        case harness_session.HistoryEntryAddedEvent(entry=harness_session.NoticeHistoryEntry() as entry):
            # The host writes the turn it belongs to, so every read gives the same one.
            return Notice(
                **{**base, "turn_id": entry.turn_id},
                message=entry.message,
                level=read_value(entry.level, "Notice.level"),
                source=_source(entry.details),
                details=entry.details,
            )
        case harness_session.HistoryEntryPatchedEvent(entry_id=entry_id, patches=patches) if entry_id in streams:
            return _delta(event, turn_id, entry_id, "".join(_added_text(patch) for patch in patches))
        case harness_session.TurnUpdatedEvent(turn=turn):
            return TurnUpdated(**{**base, "turn_id": turn.id}, status=read_value(turn.status, "TurnUpdated.status"))
        case harness_session.SessionUpdatedEvent(session=session):
            # The session's state names no turn: the event belongs to none, wherever it is read from.
            return SessionUpdated(
                **{**base, "turn_id": None},
                status=read_value(session.status, "SessionUpdated.status"),
                title=session.title,
                archived=session.archived_at is not None,
            )
        case harness_session.UnknownEventPayload(original_type=event_type, raw=raw) if event_type not in _KNOWN_TYPES:
            # This SDK does not know the type's fields, so not its turn either: ``raw`` has them.
            return UnknownEvent(**{**base, "turn_id": None}, type=event_type, raw=raw)
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


def _entry(entry: harness_session.HistoryEntry) -> Entry:
    """The SDK's entry for the host's: an :class:`UnknownEntry` for one this SDK does not type."""
    match entry:
        case harness_session.MessageHistoryEntry():
            return message_entry(entry)
        case harness_session.CapabilityContextMessageHistoryEntry() | harness_session.InputContextMessageHistoryEntry():
            return context_message(entry)
        case harness_session.ToolCallHistoryEntry():
            return tool_call_entry(entry)
        case harness_session.ToolResultHistoryEntry():
            return tool_result_entry(entry)
        case _:
            return unknown_entry(entry)


def _delta(event: harness_session.Event, turn_id: str | None, entry_id: str, text: str) -> TextDelta | None:
    if not text:
        return None
    return TextDelta(id=event.event_id, session_id=event.session_id, turn_id=turn_id, entry_id=entry_id, text=text)


def _text(content: Iterable[harness_session.ContentBlock]) -> str:
    return "".join(block.text for block in content if isinstance(block, harness_session.TextContentBlock))


def _added_text(patch: harness_session.JsonPatchOperation) -> str:
    """The text a patch of a message being written adds: appended to a text block, or a new text block.

    Any other change, such as a new ``updatedAt``, adds no text.
    """
    match patch:
        case harness_session.JsonPatchAppendOperation(path=path, value=str(text)) if _TEXT_PATH.fullmatch(path):
            return text
        case harness_session.JsonPatchAddOperation(path=path, value={"type": "text", "text": str(text)}) if (
            _BLOCK_PATH.fullmatch(path)
        ):
            return text
        case _:
            return ""


# A text block of a message's content, and a new block of it.
_TEXT_PATH = re.compile(r"/content/\d+/text")
_BLOCK_PATH = re.compile(r"/content/(\d+|-)")


def _source(details: JsonValue) -> str | None:
    match details:
        case {"source_id": str(source)}:
            return source
        case _:
            return None


def _events(item: harness_session.ClientTransportStreamItem) -> Iterable[harness_session.Event]:
    match item:
        case harness_session.EventBatch(events=events):
            return events
        case harness_session.Event():
            return (item,)
        case _:
            return ()
