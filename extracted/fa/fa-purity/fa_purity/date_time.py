"""Builtin datetime purity patch."""

from __future__ import (
    annotations,
)

from collections.abc import (
    Callable,
)
from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
    timedelta,
    timezone,
)
from typing import (
    TypeVar,
)

from fa_purity._bug import (
    LibraryBug,
)
from fa_purity._core.cmd import (
    Cmd,
)
from fa_purity._core.result import (
    Result,
    ResultE,
    ResultFactory,
)
from fa_purity._core.utils import (
    cast_exception,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class _Private:
    pass


def _handle_overflow(impure: Callable[[], _T]) -> ResultE[_T]:
    factory: ResultFactory[_T, Exception] = ResultFactory()
    try:
        return factory.success(impure())
    except OverflowError as err:
        return factory.failure(err).alt(cast_exception)


def _handle_value_error(impure: Callable[[], _T]) -> ResultE[_T]:
    factory: ResultFactory[_T, Exception] = ResultFactory()
    try:
        return factory.success(impure())
    except ValueError as err:
        return factory.failure(err).alt(cast_exception)


@dataclass(frozen=True, kw_only=True)
class RawDatetime:
    """Raw date-time data."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
    time_zone: timezone | None


def new_datetime(raw: RawDatetime) -> ResultE[datetime]:
    """Build a datetime object with error handling enabled."""

    def _build() -> datetime:
        return datetime(
            year=raw.year,
            month=raw.month,
            day=raw.day,
            hour=raw.hour,
            minute=raw.minute,
            second=raw.second,
            microsecond=raw.microsecond,
            tzinfo=raw.time_zone,
        )

    return _handle_overflow(lambda: _handle_value_error(_build)).bind(lambda r: r)


@dataclass(frozen=True)
class DatetimeTZ:
    """Represents a datetime with a timezone defined."""

    _private: _Private = field(repr=False, hash=False, compare=False)
    date_time: datetime

    @staticmethod
    def assert_tz(time: datetime) -> ResultE[DatetimeTZ]:
        """Build a `DatetimeTZ` from a datetime object."""
        if time.tzinfo is not None:
            return Result.success(DatetimeTZ(_Private(), time))
        err = ValueError("datetime must have a timezone")
        return Result.failure(err, DatetimeTZ).alt(cast_exception)

    def __add__(self, delta: timedelta) -> DatetimeTZ:
        return (
            self.assert_tz(self.date_time + delta)
            .alt(
                lambda _: LibraryBug.new(
                    ValueError("`DatetimeTZ` plus some delta result is missing a timezone"),
                ),
            )
            .to_union()
        )

    def __sub__(self, delta: timedelta) -> DatetimeTZ:
        return (
            self.assert_tz(self.date_time - delta)
            .alt(
                lambda _: LibraryBug.new(
                    ValueError("`DatetimeTZ` plus some delta result is missing a timezone"),
                ),
            )
            .to_union()
        )


@dataclass(frozen=True)
class DatetimeUTC:
    _private: _Private = field(repr=False, hash=False, compare=False)
    date_time: datetime

    @staticmethod
    def assert_utc(time: datetime | DatetimeTZ) -> ResultE[DatetimeUTC]:
        """Build a `DatetimeUTC` from a `datetime` or `DatetimeTZ` object."""
        _time = time if isinstance(time, datetime) else time.date_time
        if _time.tzinfo == UTC:
            return Result.success(DatetimeUTC(_Private(), _time))
        err = ValueError(f"datetime must have UTC timezone but got {_time.tzinfo}")
        return Result.failure(err, DatetimeUTC).alt(cast_exception)

    def __add__(self, delta: timedelta) -> DatetimeUTC:
        return self.assert_utc(self.date_time + delta).alt(LibraryBug.new).to_union()

    def __sub__(self, delta: timedelta) -> DatetimeUTC:
        return self.assert_utc(self.date_time - delta).alt(LibraryBug.new).to_union()


@dataclass(frozen=True)
class DatetimeFactory:
    EPOCH_START: DatetimeUTC = DatetimeUTC.assert_utc(  # noqa: RUF009 # this is inmutable
        datetime.fromtimestamp(0, UTC),
    ).or_else_call(lambda: LibraryBug.new(ValueError("Invalid EPOCH_START")))

    @staticmethod
    def new_utc(raw: RawDatetime) -> ResultE[DatetimeUTC]:
        """Build a `DatetimeUTC`."""
        return new_datetime(raw).map(
            lambda d: DatetimeUTC.assert_utc(d).alt(LibraryBug.new).to_union(),
        )

    @staticmethod
    def new_tz(raw: RawDatetime) -> ResultE[DatetimeTZ]:
        """Build a `DatetimeTZ`."""
        return new_datetime(raw).map(
            lambda d: DatetimeTZ.assert_tz(d).alt(LibraryBug.new).to_union(),
        )

    @staticmethod
    def to_tz(date_time: datetime | DatetimeUTC, time_zone: timezone) -> DatetimeTZ:
        """Transform `datetime` or `DatetimeUTC` into a `DatetimeTZ` of a specified time zone."""
        item = date_time if isinstance(date_time, datetime) else date_time.date_time
        return DatetimeTZ.assert_tz(item.astimezone(time_zone)).alt(LibraryBug.new).to_union()

    @classmethod
    def to_utc(cls, date_time: DatetimeTZ) -> DatetimeUTC:
        """Transform a `DatetimeTZ` into a `DatetimeUTC`."""
        return (
            DatetimeUTC.assert_utc(cls.to_tz(date_time.date_time, UTC))
            .alt(LibraryBug.new)
            .to_union()
        )

    @staticmethod
    def date_now() -> Cmd[DatetimeUTC]:
        """Command to get the current time as a `DatetimeUTC."""

        def _now() -> datetime:
            return datetime.now(UTC)

        return Cmd.wrap_impure(_now).map(
            lambda d: DatetimeUTC.assert_utc(d).or_else_call(lambda: LibraryBug.new(ValueError(d))),
        )
