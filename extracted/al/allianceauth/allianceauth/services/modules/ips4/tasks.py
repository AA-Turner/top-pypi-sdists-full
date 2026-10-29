__lazy_modules__ = ["django.contrib.auth.models"]

import logging
from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist

from allianceauth.services.hooks import NameFormatter

from .manager import Ips4Manager
from .models import Ips4User

if TYPE_CHECKING:
    from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class Ips4Tasks:
    def __init__(self) -> None:
        pass

    @classmethod
    def delete_user(cls, user: "User") -> bool:
        logging.debug(f"Attempting to delete IPS4 account for {user}")
        if cls.has_account(user) and Ips4Manager.delete_user(user.ips4.id):
            user.ips4.delete()
            logger.info(f"Successfully deactivated IPS4 for user {user}")
            return True
        return False

    @staticmethod
    def has_account(user: "User") -> bool:
        try:
            return user.ips4.id != ''
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def disable() -> None:
        logging.debug("Deleting all IPS4 users")
        Ips4User.objects.all().delete()

    @staticmethod
    def get_username(user: "User") -> str:
        from .auth_hooks import Ips4Service
        return NameFormatter(Ips4Service(), user).format_name()
