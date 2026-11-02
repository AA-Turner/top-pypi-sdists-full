"""Tests for bound_fallback_context()."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.review.source_context import (
    _TRUNCATION_MARKER,
    bound_fallback_context,
)


class TestBoundFallbackContext:
    """Tests for bounding full-file fallback source context."""

    def test_returns_content_unchanged_when_within_budget(self) -> None:
        """Content shorter than the budget is returned verbatim."""
        content = "def helper():\n    return 1"
        assert bound_fallback_context(content, max_chars=1000) == content

    def test_returns_content_unchanged_when_exactly_at_budget(self) -> None:
        """Content exactly at the budget is not truncated."""
        content = "x" * 50
        assert bound_fallback_context(content, max_chars=50) == content

    def test_truncates_large_content_with_marker(self) -> None:
        """Content over the budget is clipped and carries the truncation marker."""
        content = "".join(f"line{i}\n" for i in range(1000))
        result = bound_fallback_context(content, max_chars=200)

        assert _TRUNCATION_MARKER in result
        assert len(result) == 200
        # Head and tail of the original content are preserved.
        assert result.startswith("line0")
        assert result.endswith("line999\n")

    def test_returns_head_slice_when_marker_exceeds_budget(self) -> None:
        """When the budget is smaller than the marker, return a plain head slice."""
        content = "abcdefghij"
        result = bound_fallback_context(content, max_chars=5)

        assert result == "abcde"
        assert _TRUNCATION_MARKER not in result

    def test_result_bounded_when_tail_len_is_zero(self) -> None:
        """When budget==1 tail_len is 0; result must not exceed max_chars."""
        marker_len = len(_TRUNCATION_MARKER)
        max_chars = marker_len + 1  # budget==1 => tail_len = 1//2 == 0
        content = "a" * (max_chars + 100)
        result = bound_fallback_context(content, max_chars=max_chars)
        assert len(result) == max_chars
        assert _TRUNCATION_MARKER in result
        # head is the single character before the marker, no tail
        assert result == f"a{_TRUNCATION_MARKER}"

    def test_rejects_non_positive_budget(self) -> None:
        """A non-positive max_chars raises ValueError."""
        with pytest.raises(ValueError, match="max_chars must be > 0"):
            bound_fallback_context("content", max_chars=0)
