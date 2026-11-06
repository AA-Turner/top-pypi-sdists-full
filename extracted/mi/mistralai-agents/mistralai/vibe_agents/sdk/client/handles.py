"""Handles: a session or a turn named by its ID, on the host that runs it.

A handle holds IDs and the way to reach their host, and nothing the host reported. Getting one
sends no request, so it is never out of date: store the IDs, and bind them again in any process
with ``agent.session(session_id)`` and ``session.turn(turn_id)``.

Sends return a value when the host refuses them for the session's state: ``Busy`` when
``start_turn`` cannot start a turn, ``TurnConflict`` when a turn command names a turn that is no
longer active, ``AlreadySettled`` or ``NotFound`` when an answer names a callback that is no longer
open or never was. ``send_message`` always returns a turn: it starts one or adds to the running one.
Reads return a record (``turn.get()`` returns a ``TurnState``), which can be out of date: read
again for a newer one. Waits return a record too (``turn.result()``, ``session.run()``), and
leaving one never changes the turn. ``iter_events`` reads the session's events and never changes
anything. With ``output_type=``, a wait validates the output of a ``Completed`` record against
that model, as ``agent.run`` does. Without it, reads and waits use the
``output_type`` of the Agent the handle came from: ``agent.start_session()`` and
``agent.session(id)`` keep it, and so do the session's turns. A subagent's handle has none. A
handle's ``on_approval`` handler answers approvals, its ``on_client_tool`` answers client tools, and
its ``on_sign_in`` answers sign-ins, while a call waits on it.
"""

from __future__ import annotations

import asyncio
import contextlib
import dataclasses
from collections.abc import AsyncIterator, Callable, Iterator, Mapping
from pathlib import Path
from typing import Any, Protocol, cast, overload

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
from mistralai.vibe_agents.sdk.authoring.errors import (
    InvalidCursorError,
    SdkError,
    UnsupportedSessionProcedureError,
    public_errors,
    public_iter_errors,
)
from mistralai.vibe_agents.sdk.client.approval_requests import NO_TOOLS, _Tool
from mistralai.vibe_agents.sdk.client.approvals import (
    ApprovalHandler,
    Approvals,
    answer_callback,
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
from mistralai.vibe_agents.sdk.client.sign_ins import SignInHandler
from mistralai.vibe_agents.sdk.client.turn_reads import read_turn, read_turn_and_start, typed
from mistralai.vibe_agents.sdk.client.turn_waits import WaitBudget, wait_for_turn
from mistralai.vibe_agents.sdk.transport import client_tools as client_tools_registry
from mistralai.vibe_agents.sdk.transport import local
from mistralai.vibe_agents.sdk.transport import remote as remote_transport
from mistralai.vibe_agents.sdk.transport.client_tools import NO_CLIENT_TOOLS, ClientToolRegistry
from mistralai.vibe_agents.sdk.transport.event_ids import _session_cursor
from mistralai.vibe_agents.sessions_client import IdempotencyKey

__all__ = [
    "Session",
    "Turn",
    "checked_idempotency_key",
    "host_wait_budget",
    "left_wait_note",
    "with_running_answers_sent",
]


def left_wait_note(session_id: str, turn_id: str) -> str:
    """The note on a cancel that stopped a wait on the turn: the cancel did not stop the turn, and how to stop it."""
    return (
        f"Stopped waiting for turn {turn_id} of session {session_id}. The cancel does not stop the turn. To stop it: "
        f"await agent.session({session_id!r}).turn({turn_id!r}).interrupt()"
    )


_EMPTY_MESSAGE = "Turn messages must contain at least one content block"
_IDEMPOTENCY_KEY_ADAPTER: TypeAdapter[str] = TypeAdapter(IdempotencyKey)


class _SessionHost(Protocol):
    """Where a session runs. It reaches a session by ID without asking the host first."""

    def bind(self, session_id: str) -> SessionTransport:
        """Return a transport bound to the session. It sends no request until it is used."""
        ...

    def uploader(self, session_id: str) -> FileUploader | None:
        """The uploader of the session's files, or ``None`` when the host takes no uploads."""
        ...

    async def attach(self, session_id: str, client_tools: ClientToolRegistry) -> _RawSession:
        """Return a client of the session that answers ``client_tools`` in its tree until it closes."""
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
        runtime = self._resolved(session_id)
        reassemble = self._reassemble
        if reassemble is None:
            return runtime.bind_session(session_id)
        return runtime.bind_session(
            session_id,
            reassemble=lambda: reassemble(runtime, session_id),
            completion_provider=self._completion_provider,
        )

    def uploader(self, session_id: str) -> FileUploader | None:
        runtime = self._resolved(session_id)
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
                    raise UnsupportedSessionProcedureError(
                        method="upload_file",
                        backend="local",
                        reason="File uploads are not available in the current configuration.",
                    )
                return await uploader(session_id, source, name=name, media_type=media_type)

            return reopen_then_upload
        return _live_uploader(runtime, session_id)

    def _resolved(self, session_id: str) -> local._AgentsSdkLocalRuntime:
        if self._runtime is not None:
            return self._runtime
        local._refuse_if_freed_by_block_exit(session_id)
        return local._process_runtime()

    async def attach(self, session_id: str, client_tools: ClientToolRegistry) -> _RawSession:
        runtime = self._resolved(session_id)
        reassemble = self._reassemble
        return await runtime.get_session(
            session_id,
            client_tools=client_tools,
            reassemble=None if reassemble is None else lambda: reassemble(runtime, session_id),
            completion_provider=self._completion_provider,
        )

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

    async def attach(self, session_id: str, client_tools: ClientToolRegistry) -> _RawSession:
        return await remote_transport._get_remote_session(self._deployment, session_id, client_tools=client_tools)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _RemoteHost):
            return NotImplemented
        # A session is named by its id on its control plane, however its Agent was loaded.
        return _control_plane(self._deployment) == _control_plane(other._deployment)

    __hash__ = None  # type: ignore[assignment]


