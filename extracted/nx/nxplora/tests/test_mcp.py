"""
tests/test_mcp.py - NX MCP framework tests.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import nx_mcp


class MCPTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        tmp_path = Path(self.tmpdir.name)
        self.patchers = [
            patch.object(nx_mcp, "NX_HOME", tmp_path),
            patch.object(nx_mcp, "MCP_CONFIG_PATH", tmp_path / "mcp_config.json"),
            patch.object(nx_mcp, "MCP_CREDENTIALS_PATH", tmp_path / "mcp_credentials.json"),
        ]
        for patcher in self.patchers:
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(self.tmpdir.cleanup)


class TestMCPRegistry(unittest.TestCase):
    def test_registry_covers_expected_worlds(self):
        worlds_covered = set()
        for mcp in nx_mcp.MCP_REGISTRY.values():
            worlds_covered.update(mcp["worlds"])
        expected = {
            "marketing",
            "growth",
            "brand",
            "sales",
            "customers",
            "finance",
            "code",
            "devops",
            "ops",
            "hr",
            "recruiting",
            "onboarding",
            "legal",
            "compliance",
            "cowork",
            "knowledge",
            "product",
            "research",
            "strategy",
            "leads",
        }
        self.assertTrue(expected.issubset(worlds_covered))

    def test_total_tools_exceeds_two_thousand(self):
        total = sum(m["tools_count"] for m in nx_mcp.MCP_REGISTRY.values())
        self.assertGreater(total, 2000)

    def test_all_registry_entries_have_required_fields(self):
        required = {"worlds", "description", "install", "auth", "tools_count", "env_key", "status"}
        for name, mcp in nx_mcp.MCP_REGISTRY.items():
            self.assertTrue(required.issubset(mcp), f"{name} missing required fields")

    def test_list_integrations_filters_by_world(self):
        marketing = nx_mcp.list_integrations("marketing")
        self.assertTrue(marketing)
        for integration in marketing:
            self.assertIn("marketing", integration["worlds"])


class TestMCPInstall(MCPTestCase):
    def test_install_unknown_mcp_returns_error(self):
        result = nx_mcp.install_mcp("nonexistent")
        self.assertFalse(result["success"])
        self.assertIn("Unknown MCP", result["error"])

    @patch("nx_mcp.is_cleared", return_value=False)
    def test_install_is_blocked_without_security_clearance(self, mock_is_cleared):
        result = nx_mcp.install_mcp("github")
        self.assertFalse(result["success"])
        self.assertIn("security audit", result["error"])
        self.assertEqual(result["action"], "Run: /audit github")
        mock_is_cleared.assert_called_once_with("github")

    @patch("nx_mcp.subprocess.run")
    def test_install_known_mcp_succeeds_with_skip_audit(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        result = nx_mcp.install_mcp("github", skip_audit=True)
        self.assertTrue(result["success"])
        self.assertIn(result["status"], {"installed_needs_auth", "installed"})

    @patch("nx_mcp.subprocess.run")
    def test_install_records_to_config(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        nx_mcp.install_mcp("docker", skip_audit=True)
        config = nx_mcp.load_mcp_config()
        self.assertIn("docker", config["installed"])

    @patch("nx_mcp.subprocess.run")
    def test_install_twice_returns_already_installed(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        nx_mcp.install_mcp("docker", skip_audit=True)
        result = nx_mcp.install_mcp("docker", skip_audit=True)
        self.assertEqual(result["status"], "already_installed")


class TestMCPAuth(MCPTestCase):
    def test_auth_unknown_mcp_returns_error(self):
        result = nx_mcp.auth_mcp("nonexistent", "token")
        self.assertFalse(result["success"])

    def test_auth_stores_credentials_and_marks_authenticated(self):
        nx_mcp.save_mcp_config(
            {"installed": {"github": {"auth_status": "pending", "worlds": ["code"], "tools_count": 50}}}
        )

        result = nx_mcp.auth_mcp("github", "ghp_test_123")

        self.assertTrue(result["success"])
        creds = nx_mcp.load_credentials()
        config = nx_mcp.load_mcp_config()
        self.assertEqual(creds["github"]["key"], "ghp_test_123")
        self.assertEqual(config["installed"]["github"]["auth_status"], "authenticated")

    def test_credentials_are_in_os_keyring_or_user_only_file(self):
        """Credentials must land in either the OS secret store, or — when
        no keyring backend is available — a 0600-permissioned file."""
        nx_mcp.auth_mcp("github", "ghp_test_123")
        if nx_mcp._get_keyring() is not None:
            # Real keyring backend — plaintext file must NOT exist.
            self.assertFalse(
                nx_mcp.MCP_CREDENTIALS_PATH.exists(),
                "MCP_CREDENTIALS_PATH should not be created when keyring is available",
            )
            creds = nx_mcp.load_credentials()
            self.assertIn("github", creds, "credential should be readable from keyring")
        else:
            mode = oct(nx_mcp.MCP_CREDENTIALS_PATH.stat().st_mode & 0o777)
            self.assertEqual(mode, "0o600")


class TestMCPToolDiscovery(MCPTestCase):
    def test_discover_not_installed_returns_error(self):
        result = nx_mcp.discover_tools("hubspot")
        self.assertFalse(result["success"])
        self.assertIn("not installed", result["error"])

    @patch("nx_mcp.subprocess.run")
    def test_discover_installed_returns_tool_info(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        nx_mcp.install_mcp("github", skip_audit=True)
        result = nx_mcp.discover_tools("github")
        self.assertTrue(result["success"])
        self.assertGreater(result["tools_count"], 0)
        self.assertIn("worlds", result)


class TestMCPExecute(MCPTestCase):
    def test_execute_not_installed_returns_error(self):
        result = nx_mcp.execute_mcp_tool("hubspot", "list_contacts", {}, test_mode=True)
        self.assertFalse(result["success"])
        self.assertIn("not installed", result["error"])

    @patch("nx_mcp.subprocess.run")
    def test_execute_test_mode_returns_401_as_pass_condition(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        nx_mcp.install_mcp("github", skip_audit=True)

        result = nx_mcp.execute_mcp_tool(
            mcp_name="github",
            tool_name="list_repos",
            params={"owner": "testuser"},
            test_mode=True,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["response"]["status"], 401)
        self.assertIn("PASS", result["response"]["test_result"])
        self.assertTrue(result["test_mode"])

    @patch("nx_mcp.subprocess.run")
    def test_full_flow_install_auth_discover_execute(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        install_result = nx_mcp.install_mcp("hubspot", skip_audit=True)
        self.assertTrue(install_result["success"])

        auth_result = nx_mcp.auth_mcp("hubspot", "TEST_HUBSPOT_KEY_12345")
        self.assertTrue(auth_result["success"])

        discover_result = nx_mcp.discover_tools("hubspot")
        self.assertTrue(discover_result["success"])
        self.assertEqual(discover_result["auth_status"], "authenticated")

        execute_result = nx_mcp.execute_mcp_tool(
            mcp_name="hubspot",
            tool_name="list_contacts",
            params={"limit": 10},
            test_mode=True,
        )
        self.assertTrue(execute_result["success"])
        self.assertEqual(execute_result["response"]["status"], 401)
        self.assertIn("PASS", execute_result["response"]["test_result"])


if __name__ == "__main__":
    unittest.main()
