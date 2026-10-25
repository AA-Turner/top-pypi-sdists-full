"""A running parent takes EVERY waiting report at its final boundary in ONE round.

Arman, 2026-10-25: "if there are multiple, we don't wake the agent up over and over
again." ``claim_next_turn_end`` used to take ONE ``turn_end`` row per extra model round, so
three helper reports cost three extra paid rounds. Host notes now come all at once; a
person's own queued message stays one per turn (the three-send-modes ruling).

Also: a caller that holds the conversation's organization passes it, and the door uses it
as given (no second read) — the database refuses a foreign one and fills none.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import _cx_managers_impl as cx


def _row(kind: str, seq: int, *, status: str = "pending", source: str = "deferred_tool") -> SimpleNamespace:
    return SimpleNamespace(
        id=str(uuid4()), kind=kind, status=status, enqueued_seq=seq, source=source, metadata={}
    )


def _patch(monkeypatch: pytest.MonkeyPatch, rows: list[SimpleNamespace]) -> None:
    async def filter_items(self, **where):
        return [r for r in rows if all(str(getattr(r, k)) == str(v) for k, v in where.items() if k != "conversation_id" and k != "delivery")]

    async def update_where(self, where, **sets):
        hit = [r for r in rows if all(str(getattr(r, k)) == str(v) for k, v in where.items())]
        for r in hit:
            for k, v in sets.items():
                setattr(r, k, v)
        return SimpleNamespace(updated_rows=hit, rows_affected=len(hit))

    monkeypatch.setattr(cx.CxPendingInjectionManager, "filter_items", filter_items)
    monkeypatch.setattr(cx.CxPendingInjectionManager, "update_where", update_where)


@pytest.mark.asyncio
async def test_three_reports_are_taken_in_one_round(monkeypatch):
    rows = [_row("system_message", 1), _row("system_message", 2, status="failed"), _row("system_message", 3)]
    _patch(monkeypatch, rows)
    claimed = await cx.cx_pending_injection_manager_instance.claim_next_turn_end("c", request_id="r")
    assert sorted(r.enqueued_seq for r in claimed) == [1, 2, 3]
    assert all(r.status == "consumed" for r in rows)


@pytest.mark.asyncio
async def test_a_persons_queued_message_is_still_one_per_turn(monkeypatch):
    rows = [_row("user_message", 1, source="queue"), _row("user_message", 2, source="queue"), _row("system_message", 3)]
    _patch(monkeypatch, rows)
    claimed = await cx.cx_pending_injection_manager_instance.claim_next_turn_end("c", request_id="r")
    assert [r.enqueued_seq for r in claimed] == [1]
    # The next round takes the next person's message, and the report behind it only after.
    claimed = await cx.cx_pending_injection_manager_instance.claim_next_turn_end("c", request_id="r")
    assert [r.enqueued_seq for r in claimed] == [2]


@pytest.mark.asyncio
async def test_reports_ahead_of_a_persons_message_ride_together_and_leave_it_queued(monkeypatch):
    rows = [_row("system_message", 1), _row("user_message", 2, source="queue"), _row("system_message", 3)]
    _patch(monkeypatch, rows)
    claimed = await cx.cx_pending_injection_manager_instance.claim_next_turn_end("c", request_id="r")
    assert sorted(r.enqueued_seq for r in claimed) == [1, 3]
    assert rows[1].status == "pending"


@pytest.mark.asyncio
async def test_a_caller_named_organization_is_written_as_given(monkeypatch):
    class _NoRead:
        @classmethod
        def filter(cls, **_kw):
            raise AssertionError("the conversation is not read again when the caller named the organization")

    captured: dict = {}

    async def fake_create_item(self, **kwargs):
        captured.update(kwargs)
        return SimpleNamespace(id=kwargs["id"])

    monkeypatch.setattr(cx, "CxConversation", _NoRead)
    monkeypatch.setattr(cx.CxPendingInjectionManager, "create_item", fake_create_item)
    org = str(uuid4())
    await cx.cx_pending_injection_manager_instance.enqueue(
        injection_id=str(uuid4()),
        conversation_id=str(uuid4()),
        organization_id=org,
        created_by="u",
        kind="system_message",
        content={"text": "hi"},
        source="scheduled_wake",
        is_visible_to_user=True,
        is_visible_to_model=True,
    )
    assert captured["organization_id"] == org
