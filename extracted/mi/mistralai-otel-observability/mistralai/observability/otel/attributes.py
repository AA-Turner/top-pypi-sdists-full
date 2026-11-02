"""OpenTelemetry attribute normalization for transformed operation data."""

import json
from collections.abc import Mapping, Sequence
from typing import cast

from opentelemetry.util.types import AttributeValue

from .hooks import OperationDataValue

_OTEL_PRIMITIVE_TYPES = (str, bool, int, float)


def normalize_otel_attribute(
    value: OperationDataValue,
    *,
    structured_document: bool = False,
) -> AttributeValue | None:
    """Convert an already-transformed value into an OTel attribute.

    Structured GenAI fields represent one JSON document, while ordinary
    homogeneous primitive sequences remain OpenTelemetry attribute arrays.
    """
    if value is None or isinstance(value, _OTEL_PRIMITIVE_TYPES):
        return value
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    if not structured_document and isinstance(value, Sequence) and _is_otel_primitive_sequence(value):
        return cast("AttributeValue", value)
    return _json_attribute(value)


def normalize_otel_attributes(
    attributes: Mapping[str, OperationDataValue],
) -> dict[str, AttributeValue]:
    """Normalize transformed attributes and omit values dropped as ``None``."""
    normalized: dict[str, AttributeValue] = {}
    for key, value in attributes.items():
        attribute = normalize_otel_attribute(value)
        if attribute is not None:
            normalized[key] = attribute
    return normalized


def _is_otel_primitive_sequence(value: Sequence[OperationDataValue]) -> bool:
    if not value:
        return True
    item_type = type(value[0])
    return item_type in _OTEL_PRIMITIVE_TYPES and all(type(item) is item_type for item in value)


def _json_attribute(value: OperationDataValue) -> str:
    return json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"))


def _jsonable(value: object) -> object:
    if value is None or isinstance(value, _OTEL_PRIMITIVE_TYPES):
        return value
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    if isinstance(value, Mapping):
        mapping = cast("Mapping[str, object]", value)
        return {key: _jsonable(nested_value) for key, nested_value in mapping.items()}
    if isinstance(value, Sequence):
        sequence = cast("Sequence[object]", value)
        return [_jsonable(nested_value) for nested_value in sequence]
    message = f"Unsupported operation data type: {type(value).__name__}"
    raise TypeError(message)
