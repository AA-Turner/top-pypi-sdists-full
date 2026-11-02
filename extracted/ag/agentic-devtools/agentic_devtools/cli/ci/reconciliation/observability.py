"""Structured operator reporting for trusted reconciliation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ObservationSlaBreach:
    """SLA breach record for one pull-request record."""

    record_id: str
    breached_interval_seconds: int
    observed_at_utc_z: str


@dataclass(frozen=True)
class OperatorReport:
    """Structured observability report emitted by reconciliation."""

    failures: tuple[dict[str, str], ...]
    stale_records: tuple[dict[str, str], ...]
    invalidations: tuple[dict[str, str], ...]
    lease_conflicts: tuple[dict[str, str], ...]
    retry_exhaustions: tuple[dict[str, str], ...]
    sla_breaches: tuple[ObservationSlaBreach, ...]


def create_operator_report(
    *,
    failures: list[dict[str, str]] | None = None,
    stale_records: list[dict[str, str]] | None = None,
    invalidations: list[dict[str, str]] | None = None,
    lease_conflicts: list[dict[str, str]] | None = None,
    retry_exhaustions: list[dict[str, str]] | None = None,
    sla_breaches: list[ObservationSlaBreach] | None = None,
) -> OperatorReport:
    """Create a structured operator report with immutable tuple payloads."""
    return OperatorReport(
        failures=tuple(failures or []),
        stale_records=tuple(stale_records or []),
        invalidations=tuple(invalidations or []),
        lease_conflicts=tuple(lease_conflicts or []),
        retry_exhaustions=tuple(retry_exhaustions or []),
        sla_breaches=tuple(sla_breaches or []),
    )
