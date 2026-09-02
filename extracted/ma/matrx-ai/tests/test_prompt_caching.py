"""Anthropic prompt caching + the cache-observability guard.

The 2026-07 finding: Anthropic ``cached_input_tokens`` was ALWAYS 0 because the
translator never sent ``cache_control`` breakpoints — caching was never enabled.
These tests lock in three things so that class of failure stays dead:

1. The Anthropic translator emits ``cache_control`` breakpoints (system + rolling
   last message, or last tool when there is no system).
2. ``TokenUsage.from_anthropic`` accounts for cache read/write correctly (it must
   NOT subtract cache_read from Anthropic's already-cache-excluded input_tokens,
   and it must NOT drop cache_write from the bill).
3. The guard SCREAMS on system-prompt drift and on a zero-cache-read stable
   prefix, and stays SILENT when caching works.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import ModelPricing, PricingTier, TokenUsage, UnifiedConfig
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers import cache_guard
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile


def _profile():
    return make_profile(model_name="claude-x", wire_format="anthropic_chat")


# ─────────────────────────────────────────────────────────────────────────────
# 1. Translator emits cache_control breakpoints
# ─────────────────────────────────────────────────────────────────────────────


def _config_with_system() -> UnifiedConfig:
    return UnifiedConfig(
        model="claude-sonnet-5",
        system_instruction="You are a helpful assistant. " * 50,
        messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])],
    )


def test_system_block_carries_cache_control():
    payload = AnthropicTranslator().build_request(_config_with_system(), _profile())
    system = payload["system"]
    assert isinstance(system, list), "system must be a block array to carry cache_control"
    assert system[-1]["cache_control"] == {"type": "ephemeral"}
    assert "You are a helpful assistant." in system[-1]["text"]


def test_last_message_carries_rolling_cache_control():
    payload = AnthropicTranslator().build_request(_config_with_system(), _profile())
    last_block = payload["messages"][-1]["content"][-1]
    assert last_block["cache_control"] == {"type": "ephemeral"}


def test_rolling_breakpoint_skips_trailing_thinking_block():
    messages = [
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "visible answer"},
                {"type": "thinking", "thinking": "private reasoning", "signature": "sig"},
            ],
        }
    ]

    AnthropicTranslator._mark_last_message_cacheable(messages)

    assert messages[0]["content"][0]["cache_control"] == {"type": "ephemeral"}
    assert "cache_control" not in messages[0]["content"][1]


def test_rolling_breakpoint_omits_thinking_only_message():
    messages = [
        {
            "role": "assistant",
            "content": [
                {"type": "thinking", "thinking": "private reasoning", "signature": "sig"},
                {"type": "redacted_thinking", "data": "opaque"},
            ],
        }
    ]

    AnthropicTranslator._mark_last_message_cacheable(messages)

    assert all("cache_control" not in block for block in messages[0]["content"])


def test_no_system_puts_breakpoint_on_last_tool(monkeypatch):
    # Force build_provider_tools to yield a couple of plain tool declarations,
    # with no system prompt present.
    monkeypatch.setattr(
        AnthropicTranslator,
        "build_provider_tools",
        lambda self, config, provider: [
            {"name": "a", "input_schema": {"type": "object"}},
            {"name": "b", "input_schema": {"type": "object"}},
        ],
    )
    config = UnifiedConfig(
        model="claude-sonnet-5",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])],
    )
    payload = AnthropicTranslator().build_request(config, _profile())
    assert "system" not in payload
    tools = payload["tools"]
    assert "cache_control" not in tools[0]
    assert tools[-1]["cache_control"] == {"type": "ephemeral"}


def test_caching_can_be_disabled(monkeypatch):
    monkeypatch.setattr("matrx_ai.providers.anthropic.translator.PROMPT_CACHING_ENABLED", False)
    payload = AnthropicTranslator().build_request(_config_with_system(), _profile())
    assert isinstance(payload["system"], str), "disabled → plain string system, no breakpoints"
    assert "cache_control" not in payload["messages"][-1]["content"][-1]


# ─────────────────────────────────────────────────────────────────────────────
# 2. Usage accounting
# ─────────────────────────────────────────────────────────────────────────────


def test_from_anthropic_maps_cache_read_and_write():
    usage = {
        "input_tokens": 100,  # Anthropic: already EXCLUDES cache read + write
        "output_tokens": 20,
        "cache_read_input_tokens": 5000,
        "cache_creation_input_tokens": 800,
    }
    tu = TokenUsage.from_anthropic(usage, matrx_model_name="claude-sonnet-5")
    assert tu.cached_input_tokens == 5000, "cache_read → cached_input_tokens"
    # cache_write folded into billed input; cache_read NOT subtracted from input.
    assert tu.input_tokens == 100 + 800
    assert tu.output_tokens == 20
    assert tu.raw_usage["cache_read_input_tokens"] == 5000


def test_from_anthropic_records_hosted_search_as_billable_component():
    usage = {
        "input_tokens": 100,
        "output_tokens": 20,
        "server_tool_use": {"web_search_requests": 3},
    }

    token_usage = TokenUsage.from_anthropic(usage, matrx_model_name="claude-sonnet-5")

    assert token_usage.billing_components == {"service.web_search": 3}
    assert token_usage.raw_usage["server_tool_use"]["web_search_requests"] == 3


def test_hosted_search_component_is_included_in_exact_cost():
    usage = TokenUsage(
        input_tokens=1_000_000,
        output_tokens=0,
        matrx_model_name="claude-test",
        api="anthropic",
        billing_components={"service.web_search": 2},
    )
    pricing = {
        "claude-test": ModelPricing(
            model_name="claude-test",
            api="anthropic",
            tiers=[
                PricingTier(
                    max_tokens=None,
                    input_price=1.0,
                    output_price=0.0,
                    cached_input_price=0.0,
                    component_prices={"service.web_search": 10_000.0},
                )
            ],
        )
    }

    assert usage.calculate_cost(pricing) == pytest.approx(1.02)


def test_from_anthropic_no_cache_unchanged():
    usage = {"input_tokens": 100, "output_tokens": 20}
    tu = TokenUsage.from_anthropic(usage, matrx_model_name="claude-sonnet-5")
    assert tu.input_tokens == 100
    assert tu.cached_input_tokens == 0


def test_anthropic_cost_uses_distinct_cache_read_and_write_prices():
    usage = {
        "input_tokens": 2,
        "output_tokens": 467,
        "cache_read_input_tokens": 10_000,
        "cache_creation_input_tokens": 23_135,
        "cache_creation": {
            "ephemeral_5m_input_tokens": 23_135,
            "ephemeral_1h_input_tokens": 0,
        },
    }
    token_usage = TokenUsage.from_anthropic(usage, matrx_model_name="claude-sonnet-5")
    pricing = {
        "claude-sonnet-5": ModelPricing(
            "claude-sonnet-5",
            "anthropic",
            [
                PricingTier(
                    None,
                    input_price=3,
                    output_price=15,
                    cached_input_price=0.3,
                    cache_write_5m_price=3.75,
                    cache_write_1h_price=6,
                    cache_hit_price=0.3,
                )
            ],
        )
    }

    breakdown = token_usage.calculate_cost_breakdown(pricing)

    assert breakdown is not None
    assert breakdown.input_tokens == 2
    assert breakdown.cached_input_tokens == 10_000
    assert breakdown.cache_write_5m_tokens == 23_135
    assert breakdown.total_cost == pytest.approx(
        (2 * 3 + 10_000 * 0.3 + 23_135 * 3.75 + 467 * 15) / 1_000_000
    )


def test_anthropic_one_hour_cache_write_is_not_double_billed():
    usage = {
        "input_tokens": 2,
        "output_tokens": 3,
        "cache_creation_input_tokens": 1_000,
        "cache_creation": {"ephemeral_1h_input_tokens": 1_000},
    }
    pricing = {
        "claude-sonnet-5": ModelPricing(
            "claude-sonnet-5",
            "anthropic",
            [PricingTier(None, 3, 15, 0.3, cache_write_5m_price=3.75, cache_write_1h_price=6)],
        )
    }

    breakdown = TokenUsage.from_anthropic(
        usage, matrx_model_name="claude-sonnet-5"
    ).calculate_cost_breakdown(pricing)

    assert breakdown is not None
    assert breakdown.cache_write_5m_tokens == 0
    assert breakdown.cache_write_1h_tokens == 1_000
    assert breakdown.total_cost == pytest.approx((2 * 3 + 1_000 * 6 + 3 * 15) / 1_000_000)


# ─────────────────────────────────────────────────────────────────────────────
# 3. The guard
# ─────────────────────────────────────────────────────────────────────────────


class _Screams:
    """Capture vcprint calls so we can assert what the guard screamed."""

    def __init__(self):
        self.calls: list[tuple[str, str | None]] = []

    def __call__(self, *args, color=None, log_level=None, **kwargs):
        text = " ".join(str(a) for a in args)
        self.calls.append((text, color))

    def red_texts(self) -> list[str]:
        return [t for t, c in self.calls if c == "red"]

    def yellow_texts(self) -> list[str]:
        return [t for t, c in self.calls if c == "yellow"]


def _fresh_guard(monkeypatch) -> _Screams:
    screams = _Screams()
    monkeypatch.setattr(cache_guard, "vcprint", screams)
    cache_guard._LOOPS.clear()
    return screams


def test_extract_cache_metrics_anthropic():
    m = cache_guard.extract_cache_metrics(
        "anthropic",
        {
            "input_tokens": 100,
            "output_tokens": 20,
            "cache_read_input_tokens": 5000,
            "cache_creation_input_tokens": 800,
        },
    )
    assert m.cache_read == 5000
    assert m.cache_write == 800
    assert m.uncached_input == 100
    assert m.total_input == 5900


def test_guard_silent_when_caching_works(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    common = dict(
        provider="anthropic",
        model="claude-sonnet-5",
        conversation_id="conv-1",
        request_id="req-1",
        system_text="SYS " * 500,
        tool_names=("a", "b"),
    )
    # Call 0: cache write (creation), no read yet — legitimate.
    cache_guard.observe_cache_usage(
        raw_usage={"input_tokens": 20, "cache_creation_input_tokens": 6000}, **common
    )
    # Call 1: stable prefix → cache read present. No screams.
    cache_guard.observe_cache_usage(
        raw_usage={"input_tokens": 20, "cache_read_input_tokens": 6000}, **common
    )
    assert screams.red_texts() == []
    assert screams.yellow_texts() == []


def test_guard_screams_on_system_drift(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    base = dict(
        provider="anthropic",
        model="claude-sonnet-5",
        conversation_id="conv-2",
        request_id="req-2",
        tool_names=("a",),
    )
    cache_guard.observe_cache_usage(
        system_text="ORIGINAL SYSTEM " * 200,
        raw_usage={"input_tokens": 20, "cache_creation_input_tokens": 6000},
        **base,
    )
    # System prompt mutated between rounds — the cardinal violation.
    cache_guard.observe_cache_usage(
        system_text="MUTATED SYSTEM at " + "2026-07-07 " * 200,
        raw_usage={"input_tokens": 6000},
        **base,
    )
    reds = " ".join(screams.red_texts())
    assert "SYSTEM PROMPT MUTATED BETWEEN ROUNDS" in reds


def test_guard_does_not_compare_separate_requests_in_one_conversation(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    common = dict(
        provider="google",
        model="gemini-2.5-flash",
        conversation_id="conv-shared",
        tool_names=("a",),
        raw_usage={"prompt_token_count": 3000},
    )

    cache_guard.observe_cache_usage(
        request_id="request-first",
        system_text="FIRST TURN SYSTEM " * 200,
        **common,
    )
    cache_guard.observe_cache_usage(
        request_id="request-second",
        system_text="CONTINUATION SYSTEM " * 200,
        **common,
    )

    assert screams.red_texts() == []


def test_guard_does_not_compare_sibling_agent_loops_in_one_request(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    common = dict(
        provider="google",
        model="gemini-2.5-flash",
        request_id="shared-workflow-request",
        tool_names=("a",),
        raw_usage={"prompt_token_count": 3000},
    )

    cache_guard.observe_cache_usage(
        conversation_id="assessment-agent-loop",
        system_text="ASSESSMENT SYSTEM " * 200,
        **common,
    )
    cache_guard.observe_cache_usage(
        conversation_id="naming-agent-loop",
        system_text="NAMING SYSTEM " * 200,
        **common,
    )
    cache_guard.observe_cache_usage(
        conversation_id="lesson-agent-loop",
        system_text="LESSON SYSTEM " * 200,
        **common,
    )

    assert screams.red_texts() == []


@pytest.mark.asyncio
async def test_system_drift_creates_structured_error_without_prompt_text(monkeypatch):
    captured = []

    async def record_error(exc, **kwargs):
        captured.append((exc, kwargs))

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)

    await cache_guard._record_system_drift(
        provider="google",
        model="gemini-test",
        conversation_id="conv-structured",
        request_id="req-structured",
        call_index=1,
        prev_system="private previous prompt",
        new_system="private changed prompt",
    )

    assert len(captured) == 1
    _, details = captured[0]
    assert details["kind"] == "prompt_cache_system_drift"
    assert details["payload"]["request_id"] == "req-structured"
    assert "private" not in repr(details)


def test_guard_screams_on_zero_cache_read_stable_prefix(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    common = dict(
        provider="anthropic",
        model="claude-sonnet-5",
        conversation_id="conv-3",
        request_id="req-3",
        system_text="SYS " * 500,
        tool_names=("a", "b"),
    )
    cache_guard.observe_cache_usage(raw_usage={"input_tokens": 6000}, **common)
    # Identical prefix, big prompt, yet zero cache read → broken caching.
    cache_guard.observe_cache_usage(raw_usage={"input_tokens": 6000}, **common)
    reds = " ".join(screams.red_texts())
    assert "ZERO CACHE READ ON A STABLE PREFIX" in reds


def test_guard_does_not_scream_when_anthropic_refreshes_expired_cache(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    common = dict(
        provider="anthropic",
        model="claude-opus-5",
        conversation_id="conv-cache-refresh",
        request_id="req-cache-refresh",
        system_text="SYS " * 500,
        tool_names=("a", "b"),
    )

    cache_guard.observe_cache_usage(
        raw_usage={"input_tokens": 2, "cache_creation_input_tokens": 277_659},
        **common,
    )
    state = next(iter(cache_guard._LOOPS.values()))
    state.last_call_ts -= 290.2
    cache_guard.observe_cache_usage(
        raw_usage={"input_tokens": 2, "cache_creation_input_tokens": 277_659},
        **common,
    )

    assert screams.red_texts() == []


def test_guard_does_not_scream_below_haiku_45_cache_floor(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    common = dict(
        provider="anthropic",
        model="claude-haiku-4-5-20251001",
        conversation_id="conv-haiku-floor",
        request_id="req-haiku-floor",
        system_text="SYS " * 500,
        tool_names=("a", "b"),
    )

    cache_guard.observe_cache_usage(raw_usage={"input_tokens": 3256}, **common)
    cache_guard.observe_cache_usage(raw_usage={"input_tokens": 3256}, **common)

    assert screams.red_texts() == []


@pytest.mark.asyncio
async def test_genuine_cache_miss_creates_structured_error(monkeypatch):
    captured = []

    async def record_error(exc, **kwargs):
        captured.append((exc, kwargs))

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)

    await cache_guard._record_cache_miss(
        provider="anthropic",
        model="claude-haiku-4-5-20251001",
        conversation_id="conv-cache-miss",
        request_id="req-cache-miss",
        call_index=1,
        metrics=cache_guard.CacheMetrics(
            provider="anthropic", uncached_input=5000, cache_read=0, cache_write=0
        ),
        cacheable_threshold=4096,
    )

    assert len(captured) == 1
    _, details = captured[0]
    assert details["kind"] == "prompt_cache_read_missing"
    assert details["payload"]["cacheable_threshold"] == 4096
    assert details["payload"]["request_id"] == "req-cache-miss"


def test_guard_does_not_treat_google_implicit_cache_miss_as_failure(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    common = dict(
        provider="google",
        model="gemini-2.5-flash",
        conversation_id="conv-google",
        request_id="req-google",
        system_text="SYS " * 1200,
        tool_names=("a", "b"),
    )
    usage = {"prompt_token_count": 4800, "cached_content_token_count": None}

    cache_guard.observe_cache_usage(raw_usage=usage, **common)
    cache_guard.observe_cache_usage(raw_usage=usage, **common)

    assert screams.red_texts() == []


def test_guard_tool_drift_is_yellow_not_red(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    base = dict(
        provider="anthropic",
        model="claude-sonnet-5",
        conversation_id="conv-4",
        request_id="req-4",
        system_text="SYS " * 500,
    )
    cache_guard.observe_cache_usage(
        tool_names=("a",),
        raw_usage={"input_tokens": 20, "cache_creation_input_tokens": 6000},
        **base,
    )
    # Tool set changed (legitimate dynamic injection) → yellow notice, and no
    # cache-miss red because the prefix legitimately changed this turn.
    cache_guard.observe_cache_usage(
        tool_names=("a", "b"),
        raw_usage={"input_tokens": 6000},
        **base,
    )
    assert any("TOOL SET CHANGED" in t for t in screams.yellow_texts())
    assert screams.red_texts() == []


def test_guard_no_scream_below_threshold(monkeypatch):
    screams = _fresh_guard(monkeypatch)
    common = dict(
        provider="anthropic",
        model="claude-sonnet-5",
        conversation_id="conv-5",
        request_id="req-5",
        system_text="tiny",
        tool_names=(),
    )
    # Small prompts legitimately don't cache — never scream.
    cache_guard.observe_cache_usage(raw_usage={"input_tokens": 50}, **common)
    cache_guard.observe_cache_usage(raw_usage={"input_tokens": 50}, **common)
    assert screams.red_texts() == []
