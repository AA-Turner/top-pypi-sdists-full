"""SMS Email Delivery Tests — validates the email (IMAP→SMTP) delivery path.

Tests that the backend's `handle_inbound_email()` correctly intercepts commands
and that replies are routed back through the email channel.
"""

from __future__ import annotations

import os
import pytest
import httpx

BACKEND_URL = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
TEST_EMAIL = "test-email-delivery@sageworksai.com"


def _is_backend_reachable() -> bool:
    try:
        return httpx.get(f"{BACKEND_URL}/health", timeout=5).status_code == 200
    except Exception:
        return False


def _dispatch_email(text: str) -> httpx.Response:
    """Simulate an inbound email by hitting the dispatch endpoint."""
    payload = {
        "text": text,
        "from": TEST_EMAIL,
        "device_type": "email",
        "channel": "email",
    }
    return httpx.post(
        f"{BACKEND_URL}/sms/webhook",
        json=payload, timeout=600,
    )


pytestmark = pytest.mark.skipif(
    not _is_backend_reachable(),
    reason=f"Backend not reachable at {BACKEND_URL}",
)


class TestEmailDeliveryCommands:
    def test_help_via_email(self):
        r = _dispatch_email("@help")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert len(output) > 10

    def test_models_via_email(self):
        r = _dispatch_email("@models")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert "model" in output.lower() or "qwen" in output.lower()

    def test_status_via_email(self):
        r = _dispatch_email("@status")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert len(output) > 5

    def test_ask_via_email(self):
        r = _dispatch_email("@ask What is 2+2?")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert "4" in output or len(output) > 5

    def test_model_switch_via_email(self):
        r = _dispatch_email("@model cloud:gemma-4")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert "gemma" in output.lower() or "model" in output.lower()

    def test_temp_via_email(self):
        r = _dispatch_email("@temp 0.8")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert "0.8" in output or "temperature" in output.lower()

    def test_freeform_task_via_email(self):
        r = _dispatch_email("What is the speed of light?")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert len(output) > 10

    def test_cd_via_email(self):
        r = _dispatch_email("cd /tmp")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert "tmp" in output.lower() or "📁" in output

    def test_verbose_via_email(self):
        r = _dispatch_email("@verbose")
        assert r.status_code == 200

    def test_quiet_via_email(self):
        r = _dispatch_email("@quiet")
        assert r.status_code == 200

    def test_timeout_via_email(self):
        r = _dispatch_email("@timeout 60")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert "60" in output or "timeout" in output.lower()

    def test_run_task_via_email(self):
        r = _dispatch_email("@run print hello world")
        assert r.status_code == 200
        output = r.json().get("output", r.json().get("reply", ""))
        assert len(output) > 0
