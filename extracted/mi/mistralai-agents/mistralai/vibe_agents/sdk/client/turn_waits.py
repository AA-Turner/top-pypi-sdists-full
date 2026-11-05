"""Wait for a turn without ever changing it: read its record, then follow the session's events
and the open callbacks of its subagents.

A wait sends reads only. However it ends (its own ``timeout``, a cancel, a lost event stream), the
turn goes on on the host.
"""

from __future__ import annotations

import asyncio
import contextlib
import dataclasses
from collections.abc import AsyncGenerator, AsyncIterator, Callable, Iterable, Mapping
from typing import Any

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.app_server.session import SessionClient as _RawSession
from mistralai.vibe.harness.app_server.session import SessionTransport
from mistralai.vibe_agents.sdk.client.approval_requests import NO_TOOLS, _Tool
from mistralai.vibe_agents.sdk.client.approvals import Approvals, cancel
from mistralai.vibe_agents.sdk.client.events import (
    CallbackOpened,
    Event,
    EventHandler,
    TurnEnded,
    active_turn_at,
    deliver,
    ended_record,
    follow,
    up_to,
    up_to_end,
)
from mistralai.vibe_agents.sdk.client.loop_wake import waking
from mistralai.vibe_agents.sdk.client.records import (
    Blocked,
    ObservationLost,
    OpenCallback,
    OpenClientToolCall,
    Running,
    TurnState,
)
from mistralai.vibe_agents.sdk.client.turn_reads import read_turn, read_turn_and_start
from mistralai.vibe_agents.sdk.transport.client_tools import (
    NO_CLIENT_TOOLS,
    ClientToolRegistry,
    left_open,
    watching_left_open,
)

__all__ = ["WaitBudget", "wait_for_turn"]


class WaitBudget:
    """The time a wait may wait for the host: ``timeout`` seconds, but not while it is paused.

    The caller pauses it while its own code answers one of the turn's calls, a client tool's, so
    that time does not count. The clock starts with the wait: a run's start does not count either.
    """

    def __init__(self, timeout: float | None) -> None:
        self._loop = asyncio.get_running_loop()
        self._left = timeout
        self._started = False
        self._paused = False
        # When the clock last started running; meaningful only while it runs.
        self._since = 0.0
        self._deadlines: set[asyncio.Timeout] = set()

    def _running(self) -> bool:
        return self._left is not None and self._started and not self._paused

    def remaining(self) -> float | None:
        if self._left is None or not self._running():
            return self._left
        return max(0.0, self._left - (self._loop.time() - self._since))

    def when(self) -> float | None:
        return self._since + self._left if self._left is not None and self._running() else None

    def start(self) -> None:
        if not self._started:
            self._started = True
            self._since = self._loop.time()

    def pause(self, paused: bool) -> None:
        if paused == self._paused:
            return
        if self._running():
            self._left = self.remaining()
        self._paused = paused
        self._since = self._loop.time()
        for deadline in self._deadlines:
            if not deadline.expired():
                deadline.reschedule(self.when())

    def spent(self) -> bool:
        return self._running() and self.remaining() == 0.0

    @contextlib.asynccontextmanager
    async def bounding(self) -> AsyncIterator[asyncio.Timeout]:
        """Bound a block by the budget, moving its deadline as the budget pauses and goes on."""
        async with asyncio.timeout_at(self.when()) as deadline:
            self._deadlines.add(deadline)
            try:
                yield deadline
            finally:
                self._deadlines.discard(deadline)


# How long a wait waits before it reads the turn again when the host lists a callback that opened
# and the read does not show it yet. Each later try waits twice as long, up to
# ``_LAGGED_READ_MAX_SECONDS``.
_LAGGED_READ_RETRY_SECONDS = 0.05
_LAGGED_READ_MAX_SECONDS = 1.0
# How long a wait reads the turn again for a callback that opened, when the host cannot list its
# open callbacks: past that, the wait takes the callback as answered.
_UNLISTED_OPENING_SECONDS = 3.0


