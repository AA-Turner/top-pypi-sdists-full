import calendar
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import List

HOUR_KEY_FORMAT = "%Y-%m-%dT%H"
DAY_KEY_FORMAT = "%Y-%m-%d"
MONTH_KEY_FORMAT = "%Y-%m"


@dataclass(frozen=True, order=True)
class MonthPartition:
    period: str  # YYYY-MM

    @property
    def key(self) -> str:
        return self.period

    @property
    def days(self) -> List["DayPartition"]:
        year, month = int(self.period[:4]), int(self.period[5:7])
        n_days = calendar.monthrange(year, month)[1]
        return [
            DayPartition(date(year, month, d).isoformat()) for d in range(1, n_days + 1)
        ]

    @classmethod
    def from_key(cls, key: str) -> "MonthPartition":
        datetime.strptime(key, MONTH_KEY_FORMAT)
        return cls(period=key)


@dataclass(frozen=True, order=True)
class DayPartition:
    dt: str  # YYYY-MM-DD

    @property
    def key(self) -> str:
        return self.dt

    @property
    def hours(self) -> List["HourPartition"]:
        return [HourPartition(dt=self.dt, hour=h) for h in range(24)]

    @property
    def month(self) -> MonthPartition:
        return MonthPartition(period=self.dt[:7])

    @classmethod
    def from_key(cls, key: str) -> "DayPartition":
        datetime.strptime(key, DAY_KEY_FORMAT)
        return cls(dt=key)


@dataclass(frozen=True, order=True)
class HourPartition:
    dt: str  # YYYY-MM-DD
    hour: int  # 0..23

    @property
    def key(self) -> str:
        return f"{self.dt}T{self.hour:02d}"

    @property
    def start(self) -> datetime:
        base = datetime.strptime(self.dt, DAY_KEY_FORMAT).replace(tzinfo=timezone.utc)
        return base + timedelta(hours=self.hour)

    @property
    def end(self) -> datetime:
        return self.start + timedelta(hours=1)

    @property
    def day(self) -> DayPartition:
        return DayPartition(dt=self.dt)

    @classmethod
    def from_key(cls, key: str) -> "HourPartition":
        parsed = datetime.strptime(key, HOUR_KEY_FORMAT)
        return cls(dt=parsed.strftime(DAY_KEY_FORMAT), hour=parsed.hour)

    @classmethod
    def from_datetime(cls, ts: datetime) -> "HourPartition":
        if ts.tzinfo is None:
            raise ValueError(
                "naive datetime passed to from_datetime — all periodic_analytics "
                "time math is UTC-aware only"
            )
        ts_utc = ts.astimezone(timezone.utc)
        return cls(dt=ts_utc.strftime(DAY_KEY_FORMAT), hour=ts_utc.hour)


def hours_between(start: datetime, end: datetime) -> List[HourPartition]:
    """All complete UTC hours h with start <= h.start and h.end <= end."""
    result: List[HourPartition] = []
    cursor = start.astimezone(timezone.utc).replace(minute=0, second=0, microsecond=0)
    if cursor < start:
        cursor += timedelta(hours=1)
    while cursor + timedelta(hours=1) <= end:
        result.append(HourPartition.from_datetime(cursor))
        cursor += timedelta(hours=1)
    return result


def days_of_period_through(period: str, as_of_date: str) -> List[DayPartition]:
    return [d for d in MonthPartition.from_key(period).days if d.key <= as_of_date]


def hours_of_period_through(
    period: str, as_of_hour: HourPartition
) -> List[HourPartition]:
    """All hours of ``period`` from the 1st 00:00 through ``as_of_hour`` inclusive."""
    if as_of_hour.day.month.key != period:
        raise ValueError(f"as_of_hour {as_of_hour.key!r} is not in period {period!r}")
    hours: List[HourPartition] = []
    for day in MonthPartition.from_key(period).days:
        if day.key > as_of_hour.dt:
            break
        if day.key < as_of_hour.dt:
            hours.extend(day.hours)
        else:
            hours.extend(h for h in day.hours if h.hour <= as_of_hour.hour)
    return hours


def last_hour_of_period(period: str) -> HourPartition:
    last_day = MonthPartition.from_key(period).days[-1]
    return HourPartition(dt=last_day.dt, hour=23)
