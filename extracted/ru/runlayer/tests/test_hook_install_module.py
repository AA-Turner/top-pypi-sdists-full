"""Unit tests for ``runlayer_cli.hook_install`` (per-client writers + drift checker + tolerant JSON)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from runlayer_cli.hook_install import (
    Client,
    ClientStatus,
    InstallScope,
    ManagedPathError,
    check_absent_all,
    check_absent_client,
    check_all,
    check_client,
    install_client,
    uninstall_client,
)
import runlayer_cli.hook_install.clients as clients_module
import runlayer_cli.hook_install.check as check_module
import runlayer_cli.hook_install.paths as paths_module
from runlayer_cli.hook_install.clients import (
    _is_runlayer_command,
    _merge_claude_hooks,
    _merge_cursor_hooks,
    _merge_hermes_hooks,
    _vscode_user_settings_path,
    config_path_for,
    expected_event_names,
    hook_command_for_client,
    iter_supported_clients,
)
from runlayer_cli.hook_install.presence import client_is_installed
from runlayer_cli.tolerant_json import loads, read_dict
from runlayer_cli.scan.client_presence import DETECTION_METHOD_ORDER

# Spelled out rather than derived from the gate's own allowlist so adding a
# DetectionMethod fails here (KeyError) until someone decides whether it is
# executable-class evidence.
_EXPECTED_INSTALLED_BY_METHOD = {
    "app": True,
    "cli": True,
    "registry": True,
    "npm_global": True,
    "pip_global": False,
    "container": False,
    "config": False,
    "trace": False,
    "server": False,
    "skill": False,
    "plugin": False,
    "extension": False,
}


def _disable_host_client_probes(monkeypatch) -> None:
    from runlayer_cli.scan import client_presence

    monkeypatch.setattr(clients_module.platform, "system", lambda: "Unknown")
    monkeypatch.setattr(
        client_presence,
        "locate_cli_binary",
        lambda *_args, **_kwargs: None,
    )


def _mark_client_executable_installed(monkeypatch) -> None:
    """Seed an executable-class presence signal without using the host."""
    from runlayer_cli.scan import client_presence

    monkeypatch.setattr(
        client_presence,
        "locate_cli_binary",
        lambda *_args, **_kwargs: Path("/test/client"),
    )


# ── client presence gating ───────────────────────────────────────────


class TestClientPresenceGate:
    def test_grok_cli_home_binary_counts_as_installed(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import presence
        from runlayer_cli.scan import client_presence

        grok_binary = tmp_path / ".grok" / "bin" / "grok"
        grok_binary.parent.mkdir(parents=True)
        grok_binary.write_text("#!/bin/sh\n")
        grok_binary.chmod(0o755)
        monkeypatch.delenv("GROK_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(presence.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            client_presence,
            "locate_cli_binary",
            lambda *_args, **_kwargs: None,
        )

        assert client_is_installed(Client.GROK_CLI, scope=InstallScope.USER)

    def test_mdm_skips_every_supported_client_when_none_are_installed(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Unknown")
        monkeypatch.setattr(
            clients_module,
            "console_home_anchor",
            lambda _path, *, mdm: tmp_path if mdm else None,
        )
        monkeypatch.setenv("PATH", "")

        managed_root = tmp_path / "managed"
        for client in iter_supported_clients():
            monkeypatch.setattr(
                clients_module,
                f"enterprise_{client.value.replace('-', '_')}_dir",
                lambda client=client: managed_root / client.value,
            )

        results = [
            install_client(
                client,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch-hook",
                skip_when_missing=True,
            )
            for client in iter_supported_clients()
        ]

        assert all(
            not result.written and result.skipped_reason == "client not installed"
            for result in results
        )
        assert not managed_root.exists()

    def test_claude_code_state_file_without_executable_is_not_installed(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli.scan import client_presence

        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            client_presence,
            "locate_cli_binary",
            lambda *_args, **_kwargs: None,
        )
        (tmp_path / ".claude.json").write_text('{"numStartups": 1}')

        assert not client_is_installed(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
        )

    def test_claude_code_cursor_extension_counts_as_installed(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli.scan import client_presence

        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setenv("USERPROFILE", str(tmp_path))
        monkeypatch.setattr(
            client_presence,
            "locate_cli_binary",
            lambda *_args, **_kwargs: None,
        )
        monkeypatch.setattr(
            client_presence,
            "_windows_uninstall_entries",
            lambda *_args, **_kwargs: [],
        )
        (
            tmp_path
            / ".cursor"
            / "extensions"
            / "anthropic.claude-code-2.1.42-win32-x64"
        ).mkdir(parents=True)

        assert client_is_installed(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
        )

    def test_claude_code_wsl_extension_does_not_count_as_installed(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli.scan import client_presence

        windows_home = tmp_path / "windows-home"
        windows_home.mkdir()
        wsl_home = tmp_path / "wsl-home"
        (
            wsl_home
            / ".vscode-server"
            / "extensions"
            / "anthropic.claude-code-2.1.42-linux-x64"
        ).mkdir(parents=True)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: windows_home))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setenv("USERPROFILE", str(windows_home))
        monkeypatch.setattr(
            client_presence,
            "locate_cli_binary",
            lambda *_args, **_kwargs: None,
        )
        monkeypatch.setattr(
            client_presence,
            "_windows_uninstall_entries",
            lambda *_args, **_kwargs: [],
        )
        monkeypatch.setattr(client_presence, "_wsl_homes", lambda: [wsl_home])

        assert not client_is_installed(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
        )

    def test_config_only_does_not_mark_any_client_installed(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("COPILOT_HOME", raising=False)
        _disable_host_client_probes(monkeypatch)
        for client in iter_supported_clients():
            home = tmp_path / client.value
            home.mkdir()
            monkeypatch.setattr(
                Path,
                "home",
                classmethod(lambda cls, home=home: home),
            )

            install_client(
                client,
                scope=InstallScope.USER,
                hook_command="/usr/local/bin/aiwatch-hook",
                skip_when_missing=False,
            )

            assert not client_is_installed(
                client,
                scope=InstallScope.USER,
            ), client.value

    @pytest.mark.parametrize("method", DETECTION_METHOD_ORDER)
    def test_only_executable_detection_methods_count_as_installed(
        self, tmp_path, monkeypatch, method
    ):
        """The gate is an allowlist, so a new DetectionMethod can't opt itself in."""
        from runlayer_cli.scan import client_presence

        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(
            client_presence,
            "detect_client_presence",
            lambda definitions, **_kwargs: [
                client_presence.DetectedClient(
                    client=definitions[0].name,
                    display_name=definitions[0].display_name,
                    detected_via=[method],
                )
            ],
        )

        installed = client_is_installed(Client.CURSOR, scope=InstallScope.USER)
        assert installed is _EXPECTED_INSTALLED_BY_METHOD[method], method

    def test_windows_mdm_uses_console_user_environment(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import console_user
        from runlayer_cli.hook_install import presence

        console_home = tmp_path / "Users" / "alice"
        cursor_exe = (
            console_home / "AppData" / "Local" / "Programs" / "cursor" / "Cursor.exe"
        )
        cursor_exe.parent.mkdir(parents=True)
        cursor_exe.touch()
        monkeypatch.setattr(presence.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            console_user,
            "find_console_user_home",
            lambda: console_home,
        )
        monkeypatch.setenv(
            "LOCALAPPDATA",
            str(tmp_path / "Windows" / "System32" / "config" / "systemprofile"),
        )

        assert client_is_installed(Client.CURSOR, scope=InstallScope.MDM)

    def test_windows_mdm_detects_npm_installed_copilot_cli(self, tmp_path, monkeypatch):
        """SYSTEM's PATH never has the console user's npm shims (ENG-4814)."""
        from runlayer_cli.hook_install import console_user
        from runlayer_cli.hook_install import presence
        from runlayer_cli.scan import cli_binaries

        console_home = tmp_path / "Users" / "alice"
        copilot_cmd = console_home / "AppData" / "Roaming" / "npm" / "copilot.cmd"
        copilot_cmd.parent.mkdir(parents=True)
        copilot_cmd.write_text("@echo off\n")
        monkeypatch.setattr(presence.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            console_user,
            "find_console_user_home",
            lambda: console_home,
        )
        monkeypatch.setattr(cli_binaries.shutil, "which", lambda _binary: None)

        assert client_is_installed(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.MDM,
        )

    def test_windows_mdm_detects_npm_package_under_disguised_prefix(
        self, tmp_path, monkeypatch
    ):
        """Hook install runs no home crawl, so anchors must resolve statically."""
        from runlayer_cli.hook_install import console_user
        from runlayer_cli.hook_install import presence
        from runlayer_cli.scan import cli_binaries

        console_home = tmp_path / "Users" / "alice"
        package_dir = (
            console_home
            / "AppData"
            / "Local"
            / "PrintSpoolerCache"
            / "v2"
            / "node_modules"
            / "@openai"
            / "codex"
        )
        bin_target = package_dir / "bin" / "codex.js"
        bin_target.parent.mkdir(parents=True)
        bin_target.write_text("#!/usr/bin/env node\n")
        (package_dir / "package.json").write_text(
            json.dumps(
                {
                    "name": "@openai/codex",
                    "version": "1.2.3",
                    "bin": {"codex": "bin/codex.js"},
                }
            )
        )
        monkeypatch.setattr(presence.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            console_user,
            "find_console_user_home",
            lambda: console_home,
        )
        monkeypatch.setattr(cli_binaries.shutil, "which", lambda _binary: None)

        assert client_is_installed(Client.CODEX, scope=InstallScope.MDM)

    def test_windows_console_sid_requires_matching_profile(self, monkeypatch):
        from runlayer_cli.hook_install import presence
        from runlayer_cli.scan import windows_users

        sid = "S-1-5-21-1-2-3-1001"
        monkeypatch.setattr(windows_users, "active_session_sids", lambda: {sid: 2})
        monkeypatch.setattr(
            windows_users,
            "enumerate_real_user_profiles",
            lambda: [
                windows_users.RealUserProfile(
                    sid=sid,
                    profile_path=Path("D:/Profiles/bob"),
                    username="bob",
                )
            ],
        )

        assert presence._windows_console_user_sid(Path("C:/Users/alice")) is None


# ── _is_runlayer_command recognition ────────────────────────────────


class TestIsRunlayerCommand:
    """Both install paths must recognize each other's command forms.

    The MDM bundle path writes ``aiwatch hook --client <name>``; the operator
    path (``commands/setup.py``) writes ``runlayer hook --client <name>``. The
    filter also has to keep matching the legacy ``runlayer-hook.sh`` script name
    so re-install merge + uninstall clean up pre-migration installs.
    """

    def test_recognizes_aiwatch_hook_command(self):
        assert _is_runlayer_command("/usr/local/bin/aiwatch hook --client cursor")

    def test_recognizes_native_hook_shim_command(self):
        assert _is_runlayer_command(
            "/usr/local/lib/runlayer/aiwatch/aiwatch-hook hook --client cursor"
        )
        assert _is_runlayer_command(
            r'"C:\Program Files\Runlayer\AIWatch\aiwatch-hook.exe" '
            "hook --client cursor"
        )

    def test_recognizes_runlayer_hook_command(self):
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

    def test_recognizes_python_module_hook_command(self):
        assert _is_runlayer_command(
            "'/opt/Runlayer CLI/bin/python' -m runlayer_cli.hook --client goose"
        )

    def test_recognizes_legacy_runlayer_hook_script(self):
        assert _is_runlayer_command("/home/user/.cursor/hooks/runlayer-hook.sh")

    def test_ignores_third_party_command(self):
        assert not _is_runlayer_command("/usr/local/bin/some-other-hook --flag")
        assert not _is_runlayer_command("")

    def test_recognizes_powershell_call_operator_form(self):
        assert _is_runlayer_command(
            r'& "C:\Program Files\Runlayer\AIWatch\aiwatch.exe" '
            "hook --client claude_code"
        )
        assert _is_runlayer_command(
            r'& "C:\Program Files\Runlayer\AIWatch\aiwatch-hook.exe" '
            "hook --client claude_code"
        )


# ── Windows hook command emission ─────────────────────────────────────

# Claude Code chooses Git Bash for shell-form hooks when installed, otherwise
# PowerShell. No command string invokes a quoted executable under both shells,
# so Windows Claude Code must use its shell-free command + args form. Clients
# known to execute command strings via PowerShell still need the ``&`` form.

_WINDOWS_AIWATCH_HOOK_COMMAND = r'"C:\Program Files\Runlayer\AIWatch\aiwatch.exe" hook'


def _powershell_rejects_as_expression(command: str) -> bool:
    """True when PowerShell parses *command* as a doomed expression statement.

    A command string whose first token is a quoted string literal is parsed
    by PowerShell in expression mode; any bare token after it is a
    ParserError. This is the structural property behind the customer-reported
    ``Unexpected token 'hook' in expression or statement``.
    """
    return command.lstrip().startswith(('"', "'"))


class TestWindowsHookCommands:
    def test_windows_claude_code_uses_shell_free_exec_form(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
        )

        settings = json.loads((claude_dir / "settings.json").read_text())
        entry = settings["hooks"]["PreToolUse"][0]["hooks"][0]
        assert entry == {
            "type": "command",
            "command": r"C:\Program Files\Runlayer\AIWatch\aiwatch.exe",
            "args": ["hook", "--client", "claude_code"],
        }

    @pytest.mark.parametrize(
        "stale_command",
        [
            f"& {_WINDOWS_AIWATCH_HOOK_COMMAND} --client claude_code",
            f"{_WINDOWS_AIWATCH_HOOK_COMMAND} --client claude_code",
        ],
    )
    def test_windows_claude_code_reconcile_migrates_without_duplicates(
        self, tmp_path, monkeypatch, stale_command
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        third_party = {
            "matcher": "",
            "hooks": [{"type": "command", "command": "third-party-hook"}],
        }
        legacy = {
            "matcher": "",
            "hooks": [{"type": "command", "command": stale_command}],
        }
        (claude_dir / "settings.json").write_text(
            json.dumps({"hooks": {"PreToolUse": [third_party, legacy]}})
        )

        for _ in range(2):
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.USER,
                hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
            )

        settings = json.loads((claude_dir / "settings.json").read_text())
        assert settings["hooks"]["PreToolUse"] == [
            third_party,
            {
                "matcher": "",
                "hooks": [
                    {
                        "type": "command",
                        "command": r"C:\Program Files\Runlayer\AIWatch\aiwatch.exe",
                        "args": ["hook", "--client", "claude_code"],
                    }
                ],
            },
        ]

    def test_windows_claude_code_uninstall_removes_exec_form(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        third_party = {
            "matcher": "",
            "hooks": [{"type": "command", "command": "third-party-hook"}],
        }
        (claude_dir / "settings.json").write_text(
            json.dumps({"hooks": {"PreToolUse": [third_party]}})
        )
        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
        )
        assert (
            check_absent_client(Client.CLAUDE_CODE, scope=InstallScope.USER).status
            == ClientStatus.DRIFTED
        )

        result = uninstall_client(Client.CLAUDE_CODE, scope=InstallScope.USER)

        assert result.changed
        settings = json.loads((claude_dir / "settings.json").read_text())
        assert settings["hooks"] == {"PreToolUse": [third_party]}
        assert (
            check_absent_client(Client.CLAUDE_CODE, scope=InstallScope.USER).status
            == ClientStatus.OK
        )

    def _install_claude_code_on_windows(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
        )

    def test_windows_claude_code_install_then_check_reports_ok(
        self, tmp_path, monkeypatch
    ):
        self._install_claude_code_on_windows(tmp_path, monkeypatch)
        _mark_client_executable_installed(monkeypatch)

        result = check_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            expected_hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
            include_pipeline=False,
        )

        assert result.status == ClientStatus.OK

    @pytest.mark.parametrize(
        "stale_command",
        [
            f"& {_WINDOWS_AIWATCH_HOOK_COMMAND} --client claude_code",
            f"{_WINDOWS_AIWATCH_HOOK_COMMAND} --client claude_code",
        ],
    )
    def test_windows_claude_code_stale_shell_form_is_drifted(
        self, tmp_path, monkeypatch, stale_command
    ):
        # Both legacy shell strings must drift now that Windows requires the
        # shell-free command + args form.
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        _mark_client_executable_installed(monkeypatch)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        entry = {
            "matcher": "",
            "hooks": [{"type": "command", "command": stale_command}],
        }
        (claude_dir / "settings.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        name: [entry]
                        for name in (
                            "PreToolUse",
                            "PostToolUse",
                            "PostToolUseFailure",
                        )
                    }
                }
            )
        )

        result = check_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            expected_hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
            include_pipeline=False,
        )

        assert result.status == ClientStatus.DRIFTED

    def test_copilot_cli_powershell_field_is_not_a_powershell_expression(
        self, tmp_path, monkeypatch
    ):
        # Copilot CLI entries carry explicit per-shell commands: the
        # ``powershell`` field runs under PowerShell and needs the call
        # operator; the ``bash`` field runs under bash where ``&`` is a
        # syntax error, so it must keep the plain quoted form.
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        (copilot_dir / "mcp-config.json").write_text("{}")

        install_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
        )

        entry = json.loads((copilot_dir / "settings.json").read_text())["hooks"][
            "PreToolUse"
        ][0]
        assert not _powershell_rejects_as_expression(entry["powershell"])
        assert entry["powershell"].endswith("--client github-copilot-cli")
        assert _is_runlayer_command(entry["powershell"])
        assert entry["bash"] == (
            f"{_WINDOWS_AIWATCH_HOOK_COMMAND} --client github-copilot-cli"
        )

    def test_copilot_cli_windows_install_then_check_reports_ok(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        _mark_client_executable_installed(monkeypatch)
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        (copilot_dir / "mcp-config.json").write_text("{}")

        install_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
        )

        result = check_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            expected_hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
            include_pipeline=False,
        )

        assert result.status == ClientStatus.OK

    @pytest.mark.parametrize(
        ("client", "config_relpath", "extract"),
        [
            # Gemini CLI always executes hooks through PowerShell on Windows
            # (pwsh/powershell -Command; cmd.exe is never used).
            (
                Client.GEMINI_CLI,
                ".gemini/settings.json",
                lambda cfg: cfg["hooks"]["BeforeTool"][0]["hooks"][0]["command"],
            ),
            # VS Code Copilot chat spawns hooks with Windows PowerShell 5.1 as
            # the shell when ComSpec is the default cmd.exe.
            (
                Client.VSCODE,
                ".copilot/hooks/runlayer.json",
                lambda cfg: cfg["hooks"]["PreToolUse"][0]["command"],
            ),
            # Windsurf/Cascade docs: on Windows the ``command`` field is the
            # fallback and runs via ``powershell -Command``.
            (
                Client.WINDSURF,
                ".codeium/windsurf/hooks.json",
                lambda cfg: cfg["hooks"]["pre_mcp_tool_use"][0]["command"],
            ),
            # Codex CLI resolves the Windows session shell to PowerShell
            # (pwsh/powershell -NoProfile -Command); cmd only as last resort.
            (
                Client.CODEX,
                ".codex/hooks.json",
                lambda cfg: cfg["hooks"]["PreToolUse"][0]["hooks"][0]["command"],
            ),
        ],
    )
    def test_windows_powershell_clients_emit_parseable_commands(
        self, tmp_path, monkeypatch, client, config_relpath, extract
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.delenv("APPDATA", raising=False)
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.delenv("COPILOT_HOME", raising=False)
        (tmp_path / Path(config_relpath).parent).mkdir(parents=True, exist_ok=True)

        install_client(
            client,
            scope=InstallScope.USER,
            hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
        )

        command = extract(json.loads((tmp_path / config_relpath).read_text()))
        assert not _powershell_rejects_as_expression(command)
        assert command.endswith(f"--client {client.value}")
        assert _is_runlayer_command(command)

    @pytest.mark.parametrize(
        ("client", "config_relpath", "extract"),
        [
            # Qwen Code executes hook commands with cmd.exe (`%ComSpec% /d /s
            # /c`) by default on Windows, where a leading ``&`` is a syntax
            # error — the plain quoted form must be preserved.
            (
                Client.QWEN_CODE,
                ".qwen/settings.json",
                lambda cfg: cfg["hooks"]["PreToolUse"][0]["hooks"][0]["command"],
            ),
            # Goose runs hooks via ``sh -c`` on every platform, Windows
            # included — POSIX quoting rules, no call operator.
            (
                Client.GOOSE,
                ".agents/plugins/runlayer-hooks/hooks/hooks.json",
                lambda cfg: cfg["hooks"]["PreToolUse"][0]["hooks"][0]["command"],
            ),
        ],
    )
    def test_windows_non_powershell_clients_keep_plain_quoted_form(
        self, tmp_path, monkeypatch, client, config_relpath, extract
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.delenv("QWEN_HOME", raising=False)
        (tmp_path / Path(config_relpath).parent).mkdir(parents=True, exist_ok=True)

        install_client(
            client,
            scope=InstallScope.USER,
            hook_command=_WINDOWS_AIWATCH_HOOK_COMMAND,
        )

        command = extract(json.loads((tmp_path / config_relpath).read_text()))
        assert command == (f"{_WINDOWS_AIWATCH_HOOK_COMMAND} --client {client.value}")

    def test_posix_claude_code_command_keeps_plain_quoted_form(
        self, tmp_path, monkeypatch
    ):
        # macOS/Linux clients execute hooks via sh/bash, where a leading ``&``
        # is a syntax error — the call-operator form must stay Windows-only
        # even when the path needs quoting.
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        posix_command = '"/opt/Runlayer App/aiwatch" hook'

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            hook_command=posix_command,
        )

        settings = json.loads((claude_dir / "settings.json").read_text())
        command = settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        assert command == f"{posix_command} --client claude_code"


# ── tolerant_json ───────────────────────────────────────────────────


class TestTolerantJson:
    def test_plain_json_parses(self):
        assert loads('{"a": 1}') == {"a": 1}

    def test_line_comments_stripped(self):
        text = """
            {
                // a comment
                "a": 1
            }
        """
        assert loads(text) == {"a": 1}

    def test_trailing_commas_stripped(self):
        text = '{"a": [1, 2,], "b": {"c": 3,}}'
        assert loads(text) == {"a": [1, 2], "b": {"c": 3}}

    def test_block_comments_are_deliberately_not_tolerated(self):
        """Install-path writers reserialize what they parse, so a block-commented
        file must stay unparsed and be left untouched rather than have the user's
        comments silently dropped -- see
        TestVSCodeInstall::test_user_preserves_vscode_settings_on_parse_error.
        The read-only MCP lookup path strips them locally instead."""
        with pytest.raises(json.JSONDecodeError):
            loads('{ /* why */ "a": 1 }')

    def test_read_dict_handles_empty_string(self):
        assert read_dict("") == {}
        assert read_dict("   \n") == {}

    def test_read_dict_coerces_list_to_empty(self):
        assert read_dict("[1, 2, 3]") == {}

    def test_double_slash_inside_string_preserved_with_file_url(self):
        # ``// comment`` forces the cleanup branch; ``file:///`` inside the
        # string value must survive comment stripping.
        text = """
            {
                // a comment
                "url": "file:///Users/me/foo.txt",
            }
        """
        assert loads(text) == {"url": "file:///Users/me/foo.txt"}

    def test_double_slash_inside_string_preserved_with_unc_like_path(self):
        text = """
            {
                // a comment
                "share": "//server/share/foo",
            }
        """
        assert loads(text) == {"share": "//server/share/foo"}

    def test_double_slash_after_escaped_quote_inside_string_preserved(self):
        # Escaped quote inside the string must not flip the in-string state.
        text = r"""
            {
                // a comment
                "weird": "a\"//still-in-string"
            }
        """
        assert loads(text) == {"weird": 'a"//still-in-string'}

    def test_line_comment_after_string_value_still_stripped(self):
        text = """
            {
                "url": "file:///Users/me/foo.txt", // trailing comment
                "a": 1
            }
        """
        assert loads(text) == {"url": "file:///Users/me/foo.txt", "a": 1}


# ── Cursor install ──────────────────────────────────────────────────


class TestCursorInstall:
    def test_writes_hooks_json_into_user_cursor_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()

        result = install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        hooks_json = cursor_dir / "hooks.json"
        data = json.loads(hooks_json.read_text())
        assert data["version"] == 1
        assert "beforeMCPExecution" in data["hooks"]
        assert data["hooks"]["beforeMCPExecution"][0]["command"].endswith(
            "aiwatch-hook --client cursor"
        )
        # Enforcement now lives in MDM managed config; the install path no
        # longer writes a sibling runlayer-config.json file.
        assert not (cursor_dir / "hooks" / "runlayer-config.json").exists()

    def test_user_skip_when_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _disable_host_client_probes(monkeypatch)

        result = install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
            skip_when_missing=True,
        )

        assert not result.written
        assert result.skipped_reason == "client not installed"
        assert not (tmp_path / ".cursor").exists()

    def test_user_idempotent_repeat_writes_match(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        first = (tmp_path / ".cursor" / "hooks.json").read_text()

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        second = (tmp_path / ".cursor" / "hooks.json").read_text()

        assert first == second

    def test_user_preserves_third_party_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()

        third_party_command = "/usr/local/bin/some-other-tool"
        (cursor_dir / "hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [{"command": third_party_command}],
                    },
                }
            )
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        data = json.loads((cursor_dir / "hooks.json").read_text())
        commands = [entry["command"] for entry in data["hooks"]["beforeMCPExecution"]]
        assert third_party_command in commands
        assert any(c.endswith("aiwatch-hook --client cursor") for c in commands)

    def test_user_replaces_stale_runlayer_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()

        (cursor_dir / "hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": "/old/path/aiwatch-hook"},
                            {"command": "/usr/local/bin/aiwatch-enforce"},
                        ],
                    },
                }
            )
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/new/path/aiwatch-hook",
            skip_when_missing=False,
        )

        data = json.loads((cursor_dir / "hooks.json").read_text())
        commands = [entry["command"] for entry in data["hooks"]["beforeMCPExecution"]]
        assert commands == ["/new/path/aiwatch-hook --client cursor"]


