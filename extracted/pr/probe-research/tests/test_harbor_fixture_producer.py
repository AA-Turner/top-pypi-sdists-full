"""The producer-generated Harbor trial, captured through the real connector.

These are the tests the hand-authored `rl-ui-happy-path` fixture could never
pass. Its phases and steps were written separately and disagree by five
seconds, so it exercised the containment clamp on every trial while real
captures never do -- which made the clamp stop meaning "something is wrong".

Every assertion here is about the AGREEMENT between the two artifacts, not
about specific numbers. A generator projecting both from one clock cannot
express a disagreement; these prove it, and they fail if anyone reintroduces a
fixture that can.
"""

from __future__ import annotations

import json

from probe.connectors.atif import CONTAINMENT_CLAMPED
from probe.connectors.harbor import capture_trial, parse_trial
from probe.connectors.harbor_phases import (
    SPAN_TYPE_GAP,
    SPAN_TYPE_PHASE,
    plan_phase_spans,
)
from tests.conftest import open_run
from tests.fixtures.harbor_trial import HAPPY_PATH, ToolCall, Turn, TrialScript, build, write


def _spans(app) -> list[dict]:
    return [
        span
        for request in app.requests
        if request.url.path.endswith("/spans")
        for span in json.loads(request.content)["spans"]
    ]


def _capture(client, tmp_path, script=HAPPY_PATH):
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    return capture_trial(run, write(script, tmp_path / script.name), strict=True)


# -- the property the hand-authored fixture violated -------------------------
def test_no_turn_is_ever_clamped_because_none_can_fall_outside_its_phase(
    client, app, tmp_path
):
    _capture(client, tmp_path)
    clamped = [
        span
        for span in _spans(app)
        if span["attributes"].get("containment") == CONTAINMENT_CLAMPED
    ]
    assert clamped == [], (
        "A generated trial must never need the clamp. If this fails the "
        "producer has grown a way to state a turn's time independently of the "
        "phase around it, which is the bug this fixture exists to prevent."
    )


def test_every_turn_falls_inside_the_agent_execution_window():
    built = build(HAPPY_PATH)
    phase = built["result"]["agent_execution"]
    for step in built["trajectory"]["steps"]:
        assert phase["started_at"] <= step["timestamp"] <= phase["finished_at"]


def test_turns_reparent_under_the_phase_rather_than_the_rollout(client, app, tmp_path):
    _capture(client, tmp_path)
    spans = _spans(app)
    by_id = {span["id"]: span for span in spans}
    phase = next(
        s for s in spans if s["span_type"] == SPAN_TYPE_PHASE and s["name"] == "agent_execution"
    )
    turns = [s for s in spans if s["span_type"] == "turn"]
    assert turns
    for turn in turns:
        assert by_id[turn["parent_span_id"]]["id"] == phase["id"]


# -- the trial accounts for its own duration ---------------------------------
def test_children_cover_the_trial_and_the_seams_are_not_spans():
    built = build(HAPPY_PATH)
    result = built["result"]
    plans, report = plan_phase_spans(
        {k: result[k] for k in ("environment_setup", "agent_setup", "agent_execution", "verifier")},
        trial_started_at=result["started_at"],
        trial_ended_at=result["finished_at"],
    )
    assert report["state"] == "complete"
    assert report["overlaps"] == []
    assert len([p for p in plans if p.span_type == SPAN_TYPE_PHASE]) == 4
    # Three gaps: orchestration, log download, teardown. The 39-microsecond
    # seam between environment_setup and agent_setup is real and deliberately
    # below the floor, so a fourth here would mean the floor stopped working.
    assert len([p for p in plans if p.span_type == SPAN_TYPE_GAP]) == 3


def test_the_generated_trial_carries_sub_millisecond_seams_like_a_real_one():
    """A grid of tidy whole seconds teaches a shape production does not have."""
    result = build(HAPPY_PATH)["result"]
    assert result["environment_setup"]["finished_at"] != result["agent_setup"]["started_at"]
    assert result["started_at"].endswith("Z") and "." in result["started_at"]


# -- measured tool timing ----------------------------------------------------
def test_the_session_transcript_closes_every_tool_call(client, app, tmp_path):
    _capture(client, tmp_path)
    calls = [s for s in _spans(app) if s["span_type"] == "tool_call"]
    assert len(calls) == 3
    for call in calls:
        assert call["ended_at"] is not None
        assert call["attributes"]["timing_source"] == "agent_session_log"
        # A measured window replaces the inference; carrying both would hand a
        # reader two durations and no rule for which wins.
        assert "elapsed_ms" not in call["attributes"]


def test_a_batch_reports_its_shared_dispatch_and_a_solitary_call_does_not(
    client, app, tmp_path
):
    _capture(client, tmp_path)
    calls = {s["name"]: s for s in _spans(app) if s["span_type"] == "tool_call"}
    assert calls["rg"]["started_at"] == calls["read_file"]["started_at"]
    assert calls["rg"]["attributes"]["dispatch"] == "batched_dispatch"
    assert "dispatch" not in calls["bash_command"]["attributes"]


# -- reproducibility ---------------------------------------------------------
def test_generation_is_deterministic(tmp_path):
    first = write(HAPPY_PATH, tmp_path / "a")
    second = write(HAPPY_PATH, tmp_path / "b")
    for name in ("result.json", "agent/trajectory.json"):
        assert (first / name).read_text() == (second / name).read_text()


def test_a_longer_script_still_cannot_produce_a_disagreement():
    """The invariant is structural, so it survives any script shape."""
    script = TrialScript(
        name="synthetic__long__s0",
        task_name="probe/rl-ui/long",
        environment_setup_seconds=0.001,
        teardown_seconds=0.0,
        turns=tuple(
            Turn(
                "agent",
                f"step {index}",
                0.5,
                tool_calls=(ToolCall("bash_command", {"n": index}, "ok", 0.25),),
            )
            for index in range(25)
        ),
    )
    built = build(script)
    phase = built["result"]["agent_execution"]
    stamps = [step["timestamp"] for step in built["trajectory"]["steps"]]
    assert stamps == sorted(stamps)
    assert phase["started_at"] <= stamps[0]
    assert stamps[-1] <= phase["finished_at"]


def test_the_written_directory_is_what_parse_trial_expects(tmp_path):
    root = write(HAPPY_PATH, tmp_path / "t")
    parsed = parse_trial(root)
    assert parsed.name == HAPPY_PATH.name
    assert parsed.trajectory_format == "ATIF-v1.7"
    assert parsed.reward == HAPPY_PATH.reward
    assert set(parsed.phases) == {
        "environment_setup",
        "agent_setup",
        "agent_execution",
        "verifier",
    }
