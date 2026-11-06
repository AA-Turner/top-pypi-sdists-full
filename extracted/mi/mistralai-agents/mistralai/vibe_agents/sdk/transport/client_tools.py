"""Answer Harness client-tool callbacks from the process that opened the Session."""

import asyncio
import functools
import weakref
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable, Iterator, Mapping, Set
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Never, Protocol, cast

import structlog
from pydantic import JsonValue, ValidationError
from pydantic_core import PydanticSerializationError

from mistralai.vibe.harness.app_server.session import (
    CallbackResult,
    ClientToolCallback,
    EventId,
    ProtocolError,
    SessionCallback,
    SessionCallbackSettledError,
    SessionClient,
    SessionId,
    SessionState,
    SessionTransport,
)
from mistralai.vibe.harness.app_server.session.models import AllowApproval, DenyApproval
from mistralai.vibe.harness.app_server.session.procedures.session import CallbackResultResponse
from mistralai.vibe.harness.runtime.capabilities import ProvidedToolInvocationFailed
from mistralai.vibe.harness.runtime.content import to_session_content
from mistralai.vibe_agents.sdk.assembly import assemble, tool_results
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring import tool as tool_authoring
from mistralai.vibe_agents.sdk.authoring.errors import (
    ClientToolAnswerError,
    SdkError,
    sdk_runtime_error,
)
from mistralai.vibe_agents.sdk.authoring.keep_open import KeepCallbackOpen
from mistralai.vibe_agents.sdk.authoring.tool_errors import (
    DEFAULT_TOOL_ERRORS,
    ToolCodeError,
    ToolError,
    ToolErrors,
    ToolFunctionError,
    call_is_cancelling,
    failed_tool_result,
)
from mistralai.vibe_agents.sdk.authoring.tool_errors import logger as tool_error_logger
from mistralai.vibe_agents.sdk.authoring.tool_result import is_rich_tool_result

logger = structlog.get_logger(__name__)

# Answers kept after they finish, so a restarted loop that still sees their call pending resends
# them instead of calling the answer function again. Past this, the oldest finished ones go, those
# already sent first.
_KEPT_ANSWERS = 256

# After the answering loop fails, it restarts after 0.5 s, then twice as long each time, up to this.
_MAX_RESTART_DELAY = 10.0


@dataclass(slots=True)
class _LeftOpenCalls:
    """The client tool calls that a registry's answers left open, and the waits to wake when one is."""

    # Not bounded: a call dropped while still open would make a wait wait for an answer no handler sends.
    # One leaves when the registry answers it again, not when it settles otherwise: such an entry is
    # harmless, as a wait looks only at the callbacks the host lists as open. The set lives as long as
    # the registry: one run, or the client of create_session.
    calls: set[tuple[SessionId, str]] = field(default_factory=set)
    watchers: set[asyncio.Event] = field(default_factory=set)

    def add(self, key: tuple[SessionId, str]) -> None:
        self.calls.add(key)
        for watcher in self.watchers:
            watcher.set()


def left_open(client_tools: "ClientToolRegistry", session_id: str, callback_id: str) -> bool:
    """Whether an answer or the ``on_client_tool`` of ``client_tools`` kept the call open with
    ``agents.KeepCallbackOpen()``."""

    return (session_id, callback_id) in client_tools._left_open.calls


@contextmanager
def watching_left_open(client_tools: "ClientToolRegistry") -> Iterator[asyncio.Event]:
    """An event set each time an answer of ``client_tools`` leaves a client tool call open, until the block exits."""

    left = client_tools._left_open
    event = asyncio.Event()
    left.watchers.add(event)
    try:
        yield event
    finally:
        left.watchers.discard(event)


@dataclass(slots=True)
class _SharedAnswer:
    """One call's answer, shared by the clients of an event loop that see the call open.

    Two waits that run at once, on one handle or on a parent's and a subagent's, each open a client
    that sees the same open call. The first one starts the answer function; the others wait for it and
    send the same result, so the function runs once and every wait ends as it would alone.
    """

    task: asyncio.Task[CallbackResult | KeepCallbackOpen | None]
    # The exception the function raised with tool_errors="raise", if it did: each client raises it to its caller.
    raised: list[ToolCodeError] = field(default_factory=list)
    # The clients using it, from its start until each sent its result or left. When the last one is
    # done it is forgotten, and cancelled if it still runs.
    users: int = 0


# The answers of each event loop, by the Session that opened the call and the call's id.
_SHARED_ANSWERS: weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, dict[tuple[SessionId, str], _SharedAnswer]] = (
    weakref.WeakKeyDictionary()
)


