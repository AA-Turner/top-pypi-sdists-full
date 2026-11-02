"""Tests for ValidationSummary dataclass."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import (
    TemplateDiagnostic,
    TemplateValidationResult,
    ValidationSummary,
)


class TestValidationSummary:
    """Tests for the ValidationSummary aggregate dataclass."""

    def test_empty_summary_counts(self) -> None:
        """An empty summary reports zero checked/errors/warnings."""
        summary = ValidationSummary(results=[], command_diagnostics=[])
        assert summary.templates_checked == 0
        assert summary.error_count == 0
        assert summary.warning_count == 0

    def test_templates_checked_counts_results(self) -> None:
        """templates_checked equals the number of results."""
        summary = ValidationSummary(
            results=[
                TemplateValidationResult("a.md", []),
                TemplateValidationResult("b.md", []),
            ],
            command_diagnostics=[],
        )
        assert summary.templates_checked == 2

    def test_error_and_warning_counts_across_results_and_command(self) -> None:
        """Counts include both per-template and command-level diagnostics."""
        summary = ValidationSummary(
            results=[
                TemplateValidationResult(
                    "a.md",
                    [
                        TemplateDiagnostic("error", "E001", 1, 1, "e1"),
                        TemplateDiagnostic("warning", "W001", 2, 1, "w1"),
                    ],
                ),
                TemplateValidationResult(
                    "b.md",
                    [TemplateDiagnostic("warning", "W002", None, None, "w2")],
                ),
            ],
            command_diagnostics=[TemplateDiagnostic("error", "E003", None, None, "e3")],
        )
        assert summary.error_count == 2
        assert summary.warning_count == 2
