"""Tests for sage.core.discovery module."""

import shutil
import tempfile
from pathlib import Path

import pytest

from sage.core.discovery import (
    CONFIG_PATTERNS,
    IGNORED_DIRECTORIES,
    LANGUAGE_EXTENSIONS,
    TEST_PATTERNS,
    DiscoveryResult,
    FileDiscovery,
    discover_files,
    discover_modules,
)


class TestFileDiscovery:
    """Test FileDiscovery class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        # Create a sample project structure
        (self.temp_dir / "src").mkdir()
        (self.temp_dir / "src" / "__init__.py").write_text("")
        (self.temp_dir / "src" / "main.py").write_text("def main(): pass")
        (self.temp_dir / "src" / "utils.py").write_text("def helper(): pass")
        (self.temp_dir / "tests").mkdir()
        (self.temp_dir / "tests" / "__init__.py").write_text("")
        (self.temp_dir / "tests" / "test_main.py").write_text("def test_main(): pass")
        (self.temp_dir / "pyproject.toml").write_text('[project]\nname = "test"')

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_discover_all_files(self):
        """Test discovering all files in a directory."""
        discovery = FileDiscovery(self.temp_dir)
        result = discovery.discover("*")
        assert result.total_files >= 4  # At least 4 Python files + toml
        assert result.total_directories >= 2  # src and tests

    def test_discover_python_files(self):
        """Test discovering only Python files."""
        discovery = FileDiscovery(self.temp_dir)
        result = discovery.discover("*.py")
        assert all(f.suffix == ".py" for f in result.files)
        assert result.total_files >= 4

    def test_discover_with_extensions_filter(self):
        """Test filtering by extensions."""
        discovery = FileDiscovery(self.temp_dir)
        result = discovery.discover("*", extensions=[".py"])
        assert all(f.suffix == ".py" for f in result.files)

    def test_discover_modules(self):
        """Test module discovery."""
        discovery = FileDiscovery(self.temp_dir)
        modules = discovery.discover_modules()
        assert "main" in modules
        assert "utils" in modules
        assert "src" in modules  # Package

    def test_test_file_detection(self):
        """Test that test files are correctly identified."""
        discovery = FileDiscovery(self.temp_dir)
        result = discovery.discover("*.py")
        test_file_names = [f.name for f in result.test_files]
        assert "test_main.py" in test_file_names

    def test_config_file_detection(self):
        """Test that config files are correctly identified."""
        discovery = FileDiscovery(self.temp_dir)
        result = discovery.discover("*")
        config_file_names = [f.name for f in result.config_files]
        assert "pyproject.toml" in config_file_names

    def test_language_detection(self):
        """Test that languages are correctly detected."""
        discovery = FileDiscovery(self.temp_dir)
        result = discovery.discover("*")
        assert "python" in result.languages
        assert result.languages["python"] >= 4

    def test_caching(self):
        """Test that results are cached."""
        discovery = FileDiscovery(self.temp_dir, cache_ttl=10.0)
        result1 = discovery.discover("*.py")
        result2 = discovery.discover("*.py")
        # Second call should be faster (cached)
        assert result1.total_files == result2.total_files

    def test_clear_cache(self):
        """Test clearing the cache."""
        discovery = FileDiscovery(self.temp_dir)
        discovery.discover("*.py")
        assert len(discovery._cache) > 0
        discovery.clear_cache()
        assert len(discovery._cache) == 0

    def test_ignored_directories(self):
        """Test that ignored directories are skipped."""
        # Create an ignored directory
        (self.temp_dir / ".git").mkdir()
        (self.temp_dir / ".git" / "config").write_text("ignored")
        (self.temp_dir / "__pycache__").mkdir()
        (self.temp_dir / "__pycache__" / "cache.pyc").write_text("ignored")

        discovery = FileDiscovery(self.temp_dir)
        result = discovery.discover("*")

        # Check that ignored directories are not in results
        dir_names = [d.name for d in result.directories]
        assert ".git" not in dir_names
        assert "__pycache__" not in dir_names


class TestProjectDetection:
    """Test project detection functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_detect_python_project(self):
        """Test detecting a Python project."""
        (self.temp_dir / "pyproject.toml").write_text('[project]\nname = "test"')
        (self.temp_dir / "tests").mkdir()
        (self.temp_dir / "tests" / "test_foo.py").write_text("def test_foo(): pass")

        discovery = FileDiscovery(self.temp_dir)
        projects = discovery.discover_projects()

        assert len(projects) >= 1
        assert projects[0].type == "python"
        assert projects[0].has_tests is True

    def test_detect_node_project(self):
        """Test detecting a Node.js project."""
        pkg_json = {"name": "test", "scripts": {"test": "jest"}}
        import json

        (self.temp_dir / "package.json").write_text(json.dumps(pkg_json))

        discovery = FileDiscovery(self.temp_dir)
        projects = discovery.discover_projects()

        assert len(projects) >= 1
        assert projects[0].type == "node"
        assert projects[0].test_command == "npm test"

    def test_detect_rust_project(self):
        """Test detecting a Rust project."""
        (self.temp_dir / "Cargo.toml").write_text('[package]\nname = "test"')

        discovery = FileDiscovery(self.temp_dir)
        projects = discovery.discover_projects()

        assert len(projects) >= 1
        assert projects[0].type == "rust"
        assert projects[0].test_command == "cargo test"

    def test_detect_go_project(self):
        """Test detecting a Go project."""
        (self.temp_dir / "go.mod").write_text("module test")

        discovery = FileDiscovery(self.temp_dir)
        projects = discovery.discover_projects()

        assert len(projects) >= 1
        assert projects[0].type == "go"
        assert projects[0].test_command == "go test ./..."

    def test_get_test_command(self):
        """Test getting the test command."""
        (self.temp_dir / "pyproject.toml").write_text("[tool.pytest]\n")
        (self.temp_dir / "tests").mkdir()

        discovery = FileDiscovery(self.temp_dir)
        test_cmd = discovery.get_test_command()

        assert test_cmd is not None
        assert "pytest" in test_cmd


