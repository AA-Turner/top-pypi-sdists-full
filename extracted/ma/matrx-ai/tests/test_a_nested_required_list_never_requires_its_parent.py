"""An object parameter's NESTED required list never makes the parameter itself required.

2026-10-03: the frontend offered ``apply_surface_write`` an optional ``item``
(``{resource_type, resource_id}``, both required INSIDE it). The internal
notation overloads ``required`` — a BOOL on a scalar, the nested LIST on an
object — and every schema builder read it truthily, so ``item`` became required
at the root and the pre-delegation check refused every call without it
("<root>: 'item' is a required property").
"""

from __future__ import annotations

from matrx_ai.tools.executor import _validate_against_declared_schema
from matrx_ai.tools.models import ToolDefinition


def _surface_write_tool() -> ToolDefinition:
    return ToolDefinition(
        name="apply_surface_write",
        parameters={
            "target": {"type": "string", "description": "t"},
            "item": {
                "type": "object",
                "description": "the record",
                "properties": {
                    "resource_type": {"type": "string"},
                    "resource_id": {"type": "string"},
                },
                "required": ["resource_type", "resource_id"],
            },
            "value": {"type": ["string", "object"], "description": "v"},
        },
        required_params=["target", "value"],
    )


def test_the_root_requires_only_what_the_root_lists() -> None:
    schema = _surface_write_tool()._build_json_schema(contract=True)
    assert schema["required"] == ["target", "value"]
    assert schema["properties"]["item"]["required"] == ["resource_type", "resource_id"]


def test_google_format_keeps_item_optional() -> None:
    params = _surface_write_tool().to_google_format()["parameters"]
    assert "item" not in params.get("required", [])


def test_a_call_without_the_optional_object_passes_the_delegation_check() -> None:
    tool = _surface_write_tool()
    assert _validate_against_declared_schema(tool, {"target": "x", "value": "y"}) is None


def test_a_given_object_still_needs_its_nested_fields() -> None:
    error = _validate_against_declared_schema(
        _surface_write_tool(), {"target": "x", "value": "y", "item": {"resource_type": "html_page"}}
    )
    assert error is not None and "resource_id" in error


def test_a_bool_flag_still_marks_a_parameter_required() -> None:
    tool = ToolDefinition(name="t", parameters={"q": {"type": "string", "required": True}})
    assert tool._build_json_schema()["required"] == ["q"]
