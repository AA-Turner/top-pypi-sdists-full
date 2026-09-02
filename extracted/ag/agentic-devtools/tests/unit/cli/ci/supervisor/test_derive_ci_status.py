"""Tests for check-run status normalization."""

from agentic_devtools.cli.ci.models import CheckRunStatus
from agentic_devtools.cli.ci.supervisor import derive_ci_status


def test_derive_ci_status_returns_unknown_without_checks() -> None:
    assert derive_ci_status([]) == "unknown"


def test_derive_ci_status_returns_failing_for_failed_check() -> None:
    checks = [CheckRunStatus(id=1, name="tests", status="completed", conclusion="failure")]

    assert derive_ci_status(checks) == "failing"


def test_derive_ci_status_returns_failing_for_stale_check() -> None:
    checks = [CheckRunStatus(id=1, name="tests", status="completed", conclusion="stale")]

    assert derive_ci_status(checks) == "failing"


def test_derive_ci_status_returns_pending_for_incomplete_check() -> None:
    checks = [CheckRunStatus(id=1, name="tests", status="in_progress")]

    assert derive_ci_status(checks) == "pending"


def test_derive_ci_status_returns_passing_for_successful_checks() -> None:
    checks = [
        CheckRunStatus(id=1, name="tests", status="completed", conclusion="success"),
        CheckRunStatus(id=2, name="lint", status="completed", conclusion="neutral"),
    ]

    assert derive_ci_status(checks) == "passing"


def test_derive_ci_status_returns_pending_for_unknown_completed_conclusion() -> None:
    checks = [CheckRunStatus(id=1, name="tests", status="completed", conclusion="unknown")]

    assert derive_ci_status(checks) == "pending"
