"""
tests/test_mcp_manager.py
Control-plane contracts validated June 14 2026.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import nx_mcp_manager


class TestControlPlaneHealth(unittest.TestCase):
    @patch("nx_mcp_manager.httpx.get")
    def test_start_user_hub_checks_control_plane_health(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"status": "ok", "hub_alive": True, "hub_port": 37373},
        )

        result = nx_mcp_manager.start_user_hub("user_test")

        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["user_id"], "user_test")
        self.assertTrue(result["hub_alive"])
        self.assertEqual(
            mock_get.call_args[0][0],
            f"{nx_mcp_manager.NX_CONTROL_PLANE}/health",
        )

    @patch("nx_mcp_manager.httpx.get", side_effect=Exception("connection refused"))
    def test_start_user_hub_handles_unavailable_control_plane(self, _mock_get):
        result = nx_mcp_manager.start_user_hub("user_test")

        self.assertEqual(result["status"], "unavailable")
        self.assertIn("connection refused", result["error"])


class TestRemoteConnect(unittest.TestCase):
    @patch("nx_mcp_manager.httpx.post")
    def test_add_server_for_user_posts_expected_payload(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "success": True,
                "server": "github",
                "status": "connected",
                "tools_count": 2,
                "key": "user_test__github",
            },
        )

        result = nx_mcp_manager.add_server_for_user(
            user_id="user_test",
            server_name="github",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_test"},
        )

        self.assertTrue(result["success"])
        self.assertEqual(
            mock_post.call_args[0][0],
            f"{nx_mcp_manager.NX_CONTROL_PLANE}/api/connect",
        )
        self.assertEqual(
            mock_post.call_args.kwargs["json"],
            {
                "user_id": "user_test",
                "server_name": "github",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_test"},
            },
        )
        self.assertEqual(mock_post.call_args.kwargs["timeout"], 60)

    @patch("nx_mcp_manager.httpx.post", side_effect=Exception("timeout"))
    def test_add_server_for_user_handles_transport_failure(self, _mock_post):
        result = nx_mcp_manager.add_server_for_user(
            user_id="user_test",
            server_name="github",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
        )

        self.assertFalse(result["success"])
        self.assertIn("timeout", result["error"])


class TestUserTools(unittest.TestCase):
    @patch("nx_mcp_manager.httpx.get")
    def test_get_user_tools_reads_user_scoped_endpoint(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "tools": [
                    {
                        "name": "create_or_update_file",
                        "description": "Create or update a file",
                        "server": "github",
                        "user_id": "user_test",
                    },
                    {
                        "name": "search_repositories",
                        "description": "Search repos",
                        "server": "github",
                        "user_id": "user_test",
                    },
                ],
                "count": 2,
            },
        )

        tools = nx_mcp_manager.get_user_tools("user_test")

        self.assertEqual(len(tools), 2)
        self.assertEqual(tools[0]["server"], "github")
        self.assertEqual(tools[0]["user_id"], "user_test")
        self.assertEqual(
            mock_get.call_args[0][0],
            f"{nx_mcp_manager.NX_CONTROL_PLANE}/api/user/user_test/tools",
        )

    @patch("nx_mcp_manager.httpx.get")
    def test_get_user_tools_returns_empty_on_non_200(self, mock_get):
        mock_get.return_value = MagicMock(status_code=503)

        self.assertEqual(nx_mcp_manager.get_user_tools("user_test"), [])

    @patch("nx_mcp_manager.httpx.get")
    def test_get_user_servers_reads_user_scoped_endpoint(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "servers": [
                    {
                        "name": "github",
                        "status": "connected",
                        "tools_count": 2,
                        "error": None,
                    }
                ],
                "count": 1,
            },
        )

        servers = nx_mcp_manager.get_user_servers("user_test")

        self.assertEqual(len(servers), 1)
        self.assertEqual(servers[0]["name"], "github")
        self.assertEqual(
            mock_get.call_args[0][0],
            f"{nx_mcp_manager.NX_CONTROL_PLANE}/api/user/user_test/servers",
        )


class TestMarketplaceSearch(unittest.TestCase):
    @patch("nx_mcp_manager.httpx.get")
    def test_search_uses_validated_registry_shape(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "version": "1.0",
                "totalServers": 37,
                "servers": [
                    {
                        "id": "github",
                        "name": "GitHub",
                        "description": "GitHub repos and issues",
                        "category": "development",
                        "tags": ["git", "repos"],
                        "installations": 1000,
                        "verified": True,
                        "stars": 500,
                    }
                ],
            },
        )

        results = nx_mcp_manager.search_marketplace("github")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "github")
        self.assertTrue(results[0]["verified"])

    @patch("nx_mcp_manager.httpx.get")
    def test_search_matches_tags(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "servers": [
                    {
                        "id": "gh",
                        "name": "GitHub",
                        "description": "",
                        "tags": ["version-control", "repos"],
                        "verified": True,
                        "stars": 100,
                        "installations": 500,
                    }
                ]
            },
        )

        results = nx_mcp_manager.search_marketplace("version-control")

        self.assertEqual(len(results), 1)

    @patch("nx_mcp_manager.httpx.get", side_effect=Exception("network error"))
    def test_search_handles_network_failure(self, _mock_get):
        self.assertEqual(nx_mcp_manager.search_marketplace("anything"), [])
