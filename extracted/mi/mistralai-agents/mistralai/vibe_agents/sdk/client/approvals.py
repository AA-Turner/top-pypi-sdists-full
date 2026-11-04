"""Session approvals and sign-ins: handlers that answer the approvals and the sign-ins of a session
tree while a call waits.

A handler set with ``on_approval=`` gets an ``ApprovalCallbackContext`` and an ``ApprovalRequest``
for each approval that the session, or one of its subagents, opens, and answers it with
``AllowApproval`` or ``DenyApproval``. ``KeepCallbackOpen()``
leaves the approval open: a wait then returns ``Blocked`` on it. A handler that raises leaves the
approval open too, and the waiting call raises its error; the turn goes on. Any other return,
``None`` or ``True`` included, raises ``SdkError`` that way.

A handler set with ``on_sign_in=`` gets each ``OpenSignIn`` of the tree, and answers it with a
``SignInAnswer``; it returns no ``None`` (that raises ``SdkError``). A handler that raises makes the
waiting call raise, and the sign-in stays open, as for an approval.

The handlers run only while a call waits on the handle (``session.run``, ``turn.result``) or inside
``agent.run``. Between calls, nothing answers: an approval or a sign-in stays open until a call
waits again or someone answers it with ``turn.answer``.

``turn.answer`` answers one approval, one client tool call with the tool's result, or one sign-in
with a ``SignInAnswer``: any open callback of the turn's session or of its subagents, from any turn.
It reads the session once, then answers: ``Answered`` when the callback was open when read, with
the approval answer that counted, ``AlreadySettled`` when it was no longer open, ``NotFound`` when
the session never opened it. A subagent's callback is answered on the subagent's session, found in
the tree's open callbacks. Both kinds of host give the same result.
``agents.KeepCallbackOpen()`` is a handler's return only: ``turn.answer`` raises ``SdkError`` for it
before anything is read.
"""

from __future__ import annotations

import asyncio
import contextlib
import dataclasses
import inspect
import uuid
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable, Callable, Iterable, Mapping
from typing import Any, Protocol, cast

from pydantic import JsonValue, TypeAdapter, ValidationError

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.app_server.session import SessionClient as _RawSession
from mistralai.vibe.harness.app_server.session import SessionTransport
from mistralai.vibe.harness.app_server.session.models import AllowApproval, CallbackKind, DenyApproval
from mistralai.vibe_agents.sdk.authoring import tool as tool_authoring
from mistralai.vibe_agents.sdk.authoring.contracts import CallbackContext, CallbackSession, KeepCallbackOpen
from mistralai.vibe_agents.sdk.authoring.errors import SdkError, described_value
from mistralai.vibe_agents.sdk.client.approval_requests import (
    NO_TOOLS,
    ApprovalRequest,
    ApprovalTool,
    _Tool,
    approval_request,
    tools_by_id,
)
from mistralai.vibe_agents.sdk.client.records import AlreadySettled, Answered, NotFound, ObservationLost, SignInRequest
from mistralai.vibe_agents.sdk.client.sign_ins import (
    SignInAnswer,
    SignInHandler,
    check_sign_in_answer,
    is_sign_in_tool,
    open_sign_in,
    sign_in_output,
    sign_in_requests,
)
from mistralai.vibe_agents.sdk.transport.client_tools import callback_turn_id, given_answer
from mistralai.vibe_agents.sdk.transport.remote import VibeAgentsSessionTransport

__all__ = [
    "AllowApproval",
    "ApprovalCallbackContext",
    "ApprovalHandler",
    "ApprovalRequest",
    "ApprovalTool",
    "Approvals",
    "DenyApproval",
    "WithTools",
    "answer_callback",
    "cancel",
    "with_tools",
]

type _Answer = AllowApproval | DenyApproval | KeepCallbackOpen


