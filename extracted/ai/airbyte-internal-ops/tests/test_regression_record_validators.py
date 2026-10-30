# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for record schema and incremental cursor checks."""

from __future__ import annotations

import pytest
from airbyte_protocol.models import AirbyteCatalog, AirbyteStream

from airbyte_ops_mcp.regression_tests.masking import mask_record_data
from airbyte_ops_mcp.regression_tests.validation.catalog_validators import (
    validate_cursors_exist_in_schema,
    validate_primary_keys_exist_in_schema,
)
from airbyte_ops_mcp.regression_tests.validation.record_validators import (
    _MAX_OBSERVED_FIELDS,
    check_incremental_cursor,
    check_record_schema,
    declared_types,
    observed_type,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, "null"),
        (True, "boolean"),
        (4, "integer"),
        (4.0, "integer"),
        (4.25, "number"),
        ("text", "string"),
        ([], "array"),
        ({}, "object"),
    ],
)
def test_observed_type_raw_values(value, expected):
    assert observed_type(value, masked=False) == expected


@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("string_len-5_hash", "string"),
        ("integer_len-2_hash", "integer"),
        ("number_len-4_hash", "number"),
        ("boolean_len-5_hash", "boolean"),
        ("array_len-2_hash", "array"),
        ("object_len-2_hash", "object"),
        ("unknown_len-4_hash", "unknown"),
    ],
)
def test_observed_type_masked_tokens(token, expected):
    assert observed_type(token, masked=True) == expected


def test_masked_readable_values_use_raw_types():
    assert observed_type(None, masked=True) == "null"
    assert observed_type(3, masked=True) == "integer"
    assert observed_type("2025-01-01", masked=True) == "string"


def test_declared_types_accepts_unions_and_unconstrained_nodes():
    assert declared_types({"type": ["string", "null"]}) == frozenset({"string", "null"})
    assert declared_types({"type": "number"}) == frozenset({"number"})
    assert declared_types({}) is None


def test_record_schema_checks_top_level_types_and_counts_only_undeclared_rows():
    result = check_record_schema(
        [
            {"id": 4, "name": None, "metadata": {"source": "api"}},
            {"id": "wrong", "name": "ok", "extra": "ignored"},
            {"name": "missing id is allowed"},
        ],
        {
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": ["string", "null"]},
                "metadata": {
                    "type": "object",
                    "properties": {"source": {"type": "integer"}},
                },
            }
        },
        masked=False,
    )

    assert result.records_checked == 3
    assert result.mismatched_records == 1
    assert result.mismatches_by_field == {"id": 1}
    assert result.observed_types_by_field == {"id": ("string",)}
    assert result.undeclared_field_records == 1


def test_record_schema_counts_mismatches_beyond_the_observed_type_cap():
    field_count = _MAX_OBSERVED_FIELDS + 1
    properties = {
        f"field_{index:03}": {"type": "integer"} for index in range(field_count)
    }
    record = dict.fromkeys(properties, "wrong")

    result = check_record_schema([record], {"properties": properties}, masked=False)

    assert result.mismatched_records == 1
    assert len(result.mismatches_by_field) == field_count
    assert all(count == 1 for count in result.mismatches_by_field.values())
    assert len(result.observed_types_by_field) == _MAX_OBSERVED_FIELDS


def test_number_accepts_integer_but_null_requires_a_null_union():
    result = check_record_schema(
        [{"count": 2}, {"count": None}],
        {"properties": {"count": {"type": "number"}}},
        masked=False,
    )
    assert result.mismatched_records == 1
    assert result.observed_types_by_field == {"count": ("null",)}


def test_unknown_mask_token_never_fails_a_declared_type():
    result = check_record_schema(
        [{"value": "unknown_len-2_hash"}],
        {"properties": {"value": {"type": "integer"}}},
        masked=True,
    )
    assert result.mismatched_records == 0


def test_nested_objects_are_object_types_in_raw_and_masked_records():
    record = {"nested": {"private": "value"}}
    schema = {"properties": {"nested": {"type": "object"}}}

    assert check_record_schema([record], schema, masked=False).mismatched_records == 0
    masked = mask_record_data(record, key=b"schema-check-key")
    assert observed_type(masked["nested"], masked=True) == "object"
    assert check_record_schema([masked], schema, masked=True).mismatched_records == 0


def test_raw_and_masked_schema_check_results_match():
    records = [
        {
            "id": 4,
            "ratio": 2.0,
            "active": True,
            "name": None,
            "nested": {"private": "value"},
            "items": [1, 2],
        },
        {
            "id": 5,
            "ratio": 2.5,
            "active": False,
            "name": "row",
            "nested": {"private": "another"},
            "items": [],
            "undeclared": "counted",
        },
    ]
    schema = {
        "properties": {
            "id": {"type": "integer"},
            "ratio": {"type": "number"},
            "active": {"type": "boolean"},
            "name": {"type": ["string", "null"]},
            "nested": {"type": "object"},
            "items": {"type": "array"},
        }
    }
    masked_records = [
        mask_record_data(record, key=b"schema-check-key") for record in records
    ]

    assert check_record_schema(records, schema, masked=False) == check_record_schema(
        masked_records, schema, masked=True
    )


