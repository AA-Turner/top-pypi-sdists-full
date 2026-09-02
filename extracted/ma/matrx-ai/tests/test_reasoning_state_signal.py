"""Regression tests for the content-less reasoning-lifecycle signal.

Every provider signals when a thinking/reasoning block STARTS independent of
whether reasoning TEXT is streamed. With thinking-content suppressed (Anthropic
display="omitted", OpenAI reasoning_summary="never", Gemini include_thoughts=
False) no reasoning text ever arrives, so the FE used to see nothing but
heartbeats during a long silent think. These tests lock the fix: the provider
stream parsers emit balanced ``reasoning`` state events ("started"/"stopped")
at the block boundary, whether or not any reasoning text flows — and NEVER emit
a stray signal on a turn with no thinking.
"""

from __future__ import annotations

from types import SimpleNamespace as NS

import pytest

from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat
from matrx_ai.providers.google.google_api import GoogleChat
from matrx_ai.providers.openai.openai_api import OpenAIChat


class _CaptureEmitter:
    """Records the ordered sequence of reasoning-state signals (and chunks)."""

    def __init__(self) -> None:
        self.events: list[tuple[str, object]] = []

    async def send_chunk(self, text: str) -> None:
        self.events.append(("chunk", text))

    async def send_reasoning_state(self, state: str) -> None:
        self.events.append(("reasoning", state))

    async def send_info(self, payload) -> None:
        self.events.append(("info", None))

    def reset_turn_text(self) -> None: ...

    def get_turn_text(self) -> str:
        return ""

    @property
    def reasoning(self) -> list[str]:
        return [v for k, v in self.events if k == "reasoning"]


# --------------------------------------------------------------------------- #
# Google / Gemini — reasoning is inferred from part shape.
# --------------------------------------------------------------------------- #

def _part(**kw):
    base = dict(thought=None, text=None, inline_data=None, function_call=None, thought_signature=None)
    base.update(kw)
    return NS(**base)


async def _run_google(parts) -> _CaptureEmitter:
    api = object.__new__(GoogleChat)  # skip genai.Client construction
    api._reasoning_signaled = False
    em = _CaptureEmitter()
    for p in parts:
        await api._handle_part(p, em)
    await api._signal_reasoning_stopped(em)  # stream-end safety net
    return em


@pytest.mark.asyncio
async def test_google_thinking_omitted_signals_started_stopped():
    # include_thoughts=False: bare thought_signature parts, then the answer.
    em = await _run_google([
        _part(thought_signature=b"sig"),
        _part(thought_signature=b"sig2"),
        _part(text="The answer is 42."),
    ])
    assert em.reasoning == ["started", "stopped"]


@pytest.mark.asyncio
async def test_google_thinking_visible_signals_started_stopped():
    em = await _run_google([
        _part(thought=True, text="Let me think..."),
        _part(text="Final answer."),
    ])
    assert em.reasoning == ["started", "stopped"]


@pytest.mark.asyncio
async def test_google_no_thinking_emits_no_signal():
    em = await _run_google([_part(text="Hi.")])
    assert em.reasoning == []


@pytest.mark.asyncio
async def test_google_thinking_then_toolcall_closes_signal():
    em = await _run_google([
        _part(thought_signature=b"sig"),
        _part(function_call=NS(name="foo")),
    ])
    assert em.reasoning == ["started", "stopped"]


# --------------------------------------------------------------------------- #
# Anthropic — explicit thinking content_block start/stop.
# --------------------------------------------------------------------------- #

def _cb_start(block_type):
    return NS(type="content_block_start", content_block=NS(type=block_type, name=""))

def _cb_delta_thinking(text):
    return NS(type="content_block_delta", delta=NS(type="thinking_delta", thinking=text))

def _cb_delta_text(text):
    return NS(type="content_block_delta", delta=NS(type="text_delta", text=text))

def _cb_stop():
    return NS(type="content_block_stop")


async def _run_anthropic(events) -> _CaptureEmitter:
    api = AnthropicChat()  # SDK client tolerates a missing key at construction
    api._reasoning_open = False
    api._reasoning_signaled = False
    em = _CaptureEmitter()
    for ev in events:
        await api._handle_event(ev, em)
    return em


@pytest.mark.asyncio
async def test_anthropic_thinking_omitted_signals_started_stopped():
    # display="omitted": a thinking block start/stop with NO thinking_delta.
    em = await _run_anthropic([
        _cb_start("thinking"),
        _cb_stop(),
        _cb_start("text"),
        _cb_delta_text("Hello."),
        _cb_stop(),
    ])
    assert em.reasoning == ["started", "stopped"]


@pytest.mark.asyncio
async def test_anthropic_thinking_visible_signals_started_stopped():
    em = await _run_anthropic([
        _cb_start("thinking"),
        _cb_delta_thinking("reasoning text"),
        _cb_stop(),
        _cb_start("text"),
        _cb_delta_text("answer"),
        _cb_stop(),
    ])
    assert em.reasoning == ["started", "stopped"]


@pytest.mark.asyncio
async def test_anthropic_no_thinking_emits_no_stray_signal():
    # A text block's content_block_stop must NOT fire a reasoning-stopped.
    em = await _run_anthropic([
        _cb_start("text"),
        _cb_delta_text("answer"),
        _cb_stop(),
    ])
    assert em.reasoning == []


# --------------------------------------------------------------------------- #
# OpenAI (Responses API) — reasoning output item added/done.
# --------------------------------------------------------------------------- #

def _oa_reasoning_added(item_id):
    return NS(type="response.output_item.added", item=NS(type="reasoning", id=item_id))

def _oa_reasoning_summary_delta(item_id, text):
    return NS(type="response.reasoning_summary_text.delta", item_id=item_id, delta=text)

def _oa_reasoning_done(item_id):
    return NS(type="response.output_item.done", item=NS(type="reasoning", id=item_id))

def _oa_text_delta(text):
    return NS(type="response.output_text.delta", delta=text)


async def _run_openai(events) -> _CaptureEmitter:
    api = OpenAIChat()
    api._reasoning_started = {}
    api._reasoning_signaled_ids = set()
    api._event_samples = {}
    em = _CaptureEmitter()
    for ev in events:
        await api._handle_event(ev, em)
    return em


@pytest.mark.asyncio
async def test_openai_reasoning_summary_never_signals_started_stopped():
    # reasoning_summary="never": item added + done, no summary text delta.
    em = await _run_openai([
        _oa_reasoning_added("rs_1"),
        _oa_reasoning_done("rs_1"),
        _oa_text_delta("Hello."),
    ])
    assert em.reasoning == ["started", "stopped"]


@pytest.mark.asyncio
async def test_openai_reasoning_with_summary_signals_started_stopped():
    em = await _run_openai([
        _oa_reasoning_added("rs_1"),
        _oa_reasoning_summary_delta("rs_1", "summary text"),
        _oa_reasoning_done("rs_1"),
        _oa_text_delta("answer"),
    ])
    assert em.reasoning == ["started", "stopped"]


@pytest.mark.asyncio
async def test_openai_no_reasoning_emits_no_signal():
    em = await _run_openai([_oa_text_delta("just an answer")])
    assert em.reasoning == []
