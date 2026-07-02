"""App's base definitions"""

from django.apps import AppConfig
from django.utils.text import format_lazy

from memberaudit_securegroups import __title_translated__, __version__


class MemberAuditSecureGroupsConfig(AppConfig):
    name = "memberaudit_securegroups"
    label = "memberaudit_securegroups"
    verbose_name = format_lazy(
        "{app_title} v{version}", app_title=__title_translated__, version=__version__
    )
