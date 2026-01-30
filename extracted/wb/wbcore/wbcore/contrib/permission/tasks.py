from celery import shared_task
from tqdm import tqdm

from wbcore.contrib.permission.models.mixins import PermissionObjectModelMixin
from wbcore.utils.itertools import get_inheriting_subclasses
from wbcore.workers import Queue


@shared_task(queue=Queue.EXTENDED_BACKGROUND.value)
def reload_permissions_as_task(
    prune_existing: bool | None = True, force_pruning: bool | None = False, debug: bool = False
):
    for subclass in get_inheriting_subclasses(PermissionObjectModelMixin):
        gen = subclass.objects.iterator()
        if debug:
            gen = tqdm(gen, total=subclass.objects.count())
        for instance in gen:
            instance.reload_permissions(prune_existing=prune_existing, force_pruning=force_pruning)
