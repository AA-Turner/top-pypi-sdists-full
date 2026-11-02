"""Tests for TemplateValidationResult dataclass."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import (
    TemplateDiagnostic,
    TemplateValidationResult,
)


class TestTemplateValidationResult:
    """Tests for the TemplateValidationResult dataclass and its status property."""

    def test_status_pass_when_no_diagnostics(self) -> None:
        """A result with no diagnostics has status 'pass'."""
        result = TemplateValidationResult(template_path="a.md", diagnostics=[])
        assert result.status == "pass"

    def test_status_pass_when_only_warnings(self) -> None:
        """A result with only warning diagnostics still passes."""
        result = TemplateValidationResult(
            template_path="a.md",
            diagnostics=[TemplateDiagnostic("warning", "W001", 1, 1, "w")],
        )
        assert result.status == "pass"

    def test_status_fail_when_error_present(self) -> None:
        """A result with any error diagnostic fails."""
        result = TemplateValidationResult(
            template_path="a.md",
            diagnostics=[
                TemplateDiagnostic("warning", "W001", 1, 1, "w"),
                TemplateDiagnostic("error", "E001", 2, 1, "e"),
            ],
        )
        assert result.status == "fail"

    def test_template_path_stored(self) -> None:
        """The template path is stored verbatim."""
        result = TemplateValidationResult(template_path="/x/y.md", diagnostics=[])
        assert result.template_path == "/x/y.md"