class _Wait:
    """The position a wait starts after, and what it has read of the session's events since.

    A record and its ``cursor`` are the same position: the wait returns at a callback whose
    opening is among the events after it, and that the host still lists as open. The session's
    events do not carry its subagents' callbacks, so a position does not order them: the wait
    returns while one of them is open, except one that a ``Blocked`` record passed as ``after``
    lists.
    """

    def __init__(
        self,
        session_id: str,
        turn_id: str,
        after: TurnState[object] | str | None,
        approvals: Approvals | None = None,
        *,
        tools: Mapping[str, _Tool] = NO_TOOLS,
        client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
        confirmed: bool = False,
    ) -> None:
        self.session_id = session_id
        self.turn_id = turn_id
        # Whether the host confirmed the turn, as a start's or a send's answer does: a read that
        # does not list it yet says it runs (see ``read_turn_and_start``).
        self.confirmed = confirmed
        self.after = after is not None
        # The turn running at the last event the wait read (``seen``): another turn's record says
        # which turn runs at its position; its cursor alone does not.
        self.active = active_turn_at(after, turn_id)
        # A bare cursor does not say whether the turn still ran there.
        self.active_known = not isinstance(after, str)
        # The id of the last event the wait read.
        self.seen = after if after is None or isinstance(after, str) else after.cursor
        # Where the wait started reading: see ``position``.
        self.start = self.seen
        # Whether the wait read an event of its turn, or its record running: see ``position``.
        self.reached = False
        # After a record taken where the turn does not run, such as the previous turn's result, the
        # wait names the previous turn's start until it reads its turn: a cursor between the turns
        # would not say that no turn runs there. ``_read_from_start`` reads it.
        self.before = after is not None and not isinstance(after, str) and self.active != turn_id
        # The turn running at ``start``, and whether that is known: a wait that read nothing of its
        # turn reads again from ``start``, since ``active`` says nothing of the turns it read past.
        self.start_active, self.start_known = self.active, self.active_known
        # Whether the wait gave an event that names no turn, raised while no turn ran: ``seen`` is
        # before the turn's start, where no turn runs.
        self.gap = False
        # The subagents' callbacks the caller has: those a Blocked record passed as ``after`` lists.
        self.listed = frozenset(
            (callback.session_id, callback.id)
            for callback in (after.callbacks if isinstance(after, Blocked) else ())
            if callback.session_id != session_id
        )
        # The ``(session_id, callback_id)`` of the callbacks that opened after the position.
        self.opened: set[tuple[str, str]] = set()
        # An approval that a handler answers is not a reason to return.
        self.approvals = approvals
        # The agent's tool objects by tool id, for the requests of approvals.
        self.tools = tools
        # The client tools, by the name the host gives them, that a client attached in this process
        # answers in the session tree: like an approval the handler answers, a call of one is not a
        # reason to return.
        self.client_tools = client_tools
        # Whether ``on_event`` has an event now: a wait that starts again lets it finish first.
        self.delivering = False
        self.delivered = asyncio.Event()

    def position(self) -> str | None:
        """Where a caller resumes: ``seen``, or ``start`` until the wait read its turn running.

        A position read before the turn's start, in the previous turn or after it, would not say
        which turn ran there: a reader after it would take the events there as this turn's.
        """
        return self.seen if self.reached else self.start

    def note(self, cursor: str, event: Event | None) -> None:
        """Note that the wait read up to ``cursor``, ``event`` there."""
        self.seen = cursor
        if event is None:
            return
        if event.turn_id == self.turn_id or self.active == self.turn_id:
            # An event of the turn, or one that names no turn, such as a SessionUpdated, given while
            # the turn runs: it still runs there.
            self.active, self.active_known, self.reached = self.turn_id, True, True
        elif event.turn_id is None and not self.reached:
            # An event that names no turn, given before the turn's start: no turn runs there.
            self.active, self.active_known, self.gap = None, True, True

    def returns(self, state: TurnState[str]) -> bool:
        """Whether a wait returns this record: the turn ended, or it waits on a callback that opened
        and that no handler answers."""
        if isinstance(state, Blocked):
            return any(
                (callback.session_id, callback.id) in self.opened and not self._answered(callback)
                for callback in state.callbacks
            )
        return _ended(state)

    def returns_at_first_read(self, state: TurnState[str]) -> bool:
        """Whether the wait's first read returns this ``Blocked``: without ``after``, any callback
        that no handler answers; after a position, as ``returns``. A wait that starts again after a
        handler left an approval open has it among ``opened``, or reads its opening next."""
        if isinstance(state, Blocked) and not self.after:
            return any(not self._answered(callback) for callback in state.callbacks)
        return isinstance(state, Blocked) and self.returns(state)

    def _answered(self, callback: OpenCallback) -> bool:
        if isinstance(callback, OpenClientToolCall):
            # The caller's client answers the client tools of the whole tree, its subagents' too, but
            # not a provided tool's call, such as the connector sign-in: that one returns. One its
            # answer left open with agents.KeepCallbackOpen() is not answered.
            registry = self.client_tools
            return registry.covers(callback.call.name) and not left_open(registry, callback.session_id, callback.id)
        return self.approvals is not None and self.approvals.answers(callback.kind, callback.session_id, callback.id)


