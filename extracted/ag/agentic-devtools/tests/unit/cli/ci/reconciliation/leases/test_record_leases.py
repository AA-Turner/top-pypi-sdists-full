"""Tests for RecordLeaseManager."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.reconciliation.leases import LeaseConflictError, RecordLeaseManager


def test_acquire_validates_ttl() -> None:
    with pytest.raises(ValueError, match="ttl_seconds"):
        RecordLeaseManager().acquire(
            existing=None,
            record_id="r1",
            owner="owner",
            acquired_at_utc_z="2026-09-15T12:00:00Z",
            acquired_monotonic_seconds=10,
            ttl_seconds=0,
        )


def test_acquire_rejects_active_conflict() -> None:
    manager = RecordLeaseManager()
    first = manager.acquire(
        existing=None,
        record_id="r1",
        owner="owner",
        acquired_at_utc_z="2026-09-15T12:00:00Z",
        acquired_monotonic_seconds=10,
        ttl_seconds=30,
    )
    with pytest.raises(LeaseConflictError):
        manager.acquire(
            existing=first,
            record_id="r1",
            owner="other",
            acquired_at_utc_z="2026-09-15T12:00:01Z",
            acquired_monotonic_seconds=20,
            ttl_seconds=30,
        )


def test_validate_write_checks_owner_token_and_expiry() -> None:
    manager = RecordLeaseManager()
    lease = manager.acquire(
        existing=None,
        record_id="r1",
        owner="owner",
        acquired_at_utc_z="2026-09-15T12:00:00Z",
        acquired_monotonic_seconds=10,
        ttl_seconds=10,
    )
    assert manager.validate_write(
        lease=lease, owner="owner", fencing_token=lease.fencing_token, current_monotonic_seconds=15
    )
    assert not manager.validate_write(
        lease=lease, owner="other", fencing_token=lease.fencing_token, current_monotonic_seconds=15
    )
    assert not manager.validate_write(lease=lease, owner="owner", fencing_token="bad", current_monotonic_seconds=15)
    assert not manager.validate_write(
        lease=lease, owner="owner", fencing_token=lease.fencing_token, current_monotonic_seconds=25
    )


def test_release_and_expire_update_status() -> None:
    manager = RecordLeaseManager()
    lease = manager.acquire(
        existing=None,
        record_id="r1",
        owner="owner",
        acquired_at_utc_z="2026-09-15T12:00:00Z",
        acquired_monotonic_seconds=10,
        ttl_seconds=10,
    )
    released = manager.release(lease)
    assert released.status.value == "released"
    assert manager.expire(lease).status.value == "expired"
    assert not manager.validate_write(
        lease=released,
        owner="owner",
        fencing_token=released.fencing_token,
        current_monotonic_seconds=11,
    )
