"""Tests for agentic_devtools.cli.issue_template.renderer.render_issue."""

from __future__ import annotations

import pytest
import yaml

from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError
from agentic_devtools.cli.issue_template.renderer import PropertyConfig, render_issue


def _make_issue(**kwargs: object) -> NormalizedIssue:
    """Create a NormalizedIssue with sensible defaults."""
    defaults: dict[str, object] = {
        "issue_id": "PROJECT-42",
        "title": "Add webhook support",
        "url": "https://example.com/issues/42",
        "provider": "jira",
        "description": "Implement webhook handler for notifications.",
        "status": "open",
        "labels": ["feature", "backend"],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
        "raw": {},
    }
    defaults.update(kwargs)
    return NormalizedIssue(**defaults)  # type: ignore[arg-type]


_RENDERED_AT = "2024-06-15T12:00:00+00:00"


def _frontmatter(result: str) -> dict:
    """Parse the YAML frontmatter from a rendered issue."""
    return yaml.safe_load(result.split("---\n")[1])


class TestRenderIssue:
    """Tests for the render_issue function."""

    def test_happy_path_story_template(self) -> None:
        """US-1/AS1: Story template renders with correct frontmatter and body."""
        issue = _make_issue(labels=["story", "backend"])
        template = "## Description\n\n{{description}}\n\n## Acceptance Criteria\n\n{{acceptance_criteria}}"
        result = render_issue(issue, "story", template, _RENDERED_AT)

        # Parse frontmatter
        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])

        assert frontmatter["id"] == "PROJECT-42"
        assert frontmatter["title"] == "Add webhook support"
        assert frontmatter["type"] == "story"
        assert frontmatter["status"] == "open"
        assert frontmatter["provider"] == "jira"
        assert frontmatter["labels"] == ["story", "backend"]
        assert frontmatter["rendered_at"] == _RENDERED_AT

    def test_happy_path_bug_template(self) -> None:
        """US-1/AS2: Bug template includes bug-specific sections."""
        issue = _make_issue(
            raw={
                "severity": "Critical",
                "reproduction_steps": "1. Click button\n2. See error",
                "expected_behavior": "Should work",
                "actual_behavior": "Crashes",
            },
        )
        template = (
            "## Description\n\n{{description}}\n\n"
            "## Reproduction Steps\n\n{{reproduction_steps}}\n\n"
            "## Expected Behavior\n\n{{expected_behavior}}\n\n"
            "## Actual Behavior\n\n{{actual_behavior}}\n\n"
            "## Severity\n\n{{severity}}"
        )
        result = render_issue(issue, "bug", template, _RENDERED_AT)

        assert "Reproduction Steps" in result
        assert "1. Click button\n2. See error" in result
        assert "Should work" in result
        assert "Crashes" in result
        assert "Critical" in result

    def test_default_fallback_template(self) -> None:
        """US-1/AS3: Default template renders when type is unrecognized."""
        issue = _make_issue()
        template = "## Description\n\n{{description}}\n\n## Details\n\n- **Status**: {{status}}"
        result = render_issue(issue, "unknown-type", template, _RENDERED_AT)

        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["type"] == "unknown-type"
        assert "Implement webhook handler" in result

    def test_labels_as_yaml_list(self) -> None:
        """Labels are rendered as a native YAML list."""
        issue = _make_issue(labels=["bug", "priority-high"])
        result = render_issue(issue, "bug", "{{description}}", _RENDERED_AT)

        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["labels"] == ["bug", "priority-high"]
        assert isinstance(frontmatter["labels"], list)

    def test_empty_labels_as_empty_list(self) -> None:
        """Empty labels render as YAML empty list []."""
        issue = _make_issue(labels=[])
        result = render_issue(issue, "task", "{{description}}", _RENDERED_AT)

        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["labels"] == []

    def test_placeholder_substitution_canonical_fields(self) -> None:
        """Canonical NormalizedIssue fields are substituted."""
        issue = _make_issue()
        template = "ID: {{id}}, Title: {{title}}, Status: {{status}}, URL: {{url}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "ID: PROJECT-42" in body
        assert "Title: Add webhook support" in body
        assert "Status: open" in body
        assert "URL: https://example.com/issues/42" in body

    def test_issue_id_alias(self) -> None:
        """{{issue_id}} is an alias for issue.issue_id."""
        issue = _make_issue()
        template = "Issue ID: {{issue_id}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Issue ID: PROJECT-42" in body

    def test_type_placeholder_resolves_to_type_slug(self) -> None:
        """{{type}} in template body resolves to the type_slug argument."""
        issue = _make_issue()
        template = "Type: {{type}}"
        result = render_issue(issue, "story", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Type: story" in body

    def test_unresolved_placeholder_becomes_empty(self) -> None:
        """Unresolved placeholders render as empty strings."""
        issue = _make_issue()
        template = "Value: {{nonexistent_field}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Value: " in body
        assert "{{nonexistent_field}}" not in body

    def test_markdown_injection_verbatim(self) -> None:
        """Markdown in description is injected verbatim (no escaping)."""
        issue = _make_issue(description="# Heading\n\n- bullet\n- **bold**")
        template = "{{description}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "# Heading" in body
        assert "- bullet" in body
        assert "- **bold**" in body

    def test_determinism(self) -> None:
        """Same inputs produce same output (deterministic)."""
        issue = _make_issue()
        template = "{{description}}"
        r1 = render_issue(issue, "task", template, _RENDERED_AT)
        r2 = render_issue(issue, "task", template, _RENDERED_AT)
        assert r1 == r2

    def test_list_coercion_in_body(self) -> None:
        """List values in placeholders are joined with comma-space."""
        issue = _make_issue()
        template = "Labels: {{labels}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Labels: feature, backend" in body

    def test_none_coercion_in_body(self) -> None:
        """None values from raw dict render as empty string."""
        issue = _make_issue(raw={"optional_field": None})
        template = "Value: {{optional_field}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Value: " in body

    def test_no_provider_specific_branches(self) -> None:
        """Renderer has zero provider-specific conditional branches."""
        import inspect

        from agentic_devtools.cli.issue_template import renderer

        source = inspect.getsource(renderer)
        assert 'provider == "jira"' not in source
        assert 'provider == "github"' not in source
        assert 'provider == "markdown"' not in source

    # --- Provider-specific rendering tests (FR-007) ---

    def test_github_provider_rendering(self) -> None:
        """GitHub provider issue renders through same path."""
        issue = _make_issue(
            provider="github",
            raw={"milestone": "v2.0", "number": 42},
        )
        template = "{{description}}\n\nMilestone: {{milestone}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["provider"] == "github"
        assert "Milestone: v2.0" in result

    def test_jira_provider_rendering(self) -> None:
        """Jira provider issue renders through same path."""
        issue = _make_issue(
            provider="jira",
            raw={"priority": "High", "issue_type": "Story"},
        )
        template = "{{description}}\n\nPriority: {{priority}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["provider"] == "jira"
        assert "Priority: High" in result

    def test_markdown_provider_rendering(self) -> None:
        """Markdown provider with empty raw dict produces valid output."""
        issue = _make_issue(provider="markdown", raw={})
        template = "{{description}}\n\nPriority: {{priority}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["provider"] == "markdown"
        assert "Priority: " in result

    # --- Provider-specific property mapping tests (Phase 4) ---

    def test_raw_dict_priority_from_jira(self) -> None:
        """{{priority}} resolves from Jira raw dict."""
        issue = _make_issue(raw={"priority": "High"})
        template = "Priority: {{priority}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Priority: High" in body

    def test_raw_dict_milestone_from_github(self) -> None:
        """{{milestone}} resolves from GitHub raw dict."""
        issue = _make_issue(provider="github", raw={"milestone": "v3.0"})
        template = "Milestone: {{milestone}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Milestone: v3.0" in body

    def test_missing_raw_key_becomes_empty(self) -> None:
        """Missing raw dict key renders as empty string."""
        issue = _make_issue(raw={})
        template = "Priority: {{priority}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Priority: " in body


class TestRenderIssueMapping:
    """render_issue honours property_section_mapping targets."""

    def test_no_mapping_is_noop(self) -> None:
        issue = _make_issue()
        template = "## Description\n\n{{description}}\n"
        baseline = render_issue(issue, "story", template, _RENDERED_AT)
        with_empty = render_issue(issue, "story", template, _RENDERED_AT, PropertyConfig())
        assert baseline == with_empty

    def test_omit_removes_property(self) -> None:
        issue = _make_issue()
        template = "## Meta\n\n- Created: {{created_at}}\n"
        cfg = PropertyConfig(property_section_mapping={"created_at": "omit"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "{{created_at}}" not in result
        assert "2024-01-01" not in result
        assert "created_at" not in _frontmatter(result)

    def test_omit_removes_description_from_all_output(self) -> None:
        issue = _make_issue()
        template = "## Description\n\n{{description}}\n"
        cfg = PropertyConfig(property_section_mapping={"description": "omit"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "{{description}}" not in result
        assert "Implement webhook handler for notifications." not in result

    def test_frontmatter_routes_to_yaml(self) -> None:
        issue = _make_issue()
        template = "## Links\n\n{{url}}\n"
        cfg = PropertyConfig(property_section_mapping={"url": "frontmatter"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        fm = _frontmatter(result)
        assert fm["url"] == "https://example.com/issues/42"
        assert "https://example.com/issues/42" not in result.split("---\n")[2]

    def test_title_frontmatter_suppresses_body_placeholder(self) -> None:
        issue = _make_issue()
        template = "## Summary\n\n{{title}}\n"
        cfg = PropertyConfig(property_section_mapping={"title": "frontmatter"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert _frontmatter(result)["title"] == "Add webhook support"
        body = result.split("---\n")[2]
        assert "{{title}}" not in body
        assert "Add webhook support" not in body
        assert "| Title |" not in body

    def test_body_retains_existing_placeholder(self) -> None:
        issue = _make_issue()
        template = "## Links\n\n- URL: {{url}}\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Links"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert result.count("https://example.com/issues/42") == 1
        assert "- URL: https://example.com/issues/42" in result

    def test_body_appends_to_custom_section_with_content(self) -> None:
        issue = _make_issue()
        template = "## Links\n\nSome intro text.\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Links"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "Some intro text." in result
        assert "- URL: https://example.com/issues/42" in result

    def test_body_appends_to_heading_only_section(self) -> None:
        issue = _make_issue()
        template = "## Links\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Links"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "## Links" in result
        assert "- URL: https://example.com/issues/42" in result

    def test_free_text_and_labelled_in_same_custom_section(self) -> None:
        issue = _make_issue()
        template = "## Overview\n\nExisting.\n"
        cfg = PropertyConfig(property_section_mapping={"description": "body:Overview", "url": "body:Overview"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "Implement webhook handler for notifications." in result
        assert "- URL: https://example.com/issues/42" in result

    def test_synthesized_custom_section(self) -> None:
        issue = _make_issue()
        template = "## Description\n\n{{description}}\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:References", "updated_at": "body:References"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "## References" in result
        assert "- URL: https://example.com/issues/42" in result
        assert "- Updated: 2024-01-02T00:00:00Z" in result

    def test_synthesized_section_does_not_keep_orphaned_template_heading(self) -> None:
        """Synthetic mapped sections must not affect orphan cleanup of template headings."""
        issue = _make_issue()
        template = "# Empty\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Links"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "# Empty" not in body
        assert "## Links" in body
        assert "- URL: https://example.com/issues/42" in body

    def test_synthesized_custom_section_free_text_first(self) -> None:
        issue = _make_issue()
        template = "## Meta\n\n- x\n"
        cfg = PropertyConfig(property_section_mapping={"description": "body:Notes", "url": "body:Notes"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        notes = result.split("## Notes", 1)[1]
        assert notes.index("Implement webhook") < notes.index("- URL:")

    def test_synthesized_canonical_section_is_table(self) -> None:
        issue = _make_issue()
        template = "## Description\n\n{{description}}\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata", "created_at": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "## Metadata" in result
        assert "| Property | Value |" in result
        assert "| --- | --- |" in result
        assert "| URL | https://example.com/issues/42 |" in result
        assert "| Created | 2024-01-01T00:00:00Z |" in result

    def test_canonical_section_retains_existing_rows(self) -> None:
        issue = _make_issue()
        template = (
            "## Metadata\n\n"
            "| Property | Value |\n| --- | --- |\n"
            "| Created | {{created_at}} |\n"
            "| Updated | {{updated_at}} |\n"
        )
        cfg = PropertyConfig(property_section_mapping={"created_at": "body:Metadata", "updated_at": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert result.count("2024-01-01T00:00:00Z") == 1
        assert result.count("2024-01-02T00:00:00Z") == 1
        assert "| Created | 2024-01-01T00:00:00Z |" in result

    def test_canonical_section_injects_new_row(self) -> None:
        issue = _make_issue()
        template = "## Metadata\n\n| Property | Value |\n| --- | --- |\n| Created | {{created_at}} |\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata", "created_at": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| URL | https://example.com/issues/42 |" in result
        assert "| Created | 2024-01-01T00:00:00Z |" in result

    def test_canonical_section_without_table_injects_table(self) -> None:
        issue = _make_issue()
        template = "## Metadata\n\nsome prose\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| Property | Value |" in result
        assert "| URL | https://example.com/issues/42 |" in result

    def test_existing_properties_section_without_placeholder_gets_row(self) -> None:
        issue = _make_issue()
        template = "## Properties\n\n| Property | Value |\n| --- | --- |\n| Existing | value |\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Properties"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| Existing | value |" in result
        assert "| URL | https://example.com/issues/42 |" in result

    def test_existing_provenance_section_without_placeholder_gets_row(self) -> None:
        issue = _make_issue()
        template = "## Provenance\n\n| Property | Value |\n| --- | --- |\n| Existing | value |\n"
        cfg = PropertyConfig(property_section_mapping={"created_at": "body:Provenance"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| Existing | value |" in result
        assert "| Created | 2024-01-01T00:00:00Z |" in result

    def test_table_cell_encoding(self) -> None:
        issue = _make_issue(description="Line A\nHas | pipe and \\ backslash")
        template = "## Description\n\n{{description}}\n"
        cfg = PropertyConfig(property_section_mapping={"description": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "Line A<br>Has \\| pipe and \\\\ backslash" in result

    def test_unmapped_custom_table_row_keeps_plain_substitution(self) -> None:
        issue = _make_issue(description="Line A\nHas | pipe and \\ backslash")
        template = (
            "## Details\n\n| Field | Value |\n| --- | --- |\n| Description | {{description}} |\n\n## Links\n\n{{url}}\n"
        )
        cfg = PropertyConfig(property_section_mapping={"url": "omit"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| Description | Line A\nHas | pipe and \\ backslash |" in result
        assert "\\|" not in result

    def test_excluded_and_mapped_key_overlap(self) -> None:
        issue = _make_issue()
        template = "## Links\n\n{{url}}\n"
        cfg = PropertyConfig(
            excluded_fields=frozenset({"url"}),
            property_section_mapping={"url": "frontmatter"},
        )
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert _frontmatter(result)["url"] == "https://example.com/issues/42"

    @pytest.mark.parametrize(
        ("mapping", "message"),
        [
            ({"status": "omit"}, '"status" can only be mapped to "frontmatter"'),
            ({"url": "sidebar"}, 'invalid mapping target "sidebar" for "url"'),
        ],
    )
    def test_invalid_property_mapping_rejected(self, mapping: dict[str, str], message: str) -> None:
        issue = _make_issue()
        with pytest.raises(TemplateValidationError, match=message):
            render_issue(
                issue,
                "story",
                "## Description\n\n{{description}}\n",
                _RENDERED_AT,
                PropertyConfig(property_section_mapping=mapping),
            )

    def test_mapped_key_ignores_its_stale_exclusion_during_retention(self) -> None:
        issue = _make_issue()
        template = "## Links\n\n{{created_at}} {{url}}\n"
        cfg = PropertyConfig(
            excluded_fields=frozenset({"created_at"}),
            property_section_mapping={"created_at": "body:Links", "url": "body:Links"},
        )
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        body = result.split("---\n", 2)[2]
        assert "2024-01-01T00:00:00Z https://example.com/issues/42" in body
        assert body.count("2024-01-01T00:00:00Z") == 1
        assert body.count("https://example.com/issues/42") == 1

    def test_deterministic_across_runs(self) -> None:
        issue = _make_issue()
        template = "## Description\n\n{{description}}\n\n## Links\n\n{{url}}\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata", "created_at": "omit"})
        first = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        second = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert first == second

    def test_canonical_section_pseudo_row_then_prose(self) -> None:
        issue = _make_issue()
        template = "## Metadata\n\n| A | B |\nplain line\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| A | B |" in result
        assert "| URL | https://example.com/issues/42 |" in result

    def test_canonical_section_two_pseudo_rows(self) -> None:
        issue = _make_issue()
        template = "## Metadata\n\n| A | B |\n| C | D |\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| C | D |" in result
        assert "| URL | https://example.com/issues/42 |" in result

    def test_canonical_section_short_dash_delimiter_is_not_compatible(self) -> None:
        issue = _make_issue()
        template = "## Metadata\n\n| Property | Value |\n| - | - |\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| --- | --- |" in result
        assert "| URL | https://example.com/issues/42 |" in result

    def test_first_compatible_table_is_selected_when_multiple_present(self) -> None:
        """When a section contains two compatible tables, injection targets the first."""
        issue = _make_issue()
        template = (
            "## Metadata\n\n"
            "| Property | Value |\n| --- | --- |\n| Alpha | first |\n\n"
            "| Property | Value |\n| --- | --- |\n| Beta | second |\n"
        )
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        lines = result.splitlines()
        url_idx = next(i for i, ln in enumerate(lines) if "https://example.com/issues/42" in ln)
        beta_idx = next(i for i, ln in enumerate(lines) if "Beta" in ln)
        assert url_idx < beta_idx, "injected row must appear before the second table"

    def test_insertion_stops_at_last_contiguous_data_row_not_crossing_blank_gap(self) -> None:
        """Blank gap separates tables; injection appends after the last contiguous row."""
        issue = _make_issue()
        template = "## Metadata\n\n| Property | Value |\n| --- | --- |\n| Row1 | val1 |\n\nextra prose\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        lines = result.splitlines()
        row1_idx = next(i for i, ln in enumerate(lines) if "val1" in ln)
        url_idx = next(i for i, ln in enumerate(lines) if "https://example.com/issues/42" in ln)
        extra_idx = next(i for i, ln in enumerate(lines) if "extra prose" in ln)
        assert row1_idx < url_idx < extra_idx, (
            "injected row must follow the last contiguous data row before the blank gap"
        )

    def test_indented_code_block_rows_are_not_selected_as_canonical_table(self) -> None:
        issue = _make_issue()
        template = "## Metadata\n\n    | Property | Value |\n    | --- | --- |\n    | Alpha | first |\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| Property | Value |" in result
        assert "| --- | --- |" in result
        assert "| URL | https://example.com/issues/42 |" in result
        assert "    | Alpha | first |" in result

    def test_custom_retained_line_invalidated_by_excluded_placeholder_injects_replacement(self) -> None:
        issue = _make_issue(raw={"priority": "High"})
        template = "## Links\n\n{{url}} ({{priority}})\n"
        cfg = PropertyConfig(
            excluded_fields=frozenset({"priority"}),
            property_section_mapping={"url": "body:Links"},
        )
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        body = result.split("---\n", 2)[2]
        assert "{{priority}}" not in body
        assert "https://example.com/issues/42" in body
        assert "{{url}} (" not in body

    def test_canonical_retained_row_invalidated_by_excluded_placeholder_injects_replacement(self) -> None:
        issue = _make_issue(raw={"priority": "High"})
        template = (
            "## Metadata\n\n| Property | Value |\n| --- | --- |\n| URL | {{url}} {{priority}} |\n| Other | kept |\n"
        )
        cfg = PropertyConfig(
            excluded_fields=frozenset({"priority"}),
            property_section_mapping={"url": "body:Metadata"},
        )
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        body = result.split("---\n", 2)[2]
        assert "{{priority}}" not in body
        assert "| Other | kept |" in body
        assert body.count("https://example.com/issues/42") == 1

    def test_canonical_retained_row_three_cells_injects_replacement(self) -> None:
        """A data row with three cells is not used as the retained destination."""
        issue = _make_issue()
        template = "## Metadata\n\n| Property | Value |\n| --- | --- |\n| URL | {{url}} | Extra |\n| Other | kept |\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        body = result.split("---\n", 2)[2]
        # The 3-column row must NOT survive as the injected destination.
        assert "| URL | https://example.com/issues/42 | Extra |" not in body
        # A canonical 2-column row must be injected.
        assert "| URL | https://example.com/issues/42 |" in body
        assert "| Other | kept |" in body

    def test_custom_section_append_free_text_only(self) -> None:
        issue = _make_issue()
        template = "## Overview\n\nintro\n"
        cfg = PropertyConfig(property_section_mapping={"description": "body:Overview"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "intro" in result
        assert "Implement webhook handler for notifications." in result

    def test_retained_table_cell_encoding(self) -> None:
        issue = _make_issue(created_at="2024-01-01\nnote | pipe")
        template = "## Metadata\n\n| Property | Value |\n| --- | --- |\n| Created | {{created_at}} |\n"
        cfg = PropertyConfig(property_section_mapping={"created_at": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| Created | 2024-01-01<br>note \\| pipe |" in result

    def test_synthesized_section_casefold_tiebreaker(self) -> None:
        issue = _make_issue()
        template = "## Description\n\n{{description}}\n"
        cfg = PropertyConfig(property_section_mapping={"description": "body:Overview", "url": "body:overview"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        body = result.split("---\n")[2]
        assert body.index("## Overview") < body.index("## overview")

    def test_synthesized_heading_not_substituted_when_name_is_placeholder_shaped(self) -> None:
        """Synthesized section heading must not be substituted even if it matches a placeholder."""
        issue = _make_issue(status="open")
        template = "## Description\n\n{{description}}\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:{{status}}"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "## {{status}}" in result
        assert "## open" not in result

    def test_injected_value_with_literal_placeholder_not_reresolved(self) -> None:
        issue = _make_issue(description="please see {{url}} for details")
        template = "## Description\n\n{{description}}\n"
        cfg = PropertyConfig(property_section_mapping={"description": "body:Notes"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "please see {{url}} for details" in result
        assert "https://example.com/issues/42" not in result.split("## Notes", 1)[1]

    def test_injected_canonical_value_with_literal_placeholder_preserved(self) -> None:
        issue = _make_issue(description="code: {{status}} literal")
        template = "## Description\n\n{{description}}\n"
        cfg = PropertyConfig(property_section_mapping={"description": "body:Metadata"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "| Description | code: {{status}} literal |" in result

    def test_injected_labelled_value_with_literal_placeholder_preserved(self) -> None:
        issue = _make_issue(url="https://x/{{status}}/end")
        template = "## Description\n\n{{description}}\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Refs"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert "- URL: https://x/{{status}}/end" in result

    def test_target_section_span_ends_at_next_heading_with_fence(self) -> None:
        issue = _make_issue()
        template = "## Links\n\n- URL: {{url}}\n\n```\n## NotAHeading\n```\n\n## Other\n\ntext\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Links"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        assert result.count("https://example.com/issues/42") == 1
        assert "## Other" in result

    def test_fenced_heading_ignored_for_section_detection(self) -> None:
        issue = _make_issue()
        template = "## Description\n\n```\n## Links\n```\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Links"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        body = result.split("---\n")[2]
        assert body.count("## Links") == 2
        assert "- URL: https://example.com/issues/42" in result

    def test_body_mapped_placeholder_inside_fence_is_removed(self) -> None:
        issue = _make_issue()
        template = "## Description\n\n```\n{{url}}\n```\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Links"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        body = result.split("---\n")[2]
        assert body.count("https://example.com/issues/42") == 1
        assert "```\n{{url}}\n```" not in body
        assert "{{priority}}" not in body

    def test_mapping_path_keeps_target_heading_with_indented_markdown_heading_line(self) -> None:
        issue = _make_issue()
        template = "## Links\n\n    ## Example\n"
        cfg = PropertyConfig(property_section_mapping={"url": "body:Links"})
        result = render_issue(issue, "story", template, _RENDERED_AT, cfg)
        body = result.split("---\n", 2)[2]
        assert "## Links" in body
        assert "    ## Example" in body
        assert "- URL: https://example.com/issues/42" in body

    def test_canonical_field_takes_precedence_over_raw(self) -> None:
        """Canonical field wins over same-named raw key."""
        issue = _make_issue(
            title="Canonical Title",
            raw={"title": "Raw Title"},
        )
        template = "Title: {{title}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Title: Canonical Title" in body

    def test_empty_raw_dict_all_placeholders_empty(self) -> None:
        """Empty raw dict with provider-specific placeholders all resolve empty."""
        issue = _make_issue(provider="markdown", raw={})
        template = "A: {{priority}}, B: {{milestone}}, C: {{severity}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "A: , B: , C: " in body

    def test_jira_nested_fields_placeholder_resolved(self) -> None:
        """Placeholders resolve from top-level raw dict keys (FR-003 two-tier lookup)."""
        issue = _make_issue(
            provider="jira",
            raw={"assignee": "alice", "priority": "High"},
        )
        template = "Assignee: {{assignee}}, Priority: {{priority}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Assignee: alice" in body
        assert "Priority: High" in body

    def test_raw_top_level_takes_priority_over_raw_fields(self) -> None:
        """Top-level raw key wins; nested raw['fields'] is not consulted."""
        issue = _make_issue(
            raw={"priority": "Top-Level", "fields": {"priority": "Nested"}},
        )
        template = "Priority: {{priority}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Priority: Top-Level" in body

    def test_canonical_takes_priority_over_raw_fields(self) -> None:
        """Canonical field wins over same-named key in raw['fields']."""
        issue = _make_issue(
            title="Canonical Title",
            raw={"fields": {"title": "Nested Title"}},
        )
        template = "Title: {{title}}"
        result = render_issue(issue, "task", template, _RENDERED_AT)

        body = result.split("---\n", 2)[2].lstrip("\n")
        assert "Title: Canonical Title" in body

    def test_property_config_exclusion(self) -> None:
        """PropertyConfig excludes specified fields from rendered body."""
        from agentic_devtools.cli.issue_template.renderer import PropertyConfig

        issue = _make_issue(raw={"priority": "High", "milestone": "v2.0"})
        template = "Priority: {{priority}}\nMilestone: {{milestone}}\nDesc: {{description}}"
        config = PropertyConfig(excluded_fields=frozenset({"priority", "milestone"}))
        result = render_issue(issue, "task", template, _RENDERED_AT, property_config=config)

        body = result.split("---\n", 2)[2]
        assert "{{priority}}" not in body
        assert "{{milestone}}" not in body
        assert "Priority:" not in body
        assert "Milestone:" not in body
        assert "Desc: Implement webhook handler" in body

    def test_empty_template_produces_frontmatter_only(self) -> None:
        """Empty template content produces frontmatter + empty body."""
        issue = _make_issue()
        result = render_issue(issue, "task", "", _RENDERED_AT)

        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["id"] == "PROJECT-42"
        # Body should be empty (just newline separator)
        body = parts[2] if len(parts) > 2 else ""
        assert body.strip() == ""

    def test_exclusion_with_alias_equivalence(self) -> None:
        """Excluding 'id' also suppresses {{issue_id}} lines."""
        from agentic_devtools.cli.issue_template.renderer import PropertyConfig

        issue = _make_issue()
        template = "ID: {{id}}\nAlias: {{issue_id}}\nTitle: {{title}}"
        config = PropertyConfig(excluded_fields=frozenset({"id"}))
        result = render_issue(issue, "task", template, _RENDERED_AT, property_config=config)

        body = result.split("---\n", 2)[2]
        assert "ID:" not in body
        assert "Alias:" not in body
        assert "Title: Add webhook support" in body

    def test_yaml_special_chars_in_title_escaped(self) -> None:
        """Special characters in title are properly escaped in frontmatter."""
        issue = _make_issue(title="feat: add support for #tags")
        result = render_issue(issue, "task", "{{description}}", _RENDERED_AT)

        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["title"] == "feat: add support for #tags"

    def test_empty_status_escaped(self) -> None:
        """Empty status value is properly escaped in YAML as quoted empty string."""
        issue = _make_issue(status="")
        result = render_issue(issue, "task", "{{description}}", _RENDERED_AT)
        parts = result.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert frontmatter["status"] == ""
