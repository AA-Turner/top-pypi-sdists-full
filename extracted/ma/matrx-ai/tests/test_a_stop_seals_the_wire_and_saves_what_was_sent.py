"""A stopped turn sends NO content after the stop, and saves exactly what it sent (P8-RUNS).

Live defect (lead's adversary): a STOPPED chat reply kept growing ~0.9 s after
Stop (the wire reached byte 3484) while the saved reply held 1641 bytes and
ended mid-code-fence. The stop poll only cancelled the provider task; until
then — and while the task unwound — every chunk the provider produced still
streamed, while the save was cut at the Stop moment. Now the loop SEALS its own
emitter the instant it sees the stop (this is the only door a cancel that
landed on another server task has: the spine stamp), and the stopped turn's
saved text is the concatenation of the content frames that were sent.

Seam: the real StreamEmitter (installed as the AppContext emitter, read by a
real primary reader), the real ``_execute_stoppable`` stop poll driven by the
spine control hook, and the real ``_stopped_call_response`` save. The fake
provider streams a token every 10 ms and does not stop on its own. Break this
guards: a content frame published after the stop is seen; saved != sent.
"""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import _app_context, set_app_context
from matrx_connect.emitters.stream_emitter import StreamEmitter

from matrx_ai import _ext
from matrx_ai.orchestrator import executor


@pytest.mark.asyncio
async def test_a_spine_stop_seals_the_wire_and_the_save_equals_what_was_sent(monkeypatch):
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.reset_turn_text()
    frames: list[dict] = []

    async def read() -> None:
        async for raw in emitter.generate():
            frames.append(json.loads(raw))

    reader = asyncio.create_task(read())
    stamped = asyncio.Event()
    seal_seq: dict[str, int] = {}

    async def spine_check() -> str | None:
        return "cancel requested" if stamped.is_set() else None

    monkeypatch.setitem(_ext._registry, "spine_control_check", spine_check)

    real_seal = emitter.seal_after_stop

    def recording_seal() -> bool:
        seal_seq.setdefault("seq", emitter._wire_seq)
        return real_seal()

    monkeypatch.setattr(emitter, "seal_after_stop", recording_seal)

    async def fake_provider_call() -> str:
        for i in range(400):
            if i == 15:
                stamped.set()  # Stop accepted on ANOTHER server task: only the spine knows
            try:
                await emitter.send_chunk(f"word{i:03d} ")
                await asyncio.sleep(0.01)
            except asyncio.CancelledError:
                # A provider adapter flushing what it held while it unwinds.
                await emitter.send_chunk("UNWIND-TAIL ")
                raise
        return "full answer"

    token = set_app_context(AppContext(emitter=emitter, metadata={}))
    try:
        with pytest.raises(executor.ProviderCallStopped):
            await executor._execute_stoppable(fake_provider_call(), "p8-seal-spine")
        # The provider produced past the stamp; nothing it produced after the seal left.
        await emitter.send_chunk("a straggler after the stop")
        saved = executor._stopped_call_response(SimpleNamespace(emitter=emitter), "p8-seal-spine")
        await emitter.send_end(reason="cancelled")
    finally:
        _app_context.reset(token)
    await reader

    assert "seq" in seal_seq, "the loop never sealed its own stream when it saw the stop"
    content = [f for f in frames if f.get("e") in ("c", "r")]
    late = [f for f in content if f["stream_seq"] > seal_seq["seq"]]
    assert not late, f"content frames left after the stop: {late}"
    sent = "".join(f["t"] for f in content if f["e"] == "c")
    assert "UNWIND-TAIL" not in sent
    texts = [c.text for m in saved.messages for c in m.content if getattr(c, "text", None)]
    assert "".join(texts) == sent
    assert frames[-1]["event"] == "end"
