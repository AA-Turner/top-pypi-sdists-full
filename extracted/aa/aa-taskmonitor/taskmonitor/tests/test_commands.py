from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from taskmonitor.core.celery_queues import QueuedTaskShort
from taskmonitor.management.commands import taskmonitorctl
from taskmonitor.models import TaskLog

from .factories import QueuedTaskRawFactory, TaskLogFactory

MODULE_PATH = "taskmonitor.management.commands.taskmonitorctl"


class TestCommands(TestCase):
    def test_should_continue_when_user_accepts(self):
        # given
        out = StringIO()
        cmd = taskmonitorctl.Command(out, out)
        # when/then
        with patch(MODULE_PATH + ".my_input") as m:
            m.return_value = "y"
            cmd._user_confirmed("question")

    def test_should_stop_when_user_does_not_accept(self):
        # given
        out = StringIO()
        cmd = taskmonitorctl.Command(out, out)
        # when/then
        with self.assertRaises(SystemExit):
            with patch(MODULE_PATH + ".my_input") as m:
                m.return_value = "n"
                cmd._user_confirmed("question")

    def test_should_inspect_filled_logs(self):
        # given
        TaskLogFactory()
        out = StringIO()
        # when
        call_command("taskmonitorctl", "inspect", "logs", stdout=out)

    def test_should_inspect_empty_logs(self):
        # given
        out = StringIO()
        # when
        call_command("taskmonitorctl", "inspect", "logs", stdout=out)

    def test_should_inspect_empty_queue(self):
        # given
        out = StringIO()
        # when
        with patch(MODULE_PATH + ".celery_queues", spec=True) as m:
            m.queue_length.return_value = 0
            m._fetch_task_from_all_queues.return_value = []
            call_command("taskmonitorctl", "inspect", "queue", stdout=out)

    def test_should_inspect_filled_queue(self):
        # given
        out = StringIO()
        task = QueuedTaskShort.from_dict(QueuedTaskRawFactory())
        # when
        with patch(MODULE_PATH + ".celery_queues", spec=True) as m:
            m.queue_length.return_value = 1
            m._fetch_task_from_all_queues.return_value = [task]
            call_command("taskmonitorctl", "inspect", "queue", stdout=out)

    def test_should_inspect_settings(self):
        # given
        out = StringIO()
        # when
        call_command("taskmonitorctl", "inspect", "settings", stdout=out)

    @patch(MODULE_PATH + ".celery_queues", spec=True)
    def test_should_purge_empty_queue(self, mock_celery_queues):
        # given
        mock_celery_queues.queue_length.return_value = 0
        out = StringIO()
        # when
        with self.assertRaises(SystemExit):
            call_command("taskmonitorctl", "purge", "queue", "--all", stdout=out)
        # then
        self.assertFalse(mock_celery_queues.clear_tasks.called)

    @patch(MODULE_PATH + ".celery_queues", spec=True)
    def test_should_purge_filled_queue_all(self, mock_celery_queues):
        # given
        mock_celery_queues.queue_length.return_value = 1
        out = StringIO()
        # when
        with patch(MODULE_PATH + ".Command._user_confirmed", spec=True) as m:
            m.return_value = None
            call_command("taskmonitorctl", "purge", "queue", "--all", stdout=out)
        # then
        self.assertTrue(mock_celery_queues.clear_tasks.called)

    @patch(MODULE_PATH + ".celery_queues", spec=True)
    def test_should_purge_by_task_name(self, mock_celery_queues):
        # given
        mock_celery_queues.queue_length.return_value = 1
        mock_celery_queues.delete_task_by_name.return_value = 1
        out = StringIO()
        # when
        with patch(MODULE_PATH + ".Command._user_confirmed", spec=True) as m:
            m.return_value = None
            call_command(
                "taskmonitorctl", "purge", "queue", "--task-name", "alpha", stdout=out
            )
        # then
        self.assertTrue(mock_celery_queues.delete_task_by_name.called)

    @patch(MODULE_PATH + ".celery_queues", spec=True)
    def test_should_purge_by_task_id(self, mock_celery_queues):
        # given
        mock_celery_queues.queue_length.return_value = 1
        mock_celery_queues.delete_task_by_id.return_value = 1
        out = StringIO()
        # when
        with patch(MODULE_PATH + ".Command._user_confirmed", spec=True) as m:
            m.return_value = None
            call_command(
                "taskmonitorctl", "purge", "queue", "--task-id", "my-id", stdout=out
            )
        # then
        self.assertTrue(mock_celery_queues.delete_task_by_id.called)

    @patch(MODULE_PATH + ".celery_queues", spec=True)
    def test_should_purge_by_app_name(self, mock_celery_queues):
        # given
        mock_celery_queues.queue_length.return_value = 1
        mock_celery_queues.delete_task_by_app_name.return_value = 1
        out = StringIO()
        # when
        with patch(MODULE_PATH + ".Command._user_confirmed", spec=True) as m:
            m.return_value = None
            call_command(
                "taskmonitorctl", "purge", "queue", "--app-name", "alpha", stdout=out
            )
        # then
        self.assertTrue(mock_celery_queues.delete_task_by_app_name.called)

    @patch(MODULE_PATH + ".cached_reports", spec=True)
    def test_should_purge_logs_filled(self, mock_cached_reports):
        # given
        TaskLogFactory()
        out = StringIO()
        # when
        with patch(MODULE_PATH + ".Command._user_confirmed", spec=True) as m:
            m.return_value = None
            call_command("taskmonitorctl", "purge", "logs", "--all", stdout=out)
        # then
        self.assertEqual(TaskLog.objects.count(), 0)
        self.assertTrue(mock_cached_reports.refresh_cache.called)

    @patch(MODULE_PATH + ".cached_reports", spec=True)
    def test_should_purge_logs_empty(self, mock_cached_reports):
        # given
        out = StringIO()
        # when/then
        with self.assertRaises(SystemExit):
            with patch(MODULE_PATH + ".Command._user_confirmed", spec=True) as m:
                m.return_value = None
                call_command("taskmonitorctl", "purge", "logs", "--all", stdout=out)
