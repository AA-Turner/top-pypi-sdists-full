"""Remark handles (THREADS S1/R1): every remark gets a stable id and a
conversation-wide handle (c1, c2 …) the model can cite; handles never repeat,
survive a resend, are never taken from the client, and a failed comment_reply
is told to the model in the next remarks text.

Use case: Harbor Dental's front-desk manager remarks on the agent's intake and
reminder replies across several turns.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

import matrx_ai.config.remark_handles as remark_handles
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.remarks import REMARKS_PART_TYPE
from matrx_ai.config.structured_input_config import RemarksInputContent
from matrx_ai.config.structured_input_resolver import resolve_structured_inputs
from matrx_ai.config.unified_content import TextContent, reconstruct_content


def _reply(mid: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role="assistant", id=mid, content=[TextContent(text=text)])


def _turn(*items: dict) -> UnifiedMessage:
    return UnifiedMessage.from_dict(
        {"role": "user", "content": [{"type": REMARKS_PART_TYPE, "items": [dict(i) for i in items]}]}
    )


def _stored(turn: UnifiedMessage) -> UnifiedMessage:
    """The message as a later turn loads it back from storage."""
    block = next(c for c in turn.content if isinstance(c, RemarksInputContent))
    return UnifiedMessage(role="user", content=[reconstruct_content(block.to_storage_dict())])


def _send(history: list[UnifiedMessage], turn: UnifiedMessage) -> list[dict[str, Any]]:
    asyncio.run(resolve_structured_inputs(MessageList([*history, turn])))
    block = next(c for c in turn.content if isinstance(c, RemarksInputContent))
    return block.to_storage_dict()["items"]


def _comment(mid: str, body: str, **extra: Any) -> dict[str, Any]:
    return {"kind": "comment", "target": {"message_id": mid}, "body": body, **extra}


def test_handles_continue_across_turns_and_every_item_gets_an_id() -> None:
    history = [UnifiedMessage(role="user", content=[TextContent(text="Draft intake.")]), _reply("a-1", "Form.")]
    first = _turn(_comment("a-1", "Add insurance."), _comment("a-1", "Add photo ID.", id="fe-2"))
    items = _send(history, first)
    assert [i["handle"] for i in items] == ["c1", "c2"]
    assert items[0]["id"] and items[1]["id"] == "fe-2"

    history = [*history, _stored(first), _reply("a-2", "Updated.")]
    second = _turn(_comment("a-2", "Looks right."))
    assert [i["handle"] for i in _send(history, second)] == ["c3"]


def test_a_resend_keeps_its_handle_and_a_client_handle_is_never_trusted() -> None:
    history = [UnifiedMessage(role="user", content=[TextContent(text="Hi")]), _reply("a-1", "Hello.")]
    first = _turn(_comment("a-1", "Too formal.", id="fe-1"))
    _send(history, first)
    history = [*history, _stored(first), _reply("a-2", "Better?")]
    # The same remark (same id) sent again keeps c1; a new one claiming c1 is re-minted.
    again = _turn(_comment("a-1", "Too formal.", id="fe-1"), _comment("a-2", "Yes.", id="fe-9", handle="c1"))
    assert [i["handle"] for i in _send(history, again)] == ["c1", "c2"]


def test_the_marker_names_the_handle_and_is_frozen_with_it() -> None:
    history = [UnifiedMessage(role="user", content=[TextContent(text="Hi")]), _reply("a-1", "Hello.")]
    turn = _turn(_comment("a-1", "Too formal."))
    _send(history, turn)
    block = next(c for c in turn.content if isinstance(c, RemarksInputContent))
    assert block.metadata["resolved_text"].startswith("<!-- comment c1 on your previous reply -->")
    stored = reconstruct_content(block.to_storage_dict())
    assert stored.items[0]["handle"] == "c1" and stored.metadata["resolved_text"] == block.metadata["resolved_text"]




def test_numbers_continue_above_every_stored_handle_even_ones_not_loaded(monkeypatch) -> None:
    """R1: a trimmed/hidden earlier message still owns its handles."""
    async def stored(conversation_id):
        assert conversation_id == "conv-1"
        return 41

    monkeypatch.setattr(remark_handles, "stored_handle_floor", stored)
    items = [{"kind": "comment", "body": "a"}, {"kind": "comment", "body": "b"}]
    asyncio.run(remark_handles.assign_remark_handles([], items, "conv-1"))
    assert [i["handle"] for i in items] == ["c42", "c43"]


def test_a_failed_reply_is_told_to_the_model_in_the_next_remarks_text(monkeypatch) -> None:
    async def drain(conversation_id):
        return [{"to": "c9", "reason": "there is no remark c9 in this conversation"}]

    monkeypatch.setattr(remark_handles, "drain_reply_failures", drain)
    history = [UnifiedMessage(role="user", content=[TextContent(text="Hi")]), _reply("a-1", "Hello.")]
    turn = _turn(_comment("a-1", "Shorter please."))
    _send(history, turn)
    text = next(c for c in turn.content if isinstance(c, RemarksInputContent)).metadata["resolved_text"]
    assert text.endswith("<!-- your reply to c9 failed: there is no remark c9 in this conversation -->")


@pytest.mark.parametrize("handle", ["c0", "x3", "c1234567", "C3"])
def test_a_malformed_handle_is_refused(handle: str) -> None:
    from pydantic import ValidationError

    from matrx_ai.config.remarks import RemarkItem

    with pytest.raises(ValidationError):
        RemarkItem.model_validate({"kind": "comment", "body": "x", "handle": handle})


def test_a_continued_thread_reads_as_quoted_lines_under_the_marker() -> None:
    history = [UnifiedMessage(role="user", content=[TextContent(text="Hi")]), _reply("a-1", "Hello.")]
    turn = _turn({"kind": "comment", "id": "cmt-root-1", "comment_id": "cmt-root-1",
                  "target": {"message_id": "a-1"}, "body": "Is 2h enough?",
                  "thread": [{"author_name": "Dana Ruiz", "author_kind": "person", "body": "Is 2h enough?",
                              "created_at": "2026-10-03T10:00:00Z"},
                             {"author_name": "Front Desk Helper", "author_kind": "agent", "body": "Most clinics use 24h."}]})
    items = _send(history, turn)
    assert items[0]["thread"][1]["author_kind"] == "agent"
    text = next(c for c in turn.content if isinstance(c, RemarksInputContent)).metadata["resolved_text"]
    assert "> Dana Ruiz: Is 2h enough?\n> Front Desk Helper (agent): Most clinics use 24h." in text