def _ended(state: TurnState[str]) -> bool:
    return not isinstance(state, Running | Blocked)


async def wait_for_turn(
    raw: _RawSession,
    transport: SessionTransport,
    session_id: str,
    turn_id: str,
    *,
    after: TurnState[object] | str | None,
    timeout: float | WaitBudget | None,
    on_event: EventHandler | None = None,
    start: str | None = None,
    approvals: Approvals | None = None,
    tools: Mapping[str, _Tool] = NO_TOOLS,
    client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
    confirmed: bool = False,
) -> TurnState[str]:
    """Return the turn's record at its end, or at a callback opened after ``after``.

    ``raw`` and the event stream share ``transport``; ``tools`` are the agent's tool objects by tool
    id. Without ``after``, the first read returns any ``Blocked``. After a position, a callback of
    the turn whose opening the events show wakes the wait, and the wait returns only if the host
    still lists it as open: one another client already answered does not. A subagent's callback
    returns while open, unless a ``Blocked`` given as ``after`` lists it. ``timeout`` bounds the
    first read and the wait; one more read then returns the record as the host has it. A
    ``WaitBudget`` bounds them by the time spent waiting for the host only.

    ``on_event`` gets the turn's events after ``after`` up to the record returned, at the timeout
    too: without ``after``, after ``start`` (the previous turn's start, read before this turn
    started), else from the previous turn's start position the host recorded, else from the
    session's start: the events that name no turn since the previous turn's end are this
    turn's. They are read up to
    the record's position with no time limit. The record's ``cursor`` is the position they reached.
    With ``approvals``, which the caller serves while the call waits, a ``Blocked`` returns only on a
    callback its handler does not answer, or an approval it leaves open. A client tool call
    that ``client_tools`` answers, by its answers or its ``on_client_tool``, does not return
    either: a client attached in this process answers it, in the session or its subagents. One
    whose answer returned ``agents.KeepCallbackOpen()`` does.

    A ``confirmed`` turn, one a start or a send returned, that the host's read does not list yet
    is followed as running: a deployment answers the start before its read lists the turn. Such a
    turn the host never lists is waited for until ``timeout``, or the session's end.

    Raises:
        TurnNotFoundError: The session has no turn with this id, and it is not ``confirmed``.
        ObservationLost: The session's events, or its subagents' callbacks, could not be read, and
            the turn has not ended.
        Exception: The approval handler raised this error; its approval stays open.
    """
    wait = _Wait(session_id, turn_id, after, approvals, tools=tools, client_tools=client_tools, confirmed=confirmed)
    if on_event is not None and start is not None and after is None:
        wait.seen = wait.start = start
    # A notebook's stop must land while the turn is quiet: see ``waking``.
    budget = timeout if isinstance(timeout, WaitBudget) else WaitBudget(timeout)
    budget.start()
    with waking():
        if approvals is None and not client_tools:
            return await _wait_for_turn(raw, transport, wait, after=after, budget=budget, on_event=on_event)
        with watching_left_open(client_tools) as left:
            return await _wait_answering(
                raw, transport, wait, approvals, left, after=after, budget=budget, on_event=on_event
            )


