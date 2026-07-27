"""Comprehensive tests for sage/core/project.py - Project discovery utilities."""

import pytest
from pathlib import Path
import tempfile

from sage.core.project import (
    detect_test_files,
    detect_runnable_files,
    discover_workspace_project_roots,
    project_root_score,
    default_project_root,
    discover_npm_script,
    discover_python_test_command,
    discover_project_test_command,
    discover_project_full_test_command,
    discover_project_root_for_file,
    command_from_project_root,
    validation_command_for_written_files,
    PROJECT_MARKERS,
    SKIP_DIRS,
)


# =============================================================================
# Tests for Constants
# =============================================================================


class TestProjectMarkers:
    """Tests for PROJECT_MARKERS constant."""

    def test_is_tuple(self):
        """PROJECT_MARKERS is a tuple."""
        assert isinstance(PROJECT_MARKERS, tuple)

    def test_contains_pyproject(self):
        """Contains pyproject.toml."""
        assert "pyproject.toml" in PROJECT_MARKERS

    def test_contains_package_json(self):
        """Contains package.json."""
        assert "package.json" in PROJECT_MARKERS

    def test_contains_cargo_toml(self):
        """Contains Cargo.toml."""
        assert "Cargo.toml" in PROJECT_MARKERS

    def test_contains_go_mod(self):
        """Contains go.mod."""
        assert "go.mod" in PROJECT_MARKERS


class TestSkipDirs:
    """Tests for SKIP_DIRS constant."""

    def test_is_set(self):
        """SKIP_DIRS is a set."""
        assert isinstance(SKIP_DIRS, set)

    def test_contains_git(self):
        """Contains .git."""
        assert ".git" in SKIP_DIRS

    def test_contains_venv(self):
        """Contains venv directories."""
        assert "venv" in SKIP_DIRS
        assert ".venv" in SKIP_DIRS

    def test_contains_node_modules(self):
        """Contains node_modules."""
        assert "node_modules" in SKIP_DIRS

    def test_contains_pycache(self):
        """Contains __pycache__."""
        assert "__pycache__" in SKIP_DIRS

    def test_contains_build_dirs(self):
        """Contains build output directories."""
        assert "dist" in SKIP_DIRS
        assert "build" in SKIP_DIRS


# =============================================================================
# Tests for detect_test_files function
# =============================================================================


class TestDetectTestFiles:
    """Tests for detect_test_files function."""

    def test_detect_test_prefix(self):
        """Detect files with test_ prefix."""
        files = ["test_main.py", "main.py", "test_utils.py"]
        result = detect_test_files(files)
        assert "test_main.py" in result
        assert "test_utils.py" in result
        assert "main.py" not in result

    def test_only_python_files(self):
        """Only return Python test files."""
        files = ["test_main.py", "test_app.js", "test_config.ts"]
        result = detect_test_files(files)
        assert result == ["test_main.py"]

    def test_empty_list(self):
        """Empty list returns empty."""
        result = detect_test_files([])
        assert result == []

    def test_no_test_files(self):
        """No test files returns empty."""
        files = ["main.py", "utils.py", "config.py"]
        result = detect_test_files(files)
        assert result == []

    def test_nested_paths(self):
        """Handle nested paths."""
        files = ["tests/test_main.py", "src/app.py"]
        result = detect_test_files(files)
        assert "tests/test_main.py" in result

    def test_not_matching_contains_test(self):
        """Files containing 'test' but not prefixed are excluded."""
        files = ["test_main.py", "testing.py", "my_test.py"]
        result = detect_test_files(files)
        # Only test_main.py starts with test_
        assert result == ["test_main.py"]


# =============================================================================
# Tests for detect_runnable_files function
# =============================================================================


