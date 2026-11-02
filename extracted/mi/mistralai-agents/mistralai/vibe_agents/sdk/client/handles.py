"""Handles: a session or a turn named by its id, on the host that runs it.

A handle holds ids and the way to reach their host, and nothing the host reported. Getting one
sends no request, so it is never out of date: store the ids, and bind them again in any process
with ``agent.session(session_id)`` and ``session.turn(turn_id)``.

Sends return a value when the host refuses them for the session's state: ``Busy`` when
``start_turn`` cannot start a turn, ``TurnConflict`` when a turn command names a turn that is no
longer active, ``AlreadySettled`` or ``NotFound`` when an answer names a callback that is no longer
open or never was. ``send_message`` always returns a turn: it starts one or adds to the running one.
Reads return a record (``turn.get()`` returns a ``TurnState``), which can be out of date: read
again for a newer one. Waits return a record too (``turn.result()``, ``session.run()``), and
leaving one never changes the turn. ``iter_events`` reads the session's events and never changes
anything. With ``response_format=``, a wait validates the output of a ``Completed`` record against
that model, as ``agent.run`` does. Without it, reads and waits use the
``response_format`` of the Agent the handle came from: ``agent.start_session()`` and
``agent.session(id)`` keep it, and so do the session's turns. A subagent's handle has none. A
handle's ``on_approval`` handler answers approvals while a call waits on it.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator, Callable, Mapping
from pathlib import Path
from typing import Any, Protocol, overload

from pydantic import BaseModel, TypeAdapter, ValidationError

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.app_server.session import SessionClient as _RawSession
from mistralai.vibe.harness.app_server.session import SessionTransport
from mistralai.vibe.harness.app_server.session.file_upload import FileUploader
from mistralai.vibe.harness.app_server.session.models.content import (
    EmbeddedResourceContentBlock,
    ResourceLinkContentBlock,
)
from mistralai.vibe.harness.runtime.completion import CompletionProvider
from mistralai.vibe_agents.sdk.assembly import assemble
from mistralai.vibe_agents.sdk.authoring.errors import SdkError, public_errors, public_iter_errors
from mistralai.vibe_agents.sdk.client.approval_requests import NO_TOOLS, _Tool
from mistralai.vibe_agents.sdk.client.approvals import (
    AllowApproval,
    ApprovalHandler,
    Approvals,
    DenyApproval,
    answer_approval,
)
from mistralai.vibe_agents.sdk.client.content import UserContentLike, to_session_content
from mistralai.vibe_agents.sdk.client.events import (
    Event,
    EventHandler,
    active_turn_at,
    ended_record,
    follow,
    up_to_end,
)
from mistralai.vibe_agents.sdk.client.records import (
    AlreadySettled,
    Answered,
    Blocked,
    Busy,
    NotFound,
    Running,
    TurnConflict,
    TurnState,
)
from mistralai.vibe_agents.sdk.client.turn_reads import read_turn, read_turn_and_start, typed
from mistralai.vibe_agents.sdk.client.turn_waits import WaitBudget, wait_for_turn
from mistralai.vibe_agents.sdk.transport import local
from mistralai.vibe_agents.sdk.transport import remote as remote_transport
from mistralai.vibe_agents.sdk.transport.client_tools import NO_CLIENT_TOOLS, ClientToolRegistry
from mistralai.vibe_agents.sessions_client import IdempotencyKey

__all__ = ["Session", "Turn", "checked_idempotency_key", "left_wait_note"]


def left_wait_note(session_id: str, turn_id: str) -> str:
    """The note on a cancel that left a wait on the turn: the turn goes on, and how to stop it."""
    return (
        f"Left the wait: turn {turn_id} of session {session_id} goes on. To stop it: "
        f"await agent.session({session_id!r}).turn({turn_id!r}).interrupt()"
    )


_EMPTY_MESSAGE = "Turn messages must contain at least one content block"
_IDEMPOTENCY_KEY_ADAPTER: TypeAdapter[str] = TypeAdapter(IdempotencyKey)


class _SessionHost(Protocol):
    """Where a session runs. It reaches a session by id without asking the host first."""

    def bind(self, session_id: str) -> SessionTransport:
        """Return a transport bound to the session. It sends no request until it is used."""
        ...

    def uploader(self, session_id: str) -> FileUploader | None:
        """The uploader of the session's files, or ``None`` when the host takes no uploads."""
        ...

    async def send_started(
        self, raw: _RawSession, session_id: str, receipt: harness_session.MessageSendResponse
    ) -> bool | None:
        """Whether the send that gave ``receipt`` started its turn, or ``None`` when the host cannot tell."""
        ...


