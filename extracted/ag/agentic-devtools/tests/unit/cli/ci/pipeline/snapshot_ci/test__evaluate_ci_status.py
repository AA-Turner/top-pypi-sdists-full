"""Producer validation for all recognized CodeQL check names."""

import pytest

from agentic_devtools.cli.ci.models import CheckRunStatus
from agentic_devtools.cli.ci.pipeline.snapshot_ci import (
    CODEQL_CHECK_NAMES,
    _evaluate_ci_status,
)


@pytest.mark.parametrize("name", sorted(CODEQL_CHECK_NAMES))
@pytest.mark.parametrize("codeql_configured", [False, True])
@pytest.mark.parametrize("app_slug", ["third-party-app", "untrusted-scanner"])
@pytest.mark.parametrize("status,conclusion", [("completed", "success"), ("completed", "failure"), ("in_progress", "")])
def test_untrusted_codeql_producers_are_ignored(name, codeql_configured, app_slug, status, conclusion):
    checks = [
        CheckRunStatus(id=1, name=name, status=status, conclusion=conclusion, app_slug=app_slug),
        CheckRunStatus(id=2, name="Run Targeted Checks", status="completed", conclusion="success"),
    ]

    assert _evaluate_ci_status(checks, frozenset({name, "Run Targeted Checks"}), codeql_configured) == (
        "pending" if codeql_configured else "passing",
        [],
    )


@pytest.mark.parametrize("name", sorted(CODEQL_CHECK_NAMES))
@pytest.mark.parametrize("app_slug", ["github-advanced-security", "github-actions", ""])
@pytest.mark.parametrize(
    "status,conclusion,expected",
    [
        ("completed", "success", "passing"),
        ("in_progress", "", "pending"),
        ("completed", "failure", "failing"),
    ],
)
def test_trusted_codeql_producers_remain_actionable(name, app_slug, status, conclusion, expected):
    checks = [CheckRunStatus(id=1, name=name, status=status, conclusion=conclusion, app_slug=app_slug)]

    assert _evaluate_ci_status(checks, frozenset(), True) == (expected, [name] if expected == "failing" else [])


def test_evaluate_ci_status_pending_when_actionable_pending() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(id=1, name="Targeted Checks ✅", status="in_progress", conclusion=""),
        ],
        frozenset({"Targeted Checks ✅"}),
    )
    assert status == "pending"
    assert failed == []


def test_evaluate_ci_status_unknown_for_unrecognized_conclusion() -> None:
    check = CheckRunStatus(id=1, name="build", status="completed", conclusion="action_required")

    assert _evaluate_ci_status([check], frozenset({"build"})) == ("unknown", [])


def test_evaluate_ci_status_pending_when_no_checks_are_actionable() -> None:
    check = CheckRunStatus(id=1, name="build", status="completed", conclusion="success")

    assert _evaluate_ci_status([check], frozenset({"test"})) == ("pending", [])


def test_evaluate_ci_status_failing_with_actionable_failed_checks() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(id=1, name="Targeted Checks ✅", status="completed", conclusion="failure"),
        ],
        frozenset({"Targeted Checks ✅"}),
    )
    assert status == "failing"
    assert failed == ["Targeted Checks ✅"]


def test_evaluate_ci_status_pending_takes_priority_over_failed() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(id=1, name="Targeted Checks ✅", status="completed", conclusion="failure"),
            CheckRunStatus(id=2, name="Smart Module Tests ✅", status="queued", conclusion=""),
        ],
        frozenset({"Targeted Checks ✅", "Smart Module Tests ✅"}),
    )
    assert status == "pending"
    assert failed == ["Targeted Checks ✅"]


def test_evaluate_ci_status_passing_when_actionable_checks_succeed() -> None:
    status, failed = _evaluate_ci_status(
        [
            CheckRunStatus(id=1, name="Targeted Checks ✅", status="completed", conclusion="success"),
            CheckRunStatus(id=2, name="non-actionable", status="completed", conclusion="failure"),
        ],
        frozenset({"Targeted Checks ✅"}),
    )
    assert status == "passing"
    assert failed == []
