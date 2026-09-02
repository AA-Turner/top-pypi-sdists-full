"""Tests for _determine_exit_code()."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import (
    TemplateDiagnostic,
    TemplateValidationResult,
    ValidationSummary,
    _determine_exit_code,
)


def _summary(errors: int, warnings: int) -> ValidationSummary:
    diagnostics = [TemplateDiagnostic("error", "E001", 1, 1, "e") for _ in range(errors)]
    diagnostics += [TemplateDiagnostic("warning", "W001", 1, 1, "w") for _ in range(warnings)]
    return ValidationSummary(
        results=[TemplateValidationResult("a.md", diagnostics)],
        command_diagnostics=[],
    )


class TestDetermineExitCode:
    """Tests for exit-code derivation (FR-005)."""

    def test_errors_return_one(self) -> None:
        """Any error yields exit code 1 regardless of strict."""
        assert _determine_exit_code(_summary(1, 0), strict=False) == 1

    def test_warnings_only_return_zero(self) -> None:
        """Warnings alone yield exit code 0 without strict."""
        assert _determine_exit_code(_summary(0, 2), strict=False) == 0

    def test_strict_promotes_warnings(self) -> None:
        """Warnings yield exit code 1 under strict mode."""
        assert _determine_exit_code(_summary(0, 1), strict=True) == 1

    def test_clean_returns_zero(self) -> None:
        """No diagnostics yields exit code 0 even under strict."""
        assert _determine_exit_code(_summary(0, 0), strict=True) == 0
