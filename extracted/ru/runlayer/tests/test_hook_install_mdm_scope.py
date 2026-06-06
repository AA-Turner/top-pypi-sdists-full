"""MDM-scope writer tests for ``runlayer_cli.hook_install`` (enterprise/console-home writes + ENG-3217 link safety)."""

from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from runlayer_cli.hook_install import (
    Client,
    InstallScope,
    install_client,
)
from runlayer_cli.hook_install import console_user as console_user_module
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
        )

        config_path = console_hermes_root / "config.yaml"
        assert config_path.exists()
        chowned_inos = {ino for ino, _, _ in records}
        assert config_path.stat().st_ino in chowned_inos
        assert console_hermes_root.stat().st_ino in chowned_inos
        assert console_home.stat().st_ino not in chowned_inos

    def test_mdm_claude_code_write_refuses_symlinked_settings(
        self, tmp_path, monkeypatch
    ):
        """Regression (ENG-3217): a pre-staged ``settings.json`` symlink must not
        let the root MDM write clobber a file outside the home. The link is
        replaced by a real file; the outside target is untouched."""
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

        install_client(
            Client.CLAUDE_CODE,
            scope=InstallScope.MDM,
            hook_command="/usr/local/bin/aiwatch hook",
        )

        # The outside target is left exactly as it was — never written through.
        assert outside.read_text() == '{"secret": "do not clobber"}'
        settings_path = console_claude_root / "settings.json"
        assert not settings_path.is_symlink()
        data = json.loads(settings_path.read_text())
        assert "PreToolUse" in data["hooks"]

    def test_mdm_claude_code_write_refuses_symlinked_dir(self, tmp_path, monkeypatch):
        """Regression (ENG-3217): an intermediate ``~/.claude`` symlink (e.g. to
        ``/``) must not let the root MDM write create files outside the home."""
        from runlayer_cli.hook_install import clients as clients_module

        console_home = tmp_path / "Users" / "alice"
        console_home.mkdir(parents=True)
        outside_dir = tmp_path / "outside_dir"
        outside_dir.mkdir()
        (console_home / ".claude").symlink_to(outside_dir, target_is_directory=True)
        console_claude_root = console_home / ".claude"
        monkeypatch.setattr(
            clients_module, "enterprise_claude_code_dir", lambda: console_claude_root
        )
        _patch_console_home(monkeypatch, console_home)

        try:
            install_client(
                Client.CLAUDE_CODE,
                scope=InstallScope.MDM,
                hook_command="/usr/local/bin/aiwatch hook",
            )
        except OSError:
            # Refusing the write (rather than self-healing the dir) is acceptable.
            pass

        # Nothing was written into the symlink target outside the home.
        assert not (outside_dir / "settings.json").exists()

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
        )

        config = yaml.safe_load((console_hermes_root / "config.yaml").read_text())
        assert "pre_tool_call" in config["hooks"]
        assert (
            config["hooks"]["pre_tool_call"][0]["command"]
            == "/usr/local/bin/aiwatch hook --client hermes"
        )
        assert not (console_hermes_root / "agent-hooks").exists()
