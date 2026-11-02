"""Sanitization helpers for generic metric attributes."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from types import MappingProxyType

_ATTRIBUTION_EVENT_SCHEMAS: dict[str, tuple[frozenset[str], dict[str, frozenset[str]]]] = {
    "unknown_attribution": (
        frozenset({"outcome"}),
        {
            "outcome": frozenset({"unknown", "complete"}),
            "reason": frozenset({"incomplete"}),
        },
    ),
    "watermark_advanced": (
        frozenset({"outcome"}),
        {"outcome": frozenset({"advanced"})},
    ),
    "provider_attribution_failure": (
        frozenset({"outcome", "reason"}),
        {
            "outcome": frozenset({"failed"}),
            "reason": frozenset({"provider_error"}),
        },
    ),
}


def _sanitize_mapping(
    attributes: Mapping[str, object],
    *,
    event_type: str | None = None,
) -> MappingProxyType[str, object]:
    schema = _ATTRIBUTION_EVENT_SCHEMAS.get(event_type or "")
    if schema is not None:
        required_keys, enum_values = schema
        allowed_keys = {"pr_number", *enum_values}
        unexpected_keys = set(attributes) - allowed_keys
        if unexpected_keys:
            raise ValueError("Unsupported attribution metric attributes")

        missing_keys = required_keys - attributes.keys()
        if missing_keys:
            raise ValueError(f"Missing attribution metric attributes: {missing_keys!r}")

        for key, value in attributes.items():
            if key == "pr_number":
                if type(value) is not int or value <= 0:
                    raise ValueError("Attribution metric pr_number must be a positive integer")
                continue
            if not isinstance(value, str) or value not in enum_values[key]:
                raise ValueError(f"Unsupported attribution metric {key}")

    return MappingProxyType(
        {
            str(key): _sanitize_attribute_value(value)
            for key, value in sorted(attributes.items(), key=lambda item: str(item[0]))
        }
    )


def _sanitize_attribute_value(value: object) -> object:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise TypeError("Metric attribute datetimes must be timezone-aware")
        return value.isoformat()
    if isinstance(value, Enum):
        return _sanitize_attribute_value(value.value)
    if isinstance(value, Mapping):
        return _sanitize_mapping(value)
    if isinstance(value, (list, tuple)):
        return tuple(_sanitize_attribute_value(item) for item in value)
    if isinstance(value, (set, frozenset)):
        sanitized = (_sanitize_attribute_value(item) for item in value)
        return tuple(sorted(sanitized, key=repr))
    return f"<redacted:{type(value).__name__}>"
