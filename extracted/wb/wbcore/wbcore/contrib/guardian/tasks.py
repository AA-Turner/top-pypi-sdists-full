from celery import shared_task

from wbcore.contrib.guardian.models.mixins import PermissionObjectModelMixin
from wbcore.utils.itertools import get_inheriting_subclasses
from wbcore.workers import Queue


@shared_task(queue=Queue.EXTENDED_BACKGROUND.value)
def reload_permissions_as_task(prune_existing: bool | None = True, force_pruning: bool | None = False):
    for subclass in get_inheriting_subclasses(PermissionObjectModelMixin):
        for instance in subclass.objects.iterator():
            instance.reload_permissions(prune_existing=prune_existing, force_pruning=force_pruning)
