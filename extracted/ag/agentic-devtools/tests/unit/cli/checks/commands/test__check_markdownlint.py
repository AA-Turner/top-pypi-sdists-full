"""Tests for _check_markdownlint."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.checks.commands import _check_markdownlint

MODULE = "agentic_devtools.cli.checks.commands"


class TestCheckMarkdownlint:
    """Tests for _check_markdownlint."""

    @patch(f"{MODULE}.markdownlint_files", return_value=(True, "Summary: 0 error(s)"))
    def test_pass_returns_labelled_result(self, mock_lint, tmp_path):
        result = _check_markdownlint(["README.md"], str(tmp_path))
        assert result.passed is True
        assert result.label == "markdownlint changed files"
        assert "0 error(s)" in result.output
        mock_lint.assert_called_once_with(["README.md"], cwd=str(tmp_path))

    @patch(f"{MODULE}.markdownlint_files", return_value=(False, "README.md:1 MD041"))
    def test_failure_is_reported(self, mock_lint, tmp_path):
        result = _check_markdownlint(["README.md"], str(tmp_path))
        assert result.passed is False
        assert "MD041" in result.output
