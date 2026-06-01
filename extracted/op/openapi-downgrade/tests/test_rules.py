# tests/test_rules.py

import pytest
import json
import yaml
from unittest.mock import patch, mock_open
from pathlib import Path # Added for loader tests

from openapi_downgrade.converter.rules.mixed_types import convert_mixed_types
from openapi_downgrade.converter.rules.nullable import convert_nullable
from openapi_downgrade.converter.rules.const_to_enum import convert_const
from openapi_downgrade.converter.rules.examples import convert_examples
from openapi_downgrade.converter.rules.exclusives import fix_exclusive_min_max
from openapi_downgrade.converter.rules.fix_null_type import fix_null_type
from openapi_downgrade.converter.rules.booleans import fix_booleans
from openapi_downgrade.converter.rules.conditionals_to_oneof import conditionals_to_oneof
from openapi_downgrade.converter.rules.emulate_tuple_items import emulate_tuple_items
from openapi_downgrade.converter.rules.jsonschema import downgrade_json_schema
from openapi_downgrade.converter.rules.webhooks import drop_webhooks
from openapi_downgrade.converter.rules.warn_unsupported import warn_unsupported_keywords
from openapi_downgrade.converter.warnings import WarningCollector
from openapi_downgrade.converter.loader import load_spec


def test_convert_mixed_types():
    # Test case 1: Simple mixed type
    schema1 = {"type": ["string", "number"]}
    expected1 = {"oneOf": [{"type": "string"}, {"type": "number"}]}
    assert convert_mixed_types(schema1) == expected1

    # Test case 2: Nested mixed type
    schema2 = {
        "type": "object",
        "properties": {
            "id": {"type": ["string", "integer"]},
            "name": {"type": "string"}
        }
    }
    expected2 = {
        "type": "object",
        "properties": {
            "id": {"oneOf": [{"type": "string"}, {"type": "integer"}]},
            "name": {"type": "string"}
        }
    }
    assert convert_mixed_types(schema2) == expected2

    # Test case 3: No mixed type
    schema3 = {"type": "string"}
    expected3 = {"type": "string"}
    assert convert_mixed_types(schema3) == expected3
    
    # Test case 4: Mixed type with only one type in list (should not change)
    schema4 = {"type": ["string"]}
    expected4 = {"type": ["string"]}
    assert convert_mixed_types(schema4) == expected4

def test_convert_nullable_simple_string():
    schema = {"type": ["string", "null"]}
    expected = {"type": "string", "nullable": True}
    assert convert_nullable(schema) == expected

def test_convert_nullable_multiple_types():
    schema = {"type": ["string", "integer", "null"]}
    expected = {"type": ["string", "integer"], "nullable": True}
    assert convert_nullable(schema) == expected

def test_convert_nullable_no_null():
    schema = {"type": ["string", "integer"]}
    expected = {"type": ["string", "integer"]}
    assert convert_nullable(schema) == expected

def test_convert_nullable_nested():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": ["string", "null"]},
            "age": {"type": "integer"}
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "nullable": True},
            "age": {"type": "integer"}
        }
    }
    assert convert_nullable(schema) == expected

def test_convert_const_simple():
    schema = {"const": "value"}
    expected = {"enum": ["value"]}
    assert convert_const(schema) == expected

def test_convert_const_nested():
    schema = {
        "type": "object",
        "properties": {
            "status": {"const": "active"},
            "id": {"type": "integer"}
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "status": {"enum": ["active"]},
            "id": {"type": "integer"}
        }
    }
    assert convert_const(schema) == expected

def test_convert_const_no_const():
    schema = {"type": "string"}
    expected = {"type": "string"}
    assert convert_const(schema) == expected

def test_convert_const_in_array():
    schema = {
        "type": "array",
        "items": [
            {"const": 1},
            {"type": "string"}
        ]
    }
    expected = {
        "type": "array",
        "items": [
            {"enum": [1]},
            {"type": "string"}
        ]
    }
    assert convert_const(schema) == expected

def test_convert_examples_simple():
    schema = {"examples": ["example1", "example2"]}
    expected = {"example": "example1"}
    assert convert_examples(schema) == expected

def test_convert_examples_nested():
    schema = {
        "type": "object",
        "properties": {
            "data": {"examples": ["data1", "data2"]},
            "id": {"type": "integer"}
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "data": {"example": "data1"},
            "id": {"type": "integer"}
        }
    }
    assert convert_examples(schema) == expected

def test_convert_examples_no_examples():
    schema = {"type": "string"}
    expected = {"type": "string"}
    assert convert_examples(schema) == expected

def test_convert_examples_empty_list():
    schema = {"examples": []}
    expected = {}
    assert convert_examples(schema) == expected