def _live_uploader(runtime: local._AgentsSdkLocalRuntime, session_id: str) -> FileUploader | None:
    """The uploader of a session the runtime holds, without reopening a saved one."""
    uploader = runtime._uploader_for(session_id)
    if uploader is None:
        # A session whose tree was closed has no uploader either: refuse it as closed, or as a
        # subagent's, as the uploader of a live tree does, rather than as unsupported.
        runtime._validate_session(session_id)
    return uploader


type Reassemble = Callable[[local._AgentsSdkLocalRuntime, str], assemble.AgentAssembly]


class _LocalHost:
    """The local runtime of an Agent bound with ``local_runtime()``, else the event loop's own.

    With ``reassemble``, which builds the session's Agent again for a runtime, a session that an
    earlier process saved through the runtime's ``journal_factory`` reopens on first use.
    """

    def __init__(
        self,
        runtime: local._AgentsSdkLocalRuntime | None,
        reassemble: Reassemble | None = None,
        completion_provider: CompletionProvider | None = None,
    ) -> None:
        self._runtime = runtime
        self._reassemble = reassemble
        self._completion_provider = completion_provider

    def bind(self, session_id: str) -> SessionTransport:
        runtime = self._resolved()
        reassemble = self._reassemble
        if reassemble is None:
            return runtime.bind_session(session_id)
        return runtime.bind_session(
            session_id,
            reassemble=lambda: reassemble(runtime, session_id),
            completion_provider=self._completion_provider,
        )

    def uploader(self, session_id: str) -> FileUploader | None:
        runtime = self._resolved()
        reassemble = self._reassemble
        if reassemble is not None and runtime.journals is not None and not runtime._knows(session_id):
            # A saved session reopens on its first request, and an upload can be that request.
            saved_id = session_id

            async def reopen_then_upload(
                session_id: str,
                source: str | Path | bytes | AsyncIterator[bytes],
                *,
                name: str | None,
                media_type: str | None,
            ) -> EmbeddedResourceContentBlock | ResourceLinkContentBlock:
                await runtime.reopen_saved(
                    saved_id,
                    lambda: reassemble(runtime, saved_id),
                    completion_provider=self._completion_provider,
                )
                # Nothing saved under the ID leaves it unknown: the live lookup refuses it as not found.
                uploader = _live_uploader(runtime, saved_id)
                if uploader is None:
                    raise harness_session.UnsupportedSessionProcedureError(
                        method="upload_file",
                        backend="local",
                        reason="File uploads are not available in the current configuration.",
                    )
                return await uploader(session_id, source, name=name, media_type=media_type)

            return reopen_then_upload
        return _live_uploader(runtime, session_id)

    def _resolved(self) -> local._AgentsSdkLocalRuntime:
        return self._runtime if self._runtime is not None else local._process_runtime()

    async def send_started(
        self, raw: _RawSession, session_id: str, receipt: harness_session.MessageSendResponse
    ) -> bool | None:
        # The turn's first history entry is the message that opened it. The message was taken
        # already, so a failed read leaves the answer unknown rather than failing the send.
        try:
            first = await raw.request(
                "app_server/session/history/list",
                harness_session.SessionHistoryListParams(
                    session_id=session_id,
                    turn_id=receipt.turn_id,
                    page=harness_session.PageRequest(limit=1, direction="forward"),
                ),
                harness_session.SessionHistoryListResponse,
            )
        except Exception:
            return None
        if not first.page.items:
            # The turn writes its opening message once its pre_agent_turn hook returns, so a turn
            # this send opened can have no entry yet.
            return None
        return first.page.items[0].id == receipt.message_entry_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _LocalHost):
            return NotImplemented
        # Two hosts without a bound runtime are equal, though each resolves the runtime of the
        # event loop it connects from. Session ids are UUIDs, so they name one session anyway.
        return self._runtime is other._runtime

    __hash__ = None  # type: ignore[assignment]


