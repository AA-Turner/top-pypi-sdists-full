"""Tests for ``_validate_within_specs``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import (
    FeatureResolutionError,
    _validate_within_specs,
)


class TestValidateWithinSpecs:
    """_validate_within_specs rejects paths that escape specs_dir."""

    def test_valid_child_passes(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        child = specs_dir / "042-feature"
        # Should not raise.
        _validate_within_specs(child, specs_dir, source="test")

    def test_dotdot_traversal_raises(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        outside = specs_dir / ".." / "outside"

        with pytest.raises(FeatureResolutionError, match=r"outside specs/"):
            _validate_within_specs(outside, specs_dir, source="test")

    def test_absolute_path_outside_raises(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        outside = tmp_path / "other"
        outside.mkdir()

        with pytest.raises(FeatureResolutionError, match=r"outside specs/"):
            _validate_within_specs(outside, specs_dir, source="test")

    def test_resolved_symlink_escaping_raises(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        link = specs_dir / "escape-link"

        with (
            patch.object(Path, "resolve", side_effect=[outside, specs_dir]),
            pytest.raises(FeatureResolutionError, match=r"outside specs/"),
        ):
            _validate_within_specs(link, specs_dir, source="test")

    def test_error_includes_source_label(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()

        with pytest.raises(FeatureResolutionError, match=r"'.specify/feature\.json'"):
            _validate_within_specs(outside, specs_dir, source=".specify/feature.json")

    def test_resolved_specs_root_outside_repo_raises(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        outside_specs = tmp_path / "outside-specs"
        outside_specs.mkdir()
        specs_link = repo_root / "specs"
        outside_child = specs_link / "042-feature"

        with (
            patch.object(Path, "resolve", side_effect=[outside_specs / "042-feature", outside_specs, repo_root]),
            pytest.raises(FeatureResolutionError, match=r"outside the repository root"),
        ):
            _validate_within_specs(outside_child, specs_link, source="test", repo_root=repo_root)
