"""Unit tests for context injection records and trace event_detail serialization."""

from __future__ import annotations

from datetime import datetime

import pytest

from agentic_devtools.orchestration.hierarchy.context import (
    RetentionMetadata,
    retention_metadata,
)


def test_retention_metadata_rejects_negative_days_and_reversed_dates() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        retention_metadata(retention_days=-1)
    with pytest.raises(ValueError, match="precede"):
        RetentionMetadata(
            created_at="2026-01-02T00:00:00+00:00",
            expires_at="2026-01-01T00:00:00+00:00",
        )


def test_retention_metadata_direct_constructor_enforces_limit() -> None:
    with pytest.raises(ValueError, match="30 days"):
        RetentionMetadata(
            created_at="2026-01-01T00:00:00+00:00",
            expires_at="2026-02-02T00:00:00+00:00",
        )


def test_retention_metadata_rejects_invalid_timestamp() -> None:
    with pytest.raises(ValueError, match="invalid retention timestamp"):
        RetentionMetadata(created_at="not-a-date", expires_at="2026-01-01T00:00:00+00:00")


def test_retention_metadata_factory_handles_hold_and_naive_creation_time() -> None:
    """The factory permits held retention beyond 30 days and normalizes naive timestamps."""
    metadata = retention_metadata(created_at=datetime(2026, 1, 1), retention_days=31, incident_hold=True)
    assert metadata.incident_hold
    assert metadata.expires_at.startswith("2026-02-01T00:00:00")


def test_retention_metadata_factory_rejects_extended_retention_without_hold() -> None:
    """The factory rejects retention periods beyond 30 days without an incident hold."""
    with pytest.raises(ValueError, match="30 days"):
        retention_metadata(retention_days=31)


def test_retention_metadata_factory_uses_current_time_when_creation_time_omitted() -> None:
    """The factory creates metadata when no explicit creation timestamp is supplied."""
    metadata = retention_metadata(retention_days=0)
    assert metadata.created_at == metadata.expires_at


def test_retention_metadata_serializes_without_retention_override() -> None:
    """Retention metadata serialization preserves its fields and optional hold flag."""
    metadata = RetentionMetadata(
        created_at="2026-01-01T00:00:00+00:00",
        expires_at="2026-01-02T00:00:00+00:00",
    )
    assert metadata.to_dict() == {
        "created_at": "2026-01-01T00:00:00+00:00",
        "expires_at": "2026-01-02T00:00:00+00:00",
        "incident_hold": False,
    }
