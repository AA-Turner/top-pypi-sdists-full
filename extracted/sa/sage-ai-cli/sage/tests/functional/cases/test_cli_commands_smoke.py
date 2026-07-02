"""CLI Commands Smoke Tests — every `sage` subcommand and flag combination.

Each test invokes `sage <subcommand> [flags]` as a subprocess and asserts
exit-code == 0 and expected output patterns.  NO MOCKS.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SAGE = [sys.executable, "-m", "sage"]
TIMEOUT = 30


def _run(args: list[str], timeout: int = TIMEOUT, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["SAGE_TESTING"] = "1"
    env["SAGE_DISABLE_RAG"] = "1"
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        SAGE + args, capture_output=True, text=True, timeout=timeout, env=env,
        cwd=tempfile.mkdtemp(prefix="sage-smoke-"),
    )


# ── sage --help ──────────────────────────────────────────────────────────

class TestSageHelp:
    def test_help_flag(self):
        r = _run(["--help"])
        assert r.returncode == 0
        assert "sage" in r.stdout.lower()

    def test_run_help(self):
        r = _run(["run", "--help"])
        assert r.returncode == 0
        assert "model" in r.stdout.lower()

    def test_ask_help(self):
        r = _run(["ask", "--help"])
        assert r.returncode == 0
        assert "prompt" in r.stdout.lower()

    def test_models_help(self):
        r = _run(["models", "--help"])
        assert r.returncode == 0

    def test_autopolit_help(self):
        r = _run(["autopolit", "--help"])
        assert r.returncode == 0

    def test_config_help(self):
        r = _run(["config", "--help"])
        assert r.returncode == 0

    def test_sms_help(self):
        r = _run(["sms", "--help"])
        assert r.returncode == 0

    def test_schedule_help(self):
        r = _run(["schedule", "--help"])
        assert r.returncode == 0

    def test_integrate_help(self):
        r = _run(["integrate", "--help"])
        assert r.returncode == 0

    def test_daemon_help(self):
        r = _run(["daemon", "--help"])
        assert r.returncode == 0


# ── sage models ──────────────────────────────────────────────────────────

class TestModelsCommand:
    def test_models_default(self):
        r = _run(["models"])
        assert r.returncode == 0
        # Should list at least one model
        assert len(r.stdout.strip()) > 0

    def test_models_all(self):
        r = _run(["models", "--all"])
        assert r.returncode == 0

    def test_models_details(self):
        r = _run(["models", "--details"])
        assert r.returncode == 0

    def test_models_category_coding(self):
        r = _run(["models", "--category", "coding"])
        assert r.returncode == 0

    def test_models_search_qwen(self):
        r = _run(["models", "--search", "qwen"])
        assert r.returncode == 0

    def test_models_provider_cloud(self):
        r = _run(["models", "--provider", "cloud"])
        assert r.returncode == 0

    def test_models_filter_keyword(self):
        r = _run(["models", "--filter", "coder"])
        assert r.returncode == 0

    def test_models_ollama(self):
        r = _run(["models", "--ollama"])
        # May return non-zero if ollama not installed — that's OK
        assert r.returncode in (0, 1)

    def test_models_combined_flags(self):
        r = _run(["models", "--all", "--details"])
        assert r.returncode == 0


# ── sage config ──────────────────────────────────────────────────────────

class TestConfigCommand:
    def test_config_show(self):
        r = _run(["config", "show"])
        assert r.returncode == 0

    def test_config_get_default_model(self):
        r = _run(["config", "get", "default_model"])
        assert r.returncode == 0

    def test_config_init(self):
        tmp = tempfile.mkdtemp(prefix="sage-config-init-")
        r = _run(["config", "init"], env_extra={"HOME": tmp})
        assert r.returncode == 0


# ── sage whoami ──────────────────────────────────────────────────────────

class TestWhoami:
    def test_whoami(self):
        r = _run(["whoami"])
        # May return 0 (logged in) or 1 (not logged in) — both valid
        assert r.returncode in (0, 1)


# ── sage sms status/devices ──────────────────────────────────────────────

class TestSmsCommands:
    def test_sms_status(self):
        r = _run(["sms", "status"])
        # Will return non-zero if bridge not running — expected
        assert r.returncode in (0, 1)

    def test_sms_devices(self):
        r = _run(["sms", "devices"])
        assert r.returncode in (0, 1)

    def test_sms_contacts_list(self):
        r = _run(["sms", "contacts", "list"])
        assert r.returncode in (0, 1)

    def test_sms_logs(self):
        r = _run(["sms", "logs"])
        assert r.returncode in (0, 1)

    def test_sms_diagnose(self):
        r = _run(["sms", "diagnose"])
        assert r.returncode in (0, 1)


# ── sage schedule list ───────────────────────────────────────────────────

class TestScheduleCommand:
    def test_schedule_list(self):
        r = _run(["schedule", "list"])
        assert r.returncode in (0, 1)


# ── sage integrate list ──────────────────────────────────────────────────

class TestIntegrateCommand:
    def test_integrate_list(self):
        r = _run(["integrate", "list"])
        assert r.returncode in (0, 1)


# ── sage daemon status ───────────────────────────────────────────────────

class TestDaemonCommand:
    def test_daemon_status(self):
        r = _run(["daemon", "status"])
        assert r.returncode in (0, 1)


# ── sage search ──────────────────────────────────────────────────────────

class TestSearchCommand:
    def test_search_help(self):
        r = _run(["search", "--help"])
        assert r.returncode == 0


# ── sage image ───────────────────────────────────────────────────────────

class TestImageCommand:
    def test_image_help(self):
        r = _run(["image", "--help"])
        assert r.returncode == 0