async def _wait_answering(
    raw: _RawSession,
    transport: SessionTransport,
    wait: _Wait,
    approvals: Approvals | None,
    left: asyncio.Event,
    *,
    after: TurnState[object] | str | None,
    budget: WaitBudget,
    on_event: EventHandler | None,
) -> TurnState[str]:
    """Wait as ``_wait_for_turn`` does while the handlers answer approvals and client tool calls.

    When the approval handler leaves an approval open, or an answer leaves a client tool call open
    (``left`` is set), the wait starts again from the position it reached, within the same budget,
    so it returns ``Blocked`` on that callback. When the approval handler raises, the wait stops and
    raises its error.
    """
    while True:
        waiting = asyncio.ensure_future(
            _wait_for_turn(raw, transport, wait, after=after, budget=budget, on_event=on_event)
        )
        changes = [asyncio.ensure_future(_set_and_cleared(left))]
        if approvals is not None:
            changes.append(asyncio.ensure_future(approvals.changed()))
        try:
            await asyncio.wait({waiting, *changes}, return_when=asyncio.FIRST_COMPLETED)
            # Start again between two events, so that ``on_event`` gets each one once, in full.
            while wait.delivering and not waiting.done():
                wait.delivered.clear()
                await wait.delivered.wait()
        finally:
            await cancel(*changes, *(() if waiting.done() else (waiting,)))
        if approvals is not None:
            approvals.raise_error()
        if not waiting.cancelled():
            return waiting.result()


async def _set_and_cleared(event: asyncio.Event) -> None:
    await event.wait()
    event.clear()


async def _wait_for_turn(
    raw: _RawSession,
    transport: SessionTransport,
    wait: _Wait,
    *,
    after: TurnState[object] | str | None,
    budget: WaitBudget,
    on_event: EventHandler | None,
) -> TurnState[str]:
    turn_id = wait.turn_id
    if not budget.spent():
        deadline: asyncio.Timeout | None = None
        try:
            async with budget.bounding() as deadline:
                state = await _read_from_start(raw, wait, on_event=on_event)
                # Without ``after``, the first read returns any ``Blocked`` (on a callback no handler answers).
                target = state if isinstance(state, Blocked) and wait.returns_at_first_read(state) else None
                if on_event is None:
                    if target is not None or _ended(state):
                        return state
                    if after is None:
                        wait.seen, wait.active, wait.reached = state.cursor, turn_id, True
                    return await _follow(raw, transport, wait)
                if isinstance(state, Running | Blocked):
                    return await _follow(raw, transport, wait, on_event=on_event, target=target)
                if not ended_record(after, turn_id):
                    await _up_to_end(raw, transport, wait, state, on_event=on_event)
                return state
        except TimeoutError:
            if deadline is None or not deadline.expired():
                raise
    # The wait ran out: return the turn's record now. Nothing is sent to the host.
    state = await _read_from_start(raw, wait, on_event=on_event)
    if on_event is None or state.cursor in (None, wait.seen) or ended_record(after, turn_id):
        return state
    return await _catch_up(raw, transport, wait, state, on_event=on_event)


async def _read_from_start(raw: _RawSession, wait: _Wait, *, on_event: EventHandler | None) -> TurnState[str]:
    """Read the turn. A handler with no position yet gets the turn's events from the previous turn's start.

    Without one recorded, the events are read from the session's start, and the other turns' are skipped.
    """
    if wait.before:
        state, wait.start = await read_turn_and_start(
            raw, wait.session_id, wait.turn_id, tools=wait.tools, confirmed=wait.confirmed
        )
        # Once read: a read cut short by the deadline is made again.
        wait.before = False
        # The previous turn's start: no turn runs there.
        wait.start_active, wait.start_known = None, True
        return state
    if on_event is None or wait.seen is not None:
        return await read_turn(raw, wait.session_id, wait.turn_id, tools=wait.tools, confirmed=wait.confirmed)
    state, start = await read_turn_and_start(
        raw, wait.session_id, wait.turn_id, tools=wait.tools, confirmed=wait.confirmed
    )
    wait.seen = wait.start = start
    return state


