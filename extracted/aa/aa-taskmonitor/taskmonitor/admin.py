"""Admin site for Task Monitor."""

# pylint: disable = missing-class-docstring, missing-function-docstring

import datetime as dt
import json
from typing import Optional
from urllib.parse import urlencode

from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import html, safestring, timezone
from django.utils.translation import gettext_lazy as _

from app_utils.admin import FieldFilterCountsDb, FieldFilterCountsMemory

from .app_settings import (
    TASKMONITOR_DATA_MAX_AGE,
    TASKMONITOR_QUEUED_TASKS_ADMIN_LIMIT,
    TASKMONITOR_QUEUED_TASKS_CACHE_TIMEOUT,
)
from .core import cached_reports, celery_queues
from .models import QueuedTask, TaskLog, TaskReport, TaskStatistic


class QueuedTaskAppsListFilter(FieldFilterCountsMemory):
    """Filter by app name and show name with counts."""

    title = _("app name")
    parameter_name = "app_name"
    field_name = "app_name"


class QueuedTaskTasksListFilter(FieldFilterCountsMemory):
    """Filter by task name and show name with counts."""

    title = _("task name")
    parameter_name = "task_name"
    field_name = "name"


@admin.register(QueuedTask)
class QueuedTaskAdmin(admin.ModelAdmin):
    list_display = (
        "position",
        "id",
        "name",
        "priority",
        "app_name",
    )
    list_display_links = None
    list_filter = (QueuedTaskAppsListFilter, "priority", QueuedTaskTasksListFilter)
    ordering = ["position"]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        cache_created_at = celery_queues.tasks_cache.created_at() or timezone.now()
        objs_count = celery_queues.queue_length()
        context = {
            "title": "Currently queued tasks",
            "cache_created_at": cache_created_at,
            "task_count": objs_count,
            "cache_timeout": TASKMONITOR_QUEUED_TASKS_CACHE_TIMEOUT,
            "is_below_limit": objs_count < TASKMONITOR_QUEUED_TASKS_ADMIN_LIMIT,
        }
        extra_context.update(context)
        return super().changelist_view(request, extra_context)


@admin.register(TaskReport)
class TaskReportAdmin(admin.ModelAdmin):
    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def changelist_view(self, request, extra_context=None):
        return redirect("taskmonitor:admin_taskmonitor_reports")


class TaskLogAppsListFilter(FieldFilterCountsDb):
    """Filter by app name and show name with counts."""

    title = _("app name")
    parameter_name = "app"
    field_name = "app_name"


class TaskLogStatesListFilter(FieldFilterCountsDb):
    """Filter by app name and show name with counts."""

    title = _("state")
    parameter_name = "state"
    field_name = "state"


class TaskLogExceptionsListFilter(FieldFilterCountsDb):
    """Filter by exception name and show name with counts."""

    title = _("exception")
    parameter_name = "exception"
    field_name = "exception"


@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = (
        "_timestamp",
        "task_name",
        "_params",
        "priority",
        "_state",
        "_runtime",
        "_exception",
    )
    list_filter = (
        TaskLogStatesListFilter,
        TaskLogExceptionsListFilter,
        "timestamp",
        TaskLogAppsListFilter,
        "priority",
    )
    search_fields = ("task_name", "app_name", "task_id")
    actions = ["delete_selected_2"]
    show_full_result_count = False
    fields = (
        "task_id",
        "task_name",
        "timestamp",
        "_args",
        "_kwargs",
        "_result",
        "retries",
        "priority",
        "state",
        "runtime",
        "app_name",
        "_exception",
        "parent_id",
        "received",
        "started",
        "_traceback",
    )

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_readonly_fields(self, request, obj=None):
        try:
            field = [f for f in TaskLog._meta.fields if f.name == "kwargs"]
            if len(field) > 0:
                field = field[0]
                field.help_text = "some special help text"
        except Exception:  # pylint: disable = broad-exception-caught
            pass
        return self.readonly_fields

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(_task_log_stats())
        return super().changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        obj = get_object_or_404(TaskLog, pk=object_id)
        extra_context["tasklog_text"] = obj.astext()
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    @admin.display
    def _params(self, obj):
        if obj.args and not obj.kwargs:
            return html.format_html("<code>{}</code>", json.dumps(obj.args))
        if not obj.args and obj.kwargs:
            return html.format_html(
                "<code>{}</code>", json.dumps(obj.kwargs, sort_keys=True)
            )
        if obj.args and obj.kwargs:
            return html.format_html(
                "<code>{}<br>{}</code>",
                json.dumps(obj.args),
                json.dumps(obj.kwargs, sort_keys=True),
            )
        return None

    @admin.display(description="Exception")
    def _exception(self, obj) -> str:
        return html.format_html("<code>{}</code>", obj.exception)

    @admin.display(ordering="runtime")
    def _runtime(self, obj) -> Optional[str]:
        return f"{obj.runtime:.1f}" if obj.runtime else None

    @admin.display(ordering="state")
    def _state(self, obj: TaskLog) -> str:
        css_class_map = {
            TaskLog.State.RETRY: "state-retry",
            TaskLog.State.FAILURE: "text-danger",
        }
        css_class = css_class_map.get(obj.state, "")
        return html.format_html(
            '<span class="{}">{}</span>', css_class, obj.get_state_display()
        )

    @admin.display(ordering="timestamp")
    def _timestamp(self, obj: TaskLog) -> str:
        return obj.timestamp_formatted

    @admin.action(description="Delete selected entries (NO CONFIRMATION!")
    def delete_selected_2(self, request, queryset):
        entries_count = queryset.count()
        queryset._raw_delete(queryset.db)  # pylint: disable = protected-access
        self.message_user(request, f"Deleted {entries_count} entries.")

    @admin.display(description="Result")
    def _result(self, obj):
        if obj.state == TaskLog.State.SUCCESS:
            return _format_html_data(obj.result)
        return "-"

    @admin.display(description="Args")
    def _args(self, obj):
        return _format_html_data(obj.args)

    @admin.display(description="Kwargs")
    def _kwargs(self, obj):
        return _format_html_data(obj.kwargs)

    @admin.display(description="Traceback")
    def _traceback(self, obj):
        return _format_html_lines(obj.traceback)