def test_fix_exclusive_min_max_min():
    schema = {"exclusiveMinimum": 10}
    expected = {"minimum": 10, "exclusiveMinimum": True}
    assert fix_exclusive_min_max(schema) == expected

def test_fix_exclusive_min_max_max():
    schema = {"exclusiveMaximum": 100}
    expected = {"maximum": 100, "exclusiveMaximum": True}
    assert fix_exclusive_min_max(schema) == expected

def test_fix_exclusive_min_max_both():
    schema = {"exclusiveMinimum": 10, "exclusiveMaximum": 100}
    expected = {"minimum": 10, "exclusiveMinimum": True, "maximum": 100, "exclusiveMaximum": True}
    assert fix_exclusive_min_max(schema) == expected

def test_fix_exclusive_min_max_no_change():
    schema = {"minimum": 5, "maximum": 50}
    expected = {"minimum": 5, "maximum": 50}
    assert fix_exclusive_min_max(schema) == expected

def test_fix_exclusive_min_max_nested():
    schema = {
        "type": "object",
        "properties": {
            "age": {"exclusiveMinimum": 18},
            "score": {"exclusiveMaximum": 100}
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "age": {"minimum": 18, "exclusiveMinimum": True},
            "score": {"maximum": 100, "exclusiveMaximum": True}
        }
    }
    assert fix_exclusive_min_max(schema) == expected

def test_fix_null_type_simple():
    schema = {"type": "null"}
    expected = {"nullable": True}
    assert fix_null_type(schema) == expected

def test_fix_null_type_nested():
    schema = {
        "type": "object",
        "properties": {
            "status": {"type": "null"},
            "id": {"type": "integer"}
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "status": {"nullable": True},
            "id": {"type": "integer"}
        }
    }
    assert fix_null_type(schema) == expected

def test_fix_null_type_no_null():
    schema = {"type": "string"}
    expected = {"type": "string"}
    assert fix_null_type(schema) == expected

def test_fix_null_type_in_oneof():
    schema = {
        "oneOf": [
            {"type": "string"},
            {"type": "null"}
        ]
    }
    expected = {
        "oneOf": [
            {"type": "string"},
            {"nullable": True}
        ]
    }
    assert fix_null_type(schema) == expected

def test_fix_booleans_string_true():
    schema = {"value": "true"}
    expected = {"value": True}
    assert fix_booleans(schema) == expected

def test_fix_booleans_string_false():
    schema = {"value": "false"}
    expected = {"value": False}
    assert fix_booleans(schema) == expected

def test_fix_booleans_nested():
    schema = {
        "type": "object",
        "properties": {
            "enabled": {"value": "true"},
            "admin": {"value": "false"}
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "enabled": {"value": True},
            "admin": {"value": False}
        }
    }
    assert fix_booleans(schema) == expected

def test_fix_booleans_no_change():
    schema = {"value": True}
    expected = {"value": True}
    assert fix_booleans(schema) == expected

def test_fix_booleans_other_string():
    schema = {"value": "other"}
    expected = {"value": "other"}
    assert fix_booleans(schema) == expected

def test_conditionals_to_oneof_simple_const():
    schema = {
        "if": {"properties": {"type": {"const": "A"}}},
        "then": {"properties": {"propA": {"type": "string"}}},
        "else": {"properties": {"propB": {"type": "integer"}}}
    }
    expected = {
        "oneOf": [
            {
                "required": ["type"],
                "properties": {
                    "propA": {"type": "string"},
                    "type": {"enum": ["A"]}
                }
            },
            {
                "required": ["type"],
                "properties": {
                    "propB": {"type": "integer"},
                    "type": {"not": {"const": "A"}}
                }
            }
        ]
    }
    assert conditionals_to_oneof(schema) == expected

def test_conditionals_to_oneof_no_change():
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"}
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "id": {"type": "string"}
        }
    }
    assert conditionals_to_oneof(schema) == expected

def test_conditionals_to_oneof_complex_if():
    original_schema = {
        "if": {"properties": {"type": {"enum": ["A", "B"]}}},
        "then": {"properties": {"propA": {"type": "string"}}},
        "else": None
    }
    schema_copy = original_schema.copy()

    expected = {
        "x-original-conditionals": {
            "if": {"properties": {"type": {"enum": ["A", "B"]}}},
            "then": {"properties": {"propA": {"type": "string"}}},
            "else": None
        }
    }
    result = conditionals_to_oneof(schema_copy)
    assert result == expected

