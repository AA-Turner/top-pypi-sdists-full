"""Tests for sanitize_suggestion (FR-014, SC-007)."""

from agentic_devtools.orchestration.review.suggestion_syntax import sanitize_suggestion

FILE = "def f():\n    x = 1\n    return x\n"


class TestSanitizeSuggestion:
    def test_valid_python_kept(self):
        assert (
            sanitize_suggestion(
                file_path="a.py",
                file_content=FILE,
                diff_side="new",
                start_line=2,
                end_line=2,
                replacement_code="    x = 2",
            )
            == "    x = 2"
        )

    def test_absent_replacement_returns_none(self):
        assert (
            sanitize_suggestion(
                file_path="a.py",
                file_content=FILE,
                diff_side="new",
                start_line=2,
                end_line=2,
                replacement_code=None,
            )
            is None
        )

    def test_empty_replacement_deletion_kept(self):
        # Empty string is a deletion suggestion; it's kept when the resulting file
        # still has valid syntax (splicing zero lines removes the targeted lines).
        assert (
            sanitize_suggestion(
                file_path="a.py",
                file_content=FILE,
                diff_side="new",
                start_line=2,
                end_line=2,
                replacement_code="",
            )
            == ""
        )

    def test_old_side_dropped(self):
        assert (
            sanitize_suggestion(
                file_path="a.py",
                file_content=FILE,
                diff_side="old",
                start_line=2,
                end_line=2,
                replacement_code="    x = 2",
            )
            is None
        )

    def test_unknown_diff_side_dropped(self):
        assert (
            sanitize_suggestion(
                file_path="a.py",
                file_content=FILE,
                diff_side="deleted",
                start_line=2,
                end_line=2,
                replacement_code="    x = 2",
            )
            is None
        )

    def test_unsupported_language_dropped(self):
        assert (
            sanitize_suggestion(
                file_path="a.ts",
                file_content="const x = 1;",
                diff_side="new",
                start_line=1,
                end_line=1,
                replacement_code="const x = 2;",
            )
            is None
        )

    def test_invalid_syntax_dropped(self):
        assert (
            sanitize_suggestion(
                file_path="a.py",
                file_content=FILE,
                diff_side="new",
                start_line=2,
                end_line=2,
                replacement_code="    x = (",
            )
            is None
        )
