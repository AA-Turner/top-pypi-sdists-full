# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the catalogs built for streams a connection does not sync yet."""

from __future__ import annotations

from typing import Any

import pytest

from airbyte_ops_mcp.regression_tests.config_overrides import (
    StreamsNotDiscoveredError,
    build_injected_catalogs,
)

pytestmark = pytest.mark.unit


def _discovered(*streams: dict[str, Any]) -> dict[str, Any]:
    return {"streams": list(streams)}


def _stream(name: str, **fields: Any) -> dict[str, Any]:
    return {
        "name": name,
        "json_schema": {"type": "object"},
        "supported_sync_modes": ["full_refresh"],
        **fields,
    }


def _configured(name: str, sync_mode: str = "incremental") -> dict[str, Any]:
    return {
        "stream": {"name": name, "json_schema": {"type": "object"}},
        "sync_mode": sync_mode,
        "destination_sync_mode": "append",
        "cursor_field": ["updated_at"],
    }


def _names(catalog: dict[str, Any]) -> list[str]:
    return [stream["stream"]["name"] for stream in catalog["streams"]]


def test_a_stream_the_released_version_does_not_discover_is_read_by_the_target_only():
    injection = build_injected_catalogs(
        {"streams": [_configured("users")]},
        {"users", "feedback"},
        _discovered(_stream("users"), _stream("feedback")),
        _discovered(_stream("users")),
    )

    assert injection.new_streams == ("feedback",)
    assert _names(injection.target_catalog) == ["users", "feedback"]
    assert _names(injection.control_catalog) == ["users"]
    assert injection.target_only_streams == ("feedback",)


def test_a_stream_the_released_version_discovers_is_compared_on_both_versions():
    """Absent from the connection but not new: only unselected there (airbyte#85243)."""
    injection = build_injected_catalogs(
        {"streams": [_configured("users")]},
        {"users", "teams"},
        _discovered(_stream("users"), _stream("teams")),
        _discovered(_stream("users"), _stream("teams")),
    )

    assert injection.new_streams == ()
    assert injection.shared_streams == ("teams",)
    assert _names(injection.control_catalog) == ["users", "teams"]
    assert _names(injection.target_catalog) == ["users", "teams"]
    assert injection.target_only_streams == ()


def test_without_the_released_catalog_novelty_is_unknown_and_the_target_reads_alone():
    injection = build_injected_catalogs(
        None,
        {"feedback"},
        _discovered(_stream("feedback")),
        None,
    )

    assert injection.unknown_streams == ("feedback",)
    assert injection.new_streams == ()
    assert _names(injection.control_catalog) == []
    assert injection.target_only_streams == ("feedback",)


def test_a_selected_stream_the_connection_syncs_keeps_the_customers_entry():
    customer_entry = _configured("users")
    injection = build_injected_catalogs(
        {"streams": [customer_entry, _configured("orders")]},
        {"users", "feedback"},
        _discovered(
            _stream("users", supported_sync_modes=["full_refresh"]),
            _stream("feedback"),
        ),
        _discovered(_stream("users")),
    )

    assert injection.target_catalog["streams"][0] == customer_entry
    assert "orders" not in _names(injection.target_catalog)
    assert injection.injected_streams == ("feedback",)


def test_a_selected_stream_the_target_does_not_discover_is_a_setup_error():
    with pytest.raises(StreamsNotDiscoveredError) as raised:
        build_injected_catalogs(
            None,
            {"feedbak"},
            _discovered(_stream("feedback")),
            None,
        )

    assert raised.value.missing == ("feedbak",)
    assert "feedbak" in str(raised.value)
    assert "Discovered: feedback" in str(raised.value)


def test_new_streams_prefer_full_refresh_with_the_source_defined_primary_key():
    injection = build_injected_catalogs(
        None,
        {"feedback"},
        _discovered(
            _stream(
                "feedback",
                supported_sync_modes=["full_refresh", "incremental"],
                default_cursor_field=["updated_at"],
                source_defined_primary_key=[["id"]],
            )
        ),
        _discovered(),
    )

    (entry,) = injection.target_catalog["streams"]
    assert entry["sync_mode"] == "full_refresh"
    assert entry["destination_sync_mode"] == "overwrite"
    assert entry["primary_key"] == [["id"]]
    assert "cursor_field" not in entry
    assert injection.sync_modes == {"feedback": "full_refresh"}


