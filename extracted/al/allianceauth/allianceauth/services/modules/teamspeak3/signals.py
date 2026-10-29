__lazy_modules__ = ["allianceauth.authentication.models", "django.contrib.auth.models"]

import logging
from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from allianceauth.authentication.signals import state_changed

from .models import AuthTS, StateGroup
from .tasks import Teamspeak3Tasks

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from allianceauth.authentication.models import State

logger = logging.getLogger(__name__)


def trigger_all_ts_update() -> None:
    logger.debug("Triggering update_all_groups")
    Teamspeak3Tasks.update_all_groups()


@receiver(m2m_changed, sender=AuthTS.ts_group.through)
def m2m_changed_authts_group(sender: type, instance: AuthTS, action: str, *args, **kwargs) -> None:
    logger.debug(f"Received m2m_changed from {instance} ts_group with action {action}")
    if action == "post_add" or action == "post_remove":
        transaction.on_commit(trigger_all_ts_update)


@receiver(post_save, sender=AuthTS)
def post_save_authts(sender: type[AuthTS], instance: AuthTS, *args, **kwargs) -> None:
    logger.debug(f"Received post_save from {instance}")
    transaction.on_commit(trigger_all_ts_update)


@receiver(post_delete, sender=AuthTS)
def post_delete_authts(sender: type[AuthTS], instance: AuthTS, *args, **kwargs) -> None:
    logger.debug(f"Received post_delete signal from {instance}")
    transaction.on_commit(trigger_all_ts_update)


# it's literally the same logic so just recycle the receiver
post_save.connect(post_save_authts, sender=StateGroup)
post_delete.connect(post_delete_authts, sender=StateGroup)


@receiver(state_changed)
def check_groups_on_state_change(sender, user: "User", state: "State", **kwargs) -> None:
    def trigger_update() -> None:
        Teamspeak3Tasks.update_groups.delay(user.pk)
    logger.debug(f"Received state_changed signal from {user}")
    transaction.on_commit(trigger_update)
