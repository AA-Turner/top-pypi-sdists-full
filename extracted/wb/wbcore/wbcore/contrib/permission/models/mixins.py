from contextlib import suppress
from datetime import datetime

from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from wbcore.contrib.authentication.models.users import User
from wbcore.contrib.permission.utils import reload_permissions
from wbcore.utils.itertools import get_inheriting_subclasses
from wbcore.workers import Queue


class PermissionMixin(models.Model):
    class Meta:
        abstract = True

    @classmethod
    @property
    def view_perm_str(cls) -> str:
        """
        Get the view string permission identifer

        Returns:
            The view string permission identifier
        """
        return f"{cls._meta.app_label}.view_{cls._meta.model_name}"

    @classmethod
    @property
    def change_perm_str(cls) -> str:
        """
        Get the change string permission identifer

        Returns:
            The change string permission identifier
        """
        return f"{cls._meta.app_label}.change_{cls._meta.model_name}"

    @classmethod
    @property
    def delete_perm_str(cls) -> str:
        """
        Get the delete string permission identifer

        Returns:
            The delete string permission identifier
        """
        return f"{cls._meta.app_label}.delete_{cls._meta.model_name}"

    @classmethod
    @property
    def select_perm_str(cls) -> str:
        """
        Get the select string permission identifer

        Returns:
            The select string permission identifier
        """
        return f"{cls._meta.app_label}.select_{cls._meta.model_name}"

    @classmethod
    @property
    def admin_perm_str(cls) -> str:
        """
        Get the admin string permission identifer

        Returns:
            The admin string permission identifier
        """
        return f"{cls._meta.app_label}.administrate_{cls._meta.model_name}"

    @classmethod
    @property
    def add_perm_str(cls) -> str:
        """
        Get the add string permission identifer

        Returns:
            The add string permission identifier
        """
        return f"{cls._meta.app_label}.add_{cls._meta.model_name}"


class PermissionObjectModelMixin(PermissionMixin):
    """
    Permission object Mixin that set the default behavior for permission assignments.
    Methods can be supercharged in order to customize behavior.
    """

    id: int

    class PermissionType(models.TextChoices):
        INTERNAL = "INTERNAL", _("Internal")
        PUBLIC = "PUBLIC", _("Public")
        PRIVATE = "PRIVATE", _("Private")

    permission_shortcut_kwargs = {"accept_global_perms": False}

    permission_type = models.CharField(default=PermissionType.PRIVATE, choices=PermissionType.choices, max_length=8)
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_%(app_label)s_%(class)s",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self)
        transaction.on_commit(lambda: assign_user_permissions_for_object_as_task.delay(content_type.id, self.id))  # type: ignore

    class Meta:
        abstract = True
        default_permissions = ("add", "change", "delete", "view", "administrate")

    def get_permissions_for_user(self, user: User, created: datetime | None = None) -> dict[str, bool]:
        """
        Determine the permissions for a given user on this object. This method uses a best guess approach.
        If this approach is not suitable for your needs, please override this method in your subclass and
        avoid a call to `super().get_permissions_for_user`.

        This method checks the user's status and permissions to determine what actions
        they are allowed to perform on the object. The permissions are returned as a
        dictionary where the keys are permission strings and the values are booleans
        indicating whether the permission is editable.

        Behavior:
            - If the user is a superuser, they are granted all permissions (non-editable).
            - If the user is internal and has admin permissions, they are granted all permissions (non-editable).
            - For other internal users, permissions are checked individually and added to the
              result if the user has them (all set as non-editable).
            - Non-internal users receive no permissions.
        """

        # Superuser have access regardless, but we do not want to overpolute the permission table
        if user.is_superuser:
            return {}

        # If the user is internal and has the admin permission, this user can do anything
        if user.is_internal and user.has_perm(self.admin_perm_str):
            return {
                self.view_perm_str: False,
                self.change_perm_str: False,
                self.delete_perm_str: False,
                self.select_perm_str: False,
                self.add_perm_str: False,
            }

        permissions = {}
        if user.is_internal:
            if user.has_perm(self.view_perm_str):
                permissions[self.view_perm_str] = False

            if user.has_perm(self.change_perm_str):
                permissions[self.change_perm_str] = False

            if user.has_perm(self.delete_perm_str):
                permissions[self.delete_perm_str] = False

            if user.has_perm(self.select_perm_str):
                permissions[self.select_perm_str] = False

            if user.has_perm(self.add_perm_str):
                permissions[self.add_perm_str] = False

        return permissions

    def reload_permissions(self, prune_existing: bool = True, force_pruning: bool = False):
        reload_permissions(
            self.__class__.objects, instance=self, prune_existing=prune_existing, force_pruning=force_pruning
        )


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    """
    Triggers the load_permission_objects as a celery task for all connected signals on User save
    """
    if created:
        transaction.on_commit(lambda: assign_object_permissions_for_user_as_task.delay(instance.id))  # type: ignore


@shared_task(queue=Queue.DEFAULT.value)
def assign_user_permissions_for_object_as_task(
    content_type_id: int, instance_id: int, prune_existing: bool | None = True
):
    """
    Utility function to create object permission from obj decoupling from the main thread
    """
    content_type = ContentType.objects.get(id=content_type_id)
    if model_class := content_type.model_class():
        with suppress(model_class.DoesNotExist):
            instance = model_class.objects.get(id=instance_id)
            instance.reload_permissions(prune_existing=prune_existing)  # type: ignore


@shared_task(queue=Queue.DEFAULT.value)
def assign_object_permissions_for_user_as_task(user_id: int):
    """
    Utility function to create object permission from user decoupling from the main thread
    """

    user = User.objects.get(id=user_id)
    for permission_class in get_inheriting_subclasses(PermissionObjectModelMixin):
        reload_permissions(permission_class.objects, user=user, prune_existing=True)
