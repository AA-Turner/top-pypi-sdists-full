from unittest import mock

from django.test import TestCase

from taskmonitor.core import celery_queues
from taskmonitor.core.celery_queues import QueuedTaskShort, tasks_cache

from ..factories import QueuedTaskRawFactory

CELERY_QUEUE_NAME = "test_task_monitor_celery"
MODULE_PATH = "taskmonitor.core.celery_queues"


@mock.patch(MODULE_PATH + ".TASKMONITOR_QUEUED_TASKS_CACHE_TIMEOUT", 10)
@mock.patch(MODULE_PATH + ".default_queue_name")
class TestCeleryQueues(TestCase):
    def setUp(self):
        celery_queues.clear_tasks(CELERY_QUEUE_NAME)

    def tearDown(self):
        celery_queues.clear_tasks(CELERY_QUEUE_NAME)

    def test_should_return_queue_length(self, mock_queue_base_name):
        # given
        mock_queue_base_name.return_value = CELERY_QUEUE_NAME
        raw_tasks = [QueuedTaskRawFactory(), QueuedTaskRawFactory()]
        celery_queues.add_tasks(CELERY_QUEUE_NAME, raw_tasks)
        # when/then
        self.assertEqual(celery_queues.queue_length(), 2)

    def test_should_clear_queue(self, mock_queue_base_name):
        # given
        mock_queue_base_name.return_value = CELERY_QUEUE_NAME
        raw_tasks = [QueuedTaskRawFactory(), QueuedTaskRawFactory()]
        celery_queues.add_tasks(CELERY_QUEUE_NAME, raw_tasks)
        # when
        celery_queues.clear_tasks()
        # then
        self.assertEqual(celery_queues.queue_length(), 0)

    def test_should_fetch_tasks_in_correct_order(self, mock_queue_base_name):
        # given
        mock_queue_base_name.return_value = CELERY_QUEUE_NAME
        raw_task_1 = QueuedTaskRawFactory(properties__priority=4)
        raw_task_2 = QueuedTaskRawFactory(properties__priority=4)
        raw_task_3 = QueuedTaskRawFactory(properties__priority=3)
        celery_queues.add_tasks(CELERY_QUEUE_NAME, [raw_task_1, raw_task_2, raw_task_3])
        # when
        with mock.patch(MODULE_PATH + ".tasks_cache") as m:
            m.get.return_value = None
            result = celery_queues.fetch_tasks()
        # then
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], QueuedTaskShort.from_dict(raw_task_3))
        self.assertEqual(result[1], QueuedTaskShort.from_dict(raw_task_1))
        self.assertEqual(result[2], QueuedTaskShort.from_dict(raw_task_2))

    def test_should_retrieve_tasks_from_cache(self, mock_queue_base_name):
        # given
        tasks = [QueuedTaskShort.from_dict(QueuedTaskRawFactory())]
        tasks_cache.set(tasks)
        # when
        result = celery_queues.fetch_tasks()
        # then
        self.assertEqual(result, tasks)

    def test_should_retrieve_tasks_from_redis_when_no_cache(self, mock_queue_base_name):
        # given
        mock_queue_base_name.return_value = CELERY_QUEUE_NAME
        tasks = [QueuedTaskRawFactory()]
        celery_queues.add_tasks(CELERY_QUEUE_NAME, tasks)
        # when
        result = celery_queues.fetch_tasks()
        # then
        self.assertEqual(result[0], QueuedTaskShort.from_dict(tasks[0]))

    def test_should_delete_task_by_id(self, mock_queue_base_name):
        # given
        mock_queue_base_name.return_value = CELERY_QUEUE_NAME
        task_1 = QueuedTaskRawFactory()
        task_2 = QueuedTaskRawFactory()
        celery_queues.add_tasks(CELERY_QUEUE_NAME, [task_1, task_2])
        task_1_dto = QueuedTaskShort.from_dict(task_1)
        task_2_dto = QueuedTaskShort.from_dict(task_2)
        # when
        result = celery_queues.delete_task_by_id(task_1_dto.id)
        # then
        self.assertEqual(result, 1)
        tasks = celery_queues.fetch_tasks()
        self.assertNotIn(task_1_dto, tasks)
        self.assertIn(task_2_dto, tasks)

    def test_should_delete_task_by_name(self, mock_queue_base_name):
        # given
        mock_queue_base_name.return_value = CELERY_QUEUE_NAME
        task_1 = QueuedTaskRawFactory(headers__task="alpha.tasks.blue")
        task_2 = QueuedTaskRawFactory(headers__task="alpha.tasks.yellow")
        celery_queues.add_tasks(CELERY_QUEUE_NAME, [task_1, task_2])
        task_1_dto = QueuedTaskShort.from_dict(task_1)
        task_2_dto = QueuedTaskShort.from_dict(task_2)
        # when
        result = celery_queues.delete_task_by_name(task_1_dto.name)
        # then
        self.assertEqual(result, 1)
        tasks = celery_queues.fetch_tasks()
        self.assertNotIn(task_1_dto, tasks)
        self.assertIn(task_2_dto, tasks)

    def test_should_delete_task_by_app_name(self, mock_queue_base_name):
        # given
        mock_queue_base_name.return_value = CELERY_QUEUE_NAME
        task_1 = QueuedTaskRawFactory(headers__task="alpha.tasks.blue")
        task_2 = QueuedTaskRawFactory(headers__task="bravo.tasks.yellow")
        celery_queues.add_tasks(CELERY_QUEUE_NAME, [task_1, task_2])
        task_1_dto = QueuedTaskShort.from_dict(task_1)
        task_2_dto = QueuedTaskShort.from_dict(task_2)
        # when
        result = celery_queues.delete_task_by_app_name(task_1_dto.app_name)
        # then
        self.assertEqual(result, 1)
        tasks = celery_queues.fetch_tasks()
        self.assertNotIn(task_1_dto, tasks)
        self.assertIn(task_2_dto, tasks)
