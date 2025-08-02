"""Utilities related to date and time."""

import datetime as dt

import pytz

from django.utils.translation import gettext_lazy as _

# Default format for output of datetime
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def datetime_round_hour(my_dt: dt.datetime) -> dt.datetime:
    """Rounds given datetime object to nearest hour"""
    return my_dt.replace(
        second=0, microsecond=0, minute=0, hour=my_dt.hour
    ) + dt.timedelta(hours=my_dt.minute // 30)


def dt_eveformat(my_dt: dt.datetime) -> str:
    """converts a datetime to a string in eve format
    e.g. ``2019-06-25T19:04:44``
    """
    my_dt_2 = dt.datetime(
        my_dt.year, my_dt.month, my_dt.day, my_dt.hour, my_dt.minute, my_dt.second
    )
    return my_dt_2.isoformat()


def ldap_time_2_datetime(ldap_dt: int) -> dt.datetime:
    """converts ldap time to datetime.datetime"""
    return pytz.utc.localize(
        dt.datetime.utcfromtimestamp((ldap_dt / 10000000) - 11644473600)
    )


def ldap_timedelta_2_timedelta(ldap_td: int) -> dt.timedelta:
    """converts a ldap time delta into a datetime.timedelta"""
    return dt.timedelta(microseconds=ldap_td / 10)


def timeuntil_str(duration: dt.timedelta, show_seconds=True) -> str:
    """return the duration as nicely formatted string.
    Or empty string if duration is negative.

    Format: ``[[[999y] [99m]] 99d] 99h 99m 99s``
    """
    seconds = int(duration.total_seconds())
    if seconds > 0:
        periods = [
            # Translators: Abbreviation for years
            (_("y"), 60 * 60 * 24 * 365, False, True),
            # Translators: Abbreviation for months
            (_("mt"), 60 * 60 * 24 * 30, False, True),
            # Translators: Abbreviation for days
            (_("d"), 60 * 60 * 24, False, True),
            # Translators: Abbreviation for hours
            (_("h"), 60 * 60, True, True),
            # Translators: Abbreviation for months
            (_("m"), 60, True, True),
            # Translators: Abbreviation for seconds
            (_("s"), 1, True, show_seconds),
        ]
        strings = []
        for period_name, period_seconds, period_static, show in periods:
            if seconds >= period_seconds or period_static:
                period_value, seconds = divmod(seconds, period_seconds)
                if show:
                    strings.append(f"{period_value}{period_name}")

        result = " ".join(strings)
    else:
        result = ""

    return result
