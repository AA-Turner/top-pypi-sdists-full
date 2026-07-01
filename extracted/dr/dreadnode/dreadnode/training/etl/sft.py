"""Reusable SFT ETL helpers for hosted training datasets."""

from __future__ import annotations

import json
import typing as t
from dataclasses import dataclass

from dreadnode.training.etl._common import (
    apply_system_prompt,
    normalize_messages,
    normalize_optional_string,
    normalize_prompt,
)

if t.TYPE_CHECKING:
    from dreadnode.datasets.dataset import Dataset
    from dreadnode.datasets.local import LocalDataset
    from dreadnode.training.etl.worlds import OpenAIConversation


@dataclass(slots=True)
class SFTConversation:
    """Normalized conversation row for supervised fine-tuning."""

    messages: list[dict[str, str]]
    metadata: dict[str, t.Any]


def load_sft_conversations_from_dataset(
    dataset: Dataset | LocalDataset,
    *,
    split: str | None = None,
    limit: int | None = None,
    system_prompt: str | None = None,
) -> list[SFTConversation]:
    """Load a published dataset into normalized SFT conversations."""

    table = dataset.load(split=split)
    records = [record for record in table.to_pylist() if isinstance(record, dict)]
    conversations = convert_records_to_sft_conversations(
        records,
        system_prompt=system_prompt,
    )
    if limit is None:
        return conversations
    return conversations[:limit]


def convert_records_to_sft_conversations(
    records: list[dict[str, t.Any]],
    *,
    system_prompt: str | None = None,
) -> list[SFTConversation]:
    """Convert record dictionaries into SFT conversations."""

    conversations = [
        _normalize_sft_conversation(record=record, system_prompt=system_prompt)
        for record in records
    ]
    return [conversation for conversation in conversations if conversation is not None]


def _normalize_sft_conversation(
    *,
    record: dict[str, t.Any],
    system_prompt: str | None,
) -> SFTConversation | None:
    # Records carrying structured tool_calls / tool_call_id are routed through
    # the renderer-aware OpenAIConversation pipeline (see
    # convert_records_to_openai_conversations) so each model's native tool-call
    # format is preserved during tokenization. Returning None here keeps them
    # out of the text-only path.
    if _record_has_structured_tool_calls(record):
        return None

    messages = normalize_messages(record.get("messages"))

    if not messages:
        messages = _messages_from_atif_steps(record)

    if not messages:
        prompt = normalize_prompt(record)
        completion = normalize_optional_string(
            record.get("expected_output")
            or record.get("target")
            or record.get("answer")
            or record.get("output")
        )
        if prompt and completion:
            messages = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": completion},
            ]

    if not messages:
        return None

    normalized_messages = apply_system_prompt(
        system_prompt=system_prompt,
        messages=messages,
    )
    metadata = {
        key: value
        for key, value in record.items()
        if key
        not in {"messages", "prompt", "input", "question", "task_prompt", "steps"}
    }
    return SFTConversation(messages=normalized_messages, metadata=metadata)


def _messages_from_atif_steps(record: dict[str, t.Any]) -> list[dict[str, str]]:
    """Extract chat messages from a Worlds/ATIF trajectory record.

    Worlds publishes datasets where each row is an ATIF trajectory: the
    conversation lives under `steps[*]` with a `source` and a `message`
    string. We preserve every step that carries content — including `tool`
    steps that hold tool-call results the assistant's next move references.
    Dropping them would leave the assistant talking to nothing, even though
    only assistant-role tokens carry loss weight downstream.

    `source` is canonicalised (`agent` → `assistant`) and otherwise passed
    through; the tinker tokenizer's `_normalize_role` collapses anything
    unrecognised to `user` for the header but keeps the body content intact.
    The dedicated `load_sft_conversations_from_worlds_dataset` covers the
    `trajectory_datasets` slot end-to-end; this slice picks up Worlds rows
    that get routed through the regular `dataset` slot.
    """

    raw_steps = record.get("steps")
    if not isinstance(raw_steps, list):
        return []
    messages: list[dict[str, str]] = []
    for step in raw_steps:
        if not isinstance(step, dict):
            continue
        source = normalize_optional_string(step.get("source"))
        content = normalize_optional_string(step.get("message"))
        if source is None or content is None:
            continue
        role = "assistant" if source == "agent" else source
        messages.append({"role": role, "content": content})
    return messages


def load_openai_conversations_from_dataset(
    dataset: Dataset | LocalDataset,
    *,
    split: str | None = None,
    limit: int | None = None,
    system_prompt: str | None = None,
) -> list[OpenAIConversation]:
    """Load transcript-shaped rows into renderer-ready OpenAI conversations.

    Sibling of `load_sft_conversations_from_dataset`. Same dataset, per-record
    dispatch — this loader picks up rows whose `messages` carry structured
    `tool_calls` / `tool_call_id` (e.g. `dn eval get-transcript` exports);
    plain text rows continue through the SFT loader. Returned conversations
    feed `load_from_conversations` so the model's tinker renderer applies its
    native tool-call template instead of any fixed text rendering.
    """

    table = dataset.load(split=split)
    records = [record for record in table.to_pylist() if isinstance(record, dict)]
    conversations = convert_records_to_openai_conversations(
        records,
        system_prompt=system_prompt,
    )
    if limit is None:
        return conversations
    return conversations[:limit]


