"""Tests for _parse_retry_after header parsing helper."""

from agentic_devtools.hierarchy.cascade import _parse_retry_after


class TestParseRetryAfter:
    """Tests for the _parse_retry_after helper function."""

    def test_returns_float_when_header_present(self) -> None:
        """Returns the numeric Retry-After value as float when the header is present."""
        headers = "HTTP/2 429\nRetry-After: 45\nContent-Type: application/json\n\n{}"
        assert _parse_retry_after(headers) == 45.0

    def test_returns_none_when_header_absent(self) -> None:
        """Returns None when no Retry-After header is present."""
        headers = "HTTP/2 200\nContent-Type: application/json\n\n{}"
        assert _parse_retry_after(headers) is None

    def test_returns_none_for_non_numeric_retry_after(self) -> None:
        """Returns None when Retry-After header value is not a valid number (ValueError branch)."""
        headers = "HTTP/2 429\nRetry-After: not-a-number\nContent-Type: application/json\n\n{}"
        assert _parse_retry_after(headers) is None

    def test_case_insensitive_header_matching(self) -> None:
        """Matches Retry-After header case-insensitively."""
        headers = "HTTP/2 429\nretry-after: 30\n\n{}"
        assert _parse_retry_after(headers) == 30.0

    def test_returns_none_for_empty_string(self) -> None:
        """Returns None for empty headers text."""
        assert _parse_retry_after("") is None
