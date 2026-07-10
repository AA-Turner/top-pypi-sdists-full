import unittest
from unittest.mock import MagicMock, patch

import flask

from abstra_internals.server.apps.local import (
    _guard,
    _register_editor_auth_renewal,
)
from abstra_internals.server.blueprints.editor import _safe_redirect_path

PROJECT_ID = "proj-1"
NAVIGATION_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"


def make_app() -> flask.Flask:
    app = flask.Flask(__name__)

    @app.route("/_editor/")
    def _index():
        return "ok"

    return app


@patch("abstra_internals.server.apps.local.EDITOR_MODE", "web")
@patch("abstra_internals.server.apps.local.PROJECT_ID", PROJECT_ID)
class TestGuard(unittest.TestCase):
    def setUp(self):
        self.app = make_app()

    def test_valid_token_passes(self):
        with self.app.test_request_context(
            "/_editor/", headers={"Cookie": "editor_auth=valid"}
        ):
            with patch(
                "abstra_internals.server.apps.local.decode_jwt",
                return_value={"authorId": "a"},
            ) as mock_decode:
                self.assertIsNone(_guard())
                mock_decode.assert_called_once_with(
                    "valid", aud=f"web-editor-{PROJECT_ID}"
                )

    def test_navigation_with_expired_token_redirects_to_console(self):
        with self.app.test_request_context(
            "/_editor/",
            headers={"Cookie": "editor_auth=expired", "Accept": NAVIGATION_ACCEPT},
        ):
            with patch(
                "abstra_internals.server.apps.local.decode_jwt", return_value=None
            ):
                response = _guard()

        assert response is not None
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.headers["Location"].startswith(
                f"https://cloud.abstra.io/projects/{PROJECT_ID}/web-editor"
            )
        )
        self.assertIn("redirect=%2F_editor%2F", response.headers["Location"])

    def test_navigation_without_token_redirects_to_console(self):
        with self.app.test_request_context(
            "/_editor/", headers={"Accept": NAVIGATION_ACCEPT}
        ):
            response = _guard()

        assert response is not None
        self.assertEqual(response.status_code, 302)

    def test_xhr_without_token_gets_401(self):
        with self.app.test_request_context(
            "/_editor/api/stages", headers={"Accept": "*/*"}
        ):
            response = _guard()

        assert response is not None
        self.assertEqual(response.status_code, 401)

    def test_xhr_with_invalid_token_gets_403(self):
        with self.app.test_request_context(
            "/_editor/api/stages",
            headers={"Cookie": "editor_auth=bad", "Accept": "*/*"},
        ):
            with patch(
                "abstra_internals.server.apps.local.decode_jwt", return_value=None
            ):
                response = _guard()

        assert response is not None
        self.assertEqual(response.status_code, 403)

    def test_local_mode_skips_guard(self):
        with patch("abstra_internals.server.apps.local.EDITOR_MODE", "local"):
            with self.app.test_request_context("/_editor/"):
                self.assertIsNone(_guard())


@patch("abstra_internals.server.apps.local.EDITOR_MODE", "web")
@patch("abstra_internals.server.apps.local.PROJECT_ID", PROJECT_ID)
class TestEditorAuthRenewalHook(unittest.TestCase):
    def _build_app_with_renewer(self, renewer: MagicMock) -> flask.Flask:
        app = make_app()
        with patch(
            "abstra_internals.server.apps.local.EditorAuthRenewer",
            return_value=renewer,
        ):
            _register_editor_auth_renewal(app, MagicMock())
        return app

    def test_sets_cookie_when_fresh_token_is_available(self):
        renewer = MagicMock()
        renewer.fresh_token_for.return_value = "renewed-token"
        app = self._build_app_with_renewer(renewer)

        client = app.test_client()
        client.set_cookie("editor_auth", "old-token")
        response = client.get("/_editor/")

        renewer.fresh_token_for.assert_called_once_with("old-token")
        set_cookie = response.headers.get("Set-Cookie", "")
        self.assertIn("editor_auth=renewed-token", set_cookie)
        self.assertIn("HttpOnly", set_cookie)

    def test_kicks_off_renewal_when_token_is_near_expiration(self):
        renewer = MagicMock()
        renewer.fresh_token_for.return_value = None
        app = self._build_app_with_renewer(renewer)

        client = app.test_client()
        client.set_cookie("editor_auth", "old-token")
        with patch(
            "abstra_internals.server.apps.local.decode_jwt",
            return_value={"exp": 1234567890},
        ):
            response = client.get("/_editor/")

        renewer.maybe_renew.assert_called_once_with("old-token", 1234567890)
        self.assertNotIn("editor_auth", response.headers.get("Set-Cookie", ""))

    def test_does_nothing_without_cookie(self):
        renewer = MagicMock()
        app = self._build_app_with_renewer(renewer)

        app.test_client().get("/_editor/")

        renewer.fresh_token_for.assert_not_called()
        renewer.maybe_renew.assert_not_called()

    def test_does_nothing_in_local_mode(self):
        renewer = MagicMock()
        app = self._build_app_with_renewer(renewer)

        client = app.test_client()
        client.set_cookie("editor_auth", "old-token")
        with patch("abstra_internals.server.apps.local.EDITOR_MODE", "local"):
            client.get("/_editor/")

        renewer.fresh_token_for.assert_not_called()


class TestSafeRedirectPath(unittest.TestCase):
    def test_relative_path_is_kept(self):
        self.assertEqual(_safe_redirect_path("/_editor/stages"), "/_editor/stages")

    def test_defaults_to_editor_root(self):
        self.assertEqual(_safe_redirect_path(None), "/_editor/")

    def test_rejects_protocol_relative_url(self):
        self.assertEqual(_safe_redirect_path("//evil.com/x"), "/_editor/")

    def test_rejects_absolute_url(self):
        self.assertEqual(_safe_redirect_path("https://evil.com"), "/_editor/")


if __name__ == "__main__":
    unittest.main()
