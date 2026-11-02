"""Tests for raw row validation without lifecycle conversion."""

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import _agent_task_row_failure


@pytest.mark.parametrize(
    "state",
    [
        "idle",
        "in_progress",
        "queued",
        "requested",
        "running",
        "waiting",
        "waiting_for_user",
        "canceled",
        "cancelled",
        "completed",
        "failed",
        "stopped",
        "timed_out",
        " Running ",
        {"state": "running"},
        {"status": "running"},
    ],
)
@pytest.mark.parametrize("key", ["state", "status"])
def test_accepts_supported_states(state, key) -> None:
    assert _agent_task_row_failure({key: state}) is None


@pytest.mark.parametrize(
    "row",
    [
        {},
        {"state": ""},
        {"state": {"name": "running"}},
        {"state": {"state": []}},
        {"state": True},
        {"state": "paused"},
    ],
)
def test_unknown_states_are_explicit(row) -> None:
    assert _agent_task_row_failure(row) == "unknown_task_state"


@pytest.mark.parametrize("row", [None, "row", [], 1])
def test_non_objects_are_malformed(row) -> None:
    assert _agent_task_row_failure(row) == "malformed_response"
