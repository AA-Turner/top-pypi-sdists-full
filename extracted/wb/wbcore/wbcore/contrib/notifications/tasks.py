from celery import shared_task
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.utils.module_loading import import_string

from wbcore.contrib.notifications.models.notification_types import (
    NotificationTypeSetting,
)
from wbcore.contrib.notifications.models.notifications import Notification
from wbcore.workers import Queue


def send_notification_email(notification: Notification):
    """Sends out a notification to the user specified inside the notification

    Args:
        notification: The notification that is going to be send
    """

    context = {
        "title": notification.title,
        "message": notification.body or "",
        "notification_share_url": notification.get_full_endpoint(as_shareable_internal_link=True),
        "notification_endpoint": notification.get_full_endpoint(),
    }
    rendered_template = get_template("notifications/notification_template.html").render(context)
    msg = EmailMultiAlternatives(
        subject=notification.title,
        body=strip_tags(rendered_template),
        from_email=getattr(settings, "WBCORE_NOTIFICATION_EMAIL_FROM", "no_reply@stainly.com"),
        to=[notification.user.email],  # type: ignore
    )
    msg.attach_alternative(rendered_template, "text/html")
    msg.send()


@shared_task(queue=Queue.HIGH_PRIORITY.value)
def send_notification_task(notification_pk: int):
    """A celery task to send out a notification via email, web or mobile

    Args:
        notification_pk: The primary key of the notification that is going to be send out
    """

    notification = Notification.objects.get(pk=notification_pk)

    notification_user_settings = NotificationTypeSetting.objects.get(
        notification_type=notification.notification_type,
        user=notification.user,
    )
    if notification_user_settings.enable_email:
        send_notification_email(notification)

    backend = import_string(settings.NOTIFICATION_BACKEND)
    backend.send_notification(notification)
