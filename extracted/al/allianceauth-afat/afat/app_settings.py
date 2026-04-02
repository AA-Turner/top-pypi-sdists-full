"""
Our app setting
"""

# Standard Library
from re import RegexFlag

# Django
from django.apps import apps
from django.conf import settings


def fittings_installed() -> bool:
    """
    Check if the Fittings module is installed

    :return:
    :rtype:
    """

    return apps.is_installed(app_name="fittings")


def securegroups_installed() -> bool:
    """
    Check if the Alliance Auth Secure Groups module is installed

    :return:
    :rtype:
    """

    return apps.is_installed(app_name="securegroups")


def use_fittings_module_for_doctrines() -> bool:
    """
    Check if the Fittings module is used for doctrines

    :return:
    :rtype:
    """

    # Alliance Auth AFAT
    from afat.models import (  # pylint: disable=import-outside-toplevel, cyclic-import
        Setting,
    )

    return (
        fittings_installed() is True
        and Setting.get_setting(Setting.Field.USE_DOCTRINES_FROM_FITTINGS_MODULE)
        is True
    )


def debug_enabled() -> RegexFlag:
    """
    Check if DEBUG is enabled

    :return:
    :rtype:
    """

    return settings.DEBUG
