"""PR state snapshot and derived state for the pipeline."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from agentic_devtools.cli.ci.actionable_checks import DEFAULT_ACTIONABLE_CHECK_NAMES
from agentic_devtools.cli.ci.guards import find_repair_satisfied_review_id
from agentic_devtools.cli.ci.models import (
    CheckRunStatus,
    ReviewCommentInfo,
    ReviewInfo,
    is_cloud_coding_agent_login,
    is_copilot_login,
)
from agentic_devtools.cli.ci.pipeline.deferral import (
    find_suppressed_deferral_state,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_API_ERROR,
    CopilotGateVerdict,
    evaluate_copilot_gate_verdict,
    is_copilot_or_synthetic_review,
    is_suppressed_only_block,
    select_prior_actionable_reviews,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.retry import ProviderRateLimitError
from agentic_devtools.cli.github.ccr_review_format import parse_suppressed_count

logger = logging.getLogger(__name__)


def _raise_if_rate_limit(exc: Exception) -> None:
    """Re-raise actual provider rate limits so caller can return paused exit."""
    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
        raise


@dataclass(frozen=True)
class PRStateSnapshot:
    """Immutable snapshot of all PR state gathered in one pass.

    Attributes:
        pr_number: The pull request number.
        head_sha: Current HEAD commit SHA.
        base_branch: Target branch name.
        head_branch: Source branch name.
        commit_count: Number of commits above merge-base.
        ci_status: Overall CI status ("passing", "failing", "pending", "unknown").
        ci_failed_checks: List of failed check run names.
        review_state: Latest genuine or trusted synthetic Copilot review state on
            HEAD (or empty string).
        copilot_review_id: ID of the latest genuine or trusted synthetic Copilot
            review on HEAD (0 if none).
        copilot_review_inline_count: Number of inline comments in the latest genuine
            or trusted synthetic Copilot review; `-1` indicates the count is unknown
            because review comments could not be fetched.
        effective_review_comment_count: Number of comments remaining after the same
            reply and thread-state filtering used by repair dispatch; ``None`` means
            the effective inventory could not be determined and callers must fail open.
        effective_review_comment_count_review_id: Review id whose comments produced
            ``effective_review_comment_count``. ``None`` means no source review was
            available (for example, when no current Copilot review targets HEAD).
        effective_review_comment_filter_applied: Whether at least one fetched
            positive-id review comment was removed by reply/thread-state filtering
            while deriving ``effective_review_comment_count``. ``None`` means the
            inventory was unknown.
        active_session: Whether a Copilot coding session is currently active.
        copilot_review_pending: Whether Copilot is pending as a reviewer.
        unresolved_threads: Number of unresolved Copilot review threads not owned by the
            gate verdict (i.e. from reviews whose ID differs from the verdict's effective
            ``review_id``). When the gate has no valid verdict (``review_id == 0``), all
            actionable threads are counted (fail-closed). When ``unresolved_threads_degraded``
            is True this holds a conservative
            blocking fallback value rather than a measured thread count.
        unresolved_threads_degraded: Whether the provider could not report review-thread
            state (capability missing/unimplemented, the lookup failed, the returned
            mapping omitted selected comments, or a review's comments could not be
            listed), so ``unresolved_threads`` is unknown. The gate fails closed on this signal and
            the run summary reports "degraded / unknown" instead of a fabricated integer.
        unresolved_threads_unknown_provenance: Whether the gate-verdict review ID could not be
            resolved when ``unresolved_threads`` was computed, so the count covers *all*
            actionable reviews (the conservative count-all floor) rather than being scoped
            to reviews whose ID differs from the verdict's owner. The count is still
            authoritative — it is the maximum possible value — but consumers can use this
            flag to emit extra diagnostics. No additional gate blocking is required: the
            count-all strategy is already the most conservative possible reading.
        repairable_threads: Number of all unresolved Copilot review threads from any
            actionable Copilot review (current or prior). Unlike ``unresolved_threads``,
            this is independent of the gate verdict and is used solely to determine if
            there is repairable work, decoupled from whether those threads are blocking.
        labels: List of labels on the PR.
        is_draft: Whether the PR is a draft.
        mergeable: Whether the PR is mergeable (None if unknown).
        mergeable_state: Fine-grained mergeability state reported by the provider
            (e.g. ``"clean"``, ``"dirty"``, ``"blocked"``, ``"behind"``, ``"unknown"``).
            ``"dirty"`` is the authoritative signal for a real base-branch conflict.
            Empty string when the provider does not report it.
        requested_reviewers: List of pending reviewer logins.
        has_approval_on_head: Whether an approval exists targeting the current HEAD.
        approver_login: GitHub login of the approver-PAT identity (resolved via
            ``GET /user`` with ``AGDT_PR_APPROVER_PAT``).  Empty string when the token
            is not configured or login resolution failed.  Used together with
            ``has_approver_approval_on_head`` for precise approve-action idempotency.
        has_approver_approval_on_head: Whether the approver-PAT identity has already
            approved the current HEAD.  Computed from ``approver_login`` and the
            effective HEAD reviews — only ``True`` when ``approver_login`` is non-empty,
            a matching APPROVED review exists on HEAD, and that review carries a non-empty
            ``commit_sha`` (reviews with an unknown target SHA fail closed and are not
            treated as current).  Used as the idempotency guard for ``ApproveAction`` so
            that the loop skips the API call only when its own required approval is already
            present on HEAD, without treating incidental human approvals as the loop's own.
        title: PR title.
        head_repo_full_name: Full name of the head repository.
        base_repo_full_name: Full name of the base repository.
        files: List of files changed in the PR.
        check_runs: All check run statuses.
        reviews: All reviews for the PR.
        has_changes: Whether the PR has file changes.
        commits_behind: Number of commits the head branch is behind the base branch.
        head_author_login: GitHub login of the HEAD commit's author ("" if unknown).
        copilot_gate_verdict: Structured Copilot gate verdict for the current HEAD.
            ``None`` when the verdict has not been evaluated (e.g. in unit tests that
            construct a snapshot directly without going through
            ``build_pr_state_snapshot``).  When set, ``approve`` and ``merge`` actions
            use this verdict instead of the legacy ``review_state`` + inline-count check.
        head_changed_since_review: Whether the Copilot review selected by the gate
            verdict targets a commit other than the current HEAD. When that effective
            review cannot be resolved to a commit SHA, this fails closed to ``True``.
            Used with ``repair_satisfied_review_id`` to safely clear an already-
            evaluated suppressed-comments block only while the reviewed code is
            unchanged.
        repair_satisfied_review_id: Review id from the most recent Copilot
            ``repair-satisfied`` marker (``None`` when absent). Populated only when the
            gate is blocked solely by suppressed comments on the current HEAD, so the
            approve/merge gate can recognise that those suppressed comments were already
            evaluated by the repair agent.
        suppressed_deferral_review_id: Review id recorded by the most recent active
            ``suppressed-deferral`` marker (``None`` when absent). Populated from the
            same ``issue_comments`` fetch as ``repair_satisfied_review_id`` — no extra
            API call — so the approve/merge gate can recognise a suppressed-only block
            that ``DeferSuppressedAction`` handed to a follow-up triage issue.
        suppressed_deferral_issue_number: Issue number of the deferral follow-up issue
            recorded in the most recent active ``suppressed-deferral`` marker (``None``
            when absent). Populated from the same ``issue_comments`` fetch as
            ``suppressed_deferral_review_id`` — no extra API call — so the post-merge
            dispatch in ``MergeAction`` can recover the issue number on any run, not
            only the run that filed the deferral.
    """

    pr_number: int = 0
    head_sha: str = ""
    base_branch: str = ""
    head_branch: str = ""
    commit_count: int = 1
    ci_status: str = "unknown"
    ci_failed_checks: list[str] = field(default_factory=list)
    review_state: str = ""
    copilot_review_id: int = 0
    copilot_review_inline_count: int = 0
    effective_review_comment_count: int | None = None
    effective_review_comment_count_review_id: int | None = None
    effective_review_comment_filter_applied: bool | None = None
    active_session: bool = False
    copilot_review_pending: bool = False
    unresolved_threads: int = 0
    unresolved_threads_degraded: bool = False
    repairable_threads: int = 0
    unresolved_threads_unknown_provenance: bool = False
    labels: list[str] = field(default_factory=list)
    is_draft: bool = False
    mergeable: bool | None = None
    mergeable_state: str = ""
    requested_reviewers: list[str] = field(default_factory=list)
    has_approval_on_head: bool = False
    approver_login: str = ""
    has_approver_approval_on_head: bool = False
    title: str = ""
    head_repo_full_name: str = ""
    base_repo_full_name: str = ""
    files: list[str] = field(default_factory=list)
    check_runs: list[CheckRunStatus] = field(default_factory=list)
    reviews: list[ReviewInfo] = field(default_factory=list)
    has_changes: bool = False
    commits_behind: int = 0
    head_author_login: str = ""
    copilot_gate_verdict: CopilotGateVerdict | None = None
    head_changed_since_review: bool = False
    repair_satisfied_review_id: int | None = None
    suppressed_deferral_review_id: int | None = None
    suppressed_deferral_issue_number: int | None = None


class DerivedState:
    """Mutable proxy over PRStateSnapshot that allows pipeline actions to update state.

    Actions can mutate derived state (e.g., marking draft as published) so that
    subsequent actions see the effect without re-querying the provider.
    """

    def __init__(self, snapshot: PRStateSnapshot) -> None:
        self._snapshot = snapshot
        self._overrides: dict[str, Any] = {}

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self._overrides:
            return self._overrides[name]
        return getattr(self._snapshot, name)

    def set(self, name: str, value: Any) -> None:
        """Set a derived state override."""
        self._overrides[name] = value

    def get(self, name: str, default: Any = None) -> Any:
        """Get a derived state value with default fallback."""
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self._overrides:
            return self._overrides[name]
        return getattr(self._snapshot, name, default)

    @property
    def snapshot(self) -> PRStateSnapshot:
        """Access the underlying immutable snapshot."""
        return self._snapshot


_DEFAULT_ACTIONABLE_CHECK_NAMES = DEFAULT_ACTIONABLE_CHECK_NAMES
REPAIRABLE_REVIEW_STATES = frozenset({"CHANGES_REQUESTED", "COMMENTED", "APPROVED"})


def build_pr_state_snapshot(
    provider: CIPlatformProvider,
    pr_number: int,
    *,
    actionable_check_names: frozenset[str] | None = None,
) -> PRStateSnapshot:
    """Build a complete PR state snapshot in one pass.

    Gathers all required data from the provider to make a single
    immutable snapshot that the pipeline evaluates against.
    """
    if actionable_check_names is None:
        actionable_check_names = _DEFAULT_ACTIONABLE_CHECK_NAMES

    # Get PR metadata
    pr_meta = provider.get_pr_metadata(pr_number)

    # Resolve the HEAD commit author login (used to detect Copilot-authored HEADs
    # whose pushes do not trigger pull_request workflows). Fail open: a missing or
    # unknown author simply means "no takeover this run".
    try:
        raw_head_author = provider.get_commit_author_login(pr_meta.head_sha)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        raw_head_author = ""
    head_author_login = raw_head_author if isinstance(raw_head_author, str) else ""

    # List files — fail closed: if this raises, the caller gets EXIT_METADATA_FAILED
    # so that guards (privileged-path / Dockerfile checks) are never bypassed by a
    # missing file list.
    files = provider.list_pr_files(pr_number)

    # Get check runs — fail closed: if this raises, the caller gets EXIT_METADATA_FAILED
    # so that a provider/API outage cannot silently drive ci_status to 'pending' and
    # allow the pipeline to evaluate readiness against stale/missing data.
    check_runs = provider.list_check_runs(pr_meta.head_sha)

    # Evaluate CI status
    ci_status, ci_failed_checks = _evaluate_ci_status(check_runs, actionable_check_names)

    # Get reviews — fail closed: if this raises, the caller gets EXIT_METADATA_FAILED
    # so that review/pending-review state is never evaluated from incomplete metadata.
    reviews = provider.list_reviews(pr_number)

    # Determine effective review states on HEAD (latest review.id per reviewer;
    # all Copilot aliases are collapsed to one reviewer key).
    copilot_review_state = ""
    copilot_review_id = 0
    copilot_review_inline_count = 0
    comments: list[ReviewCommentInfo] | None = None
    has_approval_on_head = False

    current_head_sha = pr_meta.head_sha
    effective_head_reviews = get_effective_head_reviews(reviews, current_head_sha)
    has_approval_on_head = any(review.state == "APPROVED" for review in effective_head_reviews)

    # Resolve the approver-PAT identity (best-effort — fails open to "" so a
    # transient API error does not block the pipeline). When the login is known,
    # compute whether that exact identity has already approved HEAD for a precise
    # idempotency guard in ApproveAction.
    try:
        raw_approver_login = provider.get_approver_login()
        approver_login = raw_approver_login if isinstance(raw_approver_login, str) else ""
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.debug("Failed to resolve approver login for PR %s", pr_number, exc_info=True)
        approver_login = ""
    has_approver_approval_on_head = bool(
        approver_login
        and any(
            review.state == "APPROVED"
            and isinstance(review.user, str)
            and review.user.casefold() == approver_login.casefold()
            and not is_copilot_or_synthetic_review(review)
            and review.commit_sha  # fail closed: unknown target SHA is not treated as current HEAD
            for review in effective_head_reviews
        )
    )

    # Find the latest genuine or trusted synthetic Copilot review that explicitly targets HEAD.
    # Use the raw reviews list rather than effective_head_reviews so that a synthetic-marker
    # review is not lost when the trusted synthetic user also submitted a later plain approval
    # (which would otherwise win the per-user de-duplication in get_effective_head_reviews).
    copilot_review = max(
        (
            review
            for review in reviews
            if is_copilot_or_synthetic_review(review)
            and (not review.commit_sha or review.commit_sha == current_head_sha)
        ),
        key=lambda review: (review.submitted_at if isinstance(review.submitted_at, str) else "", review.id),
        default=None,
    )
    if copilot_review is not None:
        copilot_review_state = copilot_review.state
        copilot_review_id = copilot_review.id
        # Count inline comments for review states whose feedback can trigger repair.
        if copilot_review.state in {"COMMENTED", "CHANGES_REQUESTED", "APPROVED"}:
            try:
                comments = provider.list_review_comments(pr_number, copilot_review.id)
                if copilot_review.state == "COMMENTED":
                    copilot_review_inline_count = len(comments)
            except Exception as exc:
                _raise_if_rate_limit(exc)
                comments = None
                if copilot_review.state == "COMMENTED":
                    copilot_review_inline_count = -1  # unknown

    # Check Copilot review pending
    copilot_review_pending = _is_copilot_review_pending(pr_meta.requested_reviewers)

    # Count commits above merge-base
    commit_count = _count_commits(provider, base_branch=pr_meta.base_branch, head_sha=pr_meta.head_sha)

    # Count commits behind base branch
    commits_behind = _count_commits_behind(
        provider, pr_number=pr_number, base_branch=pr_meta.base_branch, head_branch=pr_meta.head_branch
    )

    # Evaluate Copilot gate verdict — fail closed on any error so the gate
    # cannot be bypassed by a provider/API outage.
    try:
        copilot_gate_verdict = evaluate_copilot_gate_verdict(
            reviews=reviews,
            head_sha=current_head_sha,
            pr_number=pr_number,
            provider=provider,
            base_branch=pr_meta.base_branch,
        )
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.exception("PR #%d: Failed to evaluate gate verdict", pr_number)
        exc_summary = str(exc)[:200]
        copilot_gate_verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_API_ERROR,
            details=f"Gate verdict evaluation raised an unexpected exception: {exc_summary}",
        )

    # Count unresolved threads from reviews the gate verdict does not already own.
    # This must run *after* the verdict is evaluated (not before, as it did
    # previously) because provenance is now scoped to the verdict's effective
    # review_id rather than to HEAD's commit SHA — a HEAD move alone (e.g.
    # squash/takeover minting a new commit) must not change which reviews count
    # as "prior". When the verdict evaluation above failed closed, its review_id
    # defaults to 0, so this degrades explicitly to count-all — the same
    # fail-closed direction the verdict itself takes on exception.
    effective_verdict_review_id = (
        copilot_gate_verdict.review_id
        if copilot_gate_verdict is not None and copilot_gate_verdict.review_id > 0
        else None
    )
    unresolved_threads, repairable_threads, unresolved_threads_degraded, unresolved_threads_unknown_provenance = (
        count_unresolved_prior_threads(
            provider,
            pr_number,
            reviews,
            effective_verdict_review_id,
            verdict=copilot_gate_verdict,
        )
    )

    # Whether the Copilot review actually evaluated by the gate still matches HEAD.
    # This must use the verdict's effective review_id rather than the newest Copilot
    # review: force-push/rewind scenarios can leave a newer Copilot review on a
    # non-HEAD commit while the gate still evaluates an older review on HEAD.
    # Fail closed when the effective review cannot be resolved to a commit SHA.
    head_changed_since_review = _head_changed_since_effective_gate_review(
        reviews=reviews,
        current_head_sha=current_head_sha,
        verdict=copilot_gate_verdict,
    )

    effective_review_comment_count = None
    effective_review_comment_count_review_id: int | None = None
    effective_review_comment_filter_applied: bool | None = None
    if copilot_review is not None:
        effective_review_comment_count_review_id = copilot_review.id
        (
            effective_review_comment_count,
            effective_review_comment_filter_applied,
        ) = _count_effective_review_comments(
            provider,
            pr_number,
            copilot_review,
            comments,
        )

    # Detect the repair-satisfied marker only when it could actually clear the gate:
    # a suppressed-only block on the still-current HEAD. This avoids an extra
    # issue-comments API call on every run. Best-effort / fail-open to None so a
    # transient API error never blocks the pipeline — the marker only *relaxes* the
    # gate (it is never used to make it stricter).
    repair_satisfied_review_id: int | None = None
    suppressed_deferral_review_id: int | None = None
    suppressed_deferral_issue_number: int | None = None
    if (
        copilot_gate_verdict is not None
        and not copilot_gate_verdict.passed
        and not head_changed_since_review
        and is_suppressed_only_block(copilot_gate_verdict)
    ):
        list_issue_comments = getattr(provider, "list_issue_comments", None)
        if callable(list_issue_comments):
            try:
                issue_comments = list_issue_comments(pr_number)
                # Resolve the PR token login so that markers posted by the
                # workflow identity (which may not be a Copilot bot) are trusted.
                pr_token_login: str | None = None
                get_pr_token_login = getattr(provider, "get_pr_token_login", None)
                if callable(get_pr_token_login):
                    try:
                        pr_token_login = get_pr_token_login()
                    except Exception as exc:
                        _raise_if_rate_limit(exc)
                        pass
                extra_authors = frozenset({pr_token_login.casefold()}) if pr_token_login else None
                repair_satisfied_review_id = find_repair_satisfied_review_id(issue_comments)
                suppressed_deferral_review_id, suppressed_deferral_issue_number = find_suppressed_deferral_state(
                    issue_comments, extra_authors
                )
            except Exception as exc:
                _raise_if_rate_limit(exc)
                logger.warning(
                    "PR #%d: Failed to fetch issue comments for repair-satisfied marker: %s",
                    pr_number,
                    str(exc)[:200],
                )

    return PRStateSnapshot(
        pr_number=pr_number,
        head_sha=pr_meta.head_sha,
        base_branch=pr_meta.base_branch,
        head_branch=pr_meta.head_branch,
        commit_count=commit_count,
        ci_status=ci_status,
        ci_failed_checks=ci_failed_checks,
        review_state=copilot_review_state,
        copilot_review_id=copilot_review_id,
        copilot_review_inline_count=copilot_review_inline_count,
        effective_review_comment_count=effective_review_comment_count,
        effective_review_comment_count_review_id=effective_review_comment_count_review_id,
        effective_review_comment_filter_applied=effective_review_comment_filter_applied,
        copilot_review_pending=copilot_review_pending,
        unresolved_threads=unresolved_threads,
        unresolved_threads_degraded=unresolved_threads_degraded,
        repairable_threads=repairable_threads,
        unresolved_threads_unknown_provenance=unresolved_threads_unknown_provenance,
        labels=list(pr_meta.labels),
        is_draft=pr_meta.is_draft,
        mergeable=pr_meta.mergeable,
        mergeable_state=pr_meta.mergeable_state,
        requested_reviewers=list(pr_meta.requested_reviewers),
        has_approval_on_head=has_approval_on_head,
        approver_login=approver_login,
        has_approver_approval_on_head=has_approver_approval_on_head,
        title=pr_meta.title,
        head_repo_full_name=pr_meta.head_repo_full_name,
        base_repo_full_name=pr_meta.base_repo_full_name,
        files=files,
        check_runs=check_runs,
        reviews=reviews,
        has_changes=bool(files),
        commits_behind=commits_behind,
        head_author_login=head_author_login,
        copilot_gate_verdict=copilot_gate_verdict,
        head_changed_since_review=head_changed_since_review,
        repair_satisfied_review_id=repair_satisfied_review_id,
        suppressed_deferral_review_id=suppressed_deferral_review_id,
        suppressed_deferral_issue_number=suppressed_deferral_issue_number,
    )


def _evaluate_ci_status(
    check_runs: list[CheckRunStatus],
    actionable_check_names: frozenset[str],
) -> tuple[str, list[str]]:
    """Evaluate CI status from check runs.

    Returns:
        Tuple of (status_string, list_of_failed_check_names).
    """
    any_failed = False
    any_pending = False
    any_unknown = False
    failed_checks: list[str] = []
    actionable_seen = 0

    for cr in check_runs:
        if cr.name not in actionable_check_names:
            continue
        actionable_seen += 1
        if cr.status != "completed":
            any_pending = True
        elif cr.conclusion == "failure":
            any_failed = True
            failed_checks.append(cr.name)
        elif cr.conclusion not in ("success", "neutral", "skipped"):
            any_unknown = True

    if actionable_seen == 0:
        return "pending", []
    if any_pending:
        return "pending", failed_checks
    if any_failed:
        return "failing", failed_checks
    if any_unknown:
        return "unknown", failed_checks
    return "passing", []


def _is_copilot_review_pending(requested_reviewers: list[str]) -> bool:
    """Return True when Copilot is currently requested as a pending reviewer."""
    return any(is_copilot_login(reviewer) for reviewer in requested_reviewers)


def _count_effective_review_comments(
    provider: CIPlatformProvider,
    pr_number: int,
    review: ReviewInfo,
    comments: list[ReviewCommentInfo] | None,
) -> tuple[int | None, bool | None]:
    """Count current-review comments left after reply and thread filtering.

    Returns:
        Tuple of ``(effective_count, filter_applied)``.
        ``(None, None)`` is returned whenever the provider cannot establish the
        complete inventory, preserving repair dispatch's fail-open behavior.
    """
    if comments is None:
        return None, None

    thread_lookup = getattr(provider, "list_review_threads_by_thread_id", None)
    if not callable(thread_lookup):
        return None, None
    try:
        thread_states = thread_lookup(pr_number)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning("PR #%d: Failed to derive effective review comments: %s", pr_number, str(exc)[:200])
        return None, None
    if not isinstance(thread_states, dict):
        return None, None

    resolved_comment_ids: set[int] = set()
    known_comment_ids: set[int] = set()
    comment_thread_ids: dict[int, str] = {}
    for thread_id, state in thread_states.items():
        if (
            not isinstance(thread_id, str)
            or not thread_id
            or not isinstance(state, tuple)
            or len(state) != 2
            or type(state[0]) is not bool
            or not isinstance(state[1], tuple)
            or any(type(comment_id) is not int for comment_id in state[1])
        ):
            return None, None
        is_resolved = state[0]
        for comment_id in state[1]:
            mapped_thread = comment_thread_ids.get(comment_id)
            if mapped_thread is not None and mapped_thread != thread_id:
                return None, None
            comment_thread_ids[comment_id] = thread_id
            known_comment_ids.add(comment_id)
            if is_resolved and comment_id > 0:
                resolved_comment_ids.add(comment_id)
    root_ids = {
        comment.id
        for comment in comments
        if type(comment.id) is int and comment.id > 0 and comment.in_reply_to_id is None
    }
    reply_ids = {
        comment.id
        for comment in comments
        if (
            type(comment.id) is int
            and comment.id > 0
            and is_cloud_coding_agent_login(comment.author_login)
            and type(comment.in_reply_to_id) is int
            and comment.in_reply_to_id > 0
            and comment.in_reply_to_id in root_ids
        )
    }
    answered_root_ids = {
        comment.in_reply_to_id
        for comment in comments
        if (comment.id in reply_ids and isinstance(comment.body, str) and bool(comment.body.strip()))
    }

    effective_count = 0
    filter_applied = False
    for comment in comments:
        if type(comment.id) is not int:
            return None, None
        if comment.id > 0:
            if comment.id not in known_comment_ids:
                return None, None
            if comment.id in resolved_comment_ids or comment.id in reply_ids or comment.id in answered_root_ids:
                filter_applied = True
                continue
            effective_count += 1
        elif comment.id < 0:
            effective_count += 1
        else:
            return None, None

    # Synthetic suppressed entries are normally recovered by the provider. If
    # they are absent despite a declared count, the inventory is incomplete.
    if parse_suppressed_count(review.body) > 0 and not any(
        type(comment.id) is int and comment.id < 0 for comment in comments
    ):
        return None, None
    return effective_count, filter_applied


def _effective_thread_owner_verdict_id(
    verdict_review_id: int | None,
    verdict: CopilotGateVerdict | None,
) -> int | None:
    """Resolve the effective thread-owner review ID for merge-gate provenance.

    ``None`` represents unknown provenance, which is the fail-closed signal for
    the count-all path. When a verdict object is present it is authoritative:
    a positive ``verdict.review_id`` is used, otherwise provenance remains
    unknown. The legacy integer is used only when no verdict object is supplied.
    """
    if verdict is not None:
        if verdict.review_id > 0:
            return verdict.review_id
        return None
    if verdict_review_id is not None and verdict_review_id > 0:
        return verdict_review_id
    return None


def count_unresolved_prior_threads(
    provider: CIPlatformProvider,
    pr_number: int,
    reviews: list[ReviewInfo],
    verdict_review_id: int | None,
    *,
    verdict: CopilotGateVerdict | None = None,
) -> tuple[int, int, bool, bool]:
    """Count unresolved Copilot or trusted synthetic review threads.

    Returns a ``(blocking_count, repairable_count, degraded, unknown_provenance)`` tuple.
    ``blocking_count`` (unresolved_threads) is the number of distinct review threads
    from genuine Copilot or trusted synthetic reviews — other than the one the gate
    verdict already accounts for (``verdict_review_id``) — whose provider-reported
    state is unresolved.

    ``repairable_count`` (repairable_threads) is the total number of unresolved
    threads from ALL genuine or trusted Copilot reviews (including APPROVED reviews),
    regardless of whether they are owned by the gate verdict. This decoupled count
    allows the repair agent to detect genuinely repairable state even when a gate
    block zeroes out the blocking count.

    Provenance is scoped to ``verdict_review_id``, not to HEAD's commit SHA: this
    keeps the count HEAD-independent, so a HEAD move that touches no review or
    thread (e.g. ``squash``/``takeover`` minting a new commit) cannot change it.
    When ``verdict_review_id <= 0`` (no verdict evaluated, or evaluation failed
    closed), this explicitly degenerates to counting every actionable review for
    the blocking count — the same fail-closed direction the verdict itself takes.

    When the provider cannot report review-thread state (the capability is
    missing, the lookup failed, the returned mapping omits selected comments, or
    a review's comments could not be listed), ``degraded`` is True. Degradation is
    tracked separately for blocking and repairable inventories:
    ``blocking_count`` is floored to ``1`` only when blocking inventory is unknown,
    while ``repairable_count`` is floored to ``1`` when repairable inventory is
    unknown and no unresolved repairable threads were measured. This prevents
    false-open merge gates and also prevents repair dispatch from stalling behind
    an unknown-but-possible repairable inventory.
    Every degradation is logged, so no thread is ever dropped from the count
    without a diagnostic.
    """
    effective_review_id = _effective_thread_owner_verdict_id(verdict_review_id, verdict)
    unknown_provenance = effective_review_id is None
    if unknown_provenance:
        logger.warning(
            "PR #%d: no concrete thread-owner provenance for prior actionable reviews; "
            "falling back to count-all (conservative floor — not a query failure)",
            pr_number,
        )

    # All genuine/trusted Copilot reviews are candidates for repairable-thread counting,
    # regardless of their verdict state (APPROVED reviews can still have unresolved threads).
    all_copilot_reviews = [
        r for r in reviews if is_copilot_or_synthetic_review(r) and r.state in REPAIRABLE_REVIEW_STATES
    ]
    if not all_copilot_reviews:
        # Nothing to report on — no capability was needed, so this is not degraded.
        return 0, 0, False, unknown_provenance

    # Blocking classification still uses the filtered (CHANGES_REQUESTED/COMMENTED) set.
    blocking_review_ids = {r.id for r in select_prior_actionable_reviews(reviews, effective_review_id)}

    def _unknown_inventory_fallback(unknown_provenance: bool) -> tuple[int, int, bool, bool]:
        blocking_floor = 1 if blocking_review_ids else 0
        # We have at least one repairable review candidate, but inventory is
        # unknown; fail closed so repair paths do not stall.
        return blocking_floor, 1, True, unknown_provenance

    thread_lookup = getattr(provider, "list_review_threads_by_thread_id", None)
    if not callable(thread_lookup):
        logger.warning(
            "PR #%d: review-thread state unavailable (provider does not expose list_review_threads_by_thread_id())"
            " — failing closed with an unknown-thread count",
            pr_number,
        )
        return _unknown_inventory_fallback(unknown_provenance)

    try:
        thread_states = thread_lookup(pr_number)
    except NotImplementedError:
        logger.warning(
            "PR #%d: review-thread state unavailable (provider does not implement list_review_threads_by_thread_id())"
            " — failing closed with an unknown-thread count",
            pr_number,
        )
        return _unknown_inventory_fallback(unknown_provenance)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning(
            "PR #%d: review-thread state unavailable (%s) — failing closed with an unknown-thread count",
            pr_number,
            str(exc)[:200],
        )
        return _unknown_inventory_fallback(unknown_provenance)

    if not isinstance(thread_states, dict):
        logger.warning(
            "PR #%d: review-thread state unavailable "
            "(list_review_threads_by_thread_id() returned %s, expected a mapping)"
            " — failing closed with an unknown-thread count",
            pr_number,
            type(thread_states).__name__,
        )
        return _unknown_inventory_fallback(unknown_provenance)

    comment_to_thread: dict[int, str] = {}
    for thread_key, state in thread_states.items():
        if not isinstance(thread_key, str) or not thread_key:
            logger.warning(
                "PR #%d: review-thread state unavailable "
                "(list_review_threads_by_thread_id() returned an invalid thread key: "
                "thread_key=%r)"
                " — failing closed with an unknown-thread count",
                pr_number,
                thread_key,
            )
            return _unknown_inventory_fallback(unknown_provenance)
        if not isinstance(state, tuple) or len(state) != 2 or type(state[0]) is not bool:
            logger.warning(
                "PR #%d: review-thread state unavailable "
                "(list_review_threads_by_thread_id() returned an invalid state mapping: "
                "thread=%r state=%r)"
                " — failing closed with an unknown-thread count",
                pr_number,
                thread_key,
                state,
            )
            return _unknown_inventory_fallback(unknown_provenance)
        comment_ids = state[1]
        if not isinstance(comment_ids, tuple):
            logger.warning(
                "PR #%d: review-thread state unavailable "
                "(list_review_threads_by_thread_id() returned an invalid state mapping)"
                " — failing closed with an unknown-thread count",
                pr_number,
            )
            return _unknown_inventory_fallback(unknown_provenance)
        for comment_id in comment_ids:
            if type(comment_id) is not int:
                logger.warning(
                    "PR #%d: review-thread state unavailable "
                    "(list_review_threads_by_thread_id() returned an invalid state mapping: "
                    "thread=%r comment_id=%r)"
                    " — failing closed with an unknown-thread count",
                    pr_number,
                    thread_key,
                    comment_id,
                )
                return _unknown_inventory_fallback(unknown_provenance)
            mapped_thread = comment_to_thread.get(comment_id)
            if mapped_thread is not None and mapped_thread != thread_key:
                logger.warning(
                    "PR #%d: review-thread state unavailable "
                    "(list_review_threads_by_thread_id() returned conflicting thread mappings: "
                    "comment_id=%r thread=%r conflicting_thread=%r)"
                    " — failing closed with an unknown-thread count",
                    pr_number,
                    comment_id,
                    mapped_thread,
                    thread_key,
                )
                return _unknown_inventory_fallback(unknown_provenance)
            comment_to_thread[comment_id] = thread_key

    total_blocking = 0
    total_repairable = 0
    blocking_inventory_unknown = False
    repairable_inventory_unknown = False
    counted_blocking_thread_ids: set[str] = set()
    counted_repairable_thread_ids: set[str] = set()

    for review in all_copilot_reviews:
        is_blocking = review.id in blocking_review_ids
        try:
            comments = provider.list_review_comments(pr_number, review.id)
            for comment in comments:
                if comment.id < 0:
                    continue  # Skip synthetic review-body entries
                if comment.id in comment_to_thread:
                    thread_id = comment_to_thread[comment.id]
                    is_resolved = thread_states[thread_id][0]

                    if not is_resolved:
                        if thread_id not in counted_repairable_thread_ids:
                            counted_repairable_thread_ids.add(thread_id)
                            total_repairable += 1
                        if is_blocking and thread_id not in counted_blocking_thread_ids:
                            counted_blocking_thread_ids.add(thread_id)
                            total_blocking += 1
                    continue

                logger.warning(
                    "PR #%d: review-thread state omitted comment %d — failing closed",
                    pr_number,
                    comment.id,
                )
                repairable_inventory_unknown = True
                if is_blocking:
                    blocking_inventory_unknown = True
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning(
                "PR #%d: failed to list review comments for review %d (%s) — failing closed",
                pr_number,
                review.id,
                str(exc)[:200],
            )
            repairable_inventory_unknown = True
            if is_blocking:
                blocking_inventory_unknown = True

    if repairable_inventory_unknown or blocking_inventory_unknown:
        if repairable_inventory_unknown and total_repairable == 0:
            logger.warning(
                "PR #%d: no unresolved repairable threads were measured and at least one review inventory "
                "is unknown — applying the repairable floor of 1 unresolved thread",
                pr_number,
            )
            total_repairable = 1
        if blocking_inventory_unknown:
            total_blocking = max(1, total_blocking)
        return total_blocking, total_repairable, True, unknown_provenance
    return total_blocking, total_repairable, False, unknown_provenance


def _count_commits(provider: CIPlatformProvider, *, base_branch: str, head_sha: str) -> int:
    """Return commit count above merge-base, or 1 when the provider lacks support.

    Raises:
        Exception: Propagated from the provider when commit counting is supported
            but fails. The caller should treat this as a metadata failure so the
            pipeline does not proceed with an unknown commit count.
    """
    counter = getattr(provider, "count_commits_above_merge_base", None)
    if not callable(counter):
        return 1
    count = counter(base_branch=base_branch, head_sha=head_sha)
    return int(count)


def _count_commits_behind(provider: CIPlatformProvider, *, pr_number: int, base_branch: str, head_branch: str) -> int:
    """Return how many commits head is behind base, or 0 when unsupported.

    Raises:
        Exception: Propagated from the provider when behind-counting is supported
            but fails. The caller should treat this as a metadata failure so the
            pipeline does not proceed with an unknown behind count.
    """
    counter = getattr(provider, "count_commits_behind", None)
    if not callable(counter):
        return 0
    return int(counter(pr_number=pr_number, base_branch=base_branch, head_branch=head_branch))


def get_effective_head_reviews(reviews: list[ReviewInfo], current_head_sha: str) -> list[ReviewInfo]:
    """Return latest effective reviews on HEAD (latest review.id per reviewer).

    All Copilot aliases are normalized to a single reviewer key so a newer
    Copilot review supersedes older Copilot reviews across aliases.
    """
    latest_by_user: dict[str, ReviewInfo] = {}
    for review in reviews:
        if review.commit_sha and review.commit_sha != current_head_sha:
            continue
        user_key = (
            "copilot"
            if is_copilot_login(review.user)
            else (review.user.casefold() if isinstance(review.user, str) else str(review.user))
        )
        existing = latest_by_user.get(user_key)
        if existing is None or review.id > existing.id:
            latest_by_user[user_key] = review
    return list(latest_by_user.values())


def _head_changed_since_effective_gate_review(
    *,
    reviews: list[ReviewInfo],
    current_head_sha: str,
    verdict: CopilotGateVerdict,
) -> bool:
    """Return whether the gate's effective Copilot review targets non-HEAD code.

    If the gate verdict identifies a specific review, that review is authoritative.
    When the review cannot be found or does not carry a commit SHA, fail closed so
    suppressed-comment bypass logic cannot clear a gate without proving the reviewed
    code still matches HEAD.
    """
    if verdict.review_id > 0:
        effective_review = next(
            (review for review in reviews if review.id == verdict.review_id and is_copilot_or_synthetic_review(review)),
            None,
        )
        if effective_review is None or not effective_review.commit_sha or not current_head_sha:
            return True
        return effective_review.commit_sha != current_head_sha

    latest_copilot_review = max(
        (review for review in reviews if is_copilot_login(review.user)),
        key=lambda review: review.id,
        default=None,
    )
    if latest_copilot_review is None or not latest_copilot_review.commit_sha or not current_head_sha:
        return True
    return latest_copilot_review.commit_sha != current_head_sha


def has_non_copilot_changes_requested_on_head(reviews: list[ReviewInfo], current_head_sha: str) -> bool:
    """Return True when any non-Copilot effective HEAD review requests changes."""
    return any(
        not is_copilot_or_synthetic_review(review) and review.state == "CHANGES_REQUESTED"
        for review in get_effective_head_reviews(reviews, current_head_sha)
    )