def test_an_incremental_request_uses_the_default_cursor():
    injection = build_injected_catalogs(
        None,
        {"feedback"},
        _discovered(
            _stream(
                "feedback",
                supported_sync_modes=["full_refresh", "incremental"],
                default_cursor_field=["updated_at"],
                source_defined_primary_key=[["id"]],
            )
        ),
        _discovered(),
        sync_mode="incremental",
    )

    (entry,) = injection.target_catalog["streams"]
    assert entry["sync_mode"] == "incremental"
    assert entry["destination_sync_mode"] == "append"
    assert entry["cursor_field"] == ["updated_at"]
    assert injection.notes == ()


def test_an_incremental_request_without_a_cursor_falls_back_and_says_so():
    injection = build_injected_catalogs(
        None,
        {"feedback"},
        _discovered(
            _stream("feedback", supported_sync_modes=["full_refresh", "incremental"])
        ),
        _discovered(),
        sync_mode="incremental",
    )

    assert injection.sync_modes == {"feedback": "full_refresh"}
    (note,) = injection.notes
    assert note.startswith("feedback: read in full refresh")


def test_a_stream_that_only_reads_incrementally_is_configured_incrementally():
    injection = build_injected_catalogs(
        None,
        {"events"},
        _discovered(
            _stream(
                "events",
                supported_sync_modes=["incremental"],
                source_defined_cursor=True,
                default_cursor_field=["created"],
            )
        ),
        _discovered(),
    )

    (entry,) = injection.target_catalog["streams"]
    assert entry["sync_mode"] == "incremental"
    assert entry["cursor_field"] == ["created"]


def test_the_summary_names_streams_only():
    injection = build_injected_catalogs(
        None,
        {"feedback", "teams"},
        _discovered(_stream("feedback"), _stream("teams")),
        _discovered(_stream("teams")),
    )

    assert injection.to_dict() == {
        "new_streams": ["feedback"],
        "shared_streams": ["teams"],
        "unknown_streams": [],
        "kept_target_only": [],
        "sync_modes": {"feedback": "full_refresh", "teams": "full_refresh"},
        "notes": [],
    }


def test_a_configured_stream_the_control_version_does_not_discover_is_kept_from_it():
    """A run without a connection: the catalog comes from the target's DISCOVER."""
    injection = build_injected_catalogs(
        {"streams": [_configured("users"), _configured("feedback", "full_refresh")]},
        {"users", "feedback"},
        _discovered(_stream("users"), _stream("feedback")),
        _discovered(_stream("users")),
    )

    assert injection.kept_target_only == ("feedback",)
    assert injection.new_streams == ()
    assert _names(injection.target_catalog) == ["users", "feedback"]
    assert _names(injection.control_catalog) == ["users"]
    assert injection.target_only_streams == ("feedback",)
    assert injection.changes_anything
    assert injection.to_dict()["kept_target_only"] == ["feedback"]


def test_an_incremental_request_also_configures_a_kept_target_only_stream():
    """A run without a connection: the generated entry would read the PR's new
    stream in full refresh whatever was asked for."""
    generated = {
        "stream": {"name": "feedback", "json_schema": {"type": "object"}},
        "sync_mode": "full_refresh",
        "destination_sync_mode": "overwrite",
    }
    injection = build_injected_catalogs(
        {"streams": [_configured("users"), generated]},
        {"users", "feedback"},
        _discovered(
            _stream("users"),
            _stream(
                "feedback",
                supported_sync_modes=["full_refresh", "incremental"],
                default_cursor_field=["updated_at"],
            ),
        ),
        _discovered(_stream("users")),
        sync_mode="incremental",
    )

    users, feedback = injection.target_catalog["streams"]
    assert users == _configured("users")
    assert feedback["sync_mode"] == "incremental"
    assert feedback["cursor_field"] == ["updated_at"]
    assert injection.sync_modes == {"feedback": "incremental"}
    assert _names(injection.control_catalog) == ["users"]


def test_without_a_sync_mode_a_kept_target_only_stream_keeps_its_entry():
    configured = {"streams": [_configured("users"), _configured("feedback")]}
    injection = build_injected_catalogs(
        configured,
        {"users", "feedback"},
        _discovered(_stream("users"), _stream("feedback")),
        _discovered(_stream("users")),
    )

    assert injection.target_catalog["streams"] == configured["streams"]
    assert injection.sync_modes == {}


def test_configured_streams_stay_on_both_versions_when_the_control_catalog_is_unknown():
    injection = build_injected_catalogs(
        {"streams": [_configured("users"), _configured("feedback")]},
        {"users", "feedback"},
        _discovered(_stream("users"), _stream("feedback")),
        None,
    )

    assert injection.kept_target_only == ()
    assert _names(injection.control_catalog) == ["users", "feedback"]
    assert not injection.changes_anything
