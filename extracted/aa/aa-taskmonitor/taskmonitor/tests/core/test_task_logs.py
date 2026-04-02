from unittest.mock import patch

from django.utils.timezone import now

from app_utils.testing import NoSocketsTestCase

from taskmonitor.core import task_logs
from taskmonitor.models import TaskLog

from ..factories import SenderStub, TaskLogFactory

MODULE_PATH = "taskmonitor.core.task_logs"


class TestRunWhenEnabledDecorator(NoSocketsTestCase):
    @patch(MODULE_PATH + ".TASKMONITOR_ENABLED", True)
    def test_should_pass_when_enabled(self):
        # given
        @task_logs.run_when_enabled
        def dummy(x, y, z):
            nonlocal my_var
            my_var = 1

        my_var = 0

        # when
        dummy(1, 2, 3)
        # then
        self.assertEqual(my_var, 1)

    @patch(MODULE_PATH + ".TASKMONITOR_ENABLED", False)
    def test_should_not_pass_when_disabled(self):
        # given
        @task_logs.run_when_enabled
        def dummy(x, y, z):
            nonlocal my_var
            my_var = 1

        my_var = 0

        # when
        dummy(1, 2, 3)
        # then
        self.assertEqual(my_var, 0)


@patch(MODULE_PATH + ".celery_queues.queue_length_cached", lambda: 0)
@patch(MODULE_PATH + ".task_records.fetch", spec=True)
@patch(MODULE_PATH + "._run_housekeeping_if_stale", spec=True)
class TestTaskFailureHandler(NoSocketsTestCase):
    def test_should_create_log_for_complete_task(
        self, mock_run_housekeeping_if_stale, mock_task_records_fetch
    ):
        # given
        mock_task_records_fetch.return_value = now()
        expected = TaskLogFactory.build(
            state=TaskLog.State.FAILURE, exception="", traceback=""
        )
        sender = SenderStub.create_from_obj(expected)
        # when
        task_logs.task_failure_handler_2(
            sender=sender, task_id=str(expected.task_id), exception=None
        )
        # then
        self.assertTrue(
            TaskLog.objects.filter(
                task_id=expected.task_id, state=TaskLog.State.FAILURE
            ).exists()
        )
        self.assertTrue(mock_run_housekeeping_if_stale.called)

    def test_should_create_log_for_task_without_delivery_info(
        self, mock_run_housekeeping_if_stale, mock_task_records_fetch
    ):
        # given
        mock_task_records_fetch.return_value = now()
        expected = TaskLogFactory.build(
            state=TaskLog.State.FAILURE, exception="", traceback=""
        )
        sender = SenderStub.create_from_obj(expected)
        sender.request.delivery_info = None
        # when
        task_logs.task_failure_handler_2(
            sender=sender, task_id=str(expected.task_id), exception=None
        )
        # then
        self.assertTrue(
            TaskLog.objects.filter(
                task_id=expected.task_id, state=TaskLog.State.FAILURE
            ).exists()
        )
        self.assertTrue(mock_run_housekeeping_if_stale.called)


@patch(MODULE_PATH + ".celery_queues.queue_length_cached", lambda: 0)
@patch(MODULE_PATH + ".task_records.fetch", spec=True)
@patch(MODULE_PATH + "._run_housekeeping_if_stale", spec=True)
class TestTaskInternalErrorHandler(NoSocketsTestCase):
    def test_should_create_log_for_complete_task(
        self, mock_run_housekeeping_if_stale, mock_task_records_fetch
    ):
        # given
        mock_task_records_fetch.return_value = now()
        expected = TaskLogFactory.build(
            state=TaskLog.State.FAILURE, exception="", traceback=""
        )
        sender = SenderStub.create_from_obj(expected)
        # when
        task_logs.task_internal_error_handler_2(
            sender=sender,
            task_id=str(expected.task_id),
            request=sender.request.asdict(),
            exception=None,
        )
        # then
        self.assertTrue(
            TaskLog.objects.filter(
                task_id=expected.task_id, state=TaskLog.State.FAILURE
            ).exists()
        )
        self.assertTrue(mock_run_housekeeping_if_stale.called)

    def test_should_create_log_for_task_without_delivery_info_1(
        self, mock_run_housekeeping_if_stale, mock_task_records_fetch
    ):
        # given
        mock_task_records_fetch.return_value = now()
        expected = TaskLogFactory.build(
            state=TaskLog.State.FAILURE, exception="", traceback=""
        )
        sender = SenderStub.create_from_obj(expected)
        sender.request.delivery_info = None
        # when
        task_logs.task_internal_error_handler_2(
            sender=sender,
            task_id=str(expected.task_id),
            request=sender.request.asdict(),
            exception=None,
        )
        # then
        self.assertTrue(
            TaskLog.objects.filter(
                task_id=expected.task_id, state=TaskLog.State.FAILURE
            ).exists()
        )
        self.assertTrue(mock_run_housekeeping_if_stale.called)

    def test_should_create_log_for_task_without_delivery_info_2(
        self, mock_run_housekeeping_if_stale, mock_task_records_fetch
    ):
        # given
        mock_task_records_fetch.return_value = now()
        expected = TaskLogFactory.build(
            state=TaskLog.State.FAILURE, exception="", traceback=""
        )
        sender = SenderStub.create_from_obj(expected)
        request = sender.request.asdict()
        del request["delivery_info"]
        # when
        task_logs.task_internal_error_handler_2(
            sender=sender,
            task_id=str(expected.task_id),
            request=request,
            exception=None,
        )
        # then
        self.assertTrue(
            TaskLog.objects.filter(
                task_id=expected.task_id, state=TaskLog.State.FAILURE
            ).exists()
        )
        self.assertTrue(mock_run_housekeeping_if_stale.called)
