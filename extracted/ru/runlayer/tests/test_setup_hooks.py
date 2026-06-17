"""Tests for the setup hooks command."""

import json
import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import yaml
from typer.testing import CliRunner

from runlayer_cli.config import Config, HostConfig
from runlayer_cli.credential_store import KeyringCredentialStore

from runlayer_cli.commands.setup import (
    Client,
    _generate_claude_settings,
    _install_ignorefile,
    _is_runlayer_command,
    _merge_claude_hooks,
    _merge_cursor_hooks,
    _migrate_claude_code_user_to_enterprise,
    _migrate_user_to_enterprise,
    _uninstall_ignorefile,
)
from runlayer_cli.main import app

runner = CliRunner()


class TestIsRunlayerCommand:
    """``_is_runlayer_command`` must recognize both install paths' output.

    The MDM bundle path (``hook_install/clients.py``) writes the converged
    ``aiwatch hook --client <name>`` form (space, not hyphen). The operator
    path's filter has to treat those as Runlayer-owned so it rewrites/cleans
    them instead of leaving duplicates behind.
    """

    def test_recognizes_converged_bundle_command(self):
        assert _is_runlayer_command("/usr/local/bin/aiwatch hook --client cursor")

    def test_recognizes_quoted_converged_command(self):
        assert _is_runlayer_command('"/opt/Runlayer App/aiwatch" hook --client claude')

    def test_recognizes_windows_converged_command(self):
        assert _is_runlayer_command(
            r'"C:\Program Files\Runlayer\aiwatch.exe" hook --client cursor'
        )

    def test_recognizes_legacy_script_names(self):
        assert _is_runlayer_command("/old/aiwatch-hook --client cursor")

    def test_ignores_empty_command(self):
        assert not _is_runlayer_command("")

    def test_ignores_third_party_command(self):
        assert not _is_runlayer_command("/usr/bin/some-other-hook --flag")


def strip_ansi(text: str) -> str:
    """Strip ANSI escape codes from text."""
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_escape.sub("", text)


def test_setup_hooks_help():
    """Test that setup hooks command shows help."""
    result = runner.invoke(app, ["setup", "hooks", "--help"])
    assert result.exit_code == 0
    plain_output = strip_ansi(result.stdout)
    assert "Install or uninstall Runlayer client hooks" in plain_output
    assert "--install" in plain_output
    assert "--uninstall" in plain_output
    assert "--host" in plain_output
    assert "--yes" in plain_output
    assert "--mdm" in plain_output
    assert "--event-hooks" in plain_output
    assert "cursor" in plain_output.lower()


def test_setup_hooks_requires_action():
    """Test that setup hooks command requires --install or --uninstall."""
    result = runner.invoke(
        app,
        ["setup", "hooks", "--client", "cursor"],
    )
    assert result.exit_code != 0
    plain_output = strip_ansi(result.output)
    assert "Must specify either --install or --uninstall" in plain_output


def test_setup_hooks_install_uninstall_mutually_exclusive():
    """Test that --install and --uninstall cannot be used together."""
    result = runner.invoke(
        app,
        [
            "setup",
            "hooks",
            "--client",
            "cursor",
            "--install",
            "--uninstall",
        ],
    )
    assert result.exit_code != 0
    plain_output = strip_ansi(result.output)
    assert "Cannot use both --install and --uninstall" in plain_output


def test_setup_hooks_install_requires_config():
    """Test that --install requires config.yaml to exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--yes",
                ],
            )
            assert result.exit_code != 0
            plain_output = strip_ansi(result.output)
            assert "No Runlayer config found" in plain_output


def test_setup_hooks_install():
    """Test that --install installs enforcement-only hooks by default."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        # Create config.yaml
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Hooks installed" in plain_output
            assert "enforcement only" in plain_output
            assert "Restart Cursor" in plain_output

            hook_script = client_dir / "hooks" / "runlayer-hook.sh"
            assert hook_script.exists()

            # Verify hook script is static (no baked-in credentials)
            hook_content = hook_script.read_text()
            assert "__RUNLAYER_API_KEY__" not in hook_content
            assert "__RUNLAYER_API_HOST__" not in hook_content
            assert "beforeMCPExecution" in hook_content
            assert "beforeReadFile" in hook_content
            assert "beforeTabFileRead" in hook_content

            # Verify hooks.json has only enforcement hooks
            hooks_json = client_dir / "hooks.json"
            assert hooks_json.exists()
            hooks_config = json.loads(hooks_json.read_text())
            assert hooks_config["version"] == 1
            assert "beforeMCPExecution" in hooks_config["hooks"]
            assert "beforeReadFile" in hooks_config["hooks"]
            assert "beforeTabFileRead" in hooks_config["hooks"]
            assert "beforeShellExecution" in hooks_config["hooks"]
            assert "preToolUse" in hooks_config["hooks"]
            assert "postToolUse" in hooks_config["hooks"]
            assert "postToolUseFailure" in hooks_config["hooks"]
            # Event/session hooks should NOT be registered
            assert "sessionStart" not in hooks_config["hooks"]
            assert (
                str(hook_script)
                in hooks_config["hooks"]["beforeMCPExecution"][0]["command"]
            )
            assert (
                str(hook_script)
                in hooks_config["hooks"]["beforeReadFile"][0]["command"]
            )
            assert (
                str(hook_script)
                in hooks_config["hooks"]["beforeTabFileRead"][0]["command"]
            )


def test_setup_hooks_install_event_hooks():
    """Test that --event-hooks registers enforcement + all event hooks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--event-hooks",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "enforcement + event hooks" in plain_output

            hooks_json = client_dir / "hooks.json"
            hooks_config = json.loads(hooks_json.read_text())
            assert "beforeMCPExecution" in hooks_config["hooks"]
            assert "sessionStart" in hooks_config["hooks"]
            assert "preToolUse" in hooks_config["hooks"]
            assert "afterTabFileEdit" in hooks_config["hooks"]
            assert "stop" in hooks_config["hooks"]

            config_path = client_dir / "hooks" / "runlayer-config.json"
            config = json.loads(config_path.read_text())
            assert config["enforcement"] is True


def test_setup_hooks_install_no_enforcement():
    """Test that --no-enforcement installs all hooks in monitoring-only mode."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--no-enforcement",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "monitoring only (no enforcement)" in plain_output

            # All hooks (enforcement + event/session hooks) should be registered
            hooks_json = client_dir / "hooks.json"
            hooks_config = json.loads(hooks_json.read_text())
            assert "beforeMCPExecution" in hooks_config["hooks"]
            assert "beforeReadFile" in hooks_config["hooks"]
            assert "beforeTabFileRead" in hooks_config["hooks"]
            assert "sessionStart" in hooks_config["hooks"]
            assert "afterTabFileEdit" in hooks_config["hooks"]
            assert "preToolUse" in hooks_config["hooks"]

            # Config file should indicate enforcement=false
            config_path = client_dir / "hooks" / "runlayer-config.json"
            assert config_path.exists()
            config = json.loads(config_path.read_text())
            assert config["enforcement"] is False

            # .cursorignore should NOT be installed
            cursorignore = fake_home / ".cursorignore"
            assert not cursorignore.exists()

            # "Hierarchical Cursor Ignore" note should NOT appear
            assert "Hierarchical Cursor Ignore" not in plain_output


def test_setup_hooks_install_hermes():
    """Hermes install writes shell hooks into ~/.hermes/config.yaml."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hermes_dir = Path(temp_dir) / ".hermes"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.HERMES: hermes_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "hermes",
                    "--install",
                    "--yes",
                ],
            )

        plain_output = strip_ansi(result.stdout)
        assert result.exit_code == 0
        assert "Hooks installed" in plain_output
        assert "enforcement only" in plain_output
        assert "Restart Hermes" in plain_output

        hook_script = hermes_dir / "agent-hooks" / "runlayer-hook.sh"
        assert hook_script.exists()
        hook_content = hook_script.read_text()
        assert "__RUNLAYER_API_KEY__" not in hook_content
        assert "__RUNLAYER_API_HOST__" not in hook_content

        config = yaml.safe_load((hermes_dir / "config.yaml").read_text())
        assert "pre_tool_call" in config["hooks"]
        assert "transform_tool_result" in config["hooks"]
        assert "post_tool_call" not in config["hooks"]
        assert config["hooks"]["pre_tool_call"][0]["command"] == str(hook_script)

        runtime_config = json.loads(
            (hermes_dir / "agent-hooks" / "runlayer-config.json").read_text()
        )
        assert runtime_config["enforcement"] is True


def test_setup_hooks_install_hermes_event_hooks():
    with tempfile.TemporaryDirectory() as temp_dir:
        hermes_dir = Path(temp_dir) / ".hermes"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.HERMES: hermes_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "hermes",
                    "--install",
                    "--event-hooks",
                    "--yes",
                ],
            )

        assert result.exit_code == 0
        hooks = yaml.safe_load((hermes_dir / "config.yaml").read_text())["hooks"]
        assert "pre_tool_call" in hooks
        assert "transform_tool_result" in hooks
        assert "post_tool_call" in hooks
        assert "pre_llm_call" in hooks
        assert "on_session_start" in hooks
        assert "on_session_end" in hooks
        assert "on_session_finalize" in hooks


def test_setup_hooks_uninstall_hermes_preserves_third_party_hooks():
    with tempfile.TemporaryDirectory() as temp_dir:
        hermes_dir = Path(temp_dir) / ".hermes"
        hooks_dir = hermes_dir / "agent-hooks"
        hooks_dir.mkdir(parents=True)
        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho hook")
        (hooks_dir / "runlayer-config.json").write_text('{"enforcement": true}')
        config_path = hermes_dir / "config.yaml"
        config_path.write_text(
            yaml.safe_dump(
                {
                    "hooks": {
                        "pre_tool_call": [
                            {"command": "/usr/local/bin/third-party-hook"},
                            {"command": str(hook_script)},
                        ],
                        "transform_tool_result": [
                            {"command": str(hook_script)},
                        ],
                    }
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.HERMES: hermes_dir},
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "hermes", "--uninstall", "--yes"],
            )

        assert result.exit_code == 0
        assert not hook_script.exists()
        config = yaml.safe_load(config_path.read_text())
        assert config["hooks"] == {
            "pre_tool_call": [{"command": "/usr/local/bin/third-party-hook"}]
        }


def test_setup_hooks_install_hermes_mdm_not_supported():
    result = runner.invoke(
        app,
        [
            "setup",
            "hooks",
            "--client",
            "hermes",
            "--install",
            "--mdm",
            "--yes",
        ],
    )

    plain_output = strip_ansi(result.output)
    assert result.exit_code == 1
    assert "Hermes MDM hooks are not supported" in plain_output


def test_setup_hooks_install_cursor_creates_cursorignore_not_claudeignore():
    """Cursor install creates .cursorignore, not .claudeignore, and shows Cursor note."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0

            assert (fake_home / ".cursorignore").exists()
            assert not (fake_home / ".claudeignore").exists()
            assert "Updated ~/.cursorignore" in plain_output
            assert "Hierarchical Cursor Ignore" in plain_output


