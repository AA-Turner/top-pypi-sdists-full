"""Tests for ``runlayer_cli.hook_install.console_user.has_enrolled_credential_for_host``.

Witness contract: gate fires on the per-host enrollment marker file
(``~/.runlayer/.enrolled-<host_key>``), **not** on YAML ``hosts.<key>``
presence. This avoids the ``runlayer org-api-key add`` false-positive where
the org-key writer creates a ``hosts.<key>`` entry without enrollment ever
having run.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from runlayer_cli.enrollment import enrollment_marker_path
from runlayer_cli.hook_install import console_user
from runlayer_cli.hook_install.console_user import (
    has_enrolled_credential_for_host,
    reown_to_console_user,
)


def _write_marker(home: Path, host: str) -> Path:
    path = enrollment_marker_path(host, home=home)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    return path


class TestHasEnrolledCredentialForHost:
    def test_returns_true_when_marker_present(self, tmp_path: Path):
        _write_marker(tmp_path, "https://t.example.com")

        assert has_enrolled_credential_for_host(tmp_path, "https://t.example.com")

    def test_returns_false_when_marker_absent(self, tmp_path: Path):
        assert not has_enrolled_credential_for_host(tmp_path, "https://t.example.com")

    def test_returns_false_when_runlayer_dir_missing(self, tmp_path: Path):
        # No ~/.runlayer/ directory at all (fresh-imaged device, never enrolled).
        assert not has_enrolled_credential_for_host(tmp_path, "https://t.example.com")

    def test_marker_for_other_host_does_not_satisfy(self, tmp_path: Path):
        _write_marker(tmp_path, "https://other.example.com")

        assert not has_enrolled_credential_for_host(tmp_path, "https://t.example.com")

    def test_yaml_host_entry_without_marker_does_not_satisfy(self, tmp_path: Path):
        """Regression: pre-marker-file YAML witness must not pass the gate.

        Prevents the ``runlayer org-api-key add`` false-positive — that command
        creates a ``hosts.<key>`` entry (see ``Config.set_org_api_key``) but
        does not drop the enrollment marker.
        """
        runlayer_dir = tmp_path / ".runlayer"
        runlayer_dir.mkdir()
        (runlayer_dir / "config.yaml").write_text(
            "default_host: https://t.example.com\n"
            "hosts:\n"
            "  t.example.com:\n"
            "    url: https://t.example.com\n"
            "    org_api_keys:\n"
            "      ai_watch_mdm: rl_org_xyz\n"
        )

        assert not has_enrolled_credential_for_host(tmp_path, "https://t.example.com")

    def test_org_api_key_add_does_not_satisfy_gate(self, tmp_path: Path):
        """End-to-end regression: ``Config.set_org_api_key`` doesn't trip the gate.

        Drives the real writer (not a YAML fixture) to prove the gate stays
        org-key-add-blind no matter how that command evolves.
        """
        from runlayer_cli.config import Config, save_config

        config = Config()
        config.set_org_api_key("https://t.example.com", "ai_watch_mdm", "rl_org_xyz")
        # save_config writes to ~/.runlayer/config.yaml by default; redirect via
        # a Path.home patch isn't worth the ceremony — write directly.
        runlayer_dir = tmp_path / ".runlayer"
        runlayer_dir.mkdir(parents=True, exist_ok=True)
        (runlayer_dir / "config.yaml").write_text(_dump_config(config))

        assert not has_enrolled_credential_for_host(tmp_path, "https://t.example.com")


def _dump_config(config) -> str:
    import yaml

    return yaml.safe_dump(config.to_dict())


def _spy_fchown(monkeypatch) -> list[int]:
    """Record the *effective* inode of every chown and still apply it.

    Spies on both ``os.fchown`` (fd-based, link-safe — the fix) and ``os.chown``
    (path-based, which the old code used and which *follows symlinks*). For
    ``os.chown`` we record the inode it would actually land on (resolving the
    link), so a vulnerable reown that chases ``~/.claude/settings.json ->
    /etc/passwd`` shows the outside target's inode here and trips the assertions.
    """
    inodes: list[int] = []
    real_fchown = os.fchown
    real_chown = os.chown

    def fchown_spy(fd: int, uid: int, gid: int) -> None:
        try:
            inodes.append(os.fstat(fd).st_ino)
        except OSError:
            pass
        return real_fchown(fd, uid, gid)

    def chown_spy(path, uid, gid, *args, **kwargs) -> None:
        follow = kwargs.get("follow_symlinks", True)
        try:
            inodes.append(os.stat(path, follow_symlinks=follow).st_ino)
        except OSError:
            pass
        return real_chown(path, uid, gid, *args, **kwargs)

    monkeypatch.setattr(os, "fchown", fchown_spy)
    monkeypatch.setattr(os, "chown", chown_spy)
    return inodes


def _as_root(monkeypatch, home: Path) -> None:
    monkeypatch.setattr(console_user.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(console_user.os, "geteuid", lambda: 0, raising=False)
    monkeypatch.setattr(console_user, "find_console_user_home", lambda: home)


class TestReownSymlinkSafety:
    """Regression (ENG-3217 / CWE-59,61): ``reown_to_console_user`` must never
    follow a symlink planted in the (user-controlled) home, or root would chown
    an attacker-chosen file (e.g. ``/etc/passwd``) to the user."""

    def test_reowns_real_file_within_home(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        claude = home / ".claude"
        claude.mkdir(parents=True)
        settings = claude / "settings.json"
        settings.write_text("{}")
        _as_root(monkeypatch, home)
        inodes = _spy_fchown(monkeypatch)

        reown_to_console_user(settings)

        # File + the ~/.claude dir are reclaimed; the home itself is not.
        assert settings.stat().st_ino in inodes
        assert claude.stat().st_ino in inodes
        assert home.stat().st_ino not in inodes

    def test_does_not_follow_symlinked_final_component(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        claude = home / ".claude"
        claude.mkdir(parents=True)
        outside = tmp_path / "outside" / "secret"
        outside.parent.mkdir(parents=True)
        outside.write_text("root-owned")
        outside_ino = outside.stat().st_ino
        link = claude / "settings.json"
        link.symlink_to(outside)
        _as_root(monkeypatch, home)
        inodes = _spy_fchown(monkeypatch)

        reown_to_console_user(link)

        # The outside target's inode is never chowned, and the link is intact.
        assert outside_ino not in inodes
        assert link.is_symlink()
        assert outside.read_text() == "root-owned"

    def test_does_not_follow_symlinked_parent_component(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        home.mkdir(parents=True)
        outside_dir = tmp_path / "outside_dir"
        outside_dir.mkdir()
        outside_file = outside_dir / "settings.json"
        outside_file.write_text("root-owned")
        outside_dir_ino = outside_dir.stat().st_ino
        outside_file_ino = outside_file.stat().st_ino
        (home / ".claude").symlink_to(outside_dir, target_is_directory=True)
        _as_root(monkeypatch, home)
        inodes = _spy_fchown(monkeypatch)

        reown_to_console_user(home / ".claude" / "settings.json")

        assert outside_dir_ino not in inodes
        assert outside_file_ino not in inodes

    def test_no_op_when_path_outside_home(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        home.mkdir(parents=True)
        outside = tmp_path / "elsewhere" / "f.json"
        outside.parent.mkdir(parents=True)
        outside.write_text("{}")
        outside_ino = outside.stat().st_ino
        _as_root(monkeypatch, home)
        inodes = _spy_fchown(monkeypatch)

        reown_to_console_user(outside)

        assert outside_ino not in inodes

    def test_no_op_when_not_root(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        claude = home / ".claude"
        claude.mkdir(parents=True)
        settings = claude / "settings.json"
        settings.write_text("{}")
        monkeypatch.setattr(console_user.platform, "system", lambda: "Darwin")
        monkeypatch.setattr(console_user.os, "geteuid", lambda: 501, raising=False)
        monkeypatch.setattr(console_user, "find_console_user_home", lambda: home)
        inodes = _spy_fchown(monkeypatch)

        reown_to_console_user(settings)

        assert inodes == []


class TestEnrollmentMarkerPath:
    def test_path_uses_host_key_not_full_url(self, tmp_path: Path):
        path = enrollment_marker_path("https://tenant.runlayer.com", home=tmp_path)

        assert path == tmp_path / ".runlayer" / ".enrolled-tenant.runlayer.com"

    def test_path_includes_nondefault_port(self, tmp_path: Path):
        path = enrollment_marker_path("https://t.example.com:8443", home=tmp_path)

        assert path == tmp_path / ".runlayer" / ".enrolled-t.example.com:8443"

    def test_path_omits_default_port(self, tmp_path: Path):
        path = enrollment_marker_path("https://t.example.com:443", home=tmp_path)

        assert path == tmp_path / ".runlayer" / ".enrolled-t.example.com"


class TestWtsActiveConsoleUser:
    """Picker logic over WTS session enumeration.

    The point of switching off ``query session`` is locale-independence —
    these cases are what broke the old text parser (localized "Active"
    keyword, services session noise, RDP sessions in disconnected state).
    """

    def test_picks_active_interactive_session(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(
            console_user,
            "_iter_wts_sessions",
            lambda: [(0, 0, "SYSTEM"), (1, 0, "alice")],
        )

        assert console_user._wts_active_console_user() == "alice"

    def test_skips_session_zero_even_when_marked_active(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        # Services session is always id 0 regardless of locale.
        monkeypatch.setattr(
            console_user, "_iter_wts_sessions", lambda: [(0, 0, "alice")]
        )

        assert console_user._wts_active_console_user() is None

    def test_skips_disconnected_sessions(self, monkeypatch: pytest.MonkeyPatch):
        # WTSDisconnected = 4. Old text parser would have picked this up if
        # the localized state string happened to contain "Active".
        monkeypatch.setattr(
            console_user, "_iter_wts_sessions", lambda: [(2, 4, "alice")]
        )

        assert console_user._wts_active_console_user() is None

    def test_skips_service_account_names(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(
            console_user,
            "_iter_wts_sessions",
            lambda: [
                (1, 0, "SYSTEM"),
                (2, 0, "Local Service"),
                (3, 0, "Network Service"),
            ],
        )

        assert console_user._wts_active_console_user() is None

    def test_skips_empty_username(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(
            console_user,
            "_iter_wts_sessions",
            lambda: [(1, 0, ""), (2, 0, "alice")],
        )

        assert console_user._wts_active_console_user() == "alice"

    def test_no_sessions(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(console_user, "_iter_wts_sessions", lambda: [])

        assert console_user._wts_active_console_user() is None


class TestWindowsConsoleUserHome:
    def test_uses_wts_username_when_available(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(console_user, "_wts_active_console_user", lambda: "alice")

        assert console_user._windows_console_user_home() == Path("C:/Users/alice")

    def test_falls_back_to_userprofile_when_wts_returns_none(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(console_user, "_wts_active_console_user", lambda: None)
        monkeypatch.setenv("USERPROFILE", "C:\\Users\\bob")

        assert console_user._windows_console_user_home() == Path("C:\\Users\\bob")

    def test_systemprofile_fallback_rejected(self, monkeypatch: pytest.MonkeyPatch):
        # Under SYSTEM context (LaunchDaemon equivalent), USERPROFILE points
        # at systemprofile — that's not a real console user, so the gate
        # should report "no console user detected" rather than checking the
        # wrong directory for the enrollment marker.
        monkeypatch.setattr(console_user, "_wts_active_console_user", lambda: None)
        monkeypatch.setenv(
            "USERPROFILE", "C:\\Windows\\system32\\config\\systemprofile"
        )

        assert console_user._windows_console_user_home() is None

    def test_returns_none_when_no_signals(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(console_user, "_wts_active_console_user", lambda: None)
        monkeypatch.delenv("USERPROFILE", raising=False)

        assert console_user._windows_console_user_home() is None


def _scutil_console_user_output(name: str, uid: int) -> str:
    """``scutil`` ``show State:/Users/ConsoleUser`` output for an active session.

    Mirrors the real layout: the top-level ``UID`` line comes after the nested
    ``SessionInfo`` block.
    """
    return (
        "<dictionary> {\n"
        "  GID : 20\n"
        f"  Name : {name}\n"
        "  SessionInfo : <array> {\n"
        "    0 : <dictionary> {\n"
        "      kCGSSessionOnConsoleKey : TRUE\n"
        f"      kCGSSessionUserIDKey : {uid}\n"
        "    }\n"
        "  }\n"
        f"  UID : {uid}\n"
        "}\n"
    )


class TestMacosConsoleUserHome:
    """The macOS console-user home comes from the account record, not the login name.

    With IdP-backed accounts (Platform SSO / Jamf Connect) the user can log in
    with an email alias of the account's short name, and ``scutil`` then
    reports that alias as the console user's ``Name``. ``/Users/<alias>`` does
    not exist, so every root-context lifecycle step failed with ``console user
    lookup failed`` and the bootstrap LaunchDaemon relaunched every minute.
    """

    accounts = pytest.importorskip("pwd")

    def _stub_scutil(
        self, monkeypatch: pytest.MonkeyPatch, *, name: str, uid: int
    ) -> None:
        monkeypatch.setattr(console_user.platform, "system", lambda: "Darwin")
        output = _scutil_console_user_output(name, uid)
        monkeypatch.setattr(
            console_user.subprocess,
            "run",
            lambda *args, **kwargs: subprocess.CompletedProcess(
                args=args, returncode=0, stdout=output, stderr=""
            ),
        )

    def _stub_accounts(
        self, monkeypatch: pytest.MonkeyPatch, homes_by_uid: dict[int, str]
    ) -> None:
        def getpwuid(uid: int) -> SimpleNamespace:
            if uid not in homes_by_uid:
                raise KeyError(f"getpwuid(): uid not found: {uid}")
            return SimpleNamespace(pw_dir=homes_by_uid[uid])

        monkeypatch.setattr(self.accounts, "getpwuid", getpwuid)

    def test_email_alias_login_resolves_account_home(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        self._stub_scutil(monkeypatch, name="alice@example.com", uid=501)
        self._stub_accounts(monkeypatch, {501: "/Users/alice"})

        assert console_user.find_console_user_home() == Path("/Users/alice")

    def test_home_outside_users_directory(self, monkeypatch: pytest.MonkeyPatch):
        self._stub_scutil(monkeypatch, name="alice", uid=501)
        self._stub_accounts(monkeypatch, {501: "/Volumes/Data/Users/alice"})

        assert console_user.find_console_user_home() == Path(
            "/Volumes/Data/Users/alice"
        )

    def test_unknown_uid_falls_back_to_users_directory(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        self._stub_scutil(monkeypatch, name="alice", uid=501)
        self._stub_accounts(monkeypatch, {})

        assert console_user.find_console_user_home() == Path("/Users/alice")

    @pytest.mark.parametrize("pw_dir", ["", "Users/alice"])
    def test_non_absolute_account_home_falls_back_to_users_directory(
        self, monkeypatch: pytest.MonkeyPatch, pw_dir: str
    ):
        # A relative home would resolve against root's cwd ("/" for the
        # bootstrap LaunchDaemon) and send root-owned writes there.
        self._stub_scutil(monkeypatch, name="alice", uid=501)
        self._stub_accounts(monkeypatch, {501: pw_dir})

        assert console_user.find_console_user_home() == Path("/Users/alice")

    @pytest.mark.parametrize("name", ["loginwindow", "_mbsetupuser", "root"])
    def test_non_user_sessions_have_no_console_home(
        self, monkeypatch: pytest.MonkeyPatch, name: str
    ):
        self._stub_scutil(monkeypatch, name=name, uid=0)
        self._stub_accounts(monkeypatch, {0: "/var/root"})

        assert console_user.find_console_user_home() is None