class TestDetectRunnableFiles:
    """Tests for detect_runnable_files function."""

    def test_detect_python_files(self):
        """Detect Python files."""
        files = ["main.py", "utils.py", "app.js"]
        result = detect_runnable_files(files)
        assert "main.py" in result
        assert "utils.py" in result
        assert "app.js" not in result

    def test_empty_list(self):
        """Empty list returns empty."""
        result = detect_runnable_files([])
        assert result == []

    def test_no_python_files(self):
        """No Python files returns empty."""
        files = ["main.js", "app.ts", "config.json"]
        result = detect_runnable_files(files)
        assert result == []

    def test_nested_paths(self):
        """Handle nested paths."""
        files = ["src/main.py", "tests/test_main.py"]
        result = detect_runnable_files(files)
        assert len(result) == 2


# =============================================================================
# Tests for discover_workspace_project_roots function
# =============================================================================


class TestDiscoverWorkspaceProjectRoots:
    """Tests for discover_workspace_project_roots function."""

    def test_empty_directory(self):
        """Empty directory returns empty list or cwd."""
        with tempfile.TemporaryDirectory() as tmpdir:
            roots = discover_workspace_project_roots(Path(tmpdir))
            # Empty directory has no markers
            assert roots == []

    def test_single_pyproject(self):
        """Detect single pyproject.toml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "pyproject.toml").write_text("[project]")
            roots = discover_workspace_project_roots(Path(tmpdir))
            assert len(roots) == 1
            assert roots[0] == Path(tmpdir).resolve()

    def test_nested_projects(self):
        """Detect nested projects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Root project
            (Path(tmpdir) / "pyproject.toml").write_text("[project]")
            # Nested project
            subdir = Path(tmpdir) / "backend"
            subdir.mkdir()
            (subdir / "pyproject.toml").write_text("[project]")

            roots = discover_workspace_project_roots(Path(tmpdir))
            assert len(roots) == 2

    def test_multiple_marker_types(self):
        """Detect projects with different markers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Python project
            python_dir = Path(tmpdir) / "python_app"
            python_dir.mkdir()
            (python_dir / "pyproject.toml").write_text("[project]")

            # JS project
            js_dir = Path(tmpdir) / "js_app"
            js_dir.mkdir()
            (js_dir / "package.json").write_text("{}")

            # Rust project
            rust_dir = Path(tmpdir) / "rust_app"
            rust_dir.mkdir()
            (rust_dir / "Cargo.toml").write_text("[package]")

            roots = discover_workspace_project_roots(Path(tmpdir))
            assert len(roots) == 3

    def test_respects_max_depth(self):
        """Respects max_depth parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create deep nesting
            deep_path = Path(tmpdir) / "a" / "b" / "c" / "d" / "e"
            deep_path.mkdir(parents=True)
            (deep_path / "pyproject.toml").write_text("[project]")

            # Default max_depth is 3
            roots = discover_workspace_project_roots(Path(tmpdir), max_depth=2)
            # Should not find the deeply nested project
            assert len(roots) == 0

    def test_skips_hidden_directories(self):
        """Skips hidden directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            hidden = Path(tmpdir) / ".hidden"
            hidden.mkdir()
            (hidden / "pyproject.toml").write_text("[project]")

            roots = discover_workspace_project_roots(Path(tmpdir))
            # Should not find project in hidden directory
            assert len(roots) == 0

    def test_skips_skip_dirs(self):
        """Skips directories in SKIP_DIRS."""
        with tempfile.TemporaryDirectory() as tmpdir:
            node_modules = Path(tmpdir) / "node_modules"
            node_modules.mkdir()
            (node_modules / "package.json").write_text("{}")

            roots = discover_workspace_project_roots(Path(tmpdir))
            assert len(roots) == 0


# =============================================================================
# Tests for project_root_score function
# =============================================================================


class TestProjectRootScore:
    """Tests for project_root_score function."""

    def test_returns_tuple(self):
        """Returns a tuple of 3 integers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Resolve to handle macOS /var -> /private/var symlink
            resolved = Path(tmpdir).resolve()
            score = project_root_score(resolved, resolved)
            assert isinstance(score, tuple)
            assert len(score) == 3

    def test_sage_dir_bonus(self):
        """sage directory adds score."""
        with tempfile.TemporaryDirectory() as tmpdir:
            resolved = Path(tmpdir).resolve()
            sage_dir = resolved / "sage"
            sage_dir.mkdir()

            score = project_root_score(resolved, resolved)
            assert score[0] >= 12

    def test_tests_sage_bonus(self):
        """tests/sage directory adds score."""
        with tempfile.TemporaryDirectory() as tmpdir:
            resolved = Path(tmpdir).resolve()
            tests_sage = resolved / "tests" / "sage"
            tests_sage.mkdir(parents=True)

            score = project_root_score(resolved, resolved)
            assert score[0] >= 10

    def test_backend_frontend_bonus(self):
        """backend and frontend directories add score."""
        with tempfile.TemporaryDirectory() as tmpdir:
            resolved = Path(tmpdir).resolve()
            (resolved / "backend").mkdir()
            (resolved / "frontend").mkdir()

            score = project_root_score(resolved, resolved)
            assert score[0] >= 8

    def test_tests_dir_bonus(self):
        """tests directory adds score."""
        with tempfile.TemporaryDirectory() as tmpdir:
            resolved = Path(tmpdir).resolve()
            (resolved / "tests").mkdir()

            score = project_root_score(resolved, resolved)
            assert score[0] >= 3

    def test_pyproject_bonus(self):
        """pyproject.toml adds score."""
        with tempfile.TemporaryDirectory() as tmpdir:
            resolved = Path(tmpdir).resolve()
            (resolved / "pyproject.toml").write_text("[project]")

            score = project_root_score(resolved, resolved)
            assert score[0] >= 4

    def test_package_json_bonus(self):
        """package.json adds score."""
        with tempfile.TemporaryDirectory() as tmpdir:
            resolved = Path(tmpdir).resolve()
            (resolved / "package.json").write_text("{}")

            score = project_root_score(resolved, resolved)
            assert score[0] >= 2


