"""Create task logs from executed celery tasks."""

from django.core.cache import cache
from django.utils import timezone

from taskmonitor.app_settings import (
    TASKMONITOR_ENABLED,
    TASKMONITOR_HOUSEKEEPING_FREQUENCY,
)
from taskmonitor.models import TaskLog
from taskmonitor.tasks import DEFAULT_TASK_PRIORITY, run_housekeeping

from . import celery_queues, task_records

TASK_RECEIVED = "received"
TASK_STARTED = "started"

CACHE_KEY = "taskmonitor_last_housekeeping"


def run_when_enabled(func):
    """Run when Task monitor is enabled only. Else abort silently."""

    def wrapper(*args, **kwargs):
        if TASKMONITOR_ENABLED:
            func(*args, **kwargs)

    return wrapper


@run_when_enabled
def task_received_handler_2(request):
    """Handle task received signal."""
    if request:
        task_records.set(request.id, TASK_RECEIVED, timezone.now())


@run_when_enabled
def task_prerun_handler_2(task_id):
    """Handle task prerun signal."""
    if task_id:
        task_records.set(task_id, TASK_STARTED, timezone.now())


@run_when_enabled
def task_success_handler_2(sender, result):
    """Handle task success signal."""
    if sender and sender.request:
        request = sender.request
        task_id = request.id
        TaskLog.objects.create_from_task(
            task_id=task_id,
            task_name=sender.name,
            state=TaskLog.State.SUCCESS,
            retries=request.retries,
            priority=request.delivery_info["priority"],
            parent_id=request.parent_id,
            received=task_records.fetch(task_id, TASK_RECEIVED),
            started=task_records.fetch(task_id, TASK_STARTED),
            args=request.args,
            kwargs=request.kwargs,
            result=result,
            current_queue_length=celery_queues.queue_length_cached(),
        )
    _run_housekeeping_if_stale()


@run_when_enabled
def task_retry_handler_2(sender, request, reason):
    """Handle task retry signal."""
    if sender and request:
        task_id = request.id
        TaskLog.objects.create_from_task(
            task_id=task_id,
            task_name=sender.name,
            state=TaskLog.State.RETRY,
            retries=request.retries,
            priority=request.delivery_info["priority"],
            parent_id=request.parent_id,
            received=task_records.fetch(task_id, TASK_RECEIVED),
            started=task_records.fetch(task_id, TASK_STARTED),
            args=request.args,
            kwargs=request.kwargs,
            exception=reason,
            current_queue_length=celery_queues.queue_length_cached(),
        )
    _run_housekeeping_if_stale()


@run_when_enabled
def task_failure_handler_2(sender, task_id, exception):
    """Handle task failure signal."""
    if sender and task_id:
        request = sender.request
        priority = (
            request.delivery_info.get("priority") if request.delivery_info else None
        )
        TaskLog.objects.create_from_task(
            task_id=task_id,
            task_name=sender.name,
            state=TaskLog.State.FAILURE,
            retries=request.retries,
            priority=priority,
            parent_id=request.parent_id,
            received=task_records.fetch(task_id, TASK_RECEIVED),
            started=task_records.fetch(task_id, TASK_STARTED),
            args=request.args,
            kwargs=request.kwargs,
            exception=exception,
            current_queue_length=celery_queues.queue_length_cached(),
        )
    _run_housekeeping_if_stale()


@run_when_enabled
def task_internal_error_handler_2(sender, task_id, request, exception):
    """Handle task internal error signal."""
    if task_id and request:
        try:
            priority = (
                request["delivery_info"].get("priority")
                if request["delivery_info"]
                else None
            )
        except KeyError:
            priority = None
        TaskLog.objects.create_from_task(
            task_id=task_id,
            task_name=sender.name if sender else "?",
            state=TaskLog.State.FAILURE,
            retries=request["retries"],
            priority=priority,
            parent_id=request.get("parent_id"),
            received=task_records.fetch(task_id, TASK_RECEIVED),
            started=task_records.fetch(task_id, TASK_STARTED),
            args=request.get("args", []),
            kwargs=request.get("kwargs", {}),
            exception=exception,
        )
    _run_housekeeping_if_stale()


def _run_housekeeping_if_stale():
    """Spawn a task to run house keeping if last run was too long ago."""
    was_expired = cache.add(
        key=CACHE_KEY,
        value="no-value",
        timeout=TASKMONITOR_HOUSEKEEPING_FREQUENCY * 60,
    )
    if was_expired:
        run_housekeeping.apply_async(priority=DEFAULT_TASK_PRIORITY)


# def request_asdict(request) -> dict:
#     """Convert a request object into a dict."""
#     return {
#         "delivery_info": request.delivery_info,
#         "retries": request.retries,
#         "parent_id": request.parent_id,
#     }
