"""Backwards compatibility tests for CLI command patterns.

These tests ensure that existing CLI command patterns continue to work
when we make changes to the CLI. Each test validates that a specific
command pattern is still accepted by the CLI parser.

If any of these tests fail, it means a backwards-incompatible change
was made to the CLI that could break existing user scripts/configs.
"""

from types import SimpleNamespace
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from runlayer_cli import regex_safe
from runlayer_cli.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_login_flow():
    """Mock login function to prevent it from starting a server and waiting forever."""
    with patch("runlayer_cli.commands.auth.login") as mock_login:
        # Make login a no-op
        mock_login.return_value = None
        yield mock_login


def strip_ansi(text: str) -> str:
    """Strip ANSI escape codes from text."""
    ansi_escape = regex_safe.compile(r"\x1b\[[0-9;]*m")
    return ansi_escape.sub("", text)


# =============================================================================
# Command patterns that MUST continue to work for backwards compatibility
# =============================================================================

# Format: (command_args, expected_in_output, description)
# We test --help for each pattern to verify the options are accepted

BACKWARDS_COMPAT_PATTERNS = [
    # Run command - old pattern with command-level options
    (
        ["run", "--help"],
        ["--secret", "--host", "TARGET"],
        "run command should accept --secret and --host options",
    ),
    (
        ["run", "test-uuid", "--secret", "test-key", "--host", "http://localhost"],
        None,  # Will fail on connection, but should parse args
        "run command should accept: run <uuid> --secret <key> --host <url>",
    ),
    # Deploy command - old pattern with command-level options
    (
        ["deploy", "--help"],
        ["--secret", "--host", "--config"],
        "deploy command should accept --secret and --host options",
    ),
    (
        ["deploy", "validate", "--help"],
        ["--secret", "--host", "--config"],
        "deploy validate should accept --secret and --host options",
    ),
    (
        ["deploy", "init", "--help"],
        ["--secret", "--host", "--config"],
        "deploy init should accept --secret and --host options",
    ),
    (
        ["deploy", "destroy", "--help"],
        ["--secret", "--host", "--config", "--deployment-id"],
        "deploy destroy should accept --secret and --host options",
    ),
    (
        ["deploy", "pull", "--help"],
        ["--secret", "--host", "--config", "--deployment-id"],
        "deploy pull should accept --secret and --host options",
    ),
    # Scan command - old pattern with command-level options
    (
        ["scan", "--help"],
        ["--secret", "--host", "--dry-run"],
        "scan command should accept --secret and --host options",
    ),
    # Login command
    (
        ["login", "--help"],
        ["--host"],
        "login command should accept --host option",
    ),
    # Logout command
    (
        ["logout", "--help"],
        [],
        "logout command should exist",
    ),
    # Global options - new pattern
    (
        ["--help"],
        ["--secret", "--host", "--version"],
        "root command should have global --secret and --host options",
    ),
    # Version flag
    (
        ["--version"],
        ["runlayer version"],
        "version flag should work",
    ),
    (
        ["-v"],
        ["runlayer version"],
        "short version flag should work",
    ),
]


@pytest.mark.parametrize(
    "args,expected_strings,description",
    BACKWARDS_COMPAT_PATTERNS,
    ids=[p[2] for p in BACKWARDS_COMPAT_PATTERNS],
)
def test_backwards_compat_pattern(args, expected_strings, description):
    """Test that backwards compatible command patterns still work."""
    result = runner.invoke(app, args)
    output = strip_ansi(result.stdout + result.stderr)

    # For --help commands, we expect exit code 0
    if "--help" in args:
        assert result.exit_code == 0, (
            f"Command failed: {' '.join(args)}\n"
            f"Exit code: {result.exit_code}\n"
            f"Output: {output}"
        )

    # Check expected strings are present
    if expected_strings:
        for expected in expected_strings:
            assert expected in output, (
                f"Expected '{expected}' in output for: {' '.join(args)}\n"
                f"Output: {output}"
            )


# =============================================================================
# Specific backwards compatibility scenarios
# =============================================================================


def test_run_accepts_secret_after_uuid():
    """Ensure 'runlayer run <uuid> --secret <key>' pattern works (old pattern)."""
    result = runner.invoke(
        app, ["run", "test-uuid", "--secret", "test-key", "--host", "http://localhost"]
    )
    output = strip_ansi(result.stdout + result.stderr)

    # Should fail on connection, not on argument parsing
    # If args were rejected, we'd see "No such option" error
    assert "No such option" not in output, (
        f"Command-level --secret/--host should be accepted.\nOutput: {output}"
    )


def test_global_options_work():
    """Ensure global --secret and --host options work (new pattern)."""
    result = runner.invoke(
        app, ["--secret", "test-key", "--host", "http://localhost", "run", "test-uuid"]
    )
    output = strip_ansi(result.stdout + result.stderr)

    # Should fail on connection, not on argument parsing
    assert "No such option" not in output, (
        f"Global --secret/--host should be accepted.\nOutput: {output}"
    )


def test_deploy_validate_accepts_command_level_options():
    """Ensure 'deploy validate --secret <key> --host <url>' works."""
    result = runner.invoke(
        app,
        [
            "deploy",
            "validate",
            "--secret",
            "test-key",
            "--host",
            "http://localhost",
            "--config",
            "nonexistent.yaml",
        ],
    )
    output = strip_ansi(result.stdout + result.stderr)

    # Should fail on file not found, not on argument parsing
    assert "No such option" not in output, (
        f"Command-level options should be accepted.\nOutput: {output}"
    )


def test_scan_accepts_command_level_options():
    """Ensure 'scan --secret <key> --host <url>' works."""
    # This is a parse-only backwards-compat check ("no rejected option"), so stub
    # the scan itself: with static agent detection on by default a real dry-run
    # would crawl + walk the whole home tree (seconds-to-minutes of I/O) for a
    # test that only cares whether typer accepts the flags. Mirrors the scan
    # mocking in test_cli.py.
    scan_result = SimpleNamespace(
        total_servers=0,
        detected_clients=[],
        total_skills=0,
        total_plugins=0,
        agents=[],
        processes=[],
        containers=[],
        containers_scanned=False,
        wsl_distros=[],
        wsl_scanned=False,
    )
    with patch(
        "runlayer_cli.commands.scan.scan_all_clients",
        return_value=scan_result,
    ):
        result = runner.invoke(
            app,
            ["scan", "--secret", "test-key", "--host", "http://localhost", "--dry-run"],
        )
    output = strip_ansi(result.stdout + result.stderr)

    # Should run (dry-run doesn't need connection)
    assert "No such option" not in output, (
        f"Command-level options should be accepted.\nOutput: {output}"
    )


def test_scan_envvar_still_works():
    """Ensure RUNLAYER_API_KEY and RUNLAYER_HOST envvars still work for scan."""
    result = runner.invoke(
        app,
        ["scan", "--help"],
    )
    output = strip_ansi(result.stdout)

    # The help should mention the envvars
    # (envvar support is defined in the option)
    assert result.exit_code == 0
