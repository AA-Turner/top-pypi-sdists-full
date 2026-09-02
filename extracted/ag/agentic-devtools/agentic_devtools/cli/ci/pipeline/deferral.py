"""Deferral signals — PR-comment markers that delay repair dispatch.

Two marker types share this subsystem (same sentinel/JSON/author-allowlist
mechanics, distinguished only by their sentinel prefix):

* **autofix deferral** — posted by ``ApplySuggestionsAction`` when discovery is
  inconclusive, consumed (deactivated) by ``DispatchRepairAction``;
* **suppressed-comment deferral** — posted by ``DeferSuppressedAction`` when a
  specs-only suppressed-only review round is handed to a follow-up issue.  It is
  read, never consumed: it must stay active so the approve/merge bypass still
  recognises the deferral on a later pipeline run.

Autofix deferral signal — delays repair dispatch when discovery is inconclusive.

When all discovery strategy attempts return EMPTY and ``has_inline_evidence``
indicates that inline suggestions should exist (CHANGES_REQUESTED reviews always
qualify; COMMENTED reviews qualify when the inline count is non-zero or unknown),
a deferral marker is posted as a PR comment.  The DispatchRepairAction checks for
active markers and skips dispatch to give the autofix path another chance on the
next pipeline iteration.

Marker format:
    <!-- ai-pr-loop:autofix-deferral {"review_id":"12345",
    "deferred_until":"2026-06-14T00:36:52Z","active":true} -->

Lifecycle:
    1. ApplySuggestionsAction posts marker when inconclusive
    2. DispatchRepairAction reads marker
    3. DispatchRepairAction skips only if it can deactivate (consume) the marker
    4. If marker deactivation fails, DispatchRepairAction proceeds with repair
       dispatch to avoid a permanent skip loop behind an active marker
"""

from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.models import COPILOT_COMMENT_LOGINS, IssueCommentInfo
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)

# Sentinel prefix for autofix deferral markers in PR comments
_DEFERRAL_SENTINEL = "<!-- ai-pr-loop:autofix-deferral "

# Sentinel prefix for suppressed-comment deferral markers in PR comments.  It is
# deliberately distinct from the issue-side ``ai-pr-loop:suppressed-comment-deferral``
# marker written into the deferral issue body, and neither string is a substring
# of the other, so the two can never be confused.
SUPPRESSED_DEFERRAL_SENTINEL = "<!-- ai-pr-loop:suppressed-deferral "

# Default deferral TTL: marker expires after this many seconds
_DEFERRAL_TTL_SECONDS = 300  # 5 minutes
_DEFERRAL_ALLOWED_AUTHORS = {
    *(login.casefold() for login in COPILOT_COMMENT_LOGINS),
    "github-actions[bot]".casefold(),
}


def _format_utc_iso8601_z(timestamp: datetime) -> str:
    """Format datetime as UTC ISO-8601 string with ``Z`` suffix."""
    return timestamp.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _parse_utc_timestamp(timestamp_value: str) -> datetime:
    """Parse ISO-8601 timestamp to timezone-aware UTC datetime.

    Naive timestamps (without timezone information) are interpreted as UTC.
    """
    normalized = timestamp_value.strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def post_deferral_marker(
    provider: CIPlatformProvider,
    pr_number: int,
    review_id: int,
) -> bool:
    """Post a deferral marker comment on the PR.

    Enforces single-deferral cap: if any marker already exists for the same
    review (active or already consumed), skips posting.

    Args:
        provider: CI platform provider.
        pr_number: Pull request number.
        review_id: ID of the Copilot review triggering deferral.

    Returns:
        True if a marker was posted, False if skipped (existing marker).
    """
    existing = _find_matching_deferral_comment(provider, pr_number, review_id)
    if existing is not None:
        logger.info(
            "PR #%d: Deferral marker already exists for review %d — skipping",
            pr_number,
            review_id,
        )
        return False

    deferred_until = datetime.now(UTC) + timedelta(seconds=_DEFERRAL_TTL_SECONDS)
    payload = {
        "review_id": str(review_id),
        "deferred_until": _format_utc_iso8601_z(deferred_until),
        "active": True,
        "posted_at": _format_utc_iso8601_z(datetime.now(UTC)),
    }

    body = f"{_DEFERRAL_SENTINEL}{json.dumps(payload)} -->"

    try:
        provider.post_comment(pr_number, body)
        logger.info(
            "PR #%d: Posted autofix deferral marker (review_id=%d, expires=%s)",
            pr_number,
            review_id,
            _format_utc_iso8601_z(deferred_until),
        )
        return True
    except ProviderRateLimitError:
        raise
    except Exception as exc:
        logger.warning(
            "PR #%d: Failed to post deferral marker: %s",
            pr_number,
            exc,
        )
        return False


