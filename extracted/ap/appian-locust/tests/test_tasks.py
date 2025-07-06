import os
import unittest
import json

from appian_locust._interactor import _Interactor
from appian_locust._tasks import _Tasks
from locust import Locust, TaskSet

from tests.mock_client import CustomLocust
from tests.mock_reader import read_mock_file


class TestTask(unittest.TestCase):

    task_feed_resp = read_mock_file("tasks_response.json")
    task_feed_with_next = read_mock_file("tasks_response_with_next.json")

    def get_task_attributes(self, is_auto_acceptable: bool) -> str:
        return f"""
        {{
            "isOfflineTask": false,
            "isSailTask": true,
            "isQuickTask": false,
            "taskId": "1",
            "isAutoAcceptable": {'true' if is_auto_acceptable else 'false'}
        }}"""

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        setattr(self.custom_locust.client, "feature_flag", "")
        setattr(self.custom_locust.client, "feature_flag_extended", "")
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.interactor: _Interactor = _Interactor(self.custom_locust.client, "")
        self.interactor.login(["", ""])
        self.task_interactor: _Tasks = _Tasks(self.interactor)
        self.custom_locust.set_default_response(200, "{}")
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/attributes",
            200,
            self.get_task_attributes(is_auto_acceptable=True))
        self.custom_locust.set_response(_Tasks.INITIAL_FEED_URI, 200, self.task_feed_resp)

    def test_task_get_all(self) -> None:
        self.custom_locust.enqueue_response(200, self.task_feed_with_next)
        self.custom_locust.enqueue_response(200, self.task_feed_resp)
        all_task = self.task_interactor.get_all()

        self.assertEqual(len(all_task.keys()), 21)
        # TODO: These keys are bad, as are the record/ report keys, consider just using the names/ IDs
        self.assertEqual(all_task['t-2109072_34 Task_Assign SR#0G56-W7N3 to Case Worker']['id'], 't-2109072')

    def test_task_get_task_pages_all(self) -> None:
        self.custom_locust.enqueue_response(200, self.task_feed_with_next)
        self.custom_locust.enqueue_response(200, self.task_feed_resp)
        all_task = self.task_interactor.get_task_pages()

        self.assertEqual(len(all_task.keys()), 21)
        # TODO: These keys are bad, as are the record/ report keys, consider just using the names/ IDs
        self.assertEqual(all_task['t-2109072_34 Task_Assign SR#0G56-W7N3 to Case Worker']['id'], 't-2109072')

    def test_task_get_task_pages_twice(self) -> None:
        # TODO: This doesn't really test the paging algorithm.
        self.custom_locust.enqueue_response(200, self.task_feed_with_next)
        self.custom_locust.enqueue_response(200, self.task_feed_resp)
        all_task_1 = self.task_interactor.get_task_pages(pages_requested=1)

        self.custom_locust.enqueue_response(200, self.task_feed_with_next)
        self.custom_locust.enqueue_response(200, self.task_feed_resp)
        all_task_2 = self.task_interactor.get_task_pages(
            next_uri=self.task_interactor.get_next_task_page_uri(), pages_requested=1)

        all_task = {**all_task_1, **all_task_2}
        self.assertEqual(len(all_task.keys()), 21)  # There should still be 21 since we used the same input twice.

        # TODO: These keys are bad, as are the record/ report keys, consider just using the names/ IDs
        self.assertEqual(all_task['t-2109072_34 Task_Assign SR#0G56-W7N3 to Case Worker']['id'], 't-2109072')

    def test_task_get(self) -> None:
        task = self.task_interactor.get_task(
            "t-1", False)
        self.assertIsInstance(task, dict)

    def test_task_get_missing_task(self) -> None:
        with self.assertRaisesRegex(Exception, "There is no task with name .* in the system under test.*"):
            self.task_interactor.get_task("some random word")

    def test_get_task_form_json(self) -> None:
        output = self.task_interactor.get_task_form_json(task_name="t-1", exact_match=False)
        self.assertEqual(output, {})


if __name__ == '__main__':
    unittest.main()