async def _follow(
    raw: _RawSession,
    transport: SessionTransport,
    wait: _Wait,
    *,
    on_event: EventHandler | None = None,
    target: Blocked | None = None,
) -> TurnState[str]:
    """Follow the turn's events after ``wait.seen`` until a record returns.

    The turn is read again when one of its callbacks opens, or one of its subagents', and the host
    still lists it as open: one another client answered first needs no read. With
    ``on_event``, a ``Blocked`` that returns, read already (``target``) or now, returns once the
    events up to its position were given; an end read now returns at its ``TurnEnded``, with no
    read again. The events' stream ending ends the wait; the subagents' list ending does not.
    Once a ``Blocked`` returns, the subagents are no longer watched: losing their list then cannot
    raise ``ObservationLost`` in place of it.
    """
    ends: dict[str, TurnState[str]] = {}
    async with (
        contextlib.aclosing(_events(raw, transport, wait, ends=ends)) as events,
        # ``target`` is read at each item: the watch stops once it is set.
        contextlib.aclosing(_with_subagents(events, transport, wait, watching=lambda: target is None)) as items,
    ):
        if target is None:
            async for item in items:
                if isinstance(item, frozenset):
                    opened = item  # Subagents' callbacks opened.
                else:
                    cursor, event = item
                    if (state := await _take(wait, on_event, cursor, event)) is not None:
                        return state
                    if not isinstance(event, CallbackOpened):
                        continue
                    opened = frozenset({(event.callback.session_id, event.callback.id)})
                wait.opened.update(opened)
                if (state := await _read_opened(raw, wait, opened)) is None:
                    continue  # Answered already: the host no longer lists it.
                if on_event is None and wait.returns(state):
                    return state
                if isinstance(state, Blocked) and wait.returns(state):
                    target = state
                    break
                if _ended(state):
                    ends[wait.turn_id] = state  # Its TurnEnded needs no second read.
            else:
                # The stream ended: the session may have ended with the turn.
                if _ended(
                    state := await read_turn(
                        raw, wait.session_id, wait.turn_id, tools=wait.tools, confirmed=wait.confirmed
                    )
                ):
                    return state
                raise ObservationLost(wait.session_id, wait.position())
        # The next leg reads after the record's position: give every event up to it first.
        if wait.seen != target.cursor:
            stream = _only_events(items)
            async with contextlib.aclosing(up_to(stream, target.cursor)) as caught:
                async for cursor, event in caught:
                    if (state := await _take(wait, on_event, cursor, event)) is not None:
                        return state
    return _read_to(wait, target)


async def _with_subagents(
    events: AsyncGenerator[tuple[str, Event | None]],
    transport: SessionTransport,
    wait: _Wait,
    *,
    watching: Callable[[], bool],
) -> AsyncGenerator[tuple[str, Event | None] | frozenset[tuple[str, str]]]:
    """Yield the items of ``events`` and, while ``watching()``, the subagents' callbacks that opened.

    An event is read while the caller waits for the next item, and, after the callbacks, while the
    caller reads the turn: if the turn ends then, ``follow`` may read the turn once more.
    An error of the subagents' list raises ``ObservationLost`` at ``wait.position()``, the events after
    it not taken yet. Once ``watching()`` is false, at the caller's next item, the list is closed
    and its error, if any, dropped. This ends with ``events``; the subagents' list ending does not.
    """
    subagents = _subagent_changes(transport, wait) if watching() else None
    next_event: asyncio.Future[tuple[str, Event | None]] | None = None
    next_change: asyncio.Future[frozenset[tuple[str, str]]] | None = None
    try:
        while True:
            if subagents is not None and not watching():
                await _cancel(next_change)
                await subagents.aclose()
                subagents = next_change = None
            if next_event is None:
                next_event = asyncio.ensure_future(anext(events))
            if next_change is None and subagents is not None:
                next_change = asyncio.ensure_future(anext(subagents))
            pending: set[asyncio.Future[Any]] = {next_event} if next_change is None else {next_event, next_change}
            done, _ = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            # The subagents' change first: on an error, the events not taken yet come after it.
            if next_change is not None and next_change in done:
                change, next_change = next_change, None
                try:
                    opened = change.result()
                except StopAsyncIteration:
                    subagents = None
                except harness_session.SessionEventStreamLostError as error:
                    raise ObservationLost(wait.session_id, wait.position()) from error
                else:
                    if opened:
                        yield opened
            if next_event in done:
                event, next_event = next_event, None
                try:
                    item = event.result()
                except StopAsyncIteration:
                    return
                yield item
    finally:
        await _cancel(next_event, next_change)
        if subagents is not None:
            await subagents.aclose()


