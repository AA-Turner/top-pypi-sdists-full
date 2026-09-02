from __future__ import annotations

import pytest
from matrx_connect.streaming import error_capture

from matrx_ai.config.tool_result_guard import (
    LAYER_SANITIZE,
    NONADJACENT_TOOL_USE_ERROR_KIND,
    capture_nonadjacent_tool_uses,
)
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.db._conversation_rebuild_impl import _relocate_separated_tool_results


@pytest.mark.asyncio
async def test_nonadjacent_guard_creates_structured_system_error(monkeypatch) -> None:
    captured: list[tuple[BaseException, dict[str, object]]] = []

    async def fake_sink(exc: BaseException, **fields: object) -> None:
        captured.append((exc, fields))

    monkeypatch.setattr(error_capture, "_capture_fn", fake_sink)
    monkeypatch.setattr(error_capture, "_allow_in_tests", True)

    await capture_nonadjacent_tool_uses(
        layer=LAYER_SANITIZE,
        dropped=[
            {"tool_use_id": "sensitive-call-id", "name": "user", "reason": "separated"}
        ],
        context={
            "request_id": "request-id",
            "user_id": "user-id",
            "conversation_id": "conversation-id",
            "route": "/v2/ai/conversations/conversation-id",
        },
    )

    assert len(captured) == 1
    exc, fields = captured[0]
    assert fields["kind"] == NONADJACENT_TOOL_USE_ERROR_KIND
    assert fields["error_type"] == "NonadjacentToolResult"
    assert fields["request_id"] == "request-id"
    assert fields["conversation_id"] == "conversation-id"
    assert fields["context"] == {
        "layer": LAYER_SANITIZE,
        "dropped_count": 1,
        "separated_count": 1,
    }
    assert "sensitive-call-id" not in str(exc)
    assert "user" not in str(exc)


def test_rebuild_relocates_a_late_result_before_intervening_assistant() -> None:
    messages = [
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="call-a", name="user", arguments={})],
        ),
        UnifiedMessage(role="assistant", content=[TextContent(text="later turn")]),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="call-a", content="answer")],
        ),
    ]

    repaired = _relocate_separated_tool_results(messages)

    assert [getattr(m.role, "value", m.role) for m in repaired] == [
        "assistant",
        "tool",
        "assistant",
    ]
    assert repaired[1].content[0].tool_use_id == "call-a"
