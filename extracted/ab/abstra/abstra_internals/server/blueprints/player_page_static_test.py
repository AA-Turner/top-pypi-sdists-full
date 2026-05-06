import datetime
import os
import pathlib
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock

import jwt as pyjwt

from abstra_internals.environment import CLOUD_API_PROD_SHARED_TOKEN
from abstra_internals.settings import Settings


def _sign(
    asset: str, exp_delta: datetime.timedelta = datetime.timedelta(hours=1)
) -> str:
    return pyjwt.encode(
        {
            "asset": asset,
            "exp": datetime.datetime.now(datetime.timezone.utc) + exp_delta,
        },
        key=CLOUD_API_PROD_SHARED_TOKEN,
        algorithm="HS256",
    )


class TestServePageStatic(unittest.TestCase):
    """Tests for the static-file handler that backs URLs returned by
    `register_static`."""

    def setUp(self):
        from abstra_internals.server.apps import get_cloud_app

        self.real_tmpdir = os.path.realpath(tempfile.mkdtemp())
        Settings.set_root_path(self.real_tmpdir)

        controller = MagicMock()
        app = get_cloud_app(controller)
        self.client = app.test_client()

    def tearDown(self):
        shutil.rmtree(self.real_tmpdir, ignore_errors=True)
        Settings.set_root_path("/tmp")

    def _write(self, *segments: str, content: bytes = b"x") -> str:
        path = pathlib.Path(self.real_tmpdir, *segments)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return "/".join(segments)

    def test_valid_token_serves_file(self):
        rel = self._write("static", "css", "page.css", content=b".x{}")
        token = _sign(rel)

        res = self.client.get(f"/_page-home/{rel}?token={token}")

        self.assertEqual(res.status_code, 200, res.data)
        self.assertEqual(res.data, b".x{}")

    def test_serves_file_when_root_is_symlinked(self):
        """Regression: on macOS `Settings.set_root_path("/tmp/...")` stores the
        un-resolved `/tmp/...` path, but `(root / filename).resolve()` follows
        `/tmp` -> `/private/tmp`. The `is_relative_to` check must compare both
        paths in resolved form, otherwise every register_static URL 404s."""
        link_dir = tempfile.mkdtemp()
        try:
            real_root = pathlib.Path(self.real_tmpdir)
            link_root = pathlib.Path(link_dir) / "linked_root"
            os.symlink(real_root, link_root)

            self._write("static", "app.js", content=b"var x=1;")
            Settings.set_root_path(str(link_root))

            token = _sign("static/app.js")
            res = self.client.get(f"/_page-home/static/app.js?token={token}")

            self.assertEqual(res.status_code, 200, res.data)
            self.assertEqual(res.data, b"var x=1;")
        finally:
            shutil.rmtree(link_dir, ignore_errors=True)

    def test_missing_token_returns_403(self):
        rel = self._write("a.css")
        res = self.client.get(f"/_page-home/{rel}")
        self.assertEqual(res.status_code, 403)

    def test_invalid_token_returns_403(self):
        rel = self._write("a.css")
        res = self.client.get(f"/_page-home/{rel}?token=not-a-jwt")
        self.assertEqual(res.status_code, 403)

    def test_expired_token_returns_403(self):
        rel = self._write("a.css")
        token = _sign(rel, exp_delta=datetime.timedelta(seconds=-1))
        res = self.client.get(f"/_page-home/{rel}?token={token}")
        self.assertEqual(res.status_code, 403)

    def test_asset_mismatch_returns_403(self):
        self._write("a.css", content=b"a")
        self._write("b.css", content=b"b")
        token = _sign("a.css")
        res = self.client.get(f"/_page-home/b.css?token={token}")
        self.assertEqual(res.status_code, 403)

    def test_missing_file_returns_404(self):
        token = _sign("missing.css")
        res = self.client.get(f"/_page-home/missing.css?token={token}")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
