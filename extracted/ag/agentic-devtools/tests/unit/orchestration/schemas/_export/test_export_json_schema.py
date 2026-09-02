"""Tests for export_json_schema() function."""

import json

import pytest

from agentic_devtools.orchestration.schemas._export import export_json_schema
from agentic_devtools.orchestration.schemas.review.result import FileReviewResult
from agentic_devtools.orchestration.schemas.work_on_issue.checklist import ChecklistItem
from agentic_devtools.orchestration.schemas.work_on_issue.plan import ImplementationPlan


class TestExportJsonSchemaDefault:
    """Tests for export_json_schema default mode."""

    def test_returns_valid_json_schema(self):
        schema = export_json_schema(FileReviewResult)
        assert "type" in schema
        assert schema["type"] == "object"
        assert "properties" in schema

    def test_contains_properties(self):
        schema = export_json_schema(FileReviewResult)
        props = schema["properties"]
        assert "file_path" in props
        assert "status" in props
        assert "summary" in props
        assert "findings" in props

    def test_nested_model_uses_defs_or_ref(self):
        schema = export_json_schema(ImplementationPlan)
        # Should have either $defs or inline definitions
        raw = json.dumps(schema)
        assert "tasks" in raw

    def test_constrained_fields_export_enum_contracts(self):
        review_schema = export_json_schema(FileReviewResult)
        assert review_schema["properties"]["status"]["enum"] == ["approved", "needs-work"]

        plan_schema = export_json_schema(ImplementationPlan)
        task_schema = plan_schema["$defs"]["PlanTask"]["properties"]
        risk_schema = plan_schema["$defs"]["RiskAssessment"]["properties"]
        dependency_schema = plan_schema["$defs"]["TaskDependency"]["properties"]
        assert task_schema["estimated_complexity"]["enum"] == ["low", "medium", "high"]
        assert risk_schema["likelihood"]["enum"] == ["low", "medium", "high"]
        assert risk_schema["impact"]["enum"] == ["low", "medium", "high"]
        assert dependency_schema["dependency_type"]["enum"] == ["blocks", "informs", "enables"]

        checklist_schema = export_json_schema(ChecklistItem)
        assert checklist_schema["properties"]["estimated_complexity"]["enum"] == ["low", "medium", "high"]


class TestExportJsonSchemaStrict:
    """Tests for export_json_schema with strict_mode=True."""

    def test_no_ref_or_defs(self):
        schema = export_json_schema(FileReviewResult, strict_mode=True)
        raw = json.dumps(schema)
        assert "$ref" not in raw
        assert "$defs" not in raw

    def test_additional_properties_false(self):
        schema = export_json_schema(FileReviewResult, strict_mode=True)
        assert schema.get("additionalProperties") is False

    def test_all_properties_required(self):
        schema = export_json_schema(FileReviewResult, strict_mode=True)
        props = schema.get("properties", {})
        required = schema.get("required", [])
        for prop_name in props:
            assert prop_name in required

    def test_strict_alias_accepted(self):
        """strict=True is an ergonomic alias for strict_mode=True."""
        schema = export_json_schema(FileReviewResult, strict=True)
        raw = json.dumps(schema)
        assert "$ref" not in raw
        assert "$defs" not in raw
        assert schema.get("additionalProperties") is False

    def test_strict_alias_precedence_over_strict_mode(self):
        """When both strict and strict_mode are given, strict takes precedence."""
        schema_with_alias = export_json_schema(FileReviewResult, strict=True, strict_mode=False)
        schema_plain = export_json_schema(FileReviewResult, strict_mode=True)
        # Both should produce the same strict schema
        assert schema_with_alias.get("additionalProperties") == schema_plain.get("additionalProperties")


class TestExportJsonSchemaCircularRef:
    """Tests for circular reference detection."""

    def test_circular_reference_raises_value_error(self):
        # Create a model with circular reference via $defs manipulation
        # Since our models don't have circular refs, test the guard directly
        from agentic_devtools.orchestration.schemas._export import _inline_refs

        # Simulate circular reference
        defs = {"A": {"$ref": "#/$defs/A"}}
        schema = {"$ref": "#/$defs/A"}
        with pytest.raises(ValueError, match="Circular reference"):
            _inline_refs(schema, defs, seen=set())


