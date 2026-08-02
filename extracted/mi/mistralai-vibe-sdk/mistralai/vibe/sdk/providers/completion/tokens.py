"""Token estimation helpers for compaction decisions."""

from __future__ import annotations

import math
from typing import Any

from mistralai.vibe.sdk.execution_record.snapshots import latest_snapshot_index
from mistralai.vibe.sdk.execution_record.state import MessageEntry, TaskState
from mistralai.vibe.sdk.providers.completion.bridge import (
    build_completion_request_from_state,
)
from mistralai.vibe.sdk.providers.completion.messages import Message
from mistralai.vibe.sdk.providers.completion.types import (
    AGENT_COMPACTION_SENTINEL_TYPE,
    COMPLETION_USAGE_ANNOTATION,
    CompletionRequest,
)
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage

__all__ = [
    "estimate_completion_request_tokens",
    "estimate_context_tokens",
    "latest_compaction_sentinel_index",
]


def estimate_completion_request_tokens(request: CompletionRequest) -> int:
    """Return a conservative local estimate for a completion request."""
    token_count = sum(_estimate_message_tokens(message) for message in request.messages)
    if request.tools:
        token_count += sum(
            4 + _estimate_text_tokens(tool.model_dump_json()) for tool in request.tools
        )
    return token_count


def estimate_context_tokens(
    state: TaskState,
    task_implementations: dict[str, Any],
    *,
    prefer_reported_usage: bool = True,
) -> int:
    """Estimate context pressure for a state.

    When possible, use the latest provider-reported assistant usage as the
    baseline, then estimate only entries added after that response.
    """
    if prefer_reported_usage:
        latest_sentinel_index = latest_compaction_sentinel_index(state)
        for index in range(len(state.history) - 1, latest_sentinel_index, -1):
            entry = state.history[index]
            if not isinstance(entry, MessageEntry) or entry.payload.role != "assistant":
                continue
            context_tokens = _context_tokens_from_annotation(entry)
            if context_tokens is None:
                continue

            suffix_state = state.model_copy(update={"history": state.history[index + 1 :]})
            suffix_request = build_completion_request_from_state(suffix_state, {})
            return context_tokens + estimate_completion_request_tokens(suffix_request)

    request = build_completion_request_from_state(state, task_implementations)
    return estimate_completion_request_tokens(request)


def _estimate_message_tokens(message: Message) -> int:
    token_count = 4 + _estimate_text_tokens(message.role) + _estimate_text_tokens(message.content)
    if message.tool_call_id:
        token_count += _estimate_text_tokens(message.tool_call_id)
    if message.tool_calls:
        token_count += sum(
            _estimate_text_tokens(
                "".join(
                    [
                        tool_call.id,
                        tool_call.function.name,
                        tool_call.function.arguments,
                    ]
                )
            )
            for tool_call in message.tool_calls
        )
    return token_count


def _estimate_text_tokens(text: str | None) -> int:
    if not text:
        return 0
    return max(1, math.ceil(len(text) / 4))


def latest_compaction_sentinel_index(state: TaskState) -> int:
    index = latest_snapshot_index(state, AGENT_COMPACTION_SENTINEL_TYPE)

    return index if index is not None else -1


def _context_tokens_from_annotation(entry: MessageEntry) -> int | None:
    usage = (entry.annotations or {}).get(COMPLETION_USAGE_ANNOTATION)
    if not isinstance(usage, dict):
        return None

    context_tokens = usage.get("context_tokens")
    if isinstance(context_tokens, int):
        return context_tokens

    parsed = TokenUsage.model_validate(usage)
    return parsed.context_tokens if not parsed.is_empty else None
