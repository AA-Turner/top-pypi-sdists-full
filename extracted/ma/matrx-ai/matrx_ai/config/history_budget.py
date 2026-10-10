"""A TOKEN budget for the history a conversation hands the model — shared by every channel.

A turn window (``thread_context_turns``) bounds HOW MANY turns are read; it says nothing about
how big they are. On the SMS/voice staff thread 40 turns of tool results inflated each text to
~60k input tokens (sms-assistant cost report, 2026-10-09). This is the size bound: when the
persisted history is estimated over ``budget_tokens``, the OLDEST tool results are replaced — one
at a time, oldest first — by the same cleared-result stub the context trimmer writes, until the
history fits. Words from the person and the assistant's answers are never touched; tool_use <->
tool_result pairing survives (only the result ``content`` is rewritten); media-bearing results
and already-cleared ones are skipped.

Pure and host-free: a host door (``conversation_history_window``) reads its budget knob and calls
this. Any channel reuses it by passing a different budget; ``None``/``<= 0`` means unbounded.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from matrx_ai.config.context_trim import (
    _DEFAULT_SUBSTITUTE,
    _already_trimmed,
    _get_content,
    _is_media_bearing,
    _is_tool_call_block,
    _is_tool_result_block,
    _rewrite_block_content,
)

_CHARS_PER_TOKEN = 4  # the platform's rough estimate; the budget is a soft cost bound, not a limit


@dataclass
class HistoryBudgetReport:
    budget_tokens: int
    tokens_before: int
    tokens_after: int
    blocks_cleared: int

    @property
    def over_budget_after(self) -> bool:
        return self.tokens_after > self.budget_tokens


def _blocks(message: Any) -> list[Any]:
    content = message.get("content") if isinstance(message, dict) else getattr(message, "content", None)
    if isinstance(content, list):
        return content
    return []


def _block_chars(block: Any) -> int:
    if _is_tool_result_block(block):
        content = _get_content(block)
        return len(content) if isinstance(content, str) else len(json.dumps(content, default=str))
    if _is_tool_call_block(block):
        args = block.get("arguments") if isinstance(block, dict) else getattr(block, "arguments", None)
        return len(json.dumps(args, default=str)) if args else 0
    text = block.get("text") if isinstance(block, dict) else getattr(block, "text", None)
    return len(text) if isinstance(text, str) else 0


def _message_chars(message: Any) -> int:
    blocks = _blocks(message)
    if not blocks:
        content = message.get("content") if isinstance(message, dict) else getattr(message, "content", None)
        return len(content) if isinstance(content, str) else 0
    return sum(_block_chars(block) for block in blocks)


def estimate_history_tokens(messages: list[Any]) -> int:
    return sum(_message_chars(m) for m in messages) // _CHARS_PER_TOKEN


def trim_history_to_token_budget(
    messages: list[Any], budget_tokens: int | None, *, marker: str = _DEFAULT_SUBSTITUTE
) -> HistoryBudgetReport:
    """Clear oldest tool results in place until the estimate fits ``budget_tokens``."""
    before = estimate_history_tokens(messages)
    if not budget_tokens or budget_tokens <= 0 or before <= budget_tokens:
        return HistoryBudgetReport(int(budget_tokens or 0), before, before, 0)

    total_chars = before * _CHARS_PER_TOKEN
    limit_chars = budget_tokens * _CHARS_PER_TOKEN
    cleared = 0
    for message in messages:
        for block in _blocks(message):
            if total_chars <= limit_chars:
                break
            if not _is_tool_result_block(block) or _already_trimmed(block) or _is_media_bearing(block):
                continue
            was = _block_chars(block)
            _rewrite_block_content(block, marker)
            total_chars -= max(0, was - _block_chars(block))
            cleared += 1
        if total_chars <= limit_chars:
            break
    return HistoryBudgetReport(budget_tokens, before, estimate_history_tokens(messages), cleared)


__all__ = ["HistoryBudgetReport", "estimate_history_tokens", "trim_history_to_token_budget"]
