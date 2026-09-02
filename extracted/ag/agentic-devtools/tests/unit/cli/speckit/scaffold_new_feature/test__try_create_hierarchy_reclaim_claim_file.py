"""Tests for ``_try_create_hierarchy_reclaim_claim_file``."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _try_create_hierarchy_reclaim_claim_file


def test_creates_claim_file(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()

    claim_path = _try_create_hierarchy_reclaim_claim_file(lock_path)

    assert claim_path is not None
    assert claim_path.exists() is True


def test_returns_none_when_open_fails(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()

    with patch("agentic_devtools.cli.speckit.scaffold_new_feature.os.open", side_effect=OSError):
        assert _try_create_hierarchy_reclaim_claim_file(lock_path) is None


def test_works_without_o_nofollow(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()

    with patch("agentic_devtools.cli.speckit.scaffold_new_feature.hasattr", return_value=False):
        claim_path = _try_create_hierarchy_reclaim_claim_file(lock_path)

    assert claim_path is not None
    assert claim_path.exists() is True
