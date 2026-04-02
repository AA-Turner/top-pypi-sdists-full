from unittest.mock import patch

import pytz

from django.core.cache import cache
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.timezone import now

from app_utils.testdata_factories import UserFactory

from taskmonitor import views
from taskmonitor.models import TaskLog

from .factories import TaskLogFactory

MODULE_PATH = "taskmonitor.views"


def _format_dt(my_dt) -> str:
    """Format datetime into a format with a special timezone offset,
    which strtime() does not support.
    """
    offset = pytz.utc.utcoffset(my_dt).total_seconds()
    sign = "+" if offset >= 0 else "-"
    hours = int(offset / 3600)
    minutes = int(offset / 60)
    offset_str = f"{sign}{hours:02}:{minutes:02}"
    return my_dt.strftime("%Y-%m-%d %H:%M:%S.%f") + offset_str


def _streaming_content_to_string(response):
    bytes = b"".join(response.streaming_content)
    return bytes.decode("utf-8")


class TestCsvViews(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()

    def test_should_export_data_to_csv(self):
        # given
        user = UserFactory(is_staff=True)
        request = self.request_factory.get(
            reverse("taskmonitor:admin_taskmonitor_download_csv")
        )
        request.user = user
        self.maxDiff = None
        # when
        TaskLogFactory(state=TaskLog.State.SUCCESS)
        TaskLogFactory(state=TaskLog.State.RETRY)
        TaskLogFactory(state=TaskLog.State.FAILURE)
        for _ in range(50):
            TaskLogFactory()
        response = views.admin_taskmonitor_download_csv(request)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/csv")
        content = _streaming_content_to_string(response)
        lines = content.splitlines()
        lines.reverse()
        self.assertEqual(
            lines.pop(),
            "id;app_name;exception;parent_id;priority;retries;received;runtime;started;state;"
            "task_id;task_name;timestamp",
        )
        for entry in TaskLog.objects.order_by("pk"):
            values = lines.pop().split(";")
            self.assertEqual(len(values), 13)
            self.assertEqual(values[0], str(entry.pk))
            self.assertEqual(values[1], entry.app_name)
            self.assertEqual(values[2], "" if not entry.exception else entry.exception)
            self.assertEqual(values[3], "" if not entry.parent_id else entry.parent_id)
            self.assertEqual(values[4], str(entry.priority))
            self.assertEqual(values[5], str(entry.retries))
            self.assertEqual(values[6], _format_dt(entry.received))
            self.assertEqual(values[7], str(entry.runtime))
            self.assertEqual(values[8], _format_dt(entry.started))
            self.assertEqual(values[9], entry.get_state_display())
            self.assertEqual(values[10], str(entry.task_id))
            self.assertEqual(values[11], entry.task_name)
            self.assertEqual(values[12], _format_dt(entry.timestamp))


@patch(MODULE_PATH + ".cached_reports.report", spec=True)
class TestAdminUi(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()
        cache.clear()

    def test_should_open_reports_view(self, mock_report):
        # given
        mock_report.return_value.data.return_value = {
            "total_runs": 1,
            "total_runtime": 1,
            "oldest_date": now(),
            "newest_date": now(),
        }
        TaskLogFactory()
        user = UserFactory(is_staff=True)
        request = self.request_factory.get(
            reverse("taskmonitor:admin_taskmonitor_reports")
        )
        request.user = user
        # when
        response = views.admin_taskmonitor_reports(request)
        # then
        self.assertEqual(response.status_code, 200)
