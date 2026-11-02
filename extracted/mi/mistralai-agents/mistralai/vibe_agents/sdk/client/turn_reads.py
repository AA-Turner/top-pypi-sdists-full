"""Read one turn from its host and build its record.

Two requests: the session (its active turn, its open callbacks, its most recent turns and its last
event id), then the turn's history entries. A turn older than the most recent turns costs one
``turns/list`` request per page before the history. The session's active turn costs one more: the
open callbacks of its subagents, from ``callbacks/tree``.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

from pydantic import BaseModel, ValidationError

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.app_server.session import SessionClient as _RawSession
from mistralai.vibe.harness.app_server.session import SessionTransport
from mistralai.vibe_agents.sdk.authoring.errors import TurnNotFoundError
from mistralai.vibe_agents.sdk.client.approval_requests import NO_TOOLS, _Tool, approval_request
from mistralai.vibe_agents.sdk.client.records import (
    Blocked,
    Completed,
    Failed,
    Interrupted,
    InvalidOutput,
    OpenApproval,
    OpenCallback,
    OpenClientToolCall,
    ProtocolError,
    Running,
    TurnState,
    UnknownOpenCallback,
)
from mistralai.vibe_agents.sdk.transport.client_tools import client_tool_call
from mistralai.vibe_agents.sdk.transport.results import parsed_output, turn_text, turn_tool_calls

__all__ = ["callback_turn_id", "open_callback", "read_turn", "read_turn_and_start", "typed"]

# The turns read with the session; an older turn is looked up with turns/list.
_RECENT_TURNS = 50
# Large pages: a deployment-backed host rebuilds the session from its events for every request.
_PAGE_LIMIT = 1000


async def read_turn(
    raw: _RawSession,
    session_id: str,
    turn_id: str,
    *,
    bind: Callable[[str], SessionTransport],
    tools: Mapping[str, _Tool] = NO_TOOLS,
) -> TurnState[str]:
    """Return the turn's state as of the session's last event id, read first.

    ``bind`` binds another session of the host by id: a subagent's, to read its running turn.
    ``tools`` are the agent's tool objects by tool id, for the requests of its open approvals.

    Raises:
        TurnNotFoundError: The session has no turn with this id.
    """
    state, _start = await read_turn_and_start(raw, session_id, turn_id, bind=bind, tools=tools)
    return state


async def read_turn_and_start(
    raw: _RawSession,
    session_id: str,
    turn_id: str,
    *,
    bind: Callable[[str], SessionTransport],
    tools: Mapping[str, _Tool] = NO_TOOLS,
) -> tuple[TurnState[str], str | None]:
    """Return what ``read_turn`` does, and the event id just before the turn's start.

    Reading the session's events after that id gives the turn's events from its start. It is
    ``None`` when the host does not record it, or has not reported the turn yet.

    Raises:
        TurnNotFoundError: The session has no turn with this id.
    """
    read = await raw.request(
        "app_server/session/read",
        harness_session.SessionReadParams(
            session_id=session_id,
            # Only the most recent turns; the history is read per turn below.
            history=harness_session.PageRequest(limit=1),
            turns=harness_session.PageRequest(limit=_RECENT_TURNS, direction="backward"),
        ),
        harness_session.SessionReadResponse,
    )
    state = read.state
    session = state.session
    turn = next((found for found in state.turns.items if found.id == turn_id), None) if state.turns else None
    if turn is None and state.active_turn_id != turn_id:
        if state.turns is not None and state.turns.next_cursor is None:
            raise TurnNotFoundError(session_id, turn_id)
        turn = await _find_turn(raw, session_id, turn_id)
    entries = await _turn_entries(raw, session_id, turn_id)
    base = {"session_id": session_id, "turn_id": turn_id, "cursor": read.last_event_id}
    start = None if turn is None else turn.started_after_event_id

    if turn is not None and turn.status == "terminated" and turn.termination is not None:
        termination = turn.termination
        ended_with_session = (
            session.status == "terminated" and turn.completed_at is not None and turn.completed_at >= session.updated_at
        )
    elif session.status == "terminated":
        # The host never reported how the turn ended, so it ended with its session, as the v1
        # projection records it: no turn of an ended session reads Running.
        termination = session.termination or harness_session.CancelledTermination()
        ended_with_session = True
    else:
        # The runtime never sets the turn status "blocked": an open callback says it.
        callbacks = await _blocking_callbacks(raw, state, session_id, turn_id, bind, tools)
        text = turn_text(None, entries)
        if callbacks:
            return Blocked(**base, text=text, callbacks=callbacks), start
        return Running(**base, text=text), start

    match termination:
        case harness_session.CompletedTermination():
            text = turn_text(termination, entries)
            return Completed[str](
                **base,
                text=text,
                output=text or "",
                stop_reason=termination.stop_reason,
                tool_calls=turn_tool_calls(entries),
            ), start
        case harness_session.CancelledTermination():
            # The hosts name a cause only for a limit: a turn that ended with its session was
            # cancelled with it, any other was interrupted.
            cause = termination.cause or ("cancelled" if ended_with_session else "interrupted")
            return Interrupted(**base, text=turn_text(termination, entries), cause=cause), start
        case _:
            return Failed(**base, text=turn_text(None, entries), error=protocol_error(termination.error)), start


def protocol_error(error: harness_session.ProtocolError) -> ProtocolError:
    """Return the SDK record of an error the host reported."""
    return ProtocolError(
        message=error.message,
        code=error.code,
        retryable=error.retryable,
        details=error.details if isinstance(error.details, dict) else None,
    )


def typed[M: BaseModel](state: TurnState[str], response_format: type[M]) -> TurnState[M | None]:
    """Return the record with a ``Completed`` output validated as JSON against ``response_format``.

    The rule is ``agent.run``'s: the output is ``None`` when the turn did not end ``"completed"``
    (its iteration limit, or a skip by a hook). An output that does not validate becomes
    ``InvalidOutput``, with the text in ``raw``. Other records have no output and are returned as
    they are.
    """
    if not isinstance(state, Completed):
        return state
    output: M | InvalidOutput | None
    if isinstance(state.output, InvalidOutput):
        output = state.output
    else:
        try:
            output = parsed_output(response_format, state.stop_reason, state.output)
        except ValidationError as error:
            output = InvalidOutput(raw=state.output, error=str(error))
    return Completed[M | None](
        session_id=state.session_id,
        turn_id=state.turn_id,
        cursor=state.cursor,
        text=state.text,
        output=output,
        stop_reason=state.stop_reason,
        tool_calls=state.tool_calls,
    )


async def _find_turn(raw: _RawSession, session_id: str, turn_id: str) -> harness_session.TurnState:
    cursor: str | None = None
    while True:
        page = (
            await raw.request(
                "app_server/session/turns/list",
                harness_session.SessionTurnsListParams(
                    session_id=session_id,
                    page=harness_session.PageRequest(cursor=cursor, limit=_PAGE_LIMIT, direction="backward"),
                ),
                harness_session.SessionTurnsListResponse,
            )
        ).page
        for turn in page.items:
            if turn.id == turn_id:
                return turn
        if page.next_cursor is None:
            raise TurnNotFoundError(session_id, turn_id)
        cursor = page.next_cursor


async def _turn_entries(raw: _RawSession, session_id: str, turn_id: str) -> list[harness_session.HistoryEntry]:
    entries: list[harness_session.HistoryEntry] = []
    cursor: str | None = None
    while True:
        page = (
            await raw.request(
                "app_server/session/history/list",
                harness_session.SessionHistoryListParams(
                    session_id=session_id,
                    turn_id=turn_id,
                    page=harness_session.PageRequest(cursor=cursor, limit=_PAGE_LIMIT, direction="forward"),
                ),
                harness_session.SessionHistoryListResponse,
            )
        ).page
        entries.extend(page.items)
        if page.next_cursor is None:
            return entries
        cursor = page.next_cursor


async def _blocking_callbacks(
    raw: _RawSession,
    state: harness_session.SessionState,
    session_id: str,
    turn_id: str,
    bind: Callable[[str], SessionTransport],
    tools: Mapping[str, _Tool],
) -> tuple[OpenCallback, ...]:
    """Return the open callbacks the turn waits on: its own, then its subagents'.

    A callback that names no turn is the active turn's. Every open callback of a subagent, at any
    depth, blocks the session's active turn, whichever turn started the subagent: the subagent's
    result joins the active turn. Each callback names the session and the turn that opened it: a
    subagent's callback names the subagent's own turn. A host that cannot list the session tree, such as a control plane
    older than its callbacks route, gives the turn's own callbacks only.
    """
    own = tuple(
        open_callback(callback, session_id, turn_id, tools)
        for callback in state.active_callbacks
        if callback.turn_id == turn_id or (callback.turn_id is None and state.active_turn_id == turn_id)
    )
    if state.active_turn_id != turn_id:
        return own
    try:
        tree = await raw.request(
            "app_server/session/callbacks/tree",
            harness_session.CallbacksTreeParams(session_id=session_id),
            harness_session.CallbacksTreeResponse,
        )
    except harness_session.UnsupportedSessionProcedureError:
        return own
    return own + tuple(
        [
            open_callback(
                item.callback, item.session_id, await callback_turn_id(item.callback, item.session_id, bind), tools
            )
            for item in tree.callbacks
            if item.session_id != session_id
        ]
    )


async def callback_turn_id(
    callback: harness_session.SessionCallback, session_id: str, bind: Callable[[str], SessionTransport]
) -> str:
    """The turn that opened ``callback``, of ``session_id``, the session that opened it.

    Hosts name it on every callback. For a host that does not, it is the session's running turn,
    which this reads through the session's own binding, ``bind(session_id)``: a deployed host's
    transport reads only the session it is bound to. A callback is open only while the turn that
    opened it runs. ``""`` when the session runs no turn any more.
    """
    if callback.turn_id is not None:
        return callback.turn_id
    async with _RawSession(bind(session_id)) as raw:
        read = await raw.request(
            "app_server/session/read",
            harness_session.SessionReadParams(session_id=session_id),
            harness_session.SessionReadResponse,
        )
    return read.state.active_turn_id or ""


def open_callback(
    callback: harness_session.SessionCallback, session_id: str, turn_id: str, tools: Mapping[str, _Tool] = NO_TOOLS
) -> OpenCallback:
    """The record of ``callback``: an approval's carries its request, with its tool object from
    ``tools``; a client tool call's carries the call ``on_client_tool`` gets."""
    turn_id = callback.turn_id or turn_id
    if isinstance(callback, harness_session.ApprovalCallback):
        return OpenApproval(
            id=callback.id,
            session_id=session_id,
            turn_id=turn_id,
            kind=callback.kind,
            title=callback.title,
            request=approval_request(callback, tools),
        )
    if isinstance(callback, harness_session.ClientToolCallback):
        return OpenClientToolCall(
            id=callback.id,
            session_id=session_id,
            turn_id=turn_id,
            kind=callback.kind,
            title=None,
            call=client_tool_call(callback),
        )
    return UnknownOpenCallback(
        id=callback.id,
        session_id=session_id,
        turn_id=turn_id,
        kind=callback.kind,
        title=None,
        raw=callback.model_dump(mode="json", by_alias=True),
    )
