import pytest
from django.db.utils import IntegrityError

from wbcore.contrib.authentication.factories import UserFactory
from wbcore.contrib.notifications.factories.notification_types import (
    NotificationTypeFactory,
)
from wbcore.contrib.notifications.models import (
    NotificationType,
    NotificationTypeSetting,
)


@pytest.mark.django_db
class TestNotificationType:
    def test_factory(self, notification_type: NotificationType):
        assert isinstance(notification_type, NotificationType)
        assert notification_type.pk is not None

    def test_to_str(self, notification_type: NotificationType):
        assert str(notification_type) == notification_type.title

    def test_endpoint_basename(self):
        assert NotificationType.get_endpoint_basename() == "wbcore:notifications:notification_type"

    def test_representation_endpoint(self):
        assert (
            NotificationType.get_representation_endpoint()
            == "wbcore:notifications:notification_type_representation-list"
        )

    def test_representation_value_key(self):
        assert NotificationType.get_representation_value_key() == "id"

    def test_representation_label_key(self):
        assert NotificationType.get_representation_label_key() == "{{title}}"

    @pytest.mark.parametrize("notification_type__code", ["code"])
    def test_unique_code(self, notification_type: NotificationType):
        assert notification_type.pk is not None

        with pytest.raises(IntegrityError):
            NotificationTypeFactory(code="code")


@pytest.mark.django_db
class TestNotificationTypeSetting:
    def test_factory(self, notification_type_setting: NotificationTypeSetting):
        assert isinstance(notification_type_setting, NotificationTypeSetting)
        assert notification_type_setting.pk is not None

    def test_to_str(self, notification_type_setting: NotificationTypeSetting):
        template = "{0.user}: {0.notification_type} ({0.enable_web}/{0.enable_mobile}/{0.enable_email})"
        assert str(notification_type_setting) == template.format(notification_type_setting)

    def test_endpoint_basename(self):
        assert NotificationTypeSetting.get_endpoint_basename() == "wbcore:notifications:notification_type_setting"

    def test_representation_endpoint(self):
        assert (
            NotificationTypeSetting.get_representation_endpoint()
            == "wbcore:notifications:notification_type_setting_representation-list"
        )

    def test_representation_value_key(self):
        assert NotificationTypeSetting.get_representation_value_key() == "id"

    def test_representation_label_key(self):
        assert NotificationTypeSetting.get_representation_label_key() == "{{notification_type}}"

    def test_create_through_post_save_from_notification_type(self, user):
        assert user.pk is not None
        type_count = NotificationTypeSetting.objects.filter(user=user).count()

        NotificationTypeFactory()

        assert NotificationTypeSetting.objects.filter(user=user).count() == type_count + 1

    def test_create_through_post_save_from_user(self, notification_type):
        assert notification_type.pk is not None
        assert not NotificationTypeSetting.objects.filter(notification_type=notification_type).exists()

        UserFactory()

        assert NotificationTypeSetting.objects.filter(notification_type=notification_type).exists()
