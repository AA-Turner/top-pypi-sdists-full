__lazy_modules__ = ["celery"]

import logging
from typing import TYPE_CHECKING

from celery import shared_task

from django.core.exceptions import ObjectDoesNotExist

from allianceauth.authentication.models import User
from allianceauth.notifications import notify
from allianceauth.services.hooks import NameFormatter
from allianceauth.services.tasks import QueueOnce

from .manager import Phpbb3Manager
from .models import Phpbb3User

if TYPE_CHECKING:
    from celery import Task

    # https://github.com/sbdchd/celery-types
    classes = [
        Task,
    ]

    for cls in classes:
        setattr(cls, "__class_getitem__", classmethod(lambda cls, *args, **kwargs: cls))

logger = logging.getLogger(__name__)


class Phpbb3Tasks:
    def __init__(self) -> None:
        pass

    @classmethod
    def delete_user(cls, user: User, notify_user: bool = False) -> bool:
        if cls.has_account(user):
            logger.debug(f"User {user} has forum account {user.phpbb3.username}. Deleting.")
            if Phpbb3Manager.disable_user(user.phpbb3.username):
                user.phpbb3.delete()
                if notify_user:
                    notify(user, 'Forum Account Disabled', level='danger')
                return True
        return False

    @staticmethod
    def has_account(user: User) -> bool:
        try:
            return user.phpbb3.username != ''
        except ObjectDoesNotExist:
            return False

    @staticmethod
    @shared_task(bind=True, name="phpbb3.update_groups", base=QueueOnce)
    def update_groups(self: "Task", pk: int) -> None:
        user = User.objects.get(pk=pk)
        logger.debug(f"Updating phpbb3 groups for user {user}")
        if Phpbb3Tasks.has_account(user):
            groups = [user.profile.state.name]
            for group in user.groups.all():
                groups.append(str(group.name))
            logger.debug(f"Updating user {user} phpbb3 groups to {groups}")
            try:
                Phpbb3Manager.update_groups(user.phpbb3.username, groups)
            except Exception as e:
                logger.exception(f"Phpbb group sync failed for {user}, retrying in 10 mins")
                raise self.retry(exc=e, countdown=60 * 10) from e
            logger.debug(f"Updated user {user} phpbb3 groups.")
        else:
            logger.debug("User does not have a Phpbb3 account")

    @staticmethod
    @shared_task(name="phpbb3.update_all_groups")
    def update_all_groups() -> None:
        logger.debug("Updating ALL phpbb3 groups")
        for user in Phpbb3User.objects.exclude(username__exact=''):
            Phpbb3Tasks.update_groups.delay(user.user_id)

    @staticmethod
    def disable() -> None:
        Phpbb3User.objects.all().delete()

    @staticmethod
    def get_username(user: User) -> str:
        from .auth_hooks import Phpbb3Service
        return NameFormatter(Phpbb3Service(), user).format_name()
