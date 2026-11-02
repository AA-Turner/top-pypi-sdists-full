"""A crashed streaming task must never end the wire with a success word.

THE BREAK THESE GUARD (live 2026-09-17): a task handed to
``create_streaming_response`` raised, the framework logged "TASK CRASHED", and
the client's NDJSON stream ended with
``{"event":"end","data":{"reason":"complete"}}``. Every consumer on every
platform surface therefore read a SUCCESSFUL stream that simply produced no
content. The production change that turns these tests red is reverting
``StreamEmitter.fatal_error`` to ``await self.send_end()`` (the default reason
is "complete") or removing the crash branch's announcement in
``matrx_connect/streaming/response.py``.

``test_planted_old_behaviour_fails_the_guard`` proves the guard is falsifiable:
it monkeypatches the honest ending back OFF — restoring the exact pre-fix
``fatal_error`` body — and asserts that the SAME assertions the guard uses now
fail, with the old success word in the failure text.

Pure asyncio + matrx-connect: a real StreamEmitter, the real
``create_streaming_response``, a real task that really raises, and the real
NDJSON bytes read off the response body. No DB, no other matrx-* package.
"""

from __future__ import annotations

import asyncio
import json
import types
from typing import Any

import pytest

from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.streaming.response import create_streaming_response


def _ctx(emitter: Any) -> Any:
    return types.SimpleNamespace(
        request_id="req-crash-guard-1",
        user_id="user-1",
        conversation_id=None,
        source_app="test",
        agent_id=None,
        emitter=emitter,
    )


async def _drain(response: Any) -> list[dict[str, Any]]:
    """Read the real response body and decode every NDJSON frame."""
    events: list[dict[str, Any]] = []
    async for chunk in response.body_iterator:
        text = chunk.decode() if isinstance(chunk, bytes) else chunk
        for line in text.splitlines():
            if line.strip():
                events.append(json.loads(line))
    return events


async def _run_stream(task_fn: Any, *, label: str = "guard_stream") -> list[dict[str, Any]]:
    # A long heartbeat keeps the frame list to the events the test is about.
    emitter = StreamEmitter(heartbeat_interval=600)
    response = create_streaming_response(_ctx(emitter), task_fn, debug_label=label)
    return await _drain(response)


# --- the assertions under test -------------------------------------------
# One function, used by the guard AND by the planted-defect test, so the
# falsifiability proof exercises the guard's own criteria rather than a
# paraphrase of them.


def _assert_honest_crash_ending(events: list[dict[str, Any]]) -> None:
    kinds = [e.get("event") for e in events]

    errors = [e for e in events if e.get("event") == "error"]
    assert errors, (
        "a crashed streaming task emitted NO error event — the client sees a "
        f"stream that merely produced nothing. Events: {kinds}"
    )

    ends = [e for e in events if e.get("event") == "end"]
    assert len(ends) == 1, f"expected exactly one terminal end event, got {len(ends)}: {kinds}"

    reason = ends[0].get("data", {}).get("reason")
    assert reason != "complete", (
        "the stream of a CRASHED task terminated with reason='complete' — a "
        "successful ending for work that died. The client cannot tell this "
        "apart from an empty success."
    )
    assert reason in {"error", "failed", "cancelled"}, (
        f"terminal end reason {reason!r} is not a recognized non-success reason"
    )

    # The error must be a readable sentence naming the failure, and must carry
    # the exception's TYPE — without leaking a traceback or a file path.
    payload = errors[-1].get("data", {})
    user_message = payload.get("user_message") or ""
    assert user_message and "RuntimeError" not in user_message and "settings" not in user_message, (
        f"error event's person-facing sentence names a class or blames settings: {user_message!r}"
    )
    blob = json.dumps(payload)
    assert "RuntimeError" in blob, (
        f"error event does not name the exception type anywhere: {blob}"
    )
    assert "Traceback" not in blob and ".py" not in blob, (
        f"error event leaks developer detail to the client: {blob}"
    )


# --- the guard ------------------------------------------------------------


@pytest.mark.asyncio
async def test_crashed_task_ends_the_stream_with_an_error_not_a_success():
    """A real task raises mid-stream; the wire must end honestly."""

    async def crashing_task(emitter: Any) -> None:
        await emitter.send_phase("processing")
        raise RuntimeError("downstream call blew up")

    events = await _run_stream(crashing_task)
    _assert_honest_crash_ending(events)