async def _cancel(*reads: asyncio.Future[Any] | None) -> None:
    """Cancel the pending reads, dropping their results or errors."""
    pending = [read for read in reads if read is not None]
    for read in pending:
        read.cancel()
    await asyncio.gather(*pending, return_exceptions=True)


async def _only_events(
    items: AsyncIterator[tuple[str, Event | None] | frozenset[tuple[str, str]]],
) -> AsyncGenerator[tuple[str, Event | None]]:
    """The items of ``_with_subagents`` that are events."""
    async for item in items:
        if not isinstance(item, frozenset):
            yield item


async def _subagent_changes(transport: SessionTransport, wait: _Wait) -> AsyncGenerator[frozenset[tuple[str, str]]]:
    """Yield, for each list of the open callbacks of the session tree, the subagents' that opened.

    The first list counts every subagent callback as opened but those ``wait.listed`` has: the
    session's events do not order them. A host that cannot follow the tree yields nothing: the
    wait sees the turn's own callbacks only, as its read does.
    """
    params = harness_session.CallbacksTreeParams(session_id=wait.session_id)
    before = wait.listed
    try:
        trees = transport.watch_callbacks_tree(params)
        async with contextlib.aclosing(trees) as stream:  # type: ignore[type-var]
            async for tree in stream:
                now = {
                    (item.session_id, item.callback.id) for item in tree.callbacks if item.session_id != wait.session_id
                }
                yield frozenset(now - before)
                before = frozenset(now)
    except harness_session.UnsupportedSessionProcedureError:
        return


async def _read_opened(raw: _RawSession, wait: _Wait, opened: frozenset[tuple[str, str]]) -> TurnState[str] | None:
    """Read the turn after callbacks ``opened``; ``None`` when the host no longer lists any of them.

    The host's open callbacks can list a callback of the turn before the session read does, and no
    later event asks for another read of a callback that stays open: while the host lists one of the
    turn's own and the read does not show it, read again. A host that cannot list them cannot tell
    a lagged read from an answered callback: read again for ``_UNLISTED_OPENING_SECONDS`` at most.
    A subagent's callback is not retried: the read takes it from the same list. The wait's
    ``timeout`` bounds the reads.
    """
    delay = _LAGGED_READ_RETRY_SECONDS
    unlisted_until = asyncio.get_running_loop().time() + _UNLISTED_OPENING_SECONDS
    while True:
        listed = await _still_open(raw, wait, opened)
        if listed is not None and not listed:
            return None
        state = await read_turn(raw, wait.session_id, wait.turn_id, tools=wait.tools, confirmed=wait.confirmed)
        if _ended(state) or (isinstance(state, Blocked) and _lists(state, opened)):
            return state
        if listed is None:
            if asyncio.get_running_loop().time() >= unlisted_until:
                return state
        elif not _the_turns(wait, listed):
            return state
        await asyncio.sleep(delay)
        delay = min(delay * 2, _LAGGED_READ_MAX_SECONDS)


def _lists(state: Blocked, opened: frozenset[tuple[str, str]]) -> bool:
    return any((callback.session_id, callback.id) in opened for callback in state.callbacks)


def _the_turns(wait: _Wait, listed: Iterable[harness_session.TreeCallback] | None) -> bool:
    """Whether ``listed`` has a callback of the session's own that is the waited turn's."""
    return any(item.session_id == wait.session_id and item.callback.turn_id == wait.turn_id for item in listed or ())


async def _still_open(
    raw: _RawSession, wait: _Wait, opened: frozenset[tuple[str, str]]
) -> tuple[harness_session.TreeCallback, ...] | None:
    """The callbacks that ``opened`` and that the host still lists as open: one read of the session
    tree's open callbacks, not of the session.

    ``None`` from a host that cannot list the tree: the turn's read tells.
    """
    try:
        tree = await raw.request(
            "app_server/session/callbacks/tree",
            harness_session.CallbacksTreeParams(session_id=wait.session_id),
            harness_session.CallbacksTreeResponse,
        )
    except harness_session.UnsupportedSessionProcedureError:
        return None
    return tuple(item for item in tree.callbacks if (item.session_id, item.callback.id) in opened)