class Session:
    """A session, named by its ID. Binding one with ``agent.session(session_id)`` sends no request.

    Get one with ``await agent.start_session()``, or bind a stored ID with
    ``agent.session(session_id)``. Both keep the agent's ``output_type`` for ``run``, and for the
    ``get`` and ``result`` of the session's turns.

    ``on_approval`` answers the approvals of the session and its subagents while ``session.run`` or
    ``turn.result`` waits, with ``AllowApproval``, ``DenyApproval`` or ``agents.KeepCallbackOpen()``.
    ``on_sign_in`` answers their sign-ins with a ``SignInAnswer``. ``on_client_tool`` answers their
    client tool calls, so the wait does not return ``Blocked`` on them. An approval or sign-in handler
    that raises, or returns anything else, leaves its callback open, and the waiting call raises while
    the turn keeps running. A client tool answer or ``on_client_tool`` handler that raises follows the
    agent's ``tool_errors``, as on ``agent.run``: by default the model reads that the call failed
    and the wait goes on. Two waits at once in one event loop share the answers: the answer runs once
    per client tool call.

    Two handles are equal when they name the same session in the same place: the same Mistral API
    for a deployed agent, however you loaded it, or the same local runtime. Keep them in a set or
    as dictionary keys.
    """

    __slots__ = ("_client_tools", "_host", "_id", "_on_approval", "_on_sign_in", "_output_type", "_tools")

    def __init__(
        self,
        session_id: str,
        host: _SessionHost,
        *,
        on_approval: ApprovalHandler | None = None,
        on_sign_in: SignInHandler | None = None,
        output_type: type[BaseModel] | None = None,
    ) -> None:
        self._id = session_id
        self._host = host
        self._on_approval = on_approval
        self._on_sign_in = on_sign_in
        self._output_type = output_type
        # The agent's tool objects by tool id, for the requests of approvals: set by the agent.
        self._tools: Mapping[str, _Tool] = NO_TOOLS
        # The client tools that this handle's waits answer in the session tree: set by the agent.
        self._client_tools: ClientToolRegistry = NO_CLIENT_TOOLS

    @property
    def id(self) -> str:
        """The session's ID."""
        return self._id

    def turn(self, turn_id: str) -> Turn:
        """Return the handle of a turn of this session. Sends no request.

        Args:
            turn_id: The ID of the turn.
        """
        return Turn(self, turn_id)

    @public_errors
    async def send_message(self, content: UserContentLike, *, idempotency_key: str | None = None) -> Turn:
        """Send a message: the session starts a turn, or adds the message to the running one.

        ``turn.started`` says which: ``True`` for a new turn, ``False`` for the running one.

        Raises ``agents.SessionBusyError`` when the session still cannot take the message after its retries;
        nothing was applied.

        Args:
            content: The message: a string or content blocks.
            idempotency_key: Makes the send safe to retry: the same key returns the same turn, and reusing
                it for another message raises ``agents.SessionIdempotencyConflictError``.
        """
        message = checked_message(content)
        key = checked_idempotency_key(idempotency_key)
        async with self._connect() as raw:
            receipt = await raw.request(
                "app_server/session/message/send",
                harness_session.MessageSendParams(idempotency_key=key, session_id=self.id, message=message),
                harness_session.MessageSendResponse,
            )
        return Turn(self, receipt.turn_id, started=_send_started(receipt))

    @public_errors
    async def start_turn(self, content: UserContentLike, *, idempotency_key: str | None = None) -> Turn | Busy:
        """Start a new turn. Returns ``Busy``, with the running turn in ``busy.turn``, when one is active.

        The same ``idempotency_key`` returns the turn that key started; reusing it for another
        message raises ``agents.SessionIdempotencyConflictError`` while the session runs. A retry
        with a key refused with ``Busy`` starts a turn once the running one ends. A start never
        joins a running turn, so ``turn.started`` is ``True``.

        Raises ``SessionBusyError`` when the session cannot take a start for another reason, such
        as a limit on running subagents; nothing was applied.

        Args:
            content: The message that starts the turn: a string or content blocks.
            idempotency_key: Names the start, so a retry with it returns the turn it started.
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
                    session_id=self.id,
                    active_turn_id=error.active_turn_id,
                    turn=host_named_turn(self, error.active_turn_id),
                )
        return Turn(self, response.turn.id, started=True)

    @overload
    async def run[M: BaseModel](
        self,
        content: UserContentLike,
        *,
        output_type: type[M],
        idempotency_key: str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[M] | Busy: ...

    @overload
    async def run(
        self,
        content: UserContentLike,
        *,
        output_type: None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[Any] | Busy: ...

    @public_errors
    async def run(
        self,
        content: UserContentLike,
        *,
        output_type: type[BaseModel] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[Any] | Busy:
        """Start a turn and wait for it to end, or to wait on a callback; return its record.

        Returns ``Busy`` when another turn is active. It is ``start_turn``, then
        ``turn.result(timeout=, on_event=)``: leaving the wait does not stop the turn. With the
        handle's ``on_client_tool``, it raises what ``Turn.result`` raises for a client tool answer.

        Args:
            content: The message that starts the turn: a string or content blocks.
            output_type: A Pydantic model that validates the output of a ``Completed`` record (see
                ``Turn.result``). Without it, the handle's agent's ``output_type`` does, if it has one.
            idempotency_key: Names the start, so a retry with it returns the turn it started.
            timeout: The most seconds to wait for the turn, not counting the start. An ``on_approval`` or
                ``on_sign_in`` handler's time counts; your client-tool code does not. ``None`` waits with no limit.
            on_event: A plain or async function called with each of the turn's events while the call waits.
                When the turn has ended, the last event is ``TurnEnded``.
        """
        return await self._run(
            content,
            output_type=output_type,
            idempotency_key=idempotency_key,
            timeout=timeout,
            on_event=on_event,
        )

    async def _run(
        self,
        content: UserContentLike,
        *,
        output_type: type[BaseModel] | None,
        idempotency_key: str | None,
        timeout: float | WaitBudget | None,
        on_event: EventHandler | None,
        client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
    ) -> TurnState[Any] | Busy:
        """``run``; the wait does not return on a call of ``client_tools``, which the caller answers."""
        start = None
        if on_event is not None and idempotency_key is None:
            # The start's answer has no position before the turn's events: read one first.
            # A retry with a key can return a turn that started before that read: not then.
            async with self._connect() as raw:
                start = await _last_turn_start(raw, self.id)
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
        return turn._typed(state, output_type)

    def iter_events(self, *, after: TurnState[object] | str | None = None) -> AsyncIterator[Event]:
        """Yield the session's events after ``after``, a record or a cursor, or from its start.

        It follows the session until the session ends, and never changes anything. It reads each
        ended turn, so each ``TurnEnded`` carries its record.

        Args:
            after: A record or a cursor to continue after. ``None`` starts at the session's start.

        Raises:
            ObservationLost: The session's events could not be read again; continue after its cursor.
            InvalidCursorError: At the first iteration, ``after`` is a record or a cursor of another session,
                or a cursor that is not valid.
        """
        return _iter_events(self, after, turn_id=None)

    @public_errors
    async def cancel(self) -> None:
        """End the session and its subagents. A session that already ended is left as it is.

        Running turns are interrupted, and the session takes no new command: a later send raises
        ``SessionTerminatedError``. Its history stays readable. A deployed cancel returns once the
        deployment accepts it; a local one returns once the session has ended and released its
        sandbox. A subagent cannot be cancelled on its own. Cancel its root session instead.
        """
        try:
            async with self._connect() as raw:
                await raw.request(
                    "app_server/session/cancel",
                    harness_session.SessionCancelParams(session_id=self.id),
                    harness_session.SessionCancelResponse,
                )
        except harness_session.SessionTerminatedError as error:
            if isinstance(error, local._LocalSessionEndedError) and error.continues_in_a_new_block:
                # A saved tree did not end: a new block with its journal_factory= continues it.
                raise
            return

    @public_errors
    async def subagents(self) -> list[Session]:
        """Return the handles of this session's direct subagents, newest first.

        A subagent's handle reads, and its turns take ``interrupt``: ``send_message``, ``start_turn``,
        ``run`` and ``cancel`` on the handle, and ``steer`` on its turns, raise
        :class:`UnsupportedSessionProcedureError`. To redirect a subagent, message or steer its parent;
        to stop it, cancel its root session. It has this handle's ``on_approval``, ``on_sign_in`` and
        ``on_client_tool``.
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
                # A subagent runs its own Agent, which never inherits the parent's output_type.
                for child in page.items:
                    handle = Session(
                        child.session.id, self._host, on_approval=self._on_approval, on_sign_in=self._on_sign_in
                    )
                    handle._tools = self._tools
                    handle._client_tools = self._client_tools
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
    """A turn of a session, named by its ID. Binding one with ``session.turn(turn_id)`` sends no request.

    Get one with ``session.turn(turn_id)``, or from a send. Two handles of the same turn of the
    same session are equal.
    """

    __slots__ = ("_host_named", "_id", "_session", "_started")

    def __init__(self, session: Session, turn_id: str, *, started: bool | None = None) -> None:
        self._id = turn_id
        self._session = session
        self._started = started
        # Set by ``host_named_turn``: the host named this turn in an answer, as a refused start does.
        self._host_named = False

    @property
    def id(self) -> str:
        """The turn's ID."""
        return self._id

    @property
    def started(self) -> bool | None:
        """``True`` for a turn a send started, ``False`` for a running turn a send joined.

        ``None`` for a handle that did not come from a send, such as one bound by ID.
        """
        return self._started

    @public_errors
    async def get(self) -> TurnState[Any]:
        """Read this turn's state now. Never waits and never changes the turn.

        Returns ``Running``, ``Blocked`` (the turn waits on a callback), or the record of how the
        turn ended: ``Completed``, ``Interrupted``, ``Failed`` or ``UnknownOutcome``. ``Completed.output``
        is the turn's text, or, when the handle's agent has an ``output_type``, that text parsed as on
        ``result(output_type=...)``. The
        record's ``cursor`` is the session's last event ID when the record was read. The session's
        active turn is ``Blocked`` also while one of its subagents, at any depth, waits on a
        callback, such as an approval: ``Blocked.callbacks`` lists it with the subagent's IDs.
        A turn of a session that ended is never ``Running``. When the session did not report how the
        turn ended, the turn reads as the session ended: for a cancelled session, ``Interrupted`` with
        ``cause="cancelled"``.
        A turn a send returned is ``Running`` until the session lists it: a deployed agent answers the
        send before it does.

        Raises:
            TurnNotFoundError: The session has no turn with this ID. Never for a turn a send returned,
                nor for ``busy.turn``.
        """
        return await self._get(None)

    async def _get(self, output_type: type[BaseModel] | None) -> TurnState[Any]:
        """``get``, parsing a ``Completed`` output with ``output_type`` when given one."""
        async with self._session._connect() as raw:
            state = await read_turn(
                raw, self._session.id, self.id, tools=self._session._tools, confirmed=self._confirmed()
            )
        return self._typed(state, output_type)

    @overload
    async def result[M: BaseModel](
        self,
        *,
        output_type: type[M],
        after: TurnState[object] | str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[M]: ...

    @overload
    async def result(
        self,
        *,
        output_type: None = None,
        after: TurnState[object] | str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[Any]: ...

    @public_errors
    async def result(
        self,
        *,
        output_type: type[BaseModel] | None = None,
        after: TurnState[object] | str | None = None,
        timeout: float | None = None,
        on_event: EventHandler | None = None,
    ) -> TurnState[Any]:
        """Wait for the turn to end, or to wait on a callback, and return its record.

        Returns ``Completed``, ``Interrupted``, ``Failed`` or ``UnknownOutcome`` when the turn ends,
        and ``Blocked`` when it waits on a callback opened after ``after`` that is still open. At the
        deadline, it returns the turn's record at that moment, ``Running`` or ``Blocked``, and raises
        nothing.

        Leaving the wait sends nothing, and the turn keeps running. A cancel, such as
        ``asyncio.wait_for`` or Ctrl-C, gets a note with the IDs and how to stop the turn.

        Without ``after``, a turn that waits on any callback returns at once. Pass this turn's last
        record as ``after`` to wait past the callbacks you already handled.

        Args:
            output_type: A Pydantic model that the turn's text is parsed into, as ``Completed.output``.
                Defaults to the handle's agent's ``output_type``.
            after: A record of this session, or its ``cursor``, to read the turn's events after.
                Defaults to this turn's start: callbacks of earlier turns don't count. Pass this turn's
                record, or one read before this turn started. Another turn's record, read while this
                turn ran, can miss some of this turn's events.
            timeout: The most seconds to wait for the turn. An ``on_approval`` or ``on_sign_in`` handler's time
                counts; your client-tool code does not. ``None`` waits as long as the turn does.
            on_event: A plain or async function called with each of the turn's events, in order, while the
                call waits. When the turn has ended, the last event is ``TurnEnded``.

        Raises:
            ObservationLost: The session's events, or its subagents' callbacks, could not be read;
                the turn keeps running.
            TurnNotFoundError: The session has no turn with this ID. Never for a turn a send
                returned, nor for ``busy.turn``: until the session lists it, the wait follows its events.
            InvalidCursorError: ``after`` is a record or a cursor of another session, raised before any
                read, or a cursor the session never had, raised only when the wait reads the events.
            ClientToolAnswerError: The handle's ``on_client_tool`` answered a call, and the answer
                could not be sent; the call stays open.
            Exception: With ``tool_errors="raise"``, the exception a client tool answer or
                ``on_client_tool`` handler raised; its call stays open.
        """
        state = await self._result(after=after, timeout=timeout, on_event=on_event, start=None)
        return self._typed(state, output_type)

    async def _result(
        self,
        *,
        after: TurnState[object] | str | None,
        timeout: float | WaitBudget | None,
        on_event: EventHandler | None,
        start: str | None,
        client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
    ) -> TurnState[str]:
        """``result`` without the output parsed. With ``client_tools``, the caller answers their calls
        meanwhile; without it, the handle's own client tool answers run during the wait."""
        answers = self._session._client_tools
        # ``timeout=0`` only reads, so it answers nothing, in-process and on a deployment alike.
        if client_tools or not answers or timeout == 0:
            return await self._wait(
                after=after, timeout=timeout, on_event=on_event, start=start, client_tools=client_tools
            )
        _position(after, self._session.id)
        try:
            client = await self._session._host.attach(self._session.id, answers)
        except (asyncio.CancelledError, KeyboardInterrupt) as error:
            error.add_note(left_wait_note(self._session.id, self.id))
            raise
        async with client, client_tools_registry.raising_answer_failures(client):
            with host_wait_budget(client, timeout) as budget:
                # With tool_errors="raise", a client tool's exception raises here; its call stays open.
                state = await client_tools_registry.raise_from_client_tools(
                    client,
                    self._wait(after=after, timeout=budget, on_event=on_event, start=start, client_tools=answers),
                )
            reader = Session(self._session.id, self._session._host)
            reader._tools = self._session._tools
            latest = await client_tools_registry.raise_from_client_tools(
                client, with_running_answers_sent(client, reader, state, None, on_event, answers)
            )
        # ``state`` is a turn's record, never ``Busy``, so the latest record is one too.
        return cast("TurnState[str]", latest)

    async def _wait(
        self,
        *,
        after: TurnState[object] | str | None,
        timeout: float | WaitBudget | None,
        on_event: EventHandler | None,
        start: str | None,
        client_tools: ClientToolRegistry,
    ) -> TurnState[str]:
        cursor = _position(after, self._session.id)
        if isinstance(after, str):
            after = cursor
        elif after is not None and cursor is not None and after.cursor != cursor:
            after = dataclasses.replace(after, cursor=cursor)  # A cursor an earlier version gave.
        handler, on_sign_in = self._session._on_approval, self._session._on_sign_in
        approvals = None if handler is None and on_sign_in is None else Approvals(handler, on_sign_in=on_sign_in)
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
                    tools=self._session._tools,
                    client_tools=client_tools,
                    confirmed=self._confirmed(),
                )
        except (asyncio.CancelledError, KeyboardInterrupt) as error:
            error.add_note(left_wait_note(self._session.id, self.id))
            raise
        return state

    def iter_events(self, *, after: TurnState[object] | str | None = None) -> AsyncIterator[Event]:
        """Yield this turn's events after ``after``, or from its start, up to its ``TurnEnded``.

        It yields the events the session has, then the live ones, with no time limit: a turn that
        waits on an approval can send no event for hours. When the turn ended, the last is
        ``TurnEnded``, with its record, and a position at or after its end yields nothing, at once.
        It changes nothing.

        Args:
            after: This turn's record, a record read before this turn started (such as the previous
                turn's result), or a cursor inside this turn. ``None`` starts after the previous turn's end.

        Raises:
            ObservationLost: The session's events could not be read again; continue after its cursor.
            TurnNotFoundError: At the first iteration, the session has no turn with this ID. Never
                for a turn a send returned, nor for ``busy.turn``.
            InvalidCursorError: At the first iteration, ``after`` is a record or a cursor of another session,
                or a cursor that is not valid.
        """
        return _iter_events(self._session, after, turn_id=self.id, confirmed=self._confirmed())

    def _confirmed(self) -> bool:
        """Whether the host confirmed this turn: a send returned the handle, or the host named the turn
        in an answer. A deployment answers before its session read lists the turn, so a read that
        does not list it says it runs."""
        return self._started is not None or self._host_named

    def _typed(self, state: TurnState[str], output_type: type[BaseModel] | None) -> TurnState[Any]:
        model = output_type if output_type is not None else self._session._output_type
        return state if model is None else typed(state, model)

    @public_errors
    async def steer(self, content: UserContentLike) -> Turn | TurnConflict:
        """Add a message to this turn while it runs.

        Returns ``TurnConflict`` when this turn is no longer the active one: the message is not added.

        Args:
            content: The message to add: a string or content blocks.
        """
        message = checked_message(content)
        return await self._command(
            "app_server/session/turn/steer",
            harness_session.TurnSteerParams(session_id=self._session.id, expected_turn_id=self.id, message=message),
            harness_session.TurnSteerResponse,
        )

    @public_errors
    async def answer(self, callback_id: str, answer: object) -> Answered | AlreadySettled | NotFound:
        """Answer any open callback of this turn's session or of its subagents, from any turn, by
        its callback ID. The turn's ID is not used: a callback's ID names it in its session.

        An approval (``OpenApproval``) takes ``AllowApproval`` or ``DenyApproval``. A sign-in
        (``OpenSignIn``) takes a ``SignInAnswer`` that names each source it asks for, and only
        those. A client tool call (``OpenClientToolCall``) takes the tool's result: what an answer
        function would return, such as a model, a dict or a ``ToolResult``. When the stub is in the
        ``tools=`` of the agent or of its subagents, the result is checked against the stub's return
        type and sent as its answer is. Otherwise it is sent as JSON, unchecked: a tool built with
        ``output_schema=``, a hook's tool, a tool ID that two different stubs share, or a handle
        from ``Agent.load_from()``.

        Reads the session once, then answers. Returns ``Answered`` when the callback was open,
        ``AlreadySettled`` when it is no longer open (another client answered it first, or it
        closed), and ``NotFound`` when the session never opened it. A subagent's open callback,
        listed in the root's ``Blocked.callbacks``, is answered on the subagent's session, and the
        record names that session; once it is no longer open, the root says ``NotFound`` and the
        subagent's own session, ``agent.session(callback.session_id)``, says ``AlreadySettled``.

        For an approval, ``Answered.answer`` is the answer that counted: two clients that answer
        at the same time both get ``Answered``, with the answer of the one that came first, so
        compare it with yours. It is ``None`` when the answer that counted could not be read in time;
        read the turn to see the outcome. For a client tool call and a sign-in it is ``None``: the
        first result sent counts. Local and deployed sessions do the same.

        An approval's ``answer`` is ``AllowApproval`` or ``DenyApproval``, never a bool, a dict or
        ``None``. ``KeepCallbackOpen()`` is a handler's return, never an answer: to leave a
        callback open, do not answer it.

        Args:
            callback_id: The ID of the open callback, as in ``Blocked.callbacks``.
            answer: The answer of the callback's kind: ``AllowApproval`` or ``DenyApproval``, a
                ``SignInAnswer``, or a client tool's result.

        Raises:
            ValueError: ``callback_id`` is not a UUID (nothing is sent).
            SdkError: ``answer`` is ``KeepCallbackOpen()`` or does not fit the callback, or two subagents
                have a callback open with that ID. Also when ``answer`` allows a hook's approval for the
                whole session (``AllowApproval(scope="session")``), or the callback is a client tool call of
                a tool the platform provides, such as one in the ``connectors`` namespace. Nothing is sent.
                A sign-in arrives as ``OpenSignIn`` and takes a ``SignInAnswer``.
            ObservationLost: The callback is open nowhere, and the session's events could not be read.
        """
        return await answer_callback(
            self._session._host.bind, self._session.id, callback_id, answer, tools=self._session._tools
        )

    @public_errors
    async def interrupt(self) -> Turn | TurnConflict:
        """Stop this turn; the session stays open for new turns.

        Returns ``TurnConflict`` when this turn is no longer the active one.
        """
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


def host_named_turn(session: Session, turn_id: str) -> Turn:
    """The handle of a turn the host named in an answer, such as the running turn of a refused start.
    Its waits and reads take it as running until the session read lists it, as for a turn a send
    returned; ``turn.started`` stays ``None``, since no send started or joined it."""
    turn = Turn(session, turn_id)
    turn._host_named = True
    return turn


def _send_started(receipt: harness_session.MessageSendResponse) -> bool:
    """Whether the send that gave ``receipt`` started its turn rather than joining the running one."""
    if receipt.steered is not None:
        return not receipt.steered
    # Only a control plane or Agent built before receipts said `steered` leaves it out: the
    # in-process Harness is pinned with this SDK. That worker names the message entry and a turn the
    # send opens after the send's command; a send it adds to the running turn keeps that turn's id.
    # A caller-named entry would break this, but `send_message` never names one.
    return receipt.turn_id == receipt.message_entry_id


def _control_plane(deployment: remote_transport.RemoteAgentDeployment) -> str:
    return deployment.server_url.strip().rstrip("/")


def _position(after: TurnState[object] | str | None, session_id: str) -> str | None:
    """The cursor of ``after``. A record or a cursor of another session is refused before any request."""
    if after is None:
        return None
    if isinstance(after, str):
        return _session_cursor(after, session_id)
    if after.session_id != session_id:
        raise InvalidCursorError(
            f"after= is a record of session {after.session_id}, not of {session_id}: pass a record or a cursor "
            "this session gave, or after=None",
            cursor=after.cursor,
        )
    # A record an earlier version gave holds a cursor without the session id.
    return _session_cursor(after.cursor, session_id)


@public_iter_errors
async def _iter_events(
    session: Session, after: TurnState[object] | str | None, *, turn_id: str | None, confirmed: bool = False
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
                raw, session.id, turn_id, tools=session._tools, confirmed=confirmed
            )
            if after is None and start is not None:
                # The host recorded where the previous turn started: read from there, not the session's start.
                cursor = start
            if after is not None and not isinstance(after, str) and active != turn_id:
                # A record taken where the turn does not run, such as the previous turn's result: read
                # from the previous turn's start, as without ``after``, and a loss names it. The
                # notices since the previous turn's end are this turn's, those before the record too,
                # and a cursor between the turns would not say that no turn runs there.
                cursor = start
                active = None
        ends = {} if turn_id is None or state is None or isinstance(state, Running | Blocked) else {turn_id: state}
        events = follow(
            raw,
            transport,
            session.id,
            after=cursor,
            start=cursor,
            active_turn_id=active,
            active_known=not isinstance(after, str),
            tools=session._tools,
            turn_id=turn_id,
            ends=ends,
            confirmed=confirmed,
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


async def _last_turn_start(raw: _RawSession, session_id: str) -> str | None:
    """The position the session's last turn started after.

    ``None`` before its first turn, or when the host records no start: the turn's events are then
    read from the session's start, as ``Turn.result`` reads them.
    """
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
    return last[0].started_after_event_id if last else None


@contextlib.contextmanager
def host_wait_budget(client: _RawSession | None, timeout: float | WaitBudget | None) -> Iterator[WaitBudget]:
    """``timeout`` as the time a wait waits for the host: the time ``client`` answers client tools does not count."""
    budget = timeout if isinstance(timeout, WaitBudget) else WaitBudget(timeout)
    stop = (
        client.watch_answering(budget.pause)
        if isinstance(client, client_tools_registry.ClientToolSessionClient)
        else None
    )
    try:
        yield budget
    finally:
        if stop is not None:
            stop()


async def with_running_answers_sent(
    client: _RawSession | None,
    reader: Session,
    state: TurnState[Any] | Busy,
    output_type: type[BaseModel] | None,
    on_event: EventHandler | None,
    client_tools: ClientToolRegistry,
) -> TurnState[Any] | Busy:
    """Return the turn's record once the client tool answers running now are sent.

    Leaving the wait stops answering: an answer still running would be lost, and its call would wait
    for the host's callback timeout. Once answers were sent, the record is read again: the one from
    the deadline can still show their calls as open. ``reader`` has no approval handler: the wait's
    handler already had its chance at the approvals that record lists.
    """
    try:
        # Also when the turn ended: a subagent's answer can still run.
        sent = await client_tools_registry.finish_answers(client)
        if not sent or not isinstance(state, Running | Blocked):
            return state
        turn = reader.turn(state.turn_id)
        if on_event is None:
            return await turn._get(output_type)
    except (asyncio.CancelledError, KeyboardInterrupt) as error:
        # As a cancel of the wait on the turn: ``turn._result`` below adds its own.
        if isinstance(state, Running | Blocked):
            error.add_note(left_wait_note(state.session_id, state.turn_id))
        raise
    # From the record's position, so ``on_event`` gets the events the answers caused, none twice.
    latest = await turn._result(after=state, timeout=0, on_event=on_event, start=None, client_tools=client_tools)
    return latest if output_type is None else typed(latest, output_type)


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
    on_sign_in: SignInHandler | None = None,
    output_type: type[BaseModel] | None = None,
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
        on_sign_in=on_sign_in,
        output_type=output_type,
    )
    session._tools = tools
    session._client_tools = client_tools
    return session


def remote_session(
    deployment: remote_transport.RemoteAgentDeployment,
    session_id: str,
    *,
    on_approval: ApprovalHandler | None = None,
    on_sign_in: SignInHandler | None = None,
    output_type: type[BaseModel] | None = None,
    tools: Mapping[str, _Tool] = NO_TOOLS,
    client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
) -> Session:
    host = _RemoteHost(deployment)
    host.check(session_id)
    session = Session(session_id, host, on_approval=on_approval, on_sign_in=on_sign_in, output_type=output_type)
    session._tools = tools
    session._client_tools = client_tools
    return session
