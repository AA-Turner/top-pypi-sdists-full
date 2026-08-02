"""Completion request projection from execution state."""

import json
from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from mistralai.vibe.sdk.execution_record.state import (
    CompletedOutput,
    FailedOutput,
    HistoryEntry,
    MessageEntry,
    StateEntry,
    TaskCallEntry,
    TaskResultEntry,
    TaskState,
    content_text,
)
from mistralai.vibe.sdk.execution_record.utils import model_context_projection
from mistralai.vibe.sdk.providers.completion.messages import (
    FunctionCall,
    Message,
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
) -> CompletionRequest:
    """Build a CompletionRequest from TaskState history."""
    messages: list[Message] = []

    history = state.history
    projection = _completion_projection(history)
    if projection.preserved_system_content is not None:
        messages.append(Message(role="system", content=projection.preserved_system_content))
    if projection.compaction_summary is not None:
        messages.append(Message(role="user", content=projection.compaction_summary))

    for index, entry in projection.entries:
        if isinstance(entry, MessageEntry):
            if entry.payload.channel == "thinking":
                continue

            role = entry.payload.role
            content = content_text(entry.payload.content)

            if role == "system":
                messages.append(Message(role="system", content=content))
            elif role == "user":
                messages.append(Message(role="user", content=content))
            elif role == "assistant":
                msg = Message(role="assistant", content=content or None)
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
                result_content = json.dumps(child_state.output.value)
            elif child_state and isinstance(child_state.output, FailedOutput):
                result_content = f"Error: {child_state.output.error}"
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


__all__ = ["build_completion_request_from_state", "tool_call_provider_id"]