class ApprovalCallbackContext(CallbackContext):
    """What an approval handler gets as ``ctx``: the session that asked, and the approval's id.

    ``ctx.session.id`` and ``ctx.session.turn_id`` name the session and turn that asked: a
    subagent's approval has the subagent's session and its own turn there. ``ctx.callback_id`` is the approval's id, the
    one ``turn.answer`` takes. The handler runs in your program, so ``ctx.sandbox`` has no sandbox
    to use.
    """

    def __init__(self, session: CallbackSession, callback_id: str) -> None:
        super().__init__(session)
        self._callback_id = callback_id

    @property
    def callback_id(self) -> str:
        return self._callback_id


class ApprovalHandler(Protocol):
    """A plain or async function of ``(ctx, request)`` that answers an approval: ``AllowApproval``,
    ``DenyApproval``, or ``KeepCallbackOpen()`` to keep it open. Any other return, ``None``
    included, raises ``SdkError``. Its parameters may have any names."""

    def __call__(self, ctx: ApprovalCallbackContext, request: ApprovalRequest, /) -> _Answer | Awaitable[_Answer]: ...


@dataclasses.dataclass(frozen=True, slots=True)
class WithTools:
    """A handler, with the agent's tool objects by tool id: its requests carry the tool."""

    handler: ApprovalHandler
    tools: Mapping[str, _Tool]

    def __call__(self, ctx: ApprovalCallbackContext, request: ApprovalRequest, /) -> _Answer | Awaitable[_Answer]:
        return self.handler(ctx, request)


def with_tools(handler: ApprovalHandler | None, tools: Iterable[_Tool]) -> ApprovalHandler | None:
    """``handler`` with ``tools``, by the id the host gives a tool, ``<namespace>.<name>``. A tool
    id that two different objects share has no tool object."""
    if handler is None:
        return None
    if isinstance(handler, WithTools):
        handler = handler.handler
    return WithTools(handler, tools_by_id(tools))


