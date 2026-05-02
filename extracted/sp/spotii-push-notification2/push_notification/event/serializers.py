from push_notification.event.models import PushNotification
from rest_framework import serializers


class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotification
        fields = ['push_notification_id', 'callback_url', 'pattern', 'deleted_at']
        read_only_fields = ['push_notification_id', 'deleted_at']
        validators = [
        ]
