"""Tasks for Task Monitor."""

from celery import chain, shared_task

from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce
from app_utils.helpers import chunks
from app_utils.logging import LoggerAddTag

from . import __title__
from .app_settings import TASKMONITOR_DATA_MAX_AGE, TASKMONITOR_DELETE_STALE_BATCH_SIZE
from .core import cached_reports
from .models import TaskLog, TaskStatistic

logger = LoggerAddTag(get_extension_logger(__name__), __title__)

DEFAULT_TASK_PRIORITY = 4


@shared_task(base=QueueOnce)
def run_housekeeping():
    """Run all housekeeping tasks."""
    delete_stale_tasklogs.apply_async(priority=DEFAULT_TASK_PRIORITY)
    refresh_cached_data.apply_async(priority=DEFAULT_TASK_PRIORITY)


# @shared_task
# def delete_stale_tasklogs():
#     """Delete all stale tasklogs from the database."""
#     log_pks = TaskLog.objects.filter(
#         timestamp__lte=timezone.now() - dt.timedelta(hours=TASKMONITOR_DATA_MAX_AGE)
#     ).values_list("pk", flat=True)
#     for log_pks_chunk in chunks(log_pks, TASKMONITOR_DELETE_STALE_BATCH_SIZE):
#         delete_tasklogs_batch.apply_async(priority=7, kwargs={"log_pks": log_pks_chunk})


# @shared_task
# def delete_tasklogs_batch(log_pks: list):
#     """Delete a selection of tasklogs."""
#     logs_to_delete = TaskLog.objects.filter(pk__in=log_pks)
#     logger.info(f"Deleting {logs_to_delete.count():,} stale tasklogs.")
#     logs_to_delete._raw_delete(logs_to_delete.db)


@shared_task(base=QueueOnce)
def delete_stale_tasklogs():
    """Delete stale logs in batches.

    Will spawn itself again and again until all stale logs are deleted.
    """

    stale_logs = TaskLog.objects.filter_stale_logs(max_hours=TASKMONITOR_DATA_MAX_AGE)
    if not stale_logs.exists():
        logger.info("There currently are no stale application logs.")
        return

    stale_logs_pks = list(stale_logs.values_list("pk", flat=True))
    for pks_to_delete in chunks(stale_logs_pks, TASKMONITOR_DELETE_STALE_BATCH_SIZE):
        qs_to_delete = TaskLog.objects.filter(pk__in=pks_to_delete)
        qs_to_delete._raw_delete(qs_to_delete.db)  # pylint: disable = protected-access
        logger.info("Deleted %d stale task logs.", len(pks_to_delete))


@shared_task
def refresh_cached_data():
    """Refresh cached data incl. reports."""

    tasks = [
        refresh_single_report_cache.si(report.name).set(priority=DEFAULT_TASK_PRIORITY)
        for report in cached_reports.reports()
    ]
    tasks.append(refresh_statistics_cache.si().set(priority=DEFAULT_TASK_PRIORITY))
    chain(tasks).delay()


@shared_task(base=QueueOnce)
def refresh_single_report_cache(report_name: str):
    """Refresh cache for given report."""
    cached_reports.report(report_name).refresh_cache()
    logger.info(f"Refreshed reports cache of {report_name}.")


@shared_task(base=QueueOnce)
def refresh_statistics_cache():
    """Refresh cache for given report."""
    TaskStatistic.objects.refresh_cache()
    logger.info("Refreshed statistics cache.")