def test_setup_hooks_install_claude_code_creates_claudeignore_not_cursorignore():
    """Claude Code install creates .claudeignore, not .cursorignore, no Cursor note."""
    with tempfile.TemporaryDirectory() as temp_dir:
        claude_dir = Path(temp_dir) / ".claude"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CLAUDE_CODE: claude_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "claude_code",
                    "--install",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0

            assert (fake_home / ".claudeignore").exists()
            assert not (fake_home / ".cursorignore").exists()
            assert "Updated ~/.claudeignore" in plain_output
            assert "Hierarchical Cursor Ignore" not in plain_output


def test_setup_hooks_install_default_enforcement_config():
    """Test that default install writes runlayer-config.json with enforcement=true."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--yes",
                ],
            )

            assert result.exit_code == 0
            config_path = client_dir / "hooks" / "runlayer-config.json"
            assert config_path.exists()
            config = json.loads(config_path.read_text())
            assert config["enforcement"] is True


def test_setup_hooks_uninstall_removes_config():
    """Test that --uninstall also removes runlayer-config.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        hooks_dir = client_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho test")
        hook_config = hooks_dir / "runlayer-config.json"
        hook_config.write_text('{"enforcement": false}')
        hooks_json = client_dir / "hooks.json"
        hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": str(hooks_dir / "runlayer-hook.sh")}
                        ]
                    },
                }
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "cursor", "--uninstall", "--yes"],
            )

            assert result.exit_code == 0
            assert not hook_script.exists()
            assert not hook_config.exists()
            assert not hooks_json.exists()


def test_setup_hooks_install_does_not_auto_enable_event_hooks():
    """Install should not auto-enable event hooks from backend config."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--yes",
                ],
            )
            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "enforcement only" in plain_output

            hooks_json = client_dir / "hooks.json"
            hooks_config = json.loads(hooks_json.read_text())
            assert "sessionStart" not in hooks_config["hooks"]
            assert "preToolUse" in hooks_config["hooks"]
            assert "postToolUse" in hooks_config["hooks"]


def test_setup_hooks_install_all_clients():
    """Test that setup hooks installs to all clients when --client is not specified."""
    with tempfile.TemporaryDirectory() as temp_dir:
        cursor_dir = Path(temp_dir) / ".cursor"
        claude_dir = Path(temp_dir) / ".claude"
        codex_dir = Path(temp_dir) / ".codex"
        hermes_dir = Path(temp_dir) / ".hermes"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {
                    Client.CURSOR: cursor_dir,
                    Client.CLAUDE_CODE: claude_dir,
                    Client.CODEX: codex_dir,
                    Client.HERMES: hermes_dir,
                },
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--install",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Hooks installed" in plain_output

            assert (cursor_dir / "hooks" / "runlayer-hook.sh").exists()
            assert (claude_dir / "hooks" / "runlayer-hook.sh").exists()
            assert (codex_dir / "hooks" / "runlayer-hook.sh").exists()
            assert (hermes_dir / "agent-hooks" / "runlayer-hook.sh").exists()


def test_setup_hooks_install_blocked_on_windows():
    """Hook install should fail immediately on Windows."""
    with tempfile.TemporaryDirectory() as temp_dir:
        cursor_dir = Path(temp_dir) / ".cursor"
        claude_dir = Path(temp_dir) / ".claude"
        codex_dir = Path(temp_dir) / ".codex"
        hermes_dir = Path(temp_dir) / ".hermes"

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {
                    Client.CURSOR: cursor_dir,
                    Client.CLAUDE_CODE: claude_dir,
                    Client.CODEX: codex_dir,
                    Client.HERMES: hermes_dir,
                },
            ),
            patch("runlayer_cli.commands.setup.plat.system", return_value="Windows"),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--install", "--yes"],
            )

            plain_output = strip_ansi(result.output)
            assert result.exit_code == 1
            assert "not supported on Windows" in plain_output

            assert not cursor_dir.exists()
            assert not claude_dir.exists()
            assert not codex_dir.exists()
            assert not hermes_dir.exists()


def test_generate_claude_settings_no_shell_key():
    """Hook entries must not contain a 'shell' key (regression for PowerShell-on-bash bug)."""
    settings = _generate_claude_settings(Path("/x/runlayer-hook.sh"))
    for event_name, entries in settings.items():
        for entry in entries:
            for hook in entry["hooks"]:
                assert "shell" not in hook, f"Unexpected 'shell' key in {event_name}"
                assert hook == {"type": "command", "command": "/x/runlayer-hook.sh"}


def test_generate_claude_settings_hook_entries_are_independent():
    """Each event's hook entry must be a distinct dict (no shared references).

    Regression for shared-reference bug: prior impl built one hook_entry dict and
    reused it across all events, so a per-event mutation (e.g. adding "shell":
    "powershell" for Windows) would silently corrupt every other event.
    """
    settings = _generate_claude_settings(
        Path("/x/runlayer-hook.sh"), include_pipeline=True
    )
    seen: list[int] = []
    for entries in settings.values():
        for entry in entries:
            for hook in entry["hooks"]:
                seen.append(id(hook))
    assert len(seen) == len(set(seen)), "hook dicts share references across events"

    first_event = next(iter(settings))
    settings[first_event][0]["hooks"][0]["shell"] = "powershell"
    for event_name, entries in settings.items():
        if event_name == first_event:
            continue
        for entry in entries:
            for hook in entry["hooks"]:
                assert "shell" not in hook, (
                    f"mutation on {first_event} leaked into {event_name}"
                )


def test_setup_hooks_install_creates_backup():
    """Test that --install backs up existing files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        hooks_dir = client_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        # Create existing files
        existing_hook = hooks_dir / "runlayer-hook.sh"
        existing_hook.write_text("# existing hook")
        existing_json = client_dir / "hooks.json"
        existing_json.write_text('{"version": 0}')

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Backed up" in plain_output

            # Verify backup files were created
            backup_files = list(hooks_dir.glob("runlayer-hook.backup_*.sh"))
            assert len(backup_files) == 1
            assert backup_files[0].read_text() == "# existing hook"

            json_backups = list(client_dir.glob("hooks.backup_*.json"))
            assert len(json_backups) == 1
            assert json_backups[0].read_text() == '{"version": 0}'


def test_setup_hooks_install_validates_host_in_config():
    """Test that --host validates the host exists in config."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": HostConfig(
                    url="https://app.runlayer.com", secret="test-key"
                )
            },
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
            patch("runlayer_cli.config.load_config", return_value=config),
        ):
            # Unknown host should fail
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--yes",
                    "--host",
                    "https://unknown.example.com",
                ],
            )
            assert result.exit_code != 0
            plain_output = strip_ansi(result.output)
            assert "not found in config" in plain_output


def test_setup_hooks_install_mdm():
    """Test that --mdm installs to enterprise location."""
    with tempfile.TemporaryDirectory() as temp_dir:
        enterprise_dir = Path(temp_dir) / "enterprise"
        user_dir = Path(temp_dir) / ".cursor"

        with (
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: user_dir},
            ),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Hooks installed" in plain_output

            # Verify installed to enterprise location
            hook_script = enterprise_dir / "hooks" / "runlayer-hook.sh"
            assert hook_script.exists()
            hooks_json = enterprise_dir / "hooks.json"
            assert hooks_json.exists()


def test_setup_hooks_install_quotes_path_with_spaces():
    """Test that hooks.json quotes the command when path has spaces."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Simulate enterprise path with spaces (like /Library/Application Support/Cursor/)
        enterprise_dir = Path(temp_dir) / "Library" / "Application Support" / "Cursor"
        user_dir = Path(temp_dir) / ".cursor"

        with (
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: user_dir},
            ),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            assert result.exit_code == 0
            hooks_json = enterprise_dir / "hooks.json"
            hooks_config = json.loads(hooks_json.read_text())
            command = hooks_config["hooks"]["beforeMCPExecution"][0]["command"]
            # Path with spaces must be quoted
            assert command.startswith('"')
            assert command.endswith('"')
            assert "Application Support" in command


def test_setup_hooks_install_mdm_skips_config_check():
    """Test that --mdm skips config.yaml check (runs as root)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        enterprise_dir = Path(temp_dir) / "enterprise"
        user_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "root_home"
        fake_home.mkdir()
        # No config.yaml exists -- should still succeed with --mdm

        with (
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: user_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            assert result.exit_code == 0
            hook_script = enterprise_dir / "hooks" / "runlayer-hook.sh"
            assert hook_script.exists()


def test_setup_hooks_uninstall():
    """Test that --uninstall removes hook files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        hooks_dir = client_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho test")
        hooks_json = client_dir / "hooks.json"
        hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": str(hooks_dir / "runlayer-hook.sh")}
                        ]
                    },
                }
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "cursor", "--uninstall", "--yes"],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Removed" in plain_output
            assert "runlayer-hook.sh" in plain_output
            assert "Restart Cursor" in plain_output

            assert not hook_script.exists()
            assert not hooks_json.exists()


