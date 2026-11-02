"""Tests for the build_status_report symbol."""

from __future__ import annotations

from agentic_devtools.cli.ci.supervision_control import Checkpoint, PRObservation
from agentic_devtools.cli.ci.supervision_control_command import build_status_report


def _observation(number: int, head: str, *labels: str) -> PRObservation:
    return PRObservation(number, head, frozenset(labels))


def test_build_status_report_shapes_full_contract() -> None:
    checkpoint = Checkpoint("run-1", {"selected": [7]}, "repo")

    report = build_status_report(
        {"loop.yml": True, "watchdog.yml": False},
        42,
        checkpoint,
        [_observation(7, "head-7", "ai-pr-loop-supervised")],
    )

    assert report == {
        "workflows": {"loop.yml": True, "watchdog.yml": False},
        "control_issue": {"number": 42, "checkpoint": {"run_id": "run-1", "payload": {"selected": [7]}}},
        "managed_prs": [{"number": 7, "head_sha": "head-7", "labels": ["ai-pr-loop-supervised"]}],
    }


def test_build_status_report_handles_missing_control_issue_and_checkpoint() -> None:
    report = build_status_report({}, None, None, [])

    assert report == {
        "workflows": {},
        "control_issue": {"number": None, "checkpoint": None},
        "managed_prs": [],
    }
