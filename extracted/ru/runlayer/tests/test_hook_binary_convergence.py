"""Native hook shim selection + full-event-set bootstrap.

Encodes the managed hook command contract:

* Gate-open frozen bundles use the sibling native shim; all other states fall
  back to ``aiwatch hook``.
* Installs append ``--client <name>`` and never create per-client symlinks.
* The drift check flags a partial install (enforcement-only when the event set
  is expected) as DRIFTED so the next hooks re-assert (macOS bootstrap
  LaunchDaemon / Windows AIWatchHooks scheduled task) re-runs the install.
* ``resolve_include_pipeline`` drives the full-vs-enforce decision from the
  resolved ``Sessions`` config (missing fails closed), independent of scope.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from runlayer_cli import regex_safe as re
from runlayer_cli.hook.daemon_protocol import HOOK_ENV_ALLOWLIST
from runlayer_cli.hook_install import (
    Client,
    ClientStatus,
    InstallScope,
    check_client,
    install_client,
)
from runlayer_cli.hook_install import paths as paths_module
from runlayer_cli.hook_install.clients import expected_event_names
import runlayer_cli.mdm_config as mdm_config
from runlayer_cli.mdm_config import resolve_include_pipeline


# ── resolve_hook_command selects the managed shim ───────────────────────


def _seed_frozen_aiwatch_bundle(
    tmp_path: Path,
    monkeypatch,
    *,
    system: str = "Darwin",
    with_shim: bool = True,
) -> tuple[Path, Path]:
    bundle_dir = tmp_path / ("Program Files" if system == "Windows" else "AIWatch")
    bundle_dir.mkdir()
    aiwatch_name = "aiwatch.exe" if system == "Windows" else "aiwatch"
    shim_name = "aiwatch-hook.exe" if system == "Windows" else "aiwatch-hook"
    aiwatch = bundle_dir / aiwatch_name
    shim = bundle_dir / shim_name
    aiwatch.touch()
    if with_shim:
        shim.touch()
    monkeypatch.setattr(paths_module.sys, "frozen", True, raising=False)
    monkeypatch.setattr(paths_module.sys, "executable", str(aiwatch), raising=False)
    monkeypatch.setattr(paths_module.platform, "system", lambda: system)
    return aiwatch, shim


class TestResolveHookCommand:
    def test_gate_open_uses_sibling_shim(self, tmp_path, monkeypatch):
        _aiwatch, shim = _seed_frozen_aiwatch_bundle(tmp_path, monkeypatch)
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"org_api_key": "rl_org_test", "daemon_enabled": True},
        )

        assert paths_module.resolve_hook_shim_binary() == shim
        assert paths_module.resolve_hook_command() == f"{shim} hook"

    def test_linux_bundle_keeps_native_shim_dormant(self, tmp_path, monkeypatch):
        aiwatch, _shim = _seed_frozen_aiwatch_bundle(
            tmp_path, monkeypatch, system="Linux"
        )
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"org_api_key": "rl_org_test", "daemon_enabled": True},
        )

        assert paths_module.resolve_hook_shim_binary() is None
        assert paths_module.resolve_hook_command() == f"{aiwatch} hook"

    def test_gate_off_uses_aiwatch(self, tmp_path, monkeypatch):
        aiwatch, _shim = _seed_frozen_aiwatch_bundle(tmp_path, monkeypatch)
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"org_api_key": "rl_org_test", "daemon_enabled": False},
        )

        assert paths_module.resolve_hook_command() == f"{aiwatch} hook"

    def test_missing_org_key_uses_aiwatch(self, tmp_path, monkeypatch):
        aiwatch, _shim = _seed_frozen_aiwatch_bundle(tmp_path, monkeypatch)
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"daemon_enabled": True},
        )

        assert paths_module.resolve_hook_command() == f"{aiwatch} hook"

    def test_gate_open_without_sibling_shim_uses_aiwatch(self, tmp_path, monkeypatch):
        aiwatch, shim = _seed_frozen_aiwatch_bundle(
            tmp_path, monkeypatch, with_shim=False
        )
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"org_api_key": "rl_org_test", "daemon_enabled": True},
        )

        assert paths_module.resolve_hook_shim_binary() is None
        assert not shim.exists()
        assert paths_module.resolve_hook_command() == f"{aiwatch} hook"

    def test_managed_config_read_error_uses_aiwatch(self, tmp_path, monkeypatch):
        aiwatch, _shim = _seed_frozen_aiwatch_bundle(tmp_path, monkeypatch)

        def _raise_read_error():
            raise OSError("managed config unavailable")

        monkeypatch.setattr(mdm_config, "read_managed_config", _raise_read_error)

        assert paths_module.resolve_hook_command() == f"{aiwatch} hook"

    def test_gate_error_uses_aiwatch(self, tmp_path, monkeypatch):
        aiwatch, _shim = _seed_frozen_aiwatch_bundle(tmp_path, monkeypatch)
        monkeypatch.setattr(mdm_config, "read_managed_config", lambda: {})

        def _raise_gate_error(_managed):
            raise ValueError("invalid managed config")

        monkeypatch.setattr(mdm_config, "daemon_gate_open", _raise_gate_error)

        assert paths_module.resolve_hook_command() == f"{aiwatch} hook"

    def test_unfrozen_aiwatch_does_not_resolve_adjacent_shim(
        self, tmp_path, monkeypatch
    ):
        aiwatch = tmp_path / "aiwatch"
        shim = tmp_path / "aiwatch-hook"
        aiwatch.touch()
        shim.touch()
        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(paths_module, "_PREFERRED_SYMLINK_UNIX", aiwatch)
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"org_api_key": "rl_org_test", "daemon_enabled": True},
        )

        assert paths_module.resolve_hook_shim_binary() is None
        assert paths_module.resolve_hook_command() == f"{aiwatch} hook"

    def test_windows_shim_basename_and_path_quoting(self, tmp_path, monkeypatch):
        _aiwatch, shim = _seed_frozen_aiwatch_bundle(
            tmp_path, monkeypatch, system="Windows"
        )
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"org_api_key": "rl_org_test", "daemon_enabled": True},
        )

        assert shim.name == "aiwatch-hook.exe"
        assert paths_module.resolve_hook_shim_binary() == shim
        assert paths_module.resolve_hook_command() == f'"{shim}" hook'

    def test_fallback_shim_behavior_is_preserved(self, tmp_path, monkeypatch):
        fallback = tmp_path / "dev hook"
        monkeypatch.setattr(paths_module, "resolve_hook_binary", lambda: None)

        assert paths_module.resolve_hook_command(fallback) == f'"{fallback}" hook'


class TestNativeShimContract:
    def test_environment_allowlist_matches_python_protocol(self):
        repo_root = Path(__file__).resolve().parents[2]
        source = (
            repo_root / "aiwatch-hook-shim" / "internal" / "shim" / "request.go"
        ).read_text(encoding="utf-8")
        block = re.search(
            r"var HookEnvAllowlist = map\[string\]struct\{\}\{\n(?P<body>.*?)^\}",
            source,
            re.MULTILINE | re.DOTALL,
        )
        assert block is not None
        go_allowlist = frozenset(
            re.findall(r'^\s*"([^"]+)":\s*\{\},\s*$', block.group("body"), re.MULTILINE)
        )

        assert go_allowlist == HOOK_ENV_ALLOWLIST


# ── resolve_runlayer_hook_command: operator (full runlayer CLI) path ────


class TestResolveRunlayerHookCommand:
    """Operator path resolves the full ``runlayer`` CLI's ``hook`` subcommand.

    Chain: frozen ``runlayer`` exe -> ``runlayer`` on ``PATH`` -> a
    ``"<python>" -m runlayer_cli.hook`` module fallback.
    """

    def test_frozen_uses_running_executable(self, monkeypatch):
        monkeypatch.setattr(paths_module.sys, "frozen", True, raising=False)
        monkeypatch.setattr(
            paths_module.sys, "executable", "/opt/Runlayer/runlayer", raising=False
        )
        assert (
            paths_module.resolve_runlayer_hook_command()
            == "/opt/Runlayer/runlayer hook"
        )

    def test_frozen_quotes_path_with_spaces(self, monkeypatch):
        monkeypatch.setattr(paths_module.sys, "frozen", True, raising=False)
        monkeypatch.setattr(
            paths_module.sys,
            "executable",
            "/opt/Runlayer App/runlayer",
            raising=False,
        )
        assert (
            paths_module.resolve_runlayer_hook_command()
            == '"/opt/Runlayer App/runlayer" hook'
        )

    def test_native_shim_does_not_change_operator_target(self, tmp_path, monkeypatch):
        bundle_dir = tmp_path / "Runlayer App"
        bundle_dir.mkdir()
        runlayer = bundle_dir / "runlayer"
        runlayer.touch()
        (bundle_dir / "aiwatch-hook").touch()
        monkeypatch.setattr(paths_module.sys, "frozen", True, raising=False)
        monkeypatch.setattr(
            paths_module.sys, "executable", str(runlayer), raising=False
        )
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"org_api_key": "rl_org_test", "daemon_enabled": True},
        )

        assert paths_module.resolve_runlayer_hook_command() == f'"{runlayer}" hook'

    def test_unfrozen_uses_runlayer_on_path(self, monkeypatch):
        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Linux")
        monkeypatch.setattr(
            paths_module.shutil, "which", lambda name: "/usr/local/bin/runlayer"
        )
        assert (
            paths_module.resolve_runlayer_hook_command()
            == "/usr/local/bin/runlayer hook"
        )

    def test_unfrozen_looks_up_windows_basename(self, monkeypatch):
        seen: dict[str, str] = {}

        def fake_which(name):
            seen["name"] = name
            return r"C:\Program Files\Runlayer\runlayer.exe"

        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(paths_module.shutil, "which", fake_which)
        command = paths_module.resolve_runlayer_hook_command()
        assert seen["name"] == "runlayer.exe"
        assert command == r'"C:\Program Files\Runlayer\runlayer.exe" hook'

    def test_unfrozen_prefers_invoked_binary_over_path(self, tmp_path, monkeypatch):
        # `uv run /path/to/runlayer setup hooks` must wire the invoked binary,
        # not a different `runlayer` earlier on PATH.
        invoked = tmp_path / "runlayer"
        invoked.touch()
        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Linux")
        monkeypatch.setattr(paths_module.sys, "argv", [str(invoked), "setup", "hooks"])
        monkeypatch.setattr(
            paths_module.shutil, "which", lambda name: "/usr/local/bin/runlayer"
        )
        resolved = invoked.resolve()
        assert paths_module.resolve_runlayer_hook_command() == f"{resolved} hook"

    def test_unfrozen_falls_back_to_path_when_argv0_not_runlayer(self, monkeypatch):
        # `python -m runlayer_cli` (argv[0] basename != runlayer) => use PATH.
        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Linux")
        monkeypatch.setattr(
            paths_module.sys, "argv", ["/opt/py/bin/python", "-m", "runlayer_cli"]
        )
        monkeypatch.setattr(
            paths_module.shutil, "which", lambda name: "/usr/local/bin/runlayer"
        )
        assert (
            paths_module.resolve_runlayer_hook_command()
            == "/usr/local/bin/runlayer hook"
        )

    def test_unfrozen_falls_back_to_path_when_invoked_binary_absent(self, monkeypatch):
        # argv[0] basename matches but the path doesn't exist (e.g. bare name
        # resolved against CWD) => fall through to PATH.
        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Linux")
        monkeypatch.setattr(
            paths_module.sys, "argv", ["/nonexistent/runlayer", "setup"]
        )
        monkeypatch.setattr(
            paths_module.shutil, "which", lambda name: "/usr/local/bin/runlayer"
        )
        assert (
            paths_module.resolve_runlayer_hook_command()
            == "/usr/local/bin/runlayer hook"
        )

    def test_module_fallback_when_no_binary(self, monkeypatch):
        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Linux")
        monkeypatch.setattr(paths_module.shutil, "which", lambda name: None)
        monkeypatch.setattr(
            paths_module.sys, "executable", "/opt/py/bin/python", raising=False
        )
        assert (
            paths_module.resolve_runlayer_hook_command()
            == "/opt/py/bin/python -m runlayer_cli.hook"
        )

    def test_module_fallback_quotes_python_with_spaces(self, monkeypatch):
        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Linux")
        monkeypatch.setattr(paths_module.shutil, "which", lambda name: None)
        monkeypatch.setattr(
            paths_module.sys,
            "executable",
            "/opt/Runlayer CLI/bin/python",
            raising=False,
        )
        assert (
            paths_module.resolve_runlayer_hook_command()
            == '"/opt/Runlayer CLI/bin/python" -m runlayer_cli.hook'
        )


class TestRunlayerHookCommandUsesModuleFallback:
    """Predicate tracks resolve_runlayer_hook_command()'s module-fallback branch."""

    def test_false_when_frozen(self, monkeypatch):
        monkeypatch.setattr(paths_module.sys, "frozen", True, raising=False)
        monkeypatch.setattr(
            paths_module.sys, "executable", "/opt/Runlayer/runlayer", raising=False
        )
        assert paths_module.runlayer_hook_command_uses_module_fallback() is False

    def test_false_when_runlayer_on_path(self, monkeypatch):
        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Linux")
        monkeypatch.setattr(
            paths_module.shutil, "which", lambda name: "/usr/local/bin/runlayer"
        )
        assert paths_module.runlayer_hook_command_uses_module_fallback() is False

    def test_true_when_no_binary(self, monkeypatch):
        monkeypatch.setattr(paths_module.sys, "frozen", False, raising=False)
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Linux")
        monkeypatch.setattr(paths_module.shutil, "which", lambda name: None)
        assert paths_module.runlayer_hook_command_uses_module_fallback() is True