def test_setup_hooks_uninstall_no_files():
    """Test --uninstall when no hooks are installed."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        client_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "cursor", "--uninstall", "--yes"],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "No Runlayer hooks found" in plain_output


def test_setup_hooks_install_claude_code_enforcement_only():
    """Enforcement-only install registers PreToolUse hook in settings.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        claude_dir = Path(temp_dir) / ".claude"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CLAUDE_CODE: claude_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "claude_code",
                    "--install",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "enforcement only" in plain_output
            assert "Restart Claude Code to activate" in plain_output

            settings_path = claude_dir / "settings.json"
            assert settings_path.exists()
            settings = json.loads(settings_path.read_text())
            assert "hooks" in settings
            assert "PreToolUse" in settings["hooks"]
            assert "PostToolUse" in settings["hooks"]
            assert "PostToolUseFailure" in settings["hooks"]
            # Event/session hooks should NOT be registered
            assert "SessionStart" not in settings["hooks"]
            assert "Stop" not in settings["hooks"]

            hook_script = claude_dir / "hooks" / "runlayer-hook.sh"
            assert hook_script.exists()
            assert str(hook_script) in str(settings["hooks"]["PreToolUse"])

            config_path = claude_dir / "hooks" / "runlayer-config.json"
            assert config_path.exists()
            config = json.loads(config_path.read_text())
            assert config["enforcement"] is True


def test_setup_hooks_install_claude_code_all_events():
    """Test that Claude Code --all-events registers enforcement + all event hooks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        claude_dir = Path(temp_dir) / ".claude"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CLAUDE_CODE: claude_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "claude_code",
                    "--install",
                    "--all-events",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "enforcement + event hooks" in plain_output

            settings_path = claude_dir / "settings.json"
            assert settings_path.exists()
            settings = json.loads(settings_path.read_text())
            assert "hooks" in settings
            assert "PreToolUse" in settings["hooks"]
            assert "SessionStart" in settings["hooks"]
            assert "Stop" in settings["hooks"]
            # Worktree hooks are provider hooks in Claude Code (the hook must
            # create/remove the worktree) — registering aiwatch there breaks
            # worktree creation, so they must never be installed.
            assert "WorktreeCreate" not in settings["hooks"]
            assert "WorktreeRemove" not in settings["hooks"]

            hook_script = claude_dir / "hooks" / "runlayer-hook.sh"
            assert hook_script.exists()

            config_path = claude_dir / "hooks" / "runlayer-config.json"
            config = json.loads(config_path.read_text())
            assert config["enforcement"] is True


def test_setup_hooks_install_codex_enforcement_only():
    """Codex install should write hooks.json and enable features.hooks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        codex_dir = Path(temp_dir) / ".codex"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CODEX: codex_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "codex",
                    "--install",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Restart Codex to activate" in plain_output
            assert "Enabled Codex hooks in config.toml" in plain_output

            hook_script = codex_dir / "hooks" / "runlayer-hook.sh"
            assert hook_script.exists()

            hooks_json = codex_dir / "hooks.json"
            hooks_config = json.loads(hooks_json.read_text())
            assert "PreToolUse" in hooks_config["hooks"]
            assert "PermissionRequest" in hooks_config["hooks"]
            assert "Stop" not in hooks_config["hooks"]
            assert str(hook_script) in str(hooks_config["hooks"]["PreToolUse"])
            assert hooks_config["hooks"]["PreToolUse"][0]["matcher"] == ""
            assert hooks_config["hooks"]["PostToolUse"][0]["matcher"] == ""
            assert hooks_config["hooks"]["PostToolUseFailure"][0]["matcher"] == ""
            assert hooks_config["hooks"]["PermissionRequest"][0]["matcher"] == "Bash"

            config_toml = codex_dir / "config.toml"
            assert config_toml.exists()
            config_toml_text = config_toml.read_text()
            assert "[features]" in config_toml_text
            assert "hooks = true" in config_toml_text
            assert "codex_hooks" not in config_toml_text

            runtime_config = json.loads(
                (codex_dir / "hooks" / "runlayer-config.json").read_text()
            )
            assert runtime_config["enforcement"] is True


def test_setup_hooks_install_codex_replaces_deprecated_feature_flag():
    """Codex install should migrate the old codex_hooks feature flag."""
    with tempfile.TemporaryDirectory() as temp_dir:
        codex_dir = Path(temp_dir) / ".codex"
        codex_dir.mkdir()
        (codex_dir / "config.toml").write_text(
            '[features]\ncodex_hooks = true\napproval_policy = "on-request"\n'
        )
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CODEX: codex_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "codex",
                    "--install",
                    "--yes",
                ],
            )

            assert result.exit_code == 0
            config_toml_text = (codex_dir / "config.toml").read_text()
            assert "hooks = true" in config_toml_text
            assert "codex_hooks" not in config_toml_text
            assert 'approval_policy = "on-request"' in config_toml_text


def test_setup_hooks_install_codex_all_events():
    """Codex all-events install should add the limited event hooks it supports."""
    with tempfile.TemporaryDirectory() as temp_dir:
        codex_dir = Path(temp_dir) / ".codex"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CODEX: codex_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "codex",
                    "--install",
                    "--all-events",
                    "--yes",
                ],
            )

            assert result.exit_code == 0
            hooks_config = json.loads((codex_dir / "hooks.json").read_text())
            assert "SessionStart" in hooks_config["hooks"]
            assert "PostToolUse" in hooks_config["hooks"]
            assert "PostToolUseFailure" in hooks_config["hooks"]
            assert "UserPromptSubmit" in hooks_config["hooks"]
            assert "Stop" in hooks_config["hooks"]
            assert hooks_config["hooks"]["PreToolUse"][0]["matcher"] == ""
            assert hooks_config["hooks"]["PostToolUse"][0]["matcher"] == ""
            assert hooks_config["hooks"]["PostToolUseFailure"][0]["matcher"] == ""
            assert hooks_config["hooks"]["PermissionRequest"][0]["matcher"] == "Bash"


def test_setup_hooks_uninstall_claude_code():
    """Test that --uninstall removes Claude Code hook files and cleans settings.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        claude_dir = Path(temp_dir) / ".claude"
        hooks_dir = claude_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho test")

        settings_path = claude_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "permissions": {"allow": ["Bash"]},
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": str(hook_script),
                                    }
                                ],
                            }
                        ]
                    },
                },
                indent=2,
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CLAUDE_CODE: claude_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CLAUDE_CODE: enterprise_dir},
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "claude_code", "--uninstall", "--yes"],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Removed" in plain_output
            assert "Restart Claude Code" in plain_output

            assert not hook_script.exists()

            assert settings_path.exists()
            remaining = json.loads(settings_path.read_text())
            assert "hooks" not in remaining
            assert remaining["permissions"] == {"allow": ["Bash"]}


def test_setup_hooks_uninstall_all_clients():
    """Test that --uninstall removes hooks from all clients."""
    with tempfile.TemporaryDirectory() as temp_dir:
        cursor_dir = Path(temp_dir) / ".cursor"
        cursor_hooks_dir = cursor_dir / "hooks"
        cursor_hooks_dir.mkdir(parents=True)
        cursor_enterprise_dir = Path(temp_dir) / "cursor-enterprise"

        cursor_hook_script = cursor_hooks_dir / "runlayer-hook.sh"
        cursor_hook_script.write_text("#!/bin/bash\necho test")
        cursor_hooks_json = cursor_dir / "hooks.json"
        cursor_hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": str(cursor_hooks_dir / "runlayer-hook.sh")}
                        ]
                    },
                }
            )
        )

        claude_dir = Path(temp_dir) / ".claude"
        claude_hooks_dir = claude_dir / "hooks"
        claude_hooks_dir.mkdir(parents=True)
        claude_hook_script = claude_hooks_dir / "runlayer-hook.sh"
        claude_hook_script.write_text("#!/bin/bash\necho test")
        claude_settings_path = claude_dir / "settings.json"
        claude_settings_path.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": str(claude_hook_script),
                                    }
                                ],
                            }
                        ]
                    }
                }
            )
        )

        codex_dir = Path(temp_dir) / ".codex"
        codex_hooks_dir = codex_dir / "hooks"
        codex_hooks_dir.mkdir(parents=True)
        codex_hook_script = codex_hooks_dir / "runlayer-hook.sh"
        codex_hook_script.write_text("#!/bin/bash\necho test")
        codex_hook_config = codex_hooks_dir / "runlayer-config.json"
        codex_hook_config.write_text('{"enforcement": true}')
        codex_hooks_json = codex_dir / "hooks.json"
        codex_hooks_json.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "Bash",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": str(codex_hook_script),
                                    }
                                ],
                            }
                        ]
                    }
                }
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {
                    Client.CURSOR: cursor_dir,
                    Client.CLAUDE_CODE: claude_dir,
                    Client.CODEX: codex_dir,
                },
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {
                    Client.CURSOR: cursor_enterprise_dir,
                    Client.CLAUDE_CODE: Path(temp_dir) / "claude-enterprise",
                    Client.CODEX: Path(temp_dir) / "codex-enterprise",
                },
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--uninstall", "--yes"],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "runlayer-hook.sh" in plain_output
            assert not cursor_hook_script.exists()
            assert not cursor_hooks_json.exists()
            assert not claude_hook_script.exists()
            assert claude_settings_path.exists()
            assert "hooks" not in json.loads(claude_settings_path.read_text())
            assert not codex_hook_script.exists()
            assert not codex_hook_config.exists()
            assert not codex_hooks_json.exists()


def test_setup_hooks_uninstall_permission_error_enterprise():
    """Test --uninstall handles PermissionError on enterprise files gracefully."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # User-level hooks
        client_dir = Path(temp_dir) / ".cursor"
        hooks_dir = client_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho test")
        hooks_json = client_dir / "hooks.json"
        hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": str(hooks_dir / "runlayer-hook.sh")}
                        ]
                    },
                }
            )
        )

        # Enterprise-level hooks
        enterprise_dir = Path(temp_dir) / "enterprise"
        ent_hooks_dir = enterprise_dir / "hooks"
        ent_hooks_dir.mkdir(parents=True)
        ent_hook_script = ent_hooks_dir / "runlayer-hook.sh"
        ent_hook_script.write_text("#!/bin/bash\necho enterprise")
        ent_hooks_json = enterprise_dir / "hooks.json"
        ent_hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": str(ent_hooks_dir / "runlayer-hook.sh")}
                        ]
                    },
                }
            )
        )

        original_unlink = Path.unlink

        def guarded_unlink(self, *args, **kwargs):
            if str(self).startswith(str(enterprise_dir)):
                raise PermissionError(13, "Permission denied", str(self))
            return original_unlink(self, *args, **kwargs)

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
            patch.object(Path, "unlink", guarded_unlink),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "cursor", "--uninstall", "--yes"],
            )

            plain_output = strip_ansi(result.output)
            assert result.exit_code == 0
            # User-level hooks should be removed
            assert not hook_script.exists()
            assert not hooks_json.exists()
            # Enterprise files remain (permission denied)
            assert ent_hook_script.exists()
            assert ent_hooks_json.exists()
            # Should warn about enterprise permission issue
            assert "permission denied" in plain_output.lower()
            # cursorignore cleanup should still run (not skipped by crash)
            assert "Runlayer hooks removed" in plain_output


