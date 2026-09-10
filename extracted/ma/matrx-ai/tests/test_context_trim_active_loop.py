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
