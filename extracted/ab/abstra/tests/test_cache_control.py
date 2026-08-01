import unittest

import flask

from abstra_internals.server.cache.control import Cache


class TestStaticsCachePolicy(unittest.TestCase):
    """The statics policy must cache content-hashed /assets/* immutably even when
    caching is otherwise disabled (web-editor pods run with enabled=False), while
    still keeping the SPA HTML shell and non-hashed statics revalidating."""

    def _client(self, enabled: bool):
        app = flask.Flask(__name__)
        cache = Cache(enabled=enabled)

        @app.get("/assets/<path:f>")
        @cache.statics()
        def asset(f: str):
            # "missing" simulates the SPA catch-all falling back to the HTML shell.
            if f == "missing":
                return flask.Response("<html>", content_type="text/html; charset=utf-8")
            return flask.Response("x", content_type="application/javascript")

        @app.get("/other.js")
        @cache.statics()
        def other():
            return flask.Response("x", content_type="application/javascript")

        return app.test_client()

    def test_hashed_asset_is_immutable_even_when_disabled(self):
        res = self._client(enabled=False).get("/assets/editor-DfIhb9tT.js")
        self.assertEqual(
            res.headers["Cache-Control"], "public, max-age=31536000, immutable"
        )

    def test_assets_html_fallback_is_not_cached(self):
        # An unknown /assets/ path resolves to the HTML shell — must revalidate.
        res = self._client(enabled=False).get("/assets/missing")
        self.assertNotIn("immutable", res.headers.get("Cache-Control", ""))

    def test_non_asset_static_still_gated_on_enabled(self):
        res = self._client(enabled=False).get("/other.js")
        self.assertNotIn("immutable", res.headers.get("Cache-Control", ""))

    def test_hashed_asset_immutable_when_enabled_too(self):
        res = self._client(enabled=True).get("/assets/editor-DfIhb9tT.js")
        self.assertEqual(
            res.headers["Cache-Control"], "public, max-age=31536000, immutable"
        )


if __name__ == "__main__":
    unittest.main()
