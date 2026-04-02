"""Container for caching the reports data used in views."""

# pylint: disable = missing-class-docstring

import datetime as dt
import inspect
import re
import sys
from collections import defaultdict
from statistics import mean
from typing import Callable, Iterable, List, Optional, Tuple

from django.core.cache import cache
from django.db.models import Avg, Count, F, Max, Sum, Value
from django.db.models.functions import Concat, TruncMinute
from django.urls import reverse
from django.utils import timezone

from taskmonitor.app_settings import (
    TASKMONITOR_HOUSEKEEPING_FREQUENCY,
    TASKMONITOR_REPORTS_MAX_AGE,
    TASKMONITOR_REPORTS_MAX_TOP,
)
from taskmonitor.models import TaskLog

CACHE_KEY = "taskmonitor_reports_data"
MAX_APPS_COUNT = 14
APP_NAME_OTHERS = "Others"


class _CachedReport:
    """Base class for a cached report."""

    is_included = True  # whether a report is included in the main group

    def __init__(self) -> None:
        self.name = self._to_snake_case(self.__class__.__name__)

    @property
    def cache_key(self):
        """Return cache key."""
        return f"{CACHE_KEY}_{self.name}"

    @property
    def timeout(self):
        """Timeout in seconds."""
        return TASKMONITOR_REPORTS_MAX_AGE * 60

    @property
    def now(self) -> dt.datetime:
        """Return current date and time."""
        return timezone.now()

    @staticmethod
    def changelist_url() -> str:
        """Return changelist URL."""
        return reverse("admin:taskmonitor_tasklog_changelist")

    def data(self, use_cache=True):
        """Return data for this report."""
        if use_cache:
            return cache.get_or_set(
                self.cache_key, self._calc_data, timeout=self.timeout
            )
        calculated_data = self._calc_data()
        cache.set(self.cache_key, calculated_data, timeout=self.timeout)
        return calculated_data

    def refresh_cache(self) -> None:
        """Refresh the cache."""
        cache.set(self.cache_key, self._calc_data(), timeout=self.timeout)

    def clear_cache(self) -> None:
        """Clear the cache."""
        cache.delete(self.cache_key)

    def last_update_at(self) -> Optional[dt.datetime]:
        """When the cache was last updated or None if there is no cache."""
        ttl = self._ttl()
        if not ttl:
            return None
        return timezone.now() - dt.timedelta(seconds=max(0, self.timeout - ttl))

    def next_update_at(self) -> Optional[dt.datetime]:
        """When the cache will be updated next (earliest) or None if no cache."""
        ttl = self._ttl()
        if not ttl:
            return None
        duration = TASKMONITOR_HOUSEKEEPING_FREQUENCY * 60 / 2 + ttl
        return timezone.now() + dt.timedelta(seconds=duration)

    def _ttl(self):
        return cache.ttl(self.cache_key)

    def _calc_data(self):
        """Calculate data."""
        raise NotImplementedError()

    @staticmethod
    def _truncate_minutes(
        func: Callable, qs: Iterable, minutes: int = 1
    ) -> List[Tuple[int, int]]:
        """Truncate data to one aggregated value over a span of minutes.

        Result will be sorted ascending by datetime.

        Args:
            - func: function which takes a list of values and returns one value
            - values: iterable of values in the format: [{"x": 1, "y": 2}, ...]
            - minutes: number of minutes to apply the function over.
            Must be a divider of 60.

        This function is necessary, because tests show that the ORM grouping
        with TruncMinute is not reliable.
        """

        def _func_or_zero(func, lst) -> int:
            return func(lst) if lst else 0

        if 60 % minutes > 0:
            raise ValueError("minutes must be a divider of 60.")
        data_raw = defaultdict(list)
        for x, y in qs.values_list("x", "y").iterator():
            new_minutes = x.minute // minutes * minutes
            new_x = x.replace(minute=new_minutes, second=0, microsecond=0)
            x_timestamp = int(new_x.timestamp() * 1000)
            data_raw[x_timestamp].append(y)
        data_raw = dict(sorted(data_raw.items()))
        my_data = [
            tuple([x, int(round(_func_or_zero(func, values), 0))])
            for x, values in data_raw.items()
        ]
        return my_data

    @staticmethod
    def _to_snake_case(name: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

    @classmethod
    def report_classes(cls):
        """Return all known report classes."""
        return [
            obj
            for _, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass)
            if issubclass(obj, cls) and obj is not cls
        ]


