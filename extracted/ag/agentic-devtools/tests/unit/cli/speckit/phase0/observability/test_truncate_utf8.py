"""Tests for truncate_utf8 in speckit/phase0/observability.py (FR-012e)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.observability import truncate_utf8


class TestTruncateUtf8:
    """Tests for the truncate_utf8 function."""

    def test_short_text_is_unchanged(self) -> None:
        assert truncate_utf8("hello") == "hello"

    def test_text_at_exact_limit_is_unchanged(self) -> None:
        text = "a" * 1024
        assert truncate_utf8(text) == text

    def test_long_text_is_truncated_with_marker(self) -> None:
        text = "a" * 2000
        result = truncate_utf8(text)
        assert result.endswith("\u2026[T]")
        assert len(result.encode("utf-8")) <= 1024

    def test_truncation_does_not_split_multibyte_character(self) -> None:
        # Each "é" is 2 bytes in UTF-8; force truncation right at a boundary.
        text = "\u00e9" * 600
        result = truncate_utf8(text)
        # Must decode cleanly (no stray/split multi-byte sequences).
        result.encode("utf-8").decode("utf-8")
        assert result.endswith("\u2026[T]")

    def test_custom_limits(self) -> None:
        text = "b" * 50
        result = truncate_utf8(text, byte_limit=10, prefix_limit=4, marker="...")
        assert result == "bbbb..."
        assert len(result.encode("utf-8")) <= 10

    def test_reduces_prefix_when_limit_splits_utf8_character(self) -> None:
        result = truncate_utf8("é" * 10, byte_limit=8, prefix_limit=5, marker="!")
        assert result == "éé!"

    def test_handles_empty_prefix_limit(self) -> None:
        assert truncate_utf8("é", byte_limit=1, prefix_limit=0, marker="!") == "!"

    def test_rejects_marker_larger_than_byte_limit(self) -> None:
        with pytest.raises(ValueError, match="exceeds byte_limit"):
            truncate_utf8("hello world", byte_limit=2, prefix_limit=0, marker="...")

    def test_prefix_limit_exceeding_budget_is_capped(self) -> None:
        # prefix_limit=10 + marker(3) = 13 > byte_limit=10, must be capped
        text = "b" * 50
        result = truncate_utf8(text, byte_limit=10, prefix_limit=10, marker="...")
        assert len(result.encode("utf-8")) <= 10
        assert result.endswith("...")

    def test_rejects_negative_prefix_limit(self) -> None:
        with pytest.raises(ValueError, match="prefix_limit"):
            truncate_utf8("hello world", byte_limit=5, prefix_limit=-1, marker=".")
