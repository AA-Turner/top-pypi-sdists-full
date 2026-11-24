"""One response opens ONE journal segment, however its start was interrupted.

THE BREAK THIS GUARDS (one turn, one stream — 2026-11-18, production rows):
``runtime.operation_stream`` held TWO rows, created 0.4 ms apart, for ~450 chat
requests a week. The body generator was cancelled (the client was already gone)
while it awaited the host's journal open; ``journal_done`` is set only AFTER that
await, so ``_begin_unread_work`` opened a SECOND segment for the same request. The
first row was never written to and never closed: it sat ``open`` with ``last_seq=0``
until the reaper failed it a minute later (``operation_stream_stranded_after_terminal_
request``) — a phantom live stream for a turn that had already finished, which a
rejoin can pick as "the newest segment" and follow as if the run were still going.

Drives the REAL Starlette ``StreamingResponse.__call__`` with a client that is gone.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_connect.context.app_context import AppContext
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.streaming import journal as journal_mod
from matrx_connect.streaming.response import create_streaming_response

ORG = "5b0e4a51-8d2f-4c52-9d0a-2f3c1e7a9b10"


class _Segment:
    """A journal segment that publishes at once and records how it ended."""

    def __init__(self, name: str) -> None:
        self.stream_id = name
        self.frames = 0
        self.closed: str | None = None

    async def enqueue(self, *, sequence: int, wire: bytes, publish: Any) -> None:
        self.frames += 1
        await publish(wire)

    async def close(self, *, status: str, last_seq: int) -> None:
        self.closed = status


async def _gone_receive() -> dict[str, Any]:
    return {"type": "http.disconnect"}


async def _run(emitter: Any, done: asyncio.Event) -> None:
    await asyncio.sleep(0.05)
    await emitter.send_end()
    done.set()


@pytest.mark.asyncio
async def test_a_start_interrupted_mid_open_still_opens_one_segment(monkeypatch: pytest.MonkeyPatch) -> None:
    opened: list[_Segment] = []

    async def factory(_ctx: AppContext) -> _Segment:
        # The host's open is a real round trip (aidream: a Postgres insert). The row is
        # written the moment the call is made; the await is where a disconnect lands.
        segment = _Segment(f"segment-{len(opened) + 1}")
        opened.append(segment)
        await asyncio.sleep(0.02)
        return segment

    monkeypatch.setattr(journal_mod, "_sink_factory", factory)
    emitter = StreamEmitter(heartbeat_interval=600)
    ctx = AppContext(
        emitter=emitter,
        user_id="user-front-desk",
        auth_type="token",
        is_authenticated=True,
        organization_id=ORG,
        organization_admission="verified",
        request_id="req-one-segment",
        conversation_id="conv-one-segment",
    )
    done = asyncio.Event()
    response = create_streaming_response(ctx, _run, done, debug_label="one-segment")

    async def send(_message: dict[str, Any]) -> None:
        return None

    scope = {"type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"}}
    try:
        await response(scope, _gone_receive, send)
    except Exception:  # noqa: BLE001 — a disconnect surfaced by the server
        pass
    await asyncio.wait_for(done.wait(), timeout=5)
    for _ in range(50):
        if opened and opened[-1].closed is not None:
            break
        await asyncio.sleep(0.02)

    assert len(opened) == 1, (
        f"one response opened {len(opened)} journal segments for one request: the extra one is "
        "never written and never closed, a phantom live stream for a finished turn "
        "(operation_stream_stranded_after_terminal_request)."
    )
    assert opened[0].frames > 0, "the one segment carried no frames"
    assert opened[0].closed is not None, "the one segment was never closed"


@pytest.mark.asyncio
async def test_a_refused_open_is_tried_once_and_reaches_both_starters(monkeypatch: pytest.MonkeyPatch) -> None:
    """The open fails while the body is being cancelled: the unread starter gets the SAME refusal (no second
    open, no exception left unretrieved on the shared task) and the work still runs, journal-less, as before."""
    opens = 0

    async def factory(_ctx: AppContext) -> _Segment:
        nonlocal opens
        opens += 1
        await asyncio.sleep(0.02)
        raise RuntimeError("the journal database is unreachable")

    monkeypatch.setattr(journal_mod, "_sink_factory", factory)
    emitter = StreamEmitter(heartbeat_interval=600)
    ctx = AppContext(
        emitter=emitter,
        user_id="user-front-desk",
        auth_type="token",
        is_authenticated=True,
        organization_id=ORG,
        organization_admission="verified",
        request_id="req-refused-open",
        conversation_id="conv-refused-open",
    )
    done = asyncio.Event()
    response = create_streaming_response(ctx, _run, done, debug_label="refused-open")

    async def send(_message: dict[str, Any]) -> None:
        return None

    scope = {"type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"}}
    try:
        await response(scope, _gone_receive, send)
    except Exception:  # noqa: BLE001 — a disconnect surfaced by the server
        pass
    await asyncio.wait_for(done.wait(), timeout=5)
    assert opens == 1, f"a refused open was retried {opens} times for one response"


@pytest.mark.asyncio
async def test_a_raising_journal_open_is_reported_loudly_and_never_raises_into_the_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A journal that cannot open must neither raise out of the response nor go silent: the still-connected
    client receives the typed ``operation_stream_journal_unavailable`` error and a clean end of body, the work
    is never half-started, and the failure is captured."""
    from matrx_connect.streaming import response as response_mod

    async def factory(_ctx: AppContext) -> _Segment:
        raise RuntimeError("the journal database is unreachable")

    captured: list[str] = []

    async def fake_capture(_exc: BaseException, *, kind: str, **_kw: Any) -> None:
        captured.append(kind)

    monkeypatch.setattr(journal_mod, "_sink_factory", factory)
    monkeypatch.setattr(response_mod, "capture_error", fake_capture)
    emitter = StreamEmitter(heartbeat_interval=600)
    ctx = AppContext(
        emitter=emitter,
        user_id="user-front-desk",
        auth_type="token",
        is_authenticated=True,
        organization_id=ORG,
        organization_admission="verified",
        request_id="req-raising-sink-live",
        conversation_id="conv-raising-sink-live",
    )
    done = asyncio.Event()
    response = create_streaming_response(ctx, _run, done, debug_label="raising-sink-live")
    sent: list[Any] = []
    hold = asyncio.Event()

    async def receive() -> dict[str, Any]:
        await hold.wait()
        return {"type": "http.disconnect"}

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    scope = {"type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"}}
    try:
        await asyncio.wait_for(response(scope, receive, send), timeout=5)
    finally:
        hold.set()
    body = b"".join(m.get("body", b"") for m in sent if m.get("type") == "http.response.body")
    assert b"operation_stream_journal_unavailable" in body, "the client was not told the journal failed"
    assert captured == ["operation_stream_journal_open_failed"], f"the failure was not captured: {captured}"
    assert not done.is_set(), "the work started against a stream with no journal"
