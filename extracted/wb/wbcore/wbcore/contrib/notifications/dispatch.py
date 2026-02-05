from typing import Iterable

from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.dispatch import receiver
from django.utils.module_loading import import_string
from django.utils.translation import gettext
from rest_framework.reverse import reverse

from wbcore.contrib.authentication.models.users import User
from wbcore.shares.signals import handle_widget_sharing

from ...workers import Queue
from .models import NotificationType
from .models.notifications import Notification, send_notification_as_task


def get_user(u: User | int) -> User:
    if isinstance(u, User):
        return u
    elif isinstance(u, int):
        return User.objects.get(id=u)
    raise ValueError("Invalid user type")


@shared_task(queue=Queue.HIGH_PRIORITY.value)
def send_notification(
    code: str,
    title: str,
    body: str,
    user: User | Iterable[User | int] | int,
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
    users = []
    if isinstance(user, list):
        for u in user:
            users.append(get_user(u))
    else:
        users.append(get_user(user))

    for user in users:
        notification_type = NotificationType.objects.get(code=code)
        if user.is_active:
            if not endpoint:
                endpoint = reverse(reverse_name, reverse_args, reverse_kwargs) if reverse_name else None
            notification = Notification.objects.create(
                title=title,
                body=body,
                user=user,
                notification_type=notification_type,
                endpoint=endpoint,
            )
            transaction.on_commit(
                lambda notification_pk=notification.pk: send_notification_as_task.delay(notification_pk)
            )


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