class TestInlineRefsEdgeCases:
    """Tests for edge cases in $ref inlining."""

    def test_ref_with_extra_keys_merged(self):
        """Line 82-83: Extra keys from original schema beside $ref are merged."""
        from agentic_devtools.orchestration.schemas._export import _inline_refs

        defs = {"Thing": {"type": "object", "properties": {"x": {"type": "integer"}}}}
        schema = {"$ref": "#/$defs/Thing", "description": "A thing"}
        result = _inline_refs(schema, defs, seen=set())
        assert result["type"] == "object"
        assert result["description"] == "A thing"

    def test_unresolvable_ref_returned_as_is(self):
        """Line 85-86: Unresolvable ref is returned unchanged."""
        from agentic_devtools.orchestration.schemas._export import _inline_refs

        schema = {"$ref": "#/unknown/path"}
        result = _inline_refs(schema, {}, seen=set())
        assert result == {"$ref": "#/unknown/path"}

    def test_defs_key_excluded_from_output(self):
        """Line 90-91: $defs key is not included in output."""
        from agentic_devtools.orchestration.schemas._export import _inline_refs

        schema = {"type": "object", "$defs": {"A": {"type": "string"}}, "properties": {"x": {"type": "integer"}}}
        result = _inline_refs(schema, {}, seen=set())
        assert "$defs" not in result
        assert result["type"] == "object"

    def test_list_items_in_schema_inlined(self):
        """Lists containing dicts in schema values are recursed."""
        from agentic_devtools.orchestration.schemas._export import _inline_refs

        defs = {"S": {"type": "string"}}
        schema = {"anyOf": [{"$ref": "#/$defs/S"}, {"type": "integer"}]}
        result = _inline_refs(schema, defs, seen=set())
        assert result["anyOf"][0] == {"type": "string"}
        assert result["anyOf"][1] == {"type": "integer"}

    def test_ref_to_valid_path_but_missing_def(self):
        """Branch 77->86: $ref with valid #/$defs/ path but name not in defs."""
        from agentic_devtools.orchestration.schemas._export import _inline_refs

        schema = {"$ref": "#/$defs/NonExistent"}
        result = _inline_refs(schema, {"Other": {"type": "string"}}, seen=set())
        assert result == {"$ref": "#/$defs/NonExistent"}


class TestAddStrictConstraintsEdgeCases:
    """Tests for _add_strict_constraints edge cases."""

    def test_object_with_no_properties(self):
        """Branch 120->124: Object type with empty properties dict."""
        from agentic_devtools.orchestration.schemas._export import _add_strict_constraints

        schema = {"type": "object", "properties": {}}
        _add_strict_constraints(schema)
        assert schema["additionalProperties"] is False
        # required should not be set for empty properties
        assert "required" not in schema

    def test_anyof_with_non_dict_items(self):
        """Branch 135->134: anyOf list containing non-dict items."""
        from agentic_devtools.orchestration.schemas._export import _add_strict_constraints

        schema = {"anyOf": [{"type": "string"}, True, {"type": "integer"}]}
        _add_strict_constraints(schema)
        # Should not crash, non-dict items are skipped
        assert schema["anyOf"][1] is True

    def test_non_nullable_optional_field_not_made_nullable(self):
        """Non-nullable fields with defaults must NOT become nullable in strict mode.

        A field like ``details: str = ""`` is absent from Pydantic's ``required``
        list (it has a default) but its type is still ``string``, not
        ``string | null``.  Strict mode must make it required without injecting
        ``null`` into its type, keeping the exported schema consistent with what
        Pydantic accepts at runtime.
        """
        from agentic_devtools.orchestration.schemas.shared.stop_condition import StopCondition

        schema = export_json_schema(StopCondition, strict=True)
        # All three fields must appear in required
        assert "details" in schema["required"]
        assert "is_recoverable" in schema["required"]
        # Neither field should have been widened to nullable
        details_schema = schema["properties"]["details"]
        assert details_schema.get("type") == "string"
        assert "anyOf" not in details_schema
        is_recoverable_schema = schema["properties"]["is_recoverable"]
        assert is_recoverable_schema.get("type") == "boolean"
        assert "anyOf" not in is_recoverable_schema

    def test_already_nullable_field_stays_nullable_in_strict_mode(self):
        """Fields that are genuinely nullable (``int | None``) must stay nullable.

        A field declared as ``line: int | None = None`` already carries
        ``anyOf: [{type: integer}, {type: null}]`` in the Pydantic schema.
        Strict mode must preserve that without stripping or duplicating the
        null branch.
        """
        from agentic_devtools.orchestration.schemas.review.finding import FileReviewFinding

        schema = export_json_schema(FileReviewFinding, strict=True)
        assert "line" in schema["required"]
        line_schema = schema["properties"]["line"]
        # Must still be nullable
        assert "anyOf" in line_schema
        null_variants = [item for item in line_schema["anyOf"] if isinstance(item, dict) and item.get("type") == "null"]
        assert len(null_variants) == 1, "null branch should appear exactly once"


