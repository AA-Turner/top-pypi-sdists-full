"""
Versioned static URLs to break browser caches when changing the app version.
"""

# Django
from django.template.defaulttags import register
from django.utils.translation import gettext as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth AFAT
from afat import __title__
from afat.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(__name__), prefix=__title__)


@register.filter
def month_name(month_number):
    """
    Template tag :: get month name from month number
    example: {{ event.month|month_name }}

    :param month_number:
    :return:
    """

    month_mapper = {
        1: _("January"),
        2: _("February"),
        3: _("March"),
        4: _("April"),
        5: _("May"),
        6: _("June"),
        7: _("July"),
        8: _("August"),
        9: _("September"),
        10: _("October"),
        11: _("November"),
        12: _("December"),
    }

    return month_mapper[int(month_number)]


@register.filter
def sum_values(dictionary):
    """
    Template tag :: sum all values in a dictionary
    example: {{ dictionary|sum_values }}

    :param dictionary:
    :type dictionary:
    :return:
    :rtype:
    """

    return sum(dictionary.values())
