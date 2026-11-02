"""Locate schema positions independently of instance-valued annotations."""

from collections.abc import Iterator
from typing import ClassVar

from labqoat.json_document import JsonValue


class SchemaNodes:
    """Traverse Draft 2020-12 applicators while keeping property names opaque."""

    maps: ClassVar[frozenset[str]] = frozenset(
        {"$defs", "definitions", "properties", "patternProperties", "dependentSchemas"}
    )
    arrays: ClassVar[frozenset[str]] = frozenset({"allOf", "anyOf", "oneOf", "prefixItems"})
    singles: ClassVar[frozenset[str]] = frozenset(
        {
            "items",
            "contains",
            "additionalProperties",
            "unevaluatedProperties",
            "unevaluatedItems",
            "propertyNames",
            "if",
            "then",
            "else",
            "not",
            "contentSchema",
        }
    )

    @classmethod
    def walk(cls, schema: JsonValue, pointer: str = "") -> Iterator[tuple[str, JsonValue]]:
        """Yield recognized schema locations, including boolean schemas."""
        yield pointer, schema
        if isinstance(schema, dict):
            for keyword, value in schema.items():
                for suffix, child in cls._children(keyword, value):
                    yield from cls.walk(child, pointer + "/" + keyword + suffix)

    @classmethod
    def _children(cls, keyword: str, value: JsonValue) -> Iterator[tuple[str, JsonValue]]:
        """Expand only containers defined to hold subschemas by the fixed dialect."""
        if keyword in cls.maps and isinstance(value, dict):
            for name, child in value.items():
                yield "/" + name.replace("~", "~0").replace("/", "~1"), child
        elif keyword in cls.arrays and isinstance(value, list):
            for index, child in enumerate(value):
                yield "/" + str(index), child
        elif keyword in cls.singles:
            yield "", value
