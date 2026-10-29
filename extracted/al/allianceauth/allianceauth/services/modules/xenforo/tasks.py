__lazy_modules__ = ["django.contrib.auth.models"]

import logging
from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist

from allianceauth.notifications import notify
from allianceauth.services.hooks import NameFormatter

from .manager import XenForoManager
from .models import XenforoUser

if TYPE_CHECKING:
    from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class XenforoTasks:
    def __init__(self) -> None:
        pass

    @classmethod
    def delete_user(cls, user: "User", notify_user: bool = False) -> bool:
        if cls.has_account(user):
            logger.debug(f"User {user} has a XenForo account {user.xenforo.username}. Deleting.")
            if XenForoManager.disable_user(user.xenforo.username) == 200:
                user.xenforo.delete()
                if notify_user:
                    notify(user, 'XenForo Account Disabled', level='danger')
                return True
        return False

    @staticmethod
    def has_account(user: "User") -> bool:
        try:
            return user.xenforo.username != ''
        except ObjectDoesNotExist:
            return False

    @classmethod
    def disable(cls) -> None:
        logger.debug("Deleting ALL XenForo users")
        XenforoUser.objects.all().delete()

    @staticmethod
    def get_username(user: "User") -> str:
        from .auth_hooks import XenforoService
        return NameFormatter(XenforoService(), user).format_name()
