from __future__ import (
    annotations,
)

import inspect
from collections.abc import Iterable
from dataclasses import (
    dataclass,
)
from typing import (
    TypeVar,
)

from dateutil.relativedelta import (
    relativedelta,
)
from fa_purity import (
    Bool,
    Cmd,
    Maybe,
    PureIter,
    PureIterFactory,
    PureIterTransform,
    Unsafe,
    cast_exception,
)
from fa_purity._core.result import (
    Result,
    ResultE,
)
from fa_purity.date_time import (
    DatetimeUTC,
)

from fluidattacks_etl_utils.bug import (
    Bug,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class DateRange:
    @dataclass(frozen=True)
    class _Private:
        pass

    _private: DateRange._Private
    from_date: DatetimeUTC
    to_date: DatetimeUTC

    @staticmethod
    def new(from_date: DatetimeUTC, to_date: DatetimeUTC) -> ResultE[DateRange]:
        if from_date.date_time < to_date.date_time:
            return Result.success(DateRange(DateRange._Private(), from_date, to_date))
        return Result.failure(ValueError("from_date is >= to_date")).alt(cast_exception)


def _append(items: PureIter[_T], item: _T) -> PureIter[_T]:
    def _iter() -> Iterable[_T]:
        yield from items
        yield item

    return Unsafe.pure_iter_from_cmd(Cmd.wrap_impure(_iter))


def split_date_range(
    date_range: DateRange,
    delta: relativedelta,
) -> PureIter[DateRange]:
    @dataclass(frozen=True)
    class _State:
        start: DatetimeUTC
        end_reached: bool

    def _generate(
        state: _State,
    ) -> _State:
        end_candidate = Bug.assume_success(
            "end_candidate",
            inspect.currentframe(),
            (str(state),),
            DatetimeUTC.assert_utc(state.start.date_time + delta),
        )
        if end_candidate.date_time >= date_range.to_date.date_time:
            return _State(date_range.to_date, True)
        return _State(end_candidate, False)

    endpoints: PureIter[DatetimeUTC] = (
        PureIterFactory.infinite_gen(
            _generate,
            _State(date_range.from_date, False),
        )
        .map(lambda s: Maybe.empty(_State) if s.end_reached else Maybe.some(s))
        .transform(lambda x: PureIterTransform.until_empty(x))
        .enumerate(0)
        .map(
            lambda t: Bool.from_primitive(t[0] == 0).map(
                lambda _: Maybe.empty(),
                lambda _: Maybe.some(t[1].start),
            ),
        )
        .transform(PureIterTransform.filter_maybe)
    )
    return _append(endpoints, date_range.to_date).generate(
        lambda s, e: (
            e,
            Bug.assume_success(
                "gen_range",
                inspect.currentframe(),
                (str(s), str(e)),
                DateRange.new(s, e),
            ),
        ),
        date_range.from_date,
    )
