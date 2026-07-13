"""Note: This test script expects the dhooks_lite module to be installed
in the current environment, e.g. with pip install -e
"""

import json
import logging
from unittest import TestCase
from unittest.mock import Mock, patch

import requests_mock

from dhooks_lite import (
    Embed,
    UserAgent,
    Webhook,
    WebhookResponse,
    __title__,
    __url__,
    __version__,
)

MODULE_PATH = "dhooks_lite.client"

TEST_URL_1 = "https://www.example.com/test-url-1/"
TEST_URL_2 = "https://www.example.com/test-url-2/"


def extract_contents(requests_mocker: Mock):
    """extract results from mock requests"""
    url = None
    json_data = None
    for x in requests_mocker.post.call_args:
        if type(x) is dict and "url" in x:
            url = x["url"]
        if type(x) is dict and "data" in x:
            json_data = json.loads(x["data"])

    return url, json_data


def my_sleep(value):
    """mock function for sleep that also checks for valid values"""
    if value < 0:
        raise ValueError("sleep length must be non-negative")


@requests_mock.Mocker()
class TestWebhook(TestCase):
    def test_has_repr(self, requests_mocker):
        # given
        obj = Webhook(TEST_URL_1)
        # then
        self.assertTrue(repr(obj))

    def test_has_str(self, requests_mocker):
        # given
        obj = Webhook(TEST_URL_1)
        # then
        self.assertTrue(str(obj))

    def test_can_set_webhook_url(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_2,
            status_code=200,
            json={"message": True},
        )
        hook = Webhook(TEST_URL_2)
        self.assertEqual(hook.url, TEST_URL_2)
        hook.execute("Hi there")
        self.assertTrue(requests_mocker.called)

    def test_request_has_headers(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_2,
            status_code=200,
            json={"message": True},
        )
        hook = Webhook(TEST_URL_2)
        self.assertEqual(hook.url, TEST_URL_2)
        hook.execute("Hi there")

        headers = requests_mocker.last_request.headers
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(
            headers["User-Agent"],
            "{} ({}, {})".format(__title__, __url__, __version__),
        )

    def test_request_has_custom_user_agent(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_2,
            status_code=200,
            json={"message": True},
        )
        hook = Webhook(TEST_URL_2, user_agent=UserAgent("name", "url", "version"))
        self.assertEqual(hook.url, TEST_URL_2)
        hook.execute("Hi there")

        headers = requests_mocker.last_request.headers
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(headers["User-Agent"], "name (url, version)")

    def test_detects_missing_webhook_url(self, requests_mocker):
        with self.assertRaises(ValueError):
            Webhook(None)  # type: ignore

        self.assertFalse(requests_mocker.called)

    def test_can_set_content(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=200,
            json={"message": True},
        )

        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there")
        self.assertDictEqual(
            requests_mocker.last_request.json(), {"content": "Hi there"}
        )

    def test_detects_max_character_limit(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=200,
            json={"message": True},
        )

        hook = Webhook(TEST_URL_1)
        large_string = "x" * 2001
        with self.assertRaises(ValueError):
            hook.execute(large_string)

        self.assertFalse(requests_mocker.called)

    def test_can_get_send_report(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1 + "?wait=True",
            status_code=200,
            json={"message": True},
        )

        hook = Webhook(TEST_URL_1)
        response = hook.execute("Hi there", wait_for_response=True)
        self.assertEqual(response.content, {"message": True})

    def test_detects_missing_content_and_embed(self, requests_mocker):
        hook = Webhook(TEST_URL_1)
        with self.assertRaises(ValueError):
            hook.execute()

        self.assertFalse(requests_mocker.called)

    def test_can_set_username(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=200,
            json={"message": True},
        )
        hook = Webhook(TEST_URL_1, username="Bruce Wayne")
        self.assertEqual(hook.username, "Bruce Wayne")

        hook.execute("Hi there")
        self.assertDictEqual(
            requests_mocker.last_request.json(),
            {"content": "Hi there", "username": "Bruce Wayne"},
        )

    def test_can_set_avatar_url(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=200,
            json={"message": True},
        )

        hook = Webhook(TEST_URL_1, avatar_url="abc")
        self.assertEqual(hook.avatar_url, "abc")

        hook.execute("Hi there")
        self.assertDictEqual(
            requests_mocker.last_request.json(),
            {"content": "Hi there", "avatar_url": "abc"},
        )

    def test_can_send_with_tts(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=200,
            json={"message": True},
        )
        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there", tts=True)
        self.assertDictEqual(
            requests_mocker.last_request.json(), {"content": "Hi there", "tts": True}
        )

    def test_detect_wrong_tts_type(self, requests_mocker):
        hook = Webhook(TEST_URL_1)
        with self.assertRaises(TypeError):
            hook.execute("Hi there", tts=int(5))  # type: ignore

        self.assertFalse(requests_mocker.called)

    def test_detects_wrong_embeds_type(self, requests_mocker):
        hook = Webhook(TEST_URL_1)
        with self.assertRaises(TypeError):
            hook.execute("dummy", embeds=int(5))  # type: ignore

        self.assertFalse(requests_mocker.called)

    def test_detects_wrong_embeds_element_type(self, requests_mocker):
        hook = Webhook(TEST_URL_1)
        e = [int(5), float(5)]
        with self.assertRaises(TypeError):
            hook.execute("dummy", embeds=e)

        self.assertFalse(requests_mocker.called)

    def test_returns_none_on_invalid_response(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=200,
            text="this is no JSON",
        )
        hook = Webhook(TEST_URL_1)
        response = hook.execute("Hi there")
        self.assertIsNone(response.content)

    @patch(MODULE_PATH + ".logger.getEffectiveLevel", return_value=logging.DEBUG)
    def test_produce_debug_logging(self, requests_mocker, mock_logger):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=200,
            json={"message": True},
        )
        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there")

    @patch(MODULE_PATH + ".logger.getEffectiveLevel", return_value=logging.INFO)
    def test_produce_normal_logging_with_http_error(self, requests_mocker, mock_logger):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=404,
            json={"message": True},
        )
        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there")

    @patch(MODULE_PATH + ".logger.getEffectiveLevel", return_value=logging.INFO)
    def test_produce_no_logging_when_http_ok(self, requests_mocker, mock_logger):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=200,
            json={"message": True},
        )
        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there")

    @patch(MODULE_PATH + ".BACKOFF_FACTOR", 0.5)
    @patch(MODULE_PATH + ".sleep")
    def test_can_retry_on_retryable_error_502(self, requests_mocker, mock_sleep):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=502,
            json={"message": True},
        )
        mock_sleep.side_effect = my_sleep

        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there", max_retries=3)
        self.assertEqual(requests_mocker.call_count, 4)

        call_list = mock_sleep.call_args_list
        result = [args[0] for args, kwargs in [x for x in call_list]]
        expected = [1.0, 2.0]
        self.assertListEqual(expected, result)

    @patch(MODULE_PATH + ".sleep")
    def test_can_retry_on_retryable_error_503(self, requests_mocker, mock_sleep):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            [
                {"status_code": 503, "json": {"message": True}},
                {"status_code": 200, "json": {"message": True}},
            ],
        )
        mock_sleep.side_effect = my_sleep

        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there", max_retries=3)
        self.assertEqual(requests_mocker.call_count, 2)

    @patch(MODULE_PATH + ".sleep")
    def test_can_retry_on_retryable_error_504(self, requests_mocker, mock_sleep):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            [
                {"status_code": 504, "json": {"message": True}},
                {"status_code": 200, "json": {"message": True}},
            ],
        )
        mock_sleep.side_effect = my_sleep

        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there", max_retries=3)
        self.assertEqual(requests_mocker.call_count, 2)

    @patch(MODULE_PATH + ".sleep")
    def test_can_set_max_retries_1(self, requests_mocker, mock_sleep):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=502,
            json={"message": True},
        )
        mock_sleep.side_effect = my_sleep

        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there", max_retries=3)
        self.assertEqual(requests_mocker.call_count, 4)

    @patch(MODULE_PATH + ".sleep")
    def test_can_set_max_retries_2(self, requests_mocker, mock_sleep):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=502,
            json={"message": True},
        )
        mock_sleep.side_effect = my_sleep

        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there", max_retries=1)
        self.assertEqual(requests_mocker.call_count, 2)

    @patch(MODULE_PATH + ".sleep")
    def test_can_set_max_retries_3(self, requests_mocker, mock_sleep):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=502,
            json={"message": True},
        )
        mock_sleep.side_effect = my_sleep

        hook = Webhook(TEST_URL_1)
        hook.execute("Hi there", max_retries=0)
        self.assertEqual(requests_mocker.call_count, 1)

    def test_can_return_response_when_status_ok(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=200,
            json={"message": "All is fine"},
        )
        hook = Webhook(TEST_URL_1)
        response = hook.execute("Hi there", wait_for_response=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.status_ok)
        self.assertEqual(response.content, {"message": "All is fine"})

    def test_can_return_response_for_http_error(self, requests_mocker):
        requests_mocker.register_uri(
            "POST",
            TEST_URL_1,
            status_code=429,
            json={
                "global": False,
                "message": "You are being rate limited.",
                "retry_after": 43081,
            },
        )
        hook = Webhook(TEST_URL_1)
        response = hook.execute("Hi there")
        self.assertEqual(response.status_code, 429)
        self.assertFalse(response.status_ok)
        self.assertEqual(
            response.content,
            {
                "global": False,
                "message": "You are being rate limited.",
                "retry_after": 43081,
            },
        )


