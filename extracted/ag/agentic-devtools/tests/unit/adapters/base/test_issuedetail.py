"""Tests for IssueDetail TypedDict — required + optional normalization fields."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.adapters.base import IssueDetail, JSONValue, _IssueDetailRequired


def _make_required_detail() -> IssueDetail:
    """Return an IssueDetail with only the 7 required fields."""
    return IssueDetail(
        issue_id="123",
        title="Test issue",
        description="A description",
        status="open",
        labels=["bug"],
        url="https://example.com/issues/123",
        comments=[],
    )


class TestAllOptionalFieldsPopulated:
    """Test case 1: All 6 optional fields populated — dict access works."""

    def test_all_optional_fields_accessible(self) -> None:
        detail: IssueDetail = IssueDetail(
            issue_id="1",
            title="Title",
            description="Desc",
            status="open",
            labels=["feat"],
            url="https://example.com/1",
            comments=[],
            issue_type="bug",
            priority="high",
            assignees=["alice", "bob"],
            custom_fields={"sprint": "Sprint 42", "story_points": 5},
            provider="jira",
            raw_metadata={"api_version": "3"},
        )
        assert detail["issue_type"] == "bug"
        assert detail["priority"] == "high"
        assert detail["assignees"] == ["alice", "bob"]
        assert detail["custom_fields"] == {"sprint": "Sprint 42", "story_points": 5}
        assert detail["provider"] == "jira"
        assert detail["raw_metadata"] == {"api_version": "3"}


class TestRequiredFieldsOnly:
    """Test case 2: No optional fields — no errors, required keys accessible."""

    def test_only_required_fields_no_error(self) -> None:
        detail = _make_required_detail()
        assert detail["issue_id"] == "123"
        assert detail["title"] == "Test issue"
        assert detail["description"] == "A description"
        assert detail["status"] == "open"
        assert detail["labels"] == ["bug"]
        assert detail["url"] == "https://example.com/issues/123"
        assert detail["comments"] == []


class TestPartialOptionalFields:
    """Test case 3: Partial population (2 of 6) — mypy-safe runtime access."""

    def test_partial_fields_accessible(self) -> None:
        detail: IssueDetail = IssueDetail(
            issue_id="2",
            title="Partial",
            description="Desc",
            status="open",
            labels=[],
            url="https://example.com/2",
            comments=[],
            provider="github",
            issue_type="story",
        )
        assert detail["provider"] == "github"
        assert detail["issue_type"] == "story"


class TestAssigneesEmptyVsAbsent:
    """Test case 4: assignees as empty list vs key absence — semantic distinction."""

    def test_empty_assignees_is_accessible(self) -> None:
        detail: IssueDetail = IssueDetail(
            issue_id="3",
            title="Empty assignees",
            description="D",
            status="open",
            labels=[],
            url="https://example.com/3",
            comments=[],
            assignees=[],
        )
        assert detail["assignees"] == []

    def test_absent_assignees_raises_keyerror(self) -> None:
        detail = _make_required_detail()
        with pytest.raises(KeyError, match="assignees"):
            detail["assignees"]  # type: ignore[typeddict-item]


class TestCustomFieldsNested:
    """Test case 5: custom_fields with 3+ nested entries — runtime access."""

    def test_nested_custom_fields(self) -> None:
        fields: dict[str, JSONValue] = {
            "sprint": "Sprint 42",
            "story_points": 8,
            "metadata": {"team": "platform", "quarter": "Q4"},
        }
        detail: IssueDetail = IssueDetail(
            issue_id="4",
            title="Nested",
            description="D",
            status="open",
            labels=[],
            url="https://example.com/4",
            comments=[],
            custom_fields=fields,
        )
        cf = detail["custom_fields"]
        assert cf["sprint"] == "Sprint 42"
        assert cf["story_points"] == 8
        assert cf["metadata"] == {"team": "platform", "quarter": "Q4"}


class TestJsonRoundTrip:
    """Test case 6: JSON round-trip serialization for custom_fields and raw_metadata."""

    def test_json_round_trip(self) -> None:
        detail: IssueDetail = IssueDetail(
            issue_id="5",
            title="JSON",
            description="D",
            status="open",
            labels=["a"],
            url="https://example.com/5",
            comments=[],
            custom_fields={"nested": {"key": [1, 2, 3]}},
            raw_metadata={"version": 2, "items": [True, None, "text"]},
        )
        serialized = json.dumps(dict(detail))
        restored = json.loads(serialized)
        assert restored["custom_fields"] == {"nested": {"key": [1, 2, 3]}}
        assert restored["raw_metadata"] == {"version": 2, "items": [True, None, "text"]}


class TestAbsentOptionalKeyDirectAccess:
    """Test case 7: direct access for absent optional key raises KeyError."""

    def test_keyerror_on_absent_optional(self) -> None:
        detail = _make_required_detail()
        with pytest.raises(KeyError, match="provider"):
            detail["provider"]  # type: ignore[typeddict-item]


class TestAbsentOptionalKeyGetAccess:
    """Test case 8: dict.get() returns None for absent optional key."""

    def test_get_returns_none(self) -> None:
        detail = _make_required_detail()
        assert detail.get("provider") is None  # type: ignore[arg-type]
        assert detail.get("issue_type") is None  # type: ignore[arg-type]
        assert detail.get("raw_metadata") is None  # type: ignore[arg-type]


class TestRequiredKeys:
    """Test case 9: __required_keys__ contains exactly 7 keys."""

    def test_required_keys_count(self) -> None:
        expected = {"issue_id", "title", "description", "status", "labels", "url", "comments"}
        assert IssueDetail.__required_keys__ == expected


class TestOptionalKeys:
    """Test case 10: __optional_keys__ contains exactly 6 keys."""

    def test_optional_keys_count(self) -> None:
        expected = {"issue_type", "priority", "assignees", "custom_fields", "provider", "raw_metadata"}
        assert IssueDetail.__optional_keys__ == expected


class TestTotalFieldCount:
    """Test case 11: Combined total is exactly 13 fields."""

    def test_total_field_count(self) -> None:
        total = len(IssueDetail.__required_keys__) + len(IssueDetail.__optional_keys__)
        assert total == 13


class TestTypeCorrectness:
    """Test case 12: type correctness assertions for each optional field value."""

    def test_field_types(self) -> None:
        detail: IssueDetail = IssueDetail(
            issue_id="6",
            title="Types",
            description="D",
            status="open",
            labels=[],
            url="https://example.com/6",
            comments=[],
            issue_type="task",
            priority="low",
            assignees=["user1"],
            custom_fields={"key": "value"},
            provider="markdown",
            raw_metadata={"raw": True},
        )
        assert isinstance(detail["issue_type"], str)
        assert isinstance(detail["priority"], str)
        assert isinstance(detail["assignees"], list)
        assert isinstance(detail["custom_fields"], dict)
        assert isinstance(detail["provider"], str)
        assert isinstance(detail["raw_metadata"], dict)


class TestPrivateBaseNotExported:
    """Test case: _IssueDetailRequired is not in adapters.__all__."""

    def test_not_in_adapters_all(self) -> None:
        import agentic_devtools.adapters as adapters_pkg

        assert "_IssueDetailRequired" not in adapters_pkg.__all__
        assert not hasattr(adapters_pkg, "_IssueDetailRequired")

    def test_private_base_exists(self) -> None:
        # Confirm the private base is accessible for internal use
        assert hasattr(_IssueDetailRequired, "__required_keys__")
        assert _IssueDetailRequired.__required_keys__ == {
            "issue_id",
            "title",
            "description",
            "status",
            "labels",
            "url",
            "comments",
        }
