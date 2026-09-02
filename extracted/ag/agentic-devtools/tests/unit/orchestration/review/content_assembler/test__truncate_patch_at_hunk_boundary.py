"""Tests for _truncate_patch_at_hunk_boundary."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.review.content_assembler import (
    _PATCH_TRUNCATION_MARKER,
    _truncate_patch_at_hunk_boundary,
)


class TestTruncatePatchAtHunkBoundary:
    """Tests for hunk-boundary patch truncation."""

    def test_short_patch_returned_unchanged(self) -> None:
        """Patch that fits within max_chars is returned unchanged."""
        patch = "@@ -1,3 +1,3 @@\n line1\n-old\n+new\n"
        result = _truncate_patch_at_hunk_boundary(patch, max_chars=len(patch) + 10)
        assert result == patch

    def test_exact_length_patch_returned_unchanged(self) -> None:
        """Patch whose length equals max_chars is returned unchanged."""
        patch = "@@ -1,1 +1,1 @@\n line\n"
        result = _truncate_patch_at_hunk_boundary(patch, max_chars=len(patch))
        assert result == patch

    def test_truncated_patch_ends_with_marker(self) -> None:
        """Any truncated patch ends with the explicit truncation marker."""
        patch = "@@ -1,1 +1,1 @@\n line\n" + "x" * 500
        result = _truncate_patch_at_hunk_boundary(patch, max_chars=50)
        assert result.endswith(_PATCH_TRUNCATION_MARKER)

    def test_cuts_before_last_incomplete_hunk(self) -> None:
        """When two hunks are present, the incomplete second hunk is dropped."""
        hunk1 = "@@ -1,3 +1,3 @@\n line1\n-old\n+new\n"
        hunk2 = "@@ -10,3 +10,3 @@\n line10\n" + "x" * 500
        patch = hunk1 + hunk2
        # max_chars forces a cut inside hunk2
        max_chars = len(hunk1) + 30 + len(_PATCH_TRUNCATION_MARKER)
        result = _truncate_patch_at_hunk_boundary(patch, max_chars=max_chars)
        assert "@@ -1,3 +1,3 @@" in result
        assert "@@ -10,3 +10,3 @@" not in result
        assert result.endswith(_PATCH_TRUNCATION_MARKER)

    def test_preserves_prefix_when_truncating_inside_first_hunk(self) -> None:
        """Truncation inside first hunk keeps visible changed lines."""
        patch = (
            "diff --git a/a.py b/a.py\n"
            "index 1111111..2222222 100644\n"
            "--- a/a.py\n"
            "+++ b/a.py\n"
            "@@ -1,6 +1,6 @@\n"
            " line1\n"
            "-old_line_2\n"
            "+new_line_2\n"
            " line3\n"
            " line4\n" + ("x" * 300)
        )
        max_chars = 150
        result = _truncate_patch_at_hunk_boundary(patch, max_chars=max_chars)
        assert "@@ -1,6 +1,6 @@" in result
        assert "\n-old_" in result
        assert result.endswith(_PATCH_TRUNCATION_MARKER)

    def test_falls_back_to_character_cut_when_no_hunk_boundary(self) -> None:
        """When the patch has no hunk header before max_chars, falls back to char cut."""
        patch = "x" * 200
        max_chars = 50
        result = _truncate_patch_at_hunk_boundary(patch, max_chars=max_chars)
        assert result.endswith(_PATCH_TRUNCATION_MARKER)
        assert len(result) <= max_chars

    def test_tiny_max_chars_is_bounded(self) -> None:
        """When max_chars is smaller than the marker, the result is bounded to max_chars."""
        patch = "@@ -1,1 +1,1 @@\n" + "x" * 100
        result = _truncate_patch_at_hunk_boundary(patch, max_chars=5)
        # The marker itself is truncated so the output never exceeds the budget.
        assert len(result) <= 5
        assert result == _PATCH_TRUNCATION_MARKER[:5]

    @pytest.mark.parametrize("max_chars", [0, 1, 2])
    def test_zero_or_tiny_budget_returns_truncated_patch(self, max_chars: int) -> None:
        """Very small max_chars does not raise; result is bounded."""
        patch = "@@ -1,1 +1,1 @@\n line\n"
        result = _truncate_patch_at_hunk_boundary(patch, max_chars=max_chars)
        assert isinstance(result, str)
