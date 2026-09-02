"""Tests for TemplateDiagnostic dataclass."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import TemplateDiagnostic


class TestTemplateDiagnostic:
    """Tests for the TemplateDiagnostic frozen dataclass."""

    def test_fields_are_stored(self) -> None:
        """All constructor fields are exposed as attributes."""
        diag = TemplateDiagnostic(
            level="error",
            code="E001",
            line=3,
            column=5,
            message="boom",
        )
        assert diag.level == "error"
        assert diag.code == "E001"
        assert diag.line == 3
        assert diag.column == 5
        assert diag.message == "boom"

    def test_none_location(self) -> None:
        """line and column may be None for location-less diagnostics."""
        diag = TemplateDiagnostic(
            level="warning",
            code="W003",
            line=None,
            column=None,
            message="empty",
        )
        assert diag.line is None
        assert diag.column is None

    def test_equality(self) -> None:
        """Two diagnostics with identical fields compare equal (frozen dataclass)."""
        a = TemplateDiagnostic("warning", "W001", 1, 2, "x")
        b = TemplateDiagnostic("warning", "W001", 1, 2, "x")
        assert a == b
