"""Input validation using JSON Schema (FR-006).

Validates tool invocation parameters against the tool's declared
``input_schema``.  Uses cached ``jsonschema.Draft202012Validator``
instances for performance.
"""

from __future__ import annotations

import functools
from typing import Any

import jsonschema

from .result import ToolResult


@functools.lru_cache(maxsize=128)
def _get_validator(schema_json: str) -> jsonschema.Draft202012Validator:
    """Return a cached validator for the given schema.

    ``schema_json`` acts as both the cache key and the deserialization source.
    """
    import json

    schema = json.loads(schema_json)
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def validate_inputs(input_schema: dict[str, Any], inputs: dict[str, Any]) -> ToolResult | None:
    """Validate *inputs* against *input_schema*.

    Returns ``None`` if validation succeeds, or a ``ToolResult`` with
    ``success=False`` and ``error_type="validation_error"`` on failure.
    """
    import json

    try:
        schema_json = json.dumps(input_schema, sort_keys=True)
        validator = _get_validator(schema_json)
    except (TypeError, ValueError) as exc:
        return ToolResult(
            success=False,
            error_type="validation_error",
            error_message=f"Invalid tool schema: {exc}",
        )
    except jsonschema.SchemaError as exc:
        return ToolResult(
            success=False,
            error_type="validation_error",
            error_message=f"Invalid tool schema: {exc.message}",
        )

    first_error = next(validator.iter_errors(inputs), None)
    if first_error is not None:
        path = ".".join(str(p) for p in first_error.absolute_path) if first_error.absolute_path else ""
        field_info = f" (field: {path})" if path else ""
        return ToolResult(
            success=False,
            error_type="validation_error",
            error_message=f"{first_error.message}{field_info}",
        )

    return None
