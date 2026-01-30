from wbcore.contrib.permission.models.mixins import PermissionObjectModelMixin


class PermissionTestModel(PermissionObjectModelMixin):
    class Meta(PermissionObjectModelMixin.Meta):
        managed = False
