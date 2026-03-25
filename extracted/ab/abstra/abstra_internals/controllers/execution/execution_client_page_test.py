import unittest
from unittest.mock import MagicMock

from abstra_internals.controllers.execution.execution_client_page import PageClient
from abstra_internals.entities.execution_context import PageContext, Request, Response
from abstra_internals.interface.sdk.user_exceptions import (
    AuthorizationRequired,
    GetUserFailed,
)
from abstra_internals.settings import Settings

Settings.set_root_path("/tmp")


def _make_client() -> PageClient:
    context = PageContext(
        request=Request(headers={}, body="", query_params={}, method="GET"),
        response=Response(headers={}, status=200, body=""),
    )
    conn = MagicMock()
    client = PageClient(context=context, conn=conn, production_mode=False)
    client._send = MagicMock()  # type: ignore
    return client


class TestPageClientAuthFailure(unittest.TestCase):
    def test_get_user_failed_sets_401(self):
        client = _make_client()
        client.handle_failure(GetUserFailed())
        self.assertEqual(client.response.status, 401)
        self.assertIn("Failed to get the current user", client.response.body)

    def test_authorization_required_sets_401(self):
        client = _make_client()
        client.handle_failure(AuthorizationRequired("Custom msg"))
        self.assertEqual(client.response.status, 401)
        self.assertIn("Custom msg", client.response.body)

    def test_generic_exception_sets_500(self):
        client = _make_client()
        client.handle_failure(Exception("something broke"))
        self.assertEqual(client.response.status, 500)
        self.assertIn("exception occurred", client.response.body)


class TestPageClientContextResponseSync(unittest.TestCase):
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


class TestExceptionHierarchy(unittest.TestCase):
    def test_get_user_failed_is_authorization_required(self):
        self.assertTrue(issubclass(GetUserFailed, AuthorizationRequired))

    def test_authorization_required_has_status_code(self):
        e = AuthorizationRequired()
        self.assertEqual(e.status_code, 401)

    def test_get_user_failed_inherits_status_code(self):
        e = GetUserFailed()
        self.assertEqual(e.status_code, 401)
        self.assertIsInstance(e, AuthorizationRequired)
