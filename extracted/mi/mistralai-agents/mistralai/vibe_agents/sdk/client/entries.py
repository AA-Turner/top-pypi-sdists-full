"""History entries: the items of a session's history, as immutable values.

The host keeps a session's history as a list of entries: messages, tool calls, tool results and
others. This module has the SDK's own types for a message entry, a context message, a tool call
entry, a tool result entry and an entry of a type the SDK does not know, and the functions that
build them from the host's entries, for any read that returns history.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from pydantic import JsonValue, ValidationError

from mistralai.vibe.harness.app_server.session import (
    CapabilityContextMessageHistoryEntry,
    ContentBlock,
    ContentBlockAdapter,
    HistoryEntry,
    InputContextMessageHistoryEntry,
    MessageHistoryEntry,
    TextContentBlock,
    ToolCallHistoryEntry,
    ToolResultHistoryEntry,
    UnknownHistoryEntry,
)

__all__ = [
    "ContextMessage",
    "Entry",
    "MessageEntry",
    "ToolCallEntry",
    "ToolResultEntry",
    "UnknownEntry",
    "context_message",
    "message_entry",
    "tool_call_entry",
    "tool_result_entry",
    "unknown_entry",
]


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class MessageEntry:
    """A message in a session's history: the user's, the model's, a system message or a context message.

    ``id`` and ``turn_id`` are as in :class:`ToolCallEntry`. ``role`` is ``"user"`` for a turn's
    input or a steer, ``"assistant"`` for the model's text, ``"system"`` for a system message
    given in a session's starting history, and ``"context"`` for a :class:`ContextMessage`.
    ``content`` is the message's content blocks, the block classes of a turn's input; ``text`` is
    their text, joined. A message another agent sent this session's model is an
    :class:`UnknownEntry` of type ``"message"``, with its sender in ``raw``.
    """

    __match_args__ = ("role", "content")

    id: str
    """The entry's ID in the history."""
    turn_id: str | None
    """The turn this entry belongs to, or ``None`` when it is not part of a turn, for example in a
    history given at the session's start."""
    role: Literal["user", "assistant", "system", "context"]
    """``"user"`` for a turn's input or a steer, ``"assistant"`` for the model's text, ``"system"``
    for a system message given in a session's starting history, ``"context"`` for a
    :class:`ContextMessage`."""
    content: tuple[ContentBlock, ...]
    """The message's content blocks, the block classes of a turn's input."""

    @property
    def text(self) -> str:
        """The text of the message's text blocks, joined; ``""`` when it has none."""
        return "".join(block.text for block in self.content if isinstance(block, TextContentBlock))


def message_entry(entry: MessageHistoryEntry) -> MessageEntry:
    """The SDK's message entry for the host's ``message`` history entry."""
    return MessageEntry(id=entry.id, turn_id=entry.turn_id, role=entry.role, content=tuple(entry.content))


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class ContextMessage(MessageEntry):
    """A context message in a session's history: text the model got with a turn's input, which is
    not the user's own message.

    It is a :class:`MessageEntry` whose ``role`` is ``"context"``; ``id``, ``turn_id``,
    ``content`` and ``text`` are as there. ``kind`` says who added it: ``"input"`` for a context
    message sent with a message, ``"capability_source"`` for one the session added about a tool
    source, such as a connector whose tools cannot be used now, or are back. ``source`` names
    that tool source, such as ``"mistral_connectors:notion"``, as in :class:`Notice`; it is
    ``None`` for a context message sent with a message. The model gets it just before the input
    of the turn start or the steer that carried it; the history has it after that input.
    """

    role: Literal["context"] = field(default="context", init=False)
    """Always ``"context"``."""
    kind: Literal["input", "capability_source"]
    """Who added it: ``"input"`` for a context message sent with a message,
    ``"capability_source"`` for one the session added about a tool source."""
    source: str | None
    """The tool source it is about, such as ``"mistral_connectors:notion"``, or ``None`` for a
    context message sent with a message."""


def context_message(entry: CapabilityContextMessageHistoryEntry | InputContextMessageHistoryEntry) -> ContextMessage:
    """The SDK's context message for the host's context message entry sent with a message, or about a
    tool source."""
    source = entry.source_id if isinstance(entry, CapabilityContextMessageHistoryEntry) else None
    return ContextMessage(
        id=entry.id, turn_id=entry.turn_id, content=tuple(entry.content), kind=entry.kind, source=source
    )


