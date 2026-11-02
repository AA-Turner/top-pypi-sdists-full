"""Cross-language RFC 8785 identities for static schema documents."""

import builtins
import hashlib
import json
import math
from decimal import Decimal
from typing import cast

import rfc8785

from labqoat.json_document import JsonValue


class Identity:
    """Canonicalize captured documents without coercion or schema rewriting."""

    @staticmethod
    def bytes(value: JsonValue) -> bytes:
        """Encode canonical UTF-8, preserving Unicode and rejecting ambiguous values."""
        Identity._check(value)
        return rfc8785.dumps(value)

    @staticmethod
    def check(value: JsonValue) -> None:
        """Require a value the canonical encoding accepts, without paying to produce its bytes."""
        Identity._check(value)

    @staticmethod
    def digest(value: JsonValue) -> str:
        """Return the algorithm-qualified digest of canonical document bytes."""
        return "sha256:" + Identity.hash(Identity.bytes(value))

    @staticmethod
    def hash(value: builtins.bytes) -> str:
        """Hash captured bytes without reinterpreting their content."""
        return hashlib.sha256(value).hexdigest()

    @staticmethod
    def decode(text: str) -> JsonValue:
        """Reject duplicate keys, non-finite numbers, and precision-losing tokens."""
        value = cast(
            JsonValue,
            json.loads(text, object_pairs_hook=Identity._object, parse_float=Identity._float),
        )
        Identity.bytes(value)
        return value

    @staticmethod
    def _object(pairs: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
        """Build a decoded object without discarding duplicate members."""
        result: dict[str, JsonValue] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate object key: {key}")
            result[key] = value
        return result

    @staticmethod
    def _float(token: str) -> float:
        """Require decimal spelling to survive a binary64 round trip."""
        value = float(token)
        if (value == 0 and token.startswith("-")) or Decimal(token) != Decimal(str(value)):
            raise ValueError("number loses precision in binary64")
        return value

    @staticmethod
    def _check(value: JsonValue) -> None:
        """Apply the shared I-JSON character and finite-number policy recursively."""
        if isinstance(value, str):
            Identity._string(value)
        elif isinstance(value, list):
            Identity._items(value)
        elif isinstance(value, dict):
            Identity._members(value)
        else:
            Identity._scalar(value)

    @staticmethod
    def _items(values: list[JsonValue]) -> None:
        """Check long runs of plain integers in place; every other element takes the general path."""
        for item in values:
            if type(item) is not int or not -9_007_199_254_740_991 <= item <= 9_007_199_254_740_991:
                Identity._check(item)

    @staticmethod
    def _scalar(value: object) -> None:
        """Accept only JSON scalars, including finite binary64 numbers."""
        if value is not None and not isinstance(value, (bool, int, float)):
            raise ValueError("value outside the canonical JSON domain")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("non-finite JSON number")
        if type(value) is int and not -9_007_199_254_740_991 <= value <= 9_007_199_254_740_991:
            raise ValueError("integer outside the interoperable JSON range")

    @staticmethod
    def _members(value: dict[str, JsonValue]) -> None:
        """Validate both member names and values before canonical encoding."""
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("object keys must be strings")
            Identity._string(key)
            Identity._check(item)

    @staticmethod
    def _string(value: str) -> None:
        """Reject lone surrogates and I-JSON noncharacters."""
        if value.isascii():
            return
        value.encode("utf-8")
        if any(0xFDD0 <= ord(char) <= 0xFDEF or ord(char) & 0xFFFF >= 0xFFFE for char in value):
            raise ValueError("Unicode noncharacter in JSON string")