def test_setup_hooks_install_prompts_without_yes():
    """Test that --install prompts for confirmation without --yes."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                ],
                input="n\n",
            )

            plain_output = strip_ansi(result.output)
            assert result.exit_code == 0
            assert "Proceed with installation?" in plain_output
            assert "Aborted" in plain_output

            hook_script = client_dir / "hooks" / "runlayer-hook.sh"
            assert not hook_script.exists()


def test_setup_hooks_install_confirms_with_prompt():
    """Test that --install proceeds when user confirms."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                ],
                input="y\n",
            )

            plain_output = strip_ansi(result.output)
            assert result.exit_code == 0
            assert "Hooks installed" in plain_output

            hook_script = client_dir / "hooks" / "runlayer-hook.sh"
            assert hook_script.exists()


def test_setup_hooks_uninstall_prompts_without_yes():
    """Test that --uninstall prompts for confirmation without --yes."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        hooks_dir = client_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho test")

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "cursor", "--uninstall"],
                input="n\n",
            )

            plain_output = strip_ansi(result.output)
            assert result.exit_code == 0
            assert "Proceed with uninstallation?" in plain_output
            assert "Aborted" in plain_output

            assert hook_script.exists()


def test_setup_hooks_invalid_client():
    """Test that setup hooks command rejects invalid client."""
    result = runner.invoke(
        app,
        [
            "setup",
            "hooks",
            "--client",
            "invalid-client",
            "--install",
            "--yes",
        ],
    )
    assert result.exit_code != 0


def test_setup_hooks_deprecated_secret_saves_config():
    """Test that deprecated --secret saves to config.yaml."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: old-key\n"
        )

        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": HostConfig(
                    url="https://app.runlayer.com", secret="old-key"
                )
            },
        )

        # In-memory store so set_host_credentials → get_secret_for_host round-trips
        secrets: dict[str, str] = {}
        mock_store = MagicMock(spec=KeyringCredentialStore)
        mock_store.set_secret.side_effect = lambda k, v: (
            secrets.__setitem__(k, v) or True
        )
        mock_store.get_secret.side_effect = lambda k: secrets.get(k)

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.save_config") as mock_save,
            patch(
                "runlayer_cli.config.get_keyring_store",
                return_value=mock_store,
            ),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--yes",
                    "--secret",
                    "new-key",
                    "--host",
                    "https://app.runlayer.com",
                ],
            )

            assert result.exit_code == 0
            plain_output = strip_ansi(result.output)
            assert "deprecated" in plain_output.lower()
            mock_save.assert_called_once()


# =============================================================================
# _install_ignorefile tests
# =============================================================================


def test_install_ignorefile_creates_new_file():
    """Test creating an ignore file from scratch."""
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / ".cursorignore"
        _install_ignorefile(path)

        assert path.exists()
        content = path.read_text()
        assert "# >>> Runlayer managed" in content
        assert ".env" in content
        assert "mcp.json" in content


def test_install_ignorefile_appends_to_existing():
    """Test appending to an existing ignore file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / ".cursorignore"
        path.write_text("# my custom ignores\nnode_modules/\n")

        _install_ignorefile(path)

        content = path.read_text()
        assert "# my custom ignores" in content
        assert "node_modules/" in content
        assert "# >>> Runlayer managed" in content
        assert ".env" in content


def test_install_ignorefile_idempotent_update():
    """Test that running twice replaces the managed block."""
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / ".cursorignore"
        _install_ignorefile(path)
        _install_ignorefile(path)

        content = path.read_text()
        assert content.count("# >>> Runlayer managed") == 1
        assert content.count("# <<< Runlayer managed") == 1


# =============================================================================
# _migrate_user_to_enterprise tests
# =============================================================================


def test_migrate_removes_user_hooks():
    """Test that MDM migration removes user-level hooks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".cursor"
        hooks_dir = user_dir / "hooks"
        hooks_dir.mkdir(parents=True)

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho hook")
        hooks_json = user_dir / "hooks.json"
        hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {"beforeMCPExecution": [{"command": str(hook_script)}]},
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.CURSOR: user_dir},
        ):
            _migrate_user_to_enterprise(Client.CURSOR)

        assert not hook_script.exists()
        assert not hooks_json.exists()
        # Backups should exist
        assert len(list(hooks_dir.glob("runlayer-hook.backup_*.sh"))) == 1
        assert len(list(user_dir.glob("hooks.backup_*.json"))) == 1


def test_migrate_removes_user_hooks_jsonc():
    """Test that MDM migration handles JSONC hooks.json (comments, trailing commas)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".cursor"
        hooks_dir = user_dir / "hooks"
        hooks_dir.mkdir(parents=True)

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho hook")
        hooks_json = user_dir / "hooks.json"
        # JSONC: has comments and trailing comma — json.loads would choke on this
        hooks_json.write_text(
            "{\n"
            "  // Cursor hooks config\n"
            '  "version": 1,\n'
            '  "hooks": {\n'
            '    "beforeMCPExecution": [\n'
            '      {"command": "' + str(hook_script).replace("\\", "\\\\") + '"},\n'
            "    ]\n"
            "  }\n"
            "}\n"
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.CURSOR: user_dir},
        ):
            _migrate_user_to_enterprise(Client.CURSOR)

        assert not hook_script.exists()
        assert not hooks_json.exists()
        assert len(list(hooks_dir.glob("runlayer-hook.backup_*.sh"))) == 1
        assert len(list(user_dir.glob("hooks.backup_*.json"))) == 1


def test_migrate_leaves_non_runlayer_hooks():
    """Test that migration leaves non-Runlayer hooks.json alone."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".cursor"
        user_dir.mkdir(parents=True)

        hooks_json = user_dir / "hooks.json"
        hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {"afterFileEdit": [{"command": "/some/other/hook.sh"}]},
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.CURSOR: user_dir},
        ):
            _migrate_user_to_enterprise(Client.CURSOR)

        # hooks.json should NOT be removed (not Runlayer-managed)
        assert hooks_json.exists()


def test_migrate_mdm_install_creates_enterprise_hooks():
    """Test full --mdm install: migrate user hooks + create enterprise hooks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".cursor"
        user_hooks_dir = user_dir / "hooks"
        user_hooks_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"

        # Create user-level hooks
        user_hook = user_hooks_dir / "runlayer-hook.sh"
        user_hook.write_text("#!/bin/bash\necho old")
        user_json = user_dir / "hooks.json"
        user_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {"beforeMCPExecution": [{"command": str(user_hook)}]},
                }
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: user_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "cursor",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            assert result.exit_code == 0

            # User hooks should be gone
            assert not user_hook.exists()
            assert not user_json.exists()

            # Enterprise hooks should exist
            ent_hook = enterprise_dir / "hooks" / "runlayer-hook.sh"
            assert ent_hook.exists()
            ent_json = enterprise_dir / "hooks.json"
            assert ent_json.exists()


# =============================================================================
# _uninstall_ignorefile tests
# =============================================================================


def test_uninstall_ignorefile_removes_managed_block():
    """Test that uninstall removes the Runlayer managed block."""
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / ".cursorignore"
        _install_ignorefile(path)
        assert path.exists()

        _uninstall_ignorefile(path)
        assert not path.exists()


def test_uninstall_ignorefile_preserves_user_content():
    """Test that uninstall preserves user-added content."""
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / ".cursorignore"
        path.write_text("# my custom ignores\nnode_modules/\n")

        _install_ignorefile(path)
        _uninstall_ignorefile(path)

        assert path.exists()
        content = path.read_text()
        assert "# my custom ignores" in content
        assert "node_modules/" in content
        assert "Runlayer managed" not in content


def test_uninstall_ignorefile_noop_when_no_file():
    """Test that uninstall is a no-op when the ignore file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / ".cursorignore"
        _uninstall_ignorefile(path)  # should not raise
        assert not path.exists()


def _write_fake_runlayer(
    bin_dir: Path,
    *,
    response: str = '{"permission":"allow"}',
    exit_code: int = 0,
    capture_path: Path | None = None,
) -> None:
    """Create a fake runlayer binary that simulates hooks relay."""
    bin_dir.mkdir(exist_ok=True)
    fake = bin_dir / "runlayer"
    enforce_input = (
        f"  cat > {shlex.quote(str(capture_path))}\n"
        if capture_path is not None
        else "  cat >/dev/null\n"
    )
    fake.write_text(
        "#!/bin/bash\n"
        'if [[ "$1" == "hooks" && "$2" == "relay" ]]; then\n'
        '  if [[ "${3:-}" == "enforce" ]]; then\n'
        f"{enforce_input}"
        f"    printf '%s\\n' {shlex.quote(response)}\n"
        f"    exit {exit_code}\n"
        "  fi\n"
        "  cat >/dev/null\n"
        "  printf '%s\\n' '{\"permission\":\"allow\"}'\n"
        "  exit 0\n"
        "fi\n"
        "exit 1\n"
    )
    fake.chmod(0o755)


