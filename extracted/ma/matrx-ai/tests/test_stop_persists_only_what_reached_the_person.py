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


# ── CGU-09 fourth verification (2026-11-01), parity P-008 ──
# The phone pressed Stop while its waiting dot still showed; the screen said
# "Stopped" with no text, and the saved reply held 1,000–2,100 characters. Two
# leaks: the server cut where the provider call STOPPED (up to a poll later),
# not where the wire was when Stop arrived; and a cancel that landed on ANOTHER
# server task (no stickiness) never reached this emitter at all.


@pytest.mark.asyncio
async def test_a_stop_keeps_only_what_was_on_the_wire_when_it_was_asked_for():
    import asyncio
    import time

    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await emitter.send_chunk(SEEN)
    reader = emitter.generate()
    await anext(reader)  # still attached: no reader-left mark, no client cursor
    await asyncio.sleep(0.01)
    emitter.note_stop_cursor(at=time.time())
    await asyncio.sleep(0.01)
    await emitter.send_chunk(UNSEEN)  # the provider ran on until the stop poll
    await anext(reader)

    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "p008-cancel-moment"
    )
    assert _texts(response) == [SEEN]
    await reader.aclose()


@pytest.mark.asyncio
async def test_a_client_that_applied_nothing_keeps_nothing():
    """``seen_seq=0``: the phone's Stop during the waiting dot — no frame applied."""
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await emitter.send_chunk(SEEN + UNSEEN)
    emitter.note_stop_cursor(seen_seq=0)

    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "p008-nothing-applied"
    )
    assert response.messages == []


@pytest.mark.asyncio
async def test_a_cancel_on_another_server_task_reaches_the_cut(monkeypatch):
    """The cancel route on task B noted the cursor on the run's spine; task A's
    stopped call reads it back through the host hook before it saves."""
    from matrx_ai import _ext

    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await emitter.send_chunk(SEEN)
    reader = emitter.generate()
    seen_frame = json.loads(await anext(reader))
    await emitter.send_chunk(UNSEEN)
    await anext(reader)

    async def _cursor_from_spine():
        return {"seen_seq": seen_frame["stream_seq"], "at": None}

    monkeypatch.setitem(_ext._registry, "spine_stop_cursor", _cursor_from_spine)
    exec_ctx = SimpleNamespace(emitter=emitter)
    await executor._adopt_spine_stop_cursor(exec_ctx)
    response = executor._stopped_call_response(exec_ctx, "p008-other-task")
    assert _texts(response) == [SEEN]
    await reader.aclose()


@pytest.mark.asyncio
async def test_a_stopped_thought_keeps_its_duration():
    """CGU-09 P2-5: a stopped turn's inline thought saved no duration, so a
    reload read "Thought" where the live row had read "Thought for Ns"."""
    import asyncio

    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await emitter.send_reasoning_state("started")
    await emitter.send_chunk("<reasoning>Short paragraphs.\n</reasoning>\n")
    await asyncio.sleep(0.02)
    await emitter.send_reasoning_state("stopped")
    await emitter.send_chunk(SEEN)

    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "p25-stopped-thought"
    )
    # The inline thought is saved as its own thinking part (AND-V 05r F6); the duration rides it.
    thought, answer = [c for m in response.messages for c in m.content]
    assert (thought.type, answer.type) == ("thinking", "text")
    assert thought.metadata.get("duration_ms", 0) >= 20


@pytest.mark.asyncio
async def test_an_inline_thought_with_no_signals_still_keeps_its_duration():
    """Live (2026-11-01): the default chat model streams its thought as
    ``<reasoning>`` text with no started/stopped signal; a turn stopped in the
    middle saved ``<reasoning>`` with no duration, so a reload read "Thought"."""
    import asyncio

    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    emitter.take_reasoning_ms()  # the provider call's clock starts here
    await emitter.send_chunk("<reasoning>")
    await asyncio.sleep(0.03)
    await emitter.send_chunk("Need short paragraphs, no markdown.")

    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "p25-inline-thought"
    )
    (thought,) = [c for m in response.messages for c in m.content]
    assert thought.type == "thinking"
    assert thought.metadata.get("duration_ms", 0) >= 30


@pytest.mark.asyncio
async def test_a_stopped_thought_s_duration_reaches_the_saved_row():
    """CGU-09 fifth verification P2-1 (13 of 13 API Stops): the duration was set on
    the in-memory text part, but ``TextContent.to_storage_dict`` wrote only
    ``type``/``text``, so the saved part had no ``metadata.duration_ms`` and a
    reopen read "Thought" where the live row read "Thought for 1s"."""
    import asyncio

    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    emitter.take_reasoning_ms()
    await emitter.send_chunk("<reasoning>")
    await asyncio.sleep(0.03)
    await emitter.send_chunk("Need short paragraphs.")

    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "p21-saved-duration"
    )
    (thought,) = [c for m in response.messages for c in m.content]
    stored = thought.to_storage_dict()
    assert stored["type"] == "thinking"  # never "<reasoning>…" inside a text part (AND-V 05r F6)
    assert stored["text"] == "Need short paragraphs."
    assert stored.get("metadata", {}).get("duration_ms", 0) >= 30


# ── CGU-M2 attack 3, MJ1 (2026-11-02): Stop after a reload ──
# A reload drops the primary reader (the reader-left mark lands at the reload
# moment), then the page rejoins through the journal — on another server task,
# invisible to this emitter — and goes on applying frames. Its Stop carries the
# rejoined reader's applied frame. The emitter cut at the reader-left mark
# anyway: chat app showed 2,787 characters and saved 1,607; www 2,598 → 1,392.
# The client's cursor is the truth; the reader-left mark is only the fallback.


@pytest.mark.asyncio
async def test_a_stop_after_a_reload_rejoin_keeps_what_the_rejoined_page_applied():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await _primary_reads_then_leaves(emitter, "A" * 100)  # reload: the primary reader leaves
    await emitter.send_chunk("B" * 100)  # the journal rejoin reads these on another task
    await emitter.send_chunk("C" * 100)

    last_applied = emitter._turn_chunk_marks[-1][0]
    emitter.note_stop_cursor(seen_seq=last_applied)
    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "cgu-m2-reload-then-stop"
    )
    assert _texts(response) == ["A" * 100 + "B" * 100 + "C" * 100]


@pytest.mark.asyncio
async def test_a_rejoined_page_s_cursor_still_cuts_what_it_never_applied():
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    await _primary_reads_then_leaves(emitter, "A" * 100)
    await emitter.send_chunk("B" * 100)
    applied_through_b = emitter._turn_chunk_marks[-1][0]
    await emitter.send_chunk("C" * 100)  # generated, never applied by the rejoined page

    emitter.note_stop_cursor(seen_seq=applied_through_b)
    response = executor._stopped_call_response(
        SimpleNamespace(emitter=emitter), "cgu-m2-reload-partial"
    )
    assert _texts(response) == ["A" * 100 + "B" * 100]
