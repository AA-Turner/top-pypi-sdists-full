"""Shared JSON value types for decoded payloads and documents."""

from __future__ import annotations

from typing import TypeVar

ScalarT = TypeVar("ScalarT", str, int, float, bool)

JsonValue = dict[str, "JsonValue"] | list["JsonValue"] | str | int | float | bool | None


class JsonDocument(dict[str, JsonValue]):
    """A decoded JSON object with validation helpers."""

    @staticmethod
    def expect_dict(value: object) -> JsonDocument:
        """Require a JSON object."""
        if isinstance(value, dict):
            return JsonDocument(value)
        raise TypeError(f"expected a JSON object, found {type(value).__name__}")

    @staticmethod
    def expect_optional_dict(value: object) -> JsonDocument | None:
        """Require a JSON object or an explicit null."""
        if value is None:
            return None
        return JsonDocument.expect_dict(value)

    @staticmethod
    def expect_list(value: object) -> list[JsonValue]:
        """Require a JSON array."""
        if isinstance(value, list):
            return list(value)
        raise TypeError(f"expected a JSON array, found {type(value).__name__}")

    @staticmethod
    def expect_scalar(value: object, kind: type[ScalarT]) -> ScalarT:
        """Require a JSON scalar of one kind."""
        if isinstance(value, kind) and not (kind is int and isinstance(value, bool)):
            return value
        raise TypeError(f"expected {kind.__name__}, found {type(value).__name__}")

    @staticmethod
    def expect_optional_scalar(value: object, kind: type[ScalarT]) -> ScalarT | None:
        """Require a JSON scalar of one kind or an explicit null."""
        if value is None:
            return None
        return JsonDocument.expect_scalar(value, kind)

    @staticmethod
    def expect_value(value: object) -> JsonValue:
        """Require and normalize one recursively JSON-compatible value."""
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, (list, tuple)):
            return [JsonDocument.expect_value(item) for item in value]
        if isinstance(value, dict):
            return {str(name): JsonDocument.expect_value(item) for name, item in value.items()}
        raise TypeError(f"expected a JSON value, found {type(value).__name__}")