class Approvals:
    """Answer approvals and sign-ins with their handlers, for one waiting call.

    An approval handler that returns ``KeepCallbackOpen()``, or any handler that raises, leaves its
    callback open; ``changed`` then wakes the waiting call, which reads the turn again or raises the
    handler's error. An approval handler's return that is not an answer raises ``SdkError`` that way.
    """

    def __init__(self, handler: ApprovalHandler | None, *, on_sign_in: SignInHandler | None = None) -> None:
        self._handler = handler
        self._on_sign_in = on_sign_in
        self._tools: Mapping[str, _Tool] = handler.tools if isinstance(handler, WithTools) else NO_TOOLS
        # By session and id: a callback's id is its session's, so two sessions could share one.
        self._left_open: set[tuple[str, str]] = set()
        self._error: Exception | None = None
        self._changed = asyncio.Event()

    def answers(self, kind: str, session_id: str, callback_id: str) -> bool:
        """Whether a handler answers this callback of ``session_id``: an approval, or a sign-in, that
        its handler has not left open."""
        handled = (kind == "approval" and self._handler is not None) or (
            kind == "sign_in" and self._on_sign_in is not None
        )
        return handled and (session_id, callback_id) not in self._left_open

    async def changed(self) -> None:
        """Return when the handler left an approval open or raised since the last call."""
        await self._changed.wait()
        self._changed.clear()

    def raise_error(self) -> None:
        """Raise the error of the handler, if it raised."""
        if self._error is not None:
            raise self._error

    @contextlib.asynccontextmanager
    async def serving(self, raw: _RawSession) -> AsyncIterator[None]:
        """Answer the approvals and sign-ins of ``raw``'s session and its subagents until the block exits."""
        kinds: set[CallbackKind] = set()
        if self._handler is not None:
            kinds.add("approval")
        if self._on_sign_in is not None:
            kinds.add("auth")
        try:
            async with raw.provide_callbacks(
                kinds=kinds,
                handler=self._answer,
            ):
                yield
        except BaseExceptionGroup as group:
            # provide_callbacks runs a TaskGroup, which wraps the error of the block it guards.
            if len(group.exceptions) != 1:
                raise
            [error] = group.exceptions
            raise error from error.__cause__

    @contextlib.asynccontextmanager
    async def serving_session(self, bind: Callable[[str], SessionTransport], session_id: str) -> AsyncIterator[None]:
        """As ``serving``, on a client of its own, ``bind(session_id)``, that reads the session once to attach."""
        async with _RawSession(bind(session_id)) as raw:
            read = await raw.request(
                "app_server/session/read",
                harness_session.SessionReadParams(session_id=session_id),
                harness_session.SessionReadResponse,
            )
            await raw.adopt_session_snapshot(read.state, read.last_event_id)
            async with self.serving(raw):
                yield

    async def _answer(self, callback: harness_session.SessionCallback) -> harness_session.CallbackResult | None:
        requests = sign_in_requests(callback)
        if requests is not None and self._on_sign_in is not None:
            return await self._answer_sign_in(callback, requests, self._on_sign_in)
        if not isinstance(callback, harness_session.ApprovalCallback) or self._handler is None:
            return None
        session_id = cast(str, callback.session_id)
        ctx = ApprovalCallbackContext(CallbackSession(id=session_id, turn_id=callback_turn_id(callback)), callback.id)
        request = approval_request(callback, self._tools)
        try:
            answer = self._handler(ctx, request)
            if inspect.isawaitable(answer):
                answer = await answer
            if not isinstance(answer, AllowApproval | DenyApproval | KeepCallbackOpen):
                raise SdkError(
                    "An approval handler returns agents.AllowApproval, agents.DenyApproval, or "
                    f"agents.KeepCallbackOpen() to keep the approval open, not {described_value(answer)}"
                )
            if not isinstance(answer, KeepCallbackOpen):
                _check_answer(callback, answer)
        except Exception as error:
            # The approval stays open and the turn goes on: the waiting call raises the error.
            error.add_note(
                f"Approval {callback.id} of session {ctx.session.id}, turn {ctx.session.turn_id}, is still open"
            )
            if self._error is None:
                self._error = error
            self._changed.set()
            return None
        if isinstance(answer, KeepCallbackOpen):
            self._left_open.add((session_id, callback.id))
            self._changed.set()
            return None
        return harness_session.CallbackResult(callback_id=callback.id, output=answer.model_dump(mode="json"))

    async def _answer_sign_in(
        self,
        callback: harness_session.SessionCallback,
        requests: tuple[SignInRequest, ...],
        handler: SignInHandler,
    ) -> harness_session.CallbackResult | None:
        session_id = cast(str, callback.session_id)
        sign_in = open_sign_in(callback, requests, session_id, callback_turn_id(callback))
        try:
            answer = handler(sign_in)
            if inspect.isawaitable(answer):
                answer = await answer
            # TODO(sign-in-callback): accept ``agents.KeepCallbackOpen()``, the "keep it open" answer
            # that approval and client tool handlers share, once #71815 is on main.
            if not isinstance(answer, SignInAnswer):
                returned = "None" if answer is None else type(answer).__name__
                raise SdkError(f"A sign-in handler returns SignInAnswer, not {returned}")
            check_sign_in_answer(callback.id, sign_in.requests, answer)
        except Exception as error:
            # The sign-in stays open and the turn goes on: the waiting call raises the error.
            error.add_note(f"Sign-in {callback.id} of session {session_id}, turn {sign_in.turn_id}, is still open")
            if self._error is None:
                self._error = error
            self._changed.set()
            return None
        return harness_session.CallbackResult(callback_id=callback.id, output=sign_in_output(answer))


def refuse_keep_open(answer: object) -> None:
    """Raise ``SdkError`` when ``answer`` is ``KeepCallbackOpen()``: a handler's return, never an answer."""
    if isinstance(answer, KeepCallbackOpen):
        raise SdkError(
            "turn.answer answers the callback: agents.KeepCallbackOpen() is what a handler returns to "
            "leave it open. To leave it open here, do not answer it"
        )


