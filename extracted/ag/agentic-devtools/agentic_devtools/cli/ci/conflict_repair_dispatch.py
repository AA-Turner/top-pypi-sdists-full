"""Conflict-repair dispatch deduplication and per-HEAD attempt accounting."""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from agentic_devtools.cli.ci.conflict_repair_markers import (
    _CONFLICT_REPAIR_MARKER_RE,
    CONFLICT_REPAIR_MARKER_PREFIX,
)
from agentic_devtools.cli.ci.guards import DISPATCH_IDEMPOTENCY_TTL_MINUTES, _parse_iso8601_timestamp_guard
from agentic_devtools.cli.ci.models import COPILOT_COMMENT_LOGINS
from agentic_devtools.cli.ci.provider import CIPlatformProvider

# Keep the historical logger name so existing log filters still match.
logger = logging.getLogger("agentic_devtools.cli.ci.guards")
MAX_CONFLICT_REPAIR_ATTEMPTS = 3


def should_dispatch_conflict_repair(
    provider: CIPlatformProvider,
    pr_number: int,
    head_sha: str,
    base_sha: str,
    *,
    dispatch_login: str = "",
    ttl_minutes: int = DISPATCH_IDEMPOTENCY_TTL_MINUTES,
    now: datetime | None = None,
) -> bool:
    """Return True when dispatching a conflict-repair comment is allowed.

    Re-dispatch is allowed when ANY of the following is true:

    * No conflict-repair marker exists on the PR.
    * The marker's ``head_sha`` differs from the current ``head_sha``
      (the PR branch has been updated since the last dispatch).
    * The marker's ``base_sha`` differs from the current ``base_sha``
      (the base branch has advanced again since the last dispatch).
    * The marker's timestamp is older than ``ttl_minutes``.

    An unparseable timestamp is treated as expired (fail-open), so a
    malformed marker can never permanently wedge the PR.

    Args:
        provider: CI platform provider for comment lookup.
        pr_number: Pull request number.
        head_sha: Current HEAD SHA of the PR branch.
        base_sha: Current tip SHA of the base branch.
        dispatch_login: Authenticated login that posts the dispatch comment.
            When provided, only markers from this identity are trusted for
            deduplication.
        ttl_minutes: Age threshold in minutes after which a marker expires.
        now: Override for the current time (UTC); defaults to ``datetime.now(timezone.utc)``.

    Returns:
        True if a (re)dispatch is allowed, False if a recent in-TTL marker
        for the same head and base already exists.
    """
    if dispatch_login:
        matching = [
            comment
            for comment in provider.list_issue_comments(pr_number)
            if comment.author == dispatch_login and CONFLICT_REPAIR_MARKER_PREFIX in comment.body
        ]
        if not matching:
            return True
        comment_body = max(matching, key=lambda comment: comment.id).body
    else:
        existing = provider.find_comment(pr_number, CONFLICT_REPAIR_MARKER_PREFIX)
        if existing is None:
            return True
        _, comment_body = existing

    match = _CONFLICT_REPAIR_MARKER_RE.search(comment_body)
    if not match:
        # Marker prefix found but body is unrecognised — treat as expired.
        logger.warning(
            "PR #%d: conflict-repair marker found but unparseable — treating as expired, allowing re-dispatch",
            pr_number,
        )
        return True

    marker_base_sha = match.group(1)
    marker_head_sha = match.group(2)
    timestamp_str = match.group(3).strip()

    # SHA change → always allow re-dispatch
    if marker_head_sha != head_sha:
        logger.info(
            "PR #%d: conflict-repair marker head SHA mismatch (marker=%s, current=%s) — allowing re-dispatch",
            pr_number,
            marker_head_sha[:8],
            head_sha[:8],
        )
        return True
    if marker_base_sha != base_sha:
        logger.info(
            "PR #%d: conflict-repair marker base SHA mismatch (marker=%s, current=%s) — allowing re-dispatch",
            pr_number,
            marker_base_sha[:8],
            base_sha[:8],
        )
        return True

    # TTL check
    marker_time = _parse_iso8601_timestamp_guard(timestamp_str)
    if marker_time is None:
        logger.warning(
            "PR #%d: conflict-repair marker has unparseable timestamp (%r) — treating as expired, allowing re-dispatch",
            pr_number,
            timestamp_str,
        )
        return True

    current_time = now if now is not None else datetime.now(UTC)
    age_minutes = (current_time - marker_time).total_seconds() / 60
    if age_minutes >= ttl_minutes:
        logger.info(
            "PR #%d: conflict-repair marker is %.1f min old (TTL=%d min) — allowing re-dispatch",
            pr_number,
            age_minutes,
            ttl_minutes,
        )
        return True

    logger.info(
        "PR #%d: conflict-repair marker is %.1f min old (TTL=%d min), same head+base — suppressing re-dispatch",
        pr_number,
        age_minutes,
        ttl_minutes,
    )
    return False


def count_conflict_repair_dispatches(
    provider: CIPlatformProvider,
    pr_number: int,
    head_sha: str,
    dispatch_login: str = "",
) -> int:
    """Count conflict-repair dispatches already made against ``head_sha``.

    Only markers whose embedded head SHA equals the *current* HEAD are
    counted: once the cloud agent pushes a resolution the HEAD changes, so
    the attempt budget naturally resets for the new commit.

    When ``dispatch_login`` is provided (non-empty), only comments authored
    by that identity are counted. This prevents any PR participant from
    inflating the attempt counter by posting a comment that contains the
    public marker format. When ``dispatch_login`` is empty the function
    falls back to excluding known Copilot identities, which preserves
    backwards compatibility for callers that cannot resolve the dispatch
    identity.

    Args:
        provider: CI platform provider for comment lookup.
        pr_number: Pull request number.
        head_sha: Current HEAD SHA of the PR branch.
        dispatch_login: GitHub login of the identity that posts dispatch
            comments (e.g. the ``SPECKIT_PR_TOKEN`` owner). When non-empty,
            only comments from this login are counted.

    Returns:
        Number of distinct comments carrying a conflict-repair marker for
        ``head_sha``. A comment containing several markers counts once.
    """
    count = 0
    for comment in provider.list_issue_comments(pr_number):
        if dispatch_login:
            if comment.author != dispatch_login:
                continue
        elif comment.author in COPILOT_COMMENT_LOGINS:
            continue
        if any(match.group(2) == head_sha for match in _CONFLICT_REPAIR_MARKER_RE.finditer(comment.body)):
            count += 1
    return count
