"""Unit tests for rolling-window SLO aggregation and alert evaluation (NFR-002, NFR-003)."""

from __future__ import annotations

from datetime import UTC, datetime

from agentic_devtools.orchestration.hierarchy.aggregation import (
    _parse_iso,
)

_NOW = datetime(2026, 6, 15, tzinfo=UTC)


def test_parse_iso_defaults_naive_timestamp_to_utc() -> None:
    parsed = _parse_iso("2026-06-15T00:00:00")
    assert parsed.tzinfo == UTC
