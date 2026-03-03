import json
import urllib.error
import urllib.request
from typing import Optional
from unittest import TestCase

from abstra_internals.interface.sdk.agent_callback_server import AgentCallbackServer


class TestAgentCallbackServer(TestCase):
    def _post(
        self, url: str, path: str, body: dict, secret: Optional[str] = None
    ) -> tuple[int, dict]:
        data = json.dumps(body).encode("utf-8")
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if secret is not None:
            headers["X-Callback-Secret"] = secret
        req = urllib.request.Request(
            f"{url}{path}",
            data=data,
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_empty_functions_raises(self):
        with self.assertRaises(ValueError):
            AgentCallbackServer({})

    def test_start_returns_url_and_secret(self):
        server = AgentCallbackServer({"noop": lambda: None})
        try:
            url, secret = server.start()
            self.assertTrue(url.startswith("http://127.0.0.1:"))
            self.assertIsInstance(secret, str)
            self.assertTrue(len(secret) > 0)
        finally:
            server.stop()

    def test_execute_simple_function(self):
        def add(a: int, b: int) -> int:
            return a + b

        server = AgentCallbackServer({"add": add})
        try:
            url, secret = server.start()
            status, body = self._post(
                url,
                "/execute",
                {
                    "toolName": "add",
                    "input": {"a": 3, "b": 5},
                },
                secret=secret,
            )
            self.assertEqual(status, 200)
            self.assertEqual(body["result"], 8)
        finally:
            server.stop()

    def test_execute_function_returning_dict(self):
        def get_user(name: str) -> dict:
            return {"name": name, "role": "admin"}

        server = AgentCallbackServer({"get_user": get_user})
        try:
            url, secret = server.start()
            status, body = self._post(
                url,
                "/execute",
                {
                    "toolName": "get_user",
                    "input": {"name": "Alice"},
                },
                secret=secret,
            )
            self.assertEqual(status, 200)
            self.assertEqual(body["result"], {"name": "Alice", "role": "admin"})
        finally:
            server.stop()

    def test_execute_tool_not_found(self):
        server = AgentCallbackServer({"real": lambda: "ok"})
        try:
            url, secret = server.start()
            status, body = self._post(
                url,
                "/execute",
                {
                    "toolName": "missing",
                    "input": {},
                },
                secret=secret,
            )
            self.assertEqual(status, 404)
            self.assertIn("Tool not found", body["error"])
        finally:
            server.stop()

    def test_execute_function_raises_error(self):
        def bad_func():
            raise ValueError("something went wrong")

        server = AgentCallbackServer({"bad_func": bad_func})
        try:
            url, secret = server.start()
            status, body = self._post(
                url,
                "/execute",
                {
                    "toolName": "bad_func",
                    "input": {},
                },
                secret=secret,
            )
            self.assertEqual(status, 500)
            self.assertEqual(body["error"], "Tool execution failed")
        finally:
            server.stop()

    def test_wrong_path_returns_404(self):
        server = AgentCallbackServer({"noop": lambda: None})
        try:
            url, secret = server.start()
            status, body = self._post(
                url, "/wrong", {"toolName": "noop"}, secret=secret
            )
            self.assertEqual(status, 404)
            self.assertIn("Not found", body["error"])
        finally:
            server.stop()

    def test_missing_tool_name_returns_400(self):
        server = AgentCallbackServer({"noop": lambda: None})
        try:
            url, secret = server.start()
            status, body = self._post(url, "/execute", {"input": {}}, secret=secret)
            self.assertEqual(status, 400)
            self.assertIn("toolName", body["error"])
        finally:
            server.stop()

    def test_stop_is_idempotent(self):
        server = AgentCallbackServer({"noop": lambda: None})
        server.start()
        server.stop()
        server.stop()  # should not raise

    def test_execute_with_no_input_field(self):
        def greet() -> str:
            return "hello"

        server = AgentCallbackServer({"greet": greet})
        try:
            url, secret = server.start()
            status, body = self._post(
                url, "/execute", {"toolName": "greet"}, secret=secret
            )
            self.assertEqual(status, 200)
            self.assertEqual(body["result"], "hello")
        finally:
            server.stop()

    # --- New security tests ---

    def test_missing_secret_returns_403(self):
        server = AgentCallbackServer({"noop": lambda: None})
        try:
            url, _secret = server.start()
            status, body = self._post(
                url,
                "/execute",
                {"toolName": "noop", "input": {}},
                secret=None,
            )
            self.assertEqual(status, 403)
            self.assertIn("Forbidden", body["error"])
        finally:
            server.stop()

    def test_wrong_secret_returns_403(self):
        server = AgentCallbackServer({"noop": lambda: None})
        try:
            url, _secret = server.start()
            status, body = self._post(
                url,
                "/execute",
                {"toolName": "noop", "input": {}},
                secret="wrong-secret",
            )
            self.assertEqual(status, 403)
            self.assertIn("Forbidden", body["error"])
        finally:
            server.stop()

    def test_non_dict_input_returns_400(self):
        server = AgentCallbackServer({"echo": lambda x: x})
        try:
            url, secret = server.start()
            status, body = self._post(
                url,
                "/execute",
                {"toolName": "echo", "input": "not-a-dict"},
                secret=secret,
            )
            self.assertEqual(status, 400)
            self.assertIn("'input' must be an object", body["error"])
        finally:
            server.stop()