class TestWebhookResponse(TestCase):
    def setUp(self):
        self.response = WebhookResponse(
            headers={"Content-Type": "application/json"},
            content={"username": "Bruce Wayne", "content": "Checkout this new report"},
            status_code=200,
        )

    def test_headers(self):
        expected = {"Content-Type": "application/json"}
        self.assertDictEqual(self.response.headers, expected)

    def test_status_code(self):
        expected = 200
        self.assertEqual(self.response.status_code, expected)

    def test_content(self):
        expected = {"username": "Bruce Wayne", "content": "Checkout this new report"}
        self.assertEqual(self.response.content, expected)

    def test_create(self):
        obj = WebhookResponse(
            headers={"headers": True}, status_code=200, content={"content": True}
        )
        self.assertEqual(obj.headers, {"headers": True})
        self.assertEqual(obj.status_code, 200)
        self.assertEqual(obj.content, {"content": True})

        obj_2 = WebhookResponse(
            headers={"headers": True}, status_code=200, content=None
        )
        self.assertIsNone(obj_2.content)

    def test_status_ok(self):
        x = WebhookResponse(headers={"headers": True}, status_code=199)
        self.assertFalse(x.status_ok)

        x = WebhookResponse(headers={"headers": True}, status_code=200)
        self.assertTrue(x.status_ok)

        x = WebhookResponse(headers={"headers": True}, status_code=300, content=None)
        self.assertFalse(x.status_ok)


