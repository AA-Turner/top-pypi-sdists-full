from contextlib import suppress
from datetime import datetime
from typing import TYPE_CHECKING, Iterable, Iterator

from django.contrib.contenttypes.models import ContentType
from django.db import ProgrammingError
from django.db.models import Model, Q, QuerySet
from django.utils import timezone
from guardian.shortcuts import assign_perm, get_anonymous_user
from psycopg.errors import InvalidCursorName

from wbcore.contrib.authentication.models import User
from wbcore.contrib.permission.models import UserObjectPermission

if TYPE_CHECKING:
    from wbcore.contrib.permission.models.mixins import PermissionObjectModelMixin

from django.contrib.auth.models import Permission


def perm_to_permission(perm: str) -> Permission:
    """
    Convert a identifier string permission format in 'app_label.codename'
    (teremd as *perm*) to a django permission instance.

    Args:
        perm: The string permission identifier in the form 'app_label.codename'

    Returns:
        The Permission object corresponding to the given string identifier

    Raises:
        AttributeError: When the given string identifier does not match the expected format 'app_label.codename'
    """
    try:
        app_label, codename = perm.split(".", 1)
    except IndexError as e:
        raise AttributeError(
            "The format of identifier string permission (perm) is wrong. It should be in 'app_label.codename'."
        ) from e
    else:
        permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
        return permission


def assign_permissions(permissions_map: Iterable[tuple[str, Model, User, bool]]):
    """
    Assigns object-level permissions to users based on the provided permissions map.

    This method iterates through the permissions_map, assigns the specified permission
    to the user for the model instance, sets the 'editable' flag for the permission,
    and saves the object permission.
    """
    for permission, instance, user, editable in permissions_map:
        object_permissions = assign_perm(permission, user, instance)

        if object_permissions is None:
            continue

        if isinstance(object_permissions, Model):
            object_permissions = [object_permissions]

        for object_permission in object_permissions:
            object_permission.editable = editable  # type: ignore -- We have our custom Permission class here
            object_permission.save()


def get_public_user_or_group(only_internal: bool = False) -> QuerySet[User]:
    """
    Retrieves a queryset of active users, optionally filtering to internal users only.

    This method fetches users based on the `only_internal` flag.
    If set, it filters for internal users, otherwise returns all users.
    The queryset includes active users or the anonymous user and excludes superusers
    from the main set, while later ensuring their inclusion through a union operation.
    """
    users = User.objects.filter(is_active=True)
    if only_internal:
        users = users.filter(
            Q(is_superuser=True)
            | Q(id=get_anonymous_user().pk)
            | Q(id__in=User.objects.filter_internal().values("id"))
        )
    return users


def get_permission_matrix(
    queryset: QuerySet,
    created: datetime | None = None,
    instance: Model | None = None,
    user: User | None = None,
) -> Iterator[tuple[str, Model, User, bool]]:
    """
    Retrieves the permission matrix for all (user, object) pairs

    If an instance is provided, the queryset is filtered to that specific object. The method determines the
    appropriate set of users based on the permission type of the object (private or public).

    For each user, the function yields a tuple containing the permission string, the object instance,
    the user, and whether the permission is editable.
    """

    if instance:
        queryset = queryset.filter(id=instance.id)  # type: ignore

    for _instance in queryset.all():
        if _instance.permission_type is _instance.PermissionType.PUBLIC:
            users = get_public_user_or_group()
        else:
            users = get_public_user_or_group(only_internal=True)
        if user:
            users = users.filter(id=user.id)
        for user in users:
            for permission, editable in _instance.get_permissions_for_user(user, created=created).items():
                yield permission, _instance, user, editable


def prune_permissions(instance: "PermissionObjectModelMixin", force: bool | None = False):
    queryset = UserObjectPermission.objects.filter(
        content_type=ContentType.objects.get_for_model(instance), object_pk=instance.id
    )
    if not force:
        queryset = queryset.exclude(editable=True)
    for permission in queryset:
        permission.delete()


def reload_permissions(
    queryset: QuerySet,
    created: datetime | None = None,
    user: User | None = None,
    instance: "PermissionObjectModelMixin | None" = None,
    prune_existing: bool = True,
    force_pruning: bool = False,
):
    """
    Assigns permissions based on a given queryset, with options to prune existing permissions and
    specify the creation timestamp. If no creation time is provided, the current time is used.

    The function first checks if existing permissions should be pruned, which happens if both
    `prune_existing` and `instance` are provided. It then retrieves the permission matrix
    using `get_permission_matrix()` and assigns the appropriate permissions.

    Error handling is in place to suppress database-related errors, such as `ProgrammingError`
    and `InvalidCursorName`, which can occur due to unmanaged tables.
    """
    if not created:
        created = timezone.now()
    with suppress(ProgrammingError, InvalidCursorName):  # We check this to catch error trigger by unmanaged table
        if prune_existing and instance:
            prune_permissions(instance, force=force_pruning)
        permission_matrix = get_permission_matrix(queryset, created=created, instance=instance, user=user)
        assign_permissions(permission_matrix)
