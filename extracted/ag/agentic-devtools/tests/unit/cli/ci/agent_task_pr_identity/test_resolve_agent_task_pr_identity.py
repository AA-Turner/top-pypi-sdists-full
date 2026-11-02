"""Tests for resolving Agent Task PR identity provenance."""

import pytest

from agentic_devtools.cli.ci.agent_task_pr_identity import (
    AgentTaskPrIdentityKind,
    resolve_agent_task_pr_identity,
)


def test_exact_requested_pr_number_is_verified_identity() -> None:
    identity = resolve_agent_task_pr_identity(
        requested_pr_number=42,
        task_pr_number=42,
        requested_pr_database_id=9001,
        task_pr_database_id=8001,
        requested_head_branch="copilot/pr-42",
        task_branch="copilot/other",
    )

    assert identity.kind is AgentTaskPrIdentityKind.PR_NUMBER
    assert identity.correlates is True
    assert identity.is_verified_pr_identity is True
    assert identity.task_pr_number == 42
    assert identity.task_branch == "copilot/other"


def test_exact_requested_pr_database_id_normalizes_task_pr_number() -> None:
    identity = resolve_agent_task_pr_identity(
        requested_pr_number=42,
        task_pr_number=7,
        requested_pr_database_id=9001,
        task_pr_database_id="9001",
        requested_head_branch="copilot/pr-42",
        task_branch="copilot/task-7",
    )

    assert identity.kind is AgentTaskPrIdentityKind.PR_DATABASE_ID
    assert identity.correlates is True
    assert identity.is_verified_pr_identity is True
    assert identity.task_pr_number == 42
    assert identity.task_branch == "copilot/task-7"


@pytest.mark.parametrize("unconvertible_database_id", ["²", "9" * 5000])
@pytest.mark.parametrize(
    ("task_pr_number", "task_branch", "expected_kind"),
    [
        (42, "copilot/other", AgentTaskPrIdentityKind.PR_NUMBER),
        (7, "refs/heads/copilot/pr-42", AgentTaskPrIdentityKind.BRANCH_ONLY),
    ],
)
def test_unconvertible_database_id_allows_other_identity_matches(
    unconvertible_database_id: str,
    task_pr_number: int,
    task_branch: str,
    expected_kind: AgentTaskPrIdentityKind,
) -> None:
    identity = resolve_agent_task_pr_identity(
        requested_pr_number=42,
        task_pr_number=task_pr_number,
        requested_pr_database_id=9001,
        task_pr_database_id=unconvertible_database_id,
        requested_head_branch="copilot/pr-42",
        task_branch=task_branch,
    )

    assert identity.kind is expected_kind


def test_branch_only_correlation_is_not_verified_pr_identity() -> None:
    identity = resolve_agent_task_pr_identity(
        requested_pr_number=42,
        task_pr_number=7,
        requested_pr_database_id=None,
        task_pr_database_id=None,
        requested_head_branch="copilot/pr-42",
        task_branch="refs/heads/copilot/pr-42",
    )

    assert identity.kind is AgentTaskPrIdentityKind.BRANCH_ONLY
    assert identity.correlates is True
    assert identity.is_verified_pr_identity is False
    assert identity.task_pr_number == 7
    assert identity.task_branch == "copilot/pr-42"


def test_unmatched_identity_does_not_correlate() -> None:
    identity = resolve_agent_task_pr_identity(
        requested_pr_number=42,
        task_pr_number=7,
        requested_pr_database_id=9001,
        task_pr_database_id="not-a-number",
        requested_head_branch="copilot/pr-42",
        task_branch="copilot/task-7",
    )

    assert identity.kind is AgentTaskPrIdentityKind.NONE
    assert identity.correlates is False
    assert identity.is_verified_pr_identity is False
    assert identity.task_pr_number == 7
    assert identity.task_branch == "copilot/task-7"
