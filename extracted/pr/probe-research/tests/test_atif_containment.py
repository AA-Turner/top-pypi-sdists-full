"""Turn containment: reparenting onto a phase, clamping strays, bounding the tail.

Depth-first rendering equals chronological order only when a child really sits
inside its parent. These are the three places that stops being true for free.
"""

from __future__ import annotations

from probe.connectors.atif import (
    CONTAINMENT_CLAMPED,
    ELAPSED_SOURCE_NEXT_STEP,
    _apply_tool_call_timing,
    _reparent_root_turns,
    parse_atif,
)

PHASE_START = "2026-08-05T08:50:17.310979Z"
PHASE_END = "2026-08-05T08:51:01.021424Z"


def _doc(*timestamps: str) -> dict:
    return {
        "schema_version": "ATIF-v1.7",
        "steps": [
            {
                "step_id": index + 1,
                "source": "agent" if index else "user",
                "message": f"step {index + 1}",
                "timestamp": stamp,
            }
            for index, stamp in enumerate(timestamps)
        ],
    }


def _turns(plans):
    return [p for p in plans if p.span_type == "turn"]


# -- the terminal step -------------------------------------------------------
def test_boundary_bounds_the_last_turn_which_otherwise_has_no_extent():
    doc = _doc("2026-08-05T08:50:18.000000Z", "2026-08-05T08:50:25.000000Z")
    unbounded = _turns(parse_atif(doc))
    assert unbounded[-1].attributes.get("elapsed_ms") is None

    bounded = _turns(parse_atif(doc, boundary=PHASE_END))
    tail = bounded[-1]
    assert tail.attributes["elapsed_ms"] == 36021
    assert tail.attributes["elapsed_source"] == ELAPSED_SOURCE_NEXT_STEP


def test_boundary_never_overrides_a_real_next_sibling():
    doc = _doc("2026-08-05T08:50:18.000000Z", "2026-08-05T08:50:25.000000Z")
    turns = _turns(parse_atif(doc, boundary=PHASE_END))
    # First step still measures to the second step, not to the phase end.
    assert turns[0].attributes["elapsed_ms"] == 7000


def test_a_boundary_before_the_last_step_yields_no_extent_not_a_negative_one():
    doc = _doc("2026-08-05T08:50:18.000000Z", "2026-08-05T08:51:30.000000Z")
    tail = _turns(parse_atif(doc, boundary=PHASE_END))[-1]
    assert "elapsed_ms" not in tail.attributes


def test_nested_subagent_under_a_terminal_step_is_no_longer_untimed():
    """TODOS.md 'Inferred span timing: provenance gaps', case 3."""
    doc = {
        "schema_version": "ATIF-v1.7",
        "steps": [
            {
                "step_id": 1,
                "source": "agent",
                "message": "delegate",
                "timestamp": "2026-08-05T08:50:18.000000Z",
                "tool_calls": [
                    {"tool_call_id": "c1", "function_name": "spawn", "arguments": {}}
                ],
                "observation": {
                    "results": [
                        {
                            "source_call_id": "c1",
                            "content": "done",
                            "subagent_trajectory_ref": [{"trajectory_id": "sub-1"}],
                        }
                    ]
                },
            }
        ],
        "subagent_trajectories": [
            {
                "trajectory_id": "sub-1",
                "agent": {"name": "investigator"},
                "steps": [
                    {
                        "step_id": 1,
                        "source": "agent",
                        "message": "look",
                        "timestamp": "2026-08-05T08:50:20.000000Z",
                    }
                ],
            }
        ],
    }
    wrapper = next(p for p in parse_atif(doc, boundary=PHASE_END) if p.attributes.get("subagent"))
    assert wrapper.attributes["elapsed_ms"] is not None


# -- reparenting -------------------------------------------------------------
def test_root_turns_reparent_onto_the_phase_and_nested_spans_do_not_move():
    plans = parse_atif(_doc("2026-08-05T08:50:18.000000Z"))
    plans.append(
        type(plans[0])(
            path="turn/1/call/0", span_type="tool_call", name="rg", parent_path="turn/1"
        )
    )
    _reparent_root_turns(
        plans, "phase/agent_execution", phase_start=PHASE_START, phase_end=PHASE_END
    )
    by_path = {p.path: p for p in plans}
    assert by_path["turn/1"].parent_path == "phase/agent_execution"
    assert by_path["turn/1/call/0"].parent_path == "turn/1"


def test_a_turn_inside_the_phase_is_untouched():
    plans = parse_atif(_doc("2026-08-05T08:50:18.000000Z"))
    _reparent_root_turns(
        plans, "phase/agent_execution", phase_start=PHASE_START, phase_end=PHASE_END
    )
    turn = _turns(plans)[0]
    assert turn.started_at == "2026-08-05T08:50:18.000000Z"
    assert "containment" not in turn.attributes
    assert "raw_started_at" not in turn.attributes


