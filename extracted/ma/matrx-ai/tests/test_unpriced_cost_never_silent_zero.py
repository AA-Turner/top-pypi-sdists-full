"""THE guard for the unpriced-spend class.

Root cause (2026-09-12): every consumer of measured usage wrote the same line —
``totals.total_cost or 0`` / ``usage.calculate_cost()`` passed straight into a
meter. ``total_cost`` is deliberately ``None`` when ANY call in a run could not
be priced from the catalog, and ``calculate_cost()`` is ``None`` when the
offering has no pricing row. Both collapsed to a believable **$0** on the spend
ledger, so real money read as free work: 139 zero-cost ``internal_agent_run``
rows and 5 zero-cost ``audio_transcription`` rows in the live 30-day window.

The fix is the two builders below, and this file is the forcing function: it
FAILS against the old ``or 0`` behaviour, because the old behaviour produced a
meter indistinguishable from a genuinely-free call.

Proven failing-then-passing: reverting either builder to `or 0` makes
`test_unknown_total_cost_is_not_a_silent_zero` and
`test_missing_catalog_price_is_not_a_silent_zero` fail on the missing
`unpriced_calls` key.
"""

from __future__ import annotations

from matrx_ai.config.usage_config import (
    UNPRICED_CALLS_METER,
    TokenUsage,
    UsageTotals,
    cost_meters_from_totals,
    cost_meters_from_usage,
)


def test_unknown_total_cost_is_not_a_silent_zero() -> None:
    """A run with 2 unpriceable calls out of 5 must NOT report a complete bill."""
    totals = UsageTotals(
        input_tokens=1000,
        output_tokens=200,
        total_requests=5,
        total_cost=None,          # the honest "unknown"
        known_cost_subtotal=1.25,  # what we DID price
        unknown_cost_requests=2,
    )
    meters = cost_meters_from_totals(totals, label="guard")

    # The old `or 0` produced exactly {"usd": 0, ...} — a free-looking run.
    assert meters["usd"] == 1.25, "the known subtotal is the floor, never 0"
    assert meters[UNPRICED_CALLS_METER] == 2, (
        "an unpriced call MUST appear as a meter; without it the ledger cannot "
        "be told apart from genuinely free work"
    )


def test_fully_priced_run_carries_no_unpriced_meter() -> None:
    totals = UsageTotals(
        input_tokens=10, output_tokens=3, total_requests=2,
        total_cost=0.5, known_cost_subtotal=0.5, unknown_cost_requests=0,
    )
    meters = cost_meters_from_totals(totals)
    assert meters["usd"] == 0.5
    assert UNPRICED_CALLS_METER not in meters, (
        "a fully priced run must stay clean — the marker means something"
    )


def test_missing_catalog_price_is_not_a_silent_zero() -> None:
    """A single call whose model has no pricing row records a HOLE, not $0."""
    usage = TokenUsage(
        input_tokens=100,
        output_tokens=0,
        matrx_model_name="model-with-no-pricing-row-xyz",
        api="some_api",
    )
    assert usage.calculate_cost() is None, "fixture must be genuinely unpriceable"

    meters = cost_meters_from_usage(usage, label="guard", audio_seconds=12.5)
    assert meters[UNPRICED_CALLS_METER] == 1
    assert meters["audio_seconds"] == 12.5, "caller quantities survive the builder"


def test_no_usage_object_at_all_is_not_a_silent_zero() -> None:
    """Providers that return raw bytes and NO usage block (several TTS APIs)."""
    meters = cost_meters_from_usage(None, label="guard", characters=42)
    assert meters[UNPRICED_CALLS_METER] == 1
    assert meters["characters"] == 42


def test_none_totals_yields_no_meters() -> None:
    """No usage aggregate at all is 'nothing measured', not 'measured as zero'."""
    assert cost_meters_from_totals(None) == {}
