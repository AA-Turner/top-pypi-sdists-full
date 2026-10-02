"""Phase and gap span synthesis from a Harbor trial manifest.

The golden numbers here are lifted verbatim from a REAL captured trial
(``marshmallow-code__apispec.8b421526.lm_rewrite__drebcc8r__probe-a32fd70b`` in
run ``rollouts-300``), not hand-authored. Hand-authored fixtures are exactly how
the producer/consumer mismatch this module exists to expose stayed hidden: the
synthetic ``rl-ui-happy-path`` fixture has phases and steps that disagree by
five seconds because a seeder wrote each independently.
"""

from __future__ import annotations

import re
from probe._compat import tomllib
from pathlib import Path

import pytest

from probe.connectors.harbor_phases import (
    CAUSE_HARBOR_RANGE,
    CAUSE_SOURCE_CONTROL_FLOW,
    GAP_SOURCE_MEASURED,
    MIN_GAP_MS,
    PHASE_ORDER,
    PHASE_SOURCE_HARBOR,
    SPAN_TYPE_GAP,
    SPAN_TYPE_PHASE,
    agent_execution_bounds,
    agent_execution_path,
    plan_phase_spans,
)

# The real trial, exactly as Harbor recorded it. Deliberately NOT in phase order
# in the dict: Harbor writes a JSON object and we must order on the timestamps.
REAL_PHASES = {
    "verifier": {
        "started_at": "2026-08-05T08:51:03.746632Z",
        "finished_at": "2026-08-05T08:51:14.506633Z",
    },
    "agent_setup": {
        "started_at": "2026-08-05T08:49:58.164926Z",
        "finished_at": "2026-08-05T08:50:16.023521Z",
    },
    "agent_execution": {
        "started_at": "2026-08-05T08:50:17.310979Z",
        "finished_at": "2026-08-05T08:51:01.021424Z",
    },
    "environment_setup": {
        "started_at": "2026-08-05T08:49:56.441689Z",
        "finished_at": "2026-08-05T08:49:58.164887Z",
    },
}
REAL_START = "2026-08-05T08:49:56.441183Z"
REAL_END = "2026-08-05T08:51:25.330905Z"


def _real():
    return plan_phase_spans(
        REAL_PHASES, trial_started_at=REAL_START, trial_ended_at=REAL_END
    )


def test_real_trial_yields_four_phases_and_three_gaps_in_wall_order():
    plans, report = _real()
    assert [(p.span_type, p.name) for p in plans] == [
        (SPAN_TYPE_PHASE, "environment_setup"),
        (SPAN_TYPE_PHASE, "agent_setup"),
        (SPAN_TYPE_GAP, "unattributed"),
        (SPAN_TYPE_PHASE, "agent_execution"),
        (SPAN_TYPE_GAP, "unattributed"),
        (SPAN_TYPE_PHASE, "verifier"),
        (SPAN_TYPE_GAP, "unattributed"),
    ]
    assert report["state"] == "complete"
    assert (report["phases"], report["gaps"]) == (4, 3)
    assert report["overlaps"] == []


def test_children_cover_the_whole_trial_as_a_union_not_a_sum():
    """The invariant is union-vs-extent, and it is reported, never forced."""
    plans, report = _real()
    assert report["trial_ms"] == 88889
    # Phases alone are 83% -- which is the whole reason gaps exist.
    assert report["covered_ms"] == 74051
    covered = report["covered_ms"] + sum(
        _ms(p.started_at, p.ended_at) for p in plans if p.span_type == SPAN_TYPE_GAP
    )
    # Two milliseconds of sub-millisecond seams round away; nothing else is lost.
    assert report["trial_ms"] - covered <= 2


def _ms(start: str, end: str) -> int:
    from probe.connectors.atif import _elapsed_ms

    value = _elapsed_ms(start, end)
    assert value is not None
    return value


def test_every_phase_and_gap_is_closed_and_carries_its_provenance():
    plans, _ = _real()
    for plan in plans:
        assert plan.started_at and plan.ended_at, plan.path
        # These are the only spans in the tree whose extent is a subtraction of
        # two recorded stamps. Mixing them into the inferred vocabulary would
        # erase the distinction that makes them worth having.
        assert "elapsed_ms" not in plan.attributes
        expected = (
            PHASE_SOURCE_HARBOR if plan.span_type == SPAN_TYPE_PHASE else GAP_SOURCE_MEASURED
        )
        assert plan.attributes["timing_source"] == expected


def test_gap_cause_is_an_attribute_with_provenance_never_the_span_name():
    plans, _ = _real()
    gaps = [p for p in plans if p.span_type == SPAN_TYPE_GAP]
    assert {p.name for p in gaps} == {"unattributed"}
    causes = [g.attributes["likely_cause"] for g in gaps]
    assert "agent log download" in causes[1]
    assert "teardown" in causes[2]
    for gap in gaps:
        assert gap.attributes["cause_source"] == CAUSE_SOURCE_CONTROL_FLOW
        assert gap.attributes["cause_harbor_range"] == CAUSE_HARBOR_RANGE


def test_sub_millisecond_seam_is_not_a_span():
    """environment_setup -> agent_setup is 39 microseconds on the real trial."""
    plans, report = _real()
    assert report["gaps"] == 3
    for plan in plans:
        if plan.span_type == SPAN_TYPE_GAP:
            assert _ms(plan.started_at, plan.ended_at) >= MIN_GAP_MS


