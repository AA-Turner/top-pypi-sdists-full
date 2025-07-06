from locust import TaskSet, Locust
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet
from appian_locust._interactor import _Interactor
from appian_locust._news import _News

import unittest

NEWS_URI = "/suite/api/feed/tempo?t=e,x,b&m=menu-news&st=o"


class TestNews(unittest.TestCase):

    news = read_mock_file("news_response.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(self.custom_locust.client, "feature_flag", "")
        setattr(self.custom_locust.client, "feature_flag_extended", "")
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.interactor = _Interactor(self.custom_locust.client, "")
        self.interactor.login(["", ""])
        self.news_interactor = _News(self.interactor)
        self.task_set.on_start()

        self.custom_locust.set_response(NEWS_URI, 200, self.news)

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_news_get_all(self) -> None:
        all_news = self.news_interactor.get_all()
        self.assertIsInstance(all_news, dict)

    def test_news_search(self) -> None:
        self.custom_locust.set_response("/suite/api/feed/tempo?q=appian", 200, self.news)
        all_news = self.news_interactor.search("appian")
        self.assertIsInstance(all_news, dict)

    def test_news_get(self) -> None:
        news = self.news_interactor.get_news(
            "x-1")
        self.assertIsInstance(news, dict)

    def test_news_get_corrupt_news_post(self) -> None:
        corrupt_news = self.news.replace('"id": "x-3"', '"corrupt_id": "x-3"')
        self.custom_locust.set_response(NEWS_URI, 200, corrupt_news)
        all_news = self.news_interactor.get_all()
        self.assertTrue("ERROR::1" in str(all_news))
        self.assertTrue(self.news_interactor._errors == 1)

    def test_actions_get_retry(self) -> None:
        self.news_interactor._news = dict()  # Resetting the cache.
        self.custom_locust.set_response("/suite/api/feed/tempo?q=Admin", 200, self.news)
        action = self.news_interactor.get_news(
            "x-1", True, "Admin")
        self.assertIsInstance(action, dict)

    def test_news_get_missing_news(self) -> None:
        with self.assertRaisesRegex(Exception, "There is no news with name .* in the system under test.*"):
            self.news_interactor.get_news("some random word")

    def test_news_visit(self) -> None:
        self.news_interactor.visit("x-1", False)

    def test_news_visit_entry(self) -> None:
        self.custom_locust.set_response("/suite/api/feed/tempo?q=appian", 200, self.news)
        self.assertEqual((200, 200), self.news_interactor.visit_news_entry("x-1", False))

    def test_news_visit_entry_no_share_link(self) -> None:
        self.custom_locust.set_response("/suite/api/feed/tempo?q=appian", 200, self.news)
        self.assertEqual(self.news_interactor.visit_news_entry("x-2", False), (None, 200))

    def test_news_visit_entry_no_edit_link(self) -> None:
        self.custom_locust.set_response("/suite/api/feed/tempo?q=appian", 200, self.news)
        self.assertEqual(self.news_interactor.visit_news_entry("x-3", False), (200, None))

    def test_news_get_all_logic(self) -> None:
        test_cases = [
            {
                "input": '{"feed":{"entries":[{"title": "valid_test", "id": "123"}]}}',
                "expected": {'123::valid_test': {'title': 'valid_test', 'id': '123'}}
            },
            {
                "input": '{"feed":{"not_entries":[{"title": "valid_test", "id": "123"}]}}',
                "expected": {}
            },
            {
                "input": '{"not_feed":{"entries":[{"title": "valid_test", "id": "123"}]}}',
                "expected": {}
            },
            {
                "input": '{"feed":{"entries":[{"not_title": "valid_test", "id": "123"}]}}',
                "expected": {}
            }
        ]
        for test_case in test_cases:
            # Given
            self.custom_locust.set_response(NEWS_URI,
                                            200,
                                            str(test_case['input']))
            # When
            response = self.news_interactor.get_all()
            # Then
            self.assertEqual(response, test_case['expected'])


if __name__ == '__main__':
    unittest.main()
