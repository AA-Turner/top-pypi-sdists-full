"""Snapshot builder for the post-agent evaluator.

Gathers all PR state needed to create an immutable PostAgentSnapshot."""

from __future__ import annotations

import logging

from ..guards import find_repair_satisfied_review_id
from ..pipeline.gate_verdict import is_copilot_or_synthetic_review
from ..provider import CIPlatformProvider
from . import snapshot_comments, snapshot_control_markers
from .critique_snapshot import build_critique_post_agent_fields as build_fields
from .lock import check_lock_status
from .models import PostAgentSnapshot, ThreadInfo

logger = logging.getLogger(__name__)


def _get_issue_comments(provider: CIPlatformProvider, pr_number: int) -> list:
    """Fetch issue comments when supported, defaulting to an empty list on failure."""
    list_issue_comments = getattr(provider, "list_issue_comments", None)
    if not callable(list_issue_comments):
        return []
    try:
        return list_issue_comments(pr_number)
    except Exception as exc:
        logger.warning("Failed to fetch issue comments for PR #%d: %s", pr_number, exc)
        return []


def _get_pr_diff(
    provider: CIPlatformProvider,
    pr_number: int,
    review_commit_sha: str,
    current_head_sha: str,
    head_changed: bool,
) -> str:
    """Fetch the post-review range diff when available, otherwise the PR diff."""
    try:
        if review_commit_sha and head_changed:
            return provider.get_commit_range_diff(review_commit_sha, current_head_sha)
        return provider.get_pr_diff(pr_number)
    except NotImplementedError, Exception:
        logger.debug("PR diff unavailable for PR #%d", pr_number)
        return ""


def build_snapshot(
    provider: CIPlatformProvider,
    pr_number: int,
    repo: str,
    *,
    current_lock_token: str | None = None,
    persist_sanitized_comment: bool = False,
) -> PostAgentSnapshot:
    """Build an immutable snapshot of the PR state for classification.

    Gathers all data needed by ``classify_post_agent_state()`` using
    provider methods. This function performs I/O (via the provider) but
    produces an immutable result suitable for pure classification.

    Args:
        provider: CI platform provider.
        pr_number: Pull request number.
        repo: Full repository name (owner/repo).
        current_lock_token: Lock token held by the current evaluator run, if any.
        persist_sanitized_comment: When True, best-effort patch a sanitized
            Copilot issue comment back to the provider.

    Returns:
        Frozen PostAgentSnapshot with all relevant PR state.
    """
    # 1. Get PR metadata for HEAD SHA
    pr_meta = provider.get_pr_metadata(pr_number)
    current_head_sha = pr_meta.head_sha

    # 2. Get reviews to find the latest Copilot review
    reviews = provider.list_reviews(pr_number)
    copilot_reviews = [review for review in reviews if is_copilot_or_synthetic_review(review)]
    review_candidates = [
        review for review in copilot_reviews if review.commit_sha == current_head_sha
    ] or copilot_reviews
    latest_review = max(review_candidates, key=lambda review: (review.submitted_at, review.id), default=None)
    review_id, review_commit_sha = (
        (latest_review.id, latest_review.commit_sha) if latest_review is not None else (0, "")
    )

    # 3. Determine if HEAD changed since the review
    head_changed = bool(review_commit_sha and current_head_sha and review_commit_sha != current_head_sha)

    def _load_review_threads(target_review_id: int) -> list[ThreadInfo]:
        loaded_threads: list[ThreadInfo] = []
        try:
            thread_statuses: dict[int, tuple[bool, bool]] = {}
            try:
                thread_statuses = snapshot_comments._get_review_thread_statuses(provider, pr_number)
            except Exception:
                logger.warning("Failed to fetch review thread statuses for PR #%d", pr_number)

            review_comments = provider.list_review_comments(pr_number, target_review_id)
            for rc in review_comments:
                # Skip synthetic review-body entries — they have no real GitHub
                # thread and must not be used for thread-resolution lookup.
                if rc.id < 0:
                    continue
                is_resolved, has_reply = thread_statuses.get(rc.id, (False, False))
                loaded_threads.append(
                    ThreadInfo(
                        comment_id=rc.id,
                        path=rc.path,
                        start_line=rc.start_line,
                        end_line=rc.end_line,
                        is_resolved=is_resolved,
                        has_reply=has_reply,
                        body=rc.body,
                    )
                )
        except Exception as exc:
            logger.warning("Failed to fetch review comments for review %d: %s", target_review_id, exc)
        return loaded_threads

    # 4. Get review threads (comments from the review)
    threads: list[ThreadInfo] = []
    if review_id:
        threads = _load_review_threads(review_id)

    # 5. Find latest Copilot agent comment (issue comment, not review comment)
    issue_comments = _get_issue_comments(provider, pr_number)

    latest_agent_comment = snapshot_comments._get_latest_agent_comment(
        provider,
        pr_number,
        comments=issue_comments,
        persist_sanitized_body=persist_sanitized_comment,
    )
    latest_agent_issue_comment = snapshot_comments._get_latest_copilot_issue_comment(issue_comments)

    head_sha_short = current_head_sha[:8] if current_head_sha else ""

    # Sentinel is present if:
    # (a) the latest Copilot comment contains the marker and is scoped to the current
    #     HEAD (avoids treating stale prior-cycle sentinels as current completion), or
    # (b) any issue comment contains an evaluator-synthesized sentinel scoped to the
    #     current HEAD (posted via provider.post_comment() by the workflow token, not
    #     a Copilot login, so not captured by _get_latest_agent_comment()).
    has_sentinel = bool(
        (
            latest_agent_issue_comment is not None
            and snapshot_control_markers._SENTINEL_MARKER in latest_agent_issue_comment.body
            and bool(head_sha_short)
            and head_sha_short in latest_agent_issue_comment.body
        )
        or snapshot_comments._has_evaluator_sentinel_comment(
            provider, pr_number, current_head_sha, comments=issue_comments
        )
    )

    # 6. Check lock status
    lock_status = check_lock_status(provider, pr_number)

    # 7. Get PR diff (prefer post-review range diff when available)
    diff_text = _get_pr_diff(provider, pr_number, review_commit_sha, current_head_sha, head_changed)

    lock_holder = lock_status.holder if lock_status.is_locked and not lock_status.is_stale else ""
    if current_lock_token and lock_holder == current_lock_token:
        lock_holder = ""

    # 8. Detect repair-satisfied marker in Copilot-authored issue comments
    repair_satisfied_review_id = find_repair_satisfied_review_id(issue_comments)
    has_repair_satisfied_marker = repair_satisfied_review_id is not None

    # If active Copilot review cannot be derived from list_reviews(), fall back to the
    # review-id encoded in the repair-satisfied marker so thread state can still be loaded.
    if not review_id and repair_satisfied_review_id:
        review_id = repair_satisfied_review_id
        threads = _load_review_threads(review_id)

    return PostAgentSnapshot(
        pr_number=pr_number,
        repo=repo,
        has_sentinel=has_sentinel,
        head_changed_since_review=head_changed,
        threads=tuple(threads),
        latest_agent_comment=latest_agent_comment,
        review_id=review_id,
        review_commit_sha=review_commit_sha,
        current_head_sha=current_head_sha,
        lock_holder=lock_holder,
        lock_age_seconds=lock_status.age_seconds,
        diff_text=diff_text,
        has_repair_satisfied_marker=has_repair_satisfied_marker,
        repair_satisfied_review_id=repair_satisfied_review_id,
        **build_fields(provider, pr_meta, copilot_reviews, issue_comments, review_id, current_head_sha, head_changed),
    )
