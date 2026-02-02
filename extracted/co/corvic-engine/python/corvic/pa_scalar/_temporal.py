import datetime
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

from corvic.pa_scalar._const import unit_to_frac_digits, unit_to_seconds


@dataclass
class MonthDayNanoFrac:
    """A duration or interval that also carries its original second precision.

    An alternative for pa.MonthDayNano because pyright thinks pa.MonthDayNano
    should be called like a namedtuple pa.MonthDayNano(month,day,nano) but in
    practice pa.MonthDayNano needs to be called as pa.MonthDayNano((month,day,nano)).
    """

    month: int
    day: int
    nano: int
    second_frac: str | None


# Parse date strings like
# 2012-01-02
_DATE_RE: Final[str] = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"

# Parse time strings like
# 13:01:02
# 13:01:02.1
_TIME_RE: Final[str] = (
    r"(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})(?:\.(?P<second_frac>\d+))?"
)

# Parse time zone strings like
# Z
# +0830
# +08:30
_OFFSET_RE: Final[str] = r"(?P<utc>[zZ])|(?P<tz_hour>[-+]\d{2}):?(?P<tz_minute>\d{2})"

_DATE_TIME_RE: Final[str] = rf"{_DATE_RE}[ tT]{_TIME_RE}(?:{_OFFSET_RE})?"

_DATE_TIME_PAT: Final = re.compile(rf"^{_DATE_TIME_RE}$")

_TIME_PAT: Final = re.compile(rf"^{_TIME_RE}$")

_YEAR_MONTH_DAY_RE: Final[str] = (
    r"(?:(?P<year>\d+)Y)?(?:(?P<month>\d+)M)?(?:(?P<day>\d+)D)?"
)
_HOUR_MINUTE_SECOND_RE: Final[str] = (
    r"(?:(?P<hour>\d+)H)?(?:(?P<minute>\d+)M)?(?:(?P<second>\d+)(?:\.(?P<second_frac>\d+))?S)?"
)

_DURATION_PAT: Final = re.compile(
    rf"^P(?:{_YEAR_MONTH_DAY_RE})?(?:T{_HOUR_MINUTE_SECOND_RE})?$"
)

_LAX_PAT: Final = re.compile(r"^(?P<second>\d+)(?:\.(?P<second_frac>\d+))?[Ss]?$")


def datetime_fromisoformat(s: str) -> datetime.datetime:
    """A datetime.fromisoformat for Python 3.10 and earlier.

    Python 3.11 introduces better datetime parsing and should
    be used instead when earlier versions of Python are not
    required to be supported.
    """
    m = _DATE_TIME_PAT.match(s)
    if not m:
        raise ValueError("invalid ISO 8601 timestamp")
    year = int(m.group("year"))
    month = int(m.group("month"))
    day = int(m.group("day"))
    hour = int(m.group("hour"))
    minute = int(m.group("minute"))
    second = int(m.group("second"))

    microsecond = 0
    second_frac = m.group("second_frac")
    if second_frac:
        padding_for_us = 6 - len(second_frac)
        if padding_for_us > 0:
            second_frac += "0" * padding_for_us
        microsecond = int(second_frac[:6])

    tzinfo = None
    if m.group("utc"):
        tzinfo = datetime.timezone.utc

    tz_hour = m.group("tz_hour")
    if tz_hour:
        delta = datetime.timedelta(
            hours=int(tz_hour), minutes=int(m.group("tz_minute"))
        )
        tzinfo = datetime.timezone(delta)

    return datetime.datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond,
        tzinfo=tzinfo,
    )


def time_fromisoformat(s: str) -> datetime.time:
    """A time.fromisoformat for Python 3.10 and earlier.

    Python 3.11 introduces better datetime parsing and should
    be used instead when earlier versions of Python are not
    required to be supported.
    """
    m = _TIME_PAT.match(s)
    if not m:
        raise ValueError("invalid ISO 8601 time")
    hour = int(m.group("hour"))
    minute = int(m.group("minute"))
    second = int(m.group("second"))

    microsecond = 0
    second_frac = m.group("second_frac")
    if second_frac:
        padding_for_us = 6 - len(second_frac)
        if padding_for_us > 0:
            second_frac += "0" * padding_for_us
        microsecond = int(second_frac[:6])

    return datetime.time(
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond,
    )


