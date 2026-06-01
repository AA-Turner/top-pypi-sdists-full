# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Configuration options for live tests.

This module provides configuration classes and enums for controlling
live test behavior, including connection filtering, stream selection,
and test modes.

Based on airbyte-ci implementation:
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/models.py
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/connection_objects_retrieval.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ConnectionSubset(Enum):
    """Signals which connection pool to consider for live tests.

    SANDBOXES: Only use Airbyte sandbox connections (safer, limited data)
    ALL: Use all available connections on Cloud (more coverage, real data)
    """

    SANDBOXES = "sandboxes"
    ALL = "all"

    @classmethod
    def from_string(
        cls,
        value: str,
    ) -> ConnectionSubset:
        """Parse connection subset from string."""
        value_lower = value.lower()
        if value_lower == "sandboxes":
            return cls.SANDBOXES
        if value_lower == "all":
            return cls.ALL
        raise ValueError(
            f"Unknown connection subset: {value}. Must be 'sandboxes' or 'all'."
        )


class TargetOrControl(Enum):
    """Identifies whether a connector is the target or control version."""

    TARGET = "target"
    CONTROL = "control"


class ActorType(Enum):
    """Type of connector actor."""

    SOURCE = "source"
    DESTINATION = "destination"


@dataclass
class LiveTestConfig:
    """Configuration for live test execution.

    This class consolidates all configuration options for running live tests,
    including connection filtering, stream selection, and test behavior.
    """

    # Connection filtering
    connection_id: str | None = None
    connection_subset: ConnectionSubset = ConnectionSubset.SANDBOXES
    max_connections: int | None = None
    auto_select_connections: bool = False

    # Stream filtering
    selected_streams: set[str] | None = None

    # Custom paths for local testing
    custom_config_path: Path | None = None
    custom_catalog_path: Path | None = None
    custom_state_path: Path | None = None

    # Test behavior
    test_description: str | None = None
    retrieval_reason: str | None = None

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.connection_id and self.auto_select_connections:
            raise ValueError(
                "Cannot set both connection_id and auto_select_connections"
            )


@dataclass
class StreamFilter:
    """Filter for selecting which streams to test.

    Provides utilities for filtering streams based on include/exclude patterns.
    """

    include_streams: set[str] | None = None
    exclude_streams: set[str] | None = None

    def filter_streams(
        self,
        available_streams: set[str],
    ) -> set[str]:
        """Filter available streams based on include/exclude rules.

        If include_streams is set, only those streams are included.
        If exclude_streams is set, those streams are removed from the result.
        """
        if self.include_streams:
            result = available_streams & self.include_streams
        else:
            result = available_streams.copy()

        if self.exclude_streams:
            result = result - self.exclude_streams

        return result

    def matches(
        self,
        stream_name: str,
    ) -> bool:
        """Check if a stream name matches the filter."""
        if self.include_streams and stream_name not in self.include_streams:
            return False
        return not (self.exclude_streams and stream_name in self.exclude_streams)


@dataclass
class ConnectionCandidate:
    """Represents a candidate connection for testing.

    Used when auto-selecting connections to test based on stream coverage
    and sync duration.
    """

    connection_id: str
    workspace_id: str | None = None
    streams_with_data: list[str] = field(default_factory=list)
    last_sync_duration_seconds: float | None = None

    @property
    def stream_count(self) -> int:
        return len(self.streams_with_data)


def select_best_connection_candidates(
    candidates: list[ConnectionCandidate],
    max_connections: int | None = None,
) -> list[tuple[ConnectionCandidate, list[str]]]:
    """Select the best subset of connection candidates for testing.

    This function reduces the list of candidates to minimize the number of
    connections while maximizing stream coverage. It prioritizes faster
    connections (shorter sync duration).

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/connection_objects_retrieval.py#L201-L220
    """
    # Sort by sync duration (faster first)
    sorted_candidates = sorted(
        candidates,
        key=lambda c: c.last_sync_duration_seconds or float("inf"),
    )

    tested_streams: set[str] = set()
    selected: list[tuple[ConnectionCandidate, list[str]]] = []

    for candidate in sorted_candidates:
        streams_to_test = []
        for stream in candidate.streams_with_data:
            if stream not in tested_streams:
                streams_to_test.append(stream)
                tested_streams.add(stream)

        if streams_to_test:
            selected.append((candidate, streams_to_test))

    # Sort by number of streams (most streams first)
    selected = sorted(selected, key=lambda x: len(x[1]), reverse=True)

    # Apply max_connections limit
    if max_connections:
        selected = selected[:max_connections]

    return selected
