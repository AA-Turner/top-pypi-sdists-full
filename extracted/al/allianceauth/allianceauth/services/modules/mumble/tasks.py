import logging

from django.utils import timezone

from .models import MumbleUser, TempLink, TempUser
from celery import shared_task

from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


class MumbleTasks:
    def __init__(self):
        pass

    @staticmethod
    def has_account(user):
        try:
            return user.mumble.username != ''
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def disable_mumble():
        logger.info("Deleting all MumbleUser models")
        MumbleUser.objects.all().delete()


@shared_task
def tidy_up_temp_links() -> None:
    TempLink.objects.filter(expires__lt=timezone.now()).delete()
    TempUser.objects.filter(templink__isnull=True).delete()
