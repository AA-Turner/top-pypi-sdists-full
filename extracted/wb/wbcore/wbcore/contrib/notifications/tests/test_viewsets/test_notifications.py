import pytest
from django.utils import timezone
from rest_framework.reverse import reverse

from wbcore.contrib.authentication.factories import UserFactory
from wbcore.contrib.notifications.factories.notifications import (
    NotificationFactory,
)
from wbcore.contrib.notifications.models.notifications import Notification


@pytest.mark.django_db
class TestNotificationModelViewSet:
    @pytest.mark.parametrize(
        "user__user_permissions, status_code",
        [(None, 403), (["notifications.view_notification"], 200)],
    )
    def test_instance(self, notification, client, user, status_code):
        client.force_authenticate(user)
        response = client.get(reverse("wbcore:notifications:notification-detail", args=[notification.pk]))
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code",
        [(["notifications.view_notification"], 200)],
    )
    def test_instance_read(self, notification, client, user, status_code):
        assert notification.read is None
        client.force_authenticate(user)
        response = client.get(reverse("wbcore:notifications:notification-detail", args=[notification.pk]))
        assert response.status_code == status_code  # type: ignore
        notification.refresh_from_db()
        assert notification.read is not None

    @pytest.mark.parametrize(
        "user__user_permissions,status_code",
        [(None, 403), (["notifications.view_notification"], 200)],
    )
    def test_list(self, client, user, status_code):
        client.force_authenticate(user)
        response = client.get(reverse("wbcore:notifications:notification-list"))
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code",
        [(["notifications.add_notification"], 403)],
    )
    def test_create(self, notification, client, user, status_code):
        """Regardless of permission, no user should ever be able to create notification"""
        client.force_authenticate(user)
        response = client.post(
            reverse("wbcore:notifications:notification-list"),
            {
                "user": user.id,
                "notification": notification.id,
                "title": "abc",
                "body": "abc",
            },
        )
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code",
        [(["notifications.change_notification"], 403)],
    )
    def test_change(self, notification, client, user, status_code):
        """Regardless of permission, no user should ever be able to change notification"""
        client.force_authenticate(user)
        response = client.patch(
            reverse("wbcore:notifications:notification-detail", args=[notification.pk]),
            {"title": "abc"},
        )
        assert response.status_code == status_code  # type: ignore
        response = client.put(
            reverse("wbcore:notifications:notification-detail", args=[notification.pk]),
            {"title": "abc"},
        )
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code",
        [(None, 403), (["notifications.delete_notification"], 204)],
    )
    def test_delete(self, notification, client, user, status_code):
        client.force_authenticate(user)
        response = client.delete(reverse("wbcore:notifications:notification-detail", args=[notification.pk]))
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize(
        "user__user_permissions,status_code",
        [(["notifications.delete_notification"], 404)],
    )
    def test_delete_other_notification(self, notification, client, user, status_code):
        """Regardless of the permission, a user should never be able to delete another users notifications"""
        user2 = UserFactory()
        notification.user = user2
        notification.save()
        client.force_authenticate(user)
        response = client.delete(reverse("wbcore:notifications:notification-detail", args=[notification.pk]))
        assert response.status_code == status_code  # type: ignore

    @pytest.mark.parametrize("user__user_permissions", [(["notifications.change_notification"])])
    def test_read_all_action(self, notification, client, user):
        assert notification.read is None
        client.force_authenticate(user)
        client.patch(reverse("wbcore:notifications:notification-read-all"))
        notification.refresh_from_db()
        assert notification.read is not None

    @pytest.mark.parametrize("user__user_permissions", [(["notifications.change_notification"])])
    def test_read_all_action_other_notification(self, notification, client, user):
        notification2 = NotificationFactory()
        assert notification.read is None
        assert notification2.read is None  # type: ignore
        client.force_authenticate(user)
        client.patch(reverse("wbcore:notifications:notification-read-all"))
        notification.refresh_from_db()
        notification2.refresh_from_db()  # type: ignore
        assert notification.read is not None
        assert notification2.read is None  # type: ignore

    @pytest.mark.parametrize("user__user_permissions", [(["notifications.change_notification"])])
    def test_delete_all_action(self, notification, client, user):
        NotificationFactory(user=user, read=timezone.now())
        assert Notification.objects.filter(user=user).count() == 2

        client.force_authenticate(user)
        client.patch(reverse("wbcore:notifications:notification-delete-all-read"))

        assert Notification.objects.filter(user=user).count() == 1

    @pytest.mark.parametrize("user__user_permissions", [(["notifications.change_notification"])])
    def test_delete_all_action_other_notification(self, notification, client, user):
        user2 = UserFactory()
        NotificationFactory(user=user2, read=timezone.now())
        notification.read = timezone.now()
        notification.save()
        assert Notification.objects.all().count() == 2

        client.force_authenticate(user)
        client.patch(reverse("wbcore:notifications:notification-delete-all-read"))

        assert Notification.objects.all().count() == 1
