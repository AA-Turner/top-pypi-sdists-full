"""Tests for ``_find_by_prefix``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import FeatureResolutionError, _find_by_prefix


class TestFindByPrefix:
    """_find_by_prefix locates a single specs/ subdirectory matching a numeric prefix."""

    def test_returns_none_when_specs_dir_missing(self, tmp_path: Path) -> None:
        assert _find_by_prefix(tmp_path / "specs", "042") is None

    def test_returns_none_when_no_match(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "001-other").mkdir(parents=True)

        assert _find_by_prefix(specs_dir, "042") is None

    def test_matches_exact_prefix_directory(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        exact = specs_dir / "042"
        exact.mkdir(parents=True)

        assert _find_by_prefix(specs_dir, "042") == exact

    def test_matches_prefixed_directory(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        match = specs_dir / "042-my-feature"
        match.mkdir(parents=True)

        assert _find_by_prefix(specs_dir, "042") == match

    def test_matches_nested_prefixed_directory(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        match = specs_dir / "010-parent" / "042-my-feature"
        match.mkdir(parents=True)

        assert _find_by_prefix(specs_dir, "042") == match

    def test_ignores_files_and_symlinks(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        (specs_dir / "042-file.txt").write_text("not a dir", encoding="utf-8")
        real_dir = specs_dir / "099-real"
        real_dir.mkdir()
        symlink = specs_dir / "042-link"
        symlink.mkdir()

        def _is_symlink(path: Path) -> bool:
            return path == symlink

        with patch.object(Path, "is_symlink", _is_symlink):
            assert _find_by_prefix(specs_dir, "042") is None

    def test_raises_on_multiple_matches(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "042-a").mkdir(parents=True)
        (specs_dir / "042-b").mkdir(parents=True)

        with pytest.raises(FeatureResolutionError, match="Multiple spec directories"):
            _find_by_prefix(specs_dir, "042")

    def test_raises_on_multiple_nested_matches(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "010-parent" / "042-a").mkdir(parents=True)
        (specs_dir / "020-parent" / "042-b").mkdir(parents=True)

        with pytest.raises(FeatureResolutionError, match="Multiple spec directories"):
            _find_by_prefix(specs_dir, "042")

    def test_matches_zero_padded_directory_with_unpadded_prefix(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        match = specs_dir / "042-feature"
        match.mkdir(parents=True)

        assert _find_by_prefix(specs_dir, "42") == match

    def test_matches_unpadded_directory_with_padded_prefix(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        match = specs_dir / "42-feature"
        match.mkdir(parents=True)

        assert _find_by_prefix(specs_dir, "042") == match

    def test_returns_none_for_invalid_prefix(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "042-feature").mkdir(parents=True)

        assert _find_by_prefix(specs_dir, "not-a-number") is None
