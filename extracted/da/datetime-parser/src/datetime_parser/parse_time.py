from math import ceil, log
import re
from operator import eq, gt, lt
import pendulum

DEFAULT_TIMEVAL_IGNORES = [
        "\d+/\d+$"  # Don't match stuff like 5/67
]


def is_datetime(val, oldest_dt_allowed=None):
    """
    :param val: A string representing a datetime.
    :param oldest_dt_allowed: String of the oldest datetime that is allowed to be parsed. Defaults to 2005
    This can be any standard datetime format supported by pendulum or a relative datetime.
    Relative datetime format:
        For the current time:
            now
        Any other time:
            (+/-)(integer) (milliseconds|seconds|minutes|days|weeks|months|years)
    examples:
        now
        -1 months
        +3 days
        -123 seconds

    :return: a pendulum object for the datetime
    """
    try:
        return ComparisonTimeval.create_timeval(val)
    except InvalidComparisonTimevalError:
        pass

    dt = try_parse_dt(val, return_pend_obj=True, oldest_dt_allowed=oldest_dt_allowed)
    if isinstance(dt, pendulum.DateTime):
        return dt
    return None


def try_parse_dt(value, is_number=False, ignore_dt_formats=None, special_dt_formats=None, oldest_dt_allowed=None,
                 return_pend_obj=False):
    """
            Try to parse a given value into a pendulum object, then return the iso string
            Works with strings and numbers that look like datestamps
            Ignores anything not parsed, returning it without parsing
            Ignores any datetime that is too old (could just be a really big numerical value) (anything past 2005)
            Uses self.special_dt_formats for other formats that could be specific to the data

            Args:
                value: Value to attempt to parse into a datetime
                is_number: Is the value a number and should be treated as a timestamp?
                ignore_dt_formats: List of formats to ignore in parsing, defaults to DEFAULT_TIMEVAL_IGNORES
                special_dt_formats: List of string formats to attempt parsing on for auto DT parsing.
                oldest_dt_allowed: String of the oldest datetime that is allowed to be parsed. Defaults to 2005
                return_pend_obj: Return a pendulum object if parsing is successful, otherwise a string will be returned
            """
    if not (isinstance(value, str) or isinstance(value, int) or isinstance(value, float)):
        return value

    dt = None
    if not ignore_dt_formats:
        ignore_dt_formats = DEFAULT_TIMEVAL_IGNORES

    if not special_dt_formats:
        special_dt_formats = []

    if not oldest_dt_allowed:
        oldest_dt_allowed = pendulum.parse("2005")

    try:
        original_value = value
        value = float(original_value)
        is_number = True
        value = int(original_value)
    except ValueError:
        # Attempt to parse the value as a number, in case it's a string
        pass

    if ignore_dt_formats and not is_number:
        for fmt in ignore_dt_formats:
            if re.match(fmt, value):
                return value  # Ignore format, return value unprocessed

    try:
        if is_number:
            if ceil(log(value, 10)) == 13:
                value = value / 1000.0
            dt = pendulum.from_timestamp(value)
        else:
            dt = pendulum.parse(value, strict=False)
    except Exception:  # Broad exception clause to be picky about dates and parsing errors
        if is_number:  # Can't parse number with format, must be unparsable
            return value

        for fmt in special_dt_formats:  # Try special formats
            try:
                dt = pendulum.from_format(value, fmt)
            except ValueError:
                continue

    if dt:
        diff = oldest_dt_allowed.diff(dt)
        signed_diff = diff.years * (1 if diff.invert else -1)
        if signed_diff <= 0:
            # Difference between datetime and oldest_dt is negative, which means it's oldest_dt+
            if return_pend_obj:
                return dt
            else:
                return dt.to_iso8601_string()
        else:
            # Difference is positive, earlier than oldest_dt, probably not a timestamp
            return value
    else:
        return value  # dt isn't a value


class InvalidComparisonTimevalError(Exception):
    pass


