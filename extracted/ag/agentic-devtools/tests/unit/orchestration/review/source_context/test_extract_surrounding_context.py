"""Tests for extract_surrounding_context()."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.review.source_context import extract_surrounding_context


class TestExtractSurroundingContext:
    """Tests for surrounding context extraction."""

    def test_empty_file_returns_empty(self) -> None:
        """Empty file content returns empty string."""
        assert extract_surrounding_context("", [(1, 5)]) == ""

    def test_empty_diff_lines_returns_empty(self) -> None:
        """Empty diff_lines returns empty string."""
        assert extract_surrounding_context("line1\nline2", []) == ""

    def test_blank_content_with_diff_returns_empty(self) -> None:
        """Blank content that splits to zero lines still returns an empty string."""

        class BlankContent(str):
            def splitlines(self, keepends: bool = False) -> list[str]:  # noqa: ARG002
                return []

        assert extract_surrounding_context(BlankContent("placeholder"), [(1, 1)]) == ""

    def test_extracts_context_around_hunk(self) -> None:
        """Extracts at least 20 lines above and below a diff hunk."""
        lines = [f"line {i}" for i in range(1, 101)]
        content = "\n".join(lines)

        result = extract_surrounding_context(content, [(50, 55)])
        assert result != ""
        assert "line 50" in result
        assert "line 55" in result

    def test_includes_imports_from_top(self) -> None:
        """Includes import statements from the top of the file."""
        content = "import os\nimport sys\n\nclass Foo:\n    pass\n" + "\n".join(f"# line {i}" for i in range(6, 50))

        result = extract_surrounding_context(content, [(40, 42)])
        assert "import os" in result

    def test_handles_hunk_at_start_of_file(self) -> None:
        """Handles diff hunk at the very start of the file."""
        lines = [f"line {i}" for i in range(1, 51)]
        content = "\n".join(lines)

        result = extract_surrounding_context(content, [(1, 3)])
        assert result != ""
        assert "line 1" in result

    def test_handles_hunk_at_end_of_file(self) -> None:
        """Handles diff hunk at the very end of the file."""
        lines = [f"line {i}" for i in range(1, 51)]
        content = "\n".join(lines)

        result = extract_surrounding_context(content, [(48, 50)])
        assert result != ""
        assert "line 50" in result

    def test_negative_context_lines_raises_value_error(self) -> None:
        """Negative context_lines is rejected explicitly."""
        with pytest.raises(ValueError, match="context_lines must be >= 0"):
            extract_surrounding_context("line 1\nline 2", [(1, 1)], context_lines=-1)

    def test_out_of_bounds_diff_hunk_skipped(self) -> None:
        """Diff hunks beyond the file length produce no output and no stray markers.

        Removed-line anchors in a diff reference base-file line numbers that
        may not exist in the source-branch version; the function must skip
        such invalid ranges instead of emitting empty sections or stray '...'
        markers.
        """
        lines = [f"line {i}" for i in range(1, 6)]  # 5-line file
        content = "\n".join(lines)

        # Hunk at line 100 is well beyond the 5-line file
        result = extract_surrounding_context(content, [(100, 110)], context_lines=3)
        assert result == ""

    def test_mixed_valid_and_out_of_bounds_hunks(self) -> None:
        """Valid hunks are extracted even when some hunks are out of bounds."""
        lines = [f"line {i}" for i in range(1, 11)]  # 10-line file
        content = "\n".join(lines)

        # First hunk is valid, second is beyond the file
        result = extract_surrounding_context(content, [(3, 4), (200, 210)], context_lines=1)
        assert "line 3" in result
        assert "line 4" in result
        # Should not have a stray trailing '...' from the out-of-bounds hunk
        # (there may be one trailing '...' from the valid hunk, but not extras)
        assert result.count("...") <= 1

    def test_single_range_no_trailing_ellipsis(self) -> None:
        """A single merged range produces no trailing '...' separator."""
        lines = [f"line {i}" for i in range(1, 21)]
        content = "\n".join(lines)

        result = extract_surrounding_context(content, [(10, 11)], context_lines=2)
        assert result != ""
        assert not result.endswith("...")
        assert "..." not in result

    def test_multiple_ranges_separated_by_ellipsis(self) -> None:
        """Multiple non-adjacent merged ranges are separated by '...' but not trailed by one."""
        # 100-line file; two hunks far enough apart to remain as separate merged ranges
        lines = [f"line {i}" for i in range(1, 101)]
        content = "\n".join(lines)

        result = extract_surrounding_context(content, [(10, 11), (80, 81)], context_lines=2)
        assert "line 10" in result
        assert "line 80" in result
        # Exactly one '...' separator between the two ranges; no trailing one
        assert result.count("...") == 1
        assert not result.endswith("...")
