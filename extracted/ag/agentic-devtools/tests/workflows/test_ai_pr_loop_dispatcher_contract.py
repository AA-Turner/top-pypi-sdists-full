"""Workflow contract tests for the AI PR Loop dispatcher."""

from pathlib import Path

import yaml

WORKFLOW = Path(".github/workflows/ai-pr-loop-dispatcher.yml")


def test_ai_pr_loop_dispatcher_uses_default_workflow_pat_for_throttle_and_dispatch() -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["dispatch-monitor"]["steps"]

    for step_name in ("Throttle check", "Dispatch AI PR Loop Throttler"):
        step = next(step for step in steps if step.get("name") == step_name)
        assert step["env"] == {
            "GH_TOKEN": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
            "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
            "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        }
