"""Tests for type coercion, validation, serialization, and schema generation
additions inspired by Claude Code patterns."""

import json
import sys
from typing import Optional, Union
from unittest import TestCase

from abstra_internals.utils.json_schema import (
    coerce_and_validate,
    coerce_value,
    extract_copywritings,
    type_to_json_schema,
)
from abstra_internals.utils.mcp import (
    serialize_tool_result,
    validate_and_coerce_arguments,
)

_HAS_UNION_TYPE = sys.version_info >= (3, 10)


class TestCoerceValue(TestCase):
    """coerce_value: LLM type tolerance."""

    def test_string_to_int(self):
        self.assertEqual(coerce_value("30", {"type": "integer"}), 30)

    def test_negative_string_to_int(self):
        self.assertEqual(coerce_value("-5", {"type": "integer"}), -5)

    def test_non_numeric_string_stays_string(self):
        self.assertEqual(coerce_value("abc", {"type": "integer"}), "abc")

    def test_empty_string_stays_string(self):
        self.assertEqual(coerce_value("", {"type": "integer"}), "")

    def test_string_to_float(self):
        result = coerce_value("3.14", {"type": "number"})
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(float(result), 3.14)  # type: ignore[arg-type]

    def test_non_numeric_string_stays_for_float(self):
        self.assertEqual(coerce_value("abc", {"type": "number"}), "abc")

    def test_string_true_to_bool(self):
        self.assertIs(coerce_value("true", {"type": "boolean"}), True)

    def test_string_false_to_bool(self):
        self.assertIs(coerce_value("false", {"type": "boolean"}), False)

    def test_string_yes_to_bool(self):
        self.assertIs(coerce_value("yes", {"type": "boolean"}), True)

    def test_string_no_to_bool(self):
        self.assertIs(coerce_value("no", {"type": "boolean"}), False)

    def test_non_bool_string_stays(self):
        self.assertEqual(coerce_value("maybe", {"type": "boolean"}), "maybe")

    def test_float_to_int(self):
        self.assertEqual(coerce_value(30.0, {"type": "integer"}), 30)
        self.assertIsInstance(coerce_value(30.0, {"type": "integer"}), int)

    def test_float_with_decimal_stays_float(self):
        self.assertEqual(coerce_value(30.5, {"type": "integer"}), 30.5)

    def test_none_passthrough(self):
        self.assertIsNone(coerce_value(None, {"type": "integer"}))

    def test_null_string_to_none_with_nullable(self):
        self.assertIsNone(coerce_value("null", {"type": "integer", "nullable": True}))

    def test_null_string_uppercase(self):
        self.assertIsNone(coerce_value("NULL", {"type": "string", "nullable": True}))

    def test_null_string_not_coerced_without_nullable(self):
        self.assertEqual(coerce_value("null", {"type": "string"}), "null")

    def test_whitespace_trimmed(self):
        self.assertEqual(coerce_value("  30  ", {"type": "integer"}), 30)

    def test_no_type_passthrough(self):
        self.assertEqual(coerce_value("hello", {}), "hello")

    def test_json_string_to_array(self):
        self.assertEqual(coerce_value("[50, 60]", {"type": "array"}), [50, 60])

    def test_json_string_to_empty_array(self):
        self.assertEqual(coerce_value("[]", {"type": "array"}), [])

    def test_json_string_to_string_array(self):
        self.assertEqual(coerce_value('["a", "b"]', {"type": "array"}), ["a", "b"])

    def test_json_string_to_nested_array(self):
        self.assertEqual(
            coerce_value("[[1, 2], [3, 4]]", {"type": "array"}), [[1, 2], [3, 4]]
        )

    def test_json_array_with_whitespace(self):
        self.assertEqual(coerce_value("  [1, 2]  ", {"type": "array"}), [1, 2])

    def test_bracketed_non_json_stays_string(self):
        self.assertEqual(coerce_value("[INFO]", {"type": "array"}), "[INFO]")

    def test_malformed_json_array_stays_string(self):
        self.assertEqual(coerce_value("[1, 2,", {"type": "array"}), "[1, 2,")

    def test_actual_array_passthrough(self):
        self.assertEqual(coerce_value([1, 2], {"type": "array"}), [1, 2])

    def test_non_bracketed_string_stays_for_array(self):
        self.assertEqual(coerce_value("hello", {"type": "array"}), "hello")

    def test_json_object_string_not_coerced_to_array(self):
        # Object-shaped JSON should not become an array
        self.assertEqual(coerce_value('{"a": 1}', {"type": "array"}), '{"a": 1}')

    def test_json_string_to_object(self):
        self.assertEqual(coerce_value('{"a": 1}', {"type": "object"}), {"a": 1})

    def test_json_string_to_empty_object(self):
        self.assertEqual(coerce_value("{}", {"type": "object"}), {})

    def test_malformed_json_object_stays_string(self):
        self.assertEqual(coerce_value('{"a": 1', {"type": "object"}), '{"a": 1')

    def test_array_string_not_coerced_to_object(self):
        self.assertEqual(coerce_value("[1, 2]", {"type": "object"}), "[1, 2]")