async def _up_to_end(
    raw: _RawSession,
    transport: SessionTransport,
    wait: _Wait,
    state: TurnState[str],
    *,
    on_event: EventHandler | None,
    reconnect: bool = True,
) -> None:
    """Give the events of the turn that ended, ``state`` its record, after ``wait.seen``, as ``up_to_end`` does.

    ``up_to_end`` raises ``ObservationLost`` before it gives any event: at ``wait.position()``.
    """
    events = _events(raw, transport, wait, ends={wait.turn_id: state}, reconnect=reconnect)
    try:
        async for event in up_to_end(events, after=wait.seen, state=state):
            wait.note(event.id, event)
            await _deliver(wait, on_event, event)
    except ObservationLost as error:
        raise ObservationLost(wait.session_id, wait.position()) from error.__cause__


async def _catch_up(
    raw: _RawSession, transport: SessionTransport, wait: _Wait, state: TurnState[str], *, on_event: EventHandler
) -> TurnState[str]:
    """Give the turn's events after ``wait.seen`` up to ``state``'s position; return the record then.

    They are read, as ``_read_to`` says, up to that position or the stream's end. The record is
    the turn's state here: a turn's end it does not show yet is not read again. A stream that fails
    is not reconnected: the wait raises ``ObservationLost``.
    """
    if _ended(state):
        await _up_to_end(raw, transport, wait, state, on_event=on_event, reconnect=False)
        return state
    async with (
        contextlib.aclosing(_events(raw, transport, wait, reconnect=False, reread=False)) as stream,
        contextlib.aclosing(up_to(stream, state.cursor)) as items,
    ):
        async for cursor, event in items:
            if (ended := await _take(wait, on_event, cursor, event)) is not None:
                return ended
    return _read_to(wait, state)


def _read_to(wait: _Wait, state: TurnState[str]) -> TurnState[str]:
    """``state`` at the position the handler's events reached, if short of its own.

    ``up_to`` can stop before the record's position, at the stream's end: the next leg, after the
    record returned, then neither repeats nor misses an event. Short of it with no position to
    name, read from the session's start, the wait raises ``ObservationLost`` with no cursor.
    """
    position = wait.position()
    if wait.seen == state.cursor or position == state.cursor:
        return state
    if position is None:
        # Read from the session's start and short of the turn's start: a resume after the record
        # would miss the notices before it.
        raise ObservationLost(wait.session_id, None)
    return dataclasses.replace(state, cursor=position)


def _events(
    raw: _RawSession,
    transport: SessionTransport,
    wait: _Wait,
    *,
    ends: Mapping[str, TurnState[str]] | None = None,
    reconnect: bool = True,
    reread: bool = True,
) -> AsyncGenerator[tuple[str, Event | None]]:
    """``follow`` the turn's events after ``wait.seen``.

    A wait that read nothing of its turn reads again from its start: it does not know which turn
    runs at ``seen``. It gave no event then.
    """
    if not (wait.reached or wait.gap):
        wait.seen, wait.active, wait.active_known = wait.start, wait.start_active, wait.start_known
    return follow(
        raw,
        transport,
        wait.session_id,
        after=wait.seen,
        start=wait.position(),
        active_turn_id=wait.active,
        active_known=wait.active_known,
        turn_id=wait.turn_id,
        ends=ends,
        reconnect=reconnect,
        reread=reread,
        tools=wait.tools,
        confirmed=wait.confirmed,
    )


async def _take(wait: _Wait, on_event: EventHandler | None, cursor: str, event: Event | None) -> TurnState[str] | None:
    """Give ``event`` and note it in ``wait``; the turn's record if it ended there."""
    wait.note(cursor, event)
    if event is not None:
        await _deliver(wait, on_event, event)
    if isinstance(event, TurnEnded):
        return event.state
    return None


async def _deliver(wait: _Wait, on_event: EventHandler | None, event: Event) -> None:
    wait.delivering = True
    try:
        await deliver(on_event, event)
    finally:
        wait.delivering = False
        wait.delivered.set()
