#!/usr/bin/env python3
"""
Test request_file_adapters.
"""

import contextlib
import datetime
import pathlib
import socket
import tempfile
import unittest

from requests_file_adapter import get_session

RFC_9110_FMT = "%a, %d %b %Y %H:%M:%S GMT"


@contextlib.contextmanager
def tmp_file():
    """
    Create a temporary file in a temporary directory.

    Returns:
        A 3-tuple with the file content, the file modification time and the
        path.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = pathlib.Path(tmp_dir) / "tmp.txt"
        text = "placeholder text"
        tmp_path.write_text(text)
        mtime = datetime.datetime.fromtimestamp(
            tmp_path.stat().st_mtime, datetime.timezone.utc
        )
        yield text, mtime, tmp_path


class TestText(unittest.TestCase):
    """
    Test text loading.
    """

    def setUp(self):
        self._session = get_session()

    def test_file_content(self):
        """
        Retrieve file content.
        """
        with tmp_file() as (text, _, path):
            resp = self._session.get(path.as_uri())
            self.assertEqual(text, resp.content.decode())

    def test_head_request(self):
        """
        HEAD request sends no content.
        """
        with tmp_file() as (text, _, path):
            resp = self._session.head(path.as_uri())
            self.assertIsNone(resp.content)

    def test_headers(self):
        """
        Expected headers are set.
        """
        with tmp_file() as (content, mtime, path):
            for method in ("HEAD", "GET"):
                with self.subTest(method=method):
                    resp = getattr(self._session, method.lower())(path.as_uri())
                    headers = resp.headers
                    self.assertEqual(
                        headers["Content-Length"], len(content.encode("utf-8"))
                    )
                    self.assertEqual(
                        headers["Last-Modified"], mtime.strftime(RFC_9110_FMT)
                    )
                    self.assertEqual(headers["Content-Type"], "text/plain")

    def test_ok(self):
        """
        Successful response returns a 200 OK code.
        """
        with tmp_file() as (_, _, path):
            for method in ("HEAD", "GET"):
                with self.subTest(method=method):
                    resp = getattr(self._session, method.lower())(path.as_uri())
                    self.assertEqual(resp.status_code, 200)

    def test_missing(self):
        """
        Missing file returns a 404 Not Found error.
        """
        with tmp_file() as (_, _, path):
            path = path.parent / "missing.txt"
            for method in ("HEAD", "GET"):
                with self.subTest(method=method):
                    resp = getattr(self._session, method.lower())(path.as_uri())
                    self.assertEqual(resp.status_code, 404)

    def test_no_perm(self):
        """
        Permission error returns a 403 Forbidden error.
        """
        with tmp_file() as (_, _, path):
            path.chmod(0o000)
            for method in ("HEAD", "GET"):
                with self.subTest(method=method):
                    resp = getattr(self._session, method.lower())(path.as_uri())
                    self.assertEqual(resp.status_code, 403)

    def test_localhost(self):
        """
        Localhost is recognized.
        """
        hostname = socket.gethostname()
        with tmp_file() as (text, _, path):
            for host in (
                "localhost",
                "localhost.localdomain",
                "127.0.0.1",
                hostname,
                socket.gethostbyname(hostname),
            ):
                uri = f"file://{host}{path}"
                with self.subTest(host=host):
                    resp = self._session.get(uri)
                    self.assertEqual(text, resp.content.decode())

    def test_other_host(self):
        """
        Other hosts raise ValueErrors.
        """
        hostname = socket.gethostname() * 2
        with tmp_file() as (text, _, path):
            uri = f"file://{hostname}{path}"
            with self.assertRaises(ValueError):
                self._session.get(uri)

    def test_other_methods(self):
        """
        Unsupported HTTP methods raise ValueErrors.
        """
        with tmp_file() as (_, _, path):
            for method in ("POST", "PUT"):
                with self.subTest(method=method), self.assertRaises(ValueError):
                    getattr(self._session, method.lower())(path.as_uri())

    def test_rel_paths(self):
        """
        Relative paths raise value errors.
        """
        uri = "file://foo.txt"
        with self.assertRaises(ValueError):
            self._session.get(uri)


if __name__ == "__main__":
    unittest.main()
