"""Tests for the setup hooks command."""

import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml
from typer.testing import CliRunner

from runlayer_cli import regex_safe
from runlayer_cli.commands import setup as setup_commands
from runlayer_cli.commands.setup import (
    Client,
    _generate_claude_settings,
    _install_grok_cli_hooks,
    _install_ignorefile,
    _is_runlayer_command,
    _merge_claude_hooks,
    _merge_cursor_hooks,
    _migrate_claude_code_user_to_enterprise,
    _migrate_user_to_enterprise,
    _uninstall_ignorefile,
    _uninstall_grok_cli_hooks,
)
from runlayer_cli.config import Config, HostConfig
from runlayer_cli.credential_store import KeyringCredentialStore
from runlayer_cli.hook_install.clients import (
    _vscode_user_settings_path,
    expected_event_names,
)
from runlayer_cli.main import app

runner = CliRunner()

# The bash shim is gone: ``runlayer setup hooks --install`` now registers the
# ``runlayer hook`` command from ``resolve_runlayer_hook_command()``. Pin it so
# install assertions are stable; tests needing another resolution re-patch it.
RUNLAYER_HOOK_COMMAND = "/usr/local/bin/runlayer hook"


@pytest.fixture(autouse=True)
def _stub_runlayer_hook_command(monkeypatch):
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.resolve_runlayer_hook_command",
        lambda: RUNLAYER_HOOK_COMMAND,
    )


def _expected_hook_command(client_value: str, *, enforcement: bool = True) -> str:
    command = f"{RUNLAYER_HOOK_COMMAND} --client {client_value}"
    if not enforcement:
        command = f"{command} --no-enforcement"
    return command


@pytest.mark.parametrize("include_pipeline", [False, True])
def test_operator_grok_events_match_canonical_install_contract(
    include_pipeline: bool,
) -> None:
    hooks = setup_commands._generate_grok_cli_hooks(
        RUNLAYER_HOOK_COMMAND,
        include_pipeline=include_pipeline,
    )

    assert set(hooks) == expected_event_names(
        setup_commands.HookInstallClient.GROK_CLI,
        include_pipeline=include_pipeline,
    )


def _invoke_cursor_install(tmp_path: Path, *options: str):
    client_dir = tmp_path / ".cursor"
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    runlayer_dir = fake_home / ".runlayer"
    runlayer_dir.mkdir()
    (runlayer_dir / "config.yaml").write_text(
        "default_host: https://app.runlayer.com\nhosts:\n"
        "  app.runlayer.com:\n"
        "    url: https://app.runlayer.com\n"
        "    secret: test-key\n"
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
            ["setup", "hooks", "--client", "cursor", "--install", *options, "--yes"],
        )
    return result, client_dir, fake_home


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

    def test_recognizes_runlayer_hook_command(self):
        # Operator single-binary form: the full ``runlayer`` CLI dispatching hook.
        assert _is_runlayer_command("runlayer hook --client cursor")
        assert _is_runlayer_command("/usr/local/bin/runlayer hook --client cursor")

    def test_recognizes_quoted_runlayer_hook_command(self):
        assert _is_runlayer_command(
            '"/opt/Runlayer App/runlayer" hook --client claude_code --no-enforcement'
        )

    def test_recognizes_windows_runlayer_hook_command(self):
        assert _is_runlayer_command(
            r'"C:\Program Files\Runlayer\CLI\runlayer.exe" hook --client cursor'
        )

    def test_recognizes_legacy_script_names(self):
        assert _is_runlayer_command("/old/aiwatch-hook --client cursor")

    def test_recognizes_python_module_hook_command(self):
        assert _is_runlayer_command(
            "'/opt/Runlayer CLI/bin/python' -m runlayer_cli.hook "
            "--client github-copilot-cli"
        )

    def test_ignores_empty_command(self):
        assert not _is_runlayer_command("")

    def test_ignores_third_party_command(self):
        assert not _is_runlayer_command("/usr/bin/some-other-hook --flag")


def strip_ansi(text: str) -> str:
    """Strip ANSI escape codes from text."""
    ansi_escape = regex_safe.compile(r"\x1b\[[0-9;]*m")
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
    assert "--mode" in plain_output
    assert "cursor" in plain_output.lower()
    assert "vscode" in plain_output.lower()


