import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl.cli.channel
import cpsl.cli.http
from cpsl.client import Client, _http_base as client_http_base
from cpsl.config import ConfigContext


class ChannelHttpBaseTests(unittest.TestCase):
    def test_serve_channel_api_uses_gateway_http_port_when_configured(self):
        ctx = ConfigContext(
            token="token",
            gateway_host="localhost",
            gateway_port=50051,
            gateway_http_port=8080,
        )

        with unittest.mock.patch("cpsl.cli.http.get_config_context", return_value=ctx):
            base, _ = cpsl.cli.http.api_base("/channels")

        self.assertEqual(base, "http://localhost:8080/api/v1/channels")

    def test_serve_channel_api_uses_next_port_for_local_grpc_gateway(self):
        ctx = ConfigContext(
            token="token",
            gateway_host="localhost",
            gateway_port=50051,
        )

        with unittest.mock.patch("cpsl.cli.http.get_config_context", return_value=ctx):
            base, _ = cpsl.cli.http.api_base("/channels")

        self.assertEqual(base, "http://localhost:50052/api/v1/channels")

    def test_serve_channel_api_uses_https_without_port_for_prod_gateway(self):
        ctx = ConfigContext(
            token="token",
            gateway_host="gateway.capsule.new",
            gateway_port=443,
        )

        with unittest.mock.patch("cpsl.cli.http.get_config_context", return_value=ctx):
            base, _ = cpsl.cli.http.api_base("/channels")

        self.assertEqual(base, "https://api.capsule.new/api/v1/channels")

    def test_channel_cli_uses_next_port_for_local_grpc_gateway(self):
        ctx = ConfigContext(
            token="token",
            gateway_host="localhost",
            gateway_port=50051,
        )

        with unittest.mock.patch("cpsl.cli.http.get_config_context", return_value=ctx):
            base, _ = cpsl.cli.channel._http_base()

        self.assertEqual(base, "http://localhost:50052/api/v1/channels")

    def test_channel_cli_uses_https_without_port_for_prod_gateway(self):
        ctx = ConfigContext(
            token="token",
            gateway_host="gateway.capsule.new",
            gateway_port=443,
        )

        with unittest.mock.patch("cpsl.cli.http.get_config_context", return_value=ctx):
            base, _ = cpsl.cli.channel._http_base()

        self.assertEqual(base, "https://api.capsule.new/api/v1/channels")

    def test_client_reset_onboarding_uses_current_app_user_endpoint(self):
        c = Client.__new__(Client)
        c._app_cache = {}
        c._resolve_app_id = lambda app: "app-1"
        calls = []
        c._api_delete = lambda path, body=None: calls.append((path, body)) or {"ok": True}

        out = c.reset_onboarding("demo")

        self.assertEqual(out, {"ok": True})
        self.assertEqual(calls, [("/app/app-1/onboarding/complete", {"reset": True})])

    def test_programmatic_client_maps_prod_gateway_to_http_api_host(self):
        ctx = ConfigContext(
            token="token",
            gateway_host="gateway.capsule.new",
            gateway_port=443,
        )

        self.assertEqual(client_http_base(ctx), "https://api.capsule.new")

    def test_programmatic_client_uses_next_port_for_local_grpc_gateway(self):
        ctx = ConfigContext(
            token="token",
            gateway_host="localhost",
            gateway_port=50051,
        )

        self.assertEqual(client_http_base(ctx), "http://localhost:50052")


if __name__ == "__main__":
    unittest.main()
