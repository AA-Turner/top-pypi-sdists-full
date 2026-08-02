import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import nx_mcp_hub


class TestRealAPIContracts(unittest.TestCase):
    """Tests based on validated real API responses."""

    @patch("httpx.get")
    def test_health_uses_api_servers_not_health_endpoint(self, mock_get):
        """Real contract: /api/servers returns 200, /health returns 404."""
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "servers": [
                    {
                        "name": "github",
                        "status": "connected",
                        "capabilities": {"tools": [{"name": "search_repositories"}]},
                        "serverInfo": {"name": "github-mcp-server", "version": "0.6.2"},
                    }
                ],
                "timestamp": "2026-06-14T18:39:30.696Z",
            },
        )
        status = nx_mcp_hub.hub_health()
        self.assertTrue(status["running"])
        self.assertEqual(status["connected"], 1)
        call_url = mock_get.call_args[0][0]
        self.assertIn("/api/servers", call_url)
        self.assertNotIn("/health", call_url)

    @patch("httpx.get")
    def test_tool_discovery_reads_capabilities_tools(self, mock_get):
        """Real contract: tools live at servers[].capabilities.tools[]"""
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "servers": [
                    {
                        "name": "github",
                        "status": "connected",
                        "capabilities": {
                            "tools": [
                                {
                                    "name": "create_or_update_file",
                                    "description": "Create or update a single file",
                                    "inputSchema": {},
                                },
                                {
                                    "name": "search_repositories",
                                    "description": "Search for GitHub repositories",
                                    "inputSchema": {},
                                },
                            ]
                        },
                        "serverInfo": {"name": "github-mcp-server", "version": "0.6.2"},
                    }
                ]
            },
        )
        tools = nx_mcp_hub.hub_list_tools()
        self.assertEqual(len(tools), 2)
        names = [tool["name"] for tool in tools]
        self.assertIn("create_or_update_file", names)
        self.assertIn("search_repositories", names)
        self.assertEqual(tools[0]["server"], "github")

    @patch("httpx.get")
    def test_tool_discovery_filters_by_server(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "servers": [
                    {
                        "name": "github",
                        "status": "connected",
                        "capabilities": {"tools": [{"name": "search_repos"}]},
                        "serverInfo": {},
                    },
                    {
                        "name": "stripe",
                        "status": "connected",
                        "capabilities": {"tools": [{"name": "list_customers"}]},
                        "serverInfo": {},
                    },
                ]
            },
        )
        tools = nx_mcp_hub.hub_list_tools(server_name="github")
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0]["name"], "search_repos")

    @patch("httpx.get")
    def test_disconnected_servers_excluded_from_tools(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "servers": [
                    {
                        "name": "github",
                        "status": "disconnected",
                        "capabilities": {"tools": [{"name": "search_repos"}]},
                        "serverInfo": {},
                    }
                ]
            },
        )
        tools = nx_mcp_hub.hub_list_tools()
        self.assertEqual(len(tools), 0)

    def test_hub_add_server_writes_correct_config_shape(self):
        """Real config shape validated from mcp-hub boot output."""
        tmpdir = Path(tempfile.mkdtemp())
        with patch.object(nx_mcp_hub, "NX_HUB_CONFIG", tmpdir / "config.json"):
            result = nx_mcp_hub.hub_add_server(
                name="github",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-github"],
                env={"GITHUB_PERSONAL_ACCESS_TOKEN": "test"},
            )
            self.assertTrue(result["success"])
            config = json.loads((tmpdir / "config.json").read_text())
            self.assertIn("mcpServers", config)
            self.assertIn("github", config["mcpServers"])
            server = config["mcpServers"]["github"]
            self.assertEqual(server["command"], "npx")
            self.assertIn("-y", server["args"])
            self.assertIn("GITHUB_PERSONAL_ACCESS_TOKEN", server["env"])

    @patch("httpx.get")
    def test_hub_not_running_returns_false(self, mock_get):
        mock_get.side_effect = Exception("connection refused")
        status = nx_mcp_hub.hub_health()
        self.assertFalse(status["running"])

    @patch("httpx.get")
    def test_registry_search(self, mock_get):
        """Registry is ravitemer.github.io not TensorBlock."""
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: [
                {"name": "github", "description": "GitHub repos and issues"},
                {"name": "stripe", "description": "Payments and billing"},
            ]
        )
        nx_mcp_hub._registry_cache = []
        results = nx_mcp_hub.search_registry("github")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "github")
        call_url = mock_get.call_args[0][0]
        self.assertIn("ravitemer", call_url)


class TestHubStatusIntegration(unittest.TestCase):
    @patch("httpx.get")
    def test_status_includes_tool_counts(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "servers": [
                    {
                        "name": "github",
                        "status": "connected",
                        "capabilities": {
                            "tools": [
                                {"name": "tool1"},
                                {"name": "tool2"},
                                {"name": "tool3"},
                            ]
                        },
                        "serverInfo": {"version": "0.6.2"},
                    }
                ],
                "timestamp": "2026-06-14T00:00:00Z",
            },
        )
        status = nx_mcp_hub.hub_status()
        self.assertTrue(status["running"])
        self.assertEqual(status["tools_total"], 3)
        self.assertEqual(status["tools_by_server"]["github"], 3)


if __name__ == "__main__":
    unittest.main()