def test_root_help_does_not_resolve_invalid_managed_grok_home():
    script = """
from pathlib import Path
from typer.testing import CliRunner
from runlayer_cli import mdm_config
from runlayer_cli.hook_install import console_user

console_user.find_console_user_home = lambda: Path("/Users/alice")
mdm_config.read_managed_config = lambda: {"grok_home": "../outside"}

from runlayer_cli.main import app
from runlayer_cli.commands.setup import Client, _get_config_dir

result = CliRunner().invoke(app, ["--help"])
if result.exit_code != 0:
    raise SystemExit(result.exit_code)
try:
    _get_config_dir(Client.GROK_CLI, True)
except ValueError:
    pass
else:
    raise AssertionError("Grok setup did not validate managed GrokHome")
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_operator_grok_mdm_install_refuses_nested_windows_reparse_point(
    tmp_path, monkeypatch
):
    config_dir = tmp_path / "Users" / "alice" / ".grok"
    hook_path = config_dir / "hooks" / "runlayer.json"
    monkeypatch.setattr(
        setup_commands,
        "_get_config_dir",
        lambda client, mdm: config_dir,
    )
    monkeypatch.setattr(setup_commands.plat, "system", lambda: "Windows")
    monkeypatch.setattr(
        setup_commands,
        "path_has_link_or_reparse_point",
        lambda path: path == hook_path,
        raising=False,
    )
    monkeypatch.setattr(setup_commands, "reown_to_console_user", lambda _path: None)

    with pytest.raises(OSError, match="unsafe Grok CLI hooks directory"):
        _install_grok_cli_hooks(mdm=True)

    assert not hook_path.exists()


def test_operator_vscode_mdm_install_refuses_nested_windows_reparse_point(
    tmp_path, monkeypatch
):
    config_dir = tmp_path / "Users" / "alice" / ".copilot" / "hooks"
    hook_path = config_dir / "runlayer.json"
    privileged = tmp_path / "privileged-config"
    privileged.write_text("must remain unchanged")
    hook_path.parent.mkdir(parents=True)
    hook_path.symlink_to(privileged)
    monkeypatch.setattr(
        setup_commands,
        "_get_config_dir",
        lambda client, mdm: config_dir,
    )
    monkeypatch.setattr(setup_commands.plat, "system", lambda: "Windows")

    with pytest.raises(OSError, match="unsafe VS Code hooks path"):
        setup_commands._install_hooks(Client.VSCODE, True)

    assert hook_path.is_symlink()
    assert privileged.read_text() == "must remain unchanged"


def test_operator_grok_mdm_uninstall_refuses_nested_windows_reparse_point(
    tmp_path, monkeypatch
):
    user_dir = tmp_path / "current-user" / ".grok"
    mdm_dir = tmp_path / "Users" / "alice" / ".grok"
    hook_path = mdm_dir / "hooks" / "runlayer.json"
    hook_path.parent.mkdir(parents=True)
    original = json.dumps(
        {
            "hooks": {
                "PreToolUse": [
                    {
                        "hooks": [
                            {
                                "type": "command",
                                "command": "runlayer hook --client grok-cli",
                            }
                        ]
                    }
                ]
            }
        }
    )
    hook_path.write_text(original)
    monkeypatch.setitem(setup_commands.CLIENT_CONFIG_DIRS, Client.GROK_CLI, user_dir)
    monkeypatch.setattr(setup_commands, "enterprise_grok_cli_dir", lambda: mdm_dir)
    monkeypatch.setattr(setup_commands.plat, "system", lambda: "Windows")
    monkeypatch.setattr(
        setup_commands,
        "path_has_link_or_reparse_point",
        lambda path: path == hook_path,
        raising=False,
    )
    monkeypatch.setattr(setup_commands, "reown_to_console_user", lambda _path: None)

    _uninstall_grok_cli_hooks()

    assert hook_path.read_text() == original


def test_operator_grok_uninstall_continues_user_cleanup_when_managed_home_invalid(
    tmp_path, monkeypatch
):
    user_dir = tmp_path / "current-user" / ".grok"
    hook_path = user_dir / "hooks" / "runlayer.json"
    hook_path.parent.mkdir(parents=True)
    hook_path.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "runlayer hook --client grok-cli",
                                }
                            ]
                        },
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "third-party-hook",
                                }
                            ]
                        },
                    ]
                }
            }
        )
    )
    console_home = tmp_path / "ConsoleUser"
    managed = {"grok_home": str(tmp_path / "OutsideConsoleHome")}
    monkeypatch.setitem(setup_commands.CLIENT_CONFIG_DIRS, Client.GROK_CLI, user_dir)
    monkeypatch.setattr(
        "runlayer_cli.hook_install.console_user.find_console_user_home",
        lambda: console_home,
    )
    monkeypatch.setattr(
        "runlayer_cli.mdm_config.read_managed_config",
        lambda: managed,
    )

    result = runner.invoke(
        app,
        ["setup", "hooks", "--client", "grok-cli", "--uninstall", "--yes"],
    )

    assert result.exit_code == 0, result.output
    assert "managed GrokHome must stay within the console user's home" in result.output
    assert "Runlayer hooks removed from Grok CLI" in result.output
    assert json.loads(hook_path.read_text()) == {
        "hooks": {
            "PreToolUse": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "third-party-hook",
                        }
                    ]
                }
            ]
        }
    }


def test_operator_grok_uninstall_does_not_hide_unexpected_value_error(monkeypatch):
    def _raise_programming_error():
        raise ValueError("programming error")

    monkeypatch.setattr(
        setup_commands,
        "enterprise_grok_cli_dir",
        _raise_programming_error,
    )

    with pytest.raises(ValueError, match="programming error"):
        _uninstall_grok_cli_hooks()


def test_operator_mdm_install_all_reports_invalid_grok_home_and_continues(
    tmp_path, monkeypatch
):
    from runlayer_cli.hook_install.paths import enterprise_grok_cli_dir

    console_home = tmp_path / "ConsoleUser"
    managed = {"grok_home": str(tmp_path / "OutsideConsoleHome")}
    attempted: list[Client] = []

    def _fake_install(client, *_args, **_kwargs):
        attempted.append(client)
        if client == Client.GROK_CLI:
            enterprise_grok_cli_dir()

    monkeypatch.setattr(
        setup_commands,
        "client_is_installed",
        lambda client, **_kwargs: (
            client
            in {
                setup_commands.HookInstallClient.GROK_CLI,
                setup_commands.HookInstallClient.CLINE_CLI,
            }
        ),
    )
    monkeypatch.setattr(setup_commands, "_install_hooks", _fake_install)
    monkeypatch.setattr(
        "runlayer_cli.hook_install.console_user.find_console_user_home",
        lambda: console_home,
    )
    monkeypatch.setattr(
        "runlayer_cli.mdm_config.read_managed_config",
        lambda: managed,
    )

    result = runner.invoke(
        app,
        ["setup", "hooks", "--install", "--mdm", "--yes"],
    )

    assert result.exit_code == 1, result.output
    assert (
        "grok-cli: configuration invalid "
        "(managed GrokHome must stay within the console user's home)"
    ) in result.output
    assert attempted == [Client.GROK_CLI, Client.CLINE_CLI]


def test_operator_mdm_install_all_lists_invalid_grok_home_and_continues(
    tmp_path, monkeypatch
):
    from runlayer_cli.hook_install.paths import enterprise_grok_cli_dir

    console_home = tmp_path / "ConsoleUser"
    cline_dir = console_home / ".cline" / "hooks"
    managed = {"grok_home": str(tmp_path / "OutsideConsoleHome")}
    attempted: list[Client] = []

    def _fake_install(client, *_args, **_kwargs):
        attempted.append(client)
        if client == Client.GROK_CLI:
            enterprise_grok_cli_dir()

    monkeypatch.setattr(
        setup_commands,
        "client_is_installed",
        lambda client, **_kwargs: (
            client
            in {
                setup_commands.HookInstallClient.GROK_CLI,
                setup_commands.HookInstallClient.CLINE_CLI,
            }
        ),
    )
    monkeypatch.setitem(
        setup_commands.ENTERPRISE_CONFIG_DIRS, Client.CLINE_CLI, cline_dir
    )
    monkeypatch.setattr(setup_commands, "_install_hooks", _fake_install)
    monkeypatch.setattr(
        "runlayer_cli.hook_install.console_user.find_console_user_home",
        lambda: console_home,
    )
    monkeypatch.setattr(
        "runlayer_cli.mdm_config.read_managed_config",
        lambda: managed,
    )

    result = runner.invoke(
        app,
        ["setup", "hooks", "--install", "--mdm"],
        input="y\n",
    )

    assert result.exit_code == 1, result.output
    assert "This will install Runlayer hooks for all clients:" in result.output
    assert f"  - {cline_dir}/" in result.output
    assert (
        "grok-cli: configuration invalid "
        "(managed GrokHome must stay within the console user's home)"
    ) in result.output
    assert attempted == [Client.CLINE_CLI]


def test_operator_mdm_install_all_contains_invalid_grok_home_during_detection(
    tmp_path, monkeypatch
):
    from runlayer_cli.hook_install.paths import enterprise_grok_cli_dir

    console_home = tmp_path / "ConsoleUser"
    managed = {"grok_home": str(tmp_path / "OutsideConsoleHome")}
    attempted: list[Client] = []

    def _fake_is_installed(client, **_kwargs):
        if client == setup_commands.HookInstallClient.GROK_CLI:
            enterprise_grok_cli_dir()
        return client == setup_commands.HookInstallClient.CLINE_CLI

    monkeypatch.setattr(setup_commands, "client_is_installed", _fake_is_installed)
    monkeypatch.setattr(
        setup_commands,
        "_install_hooks",
        lambda client, *_args, **_kwargs: attempted.append(client),
    )
    monkeypatch.setattr(
        "runlayer_cli.hook_install.console_user.find_console_user_home",
        lambda: console_home,
    )
    monkeypatch.setattr(
        "runlayer_cli.mdm_config.read_managed_config",
        lambda: managed,
    )

    result = runner.invoke(
        app,
        ["setup", "hooks", "--install", "--mdm", "--yes"],
    )

    assert result.exit_code == 1, result.output
    assert (
        "grok-cli: configuration invalid "
        "(managed GrokHome must stay within the console user's home)"
    ) in result.output
    assert attempted == [Client.CLINE_CLI]


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


def test_setup_hooks_rejects_mode_with_legacy_no_enforcement(tmp_path):
    """Mode and its legacy compatibility flag cannot both select behavior."""
    result, _, _ = _invoke_cursor_install(
        tmp_path, "--mode", "monitor", "--no-enforcement"
    )

    assert result.exit_code != 0
    plain_output = strip_ansi(result.output)
    assert "Cannot use both --mode and --no-enforcement" in plain_output


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

            # No bash shim is written any more; the command points at the
            # in-process ``runlayer hook`` dispatch.
            assert not (client_dir / "hooks" / "runlayer-hook.sh").exists()

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
            expected = _expected_hook_command("cursor")
            assert hooks_config["hooks"]["beforeMCPExecution"][0]["command"] == expected
            assert hooks_config["hooks"]["beforeReadFile"][0]["command"] == expected
            assert hooks_config["hooks"]["beforeTabFileRead"][0]["command"] == expected
            # No sibling runtime config file any more.
            assert not (client_dir / "hooks" / "runlayer-config.json").exists()


def test_setup_hooks_install_vscode():
    """Test that legacy setup hooks installs VS Code Copilot hooks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".copilot" / "hooks"
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
                {Client.VSCODE: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "vscode",
                    "--install",
                    "--yes",
                ],
            )

        plain_output = strip_ansi(result.stdout)
        assert result.exit_code == 0
        assert "Hooks installed" in plain_output
        assert "Restart VS Code" in plain_output

        # No bash shim / RUNLAYER_HOOK_CLIENT env; client is passed via --client.
        assert not (client_dir / "hooks" / "runlayer-hook.sh").exists()

        hooks_config = json.loads((client_dir / "runlayer.json").read_text())
        assert "PreToolUse" in hooks_config["hooks"]
        assert "SessionStart" not in hooks_config["hooks"]
        # No bash/powershell keys: Copilot CLI also loads ~/.copilot/hooks/,
        # and per-shell keys would make it run these vscode entries too.
        assert hooks_config["hooks"]["PreToolUse"][0] == {
            "type": "command",
            "command": _expected_hook_command("vscode"),
        }
        settings = json.loads(
            _vscode_user_settings_path(client_dir.parent.parent).read_text()
        )
        assert settings["chat.hookFilesLocations"] == {
            "~/.copilot/hooks": True,
            ".claude/settings.json": False,
            ".claude/settings.local.json": False,
            "~/.claude/settings.json": False,
        }


