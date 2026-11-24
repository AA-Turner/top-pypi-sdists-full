"""A QUEUED MESSAGE NAMES THE QUEUE ITEM IT CAME FROM (2026-11-05, conversation 6c9efe35…).

A Company Setup chat showed the person's "Yes, put it live for our clients." twice. The second row was a real
second send — the browser queued it into the running turn 1.5 s after an ``ask_person`` answer — but the stored
message carried ``metadata = {}`` and the queue row (``chat.pending_injection``) kept no link to the message it
became, so it read as the server writing one message twice and cost an investigation to tell apart. Every message
the Turn-Boundary Inbox delivers now carries the queue item's id and the request that queued it, so a stored row
always says where it came from. A person's queued words stay hers: no host-authorship key is added.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext

from matrx_ai.db import cxm
from matrx_ai.tools import dynamic_drain

CONVERSATION = "6c9efe35-3dc7-48bd-8331-690f7ce9fd08"
QUEUED_BY = "61acc925-0000-4000-8000-000000000001"


class _Emitter:
    async def send_injection_consumed(self, payload: Any) -> None:
        return None


def _row(row_id: str, kind: str, source: str, text: str, seq: int) -> SimpleNamespace:
    return SimpleNamespace(
        id=row_id,
        kind=kind,
        source=source,
        content={"text": text},
        is_visible_to_user=True,
        enqueued_seq=seq,
        metadata={"enqueued_by_request_id": QUEUED_BY},
    )


@pytest.mark.asyncio
async def test_every_delivered_queue_item_names_its_source(monkeypatch) -> None:
    person = _row("133efafa-ab44-46b4-bf35-ae02d8a2d023", "user_message", "user", "Yes, put it live for our clients.", 1)
    note = _row("5f659d07-b382-4a9b-be25-993e66c13b00", "system_message", "scheduled_wake", "[Scheduled wake] Check.", 2)

    async def claim_pending(_cid: str, *, request_id: str | None = None):
        return []

    async def claim_reports_now(_cid: str, *, request_id: str | None = None):
        return []

    async def claim_next_turn_end(_cid: str, *, request_id: str | None = None):
        return [person, note]

    monkeypatch.setattr(cxm.pending_injection, "claim_pending", claim_pending)
    monkeypatch.setattr(cxm.pending_injection, "claim_reports_now", claim_reports_now)
    monkeypatch.setattr(cxm.pending_injection, "claim_next_turn_end", claim_next_turn_end)
    ctx = AppContext(
        emitter=_Emitter(),
        user_id="11111111-1111-4111-8111-111111111111",
        organization_id="884d1ce8-7b49-4fba-a2f3-0f7dd7c83d4f",
        conversation_id=CONVERSATION,
        request_id="7a8f78b7-58e2-4fa7-9c30-955f5ff48342",
        store=True,
    )
    config = SimpleNamespace(messages=[])

    await dynamic_drain.drain_pending_injections(config, ctx, include_turn_end=True)

    delivered_person, delivered_note = config.messages
    for message, row in ((delivered_person, person), (delivered_note, note)):
        assert message.metadata.get("injection_id") == row.id, "a delivered queue item lost its queue id"
        assert message.metadata.get("enqueued_by_request_id") == QUEUED_BY, "it lost the request that queued it"
    # The person's own words are still hers — the trace adds no host-authorship key.
    assert "authored_by" not in delivered_person.metadata
    assert "injection_source" not in delivered_person.metadata
