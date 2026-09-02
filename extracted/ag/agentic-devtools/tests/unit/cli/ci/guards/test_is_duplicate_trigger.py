"""Tests for is_duplicate_trigger guard."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.guards import DISPATCH_IDEMPOTENCY_TTL_MINUTES, is_duplicate_trigger
from agentic_devtools.cli.ci.models import IssueCommentInfo


class TestIsDuplicateTrigger:
    """Tests for is_duplicate_trigger (FR-012)."""

    def test_returns_true_when_legacy_marker_exists(self) -> None:
        """Legacy trigger comment (no timestamp) permanently blocks duplicate."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=200,
                author="copilot",
                body="@copilot - Review\n\n<!-- copilot-trigger:4401589029 -->\n",
            )
        ]

        result = is_duplicate_trigger(provider, pr_number=42, review_id=4401589029)

        assert result is True
        provider.list_issue_comments.assert_called_once_with(42)

    def test_returns_false_when_no_marker_exists(self) -> None:
        """No existing trigger comment allows new dispatch."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        result = is_duplicate_trigger(provider, pr_number=42, review_id=4401589029)

        assert result is False
        provider.list_issue_comments.assert_called_once_with(42)

    def test_returns_false_for_zero_review_id(self) -> None:
        """Zero review_id (CI-only repair) skips the check entirely."""
        provider = MagicMock()

        result = is_duplicate_trigger(provider, pr_number=42, review_id=0)

        assert result is False
        provider.list_issue_comments.assert_not_called()

    def test_returns_false_for_negative_review_id(self) -> None:
        """Negative review_id skips the check entirely."""
        provider = MagicMock()

        result = is_duplicate_trigger(provider, pr_number=42, review_id=-1)

        assert result is False
        provider.list_issue_comments.assert_not_called()

    def test_different_review_id_not_blocked(self) -> None:
        """A different review_id is not blocked by an existing trigger."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=201, author="copilot", body="@copilot\n\n<!-- copilot-trigger:12345678 -->")
        ]

        result = is_duplicate_trigger(provider, pr_number=42, review_id=9999999)

        assert result is False

    def test_concurrent_triggers_same_review_id(self) -> None:
        """Second trigger for same review_id is blocked once first is posted."""
        provider = MagicMock()
        # First call: no existing comment
        provider.list_issue_comments.side_effect = [
            [],  # first trigger check
            [IssueCommentInfo(id=300, author="copilot", body="@copilot\n\n<!-- copilot-trigger:12345 -->")],
        ]

        # First trigger passes
        result1 = is_duplicate_trigger(provider, pr_number=10, review_id=12345)
        assert result1 is False

        # Second trigger is blocked (legacy marker = permanent block)
        result2 = is_duplicate_trigger(provider, pr_number=10, review_id=12345)
        assert result2 is True

    def test_timestamped_marker_within_ttl_blocks(self) -> None:
        """Timestamped marker younger than TTL blocks re-dispatch."""
        provider = MagicMock()
        now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        # Marker written 10 minutes ago (well within 60-minute TTL)
        marker_time = datetime(2024, 6, 1, 11, 50, 0, tzinfo=timezone.utc)
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=200,
                author="copilot",
                body=f"@copilot\n\n<!-- copilot-trigger:999:{marker_time.isoformat()} -->\n",
            )
        ]

        result = is_duplicate_trigger(provider, pr_number=5, review_id=999, now=now)

        assert result is True

    def test_timestamped_marker_older_than_ttl_allows_redispatch(self) -> None:
        """Timestamped marker older than TTL allows re-dispatch."""
        provider = MagicMock()
        now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        # Marker written 90 minutes ago (exceeds 60-minute TTL)
        marker_time = datetime(2024, 6, 1, 10, 30, 0, tzinfo=timezone.utc)
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=200,
                author="copilot",
                body=f"@copilot\n\n<!-- copilot-trigger:888:{marker_time.isoformat()} -->\n",
            )
        ]

        result = is_duplicate_trigger(provider, pr_number=5, review_id=888, now=now)

        assert result is False

    def test_unparseable_timestamp_treated_as_non_expired(self) -> None:
        """Marker with unparseable timestamp is treated as non-expired (fail-closed)."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=200,
                author="copilot",
                body="@copilot\n\n<!-- copilot-trigger:777:not-a-timestamp -->\n",
            )
        ]

        result = is_duplicate_trigger(provider, pr_number=5, review_id=777)

        assert result is True

    def test_prefix_only_match_does_not_block(self) -> None:
        """A different review ID sharing the same prefix must not match."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=200, author="copilot", body="@copilot\n\n<!-- copilot-trigger:1234 -->\n")
        ]

        result = is_duplicate_trigger(provider, pr_number=5, review_id=123)

        assert result is False

    def test_newest_timestamped_marker_controls_ttl(self) -> None:
        """A newer in-TTL marker blocks even when an older matching marker is expired."""
        provider = MagicMock()
        now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=100,
                author="copilot",
                body="@copilot\n\n<!-- copilot-trigger:999:2024-06-01T10:00:00+00:00 -->\n",
            ),
            IssueCommentInfo(
                id=101,
                author="copilot",
                body="@copilot\n\n<!-- copilot-trigger:999:2024-06-01T11:50:00+00:00 -->\n",
            ),
        ]

        result = is_duplicate_trigger(provider, pr_number=5, review_id=999, now=now)

        assert result is True

    def test_newest_timestamped_marker_controls_ttl_for_newest_first_order(self) -> None:
        """Newest-first provider ordering must still use the newest marker."""
        provider = MagicMock()
        now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=101,
                author="copilot",
                body="@copilot\n\n<!-- copilot-trigger:999:2024-06-01T11:50:00+00:00 -->\n",
            ),
            IssueCommentInfo(
                id=100,
                author="copilot",
                body="@copilot\n\n<!-- copilot-trigger:999:2024-06-01T10:00:00+00:00 -->\n",
            ),
        ]

        result = is_duplicate_trigger(provider, pr_number=5, review_id=999, now=now)

        assert result is True

    def test_legacy_marker_anywhere_still_blocks(self) -> None:
        """Older legacy markers remain blocking even if a newer timestamped marker expired."""
        provider = MagicMock()
        now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=100, author="copilot", body="@copilot\n\n<!-- copilot-trigger:999 -->\n"),
            IssueCommentInfo(
                id=101,
                author="copilot",
                body="@copilot\n\n<!-- copilot-trigger:999:2024-06-01T10:00:00+00:00 -->\n",
            ),
        ]

        result = is_duplicate_trigger(provider, pr_number=5, review_id=999, now=now)

        assert result is True

    def test_default_ttl_is_dispatch_idempotency_ttl(self) -> None:
        """Default TTL constant value is DISPATCH_IDEMPOTENCY_TTL_MINUTES (60)."""
        assert DISPATCH_IDEMPOTENCY_TTL_MINUTES == 60

    def test_detects_end_placed_marker_from_build_repair_comment(self) -> None:
        """Dedup still fires when the marker sits at the end of a real repair comment.

        The marker was moved to the end of the comment body (truncation-safety);
        because detection is substring/regex-based over the full body, end
        placement must not change deduplication behaviour.
        """
        body = (
            "@copilot - repair needed\n\n"
            "<details>\n"
            "<summary>Review feedback</summary>\n\n"
            "- item\n\n"
            "</details>\n\n"
            "<!-- copilot-trigger:777:2024-06-01T12:00:00+00:00 -->"
        )
        provider = MagicMock()
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=1, author="copilot", body=body)]

        now = datetime(2024, 6, 1, 12, 5, 0, tzinfo=timezone.utc)

        result = is_duplicate_trigger(provider, pr_number=42, review_id=777, ttl_minutes=60, now=now)

        assert result is True
