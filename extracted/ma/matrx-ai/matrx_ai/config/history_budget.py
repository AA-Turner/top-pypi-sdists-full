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

THE TURN BUDGET BINDS (2026-11-19, staff thread 3af9e95c): the tool-result budget never touches words, so a
history made of text — four earlier turns' kept turn context of ~87k characters each, thinking, answers — sat
at ~150k tokens under a "12,000-token" budget and pushed every staff send over the 200,000 input budget, where
the last-resort fit rewrote history on every send. :func:`cut_oldest_turns_to_budget` is the size bound that
binds: after the results are stubbed, while the history is still estimated over the host's turn budget, the
oldest WHOLE turns are left out (a cut lands on a person turn; the newest earlier turn and the turn in flight
always stay). Its estimate counts what each turn really sends: the kept turn context and late-tools carrier its
row replays (``typed_text_last.STORED_*``), not only the visible blocks.
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
    call_index,
    refetch_for,
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


def _replayed_chars(message: Any) -> int:
    """The characters an EARLIER turn's row puts back on every send it is read on: its kept whole turn-context
    block, else its late-tools carrier (``send_boundary._replayed_on`` reads the same keys)."""
    from matrx_ai.config.typed_text_last import STORED_LATE_TOOLS_KEY, STORED_TURN_CONTEXT_KEY

    metadata = message.get("metadata") if isinstance(message, dict) else getattr(message, "metadata", None)
    if not isinstance(metadata, dict):
        return 0
    kept = metadata.get(STORED_TURN_CONTEXT_KEY)
    if isinstance(kept, str) and kept:
        return len(kept)
    carrier = metadata.get(STORED_LATE_TOOLS_KEY)
    if isinstance(carrier, dict):
        return sum(len(v) for v in carrier.values() if isinstance(v, str))
    return 0


def _sent_chars(message: Any) -> int:
    return _message_chars(message) + _replayed_chars(message)


def estimate_sent_history_tokens(messages: list[Any]) -> int:
    """What this history really sends: every block plus each earlier turn's replayed turn context."""
    return sum(_sent_chars(m) for m in messages) // _CHARS_PER_TOKEN


def _is_person(message: Any) -> bool:
    """A person message: a ``user`` row that is not only tool results."""
    role = message.get("role") if isinstance(message, dict) else getattr(message, "role", None)
    if str(getattr(role, "value", role) or "") != "user":
        return False
    blocks = _blocks(message)
    return not (blocks and all(_is_tool_result_block(b) for b in blocks))


@dataclass
class TurnCutReport:
    budget_tokens: int
    tokens_before: int
    tokens_after: int
    turns_dropped: int

    @property
    def over_budget_after(self) -> bool:
        return self.tokens_after > self.budget_tokens


