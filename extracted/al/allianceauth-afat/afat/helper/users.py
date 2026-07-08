"""
Helper functions for user queries
"""

# Django
from django.db import models

# Alliance Auth
from allianceauth.authentication.models import Permission, User


def users_with_permission(
    permission: Permission, include_superusers=True
) -> models.QuerySet:
    """
    Returns queryset of users that have the given Django permission

    :param permission:
    :type permission:
    :param include_superusers:
    :type include_superusers:
    :return:
    :rtype:
    """

    users_qs = (
        User.objects.filter(pk__in=permission.user_set.values_list("pk", flat=True))
        | User.objects.filter(
            groups__in=list(permission.group_set.values_list("pk", flat=True))
        )
        | User.objects.select_related("profile").filter(
            profile__state__in=list(permission.state_set.values_list("pk", flat=True))
        )
    )

    if include_superusers:
        users_qs = users_qs | User.objects.filter(is_superuser=True)

    return users_qs.distinct()
