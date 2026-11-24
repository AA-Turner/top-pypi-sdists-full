"""Blocks v1 shadow (CGU-14 P2): off unless switched on, never touches the call, records truth."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.processing.blocks import blocks_shadow
from matrx_ai.processing.blocks.blocks_shadow import (
    configure_blocks_shadow,
    shadowing_blocks,
    take_summary,
)


class _Sink:
    def __init__(self) -> None:
        self.chunks: list[str] = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_phase(self, phase: str) -> None:
        self.chunks.append(f"<phase:{phase}>")


@dataclass
class _Text:
    text: str
    type: str = "text"


@dataclass
class _Msg:
    content: list[Any]
    role: str = "assistant"


@dataclass
class _Resp:
    messages: list[_Msg] = field(default_factory=list)


@pytest.fixture(autouse=True)
def _switch_reset():
    yield
    configure_blocks_shadow(None)


def _run(chunks: list[str], response_text: str | None, *, on: bool = True) -> tuple[ExecutionState, _Sink]:
    from matrx_connect.context.app_context import AppContext, set_app_context, try_get_app_context

    configure_blocks_shadow((lambda: True) if on else None)
    sink = _Sink()
    before = try_get_app_context()
    set_app_context(AppContext(emitter=sink))
    state = ExecutionState()

    async def call() -> None:
        with shadowing_blocks(state) as finish:
            emitter = try_get_app_context().emitter
            for c in chunks:
                await emitter.send_chunk(c)
            await emitter.send_phase("done")
            await finish(_Resp([_Msg([_Text(response_text if response_text is not None else "".join(chunks))])]))
        assert try_get_app_context().emitter is sink

    try:
        asyncio.run(call())
    finally:
        if before is not None:
            set_app_context(before)
    return state, sink


TEXT = 'Intro\n```json\n{"__kind":"flashcard_set","title":"T"}\n```\n<think>\nhm\n</think>\nEnd'


def _chunks(text: str, n: int = 5) -> list[str]:
    return [text[i : i + n] for i in range(0, len(text), n)]


def test_off_unless_switched_on() -> None:
    state, sink = _run(_chunks(TEXT), None, on=False)
    assert take_summary(state) is None
    assert "".join(c for c in sink.chunks if not c.startswith("<phase")) == TEXT


def test_records_cost_types_and_no_divergence_and_forwards_everything() -> None:
    state, sink = _run(_chunks(TEXT), None)
    s = take_summary(state)
    assert s is not None
    assert (s["calls"], s["text_mismatch"], s["block_divergence"], s["shadow_errors"]) == (1, 0, 0, 0)
    assert s["tokens"] == len(_chunks(TEXT))
    assert s["types"] == {"markdown": 2, "kind": 1, "reasoning": 1}
    assert s["feed_us_total"] > 0 and s["feed_us_worst_call_p99"] > 0
    assert sink.chunks[:-1] == _chunks(TEXT) and sink.chunks[-1] == "<phase:done>"


def test_stream_text_that_is_not_the_saved_text_is_counted() -> None:
    state, _ = _run(["<reasoning>x</reasoning>", "Answer"], "Answer")
    s = take_summary(state)
    assert s["text_mismatch"] == 1
    assert s["last_text_mismatch"]["stream_has_reasoning_tag"] is True
    assert s["last_text_mismatch"]["cause"] == "reasoning_in_stream"
    assert s["text_mismatch_causes"] == {"reasoning_in_stream": 1}


def test_every_text_mismatch_is_named_with_a_bounded_head() -> None:
    # CGU-14 step 6c: a mismatch with no reasoning tag still says where the texts part and what differs.
    state, _ = _run(["Hello ", "world"], "Hello world\n\nSources: [1] a.com")
    m = take_summary(state)["last_text_mismatch"]
    assert m["common_prefix_chars"] == len("Hello world")
    assert m["stream_only_chars"] == 0 and m["response_only_head"] == "\n\nSources: [1] a.com"
    assert m["cause"] == "response_extra"
    state, _ = _run(["Text\nMATRX_JSON_BEGIN\n", "{}"], "Text\n{}")
    m = take_summary(state)["last_text_mismatch"]
    assert m["cause"] == "grounded_json_markers" and len(m["stream_only_head"]) <= blocks_shadow.MISMATCH_HEAD_CHARS


def test_a_broken_guarantee_is_counted(monkeypatch: pytest.MonkeyPatch) -> None:
    real = blocks_shadow.split_blocks_v1

    def lying(text: str, **kw: Any):
        blocks = real(text, **kw)
        return blocks[:-1] if not kw else blocks

    from matrx_connect.streaming.error_capture import configure_error_capture

    captured: list[dict[str, Any]] = []

    async def sink(exc: BaseException, **fields: Any) -> None:
        captured.append({"exc": str(exc), **fields})

    monkeypatch.setattr(blocks_shadow, "split_blocks_v1", lying)
    configure_error_capture(sink, allow_in_tests=True)
    try:
        state, _ = _run(_chunks(TEXT), None)
    finally:
        configure_error_capture(None)
    assert take_summary(state)["block_divergence"] == 1
    # Through the REAL capture door (no stubbed import): the incident reaches system_error.
    assert [c["kind"] for c in captured] == ["blocks_v1_shadow_divergence"]


def test_several_text_parts_are_counted_not_skipped() -> None:
    from matrx_connect.context.app_context import AppContext, set_app_context, try_get_app_context

    configure_blocks_shadow(lambda: True)
    before = try_get_app_context()
    set_app_context(AppContext(emitter=_Sink()))
    state = ExecutionState()

    async def call() -> None:
        with shadowing_blocks(state) as finish:
            await try_get_app_context().emitter.send_chunk("ab")
            await finish(_Resp([_Msg([_Text("a"), _Text("b")])]))

    try:
        asyncio.run(call())
    finally:
        if before is not None:
            set_app_context(before)
    assert take_summary(state)["divergence_unchecked"] == 1


def test_a_sealed_run_keeps_the_summary_but_not_free_text() -> None:
    from matrx_ai.persistence.sealed import keep_by_spec, sealed_metadata_spec

    state, _ = _run(_chunks(TEXT), None)
    summary = {**take_summary(state), "last_error": "may quote the reply"}
    kept = keep_by_spec({"blocks_shadow": summary}, sealed_metadata_spec("chat.user_request"))["blocks_shadow"]
    assert kept["calls"] == 1 and kept["types"] == summary["types"]
    assert "last_error" not in kept
    assert set(summary) - set(kept) == {"last_error"}


def test_a_shadow_failure_never_touches_the_call(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(self: Any, chunk: str) -> list[Any]:
        raise RuntimeError("scanner broke")

    monkeypatch.setattr(blocks_shadow.BlocksV1Splitter, "feed", boom)
    state, sink = _run(_chunks(TEXT), None)
    s = take_summary(state)
    assert s["shadow_errors"] == 1 and "scanner broke" in s["last_error"]
    assert "".join(c for c in sink.chunks if not c.startswith("<phase")) == TEXT

