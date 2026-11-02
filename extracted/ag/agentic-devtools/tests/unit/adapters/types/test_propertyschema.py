"""Tests for agentic_devtools.adapters.types.PropertySchema."""

from __future__ import annotations

from agentic_devtools.adapters.base import PropertySchema as PropertySchemaFromBase
from agentic_devtools.adapters.types import PropertySchema


class TestPropertySchema:
    """Tests for the PropertySchema TypedDict."""

    def test_importable_from_types_module(self) -> None:
        """PropertySchema can be imported from agentic_devtools.adapters.types."""
        assert PropertySchema is not None

    def test_importable_from_base_module(self) -> None:
        """PropertySchema can be imported from agentic_devtools.adapters.base."""
        assert PropertySchemaFromBase is PropertySchema

    def test_importable_from_package(self) -> None:
        """PropertySchema can be imported from agentic_devtools.adapters."""
        from agentic_devtools.adapters import PropertySchema as PropertySchemaFromPkg

        assert PropertySchemaFromPkg is PropertySchema

    def test_instantiation_with_allowed_values_none(self) -> None:
        """PropertySchema can be instantiated with allowed_values as None."""
        schema: PropertySchema = {
            "name": "summary",
            "type": "string",
            "required": True,
            "allowed_values": None,
        }
        assert schema["name"] == "summary"
        assert schema["type"] == "string"
        assert schema["required"] is True
        assert schema["allowed_values"] is None

    def test_instantiation_with_allowed_values_list(self) -> None:
        """PropertySchema can be instantiated with allowed_values as a list."""
        schema: PropertySchema = {
            "name": "priority",
            "type": "string",
            "required": False,
            "allowed_values": ["High", "Medium", "Low"],
        }
        assert schema["name"] == "priority"
        assert schema["type"] == "string"
        assert schema["required"] is False
        assert schema["allowed_values"] == ["High", "Medium", "Low"]

    def test_instantiation_with_empty_allowed_values_list(self) -> None:
        """PropertySchema can be instantiated with an empty allowed_values list."""
        schema: PropertySchema = {
            "name": "labels",
            "type": "array",
            "required": False,
            "allowed_values": [],
        }
        assert schema["allowed_values"] == []
