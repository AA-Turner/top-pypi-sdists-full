from __future__ import annotations

import re
from datetime import timedelta
from re import Pattern
from typing import Literal, Mapping, Optional, Tuple, Union

from typing_extensions import TypeAlias

Duration: TypeAlias = Union[str, timedelta, Literal["infinity", "all"]]
"""
Duration is used to describe time periods in natural language.
To specify using natural language, write the count of the unit
you would like, followed by the representation of the unit.

Chalk supports the following units:

 | Signifier | Meaning       |
 | --------- | ------------- |
 | w         | Weeks         |
 | d         | Days          |
 | h         | Hours         |
 | m         | Minutes       |
 | s         | Seconds       |
 | ms        | Milliseconds  |

As well as the special keywords `"infinity"` and `"all"`.

Examples:

| Signifier            | Meaning                           |
| -------------------- | --------------------------------- |
| "10h"                | 10 hours                          |
| "1w 2m"              | 1 week and 2 minutes              |
| "1h 10m 2s"          | 1 hour, 10 minutes, and 2 seconds |
| "infinity" and "all" | Unbounded time duration           |
"""

CronTab: TypeAlias = str
"""
A schedule defined using the Unix-cron
string format (`* * * * *`).
Values are given in the order below:


| Field        | Values |
| ------------ | ------ |
| Minute       | 0-59   |
| Hour         | 0-23   |
| Day of Month | 1-31   |
| Month        | 1-12   |
| Day of Week  | 0-6    |
"""

ScheduleOptions: TypeAlias = Optional[Union[CronTab, Duration, Literal[True]]]
"""The schedule on which to run a resolver.

One of:
- `CronTab`: A Unix-cron string, e.g. `"* * * * *"`.
- `Duration`: A Chalk Duration, e.g. `"2h30m"`.
"""


_kwarg_to_regex: Mapping[str, Pattern] = {
    timedelta_kwarg: re.compile(rf"(([0-9]+?){abbreviation}(?![a-z]))")
    for timedelta_kwarg, abbreviation in dict(
        weeks="w",
        days="d",
        hours="h",
        minutes="m",
        seconds="s",
        milliseconds="ms",
    ).items()
}


def _parse(s: str, regex: Pattern) -> Tuple[int, str]:
    matched = regex.search(s)
    if matched is None:
        return 0, ""

    return int(matched.groups()[1]), matched.groups()[0]


CHALK_MAX_TIMEDELTA = timedelta(days=100 * 365)
"""The maximum duration supported that can be represented in an int64_t in nanoseconds, rounded down to a nice number."""


def parse_chalk_duration_s(s: str | timedelta | int | Literal["infinity"]) -> int:
    return int(parse_chalk_duration(s).total_seconds())


def parse_chalk_duration(s: str | timedelta | int | Literal["infinity", "all"]) -> timedelta:
    """Parses any form of Chalk duration into a timedelta.

    If conversion fails, a value error is raised with a friendly error message the as the only arg.
    """
    if isinstance(s, timedelta):
        return s
    elif isinstance(s, int):
        return CHALK_MAX_TIMEDELTA if s >= CHALK_MAX_TIMEDELTA.total_seconds() else timedelta(seconds=s)
    elif s == "infinity" or s == "all":
        return CHALK_MAX_TIMEDELTA

    if not isinstance(s, str):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise ValueError(
            f"Expected a string, timedelta, or integer, but got `{s}`. "
            + "Please use a valid duration, like '10m', '1h', or '1h30m'. "
            + "Read more at https://docs.chalk.ai/api-docs#Duration"
        )

    negative = s.startswith("-")
    s = s.removeprefix("-")

    parsed_values: dict[str, tuple[int, str]] = {k: _parse(s, unit) for k, unit in _kwarg_to_regex.items()}

    # Check for remaining unparsed input
    timedelta_constructor: dict[str, int] = {}
    remainder = s
    for k, v in parsed_values.items():
        remainder = remainder.replace(v[1], "", 1)
        timedelta_constructor[k] = v[0]
    remainder = remainder.strip()

    if remainder != "":
        raise ValueError(
            (
                f"The duration '{s}' contained a component '{remainder}' that could not be parsed. "
                "Please use a valid duration, like '10m', '1h', or '1h30m'. "
                "Read more at https://docs.chalk.ai/api-docs#Duration"
            )
        )

    td = timedelta(**timedelta_constructor)
    return -td if negative else td


def timedelta_to_duration(td: timedelta | int) -> str:
    if isinstance(td, int):
        td = timedelta(seconds=td)

    if td >= CHALK_MAX_TIMEDELTA:
        return "infinity"
    total_seconds = td.total_seconds()
    negative = total_seconds < 0
    total_seconds = abs(total_seconds)
    seconds = int(total_seconds)
    milliseconds = int((total_seconds - seconds) * 1000)
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration = []
    if days > 0:
        duration.append(f"{days}d")
    if hours > 0:
        duration.append(f"{hours}h")
    if minutes > 0:
        duration.append(f"{minutes}m")
    if seconds > 0:
        duration.append(f"{seconds}s")
    if milliseconds > 0:
        duration.append(f"{milliseconds}ms")
    return ("-" if negative else "") + "".join(duration)