@admin.register(TaskStatistic)
class TaskStatisticAdmin(admin.ModelAdmin):
    list_display = [
        "_name",
        "_runs_total",
        "_runs_succeeded",
        "_runs_failed",
        "_runs_retried",
        "_runtime_min",
        "_runtime_avg",
        "_runtime_max",
        "_runtime_total",
    ]
    list_display_links = None
    list_filter = ["app"]
    ordering = ["name"]
    search_fields = ["name"]

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False

        qs = queryset.filter(name__icontains=search_term)
        return qs, False

    def changelist_view(self, request, extra_context=None):
        context = {"title": "Task Statistics"}
        last_update_at = TaskStatistic.objects.cached_at()
        context.update(_task_log_stats(last_update_at))
        extra_context = extra_context or {}
        extra_context.update(context)
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    @admin.display(ordering="name", description="name")
    def _name(self, obj: TaskStatistic):
        base_url = reverse("admin:taskmonitor_tasklog_changelist")
        query_encoded = urlencode({"task_name": obj.name})
        url = f"{base_url}?{query_encoded}"
        return html.format_html('<a href="{}">{}</a>', url, obj.name)

    @admin.display(ordering="runs_total", description="runs")
    def _runs_total(self, obj: TaskStatistic):
        return f"{obj.runs_total:,}"

    @admin.display(ordering="runs_succeeded", description="succeeded")
    def _runs_succeeded(self, obj: TaskStatistic):
        return f"{obj.runs_succeeded:,}"

    @admin.display(ordering="runs_failed", description="failed")
    def _runs_failed(self, obj: TaskStatistic):
        return f"{obj.runs_failed:,}"

    @admin.display(ordering="runs_retried", description="retried")
    def _runs_retried(self, obj: TaskStatistic):
        return f"{obj.runs_retried:,}"

    @admin.display(ordering="runtime_min")
    def _runtime_min(self, obj: TaskStatistic):
        return self._format_float(obj.runtime_min)

    @admin.display(ordering="runtime_avg")
    def _runtime_avg(self, obj: TaskStatistic):
        return self._format_float(obj.runtime_avg)

    @admin.display(ordering="runtime_max")
    def _runtime_max(self, obj: TaskStatistic):
        return self._format_float(obj.runtime_max)

    @admin.display(ordering="runtime_total")
    def _runtime_total(self, obj: TaskStatistic):
        return self._format_float(obj.runtime_total)

    @staticmethod
    def _format_float(value) -> str:
        return f"{value:,.2f}"


def _task_log_stats(last_update_at: Optional[dt.datetime] = None) -> dict:
    """Return dict with task log stats."""
    report = cached_reports.report("tasks_basics")
    report_data = report.data()
    total_runs = report_data["total_runs"]
    oldest_date = report_data["oldest_date"]
    newest_date = report_data["newest_date"]
    context = {
        "total_runs": total_runs,
        "oldest_date": oldest_date,
        "newest_date": newest_date,
        "data_max_age": TASKMONITOR_DATA_MAX_AGE,
        "last_update_at": last_update_at,
    }
    return context


def _format_html_lines(text) -> str:
    return safestring.mark_safe(
        "<br>".join(
            [html.format_html("<code>{}</code>", line) for line in text.splitlines()]
        )
    )


def _format_html_data(data) -> str:
    return html.format_html(
        "<code>{}</code>", json.dumps(data, sort_keys=True, indent=4)
    )
