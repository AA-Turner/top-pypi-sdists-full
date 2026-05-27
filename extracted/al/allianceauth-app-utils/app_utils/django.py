"""Extending the Django utilities."""

# pylint: disable = unused-import

from typing import List, Optional

from django.apps import apps
from django.contrib.auth.models import Permission, User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.html import format_html

from allianceauth.tests.auth_utils import AuthUtils

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


def add_permissions_to_user_by_name(user: User, permission_names: List[str]):
    permissions = [permission_by_name(p) for p in set(permission_names)]
    return AuthUtils.add_permissions_to_user(permissions, user)


def permission_by_name(perm: str) -> Permission:
    """Return permission specified by qualified name, e.g. `'app_label.codename'`.

    Note that an app can have multiple permissions with the same codename.
    This function will return the first such permission.
    This emulates Django's behavior in permission checks,
    where permission with the same codename are threated as the same permission.
    """
    perm_parts = perm.split(".")
    if len(perm_parts) != 2:
        raise ValueError("Invalid format for permission name")

    p = (
        Permission.objects.filter(
            content_type__app_label=perm_parts[0], codename=perm_parts[1]
        )
        .order_by()
        .first()
    )
    if not p:
        raise ObjectDoesNotExist(f"No permission with the name: {perm}")

    return p