# ── VS Code install ──────────────────────────────────────────────────


class TestVSCodeInstall:
    def test_user_writes_copilot_hook_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        code_dir = tmp_path / "Library" / "Application Support" / "Code"
        code_dir.mkdir(parents=True)

        result = install_client(
            Client.VSCODE,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        hooks_json = tmp_path / ".copilot" / "hooks" / "runlayer.json"
        data = json.loads(hooks_json.read_text())
        assert "PreToolUse" in data["hooks"]
        first_entry = data["hooks"]["PreToolUse"][0]
        # No bash/powershell keys: Copilot CLI also loads ~/.copilot/hooks/,
        # and per-shell keys would make it run these vscode entries too.
        assert first_entry == {
            "type": "command",
            "command": "/usr/local/bin/aiwatch-hook --client vscode",
        }
        settings = json.loads(_vscode_user_settings_path(tmp_path).read_text())
        assert settings["chat.hookFilesLocations"] == {
            "~/.copilot/hooks": True,
            ".claude/settings.json": False,
            ".claude/settings.local.json": False,
            "~/.claude/settings.json": False,
        }
        assert "SessionStart" not in data["hooks"]

    def test_user_preserves_vscode_settings_on_parse_error(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        settings_path = _vscode_user_settings_path(tmp_path)
        settings_path.parent.mkdir(parents=True)
        existing = '{\n  /* block comment */\n  "editor.tabSize": 2\n}\n'
        settings_path.write_text(existing)

        result = install_client(
            Client.VSCODE,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        assert settings_path.read_text() == existing

    def test_user_include_pipeline_registers_documented_events(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".vscode").mkdir()

        install_client(
            Client.VSCODE,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = json.loads(
            (tmp_path / ".copilot" / "hooks" / "runlayer.json").read_text()
        )["hooks"]
        for name in ("SessionStart", "UserPromptSubmit", "Stop", "PreCompact"):
            assert name in hooks

    def test_user_preserves_third_party_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        vscode_dir = tmp_path / ".copilot" / "hooks"
        vscode_dir.mkdir(parents=True)
        third_party_command = "/usr/local/bin/some-other-tool"
        (vscode_dir / "runlayer.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {"type": "command", "command": third_party_command}
                        ],
                    },
                }
            )
        )

        install_client(
            Client.VSCODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        data = json.loads((vscode_dir / "runlayer.json").read_text())
        commands = [entry["command"] for entry in data["hooks"]["PreToolUse"]]
        assert third_party_command in commands
        assert any(c.endswith("aiwatch-hook --client vscode") for c in commands)


# ── GitHub Copilot CLI install ───────────────────────────────────────


class TestGitHubCopilotCLIInstall:
    def test_user_writes_copilot_settings_json(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        (copilot_dir / "mcp-config.json").write_text("{}")

        result = install_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        settings = json.loads((copilot_dir / "settings.json").read_text())
        assert settings["version"] == 1
        assert "PreToolUse" in settings["hooks"]
        first_entry = settings["hooks"]["PreToolUse"][0]
        assert first_entry == {
            "type": "command",
            "bash": "/usr/local/bin/aiwatch-hook --client github-copilot-cli",
            "powershell": "/usr/local/bin/aiwatch-hook --client github-copilot-cli",
        }
        assert "SessionStart" not in settings["hooks"]

    def test_user_detects_fresh_copilot_config_json(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        (copilot_dir / "config.json").write_text("{}")

        result = install_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        settings = json.loads((copilot_dir / "settings.json").read_text())
        assert "PreToolUse" in settings["hooks"]

    def test_user_include_pipeline_registers_session_events(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        (copilot_dir / "mcp-config.json").write_text("{}")

        install_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = json.loads((tmp_path / ".copilot" / "settings.json").read_text())[
            "hooks"
        ]
        for name in (
            "SessionStart",
            "SessionEnd",
            "UserPromptSubmit",
            "subagentStart",
            "Stop",
            "ErrorOccurred",
        ):
            assert name in hooks
        assert "SubagentStart" not in hooks
        assert hooks["subagentStart"][0]["env"] == {"HOOK_EVENT_NAME": "subagentStart"}
        for name, entries in hooks.items():
            if name != "subagentStart":
                assert "env" not in entries[0]

    def test_mdm_creates_copilot_policy_dir(self, tmp_path, monkeypatch):
        policy_dir = tmp_path / "managed" / "copilot-cli"
        monkeypatch.setattr(
            clients_module,
            "enterprise_github_copilot_cli_dir",
            lambda: policy_dir,
        )

        result = install_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.MDM,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        assert result.config_path == policy_dir / "runlayer.json"
        policy = json.loads((policy_dir / "runlayer.json").read_text())
        assert policy["hooks"]["PreToolUse"][0] == {
            "type": "command",
            "bash": "/usr/local/bin/aiwatch-hook --client github-copilot-cli",
            "powershell": "/usr/local/bin/aiwatch-hook --client github-copilot-cli",
        }

    def test_user_preserves_existing_settings_and_third_party_hooks(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        third_party_command = "/usr/local/bin/some-other-tool"
        (copilot_dir / "settings.json").write_text(
            json.dumps(
                {
                    "theme": "dark",
                    "hooks": {
                        "PreToolUse": [
                            {"type": "command", "command": third_party_command},
                            {
                                "type": "command",
                                "command": (
                                    "/old/path/aiwatch-hook --client github-copilot-cli"
                                ),
                            },
                        ],
                    },
                }
            )
        )

        install_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        data = json.loads((copilot_dir / "settings.json").read_text())
        assert data["theme"] == "dark"
        assert data["version"] == 1
        assert data["hooks"]["PreToolUse"] == [
            {"type": "command", "command": third_party_command},
            {
                "type": "command",
                "bash": "/usr/local/bin/aiwatch-hook --client github-copilot-cli",
                "powershell": (
                    "/usr/local/bin/aiwatch-hook --client github-copilot-cli"
                ),
            },
        ]

    def test_reinstall_replaces_shell_specific_runlayer_entries(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        (copilot_dir / "mcp-config.json").write_text("{}")

        for _ in range(2):
            install_client(
                Client.GITHUB_COPILOT_CLI,
                scope=InstallScope.USER,
                hook_command="/usr/local/bin/aiwatch-hook",
            )

        hooks = json.loads((copilot_dir / "settings.json").read_text())["hooks"]
        assert hooks["PreToolUse"] == [
            {
                "type": "command",
                "bash": "/usr/local/bin/aiwatch-hook --client github-copilot-cli",
                "powershell": (
                    "/usr/local/bin/aiwatch-hook --client github-copilot-cli"
                ),
            }
        ]

    def test_user_skip_when_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _disable_host_client_probes(monkeypatch)

        result = install_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
            skip_when_missing=True,
        )

        assert not result.written
        assert result.skipped_reason == "client not installed"
        assert not (tmp_path / ".copilot").exists()

    def test_user_reports_ok_when_command_matches(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        (copilot_dir / "mcp-config.json").write_text("{}")
        install_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        result = check_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )

        assert result.status == ClientStatus.OK

    def test_user_reports_legacy_command_format_as_drifted(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        command = "/usr/local/bin/aiwatch-hook --client github-copilot-cli"
        legacy_entry = {"type": "command", "command": command}
        (copilot_dir / "settings.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        event: [legacy_entry]
                        for event in (
                            "PreToolUse",
                            "PostToolUse",
                            "PostToolUseFailure",
                            "PermissionRequest",
                        )
                    },
                }
            )
        )

        result = check_client(
            Client.GITHUB_COPILOT_CLI,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )

        assert result.status == ClientStatus.DRIFTED
        assert result.detail == "Runlayer hook entry lacks bash/powershell commands"


# ── Gemini CLI install ───────────────────────────────────────────────

_GEMINI_HOOK_COMMAND = "/usr/local/bin/aiwatch-hook"
_GEMINI_EXPECTED_COMMAND = f"{_GEMINI_HOOK_COMMAND} --client gemini-cli"
_GEMINI_PIPELINE_EVENTS = (
    "SessionStart",
    "SessionEnd",
    "BeforeAgent",
    "AfterAgent",
    "Notification",
    "PreCompress",
)


def _gemini_settings(gemini_dir: Path) -> dict:
    return json.loads((gemini_dir / "settings.json").read_text())


def _gemini_commands(settings: dict) -> list[str]:
    """Flatten Gemini's nested (Claude-shaped) ``matcher`` + ``hooks`` entries."""
    return [
        hook["command"]
        for entries in settings["hooks"].values()
        for entry in entries
        for hook in entry["hooks"]
    ]


class TestGeminiCLIInstall:
    def test_user_writes_settings_json_with_nested_enforcement_entries(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        gemini_dir = tmp_path / ".gemini"
        gemini_dir.mkdir()

        result = install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command=_GEMINI_HOOK_COMMAND,
        )

        assert result.written
        assert result.config_path == gemini_dir / "settings.json"
        settings = _gemini_settings(gemini_dir)
        assert set(settings["hooks"]) == {"BeforeTool", "AfterTool"}
        for event in ("BeforeTool", "AfterTool"):
            assert settings["hooks"][event] == [
                {
                    "matcher": "",
                    "hooks": [{"type": "command", "command": _GEMINI_EXPECTED_COMMAND}],
                }
            ]
        for event in _GEMINI_PIPELINE_EVENTS:
            assert event not in settings["hooks"]

    def test_user_include_pipeline_registers_all_eight_events(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        gemini_dir = tmp_path / ".gemini"
        gemini_dir.mkdir()

        install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command=_GEMINI_HOOK_COMMAND,
        )

        hooks = _gemini_settings(gemini_dir)["hooks"]
        assert set(hooks) == {"BeforeTool", "AfterTool", *_GEMINI_PIPELINE_EVENTS}
        # Model round-trip events carry the full message list; deliberately unwired.
        for event in ("BeforeModel", "AfterModel", "BeforeToolSelection"):
            assert event not in hooks

    def test_user_scope_does_not_set_hooks_config(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".gemini").mkdir()

        install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            hook_command=_GEMINI_HOOK_COMMAND,
        )

        assert "hooksConfig" not in _gemini_settings(tmp_path / ".gemini")

    def test_user_scope_reenables_explicitly_disabled_hooks(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        gemini_dir = tmp_path / ".gemini"
        gemini_dir.mkdir()
        (gemini_dir / "settings.json").write_text(
            json.dumps({"hooksConfig": {"enabled": False, "timeout": 30}})
        )

        install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            hook_command=_GEMINI_HOOK_COMMAND,
        )

        assert _gemini_settings(gemini_dir)["hooksConfig"] == {
            "enabled": True,
            "timeout": 30,
        }

    def test_mdm_writes_enterprise_settings_and_pins_hooks_config(
        self, tmp_path, monkeypatch
    ):
        enterprise_dir = tmp_path / "managed" / "GeminiCli"
        monkeypatch.setattr(
            clients_module,
            "enterprise_gemini_cli_dir",
            lambda: enterprise_dir,
        )

        result = install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.MDM,
            include_pipeline=False,
            hook_command=_GEMINI_HOOK_COMMAND,
        )

        assert result.written
        assert result.config_path == enterprise_dir / "settings.json"
        settings = _gemini_settings(enterprise_dir)
        # System settings outrank user settings, so the toggle is pinned on to
        # stop a user disabling every Runlayer hook from ~/.gemini.
        assert settings["hooksConfig"]["enabled"] is True
        assert set(settings["hooks"]) == {"BeforeTool", "AfterTool"}
        assert _gemini_commands(settings) == [
            _GEMINI_EXPECTED_COMMAND,
            _GEMINI_EXPECTED_COMMAND,
        ]

    def test_mdm_preserves_existing_hooks_config_keys(self, tmp_path, monkeypatch):
        enterprise_dir = tmp_path / "managed" / "GeminiCli"
        enterprise_dir.mkdir(parents=True)
        (enterprise_dir / "settings.json").write_text(
            json.dumps({"hooksConfig": {"enabled": False, "timeout": 30}})
        )
        monkeypatch.setattr(
            clients_module,
            "enterprise_gemini_cli_dir",
            lambda: enterprise_dir,
        )

        install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.MDM,
            hook_command=_GEMINI_HOOK_COMMAND,
        )

        hooks_config = _gemini_settings(enterprise_dir)["hooksConfig"]
        assert hooks_config == {"enabled": True, "timeout": 30}

    def test_user_preserves_third_party_hook_entry(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        gemini_dir = tmp_path / ".gemini"
        gemini_dir.mkdir()
        third_party_entry = {
            "matcher": "Shell",
            "hooks": [{"type": "command", "command": "/opt/other/hook"}],
        }
        (gemini_dir / "settings.json").write_text(
            json.dumps(
                {
                    "security": {"auth": {"selectedType": "oauth-personal"}},
                    "hooks": {"BeforeTool": [third_party_entry]},
                }
            )
        )

        install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            hook_command=_GEMINI_HOOK_COMMAND,
        )

        settings = _gemini_settings(gemini_dir)
        assert settings["security"] == {"auth": {"selectedType": "oauth-personal"}}
        # Gemini merges hooks with CONCAT, so ours is added, not substituted.
        assert third_party_entry in settings["hooks"]["BeforeTool"]
        assert _GEMINI_EXPECTED_COMMAND in _gemini_commands(settings)

    def test_reinstall_does_not_duplicate_runlayer_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        gemini_dir = tmp_path / ".gemini"
        gemini_dir.mkdir()

        for _ in range(2):
            install_client(
                Client.GEMINI_CLI,
                scope=InstallScope.USER,
                include_pipeline=True,
                hook_command=_GEMINI_HOOK_COMMAND,
            )

        hooks = _gemini_settings(gemini_dir)["hooks"]
        assert len(hooks) == 8
        for event, entries in hooks.items():
            assert len(entries) == 1, event

    def test_uninstall_removes_only_runlayer_entries_and_keeps_hooks_config(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        gemini_dir = tmp_path / ".gemini"
        gemini_dir.mkdir()
        third_party_entry = {
            "matcher": "Shell",
            "hooks": [{"type": "command", "command": "/opt/other/hook"}],
        }
        (gemini_dir / "settings.json").write_text(
            json.dumps(
                {
                    "hooksConfig": {"enabled": True},
                    "hooks": {"BeforeTool": [third_party_entry]},
                }
            )
        )
        install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command=_GEMINI_HOOK_COMMAND,
        )

        result = uninstall_client(Client.GEMINI_CLI, scope=InstallScope.USER)

        assert result.changed
        settings = _gemini_settings(gemini_dir)
        assert settings["hooks"] == {"BeforeTool": [third_party_entry]}
        # Other hook users may rely on the toggle; uninstall leaves it alone.
        assert settings["hooksConfig"] == {"enabled": True}

    def test_user_reports_ok_when_command_matches(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        (tmp_path / ".gemini").mkdir()
        install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            hook_command=_GEMINI_HOOK_COMMAND,
        )

        result = check_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            expected_hook_command=_GEMINI_HOOK_COMMAND,
            include_pipeline=False,
        )

        assert result.status == ClientStatus.OK

    def test_user_reports_drift_when_hooks_are_explicitly_disabled(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        gemini_dir = tmp_path / ".gemini"
        gemini_dir.mkdir()
        install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            hook_command=_GEMINI_HOOK_COMMAND,
        )
        settings = _gemini_settings(gemini_dir)
        settings["hooksConfig"] = {"enabled": False}
        (gemini_dir / "settings.json").write_text(json.dumps(settings))

        result = check_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            expected_hook_command=_GEMINI_HOOK_COMMAND,
            include_pipeline=False,
        )

        assert result.status == ClientStatus.DRIFTED
        assert result.detail == "hooksConfig.enabled is false"

    def test_user_skip_when_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _disable_host_client_probes(monkeypatch)

        result = install_client(
            Client.GEMINI_CLI,
            scope=InstallScope.USER,
            hook_command=_GEMINI_HOOK_COMMAND,
            skip_when_missing=True,
        )

        assert not result.written
        assert result.skipped_reason == "client not installed"
        assert not (tmp_path / ".gemini").exists()


