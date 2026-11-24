"""A run that settles while nobody reads its wire tells the host — once.

The real ``create_streaming_response``; the "reader" is the response body
iterator. Unread = the body was never driven (the client left before the body
opened) or was closed mid-run (a detached stream keeps working).
"""

from __future__ import annotations

import asyncio

import pytest
from matrx_connect import AppContext, StreamEmitter
from matrx_connect.streaming import journal, response, run_tracking, unread_settle
from matrx_connect.streaming.unread_settle import RunSettledUnread

pytestmark = pytest.mark.asyncio

ORG = "6b0f2c4e-6b3f-4a37-9a1a-6b1d0f2a51cc"
USER = "44444444-4444-4444-8444-444444444444"
CONV = "77777777-7777-4777-8777-777777777777"


def _ctx(request_id: str = "55555555-5555-4555-8555-555555555555") -> AppContext:
    return AppContext(
        emitter=StreamEmitter(),
        user_id=USER,
        request_id=request_id,
        organization_id=ORG,
        conversation_id=CONV,
        metadata={"host_marker": "chat"},
    )


@pytest.fixture
def heard(monkeypatch):
    calls: list[RunSettledUnread] = []

    async def hook(payload: RunSettledUnread) -> None:
        calls.append(payload)

    async def _no_capture(*_a, **_k):
        return None

    monkeypatch.setattr(response, "capture_error", _no_capture)
    prior = (run_tracking._opener, journal._sink_factory, unread_settle._hook)
    run_tracking.configure_stream_run_opener(None)
    journal.configure_stream_journal_sink_factory(None)
    unread_settle.configure_run_settled_unread(hook)
    yield calls
    run_tracking.configure_stream_run_opener(prior[0])
    journal.configure_stream_journal_sink_factory(prior[1])
    unread_settle.configure_run_settled_unread(prior[2])


async def _leave_mid_run(resp, released: asyncio.Event, finished: asyncio.Event) -> None:
    """Read the opening, hang up, then let the work finish with nobody reading."""
    body = resp.body_iterator
    await body.__anext__()
    await body.aclose()  # the client left; detach keeps the work running
    released.set()
    await asyncio.wait_for(finished.wait(), 2)
    await asyncio.sleep(0.05)


async def test_a_run_finished_with_nobody_reading_tells_the_host_once(heard):
    released, finished = asyncio.Event(), asyncio.Event()

    async def task(emitter):
        await released.wait()
        await emitter.send_chunk("the answer")
        finished.set()

    ctx = _ctx()
    await _leave_mid_run(response.create_streaming_response(ctx, task, debug_label="Chat"), released, finished)

    assert len(heard) == 1
    got = heard[0]
    assert got.outcome == "completed"
    assert (got.user_id, got.organization_id, got.conversation_id) == (USER, ORG, CONV)
    assert got.request_id == ctx.request_id
    assert got.metadata["host_marker"] == "chat"
    assert got.context is ctx
    # The claim is spent: a second announce for the same stream says nothing.
    assert await unread_settle.announce_run_settled_unread(ctx.emitter, ctx, "completed", "Chat") is False
    assert len(heard) == 1


async def test_a_failed_run_with_nobody_reading_tells_the_host_failed(heard):
    released, finished = asyncio.Event(), asyncio.Event()

    async def task(_emitter):
        await released.wait()
        finished.set()
        raise ValueError("provider crashed")

    await _leave_mid_run(response.create_streaming_response(_ctx(), task, debug_label="Chat"), released, finished)
    assert [c.outcome for c in heard] == ["failed"]


async def test_a_run_read_to_the_end_tells_the_host_nothing(heard):
    async def task(emitter):
        await emitter.send_chunk("seen")

    resp = response.create_streaming_response(_ctx(), task, debug_label="Chat")
    async for _ in resp.body_iterator:
        pass
    await asyncio.sleep(0.05)
    assert heard == []


async def test_a_rejoined_reader_at_the_end_tells_the_host_nothing(heard):
    released, finished = asyncio.Event(), asyncio.Event()

    async def task(emitter):
        await released.wait()
        await emitter.send_chunk("seen on rejoin")
        finished.set()

    ctx = _ctx()
    resp = response.create_streaming_response(ctx, task, debug_label="Chat")
    body = resp.body_iterator
    await body.__anext__()
    await body.aclose()
    replay = [item async for item in _rejoin(ctx.emitter, released)]
    await asyncio.wait_for(finished.wait(), 2)
    await asyncio.sleep(0.05)
    assert replay, "the rejoined reader saw the stream"
    assert heard == []


async def _rejoin(emitter: StreamEmitter, released: asyncio.Event):
    gen = emitter.generate_replay()
    first = await gen.__anext__()
    released.set()
    yield first
    async for item in gen:
        yield item


async def test_a_stopped_run_tells_the_host_nothing(heard):
    async def task(emitter):
        await emitter.send_cancelled()

    ctx = _ctx()
    emitter = ctx.emitter
    emitter.release_primary_reader()
    resp = response.create_streaming_response(ctx, task, debug_label="Chat")
    async for _ in resp.body_iterator:
        pass
    await asyncio.sleep(0.05)
    assert emitter.ended_unread is True
    assert heard == []


async def test_a_raising_hook_never_breaks_the_stream(heard, monkeypatch):
    captured: list[str] = []

    async def bad_hook(_payload):
        raise RuntimeError("host exploded")

    async def capture(_exc, *, kind, **_fields):
        captured.append(kind)

    monkeypatch.setattr(unread_settle, "capture_error", capture)
    unread_settle.configure_run_settled_unread(bad_hook)
    released, finished = asyncio.Event(), asyncio.Event()

    async def task(emitter):
        await released.wait()
        await emitter.send_chunk("x")
        finished.set()

    await _leave_mid_run(response.create_streaming_response(_ctx(), task, debug_label="Chat"), released, finished)
    assert captured == ["unread_settle_hook_failed"]


async def test_no_hook_installed_is_a_no_op(heard):
    unread_settle.configure_run_settled_unread(None)
    ctx = _ctx()
    ctx.emitter.release_primary_reader()
    await ctx.emitter.send_end()
    assert await unread_settle.announce_run_settled_unread(ctx.emitter, ctx, "completed", "Chat") is False
