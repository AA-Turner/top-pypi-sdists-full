"""Tests for ``_find_specify_project_root``."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import (
    FeatureResolutionError,
    _find_specify_project_root,
)


class TestFindSpecifyProjectRoot:
    """_find_specify_project_root walks up from start looking for .specify."""

    def test_returns_directory_containing_specify(self, tmp_path: Path) -> None:
        (tmp_path / ".specify").mkdir()
        result = _find_specify_project_root(start=tmp_path)
        assert result == tmp_path

    def test_returns_ancestor_when_specify_is_in_parent(self, tmp_path: Path) -> None:
        (tmp_path / ".specify").mkdir()
        nested = tmp_path / "sub" / "deep"
        nested.mkdir(parents=True)
        result = _find_specify_project_root(start=nested)
        assert result == tmp_path

    def test_returns_none_when_no_specify_dir_found(self, tmp_path: Path) -> None:
        result = _find_specify_project_root(start=tmp_path)
        assert result is None

    def test_specify_init_dir_env_overrides_start(self, tmp_path: Path) -> None:
        project_root = tmp_path / "project"
        (project_root / ".specify").mkdir(parents=True)
        other = tmp_path / "other"
        other.mkdir()
        with patch.dict(os.environ, {"SPECIFY_INIT_DIR": str(project_root)}):
            result = _find_specify_project_root(start=other)
        assert result == project_root

    def test_specify_init_dir_raises_when_directory_does_not_exist(self, tmp_path: Path) -> None:
        missing = tmp_path / "nonexistent"
        with patch.dict(os.environ, {"SPECIFY_INIT_DIR": str(missing)}):
            with pytest.raises(FeatureResolutionError, match="is not an existing directory"):
                _find_specify_project_root()

    def test_specify_init_dir_raises_when_no_specify_subdir(self, tmp_path: Path) -> None:
        no_specify = tmp_path / "no-specify-here"
        no_specify.mkdir()
        with patch.dict(os.environ, {"SPECIFY_INIT_DIR": str(no_specify)}):
            with pytest.raises(FeatureResolutionError, match=r"does not contain a '\.specify' directory"):
                _find_specify_project_root()

    def test_specify_init_dir_does_not_walk_ancestors(self, tmp_path: Path) -> None:
        # Even if a parent has .specify, an SPECIFY_INIT_DIR without .specify raises.
        (tmp_path / ".specify").mkdir()
        child = tmp_path / "child"
        child.mkdir()
        with patch.dict(os.environ, {"SPECIFY_INIT_DIR": str(child)}):
            with pytest.raises(FeatureResolutionError):
                _find_specify_project_root()

    def test_specify_init_dir_empty_falls_through_to_start(self, tmp_path: Path) -> None:
        (tmp_path / ".specify").mkdir()
        with patch.dict(os.environ, {"SPECIFY_INIT_DIR": "   "}):
            result = _find_specify_project_root(start=tmp_path)
        assert result == tmp_path

    def test_nested_specify_takes_precedence_over_outer(self, tmp_path: Path) -> None:
        outer = tmp_path / "outer"
        (outer / ".specify").mkdir(parents=True)
        inner = outer / "inner"
        (inner / ".specify").mkdir(parents=True)
        result = _find_specify_project_root(start=inner / "src")
        # nearest ancestor is `inner`
        assert result == inner

    def test_defaults_to_cwd_when_start_is_none(self, tmp_path: Path) -> None:
        (tmp_path / ".specify").mkdir()
        with patch("agentic_devtools.cli.speckit.scaffold_common.Path.cwd", return_value=tmp_path):
            with patch.dict(os.environ, {"SPECIFY_INIT_DIR": ""}, clear=False):
                result = _find_specify_project_root()
        assert result == tmp_path

    def test_blank_specify_init_dir_falls_through_to_start_walk(self, tmp_path: Path) -> None:
        # Whitespace SPECIFY_INIT_DIR is treated as unset; the walk starts from `start`.
        # With no .specify under tmp_path, the result is None.
        with patch.dict(os.environ, {"SPECIFY_INIT_DIR": "   "}):
            result = _find_specify_project_root(start=tmp_path)
        assert result is None