# ── Grok CLI install ─────────────────────────────────────────────────

_GROK_HOOK_COMMAND = "/usr/local/bin/aiwatch-hook"
_GROK_EXPECTED_COMMAND = f"{_GROK_HOOK_COMMAND} --client grok-cli"
_GROK_PIPELINE_EVENTS = {
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "PostToolUse",
    "PostToolUseFailure",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "Notification",
    "PreCompact",
}


class TestGrokCLIInstall:
    def test_windows_mdm_install_refuses_nested_reparse_point(
        self, tmp_path, monkeypatch
    ):
        grok_home = tmp_path / "Users" / "alice" / ".grok"
        hook_path = grok_home / "hooks" / "runlayer.json"
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module, "enterprise_grok_cli_dir", lambda: grok_home
        )
        monkeypatch.setattr(
            clients_module,
            "path_has_link_or_reparse_point",
            lambda path: path == hook_path,
        )
        monkeypatch.setattr(clients_module, "_reown_to_console_user", lambda _p: None)

        with pytest.raises(OSError, match="unsafe Grok CLI hooks directory"):
            install_client(
                Client.GROK_CLI,
                scope=InstallScope.MDM,
                hook_command=_GROK_HOOK_COMMAND,
            )

        assert not hook_path.exists()

    def test_windows_mdm_check_reports_nested_reparse_point(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli.hook_install import presence

        grok_home = tmp_path / "Users" / "alice" / ".grok"
        hook_path = grok_home / "hooks" / "runlayer.json"
        grok_binary = grok_home / "bin" / "grok.exe"
        grok_binary.parent.mkdir(parents=True)
        grok_binary.write_text("")
        grok_binary.chmod(0o755)
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
                                        "command": _GROK_EXPECTED_COMMAND,
                                    }
                                ]
                            }
                        ]
                    }
                }
            )
        )
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module, "enterprise_grok_cli_dir", lambda: grok_home
        )
        monkeypatch.setattr(presence, "enterprise_grok_cli_dir", lambda: grok_home)
        monkeypatch.setattr(
            check_module,
            "path_has_link_or_reparse_point",
            lambda path: path == hook_path,
        )

        result = check_client(
            Client.GROK_CLI,
            scope=InstallScope.MDM,
            expected_hook_command=_GROK_HOOK_COMMAND,
            include_pipeline=False,
        )

        assert result.status == ClientStatus.DRIFTED
        assert result.detail == "unsafe Grok CLI hooks directory"

    def test_windows_mdm_absent_check_reports_nested_reparse_point(
        self, tmp_path, monkeypatch
    ):
        grok_home = tmp_path / "Users" / "alice" / ".grok"
        hook_path = grok_home / "hooks" / "runlayer.json"
        hook_path.parent.mkdir(parents=True)
        hook_path.write_text(json.dumps({"hooks": {}}))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module, "enterprise_grok_cli_dir", lambda: grok_home
        )
        monkeypatch.setattr(
            check_module,
            "path_has_link_or_reparse_point",
            lambda path: path == hook_path,
        )

        result = check_absent_client(Client.GROK_CLI, scope=InstallScope.MDM)

        assert result.status == ClientStatus.DRIFTED
        assert result.detail == "unsafe Grok CLI hooks directory"

    def test_windows_mdm_uninstall_refuses_nested_reparse_point(
        self, tmp_path, monkeypatch
    ):
        grok_home = tmp_path / "Users" / "alice" / ".grok"
        hook_path = grok_home / "hooks" / "runlayer.json"
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
                                        "command": _GROK_EXPECTED_COMMAND,
                                    }
                                ]
                            }
                        ]
                    }
                }
            )
        )
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module, "enterprise_grok_cli_dir", lambda: grok_home
        )
        monkeypatch.setattr(
            clients_module,
            "path_has_link_or_reparse_point",
            lambda path: path == hook_path,
        )

        result = uninstall_client(Client.GROK_CLI, scope=InstallScope.MDM)

        assert not result.changed
        assert result.skipped_reason == "unsafe Grok CLI hooks directory"
        assert hook_path.is_file()

    def test_mdm_prefers_managed_grok_home_over_untrusted_process_env(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli import mdm_config
        from runlayer_cli.hook_install import console_user

        console_home = tmp_path / "Users" / "alice"
        process_grok_home = tmp_path / "root-process-env" / ".grok"
        monkeypatch.setenv("GROK_HOME", str(process_grok_home))
        monkeypatch.setattr(
            console_user, "find_console_user_home", lambda: console_home
        )
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"grok_home": ".grok-managed"},
        )

        assert paths_module.enterprise_grok_cli_dir() == (
            console_home / ".grok-managed"
        )

    def test_mdm_honors_managed_grok_home_without_system_env(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli import mdm_config
        from runlayer_cli.hook_install import console_user, presence

        console_home = tmp_path / "Users" / "alice"
        grok_home = console_home / ".grok-custom"
        grok_binary = grok_home / "bin" / "grok"
        grok_binary.parent.mkdir(parents=True)
        grok_binary.write_text("#!/bin/sh\n")
        grok_binary.chmod(0o755)
        monkeypatch.delenv("GROK_HOME", raising=False)
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(presence.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            console_user, "find_console_user_home", lambda: console_home
        )
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"grok_home": ".grok-custom"},
        )
        monkeypatch.setattr(clients_module, "_reown_to_console_user", lambda _p: None)

        result = install_client(
            Client.GROK_CLI,
            scope=InstallScope.MDM,
            hook_command=_GROK_HOOK_COMMAND,
            skip_when_missing=True,
        )

        assert result.written
        assert result.config_path == grok_home / "hooks" / "runlayer.json"

    def test_mdm_rejects_managed_grok_home_outside_console_home(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli import mdm_config
        from runlayer_cli.hook_install import console_user

        console_home = tmp_path / "Users" / "alice"
        monkeypatch.delenv("GROK_HOME", raising=False)
        monkeypatch.setattr(
            console_user, "find_console_user_home", lambda: console_home
        )
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"grok_home": "../outside"},
        )

        with pytest.raises(
            ManagedPathError, match="must stay within the console user's home"
        ):
            paths_module.enterprise_grok_cli_dir()

    def test_user_writes_dedicated_hook_file_with_pre_tool_enforcement(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("GROK_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        result = install_client(
            Client.GROK_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command=_GROK_HOOK_COMMAND,
        )

        assert result.config_path == tmp_path / ".grok" / "hooks" / "runlayer.json"
        config = json.loads(result.config_path.read_text())
        assert set(config["hooks"]) == {"PreToolUse"}
        assert config["hooks"]["PreToolUse"] == [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": _GROK_EXPECTED_COMMAND,
                        "timeout": 15,
                    }
                ]
            }
        ]

    def test_user_honors_grok_home_and_registers_observational_pipeline(
        self, tmp_path, monkeypatch
    ):
        grok_home = tmp_path / "custom-grok"
        monkeypatch.setenv("GROK_HOME", str(grok_home))

        result = install_client(
            Client.GROK_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command=_GROK_HOOK_COMMAND,
        )

        config = json.loads(result.config_path.read_text())
        assert result.config_path == grok_home / "hooks" / "runlayer.json"
        assert set(config["hooks"]) == {"PreToolUse", *_GROK_PIPELINE_EVENTS}

    def test_user_metadata_only_registers_pre_tool_without_pipeline(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("GROK_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        result = install_client(
            Client.GROK_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            metadata_only=True,
            hook_command=_GROK_HOOK_COMMAND,
        )

        config = json.loads(result.config_path.read_text())
        assert set(config["hooks"]) == {"PreToolUse"}

    def test_uninstall_preserves_third_party_entries(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GROK_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hook_path = tmp_path / ".grok" / "hooks" / "runlayer.json"
        hook_path.parent.mkdir(parents=True)
        third_party = {
            "matcher": "run_terminal_cmd",
            "hooks": [{"type": "command", "command": "/opt/theirs"}],
        }
        hook_path.write_text(json.dumps({"hooks": {"PreToolUse": [third_party]}}))
        install_client(
            Client.GROK_CLI,
            scope=InstallScope.USER,
            hook_command=_GROK_HOOK_COMMAND,
        )

        result = uninstall_client(Client.GROK_CLI, scope=InstallScope.USER)

        assert result.changed
        assert json.loads(hook_path.read_text()) == {
            "hooks": {"PreToolUse": [third_party]}
        }


# ── Qwen Code install ────────────────────────────────────────────────


# Every name Runlayer registers must be present in BOTH Qwen's runtime
# HookEventName enum and its settings schema. These five load at runtime but are
# schema-absent, so registering them would read as permanent drift.
_QWEN_SCHEMA_ABSENT_EVENTS = (
    "PostCompact",
    "PermissionDenied",
    "TodoCreated",
    "TodoCompleted",
    "InstructionsLoaded",
)

# Claude Code registers these; Qwen has no such events at all.
_QWEN_NONEXISTENT_EVENTS = (
    "TeammateIdle",
    "TaskCompleted",
    "ConfigChange",
    "BeforeToolCall",
    "AfterToolCall",
)

# Reserved non-event keys under "hooks" that Qwen skips without warning.
_QWEN_RESERVED_HOOK_KEYS = ("enabled", "disabled", "notifications")


class TestQwenCodeInstall:
    def test_user_writes_qwen_settings_json(self, tmp_path, monkeypatch):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        result = install_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        settings = json.loads((tmp_path / ".qwen" / "settings.json").read_text())
        assert settings["hooks"]["PreToolUse"] == [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "/usr/local/bin/aiwatch-hook --client qwen-code",
                    }
                ]
            }
        ]
        assert "SessionStart" not in settings["hooks"]

    def test_qwen_home_env_var_relocates_user_config(self, tmp_path, monkeypatch):
        relocated = tmp_path / "elsewhere"
        monkeypatch.setenv("QWEN_HOME", str(relocated))
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        install_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert (relocated / "settings.json").exists()
        assert not (tmp_path / ".qwen").exists()

    def test_empty_qwen_home_falls_back_to_default_dir(self, tmp_path, monkeypatch):
        monkeypatch.setenv("QWEN_HOME", "")
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        install_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert (tmp_path / ".qwen" / "settings.json").exists()

    def test_registered_events_never_include_unloadable_names(self):
        registered = expected_event_names(Client.QWEN_CODE, include_pipeline=True)

        for name in _QWEN_SCHEMA_ABSENT_EVENTS + _QWEN_NONEXISTENT_EVENTS:
            assert name not in registered

    def test_registered_events_are_the_verified_golden_set(self):
        assert expected_event_names(Client.QWEN_CODE, include_pipeline=False) == {
            "PreToolUse",
            "PostToolUse",
            "PostToolUseFailure",
        }
        assert expected_event_names(Client.QWEN_CODE, include_pipeline=True) == {
            "PreToolUse",
            "PostToolUse",
            "PostToolUseFailure",
            "SessionStart",
            "SessionEnd",
            "UserPromptSubmit",
            "SubagentStart",
            "SubagentStop",
            "Stop",
            "PreCompact",
            "PermissionRequest",
            "Notification",
        }

    def test_entries_omit_matcher_because_semantics_are_per_event(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        install_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = json.loads((tmp_path / ".qwen" / "settings.json").read_text())["hooks"]
        for entries in hooks.values():
            for entry in entries:
                assert "matcher" not in entry

    def test_no_reserved_keys_written_under_hooks(self, tmp_path, monkeypatch):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        install_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = json.loads((tmp_path / ".qwen" / "settings.json").read_text())["hooks"]
        for reserved in _QWEN_RESERVED_HOOK_KEYS:
            assert reserved not in hooks

    def test_install_preserves_third_party_hooks_and_other_settings(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        qwen_dir = tmp_path / ".qwen"
        qwen_dir.mkdir()
        (qwen_dir / "settings.json").write_text(
            json.dumps(
                {
                    "theme": "Default",
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "^run_shell_command$",
                                "hooks": [
                                    {"type": "command", "command": "/opt/theirs.sh"}
                                ],
                            }
                        ]
                    },
                }
            )
        )

        install_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        settings = json.loads((qwen_dir / "settings.json").read_text())
        assert settings["theme"] == "Default"
        commands = [
            inner["command"]
            for entry in settings["hooks"]["PreToolUse"]
            for inner in entry["hooks"]
        ]
        assert "/opt/theirs.sh" in commands
        assert "/usr/local/bin/aiwatch-hook --client qwen-code" in commands

    def test_install_leaves_invalid_qwen_settings_unchanged(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        settings_path = tmp_path / ".qwen" / "settings.json"
        settings_path.parent.mkdir()
        original = '{"theme": "Default"'
        settings_path.write_text(original)

        with pytest.raises(OSError, match="invalid Qwen Code settings"):
            install_client(
                Client.QWEN_CODE,
                scope=InstallScope.USER,
                hook_command="/usr/local/bin/aiwatch-hook",
            )

        assert settings_path.read_text() == original

    def test_install_rejects_disabled_qwen_hooks(self, tmp_path, monkeypatch):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        settings_path = tmp_path / ".qwen" / "settings.json"
        settings_path.parent.mkdir()
        original = json.dumps({"disableAllHooks": True})
        settings_path.write_text(original)

        with pytest.raises(OSError, match="Qwen Code hooks are disabled"):
            install_client(
                Client.QWEN_CODE,
                scope=InstallScope.USER,
                hook_command="/usr/local/bin/aiwatch-hook",
            )

        assert settings_path.read_text() == original

    def test_check_reports_disabled_qwen_hooks_as_drifted(self, tmp_path, monkeypatch):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        qwen_dir = tmp_path / ".qwen"
        install_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        settings_path = qwen_dir / "settings.json"
        settings = json.loads(settings_path.read_text())
        settings["disableAllHooks"] = True
        settings_path.write_text(json.dumps(settings))

        result = check_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )

        assert result.status == ClientStatus.DRIFTED
        assert result.detail == "disableAllHooks is true"

    def test_reinstall_is_idempotent(self, tmp_path, monkeypatch):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        for _ in range(2):
            install_client(
                Client.QWEN_CODE,
                scope=InstallScope.USER,
                hook_command="/usr/local/bin/aiwatch-hook",
            )

        settings = json.loads((tmp_path / ".qwen" / "settings.json").read_text())
        assert len(settings["hooks"]["PreToolUse"]) == 1

    def test_mdm_writes_system_settings_dir_per_platform(self, tmp_path, monkeypatch):
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Darwin")
        assert config_path_for(Client.QWEN_CODE, InstallScope.MDM) == Path(
            "/Library/Application Support/QwenCode/settings.json"
        )

        monkeypatch.setattr(paths_module.platform, "system", lambda: "Linux")
        assert config_path_for(Client.QWEN_CODE, InstallScope.MDM) == Path(
            "/etc/qwen-code/settings.json"
        )

        monkeypatch.setattr(paths_module.platform, "system", lambda: "Windows")
        assert config_path_for(Client.QWEN_CODE, InstallScope.MDM) == Path(
            "C:/ProgramData/qwen-code/settings.json"
        )

    def test_uninstall_strips_runlayer_hooks_but_keeps_file(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        install_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        result = uninstall_client(Client.QWEN_CODE, scope=InstallScope.USER)

        assert result.changed
        settings_path = tmp_path / ".qwen" / "settings.json"
        assert settings_path.exists()
        assert "hooks" not in json.loads(settings_path.read_text())

    def test_uninstall_preserves_third_party_hooks(self, tmp_path, monkeypatch):
        monkeypatch.delenv("QWEN_HOME", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        qwen_dir = tmp_path / ".qwen"
        qwen_dir.mkdir()
        (qwen_dir / "settings.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "hooks": [
                                    {"type": "command", "command": "/opt/theirs.sh"}
                                ]
                            }
                        ]
                    }
                }
            )
        )
        install_client(
            Client.QWEN_CODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        uninstall_client(Client.QWEN_CODE, scope=InstallScope.USER)

        settings = json.loads((qwen_dir / "settings.json").read_text())
        commands = [
            inner["command"]
            for entry in settings["hooks"]["PreToolUse"]
            for inner in entry["hooks"]
        ]
        assert commands == ["/opt/theirs.sh"]


# ── Cline CLI install (dir-of-scripts) ───────────────────────────────


# Valid upstream file names that must never be registered:
# PreCompact maps to an undefined internal event and never fires; Stop and
# Notification are not CLI file-hook names at all (Notification is
# extension-only).
_CLINE_NEVER_REGISTERED = ("PreCompact", "Stop", "Notification")


class TestClineCliInstall:
    def _hooks_dir(self, tmp_path):
        return tmp_path / ".cline" / "hooks"

    def test_user_writes_one_executable_script_per_event(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")

        result = install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        script = self._hooks_dir(tmp_path) / "PreToolUse"
        assert script.is_file()
        body = script.read_text()
        assert body.startswith("#!/usr/bin/env bash\n")
        assert "/usr/local/bin/aiwatch-hook --client cline-cli" in body
        # Event identity comes from the file name, so the script must hand it to
        # the dispatcher explicitly.
        assert 'export HOOK_EVENT_NAME="PreToolUse"' in body
        # Executable bit: not required by the CLI, required by the extension.
        assert script.stat().st_mode & 0o111

    def test_enforcement_only_install_writes_just_pretooluse(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        names = {p.name for p in self._hooks_dir(tmp_path).iterdir()}
        assert names == {"PreToolUse"}

    def test_include_pipeline_writes_every_registered_event(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        names = {p.name for p in self._hooks_dir(tmp_path).iterdir()}
        assert names == expected_event_names(Client.CLINE_CLI, include_pipeline=True)

    def test_never_registers_dead_or_invalid_event_names(self):
        registered = expected_event_names(Client.CLINE_CLI, include_pipeline=True)
        for name in _CLINE_NEVER_REGISTERED:
            assert name not in registered

    def test_only_pretooluse_is_enforcement(self):
        assert expected_event_names(Client.CLINE_CLI, include_pipeline=False) == {
            "PreToolUse"
        }

    def test_cline_dir_env_var_relocates_hooks_dir(self, tmp_path, monkeypatch):
        relocated = tmp_path / "elsewhere"
        monkeypatch.setenv("CLINE_DIR", str(relocated))
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert (relocated / "hooks" / "PreToolUse").is_file()
        assert not (tmp_path / ".cline").exists()

    def test_never_writes_under_documents(self, tmp_path, monkeypatch):
        # ~/Documents/Cline/Hooks is TCC-protected on macOS; a root MDM daemon
        # writing there would prompt or fail.
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert not (tmp_path / "Documents").exists()

    def test_windows_writes_ps1_scripts(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        script = self._hooks_dir(tmp_path) / "PreToolUse.ps1"
        assert script.is_file()
        assert "$env:HOOK_EVENT_NAME = 'PreToolUse'" in script.read_text()

    def test_windows_invokes_quoted_executable_with_call_operator(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            hook_command='"C:\\Program Files\\Runlayer\\AIWatch\\aiwatch.exe" hook',
        )

        body = (self._hooks_dir(tmp_path) / "PreToolUse.ps1").read_text()
        assert (
            '& "C:\\Program Files\\Runlayer\\AIWatch\\aiwatch.exe" hook '
            "--client cline-cli\n"
        ) in body

    def test_reinstall_is_idempotent(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")

        for _ in range(2):
            install_client(
                Client.CLINE_CLI,
                scope=InstallScope.USER,
                hook_command="/usr/local/bin/aiwatch-hook",
            )

        script = self._hooks_dir(tmp_path) / "PreToolUse"
        assert script.read_text().count("aiwatch-hook") == 1

    def test_downgrade_to_enforcement_only_removes_stale_runlayer_scripts(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        names = {p.name for p in self._hooks_dir(tmp_path).iterdir()}
        assert names == {"PreToolUse"}

    def test_install_and_uninstall_never_touch_third_party_scripts(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        hooks_dir = self._hooks_dir(tmp_path)
        hooks_dir.mkdir(parents=True)
        # A differently-named third-party hook, and a third-party script sharing
        # a registered event name but with a different extension.
        theirs = hooks_dir / "PostToolUse.py"
        theirs.write_text("#!/usr/bin/env python3\nprint('{}')\n")
        unrelated = hooks_dir / "TaskStart.sh"
        unrelated.write_text("#!/bin/sh\necho '{}'\n")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        uninstall_client(Client.CLINE_CLI, scope=InstallScope.USER)

        assert theirs.read_text() == "#!/usr/bin/env python3\nprint('{}')\n"
        assert unrelated.read_text() == "#!/bin/sh\necho '{}'\n"

    def test_foreign_canonical_hook_survives_install_check_and_uninstall(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            "runlayer_cli.hook_install.check.client_is_installed",
            lambda *_a, **_k: True,
        )
        hooks_dir = self._hooks_dir(tmp_path)
        hooks_dir.mkdir(parents=True)
        foreign = hooks_dir / "PreToolUse"
        foreign.write_text("#!/bin/sh\necho 'foreign'\n")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert foreign.read_text() == "#!/bin/sh\necho 'foreign'\n"
        assert (hooks_dir / "PreToolUse.sh").is_file()
        assert (
            check_client(
                Client.CLINE_CLI,
                scope=InstallScope.USER,
                expected_hook_command="/usr/local/bin/aiwatch-hook",
                include_pipeline=False,
            ).status
            == ClientStatus.OK
        )

        result = uninstall_client(Client.CLINE_CLI, scope=InstallScope.USER)

        assert result.changed
        assert foreign.read_text() == "#!/bin/sh\necho 'foreign'\n"
        assert not (hooks_dir / "PreToolUse.sh").exists()

    def test_mdm_install_does_not_follow_symlinked_cline_directory(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        console_home.mkdir(parents=True)
        outside = tmp_path / "outside"
        outside.mkdir()
        (console_home / ".cline").symlink_to(outside, target_is_directory=True)
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            clients_module,
            "enterprise_cline_cli_dir",
            lambda: console_home / ".cline" / "hooks",
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )
        monkeypatch.setattr(clients_module, "_reown_to_console_user", lambda _p: None)

        with pytest.raises(OSError):
            install_client(
                Client.CLINE_CLI,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch-hook",
            )

        assert not (outside / "hooks").exists()

    def test_mdm_uninstall_does_not_follow_swapped_symlinked_directory(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        hooks_dir = console_home / ".cline" / "hooks"
        outside_hook = tmp_path / "outside" / "hooks" / "PreToolUse"
        outside_hook.parent.mkdir(parents=True)
        outside_hook.write_text("outside must survive\n")
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            clients_module, "enterprise_cline_cli_dir", lambda: hooks_dir
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )
        monkeypatch.setattr(clients_module, "_reown_to_console_user", lambda _p: None)
        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        original_read = clients_module.maybe_safe_read_text
        swapped = False

        def swap_after_read(path, *, home):
            nonlocal swapped
            text = original_read(path, home=home)
            if path.name == "PreToolUse" and not swapped:
                swapped = True
                (console_home / ".cline").rename(console_home / ".cline-original")
                (console_home / ".cline").symlink_to(
                    tmp_path / "outside", target_is_directory=True
                )
            return text

        monkeypatch.setattr(clients_module, "maybe_safe_read_text", swap_after_read)

        uninstall_client(Client.CLINE_CLI, scope=InstallScope.MDM)

        assert outside_hook.read_text() == "outside must survive\n"

    def test_windows_mdm_install_refuses_reparse_point(self, tmp_path, monkeypatch):
        hooks_dir = tmp_path / "Users" / "alice" / ".cline" / "hooks"
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module, "enterprise_cline_cli_dir", lambda: hooks_dir
        )
        monkeypatch.setattr(
            clients_module, "path_has_link_or_reparse_point", lambda _p: True
        )
        monkeypatch.setattr(clients_module, "_reown_to_console_user", lambda _p: None)

        with pytest.raises(OSError, match="unsafe Cline hooks directory"):
            install_client(
                Client.CLINE_CLI,
                scope=InstallScope.MDM,
                hook_command='"C:\\Program Files\\Runlayer\\AIWatch\\aiwatch.exe" hook',
            )

        assert not hooks_dir.exists()

    def test_windows_mdm_uninstall_refuses_reparse_point(self, tmp_path, monkeypatch):
        hooks_dir = tmp_path / "Users" / "alice" / ".cline" / "hooks"
        script = hooks_dir / "PreToolUse.ps1"
        script.parent.mkdir(parents=True)
        script.write_text(
            "# runlayer-owned Cline hook — safe to delete\n"
            '"C:\\Program Files\\Runlayer\\AIWatch\\aiwatch.exe" hook\n'
        )
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module, "enterprise_cline_cli_dir", lambda: hooks_dir
        )
        monkeypatch.setattr(
            clients_module, "path_has_link_or_reparse_point", lambda _p: True
        )

        result = uninstall_client(Client.CLINE_CLI, scope=InstallScope.MDM)

        assert not result.changed
        assert result.skipped_reason == "unsafe Cline hooks directory"
        assert script.is_file()

    def test_uninstall_removes_only_runlayer_owned_scripts(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        hooks_dir = self._hooks_dir(tmp_path)
        hooks_dir.mkdir(parents=True)
        # Same canonical file name, but not ours: must survive untouched.
        foreign = hooks_dir / "TaskComplete"
        foreign.write_text("#!/bin/sh\necho 'someone elses hook'\n")

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        result = uninstall_client(Client.CLINE_CLI, scope=InstallScope.USER)

        assert result.changed
        assert not (hooks_dir / "PreToolUse").exists()
        assert foreign.read_text() == "#!/bin/sh\necho 'someone elses hook'\n"

    def test_uninstall_without_hooks_dir_is_not_a_change(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        result = uninstall_client(Client.CLINE_CLI, scope=InstallScope.USER)

        assert not result.changed


class TestClineCliCheck:
    def test_check_reports_ok_after_install(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            "runlayer_cli.hook_install.check.client_is_installed",
            lambda *_a, **_k: True,
        )
        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        result = check_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )

        assert result.status == ClientStatus.OK

    def test_check_reports_missing_when_no_scripts(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(
            "runlayer_cli.hook_install.check.client_is_installed",
            lambda *_a, **_k: True,
        )
        (tmp_path / ".cline" / "hooks").mkdir(parents=True)

        result = check_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )

        assert result.status == ClientStatus.MISSING

    def test_check_reports_drift_on_stale_command(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            "runlayer_cli.hook_install.check.client_is_installed",
            lambda *_a, **_k: True,
        )
        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/old/path/aiwatch-hook",
        )

        result = check_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )

        assert result.status == ClientStatus.DRIFTED

    def test_absent_check_ignores_third_party_scripts(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hooks_dir = tmp_path / ".cline" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "PreToolUse").write_text("#!/bin/sh\necho '{}'\n")

        result = check_absent_client(Client.CLINE_CLI, scope=InstallScope.USER)

        assert result.status == ClientStatus.OK

    def test_absent_check_flags_runlayer_scripts(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CLINE_DIR", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        result = check_absent_client(Client.CLINE_CLI, scope=InstallScope.USER)

        assert result.status == ClientStatus.DRIFTED


# ── Per-client command hints ───────────────────────────────────────────


class TestHookCommandForClient:
    def test_user_scope_adds_client_arg_for_every_supported_client(self):
        for client in iter_supported_clients():
            command = hook_command_for_client(
                "/usr/local/bin/aiwatch-hook",
                client,
            )

            assert command == f"/usr/local/bin/aiwatch-hook --client {client.value}"


# ── Claude Code install ─────────────────────────────────────────────


class TestClaudeCodeInstall:
    def test_user_writes_settings_json(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        settings = json.loads((claude_dir / "settings.json").read_text())
        assert settings["showThinkingSummaries"] is True
        assert "PreToolUse" in settings["hooks"]
        first_entry = settings["hooks"]["PreToolUse"][0]
        assert first_entry["matcher"] == ""
        assert first_entry["hooks"][0]["command"].endswith(
            "aiwatch-hook --client claude_code"
        )

    def test_user_does_not_register_worktree_provider_hooks(
        self, tmp_path, monkeypatch
    ):
        # Claude Code treats a configured WorktreeCreate hook as the worktree
        # *provider* (it must create the worktree and print its path), so a
        # passive telemetry entry there breaks worktree creation entirely.
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = json.loads((claude_dir / "settings.json").read_text())["hooks"]
        assert "SessionStart" in hooks
        assert "WorktreeCreate" not in hooks
        assert "WorktreeRemove" not in hooks

    def test_user_removes_stale_worktree_hook_entries(self, tmp_path, monkeypatch):
        # Deployed fleets already carry worktree entries; reinstall must strip
        # Runlayer's while preserving third-party providers.
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        runlayer_entry = {
            "matcher": "",
            "hooks": [
                {
                    "type": "command",
                    "command": (
                        '"/usr/local/lib/runlayer/aiwatch/aiwatch"'
                        " hook --client claude_code"
                    ),
                }
            ],
        }
        third_party_entry = {
            "matcher": "",
            "hooks": [{"type": "command", "command": "/opt/other/worktree-provider"}],
        }
        (claude_dir / "settings.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "WorktreeCreate": [runlayer_entry, third_party_entry],
                        "WorktreeRemove": [runlayer_entry],
                    }
                }
            )
        )

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = json.loads((claude_dir / "settings.json").read_text())["hooks"]
        assert hooks["WorktreeCreate"] == [third_party_entry]
        assert "WorktreeRemove" not in hooks

    def test_user_preserves_unrelated_settings_keys(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.json").write_text(
            json.dumps({"theme": "dark", "model": "claude-3"})
        )

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        settings = json.loads((claude_dir / "settings.json").read_text())
        assert settings["theme"] == "dark"
        assert settings["model"] == "claude-3"
        assert "hooks" in settings


# ── Codex install ────────────────────────────────────────────────────


class TestCodexInstall:
    def test_user_enables_features_hooks(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        codex_dir = tmp_path / ".codex"
        codex_dir.mkdir()

        install_client(
            Client.CODEX,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        config_toml = (codex_dir / "config.toml").read_text()
        assert "[features]" in config_toml
        assert "hooks = true" in config_toml
        hooks = json.loads((codex_dir / "hooks.json").read_text())["hooks"]
        command = hooks["PreToolUse"][0]["hooks"][0]["command"]
        assert command.endswith("aiwatch-hook --client codex")

    def test_user_features_hooks_already_set_is_idempotent(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        codex_dir = tmp_path / ".codex"
        codex_dir.mkdir()
        (codex_dir / "config.toml").write_text("[features]\nhooks = true\n")

        install_client(
            Client.CODEX,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        content = (codex_dir / "config.toml").read_text()
        # No duplicate hooks = true lines.
        assert content.count("hooks = true") == 1


# ── Hermes install ───────────────────────────────────────────────────


class TestHermesInstall:
    def test_user_writes_config_yaml(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hermes_dir = tmp_path / ".hermes"
        hermes_dir.mkdir()

        result = install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        config = yaml.safe_load((hermes_dir / "config.yaml").read_text())
        assert "pre_tool_call" in config["hooks"]
        assert config["hooks"]["pre_tool_call"][0]["command"].endswith(
            "aiwatch-hook --client hermes"
        )
        assert "transform_tool_result" in config["hooks"]
        # Pipeline events not registered by default.
        assert "post_tool_call" not in config["hooks"]

    def test_user_include_pipeline_registers_event_hooks(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".hermes").mkdir()

        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = yaml.safe_load((tmp_path / ".hermes" / "config.yaml").read_text())[
            "hooks"
        ]
        for name in ("post_tool_call", "pre_llm_call", "on_session_start"):
            assert name in hooks

    def test_user_skip_when_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _disable_host_client_probes(monkeypatch)

        result = install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
            skip_when_missing=True,
        )

        assert not result.written
        assert result.skipped_reason == "client not installed"

    def test_user_preserves_top_level_yaml_keys(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hermes_dir = tmp_path / ".hermes"
        hermes_dir.mkdir()
        (hermes_dir / "config.yaml").write_text(
            yaml.safe_dump(
                {
                    "mcp_servers": {"linear": {"url": "https://linear.example/mcp"}},
                    "hooks": {
                        "pre_tool_call": [{"command": "/other/tool"}],
                    },
                }
            )
        )

        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        config = yaml.safe_load((hermes_dir / "config.yaml").read_text())
        assert config["mcp_servers"]["linear"]["url"] == "https://linear.example/mcp"
        commands = [entry["command"] for entry in config["hooks"]["pre_tool_call"]]
        assert "/other/tool" in commands
        assert any(c.endswith("aiwatch-hook --client hermes") for c in commands)

    def test_user_replaces_stale_runlayer_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hermes_dir = tmp_path / ".hermes"
        hermes_dir.mkdir()
        (hermes_dir / "config.yaml").write_text(
            yaml.safe_dump(
                {
                    "hooks": {
                        "pre_tool_call": [
                            {"command": "/old/path/aiwatch-hook"},
                            {"command": "/usr/local/bin/aiwatch-enforce"},
                        ]
                    }
                }
            )
        )

        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/new/path/aiwatch-hook",
            skip_when_missing=False,
        )

        config = yaml.safe_load((hermes_dir / "config.yaml").read_text())
        commands = [entry["command"] for entry in config["hooks"]["pre_tool_call"]]
        assert commands == ["/new/path/aiwatch-hook --client hermes"]


# ── Goose install ────────────────────────────────────────────────────


class TestGooseInstall:
    def test_user_writes_plugin_hooks_json(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        goose_config_dir = tmp_path / ".config" / "goose"
        goose_config_dir.mkdir(parents=True)

        result = install_client(
            Client.GOOSE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        plugin_dir = tmp_path / ".agents" / "plugins" / "runlayer-hooks"
        assert result.written
        manifest = json.loads((plugin_dir / "plugin.json").read_text())
        assert manifest["name"] == "runlayer-hooks"
        hooks = json.loads((plugin_dir / "hooks" / "hooks.json").read_text())["hooks"]
        command = hooks["PreToolUse"][0]["hooks"][0]["command"]
        assert command.endswith("aiwatch-hook --client goose")
        assert "BeforeReadFile" in hooks
        assert "BeforeShellExecution" in hooks
        assert "SessionStart" not in hooks

    def test_user_include_pipeline_registers_event_hooks(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".config" / "goose").mkdir(parents=True)

        install_client(
            Client.GOOSE,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = json.loads(
            (
                tmp_path
                / ".agents"
                / "plugins"
                / "runlayer-hooks"
                / "hooks"
                / "hooks.json"
            ).read_text()
        )["hooks"]
        for name in ("SessionStart", "SessionEnd", "AfterFileEdit"):
            assert name in hooks

    def test_user_skip_when_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _disable_host_client_probes(monkeypatch)

        result = install_client(
            Client.GOOSE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
            skip_when_missing=True,
        )

        assert not result.written
        assert result.skipped_reason == "client not installed"

    def test_user_preserves_third_party_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        plugin_dir = tmp_path / ".agents" / "plugins" / "runlayer-hooks"
        hooks_dir = plugin_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        third_party = {"hooks": [{"type": "command", "command": "/opt/other/hook"}]}
        (hooks_dir / "hooks.json").write_text(
            json.dumps({"hooks": {"PreToolUse": [third_party]}})
        )

        install_client(
            Client.GOOSE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = json.loads((hooks_dir / "hooks.json").read_text())["hooks"]
        commands = [entry["hooks"][0]["command"] for entry in hooks["PreToolUse"]]
        assert "/opt/other/hook" in commands
        assert any(c.endswith("aiwatch-hook --client goose") for c in commands)

    def test_user_reports_ok_when_command_matches(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        (tmp_path / ".config" / "goose").mkdir(parents=True)
        install_client(
            Client.GOOSE,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        result = check_client(
            Client.GOOSE,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )

        assert result.status == ClientStatus.OK


# ── Windsurf install ─────────────────────────────────────────────────

# Cascade's own snake_case event names, split by what can actually block
# (only *pre* hooks; Cascade ignores post-hook exit codes).
_WINDSURF_ENFORCEMENT_EVENTS = {
    "pre_mcp_tool_use",
    "pre_run_command",
    "pre_read_code",
}
_WINDSURF_PIPELINE_EVENTS = {
    "pre_user_prompt",
    "post_mcp_tool_use",
    "post_run_command",
    "post_write_code",
    "post_cascade_response",
}


def _windsurf_hooks_json(root: Path) -> Path:
    return root / ".codeium" / "windsurf" / "hooks.json"


class TestWindsurfInstall:
    def test_user_writes_hooks_json_into_codeium_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        result = install_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks_json = _windsurf_hooks_json(tmp_path)
        assert result.written
        assert result.config_path == hooks_json
        data = json.loads(hooks_json.read_text())
        # Flat Cascade entries: no inner "hooks" list, no "version" key.
        assert set(data) == {"hooks"}
        assert set(data["hooks"]) == _WINDSURF_ENFORCEMENT_EVENTS
        assert data["hooks"]["pre_mcp_tool_use"] == [
            {"command": "/usr/local/bin/aiwatch-hook --client windsurf"}
        ]
        assert data["hooks"]["pre_read_code"] == [
            {"command": "/usr/local/bin/aiwatch-hook --client windsurf"}
        ]

    def test_user_include_pipeline_registers_cascade_events(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        install_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        hooks = json.loads(_windsurf_hooks_json(tmp_path).read_text())["hooks"]
        assert set(hooks) == _WINDSURF_ENFORCEMENT_EVENTS | _WINDSURF_PIPELINE_EVENTS
        # pre_write_code has no canonical normalized event, so it is never wired.
        assert "pre_write_code" not in hooks

    def test_user_idempotent_repeat_writes_match(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        install_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        first = _windsurf_hooks_json(tmp_path).read_text()

        install_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        second = _windsurf_hooks_json(tmp_path).read_text()

        assert first == second
        hooks = json.loads(second)["hooks"]
        assert all(len(entries) == 1 for entries in hooks.values())

    def test_user_preserves_third_party_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hooks_json = _windsurf_hooks_json(tmp_path)
        hooks_json.parent.mkdir(parents=True)
        third_party_command = "/usr/local/bin/some-other-tool"
        hooks_json.write_text(
            json.dumps(
                {
                    "hooks": {
                        "pre_run_command": [{"command": third_party_command}],
                    },
                }
            )
        )

        install_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        commands = [
            entry["command"]
            for entry in json.loads(hooks_json.read_text())["hooks"]["pre_run_command"]
        ]
        assert third_party_command in commands
        assert any(c.endswith("aiwatch-hook --client windsurf") for c in commands)

    def test_user_replaces_stale_runlayer_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hooks_json = _windsurf_hooks_json(tmp_path)
        hooks_json.parent.mkdir(parents=True)
        hooks_json.write_text(
            json.dumps(
                {
                    "hooks": {
                        "pre_mcp_tool_use": [
                            {"command": "/old/path/aiwatch-hook"},
                            {"command": "/usr/local/bin/aiwatch-enforce"},
                        ],
                    },
                }
            )
        )

        install_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            hook_command="/new/path/aiwatch-hook",
        )

        commands = [
            entry["command"]
            for entry in json.loads(hooks_json.read_text())["hooks"]["pre_mcp_tool_use"]
        ]
        assert commands == ["/new/path/aiwatch-hook --client windsurf"]

    def test_user_skip_when_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _disable_host_client_probes(monkeypatch)

        result = install_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
            skip_when_missing=True,
        )

        assert not result.written
        assert result.skipped_reason == "client not installed"
        assert not (tmp_path / ".codeium").exists()

    def test_mdm_writes_enterprise_dir_not_console_home(self, tmp_path, monkeypatch):
        """Windsurf has a real root-owned system dir, so MDM never touches ~."""
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
        enterprise_root = tmp_path / "enterprise" / "Windsurf"
        monkeypatch.setattr(
            clients_module, "enterprise_windsurf_dir", lambda: enterprise_root
        )

        result = install_client(
            Client.WINDSURF,
            scope=InstallScope.MDM,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        assert result.written
        assert result.config_path == enterprise_root / "hooks.json"
        hooks = json.loads((enterprise_root / "hooks.json").read_text())["hooks"]
        assert set(hooks) == _WINDSURF_ENFORCEMENT_EVENTS
        assert not (home / ".codeium").exists()

    def test_mdm_migrates_user_runlayer_hooks_and_preserves_third_party(
        self, tmp_path, monkeypatch
    ):
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
        enterprise_root = tmp_path / "enterprise" / "Windsurf"
        monkeypatch.setattr(
            clients_module, "enterprise_windsurf_dir", lambda: enterprise_root
        )
        user_hooks_json = _windsurf_hooks_json(home)
        user_hooks_json.parent.mkdir(parents=True)
        third_party = {"command": "/usr/local/bin/third-party-hook"}
        user_hooks_json.write_text(
            json.dumps(
                {
                    "hooks": {
                        "pre_run_command": [
                            {
                                "command": (
                                    "/usr/local/bin/aiwatch-hook --client windsurf"
                                )
                            },
                            third_party,
                        ],
                        "pre_read_code": [
                            {
                                "command": (
                                    "/usr/local/bin/aiwatch-hook --client windsurf"
                                )
                            }
                        ],
                    }
                }
            )
        )

        install_client(
            Client.WINDSURF,
            scope=InstallScope.MDM,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        user_hooks = json.loads(user_hooks_json.read_text())["hooks"]
        assert user_hooks == {"pre_run_command": [third_party]}
        enterprise_hooks = json.loads((enterprise_root / "hooks.json").read_text())[
            "hooks"
        ]
        assert set(enterprise_hooks) == _WINDSURF_ENFORCEMENT_EVENTS

    def test_user_reports_ok_when_command_matches(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        install_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        result = check_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )

        assert result.status == ClientStatus.OK


# ── uninstall / absent detection ───────────────────────────────────────


class TestUninstall:
    def test_user_cursor_removes_runlayer_and_preserves_third_party(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()
        (cursor_dir / "hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "theme": "dark",
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": "/usr/local/bin/aiwatch hook --client cursor"},
                            {"command": "/opt/other/hook"},
                        ],
                        "beforeReadFile": [{"command": "/usr/local/bin/aiwatch-hook"}],
                    },
                }
            )
        )

        result = uninstall_client(Client.CURSOR, scope=InstallScope.USER)

        assert result.changed
        data = json.loads((cursor_dir / "hooks.json").read_text())
        assert data["theme"] == "dark"
        assert data["hooks"] == {"beforeMCPExecution": [{"command": "/opt/other/hook"}]}

    def test_user_claude_removes_nested_runlayer_hooks_preserving_settings(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        third_party_entry = {
            "matcher": "Bash",
            "hooks": [{"type": "command", "command": "/opt/other/hook"}],
        }
        (claude_dir / "settings.json").write_text(
            json.dumps(
                {
                    "theme": "dark",
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/usr/local/bin/aiwatch hook "
                                        "--client claude_code",
                                    }
                                ],
                            },
                            third_party_entry,
                        ],
                        "PostToolUse": [
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

        result = uninstall_client(Client.CLAUDE_CODE, scope=InstallScope.USER)

        assert result.changed
        settings = json.loads((claude_dir / "settings.json").read_text())
        assert settings["theme"] == "dark"
        assert settings["hooks"] == {"PreToolUse": [third_party_entry]}

    def test_user_codex_leaves_features_hooks_enabled(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        codex_dir = tmp_path / ".codex"
        codex_dir.mkdir()
        install_client(
            Client.CODEX,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        result = uninstall_client(Client.CODEX, scope=InstallScope.USER)

        assert result.changed
        assert not (codex_dir / "hooks.json").exists()
        assert "hooks = true" in (codex_dir / "config.toml").read_text()

    def test_user_hermes_removes_runlayer_and_preserves_yaml(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hermes_dir = tmp_path / ".hermes"
        hermes_dir.mkdir()
        (hermes_dir / "config.yaml").write_text(
            yaml.safe_dump(
                {
                    "mcp_servers": {"linear": {"url": "https://linear.example/mcp"}},
                    "hooks": {
                        "pre_tool_call": [
                            {"command": "/usr/local/bin/aiwatch hook --client hermes"},
                            {"command": "/opt/other/hook"},
                        ],
                        "transform_tool_result": [
                            {"command": "/usr/local/bin/aiwatch-hook"}
                        ],
                    },
                },
                sort_keys=False,
            )
        )

        result = uninstall_client(Client.HERMES, scope=InstallScope.USER)

        assert result.changed
        config = yaml.safe_load((hermes_dir / "config.yaml").read_text())
        assert config["mcp_servers"]["linear"]["url"] == "https://linear.example/mcp"
        assert config["hooks"] == {"pre_tool_call": [{"command": "/opt/other/hook"}]}

    def test_user_goose_removes_runlayer_and_preserves_third_party(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        plugin_dir = tmp_path / ".agents" / "plugins" / "runlayer-hooks"
        hooks_dir = plugin_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        third_party = {"hooks": [{"type": "command", "command": "/opt/other/hook"}]}
        (hooks_dir / "hooks.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/usr/local/bin/aiwatch hook "
                                        "--client goose",
                                    }
                                ]
                            },
                            third_party,
                        ],
                        "BeforeReadFile": [
                            {
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/usr/local/bin/aiwatch-hook",
                                    }
                                ]
                            }
                        ],
                    }
                }
            )
        )

        result = uninstall_client(Client.GOOSE, scope=InstallScope.USER)

        assert result.changed
        hooks = json.loads((hooks_dir / "hooks.json").read_text())["hooks"]
        assert hooks == {"PreToolUse": [third_party]}

    def test_user_vscode_removes_runlayer_hook_locations_preserving_custom_settings(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / "Library" / "Application Support" / "Code").mkdir(parents=True)
        vscode_dir = tmp_path / ".copilot" / "hooks"
        vscode_dir.mkdir(parents=True)
        (vscode_dir / "runlayer.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "type": "command",
                                "command": "/usr/local/bin/aiwatch hook --client vscode",
                            }
                        ],
                    }
                }
            )
        )
        settings_path = _vscode_user_settings_path(tmp_path)
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

        result = uninstall_client(Client.VSCODE, scope=InstallScope.USER)

        assert result.changed
        assert not (vscode_dir / "runlayer.json").exists()
        settings = json.loads(settings_path.read_text())
        assert settings == {
            "editor.tabSize": 2,
            "chat.hookFilesLocations": {"custom/hooks": True},
        }

    def test_user_copilot_uninstall_removes_legacy_and_shell_specific_entries(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        copilot_dir = tmp_path / ".copilot"
        copilot_dir.mkdir()
        third_party = {
            "type": "command",
            "bash": "/opt/other/hook",
            "powershell": "/opt/other/hook",
        }
        (copilot_dir / "settings.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "theme": "dark",
                    "hooks": {
                        "PreToolUse": [
                            {
                                "type": "command",
                                "command": (
                                    "/old/path/aiwatch-hook --client github-copilot-cli"
                                ),
                            },
                            {
                                "type": "command",
                                "bash": (
                                    "/usr/local/bin/aiwatch-hook "
                                    "--client github-copilot-cli"
                                ),
                                "powershell": (
                                    "/usr/local/bin/aiwatch-hook "
                                    "--client github-copilot-cli"
                                ),
                            },
                            third_party,
                        ]
                    },
                }
            )
        )

        result = uninstall_client(Client.GITHUB_COPILOT_CLI, scope=InstallScope.USER)

        assert result.changed
        settings = json.loads((copilot_dir / "settings.json").read_text())
        assert settings == {
            "version": 1,
            "theme": "dark",
            "hooks": {"PreToolUse": [third_party]},
        }

    def test_user_windsurf_removes_runlayer_and_preserves_third_party(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        hooks_json = _windsurf_hooks_json(tmp_path)
        hooks_json.parent.mkdir(parents=True)
        hooks_json.write_text(
            json.dumps(
                {
                    "otherSetting": "keep me",
                    "hooks": {
                        "pre_mcp_tool_use": [
                            {
                                "command": "/usr/local/bin/aiwatch hook "
                                "--client windsurf"
                            },
                            {"command": "/opt/other/hook"},
                        ],
                        "pre_read_code": [{"command": "/usr/local/bin/aiwatch-hook"}],
                    },
                }
            )
        )

        result = uninstall_client(Client.WINDSURF, scope=InstallScope.USER)

        assert result.changed
        data = json.loads(hooks_json.read_text())
        assert data["otherSetting"] == "keep me"
        assert data["hooks"] == {"pre_mcp_tool_use": [{"command": "/opt/other/hook"}]}

    def test_user_windsurf_removes_file_when_only_runlayer_entries_remain(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        install_client(
            Client.WINDSURF,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        result = uninstall_client(Client.WINDSURF, scope=InstallScope.USER)

        assert result.changed
        assert not _windsurf_hooks_json(tmp_path).exists()

    def test_user_windsurf_uninstall_is_noop_without_config(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        result = uninstall_client(Client.WINDSURF, scope=InstallScope.USER)

        assert not result.changed
        assert result.skipped_reason == "no hooks.json"


# ── Install never writes runlayer-config.json (enforcement lives in MDM) ───


class TestInstallDoesNotWriteRuntimeConfig:
    """The bundle install path delegates enforcement to MDM managed config;
    no sibling runlayer-config.json should ever be written."""

    def test_user_install_does_not_write_runtime_config(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        bin_dir = tmp_path / "usr" / "local" / "bin"
        bin_dir.mkdir(parents=True)
        hook_binary = bin_dir / "aiwatch-hook"

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command=str(hook_binary),
        )

        assert not (tmp_path / ".cursor" / "hooks" / "runlayer-config.json").exists()
        assert not (bin_dir / "runlayer-config.json").exists()

    def test_mdm_install_does_not_write_runtime_config(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import clients as clients_module

        enterprise_root = tmp_path / "enterprise" / "Cursor"
        monkeypatch.setattr(
            clients_module, "enterprise_cursor_dir", lambda: enterprise_root
        )
        bin_dir = tmp_path / "usr" / "local" / "bin"
        bin_dir.mkdir(parents=True)
        hook_binary = bin_dir / "aiwatch-hook"

        install_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            hook_command=str(hook_binary),
        )

        assert not (enterprise_root / "hooks" / "runlayer-config.json").exists()
        assert not (bin_dir / "runlayer-config.json").exists()


# ── check / drift detection ─────────────────────────────────────────


class TestCheck:
    def test_user_reports_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _disable_host_client_probes(monkeypatch)
        result = check_client(Client.CURSOR, scope=InstallScope.USER)
        assert result.status == ClientStatus.CLIENT_NOT_INSTALLED

    def test_mdm_reports_client_not_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _disable_host_client_probes(monkeypatch)

        result = check_client(Client.CURSOR, scope=InstallScope.MDM)

        assert result.status == ClientStatus.CLIENT_NOT_INSTALLED

    def test_user_reports_missing_when_no_config_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        result = check_client(Client.CURSOR, scope=InstallScope.USER)
        assert result.status == ClientStatus.MISSING

    def test_user_reports_ok_when_command_matches(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        (tmp_path / ".cursor").mkdir()
        (tmp_path / ".cursor" / "mcp.json").write_text("{}")
        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        result = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )
        assert result.status == ClientStatus.OK

    def test_user_reports_drifted_when_command_mismatches(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        (tmp_path / ".cursor").mkdir()
        (tmp_path / ".cursor" / "mcp.json").write_text("{}")
        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/old/path/aiwatch-hook",
        )
        result = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            expected_hook_command="/new/path/aiwatch-hook",
        )
        assert result.status == ClientStatus.DRIFTED

    def test_check_all_returns_one_per_client(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        results = check_all(
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
        )
        assert {r.client for r in results} == set(iter_supported_clients())

    def test_check_all_does_not_hide_unexpected_value_error(self, monkeypatch):
        def _raise_programming_error(*_args, **_kwargs):
            raise ValueError("unknown client programming error")

        monkeypatch.setattr(
            check_module, "iter_supported_clients", lambda: (Client.CURSOR,)
        )
        monkeypatch.setattr(
            check_module,
            "check_client",
            _raise_programming_error,
        )

        with pytest.raises(ValueError, match="unknown client programming error"):
            check_all()

    def test_user_reports_ok_for_hermes_when_command_matches(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        (tmp_path / ".hermes").mkdir()
        (tmp_path / ".hermes" / "config.yaml").write_text("model: auto\n")
        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )
        result = check_client(
            Client.HERMES,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch-hook",
            include_pipeline=False,
        )
        assert result.status == ClientStatus.OK

    def test_user_reports_drifted_for_hermes_when_command_mismatches(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_client_executable_installed(monkeypatch)
        (tmp_path / ".hermes").mkdir()
        (tmp_path / ".hermes" / "config.yaml").write_text("model: auto\n")
        install_client(
            Client.HERMES,
            scope=InstallScope.USER,
            hook_command="/old/path/aiwatch-hook",
        )
        result = check_client(
            Client.HERMES,
            scope=InstallScope.USER,
            expected_hook_command="/new/path/aiwatch-hook",
        )
        assert result.status == ClientStatus.DRIFTED

    def test_mdm_reports_drifted_when_event_hooks_missing(self, tmp_path, monkeypatch):
        """Enforcement-only install is DRIFTED when the event set is expected."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        _mark_client_executable_installed(monkeypatch)
        enterprise_root = tmp_path / "enterprise" / "Cursor"
        monkeypatch.setattr(
            clients_module, "enterprise_cursor_dir", lambda: enterprise_root
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        result = check_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        assert result.status == ClientStatus.DRIFTED
        assert "missing event hooks" in result.detail

    def test_mdm_reports_ok_when_full_event_set_present(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        _mark_client_executable_installed(monkeypatch)
        enterprise_root = tmp_path / "enterprise" / "Cursor"
        monkeypatch.setattr(
            clients_module, "enterprise_cursor_dir", lambda: enterprise_root
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        result = check_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        assert result.status == ClientStatus.OK

    def test_mdm_claude_code_reports_ok_from_console_home(self, tmp_path, monkeypatch):
        """MDM Claude Code drift check reads the console user's ~/.claude
        link-safe and reports OK when the install is present."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        _mark_client_executable_installed(monkeypatch)
        console_claude_root = console_home / ".claude"
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        result = check_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        assert result.status == ClientStatus.OK

    def test_mdm_claude_code_check_refuses_symlinked_settings(
        self, tmp_path, monkeypatch
    ):
        """Regression (ENG-3217): a planted ``~/.claude/settings.json`` symlink
        must not let the root drift check read a file outside the home. The
        link-safe read returns nothing -> MISSING; the outside target (which
        contains a valid-looking Runlayer hook) is never followed."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        _mark_client_executable_installed(monkeypatch)
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        outside = tmp_path / "outside.json"
        outside.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/usr/local/bin/aiwatch hook "
                                        "--client claude_code",
                                    }
                                ],
                            }
                        ]
                    }
                }
            )
        )
        (console_claude_root / "settings.json").symlink_to(outside)
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )

        result = check_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        # Symlink not followed: the outside hooks were never read.
        assert result.status == ClientStatus.MISSING

    def test_mdm_hermes_check_refuses_symlinked_config(self, tmp_path, monkeypatch):
        """Regression (ENG-3217): a planted ``~/.hermes/config.yaml`` symlink is
        not followed by the root drift check."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        _mark_client_executable_installed(monkeypatch)
        console_hermes_root = console_home / ".hermes"
        console_hermes_root.mkdir(parents=True)
        outside = tmp_path / "outside.yaml"
        outside.write_text(
            yaml.safe_dump(
                {
                    "hooks": {
                        "pre_tool_call": [
                            {"command": "/usr/local/bin/aiwatch hook --client hermes"}
                        ]
                    }
                }
            )
        )
        (console_hermes_root / "config.yaml").symlink_to(outside)
        monkeypatch.setattr(
            clients_module, "enterprise_hermes_dir", lambda: console_hermes_root
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )

        result = check_client(
            Client.HERMES,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        assert result.status == ClientStatus.MISSING

    def test_mdm_goose_check_refuses_symlinked_hooks_json(self, tmp_path, monkeypatch):
        """Regression (ENG-3217): a planted Goose hooks.json symlink is not
        followed by the root drift check."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        _mark_client_executable_installed(monkeypatch)
        console_goose_root = console_home / ".agents" / "plugins" / "runlayer-hooks"
        hooks_dir = console_goose_root / "hooks"
        hooks_dir.mkdir(parents=True)
        outside = tmp_path / "outside.json"
        outside.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "/usr/local/bin/aiwatch hook "
                                        "--client goose",
                                    }
                                ]
                            }
                        ]
                    }
                }
            )
        )
        (hooks_dir / "hooks.json").symlink_to(outside)
        monkeypatch.setattr(
            clients_module, "enterprise_goose_dir", lambda: console_goose_root
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )

        result = check_client(
            Client.GOOSE,
            scope=InstallScope.MDM,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )

        assert result.status == ClientStatus.MISSING


class TestAbsentCheck:
    def test_user_reports_ok_when_client_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        result = check_absent_client(Client.CURSOR, scope=InstallScope.USER)

        assert result.status == ClientStatus.OK

    def test_user_reports_drifted_when_runlayer_entries_remain(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch-hook",
        )

        result = check_absent_client(Client.CURSOR, scope=InstallScope.USER)

        assert result.status == ClientStatus.DRIFTED
        assert "Runlayer hook entries present" in result.detail

    def test_check_absent_all_returns_one_per_client(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        results = check_absent_all(scope=InstallScope.USER)

        assert {r.client for r in results} == set(iter_supported_clients())

    def test_check_absent_all_does_not_hide_unexpected_value_error(self, monkeypatch):
        def _raise_programming_error(*_args, **_kwargs):
            raise ValueError("unknown client programming error")

        monkeypatch.setattr(
            check_module, "iter_supported_clients", lambda: (Client.CURSOR,)
        )
        monkeypatch.setattr(
            check_module,
            "check_absent_client",
            _raise_programming_error,
        )

        with pytest.raises(ValueError, match="unknown client programming error"):
            check_absent_all()


# ── merge helpers ────────────────────────────────────────────────────


class TestMergeHelpers:
    def test_merge_cursor_preserves_third_party_only_dropping_old_runlayer(self):
        existing = {
            "beforeMCPExecution": [
                {"command": "/old/path/aiwatch-hook"},
                {"command": "/usr/local/bin/some-other"},
            ],
        }
        runlayer = {
            "beforeMCPExecution": [{"command": "/new/path/aiwatch-hook"}],
        }
        merged = _merge_cursor_hooks(existing, runlayer)
        commands = [h["command"] for h in merged["beforeMCPExecution"]]
        assert commands == ["/usr/local/bin/some-other", "/new/path/aiwatch-hook"]

    def test_merge_hermes_preserves_third_party_only_dropping_old_runlayer(self):
        existing = {
            "pre_tool_call": [
                {"command": "/old/path/aiwatch-hook"},
                {"command": "/usr/local/bin/some-other"},
            ],
        }
        runlayer = {
            "pre_tool_call": [{"command": "/new/path/aiwatch-hook"}],
        }
        merged = _merge_hermes_hooks(existing, runlayer)
        commands = [h["command"] for h in merged["pre_tool_call"]]
        assert commands == ["/usr/local/bin/some-other", "/new/path/aiwatch-hook"]

    def test_merge_claude_replaces_runlayer_nested(self):
        existing = {
            "PreToolUse": [
                {"matcher": "", "hooks": [{"command": "/old/aiwatch-hook"}]},
                {"matcher": "Bash", "hooks": [{"command": "/usr/bin/echo"}]},
            ]
        }
        runlayer = {
            "PreToolUse": [{"matcher": "", "hooks": [{"command": "/new/aiwatch-hook"}]}]
        }
        merged = _merge_claude_hooks(existing, runlayer)
        # Third-party preserved + new runlayer appended.
        assert any(entry.get("matcher") == "Bash" for entry in merged["PreToolUse"])
        assert any(
            entry["hooks"][0]["command"] == "/new/aiwatch-hook"
            for entry in merged["PreToolUse"]
        )
        # Old runlayer entry gone.
        assert all(
            entry["hooks"][0]["command"] != "/old/aiwatch-hook"
            for entry in merged["PreToolUse"]
        )


# ── Devin CLI install ────────────────────────────────────────────────

_DEVIN_HOOK_COMMAND = "/usr/local/bin/aiwatch-hook"
_DEVIN_EXPECTED_COMMAND = f"{_DEVIN_HOOK_COMMAND} --client devin-cli"
_DEVIN_PIPELINE_EVENTS = (
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "PostToolUse",
    "Stop",
    "PostCompaction",
)


def _devin_config(devin_dir: Path) -> dict:
    return json.loads((devin_dir / "config.json").read_text())


class TestDevinCLIInstall:
    @staticmethod
    def _devin_dir(tmp_path: Path) -> Path:
        devin_dir = tmp_path / ".config" / "devin"
        devin_dir.mkdir(parents=True)
        return devin_dir

    def test_user_writes_nested_enforcement_entry_without_matcher(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        devin_dir = self._devin_dir(tmp_path)

        result = install_client(
            Client.DEVIN_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command=_DEVIN_HOOK_COMMAND,
        )

        assert result.written
        assert result.config_path == devin_dir / "config.json"
        config = _devin_config(devin_dir)
        assert set(config["hooks"]) == {"PreToolUse"}
        # An omitted matcher is Devin's match-all; do not emit an empty one. The
        # 15s timeout caps a network-stalled hook (Devin's default is undocumented).
        assert config["hooks"]["PreToolUse"] == [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": _DEVIN_EXPECTED_COMMAND,
                        "timeout": 15,
                    }
                ]
            }
        ]

    def test_include_pipeline_registers_every_supported_event(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        devin_dir = self._devin_dir(tmp_path)

        install_client(
            Client.DEVIN_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command=_DEVIN_HOOK_COMMAND,
        )

        config = _devin_config(devin_dir)
        # Exact set, so PermissionRequest can never creep in: Devin grants only on
        # an explicit approve decision, and an observational hook registered there
        # would silently suppress prompts the user expected to be asked.
        assert set(config["hooks"]) == {"PreToolUse", *_DEVIN_PIPELINE_EVENTS}
        assert "PermissionRequest" not in config["hooks"]

    def test_install_preserves_unrelated_config_keys_and_third_party_hooks(
        self, tmp_path, monkeypatch
    ):
        """config.json is the user's whole Devin config, not a Runlayer file."""
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        devin_dir = self._devin_dir(tmp_path)
        (devin_dir / "config.json").write_text(
            json.dumps(
                {
                    "model": "devin-2",
                    "read_config_from": {"claude": False},
                    "hooks": {
                        "PreToolUse": [
                            {"hooks": [{"type": "command", "command": "/other/hook"}]}
                        ]
                    },
                }
            )
        )

        install_client(
            Client.DEVIN_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command=_DEVIN_HOOK_COMMAND,
        )

        config = _devin_config(devin_dir)
        assert config["model"] == "devin-2"
        assert config["read_config_from"] == {"claude": False}
        commands = [
            hook["command"]
            for entry in config["hooks"]["PreToolUse"]
            for hook in entry["hooks"]
        ]
        assert "/other/hook" in commands
        assert _DEVIN_EXPECTED_COMMAND in commands

    def test_uninstall_removes_only_runlayer_hooks_and_keeps_the_file(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        devin_dir = self._devin_dir(tmp_path)
        (devin_dir / "config.json").write_text(
            json.dumps(
                {
                    "model": "devin-2",
                    "hooks": {
                        "PreToolUse": [
                            {"hooks": [{"type": "command", "command": "/other/hook"}]}
                        ]
                    },
                }
            )
        )
        install_client(
            Client.DEVIN_CLI,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command=_DEVIN_HOOK_COMMAND,
        )

        result = uninstall_client(Client.DEVIN_CLI, scope=InstallScope.USER)

        assert result.changed
        assert (devin_dir / "config.json").exists()
        config = _devin_config(devin_dir)
        assert config["model"] == "devin-2"
        assert config["hooks"]["PreToolUse"] == [
            {"hooks": [{"type": "command", "command": "/other/hook"}]}
        ]
        for event in _DEVIN_PIPELINE_EVENTS:
            assert event not in config["hooks"]

    def test_check_reports_ok_after_install(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.setattr(
            "runlayer_cli.hook_install.check.client_is_installed",
            lambda *_a, **_k: True,
        )
        self._devin_dir(tmp_path)
        install_client(
            Client.DEVIN_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command=_DEVIN_HOOK_COMMAND,
        )

        result = check_client(
            Client.DEVIN_CLI,
            scope=InstallScope.USER,
            include_pipeline=False,
            expected_hook_command=_DEVIN_HOOK_COMMAND,
        )

        assert result.status == ClientStatus.OK

    def test_windows_mdm_install_refuses_reparse_point(self, tmp_path, monkeypatch):
        """The AIWatchHooks task runs as SYSTEM and Windows has no O_NOFOLLOW
        anchor, so a junction/symlink planted by the console user must not be
        read or rewritten (ENG-3217 / CWE-59,61). Devin gets this from the
        centralized CONSOLE_HOME_CLIENTS preflight rather than a bespoke check."""
        devin_dir = tmp_path / "Users" / "alice" / "AppData" / "Roaming" / "devin"
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module, "enterprise_devin_cli_dir", lambda: devin_dir
        )
        monkeypatch.setattr(
            clients_module, "path_has_link_or_reparse_point", lambda _p: True
        )
        monkeypatch.setattr(clients_module, "_reown_to_console_user", lambda _p: None)

        with pytest.raises(OSError, match="unsafe Windows MDM hooks path"):
            install_client(
                Client.DEVIN_CLI,
                scope=InstallScope.MDM,
                hook_command='"C:\\Program Files\\Runlayer\\AIWatch\\aiwatch.exe" hook',
            )

        assert not (devin_dir / "config.json").exists()

    def test_windows_mdm_uninstall_refuses_reparse_point(self, tmp_path, monkeypatch):
        devin_dir = tmp_path / "Users" / "alice" / "AppData" / "Roaming" / "devin"
        config = devin_dir / "config.json"
        config.parent.mkdir(parents=True)
        config.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "aiwatch hook --client devin-cli",
                                    }
                                ]
                            }
                        ]
                    }
                }
            )
        )
        original = config.read_text()
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module, "enterprise_devin_cli_dir", lambda: devin_dir
        )
        monkeypatch.setattr(
            clients_module, "path_has_link_or_reparse_point", lambda _p: True
        )

        result = uninstall_client(Client.DEVIN_CLI, scope=InstallScope.MDM)

        assert not result.changed
        assert result.skipped_reason == "unsafe Windows MDM hooks path"
        assert config.read_text() == original

    def test_posix_mdm_install_is_unaffected_by_the_windows_preflight(
        self, tmp_path, monkeypatch
    ):
        """POSIX MDM keeps its O_NOFOLLOW anchor, so the preflight must not fire."""
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        devin_dir = console_home / ".config" / "devin"
        devin_dir.mkdir(parents=True)
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            clients_module, "enterprise_devin_cli_dir", lambda: devin_dir
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )
        monkeypatch.setattr(
            clients_module, "path_has_link_or_reparse_point", lambda _p: True
        )
        monkeypatch.setattr(clients_module, "_reown_to_console_user", lambda _p: None)

        result = install_client(
            Client.DEVIN_CLI,
            scope=InstallScope.MDM,
            hook_command=_DEVIN_HOOK_COMMAND,
        )

        assert result.written
        assert (devin_dir / "config.json").is_file()


def test_every_supported_client_resolves_to_a_scan_definition():
    """A hook client whose scan name is missing from the scan registry is
    silently treated as never-installed, so its hooks would never install."""
    from runlayer_cli.hook_install.presence import _CLIENT_SCAN_NAMES
    from runlayer_cli.scan.clients import get_client_by_name

    unresolved = {
        client.value: _CLIENT_SCAN_NAMES.get(client, client.value)
        for client in iter_supported_clients()
        if get_client_by_name(_CLIENT_SCAN_NAMES.get(client, client.value)) is None
    }
    assert unresolved == {}