def read_active_deferral(
    provider: CIPlatformProvider,
    pr_number: int,
    review_id: int,
) -> dict | None:
    """Read an active, unexpired deferral marker for the given review.

    Args:
        provider: CI platform provider.
        pr_number: Pull request number.
        review_id: ID of the review to check deferral for.

    Returns:
        Deferral payload dict if active and unexpired, None otherwise.
    """
    match = _find_matching_deferral_comment(provider, pr_number, review_id, active_only=True)
    if match is None:
        return None

    _comment_id, payload = match

    # Check expiry
    deferred_until_str = payload.get("deferred_until", "")
    if deferred_until_str:
        try:
            deferred_until = _parse_utc_timestamp(deferred_until_str)
            if datetime.now(UTC) > deferred_until:
                logger.info(
                    "PR #%d: Deferral marker expired at %s",
                    pr_number,
                    deferred_until_str,
                )
                return None
        except (ValueError, TypeError):
            pass

    return payload


def deactivate_deferral_marker(
    provider: CIPlatformProvider,
    pr_number: int,
    review_id: int,
) -> bool:
    """Deactivate (consume) a deferral marker.

    Updates the marker comment to set ``active: false`` and record
    the consuming run ID.

    Args:
        provider: CI platform provider.
        pr_number: Pull request number.
        review_id: ID of the review whose deferral is being consumed.

    Returns:
        True if marker was deactivated, False if not found or error.
    """
    match = _find_matching_deferral_comment(provider, pr_number, review_id, active_only=True)
    if match is None:
        return False

    comment_id, payload = match

    # Update payload to inactive
    payload["active"] = False
    payload["cleared_at"] = _format_utc_iso8601_z(datetime.now(UTC))
    payload["consumed_by_run_id"] = os.environ.get("GITHUB_RUN_ID", "unknown")

    new_body = f"{_DEFERRAL_SENTINEL}{json.dumps(payload)} -->"

    try:
        provider.update_comment(comment_id, new_body)
        logger.info(
            "PR #%d: Deactivated deferral marker for review %d",
            pr_number,
            review_id,
        )
        return True
    except ProviderRateLimitError:
        raise
    except Exception as exc:
        logger.warning(
            "PR #%d: Failed to deactivate deferral marker: %s",
            pr_number,
            exc,
        )
        return False


def post_suppressed_deferral_marker(
    provider: CIPlatformProvider,
    pr_number: int,
    review_id: int,
    issue_number: int,
) -> bool:
    """Post a suppressed-comment deferral marker on the PR.

    The marker records that the suppressed comments of *review_id* were handed to
    deferral issue *issue_number*.  Unlike the autofix marker it carries **no**
    expiry: it is the durable evidence the approve/merge bypass reads on this and
    every subsequent pipeline run.

    Enforces the single-deferral cap: when a marker already exists for the same
    review, nothing is posted.

    Args:
        provider: CI platform provider.
        pr_number: Pull request number.
        review_id: ID of the Copilot review whose suppressed comments were deferred.
        issue_number: Number of the deferral follow-up issue.

    Returns:
        True if a marker was posted, False if skipped or the post failed.
    """
    existing = _find_matching_deferral_comment(provider, pr_number, review_id, sentinel=SUPPRESSED_DEFERRAL_SENTINEL)
    if existing is not None:
        logger.info(
            "PR #%d: Suppressed deferral marker already exists for review %d — skipping",
            pr_number,
            review_id,
        )
        return False

    payload = {
        "review_id": str(review_id),
        "issue": issue_number,
        "active": True,
        "posted_at": _format_utc_iso8601_z(datetime.now(UTC)),
    }
    body = f"{SUPPRESSED_DEFERRAL_SENTINEL}{json.dumps(payload)} -->"

    try:
        provider.post_comment(pr_number, body)
        logger.info(
            "PR #%d: Posted suppressed deferral marker (review_id=%d, issue=#%d)",
            pr_number,
            review_id,
            issue_number,
        )
        return True
    except ProviderRateLimitError:
        raise
    except Exception as exc:
        logger.warning("PR #%d: Failed to post suppressed deferral marker: %s", pr_number, exc)
        return False


