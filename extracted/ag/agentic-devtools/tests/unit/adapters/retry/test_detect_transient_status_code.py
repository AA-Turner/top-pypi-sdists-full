"""Tests for the shared transient HTTP status-code matcher."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.retry import detect_transient_status_code


class TestDetectTransientStatusCode:
    """Verify precise ``HTTP <code>`` detection used by all transient paths."""

    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("HTTP 429 too many requests", 429),
            ("HTTP 502 bad gateway", 502),
            ("HTTP 503 service unavailable", 503),
            ("HTTP/2.0 503 service unavailable", 503),
            ("gh: request failed (http 503)", 503),
            ("503 service unavailable", 503),
        ],
    )
    def test_returns_code_for_transient_error_text(self, text, expected):
        assert detect_transient_status_code(text) == expected

    @pytest.mark.parametrize(
        "text",
        [
            "processed 429 rows",  # standalone number, no HTTP prefix
            "error code 1429",  # adjacent leading digit
            "HTTP 50200 weird status",  # adjacent trailing digit
            "err503 service unavailable",  # adjacent leading letters
            "HTTP 404 not found",  # non-transient status
            "HTTP 500 internal server error",  # excluded by the shared retry contract
            "HTTP 504 gateway timeout",  # excluded by the shared retry contract
            "500 internal server error",
            "504 gateway timeout",
            "no status here",
        ],
    )
    def test_returns_none_for_non_transient_text(self, text):
        assert detect_transient_status_code(text) is None
