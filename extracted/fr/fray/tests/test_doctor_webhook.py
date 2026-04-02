#!/usr/bin/env python3
"""
Tests for fray doctor and fray webhook modules.
"""

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure fray package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from fray.doctor import FrayDoctor, PASS, WARN, FAIL, FIXED, run_doctor
from fray.webhook import detect_platform, send_webhook, _build_slack_payload, _build_discord_payload, _build_teams_payload, _build_generic_payload


# ── Doctor Tests ─────────────────────────────────────────────────────────────

class TestDoctorChecks(unittest.TestCase):
    """Test individual doctor checks."""

    def setUp(self):
        self.doctor = FrayDoctor(auto_fix=False, verbose=False)

    def test_python_version_pass(self):
        self.doctor.check_python_version()
        self.assertEqual(len(self.doctor.checks), 1)
        self.assertEqual(self.doctor.checks[0]["status"], PASS)
        self.assertIn("Python version", self.doctor.checks[0]["name"])

    def test_package_integrity(self):
        self.doctor.check_package_integrity()
        self.assertEqual(self.doctor.checks[0]["status"], PASS)

    def test_payloads_directory(self):
        self.doctor.check_payloads_directory()
        # Should have at least 2 checks (categories + json validity)
        self.assertGreaterEqual(len(self.doctor.checks), 2)
        # Categories should pass since we have the directory
        cat_check = self.doctor.checks[0]
        self.assertIn("categories", cat_check["name"].lower())

    def test_network_connectivity(self):
        self.doctor.check_network_connectivity()
        self.assertEqual(len(self.doctor.checks), 1)
        # May pass or fail depending on network — just verify it ran
        self.assertIn(self.doctor.checks[0]["status"], [PASS, FAIL])

    def test_ssl_tls(self):
        self.doctor.check_ssl_tls()
        self.assertEqual(self.doctor.checks[0]["status"], PASS)

    def test_file_permissions(self):
        self.doctor.check_file_permissions()
        self.assertEqual(self.doctor.checks[0]["status"], PASS)

    def test_encoding(self):
        self.doctor.check_encoding()
        self.assertEqual(len(self.doctor.checks), 1)
        self.assertIn(self.doctor.checks[0]["status"], [PASS, WARN])

    def test_disk_space(self):
        self.doctor.check_disk_space()
        self.assertEqual(len(self.doctor.checks), 1)
        self.assertEqual(self.doctor.checks[0]["status"], PASS)

    def test_mcp_server(self):
        self.doctor.check_mcp_server()
        self.assertEqual(len(self.doctor.checks), 1)
        # Either pass (installed) or warn (not installed) — both are valid
        self.assertIn(self.doctor.checks[0]["status"], [PASS, WARN])


class TestDoctorRunAll(unittest.TestCase):
    """Test full doctor run."""

    def test_run_all_returns_checks(self):
        doctor = FrayDoctor(auto_fix=False, verbose=False)
        checks = doctor.run_all()
        self.assertIsInstance(checks, list)
        self.assertGreaterEqual(len(checks), 8)  # At least 8 checks

    def test_run_all_check_structure(self):
        doctor = FrayDoctor(auto_fix=False, verbose=False)
        checks = doctor.run_all()
        for check in checks:
            self.assertIn("name", check)
            self.assertIn("status", check)
            self.assertIn(check["status"], [PASS, WARN, FAIL, FIXED])

    def test_print_report_no_crash(self):
        """Ensure print_report doesn't crash."""
        doctor = FrayDoctor(auto_fix=False, verbose=True)
        doctor.run_all()
        # Should not raise
        doctor.print_report()

    def test_run_doctor_entry_point(self):
        """Test the run_doctor() convenience function."""
        checks = run_doctor(auto_fix=False, verbose=False)
        self.assertIsInstance(checks, list)
        self.assertGreaterEqual(len(checks), 8)


class TestDoctorAutoFix(unittest.TestCase):
    """Test auto-fix mode."""

    def test_auto_fix_creates_missing_dirs(self):
        """Test that --fix creates missing payload category dirs (if any are missing)."""
        doctor = FrayDoctor(auto_fix=True, verbose=False)
        doctor.check_payloads_directory()
        # All statuses should be PASS or FIXED (not FAIL)
        for check in doctor.checks:
            self.assertIn(check["status"], [PASS, FIXED, WARN])


# ── Webhook Tests ────────────────────────────────────────────────────────────

class TestWebhookPlatformDetection(unittest.TestCase):
    """Test webhook platform auto-detection."""

    def test_detect_slack(self):
        self.assertEqual(detect_platform("https://hooks.slack.com/services/T0/B0/xxx"), "slack")

    def test_detect_discord(self):
        self.assertEqual(detect_platform("https://discord.com/api/webhooks/123/abc"), "discord")

    def test_detect_discord_old(self):
        self.assertEqual(detect_platform("https://discordapp.com/api/webhooks/123/abc"), "discord")

    def test_detect_teams(self):
        self.assertEqual(detect_platform("https://outlook.office.com/webhook/xxx"), "teams")

    def test_detect_teams_alt(self):
        self.assertEqual(detect_platform("https://xxx.webhook.office.com/xxx"), "teams")

    def test_detect_generic(self):
        self.assertEqual(detect_platform("https://example.com/webhook"), "generic")


SAMPLE_REPORT = {
    "target": "https://example.com",
    "duration": "45s",
    "summary": {
        "total": 100,
        "blocked": 95,
        "passed": 5,
        "block_rate": "95.0%",
    }
}

