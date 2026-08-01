# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for merging stream schemas into a configured catalog."""

from __future__ import annotations

import copy
from typing import Any

import pytest

from airbyte_ops_mcp.regression_tests.connection_fetcher import (
    merge_stream_schemas,
    streams_missing_schemas,
)

USERS_SCHEMA = {"type": "object", "properties": {"id": {"type": "integer"}}}
ORDERS_SCHEMA = {"type": "object", "properties": {"total": {"type": "number"}}}


def _configured_stream(name: str, json_schema: dict[str, Any]) -> dict[str, Any]:
    return {
        "stream": {"name": name, "json_schema": json_schema},
        "sync_mode": "full_refresh",
        "destination_sync_mode": "overwrite",
    }


@pytest.mark.parametrize(
    "catalog,schema_source_catalog,expected_schemas,expected_count",
    [
        pytest.param(
            {"streams": [_configured_stream("users", {})]},
            {"streams": [{"stream": {"name": "users", "jsonSchema": USERS_SCHEMA}}]},
            {"users": USERS_SCHEMA},
            1,
            id="merges_platform_camelcase_jsonSchema",
        ),
        pytest.param(
            {"streams": [_configured_stream("users", {})]},
            {"streams": [{"stream": {"name": "users", "json_schema": USERS_SCHEMA}}]},
            {"users": USERS_SCHEMA},
            1,
            id="merges_protocol_snakecase_json_schema",
        ),
        pytest.param(
            {"streams": [_configured_stream("users", USERS_SCHEMA)]},
            {"streams": [{"stream": {"name": "users", "jsonSchema": ORDERS_SCHEMA}}]},
            {"users": USERS_SCHEMA},
            0,
            id="preserves_existing_non_empty_schema",
        ),
        pytest.param(
            {
                "streams": [
                    _configured_stream("users", {}),
                    _configured_stream("orders", {}),
                ]
            },
            {"streams": [{"stream": {"name": "orders", "jsonSchema": ORDERS_SCHEMA}}]},
            {"users": {}, "orders": ORDERS_SCHEMA},
            1,
            id="merges_only_streams_present_in_source",
        ),
        pytest.param(
            {"streams": [_configured_stream("users", {})]},
            {"streams": []},
            {"users": {}},
            0,
            id="empty_source_catalog_merges_nothing",
        ),
        pytest.param(
            {"streams": [_configured_stream("users", {})]},
            {"streams": [{"stream": {"name": "users", "jsonSchema": {}}}]},
            {"users": {}},
            0,
            id="empty_source_schema_is_not_merged",
        ),
        pytest.param(
            {"streams": [{"stream": {"name": "users"}, "sync_mode": "full_refresh"}]},
            {"streams": [{"stream": {"name": "users", "jsonSchema": USERS_SCHEMA}}]},
            {"users": USERS_SCHEMA},
            1,
            id="merges_when_json_schema_key_absent",
        ),
        pytest.param(
            {"streams": [_configured_stream("users", {})]},
            {
                "streams": [
                    {
                        "stream": {
                            "name": "users",
                            "namespace": "public",
                            "jsonSchema": ORDERS_SCHEMA,
                        }
                    },
                    {
                        "stream": {
                            "name": "users",
                            "namespace": "other",
                            "jsonSchema": USERS_SCHEMA,
                        }
                    },
                ]
            },
            {"users": USERS_SCHEMA},
            1,
            id="duplicate_stream_names_last_occurrence_wins_with_warning",
        ),
    ],
)
def test_merge_stream_schemas(
    catalog: dict[str, Any],
    schema_source_catalog: dict[str, Any],
    expected_schemas: dict[str, dict[str, Any]],
    expected_count: int,
) -> None:
    original_catalog = copy.deepcopy(catalog)

    merged_catalog, merged_count = merge_stream_schemas(catalog, schema_source_catalog)

    assert merged_count == expected_count
    result_schemas = {
        configured["stream"]["name"]: configured["stream"]["json_schema"]
        for configured in merged_catalog["streams"]
    }
    assert result_schemas == expected_schemas
    assert catalog == original_catalog, "input catalog must not be mutated"


@pytest.mark.parametrize(
    "source_schemas,expect_warning",
    [
        pytest.param([ORDERS_SCHEMA, USERS_SCHEMA], True, id="differing_dupes_warn"),
        pytest.param([USERS_SCHEMA, USERS_SCHEMA], False, id="identical_dupes_silent"),
    ],
)
def test_merge_stream_schemas_duplicate_warning(
    source_schemas: list[dict[str, Any]],
    expect_warning: bool,
    caplog: pytest.LogCaptureFixture,
) -> None:
    catalog = {"streams": [_configured_stream("users", {})]}
    source = {
        "streams": [
            {"stream": {"name": "users", "jsonSchema": schema}}
            for schema in source_schemas
        ]
    }

    with caplog.at_level("WARNING"):
        merge_stream_schemas(catalog, source)

    warned = any("Duplicate stream name" in rec.message for rec in caplog.records)
    assert warned == expect_warning


@pytest.mark.parametrize(
    "catalog,expected_missing",
    [
        pytest.param(
            {"streams": [_configured_stream("users", USERS_SCHEMA)]},
            [],
            id="no_streams_missing",
        ),
        pytest.param(
            {
                "streams": [
                    _configured_stream("users", USERS_SCHEMA),
                    _configured_stream("orders", {}),
                    {"stream": {"name": "events"}, "sync_mode": "full_refresh"},
                ]
            },
            ["orders", "events"],
            id="empty_and_absent_schemas_reported",
        ),
        pytest.param(
            {"streams": []},
            [],
            id="empty_catalog",
        ),
    ],
)
def test_streams_missing_schemas(
    catalog: dict[str, Any],
    expected_missing: list[str],
) -> None:
    assert streams_missing_schemas(catalog) == expected_missing
