"""Unit tests for is_retention_expired."""

from __future__ import annotations

from datetime import UTC, datetime

from agentic_devtools.orchestration.hierarchy.context import (
    RetentionMetadata,
    is_retention_expired,
)


def test_retention_not_expired_when_incident_hold_is_set() -> None:
    metadata = RetentionMetadata(
        created_at="2026-01-01T00:00:00+00:00",
        expires_at="2026-03-01T00:00:00+00:00",
        incident_hold=True,
    )
    assert not is_retention_expired(metadata, now=datetime(2026, 2, 1, tzinfo=UTC))


def test_retention_not_expired_before_deadline() -> None:
    metadata = RetentionMetadata(
        created_at="2026-01-01T00:00:00+00:00",
        expires_at="2026-01-02T00:00:00+00:00",
    )
    assert not is_retention_expired(metadata, now=datetime(2026, 1, 1, tzinfo=UTC))


def test_retention_expiry_normalizes_naive_now() -> None:
    metadata = RetentionMetadata(
        created_at="2026-01-01T00:00:00+00:00",
        expires_at="2026-01-02T00:00:00+00:00",
    )
    assert is_retention_expired(metadata, now=datetime(2026, 1, 3))
