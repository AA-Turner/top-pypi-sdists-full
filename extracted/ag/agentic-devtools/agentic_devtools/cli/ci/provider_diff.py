"""Diff, commit-range, and branch synchronization capabilities."""

from __future__ import annotations

from abc import ABC
from typing import Any


class _ProviderDiffMixin(ABC):
    """Diff, commit-range, and branch synchronization capabilities."""

    def get_ref_sha(self, ref: str) -> str:
        """Return the commit SHA a branch/ref currently points at.

        Args:
            ref: Branch name or ref (e.g. ``"main"``).

        Returns:
            Full commit SHA, or an empty string when the ref cannot be
            resolved or the provider does not support this operation.
        """
        return ""

    def compute_diff_hash(self, *, base_branch: str, sha: str, base_sha: str = "") -> str | None:
        """Return a patch fingerprint compared with the base, when supported."""
        return None

    def compute_diff_files(self, *, base_branch: str, sha: str, base_sha: str = "") -> list[str] | None:
        """Return changed files compared with the base, when supported."""
        return None

    def list_pr_commits(self, pr_number: int) -> list[dict[str, Any]]:
        """Return PR commits oldest first, including ``sha`` and ``parents``."""
        raise NotImplementedError(f"{type(self).__name__} does not implement list_pr_commits")

    def get_pr_diff(self, pr_number: int) -> str:
        """Get the unified diff for a pull request.

        Args:
            pr_number: Pull request number.

        Returns:
            Unified diff text as a string.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_pr_diff")

    def get_commit_range_diff(self, base_sha: str, head_sha: str) -> str:
        """Get unified diff text between two commit SHAs.

        Args:
            base_sha: Base commit SHA.
            head_sha: Head commit SHA.

        Returns:
            Unified diff text as a string.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_commit_range_diff")

    def get_commit_range_diff_bytes(self, base_sha: str, head_sha: str) -> bytes:
        """Get lossless unified diff bytes between two commit SHAs."""
        raise NotImplementedError(f"{type(self).__name__} does not implement get_commit_range_diff_bytes")

    def get_commit_range_diff_change_counts(self, base_sha: str, head_sha: str) -> dict[str, int]:
        """Get provider-reported changed-line counts by destination file for a commit range."""
        raise NotImplementedError(f"{type(self).__name__} does not implement get_commit_range_diff_change_counts")

    def count_commits_behind(self, *, pr_number: int, base_branch: str, head_branch: str) -> int:
        """Return how many commits the head branch is behind the base branch.

        Args:
            pr_number: Pull request number (for logging).
            base_branch: Target branch name.
            head_branch: Source branch name.

        Returns:
            Number of commits the head branch is behind. Returns 0 when the
            provider does not support this operation.
        """
        return 0

    def rebase_onto_base(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> str | None:
        """Rebase the head branch onto the base branch and force-push.

        Performs: fetch → checkout → rebase → conflict resolution → force-push-with-lease.
        Returns the new HEAD SHA after a successful update, or ``None`` when no
        update is needed because the expected head changed or is no longer behind.

        Args:
            pr_number: Pull request number (for logging).
            base_branch: Target branch to rebase onto.
            head_branch: Source branch to rebase.
            head_sha: Expected current HEAD SHA (for safety).

        Raises:
            RebaseConflictError: When rebase conflicts cannot be auto-resolved.
            ForceWithLeaseError: When force-push-with-lease fails.
            NotImplementedError: When the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement rebase_onto_base")