# ── installs use command strings + no symlinks ──────────────────────────


class TestNoSymlinkCommandStrings:
    def test_metadata_only_replaces_full_cursor_profile_exactly(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        drifted = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=False,
            metadata_only=True,
        )
        assert drifted.status == ClientStatus.DRIFTED
        assert "unexpected event hooks" in drifted.detail

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=False,
            metadata_only=True,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        data = json.loads((tmp_path / ".cursor" / "hooks.json").read_text())
        assert set(data["hooks"]) == {"beforeMCPExecution"}
        assert (
            check_client(
                Client.CURSOR,
                scope=InstallScope.USER,
                expected_hook_command="/usr/local/bin/aiwatch hook",
                include_pipeline=False,
                metadata_only=True,
            ).status
            == ClientStatus.OK
        )

    def test_user_cursor_writes_hook_command_no_symlink(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        data = json.loads((tmp_path / ".cursor" / "hooks.json").read_text())
        assert (
            data["hooks"]["beforeMCPExecution"][0]["command"]
            == "/usr/local/bin/aiwatch hook --client cursor"
        )
        assert not (tmp_path / ".cursor" / "hooks").exists()

    def test_mdm_cursor_writes_hook_command_no_symlink(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import clients as clients_module

        enterprise_root = tmp_path / "enterprise" / "Cursor"
        monkeypatch.setattr(
            clients_module, "enterprise_cursor_dir", lambda: enterprise_root
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        data = json.loads((enterprise_root / "hooks.json").read_text())
        assert (
            data["hooks"]["beforeMCPExecution"][0]["command"]
            == "/usr/local/bin/aiwatch hook --client cursor"
        )
        # No per-client symlink dir is created any more.
        assert not (enterprise_root / "hooks" / "aiwatch-hook").exists()
        assert not (enterprise_root / "hooks" / "aiwatch").exists()

    def test_mdm_hermes_writes_hook_command_no_symlink(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_hermes_root = tmp_path / "Users" / "alice" / ".hermes"
        monkeypatch.setattr(
            clients_module, "enterprise_hermes_dir", lambda: console_hermes_root
        )
        monkeypatch.setattr(
            console_user_module,
            "find_console_user_home",
            lambda: tmp_path / "Users" / "alice",
        )

        install_client(
            Client.HERMES,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        config = yaml.safe_load((console_hermes_root / "config.yaml").read_text())
        assert (
            config["hooks"]["pre_tool_call"][0]["command"]
            == "/usr/local/bin/aiwatch hook --client hermes"
        )
        assert not (console_hermes_root / "agent-hooks").exists()

    def test_stale_aiwatch_hook_entry_is_replaced(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()
        (cursor_dir / "hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": "/old/aiwatch-hook --client cursor"},
                        ]
                    },
                }
            )
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        data = json.loads((cursor_dir / "hooks.json").read_text())
        commands = [e["command"] for e in data["hooks"]["beforeMCPExecution"]]
        assert commands == ["/usr/local/bin/aiwatch hook --client cursor"]

    def test_old_aiwatch_command_drifts_then_install_replaces_it(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        aiwatch, shim = _seed_frozen_aiwatch_bundle(tmp_path, monkeypatch)
        monkeypatch.setattr(
            mdm_config,
            "read_managed_config",
            lambda: {"org_api_key": "rl_org_test", "daemon_enabled": True},
        )
        old_command = f"{aiwatch} hook"
        new_command = paths_module.resolve_hook_command()
        assert new_command == f"{shim} hook"

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command=old_command,
        )

        drifted = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            expected_hook_command=new_command,
            include_pipeline=False,
        )
        assert drifted.status == ClientStatus.DRIFTED
        assert "does not match" in drifted.detail

        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
        )

        data = json.loads((tmp_path / ".cursor" / "hooks.json").read_text())
        commands = [e["command"] for e in data["hooks"]["beforeMCPExecution"]]
        assert commands == [f"{new_command} --client cursor"]
        assert (
            check_client(
                Client.CURSOR,
                scope=InstallScope.USER,
                expected_hook_command=new_command,
                include_pipeline=False,
            ).status
            == ClientStatus.OK
        )

    def test_gate_close_makes_installed_shim_drifted(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        aiwatch, shim = _seed_frozen_aiwatch_bundle(tmp_path, monkeypatch)
        managed = {"org_api_key": "rl_org_test", "daemon_enabled": True}
        monkeypatch.setattr(mdm_config, "read_managed_config", lambda: managed)

        shim_command = paths_module.resolve_hook_command()
        assert shim_command == f"{shim} hook"
        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            hook_command=shim_command,
        )

        managed["daemon_enabled"] = False
        fallback_command = paths_module.resolve_hook_command()
        assert fallback_command == f"{aiwatch} hook"
        drifted = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=False,
        )

        assert drifted.status == ClientStatus.DRIFTED
        assert "does not match" in drifted.detail


