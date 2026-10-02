"""A run that persists nothing never takes a message out of the person's inbox.

Found by the PB-05 "nothing lost" real test (2026-10-01, conversation
9004fe9b-165c-4b72-a488-34cfd38a013d, ledger W-40): a moving coordinator asked
the Compass Itinerary Clerk for a 40-stop itinerary and, while it was still
"Initializing", queued "Once the itinerary is done: what do we need for the
Okafor piano?". The row was marked ``consumed`` 60 ms after the run started,
by the run's own request id, yet no user row and no answer exist.

The consumer was the conversation labeler (``conversation.label_agent_run``):
``run_held_call`` nests a one-turn, ``store=False`` execution inside the chat
request's AppContext, so it inherits the conversation id. Its final boundary
ran the self-drain with ``include_turn_end=True``, claimed the queued row,
appended it to ITS throwaway config, hit ``max_iterations=1`` and returned —
the person's words vanished with a call that never persists anything.

The break this guards: ``drain_pending_injections`` claiming inbox rows for a
run whose ``store`` is False.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext

from matrx_ai.db import cxm
from matrx_ai.tools import dynamic_drain

CONVERSATION = "9004fe9b-165c-4b72-a488-34cfd38a013d"
REQUEST = "096bc62e-962c-4722-9943-a6b749fe4cdf"
QUEUED_TEXT = "Once the itinerary is done: what do we need for the Okafor piano?"


class _Emitter:
    def __init__(self) -> None:
        self.consumed: list[Any] = []

    async def send_injection_consumed(self, payload: Any) -> None:
        self.consumed.append(payload)


def _queued_row() -> Any:
    return SimpleNamespace(
        id="5f659d07-b382-4a9b-be25-993e66c13b00",
        kind="user_message",
        content={"text": QUEUED_TEXT},
        is_visible_to_user=True,
        enqueued_seq=1,
        metadata={},
    )


def _claim_spy(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """The inbox table is the external dependency; record every claim."""
    claims: list[str] = []
    row = _queued_row()

    async def claim_pending(conversation_id: str, *, request_id: str | None = None):
        claims.append("next_boundary")
        return []

    async def claim_next_turn_end(conversation_id: str, *, request_id: str | None = None):
        claims.append("turn_end")
        return [row]

    monkeypatch.setattr(cxm.pending_injection, "claim_pending", claim_pending)
    monkeypatch.setattr(cxm.pending_injection, "claim_next_turn_end", claim_next_turn_end)
    return claims


def _chat_request_ctx(emitter: _Emitter) -> AppContext:
    return AppContext(
        emitter=emitter,
        user_id="11111111-1111-4111-8111-111111111111",
        organization_id="2c1d4319-bf0d-40bc-8ca1-657f4063d080",
        conversation_id=CONVERSATION,
        request_id=REQUEST,
        store=True,
    )


@pytest.mark.asyncio
async def test_a_held_call_inside_a_chat_request_leaves_the_queued_message_pending(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    claims = _claim_spy(monkeypatch)
    emitter = _Emitter()
    # Exactly the derivation run_held_call performs (matrx_ai/mandates.py).
    held_ctx = _chat_request_ctx(emitter).with_overrides(store=False)
    config = SimpleNamespace(messages=[])

    await dynamic_drain.drain_pending_injections(config, held_ctx, include_turn_end=True)

    assert claims == [], f"a store=False run claimed inbox rows: {claims}"
    assert config.messages == []
    assert emitter.consumed == []


@pytest.mark.asyncio
async def test_the_persisting_chat_run_delivers_the_queued_message_at_its_final_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    claims = _claim_spy(monkeypatch)
    emitter = _Emitter()
    config = SimpleNamespace(messages=[])

    await dynamic_drain.drain_pending_injections(
        config, _chat_request_ctx(emitter), include_turn_end=True
    )

    assert claims == ["next_boundary", "turn_end"]
    assert [m.content[0].text for m in config.messages] == [QUEUED_TEXT]
    assert emitter.consumed and emitter.consumed[0].items[0].text == QUEUED_TEXT
