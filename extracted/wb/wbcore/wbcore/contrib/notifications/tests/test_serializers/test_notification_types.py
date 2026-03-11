import pytest
from rest_framework.reverse import reverse

from wbcore.contrib.notifications.serializers import (
    NotificationTypeRepresentationSerializer,
    NotificationTypeSettingModelSerializer,
)


@pytest.mark.django_db
class TestNotificationTypeRepresentationSerializer:
    def test_serialize_instance(self, notification_type):
        serializer = NotificationTypeRepresentationSerializer(notification_type)
        assert serializer.data == {
            "id": notification_type.id,
            "code": notification_type.code,
            "title": notification_type.title,
            "help_text": notification_type.help_text,
        }


@pytest.mark.django_db
class TestNotificationTypeSettingModelSerializer:
    def test_serialize_instance(self, notification_type_setting, request_with_user):
        # We need to add the help_text here manually - we assume the queryset passed into the serializer annotates it
        # in the viewset.
        notification_type_setting.help_text = notification_type_setting.notification_type.help_text
        serializer = NotificationTypeSettingModelSerializer(
            notification_type_setting, context={"request": request_with_user}
        )

        assert serializer.data == {
            "id": notification_type_setting.id,
            "notification_type": notification_type_setting.notification_type.id,
            "_notification_type": NotificationTypeRepresentationSerializer(
                notification_type_setting.notification_type
            ).data,
            "help_text": notification_type_setting.notification_type.help_text,
            "user": notification_type_setting.user.id,
            "enable_web": notification_type_setting.enable_web,
            "enable_mobile": notification_type_setting.enable_mobile,
            "enable_email": notification_type_setting.enable_email,
            "frequency": notification_type_setting.frequency,
            "_additional_resources": {},
            "_update_url": reverse(
                "wbcore:notifications:notification_type_setting-list", args=[], request=request_with_user
            ),
            "locked_icon": None,
        }

    def test_deserialize_partial_instance(self, notification_type_setting, request_with_user):
        serializer = NotificationTypeSettingModelSerializer(
            notification_type_setting,
            data={"enable_web": True},
            partial=True,
            context={"request": request_with_user},
        )

        assert serializer.is_valid()
        assert serializer.validated_data["enable_web"]  # type: ignore
