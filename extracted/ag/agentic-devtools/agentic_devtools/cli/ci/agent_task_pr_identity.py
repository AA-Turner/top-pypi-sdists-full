"""Typed PR identity provenance for Agent Task lifecycle evidence."""

from dataclasses import dataclass
from enum import StrEnum


class AgentTaskPrIdentityKind(StrEnum):
    """How an Agent Task is associated with a requested pull request."""

    PR_NUMBER = "pr_number"
    PR_DATABASE_ID = "pr_database_id"
    BRANCH_ONLY = "branch_only"
    NONE = "none"


@dataclass(frozen=True)
class AgentTaskPrIdentity:
    """Correlation details without treating branch-only evidence as verified identity."""

    kind: AgentTaskPrIdentityKind = AgentTaskPrIdentityKind.NONE
    correlates: bool = False
    task_pr_number: int | None = None
    task_branch: str = ""

    @property
    def is_verified_pr_identity(self) -> bool:
        """Return whether exact PR-number or database-ID evidence matched."""
        return self.kind in {
            AgentTaskPrIdentityKind.PR_NUMBER,
            AgentTaskPrIdentityKind.PR_DATABASE_ID,
        }


def resolve_agent_task_pr_identity(
    *,
    requested_pr_number: int,
    task_pr_number: int | None,
    requested_pr_database_id: int | None,
    task_pr_database_id: int | str | None,
    requested_head_branch: str,
    task_branch: str,
) -> AgentTaskPrIdentity:
    """Classify exact PR identity, branch-only correlation, or no match."""
    normalized_task_branch = task_branch.removeprefix("refs/heads/")
    normalized_task_pr_database_id = task_pr_database_id
    if isinstance(task_pr_database_id, str) and task_pr_database_id.isascii() and task_pr_database_id.isdigit():
        try:
            normalized_task_pr_database_id = int(task_pr_database_id)
        except ValueError:
            normalized_task_pr_database_id = None

    if type(requested_pr_number) is int and type(task_pr_number) is int and task_pr_number == requested_pr_number:
        kind = AgentTaskPrIdentityKind.PR_NUMBER
    elif (
        type(requested_pr_database_id) is int
        and type(normalized_task_pr_database_id) is int
        and normalized_task_pr_database_id == requested_pr_database_id
    ):
        kind = AgentTaskPrIdentityKind.PR_DATABASE_ID
    elif requested_head_branch and normalized_task_branch == requested_head_branch.removeprefix("refs/heads/"):
        kind = AgentTaskPrIdentityKind.BRANCH_ONLY
    else:
        kind = AgentTaskPrIdentityKind.NONE

    normalized_pr_number = task_pr_number
    if kind is AgentTaskPrIdentityKind.PR_DATABASE_ID:
        normalized_pr_number = requested_pr_number

    return AgentTaskPrIdentity(
        kind=kind,
        correlates=kind is not AgentTaskPrIdentityKind.NONE,
        task_pr_number=normalized_pr_number,
        task_branch=normalized_task_branch,
    )
