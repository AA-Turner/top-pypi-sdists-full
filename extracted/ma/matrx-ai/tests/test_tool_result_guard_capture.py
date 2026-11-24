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
            "route": "/ai/conversations/conversation-id",
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
        "dropped": [{"tool_use_id": "sensitive-call-id", "name": "user", "reason": "separated"}],
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


def test_a_result_before_its_call_is_named_with_both_positions(monkeypatch) -> None:
    """Feedback 7e1c088c: personal-staff turns lost a call with separated=0 and no id or
    position, so the writer that split the pair could not be found."""
    from matrx_ai.config import message_config
    from matrx_ai.config.message_config import MessageList

    seen: list[list[dict]] = []
    monkeypatch.setattr(
        message_config, "report_nonadjacent_tool_uses", lambda *, layer, dropped: seen.append(dropped)
    )
    ml = MessageList(
        [
            UnifiedMessage(role="user", content=[TextContent(text="hi")], id="m-user"),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id="call-b", content="early")],
                id="m-result",
            ),
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="call-b", name="github", arguments={})],
                id="m-call",
            ),
            UnifiedMessage(role="user", content=[TextContent(text="next")], id="m-next"),
        ]
    )
    ml.sanitize()

    assert len(seen) == 1
    (drop,) = seen[0]
    assert drop["tool_use_id"] == "call-b" and drop["name"] == "github"
    assert drop["reason"] == "result_before_call"
    assert drop["use_message_id"] == "m-call"
    assert drop["result_message_ids"] == ["m-result"]
    assert drop["result_indexes"] < [drop["use_index"]]


def _sms_history_with_result_before_call() -> list[UnifiedMessage]:
    """The live shape of class sec_08238d: the staff_roster result row sits two places
    BEFORE its call, so every SMS turn re-filed the same pair as a new error."""
    return [
        UnifiedMessage(role="user", content=[TextContent(text="who is on today")], id="m-user"),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="call-r", content="roster")],
            id="m-result",
        ),
        UnifiedMessage(role="assistant", content=[TextContent(text="checking")], id="m-text"),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="call-r", name="staff_roster", arguments={})],
            id="m-call",
        ),
        UnifiedMessage(role="assistant", content=[TextContent(text="Ana and Ben")], id="m-answer"),
        UnifiedMessage(role="user", content=[TextContent(text="next turn")], id="m-next"),
    ]


def test_rebuild_heals_a_result_stored_before_its_call_so_the_guard_never_refiles(monkeypatch) -> None:
    from matrx_ai.config import message_config
    from matrx_ai.config.message_config import MessageList

    seen: list[list[dict]] = []
    monkeypatch.setattr(
        message_config, "report_nonadjacent_tool_uses", lambda *, layer, dropped: seen.append(dropped)
    )
    repaired = _relocate_separated_tool_results(_sms_history_with_result_before_call())

    call_at = next(i for i, m in enumerate(repaired) if getattr(m, "id", None) == "m-call")
    assert repaired[call_at + 1].content[0].tool_use_id == "call-r"
    assert all(getattr(m, "id", None) != "m-result" for m in repaired)  # emptied projection dropped

    ml = MessageList(repaired)
    ml.sanitize()
    assert seen == []
    kept = [c for m in ml._messages for c in m.content]
    assert any(isinstance(c, ToolCallContent) and c.id == "call-r" for c in kept)
    assert any(isinstance(c, ToolResultContent) and c.tool_use_id == "call-r" for c in kept)


def test_rebuild_never_steals_an_earlier_same_id_calls_result() -> None:
    """Provider ids are not globally unique: a result an earlier same-id call owns stays put."""
    messages = [
        UnifiedMessage(
            role="assistant", content=[ToolCallContent(id="dup", name="t", arguments={})], id="a1"
        ),
        UnifiedMessage(
            role="tool", content=[ToolResultContent(tool_use_id="dup", content="x")], id="t1"
        ),
        UnifiedMessage(
            role="assistant", content=[ToolCallContent(id="dup", name="t", arguments={})], id="a2"
        ),
    ]
    repaired = _relocate_separated_tool_results(messages)
    assert [getattr(m, "id", None) for m in repaired] == ["a1", "t1", "a2"]
