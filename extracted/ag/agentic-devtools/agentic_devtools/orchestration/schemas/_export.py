"""JSON Schema export utilities for structured LLM output schemas.

Provides export_json_schema() with optional strict mode for LLM structured output APIs.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


def export_json_schema(
    model_class: type[BaseModel],
    *,
    strict_mode: bool = False,
    strict: bool | None = None,
) -> dict[str, Any]:
    """Export a JSON Schema from a Pydantic model class.

    Args:
        model_class: The Pydantic model class to export schema for.
        strict_mode: If True, inline all $ref pointers, add
            additionalProperties: false to all objects, and make all
            object properties required while preserving existing
            nullability from the generated schema. This produces a
            self-contained schema compatible with OpenAI's strict
            structured output mode.
        strict: Alias for strict_mode. When both are given, strict takes
            precedence.

    Returns:
        A JSON Schema dict compatible with Draft 2020-12.

    Raises:
        ValueError: If strict_mode=True and circular references are detected.
    """
    if strict is not None:
        strict_mode = strict

    schema = model_class.model_json_schema()

    if not strict_mode:
        return schema

    # Strict mode: inline all $ref, add additionalProperties: false
    defs = schema.pop("$defs", {})
    resolved = _inline_refs(schema, defs, seen=set())
    _add_strict_constraints(resolved)
    return resolved


def _inline_refs(
    schema: dict[str, Any],
    defs: dict[str, Any],
    *,
    seen: set[str],
) -> dict[str, Any]:
    """Recursively inline all $ref pointers in a JSON Schema.

    Args:
        schema: The schema dict to process.
        defs: The $defs mapping from the root schema.
        seen: Set of definition names currently being resolved (cycle detection).

    Returns:
        The schema with all $ref pointers resolved inline.

    Raises:
        ValueError: If circular references are detected.
    """
    if "$ref" in schema:
        ref_path = schema["$ref"]
        # Extract definition name from "#/$defs/Name"
        if ref_path.startswith("#/$defs/"):
            def_name = ref_path[len("#/$defs/") :]
            if def_name in seen:
                msg = (
                    f"Circular reference detected: {def_name} references itself "
                    f"(chain: {' -> '.join(seen)} -> {def_name}). "
                    f"Cannot inline circular schemas in strict mode."
                )
                raise ValueError(msg)
            if def_name in defs:
                seen_copy = seen | {def_name}
                resolved = _inline_refs(defs[def_name].copy(), defs, seen=seen_copy)
                # Merge any other keys from the original schema (e.g., description)
                for key, value in schema.items():
                    if key != "$ref" and key not in resolved:
                        resolved[key] = value
                return resolved
        # If we can't resolve the ref, return as-is
        return schema

    result: dict[str, Any] = {}
    for key, value in schema.items():
        if key == "$defs":
            continue  # Don't include $defs in output
        if isinstance(value, dict):
            result[key] = _inline_refs(value, defs, seen=seen)
        elif isinstance(value, list):
            result[key] = [_inline_refs(item, defs, seen=seen) if isinstance(item, dict) else item for item in value]
        else:
            result[key] = value
    return result


def _add_strict_constraints(schema: dict[str, Any]) -> None:
    """Add strict-mode constraints to all object schemas in-place.

    - Adds additionalProperties: false to all object types
    - Makes all properties required, preserving their existing nullability

    Fields that are already nullable in the Pydantic-generated schema
    (i.e. they carry ``anyOf: [{...}, {type: null}]``) remain nullable.
    Fields that have a Python default but are not nullable (e.g.
    ``details: str = ""``) are moved into ``required`` without adding
    ``null`` to their type — keeping the exported schema consistent with
    what Pydantic will accept at runtime.
    """
    schema_type = schema.get("type")

    if schema_type == "object":
        schema["additionalProperties"] = False
        properties = schema.get("properties", {})

        # All properties are required; existing nullable fields already carry
        # anyOf/null in their Pydantic-generated schema — no need to inject
        # null into non-nullable optional fields.
        if properties:
            schema["required"] = sorted(properties.keys())

        # Recurse into properties
        for prop_schema in properties.values():
            _add_strict_constraints(prop_schema)

    # Recurse into array items
    if "items" in schema and isinstance(schema["items"], dict):
        _add_strict_constraints(schema["items"])

    # Recurse into anyOf/oneOf/allOf
    for combinator in ("anyOf", "oneOf", "allOf"):
        if combinator in schema and isinstance(schema[combinator], list):
            for item in schema[combinator]:
                if isinstance(item, dict):
                    _add_strict_constraints(item)


def _make_nullable(schema: dict[str, Any]) -> None:
    """Convert a schema to nullable by adding 'null' to the type."""
    if "anyOf" in schema:
        # Check if null is already an option
        has_null = any(item.get("type") == "null" for item in schema["anyOf"] if isinstance(item, dict))
        if not has_null:
            schema["anyOf"].append({"type": "null"})
    elif "type" in schema:
        current_type = schema["type"]
        if isinstance(current_type, list):
            if "null" not in current_type:
                current_type.append("null")
        elif current_type != "null":
            schema["anyOf"] = [{"type": current_type}, {"type": "null"}]
            # Move other constraints to the first anyOf option
            for key in list(schema.keys()):
                if key not in ("anyOf", "description", "title", "default"):
                    schema["anyOf"][0][key] = schema.pop(key)
    else:
        # No type specified, just add anyOf with null
        schema["anyOf"] = [schema.copy(), {"type": "null"}]
        for key in list(schema.keys()):
            if key != "anyOf":
                del schema[key]