def test_incremental_records_without_state_fail_strictly():
    result = check_incremental_cursor(
        [{"updated_at": 3}],
        ["updated_at"],
        None,
        cursor_readable=True,
        stopped=False,
    )
    assert result.records == 1
    assert result.state_present is False
    assert result.strict_failed is True


@pytest.mark.parametrize(
    "state",
    [
        {"updated_at": 3},
        {"states": [{"cursor": {"updated_at": 3}}]},
    ],
)
def test_incremental_state_with_cursor_passes(state):
    result = check_incremental_cursor(
        [{"updated_at": 3}],
        ["updated_at"],
        state,
        cursor_readable=True,
        stopped=False,
    )
    assert result.state_has_cursor_value is True
    assert result.strict_failed is False


def test_sentinel_only_state_fails_strictly():
    result = check_incremental_cursor(
        [{"updated_at": 3}],
        ["updated_at"],
        {"__ab_no_cursor_state_message": True},
        cursor_readable=True,
        stopped=False,
    )
    assert result.state_has_cursor_value is False
    assert result.strict_failed is True


def test_masked_state_cursor_passes_without_comparing_values():
    result = check_incremental_cursor(
        [{"updated_at": "integer_len-1_hash"}],
        ["updated_at"],
        {"updated_at": "integer_len-1_other"},
        cursor_readable=True,
        stopped=False,
    )
    assert result.state_has_cursor_value is True
    assert result.state_below_max is None
    assert result.strict_failed is False


@pytest.mark.parametrize(
    ("state_value", "record_value"),
    [
        (4, 5),
        ("2025-01-01T00:00:00Z", "2025-01-02T00:00:00Z"),
    ],
)
def test_readable_cursor_state_below_record_max_is_diagnostic(
    state_value, record_value
):
    result = check_incremental_cursor(
        [{"updated_at": record_value}],
        ["updated_at"],
        {"updated_at": state_value},
        cursor_readable=True,
        stopped=False,
    )
    assert result.state_below_max is True
    assert result.strict_failed is False


def test_null_or_missing_record_cursor_is_counted():
    result = check_incremental_cursor(
        [{"updated_at": None}, {}],
        ["updated_at"],
        {"updated_at": 4},
        cursor_readable=True,
        stopped=False,
    )
    assert result.records == 2
    assert result.null_cursor_records == 2
    assert result.state_below_max is None


@pytest.mark.parametrize(
    ("records", "stopped"),
    [
        ([{"updated_at": 3}], True),
        ([], False),
    ],
)
def test_stopped_or_zero_record_reads_skip_strict_state_rule(records, stopped):
    result = check_incremental_cursor(
        records,
        ["updated_at"],
        None,
        cursor_readable=True,
        stopped=stopped,
    )
    assert result.strict_failed is False


def test_missing_cursor_key_with_other_scalar_is_diagnostic_and_passes():
    result = check_incremental_cursor(
        [{"updated_at": 3}],
        ["updated_at"],
        {"state_value": "integer_len-1_hash"},
        cursor_readable=False,
        stopped=False,
    )
    assert result.state_has_cursor_value is True
    assert result.cursor_key_not_found is True
    assert result.strict_failed is False


def test_partition_and_parent_state_are_not_cursor_state():
    result = check_incremental_cursor(
        [{"updated_at": 3}],
        ["updated_at"],
        {
            "partition": {"updated_at": 2},
            "parent_state": {"updated_at": 2},
            "__ab_full_refresh_sync_complete": True,
        },
        cursor_readable=True,
        stopped=False,
    )
    assert result.state_has_cursor_value is False
    assert result.strict_failed is True


def test_catalog_primary_key_validator_rejects_a_missing_declared_path():
    stream = AirbyteStream(
        name="audit_logs",
        json_schema={"properties": {"other": {"type": "integer"}}},
        supported_sync_modes=["full_refresh"],
        source_defined_primary_key=[["id"]],
    )

    result = validate_primary_keys_exist_in_schema(AirbyteCatalog(streams=[stream]))

    assert result.passed is False


def test_catalog_cursor_validator_checks_the_configured_cursor_path():
    stream = AirbyteStream(
        name="audit_logs",
        json_schema={"properties": {"default_cursor": {"type": "integer"}}},
        supported_sync_modes=["incremental"],
        default_cursor_field=["default_cursor"],
    )

    result = validate_cursors_exist_in_schema(
        AirbyteCatalog(streams=[stream]),
        cursor_paths_by_stream={"audit_logs": ["configured_cursor"]},
    )

    assert result.passed is False