# =============================================================================
# Tests for default_project_root function
# =============================================================================


class TestDefaultProjectRoot:
    """Tests for default_project_root function."""

    def test_returns_cwd_when_no_markers(self):
        """Returns cwd when no project markers found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = default_project_root(Path(tmpdir))
            assert result == Path(tmpdir).resolve()

    def test_finds_single_project(self):
        """Finds single project root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "pyproject.toml").write_text("[project]")
            result = default_project_root(Path(tmpdir))
            assert result == Path(tmpdir).resolve()

    def test_picks_best_scored_project(self):
        """Picks the best scored project root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create two projects
            proj1 = Path(tmpdir) / "proj1"
            proj1.mkdir()
            (proj1 / "pyproject.toml").write_text("[project]")

            proj2 = Path(tmpdir) / "proj2"
            proj2.mkdir()
            (proj2 / "pyproject.toml").write_text("[project]")
            (proj2 / "tests").mkdir()  # Higher score

            result = default_project_root(Path(tmpdir))
            # proj2 should win due to tests directory
            assert "proj2" in str(result)


# =============================================================================
# Tests for discover_npm_script function
# =============================================================================


class TestDiscoverNpmScript:
    """Tests for discover_npm_script function."""

    def test_no_package_json(self):
        """Returns None when no package.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = discover_npm_script(Path(tmpdir), "test")
            assert result is None

    def test_finds_test_script(self):
        """Finds test script in package.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"test": "jest"}}'
            )
            result = discover_npm_script(Path(tmpdir), "test")
            assert result == "jest"

    def test_no_scripts_section(self):
        """Returns None when no scripts section."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text('{"name": "test"}')
            result = discover_npm_script(Path(tmpdir), "test")
            assert result is None

    def test_script_not_found(self):
        """Returns None when script not found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"build": "webpack"}}'
            )
            result = discover_npm_script(Path(tmpdir), "test")
            assert result is None

    def test_skip_no_test_specified(self):
        """Skips 'no test specified' error script."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"test": "echo \\"Error: no test specified\\" && exit 1"}}'
            )
            result = discover_npm_script(Path(tmpdir), "test")
            assert result is None

    def test_invalid_json(self):
        """Returns None for invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text("invalid json")
            result = discover_npm_script(Path(tmpdir), "test")
            assert result is None

    def test_non_string_script(self):
        """Returns None for non-string script value."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"test": 123}}'
            )
            result = discover_npm_script(Path(tmpdir), "test")
            assert result is None