SAMPLE_REPORT_ALL_BLOCKED = {
    "target": "https://secure.example.com",
    "duration": "2m 30s",
    "summary": {
        "total": 200,
        "blocked": 200,
        "passed": 0,
        "block_rate": "100.0%",
    }
}


class TestWebhookPayloadBuilders(unittest.TestCase):
    """Test webhook message payload builders."""

    def test_slack_payload_structure(self):
        payload = _build_slack_payload(SAMPLE_REPORT)
        self.assertIn("blocks", payload)
        self.assertIsInstance(payload["blocks"], list)
        self.assertGreaterEqual(len(payload["blocks"]), 2)
        # Header block
        self.assertEqual(payload["blocks"][0]["type"], "header")

    def test_slack_payload_contains_target(self):
        payload = _build_slack_payload(SAMPLE_REPORT)
        payload_str = json.dumps(payload)
        self.assertIn("example.com", payload_str)

    def test_discord_payload_structure(self):
        payload = _build_discord_payload(SAMPLE_REPORT)
        self.assertIn("embeds", payload)
        self.assertEqual(len(payload["embeds"]), 1)
        embed = payload["embeds"][0]
        self.assertIn("fields", embed)
        self.assertIn("title", embed)
        self.assertIn("color", embed)

    def test_discord_color_green_when_all_blocked(self):
        payload = _build_discord_payload(SAMPLE_REPORT_ALL_BLOCKED)
        self.assertEqual(payload["embeds"][0]["color"], 0x22C55E)

    def test_discord_color_red_when_many_bypassed(self):
        report = {
            "target": "https://weak.com",
            "duration": "10s",
            "summary": {"total": 100, "blocked": 50, "passed": 50, "block_rate": "50.0%"}
        }
        payload = _build_discord_payload(report)
        self.assertEqual(payload["embeds"][0]["color"], 0xEF4444)

    def test_teams_payload_structure(self):
        payload = _build_teams_payload(SAMPLE_REPORT)
        self.assertEqual(payload["@type"], "MessageCard")
        self.assertIn("sections", payload)
        self.assertIn("facts", payload["sections"][0])

    def test_teams_theme_color_green_when_all_blocked(self):
        payload = _build_teams_payload(SAMPLE_REPORT_ALL_BLOCKED)
        self.assertEqual(payload["themeColor"], "22C55E")

    def test_generic_payload_structure(self):
        payload = _build_generic_payload(SAMPLE_REPORT)
        self.assertIn("text", payload)
        self.assertIn("example.com", payload["text"])
        self.assertIn("95", payload["text"])

    def test_empty_report_doesnt_crash(self):
        empty = {"target": "", "duration": "", "summary": {}}
        # None of these should raise
        _build_slack_payload(empty)
        _build_discord_payload(empty)
        _build_teams_payload(empty)
        _build_generic_payload(empty)


class TestWebhookSend(unittest.TestCase):
    """Test send_webhook with mocked HTTP."""

    @patch("fray.webhook.http.client.HTTPSConnection")
    def test_send_slack_success(self, mock_conn_cls):
        mock_conn = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b"ok"
        mock_conn.getresponse.return_value = mock_resp
        mock_conn_cls.return_value = mock_conn

        result = send_webhook("https://hooks.slack.com/services/T0/B0/xxx", SAMPLE_REPORT)
        self.assertTrue(result)

        # Verify POST was called
        mock_conn.request.assert_called_once()
        call_args = mock_conn.request.call_args
        self.assertEqual(call_args[0][0], "POST")

        # Verify body is valid JSON with Slack blocks
        body = json.loads(call_args[1]["body"])
        self.assertIn("blocks", body)

    @patch("fray.webhook.http.client.HTTPSConnection")
    def test_send_discord_success(self, mock_conn_cls):
        mock_conn = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 204
        mock_resp.read.return_value = b""
        mock_conn.getresponse.return_value = mock_resp
        mock_conn_cls.return_value = mock_conn

        result = send_webhook("https://discord.com/api/webhooks/123/abc", SAMPLE_REPORT)
        self.assertTrue(result)

    @patch("fray.webhook.http.client.HTTPSConnection")
    def test_send_failure_returns_false(self, mock_conn_cls):
        mock_conn = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 500
        mock_resp.read.return_value = b"Internal Server Error"
        mock_conn.getresponse.return_value = mock_resp
        mock_conn_cls.return_value = mock_conn

        result = send_webhook("https://hooks.slack.com/services/T0/B0/xxx", SAMPLE_REPORT)
        self.assertFalse(result)

    @patch("fray.webhook.http.client.HTTPSConnection")
    def test_send_connection_error_returns_false(self, mock_conn_cls):
        mock_conn_cls.side_effect = ConnectionRefusedError("Connection refused")

        result = send_webhook("https://hooks.slack.com/services/T0/B0/xxx", SAMPLE_REPORT)
        self.assertFalse(result)


# ── CLI Integration Tests ────────────────────────────────────────────────────

class TestCLIIntegration(unittest.TestCase):
    """Test CLI wiring for doctor and webhook."""

    def test_doctor_subcommand_exists(self):
        from fray.cli import main
        import argparse
        # Just verify parsing works — don't actually run
        with patch("sys.argv", ["fray", "doctor", "--help"]):
            with self.assertRaises(SystemExit) as ctx:
                main()
            self.assertEqual(ctx.exception.code, 0)

    def test_test_webhook_arg_exists(self):
        from fray.cli import main
        with patch("sys.argv", ["fray", "test", "--help"]):
            with self.assertRaises(SystemExit) as ctx:
                main()
            self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
