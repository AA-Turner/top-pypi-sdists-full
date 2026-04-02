from celery.app import default_app

from django.core.cache import cache
from django.test import TransactionTestCase, override_settings

from taskmonitor.models import TaskLog

TASK_LOGS_PATH = "taskmonitor.core.task_logs"


@default_app.task
def normal_task():
    pass


@default_app.task
def special_task():
    """Task returns an object, which is not JSON serializable."""
    return Dummy()


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestTaskLogCreation(TransactionTestCase):
    def setUp(self) -> None:
        cache.clear()

    def test_should_create_entry_for_normal_task(self):
        # when
        normal_task.delay()
        # then
        self.assertTrue(
            TaskLog.objects.filter(
                task_name="taskmonitor.tests.integration.test_tasklogs.normal_task",
                state=TaskLog.State.SUCCESS,
            ).exists()
        )

    def test_should_create_entry_for_task_which_result_can_not_be_serialized(self):
        # when
        special_task.delay()
        # then
        self.assertTrue(
            TaskLog.objects.filter(
                task_name="taskmonitor.tests.integration.test_tasklogs.special_task",
                state=TaskLog.State.SUCCESS,
            ).exists()
        )


class Dummy:
    pass
