"""GATE 2 may reject a script — it may NEVER discard what the script cost.

The third podcast billing-undercount incident: ``_validated_script_stage``
built its ``StageResult`` by hand and simply never passed ``usage=``, so
``create_script`` — the single most expensive agent in the pipeline — recorded
ZERO cost on EVERY podcast run ever made. Nothing failed; the run just showed
a fraction of its real spend, and S6's per-arm cost audit is what finally
caught it (verified across the 5 most recent live runs, 2026-08-15).

The rule these tests force: **a wrapper that receives an already-paid
``AgentRunResult`` propagates its usage on every path it can return through —
success, validation rejection, and agent failure alike.** A GATE-2 rejection
does not refund the tokens the agent already burned.
"""

from __future__ import annotations

from matrx_ai.agent_runners.podcast_generator import (
    InputDataType,
    PodcastRequest,
    PodcastType,
    SpeakerSpec,
    _validated_script_stage,
)
from matrx_ai.config.usage_config import (
    AggregatedUsage,
    ModelUsageSummary,
    UsageTotals,
)


class _FakeAgentRunResult:
    """The only three attributes ``_validated_script_stage`` reads."""

    def __init__(self, *, success: bool, output: str, error: str | None = None):
        self.success = success
        self.output = output
        self.error = error
        self.usage_aggregated = AggregatedUsage(
            by_model={
                "m1": ModelUsageSummary(
                    input_tokens=1000, output_tokens=500, total_tokens=1500, cost=0.0421
                )
            },
            total=UsageTotals(
                input_tokens=1000, output_tokens=500, total_tokens=1500, total_cost=0.0421
            ),
        )


_GOOD_SCRIPT = (
    "<podcast_dialogue>\nAlice: Welcome to the show.\nBob: Glad to be here.\n</podcast_dialogue>"
)
# Two speakers requested, ONE delivered — a real GATE 2 rejection.
_CAST_VIOLATING_SCRIPT = "<podcast_dialogue>\nAlice: I am alone here.\n</podcast_dialogue>"


def _request() -> PodcastRequest:
    return PodcastRequest(
        show_id="s6-harness-test",
        input_data_type=InputDataType.TOPIC,
        podcast_type=PodcastType.EDUCATIONAL,
        host_count=2,
        speakers=[SpeakerSpec(name="Alice"), SpeakerSpec(name="Bob")],
    )


def test_a_PASSING_script_carries_the_agents_cost():
    stage = _validated_script_stage(
        _FakeAgentRunResult(success=True, output=_GOOD_SCRIPT), _request()
    )
    assert stage.success is True
    assert stage.usage is not None, "create_script recorded no cost for a paid agent call"
    assert stage.usage["cost_usd"] == 0.0421
    assert stage.usage["total_tokens"] == 1500


def test_a_GATE_2_REJECTED_script_still_carries_the_agents_cost():
    """The rejection is free; the agent call that produced it was not."""
    stage = _validated_script_stage(
        _FakeAgentRunResult(success=True, output=_CAST_VIOLATING_SCRIPT), _request()
    )
    assert stage.success is False
    assert stage.usage is not None, "a rejected script silently refunded its own tokens"
    assert stage.usage["cost_usd"] == 0.0421


def test_a_FAILED_script_agent_still_carries_its_cost():
    stage = _validated_script_stage(
        _FakeAgentRunResult(success=False, output="", error="provider 500"), _request()
    )
    assert stage.success is False
    assert stage.usage is not None
    assert stage.usage["cost_usd"] == 0.0421
