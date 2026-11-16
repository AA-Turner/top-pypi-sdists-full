"""``agilicus assistant``: a chat with the Agilicus assistant, in the terminal.

A thin client, deliberately: it holds the transcript, streams a turn as it
arrives and shows every tool the model called. It is the harness the chat
surface is tested with, and it is how an engineer asks a tenant a question
without clicking through the portal.
"""

from __future__ import annotations

import json
import os
import sys

import click
import httpx

from .. import context
from . import assistant

RESULT_PREVIEW = 160

PROMPT = "you> "
ANSWER = "assistant> "


def _colour(text: str, code: str) -> str:
    """Colour when a person is looking, plain text when a script is."""
    if not sys.stdout.isatty() or "NO_COLOR" in os.environ:
        return text
    return f"{code}{text}\033[0m"


def _dim(text: str) -> str:
    return _colour(text, "\033[2m")


def _bold(text: str) -> str:
    return _colour(text, "\033[1m")


def _red(text: str) -> str:
    return _colour(text, "\033[31m")


def _yellow(text: str) -> str:
    return _colour(text, "\033[33m")


def _cyan(text: str) -> str:
    return _colour(text, "\033[36m")


def _stdin_is_tty() -> bool:
    """Whether a person is at the keyboard, rather than a pipe or a test."""
    try:
        return sys.stdin.isatty()
    except (AttributeError, ValueError):
        return False


HELP = """\
/mode explain|do   choose whether this conversation may act (do needs approval)
/clear             forget the transcript and start again
/help              this list
/quit              leave
"""


class _Renderer:
    """Draws one turn as it arrives, and remembers whether it finished.

    A method per event name keeps the loop readable and keeps each rule in one
    place: unknown names are ignored, because a client is required to ignore an
    event it does not know rather than fail the turn.
    """

    def __init__(self, conversation, *, show_tools, as_json):
        self.conversation = conversation
        self.show_tools = show_tools
        self.as_json = as_json
        self.answer: list[str] = []
        self.started = False
        self.finished = False

    def feed(self, events) -> str | None:
        for name, data in events:
            if self.as_json:
                print(json.dumps({"event": name, **data}, default=str), flush=True)
            handler = getattr(self, f"_on_{name}", None)
            if handler is not None:
                handler(data)
        self.close()
        # A turn that never reached `done` has no answer, only a fragment of
        # one: returning it would let a severed stream be remembered as a turn.
        if not self.finished:
            return None
        return "".join(self.answer)

    def close(self) -> None:
        self._break_line()
        if not self.finished:
            print(
                _red("  ! the stream ended without a `done` event; the turn failed"),
                file=sys.stderr,
            )

    def _break_line(self) -> None:
        if self.started:
            sys.stdout.write("\n")
            self.started = False

    def _on_token(self, data) -> None:
        # The answer is accumulated whether or not it is drawn: `--json`
        # suppresses the terminal output, not the transcript.
        text = data.get("text", "")
        self.answer.append(text)
        if self.as_json:
            return
        if not self.started:
            sys.stdout.write(_bold(ANSWER))
            self.started = True
        sys.stdout.write(text)
        sys.stdout.flush()

    def _on_tool_call(self, data) -> None:
        if self.as_json or not self.show_tools:
            return
        self._break_line()
        arguments = json.dumps(data.get("arguments"))[:RESULT_PREVIEW]
        print(_dim(f"  · {data.get('tool')} {arguments}"))

    def _on_tool_result(self, data) -> None:
        if self.as_json or not self.show_tools:
            return
        content = str(data.get("content", ""))[:RESULT_PREVIEW].replace("\n", " ")
        print(_dim(f"  · result {data.get('tool')}: {content}"))

    def _on_usage(self, data) -> None:
        if self.as_json or not self.show_tools:
            return
        self._break_line()
        usage = data.get("usage") or {}
        print(
            _dim(
                f"  · {usage.get('requests')} requests, "
                f"{usage.get('input_tokens')} in / {usage.get('output_tokens')} out"
            )
        )

    def _on_approval_required(self, data) -> None:
        self.conversation.pending_approval = data
        self._break_line()
        print(
            _yellow(
                "  · this needs approval before it runs: "
                + json.dumps(data.get("approval") or data)[:400]
            )
        )

    def _on_error(self, data) -> None:
        self._break_line()
        print(_red(f"  ! {data.get('message') or data}"), file=sys.stderr)

    def _on_done(self, data) -> None:
        self.finished = True
        self._break_line()


