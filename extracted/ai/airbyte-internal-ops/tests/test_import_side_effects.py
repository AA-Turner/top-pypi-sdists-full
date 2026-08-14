# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Tests for import-time side effects."""

from __future__ import annotations

import subprocess
import sys


def test_importing_cli_app_does_not_fetch_oss_catalog() -> None:
    """Importing the CLI does not make an outbound HTTP request."""
    script = """
import requests


def fail(*_args, **_kwargs):
    raise AssertionError("HTTP request attempted during import")


requests.get = fail
requests.sessions.Session.request = fail
import airbyte_ops_mcp.cli.app
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
