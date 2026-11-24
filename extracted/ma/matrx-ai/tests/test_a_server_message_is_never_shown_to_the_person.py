"""A SERVER MESSAGE IS NEVER SHOWN AS A MESSAGE (Arman, 2026-11-01, superseding the 2026-10-23 ruling).

His words: "when you send a server message, mark it as 'visible to user' false so it doesn't show up in the ui". A
run-end wake once landed in a customer's chat as a "Sent by system" bubble holding a huge token twice, the agent's
instructions and raw report JSON. Every user-role turn the server writes (``host_authored_user_turn``, ``HostTurn``,
a drained system note) and every non-person row on the shared send path (``pending_injection.enqueue``) is stored
with ``is_visible_to_user = false`` — the model still reads it; the chat's reads (``is_visible_to_user = true``) never
list it. Only the person's own queued words stay visible.
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
async def test_a_wake_note_is_delivered_hidden_and_host_authored(monkeypatch) -> None:
    row = SimpleNamespace(
        id="5f659d07-b382-4a9b-be25-993e66c13b00",
        kind="system_message",
        source="scheduled_wake",
        content={"text": "[Scheduled wake] Check the deploy."},
        is_visible_to_user=True,  # a caller that says "visible" is overruled
        enqueued_seq=1,
        metadata={},
    )

    async def claim_pending(_cid: str, *, request_id: str | None = None):
        return []

    async def claim_next_turn_end(_cid: str, *, request_id: str | None = None):
        return [row]

    monkeypatch.setattr(cxm.pending_injection, "claim_pending", claim_pending)
    monkeypatch.setattr(cxm.pending_injection, "claim_next_turn_end", claim_next_turn_end)
    async def _no_reports(_cid, *, request_id=None):
        return []

    monkeypatch.setattr(cxm.pending_injection, "claim_reports_now", _no_reports)
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
    assert delivered.metadata["is_visible_to_user"] is False, "a server message was stored visible to the person"
    assert delivered.metadata["authored_by"] == HOST_AUTHORED_BY == "host"
    assert delivered.metadata["authored_reason"] == "injection:system_message"
    assert delivered.metadata["injection_source"] == "scheduled_wake"
    assert delivered.user_content == [], "the person said nothing here"
    assert emitter.consumed[0].items[0].is_visible_to_user is False


def test_every_host_written_turn_is_hidden_even_when_a_caller_says_otherwise() -> None:
    from matrx_ai.config.host_turn import HostTurn
    from matrx_ai.config.message_config import host_authored_user_turn

    assert host_authored_user_turn("[Background run x] ended.", reason="inbox_driver").metadata["is_visible_to_user"] is False
    turn = HostTurn(text="[Background run x] ended.", reason="inbox_driver", metadata={"is_visible_to_user": True})
    assert turn.to_message().metadata["is_visible_to_user"] is False
    # a question asked OF the person (the Debrief fork) is theirs to read, so it stays shown
    asked = HostTurn(text="What went well?", reason="agent_debrief", metadata={"visible_to_person": True})
    assert asked.to_message().metadata["is_visible_to_user"] is True


@pytest.mark.asyncio
async def test_the_shared_send_path_stores_every_server_row_hidden(monkeypatch) -> None:
    from matrx_ai.db._cx_managers_impl import CxPendingInjectionManager

    written: list[dict[str, Any]] = []

    async def create_item(self, **fields):
        written.append(fields)
        return fields

    monkeypatch.setattr(CxPendingInjectionManager, "create_item", create_item)
    manager = CxPendingInjectionManager.__new__(CxPendingInjectionManager)
    common = {"conversation_id": CONVERSATION, "created_by": "u", "content": {"text": "x"}, "source": "background_run",
              "is_visible_to_model": True, "organization_id": "2c1d4319-bf0d-40bc-8ca1-657f4063d080"}
    await manager.enqueue(injection_id="a", kind="system_message", is_visible_to_user=True, **common)
    await manager.enqueue(injection_id="b", kind="user_message", is_visible_to_user=True, **common)
    assert [w["is_visible_to_user"] for w in written] == [False, True]  # only the person's own words show
