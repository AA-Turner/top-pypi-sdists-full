from __future__ import annotations

import re
from datetime import timedelta
from typing import Literal, Optional, TypeAlias, Union

from chalk_rs import parse_duration_ms as _rs_parse_duration_ms
from chalk_rs import parse_duration_s as _rs_parse_duration_s
from chalk_rs import seconds_to_duration_string as _rs_seconds_to_duration_string

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


CHALK_MAX_TIMEDELTA = timedelta(days=100 * 365)
"""The maximum duration supported that can be represented in an int64_t in nanoseconds, rounded down to a nice number."""


def parse_chalk_duration_s(s: str | timedelta | int | Literal["infinity"]) -> int:
    if isinstance(s, timedelta):
        return int(s.total_seconds())
    if isinstance(s, int):
        return int(CHALK_MAX_TIMEDELTA.total_seconds()) if s >= CHALK_MAX_TIMEDELTA.total_seconds() else s
    if s.startswith("-"):
        return -_rs_parse_duration_s(s[1:])
    return _rs_parse_duration_s(s)


def parse_chalk_duration(s: str | timedelta | int | Literal["infinity", "all"]) -> timedelta:
    """Parses any form of Chalk duration into a timedelta.

    If conversion fails, a value error is raised with a friendly error message the as the only arg.
    """
    if isinstance(s, timedelta):
        return s
    if isinstance(s, int):
        return CHALK_MAX_TIMEDELTA if s >= CHALK_MAX_TIMEDELTA.total_seconds() else timedelta(seconds=s)

    if not isinstance(s, str):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise ValueError(
            f"Expected a string, timedelta, or integer, but got `{s}`. "
            + "Please use a valid duration, like '10m', '1h', or '1h30m'. "
            + "Read more at https://docs.chalk.ai/api-docs#Duration"
        )

    if s.startswith("-"):
        ms = _rs_parse_duration_ms(s[1:])
        return timedelta(milliseconds=-ms)
    ms = _rs_parse_duration_ms(s)
    return timedelta(milliseconds=ms)


def timedelta_to_duration(td: timedelta | int) -> str:
    if isinstance(td, int):
        td = timedelta(seconds=td)

    return _rs_seconds_to_duration_string(td.total_seconds())


_WINDOWED_FQN_RE = re.compile(r"^(.+?)__(\d+|all)__(@.+)?$")


def translate_windowed_fqn(fqn: str) -> str:
    """Rewrite a windowed FQN like ``ns.feat__86400__`` to ``ns.feat["1d"]``.

    Non-windowed FQNs are returned unchanged.
    """
    m = _WINDOWED_FQN_RE.match(fqn)
    if m is None:
        return fqn
    stem, bucket, version = m.group(1), m.group(2), m.group(3) or ""
    window_str = "all" if bucket == "all" else timedelta_to_duration(int(bucket))
    return f'{stem}["{window_str}"]{version}'
