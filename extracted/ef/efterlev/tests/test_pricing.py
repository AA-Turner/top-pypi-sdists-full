"""Tests for `efterlev.llm.pricing` (Tier 1 #2a, v0.1.19).

Locks the pricing table's shape and behavior. Numeric pricing values
themselves drift over time as Anthropic adjusts rates; tests assert
the structure (lookup behavior, bedrock-detection, cost arithmetic)
not the dollar amounts so a future pricing update doesn't break tests
that just need the table updated.
"""

from __future__ import annotations

from efterlev.llm.pricing import (
    ModelPrice,
    estimate_cost_usd,
    is_bedrock_model,
    lookup,
)


def test_lookup_returns_modelprice_for_known_anthropic_models() -> None:
    """The two model IDs the codebase actually invokes are registered."""
    for model_id in ("claude-opus-4-7", "claude-sonnet-4-6"):
        price = lookup(model_id)
        assert price is not None, f"{model_id} should be in the pricing table"
        assert isinstance(price, ModelPrice)
        assert price.input_per_mtok_usd > 0
        assert price.output_per_mtok_usd > 0
        # Output should always cost more than input for Anthropic frontier models.
        assert price.output_per_mtok_usd > price.input_per_mtok_usd
        # `as_of` is an ISO date string.
        assert len(price.as_of) == 10
        assert price.as_of[4] == "-" and price.as_of[7] == "-"


def test_lookup_returns_modelprice_for_known_bedrock_models() -> None:
    """Bedrock IDs are aliased to the same Anthropic rate (we use it as
    a proxy and qualify with `via bedrock` in the cost summary suffix)."""
    for model_id in (
        "us.anthropic.claude-opus-4-7-v1:0",
        "us.anthropic.claude-sonnet-4-6-v1:0",
    ):
        price = lookup(model_id)
        assert price is not None
        assert price.model_id == model_id


def test_lookup_returns_none_for_unregistered_model() -> None:
    """Unregistered models don't crash — the cost summary falls back
    to tokens-only with a `pricing not registered` suffix. Test the
    contract: lookup returns None."""
    assert lookup("claude-future-model") is None
    assert lookup("") is None
    assert lookup("gpt-99-future-model") is None


def test_estimate_cost_usd_arithmetic() -> None:
    """1M input + 1M output tokens on a known model equals
    input_per_mtok + output_per_mtok in dollars."""
    price = lookup("claude-sonnet-4-6")
    assert price is not None
    cost = estimate_cost_usd("claude-sonnet-4-6", 1_000_000, 1_000_000)
    assert cost is not None
    assert abs(cost - (price.input_per_mtok_usd + price.output_per_mtok_usd)) < 0.001


def test_estimate_cost_usd_returns_none_for_unregistered_model() -> None:
    """Unregistered model → no cost. Tested separately from lookup
    because callers use this as the single-call API."""
    assert estimate_cost_usd("unknown-model", 1000, 1000) is None


def test_lookup_resolves_openai_dated_snapshot_to_base_alias() -> None:
    """OpenAI Chat Completions reports the served model as a dated snapshot
    (e.g. 'gpt-5.4-mini-2026-03-17') even when the request used the base
    alias. lookup must price it via the base alias rather than returning
    None ('pricing not registered' in the cost summary). Regression for the
    cost-rollup gap surfaced by the 2026-05-29 OpenAI validation run."""
    base = lookup("gpt-5.4-mini")
    snapshot = lookup("gpt-5.4-mini-2026-03-17")
    assert base is not None
    assert snapshot is not None
    assert snapshot.input_per_mtok_usd == base.input_per_mtok_usd
    assert snapshot.output_per_mtok_usd == base.output_per_mtok_usd
    # estimate_cost_usd works through the same path.
    assert estimate_cost_usd("gpt-5.4-mini-2026-03-17", 1_000_000, 0) is not None


def test_lookup_dated_snapshot_of_unregistered_base_still_none() -> None:
    """Stripping the date must not invent a price for an unregistered base."""
    assert lookup("gpt-99-future-2026-03-17") is None


def test_lookup_resolves_bare_bedrock_id_without_version_suffix() -> None:
    """AWS Bedrock cross-region inference profiles invoke WITH or WITHOUT the
    trailing `-v1:0` version segment. The table keys the versioned form; the
    bare form must price the same. Regression for the govnotes-demo validation
    (2026-06-07) where `--llm-model us.anthropic.claude-sonnet-4-6` (no
    `-v1:0`) produced NO cost line because the bare ID missed the table."""
    versioned = lookup("us.anthropic.claude-sonnet-4-6-v1:0")
    bare = lookup("us.anthropic.claude-sonnet-4-6")
    assert versioned is not None
    assert bare is not None
    assert bare.input_per_mtok_usd == versioned.input_per_mtok_usd
    assert bare.output_per_mtok_usd == versioned.output_per_mtok_usd
    # Opus + Haiku bare forms resolve too.
    assert lookup("us.anthropic.claude-opus-4-7") is not None
    assert lookup("us.anthropic.claude-haiku-4-5-20251001") is not None
    # estimate_cost_usd works through the same path — a real 613K/127K gap run
    # on bare-ID Sonnet prices to several dollars, not nothing.
    cost = estimate_cost_usd("us.anthropic.claude-sonnet-4-6", 613_330, 126_760)
    assert cost is not None
    assert cost > 1.0


def test_lookup_bare_bedrock_id_of_unregistered_model_still_none() -> None:
    """Version-stripping must not invent a price for an unregistered Bedrock ID."""
    assert lookup("us.anthropic.claude-future-9-9") is None


def test_bedrock_openai_models_registered_and_treated_as_bedrock() -> None:
    """The Mantle model IDs (`openai.gpt-5.4` / `openai.gpt-5.5`) have pricing
    and are recognized as Bedrock-served (for the `via bedrock` cost suffix)."""
    from efterlev.llm.pricing import is_bedrock_model

    for model_id in ("openai.gpt-5.4", "openai.gpt-5.5"):
        price = lookup(model_id)
        assert price is not None, f"{model_id} should be priced"
        assert price.input_per_mtok_usd > 0
        assert is_bedrock_model(model_id), f"{model_id} should be treated as Bedrock-served"


def test_is_bedrock_model_recognizes_aws_prefix() -> None:
    """AWS Bedrock model IDs carry a `us.anthropic.` or `anthropic.`
    prefix; the cost summary uses this signal to decide whether to
    append the `via bedrock` clarifier."""
    assert is_bedrock_model("us.anthropic.claude-opus-4-7-v1:0")
    assert is_bedrock_model("us.anthropic.claude-sonnet-4-6-v1:0")
    assert is_bedrock_model("anthropic.claude-3-haiku-20240307-v1:0")
    # Anthropic API IDs are NOT bedrock.
    assert not is_bedrock_model("claude-opus-4-7")
    assert not is_bedrock_model("claude-sonnet-4-6")
    assert not is_bedrock_model("")