@dataclass(frozen=True, slots=True, kw_only=True, match_args=False)
class ToolCallEntry:
    """A tool call in a session's history: the model called a tool.

    ``id`` is the entry's ID in the history. ``turn_id`` is the turn the call was made in, or
    ``None`` when the entry is not part of a turn, for example in a history given at the session's
    start. ``tool_call_id`` names the call: the tool's result carries the same ID.
    ``name`` is the tool's full ID, such as ``client.get_weather``, as in :class:`ToolCall`.
    ``arguments`` is the call's arguments: the model's, or the ones a ``pre_tool_call`` hook set (a
    skipped call keeps the model's). Do not change it, copy it first.

    This is a history entry. :class:`ToolCall` stays the item of ``Completed.tool_calls``.
    """

    __match_args__ = ("name", "arguments")

    id: str
    """The entry's ID in the history."""
    turn_id: str | None
    """The turn this entry belongs to, or ``None`` when it is not part of a turn, for example in a
    history given at the session's start."""
    tool_call_id: str
    """The ID of the call: the tool's result carries the same ID."""
    name: str
    """The tool's full ID, such as ``client.get_weather``, as in :class:`ToolCall`."""
    arguments: JsonValue
    """The call's arguments: the model's, or the ones a ``pre_tool_call`` hook set (a skipped call keeps
    the model's). Do not change it, copy it first."""


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

    ``id`` and ``turn_id`` are as in :class:`ToolCallEntry`. ``tool_call_id`` is the ID of the call
    this result answers. ``name`` is the tool's full ID, such as ``client.get_weather``, or ``None``
    when it is not known.
    ``content`` is the content blocks the tool returned, the block classes of a turn's input; a
    tool that returned a string has one text block. ``structured_content`` is the tool's structured
    output, such as a dict, or ``None`` when it returned none. ``is_error`` is ``True`` when the
    call failed: ``content`` then holds the error's content blocks, or its message as one text
    block. ``structured_content`` then holds the failed call's output, if any, such as a failed
    command's stdout and stderr. ``meta`` is the result's metadata for the client, as MCP's
    ``_meta`` and as in :class:`ToolResult`; it is empty when there is none. Do not change
    ``structured_content`` or ``meta``, copy them first.
    """

    __match_args__ = ("name", "content")

    id: str
    """The entry's ID in the history."""
    turn_id: str | None
    """The turn this entry belongs to, or ``None`` when it is not part of a turn."""
    tool_call_id: str
    """The ID of the call this result answers."""
    name: str | None
    """The tool's full ID, such as ``client.get_weather``, or ``None`` when it is not known."""
    content: tuple[ContentBlock, ...]
    """The content blocks the tool returned, the block classes of a turn's input; a tool that returned a
    string has one text block. For a failed call, the error's content blocks, or its message as one
    text block."""
    structured_content: JsonValue
    """The tool's structured output, such as a dict, or ``None`` when it returned none. For a failed call,
    its output, if any, such as a failed command's stdout and stderr."""
    is_error: bool
    """``True`` when the call failed."""
    meta: dict[str, JsonValue] = field(default_factory=dict)
    """The result's metadata for the client, as MCP's ``_meta`` and as in :class:`ToolResult`; empty
    when there is none."""


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
    """An entry of a type added after your SDK version, or one this version reads only as raw data, such
    as a checkpoint. ``type`` names it, and ``raw`` holds its data.

    The entry keeps its place in the history instead of failing the read. ``id`` and ``turn_id`` are
    as in :class:`ToolCallEntry`. A later SDK version can give a typed entry instead.
    """

    __match_args__ = ("type", "raw")

    id: str
    """The entry's ID in the history."""
    turn_id: str | None
    """The turn this entry belongs to, or ``None`` when it is not part of a turn."""
    type: str
    """The entry's type, such as ``"checkpoint"``."""
    raw: dict[str, JsonValue]
    """The whole entry as a JSON object, unparsed, with its camelCase field names and its ``type``.
    Do not change it, copy it first."""


def unknown_entry(entry: HistoryEntry) -> UnknownEntry:
    """The SDK's unknown entry for a host history entry this SDK does not type: of a type the host's
    models do not know, or of one they know, such as a reasoning entry or a context message from
    another agent (whose ``type`` is ``"message"``)."""
    if isinstance(entry, UnknownHistoryEntry):
        raw = entry.model_dump(mode="json", by_alias=True, exclude={"original_type"}, exclude_unset=True)
        raw["type"] = entry.original_type
        return UnknownEntry(id=entry.id, turn_id=entry.turn_id, type=entry.original_type, raw=raw)
    # A message's role tells what it is, also the default role an in-process host leaves unset.
    raw = {
        **entry.model_dump(mode="json", by_alias=True, include={"role"}),
        **entry.model_dump(mode="json", by_alias=True, exclude_unset=True),
    }
    raw["type"] = entry.type
    return UnknownEntry(id=entry.id, turn_id=entry.turn_id, type=entry.type, raw=raw)


type Entry = MessageEntry | ToolCallEntry | ToolResultEntry | UnknownEntry
"""An entry of a session's history: a message (a :class:`ContextMessage` too), a tool call, a
tool's result, or an entry of a type added after your SDK version, or one this version reads only as raw
data, such as a checkpoint."""