def _render(
    events, conversation: assistant.Conversation, *, show_tools: bool, as_json: bool
) -> str | None:
    """Print one turn as it arrives, and return its answer, or None if it failed."""
    return _Renderer(conversation, show_tools=show_tools, as_json=as_json).feed(events)


def _turn(ctx, conversation, message, client, url, token, timeout, show_tools, as_json):
    payload = conversation.payload(message)
    try:
        events = assistant.stream_events(client, url, token, payload, timeout)
        answer = _render(events, conversation, show_tools=show_tools, as_json=as_json)
    except assistant.AssistantError as failure:
        print(
            _red(
                f"  ! the assistant refused the request ({failure.status}): "
                f"{failure.detail}"
            ),
            file=sys.stderr,
        )
        return None
    except KeyboardInterrupt:
        print(_dim("  · interrupted"), file=sys.stderr)
        return None
    except httpx.HTTPError as failure:
        print(_red(f"  ! could not reach {url}: {failure}"), file=sys.stderr)
        return None
    if answer is None:
        # Half an answer is not an answer: keep neither side of the exchange,
        # so the next turn does not carry a question with no reply after it.
        return None
    conversation.remember("user", message)
    if answer:
        conversation.remember("assistant", answer)
    return answer


@click.command(
    name="assistant",
    help=(
        "Chat with the Agilicus assistant over /v1/assistant/chat. "
        "`explain` answers questions and cannot change anything; `do` may act, "
        "and a mutation needs approval."
    ),
)
@click.option(
    "--mode",
    type=click.Choice(assistant.MODES, case_sensitive=False),
    default="explain",
    show_default=True,
    help="explain answers, do acts.",
)
@click.option(
    "--message",
    "-m",
    default=None,
    help="Ask one question and exit, instead of starting a conversation.",
)
@click.option(
    "--timeout",
    type=float,
    default=assistant.DEFAULT_TIMEOUT,
    show_default=True,
    help="Seconds to wait for one turn.",
)
@click.option(
    "--quiet",
    is_flag=True,
    default=False,
    help="Show the answer only, without the tool trace.",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    default=False,
    help="Print the raw events, one JSON object per line.",
)
@click.pass_context
def assistant_command(ctx, mode, message, timeout, quiet, as_json):
    api = context.get_api(ctx)
    url = assistant.chat_url(api)
    token = context.get_token(ctx)
    client = assistant.make_client(context.get_cacert(ctx))
    conversation = assistant.Conversation(mode=mode)
    show_tools = not quiet

    try:
        if message is not None or not _stdin_is_tty():
            if message is None:
                message = sys.stdin.read().strip()
            if not message:
                raise click.UsageError("nothing to ask")
            answer = _turn(
                ctx,
                conversation,
                message,
                client,
                url,
                token,
                timeout,
                show_tools,
                as_json,
            )
            if answer is None:
                # This was asked for by a script, so a refusal or a broken
                # stream has to be a non-zero exit: `if agilicus assistant -m
                # ...` must not read a failure as an answer.
                ctx.exit(1)
            return

        print(_dim(f"assistant ({mode}) · {url} · /help for commands, /quit to leave"))
        while True:
            try:
                line = input(_cyan(PROMPT))
            except (EOFError, KeyboardInterrupt):
                print()
                return
            line = line.strip()
            if not line:
                continue
            if line in ("/quit", "/exit"):
                return
            if line == "/help":
                print(HELP, end="")
                continue
            if line == "/clear":
                conversation.clear()
                print(_dim("  · transcript cleared"))
                continue
            if line.startswith("/mode"):
                _, _, wanted = line.partition(" ")
                wanted = wanted.strip().lower()
                if wanted not in assistant.MODES:
                    print(_red(f"  ! mode must be one of {', '.join(assistant.MODES)}"))
                    continue
                conversation.mode = wanted
                print(_dim(f"  · mode is now {wanted}"))
                continue
            if line.startswith("/"):
                print(_red(f"  ! unknown command {line.split()[0]}; /help"))
                continue
            _turn(
                ctx,
                conversation,
                line,
                client,
                url,
                token,
                timeout,
                show_tools,
                as_json,
            )
    finally:
        client.close()


def add_commands(cli):
    cli.add_command(assistant_command)
