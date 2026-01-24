from collections.abc import Callable
from dataclasses import dataclass
from typing import (
    TypeVar,
)

from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    FrozenList,
    Maybe,
    Result,
    ResultE,
    cast_exception,
)
from fa_purity.date_time import (
    DatetimeFactory,
    DatetimeTZ,
    DatetimeUTC,
)
from fa_purity.json import (
    JsonPrimitiveUnfolder,
    JsonValue,
    Unfolder,
)

_T = TypeVar("_T")


def int_to_str(number: int) -> str:
    return str(number)


def str_to_int(raw: str) -> ResultE[int]:
    try:
        return Result.success(int(raw))
    except ValueError as err:
        return Result.failure(err)


def require_index(items: FrozenList[_T], index: int) -> ResultE[_T]:
    try:
        return Result.success(items[index])
    except IndexError as err:
        return Result.failure(cast_exception(err))


def get_index(items: FrozenList[_T], index: int) -> Maybe[_T]:
    return require_index(items, index).map(lambda v: Maybe.some(v)).value_or(Maybe.empty())


def to_datetime_tz(raw: str) -> ResultE[DatetimeTZ]:
    try:
        _date = isoparse(raw)
        return DatetimeTZ.assert_tz(_date)
    except ValueError as err:
        return Result.failure(err, DatetimeTZ).alt(cast_exception)


def to_datetime_utc(raw: str) -> ResultE[DatetimeUTC]:
    return to_datetime_tz(raw).map(DatetimeFactory.to_utc)


@dataclass(frozen=True)
class DecodeUtils:
    """Common json unfolder aliases/shortcuts."""

    @staticmethod
    def to_str(raw: JsonValue) -> ResultE[str]:
        return Unfolder.to_primitive(raw).bind(JsonPrimitiveUnfolder.to_str)

    @staticmethod
    def to_bool(raw: JsonValue) -> ResultE[bool]:
        return Unfolder.to_primitive(raw).bind(JsonPrimitiveUnfolder.to_bool)

    @staticmethod
    def to_int(raw: JsonValue) -> ResultE[int]:
        return Unfolder.to_primitive(raw).bind(JsonPrimitiveUnfolder.to_int)

    @staticmethod
    def to_date_time(raw: JsonValue) -> ResultE[DatetimeUTC]:
        return Unfolder.to_primitive(raw).bind(JsonPrimitiveUnfolder.to_str).bind(to_datetime_utc)

    @staticmethod
    def to_maybe(
        raw: JsonValue,
        transform: Callable[[JsonValue], ResultE[_T]],
    ) -> ResultE[Maybe[_T]]:
        return (
            Unfolder.extract_maybe(raw)
            .to_result()
            .to_coproduct()
            .map(
                lambda v: transform(v).map(Maybe.some),
                lambda _: Result.success(Maybe.empty()),
            )
        )

    @classmethod
    def to_opt_date_time(cls, raw: JsonValue) -> ResultE[Maybe[DatetimeUTC]]:
        return cls.to_maybe(raw, lambda v: cls.to_str(v).bind(to_datetime_utc))

    @classmethod
    def to_opt_str(cls, raw: JsonValue) -> ResultE[Maybe[str]]:
        return cls.to_maybe(raw, cls.to_str)
