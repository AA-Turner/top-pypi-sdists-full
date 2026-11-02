"""Tests for format_human_output() (FR-008)."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import (
    TemplateDiagnostic,
    TemplateValidationResult,
    ValidationSummary,
    format_human_output,
)


class TestFormatHumanOutput:
    """Tests for lint-style human-readable formatting."""

    def test_located_diagnostic_line(self) -> None:
        """A diagnostic with a location renders file:line:col."""
        summary = ValidationSummary(
            results=[
                TemplateValidationResult(
                    "a.md",
                    [TemplateDiagnostic("error", "E001", 3, 5, "boom")],
                )
            ],
            command_diagnostics=[],
        )
        output = format_human_output(summary)
        assert "a.md:3:5: error: [E001] boom" in output

    def test_locationless_diagnostic_uses_dashes(self) -> None:
        """A diagnostic without a location renders '-' for line and column."""
        summary = ValidationSummary(
            results=[
                TemplateValidationResult(
                    "a.md",
                    [TemplateDiagnostic("warning", "W002", None, None, "missing")],
                )
            ],
            command_diagnostics=[],
        )
        output = format_human_output(summary)
        assert "a.md:-:-: warning: [W002] missing" in output

    def test_command_diagnostic_uses_dash_file(self) -> None:
        """Command-level diagnostics use '-' for the file label."""
        summary = ValidationSummary(
            results=[],
            command_diagnostics=[TemplateDiagnostic("error", "E003", None, None, "none found")],
        )
        output = format_human_output(summary)
        assert "-:-:-: error: [E003] none found" in output

    def test_summary_line_present(self) -> None:
        """The final line summarizes checked templates and counts."""
        summary = ValidationSummary(
            results=[
                TemplateValidationResult(
                    "a.md",
                    [TemplateDiagnostic("warning", "W001", 1, 1, "w")],
                )
            ],
            command_diagnostics=[],
        )
        output = format_human_output(summary)
        assert output.splitlines()[-1] == "Checked 1 template(s): 0 error(s), 1 warning(s)"
