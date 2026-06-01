"""
Schemas - JSON Schema generation from Python type hints.

Provides utilities for automatically generating JSON schemas from
Python function signatures and type annotations for LLM tool calling.

Example:
    ```python
    from aigie.schemas import generate_json_schema

    def greet(name: str, age: int = 25) -> str:
        '''Greet a person.'''
        return f"Hello {name}, you are {age}!"

    schema = generate_json_schema(greet)
    # {
    #   "type": "object",
    #   "properties": {
    #     "name": {"type": "string"},
    #     "age": {"type": "integer", "default": 25}
    #   },
    #   "required": ["name"]
    # }
    ```
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    ForwardRef,
    Literal,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)
from uuid import UUID


def type_to_json_schema(
    type_hint: Any, include_description: bool = True, definitions: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Convert a Python type hint to JSON Schema.

    Args:
        type_hint: The type annotation to convert
        include_description: Whether to include type name as description
        definitions: Dictionary to store complex type definitions

    Returns:
        JSON Schema dictionary
    """
    if definitions is None:
        definitions = {}

    # Handle None
    if type_hint is None or type_hint is type(None):
        return {"type": "null"}

    # Handle basic types
    if type_hint is str:
        return {"type": "string"}
    if type_hint is int:
        return {"type": "integer"}
    if type_hint is float:
        return {"type": "number"}
    if type_hint is bool:
        return {"type": "boolean"}

    # Handle special types
    if type_hint is bytes:
        return {"type": "string", "format": "binary"}
    if type_hint is datetime:
        return {"type": "string", "format": "date-time"}
    if type_hint is date:
        return {"type": "string", "format": "date"}
    if type_hint is time:
        return {"type": "string", "format": "time"}
    if type_hint is timedelta:
        return {"type": "string", "format": "duration"}
    if type_hint is UUID:
        return {"type": "string", "format": "uuid"}
    if type_hint is Decimal:
        return {"type": "string", "format": "decimal"}
    if type_hint is Path:
        return {"type": "string", "format": "path"}

    # Handle Any
    if type_hint is Any:
        return {}

    # Get origin and args for generic types
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # Handle Optional (Union with None)
    if origin is Union:
        # Filter out None types
        non_none_args = [a for a in args if a is not type(None)]

        if len(non_none_args) == 0:
            return {"type": "null"}
        if len(non_none_args) == 1:
            # Optional[X] becomes just X's schema
            return type_to_json_schema(non_none_args[0], include_description, definitions)
        # Union of multiple types
        return {
            "oneOf": [
                type_to_json_schema(a, include_description, definitions) for a in non_none_args
            ]
        }

    # Handle Literal
    if origin is Literal:
        values = list(args)
        if all(isinstance(v, str) for v in values):
            return {"type": "string", "enum": values}
        if all(isinstance(v, int) for v in values):
            return {"type": "integer", "enum": values}
        if all(isinstance(v, bool) for v in values):
            return {"type": "boolean", "enum": values}
        return {"enum": values}

    # Handle List
    if origin is list or (origin is not None and origin.__name__ == "list"):
        if args:
            return {
                "type": "array",
                "items": type_to_json_schema(args[0], include_description, definitions),
            }
        return {"type": "array"}

    # Handle Set
    if origin is set or (origin is not None and getattr(origin, "__name__", None) == "set"):
        if args:
            return {
                "type": "array",
                "items": type_to_json_schema(args[0], include_description, definitions),
                "uniqueItems": True,
            }
        return {"type": "array", "uniqueItems": True}

    # Handle Tuple
    if origin is tuple or (origin is not None and getattr(origin, "__name__", None) == "tuple"):
        if args:
            if len(args) == 2 and args[1] is ...:
                # Tuple[X, ...] is an array of X
                return {
                    "type": "array",
                    "items": type_to_json_schema(args[0], include_description, definitions),
                }
            # Fixed-length tuple
            return {
                "type": "array",
                "prefixItems": [
                    type_to_json_schema(a, include_description, definitions) for a in args
                ],
                "minItems": len(args),
                "maxItems": len(args),
            }
        return {"type": "array"}

    # Handle Dict
    if origin is dict or (origin is not None and getattr(origin, "__name__", None) == "dict"):
        if args and len(args) >= 2:
            return {
                "type": "object",
                "additionalProperties": type_to_json_schema(
                    args[1], include_description, definitions
                ),
            }
        return {"type": "object"}

    # Handle Enum
    if isinstance(type_hint, type) and issubclass(type_hint, Enum):
        values = [e.value for e in type_hint]
        return {"type": "string", "enum": values}

    # Handle Pydantic models
    if hasattr(type_hint, "model_json_schema"):
        return type_hint.model_json_schema()
    if hasattr(type_hint, "schema"):
        return type_hint.schema()

    # Handle dataclasses
    if hasattr(type_hint, "__dataclass_fields__"):
        properties = {}
        required = []

        for field_name, field_info in type_hint.__dataclass_fields__.items():
            field_type = field_info.type
            field_schema = type_to_json_schema(field_type, include_description, definitions)

            # Check for default
            if field_info.default is not field_info.default_factory:
                if field_info.default is not None:
                    field_schema["default"] = field_info.default
            elif field_info.default_factory is not field_info.default_factory:
                pass  # Has default factory
            else:
                required.append(field_name)

            properties[field_name] = field_schema

        result = {"type": "object", "properties": properties}
        if required:
            result["required"] = required
        return result

    # Handle TypedDict
    if hasattr(type_hint, "__annotations__") and hasattr(type_hint, "__total__"):
        properties = {}
        required = []
        total = getattr(type_hint, "__total__", True)

        for field_name, field_type in type_hint.__annotations__.items():
            properties[field_name] = type_to_json_schema(
                field_type, include_description, definitions
            )
            if total:
                required.append(field_name)

        result = {"type": "object", "properties": properties}
        if required:
            result["required"] = required
        return result

    # Handle ForwardRef (string annotations)
    if isinstance(type_hint, (str, ForwardRef)):
        # Return a placeholder for forward references
        ref_name = type_hint if isinstance(type_hint, str) else type_hint.__forward_arg__
        return {"$ref": f"#/definitions/{ref_name}"}

    # Handle classes with __annotations__
    if hasattr(type_hint, "__annotations__"):
        try:
            hints = get_type_hints(type_hint)
            properties = {}
            required = []

            for field_name, field_type in hints.items():
                properties[field_name] = type_to_json_schema(
                    field_type, include_description, definitions
                )
                # Simple heuristic: if no default, it's required
                if not hasattr(type_hint, field_name):
                    required.append(field_name)

            result = {"type": "object", "properties": properties}
            if required:
                result["required"] = required
            return result
        except Exception:
            pass

    # Fallback for unknown types
    if include_description and hasattr(type_hint, "__name__"):
        return {"description": f"Type: {type_hint.__name__}"}

    return {}


