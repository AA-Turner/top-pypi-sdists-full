"""A stream must end only after every accepted frame has committed and reached the reader.

THE BREAK THIS GUARDS (live 2026-09-27, Knowledge Ask): the journal sink publishes
a frame to the reader only AFTER it commits. A task that returned without calling
``send_end()`` let ``StreamEmitter.generate`` see "task done" on its next idle tick
and close the response while the last frames (``citations``, ``sources_used``,
``ask_done``) were still committing — they never reached the person, and the wire
carried no END at all. Every route had to remember ``send_end()``; most did not.

The fix is in ``create_streaming_response``: a task that returns normally is ended
by the framework (``send_end`` closes the sink, which flushes every accepted frame,
then puts the terminator). ``test_old_behaviour_loses_the_late_frame`` plants the
old wrapper (no framework end) and shows the same assertions fail.

Pure asyncio + matrx-connect: the real StreamEmitter, the real response, a journal
double that commits on a background writer after a delay (the Postgres sink's shape).
"""

from __future__ import annotations

import asyncio
import json
import types
from typing import Any

import pytest

from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.streaming import journal as journal_mod
from matrx_connect.streaming import response as response_mod
from matrx_connect.streaming.response import create_streaming_response

COMMIT_DELAY_S = 1.6  # longer than generate()'s 1 s idle tick


class SlowCommitSink:
    """Commits each frame on a background writer after a delay, then publishes it."""

    stream_id = "stream-slow-commit"

    def __init__(self) -> None:
        self._queue: asyncio.Queue[tuple[bytes, Any] | None] = asyncio.Queue()
        self._writer = asyncio.create_task(self._run())

    async def _run(self) -> None:
        while True:
            item = await self._queue.get()
            if item is None:
                return
            wire, publish = item
            await asyncio.sleep(COMMIT_DELAY_S)
            await publish(wire)

    async def enqueue(self, *, sequence: int, wire: bytes, publish: Any) -> None:
        await self._queue.put((wire, publish))

    async def close(self, *, status: str, last_seq: int) -> None:
        await self._queue.put(None)
        await self._writer


def _ctx(emitter: Any) -> Any:
    return types.SimpleNamespace(
        request_id="req-journal-flush-1",
        user_id="user-1",
        conversation_id=None,
        source_app="test",
        agent_id=None,
        emitter=emitter,
    )


async def _drain(response: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    async for chunk in response.body_iterator:
        text = chunk.decode() if isinstance(chunk, bytes) else chunk
        events.extend(json.loads(line) for line in text.splitlines() if line.strip())
    return events


async def _task_that_forgets_send_end(emitter: Any) -> None:
    await emitter.send_data({"type": "answer_delta", "text": "The budget is 40k [S1]."})
    await emitter.send_data({"type": "citations", "citations": [{"number": 1}]})
    # returns WITHOUT send_end — exactly what run_knowledge_search does


async def _run() -> list[dict[str, Any]]:
    async def factory(_ctx: Any) -> SlowCommitSink:
        return SlowCommitSink()

    journal_mod.configure_stream_journal_sink_factory(factory)
    try:
        emitter = StreamEmitter(heartbeat_interval=600)
        response = create_streaming_response(_ctx(emitter), _task_that_forgets_send_end, debug_label="flush_guard")
        return await asyncio.wait_for(_drain(response), timeout=30)
    finally:
        journal_mod.configure_stream_journal_sink_factory(None)


def _assert_every_frame_then_end(events: list[dict[str, Any]]) -> None:
    kinds = [(e.get("event"), (e.get("data") or {}).get("type")) for e in events]
    assert ("data", "citations") in kinds, f"the late citations frame never reached the reader: {kinds}"
    assert kinds[-1][0] == "end", f"the stream closed without an END frame: {kinds}"
    assert kinds.index(("data", "citations")) < len(kinds) - 1


@pytest.mark.asyncio
async def test_a_task_that_returns_is_ended_after_every_frame_commits() -> None:
    _assert_every_frame_then_end(await _run())


@pytest.mark.asyncio
async def test_old_behaviour_loses_the_late_frame(monkeypatch: pytest.MonkeyPatch) -> None:
    async def no_framework_end(_emitter: Any) -> None:
        return None

    monkeypatch.setattr(response_mod, "_end_after_normal_return", no_framework_end)
    events = await _run()
    with pytest.raises(AssertionError, match="never reached the reader|without an END"):
        _assert_every_frame_then_end(events)
