"""A call stopped while a model THINKS IN HIDING is billed for the thinking it did, not ~8 tokens.

Live run 5b068a57 (conversation e381441d, 2026-11-15 03:22Z): claude-haiku-5-5 hides its reasoning, so the
stream carried a "reasoning started" frame and then nothing for ~4.6 s until Stop. No reasoning text ever
streamed, so the estimate (visible text + streamed reasoning) was 0 and the adapter's ``message_start``
count of 8 output tokens stood: $0.000118, 3 points. At the model's measured ~213 output tokens/s the
provider generated ~980 thinking tokens and billed every one.

The rule: thinking tokens >= elapsed thinking time (reasoning-start frame -> stop) x the model's output
rate (catalog data, ``ai.offering.metadata.output_tokens_per_second``); with no catalog figure a stated
conservative default is used and the note says so. Streamed reasoning is part of that thinking, never
added on top of it. These drive the REAL dispatch seam (``UnifiedAIClient._dispatch_admitted``).
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.config import TokenUsage
from matrx_ai.providers.errors import attach_billed_usage, get_billed_usage
from matrx_ai.providers.stopped_usage import (
    DEFAULT_OUTPUT_TOKENS_PER_SECOND,
    stopped_output_estimate,
)
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile


class _HiddenThinkingEmitter:
    """The stream showed 'reasoning started' and then nothing: no text, no reasoning text."""

    def __init__(self, thinking_ms: int, reasoning_chars: int = 0) -> None:
        self.thinking_ms = thinking_ms
        self.reasoning_chars = reasoning_chars

    def get_turn_text(self) -> str:
        return ""

    def sent_text_snapshot(self) -> str:
        return ""

    def get_turn_reasoning_chars(self) -> int:
        return self.reasoning_chars

    def get_turn_thinking_ms(self) -> int:
        return self.thinking_ms


async def _stopped(emitter: Any, *, rate: float | None) -> TokenUsage:
    profile = make_profile(model_name="stop-test-model", wire_format="anthropic")
    if rate is not None:
        profile = profile.model_copy(update={"offering_metadata": {"output_tokens_per_second": rate}})
    started = asyncio.Event()
    partial = TokenUsage(input_tokens=665, output_tokens=8, matrx_model_name="stop-test-model", api="anthropic")

    async def dispatch() -> Any:
        try:
            started.set()
            await asyncio.sleep(30)
        except asyncio.CancelledError as cancel:
            attach_billed_usage(cancel, partial)  # message_start's count, all Anthropic ever sent
            raise

    token = set_app_context(AppContext(emitter=emitter, user_id="u", request_id="r", conversation_id="c"))  # type: ignore[arg-type]
    try:
        task = asyncio.ensure_future(
            UnifiedAIClient._dispatch_admitted(dispatch, profile=profile, provider_client=None, config=None)
        )
        await started.wait()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError as exc:
            usage = get_billed_usage(exc)
            assert isinstance(usage, TokenUsage)
            return usage
        raise AssertionError("the stopped call did not raise its cancellation")
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_a_call_stopped_during_hidden_thinking_is_billed_elapsed_time_times_the_models_rate():
    usage = await _stopped(_HiddenThinkingEmitter(thinking_ms=4600), rate=213.0)
    assert usage.output_tokens == round(4.6 * 213.0) == 980, usage.output_tokens
    note = usage.metadata["usage_estimated"]
    assert "hidden thinking" in note and "4.6 s" in note and "213" in note and "reported 8" in note


@pytest.mark.asyncio
async def test_without_a_catalog_rate_the_conservative_default_is_used_and_announced():
    usage = await _stopped(_HiddenThinkingEmitter(thinking_ms=4600), rate=None)
    assert usage.output_tokens == round(4.6 * DEFAULT_OUTPUT_TOKENS_PER_SECOND)
    assert "default" in usage.metadata["usage_estimated"]


@pytest.mark.asyncio
async def test_streamed_reasoning_is_part_of_the_thinking_never_added_on_top():
    streamed = "Weighing the regional figures against last quarter. " * 80  # ~4,200 chars, ~1,000 tokens
    streamed_tokens = stopped_output_estimate("", reasoning_chars=len(streamed))
    # 1 s of thinking at 213 tok/s is FEWER tokens than the reasoning that visibly streamed: the streamed count wins.
    usage = await _stopped(_HiddenThinkingEmitter(thinking_ms=1000, reasoning_chars=len(streamed)), rate=213.0)
    assert usage.output_tokens == streamed_tokens
    # 10 s at 213 tok/s exceeds it: the time estimate wins, and the streamed part is not counted twice.
    usage = await _stopped(_HiddenThinkingEmitter(thinking_ms=10_000, reasoning_chars=len(streamed)), rate=213.0)
    assert usage.output_tokens == 2130


@pytest.mark.asyncio
async def test_no_thinking_frame_means_no_thinking_estimate():
    usage = await _stopped(_HiddenThinkingEmitter(thinking_ms=0), rate=213.0)
    assert usage.output_tokens == 8, "no reasoning-start frame: nothing before the provider began is counted"


@pytest.mark.asyncio
async def test_every_emitter_clocks_this_turns_thinking_from_the_start_frame():
    from matrx_connect.emitters.console_emitter import ConsoleEmitter
    from matrx_connect.emitters.silent_emitter import SilentEmitter
    from matrx_connect.emitters.stream_emitter import StreamEmitter

    for emitter in (StreamEmitter(), SilentEmitter(), ConsoleEmitter()):
        name = type(emitter).__name__
        emitter.reset_turn_text()
        assert emitter.get_turn_thinking_ms() == 0, name
        await emitter.send_reasoning_state("started")
        await asyncio.sleep(0.12)
        open_ms = emitter.get_turn_thinking_ms()  # still thinking when Stop lands: counts up to now
        assert 100 <= open_ms < 1000, (name, open_ms)
        await emitter.send_reasoning_state("stopped")
        closed = emitter.get_turn_thinking_ms()
        await asyncio.sleep(0.05)
        assert emitter.get_turn_thinking_ms() == closed, f"{name}: a closed block stops the clock"
        emitter.reset_turn_text()
        assert emitter.get_turn_thinking_ms() == 0, f"{name}: the clock is per provider call"


@pytest.mark.asyncio
async def test_a_dispatched_call_whose_emitter_keeps_no_turn_text_is_still_billed_its_input():
    """Run 1aacd937 (2026-11-15): a stopped helper call's provider row carried no tokens and no cost. The seam
    returned early whenever the emitter had no ``get_turn_text`` (capture / tee / block emitters), so even a
    call that WAS dispatched was billed nothing. A dispatched call read its prompt; it is billed its input."""
    from types import SimpleNamespace

    from matrx_ai.config.context_preflight import estimate_prompt_tokens

    config = SimpleNamespace(system_instruction="You are a careful analyst. " * 200, messages=[])
    profile = make_profile(model_name="stop-test-model", wire_format="anthropic")
    started = asyncio.Event()

    async def dispatch() -> Any:
        started.set()
        await asyncio.sleep(30)

    token = set_app_context(AppContext(emitter=object(), user_id="u", request_id="r", conversation_id="c"))  # type: ignore[arg-type]
    try:
        task = asyncio.ensure_future(
            UnifiedAIClient._dispatch_admitted(dispatch, profile=profile, provider_client=None, config=config)
        )
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError) as caught:
            await task
    finally:
        clear_app_context(token)
    usage = get_billed_usage(caught.value)
    assert usage is not None, "a dispatched, stopped call read its prompt: it carries usage"
    assert usage.input_tokens == estimate_prompt_tokens(config) > 0
    assert usage.output_tokens == 0
