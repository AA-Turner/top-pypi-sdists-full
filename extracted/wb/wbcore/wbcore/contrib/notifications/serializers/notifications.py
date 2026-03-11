from wbcore import serializers
from wbcore.contrib.notifications.models import Notification
from wbcore.contrib.notifications.serializers.notification_types import (
    NotificationTypeRepresentationSerializer,
)


class NotificationModelSerializer(serializers.ModelSerializer):
    _notification_type = NotificationTypeRepresentationSerializer(source="notification_type")

    @serializers.register_resource()
    def register_buttons(self, instance, request, user) -> dict[str, str]:
        if endpoint := instance.endpoint:
            if instance.is_endpoint_internal:
                return {"open_internal_resource": endpoint}
            else:
                return {"open_external_resource": endpoint}
        return {}

    class Meta:
        model = Notification
        fields = read_only_fields = (
            "id",
            "title",
            "notification_type",
            "_notification_type",
            "body",
            "user",
            "endpoint",
            "sent_web",
            "sent_email",
            "sent_mobile",
            "read",
            "created",
            "_additional_resources",
        )
