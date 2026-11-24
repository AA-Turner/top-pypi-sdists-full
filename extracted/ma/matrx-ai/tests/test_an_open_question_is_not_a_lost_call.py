"""An open question is not a lost call (live error classes 2026-11-04, sec_05aa…).

Every ``orphan_tool_use_repaired`` row in the chat class named ``ask_person``: the agent asked the person, the person's
next message did not answer it, so the card stays open (aidream ``settle_answered_in_chat`` leaves it up by design) and
the next turn's history carried the ask with no result. The sanitizer answered it with "TOOL NEVER ANSWERED … it is NOT
known whether the action ran" and filed a red row. The model is now told the truth — still waiting — and nothing is
filed; a real orphan of any other tool is still repaired loudly.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.config import message_config
from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import TextContent


def _turns(tool: str) -> MessageList:
    return MessageList(
        [
            UnifiedMessage(role=Role.USER, content=[TextContent(text="Plan my week.")]),
            UnifiedMessage(role=Role.ASSISTANT, content=[ToolCallContent(id="fc_1", name=tool, arguments={"kind": "choose_one"})]),
            UnifiedMessage(role=Role.USER, content=[TextContent(text="Actually, what is on my calendar today?")]),
        ]
    )


def _results(messages: MessageList) -> list[ToolResultContent]:
    return [c for m in messages for c in m.content if isinstance(c, ToolResultContent)]


def test_an_open_question_reads_still_waiting_and_files_nothing(monkeypatch: Any) -> None:
    reported: list[Any] = []
    monkeypatch.setattr(message_config, "report_orphan_tool_uses_repaired", lambda **kw: reported.append(kw))
    messages = _turns("ask_person")
    messages.sanitize()
    [result] = _results(messages)
    assert result.tool_use_id == "fc_1"
    assert result.is_error is False
    assert "STILL WAITING [ask_person]" in str(result.content)
    assert result.metadata.get("reason") == "open_person_ask"
    assert reported == []


def test_a_lost_call_of_any_other_tool_is_still_repaired_loudly(monkeypatch: Any) -> None:
    reported: list[Any] = []
    monkeypatch.setattr(message_config, "report_orphan_tool_uses_repaired", lambda **kw: reported.append(kw))
    messages = _turns("records")
    messages.sanitize()
    [result] = _results(messages)
    assert result.is_error is True
    assert "TOOL NEVER ANSWERED [records]" in str(result.content)
    assert len(reported) == 1