def generate_json_schema(
    func: Callable,
    skip_context: bool = True,
    skip_self: bool = True,
) -> dict[str, Any]:
    """
    Generate JSON Schema from a function's type hints.

    Args:
        func: The function to generate schema for
        skip_context: Skip parameters named 'ctx' or 'context'
        skip_self: Skip 'self' and 'cls' parameters

    Returns:
        JSON Schema dictionary for the function parameters
    """
    try:
        hints = get_type_hints(func)
    except Exception:
        hints = {}

    sig = inspect.signature(func)
    properties = {}
    required = []

    # Parameters to skip
    skip_names = set()
    if skip_self:
        skip_names.update({"self", "cls"})
    if skip_context:
        skip_names.update({"ctx", "context", "run_context"})

    for param_name, param in sig.parameters.items():
        # Skip certain parameters
        if param_name in skip_names:
            continue

        # Skip *args and **kwargs
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue

        # Get type hint
        type_hint = hints.get(param_name, Any)

        # Skip if type is RunContext
        if hasattr(type_hint, "__origin__"):
            origin = get_origin(type_hint)
            if origin and hasattr(origin, "__name__") and "RunContext" in origin.__name__:
                continue
        if hasattr(type_hint, "__name__") and "RunContext" in type_hint.__name__:
            continue

        # Generate schema for this parameter
        param_schema = type_to_json_schema(type_hint)

        # Add default if present
        if param.default is not inspect.Parameter.empty:
            if param.default is not None:
                param_schema["default"] = param.default
        else:
            required.append(param_name)

        # Add description from docstring if available
        # (Could parse docstring here)

        properties[param_name] = param_schema

    result = {
        "type": "object",
        "properties": properties,
    }

    if required:
        result["required"] = required

    return result


def extract_description_from_docstring(func: Callable) -> str | None:
    """
    Extract parameter descriptions from a function's docstring.

    Supports Google, NumPy, and Sphinx docstring formats.

    Args:
        func: The function to extract documentation from

    Returns:
        The function description or None
    """
    docstring = func.__doc__
    if not docstring:
        return None

    # Get first paragraph (before Args:, Parameters:, etc.)
    lines = docstring.strip().split("\n")
    description_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith(
            ("args:", "arguments:", "parameters:", "returns:", "raises:")
        ):
            break
        if stripped.startswith(":param ") or stripped.startswith(":type "):
            break
        description_lines.append(line)

    description = "\n".join(description_lines).strip()
    return description if description else None


def merge_schemas(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """
    Merge two JSON schemas, with override taking precedence.

    Args:
        base: The base schema
        override: Schema values to override

    Returns:
        Merged schema
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_schemas(result[key], value)
        else:
            result[key] = value

    return result


__all__ = [
    "extract_description_from_docstring",
    "generate_json_schema",
    "merge_schemas",
    "type_to_json_schema",
]
