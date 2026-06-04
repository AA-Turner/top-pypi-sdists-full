# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("time_val_init",)

__docformat__ = "restructuredtext"

import datetime
import numbers
import time

from tango import TimeVal


def __TimeVal__init(self, a=None, b=None, c=None):
    TimeVal.__init_original(self)
    if a is None:
        return

    if isinstance(a, datetime.datetime):
        assert b is None and c is None
        a = time.mktime(a.timetuple()) + a.microsecond * 1e-6

    if isinstance(a, numbers.Number):
        if b is None:
            self.tv_sec = int(a)
            usec = (a - self.tv_sec) * 1e6
            self.tv_usec = int(usec)
            self.tv_nsec = int((usec - self.tv_usec) * 1e3)
        else:
            self.tv_sec, self.tv_usec, self.tv_nsec = a, b, c


def __TimeVal__totime(self) -> float:
    """
    Returns a float representing this time value

    .. versionadded:: 7.1.0
    """
    return self.tv_sec + 1e-6 * self.tv_usec + 1e-9 * self.tv_nsec


def __TimeVal__todatetime(self) -> datetime.datetime:
    """
    Returns a :class:`datetime.datetime` object representing
    the same time value

    .. versionadded:: 7.1.0
    """
    return datetime.datetime.fromtimestamp(self.totime())


def __TimeVal__fromtimestamp(ts: float) -> TimeVal:
    """
    A static method returning a :class:`tango.TimeVal` object representing
    the given timestamp

    :param ts: a timestamp
    :type ts: float

    .. versionadded:: 7.1.0
    """
    return TimeVal(ts)


def __TimeVal__fromdatetime(dt: datetime.datetime) -> TimeVal:
    """
    A static method returning a :class:`tango.TimeVal` object representing
    the given :class:`datetime.datetime`

    :param dt: a datetime object
    :type dt: :py:obj:`datetime.datetime`

    .. versionadded:: 7.1.0
    """
    return TimeVal(dt)


def __TimeVal__now() -> TimeVal:
    """
    A static method returning a :class:`tango.TimeVal` object representing
    the current time

    .. versionadded:: 7.1.0
    """
    return TimeVal(time.time())


def __TimeVal__strftime(self, format: str) -> str:
    """

    Convert a time value to a string according to a format specification.

    :param format: see the python library reference manual for formatting codes
    :type format: :py:obj:`str`

    .. versionadded:: 7.1.0

    """
    return self.todatetime().strftime(format)


def __TimeVal__isoformat(self, sep: str = "T") -> str:
    """
    Returns a string in ISO 8601 format, YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]

    :param sep: (str) sep is used to separate the year from the time, and defaults to 'T'
    :type sep: :py:obj:`str`

    .. versionadded:: 7.1.0

    .. versionadded:: 7.1.2
        Documented

    .. versionchanged:: 7.1.2
        The `sep` parameter is not mandatory anymore and defaults to 'T' (same as :meth:`datetime.datetime.isoformat`)
    """
    return self.todatetime().isoformat(sep)


def __TimeVal__str__(self) -> str:
    """

    Returns a string representation of TimeVal

    .. versionadded:: 7.1.0
    """
    return str(self.todatetime())


def time_val_init():
    TimeVal.__init_original = TimeVal.__init__
    TimeVal.__init__ = __TimeVal__init
    TimeVal.totime = __TimeVal__totime
    TimeVal.todatetime = __TimeVal__todatetime
    TimeVal.fromtimestamp = staticmethod(__TimeVal__fromtimestamp)
    TimeVal.fromdatetime = staticmethod(__TimeVal__fromdatetime)
    TimeVal.now = staticmethod(__TimeVal__now)
    TimeVal.strftime = __TimeVal__strftime
    TimeVal.isoformat = __TimeVal__isoformat
    TimeVal.__str__ = __TimeVal__str__
