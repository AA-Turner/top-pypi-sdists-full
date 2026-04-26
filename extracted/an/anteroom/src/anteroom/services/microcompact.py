"""Proactive microcompact stage (#1266).

Pure, synchronous, in-memory history trimming that runs every turn in
the agent loop before the LLM call. Complements the existing per-tool
compaction at ``services/tool_result_compact.py`` (which only touches
each tool result at ingestion) and the reactive overflow ladder (#1415)
by proactively sweeping the full conversation history.

Microcompact never writes to SQLite, never makes an LLM call, and never
reorders messages. The trade-off: trims are not durable across session
resume. Documented in ``docs/cli/context-management.md``.

Single source of truth — the :data:`STRATEGIES` registry is also used by
reactive Strategy 1 (``services.agent_loop._truncate_large_tool_outputs``)
so the same trim behaviour is exercised whether microcompact fires
proactively or reactively. See ``test_strategy_1_and_microcompact_agree``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable

from .compaction import collapse_old_tool_results_details

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MicroCompactResult:
    """Outcome of a microcompact pass.

    ``success`` is True when at least one strategy reported a change.
    ``strategies_applied`` lists the strategy names that actually
    mutated ``messages`` (empty when no-op). ``bytes_saved`` is an
    advisory count of bytes freed across all applied strategies; exact
    accounting is strategy-specific.
    """

    success: bool
    strategies_applied: list[str] = field(default_factory=list)
    bytes_saved: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StrategyOutcome:
    """Strategy-level result normalized by :func:`microcompact`."""

    success: bool
    bytes_saved: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


def _strategy_oversized_tool_outputs(
    messages: list[dict[str, Any]],
    *,
    tool_output_max_chars: int,
    **_: Any,
) -> int:
    """Trim tool result messages whose content exceeds ``tool_output_max_chars``.

    Replaces content with the truncated head plus a retry hint that tells
    the LLM to re-issue the tool call with more constrained parameters.
    Returns the number of bytes saved across all trimmed messages (0 when
    no message needed trimming).

    Preserves turn-group atomicity — content is replaced in place; no
    message is dropped or reordered. This is the shared implementation
    used by both proactive microcompact and reactive Strategy 1.
    """
    bytes_saved = 0
    tool_call_names: dict[str, str] = {}

    for msg in messages:
        for tc in msg.get("tool_calls", []):
            tc_id = tc.get("id", "")
            func = tc.get("function", {})
            if tc_id and func.get("name"):
                tool_call_names[tc_id] = func["name"]

    for msg in messages:
        if msg.get("role") != "tool":
            continue
        content = msg.get("content", "")
        if len(content) <= tool_output_max_chars:
            continue

        tc_id = msg.get("tool_call_id", "")
        tool_name = tool_call_names.get(tc_id, "unknown tool")
        original_len = len(content)
        new_content = (
            content[:tool_output_max_chars]
            + f"\n\n... [TRUNCATED — original output was {original_len:,} chars from '{tool_name}'. "
            f"The output exceeded the context window. "
            f"You MUST retry this tool call with more constrained parameters "
            f"(e.g. fewer results, a narrower query, or a smaller limit) "
            f"to get output that fits within the context window.]"
        )
        # Skip mutation when the trimmed form would be larger than the
        # original — e.g. a 101-byte message where the retry hint alone
        # is longer. Trimming only makes sense when it's a net reduction.
        if len(new_content) >= original_len:
            continue
        msg["content"] = new_content
        bytes_saved += original_len - len(new_content)
        logger.info(
            "microcompact trimmed tool output for %s (call %s): %d -> %d chars",
            tool_name,
            tc_id,
            original_len,
            len(new_content),
        )

    return bytes_saved


def _strategy_historical_tool_results(
    messages: list[dict[str, Any]],
    *,
    historical_tool_collapse_enabled: bool = False,
    historical_tool_collapse_force: bool = False,
    estimated_tokens: int | None = None,
    historical_tool_collapse_trigger_token_count: int = 90_000,
    historical_tool_collapse_keep_recent_groups: int = 6,
    historical_tool_collapse_compact_chars: int = 1_000,
    **_: Any,
) -> StrategyOutcome:
    """Collapse older tool results when token pressure is high.

    The default is a no-op so registering this strategy does not make small
    conversations mutate on every turn. The shared agent loop passes the
    current token estimate and config thresholds when pressure is reached.
    Tests may opt in directly with ``historical_tool_collapse_force=True``.
    """
    if not historical_tool_collapse_enabled and not historical_tool_collapse_force:
        return StrategyOutcome(success=False)

    pressure_hit = (
        historical_tool_collapse_force
        or historical_tool_collapse_trigger_token_count <= 0
        or (estimated_tokens is not None and estimated_tokens >= historical_tool_collapse_trigger_token_count)
    )
    if not pressure_hit:
        return StrategyOutcome(
            success=False,
            metadata={
                "estimated_tokens": estimated_tokens,
                "trigger_token_count": historical_tool_collapse_trigger_token_count,
            },
        )

    result = collapse_old_tool_results_details(
        messages,
        keep_recent_groups=historical_tool_collapse_keep_recent_groups,
        compact_chars=historical_tool_collapse_compact_chars,
    )
    return StrategyOutcome(
        success=result.success,
        bytes_saved=result.bytes_saved,
        metadata={
            "modified_count": result.modified_count,
            "bytes_saved": result.bytes_saved,
            "keep_recent_groups": result.keep_recent_groups,
            "compact_chars": result.compact_chars,
            "estimated_tokens": estimated_tokens,
            "trigger_token_count": historical_tool_collapse_trigger_token_count,
        },
    )


# Strategy registry. Keys are stable string names surfaced in
# ``MicroCompactResult.strategies_applied`` and in the ``strategies``
# filter kwarg of :func:`microcompact`. New strategies plug in by
# adding an entry here.
_Strategy = Callable[..., int | StrategyOutcome]

STRATEGIES: dict[str, _Strategy] = {
    "oversized_tool_outputs": _strategy_oversized_tool_outputs,
    "historical_tool_results": _strategy_historical_tool_results,
}


def _normalize_outcome(raw: int | StrategyOutcome) -> StrategyOutcome:
    if isinstance(raw, StrategyOutcome):
        return raw
    return StrategyOutcome(success=raw > 0, bytes_saved=max(0, raw))


def microcompact(
    messages: list[dict[str, Any]],
    *,
    tool_output_max_chars: int,
    min_messages: int = 4,
    strategies: list[str] | None = None,
    **strategy_kwargs: Any,
) -> MicroCompactResult:
    """Run deterministic, in-memory trimming strategies on ``messages``.

    ``strategies`` selects which strategy names to run (from
    :data:`STRATEGIES`). When omitted, every registered strategy runs.

    Skips all work — returning ``success=False`` with empty
    ``strategies_applied`` — when ``len(messages) < min_messages``. This
    is a safety floor matching ``COMPACTION_MIN_MESSAGES`` so microcompact
    never fires on nearly-empty histories.

    Mutates ``messages`` in place. Never writes to SQLite. Never calls an
    LLM. Never reorders. Strategy-level failures do not raise — they log
    and skip.
    """
    if len(messages) < min_messages:
        return MicroCompactResult(success=False, strategies_applied=[], bytes_saved=0)

    selected: list[str] = list(STRATEGIES.keys()) if strategies is None else list(strategies)
    applied: list[str] = []
    total_saved = 0
    metadata: dict[str, Any] = {}

    for name in selected:
        fn = STRATEGIES.get(name)
        if fn is None:
            logger.warning("microcompact: unknown strategy %r — skipping", name)
            continue
        try:
            raw_outcome = fn(
                messages,
                tool_output_max_chars=tool_output_max_chars,
                **strategy_kwargs,
            )
            outcome = _normalize_outcome(raw_outcome)
        except Exception:
            logger.exception("microcompact strategy %r failed — leaving messages untouched", name)
            continue
        if outcome.metadata:
            metadata[name] = outcome.metadata
        if outcome.success:
            applied.append(name)
            total_saved += outcome.bytes_saved

    return MicroCompactResult(
        success=bool(applied),
        strategies_applied=applied,
        bytes_saved=total_saved,
        metadata=metadata,
    )