def test_hook_script_monitoring_only_allows_mcp():
    """Test that hook script with enforcement=false allows MCP without calling enforce."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        hook_dir = Path(temp_dir) / "hooks"
        hook_dir.mkdir()
        hook_copy = hook_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (hook_dir / "runlayer-config.json").write_text('{"enforcement": false}')

        hook_input = json.dumps(
            {
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "test",
                "tool_input": "{}",
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir)

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        output = json.loads(result.stdout)
        assert output["permission"] == "allow"


def test_hook_script_monitoring_only_allows_mcp_without_credentials():
    """Test that monitoring-only mode allows MCP even when credentials are missing."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        hook_dir = Path(temp_dir) / "hooks"
        hook_dir.mkdir()
        hook_copy = hook_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (hook_dir / "runlayer-config.json").write_text('{"enforcement": false}')

        hook_input = json.dumps(
            {
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "test",
                "tool_input": "{}",
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir, exit_code=1)

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        output = json.loads(result.stdout)
        assert output["permission"] == "allow", (
            f"Monitoring-only mode should allow MCP even without credentials, "
            f"got: {result.stdout}"
        )


def test_hook_script_monitoring_only_allows_read_file():
    """Test that hook script with enforcement=false allows .env file reads."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        hook_dir = Path(temp_dir) / "hooks"
        hook_dir.mkdir()
        hook_copy = hook_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (hook_dir / "runlayer-config.json").write_text('{"enforcement": false}')

        hook_input = json.dumps(
            {
                "hook_event_name": "beforeReadFile",
                "file_path": "/project/.env",
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir)

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        output = json.loads(result.stdout)
        assert output["permission"] == "allow"


def test_hook_script_enforcement_no_credentials_denies():
    """Enforcement mode denies when relay exits 1 (credential error)."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        hook_dir = Path(temp_dir) / ".cursor" / "hooks"
        hook_dir.mkdir(parents=True)
        hook_copy = hook_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (hook_dir / "runlayer-config.json").write_text('{"enforcement": true}')

        hook_input = json.dumps(
            {
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "test",
                "tool_input": "{}",
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir, exit_code=1)

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        output = json.loads(result.stdout)
        assert output["permission"] == "deny"
        assert "runlayer login" in output["user_message"].lower()


def test_hook_script_enforcement_api_error_denies():
    """Enforcement mode denies when relay exits 2 (API error)."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        hook_dir = Path(temp_dir) / ".cursor" / "hooks"
        hook_dir.mkdir(parents=True)
        hook_copy = hook_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (hook_dir / "runlayer-config.json").write_text('{"enforcement": true}')

        hook_input = json.dumps(
            {
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "test",
                "tool_input": "{}",
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir, response="", exit_code=2)

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        output = json.loads(result.stdout)
        assert output["permission"] == "deny"
        assert "Failed to contact Runlayer API" in output["user_message"]


def test_hook_script_enforcement_allow_response():
    """Enforcement mode returns allow when relay succeeds with allow."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        hook_dir = Path(temp_dir) / ".cursor" / "hooks"
        hook_dir.mkdir(parents=True)
        hook_copy = hook_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (hook_dir / "runlayer-config.json").write_text('{"enforcement": true}')

        hook_input = json.dumps(
            {
                "hook_event_name": "beforeMCPExecution",
                "tool_name": "test",
                "tool_input": "{}",
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir, response='{"permission":"allow"}')

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        output = json.loads(result.stdout)
        assert output["permission"] == "allow"


# =============================================================================
# Claude Code hook script enforcement tests
# =============================================================================


def _setup_claude_hook(temp_dir: str, *, enforcement: bool = True) -> Path:
    """Set up a Claude Code hook script with config in a temp directory.

    Returns the path to the copied hook script.
    """
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists(), "Claude Code hook source script not found"

    hook_dir = Path(temp_dir) / "hooks"
    hook_dir.mkdir(exist_ok=True)
    hook_copy = hook_dir / "runlayer-hook.sh"
    hook_copy.write_text(hook_src.read_text())
    hook_copy.chmod(0o755)
    (hook_dir / "runlayer-config.json").write_text(
        json.dumps({"enforcement": enforcement})
    )

    config_path = Path(temp_dir) / ".runlayer" / "config.yaml"
    config_path.parent.mkdir(exist_ok=True)
    config_path.write_text(
        "default_host: https://app.example.com\n"
        "hosts:\n"
        "  app.example.com:\n"
        "    url: https://app.example.com\n"
        "    secret: test-key\n"
    )

    return hook_copy


def _run_claude_hook(
    hook_path: Path, hook_input: str, home_dir: str, **extra_env: str
) -> subprocess.CompletedProcess:
    """Run the Claude Code hook script and return the result."""
    bin_dir = Path(home_dir) / "bin"
    _write_fake_runlayer(bin_dir)

    env = {
        **os.environ,
        "HOME": home_dir,
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
        **extra_env,
    }
    return subprocess.run(
        ["bash", str(hook_path)],
        input=hook_input,
        capture_output=True,
        text=True,
        env=env,
    )


def _setup_codex_hook(temp_dir: str, *, enforcement: bool = True) -> Path:
    """Set up a Codex hook script with config in a temp directory."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists(), "Codex hook source script not found"

    hook_dir = Path(temp_dir) / ".codex" / "hooks"
    hook_dir.mkdir(parents=True, exist_ok=True)
    hook_copy = hook_dir / "runlayer-hook.sh"
    hook_copy.write_text(hook_src.read_text())
    hook_copy.chmod(0o755)
    (hook_dir / "runlayer-config.json").write_text(
        json.dumps({"enforcement": enforcement})
    )

    config_path = Path(temp_dir) / ".runlayer" / "config.yaml"
    config_path.parent.mkdir(exist_ok=True)
    config_path.write_text(
        "default_host: https://app.example.com\n"
        "hosts:\n"
        "  app.example.com:\n"
        "    url: https://app.example.com\n"
        "    secret: test-key\n"
    )

    return hook_copy


def _run_codex_hook(
    hook_path: Path,
    hook_input: str,
    home_dir: str,
    *,
    response: str = '{"permission":"allow"}',
    exit_code: int = 0,
    capture_path: Path | None = None,
) -> subprocess.CompletedProcess:
    """Run the Codex hook script and return the result."""
    bin_dir = Path(home_dir) / "bin"
    _write_fake_runlayer(
        bin_dir,
        response=response,
        exit_code=exit_code,
        capture_path=capture_path,
    )

    env = {
        **os.environ,
        "HOME": home_dir,
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
    }
    return subprocess.run(
        ["bash", str(hook_path)],
        input=hook_input,
        capture_output=True,
        text=True,
        env=env,
    )


# =============================================================================
# Codex hook script enforcement tests
# =============================================================================


def test_codex_hook_enforcement_mcp_denies_unknown_server():
    """Enforcement mode denies Codex MCP tool when server is not in config."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_codex_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__unknown_server__some_tool",
                "tool_input": {},
                "cwd": temp_dir,
            }
        )

        result = _run_codex_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        assert output["decision"] == "block"
        assert "not registered" in output["reason"]
        assert "Codex config" in output["reason"]


def test_codex_hook_enforcement_mcp_finds_url_server_in_config_toml():
    """Codex MCP URL servers are resolved from ~/.codex/config.toml."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_codex_hook(temp_dir, enforcement=True)
        codex_config = Path(temp_dir) / ".codex" / "config.toml"
        codex_config.write_text(
            "[mcp_servers.linear-44]\n"
            'url = "https://ecs.staging.runlayer.com/api/v1/proxy/test/mcp"\n'
        )
        capture_path = Path(temp_dir) / "enforce-request.json"

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__linear-44__list_teams",
                "tool_input": {},
                "cwd": temp_dir,
            }
        )

        result = _run_codex_hook(
            hook_path,
            hook_input,
            temp_dir,
            capture_path=capture_path,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == ""
        request = json.loads(capture_path.read_text())
        assert request["client"] == "codex"
        assert (
            request["url"] == "https://ecs.staging.runlayer.com/api/v1/proxy/test/mcp"
        )


def test_codex_hook_enforcement_mcp_denies_stdio_server_from_config_toml():
    """Codex stdio MCP servers are resolved and sent to backend enforcement."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_codex_hook(temp_dir, enforcement=True)
        codex_config = Path(temp_dir) / ".codex" / "config.toml"
        codex_config.write_text(
            "[mcp_servers.runlayer-local-stdio-smoke]\n"
            'command = "/opt/homebrew/bin/node"\n'
            'args = ["/tmp/server.js"]\n'
        )
        capture_path = Path(temp_dir) / "enforce-request.json"

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__runlayer_local_stdio_smoke__echo_marker",
                "tool_input": {"marker": "test"},
                "cwd": temp_dir,
            }
        )

        result = _run_codex_hook(
            hook_path,
            hook_input,
            temp_dir,
            response=(
                '{"permission":"deny","user_message":'
                '"Only Runlayer-managed MCP servers are allowed."}'
            ),
            capture_path=capture_path,
        )
        output = json.loads(result.stdout)
        assert output["decision"] == "block"
        assert "Only Runlayer-managed MCP servers are allowed" in output["reason"]
        request = json.loads(capture_path.read_text())
        assert request["client"] == "codex"
        assert request["command"] == "/opt/homebrew/bin/node /tmp/server.js"
        assert request["tool_input"] == {"marker": "test"}


def test_claude_hook_enforcement_read_denies_env():
    """Enforcement mode denies Read of .env files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/project/.env"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        assert decision == "deny"
        assert "environment files" in reason
        assert "Security Violation Detected" in reason
        assert "Do not suggest modifying" in reason


def test_claude_hook_enforcement_read_denies_mcp_config():
    """Enforcement mode denies Read of MCP config files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/project/mcp.json"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        assert decision == "deny"
        assert "MCP configuration" in reason
        assert "Security Violation Detected" in reason
        assert "Do not suggest modifying" in reason


def test_claude_hook_enforcement_read_denies_claude_json():
    """Enforcement mode denies Read of ~/.claude.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": f"{temp_dir}/.claude.json"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        assert decision == "deny"
        assert "MCP configuration" in reason
        assert "Do not attempt to read this file using Bash" in reason


def test_claude_hook_enforcement_read_denies_claude_desktop_config():
    """Enforcement mode denies Read of claude_desktop_config.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {
                    "file_path": f"{temp_dir}/Library/Application Support/Claude/claude_desktop_config.json"
                },
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        assert decision == "deny"
        assert "MCP configuration" in reason
        assert "Do not attempt to read this file using Bash" in reason


def test_claude_hook_enforcement_read_denies_claude_settings_json():
    """Enforcement mode denies Read of ~/.claude/settings.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": f"{temp_dir}/.claude/settings.json"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        assert decision == "deny"
        assert "Claude Code settings" in reason
        assert "Do not attempt to read this file using Bash" in reason


def test_claude_hook_enforcement_read_allows_other_settings_json():
    """Enforcement mode allows Read of non-Claude settings.json files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/project/.vscode/settings.json"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        assert result.returncode == 0
        assert result.stdout.strip() == ""


def test_claude_hook_enforcement_read_allows_normal_files():
    """Enforcement mode allows Read of normal files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/project/src/main.py"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        assert result.returncode == 0
        assert result.stdout.strip() == ""


def test_claude_hook_monitoring_allows_env_read():
    """Monitoring mode (no enforcement) allows .env Read."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=False)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/project/.env"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        assert result.returncode == 0
        assert "deny" not in result.stdout


