"""Test that aiwatch-enforce --version prints version and exits cleanly.

Subprocess invocation because the entrypoint calls sys.exit(0).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CLI_ROOT = Path(__file__).resolve().parents[1]


def test_enforce_version_flag():
    result = subprocess.run(
        [sys.executable, "-m", "runlayer_cli.hook", "--version"],
        cwd=CLI_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "aiwatch-enforce version" in result.stdout


def test_enforce_version_short_flag():
    result = subprocess.run(
        [sys.executable, "-m", "runlayer_cli.hook", "-v"],
        cwd=CLI_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "aiwatch-enforce version" in result.stdout
