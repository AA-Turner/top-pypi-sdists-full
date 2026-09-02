"""CI provider data models.

Dataclasses representing normalized CI platform events and metadata.
These are provider-agnostic — each provider's ``parse_event()`` method
normalizes platform-specific payloads into these structures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class EventPayload:
    """Normalized CI event payload.

    Attributes:
        pr_number: Pull request number (0 if not a PR event).
        head_branch: Head branch name.
        head_sha: HEAD commit SHA.
        base_branch: Base/target branch name.
        action: Event action (e.g., "opened", "synchronize", "submitted").
        trigger_label: Label name that triggered the event (empty if not a label event).
        repository_full_name: Full repository name (e.g., "owner/repo").
        sender_login: Login of the event sender/actor, when available.
        title_changed: Whether the PR title was changed in an edit event.
        body_changed: Whether the PR body/description was changed in an edit event.
        base_changed: Whether the base/target branch was changed in an edit event.
        edit_changes_known: Whether the provider had reliable per-field change
            metadata for an edited event. When False, the edit-relevance guard
            fails open (does not skip).
    """

    pr_number: int = 0
    head_branch: str = ""
    head_sha: str = ""
    base_branch: str = ""
    action: str = ""
    trigger_label: str = ""
    repository_full_name: str = ""
    sender_login: str = ""
    title_changed: bool = False
    body_changed: bool = False
    base_changed: bool = False
    edit_changes_known: bool = False


@dataclass(frozen=True)
class PRMetadata:
    """Pull request metadata retrieved from the CI platform.

    Attributes:
        number: PR number.
        title: PR title.
        head_branch: Source branch name.
        head_sha: HEAD commit SHA.
        base_branch: Target branch name.
        head_repo_full_name: Full name of the head (source) repository.
        base_repo_full_name: Full name of the base (target) repository.
        labels: List of label names on the PR.
        requested_reviewers: List of pending reviewer logins on the PR.
        is_draft: Whether the PR is a draft.
        mergeable: Whether the PR is mergeable (None if unknown).
        mergeable_state: Fine-grained mergeability state from the GitHub REST API
            (e.g. ``"clean"``, ``"dirty"``, ``"blocked"``, ``"behind"``, ``""``).
            ``"dirty"`` is the authoritative signal for a real base-branch conflict.
            Defaults to ``""`` when the field is absent from the API response so that
            existing constructors and tests are unaffected.
    """

    number: int
    title: str
    head_branch: str
    head_sha: str
    base_branch: str
    head_repo_full_name: str = ""
    base_repo_full_name: str = ""
    labels: list[str] = field(default_factory=list)
    requested_reviewers: list[str] = field(default_factory=list)
    is_draft: bool = False
    mergeable: bool | None = None
    mergeable_state: str = ""


@dataclass(frozen=True)
class CheckRunStatus:
    """Status of a single CI check run.

    Attributes:
        id: Check run ID.
        name: Check run name.
        status: Run status (e.g., "completed", "in_progress", "queued").
        conclusion: Run conclusion (e.g., "success", "failure", "neutral").
            Empty string if not yet completed.
        html_url: Direct HTML URL to view this check run in the GitHub UI.
            Prefer this over constructing a URL from ``id``, since the check
            run ID does not match the Actions workflow run ID.
            Empty string when not available.
    """

    id: int
    name: str
    status: str
    conclusion: str = ""
    html_url: str = ""


@dataclass(frozen=True)
class FailedStepLog:
    """Condensed log for a single failing CI step.

    Attributes:
        step_name: Name of the failing step. An empty string means there is no
            per-step breakdown — ``condensed_log`` covers the whole job and is
            rendered as a single block (no nested per-step ``<details>``).
        condensed_log: Condensed log text for this step (or the whole job).
    """

    step_name: str
    condensed_log: str


@dataclass(frozen=True)
class FailedCheckContext:
    """Display metadata and per-step condensed logs for a failing CI check.

    Attributes:
        display_name: Full check name as shown in the PR checks list,
            ``"<workflow_name> / <job_name> (<event>)"`` with segments dropped
            gracefully when unavailable. Empty when nothing could be resolved,
            in which case the renderer falls back to the raw check name.
        step_logs: Condensed logs for the failing steps only. Empty means the
            check renders link-only (no condensed-output block).
    """

    display_name: str
    step_logs: tuple[FailedStepLog, ...]


@dataclass(frozen=True)
class ReviewInfo:
    """Information about a pull request review.

    Attributes:
        id: Review ID.
        user: Username of the reviewer.
        state: Review state (e.g., "APPROVED", "CHANGES_REQUESTED", "COMMENTED").
        body: Review body text.
        commit_sha: Commit SHA that this review targets.
        submitted_at: ISO 8601 timestamp when the review was submitted (empty if unknown).
    """

    id: int
    user: str
    state: str
    body: str = ""
    commit_sha: str = ""
    submitted_at: str = ""


# Copilot login names used in review detection (provider-agnostic)
COPILOT_REVIEWER_LOGIN = "copilot-pull-request-reviewer[bot]"
COPILOT_LOGINS = frozenset(
    {
        "Copilot",
        "copilot[bot]",
        "copilot-swe-agent[bot]",
        COPILOT_REVIEWER_LOGIN,
    }
)
# All Copilot identities that may leave comments (same set as COPILOT_LOGINS)
COPILOT_COMMENT_LOGINS = COPILOT_LOGINS
# Exact identities used by the Cloud Coding Agent, excluding the CCR reviewer bot.
CLOUD_CODING_AGENT_LOGINS = frozenset(
    {
        "copilot-swe-agent[bot]",
        "copilot-swe-agent",
        "app/copilot-swe-agent",
    }
)
# Logins whose HEAD commits should trigger takeover — extends COPILOT_LOGINS with
# github-actions[bot] so automation-authored commits are also reclaimed, without
# polluting the Copilot-review-detection sets with a generic CI identity.
TAKEOVER_HEAD_AUTHOR_LOGINS = COPILOT_LOGINS | frozenset({"github-actions[bot]"})

_COPILOT_LOGINS_CASEFOLDED = frozenset(login.casefold() for login in COPILOT_LOGINS)
_CLOUD_CODING_AGENT_LOGINS_CASEFOLDED = frozenset(login.casefold() for login in CLOUD_CODING_AGENT_LOGINS)


def is_copilot_login(login: object) -> bool:
    """Return True when *login* belongs to a known Copilot identity (case-insensitive).

    GitHub logins are case-insensitive, so the comparison is performed on the
    casefolded form of *login* against the pre-computed casefolded set. Any
    non-string value returns ``False``.
    """
    if not isinstance(login, str):
        return False
    return login.casefold() in _COPILOT_LOGINS_CASEFOLDED


def is_cloud_coding_agent_login(login: object) -> bool:
    """Return True when *login* is an exact Cloud Coding Agent identity."""
    if not isinstance(login, str):
        return False
    return login.casefold() in _CLOUD_CODING_AGENT_LOGINS_CASEFOLDED


@dataclass(frozen=True)
class ReviewCommentInfo:
    """Rich metadata for a single PR review comment.

    Attributes:
        id: Database ID of the review comment.
        path: File path the comment is on.
        body: Full comment text (the reviewer's feedback).
        html_url: Direct link to the inline comment on GitHub.
        is_suppressed: Whether the comment has been minimized/suppressed on GitHub.
        start_line: Start line number the comment targets (None for file-level).
        end_line: End line number the comment targets (single-line comments set
            this to the anchor line; None only when line metadata is unavailable).
        line: Line number the comment targets (None if PR-level).
        position: Diff position the comment targets (None if PR-level).
        diff_hunk: Diff hunk context from the API (empty if not available).
        commit_id: SHA of the commit the comment was placed on (empty if not available).
            GitHub may remap this to the current HEAD after squash/force-push.
        original_commit_id: The original commit SHA the comment was placed on, before
            any remapping by GitHub (empty if not available). Use this for guards that
            compare whether the comment predates the current HEAD.
        source_review_id: ID of the review body that originally carried this comment.
            For inline comments this is their parent review; for synthetic body-only
            suppressed comments this identifies the review whose body must be fetched
            if the embedded comment text is trimmed.
        author_login: Login of the review comment author when available.
        in_reply_to_id: Review comment ID this comment replies to (None for root).
    """

    id: int
    path: str
    body: str
    html_url: str
    is_suppressed: bool = False
    start_line: int | None = None
    end_line: int | None = None
    line: int | None = None
    position: int | None = None
    diff_hunk: str = ""
    commit_id: str = ""
    original_commit_id: str = ""
    source_review_id: int = 0
    author_login: str = ""
    in_reply_to_id: int | None = None


@dataclass(frozen=True)
class IssueCommentInfo:
    """Metadata for a pull request issue comment.

    Attributes:
        id: Database ID of the issue comment.
        author: Login of the comment author.
        body: Full comment body text.
        created_at: ISO 8601 creation timestamp.
    """

    id: int
    author: str
    body: str = ""
    created_at: str = ""


# Copilot session event type strings from the GitHub Issues Events API
COPILOT_SESSION_EVENT_FINISHED = "copilot_work_finished"
COPILOT_SESSION_EVENT_FINISHED_FAILURE = "copilot_work_finished_failure"
COPILOT_SESSION_EVENT_STARTED = "copilot_work_started"

_COPILOT_SESSION_EVENTS = frozenset(
    {
        COPILOT_SESSION_EVENT_FINISHED,
        COPILOT_SESSION_EVENT_FINISHED_FAILURE,
        COPILOT_SESSION_EVENT_STARTED,
    }
)


@dataclass(frozen=True)
class IssueEvent:
    """A single issue/PR timeline event from the GitHub Issues Events API.

    Attributes:
        id: Event ID.
        event: Event type string (e.g., "copilot_work_finished",
               "copilot_work_finished_failure", "copilot_work_started").
        created_at: ISO 8601 timestamp string when the event was created.
        actor_login: Login of the actor who triggered the event (empty if unknown).
    """

    id: int
    event: str
    created_at: str
    actor_login: str = ""


@dataclass(frozen=True)
class RepairDecision:
    """Result of the dispatch decision for repair.

    Attributes:
        repair_needed: Whether a repair dispatch should be triggered.
        repair_type: Type of repair needed: ``"review"``, ``"ci"``, or ``"both"``.
            Empty string when no repair is needed.
        review_id: ID of the actionable Copilot review (CHANGES_REQUESTED or
            COMMENTED with inline comments; 0 if N/A).
        review_comments: Rich review comment metadata pre-fetched during detection
            (populated for COMMENTED reviews; empty for CHANGES_REQUESTED so
            that ``_dispatch_repair`` fetches them lazily).
        failed_checks: Failed check run details (name, status, conclusion).
    """

    repair_needed: bool = False
    repair_type: str = ""
    review_id: int = 0
    review_comments: tuple[ReviewCommentInfo, ...] = ()
    failed_checks: tuple[CheckRunStatus, ...] = ()


class VerificationVerdict(Enum):
    """Verdict from the SDK verification of a review comment against the diff.

    Attributes:
        COMMENT_RESOLVE: The comment has been addressed by the diff.
        COMMENT_UNRESOLVE: The comment has NOT been addressed by the diff.
    """

    COMMENT_RESOLVE = "COMMENT_RESOLVE"
    COMMENT_UNRESOLVE = "COMMENT_UNRESOLVE"


@dataclass(frozen=True)
class CommentResolution:
    """Resolution result for a single review comment.

    Attributes:
        comment_id: Database ID of the review comment.
        thread_id: Thread/node ID for GraphQL resolution (empty if unknown).
        verdict: SDK verdict for this comment.
        error: Error message if SDK call failed (empty on success).
    """

    comment_id: int
    thread_id: str = ""
    verdict: VerificationVerdict = VerificationVerdict.COMMENT_UNRESOLVE
    error: str = ""


@dataclass(frozen=True)
class FinalizationResult:
    """Result of the post-repair finalization process.

    Attributes:
        skipped: Whether finalization was skipped entirely (e.g., no new commit).
        reason: Human-readable reason when skipped or for summary purposes.
        resolved_count: Number of comments resolved.
        unresolved_count: Number of real (positive-ID) comments left unresolved.
            Synthetic suppressed entries recovered from a review body carry
            negative sentinel IDs and have no GitHub thread, so they can never be
            resolved and are excluded here — they are reported in
            ``suppressed_count`` instead. This keeps the count aligned with
            ``snapshot.count_unresolved_prior_threads``, which also skips
            ``id < 0``.
        suppressed_count: Number of synthetic suppressed entries (negative
            sentinel IDs) recorded for reporting. Informational only — these
            never block the merge gate.
        resolutions: Individual resolution results per comment.
        errors: List of error messages encountered during finalization.
    """

    skipped: bool = False
    reason: str = ""
    resolved_count: int = 0
    unresolved_count: int = 0
    suppressed_count: int = 0
    resolutions: tuple[CommentResolution, ...] = ()
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class SquashResult:
    """Result of a post-repair squash operation.

    Records the actual tree identity observed before and after the squash so
    callers can verify that the squash preserved the tree, rather than relying
    on a pre-execution snapshot flag (e.g. ``commits_behind``). ``squash_post_repair``
    may refetch base/head and perform a second reset/squash to absorb a commit
    pushed during finalization, so the resulting tree can differ from the
    pre-execution snapshot even when the branch was not behind base beforehand.

    Attributes:
        before_tree: Git tree SHA of the pre-squash HEAD (``head_sha``) that
            carried the pre-squash CI result. Empty when it could not be resolved.
        after_tree: Git tree SHA of the final squashed HEAD after force-push.
            Empty when it could not be resolved.
        after_sha: Commit SHA of the final squashed HEAD after force-push.
            Empty when it could not be resolved. Used by the runner to verify
            that the refreshed snapshot still points to the squashed commit
            before restoring the ``squash_preserved_green`` flag.
    """

    before_tree: str = ""
    after_tree: str = ""
    after_sha: str = ""

    @property
    def tree_preserved(self) -> bool:
        """True only when both trees resolved and are identical."""
        return bool(self.before_tree) and self.before_tree == self.after_tree


@dataclass(frozen=True)
class ReviewCommentTarget:
    """A single PR comment selected for deletion by the review-comment cleanup.

    Attributes:
        thread_id: ID of the comment thread the comment belongs to.
        comment_id: ID of the comment within the thread.
        comment_type: Azure DevOps comment type (always ``"text"`` for deletable comments).
        marker_type: The ``agdt-review`` marker type (e.g. ``"file-summary"``) when the
            comment was matched by its marker, or ``None`` when matched only by author.
        snippet: A short, human-readable excerpt of the comment content (marker stripped).
        deleted: Whether the comment was successfully deleted (set during ``--execute``).
        error: Error detail when deletion failed, or ``None`` on success / dry-run.
    """

    thread_id: int
    comment_id: int
    comment_type: str
    marker_type: str | None
    snippet: str
    deleted: bool = False
    error: str | None = None


@dataclass(frozen=True)
class ReviewCommentDeletionResult:
    """Outcome of a review-comment deletion request.

    Attributes:
        executed: ``False`` for a dry-run (nothing deleted), ``True`` when deletions ran.
        targets: The comments selected for deletion; in execute mode each target carries
            its per-comment outcome via :attr:`ReviewCommentTarget.deleted` / ``error``.
    """

    executed: bool
    targets: tuple[ReviewCommentTarget, ...] = ()

    @property
    def selected_count(self) -> int:
        """Number of comments selected for deletion."""
        return len(self.targets)

    @property
    def deleted_count(self) -> int:
        """Number of comments successfully deleted (always 0 for a dry-run)."""
        return sum(1 for target in self.targets if target.deleted)

    @property
    def failed_count(self) -> int:
        """Number of comments whose deletion failed."""
        return sum(1 for target in self.targets if target.error is not None)


@dataclass(frozen=True)
class NoChangePRBrief:
    """Cheap listing data for one candidate no-change follow-up pull request.

    Carries everything the suppressed-triage reaper needs to reject a pull
    request without spending further API calls: the author, the raw body (the
    only place the anchored marker is trusted) and the diff statistics.

    Attributes:
        number: Pull request number.
        author_login: Login of the pull request author.
        body: Raw pull request body, exactly as stored by the platform.
        changed_files: Number of files the pull request changes.
        additions: Number of added lines.
        deletions: Number of deleted lines.
        head_branch: Source branch name.
        is_cross_repository: Whether the head branch lives in a fork.
    """

    number: int
    author_login: str
    body: str
    changed_files: int
    additions: int
    deletions: int
    head_branch: str = ""
    is_cross_repository: bool = False


@dataclass(frozen=True)
class PRTreeState:
    """Tree identity of a pull request head against its merge base.

    Attributes:
        merge_base_sha: Merge base of ``base.sha`` and ``head.sha``.
        merge_base_tree_sha: Git tree SHA at ``merge_base_sha``.
        head_tree_sha: Git tree SHA at ``head.sha``.
        head_sha: The pull request HEAD commit SHA that produced ``head_tree_sha``.
    """

    merge_base_sha: str
    merge_base_tree_sha: str
    head_tree_sha: str
    head_sha: str = ""

    @property
    def tree_identical(self) -> bool:
        """True only when both trees resolved and are identical."""
        return bool(self.merge_base_tree_sha) and self.merge_base_tree_sha == self.head_tree_sha


@dataclass(frozen=True)
class IssueFacts:
    """Minimal issue state used for cross-checking a deferral issue.

    Attributes:
        number: Issue number.
        state: Issue state, lowercased (``"open"`` or ``"closed"``).
        body: Raw issue body.
        resource_kind: Whether the ``/issues/{number}`` target is a genuine issue
            or a pull request masquerading behind the shared endpoint.
    """

    number: int
    state: str
    body: str
    resource_kind: str = "issue"
