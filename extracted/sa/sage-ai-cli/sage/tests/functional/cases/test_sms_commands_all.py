"""SMS Bridge Command Tests — every @command via the webhook endpoint.

Sends each command through the `/sms/webhook` HTTP endpoint and validates
the JSON response.  NO MOCKS — hits the real backend.
"""

from __future__ import annotations

import os
import json
import time
import uuid
import tempfile
import subprocess
import sys
from pathlib import Path

import pytest
import httpx

BACKEND_URL = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
TEST_EMAIL = "test-functional@sageworksai.com"
TIMEOUT = 600
MODEL = "cloud:qwen3-coder"


def _is_backend_reachable() -> bool:
    try:
        r = httpx.get(f"{BACKEND_URL}/health", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def _webhook(text: str, device_type: str = "apple") -> httpx.Response:
    """Post a message to the SMS webhook and return the response."""
    payload = {
        "text": text,
        "from": TEST_EMAIL,
        "device_type": device_type,
    }
    return httpx.post(
        f"{BACKEND_URL}/sms/webhook",
        json=payload,
        timeout=TIMEOUT,
    )


pytestmark = pytest.mark.skipif(
    not _is_backend_reachable(),
    reason=f"Backend not reachable at {BACKEND_URL}",
)


# ── Help commands ────────────────────────────────────────────────────────

class TestSMSHelpCommands:
    def test_help(self):
        r = _webhook("help")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "help" in output.lower() or "command" in output.lower() or "sage" in output.lower()

    def test_question_mark(self):
        r = _webhook("?")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert len(output) > 10

    def test_at_help(self):
        r = _webhook("@help")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert len(output) > 10


# ── Model commands ───────────────────────────────────────────────────────

class TestSMSModelCommands:
    def test_at_models(self):
        r = _webhook("@models")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "model" in output.lower() or "qwen" in output.lower()

    def test_at_list(self):
        r = _webhook("@list")
        assert r.status_code == 200

    def test_at_list_models(self):
        r = _webhook("@list-models")
        assert r.status_code == 200

    def test_models_plain(self):
        r = _webhook("models")
        assert r.status_code == 200

    def test_at_model_show(self):
        r = _webhook("@model")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "model" in output.lower()

    def test_at_current_model(self):
        r = _webhook("@current-model")
        assert r.status_code == 200

    def test_at_model_switch(self):
        r = _webhook("@model cloud:llama-3-2")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "llama" in output.lower() or "model" in output.lower()


# ── Status commands ──────────────────────────────────────────────────────

class TestSMSStatusCommands:
    def test_at_status(self):
        r = _webhook("@status")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "✅" in output or "status" in output.lower() or "model" in output.lower()

    def test_status_plain(self):
        r = _webhook("status")
        assert r.status_code == 200

    def test_at_dir(self):
        r = _webhook("@dir")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "📁" in output or "/" in output

    def test_at_pwd(self):
        r = _webhook("@pwd")
        assert r.status_code == 200

    def test_pwd_plain(self):
        r = _webhook("pwd")
        assert r.status_code == 200


# ── Configuration commands ───────────────────────────────────────────────

class TestSMSConfigCommands:
    def test_at_temp(self):
        r = _webhook("@temp 0.5")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "0.5" in output or "temperature" in output.lower()

    def test_at_timeout(self):
        r = _webhook("@timeout 120")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "120" in output or "timeout" in output.lower()

    def test_at_verbose(self):
        r = _webhook("@verbose")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "verbose" in output.lower() or "📢" in output

    def test_at_quiet(self):
        r = _webhook("@quiet")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "quiet" in output.lower() or "🔇" in output


# ── Task execution commands ──────────────────────────────────────────────

class TestSMSTaskCommands:
    def test_at_ask(self):
        r = _webhook("@ask What is 2+2?")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert "4" in output or len(output) > 5

    def test_at_run(self):
        r = _webhook("@run Write a python hello world to hello.py and stop")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert len(output) > 5

    def test_freeform_task(self):
        """A message without @ prefix should be treated as a full task."""
        r = _webhook("What is the capital of France?")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        assert len(output) > 5


# ── Device type routing ──────────────────────────────────────────────────

class TestSMSDeviceRouting:
    def test_apple_device(self):
        r = _webhook("@status", device_type="apple")
        assert r.status_code == 200

    def test_android_device(self):
        r = _webhook("@status", device_type="android")
        assert r.status_code == 200

    def test_unknown_device(self):
        r = _webhook("@status", device_type="")
        assert r.status_code == 200
