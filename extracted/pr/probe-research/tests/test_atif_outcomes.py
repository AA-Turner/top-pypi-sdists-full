"""Operational outcomes for ATIF-imported turns and tool calls.

Three axes are kept apart and these tests exist to hold them apart:

  lifecycle   `span.status` — running vs over
  outcome     `attributes.outcome` — succeeded / failed / unknown
  quality     reward, verifier score — never a turn or tool property

ATIF has no outcome field in any version Harbor 0.21 accepts, so an outcome is
producer-specific by construction. The evidence behind every rule here is in
docs/2026-08-24-atif-operational-outcomes.md; the short version is that
`ObservationResult.extra.tool_result_is_error` is the only authoritative
per-invocation signal any pinned producer emits, and prose is never a signal.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from tests.conftest import open_run

from probe.connectors.atif import (
    OUTCOME_FAILED,
    OUTCOME_SUCCEEDED,
    OUTCOME_UNKNOWN,
    RULE_CHILD_FAILED,
    RULE_CHILDREN_ALL_SUCCEEDED,
    RULE_CONFLICT,
    RULE_EXPLICIT_CALL,
    RULE_EXPLICIT_RESULT,
    RULE_EXPLICIT_TURN,
    RULE_MIXED_CHILDREN,
    RULE_NO_SIGNAL,
    RULE_TRIAL_EXCEPTION,
    expand_trajectory,
    parse_atif,
)
from probe.connectors.harbor import capture_trial

FIXTURES = Path(__file__).parent / "fixtures" / "atif"
OUTCOMES_FIXTURE = FIXTURES / "synthetic-outcomes.trajectory.json"
#: Everything Harbor's own terminus-2 wrote, which is every fixture except the
#: one we authored to carry outcome fields at all.
LEGACY_GOLDEN = sorted(
    path
    for path in FIXTURES.glob("*.trajectory*.json")
    if path != OUTCOMES_FIXTURE
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def _by_path(doc: dict) -> dict:
    return {plan.path: plan for plan in parse_atif(doc)}


def _doc(*steps: dict, agent: dict | None = None) -> dict:
    return {
        "schema_version": "ATIF-v1.7",
        "agent": agent or {"name": "test-producer", "version": "1.0.0"},
        "steps": list(steps),
    }


def _agent_step(step_id: int, **kw) -> dict:
    return {"step_id": step_id, "source": "agent", "message": "", **kw}


def _call(call_id: str, **kw) -> dict:
    return {
        "tool_call_id": call_id,
        "function_name": "Bash",
        "arguments": {},
        **kw,
    }


def _result(call_id: str | None, content: str = "out", **kw) -> dict:
    return {"source_call_id": call_id, "content": content, **kw}


# -- explicit signals, with provenance -------------------------------------------
def test_explicit_structured_failure_is_recorded_with_its_source():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={
                "results": [_result("c1", extra={"tool_result_is_error": True})]
            },
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_FAILED
    assert call["outcome_rule"] == RULE_EXPLICIT_RESULT
    assert (
        call["outcome_source"]
        == "observation.results[].extra.tool_result_is_error"
    )
    assert call["outcome_producer"] == "test-producer"
    assert call["outcome_producer_version"] == "1.0.0"


def test_explicit_structured_success_is_recorded_with_its_source():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={
                "results": [_result("c1", extra={"tool_result_is_error": False})]
            },
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_SUCCEEDED
    assert call["outcome_rule"] == RULE_EXPLICIT_RESULT
    assert (
        call["outcome_source"]
        == "observation.results[].extra.tool_result_is_error"
    )


def test_explicit_false_is_a_success_signal_not_an_absent_one():
    """`false` is the producer SAYING it worked. A truthiness test would read it
    as absence and drop 484 of the 570 stated results in production."""
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={"results": [_result("c1", extra={"is_error": False})]},
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_SUCCEEDED
    assert call["outcome_source"] == "observation.results[].extra.is_error"


@pytest.mark.parametrize("value", [0, 1, "true", "false", "", None, [], {}])
def test_only_real_booleans_are_read_as_an_outcome(value):
    """A producer writing an int or a string has not stated an outcome in a
    vocabulary we can prove. Coercing it would invent one."""
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={
                "results": [_result("c1", extra={"tool_result_is_error": value})]
            },
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_UNKNOWN
    assert call["outcome_rule"] == RULE_NO_SIGNAL
    assert "outcome_source" not in call


def test_invocation_scope_flag_is_read_when_the_result_states_nothing():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1", extra={"tool_use_is_error": True})],
            observation={"results": [_result("c1")]},
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_FAILED
    assert call["outcome_rule"] == RULE_EXPLICIT_CALL
    assert call["outcome_source"] == "tool_calls[].extra.tool_use_is_error"


# -- absence stays absent ---------------------------------------------------------
def test_missing_outcome_metadata_stays_unknown():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={"results": [_result("c1", extra={"latency_ms": 12})]},
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_UNKNOWN
    assert call["outcome_rule"] == RULE_NO_SIGNAL
    assert "outcome_source" not in call


def test_a_result_existing_is_not_success_and_a_result_missing_is_not_failure():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("with_result"), _call("without_result")],
            observation={"results": [_result("with_result", "lots of output")]},
        )
    )
    plans = _by_path(doc)
    assert plans["turn/1/call/0"].attributes["outcome"] == OUTCOME_UNKNOWN
    assert plans["turn/1/call/1"].attributes["outcome"] == OUTCOME_UNKNOWN


def test_lifecycle_completed_without_execution_evidence_stays_unknown():
    """Every planned span is `status="completed"` — that is lifecycle, and it is
    the default. It must never become an outcome."""
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={"results": [_result("c1")]},
        )
    )
    for plan in parse_atif(doc):
        assert plan.status == "completed"
        assert plan.attributes["outcome"] == OUTCOME_UNKNOWN


def test_a_producer_status_string_is_never_an_outcome():
    """Codex writes the Responses API item status, which reports that ARGUMENT
    GENERATION completed — not that the tool ran, let alone succeeded."""
    doc = _doc(
        _agent_step(
            1,
            extra={"tool_call_details": {"c1": {"status": "completed"}}},
            tool_calls=[_call("c1", extra={"status": "completed"})],
            observation={"results": [_result("c1", extra={"status": "completed"})]},
        )
    )
    plans = _by_path(doc)
    assert plans["turn/1/call/0"].attributes["outcome"] == OUTCOME_UNKNOWN
    assert plans["turn/1"].attributes["outcome"] == OUTCOME_UNKNOWN


# -- prose is never a signal -------------------------------------------------------
def test_prose_saying_error_does_not_override_an_explicit_success():
    """163 real results are explicitly `is_error: false` while their text
    contains "error"/"failed"/"traceback" — git output, diffs, log tails."""
    doc = _load(OUTCOMES_FIXTURE)
    call = _by_path(doc)["turn/2/call/0"].attributes
    assert "ERROR" in call["result"] and "Traceback" in call["result"]
    assert call["outcome"] == OUTCOME_SUCCEEDED
    assert call["outcome_rule"] == RULE_EXPLICIT_RESULT


def test_prose_saying_passed_without_structured_metadata_stays_unknown():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={"results": [_result("c1", "2 passed in 0.10s")]},
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert "2 passed" in call["result"]
    assert call["outcome"] == OUTCOME_UNKNOWN


def test_a_message_only_turn_is_not_successful_however_it_reads():
    doc = _load(OUTCOMES_FIXTURE)
    turn = _by_path(doc)["turn/5"].attributes
    assert "everything succeeded" in turn["message"]
    assert turn["outcome"] == OUTCOME_UNKNOWN
    assert turn["outcome_rule"] == RULE_NO_SIGNAL


def test_the_trajectory_continuing_is_not_evidence_the_turn_succeeded():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={"results": [_result("c1")]},
        ),
        _agent_step(2, message="carrying on"),
    )
    plans = _by_path(doc)
    assert plans["turn/1"].attributes["outcome"] == OUTCOME_UNKNOWN
    assert plans["turn/2"].attributes["outcome"] == OUTCOME_UNKNOWN


# -- correlation, never position ----------------------------------------------------
def test_parallel_results_bind_by_id_not_by_list_position():
    """The fixture returns `call_b`'s failure BEFORE `call_a`'s success. A
    positional zip would swap them. 74 steps in the real sample issue 2-5 calls."""
    plans = _by_path(_load(OUTCOMES_FIXTURE))
    first, second = plans["turn/3/call/0"], plans["turn/3/call/1"]
    assert first.attributes["tool_call_id"] == "call_a"
    assert first.attributes["outcome"] == OUTCOME_SUCCEEDED
    assert second.attributes["tool_call_id"] == "call_b"
    assert second.attributes["outcome"] == OUTCOME_FAILED


def test_an_unmatched_result_cannot_speak_for_a_sibling_call():
    """An ATIF result with no `source_call_id` came from an action outside the
    tool-calling format. Its metadata is preserved and never derived from."""
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={
                "results": [
                    _result(None, "system note", extra={"tool_result_is_error": True})
                ]
            },
        )
    )
    plans = _by_path(doc)
    assert plans["turn/1/call/0"].attributes["outcome"] == OUTCOME_UNKNOWN
    turn = plans["turn/1"].attributes
    assert turn["outcome"] == OUTCOME_UNKNOWN
    # preserved, not dropped — it was being discarded entirely before
    assert "tool_result_is_error" in turn["observation_extra"]


def test_a_result_for_an_unknown_call_id_contaminates_nothing():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={
                "results": [_result("ghost", extra={"tool_result_is_error": True})]
            },
        )
    )
    plans = _by_path(doc)
    assert plans["turn/1/call/0"].attributes["outcome"] == OUTCOME_UNKNOWN
    assert plans["turn/1"].attributes["outcome"] == OUTCOME_UNKNOWN


# -- conflict --------------------------------------------------------------------
def test_conflicting_signals_refuse_rather_than_pick_a_winner():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1", extra={"tool_use_is_error": True})],
            observation={
                "results": [_result("c1", extra={"tool_result_is_error": False})]
            },
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_UNKNOWN
    assert call["outcome_rule"] == RULE_CONFLICT
    # both disagreeing fields are named, so the refusal is auditable
    assert "tool_result_is_error=succeeded" in call["outcome_source"]
    assert "tool_use_is_error=failed" in call["outcome_source"]


def test_two_results_for_one_call_that_disagree_also_refuse():
    """ATIF puts no uniqueness constraint on `source_call_id` and Harbor's
    copilot converter appends results onto the issuing step, so one call can
    carry several. Keeping only the last would resolve a disagreement by
    arrival order."""
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={
                "results": [
                    _result("c1", "partial", extra={"tool_result_is_error": True}),
                    _result("c1", "final", extra={"tool_result_is_error": False}),
                ]
            },
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_UNKNOWN
    assert call["outcome_rule"] == RULE_CONFLICT
    # content still takes the last result — only the outcome reads them all
    assert call["result"] == "final"


def test_agreeing_duplicate_results_still_resolve():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={
                "results": [
                    _result("c1", "partial", extra={"tool_result_is_error": True}),
                    _result("c1", "final", extra={"tool_result_is_error": True}),
                ]
            },
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_FAILED
    assert call["outcome_rule"] == RULE_EXPLICIT_RESULT


def test_two_disagreeing_keys_in_one_extra_also_refuse():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("c1")],
            observation={
                "results": [
                    _result(
                        "c1", extra={"tool_result_is_error": True, "is_error": False}
                    )
                ]
            },
        )
    )
    call = _by_path(doc)["turn/1/call/0"].attributes
    assert call["outcome"] == OUTCOME_UNKNOWN
    assert call["outcome_rule"] == RULE_CONFLICT


# -- turn aggregation ---------------------------------------------------------------
def test_turn_succeeds_only_when_every_child_states_success():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("a"), _call("b")],
            observation={
                "results": [
                    _result("a", extra={"tool_result_is_error": False}),
                    _result("b", extra={"tool_result_is_error": False}),
                ]
            },
        )
    )
    turn = _by_path(doc)["turn/1"].attributes
    assert turn["outcome"] == OUTCOME_SUCCEEDED
    assert turn["outcome_rule"] == RULE_CHILDREN_ALL_SUCCEEDED


def test_one_failed_child_fails_the_turn():
    turn = _by_path(_load(OUTCOMES_FIXTURE))["turn/3"].attributes
    assert turn["outcome"] == OUTCOME_FAILED
    assert turn["outcome_rule"] == RULE_CHILD_FAILED


def test_a_known_success_beside_an_unknown_leaves_the_turn_unknown():
    turn = _by_path(_load(OUTCOMES_FIXTURE))["turn/4"].attributes
    assert turn["outcome"] == OUTCOME_UNKNOWN
    assert turn["outcome_rule"] == RULE_MIXED_CHILDREN


def test_a_proven_failure_survives_an_unknown_sibling():
    """Success needs unanimity; failure does not. One proven failure is positive
    evidence that something in this turn failed, whatever the silent sibling did."""
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("bad"), _call("quiet")],
            observation={
                "results": [
                    _result("bad", extra={"tool_result_is_error": True}),
                    _result("quiet"),
                ]
            },
        )
    )
    turn = _by_path(doc)["turn/1"].attributes
    assert turn["outcome"] == OUTCOME_FAILED
    assert turn["outcome_rule"] == RULE_CHILD_FAILED


def test_a_turn_with_no_tool_calls_reports_absence_not_a_mixture():
    doc = _doc(_agent_step(1, message="thinking out loud"))
    turn = _by_path(doc)["turn/1"].attributes
    assert turn["outcome"] == OUTCOME_UNKNOWN
    assert turn["outcome_rule"] == RULE_NO_SIGNAL


def test_an_explicit_turn_success_cannot_overrule_a_failed_child():
    """The one direction an explicit turn flag does NOT win. A producer saying
    "the turn was fine" while one of its calls explicitly failed is the exact
    false-green this attribute exists to prevent."""
    doc = _doc(
        _agent_step(
            1,
            extra={"is_error": False},
            tool_calls=[_call("a")],
            observation={
                "results": [_result("a", extra={"tool_result_is_error": True})]
            },
        )
    )
    plans = _by_path(doc)
    turn = plans["turn/1"].attributes
    assert turn["outcome"] == OUTCOME_UNKNOWN
    assert turn["outcome_rule"] == RULE_CONFLICT
    assert "succeeded" in turn["outcome_source"]
    assert "failed" in turn["outcome_source"]
    # the child keeps its own proven failure
    assert plans["turn/1/call/0"].attributes["outcome"] == OUTCOME_FAILED


def test_a_result_scoped_key_is_not_read_at_turn_scope():
    """`tool_result_is_error` names a RESULT. Finding it on a step and calling
    the meaning proven would be reading a scope the name does not claim."""
    doc = _doc(_agent_step(1, extra={"tool_result_is_error": True}))
    turn = _by_path(doc)["turn/1"].attributes
    assert turn["outcome"] == OUTCOME_UNKNOWN
    assert turn["outcome_rule"] == RULE_NO_SIGNAL


def test_a_repeated_tool_call_id_makes_correlation_ambiguous():
    """ATIF does not require call ids to be unique within a step. Handing both
    calls the same result would let one success mark two invocations."""
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("same"), _call("same")],
            observation={
                "results": [_result("same", extra={"tool_result_is_error": False})]
            },
        )
    )
    plans = _by_path(doc)
    for path in ("turn/1/call/0", "turn/1/call/1"):
        assert plans[path].attributes["outcome"] == OUTCOME_UNKNOWN
    assert plans["turn/1"].attributes["outcome"] == OUTCOME_UNKNOWN


def test_a_hostile_producer_name_cannot_bloat_every_span():
    doc = _doc(
        _agent_step(1, tool_calls=[_call("a")]),
        agent={"name": "x" * 5000, "version": "y" * 5000},
    )
    for plan in parse_atif(doc):
        assert len(plan.attributes["outcome_producer"]) == 120
        assert len(plan.attributes["outcome_producer_version"]) == 120


def test_an_explicit_turn_failure_has_turn_scope_and_outranks_its_children():
    """No pinned producer emits one; the rule exists so a fork that does is
    honored. A turn can fail for a reason that is not one of its tools."""
    doc = _doc(
        _agent_step(
            1,
            extra={"is_error": True},
            tool_calls=[_call("a")],
            observation={"results": [_result("a", extra={"tool_result_is_error": False})]},
        )
    )
    plans = _by_path(doc)
    turn = plans["turn/1"].attributes
    assert turn["outcome"] == OUTCOME_FAILED
    assert turn["outcome_rule"] == RULE_EXPLICIT_TURN
    assert turn["outcome_source"] == "steps[].extra.is_error"
    # scoped to the turn: the child keeps what its own result stated
    assert plans["turn/1/call/0"].attributes["outcome"] == OUTCOME_SUCCEEDED


# -- subagents stay scoped ------------------------------------------------------------
def test_subagent_outcomes_do_not_leak_into_the_delegating_turn():
    doc = _doc(
        _agent_step(
            1,
            tool_calls=[_call("spawn", function_name="spawn_subagent")],
            observation={
                "results": [
                    _result(
                        "spawn",
                        subagent_trajectory_ref=[{"trajectory_id": "sub-a"}],
                    )
                ]
            },
        )
    )
    doc["subagent_trajectories"] = [
        {
            "schema_version": "ATIF-v1.7",
            "trajectory_id": "sub-a",
            "agent": {"name": "worker", "version": "0.1.0"},
            "steps": [
                _agent_step(
                    1,
                    tool_calls=[_call("inner")],
                    observation={
                        "results": [
                            _result("inner", extra={"tool_result_is_error": True})
                        ]
                    },
                )
            ],
        }
    ]
    plans = _by_path(doc)
    inner = plans["turn/1/call/0/sub/sub-a/turn/1"].attributes
    assert inner["outcome"] == OUTCOME_FAILED
    assert inner["outcome_producer"] == "worker"
    # the wrapper is a container, and the delegating turn/call saw no statement
    wrapper = plans["turn/1/call/0/sub/sub-a"].attributes
    assert wrapper["outcome"] == OUTCOME_UNKNOWN
    assert plans["turn/1/call/0"].attributes["outcome"] == OUTCOME_UNKNOWN
    assert plans["turn/1"].attributes["outcome"] == OUTCOME_UNKNOWN


# -- legacy goldens -------------------------------------------------------------------
@pytest.mark.parametrize(
    "path", LEGACY_GOLDEN, ids=[p.name for p in LEGACY_GOLDEN]
)
def test_goldens_keep_their_tree_shape_and_take_neutral_outcomes(path):
    """Harbor's upstream terminus-2 goldens carry no outcome field of any kind.
    Every span must stay `completed` lifecycle and `unknown` outcome — and the
    tree must not move."""
    doc = _load(path)
    plans = parse_atif(doc)
    assert plans, path.name
    paths = [plan.path for plan in plans]
    assert paths == sorted(set(paths), key=paths.index)  # no duplicates
    seen: set[str] = set()
    for plan in plans:
        assert plan.parent_path is None or plan.parent_path in seen
        seen.add(plan.path)
        assert plan.status == "completed"
        assert plan.attributes["outcome"] == OUTCOME_UNKNOWN
        assert plan.attributes["outcome_rule"] in {
            RULE_NO_SIGNAL,
            RULE_MIXED_CHILDREN,
        }
        assert "outcome_source" not in plan.attributes


# -- the two write paths agree ----------------------------------------------------------
def _outcomes(spans: list[dict]) -> dict:
    return {
        s["external_key"]: (
            s["attributes"].get("outcome"),
            s["attributes"].get("outcome_rule"),
            s["attributes"].get("outcome_source"),
        )
        for s in spans
        if s["span_type"] in {"turn", "tool_call"}
    }


def _write_trial(root: Path, *, exception: bool = False, reward: float = 1.0) -> Path:
    root.mkdir(parents=True)
    result: dict = {"trial_name": "t__1", "verifier_result": {"reward": reward}}
    if exception:
        result["exception_info"] = {
            "exception_type": "TimeoutError",
            "exception_message": "agent exceeded its budget",
            "exception_traceback": "…",
            "occurred_at": "2026-08-24T10:05:00Z",
        }
    (root / "result.json").write_text(json.dumps(result))
    (root / "trajectory.json").write_text(OUTCOMES_FIXTURE.read_text())
    return root


def test_capture_time_and_retroactive_expansion_agree(
    client, app, tmp_path, monkeypatch
):
    """`probe trial expand` reads only the stored trajectory artifact — it never
    sees result.json or native logs. Every rule must therefore be derivable from
    the ATIF document alone, or the two paths would disagree."""
    import importlib

    cli_main = importlib.import_module("probe.cli.main")
    client.fail_open = False

    eager = open_run(client, experiment="e", name="eager")
    capture_trial(eager, _write_trial(tmp_path / "a"), step_index=7, strict=True)
    at_capture = _outcomes(app.spans[eager.id])

    # Both trials carry byte-identical trajectories, which is the point — but
    # the upload door is content-addressed, so the second one would dedupe to
    # `have: true` and never land a blob the retroactive path could read back.
    app.uploaded.clear()
    late = open_run(client, experiment="e", name="late")
    result = capture_trial(
        late, _write_trial(tmp_path / "b"), step_index=7, expand=False, strict=True
    )
    # The CLI owns its client and closes it on exit, so it goes last.
    monkeypatch.setattr(cli_main, "_client", lambda: client)
    cli_main.trial_expand(late.id, result["manifest"]["id"], max_spans=0)
    retroactive = _outcomes(app.spans[late.id])

    assert at_capture and at_capture == retroactive
    assert OUTCOME_FAILED in {outcome for outcome, _, _ in at_capture.values()}
    assert OUTCOME_SUCCEEDED in {outcome for outcome, _, _ in at_capture.values()}


def test_re_expansion_updates_in_place_without_duplicating(client, app, tmp_path):
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    doc = _load(OUTCOMES_FIXTURE)
    root = run.span("rollout", name="t")
    expand_trajectory(run, doc, root_span_id=root, trial="t__1", max_spans=0, strict=True)
    first = _outcomes(app.spans[run.id])
    ids_once = [s["id"] for s in app.spans[run.id] if s["span_type"] != "rollout"]
    # The parse must not emit the same id twice in ONE batch either — that is a
    # real duplicate, unlike the two-batch case below.
    assert len(ids_once) == len(set(ids_once))

    expand_trajectory(run, doc, root_span_id=root, trial="t__1", max_spans=0, strict=True)
    spans = app.spans[run.id]
    ids_twice = [s["id"] for s in spans if s["span_type"] != "rollout"]
    # The fake server APPENDS rather than upserting, so the second batch's rows
    # are still in the list; the real server's `ON CONFLICT (id) DO UPDATE`
    # collapses them. What idempotence means through this harness is that the
    # second pass introduced no NEW id — every row it wrote lands on one that
    # already existed — and that the values it wrote are identical.
    assert set(ids_twice) == set(ids_once)
    assert len(ids_twice) == 2 * len(ids_once)  # appended, not id-duplicated
    assert _outcomes(spans) == first


# -- trial scope stays at trial scope ------------------------------------------------------
def test_reward_zero_without_an_exception_is_not_an_operational_failure(
    client, app, tmp_path
):
    """107 of the 412 rollouts in production completed with reward 0 and no
    exception. Reward is task quality, on its own axis."""
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    capture_trial(run, _write_trial(tmp_path / "t", reward=0.0), strict=True)
    rollout = next(s for s in app.spans[run.id] if s["span_type"] == "rollout")
    assert rollout["status"] == "completed"
    assert rollout["attributes"]["reward"] == 0.0
    assert rollout["attributes"]["outcome"] == OUTCOME_UNKNOWN
    assert rollout["attributes"]["outcome_rule"] == RULE_NO_SIGNAL


def test_a_malformed_but_present_exception_still_fails_the_rollout(
    client, app, tmp_path
):
    """`exception_info: {}` is a broken record of a crash, not the absence of
    one. A truthiness test would read it as a healthy trial."""
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    root = tmp_path / "t"
    root.mkdir(parents=True)
    (root / "result.json").write_text(
        json.dumps({"trial_name": "t__1", "exception_info": {}})
    )
    (root / "trajectory.json").write_text(OUTCOMES_FIXTURE.read_text())
    capture_trial(run, root, strict=True)
    rollout = next(s for s in app.spans[run.id] if s["span_type"] == "rollout")
    assert rollout["status"] == "failed"
    assert rollout["attributes"]["outcome"] == OUTCOME_FAILED


def test_a_trial_exception_fails_the_rollout_and_only_the_rollout(
    client, app, tmp_path
):
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    capture_trial(run, _write_trial(tmp_path / "t", exception=True), strict=True)
    spans = app.spans[run.id]
    rollout = next(s for s in spans if s["span_type"] == "rollout")
    assert rollout["status"] == "failed"
    assert rollout["attributes"]["outcome"] == OUTCOME_FAILED
    assert rollout["attributes"]["outcome_rule"] == RULE_TRIAL_EXCEPTION
    assert rollout["attributes"]["outcome_source"] == "result.json:exception_info"
    # the exception does NOT recolor the children — each keeps what it proved
    children = _outcomes(spans)
    assert OUTCOME_SUCCEEDED in {outcome for outcome, _, _ in children.values()}
    assert OUTCOME_UNKNOWN in {outcome for outcome, _, _ in children.values()}
