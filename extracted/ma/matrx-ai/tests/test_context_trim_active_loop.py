from datetime import UTC, datetime

from matrx_ai.config import ToolResultContent, UnifiedMessage
from matrx_ai.config.context_trim import trim_messages_context


def _tool_result(chars: int, *, position: int | None = None) -> UnifiedMessage:
    return UnifiedMessage(
        role="tool",
        position=position,
        content=[
            ToolResultContent(
                tool_use_id=f"call-{position}-{chars}",
                name="large_tool",
                content="x" * chars,
                output_chars=chars,
            )
        ],
    )


def test_trims_old_unpersisted_tool_results_during_active_loop() -> None:
    # 15 loop turns; tier 1 (12 positions back) reaches the first three.
    messages = [_tool_result(20_000) for _ in range(15)]

    report = trim_messages_context(messages)

    assert report.blocks_rewritten == 3
    assert report.freed_chars > 50_000
    assert messages[0].position is None
    assert "tool result cleared" in str(messages[0].content[0].content)
    assert "tool result cleared" not in str(messages[-1].content[0].content)


def test_orders_unpersisted_turns_after_persisted_history() -> None:
    messages = [_tool_result(20_000, position=10)]
    messages.extend(_tool_result(20_000) for _ in range(14))

    report = trim_messages_context(messages)

    assert report.blocks_rewritten == 3
    assert report.rewritten_blocks[0]["message_position"] == 10
    assert messages[-1].position is None


def test_default_policy_is_the_2026_09_09_ruling() -> None:
    """Arman ruled the tiers from re-fetch measurements (chat.vw_tool_refetch).
    Changing these numbers is a ruling, not a refactor — update this test only
    with a new ruling recorded in the ai-models / execution-runtime docs."""
    from matrx_ai.config.context_trim import TrimPolicy

    p = TrimPolicy()
    assert (p.tier_1_min_positions_back, p.tier_1_min_output_chars) == (12, 8000)
    assert (p.tier_2_min_positions_back, p.tier_2_min_output_chars) == (24, 2000)


def test_recent_large_result_survives() -> None:
    """A 7K doc page read two tool calls ago must still be readable — the
    exact case that made the 2026-09-08 Google sync re-read a page 3 times."""
    messages = [_tool_result(7_000) for _ in range(6)]
    report = trim_messages_context(messages)
    assert report.blocks_rewritten == 0


# --------------------------------------------------------------------------- #
# THE ASSISTANT SIDE — stale tool_call ARGUMENTS (2026-09-13)                  #
#                                                                              #
# Measured in chat.request / chat.message: the Masterwork Conductor saves      #
# workflow definitions through workflow_author with 25-73K-char argument       #
# payloads that live in assistant messages forever. One conversation reached   #
# 1.5M chars of assistant content against 19K of tool results; average request #
# context 362K tokens, peak 559K, $95 on Opus 5. 408 of 419 Conductor requests #
# reported the trimmer ran and freed nothing because nothing eligible existed  #
# on the RESULT side.                                                          #
# --------------------------------------------------------------------------- #

import json

from matrx_ai.config import ToolCallContent
from matrx_ai.config.context_trim import TrimPolicy


def _tool_call(chars: int, *, position: int | None = None, call_id: str = "call-big") -> UnifiedMessage:
    return UnifiedMessage(
        role="assistant",
        position=position,
        content=[
            ToolCallContent(
                id=call_id,
                name="workflow_author",
                arguments={"definition": "y" * chars, "action": "save"},
            )
        ],
    )


def test_stale_large_tool_call_arguments_are_rewritten() -> None:
    messages = [_tool_call(40_000, call_id="call-stale")]
    messages.extend(_tool_result(100) for _ in range(30))

    report = trim_messages_context(messages)

    block = messages[0].content[0]
    assert report.blocks_rewritten == 1
    assert report.arguments_rewritten == 1
    assert report.freed_chars > 39_000
    assert report.rewritten_blocks[0]["block"] == "tool_call"
    assert report.rewritten_blocks[0]["call_id"] == "call-stale"
    assert report.rewritten_blocks[0]["tool_name"] == "workflow_author"

    # Identity is untouched — provider tool_use <-> tool_result pairing survives.
    assert block.id == "call-stale"
    assert block.name == "workflow_author"
    assert block.type == "tool_call"

    # The stub is a plain dict naming what was there, and serialises as a JSON
    # object for every provider (Anthropic input, OpenAI arguments, Google args).
    assert isinstance(block.arguments, dict)
    assert block.arguments["keys"] == ["definition", "action"]
    assert block.arguments["chars"] > 39_000
    assert "[tool arguments cleared]" in block.arguments["result"]
    assert isinstance(json.loads(json.dumps(block.arguments)), dict)
    assert isinstance(block.to_anthropic()["input"], dict)
    assert json.loads(block.to_openai()["arguments"])["keys"] == ["definition", "action"]
    assert isinstance(block.to_google()["functionCall"]["args"], dict)

    # Result blocks were below threshold and must be untouched.
    assert messages[5].content[0].content == "x" * 100


def test_fresh_large_tool_call_arguments_survive() -> None:
    """A workflow the assistant just saved is still readable in context."""
    messages = [_tool_call(40_000)]
    messages.extend(_tool_result(100) for _ in range(5))

    report = trim_messages_context(messages)

    assert report.blocks_rewritten == 0
    assert report.arguments_rewritten == 0
    assert len(messages[0].content[0].arguments["definition"]) == 40_000


def test_argument_trim_is_idempotent() -> None:
    messages = [_tool_call(40_000)]
    messages.extend(_tool_result(100) for _ in range(30))

    first = trim_messages_context(messages)
    stub = dict(messages[0].content[0].arguments)
    second = trim_messages_context(messages)

    assert first.arguments_rewritten == 1
    assert second.blocks_rewritten == 0
    assert second.arguments_rewritten == 0
    assert second.freed_chars == 0
    assert messages[0].content[0].arguments == stub


def test_cache_gate_counts_argument_savings() -> None:
    """The gate used to see 0 savings on a call-heavy conversation and protect
    a cache that was costing $95 to keep. Argument bytes now count."""
    fresh_cache = {
        "last_response_at": datetime.now(UTC).isoformat(),
        "last_provider": "anthropic",
        "est_cache_ttl_secs": 300,
    }

    results_only = [_tool_result(2_500) for _ in range(30)]
    protected = trim_messages_context(results_only, cache_state=fresh_cache)
    assert protected.blocks_rewritten == 0
    assert protected.eligible_but_skipped_reason == "cache_protect"
    assert protected.policy["cache_gate"]["est_savings_tokens"] < 5000

    with_arguments = [_tool_call(40_000)]
    with_arguments.extend(_tool_result(2_500) for _ in range(29))
    trimmed = trim_messages_context(with_arguments, cache_state=fresh_cache)
    assert trimmed.eligible_but_skipped_reason is None
    assert trimmed.arguments_rewritten == 1
    assert trimmed.freed_chars > 39_000


def test_trim_tool_call_arguments_false_restores_old_behaviour() -> None:
    messages = [_tool_call(40_000)]
    messages.extend(_tool_result(100) for _ in range(30))

    report = trim_messages_context(messages, policy=TrimPolicy(trim_tool_call_arguments=False))

    assert report.blocks_rewritten == 0
    assert report.arguments_rewritten == 0
    assert len(messages[0].content[0].arguments["definition"]) == 40_000
