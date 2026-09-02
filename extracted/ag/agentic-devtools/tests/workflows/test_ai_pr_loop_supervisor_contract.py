"""Workflow contract tests for the report-only AI PR Loop supervisor."""

from pathlib import Path

import yaml

WORKFLOW = Path(".github/workflows/ai-pr-loop-supervisor.yml")


def test_ai_pr_loop_supervisor_has_scheduled_and_manual_triggers() -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    triggers = workflow.get("on", workflow.get(True, {}))

    assert "schedule" in triggers
    assert "workflow_dispatch" in triggers
    assert workflow["permissions"] == {"contents": "read", "pull-requests": "read", "actions": "read"}


def test_ai_pr_loop_supervisor_is_read_only_and_bounded() -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    job = workflow["jobs"]["scan"]

    assert job["timeout-minutes"] == 10
    run_step = next(step for step in job["steps"] if step.get("name") == "Run read-only supervisor scan")
    assert "agdt-ai-pr-loop-supervisor" in run_step["run"]
    assert "--max-candidates 10" in run_step["run"]
