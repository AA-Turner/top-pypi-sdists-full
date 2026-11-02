"""Tests for MarkdownAdapter.get_type_properties method."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.markdown_adapter import MarkdownAdapter


class TestGetTypeProperties:
    """Tests for MarkdownAdapter.get_type_properties."""

    def test_default_task_has_seven_required_properties(self, tmp_path: Path) -> None:
        """Default 'task' type returns at least 7 properties with all required names."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        props = adapter.get_type_properties("task")
        assert len(props) >= 7
        names = [p["name"] for p in props]
        for expected in ("id", "title", "description", "status", "labels", "comments", "created_at"):
            assert expected in names

    @pytest.mark.parametrize("type_name", ["task", "bug", "feature", "story"])
    def test_all_default_types_have_same_properties(self, tmp_path: Path, type_name: str) -> None:
        """All 4 default types have the same 7+ default properties."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        props = adapter.get_type_properties(type_name)
        assert len(props) >= 7
        names = {p["name"] for p in props}
        assert {"id", "title", "description", "status", "labels", "comments", "created_at"} <= names

    def test_every_property_has_allowed_values_key(self, tmp_path: Path) -> None:
        """Every PropertySchema dict contains 'allowed_values' key."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        props = adapter.get_type_properties("task")
        for p in props:
            assert "allowed_values" in p

    def test_default_description_property_is_not_required(self, tmp_path: Path) -> None:
        """Default description schema reflects optional description input."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        props = adapter.get_type_properties("task")
        description_prop = next(p for p in props if p["name"] == "description")
        assert description_prop["required"] is False

    def test_status_property_has_allowed_values(self, tmp_path: Path) -> None:
        """Status property has allowed_values with open, closed, unknown."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        props = adapter.get_type_properties("task")
        status_props = [p for p in props if p["name"] == "status"]
        assert len(status_props) == 1
        av = status_props[0]["allowed_values"]
        assert av is not None
        assert len(av) >= 3
        assert "open" in av
        assert "closed" in av
        assert "unknown" in av

    def test_case_insensitive_lookup_lower(self, tmp_path: Path) -> None:
        """Lowercase 'task' resolves correctly."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        props = adapter.get_type_properties("task")
        assert len(props) >= 7

    def test_case_insensitive_lookup_title(self, tmp_path: Path) -> None:
        """Title-case 'Task' resolves correctly."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        props = adapter.get_type_properties("Task")
        assert len(props) >= 7

    def test_case_insensitive_lookup_upper(self, tmp_path: Path) -> None:
        """Uppercase 'TASK' resolves correctly."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        props = adapter.get_type_properties("TASK")
        assert len(props) >= 7

    def test_empty_string_raises_value_error(self, tmp_path: Path) -> None:
        """Empty string raises ValueError."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        with pytest.raises(ValueError, match="non-empty"):
            adapter.get_type_properties("")

    def test_whitespace_only_raises_value_error(self, tmp_path: Path) -> None:
        """Whitespace-only string raises ValueError."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        with pytest.raises(ValueError, match="non-empty"):
            adapter.get_type_properties("   ")

    def test_unknown_type_raises_value_error(self, tmp_path: Path) -> None:
        """Unknown type name raises ValueError with the type name in message."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        with pytest.raises(ValueError, match="nonexistent"):
            adapter.get_type_properties("nonexistent")

    def test_override_type_with_mixed_case_name_lookup(self, tmp_path: Path) -> None:
        """Case-insensitive lookup works for override types with mixed-case names."""
        override = {
            "types": [
                {"name": "Incident", "description": "An incident", "properties": []},
            ]
        }
        adapter = MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)
        # All of these should resolve to the same type
        assert adapter.get_type_properties("Incident") == []
        assert adapter.get_type_properties("incident") == []
        assert adapter.get_type_properties("INCIDENT") == []

    def test_override_type_with_custom_properties(self, tmp_path: Path) -> None:
        """Override type returns only explicitly listed properties, no defaults."""
        override = {
            "types": [
                {
                    "name": "custom",
                    "description": "A custom type",
                    "properties": [
                        {"name": "severity", "type": "string", "required": True, "allowed_values": ["high", "low"]},
                    ],
                }
            ]
        }
        adapter = MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)
        props = adapter.get_type_properties("custom")
        assert len(props) == 1
        assert props[0]["name"] == "severity"
        assert props[0]["allowed_values"] == ["high", "low"]

    def test_override_properties_are_stored_trimmed(self, tmp_path: Path) -> None:
        """Override property name/type are stripped before schema storage."""
        override = {
            "types": [
                {
                    "name": "custom",
                    "description": "A custom type",
                    "properties": [
                        {"name": " severity ", "type": " string ", "required": True, "allowed_values": None},
                    ],
                }
            ]
        }
        adapter = MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)
        props = adapter.get_type_properties("custom")
        assert props[0]["name"] == "severity"
        assert props[0]["type"] == "string"

    def test_override_type_with_zero_properties(self, tmp_path: Path) -> None:
        """Override type with 0 properties returns empty list."""
        override = {
            "types": [
                {"name": "minimal", "description": "No props", "properties": []},
            ]
        }
        adapter = MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)
        props = adapter.get_type_properties("minimal")
        assert props == []

    def test_override_invalid_allowed_values_element_raises(self, tmp_path: Path) -> None:
        """Override property with non-string allowed_values element raises error."""
        override = {
            "types": [
                {
                    "name": "t",
                    "description": "d",
                    "properties": [
                        {"name": "f", "type": "string", "required": False, "allowed_values": [123]},
                    ],
                }
            ]
        }
        with pytest.raises(AdapterValidationError, match="must be a string"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_override_property_missing_required_keys_raises(self, tmp_path: Path) -> None:
        """Override property missing required keys raises AdapterValidationError."""
        override = {
            "types": [
                {
                    "name": "t",
                    "description": "d",
                    "properties": [
                        {"name": "f"},  # missing type, required, allowed_values
                    ],
                }
            ]
        }
        with pytest.raises(AdapterValidationError, match="'type' key"):
            MarkdownAdapter(repo_path=str(tmp_path), schema_override=override)

    def test_no_filesystem_io_for_consecutive_calls(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """1000 consecutive calls produce stable results with no filesystem I/O."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        # Get reference results before patching
        ref_types = adapter.get_issue_types()
        ref_props = adapter.get_type_properties("task")

        # Patch filesystem operations to detect accidental I/O
        def _raise(*args: object, **kwargs: object) -> None:
            raise AssertionError("Unexpected filesystem I/O")

        monkeypatch.setattr(Path, "iterdir", _raise)
        monkeypatch.setattr(Path, "glob", _raise)
        monkeypatch.setattr(Path, "open", _raise)

        for _ in range(1000):
            assert adapter.get_issue_types() == ref_types
            assert adapter.get_type_properties("task") == ref_props

    def test_returns_deep_copies(self, tmp_path: Path) -> None:
        """Mutating returned properties does not affect subsequent calls."""
        adapter = MarkdownAdapter(repo_path=str(tmp_path))
        first = adapter.get_type_properties("task")
        first[0]["name"] = "mutated"
        first.append({"name": "extra", "type": "x", "required": False, "allowed_values": None})
        second = adapter.get_type_properties("task")
        assert second[0]["name"] == "id"
        assert len(second) == 7