class TestCoerceAndValidate(TestCase):
    """coerce_and_validate: combined coercion + validation."""

    def test_string_coerced_and_valid(self):
        val, valid = coerce_and_validate("42", {"type": "integer"})
        self.assertEqual(val, 42)
        self.assertTrue(valid)

    def test_string_not_coercible_invalid(self):
        val, valid = coerce_and_validate("abc", {"type": "integer"})
        self.assertEqual(val, "abc")
        self.assertFalse(valid)

    def test_correct_type_valid(self):
        val, valid = coerce_and_validate(42, {"type": "integer"})
        self.assertEqual(val, 42)
        self.assertTrue(valid)

    def test_nullable_none_valid(self):
        val, valid = coerce_and_validate(None, {"type": "integer", "nullable": True})
        self.assertIsNone(val)
        # validate_type returns True for None when type has no explicit null handling
        # This is the fallback behavior
        self.assertTrue(valid)

    def test_json_string_coerced_to_array_and_valid(self):
        val, valid = coerce_and_validate(
            "[50, 60]", {"type": "array", "items": {"type": "integer"}}
        )
        self.assertEqual(val, [50, 60])
        self.assertTrue(valid)

    def test_json_string_coerced_to_fixed_tuple_and_valid(self):
        # Mirrors the schema generated for `workflow_position: tuple[int, int]`.
        tuple_schema = {
            "type": "array",
            "items": [{"type": "integer"}, {"type": "integer"}],
            "minItems": 2,
            "maxItems": 2,
        }
        val, valid = coerce_and_validate("[50, 60]", tuple_schema)
        self.assertEqual(val, [50, 60])
        self.assertTrue(valid)

    def test_json_string_wrong_tuple_arity_invalid(self):
        tuple_schema = {
            "type": "array",
            "items": [{"type": "integer"}, {"type": "integer"}],
            "minItems": 2,
            "maxItems": 2,
        }
        val, valid = coerce_and_validate("[50, 60, 70]", tuple_schema)
        self.assertEqual(val, [50, 60, 70])
        self.assertFalse(valid)

    def test_malformed_json_array_stays_string_and_invalid(self):
        val, valid = coerce_and_validate(
            "[50, 60", {"type": "array", "items": {"type": "integer"}}
        )
        self.assertEqual(val, "[50, 60")
        self.assertFalse(valid)

    def test_plain_string_rejected_as_string_array(self):
        # Regression: before the tighter validate_type check, "hello" would be
        # treated as ["h","e","l","l","o"] and pass validation against items
        # of type string.
        val, valid = coerce_and_validate(
            "hello", {"type": "array", "items": {"type": "string"}}
        )
        self.assertEqual(val, "hello")
        self.assertFalse(valid)

    def test_plain_string_rejected_for_array_without_items(self):
        # Default items={"type":"string"} used to silently accept any string.
        val, valid = coerce_and_validate("hello", {"type": "array"})
        self.assertEqual(val, "hello")
        self.assertFalse(valid)

    def test_bytes_rejected_as_array(self):
        val, valid = coerce_and_validate(b"abc", {"type": "array"})
        self.assertFalse(valid)

    def test_dict_rejected_as_array(self):
        val, valid = coerce_and_validate({"a": 1}, {"type": "array"})
        self.assertFalse(valid)

    def test_python_tuple_accepted_as_array(self):
        # Tuples are valid JSON-schema arrays — some Python callers pass tuples.
        val, valid = coerce_and_validate(
            (1, 2, 3), {"type": "array", "items": {"type": "integer"}}
        )
        self.assertEqual(val, (1, 2, 3))
        self.assertTrue(valid)


