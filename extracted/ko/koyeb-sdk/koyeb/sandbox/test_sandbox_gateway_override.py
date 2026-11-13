"""KOYEB_SANDBOX_GATEWAY_URL replaces the gateway URL for exec/files."""

import unittest
from unittest import mock

from koyeb.sandbox.sandbox import Sandbox


class TestSandboxGatewayOverride(unittest.TestCase):
    def _sandbox(self):
        sandbox = Sandbox(
            sandbox_id="svc-1", app_id="app-1", service_id="svc-1", sandbox_secret="s"
        )
        sandbox._sandbox_url = ("https://sandboxes.example.com/koyeb-sandbox", "rk")
        return sandbox

    def test_unset_uses_url_from_api(self):
        with mock.patch.dict("os.environ", {"KOYEB_SANDBOX_GATEWAY_URL": ""}):
            conn = self._sandbox()._get_conn_info()
        self.assertEqual(conn.public_url, "https://sandboxes.example.com/koyeb-sandbox")
        self.assertEqual(conn.routing_key, "rk")

    def test_set_overrides_gateway(self):
        env = {"KOYEB_SANDBOX_GATEWAY_URL": "http://sandbox-gateway.ns.svc/"}
        with mock.patch.dict("os.environ", env):
            conn = self._sandbox()._get_conn_info()
        self.assertEqual(conn.public_url, "http://sandbox-gateway.ns.svc/koyeb-sandbox")
        self.assertEqual(conn.routing_key, "rk")
        self.assertEqual(conn.secret, "s")


if __name__ == "__main__":
    unittest.main()
