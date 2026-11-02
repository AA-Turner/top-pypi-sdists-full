"""Tests for the ``CustomizationQualityResult`` dataclass."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import CustomizationQualityResult, Violation


class TestCustomizationQualityResult:
    def test_defaults_to_an_empty_valid_result(self) -> None:
        """A freshly built result has no files, no violations, and is valid."""
        result = CustomizationQualityResult()

        assert result.checked_files == []
        assert result.corpus_files == []
        assert result.violations == []
        assert result.is_valid is True

    def test_is_invalid_when_a_violation_is_present(self) -> None:
        """Any violation makes the result invalid."""
        result = CustomizationQualityResult(
            checked_files=["a.md"],
            corpus_files=["a.md", "b.md"],
            violations=[Violation("Q1", "a.md", "missing description")],
        )

        assert result.is_valid is False
