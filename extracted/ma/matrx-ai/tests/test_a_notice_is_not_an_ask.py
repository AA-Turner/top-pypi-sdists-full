"""A NOTICE TO THE PERSON IS NOT AN ASK (second adversarial pass, 2026-11-14).

Adding the extension's ``user`` tool to ``PERSON_ASK_TOOLS`` made every ``user`` call an ask by NAME. But ``user``
also carries ``type: "notify"`` — "I finished, here is the summary" — which waits on nobody. By name alone:

* the orphan repair told a lost notice (the extension died before posting its result) "STILL WAITING: the person
  has not answered", with no error filed — a lie to the model and a hidden lost call;
* interim text treated a notify as parking the turn, so the note before it was never marked interim;
* the turn clock subtracted a notify's span from ``work_ms`` as if the person were answering.

The rule is decided by TYPE, once per language: ``tool_result_guard.is_person_ask_call`` here, tool-cards
``isPersonAskCall`` on the client (aidream ``test_person_ask_tools_agree.py`` proves both agree on sample calls).
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import message_config
from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tool_result_guard import PERSON_ASK_TOOLS, is_person_ask_call
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import TextContent
from matrx_ai.processing.blocks.interim_text import interim_flags

NOTIFY = {"type": "notify", "question": "All 5 DNS records are saved."}
NOTIFY_BATCH = {"questions": [{"type": "notify", "question": "Done."}, {"type": "notify", "question": "Bye."}]}
CHOICE = {"type": "choice", "question": "Which account?", "options": ["A", "B"]}
MIXED_BATCH = {"questions": [{"type": "notify", "question": "Saved."}, {"type": "confirm", "question": "Publish?"}]}


@pytest.mark.parametrize(
    ("name", "arguments", "asks"),
    [
        ("user", CHOICE, True),
        ("user", MIXED_BATCH, True),
        ("user", {}, True),
        ("user", NOTIFY, False),
        ("user", NOTIFY_BATCH, False),
        ("user", '{"type": "notify"}', False),
        ("ask_person", NOTIFY, True),  # only the extension's `user` tool carries notify
        ("read_page", NOTIFY, False),
        (None, None, False),
    ],
)
def test_the_predicate(name: str | None, arguments: Any, asks: bool) -> None:
    assert is_person_ask_call(name, arguments) is asks


def _turns(arguments: dict[str, Any]) -> MessageList:
    return MessageList(
        [
            UnifiedMessage(role=Role.USER, content=[TextContent(text="Add the DNS records.")]),
            UnifiedMessage(role=Role.ASSISTANT, content=[ToolCallContent(id="fc_1", name="user", arguments=arguments)]),
            UnifiedMessage(role=Role.USER, content=[TextContent(text="Did it work?")]),
        ]
    )


def _results(messages: MessageList) -> list[ToolResultContent]:
    return [c for m in messages for c in m.content if isinstance(c, ToolResultContent)]


@pytest.mark.parametrize("arguments", [NOTIFY, NOTIFY_BATCH])
def test_a_lost_notice_is_a_lost_call_not_an_open_question(monkeypatch: Any, arguments: dict[str, Any]) -> None:
    reported: list[Any] = []
    monkeypatch.setattr(message_config, "report_orphan_tool_uses_repaired", lambda **kw: reported.append(kw))
    messages = _turns(arguments)
    messages.sanitize()
    [result] = _results(messages)
    assert result.is_error is True
    assert "STILL WAITING" not in str(result.content)
    assert "TOOL NEVER ANSWERED [user]" in str(result.content)
    assert len(reported) == 1


def test_an_open_user_question_still_reads_still_waiting(monkeypatch: Any) -> None:
    reported: list[Any] = []
    monkeypatch.setattr(message_config, "report_orphan_tool_uses_repaired", lambda **kw: reported.append(kw))
    messages = _turns(CHOICE)
    messages.sanitize()
    [result] = _results(messages)
    assert result.is_error is False
    assert "STILL WAITING [user]" in str(result.content)
    assert reported == []


def _text(t: str) -> dict[str, Any]:
    return {"type": "text", "text": t}


def _call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return {"type": "tool_call", "call_id": "c1", "name": name, "arguments": arguments}


def test_text_before_a_notice_is_interim_and_before_a_question_is_not() -> None:
    assert interim_flags([_text("Saving the last record."), _call("user", NOTIFY)]) == [True, False]
    assert interim_flags([_text("Saving the last record."), _call("user", NOTIFY_BATCH)]) == [True, False]
    assert interim_flags([_text("I need one thing from you."), _call("user", CHOICE)]) == [False, False]


async def test_the_turn_clock_counts_a_notices_span_as_work(monkeypatch: Any) -> None:
    from matrx_ai.db import _cx_managers_impl as impl

    t = lambda s: datetime(2026, 11, 14, 12, 0, s, tzinfo=UTC)  # noqa: E731
    rows = [
        {"tool_name": "user", "arguments": CHOICE, "started_at": t(10), "completed_at": t(10), "resolved_at": t(40)},
        {"tool_name": "user", "arguments": NOTIFY, "started_at": t(45), "completed_at": t(50), "resolved_at": None},
    ]

    class _Query:
        def __init__(self, result: list[dict[str, Any]]) -> None:
            self._result = result

        async def values(self, *fields: str) -> list[dict[str, Any]]:
            return [{f: r.get(f) for f in fields} for r in self._result]

    monkeypatch.setattr(impl, "CxUserRequest", SimpleNamespace(filter=lambda **_: _Query([{"created_at": t(0)}])))
    monkeypatch.setattr(impl, "CxToolCall", SimpleNamespace(filter=lambda **_: _Query(rows)))
    sent, waits = await impl.CxUserRequestManager.turn_clock(
        SimpleNamespace(), "ur-1", person_ask_tools=PERSON_ASK_TOOLS
    )
    assert sent == t(0)
    assert waits == [(t(10), t(40))], "the question's wait comes off; the notice's span stays work"
