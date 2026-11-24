"""``datetime.local_day`` — "Get a Local Day": today / tomorrow / N days away, in the BUSINESS's own clock.

The other datetime steps are UTC-only, so an owner who wanted "tomorrow's visits" hand-built
``now + 17h`` — right for one zone in one season, and wrong for a run at 10pm local. This step
answers the question the owner actually asked: which calendar day is it where the business is, and
exactly when does that day begin and end.

The zone is, in order: the step's own ``time_zone``; else the ORGANIZATION's zone, read from the
organization the run carries through a host-injected resolver
(:func:`configure_organization_time_zone`; hosted, it reads the ``custom.time_zone`` knob). Neither
set is a plain refusal — never a silent UTC. DST is ``zoneinfo``'s: a spring-forward day is 23 hours
long and a fall-back day 25, and ``start``/``end`` say so.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import UTC, date, datetime, time, timedelta
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.actions import ActionFailed, declare_action
from matrx_graph.types.primitives import ActionTier, NodeCategory

#: ``async (organization_id) -> IANA zone name | None`` — injected by the host.
OrganizationTimeZoneResolver = Callable[[str], Awaitable[str | None]]

_resolver: OrganizationTimeZoneResolver | None = None

NO_TIME_ZONE_MESSAGE = "Set your business's time zone in your organization's Settings (Configuration) to use local days."


def configure_organization_time_zone(resolver: OrganizationTimeZoneResolver | None) -> None:
    """Install (or clear, with ``None``) the host's organization-zone reader."""
    global _resolver
    _resolver = resolver


class LocalDayInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    offset_days: int = Field(
        default=0,
        ge=-3660,
        le=3660,
        description="Which day: 0 is today, 1 is tomorrow, -1 is yesterday.",
    )
    time_zone: str | None = Field(
        default=None,
        description=(
            "A time zone name such as America/Denver. Leave empty to use your business's "
            "time zone from Settings."
        ),
    )
    at: str | None = Field(
        default=None,
        description=(
            "Count from this moment instead of now (an ISO date and time that states its UTC "
            "offset, such as 2026-11-15T05:24:00+00:00). Leave empty for now."
        ),
    )


class LocalDayOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: str = Field(description="The local day, as YYYY-MM-DD.")
    start: str = Field(description="Midnight that begins the day, with its UTC offset.")
    end: str = Field(description="Midnight that begins the NEXT day, with its UTC offset.")
    time_zone: str = Field(description="The time zone the day was worked out in.")


def _midnight(day: date, tz: ZoneInfo) -> datetime:
    """The first instant of ``day`` in ``tz`` (a skipped midnight rolls to the first real moment)."""
    return datetime.combine(day, time.min, tzinfo=tz).astimezone(UTC).astimezone(tz)


def local_day(now: datetime, offset_days: int, tz: ZoneInfo) -> LocalDayOutput:
    """The pure computation: the local day ``offset_days`` from ``now`` in ``tz``."""
    day = now.astimezone(tz).date() + timedelta(days=offset_days)
    return LocalDayOutput(
        date=day.isoformat(),
        start=_midnight(day, tz).isoformat(),
        end=_midnight(day + timedelta(days=1), tz).isoformat(),
        time_zone=tz.key,
    )


def _zone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name.strip())
    except (ZoneInfoNotFoundError, ValueError, OSError):
        raise ActionFailed(
            "invalid_time_zone",
            f"'{name}' is not a time zone name. Use one like America/Denver or Europe/London.",
        ) from None


async def _organization_zone_name(app: Any) -> str | None:
    organization_id = getattr(app, "organization_id", None)
    if not organization_id or _resolver is None:
        return None
    try:
        name = await _resolver(str(organization_id))
    except Exception as exc:  # noqa: BLE001 — an unreadable setting is NOT "not set": say so, never guess
        raise ActionFailed(
            "time_zone_unreadable",
            "Your business's time zone could not be read right now, so the day was not worked out. Try again in a moment.",
            error_type="execution",
        ) from exc
    return name.strip() if isinstance(name, str) and name.strip() else None


@declare_action(
    name="datetime.local_day",
    display_name="Get a Local Day",
    description=(
        "Today, tomorrow or any day, by your business's own clock: the date plus the exact moments "
        "that day begins and ends."
    ),
    category=NodeCategory.DATA,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=LocalDayInput,
    output_schema=LocalDayOutput,
    icon="calendar-days",
    tags=("datetime", "time zone", "day"),
    doors={"step"},
    values_are="deterministic",
)
async def datetime_local_day(app: Any, inputs: LocalDayInput) -> LocalDayOutput:
    name = (inputs.time_zone or "").strip() or await _organization_zone_name(app)
    if not name:
        raise ActionFailed("no_time_zone", NO_TIME_ZONE_MESSAGE)
    tz = _zone(name)
    if inputs.at:
        try:
            moment = datetime.fromisoformat(inputs.at)
        except ValueError:
            raise ActionFailed(
                "invalid_moment", f"'{inputs.at}' is not a date and time. Use a form like 2026-11-15T05:24:00+00:00."
            ) from None
        if moment.utcoffset() is None:
            raise ActionFailed(
                "invalid_moment", "The moment must say its UTC offset, such as +00:00 or -07:00."
            )
    else:
        moment = datetime.now(UTC)
    return local_day(moment, inputs.offset_days, tz)