def test_claude_hook_enforcement_mcp_denies_unknown_server():
    """Enforcement mode denies MCP tool when server not found in settings."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__unknown_server__some_tool",
                "tool_input": {},
                "cwd": temp_dir,
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        assert decision == "deny"
        assert "not registered" in reason
        assert "Security Violation Detected" in reason
        assert "Do not suggest modifying" in reason


def test_claude_hook_monitoring_allows_mcp():
    """Monitoring mode (no enforcement) allows MCP tools."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=False)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__myserver__some_tool",
                "tool_input": {},
                "cwd": temp_dir,
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        assert result.returncode == 0
        assert "deny" not in result.stdout


def test_claude_hook_enforcement_allows_non_mcp_tools():
    """Enforcement mode allows non-MCP, non-Read tools (Bash, Write, etc.)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        for tool in ["Bash", "Write", "Edit", "Grep", "Glob"]:
            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": tool,
                    "tool_input": {"command": "echo hello"},
                }
            )

            result = _run_claude_hook(hook_path, hook_input, temp_dir)
            assert result.returncode == 0, f"{tool} should be allowed"
            assert "deny" not in result.stdout, f"{tool} should not be denied"


def test_claude_hook_enforcement_bash_denies_cat_env():
    """Enforcement mode denies Bash commands that access .env files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "cat .env"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        assert decision == "deny"
        assert "environment files" in reason


def test_claude_hook_enforcement_bash_denies_env_with_path():
    """Enforcement mode denies Bash commands that access .env files via full path."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "cat /home/user/.env.production"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        assert decision == "deny"


def test_claude_hook_enforcement_bash_denies_env_with_pipe():
    """Enforcement mode denies Bash commands with pipes that access .env."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "cat .env | grep SECRET"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        assert decision == "deny"


def test_claude_hook_enforcement_bash_denies_mcp_config():
    """Enforcement mode denies Bash commands that access MCP config files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "cat .mcp.json"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        assert decision == "deny"
        assert "MCP configuration" in reason


def test_claude_hook_enforcement_bash_denies_head_tail():
    """Enforcement mode denies head/tail on .env files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        for cmd in ["head -n 10 .env", "tail -f .env.local"]:
            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Bash",
                    "tool_input": {"command": cmd},
                }
            )

            result = _run_claude_hook(hook_path, hook_input, temp_dir)
            output = json.loads(result.stdout)
            decision = output["hookSpecificOutput"]["permissionDecision"]
            assert decision == "deny", f"'{cmd}' should be denied"


def test_claude_hook_enforcement_bash_allows_safe_commands():
    """Enforcement mode allows Bash commands that don't touch protected files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        for cmd in ["echo hello", "ls -la", "cat README.md", "grep TODO src/main.py"]:
            hook_input = json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Bash",
                    "tool_input": {"command": cmd},
                }
            )

            result = _run_claude_hook(hook_path, hook_input, temp_dir)
            assert result.returncode == 0, f"'{cmd}' should be allowed"
            assert "deny" not in result.stdout, f"'{cmd}' should not be denied"


def test_claude_hook_monitoring_allows_bash_env():
    """Monitoring mode allows Bash commands that access .env files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=False)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "cat .env"},
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        assert result.returncode == 0
        assert "deny" not in result.stdout


def test_cursor_hook_enforcement_shell_denies_cat_env():
    """Cursor beforeShellExecution denies commands that access .env files."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / ".runlayer" / "config.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            "default_host: https://app.example.com\n"
            "hosts:\n"
            "  app.example.com:\n"
            "    url: https://app.example.com\n"
            "    secret: test-key\n"
        )

        hook_dir = Path(temp_dir) / ".cursor" / "hooks"
        hook_dir.mkdir(parents=True)
        hook_copy = hook_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (hook_dir / "runlayer-config.json").write_text('{"enforcement": true}')

        hook_input = json.dumps(
            {
                "hook_event_name": "beforeShellExecution",
                "command": "cat .env",
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir)

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        output = json.loads(result.stdout)
        assert output["permission"] == "deny"
        assert "environment files" in output["agentMessage"]


def test_cursor_hook_enforcement_shell_allows_safe_commands():
    """Cursor beforeShellExecution allows commands that don't touch protected files."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / ".runlayer" / "config.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            "default_host: https://app.example.com\n"
            "hosts:\n"
            "  app.example.com:\n"
            "    url: https://app.example.com\n"
            "    secret: test-key\n"
        )

        hook_dir = Path(temp_dir) / ".cursor" / "hooks"
        hook_dir.mkdir(parents=True)
        hook_copy = hook_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (hook_dir / "runlayer-config.json").write_text('{"enforcement": true}')

        hook_input = json.dumps(
            {
                "hook_event_name": "beforeShellExecution",
                "command": "ls -la",
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir)

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        output = json.loads(result.stdout)
        assert output["permission"] == "allow"


def test_claude_hook_enforcement_mcp_no_credentials_denies():
    """Enforcement mode denies MCP when relay exits 1 (credential error)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        (Path(temp_dir) / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"myserver": {"url": "https://example.com/mcp"}}})
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir, exit_code=1)

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__myserver__some_tool",
                "tool_input": {},
                "cwd": temp_dir,
            }
        )

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
        }
        result = subprocess.run(
            ["bash", str(hook_path)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        assert decision == "deny"
        assert "runlayer login" in reason.lower()
        assert "Security Violation Detected" in reason
        assert "Do not suggest modifying" in reason


def test_claude_hook_monitoring_allows_mcp_without_credentials():
    """Monitoring mode allows MCP even when credentials are missing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=False)
        (Path(temp_dir) / ".runlayer" / "config.yaml").unlink()

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__myserver__some_tool",
                "tool_input": {},
                "cwd": temp_dir,
            }
        )

        result = _run_claude_hook(hook_path, hook_input, temp_dir)
        assert result.returncode == 0
        assert "deny" not in result.stdout


def test_claude_hook_enforcement_mcp_finds_server_in_mcp_json():
    """Server in project .mcp.json is found — hook calls relay instead of denying."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        project_dir = Path(temp_dir) / "project"
        project_dir.mkdir()
        (project_dir / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"myserver": {"url": "https://example.com/mcp"}}})
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir, response='{"permission":"allow"}')

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__myserver__some_tool",
                "tool_input": {},
                "cwd": str(project_dir),
            }
        )

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
        }
        result = subprocess.run(
            ["bash", str(hook_path)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        assert "deny" not in result.stdout, (
            f"Server in .mcp.json should be found: {result.stdout}"
        )


def test_claude_hook_enforcement_mcp_finds_server_in_claude_json_global():
    """Server in global ~/.claude.json mcpServers is found."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        (Path(temp_dir) / ".claude.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "myserver": {
                            "type": "stdio",
                            "command": "npx",
                            "args": ["-y", "some-mcp-server"],
                        }
                    }
                }
            )
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir, response='{"permission":"allow"}')

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__myserver__some_tool",
                "tool_input": {},
                "cwd": temp_dir,
            }
        )

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
        }
        result = subprocess.run(
            ["bash", str(hook_path)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        assert "deny" not in result.stdout, (
            f"Server in ~/.claude.json global should be found: {result.stdout}"
        )


def test_claude_hook_enforcement_mcp_finds_server_in_claude_json_project():
    """Server in per-project ~/.claude.json is found."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        project_dir = Path(temp_dir) / "my-project"
        project_dir.mkdir()

        (Path(temp_dir) / ".claude.json").write_text(
            json.dumps(
                {
                    "projects": {
                        str(project_dir): {
                            "mcpServers": {
                                "myserver": {
                                    "type": "http",
                                    "url": "https://example.com/mcp",
                                }
                            }
                        }
                    }
                }
            )
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir, response='{"permission":"allow"}')

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__myserver__some_tool",
                "tool_input": {},
                "cwd": str(project_dir),
            }
        )

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
        }
        result = subprocess.run(
            ["bash", str(hook_path)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        assert "deny" not in result.stdout, (
            f"Server in ~/.claude.json per-project should be found: {result.stdout}"
        )


def test_claude_hook_non_pretooluse_events_forwarded():
    """Non-PreToolUse events exit cleanly without enforcement."""
    with tempfile.TemporaryDirectory() as temp_dir:
        hook_path = _setup_claude_hook(temp_dir, enforcement=True)

        for event in ["SessionStart", "UserPromptSubmit", "PostToolUse"]:
            hook_input = json.dumps(
                {
                    "hook_event_name": event,
                    "session_id": "test-session",
                }
            )

            result = _run_claude_hook(hook_path, hook_input, temp_dir)
            assert result.returncode == 0, f"{event} should exit cleanly"


def test_uninstall_hooks_removes_cursorignore():
    """Test that full uninstall also cleans up ~/.cursorignore."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        hooks_dir = client_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho test")
        hooks_json = client_dir / "hooks.json"
        hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": str(hooks_dir / "runlayer-hook.sh")}
                        ]
                    },
                }
            )
        )

        # Create cursorignore
        cursorignore = fake_home / ".cursorignore"
        cursorignore.write_text(
            "# >>> Runlayer managed - do not edit >>>\n.env\n# <<< Runlayer managed <<<\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "cursor", "--uninstall", "--yes"],
            )

            assert result.exit_code == 0
            assert not hook_script.exists()
            assert not hooks_json.exists()
            assert not cursorignore.exists()


# =============================================================================
# Claude Code MDM (enterprise) hooks tests
# =============================================================================