def test_emulate_tuple_items_old_syntax():
    warnings = WarningCollector()
    schema = {
        "type": "array",
        "items": [{"type": "string"}, {"type": "integer"}]
    }
    expected = {
        "type": "array",
        "items": {}, # This is important for 3.0 compatibility
        "minItems": 2,
        "maxItems": 2,
        "x-tuple-items": [
            {"index": 0, "type": "string"},
            {"index": 1, "type": "integer"}
        ]
    }
    result = emulate_tuple_items(schema, warnings)
    assert result == expected
    assert warnings.has_warnings()
    assert "Tuple-style 'items' array detected; emulating using 'x-tuple-items'." in warnings.warnings

def test_emulate_tuple_items_prefix_items():
    warnings = WarningCollector()
    schema = {
        "type": "array",
        "prefixItems": [{"type": "string"}, {"type": "integer"}],
        "items": {"type": "boolean"} # Additional items schema
    }
    expected = {
        "type": "array",
        "items": {"type": "boolean"},
        "minItems": 2,
        "maxItems": 2,
        "x-tuple-items": [
            {"index": 0, "type": "string"},
            {"index": 1, "type": "integer"}
        ]
    }
    result = emulate_tuple_items(schema, warnings)
    assert result == expected
    assert warnings.has_warnings()
    assert "Tuple-style 'prefixItems' detected; emulating using 'x-tuple-items'." in warnings.warnings

def test_emulate_tuple_items_no_change():
    warnings = WarningCollector()
    schema = {
        "type": "array",
        "items": {"type": "string"}
    }
    expected = {
        "type": "array",
        "items": {"type": "string"}
    }
    result = emulate_tuple_items(schema, warnings)
    assert result == expected
    assert not warnings.has_warnings()

def test_emulate_tuple_items_nested():
    warnings = WarningCollector()
    schema = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "prefixItems": [{"type": "string"}, {"type": "integer"}]
            }
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": {},
                "minItems": 2,
                "maxItems": 2,
                "x-tuple-items": [
                    {"index": 0, "type": "string"},
                    {"index": 1, "type": "integer"}
                ]
            }
        }
    }
    result = emulate_tuple_items(schema, warnings)
    assert result == expected
    assert warnings.has_warnings()
    assert "Tuple-style 'prefixItems' detected; emulating using 'x-tuple-items'." in warnings.warnings

def test_downgrade_json_schema_unsupported_keywords():
    warnings = WarningCollector()
    schema = {
        "not": {"type": "string"},
        "dependentSchemas": {"foo": {"type": "integer"}},
        "unevaluatedProperties": False,
        "type": "object"
    }
    expected = {
        "x-dropped-not": {"type": "string"},
        "x-dropped-dependentSchemas": {"foo": {"type": "integer"}},
        "x-dropped-unevaluatedProperties": False,
        "type": "object"
    }
    result = downgrade_json_schema(schema, warnings)
    assert result == expected
    assert warnings.has_warnings()
    assert "The keyword 'not' is not supported in OpenAPI 3.0 and has been moved to 'x-dropped-not'." in warnings.warnings
    assert "The keyword 'dependentSchemas' is not supported in OpenAPI 3.0 and has been moved to 'x-dropped-dependentSchemas'." in warnings.warnings
    assert "The keyword 'unevaluatedProperties' is not supported in OpenAPI 3.0 and has been moved to 'x-dropped-unevaluatedProperties'." in warnings.warnings

def test_downgrade_json_schema_no_unsupported():
    warnings = WarningCollector()
    schema = {"type": "string", "minLength": 5}
    expected = {"type": "string", "minLength": 5}
    result = downgrade_json_schema(schema, warnings)
    assert result == expected
    assert not warnings.has_warnings()

def test_downgrade_json_schema_nested():
    warnings = WarningCollector()
    schema = {
        "type": "object",
        "properties": {
            "item": {
                "not": {"type": "integer"}
            }
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "item": {
                "x-dropped-not": {"type": "integer"}
            }
        }
    }
    result = downgrade_json_schema(schema, warnings)
    assert result == expected
    assert warnings.has_warnings()
    assert "The keyword 'not' is not supported in OpenAPI 3.0 and has been moved to 'x-dropped-not'." in warnings.warnings