class AppsTopCumRuntime(_CachedReport):
    def _calc_data(self):
        if not report("tasks_basics").data()["total_runtime"]:
            return None
        return list(
            TaskLog.objects.values(name=F("app_name"))
            .annotate(y=Sum("runtime"))
            .annotate(
                url=Concat(Value(f"{self.changelist_url()}?o=5&app_name="), F("name"))
            )
            .order_by("-y")[:TASKMONITOR_REPORTS_MAX_TOP]
        )


class AppsTopRuns(_CachedReport):
    def _calc_data(self):
        if not report("tasks_basics").data()["total_runs"]:
            return None
        return list(
            TaskLog.objects.values(name=F("app_name"))
            .annotate(y=Count("pk"))
            .annotate(
                url=Concat(Value(f"{self.changelist_url()}?app_name="), F("name"))
            )
            .order_by("-y")[:TASKMONITOR_REPORTS_MAX_TOP]
        )


class TasksBasics(_CachedReport):
    """Basic information about tasks used by many other reports."""

    def _calc_data(self):
        total_runs = TaskLog.objects.count()
        total_runtime = TaskLog.objects.aggregate(total_runtime=Sum("runtime"))[
            "total_runtime"
        ]
        oldest_date = TaskLog.objects.oldest_date()
        newest_date = TaskLog.objects.newest_date()
        return {
            "total_runs": total_runs,
            "total_runtime": total_runtime,
            "oldest_date": oldest_date,
            "newest_date": newest_date,
        }


class QueueLengthOverTime(_CachedReport):
    is_included = False

    def _calc_data(self):
        qs = (
            TaskLog.objects.exclude(current_queue_length__isnull=True)
            .order_by("timestamp")
            .annotate(x=TruncMinute("timestamp"))
            .values("x")
            .annotate(y=Avg("current_queue_length"))
        )
        my_data = self._truncate_minutes(mean, qs, 5)
        return [{"name": "length", "data": my_data}]


class TaskStatistics(_CachedReport):
    def _calc_data(self):
        qs = (
            TaskLog.objects.values("app_name", "task_name")
            .annotate(x=Count("pk"))
            .annotate(y=Avg("runtime"))
        )
        grouped_by_app = defaultdict(list)
        for obj in qs:
            point = {
                "x": obj["x"],
                "y": obj["y"],
                "task_name": obj["task_name"],
            }
            grouped_by_app[obj["app_name"]].append(point)
        my_data = [
            {"name": name, "data": data} for name, data in grouped_by_app.items()
        ]
        return my_data


class TaskRunsByState(_CachedReport):
    def _calc_data(self):
        if not report("tasks_basics").data()["total_runs"]:
            return None
        return [
            {
                "name": state.label,
                "y": TaskLog.objects.filter(state=state.value).count(),
                "url": f"{self.changelist_url()}?state__exact={state}",
            }
            for state in TaskLog.State
        ]


class TaskRunsByApp(_CachedReport):
    def _calc_data(self):
        if not report("tasks_basics").data()["total_runs"]:
            return None
        my_data = list(
            TaskLog.objects.values(name=F("app_name"))
            .annotate(y=Count("pk"))
            .annotate(
                url=Concat(Value(f"{self.changelist_url()}?app_name="), F("name"))
            )
            .order_by("-y")
        )
        if len(my_data) > MAX_APPS_COUNT:
            others_y = sum(
                (
                    app["y"]
                    for i, app in enumerate(my_data, start=1)
                    if i > MAX_APPS_COUNT
                )
            )
            return my_data[:MAX_APPS_COUNT] + [
                {"name": APP_NAME_OTHERS, "y": others_y, "url": "#"}
            ]
        return my_data