def _check_answer(callback: harness_session.ApprovalCallback, answer: AllowApproval | DenyApproval) -> None:
    # Both hosts refuse it; checked here so that every host says why, before anything is sent.
    if callback.hook is not None and isinstance(answer, AllowApproval) and answer.scope == "session":
        raise ValueError(
            f"Approval {callback.id} was asked by the hook {callback.hook!r}: a hook's approval cannot be "
            "allowed for the session; allow this call once with AllowApproval()"
        )


def check_callback_id(callback_id: str) -> str:
    """``callback_id`` in the canonical UUID form that hosts name callbacks by.

    Raises ``ValueError`` when ``callback_id`` is not a UUID: every host names callbacks by UUID.
    """
    try:
        return str(uuid.UUID(callback_id))
    except (TypeError, ValueError, AttributeError):
        raise ValueError(f"A callback id is a UUID, not {callback_id!r}") from None


async def answer_callback(
    bind: Callable[[str], SessionTransport],
    session_id: str,
    callback_id: str,
    answer: object,
    *,
    tools: Mapping[str, _Tool] = NO_TOOLS,
    in_tree: bool = True,
) -> Answered | AlreadySettled | NotFound:
    """Answer a callback of the session or of one of its subagents: read the session once, then
    send the answer if the callback is open.

    An approval takes ``AllowApproval`` or ``DenyApproval``. A client tool call takes the tool's
    result, checked against the return type of its stub in ``tools`` when there is one. A sign-in
    takes a ``SignInAnswer`` that names each source it asks for, and only those.

    ``bind`` binds a session of the host by id. A callback the session does not have open is
    looked up, with ``in_tree``, in its tree's open callbacks: one that a subagent has open is
    answered on the subagent's session, and the record names that session. A callback open nowhere
    is ``AlreadySettled`` when the session's log, up to its read, has it, else ``NotFound``. A
    callback open at the read is ``Answered``, with ``answer`` the approval answer that counted:
    another client's when it answered first; ``None`` for a client tool call and a sign-in. It is
    ``AlreadySettled`` when it closed without an answer since the read.

    Raises:
        ValueError: ``callback_id`` is not a UUID (nothing is read or sent).
        SdkError: ``answer`` is ``KeepCallbackOpen()``, a handler's return only (nothing is read or
            sent). Or the callback is open but ``answer`` is not an answer of its kind, a client
            tool's result does not match its stub's return type, ``answer`` allows a hook's approval
            for the session, or a sign-in answer names a source the sign-in does not ask for or
            leaves out one it asks for; the callback is not an approval, a client tool call or a
            sign-in, or is a call of another tool the host provides; or two subagents have a
            callback open with that id. Nothing is sent.
        ObservationLost: The callback is open nowhere, and the session's events could not be read.
    """
    refuse_keep_open(answer)
    callback_id = check_callback_id(callback_id)
    transport = bind(session_id)
    async with _RawSession(transport) as raw:
        read = await raw.request(
            "app_server/session/read",
            harness_session.SessionReadParams(session_id=session_id),
            harness_session.SessionReadResponse,
        )
        callback = next((open_ for open_ in read.state.active_callbacks if open_.id == callback_id), None)
        if callback is not None:
            return await _answer_open(raw, transport, session_id, callback, answer, tools, read.last_event_id)
        owner = await _subagent_owner(raw, session_id, callback_id) if in_tree else None
        if owner is None:
            if await _logged(transport, session_id, callback_id, until=read.last_event_id):
                return AlreadySettled(session_id=session_id, callback_id=callback_id)
            return NotFound(session_id=session_id, callback_id=callback_id)
    # The subagent's own session reads and answers it.
    return await answer_callback(bind, owner, callback_id, answer, tools=tools, in_tree=False)


