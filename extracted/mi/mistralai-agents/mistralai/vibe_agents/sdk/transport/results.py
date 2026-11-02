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
    ``arguments`` is the object the model passed; a deployment-backed Session may report any JSON value.
    """

    name: str
    arguments: JsonValue


def turn_text(
    termination: CompletedTermination | CancelledTermination | None, entries: Sequence[HistoryEntry]
) -> str | None:
    """A Turn's text: the text of its output, else its latest assistant text, else ``None``.

    ``entries`` are the Turn's own history entries, oldest first. A cancelled Turn's output is
    its latest assistant message.
    """
    if termination is not None and isinstance(termination.output, list):
        try:
            content = [ContentBlockAdapter.validate_python(block) for block in termination.output]
        except ValidationError:
            content = []
        text = "".join(block.text for block in content if isinstance(block, TextContentBlock))
        if text:
            return text
    for entry in reversed(entries):
        if isinstance(entry, MessageHistoryEntry) and entry.role == "assistant":
            text = "".join(block.text for block in entry.content if isinstance(block, TextContentBlock))
            if text:
                return text
    return None


def turn_tool_calls(entries: Sequence[HistoryEntry]) -> tuple[ToolCall, ...]:
    """A Turn's own tool calls, in the order the model made them."""
    return tuple(
        ToolCall(name=entry.name, arguments=entry.arguments)
        for entry in entries
        if isinstance(entry, ToolCallHistoryEntry)
    )


def parsed_output[ModelT: BaseModel](
    response_format: type[ModelT], stop_reason: str | None, text: str
) -> ModelT | None:
    """A Turn's text parsed into ``response_format``, or ``None`` when the Turn did not end ``"completed"``.

    A Turn that reached its iteration limit, or that a Hook skipped, has no final answer to parse.
    ``stop_reason`` ``None`` is ``"completed"``.

    Raises:
        ValidationError: The text does not validate against ``response_format``.
    """
    if (stop_reason or "completed") != "completed":
        return None
    return response_format.model_validate_json(text)


__all__ = ["ToolCall", "parsed_output", "turn_text", "turn_tool_calls"]
