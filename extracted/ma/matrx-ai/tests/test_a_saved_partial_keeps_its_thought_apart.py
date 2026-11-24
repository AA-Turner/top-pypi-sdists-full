"""A turn saved from the streamed text holds its thought as a thinking part, never inside the text.

AND-V 05r F6 (2026-11-05): the providers stream a thought INLINE (``<reasoning>…</reasoning>`` at the
front of the text chunks). A finished turn is saved from the provider's native reasoning field — a
``thinking`` part and a clean ``text`` part. A turn saved from the emitter's streamed text was not: a
stopped partial (2,119 rows in four days) and an iteration-1 row whose provider call ended before its tool
call (21 rows, e.g. conversation 5949557c… — ``<reasoning>Need to use web search function.``) kept the tag
in one ``text`` part, so every reader that is not a renderer (copy, export, search, an agent reading
history) got the thought as answer text.

Seams: the real StreamEmitter and the executor's builders (``_stopped_call_response``,
``_partial_response_from_emitter`` + ``_append_partial_response``), read back through
``to_storage_dict`` — the shape ``chat.message.content`` stores. Break these guard: a saved text part
starts with or contains a reasoning region; the thought is dropped instead of kept as its own part; the
thought's duration leaves it.
"""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace

import pytest
from matrx_connect.emitters.stream_emitter import StreamEmitter

from matrx_ai.config import UnifiedConfig
from matrx_ai.orchestrator import executor
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.processing.blocks.reasoning_parts import inline_reasoning_parts


def _stored(response) -> list[dict]:
    return [part.to_storage_dict() for m in response.messages for part in m.content]


def _no_tag_in_text(parts: list[dict]) -> None:
    for part in parts:
        if part["type"] == "text":
            for tag in ("<reasoning>", "</reasoning>", "<think>", "<thinking>"):
                assert tag not in part["text"], part


async def _emitter_streamed(*chunks: str) -> StreamEmitter:
    emitter = StreamEmitter(heartbeat_interval=3600)
    emitter.set_detach_on_disconnect(True)
    emitter.reset_turn_text()
    emitter.take_reasoning_ms()  # the provider call's clock starts here
    for chunk in chunks:
        await emitter.send_chunk(chunk)
        await asyncio.sleep(0.01)
    return emitter


# What groq_api.py streams: reasoning_opener, the thought, "\n</reasoning>\n", then the answer.
GROQ_STREAM = ("<reasoning>", "We need to produce three sections.", "\n</reasoning>\n", "**Wins**\n\nShipped the gate.")


@pytest.mark.asyncio
async def test_a_stopped_partial_that_began_with_a_thought_saves_it_as_a_thinking_part():
    emitter = await _emitter_streamed(*GROQ_STREAM)

    response = executor._stopped_call_response(SimpleNamespace(emitter=emitter), "f6-stopped")

    parts = _stored(response)
    assert [p["type"] for p in parts] == ["thinking", "text"]
    assert parts[0]["text"] == "We need to produce three sections."
    assert parts[1]["text"] == "**Wins**\n\nShipped the gate."
    assert parts[0]["metadata"].get("duration_ms", 0) >= 20  # "Thought for Ns" survives the reload
    _no_tag_in_text(parts)
    assert response.messages[0].metadata.get("stopped") is True


@pytest.mark.asyncio
async def test_a_stop_in_the_middle_of_the_thought_keeps_the_thought_and_no_text():
    emitter = await _emitter_streamed("\n<reasoning>\n", "Need short paragraphs, no markdown.")

    parts = _stored(executor._stopped_call_response(SimpleNamespace(emitter=emitter), "f6-mid-thought"))

    assert [p["type"] for p in parts] == ["thinking"]
    assert parts[0]["text"] == "Need short paragraphs, no markdown."
    assert parts[0]["metadata"].get("duration_ms", 0) >= 10


@pytest.mark.asyncio
async def test_a_tool_call_iteration_row_saved_from_the_stream_holds_no_tag():
    """Iteration 1 thought about its tool call, then the provider call ended before the call was
    assembled: the failure path saves the streamed text as that iteration's assistant row."""
    emitter = await _emitter_streamed("<reasoning>", "Need to use web search function.")
    request = AIMatrixRequest(
        conversation_id="conv-f6",
        request_id="req-f6",
        config=UnifiedConfig.from_dict(
            {
                "model": "openai/gpt-oss-120b",
                "messages": [{"role": "user", "content": [{"type": "text", "text": "Search the web."}]}],
            }
        ),
    )
    state = SimpleNamespace(iteration=1, current_request=request)

    partial = executor._partial_response_from_emitter(SimpleNamespace(emitter=emitter))
    updated = executor._append_partial_response(request, partial, state)

    row = updated.config.messages[-1]
    assert row.metadata.get("provider_iteration") == 1
    parts = [part.to_storage_dict() for part in row.content]
    assert [p["type"] for p in parts] == ["thinking"]
    assert parts[0]["text"] == "Need to use web search function."
    _no_tag_in_text(parts)


