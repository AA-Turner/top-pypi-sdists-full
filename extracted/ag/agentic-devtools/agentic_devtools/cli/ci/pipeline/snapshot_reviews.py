"""Review selection and HEAD-provenance helpers for PR snapshots."""

from __future__ import annotations

from agentic_devtools.cli.ci.models import ReviewInfo, is_copilot_login
from agentic_devtools.cli.ci.pipeline.gate_verdict import CopilotGateVerdict, is_copilot_or_synthetic_review


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
