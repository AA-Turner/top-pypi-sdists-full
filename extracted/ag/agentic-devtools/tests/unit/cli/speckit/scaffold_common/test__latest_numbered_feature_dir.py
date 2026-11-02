"""Tests for ``_latest_numbered_feature_dir``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import FeatureResolutionError, _latest_numbered_feature_dir


class TestLatestNumberedFeatureDir:
    """_latest_numbered_feature_dir returns the highest-numbered specs/ directory."""

    def test_returns_none_when_specs_dir_missing(self, tmp_path: Path) -> None:
        assert _latest_numbered_feature_dir(tmp_path / "specs") is None

    def test_returns_none_when_no_numbered_dirs(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "not-numbered").mkdir(parents=True)

        assert _latest_numbered_feature_dir(specs_dir) is None

    def test_returns_highest_numbered_directory(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "001-a").mkdir(parents=True)
        (specs_dir / "042-b").mkdir(parents=True)
        (specs_dir / "007-c").mkdir(parents=True)

        assert _latest_numbered_feature_dir(specs_dir) == "042-b"

    def test_ignores_files(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        (specs_dir / "099-file.txt").write_text("not a dir", encoding="utf-8")

        assert _latest_numbered_feature_dir(specs_dir) is None

    def test_ignores_numbered_symlink_directories(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        (specs_dir / "042-local").mkdir()
        external_dir = specs_dir / "999-external"
        external_dir.mkdir()

        def _is_symlink(path: Path) -> bool:
            return path == external_dir

        with patch.object(Path, "is_symlink", _is_symlink):
            assert _latest_numbered_feature_dir(specs_dir) == "042-local"

    def test_returns_nested_highest_numbered_directory(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "010-parent").mkdir(parents=True)
        (specs_dir / "010-parent" / "042-child").mkdir()

        assert _latest_numbered_feature_dir(specs_dir) == "010-parent/042-child"

    def test_raises_on_tied_highest_number_across_depths(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "042-flat").mkdir(parents=True)
        (specs_dir / "010-parent" / "042-nested").mkdir(parents=True)

        with pytest.raises(FeatureResolutionError, match="042-flat") as exc_info:
            _latest_numbered_feature_dir(specs_dir)

        assert "042-nested" in str(exc_info.value)

    def test_raises_on_tied_highest_number(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "042-a").mkdir(parents=True)
        (specs_dir / "042-b").mkdir(parents=True)
        (specs_dir / "001-c").mkdir(parents=True)

        with pytest.raises(FeatureResolutionError, match="042-a") as exc_info:
            _latest_numbered_feature_dir(specs_dir)

        assert "042-b" in str(exc_info.value)

    def test_returns_bare_numeric_directory(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "1000-old").mkdir(parents=True)
        (specs_dir / "2249").mkdir(parents=True)

        assert _latest_numbered_feature_dir(specs_dir) == "2249"

    def test_bare_numeric_and_dashed_treated_as_same_number_causes_tie(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        (specs_dir / "42").mkdir(parents=True)
        (specs_dir / "042-feature").mkdir(parents=True)

        with pytest.raises(FeatureResolutionError, match="42"):
            _latest_numbered_feature_dir(specs_dir)

    def test_continues_after_a_lower_number_than_current_best(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        with patch(
            "agentic_devtools.cli.speckit.scaffold_common.os.walk",
            return_value=[(str(specs_dir), ["099-high", "042-low"], [])],
        ):
            assert _latest_numbered_feature_dir(specs_dir) == "099-high"
