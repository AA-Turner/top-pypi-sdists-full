import os
import unittest
from acdh_handle_pyutils.client import HandleClient

HANDLE_USERNAME = os.environ.get("HANDLE_USERNAME")
HANDLE_PASSWORD = os.environ.get("HANDLE_PASSWORD")
HANDLE_TO_UPDATE = "https://hdl.handle.net/21.11115/0000-000F-743B-D"
URL_TO_REGISTER = "https://id.hansi4ever.com/123"
URL_TO_UPDATE = "https://sumsi.com/is-the-best"
cl = HandleClient(HANDLE_USERNAME, HANDLE_PASSWORD)
cl_one = HandleClient(HANDLE_USERNAME, HANDLE_PASSWORD, hdl_prefix="21.1234/")


class TestClient(unittest.TestCase):
    """Tests for `acdh_handle_pyutils.client` module."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001(self):
        self.assertTrue(cl.url.endswith("/"))
        self.assertTrue(cl_one.url.endswith("/"))

    def test_002_register_handle(self):
        result = cl.register_handle(URL_TO_REGISTER, full_url=False)
        self.assertTrue(cl.prefix in result)
        result = cl.register_handle(URL_TO_REGISTER, full_url=True)
        self.assertTrue(result.startswith("http"))

    def test_003_strip_resolver(self):
        dummies = [
            "https://hdl.handle.net/21.11115/0000-000F-743B-D",
            "21.11115/0000-000F-743B-D",
        ]
        for x in dummies:
            stripped = cl.strip_resolver(x)
            self.assertEqual(stripped, "21.11115/0000-000F-743B-D")

    def test_004_update(self):
        updated = cl.update_handle(HANDLE_TO_UPDATE, URL_TO_UPDATE)
        self.assertEqual(updated.status_code, 204)
