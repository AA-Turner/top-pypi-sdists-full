"""Tests for _check_customization_quality."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.checks.commands import _check_customization_quality
from agentic_devtools.cli.checks.customization_quality import (
    CustomizationQualityResult,
    Violation,
)

QUALITY_MOD = "agentic_devtools.cli.checks.customization_quality"


class TestCheckCustomizationQualitySkip:
    """No selected customization file changed → graceful skip (pass)."""

    def test_no_changed_files_returns_pass(self, tmp_path):
        result = _check_customization_quality([], tmp_path)
        assert result.passed is True
        assert "skipped" in result.output

    def test_unselected_changed_files_returns_pass(self, tmp_path):
        result = _check_customization_quality(["README.md", ".github/prompts/agdt.x.prompt.md"], tmp_path)
        assert result.passed is True
        assert "skipped" in result.output


class TestCheckCustomizationQualityPass:
    """Validation passes when the changed files carry no violation."""

    @patch(f"{QUALITY_MOD}.check_customization_quality")
    def test_valid_returns_ok(self, mock_validate, tmp_path):
        mock_validate.return_value = CustomizationQualityResult(
            checked_files=[".github/instructions/python.instructions.md"],
        )
        result = _check_customization_quality([".github/instructions/python.instructions.md"], tmp_path)
        assert result.passed is True
        assert "1 customization file(s) validated" in result.output
        mock_validate.assert_called_once_with(tmp_path, [".github/instructions/python.instructions.md"])


class TestCheckCustomizationQualityUnreadable:
    """Unreadable or unresolvable inputs fail without crashing the pool."""

    @patch(f"{QUALITY_MOD}.check_customization_quality", side_effect=PermissionError("permission denied"))
    def test_os_error_returns_failure(self, mock_validate, tmp_path):
        result = _check_customization_quality([".github/instructions/python.instructions.md"], tmp_path)
        assert result.passed is False
        assert "Unreadable customization file" in result.output

    @patch(f"{QUALITY_MOD}.check_customization_quality", side_effect=ValueError("outside the selection"))
    def test_value_error_returns_failure(self, mock_validate, tmp_path):
        result = _check_customization_quality([".github/instructions/python.instructions.md"], tmp_path)
        assert result.passed is False
        assert "Unreadable customization file" in result.output


class TestCheckCustomizationQualityViolations:
    """Violations are formatted one per line with a trailing count."""

    @patch(f"{QUALITY_MOD}.check_customization_quality")
    def test_violations_are_reported(self, mock_validate, tmp_path):
        mock_validate.return_value = CustomizationQualityResult(
            checked_files=[".agents/skills/demo/SKILL.md"],
            violations=[
                Violation(rule="Q2", path=".agents/skills/demo/SKILL.md", message="name is not a legal slug"),
                Violation(rule="Q9", path=".agents/skills/demo/SKILL.md", message="3 emphatic directives"),
            ],
        )
        result = _check_customization_quality([".agents/skills/demo/SKILL.md"], tmp_path)
        assert result.passed is False
        assert "  Q2: .agents/skills/demo/SKILL.md: name is not a legal slug" in result.output
        assert "  Q9: .agents/skills/demo/SKILL.md: 3 emphatic directives" in result.output
        assert "FAIL: 2 violation(s)" in result.output


class TestCheckCustomizationQualityEndToEnd:
    """The step runs the real quality module against a real repository tree."""

    def test_real_violation_is_surfaced(self, tmp_path):
        skill = tmp_path / ".agents" / "skills" / "Bad_Name" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text(
            "---\nname: Bad_Name\ndescription: Use when demonstrating the check behaviour end to end.\n---\n\nBody.\n",
            encoding="utf-8",
        )
        result = _check_customization_quality([".agents/skills/Bad_Name/SKILL.md"], tmp_path)
        assert result.passed is False
        assert "Q2" in result.output
