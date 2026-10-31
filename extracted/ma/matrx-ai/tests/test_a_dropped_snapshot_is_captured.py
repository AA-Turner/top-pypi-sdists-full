"""A dropped request snapshot is CAPTURED, never silent — adversarial 2026-10-30 B9.

``redact_wire_payload`` fails closed (a value that cannot be swapped back safely drops the whole
snapshot). RED before: it returned None with nothing recorded — the next empty-snapshot regression
would arrive as a report, not a captured error. Now each drop goes to ``matrx_utils.capture_error``
(kind ``request_snapshot_dropped``) with the reason and the value's length, never the value.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_ai.config.picklist_runtime import redact_wire_payload, set_wire_swaps


@pytest.fixture
def captured(monkeypatch):
    out: list[dict] = []

    async def capture_error(exc, *, kind, **fields):
        out.append({"exc": exc, "kind": kind, **fields})

    monkeypatch.setattr("matrx_utils.capture_error", capture_error)
    return out


@pytest.mark.asyncio
async def test_a_short_value_on_the_wire_drops_the_snapshot_and_says_so(captured) -> None:
    set_wire_swaps({"⟦pick:answer⟧": "yes"})
    try:
        assert redact_wire_payload({"messages": [{"content": "yes, I will"}]}) is None
        for _ in range(3):
            await asyncio.sleep(0)
    finally:
        set_wire_swaps({})
    assert [c["kind"] for c in captured] == ["request_snapshot_dropped"]
    context = captured[0]["context"]
    assert context["value_chars"] == 3
    assert "yes" not in repr(context), "the captured record must never carry the value"


@pytest.mark.asyncio
async def test_a_kept_snapshot_captures_nothing(captured) -> None:
    set_wire_swaps({})
    assert redact_wire_payload({"system": "plain"}) == {"system": "plain"}
    await asyncio.sleep(0)
    assert captured == []