def test_setup_hooks_install_vscode_no_enforcement():
    """VS Code monitoring-only install appends --no-enforcement to the command."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".copilot" / "hooks"
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
                {Client.VSCODE: client_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "vscode",
                    "--install",
                    "--no-enforcement",
                    "--yes",
                ],
            )

        assert result.exit_code == 0, result.output
        assert not (client_dir / "hooks" / "runlayer-hook.sh").exists()
        assert not (client_dir / "hooks" / "runlayer-config.json").exists()

        hooks_config = json.loads((client_dir / "runlayer.json").read_text())
        assert hooks_config["hooks"]["PreToolUse"][0] == {
            "type": "command",
            "command": _expected_hook_command("vscode", enforcement=False),
        }
        settings = json.loads(
            _vscode_user_settings_path(client_dir.parent.parent).read_text()
        )
        assert settings["chat.hookFilesLocations"]["~/.claude/settings.json"] is False


def test_setup_hooks_uninstall_vscode_cleans_hook_locations():
    """VS Code uninstall should undo settings.json hook-location changes."""
    with tempfile.TemporaryDirectory() as temp_dir:
        client_dir = Path(temp_dir) / ".copilot" / "hooks"
        client_dir.mkdir(parents=True)
        hooks_dir = client_dir / "hooks"
        hooks_dir.mkdir()
        hook_script = hooks_dir / "runlayer-hook.sh"
        hook_script.write_text("#!/bin/sh\n")
        (client_dir / "runlayer.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "type": "command",
                                "command": str(hook_script),
                                "env": {"RUNLAYER_HOOK_CLIENT": "vscode"},
                            }
                        ]
                    }
                }
            )
        )
        settings_path = _vscode_user_settings_path(client_dir.parent.parent)
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(
            json.dumps(
                {
                    "editor.tabSize": 2,
                    "chat.hookFilesLocations": {
                        "~/.copilot/hooks": True,
                        ".claude/settings.json": False,
                        ".claude/settings.local.json": False,
                        "~/.claude/settings.json": False,
                        "custom/hooks": True,
                    },
                }
            )
        )

        with patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.VSCODE: client_dir},
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "vscode", "--uninstall", "--yes"],
            )

        plain_output = strip_ansi(result.stdout)
        assert result.exit_code == 0
        assert "Runlayer hooks removed from VS Code" in plain_output
        assert not hook_script.exists()
        settings = json.loads(settings_path.read_text())
        assert settings == {
            "editor.tabSize": 2,
            "chat.hookFilesLocations": {"custom/hooks": True},
        }


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

            # Enforcement is conveyed via the command, not a sidecar config file.
            assert not (client_dir / "hooks" / "runlayer-config.json").exists()
            assert hooks_config["hooks"]["beforeMCPExecution"][0][
                "command"
            ] == _expected_hook_command("cursor")


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

            # enforcement=false is conveyed by --no-enforcement in the command.
            assert not (client_dir / "hooks" / "runlayer-config.json").exists()
            assert hooks_config["hooks"]["beforeMCPExecution"][0]["command"] == (
                _expected_hook_command("cursor", enforcement=False)
            )

            # .cursorignore should NOT be installed
            cursorignore = fake_home / ".cursorignore"
            assert not cursorignore.exists()

            # "Hierarchical Cursor Ignore" note should NOT appear
            assert "Hierarchical Cursor Ignore" not in plain_output


def test_setup_hooks_install_protect_mode(tmp_path):
    """Protect is accepted and carried into every installed hook command."""
    result, client_dir, fake_home = _invoke_cursor_install(
        tmp_path, "--mode", "protect"
    )

    assert result.exit_code == 0, result.output
    assert "Configured hooks: Protect" in strip_ansi(result.stdout)
    hooks_config = json.loads((client_dir / "hooks.json").read_text())
    assert hooks_config["hooks"]["beforeMCPExecution"][0]["command"] == (
        f"{RUNLAYER_HOOK_COMMAND} --client cursor --mode protect"
    )
    assert not (fake_home / ".cursorignore").exists()


def test_setup_hooks_install_monitor_mode_with_event_hooks(tmp_path):
    """Monitor + Sessions installs event hooks without enforcement."""
    result, client_dir, fake_home = _invoke_cursor_install(
        tmp_path, "--mode", "monitor", "--event-hooks"
    )

    assert result.exit_code == 0, result.output
    assert "Configured hooks: Monitor + event hooks" in strip_ansi(result.stdout)
    hooks_config = json.loads((client_dir / "hooks.json").read_text())
    assert "sessionStart" in hooks_config["hooks"]
    assert hooks_config["hooks"]["sessionStart"][0]["command"] == (
        f"{RUNLAYER_HOOK_COMMAND} --client cursor --mode monitor"
    )
    assert not (fake_home / ".cursorignore").exists()


def test_setup_hooks_install_enforce_mode_summary(tmp_path):
    """Explicit Enforce is named directly in the install summary."""
    result, _, _ = _invoke_cursor_install(tmp_path, "--mode", "enforce")

    assert result.exit_code == 0, result.output
    assert "Configured hooks: Enforce" in strip_ansi(result.stdout)


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

        # No bash shim / sidecar config written any more.
        assert not (hermes_dir / "agent-hooks" / "runlayer-hook.sh").exists()
        assert not (hermes_dir / "agent-hooks" / "runlayer-config.json").exists()

        config = yaml.safe_load((hermes_dir / "config.yaml").read_text())
        assert "pre_tool_call" in config["hooks"]
        assert "transform_tool_result" in config["hooks"]
        assert "post_tool_call" not in config["hooks"]
        assert config["hooks"]["pre_tool_call"][0]["command"] == _expected_hook_command(
            "hermes"
        )


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


def test_setup_hooks_install_default_enforcement_is_on():
    """Default install registers the hook command without --no-enforcement."""
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
            # No sidecar config file; enforcement is the default (no flag).
            assert not (client_dir / "hooks" / "runlayer-config.json").exists()
            hooks_config = json.loads((client_dir / "hooks.json").read_text())
            assert hooks_config["hooks"]["beforeMCPExecution"][0][
                "command"
            ] == _expected_hook_command("cursor")


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
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        cursor_dir = fake_home / ".cursor"
        vscode_dir = fake_home / ".copilot" / "hooks"
        claude_dir = fake_home / ".claude"
        codex_dir = fake_home / ".codex"
        hermes_dir = fake_home / ".hermes"
        goose_dir = fake_home / ".agents" / "plugins" / "runlayer-hooks"
        copilot_cli_dir = fake_home / ".copilot"
        windsurf_dir = fake_home / ".codeium" / "windsurf"
        qwen_code_dir = fake_home / ".qwen"
        gemini_cli_dir = fake_home / ".gemini"
        for config_dir in (
            cursor_dir,
            vscode_dir,
            claude_dir,
            codex_dir,
            hermes_dir,
            windsurf_dir,
            qwen_code_dir,
            gemini_cli_dir,
            fake_home / ".config" / "goose",
        ):
            config_dir.mkdir(parents=True)
        (cursor_dir / "mcp.json").write_text("{}")
        for vscode_mcp in (
            fake_home
            / "Library"
            / "Application Support"
            / "Code"
            / "User"
            / "mcp.json",
            fake_home / ".config" / "Code" / "User" / "mcp.json",
        ):
            vscode_mcp.parent.mkdir(parents=True)
            vscode_mcp.write_text("{}")
        (fake_home / ".claude.json").write_text("{}")
        (codex_dir / "config.toml").write_text('model = "gpt-5"\n')
        (hermes_dir / "config.yaml").write_text("model: auto\n")
        (copilot_cli_dir / "mcp-config.json").write_text("{}")
        (windsurf_dir / "mcp_config.json").write_text("{}")
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
                    Client.VSCODE: vscode_dir,
                    Client.CLAUDE_CODE: claude_dir,
                    Client.CODEX: codex_dir,
                    Client.HERMES: hermes_dir,
                    Client.GOOSE: goose_dir,
                    Client.GITHUB_COPILOT_CLI: copilot_cli_dir,
                    Client.WINDSURF: windsurf_dir,
                    Client.QWEN_CODE: qwen_code_dir,
                    Client.GEMINI_CLI: gemini_cli_dir,
                },
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
            patch(
                "runlayer_cli.commands.setup.client_is_installed",
                return_value=True,
            ),
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

            # No client writes a bash shim any more.
            assert not (cursor_dir / "hooks" / "runlayer-hook.sh").exists()
            assert not (vscode_dir / "hooks" / "runlayer-hook.sh").exists()
            assert (vscode_dir / "runlayer.json").exists()
            assert not (claude_dir / "hooks" / "runlayer-hook.sh").exists()
            assert not (codex_dir / "hooks" / "runlayer-hook.sh").exists()
            assert not (hermes_dir / "agent-hooks" / "runlayer-hook.sh").exists()
            assert not (goose_dir / "scripts" / "runlayer-hook.sh").exists()
            assert not (copilot_cli_dir / "hooks" / "runlayer-hook.sh").exists()
            assert (copilot_cli_dir / "settings.json").exists()
            copilot_cli_settings = json.loads(
                (copilot_cli_dir / "settings.json").read_text()
            )
            assert copilot_cli_settings["version"] == 1
            copilot_entries = [
                entry
                for entries in copilot_cli_settings["hooks"].values()
                for entry in entries
            ]
            expected_copilot_command = _expected_hook_command("github-copilot-cli")
            assert copilot_entries
            assert all(
                entry["bash"] == expected_copilot_command
                and entry["powershell"] == expected_copilot_command
                and "command" not in entry
                for entry in copilot_entries
            )
            windsurf_hooks = json.loads((windsurf_dir / "hooks.json").read_text())[
                "hooks"
            ]
            assert windsurf_hooks["pre_mcp_tool_use"] == [
                {"command": _expected_hook_command("windsurf")}
            ]

            assert (qwen_code_dir / "settings.json").exists()
            qwen_settings = json.loads((qwen_code_dir / "settings.json").read_text())
            qwen_commands = [
                hook["command"]
                for entries in qwen_settings["hooks"].values()
                for entry in entries
                for hook in entry["hooks"]
            ]
            assert qwen_commands
            assert all(
                command == _expected_hook_command("qwen-code")
                for command in qwen_commands
            )

            assert (gemini_cli_dir / "settings.json").exists()
            gemini_settings = json.loads((gemini_cli_dir / "settings.json").read_text())
            gemini_commands = [
                hook["command"]
                for entries in gemini_settings["hooks"].values()
                for entry in entries
                for hook in entry["hooks"]
            ]
            assert gemini_commands
            assert all(
                command == _expected_hook_command("gemini-cli")
                for command in gemini_commands
            )
            # User scope never pins the toggle; only the MDM writer does.
            assert "hooksConfig" not in gemini_settings


def test_setup_hooks_install_skips_every_client_when_none_are_installed():
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        fake_home = root / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\n"
            "hosts:\n"
            "  app.runlayer.com:\n"
            "    url: https://app.runlayer.com\n"
            "    secret: test-key\n"
        )
        client_dirs = {
            Client.CURSOR: root / ".cursor",
            Client.VSCODE: root / ".copilot" / "hooks",
            Client.CLAUDE_CODE: root / ".claude",
            Client.CODEX: root / ".codex",
            Client.HERMES: root / ".hermes",
            Client.GOOSE: root / ".agents" / "plugins" / "runlayer-hooks",
            Client.GITHUB_COPILOT_CLI: root / ".copilot-cli",
            Client.WINDSURF: root / ".codeium" / "windsurf",
            Client.GEMINI_CLI: root / ".gemini",
        }

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                client_dirs,
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
            patch("runlayer_cli.commands.setup.plat.system", return_value="Unknown"),
            patch.dict("os.environ", {"PATH": ""}, clear=False),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--install", "--yes"],
            )

        assert result.exit_code == 0, result.output
        assert all(not path.exists() for path in client_dirs.values())


def test_setup_hooks_install_ignores_runlayer_only_hermes_config():
    with tempfile.TemporaryDirectory() as temp_dir:
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\n"
            "hosts:\n"
            "  app.runlayer.com:\n"
            "    url: https://app.runlayer.com\n"
            "    secret: test-key\n"
        )
        hermes_dir = fake_home / ".hermes"
        hermes_dir.mkdir()
        config_path = hermes_dir / "config.yaml"
        original = {
            "hooks": {
                "pre_tool_call": [
                    {"command": ("/usr/local/bin/runlayer hook --client hermes")}
                ]
            }
        }
        config_path.write_text(yaml.safe_dump(original))

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {client: fake_home / f".absent-{client.value}" for client in Client}
                | {Client.HERMES: hermes_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
            patch("runlayer_cli.commands.setup.plat.system", return_value="Unknown"),
            patch.dict("os.environ", {"PATH": ""}, clear=False),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--install", "--yes"],
            )

        assert result.exit_code == 0, result.output
        assert "Restart Hermes" not in strip_ansi(result.output)
        assert yaml.safe_load(config_path.read_text()) == original
        assert not list(hermes_dir.glob("config.backup_*"))


def test_setup_hooks_install_qwen_code_uses_runlayer_command():
    with tempfile.TemporaryDirectory() as temp_dir:
        qwen_dir = Path(temp_dir) / ".qwen"
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
                {Client.QWEN_CODE: qwen_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "qwen-code", "--install", "--yes"],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Hooks installed" in plain_output
            settings = json.loads((qwen_dir / "settings.json").read_text())
            # Claude-shaped: command nested under an inner "hooks" list.
            commands = [
                inner["command"]
                for entries in settings["hooks"].values()
                for entry in entries
                for inner in entry["hooks"]
            ]
            assert commands
            assert all(
                command == _expected_hook_command("qwen-code") for command in commands
            )
            # matcher is omitted deliberately (per-event matcher semantics).
            assert all(
                "matcher" not in entry
                for entries in settings["hooks"].values()
                for entry in entries
            )


def test_setup_hooks_install_qwen_code_preserves_other_settings():
    with tempfile.TemporaryDirectory() as temp_dir:
        qwen_dir = Path(temp_dir) / ".qwen"
        qwen_dir.mkdir()
        (qwen_dir / "settings.json").write_text(
            json.dumps({"theme": "Default", "disableAllHooks": False})
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
                {Client.QWEN_CODE: qwen_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "qwen-code", "--install", "--yes"],
            )

            assert result.exit_code == 0
            settings = json.loads((qwen_dir / "settings.json").read_text())
            assert settings["theme"] == "Default"
            assert settings["disableAllHooks"] is False
            assert "PreToolUse" in settings["hooks"]


def test_setup_hooks_install_qwen_code_warns_when_hooks_globally_disabled():
    with tempfile.TemporaryDirectory() as temp_dir:
        qwen_dir = Path(temp_dir) / ".qwen"
        qwen_dir.mkdir()
        (qwen_dir / "settings.json").write_text(json.dumps({"disableAllHooks": True}))
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
                {Client.QWEN_CODE: qwen_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "qwen-code", "--install", "--yes"],
            )

            assert result.exit_code == 0
            assert "disableAllHooks" in strip_ansi(result.stdout + result.stderr)


def test_setup_hooks_uninstall_qwen_code_keeps_file_and_third_party_hooks():
    with tempfile.TemporaryDirectory() as temp_dir:
        qwen_dir = Path(temp_dir) / ".qwen"
        qwen_dir.mkdir()
        (qwen_dir / "settings.json").write_text(
            json.dumps(
                {
                    "theme": "Default",
                    "hooks": {
                        "PreToolUse": [
                            {
                                "hooks": [
                                    {"type": "command", "command": "/opt/theirs.sh"}
                                ]
                            }
                        ]
                    },
                }
            )
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
                {Client.QWEN_CODE: qwen_dir},
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_qwen_code_dir",
                return_value=qwen_dir,
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            install = runner.invoke(
                app,
                ["setup", "hooks", "--client", "qwen-code", "--install", "--yes"],
            )
            assert install.exit_code == 0

            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "qwen-code", "--uninstall", "--yes"],
            )

            assert result.exit_code == 0
            settings_path = qwen_dir / "settings.json"
            assert settings_path.exists()
            settings = json.loads(settings_path.read_text())
            assert settings["theme"] == "Default"
            commands = [
                inner["command"]
                for entry in settings["hooks"]["PreToolUse"]
                for inner in entry["hooks"]
            ]
            assert commands == ["/opt/theirs.sh"]


def test_setup_hooks_install_github_copilot_cli_uses_runlayer_command():
    with tempfile.TemporaryDirectory() as temp_dir:
        copilot_cli_dir = Path(temp_dir) / ".copilot-cli"
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
                {Client.GITHUB_COPILOT_CLI: copilot_cli_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "github-copilot-cli",
                    "--install",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Hooks installed" in plain_output
            assert not (copilot_cli_dir / "hooks" / "runlayer-hook.sh").exists()
            assert not (copilot_cli_dir / "hooks" / "runlayer-config.json").exists()
            settings = json.loads((copilot_cli_dir / "settings.json").read_text())
            entries = [
                entry for entries in settings["hooks"].values() for entry in entries
            ]
            expected_command = _expected_hook_command("github-copilot-cli")
            assert entries
            assert all(
                entry
                == {
                    "type": "command",
                    "bash": expected_command,
                    "powershell": expected_command,
                }
                for entry in entries
            )
            assert all("env" not in entry for entry in entries)


def test_setup_hooks_install_github_copilot_cli_falls_back_to_module_hook(monkeypatch):
    """No runlayer binary resolvable -> the ``python -m`` module form is wired + cleaned."""
    module_command = "'/opt/Runlayer CLI/bin/python' -m runlayer_cli.hook"
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.resolve_runlayer_hook_command",
        lambda: module_command,
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        copilot_cli_dir = Path(temp_dir) / ".copilot-cli"
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        enterprise_dir = Path(temp_dir) / "enterprise-copilot"
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.GITHUB_COPILOT_CLI: copilot_cli_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
            patch(
                "runlayer_cli.commands.setup.enterprise_github_copilot_cli_dir",
                return_value=enterprise_dir,
            ),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "github-copilot-cli",
                    "--install",
                    "--yes",
                ],
            )

            settings_path = copilot_cli_dir / "settings.json"
            assert result.exit_code == 0
            settings = json.loads(settings_path.read_text())
            entries = [
                entry for entries in settings["hooks"].values() for entry in entries
            ]
            assert entries
            assert all(
                entry["bash"] == f"{module_command} --client github-copilot-cli"
                # powershell field carries the call-operator form: the quoted
                # interpreter path would otherwise parse as an expression.
                and entry["powershell"]
                == f"& {module_command} --client github-copilot-cli"
                and "command" not in entry
                for entry in entries
            )

            uninstall_result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "github-copilot-cli",
                    "--uninstall",
                    "--yes",
                ],
            )

            assert uninstall_result.exit_code == 0
            remaining = json.loads(settings_path.read_text())
            assert "hooks" not in remaining


_UVX_FALLBACK_WARNING_MARKER = "ephemeral uv cache interpreter"


def _invoke_copilot_cli_install(temp_dir: str):
    copilot_cli_dir = Path(temp_dir) / ".copilot-cli"
    fake_home = Path(temp_dir) / "home"
    fake_home.mkdir()
    enterprise_dir = Path(temp_dir) / "enterprise-copilot"
    runlayer_dir = fake_home / ".runlayer"
    runlayer_dir.mkdir()
    (runlayer_dir / "config.yaml").write_text(
        "default_host: https://app.runlayer.com\nhosts:\n  app.runlayer.com:\n    url: https://app.runlayer.com\n    secret: test-key\n"
    )
    with (
        patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.GITHUB_COPILOT_CLI: copilot_cli_dir},
        ),
        patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        patch(
            "runlayer_cli.commands.setup.enterprise_github_copilot_cli_dir",
            return_value=enterprise_dir,
        ),
    ):
        return runner.invoke(
            app,
            [
                "setup",
                "hooks",
                "--client",
                "github-copilot-cli",
                "--install",
                "--yes",
            ],
        )


def test_setup_hooks_install_warns_when_module_fallback(monkeypatch):
    """uvx/bare-dev module fallback -> warn about evictable uv cache interpreter."""
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.runlayer_hook_command_uses_module_fallback",
        lambda: True,
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        result = _invoke_copilot_cli_install(temp_dir)
    assert result.exit_code == 0
    assert _UVX_FALLBACK_WARNING_MARKER in strip_ansi(result.output)


def test_setup_hooks_install_no_warning_when_binary_resolved(monkeypatch):
    """Frozen exe / runlayer on PATH -> no evictable-interpreter warning."""
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.runlayer_hook_command_uses_module_fallback",
        lambda: False,
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        result = _invoke_copilot_cli_install(temp_dir)
    assert result.exit_code == 0
    assert _UVX_FALLBACK_WARNING_MARKER not in strip_ansi(result.output)


def test_setup_hooks_install_github_copilot_cli_no_enforcement_sets_command_flag():
    with tempfile.TemporaryDirectory() as temp_dir:
        copilot_cli_dir = Path(temp_dir) / ".copilot-cli"
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
                {Client.GITHUB_COPILOT_CLI: copilot_cli_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "github-copilot-cli",
                    "--install",
                    "--no-enforcement",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "monitoring only (no enforcement)" in plain_output
            settings = json.loads((copilot_cli_dir / "settings.json").read_text())
            entries = [
                entry for entries in settings["hooks"].values() for entry in entries
            ]
            assert entries
            expected_command = _expected_hook_command(
                "github-copilot-cli", enforcement=False
            )
            assert all(
                entry["bash"] == expected_command
                and entry["powershell"] == expected_command
                and "command" not in entry
                for entry in entries
            )
            assert "SessionStart" in settings["hooks"]
            assert "subagentStart" in settings["hooks"]
            assert settings["hooks"]["subagentStart"][0]["env"] == {
                "HOOK_EVENT_NAME": "subagentStart"
            }
            for name, hook_entries in settings["hooks"].items():
                if name != "subagentStart":
                    assert "env" not in hook_entries[0]
            assert "SubagentStart" not in settings["hooks"]


def test_setup_hooks_install_github_copilot_cli_mdm_creates_config_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        enterprise_dir = Path(temp_dir) / "managed" / "copilot-cli"

        with (
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.GITHUB_COPILOT_CLI: enterprise_dir},
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_github_copilot_cli_dir",
                return_value=enterprise_dir,
            ),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "github-copilot-cli",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            assert result.exit_code == 0
            policy = json.loads((enterprise_dir / "runlayer.json").read_text())
            expected_command = _expected_hook_command("github-copilot-cli")
            assert policy["hooks"]["PreToolUse"][0] == {
                "type": "command",
                "bash": expected_command,
                "powershell": expected_command,
            }


_WINDSURF_EXPECTED_ENFORCEMENT_EVENTS = {
    "pre_mcp_tool_use",
    "pre_run_command",
    "pre_read_code",
}

_WINDSURF_EXPECTED_PIPELINE_EVENTS = {
    "pre_user_prompt",
    "post_mcp_tool_use",
    "post_run_command",
    "post_write_code",
    "post_cascade_response",
}


def _invoke_windsurf_install(tmp_path: Path, *options: str):
    client_dir = tmp_path / ".codeium" / "windsurf"
    fake_home = tmp_path / "home"
    fake_home.mkdir(exist_ok=True)
    runlayer_dir = fake_home / ".runlayer"
    runlayer_dir.mkdir(exist_ok=True)
    (runlayer_dir / "config.yaml").write_text(
        "default_host: https://app.runlayer.com\nhosts:\n"
        "  app.runlayer.com:\n"
        "    url: https://app.runlayer.com\n"
        "    secret: test-key\n"
    )
    with (
        patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.WINDSURF: client_dir},
        ),
        patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
    ):
        result = runner.invoke(
            app,
            ["setup", "hooks", "--client", "windsurf", "--install", *options, "--yes"],
        )
    return result, client_dir, fake_home


def _windsurf_hooks(client_dir: Path) -> dict:
    return json.loads((client_dir / "hooks.json").read_text())["hooks"]


def _invoke_windsurf_uninstall(client_dir: Path, enterprise_dir: Path):
    with (
        patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.WINDSURF: client_dir},
        ),
        patch.dict(
            "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
            {Client.WINDSURF: enterprise_dir},
        ),
    ):
        return runner.invoke(
            app,
            ["setup", "hooks", "--client", "windsurf", "--uninstall", "--yes"],
        )


def test_setup_hooks_install_windsurf(tmp_path):
    """Windsurf install writes flat command entries to the Codeium profile dir."""
    result, client_dir, _ = _invoke_windsurf_install(tmp_path)

    plain_output = strip_ansi(result.stdout)
    assert result.exit_code == 0, result.output
    assert "Hooks installed" in plain_output
    assert "enforcement only" in plain_output
    assert "Restart Windsurf" in plain_output

    config = json.loads((client_dir / "hooks.json").read_text())
    # Cascade's config carries no ``version`` key and no inner ``hooks`` list.
    assert set(config) == {"hooks"}
    assert set(config["hooks"]) == _WINDSURF_EXPECTED_ENFORCEMENT_EVENTS
    expected_entries = [{"command": _expected_hook_command("windsurf")}]
    assert all(entries == expected_entries for entries in config["hooks"].values())


def test_setup_hooks_install_windsurf_event_hooks(tmp_path):
    result, client_dir, _ = _invoke_windsurf_install(tmp_path, "--event-hooks")

    assert result.exit_code == 0, result.output
    hooks = _windsurf_hooks(client_dir)
    assert set(hooks) == (
        _WINDSURF_EXPECTED_ENFORCEMENT_EVENTS | _WINDSURF_EXPECTED_PIPELINE_EVENTS
    )
    # No canonical pre-write event exists in the normalized vocabulary.
    assert "pre_write_code" not in hooks


def test_setup_hooks_install_windsurf_no_enforcement_sets_command_flag(tmp_path):
    result, client_dir, _ = _invoke_windsurf_install(tmp_path, "--no-enforcement")

    assert result.exit_code == 0, result.output
    assert "monitoring only (no enforcement)" in strip_ansi(result.stdout)
    hooks = _windsurf_hooks(client_dir)
    expected_command = _expected_hook_command("windsurf", enforcement=False)
    assert hooks
    assert all(
        entry["command"] == expected_command
        for entries in hooks.values()
        for entry in entries
    )


def test_setup_hooks_install_windsurf_is_idempotent(tmp_path):
    """Re-install rewrites the Runlayer entries instead of appending duplicates."""
    _, client_dir, _ = _invoke_windsurf_install(tmp_path)
    first_install = _windsurf_hooks(client_dir)

    result, _, _ = _invoke_windsurf_install(tmp_path)

    assert result.exit_code == 0, result.output
    assert _windsurf_hooks(client_dir) == first_install


def test_setup_hooks_install_windsurf_preserves_third_party_hooks(tmp_path):
    client_dir = tmp_path / ".codeium" / "windsurf"
    client_dir.mkdir(parents=True)
    (client_dir / "hooks.json").write_text(
        json.dumps(
            {
                "hooks": {
                    "pre_mcp_tool_use": [
                        {"command": "/usr/local/bin/third-party-hook"}
                    ],
                    "post_cascade_response": [{"command": "/usr/local/bin/other-hook"}],
                }
            }
        )
    )

    result, _, _ = _invoke_windsurf_install(tmp_path)

    assert result.exit_code == 0, result.output
    hooks = _windsurf_hooks(client_dir)
    assert hooks["pre_mcp_tool_use"] == [
        {"command": "/usr/local/bin/third-party-hook"},
        {"command": _expected_hook_command("windsurf")},
    ]
    # Enforcement-only install leaves the untouched third-party pipeline entry.
    assert hooks["post_cascade_response"] == [{"command": "/usr/local/bin/other-hook"}]
    assert list(client_dir.glob("hooks.backup_*"))


def test_setup_hooks_install_windsurf_mdm_writes_enterprise_hooks(tmp_path):
    """Windsurf has a real system config dir, so --mdm is supported."""
    enterprise_dir = tmp_path / "managed" / "Windsurf"

    with patch.dict(
        "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
        {Client.WINDSURF: enterprise_dir},
    ):
        result = runner.invoke(
            app,
            [
                "setup",
                "hooks",
                "--client",
                "windsurf",
                "--install",
                "--mdm",
                "--yes",
            ],
        )

    assert result.exit_code == 0, result.output
    hooks = _windsurf_hooks(enterprise_dir)
    assert hooks["pre_mcp_tool_use"] == [
        {"command": _expected_hook_command("windsurf")}
    ]


def test_setup_hooks_install_windsurf_mdm_migrates_user_runlayer_hooks(tmp_path):
    user_dir = tmp_path / "home" / ".codeium" / "windsurf"
    enterprise_dir = tmp_path / "managed" / "Windsurf"
    user_dir.mkdir(parents=True)
    third_party = {"command": "/usr/local/bin/third-party-hook"}
    (user_dir / "hooks.json").write_text(
        json.dumps(
            {
                "hooks": {
                    "pre_run_command": [
                        {"command": _expected_hook_command("windsurf")},
                        third_party,
                    ],
                    "pre_read_code": [{"command": _expected_hook_command("windsurf")}],
                }
            }
        )
    )

    with (
        patch.dict(
            "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
            {Client.WINDSURF: user_dir},
        ),
        patch.dict(
            "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
            {Client.WINDSURF: enterprise_dir},
        ),
    ):
        result = runner.invoke(
            app,
            [
                "setup",
                "hooks",
                "--client",
                "windsurf",
                "--install",
                "--mdm",
                "--yes",
            ],
        )

    assert result.exit_code == 0, result.output
    assert _windsurf_hooks(user_dir) == {"pre_run_command": [third_party]}
    assert set(_windsurf_hooks(enterprise_dir)) == _WINDSURF_EXPECTED_ENFORCEMENT_EVENTS


def test_setup_hooks_uninstall_windsurf_preserves_third_party_hooks(tmp_path):
    client_dir = tmp_path / ".codeium" / "windsurf"
    client_dir.mkdir(parents=True)
    hooks_json = client_dir / "hooks.json"
    hooks_json.write_text(
        json.dumps(
            {
                "hooks": {
                    "pre_mcp_tool_use": [
                        {"command": "/usr/local/bin/third-party-hook"},
                        {"command": _expected_hook_command("windsurf")},
                    ],
                    "pre_run_command": [
                        {"command": _expected_hook_command("windsurf")}
                    ],
                }
            }
        )
    )

    result = _invoke_windsurf_uninstall(client_dir, tmp_path / "windsurf-enterprise")

    plain_output = strip_ansi(result.stdout)
    assert result.exit_code == 0, result.output
    assert "Runlayer hooks removed from Windsurf" in plain_output
    assert json.loads(hooks_json.read_text())["hooks"] == {
        "pre_mcp_tool_use": [{"command": "/usr/local/bin/third-party-hook"}]
    }


def test_setup_hooks_uninstall_windsurf_removes_runlayer_only_config(tmp_path):
    """A hooks.json holding nothing but Runlayer entries is removed outright."""
    result, client_dir, _ = _invoke_windsurf_install(tmp_path)
    assert result.exit_code == 0, result.output

    result = _invoke_windsurf_uninstall(client_dir, tmp_path / "windsurf-enterprise")

    assert result.exit_code == 0, result.output
    assert not (client_dir / "hooks.json").exists()


def test_setup_hooks_uninstall_windsurf_reports_nothing_found(tmp_path):
    result = _invoke_windsurf_uninstall(
        tmp_path / ".codeium" / "windsurf", tmp_path / "windsurf-enterprise"
    )

    assert result.exit_code == 0, result.output
    assert "No Runlayer hooks found for Windsurf" in strip_ansi(result.stdout)


def _gemini_hook_commands(settings: dict) -> list[str]:
    """Flatten the nested Gemini/Claude ``matcher`` + ``hooks`` entry shape."""
    return [
        hook["command"]
        for entries in settings["hooks"].values()
        for entry in entries
        for hook in entry["hooks"]
    ]


def test_setup_hooks_install_gemini_cli_uses_runlayer_command():
    with tempfile.TemporaryDirectory() as temp_dir:
        gemini_cli_dir = Path(temp_dir) / ".gemini"
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
                {Client.GEMINI_CLI: gemini_cli_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "gemini-cli",
                    "--install",
                    "--yes",
                ],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0
            assert "Hooks installed" in plain_output
            assert not (gemini_cli_dir / "hooks" / "runlayer-hook.sh").exists()
            settings = json.loads((gemini_cli_dir / "settings.json").read_text())
            assert set(settings["hooks"]) == {"BeforeTool", "AfterTool"}
            entry = settings["hooks"]["BeforeTool"][0]
            assert entry == {
                "matcher": "",
                "hooks": [
                    {
                        "type": "command",
                        "command": _expected_hook_command("gemini-cli"),
                    }
                ],
            }
            commands = _gemini_hook_commands(settings)
            assert commands
            assert all(
                command == _expected_hook_command("gemini-cli") for command in commands
            )
            # An absent user-scope toggle remains absent.
            assert "hooksConfig" not in settings


def test_setup_hooks_install_gemini_cli_reenables_explicitly_disabled_hooks():
    with tempfile.TemporaryDirectory() as temp_dir:
        gemini_cli_dir = Path(temp_dir) / ".gemini"
        gemini_cli_dir.mkdir()
        (gemini_cli_dir / "settings.json").write_text(
            json.dumps({"hooksConfig": {"enabled": False, "timeout": 30}})
        )
        fake_home = Path(temp_dir) / "home"
        fake_home.mkdir()
        runlayer_dir = fake_home / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://app.runlayer.com\nhosts:\n"
            "  app.runlayer.com:\n"
            "    url: https://app.runlayer.com\n"
            "    secret: test-key\n"
        )

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {Client.GEMINI_CLI: gemini_cli_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "gemini-cli",
                    "--install",
                    "--yes",
                ],
            )

            assert result.exit_code == 0, result.output
            settings = json.loads((gemini_cli_dir / "settings.json").read_text())
            assert settings["hooksConfig"] == {"enabled": True, "timeout": 30}


def test_setup_hooks_install_gemini_cli_all_events():
    with tempfile.TemporaryDirectory() as temp_dir:
        gemini_cli_dir = Path(temp_dir) / ".gemini"
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
                {Client.GEMINI_CLI: gemini_cli_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "gemini-cli",
                    "--install",
                    "--event-hooks",
                    "--yes",
                ],
            )

            assert result.exit_code == 0, result.output
            settings = json.loads((gemini_cli_dir / "settings.json").read_text())
            assert set(settings["hooks"]) == {
                "BeforeTool",
                "AfterTool",
                "SessionStart",
                "SessionEnd",
                "BeforeAgent",
                "AfterAgent",
                "Notification",
                "PreCompress",
            }
            # High-volume model round-trip events stay unregistered.
            assert "BeforeModel" not in settings["hooks"]
            assert "BeforeToolSelection" not in settings["hooks"]


def test_setup_hooks_install_gemini_cli_mdm_pins_hooks_config_enabled():
    with tempfile.TemporaryDirectory() as temp_dir:
        enterprise_dir = Path(temp_dir) / "managed" / "GeminiCli"

        with (
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.GEMINI_CLI: enterprise_dir},
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_gemini_cli_dir",
                return_value=enterprise_dir,
            ),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "gemini-cli",
                    "--install",
                    "--mdm",
                    "--yes",
                ],
            )

            assert result.exit_code == 0, result.output
            settings_path = enterprise_dir / "settings.json"
            assert settings_path.exists()
            settings = json.loads(settings_path.read_text())
            assert settings["hooksConfig"]["enabled"] is True
            commands = _gemini_hook_commands(settings)
            assert commands
            assert all(
                command == _expected_hook_command("gemini-cli") for command in commands
            )


def test_setup_hooks_install_gemini_cli_preserves_third_party_hooks():
    with tempfile.TemporaryDirectory() as temp_dir:
        gemini_cli_dir = Path(temp_dir) / ".gemini"
        gemini_cli_dir.mkdir()
        third_party_entry = {
            "matcher": "Shell",
            "hooks": [{"type": "command", "command": "/opt/other/hook"}],
        }
        (gemini_cli_dir / "settings.json").write_text(
            json.dumps(
                {
                    "security": {"auth": {"selectedType": "oauth-personal"}},
                    "hooks": {"BeforeTool": [third_party_entry]},
                }
            )
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
                {Client.GEMINI_CLI: gemini_cli_dir},
            ),
            patch("runlayer_cli.commands.setup.Path.home", return_value=fake_home),
        ):
            result = runner.invoke(
                app,
                [
                    "setup",
                    "hooks",
                    "--client",
                    "gemini-cli",
                    "--install",
                    "--yes",
                ],
            )

            assert result.exit_code == 0, result.output
            settings = json.loads((gemini_cli_dir / "settings.json").read_text())
            assert settings["security"] == {"auth": {"selectedType": "oauth-personal"}}
            assert third_party_entry in settings["hooks"]["BeforeTool"]
            assert _expected_hook_command("gemini-cli") in _gemini_hook_commands(
                settings
            )


def test_setup_hooks_uninstall_gemini_cli_keeps_third_party_and_hooks_config():
    with tempfile.TemporaryDirectory() as temp_dir:
        gemini_cli_dir = Path(temp_dir) / ".gemini"
        gemini_cli_dir.mkdir()
        third_party_entry = {
            "matcher": "Shell",
            "hooks": [{"type": "command", "command": "/opt/other/hook"}],
        }
        settings_path = gemini_cli_dir / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "hooksConfig": {"enabled": True},
                    "hooks": {
                        "BeforeTool": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": _expected_hook_command("gemini-cli"),
                                    }
                                ],
                            },
                            third_party_entry,
                        ],
                        "AfterTool": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/usr/local/bin/aiwatch-hook",
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
                {Client.GEMINI_CLI: gemini_cli_dir},
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {Client.GEMINI_CLI: Path(temp_dir) / "gemini-enterprise"},
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_gemini_cli_dir",
                return_value=Path(temp_dir) / "gemini-enterprise",
            ),
        ):
            result = runner.invoke(
                app,
                ["setup", "hooks", "--client", "gemini-cli", "--uninstall", "--yes"],
            )

            plain_output = strip_ansi(result.stdout)
            assert result.exit_code == 0, result.output
            assert "Runlayer hooks removed from Gemini CLI" in plain_output
            settings = json.loads(settings_path.read_text())
            assert settings["hooks"] == {"BeforeTool": [third_party_entry]}
            # Uninstall must not flip a toggle other hook users may rely on.
            assert settings["hooksConfig"] == {"enabled": True}


def test_setup_hooks_install_blocked_on_windows():
    """Hook install should fail immediately on Windows."""
    with tempfile.TemporaryDirectory() as temp_dir:
        cursor_dir = Path(temp_dir) / ".cursor"
        vscode_dir = Path(temp_dir) / ".copilot" / "hooks"
        claude_dir = Path(temp_dir) / ".claude"
        codex_dir = Path(temp_dir) / ".codex"
        hermes_dir = Path(temp_dir) / ".hermes"
        goose_dir = Path(temp_dir) / ".agents" / "plugins" / "runlayer-hooks"
        copilot_cli_dir = Path(temp_dir) / ".copilot-cli"
        windsurf_dir = Path(temp_dir) / ".codeium" / "windsurf"
        gemini_cli_dir = Path(temp_dir) / ".gemini"

        with (
            patch.dict(
                "runlayer_cli.commands.setup.CLIENT_CONFIG_DIRS",
                {
                    Client.CURSOR: cursor_dir,
                    Client.VSCODE: vscode_dir,
                    Client.CLAUDE_CODE: claude_dir,
                    Client.CODEX: codex_dir,
                    Client.HERMES: hermes_dir,
                    Client.GOOSE: goose_dir,
                    Client.GITHUB_COPILOT_CLI: copilot_cli_dir,
                    Client.WINDSURF: windsurf_dir,
                    Client.GEMINI_CLI: gemini_cli_dir,
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
            assert not vscode_dir.exists()
            assert not claude_dir.exists()
            assert not codex_dir.exists()
            assert not hermes_dir.exists()
            assert not goose_dir.exists()
            assert not copilot_cli_dir.exists()
            assert not windsurf_dir.exists()
            assert not gemini_cli_dir.exists()


def test_generate_claude_settings_no_shell_key():
    """Hook entries must not contain a 'shell' key (regression for PowerShell-on-bash bug)."""
    command = "/usr/local/bin/runlayer hook --client claude_code"
    settings = _generate_claude_settings(command)
    for event_name, entries in settings.items():
        for entry in entries:
            for hook in entry["hooks"]:
                assert "shell" not in hook, f"Unexpected 'shell' key in {event_name}"
                assert hook == {"type": "command", "command": command}


def test_generate_claude_settings_windows_uses_exec_form(monkeypatch):
    monkeypatch.setattr(setup_commands.plat, "system", lambda: "Windows")
    command = r'"C:\Program Files\Runlayer\CLI\runlayer.exe" hook --client claude_code'

    settings = _generate_claude_settings(command)

    assert settings["PreToolUse"][0]["hooks"][0] == {
        "type": "command",
        "command": r"C:\Program Files\Runlayer\CLI\runlayer.exe",
        "args": ["hook", "--client", "claude_code"],
    }


def test_merge_claude_hooks_recognizes_windows_exec_form(monkeypatch):
    monkeypatch.setattr(setup_commands.plat, "system", lambda: "Windows")
    command = r'"C:\Program Files\Runlayer\CLI\runlayer.exe" hook --client claude_code'
    generated = _generate_claude_settings(command)

    merged = _merge_claude_hooks(generated, generated)

    assert all(len(entries) == 1 for entries in merged.values())


def test_generate_claude_settings_hook_entries_are_independent():
    """Each event's hook entry must be a distinct dict (no shared references).

    Regression for shared-reference bug: prior impl built one hook_entry dict and
    reused it across all events, so a per-event mutation (e.g. adding "shell":
    "powershell" for Windows) would silently corrupt every other event.
    """
    settings = _generate_claude_settings(
        "/usr/local/bin/runlayer hook --client claude_code", include_pipeline=True
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

            # The legacy bash shim is removed (unlinked), not backed up.
            assert not existing_hook.exists()
            assert list(hooks_dir.glob("runlayer-hook.backup_*.sh")) == []

            # The client config (hooks.json) is still backed up before rewrite.
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

            # Verify installed to enterprise location (command, not a bash shim).
            assert not (enterprise_dir / "hooks" / "runlayer-hook.sh").exists()
            hooks_json = enterprise_dir / "hooks.json"
            assert hooks_json.exists()
            hooks_config = json.loads(hooks_json.read_text())
            assert hooks_config["hooks"]["beforeMCPExecution"][0][
                "command"
            ] == _expected_hook_command("cursor")


def test_setup_hooks_install_preserves_quoted_command(monkeypatch):
    """Installer writes the resolver's command verbatim, preserving quoting."""
    quoted_command = '"/Library/Application Support/Runlayer/runlayer" hook'
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.resolve_runlayer_hook_command",
        lambda: quoted_command,
    )
    with tempfile.TemporaryDirectory() as temp_dir:
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
            assert command == f"{quoted_command} --client cursor"
            # Quoting from the resolver is preserved verbatim.
            assert command.startswith('"')
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
            assert not (enterprise_dir / "hooks" / "runlayer-hook.sh").exists()
            assert (enterprise_dir / "hooks.json").exists()


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

            assert not (claude_dir / "hooks" / "runlayer-hook.sh").exists()
            assert not (claude_dir / "hooks" / "runlayer-config.json").exists()
            assert _expected_hook_command("claude_code") in str(
                settings["hooks"]["PreToolUse"]
            )


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

            assert not (claude_dir / "hooks" / "runlayer-hook.sh").exists()
            assert not (claude_dir / "hooks" / "runlayer-config.json").exists()
            assert _expected_hook_command("claude_code") in str(
                settings["hooks"]["PreToolUse"]
            )


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

            assert not (codex_dir / "hooks" / "runlayer-hook.sh").exists()

            hooks_json = codex_dir / "hooks.json"
            hooks_config = json.loads(hooks_json.read_text())
            assert "PreToolUse" in hooks_config["hooks"]
            assert "PermissionRequest" in hooks_config["hooks"]
            assert "Stop" not in hooks_config["hooks"]
            assert _expected_hook_command("codex") in str(
                hooks_config["hooks"]["PreToolUse"]
            )
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

            # Enforcement is conveyed via the command, not a sidecar config file.
            assert not (codex_dir / "hooks" / "runlayer-config.json").exists()


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

        vscode_dir = Path(temp_dir) / ".copilot" / "hooks"
        hermes_dir = Path(temp_dir) / ".hermes"
        goose_dir = Path(temp_dir) / ".agents" / "plugins" / "runlayer-hooks"

        windsurf_dir = Path(temp_dir) / ".codeium" / "windsurf"
        windsurf_dir.mkdir(parents=True)
        windsurf_hooks_json = windsurf_dir / "hooks.json"
        windsurf_hooks_json.write_text(
            json.dumps(
                {
                    "hooks": {
                        "pre_mcp_tool_use": [
                            {"command": _expected_hook_command("windsurf")}
                        ]
                    }
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

        gemini_cli_dir = Path(temp_dir) / ".gemini"
        gemini_cli_dir.mkdir(parents=True)
        gemini_cli_settings = gemini_cli_dir / "settings.json"
        gemini_cli_settings.write_text(
            json.dumps(
                {
                    "hooks": {
                        "BeforeTool": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": _expected_hook_command("gemini-cli"),
                                    }
                                ],
                            }
                        ]
                    }
                }
            )
        )

        qwen_code_dir = Path(temp_dir) / ".qwen"
        qwen_code_dir.mkdir(parents=True)
        qwen_code_settings = qwen_code_dir / "settings.json"
        qwen_code_settings.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": _expected_hook_command("qwen-code"),
                                    }
                                ]
                            }
                        ]
                    }
                }
            )
        )

        copilot_cli_dir = Path(temp_dir) / ".copilot-cli"
        copilot_cli_hooks_dir = copilot_cli_dir / "hooks"
        copilot_cli_hooks_dir.mkdir(parents=True)
        copilot_cli_hook_script = copilot_cli_hooks_dir / "runlayer-hook.sh"
        copilot_cli_hook_script.write_text("#!/bin/bash\necho test")
        copilot_cli_hook_config = copilot_cli_hooks_dir / "runlayer-config.json"
        copilot_cli_hook_config.write_text('{"enforcement": true}')
        copilot_cli_settings = copilot_cli_dir / "settings.json"
        copilot_cli_settings.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "type": "command",
                                "command": str(copilot_cli_hook_script),
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
                    Client.VSCODE: vscode_dir,
                    Client.CLAUDE_CODE: claude_dir,
                    Client.CODEX: codex_dir,
                    Client.HERMES: hermes_dir,
                    Client.GOOSE: goose_dir,
                    Client.GITHUB_COPILOT_CLI: copilot_cli_dir,
                    Client.WINDSURF: windsurf_dir,
                    Client.QWEN_CODE: qwen_code_dir,
                    Client.GEMINI_CLI: gemini_cli_dir,
                },
            ),
            patch.dict(
                "runlayer_cli.commands.setup.ENTERPRISE_CONFIG_DIRS",
                {
                    Client.CURSOR: cursor_enterprise_dir,
                    Client.CLAUDE_CODE: Path(temp_dir) / "claude-enterprise",
                    Client.CODEX: Path(temp_dir) / "codex-enterprise",
                    Client.GITHUB_COPILOT_CLI: Path(temp_dir) / "copilot-enterprise",
                    Client.WINDSURF: Path(temp_dir) / "windsurf-enterprise",
                    Client.GEMINI_CLI: Path(temp_dir) / "gemini-enterprise",
                },
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_vscode_dir",
                return_value=Path(temp_dir) / "vscode-enterprise",
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_claude_code_dir",
                return_value=Path(temp_dir) / "claude-enterprise-current",
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_goose_dir",
                return_value=Path(temp_dir) / "goose-enterprise",
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_github_copilot_cli_dir",
                return_value=Path(temp_dir) / "copilot-enterprise-current",
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_qwen_code_dir",
                return_value=Path(temp_dir) / "qwen-enterprise-current",
            ),
            patch(
                "runlayer_cli.commands.setup.enterprise_gemini_cli_dir",
                return_value=Path(temp_dir) / "gemini-enterprise-current",
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
            assert not copilot_cli_hook_script.exists()
            assert not copilot_cli_hook_config.exists()
            assert not copilot_cli_settings.exists()
            assert not windsurf_hooks_json.exists()
            assert qwen_code_settings.exists()
            assert "hooks" not in json.loads(qwen_code_settings.read_text())
            assert not windsurf_hooks_json.exists()
            assert not gemini_cli_settings.exists()


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

            # Install aborted: no client config written.
            assert not (client_dir / "hooks.json").exists()


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

            assert not (client_dir / "hooks" / "runlayer-hook.sh").exists()
            hooks_config = json.loads((client_dir / "hooks.json").read_text())
            assert hooks_config["hooks"]["beforeMCPExecution"][0][
                "command"
            ] == _expected_hook_command("cursor")


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

            # Enterprise hooks should exist (command, not a bash shim).
            assert not (enterprise_dir / "hooks" / "runlayer-hook.sh").exists()
            ent_json = enterprise_dir / "hooks.json"
            assert ent_json.exists()
            ent_config = json.loads(ent_json.read_text())
            assert ent_config["hooks"]["beforeMCPExecution"][0][
                "command"
            ] == _expected_hook_command("cursor")


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
    tmp_fake = bin_dir / "runlayer.tmp"
    enforce_input = (
        f"  cat > {shlex.quote(str(capture_path))}\n"
        if capture_path is not None
        else "  cat >/dev/null\n"
    )
    tmp_fake.write_text(
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
    tmp_fake.chmod(0o755)
    tmp_fake.replace(fake)


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


def test_vscode_hook_script_mcp_uses_servers_config():
    """Fallback shim enforces VS Code mcp__ tools using VS Code server config."""
    hook_src = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
    assert hook_src.exists()

    with tempfile.TemporaryDirectory() as temp_dir:
        hook_dir = Path(temp_dir) / "hooks"
        hook_dir.mkdir()
        hook_copy = hook_dir / "runlayer-hook.sh"
        hook_copy.write_text(hook_src.read_text())
        hook_copy.chmod(0o755)
        (hook_dir / "runlayer-config.json").write_text('{"enforcement": true}')

        project_dir = Path(temp_dir) / "project"
        vscode_dir = project_dir / ".vscode"
        vscode_dir.mkdir(parents=True)
        (vscode_dir / "mcp.json").write_text(
            json.dumps(
                {"servers": {"linear-44": {"url": "https://mcp.example.com/sse"}}}
            )
        )

        capture_path = Path(temp_dir) / "enforce.json"
        bin_dir = Path(temp_dir) / "bin"
        _write_fake_runlayer(
            bin_dir,
            response='{"permission":"allow"}',
            capture_path=capture_path,
        )

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__linear-44__list_teams",
                "tool_input": {"limit": 3},
                "session_id": "session-123",
                "tool_use_id": "tool-use-456",
                "cwd": str(project_dir),
            }
        )
        env = {
            **os.environ,
            "HOME": temp_dir,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "RUNLAYER_HOOK_CLIENT": "vscode",
        }
        result = subprocess.run(
            ["bash", str(hook_copy)],
            input=hook_input,
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == ""
        payload = json.loads(capture_path.read_text())
        assert payload["hook_event_name"] == "beforeMCPExecution"
        assert payload["client"] == "vscode"
        assert payload["conversation_id"] == "session-123"
        assert payload["generation_id"] == "tool-use-456"
        assert payload["tool_name"] == "mcp__linear-44__list_teams"
        assert payload["url"] == "https://mcp.example.com/sse"


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
            assert not (claude_dir / "hooks" / "runlayer-hook.sh").exists()

            settings_path = claude_dir / "settings.json"
            assert settings_path.exists()
            settings = json.loads(settings_path.read_text())
            assert "hooks" in settings
            assert "PreToolUse" in settings["hooks"]
            assert _expected_hook_command("claude_code") in str(
                settings["hooks"]["PreToolUse"]
            )

            assert settings.get("showThinkingSummaries") is True

            # Enforcement is conveyed via the command, not a sidecar config file.
            assert not (claude_dir / "hooks" / "runlayer-config.json").exists()

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
            claude_dir = console_home / ".claude"
            assert not (claude_dir / "hooks" / "runlayer-hook.sh").exists()
            assert (claude_dir / "settings.json").exists()


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

            # Third-party settings preserved; Runlayer hooks re-pointed in place.
            settings = json.loads(settings_path.read_text())
            assert settings["permissions"] == {"allow": ["Bash"]}
            assert "PreToolUse" in settings["hooks"]
            assert _expected_hook_command("claude_code") in str(
                settings["hooks"]["PreToolUse"]
            )


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


def test_setup_hooks_install_claude_code_mdm_preserves_quoted_command(monkeypatch):
    """settings.json preserves the resolver's quoting for spaced install paths."""
    quoted_command = '"/Library/Application Support/Runlayer/runlayer" hook'
    monkeypatch.setattr(
        "runlayer_cli.commands.setup.resolve_runlayer_hook_command",
        lambda: quoted_command,
    )
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
            assert command == f"{quoted_command} --client claude_code"
            # Quoting from the resolver is preserved verbatim.
            assert command.startswith('"')
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
            assert _expected_hook_command("cursor") in commands


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
            assert _expected_hook_command("claude_code") in pre_tool_commands
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
