"""Talk to an agent turn by turn, for `agents chat`.

`open_session` opens a Session on the project's agent, in this process, or on a served or deployed agent
by name. `run_turn` drives one turn and reports what happens to a `ChatOutput`: the reply as it is
written, each tool call and its result, and approvals, which it answers with what the output decides.
The terminal is the CLI's business; this module only reads the Session's events.
"""

from __future__ import annotations

import contextlib
import signal
import threading
from collections.abc import Iterator
from enum import StrEnum
from pathlib import Path
from typing import Protocol, TypeGuard

import httpx
from pydantic import JsonValue, ValidationError

from mistralai.vibe.harness.app_server import session as harness_session

from .runtime_logs import terminal_safe


class ChatError(Exception):
    pass


class ApprovalAnswer(StrEnum):
    ONCE = "once"
    SESSION = "session"
    DENY = "deny"


class ChatOutput(Protocol):
    def reply(self, text: str) -> None:
        """More of the agent's reply. Called as it is written, then once more for the rest when it is final."""

    def reply_done(self) -> None:
        """The reply entry is final."""

    def tool_call(self, name: str, arguments: JsonValue) -> None: ...

    def tool_result(self, name: str, error: str | None) -> None: ...

    def ask_approval(self, callback: harness_session.ApprovalCallback) -> ApprovalAnswer: ...

    def notice(self, message: str) -> None:
        """Something the user should know that is not part of the reply: a refused callback, an error entry."""

    def turn_failed(self, message: str) -> None: ...

    def turn_cancelled(self, reason: str | None) -> None: ...


async def open_session(*, agent_name: str | None, path: Path) -> harness_session.SessionClient:
    """Open a Session on the named served or deployed agent, or, without a name, on the project at ``path``.

    The project's agent runs in this process: no worker, nothing registered.
    """
    from mistralai.vibe_agents.sdk.authoring import errors as sdk_errors  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.authoring.agent import Agent  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.transport.remote import RemoteSessionStartFailedError  # noqa: PLC0415

    if agent_name is not None:
        await _require_reachable(agent_name)
        try:
            return await Agent.load_from(agent_name=agent_name)._create_session()
        except sdk_errors.RemoteAgentDeploymentNotFoundError as exc:
            raise ChatError(f"Agent {agent_name} no longer exists; it may have been shut down.") from exc
        except sdk_errors.SdkError as exc:
            raise ChatError(f"Cannot start a session with {agent_name}: {exc}") from exc
        except sdk_errors.SessionStartupTimeoutError as exc:
            raise ChatError(
                f"Agent {agent_name} did not report ready in time; the session "
                f"{exc.session_id} was created and may still start. Attach to it with "
                f"`Agent.load_from(agent_name={agent_name!r}).session({exc.session_id!r})` "
                "instead of starting another chat."
            ) from exc
        except RemoteSessionStartFailedError as exc:
            # The session ended before it was ready, such as a sandbox that could not be created: the agent's
            # own failure, so it is reported as one line rather than a traceback.
            raise ChatError(f"The session with {agent_name} failed to start: {terminal_safe(str(exc))}") from exc
        except httpx.HTTPError as exc:
            raise ChatError(f"Cannot start a session with {agent_name}: {exc}") from exc

    from . import loader, preflight  # noqa: PLC0415

    loaded = loader.load_app(path)
    # The same checks `agents serve` makes: without them, a missing Koyeb token is a traceback on the first turn.
    issues = [*preflight.sandbox_dependency_issues(loaded), *preflight.sandbox_config_issues(loaded.harness)]
    if issues:
        raise ChatError("\n".join(["This agent cannot run here:", *(f"  - {issue}" for issue in issues)]))
    try:
        return await loaded.agent._create_session()
    except sdk_errors.SdkError as exc:
        raise ChatError(f"Cannot start a session with {loaded.name}: {exc}") from exc


async def _require_reachable(agent_name: str) -> None:
    """Fail now on a name that matches nothing, or a served agent whose worker is stopped.

    Otherwise the first would surface as a bare HTTP error, and the second would wait out the Session's
    whole startup budget. A deployed agent is not refused when it reads inactive: its platform starts it.
    """
    from mistralai.vibe_agents.agents_client import AgentsClient  # noqa: PLC0415

    from . import config  # noqa: PLC0415

    try:
        settings = config.load_control_plane_settings()
    except config.SettingsError as exc:
        raise ChatError(str(exc)) from exc
    async with AgentsClient(base_url=settings.deploy_control_plane_url, api_key=settings.api_key) as client:
        try:
            agent = await client.get_agent_by_name(agent_name)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == httpx.codes.NOT_FOUND:
                raise ChatError(
                    f"No agent named {agent_name} in this workspace. See your agents with `agents list`."
                ) from exc
            raise ChatError(f"Failed to look up agent {agent_name} (HTTP {exc.response.status_code})") from exc
        # A 200 with a body that is not JSON, or not an agent, raises a ValueError (JSONDecodeError,
        # ValidationError) rather than an HTTP error.
        except (httpx.HTTPError, ValueError) as exc:
            raise ChatError(f"Failed to look up agent {agent_name}: {exc}") from exc
    if not agent.managed and not agent.is_active:
        raise ChatError(f"Agent {agent_name} is served, but no worker is running it. Start it with `agents serve`.")


