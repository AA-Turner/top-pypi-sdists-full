"""Tests for MarkdownAdapter.get_issue_types method."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.markdown_adapter import MarkdownAdapter


class TestGetIssueTypes:
    """Tests for MarkdownAdapter.get_issue_types."""

    def test_returns_four_default_types(self, tmp_path: Path) -> None:
        """Default get_issue_types returns exactly 4 IssueTypeInfo dicts."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        types = adapter.get_issue_types()
        assert len(types) == 4

    def test_default_types_declaration_order(self, tmp_path: Path) -> None:
        """Default types are returned in declaration order: task, bug, feature, story."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        types = adapter.get_issue_types()
        assert [t["name"] for t in types] == ["task", "bug", "feature", "story"]

    def test_each_type_has_non_empty_name_and_description(self, tmp_path: Path) -> None:
        """Each default type has non-empty name and description."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        types = adapter.get_issue_types()
        for t in types:
            assert t["name"].strip() != ""
            assert t["description"].strip() != ""

    def test_stability_across_consecutive_calls(self, tmp_path: Path) -> None:
        """10 consecutive calls return identical lists with no side effects."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        first = adapter.get_issue_types()
        for _ in range(9):
            assert adapter.get_issue_types() == first

    def test_returns_deep_copies(self, tmp_path: Path) -> None:
        """Mutating returned list does not affect subsequent calls."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        first = adapter.get_issue_types()
        first[0]["name"] = "mutated"
        first.append({"name": "extra", "description": "extra"})
        second = adapter.get_issue_types()
        assert second[0]["name"] == "task"
        assert len(second) == 4

    def test_override_with_two_types(self, tmp_path: Path) -> None:
        """Override with 2 types returns exactly 2 entries, no defaults."""
        override = {
            "types": [
                {"name": "incident", "description": "An incident", "properties": []},
                {"name": "request", "description": "A request", "properties": []},
            ]
        }
        adapter = MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)
        types = adapter.get_issue_types()
        assert len(types) == 2
        assert [t["name"] for t in types] == ["incident", "request"]

    def test_override_preserves_original_name_case(self, tmp_path: Path) -> None:
        """Override type names round-trip with their original case, not lowercased."""
        override = {
            "types": [
                {"name": "Incident", "description": "An incident", "properties": []},
                {"name": "ServiceRequest", "description": "A request", "properties": []},
            ]
        }
        adapter = MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)
        types = adapter.get_issue_types()
        assert [t["name"] for t in types] == ["Incident", "ServiceRequest"]

    def test_override_with_zero_types(self, tmp_path: Path) -> None:
        """Override with 0 types returns empty list."""
        override: dict = {"types": []}
        adapter = MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)
        types = adapter.get_issue_types()
        assert types == []

    def test_invalid_override_string_raises(self, tmp_path: Path) -> None:
        """Non-dict override raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="must be a dict"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override="invalid")

    def test_invalid_override_int_raises(self, tmp_path: Path) -> None:
        """Integer override raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="must be a dict"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=42)

    def test_invalid_override_list_raises(self, tmp_path: Path) -> None:
        """List override raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="must be a dict"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=[1, 2])

    def test_invalid_override_bool_raises(self, tmp_path: Path) -> None:
        """Bool override raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="must be a dict"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=True)

    def test_override_missing_types_key_raises(self, tmp_path: Path) -> None:
        """Override dict missing 'types' key raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="'types' key"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override={"other": []})

    def test_override_missing_name_raises(self, tmp_path: Path) -> None:
        """Override type entry missing 'name' raises AdapterValidationError."""
        override = {"types": [{"description": "no name", "properties": []}]}
        with pytest.raises(AdapterValidationError, match="'name' key"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_empty_name_raises(self, tmp_path: Path) -> None:
        """Override type entry with empty name raises AdapterValidationError."""
        override = {"types": [{"name": "  ", "description": "empty", "properties": []}]}
        with pytest.raises(AdapterValidationError, match="non-empty string"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_duplicate_names_raises(self, tmp_path: Path) -> None:
        """Duplicate type names after case normalization raise AdapterValidationError."""
        override = {
            "types": [
                {"name": "Task", "description": "a", "properties": []},
                {"name": "task", "description": "b", "properties": []},
            ]
        }
        with pytest.raises(AdapterValidationError, match="Duplicate type name"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_non_string_description_raises(self, tmp_path: Path) -> None:
        """Override type with non-string description raises AdapterValidationError."""
        override = {"types": [{"name": "task", "description": 123, "properties": []}]}
        with pytest.raises(AdapterValidationError, match="description.*must be a string"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_missing_description_raises(self, tmp_path: Path) -> None:
        """Override type entry missing 'description' raises AdapterValidationError."""
        override = {"types": [{"name": "task", "properties": []}]}
        with pytest.raises(AdapterValidationError, match="'description' key"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_missing_properties_raises(self, tmp_path: Path) -> None:
        """Override type entry missing 'properties' raises AdapterValidationError."""
        override = {"types": [{"name": "task", "description": "d"}]}
        with pytest.raises(AdapterValidationError, match="'properties' key"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_types_not_a_list_raises(self, tmp_path: Path) -> None:
        """Override with types not being a list raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="must be a list"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override={"types": "not-a-list"})

    def test_override_type_entry_not_dict_raises(self, tmp_path: Path) -> None:
        """Override type entry that is not a dict raises AdapterValidationError."""
        with pytest.raises(AdapterValidationError, match="must be a dict"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override={"types": ["not-a-dict"]})

    def test_override_properties_not_list_raises(self, tmp_path: Path) -> None:
        """Override with properties not a list raises AdapterValidationError."""
        override = {"types": [{"name": "t", "description": "d", "properties": "bad"}]}
        with pytest.raises(AdapterValidationError, match="must be a list"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_property_not_dict_raises(self, tmp_path: Path) -> None:
        """Override property entry that is not a dict raises AdapterValidationError."""
        override = {"types": [{"name": "t", "description": "d", "properties": ["not-dict"]}]}
        with pytest.raises(AdapterValidationError, match="must be a dict"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_property_name_not_string_raises(self, tmp_path: Path) -> None:
        """Override property with non-string name raises AdapterValidationError."""
        override = {
            "types": [
                {
                    "name": "t",
                    "description": "d",
                    "properties": [{"name": 123, "type": "string", "required": False, "allowed_values": None}],
                }
            ]
        }
        with pytest.raises(AdapterValidationError, match="must be a string"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_property_name_empty_string_raises(self, tmp_path: Path) -> None:
        """Override property with empty/whitespace name raises AdapterValidationError."""
        override = {
            "types": [
                {
                    "name": "t",
                    "description": "d",
                    "properties": [{"name": "   ", "type": "string", "required": False, "allowed_values": None}],
                }
            ]
        }
        with pytest.raises(AdapterValidationError, match="name.*must be a non-empty string"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_property_type_not_string_raises(self, tmp_path: Path) -> None:
        """Override property with non-string type raises AdapterValidationError."""
        override = {
            "types": [
                {
                    "name": "t",
                    "description": "d",
                    "properties": [{"name": "f", "type": 42, "required": False, "allowed_values": None}],
                }
            ]
        }
        with pytest.raises(AdapterValidationError, match="must be a string"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_property_type_empty_string_raises(self, tmp_path: Path) -> None:
        """Override property with empty/whitespace type raises AdapterValidationError."""
        override = {
            "types": [
                {
                    "name": "t",
                    "description": "d",
                    "properties": [{"name": "field", "type": "   ", "required": False, "allowed_values": None}],
                }
            ]
        }
        with pytest.raises(AdapterValidationError, match="type.*must be a non-empty string"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_property_required_not_bool_raises(self, tmp_path: Path) -> None:
        """Override property with non-bool required raises AdapterValidationError."""
        override = {
            "types": [
                {
                    "name": "t",
                    "description": "d",
                    "properties": [{"name": "f", "type": "string", "required": "yes", "allowed_values": None}],
                }
            ]
        }
        with pytest.raises(AdapterValidationError, match="must be a bool"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_property_allowed_values_not_list_raises(self, tmp_path: Path) -> None:
        """Override property with non-list allowed_values raises AdapterValidationError."""
        override = {
            "types": [
                {
                    "name": "t",
                    "description": "d",
                    "properties": [{"name": "f", "type": "string", "required": False, "allowed_values": "bad"}],
                }
            ]
        }
        with pytest.raises(AdapterValidationError, match="must be a list or None"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_property_with_none_allowed_values_passes(self, tmp_path: Path) -> None:
        """Override property with allowed_values=None is valid."""
        override = {
            "types": [
                {
                    "name": "t",
                    "description": "d",
                    "properties": [{"name": "f", "type": "string", "required": False, "allowed_values": None}],
                }
            ]
        }
        adapter = MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)
        props = adapter.get_type_properties("t")
        assert props[0]["allowed_values"] is None
