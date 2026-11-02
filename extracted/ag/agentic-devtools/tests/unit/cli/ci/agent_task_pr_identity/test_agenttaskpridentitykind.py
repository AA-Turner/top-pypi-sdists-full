"""Tests for the AgentTaskPrIdentityKind enum."""

from agentic_devtools.cli.ci.agent_task_pr_identity import AgentTaskPrIdentityKind


def test_identity_kind_values_are_stable() -> None:
    assert AgentTaskPrIdentityKind.PR_NUMBER.value == "pr_number"
    assert AgentTaskPrIdentityKind.PR_DATABASE_ID.value == "pr_database_id"
    assert AgentTaskPrIdentityKind.BRANCH_ONLY.value == "branch_only"
    assert AgentTaskPrIdentityKind.NONE.value == "none"