def _shared_answers() -> dict[tuple[SessionId, str], _SharedAnswer]:
    return _SHARED_ANSWERS.setdefault(asyncio.get_running_loop(), {})


def _release_shared_answer(
    answers: dict[tuple[SessionId, str], _SharedAnswer], key: tuple[SessionId, str], shared: _SharedAnswer
) -> bool:
    """A client is done with ``shared``: it sent its result, the send failed, or it left. Once no
    client uses it, forget it, so a later wait calls the function again, as it would with no other
    client; cancel it if it still runs, and return whether it was cancelled."""

    shared.users -= 1
    if shared.users > 0:
        return False
    if answers.get(key) is shared:
        del answers[key]
    if shared.task.done():
        return False
    shared.task.cancel()
    return True


@dataclass(frozen=True, slots=True)
class ClientToolCall:
    """One call of a client tool, as ``on_client_tool`` receives it and ``OpenClientToolCall.call`` holds it.

    ``name`` is the tool's ID, its namespace then the name it was declared with, such as
    ``client.get_weather`` (``client`` is the default namespace) or ``ui.get_location``: the same
    as ``agents.ToolCall.name`` in ``Completed.tool_calls``.
    ``arguments`` holds the call's arguments, not validated: the model's, or the ones a
    ``pre_tool_call`` hook set. The handler checks them.

    A tool with its own answer in ``agents.ClientToolAnswers`` never reaches the default handler:
    its answer wins.
    """

    name: str
    """The tool's ID, its namespace then the name it was declared with, such as
    ``client.get_weather`` (``client`` is the default namespace) or ``ui.get_location``: the same
    as ``agents.ToolCall.name`` in ``Completed.tool_calls``."""
    arguments: JsonValue
    """The call's arguments, not validated: the model's, or the ones a ``pre_tool_call`` hook set.
    The handler checks them."""


def client_tool_call(callback: ClientToolCallback) -> ClientToolCall:
    """The call that ``callback`` asks the program to answer."""

    return ClientToolCall(name=callback.name, arguments=callback.input)


class ClientToolHandler(Protocol):
    """Answers any client tool call: returns the result the model reads, synchronously or not, or
    ``agents.KeepCallbackOpen()`` to keep the call open. ``None`` is a result: the model reads
    ``null``. Its parameter may have any name."""

    def __call__(self, call: ClientToolCall, /) -> object | Awaitable[object]: ...


class ClientToolAnswers:
    """Your functions that answer client tools, one per tool, and a default for every other call.

    Pass it as ``on_client_tool=`` to ``agent.run``, ``agent.start_session`` or ``agent.session(id)``::

        answers = agents.ClientToolAnswers(get_location.answer(read_gps), default=handle)
        state = await agent.run("Find a shop near me", on_client_tool=answers)

    Each answer comes from ``<tool>.answer(function)``, which a type checker checks against the
    tool's stub. ``default`` gets the calls of every other client tool, as a plain
    ``on_client_tool=`` handler does: a tool's own answer wins over it.

    A plain function runs in a separate thread, so a blocking call such as ``input()`` does not stop
    the session. An ``async def`` one runs on the event loop: do not block in it. The answers also
    get the client tool calls of the session's subagents.

    Raises ``SdkError`` here when two answers are for the same tool. Before the session starts, the
    agent raises ``SdkError`` for an answer to a stub that is not one of its tools or its subagents'.
    A deployed agent loaded with ``Agent.load_from`` skips that check: it has no tool objects.

    Args:
        answers: The answers, each from ``<tool>.answer(function)``, one per tool.
        default: The handler of every other client tool call. ``None`` leaves those calls open: the
            run returns ``Blocked``.
    """

    __slots__ = ("_answers", "_default")

    def __init__(
        self, *answers: tool_authoring.ClientToolAnswer[..., Any], default: ClientToolHandler | None = None
    ) -> None:
        by_id: dict[str, tool_authoring.ClientToolAnswer[..., Any]] = {}
        for answer in answers:
            if not isinstance(answer, tool_authoring.ClientToolAnswer):
                raise SdkError(
                    f"{ClientToolAnswers.__name__} takes the answers that <tool>.answer(function) returns, "
                    f"got {type(answer).__name__}"
                )
            # The call arrives under the tool's ID, `<namespace>.<name>`.
            tool_id = f"{answer.tool.namespace}.{answer.tool.name}"
            if tool_id in by_id:
                raise SdkError(f"{ClientToolAnswers.__name__} answers {tool_id!r} twice")
            by_id[tool_id] = answer
        if default is not None and not callable(default):
            raise SdkError(f"default takes a function, got {type(default).__name__}")
        self._answers: Mapping[str, tool_authoring.ClientToolAnswer[..., Any]] = MappingProxyType(by_id)
        self._default = default

    def __repr__(self) -> str:
        answered = ", ".join(self._answers)
        return f"{ClientToolAnswers.__name__}({answered}, default={self._default!r})"


