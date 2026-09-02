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
    messages = [_tool_result(20_000) for _ in range(7)]

    report = trim_messages_context(messages)

    assert report.blocks_rewritten == 2
    assert report.freed_chars > 30_000
    assert messages[0].position is None
    assert "tool result cleared" in str(messages[0].content[0].content)
    assert "tool result cleared" not in str(messages[-1].content[0].content)


def test_orders_unpersisted_turns_after_persisted_history() -> None:
    messages = [_tool_result(20_000, position=10)]
    messages.extend(_tool_result(20_000) for _ in range(6))

    report = trim_messages_context(messages)

    assert report.blocks_rewritten == 2
    assert report.rewritten_blocks[0]["message_position"] == 10
    assert messages[-1].position is None
