"""Tests for _remove_excluded_lines in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _remove_excluded_lines


class TestRemoveExcludedLines:
    """Tests for _remove_excluded_lines (FR-010)."""

    def test_single_excluded_placeholder_removed(self) -> None:
        """Line with a single excluded placeholder is removed."""
        lines = ["Title: {{title}}", "Priority: {{priority}}", "Desc: {{description}}"]
        result = _remove_excluded_lines(lines, frozenset({"priority"}))
        assert result == ["Title: {{title}}", "Desc: {{description}}"]

    def test_mixed_literal_and_excluded_removed(self) -> None:
        """Line with literal text + excluded placeholder is fully removed."""
        lines = ["**Priority**: {{priority}}", "Other text"]
        result = _remove_excluded_lines(lines, frozenset({"priority"}))
        assert result == ["Other text"]

    def test_multiple_placeholders_one_excluded(self) -> None:
        """Line with multiple placeholders, one excluded, entire line removed."""
        lines = ["{{title}} - {{priority}}"]
        result = _remove_excluded_lines(lines, frozenset({"priority"}))
        assert result == []

    def test_alias_equivalent_exclusion_id(self) -> None:
        """Excluding 'id' also removes lines with {{issue_id}}."""
        lines = ["ID: {{id}}", "Alias: {{issue_id}}", "Title: {{title}}"]
        result = _remove_excluded_lines(lines, frozenset({"id"}))
        assert result == ["Title: {{title}}"]

    def test_alias_equivalent_exclusion_issue_id(self) -> None:
        """Excluding 'issue_id' also removes lines with {{id}}."""
        lines = ["ID: {{id}}", "Alias: {{issue_id}}", "Title: {{title}}"]
        result = _remove_excluded_lines(lines, frozenset({"issue_id"}))
        assert result == ["Title: {{title}}"]

    def test_no_exclusion_returns_all_lines(self) -> None:
        """Empty excluded set returns all lines unchanged."""
        lines = ["A: {{a}}", "B: {{b}}"]
        result = _remove_excluded_lines(lines, frozenset())
        assert result == ["A: {{a}}", "B: {{b}}"]

    def test_lines_without_placeholders_kept(self) -> None:
        """Lines without any placeholder are always kept."""
        lines = ["Plain text", "Priority: {{priority}}", "More text"]
        result = _remove_excluded_lines(lines, frozenset({"priority"}))
        assert result == ["Plain text", "More text"]
