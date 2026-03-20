import json
import unittest
from unittest.mock import MagicMock, call

from abstra_internals.controllers.execution.execution_client_page import PageClient
from abstra_internals.controllers.sdk.sdk_pages import PageSDKController
from abstra_internals.entities.execution_context import PageContext, Request, Response
from abstra_internals.settings import Settings

Settings.set_root_path("/tmp")


def _make_sdk() -> tuple[PageSDKController, PageClient]:
    context = PageContext(
        request=Request(headers={}, body="", query_params={}, method="POST"),
        response=Response(headers={}, status=200, body=""),
    )
    conn = MagicMock()
    client = PageClient(context=context, conn=conn, production_mode=False)
    client._send = MagicMock()  # type: ignore
    users_repo = MagicMock()
    sdk = PageSDKController(client, users_repo)
    return sdk, client


class TestRegisterFunction(unittest.TestCase):
    def test_regular_function_sets_json_response(self):
        sdk, client = _make_sdk()

        @sdk.register_function
        def greet(name: str):
            return {"hello": name}

        client.context.request = Request(
            headers={},
            method="POST",
            query_params={},
            body=json.dumps({"function": "greet", "params": {"name": "world"}}),
        )
        sdk.handle_request()

        self.assertEqual(client.response.status, 200)
        data = json.loads(client.response.body)
        self.assertEqual(data["result"]["hello"], "world")

    def test_generator_function_streams(self):
        sdk, client = _make_sdk()

        @sdk.register_function
        def numbers():
            yield 1
            yield 2
            yield 3

        client.context.request = Request(
            headers={},
            method="POST",
            query_params={},
            body=json.dumps({"function": "numbers", "params": {}}),
        )
        sdk.handle_request()

        # Should have streamed via conn.send, not set response
        self.assertTrue(client._streamed)
        send_mock: MagicMock = client.conn.send  # type: ignore[assignment]
        calls = send_mock.call_args_list
        self.assertEqual(
            calls[0],
            call(
                {
                    "__page_stream__": "start",
                    "status": 200,
                    "headers": {"Content-Type": "application/x-ndjson"},
                }
            ),
        )
        self.assertEqual(calls[1], call({"__page_stream__": "chunk", "data": 1}))
        self.assertEqual(calls[2], call({"__page_stream__": "chunk", "data": 2}))
        self.assertEqual(calls[3], call({"__page_stream__": "chunk", "data": 3}))
        self.assertEqual(calls[4], call({"__page_stream__": "end"}))

    def test_generator_error_mid_stream(self):
        sdk, client = _make_sdk()

        @sdk.register_function
        def failing():
            yield "ok"
            raise ValueError("boom")

        client.context.request = Request(
            headers={},
            method="POST",
            query_params={},
            body=json.dumps({"function": "failing", "params": {}}),
        )
        sdk.handle_request()

        send_mock: MagicMock = client.conn.send  # type: ignore[assignment]
        calls = send_mock.call_args_list
        self.assertEqual(calls[0][0][0]["__page_stream__"], "start")
        self.assertEqual(calls[1], call({"__page_stream__": "chunk", "data": "ok"}))
        self.assertEqual(calls[2], call({"__page_stream__": "error", "error": "boom"}))

    def test_unknown_function_returns_404(self):
        sdk, client = _make_sdk()

        client.context.request = Request(
            headers={},
            method="POST",
            query_params={},
            body=json.dumps({"function": "nonexistent", "params": {}}),
        )
        sdk.handle_request()
        self.assertEqual(client.response.status, 404)


class TestJsStubGeneration(unittest.TestCase):
    def test_regular_function_generates_async(self):
        sdk, _ = _make_sdk()

        @sdk.register_function
        def get_data():
            return {}

        js = sdk._build_js_functions()
        self.assertIn("async function get_data()", js)
        self.assertNotIn("async function*", js)
        self.assertIn("return data.result", js)

    def test_generator_function_generates_stream_wrapper(self):
        sdk, _ = _make_sdk()

        @sdk.register_function
        def stream_data():
            yield 1

        js = sdk._build_js_functions()
        self.assertIn("function stream_data()", js)
        self.assertIn("async function* __stream()", js)
        self.assertIn("iter.then", js)
        self.assertIn("iter.forEach", js)
        self.assertIn("iter[Symbol.iterator]", js)
        self.assertIn("yield parsed.data", js)

    def test_render_not_exposed_in_js(self):
        sdk, _ = _make_sdk()

        @sdk.register_function
        def __render__():
            return "<h1>Hi</h1>"

        js = sdk._build_js_functions()
        self.assertNotIn("__render__", js)


class TestPageClientStreaming(unittest.TestCase):
    def test_handle_success_skips_response_when_streamed(self):
        context = PageContext(
            request=Request(headers={}, body="", query_params={}, method="GET"),
            response=Response(headers={}, status=200, body=""),
        )
        conn = MagicMock()
        client = PageClient(context=context, conn=conn, production_mode=False)
        client._send = MagicMock()  # type: ignore

        # Simulate streaming
        client.send_stream_start(200, {"Content-Type": "application/x-ndjson"})
        client.send_stream_chunk("data")
        client.send_stream_end()

        self.assertTrue(client._streamed)

        # handle_success should NOT send self.response
        conn.reset_mock()
        client.handle_success()

        # conn.send should NOT have been called (response skipped)
        conn.send.assert_not_called()

    def test_handle_success_sends_response_when_not_streamed(self):
        context = PageContext(
            request=Request(headers={}, body="", query_params={}, method="GET"),
            response=Response(headers={}, status=200, body=""),
        )
        conn = MagicMock()
        client = PageClient(context=context, conn=conn, production_mode=False)
        client._send = MagicMock()  # type: ignore

        client.set_response(200, "hello", {})
        client.handle_success()

        # conn.send should have been called with the response
        conn.send.assert_called_once()
        sent = conn.send.call_args[0][0]
        self.assertEqual(sent.body, "hello")
