"""Tests for selecting the latest AI PR Loop workflow run."""

from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun
from agentic_devtools.cli.ci.supervisor import select_latest_loop_run


def test_select_latest_loop_run_returns_status_conclusion_and_timestamp_for_pr() -> None:
    runs = [
        WorkflowRun(
            id=1,
            name="AI PR Loop",
            conclusion="success",
            run_attempt=1,
            created_at="2026-08-31T10:00:00Z",
            event="workflow_dispatch",
            head_branch="feature",
            pr_number=7,
        ),
        WorkflowRun(
            id=2,
            name="AI PR Loop",
            conclusion="",
            run_attempt=1,
            created_at="2026-08-31T11:00:00Z",
            event="workflow_dispatch",
            head_branch="feature",
            pr_number=7,
        ),
    ]

    status, conclusion, timestamp = select_latest_loop_run(runs, 7)

    assert status == "in_progress"
    assert conclusion == ""
    assert timestamp is not None
    assert timestamp.isoformat() == "2026-08-31T11:00:00+00:00"


def test_select_latest_loop_run_ignores_other_prs_and_invalid_entries() -> None:
    runs = [
        object(),
        WorkflowRun(
            id=2,
            name="AI PR Loop",
            conclusion="failure",
            run_attempt=1,
            created_at="invalid",
            event="workflow_dispatch",
            head_branch="feature",
            pr_number=7,
        ),
        WorkflowRun(
            id=3,
            name="AI PR Loop",
            conclusion="failure",
            run_attempt=1,
            created_at="invalid",
            event="workflow_dispatch",
            head_branch="feature",
            pr_number=8,
        ),
    ]

    assert select_latest_loop_run(runs, 7) == ("", "", None)
