from typing import Iterable

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.dispatch import receiver
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.translation import gettext
from rest_framework.reverse import reverse

from wbcore.shares.signals import handle_widget_sharing

from .models import Notification, NotificationType, NotificationTypeSetting
from .tasks import send_notification_task

User = get_user_model()


def send_notification(
    code: str,
    title: str,
    body: str,
    user: User | Iterable[User],
    reverse_name: str | None = None,
    reverse_args=None,
    reverse_kwargs=None,
    endpoint: str | None = None,
):
    """Method for dispatching a notification

    Args:
        code: The code pointing to a `NotificationType`
        title: The title of the notification
        body: The text of the notification
        user: The users that should receive the notification. Can either be a User object or an iterable of User objects
        reverse_name: The reverse name of an endpoint attached to this notification
        reverse_args: The arguments passed to the `reverse` function
        reverse_kwargs: The keyword arguments passed to the `reverse` function
        endpoint: The endpoint of resource. If provided, reverse_name + args + kwargs are disregarded
    """
    users = user
    if isinstance(users, User):
        users = [users]
    for user in users:
        notification_type = NotificationType.objects.get(code=code)
        if (
            user.is_active
            and NotificationTypeSetting.objects.filter(notification_type=notification_type, user=user).exists()
        ):
            if not endpoint:
                endpoint = reverse(reverse_name, reverse_args, reverse_kwargs) if reverse_name else None
            notification = Notification.objects.create(
                title=title,
                body=body,
                user=user,
                notification_type=notification_type,
                endpoint=endpoint,
                sent=timezone.now(),
            )
            transaction.on_commit(lambda: send_notification_task.delay(notification.pk))


@receiver(handle_widget_sharing)
def share_notification(
    request, widget_relative_endpoint, share=False, share_message=None, share_recipients=None, **kwargs
):
    if share and share_recipients and share_message:
        for recipient in share_recipients:
            send_notification(
                code="workbench.system",
                title=gettext("{} shared a widget with you").format(
                    import_string(settings.WBCORE_DEFAULT_USER_NAME)(request.user)
                ),
                user=recipient,
                body=share_message,
                endpoint=widget_relative_endpoint,
            )
