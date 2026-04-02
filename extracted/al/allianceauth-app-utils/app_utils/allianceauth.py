"""Utilities related to Alliance Auth."""

# pylint: disable=unused-import

from functools import partial
from typing import Optional

from redis import Redis

from django.contrib.auth.models import Permission, User
from django.core.cache import caches

from allianceauth.notifications import notify
from allianceauth.views import NightModeRedirectView

from ._app_settings import APP_UTILS_NOTIFY_THROTTLED_TIMEOUT
from .django import users_with_permission
from .helpers import throttle
from .testing import create_fake_user  # noqa: F401

try:
    import django_redis
except ImportError:
    django_redis = None


def notify_admins(message: str, title: str, level: str = "info") -> None:
    """Send notification to all admins.

    Args:
        message: Message text
        title: Message title
        level: Notification level of the message.
    """
    try:
        perm = Permission.objects.get(codename="logging_notifications")
    except Permission.DoesNotExist:
        users = User.objects.filter(is_superuser=True)
    else:
        users = users_with_permission(perm)
    for user in users:
        notify(user, title=title, message=message, level=level)


def notify_admins_throttled(
    message_id: str,
    message: str,
    title: str,
    level: str = "info",
    timeout: Optional[int] = None,
):
    """Send notification to all admins, but limits the frequency
    for sending messages with the same message ID, e.g. to once per day.

    If this function is called during a timeout the notification will simply be ignored.

    Args:
        message_id: ID representing this message
        message: Message text
        title: Message title
        level: Notification level of the message.
        timeout: Time between each notification, e.g. 86400 = once per day.\
            When not provided uses system default,\
            which is 86400 and can also be set via this Django setting:\
            APP_UTILS_NOTIFY_THROTTLED_TIMEOUT
    """
    if not timeout:
        timeout = APP_UTILS_NOTIFY_THROTTLED_TIMEOUT
    throttle(
        func=partial(notify_admins, message, title, level),
        context_id=message_id,
        timeout=timeout,
    )


def notify_throttled(
    message_id: str,
    user: User,
    title: str,
    message: str,
    level: str = "info",
    timeout: Optional[int] = None,
):
    """Send notification to user, but limits the frequency
    for sending messages with the same message ID, e.g. to once per day.

    If this function is called during a timeout the notification will simply be ignored.

    Args:
        message_id: ID representing this message
        title: Message title
        message: Message text
        level: Notification level of the message.
        timeout: Time between each notification, e.g. 86400 = once per day.\
            When not provided uses system default,\
            which is 86400 and can also be set via this Django setting:\
            APP_UTILS_NOTIFY_THROTTLED_TIMEOUT
    """
    if not timeout:
        timeout = APP_UTILS_NOTIFY_THROTTLED_TIMEOUT
    throttle(
        func=partial(notify, user, title, message, level),
        context_id=message_id,
        timeout=timeout,
    )


def is_night_mode(request) -> bool:
    """Returns True if the current user session is in night mode, else False"""
    return NightModeRedirectView.night_mode_state(request)


def get_redis_client() -> Redis:
    """Return configured redis client used for Django caching in Alliance Auth."""
    try:
        return django_redis.get_redis_connection("default")  # type: ignore
    except AttributeError:
        default_cache = caches["default"]
        return default_cache.get_master_client()  # type: ignore
