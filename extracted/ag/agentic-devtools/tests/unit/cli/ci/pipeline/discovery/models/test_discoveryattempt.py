"""Tests for DiscoveryAttempt dataclass."""

from __future__ import annotations

from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)


class TestDiscoveryAttempt:
    """Tests for DiscoveryAttempt dataclass."""

    def test_minimal_construction(self) -> None:
        attempt = DiscoveryAttempt(
            method="graphql",
            outcome=DiscoveryOutcome.SUCCESS,
        )
        assert attempt.method == "graphql"
        assert attempt.outcome == DiscoveryOutcome.SUCCESS
        assert attempt.suggestion_count == 0
        assert attempt.error_message == ""
        assert attempt.duration_ms == 0

    def test_full_construction(self) -> None:
        attempt = DiscoveryAttempt(
            method="rest-rederivation",
            outcome=DiscoveryOutcome.ERROR,
            suggestion_count=5,
            error_message="connection timeout",
            duration_ms=1234,
        )
        assert attempt.method == "rest-rederivation"
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert attempt.suggestion_count == 5
        assert attempt.error_message == "connection timeout"
        assert attempt.duration_ms == 1234

    def test_default_count_is_zero(self) -> None:
        attempt = DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.EMPTY,
        )
        assert attempt.suggestion_count == 0