@pytest.mark.asyncio
async def test_planted_old_behaviour_fails_the_guard(monkeypatch: pytest.MonkeyPatch):
    """FALSIFIABILITY: put the pre-fix ending back and the guard must go red.

    The plant is the exact old body of ``StreamEmitter.fatal_error`` — error
    event, then ``send_end()`` with its default reason.
    """

    async def old_fatal_error(
        self: StreamEmitter,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        await self.send_error(error_type, message, user_message, code, details)
        await self.send_end()  # <- the defect: default reason is "complete"

    monkeypatch.setattr(StreamEmitter, "fatal_error", old_fatal_error)

    async def crashing_task(emitter: Any) -> None:
        await emitter.send_phase("processing")
        raise RuntimeError("downstream call blew up")

    events = await _run_stream(crashing_task, label="planted_old_behaviour")

    with pytest.raises(AssertionError) as excinfo:
        _assert_honest_crash_ending(events)

    assert "reason='complete'" in str(excinfo.value), (
        "the planted defect did not fail the guard on the terminal reason — "
        f"it failed on something else instead: {excinfo.value}"
    )


@pytest.mark.asyncio
async def test_successful_task_still_ends_complete():
    """The honest-ending change must not turn healthy streams into failures."""

    async def good_task(emitter: Any) -> None:
        await emitter.send_chunk("hello")
        await emitter.send_end()

    events = await _run_stream(good_task, label="healthy_stream")
    ends = [e for e in events if e.get("event") == "end"]
    assert [e.get("data", {}).get("reason") for e in ends] == ["complete"]
    assert not [e for e in events if e.get("event") == "error"]


@pytest.mark.asyncio
async def test_task_that_already_ended_gets_no_second_terminal_event():
    """IDEMPOTENCY: a task that ended its own stream and THEN crashed must not
    have a second terminal event bolted on behind the one the client read."""

    async def ends_then_crashes(emitter: Any) -> None:
        await emitter.send_chunk("done")
        await emitter.send_end()
        raise RuntimeError("tail step blew up after the stream was closed")

    events = await _run_stream(ends_then_crashes, label="already_ended_stream")
    ends = [e for e in events if e.get("event") == "end"]
    assert len(ends) == 1, f"a second terminal event was emitted: {events}"
    assert ends[-1] is events[-1], "a frame was published after the terminal end event"


@pytest.mark.asyncio
async def test_client_disconnect_is_not_an_error_and_does_not_stop_the_work():
    """detach_on_disconnect is untouched: a disconnect is not a crash.

    The reader stops consuming the body (a client going away); with detach on,
    the work task must keep running to completion and NOTHING may emit a
    failure terminal on its behalf.
    """
    started = asyncio.Event()
    finished = asyncio.Event()

    async def slow_task(emitter: Any) -> None:
        started.set()
        await asyncio.sleep(0.05)
        await emitter.send_chunk("work that outlived the browser")
        finished.set()

    emitter = StreamEmitter(heartbeat_interval=600)
    response = create_streaming_response(
        _ctx(emitter), slow_task, debug_label="detach_stream", detach_on_disconnect=True
    )

    iterator = response.body_iterator
    await iterator.__anext__()  # open the body, then walk away
    await started.wait()
    await iterator.aclose()

    await asyncio.wait_for(finished.wait(), timeout=5)
    # The detached work ends on its own terms: once it returns, the framework ends
    # the stream with "complete" (tests/test_stream_ends_after_journal_flush.py) so a
    # replay rejoiner knows the turn is over. What must never appear is an error or
    # canceled terminal written on the disconnect's behalf.
    for _ in range(50):
        if emitter.has_ended:
            break
        await asyncio.sleep(0.02)
    frames = [json.loads(b) for b in emitter._wire_replay]
    terminals = [f for f in frames if f.get("event") in ("end", "error")]
    assert [f.get("event") for f in terminals] == ["end"], (
        "a client disconnect terminalized the stream with a failure — detached work "
        f"must be left alone to finish and end on its own terms: {terminals}"
    )
    assert terminals[0]["data"].get("reason") == "complete"
    assert frames[-1] is terminals[0], "the END was not the last frame the detached work wrote"
    assert any("work that outlived the browser" in json.dumps(f) for f in frames[:-1])
