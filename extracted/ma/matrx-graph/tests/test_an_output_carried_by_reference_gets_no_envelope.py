"""A step output the ``node_completed`` frame carries BY REFERENCE gets no ``__ir`` envelope, and is never fingerprinted.

The envelope's ``root.value`` is wire-elided and rehydrated from the frame's ``output`` (Studio
``inbound-envelope.ts``). Over ``workflow.event_payload.inline_value_max_bytes`` that ``output`` holds
reference markers (``event_payload_row``), so the envelope would label markers a verified kind — and its
fingerprint is pure-Python FNV over the whole value: the research pick child's 15 MB of step outputs paid
~2.4 s of CPU on a laptop per pass (L-SPEED, 2026-11-02), on every step and again on the caller's Run
Workflow step. Under the limit, and for ``output.to_frontend``'s own payload (not interned), nothing changes.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph.checkpoint import postgres as checkpoint_pg
from matrx_graph.checkpoint.values import event_payload_row
from matrx_graph.content_ir import envelope as env
from matrx_graph.content_ir import fingerprint as fp

LIMIT = 4096


@pytest.fixture
def store_on(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    """The value store is on with a 4 KB event limit; returns the lengths of every fingerprinted text."""
    import matrx_graph.knobs as knobs

    monkeypatch.setattr(checkpoint_pg, "_value_store_available", lambda: True)

    async def limit() -> int:
        return LIMIT

    monkeypatch.setattr(knobs, "event_inline_value_max_bytes", limit)
    hashed: list[int] = []
    real = fp.fingerprint_text

    def spy(text: str) -> str:
        hashed.append(len(text))
        return real(text)

    monkeypatch.setattr(fp, "fingerprint_text", spy)
    return hashed


def _rows(n: int) -> dict[str, Any]:
    return {"rows": [{"id": i, "url": f"https://example.org/{i}", "score": i / 7} for i in range(n)]}


@pytest.mark.asyncio
async def test_an_output_the_frame_carries_by_reference_gets_no_envelope(store_on: list[int]) -> None:
    value = _rows(400)
    assert len(env.compact_json(value).encode()) > LIMIT
    # The frame really does carry it by reference: the envelope would rehydrate markers.
    frame, stored = event_payload_row({"event": "node_completed", "output": value}, LIMIT)
    assert stored and frame["output"] != value
    assert await env.ir_metadata_for_verified_output_async(value, "x_kind", frame_interns_output=True) is None
    assert store_on == [], "a value that ships no envelope was fingerprinted anyway"


@pytest.mark.asyncio
async def test_an_output_the_frame_carries_inline_keeps_its_exact_envelope(store_on: list[int]) -> None:
    value = _rows(5)
    assert len(env.compact_json(value).encode()) <= LIMIT
    frame, stored = event_payload_row({"event": "node_completed", "output": value}, LIMIT)
    assert not stored and frame["output"] == value
    got = await env.ir_metadata_for_verified_output_async(value, "x_kind", frame_interns_output=True)
    assert got == env.ir_metadata_for_verified_output(value, "x_kind")


@pytest.mark.asyncio
async def test_a_frontend_payload_keeps_its_envelope_at_any_size(store_on: list[int]) -> None:
    """``output.to_frontend`` ships its value inline in ``payload`` (never interned)."""
    value = _rows(400)
    got = await env.ir_metadata_for_verified_output_async(value, "x_kind")
    assert got == env.ir_metadata_for_verified_output(value, "x_kind")


@pytest.mark.asyncio
async def test_without_a_value_store_every_output_keeps_its_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(checkpoint_pg, "_value_store_available", lambda: False)
    value = _rows(400)
    got = await env.ir_metadata_for_verified_output_async(value, "x_kind", frame_interns_output=True)
    assert got == env.ir_metadata_for_verified_output(value, "x_kind")


def test_the_scheduler_says_its_frame_interns_the_output() -> None:
    from pathlib import Path

    text = (Path(env.__file__).resolve().parents[1] / "executor" / "scheduler.py").read_text()
    assert "ir_metadata_for_verified_output_async(" in text
    assert "frame_interns_output=True" in text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "source",
    ["a" * (LIMIT + 1), "a" * LIMIT, "é" * (LIMIT // 2), "é" * (LIMIT // 2 + 1), "😀" * (LIMIT // 4), "😀" * 1100, "x"],
)
async def test_the_by_reference_test_matches_the_byte_length_exactly(store_on: list[int], source: str) -> None:
    assert await env._output_rides_by_reference(source) == (len(source.encode()) > LIMIT)


@pytest.mark.asyncio
async def test_a_large_output_is_never_encoded_on_the_loop(store_on: list[int], monkeypatch: pytest.MonkeyPatch) -> None:
    """event_loop_stall 5e9e61da: ``len(source.encode())`` on a huge output held the loop 1.28 s."""
    encoded_on_loop: list[int] = []
    monkeypatch.setattr(env, "_utf8_length", lambda s: encoded_on_loop.append(len(s)) or len(s.encode()))
    assert await env._output_rides_by_reference("a" * (50 * LIMIT)) is True
    assert encoded_on_loop == [], "an over-limit string was encoded although its char count already answered"
