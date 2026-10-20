"""The PAYBACK cache gate: a warm-cache trim runs only when it pays for its rewrite.

A trim rewrites history, so every token after its first rewritten block is
written again at the cache-WRITE price. Cora's 2026-10-15 Opus 5.5 job paid
~1046 ¢ of such rewrites to free context worth at most ~271 ¢ (common-docs
projects/agent-evaluation/research/real-jobs-cache-review.md). ``payback``
holds a warm trim unless
    freed × read × expected_remaining_calls ≥ rewrite × (write − read)
and takes held trims at the next cold cache, or at once near the window.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

import matrx_ai.config.context_preflight as preflight
import matrx_ai.config.usage_config as usage_config
from matrx_ai.config import ToolCallContent, ToolResultContent, UnifiedMessage
from matrx_ai.config.cache_marks import history_cache_ttl
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.config.usage_config import ModelPricing, PricingTier

CONVERSATION_ID = "conv-trim-payback"
REQUEST_ID = "req-trim-payback"
MODEL = "claude-opus-5-5"

OPUS_55 = ModelPricing(
    model_name=MODEL,
    api="anthropic",
    tiers=[
        PricingTier(
            max_tokens=None,
            input_price=4.0,
            output_price=20.0,
            cached_input_price=0.20,
            cache_write_5m_price=5.00,
            cache_write_1h_price=8.00,
            cache_hit_price=0.20,
        )
    ],
)
GPT = ModelPricing(
    model_name="gpt-x",
    api="openai",
    tiers=[PricingTier(max_tokens=None, input_price=1.25, output_price=10.0, cached_input_price=0.125)],
)


def _result(chars: int, position: int) -> UnifiedMessage:
    return UnifiedMessage(
        role="tool",
        position=position,
        content=[
            ToolResultContent(
                tool_use_id=f"call-{position}",
                name="records",
                content="x" * chars,
                output_chars=chars,
            )
        ],
    )


def _serial(sizes: list[int]) -> list[UnifiedMessage]:
    """A serial loop: each result is followed by the assistant turn that acted on
    it (distance is counted in model iterations since 2026-10-17)."""
    out: list[UnifiedMessage] = []
    for i, chars in enumerate(sizes):
        out.append(_result(chars, len(out)))
        if i < len(sizes) - 1:
            out.append(
                UnifiedMessage(
                    role="assistant",
                    position=len(out),
                    content=[ToolCallContent(id=f"next-{i}", name="records", arguments={})],
                )
            )
    return out


def _config(sizes: list[int], *, model: str = MODEL, long_cache: bool = False) -> SimpleNamespace:
    return SimpleNamespace(
        messages=_serial(sizes),
        system_instruction=None,
        tools=None,
        prompt_cache_key=None,
        model=model,
        matrx_model_name=model,
        routing_offering_id=None,
        extended_prompt_cache=long_cache,
    )


def _mid_loop(**kw) -> SimpleNamespace:
    # Cora's shape: two 9K results just scrolled past tier 1 (12 positions = 6
    # iterations back), and a long, heavy tail after them that a trim would force
    # the provider to write again. Legacy takes it (~6.2K tokens freed ≥ 5000).
    return _config([500, 9_000, 9_000] + [16_000] * 6, **kw)


def _turn_start_giant() -> SimpleNamespace:
    # Two huge stale results with a light tail: the 434-648K-char turn-start
    # trims that were good.
    return _config([300_000, 300_000] + [200] * 6)


def _state(age_secs: float, *, ttl: int = 300, provider: str = "anthropic") -> dict:
    return {
        "last_response_at": (datetime.now(UTC) - timedelta(seconds=age_secs)).isoformat(),
        "last_provider": provider,
        "est_cache_ttl_secs": ttl,
    }


def _payback(**over) -> TrimPolicy:
    return TrimPolicy(cache_gate_mode="payback", **over)


@pytest.fixture(autouse=True)
def _catalog(monkeypatch):
    lookup = {MODEL: OPUS_55, "gpt-x": GPT}
    windows = {MODEL: 1_000_000, "gpt-x": 1_000_000}
    monkeypatch.setattr(usage_config, "_get_db_pricing_lookup", lambda: lookup)
    monkeypatch.setattr(preflight, "_declared_window", lambda ref: windows.get(ref))
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    yield windows
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)


async def _send(config, state, policy):
    return await prepare_for_send(
        config,
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=3,
        cache_state=state,
        policy=policy,
    )


@pytest.mark.asyncio
async def test_warm_small_trim_is_held_under_payback_but_taken_by_legacy() -> None:
    legacy = await _send(_mid_loop(), _state(5), TrimPolicy())
    assert legacy.trim_report.blocks_rewritten == 2  # the old rule pays the rewrite

    config = _mid_loop()
    prep = await _send(config, _state(5), _payback())
    report = prep.trim_report
    gate = report.policy["cache_gate"]
    assert report.blocks_rewritten == 0
    assert report.eligible_but_skipped_reason == "cache_protect"
    assert (gate["mode"], gate["rule"], gate["decision"]) == ("payback", "payback", "hold")
    assert gate["rewrite_cost_usd"] > gate["benefit_usd"] > 0
    assert gate["rewrite_tokens"] > gate["est_savings_tokens"]
    assert gate["inputs"]["write_price"] == 5.00 and gate["inputs"]["read_price"] == 0.20
    assert gate["est_savings_chars"] == 18_000  # feeds cumulative_trimmable_chars
    assert "tool result cleared" not in str(config.messages[2].content[0].content)


@pytest.mark.asyncio
async def test_warm_big_trim_is_taken_under_payback() -> None:
    prep = await _send(_turn_start_giant(), _state(5), _payback())
    gate = prep.trim_report.policy["cache_gate"]
    assert prep.trim_report.blocks_rewritten == 2
    assert (gate["rule"], gate["decision"]) == ("payback", "take")
    assert gate["benefit_usd"] >= gate["rewrite_cost_usd"]


@pytest.mark.asyncio
async def test_cold_cache_trims_exactly_like_legacy() -> None:
    prep = await _send(_mid_loop(), _state(3_600), _payback())
    gate = prep.trim_report.policy["cache_gate"]
    assert prep.trim_report.blocks_rewritten == 2
    assert (gate["rule"], gate["decision"]) == ("cold_cache", "take")


@pytest.mark.asyncio
async def test_payback_treats_the_margin_band_before_expiry_as_warm() -> None:
    # Cora 2026-10-18: age 263 s of a 300 s TTL (> 0.8 x TTL) was called cold and a
    # live cache was rewritten. Payback: warm until age >= TTL; legacy unchanged.
    payback = await _send(_mid_loop(), _state(263), _payback())
    gate = payback.trim_report.policy["cache_gate"]
    assert (gate["rule"], gate["decision"]) == ("payback", "hold")
    assert payback.trim_report.blocks_rewritten == 0

    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    legacy = await _send(_mid_loop(), _state(263), TrimPolicy())
    assert legacy.trim_report.policy["cache_gate"]["rule"] == "cold_cache"
    assert legacy.trim_report.blocks_rewritten == 2

    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    expired = await _send(_mid_loop(), _state(301), _payback())
    assert expired.trim_report.policy["cache_gate"]["rule"] == "cold_cache"


@pytest.mark.asyncio
async def test_near_the_window_forces_the_held_trim(_catalog) -> None:
    # The mid-loop prompt is ~41K estimated tokens; a 46K window puts it past
    # 85% of the pre-flight ceiling, so holding could cause a refusal.
    _catalog[MODEL] = 46_000
    prep = await _send(_mid_loop(), _state(5), _payback())
    gate = prep.trim_report.policy["cache_gate"]
    assert prep.trim_report.blocks_rewritten == 2
    assert (gate["rule"], gate["decision"]) == ("forced_near_limit", "take")
    assert gate["inputs"]["estimated_prompt_tokens"] >= gate["force_at_tokens"]


@pytest.mark.asyncio
async def test_unpriced_model_falls_back_to_the_legacy_floor_out_loud() -> None:
    prep = await _send(_mid_loop(model="no-such-model"), _state(5), _payback())
    gate = prep.trim_report.policy["cache_gate"]
    assert gate["rule"] == "payback_unpriced:legacy_floor"
    assert prep.trim_report.blocks_rewritten == 2


@pytest.mark.asyncio
async def test_a_one_hour_cache_ttl_keeps_the_cache_warm_past_five_minutes() -> None:
    # A wire whose history really lives an hour (est_cache_ttl_secs=3600, no
    # mark fact overriding it): 20 minutes later the cache is still warm, so the
    # small trim is held — a 5-minute assumption would have rebuilt it.
    config = _mid_loop(model="gpt-x")
    prep = await _send(config, _state(1_200, ttl=3_600, provider="openai"), _payback())
    gate = prep.trim_report.policy["cache_gate"]
    assert gate["cache_ttl_secs"] == 3_600
    assert (gate["rule"], gate["decision"]) == ("payback", "hold")
    # No write premium on this wire: a rewrite is billed as fresh input.
    assert gate["inputs"]["write_price"] == 1.25


@pytest.mark.asyncio
async def test_anthropic_long_cache_history_is_still_the_five_minute_tier() -> None:
    # Long cache puts ttl "1h" on the system/template marks only; the rolling
    # history mark stays 5m (Anthropic orders 1h marks before 5m marks). So a
    # trim rewrites at the 5m price, and history 10 minutes old is COLD even
    # when a stale state claims an hour.
    assert history_cache_ttl("anthropic", long=True) == (300, "5m", 3_600)
    prep = await _send(_mid_loop(long_cache=True), _state(600, ttl=3_600), _payback())
    gate = prep.trim_report.policy["cache_gate"]
    assert gate["inputs"]["long_cache"] is True
    assert gate["inputs"]["rewrite_ttl_secs"] == 300
    assert (gate["rule"], gate["decision"]) == ("cold_cache", "take")


def test_mode_knob_refuses_an_unknown_value() -> None:
    from matrx_ai.config.context_trim import trim_policy_from_knobs

    values = {
        "tier_1_min_positions_back": 12,
        "tier_1_min_output_chars": 8000,
        "tier_2_min_positions_back": 24,
        "tier_2_min_output_chars": 2000,
        "cache_gate_min_saved_tokens": 5000,
        "payback_expected_remaining_calls": 20,
        "payback_force_window_percent": 85,
        "cache_gate_mode": "payback",
    }
    assert trim_policy_from_knobs(values).cache_gate_mode == "payback"
    with pytest.raises(ValueError):
        trim_policy_from_knobs({**values, "cache_gate_mode": "sometimes"})
