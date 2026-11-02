"""Tests for ``_read_hierarchy_lock_metadata``."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _read_hierarchy_lock_metadata


def test_reads_owner_metadata_from_directory(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    (lock_path / ".owner").write_text('{"pid": 123, "created_at": 1.5}', encoding="utf-8")

    assert _read_hierarchy_lock_metadata(lock_path) == (123, 1.5)


def test_uses_directory_mtime_when_owner_timestamp_is_missing(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    with (
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._parse_hierarchy_lock_metadata",
            return_value=(123, None),
        ),
        patch.object(Path, "stat", return_value=SimpleNamespace(st_mtime=4.5)),
    ):
        assert _read_hierarchy_lock_metadata(lock_path) == (123, 4.5)


def test_returns_missing_timestamp_when_metadata_and_stat_are_unavailable(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    with (
        patch.object(Path, "read_text", side_effect=OSError),
        patch.object(Path, "stat", side_effect=OSError),
    ):
        assert _read_hierarchy_lock_metadata(lock_path) == (None, None)