# ── drift check verifies the full expected event set ────────────────────


def _mark_cursor_installed(home: Path, monkeypatch) -> None:
    """Seed cursor's config plus the executable the presence gate requires.

    Config files survive uninstall, so they alone no longer prove a client is
    installed. Stubbing the binary probe (rather than dropping a real file in
    *home*) also keeps a host-installed CLI from leaking in as a second client.
    """
    from runlayer_cli.scan import client_presence

    config_path = home / ".cursor" / "mcp.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("{}")
    monkeypatch.setattr(
        client_presence,
        "locate_cli_binary",
        lambda binary, **_kwargs: Path("/test/cursor") if binary == "cursor" else None,
    )


class TestCheckEventSetCompleteness:
    def test_enforcement_only_is_drifted_when_pipeline_expected(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        result = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )
        assert result.status == ClientStatus.DRIFTED
        assert "missing" in result.detail.lower()

    def test_full_set_is_ok_when_pipeline_expected(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=True,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        result = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=True,
        )
        assert result.status == ClientStatus.OK

    def test_enforcement_only_is_ok_when_pipeline_not_expected(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        install_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            include_pipeline=False,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        result = check_client(
            Client.CURSOR,
            scope=InstallScope.USER,
            expected_hook_command="/usr/local/bin/aiwatch hook",
            include_pipeline=False,
        )
        assert result.status == ClientStatus.OK


class TestExpectedEventNames:
    def test_enforcement_subset_of_full(self):
        enforce = expected_event_names(Client.CURSOR, include_pipeline=False)
        full = expected_event_names(Client.CURSOR, include_pipeline=True)
        assert enforce
        assert enforce < full
        assert "sessionStart" in full
        assert "sessionStart" not in enforce

    @pytest.mark.parametrize(
        ("client", "event_name"),
        [
            (Client.CURSOR, "beforeMCPExecution"),
            (Client.VSCODE, "PreToolUse"),
            (Client.CLAUDE_CODE, "PreToolUse"),
            (Client.CODEX, "PreToolUse"),
            (Client.HERMES, "pre_tool_call"),
            (Client.GOOSE, "PreToolUse"),
            (Client.GITHUB_COPILOT_CLI, "PreToolUse"),
            (Client.WINDSURF, "pre_mcp_tool_use"),
            (Client.QWEN_CODE, "PreToolUse"),
            (Client.GEMINI_CLI, "BeforeTool"),
            (Client.CLINE_CLI, "PreToolUse"),
        ],
    )
    def test_metadata_only_registers_one_pre_call_hook(self, client, event_name):
        assert expected_event_names(
            client,
            include_pipeline=False,
            metadata_only=True,
        ) == {event_name}


# ── resolve_include_pipeline: config-driven, scope-independent ──────────


class TestResolveIncludePipeline:
    def test_all_events_forces_true(self):
        assert resolve_include_pipeline(True, managed={"sessions": False}) is True

    def test_sessions_false_excludes(self):
        assert resolve_include_pipeline(False, managed={"sessions": False}) is False

    def test_sessions_absent_fails_closed(self):
        assert resolve_include_pipeline(False, managed={}) is False

    def test_sessions_true_includes(self):
        assert resolve_include_pipeline(False, managed={"sessions": True}) is True
