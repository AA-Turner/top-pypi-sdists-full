"""CI platform provider abstract base class.

Defines the ``CIPlatformProvider`` ABC that all CI-platform-specific
implementations must satisfy. This is separate from ``IssueAdapter`` —
it covers CI-specific operations (event parsing, check status, comment
posting, merge gating) rather than issue CRUD.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from agentic_devtools.cli.ci.models import (
    CheckRunStatus,
    EventPayload,
    FinalizationResult,
    IssueCommentInfo,
    IssueEvent,
    IssueFacts,
    NoChangePRBrief,
    PRMetadata,
    PRTreeState,
    ReviewCommentDeletionResult,
    ReviewCommentInfo,
    ReviewInfo,
    SquashResult,
)

if TYPE_CHECKING:
    from datetime import datetime

    from agentic_devtools.cli.audit.models import ClaimResult, ClosedPRInfo
    from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult
    from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun
    from agentic_devtools.cli.ci.scheduler import DispatchEvent, EligiblePR


class CIPlatformProvider(ABC):
    """Abstract base class for CI platform providers.

    Concrete implementations translate platform-specific APIs into a
    unified interface consumed by the orchestrator and guard modules.
    """

    @abstractmethod
    def parse_event(self, raw_payload: dict, event_name: str) -> EventPayload:
        """Parse a raw CI event payload into a normalized EventPayload.

        Args:
            raw_payload: Raw JSON payload from the CI platform.
            event_name: Event type name (e.g., "pull_request", "issues").

        Returns:
            Normalized EventPayload dataclass.

        Raises:
            MalformedEventError: If the payload cannot be parsed.
        """

    @abstractmethod
    def get_pr_metadata(self, pr_number: int) -> PRMetadata:
        """Retrieve pull request metadata from the CI platform.

        Args:
            pr_number: Pull request number.

        Returns:
            PRMetadata with full PR details.
        """

    @abstractmethod
    def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
        """List check runs for a given commit SHA.

        Args:
            head_sha: Commit SHA to query check runs for.

        Returns:
            List of CheckRunStatus for all check runs.
        """

    @abstractmethod
    def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
        """List reviews for a pull request.

        Args:
            pr_number: Pull request number.

        Returns:
            List of ReviewInfo for all reviews.
        """

    @abstractmethod
    def post_comment(self, pr_number: int, body: str) -> int:
        """Post a comment on a pull request.

        Args:
            pr_number: Pull request number.
            body: Comment body text.

        Returns:
            The ID of the created comment.
        """

    def post_comment_as_pr_token(self, pr_number: int, body: str) -> int:
        """Post a comment using the PR-token identity when supported.

        Providers that support multiple comment identities can override this
        to force the same identity used by ``dispatch_conflict_repair`` and
        marker-authenticated dedup checks.  The default implementation falls
        back to ``post_comment`` for backward compatibility.

        Args:
            pr_number: Pull request number.
            body: Comment body text.

        Returns:
            The ID of the created comment.
        """
        return self.post_comment(pr_number, body)

    @abstractmethod
    def update_comment(self, comment_id: int, body: str) -> None:
        """Update an existing comment.

        Args:
            comment_id: ID of the comment to update.
            body: New comment body text.
        """

    @abstractmethod
    def find_comment(self, pr_number: int, marker: str) -> tuple[int, str] | None:
        """Find a comment containing a specific marker string.

        Args:
            pr_number: Pull request number.
            marker: Marker string to search for in comment bodies.

        Returns:
            Tuple of (comment_id, comment_body) if found, None otherwise.
        """

    @abstractmethod
    def approve_pr(self, pr_number: int, head_sha: str, body: str) -> bool:
        """Approve a pull request.

        Args:
            pr_number: Pull request number.
            head_sha: Expected HEAD SHA (for safety check).
            body: Approval comment body.

        Returns:
            ``True`` when approval was posted, ``False`` when intentionally skipped.
        """

    def get_approver_login(self) -> str:
        """Return the approver identity login/name for this provider.

        Best-effort helper for providers that can resolve the identity used for
        automated PR approval. Returns an empty string when the approver
        identity is not configured, resolution fails, or the provider does not
        support identity lookup. Callers must handle the ``""`` case.

        Returns:
            Provider-specific approver login/name, or ``""`` when unavailable.
        """
        return ""

    def get_pr_token_login(self) -> str:
        """Return the PR-token identity login used for posting comments and dispatch.

        Best-effort helper for providers that can resolve the identity used for
        posting comments (e.g. ``SPECKIT_PR_TOKEN`` on GitHub).  Returns an empty
        string when the token is absent, resolution fails, or the provider does not
        support identity lookup.  Callers must handle the ``""`` case.

        Returns:
            Provider-specific PR-token login/name, or ``""`` when unavailable.
        """
        return ""

    @abstractmethod
    def merge_pr(self, pr_number: int, head_sha: str, method: str, *, commit_title: str | None = None) -> None:
        """Merge a pull request.

        Args:
            pr_number: Pull request number.
            head_sha: Expected HEAD SHA (for safety check).
            method: Merge method (e.g., "squash", "merge", "rebase").
            commit_title: Optional squash commit title (subject line only).
        """

    @abstractmethod
    def delete_branch(self, branch: str) -> None:
        """Delete a remote branch.

        Args:
            branch: Branch name to delete (e.g., "feature/my-branch").

        Raises:
            RuntimeError: If the branch could not be deleted.
        """

    @abstractmethod
    def publish_pr(self, pr_number: int) -> None:
        """Mark a draft pull request as ready for review.

        Args:
            pr_number: Pull request number.
        """

    @abstractmethod
    def squash_before_publish(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> None:
        """Squash or otherwise normalize a draft branch before publish.

        Implementations may perform provider-specific history normalization
        before publish and force-push the prepared branch when needed.
        Single-commit branches should remain a safe no-op for the squash phase
        while still ensuring the branch is pushed.
        """

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
    def list_pr_files(self, pr_number: int) -> list[str]:
        """List files changed in a pull request.

        Args:
            pr_number: Pull request number.

        Returns:
            List of file paths changed in the PR.
        """

    @abstractmethod
    def get_check_annotations(self, check_run_id: int, limit: int) -> list[str]:
        """Get annotations from a check run.

        Args:
            check_run_id: ID of the check run.
            limit: Maximum number of annotations to return.

        Returns:
            List of annotation messages.
        """

    @abstractmethod
    def dispatch_repair(
        self,
        pr_number: int,
        head_sha: str,
        repair_type: str,
        failed_checks: list[CheckRunStatus],
        review_comments: list[ReviewCommentInfo],
        review_id: int = 0,
        declared_author_comment_count: int = 0,
        declared_author_comment_counts_by_review: dict[int, int] | None = None,
    ) -> int:
        """Dispatch a repair by posting a @copilot comment on the PR.

        Posts an authenticated comment tagging ``@copilot`` that begins
        with ``@copilot`` (required for reliable AI agent session triggering).
        The comment body includes failing CI details and/or review feedback
        depending on the repair type.

        Args:
            pr_number: Pull request number.
            head_sha: Current HEAD SHA for the PR.
            repair_type: Type of repair (``"review"``, ``"ci"``, or ``"both"``).
            failed_checks: List of failed check runs with details.
            review_comments: Rich review comment metadata to include in the
                trigger comment.
            review_id: ID of the Copilot review that triggered the repair
                (used for the dedup marker and review URL in the comment body).
            declared_author_comment_count: Suppressed-comment count declared by the
                review body. When it exceeds the number of author comments that could
                be recovered, the dispatched comment names the shortfall so the repair
                agent can fetch the remainder from the review body.
            declared_author_comment_counts_by_review: Optional per-review declared
                suppressed-comment counts. When several prior reviews contribute to a
                repair dispatch, each affected review body gets its own shortfall
                notice and recovery fetch.

        Returns:
            The ID of the posted comment.
        """

    def dispatch_conflict_repair(
        self,
        pr_number: int,
        head_sha: str,
        base_sha: str,
        base_branch: str,
        head_branch: str,
    ) -> int:
        """Post a @copilot-tagged comment to resolve base-branch merge conflicts.

        The comment MUST begin with ``@copilot`` for reliable agent triggering.
        Uses ``AGDT_PR_APPROVER_PAT`` for authentication to ensure
        ``issues:write`` access.

        The dispatched instructions direct the cloud agent to merge
        ``origin/<base_branch>`` (not rebase), resolve conflicts using
        file-type-appropriate strategies, and push a normal commit —
        explicitly prohibiting ``git rebase``, ``git commit --amend``,
        ``git push --force``, and ``git push --force-with-lease``.

        Args:
            pr_number: Pull request number.
            head_sha: Current HEAD SHA of the PR branch.
            base_sha: Current tip SHA of the base branch (used in the
                idempotency marker).
            base_branch: Name of the base/target branch.
            head_branch: Name of the PR head/source branch.

        Returns:
            The ID of the posted comment.

        Raises:
            NotImplementedError: If the provider does not implement this method.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement dispatch_conflict_repair")

    def get_ref_sha(self, ref: str) -> str:
        """Return the commit SHA a branch/ref currently points at.

        Args:
            ref: Branch name or ref (e.g. ``"main"``).

        Returns:
            Full commit SHA, or an empty string when the ref cannot be
            resolved or the provider does not support this operation.
        """
        return ""

    @abstractmethod
    def list_review_comments(self, pr_number: int, review_id: int) -> list[ReviewCommentInfo]:
        """List inline comments from a specific review.

        Args:
            pr_number: Pull request number.
            review_id: ID of the review to list comments for.

        Returns:
            List of rich review comment metadata.
        """

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
    ) -> None:
        """Rebase the head branch onto the base branch and force-push.

        Performs: fetch → checkout → rebase → conflict resolution → force-push-with-lease.

        Args:
            pr_number: Pull request number (for logging).
            base_branch: Target branch to rebase onto.
            head_branch: Source branch to rebase.
            head_sha: Current HEAD SHA (for safety).

        Raises:
            RebaseConflictError: When rebase conflicts cannot be auto-resolved.
            ForceWithLeaseError: When force-push-with-lease fails.
            NotImplementedError: When the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement rebase_onto_base")

    def get_commit_author_login(self, sha: str) -> str:
        """Return the GitHub login of the commit author for ``sha``.

        Returns an empty string when the provider does not support this
        operation or the author cannot be mapped to a GitHub login.

        Args:
            sha: Commit SHA to resolve.
        """
        return ""

    def list_relevant_pull_requests(
        self,
        *,
        cursor: str | None = None,
        limit: int = 25,
    ) -> tuple[list[PRMetadata], str | None]:
        """List one page of relevant open pull requests.

        Providers may override this method to expose a complete, cursor-based
        inventory.  The default keeps older providers source-compatible while
        making unsupported inventory explicit to callers.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_relevant_pull_requests")

    def get_pr_copilot_attribution(self, pr_number: int, *, observation_watermark: str = "") -> dict[str, bool | str]:
        """Return whether a pull request has Copilot activity after a watermark."""
        raise NotImplementedError(f"{type(self).__name__} does not implement get_pr_copilot_attribution")

    def reclaim_copilot_commit(
        self,
        *,
        pr_number: int,
        head_branch: str,
        head_sha: str,
    ) -> None:
        """Re-author the HEAD commit under the CI identity and force-push.

        Reclaims a Copilot-authored HEAD so the force-push emits a ``synchronize``
        event from a human pusher and the required ``pull_request`` checks run
        (Copilot/automation pushes are suppressed by GitHub's automation-origin
        exception to the *Require approval for workflow runs* policy).

        Args:
            pr_number: Pull request number (for logging).
            head_branch: Source branch to reclaim.
            head_sha: Current HEAD SHA (safety check before reclaim).

        Raises:
            NotImplementedError: When the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement reclaim_copilot_commit")

    def graphql(self, *, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL query or mutation against the GitHub API.

        Args:
            query: The GraphQL query or mutation string.
            variables: Optional dictionary of query variables.

        Returns:
            Parsed JSON response as a dictionary.

        Raises:
            NotImplementedError: If the provider does not support GraphQL.
            RetryableError: On rate limit or transient failures.
            RuntimeError: On non-retryable API errors.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement graphql")

    def list_workflow_runs(
        self,
        workflow_id: str,
        *,
        window_hours: int = 24,
        include_dispatch_inputs: bool = False,
    ) -> list[WorkflowRun]:
        """List recent completed workflow runs for the specified workflow.

        Implementations should query the CI platform for completed runs within
        the given time window.

        Args:
            workflow_id: Workflow file name or numeric ID.
            window_hours: How far back to look for runs (in hours).
            include_dispatch_inputs: When ``True``, resolve ``inputs.pr_number``
                from per-run workflow details for ``workflow_dispatch`` runs
                that do not expose ``pull_requests[].number`` in list payloads.

        Returns:
            List of WorkflowRun instances.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_workflow_runs")

    def rerun_workflow(self, run_id: int) -> None:
        """Trigger a re-run of all jobs for the given workflow run.

        Args:
            run_id: The workflow run ID to re-run.

        Raises:
            NotImplementedError: If the provider does not support this operation.
            RuntimeError: If the re-run API call fails.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement rerun_workflow")

    def list_eligible_prs(self, max_prs: int | None = None) -> list[EligiblePR]:
        """List open PRs eligible for AI loop processing, in creation order.

        Applies platform-specific eligibility filters:
        - Excludes fork PRs (isCrossRepository)
        - Excludes PRs with ``ai-pr-loop-ignore`` label
        - Excludes human-blocked PRs

        Args:
            max_prs: Optional maximum number of eligible PRs to return.

        Returns:
            Sorted list (oldest-first) of EligiblePR dataclasses.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_eligible_prs")

    def list_supervisor_prs(self, max_prs: int | None = None) -> list[EligiblePR]:
        """List bounded open PRs for read-only supervisor scanning.

        Unlike :meth:`list_eligible_prs`, this inventory keeps human-blocked and
        audit-handoff PRs so the supervisor can classify them explicitly. It
        still excludes fork PRs and PRs carrying the ignore label.

        Args:
            max_prs: Optional maximum number of PRs to return.

        Returns:
            Sorted list (oldest-first) of EligiblePR dataclasses.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_supervisor_prs")

    def get_recent_dispatch_history(self, workflow: str) -> list[DispatchEvent]:
        """Get recent dispatch events for a workflow (for cursor fallback).

        Queries recent completed workflow runs and infers the dispatched PR
        number using two sources, tried in order:

        1. ``pull_requests[].number`` on the workflow run object — populated
           when the run was triggered by a pull-request event and GitHub
           associates it automatically.
        2. The run name — parsed with a ``#<number>`` pattern for runs whose
           name was set explicitly (e.g., via ``run-name`` in the workflow
           YAML) to include the PR number.

        Args:
            workflow: Workflow file name (e.g., "ai-pr-loop.yml").

        Returns:
            List of DispatchEvent instances sorted most-recent-first.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_recent_dispatch_history")

    def dispatch_workflow(self, workflow: str, inputs: dict[str, str]) -> None:
        """Dispatch a workflow_dispatch event with the given inputs.

        Args:
            workflow: Workflow file name (e.g., "ai-pr-loop.yml").
            inputs: Dictionary of input field names to values.

        Raises:
            NotImplementedError: If the provider does not support this operation.
            RuntimeError: If the dispatch fails.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement dispatch_workflow")

    def get_variable(self, name: str, *, use_writer_token: bool = False) -> str | None:
        """Read a repository Actions variable by name.

        Args:
            name: Variable name (e.g., "AI_PR_LOOP_LAST_DISPATCHED_PR").
            use_writer_token: When True, prefer the writer credential if the
                provider supports one.

        Returns:
            The variable value as a string, or None when the variable is not set.

        Raises:
            RuntimeError: If the variable cannot be read because of permission,
                availability, or transport failures.

            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_variable")

    def set_variable(self, name: str, value: str) -> None:
        """Create or update a repository Actions variable.

        Requires REPO_VARIABLE_WRITER_PAT to be configured.

        Args:
            name: Variable name (e.g., "AI_PR_LOOP_LAST_DISPATCHED_PR").
            value: Variable value to set.

        Raises:
            NotImplementedError: If the provider does not support this operation.
            VariableWriteError: When the write cannot be performed.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement set_variable")

    def validate_variable_token(self) -> bool:
        """Validate that REPO_VARIABLE_WRITER_PAT is configured and functional.

        Returns:
            True if the token is valid and has sufficient permissions, False otherwise.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement validate_variable_token")

    # ------------------------------------------------------------------
    # Audit methods (concrete defaults raising NotImplementedError)
    #
    # These methods support the review feedback audit workflow. They are
    # opt-in: only providers that participate in auditing need to override.
    # ------------------------------------------------------------------

    def list_closed_prs(
        self,
        *,
        exclude_labels: list[str],
        limit: int,
        state: str = "closed",
    ) -> list[ClosedPRInfo]:
        """List closed PRs excluding those with specified labels.

        Returns newest-closed PRs first (sorted by ``closed_at`` descending).

        Args:
            exclude_labels: Labels to exclude from results.
            limit: Maximum number of PRs to return.
            state: PR state filter (default "closed").

        Returns:
            List of ``ClosedPRInfo`` dataclass instances.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Use ``GitPullRequestSearchCriteria`` with
        ``status=completed|abandoned`` and filter by tag absence. Sort by
        ``closedDate`` descending.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_closed_prs")

    def claim_pr_for_audit(self, pr_number: int, label: str) -> ClaimResult:
        """Attempt to claim a PR for audit by adding a label.

        Uses a GET-then-POST pattern: checks if the label is already
        present, then adds it if absent. Returns the claim result.

        This is best-effort, not atomic — concurrent runs may both observe
        the label absent and both proceed. Idempotency and deduplication
        are enforced downstream.

        Args:
            pr_number: PR number to claim.
            label: Label to add as the claim marker.

        Returns:
            ``ClaimResult.CLAIMED`` if newly added,
            ``ClaimResult.ALREADY_CLAIMED`` if already present.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Use PR tags (``GET /pullRequests/{id}/labels``
        then ``POST /pullRequests/{id}/labels``). Handle 409 Conflict as
        ALREADY_CLAIMED.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement claim_pr_for_audit")

    def add_label(self, pr_number: int, label: str) -> None:
        """Add a label to a PR (idempotent).

        If the label is already present, this is a no-op.

        Args:
            pr_number: PR number.
            label: Label name to add.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: ``POST /pullRequests/{id}/labels`` with the
        tag name. Handle 409 as success (already exists).
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement add_label")

    def remove_label(self, pr_number: int, label: str) -> None:
        """Remove a label from a PR (idempotent).

        If the label is not present, this is a no-op.

        Args:
            pr_number: PR number.
            label: Label name to remove.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: ``DELETE /pullRequests/{id}/labels/{labelId}``.
        Handle 404 as success (already absent).
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement remove_label")

    def count_prs_without_labels(
        self,
        *,
        exclude_labels: list[str],
        state: str = "closed",
    ) -> int:
        """Count closed PRs that do NOT have any of the specified labels.

        Used for threshold checks before triggering an audit batch.

        Args:
            exclude_labels: Labels whose absence qualifies a PR for counting.
            state: PR state filter (default "closed").

        Returns:
            Count of matching PRs.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Use search criteria with tag exclusion
        and count the results.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement count_prs_without_labels")

    def list_all_review_comments(self, pr_number: int) -> list[ReviewCommentInfo]:
        """List ALL review comments for a PR (across all reviews).

        Unlike ``list_review_comments()`` which requires a specific review ID,
        this method returns all inline review comments for the PR regardless
        of which review they belong to. Pagination is handled internally.

        Args:
            pr_number: PR number.

        Returns:
            List of ReviewCommentInfo for all review comments.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: ``GET /pullRequests/{id}/threads`` with
        ``threadContext`` filtering for inline comments.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_all_review_comments")

    def create_pull_request(
        self,
        title: str,
        body: str,
        *,
        draft: bool = True,
    ) -> str:
        """Create a pull request on the current branch.

        Args:
            title: PR title.
            body: PR body/description (Markdown).
            draft: Whether to create the PR as a draft (default True).

        Returns:
            URL of the created PR, or empty string on failure.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: ``POST /pullRequests`` with ``isDraft=True``.
        The return value should be the PR web URL.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement create_pull_request")

    def create_audit_tracking_issue(self, *, batch_id: str, pr_numbers: list[int]) -> int:
        """Create a per-batch tracking issue for review-feedback audit.

        Args:
            batch_id: Audit batch identifier.
            pr_numbers: PR numbers included in the batch.

        Returns:
            Created issue number/ID.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Create a work item (for example a Task)
        containing the batch summary and return the work item ID.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement create_audit_tracking_issue")

    def dispatch_audit_evaluation(
        self,
        *,
        tracking_issue: int,
        batch_id: str,
        batch_branch: str,
        batch_dir: str,
        pr_numbers: list[int],
    ) -> AgentAssignmentResult:
        """Dispatch the review-feedback audit evaluation agent.

        Args:
            tracking_issue: Tracking issue ID/number used as dispatch surface.
            batch_id: Audit batch identifier.
            batch_branch: Branch containing the prepared batch files.
            batch_dir: Repo-relative batch directory path.
            pr_numbers: PR numbers included in the batch.

        Returns:
            Structured assignment result, including method/task metadata.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Trigger the provider's coding-agent assignment
        flow and return equivalent assignment metadata.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement dispatch_audit_evaluation")

    def find_deferral_issue(self, *, pr_number: int, review_id: int) -> int | None:
        """Return the open deferral issue already filed for ``(pr_number, review_id)``.

        Makes :meth:`create_deferral_issue` recoverable: when a previous run created
        the issue but failed before its PR marker was posted, the next run must reuse
        that issue instead of filing a duplicate.

        Args:
            pr_number: PR whose suppressed comments are being deferred.
            review_id: Copilot review the suppressed comments were raised by.

        Returns:
            Issue number/ID of the matching open deferral issue, or ``None`` when no
            such issue exists.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: query work items carrying the deferral tag and match
        the same marker payload.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement find_deferral_issue")

    def create_deferral_issue(
        self,
        *,
        pr_number: int,
        review_id: int,
        base_sha: str,
        findings: list[tuple[str, str]],
        labels: list[str],
    ) -> int:
        """Create the follow-up triage issue for a deferred suppressed-only review.

        The issue body is the input contract consumed by the
        ``agdt.suppressed-comment-triage.evaluate`` agent (see
        ``docs/suppressed-comment-triage-contract.md``).

        Args:
            pr_number: PR whose suppressed comments are being deferred.
            review_id: Copilot review the suppressed comments were raised by.
            base_sha: Commit SHA the findings were raised against.
            findings: ``(path, comment_body)`` pairs, in review-body order.
            labels: Labels to apply at creation.

        Returns:
            Created issue number/ID.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: create a work item carrying the same body and tags.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement create_deferral_issue")

    def dispatch_suppressed_triage(
        self,
        *,
        issue_number: int,
        pr_number: int,
        review_id: int,
    ) -> AgentAssignmentResult:
        """Dispatch the suppressed-comment triage agent onto a deferral issue.

        Args:
            issue_number: Deferral issue used as the dispatch surface.
            pr_number: PR the deferred findings came from.
            review_id: Copilot review the deferred findings came from.

        Returns:
            Structured assignment result, including method/task metadata.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: trigger the provider's coding-agent assignment flow.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement dispatch_suppressed_triage")

    def count_open_issues_with_label(self, label: str) -> int:
        """Return the number of open issues carrying *label*.

        Used as the deferral circuit breaker: the loop refuses to create another
        deferral issue while the open backlog is at its ceiling.

        Args:
            label: Label name to filter on.

        Returns:
            Count of open issues carrying the label.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: query open work items by tag and return the count.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement count_open_issues_with_label")

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

    def post_issue_comment(self, issue_number: int, body: str) -> int:
        """Post a comment on an issue.

        Args:
            issue_number: Issue number to comment on.
            body: Comment body.

        Returns:
            The created comment ID.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: add a work item comment.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement post_issue_comment")

    def close_issue(self, issue_number: int, *, reason: str = "completed") -> None:
        """Close an issue.

        Args:
            issue_number: Issue number to close.
            reason: Platform close reason (``"completed"`` or ``"not_planned"``).

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: transition the work item to a closed state.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement close_issue")

    def close_pr(self, pr_number: int, *, comment: str | None = None) -> None:
        """Close a pull request without merging it.

        Args:
            pr_number: PR number to close.
            comment: Optional comment posted before closing.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: abandon the pull request.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement close_pr")