class TasksTopRuns(_CachedReport):
    def _calc_data(self):
        if not report("tasks_basics").data()["total_runs"]:
            return None
        return list(
            TaskLog.objects.values(name=F("task_name"))
            .annotate(y=Count("pk"))
            .annotate(
                url=Concat(Value(f"{self.changelist_url()}?task_name="), F("name"))
            )
            .order_by("-y")[:TASKMONITOR_REPORTS_MAX_TOP]
        )


class TasksTopAvgRuntime(_CachedReport):
    def _calc_data(self):
        if not report("tasks_basics").data()["total_runtime"]:
            return None
        return list(
            TaskLog.objects.values(name=F("task_name"))
            .annotate(y=Avg("runtime"))
            .annotate(
                url=Concat(Value(f"{self.changelist_url()}?o=5&task_name="), F("name"))
            )
            .order_by("-y")[:TASKMONITOR_REPORTS_MAX_TOP]
        )


class TasksTopCumRuntime(_CachedReport):
    def _calc_data(self):
        if not report("tasks_basics").data()["total_runtime"]:
            return None
        return list(
            TaskLog.objects.values(name=F("task_name"))
            .annotate(y=Sum("runtime"))
            .annotate(
                url=Concat(Value(f"{self.changelist_url()}?o=5&task_name="), F("name"))
            )
            .order_by("-y")[:TASKMONITOR_REPORTS_MAX_TOP]
        )


class TasksTopMaxRuntime(_CachedReport):
    def _calc_data(self):
        if not report("tasks_basics").data()["total_runtime"]:
            return None
        return list(
            TaskLog.objects.values(name=F("task_name"))
            .annotate(y=Max("runtime"))
            .annotate(
                url=Concat(Value(f"{self.changelist_url()}?o=5&task_name="), F("name"))
            )
            .order_by("-y")[:TASKMONITOR_REPORTS_MAX_TOP]
        )


class TasksTopFailed(_CachedReport):
    def _calc_data(self):
        total_failed = TaskLog.objects.filter(state=TaskLog.State.FAILURE).count()
        if not total_failed:
            return None
        return list(
            TaskLog.objects.filter(state=TaskLog.State.FAILURE)
            .values(name=F("task_name"))
            .annotate(y=Count("pk"))
            .annotate(
                url=Concat(
                    Value(f"{self.changelist_url()}?state__exact=3&task_name="),
                    F("name"),
                )
            )
            .order_by("-y")[:TASKMONITOR_REPORTS_MAX_TOP]
        )


class TasksTopRetried(_CachedReport):
    def _calc_data(self):
        total_retried = TaskLog.objects.filter(state=TaskLog.State.RETRY).count()
        if not total_retried:
            return None

        return list(
            TaskLog.objects.filter(state=TaskLog.State.RETRY)
            .values(name=F("task_name"))
            .annotate(y=Count("pk"))
            .annotate(
                url=Concat(
                    Value(f"{self.changelist_url()}?state__exact=2&task_name="),
                    F("name"),
                )
            )
            .order_by("-y")[:TASKMONITOR_REPORTS_MAX_TOP]
        )