def read_active_suppressed_deferral(
    provider: CIPlatformProvider,
    pr_number: int,
    review_id: int,
) -> dict | None:
    """Read the active suppressed-comment deferral marker for *review_id*.

    Args:
        provider: CI platform provider.
        pr_number: Pull request number.
        review_id: ID of the review to check deferral for.

    Returns:
        The deferral payload when an active marker exists, ``None`` otherwise.
    """
    match = _find_matching_deferral_comment(
        provider,
        pr_number,
        review_id,
        active_only=True,
        sentinel=SUPPRESSED_DEFERRAL_SENTINEL,
    )
    if match is None:
        return None
    _comment_id, payload = match
    # Reject markers that lack a positive issue number: approve/merge require
    # one, so returning a payload without it would stall the PR with no triage
    # target even though DispatchRepairAction skipped repair.
    issue = payload.get("issue")
    if isinstance(issue, bool) or not isinstance(issue, int) or issue <= 0:
        return None
    return payload


def find_suppressed_deferral_review_id(
    issue_comments: list[IssueCommentInfo],
    extra_allowed_authors: frozenset[str] | None = None,
) -> int | None:
    """Return the review id of the newest active suppressed-comment deferral marker.

    Pure counterpart of :func:`read_active_suppressed_deferral` for callers that
    already hold the PR's issue comments (the snapshot builder), so recording the
    deferral costs no additional API call.

    Args:
        issue_comments: PR issue comments in API order (oldest first).
        extra_allowed_authors: Additional lower-cased login names to trust as
            marker authors beyond the static ``_DEFERRAL_ALLOWED_AUTHORS`` set.
            Pass the PR token login here so markers posted by the workflow
            identity (e.g. ``AMARSNIK_swica``) are recognised.

    Returns:
        The deferred review id, or ``None`` when no active marker is present.
    """
    allowed = _DEFERRAL_ALLOWED_AUTHORS | (extra_allowed_authors or frozenset())
    for comment in reversed(issue_comments):
        if comment.author.casefold() not in allowed:
            continue
        payload = _parse_deferral_payload(comment.body, SUPPRESSED_DEFERRAL_SENTINEL)
        if payload is None or not payload.get("active", False):
            continue
        try:
            return int(payload.get("review_id", 0))
        except (TypeError, ValueError):
            continue
    return None


def find_suppressed_deferral_issue_number(
    issue_comments: list[IssueCommentInfo],
    extra_allowed_authors: frozenset[str] | None = None,
) -> int | None:
    """Return the deferral issue number from the newest active suppressed-comment deferral marker.

    Pure counterpart of :func:`read_active_suppressed_deferral` for callers that
    already hold the PR's issue comments (the snapshot builder), so recovering the
    issue number costs no additional API call.  The issue number is persisted in the
    durable marker payload as ``"issue"``; reading it here makes it available on
    every subsequent pipeline run, not only the run that filed the deferral.

    Args:
        issue_comments: PR issue comments in API order (oldest first).
        extra_allowed_authors: Additional lower-cased login names to trust as
            marker authors beyond the static ``_DEFERRAL_ALLOWED_AUTHORS`` set.
            Pass the PR token login here so markers posted by the workflow
            identity (e.g. ``AMARSNIK_swica``) are recognised.

    Returns:
        The deferral issue number, or ``None`` when no active marker is present or
        the marker payload carries no valid ``"issue"`` key.
    """
    allowed = _DEFERRAL_ALLOWED_AUTHORS | (extra_allowed_authors or frozenset())
    for comment in reversed(issue_comments):
        if comment.author.casefold() not in allowed:
            continue
        payload = _parse_deferral_payload(comment.body, SUPPRESSED_DEFERRAL_SENTINEL)
        if payload is None or not payload.get("active", False):
            continue
        try:
            return int(payload.get("issue", 0)) or None
        except (TypeError, ValueError):
            continue
    return None


