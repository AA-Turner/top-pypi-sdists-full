"""The stream run is settled or abandoned on EVERY exit of the work task.

Regression for the review finding "settle not in a finally": an error handler
that raised (or a CancelledError re-raised inside the crash branch) skipped the
settle, so the run's heartbeat renewed for hours. Recording opener, real
`create_streaming_response`.
"""

from __future__ import annotations

import asyncio

import pytest
from matrx_connect import AppContext, StreamEmitter
from matrx_connect.streaming import journal, response, run_tracking

pytestmark = pytest.mark.asyncio


class _Handle:
    execution_id = "exec-1"

    def __init__(self, events: list[str]) -> None:
        self.events = events

    async def settle(self, outcome, *, error_type=None, message=None):
        self.events.append(f"settle:{outcome}")

    def abandon(self):
        self.events.append("abandon")


def _ctx() -> AppContext:
    return AppContext(
        emitter=StreamEmitter(),
        user_id="44444444-4444-4444-8444-444444444444",
        request_id="55555555-5555-4555-8555-555555555555",
        organization_id="6b0f2c4e-6b3f-4a37-9a1a-6b1d0f2a51cc",
    )


@pytest.fixture
def events(monkeypatch):
    recorded: list[str] = []

    async def opener(_ctx, _req):
        return _Handle(recorded)

    async def _no_capture(*_a, **_k):
        return None

    monkeypatch.setattr(response, "capture_error", _no_capture)
    prior_opener, prior_sink = run_tracking._opener, journal._sink_factory
    run_tracking.configure_stream_run_opener(opener)
    journal.configure_stream_journal_sink_factory(None)
    yield recorded
    run_tracking.configure_stream_run_opener(prior_opener)
    journal.configure_stream_journal_sink_factory(prior_sink)


async def _drain(resp) -> None:
    async for _ in resp.body_iterator:
        pass
    await asyncio.sleep(0.02)


async def test_an_exploding_error_handler_still_settles_the_run_failed(events, monkeypatch):
    async def boom(**_kw):
        raise RuntimeError("persist_turn_failure exploded")

    monkeypatch.setattr(response, "persist_turn_failure", boom)

    async def task(_emitter):
        raise ValueError("work crashed")

    try:
        await _drain(response.create_streaming_response(_ctx(), task, debug_label="T"))
    except Exception:  # noqa: BLE001 - the explosion may surface; the settle is the subject
        pass
    await asyncio.sleep(0.05)
    assert events == ["settle:failed"]


async def test_a_cancel_inside_the_crash_handler_abandons_the_run(events, monkeypatch):
    async def cancelled(**_kw):
        raise asyncio.CancelledError

    monkeypatch.setattr(response, "persist_turn_failure", cancelled)

    async def task(_emitter):
        raise ValueError("work crashed")

    try:
        await _drain(response.create_streaming_response(_ctx(), task, debug_label="T"))
    except BaseException:  # noqa: BLE001
        pass
    await asyncio.sleep(0.05)
    assert events == ["abandon"], "a cancel mid-handler must stop the heartbeat, not leave it renewing"


async def test_shutdown_cancel_abandons_but_disconnect_cancel_settles_cancelled(events):
    started = asyncio.Event()

    async def slow(_emitter):
        started.set()
        await asyncio.sleep(30)

    # Shutdown-style cancel (nobody marked it a disconnect): abandon.
    ctx = _ctx()
    resp = response.create_streaming_response(ctx, slow, debug_label="T", detach_on_disconnect=False)
    body = resp.body_iterator
    reader = asyncio.ensure_future(body.__anext__())
    await asyncio.wait_for(started.wait(), 2)
    from matrx_connect.emitters.stream_emitter import get_active_stream

    get_active_stream(str(ctx.request_id))._task.cancel()
    await asyncio.sleep(0.05)
    reader.cancel()
    await body.aclose()
    assert events == ["abandon"]


async def test_client_disconnect_on_a_non_detached_stream_settles_cancelled(events):
    started = asyncio.Event()

    async def slow(_emitter):
        started.set()
        await asyncio.sleep(30)

    resp = response.create_streaming_response(
        _ctx(), slow, debug_label="T", detach_on_disconnect=False
    )
    body = resp.body_iterator
    reader = asyncio.ensure_future(body.__anext__())
    await asyncio.wait_for(started.wait(), 2)
    reader.cancel()  # the client left; the generator's teardown cancels the work
    await body.aclose()
    await asyncio.sleep(0.1)
    assert events == ["settle:cancelled"]


async def test_a_teardown_while_the_host_is_shutting_down_abandons_instead_of_cancelling(events):
    """Review 2 #2: any non-detached generator teardown was recorded `cancelled`, including
    a SERVER shutdown (deploy drain). Shutdown must abandon the run — the host's lease
    reaper then records it failed with its system_error — while a real client
    disconnect (probe says no shutdown) still settles `cancelled`."""
    started = asyncio.Event()

    async def slow(_emitter):
        started.set()
        await asyncio.sleep(30)

    run_tracking.configure_shutdown_probe(lambda: True)
    try:
        resp = response.create_streaming_response(
            _ctx(), slow, debug_label="T", detach_on_disconnect=False
        )
        body = resp.body_iterator
        reader = asyncio.ensure_future(body.__anext__())
        await asyncio.wait_for(started.wait(), 2)
        reader.cancel()
        await body.aclose()
        await asyncio.sleep(0.1)
    finally:
        run_tracking.configure_shutdown_probe(None)
    assert events == ["abandon"], "a shutdown teardown must not be settled as a client cancel"


async def test_a_broken_shutdown_probe_never_breaks_teardown(events):
    started = asyncio.Event()

    async def slow(_emitter):
        started.set()
        await asyncio.sleep(30)

    def broken() -> bool:
        raise RuntimeError("probe exploded")

    run_tracking.configure_shutdown_probe(broken)
    try:
        resp = response.create_streaming_response(
            _ctx(), slow, debug_label="T", detach_on_disconnect=False
        )
        body = resp.body_iterator
        reader = asyncio.ensure_future(body.__anext__())
        await asyncio.wait_for(started.wait(), 2)
        reader.cancel()
        await body.aclose()
        await asyncio.sleep(0.1)
    finally:
        run_tracking.configure_shutdown_probe(None)
    assert events == ["settle:cancelled"]
