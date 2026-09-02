"""Tests for validate_template_content (FR-005 template-content guards)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError
from agentic_devtools.cli.issue_template.mapping_validation import validate_template_content


class TestValidateTemplateContent:
    """Template-content rejection guards (Scenario 8a–8d)."""

    def test_same_line_duplicate_body_mapped_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match=r"url.*line 3"):
            validate_template_content("## Links\n\n{{url}} and {{url}}\n", {"url": "body:Links"})

    def test_same_line_duplicate_unmapped_ok(self) -> None:
        # url is not remapped -> ordinary substitution -> allowed.
        validate_template_content("## Links\n\n{{url}} and {{url}}\n", {"created_at": "omit"})

    def test_mixed_placeholder_line_removed_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="created_at.*updated_at.*line"):
            validate_template_content(
                "## Provenance\n\n| C/U | {{created_at}} / {{updated_at}} |\n",
                {"created_at": "body:Timeline"},
            )

    def test_mixed_placeholder_frontmatter_target_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="share line"):
            validate_template_content(
                "text {{url}} and {{created_at}}\n",
                {"url": "frontmatter"},
            )

    def test_retained_custom_section_may_share_line_with_unmapped_placeholder(self) -> None:
        validate_template_content(
            "## Links\n\n{{url}} ({{title}})\n",
            {"url": "body:Links"},
        )

    def test_duplicate_section_headings_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="Duplicate section"):
            validate_template_content(
                "## Provenance\n\na\n\n## Provenance\n\nb\n",
                {"created_at": "body:Provenance"},
            )

    def test_canonical_placeholder_in_header_row_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="header or delimiter row"):
            validate_template_content(
                "## Provenance\n\n| {{created_at}} | Value |\n| --- | --- |\n| Created | x |\n",
                {"created_at": "body:Provenance"},
            )

    def test_canonical_placeholder_in_delimiter_row_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="delimiter"):
            validate_template_content(
                "## Provenance\n\n| Property | Value |\n| --- | {{created_at}} |\n| Created | x |\n",
                {"created_at": "body:Provenance"},
            )

    def test_canonical_placeholder_in_selected_data_row_with_delimiter_label_is_allowed(self) -> None:
        validate_template_content(
            "## Metadata\n\n| Property | Value |\n| --- | --- |\n| --- | {{created_at}} |\n",
            {"created_at": "body:Metadata"},
        )

    def test_later_table_header_placeholder_in_canonical_section_is_allowed(self) -> None:
        validate_template_content(
            (
                "## Metadata\n\n"
                "| Property | Value |\n| --- | --- |\n| Created | {{created_at}} |\n\n"
                "| {{created_at}} | Example |\n| --- | --- |\n"
            ),
            {"created_at": "body:Metadata"},
        )

    def test_later_malformed_table_like_sequence_is_ignored_when_compatible_table_exists(self) -> None:
        validate_template_content(
            (
                "## Metadata\n\n"
                "| Property | Value |\n| --- | --- |\n| Created | {{created_at}} |\n\n"
                "| C | D |\n| --- | {{created_at}} |\n"
            ),
            {"created_at": "body:Metadata"},
        )

    def test_lines_without_placeholders_still_skip_fenced_headings(self) -> None:
        validate_template_content(
            "## Links\n\nplain text\n\n```\n## Metadata\nliteral text\n```\n",
            {"url": "body:Links"},
        )

    def test_mixed_placeholder_line_removed_inside_fence_rejected(self) -> None:
        with pytest.raises(TemplateValidationError, match="url.*created_at.*line 6"):
            validate_template_content(
                "## Links\n\nplain text\n\n```\n{{url}} {{created_at}}\n```\n",
                {"url": "omit"},
            )

    def test_clean_template_passes(self) -> None:
        validate_template_content(
            "## Metadata\n\n| Field | Value |\n| --- | --- |\n| Created | {{created_at}} |\n",
            {"created_at": "body:Metadata"},
        )

    def test_custom_section_no_header_check(self) -> None:
        # Non-canonical target: header/delimiter guard does not apply.
        validate_template_content(
            "## Links\n\n| {{url}} | x |\n| --- | --- |\n",
            {"url": "body:Links"},
        )
