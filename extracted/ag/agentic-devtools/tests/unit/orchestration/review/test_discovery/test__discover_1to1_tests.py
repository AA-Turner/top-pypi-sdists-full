"""Tests for _discover_1to1_tests function."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.review.test_discovery import _discover_1to1_tests


class TestDiscover1to1Tests:
    """Tests for 1:1:1 convention test discovery."""

    def test_finds_tests_in_unit_dir(self, tmp_path: Path) -> None:
        """Discovers tests following 1:1:1 convention."""
        test_dir = tmp_path / "tests" / "unit" / "cli" / "git" / "core"
        test_dir.mkdir(parents=True)
        (test_dir / "test_get_current_branch.py").write_text("")
        (test_dir / "test_run_safe.py").write_text("")
        (test_dir / "__init__.py").write_text("")

        results = _discover_1to1_tests("agentic_devtools/cli/git/core.py", tmp_path)
        assert len(results) == 2
        assert "tests/unit/cli/git/core/test_get_current_branch.py" in results
        assert "tests/unit/cli/git/core/test_run_safe.py" in results

    def test_no_test_dir_returns_empty(self, tmp_path: Path) -> None:
        """Returns empty list when test directory doesn't exist."""
        results = _discover_1to1_tests("agentic_devtools/cli/git/core.py", tmp_path)
        assert results == []

    def test_leading_slash_path(self, tmp_path: Path) -> None:
        """Paths with leading slash are handled."""
        test_dir = tmp_path / "tests" / "unit" / "cli" / "git" / "core"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("")

        results = _discover_1to1_tests("/agentic_devtools/cli/git/core.py", tmp_path)
        assert len(results) == 1

    def test_non_package_path_is_supported(self, tmp_path: Path) -> None:
        """Repo-relative Python paths outside agentic_devtools/ are supported."""
        test_dir = tmp_path / "tests" / "unit" / "src" / "app"
        test_dir.mkdir(parents=True)
        (test_dir / "test_appmodule.py").write_text("")

        results = _discover_1to1_tests("src/app.py", tmp_path)
        assert results == ["tests/unit/src/app/test_appmodule.py"]

    def test_non_py_file_returns_empty(self, tmp_path: Path) -> None:
        """Non-.py files return empty."""
        results = _discover_1to1_tests("agentic_devtools/data.json", tmp_path)
        assert results == []

    def test_top_level_module(self, tmp_path: Path) -> None:
        """Top-level module (no subdirectory) is handled."""
        test_dir = tmp_path / "tests" / "unit" / "state"
        test_dir.mkdir(parents=True)
        (test_dir / "test_get_value.py").write_text("")

        results = _discover_1to1_tests("agentic_devtools/state.py", tmp_path)
        assert len(results) == 1
