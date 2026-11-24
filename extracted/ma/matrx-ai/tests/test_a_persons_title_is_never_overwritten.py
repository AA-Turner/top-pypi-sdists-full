"""P-032: a person's own conversation title is never overwritten by the auto-titler.

Live (2026-11-02): rename a chat "G3A rename check", send a second message, wait ~15 s, and the
title became "Ping-Pong Test". The executor schedules labeling on turn 2 as well as turn 1
(``len(messages) > 3`` lets [user, assistant, user] through), and the inline attempt only guarded a
rename made WHILE it ran — its "title before" was read after the rename, so the rename was its
baseline. The one answer to "did the person name it" is now ``chat.conversation.named_by``
(kept by the DB trigger ``chat._named_by``); every automatic title write declares itself
(``named_by='auto_write'``) so the database keeps a person's title even across a race.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.agents.services.conversation_labeler as labeler
from matrx_ai import _ext
from matrx_ai.agent_runners.conversation_labeler import LabelResult

CID = "0c1f3a52-7d2e-4b8a-9f61-3e5d2c7b9a10"
OUTPUT = '{"label": "Ping-Pong Test", "description": "Echo test", "keywords": ["ping"]}'
TURN_TWO = [
    {"role": "user", "content": "Reply with exactly the word: pong"},
    {"role": "assistant", "content": "pong"},
    {"role": "user", "content": "Now reply with exactly: ping"},
]


class _Rows:
    def __init__(self, row: Any) -> None:
        self.row = row

    def filter(self, **_kw: Any) -> _Rows:
        return self

    def limit(self, _n: int) -> _Rows:
        return self

    async def all(self) -> list[Any]:
        return [self.row]


@pytest.fixture
def run(monkeypatch: pytest.MonkeyPatch) -> dict[str, list[Any]]:
    seen: dict[str, list[Any]] = {"writes": [], "labels": []}

    async def update(_cid: str, _uid: str, fields: dict[str, Any]) -> None:
        seen["writes"].append(fields)

    async def titles(_uid: str) -> list[dict[str, str]]:
        return []

    async def label(**_kw: Any) -> LabelResult:
        seen["labels"].append(1)
        return LabelResult(success=True, output=OUTPUT)

    async def not_staff(_cid: str) -> bool:
        return False

    async def no_seed(**_kw: Any) -> None:
        return None

    monkeypatch.setattr(labeler, "_update_conversation_labels", update)
    monkeypatch.setattr(labeler, "_fetch_recent_titles", titles)
    monkeypatch.setattr(labeler, "label_chat_conversation", label)
    monkeypatch.setattr(labeler, "_is_staff_channel_conversation", not_staff)
    monkeypatch.setitem(_ext._registry, "system_process_seed", no_seed)
    return seen


def _row(**fields: Any) -> Any:
    base = {"title": "New conversation", "description": "", "keywords": [], "named_by": "auto",
            "organization_id": "org-1", "deleted_at": None, "metadata": {}}
    base.update(fields)
    return SimpleNamespace(**base)


async def test_turn_two_never_retitles_a_renamed_chat(monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]) -> None:
    # The live P-032 row: labeled on turn 1, then renamed by the person, then a second message.
    renamed = _row(title="G3A rename check", description="Echo test", keywords=["pong"], named_by="person")
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(renamed))))
    await labeler._run_labeling(CID, "user-1", TURN_TWO)
    assert run["writes"] == [], "the person's title was overwritten on a later turn"
    assert run["labels"] == []


async def test_turn_two_never_relabels_a_labeled_chat(monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]) -> None:
    labeled = _row(title="Pong Exact Word Output", description="Echo test", keywords=["pong"])
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(labeled))))
    await labeler._run_labeling(CID, "user-1", TURN_TWO)
    assert run["writes"] == [] and run["labels"] == []


async def test_a_person_named_title_survives_even_when_no_label_landed(
    monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]
) -> None:
    # Turn 1's label failed; the person named the chat; the labeler may still fill description and
    # keywords, never the title.
    named = _row(title="My own name", named_by="person")
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(named))))
    outcome, _parsed = await labeler._label_and_apply(
        conversation_id=CID, user_id="user-1", conversation_content="User: hi", agent_name=None,
        agent_description=None, user_variables=None, user_prompt=None,
    )
    assert outcome == "succeeded"
    assert run["writes"] == [{"description": "Echo test", "keywords": ["ping"]}]


async def test_the_retry_leaves_a_person_named_title_alone(monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]) -> None:
    named = _row(title="New conversation", named_by="person")
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(named))))
    outcome = await labeler.run_label_retry(
        {"conversation_id": CID, "user_id": "user-1", "conversation_content": "x", "title_before": "New conversation"}
    )
    assert outcome == "skipped:already_labeled"
    assert run["writes"] == []


async def test_every_automatic_title_write_declares_itself(monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]) -> None:
    fresh = _row()
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(fresh))))
    await labeler._run_labeling(CID, "user-1", TURN_TWO[:1])
    assert run["writes"] == [
        {"title": "Ping-Pong Test", "description": "Echo test", "keywords": ["ping"], "named_by": "auto_write"}
    ]


# ── MJ1 (CGU-M3 L2-title): clearing a title hands it back, and the platform takes it back ─────────────

TURN_THREE = [*TURN_TWO, {"role": "assistant", "content": "ping"}, {"role": "user", "content": "And once more: pong"}]


async def test_a_cleared_title_is_named_again_on_a_later_turn(monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]) -> None:
    # Live: labeled on turn 1, renamed, then cleared (title NULL, named_by auto); description and keywords stay.
    cleared = _row(title=None, description="Echo test", keywords=["pong"], named_by="auto")
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(cleared))))
    await labeler._run_labeling(CID, "user-1", TURN_THREE, retitle_only=True)
    assert run["labels"] == [1], "a cleared title was never named again"
    assert run["writes"] and run["writes"][0]["title"] == "Ping-Pong Test"
    assert run["writes"][0]["named_by"] == "auto_write"


async def test_a_later_turn_costs_no_model_call_when_the_chat_has_a_title(
    monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]
) -> None:
    for row in (
        _row(title="Pong Exact Word Output", description="Echo test", keywords=["pong"]),
        _row(title="My own name", named_by="person"),
        _row(title=None, named_by="person"),  # never stored (the trigger refuses a blank claim), but never relabeled
    ):
        monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(row))))
        await labeler._run_labeling(CID, "user-1", TURN_THREE, retitle_only=True)
    assert run["labels"] == [] and run["writes"] == []


async def test_the_retry_names_a_cleared_title(monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]) -> None:
    cleared = _row(title=None, description="Echo test", keywords=["pong"])
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(cleared))))
    outcome = await labeler.run_label_retry(
        {"conversation_id": CID, "user_id": "user-1", "conversation_content": "x", "title_before": ""}
    )
    assert outcome == "succeeded"
    assert run["writes"][0]["title"] == "Ping-Pong Test"


def test_the_executor_asks_for_a_retitle_on_a_continued_turn(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.orchestrator import executor

    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(labeler, "schedule_conversation_labeling", lambda **kw: calls.append(kw))
    import matrx_ai.client_host as client_host

    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    ctx = SimpleNamespace(store=object(), system_run=False, conversation_id=CID, user_id="user-1",
                          parent_conversation_id=None, metadata={}, initial_variables=None,
                          conversation_type="standard", is_internal_agent=False)
    monkeypatch.setattr("matrx_ai.agents.conversation_type.is_internal_conversation", lambda _ctx: False)
    executor._schedule_labeling_if_new(ctx, SimpleNamespace(messages=TURN_THREE))
    assert len(calls) == 1 and calls[0].get("retitle_only") is True
    calls.clear()
    executor._schedule_labeling_if_new(ctx, SimpleNamespace(messages=TURN_TWO[:1]))
    assert len(calls) == 1 and not calls[0].get("retitle_only")


def test_a_host_turn_never_names_the_chat_and_its_line_is_never_read(monkeypatch: pytest.MonkeyPatch) -> None:
    """Review 7: a Discovery chat titled itself "Discovery Kickoff Conversation" from the host's opening line. A turn
    the host started is not labeled; the person's first own turn is, and the host line is not part of what is read."""
    from matrx_ai.config.message_config import (
        MessageList,
        TextContent,
        UnifiedMessage,
        host_authored_user_turn,
    )
    from matrx_ai.orchestrator import executor

    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(labeler, "schedule_conversation_labeling", lambda **kw: calls.append(kw))
    import matrx_ai.client_host as client_host

    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    monkeypatch.setattr("matrx_ai.agents.conversation_type.is_internal_conversation", lambda _ctx: False)
    ctx = SimpleNamespace(store=object(), system_run=False, conversation_id=CID, user_id="user-1",
                          parent_conversation_id=None, metadata={"agent_name": "Advisor"}, initial_variables=None)
    opening = host_authored_user_turn("Discovery is on. Open with your quick questions.", reason="understanding")
    executor._schedule_labeling_if_new(ctx, SimpleNamespace(messages=MessageList([opening])))
    assert calls == [], "the host's opening line named the chat"
    turn_two = MessageList([
        opening, UnifiedMessage(role="assistant", content=[TextContent(text="A few quick questions.")]),
        UnifiedMessage(role="user", content=[TextContent(text="How do I price my lawn care plans?")]),
    ])
    executor._schedule_labeling_if_new(ctx, SimpleNamespace(messages=turn_two))
    assert len(calls) == 1 and not calls[0].get("retitle_only")
    read = repr(calls[0]["messages"])
    assert "Discovery is on" not in read and "lawn care" in read
    assert calls[0]["user_prompt"] == "How do I price my lawn care plans?"


