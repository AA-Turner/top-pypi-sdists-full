"""Trusted control-plane clock primitives for reconciliation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol


@dataclass(frozen=True)
class ClockSnapshot:
    """Snapshot containing trusted UTC and monotonic readings."""

    utc_now: datetime
    monotonic_now: float


@dataclass(frozen=True)
class ElapsedReference:
    """Restart-safe persisted anchor used for elapsed-time reconstruction."""

    anchor_utc_z: str
    anchor_monotonic_seconds: float


class TrustedControlPlaneClock(Protocol):
    """Protocol for trusted wall-clock and monotonic time access."""

    def snapshot(self) -> ClockSnapshot: ...  # pragma: no cover

    def now_utc_z(self) -> str: ...  # pragma: no cover


class SystemTrustedControlPlaneClock:
    """Clock implementation backed by system UTC and monotonic time."""

    def snapshot(self) -> ClockSnapshot:
        from time import monotonic

        return ClockSnapshot(utc_now=datetime.now(UTC), monotonic_now=monotonic())

    def now_utc_z(self) -> str:
        return serialize_utc_z(datetime.now(UTC))


class DeterministicTrustedControlPlaneClock:
    """Deterministic clock for tests."""

    def __init__(self, *, utc_now: datetime, monotonic_now: float = 0.0) -> None:
        if utc_now.tzinfo is None:
            raise ValueError("utc_now must be timezone-aware")
        self._utc_now = utc_now.astimezone(UTC)
        self._monotonic_now = monotonic_now

    def snapshot(self) -> ClockSnapshot:
        return ClockSnapshot(utc_now=self._utc_now, monotonic_now=self._monotonic_now)

    def now_utc_z(self) -> str:
        return serialize_utc_z(self._utc_now)

    def advance(self, *, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("seconds must be >= 0")
        from datetime import timedelta

        self._utc_now = self._utc_now + timedelta(seconds=seconds)
        self._monotonic_now += seconds


def serialize_utc_z(value: datetime) -> str:
    """Serialize a timezone-aware datetime as UTC with trailing ``Z``."""
    if value.tzinfo is None:
        raise ValueError("value must be timezone-aware")
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc_z(value: str) -> datetime:
    """Parse a UTC timestamp with trailing ``Z``."""
    if not value.endswith("Z"):
        raise ValueError("timestamp must end with 'Z'")
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def remaining_seconds(*, deadline_utc_z: str, now: ClockSnapshot, anchor: ElapsedReference) -> float | None:
    """Compute remaining seconds using trusted elapsed time reconstruction.

    Returns ``None`` when elapsed-time reconstruction is unavailable.
    """
    deadline = parse_utc_z(deadline_utc_z)
    anchor_utc = parse_utc_z(anchor.anchor_utc_z)
    if now.utc_now < anchor_utc:
        return None
    elapsed_monotonic = now.monotonic_now - anchor.anchor_monotonic_seconds
    if elapsed_monotonic < 0:
        return None
    effective_now = anchor_utc.timestamp() + elapsed_monotonic
    return deadline.timestamp() - effective_now
