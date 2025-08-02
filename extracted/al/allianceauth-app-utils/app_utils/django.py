"""Extending the Django utilities."""

# pylint: disable = unused-import

from typing import Optional

from django.apps import apps
from django.contrib.auth.models import Permission, User
from django.db import models
from django.utils.html import format_html

from .app_settings import clean_setting  # noqa: F401 - for backwards compatibility only
from .urls import static_file_absolute_url


def app_labels() -> set:
    """returns set of all current app labels"""
    return set(apps.app_configs.keys())


def users_with_permission(
    permission: Permission, include_superusers=True
) -> models.QuerySet:
    """returns queryset of users that have the given Django permission

    Args:
        permission: required permission
        include_superusers: whether superusers are included in the returned list
    """
    users_qs = (
        permission.user_set.all()
        | User.objects.filter(
            groups__in=list(permission.group_set.values_list("pk", flat=True))
        )
        | User.objects.select_related("profile").filter(
            profile__state__in=list(permission.state_set.values_list("pk", flat=True))
        )
    )
    if include_superusers:
        users_qs |= User.objects.filter(is_superuser=True)
    return users_qs.distinct()


def admin_boolean_icon_html(value) -> Optional[str]:
    """Variation of the admin boolean type, which returns the HTML for creating
    the usual `True` and `False` icons.
    But returns `None` for `None`, instead of the question mark."""

    def make_html(icon_url: str, alt: str) -> str:
        return format_html(f'<img src="{icon_url}" alt="{alt}">')

    if value is True:
        icon_url = static_file_absolute_url("admin/img/icon-yes.svg")
        return make_html(icon_url, "True")

    if value is False:
        icon_url = static_file_absolute_url("admin/img/icon-no.svg")
        return make_html(icon_url, "False")

    return None