def test_a_turn_before_the_phase_is_clamped_and_keeps_its_recorded_stamp():
    """The synthetic rl-ui fixture does exactly this: turn 5s before its phase."""
    early = "2026-08-05T08:50:12.000000Z"
    plans = parse_atif(_doc(early))
    _reparent_root_turns(
        plans, "phase/agent_execution", phase_start=PHASE_START, phase_end=PHASE_END
    )
    turn = _turns(plans)[0]
    assert turn.started_at == PHASE_START
    assert turn.attributes["raw_started_at"] == early
    assert turn.attributes["containment"] == CONTAINMENT_CLAMPED


def test_a_turn_after_the_phase_is_clamped_to_the_end():
    late = "2026-08-05T08:52:00.000000Z"
    plans = parse_atif(_doc(late))
    _reparent_root_turns(
        plans, "phase/agent_execution", phase_start=PHASE_START, phase_end=PHASE_END
    )
    turn = _turns(plans)[0]
    assert turn.started_at == PHASE_END
    assert turn.attributes["raw_started_at"] == late


def test_without_phase_bounds_turns_reparent_but_are_never_clamped():
    plans = parse_atif(_doc("2026-08-05T08:50:12.000000Z"))
    _reparent_root_turns(
        plans, "phase/agent_execution", phase_start=None, phase_end=None
    )
    turn = _turns(plans)[0]
    assert turn.parent_path == "phase/agent_execution"
    assert "containment" not in turn.attributes


def test_a_turn_with_no_timestamp_reparents_without_a_clamp_claim():
    doc = {
        "schema_version": "ATIF-v1.7",
        "steps": [{"step_id": 1, "source": "user", "message": "hi"}],
    }
    plans = parse_atif(doc)
    _reparent_root_turns(
        plans, "phase/agent_execution", phase_start=PHASE_START, phase_end=PHASE_END
    )
    turn = _turns(plans)[0]
    assert turn.parent_path == "phase/agent_execution"
    assert turn.started_at is None
    assert "containment" not in turn.attributes


# -- measured tool-call timing ----------------------------------------------
def test_measured_timing_closes_a_tool_call_that_atif_left_open():
    """The one thing allowed to reach `ended_at`: an actual measurement."""
    doc = {
        "schema_version": "ATIF-v1.7",
        "steps": [
            {
                "step_id": 1,
                "source": "agent",
                "message": "search",
                "timestamp": "2026-08-05T08:50:20.850Z",
                "tool_calls": [
                    {"tool_call_id": "toolu_1", "function_name": "Bash", "arguments": {}}
                ],
            }
        ],
    }
    plans = parse_atif(doc)
    call = next(p for p in plans if p.span_type == "tool_call")
    assert call.ended_at is None

    _apply_tool_call_timing(
        plans,
        {
            "toolu_1": (
                "2026-08-05T08:50:20.850Z",
                "2026-08-05T08:50:23.500Z",
                {"timing_source": "agent_session_log"},
            )
        },
    )
    call = next(p for p in plans if p.span_type == "tool_call")
    assert call.started_at == "2026-08-05T08:50:20.850Z"
    assert call.ended_at == "2026-08-05T08:50:23.500Z"
    assert call.attributes["timing_source"] == "agent_session_log"


def test_an_uncovered_call_keeps_the_inherited_start_and_no_end():
    """Partial recovery is normal; each call says which kind of number it has."""
    doc = {
        "schema_version": "ATIF-v1.7",
        "steps": [
            {
                "step_id": 1,
                "source": "agent",
                "message": "search",
                "timestamp": "2026-08-05T08:50:20.850Z",
                "tool_calls": [
                    {"tool_call_id": "toolu_1", "function_name": "Bash", "arguments": {}},
                    {"tool_call_id": "toolu_2", "function_name": "rg", "arguments": {}},
                ],
            }
        ],
    }
    plans = parse_atif(doc)
    _apply_tool_call_timing(
        plans,
        {"toolu_1": ("2026-08-05T08:50:20.850Z", "2026-08-05T08:50:23.500Z", {})},
    )
    calls = {p.attributes["tool_call_id"]: p for p in plans if p.span_type == "tool_call"}
    assert calls["toolu_1"].ended_at == "2026-08-05T08:50:23.500Z"
    assert calls["toolu_2"].ended_at is None
    assert calls["toolu_2"].started_at == "2026-08-05T08:50:20.850Z"


def test_timing_joins_on_the_producer_id_never_on_name_or_position():
    doc = {
        "schema_version": "ATIF-v1.7",
        "steps": [
            {
                "step_id": 1,
                "source": "agent",
                "message": "search",
                "timestamp": "2026-08-05T08:50:20.850Z",
                "tool_calls": [
                    {"tool_call_id": "toolu_real", "function_name": "Bash", "arguments": {}}
                ],
            }
        ],
    }
    plans = parse_atif(doc)
    _apply_tool_call_timing(
        plans,
        {"Bash": ("2026-08-05T08:50:20.850Z", "2026-08-05T08:50:23.500Z", {})},
    )
    call = next(p for p in plans if p.span_type == "tool_call")
    assert call.ended_at is None
