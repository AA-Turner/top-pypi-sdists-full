from contextlib import suppress
from datetime import timedelta

from celery import shared_task
from django.db.models import ProtectedError
from django.utils import timezone
from dynamic_preferences.registries import global_preferences_registry
from tqdm import tqdm

from wbcore.cache.registry import periodic_cache_registry
from wbcore.models import DynamicModel
from wbcore.utils.itertools import get_inheriting_subclasses
from wbcore.utils.models import ComplexToStringMixin, DeleteToDisableMixin
from wbcore.workers import Queue


@shared_task(queue=Queue.EXTENDED_BACKGROUND.value)
def recompute_latest_modified_dynamic_fields(from_datetime=None, to_datetime=None, timedelta_days=1):
    """
    Daily (expected frequency) recompute of all dynamic model objects that falls within the specified time frame (default to the last 24h).
    For each recently modified object, a subroutine sends a signal to get the dependant object to be recomputed
    Args:
        from_datetime: A datetime, default to today - 24h
        to_datetime: A Datetime, default to today
        timedelta_days: time range, default to 24h
    """
    if not to_datetime:
        to_datetime = timezone.now()
    if not from_datetime:
        from_datetime = timezone.now() - timedelta(days=timedelta_days)

    if from_datetime >= to_datetime:
        raise ValueError("From date needs to be strictly lower than To date")

    # already_updated_objects = set() # We don't pass the list anymore because of in memory issue. For instrument price, we extend 10GB. We migh want to implement a non deterministric approach with Bloom filter for instance

    for subclass in get_inheriting_subclasses(DynamicModel):
        qs = subclass.objects.filter(updated_at__gte=from_datetime, updated_at__lte=to_datetime)
        for already_updated_object in tqdm(qs.distinct().iterator(), total=qs.count()):
            DynamicModel.update_dynamic_fields_of_dependant_objects(already_updated_object)


@shared_task(queue=Queue.EXTENDED_BACKGROUND.value)
def recompute_computed_str(debug: bool = False):
    """
    When this task is executed, it will loop over all objects that inherit from ComplexToStringMixin and compare their current computed_str value with the expected one.
    If different, the expected one is saved in place.
    """
    bulk_size = 1000
    for subclass in get_inheriting_subclasses(ComplexToStringMixin):
        if getattr(subclass, "COMPUTED_STR_RECOMPUTE_PERIODICALLY", True):
            objs = []
            if debug:
                qs = tqdm(subclass.objects.iterator(), total=subclass.objects.count())
            else:
                qs = subclass.objects.iterator()
            for instance in qs:
                with suppress(Exception):  # we don't want this task to fail because of
                    new_computed_str = instance.compute_str()
                    if new_computed_str != instance.computed_str:
                        instance.computed_str = new_computed_str
                        objs.append(instance)
                    if len(objs) % bulk_size == 0:
                        subclass.objects.bulk_update(objs, ["computed_str"])
                        objs = []
            if objs:
                subclass.objects.bulk_update(objs, ["computed_str"])


@shared_task(queue=Queue.EXTENDED_BACKGROUND.value)
def clean_deleted_objects():
    """
    Periodically arise deleted objects that have passed the retention period from the database.
    """
    retention_period = global_preferences_registry.manager()["wbcore__retention_period"]
    for subclass in get_inheriting_subclasses(DeleteToDisableMixin):
        if subclass.AUTOMATICALLY_CLEAN_SOFT_DELETED_OBJECTS:
            with suppress(ProtectedError):
                subclass.all_objects.filter(
                    is_active=False, deletion_datetime__lte=timezone.now() - timedelta(days=retention_period)
                ).delete()


@shared_task(queue=Queue.EXTENDED_BACKGROUND.value)
def refetch_pandas_api_view():
    for cache_api_view in periodic_cache_registry.classes:
        cache_api_view.fetch_cache()
