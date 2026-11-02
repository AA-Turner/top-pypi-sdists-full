"""Review-thread and post-repair capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod

from agentic_devtools.cli.ci.models import (
    FinalizationResult,
    IssueCommentInfo,
    IssueEvent,
    ReviewCommentDeletionResult,
    ReviewCommentInfo,
    SquashResult,
)


class _ProviderReviewsMixin(ABC):
    """Review-thread and post-repair capabilities."""

    @abstractmethod
    def request_reviewer(self, pr_number: int, reviewer: str) -> None:
        """Request a reviewer for a pull request.

        Args:
            pr_number: Pull request number.
            reviewer: Username of the reviewer to request.
        """

    @abstractmethod
    def count_unresolved_review_threads(self, pr_number: int) -> int:
        """Count unresolved review comment threads on a pull request.

        Args:
            pr_number: Pull request number.

        Returns:
            Number of unresolved review threads.
        """

    def list_review_thread_states(self, pr_number: int) -> dict[int, tuple[bool, bool]]:
        """Return per-review-comment thread state for a pull request.

        This is an **optional capability**: the default implementation raises
        ``NotImplementedError`` so that a provider which cannot report thread
        state is detected explicitly rather than appearing to report "no
        unresolved threads". Callers must go through
        :func:`agentic_devtools.cli.ci.review_thread_state.fetch_review_thread_states`
        so a missing capability degrades the result instead of silently
        loosening the merge gate.

        Args:
            pr_number: Pull request number.

        Returns:
            Mapping of review comment id to ``(is_resolved, has_reply)``.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: query pull request comment threads and their status.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_review_thread_states")

    @abstractmethod
    def list_review_comments(self, pr_number: int, review_id: int) -> list[ReviewCommentInfo]:
        """List inline comments from a specific review.

        Args:
            pr_number: Pull request number.
            review_id: ID of the review to list comments for.

        Returns:
            List of rich review comment metadata.
        """

    def create_review_thread(
        self,
        *,
        pr_number: int,
        commit_sha: str,
        path: str,
        line: int,
        side: str,
        body: str,
    ) -> ReviewCommentInfo:
        """Create a native inline review comment when supported by the provider.

        Providers without GitHub-style diff review threads must leave the
        operation unsupported rather than emulating it with a conversation comment.
        """
        raise NotImplementedError("Native inline review threads are supported only by GitHub providers")

    @abstractmethod
    def list_issue_comments(self, issue_or_pr_number: int) -> list[IssueCommentInfo]:
        """List issue/PR-level conversation comments for one issue or pull request.

        Args:
            issue_or_pr_number: Issue or pull request number.

        Returns:
            List of IssueCommentInfo in API response order.
        """

    @abstractmethod
    def finalize_post_repair(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
        review_id: int,
    ) -> FinalizationResult:
        """Finalize a Copilot-repaired PR cycle after a synchronize commit.

        Performs provider-specific post-repair actions such as replying to
        review comments and resolving review threads. Squash is handled
        separately via ``squash_post_repair()``.

        Returns:
            FinalizationResult with details about what was resolved/skipped.
        """

    @abstractmethod
    def squash_post_repair(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> SquashResult:
        """Squash post-repair commits into a single clean commit.

        Responsible strictly for commit hygiene. Review requests are handled
        explicitly by RequestReviewAction in the pipeline after squash completes.

        Returns:
            SquashResult recording the pre- and post-squash tree identity so
            callers can verify the squash preserved the tree.
        """

    @abstractmethod
    def list_pr_issue_events(self, pr_number: int) -> list[IssueEvent]:
        """List issue/PR timeline events for a pull request.

        Fetches Copilot session events (copilot_work_finished,
        copilot_work_finished_failure, copilot_work_started) from the
        GitHub Issues Events API. Returns events in chronological order
        (ascending by id).

        Args:
            pr_number: Pull request number.

        Returns:
            List of IssueEvent dataclasses, filtered to Copilot session events.
            Returns an empty list when the platform does not support this concept
            (e.g., Azure DevOps).
        """

    def delete_review_comments(
        self,
        pr_number: int,
        *,
        execute: bool = False,
        author_substring: str | None = None,
    ) -> ReviewCommentDeletionResult:
        """Delete agentic-devtools review-scaffolding comment threads on a pull request.

        The review tooling posts threads (file summaries, overall summary, activity
        log) that carry an ``<!-- agdt-review:v1 type:... -->`` marker. This method
        deletes the comments identified by that marker — the safe, precise default.
        An optional ``author_substring`` may be supplied as a fallback filter.

        Args:
            pr_number: Pull request number/ID.
            execute: When ``False`` (default), perform a dry-run and return the
                comments that *would* be deleted without deleting anything. When
                ``True``, delete the selected comments.
            author_substring: Optional case-insensitive substring matched against
                each comment author's display/unique name as a fallback selector.

        Returns:
            A :class:`ReviewCommentDeletionResult` describing the selected comments
            and, in execute mode, their per-comment deletion outcome.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement delete_review_comments")
