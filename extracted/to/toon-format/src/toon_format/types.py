"""Type definitions for TOON encoder and decoder."""

from __future__ import annotations

from typing import Any, Literal, TypeAlias, TypedDict

# JSON-compatible types
JsonPrimitive: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonPrimitive | dict[str, "JsonValue"] | list["JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]
JsonArray: TypeAlias = list[JsonValue]


class EncodeOptions(TypedDict, total=False):
    """Options for encoding values to TOON format.

    Attributes:
        indent: Number of spaces per indentation level (default: 2)
        delimiter: Delimiter for array values and tabular rows (default: ',')
        length_marker: Optional marker to prefix array lengths (default: False)
    """

    indent: int
    delimiter: Literal[",", "\t", "|"]
    length_marker: Literal["#", False]


class DecodeOptions(TypedDict, total=False):
    """Options for decoding TOON format to values.

    Attributes:
        indent: Expected number of spaces per indentation level (default: 2)
        strict: Enable strict validation (default: True)
    """

    indent: int
    strict: bool
