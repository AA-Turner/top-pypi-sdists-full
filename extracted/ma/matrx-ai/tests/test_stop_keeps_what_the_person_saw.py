"""Stop keeps what the person already watched stream (PB-05 W-47, 2026-10-01).

Preview re-check (conversation f9fa875a…, Compass Itinerary Clerk, Whitcombe
move): Stop was pressed with Stops 1–29 on screen. The provider call was
stopped mid-generation (`ProviderCallStopped`) and the run finalized with an
EMPTY response, so the database kept only Stops 1–20 — the nine stops the
coordinator had read were gone after the screen re-read the conversation.

Break this guards: the stopped call's streamed text is dropped (plain Stop), or
an INTERRUPT's abandoned partial is left visible to the person or the model.
The emitter's per-turn buffer is the dependency (what streamed); the request
control registry is real.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from matrx_connect.request_controls import RequestControlRegistry

from matrx_ai.orchestrator import executor

SEEN = (
    "Stop 21 — Baker City, OR: Fuel and crew swap at the Pilot on Campbell St.\n\n"
    "Stop 29 — Mountain Home, ID: Overnight at the Flying J; trailer locked."
)


def _ctx(streamed: str) -> SimpleNamespace:
    return SimpleNamespace(emitter=SimpleNamespace(get_turn_text=lambda: streamed))


def _texts(response) -> list[str]:
    return [c.text for m in response.messages for c in m.content if getattr(c, "text", None)]


def test_a_plain_stop_keeps_the_streamed_text_visible():
    response = executor._stopped_call_response(_ctx(SEEN), "whitcombe-stop-plain")
    assert _texts(response) == [SEEN]
    meta = response.messages[0].metadata or {}
    assert meta.get("is_visible_to_user", True) is True
    assert meta.get("is_visible_to_model", True) is True


@pytest.mark.asyncio
async def test_an_interrupt_keeps_the_partial_but_hides_it():
    request_id = "whitcombe-stop-interrupt"
    await RequestControlRegistry.get_instance().interrupt(request_id)
    response = executor._stopped_call_response(_ctx(SEEN), request_id)
    assert _texts(response) == [SEEN]
    meta = response.messages[0].metadata
    assert meta["is_visible_to_user"] is False
    assert meta["is_visible_to_model"] is False


def test_nothing_streamed_leaves_nothing_behind():
    assert executor._stopped_call_response(_ctx("   "), "whitcombe-stop-empty").messages == []