def test_text_with_no_thought_is_one_text_part_unchanged():
    text = "Plain answer.\n\n```python\nprint('<reasoning>')\n```\n"
    (part,) = inline_reasoning_parts(text)
    assert part.type == "text" and part.text == text


def test_a_tag_inside_prose_is_not_a_thought():
    (part,) = inline_reasoning_parts("Use the <reasoning> tag like this.")
    assert part.type == "text"


def test_every_region_in_order_and_unicode_offsets_hold():
    parts = inline_reasoning_parts("<think>première</think>\nÉtape 1 — ok\n<reasoning>deux\n</reasoning>\nfin")
    assert [(p.type, p.text) for p in parts] == [
        ("thinking", "première"),
        ("text", "Étape 1 — ok"),
        ("thinking", "deux"),
        ("text", "fin"),
    ]
    assert "<" not in json.dumps([p.to_storage_dict() for p in parts if p.type == "text"])


# --- The interrupt writer: execute_until_complete's cancel capture (AND-V 05u finding 1) -----------------


async def _interrupted_run(monkeypatch, *chunks: str) -> list[dict]:
    """Drive the REAL ``execute_until_complete`` into its cancel/interrupt branch with the emitter holding
    ``chunks``, and answer the parts the run handed to ``_finalize_and_persist`` (what ``cx_message`` stores)."""
    emitter = await _emitter_streamed(*chunks)
    request = AIMatrixRequest(
        conversation_id="conv-interrupt",
        request_id="req-interrupt",
        config=UnifiedConfig.from_dict(
            {
                "model": "openai/gpt-oss-120b",
                "messages": [{"role": "user", "content": [{"type": "text", "text": "Write the report."}]}],
            }
        ),
    )
    saved: dict = {}

    async def _inner(*, state, initial_request, **_):
        state.current_request = initial_request
        raise asyncio.CancelledError  # the person's Stop / a disconnect, mid-stream

    async def _persist(**kwargs):
        saved.update(kwargs)

    async def _sweep(self, **_):
        return None

    from matrx_ai.tools.logger import ToolExecutionLogger

    monkeypatch.setattr(executor, "get_app_context", lambda: SimpleNamespace(emitter=emitter))
    monkeypatch.setattr(executor, "_execute_until_complete_inner", _inner)
    monkeypatch.setattr(executor, "_finalize_and_persist", _persist)
    monkeypatch.setattr(ToolExecutionLogger, "settle_open_rows_at_run_end", _sweep)

    with pytest.raises(asyncio.CancelledError):
        await executor.execute_until_complete(request, client=SimpleNamespace())

    assert saved, "the interrupt branch never reached the persist step"
    assert saved["metadata"]["interrupted"] is True and saved["metadata"]["partial_assistant_captured"] is True
    return _stored(saved["final_response"])


@pytest.mark.asyncio
async def test_an_interrupt_saves_the_thought_apart_and_the_marker_ends_the_answer(monkeypatch):
    parts = await _interrupted_run(monkeypatch, *GROQ_STREAM)

    assert [p["type"] for p in parts] == ["thinking", "text"]
    assert parts[0]["text"] == "We need to produce three sections."
    assert parts[1]["text"] == "**Wins**\n\nShipped the gate." + executor._INTERRUPT_MARKER
    _no_tag_in_text(parts)


@pytest.mark.asyncio
async def test_an_interrupt_in_the_middle_of_the_thought_keeps_the_thought_and_a_marker_only_text(monkeypatch):
    parts = await _interrupted_run(monkeypatch, "<reasoning>", "Need short paragraphs, no markdown.")

    assert [p["type"] for p in parts] == ["thinking", "text"]
    assert parts[0]["text"] == "Need short paragraphs, no markdown."
    assert parts[1]["text"] == executor._INTERRUPT_MARKER.lstrip("\n")  # the marker never lands inside the thought
    _no_tag_in_text(parts)
