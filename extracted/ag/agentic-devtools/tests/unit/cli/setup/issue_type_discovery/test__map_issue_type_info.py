"""Tests for _map_issue_type_info in issue_type_discovery."""

from __future__ import annotations

from agentic_devtools.adapters.base import IssueTypeInfo
from agentic_devtools.cli.setup.issue_type_discovery import _map_issue_type_info


class TestMapIssueTypeInfo:
    """Tests for _map_issue_type_info."""

    def test_normal_mapping(self) -> None:
        """Maps a standard IssueTypeInfo to IssueTypeEntry correctly."""
        info = IssueTypeInfo(name="Bug", description="A software defect")
        result = _map_issue_type_info(info)
        assert result is not None
        assert result["id"] == "Bug"
        assert result["name"] == "Bug"
        assert result["description"] == "A software defect"
        assert result["is_subtask"] is False
        assert result["properties"] == []

    def test_empty_description_defaults(self) -> None:
        """Empty description is preserved as empty string."""
        info = IssueTypeInfo(name="Story", description="")
        result = _map_issue_type_info(info)
        assert result is not None
        assert result["description"] == ""

    def test_blank_name_skipped(self) -> None:
        """Blank name results in None (skipped)."""
        info = IssueTypeInfo(name="", description="desc")
        result = _map_issue_type_info(info)
        assert result is None

    def test_whitespace_only_name_skipped(self) -> None:
        """Whitespace-only name results in None (skipped)."""
        info = IssueTypeInfo(name="   ", description="desc")
        result = _map_issue_type_info(info)
        assert result is None

    def test_none_name_skipped(self) -> None:
        """None name (via dict access) results in None (skipped)."""
        # IssueTypeInfo is a TypedDict so we simulate missing/None via dict
        info = {"name": None, "description": "desc"}  # type: ignore[typeddict-item]
        result = _map_issue_type_info(info)  # type: ignore[arg-type]
        assert result is None

    def test_none_description_defaults_to_empty(self) -> None:
        """None description defaults to empty string."""
        info = {"name": "Epic", "description": None}  # type: ignore[typeddict-item]
        result = _map_issue_type_info(info)  # type: ignore[arg-type]
        assert result is not None
        assert result["description"] == ""

    def test_non_string_description_defaults_to_empty(self) -> None:
        """Non-string description defaults to empty string."""
        info = {"name": "Task", "description": 123}  # type: ignore[typeddict-item]
        result = _map_issue_type_info(info)  # type: ignore[arg-type]
        assert result is not None
        assert result["description"] == ""

    def test_name_is_trimmed_before_persisting(self) -> None:
        """Leading/trailing whitespace is removed before persisting id and name."""
        info = IssueTypeInfo(name=" Bug ", description="A defect")
        result = _map_issue_type_info(info)
        assert result is not None
        assert result["id"] == "Bug"
        assert result["name"] == "Bug"

    def test_id_equals_name(self) -> None:
        """The id field always equals the name field."""
        info = IssueTypeInfo(name="Sub-task", description="A subtask")
        result = _map_issue_type_info(info)
        assert result is not None
        assert result["id"] == result["name"]