type OnClientTool = ClientToolHandler | ClientToolAnswers
"""What ``on_client_tool=`` takes: one handler for every client tool call, or ``ClientToolAnswers``."""


@dataclass(frozen=True, slots=True)
class ClientToolRegistry:
    """The answers a Session gives its client tools: by tool name, then the one generic handler."""

    answers: Mapping[str, tool_authoring.ClientToolAnswer[..., Any]] = field(
        default_factory=lambda: MappingProxyType({})
    )
    on_client_tool: ClientToolHandler | None = None
    # What the model sees when an answer or the handler raises anything but agents.ToolError. With
    # "raise", the model sees nothing: the call stays open and the exception raises in the program.
    tool_errors: ToolErrors = DEFAULT_TOOL_ERRORS
    # The calls these answers left open, for the waits of the same run: a run with other answers
    # starts with none.
    _left_open: _LeftOpenCalls = field(default_factory=_LeftOpenCalls, init=False, repr=False, compare=False)

    def __bool__(self) -> bool:
        return bool(self.answers) or self.on_client_tool is not None

    def covers(self, name: str) -> bool:
        """Whether the call of the client tool with this ID gets an answer from this process: its own
        answer, else ``on_client_tool`` for a tool in a namespace an author can use."""

        return name in self.answers or (self.on_client_tool is not None and _is_program_tool(name))


NO_CLIENT_TOOLS = ClientToolRegistry()


def build_client_tool_registry(
    on_client_tool: OnClientTool | None,
    *,
    tool_errors: ToolErrors = DEFAULT_TOOL_ERRORS,
) -> ClientToolRegistry:
    """Index the client tool answers by the name the model's call arrives under."""

    if on_client_tool is None:
        return ClientToolRegistry(tool_errors=tool_errors)
    if isinstance(on_client_tool, ClientToolAnswers):
        return ClientToolRegistry(
            answers=on_client_tool._answers, on_client_tool=on_client_tool._default, tool_errors=tool_errors
        )
    if isinstance(on_client_tool, tool_authoring.ClientToolAnswer):
        raise SdkError(
            f"on_client_tool takes a function or agents.{ClientToolAnswers.__name__}, got the answer to "
            f"{on_client_tool.tool.name!r}: pass agents.{ClientToolAnswers.__name__}(...) with it"
        )
    if not callable(on_client_tool):
        raise SdkError(
            f"on_client_tool takes a function or agents.{ClientToolAnswers.__name__}, "
            f"got {type(on_client_tool).__name__}"
        )
    return ClientToolRegistry(on_client_tool=on_client_tool, tool_errors=tool_errors)


def check_answered_tools(on_client_tool: OnClientTool | None, tools: Iterable[object]) -> None:
    """Raise ``SdkError`` when ``on_client_tool`` answers a stub that is not in ``tools``.

    The stub itself must be there, not only a tool with the same ID: an answer to a tool the agent
    does not have would never be called.
    """

    if not isinstance(on_client_tool, ClientToolAnswers):
        return
    known = {id(tool) for tool in tools}
    for tool_id, answer in on_client_tool._answers.items():
        if id(answer.tool) not in known:
            raise SdkError(
                f"on_client_tool answers {tool_id!r}, which is not a tool of this Agent, of its guardrails "
                "and hooks, or of its subagents: add the stub to tools="
            )


