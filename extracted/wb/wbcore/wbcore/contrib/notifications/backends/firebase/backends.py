import json
import os

import firebase_admin
from django.utils.html import strip_tags
from firebase_admin import messaging
from firebase_admin.credentials import Certificate
from firebase_admin.exceptions import InvalidArgumentError

from wbcore.contrib.notifications.backends.abstract_backend import (
    AbstractNotificationBackend,
)
from wbcore.contrib.notifications.models import Notification, NotificationUserToken
from wbcore.contrib.notifications.models.notification_types import (
    NotificationTypeSetting,
)


class NotificationBackend(AbstractNotificationBackend):
    FCM_OPTIONS = messaging.FCMOptions(analytics_label="notification")

    @classmethod
    def get_firebase_app(cls, certificate: Certificate):
        try:
            return firebase_admin.get_app()
        except ValueError:
            return firebase_admin.initialize_app(certificate)

    @classmethod
    def get_firebase_credentials(cls):
        certificate = json.loads(os.environ.get("FIREBASE_SERVICE_WORKER_CREDENTIALS", "{}"))
        return Certificate(certificate)

    @classmethod
    def send_notification(cls, notification: Notification):
        app = cls.get_firebase_app(cls.get_firebase_credentials())
        notification_user_settings = NotificationTypeSetting.objects.get(
            notification_type=notification.notification_type,
            user=notification.user,
        )
        tokens = NotificationUserToken.objects.filter_for_user_settings(notification_user_settings)
        endpoint_data = {}  # Firebase can't accept non-string value
        if full_endpoint := notification.get_full_endpoint():
            endpoint_data["endpoint"] = full_endpoint
        expired_tokens = []
        for token in tokens.filter(device_type=NotificationUserToken.NotificationDeviceType.MOBILE):
            message = messaging.Message(
                notification=messaging.Notification(
                    title=notification.title,
                    body=strip_tags(notification.body or ""),
                ),
                data=endpoint_data,
                token=token.token,
                android=messaging.AndroidConfig(
                    priority="high",
                    ttl=3600,
                    notification=messaging.AndroidNotification(
                        color="#f45342",
                        default_sound=True,
                        visibility="public",
                        default_vibrate_timings=True,
                        priority="max",
                    ),
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(sound=messaging.CriticalSound("default", volume=1.0))
                    ),
                ),
                fcm_options=cls.FCM_OPTIONS,
            )
            try:
                messaging.send(message, False, app)
            except (messaging.UnregisteredError, messaging.QuotaExceededError, messaging.ThirdPartyAuthError):
                expired_tokens.append(token)
            except InvalidArgumentError:  # this happens if the body is too big for the mobile push
                pass

        for token in tokens.filter(device_type=NotificationUserToken.NotificationDeviceType.WEB):
            data = {
                "title": notification.title,
                "body": strip_tags(notification.body or ""),
                "is_endpoint_internal": (
                    "true" if notification.is_endpoint_internal else "false"
                ),  # we need the data dictionary to contains only string values, otherwise firebase API complains
            }
            data.update(endpoint_data)
            message = messaging.Message(
                data=data,
                token=token.token,
                fcm_options=cls.FCM_OPTIONS,
            )
            try:
                messaging.send(message, False, app)
            except (messaging.UnregisteredError, messaging.QuotaExceededError, messaging.ThirdPartyAuthError):
                expired_tokens.append(token)

        for expired_token in expired_tokens:
            expired_token.delete()

    @classmethod
    def get_configuration(cls) -> dict:
        return {
            "firebase_config": json.loads(os.environ.get("FIREBASE_WEB_CONFIG", "")),
            "vapid_key": os.environ.get("FIREBASE_VAPID_KEY", ""),
        }
