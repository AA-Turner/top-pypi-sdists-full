"""Tests for _resolve_placeholder in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template.renderer import _resolve_placeholder


def _make_issue(**kwargs: object) -> NormalizedIssue:
    """Create a NormalizedIssue with sensible defaults."""
    defaults: dict[str, object] = {
        "issue_id": "PROJECT-42",
        "title": "Add webhook support",
        "url": "https://example.com/issues/42",
        "provider": "jira",
        "description": "Description text.",
        "status": "open",
        "labels": ["feature", "backend"],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
        "raw": {},
    }
    defaults.update(kwargs)
    return NormalizedIssue(**defaults)  # type: ignore[arg-type]


class TestResolvePlaceholder:
    """Tests for _resolve_placeholder (FR-003, FR-004, FR-008)."""

    def test_tier1_canonical_field_title(self) -> None:
        """Tier 1: canonical NormalizedIssue field 'title' resolves correctly."""
        issue = _make_issue(title="My Title")
        assert _resolve_placeholder("title", issue) == "My Title"

    def test_tier1_canonical_id_resolves_to_issue_id(self) -> None:
        """Tier 1: 'id' resolves to issue.issue_id."""
        issue = _make_issue(issue_id="PROJ-99")
        assert _resolve_placeholder("id", issue) == "PROJ-99"

    def test_tier1_alias_issue_id_resolves_to_issue_id(self) -> None:
        """Alias: 'issue_id' resolves to same value as 'id'."""
        issue = _make_issue(issue_id="PROJ-99")
        assert _resolve_placeholder("issue_id", issue) == "PROJ-99"

    def test_tier2_top_level_raw_key(self) -> None:
        """Tier 2: top-level raw dict key resolves correctly."""
        issue = _make_issue(raw={"priority": "High"})
        assert _resolve_placeholder("priority", issue) == "High"

    def test_canonical_precedence_over_raw(self) -> None:
        """Canonical field takes precedence over same-named raw key."""
        issue = _make_issue(title="Canonical", raw={"title": "Raw"})
        assert _resolve_placeholder("title", issue) == "Canonical"

    def test_missing_field_returns_empty(self) -> None:
        """Missing field (not in canonical or raw) returns empty string."""
        issue = _make_issue(raw={})
        assert _resolve_placeholder("nonexistent", issue) == ""

    def test_none_value_coerced_to_empty(self) -> None:
        """None value in raw dict coerced to empty string."""
        issue = _make_issue(raw={"optional_field": None})
        assert _resolve_placeholder("optional_field", issue) == ""

    def test_list_value_coerced_to_comma_separated(self) -> None:
        """List value coerced to comma-separated string."""
        issue = _make_issue(raw={"assignees": ["alice", "bob"]})
        assert _resolve_placeholder("assignees", issue) == "alice, bob"

    def test_labels_canonical_coerced_to_comma_separated(self) -> None:
        """Canonical labels field coerced to comma-separated string."""
        issue = _make_issue(labels=["bug", "critical"])
        assert _resolve_placeholder("labels", issue) == "bug, critical"

    def test_nested_raw_fields_not_traversed(self) -> None:
        """raw['fields'] nested keys are NOT traversed (FR-003 two-tier only)."""
        issue = _make_issue(raw={"fields": {"nested_key": "nested_value"}})
        assert _resolve_placeholder("nested_key", issue) == ""
