"""Single-binary convergence + full-event-set bootstrap (ENG-3184).

Encodes the desired behavior after collapsing ``aiwatch`` + ``aiwatch-hook``
into one binary invoked as ``aiwatch hook --client <name>``:

* ``resolve_hook_command`` resolves the ``aiwatch`` binary and appends the
  ``hook`` subcommand (no separate ``aiwatch-hook`` exe).
* Installs write ``<aiwatch> hook --client <name>`` for every scope and never
  create per-client symlinks.
* The drift check flags a partial install (enforcement-only when the event set
  is expected) as DRIFTED so remediation re-runs.
* ``resolve_include_pipeline`` drives the full-vs-enforce decision from the MDM
  ``Sessions`` config (default on), independent of install scope.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from runlayer_cli.hook_install import (
    Client,
    ClientStatus,
    InstallScope,
    check_client,
    install_client,
)
from runlayer_cli.hook_install import paths as paths_module
from runlayer_cli.hook_install.clients import expected_event_names
from runlayer_cli.mdm_config import resolve_include_pipeline


# ── resolve_hook_command appends the hook subcommand ────────────────────


class TestResolveHookCommand:
    def test_appends_hook_subcommand(self, monkeypatch):
        monkeypatch.setattr(
            paths_module,
            "resolve_hook_binary",
            lambda: Path("/usr/local/bin/aiwatch"),
        )
        assert paths_module.resolve_hook_command() == "/usr/local/bin/aiwatch hook"

    def test_quotes_path_with_spaces_then_appends_hook(self, monkeypatch):
        monkeypatch.setattr(
            paths_module,
            "resolve_hook_binary",
            lambda: Path("/opt/Runlayer App/aiwatch"),
        )
        assert paths_module.resolve_hook_command() == '"/opt/Runlayer App/aiwatch" hook'

    def test_resolves_aiwatch_binary_not_hook_binary(self, tmp_path, monkeypatch):
        # Frozen bundle dir contains only ``aiwatch`` now.
        monkeypatch.setattr(paths_module, "_frozen_bundle_dir", lambda: tmp_path)
        (tmp_path / "aiwatch").touch()
        resolved = paths_module.resolve_hook_binary()
        assert resolved == tmp_path / "aiwatch"


# ── installs use command strings + no symlinks ──────────────────────────


class TestNoSymlinkCommandStrings:
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


# ── drift check verifies the full expected event set ────────────────────


class TestCheckEventSetCompleteness:
    def test_enforcement_only_is_drifted_when_pipeline_expected(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
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
        (tmp_path / ".cursor").mkdir()
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
        (tmp_path / ".cursor").mkdir()
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


# ── resolve_include_pipeline: config-driven, scope-independent ──────────


class TestResolveIncludePipeline:
    def test_all_events_forces_true(self):
        assert resolve_include_pipeline(True, managed={"sessions": False}) is True

    def test_sessions_false_excludes(self):
        assert resolve_include_pipeline(False, managed={"sessions": False}) is False

    def test_sessions_absent_defaults_true(self):
        assert resolve_include_pipeline(False, managed={}) is True

    def test_sessions_true_includes(self):
        assert resolve_include_pipeline(False, managed={"sessions": True}) is True
