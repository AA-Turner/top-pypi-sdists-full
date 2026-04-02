"""
Helper for time related functions
"""

# Django
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy


def get_time_delta(then, now=timezone.now(), interval="default"):
    """
    Returns a duration as specified by variable interval
    functions, except total_duration, returns [quotient, remainder]

    :param then:
    :type then:
    :param now:
    :type now:
    :param interval:
    :type interval:
    :return:
    :rtype:
    """

    duration = now.replace(tzinfo=None) - then.replace(tzinfo=None)
    duration_in_seconds = duration.total_seconds()

    def years():
        """
        Return years

        :return:
        :rtype:
        """

        return divmod(duration_in_seconds, 31536000)  # Seconds in a year = 31536000.

    def days(from_seconds=None):
        """
        Return days

        :param from_seconds:
        :type from_seconds:
        :return:
        :rtype:
        """

        return divmod(
            from_seconds if from_seconds is not None else duration_in_seconds,
            86400,  # Seconds in a day = 86400
        )

    def hours(from_seconds=None):
        """
        Return hours

        :param from_seconds:
        :type from_seconds:
        :return:
        :rtype:
        """

        return divmod(
            from_seconds if from_seconds is not None else duration_in_seconds,
            3600,  # Seconds in an hour = 3600
        )

    def minutes(from_seconds=None):
        """
        Return minutes

        :param from_seconds:
        :type from_seconds:
        :return:
        :rtype:
        """

        return divmod(
            from_seconds if from_seconds is not None else duration_in_seconds,
            60,  # Seconds in a minute = 60
        )

    def seconds(from_seconds=None):
        """
        Return seconds

        :param from_seconds:
        :type from_seconds:
        :return:
        :rtype:
        """

        if from_seconds is not None:
            return divmod(from_seconds, 1)

        return duration_in_seconds

    def total_duration():
        """
        Return total time difference

        :return:
        :rtype:
        """

        duration_years = years()
        duration_days = days(from_seconds=duration_years[1])
        duration_hours = hours(from_seconds=duration_days[1])
        duration_minutes = minutes(from_seconds=duration_hours[1])
        duration_seconds = seconds(from_seconds=duration_minutes[1])

        return _(
            "%(l10n_year)s, %(l10n_day)s, %(l10n_hour)s, %(l10n_minute)s and %(l10n_second)s"
            % {
                "l10n_year": ngettext_lazy(
                    singular="%(count)d year",
                    plural="%(count)d years",
                    number=int(duration_years[0]),
                )
                % {"count": int(duration_years[0])},
                "l10n_day": ngettext_lazy(
                    singular="%(count)d day",
                    plural="%(count)d days",
                    number=int(duration_days[0]),
                )
                % {"count": int(duration_days[0])},
                "l10n_hour": ngettext_lazy(
                    singular="%(count)d hour",
                    plural="%(count)d hours",
                    number=int(duration_hours[0]),
                )
                % {"count": int(duration_hours[0])},
                "l10n_minute": ngettext_lazy(
                    singular="%(count)d minute",
                    plural="%(count)d minutes",
                    number=int(duration_minutes[0]),
                )
                % {"count": int(duration_minutes[0])},
                "l10n_second": ngettext_lazy(
                    singular="%(count)d second",
                    plural="%(count)d seconds",
                    number=int(duration_seconds[0]),
                )
                % {"count": int(duration_seconds[0])},
            }
        )

    return {
        "years": int(years()[0]),
        "days": int(days()[0]),
        "hours": int(hours()[0]),
        "minutes": int(minutes()[0]),
        "seconds": int(seconds()),
        "default": total_duration(),
    }[interval]
