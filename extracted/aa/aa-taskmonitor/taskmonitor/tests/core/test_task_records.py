from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone

from taskmonitor.core import task_records


class TestTaskRecords(TestCase):
    def setUp(self) -> None:
        cache.clear()

    def test_should_store_and_retrieve_data(self):
        # given
        value = timezone.now()
        # when
        task_records.set("abc", "alpha", value)
        result = task_records.get("abc", "alpha")
        # then
        self.assertEqual(result, value)

    def test_should_delete_data(self):
        # given
        value = timezone.now()
        # when
        task_records.set("abc", "alpha", value)
        result = task_records.fetch("abc", "alpha")
        # then
        self.assertEqual(result, value)
        self.assertIsNone(task_records.get("abc", "alpha"))
