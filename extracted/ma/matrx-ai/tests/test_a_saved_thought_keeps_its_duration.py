"""A saved thinking part keeps how long the model thought (CGU-09 verification 2026-10-31b, P2-4).

The live row says "Thought for 1s" from the stream's reasoning started/stopped events; the saved part
had no duration, so at the hand-off (and on every reopen) the row became "Thought" and changed width.
The stream emitter now clocks the reasoning signals, and the executor stamps the call's thinking
time on the response's first thinking part as ``metadata.duration_ms`` — which persists with it.
"""

from __future__ import annotations

import asyncio

from matrx_connect.emitters.stream_emitter import StreamEmitter

from matrx_ai.config import TextContent, ThinkingContent, UnifiedMessage, UnifiedResponse
from matrx_ai.orchestrator.executor import _stamp_thinking_duration, _take_reasoning_ms


def test_the_stream_emitter_clocks_the_thought_and_the_executor_saves_it() -> None:
    async def run() -> int | None:
        emitter = StreamEmitter()
        assert _take_reasoning_ms(emitter) is None, "no thought, no figure"
        await emitter.send_reasoning_state("started")
        await asyncio.sleep(0.05)
        await emitter.send_reasoning_state("stopped")
        return _take_reasoning_ms(emitter)

    ms = asyncio.run(run())
    assert ms is not None and ms >= 40, ms

    thinking = ThinkingContent(text="weighing it up")
    response = UnifiedResponse(messages=[UnifiedMessage(role="assistant", content=[thinking, TextContent(text="Hi")])])
    _stamp_thinking_duration(response, ms)
    assert thinking.metadata.get("duration_ms") == ms
    assert thinking.to_storage_dict()["metadata"]["duration_ms"] == ms, "the figure persists with the part"


def test_a_take_resets_the_clock() -> None:
    async def run() -> tuple[int | None, int | None]:
        emitter = StreamEmitter()
        await emitter.send_reasoning_state("started")
        await asyncio.sleep(0.02)
        await emitter.send_reasoning_state("stopped")
        return _take_reasoning_ms(emitter), _take_reasoning_ms(emitter)

    first, second = asyncio.run(run())
    assert first and second is None
