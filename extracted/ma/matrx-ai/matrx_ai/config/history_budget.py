"""A TOKEN budget for the history a conversation hands the model — shared by every channel.

A turn window (``held_history_turns``) bounds HOW MANY turns are read; it says nothing about
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
from dataclasses import dataclass, field
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
    #: The ``tool_use_id`` of every result this pass cleared — a cut is replayed from these while the cache is warm.
    cleared_ids: list[str] = field(default_factory=list)

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
    cleared_ids: list[str] = []
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
            tool_use_id = _tool_use_id(block)
            if tool_use_id:
                cleared_ids.append(tool_use_id)
        if total_chars <= limit_chars:
            break
    return HistoryBudgetReport(budget_tokens, before, estimate_history_tokens(messages), cleared, cleared_ids)


def _tool_use_id(block: Any) -> str | None:
    value = block.get("tool_use_id") if isinstance(block, dict) else getattr(block, "tool_use_id", None)
    return str(value) if value else None


def clear_tool_results(messages: list[Any], tool_use_ids: set[str], *, marker: str = _DEFAULT_SUBSTITUTE) -> int:
    """Clear exactly the results named by ``tool_use_ids`` (already-cleared ones are left alone): the warm-cache
    replay of a recorded cut, so the prefix the provider cached is rebuilt byte for byte."""
    cleared = 0
    if not tool_use_ids:
        return 0
    for message in messages:
        for block in _blocks(message):
            if not _is_tool_result_block(block) or _already_trimmed(block):
                continue
            if _tool_use_id(block) in tool_use_ids:
                _rewrite_block_content(block, marker)
                cleared += 1
    return cleared


def _role(message: Any) -> str:
    if isinstance(message, dict):
        return str(message.get("role") or "")
    return str(getattr(message, "role", "") or "")


def last_turns(messages: list[Any], turns: int) -> list[Any]:
    """The last ``turns`` turns of this history, cut at a turn boundary.

    A TURN IS A MESSAGE FROM THE PERSON AND EVERYTHING THAT ANSWERED IT, so the cut lands on a ``user`` row and
    never in the middle of one (a history opening on an orphan tool result is a 400 from every provider). Fewer
    turns than the window drops nothing; a window of zero or less is refused, never silently empties the chat.
    """
    if turns <= 0:
        raise ValueError(
            f"the history window resolved to {turns} turns, which would hand the agent no history at all. "
            "Refusing to run a turn on a window nobody could have meant."
        )
    starts = [index for index, message in enumerate(messages) if _role(message) == "user"]
    if len(starts) <= turns:
        return messages
    return messages[starts[-turns] :]


class HistoryWindowUnavailable(RuntimeError):
    """The host has a window for this conversation but could not say what it is (a knob it cannot read, a window
    of zero). The turn fails loudly — the resolver re-raises it — never runs on a window nobody chose."""


@dataclass(frozen=True)
class HistoryWindowPolicy:
    """What the HOST decides for one conversation's history window (its knobs); the send boundary applies it.

    ``turns`` — read back only the last this-many turns; ``token_budget`` — then clear the oldest tool results
    until the history fits (``None``/``<= 0`` = unbounded); ``waits_for_cold_cache`` — move the cut only when the
    provider cache is already cold, so a warm conversation's prefix stays byte-identical (the cache law)."""

    turns: int
    token_budget: int | None = None
    waits_for_cold_cache: bool = True


__all__ = [
    "HistoryBudgetReport",
    "HistoryWindowPolicy",
    "HistoryWindowUnavailable",
    "clear_tool_results",
    "estimate_history_tokens",
    "last_turns",
    "trim_history_to_token_budget",
]
