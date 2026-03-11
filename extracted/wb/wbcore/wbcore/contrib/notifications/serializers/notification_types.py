from rest_framework.reverse import reverse

from wbcore import serializers
from wbcore.contrib.notifications.models import (
    NotificationType,
    NotificationTypeSetting,
)


class NotificationTypeRepresentationSerializer(serializers.RepresentationSerializer):
    class Meta:
        model = NotificationType
        fields = (
            "id",
            "code",
            "title",
            "help_text",
        )


class NotificationTypeSettingModelSerializer(serializers.ModelSerializer):
    _notification_type = NotificationTypeRepresentationSerializer(source="notification_type")
    help_text = serializers.CharField()
    locked_icon = serializers.IconSelectField(read_only=True)
    locked = serializers.BooleanField(read_only=True)
    _update_url = serializers.SerializerMethodField()

    def get__update_url(self, obj):
        if not obj.notification_type.is_lock:
            return reverse(
                "wbcore:notifications:notification_type_setting-list", args=[], request=self.context["request"]
            )
        return None

    class Meta:
        read_only_fields = ("user", "notification_type", "help_text")
        model = NotificationTypeSetting
        fields = (
            "id",
            "notification_type",
            "_notification_type",
            "help_text",
            "user",
            "enable_web",
            "enable_mobile",
            "enable_email",
            "frequency",
            "locked",
            "locked_icon",
            "_additional_resources",
            "_update_url",
        )