async def _subagent_owner(raw: _RawSession, session_id: str, callback_id: str) -> str | None:
    """The subagent session of ``session_id``'s tree that has ``callback_id`` open, if one has.

    ``None`` from a host that cannot list the tree, such as a control plane older than its
    callbacks route.

    Raises:
        SdkError: Two subagents have a callback open with that id: a callback's id is its
            session's, so the session must be named.
    """
    try:
        tree = await raw.request(
            "app_server/session/callbacks/tree",
            harness_session.CallbacksTreeParams(session_id=session_id),
            harness_session.CallbacksTreeResponse,
        )
    except harness_session.UnsupportedSessionProcedureError:
        return None
    owners = sorted(
        {
            item.session_id
            for item in tree.callbacks
            if item.callback.id == callback_id and item.session_id != session_id
        }
    )
    if len(owners) > 1:
        raise SdkError(
            f"Callback {callback_id} is open in {len(owners)} subagents of session {session_id}: "
            f"{', '.join(owners)}; answer it on its own session, agent.session(session_id).turn(turn_id).answer(...)"
        )
    return owners[0] if owners else None


async def _answer_open(
    raw: _RawSession,
    transport: SessionTransport,
    session_id: str,
    callback: harness_session.SessionCallback,
    answer: object,
    tools: Mapping[str, _Tool],
    read_at: str,
) -> Answered | AlreadySettled:
    """Answer ``callback``, open in the session when it was read at ``read_at``."""
    callback_id = callback.id
    result = _given_result(callback, answer, session_id, tools)
    settled = False
    try:
        await raw.request(
            "app_server/session/callback/result",
            harness_session.CallbackResultParams(session_id=session_id, result=result),
            harness_session.CallbackResultResponse,
        )
    except harness_session.SessionCallbackSettledError:
        # Open at the read, so it closed since: answered by another client, or its turn ended.
        settled = True
    outcome = await _resolution(transport, session_id, callback_id, after=read_at)
    if not isinstance(outcome, harness_session.AnsweredCallbackOutcome):
        if settled or not (outcome is None or isinstance(outcome, harness_session.UnknownCallbackOutcome)):
            # It closed without an answer: timed out, cancelled or failed.
            return AlreadySettled(session_id=session_id, callback_id=callback_id)
        # The answer was taken, but the log did not show the resolve in time, or showed an outcome
        # from a newer host that this SDK cannot read.
        return Answered(session_id=session_id, callback_id=callback_id, answer=None)
    # No host logs which result of a client tool call or a sign-in counted: only an approval's answer is known.
    applied = _applied(outcome.output) if isinstance(callback, harness_session.ApprovalCallback) else None
    return Answered(session_id=session_id, callback_id=callback_id, answer=applied)


def _given_result(
    callback: harness_session.SessionCallback, answer: object, session_id: str, tools: Mapping[str, _Tool]
) -> harness_session.CallbackResult:
    """What ``turn.answer`` sends for ``answer`` to ``callback``, checked for the callback's kind."""
    if (requests := sign_in_requests(callback)) is not None:
        # A sign-in is a client tool call of the host's: it takes a SignInAnswer, never a raw result.
        if not isinstance(answer, SignInAnswer):
            raise SdkError(
                f"Callback {callback.id} of session {session_id} is a sign-in: answer it with SignInAnswer, "
                f"not {type(answer).__name__}"
            )
        check_sign_in_answer(callback.id, requests, answer)
        return harness_session.CallbackResult(callback_id=callback.id, output=sign_in_output(answer))
    match callback:
        case harness_session.ApprovalCallback():
            if not isinstance(answer, AllowApproval | DenyApproval):
                raise SdkError(
                    f"Callback {callback.id} of session {session_id} is an approval: answer it with "
                    f"AllowApproval or DenyApproval, not {type(answer).__name__}"
                )
            try:
                _check_answer(callback, answer)
            except ValueError as error:
                raise SdkError(str(error)) from None
            return harness_session.CallbackResult(callback_id=callback.id, output=answer.model_dump(mode="json"))
        case harness_session.ClientToolCallback():
            namespace, _, _ = callback.name.partition(".")
            if tool_authoring.is_reserved_namespace(namespace) or is_sign_in_tool(callback.name):
                # The Harness opens the same callback kind for its provided tools, whose answer is
                # not a tool result. A sign-in has its own kind, answered above; a call under a
                # sign-in tool name is refused too, Le Chat's un-namespaced one included.
                raise SdkError(
                    f"Callback {callback.id} of session {session_id} is a call of {callback.name}, a tool "
                    "the host provides: turn.answer answers approvals, sign-ins and your own client tools' calls"
                )
            return given_answer(callback, answer, tools.get(callback.name))
        case _:
            raise SdkError(
                f"Callback {callback.id} of session {session_id} is a {callback.kind} callback: "
                "turn.answer answers approvals, client tool calls and sign-ins"
            )