class ClientToolSessionClient(SessionClient):
    """A Session that answers its client tools, and its subagents', in-process.

    The answers are served from the moment the Session is attached until the client closes.
    """

    def __init__(
        self,
        transport: SessionTransport,
        *,
        client_tools: ClientToolRegistry = NO_CLIENT_TOOLS,
    ) -> None:
        super().__init__(transport)
        self._client_tools = client_tools
        self._closing = asyncio.Event()
        self._answering: asyncio.Task[None] | None = None
        # Each call's answer, computed once, keyed by the Session that opened the call and the
        # call's id. A restarted loop resends it instead of calling again, even after a send that
        # succeeded but whose settlement the loop has not seen yet. None: no answer, the call stays
        # open (an exception with tool_errors="raise", or agents.KeepCallbackOpen()).
        self._answers: dict[tuple[SessionId, str], asyncio.Task[CallbackResult | None]] = {}
        # The answers in `_answers` that the transport accepted, which `_forget_old_answers` drops first.
        self._sent: set[tuple[SessionId, str]] = set()
        # The turn of each call in `_answers`, to name it when its answer cannot be sent.
        self._turns: dict[tuple[SessionId, str], str] = {}
        # The first answer that could not be sent: the answering stops, and a run raises it.
        self._send_failure: ClientToolAnswerError | None = None
        # Set once a caller got the error of the failed answers, so close does not raise it again.
        self._failure_raised = False
        # The answers started and not sent yet, each done once sent or once its call settled: a run waits for them.
        self._unsent: dict[tuple[SessionId, str], asyncio.Future[None]] = {}
        # The answers running their code, not sent yet: a run's timeout does not count them.
        self._in_code: set[asyncio.Task[Any]] = set()
        self._answering_watchers: list[Callable[[bool], None]] = []
        # Set when a run is leaving: no new answer starts, but those started are still sent.
        self._draining = False
        # The first exception an answer raised with tool_errors="raise" that no caller took yet, and
        # the Session whose call it left open.
        self._raised: tuple[ToolCodeError, SessionId] | None = None
        self._raised_set = asyncio.Event()

    @property
    def upload_file(self) -> Never:
        # The Harness's inherited helper is not part of the SDK's non-experimental API.
        raise AttributeError(
            "upload_file is only available through mistralai.agents.experimental.session_protocol: "
            "use session_protocol.attach(agent.session(client.session_id)).upload_file(...)"
        )

    async def adopt_session_snapshot(self, state: SessionState, last_event_id: EventId) -> None:
        await super().adopt_session_snapshot(state, last_event_id)
        if self._client_tools and self._answering is None:
            # provide_callbacks must be entered and left in the same task, and a client is often
            # opened and closed from different ones.
            self._answering = asyncio.create_task(self._answer_until_closed(), name=f"client-tools:{self.session_id}")

    async def answer_callback(
        self, result: CallbackResult, *, session_id: SessionId | None = None
    ) -> CallbackResultResponse:
        key = (session_id or self.session_id, result.callback_id)
        try:
            response = await super().answer_callback(result, session_id=session_id)
        except SessionCallbackSettledError:
            # Settled: no loop will see this call pending again.
            self._answers.pop(key, None)
            self._turns.pop(key, None)
            self._sent.discard(key)
            self._mark_sent(key)
            raise
        except Exception as error:
            if key not in self._answers:
                raise
            # An answer this client computed: name its call, so a run can say which one failed.
            failure = ClientToolAnswerError(callback_id=key[1], session_id=key[0], turn_id=self._turns[key])
            if self._send_failure is None:
                self._send_failure = failure
            self._mark_sent(key)
            raise failure from error
        self._mark_sent(key)
        if key in self._answers:
            self._sent.add(key)
            # A burst of answers may all be created before any is sent: drop the excess once they are.
            self._forget_old_answers()
        return response

    async def close(self) -> None:
        try:
            if self._answering is not None:
                self._closing.set()
                if self._failure_raised:
                    await asyncio.gather(self._answering, return_exceptions=True)
                else:
                    try:
                        await self._answering
                    except BaseExceptionGroup as group:
                        error = _answers_failed(group)
                        raise error from error.__cause__
        finally:
            answers = tuple(self._answers.values())
            self._answers.clear()
            self._turns.clear()
            self._sent.clear()
            for task in answers:
                task.cancel()
            await asyncio.gather(*answers, return_exceptions=True)
            for key in tuple(self._unsent):
                self._mark_sent(key)
            await super().close()

    def watch_answering(self, watcher: Callable[[bool], None]) -> Callable[[], None]:
        """Call ``watcher(True)`` when the client starts running an answer's code while it runs none,
        and ``watcher(False)`` once it runs none again; at once if it runs one now. Sending an answer
        is not running its code. Return the call that stops watching."""

        self._answering_watchers.append(watcher)
        if self._in_code:
            watcher(True)
        return lambda: self._answering_watchers.remove(watcher)

    def _running_code(self, task: asyncio.Task[Any], running: bool) -> None:
        was = bool(self._in_code)
        if running:
            self._in_code.add(task)
        else:
            self._in_code.discard(task)
        if bool(self._in_code) != was:
            for watcher in tuple(self._answering_watchers):
                watcher(not was)

    async def finish_answers(self) -> bool:
        """Wait until the answers running now are sent; return whether there were any.

        A call whose answer has not started yet is not waited for, and none starts from now on. When
        an answer cannot be sent, raise its error, ``ClientToolAnswerError``.
        """

        # The run is leaving: a call that opens from now on is not answered.
        self._draining = True
        running = [waiter for waiter in self._unsent.values() if not waiter.done()]
        if running:
            await asyncio.wait(running)
        if self._send_failure is not None:
            # Here, not when the client closes: its task group would wrap the error.
            self._failure_raised = True
            raise self._send_failure from self._send_failure.__cause__
        return bool(running)

    async def _answer_until_closed(self) -> None:
        """Serve the client tools until the client closes, restarting the loop after a failure.

        A failure, for example a lost event stream, would otherwise stop the loop and leave every
        later call pending until the turn times out. Restarted, the loop reads the pending calls
        again and sends each one the answer it already computed: the answer function runs once per
        call. An answer that cannot be sent stops the loop instead: its ``ClientToolAnswerError``
        ends the answering, and a run waiting on the turn raises it.
        """

        loop = asyncio.get_running_loop()
        failures = 0
        while not self._closing.is_set():
            started = loop.time()
            try:
                async with self.provide_callbacks(
                    kinds={"client_tool"}, handler=self._answer, on_pending=self._forget_settled
                ):
                    await self._closing.wait()
            except Exception as error:  # noqa: BLE001 - logged, then the loop restarts unless a send failed
                if self._send_failure is not None:
                    raise
                # A loop that served for a while starts its delays over.
                failures = 1 if loop.time() - started > _MAX_RESTART_DELAY else failures + 1
                delay = min(0.5 * 2 ** (failures - 1), _MAX_RESTART_DELAY)
                logger.warning(
                    "Client tool answering failed; restarting it",
                    session_id=self.session_id,
                    restart_in_seconds=delay,
                    exc_info=error,
                )
                try:
                    await asyncio.wait_for(self._closing.wait(), timeout=delay)
                except TimeoutError:
                    continue

    async def _answer(self, callback: SessionCallback) -> CallbackResult | None:
        if not isinstance(callback, ClientToolCallback):
            return None
        # The tool's own answer first, then the one handler for every client tool.
        answer = self._client_tools.answers.get(callback.name)
        handler = self._client_tools.on_client_tool
        key = (callback.session_id or self.session_id, callback.id)
        run: Callable[[], Awaitable[object]]
        if answer is not None:
            run = functools.partial(_run_answer, answer, callback, key[0])
        elif handler is not None and _is_program_tool(callback.name):
            # Only the program's own client tools, in any namespace an author can use: the Harness
            # opens the same callback kind for its provided tools.
            run = functools.partial(_run_handler, handler, callback)
        else:
            # A provided tool, another client tool, or a caller answering this one itself.
            return None
        computed = self._answers.get(key)
        if computed is None:
            if self._draining:
                # A run that is leaving starts no new answer.
                return None
            turn_id = callback_turn_id(callback)
            computed = asyncio.create_task(
                self._compute(callback, run, key[0]), name=f"client-tool:{key[0]}:{callback.id}"
            )
            self._answers[key] = computed
            # Answered again here: a wait no longer returns on it as left open.
            self._client_tools._left_open.calls.discard(key)
            self._turns[key] = turn_id
            self._unsent.setdefault(key, asyncio.get_running_loop().create_future())
            self._forget_old_answers()
        # Shielded: a failing loop cancels its handlers, but not the answer the next loop sends.
        return await asyncio.shield(computed)

    async def _compute(
        self, callback: ClientToolCallback, run: Callable[[], Awaitable[object]], session_id: SessionId
    ) -> CallbackResult | None:
        # While its code runs, a run's timeout does not count; sending is waiting for the host, and counts.
        task = asyncio.current_task()
        if task is not None:
            self._running_code(task, True)
        key = (session_id, callback.id)
        answers = _shared_answers()
        shared = answers.get(key)
        if shared is None:
            # The first client of this event loop to see the call open runs the answer function.
            raised: list[ToolCodeError] = []
            shared = answers[key] = _SharedAnswer(
                asyncio.create_task(
                    _invoke(callback, run, tool_errors=self._client_tools.tool_errors, on_raise=raised.append),
                    name=f"client-tool-answer:{session_id}:{callback.id}",
                ),
                raised,
            )
        shared.users += 1
        release = functools.partial(_release_shared_answer, answers, key, shared)
        sending = False
        try:
            # Shielded: a client that leaves does not cancel the answer another client waits for.
            result = await asyncio.shield(shared.task)
            for error in shared.raised:
                self._keep_raised(error, session_id=session_id)
            if isinstance(result, KeepCallbackOpen):
                # No answer: the call stays open, and a wait returns Blocked on it.
                self._client_tools._left_open.add(key)
                result = None
            if result is None:
                # It raised with tool_errors="raise", or it left the call open: no answer is sent, so a
                # run does not wait for one.
                self._mark_sent(key)
            unsent = self._unsent.get(key)
            if unsent is not None and not unsent.done():
                # Kept until this client sent it, so a client that sees the call open meanwhile sends
                # the same result rather than calling the function again.
                unsent.add_done_callback(lambda _: release())
                sending = True
            return result
        finally:
            if task is not None:
                self._running_code(task, False)
            if not sending and release():
                # The last client left while the function ran: wait for its cleanup, as closing does.
                await asyncio.gather(shared.task, return_exceptions=True)

    def _forget_settled(self, pending: Set[tuple[SessionId, str]]) -> None:
        """Stop waiting for the answers whose call is no longer pending: nothing will send them.

        Not on a handler's cancel: a failing loop cancels its handlers too, and the restarted loop
        must still send their answers.
        """

        for key in tuple(self._unsent):
            if key not in pending:
                self._mark_sent(key)

    def _mark_sent(self, key: tuple[SessionId, str]) -> None:
        waiter = self._unsent.pop(key, None)
        if waiter is not None and not waiter.done():
            waiter.set_result(None)

    def _keep_raised(self, error: ToolCodeError, *, session_id: SessionId) -> None:
        """Keep the first exception an answer raised with tool_errors="raise", for ``raise_from_client_tools``.

        ``session_id`` is the Session whose call got no answer: this one or one of its subagents'.
        """

        if self._raised is None:
            self._raised = (error, session_id)
            self._raised_set.set()

    async def _take_raised(self) -> tuple[ToolCodeError, SessionId]:
        """Wait for an exception that an answer raised with tool_errors="raise", and take it with its Session."""

        await self._raised_set.wait()
        raised = self._raised
        if raised is None:  # pragma: no cover - only _keep_raised sets the event, and it sets the error first
            raise RuntimeError("client tool exception taken twice")
        self._raised = None
        self._raised_set.clear()
        return raised

    def _forget_old_answers(self) -> None:
        """Keep at most _KEPT_ANSWERS answers, dropping the oldest finished ones, those already sent first.

        A finished answer not sent yet goes last: a restarted loop may still see its call pending and
        must resend it rather than call the answer function again. It goes at all because its call may
        have settled without it, for example when the turn was interrupted. An answer still running is
        kept.
        """

        excess = len(self._answers) - _KEPT_ANSWERS
        if excess <= 0:
            return
        finished = [key for key, task in self._answers.items() if task.done()]
        # Sorting is stable, so each group stays oldest first.
        finished.sort(key=lambda key: key not in self._sent)
        for key in finished[:excess]:
            del self._answers[key]
            self._turns.pop(key, None)
            self._sent.discard(key)


