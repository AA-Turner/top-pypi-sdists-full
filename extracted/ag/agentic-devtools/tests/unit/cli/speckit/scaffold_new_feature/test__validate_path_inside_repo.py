"""Tests for ``_validate_path_inside_repo``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_new_feature import _validate_path_inside_repo


class TestValidatePathInsideRepo:
    """_validate_path_inside_repo raises on paths outside the repo root."""

    def test_path_inside_repo_passes(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        target = repo_root / "specs" / "42-feature"
        _validate_path_inside_repo(target, repo_root)  # must not raise

    def test_path_outside_repo_raises(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        outside = tmp_path / "other"
        outside.mkdir()
        with pytest.raises(ValueError, match="Refusing to create parent stub outside repository root"):
            _validate_path_inside_repo(outside, repo_root)

    def test_resolved_path_pointing_outside_raises(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        outside = tmp_path / "external"
        outside.mkdir()
        specs_link = repo_root / "specs"
        target = specs_link / "42-feature"
        with (
            patch.object(Path, "resolve", side_effect=[outside / "42-feature", repo_root]),
            pytest.raises(ValueError, match="Refusing to create parent stub outside repository root"),
        ):
            _validate_path_inside_repo(target, repo_root)
