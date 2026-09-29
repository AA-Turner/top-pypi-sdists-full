"""MDM-scope writer tests for ``runlayer_cli.hook_install`` (enterprise/console-home writes + ENG-3217 link safety)."""

from __future__ import annotations

import errno
import json
import os
from pathlib import Path

import pytest
import yaml

from runlayer_cli.hook_install import (
    Client,
    InstallScope,
    install_client,
    uninstall_client,
)
from runlayer_cli.hook_install import console_user as console_user_module
from runlayer_cli.hook_install.clients import (
    _CLINE_CLI_SCRIPT_MARKER,
    _vscode_user_settings_path,
)
from runlayer_cli.hook_install.safe_fs import console_home_anchor


def _patch_console_home(monkeypatch, home: Path | None) -> None:
    """Pin ``find_console_user_home`` so the anchor resolves deterministically.

    ``console_home_anchor`` lazily imports it from ``console_user``, so patching
    the module attribute is picked up at call time.
    """
    monkeypatch.setattr(console_user_module, "find_console_user_home", lambda: home)


def _lstat_uid_override(monkeypatch, path: Path, uid: int) -> None:
    """Make ``os.lstat(path)`` report *uid* as owner (tests run unprivileged)."""
    real_lstat = os.lstat

    def fake(target, *args, **kwargs):
        st = real_lstat(target, *args, **kwargs)
        if isinstance(target, (str, os.PathLike)) and Path(target) == path:
            values = list(st)
            values[4] = uid
            return os.stat_result(values)
        return st

    monkeypatch.setattr(os, "lstat", fake)


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