@asynccontextmanager
async def raising_answer_failures(client: SessionClient | None) -> AsyncIterator[None]:
    """Stop the block as soon as the client's client tool answers fail, and raise their error.

    The answers run in the client's own task, which nothing else watches: a block waiting on a
    turn whose client tool call the client answers would otherwise wait until the host gives up
    on the call. Answers that ended before the block entered raise at once.
    """

    current = asyncio.current_task()
    if not isinstance(client, ClientToolSessionClient) or client._answering is None or current is None:
        yield
        return
    answering = client._answering
    failed = False
    # A done callback runs later: one that runs after the block must not cancel the caller.
    exited = False

    def stop(task: asyncio.Task[None]) -> None:
        nonlocal failed
        if not exited and not failed and not task.cancelled() and task.exception() is not None:
            failed = True
            current.cancel()

    answering.add_done_callback(stop)
    try:
        yield
    except asyncio.CancelledError:
        if not failed or current.uncancel() > 0:
            raise
        client._failure_raised = True
        error = _answers_failed(cast(BaseException, answering.exception()))
        # Not the cancellation: the error's own cause, the send error, stays.
        raise error from error.__cause__
    finally:
        exited = True
        answering.remove_done_callback(stop)
    if failed:
        # The block ended before the stop reached it: its result goes, as the answers failed.
        current.uncancel()
    if failed or (answering.done() and not answering.cancelled() and answering.exception() is not None):
        # Also when the answers failed but the stop has not run yet.
        client._failure_raised = True
        raise _answers_failed(cast(BaseException, answering.exception()))


