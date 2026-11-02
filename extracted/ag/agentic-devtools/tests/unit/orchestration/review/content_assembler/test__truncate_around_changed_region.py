"""Tests for _truncate_around_changed_region function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.content_assembler import _truncate_around_changed_region


class TestTruncateAroundChangedRegion:
    """Tests for the changed-region-aware truncation helper."""

    def test_returns_empty_for_non_positive_budget(self) -> None:
        """max_chars=0 returns an empty string."""
        assert _truncate_around_changed_region("abcdef", max_chars=0, diff_lines=[1]) == ""

    def test_returns_original_when_content_fits(self) -> None:
        """Content shorter than budget is returned unchanged."""
        assert _truncate_around_changed_region("abc", max_chars=10, diff_lines=[1]) == "abc"

    def test_without_diff_lines_falls_back_to_prefix(self) -> None:
        """Empty diff_lines uses a simple prefix truncation."""
        assert _truncate_around_changed_region("abcdef", max_chars=3, diff_lines=[]) == "abc"

    def test_handles_splitlines_empty_case(self) -> None:
        """Newline-only content produces no logical lines; falls back to simple prefix."""
        assert _truncate_around_changed_region("\n\n\n", max_chars=2, diff_lines=[1]) == "\n\n"

    def test_handles_out_of_range_diff_lines(self) -> None:
        """Diff lines beyond the file length fall back to prefix truncation."""
        assert _truncate_around_changed_region("line1\nline2", max_chars=5, diff_lines=[99]) == "line1"

    def test_falls_back_when_marker_budget_is_too_small(self) -> None:
        """Output is bounded by max_chars even when marker text itself is large."""
        content = "\n".join(f"line {i}" for i in range(1, 20))
        out = _truncate_around_changed_region(content, max_chars=20, diff_lines=[10])
        assert len(out) <= 20
        assert "line 1" in out

    def test_handles_large_changed_region_window(self) -> None:
        """A changed region that alone exceeds the budget gets prefix-style truncation."""
        content = "\n".join(["prefix", "x" * 500, "suffix"])
        out = _truncate_around_changed_region(content, max_chars=120, diff_lines=[2])
        assert "omitted before changed region" in out
        assert "omitted after changed region" in out

    def test_expands_around_changed_region_and_marks_omissions(self) -> None:
        """Context lines around the changed region are included with omission markers."""
        content = "\n".join(f"line {i}" for i in range(1, 50))
        out = _truncate_around_changed_region(content, max_chars=120, diff_lines=[25])
        assert "line 25" in out
        assert "omitted before changed region" in out
        assert "omitted after changed region" in out

    def test_handles_changed_line_at_file_start(self) -> None:
        """No 'omitted before' marker when the changed line is at the file start."""
        content = "\n".join(f"line {i}" for i in range(1, 50))
        out = _truncate_around_changed_region(content, max_chars=120, diff_lines=[1])
        assert "line 1" in out
        assert "omitted before changed region" not in out
        assert "omitted after changed region" in out

    def test_handles_changed_line_at_file_end(self) -> None:
        """No 'omitted after' marker when the changed line is at the file end."""
        content = "\n".join(f"line {i}" for i in range(1, 50))
        out = _truncate_around_changed_region(content, max_chars=120, diff_lines=[49])
        assert "line 49" in out
        assert "omitted before changed region" in out
        assert "omitted after changed region" not in out
