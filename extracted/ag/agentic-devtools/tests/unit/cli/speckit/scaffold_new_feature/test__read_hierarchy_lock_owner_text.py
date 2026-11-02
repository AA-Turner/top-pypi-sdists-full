"""Tests for ``_read_hierarchy_lock_owner_text``."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _read_hierarchy_lock_owner_text


def test_returns_owner_text_when_present(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    (lock_path / ".owner").write_text("owner", encoding="utf-8")

    assert _read_hierarchy_lock_owner_text(lock_path) == "owner"


def test_returns_none_when_owner_file_is_missing(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()

    assert _read_hierarchy_lock_owner_text(lock_path) is None


def test_returns_none_when_owner_file_cannot_be_read(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    owner_path = lock_path / ".owner"
    owner_path.write_text("owner", encoding="utf-8")

    with patch.object(Path, "read_text", side_effect=OSError):
        assert _read_hierarchy_lock_owner_text(lock_path) is None
