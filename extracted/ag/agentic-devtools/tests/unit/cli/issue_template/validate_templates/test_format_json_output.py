"""Tests for format_json_output() (FR-006)."""

from __future__ import annotations

import json

from agentic_devtools.cli.issue_template.validate_templates import (
    TemplateDiagnostic,
    TemplateValidationResult,
    ValidationSummary,
    format_json_output,
)


class TestFormatJsonOutput:
    """Tests for JSON output formatting."""

    def test_valid_json_with_summary(self) -> None:
        """Output is valid JSON containing a summary with counts."""
        summary = ValidationSummary(results=[], command_diagnostics=[])
        parsed = json.loads(format_json_output(summary))
        assert parsed["summary"] == {"errors": 0, "warnings": 0, "templates_checked": 0}
        assert parsed["results"] == []
        assert parsed["diagnostics"] == []

    def test_per_template_diagnostics_serialized(self) -> None:
        """Per-template results serialize path, status, and diagnostic objects."""
        summary = ValidationSummary(
            results=[
                TemplateValidationResult(
                    "a.md",
                    [TemplateDiagnostic("error", "E001", 2, 4, "boom")],
                )
            ],
            command_diagnostics=[],
        )
        parsed = json.loads(format_json_output(summary))
        assert parsed["summary"] == {"errors": 1, "warnings": 0, "templates_checked": 1}
        result = parsed["results"][0]
        assert result["template"] == "a.md"
        assert result["status"] == "fail"
        assert result["diagnostics"][0] == {
            "level": "error",
            "code": "E001",
            "line": 2,
            "column": 4,
            "message": "boom",
        }

    def test_command_diagnostics_serialized(self) -> None:
        """Command-level diagnostics appear in the top-level diagnostics array."""
        summary = ValidationSummary(
            results=[],
            command_diagnostics=[TemplateDiagnostic("error", "E003", None, None, "none")],
        )
        parsed = json.loads(format_json_output(summary))
        assert parsed["diagnostics"][0]["code"] == "E003"
        assert parsed["diagnostics"][0]["line"] is None
