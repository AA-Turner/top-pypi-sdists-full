import os
import sys
import unittest
from unittest.mock import Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl.cli.fs
from cpsl.cli.fs import ls
from cpsl.clients.capsule import ListFilesystemsResponse
from cpsl.config import ConfigContext


class FilesystemCliTests(unittest.TestCase):
    def test_ls_without_name_lists_filesystems(self):
        client = Mock()
        client.filesystems.list_filesystems.return_value = ListFilesystemsResponse(
            ok=True,
            filesystems=[],
        )

        ls.callback.__wrapped__(client, None, "/")

        client.filesystems.list_filesystems.assert_called_once()

    def test_http_base_uses_gateway_http_port_when_configured(self):
        ctx = ConfigContext(
            token="token",
            gateway_host="localhost",
            gateway_port=50051,
            gateway_http_port=8080,
        )

        with unittest.mock.patch("cpsl.cli.fs.get_config_context", return_value=ctx):
            base, _ = cpsl.cli.fs._http_base()

        self.assertEqual(base, "http://localhost:8080/api/v1/fs")

    def test_http_base_uses_next_port_for_local_grpc_gateway(self):
        ctx = ConfigContext(
            token="token",
            gateway_host="localhost",
            gateway_port=50051,
        )

        with unittest.mock.patch("cpsl.cli.fs.get_config_context", return_value=ctx):
            base, _ = cpsl.cli.fs._http_base()

        self.assertEqual(base, "http://localhost:50052/api/v1/fs")


if __name__ == "__main__":
    unittest.main()
