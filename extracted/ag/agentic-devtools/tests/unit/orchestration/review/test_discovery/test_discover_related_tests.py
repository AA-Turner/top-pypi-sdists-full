"""Tests for discover_related_tests function."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.review.test_discovery import discover_related_tests


class TestDiscoverRelatedTests:
    """Tests for combined test discovery."""

    def test_no_tests_sets_missing_flag(self, tmp_path: Path) -> None:
        """No matching tests → missing_tests=True."""
        result = discover_related_tests("agentic_devtools/cli/git/core.py", repo_root=tmp_path)
        assert result["related_tests"] == []
        assert result["missing_tests"] is True

    def test_non_py_file_not_flagged_missing(self, tmp_path: Path) -> None:
        """Non-.py files (docs, config, assets) return missing_tests=False."""
        for non_py_path in [
            "agentic_devtools/data.json",
            "docs/README.md",
            ".github/agdt-config.json",
        ]:
            result = discover_related_tests(non_py_path, repo_root=tmp_path)
            assert result["related_tests"] == []
            assert result["missing_tests"] is False, f"Expected missing_tests=False for {non_py_path!r}"

    def test_non_first_party_py_file_uses_generic_mapping(self, tmp_path: Path) -> None:
        """Python files outside agentic_devtools/ still discover related tests."""
        test_dir = tmp_path / "tests" / "unit" / "src" / "app"
        test_dir.mkdir(parents=True)
        (test_dir / "test_appmodule.py").write_text("")

        result = discover_related_tests("src/app.py", repo_root=tmp_path)
        assert result["related_tests"] == ["tests/unit/src/app/test_appmodule.py"]
        assert result["missing_tests"] is False

    def test_package_scaffolding_files_not_flagged_missing(self, tmp_path: Path) -> None:
        """``__init__.py`` / ``_version.py`` never have tests → missing_tests=False."""
        for scaffolding_path in [
            "agentic_devtools/__init__.py",
            "agentic_devtools/orchestration/review/__init__.py",
            "agentic_devtools/_version.py",
        ]:
            result = discover_related_tests(scaffolding_path, repo_root=tmp_path)
            assert result["related_tests"] == []
            assert result["missing_tests"] is False, f"Expected missing_tests=False for {scaffolding_path!r}"

    def test_combines_both_conventions(self, tmp_path: Path) -> None:
        """Results from both conventions are merged."""
        # 1:1:1
        test_dir = tmp_path / "tests" / "unit" / "cli" / "git" / "core"
        test_dir.mkdir(parents=True)
        (test_dir / "test_func.py").write_text("")

        # Legacy flat (basename only)
        tests_dir = tmp_path / "tests"
        (tests_dir / "test_core.py").write_text("")

        result = discover_related_tests("agentic_devtools/cli/git/core.py", repo_root=tmp_path)
        assert len(result["related_tests"]) == 2
        assert result["missing_tests"] is False

    def test_deterministic_output(self, tmp_path: Path) -> None:
        """Same input always produces same output."""
        test_dir = tmp_path / "tests" / "unit" / "state"
        test_dir.mkdir(parents=True)
        (test_dir / "test_b.py").write_text("")
        (test_dir / "test_a.py").write_text("")

        r1 = discover_related_tests("agentic_devtools/state.py", repo_root=tmp_path)
        r2 = discover_related_tests("agentic_devtools/state.py", repo_root=tmp_path)
        assert r1 == r2

    def test_auto_detect_repo_root_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When repo root auto-detection fails, returns missing."""
        import agentic_devtools.orchestration.review.test_discovery as td_module

        monkeypatch.setattr(td_module, "_cached_repo_root", False)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            result = discover_related_tests("agentic_devtools/state.py", repo_root=None)
        assert result["related_tests"] == []
        assert result["missing_tests"] is True

    def test_auto_detect_repo_root_exception(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When subprocess raises, returns missing."""
        import agentic_devtools.orchestration.review.test_discovery as td_module

        monkeypatch.setattr(td_module, "_cached_repo_root", False)
        with patch("subprocess.run", side_effect=OSError("no git")):
            result = discover_related_tests("agentic_devtools/state.py", repo_root=None)
        assert result["related_tests"] == []
        assert result["missing_tests"] is True

    def test_auto_detect_repo_root_success(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """When git rev-parse succeeds, uses detected root."""
        import agentic_devtools.orchestration.review.test_discovery as td_module

        monkeypatch.setattr(td_module, "_cached_repo_root", False)
        test_dir = tmp_path / "tests" / "unit" / "state"
        test_dir.mkdir(parents=True)
        (test_dir / "test_get_value.py").write_text("")

        with patch("subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = str(tmp_path)
            mock_run.return_value = mock_result
            result = discover_related_tests("agentic_devtools/state.py", repo_root=None)

        assert len(result["related_tests"]) == 1
        assert result["missing_tests"] is False

    def test_cached_repo_root_skips_subprocess(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Second call with repo_root=None reuses cached result without calling subprocess."""
        import agentic_devtools.orchestration.review.test_discovery as td_module

        monkeypatch.setattr(td_module, "_cached_repo_root", tmp_path)

        # No test files in tmp_path — expect empty results but no subprocess call
        with patch("subprocess.run") as mock_run:
            result = discover_related_tests("agentic_devtools/state.py", repo_root=None)
            mock_run.assert_not_called()

        assert result["related_tests"] == []
        assert result["missing_tests"] is True

    def test_cached_none_skips_subprocess_and_returns_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Cached None (previous failure) returns missing without invoking subprocess."""
        import agentic_devtools.orchestration.review.test_discovery as td_module

        monkeypatch.setattr(td_module, "_cached_repo_root", None)
        with patch("subprocess.run") as mock_run:
            result = discover_related_tests("agentic_devtools/state.py", repo_root=None)
            mock_run.assert_not_called()
        assert result["related_tests"] == []
        assert result["missing_tests"] is True

    def test_non_py_path_with_failed_cache_returns_not_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Non-Python paths return missing_tests=False even when repo-root cache is None.

        Regression test for the ordering bug where repo-root auto-detection ran
        before the applicability check, causing non-Python paths to produce
        a false ``missing_tests=True`` when called outside a git worktree.
        """
        import agentic_devtools.orchestration.review.test_discovery as td_module

        # Simulate: git previously failed → _cached_repo_root is None
        monkeypatch.setattr(td_module, "_cached_repo_root", None)
        with patch("subprocess.run") as mock_run:
            # Non-Python path — should short-circuit before cache lookup
            result = discover_related_tests("scripts/helper.sh", repo_root=None)
            mock_run.assert_not_called()
        assert result["related_tests"] == []
        assert result["missing_tests"] is False

    def test_api_only_mode_infers_remote_candidates_without_repo_root(self) -> None:
        """API-only mode infers candidate test paths from the source path/content."""
        source = "def get_value() -> str:\n    return 'x'\n\nclass WorktreeSetupResult:\n    pass\n"

        result = discover_related_tests(
            "agentic_devtools/state.py",
            repo_root=None,
            source_content=source,
            auto_detect_repo_root=False,
        )

        assert result["missing_tests"] is False
        assert result["related_tests"] == [
            "tests/test_state.py",
            "tests/unit/state/test_get_value.py",
            "tests/unit/state/test_worktreesetupresult.py",
        ]

    def test_api_only_mode_without_source_content_keeps_legacy_candidate_only(self) -> None:
        """Without source content, API-only mode still returns the flat inferred candidate."""
        result = discover_related_tests(
            "agentic_devtools/state.py",
            repo_root=None,
            source_content=None,
            auto_detect_repo_root=False,
        )

        assert result["missing_tests"] is False
        assert result["related_tests"] == ["tests/test_state.py"]

    def test_api_only_mode_with_syntax_error_ignores_symbol_inference(self) -> None:
        """Syntax-invalid source content falls back to inferable non-AST candidates."""
        result = discover_related_tests(
            "agentic_devtools/state.py",
            repo_root=None,
            source_content="def broken(:\n",
            auto_detect_repo_root=False,
        )

        assert result["missing_tests"] is False
        assert result["related_tests"] == ["tests/test_state.py"]

    def test_api_only_mode_non_python_path_returns_empty(self) -> None:
        """API-only mode still short-circuits non-Python paths."""
        result = discover_related_tests(
            "docs/README.md",
            repo_root=None,
            source_content="# doc\n",
            auto_detect_repo_root=False,
        )

        assert result["related_tests"] == []
        assert result["missing_tests"] is False