async def test_a_placeholder_title_left_by_a_host_turn_is_named_on_a_later_turn(
    monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]
) -> None:
    """Review 8 (M-3): the host's Discovery opening is never labeled, so the chat kept the conversation gate's
    "Auto: <agent>" placeholder; every later turn is a retitle-only turn, which named only a BLANK title — so the chat
    was never named. A placeholder nobody labeled is no title: the first later turn names it. Once a label landed
    (description/keywords), a placeholder is left alone without a model call."""
    placeholder = _row(title="Auto: Review8 Small Business Growth Advisor")
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(placeholder))))
    await labeler._run_labeling(CID, "user-1", TURN_THREE, retitle_only=True)
    assert run["labels"] == [1], "the placeholder title was never replaced"
    assert run["writes"][0]["title"] == "Ping-Pong Test"
    labeled = _row(title="Auto: Advisor", description="Echo test", keywords=["pong"])
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(labeled))))
    await labeler._run_labeling(CID, "user-1", TURN_THREE, retitle_only=True)
    assert run["labels"] == [1]


def test_a_host_started_chat_is_named_from_the_persons_card_answers(monkeypatch: pytest.MonkeyPatch) -> None:
    """Review 9 (M-A): a Discovery chat kept "Auto: <agent>" for its whole 7-minute Discovery stretch — the person's
    card answers (resumed into the host-started turn) are their first real words, yet only a typed message named the
    chat. The answers name it now (retitle_only: a real title is never replaced); the host line is never read, and a
    host turn with no answers still names nothing."""
    import json

    from matrx_ai.config.message_config import MessageList, UnifiedMessage, host_authored_user_turn
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
    from matrx_ai.orchestrator import executor

    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(labeler, "schedule_conversation_labeling", lambda **kw: calls.append(kw))
    import matrx_ai.client_host as client_host

    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    monkeypatch.setattr("matrx_ai.agents.conversation_type.is_internal_conversation", lambda _ctx: False)
    ctx = SimpleNamespace(store=object(), system_run=False, conversation_id=CID, user_id="user-1",
                          parent_conversation_id=None, metadata={"agent_name": "Advisor"}, initial_variables=None)
    opening = host_authored_user_turn("Discovery is on. Open with your quick questions.", reason="understanding")
    ask = UnifiedMessage(role="assistant", content=[ToolCallContent(id="toolu_9", name="ask_person", arguments={
        "kind": "questions", "message": "A few quick questions.", "payload": {"questions": [
            {"id": "understanding.subject", "type": "text", "question": "What's your business called?"},
            {"id": "understanding.industry", "type": "text", "question": "What industry is it in?"},
            {"id": "understanding.team_size", "type": "choice", "question": "How many people work there?"},
        ]}})])
    answered = UnifiedMessage(role="tool", content=[ToolResultContent(
        tool_use_id="toolu_9", name="ask_person", content=[{"type": "text", "text": json.dumps({
            "ask_record": "action_request.outcome", "status": "answered", "kind": "questions",
            "result": {"answers": [{"answer": "Pinecrest Plumbing"}, {"answer": "Residential plumbing in Boise"},
                                   {"selected": ["Other"], "freeform": "Six of us"}]}})}])])
    executor._schedule_labeling_if_new(ctx, SimpleNamespace(messages=MessageList([opening, ask])))
    assert calls == [], "a host turn with no answer yet named the chat"
    executor._schedule_labeling_if_new(ctx, SimpleNamespace(messages=MessageList([opening, ask, answered])))
    assert len(calls) == 1 and calls[0]["retitle_only"] is True
    read = repr(calls[0]["messages"])
    assert "Pinecrest Plumbing" in read and "Residential plumbing in Boise" in read
    assert "Discovery is on" not in read
    assert calls[0]["user_prompt"].startswith("What's your business called?: Pinecrest Plumbing")
    # review 11 (I5): the person's typed words, never the card's own "Other" label
    assert "How many people work there?: Six of us" in calls[0]["user_prompt"]
    assert ": Other" not in calls[0]["user_prompt"]


