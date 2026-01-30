from django.db import models
from guardian.models import GroupObjectPermissionAbstract, UserObjectPermissionAbstract


class UserObjectPermission(UserObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)
    editable = models.BooleanField(default=True)
    system = models.BooleanField(default=False)

    class Meta(UserObjectPermissionAbstract.Meta):
        abstract = False
        default_related_name = "userobjectpermissions"
        indexes = [
            *UserObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=["content_type", "object_pk", "user"]),
        ]


class GroupObjectPermission(GroupObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)
    editable = models.BooleanField(default=True)

    class Meta(GroupObjectPermissionAbstract.Meta):
        abstract = False
        default_related_name = "groupobjectpermissions"
        indexes = [
            *GroupObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=["content_type", "object_pk", "group"]),
        ]
