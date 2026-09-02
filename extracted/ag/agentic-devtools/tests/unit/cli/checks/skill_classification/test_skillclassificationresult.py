"""Tests for SkillClassificationResult dataclass."""

from __future__ import annotations

from agentic_devtools.cli.checks.skill_classification import (
    MismatchEntry,
    ParseErrorEntry,
    ParseWarningEntry,
    SkillClassificationResult,
)


class TestSkillClassificationResult:
    """Tests for is_valid computed property."""

    def test_is_valid_when_all_empty(self) -> None:
        result = SkillClassificationResult(validated_count=5)
        assert result.is_valid

    def test_not_valid_with_unregistered_files(self) -> None:
        result = SkillClassificationResult(unregistered_files=["a.md"])
        assert not result.is_valid

    def test_not_valid_with_mismatches(self) -> None:
        result = SkillClassificationResult(
            mismatches=[MismatchEntry(file="a.md", expected={}, actual={"always": True})]
        )
        assert not result.is_valid

    def test_not_valid_with_orphan_entries(self) -> None:
        result = SkillClassificationResult(orphan_entries=["a.md"])
        assert not result.is_valid

    def test_not_valid_with_parse_warnings(self) -> None:
        result = SkillClassificationResult(parse_warnings=[ParseWarningEntry(file="a.md", message="bad")])
        assert not result.is_valid

    def test_not_valid_with_parse_errors(self) -> None:
        result = SkillClassificationResult(parse_errors=[ParseErrorEntry(file="a.md", error="syntax")])
        assert not result.is_valid