# =============================================================================
# Tests for discover_python_test_command function
# =============================================================================


class TestDiscoverPythonTestCommand:
    """Tests for discover_python_test_command function."""

    def test_no_test_suite(self):
        """Returns None when no test suite detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = discover_python_test_command(Path(tmpdir))
            assert result is None

    def test_with_tests_directory(self):
        """Returns pytest command with tests directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "tests").mkdir()
            result = discover_python_test_command(Path(tmpdir))
            assert result is not None
            assert "pytest" in result

    def test_with_pytest_ini(self):
        """Returns pytest command with pytest.ini."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "pytest.ini").write_text("[pytest]")
            result = discover_python_test_command(Path(tmpdir))
            assert result is not None
            assert "pytest" in result

    def test_full_suite(self):
        """Returns full suite command when requested."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "tests").mkdir()
            result = discover_python_test_command(Path(tmpdir), full_suite=True)
            assert result == "python -m pytest -v --tb=short"

    def test_prefer_sage_subset(self):
        """Prefers sage subset when appropriate."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "sage").mkdir()
            (Path(tmpdir) / "tests" / "sage").mkdir(parents=True)
            result = discover_python_test_command(
                Path(tmpdir), prefer_sage_subset=True
            )
            assert "tests/sage" in result


# =============================================================================
# Tests for discover_project_test_command function
# =============================================================================


class TestDiscoverProjectTestCommand:
    """Tests for discover_project_test_command function."""

    def test_npm_vitest(self):
        """Detects Vitest and adds --run flag."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"test": "vitest"}}'
            )
            result = discover_project_test_command(Path(tmpdir))
            assert result == "npm test -- --run"

    def test_npm_jest(self):
        """Detects Jest and adds --runInBand flag."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"test": "jest"}}'
            )
            result = discover_project_test_command(Path(tmpdir))
            assert result == "npm test -- --runInBand"

    def test_npm_react_scripts(self):
        """Detects react-scripts test."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"test": "react-scripts test"}}'
            )
            result = discover_project_test_command(Path(tmpdir))
            assert "CI=1" in result
            assert "--watch=false" in result

    def test_npm_generic(self):
        """Falls back to npm test for other test scripts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"test": "mocha"}}'
            )
            result = discover_project_test_command(Path(tmpdir))
            assert result == "npm test"

    def test_python_fallback(self):
        """Falls back to Python test command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "tests").mkdir()
            result = discover_project_test_command(Path(tmpdir))
            assert "pytest" in result

    def test_cargo_test(self):
        """Detects Rust Cargo project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Cargo.toml").write_text("[package]")
            result = discover_project_test_command(Path(tmpdir))
            assert result == "cargo test"

    def test_go_test(self):
        """Detects Go project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "go.mod").write_text("module test")
            result = discover_project_test_command(Path(tmpdir))
            assert result == "go test ./..."

    def test_no_test_command(self):
        """Returns None when no test command found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = discover_project_test_command(Path(tmpdir))
            assert result is None


# =============================================================================
# Tests for discover_project_full_test_command function
# =============================================================================


class TestDiscoverProjectFullTestCommand:
    """Tests for discover_project_full_test_command function."""

    def test_npm_vitest(self):
        """Detects Vitest for full test."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"test": "vitest"}}'
            )
            result = discover_project_full_test_command(Path(tmpdir))
            assert result == "npm test -- --run"

    def test_python_full_suite(self):
        """Returns full Python test suite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "tests").mkdir()
            result = discover_project_full_test_command(Path(tmpdir))
            assert "pytest" in result
            assert "-v" in result

    def test_cargo_test(self):
        """Detects Rust Cargo for full test."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Cargo.toml").write_text("[package]")
            result = discover_project_full_test_command(Path(tmpdir))
            assert result == "cargo test"

    def test_go_test(self):
        """Detects Go for full test."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "go.mod").write_text("module test")
            result = discover_project_full_test_command(Path(tmpdir))
            assert result == "go test ./..."


# =============================================================================
# Tests for discover_project_root_for_file function
# =============================================================================


class TestDiscoverProjectRootForFile:
    """Tests for discover_project_root_for_file function."""

    def test_returns_cwd_for_empty(self):
        """Returns cwd when no project markers found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = discover_project_root_for_file("main.py", Path(tmpdir))
            assert result == Path(tmpdir).resolve()

    def test_finds_project_root_for_file(self):
        """Finds project root containing the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "src"
            src.mkdir()
            (src / "main.py").write_text("code")
            (Path(tmpdir) / "pyproject.toml").write_text("[project]")

            result = discover_project_root_for_file("src/main.py", Path(tmpdir))
            assert result == Path(tmpdir).resolve()

    def test_finds_nested_project_root(self):
        """Finds nested project root for file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = Path(tmpdir) / "backend"
            backend.mkdir()
            (backend / "pyproject.toml").write_text("[project]")
            (backend / "main.py").write_text("code")

            result = discover_project_root_for_file("backend/main.py", Path(tmpdir))
            assert result == backend.resolve()

    def test_handles_invalid_path(self):
        """Handles invalid file paths gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = discover_project_root_for_file("", Path(tmpdir))
            # Should return cwd for invalid paths
            assert result == Path(tmpdir).resolve()


# =============================================================================
# Tests for command_from_project_root function
# =============================================================================


class TestCommandFromProjectRoot:
    """Tests for command_from_project_root function."""

    def test_same_directory(self):
        """No prefix when same directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = command_from_project_root(
                Path(tmpdir), "pytest", Path(tmpdir)
            )
            assert result == "pytest"

    def test_nested_directory(self):
        """Adds cwd prefix for nested directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = Path(tmpdir) / "backend"
            backend.mkdir()

            result = command_from_project_root(backend, "pytest", Path(tmpdir))
            assert "[cwd=backend]" in result
            assert "pytest" in result

    def test_deeper_nesting(self):
        """Handles deeper nesting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            deep = Path(tmpdir) / "apps" / "backend"
            deep.mkdir(parents=True)

            result = command_from_project_root(deep, "pytest", Path(tmpdir))
            assert "[cwd=apps/backend]" in result