class TestValidateAndCoerceArguments(TestCase):
    """validate_and_coerce_arguments: staged validation with instructive errors."""

    def _schema(self):
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "count": {"type": "integer"},
            },
            "required": ["name"],
        }

    def test_valid_args(self):
        result = validate_and_coerce_arguments(
            {"name": "test", "count": 5}, self._schema(), "my_tool"
        )
        self.assertEqual(result, {"name": "test", "count": 5})

    def test_coerces_string_to_int(self):
        result = validate_and_coerce_arguments(
            {"name": "test", "count": "10"}, self._schema(), "my_tool"
        )
        self.assertEqual(result["count"], 10)

    def test_missing_required_raises(self):
        with self.assertRaises(TypeError) as ctx:
            validate_and_coerce_arguments({}, self._schema(), "my_tool")
        self.assertIn("Missing required", str(ctx.exception))
        self.assertIn("name", str(ctx.exception))

    def test_wrong_type_raises_with_hint(self):
        with self.assertRaises(TypeError) as ctx:
            validate_and_coerce_arguments(
                {"name": "test", "count": [1, 2]}, self._schema(), "my_tool"
            )
        self.assertIn("Invalid type", str(ctx.exception))
        self.assertIn("count", str(ctx.exception))

    def test_extra_args_accepted(self):
        result = validate_and_coerce_arguments(
            {"name": "test", "extra": "value"}, self._schema(), "my_tool"
        )
        self.assertEqual(result["extra"], "value")

    def test_empty_schema_accepts_anything(self):
        result = validate_and_coerce_arguments(
            {"anything": "goes"}, {"type": "object"}, "my_tool"
        )
        self.assertEqual(result, {"anything": "goes"})

    def test_coerces_json_string_to_tuple_like_create_job(self):
        # Reproduces the real create_job failure: LLM sends workflow_position as a
        # JSON-encoded string instead of an actual array. The tuple schema below
        # is exactly what type_to_json_schema emits for `tuple[int, int]`.
        create_job_schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "file": {"type": "string"},
                "workflow_position": {
                    "type": "array",
                    "items": [{"type": "integer"}, {"type": "integer"}],
                    "minItems": 2,
                    "maxItems": 2,
                },
            },
            "required": ["title", "file"],
        }
        result = validate_and_coerce_arguments(
            {
                "file": "job_new.py",
                "title": "New job",
                "workflow_position": "[50, 60]",
            },
            create_job_schema,
            "create_job",
        )
        self.assertEqual(result["workflow_position"], [50, 60])