class _RemoteHost:
    """The control plane of a deployment-backed Agent."""

    def __init__(self, deployment: remote_transport.RemoteAgentDeployment) -> None:
        self._deployment = deployment

    def check(self, session_id: str) -> None:
        remote_transport._parse_remote_session_id(session_id)

    def bind(self, session_id: str) -> SessionTransport:
        return remote_transport._bind_remote_session(self._deployment, session_id)

    def uploader(self, session_id: str) -> FileUploader | None:
        del session_id
        # The control plane has no upload endpoint.
        return None

    async def send_started(
        self, raw: _RawSession, session_id: str, receipt: harness_session.MessageSendResponse
    ) -> bool | None:
        del raw, session_id
        # The worker names a turn a send opens, and the send's message entry, after the send's
        # command id; a send it adds to the running turn keeps that turn's id. This is the
        # worker's convention until the protocol reports it, and it needs no read, which would
        # lag behind the send.
        if not receipt.turn_id or not receipt.message_entry_id:
            return None
        return receipt.turn_id == receipt.message_entry_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _RemoteHost):
            return NotImplemented
        # A session is named by its id on its control plane, however its Agent was loaded.
        return _control_plane(self._deployment) == _control_plane(other._deployment)

    __hash__ = None  # type: ignore[assignment]


