"""Pydantic models for the Flowtask Maintenance / Status service.

These models are intentionally free of any heavy Flowtask imports so they can
be reused (and unit-tested) in isolation. They back three SOC2 CC8-related
surfaces:

* :class:`StatusReport` — the health/status page payload.
* :class:`MaintenanceWindow` — a scheduled maintenance window.
* :class:`ChangelogEntry` — a single "what's new" changelog release.
"""
from __future__ import annotations

import enum
from datetime import date, datetime, time, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


def _utcnow() -> datetime:
    """Return a timezone-aware UTC ``datetime`` (test/patch friendly)."""
    return datetime.now(timezone.utc)


class ServiceState(str, enum.Enum):
    """Coarse health state for a service or the whole server."""

    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    DOWN = "down"
    MAINTENANCE = "maintenance"


class HealthCheck(BaseModel):
    """Result of a single health probe.

    Attributes:
        name: Stable identifier of the probe (e.g. ``"api:/api/v2/task"``).
        ok: ``True`` when the probe passed.
        detail: Human-readable explanation, useful when ``ok`` is ``False``.
        checked_at: Timestamp when the probe ran (UTC).
    """

    name: str
    ok: bool
    detail: str = ""
    checked_at: datetime = Field(default_factory=_utcnow)

    @property
    def state(self) -> ServiceState:
        """Map the boolean result to a :class:`ServiceState`."""
        return ServiceState.OPERATIONAL if self.ok else ServiceState.DOWN


class StatusReport(BaseModel):
    """Aggregated status of the server for the status page.

    Attributes:
        service: Logical service/application name.
        version: Running Flowtask version.
        environment: Deployment environment (``production``/``staging``/...).
        generated_at: When the report was built (UTC).
        started_at: Server startup time (UTC), used to compute uptime.
        checks: Individual health probes.
        upcoming_windows: Future maintenance windows to advertise.
    """

    service: str = "Flowtask"
    version: str = "unknown"
    environment: str = "development"
    generated_at: datetime = Field(default_factory=_utcnow)
    started_at: Optional[datetime] = None
    checks: list[HealthCheck] = Field(default_factory=list)
    upcoming_windows: list["MaintenanceWindow"] = Field(default_factory=list)

    @property
    def uptime_seconds(self) -> Optional[int]:
        """Seconds since ``started_at``; ``None`` when unknown."""
        if self.started_at is None:
            return None
        delta = self.generated_at - self.started_at
        return max(0, int(delta.total_seconds()))

    @property
    def overall(self) -> ServiceState:
        """Overall server state derived from the individual checks/windows.

        A currently-active maintenance window forces ``MAINTENANCE``; a failed
        probe forces ``DEGRADED`` (or ``DOWN`` if every probe failed).
        """
        now = self.generated_at
        if any(w.is_active(now) for w in self.upcoming_windows):
            return ServiceState.MAINTENANCE
        if not self.checks:
            return ServiceState.OPERATIONAL
        failed = [c for c in self.checks if not c.ok]
        if not failed:
            return ServiceState.OPERATIONAL
        if len(failed) == len(self.checks):
            return ServiceState.DOWN
        return ServiceState.DEGRADED

    @property
    def healthy(self) -> bool:
        """``True`` when every probe passed."""
        return all(c.ok for c in self.checks)


class MaintenanceWindow(BaseModel):
    """A scheduled maintenance window (a day plus an hour range).

    Attributes:
        identifier: Stable id (assigned by the store when omitted).
        title: Short summary shown to end users.
        description: Optional longer explanation.
        day: Calendar day of the window.
        start_time: Start of the window (local wall-clock time).
        end_time: End of the window; must be later than ``start_time``.
        created_at: When the window was registered (UTC).
        notify: Whether an email notification should be sent for this window.
    """

    identifier: Optional[str] = None
    title: str = Field(..., min_length=1)
    description: str = ""
    day: date
    start_time: time
    end_time: time
    created_at: datetime = Field(default_factory=_utcnow)
    notify: bool = True

    @field_validator("day", mode="before")
    @classmethod
    def _parse_day(cls, value: object) -> object:
        """Accept ISO date strings as well as ``date`` objects."""
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def _parse_time(cls, value: object) -> object:
        """Accept ``HH:MM``/``HH:MM:SS`` strings as well as ``time`` objects."""
        if isinstance(value, str):
            return time.fromisoformat(value)
        return value

    @model_validator(mode="after")
    def _check_range(self) -> "MaintenanceWindow":
        """Ensure the hour range is non-empty (end strictly after start)."""
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")
        return self

    def starts_at(self) -> datetime:
        """Return the naive ``datetime`` when the window starts."""
        return datetime.combine(self.day, self.start_time)

    def ends_at(self) -> datetime:
        """Return the naive ``datetime`` when the window ends."""
        return datetime.combine(self.day, self.end_time)

    def _as_naive(self, now: datetime) -> datetime:
        """Drop tzinfo from ``now`` so it compares against naive combinations."""
        return now.replace(tzinfo=None) if now.tzinfo is not None else now

    def is_active(self, now: Optional[datetime] = None) -> bool:
        """Whether ``now`` falls inside the window."""
        moment = self._as_naive(now or _utcnow())
        return self.starts_at() <= moment < self.ends_at()

    def is_upcoming(self, now: Optional[datetime] = None) -> bool:
        """Whether the window is active now or starts in the future."""
        moment = self._as_naive(now or _utcnow())
        return self.ends_at() > moment


class FailureRecord(BaseModel):
    """A recorded failure/incident for the audit trail.

    Attributes:
        component: What failed (e.g. ``"startup_job"`` or an API path).
        detail: Description of the failure.
        occurred_at: Timestamp of the failure (UTC).
    """

    component: str
    detail: str = ""
    occurred_at: datetime = Field(default_factory=_utcnow)


class ChangelogEntry(BaseModel):
    """A single changelog release for the "What's New" page.

    Attributes:
        version: Release version/tag (e.g. ``"5.12.7"``).
        released_on: Release date, when known.
        title: Optional release title/name.
        url: Optional link to the release (GitHub, etc.).
        sections: Mapping of category (``Added``/``Fixed``/...) to change lines.
    """

    version: str
    released_on: Optional[date] = None
    title: str = ""
    url: str = ""
    sections: dict[str, list[str]] = Field(default_factory=dict)

    @property
    def is_empty(self) -> bool:
        """``True`` when the entry carries no change lines."""
        return not any(self.sections.values())


# Resolve the forward reference used by :class:`StatusReport`.
StatusReport.model_rebuild()
