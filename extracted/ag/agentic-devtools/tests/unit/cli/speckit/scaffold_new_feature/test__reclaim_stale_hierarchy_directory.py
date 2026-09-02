"""Tests for ``_reclaim_stale_hierarchy_directory``."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _reclaim_stale_hierarchy_directory


def test_returns_false_for_a_non_directory(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.touch()

    assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False


def test_returns_false_for_a_symlinked_directory(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    with (
        patch.object(Path, "is_symlink", return_value=True),
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=True),
    ):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False


def test_returns_false_when_lock_is_not_stale(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    with patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=False):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False


def test_returns_false_when_directory_cannot_be_read(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=True),
        patch.object(Path, "iterdir", side_effect=OSError),
    ):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False


def test_returns_false_when_directory_contains_unexpected_entries(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    (lock_path / "unexpected").touch()
    with patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=True):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False


def test_treats_disappearing_directory_as_reclaimed(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=True),
        patch.object(Path, "rmdir", side_effect=FileNotFoundError),
    ):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is True


def test_returns_false_when_reclaim_claim_file_cannot_be_created(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=True),
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._try_create_hierarchy_reclaim_claim_file",
            return_value=None,
        ),
    ):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False


def test_returns_false_when_original_snapshot_cannot_be_captured(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=True),
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._capture_hierarchy_lock_directory_snapshot",
            return_value=None,
        ),
    ):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False


def test_returns_false_when_claimed_lock_no_longer_matches_original_snapshot(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    claim_path = lock_path / ".claim"
    (lock_path / ".owner").write_text('{"pid": 1, "created_at": 1}', encoding="utf-8")

    def _create_claim_path(_: Path) -> Path:
        claim_path.touch()
        return claim_path

    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=True),
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._try_create_hierarchy_reclaim_claim_file",
            side_effect=_create_claim_path,
        ),
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._capture_hierarchy_lock_directory_snapshot",
            side_effect=[(1, 1, '{"pid": 1, "created_at": 1}'), (2, 2, '{"pid": 2, "created_at": 2}')],
        ),
    ):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False

    assert lock_path.is_dir()


def test_restores_directory_when_reclaim_cleanup_fails(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=True),
        patch.object(Path, "rmdir", side_effect=OSError),
    ):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False
    assert lock_path.is_dir()


def test_cleans_up_claim_file_when_snapshot_changes_after_claim(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    claim_path = lock_path / ".claim"
    owner_path = lock_path / ".owner"
    owner_path.write_text('{"pid": 1, "created_at": 1}', encoding="utf-8")

    def _create_claim_path(_: Path) -> Path:
        claim_path.touch()
        return claim_path

    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._hierarchy_lock_is_stale", return_value=True),
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._try_create_hierarchy_reclaim_claim_file",
            side_effect=_create_claim_path,
        ),
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._capture_hierarchy_lock_directory_snapshot",
            side_effect=[(1, 1, '{"pid": 1, "created_at": 1}'), (2, 2, '{"pid": 2, "created_at": 2}')],
        ),
    ):
        assert _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=1) is False
    assert lock_path.is_dir()
    assert owner_path.exists()
    assert claim_path.exists() is False
