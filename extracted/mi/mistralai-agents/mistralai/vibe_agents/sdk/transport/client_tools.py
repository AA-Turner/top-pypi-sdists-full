"""Answer Harness client-tool callbacks from the process that opened the Session."""

import asyncio
import functools
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable, Mapping
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, cast

import structlog
from pydantic import JsonValue

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
from mistralai.vibe.harness.app_server.session.file_upload import FileUploader
from mistralai.vibe.harness.app_server.session.procedures.session import CallbackResultResponse
from mistralai.vibe.harness.runtime.capabilities import ProvidedToolInvocationFailed
from mistralai.vibe.harness.runtime.content import to_session_content
from mistralai.vibe_agents.sdk.assembly import assemble, tool_results
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring import tool as tool_authoring
from mistralai.vibe_agents.sdk.authoring.errors import ClientToolAnswerError, SdkError
from mistralai.vibe_agents.sdk.authoring.tool_errors import (
    DEFAULT_TOOL_ERRORS,
    ToolError,
    ToolErrors,
    ToolFunctionError,
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


@dataclass(frozen=True, slots=True)
class ClientToolCall:
    """One call of a client tool, as ``on_client_tool`` receives it and ``OpenClientToolCall.call`` holds it.

    ``name`` is the tool's ID, its namespace then the name it was declared with, such as
    ``client.get_weather`` (``client`` is the default namespace) or ``ui.get_location``: the same
    as ``agents.ToolCall.name`` in ``Completed.tool_calls``.
    ``arguments`` is the object the model passed, not validated: the handler checks it.

    A tool whose answer is in ``client_tools=`` never reaches ``on_client_tool``: its answer wins.
    """

    name: str
    arguments: JsonValue


def client_tool_call(callback: ClientToolCallback) -> ClientToolCall:
    """The call that ``callback`` asks the program to answer."""

    return ClientToolCall(name=callback.name, arguments=callback.input)


type ClientToolHandler = Callable[[ClientToolCall], object | Awaitable[object]]
"""Answers any client tool call: returns the result the model reads, synchronously or not."""


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

    def __bool__(self) -> bool:
        return bool(self.answers) or self.on_client_tool is not None


NO_CLIENT_TOOLS = ClientToolRegistry()


def build_client_tool_registry(
    answers: Iterable[tool_authoring.ClientToolAnswer[..., Any]],
    on_client_tool: ClientToolHandler | None = None,
    *,
    tool_errors: ToolErrors = DEFAULT_TOOL_ERRORS,
) -> ClientToolRegistry:
    """Index the client tool answers by the name the model's call arrives under."""

    registry: dict[str, tool_authoring.ClientToolAnswer[..., Any]] = {}
    for answer in answers:
        if not isinstance(answer, tool_authoring.ClientToolAnswer):
            raise SdkError(f"client_tools takes the functions bound with @<tool>.answer, got {type(answer).__name__}")
        # The call arrives under the tool's ID, `<namespace>.<name>`.
        name = f"{answer.tool.namespace}.{answer.tool.name}"
        if name in registry:
            raise SdkError(f"client_tools answers {name!r} twice")
        registry[name] = answer
    if on_client_tool is not None and not callable(on_client_tool):
        raise SdkError(f"on_client_tool takes a function, got {type(on_client_tool).__name__}")
    return ClientToolRegistry(
        answers=MappingProxyType(registry), on_client_tool=on_client_tool, tool_errors=tool_errors
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
        uploader: FileUploader | None = None,
    ) -> None:
        super().__init__(transport, uploader=uploader)
        self._client_tools = client_tools
        self._closing = asyncio.Event()
        self._answering: asyncio.Task[None] | None = None
        # Each call's answer, computed once, keyed by the Session that opened the call and the
        # call's id. A restarted loop resends it instead of calling again, even after a send that
        # succeeded but whose settlement the loop has not seen yet. None: no answer, the call stays
        # open (an exception with tool_errors="raise").
        self._answers: dict[tuple[SessionId, str], asyncio.Task[CallbackResult | None]] = {}
        # The answers in `_answers` that the transport accepted, which `_forget_old_answers` drops first.
        self._sent: set[tuple[SessionId, str]] = set()
        # The turn of each call in `_answers`, to name it when its answer cannot be sent.
        self._turns: dict[tuple[SessionId, str], str | None] = {}
        # The first answer that could not be sent: the answering stops, and a run raises it.
        self._send_failure: ClientToolAnswerError | None = None
        # Set once a caller got the error of the failed answers, so close does not raise it again.
        self._failure_raised = False
        # The answers started and not sent yet, each done once its call is answered: a run waits for them.
        self._unsent: dict[tuple[SessionId, str], asyncio.Future[None]] = {}
        # The answers running their code, not sent yet: a run's timeout does not count them.
        self._in_code: set[asyncio.Task[Any]] = set()
        self._answering_watchers: list[Callable[[bool], None]] = []
        # Set when a run is leaving: no new answer starts, but those started are still sent.
        self._draining = False
        # The first exception an answer raised with tool_errors="raise" that no caller took yet, and
        # the Session whose call it left open.
        self._raised: tuple[Exception, SessionId] | None = None
        self._raised_set = asyncio.Event()

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
            failure = ClientToolAnswerError(callback_id=key[1], session_id=key[0], turn_id=self._turns.get(key))
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
                async with self.provide_callbacks(kinds={"client_tool"}, handler=self._answer):
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
            # opens the same callback kind for its provided tools, such as the connector sign-in
            # `connectors.ask_enable_connector`.
            run = functools.partial(_run_handler, handler, callback)
        else:
            # A provided tool, another client tool, or a caller answering this one itself.
            return None
        computed = self._answers.get(key)
        if computed is None:
            if self._draining:
                # A run that is leaving starts no new answer.
                return None
            computed = asyncio.create_task(
                self._compute(callback, run, key[0]), name=f"client-tool:{key[0]}:{callback.id}"
            )
            self._answers[key] = computed
            self._turns[key] = callback.turn_id
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
        try:
            result = await _invoke(
                callback,
                run,
                tool_errors=self._client_tools.tool_errors,
                on_raise=functools.partial(self._keep_raised, session_id=session_id),
            )
            if result is None:
                # It raised with tool_errors="raise": no answer is sent, so a run does not wait for one.
                self._mark_sent((session_id, callback.id))
            return result
        finally:
            if task is not None:
                self._running_code(task, False)

    def _mark_sent(self, key: tuple[SessionId, str]) -> None:
        waiter = self._unsent.pop(key, None)
        if waiter is not None and not waiter.done():
            waiter.set_result(None)

    def _keep_raised(self, error: Exception, *, session_id: SessionId) -> None:
        """Keep the first exception an answer raised with tool_errors="raise", for ``raise_from_client_tools``.

        ``session_id`` is the Session whose call got no answer: this one or one of its subagents'.
        """

        if self._raised is None:
            self._raised = (error, session_id)
            self._raised_set.set()

    async def _take_raised(self) -> tuple[Exception, SessionId]:
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
    except Exception as error:
        raise ToolFunctionError(error) from error


async def _invoke(
    callback: ClientToolCallback,
    run: Callable[[], Awaitable[object]],
    *,
    tool_errors: ToolErrors,
    on_raise: Callable[[Exception], None],
) -> CallbackResult | None:
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
    try:
        return _answered(callback, output)
    except Exception as error:  # noqa: BLE001 - the answer's value cannot be sent: follows tool_errors
        return _failed(callback, error, tool_errors=tool_errors, on_raise=on_raise)


def _failed(
    callback: ClientToolCallback,
    error: Exception,
    *,
    tool_errors: ToolErrors,
    on_raise: Callable[[Exception], None],
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
    taken: list[tuple[Exception, SessionId]] = []

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


def _with_raise_note(error: Exception, session_id: SessionId) -> Exception:
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


def _answer_context(callback: ClientToolCallback, session_id: SessionId) -> contracts.ToolCallbackContext:
    """The context an answer gets: the Session that called the tool, and the call's ID.

    A callback opened without a turn or a tool call behind it gives ``""`` for that ID. The sandbox
    is unbound: the answer runs in the application, not where the agent runs.
    """

    return contracts.ToolCallbackContext(
        contracts.CallbackSession(id=session_id, turn_id=callback.turn_id or ""),
        tool_call_id=callback.tool_call_id or "",
    )


__all__ = [
    "NO_CLIENT_TOOLS",
    "ClientToolCall",
    "ClientToolHandler",
    "ClientToolRegistry",
    "ClientToolSessionClient",
    "build_client_tool_registry",
    "finish_answers",
    "raising_answer_failures",
    "raise_from_client_tools",
]