_RESOLVE_SECONDS = 10.0
# How long a read of the session's log waits for a next item, once its stream is open, before it
# takes the log as quiet: a stream never says that it has no more events.
_QUIET_SECONDS = 1.0

_ANSWER: TypeAdapter[AllowApproval | DenyApproval] = TypeAdapter(AllowApproval | DenyApproval)


def _applied(output: JsonValue) -> AllowApproval | DenyApproval | None:
    """The approval answer that a resolved callback's outcome holds, or ``None`` when it holds none."""
    try:
        return _ANSWER.validate_python(output)
    except ValidationError:
        return None


async def _resolution(
    transport: SessionTransport, session_id: str, callback_id: str, *, after: str
) -> harness_session.CallbackOutcome | None:
    """How the callback was resolved, from the session's log after ``after``.

    A host can log the resolve after it replies to the answer, so this follows the log for it, for
    ``_RESOLVE_SECONDS`` at most, or until the log is quiet. ``None`` when no resolve shows, when it
    has no outcome, or when the log cannot be read: the answer was sent already, so a lost read only
    loses which answer counted.
    """
    try:
        read, opening = _read_log(
            transport, harness_session.EventsReadParams(session_id=session_id, after_event_id=after)
        )
        # Both transports return an async generator: close it when the reader stops.
        async with (
            contextlib.aclosing(read) as stream,  # type: ignore[type-var]
            contextlib.aclosing(_positions(stream)) as positions,
            # No event id is empty: this reads until the resolve, a quiet log or the budget.
            contextlib.aclosing(_up_to(positions, "", budget=_RESOLVE_SECONDS, opening=opening)) as items,
        ):
            async for _, payload in items:
                match payload:
                    case harness_session.CallbackResolvedEvent(callback_id=resolved, outcome=outcome) if (
                        resolved == callback_id
                    ):
                        return outcome
    except harness_session.SessionEventStreamLostError:
        return None
    return None


async def _logged(transport: SessionTransport, session_id: str, callback_id: str, *, until: str) -> bool:
    """Whether the session's log, from its start up to ``until``, has the callback opened or resolved."""
    cursor: str | None = None
    try:
        read, opening = _read_log(transport, harness_session.EventsReadParams(session_id=session_id))
        # Both transports return an async generator: close it when the reader stops.
        async with (
            contextlib.aclosing(read) as stream,  # type: ignore[type-var]
            contextlib.aclosing(_positions(stream)) as positions,
            contextlib.aclosing(_up_to(positions, until, opening=opening)) as items,
        ):
            async for cursor, payload in items:
                match payload:
                    case harness_session.CallbackOpenedEvent(callback=callback) if callback.id == callback_id:
                        return True
                    case harness_session.CallbackResolvedEvent(callback_id=resolved) if resolved == callback_id:
                        return True
    except harness_session.SessionEventStreamLostError as error:
        raise ObservationLost(session_id, cursor) from error
    return False