def convert_records_to_openai_conversations(
    records: list[dict[str, t.Any]],
    *,
    system_prompt: str | None = None,
) -> list[OpenAIConversation]:
    """Convert transcript-shaped record dicts into OpenAI conversations."""

    conversations: list[OpenAIConversation] = []
    for record in records:
        if not _record_has_structured_tool_calls(record):
            continue
        converted = _normalize_openai_conversation(
            record=record, system_prompt=system_prompt
        )
        if converted is not None:
            conversations.append(converted)
    return conversations


def _record_has_structured_tool_calls(record: dict[str, t.Any]) -> bool:
    """True when a record's `messages` carry structured tool-call fields.

    Detection signals: a non-empty `tool_calls` list on any message, or a
    `tool_call_id` on any message. These are the fields the SessionTranscript
    response surfaces, and they're meaningless without a renderer that knows
    how to emit them per-model — so detecting either one routes the record
    out of the text-only SFT path.
    """

    raw_messages = record.get("messages")
    if not isinstance(raw_messages, list):
        return False
    for item in raw_messages:
        if not isinstance(item, dict):
            continue
        tool_calls = item.get("tool_calls")
        if isinstance(tool_calls, list) and tool_calls:
            return True
        if normalize_optional_string(item.get("tool_call_id")):
            return True
    return False


def _normalize_openai_conversation(
    *,
    record: dict[str, t.Any],
    system_prompt: str | None,
) -> OpenAIConversation | None:
    """Render a transcript-shaped record into an OpenAIConversation.

    Tool calls in transcript responses arrive as `{id, name, arguments}`
    (see `app.sessions.schemas.ToolCallResponse`); the renderer expects the
    chat-completion shape `{id, type, function: {name, arguments}}`. We
    translate here. `arguments` is preserved as-is when it's already a JSON
    string, otherwise serialized — every tinker renderer reads it as text.

    `tools=[]` is intentional: the renderer uses tools only to synthesize a
    leading "available tools" preamble, which is helpful but not required
    for imitation training. The session's tool surface isn't currently
    exposed alongside transcripts; once the export endpoint includes it,
    callers can plumb a non-empty tools list through.
    """

    raw_messages = record.get("messages")
    if not isinstance(raw_messages, list):
        return None

    from dreadnode.training.etl.worlds import OpenAIMessage

    messages: list[OpenAIMessage] = []
    for item in raw_messages:
        if not isinstance(item, dict):
            continue
        role = normalize_optional_string(item.get("role")) or "user"
        raw_content = item.get("content")
        content = "" if raw_content is None else str(raw_content)
        tool_calls = _normalize_tool_calls(item.get("tool_calls"))
        tool_call_id = normalize_optional_string(item.get("tool_call_id"))

        # Drop pure no-ops — neither text nor structured tool fields. Keeps
        # malformed transcripts from emitting empty turns the renderer would
        # frame with header/footer tokens for nothing.
        if not content and not tool_calls and not tool_call_id:
            continue

        msg = t.cast("OpenAIMessage", {"role": role, "content": content})
        if tool_calls:
            msg["tool_calls"] = tool_calls
        if tool_call_id:
            msg["tool_call_id"] = tool_call_id
        messages.append(msg)

    if not messages:
        return None

    normalized_system_prompt = normalize_optional_string(system_prompt)
    if normalized_system_prompt is not None:
        if messages and messages[0].get("role") == "system":
            existing = messages[0].get("content", "")
            merged: OpenAIMessage = {
                **messages[0],
                "content": f"{normalized_system_prompt}\n\n{existing}".strip(),
            }
            messages = [merged, *messages[1:]]
        else:
            messages = [
                t.cast(
                    "OpenAIMessage",
                    {"role": "system", "content": normalized_system_prompt},
                ),
                *messages,
            ]

    return t.cast("OpenAIConversation", {"tools": [], "messages": messages})


def _normalize_tool_calls(value: t.Any) -> list[dict[str, t.Any]]:
    """Normalize transcript-shape tool_calls to the chat-completion shape.

    Accepts both `{id, name, arguments}` (transcript) and `{id, type,
    function: {name, arguments}}` (already-normalized chat-completion). Drops
    entries missing a function name. Arguments are coerced to a JSON string —
    every tinker renderer reads `function.arguments` as text.
    """

    if not isinstance(value, list):
        return []
    normalized: list[dict[str, t.Any]] = []
    for tc in value:
        if not isinstance(tc, dict):
            continue
        function = tc.get("function") if isinstance(tc.get("function"), dict) else {}
        name = normalize_optional_string(tc.get("name") or function.get("name"))
        if name is None:
            continue
        raw_arguments = tc.get("arguments")
        if raw_arguments is None:
            raw_arguments = function.get("arguments")
        if isinstance(raw_arguments, str):
            arguments = raw_arguments
        elif raw_arguments is None:
            arguments = ""
        else:
            arguments = json.dumps(raw_arguments, ensure_ascii=False, sort_keys=True)
        tc_id = normalize_optional_string(tc.get("id")) or ""
        normalized.append(
            {
                "id": tc_id,
                "type": "function",
                "function": {"name": name, "arguments": arguments},
            }
        )
    return normalized


__all__ = [
    "SFTConversation",
    "convert_records_to_openai_conversations",
    "convert_records_to_sft_conversations",
    "load_openai_conversations_from_dataset",
    "load_sft_conversations_from_dataset",
]
