import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl.cli.channel
import cpsl.cli.http
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


if __name__ == "__main__":
    unittest.main()
