import fnmatch
import uuid
import aiohttp
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Event(models.Model):
    event_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=254)
    object_type = models.CharField(max_length=254, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    account_id = models.UUIDField(null=True, blank=True)
    meta_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    registerd_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"

    def data(self) -> dict:
        return {
            "event_id":  str(self.event_id),
            "event_type": self.event_type,
            "object_type": self.object_type if self.object_type else None,
            "object_id": str(self.object_id) if self.object_id else None,
            "account_id": str(self.account_id) if self.account_id else None,
            "meta_data": self.meta_data if self.meta_data else None,
        }

    def register(self):
        push_notifications = PushNotification.actual_objects.filter(
            created_at__lte=self.created_at
        ).all()

        for push_notification in push_notifications:
            if fnmatch.fnmatch(self.event_type, push_notification.pattern):
                PushNotificationEvent.objects.get_or_create(
                    event=self, push_notification=push_notification
                )


@receiver(post_save, sender=Event)
def event_registrator(sender, **kwargs):
    event = kwargs.get("instance", None)
    if event:
        event.register()


class PushNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class PushNotification(models.Model):
    push_notification_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    callback_url = models.URLField(max_length=2000)
    pattern = models.CharField(max_length=10000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = models.Manager()
    actual_objects = PushNotificationManager()

    class Meta:
        verbose_name = "push notification"
        verbose_name_plural = "push notifications"
        unique_together = [
            'callback_url', 'pattern',
        ]


class PushNotificationEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(processed_at__isnull=True)


class PushNotificationEvent(models.Model):
    push_notification = models.ForeignKey(
        PushNotification, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    retry = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True)
    last_retried_at = models.DateTimeField(null=True)

    objects = models.Manager()
    actual_objects = PushNotificationEventManager()

    class Meta:
        verbose_name = "push notification event"
        verbose_name_plural = "push notification events"
        unique_together = ["push_notification", "event"]
        indexes = [
            models.Index(fields=["processed_at", "retry", "last_retried_at"]),
        ]

    async def post(self, session: aiohttp.ClientSession) -> aiohttp.ClientResponse:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "SpotiiPush/1.0 (https://www.spotii.me/bot.html)",
        }

        push_notification = await PushNotification.actual_objects.aget(pk=self.push_notification_id)
        event = await Event.objects.aget(pk=self.event_id)

        async with session.post(
            push_notification.callback_url,
            json=event.data(),
            headers=headers
        ) as res:
            return res
