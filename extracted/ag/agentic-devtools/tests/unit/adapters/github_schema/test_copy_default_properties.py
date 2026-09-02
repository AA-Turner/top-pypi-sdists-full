"""Tests for github_schema.copy_default_properties."""

from __future__ import annotations

from agentic_devtools.adapters.github_schema import DEFAULT_PROPERTIES, copy_default_properties


class TestCopyDefaultProperties:
    """Tests for copy_default_properties function."""

    def test_returns_same_length_as_default(self) -> None:
        """Returned list has the same number of entries as DEFAULT_PROPERTIES."""
        result = copy_default_properties()
        assert len(result) == len(DEFAULT_PROPERTIES)

    def test_returned_list_is_independent(self) -> None:
        """Appending to the returned list does not affect DEFAULT_PROPERTIES."""
        result = copy_default_properties()
        result.append({"name": "extra", "type": "string", "required": False, "allowed_values": None})
        assert len(DEFAULT_PROPERTIES) == 4

    def test_returned_dicts_are_independent(self) -> None:
        """Mutating a returned dict does not affect DEFAULT_PROPERTIES."""
        result = copy_default_properties()
        result[0]["allowed_values"] = ["mutated"]
        assert DEFAULT_PROPERTIES[0]["allowed_values"] is None

    def test_allowed_values_list_is_copied(self) -> None:
        """When allowed_values is a list, the copy is independent."""
        from unittest.mock import patch

        patched_defaults = [
            {"name": "title", "type": "string", "required": True, "allowed_values": ["a", "b"]},
        ]
        with patch("agentic_devtools.adapters.github_schema.DEFAULT_PROPERTIES", patched_defaults):
            result = copy_default_properties()
            copied_values = result[0]["allowed_values"]
            assert copied_values is not None
            copied_values.append("c")
            # The patched constant must remain unchanged
            assert patched_defaults[0]["allowed_values"] == ["a", "b"]

    def test_none_allowed_values_preserved(self) -> None:
        """None allowed_values remains None in the copy."""
        result = copy_default_properties()
        for prop in result:
            assert prop["allowed_values"] is None

    def test_field_values_match_defaults(self) -> None:
        """Copied entries have the same field values as DEFAULT_PROPERTIES."""
        result = copy_default_properties()
        for orig, copy in zip(DEFAULT_PROPERTIES, result):
            assert copy["name"] == orig["name"]
            assert copy["type"] == orig["type"]
            assert copy["required"] == orig["required"]
            assert copy["allowed_values"] == orig["allowed_values"]