def validate_second_frac_resolution(second_frac: str, max_frac_digits: int) -> bool:
    """Return true if the fractional seconds is within the given second resolution."""
    frac_digits = len(second_frac)

    extra_digits = frac_digits - max_frac_digits
    if extra_digits <= 0:
        return True

    # If the extra digits are just zeros, this is also okay
    last_digits = second_frac[-extra_digits:]
    return last_digits.strip("0") == ""


def _seconds_and_frac_to_nano(second: str | None, second_frac: str | None) -> int:
    nano = 0
    if second:
        nano = int(second) * 1_000_000_000

    if second_frac:
        if not validate_second_frac_resolution(second_frac, unit_to_frac_digits("ns")):
            raise ValueError("sub nanosecond resolution not supported")
        frac_digits = len(second_frac)
        nano += int(second_frac + ("0" * (9 - frac_digits)))
    return nano


def month_day_nano_fromisoformat(s: str) -> MonthDayNanoFrac:
    """Parse an ISO 8601 duration into a pa.MonthDayNano."""
    m = _DURATION_PAT.match(s)
    if not m:
        raise ValueError("invalid ISO 8601 duration")

    def add(s: str, fn: Callable[[int], int]) -> int:
        group = m.group(s)
        if not group:
            return 0
        return fn(int(group))

    month = add("year", lambda x: x * 12)
    month += add("month", lambda x: x)
    day = add("day", lambda x: x)
    nano = add("hour", lambda x: 60 * 60 * 1_000_000_000 * x)
    nano += add("minute", lambda x: 60 * 1_000_000_000 * x)

    second_frac = m.group("second_frac") or ""
    nano += _seconds_and_frac_to_nano(m.group("second"), second_frac)

    return MonthDayNanoFrac(month=month, day=day, nano=nano, second_frac=second_frac)


def month_day_nano_fromlaxformat(s: str) -> MonthDayNanoFrac:
    """Parse various conventional representations of a duration into a pa.MonthDayNano.

    Supported formats:
    - ISO 8601 duration ("PT1.2S")
    - Rational number as seconds ("1.2")
    - Rational number followed by S or s as seconds ("1.2s")
    """
    try:
        return month_day_nano_fromisoformat(s)
    except ValueError:
        pass

    m = _LAX_PAT.match(s)
    if not m:
        raise ValueError("invalid duration")

    second_frac = m.group("second_frac") or ""
    nano = _seconds_and_frac_to_nano(m.group("second"), second_frac)

    return MonthDayNanoFrac(month=0, day=0, nano=nano, second_frac=second_frac)


def month_day_nano_toisoformat(mdnf: MonthDayNanoFrac) -> str:
    """Return a pa.MonthDayNano as an ISO 8601 duration string."""
    ret = "P"
    if mdnf.month:
        year, month = divmod(mdnf.month, 12)
        if year:
            ret += f"{year}Y"
        if month:
            ret += f"{month}M"
    if mdnf.day:
        ret += f"{mdnf.day}D"
    if mdnf.nano:
        second, nano = divmod(mdnf.nano, 1_000_000_000)
        minute, second = divmod(second, 60)
        hour, minute = divmod(minute, 60)

        ret += "T"

        if hour:
            ret += f"{hour}H"
        if minute:
            ret += f"{minute}M"
        if second or nano:
            ret += f"{second}"
            if nano:
                ns_str = (f"{nano:09d}").rstrip("0")
                ret += f".{ns_str}"
        ret += "S"

    return ret


def duration_toisoformat(td: datetime.timedelta) -> str:
    # datetime.timedeltas are not leap-second aware, so
    # we will treat them as representing (seconds, microseconds)
    # rather than (days, seconds, microseconds).

    second = td.seconds
    second += td.days * 24 * 60 * 60
    nano = td.microseconds * 1_000
    nano += second * unit_to_seconds("ns")
    return month_day_nano_toisoformat(
        MonthDayNanoFrac(month=0, day=0, nano=nano, second_frac=None)
    )
