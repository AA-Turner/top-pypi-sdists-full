"""A host note the model reads is never hidden from the owning person (owner ruling 2026-10-23).

Scheduled wakes, deferred-tool and background-run results, steers and write-backs reach the run as
user-role turns. Until 2026-10-23 an injection row marked ``is_visible_to_user=false`` was stamped
hidden on the durable message, so the person never saw what the model was told. Now the delivered
turn is visible and flagged as the host's with ONE shared key — ``metadata.authored_by = "host"``
(plus ``authored_reason`` and ``injection_source``) — so the chat labels it.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext

from matrx_ai.config.message_config import HOST_AUTHORED_BY
from matrx_ai.db import cxm
from matrx_ai.tools import dynamic_drain

CONVERSATION = "9004fe9b-165c-4b72-a488-34cfd38a013d"


class _Emitter:
    def __init__(self) -> None:
        self.consumed: list[Any] = []

    async def send_injection_consumed(self, payload: Any) -> None:
        self.consumed.append(payload)


@pytest.mark.asyncio
async def test_a_hidden_flagged_wake_note_is_delivered_visible_and_host_authored(monkeypatch) -> None:
    row = SimpleNamespace(
        id="5f659d07-b382-4a9b-be25-993e66c13b00",
        kind="system_message",
        source="scheduled_wake",
        content={"text": "[Scheduled wake] Check the deploy."},
        is_visible_to_user=False,
        enqueued_seq=1,
        metadata={},
    )

    async def claim_pending(_cid: str, *, request_id: str | None = None):
        return []

    async def claim_next_turn_end(_cid: str, *, request_id: str | None = None):
        return [row]

    monkeypatch.setattr(cxm.pending_injection, "claim_pending", claim_pending)
    monkeypatch.setattr(cxm.pending_injection, "claim_next_turn_end", claim_next_turn_end)
    emitter = _Emitter()
    ctx = AppContext(
        emitter=emitter,
        user_id="11111111-1111-4111-8111-111111111111",
        organization_id="2c1d4319-bf0d-40bc-8ca1-657f4063d080",
        conversation_id=CONVERSATION,
        request_id="096bc62e-962c-4722-9943-a6b749fe4cdf",
        store=True,
    )
    config = SimpleNamespace(messages=[])

    await dynamic_drain.drain_pending_injections(config, ctx, include_turn_end=True)

    [delivered] = config.messages
    assert delivered.role == "user"
    assert "is_visible_to_user" not in delivered.metadata, "the durable turn must not be hidden"
    assert delivered.metadata["authored_by"] == HOST_AUTHORED_BY == "host"
    assert delivered.metadata["authored_reason"] == "injection:system_message"
    assert delivered.metadata["injection_source"] == "scheduled_wake"
    assert delivered.user_content == [], "the person said nothing here"
    assert emitter.consumed[0].items[0].is_visible_to_user is True
