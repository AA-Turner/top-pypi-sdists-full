"""Unit tests for ``runlayer_cli.hook_install.safe_fs`` (TOCTOU-safe fs ops).

These primitives back the ENG-3217 fix: root-run MDM writes into the console
user's home must never follow a symlink the (non-admin) user planted there.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from runlayer_cli.hook_install import safe_fs


class TestSafeWriteText:
    def test_creates_missing_parent_dirs(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        target = home / ".claude" / "hooks" / "settings.json"

        safe_fs.safe_write_text(home, target, "hello")

        assert target.read_text() == "hello"

    def test_truncates_existing_regular_file(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        target = home / ".claude" / "settings.json"
        target.write_text("old-and-longer-content")

        safe_fs.safe_write_text(home, target, "new")

        assert target.read_text() == "new"

    def test_replaces_symlink_without_following(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        outside = tmp_path / "outside.txt"
        outside.write_text("DO NOT CLOBBER")
        target = home / ".claude" / "settings.json"
        target.symlink_to(outside)

        safe_fs.safe_write_text(home, target, "safe")

        assert outside.read_text() == "DO NOT CLOBBER"
        assert not target.is_symlink()
        assert target.read_text() == "safe"

    def test_refuses_symlinked_parent(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        outside_dir = tmp_path / "outside_dir"
        outside_dir.mkdir()
        (home / ".claude").symlink_to(outside_dir, target_is_directory=True)
        target = home / ".claude" / "settings.json"

        # Symlinked intermediate component: the link is replaced by a real dir
        # (self-heal) rather than followed, so nothing lands in outside_dir.
        safe_fs.safe_write_text(home, target, "safe")

        assert not (outside_dir / "settings.json").exists()
        assert target.read_text() == "safe"
        assert not (home / ".claude").is_symlink()

    def test_rejects_path_outside_home(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        outside = tmp_path / "elsewhere.txt"

        with pytest.raises(ValueError):
            safe_fs.safe_write_text(home, outside, "x")

    def test_applies_mode(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        target = home / ".claude" / "hook.sh"

        safe_fs.safe_write_text(home, target, "#!/bin/sh\n", mode=0o755)

        assert target.stat().st_mode & 0o777 == 0o755


class TestSafeReadText:
    def test_reads_regular_file(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        target = home / ".claude" / "settings.json"
        target.write_text("data")

        assert safe_fs.safe_read_text(home, target) == "data"

    def test_missing_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()

        assert safe_fs.safe_read_text(home, home / ".claude" / "x.json") is None

    def test_symlink_returns_none_without_following(self, tmp_path: Path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        outside = tmp_path / "secret.txt"
        outside.write_text("root-only-secret")
        link = home / ".claude" / "settings.json"
        link.symlink_to(outside)

        # Must NOT leak the symlink target's contents back to the caller.
        assert safe_fs.safe_read_text(home, link) is None

    def test_path_outside_home_returns_none(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()

        assert safe_fs.safe_read_text(home, tmp_path / "x.txt") is None


class TestWalkParentsFdLeak:
    """``_walk_parents`` must not leak fds when an iteration raises mid-walk."""

    def test_closes_opened_fds_when_component_raises(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        # 3 intermediate dirs, so _walk_parents opens fds for "a" and "b"
        # before failing on "c".
        (home / "a" / "b" / "c").mkdir(parents=True)
        home_fd = safe_fs._open_home_dir(home)

        opened: list[int] = []
        closed: list[int] = []
        real_open = safe_fs._open_dir_component
        real_close = os.close

        def tracking_open(parent_fd: int, name: str, *, create: bool) -> int:
            if name == "c":
                raise OSError("boom mid-walk")
            fd = real_open(parent_fd, name, create=create)
            opened.append(fd)
            return fd

        def tracking_close(fd: int) -> None:
            closed.append(fd)
            real_close(fd)

        monkeypatch.setattr(safe_fs, "_open_dir_component", tracking_open)
        monkeypatch.setattr(os, "close", tracking_close)

        try:
            with pytest.raises(OSError):
                safe_fs._walk_parents(
                    home_fd, ("a", "b", "c", "settings.json"), create=False
                )
            assert opened, "expected fds to be opened before the raise"
            assert set(opened) <= set(closed), "fds opened mid-walk were leaked"
        finally:
            monkeypatch.undo()
            os.close(home_fd)


class TestSafeChownWithinHome:
    def _spy(self, monkeypatch) -> list[int]:
        inodes: list[int] = []
        real = os.fchown

        def spy(fd: int, uid: int, gid: int) -> None:
            try:
                inodes.append(os.fstat(fd).st_ino)
            except OSError:
                pass
            return real(fd, uid, gid)

        monkeypatch.setattr(os, "fchown", spy)
        return inodes

    def test_chowns_file_and_ancestors_not_home(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        claude = home / ".claude"
        claude.mkdir(parents=True)
        target = claude / "settings.json"
        target.write_text("{}")
        inodes = self._spy(monkeypatch)
        my_uid, my_gid = os.getuid(), os.getgid()

        safe_fs.safe_chown_within_home(home, target, my_uid, my_gid)

        assert target.stat().st_ino in inodes
        assert claude.stat().st_ino in inodes
        assert home.stat().st_ino not in inodes

    def test_refuses_symlinked_target(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        claude = home / ".claude"
        claude.mkdir(parents=True)
        outside = tmp_path / "secret"
        outside.write_text("x")
        outside_ino = outside.stat().st_ino
        link = claude / "settings.json"
        link.symlink_to(outside)
        inodes = self._spy(monkeypatch)

        with pytest.raises(OSError):
            safe_fs.safe_chown_within_home(home, link, os.getuid(), os.getgid())

        assert outside_ino not in inodes
