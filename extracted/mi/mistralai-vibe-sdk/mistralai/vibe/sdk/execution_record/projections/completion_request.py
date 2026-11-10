"""Completion request projection from execution state."""

import json
from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from mistralai.vibe.sdk.execution_record.state import (
    CompletedOutput,
    FailedOutput,
    HistoryEntry,
    ImageContentBlock,
    MessageEntry,
    StateEntry,
    TaskCallEntry,
    TaskResultEntry,
    TaskState,
    ThinkingContentBlock,
    content_text,
)
from mistralai.vibe.sdk.execution_record.utils import model_context_projection
from mistralai.vibe.sdk.providers.completion.messages import (
    FunctionCall,
    ImageURL,
    ImageURLMessageContentChunk,
    Message,
    MessageContentChunk,
    TextMessageContentChunk,
    ToolCall,
)
from mistralai.vibe.sdk.providers.completion.types import (
    AGENT_COMPACTION_SENTINEL_TYPE,
    COMPLETION_REQUEST_KIND_AGENT,
    AgentCompactionSentinelContent,
    CompletionRequest,
    CompletionRequestKind,
    FunctionSpec,
    ToolDefinition,
)

_PROVIDER_ID_PREFIX = "llm:"
DEFAULT_MAX_TOOL_RESULT_CHARS = 40_000
MIN_MAX_TOOL_RESULT_CHARS = 256
_TOOL_RESULT_TRUNCATION_MARKER = "\n...[tool result truncated for model context]...\n"


@dataclass(frozen=True)
class _Reasoning:
    text: str
    signature: str | None


@dataclass(frozen=True)
class _CompletionProjection:
    preserved_system_content: str | None
    compaction_summary: str | None
    entries: list[tuple[int, HistoryEntry]]


def tool_call_provider_id(call_id: str) -> str:
    """Extract the provider-local id embedded by encode_tool_call_id()."""
    if not call_id.startswith(_PROVIDER_ID_PREFIX):
        return call_id

    remainder = call_id.removeprefix(_PROVIDER_ID_PREFIX)
    decoder = json.JSONDecoder()
    try:
        provider_id, _end = decoder.raw_decode(remainder)
    except json.JSONDecodeError:
        return call_id
    return provider_id if isinstance(provider_id, str) else call_id


@model_context_projection()
def build_completion_request_from_state(
    state: TaskState,
    task_implementations: dict[str, Any],
    *,
    metadata: dict[str, Any] | None = None,
    request_kind: CompletionRequestKind = COMPLETION_REQUEST_KIND_AGENT,
    max_tool_result_chars: int = DEFAULT_MAX_TOOL_RESULT_CHARS,
) -> CompletionRequest:
    """Build a CompletionRequest from TaskState history."""
    if max_tool_result_chars < MIN_MAX_TOOL_RESULT_CHARS:
        raise ValueError(f"max_tool_result_chars must be at least {MIN_MAX_TOOL_RESULT_CHARS}")

    messages: list[Message] = []

    history = state.history
    projection = _completion_projection(history)
    if projection.preserved_system_content is not None:
        messages.append(Message(role="system", content=projection.preserved_system_content))
    if projection.compaction_summary is not None:
        messages.append(Message(role="user", content=projection.compaction_summary))

    reasoning = _assistant_reasoning(projection.entries)
    for index, entry in projection.entries:
        if isinstance(entry, MessageEntry):
            if entry.payload.channel == "thinking":
                continue

            role = entry.payload.role
            content = _message_content(entry)

            if role == "system":
                messages.append(Message(role="system", content=content_text(entry.payload.content)))
            elif role == "user":
                messages.append(Message(role="user", content=content))
            elif role == "assistant":
                text_content = content_text(entry.payload.content)
                entry_reasoning = reasoning.get(index)
                msg = Message(
                    role="assistant",
                    content=text_content or None,
                    reasoning_content=entry_reasoning.text if entry_reasoning else None,
                    reasoning_signature=entry_reasoning.signature if entry_reasoning else None,
                )
                tool_calls = _collect_assistant_tool_calls(history, index)
                if tool_calls:
                    msg.tool_calls = [
                        ToolCall(
                            id=tool_call_provider_id(tc.payload.id),
                            function=FunctionCall(
                                name=tc.payload.name,
                                arguments=json.dumps(tc.payload.input),
                            ),
                        )
                        for tc in tool_calls
                    ]
                messages.append(msg)

        elif isinstance(entry, TaskResultEntry):
            call_id = tool_call_provider_id(entry.payload.id)
            child_state = entry.payload.state
            if child_state and isinstance(child_state.output, CompletedOutput):
                result_content = _bounded_tool_result(
                    child_state.output.value,
                    max_chars=max_tool_result_chars,
                )
            elif child_state and isinstance(child_state.output, FailedOutput):
                error_content = f"Error: {child_state.output.error}"
                if len(error_content) <= max_tool_result_chars:
                    result_content = error_content
                else:
                    result_content = _bounded_tool_result(
                        {"error": child_state.output.error},
                        max_chars=max_tool_result_chars,
                    )
            else:
                result_content = "Pending..."
            messages.append(
                Message(
                    role="tool",
                    content=result_content,
                    tool_call_id=call_id,
                )
            )

        elif isinstance(entry, TaskCallEntry):
            pass

    tools = _implementations_to_tools(task_implementations)

    return CompletionRequest(
        messages=messages,
        tools=tools or None,
        metadata=metadata,
        request_kind=request_kind,
    )


def _thinking_signature(entry: MessageEntry) -> str | None:
    blocks = [block for block in entry.payload.content if isinstance(block, ThinkingContentBlock)]
    return blocks[-1].signature if blocks else None


