from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, available_timezones

from dateutil import rrule
from django.utils.dateparse import parse_date
from django.utils.timezone import localdate
from pandas.tseries.offsets import BDay

from wbcore.utils.date_builder import (
    BusinessDay,
    Hour,
    Minute,
    Month,
    MonthEnd,
    MonthStart,
    Now,
    Quarter,
    QuarterEnd,
    QuarterStart,
    Week,
    Year,
    YearStart,
)
from wbcore.utils.date_builder.components import Component


def get_quarter_from_date(d):
    return ((d.month - 1) // 3) + 1


def get_start_date_from_date(d):
    quarter = get_quarter_from_date(d)
    return date(d.year, quarter * 3 - 2, 1)


def get_end_date_from_date(d):
    quarter = get_quarter_from_date(d)
    return date(d.year + ((quarter * 3 + 1) // 12), (quarter * 3 + 1) % 12, 1) - timedelta(days=1)


def get_start_and_end_date_from_date(d):
    return get_start_date_from_date(d), get_end_date_from_date(d)


def current_quarter_date_start(field=None, request=None, view=None):
    return get_start_date_from_date(localdate())


def current_quarter_date_end(field=None, request=None, view=None):
    return get_end_date_from_date(localdate())


def current_quarter_date_interval(field, request, view):
    return (
        current_quarter_date_start(field, request, view),
        current_quarter_date_end(field, request, view),
    )


def financial_year_to_date(field, request, view):
    d = localdate()
    return (date(d.year - 1, 12, 31), d)


def current_year_date_start(field, request, view):
    d = localdate()
    return date(d.year, 1, 1)


def current_year_date_end(field, request, view):
    d = localdate()
    return date(d.year + 1, 1, 1) - timedelta(days=1)


def current_year_date_interval(field, request, view):
    return (
        current_year_date_start(field, request, view),
        current_year_date_end(field, request, view),
    )


def current_month_date_start(field, request, view):
    d = localdate()
    return date(d.year, d.month, 1)


def current_month_date_end(field=None, request=None, view=None):
    d = localdate()
    if d.month == 12:
        return date(d.year, 12, 31)
    return date(d.year, d.month + 1, 1) - timedelta(days=1)


def current_month_date_interval(field, request, view):
    return (
        current_month_date_start(field, request, view),
        current_month_date_end(field, request, view),
    )


def get_date_interval_from_request(
    request,
    request_type="GET",
    exclude_weekend=False,
    left_interval_inclusive=False,
    right_interval_inclusive=True,
    date_range_fieldname="date",
):
    """
    Parses a request and returns the start and end date from it.

    Parameters
    ----------
    request: The GET Request Object
    exclude_weekend: If True, exclude weekend
    left_interval_inclusive: If False, corresponds to left bound excluded "(" otherwise, inclusive "["
    right_interval_inclusive: If False, corresponds to right bound excluded ")" otherwise, inclusive "]"

    Returns
    -------
    Return a tuple in the form of (start_date, end_date). If either the start date or the end date is not present in the request None is returned in the tuple
    """

    start_identifier = ["start", "start_date", "from", "date_gte", "date__gte"]
    end_identifier = ["end", "end_date", "to", "date_lte", "date__lte"]
    params = request.GET if request_type == "GET" else request.POST
    start = None
    end = None
    if date_range_fieldname in params:
        if len(params.get(date_range_fieldname).split(",")) == 2:
            start, end = map(lambda x: None if x == "" else x, params.get(date_range_fieldname).split(","))
    if not start or not end:
        start = next(
            (params.get(identifier) for identifier in start_identifier if identifier in params),
            None,
        )
        end = next((params.get(identifier) for identifier in end_identifier if identifier in params), None)
    if start:
        start = parse_date(start)
        if start and exclude_weekend:
            if left_interval_inclusive:
                start = (start - timedelta(days=1) + BDay(1)).date()
            else:
                start = (start + timedelta(days=1) - BDay(1)).date()
    if end:
        end = parse_date(end)
        if end and exclude_weekend:
            if right_interval_inclusive:
                end = (end + timedelta(days=1) - BDay(1)).date()
            else:
                end = (end - timedelta(days=1) + BDay(1)).date()
    return start, end


def get_number_of_hours_between_dates(
    d1, d2, skip_weekends=True, list_public_holidays=False, hours_range=None, granularity=12
):
    if hours_range is None:
        hours_range = range(0, 23)

    def convert_days_from_hours(hours, granularity, hours_per_day):
        return int(hours / granularity) * granularity / hours_per_day

    rules = rrule.rruleset()

    byweekday_list = [rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR]
    if not skip_weekends:
        byweekday_list.extend([rrule.SA, rrule.SU])

    rules.rrule(
        rrule.rrule(
            freq=rrule.HOURLY,
            byweekday=byweekday_list,
            byhour=hours_range,
            dtstart=d1,
            until=d2,
        )
    )
    if list_public_holidays:
        for holiday in list_public_holidays:
            s1 = datetime(holiday.year, holiday.month, holiday.day, 0, 0, 0)
            s2 = datetime(holiday.year, holiday.month, holiday.day, 23, 59, 59)
            rules.exrule(rrule.rrule(rrule.HOURLY, dtstart=s1, until=s2))
    dates = defaultdict(int)
    for r in list(rules):
        dates[r.date()] += 1
    return {k: convert_days_from_hours(v, granularity, len(hours_range)) for k, v in dates.items()}


def shortcut(label: str, value_start: str | Component, value_end: str | Component) -> dict[str, str]:
    return {"label": label, "value": f"{str(value_start)},{str(value_end)}"}


financial_performance_shortcuts = [
    shortcut("Last Day", Now - BusinessDay, Now),
    shortcut("Last Week", Now - Week - BusinessDay, Now),
    shortcut("Month to Date", MonthStart - BusinessDay, Now),
    shortcut("Last Month", Now - Month - BusinessDay, Now),
    shortcut("Quarter to Date", QuarterStart - BusinessDay, Now),
    shortcut("Last Quarter", Now - Quarter - BusinessDay, Now),
    shortcut("Year to Date", YearStart - BusinessDay, Now),
    shortcut("Last 1 Year", Now - Year - BusinessDay, Now),
    shortcut("Last 2 Years", Now - Year(2) - BusinessDay, Now),
    shortcut("Last 3 Years", Now - Year(3) - BusinessDay, Now),
    shortcut("Last 5 Years", Now - Year(5) - BusinessDay, Now),
]

current_financial_month = MonthStart - BusinessDay, MonthEnd
current_financial_quarter = QuarterStart - BusinessDay, QuarterEnd

calendar_item_shortcuts = [
    shortcut("Last Minute", Now - Minute, Now),
    shortcut("Last 5 Minutes", Now - Minute(5), Now),
    shortcut("Last 10 Minutes", Now - Minute(10), Now),
    shortcut("Last 15 Minutes", Now - Minute(15), Now),
    shortcut("Last 30 Minutes", Now - Minute(30), Now),
    shortcut("Last Hour", Now - Hour, Now),
]


def get_next_day_timedelta(now: datetime | None = None) -> int:
    if not now:
        now = datetime.now()
    return (datetime.combine(now.date() + timedelta(days=1), time(0, 0, 0)) - now).seconds


def get_timezone_choices() -> list[tuple[str, str]]:
    now_utc = datetime.now(timezone.utc)
    tz_tuples = []  # a list of (timezone_name, timezone_name (UTC offset))
    for tz_name in sorted(available_timezones()):
        tz = ZoneInfo(tz_name)
        now_in_tz = now_utc.astimezone(tz)
        offset_str = now_in_tz.strftime("UTC%z")  # gives UTC+HHMM
        offset_str = offset_str[:-2] + ":" + offset_str[-2:]
        tz_tuples.append((tz_name, f"{tz_name} ({offset_str})"))
    return tz_tuples
