"""A provider request never reaches ``chat.request_snapshot`` as ``{}``.

Defect (2026-10-21 → 10-22): ``send_boundary.order_for_wire`` (typed-text-last
reorder) began making a wire clone on sends with NO wire swaps. ``send_once``
redacts the captured payload whenever a wire clone exists, and
``redact_wire_payload`` returned ``None`` when there was nothing to redact
against — so every reordered send (Anthropic / Google / Groq / OpenAI / xAI /
Together turns carrying a platform block) stored ``request_payload = {}``:
1,187 of 1,200 ``before_typed_text`` rows on 2026-10-22.

This drives the real ``send_once`` with a wire clone and no swaps, the provider
capturing its payload through the real ``capture_request_payload`` seam, and
asserts the captured payload survives. Red on the pre-fix code, green after.
"""

from __future__ import annotations

import asyncio
from copy import copy
from types import SimpleNamespace

from matrx_ai.config.picklist_runtime import clear_wire_swaps, set_wire_swaps
from matrx_ai.config.send_boundary import SendPrep
from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
)
from matrx_ai.providers.snapshot import capture_request_payload

WIRE = {
    "model": "claude-haiku",
    "messages": [
        {"role": "user", "content": "platform block"},
        {"role": "user", "content": "what the person typed"},
    ],
}


class _Client:
    async def execute(self, request):
        capture_request_payload(dict(WIRE), provider="anthropic")
        return SimpleNamespace(ok=True)


def _run(monkeypatch, *, swaps: dict[str, str]) -> object:
    import matrx_ai.config.send_boundary as sb

    canonical = SimpleNamespace(model="claude-haiku", messages=[])

    async def _prep(config, **_kw):
        # What order_for_wire does on a reordered turn: a shallow wire copy.
        return SendPrep(stage=sb.STAGE_LOOP, wire_config=copy(config))

    monkeypatch.setattr(sb, "prepare_for_send", _prep)
    from matrx_ai.orchestrator.send_once import send_once

    request = SimpleNamespace(config=canonical, conversation_id=None, request_id=None)
    state = ExecutionState()
    token = set_execution_state(state)
    set_wire_swaps(swaps)
    try:
        asyncio.run(send_once(_Client(), request, state=state, iteration=1))
    finally:
        clear_wire_swaps()
        clear_execution_state(token)
    assert request.config is canonical  # the wire clone never outlives the call
    return state.snapshot_payload


def test_wire_clone_without_swaps_keeps_the_captured_payload(monkeypatch):
    payload = _run(monkeypatch, swaps={})
    assert payload, "a reordered send with no wire swaps stored an empty request_payload"
    assert payload["messages"][-1]["content"] == "what the person typed"


def test_wire_clone_with_swaps_still_redacts(monkeypatch):
    secret = "a referenced value long enough to swap"
    WIRE["messages"][0]["content"] = f"block {secret}"
    try:
        payload = _run(monkeypatch, swaps={"[[ref:1]]": secret})
    finally:
        WIRE["messages"][0]["content"] = "platform block"
    assert payload, "redaction dropped a payload it could redact"
    assert secret not in str(payload)
    assert "[[ref:1]]" in str(payload)
