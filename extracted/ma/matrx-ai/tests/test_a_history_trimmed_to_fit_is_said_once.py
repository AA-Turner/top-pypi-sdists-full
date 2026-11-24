"""A history shortened to fit a smaller model is SAID in the chat — one line, never silently.

One-chat plan C2: switching a long cloud chat to a model on this computer (a far smaller context
window) makes ``prepare_for_send`` -> ``input_fit.ensure_fits`` force-trim older tool results so the
call fits. Until 2026-11-08 that trim was "announced" only in the server log: the person saw an
answer that had silently lost what it was built on. Locked here, through the real send boundary
with the real stream emitter (no network in the path):

1. a trim that rewrote history sends exactly ONE ``history_trimmed_to_fit`` warning with a line
   the person reads (promoted to a visible line by @ai-matrx/chat ``PROMOTED_WARNING_CODES``);
2. later loop iterations of the same request trim again and say nothing more (one line per turn);
3. a call that fits sends no line.
"""

from __future__ import annotations

import asyncio

import pytest
from matrx_connect.emitters.stream_emitter import StreamEmitter
from test_input_fit import (  # noqa: F401
    CONVERSATION_ID,
    REQUEST_ID,
    _clean,  # the autouse fixture that frees the fit seams
    _long_tool_loop,
)

from matrx_ai.config import context_preflight
from matrx_ai.config.context_preflight import estimate_prompt_tokens
from matrx_ai.config.input_fit import HISTORY_TRIMMED_CODE, HISTORY_TRIMMED_LINE
from matrx_ai.config.send_boundary import STAGE_LOOP, STAGE_RESOLVE, prepare_for_send
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context

DEVICE_MODEL = "qwen-3-4b"


def _device_chat():
    config = _long_tool_loop()
    config.model = config.matrx_model_name = DEVICE_MODEL
    return config


async def _send(config, *, stage: str, iteration: int | None) -> None:
    await prepare_for_send(
        config, stage=stage, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, iteration=iteration
    )
    for _ in range(5):  # the warning rides a detached task (send_client_warning)
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_a_trim_to_fit_the_device_window_is_said_in_one_line(monkeypatch) -> None:
    config = _device_chat()
    window = estimate_prompt_tokens(config) // 3
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: window)
    emitter = StreamEmitter()
    token = set_app_context(AppContext(user_id="u-1", emitter=emitter, metadata={}))
    try:
        await _send(config, stage=STAGE_RESOLVE, iteration=None)
        assert estimate_prompt_tokens(config) <= window, "the history was not made to fit"
        await _send(config, stage=STAGE_LOOP, iteration=2)
        await _send(config, stage=STAGE_LOOP, iteration=3)
        warnings = [w for w in emitter.take_warnings() if w["code"] == HISTORY_TRIMMED_CODE]
    finally:
        clear_app_context(token)
    assert len(warnings) == 1, f"expected one line for the trim, got {warnings}"
    assert warnings[0]["user_message"] == HISTORY_TRIMMED_LINE
    assert warnings[0].get("count", 1) == 1, "a later iteration said it again"


@pytest.mark.asyncio
async def test_a_call_that_fits_says_nothing() -> None:
    config = _device_chat()
    emitter = StreamEmitter()
    token = set_app_context(AppContext(user_id="u-1", emitter=emitter, metadata={}))
    try:
        await _send(config, stage=STAGE_RESOLVE, iteration=None)
        warnings = [w for w in emitter.take_warnings() if w["code"] == HISTORY_TRIMMED_CODE]
    finally:
        clear_app_context(token)
    assert warnings == []


@pytest.mark.asyncio
async def test_the_warning_text_is_a_short_summary_with_no_call_id_lists(monkeypatch) -> None:
    config = _device_chat()
    window = estimate_prompt_tokens(config) // 3
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: window)
    emitter = StreamEmitter()
    token = set_app_context(AppContext(user_id="u-1", emitter=emitter, metadata={}))
    try:
        await _send(config, stage=STAGE_RESOLVE, iteration=None)
        warnings = [w for w in emitter.take_warnings() if w["code"] == HISTORY_TRIMMED_CODE]
    finally:
        clear_app_context(token)
    assert len(warnings) == 1
    text = warnings[0]["system_message"]
    assert len(text) < 600, f"system_message is {len(text)} chars"
    assert "call_id" not in text and "rewritten_blocks" not in text
    assert "blocks_rewritten=" in text or "stubbed_blocks=" in text
