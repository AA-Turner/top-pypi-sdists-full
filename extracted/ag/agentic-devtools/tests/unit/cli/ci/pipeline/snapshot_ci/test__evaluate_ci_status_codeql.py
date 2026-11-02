"""Producer validation for all recognized CodeQL check names."""

import pytest

from agentic_devtools.cli.ci.models import CheckRunStatus
from agentic_devtools.cli.ci.pipeline.snapshot_ci import (
    CODEQL_CHECK_NAMES,
    _evaluate_ci_status,
)


def test_evaluate_ci_status_pending_when_codeql_in_progress() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(
                id=1,
                name="Analyze (python)",
                status="in_progress",
                app_slug="github-actions",
            ),
        ],
        frozenset({"Analyze (python)"}),
        codeql_configured=True,
    )

    assert status == "pending"
    assert failed == []


def test_evaluate_ci_status_failing_when_codeql_failed() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(
                id=1,
                name="Analyze (python)",
                status="completed",
                conclusion="failure",
                app_slug="github-actions",
            ),
        ],
        frozenset({"Analyze (python)"}),
        codeql_configured=True,
    )

    assert status == "failing"
    assert failed == ["Analyze (python)"]


def test_evaluate_ci_status_passing_when_codeql_succeeded() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(
                id=1,
                name="CodeQL",
                status="completed",
                conclusion="success",
                app_slug="github-advanced-security",
            ),
            CheckRunStatus(
                id=2,
                name="Run Targeted Checks",
                status="completed",
                conclusion="success",
            ),
        ],
        frozenset({"CodeQL", "Run Targeted Checks"}),
        codeql_configured=True,
    )

    assert status == "passing"
    assert failed == []


def test_evaluate_ci_status_pending_when_codeql_configured_but_absent() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(
                id=1,
                name="Run Targeted Checks",
                status="completed",
                conclusion="success",
            ),
        ],
        frozenset({"Run Targeted Checks"}),
        codeql_configured=True,
    )

    assert status == "pending"
    assert failed == []


def test_evaluate_ci_status_passing_when_codeql_not_configured_and_absent() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(
                id=1,
                name="Run Targeted Checks",
                status="completed",
                conclusion="success",
            ),
        ],
        frozenset({"Run Targeted Checks"}),
    )

    assert status == "passing"
    assert failed == []


def test_evaluate_ci_status_ignores_unrelated_codeql_check_app() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(
                id=1,
                name="CodeQL",
                status="completed",
                conclusion="failure",
                app_slug="third-party-app",
            ),
            CheckRunStatus(
                id=2,
                name="Run Targeted Checks",
                status="completed",
                conclusion="success",
            ),
        ],
        frozenset({"CodeQL", "Run Targeted Checks"}),
        codeql_configured=True,
    )

    assert status == "pending"
    assert failed == []


def test_evaluate_ci_status_pending_when_codeql_excluded_by_actionable_override() -> None:
    # AI_PR_LOOP_ACTIONABLE_CHECKS omits "Analyze (python)"; a configured CodeQL
    # run in progress must still block "passing" even though an unrelated
    # overridden check already succeeded.
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(
                id=1,
                name="Analyze (python)",
                status="in_progress",
                app_slug="github-actions",
            ),
            CheckRunStatus(
                id=2,
                name="Build",
                status="completed",
                conclusion="success",
            ),
        ],
        frozenset({"Build"}),
        codeql_configured=True,
    )

    assert status == "pending"
    assert failed == []


def test_evaluate_ci_status_failing_when_codeql_excluded_by_actionable_override() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(
                id=1,
                name="Analyze (python)",
                status="completed",
                conclusion="failure",
                app_slug="github-actions",
            ),
            CheckRunStatus(
                id=2,
                name="Build",
                status="completed",
                conclusion="success",
            ),
        ],
        frozenset({"Build"}),
        codeql_configured=True,
    )

    assert status == "failing"
    assert failed == ["Analyze (python)"]


@pytest.mark.parametrize(
    "conclusion", ["neutral", "skipped", "cancelled", "timed_out", "action_required", "stale", "", "unknown"]
)
@pytest.mark.parametrize("name", sorted(CODEQL_CHECK_NAMES))
def test_configured_codeql_terminal_non_success_fails(conclusion, name):
    checks = [CheckRunStatus(id=1, name=name, status="completed", conclusion=conclusion)]
    assert _evaluate_ci_status(checks, frozenset(), True) == ("failing", [name])
