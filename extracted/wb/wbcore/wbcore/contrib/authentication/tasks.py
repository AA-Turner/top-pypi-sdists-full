import logging
from datetime import datetime, timedelta

from celery import shared_task
from django.utils import timezone
from dynamic_preferences.registries import global_preferences_registry

from ...workers import Queue
from .models import User

logger = logging.getLogger(__name__)


@shared_task(queue=Queue.BACKGROUND.value)
def delete_unregistered_user_account(prune_user_account_before_datetime: datetime | None = None):
    if not prune_user_account_before_datetime:
        global_preferences = global_preferences_registry.manager()
        max_hours = global_preferences["authentication__hours_before_deleting_unregistered_account"]
        prune_user_account_before_datetime = timezone.now() - timedelta(hours=max_hours)

    for user in User.objects.filter(
        date_joined__lt=prune_user_account_before_datetime, is_register=False, is_active=False
    ):
        # we wrap the deletion routine into a try catch block to avoid encountering unexpected error which would prevent the proper progression of this task
        try:
            if user.profile:
                user.profile.delete()
            user.delete()
        except Exception as e:
            logger.warning(f"Couldn't delete unregistered user {user} because of error {e}")