class TestSerializeToolResult(TestCase):
    """serialize_tool_result: JSON serialization with pagination hints."""

    def test_dict_result(self):
        text = serialize_tool_result({"success": True, "data": [1, 2]})
        parsed = json.loads(text)
        self.assertTrue(parsed["success"])

    def test_dict_with_has_more(self):
        text = serialize_tool_result({"has_more": True, "end_line": 50})
        self.assertIn("start_line=51", text)

    def test_dict_with_truncated(self):
        text = serialize_tool_result(
            {"truncated": True, "total_matches": 100, "matches_returned": 10}
        )
        self.assertIn("showing 10 of 100", text)

    def test_list_result(self):
        text = serialize_tool_result([1, 2, 3])
        self.assertIn("Returned 3 items", text)

    def test_empty_list(self):
        text = serialize_tool_result([])
        self.assertNotIn("Returned", text)

    def test_none_result(self):
        text = serialize_tool_result(None)
        self.assertIn("null", text)
        self.assertIn("not found", text)

    def test_string_result(self):
        self.assertEqual(serialize_tool_result("hello"), "hello")

    def test_int_result(self):
        self.assertEqual(serialize_tool_result(42), "42")

    def test_pydantic_model(self):
        from pydantic import BaseModel

        class MyModel(BaseModel):
            name: str
            value: int

        text = serialize_tool_result(MyModel(name="test", value=1))
        parsed = json.loads(text)
        self.assertEqual(parsed["name"], "test")


class TestExtractCopywritings(TestCase):
    """extract_copywritings: parse Copywritings block from docstrings."""

    def test_none_docstring(self):
        self.assertEqual(extract_copywritings(None), {})

    def test_no_copywritings(self):
        self.assertEqual(extract_copywritings("Just a normal docstring."), {})

    def test_one_line(self):
        doc = "Description.\n\nCopywritings:\n    My Title"
        result = extract_copywritings(doc)
        self.assertEqual(result, {"title": "My Title"})

    def test_two_lines(self):
        doc = "Desc.\n\nCopywritings:\n    Title\n    Activity..."
        result = extract_copywritings(doc)
        self.assertEqual(result["title"], "Title")
        self.assertEqual(result["activity"], "Activity...")

    def test_three_lines(self):
        doc = "Desc.\n\nCopywritings:\n    Title\n    Activity...\n    Doing {file}..."
        result = extract_copywritings(doc)
        self.assertEqual(result["activityTemplate"], "Doing {file}...")

    def test_rsplit_takes_last_occurrence(self):
        doc = (
            "This mentions Copywritings: in the body.\n\nCopywritings:\n    Real Title"
        )
        result = extract_copywritings(doc)
        self.assertEqual(result["title"], "Real Title")

    def test_empty_string(self):
        self.assertEqual(extract_copywritings(""), {})


class TestTypeToJsonSchemaUnions(TestCase):
    """type_to_json_schema: union syntax support."""

    def test_typing_optional_int(self):
        schema = type_to_json_schema(Optional[int])
        self.assertEqual(schema["type"], "integer")
        self.assertTrue(schema["nullable"])

    def test_typing_union(self):
        schema = type_to_json_schema(Union[int, str])
        self.assertIn("anyOf", schema)

    def test_plain_int(self):
        schema = type_to_json_schema(int)
        self.assertEqual(schema, {"type": "integer"})

    def test_typing_optional_str(self):
        schema = type_to_json_schema(Optional[str])
        self.assertEqual(schema["type"], "string")
        self.assertTrue(schema["nullable"])

    def test_typing_union_with_none(self):
        schema = type_to_json_schema(Union[int, str, None])
        self.assertIn("anyOf", schema)
        types = {s["type"] for s in schema["anyOf"]}
        self.assertEqual(types, {"integer", "string"})

    @(lambda f: f if _HAS_UNION_TYPE else lambda self: None)
    def test_pep604_int_or_none(self):
        """Python 3.10+ only: int | None"""
        schema = type_to_json_schema(eval("int | None"))  # noqa: S307
        self.assertEqual(schema["type"], "integer")
        self.assertTrue(schema["nullable"])

    @(lambda f: f if _HAS_UNION_TYPE else lambda self: None)
    def test_pep604_int_or_str(self):
        """Python 3.10+ only: int | str"""
        schema = type_to_json_schema(eval("int | str"))  # noqa: S307
        self.assertIn("anyOf", schema)
        types = {s["type"] for s in schema["anyOf"]}
        self.assertEqual(types, {"integer", "string"})
