"""Tests for the _workflow_states symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control_command import _workflow_states


def test_workflow_states_requests_manually_disabled_workflows(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[str] = []

    def fake_run_gh(arguments: list[str]) -> list[object]:
        captured.extend(arguments)
        return [{"name": "Loop", "path": ".github/workflows/ai-pr-loop.yml", "state": "disabled_manually"}]

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", fake_run_gh)

    assert _workflow_states("swai-factory/agentic-devtools") == {"ai-pr-loop.yml": False}
    assert captured == [
        "workflow",
        "list",
        "--repo",
        "swai-factory/agentic-devtools",
        "--all",
        "--json",
        "name,path,state",
    ]
