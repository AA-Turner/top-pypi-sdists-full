"""Bounded retention for ``<stem>.backup_<timestamp><suffix>`` recovery copies."""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

import pytest

from runlayer_cli.hook_install import config_backup, safe_fs
from runlayer_cli.hook_install.config_backup import (
    BACKUP_KEEP,
    BACKUP_ROOT,
    backup_dir_for,
    backup_path_for,
    prune_backups,
)

_MICRO_STAMPS = [f"202609{day:02d}_120000_000000" for day in range(1, 8)]


def _seed(directory: Path, name: str, stamps: list[str]) -> list[Path]:
    stem, suffix = os.path.splitext(name)
    paths = []
    for stamp in stamps:
        path = directory / f"{stem}.backup_{stamp}{suffix}"
        path.write_text(stamp)
        paths.append(path)
    return paths


def _names(directory: Path) -> set[str]:
    return {entry.name for entry in directory.iterdir()}


def test_backup_path_for_uses_microsecond_stamp(tmp_path: Path) -> None:
    now = datetime(2026, 9, 22, 20, 15, 30, 123456)
    assert backup_path_for(tmp_path / "settings.json", home=tmp_path, now=now) == (
        tmp_path / "settings.backup_20260922_201530_123456.json"
    )
    assert backup_path_for(tmp_path / "config.toml", home=tmp_path, now=now).name == (
        "config.backup_20260922_201530_123456.toml"
    )


class TestBackupDirFor:
    """Backups sit beside the config unless its directory is reached through a
    link — a linked dir is usually a git tree, and a backup can carry a secret."""

    def test_plain_directory_is_sibling(self, tmp_path: Path) -> None:
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)

        assert backup_dir_for(home / ".claude" / "settings.json", home=home) == (
            home / ".claude"
        )

    def test_file_link_in_plain_directory_is_sibling(self, tmp_path: Path) -> None:
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / "dotfiles").mkdir()
        (home / "dotfiles" / "settings.json").write_text("{}")
        link = home / ".claude" / "settings.json"
        link.symlink_to(home / "dotfiles" / "settings.json")

        assert backup_dir_for(link, home=home) == home / ".claude"

    @pytest.mark.skipif(sys.platform == "win32", reason="POSIX descriptor walk")
    def test_linked_directory_relocates_under_runlayer(self, tmp_path: Path) -> None:
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "claude"
        real_dir.mkdir(parents=True)
        (home / ".claude").symlink_to(real_dir, target_is_directory=True)

        assert backup_dir_for(home / ".claude" / "settings.json", home=home) == (
            home / BACKUP_ROOT / ".claude"
        )

    @pytest.mark.skipif(sys.platform == "win32", reason="POSIX descriptor walk")
    def test_escaping_directory_link_relocates_too(self, tmp_path: Path) -> None:
        home = tmp_path / "home"
        home.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        (home / ".claude").symlink_to(outside, target_is_directory=True)

        assert backup_dir_for(home / ".claude" / "settings.json", home=home) == (
            home / BACKUP_ROOT / ".claude"
        )

    def test_nested_directory_keeps_relative_layout(self, tmp_path: Path) -> None:
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "code"
        real_dir.mkdir(parents=True)
        (home / ".config").mkdir()
        (home / ".config" / "Code").symlink_to(real_dir, target_is_directory=True)
        path = home / ".config" / "Code" / "User" / "settings.json"

        assert backup_dir_for(path, home=home) == (
            home / BACKUP_ROOT / ".config" / "Code" / "User"
        )

    def test_user_scope_uses_running_home(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        home = tmp_path / "home"
        real_dir = home / "dotfiles" / "claude"
        real_dir.mkdir(parents=True)
        (home / ".claude").symlink_to(real_dir, target_is_directory=True)
        (home / ".codex").mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))

        assert backup_dir_for(home / ".claude" / "settings.json", home=None) == (
            home / BACKUP_ROOT / ".claude"
        )
        assert backup_dir_for(home / ".codex" / "config.toml", home=None) == (
            home / ".codex"
        )

    def test_user_scope_outside_home_is_sibling(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path / "home"))
        elsewhere = tmp_path / "etc" / "client"
        elsewhere.mkdir(parents=True)

        assert backup_dir_for(elsewhere / "config.json", home=None) == elsewhere


