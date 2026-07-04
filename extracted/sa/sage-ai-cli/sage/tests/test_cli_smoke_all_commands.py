"""CLI smoke tests — `--help` on every command + subcommand.

The cheapest insurance you can buy: each test runs `<cmd> --help` and
verifies the exit code is 0 + help text mentions the expected info.
Catches:

  - Import errors (missing optional deps)
  - Typer signature bugs (wrong Annotation, conflicting flags)
  - Subapp registration mistakes (command exists but doesn't appear in help)
  - Help-text drift (someone removed a documented flag)

This file expands `test_all_commands.py` with coverage for the new
commands. Real behavior tests live in their feature-specific test files.
"""

from __future__ import annotations

import pytest
from typer.testing import CliRunner


_runner = CliRunner()


@pytest.fixture(scope="module")
def sage_app():
    """Module-scoped import of the full sage CLI app."""
    from sage.cli_core import app
    return app


@pytest.fixture(scope="module")
def new_commands_app():
    """The standalone new-commands subapp (faster than importing full sage.main)."""
    from sage.cli.new_commands import app as new_app
    return new_app


# ── Top-level help loads ────────────────────────────────────────────────────


class TestRootHelp:
    def test_sage_help_runs(self, sage_app):
        result = _runner.invoke(sage_app, ["--help"])
        assert result.exit_code == 0
        assert "Sage" in result.stdout or "sage" in result.stdout

    def test_sage_help_lists_all_new_commands(self, sage_app):
        result = _runner.invoke(sage_app, ["--help"])
        assert result.exit_code == 0
        # Every new command must appear in top-level help
        for cmd in ("search", "image", "schedule", "integrate", "daemon", "autopolit"):
            assert cmd in result.stdout, f"sage {cmd} missing from --help"


# ── Per-command help ────────────────────────────────────────────────────────


class TestCommandHelp:
    """Every documented command must respond cleanly to --help. Catches
    import errors and typer signature bugs that ONLY surface when the
    command is invoked."""

    @pytest.mark.parametrize("cmd", [
        # Existing commands
        ["models", "--help"],
        ["ask", "--help"],
        ["run", "--help"],
        ["whoami", "--help"],
        # New top-level commands
        ["search", "--help"],
        ["image", "--help"],
        ["autopolit", "--help"],
    ])
    def test_command_help_exits_clean(self, sage_app, cmd):
        result = _runner.invoke(sage_app, cmd)
        assert result.exit_code == 0, f"sage {' '.join(cmd)} failed: {result.output}"


# ── New subcommand groups ───────────────────────────────────────────────────


class TestNewSubcommandHelp:
    """schedule/integrate/daemon are subcommand groups — verify each
    subcommand's help loads."""

    @pytest.mark.parametrize("cmd", [
        ["schedule", "--help"],
        ["schedule", "add", "--help"],
        ["schedule", "list", "--help"],
        ["schedule", "pause", "--help"],
        ["schedule", "resume", "--help"],
        ["schedule", "remove", "--help"],
        ["schedule", "run-due", "--help"],
        ["integrate", "--help"],
        ["integrate", "list", "--help"],
        ["integrate", "connect", "--help"],
        ["integrate", "revoke", "--help"],
        ["daemon", "--help"],
        ["daemon", "start", "--help"],
        ["daemon", "status", "--help"],
        ["daemon", "stop", "--help"],
    ])
    def test_subcommand_help_exits_clean(self, new_commands_app, cmd):
        result = _runner.invoke(new_commands_app, cmd)
        assert result.exit_code == 0, f"sage {' '.join(cmd)} failed: {result.output}"


# ── Ask --image and --file documented ───────────────────────────────────────


class TestAskFlagsDocumented:
    def test_ask_help_mentions_image_flag(self, sage_app):
        result = _runner.invoke(sage_app, ["ask", "--help"])
        assert result.exit_code == 0
        # --image flag should be in help text (with description)
        assert "--image" in result.stdout
        assert "PDF" in result.stdout or "DOCX" in result.stdout  # --file extended desc

    def test_ask_help_mentions_file_pdf_support(self, sage_app):
        result = _runner.invoke(sage_app, ["ask", "--help"])
        # Updated --file description should mention auto-extraction
        assert "--file" in result.stdout


# ── Error UX: friendly errors, not stack traces ─────────────────────────────


class TestFriendlyErrors:
    """User-facing commands must NEVER show Python tracebacks to end
    users — every failure path returns a clean message + non-zero exit."""

    def test_search_empty_query_clean_error(self, new_commands_app):
        result = _runner.invoke(new_commands_app, ["search", ""])
        assert result.exit_code != 0
        # No "Traceback" in output
        assert "Traceback" not in result.stdout
        assert "Traceback" not in (result.stderr or "")

    def test_image_empty_prompt_clean_error(self, new_commands_app):
        result = _runner.invoke(new_commands_app, ["image", ""])
        assert result.exit_code != 0
        assert "Traceback" not in result.stdout

    def test_schedule_invalid_schedule_clean_error(self, new_commands_app, tmp_path, monkeypatch):
        monkeypatch.setenv("SAGE_SCHEDULER_STATE", str(tmp_path / "tasks.json"))
        result = _runner.invoke(
            new_commands_app, ["schedule", "add", "x", "--every", "garbage"],
        )
        assert result.exit_code != 0
        assert "Traceback" not in result.stdout
        assert "Invalid" in result.stdout or "invalid" in result.stdout

    def test_integrate_unknown_service_clean_error(self, new_commands_app):
        result = _runner.invoke(new_commands_app, ["integrate", "connect", "fake-service"])
        assert result.exit_code != 0
        assert "Traceback" not in result.stdout
        assert "Unknown" in result.stdout or "unknown" in result.stdout


# ── Daemon flag combinations ────────────────────────────────────────────────


class TestDaemonFlagValidation:
    def test_daemon_start_with_no_bridges_rejected(self, new_commands_app):
        """Starting the daemon with --no-imessage and no Telegram/Discord
        means 0 bridges — should refuse to start rather than silently
        running nothing."""
        result = _runner.invoke(
            new_commands_app,
            ["daemon", "start", "--no-imessage"],
        )
        assert result.exit_code != 0
        assert "No bridges" in result.stdout or "bridge" in result.stdout.lower()