class Session:
    """A session, named by its id. Getting one sends no request.

    Get one with ``await agent.start_session()``, or bind a stored id with
    ``agent.session(session_id)``. Both keep the Agent's ``response_format`` for ``run``, and for the
    ``get`` and ``result`` of the session's turns.

    With ``on_approval``, a plain or async function, ``session.run`` and ``turn.result`` answer the
    approvals of the session and its subagents while they wait: the handler gets an
    ``ApprovalCallbackContext`` and an ``ApprovalRequest`` and returns ``AllowApproval``,
    ``DenyApproval``, or ``None`` to leave the approval open, so the wait returns ``Blocked`` on it.
    A handler that raises leaves the approval open, and the waiting call raises its error; the turn
    goes on. Nothing answers between calls.
    """

    __slots__ = ("_client_tools", "_host", "_id", "_on_approval", "_response_format", "_tools")

    def __init__(
        self,
        session_id: str,
        host: _SessionHost,
        *,
        on_approval: ApprovalHandler | None = None,
        response_format: type[BaseModel] | None = None,
    ) -> None:
        self._id = session_id
        self._host = host
        self._on_approval = on_approval
        self._response_format = response_format
        # The agent's tool objects by tool id, for the requests of approvals: set by the agent.
        self._tools: Mapping[str, _Tool] = NO_TOOLS
        # The client tools that a client attached in this process answers in the session tree: a
        # wait does not return on their calls. Set by ``agent.run``.
        self._client_tools: ClientToolRegistry = NO_CLIENT_TOOLS

    @property
    def id(self) -> str:
        """The session's id."""
        return self._id

    def turn(self, turn_id: str) -> Turn:
        """Return the handle of a turn of this session. Sends no request."""
        return Turn(self, turn_id)

    @public_errors
    async def send_message(self, content: UserContentLike, *, idempotency_key: str | None = None) -> Turn:
        """Send a message: the host starts a turn, or adds the message to the running one.

        ``turn.started`` says which: ``True`` for a new turn, ``False`` for the running one, and
        ``None`` when the host cannot tell.

        Raises ``agents.SessionBusyError`` when the host still cannot take the message after its retries;
        nothing was applied. The same ``idempotency_key`` returns the same turn; reusing it for
        another message raises ``SessionIdempotencyConflictError``.
        """
        message = checked_message(content)
        key = checked_idempotency_key(idempotency_key)
        async with self._connect() as raw:
            receipt = await raw.request(
                "app_server/session/message/send",
                harness_session.MessageSendParams(idempotency_key=key, session_id=self.id, message=message),
                harness_session.MessageSendResponse,
            )
            started = await self._host.send_started(raw, self.id, receipt)
        return Turn(self, receipt.turn_id, started=started)

    @public_errors
    async def start_turn(self, content: UserContentLike, *, idempotency_key: str | None = None) -> Turn | Busy:
        """Start a new turn. Returns ``Busy``, with the running turn in ``busy.turn``, when one is active.

        The ``idempotency_key`` names the start: the same key returns the turn that key started,
        even with another message. A retry with a key refused with ``Busy`` starts a turn once the
        running one ends. A start never joins a running turn, so ``turn.started`` is ``True``.

        Raises ``SessionBusyError`` when the session cannot take a start for another reason, such
        as a limit on running subagents; nothing was applied.
        """
        message = checked_message(content)
        key = checked_idempotency_key(idempotency_key)
        async with self._connect() as raw:
            try:
                response = await raw.request(
                    "app_server/session/turn/start",
                    harness_session.TurnStartParams(idempotency_key=key, session_id=self.id, message=message),
                    harness_session.TurnStartResponse,
                )
            except harness_session.SessionTurnActiveError as error:
                # The refusal names the running turn: a read after it could find that turn ended.
                return Busy(
                    session_id=self.id, active_turn_id=error.active_turn_id, turn=Turn(self, error.active_turn_id)
                )
        return Turn(self, response.turn.id, started=True)

    @overload
    async def run[M: BaseModel](
        self,
        content: UserContentLike,
        *,
        response_format: type[M],
        idempotency_key: str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[M | None] | Busy: ...

    @overload
    async def run(
        self,
        content: UserContentLike,
        *,
        response_format: None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[Any] | Busy: ...

    @public_errors
    async def run(
        self,
        content: UserContentLike,
        *,
        response_format: type[BaseModel] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[Any] | Busy:
        """Start a turn and wait for it: ``start_turn``, then ``turn.result(timeout=, on_event=)``.

        Returns ``Busy`` when another turn is active, and the turn's record otherwise. ``timeout``
        bounds the wait, not the start. Leaving the wait never stops the turn (see ``Turn.result``).
        With ``on_event``, one read before the start gives the position the turn's events follow;
        with ``idempotency_key`` too, they are read from the turn's start, as ``turn.result`` does,
        since a retry can return a turn that started before that read.
        ``response_format`` validates the output of a ``Completed`` record (see ``Turn.result``);
        without it, the handle's Agent's ``response_format`` does, if it has one.
        """
        return await self._run(
            content,
            response_format=response_format,
            idempotency_key=idempotency_key,
            timeout=timeout,
            on_event=on_event,
        )

    async def _run(
        self,
        content: UserContentLike,
        *,
        response_format: type[BaseModel] | None,
        idempotency_key: str | None,
        timeout: float | WaitBudget | None,
        on_event: EventHandler | None,
        client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
    ) -> TurnState[Any] | Busy:
        """``run``; the wait does not return on a call of ``client_tools``, which the caller answers."""
        start = None
        if on_event is not None and idempotency_key is None:
            # The start's answer has no position before the turn's first event: read it first.
            # A retry with a key can return a turn that started before that read: not then.
            async with self._connect() as raw:
                start = (await _read_session(raw, self.id)).last_event_id
        try:
            turn = await self.start_turn(content, idempotency_key=idempotency_key)
        except (asyncio.CancelledError, KeyboardInterrupt) as error:
            again = (
                f"run again with idempotency_key={idempotency_key!r} to get it"
                if idempotency_key is not None
                else "running again may start a second one, so pass idempotency_key= to retry safely"
            )
            error.add_note(f"Left session.run during its start: a turn of session {self.id} may have started; {again}")
            raise
        if isinstance(turn, Busy):
            return turn
        # A start never joins a running turn: no turn is taken as running at the position read before it.
        state = await turn._result(
            after=None, timeout=timeout, on_event=on_event, start=start, client_tools=client_tools
        )
        return turn._typed(state, response_format)

    def iter_events(self, *, after: TurnState[object] | str | None = None) -> AsyncIterator[Event]:
        """Yield the session's events after ``after``, a record or a cursor, or from its start.

        It follows the session until the session ends, and never changes anything. Each
        ``TurnEnded`` reads its turn (at least 2 requests). After a cursor, the session's end reads
        the session once more when no event since said which turn runs.

        Raises:
            ObservationLost: The session's events could not be read again; continue after its cursor.
            ValueError: At the first iteration, ``after`` is a record of another session.
        """
        return _iter_events(self, after, turn_id=None)

    @public_errors
    async def cancel(self) -> None:
        """End the session and its subagents. A session that already ended is left as it is.

        Running turns are interrupted, and the session takes no new command: a later send raises
        ``SessionTerminatedError``. Its history stays readable. A deployed cancel returns once the
        deployment accepts it; a local one returns once the session has ended and released its
        sandbox. A subagent cannot be cancelled on its own: cancel its root session.
        """
        async with self._connect() as raw:
            try:
                await raw.request(
                    "app_server/session/cancel",
                    harness_session.SessionCancelParams(session_id=self.id),
                    harness_session.SessionCancelResponse,
                )
            except harness_session.SessionTerminatedError:
                return

    @public_errors
    async def subagents(self) -> list[Session]:
        """Return the handles of this session's direct subagents, newest first.

        A subagent's handle takes ``interrupt`` and reads only: ``send_message``, ``start_turn``
        and ``steer`` on it raise ``ChildSessionProcedureRefusedError``. It has this handle's
        ``on_approval`` handler.
        """
        children: list[Session] = []
        cursor: str | None = None
        async with self._connect() as raw:
            while True:
                page = await raw.request(
                    "app_server/subagents/list",
                    harness_session.SubagentsListParams(
                        parent_session_id=self.id, page=harness_session.ListPageRequest(cursor=cursor)
                    ),
                    harness_session.SubagentsListResponse,
                )
                # A subagent runs its own Agent, which never inherits the parent's response_format.
                for child in page.items:
                    handle = Session(child.session.id, self._host, on_approval=self._on_approval)
                    handle._tools = self._tools
                    children.append(handle)
                if page.next_cursor is None:
                    return children
                cursor = page.next_cursor

    def _bind(self) -> SessionTransport:
        return self._host.bind(self.id)

    def _uploader(self) -> FileUploader | None:
        return self._host.uploader(self.id)

    def _connect(self) -> _RawSession:
        return _RawSession(self._bind())

    def __eq__(self, other: object) -> bool:
        """Two handles are equal when they name the same session on the same host."""
        if not isinstance(other, Session):
            return NotImplemented
        return self._id == other._id and self._host == other._host

    def __hash__(self) -> int:
        return hash((Session, self._id))

    def __repr__(self) -> str:
        return f"Session(id={self.id!r})"


class Turn:
    """A turn of a session, named by its id. Getting one sends no request.

    Get one with ``session.turn(turn_id)``, or from a send.
    """

    __slots__ = ("_id", "_session", "_started")

    def __init__(self, session: Session, turn_id: str, *, started: bool | None = None) -> None:
        self._id = turn_id
        self._session = session
        self._started = started

    @property
    def id(self) -> str:
        """The turn's id."""
        return self._id

    @property
    def started(self) -> bool | None:
        """``True`` for a turn a send started, ``False`` for a running turn a send joined.

        ``None`` when the host could not tell, or when the handle did not come from a send.
        """
        return self._started

    @public_errors
    async def get(self) -> TurnState[Any]:
        """Read this turn's state now. Never waits and never changes the turn.

        Returns ``Running``, ``Blocked`` (the turn waits on a callback), or the record of how the
        turn ended: ``Completed``, ``Interrupted`` or ``Failed``. ``Completed.output`` is the turn's
        text, or, when the handle's Agent has a ``response_format``, that text parsed as on
        ``result(response_format=...)``. The
        record's ``cursor`` is the session's last event id, read before the turn. The session's
        active turn is ``Blocked`` also while one of its subagents, at any depth, waits on a
        callback, such as an approval: ``Blocked.callbacks`` lists it with the subagent's ids.
        A turn of a session that ended
        is never ``Running``: when the host did not report how it ended, it ended with its session.

        Raises:
            TurnNotFoundError: The session has no turn with this id.
        """
        return await self._get(None)

    async def _get(self, response_format: type[BaseModel] | None) -> TurnState[Any]:
        """``get``, parsing a ``Completed`` output with ``response_format`` when given one."""
        async with self._session._connect() as raw:
            state = await read_turn(
                raw, self._session.id, self.id, bind=self._session._host.bind, tools=self._session._tools
            )
        return self._typed(state, response_format)

    @overload
    async def result[M: BaseModel](
        self,
        *,
        response_format: type[M],
        after: TurnState[object] | str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[M | None]: ...

    @overload
    async def result(
        self,
        *,
        response_format: None = None,
        after: TurnState[object] | str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[Any]: ...

    @public_errors
    async def result(
        self,
        *,
        response_format: type[BaseModel] | None = None,
        after: TurnState[object] | str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[Any]:
        """Wait until the turn ends or waits on a callback opened after ``after``, and return its record.

        Returns ``Completed``, ``Interrupted`` or ``Failed`` when the turn ends, and ``Blocked``
        when a callback opened after ``after`` and the host still lists it as open: one that another
        client already answered does not return. ``after`` is a position in the session's events:
        a record of this session, or its ``cursor``, the same position. Without ``after``, a turn
        that waits on any callback returns at once. A subagent's callback blocks the turn as on
        ``get()``; the session's events do not order it, so the wait returns while one is open,
        except one that a ``Blocked`` given as ``after`` lists. A cursor that is not one of the
        session's raises only when the wait reads the session's events: a turn that already ended
        returns its record without reading them.

        ``timeout`` is the time the SDK waits for the host, in seconds, its first read included; the
        time an ``on_approval`` handler takes counts too. At the deadline, one more read returns
        the turn's record at that moment, ``Running`` or ``Blocked`` with the callbacks the host
        lists: a timeout raises nothing, but a read that fails raises.

        ``on_event``, a plain or async function, gets the turn's events in order while the call
        waits: from the turn's start, or after ``after``, up to the record returned, at the deadline
        too. When the turn ended, the last is ``TurnEnded`` with that record. It sends no request of
        its own; without ``after``, the events are read from the turn's start position the host
        recorded, or, from a host that records none, from the session's start, within
        ``timeout``. ``after`` is this turn's record, a record read before this turn started (such
        as the previous turn's result), or a position inside this turn: another turn's record read
        while this one ran would lose this turn's events that name no turn. The events are read up
        to the record's position, with no time limit: if the stream ends short of it, the record's
        ``cursor`` is the position reached, so a next wait after it neither repeats nor misses an
        event. An error it raises ends the wait, and the deadline can cancel an async one mid-call.

        Leaving the wait sends nothing to the host: the turn goes on. A cancel, such as
        ``asyncio.wait_for`` or Ctrl-C, gets a note with the ids and how to stop the turn.

        With ``response_format``, a Pydantic model, ``Completed.output`` is the turn's text
        validated as JSON into that model, as ``agent.run`` does, or ``InvalidOutput`` when it does
        not validate. It is ``None`` when the turn did not end ``"completed"``: it reached its
        iteration limit, or a hook skipped it. This only parses the text: the model is asked for
        that format only when the Agent that runs the session sets ``response_format``. Without
        ``response_format``, the handle's Agent's ``response_format`` applies, if it has one.

        Raises:
            ObservationLost: The session's events, or its subagents' callbacks, could not be read;
                the turn goes on.
            TurnNotFoundError: The session has no turn with this id.
            LocalSessionProcedureError: In-process, ``after`` is a cursor the session never had.
            RemoteSessionConflictError: On a deployment, ``after`` is not a cursor.
        """
        state = await self._result(after=after, timeout=timeout, on_event=on_event, start=None)
        return self._typed(state, response_format)

    async def _result(
        self,
        *,
        after: TurnState[object] | str | None,
        timeout: float | WaitBudget | None,
        on_event: EventHandler | None,
        start: str | None,
        client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
    ) -> TurnState[str]:
        _position(after, self._session.id)
        handler = self._session._on_approval
        approvals = None if handler is None else Approvals(handler)
        transport = self._session._bind()
        try:
            async with contextlib.AsyncExitStack() as stack:
                raw = await stack.enter_async_context(_RawSession(transport))
                if approvals is not None:
                    await stack.enter_async_context(
                        approvals.serving_session(self._session._host.bind, self._session.id)
                    )
                state = await wait_for_turn(
                    raw,
                    transport,
                    self._session.id,
                    self.id,
                    after=after,
                    timeout=timeout,
                    on_event=on_event,
                    start=start,
                    approvals=approvals,
                    bind=self._session._host.bind,
                    tools=self._session._tools,
                    client_tools=client_tools or self._session._client_tools,
                )
        except (asyncio.CancelledError, KeyboardInterrupt) as error:
            error.add_note(left_wait_note(self._session.id, self.id))
            raise
        return state

    def iter_events(self, *, after: TurnState[object] | str | None = None) -> AsyncIterator[Event]:
        """Yield this turn's events after ``after``, or from its start.

        ``after`` is this turn's record, a record read before this turn started (such as the
        previous turn's result), or a position inside this turn: an event that names no turn counts
        as this turn's. When the turn ended, the last is ``TurnEnded``, with its record, and
        a position at or after its end yields nothing, at once. Until the turn's ``TurnEnded``, it
        yields the events the session has, then the live ones, with no time limit: a turn that
        waits on an approval can send no event for hours. Never changes anything. It reads
        the turn first (at least 2 requests). Without ``after``, it starts at the turn's start: it
        reads from the position the host recorded there, or, from a host that records none, reads
        the session's events from the session's start to find it.

        Raises:
            ObservationLost: The session's events could not be read again; continue after its cursor.
            TurnNotFoundError: At the first iteration, the session has no turn with this id.
            ValueError: At the first iteration, ``after`` is a record of another session.
        """
        return _iter_events(self._session, after, turn_id=self.id)

    def _typed(self, state: TurnState[str], response_format: type[BaseModel] | None) -> TurnState[Any]:
        model = response_format if response_format is not None else self._session._response_format
        return state if model is None else typed(state, model)

    @public_errors
    async def steer(self, content: UserContentLike) -> Turn | TurnConflict:
        """Add a message to this turn while it runs.

        Returns ``TurnConflict`` when this turn is no longer the active one: the message is not added.
        """
        message = checked_message(content)
        return await self._command(
            "app_server/session/turn/steer",
            harness_session.TurnSteerParams(session_id=self._session.id, expected_turn_id=self.id, message=message),
            harness_session.TurnSteerResponse,
        )

    @public_errors
    async def answer(
        self, callback_id: str, answer: AllowApproval | DenyApproval
    ) -> Answered | AlreadySettled | NotFound:
        """Answer an approval that this turn's session waits on, by its callback id.

        Reads the session once, then answers. Returns ``Answered`` when the approval was open,
        with ``answer`` the answer that counted, ``AlreadySettled`` when it is no longer open
        (another client answered it first, or it closed), and ``NotFound`` when the session never
        opened it. A subagent's approval is answered on the subagent's session, named by the
        callback's ``session_id``.

        Two clients that answer the same approval at the same time both get ``Answered``, with the
        answer of the one that came first: compare it with yours. Both hosts do the same.

        Raises:
            ValueError: ``callback_id`` is not a UUID (nothing is sent), the callback is open but
                is not an approval, or ``answer`` allows a hook's approval for the session.
            ObservationLost: The approval is not open, and the session's events could not be read.
        """
        return await answer_approval(self._session._bind(), self._session.id, callback_id, answer)

    @public_errors
    async def interrupt(self) -> Turn | TurnConflict:
        """Stop this turn. Returns ``TurnConflict`` when this turn is no longer the active one."""
        return await self._command(
            "app_server/session/turn/interrupt",
            harness_session.TurnInterruptParams(session_id=self._session.id, expected_turn_id=self.id),
            harness_session.TurnInterruptResponse,
        )

    async def _command(
        self, method: str, params: harness_session.SessionModel, result_type: type[harness_session.SessionModel]
    ) -> Turn | TurnConflict:
        async with self._session._connect() as raw:
            try:
                await raw.request(method, params, result_type)
            except harness_session.SessionTurnConflictError:
                active_turn_id = await _active_turn_id(raw, self._session.id)
                return TurnConflict(
                    session_id=self._session.id, expected_turn_id=self.id, active_turn_id=active_turn_id
                )
        return self

    def __eq__(self, other: object) -> bool:
        """Two handles are equal when they name the same turn of the same session; ``started`` is not compared."""
        if not isinstance(other, Turn):
            return NotImplemented
        return self._id == other._id and self._session == other._session

    def __hash__(self) -> int:
        return hash((Turn, self._session.id, self._id))

    def __repr__(self) -> str:
        return f"Turn(session_id={self._session.id!r}, id={self.id!r})"


def checked_idempotency_key(key: IdempotencyKey | None) -> str | None:
    """Return the key stripped, or raise ``SdkError`` if the control plane would refuse it.

    The control plane's rule, applied on both hosts so a key a deployment refuses fails locally too.
    """
    if key is None:
        return None
    try:
        return _IDEMPOTENCY_KEY_ADAPTER.validate_python(key)
    except ValidationError as error:
        raise SdkError("invalid idempotency_key; expected 1 to 256 characters") from error


def checked_message(content: UserContentLike) -> list[harness_session.ContentBlock]:
    """Return the content blocks of a message.

    An empty message, or one whose blocks are all blank text, raises ``SdkError`` before any request.
    """
    blocks = to_session_content(content) if content else []
    if all(isinstance(block, harness_session.TextContentBlock) and not block.text.strip() for block in blocks):
        raise SdkError(_EMPTY_MESSAGE)
    return blocks


def _control_plane(deployment: remote_transport.RemoteAgentDeployment) -> str:
    return deployment.server_url.strip().rstrip("/")


def _position(after: TurnState[object] | str | None, session_id: str) -> str | None:
    """The cursor of ``after``. A record of another session is refused before any request."""
    if after is None or isinstance(after, str):
        return after
    if after.session_id != session_id:
        raise ValueError(f"after= is a record of session {after.session_id}, not of {session_id}")
    return after.cursor


@public_iter_errors
async def _iter_events(
    session: Session, after: TurnState[object] | str | None, *, turn_id: str | None
) -> AsyncIterator[Event]:
    cursor = _position(after, session.id)
    if turn_id is not None and ended_record(after, turn_id):
        return  # None of the turn's events come after the record of its end.
    transport = session._bind()
    async with _RawSession(transport) as raw:
        active = active_turn_at(after, turn_id)
        state = None
        if turn_id is not None:
            state, start = await read_turn_and_start(
                raw, session.id, turn_id, bind=session._host.bind, tools=session._tools
            )
            if after is None and start is not None:
                # The host recorded where the turn started: read from there, not the session's start.
                cursor = start
        ends = {} if turn_id is None or state is None or isinstance(state, Running | Blocked) else {turn_id: state}
        events = follow(
            raw,
            transport,
            session.id,
            after=cursor,
            active_turn_id=active,
            active_known=not isinstance(after, str),
            bind=session._host.bind,
            tools=session._tools,
            turn_id=turn_id,
            ends=ends,
        )
        if ends and state is not None:
            async for event in up_to_end(events, after=cursor, state=state):
                yield event
            return
        async with contextlib.aclosing(events) as stream:
            async for _cursor, item in stream:
                if item is not None:
                    yield item


async def _active_turn_id(raw: _RawSession, session_id: str) -> str | None:
    return (await _read_session(raw, session_id)).state.active_turn_id


async def _read_session(raw: _RawSession, session_id: str) -> harness_session.SessionReadResponse:
    return await raw.request(
        "app_server/session/read",
        harness_session.SessionReadParams(session_id=session_id),
        harness_session.SessionReadResponse,
    )


def local_session(
    runtime: local._AgentsSdkLocalRuntime | None,
    session_id: str,
    *,
    on_approval: ApprovalHandler | None = None,
    response_format: type[BaseModel] | None = None,
    tools: Mapping[str, _Tool] = NO_TOOLS,
    client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
    reassemble: Reassemble | None = None,
    completion_provider: CompletionProvider | None = None,
) -> Session:
    """The handle of a local session. With ``reassemble``, a session saved by an earlier process
    reopens on first use, its model calls answered by ``completion_provider`` when given."""
    session = Session(
        session_id,
        _LocalHost(runtime, reassemble, completion_provider),
        on_approval=on_approval,
        response_format=response_format,
    )
    session._tools = tools
    session._client_tools = client_tools
    return session


def remote_session(
    deployment: remote_transport.RemoteAgentDeployment,
    session_id: str,
    *,
    on_approval: ApprovalHandler | None = None,
    response_format: type[BaseModel] | None = None,
    tools: Mapping[str, _Tool] = NO_TOOLS,
    client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
) -> Session:
    host = _RemoteHost(deployment)
    host.check(session_id)
    session = Session(session_id, host, on_approval=on_approval, response_format=response_format)
    session._tools = tools
    session._client_tools = client_tools
    return session
