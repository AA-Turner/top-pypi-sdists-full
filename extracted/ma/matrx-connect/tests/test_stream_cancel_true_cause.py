"""A cancelled stream records its TRUE cause, and a by-design end files no error row.

Live 2026-11-16 (system_error 27a25a2c, d2eb6af0): every research Stop — the work obeying
``POST /cancel``, or a child workflow run that ended cancelled because of it — was filed as an open
``stream_cancelled`` row reading "canceled (client disconnect or shutdown)". The Stop was honored and
nothing was lost; a shutdown or an outside cancel that cut work off must still file, with its own cause.
Real ``create_streaming_response``; recording capture sink and run opener.
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
def seen(monkeypatch):
    runs: list[str] = []
    captured: list[dict] = []

    async def opener(_ctx, _req):
        return _Handle(runs)

    async def capture(exc, *, kind, **fields):
        captured.append({"kind": kind, **fields})

    monkeypatch.setattr(response, "capture_error", capture)
    prior_opener, prior_sink = run_tracking._opener, journal._sink_factory
    run_tracking.configure_stream_run_opener(opener)
    journal.configure_stream_journal_sink_factory(None)
    yield runs, captured
    run_tracking.configure_stream_run_opener(prior_opener)
    journal.configure_stream_journal_sink_factory(prior_sink)
    run_tracking.configure_shutdown_probe(None)


async def _drain(resp) -> None:
    async for _ in resp.body_iterator:
        pass
    await asyncio.sleep(0.05)


class _ChildRunStopped(Exception):
    pass


async def test_a_stop_the_work_obeyed_files_no_error_row(seen):
    runs, captured = seen

    async def task(_emitter):
        raise asyncio.CancelledError("research pass stopped before scrape batch: canceled via POST /cancel")

    await _drain(response.create_streaming_response(_ctx(), task, debug_label="ResearchScrape"))
    assert captured == [], "an honored Stop lost nothing: it is not an open error"
    assert runs == ["settle:cancelled"]


async def test_a_child_run_that_ended_cancelled_files_no_error_row(seen):
    runs, captured = seen

    async def task(_emitter):
        try:
            raise _ChildRunStopped("Mandate 'research.journey.read': child run ended cancelled")
        except _ChildRunStopped as exc:
            raise asyncio.CancelledError("research step read stopped: workflow run x ended cancelled") from exc

    await _drain(response.create_streaming_response(_ctx(), task, debug_label="ResearchJourney:read"))
    assert captured == []
    assert runs == ["settle:cancelled"]


async def _cut_off_by_shutdown(seen, opener_returns_run: bool):
    runs, captured = seen
    started = asyncio.Event()

    async def slow(_emitter):
        started.set()
        await asyncio.sleep(30)

    if not opener_returns_run:
        async def no_run(_ctx, _req):
            return None

        run_tracking.configure_stream_run_opener(no_run)
    ctx = _ctx()
    resp = response.create_streaming_response(ctx, slow, debug_label="ResearchPipeline")
    body = resp.body_iterator
    reader = asyncio.ensure_future(body.__anext__())
    await asyncio.wait_for(started.wait(), 2)
    from matrx_connect.emitters.stream_emitter import get_active_stream

    run_tracking.configure_shutdown_probe(lambda: True)
    get_active_stream(str(ctx.request_id))._task.cancel()
    await asyncio.sleep(0.05)
    reader.cancel()
    await body.aclose()
    return runs, captured


async def test_a_shutdown_of_a_stream_with_no_run_files_an_error_naming_the_shutdown(seen):
    _runs, captured = await _cut_off_by_shutdown(seen, opener_returns_run=False)
    assert len(captured) == 1
    row = captured[0]
    assert row["kind"] == "stream_cancelled"
    assert row["error_type"] == "stream_server_shutdown"
    assert "server shutdown" in row["error_text"]
    assert "client disconnect" not in row["error_text"]
    assert row["context"]["cancel_cause"] == "server_shutdown"


async def test_a_shutdown_of_a_stream_with_a_run_leaves_the_alarm_to_the_run_reaper(seen):
    """The reaper alarms only when nothing resumes the work; a second row here would alarm a resumed one."""
    runs, captured = await _cut_off_by_shutdown(seen, opener_returns_run=True)
    assert captured == []
    assert runs == ["abandon"], "the abandoned run is what the reaper judges"


async def test_an_outside_cancel_files_an_error_that_does_not_blame_the_client(seen):
    runs, captured = seen
    started = asyncio.Event()

    async def slow(_emitter):
        started.set()
        await asyncio.sleep(30)

    ctx = _ctx()
    resp = response.create_streaming_response(ctx, slow, debug_label="T")
    body = resp.body_iterator
    reader = asyncio.ensure_future(body.__anext__())
    await asyncio.wait_for(started.wait(), 2)
    from matrx_connect.emitters.stream_emitter import get_active_stream

    get_active_stream(str(ctx.request_id))._task.cancel()
    await asyncio.sleep(0.05)
    reader.cancel()
    await body.aclose()
    assert [r["error_type"] for r in captured] == ["stream_external_cancel"]
    assert "(client disconnect or shutdown)" not in captured[0]["error_text"]
    assert "outside task.cancel()" in captured[0]["error_text"]
    assert runs == ["abandon"]


async def test_a_client_leaving_a_non_detached_route_files_no_error_row(seen):
    runs, captured = seen
    started = asyncio.Event()

    async def slow(_emitter):
        started.set()
        await asyncio.sleep(30)

    resp = response.create_streaming_response(_ctx(), slow, debug_label="T", detach_on_disconnect=False)
    body = resp.body_iterator
    reader = asyncio.ensure_future(body.__anext__())
    await asyncio.wait_for(started.wait(), 2)
    reader.cancel()
    await body.aclose()
    await asyncio.sleep(0.1)
    assert captured == []
    assert runs == ["settle:cancelled"]
