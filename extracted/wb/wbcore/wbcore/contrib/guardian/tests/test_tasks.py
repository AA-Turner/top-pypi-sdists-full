import pytest
from django.contrib.contenttypes.models import ContentType

from wbcore.contrib.guardian.models.mixins import (
    assign_object_permissions_for_user_as_task,
    assign_user_permissions_for_object_as_task,
)


class TestAssignUserPermissionsForObjectAsTask:
    def test_called(self, mocker):
        content_type_class = mocker.patch("wbcore.contrib.guardian.models.mixins.ContentType")
        content_type = mocker.Mock()
        model_class = mocker.Mock()
        instance = mocker.Mock()
        model_class.objects.get.return_value = instance
        content_type.model_class.return_value = model_class
        content_type_class.objects.get.return_value = content_type

        assign_user_permissions_for_object_as_task(1, 1)

        instance.reload_permissions.assert_called_once_with(prune_existing=True)

    def test_called_with_prune_existing(self, mocker):
        content_type_class = mocker.patch("wbcore.contrib.guardian.models.mixins.ContentType")
        content_type = mocker.Mock()
        model_class = mocker.Mock()
        instance = mocker.Mock()
        model_class.objects.get.return_value = instance
        content_type.model_class.return_value = model_class
        content_type_class.objects.get.return_value = content_type

        assign_user_permissions_for_object_as_task(1, 1, prune_existing=False)

        instance.reload_permissions.assert_called_once_with(prune_existing=False)

    def test_not_called_without_model_class(self, mocker):
        content_type_class = mocker.patch("wbcore.contrib.guardian.models.mixins.ContentType")
        content_type = mocker.Mock()
        model_class = mocker.Mock()
        instance = mocker.Mock()
        model_class.objects.get.return_value = instance
        content_type.model_class.return_value = None
        content_type_class.objects.get.return_value = content_type

        assign_user_permissions_for_object_as_task(1, 1)

        instance.reload_permissions.assert_not_called()

    @pytest.mark.django_db
    def test_not_called_with_instance(self, user):
        with pytest.raises(
            AttributeError
        ):  # this means it crashed because the method reload_permissions does not exist which is fine
            assign_user_permissions_for_object_as_task(ContentType.objects.get_for_model(user).id, user.id)

    @pytest.mark.django_db
    def test_not_called_without_instance(self, user, mocker):
        user.reload_permissions = mocker.Mock()
        spy = mocker.spy(user, "reload_permissions")
        assign_user_permissions_for_object_as_task(ContentType.objects.get_for_model(user).id, user.id + 1)
        assert spy.call_count == 0


class TestAssignObjectPermissionsForUserAsTask:
    def test_called(self, mocker):
        user_class = mocker.patch("wbcore.contrib.guardian.models.mixins.User")
        user = mocker.Mock()

        user_class.objects.get.return_value = user

        get_inheriting_subclasses = mocker.patch("wbcore.contrib.guardian.models.mixins.get_inheriting_subclasses")
        get_inheriting_subclasses.return_value = [user_class]
        reload_permissions = mocker.patch("wbcore.contrib.guardian.models.mixins.reload_permissions")

        assign_object_permissions_for_user_as_task(user_id=1)

        reload_permissions.assert_called_once()