def _read_log(
    transport: SessionTransport, params: harness_session.EventsReadParams
) -> tuple[AsyncIterator[harness_session.ClientTransportStreamItem], _StreamOpening | None]:
    """The session's log from ``params``, with the ``_StreamOpening`` its stream tells on a deployment.

    A deployment rebuilds the session before its stream opens, so ``up_to`` does not take that wait
    for a quiet log. A stream in this process has no such wait: ``None``.
    """
    if isinstance(transport, VibeAgentsSessionTransport):
        opening = _StreamOpening()
        return transport.read_events(params, on_open=opening.open), opening
    return transport.read_events(params), None


async def _positions(
    stream: AsyncIterator[harness_session.ClientTransportStreamItem],
) -> AsyncGenerator[tuple[str, object]]:
    """Each position of the session's log with its event's payload, or ``None`` for a frame with no event."""
    async for item in stream:
        match item:
            case harness_session.TransportHeartbeat(latest_event_id=str(position)):
                yield position, None
            case harness_session.EventBatch(events=events):
                for event in events:
                    yield event.event_id, event.payload
            case harness_session.Event():
                yield item.event_id, item.payload


async def cancel(*tasks: asyncio.Future[Any]) -> None:
    """Cancel the tasks that are not done, and wait until they are."""
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


class _StreamOpening:
    """Whether a log read's stream is open yet: ``_up_to``'s ``_QUIET_SECONDS`` start only then.

    A deployment's stream opens when the server accepts it, after the reads that rebuild the session
    and the connection itself. No event comes while it opens, and that time is not a quiet log.
    """

    def __init__(self) -> None:
        self.opened = False
        # The limit of the wait for an item that is running, if any.
        self.waiting: asyncio.Timeout | None = None

    def open(self) -> None:
        """The stream is open: a wait for an item started before gets ``_QUIET_SECONDS`` from now."""
        if self.opened:
            return
        self.opened = True
        if (waiting := self.waiting) is not None:
            quiet = asyncio.get_running_loop().time() + _QUIET_SECONDS
            waiting.reschedule(quiet if (when := waiting.when()) is None else min(when, quiet))


async def _up_to[T](
    items: AsyncIterator[tuple[str, T]],
    position: str,
    *,
    budget: float | None = None,
    opening: _StreamOpening | None = None,
) -> AsyncGenerator[tuple[str, T]]:
    """The log's items up to ``position``; also stops at the stream's end, once the open stream
    gives nothing for ``_QUIET_SECONDS``, or with ``budget``, after reading for that long in all.

    The time the caller takes with each item does not count. With ``opening``, the time the stream
    takes to open counts only against ``budget``.
    """
    loop = asyncio.get_running_loop()
    left = _QUIET_SECONDS if budget is None else budget
    while left > 0:
        started = loop.time()
        seconds: float | None = min(left, _QUIET_SECONDS)
        if opening is not None and not opening.opened:
            # Until the stream opens, only the budget bounds the wait.
            seconds = None if budget is None else left
        if (item := await _next_within(items, seconds, opening=opening)) is None:
            return
        if budget is not None:
            left -= loop.time() - started
        yield item
        if item[0] == position:
            return


async def _next_within[T](
    items: AsyncIterator[T], seconds: float | None, *, opening: _StreamOpening | None = None
) -> T | None:
    """The next of ``items``, or ``None`` at their end or when none comes within ``seconds``.

    If the stream opens meanwhile, ``opening`` brings the limit to ``_QUIET_SECONDS`` from then.
    """
    deadline = asyncio.timeout(seconds)
    try:
        async with deadline:
            if opening is not None and not opening.opened:
                opening.waiting = deadline
            return await anext(items)
    except StopAsyncIteration:
        return None
    except TimeoutError:
        if deadline.expired():
            return None
        raise
    finally:
        if opening is not None:
            opening.waiting = None
