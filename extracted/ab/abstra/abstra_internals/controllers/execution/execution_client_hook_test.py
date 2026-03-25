import unittest
from unittest.mock import MagicMock

from abstra_internals.controllers.execution.execution_client_hook import HookClient
from abstra_internals.entities.execution_context import HookContext, Request, Response
from abstra_internals.settings import Settings

Settings.set_root_path("/tmp")


def _make_client() -> HookClient:
    context = HookContext(
        request=Request(headers={}, body="", query_params={}, method="POST"),
        response=Response(headers={}, status=200, body=""),
    )
    conn = MagicMock()
    client = HookClient(context=context, conn=conn, production_mode=False)
    client._send = MagicMock()  # type: ignore
    return client


class TestHookClientContextResponseSync(unittest.TestCase):
    def test_set_response_syncs_body_to_context(self):
        client = _make_client()
        client.set_response(
            200, '{"message": "hello"}', {"Content-Type": "application/json"}
        )
        self.assertEqual(client.context.response.body, '{"message": "hello"}')

    def test_set_response_syncs_status_to_context(self):
        client = _make_client()
        client.set_response(201, "created", {})
        self.assertEqual(client.context.response.status, 201)

    def test_set_response_syncs_headers_to_context(self):
        client = _make_client()
        client.set_response(200, "ok", {"X-Custom": "value"})
        self.assertEqual(client.context.response.headers, {"X-Custom": "value"})

    def test_context_response_is_same_object_as_response(self):
        client = _make_client()
        client.set_response(200, "body", {})
        self.assertIs(client.context.response, client.response)

    def test_handle_failure_syncs_500_to_context(self):
        client = _make_client()
        client.handle_failure(Exception("boom"))
        self.assertEqual(client.context.response.status, 500)
        self.assertIn("exception occurred", client.context.response.body)

    def test_context_response_starts_empty(self):
        client = _make_client()
        self.assertEqual(client.context.response.body, "")
        self.assertEqual(client.context.response.status, 200)