def _stat_created_as_root(monkeypatch, home: Path) -> None:
    """Report ``st_uid=0`` from ``os.lstat``/``os.fstat`` for anything created
    under *home* after this call.

    Tests run unprivileged, so this fakes the root-run picture: every inode
    that did not exist yet was created by root, until an ``fchown`` hands it
    over. ``st_ino``/``st_mode`` survive so ``_spy_fchown`` and the ownership
    gate keep working. Call before ``_spy_fchown`` so the spy wraps this.
    """
    owned = {home.lstat().st_ino} | {p.lstat().st_ino for p in home.rglob("*")}

    def as_root(st: os.stat_result) -> os.stat_result:
        if st.st_ino in owned:
            return st
        values = list(st)
        values[4] = 0
        return os.stat_result(values)

    real_lstat = os.lstat
    real_fstat = os.fstat
    real_fchown = os.fchown

    def handed_over(fd: int, uid: int, gid: int) -> None:
        owned.add(real_fstat(fd).st_ino)
        real_fchown(fd, uid, gid)

    monkeypatch.setattr(
        os, "lstat", lambda p, *a, **kw: as_root(real_lstat(p, *a, **kw))
    )
    monkeypatch.setattr(os, "fstat", lambda fd: as_root(real_fstat(fd)))
    monkeypatch.setattr(os, "fchown", handed_over)


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

    def test_mdm_claude_code_preserves_empty_settings(self, tmp_path, monkeypatch):
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
        assert updated["enabledPlugins"] == {"linear@claude-plugins-official": True}
        assert updated["model"] == "claude-opus-4-1"

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )
        assert list(console_claude_root.glob("settings.backup_*.json")) == backups

    @staticmethod
    def _seed_claude_backups(console_claude_root: Path) -> list[Path]:
        """Seven stale copies mixing legacy second-only and microsecond names."""
        stamps = [
            "20250101_000000",
            "20250102_000000_000000",
            "20250103_000000",
            "20250104_000000_000000",
            "20250105_000000",
            "20250106_000000_000000",
            "20250107_000000",
        ]
        seeded = []
        for stamp in stamps:
            stale = console_claude_root / f"settings.backup_{stamp}.json"
            stale.write_text("stale")
            seeded.append(stale)
        return seeded

    def _mdm_claude_fixture(self, tmp_path, monkeypatch) -> tuple[Path, Path]:
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_claude_root = console_home / ".claude"
        console_claude_root.mkdir(parents=True)
        settings_path = console_claude_root / "settings.json"
        settings_path.write_text('{"permissions": {"allow": ["Bash"]}}\n')
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        _patch_console_home(monkeypatch, console_home)
        return console_claude_root, settings_path

    def test_mdm_claude_code_changed_reconcile_prunes_stale_backups(
        self, tmp_path, monkeypatch
    ):
        """A changed reconcile keeps its fresh copy plus the newest stale ones."""
        from runlayer_cli.hook_install.config_backup import BACKUP_KEEP

        console_claude_root, settings_path = self._mdm_claude_fixture(
            tmp_path, monkeypatch
        )
        original = settings_path.read_text()
        seeded = self._seed_claude_backups(console_claude_root)
        bystander = console_claude_root / "settings.local.json"
        bystander.write_text("{}")

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        remaining = sorted(console_claude_root.glob("settings.backup_*.json"))
        assert len(remaining) == BACKUP_KEEP
        assert remaining[:-1] == seeded[-(BACKUP_KEEP - 1) :]
        assert remaining[-1].read_text() == original
        assert bystander.exists()
        assert "hooks" in json.loads(settings_path.read_text())

    def test_mdm_claude_code_unchanged_reconcile_creates_no_backup_but_prunes(
        self, tmp_path, monkeypatch
    ):
        """The hourly no-op reconcile still drains a pile left by older builds."""
        from runlayer_cli.hook_install.config_backup import BACKUP_KEEP

        console_claude_root, settings_path = self._mdm_claude_fixture(
            tmp_path, monkeypatch
        )
        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )
        [fresh] = list(console_claude_root.glob("settings.backup_*.json"))
        seeded = self._seed_claude_backups(console_claude_root)
        rendered = settings_path.read_text()

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        remaining = sorted(console_claude_root.glob("settings.backup_*.json"))
        assert remaining == seeded[-(BACKUP_KEEP - 1) :] + [fresh]
        assert settings_path.read_text() == rendered

    def test_mdm_claude_code_failed_write_leaves_every_backup(
        self, tmp_path, monkeypatch
    ):
        """Retention runs only after the active write lands."""
        from runlayer_cli.hook_install import clients as clients_module

        console_claude_root, settings_path = self._mdm_claude_fixture(
            tmp_path, monkeypatch
        )
        seeded = self._seed_claude_backups(console_claude_root)
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

        remaining = sorted(console_claude_root.glob("settings.backup_*.json"))
        assert len(remaining) == len(seeded) + 1
        assert remaining[:-1] == seeded

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

    def test_mdm_claude_code_reowns_backup_before_rewrite(self, tmp_path, monkeypatch):
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
        monkeypatch.setattr(console_user_module.os, "geteuid", lambda: 0, raising=False)
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

    def test_mdm_claude_code_preserves_symlinked_settings(self, tmp_path, monkeypatch):
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
        """Regression (ENG-3217): a ``~/.hermes/config.yaml`` link escaping the
        home is neither followed nor replaced by the root MDM write (ENG-6814:
        replacing it wiped the user's real config)."""
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

        with pytest.raises(OSError) as excinfo:
            install_client(
                Client.HERMES,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
                skip_when_missing=False,
            )

        assert excinfo.value.errno == errno.ELOOP
        assert outside.read_text() == "secret: do not clobber\n"
        config_path = console_hermes_root / "config.yaml"
        assert config_path.is_symlink()
        assert config_path.resolve() == outside
        assert list(console_hermes_root.glob("config.backup_*.yaml")) == []