class ComparisonTimeval(object):
    OP_EQ = ""
    OP_GTE = "gte"
    OP_LTE = "lte"
    OP_LT = "lt"
    OP_GT = "gt"

    OP_ORDER = [OP_EQ, OP_LT, OP_LTE, OP_GT, OP_GTE]  # Higher index == higher priority

    ALL_OPS = [
        OP_GTE,
        OP_LTE,
        OP_LT,
        OP_GT,
        OP_EQ  # Always put this last in list, or regex won't work
    ]
    OP_MAP = {  # OP_NAME -> OP func (a, b) -> bool
        OP_EQ: eq,
        OP_GTE: lambda a, b: gt(a, b) or eq(a, b),
        # v1 == v2 --lte-> v2 <= v1
        OP_LTE: lambda a, b: lt(a, b) or eq(a, b),
        OP_LT: lambda a, b: lt(a, b),
        OP_GT: lambda a, b: gt(a, b),
    }
    RELATIVE_OP = {
        "-": "subtract",
        "+": "add"
    }

    def __init__(self, time_val, operator):
        if operator not in self.ALL_OPS:
            raise ValueError("Invalid time.<op>now() operator '{}' Valid operators '{}' use time.now(), time.gtenow(), etc...".format(operator, self.ALL_OPS))
        self.time_val = time_val
        self.op = operator

    def __getattr__(self, item):

        return getattr(self.time_val, item)

    def __eq__(self, other):
        dt = is_datetime(other)
        func = self.OP_MAP[self.op]
        v1 = self.time_val
        v2 = dt
        if isinstance(dt, ComparisonTimeval):
            v2 = dt.time_val

        val = func(v2, v1)

        if isinstance(other, ComparisonTimeval):
            op1 = self.OP_ORDER.index(self.op)
            op2 = self.OP_ORDER.index(other.op)
            opval1 = self.op
            opval2 = other.op

            # v1 = self.time_val
            # v2 = dt.time_val

            val = val or other == self.time_val

        return val

    def __str__(self):
        return str(self.time_val)

    @staticmethod
    def create_timeval(val):
        """
        :param val: A string representing a relative time or comparison timeval
        Relative datetime format:
            For the current time:
                now
            Any other time:
                (+/-)(integer) (milliseconds|seconds|minutes|days|weeks|months|years)
        examples:
            now
            -1 months
            +3 days
            -123 seconds

        comparison timeval format:
            ("lte"|"gte"|"lt"|"gt"|"") now (relative time format)
        examples:
            lte now -2 days

        :return: a pendulum object for the datetime
        """
        if isinstance(val, str):
            val = val.replace(" ", "")
            pat = re.compile(r'^(?:(' + "|".join(ComparisonTimeval.ALL_OPS) + r')now)?(?:(\+|-)([0-9]+)(.+))?$')
            match = pat.match(val)
            match = match.groups() if match is not None else None
            if val == 'now':
                return ComparisonTimeval(pendulum.now(), "")
            elif match and any(match):
                op, fn, timespan_val, timespan_name = match
                op = "" if op is None else op
                dt = pendulum.now()
                if fn:
                    fn_name = ComparisonTimeval.RELATIVE_OP[fn]
                    try:
                        dt = getattr(dt, fn_name)(**{timespan_name: int(timespan_val)})
                    except TypeError as e:
                        raise InvalidComparisonTimevalError(
                            "Invalid time unit '{}'.  must be one of: milliseconds, "
                            "seconds, minutes, days, weeks, months, years".format(timespan_name)
                        )
                return ComparisonTimeval(dt, op)
            else:
                raise InvalidComparisonTimevalError("Invalid value '{}', didn't match timeval regex!".format(val))

        elif isinstance(val, ComparisonTimeval):
            return val
        else:
            raise InvalidComparisonTimevalError("Invalid type for value passed to create_timeval, type: '{}'".format(type(val)))

    @staticmethod
    def to_iso8601_period(compare_val, other_time=None):
        """
        Will return the Absolute value time difference between other_time and the Comparision value.
        i.e. if it's 1/1 and the val is 1/2, the result will be 'P1D'
        and vice versa, if it's 1/2, and the val is 1/1, result will be P1D

        Convert the ComparisonTimeval to ISO 8601 Period format:

        P(x)Y(x)M(x)DT(x)H(x)M(x)S

        Where:

        P is the duration period and is always placed at the beginning of the duration.
        Y is the year
        M is the month
        D is the day
        T is the time designator that preceeds the time components
        H is the hour
        M is the minute
        S is the second
        For example:

        P2Y5M3DT12H30M5S

        Represents a duration of two years, five months, three days, twelve hours, thirty minutes, and five seconds.

        And:
        P30D
        Is a period of 30 days

        Args:
            other_time: Other time to compare against, instead of now()

        Returns:
            String value for this ComparisonTimeval
        """
        if other_time is None:
            other_time = pendulum.now()
        diff = other_time.diff(compare_val.time_val)
        times = ["years", "months", "days", "TIME", "hours", "minutes", "seconds"]

        iso_str = "P"

        for time in times:
            if time == "TIME":
                iso_str += "T"
                continue
            # Use internal timedelta for correct vals
            val = getattr(diff._delta, time)
            if val == 0:
                continue
            else:
                iso_str += "{}{}".format(int(val), time[0].upper())

        if iso_str.endswith("T"):
            iso_str = iso_str[:-1]

        if iso_str == "P":
            iso_str = "P0D"

        return iso_str