async def finish_answers(client: SessionClient | None) -> bool:
    """Wait until the client tool answers running now on ``client`` are sent; return whether there were any."""

    return isinstance(client, ClientToolSessionClient) and await client.finish_answers()


def _answers_failed(error: BaseException) -> BaseException:
    """The error a wait raises when the client tool answers fail: the first error, unwrapped.

    The answers run in task groups, which wrap their errors in ``ExceptionGroup``s.
    """

    while isinstance(error, BaseExceptionGroup) and error.exceptions:
        error = error.exceptions[0]
    return error


def _is_program_tool(name: str) -> bool:
    """Whether a client tool call's ID, ``<namespace>.<name>``, is in a namespace the program's tools can use."""

    namespace, dot, _ = name.partition(".")
    return bool(dot) and not tool_authoring.is_reserved_namespace(namespace)


async def _run_answer(
    answer: tool_authoring.ClientToolAnswer[..., Any], callback: ClientToolCallback, session_id: SessionId
) -> object:
    output = await tool_authoring.call_client_tool_answer(answer, callback.input, _answer_context(callback, session_id))
    if isinstance(output, KeepCallbackOpen):
        return output
    try:
        return tool_authoring.dump_client_tool_result(answer, output)
    except Exception as error:
        # The answer returned a value its return type cannot serialize: the author's error.
        raise ToolFunctionError(error) from error


