"""A stopped stream is billed for the text it generated, never left at ~0 tokens.

T4-C (2026-11-14): Stop cuts the provider stream before its usage block arrives. Anthropic's adapter
kept only ``message_start``'s count (8 output tokens beside a 4,983-character reply, $0.000118);
OpenAI-compatible adapters kept nothing (no provider, no tokens, $0) — 172 of 189 stopped provider
rows in 7 days had no cost. These drive the REAL dispatch seam (``UnifiedAIClient._dispatch_admitted``)
with a provider call that streams text and is then cancelled the way ``_execute_stoppable`` cancels
it, and read the usage the seam leaves on the cancellation.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.config import ModelPricing, PricingTier, TokenUsage
from matrx_ai.providers.errors import attach_billed_usage, get_billed_usage
from matrx_ai.providers.stopped_usage import stopped_output_estimate
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile

REPLY = "The quarterly figures show steady growth across every region we track. " * 70  # ~5,000 chars


class _Emitter:
    def __init__(self) -> None:
        self.text = ""

    def get_turn_text(self) -> str:
        return self.text

    def sent_text_snapshot(self) -> str:
        return self.text[: len(self.text) - 10]


def _pricing(model: str) -> dict[str, ModelPricing]:
    # Keyed by the offering that served the call — the stopped usage names it, as a reported one does.
    return {
        f"test-offering:{model}": ModelPricing(
            model_name=model,
            api="openai",
            tiers=[PricingTier(max_tokens=None, input_price=1.0, output_price=4.0, cached_input_price=0.1)],
        )
    }


async def _stopped_call(
    emitter: _Emitter, *, partial: TokenUsage | None, streams: bool = True, config: Any = None
) -> BaseException:
    profile = make_profile(model_name="stop-test-model", wire_format="openai_chat")
    streamed = asyncio.Event()

    async def dispatch() -> Any:
        try:
            if streams:
                emitter.text = REPLY  # the provider streamed this, then the person pressed Stop
            streamed.set()
            await asyncio.sleep(30)
        except asyncio.CancelledError as cancel:
            attach_billed_usage(cancel, partial)  # what the adapter had seen (often nothing)
            raise

    ctx = AppContext(emitter=emitter, user_id="u", request_id="r", conversation_id="c")  # type: ignore[arg-type]
    token = set_app_context(ctx)
    try:
        task = asyncio.ensure_future(
            UnifiedAIClient._dispatch_admitted(dispatch, profile=profile, provider_client=None, config=config)
        )
        await streamed.wait()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError as exc:
            return exc
        raise AssertionError("the stopped call did not raise its cancellation")
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_a_stopped_call_with_no_usage_block_is_billed_from_its_streamed_text():
    exc = await _stopped_call(_Emitter(), partial=None)
    usage = get_billed_usage(exc)
    assert usage is not None, "a stopped call that streamed 5,000 characters must carry usage, not nothing"
    expected = stopped_output_estimate(REPLY)
    assert expected > 1000
    assert usage.output_tokens == expected
    assert usage.matrx_model_name == "stop-test-model"
    assert usage.metadata.get("usage_estimated")
    assert (usage.calculate_cost(_pricing("stop-test-model")) or 0) > 0


@pytest.mark.asyncio
async def test_a_stopped_call_whose_adapter_saw_only_the_start_count_is_raised_to_the_estimate():
    partial = TokenUsage(input_tokens=656, output_tokens=8, cached_input_tokens=4799,
                         matrx_model_name="stop-test-model", api="anthropic")
    exc = await _stopped_call(_Emitter(), partial=partial)
    usage = get_billed_usage(exc)
    assert usage is partial
    assert usage.output_tokens == stopped_output_estimate(REPLY) > 8
    assert usage.input_tokens == 656, "the provider's own input count stays"
    assert "reported 8" in usage.metadata["usage_estimated"]


@pytest.mark.asyncio
async def test_a_provider_count_above_the_estimate_is_never_lowered():
    partial = TokenUsage(input_tokens=10, output_tokens=50_000, matrx_model_name="stop-test-model", api="openai")
    exc = await _stopped_call(_Emitter(), partial=partial)
    assert get_billed_usage(exc).output_tokens == 50_000
    assert "usage_estimated" not in get_billed_usage(exc).metadata


@pytest.mark.asyncio
async def test_a_call_stopped_before_its_first_token_is_still_billed_for_the_input_it_read():
    from types import SimpleNamespace

    from matrx_ai.config.context_preflight import estimate_prompt_tokens

    config = SimpleNamespace(system_instruction="You are a careful analyst. " * 200, messages=[])
    expected_input = estimate_prompt_tokens(config)
    assert expected_input > 0
    exc = await _stopped_call(_Emitter(), partial=None, streams=False, config=config)
    usage = get_billed_usage(exc)
    assert usage is not None, "the provider read the prompt; a stop before the first token still costs its input"
    assert usage.input_tokens == expected_input
    assert usage.output_tokens == 0
    assert "0 generated characters" in usage.metadata["usage_estimated"]
    assert (usage.calculate_cost(_pricing("stop-test-model")) or 0) > 0


@pytest.mark.asyncio
async def test_a_stop_before_the_first_token_never_lowers_an_input_count_the_provider_gave():
    from types import SimpleNamespace

    partial = TokenUsage(input_tokens=90_000, output_tokens=0, matrx_model_name="stop-test-model", api="openai")
    config = SimpleNamespace(system_instruction="short", messages=[])
    exc = await _stopped_call(_Emitter(), partial=partial, streams=False, config=config)
    assert get_billed_usage(exc).input_tokens == 90_000


THINKING = "Let me weigh each region's figures against last quarter before answering. " * 60  # ~4,400 chars


class _ThinkingEmitter(_Emitter):
    """A stream stopped while the model was still THINKING: reasoning streamed, no visible text yet."""

    def __init__(self) -> None:
        super().__init__()
        self.reasoning_chars = 0

    def get_turn_reasoning_chars(self) -> int:
        return self.reasoning_chars


@pytest.mark.asyncio
async def test_a_call_stopped_while_thinking_is_billed_for_the_reasoning_it_streamed():
    """Live run a90b318b (2026-11-15): stopped mid-thinking, billed 8 output tokens (3 points) — the
    estimate counted only visible text. Reasoning tokens are output tokens the provider bills."""
    emitter = _ThinkingEmitter()
    emitter.reasoning_chars = len(THINKING)
    partial = TokenUsage(input_tokens=656, output_tokens=8, matrx_model_name="stop-test-model", api="anthropic")
    exc = await _stopped_call(emitter, partial=partial, streams=False)
    usage = get_billed_usage(exc)
    expected = stopped_output_estimate("", reasoning_chars=len(THINKING))
    assert expected == stopped_output_estimate(THINKING) > 500
    assert usage.output_tokens == expected
    assert "reasoning" in usage.metadata["usage_estimated"]


@pytest.mark.asyncio
async def test_reasoning_and_visible_text_both_count():
    emitter = _ThinkingEmitter()
    emitter.reasoning_chars = len(THINKING)
    exc = await _stopped_call(emitter, partial=None)
    usage = get_billed_usage(exc)
    assert usage.output_tokens == stopped_output_estimate(REPLY, reasoning_chars=len(THINKING))
    assert usage.output_tokens > stopped_output_estimate(REPLY)


@pytest.mark.asyncio
async def test_every_emitter_counts_the_reasoning_it_streamed_per_turn():
    from matrx_connect.emitters.console_emitter import ConsoleEmitter
    from matrx_connect.emitters.silent_emitter import SilentEmitter
    from matrx_connect.emitters.stream_emitter import StreamEmitter

    for emitter in (StreamEmitter(), SilentEmitter(), ConsoleEmitter()):
        emitter.reset_turn_text()
        await emitter.send_reasoning_chunk("abcd")
        await emitter.send_reasoning_chunk("efgh")
        assert emitter.get_turn_reasoning_chars() == 8, type(emitter).__name__
        emitter.reset_turn_text()
        assert emitter.get_turn_reasoning_chars() == 0, type(emitter).__name__
