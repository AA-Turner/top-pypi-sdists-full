"""Tests for validate_single_template()."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.issue_template.template_placeholders import (
    CANONICAL_PLACEHOLDER_NAMES,
)
from agentic_devtools.cli.issue_template.validate_templates import (
    validate_single_template,
)


class TestValidateSingleTemplate:
    """Tests for single-template validation orchestration."""

    def test_empty_content_reports_w003_only(self) -> None:
        """A whitespace-only template yields exactly one W003 warning."""
        result = validate_single_template(Path("empty.md"), "   \n\t", set(), set())
        assert result.template_path == "empty.md"
        assert [d.code for d in result.diagnostics] == ["W003"]
        assert result.status == "pass"

    def test_valid_template_passes(self) -> None:
        """A valid template referencing known/required names has no diagnostics."""
        result = validate_single_template(
            Path("ok.md"),
            "{{title}} {{description}}",
            set(CANONICAL_PLACEHOLDER_NAMES),
            {"title", "description"},
        )
        assert result.diagnostics == []
        assert result.status == "pass"

    def test_combines_all_check_types(self) -> None:
        """Syntax, unknown, and coverage diagnostics are all aggregated."""
        content = "{{title}} {{oops}} {{bad"
        result = validate_single_template(
            Path("mix.md"),
            content,
            set(CANONICAL_PLACEHOLDER_NAMES),
            {"title", "status"},
        )
        codes = sorted({d.code for d in result.diagnostics})
        assert codes == ["E001", "W001", "W002"]
        assert result.status == "fail"
