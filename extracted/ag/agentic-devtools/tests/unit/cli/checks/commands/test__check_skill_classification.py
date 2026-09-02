"""Tests for _check_skill_classification."""

from __future__ import annotations

import json
from unittest.mock import patch

from agentic_devtools.cli.checks.commands import _check_skill_classification
from agentic_devtools.cli.checks.skill_classification import (
    MismatchEntry,
    ParseErrorEntry,
    ParseWarningEntry,
    SkillClassificationResult,
)

MODULE = "agentic_devtools.cli.checks.commands"
SKILL_MOD = "agentic_devtools.cli.checks.skill_classification"


class TestCheckSkillClassificationSkip:
    """Fixture missing → graceful skip (pass)."""

    def test_missing_fixture_returns_pass(self, tmp_path):
        result = _check_skill_classification(tmp_path)
        assert result.passed is True
        assert "skipped" in result.output


class TestCheckSkillClassificationPass:
    """Validation passes when all files are registered."""

    @patch(f"{SKILL_MOD}.validate_skill_classification")
    def test_valid_returns_ok(self, mock_validate, tmp_path):
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        mock_validate.return_value = SkillClassificationResult(validated_count=5)
        result = _check_skill_classification(tmp_path)
        assert result.passed is True
        assert "5 skill file(s) validated" in result.output


class TestCheckSkillClassificationMalformedFixture:
    """Malformed fixture JSON → failure."""

    @patch(
        f"{SKILL_MOD}.validate_skill_classification",
        side_effect=json.JSONDecodeError("bad", "", 0),
    )
    def test_json_error(self, mock_validate, tmp_path):
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        result = _check_skill_classification(tmp_path)
        assert result.passed is False
        assert "Malformed fixture" in result.output

    @patch(f"{SKILL_MOD}.validate_skill_classification", side_effect=ValueError("bad value"))
    def test_value_error(self, mock_validate, tmp_path):
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        result = _check_skill_classification(tmp_path)
        assert result.passed is False
        assert "Malformed fixture" in result.output

    @patch(
        f"{SKILL_MOD}.validate_skill_classification",
        side_effect=PermissionError("permission denied"),
    )
    def test_os_error_returns_failure_does_not_crash(self, mock_validate, tmp_path):
        """OSError (e.g. PermissionError, IsADirectoryError) must not crash the parallel run."""
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        result = _check_skill_classification(tmp_path)
        assert result.passed is False
        assert "Malformed fixture" in result.output


class TestCheckSkillClassificationViolations:
    """Various violation types are formatted."""

    @patch(f"{SKILL_MOD}.validate_skill_classification")
    def test_unregistered_files(self, mock_validate, tmp_path):
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        mock_validate.return_value = SkillClassificationResult(
            unregistered_files=[".github/agents/agdt.new.agent.md"],
        )
        result = _check_skill_classification(tmp_path)
        assert result.passed is False
        assert "unregistered: .github/agents/agdt.new.agent.md" in result.output
        assert "1 violation(s)" in result.output

    @patch(f"{SKILL_MOD}.validate_skill_classification")
    def test_mismatches(self, mock_validate, tmp_path):
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        mock_validate.return_value = SkillClassificationResult(
            mismatches=[MismatchEntry(file="f.md", expected={"a": 1}, actual={"b": 2})],
        )
        result = _check_skill_classification(tmp_path)
        assert result.passed is False
        assert "mismatch: f.md" in result.output

    @patch(f"{SKILL_MOD}.validate_skill_classification")
    def test_orphan_entries(self, mock_validate, tmp_path):
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        mock_validate.return_value = SkillClassificationResult(
            orphan_entries=["gone.md"],
        )
        result = _check_skill_classification(tmp_path)
        assert result.passed is False
        assert "orphan: gone.md" in result.output

    @patch(f"{SKILL_MOD}.validate_skill_classification")
    def test_parse_warnings(self, mock_validate, tmp_path):
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        mock_validate.return_value = SkillClassificationResult(
            parse_warnings=[ParseWarningEntry(file="w.md", message="bad axis")],
        )
        result = _check_skill_classification(tmp_path)
        assert result.passed is False
        assert "warning: w.md: bad axis" in result.output

    @patch(f"{SKILL_MOD}.validate_skill_classification")
    def test_parse_errors(self, mock_validate, tmp_path):
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        mock_validate.return_value = SkillClassificationResult(
            parse_errors=[ParseErrorEntry(file="e.md", error="yaml kaboom")],
        )
        result = _check_skill_classification(tmp_path)
        assert result.passed is False
        assert "error: e.md: yaml kaboom" in result.output

    @patch(f"{SKILL_MOD}.validate_skill_classification")
    def test_combined_violations_count(self, mock_validate, tmp_path):
        fixture = tmp_path / "tests" / "fixtures" / "skill_classification_expected.json"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}")
        mock_validate.return_value = SkillClassificationResult(
            unregistered_files=["a.md"],
            mismatches=[MismatchEntry(file="b.md", expected={}, actual={"x": 1})],
            orphan_entries=["c.md"],
            parse_warnings=[ParseWarningEntry(file="d.md", message="w")],
            parse_errors=[ParseErrorEntry(file="e.md", error="e")],
        )
        result = _check_skill_classification(tmp_path)
        assert result.passed is False
        assert "5 violation(s)" in result.output
