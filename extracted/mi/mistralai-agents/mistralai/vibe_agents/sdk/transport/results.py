"""Read a Harness Turn's text, tool calls and parsed output from its history and termination."""

from collections.abc import Sequence
from dataclasses import dataclass

from pydantic import BaseModel, JsonValue, ValidationError

from mistralai.vibe.harness.app_server.session import (
    CancelledTermination,
    CompletedTermination,
    ContentBlockAdapter,
    HistoryEntry,
    MessageHistoryEntry,
    TextContentBlock,
    ToolCallHistoryEntry,
)


@dataclass(frozen=True, slots=True)
class ToolCall:
    """One tool call the model made during the Turn.

    ``name`` is the tool's full ID, such as ``client.get_weather``, not the name the model calls.
    A call to a tool that does not exist keeps the model's name.
    In the ``tool_calls`` of a ``post_llm_call`` or ``post_agent_turn`` Hook, the call is not
    resolved yet, so ``name`` is the name the model called, such as ``get_weather``.
    A call that did not run is listed too: a permission rule denied it, a user rejected it at
    approval, its approval timed out, a Hook skipped it or failed on it, Harness Core refused it
    (``invalid_tool_call``: arguments that are not valid JSON or that the schema rejects, an unknown
    tool, ``wait`` beside other calls), or, inside ``run_typescript``, its arguments did not match the
    tool's input schema or the program's time budget stopped it before it started.
    ``arguments`` is the object the model passed; arguments that are not valid JSON are the raw string,
    and a deployment-backed Session may report any JSON value.
    """

    name: str
    arguments: JsonValue


def turn_text(
    termination: CompletedTermination | CancelledTermination | None, entries: Sequence[HistoryEntry]
) -> str | None:
    """A Turn's text: the text of its output, else its latest assistant text, else ``None``.

    ``entries`` are the Turn's own history entries, oldest first. A cancelled Turn's output is
    its latest assistant message. A Turn that a Hook skipped, or whose reply a Hook rejected, never
    reads an assistant message, which is an earlier model call's text or the rejected reply: its
    text is the Hook's reason from its output, or ``None`` when that reason is empty. A Turn whose
    last reply was cut off at the output limit has that reply as its output; when the cut came
    before any text, its text is ``None``, never an earlier model call's text.
    """
    if termination is not None and isinstance(termination.output, list):
        try:
            content = [ContentBlockAdapter.validate_python(block) for block in termination.output]
        except ValidationError:
            content = []
        text = "".join(block.text for block in content if isinstance(block, TextContentBlock))
        if text:
            return text
    if isinstance(termination, CompletedTermination) and termination.stop_reason in (
        "skipped",
        "rejected",
        "output_limit",
    ):
        return None
    for entry in reversed(entries):
        if isinstance(entry, MessageHistoryEntry) and entry.role == "assistant":
            text = "".join(block.text for block in entry.content if isinstance(block, TextContentBlock))
            if text:
                return text
    return None


def turn_tool_calls(entries: Sequence[HistoryEntry]) -> tuple[ToolCall, ...]:
    """A Turn's own tool calls, in history order."""
    return tuple(
        ToolCall(name=entry.name, arguments=entry.arguments)
        for entry in entries
        if isinstance(entry, ToolCallHistoryEntry)
    )


def parsed_output[ModelT: BaseModel](output_type: type[ModelT], stop_reason: str | None, text: str) -> ModelT | None:
    """A Turn's text parsed into ``output_type``, or ``None`` when the Turn did not end ``"completed"``.

    A Turn that reached its iteration limit, that a Hook skipped, whose reply a Hook rejected, or
    whose last reply stopped at the output token limit, has no final answer to parse.
    ``stop_reason`` ``None`` is ``"completed"``.

    Raises:
        ValidationError: The text does not validate against ``output_type``.
    """
    if (stop_reason or "completed") != "completed":
        return None
    return output_type.model_validate_json(text)


__all__ = ["ToolCall", "parsed_output", "turn_text", "turn_tool_calls"]
