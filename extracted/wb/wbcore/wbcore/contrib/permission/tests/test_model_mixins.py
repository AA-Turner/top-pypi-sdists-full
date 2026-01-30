import pytest

from wbcore.contrib.permission.models.mixins import PermissionObjectModelMixin


@pytest.fixture
def mocked_permission_object_model_mixin(mocker):
    def __init__(self): ...  # noqa

    PermissionObjectModelMixin.__init__ = __init__
    PermissionObjectModelMixin.objects = mocker.Mock()
    mocker.patch.object(PermissionObjectModelMixin, "view_perm_str", "view_perm_str")
    mocker.patch.object(PermissionObjectModelMixin, "change_perm_str", "change_perm_str")
    mocker.patch.object(PermissionObjectModelMixin, "delete_perm_str", "delete_perm_str")
    mocker.patch.object(PermissionObjectModelMixin, "select_perm_str", "select_perm_str")
    mocker.patch.object(PermissionObjectModelMixin, "add_perm_str", "add_perm_str")
    mocker.patch.object(PermissionObjectModelMixin, "admin_perm_str", "admin_perm_str")
    return PermissionObjectModelMixin


class TestPermissionObjectModelMixin:
    def test_save_run_assign_permissions(self, mocker, mocked_permission_object_model_mixin):
        mocker.patch("django.db.models.Model.save")
        on_commit = mocker.patch("wbcore.contrib.permission.models.mixins.transaction.on_commit")
        content_type_class = mocker.patch("wbcore.contrib.permission.models.mixins.ContentType")
        content_type_class.objects.get_for_model.return_value = mocker.Mock()

        mocked_permission_object_model_mixin().save()

        on_commit.assert_called_once()

    def test_reload_permissions(self, mocker, mocked_permission_object_model_mixin):
        reload_permissions = mocker.patch("wbcore.contrib.permission.models.mixins.reload_permissions")
        mocked_permission_object_model_mixin().reload_permissions(prune_existing=True, force_pruning=True)
        reload_permissions.assert_called_once()

    def test_get_permissions_for_superuser(self, mocker, mocked_permission_object_model_mixin):
        user = mocker.Mock()
        user.is_superuser = True
        permissions = mocked_permission_object_model_mixin().get_permissions_for_user(user)
        assert permissions == {}

    def test_get_permissions_for_internal_admin_user(self, mocker, mocked_permission_object_model_mixin):
        user = mocker.Mock()
        user.is_internal = True
        user.is_superuser = False
        mocker.patch.object(user, "has_perm", side_effect=lambda x: x == "admin_perm_str")
        permissions = mocked_permission_object_model_mixin().get_permissions_for_user(user)
        assert permissions == {
            "view_perm_str": False,
            "change_perm_str": False,
            "delete_perm_str": False,
            "select_perm_str": False,
            "add_perm_str": False,
        }

    def test_get_permissions_for_external_user(self, mocker, mocked_permission_object_model_mixin):
        user = mocker.Mock()
        user.is_internal = False
        user.is_superuser = False
        permissions = mocked_permission_object_model_mixin().get_permissions_for_user(user)
        assert permissions == {}

    @pytest.mark.parametrize(
        "permission", ["view_perm_str", "change_perm_str", "delete_perm_str", "select_perm_str", "add_perm_str"]
    )
    def test_get_permission_for_internal_user_and_single_permission(
        self, mocker, mocked_permission_object_model_mixin, permission
    ):
        user = mocker.Mock()
        user.is_internal = True
        user.is_superuser = False

        mocker.patch.object(user, "has_perm", side_effect=lambda x: x == permission)

        permissions = mocked_permission_object_model_mixin().get_permissions_for_user(user)
        assert permissions == {permission: False}


@pytest.mark.django_db
def test_post_save_user(user_factory, mocker):
    on_commit = mocker.patch("wbcore.contrib.permission.models.mixins.transaction.on_commit")
    user_factory.create()

    on_commit.assert_called_once()


@pytest.mark.django_db
def test_post_save_user_not_called(user_factory, mocker):
    user_factory.create()
    on_commit = mocker.patch("wbcore.contrib.permission.models.mixins.transaction.on_commit")

    on_commit.assert_not_called()
