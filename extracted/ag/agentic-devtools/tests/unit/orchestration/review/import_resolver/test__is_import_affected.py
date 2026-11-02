"""Tests for _is_import_affected function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.import_resolver import _is_import_affected


class TestIsImportAffected:
    """Tests for _is_import_affected helper."""

    def test_import_line_in_diff_detected(self) -> None:
        """Import on a diff line is detected as affected."""
        info = {"module": "agentic_devtools.state", "names": ["get_value"], "line": 5}
        assert _is_import_affected(info, [5], "line1\nline2\nline3\nline4\nfrom x import y\n") is True

    def test_no_source_code_with_diff_lines(self) -> None:
        """Empty source_code with diff_lines returns False."""
        info = {"module": "agentic_devtools.state", "names": ["get_value"], "line": 10}
        assert _is_import_affected(info, [3], "") is False

    def test_diff_line_out_of_range(self) -> None:
        """Diff line beyond file length doesn't crash."""
        info = {"module": "agentic_devtools.state", "names": ["get_value"], "line": 10}
        assert _is_import_affected(info, [999], "one line\n") is False

    def test_none_diff_lines_includes_all_imports(self) -> None:
        """diff_lines=None means all imports are considered affected."""
        info = {"module": "agentic_devtools.state", "names": ["get_value"], "line": 5}
        assert _is_import_affected(info, None, "") is True

    def test_symbol_referenced_in_diff_line_detected(self) -> None:
        """Import is affected when its symbol is referenced in a diff line."""
        info = {"module": "agentic_devtools.state", "names": ["get_value"], "line": 1}
        source = "from agentic_devtools.state import get_value\nx = get_value()\n"
        # Line 2 is in the diff and references get_value
        assert _is_import_affected(info, [2], source) is True

    def test_symbol_not_in_diff_line_not_detected(self) -> None:
        """Import is not affected when its symbol is absent from diff lines."""
        info = {"module": "agentic_devtools.state", "names": ["get_value"], "line": 1}
        source = "from agentic_devtools.state import get_value\ny = other_func()\n"
        # Line 2 does not reference get_value
        assert _is_import_affected(info, [2], source) is False
