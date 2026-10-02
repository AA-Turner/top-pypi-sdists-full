"""Stop persists only what reached the person — never the tail generated after.

Bench run 2026-10-01 (clone, conversation 360f1626…, request bd6afdce…): the
person pressed Stop on /chat. The client aborted its read AT ONCE (the screen
froze) while the cancel POST was still on its way; the chat route detaches on
disconnect, so the provider kept generating until the cancel landed. W-47
(df06420150) then persisted the emitter's WHOLE turn text — including that
unseen tail — and the client's post-Stop re-read swapped the screen to the
longer save: the answer "kept growing" after Stop (369 → 435 words) and a
reload showed the full 435.

Seam: the real StreamEmitter (primary reader + in-process replay readers) and
the executor's stopped-call builder. Break this guards: the stopped call's
persisted partial includes text published after the last live reader left.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from matrx_connect.emitters.stream_emitter import StreamEmitter

from matrx_ai.orchestrator import executor

SEEN = "Greeting: open every call with a warm, unhurried hello. "
UNSEEN = "Insurance: ask for the member ID and group number before booking."


def _texts(response) -> list[str]:
    return [c.text for m in response.messages for c in m.content if getattr(c, "text", None)]


async def _primary_reads_then_leaves(emitter: StreamEmitter, text: str) -> None:
    """The browser reads ``text`` off the wire, then aborts its fetch (Stop)."""
    await emitter.send_chunk(text)
    reader = emitter.generate()
    frame = json.loads(await anext(reader))
    assert frame["t"] == text
    await reader.aclose()  # client disconnect: detach, work keeps running


@pytest.mark.asyncio
async def test_a_stop_after_the_reader_left_keeps_only_what_it_read():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await _primary_reads_then_leaves(emitter, SEEN)

    # The cancel POST is still in flight; the provider keeps generating.
    await emitter.send_chunk(UNSEEN)

    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "bench-stop-after-detach"
    )
    assert _texts(response) == [SEEN]


@pytest.mark.asyncio
async def test_a_stop_with_the_reader_still_attached_keeps_everything_streamed():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await emitter.send_chunk(SEEN)
    await emitter.send_chunk(UNSEEN)

    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "bench-stop-attached"
    )
    assert _texts(response) == [SEEN + UNSEEN]


@pytest.mark.asyncio
async def test_a_reader_that_rejoins_sees_everything_again():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await _primary_reads_then_leaves(emitter, SEEN)
    await emitter.send_chunk(UNSEEN)

    rejoin = emitter.generate_replay()
    replayed = [json.loads(await anext(rejoin))["t"] for _ in range(2)]
    assert "".join(replayed) == SEEN + UNSEEN

    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "bench-stop-rejoined"
    )
    assert _texts(response) == [SEEN + UNSEEN]
    await rejoin.aclose()


@pytest.mark.asyncio
async def test_a_turn_that_began_after_the_reader_left_persists_nothing():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await _primary_reads_then_leaves(emitter, SEEN)

    emitter.reset_turn_text()  # next provider call, nobody watching
    await emitter.send_chunk(UNSEEN)

    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "bench-stop-next-turn"
    )
    assert response.messages == []


@pytest.mark.asyncio
async def test_a_detached_run_that_finishes_still_keeps_its_whole_turn_text():
    """Detach (tab closed) is not Stop: the full turn text stays available."""
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await _primary_reads_then_leaves(emitter, SEEN)
    await emitter.send_chunk(UNSEEN)

    assert emitter.get_turn_text() == SEEN + UNSEEN


# ── Bench run 2 (2026-10-01 23:37Z, agent window, conversation 6ca03037…) ──
# The server cut at the reader-left mark (saved 3874 of 3932 wire chars), yet
# the screen held fewer: frames already written to the socket when the browser
# aborted never reached the page, so the post-Stop re-read still GREW the
# answer (588 → 629 words). Only the client knows the last frame it applied;
# the cancel carries it (``seen_seq``) and the stopped partial ends there.


@pytest.mark.asyncio
async def test_a_stop_keeps_only_what_the_client_says_it_applied():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await emitter.send_chunk(SEEN)
    reader = emitter.generate()
    seen_frame = json.loads(await anext(reader))
    await emitter.send_chunk(UNSEEN)
    await anext(reader)  # written to the socket, never applied by the page
    await reader.aclose()

    emitter.note_seen_seq(seen_frame["stream_seq"])
    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "bench2-stop-seen-seq"
    )
    assert _texts(response) == [SEEN]


@pytest.mark.asyncio
async def test_a_seen_cursor_before_this_turn_keeps_nothing_of_it():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await emitter.send_chunk(SEEN)
    reader = emitter.generate()
    seen_frame = json.loads(await anext(reader))
    emitter.reset_turn_text()
    await emitter.send_chunk(UNSEEN)
    await anext(reader)

    emitter.note_seen_seq(seen_frame["stream_seq"])
    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "bench2-stop-prior-turn"
    )
    assert response.messages == []
    await reader.aclose()


@pytest.mark.asyncio
async def test_the_cancel_route_hands_seen_seq_to_the_live_emitter(monkeypatch):
    from matrx_connect.emitters.stream_emitter import (
        register_active_stream,
        unregister_active_stream,
    )

    from aidream.api.routers import cancel as cancel_router

    emitter = StreamEmitter(heartbeat_interval=3600)
    register_active_stream("bench2-route", emitter)
    try:
        await cancel_router.cancel_request(
            "bench2-route",
            mode="cancel",
            seen_seq=7,
            ctx=SimpleNamespace(user_id="u-1"),
        )
    finally:
        unregister_active_stream("bench2-route", emitter)
    assert emitter.seen_seq == 7


def test_the_block_wrapper_never_loses_its_own_turn_text():
    """The block wrapper owns its text (blocks replace chunks on the wire);
    asking the inner emitter would answer "" and drop the whole partial."""
    from aidream.services.ai_execution.ai_task_blocks import BlockStreamingEmitter

    wrapper = BlockStreamingEmitter(StreamEmitter(heartbeat_interval=3600))
    wrapper._turn_text_acc = [SEEN]
    response = executor._stopped_call_response(
        SimpleNamespace(emitter=wrapper), "bench2-block-wrapper"
    )
    assert _texts(response) == [SEEN]