async def run_turn(session: harness_session.SessionClient, text: str, output: ChatOutput) -> bool:
    """Send ``text`` as one turn, report it to ``output`` until the turn ends, and return whether it completed.

    A failed or cancelled turn returns False after it is reported, so a one-shot caller can exit nonzero.
    Cancelling the task interrupts the turn on the agent's side, which leaves the Session usable.
    """
    completed = False
    stream = _ReplyStream(output)
    message: list[harness_session.ContentBlock] = [harness_session.TextContentBlock(text=text)]
    # Closing the event stream on the way out interrupts the turn on the agent's side, so an exception raised
    # here, such as Ctrl+C at an approval prompt, ends the turn instead of leaving it running.
    try:
        async with contextlib.aclosing(session.run_turn(message)) as events:
            async for event in events:
                payload = event.payload
                if isinstance(payload, harness_session.HistoryEntryAddedEvent):
                    stream.added(payload.entry)
                elif isinstance(payload, harness_session.HistoryEntryPatchedEvent):
                    stream.patched(payload)
                elif isinstance(payload, harness_session.HistoryEntryCompletedEvent):
                    stream.completed(payload.entry)
                elif isinstance(payload, harness_session.CallbackOpenedEvent):
                    # A prompt or notice must not land on the end of a reply that is still being written.
                    stream.close()
                    await _answer(session, payload.callback, output)
                elif isinstance(payload, harness_session.CallbackResolvedEvent):
                    stream.close()
                    _report_unanswered(payload, output)
                elif isinstance(payload, harness_session.TurnTerminatedEvent):
                    stream.close()
                    _report_termination(payload.turn.termination, output)
                    completed = isinstance(payload.turn.termination, harness_session.CompletedTermination)
    finally:
        # An error mid-reply, such as a lost stream, is printed by the caller: it must start on a line of its own.
        stream.close()
    return completed


class _ReplyStream:
    """Print each assistant message once, as it grows, whichever way the Session reports the growth.

    An in-process Session appends text with `append` patches; a served or deployed one replaces the whole
    entry. Tracking what was printed per entry, and printing only the new suffix, covers both.
    """

    def __init__(self, output: ChatOutput) -> None:
        self._output = output
        self._printed: dict[str, str] = {}
        self._open: str | None = None
        self._tool_names: dict[str, str] = {}
        self._finished: set[str] = set()

    def added(self, entry: harness_session.HistoryEntry) -> None:
        # An entry the runtime records whole, such as a tool call, is added already complete and never
        # gets a completed event of its own.
        if entry.generation_status == "complete":
            self.completed(entry)
        elif _is_assistant_message(entry):
            self._show(entry.id, _message_text(entry))

    def patched(self, event: harness_session.HistoryEntryPatchedEvent) -> None:
        if event.entry_id not in self._printed:
            return
        current = self._printed[event.entry_id]
        for patch in event.patches:
            if isinstance(patch, harness_session.JsonPatchAppendOperation) and patch.path == "/content/0/text":
                current += patch.value
            elif isinstance(patch, harness_session.JsonPatchReplaceOperation):
                if patch.path == "/content/0/text" and isinstance(patch.value, str):
                    current = patch.value
                elif patch.path == "":
                    current = _text_of_entry_value(patch.value, default=current)
        self._show(event.entry_id, current)

    def completed(self, entry: harness_session.HistoryEntry) -> None:
        if entry.id in self._finished:
            return
        self._finished.add(entry.id)
        if _is_assistant_message(entry):
            self._show(entry.id, _message_text(entry))
            self._finish(entry.id)
        elif isinstance(entry, harness_session.ToolCallHistoryEntry):
            self._end_reply()
            name = _display_name(entry.name)
            self._tool_names[entry.tool_call_id] = name
            self._output.tool_call(name, entry.arguments)
        elif isinstance(entry, harness_session.ToolResultHistoryEntry):
            self._end_reply()
            name = self._tool_names.get(entry.tool_call_id) or _display_name(entry.name or "tool")
            self._output.tool_result(name, terminal_safe(entry.error.message) if entry.error else None)
        elif isinstance(entry, harness_session.ErrorHistoryEntry):
            self._end_reply()
            self._output.notice(f"Error: {terminal_safe(entry.error.message)}")
        elif isinstance(entry, harness_session.NoticeHistoryEntry) and entry.level != "info":
            self._end_reply()
            self._output.notice(f"{entry.level.capitalize()}: {terminal_safe(entry.message)}")

    def close(self) -> None:
        self._end_reply()

    def _show(self, entry_id: str, text: str) -> None:
        if self._open is not None and self._open != entry_id:
            self._end_reply()
        printed = self._printed.get(entry_id, "")
        # Registered even while empty: `patched` only follows entries it has seen added.
        self._printed[entry_id] = printed
        if text == printed:
            return
        if not text.startswith(printed):
            # The entry was rewritten. What is on screen cannot be unprinted, so end that line and print the
            # corrected text in full; later growth then continues from the correction.
            if self._open == entry_id:
                self._end_reply()
            printed = ""
        self._open = entry_id
        self._output.reply(terminal_safe(text[len(printed) :], keep_newlines=True))
        self._printed[entry_id] = text

    def _finish(self, entry_id: str) -> None:
        if self._open == entry_id:
            self._end_reply()

    def _end_reply(self) -> None:
        if self._open is not None:
            self._open = None
            self._output.reply_done()


