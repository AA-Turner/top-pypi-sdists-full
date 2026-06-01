from __future__ import annotations

from typing_extensions import (
    Dict,
    List,
    Literal,
    TypedDict,
    Union,
)

from types import NoneType


# Primitive JSON types
JSONSchemaType = Literal[
    "string", "number", "integer", "boolean", "object", "array", "null"
]

JSONSchemaNativeTypes: tuple[type, ...] = (
    str,
    float,
    int,
    bool,
    list,
    set,
    NoneType,
)

JSONType = Union[str, int, float, bool, None, Dict[str, "JSONType"], List["JSONType"]]

# Dynamically define TypedDict with JSON Schema keywords
JSONSchema = TypedDict(
    "JSONSchema",
    {
        "$id": str,
        "$schema": str,
        "$ref": str,
        "$anchor": str,
        "$comment": str,
        "$defs": Dict[str, "JSONSchema"],
        "title": str,
        "description": str,
        "default": JSONType,
        "examples": List[JSONType],
        "type": JSONSchemaType | List[JSONSchemaType],
        "enum": List[JSONType],
        "const": JSONType,
        "properties": Dict[str, "JSONSchema"],
        "patternProperties": Dict[str, "JSONSchema"],
        "additionalProperties": Union[bool, "JSONSchema"],
        "required": List[str],
        "minProperties": int,
        "maxProperties": int,
        "dependencies": Dict[str, Union[List[str], "JSONSchema"]],
        "items": "JSONSchema",
        "prefixItems": List["JSONSchema"],
        "additionalItems": Union[bool, "JSONSchema"],
        "contains": "JSONSchema",
        "minItems": int,
        "maxItems": int,
        "uniqueItems": bool,
        "minLength": int,
        "maxLength": int,
        "pattern": str,
        "format": str,
        "minimum": float,
        "maximum": float,
        "exclusiveMinimum": Union[bool, float],
        "exclusiveMaximum": Union[bool, float],
        "multipleOf": float,
        "if": "JSONSchema",
        "then": "JSONSchema",
        "else": "JSONSchema",
        "allOf": List["JSONSchema"],
        "anyOf": List["JSONSchema"],
        "oneOf": List["JSONSchema"],
        "not": "JSONSchema",
    },
    total=False,  # all fields optional
)
