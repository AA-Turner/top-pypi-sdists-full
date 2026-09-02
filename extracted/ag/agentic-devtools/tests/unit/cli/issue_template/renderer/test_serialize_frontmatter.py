"""Tests for _serialize_frontmatter in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

import yaml

from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template.renderer import _serialize_frontmatter


def _make_issue(**kwargs: object) -> NormalizedIssue:
    """Create a NormalizedIssue with sensible defaults."""
    defaults: dict[str, object] = {
        "issue_id": "PROJECT-42",
        "title": "Add webhook support",
        "url": "https://example.com/issues/42",
        "provider": "jira",
        "description": "Implement webhook handler.",
        "status": "open",
        "labels": ["feature", "backend"],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
        "raw": {},
    }
    defaults.update(kwargs)
    return NormalizedIssue(**defaults)  # type: ignore[arg-type]


def _parse_frontmatter(raw: str) -> dict[str, object]:
    """Extract YAML content between --- delimiters and parse it."""
    # Format is "---\n<yaml>\n---"
    lines = raw.split("\n")
    # Skip first "---" and last "---"
    yaml_lines = lines[1:-1]
    return yaml.safe_load("\n".join(yaml_lines))  # type: ignore[no-any-return]


class TestSerializeFrontmatter:
    """Tests for _serialize_frontmatter (FR-002, FR-005, FR-006)."""

    def test_contains_all_seven_required_fields(self) -> None:
        """Frontmatter includes all 7 required fields."""
        issue = _make_issue()
        result = _serialize_frontmatter(issue, "story", "2024-06-15T12:00:00+00:00")
        fm = _parse_frontmatter(result)
        assert set(fm.keys()) == {"id", "title", "type", "status", "provider", "labels", "rendered_at"}

    def test_round_trip_with_yaml_safe_load(self) -> None:
        """Frontmatter round-trips through yaml.safe_load correctly."""
        issue = _make_issue(title="feat: add webhook support")
        result = _serialize_frontmatter(issue, "bug", "2024-06-15T12:00:00+00:00")
        fm = _parse_frontmatter(result)
        assert fm["id"] == "PROJECT-42"
        assert fm["title"] == "feat: add webhook support"
        assert fm["type"] == "bug"
        assert fm["status"] == "open"
        assert fm["provider"] == "jira"
        assert fm["labels"] == ["feature", "backend"]
        assert fm["rendered_at"] == "2024-06-15T12:00:00+00:00"

    def test_labels_as_yaml_list(self) -> None:
        """Labels are serialized as a native YAML list."""
        issue = _make_issue(labels=["bug", "priority-high"])
        result = _serialize_frontmatter(issue, "task", "2024-01-01T00:00:00Z")
        fm = _parse_frontmatter(result)
        assert fm["labels"] == ["bug", "priority-high"]
        assert isinstance(fm["labels"], list)

    def test_empty_labels_as_empty_list(self) -> None:
        """Empty labels render as YAML empty list []."""
        issue = _make_issue(labels=[])
        result = _serialize_frontmatter(issue, "task", "2024-01-01T00:00:00Z")
        fm = _parse_frontmatter(result)
        assert fm["labels"] == []

    def test_boolean_status_round_trips_as_string(self) -> None:
        """Boolean-like status round-trips as string, not bool."""
        issue = _make_issue(status="true")
        result = _serialize_frontmatter(issue, "task", "2024-01-01T00:00:00Z")
        fm = _parse_frontmatter(result)
        assert fm["status"] == "true"
        assert isinstance(fm["status"], str)

    def test_numeric_id_round_trips_as_string(self) -> None:
        """Numeric-looking ID round-trips as string, not int."""
        issue = _make_issue(issue_id="42")
        result = _serialize_frontmatter(issue, "task", "2024-01-01T00:00:00Z")
        fm = _parse_frontmatter(result)
        assert fm["id"] == "42"
        assert isinstance(fm["id"], str)

    def test_empty_string_fields_round_trip(self) -> None:
        """Empty string fields round-trip as empty string, not None."""
        issue = _make_issue(status="")
        result = _serialize_frontmatter(issue, "task", "2024-01-01T00:00:00Z")
        fm = _parse_frontmatter(result)
        assert fm["status"] == ""

    def test_timestamp_rendered_at_round_trips(self) -> None:
        """ISO-8601 timestamp with colons round-trips correctly."""
        issue = _make_issue()
        ts = "2026-07-28T15:00:00+00:00"
        result = _serialize_frontmatter(issue, "task", ts)
        fm = _parse_frontmatter(result)
        assert fm["rendered_at"] == ts
