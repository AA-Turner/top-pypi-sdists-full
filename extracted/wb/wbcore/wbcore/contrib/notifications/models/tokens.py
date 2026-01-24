from django.db import models
from django.db.models.query import QuerySet

from wbcore.contrib.authentication.models.users import User
from wbcore.contrib.notifications.models.notification_types import (
    NotificationTypeSetting,
)


class NotificationUserTokenManager(models.Manager):
    def filter_for_user_settings(self, user_setting: NotificationTypeSetting) -> QuerySet["NotificationUserToken"]:
        device_type = NotificationUserToken.NotificationDeviceType
        device_types = []

        if user_setting.enable_web:
            device_types.append(device_type.WEB)

        if user_setting.enable_mobile:
            device_types.append(device_type.MOBILE)

        return self.filter(
            user=user_setting.user,
            device_type__in=device_types,
        )


class NotificationUserToken(models.Model):
    class NotificationDeviceType(models.TextChoices):
        WEB = "WEB", "Web"
        MOBILE = "MOBILE", "Mobile"

    user = models.ForeignKey(to=User, related_name="notifications_tokens", on_delete=models.CASCADE)
    token = models.CharField(max_length=256)
    device_type = models.CharField(max_length=16, choices=NotificationDeviceType.choices)

    updated = models.DateTimeField(auto_now=True)

    objects = NotificationUserTokenManager()

    def __str__(self) -> str:
        return f"{self.user}: {self.token} ({self.device_type})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "token", "device_type"], name="unique_user_token_device")
        ]