def test_prune_keeps_newest_by_filename_timestamp(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text("{}")
    seeded = _seed(tmp_path, "settings.json", _MICRO_STAMPS)
    # Make the oldest-named file the most recently modified: retention must
    # follow the name, not mtime.
    os.utime(seeded[0], ns=(2_000_000_000_000_000_000, 2_000_000_000_000_000_000))

    removed = prune_backups(path, home=None)

    assert set(removed) == set(seeded[: len(seeded) - BACKUP_KEEP])
    assert _names(tmp_path) == {"settings.json"} | {
        p.name for p in seeded[len(seeded) - BACKUP_KEEP :]
    }


def test_prune_orders_legacy_second_names_with_microsecond_names(
    tmp_path: Path,
) -> None:
    path = tmp_path / "settings.json"
    path.write_text("{}")
    stamps = [
        "20260101_000000",
        "20260101_000000_000001",
        "20260102_000000",
        "20260103_000000_500000",
        "20260104_000000",
        "20260105_000000_000000",
        "20260106_000000",
    ]
    _seed(tmp_path, "settings.json", stamps)

    prune_backups(path, home=None, keep=3)

    assert _names(tmp_path) == {
        "settings.json",
        "settings.backup_20260104_000000.json",
        "settings.backup_20260105_000000_000000.json",
        "settings.backup_20260106_000000.json",
    }


def test_prune_never_touches_unrecognized_names(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text("{}")
    _seed(tmp_path, "settings.json", _MICRO_STAMPS)
    bystanders = {
        "settings.local.json",
        "settings.backup_notatimestamp.json",
        "settings.backup_20260101_000000.json.bak",
        "settings.backup_20260101_000000.toml",
        "other.backup_20260101_000000.json",
        "mysettings.backup_20260101_000000.json",
        "settings.backup_20260101_000000_1.json",
    }
    for name in bystanders:
        (tmp_path / name).write_text("keep")

    prune_backups(path, home=None, keep=0)

    assert _names(tmp_path) == {"settings.json"} | bystanders
    assert path.read_text() == "{}"


def test_prune_skips_symlinks_and_directories_named_like_backups(
    tmp_path: Path,
) -> None:
    path = tmp_path / "settings.json"
    path.write_text("{}")
    target = tmp_path / "target.json"
    target.write_text("precious")
    link = tmp_path / "settings.backup_20260101_000000_000000.json"
    link.symlink_to(target)
    directory = tmp_path / "settings.backup_20260102_000000_000000.json"
    directory.mkdir()
    (directory / "inner").write_text("x")
    regular = _seed(tmp_path, "settings.json", ["20260103_000000_000000"])[0]

    removed = prune_backups(path, home=None, keep=0)

    assert removed == [regular]
    assert link.is_symlink()
    assert target.read_text() == "precious"
    assert directory.is_dir()


def test_prune_with_missing_parent_is_a_noop(tmp_path: Path) -> None:
    assert prune_backups(tmp_path / "absent" / "settings.json", home=None) == []


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX descriptor walk")
def test_prune_under_home_anchor_never_follows_linked_config_dir(
    tmp_path: Path,
) -> None:
    home = tmp_path / "Users" / "alice"
    home.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    outside_backups = _seed(outside, "settings.json", _MICRO_STAMPS)
    (home / ".claude").symlink_to(outside, target_is_directory=True)
    path = home / ".claude" / "settings.json"

    removed = prune_backups(path, home=home)

    assert removed == []
    assert all(p.exists() for p in outside_backups)


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX descriptor walk")
def test_prune_drains_relocated_backups_behind_linked_config_dir(
    tmp_path: Path,
) -> None:
    """Backups for ``~/.claude -> ~/dotfiles/claude`` live under
    ``~/.runlayer/config-backups/.claude`` and prune there."""
    home = tmp_path / "Users" / "alice"
    real_dir = home / "dotfiles" / "claude"
    real_dir.mkdir(parents=True)
    (home / ".claude").symlink_to(real_dir, target_is_directory=True)
    relocated = home / BACKUP_ROOT / ".claude"
    relocated.mkdir(parents=True)
    seeded = _seed(relocated, "settings.json", _MICRO_STAMPS)
    path = home / ".claude" / "settings.json"

    removed = prune_backups(path, home=home)

    surplus = seeded[: len(seeded) - BACKUP_KEEP]
    assert {p.name for p in removed} == {p.name for p in surplus}
    assert _names(relocated) == {p.name for p in seeded[len(seeded) - BACKUP_KEEP :]}
    assert (home / ".claude").is_symlink()


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX descriptor walk")
def test_prune_never_touches_the_linked_tree_itself(tmp_path: Path) -> None:
    home = tmp_path / "Users" / "alice"
    real_dir = home / "dotfiles" / "claude"
    real_dir.mkdir(parents=True)
    seeded = _seed(real_dir, "settings.json", _MICRO_STAMPS)
    (home / ".claude").symlink_to(real_dir, target_is_directory=True)

    assert prune_backups(home / ".claude" / "settings.json", home=home) == []
    assert all(p.exists() for p in seeded)


def _linked_user_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """``~/.claude -> ~/dotfiles/claude`` with ``Path.home`` patched."""
    home = tmp_path / "home"
    real_dir = home / "dotfiles" / "claude"
    real_dir.mkdir(parents=True)
    (home / ".claude").symlink_to(real_dir, target_is_directory=True)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    return home


@pytest.mark.skipif(sys.platform == "win32", reason="symlink layout")
def test_prune_moves_legacy_siblings_out_of_linked_dir_and_keeps_newest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """First user-scope run after upgrading: the relocated dir does not exist
    yet. Older CLIs' copies beside the link move there and ``keep`` still
    holds — nothing is lost merely because it sat in the dotfiles tree."""
    home = _linked_user_home(tmp_path, monkeypatch)
    real_dir = home / "dotfiles" / "claude"
    (real_dir / "settings.json").write_text("{}")
    (real_dir / "settings.json.orig").write_text("unrelated")
    legacy = _seed(real_dir, "settings.json", _MICRO_STAMPS + ["20260101_000000"])
    relocated = home / BACKUP_ROOT / ".claude"

    removed = prune_backups(home / ".claude" / "settings.json", home=None)

    newest = sorted(p.name for p in legacy)[-BACKUP_KEEP:]
    assert _names(relocated) == set(newest)
    assert {p.name for p in removed} == {p.name for p in legacy} - set(newest)
    assert all(p.parent == relocated for p in removed)
    assert _names(real_dir) == {"settings.json", "settings.json.orig"}
    assert (relocated / newest[-1]).read_text() == _MICRO_STAMPS[-1]
    assert (home / ".claude").is_symlink()


@pytest.mark.skipif(sys.platform == "win32", reason="symlink layout")
def test_prune_retention_spans_relocated_and_legacy_copies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """1 relocated + 6 legacy: the newest ``keep`` survive across both, ordered
    by stamp, not by where the copy happened to live."""
    home = _linked_user_home(tmp_path, monkeypatch)
    real_dir = home / "dotfiles" / "claude"
    legacy = _seed(real_dir, "settings.json", _MICRO_STAMPS[:6])
    relocated = home / BACKUP_ROOT / ".claude"
    relocated.mkdir(parents=True)
    [fresh] = _seed(relocated, "settings.json", ["20261001_120000_000000"])

    prune_backups(home / ".claude" / "settings.json", home=None)

    expected = sorted(p.name for p in [*legacy, fresh])[-BACKUP_KEEP:]
    assert _names(relocated) == set(expected)
    assert _names(real_dir) == set()


@pytest.mark.skipif(sys.platform == "win32", reason="symlink layout")
def test_prune_leaves_legacy_sibling_in_place_when_move_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Best-effort: a copy that cannot be moved (``EXDEV``) stays where it is
    rather than being deleted; the rest still relocate."""
    home = _linked_user_home(tmp_path, monkeypatch)
    real_dir = home / "dotfiles" / "claude"
    legacy = _seed(real_dir, "settings.json", _MICRO_STAMPS[:3])
    stuck = legacy[1]
    real_replace = os.replace

    def flaky_replace(src, dst, *args, **kwargs):
        if Path(src).name == stuck.name:
            raise OSError(18, "cross-device link")
        return real_replace(src, dst, *args, **kwargs)

    monkeypatch.setattr(os, "replace", flaky_replace)

    assert prune_backups(home / ".claude" / "settings.json", home=None) == []

    assert _names(real_dir) == {stuck.name}
    assert _names(home / BACKUP_ROOT / ".claude") == {
        p.name for p in legacy if p != stuck
    }


@pytest.mark.skipif(sys.platform == "win32", reason="symlink layout")
def test_codex_steady_state_through_linked_dir_keeps_recovery_copies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``features.hooks`` already on: the Codex writer prunes without writing
    a copy. Legacy copies beside a linked ``~/.codex`` must survive that as
    the retained set, moved out of the dotfiles tree."""
    from runlayer_cli.hook_install import clients

    home = tmp_path / "home"
    real_dir = home / "dotfiles" / "codex"
    real_dir.mkdir(parents=True)
    (home / ".codex").symlink_to(real_dir, target_is_directory=True)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    (real_dir / "config.toml").write_text("[features]\nhooks = true\n")
    legacy = _seed(real_dir, "config.toml", _MICRO_STAMPS[:3])

    clients._enable_codex_hooks_feature(home / ".codex" / "config.toml")

    assert _names(real_dir) == {"config.toml"}
    assert _names(home / BACKUP_ROOT / ".codex") == {p.name for p in legacy}


def test_prune_leaves_legacy_siblings_when_config_dir_is_plain(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A plain config dir has no relocation; siblings are the primary set and
    keep the newest ``keep`` copies as before (no double drain)."""
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    seeded = _seed(home / ".claude", "settings.json", _MICRO_STAMPS)

    removed = prune_backups(home / ".claude" / "settings.json", home=None)

    assert {p.name for p in removed} == {
        p.name for p in seeded[: len(seeded) - BACKUP_KEEP]
    }
    assert _names(home / ".claude") == {
        p.name for p in seeded[len(seeded) - BACKUP_KEEP :]
    }


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX descriptor walk")
def test_prune_under_home_anchor_leaves_legacy_siblings_in_linked_tree(
    tmp_path: Path,
) -> None:
    """Root never wrote beside the link and never deletes inside the user's
    linked tree: only the relocated surplus drains under the MDM anchor."""
    home = tmp_path / "Users" / "alice"
    real_dir = home / "dotfiles" / "claude"
    real_dir.mkdir(parents=True)
    (home / ".claude").symlink_to(real_dir, target_is_directory=True)
    legacy = _seed(real_dir, "settings.json", _MICRO_STAMPS)
    relocated = home / BACKUP_ROOT / ".claude"
    relocated.mkdir(parents=True)
    seeded = _seed(relocated, "settings.json", _MICRO_STAMPS)

    removed = prune_backups(home / ".claude" / "settings.json", home=home)

    assert {p.name for p in removed} == {
        p.name for p in seeded[: len(seeded) - BACKUP_KEEP]
    }
    assert all(p.exists() for p in legacy)


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX descriptor walk")
def test_prune_under_home_anchor_removes_regular_surplus(tmp_path: Path) -> None:
    home = tmp_path / "Users" / "alice"
    claude = home / ".claude"
    claude.mkdir(parents=True)
    path = claude / "settings.json"
    path.write_text("{}")
    seeded = _seed(claude, "settings.json", _MICRO_STAMPS)

    removed = prune_backups(path, home=home)

    assert set(removed) == set(seeded[: len(seeded) - BACKUP_KEEP])
    assert len(list(claude.glob("settings.backup_*.json"))) == BACKUP_KEEP


def test_prune_on_windows_skips_reparse_point_candidates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "settings.json"
    path.write_text("{}")
    seeded = _seed(tmp_path, "settings.json", _MICRO_STAMPS)
    flagged = seeded[0]
    monkeypatch.setattr(config_backup.platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        config_backup,
        "path_has_link_or_reparse_point",
        lambda candidate: candidate == flagged,
    )

    removed = prune_backups(path, home=None)

    assert flagged.exists()
    assert flagged not in removed
    assert set(removed) == set(seeded[1 : len(seeded) - BACKUP_KEEP])


def test_prune_tolerates_unlink_failure_and_continues(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "settings.json"
    path.write_text("{}")
    seeded = _seed(tmp_path, "settings.json", _MICRO_STAMPS)
    stubborn = seeded[0]
    real_unlink = safe_fs.maybe_safe_unlink

    def flaky_unlink(candidate: Path, *, home: Path | None, **kwargs) -> bool:
        if candidate == stubborn:
            raise PermissionError("locked")
        return real_unlink(candidate, home=home, **kwargs)

    monkeypatch.setattr(config_backup, "maybe_safe_unlink", flaky_unlink)

    removed = prune_backups(path, home=None)

    assert stubborn.exists()
    assert set(removed) == set(seeded[1 : len(seeded) - BACKUP_KEEP])
    assert len(list(tmp_path.glob("settings.backup_*.json"))) == BACKUP_KEEP + 1
