"""A failed tool call must persist its error text, not just an error FLAG.

2026-09-12: a nested agent build failed and the persisted ``chat.message``
carried ``{"type": "tool_result", "is_error": true, "output_chars": 0}`` —
a red error block with zero bytes of explanation in it. The message existed
the whole time on ``ToolResult.error``; nothing downstream read it, because
the persisted block copies ONLY ``output_chars`` and ``output_preview``, and
both are computed from ``output``, which a raised tool leaves as None.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolError, ToolResult


def _failed_result() -> ToolResult:
    return ToolResult(
        success=False,
        output=None,
        error=ToolError(
            error_type="RuntimeError",
            message="operation stream journal persistence failed",
            suggested_action="Send your message again.",
        ),
        call_id="toolu_01incident",
        tool_name="build_agent",
    )


def test_prepare_metadata_stamps_the_error_message() -> None:
    """The one synchronous funnel must carry the error into persisted fields."""
    result = _failed_result()
    ToolExecutionLogger().prepare_metadata(result)

    assert result.output_chars > 0, (
        "output_chars 0 beside is_error true is the defect: the row claims an "
        "error and holds nothing that explains it"
    )
    assert result.output_preview is not None
    assert "operation stream journal persistence failed" in str(
        result.output_preview.get("error")
    )
    assert result.output_preview.get("error_type") == "RuntimeError"
    assert "Send your message again." in str(result.output_preview.get("suggested_action"))


def test_successful_result_metadata_is_unchanged() -> None:
    """The error stamp must not touch the success path."""
    result = ToolResult(
        success=True,
        output={"agent_id": "abc"},
        call_id="toolu_ok",
        tool_name="build_agent",
    )
    ToolExecutionLogger().prepare_metadata(result)
    assert result.output_chars > 0
    assert "error" not in (result.output_preview or {})


@pytest.mark.asyncio
async def test_persisted_tool_result_block_carries_the_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """End of the real chain: prepare_metadata -> content -> persisted block."""
    from matrx_ai.db import persistence
    from matrx_ai.tools import handle_tool_calls

    result = _failed_result()
    tool_logger = ToolExecutionLogger()
    tool_logger.prepare_metadata(result)
    content_item = result.to_tool_result_content()

    class _FakeExecutor:
        execution_logger = tool_logger

    monkeypatch.setattr(handle_tool_calls, "get_executor", lambda: _FakeExecutor())

    async def _noop_backfill(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr(tool_logger, "backfill_message_id", _noop_backfill)

    blocks = await persistence._backfill_tool_message(
        {"content": [content_item]},
        "55555555-5555-4555-8555-555555555555",
        "66666666-6666-4666-8666-666666666666",
    )

    assert len(blocks) == 1
    block = blocks[0]
    assert block["is_error"] is True
    assert block["output_chars"] > 0
    assert "operation stream journal persistence failed" in str(
        block["output_preview"]["error"]
    )
