"""E2E: the editor /run route (used by the run_page MCP tool) renders a page
with the logged-in preview scaffolding.

Exercises the REAL path with no mocks of the execution layer: a real
MainController + LocalProducerRepository actually execute the page's
``__render__``, the real editor ``_run_page`` route runs, real ``_handle_render``
builds the body, and ``build_standalone_preview_html`` injects the scaffolding.

A private page typically gates its UI on ``window.abstra.logged()`` (the
documented pattern in ``templates/new_page.py``). Before this fix, run_page's
direct render carried no ``window.abstra`` and no ``abstra-auth-token`` meta, so
``abstra.logged()`` was always false and such pages showed their logged-out
branch. These tests assert the route now injects that scaffolding when an
identity is present, and omits it otherwise.
"""

import flask
import jwt

from abstra_internals.server.routes.pages import get_editor_bp
from tests.fixtures import BaseTest

# Documented private-page pattern: the UI branches on the *client* abstra.logged().
private_page = """
from abstra.pages import register_function


@register_function
def __render__():
    return (
        '<div id="c">init</div>'
        '<script>document.getElementById("c").textContent ='
        ' window.abstra.logged() ? "SECRET" : "PLEASE-LOGIN";</script>'
    )
"""


class TestRunPagePrivatePreview(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.page = self.controller.create_stage("page", "Private", "private_page.py")
        self.page.file_path.write_text(private_page)
        # Register only the pages blueprint (real controller + LocalProducer) to
        # avoid importing the full editor app's browser/mcp tooling (playwright).
        app = flask.Flask(__name__)
        app.register_blueprint(
            get_editor_bp(self.controller), url_prefix="/_editor/api/pages"
        )
        self.client = app.test_client()
        # Any JWT carrying an email; in dev get_user/decode use skip_verify.
        self.editor_jwt = jwt.encode(
            {"email": "dev@example.com"}, "k", algorithm="HS256"
        )

    def _run(self, *, authed: bool):
        headers = {"Authorization": f"Bearer {self.editor_jwt}"} if authed else {}
        return self.client.get(
            f"/_editor/api/pages/{self.page.id}/run", headers=headers
        )

    def test_authed_render_injects_login_scaffolding(self):
        res = self._run(authed=True)
        body = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        # the real page body is present (real execution happened)
        self.assertIn('id="c"', body)
        # client scaffolding present -> abstra.logged() will return true
        self.assertIn(
            f'<meta name="abstra-auth-token" content="{self.editor_jwt}">', body
        )
        self.assertIn("window.abstra.logged", body)
        # the shim is defined before the page's own body script runs
        self.assertLess(body.index("window.abstra.logged"), body.index('id="c"'))

    def test_unauthed_render_omits_auth_token(self):
        res = self._run(authed=False)
        body = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('id="c"', body)
        # no identity -> no auth-token meta -> abstra.logged() will be false
        self.assertNotIn('<meta name="abstra-auth-token"', body)
        # but the shim is still defined (so abstra.logged() exists and returns false)
        self.assertIn("window.abstra.logged", body)