# =============================================================================
# Tests for validation_command_for_written_files function
# =============================================================================


class TestValidationCommandForWrittenFiles:
    """Tests for validation_command_for_written_files function."""

    def test_empty_files_default_command(self):
        """Returns default command for empty file list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "tests").mkdir()
            result = validation_command_for_written_files([], Path(tmpdir))
            # Should return project test command
            assert result is not None
            assert "pytest" in result

    def test_empty_files_no_project(self):
        """Returns None when no project and no files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = validation_command_for_written_files([], Path(tmpdir))
            assert result is None

    def test_test_files_specific_command(self):
        """Returns specific pytest command for test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tests = Path(tmpdir) / "tests"
            tests.mkdir()
            (tests / "test_main.py").write_text("def test_x(): pass")

            result = validation_command_for_written_files(
                ["tests/test_main.py"], Path(tmpdir)
            )
            assert result is not None
            assert "pytest" in result
            assert "test_main.py" in result

    def test_python_files_project_command(self):
        """Returns project test command for Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "tests").mkdir()
            (Path(tmpdir) / "main.py").write_text("code")

            result = validation_command_for_written_files(
                ["main.py"], Path(tmpdir)
            )
            assert result is not None
            assert "pytest" in result

    def test_js_files_npm_command(self):
        """Returns npm test command for JS files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "package.json").write_text(
                '{"scripts": {"test": "jest"}}'
            )
            (Path(tmpdir) / "app.js").write_text("code")

            result = validation_command_for_written_files(
                ["app.js"], Path(tmpdir)
            )
            assert result is not None
            assert "npm" in result

    def test_shell_quote_func(self):
        """Uses shell_quote_func when provided."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tests = Path(tmpdir) / "tests"
            tests.mkdir()
            (tests / "test_main.py").write_text("def test_x(): pass")

            def custom_quote(s):
                return f'"{s}"'

            result = validation_command_for_written_files(
                ["tests/test_main.py"],
                Path(tmpdir),
                shell_quote_func=custom_quote,
            )
            assert result is not None
            assert '"' in result

    def test_multiple_files_same_project(self):
        """Handles multiple files from same project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "tests").mkdir()
            (Path(tmpdir) / "main.py").write_text("code")
            (Path(tmpdir) / "utils.py").write_text("code")

            result = validation_command_for_written_files(
                ["main.py", "utils.py"], Path(tmpdir)
            )
            assert result is not None


# =============================================================================
# Integration tests
# =============================================================================


class TestProjectIntegration:
    """Integration tests for project module."""

    def test_full_python_project_workflow(self):
        """Full workflow for Python project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create Python project structure
            (Path(tmpdir) / "pyproject.toml").write_text(
                '[project]\nname = "test-project"'
            )
            (Path(tmpdir) / "tests").mkdir()
            (Path(tmpdir) / "tests" / "test_main.py").write_text(
                "def test_example(): pass"
            )
            (Path(tmpdir) / "src").mkdir()
            (Path(tmpdir) / "src" / "main.py").write_text("def main(): pass")

            # Test project discovery
            roots = discover_workspace_project_roots(Path(tmpdir))
            assert len(roots) == 1

            # Test project scoring
            score = project_root_score(roots[0], Path(tmpdir))
            assert score[0] > 0

            # Test command discovery
            cmd = discover_project_test_command(roots[0])
            assert "pytest" in cmd

    def test_full_js_project_workflow(self):
        """Full workflow for JavaScript project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create JS project structure
            (Path(tmpdir) / "package.json").write_text(
                '{"name": "test", "scripts": {"test": "jest"}}'
            )
            (Path(tmpdir) / "src").mkdir()
            (Path(tmpdir) / "src" / "index.js").write_text("export default {}")

            # Test project discovery
            roots = discover_workspace_project_roots(Path(tmpdir))
            assert len(roots) == 1

            # Test npm script discovery
            script = discover_npm_script(roots[0], "test")
            assert script == "jest"

            # Test command discovery
            cmd = discover_project_test_command(roots[0])
            assert "npm test" in cmd

    def test_monorepo_workflow(self):
        """Full workflow for monorepo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create monorepo structure
            backend = Path(tmpdir) / "backend"
            frontend = Path(tmpdir) / "frontend"
            backend.mkdir()
            frontend.mkdir()

            (backend / "pyproject.toml").write_text("[project]")
            (backend / "tests").mkdir()
            (frontend / "package.json").write_text(
                '{"scripts": {"test": "vitest"}}'
            )

            # Test discovery
            roots = discover_workspace_project_roots(Path(tmpdir))
            assert len(roots) == 2

    def test_detect_files_integration(self):
        """Test file detection integration."""
        files = [
            "tests/test_main.py",
            "tests/test_utils.py",
            "src/main.py",
            "src/utils.py",
            "config.json",
        ]

        test_files = detect_test_files(files)
        assert len(test_files) == 2

        runnable = detect_runnable_files(files)
        assert len(runnable) == 4

    def test_backward_compat_aliases(self):
        """Test backward compatibility aliases exist."""
        from sage.core.project import (
            _detect_test_files,
            _detect_runnable_files,
            _discover_workspace_project_roots,
            _project_root_score,
            _default_project_root,
            _discover_npm_script,
            _discover_python_test_command,
            _discover_project_test_command,
            _discover_project_full_test_command,
            _discover_project_root_for_file,
            _command_from_project_root,
            _validation_command_for_written_files,
        )

        # All should be callable
        assert callable(_detect_test_files)
        assert callable(_detect_runnable_files)
        assert callable(_discover_workspace_project_roots)
        assert callable(_project_root_score)
        assert callable(_default_project_root)
        assert callable(_discover_npm_script)
        assert callable(_discover_python_test_command)
        assert callable(_discover_project_test_command)
        assert callable(_discover_project_full_test_command)
        assert callable(_discover_project_root_for_file)
        assert callable(_command_from_project_root)
        assert callable(_validation_command_for_written_files)
