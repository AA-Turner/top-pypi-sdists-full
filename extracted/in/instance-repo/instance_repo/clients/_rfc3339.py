"""Private RFC3339 calendar parser with Python 3.10+ fraction behavior.

Wire values remain untouched at the call sites. Python datetime arithmetic uses
microseconds, matching 3.11+ fromisoformat truncation of finer fractions; expiry
is never rounded up. The original wire precision is not an integrity anchor.
"""
from datetime import datetime, timedelta, timezone
import re

_UTC = re.compile(
    r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})'
    r'(?:\.([0-9]+))?(Z|[+-][0-9]{2}:[0-9]{2})\Z')


def parse_utc(value: str, *, allow_offset: bool = False) -> datetime:
    """Validate calendar fields without version-specific ISO parsing.

    Fraction processing is bounded to six digits, including arbitrarily precise
    values permitted by existing read/write callers. Entries keeps its existing
    one-to-nine-digit and byte bounds before invoking this helper.
    """
    match = _UTC.fullmatch(value) if type(value) is str and type(allow_offset) is bool else None
    if match is None:
        raise ValueError('invalid RFC3339 UTC datetime')
    fraction = match.group(7) or ''
    microsecond = int((fraction[:6] + '000000')[:6])
    suffix = match.group(8)
    hours, minutes = (0, 0) if suffix == 'Z' else (int(suffix[1:3]), int(suffix[4:6]))
    if hours > 23 or minutes > 59 or (not allow_offset and (hours or minutes)):
        raise ValueError('invalid RFC3339 datetime offset')
    offset = (hours * 60 + minutes) * (-1 if suffix.startswith('-') else 1)
    parsed = None
    try:
        parsed = datetime(*(int(match.group(n)) for n in range(1, 7)),
                          microsecond=microsecond, tzinfo=timezone(timedelta(minutes=offset)))
    except ValueError:
        pass
    if parsed is None:
        # Do not attach a calendar exception or raw wire string to the error.
        raise ValueError('invalid RFC3339 UTC calendar datetime')
    return parsed