@patch(MODULE_PATH + ".requests", spec=True)
class TestWebhookAndEmbed(TestCase):
    def setUp(self):
        x = Mock()
        x.headers = {"headers": True}
        x.status_code = 200
        x.json.return_value = {"message": True}
        self.response = x

    def test_can_send_with_embed_only(self, requests_mocker):
        requests_mocker.post.return_value = self.response

        hook = Webhook(TEST_URL_1)
        e = Embed(description="Hello, world!")
        hook.execute(embeds=[e])
        _, json = extract_contents(requests_mocker)
        self.assertIn("embeds", json)
        self.assertEqual(len(json["embeds"]), 1)
        self.assertDictEqual(
            json["embeds"][0], {"description": "Hello, world!", "type": "rich"}
        )

    def test_can_add_multiple_embeds(self, requests_mocker):
        requests_mocker.post.return_value = self.response

        hook = Webhook(TEST_URL_1)
        e1 = Embed(description="Hello, world!")
        e2 = Embed(description="Hello, world! Again!")
        hook.execute("How is it going?", embeds=[e1, e2])
        _, json = extract_contents(requests_mocker)
        self.assertIn("embeds", json)
        self.assertEqual(len(json["embeds"]), 2)
        self.assertDictEqual(
            json["embeds"][0], {"description": "Hello, world!", "type": "rich"}
        )
        self.assertDictEqual(
            json["embeds"][1], {"description": "Hello, world! Again!", "type": "rich"}
        )


class TestUserAgent(TestCase):
    def test_create(self):
        obj = UserAgent("dummy", "url", "version")
        self.assertEqual(obj.name, "dummy")
        self.assertEqual(obj.url, "url")
        self.assertEqual(obj.version, "version")

    def test_str(self):
        obj = UserAgent("dummy", "url", "version")
        self.assertEqual(str(obj), "dummy (url, version)")
