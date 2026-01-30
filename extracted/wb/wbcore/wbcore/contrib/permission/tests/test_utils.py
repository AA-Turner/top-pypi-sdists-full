import pytest
from django.contrib.contenttypes.models import ContentType

from wbcore.contrib.authentication.models.users import Permission
from wbcore.contrib.permission.models import UserObjectPermission
from wbcore.contrib.permission.models.mixins import PermissionObjectModelMixin
from wbcore.contrib.permission.utils import (
    assign_permissions,
    get_permission_matrix,
    get_public_user_or_group,
    prune_permissions,
    reload_permissions,
)


@pytest.mark.django_db
class TestAssignPermissionsMap:
    def test_assign_permissions(self, user):
        assign_permissions([("view_user", user, user, True)])

        assert user.has_perm("view_user", user)
        assert not user.has_perm("change_user", user)

    def test_assign_permissions_editable(self, user):
        assign_permissions([("view_user", user, user, True), ("change_user", user, user, False)])

        assert user.has_perm("view_user", user)
        assert user.has_perm("change_user", user)

        assert UserObjectPermission.objects.get(
            user=user,
            content_type_id=ContentType.objects.get_for_model(user).pk,
            object_pk=user.pk,
            permission__codename="view_user",
        ).editable

        assert not UserObjectPermission.objects.get(
            user=user,
            content_type_id=ContentType.objects.get_for_model(user).pk,
            object_pk=user.pk,
            permission__codename="change_user",
        ).editable

    def test_assign_permission_with_non_perm(self, mocker):
        assign_perm = mocker.patch("wbcore.contrib.permission.utils.assign_perm")
        assign_perm.return_value = None

        assign_permissions([("view_user", mocker.Mock(), mocker.Mock(), True)])

        assign_perm.assert_called_once()


@pytest.mark.django_db
class TestGetPublicUserOrGroup:
    def test_get_public_user_or_group(self, user):
        public_user = get_public_user_or_group()

        assert public_user.count() == 1
        public_user = public_user.first()
        assert public_user
        assert public_user == user
        assert public_user.is_active

    def test_get_public_user_or_group_only_internal(self, internal_user):
        users = get_public_user_or_group(only_internal=True)
        assert users.count() == 1

    def test_get_public_user_or_group_only_internal_with_external_user(self, user):
        users = get_public_user_or_group(only_internal=True)
        assert users.count() == 0


@pytest.mark.django_db
class TestGetPermissionMatrix:
    def test_get_permission_matrix(self, user, mocker):
        def get_permission_for_user(self, created=None):
            return {"view_user": True, "change_user": False}

        queryset = mocker.Mock()
        instance = mocker.Mock()
        queryset.__iter__ = lambda _: iter([instance])
        queryset.all.return_value = iter([instance])
        instance.get_permissions_for_user = get_permission_for_user
        instance.permission_type = PermissionObjectModelMixin.PermissionType.PUBLIC
        instance.PermissionType = PermissionObjectModelMixin.PermissionType

        matrix = get_permission_matrix(queryset, None, None)
        assert list(matrix) == [("view_user", instance, user, True), ("change_user", instance, user, False)]

    def test_get_permission_matrix_with_instance(self, user, mocker):
        def get_permission_for_user(self, created=None):
            return {"view_user": True, "change_user": False}

        queryset = mocker.Mock()
        queryset.filter.return_value = queryset
        instance = mocker.Mock()
        queryset.__iter__ = lambda _: iter([instance])
        queryset.all.return_value = iter([instance])
        instance.get_permissions_for_user = get_permission_for_user
        instance.permission_type = PermissionObjectModelMixin.PermissionType.PUBLIC
        instance.PermissionType = PermissionObjectModelMixin.PermissionType

        matrix = get_permission_matrix(queryset, None, instance)
        next(matrix)
        queryset.filter.assert_called_once_with(id=instance.id)

    def test_get_permission_matrix_private(self, internal_user, mocker):
        def get_permission_for_user(self, created=None):
            return {"view_user": True, "change_user": False}

        queryset = mocker.Mock()
        queryset.filter.return_value = queryset
        instance = mocker.Mock()
        queryset.__iter__ = lambda _: iter([instance])
        queryset.all.return_value = iter([instance])
        instance.get_permissions_for_user = get_permission_for_user
        instance.permission_type = PermissionObjectModelMixin.PermissionType.PRIVATE
        instance.PermissionType = PermissionObjectModelMixin.PermissionType

        matrix = get_permission_matrix(queryset, None, None)
        assert list(matrix) == [
            ("view_user", instance, internal_user, True),
            ("change_user", instance, internal_user, False),
        ]


@pytest.mark.django_db
class TestPrunePermissions:
    def test_prune_permissions(self, user):
        ct = ContentType.objects.get_for_model(user)
        permission = Permission.objects.filter(content_type=ct).first()
        UserObjectPermission.objects.create(
            permission=permission, user=user, content_type=ct, object_pk=user.id, editable=False
        )
        assert UserObjectPermission.objects.filter(permission=permission, content_type=ct, object_pk=user.id).exists()
        prune_permissions(user)
        assert not UserObjectPermission.objects.filter(
            permission=permission, content_type=ct, object_pk=user.id
        ).exists()

    def test_prune_permissions_editable(self, user):
        ct = ContentType.objects.get_for_model(user)
        permission = Permission.objects.filter(content_type=ct).first()
        UserObjectPermission.objects.create(
            permission=permission, user=user, content_type=ct, object_pk=user.id, editable=True
        )
        assert UserObjectPermission.objects.filter(permission=permission, content_type=ct, object_pk=user.id).exists()
        prune_permissions(user)
        assert UserObjectPermission.objects.filter(permission=permission, content_type=ct, object_pk=user.id).exists()

    def test_prune_permissions_editable_with_force(self, user):
        ct = ContentType.objects.get_for_model(user)
        permission = Permission.objects.filter(content_type=ct).first()
        UserObjectPermission.objects.create(
            permission=permission, user=user, content_type=ct, object_pk=user.id, editable=True
        )
        assert UserObjectPermission.objects.filter(permission=permission, content_type=ct, object_pk=user.id).exists()
        prune_permissions(user, True)
        assert not UserObjectPermission.objects.filter(
            permission=permission, content_type=ct, object_pk=user.id
        ).exists()


class TestReloadPermissions:
    def test_reload_permissions(self, mocker):
        get_permission_matrix = mocker.patch("wbcore.contrib.permission.utils.get_permission_matrix")
        assign_permissions = mocker.patch("wbcore.contrib.permission.utils.assign_permissions")

        queryset = mocker.Mock()

        reload_permissions(queryset)

        get_permission_matrix.assert_called_once()
        assign_permissions.assert_called_once()

    def test_reload_permissions_with_prune(self, mocker):
        prune_permissions = mocker.patch("wbcore.contrib.permission.utils.prune_permissions")
        mocker.patch("wbcore.contrib.permission.utils.get_permission_matrix")
        mocker.patch("wbcore.contrib.permission.utils.assign_permissions")

        queryset = mocker.Mock()

        reload_permissions(queryset)

        prune_permissions.assert_not_called()

    def test_reload_permissions_with_prune_and_instance(self, mocker):
        prune_permissions = mocker.patch("wbcore.contrib.permission.utils.prune_permissions")
        mocker.patch("wbcore.contrib.permission.utils.get_permission_matrix")
        mocker.patch("wbcore.contrib.permission.utils.assign_permissions")

        queryset = mocker.Mock()
        instance = mocker.Mock()

        reload_permissions(queryset, instance=instance)

        prune_permissions.assert_called_once()
