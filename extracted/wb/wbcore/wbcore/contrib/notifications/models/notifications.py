import urllib
from contextlib import suppress

from django.core.validators import URLValidator, ValidationError
from django.db import models
from django.urls import Resolver404, resolve
from django.utils.functional import cached_property

from wbcore.contrib.authentication.models.users import User
from wbcore.contrib.notifications.utils import base_domain, create_notification_type


class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)

    user = models.ForeignKey(to=User, related_name="notifications_notifications", on_delete=models.CASCADE)
    notification_type = models.ForeignKey(
        to="notifications.NotificationType", related_name="notifications", on_delete=models.CASCADE
    )
    endpoint = models.CharField(max_length=2048, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True, blank=True)
    read = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user} {self.title}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

        notification_types = [
            create_notification_type(
                "workbench.system",
                "System Notifications",
                "System Notifications.",
                True,
                True,
                False,
            ),
        ]

    @cached_property
    def is_endpoint_internal(self) -> bool:
        with suppress(Resolver404):
            if self.endpoint:
                resolve(
                    urllib.parse.urlsplit(urllib.parse.unquote(self.endpoint)).path
                )  # we need to truncate query parameters
                return True
        return False

    @cached_property
    def is_endpoint_valid(self) -> bool:
        try:
            URLValidator()(self.endpoint)
            return True
        except ValidationError:
            return False

    def get_full_endpoint(self, as_shareable_internal_link: bool = False) -> str | None:
        if self.is_endpoint_internal:
            if as_shareable_internal_link:
                return f"{base_domain()}?widget_endpoint={self.endpoint}"
            else:
                return f"{base_domain()}{self.endpoint}"
        elif self.is_endpoint_valid:
            return self.endpoint

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "wbcore:notifications:notification"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{title}}"
