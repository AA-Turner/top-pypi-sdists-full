"""Feedback 017807f4: a provider built-in web search's "Searched the web" card showed while streaming
and vanished on reload. The answer row now stores display-only ``provider_tool_activity`` blocks and
one completed ``chat.tool_call`` row per built-in tool (through the real persist funnel), and the
DB-load funnel drops the block so it never reaches a provider."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from test_off_engine_calls_keep_history import funnel  # noqa: F401 — the real persist funnel

from matrx_ai.config import TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.config.builtin_tool_use import PROVIDER_TOOL_ACTIVITY, builtin_tool_activity
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.requests import AIMatrixRequest

BUILTIN = {"web_search": {"count": 1, "queries": ["harbor ferry schedule"], "sources_cited": 3}}


@pytest.mark.asyncio
async def test_the_answer_row_stores_the_card_and_a_linked_tool_call_row(funnel, monkeypatch):  # noqa: F811
    import matrx_ai.persistence.queue_helpers as qh
    from matrx_ai.agents.run_history import record_sent_call

    rows: list[dict] = []
    monkeypatch.setattr(qh, "queue_tool_call_create", lambda **kw: rows.append(kw) or kw["id"])

    answer = UnifiedMessage(role="assistant", content=[TextContent(text="The ferry leaves at 9.")])
    answer.metadata = {PROVIDER_TOOL_ACTIVITY: builtin_tool_activity(BUILTIN, call_key="abcd-1-1")}
    request = AIMatrixRequest(
        conversation_id="11111111-1111-1111-1111-111111111111",
        config=UnifiedConfig(
            model="probe-model",
            messages=[UnifiedMessage(role="user", content=[TextContent(text="When is the ferry?")])],
        ),
        request_id="33333333-3333-3333-3333-333333333333",
    )
    response = UnifiedResponse(
        messages=[answer],
        usage=TokenUsage(input_tokens=5, output_tokens=5, matrx_model_name="probe-model", api="anthropic"),
        finish_reason="stop",
    )
    assert await record_sent_call(request, source_feature="test.builtin", response=response) is not None

    stored = [m for m in funnel["message_create"] if m["role"] == "assistant"][0]
    types = [b["type"] for b in stored["content"]]
    assert types == ["provider_tool_activity", "text"], types
    block = stored["content"][0]
    assert block["call_id"] == "builtin-web_search-abcd-1-1"
    assert block["name"] == "provider_web_search"
    assert block["arguments"] == {"queries": ["harbor ferry schedule"]}
    assert PROVIDER_TOOL_ACTIVITY not in (stored.get("metadata") or {})

    assert len(rows) == 1, rows
    row = rows[0]
    assert row["message_id"] == stored["id"]
    assert row["call_id"] == block["call_id"]
    assert row["tool_name"] == "provider_web_search"
    assert row["status"] == "completed" and row["success"] is True


def _stored_answer():
    return SimpleNamespace(
        id="55555555-5555-5555-5555-555555555555",
        role="assistant",
        content=[
            {"type": "provider_tool_activity", "call_id": "builtin-web_search-x", "name": "provider_web_search",
             "arguments": {"queries": ["q"]}, "result": {"count": 1}},
            {"type": "text", "text": "Answer."},
        ],
        user_content=None,
        status="active",
        metadata={},
        position=1,
        created_at=None,
        agent_id=None,
        is_visible_to_model=True,
    )


def test_the_block_never_reaches_a_provider() -> None:
    message = UnifiedMessage.from_cx_message(_stored_answer())
    assert [type(c).__name__ for c in message.content] == ["TextContent"]
    assert message.content[0].text == "Answer."
    parsed = UnifiedMessage.parse_content(_stored_answer().content)
    assert [type(c).__name__ for c in parsed] == ["TextContent"]
