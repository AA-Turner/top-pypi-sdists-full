from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import Q, QuerySet
from django.utils.module_loading import import_string

from wbcore.contrib.authentication.models import User


class UserBackendRegistry:
    def __init__(self):
        internal_users_backend_path = getattr(
            settings, "USER_BACKEND", "wbcore.contrib.permission.internal.backend.UserBackend"
        )
        internal_users_backend_class = import_string(internal_users_backend_path)
        self.backend = internal_users_backend_class()

    def get_internal_groups(self) -> QuerySet[Group]:
        return self.backend.get_internal_groups()

    def get_internal_users(self) -> QuerySet[User]:
        return User.objects.filter(Q(is_internal=True) | Q(id__in=self.backend.get_internal_users().values("id")))

    def refresh_users(self, reset_all: bool = False):
        if reset_all:
            User.objects.filter(is_internal=True).update(is_internal=False)
        users = []
        for user in self.get_internal_users().filter(is_active=True):
            user.is_internal = True
            users.append(user)
        User.objects.bulk_update(users, ["is_internal"])


def get_internal_groups() -> QuerySet[Group]:
    """
    Return the cached groups of internals users

    Returns:
        A queryset of group corresponding to the internal notion defined by the set UserBackend

    Raises:
        ValueError: If user backend path does not correspond to a valid module
    """
    return UserBackendRegistry().internal_groups
