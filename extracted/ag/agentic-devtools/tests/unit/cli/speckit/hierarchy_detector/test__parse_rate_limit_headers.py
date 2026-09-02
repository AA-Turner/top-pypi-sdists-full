"""Tests for _parse_rate_limit_headers helper."""

from __future__ import annotations

from agentic_devtools.cli.speckit.hierarchy_detector import _parse_rate_limit_headers


class TestParseRateLimitHeaders:
    """Tests for _parse_rate_limit_headers helper."""

    def test_valid_headers(self) -> None:
        """Extracts remaining and reset from valid headers."""
        headers = "x-ratelimit-remaining: 4990\nx-ratelimit-reset: 1718650800"
        remaining, reset = _parse_rate_limit_headers(headers)
        assert remaining == 4990
        assert reset == 1718650800.0

    def test_missing_headers(self) -> None:
        """Returns defaults when headers are missing."""
        remaining, reset = _parse_rate_limit_headers("content-type: application/json")
        assert remaining == 9999
        assert reset == 0.0

    def test_case_insensitive(self) -> None:
        """Header matching is case-insensitive."""
        headers = "X-RateLimit-Remaining: 100\nX-RateLimit-Reset: 1000"
        remaining, reset = _parse_rate_limit_headers(headers)
        assert remaining == 100
        assert reset == 1000.0
