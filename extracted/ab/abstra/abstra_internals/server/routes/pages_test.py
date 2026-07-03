import unittest
from unittest.mock import MagicMock

import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.server.routes.pages import get_editor_bp

HTML_BODY = "<!-- abstra pages --><h1>Hi</h1>"


class TestRunPageRoute(unittest.TestCase):
    def setUp(self):
        self.controller = MagicMock(spec=MainController)
        self.bp = get_editor_bp(self.controller)
        self.app = flask.Flask(__name__)
        self.app.register_blueprint(self.bp, url_prefix="/pages")
        self.client = self.app.test_client()

        self.controller.get_page_stage.return_value = MagicMock()
        self.controller.run_page_stage.return_value = {
            "body": HTML_BODY,
            "status": 200,
            "headers": {"Content-Type": "text/html"},
            "executionId": "exec-1",
        }

    def test_get_render_injects_auth_meta_from_editor_auth_cookie(self):
        self.client.set_cookie("editor_auth", "cookie-jwt")
        resp = self.client.get("/pages/p1/run")
        body = resp.data.decode()
        self.assertIn('<meta name="abstra-auth-token" content="cookie-jwt">', body)
        self.assertIn("window.abstra.logged", body)

    def test_get_render_injects_auth_meta_from_bearer_header(self):
        resp = self.client.get(
            "/pages/p1/run",
            headers={"Authorization": "Bearer hdr-jwt"},
        )
        body = resp.data.decode()
        self.assertIn('<meta name="abstra-auth-token" content="hdr-jwt">', body)

    def test_get_render_injects_execution_id_meta(self):
        resp = self.client.get("/pages/p1/run")
        body = resp.data.decode()
        self.assertIn('<meta name="abstra-execution-id" content="exec-1">', body)
        self.assertEqual(resp.headers.get("X-Execution-Id"), "exec-1")

    def test_get_render_injects_endpoint_meta_with_query(self):
        resp = self.client.get("/pages/p1/run?foo=1")
        body = resp.data.decode()
        self.assertIn('name="abstra-page-endpoint"', body)
        self.assertIn("/pages/p1/run", body)
        self.assertIn("foo=1", body)

    def test_post_function_call_not_scaffolded(self):
        self.controller.run_page_stage.return_value = {
            "body": '{"result": 1}',
            "status": 200,
            "headers": {"Content-Type": "application/json"},
            "executionId": None,
        }
        resp = self.client.post(
            "/pages/p1/run",
            json={"function": "greet", "params": {}},
        )
        body = resp.data.decode()
        self.assertNotIn("abstra-auth-token", body)
        self.assertNotIn("window.abstra", body)
        self.assertEqual(body, '{"result": 1}')

    def test_no_auth_token_omits_auth_meta(self):
        resp = self.client.get("/pages/p1/run")
        body = resp.data.decode()
        self.assertNotIn('<meta name="abstra-auth-token"', body)

    def test_missing_page_returns_404(self):
        self.controller.get_page_stage.return_value = None
        resp = self.client.get("/pages/missing/run")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
