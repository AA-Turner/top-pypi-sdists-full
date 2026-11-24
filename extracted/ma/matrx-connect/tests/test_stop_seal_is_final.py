"""STOP IS FINAL ON THE WIRE (P8-RUNS).

Live defect (lead's adversary): a STOPPED chat reply kept growing ~0.9 s after
Stop — the wire reached byte 3484 — while the saved reply held 1641 bytes. The
cancel route took its DB round trips (tree root, who-may-stop, the tree read)
before the in-process registry fired, and the turn only noticed at its next
0.25 s stop poll (0.5 s for a stamp from another server task); every chunk the
provider produced meanwhile went out. Now an accepted Stop SEALS the emitter:
content frames from any producer are dropped, terminal frames still go out,
and the saved stopped text is exactly what was sent.

Seam: the real StreamEmitter, fed by a fake provider producing tokens on a
timer, read by a real primary reader. Break this guards: any content frame
published after ``seal_after_stop``; a saved text that differs from the
concatenation of the sent ``c`` frames; END/close-off not going out after a seal.
"""

from __future__ import annotations

import asyncio
import json

import pytest

from matrx_connect.emitters.stream_emitter import StreamEmitter


async def _drain(emitter: StreamEmitter) -> list[dict]:
    frames: list[dict] = []
    async for raw in emitter.generate():
        frames.append(json.loads(raw))
    return frames


async def _provider(emitter: StreamEmitter, stop_after: asyncio.Event, ticks: int = 60) -> None:
    """A provider streaming a token every 5 ms — it does NOT stop when sealed (as live)."""
    for i in range(ticks):
        await emitter.send_chunk(f"tok{i:02d} ")
        if i == 20:
            stop_after.set()
        await asyncio.sleep(0.005)


@pytest.mark.asyncio
async def test_no_content_frame_leaves_after_the_seal_and_saved_equals_sent():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.reset_turn_text()
    reader = asyncio.create_task(_drain(emitter))
    stop_now = asyncio.Event()
    provider = asyncio.create_task(_provider(emitter, stop_now))

    await stop_now.wait()
    assert emitter.seal_after_stop() is True
    assert emitter.seal_after_stop() is False  # idempotent
    sealed_at_seq = emitter._wire_seq
    await provider  # the provider ran on for ~40 more tokens

    closeoff: list[str] = []

    async def close_blocks() -> None:
        closeoff.append("ran")
        await emitter.send_data({"close_off": True})
        await emitter.send_chunk("late text from a close-off")  # content: still dropped

    emitter.on_sealed(close_blocks)
    await emitter.send_end(reason="cancelled")
    frames = await reader

    content = [f for f in frames if f.get("e") in ("c", "r")]
    assert content, "the turn streamed before the Stop"
    assert all(f["stream_seq"] <= sealed_at_seq for f in content), "a content frame left after the seal"
    sent = "".join(f["t"] for f in content if f["e"] == "c")
    # The provider offered far more than was sent; the save is what was SENT.
    assert len(emitter.get_turn_text()) >= len(sent)
    assert emitter.sent_text_snapshot() == sent
    assert emitter.get_seen_turn_text() == sent
    # Order: seal → close-off frames → END.
    assert closeoff == ["ran"]
    tail = [f.get("event") for f in frames if f["stream_seq"] > sealed_at_seq]
    assert tail[-1] == "end"
    assert "data" in tail and tail.index("data") < tail.index("end")


@pytest.mark.asyncio
async def test_text_held_in_the_flush_buffer_at_the_seal_is_never_sent_nor_saved():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.reset_turn_text()
    await emitter.send_chunk("x" * 30)  # > 25 chars: flushed
    await emitter.send_chunk("held")  # < 15 ms later, short: buffered, not on the wire
    emitter.seal_after_stop()
    await emitter.send_end(reason="cancelled")
    frames = [json.loads(raw) async for raw in emitter.generate()]
    sent = "".join(f["t"] for f in frames if f.get("e") == "c")
    assert sent == "x" * 30
    assert emitter.get_seen_turn_text() == sent


@pytest.mark.asyncio
async def test_the_seal_supersedes_the_stop_moment_time_cut():
    """Frames sent between the press and the seal reached the screen: they are saved."""
    import time

    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.reset_turn_text()
    await emitter.send_chunk("before the press, long enough to flush. ")
    emitter.note_stop_cursor(at=time.time())
    await asyncio.sleep(0.02)
    await emitter.send_chunk("after the press, before the seal arrives. ")
    emitter.seal_after_stop()
    await emitter.send_chunk("after the seal")
    assert emitter.get_seen_turn_text() == (
        "before the press, long enough to flush. after the press, before the seal arrives. "
    )


@pytest.mark.asyncio
async def test_an_unsealed_stream_is_byte_identical_to_before():
    """No Stop, no seal: the frames are exactly the frames — the www chat reads the same wire."""
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.reset_turn_text()
    for i in range(5):
        await emitter.send_chunk(f"chunk number {i} with padding text ")
    await emitter.send_end()
    frames = [json.loads(raw) async for raw in emitter.generate()]
    assert "".join(f["t"] for f in frames if f.get("e") == "c") == "".join(
        f"chunk number {i} with padding text " for i in range(5)
    )
    assert frames[-1]["event"] == "end"
