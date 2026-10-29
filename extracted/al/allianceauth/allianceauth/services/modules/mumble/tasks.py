__lazy_modules__ = ["django.contrib.auth.models"]

import logging
from typing import TYPE_CHECKING

from django.utils import timezone

from .models import MumbleUser, TempLink, TempUser
from celery import shared_task

from django.core.exceptions import ObjectDoesNotExist

if TYPE_CHECKING:
    from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


class MumbleTasks:
    def __init__(self) -> None:
        pass

    @staticmethod
    def has_account(user: "User") -> bool:
        try:
            return user.mumble.username != ''
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def disable_mumble() -> None:
        logger.info("Deleting all MumbleUser models")
        MumbleUser.objects.all().delete()


@shared_task
def tidy_up_temp_links() -> None:
    TempLink.objects.filter(expires__lt=timezone.now()).delete()
    TempUser.objects.filter(templink__isnull=True).delete()