def test_no_phases_returns_nothing_rather_than_one_giant_gap():
    """Absence of phases is not evidence that nothing ran."""
    for phases in ({}, None, "not-a-dict", {"agent_execution": "not-a-dict"}):
        plans, report = plan_phase_spans(
            phases, trial_started_at=REAL_START, trial_ended_at=REAL_END
        )
        assert plans == []
        assert report["state"] == "no_phases"


def test_unclosed_phase_is_dropped_not_guessed_at():
    """A crashed trial leaves the running phase without finished_at."""
    phases = {
        "environment_setup": REAL_PHASES["environment_setup"],
        "agent_execution": {"started_at": "2026-08-05T08:50:17.310979Z"},
    }
    plans, report = plan_phase_spans(
        phases, trial_started_at=REAL_START, trial_ended_at=REAL_END
    )
    assert [p.name for p in plans if p.span_type == SPAN_TYPE_PHASE] == [
        "environment_setup"
    ]
    assert report["phases"] == 1
    assert agent_execution_path(plans) is None
    assert agent_execution_bounds(plans) == (None, None)


def test_backwards_clock_phase_is_dropped():
    phases = {
        "verifier": {
            "started_at": "2026-08-05T08:51:14.506633Z",
            "finished_at": "2026-08-05T08:51:03.746632Z",
        }
    }
    plans, report = plan_phase_spans(
        phases, trial_started_at=REAL_START, trial_ended_at=REAL_END
    )
    assert plans == []
    assert report["state"] == "no_phases"


def test_zero_duration_phase_is_kept_and_produces_no_noise():
    stamp = "2026-08-05T08:49:56.441689Z"
    phases = {"environment_setup": {"started_at": stamp, "finished_at": stamp}}
    plans, report = plan_phase_spans(
        phases, trial_started_at=stamp, trial_ended_at=stamp
    )
    assert [p.name for p in plans] == ["environment_setup"]
    assert report["gaps"] == 0
    assert report["covered_ms"] == 0


def test_overlapping_phases_are_reported_not_repaired():
    phases = {
        "agent_execution": {
            "started_at": "2026-08-05T08:50:17.000000Z",
            "finished_at": "2026-08-05T08:51:01.000000Z",
        },
        "verifier": {
            "started_at": "2026-08-05T08:50:59.000000Z",
            "finished_at": "2026-08-05T08:51:14.000000Z",
        },
    }
    plans, report = plan_phase_spans(
        phases, trial_started_at="2026-08-05T08:50:17.000000Z", trial_ended_at="2026-08-05T08:51:14.000000Z"
    )
    assert report["state"] == "overlapping"
    assert report["overlaps"] == [
        {"phases": ["agent_execution", "verifier"], "overlap_ms": 2000}
    ]
    # The union is 57s, not the 59s a naive sum would claim.
    assert report["covered_ms"] == 57000
    assert report["gaps"] == 0


def test_unbounded_trial_still_describes_the_seams_between_phases():
    plans, report = plan_phase_spans(
        REAL_PHASES, trial_started_at=None, trial_ended_at=None
    )
    # The two interior seams survive; the lead-in and the teardown tail cannot
    # be known without the trial's own extent, so they are not invented.
    assert report["gaps"] == 2
    assert report["state"] == "unbounded_trial"
    assert report["trial_ms"] is None


def test_agent_execution_lookup_finds_the_reparent_target_and_its_bounds():
    plans, _ = _real()
    path = agent_execution_path(plans)
    assert path == "phase/agent_execution"
    assert agent_execution_bounds(plans) == (
        "2026-08-05T08:50:17.310979Z",
        "2026-08-05T08:51:01.021424Z",
    )


def test_cause_table_is_pinned_to_the_harbor_range_it_was_read_from():
    """T14 contract guard.

    The ``likely_cause`` strings come from reading Harbor 0.21.0's control flow,
    not from anything Harbor reports. Widening the dependency pin without
    re-reading that flow is how a deduction quietly becomes fiction, so the pin
    and the range this table was verified against must move together.
    """
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text())
    extras = data["project"]["optional-dependencies"]["harbor"]
    pinned = next(spec for spec in extras if spec.startswith("harbor"))
    declared = re.search(r"harbor([^;]*)", pinned).group(1).strip()
    assert declared == CAUSE_HARBOR_RANGE, (
        f"agent/pyproject.toml pins harbor{declared!r} but the gap cause table in "
        f"harbor_phases.py was read from harbor{CAUSE_HARBOR_RANGE!r}. Re-read "
        "Trial._prepare/_finalize and _sync_agent_output before widening."
    )


def test_phase_order_constant_matches_what_harbor_actually_emits():
    plans, _ = _real()
    emitted = [p.name for p in plans if p.span_type == SPAN_TYPE_PHASE]
    assert emitted == list(PHASE_ORDER)


@pytest.mark.parametrize(
    ("start", "end", "gaps"),
    [
        # Both ends: 2 interior seams + the teardown tail. The lead-in is
        # 506 microseconds on the real trial, so it never clears MIN_GAP_MS.
        (REAL_START, REAL_END, 3),
        # No trial start: nothing to measure a lead-in against, tail survives.
        (None, REAL_END, 3),
        # No trial end: the teardown tail is unknowable and is not invented.
        (REAL_START, None, 2),
        (None, None, 2),
    ],
)
def test_edge_gaps_need_the_trial_extent_interior_seams_do_not(start, end, gaps):
    _, report = plan_phase_spans(
        REAL_PHASES, trial_started_at=start, trial_ended_at=end
    )
    assert report["gaps"] == gaps
    if start is None or end is None:
        assert report["trial_ms"] is None
        assert report["state"] == "unbounded_trial"
