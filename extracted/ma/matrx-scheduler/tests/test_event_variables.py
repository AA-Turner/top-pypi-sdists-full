"""The run's event reaches the agent as the `event` variable (sch_match_event)."""

from matrx_scheduler.runner import variables_for_run


def test_event_from_run_metadata_is_added():
    out = variables_for_run({"tone": "brief"}, {"event": {"action": "row.updated", "entity_id": "r1"}})
    assert out == {"tone": "brief", "event": {"action": "row.updated", "entity_id": "r1"}}


def test_no_event_leaves_task_variables_alone():
    assert variables_for_run({"event": "keep me"}, {}) == {"event": "keep me"}
    assert variables_for_run(None, None) == {}


def test_run_event_wins_over_a_task_variable_named_event():
    out = variables_for_run({"event": "stale"}, {"event": {"action": "row.created"}})
    assert out["event"] == {"action": "row.created"}
