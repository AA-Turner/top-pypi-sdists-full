"""Tests for _discover_legacy_flat_tests function."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.review.test_discovery import _discover_legacy_flat_tests


class TestDiscoverLegacyFlatTests:
    """Tests for legacy flat convention test discovery."""

    def test_finds_flat_test_file(self, tmp_path: Path) -> None:
        """Discovers legacy flat test file for release commands (special case)."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_release_commands.py").write_text("")

        results = _discover_legacy_flat_tests("agentic_devtools/cli/release/commands.py", tmp_path)
        assert "tests/test_release_commands.py" in results

    def test_no_match_returns_empty(self, tmp_path: Path) -> None:
        """Returns empty list when no flat test file exists."""
        results = _discover_legacy_flat_tests("agentic_devtools/cli/git/core.py", tmp_path)
        assert results == []

    def test_leading_slash_path(self, tmp_path: Path) -> None:
        """Paths with leading slash are handled."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_core.py").write_text("")

        results = _discover_legacy_flat_tests("/agentic_devtools/cli/git/core.py", tmp_path)
        assert "tests/test_core.py" in results

    def test_non_package_path_is_supported(self, tmp_path: Path) -> None:
        """Repo-relative Python paths outside agentic_devtools/ are supported."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_module.py").write_text("")

        results = _discover_legacy_flat_tests("other/module.py", tmp_path)
        assert results == ["tests/test_module.py"]

    def test_non_py_file_returns_empty(self, tmp_path: Path) -> None:
        """Non-.py files return empty."""
        results = _discover_legacy_flat_tests("agentic_devtools/data.json", tmp_path)
        assert results == []

    def test_basename_only_lookup(self, tmp_path: Path) -> None:
        """Only basename is used (no multi-component candidates that risk false matches)."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        # Create a file that only matches the basename, not a multi-component candidate.
        (tests_dir / "test_core.py").write_text("")

        results = _discover_legacy_flat_tests("agentic_devtools/cli/git/core.py", tmp_path)
        assert "tests/test_core.py" in results
        # The full-path and last-two-component candidates are NOT generated.
        assert "tests/test_cli_git_core.py" not in results
        assert "tests/test_git_core.py" not in results
