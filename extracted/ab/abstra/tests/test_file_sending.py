import io
import unittest

from abstra_internals.interface.sdk.forms.deprecated.widgets.file_utils import (
    upload_widget_file,
)
from abstra_internals.server.apps import get_local_app
from abstra_internals.server.utils import _immutable_cache_control, send_from_dist
from abstra_internals.utils.file import make_random_tmp_path
from tests.fixtures import BaseTest, clear_dir


class TestAssetCaching(unittest.TestCase):
    def test_hashed_bundle_asset_is_immutable(self):
        self.assertEqual(
            _immutable_cache_control(
                from_bundle=True, filename="assets/editor.main-DfIhb9tT.js"
            ),
            "public, max-age=31536000, immutable",
        )

    def test_html_shell_keeps_default(self):
        # The SPA entry shell must revalidate so it points at the current hashes.
        self.assertIsNone(
            _immutable_cache_control(from_bundle=True, filename="editor.html")
        )

    def test_project_files_are_never_immutable(self):
        # Served from a caller-supplied dist_folder (e.g. project root) => mutable.
        self.assertIsNone(
            _immutable_cache_control(from_bundle=False, filename="assets/foo.js")
        )


class TestFileSending(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.app = get_local_app(self.controller)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        self.app_context.pop()
        clear_dir(self.root)

    def test_mime_type(self):
        with self.app.test_request_context("/test.js"):
            js_file = "test.js"
            self.root.joinpath(js_file).write_text("console.log('hello world')")
            html_file = "test.html"
            self.root.joinpath(html_file).write_text("<h1>Hello world</h1>")
            css_file = "test.css"
            self.root.joinpath(css_file).write_text("h1 { color: red; }")

            js_response = send_from_dist(str(js_file), "index.html", self.root)
            self.assertEqual(js_response.mimetype, "application/javascript")
            self.assertEqual(
                js_response.headers["Content-Type"],
                "application/javascript; charset=utf-8",
            )
            html_response = send_from_dist(str(html_file), "index.html", self.root)
            self.assertEqual(html_response.mimetype, "text/html")
            self.assertEqual(
                html_response.headers["Content-Type"], "text/html; charset=utf-8"
            )
            css_response = send_from_dist(str(css_file), "index.html", self.root)
            self.assertEqual(css_response.mimetype, "text/css")
            self.assertEqual(
                css_response.headers["Content-Type"], "text/css; charset=utf-8"
            )

    def test_cache_control_wiring(self):
        # Exercises the real response headers, not just the pure helper: the
        # `from_bundle = dist_folder == _DIST_FOLDER` computation and the
        # fallback-path early return (which must NOT get the immutable header).
        from abstra_internals.server import utils

        self.root.joinpath("assets").mkdir(exist_ok=True)
        self.root.joinpath("assets", "x-hash.js").write_text("console.log(1)")
        self.root.joinpath("editor.html").write_text("<h1>shell</h1>")

        # Treat the temp dir as the built bundle so the hashed asset qualifies.
        original = utils._DIST_FOLDER
        utils._DIST_FOLDER = self.root
        try:
            with self.app.test_request_context("/assets/x-hash.js"):
                hashed = send_from_dist("assets/x-hash.js", dist_folder=self.root)
                self.assertIn("immutable", hashed.headers.get("Cache-Control", ""))

            # Missing file -> fallback to the HTML shell, which must stay revalidating.
            with self.app.test_request_context("/missing.js"):
                shell = send_from_dist(
                    "missing.js", "editor.html", dist_folder=self.root
                )
                self.assertNotIn("immutable", shell.headers.get("Cache-Control", ""))
        finally:
            utils._DIST_FOLDER = original


class TestFileUtils(BaseTest):
    def test_make_random_tmp_path(self):
        path = make_random_tmp_path("test.txt")
        self.assertEqual(path.name, "test.txt")


class TestFileUpload(BaseTest):
    def test_upload_widget_file_path(self):
        tmp_file = self.root.joinpath("tmp.txt")
        tmp_file.write_text("hello world")

        external_path = upload_widget_file(tmp_file)

        # assert path format like /_files/uuid/filename
        self.assertTrue(external_path.startswith("/_files/"))
        self.assertTrue(external_path.endswith("/tmp.txt"))

        # assert file exists
        res = self.get_cloud_flask_client().get(external_path)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"hello world")

    def test_upload_widget_file_buffered_reader(self):
        tmp_file = self.root.joinpath("tmp.txt")
        tmp_file.write_text("hello world")

        with open(tmp_file, "rb") as f:
            external_path = upload_widget_file(f)

        # assert path format like /_files/uuid/filename
        self.assertTrue(external_path.startswith("/_files/"))
        self.assertTrue(external_path.endswith("/tmp.txt"))

        # assert file exists
        res = self.get_cloud_flask_client().get(external_path)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"hello world")

    def test_upload_widget_file_io(self):
        external_path = upload_widget_file(io.BytesIO(b"hello world"))

        # assert path format like /_files/uuid
        self.assertTrue(external_path.startswith("/_files/"))

        # assert file exists
        res = self.get_cloud_flask_client().get(external_path)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"hello world")
