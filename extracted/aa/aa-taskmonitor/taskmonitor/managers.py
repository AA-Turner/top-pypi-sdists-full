"""Managers for Task Monitor."""

# pylint: disable = missing-class-docstring

import datetime as dt
import json
import traceback as tb
from typing import List, Optional
from uuid import UUID

from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.db.models.functions import TruncMinute
from django.utils import timezone

from allianceauth.services.hooks import get_extension_logger
from app_utils.database import TableSizeMixin
from app_utils.logging import LoggerAddTag

from . import __title__
from .app_settings import (
    TASKMONITOR_QUEUED_TASKS_ADMIN_LIMIT,
    TASKMONITOR_REPORTS_MAX_AGE,
    TASKMONITOR_TRUNCATE_NESTED_DATA,
)
from .core import app_names, celery_queues
from .core.list_queryset import ListAsQuerySet
from .helpers import truncate_dict, truncate_list, truncate_result

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


class QueuedTaskQuerySet(models.QuerySet):
    def count(self):
        """Return cached count."""
        return celery_queues.queue_length()


class QueuedTaskManagerBase(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        """Return queryset generated from celery API."""
        if celery_queues.queue_length() > TASKMONITOR_QUEUED_TASKS_ADMIN_LIMIT:
            return self._none()
        return self.from_dto_list(celery_queues.fetch_tasks())

    @staticmethod
    def _none():
        from .models import QueuedTask

        return ListAsQuerySet([], model=QueuedTask)

    @staticmethod
    def from_dto_list(tasks: list) -> models.QuerySet:
        """Create from a list of QueuedTaskShort objects."""
        from .models import QueuedTask

        objs = [
            QueuedTask.from_dto(obj, position) for position, obj in enumerate(tasks)
        ]
        return ListAsQuerySet(objs, model=QueuedTask)


QueuedTaskManager = QueuedTaskManagerBase.from_queryset(QueuedTaskQuerySet)


class TaskLogQuerySet(models.QuerySet):
    def csv_line_generator(self, fields: List[str]):
        """Return the task logs for a CSV file line by line.
        And return the field names as first line.
        """
        field_names = [field.name for field in fields]
        yield field_names
        for obj in self.iterator():
            values = [
                value for key, value in obj.asdict().items() if key in set(field_names)
            ]
            yield values

    def aggregate_timestamp_trunc(self):
        """Aggregate timestamp trunc."""
        return (
            self.annotate(timestamp_trunc=TruncMinute("timestamp"))
            .values("timestamp_trunc")
            .annotate(task_runs=Count("id"))
        )

    def max_throughput(self) -> int:
        """Calculate the maximum throughput in task executions per minute."""
        qs = self.aggregate_timestamp_trunc().aggregate(Max("task_runs"))
        return qs["task_runs__max"]

    def avg_throughput(self) -> float:
        """Calculate the average throughput in task executions per minute."""
        qs = self.aggregate_timestamp_trunc().aggregate(Avg("task_runs"))
        return qs["task_runs__avg"]

    def oldest_date(self) -> dt.datetime:
        """Return oldest timestamp."""
        return self.aggregate(oldest=Min("timestamp"))["oldest"]

    def newest_date(self) -> dt.datetime:
        """Return newest timestamp."""
        return self.aggregate(youngest=Max("timestamp"))["youngest"]

    def filter_stale_logs(self, max_hours: int) -> models.QuerySet:
        """Filter stale logs."""
        deadline = timezone.now() - dt.timedelta(hours=max_hours)
        qs = self.filter(timestamp__lt=deadline)
        return qs


class TaskLogManagerBase(TableSizeMixin, models.Manager):
    # pylint: disable = too-many-locals, too-many-arguments
    def create_from_task(
        self,
        *,
        task_id: str,
        task_name: str,
        state: int,
        retries: int,
        priority: int,
        args: list,
        kwargs: dict,
        received: Optional[dt.datetime] = None,
        started: Optional[dt.datetime] = None,
        parent_id: Optional[str] = None,
        exception=None,
        result=None,
        current_queue_length: Optional[int] = None,
    ) -> models.Model:
        """Create new object from a celery task."""
        params = {
            "app_name": app_names.from_task_name(task_name),
            "priority": priority,
            "parent_id": UUID(parent_id) if parent_id else None,
            "received": received,
            "retries": retries,
            "started": started,
            "state": state,
            "task_id": UUID(task_id),
            "task_name": task_name,
            "timestamp": timezone.now(),
            "current_queue_length": current_queue_length,
        }
        args = args or []
        params["args"] = (
            truncate_list(args) if TASKMONITOR_TRUNCATE_NESTED_DATA else args
        )
        kwargs = kwargs or {}
        params["kwargs"] = (
            truncate_dict(kwargs) if TASKMONITOR_TRUNCATE_NESTED_DATA else kwargs
        )
        try:
            json.dumps(result, cls=DjangoJSONEncoder)
        except TypeError:
            logger.warning(
                "%s [%s]: Result was not JSON serializable and therefore discarded.",
                task_name,
                task_id,
            )
            result = None
        params["result"] = (
            truncate_result(result) if TASKMONITOR_TRUNCATE_NESTED_DATA else result
        )
        if exception:
            params["exception"] = exception.__class__.__name__
            if traceback := getattr(exception, "__traceback__"):
                params["traceback"] = "".join(
                    tb.format_exception(None, value=exception, tb=traceback)
                )
        return self.create(**params)


TaskLogManager = TaskLogManagerBase.from_queryset(TaskLogQuerySet)


class TaskStatisticManager(models.Manager):
    _CACHE_KEY = "taskmonitor-task-statistics"
    _CACHE_TIMEOUT = TASKMONITOR_REPORTS_MAX_AGE * 60

    def get_queryset(self) -> models.QuerySet:
        """Return queryset with generated data from statistics query."""
        from .models import TaskStatistic

        objs = cache.get_or_set(
            key=self._CACHE_KEY, default=self._run_query, timeout=self._CACHE_TIMEOUT
        )

        return ListAsQuerySet(objs, model=TaskStatistic)

    @classmethod
    def refresh_cache(cls):
        """Update the query cache."""
        cache.set(
            key=cls._CACHE_KEY, value=cls._run_query(), timeout=cls._CACHE_TIMEOUT
        )

    @classmethod
    def clear_cache(cls):
        """Clear the query cache."""
        cache.delete(cls._CACHE_KEY)

    @classmethod
    def cached_at(cls) -> Optional[dt.datetime]:
        """Return datetime when cache was last created or None if there is no cache."""
        seconds = cache.ttl(cls._CACHE_KEY)
        if not seconds:
            return None
        return timezone.now() - (dt.timedelta(seconds=cls._CACHE_TIMEOUT - seconds))

    @staticmethod
    def _run_query() -> list:
        from .models import TaskLog, TaskStatistic

        excluded_fields = {"id"}
        field_names = [
            field.name
            for field in TaskStatistic._meta.get_fields()
            if field.name not in excluded_fields
        ]
        query = (
            TaskLog.objects.values(name=F("task_name"))
            .annotate(app=F("app_name"))
            .annotate(runs_total=Count("pk"))
            .annotate(runs_succeeded=Count("pk", filter=Q(state=TaskLog.State.SUCCESS)))
            .annotate(runs_failed=Count("pk", filter=Q(state=TaskLog.State.FAILURE)))
            .annotate(runs_retried=Count("pk", filter=Q(state=TaskLog.State.RETRY)))
            .annotate(runtime_min=Min("runtime"))
            .annotate(runtime_avg=Avg("runtime"))
            .annotate(runtime_max=Max("runtime"))
            .annotate(runtime_total=Sum("runtime"))
            .values(*field_names)
            .order_by("name")
        )
        items = [{**obj, **{"id": num}} for num, obj in enumerate(query, start=1)]
        objs = [TaskStatistic(**obj) for obj in items]
        return objs
