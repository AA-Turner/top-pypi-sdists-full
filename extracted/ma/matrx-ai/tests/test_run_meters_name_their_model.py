"""A run's settle meters name the model that spent the money, and carry its cached tokens.

2026-10-09: internal agent runs (``internal_agent_run``) settled meters of only
``{usd, input_tokens, output_tokens}``. They write no ``chat.request``, so the usage rules
source had nothing to read a model from: 236 runs on 2026-10-07 ($33.95, 894k output tokens)
were booked to no provider and no model, and an Admin API reconciliation by model reported them
as unrecorded Anthropic spend. Cached input was dropped from the meters as well.

The guard: the meters built from a run's aggregated usage carry ``model`` + ``provider`` (the
model that cost the most) and ``cached_tokens``, while the quantities stay numeric.
"""

from __future__ import annotations

from matrx_ai.config.usage_config import (
    AggregatedUsage,
    ModelUsageSummary,
    UsageTotals,
    cost_meters_from_aggregate,
)


def _agg() -> AggregatedUsage:
    return AggregatedUsage(
        by_model={
            "claude-haiku-4-5": ModelUsageSummary(
                input_tokens=900, output_tokens=40, api="anthropic", request_count=3, cost=0.002
            ),
            "claude-opus-5-5": ModelUsageSummary(
                input_tokens=12000, output_tokens=5100, cached_input_tokens=30000,
                api="anthropic", request_count=4, cost=0.41,
            ),
        },
        total=UsageTotals(
            input_tokens=12900, output_tokens=5140, cached_input_tokens=30000,
            total_requests=7, total_cost=0.412, known_cost_subtotal=0.412,
        ),
    )


def test_meters_name_the_costliest_model_and_its_provider() -> None:
    meters = cost_meters_from_aggregate(_agg(), label="t")
    assert meters["model"] == "claude-opus-5-5"
    assert meters["provider"] == "anthropic"


def test_meters_carry_cached_tokens_and_keep_quantities_numeric() -> None:
    meters = cost_meters_from_aggregate(_agg(), label="t")
    assert meters["cached_tokens"] == 30000
    assert meters["usd"] == 0.412
    assert meters["input_tokens"] == 12900 and meters["output_tokens"] == 5140


def test_a_run_with_no_usage_has_no_meters() -> None:
    assert cost_meters_from_aggregate(None) == {}


def test_single_call_meters_name_their_model() -> None:
    from matrx_ai.config.usage_config import TokenUsage, cost_meters_from_usage

    usage = TokenUsage(input_tokens=10, output_tokens=5, matrx_model_name="gemini-3.8-flash", api="google")
    meters = cost_meters_from_usage(usage, label="t")
    assert meters["model"] == "gemini-3.8-flash" and meters["provider"] == "google"
