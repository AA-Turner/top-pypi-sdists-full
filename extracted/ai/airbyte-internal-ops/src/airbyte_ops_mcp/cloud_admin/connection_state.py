# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Shared connection state operations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Protocol

from airbyte.cloud._connection_state import (
    ConnectionStateResponse,
    StreamState,
)
from airbyte.cloud.connections import CloudConnection
from airbyte.exceptions import (
    AirbyteConnectionSyncActiveError,
    PyAirbyteInputError,
)
from pydantic import BaseModel, Field


@dataclass(frozen=True)
class ConfiguredStream:
    """A configured connection stream."""

    name: str
    namespace: str | None


class StreamConfigEntry(Protocol):
    """Configured stream entry with source name and namespace."""

    name: str
    namespace: str | None


class ResetStreamResult(BaseModel):
    """Result of resetting a single stream's state."""

    connection_id: str = Field(description="The connection ID that was updated.")
    stream_name: str = Field(description="The stream whose state was reset.")
    stream_namespace: str | None = Field(
        default=None,
        description="The stream namespace, if one was provided.",
    )
    reset_performed: bool = Field(
        description="Whether a state write was performed.",
    )
    message: str = Field(description="Human-readable result message.")
    previous_state_backup: dict[str, Any] = Field(
        description="Raw Config API state before the reset, suitable for restore."
    )


def reset_stream_state(
    conn: CloudConnection,
    *,
    stream_name: str,
    stream_namespace: str | None,
) -> ResetStreamResult:
    """Reset a configured stream's state and return the previous state backup."""
    _validate_stream_configured(
        conn,
        stream_name=stream_name,
        stream_namespace=stream_namespace,
    )

    previous_state = conn.dump_raw_state(normalize=False)
    current = ConnectionStateResponse(**previous_state)
    if current.state_type == "not_set":
        return ResetStreamResult(
            connection_id=conn.connection_id,
            stream_name=stream_name,
            stream_namespace=stream_namespace,
            reset_performed=False,
            message=(
                "Connection state is not set; stream will already full-refresh "
                "on the next sync."
            ),
            previous_state_backup=previous_state,
        )

    try:
        conn.set_stream_state(
            stream_name=stream_name,
            state_blob_dict={},
            stream_namespace=stream_namespace,
        )
    except PyAirbyteInputError:
        if current.state_type != "legacy":
            raise
        replacement_state = _make_empty_stream_state(
            connection_id=conn.connection_id,
            stream_name=stream_name,
            stream_namespace=stream_namespace,
        )
        try:
            conn.import_raw_state(replacement_state)
        except AirbyteConnectionSyncActiveError:
            raise
        return ResetStreamResult(
            connection_id=conn.connection_id,
            stream_name=stream_name,
            stream_namespace=stream_namespace,
            reset_performed=True,
            message=(
                "Connection had legacy state. The entire state was replaced with "
                "new stream state; all streams will full-refresh on the next sync."
            ),
            previous_state_backup=previous_state,
        )

    return ResetStreamResult(
        connection_id=conn.connection_id,
        stream_name=stream_name,
        stream_namespace=stream_namespace,
        reset_performed=True,
        message="Stream state reset. The stream will full-refresh on the next sync.",
        previous_state_backup=previous_state,
    )


def _stream_identifier(stream: ConfiguredStream) -> str:
    if stream.namespace is None:
        return stream.name
    return f"{stream.namespace}.{stream.name}"


def _configured_streams(conn: CloudConnection) -> list[ConfiguredStream]:
    try:
        connection_info = conn._fetch_connection_info()
        streams = connection_info.configurations.streams or []
    except AttributeError:
        return [
            ConfiguredStream(name=name, namespace=None) for name in conn.stream_names
        ]

    return _configured_streams_from_entries(streams)


def _configured_streams_from_entries(
    streams: Iterable[StreamConfigEntry],
) -> list[ConfiguredStream]:
    return [
        ConfiguredStream(name=stream.name, namespace=stream.namespace)
        for stream in streams
    ]


def _validate_stream_configured(
    conn: CloudConnection,
    *,
    stream_name: str,
    stream_namespace: str | None,
) -> None:
    configured_streams = _configured_streams(conn)
    matching_by_name = [
        stream for stream in configured_streams if stream.name == stream_name
    ]
    matching = [
        stream
        for stream in matching_by_name
        if (stream.namespace or None) == (stream_namespace or None)
    ]
    if matching:
        return

    valid_streams = [_stream_identifier(stream) for stream in configured_streams]
    if matching_by_name:
        valid_namespaces = sorted(
            stream.namespace or "<none>" for stream in matching_by_name
        )
        raise PyAirbyteInputError(
            message="Stream namespace is not configured for this connection.",
            context={
                "stream_name": stream_name,
                "stream_namespace": stream_namespace,
                "valid_namespaces": valid_namespaces,
            },
        )

    raise PyAirbyteInputError(
        message="Stream is not configured for this connection.",
        context={
            "stream_name": stream_name,
            "valid_streams": valid_streams,
        },
    )


def _make_empty_stream_state(
    *,
    connection_id: str,
    stream_name: str,
    stream_namespace: str | None,
) -> dict[str, Any]:
    stream_state = StreamState(
        streamDescriptor={
            "name": stream_name,
            **({"namespace": stream_namespace} if stream_namespace else {}),
        },
        streamState={},
    )
    connection_state = ConnectionStateResponse.model_construct(
        state_type="stream",
        connection_id=connection_id,
        stream_state=[stream_state],
    )
    return connection_state.model_dump(by_alias=True, exclude_none=True)