async def _run_handler(handler: ClientToolHandler, callback: ClientToolCallback) -> object:
    """Call ``on_client_tool`` as an answer is called: a synchronous one runs in a tool thread."""

    call = client_tool_call(callback)
    # No declared return type: `_invoke` serializes the result by what it is at runtime, models by
    # alias, so a list of models, a dataclass or a datetime reach the model as JSON, as an answer's do.
    try:
        return await tool_authoring.call_handler(functools.partial(handler, call))
    except asyncio.CancelledError as error:
        if call_is_cancelling():
            raise
        raise ToolFunctionError(error) from error
    except Exception as error:
        raise ToolFunctionError(error) from error


async def _invoke(
    callback: ClientToolCallback,
    run: Callable[[], Awaitable[object]],
    *,
    tool_errors: ToolErrors,
    on_raise: Callable[[ToolCodeError], None],
) -> CallbackResult | KeepCallbackOpen | None:
    try:
        output = await run()
    except ToolFunctionError as raised:
        return _failed(callback, raised.error, tool_errors=tool_errors, on_raise=on_raise)
    except Exception as error:  # noqa: BLE001 - surfaced to the model as a failed tool call
        # The model's arguments did not validate: the model reads why, so it can correct the call.
        return CallbackResult(
            callback_id=callback.id,
            error=ProtocolError(
                code="client_tool_failed",
                message=f"{type(error).__name__}: {error}",
            ),
        )
    if isinstance(output, KeepCallbackOpen):
        return output
    try:
        return _answered(callback, output)
    except Exception as error:  # noqa: BLE001 - the answer's value cannot be sent: follows tool_errors
        return _failed(callback, error, tool_errors=tool_errors, on_raise=on_raise)


def _failed(
    callback: ClientToolCallback,
    error: ToolCodeError,
    *,
    tool_errors: ToolErrors,
    on_raise: Callable[[ToolCodeError], None],
) -> CallbackResult | None:
    """The answer to a call whose answer or handler raised, or returned a value that cannot be sent."""

    if tool_errors == "raise" and not isinstance(error, ToolError):
        # No answer: the call stays open, so the Turn waits for it until the host's callback
        # timeout. The exception raises in the program, from the agent.run() driving the Turn.
        tool_error_logger.error(
            "Client tool %s raised %s; the call gets no answer",
            callback.name,
            type(error).__name__,
            exc_info=error,
        )
        on_raise(error)
        return None
    # What the model reads follows tool_errors.
    return _answered(callback, failed_tool_result(error, tool_errors=tool_errors, tool_id=callback.name))


