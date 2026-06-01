# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for shared connection state operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.cloud_admin.connection_state import reset_stream_state

CONNECTION_ID = "00000000-0000-0000-0000-000000000001"


@dataclass(frozen=True)
class _StreamConfig:
    name: str
    namespace: str | None = None


@dataclass(frozen=True)
class _Configurations:
    streams: list[_StreamConfig]


@dataclass(frozen=True)
class _ConnectionInfo:
    configurations: _Configurations


class _FakeCloudConnection:
    def __init__(
        self,
        *,
        state: dict[str, Any],
        streams: list[_StreamConfig] | None = None,
        set_stream_state_error: Exception | None = None,
    ) -> None:
        self.connection_id = CONNECTION_ID
        self._state = state
        self._streams = streams or [_StreamConfig(name="orders", namespace="public")]
        self._set_stream_state_error = set_stream_state_error
        self.set_stream_state_calls: list[dict[str, Any]] = []
        self.import_raw_state_calls: list[dict[str, Any]] = []

    def _fetch_connection_info(self) -> _ConnectionInfo:
        return _ConnectionInfo(configurations=_Configurations(streams=self._streams))

    def dump_raw_state(self, *, normalize: bool = True) -> dict[str, Any]:
        assert normalize is False
        return self._state

    def set_stream_state(
        self,
        *,
        stream_name: str,
        state_blob_dict: dict[str, Any],
        stream_namespace: str | None = None,
    ) -> None:
        self.set_stream_state_calls.append(
            {
                "stream_name": stream_name,
                "state_blob_dict": state_blob_dict,
                "stream_namespace": stream_namespace,
            }
        )
        if self._set_stream_state_error is not None:
            raise self._set_stream_state_error

    def import_raw_state(self, state: dict[str, Any]) -> None:
        self.import_raw_state_calls.append(state)


@pytest.mark.unit
def test_reset_stream_state_noops_when_state_not_set() -> None:
    state = {"stateType": "not_set", "connectionId": CONNECTION_ID}
    conn = _FakeCloudConnection(state=state)

    result = reset_stream_state(
        conn,
        stream_name="orders",
        stream_namespace="public",
    )

    assert result.reset_performed is False
    assert result.previous_state_backup == state
    assert conn.set_stream_state_calls == []
    assert conn.import_raw_state_calls == []


@pytest.mark.unit
def test_reset_stream_state_clears_stream_state() -> None:
    state = {
        "stateType": "stream",
        "connectionId": CONNECTION_ID,
        "streamState": [
            {
                "streamDescriptor": {"name": "orders", "namespace": "public"},
                "streamState": {"cursor": "2026-01-01"},
            }
        ],
    }
    conn = _FakeCloudConnection(state=state)

    result = reset_stream_state(
        conn,
        stream_name="orders",
        stream_namespace="public",
    )

    assert result.reset_performed is True
    assert (
        result.message
        == "Stream state reset. The stream will full-refresh on the next sync."
    )
    assert conn.set_stream_state_calls == [
        {
            "stream_name": "orders",
            "state_blob_dict": {},
            "stream_namespace": "public",
        }
    ]
    assert conn.import_raw_state_calls == []


@pytest.mark.unit
def test_reset_stream_state_uses_legacy_fallback() -> None:
    state = {
        "stateType": "legacy",
        "connectionId": CONNECTION_ID,
        "state": {"cursor": "2026-01-01"},
    }
    conn = _FakeCloudConnection(
        state=state,
        set_stream_state_error=PyAirbyteInputError(
            message="Cannot set stream state on a legacy-type connection state."
        ),
    )

    result = reset_stream_state(
        conn,
        stream_name="orders",
        stream_namespace="public",
    )

    assert result.reset_performed is True
    assert result.message == (
        "Connection had legacy state. The entire state was replaced with "
        "new stream state; all streams will full-refresh on the next sync."
    )
    assert conn.import_raw_state_calls == [
        {
            "stateType": "stream",
            "connectionId": CONNECTION_ID,
            "streamState": [
                {
                    "streamDescriptor": {"name": "orders", "namespace": "public"},
                    "streamState": {},
                }
            ],
        }
    ]


@pytest.mark.unit
@pytest.mark.parametrize(
    ("stream_name", "stream_namespace", "expected_message"),
    [
        pytest.param(
            "missing",
            "public",
            "Stream is not configured for this connection.",
            id="unknown_stream",
        ),
        pytest.param(
            "orders",
            "wrong",
            "Stream namespace is not configured for this connection.",
            id="wrong_namespace",
        ),
    ],
)
def test_reset_stream_state_rejects_unconfigured_stream(
    stream_name: str,
    stream_namespace: str | None,
    expected_message: str,
) -> None:
    conn = _FakeCloudConnection(
        state={"stateType": "not_set", "connectionId": CONNECTION_ID}
    )

    with pytest.raises(PyAirbyteInputError) as exc_info:
        reset_stream_state(
            conn,
            stream_name=stream_name,
            stream_namespace=stream_namespace,
        )

    assert exc_info.value.message == expected_message
