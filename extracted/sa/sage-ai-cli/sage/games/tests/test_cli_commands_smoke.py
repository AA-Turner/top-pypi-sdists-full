"""Sage CLI command-surface smoke test.

For every top-level command the CLI exposes, verify `--help` loads
without throwing. This catches:

  * import errors in optional sub-modules (e.g. a missing `httpx` would
    crash `sage search --help` before the user even sees the flag list),
  * Click/Typer schema errors (`--flag` declarations that don't compile),
  * help-text rendering failures.

We use `subprocess.run` with `python -m sage <cmd> --help` rather than
calling the Typer app in-process so we exercise the real import graph
the way a user would on the command line.
"""

from __future__ import annotations

import subprocess
import sys

import pytest


# Top-level commands sage advertises in `python -m sage --help`. New
# commands added to main.py should appear here so they're smoke-tested.
_COMMANDS: list[str] = [
    "search", "image", "run", "ask", "models",
    "install", "update", "sync", "sync-catalog", "pull",
    "train-all", "train", "use", "rm",
    "login", "logout", "whoami", "fix-llama-cpp",
    "schedule", "integrate", "daemon", "config", "secrets",
    "sms", "ext", "rag", "corpus",
]


@pytest.mark.parametrize("cmd", _COMMANDS)
def test_cli_command_help_loads_without_error(cmd):
    """Every advertised command must accept `--help` and exit cleanly.

    Typer/Click return rc=0 for --help. Anything else (import errors,
    missing deps, schema bugs) shows up as a non-zero exit + stderr.
    """
    res = subprocess.run(
        [sys.executable, "-m", "sage", cmd, "--help"],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        timeout=60,
    )
    assert res.returncode == 0, (
        f"`sage {cmd} --help` exited with {res.returncode}\n"
        f"stderr tail: {(res.stderr or '')[-800:]}"
    )
    # Help output must mention the command name OR show usage/options
    # — empty help would mean the command is broken.
    text = (res.stdout or "") + (res.stderr or "")
    assert "Usage" in text or "Options" in text or "Commands" in text, (
        f"`sage {cmd} --help` printed no usage block\n"
        f"stdout tail: {(res.stdout or '')[-400:]}"
    )


def test_top_level_help_lists_every_command():
    """`sage --help` must list every command we registered, otherwise
    new commands are unreachable to users who haven't read the source."""
    res = subprocess.run(
        [sys.executable, "-m", "sage", "--help"],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        timeout=30,
    )
    assert res.returncode == 0
    text = (res.stdout or "") + (res.stderr or "")
    missing = [c for c in _COMMANDS if c not in text]
    assert not missing, f"top-level --help missing commands: {missing}"


def test_sage_version_flag_works():
    """The --version flag must produce a version string. Catches a class
    of regressions where the Typer app forgets to wire up version
    handling and the user gets a generic 'unknown option' error."""
    res = subprocess.run(
        [sys.executable, "-m", "sage", "--version"],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        timeout=15,
    )
    assert res.returncode == 0
    out = (res.stdout or "") + (res.stderr or "")
    # Just verify SOMETHING that looks like a version printed.
    assert any(ch.isdigit() for ch in out), (
        f"--version output didn't contain digits: {out!r}"
    )
