__lazy_modules__ = ["celery"]

import logging
from typing import TYPE_CHECKING

from celery import shared_task
from celery_once import AlreadyQueued, QueueOnce as BaseTask

from django.core.cache import cache

from allianceauth.authentication.models import User

from .hooks import ServicesHook

if TYPE_CHECKING:
    from celery import Task

    # https://github.com/sbdchd/celery-types
    classes = [
        Task,
    ]

    for cls in classes:
        setattr(cls, "__class_getitem__", classmethod(lambda cls, *args, **kwargs: cls))

logger = logging.getLogger(__name__)


class QueueOnce(BaseTask):
    once = BaseTask.once
    once['graceful'] = True


class DjangoBackend:
    def __init__(self, settings) -> None:
        pass

    @staticmethod
    def raise_or_lock(key: str, timeout: int) -> None:
        acquired = cache.add(key=key, value="lock", timeout=timeout)
        if not acquired:
            raise AlreadyQueued(int(cache.ttl(key)))

    @staticmethod
    def clear_lock(key: str) -> bool:
        return cache.delete(key)


@shared_task(bind=True)
def validate_services(self: "Task", pk: int) -> None:
    user = User.objects.get(pk=pk)
    logger.debug(f'Ensuring user {user} has permissions for active services')
    # Iterate through services hooks and have them check the validity of the user
    for svc in ServicesHook.get_services():
        try:
            svc.validate_user(user)
        except Exception:
            logger.exception(f'Exception running validate_user for services module {svc} on user {user}')


def disable_user(user: User) -> None:
    logger.debug(f'Disabling all services for user {user}')
    for svc in ServicesHook.get_services():
        if svc.service_active_for_user(user):
            svc.delete_user(user)


@shared_task
def update_groups_for_user(user_pk: int) -> None:
    """Update groups for all services registered to a user."""
    user = User.objects.get(pk=user_pk)
    logger.debug("%s: Triggering service group update for user", user)
    for svc in ServicesHook.get_services():
        try:
            svc.validate_user(user)
            svc.update_groups(user)
        except Exception:
            logger.exception(
                'Exception running update_groups for services module %s on user %s',
                svc,
                user
            )
