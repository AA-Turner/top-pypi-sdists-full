from unittest import TestCase

import requests
import responses
import responses.registries
from requests import HTTPError, Timeout

from pycarlo.common.retries import Backoff, retry_with_backoff


class MockBackoff(Backoff):
    def __init__(self, count: int):
        super(MockBackoff, self).__init__(start=0, maximum=0)
        self.count = count

    def backoff(self, attempt: int) -> float:
        return 0

    def delays(self):
        for i in range(self.count):
            yield 0


class RetryDecoratorTest(TestCase):
    @responses.activate(registry=responses.registries.OrderedRegistry)
    def test_exhaustion_after_retry(self):
        url = "https://example.com"
        responses.get(url=url, body=Timeout())
        responses.get(url=url, body=Timeout())
        responses.get(url=url, body=Timeout())

        backoff = MockBackoff(2)

        @retry_with_backoff(backoff=backoff, exceptions=Timeout)
        def call_api():
            r = requests.get(url=url)
            return r.text

        with self.assertRaises(expected_exception=Timeout) as e:
            call_api()
        self.assertIsInstance(obj=e.exception, cls=Timeout)
        responses.mock.assert_call_count(url=url, count=3)

    @responses.activate(registry=responses.registries.OrderedRegistry)
    def test_success_after_retry(self):
        url = "https://example.com"
        responses.get(url=url, body=Timeout())
        responses.get(url=url, body=Timeout())
        responses.get(url=url, body="hello")

        backoff = MockBackoff(2)

        @retry_with_backoff(backoff=backoff, exceptions=Timeout)
        def call_api():
            r = requests.get(url=url)
            return r.text

        self.assertEqual("hello", call_api())
        responses.mock.assert_call_count(url=url, count=3)

    @responses.activate(registry=responses.registries.OrderedRegistry)
    def test_success_without_retry(self):
        url = "https://example.com"
        responses.get(url=url, body="hello")

        backoff = MockBackoff(2)

        @retry_with_backoff(backoff=backoff, exceptions=Timeout)
        def call_api():
            r = requests.get(url=url)
            return r.text

        self.assertEqual("hello", call_api())
        responses.mock.assert_call_count(url=url, count=1)

    @responses.activate(registry=responses.registries.OrderedRegistry)
    def test_success_after_retry_with_should_retry(self):
        url = "https://example.com"
        # Adding the Timeout responses followed by a successful response
        responses.get(url=url, body=Timeout())
        responses.get(url=url, body=Timeout())
        responses.get(url=url, body="hello")

        backoff = MockBackoff(2)

        def should_retry(e: Exception):
            return isinstance(e, Timeout)

        @retry_with_backoff(
            backoff=backoff, exceptions=(HTTPError, Timeout), should_retry=should_retry
        )
        def call_api():
            r = requests.get(url=url)
            return r.text

        self.assertEqual("hello", call_api())
        self.assertEqual(len(responses.calls), 3)
