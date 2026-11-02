"""Lossless JSON encoding for workflow dataclasses and references."""

from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import Enum
from math import isfinite
from uuid import UUID

from labqoat.json_document import JsonValue
from labqoat.references import DatasetRef, ResourceId, Sha256
from labqoat.schemas.schema_record import SchemaRecord


class ValueEncoder:
    """Encode authored values without importing framework dependencies."""

    @staticmethod
    def encode(value: object) -> JsonValue:
        """Convert supported typed values into strict JSON."""
        if isinstance(value, SchemaRecord | DatasetRef):
            return value.to_dict() if isinstance(value, SchemaRecord) else value.document()
        if isinstance(value, ResourceId | Sha256):
            return str(value)
        if isinstance(value, Enum):
            return ValueEncoder.encode(value.value)
        if isinstance(value, datetime):
            return value.isoformat()
        if is_dataclass(value) and not isinstance(value, type):
            return {item.name: ValueEncoder.encode(getattr(value, item.name)) for item in fields(value)}
        if isinstance(value, Mapping):
            return ValueEncoder.mapping(value)
        if isinstance(value, tuple | list):
            return [ValueEncoder.encode(item) for item in value]
        return ValueEncoder.scalar(value)

    @staticmethod
    def mapping(value: Mapping[object, object]) -> dict[str, JsonValue]:
        """Reject nonstring keys rather than silently changing them."""
        if not all(isinstance(key, str) for key in value):
            raise ValueError("JSON object keys must be strings")
        return {str(key): ValueEncoder.encode(item) for key, item in value.items()}

    @staticmethod
    def scalar(value: object) -> JsonValue:
        """Require a finite JSON scalar."""
        if isinstance(value, float) and not isfinite(value):
            raise ValueError("JSON numbers must be finite")
        if isinstance(value, UUID):
            return str(value)
        if value is None or isinstance(value, str | int | float | bool):
            return value
        raise TypeError(f"Unsupported workflow value: {type(value).__name__}")