class TestMakeNullableEdgeCases:
    """Tests for _make_nullable edge cases."""

    def test_anyof_already_has_null(self):
        """Line 143-145: anyOf with null already present."""
        from agentic_devtools.orchestration.schemas._export import _make_nullable

        schema = {"anyOf": [{"type": "string"}, {"type": "null"}]}
        _make_nullable(schema)
        # Should not add another null
        null_count = sum(1 for item in schema["anyOf"] if isinstance(item, dict) and item.get("type") == "null")
        assert null_count == 1

    def test_anyof_without_null_appends_null(self):
        """Line 144-145: anyOf without null gets null appended."""
        from agentic_devtools.orchestration.schemas._export import _make_nullable

        schema = {"anyOf": [{"type": "string"}, {"type": "integer"}]}
        _make_nullable(schema)
        assert len(schema["anyOf"]) == 3
        assert schema["anyOf"][2] == {"type": "null"}

    def test_type_as_list_appends_null(self):
        """Line 148-150: Type as list without null gets null appended."""
        from agentic_devtools.orchestration.schemas._export import _make_nullable

        schema = {"type": ["string", "integer"]}
        _make_nullable(schema)
        assert "null" in schema["type"]

    def test_type_as_list_already_has_null(self):
        """Line 148-150: Type as list already containing null is unchanged."""
        from agentic_devtools.orchestration.schemas._export import _make_nullable

        schema = {"type": ["string", "null"]}
        _make_nullable(schema)
        assert schema["type"].count("null") == 1

    def test_type_is_null_no_change(self):
        """Line 151: Type already null gets no change."""
        from agentic_devtools.orchestration.schemas._export import _make_nullable

        schema = {"type": "null"}
        _make_nullable(schema)
        assert schema == {"type": "null"}

    def test_scalar_type_with_constraints_moved_to_anyof(self):
        """Line 152-158: Scalar type with constraints converts to anyOf."""
        from agentic_devtools.orchestration.schemas._export import _make_nullable

        schema = {"type": "integer", "minimum": 0, "maximum": 100}
        _make_nullable(schema)
        assert "anyOf" in schema
        assert "type" not in schema
        assert schema["anyOf"][0]["type"] == "integer"
        assert schema["anyOf"][0]["minimum"] == 0
        assert schema["anyOf"][1] == {"type": "null"}

    def test_no_type_no_anyof_wraps_in_anyof(self):
        """Line 160-164: Schema without type or anyOf wraps in anyOf with null."""
        from agentic_devtools.orchestration.schemas._export import _make_nullable

        schema = {"enum": ["a", "b"]}
        _make_nullable(schema)
        assert "anyOf" in schema
        assert len(schema["anyOf"]) == 2
        assert schema["anyOf"][0]["enum"] == ["a", "b"]
        assert schema["anyOf"][1] == {"type": "null"}
        # Original keys should be cleaned up
        assert "enum" not in schema
