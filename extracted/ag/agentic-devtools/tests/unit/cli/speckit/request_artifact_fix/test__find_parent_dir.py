"""Tests for ``_find_parent_dir()`` in ``request_artifact_fix``."""

from pathlib import Path

from agentic_devtools.cli.speckit.request_artifact_fix import _find_parent_dir


class TestFindParentDir:
    """Locates a parent spec directory by issue number."""

    def test_returns_none_when_base_path_missing(self, tmp_path: Path) -> None:
        assert _find_parent_dir(tmp_path / "nope", "1859") is None

    def test_matches_exact_directory_name(self, tmp_path: Path) -> None:
        (tmp_path / "1859").mkdir()
        assert _find_parent_dir(tmp_path, "1859") == tmp_path / "1859"

    def test_matches_prefixed_directory_name(self, tmp_path: Path) -> None:
        (tmp_path / "1859-feature").mkdir()
        assert _find_parent_dir(tmp_path, "1859") == tmp_path / "1859-feature"

    def test_ignores_files_and_unrelated_directories(self, tmp_path: Path) -> None:
        (tmp_path / "1859").write_text("not a directory", encoding="utf-8")
        (tmp_path / "2000-other").mkdir()
        assert _find_parent_dir(tmp_path, "1859") is None

    def test_returns_none_when_multiple_matches_exist(self, tmp_path: Path) -> None:
        (tmp_path / "1859-second").mkdir()
        (tmp_path / "1859-first").mkdir()
        assert _find_parent_dir(tmp_path, "1859") is None

    def test_finds_nested_directory_within_depth_limit(self, tmp_path: Path) -> None:
        nested = tmp_path / "a" / "b" / "1859"
        nested.mkdir(parents=True)
        assert _find_parent_dir(tmp_path, "1859") == nested

    def test_ignores_directory_beyond_depth_limit(self, tmp_path: Path) -> None:
        (tmp_path / "a" / "b" / "c" / "1859").mkdir(parents=True)
        assert _find_parent_dir(tmp_path, "1859") is None
