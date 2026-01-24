from datetime import (
    UTC,
)

from dateutil.relativedelta import (
    relativedelta,
)
from fa_purity import (
    Unsafe,
)
from fa_purity.date_time import (
    DatetimeFactory,
    DatetimeUTC,
    RawDatetime,
)

from fluidattacks_etl_utils.date_range import (
    DateRange,
    split_date_range,
)


def _mock_date(month: int, day: int, hour: int) -> DatetimeUTC:
    return (
        DatetimeFactory.new_utc(
            RawDatetime(
                year=2024,
                month=month,
                day=day,
                hour=hour,
                minute=0,
                second=0,
                microsecond=0,
                time_zone=UTC,
            ),
        )
        .alt(Unsafe.raise_exception)
        .to_union()
    )


def _date_range(from_date: DatetimeUTC, to_date: DatetimeUTC) -> DateRange:
    return DateRange.new(from_date, to_date).alt(Unsafe.raise_exception).to_union()


def test_split() -> None:
    _test_range = _date_range(_mock_date(2, 28, 0), _mock_date(3, 2, 12))
    ranges = split_date_range(_test_range, relativedelta(days=1))
    expected = (
        _date_range(_mock_date(2, 28, 0), _mock_date(2, 29, 0)),
        _date_range(_mock_date(2, 29, 0), _mock_date(3, 1, 0)),
        _date_range(_mock_date(3, 1, 0), _mock_date(3, 2, 0)),
        _date_range(_mock_date(3, 2, 0), _mock_date(3, 2, 12)),
    )
    assert ranges.to_list() == expected


def test_split_2() -> None:
    _test_range = _date_range(_mock_date(2, 28, 0), _mock_date(3, 2, 12))
    ranges = split_date_range(_test_range, relativedelta(days=2))
    expected = (
        _date_range(_mock_date(2, 28, 0), _mock_date(3, 1, 0)),
        _date_range(_mock_date(3, 1, 0), _mock_date(3, 2, 12)),
    )
    assert ranges.to_list() == expected


def test_split_3() -> None:
    _test_range = _date_range(_mock_date(2, 28, 0), _mock_date(3, 2, 12))
    ranges = split_date_range(_test_range, relativedelta(days=99))
    assert ranges.to_list() == (_test_range,)
