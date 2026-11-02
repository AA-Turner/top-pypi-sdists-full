"""Live NDJSON reattachment for detached streaming work."""

from __future__ import annotations

import asyncio
import json
import threading
import time
from unittest.mock import AsyncMock

import pytest

from matrx_connect.emitters.stream_emitter import (
    StreamEmitter,
    get_active_stream,
    register_active_stream,
    unregister_active_stream,
)
from matrx_connect.streaming.journal import configure_stream_journal_sink_factory
from matrx_connect.streaming.response import create_streaming_response


class _CommittedJournal:
    stream_id = "11111111-1111-4111-8111-111111111111"

    def __init__(self) -> None:
        self.accepted: list[tuple[int, bytes]] = []
        self.closed: tuple[str, int] | None = None

    async def enqueue(self, *, sequence: int, wire: bytes, publish) -> None:
        self.accepted.append((sequence, wire))
        await publish(wire)

    async def close(self, *, status: str, last_seq: int) -> None:
        self.closed = (status, last_seq)


@pytest.mark.asyncio
async def test_detached_disconnect_keeps_emitting_and_replays_without_a_gap() -> None:
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)

    await emitter.send_chunk("first")
    primary = emitter.generate()
    first = json.loads(await anext(primary))
    assert first["t"] == "first"
    await primary.aclose()

    assert emitter.cancelled is False
    await emitter.send_chunk(" second")
    await emitter.send_end()

    replay = [json.loads(item) async for item in emitter.generate_replay()]
    chunks = [item["t"] for item in replay if item.get("e") == "c"]
    assert chunks == ["first", " second"]
    assert [item["stream_seq"] for item in replay] == list(range(1, len(replay) + 1))


@pytest.mark.asyncio
async def test_journal_assigns_segment_cursor_and_fans_out_only_committed_ndjson() -> None:
    emitter = StreamEmitter(heartbeat_interval=3600)
    journal = _CommittedJournal()
    emitter.attach_journal_sink(journal)

    await emitter.send_chunk("durable text")
    await emitter.send_end()

    replay = [item async for item in emitter.generate_replay()]
    assert replay == [wire for _sequence, wire in journal.accepted]
    decoded = [json.loads(item) for item in replay]
    assert [item["stream_seq"] for item in decoded] == [1, 2]
    assert {item["stream_id"] for item in decoded} == {journal.stream_id}
    assert journal.closed == ("closed", 2)


@pytest.mark.asyncio
async def test_journal_open_failure_is_structured_terminal_ndjson_not_empty_200(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_connect import AppContext
    from matrx_connect.streaming import response as response_module

    async def broken_sink(_ctx):
        raise RuntimeError("database unavailable")

    async def must_not_run(_emitter):
        raise AssertionError("paid task started after journal-open failure")

    capture = AsyncMock()
    monkeypatch.setattr(response_module, "capture_error", capture)
    configure_stream_journal_sink_factory(broken_sink)
    try:
        response = create_streaming_response(
            AppContext(
                emitter=StreamEmitter(heartbeat_interval=3600),
                request_id="44444444-4444-4444-8444-444444444444",
                user_id="22222222-2222-4222-8222-222222222222",
                organization_id="66666666-6666-4666-8666-666666666666",
                auth_type="token",
                is_authenticated=True,
                metadata={},
            ),
            must_not_run,
        )
        frames = [json.loads(frame) async for frame in response.body_iterator]
    finally:
        configure_stream_journal_sink_factory(None)
    assert [frame.get("event") for frame in frames] == ["error", "end"]
    assert frames[0]["data"]["error_type"] == "operation_stream_journal_unavailable"
    assert capture.await_args.kwargs["kind"] == "operation_stream_journal_open_failed"


def test_active_stream_registry_never_removes_a_newer_emitter() -> None:
    request_id = "request-1"
    first = StreamEmitter()
    second = StreamEmitter()

    register_active_stream(request_id, first)
    register_active_stream(request_id, second)
    unregister_active_stream(request_id, first)
    assert get_active_stream(request_id) is second

    unregister_active_stream(request_id, second)
    assert get_active_stream(request_id) is None


@pytest.mark.asyncio
async def test_legacy_data_serialization_runs_off_event_loop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    emitter = StreamEmitter(heartbeat_interval=3600)
    loop_thread = threading.get_ident()
    serialization_thread: int | None = None
    original_serialize = emitter._serialize

    def slow_serialize(payload: object) -> object:
        nonlocal serialization_thread
        serialization_thread = threading.get_ident()
        time.sleep(0.05)
        return original_serialize(payload)

    monkeypatch.setattr(emitter, "_serialize", slow_serialize)
    send_task = asyncio.create_task(emitter.send_data({"rows": [1, 2, 3]}))
    await asyncio.sleep(0.01)
    assert not send_task.done()
    await send_task
    assert serialization_thread is not None
    assert serialization_thread != loop_thread