def test_drop_webhooks_conversion_success():
    warnings = WarningCollector()
    spec = {
        "webhooks": {
            "newPet": {
                "post": {
                    "requestBody": {"description": "New pet added"}
                }
            }
        },
        "paths": {
            "/pets": {
                "post": {
                    "summary": "Add a new pet"
                }
            }
        }
    }
    expected = {
        "paths": {
            "/pets": {
                "post": {
                    "summary": "Add a new pet",
                    "callbacks": {
                        "newPet": {
                            "{$request.body#/callbackUrl}": {
                                "post": {
                                    "requestBody": {"description": "New pet added"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    result = drop_webhooks(spec, warnings)
    assert result == expected
    assert warnings.has_warnings()
    assert "Webhooks were converted to callbacks on POST, PUT, PATCH, and DELETE operations using a default URL expression '{$request.body#/callbackUrl}'. Please review for correctness." in warnings.warnings

def test_drop_webhooks_no_webhooks():
    warnings = WarningCollector()
    spec = {
        "paths": {
            "/pets": {
                "get": {"summary": "List pets"}
            }
        }
    }
    expected = {
        "paths": {
            "/pets": {
                "get": {"summary": "List pets"}
            }
        }
    }
    result = drop_webhooks(spec, warnings)
    assert result == expected
    assert not warnings.has_warnings()

def test_drop_webhooks_conversion_failure_fallback():
    warnings = WarningCollector()
    spec = {
        "webhooks": {
            "invalidWebhook": "not a path item object" # This will cause an error
        },
        "paths": {}
    }
    expected = {"paths": {}} # Webhooks should be dropped
    result = drop_webhooks(spec, warnings)
    assert result == expected
    assert warnings.has_warnings()
    assert "Webhooks section found, but no suitable operations (POST, PUT, PATCH, DELETE) to attach them to as callbacks." in warnings.warnings

def test_drop_webhooks_no_suitable_operations():
    warnings = WarningCollector()
    spec = {
        "webhooks": {
            "newPet": {
                "post": {
                    "requestBody": {"description": "New pet added"}
                }
            }
        },
        "paths": {
            "/pets": {
                "get": {
                    "summary": "List pets"
                }
            }
        }
    }
    expected = {
        "paths": {
            "/pets": {
                "get": {
                    "summary": "List pets"
                }
            }
        }
    }
    result = drop_webhooks(spec, warnings)
    assert result == expected
    assert warnings.has_warnings()
    assert "Webhooks section found, but no suitable operations (POST, PUT, PATCH, DELETE) to attach them to as callbacks." in warnings.warnings

def test_warn_unsupported_keywords_found():
    warnings = WarningCollector()
    schema = {
        "unevaluatedProperties": False,
        "dependentSchemas": {"foo": {"type": "integer"}},
        "type": "object"
    }
    expected = {
        "unevaluatedProperties": False,
        "dependentSchemas": {"foo": {"type": "integer"}},
        "type": "object"
    }
    result = warn_unsupported_keywords(schema, warnings)
    assert result == schema # The function doesn't modify the schema
    assert warnings.has_warnings()
    assert "Unsupported keyword in 3.0.x: 'unevaluatedProperties'" in warnings.warnings
    assert "Unsupported keyword in 3.0.x: 'dependentSchemas'" in warnings.warnings

def test_warn_unsupported_keywords_not_found():
    warnings = WarningCollector()
    schema = {"type": "string", "minLength": 5}
    expected = {"type": "string", "minLength": 5}
    result = warn_unsupported_keywords(schema, warnings)
    assert result == schema
    assert not warnings.has_warnings()

def test_warn_unsupported_keywords_nested():
    warnings = WarningCollector()
    schema = {
        "type": "object",
        "properties": {
            "item": {
                "contains": {"type": "string"}
            }
        }
    }
    expected = {
        "type": "object",
        "properties": {
            "item": {
                "contains": {"type": "string"}
            }
        }
    }
    result = warn_unsupported_keywords(schema, warnings)
    assert result == schema
    assert warnings.has_warnings()
    assert "Unsupported keyword in 3.0.x: 'contains'" in warnings.warnings

def test_warning_collector_add_and_has_warnings():
    collector = WarningCollector()
    assert not collector.has_warnings()
    collector.add("Test warning 1")
    assert collector.has_warnings()
    assert "Test warning 1" in collector.warnings

def test_warning_collector_add_unique_warnings():
    collector = WarningCollector()
    collector.add("Duplicate warning")
    collector.add("Duplicate warning")
    assert len(collector.warnings) == 1

def test_warning_collector_export(tmp_path):
    collector = WarningCollector()
    collector.add("Export test warning")
    filepath = tmp_path / "test_warnings.txt"
    collector.export(filepath)
    with open(filepath, "r") as f:
        content = f.read()
    assert "- Export test warning\n" in content

def test_load_spec_from_file_json(tmp_path):
    file_content = '{"openapi": "3.1.0"}'
    file_path = tmp_path / "spec.json"
    file_path.write_text(file_content)
    
    spec = load_spec(str(file_path))
    assert spec == {"openapi": "3.1.0"}

def test_load_spec_from_file_yaml(tmp_path):
    file_content = "openapi: 3.1.0"
    file_path = tmp_path / "spec.yaml"
    file_path.write_text(file_content)
    
    spec = load_spec(str(file_path))
    assert spec == {"openapi": "3.1.0"}

def test_load_spec_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_spec("non_existent_file.json")
