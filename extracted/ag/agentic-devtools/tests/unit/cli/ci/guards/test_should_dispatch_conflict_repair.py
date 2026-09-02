"""Tests for should_dispatch_conflict_repair() guard helper."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.guards import (
    CONFLICT_REPAIR_MARKER_PREFIX,
    DISPATCH_IDEMPOTENCY_TTL_MINUTES,
    should_dispatch_conflict_repair,
)
from agentic_devtools.cli.ci.models import IssueCommentInfo

_HEAD = "abc" * 13 + "a"  # 40-char hex-like head SHA
_BASE = "def" * 13 + "d"  # 40-char hex-like base SHA
_NOW = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)


def _marker(base_sha: str, head_sha: str, ts: datetime) -> str:
    return f"<!-- agdt:conflict-repair:{base_sha}:{head_sha}:{ts.isoformat()} -->"


class TestShouldDispatchConflictRepair:
    """Tests for the conflict-repair idempotency guard."""

    def test_no_marker_allows_dispatch(self) -> None:
        """No existing marker → dispatch is allowed."""
        provider = MagicMock()
        provider.find_comment.return_value = None

        result = should_dispatch_conflict_repair(provider, pr_number=1, head_sha=_HEAD, base_sha=_BASE, now=_NOW)

        assert result is True
        provider.find_comment.assert_called_once_with(1, CONFLICT_REPAIR_MARKER_PREFIX)

    def test_same_head_base_within_ttl_blocks(self) -> None:
        """Same head + base, marker newer than TTL → dispatch suppressed."""
        provider = MagicMock()
        # Marker written 10 minutes ago (within 60-minute TTL)
        marker_time = datetime(2024, 6, 1, 11, 50, 0, tzinfo=timezone.utc)
        provider.find_comment.return_value = (100, _marker(_BASE, _HEAD, marker_time))

        result = should_dispatch_conflict_repair(provider, pr_number=1, head_sha=_HEAD, base_sha=_BASE, now=_NOW)

        assert result is False

    def test_same_head_base_after_ttl_allows(self) -> None:
        """Same head + base, marker older than TTL → dispatch allowed."""
        provider = MagicMock()
        # Marker written 90 minutes ago (exceeds 60-minute TTL)
        marker_time = datetime(2024, 6, 1, 10, 30, 0, tzinfo=timezone.utc)
        provider.find_comment.return_value = (100, _marker(_BASE, _HEAD, marker_time))

        result = should_dispatch_conflict_repair(provider, pr_number=1, head_sha=_HEAD, base_sha=_BASE, now=_NOW)

        assert result is True

    def test_head_sha_changed_allows(self) -> None:
        """Marker exists for an old head SHA → dispatch allowed (head changed)."""
        provider = MagicMock()
        old_head = "111" * 13 + "1"
        marker_time = datetime(2024, 6, 1, 11, 50, 0, tzinfo=timezone.utc)  # within TTL
        provider.find_comment.return_value = (100, _marker(_BASE, old_head, marker_time))

        result = should_dispatch_conflict_repair(provider, pr_number=1, head_sha=_HEAD, base_sha=_BASE, now=_NOW)

        assert result is True

    def test_base_sha_changed_allows(self) -> None:
        """Marker exists for an old base SHA → dispatch allowed (base changed)."""
        provider = MagicMock()
        old_base = "222" * 13 + "2"
        marker_time = datetime(2024, 6, 1, 11, 50, 0, tzinfo=timezone.utc)  # within TTL
        provider.find_comment.return_value = (100, _marker(old_base, _HEAD, marker_time))

        result = should_dispatch_conflict_repair(provider, pr_number=1, head_sha=_HEAD, base_sha=_BASE, now=_NOW)

        assert result is True

    def test_unparseable_timestamp_allows(self) -> None:
        """Marker with unparseable timestamp → fail-open, dispatch allowed."""
        provider = MagicMock()
        bad_marker = f"<!-- agdt:conflict-repair:{_BASE}:{_HEAD}:not-a-time -->"
        provider.find_comment.return_value = (100, bad_marker)

        result = should_dispatch_conflict_repair(provider, pr_number=1, head_sha=_HEAD, base_sha=_BASE, now=_NOW)

        assert result is True

    def test_unrecognised_marker_body_allows(self) -> None:
        """Marker prefix found but body doesn't match pattern → treat as expired."""
        provider = MagicMock()
        provider.find_comment.return_value = (100, f"{CONFLICT_REPAIR_MARKER_PREFIX}malformed -->")

        result = should_dispatch_conflict_repair(provider, pr_number=1, head_sha=_HEAD, base_sha=_BASE, now=_NOW)

        assert result is True

    def test_dispatch_login_ignores_matching_marker_from_other_author(self) -> None:
        """Dedup trusts only markers posted by the authenticated dispatch identity."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=100, author="outsider", body=_marker(_BASE, _HEAD, _NOW), created_at=_NOW.isoformat())
        ]

        result = should_dispatch_conflict_repair(
            provider,
            pr_number=1,
            head_sha=_HEAD,
            base_sha=_BASE,
            dispatch_login="loop-bot",
            now=_NOW,
        )

        assert result is True
        provider.list_issue_comments.assert_called_once_with(1)
        provider.find_comment.assert_not_called()

    def test_dispatch_login_blocks_on_matching_marker_from_dispatch_author(self) -> None:
        """A fresh marker from the dispatch identity still suppresses re-dispatch."""
        provider = MagicMock()
        marker_time = datetime(2024, 6, 1, 11, 50, 0, tzinfo=timezone.utc)
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=100,
                author="loop-bot",
                body=_marker(_BASE, _HEAD, marker_time),
                created_at=marker_time.isoformat(),
            )
        ]

        result = should_dispatch_conflict_repair(
            provider,
            pr_number=1,
            head_sha=_HEAD,
            base_sha=_BASE,
            dispatch_login="loop-bot",
            now=_NOW,
        )

        assert result is False

    def test_default_ttl_constant(self) -> None:
        """DISPATCH_IDEMPOTENCY_TTL_MINUTES is the shared constant value (60)."""
        assert DISPATCH_IDEMPOTENCY_TTL_MINUTES == 60

    def test_exactly_at_ttl_boundary_allows(self) -> None:
        """Marker exactly at TTL boundary (age == ttl_minutes) is treated as expired."""
        provider = MagicMock()
        marker_time = datetime(2024, 6, 1, 11, 0, 0, tzinfo=timezone.utc)  # exactly 60 min ago
        provider.find_comment.return_value = (100, _marker(_BASE, _HEAD, marker_time))

        result = should_dispatch_conflict_repair(
            provider, pr_number=1, head_sha=_HEAD, base_sha=_BASE, now=_NOW, ttl_minutes=60
        )

        assert result is True