def _assistant_reasoning(entries: list[tuple[int, HistoryEntry]]) -> dict[int, _Reasoning]:
    """Map each visible assistant message index to the thinking of its completion.

    One completion writes at most one thinking entry and one visible entry, next to each
    other in either order. Thinking with no visible entry in its run has nothing to ride on.
    The Mistral API takes one thinking chunk per message, so merged thinking carries the last
    block's signature: the provider then keeps that block, where unsigned it would keep none.
    """
    reasoning: dict[int, list[tuple[str, str | None]]] = {}
    pending: list[tuple[str, str | None]] = []
    last_visible: int | None = None

    def flush() -> None:
        if pending and last_visible is not None:
            reasoning.setdefault(last_visible, []).extend(pending)
        pending.clear()

    for index, entry in entries:
        if not (isinstance(entry, MessageEntry) and entry.payload.role == "assistant"):
            flush()
            last_visible = None
            continue
        if entry.payload.channel == "thinking":
            if text := content_text(entry.payload.content):
                pending.append((text, _thinking_signature(entry)))
            continue
        if pending:
            reasoning.setdefault(index, []).extend(pending)
            pending.clear()
        last_visible = index
    flush()
    return {
        index: _Reasoning(
            text="".join(text for text, _signature in parts),
            signature=parts[-1][1],
        )
        for index, parts in reasoning.items()
    }


def _bounded_tool_result(value: Any, *, max_chars: int) -> str:
    """Serialize bounded model-visible output without changing the durable result."""
    content = json.dumps(value)
    if len(content) <= max_chars:
        return content

    def truncation_envelope(retained_chars: int) -> str:
        prefix_chars = (retained_chars + 1) // 2
        suffix_chars = retained_chars // 2
        return json.dumps(
            {
                "_truncated": True,
                "original_chars": len(content),
                "content": (
                    content[:prefix_chars]
                    + _TOOL_RESULT_TRUNCATION_MARKER
                    + content[len(content) - suffix_chars :]
                ),
            }
        )

    lower = 0
    upper = max_chars
    best = truncation_envelope(0)
    while lower <= upper:
        retained_chars = (lower + upper) // 2
        candidate = truncation_envelope(retained_chars)
        if len(candidate) <= max_chars:
            best = candidate
            lower = retained_chars + 1
        else:
            upper = retained_chars - 1
    return best


def _message_content(entry: MessageEntry) -> str | list[MessageContentChunk] | None:
    chunks: list[MessageContentChunk] = []
    for block in entry.payload.content:
        match block:
            case ImageContentBlock(image_url=image_url):
                chunks.append(ImageURLMessageContentChunk(image_url=ImageURL(url=image_url)))
            case _:
                text = content_text([block])
                if text:
                    chunks.append(TextMessageContentChunk(text=text))

    if not chunks:
        return None
    if len(chunks) == 1 and isinstance(chunks[0], TextMessageContentChunk):
        return chunks[0].text
    return chunks


def _completion_projection(history: list[HistoryEntry]) -> _CompletionProjection:
    sentinel = _latest_compaction_sentinel(history)
    if sentinel is None:
        return _CompletionProjection(
            preserved_system_content=None,
            compaction_summary=None,
            entries=list(enumerate(history)),
        )

    sentinel_index, summary = sentinel
    return _CompletionProjection(
        preserved_system_content=_latest_system_content_before_boundary(history, sentinel_index),
        compaction_summary=summary,
        entries=list(enumerate(history[sentinel_index + 1 :], start=sentinel_index + 1)),
    )


def _latest_compaction_sentinel(history: list[HistoryEntry]) -> tuple[int, str] | None:
    for index in range(len(history) - 1, -1, -1):
        entry = history[index]
        if not isinstance(entry, StateEntry):
            continue
        if entry.payload.type != AGENT_COMPACTION_SENTINEL_TYPE:
            continue
        return (index, _compaction_summary(entry))
    return None


def _compaction_summary(entry: StateEntry) -> str:
    try:
        content = AgentCompactionSentinelContent.model_validate(entry.payload.content)
    except ValidationError as exc:
        msg = "agent.compaction StateEntry payload.content must match {'summary': str}"
        raise ValueError(msg) from exc
    return content.summary


def _latest_system_content_before_boundary(
    history: list[HistoryEntry], boundary_index: int
) -> str | None:
    for entry in reversed(history[:boundary_index]):
        if isinstance(entry, MessageEntry) and entry.payload.role == "system":
            return content_text(entry.payload.content)
    return None


def _collect_assistant_tool_calls(
    history: list[Any],
    assistant_index: int,
) -> list[TaskCallEntry]:
    tool_calls: list[TaskCallEntry] = []
    for entry in history[assistant_index + 1 :]:
        if isinstance(entry, MessageEntry):
            if entry.payload.channel == "thinking":
                continue
            break
        if isinstance(entry, TaskCallEntry):
            tool_calls.append(entry)
    return tool_calls


def _implementations_to_tools(
    impls: dict[str, Any],
) -> list[ToolDefinition]:
    tools = []
    for name, task in impls.items():
        if isinstance(task, dict):
            desc = task.get("description", "") or name
            params = task.get("input_schema", {}) or {}
        else:
            desc = getattr(task, "description", "") or name
            params = getattr(task, "input_schema", {}) or {}
        spec = FunctionSpec(
            name=name,
            description=desc,
            parameters=params,
        )
        tools.append(ToolDefinition(function=spec))
    return tools


__all__ = [
    "DEFAULT_MAX_TOOL_RESULT_CHARS",
    "MIN_MAX_TOOL_RESULT_CHARS",
    "build_completion_request_from_state",
    "tool_call_provider_id",
]
