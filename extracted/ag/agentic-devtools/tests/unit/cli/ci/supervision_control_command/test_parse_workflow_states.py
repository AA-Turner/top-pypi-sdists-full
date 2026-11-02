"""Tests for the parse_workflow_states symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control_command import LOOP_WORKFLOW_FILES, parse_workflow_states


@pytest.mark.parametrize(
    "raw",
    [
        "not-a-list",
        ["not-a-dict"],
        [{"name": "x", "path": 1, "state": "active"}],
        [{"name": "x", "path": "a.yml", "state": 1}],
        [{"name": "x", "path": ".github/workflows/ai-pr-loop.yml", "state": "unknown"}],
    ],
)
def test_parse_workflow_states_rejects_malformed_payloads(raw: object) -> None:
    with pytest.raises(ValueError):
        parse_workflow_states(raw)


def test_parse_workflow_states_accepts_every_documented_disabled_state() -> None:
    raw = [
        {"name": "a", "path": ".github/workflows/ai-pr-loop.yml", "state": "disabled_inactivity"},
        {"name": "b", "path": ".github/workflows/ai-pr-loop-watchdog.yml", "state": "disabled_fork"},
    ]

    states = parse_workflow_states(raw)

    assert states == {"ai-pr-loop.yml": False, "ai-pr-loop-watchdog.yml": False}


def test_parse_workflow_states_restricts_to_known_loop_workflows() -> None:
    raw = [
        {"name": "AI PR Loop", "path": ".github/workflows/ai-pr-loop.yml", "state": "active"},
        {"name": "Watchdog", "path": ".github/workflows/ai-pr-loop-watchdog.yml", "state": "disabled_manually"},
        {"name": "Unrelated", "path": ".github/workflows/unrelated.yml", "state": "active"},
    ]

    states = parse_workflow_states(raw)

    assert states == {"ai-pr-loop.yml": True, "ai-pr-loop-watchdog.yml": False}
    assert "unrelated.yml" not in states
    assert set(LOOP_WORKFLOW_FILES) >= states.keys()


@pytest.mark.parametrize(
    "states",
    [
        ["active", "active"],
        ["active", "disabled_manually"],
    ],
)
def test_parse_workflow_states_rejects_duplicate_known_workflow_evidence(states: list[str]) -> None:
    raw = [
        {"name": f"entry-{index}", "path": ".github/workflows/ai-pr-loop.yml", "state": state}
        for index, state in enumerate(states)
    ]

    with pytest.raises(ValueError, match="duplicate workflow evidence"):
        parse_workflow_states(raw)
