"""Tests for _should_retry and _get_retry_delay orchestrator helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)
from agentic_devtools.cli.ci.pipeline.discovery.orchestrator import (
    _get_retry_delay,
    _should_retry,
    run_discovery,
)
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot


class TestShouldRetry:
    """Tests for _should_retry helper."""

    def test_returns_false_when_no_inline_comments(self) -> None:
        """COMMENTED review with confirmed zero inline comments — no evidence."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
        )
        assert _should_retry(snapshot) is False

    def test_returns_false_when_no_reviews(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=3,
            reviews=[],
        )
        assert _should_retry(snapshot) is False

    def test_returns_true_when_review_recent_and_copilot(self) -> None:
        recent = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        review = ReviewInfo(id=100, user="Copilot", state="CHANGES_REQUESTED", submitted_at=recent)
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[review],
        )
        assert _should_retry(snapshot) is True

    def test_returns_false_when_review_too_old(self) -> None:
        old = (datetime.now(timezone.utc) - timedelta(seconds=600)).isoformat()
        review = ReviewInfo(id=100, user="Copilot", state="CHANGES_REQUESTED", submitted_at=old)
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[review],
        )
        assert _should_retry(snapshot) is False

    def test_returns_true_when_no_submitted_at(self) -> None:
        review = ReviewInfo(id=100, user="Copilot", state="CHANGES_REQUESTED", submitted_at="")
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[review],
        )
        assert _should_retry(snapshot) is True

    def test_returns_true_on_unparseable_submitted_at(self) -> None:
        review = ReviewInfo(id=100, user="Copilot", state="CHANGES_REQUESTED", submitted_at="not-a-date")
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[review],
        )
        assert _should_retry(snapshot) is True

    def test_returns_false_when_review_id_not_matched(self) -> None:
        recent = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        review = ReviewInfo(id=999, user="Copilot", state="CHANGES_REQUESTED", submitted_at=recent)
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[review],
        )
        assert _should_retry(snapshot) is False

    def test_returns_false_when_user_not_copilot(self) -> None:
        recent = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        review = ReviewInfo(id=100, user="human-user", state="CHANGES_REQUESTED", submitted_at=recent)
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[review],
        )
        assert _should_retry(snapshot) is False

    def test_returns_true_for_trusted_synthetic_review(self) -> None:
        """Trusted synthetic review with SYNTHETIC_MARKER qualifies for retry."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import SYNTHETIC_MARKER, TRUSTED_SYNTHETIC_USERS

        synthetic_user = next(iter(TRUSTED_SYNTHETIC_USERS))
        recent = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        review = ReviewInfo(
            id=100,
            user=synthetic_user,
            state="CHANGES_REQUESTED",
            submitted_at=recent,
            body=f"Review feedback. {SYNTHETIC_MARKER}",
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[review],
        )
        assert _should_retry(snapshot) is True

    def test_returns_true_for_changes_requested_with_zero_inline_count(self) -> None:
        """CHANGES_REQUESTED review with inline_count=0 still qualifies for retry.

        The snapshot builder only counts inline comments for COMMENTED reviews,
        so inline_count=0 on a CHANGES_REQUESTED review means "not counted",
        not "confirmed zero".  Retries must fire to avoid missing suggestions.
        """
        recent = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        review = ReviewInfo(id=100, user="Copilot", state="CHANGES_REQUESTED", submitted_at=recent)
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,  # not tracked for CHANGES_REQUESTED
            reviews=[review],
        )
        assert _should_retry(snapshot) is True

    def test_returns_true_when_unknown_inline_count(self) -> None:
        """Unknown inline count (-1) is treated as potential evidence (fail closed)."""
        recent = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        review = ReviewInfo(id=100, user="Copilot", state="COMMENTED", submitted_at=recent)
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=-1,  # unknown: fetch failed
            reviews=[review],
        )
        assert _should_retry(snapshot) is True


class TestGetRetryDelay:
    """Tests for _get_retry_delay helper."""

    def test_returns_default_when_env_not_set(self) -> None:
        with patch.dict("os.environ", {}, clear=False):
            # Ensure env var not set
            import os

            os.environ.pop("APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS", None)
            result = _get_retry_delay()
        assert result == 10

    def test_returns_env_value_when_set(self) -> None:
        with patch.dict("os.environ", {"APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS": "30"}):
            result = _get_retry_delay()
        assert result == 30

    def test_returns_default_on_invalid_env_value(self) -> None:
        with patch.dict("os.environ", {"APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS": "abc"}):
            result = _get_retry_delay()
        assert result == 10

    def test_clamps_to_minimum_of_1(self) -> None:
        with patch.dict("os.environ", {"APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS": "0"}):
            result = _get_retry_delay()
        assert result == 1


class TestRunDiscoveryRetry:
    """Tests for retry logic in run_discovery."""

    def test_retries_when_should_retry_returns_true(self) -> None:
        """Verifies that retry logic fires when conditions are met."""
        recent = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        review = ReviewInfo(id=100, user="Copilot", state="CHANGES_REQUESTED", submitted_at=recent)
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[review],
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.time.sleep") as mock_sleep,
            patch.dict("os.environ", {"APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS": "1"}),
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)
            suggestions, attempts, _node_id = run_discovery(provider, snapshot)

        assert suggestions == []
        # Should have 2 full rounds of attempts (graphql+rest+html) × 2 = 6
        assert len(attempts) == 6
        mock_sleep.assert_called_once_with(1)

    def test_emits_discrepancy_when_inline_comments_but_empty(self) -> None:
        """DISCOVERY-DISCREPANCY warning emitted when inline_count > 0 but no suggestions."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=3,
            reviews=[],  # No reviews means _should_retry returns False
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.logger") as mock_logger,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)
            run_discovery(provider, snapshot)

        # Check that warning was emitted with DISCOVERY-DISCREPANCY
        mock_logger.warning.assert_called()
        call_args = mock_logger.warning.call_args[0][0]
        assert "DISCOVERY-DISCREPANCY" in call_args

    def test_breaks_on_timeout_cap(self) -> None:
        """Lines 74-80: timeout cap prevents retry."""
        recent = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        review = ReviewInfo(id=100, user="Copilot", state="CHANGES_REQUESTED", submitted_at=recent)
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[review],
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY)

        # Simulate elapsed time exceeding timeout cap
        # start_time = 0, on retry check monotonic returns 200 (200 + delay > 120)
        call_count = [0]

        def fake_monotonic():
            call_count[0] += 1
            if call_count[0] == 1:
                return 0.0  # start_time
            return 200.0  # elapsed check on retry

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.time.monotonic", side_effect=fake_monotonic),
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.time.sleep"),
            patch.dict("os.environ", {"APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS": "5"}),
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)
            suggestions, attempts, _node_id = run_discovery(provider, snapshot)

        assert suggestions == []
        # Only 1 round of attempts (break prevented second iteration)
        assert len(attempts) == 3

    def test_emits_discrepancy_for_changes_requested_with_zero_inline_count(self) -> None:
        """DISCOVERY-DISCREPANCY fires for CHANGES_REQUESTED even when inline_count=0.

        The snapshot builder does not count inline comments for CHANGES_REQUESTED
        reviews, so inline_count=0 means "not tracked", not "confirmed zero".
        """
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,  # not tracked for CHANGES_REQUESTED
            reviews=[],
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.logger") as mock_logger,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)
            run_discovery(provider, snapshot)

        mock_logger.warning.assert_called()
        call_args = mock_logger.warning.call_args[0][0]
        assert "DISCOVERY-DISCREPANCY" in call_args

    def test_emits_discrepancy_when_unknown_inline_count(self) -> None:
        """DISCOVERY-DISCREPANCY fires when inline_count=-1 (unknown, fail closed)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=-1,  # unknown: fetch failed
            reviews=[],
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.logger") as mock_logger,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)
            run_discovery(provider, snapshot)

        mock_logger.warning.assert_called()
        call_args = mock_logger.warning.call_args[0][0]
        assert "DISCOVERY-DISCREPANCY" in call_args

    def test_no_discrepancy_when_commented_with_zero_inline_count(self) -> None:
        """No DISCOVERY-DISCREPANCY when COMMENTED review has confirmed zero inline comments."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,  # confirmed: fetch succeeded with 0 results
            reviews=[],
        )
        provider = MagicMock()
        graphql_attempt = DiscoveryAttempt(method="graphql", outcome=DiscoveryOutcome.EMPTY)
        rest_attempt = DiscoveryAttempt(method="rest", outcome=DiscoveryOutcome.EMPTY)
        html_attempt = DiscoveryAttempt(method="html", outcome=DiscoveryOutcome.EMPTY)

        with (
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.graphql_discover") as mock_graphql,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.rest_discover") as mock_rest,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.html_discover") as mock_html,
            patch("agentic_devtools.cli.ci.pipeline.discovery.orchestrator.logger") as mock_logger,
        ):
            mock_graphql.return_value = ([], graphql_attempt, "")
            mock_rest.return_value = ([], rest_attempt)
            mock_html.return_value = ([], html_attempt)
            run_discovery(provider, snapshot)

        for call in mock_logger.warning.call_args_list:
            assert "DISCOVERY-DISCREPANCY" not in call[0][0]
