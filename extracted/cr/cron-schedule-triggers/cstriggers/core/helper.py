from datetime import datetime


def dynamic_strp(datestring, date_formats=None):
    """
        Dynamically process a datestring with a list of formats till one works.
    """
    if not date_formats:
        raise ValueError("No list of formats were specified.")

    for date_format in date_formats:
        try:
            return datetime.strptime(datestring, date_format)
        except ValueError:
            continue

    raise ValueError(f"No format values matched {datestring}.")


class DotDict(dict):
    """ dot.notation access to dictionary attributes. """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def constructed_kwargs(keys, values):
    """ Converts 2 lists into a dictionary whom's elements are `dot` accessible. """
    return DotDict(
        dict(
            zip(
                keys,
                values
            )
        )
    )


def cron_dow_to_calendar(cron_values):
    """ Converts a cron index day of week to a calendar index day of week. """

    if type(cron_values) in [str, int]:
        cron_values = [int(cron_values)]

    calendar_days = []

    for value in cron_values:
        calendar_days.append({
            1: 6,
            2: 0,
            3: 1,
            4: 2,
            5: 3,
            6: 4,
            7: 5,
        }[int(value)])

    return list(calendar_days)


def next_unit(unit_name):
    return {
        "minute": "second",
        "second": "hour",
        "hour": "day",
        "day": "month",
        "day_of_week": "month",
        "month": "year",
        "year": None
    }[unit_name]
