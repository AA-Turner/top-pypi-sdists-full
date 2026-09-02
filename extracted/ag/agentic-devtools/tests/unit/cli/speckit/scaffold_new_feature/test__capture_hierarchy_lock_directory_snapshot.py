"""Tests for ``_capture_hierarchy_lock_directory_snapshot``."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _capture_hierarchy_lock_directory_snapshot


def test_returns_directory_identity_and_owner_text(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    (lock_path / ".owner").write_text("owner", encoding="utf-8")

    snapshot = _capture_hierarchy_lock_directory_snapshot(lock_path)

    assert snapshot is not None
    assert snapshot[:2] == (lock_path.stat().st_dev, lock_path.stat().st_ino)
    assert snapshot[2] == "owner"


def test_returns_none_when_lock_directory_cannot_be_statted(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()

    with patch.object(Path, "stat", side_effect=OSError):
        assert _capture_hierarchy_lock_directory_snapshot(lock_path) is None