def find_suppressed_deferral_state(
    issue_comments: list[IssueCommentInfo],
    extra_allowed_authors: frozenset[str] | None = None,
) -> tuple[int | None, int | None]:
    """Return (review_id, issue_number) from the newest active suppressed-comment deferral marker.

    Both values are read from the same comment, preventing the two-scan aliasing
    where :func:`find_suppressed_deferral_review_id` and
    :func:`find_suppressed_deferral_issue_number` could each pick a different marker
    (e.g. when the newest marker has a valid ``review_id`` but a missing ``issue``,
    causing the issue scan to fall back to an older marker).

    Args:
        issue_comments: PR issue comments in API order (oldest first).
        extra_allowed_authors: Additional lower-cased login names to trust as
            marker authors beyond the static ``_DEFERRAL_ALLOWED_AUTHORS`` set.

    Returns:
        ``(review_id, issue_number)`` from the same marker, both positive
        integers.  Returns ``(None, None)`` when no active marker is found or
        when the newest active marker does not carry both a valid ``review_id``
        and a valid ``issue`` (a partial marker is skipped so that the caller
        cannot clear the gate without evidence of a filed issue).
    """
    allowed = _DEFERRAL_ALLOWED_AUTHORS | (extra_allowed_authors or frozenset())
    for comment in reversed(issue_comments):
        if comment.author.casefold() not in allowed:
            continue
        payload = _parse_deferral_payload(comment.body, SUPPRESSED_DEFERRAL_SENTINEL)
        if payload is None or not payload.get("active", False):
            continue
        try:
            raw_review_id = payload.get("review_id", 0)
            raw_issue = payload.get("issue", 0)
            if isinstance(raw_review_id, bool) or isinstance(raw_issue, bool):
                continue
            review_id = int(raw_review_id)
            issue_number = int(raw_issue)
        except (TypeError, ValueError):
            continue
        if review_id <= 0 or issue_number <= 0:
            continue
        return review_id, issue_number
    return None, None


def _parse_deferral_payload(body: str, sentinel: str = _DEFERRAL_SENTINEL) -> dict | None:
    """Extract deferral JSON payload from a marker comment body."""
    if sentinel not in body:
        return None

    start_idx = body.index(sentinel) + len(sentinel)
    end_idx = body.find(" -->", start_idx)
    if end_idx == -1:
        return None

    json_str = body[start_idx:end_idx].strip()
    try:
        payload = json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def _find_matching_deferral_comment(
    provider: CIPlatformProvider,
    pr_number: int,
    review_id: int,
    *,
    active_only: bool = False,
    sentinel: str = _DEFERRAL_SENTINEL,
) -> tuple[int, dict] | None:
    """Find the newest deferral marker comment for a review.

    Searches PR issue comments in reverse API order so the newest matching
    marker wins when multiple markers exist. This avoids stale older markers
    masking the current review's state.

    The effective allowed-author set is ``_DEFERRAL_ALLOWED_AUTHORS`` extended
    with the PR token login resolved from the provider.  This ensures that
    markers posted by the workflow identity (e.g. the ``SPECKIT_PR_TOKEN``
    account that authors the PR comment) are recognised on subsequent reads even
    when that identity is not a Copilot bot or ``github-actions[bot]``.
    """
    try:
        comments = provider.list_issue_comments(pr_number)
    except ProviderRateLimitError:
        raise
    except Exception as exc:
        logger.warning("PR #%d: Failed to search for deferral marker: %s", pr_number, exc)
        return None

    allowed = _DEFERRAL_ALLOWED_AUTHORS
    try:
        pr_token_login = provider.get_pr_token_login()
        if pr_token_login:
            allowed = allowed | {pr_token_login.casefold()}
    except ProviderRateLimitError:
        raise
    except Exception:
        pass  # fail open: use the static set only

    for comment in reversed(comments):
        if comment.author.casefold() not in allowed:
            continue
        payload = _parse_deferral_payload(comment.body, sentinel)
        if payload is None:
            continue
        if str(payload.get("review_id", "")) != str(review_id):
            continue
        if active_only and not payload.get("active", False):
            continue
        return comment.id, payload

    return None
