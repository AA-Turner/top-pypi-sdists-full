"""Regression tests for current workflow attempt clocks."""

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.pipeline.session_detector import _classify_writer_run
from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun


@pytest.mark.parametrize(
    ("age_minutes", "blocking", "expired"),
    [(75, True, False), (76, False, True)],
)
def test_pending_writer_run_uses_expiry_policy(age_minutes, blocking, expired):
    now = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)
    run = WorkflowRun(
        id=1,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at=(now - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        status="pending",
        run_started_at=(now - timedelta(minutes=age_minutes)).isoformat(),
    )

    assessment = _classify_writer_run(run, now=now)

    assert assessment is not None
    assert assessment.blocking is blocking
    assert assessment.expired is expired


@pytest.mark.parametrize("started_at", ["", "invalid"])
@pytest.mark.parametrize("attempt", [0, 2])
def test_nonoriginal_attempt_without_start_does_not_use_original_creation(started_at, attempt):
    run = WorkflowRun(
        id=1,
        name="Cloud writer",
        conclusion="",
        run_attempt=attempt,
        created_at="2026-10-15T08:00:00Z",
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        status="queued",
        run_started_at=started_at,
    )

    assessment = _classify_writer_run(run, now=datetime(2026, 10, 16, 10, tzinfo=UTC))

    assert assessment.blocking is True
    assert assessment.expired is False
    assert assessment.since is None
