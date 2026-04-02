import json

from django.core.cache import cache
from django.test import TestCase

from taskmonitor.core.tasks_cache import QueuedTasksCache, QueuedTaskShort

from ..factories import QueuedTaskRawFactory


class TestQueuedTaskShort(TestCase):
    def test_should_create_from_dict(self):
        # given
        task = QueuedTaskRawFactory()
        # when
        obj = QueuedTaskShort.from_dict(task)
        # then
        self.assertEqual(obj.id, task["headers"]["id"])
        self.assertEqual(obj.name, task["headers"]["task"])
        self.assertEqual(obj.priority, task["properties"]["priority"])

    def test_should_create_from_redis_entry(self):
        # given
        task = QueuedTaskRawFactory()
        obj_json = json.dumps(task)
        obj_encoded = obj_json.encode("utf-8")
        # when
        obj = QueuedTaskShort.from_binary_json(obj_encoded)
        # then
        self.assertEqual(obj.id, task["headers"]["id"])
        self.assertEqual(obj.name, task["headers"]["task"])
        self.assertEqual(obj.priority, task["properties"]["priority"])


class TestCacheAPi(TestCase):
    CACHE_KEY = "test-cache-api-cache-key"

    def setUp(self) -> None:
        cache.delete(self.CACHE_KEY)

    def test_should_store_and_fetch_from_cache(self):
        # given
        tasks_cache = QueuedTasksCache(self.CACHE_KEY, 60)
        tasks = [QueuedTaskShort.from_dict(QueuedTaskRawFactory())]
        # when
        tasks_cache.set(tasks)
        result = tasks_cache.get()
        # then
        self.assertEqual(result.tasks, tasks)

    def test_should_raise_error_when_cache_returned_wrong_datatype(self):
        # given
        tasks_cache = QueuedTasksCache(self.CACHE_KEY)
        cache.set(key=self.CACHE_KEY, value="abc")
        # when/then
        with self.assertRaises(TypeError):
            tasks_cache.get()

    def test_should_clear_cache(self):
        # given
        tasks_cache = QueuedTasksCache(self.CACHE_KEY)
        tasks = [QueuedTaskShort.from_dict(QueuedTaskRawFactory())]
        tasks_cache.set(tasks)
        # when
        tasks_cache.clear()
        # then
        self.assertIsNone(tasks_cache.get())

    def test_should_return_created_at(self):
        # given
        tasks_cache = QueuedTasksCache(self.CACHE_KEY, 60)
        tasks = [QueuedTaskShort.from_dict(QueuedTaskRawFactory())]
        tasks_cache.set(tasks)
        data = tasks_cache.get()
        # when
        result = tasks_cache.created_at()
        # then
        self.assertEqual(result, data.created_at)

    def test_should_return_none_for_created_at_when_cache_invalid(self):
        # given
        tasks_cache = QueuedTasksCache(self.CACHE_KEY, 60)
        # when
        result = tasks_cache.created_at()
        # then
        self.assertIsNone(result)

    def test_should_disable_cache(self):
        # given
        tasks_cache = QueuedTasksCache(self.CACHE_KEY, 0)
        tasks = [QueuedTaskShort.from_dict(QueuedTaskRawFactory())]
        tasks_cache.set(tasks)
        # when
        result = tasks_cache.get()
        # then
        self.assertIsNone(result)
