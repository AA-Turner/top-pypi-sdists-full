import re
from datetime import datetime, timezone

# pattern to accept extended ISO 8601 date-time string
_extended_iso_pattern = re.compile(
    r"^(\+\d{5,6}|-\d{4,6})-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}([.]\d+)?(([+-]\d{2}:\d{2})|Z)?$"
)


def valid_utc_datetime(s: str) -> datetime:
    """
    Converts a string into a UTC datetime instance.

    :param s: An ISO 8601 and RFC 3339 compliant timestamp string.
    :returns: A time zone aware datetime instance with time zone UTC.
    """

    # fromisoformat(...) supports military time zone designator "Zulu" to stand for UTC only in Python 3.11 and later
    if s.endswith("Z"):
        # remove time zone suffix "Z" (UTC), parse into naive datetime, and explicitly add time zone designator
        return datetime.fromisoformat(s[:-1]).replace(tzinfo=timezone.utc)
    else:
        # parse as time zone aware datetime directly, and convert to UTC
        return datetime.fromisoformat(s).astimezone(timezone.utc)


def valid_naive_datetime(s: str) -> datetime:
    """
    Converts a string into a naive datetime instance.

    :param s: An ISO 8601 and RFC 3339 compliant timestamp string.
    :returns: A naive datetime instance that is implicitly assumed to be in time zone UTC.
    """

    # fromisoformat(...) supports military time zone designator "Zulu" to stand for UTC only in Python 3.11 and later
    if s.endswith("Z"):
        # remove time zone suffix "Z" (UTC) and parse into naive datetime
        return datetime.fromisoformat(s[:-1])
    else:
        # parse as time zone aware datetime, convert to UTC, and cast to naive datetime
        return datetime.fromisoformat(s).astimezone(timezone.utc).replace(tzinfo=None)


DATETIME_MIN = datetime.min
DATETIME_MAX = datetime.max


def clamp_naive_datetime(s: str) -> datetime:
    """
    Converts a string into a naive datetime instance, clamping dates outside RFC 3339 range.

    :param s: An ISO 8601 timestamp string.
    :returns: A naive datetime instance that is implicitly assumed to be in time zone UTC.
    """

    # check for expansion of the year representation
    if re.match(_extended_iso_pattern, s):
        if s.startswith("+"):
            # clamp at maximum date
            return DATETIME_MAX
        else:
            # clamp at minimum date
            return DATETIME_MIN
    else:
        return valid_naive_datetime(s)