async def test_a_failed_naming_call_is_tried_again_at_once(
    monkeypatch: pytest.MonkeyPatch, run: dict[str, list[Any]]
) -> None:
    """Review 15 (M7), chat c3821dca replayed: the person's card answer resumed the Discovery turn and the namer
    fired, but the provider rejected its first answer ("Parsing failed. The model generated output that could not
    be parsed"). The inline attempt gave up and left the name to the durable retry, due minutes later (which hit
    the same flake once more), so the chat read "Auto: <agent>" for eight minutes. One flaky reply is tried again
    at once; the durable retry is for a process that died, not for a single bad reply."""
    placeholder = _row(title="Auto: Review15 Small Shop Advisor")
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=_Rows(placeholder))))
    replies = [
        LabelResult(success=False, output="", error="AI turn ended with status 'failed' (invalid_request): Groq "
                    "rejected the request: Parsing failed. The model generated output that could not be parsed."),
        LabelResult(success=True, output='{"label": "Harbor Kayak Rentals", "description": "d", "keywords": ["k"]}'),
    ]

    async def flaky(**_kw: Any) -> LabelResult:
        run["labels"].append(1)
        return replies.pop(0)

    monkeypatch.setattr(labeler, "label_chat_conversation", flaky)
    answered = [{"role": "user", "content": "What is the name of the business you want to talk about?: Harbor Kayak Rentals"}]
    await labeler._run_labeling(CID, "user-1", answered, retitle_only=True)
    assert run["labels"] == [1, 1], "one flaky reply left the placeholder to a retry due minutes later"
    assert run["writes"] and run["writes"][0]["title"] == "Harbor Kayak Rentals"
