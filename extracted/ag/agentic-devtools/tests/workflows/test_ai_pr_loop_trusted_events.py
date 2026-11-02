"""Tests for ai-pr-loop-trusted-events.yml workflow structure."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_PR_LOOP_TRUSTED_EVENTS = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop-trusted-events.yml"


def test_trusted_events_passes_invalidation_and_targeted_pr_context() -> None:
    content = AI_PR_LOOP_TRUSTED_EVENTS.read_text(encoding="utf-8")

    assert "--invalidate-inventory" in content
    assert '--trusted-pr-number "${{ github.event.pull_request.number }}"' in content
    assert '--trusted-head-sha "${{ github.event.pull_request.head.sha }}"' in content


def test_trusted_events_reconciliation_uses_bookkeeping_token_without_permission_expansion() -> None:
    parsed = yaml.safe_load(AI_PR_LOOP_TRUSTED_EVENTS.read_text(encoding="utf-8"))
    job = parsed["jobs"]["trusted-event-reconciliation"]
    reconcile = next(step for step in job["steps"] if step.get("name") == "Run live reconciliation preflight")

    assert reconcile["env"]["AI_PR_LOOP_BOOKKEEPING_TOKEN"] == "${{ github.token }}"
    assert set(parsed["permissions"]) == {"contents", "actions", "pull-requests"}
    assert parsed["permissions"]["pull-requests"] == "read"