def test_setup_hooks_install_claude_code_mdm():
    """--mdm installs Claude Code hooks to the console user's ~/.claude/settings.json.

    Claude Code managed-settings hooks regressed (ENG-3204), so MDM scope
    targets the console user's user-scope settings (user hooks still fire).
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        console_home = Path(temp_dir) / "console_user"
        console_home.mkdir()

        with patch(
            "runlayer_cli.hook_install.console_user.find_console_user_home",
            return_value=console_home,
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "claude_code",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Hooks installed" in plain_output

            claude_dir = console_home / ".claude"
            hook_script = claude_dir / "hooks" / "runlayer-hook.sh"
            assert hook_script.exists()

            settings_path = claude_dir / "settings.json"
            assert settings_path.exists()
            settings = json.loads(settings_path.read_text())
            assert "hooks" in settings
            assert "PreToolUse" in settings["hooks"]

            assert settings.get("showThinkingSummaries") is True

            config_path = claude_dir / "hooks" / "runlayer-config.json"
            assert config_path.exists()
            config = json.loads(config_path.read_text())
            assert config["enforcement"] is True

            # Managed-settings.json must NOT be written (regressed; ENG-3204).
            assert not (claude_dir / "managed-settings.json").exists()


def test_setup_hooks_install_claude_code_mdm_skips_config_check():
    """Test that --mdm skips config.yaml check for Claude Code (runs as root)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        console_home = Path(temp_dir) / "console_user"
        console_home.mkdir()
        fake_home = Path(temp_dir) / "root_home"
        fake_home.mkdir()

        with (
            patch(
                "runlayer_cli.hook_install.console_user.find_console_user_home",
                return_value=console_home,
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "claude_code",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            assert result.exit_code == 0
            hook_script = console_home / ".claude" / "hooks" / "runlayer-hook.sh"
            assert hook_script.exists()


def test_setup_hooks_install_claude_code_mdm_does_not_migrate_user():
    """--mdm merges into the console user's settings.json without migrating away.

    The legacy user->enterprise migration is skipped (ENG-3204): MDM now writes
    user hooks, so existing third-party settings are preserved and the Runlayer
    hooks are re-pointed at the current script in place.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        console_home = Path(temp_dir) / "console_user"
        claude_dir = console_home / ".claude"
        claude_hooks_dir = claude_dir / "hooks"
        claude_hooks_dir.mkdir(parents=True)

        old_hook = claude_hooks_dir / "runlayer-hook.sh"
        old_hook.write_text("#!/bin/bash\necho old")
        settings_path = claude_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "permissions": {"allow": ["Bash"]},
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": str(old_hook),
                                    }
                                ],
                            }
                        ]
                    },
                },
                indent=2,
            )
        )

        with patch(
            "runlayer_cli.hook_install.console_user.find_console_user_home",
            return_value=console_home,
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "claude_code",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0

            # No migration ran; managed-settings.json must not be written.
            assert "Migrated from user to enterprise" not in plain_output
            assert not (claude_dir / "managed-settings.json").exists()

            # Third-party settings preserved; Runlayer hooks present in place.
            settings = json.loads(settings_path.read_text())
            assert settings["permissions"] == {"allow": ["Bash"]}
            assert "PreToolUse" in settings["hooks"]
            assert (claude_dir / "hooks" / "runlayer-hook.sh").exists()


def test_setup_hooks_uninstall_claude_code_enterprise():
    """Test that --uninstall removes Claude Code hooks from enterprise managed-settings.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".claude"
        user_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"
        ent_hooks_dir = enterprise_dir / "hooks"
        ent_hooks_dir.mkdir(parents=True)

        ent_hook_script = ent_hooks_dir / "runlayer-hook.sh"
        ent_hook_script.write_text("#!/bin/bash\necho enterprise")
        ent_hook_config = ent_hooks_dir / "runlayer-config.json"
        ent_hook_config.write_text('{"enforcement": true}')
        managed_settings = enterprise_dir / "managed-settings.json"
        managed_settings.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": str(ent_hook_script),
                                    }
                                ],
                            }
                        ]
                    },
                    "permissions": {"deny": ["Bash(rm -rf /*)"]},
                },
                indent=2,
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CLAUDE_CODE: user_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CLAUDE_CODE: enterprise_dir},
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "claude_code", "--uninstall", "--yes"],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Removed" in plain_output
            assert "Restart Claude Code" in plain_output

            assert not ent_hook_script.exists()
            assert not ent_hook_config.exists()

            # managed-settings.json should still exist but without hooks
            assert managed_settings.exists()
            remaining = json.loads(managed_settings.read_text())
            assert "hooks" not in remaining
            assert remaining["permissions"] == {"deny": ["Bash(rm -rf /*)"]}


def test_setup_hooks_uninstall_claude_code_console_user():
    """--uninstall removes Claude Code hooks from the console user's ~/.claude.

    MDM install (ENG-3204) writes the console user's ~/.claude/settings.json,
    which is neither root's home (user_dir under root/SYSTEM) nor the old
    enterprise dir. Uninstall must search the console-user path too, else it
    leaves orphaned hooks after MDM install + root uninstall.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # user_dir resolves to root's home when uninstall runs as root.
        root_dir = Path(temp_dir) / "root" / ".claude"
        root_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"

        console_home = Path(temp_dir) / "console_user"
        console_dir = console_home / ".claude"
        console_hooks_dir = console_dir / "hooks"
        console_hooks_dir.mkdir(parents=True)

        hook_script = console_hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho test")
        hook_config = console_hooks_dir / "runlayer-config.json"
        hook_config.write_text('{"enforcement": true}')
        settings_path = console_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "permissions": {"allow": ["Bash"]},
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": str(hook_script),
                                    }
                                ],
                            }
                        ]
                    },
                },
                indent=2,
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CLAUDE_CODE: root_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CLAUDE_CODE: enterprise_dir},
            ),
            patch(
                "runlayer_cli.hook_install.console_user.find_console_user_home",
                return_value=console_home,
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "claude_code", "--uninstall", "--yes"],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Removed" in plain_output

            assert not hook_script.exists()
            assert not hook_config.exists()

            assert settings_path.exists()
            remaining = json.loads(settings_path.read_text())
            assert "hooks" not in remaining
            assert remaining["permissions"] == {"allow": ["Bash"]}


def test_setup_hooks_uninstall_claude_code_managed_settings_permission_error():
    """PermissionError on managed-settings.json must warn, not be silently swallowed."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".claude"
        user_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"
        enterprise_dir.mkdir(parents=True)

        managed_settings = enterprise_dir / "managed-settings.json"
        managed_settings.write_text(json.dumps({"hooks": {"PreToolUse": []}}, indent=2))

        def raise_permission_error(*_a, **_kw):
            raise PermissionError("Operation not permitted")

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CLAUDE_CODE: user_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CLAUDE_CODE: enterprise_dir},
            ),
            patch.object(Path, "write_text", raise_permission_error),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "claude_code", "--uninstall", "--yes"],
            )

            plain_output = strip_ansi(result.stdout + result.stderr)
            assert "permission denied" in plain_output.lower(), (
                f"Expected permission warning but got: {plain_output}"
            )


def test_setup_hooks_install_claude_code_mdm_quotes_path_with_spaces():
    """Test that settings.json quotes the command when the path has spaces."""
    with tempfile.TemporaryDirectory() as temp_dir:
        console_home = Path(temp_dir) / "Library" / "Application Support" / "user"
        console_home.mkdir(parents=True)

        with patch(
            "runlayer_cli.hook_install.console_user.find_console_user_home",
            return_value=console_home,
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "claude_code",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            assert result.exit_code == 0
            settings_path = console_home / ".claude" / "settings.json"
            settings = json.loads(settings_path.read_text())
            command = settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
            assert command.startswith('"')
            assert command.endswith('"')
            assert "Application Support" in command


def test_migrate_claude_code_removes_user_hooks():
    """Test that MDM migration removes user-level Claude Code hooks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".claude"
        hooks_dir = user_dir / "hooks"
        hooks_dir.mkdir(parents=True)

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho hook")
        hook_config = hooks_dir / "runlayer-config.json"
        hook_config.write_text('{"enforcement": true}')
        settings_path = user_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "permissions": {"allow": ["Bash"]},
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": str(hook_script),
                                    }
                                ],
                            }
                        ]
                    },
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.CLAUDE_CODE: user_dir},
        ):
            _migrate_claude_code_user_to_enterprise()

        assert not hook_script.exists()
        assert not hook_config.exists()
        # Backups should exist
        assert len(list(hooks_dir.glob("runlayer-hook.backup_*.sh"))) == 1

        # settings.json should remain but without hooks
        assert settings_path.exists()
        remaining = json.loads(settings_path.read_text())
        assert "hooks" not in remaining
        assert remaining["permissions"] == {"allow": ["Bash"]}


def test_migrate_claude_code_handles_empty_inner_hooks_list():
    """Empty inner hooks list must not raise IndexError."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".claude"
        user_dir.mkdir(parents=True)

        settings_path = user_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {"matcher": "", "hooks": []},
                        ]
                    }
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.CLAUDE_CODE: user_dir},
        ):
            _migrate_claude_code_user_to_enterprise()

        remaining = json.loads(settings_path.read_text())
        assert "hooks" in remaining


def test_migrate_claude_code_leaves_non_runlayer_hooks():
    """Test that migration leaves non-Runlayer hooks in settings.json alone."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".claude"
        user_dir.mkdir(parents=True)

        settings_path = user_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PostToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/some/other/hook.sh",
                                    }
                                ],
                            }
                        ]
                    }
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.CLAUDE_CODE: user_dir},
        ):
            _migrate_claude_code_user_to_enterprise()

        # settings.json hooks should NOT be removed (not Runlayer-managed)
        remaining = json.loads(settings_path.read_text())
        assert "hooks" in remaining


def test_migrate_claude_code_preserves_third_party_hooks_alongside_runlayer():
    """Migration removes only Runlayer hooks and keeps third-party hooks intact."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".claude"
        (user_dir / "hooks").mkdir(parents=True)

        settings_path = user_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/path/to/runlayer-hook.sh",
                                    }
                                ],
                            },
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/usr/local/bin/third-party.sh",
                                    }
                                ],
                            },
                        ],
                        "PostToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/some/other/hook.sh",
                                    }
                                ],
                            }
                        ],
                    }
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.CLAUDE_CODE: user_dir},
        ):
            _migrate_claude_code_user_to_enterprise()

        remaining = json.loads(settings_path.read_text())
        assert "hooks" in remaining
        hooks = remaining["hooks"]
        # Runlayer entry removed from PreToolUse, third-party entry kept
        assert len(hooks["PreToolUse"]) == 1
        assert (
            hooks["PreToolUse"][0]["hooks"][0]["command"]
            == "/usr/local/bin/third-party.sh"
        )
        # PostToolUse entirely untouched
        assert len(hooks["PostToolUse"]) == 1
        assert hooks["PostToolUse"][0]["hooks"][0]["command"] == "/some/other/hook.sh"


