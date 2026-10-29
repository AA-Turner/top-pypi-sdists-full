__lazy_modules__ = ["allianceauth.authentication.models", "django.contrib.auth.models"]

import logging
from typing import TYPE_CHECKING

from django.contrib.auth.models import Group  # Signals must fire on Base Models, not proxies
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from allianceauth.authentication.signals import state_changed

from .models import AuthGroup, ReservedGroupName

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from allianceauth.authentication.models import State

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Group)
def find_new_name_for_conflicting_groups(sender: type[Group], instance: Group, **kwargs) -> None:
    """Find new name for a group which name is already reserved."""
    new_name = instance.name
    num = 0
    while ReservedGroupName.objects.filter(name__iexact=new_name).exists():
        num += 1
        new_name = f"{instance.name}_{num}"
    instance.name = new_name


@receiver(post_save, sender=Group)
def create_auth_group(sender: type[Group], instance: Group, created: bool, **kwargs) -> None:
    """Create the AuthGroup model when a group is created."""
    if created:
        AuthGroup.objects.create(group=instance)


@receiver(state_changed)
def check_groups_on_state_change(sender, user: "User", state: "State", **kwargs) -> None:
    logger.debug(
        f"Checking group memberships for {user} based on new state {state}"
    )
    state_groups = (
        user.groups.select_related("authgroup").exclude(authgroup__states=None)
    )
    for group in state_groups:
        if not group.authgroup.states.filter(id=state.id).exists():
            logger.info(
                f"Removing user {user} from group {group} due to missing state"
            )
            user.groups.remove(group)
