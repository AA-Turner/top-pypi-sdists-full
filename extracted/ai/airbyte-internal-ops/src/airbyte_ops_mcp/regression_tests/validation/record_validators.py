# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Record schema and incremental cursor checks for regression reads."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

_MASKED_TYPE = re.compile(r"^(string|integer|number|boolean|array|object)_")
_MASKED_UNKNOWN = re.compile(r"^unknown_")
_EXCLUDED_STATE_KEYS = frozenset({"partition", "parent_state"})
_MAX_OBSERVED_FIELDS = 32


@dataclass(frozen=True)
class RecordSchemaResult:
    records_checked: int
    mismatched_records: int
    mismatches_by_field: dict[str, int]
    observed_types_by_field: dict[str, tuple[str, ...]]
    undeclared_field_records: int


@dataclass(frozen=True)
class CursorResult:
    records: int
    null_cursor_records: int
    state_present: bool
    state_has_cursor_value: bool
    state_below_max: bool | None
    strict_failed: bool
    cursor_key_not_found: bool = False


def observed_type(value: Any, *, masked: bool) -> str:
    """Return the JSON-level type represented by a raw value or mask token."""
    if masked and isinstance(value, str):
        token_type = _MASKED_TYPE.match(value)
        if token_type:
            return token_type.group(1)
        if _MASKED_UNKNOWN.match(value):
            return "unknown"

    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "integer" if value.is_integer() else "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "unknown"


def declared_types(node: Any) -> frozenset[str] | None:
    """Return a property's declared type union, or `None` when unconstrained."""
    if not isinstance(node, dict):
        return None
    raw_type = node.get("type")
    if raw_type is None:
        return None
    if isinstance(raw_type, str):
        return frozenset({raw_type})
    if isinstance(raw_type, list):
        return frozenset(value for value in raw_type if isinstance(value, str))
    return None


def _type_is_allowed(observed: str, declared: frozenset[str] | None) -> bool:
    return (
        declared is None
        or observed == "unknown"
        or observed in declared
        or (observed == "integer" and "number" in declared)
    )


def check_record_schema(
    records: Iterable[dict], json_schema: dict, *, masked: bool
) -> RecordSchemaResult:
    """Check top-level property types without retaining record values."""
    properties = json_schema.get("properties")
    has_properties = isinstance(properties, dict)
    declared_properties = properties if has_properties else {}
    mismatches_by_field: dict[str, int] = {}
    observed_types: dict[str, set[str]] = {}
    records_checked = 0
    mismatched_records = 0
    undeclared_field_records = 0

    for record in records:
        records_checked += 1
        if not isinstance(record, dict):
            continue

        if has_properties and any(key not in declared_properties for key in record):
            undeclared_field_records += 1

        record_mismatched = False
        for field_name, node in declared_properties.items():
            if not isinstance(field_name, str) or field_name not in record:
                continue
            observed = observed_type(record[field_name], masked=masked)
            declared = declared_types(node)
            if not _type_is_allowed(observed, declared):
                record_mismatched = True
                mismatches_by_field[field_name] = (
                    mismatches_by_field.get(field_name, 0) + 1
                )
                if field_name in observed_types:
                    observed_types[field_name].add(observed)
                elif len(observed_types) < _MAX_OBSERVED_FIELDS:
                    observed_types[field_name] = {observed}

        if record_mismatched:
            mismatched_records += 1

    return RecordSchemaResult(
        records_checked=records_checked,
        mismatched_records=mismatched_records,
        mismatches_by_field=mismatches_by_field,
        observed_types_by_field={
            field_name: tuple(sorted(types))
            for field_name, types in sorted(observed_types.items())
        },
        undeclared_field_records=undeclared_field_records,
    )


def _cursor_value(record: Any, cursor_path: list[str]) -> Any:
    value = record
    for key in cursor_path:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def _state_cursor_values(state: Any, cursor_key: str | None) -> tuple[list[Any], bool]:
    cursor_values: list[Any] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if isinstance(key, str) and (
                    key in _EXCLUDED_STATE_KEYS or key.startswith("__ab_")
                ):
                    continue
                if key == cursor_key:
                    cursor_values.append(child)
                else:
                    walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(state)
    return cursor_values, bool(cursor_values)


def _has_non_null_scalar_leaf(value: Any) -> bool:
    if isinstance(value, dict):
        return any(
            _has_non_null_scalar_leaf(child)
            for key, child in value.items()
            if not (
                isinstance(key, str)
                and (key in _EXCLUDED_STATE_KEYS or key.startswith("__ab_"))
            )
        )
    if isinstance(value, list):
        return any(_has_non_null_scalar_leaf(child) for child in value)
    return value is not None


def _comparable_state_below_max(
    state_values: list[Any], record_values: list[Any]
) -> bool | None:
    if not state_values or not record_values:
        return None
    values = [*state_values, *record_values]
    if all(isinstance(value, int) and not isinstance(value, bool) for value in values):
        return max(state_values) < max(record_values)
    if not all(isinstance(value, str) for value in values):
        return None

    try:
        parsed = [
            datetime.fromisoformat(value.replace("Z", "+00:00")) for value in values
        ]
    except ValueError:
        return None

    awareness = {value.utcoffset() is not None for value in parsed}
    if len(awareness) != 1:
        return None
    parsed_state = parsed[: len(state_values)]
    parsed_records = parsed[len(state_values) :]
    return max(parsed_state) < max(parsed_records)


def check_incremental_cursor(
    records: Iterable[dict],
    cursor_path: list[str],
    final_state: Any,
    *,
    cursor_readable: bool,
    stopped: bool,
) -> CursorResult:
    """Check record cursor presence and whether final state reached the maximum."""
    record_values: list[Any] = []
    record_count = 0
    null_cursor_records = 0
    for record in records:
        record_count += 1
        value = _cursor_value(record, cursor_path)
        if value is None:
            null_cursor_records += 1
        else:
            record_values.append(value)

    state_present = final_state is not None
    cursor_key = cursor_path[-1] if cursor_path else None
    state_values, cursor_key_found = _state_cursor_values(final_state, cursor_key)
    non_null_state_values = [
        value
        for value in state_values
        if value is not None and not isinstance(value, (dict, list))
    ]
    if cursor_key_found:
        state_has_cursor_value = bool(non_null_state_values)
    else:
        state_has_cursor_value = state_present and _has_non_null_scalar_leaf(
            final_state
        )
    cursor_key_not_found = state_present and not cursor_key_found

    state_below_max = None
    if (
        cursor_readable
        and not null_cursor_records
        and len(non_null_state_values) == len(state_values)
        and record_values
    ):
        state_below_max = _comparable_state_below_max(
            non_null_state_values, record_values
        )

    return CursorResult(
        records=record_count,
        null_cursor_records=null_cursor_records,
        state_present=state_present,
        state_has_cursor_value=state_has_cursor_value,
        state_below_max=state_below_max,
        strict_failed=record_count > 0 and not stopped and not state_has_cursor_value,
        cursor_key_not_found=cursor_key_not_found,
    )
