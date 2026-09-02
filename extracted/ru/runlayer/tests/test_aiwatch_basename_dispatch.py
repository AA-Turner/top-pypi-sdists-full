"""End-to-end smoke test for the ``aiwatch hook`` subcommand dispatch.

The converged onedir bundle ships a single ``aiwatch`` exe. The hook fires via
the ``aiwatch hook`` command string wired into each client's config;
``runlayer_cli.aiwatch.main`` dispatches ``sys.argv[1] == "hook"`` straight to
``runlayer_cli.hook.dispatch.run_hook`` (stripping the token) before the typer
app loads, so the hot path never imports the heavier command/scan modules.

Asserting the deny shape (rather than just observing exit code) catches the
specific failure mode where someone breaks subcommand dispatch and the hook
silently routes through the typer app, which would make every Cursor hook fire
fail open.
"""

from __future__ import annotations

import json
import subprocess
import struct
import sys
import textwrap
from pathlib import Path

CLI_ROOT = Path(__file__).resolve().parents[1]


def test_aiwatch_hook_subcommand_runs_hook_main(tmp_path: Path):
    """``aiwatch hook --version`` routes to run_hook()."""
    fake_argv0 = str(tmp_path / "aiwatch")
    probe = textwrap.dedent(
        """
        import sys
        sys.argv = [%(argv0)r, "hook", "--version"]
        from runlayer_cli.aiwatch import main
        main()
        """
        % {"argv0": fake_argv0}
    )
    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=CLI_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"hook --version via subcommand dispatch failed:\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
    assert "aiwatch version" in result.stdout, result.stdout


def test_aiwatch_no_subcommand_runs_scan_app(tmp_path: Path):
    """``aiwatch --help`` (no ``hook`` token) routes to the typer scan app.

    Both the hook path and the typer callback now print ``aiwatch version``, so
    routing is distinguished by behavior unique to typer: a ``Usage:`` help
    screen, which ``run_hook`` never emits.
    """
    fake_argv0 = str(tmp_path / "aiwatch")
    probe = textwrap.dedent(
        """
        import sys
        sys.argv = [%(argv0)r, "--help"]
        from runlayer_cli.aiwatch import main
        main()
        """
        % {"argv0": fake_argv0}
    )
    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=CLI_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Usage:" in result.stdout


def test_aiwatch_hook_stdin_deny_on_missing_creds(tmp_path: Path):
    """End-to-end: stdin → hook deny shape when no creds are configured.

    Routes via the ``aiwatch hook`` subcommand, so this exercises the converged
    entrypoint plus the hook's fail-closed deny path through dispatch.run_hook
    and relay._load_credentials.
    """
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    fake_argv0 = str(tmp_path / "aiwatch")
    payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash"})

    probe = textwrap.dedent(
        """
        import os, sys
        from pathlib import Path
        import runlayer_cli.mdm_config as mdm_config
        os.environ["HOME"] = %(home)r
        # Ensure no MDM-pushed config / keyring / secret is around.
        os.environ.pop("RUNLAYER_HOST", None)
        os.environ.pop("RUNLAYER_API_KEY", None)
        mdm_config.MACOS_PLIST_PATHS = (Path(%(home)r) / "missing.plist",)
        sys.argv = [%(argv0)r, "hook"]
        from runlayer_cli.aiwatch import main
        main()
        """
        % {"home": str(fake_home), "argv0": fake_argv0}
    )
    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=CLI_ROOT,
        capture_output=True,
        text=True,
        input=payload,
        check=False,
    )
    # Hook always exits 0 (deny is a JSON response, not a non-zero exit).
    assert result.returncode == 0, (
        f"hook subprocess exited non-zero:\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
    # Deny shape is client-specific; the common shape is some JSON. Just
    # confirm we got a JSON object back (not a typer Usage error which would
    # contain "Usage:" / "Try '... --help'").
    assert "Usage:" not in result.stdout
    assert result.stdout.strip().startswith("{")


def test_aiwatch_native_messaging_basename_runs_native_host(tmp_path: Path):
    """``aiwatch-native-messaging-host`` argv0 routes to the native host."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    fake_argv0 = str(tmp_path / "aiwatch-native-messaging-host")
    request = json.dumps({"type": "identity.get", "version": 1}).encode()
    framed_request = struct.pack("<I", len(request)) + request

    probe = textwrap.dedent(
        """
        import os, sys
        os.environ["HOME"] = %(home)r
        os.environ["USER"] = "native-user"
        sys.argv = [%(argv0)r]
        from runlayer_cli.aiwatch import main
        main()
        """
        % {"home": str(fake_home), "argv0": fake_argv0}
    )
    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=CLI_ROOT,
        capture_output=True,
        input=framed_request,
        check=False,
    )

    assert result.returncode == 0, (
        f"native host subprocess exited non-zero:\n"
        f"stdout: {result.stdout!r}\n"
        f"stderr: {result.stderr!r}"
    )
    assert len(result.stdout) >= 4
    response_len = struct.unpack("<I", result.stdout[:4])[0]
    response = json.loads(result.stdout[4 : 4 + response_len].decode())
    assert response["ok"] is True
    assert response["version"] == 1
    assert set(response["identity"]) == {"username", "deviceName"}
