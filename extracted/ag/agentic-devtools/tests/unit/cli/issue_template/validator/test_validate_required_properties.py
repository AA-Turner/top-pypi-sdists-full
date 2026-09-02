"""Tests for agentic_devtools.cli.issue_template.validator.validate_required_properties."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.types import NormalizedIssue, PropertySchema
from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError
from agentic_devtools.cli.issue_template.validator import validate_required_properties


def _make_issue(**kwargs: object) -> NormalizedIssue:
    """Create a NormalizedIssue with sensible defaults."""
    defaults: dict[str, object] = {
        "issue_id": "TEST-1",
        "title": "Test Issue",
        "url": "https://example.com/issues/1",
        "provider": "github",
        "description": "A test issue",
        "status": "open",
        "labels": ["bug"],
        "raw": {},
    }
    defaults.update(kwargs)
    return NormalizedIssue(**defaults)  # type: ignore[arg-type]


def _prop(name: str, required: bool = True) -> PropertySchema:
    """Create a PropertySchema for testing."""
    return PropertySchema(
        name=name,
        type="string",
        required=required,
        allowed_values=None,
    )


class TestValidateRequiredProperties:
    """Tests for the validate_required_properties function."""

    def test_all_present_passes(self) -> None:
        """Happy-path: all required properties present, no error raised."""
        issue = _make_issue(raw={"severity": "High"})
        properties = [_prop("title"), _prop("severity")]
        validate_required_properties(issue, properties)

    def test_missing_none_property(self) -> None:
        """None value counts as missing."""
        issue = _make_issue(raw={"severity": None})
        properties = [_prop("severity")]
        with pytest.raises(TemplateValidationError, match="severity"):
            validate_required_properties(issue, properties)

    def test_missing_empty_string_property(self) -> None:
        """Empty string counts as missing."""
        issue = _make_issue(raw={"severity": ""})
        properties = [_prop("severity")]
        with pytest.raises(TemplateValidationError, match="severity"):
            validate_required_properties(issue, properties)

    def test_missing_whitespace_string_property(self) -> None:
        """Whitespace-only string counts as missing."""
        issue = _make_issue(raw={"severity": "   "})
        properties = [_prop("severity")]
        with pytest.raises(TemplateValidationError, match="severity"):
            validate_required_properties(issue, properties)

    def test_missing_empty_list_property(self) -> None:
        """Empty list counts as missing."""
        issue = _make_issue(labels=[])
        properties = [_prop("labels")]
        with pytest.raises(TemplateValidationError, match="labels"):
            validate_required_properties(issue, properties)

    def test_bool_false_is_valid(self) -> None:
        """Bool False is valid (not missing)."""
        issue = _make_issue(raw={"is_blocked": False})
        properties = [_prop("is_blocked")]
        validate_required_properties(issue, properties)

    def test_int_zero_is_valid(self) -> None:
        """Int 0 is valid (not missing)."""
        issue = _make_issue(raw={"priority_order": 0})
        properties = [_prop("priority_order")]
        validate_required_properties(issue, properties)

    def test_multiple_missing_reported(self) -> None:
        """Multiple missing properties are all reported in error message."""
        issue = _make_issue(raw={})
        properties = [_prop("severity"), _prop("priority")]
        with pytest.raises(TemplateValidationError) as exc_info:
            validate_required_properties(issue, properties)
        assert "severity" in str(exc_info.value)
        assert "priority" in str(exc_info.value)

    def test_optional_property_not_checked(self) -> None:
        """Non-required properties are not checked."""
        issue = _make_issue(raw={})
        properties = [_prop("optional_field", required=False)]
        validate_required_properties(issue, properties)

    def test_canonical_field_checked(self) -> None:
        """Canonical fields (e.g., title) are checked."""
        issue = _make_issue()
        properties = [_prop("title")]
        validate_required_properties(issue, properties)

    def test_missing_key_in_raw_counts_as_missing(self) -> None:
        """Key not present in raw dict and not canonical is missing."""
        issue = _make_issue(raw={})
        properties = [_prop("acceptance_criteria")]
        with pytest.raises(TemplateValidationError, match="acceptance_criteria"):
            validate_required_properties(issue, properties)

    # --- Per-provider tests (3 per provider, 9 total) ---

    def test_github_missing_description(self) -> None:
        """GitHub: missing (empty) description raises error."""
        issue = _make_issue(provider="github", description="")
        properties = [_prop("description")]
        with pytest.raises(TemplateValidationError, match="description"):
            validate_required_properties(issue, properties)

    def test_github_missing_labels(self) -> None:
        """GitHub: empty labels list raises error."""
        issue = _make_issue(provider="github", labels=[])
        properties = [_prop("labels")]
        with pytest.raises(TemplateValidationError, match="labels"):
            validate_required_properties(issue, properties)

    def test_github_missing_raw_milestone(self) -> None:
        """GitHub: missing milestone in raw raises error."""
        issue = _make_issue(provider="github", raw={})
        properties = [_prop("milestone")]
        with pytest.raises(TemplateValidationError, match="milestone"):
            validate_required_properties(issue, properties)

    def test_jira_missing_description(self) -> None:
        """Jira: missing (empty) description raises error."""
        issue = _make_issue(provider="jira", description="")
        properties = [_prop("description")]
        with pytest.raises(TemplateValidationError, match="description"):
            validate_required_properties(issue, properties)

    def test_jira_missing_raw_priority(self) -> None:
        """Jira: missing priority in raw raises error."""
        issue = _make_issue(provider="jira", raw={})
        properties = [_prop("priority")]
        with pytest.raises(TemplateValidationError, match="priority"):
            validate_required_properties(issue, properties)

    def test_jira_missing_raw_severity(self) -> None:
        """Jira: None severity in raw raises error."""
        issue = _make_issue(provider="jira", raw={"severity": None})
        properties = [_prop("severity")]
        with pytest.raises(TemplateValidationError, match="severity"):
            validate_required_properties(issue, properties)

    def test_jira_fields_nested_property_passes(self) -> None:
        """Jira: property present in raw['fields'] satisfies required check."""
        issue = _make_issue(
            provider="jira",
            raw={"fields": {"priority": {"name": "High"}}},
        )
        properties = [_prop("priority")]
        validate_required_properties(issue, properties)

    def test_jira_fields_nested_property_empty_raises(self) -> None:
        """Jira: empty string in raw['fields'] counts as missing."""
        issue = _make_issue(
            provider="jira",
            raw={"fields": {"priority": ""}},
        )
        properties = [_prop("priority")]
        with pytest.raises(TemplateValidationError, match="priority"):
            validate_required_properties(issue, properties)

    def test_jira_fields_nested_property_none_raises(self) -> None:
        """Jira: None value in raw['fields'] counts as missing."""
        issue = _make_issue(
            provider="jira",
            raw={"fields": {"priority": None}},
        )
        properties = [_prop("priority")]
        with pytest.raises(TemplateValidationError, match="priority"):
            validate_required_properties(issue, properties)

    def test_jira_raw_top_level_takes_priority_over_fields(self) -> None:
        """raw top-level key wins over raw['fields'] key of the same name."""
        # raw top-level has empty priority (missing), but raw["fields"] has it —
        # top-level wins, so the property is reported as missing.
        issue = _make_issue(
            provider="jira",
            raw={"priority": "", "fields": {"priority": "High"}},
        )
        properties = [_prop("priority")]
        with pytest.raises(TemplateValidationError, match="priority"):
            validate_required_properties(issue, properties)

    def test_markdown_missing_description(self) -> None:
        """Markdown: missing (empty) description raises error."""
        issue = _make_issue(provider="markdown", description="")
        properties = [_prop("description")]
        with pytest.raises(TemplateValidationError, match="description"):
            validate_required_properties(issue, properties)

    def test_markdown_missing_raw_field(self) -> None:
        """Markdown: missing raw field raises error."""
        issue = _make_issue(provider="markdown", raw={})
        properties = [_prop("custom_field")]
        with pytest.raises(TemplateValidationError, match="custom_field"):
            validate_required_properties(issue, properties)

    def test_markdown_status_present_passes(self) -> None:
        """Markdown: non-empty status passes required-property check."""
        issue = _make_issue(provider="markdown")
        properties = [_prop("status")]
        # status is "open" by default, so this should pass
        validate_required_properties(issue, properties)