async def raise_from_client_tools[T](client: SessionClient, waiting: Awaitable[T]) -> T:
    """Await ``waiting``, unless a client tool answer of ``client`` raises first with tool_errors="raise".

    Then that exception raises here instead, and ``waiting`` is cancelled: the caller stops waiting,
    and the call got no answer, so the Turn stays blocked on it until the host's callback timeout.

    ``waiting`` runs in the caller's task, so a cancellation or a timeout of the caller reaches it
    as it would without this wrapper, with the notes ``waiting`` adds.
    """

    current = asyncio.current_task()
    if (
        current is None
        or not isinstance(client, ClientToolSessionClient)
        or not client._client_tools
        or client._client_tools.tool_errors != "raise"
    ):
        return await waiting
    taken: list[tuple[ToolCodeError, SessionId]] = []

    async def take_raised() -> None:
        taken.append(await client._take_raised())
        # As asyncio.timeout does: stop the caller's wait, then tell this cancellation from others.
        current.cancel()

    watcher = asyncio.create_task(take_raised(), name=f"client-tool-raised:{client.session_id}")
    try:
        result = await waiting
    except asyncio.CancelledError:
        if not taken or current.uncancel() > 0:
            raise
    else:
        if not taken or current.uncancel() > 0:
            return result
        # `waiting` finished as the watcher took an exception: the exception still raises.
    finally:
        # Not awaited: a cancellation already asked of this task would raise from that wait.
        watcher.cancel()
    # Raised outside the `except`, so the exception keeps its own __cause__ and __context__.
    raise _with_raise_note(*taken[0])


def _with_raise_note(error: ToolCodeError, session_id: SessionId) -> ToolCodeError:
    error.add_note(
        f"A client tool raised with tool_errors='raise', so its call got no answer: the Turn of Session "
        f"{session_id} stays blocked on it, and the Session refuses a new Turn, until the host's "
        "callback timeout (1 hour by default)."
    )
    return error


def _answered(callback: ClientToolCallback, output: object) -> CallbackResult:
    """The answer to a call: a ToolResult, content blocks or an MCP result as they say, any other value as JSON."""

    if not is_rich_tool_result(output):
        return CallbackResult(callback_id=callback.id, output=assemble.to_json_value(output))
    # Normalised as a Python tool's result is, so both kinds of tool answer alike.
    result = tool_results.to_provided_tool_result(output, result_schema=None)
    return CallbackResult(
        callback_id=callback.id,
        output=result.structured_content,
        content=to_session_content(result.content),
        is_error=isinstance(result, ProvidedToolInvocationFailed),
        meta=result.metadata or None,
    )


def callback_turn_id(callback: SessionCallback) -> str:
    """The turn that opened ``callback``: a Session v1 host names it on every callback."""
    if callback.turn_id is None:
        raise sdk_runtime_error(f"Callback {callback.id} names no turn: a Session v1 host names one on every callback")
    return callback.turn_id


def given_answer(callback: ClientToolCallback, output: object, tool: object) -> CallbackResult:
    """The answer to a call with ``output``, the tool's result that the caller gives, as ``turn.answer`` sends it.

    ``tool`` is the agent's tool object for the call, if it has one. A stub with a return type
    checks ``output`` against it and serializes it as an answer's result is. Otherwise, a tool
    built with ``output_schema=`` included, ``output`` is sent as JSON, unchecked. A
    ``ToolResult`` or content blocks say themselves what the model sees.

    Raises ``SdkError`` when ``output`` is an approval answer, does not match the stub's return
    type, or is not JSON data.
    """

    if isinstance(output, AllowApproval | DenyApproval):
        raise SdkError(
            f"Callback {callback.id} is a call of the client tool {callback.name}: answer it with the "
            f"tool's result, not {type(output).__name__}"
        )
    adapter = tool._output_adapter if isinstance(tool, tool_authoring.ClientTool) else None
    try:
        if adapter is not None and not is_rich_tool_result(output):
            output = adapter.dump_python(adapter.validate_python(output), mode="json", by_alias=True)
        return _answered(callback, output)
    except (ValidationError, PydanticSerializationError) as error:
        raise SdkError(
            f"The answer to call {callback.id} of the client tool {callback.name} is not the tool's result: {error}"
        ) from None


def _answer_context(callback: ClientToolCallback, session_id: SessionId) -> contracts.ToolCallbackContext:
    """The context an answer gets: the Session and turn that called the tool, and the call's ID.

    The sandbox is unbound: the answer runs in the application, not where the agent runs.
    """

    return contracts.ToolCallbackContext(
        contracts.CallbackSession(id=session_id, turn_id=callback_turn_id(callback)),
        tool_call_id=callback.tool_call_id,
    )


__all__ = [
    "NO_CLIENT_TOOLS",
    "ClientToolAnswers",
    "ClientToolCall",
    "ClientToolHandler",
    "ClientToolRegistry",
    "ClientToolSessionClient",
    "OnClientTool",
    "build_client_tool_registry",
    "callback_turn_id",
    "check_answered_tools",
    "finish_answers",
    "given_answer",
    "left_open",
    "raising_answer_failures",
    "raise_from_client_tools",
    "watching_left_open",
]
