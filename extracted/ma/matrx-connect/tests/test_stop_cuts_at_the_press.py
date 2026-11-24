"""STOP CUTS AT THE PRESS (P8-RUNS, the server half of "Stop is final").

Live defect (proof-desk adversary, server db4f10cac55, a blocks-v2 chat): after the person pressed
Stop, text kept arriving AND WAS SAVED — +1,113 chars inside a code block, +1,129 inside mermaid,
+1,188 in the first second — because a sealed v2 turn saved up to "the last watermark the server had
SENT" when the cancel arrived (1–2 s of DB round trips after the press), ignoring the client's own
watermark (``seen_seq``) that the Stop carried. And the stopped reply's ``message_blocks`` (announced
by the save) left 0.1–1.3 s BEFORE the block owner's close-off frames (``complete: false``).

Seam: the real StreamEmitter, a fake v2 block owner (``set_shown_text_cut`` + ``on_sealed``) driving
real ``block.grow`` data frames, read by a real primary reader. Breaks this guards: a saved stopped
text longer than the grow the client's cursor covers; a ``message_blocks`` frame on the wire before
the close-off; a Stop with no cursor changing what it saves or sends.
"""

from __future__ import annotations

import asyncio
import json

import pytest

from matrx_connect.emitters.stream_emitter import StreamEmitter

def piece(i: int) -> str:
    """30 distinct chars (> 25, so every chunk flushes at once; distinct, so no snapshot defense)."""
    return f"[{i:02d}] the stopped reply goes on. "[:30]


class _FakeV2Owner:
    """The block owner's two hooks, as live_blocks registers them: a shown cut and a close-off."""

    def __init__(self, emitter: StreamEmitter) -> None:
        self.emitter = emitter
        self.shown = 0
        emitter.set_shown_text_cut(lambda: self.shown)
        emitter.on_sealed(self.close_off)

    async def grow(self, text: str) -> None:
        await self.emitter.send_chunk(text)
        if self.emitter.sealed:
            return  # nothing grows after the seal
        self.shown += len(text)
        await self.emitter.send_data({"type": "block.grow", "part": 0, "end": self.shown, "text": text})

    async def close_off(self) -> None:
        await self.emitter.send_data({"type": "block.close", "part": 0, "end": self.shown, "complete": False})


async def _drain(emitter: StreamEmitter) -> list[dict]:
    return [json.loads(raw) async for raw in emitter.generate()]


async def _run(*, cursor_after: int | None, grows: int = 12, press_at: int = 4) -> tuple[StreamEmitter, list[dict], int]:
    """Stream ``grows`` pieces; the page presses Stop after piece ``press_at``; the cancel arrives later."""
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.reset_turn_text()
    reader = asyncio.create_task(_drain(emitter))
    owner = _FakeV2Owner(emitter)
    seen_seq = 0
    for i in range(grows):
        await owner.grow(piece(i))
        if i == press_at:
            seen_seq = emitter._wire_seq  # the last frame the page applied when Stop was pressed
    # The cancel lands after the server already sent more watermarks.
    emitter.note_stop_cursor(seen_seq=seen_seq if cursor_after is not None else None, at=None)
    emitter.seal_after_stop()
    await owner.grow(piece(99))  # the provider unwinding: dropped
    await emitter.send_data({"type": "message_blocks", "message_id": "m", "parts": []})
    await emitter.send_end(reason="cancelled")
    return emitter, await reader, seen_seq


@pytest.mark.asyncio
async def test_a_stop_with_the_clients_watermark_saves_only_up_to_the_press():
    emitter, frames, seen_seq = await _run(cursor_after=4)
    grows = [f for f in frames if f.get("event") == "data" and f["data"].get("type") == "block.grow"]
    covered = [f for f in grows if f["stream_seq"] <= seen_seq]
    assert covered and len(grows) > len(covered), "the server sent watermarks past the press"
    saved = emitter.get_seen_turn_text()
    assert saved == "".join(piece(i) for i in range(len(covered))), "text past the client's watermark was saved"


@pytest.mark.asyncio
async def test_the_stop_close_off_reaches_the_wire_before_message_blocks():
    _emitter, frames, _seen = await _run(cursor_after=4)
    kinds = [(f["data"].get("type"), f["stream_seq"]) for f in frames if f.get("event") == "data"]
    close = next(seq for kind, seq in kinds if kind == "block.close")
    blocks = next(seq for kind, seq in kinds if kind == "message_blocks")
    assert close < blocks, "message_blocks went out before the close-off (complete: false)"
    assert frames[-1]["event"] == "end"
    assert sum(1 for kind, _ in kinds if kind == "block.close") == 1  # the close-off runs once


@pytest.mark.asyncio
async def test_a_stop_without_a_watermark_keeps_todays_cut_and_frames():
    """No cursor (old clients): the save is the last watermark sent, and the wire carries the same
    frames in the same order as before — only message_blocks' place relative to the close-off moved."""
    emitter, frames, _seen = await _run(cursor_after=None)
    grows = [f for f in frames if f.get("event") == "data" and f["data"].get("type") == "block.grow"]
    assert emitter.get_seen_turn_text() == "".join(piece(i) for i in range(len(grows)))
    shape = [f.get("e") or f["data"].get("type") if f.get("event") in (None, "data") else f.get("event") for f in frames]
    assert shape == ["c", "block.grow"] * 12 + ["block.close", "message_blocks", "end"]


@pytest.mark.asyncio
async def test_a_seen_seq_zero_stop_before_any_grow_saves_nothing_and_still_closes_off():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.reset_turn_text()
    reader = asyncio.create_task(_drain(emitter))
    owner = _FakeV2Owner(emitter)
    await owner.grow(piece(0))
    emitter.note_stop_cursor(seen_seq=0, at=None)  # frame numbers start at 1: nothing was applied
    emitter.seal_after_stop()
    await emitter.send_data({"type": "message_blocks", "message_id": "m", "parts": []})
    await emitter.send_end(reason="cancelled")
    frames = await reader
    assert emitter.get_seen_turn_text() == ""
    kinds = [f["data"].get("type") for f in frames if f.get("event") == "data"]
    assert kinds.index("block.close") < kinds.index("message_blocks")


@pytest.mark.asyncio
async def test_a_stop_after_the_block_owner_finished_saves_the_whole_reply_the_client_was_sent():
    """The blocks closed ``complete: true`` before the stop's last look: no close-off can say "stopped here", so the
    row must equal the frames (stop_first, live 2026-11-15: 41 chars sent, 1 saved)."""
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.reset_turn_text()
    reader = asyncio.create_task(_drain(emitter))
    owner = _FakeV2Owner(emitter)
    for i in range(3):
        await owner.grow(piece(i))
    await emitter.send_data({"type": "block.close", "part": 0, "end": owner.shown, "complete": True})
    emitter.note_shown_final()
    emitter.note_stop_cursor(seen_seq=0, at=None)
    emitter.seal_after_stop()
    await emitter.send_end(reason="cancelled")
    await reader
    assert emitter.get_seen_turn_text() == "".join(piece(i) for i in range(3))
