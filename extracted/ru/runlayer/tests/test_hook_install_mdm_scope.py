"""MDM-scope writer tests for ``runlayer_cli.hook_install`` (enterprise/console-home writes + ENG-3217 link safety)."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
import yaml

from runlayer_cli.hook_install import (
    Client,
    InstallScope,
    install_client,
)
from runlayer_cli.hook_install import console_user as console_user_module
from runlayer_cli.hook_install.clients import _vscode_user_settings_path
from runlayer_cli.hook_install.safe_fs import console_home_anchor


def _patch_console_home(monkeypatch, home: Path | None) -> None:
    """Pin ``find_console_user_home`` so the anchor resolves deterministically.

    ``console_home_anchor`` lazily imports it from ``console_user``, so patching
    the module attribute is picked up at call time.
    """
    monkeypatch.setattr(console_user_module, "find_console_user_home", lambda: home)


class TestConsoleHomeAnchor:
    """The O_NOFOLLOW anchor is the console user's home, not ``config_dir.parent``.

    Regression guard (ENG-3217): the trust boundary is the console user's home
    (whose parent ``/Users`` / ``/home`` is root-owned), resolved from
    ``find_console_user_home()`` — not the config file's depth. A future deeper
    config dir must not silently start the link-safe walk inside user-controlled
    territory.
    """

    def test_mdm_anchor_is_console_home(self, monkeypatch):
        _patch_console_home(monkeypatch, Path("/Users/alice"))
        config_dir = Path("/Users/alice/.claude")
        assert console_home_anchor(config_dir, mdm=True) == Path("/Users/alice")

    def test_user_scope_has_no_anchor(self, monkeypatch):
        _patch_console_home(monkeypatch, Path("/Users/alice"))
        config_dir = Path("/Users/alice/.claude")
        assert console_home_anchor(config_dir, mdm=False) is None

    def test_anchor_independent_of_file_nesting(self, monkeypatch):
        # A deeper client dir still anchors on the console home — not on the
        # config dir's parent (which would be user-controlled territory).
        _patch_console_home(monkeypatch, Path("/home/bob"))
        config_dir = Path("/home/bob/.config/runlayer")
        assert console_home_anchor(config_dir, mdm=True) == Path("/home/bob")

    def test_falls_back_to_config_dir_parent_without_console_user(self, monkeypatch):
        # No console user (dev / single-user, where enterprise_*_dir falls back
        # to Path.home()/.client): the anchor is config_dir.parent — the running
        # user's own home.
        _patch_console_home(monkeypatch, None)
        config_dir = Path("/Users/alice/.claude")
        assert console_home_anchor(config_dir, mdm=True) == Path("/Users/alice")

    def test_falls_back_to_running_home_for_nested_vscode_dir(
        self, tmp_path, monkeypatch
    ):
        _patch_console_home(monkeypatch, None)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        config_dir = tmp_path / ".copilot" / "hooks"

        assert console_home_anchor(config_dir, mdm=True) == tmp_path


def _spy_fchown(monkeypatch) -> list[tuple[int, int, int]]:
    """Record ``(st_ino, uid, gid)`` for every ``os.fchown`` and still apply it.

    Inode-based (not path-based) so the assertion is independent of whether the
    reown follows a symlink — the whole point of the regression: a vulnerable
    chown would land on the *outside* target's inode.
    """
    records: list[tuple[int, int, int]] = []
    real_fchown = os.fchown

    def spy(fd: int, uid: int, gid: int) -> None:
        try:
            records.append((os.fstat(fd).st_ino, uid, gid))
        except OSError:
            pass
        return real_fchown(fd, uid, gid)

    monkeypatch.setattr(os, "fchown", spy)
    return records


class TestMDMScopeWrites:
    """MDM-scope writers target enterprise dirs and use scope-aware filenames.

    The converged binary is wired in as a ``"<aiwatch>" hook --client <name>``
    command string for every scope — no per-client symlink is created.
    """

    def test_mdm_cursor_writes_to_enterprise_dir(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import clients as clients_module

        enterprise_root = tmp_path / "enterprise" / "Cursor"
        monkeypatch.setattr(
            clients_module,
            "enterprise_cursor_dir",
            lambda: enterprise_root,
        )

        install_client(
            Client.CURSOR,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        assert (enterprise_root / "hooks.json").exists()
        data = json.loads((enterprise_root / "hooks.json").read_text())
        command = data["hooks"]["beforeMCPExecution"][0]["command"]
        assert command == "/usr/local/bin/aiwatch hook --client cursor"
        assert not (enterprise_root / "hooks").exists()
        # MDM scope writes unconditionally — no user-dir prerequisite.
        assert not (tmp_path / ".cursor").exists()

    def test_mdm_claude_code_writes_console_user_settings_json(
        self, tmp_path, monkeypatch
    ):
        """Claude Code managed-settings hooks regressed (ENG-3204) — MDM scope
        targets the console user's ``~/.claude/settings.json`` (user hooks
        still fire) instead of the enterprise managed-settings.json."""
        from runlayer_cli.hook_install import clients as clients_module

        console_claude_root = tmp_path / "Users" / "alice" / ".claude"
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_claude_root,
        )
        _patch_console_home(monkeypatch, tmp_path / "Users" / "alice")

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        # MDM scope uses settings.json (not managed-settings.json).
        assert (console_claude_root / "settings.json").exists()
        settings = json.loads((console_claude_root / "settings.json").read_text())
        command = settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        assert command == "/usr/local/bin/aiwatch hook --client claude_code"
        assert not (console_claude_root / "hooks").exists()
        assert not (console_claude_root / "managed-settings.json").exists()

    def test_mdm_claude_code_preserves_unparseable_settings(
        self, tmp_path, monkeypatch
    ):
        """An existing settings file must survive a failed merge byte-for-byte."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        settings_path = console_claude_root / "settings.json"
        original = '{"permissions": {"allow": ["Bash"]}'
        settings_path.write_text(original)
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_claude_root,
        )
        _patch_console_home(monkeypatch, console_home)

        with pytest.raises(OSError, match="invalid Claude Code settings"):
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        assert settings_path.read_text() == original

    def test_mdm_claude_code_preserves_empty_settings(
        self, tmp_path, monkeypatch
    ):
        """A transient empty file must fail closed and remain untouched."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        settings_path = console_claude_root / "settings.json"
        original = "  \n"
        settings_path.write_text(original)
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_claude_root,
        )
        _patch_console_home(monkeypatch, console_home)

        with pytest.raises(OSError, match="invalid Claude Code settings"):
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        assert settings_path.read_text() == original

    def test_mdm_claude_code_preserves_undecodable_settings(
        self, tmp_path, monkeypatch
    ):
        """An existing non-UTF-8 settings file must never be treated as absent."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        settings_path = console_claude_root / "settings.json"
        original = b'{"permissions": "keep"}\xff'
        settings_path.write_bytes(original)
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_claude_root,
        )
        _patch_console_home(monkeypatch, console_home)

        with pytest.raises(OSError, match="invalid Claude Code settings"):
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        assert settings_path.read_bytes() == original

    def test_mdm_claude_code_backs_up_existing_settings_before_merge(
        self, tmp_path, monkeypatch
    ):
        """The packaged MDM path keeps the engineer's pre-merge settings."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        settings_path = console_claude_root / "settings.json"
        original = json.dumps(
            {
                "permissions": {"allow": ["Bash"], "deny": ["WebFetch"]},
                "sandbox": {"enabled": True},
                "statusLine": {"type": "command", "command": "statusline"},
                "enabledPlugins": {"linear@claude-plugins-official": True},
                "model": "claude-opus-4-1",
            },
            indent=2,
        )
        settings_path.write_text(original)
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_claude_root,
        )
        _patch_console_home(monkeypatch, console_home)

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        backups = list(console_claude_root.glob("settings.backup_*.json"))
        assert len(backups) == 1
        assert backups[0].read_text() == original
        updated = json.loads(settings_path.read_text())
        assert updated["permissions"] == {"allow": ["Bash"], "deny": ["WebFetch"]}
        assert updated["sandbox"] == {"enabled": True}
        assert updated["statusLine"] == {
            "type": "command",
            "command": "statusline",
        }
        assert updated["enabledPlugins"] == {
            "linear@claude-plugins-official": True
        }
        assert updated["model"] == "claude-opus-4-1"

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )
        assert list(console_claude_root.glob("settings.backup_*.json")) == backups

    def test_mdm_claude_code_preserves_restrictive_settings_mode(
        self, tmp_path, monkeypatch
    ):
        """Backups and rewritten settings keep the engineer's owner-only mode."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        settings_path = console_claude_root / "settings.json"
        settings_path.write_text('{"permissions": {"allow": ["Bash"]}}')
        settings_path.chmod(0o600)
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_claude_root,
        )
        _patch_console_home(monkeypatch, console_home)

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        [backup_path] = list(console_claude_root.glob("settings.backup_*.json"))
        assert settings_path.stat().st_mode & 0o777 == 0o600
        assert backup_path.stat().st_mode & 0o777 == 0o600

    def test_mdm_claude_code_reowns_backup_before_rewrite(
        self, tmp_path, monkeypatch
    ):
        """A failed active write must not strand its recovery backup as root."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_home.mkdir(parents=True)
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir()
        settings_path = console_claude_root / "settings.json"
        settings_path.write_text('{"permissions": {"allow": ["Bash"]}}')
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_claude_root,
        )
        _patch_console_home(monkeypatch, console_home)
        monkeypatch.setattr(console_user_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            console_user_module.os, "geteuid", lambda: 0, raising=False
        )
        records = _spy_fchown(monkeypatch)
        real_write_config = clients_module._write_config

        def fail_active_write(path, text, **kwargs):
            if path == settings_path:
                raise OSError("active write failed")
            return real_write_config(path, text, **kwargs)

        monkeypatch.setattr(clients_module, "_write_config", fail_active_write)

        with pytest.raises(OSError, match="active write failed"):
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        [backup_path] = list(console_claude_root.glob("settings.backup_*.json"))
        chowned_inos = {ino for ino, _, _ in records}
        assert backup_path.stat().st_ino in chowned_inos
        assert settings_path.stat().st_ino not in chowned_inos

    def test_mdm_vscode_writes_console_user_copilot_hook_file(
        self, tmp_path, monkeypatch
    ):
        """VS Code's supported hook location is a user-level Copilot hook file,
        so MDM scope writes the console user's ``~/.copilot/hooks/runlayer.json``."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_vscode_root = console_home / ".copilot" / "hooks"
        monkeypatch.setattr(
            clients_module,
            "enterprise_vscode_dir",
            lambda: console_vscode_root,
        )
        _patch_console_home(monkeypatch, console_home)

        install_client(
            Client.VSCODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        path = console_vscode_root / "runlayer.json"
        assert path.exists()
        data = json.loads(path.read_text())
        command = data["hooks"]["PreToolUse"][0]["command"]
        assert command == "/usr/local/bin/aiwatch hook --client vscode"
        assert data["hooks"]["PreToolUse"][0]["type"] == "command"
        settings = json.loads(_vscode_user_settings_path(console_home).read_text())
        assert settings["chat.hookFilesLocations"]["~/.claude/settings.json"] is False

    def test_mdm_claude_code_reowns_console_user_settings_to_owner(
        self, tmp_path, monkeypatch
    ):
        """Running as root, MDM Claude Code install chowns the file + created
        ~/.claude dir back to the console user (ENG-3204): a root:wheel
        settings.json would block the user's own /config writes."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        console_home.mkdir(parents=True)
        console_claude_root = console_home / ".claude"
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_claude_root,
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )
        monkeypatch.setattr(console_user_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(console_user_module.os, "geteuid", lambda: 0, raising=False)
        records = _spy_fchown(monkeypatch)

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        settings_path = console_claude_root / "settings.json"
        assert settings_path.exists()
        home_stat = os.stat(console_home)
        chowned_inos = {ino for ino, _, _ in records}
        # File + the ~/.claude dir root created are re-owned; home itself is not.
        assert settings_path.stat().st_ino in chowned_inos
        assert console_claude_root.stat().st_ino in chowned_inos
        assert console_home.stat().st_ino not in chowned_inos
        for _, uid, gid in records:
            assert uid == home_stat.st_uid
            assert gid == home_stat.st_gid

    def test_mdm_claude_code_non_root_does_not_chown(self, tmp_path, monkeypatch):
        """Non-root MDM install (dev / single-user) leaves ownership alone."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_claude_root = tmp_path / "Users" / "alice" / ".claude"
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_claude_root,
        )
        _patch_console_home(monkeypatch, tmp_path / "Users" / "alice")
        monkeypatch.setattr(
            console_user_module.os, "geteuid", lambda: 501, raising=False
        )
        records = _spy_fchown(monkeypatch)

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        assert (console_claude_root / "settings.json").exists()
        assert records == []

    def test_mdm_hermes_reowns_console_user_config_to_owner(
        self, tmp_path, monkeypatch
    ):
        """Root MDM Hermes install chowns ~/.hermes/config.yaml back to the owner."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import console_user as console_user_module

        console_home = tmp_path / "Users" / "alice"
        console_home.mkdir(parents=True)
        console_hermes_root = console_home / ".hermes"
        monkeypatch.setattr(
            clients_module,
            "enterprise_hermes_dir",
            lambda: console_hermes_root,
        )
        monkeypatch.setattr(
            console_user_module, "find_console_user_home", lambda: console_home
        )
        monkeypatch.setattr(console_user_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(console_user_module.os, "geteuid", lambda: 0, raising=False)
        records = _spy_fchown(monkeypatch)

        install_client(
            Client.HERMES,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
            skip_when_missing=False,
        )

        config_path = console_hermes_root / "config.yaml"
        assert config_path.exists()
        chowned_inos = {ino for ino, _, _ in records}
        assert config_path.stat().st_ino in chowned_inos
        assert console_hermes_root.stat().st_ino in chowned_inos
        assert console_home.stat().st_ino not in chowned_inos

    def test_mdm_goose_writes_to_resolved_console_user_plugin_dir(
        self, tmp_path, monkeypatch
    ):
        """Goose hook plugins are user-level, so MDM scope targets the
        console user's ``~/.agents/plugins/runlayer-hooks/hooks/hooks.json``."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_goose_root = console_home / ".agents" / "plugins" / "runlayer-hooks"
        monkeypatch.setattr(
            clients_module,
            "enterprise_goose_dir",
            lambda: console_goose_root,
        )
        _patch_console_home(monkeypatch, console_home)

        install_client(
            Client.GOOSE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        path = console_goose_root / "hooks" / "hooks.json"
        assert path.exists()
        data = json.loads(path.read_text())
        command = data["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        assert command == "/usr/local/bin/aiwatch hook --client goose"
        assert (console_goose_root / "plugin.json").exists()

    def test_mdm_claude_code_preserves_symlinked_settings(
        self, tmp_path, monkeypatch
    ):
        """MDM must not replace a user's symlinked Claude settings file."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        outside = tmp_path / "outside.json"
        outside.write_text('{"secret": "do not clobber"}')
        (console_claude_root / "settings.json").symlink_to(outside)
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        _patch_console_home(monkeypatch, console_home)

        with pytest.raises(OSError, match="unsafe Claude Code settings"):
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        # Never follow the link as root, but do preserve the user's config path.
        assert outside.read_text() == '{"secret": "do not clobber"}'
        settings_path = console_claude_root / "settings.json"
        assert settings_path.is_symlink()
        assert settings_path.resolve() == outside

    def test_windows_mdm_claude_code_does_not_backup_symlink_target(
        self, tmp_path, monkeypatch
    ):
        """SYSTEM must reject a settings symlink before copying its target."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import safe_fs as safe_fs_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        privileged_settings = tmp_path / "system-readable.json"
        original = '{"secret": "SYSTEM-readable"}'
        privileged_settings.write_text(original)
        settings_path = console_claude_root / "settings.json"
        settings_path.symlink_to(privileged_settings)
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        monkeypatch.setattr(safe_fs_module.platform, "system", lambda: "Windows")

        with pytest.raises(OSError, match="unsafe Claude Code settings"):
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="C:/Program Files/Runlayer/aiwatch.exe hook",
            )

        assert settings_path.is_symlink()
        assert privileged_settings.read_text() == original
        assert list(console_claude_root.glob("settings.backup_*.json")) == []

    def test_windows_mdm_claude_code_does_not_follow_settings_parent_link(
        self, tmp_path, monkeypatch
    ):
        """SYSTEM must reject a linked Claude directory before reading through it."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import safe_fs as safe_fs_module

        console_home = tmp_path / "Users" / "alice"
        console_home.mkdir(parents=True)
        outside_dir = tmp_path / "system-readable"
        outside_dir.mkdir()
        outside_settings = outside_dir / "settings.json"
        original = '{"secret": "SYSTEM-readable"}'
        outside_settings.write_text(original)
        console_claude_root = console_home / ".claude"
        console_claude_root.symlink_to(outside_dir, target_is_directory=True)
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        monkeypatch.setattr(safe_fs_module.platform, "system", lambda: "Windows")

        with pytest.raises(OSError, match="unsafe Claude Code settings"):
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="C:/Program Files/Runlayer/aiwatch.exe hook",
            )

        assert console_claude_root.is_symlink()
        assert outside_settings.read_text() == original
        assert list(outside_dir.glob("settings.backup_*.json")) == []

    def test_mdm_claude_code_preserves_symlinked_settings_directory(
        self, tmp_path, monkeypatch
    ):
        """MDM must not replace an engineer's symlinked ``~/.claude`` directory."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_home.mkdir(parents=True)
        outside_dir = tmp_path / "outside_dir"
        outside_dir.mkdir()
        outside_settings = outside_dir / "settings.json"
        outside_settings.write_text('{"permissions": {"allow": ["Bash"]}}')
        (console_home / ".claude").symlink_to(outside_dir, target_is_directory=True)
        console_claude_root = console_home / ".claude"
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        _patch_console_home(monkeypatch, console_home)

        with pytest.raises(OSError, match="unsafe Claude Code settings"):
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        settings_dir = console_home / ".claude"
        assert settings_dir.is_symlink()
        assert settings_dir.resolve() == outside_dir
        assert outside_settings.read_text() == '{"permissions": {"allow": ["Bash"]}}'

    def test_mdm_hermes_write_refuses_symlinked_config(self, tmp_path, monkeypatch):
        """Regression (ENG-3217): symlinked ``~/.hermes/config.yaml`` must not be
        followed by the root MDM write."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_hermes_root = console_home / ".hermes"
        console_hermes_root.mkdir(parents=True)
        outside = tmp_path / "outside.yaml"
        outside.write_text("secret: do not clobber\n")
        (console_hermes_root / "config.yaml").symlink_to(outside)
        monkeypatch.setattr(
            clients_module, "enterprise_hermes_dir", lambda: console_hermes_root
        )
        _patch_console_home(monkeypatch, console_home)

        install_client(
            Client.HERMES,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
            skip_when_missing=False,
        )

        assert outside.read_text() == "secret: do not clobber\n"
        config_path = console_hermes_root / "config.yaml"
        assert not config_path.is_symlink()
        config = yaml.safe_load(config_path.read_text())
        assert "pre_tool_call" in config["hooks"]

    def test_mdm_codex_writes_managed_config_toml(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install import clients as clients_module

        enterprise_root = tmp_path / "enterprise" / "codex"
        monkeypatch.setattr(
            clients_module,
            "enterprise_codex_dir",
            lambda: enterprise_root,
        )

        install_client(
            Client.CODEX,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        # MDM scope writes the features flag to managed_config.toml.
        data = json.loads((enterprise_root / "hooks.json").read_text())
        command = data["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        assert command == "/usr/local/bin/aiwatch hook --client codex"
        assert not (enterprise_root / "hooks").exists()
        managed_toml = (enterprise_root / "managed_config.toml").read_text()
        assert "[features]" in managed_toml
        assert "hooks = true" in managed_toml
        # The user-scope config.toml is not touched.
        assert not (enterprise_root / "config.toml").exists()

    def test_mdm_hermes_writes_to_resolved_console_user_dir(
        self, tmp_path, monkeypatch
    ):
        """Hermes has no native enterprise dir — MDM scope targets the
        console user's ``~/.hermes/config.yaml``."""
        from runlayer_cli.hook_install import clients as clients_module

        console_hermes_root = tmp_path / "Users" / "alice" / ".hermes"
        monkeypatch.setattr(
            clients_module,
            "enterprise_hermes_dir",
            lambda: console_hermes_root,
        )
        _patch_console_home(monkeypatch, tmp_path / "Users" / "alice")

        install_client(
            Client.HERMES,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
            skip_when_missing=False,
        )

        config = yaml.safe_load((console_hermes_root / "config.yaml").read_text())
        assert "pre_tool_call" in config["hooks"]
        assert (
            config["hooks"]["pre_tool_call"][0]["command"]
            == "/usr/local/bin/aiwatch hook --client hermes"
        )
        assert not (console_hermes_root / "agent-hooks").exists()
