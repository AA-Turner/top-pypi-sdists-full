import unittest

from abstra_internals.server.routes.page_preview import build_standalone_preview_html


class TestBuildStandalonePreviewHtml(unittest.TestCase):
    def test_injects_auth_token_meta(self):
        result = build_standalone_preview_html(
            "<h1>Hi</h1>",
            auth_token="tok123",
            endpoint=None,
            execution_id=None,
        )
        self.assertIn('<meta name="abstra-auth-token" content="tok123">', result)

    def test_injects_endpoint_meta(self):
        result = build_standalone_preview_html(
            "<h1>Hi</h1>",
            auth_token=None,
            endpoint="/_editor/api/pages/p1/run",
            execution_id=None,
        )
        self.assertIn(
            '<meta name="abstra-page-endpoint" content="/_editor/api/pages/p1/run">',
            result,
        )

    def test_injects_execution_id_meta(self):
        result = build_standalone_preview_html(
            "<h1>Hi</h1>",
            auth_token=None,
            endpoint=None,
            execution_id="exec-9",
        )
        self.assertIn('<meta name="abstra-execution-id" content="exec-9">', result)

    def test_injects_window_abstra_shim(self):
        result = build_standalone_preview_html(
            "<h1>Hi</h1>",
            auth_token="tok",
            endpoint=None,
            execution_id=None,
        )
        self.assertIn("window.abstra.logged", result)
        self.assertIn('meta[name="abstra-auth-token"]', result)
        self.assertIn("window.abstra.login", result)
        self.assertIn("window.abstra.logout", result)

    def test_original_body_preserved_and_last(self):
        body = "<h1>Hi</h1>"
        result = build_standalone_preview_html(
            body,
            auth_token="tok",
            endpoint=None,
            execution_id=None,
        )
        self.assertIn(body, result)
        self.assertTrue(result.endswith(body))

    def test_shim_precedes_body(self):
        body = "<h1>Hi</h1>"
        result = build_standalone_preview_html(
            body,
            auth_token="tok",
            endpoint=None,
            execution_id=None,
        )
        shim_idx = result.index("<script>")
        body_idx = result.index(body)
        self.assertLess(shim_idx, body_idx)

    def test_no_auth_token_omits_auth_meta(self):
        result = build_standalone_preview_html(
            "<h1>Hi</h1>",
            auth_token=None,
            endpoint=None,
            execution_id=None,
        )
        self.assertNotIn('<meta name="abstra-auth-token"', result)

    def test_no_execution_id_omits_exec_meta(self):
        result = build_standalone_preview_html(
            "<h1>Hi</h1>",
            auth_token=None,
            endpoint=None,
            execution_id=None,
        )
        self.assertNotIn("abstra-execution-id", result)

    def test_endpoint_query_is_escaped(self):
        result = build_standalone_preview_html(
            "<h1>Hi</h1>",
            auth_token=None,
            endpoint='/_editor/api/pages/p1/run?a=1&b="x"',
            execution_id=None,
        )
        self.assertIn("&amp;", result)
        self.assertIn("&quot;", result)
        self.assertNotIn('&b="x"', result)


if __name__ == "__main__":
    unittest.main()
