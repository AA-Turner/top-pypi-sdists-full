"""THE SUBSTITUTION IS PART OF THE ANSWER — a rerouted model leaves a record.

The live defect (2026-09-12, W69). Workflow runs 843d5847…, 94d48d9c… and
339bb4bf… each authored an ``ai.agent.tool_calling`` step naming
``claude-sonnet-5`` (ai.model_definition 617abdcd-79e2-4a4b-be76-4a9960cdffa1).
The Anthropic account was out of credit, so every call came back
``billing_error`` HTTP 400 ("Your credit balance is too low to access the
Anthropic API"), and the executor's reroute took the model row's
``retry_fallback_id`` = 49978747-… = ``gpt-4.1-2025-04-14``. The runs finished
"successfully" and the stored step output said only::

    usage.models = {"gpt-4.1-2025-04-14": {"api": "openai", ...}}

Nothing in the step's output, the run events, or the error surfaces said WHY a
model nobody chose had answered — the reroute existed only as a red terminal
block, a stream ``info`` event no workflow surface renders, and a note in the
request metadata nothing read back.

These are the two guards. Both FAIL on the code as it stood before the fix:

1. ``AiUsage.reroutes`` did not exist, and ``normalize_completed`` never read
   ``request.metadata["overload_reroutes"]`` — the step's stored output could
   not carry the substitution.
2. ``matrx_ai.orchestrator.reroute_alarm`` did not exist — no ``ops.system_error``
   row named the substitution, so an exhausted provider was not an alarm.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.graph_nodes.shared import AiUsage, normalize_completed
from matrx_ai.orchestrator.reroute_alarm import (
    PROVIDER_MODEL_SUBSTITUTED_KIND,
    PROVIDER_OFFERING_REROUTED_KIND,
    record_provider_reroute,
    reset_reported_reroutes,
)

# The live note the executor appended for these runs, verbatim in shape.
LIVE_NOTE: dict[str, Any] = {
    "kind": "overload_reroute",
    "scope": "model",
    "from_model": "617abdcd-79e2-4a4b-be76-4a9960cdffa1",
    "to_model": "49978747-e84d-4b26-baea-53b5a5380690",
    "from_offering_id": None,
    "to_offering_id": None,
    "attempts_on_model": 1,
    "error_type": "billing_error",
    "status_code": 400,
    "reason": (
        "'617abdcd-79e2-4a4b-be76-4a9960cdffa1' refused the call (billing_error, HTTP 400) "
        "after 1 attempt(s) — rerouting to retry_fallback "
        "'49978747-e84d-4b26-baea-53b5a5380690'"
    ),
}


def _completed(reroutes: list[dict[str, Any]] | None) -> Any:
    """A CompletedRequest-shaped stand-in carrying the executor's own note.

    Only the attributes ``normalize_completed`` reads are present — it is
    deliberately ``getattr``-defensive, so this exercises the real function.
    """
    metadata: dict[str, Any] = {"spec_type": "ai.agent.tool_calling"}
    if reroutes is not None:
        metadata["overload_reroutes"] = reroutes
    request = SimpleNamespace(
        conversation_id="c0ffee00-0000-4000-8000-000000000001",
        request_id="9a75a2ab-fb42-42a8-a3a9-56a4fbefa130",
        metadata=metadata,
        config=SimpleNamespace(messages=[]),
    )
    total = SimpleNamespace(input_tokens=22358, output_tokens=391, total_tokens=22749,
                            total_cost=0.047844)
    by_model = {
        "gpt-4.1-2025-04-14": SimpleNamespace(
            input_tokens=22358, output_tokens=391, total_tokens=22749,
            cost=0.047844, request_count=2, api="openai",
        )
    }
    return SimpleNamespace(
        request=request,
        final_response=SimpleNamespace(finish_reason="stop", messages=[]),
        total_usage=SimpleNamespace(total=total, by_model=by_model),
        timing_stats={},
        tool_call_stats={},
        iterations=2,
        metadata={"matrx_model_name": "gpt-4.1-2025-04-14"},
    )


class TestStepOutputCarriesTheSubstitution:
    def test_rerouted_run_names_the_model_it_asked_for(self):
        result = normalize_completed(_completed([LIVE_NOTE]))
        assert list(result.usage.models) == ["gpt-4.1-2025-04-14"], (
            "precondition: the usage block still names the model that RAN"
        )
        assert result.usage.reroutes, (
            "a run whose model was substituted must say so in its own output — "
            "usage.models alone cannot distinguish a choice from a downgrade"
        )
        note = result.usage.reroutes[0]
        assert note.from_model == LIVE_NOTE["from_model"]
        assert note.to_model == LIVE_NOTE["to_model"]
        assert note.error_type == "billing_error"
        assert note.status_code == 400
        assert "credit" in note.reason or "retry_fallback" in note.reason

    def test_normal_run_carries_no_reroutes(self):
        result = normalize_completed(_completed(None))
        assert result.usage.reroutes == [], (
            "the normal path must stay empty — a noisy field nobody can trust "
            "is the same as no field"
        )

    def test_malformed_note_never_breaks_a_finished_run(self):
        result = normalize_completed(_completed(["not-a-dict", {"scope": "model"}]))
        assert [n.to_model for n in result.usage.reroutes] == [""]

    def test_usage_default_is_empty(self):
        assert AiUsage().reroutes == []


class TestOperatorAlarm:
    @pytest.fixture(autouse=True)
    def _reset(self):
        reset_reported_reroutes()
        yield
        reset_reported_reroutes()

    def test_model_substitution_files_its_own_kind(self):
        assert record_provider_reroute(LIVE_NOTE) == PROVIDER_MODEL_SUBSTITUTED_KIND

    def test_offering_reroute_is_its_own_kind(self):
        note = dict(LIVE_NOTE, scope="offering", to_model=LIVE_NOTE["from_model"])
        assert record_provider_reroute(note) == PROVIDER_OFFERING_REROUTED_KIND

    def test_nothing_to_report_is_nothing_filed(self):
        assert record_provider_reroute(None) is None
        assert record_provider_reroute({}) is None

    def test_the_row_names_both_models_and_the_reason(self, monkeypatch):
        captured: list[dict[str, Any]] = []

        def _record_error(error, **kwargs):
            captured.append({"error": error, **kwargs})
            return None

        import matrx_ai._ext as ext

        monkeypatch.setattr(ext, "has_ext", lambda name: name == "record_error")
        monkeypatch.setattr(ext, "get_ext", lambda name: _record_error)

        record_provider_reroute(LIVE_NOTE, spec_type="ai.agent.tool_calling")

        assert captured, "the alarm must reach the host's ops.system_error door"
        row = captured[0]
        assert row["kind"] == PROVIDER_MODEL_SUBSTITUTED_KIND
        assert LIVE_NOTE["from_model"] in row["error_text"]
        assert LIVE_NOTE["to_model"] in row["error_text"]
        assert "retry_fallback_id" in row["error_text"]
        assert row["payload"]["reroute"]["error_type"] == "billing_error"
        assert row["route"] == "ai.agent.tool_calling"

    def test_one_row_per_class_per_process(self, monkeypatch):
        captured: list[Any] = []

        import matrx_ai._ext as ext

        monkeypatch.setattr(ext, "has_ext", lambda name: name == "record_error")
        monkeypatch.setattr(
            ext, "get_ext", lambda name: (lambda error, **kw: captured.append(kw))
        )

        for _ in range(5):
            record_provider_reroute(LIVE_NOTE)
        assert len(captured) == 1, (
            "one row per substitution class per process — ops.ops_issue_event "
            "already counts occurrences"
        )


class TestAggregatesKeepTheRecord:
    """A summed usage block must not lose the substitution on the way up.

    The podcast pipeline sums its stages into one usage aggregate. Dropping
    ``reroutes`` there would rebuild the same silence one layer higher: the
    run-level block would name only the models that ran.
    """

    def test_pipeline_aggregate_carries_every_stage_reroute(self):
        from matrx_ai.agent_runners.podcast_generator import (
            StageResult,
            _aggregate_stage_usage,
        )

        usage = {
            "input_tokens": 10,
            "output_tokens": 5,
            "total_tokens": 15,
            "cost_usd": 0.01,
            "models": {"gpt-4.1-2025-04-14": {"input_tokens": 10, "output_tokens": 5,
                                              "total_tokens": 15, "cost_usd": 0.01,
                                              "request_count": 1, "api": "openai"}},
            "reroutes": [LIVE_NOTE],
        }
        stage = StageResult(stage="create_script", success=True, output="s", usage=usage)
        aggregate = _aggregate_stage_usage([stage])
        assert aggregate is not None
        assert aggregate["reroutes"], "the run-level block must keep the substitution"
        assert aggregate["reroutes"][0]["to_model"] == LIVE_NOTE["to_model"]
