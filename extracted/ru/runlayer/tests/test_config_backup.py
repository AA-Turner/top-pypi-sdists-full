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
    assert backup_path_for(tmp_path / "settings.json", now) == (
        tmp_path / "settings.backup_20260922_201530_123456.json"
    )
    assert backup_path_for(tmp_path / "config.toml", now).name == (
        "config.backup_20260922_201530_123456.toml"
    )


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

    def flaky_unlink(candidate: Path, *, home: Path | None) -> bool:
        if candidate == stubborn:
            raise PermissionError("locked")
        return real_unlink(candidate, home=home)

    monkeypatch.setattr(config_backup, "maybe_safe_unlink", flaky_unlink)

    removed = prune_backups(path, home=None)

    assert stubborn.exists()
    assert set(removed) == set(seeded[1 : len(seeded) - BACKUP_KEEP])
    assert len(list(tmp_path.glob("settings.backup_*.json"))) == BACKUP_KEEP + 1
