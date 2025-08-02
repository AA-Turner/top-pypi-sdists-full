import datetime as dt

from project.api.schema.common import BaseSO


class DatetimeCommonSO(BaseSO):
    date: dt.date
    datetime: dt.datetime | None = None
    year: int
    month: int
    day: int
    hour: int | None = None
    minute: int | None = None
    second: int | None = None
    microsecond: int | None = None

    @classmethod
    def from_datetime(cls, datetime_: dt.datetime):
        return cls(
            date=datetime_.date(),
            datetime=datetime_,
            year=datetime_.year,
            month=datetime_.month,
            day=datetime_.day,
            hour=datetime_.hour,
            minute=datetime_.minute,
            second=datetime_.second,
            microsecond=datetime_.microsecond
        )

    @classmethod
    def from_date(cls, date_: dt.date):
        return cls(
            date=date_,
            year=date_.year,
            month=date_.month,
            day=date_.day
        )
