"""Issue and pull-request inventory capabilities."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any

from agentic_devtools.cli.ci.models import (
    IssueFacts,
    NoChangePRBrief,
    PRTreeState,
)

if TYPE_CHECKING:
    from datetime import datetime


class _ProviderIssueInventoryMixin(ABC):
    """Issue and pull-request inventory capabilities."""

    def list_linked_issue_labels(self, pr_number: int) -> list[str]:
        """Return label names carried by the PR's linked (closing) issues.

        Label propagation from an issue onto its PR runs a cycle behind PR
        creation, so a follow-up PR can be unlabelled while its issue is not.
        Consumers that must not act on a follow-up PR read this as well as the
        PR's own labels.

        Args:
            pr_number: PR number to inspect.

        Returns:
            Label names found on the PR's linked issues (empty when there are none).

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: read tags from linked work items.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_linked_issue_labels")

    def list_prs_with_label(self, label: str) -> list[int]:
        """List numbers of pull requests that currently carry the given label.

        Args:
            label: Label name to filter on.

        Returns:
            PR numbers carrying the label.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: query pull requests by label/tag.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_prs_with_label")

    def get_label_applied_at(self, pr_number: int, label: str) -> datetime | None:
        """Return when a label was most recently applied to a pull request.

        Args:
            pr_number: PR number to inspect.
            label: Label name to look up.

        Returns:
            Timezone-aware datetime of the most recent application of the label,
            or None when it cannot be determined.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: inspect pull request label/tag history.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_label_applied_at")

    def list_open_copilot_pr_briefs(self) -> list[dict[str, Any]]:
        """List open PRs whose head branch contains ``copilot``, oldest-first.

        Used by the scheduled audit-evaluation takeover to find candidate
        evaluation PRs cheaply before the caller applies the agent-output and
        HEAD-author gates.

        Returns:
            A list of ``{"number": int, "head_branch": str, "created_at": str}``
            dicts, sorted oldest-first by ``created_at``.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: query open pull requests by source-branch prefix.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_open_copilot_pr_briefs")

    def list_no_change_candidate_prs(self) -> list[NoChangePRBrief]:
        """List open pull requests as candidates for the no-change reaper.

        The listing must carry the author, the raw body and the diff statistics
        so the reaper can reject the overwhelming majority of pull requests
        without any further API call.

        Returns:
            One :class:`NoChangePRBrief` per open pull request.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: query open pull requests with description and
        change counts.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_no_change_candidate_prs")

    def get_pr_tree_state(self, pr_number: int) -> PRTreeState:
        """Return the merge base of a pull request and the trees on both sides.

        Args:
            pr_number: PR number to inspect.

        Returns:
            A :class:`PRTreeState` carrying the merge-base SHA and the git tree
            SHAs at the merge base and at HEAD.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: compare the pull request's source and target
        commits and read both tree identifiers.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_pr_tree_state")

    def get_issue_facts(self, issue_number: int) -> IssueFacts:
        """Return the state and body of an issue.

        Args:
            issue_number: Issue number to read.

        Returns:
            An :class:`IssueFacts` with the lowercased state, the raw body, and
            the resource kind resolved from the provider's shared issue/PR
            endpoint.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: read the linked work item's state and
        description.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_issue_facts")

    def get_file_line_count(self, ref: str, path: str) -> int | None:
        """Return the number of lines of a repository file at a given ref.

        Args:
            ref: Commit SHA or ref to read the file at.
            path: Repository-relative file path.

        Returns:
            The line count, or ``None`` when the file does not exist at *ref*.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: read item content at a specific commit.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_file_line_count")
