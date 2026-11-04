"""History entries: the items of a session's history, as immutable values.

The host keeps a session's history as a list of entries: messages, tool calls, tool results and
others. This module has the SDK's own types for a tool call entry, a tool result entry and an entry
of a type the SDK does not know, and the functions that build them from the host's entries, for any
read that returns history.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import JsonValue, ValidationError

from mistralai.vibe.harness.app_server.session import (
    ContentBlock,
    ContentBlockAdapter,
    TextContentBlock,
    ToolCallHistoryEntry,
    ToolResultHistoryEntry,
    UnknownHistoryEntry,
)

__all__ = [
    "ToolCallEntry",
    "ToolResultEntry",
    "UnknownEntry",
    "tool_call_entry",
    "tool_result_entry",
    "unknown_entry",
]


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class ToolCallEntry:
    """A tool call in a session's history: the model called a tool.

    ``id`` is the entry's id in the history. ``turn_id`` is the turn the call was made in, or
    ``None`` when the entry is not part of a turn, for example in a history given at the session's
    start. ``tool_call_id`` names the call: the tool's result carries the same id.
    ``name`` is the tool's full ID, such as ``client.get_weather``, as in :class:`ToolCall`.
    ``arguments`` is the object the model passed, as the host reported it: do not change it, copy it
    first.

    This is a history entry. :class:`ToolCall` stays the item of ``Completed.tool_calls``.
    """

    __match_args__ = ("name", "arguments")

    id: str
    turn_id: str | None
    tool_call_id: str
    name: str
    arguments: JsonValue


def tool_call_entry(entry: ToolCallHistoryEntry) -> ToolCallEntry:
    """The SDK's tool call entry for the host's ``tool_call`` history entry."""
    return ToolCallEntry(
        id=entry.id,
        turn_id=entry.turn_id,
        tool_call_id=entry.tool_call_id,
        name=entry.name,
        arguments=entry.arguments,
    )


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class ToolResultEntry:
    """A tool's result in a session's history: the pair of a :class:`ToolCallEntry`.

    ``id`` and ``turn_id`` are as in :class:`ToolCallEntry`. ``tool_call_id`` is the id of the call
    this result answers. ``name`` is the tool's full ID, such as ``client.get_weather``, or ``None``
    when the host did not report it.
    ``content`` is the content blocks the tool returned, the block classes of a turn's input; a
    tool that returned a string has one text block. ``structured_content`` is the tool's structured
    output, such as a dict, or ``None`` when it returned none. ``is_error`` is ``True`` when the
    call failed: ``content`` then holds the error's message as one text block when the host sends
    no content, else the host's content blocks. ``structured_content`` then holds the failed call's
    output when the host sent one, such as a failed command's stdout and stderr. ``meta`` is the
    result's host metadata (MCP ``_meta``), as in :class:`ToolResult`; it is empty when the host
    sent none. Do not change ``structured_content`` or ``meta``, copy them first.
    """

    __match_args__ = ("name", "content")

    id: str
    turn_id: str | None
    tool_call_id: str
    name: str | None
    content: tuple[ContentBlock, ...]
    structured_content: JsonValue
    is_error: bool
    meta: dict[str, JsonValue] = field(default_factory=dict)


def tool_result_entry(entry: ToolResultHistoryEntry) -> ToolResultEntry:
    """The SDK's tool result entry for the host's ``tool_result`` history entry.

    The host's ``result`` holds the tool's content blocks, its text, or its structured output. A
    non-empty list whose every item is a content block is read as content blocks, a string as one text block;
    any other value is structured output. A host that also sends ``content`` (the blocks ``result``
    does not hold) and ``meta`` has them read from there.
    """
    host_content: list[ContentBlock] | None = entry.content
    host_meta: dict[str, JsonValue] | None = entry.meta
    content: tuple[ContentBlock, ...] = ()
    structured_content: JsonValue = None
    if entry.error is not None:
        content = tuple(host_content) if host_content is not None else (TextContentBlock(text=entry.error.message),)
        structured_content = entry.result
    elif host_content is not None:
        content = tuple(host_content)
        structured_content = entry.result
    elif isinstance(entry.result, str):
        content = (TextContentBlock(text=entry.result),)
    elif (blocks := _content_blocks(entry.result)) is not None:
        content = blocks
    else:
        structured_content = entry.result
    return ToolResultEntry(
        id=entry.id,
        turn_id=entry.turn_id,
        tool_call_id=entry.tool_call_id,
        name=entry.name,
        content=content,
        structured_content=structured_content,
        is_error=entry.error is not None,
        meta=dict(host_meta or {}),
    )


def _content_blocks(result: JsonValue) -> tuple[ContentBlock, ...] | None:
    """``result`` as content blocks, or ``None`` when it is not a non-empty list of content blocks.

    An empty list is structured output (``structured_content=[]``, no content), so a tool that
    returned ``[]`` keeps it. ``result`` alone cannot tell that apart from a successful result with
    no blocks and no structured output, which today's host also writes as ``[]``; this reading is
    chosen on purpose.
    """
    if not isinstance(result, list) or not result:
        return None
    try:
        return tuple(ContentBlockAdapter.validate_python(block) for block in result)
    except ValidationError:
        return None


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class UnknownEntry:
    """An entry in a session's history of a type this SDK does not know.

    A newer host can add entry types. Such an entry is kept in the history, in its place, instead of
    failing the read. ``id`` and ``turn_id`` are as in :class:`ToolCallEntry`. ``type`` is the
    entry's type as the host sent it, such as ``"future_entry"``. ``raw`` is the whole entry as a
    JSON object, in the host's wire form and with its own ``type``: it keeps the fields this SDK
    does not know, and holds only the fields the host sent. A field of the entry named
    ``originalType`` is not kept: the host's models use that name for the entry's type. Do not change it, copy it first.

    A newer SDK can know the type and give a typed entry for it instead.
    """

    __match_args__ = ("type", "raw")

    id: str
    turn_id: str | None
    type: str
    raw: dict[str, JsonValue]


def unknown_entry(entry: UnknownHistoryEntry) -> UnknownEntry:
    """The SDK's unknown entry for a host history entry of a type the host's models do not know."""
    raw = entry.model_dump(mode="json", by_alias=True, exclude={"original_type"}, exclude_unset=True)
    raw["type"] = entry.original_type
    return UnknownEntry(id=entry.id, turn_id=entry.turn_id, type=entry.original_type, raw=raw)
