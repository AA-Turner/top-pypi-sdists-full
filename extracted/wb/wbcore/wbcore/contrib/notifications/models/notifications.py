import urllib
from contextlib import suppress
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.validators import URLValidator, ValidationError
from django.db import models
from django.template.loader import get_template
from django.urls import Resolver404, resolve
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.module_loading import import_string

from wbcore.contrib.authentication.models.users import User
from wbcore.contrib.notifications.utils import base_domain, create_notification_type, get_checksum
from wbcore.workers import Queue


class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(default="")
    endpoint = models.CharField(max_length=2048, null=True, blank=True)

    user = models.ForeignKey(to=User, related_name="notifications_notifications", on_delete=models.CASCADE)
    notification_type = models.ForeignKey(
        to="notifications.NotificationType", related_name="notifications", on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True, blank=True)
    read = models.DateTimeField(null=True, blank=True)
    checksum = models.CharField(max_length=64)

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
        indexes = [
            models.Index(fields=["user", "notification_type", "checksum"]),
        ]
        # constraints = [
        #     models.UniqueConstraint(fields=["user", "checksum"], name="checksum_unique"),
        # ]

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

    def _send_as_mail(self):
        """Sends out a notification to the user specified inside the notification"""

        context = {
            "title": self.title,
            "message": self.body or "",
            "notification_share_url": self.get_full_endpoint(as_shareable_internal_link=True),
            "notification_endpoint": self.get_full_endpoint(),
        }
        rendered_template = get_template("notifications/notification_template.html").render(context)
        msg = EmailMultiAlternatives(
            subject=self.title,
            body=strip_tags(rendered_template),
            from_email=getattr(settings, "WBCORE_NOTIFICATION_EMAIL_FROM", "no_reply@stainly.com"),
            to=[self.user.email],  # type: ignore
        )
        msg.attach_alternative(rendered_template, "text/html")
        msg.send()

    def save(self, *args, **kwargs):
        if not self.checksum:
            self.checksum = self.get_checksum()
        super().save(*args, **kwargs)

    def has_duplicated(self, interval: int = 60 * 4) -> bool:
        return (
            Notification.objects.exclude(id=self.id)
            .filter(
                user=self.user,
                notification_type=self.notification_type,
                checksum=self.checksum,
                sent__isnull=False,
                created__gt=self.created - timedelta(minutes=interval),
                created__lt=self.created + timedelta(minutes=interval),
            )
            .exists()
        )

    def send(self):
        notification_user_setting = self.notification_type.get_setting_for_user(self.user)

        # we do not sent notification through email if we detect similar already sent notification
        if notification_user_setting.enable_email and not self.has_duplicated():
            self._send_as_mail()
        if notification_user_setting.enable_web or notification_user_setting.enable_mobile:
            backend = import_string(settings.NOTIFICATION_BACKEND)
            backend.send_notification(self)

        # mark this notification as sent
        self.sent = timezone.now()
        self.save()

    def get_checksum(self) -> str:
        return get_checksum(self.title, self.body, self.endpoint)

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


@shared_task(queue=Queue.HIGH_PRIORITY.value)
def send_notification_as_task(notification_pk: int):
    """A celery task to send out a notification via email, web or mobile

    Args:
        notification_pk: The primary key of the notification that is going to be send out
    """

    notification = Notification.objects.get(pk=notification_pk)
    notification.send()