class TestConvenienceFunctions:
    """Test convenience functions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        (self.temp_dir / "module.py").write_text("x = 1")
        (self.temp_dir / "other.py").write_text("y = 2")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_discover_files_function(self):
        """Test the discover_files convenience function."""
        result = discover_files(self.temp_dir, "*.py")
        assert isinstance(result, DiscoveryResult)
        assert result.total_files == 2

    def test_discover_modules_function(self):
        """Test the discover_modules convenience function."""
        modules = discover_modules(self.temp_dir)
        assert "module" in modules
        assert "other" in modules


class TestConstants:
    """Test module constants."""

    def test_language_extensions(self):
        """Test that common language extensions are defined."""
        assert ".py" in LANGUAGE_EXTENSIONS
        assert ".js" in LANGUAGE_EXTENSIONS
        assert ".ts" in LANGUAGE_EXTENSIONS
        assert ".go" in LANGUAGE_EXTENSIONS
        assert ".rs" in LANGUAGE_EXTENSIONS

    def test_ignored_directories(self):
        """Test that common ignored directories are defined."""
        assert ".git" in IGNORED_DIRECTORIES
        assert "__pycache__" in IGNORED_DIRECTORIES
        assert "node_modules" in IGNORED_DIRECTORIES
        assert ".venv" in IGNORED_DIRECTORIES

    def test_test_patterns(self):
        """Test that common test patterns are defined."""
        assert any("test_" in p for p in TEST_PATTERNS)
        assert any("_test" in p for p in TEST_PATTERNS)

    def test_config_patterns(self):
        """Test that common config patterns are defined."""
        assert any("pyproject.toml" in p for p in CONFIG_PATTERNS)
        assert any("package.json" in p for p in CONFIG_PATTERNS)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
