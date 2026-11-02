"""Tests for ``_hierarchy_lock_is_stale``."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _hierarchy_lock_is_stale


def test_returns_false_for_a_fresh_lock(tmp_path: Path) -> None:
    with (
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._read_hierarchy_lock_metadata",
            return_value=(None, 100.0),
        ),
        patch("agentic_devtools.cli.speckit.scaffold_new_feature.time.time", return_value=101.0),
    ):
        assert _hierarchy_lock_is_stale(tmp_path / ".hierarchy.yml.lock", stale_after_seconds=5) is False


def test_returns_true_for_an_old_lock_without_owner(tmp_path: Path) -> None:
    with (
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._read_hierarchy_lock_metadata",
            return_value=(None, 100.0),
        ),
        patch("agentic_devtools.cli.speckit.scaffold_new_feature.time.time", return_value=106.0),
    ):
        assert _hierarchy_lock_is_stale(tmp_path / ".hierarchy.yml.lock", stale_after_seconds=5) is True


def test_returns_false_for_an_old_lock_with_live_owner(tmp_path: Path) -> None:
    with (
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._read_hierarchy_lock_metadata",
            return_value=(123, 100.0),
        ),
        patch("agentic_devtools.cli.speckit.scaffold_new_feature.time.time", return_value=106.0),
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._is_pid_alive", return_value=True),
    ):
        assert _hierarchy_lock_is_stale(tmp_path / ".hierarchy.yml.lock", stale_after_seconds=5) is False


def test_returns_true_for_an_old_lock_with_dead_owner(tmp_path: Path) -> None:
    with (
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature._read_hierarchy_lock_metadata",
            return_value=(123, 100.0),
        ),
        patch("agentic_devtools.cli.speckit.scaffold_new_feature.time.time", return_value=106.0),
        patch("agentic_devtools.cli.speckit.scaffold_new_feature._is_pid_alive", return_value=False),
    ):
        assert _hierarchy_lock_is_stale(tmp_path / ".hierarchy.yml.lock", stale_after_seconds=5) is True


def test_returns_false_when_lock_timestamp_is_unavailable(tmp_path: Path) -> None:
    with patch(
        "agentic_devtools.cli.speckit.scaffold_new_feature._read_hierarchy_lock_metadata",
        return_value=(None, None),
    ):
        assert _hierarchy_lock_is_stale(tmp_path / ".hierarchy.yml.lock", stale_after_seconds=5) is False
