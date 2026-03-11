import pytest
from rest_framework.reverse import reverse

from wbcore.contrib.authentication.factories import InternalUserFactory, UserFactory
from wbcore.contrib.notifications.factories.notification_types import (
    NotificationTypeFactory,
)


@pytest.mark.django_db
class TestNotificationTypeRepresentationViewSet:
    @pytest.mark.parametrize(
        "user__user_permissions,status_code", [(None, 403), (["notifications.select_notificationtype"], 200)]
    )
    def test_instance(self, notification_type, client, user, status_code):
        client.force_authenticate(user)
        response = client.get(
            reverse("wbcore:notifications:notification_type_representation-detail", args=[notification_type.pk])
        )
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code", [(None, 403), (["notifications.select_notificationtype"], 200)]
    )
    def test_list(self, client, user, status_code):
        client.force_authenticate(user)
        response = client.get(reverse("wbcore:notifications:notification_type_representation-list"))
        assert response.status_code == status_code  # type: ignore


@pytest.mark.django_db
class TestNotificationTypeSettingModelViewSet:
    @pytest.mark.parametrize(
        "user__user_permissions,status_code", [(None, 403), (["notifications.view_notificationtypesetting"], 200)]
    )
    def test_instance(self, notification_type_setting, client, user, status_code):
        client.force_authenticate(user)
        response = client.get(
            reverse("wbcore:notifications:notification_type_setting-detail", args=[notification_type_setting.pk])
        )
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code", [(None, 403), (["notifications.view_notificationtypesetting"], 200)]
    )
    def test_list(self, client, user, status_code):
        client.force_authenticate(user)
        response = client.get(reverse("wbcore:notifications:notification_type_setting-list"))
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code", [(None, 403), (["notifications.add_notificationtypesetting"], 403)]
    )
    def test_create(self, notification_type, client, user, status_code):
        """Regardless of permission, no user should ever be able to create notification type setting"""
        client.force_authenticate(user)
        response = client.post(
            reverse("wbcore:notifications:notification_type_setting-list"),
            {"user": user.id, "notification_type": notification_type.id},
        )
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code", [(None, 403), (["notifications.delete_notificationtypesetting"], 403)]
    )
    def test_delete(self, notification_type_setting, client, user, status_code):
        """Regardless of permission, no user should ever be able to delete notification type setting"""
        client.force_authenticate(user)
        response = client.delete(
            reverse("wbcore:notifications:notification_type_setting-detail", args=[notification_type_setting.id])
        )
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code", [(None, 403), (["notifications.change_notificationtypesetting"], 200)]
    )
    def test_change(self, notification_type_setting, client, user, status_code):
        notification_type_setting.user = user
        notification_type_setting.save()

        client.force_authenticate(user)
        response = client.patch(
            reverse("wbcore:notifications:notification_type_setting-detail", args=[notification_type_setting.id]),
            {"enable_web": True},
        )
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code", [(["notifications.change_notificationtypesetting"], 200)]
    )
    def test_change_notification_type_and_user(self, notification_type_setting, client, user, status_code):
        """Regardless of the permission, you should never be able to change the user or notification type"""
        user2 = UserFactory()
        notification_type2 = NotificationTypeFactory()

        assert user != user2
        assert notification_type_setting.notification_type != notification_type2

        client.force_authenticate(user)
        response = client.patch(
            reverse("wbcore:notifications:notification_type_setting-detail", args=[notification_type_setting.id]),
            {"notification_type": notification_type2.pk, "user": user2.pk},  # type: ignore
        )
        assert response.status_code == status_code  # type: ignore
        assert response.data["instance"]["user"] == user.pk
        assert response.data["instance"]["notification_type"] == notification_type_setting.notification_type.pk

    @pytest.mark.parametrize(
        "user__user_permissions,status_code", [(["notifications.change_notificationtypesetting"], 404)]
    )
    def test_change_setting_from_other_user(self, notification_type_setting, client, user, status_code):
        """Regardless of permission, no user should ever be able to change a setting from a different user"""
        other_user = InternalUserFactory(is_superuser=True)

        client.force_authenticate(other_user)
        response = client.patch(
            reverse("wbcore:notifications:notification_type_setting-detail", args=[notification_type_setting.id]),
            {"enable_web": True},
        )
        assert response.status_code == status_code  # type: ignore