def cut_oldest_turns_to_budget(
    messages: list[Any], budget_tokens: int | None, *, protect_from: int | None = None
) -> tuple[list[Any], TurnCutReport]:
    """The newest whole turns of ``messages`` that fit ``budget_tokens`` (``estimate_sent_history_tokens``).

    A cut lands only on a person message (a history opening on an orphan tool result is a 400), so a turn is
    kept or left out whole. The newest earlier turn always stays, and so does the turn in flight (``protect_from``:
    the index of the person message that opened it, ``current_turn_start``); a history whose last turn alone is
    over the budget is kept as it is (``over_budget_after``) — size inside one turn is the trim's and the fit
    step's job. ``None``/``<= 0`` = unbounded. Pure: the caller applies the result."""
    sizes = [_sent_chars(m) for m in messages]
    before = sum(sizes) // _CHARS_PER_TOKEN
    if not budget_tokens or budget_tokens <= 0 or before <= budget_tokens:
        return messages, TurnCutReport(int(budget_tokens or 0), before, before, 0)
    starts = [i for i, m in enumerate(messages) if i > 0 and _is_person(m)]
    if protect_from is not None:
        starts = [i for i in starts if i < protect_from]  # the newest earlier turn stays with the one in flight
    limit_chars = budget_tokens * _CHARS_PER_TOKEN
    suffix = sum(sizes)
    chosen, consumed = 0, 0
    for start in starts:
        suffix -= sum(sizes[consumed:start])
        consumed = start
        chosen = start
        if suffix <= limit_chars:
            break
    if not chosen:
        return messages, TurnCutReport(budget_tokens, before, before, 0)
    persons_before = sum(1 for m in messages[:chosen] if _is_person(m))
    kept = messages[chosen:]
    return kept, TurnCutReport(budget_tokens, before, sum(sizes[chosen:]) // _CHARS_PER_TOKEN, persons_before)


def _protected_result_ids(
    messages: list[Any], *, keep_recent_tool_results: int, protect_from: int | None
) -> set[int]:
    """``id()`` of every tool-result block the budget may never clear: the newest ``keep_recent_tool_results``
    results, and every result at or after message index ``protect_from`` (the turn in flight)."""
    protected: set[int] = set()
    results = [
        (index, block)
        for index, message in enumerate(messages)
        for block in _blocks(message)
        if _is_tool_result_block(block)
    ]
    if keep_recent_tool_results > 0:
        protected.update(id(block) for _, block in results[-keep_recent_tool_results:])
    if protect_from is not None:
        protected.update(id(block) for index, block in results if index >= protect_from)
    return protected


def trim_history_to_token_budget(
    messages: list[Any],
    budget_tokens: int | None,
    *,
    marker: str = _DEFAULT_SUBSTITUTE,
    keep_recent_tool_results: int = 0,
    protect_from: int | None = None,
) -> HistoryBudgetReport:
    """Clear oldest tool results in place until the estimate fits ``budget_tokens``.

    THE NEWEST READINGS STAY (conversation bf84b149, 2026-11-13): a 12,000-token budget on a 134-call browser run
    cleared 40 results spanning call 1 to call 132 — the latest page and form state included — so the agent could
    not see what it had just read. The newest ``keep_recent_tool_results`` results (the host's knob) and every
    result of the turn in flight (``protect_from``: the index of the person message that opened it) are never
    cleared; the budget then stays unmet rather than blind the agent. Size inside one turn is the context trim's
    and the fit step's job, never the history window's."""
    before = estimate_history_tokens(messages)
    if not budget_tokens or budget_tokens <= 0 or before <= budget_tokens:
        return HistoryBudgetReport(int(budget_tokens or 0), before, before, 0)

    total_chars = before * _CHARS_PER_TOKEN
    limit_chars = budget_tokens * _CHARS_PER_TOKEN
    cleared = 0
    cleared_ids: list[str] = []
    calls = call_index(messages)
    protected = _protected_result_ids(
        messages, keep_recent_tool_results=max(0, int(keep_recent_tool_results or 0)), protect_from=protect_from
    )
    for message in messages:
        for block in _blocks(message):
            if total_chars <= limit_chars:
                break
            if not _is_tool_result_block(block) or _already_trimmed(block) or _is_media_bearing(block):
                continue
            if id(block) in protected:
                continue
            was = _block_chars(block)
            if not _rewrite_block_content(block, marker, refetch_for(block, calls)):
                continue  # the stub would not be smaller: clearing it would grow the history
            total_chars -= was - _block_chars(block)
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
    calls = call_index(messages)
    for message in messages:
        for block in _blocks(message):
            if not _is_tool_result_block(block) or _already_trimmed(block):
                continue
            if _tool_use_id(block) in tool_use_ids and _rewrite_block_content(
                block, marker, refetch_for(block, calls)
            ):
                cleared += 1
    return cleared


def _role(message: Any) -> str:
    if isinstance(message, dict):
        return str(message.get("role") or "")
    return str(getattr(message, "role", "") or "")


def current_turn_start(history: list[Any], tail: list[Any]) -> int | None:
    """Where the turn in flight opens in ``history``: ``None`` when the person message that opens it is in
    ``tail`` (a new turn — all of ``history`` is earlier turns), else the index of the last person message in
    ``history`` (a resumed run: a client tool round trip re-resolves mid-turn). A person message is a ``user`` row
    that is not only tool results."""

    def _is_person(message: Any) -> bool:
        role = message.get("role") if isinstance(message, dict) else getattr(message, "role", None)
        if str(getattr(role, "value", role) or "") != "user":
            return False
        blocks = _blocks(message)
        return not (blocks and all(_is_tool_result_block(b) for b in blocks))

    if any(_is_person(m) for m in tail):
        return None
    for index in range(len(history) - 1, -1, -1):
        if _is_person(history[index]):
            return index
    return None


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
    provider cache is already cold, so a warm conversation's prefix stays byte-identical (the cache law);
    ``keep_recent_tool_results`` — the newest this-many tool results are never cleared by the budget;
    ``turn_token_budget`` — then, while the history is still estimated over this many tokens, the oldest whole
    turns are left out (``cut_oldest_turns_to_budget``; ``None``/``<= 0`` = no turn cut)."""

    turns: int
    token_budget: int | None = None
    waits_for_cold_cache: bool = True
    keep_recent_tool_results: int = 0
    turn_token_budget: int | None = None


__all__ = [
    "HistoryBudgetReport",
    "HistoryWindowPolicy",
    "HistoryWindowUnavailable",
    "TurnCutReport",
    "clear_tool_results",
    "current_turn_start",
    "cut_oldest_turns_to_budget",
    "estimate_history_tokens",
    "estimate_sent_history_tokens",
    "last_turns",
    "trim_history_to_token_budget",
]
