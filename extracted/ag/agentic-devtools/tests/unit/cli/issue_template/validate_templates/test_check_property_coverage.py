"""Tests for check_property_coverage() (FR-003, W002)."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.validate_templates import (
    check_property_coverage,
)


class TestCheckPropertyCoverage:
    """Tests for W002 required-property coverage detection."""

    def test_all_required_covered(self) -> None:
        """No diagnostic when every required property has a placeholder."""
        content = "{{title}} {{description}}"
        assert check_property_coverage(content, {"title", "description"}, "x.md") == []

    def test_missing_required_property(self) -> None:
        """A required property with no placeholder is reported as W002."""
        diags = check_property_coverage("{{title}}", {"title", "status"}, "x.md")
        assert len(diags) == 1
        assert diags[0].code == "W002"
        assert diags[0].level == "warning"
        assert diags[0].line is None
        assert diags[0].column is None
        assert "status" in diags[0].message
        assert "x.md" in diags[0].message

    def test_alias_placeholder_covers_canonical(self) -> None:
        """An alias placeholder (issue_id) covers the canonical property (id)."""
        assert check_property_coverage("{{issue_id}}", {"id"}, "x.md") == []

    def test_alias_required_covered_by_canonical(self) -> None:
        """A required alias name is covered by its canonical placeholder."""
        assert check_property_coverage("{{id}}", {"issue_id"}, "x.md") == []

    def test_multiple_missing_sorted(self) -> None:
        """Multiple missing properties are reported in sorted order."""
        diags = check_property_coverage("", {"status", "description"}, "x.md")
        assert [d.message.split("'")[1] for d in diags] == ["description", "status"]

    def test_empty_required_set(self) -> None:
        """No required properties produces no diagnostics."""
        assert check_property_coverage("{{title}}", set(), "x.md") == []