def _is_assistant_message(entry: harness_session.HistoryEntry) -> TypeGuard[harness_session.MessageHistoryEntry]:
    return isinstance(entry, harness_session.MessageHistoryEntry) and entry.role == "assistant"


def _message_text(entry: harness_session.MessageHistoryEntry) -> str:
    return "".join(_block_text(block) for block in entry.content)


def _block_text(block: harness_session.ContentBlock) -> str:
    """What the chat prints of one block: its text, ``[<type>]`` for a block type this SDK does not know."""
    if isinstance(block, harness_session.TextContentBlock):
        return block.text
    if isinstance(block, harness_session.UnknownContentBlock):
        return f"[{block.original_type}]"
    return ""


def _text_of_entry_value(value: JsonValue, *, default: str) -> str:
    if not isinstance(value, dict):
        return default
    content = value.get("content")
    if not isinstance(content, list):
        return default
    texts: list[str] = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            text = item.get("text")
            if isinstance(text, str):
                texts.append(text)
            continue
        try:
            block = harness_session.ContentBlockAdapter.validate_python(item)
        except ValidationError:
            continue
        if isinstance(block, harness_session.UnknownContentBlock):
            texts.append(_block_text(block))
    return "".join(texts)


# The namespace the harness gives tools an agent defines itself; approvals name them without it.
_DEFAULT_TOOL_NAMESPACE = "client."


def _display_name(name: str) -> str:
    """``name`` as the approval prompt shows it: without the default namespace, with any other one."""
    return name.removeprefix(_DEFAULT_TOOL_NAMESPACE)


@contextlib.contextmanager
def _interruptible() -> Iterator[None]:
    """Let Ctrl+C raise KeyboardInterrupt inside a blocking prompt.

    Under ``asyncio.run`` the first Ctrl+C only cancels the main task, which a prompt blocking the loop
    never sees; the second then cancels the deny sent after it. The default handler raises at once.
    """
    if threading.current_thread() is not threading.main_thread():
        yield
        return
    previous = signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        yield
    finally:
        signal.signal(signal.SIGINT, previous)


async def _answer(
    session: harness_session.SessionClient, callback: harness_session.SessionCallback, output: ChatOutput
) -> None:
    if isinstance(callback, harness_session.ApprovalCallback):
        try:
            with _interruptible():
                answer = output.ask_approval(callback)
        except BaseException:
            # The user gave up on the question (Ctrl+C at the prompt). Deny the call so the callback does
            # not stay open until its deadline, then let the interruption end the turn.
            await session.answer_callback(
                harness_session.CallbackResult(callback_id=callback.id, output={"decision": "deny"})
            )
            raise
        decision: JsonValue = (
            {"decision": "deny"} if answer is ApprovalAnswer.DENY else {"decision": "allow", "scope": answer.value}
        )
        await session.answer_callback(harness_session.CallbackResult(callback_id=callback.id, output=decision))
        return
    # Client tools, user input and the like need the application that defines them; a terminal cannot
    # stand in for it. Refusing at once lets the turn go on instead of waiting for the callback's deadline.
    output.notice(f"The agent asked for a {callback.kind} callback, which `agents chat` cannot answer; refused.")
    await session.answer_callback(
        harness_session.CallbackResult(
            callback_id=callback.id,
            error=harness_session.ProtocolError(
                message=f"agents chat cannot answer {callback.kind} callbacks", code="unsupported_callback"
            ),
        )
    )


def _report_unanswered(event: harness_session.CallbackResolvedEvent, output: ChatOutput) -> None:
    outcome = event.outcome
    if isinstance(outcome, harness_session.FailedCallbackOutcome) and outcome.error.code == "callback_timed_out":
        output.notice("A callback timed out before it was answered.")


def _report_termination(termination: harness_session.Termination | None, output: ChatOutput) -> None:
    if isinstance(termination, harness_session.FailedTermination):
        output.turn_failed(terminal_safe(termination.error.message))
    elif isinstance(termination, harness_session.CancelledTermination):
        output.turn_cancelled(termination.reason)
    elif isinstance(termination, harness_session.UnknownTermination):
        output.notice(f"The turn ended: {terminal_safe(termination.original_outcome)}.")
