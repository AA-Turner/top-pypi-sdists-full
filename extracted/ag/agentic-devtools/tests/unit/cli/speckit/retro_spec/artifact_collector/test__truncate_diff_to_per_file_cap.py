"""Tests for _truncate_diff_to_per_file_cap in retro_spec/artifact_collector.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import (
    _SHORT_FILE_DIFF_TRUNCATION_MARKER,
    _truncate_diff_to_per_file_cap,
)


class TestTruncateDiffToPerFileCap:
    """Tests for the _truncate_diff_to_per_file_cap helper."""

    def test_returns_content_unchanged_when_within_cap(self) -> None:
        """Content under the per-file cap is returned unchanged."""
        assert _truncate_diff_to_per_file_cap("body", 10) == "body"

    def test_returns_empty_when_cap_is_zero(self) -> None:
        """A non-positive cap yields an empty diff body."""
        assert _truncate_diff_to_per_file_cap("body", 0) == ""

    def test_uses_compact_marker_when_full_marker_does_not_fit(self) -> None:
        """The short marker is used when only it fits inside the cap."""
        result = _truncate_diff_to_per_file_cap("abcdefghijklmnopqrstuvwxyz", len(_SHORT_FILE_DIFF_TRUNCATION_MARKER))

        assert result == _SHORT_FILE_DIFF_TRUNCATION_MARKER

    def test_preserves_prefix_when_short_marker_fits_with_room(self) -> None:
        """The short marker still preserves a content prefix when the cap allows both."""
        result = _truncate_diff_to_per_file_cap("abcdefghijklmnopqrstuvwxyz", 15)

        assert result == "abcd[truncated]"
        assert len(result) == 15

    def test_omits_marker_when_cap_is_smaller_than_compact_marker(self) -> None:
        """Tiny caps keep the limit instead of appending an oversized marker."""
        result = _truncate_diff_to_per_file_cap("abcdefghijklmnopqrstuvwxyz", 10)

        assert len(result) == 10
        assert result == "abcdefghij"
