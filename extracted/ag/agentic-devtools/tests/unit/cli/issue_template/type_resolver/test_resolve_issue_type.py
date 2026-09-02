"""Tests for agentic_devtools.cli.issue_template.type_resolver.resolve_issue_type."""

from __future__ import annotations

from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template.type_resolver import resolve_issue_type


def _make_issue(**kwargs: object) -> NormalizedIssue:
    """Create a NormalizedIssue with sensible defaults."""
    defaults: dict[str, object] = {
        "issue_id": "TEST-1",
        "title": "Test Issue",
        "url": "https://example.com/issues/1",
        "provider": "github",
        "description": "A test issue",
        "status": "open",
        "labels": [],
        "raw": {},
    }
    defaults.update(kwargs)
    return NormalizedIssue(**defaults)  # type: ignore[arg-type]


class TestResolveIssueType:
    """Tests for the resolve_issue_type function."""

    def test_raw_issue_type_present(self) -> None:
        """raw['issue_type'] is used when present and non-empty."""
        issue = _make_issue(raw={"issue_type": "Bug"})
        result = resolve_issue_type(issue, {"bug", "story", "task"})
        assert result == "bug"

    def test_raw_issue_type_slug_in_known_types_returned(self) -> None:
        """raw['issue_type'] slug is returned when it matches a known type."""
        issue = _make_issue(raw={"issue_type": "User Story"})
        result = resolve_issue_type(issue, {"user-story", "story", "task"})
        assert result == "user-story"

    def test_raw_issue_type_slug_returned_even_when_not_known(self) -> None:
        """raw['issue_type'] slug is returned even when NOT in known_types (FR-005 step 1).

        Custom types are returned directly so template selection can later fall
        back to issue-template.md; the resolver does NOT fall through to labels.
        """
        issue = _make_issue(raw={"issue_type": "User Story"}, labels=["story"])
        result = resolve_issue_type(issue, {"story", "task"})
        assert result == "user-story"

    def test_empty_raw_issue_type_skipped(self) -> None:
        """Empty string raw['issue_type'] is treated as absent."""
        issue = _make_issue(raw={"issue_type": ""}, labels=["bug"])
        result = resolve_issue_type(issue, {"bug", "story"})
        assert result == "bug"

    def test_whitespace_raw_issue_type_skipped(self) -> None:
        """Whitespace-only raw['issue_type'] is treated as absent."""
        issue = _make_issue(raw={"issue_type": "   "}, labels=["story"])
        result = resolve_issue_type(issue, {"bug", "story"})
        assert result == "story"

    def test_raw_issue_type_slugifies_to_empty_falls_through(self) -> None:
        """raw['issue_type'] that slugifies to empty is treated as absent (FR-005)."""
        issue = _make_issue(raw={"issue_type": "!!!"}, labels=["story"])
        result = resolve_issue_type(issue, {"bug", "story"})
        assert result == "story"

    def test_none_raw_issue_type_not_passed_to_slugify(self) -> None:
        """None raw['issue_type'] is treated as absent (never passed to slugify_type)."""
        issue = _make_issue(raw={"issue_type": None}, labels=["bug"])
        result = resolve_issue_type(issue, {"bug", "story"})
        assert result == "bug"

    def test_label_based_inference_with_known_type(self) -> None:
        """Labels matching a known type slug are used."""
        issue = _make_issue(labels=["bug", "priority-high"])
        result = resolve_issue_type(issue, {"bug", "story"})
        assert result == "bug"

    def test_label_not_in_known_types_ignored(self) -> None:
        """Labels not matching known types are ignored."""
        issue = _make_issue(labels=["priority-high", "frontend"])
        result = resolve_issue_type(issue, {"bug", "story"})
        assert result == "task"

    def test_first_matching_label_wins(self) -> None:
        """The first label matching a known type is used."""
        issue = _make_issue(labels=["story", "bug"])
        result = resolve_issue_type(issue, {"bug", "story"})
        assert result == "story"

    def test_fallback_to_task(self) -> None:
        """Falls back to 'task' when no type can be resolved."""
        issue = _make_issue(labels=["unrelated"])
        result = resolve_issue_type(issue, {"bug", "story"})
        assert result == "task"

    def test_no_labels_no_raw_type_fallback(self) -> None:
        """No labels and no raw type returns 'task'."""
        issue = _make_issue()
        result = resolve_issue_type(issue, {"bug", "story"})
        assert result == "task"

    def test_empty_known_types(self) -> None:
        """Empty known_types set means no label match possible."""
        issue = _make_issue(labels=["bug"])
        result = resolve_issue_type(issue, set())
        assert result == "task"

    def test_raw_issue_type_not_string(self) -> None:
        """Non-string raw['issue_type'] is treated as absent."""
        issue = _make_issue(raw={"issue_type": 123})
        result = resolve_issue_type(issue, {"bug"})
        assert result == "task"

    def test_missing_raw_issue_type_key(self) -> None:
        """Missing raw['issue_type'] key falls through to labels."""
        issue = _make_issue(raw={"other_field": "value"}, labels=["story"])
        result = resolve_issue_type(issue, {"story"})
        assert result == "story"

    def test_nested_jira_issuetype_not_read(self) -> None:
        """Nested raw['fields']['issuetype']['name'] is NOT read (FR-005 top-level only).

        The resolver operates only on the adapter-normalized top-level
        raw['issue_type']; a nested-only Jira payload must fall through to
        labels/default rather than being resolved directly.
        """
        issue = _make_issue(
            raw={"fields": {"issuetype": {"name": "Bug"}}},
            labels=["story"],
        )
        result = resolve_issue_type(issue, {"bug", "story", "task"})
        assert result == "story"

    def test_nested_jira_issuetype_falls_back_to_task(self) -> None:
        """A nested-only Jira payload with no usable labels falls back to 'task'."""
        issue = _make_issue(raw={"fields": {"issuetype": {"name": "Bug"}}})
        result = resolve_issue_type(issue, {"bug", "story", "task"})
        assert result == "task"
