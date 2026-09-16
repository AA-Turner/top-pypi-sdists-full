"""Per-record lease acquisition and fencing validation."""

from __future__ import annotations

from dataclasses import replace

from agentic_devtools.cli.ci.reconciliation.identifiers import deterministic_id
from agentic_devtools.cli.ci.reconciliation.models import LeaseStatus, RecordLease


class LeaseConflictError(RuntimeError):
    """Raised when an active lease blocks acquisition."""


class RecordLeaseManager:
    """Coordinates durable per-record ownership and fencing tokens."""

    def acquire(
        self,
        *,
        existing: RecordLease | None,
        record_id: str,
        owner: str,
        acquired_at_utc_z: str,
        acquired_monotonic_seconds: float,
        ttl_seconds: float,
    ) -> RecordLease:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be > 0")
        if (
            existing is not None
            and existing.status == LeaseStatus.ACTIVE
            and existing.expires_at_monotonic_seconds > acquired_monotonic_seconds
        ):
            raise LeaseConflictError("active lease already exists")
        fencing_token = deterministic_id(
            "lease", record_id, owner, acquired_at_utc_z, acquired_monotonic_seconds, length=24
        )
        return RecordLease(
            record_id=record_id,
            owner=owner,
            fencing_token=fencing_token,
            acquired_at_utc_z=acquired_at_utc_z,
            acquired_monotonic_seconds=acquired_monotonic_seconds,
            expires_at_monotonic_seconds=acquired_monotonic_seconds + ttl_seconds,
            status=LeaseStatus.ACTIVE,
        )

    def validate_write(
        self,
        *,
        lease: RecordLease,
        owner: str,
        fencing_token: str,
        current_monotonic_seconds: float,
    ) -> bool:
        if lease.status != LeaseStatus.ACTIVE:
            return False
        if lease.owner != owner:
            return False
        if lease.fencing_token != fencing_token:
            return False
        return current_monotonic_seconds <= lease.expires_at_monotonic_seconds

    def release(self, lease: RecordLease) -> RecordLease:
        return replace(lease, status=LeaseStatus.RELEASED)

    def expire(self, lease: RecordLease) -> RecordLease:
        return replace(lease, status=LeaseStatus.EXPIRED)