class TasksThroughput(_CachedReport):
    def _calc_data(self):
        tasklogs_not_failed = TaskLog.objects.filter(state=TaskLog.State.SUCCESS)
        tasks_throughput = []
        average_last_hours = {}
        for hours in [1, 3, 6, 12, 24]:
            average_last_hours[hours] = tasklogs_not_failed.filter(
                timestamp__gt=self.now - dt.timedelta(hours=hours)
            ).avg_throughput()
        for hours, y in average_last_hours.items():
            tasks_throughput.append({"name": f"Average last {hours} hours", "y": y})
        average_overall = tasklogs_not_failed.avg_throughput()
        tasks_throughput.append({"name": "Average overall", "y": average_overall})
        peak_overall = tasklogs_not_failed.max_throughput()
        tasks_throughput.append({"name": "Peak overall", "y": peak_overall})
        return tasks_throughput


class TasksThroughputByState(_CachedReport):
    is_included = False

    def _calc_data(self):
        series = []
        for state in TaskLog.State:
            qs = (
                TaskLog.objects.filter(state=state)
                .order_by("timestamp")
                .annotate(x=TruncMinute("timestamp"))
                .values("x")
                .annotate(y=Count("id"))
            )
            my_data = self._truncate_minutes(sum, qs, 5)
            series.append({"name": state.label, "data": my_data})
        return series


class TasksThroughputByApp(_CachedReport):
    is_included = False

    def _calc_data(self):
        series = []
        app_names = (
            TaskLog.objects.filter(state=TaskLog.State.SUCCESS)
            .values_list("app_name", flat=True)
            .distinct()
            .order_by("app_name")
        )
        for app_name in app_names:
            qs = (
                TaskLog.objects.filter(state=TaskLog.State.SUCCESS, app_name=app_name)
                .order_by("timestamp")
                .annotate(x=TruncMinute("timestamp"))
                .values("x")
                .annotate(y=Count("id"))
            )
            my_data = self._truncate_minutes(sum, qs, 5)
            series.append({"name": app_name, "data": my_data})
        return series


class ExceptionsThroughput(_CachedReport):
    is_included = False

    def _calc_data(self):
        series = []
        exceptions = (
            TaskLog.objects.exclude(exception="")
            .exclude(exception="Retry")
            .values_list("exception", flat=True)
            .distinct()
            .order_by("exception")
        )
        for exception in exceptions:
            app_qs = TaskLog.objects.filter(exception=exception)
            qs = (
                app_qs.order_by("timestamp")
                .annotate(x=TruncMinute("timestamp"))
                .values("x")
                .annotate(y=Count("id"))
            )
            my_data = self._truncate_minutes(sum, qs, 5)
            series.append({"name": exception, "data": my_data})
        return series


class AppFailuresOverTime(_CachedReport):
    is_included = False

    def _calc_data(self):
        series = []
        app_names = (
            TaskLog.objects.filter(state=TaskLog.State.FAILURE)
            .values_list("app_name", flat=True)
            .distinct()
            .order_by("app_name")
        )
        for app_name in app_names:
            qs = (
                TaskLog.objects.filter(app_name=app_name, state=TaskLog.State.FAILURE)
                .order_by("timestamp")
                .annotate(x=TruncMinute("timestamp"))
                .values("x")
                .annotate(y=Count("id"))
            )
            my_data = self._truncate_minutes(sum, qs, 5)
            series.append({"name": app_name, "data": my_data})
        return series


def refresh_cache() -> None:
    """Refresh the cache."""
    for my_report in reports():
        my_report.refresh_cache()


def clear_cache() -> None:
    """Clear cache for all reports."""
    for my_report in reports():
        my_report.clear_cache()


def data() -> dict:
    """Calculate the report data."""
    return {
        my_report.name: report_data(my_report.name)
        for my_report in reports()
        if my_report.is_included
    }


def report_data(report_name: str, use_cache: bool = True):
    """Data of an cached report."""
    return report(report_name).data(use_cache)


def reports() -> List[_CachedReport]:
    """List of all cached reports."""
    return _reports.values()


def report(report_name: str) -> _CachedReport:
    """Access report by name."""
    return _reports[report_name]


# Instantiation of all cached reports
_reports = {obj.name: obj for obj in [cls() for cls in _CachedReport.report_classes()]}
