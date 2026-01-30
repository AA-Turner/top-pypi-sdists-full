from contextlib import suppress

from django.contrib.auth.models import Group, Permission
from django.db.models import Q, QuerySet
from django.utils.functional import cached_property
from guardian.utils import get_anonymous_user

from wbcore.contrib.authentication.models.users import User


class UserBackend:
    """
    Base UserBackend for basic support (default to all valid user except the anonymous user)
    """

    @cached_property
    def internal_user_permission(self) -> Permission | None:
        try:
            return Permission.objects.get(content_type__app_label="authentication", codename="is_internal_user")
        except Permission.DoesNotExist:
            return None

    def get_internal_groups(self) -> QuerySet[Group]:
        if self.internal_user_permission:
            return Group.objects.filter(permissions=self.internal_user_permission)
        return Group.objects.none()

    def get_internal_users(self) -> QuerySet[User]:
        if self.internal_user_permission:
            qs = User.objects.filter(is_active=True).filter(
                Q(user_permissions=self.internal_user_permission) | Q(groups__in=self.get_internal_groups().all())
            )
            with suppress(User.DoesNotExist):
                qs = qs.exclude(id=get_anonymous_user().id)
            return qs.distinct()
        return User.objects.none()
