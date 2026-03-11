import urllib
from contextlib import suppress
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.validators import URLValidator, ValidationError
from django.db import models
from django.db.models import BooleanField, Case, F, OuterRef, Q, Subquery, Value, When
from django.db.models.functions import Coalesce
from django.template.loader import get_template
from django.urls import Resolver404, resolve, reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.module_loading import import_string

from wbcore.contrib.authentication.models.users import User
from wbcore.contrib.notifications.backends.abstract_backend import AbstractNotificationBackend
from wbcore.contrib.notifications.models import NotificationTypeSetting
from wbcore.contrib.notifications.utils import base_domain, create_notification_type, get_checksum
from wbcore.workers import Queue


def get_notification_backend() -> AbstractNotificationBackend:
    return import_string(settings.NOTIFICATION_BACKEND)


class NotificationQueryset(models.QuerySet):
    def filter_unsent_and_due(self):
        unsent_notifications = self.filter(sent_email__isnull=True)
        return unsent_notifications.annotate(
            frequency=Coalesce(
                Subquery(
                    NotificationTypeSetting.objects.filter(
                        notification_type=OuterRef("notification_type"), user=OuterRef("user")
                    ).values("frequency")[:1]
                ),
                Value(NotificationTypeSetting.Frequency.IMMEDIATLY.value),
            ),
            allow_email=Coalesce(
                Subquery(
                    NotificationTypeSetting.objects.filter(
                        notification_type=OuterRef("notification_type"), user=OuterRef("user")
                    ).values("enable_email")[:1]
                ),
                Value(False),
            ),
            first_unsent_encounter=Coalesce(
                Subquery(
                    unsent_notifications.exclude(id=OuterRef("id"))
                    .filter(
                        user=OuterRef("user"),
                        notification_type=OuterRef("notification_type"),
                        created__lt=OuterRef("created"),
                    )
                    .order_by("created")
                    .values("created")[:1]
                ),
                F("created"),
            ),
            elapse_time=timezone.now() - F("first_unsent_encounter"),
            send_due=Case(
                When(
                    Q(frequency=NotificationTypeSetting.Frequency.IMMEDIATLY)
                    | Q(notification_type__is_important=True),
                    then=Value(True),
                ),
                When(
                    Q(frequency=NotificationTypeSetting.Frequency.HOURLY) & Q(elapse_time__gt=timedelta(hours=1)),
                    then=Value(True),
                ),
                When(
                    Q(frequency=NotificationTypeSetting.Frequency.DAILY) & Q(elapse_time__gt=timedelta(hours=24)),
                    then=Value(True),
                ),
                default=False,
                output_field=BooleanField(),
            ),
        ).filter(send_due=True, allow_email=True)


class NotificationManager(models.Manager):
    def get_queryset(self) -> NotificationQueryset:
        return NotificationQueryset(self.model, using=self._db)

    def filter_unsent_and_due(self):
        return self.get_queryset().filter_unsent_and_due()


class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(default="")
    endpoint = models.CharField(max_length=2048, null=True, blank=True)

    user = models.ForeignKey(to=User, related_name="notifications_notifications", on_delete=models.CASCADE)
    notification_type = models.ForeignKey(
        to="notifications.NotificationType", related_name="notifications", on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)
    sent_email = models.DateTimeField(null=True, blank=True)
    sent_mobile = models.DateTimeField(null=True, blank=True)
    sent_web = models.DateTimeField(null=True, blank=True)
    read = models.DateTimeField(null=True, blank=True)
    checksum = models.CharField(max_length=64)

    objects = NotificationManager()

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
            models.Index(fields=["user", "notification_type", "created"]),
            models.Index(fields=["sent_email"]),
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

    @cached_property
    def notification_setting(self) -> "NotificationTypeSetting":
        return self.notification_type.get_setting_for_user(self.user)

    @cached_property
    def shareable_link(self) -> str | None:
        return self.get_full_endpoint(as_shareable_internal_link=True)

    @cached_property
    def notification_link(self) -> str:
        return f"{base_domain()}?widget_endpoint={reverse('wbcore:notifications:notification-detail', args=[self.id])}"

    def save(self, *args, **kwargs):
        if not self.checksum:
            self.checksum = self.get_checksum()
        super().save(*args, **kwargs)

    def has_email_duplicated(self, interval: int = 60 * 4) -> bool:
        return (
            Notification.objects.exclude(id=self.id)
            .filter(
                user=self.user,
                notification_type=self.notification_type,
                checksum=self.checksum,
                sent_email__isnull=False,
                created__gt=self.created - timedelta(minutes=interval),
                created__lt=self.created + timedelta(minutes=interval),
            )
            .exists()
        )

    def send_email(self):
        """Sends out a notification to the user specified inside the notification"""

        if not self.notification_setting.enable_email:
            raise ValueError("This notification cannot be sent by email")
        if not self.has_email_duplicated():
            rendered_template = get_template("notifications/notification_template.html").render({"notification": self})
            msg = EmailMultiAlternatives(
                subject=self.title,
                body=strip_tags(rendered_template),
                from_email=getattr(settings, "WBCORE_NOTIFICATION_EMAIL_FROM", "no_reply@stainly.com"),
                to=[self.user.email],  # type: ignore
            )
            msg.attach_alternative(rendered_template, "text/html")
            msg.send()
            self.sent_email = timezone.now()
            self.save()

    def send_web(self):
        if not self.notification_setting.enable_web:
            raise ValueError("This notification cannot be sent by web")
        get_notification_backend().send_web_notification(self)
        self.sent_web = timezone.now()
        self.save()

    def send_mobile(self):
        if not self.notification_setting.enable_mobile:
            raise ValueError("This notification cannot be sent by mobile")
        get_notification_backend().send_mobile_notification(self)
        # mark this notification as sent
        self.sent_mobile = timezone.now()
        self.save()

    def send(self):
        if self.notification_setting.enable_web:
            self.send_web()
        if self.notification_setting.enable_mobile:
            self.send_mobile()
        if self.notification_setting.enable_email and (
            self.notification_setting.frequency == NotificationTypeSetting.Frequency.IMMEDIATLY
            or self.notification_type.is_important
        ):
            self.send_email()

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
