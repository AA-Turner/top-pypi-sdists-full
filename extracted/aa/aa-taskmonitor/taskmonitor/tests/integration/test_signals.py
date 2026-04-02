from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils import timezone

from taskmonitor.core import task_logs, task_records
from taskmonitor.models import TaskLog
from taskmonitor.tests.factories import SenderStub, TaskLogFactory


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestSignalHandlingEnd2End(TestCase):
    def setUp(self) -> None:
        cache.clear()

    def test_should_create_entry_for_succeeded_task(self):
        # given
        expected = TaskLogFactory.build(state=TaskLog.State.SUCCESS)
        task_records.set(expected.task_id, task_logs.TASK_RECEIVED, timezone.now())
        task_records.set(expected.task_id, task_logs.TASK_STARTED, timezone.now())
        sender = SenderStub.create_from_obj(expected)
        # when
        task_logs.task_success_handler_2(sender=sender, result=expected.result)
        # then
        self.assertTrue(
            TaskLog.objects.filter(
                task_id=expected.task_id, state=TaskLog.State.SUCCESS
            ).exists()
        )

    def test_should_create_entry_for_failed_task(self):
        # given
        expected = TaskLogFactory.build(
            state=TaskLog.State.FAILURE, exception="", traceback=""
        )
        task_records.set(expected.task_id, task_logs.TASK_RECEIVED, timezone.now())
        task_records.set(expected.task_id, task_logs.TASK_STARTED, timezone.now())
        sender = SenderStub.create_from_obj(expected)
        other_task = TaskLogFactory.build()
        sender.request.id = str(other_task.task_id)  # now different from expected
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

    def test_should_create_entry_for_retried_task(self):
        # given
        expected = TaskLogFactory.build(
            state=TaskLog.State.RETRY, exception="", traceback=""
        )
        task_records.set(expected.task_id, task_logs.TASK_RECEIVED, timezone.now())
        task_records.set(expected.task_id, task_logs.TASK_STARTED, timezone.now())
        sender = SenderStub.create_from_obj(expected)
        sender_no_request = SenderStub.create_from_obj(expected)
        sender_no_request.request = None
        # when
        task_logs.task_retry_handler_2(
            sender=sender_no_request, request=sender.request, reason=None
        )
        # then
        self.assertTrue(
            TaskLog.objects.filter(
                task_id=expected.task_id, state=TaskLog.State.RETRY
            ).exists()
        )

    def test_should_create_entry_for_internal_error_task(self):
        # given
        expected = TaskLogFactory.build(
            state=TaskLog.State.FAILURE, exception="", traceback=""
        )
        task_records.set(expected.task_id, task_logs.TASK_RECEIVED, timezone.now())
        task_records.set(expected.task_id, task_logs.TASK_STARTED, timezone.now())
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