class TestMDMInHomeSymlinks:
    """MDM writers follow links whose resolved chain stays inside the console home.

    Regression (ENG-6814): a dotfiles setup symlinks e.g. VS Code's
    ``settings.json`` to ``~/dotfiles/...``. The root reconcile treated every
    link as hostile, read nothing, and replaced the link with a fresh file
    holding only Runlayer's keys — every 15 minutes. Links that stay in-home
    are the user's own layout and must merge; links escaping the home are
    still refused.
    """

    def _vscode_setup(self, tmp_path, monkeypatch) -> tuple[Path, Path]:
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_vscode_root = console_home / ".copilot" / "hooks"
        monkeypatch.setattr(
            clients_module, "enterprise_vscode_dir", lambda: console_vscode_root
        )
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        _patch_console_home(monkeypatch, console_home)
        settings_path = _vscode_user_settings_path(console_home)
        settings_path.parent.mkdir(parents=True)
        return console_home, settings_path

    def test_mdm_vscode_merges_into_symlinked_user_settings(
        self, tmp_path, monkeypatch
    ):
        console_home, settings_path = self._vscode_setup(tmp_path, monkeypatch)
        target = console_home / "dotfiles" / "vscode" / "settings.json"
        target.parent.mkdir(parents=True)
        target.write_text('{"editor.fontSize": 14}\n')
        settings_path.symlink_to(target)

        install_client(
            Client.VSCODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        assert settings_path.is_symlink()
        assert settings_path.resolve() == target
        merged = json.loads(target.read_text())
        assert merged["editor.fontSize"] == 14
        assert merged["chat.hookFilesLocations"]["~/.claude/settings.json"] is False
        # The recovery copy lands beside the link, not inside the dotfiles repo.
        assert len(list(settings_path.parent.glob("settings.backup_*.json"))) == 1
        assert list(target.parent.glob("settings.backup_*.json")) == []

    def test_mdm_vscode_creates_dangling_in_home_link_target(
        self, tmp_path, monkeypatch
    ):
        console_home, settings_path = self._vscode_setup(tmp_path, monkeypatch)
        target = console_home / "dotfiles" / "vscode" / "settings.json"
        settings_path.symlink_to(target)

        install_client(
            Client.VSCODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        assert settings_path.is_symlink()
        assert "chat.hookFilesLocations" in json.loads(target.read_text())

    def test_mdm_vscode_reowns_parents_created_for_dangling_link_target(
        self, tmp_path, monkeypatch
    ):
        """Dirs root had to create for the dangling target are handed back to
        the user, otherwise VS Code can't rewrite its own settings file."""
        console_home, settings_path = self._vscode_setup(tmp_path, monkeypatch)
        target = console_home / "dotfiles" / "vscode" / "settings.json"
        settings_path.symlink_to(target)
        monkeypatch.setattr(console_user_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(console_user_module.os, "geteuid", lambda: 0, raising=False)
        _stat_created_as_root(monkeypatch, console_home)
        records = _spy_fchown(monkeypatch)

        install_client(
            Client.VSCODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        chowned_inos = {ino for ino, _, _ in records}
        assert (console_home / "dotfiles").stat().st_ino in chowned_inos
        assert (console_home / "dotfiles" / "vscode").stat().st_ino in chowned_inos
        assert target.stat().st_ino in chowned_inos
        assert console_home.stat().st_ino not in chowned_inos

    def test_mdm_vscode_refuses_escaping_user_settings_link(
        self, tmp_path, monkeypatch
    ):
        console_home, settings_path = self._vscode_setup(tmp_path, monkeypatch)
        outside = tmp_path / "outside-settings.json"
        outside.write_text('{"editor.fontSize": 14}\n')
        settings_path.symlink_to(outside)

        with pytest.raises(OSError) as excinfo:
            install_client(
                Client.VSCODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        assert excinfo.value.errno == errno.ELOOP
        assert settings_path.is_symlink()
        assert outside.read_text() == '{"editor.fontSize": 14}\n'
        assert list(settings_path.parent.glob("settings.backup_*.json")) == []

    def _claude_setup(self, tmp_path, monkeypatch) -> Path:
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_home.mkdir(parents=True)
        monkeypatch.setattr(
            clients_module,
            "enterprise_claude_code_dir",
            lambda: console_home / ".claude",
        )
        _patch_console_home(monkeypatch, console_home)
        return console_home

    def test_mdm_claude_code_merges_into_symlinked_settings(
        self, tmp_path, monkeypatch
    ):
        console_home = self._claude_setup(tmp_path, monkeypatch)
        (console_home / ".claude").mkdir()
        target = console_home / "dotfiles" / "claude" / "settings.json"
        target.parent.mkdir(parents=True)
        target.write_text('{"permissions": {"allow": ["Bash"]}}\n')
        settings_path = console_home / ".claude" / "settings.json"
        settings_path.symlink_to(target)

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        assert settings_path.is_symlink()
        merged = json.loads(target.read_text())
        assert merged["permissions"] == {"allow": ["Bash"]}
        assert "PreToolUse" in merged["hooks"]

    def test_mdm_claude_code_merges_through_symlinked_directory(
        self, tmp_path, monkeypatch
    ):
        """``~/.claude -> ~/dotfiles/claude`` is a common dotfiles layout."""
        console_home = self._claude_setup(tmp_path, monkeypatch)
        target_dir = console_home / "dotfiles" / "claude"
        target_dir.mkdir(parents=True)
        (target_dir / "settings.json").write_text(
            '{"permissions": {"allow": ["Bash"]}}\n'
        )
        (console_home / ".claude").symlink_to(target_dir, target_is_directory=True)

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        assert (console_home / ".claude").is_symlink()
        merged = json.loads((target_dir / "settings.json").read_text())
        assert merged["permissions"] == {"allow": ["Bash"]}
        assert "PreToolUse" in merged["hooks"]
        # The linked dir is usually a git working tree; the recovery copy (which
        # may carry a blanked API key) must never land in it.
        assert list(target_dir.glob("settings.backup_*.json")) == []
        relocated = console_home / ".runlayer" / "config-backups" / ".claude"
        assert len(list(relocated.glob("settings.backup_*.json"))) == 1

    def test_mdm_claude_code_prunes_relocated_backups_behind_directory_link(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli.hook_install.config_backup import BACKUP_KEEP

        console_home = self._claude_setup(tmp_path, monkeypatch)
        target_dir = console_home / "dotfiles" / "claude"
        target_dir.mkdir(parents=True)
        (console_home / ".claude").symlink_to(target_dir, target_is_directory=True)
        relocated = console_home / ".runlayer" / "config-backups" / ".claude"
        for round_index in range(BACKUP_KEEP + 3):
            (target_dir / "settings.json").write_text(
                json.dumps({"permissions": {"allow": [f"Bash{round_index}"]}})
            )
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        assert len(list(relocated.glob("settings.backup_*.json"))) == BACKUP_KEEP
        assert list(target_dir.glob("settings.backup_*.json")) == []

    def test_mdm_claude_code_relocated_backup_keeps_owner_only_mode(
        self, tmp_path, monkeypatch
    ):
        console_home = self._claude_setup(tmp_path, monkeypatch)
        target_dir = console_home / "dotfiles" / "claude"
        target_dir.mkdir(parents=True)
        settings = target_dir / "settings.json"
        settings.write_text('{"permissions": {"allow": ["Bash"]}}\n')
        settings.chmod(0o600)
        (console_home / ".claude").symlink_to(target_dir, target_is_directory=True)

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        relocated = console_home / ".runlayer" / "config-backups" / ".claude"
        [backup_path] = list(relocated.glob("settings.backup_*.json"))
        assert backup_path.stat().st_mode & 0o777 == 0o600
        assert settings.stat().st_mode & 0o777 == 0o600

    def test_mdm_claude_code_refuses_backup_relocation_into_linked_runlayer(
        self, tmp_path, monkeypatch
    ):
        """Relocation exists to keep the copy out of a dotfiles tree; a linked
        ``~/.runlayer`` is such a tree, so the write refuses instead."""
        console_home = self._claude_setup(tmp_path, monkeypatch)
        target_dir = console_home / "dotfiles" / "claude"
        target_dir.mkdir(parents=True)
        original = '{"permissions": {"allow": ["Bash"]}}\n'
        (target_dir / "settings.json").write_text(original)
        (console_home / ".claude").symlink_to(target_dir, target_is_directory=True)
        runlayer_dir = console_home / "dotfiles" / "runlayer"
        runlayer_dir.mkdir()
        (console_home / ".runlayer").symlink_to(runlayer_dir, target_is_directory=True)

        with pytest.raises(OSError) as excinfo:
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        assert excinfo.value.errno == errno.ELOOP
        assert list(runlayer_dir.rglob("*")) == []
        assert (target_dir / "settings.json").read_text() == original
        assert (console_home / ".claude").is_symlink()
        assert (console_home / ".runlayer").is_symlink()

    def test_mdm_goose_writes_through_linked_agents_dir(self, tmp_path, monkeypatch):
        """``~/.agents -> ~/dotfiles/agents``: both the hooks file and the
        Runlayer-owned manifest land in the real dir; the link survives."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        real_agents = console_home / "dotfiles" / "agents"
        real_agents.mkdir(parents=True)
        (console_home / ".agents").symlink_to(real_agents, target_is_directory=True)
        console_goose_root = console_home / ".agents" / "plugins" / "runlayer-hooks"
        monkeypatch.setattr(
            clients_module, "enterprise_goose_dir", lambda: console_goose_root
        )
        _patch_console_home(monkeypatch, console_home)
        monkeypatch.setattr(console_user_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(console_user_module.os, "geteuid", lambda: 0, raising=False)
        _stat_created_as_root(monkeypatch, console_home)
        records = _spy_fchown(monkeypatch)

        install_client(
            Client.GOOSE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        assert (console_home / ".agents").is_symlink()
        real_root = real_agents / "plugins" / "runlayer-hooks"
        hooks = json.loads((real_root / "hooks" / "hooks.json").read_text())
        assert "PreToolUse" in hooks["hooks"]
        assert (real_root / "plugin.json").exists()
        chowned_inos = {ino for ino, _, _ in records}
        for created in (
            real_agents / "plugins",
            real_root,
            real_root / "hooks",
            real_root / "hooks" / "hooks.json",
            real_root / "plugin.json",
        ):
            assert created.stat().st_ino in chowned_inos, created
        assert console_home.stat().st_ino not in chowned_inos

    def test_mdm_claude_code_leaves_user_owned_link_target_alone(
        self, tmp_path, monkeypatch
    ):
        """A pre-existing target reached through the user's link is rewritten
        in place (owner preserved), so root has nothing to hand back and never
        chowns through the link."""
        console_home = self._claude_setup(tmp_path, monkeypatch)
        (console_home / ".claude").mkdir()
        target = console_home / "dotfiles" / "claude" / "settings.json"
        target.parent.mkdir(parents=True)
        target.write_text("{}\n")
        (console_home / ".claude" / "settings.json").symlink_to(target)
        monkeypatch.setattr(console_user_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(console_user_module.os, "geteuid", lambda: 0, raising=False)
        records = _spy_fchown(monkeypatch)

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        assert "hooks" in json.loads(target.read_text())
        chowned_inos = {ino for ino, _, _ in records}
        assert target.stat().st_ino not in chowned_inos
        assert (console_home / "dotfiles").stat().st_ino not in chowned_inos
        assert (console_home / "dotfiles" / "claude").stat().st_ino not in chowned_inos
        assert console_home.stat().st_ino not in chowned_inos

    def test_mdm_vscode_refuses_link_to_target_owned_by_another_uid(
        self, tmp_path, monkeypatch
    ):
        """An in-home link to a file the user does not own is not followed:
        root must never let the console user pick a root-owned file to write
        and hand back to them."""
        console_home, settings_path = self._vscode_setup(tmp_path, monkeypatch)
        target = console_home / "Library" / "Managed" / "settings.json"
        target.parent.mkdir(parents=True)
        target.write_text('{"editor.fontSize": 14}\n')
        settings_path.symlink_to(target)
        _lstat_uid_override(monkeypatch, target, console_home.stat().st_uid + 1)

        with pytest.raises(OSError) as excinfo:
            install_client(
                Client.VSCODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )

        assert excinfo.value.errno == errno.ELOOP
        assert settings_path.is_symlink()
        assert target.read_text() == '{"editor.fontSize": 14}\n'
        assert list(settings_path.parent.glob("settings.backup_*.json")) == []

    def test_mdm_cline_does_not_follow_in_home_link_on_runlayer_script(
        self, tmp_path, monkeypatch
    ):
        """Runlayer-owned files keep refuse-or-replace: no link following."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        hooks_dir = console_home / ".cline" / "hooks"
        hooks_dir.mkdir(parents=True)
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(
            clients_module, "enterprise_cline_cli_dir", lambda: hooks_dir
        )
        _patch_console_home(monkeypatch, console_home)
        target = console_home / "dotfiles" / "cline" / "PreToolUse"
        target.parent.mkdir(parents=True)
        original = f"#!/bin/sh\n{_CLINE_CLI_SCRIPT_MARKER}\necho stale\n"
        target.write_text(original)
        (hooks_dir / "PreToolUse").symlink_to(target)

        install_client(
            Client.CLINE_CLI,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
            skip_when_missing=False,
        )

        assert (hooks_dir / "PreToolUse").is_symlink()
        assert target.read_text() == original
        assert (hooks_dir / "PreToolUse.sh").is_file()

    def test_mdm_claude_code_uninstall_edits_through_in_home_link(
        self, tmp_path, monkeypatch
    ):
        console_home = self._claude_setup(tmp_path, monkeypatch)
        (console_home / ".claude").mkdir()
        target = console_home / "dotfiles" / "claude" / "settings.json"
        target.parent.mkdir(parents=True)
        target.write_text('{"permissions": {"allow": ["Bash"]}}\n')
        settings_path = console_home / ".claude" / "settings.json"
        settings_path.symlink_to(target)
        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )
        assert "hooks" in json.loads(target.read_text())

        result = uninstall_client(Client.CLAUDE_CODE, scope=InstallScope.MDM)

        assert result.changed
        assert settings_path.is_symlink()
        after = json.loads(target.read_text())
        assert after["permissions"] == {"allow": ["Bash"]}
        assert "hooks" not in after

    def test_mdm_claude_code_uninstall_refuses_escaping_link(
        self, tmp_path, monkeypatch
    ):
        console_home = self._claude_setup(tmp_path, monkeypatch)
        (console_home / ".claude").mkdir()
        outside = tmp_path / "outside-settings.json"
        outside.write_text('{"hooks": {"PreToolUse": []}}\n')
        settings_path = console_home / ".claude" / "settings.json"
        settings_path.symlink_to(outside)

        result = uninstall_client(Client.CLAUDE_CODE, scope=InstallScope.MDM)

        assert not result.changed
        assert settings_path.is_symlink()
        assert outside.read_text() == '{"hooks": {"PreToolUse": []}}\n'

    def test_mdm_hermes_uninstall_edits_through_in_home_link(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        hermes_dir = console_home / ".hermes"
        hermes_dir.mkdir(parents=True)
        monkeypatch.setattr(clients_module, "enterprise_hermes_dir", lambda: hermes_dir)
        _patch_console_home(monkeypatch, console_home)
        target = console_home / "dotfiles" / "hermes" / "config.yaml"
        target.parent.mkdir(parents=True)
        target.write_text("model: gpt\n")
        (hermes_dir / "config.yaml").symlink_to(target)
        install_client(
            Client.HERMES,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
            skip_when_missing=False,
        )
        assert "hooks" in yaml.safe_load(target.read_text())

        result = uninstall_client(Client.HERMES, scope=InstallScope.MDM)

        assert result.changed
        assert (hermes_dir / "config.yaml").is_symlink()
        assert yaml.safe_load(target.read_text()) == {"model": "gpt"}

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

    def test_windows_mdm_codex_targets_programdata_system_layer(self, monkeypatch):
        """Codex reads ``%ProgramData%\\OpenAI\\Codex`` as its managed System
        layer on Windows. Under the SYSTEM ``AIWatchHooks`` task ``Path.home()``
        is the systemprofile, which no console user ever reads (ENG-6617)."""
        from runlayer_cli.hook_install import paths as paths_module
        from runlayer_cli.hook_install.clients import (
            _codex_features_toml_file,
            config_path_for,
        )

        monkeypatch.setattr(paths_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            Path,
            "home",
            classmethod(lambda cls: Path("C:/Windows/system32/config/systemprofile")),
        )

        hooks_path = config_path_for(Client.CODEX, InstallScope.MDM)
        toml_path = _codex_features_toml_file(InstallScope.MDM)

        assert hooks_path == Path("C:/ProgramData/OpenAI/Codex/hooks.json")
        # Only ``config.toml`` carries a hooks folder on the System layer;
        # Windows ``managed_config.toml`` lives in ``~/.codex`` and is not read
        # from ProgramData.
        assert toml_path == Path("C:/ProgramData/OpenAI/Codex/config.toml")
        assert "systemprofile" not in str(hooks_path)
        assert "systemprofile" not in str(toml_path)

    def test_windows_mdm_codex_writes_config_toml_not_managed_config(
        self, tmp_path, monkeypatch
    ):
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import paths as paths_module

        enterprise_root = tmp_path / "ProgramData" / "OpenAI" / "Codex"
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(paths_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module,
            "enterprise_codex_dir",
            lambda: enterprise_root,
        )
        _patch_console_home(monkeypatch, None)

        install_client(
            Client.CODEX,
            scope=InstallScope.MDM,
            hook_command="C:/Program Files/Runlayer/aiwatch.exe hook",
        )

        data = json.loads((enterprise_root / "hooks.json").read_text())
        assert data["hooks"]["PreToolUse"][0]["hooks"][0]["command"].endswith(
            "hook --client codex"
        )
        config_toml = (enterprise_root / "config.toml").read_text()
        assert "[features]" in config_toml
        assert "hooks = true" in config_toml
        assert not (enterprise_root / "managed_config.toml").exists()

    def test_windows_mdm_codex_removes_legacy_console_user_hooks(
        self, tmp_path, monkeypatch
    ):
        """The System-layer install supersedes a user-layer ``hooks.json`` that
        Codex would otherwise hold for ``/hooks`` trust review; strip Runlayer
        entries there and keep third-party ones."""
        from runlayer_cli.hook_install import clients as clients_module

        enterprise_root = tmp_path / "ProgramData" / "OpenAI" / "Codex"
        console_home = tmp_path / "Users" / "alice"
        legacy = console_home / ".codex" / "hooks.json"
        legacy.parent.mkdir(parents=True)
        legacy.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": (
                                            '& "C:/Program Files/Runlayer/aiwatch.exe" '
                                            "hook --client codex"
                                        ),
                                    },
                                ],
                            },
                            {
                                "matcher": "",
                                "hooks": [
                                    {"type": "command", "command": "my-linter"},
                                ],
                            },
                        ]
                    }
                }
            )
        )
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module,
            "enterprise_codex_dir",
            lambda: enterprise_root,
        )
        _patch_console_home(monkeypatch, console_home)
        monkeypatch.setattr(
            clients_module, "_reown_to_console_user", lambda _p, **_kw: None
        )

        install_client(
            Client.CODEX,
            scope=InstallScope.MDM,
            hook_command="C:/Program Files/Runlayer/aiwatch.exe hook",
        )

        assert (enterprise_root / "hooks.json").exists()
        remaining = json.loads(legacy.read_text())
        commands = [
            hook["command"]
            for entry in remaining["hooks"]["PreToolUse"]
            for hook in entry["hooks"]
        ]
        assert commands == ["my-linter"]

    def test_windows_mdm_codex_legacy_cleanup_skips_reparse_point(
        self, tmp_path, monkeypatch
    ):
        """A user-planted link under ``~/.codex`` must never be followed by
        SYSTEM, and must not block the ProgramData write."""
        from runlayer_cli.hook_install import clients as clients_module
        from runlayer_cli.hook_install import safe_fs as safe_fs_module

        enterprise_root = tmp_path / "ProgramData" / "OpenAI" / "Codex"
        console_home = tmp_path / "Users" / "alice"
        outside = tmp_path / "outside.json"
        original = json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "aiwatch.exe hook --client codex",
                                }
                            ]
                        }
                    ]
                }
            }
        )
        outside.write_text(original)
        (console_home / ".codex").mkdir(parents=True)
        (console_home / ".codex" / "hooks.json").symlink_to(outside)
        monkeypatch.setattr(clients_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(safe_fs_module.platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            clients_module,
            "enterprise_codex_dir",
            lambda: enterprise_root,
        )
        _patch_console_home(monkeypatch, console_home)

        install_client(
            Client.CODEX,
            scope=InstallScope.MDM,
            hook_command="C:/Program Files/Runlayer/aiwatch.exe hook",
        )

        assert (enterprise_root / "hooks.json").exists()
        assert outside.read_text() == original
        assert (console_home / ".codex" / "hooks.json").is_symlink()

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