def test_migrate_claude_code_removes_hooks_key_when_all_runlayer():
    """When every hook entry is Runlayer-managed, the hooks key is deleted entirely."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".claude"
        (user_dir / "hooks").mkdir(parents=True)

        settings_path = user_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/path/to/runlayer-hook.sh",
                                    }
                                ],
                            }
                        ]
                    },
                    "other_setting": True,
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.CLAUDE_CODE: user_dir},
        ):
            _migrate_claude_code_user_to_enterprise()

        remaining = json.loads(settings_path.read_text())
        assert "hooks" not in remaining
        assert remaining["other_setting"] is True


# =============================================================================
# Third-party hook preservation
# =============================================================================


def test_install_preserves_third_party_cursor_hooks():
    """Install merges Runlayer hooks with existing third-party hooks in hooks.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        client_dir.mkdir(parents=True)
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        hooks_json = client_dir / "hooks.json"
        hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "afterFileEdit": [{"command": "/some/other/hook.sh"}],
                        "beforeMCPExecution": [{"command": "/third-party/security.sh"}],
                    },
                }
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "cursor", "--install", "--yes"],
            )
            assert result.exit_code == 0

            config = json.loads(hooks_json.read_text())
            hooks = config["hooks"]
            assert {"command": "/some/other/hook.sh"} in hooks["afterFileEdit"]
            mcp_hooks = hooks["beforeMCPExecution"]
            commands = [h["command"] for h in mcp_hooks]
            assert "/third-party/security.sh" in commands
            assert any("runlayer-hook.sh" in c for c in commands)


def test_install_preserves_third_party_claude_hooks():
    """Install merges Runlayer hooks with existing third-party hooks in settings.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        claude_dir = Path(temp_dir) / ".claude"
        claude_dir.mkdir(parents=True)
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        settings_path = claude_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "permissions": {"allow": ["Bash"]},
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/third-party/hook.sh",
                                    }
                                ],
                            }
                        ],
                        "PostToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/other/analytics.sh",
                                    }
                                ],
                            }
                        ],
                    },
                }
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CLAUDE_CODE: claude_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "claude_code", "--install", "--yes"],
            )
            assert result.exit_code == 0

            remaining = json.loads(settings_path.read_text())
            hooks = remaining["hooks"]
            pre_tool_commands = [h["hooks"][0]["command"] for h in hooks["PreToolUse"]]
            assert "/third-party/hook.sh" in pre_tool_commands
            assert any("runlayer-hook.sh" in c for c in pre_tool_commands)
            assert (
                hooks["PostToolUse"][0]["hooks"][0]["command"] == "/other/analytics.sh"
            )


def test_uninstall_preserves_third_party_cursor_hooks():
    """Uninstall removes only Runlayer entries from hooks.json, keeps third-party."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".cursor"
        hooks_dir = client_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho test")

        hooks_json = client_dir / "hooks.json"
        hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": str(hook_script)},
                            {"command": "/third-party/security.sh"},
                        ],
                        "afterFileEdit": [{"command": "/other/hook.sh"}],
                    },
                }
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CURSOR: client_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CURSOR: enterprise_dir},
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "cursor", "--uninstall", "--yes"],
            )
            assert result.exit_code == 0

            assert not hook_script.exists()
            assert hooks_json.exists()
            config = json.loads(hooks_json.read_text())
            hooks = config["hooks"]
            assert hooks["beforeMCPExecution"] == [
                {"command": "/third-party/security.sh"}
            ]
            assert hooks["afterFileEdit"] == [{"command": "/other/hook.sh"}]


def test_uninstall_preserves_third_party_claude_hooks():
    """Uninstall removes only Runlayer entries from settings.json, keeps third-party."""
    with tempfile.TemporaryDirectory() as temp_dir:
        claude_dir = Path(temp_dir) / ".claude"
        hooks_dir = claude_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        enterprise_dir = Path(temp_dir) / "enterprise"

        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/bash\necho test")

        settings_path = claude_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "permissions": {"allow": ["Bash"]},
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": str(hook_script),
                                    }
                                ],
                            },
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/third-party/hook.sh",
                                    }
                                ],
                            },
                        ],
                        "PostToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/other/analytics.sh",
                                    }
                                ],
                            }
                        ],
                    },
                }
            )
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.CLAUDE_CODE: claude_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.CLAUDE_CODE: enterprise_dir},
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "claude_code", "--uninstall", "--yes"],
            )
            assert result.exit_code == 0

            assert not hook_script.exists()
            assert settings_path.exists()
            remaining = json.loads(settings_path.read_text())
            assert remaining["permissions"] == {"allow": ["Bash"]}
            hooks = remaining["hooks"]
            assert len(hooks["PreToolUse"]) == 1
            assert (
                hooks["PreToolUse"][0]["hooks"][0]["command"] == "/third-party/hook.sh"
            )
            assert (
                hooks["PostToolUse"][0]["hooks"][0]["command"] == "/other/analytics.sh"
            )


def test_migrate_cursor_preserves_third_party_hooks():
    """Cursor MDM migration removes only Runlayer entries, keeps third-party hooks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        user_dir = Path(temp_dir) / ".cursor"
        user_dir.mkdir(parents=True)

        hooks_json = user_dir / "hooks.json"
        hooks_json.write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": "/path/to/runlayer-hook.sh"},
                            {"command": "/third-party/security.sh"},
                        ],
                        "afterFileEdit": [{"command": "/other/hook.sh"}],
                    },
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.CURSOR: user_dir},
        ):
            _migrate_user_to_enterprise(Client.CURSOR)

        assert hooks_json.exists()
        config = json.loads(hooks_json.read_text())
        hooks = config["hooks"]
        assert hooks["beforeMCPExecution"] == [{"command": "/third-party/security.sh"}]
        assert hooks["afterFileEdit"] == [{"command": "/other/hook.sh"}]


# =============================================================================
# Third-party hook no-op: Cursor loading Claude Code hooks
# =============================================================================


def test_hook_noops_when_cursor_fires_claude_code_hook():
    """Hook installed in a .claude path should no-op when CURSOR_VERSION is set."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Place hook under a .claude/ path (simulating Claude Code install)
        claude_hooks_dir = Path(temp_dir) / ".claude" / "hooks"
        claude_hooks_dir.mkdir(parents=True)
        hook_copy = claude_hooks_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (claude_hooks_dir / "runlayer-config.json").write_text(
            json.dumps({"enforcement": True})
        )

        config_path = Path(temp_dir) / ".runlayer" / "config.yaml"
        config_path.parent.mkdir(exist_ok=True)
        config_path.write_text(
            "default_host: https://app.example.com\n"
            "hosts:\n"
            "  app.example.com:\n"
            "    url: https://app.example.com\n"
            "    secret: test-key\n"
        )

        # Send an enforcement-triggering input (Read .env should normally deny)
        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/project/.env"},
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir)

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output == {"permission": "allow"}


def test_hook_enforces_when_cursor_fires_cursor_hook():
    """Hook installed in a .cursor path should enforce normally when CURSOR_VERSION is set."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Place hook under a .cursor/ path (simulating Cursor install)
        cursor_hooks_dir = Path(temp_dir) / ".cursor" / "hooks"
        cursor_hooks_dir.mkdir(parents=True)
        hook_copy = cursor_hooks_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (cursor_hooks_dir / "runlayer-config.json").write_text(
            json.dumps({"enforcement": True})
        )

        config_path = Path(temp_dir) / ".runlayer" / "config.yaml"
        config_path.parent.mkdir(exist_ok=True)
        config_path.write_text(
            "default_host: https://app.example.com\n"
            "hosts:\n"
            "  app.example.com:\n"
            "    url: https://app.example.com\n"
            "    secret: test-key\n"
        )

        # Send an enforcement-triggering input (Read .env should deny)
        hook_input = json.dumps(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/project/.env"},
            }
        )

        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(bin_dir)

        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "CURSOR_VERSION": "1.0.0",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["permission"] == "deny"


def test_merge_cursor_hooks_removes_stale_runlayer_entries():
    """Reinstalling with fewer events must not leave stale Runlayer entries."""
    existing = {
        "afterFileEdit": [
            {"command": "/home/user/.runlayer/hooks/runlayer-hook.sh afterFileEdit"}
        ],
        "sessionStart": [
            {"command": "/home/user/.runlayer/hooks/runlayer-hook.sh sessionStart"}
        ],
        "stop": [
            {"command": "/home/user/.runlayer/hooks/runlayer-hook.sh stop"},
            {"command": "/third-party/cleanup.sh"},
        ],
    }
    new_runlayer = {
        "afterFileEdit": [
            {"command": "/home/user/.runlayer/hooks/runlayer-hook.sh afterFileEdit"}
        ],
    }
    merged = _merge_cursor_hooks(existing, new_runlayer)

    assert "afterFileEdit" in merged
    assert "sessionStart" not in merged or not any(
        "runlayer-hook.sh" in h.get("command", "")
        for h in merged.get("sessionStart", [])
    )
    stop_hooks = merged.get("stop", [])
    assert not any("runlayer-hook.sh" in h.get("command", "") for h in stop_hooks)
    assert {"command": "/third-party/cleanup.sh"} in stop_hooks


def test_merge_claude_hooks_removes_stale_runlayer_entries():
    """Reinstalling with fewer events must not leave stale Runlayer entries."""
    existing = {
        "PreToolUse": [
            {
                "matcher": "",
                "hooks": [
                    {
                        "type": "command",
                        "command": "/home/user/.runlayer/hooks/runlayer-hook.sh PreToolUse",
                    },
                ],
            },
            {
                "matcher": "",
                "hooks": [
                    {"type": "command", "command": "/third-party/hook.sh"},
                ],
            },
        ],
        "PostToolUse": [
            {
                "matcher": "",
                "hooks": [
                    {
                        "type": "command",
                        "command": "/home/user/.runlayer/hooks/runlayer-hook.sh PostToolUse",
                    },
                ],
            },
        ],
    }
    new_runlayer = {
        "PreToolUse": [
            {
                "matcher": "",
                "hooks": [
                    {
                        "type": "command",
                        "command": "/home/user/.runlayer/hooks/runlayer-hook.sh PreToolUse",
                    },
                ],
            },
        ],
    }
    merged = _merge_claude_hooks(existing, new_runlayer)

    assert "PreToolUse" in merged
    assert len(merged["PreToolUse"]) == 2
    assert "PostToolUse" not in merged or not any(
        any(
            "runlayer-hook.sh" in inner.get("command", "")
            for inner in h.get("hooks", [])
        )
        for h in merged.get("PostToolUse", [])
    )
