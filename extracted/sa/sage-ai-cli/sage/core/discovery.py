"""File discovery tool for SAGE autopolit.

P0-4: Add real file-discovery tool instead of overloading SEARCH.

This module provides proper file discovery that:
1. Discovers project structure without relying on model execution
2. Returns structured data, not just file paths
3. Handles monorepo/nested project structures
4. Caches results for performance
"""

from __future__ import annotations

import fnmatch
import time
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DiscoveryResult:
    """Result from file discovery operation."""

    files: list[Path] = field(default_factory=list)
    directories: list[Path] = field(default_factory=list)
    total_files: int = 0
    total_directories: int = 0
    languages: dict[str, int] = field(default_factory=dict)
    test_files: list[Path] = field(default_factory=list)
    config_files: list[Path] = field(default_factory=list)
    modules: set[str] = field(default_factory=set)
    packages: set[str] = field(default_factory=set)
    elapsed_ms: float = 0.0


@dataclass
class ProjectInfo:
    """Information about a discovered project."""

    root: Path
    name: str
    type: str  # python, node, rust, go, etc.
    test_framework: str | None = None
    test_command: str | None = None
    has_tests: bool = False
    entry_points: list[Path] = field(default_factory=list)


# Language detection by extension
LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "react",
    ".tsx": "react-ts",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".kt": "kotlin",
    ".rb": "ruby",
    ".php": "php",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c-header",
    ".hpp": "cpp-header",
    ".cs": "csharp",
    ".swift": "swift",
    ".lua": "lua",
    ".r": "r",
    ".R": "r",
    ".sql": "sql",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".ps1": "powershell",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".toml": "toml",
    ".xml": "xml",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".sass": "sass",
    ".less": "less",
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# Directories to always skip
IGNORED_DIRECTORIES = {
    ".git",
    ".svn",
    ".hg",
    ".bzr",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "bower_components",
    "venv",
    ".venv",
    "env",
    ".env",
    "virtualenv",
    ".tox",
    ".nox",
    "dist",
    "build",
    "target",
    "out",
    ".eggs",
    "*.egg-info",
    ".idea",
    ".vscode",
    ".vs",
    ".sage",
    ".claude",
    "coverage",
    "htmlcov",
    ".coverage",
}

# Test file patterns
TEST_PATTERNS = [
    "test_*.py",
    "*_test.py",
    "tests.py",
    "*.test.js",
    "*.test.ts",
    "*.spec.js",
    "*.spec.ts",
    "*_test.go",
    "test_*.go",
    "*_test.rs",
    "*_spec.rb",
]

# Config file patterns
CONFIG_PATTERNS = [
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "requirements*.txt",
    "package.json",
    "tsconfig.json",
    "Cargo.toml",
    "go.mod",
    "Gemfile",
    "Makefile",
    "CMakeLists.txt",
    ".env*",
    "config.*",
]


class FileDiscovery:
    """Fast, cached file discovery for SAGE.

    Unlike SEARCH: which relies on model execution, this tool:
    - Runs instantly without model inference
    - Returns structured data
    - Properly handles all languages
    - Caches results with TTL
    """

    def __init__(self, cwd: Path, cache_ttl: float = 30.0):
        self.cwd = cwd.resolve()
        self.cache_ttl = cache_ttl
        self._cache: dict[str, tuple[float, DiscoveryResult]] = {}

    def discover(
        self,
        pattern: str = "*",
        max_depth: int = 10,
        include_hidden: bool = False,
        extensions: list[str] | None = None,
    ) -> DiscoveryResult:
        """Discover files matching pattern.

        Args:
            pattern: Glob pattern to match (e.g., "*.py", "**/*.ts")
            max_depth: Maximum directory depth to traverse
            include_hidden: Include hidden files/directories
            extensions: Filter by file extensions (e.g., [".py", ".js"])

        Returns:
            DiscoveryResult with found files and metadata
        """
        cache_key = f"{pattern}:{max_depth}:{include_hidden}:{extensions}"
        now = time.time()

        # Check cache
        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if now - cached_time < self.cache_ttl:
                return cached_result

        start_time = time.perf_counter()
        result = DiscoveryResult()

        # Walk directory tree
        for item in self._walk(pattern, max_depth, include_hidden, extensions):
            if item.is_file():
                result.files.append(item)
                result.total_files += 1

                # Track language
                ext = item.suffix.lower()
                if ext in LANGUAGE_EXTENSIONS:
                    lang = LANGUAGE_EXTENSIONS[ext]
                    result.languages[lang] = result.languages.get(lang, 0) + 1

                # Track test files
                if self._is_test_file(item):
                    result.test_files.append(item)

                # Track config files
                if self._is_config_file(item):
                    result.config_files.append(item)

                # Track Python modules and packages
                if ext == ".py":
                    self._track_python_module(item, result)

            elif item.is_dir():
                result.directories.append(item)
                result.total_directories += 1

        result.elapsed_ms = (time.perf_counter() - start_time) * 1000

        # Cache result
        self._cache[cache_key] = (now, result)

        return result

    def discover_modules(self) -> set[str]:
        """Discover all Python modules in the project.

        Returns:
            Set of importable module names
        """
        result = self.discover("**/*.py", max_depth=10)
        return result.modules | result.packages

    def discover_projects(self) -> list[ProjectInfo]:
        """Discover all projects/subprojects in the repository.

        Handles monorepos by detecting:
        - pyproject.toml / setup.py for Python
        - package.json for Node.js
        - Cargo.toml for Rust
        - go.mod for Go
        """
        projects: list[ProjectInfo] = []
        result = self.discover("*", max_depth=5)

        # Check root first
        root_project = self._detect_project(self.cwd)
        if root_project:
            projects.append(root_project)

        # Check subdirectories
        for d in result.directories:
            sub_project = self._detect_project(d)
            if sub_project:
                projects.append(sub_project)

        return projects

    def get_test_command(self) -> str | None:
        """Detect the best test command for this project."""
        projects = self.discover_projects()
        if not projects:
            return None

        # Use root project's test command
        for project in projects:
            if project.root == self.cwd and project.test_command:
                return project.test_command

        # Fall back to first project with tests
        for project in projects:
            if project.test_command:
                return project.test_command

        return None

    def _walk(
        self,
        pattern: str,
        max_depth: int,
        include_hidden: bool,
        extensions: list[str] | None,
    ) -> Iterator[Path]:
        """Walk directory tree yielding matching paths."""

        def should_skip_dir(name: str) -> bool:
            if name in IGNORED_DIRECTORIES:
                return True
            if not include_hidden and name.startswith("."):
                return True
            return False

        def matches_pattern(path: Path) -> bool:
            if extensions and path.suffix.lower() not in extensions:
                return False
            return fnmatch.fnmatch(path.name, pattern) or fnmatch.fnmatch(str(path), pattern)

        def walk_recursive(directory: Path, depth: int):
            if depth > max_depth:
                return

            try:
                for entry in sorted(directory.iterdir()):
                    if entry.is_dir():
                        if should_skip_dir(entry.name):
                            continue
                        yield entry
                        yield from walk_recursive(entry, depth + 1)
                    elif entry.is_file():
                        if matches_pattern(entry):
                            yield entry
            except PermissionError:
                pass
            except OSError:
                pass

        yield from walk_recursive(self.cwd, 0)

    def _is_test_file(self, path: Path) -> bool:
        """Check if path is a test file."""
        name = path.name
        for pattern in TEST_PATTERNS:
            if fnmatch.fnmatch(name, pattern):
                return True
        return False

    def _is_config_file(self, path: Path) -> bool:
        """Check if path is a config file."""
        name = path.name
        for pattern in CONFIG_PATTERNS:
            if fnmatch.fnmatch(name, pattern):
                return True
        return False

    def _track_python_module(self, path: Path, result: DiscoveryResult) -> None:
        """Track Python module and package names."""
        # Module name from filename
        if path.name != "__init__.py":
            result.modules.add(path.stem)

        # Package name from directory containing __init__.py
        if path.name == "__init__.py":
            result.packages.add(path.parent.name)

        # Top-level package
        try:
            rel = path.relative_to(self.cwd)
            if len(rel.parts) > 1:
                result.packages.add(rel.parts[0])
        except ValueError:
            pass

    def _detect_project(self, directory: Path) -> ProjectInfo | None:
        """Detect project type from directory."""
        # Python
        if (directory / "pyproject.toml").exists():
            return self._detect_python_project(directory, "pyproject.toml")
        if (directory / "setup.py").exists():
            return self._detect_python_project(directory, "setup.py")

        # Node.js
        if (directory / "package.json").exists():
            return self._detect_node_project(directory)

        # Rust
        if (directory / "Cargo.toml").exists():
            return ProjectInfo(
                root=directory,
                name=directory.name,
                type="rust",
                test_command="cargo test",
                has_tests=(directory / "tests").is_dir(),
            )

        # Go
        if (directory / "go.mod").exists():
            return ProjectInfo(
                root=directory,
                name=directory.name,
                type="go",
                test_command="go test ./...",
                has_tests=any(directory.glob("*_test.go")),
            )

        # Java / Kotlin (Maven)
        if (directory / "pom.xml").exists():
            return ProjectInfo(
                root=directory,
                name=directory.name,
                type="java",
                test_command="mvn test",
                has_tests=(directory / "src" / "test").is_dir(),
            )

        # Java / Kotlin (Gradle)
        if (directory / "build.gradle").exists() or (directory / "build.gradle.kts").exists():
            is_kotlin = (directory / "build.gradle.kts").exists() or any(directory.glob("src/main/kotlin/**/*.kt"))
            return ProjectInfo(
                root=directory,
                name=directory.name,
                type="kotlin" if is_kotlin else "java",
                test_command="./gradlew test",
                has_tests=(directory / "src" / "test").is_dir(),
            )

        # Ruby
        if (directory / "Gemfile").exists():
            has_rspec = (directory / "spec").is_dir()
            return ProjectInfo(
                root=directory,
                name=directory.name,
                type="ruby",
                test_command="bundle exec rspec" if has_rspec else "bundle exec rake test",
                has_tests=has_rspec or (directory / "test").is_dir(),
            )

        # Swift
        if (directory / "Package.swift").exists():
            return ProjectInfo(
                root=directory,
                name=directory.name,
                type="swift",
                test_command="swift test",
                has_tests=(directory / "Tests").is_dir(),
            )

        # Dart / Flutter
        if (directory / "pubspec.yaml").exists():
            has_flutter = False
            try:
                content = (directory / "pubspec.yaml").read_text(encoding="utf-8", errors="replace")
                if "sdk: flutter" in content or "flutter:" in content:
                    has_flutter = True
            except Exception:
                pass
            return ProjectInfo(
                root=directory,
                name=directory.name,
                type="dart",
                test_command="flutter test" if has_flutter else "dart test",
                has_tests=(directory / "test").is_dir(),
            )

        # C++
        if (directory / "CMakeLists.txt").exists():
            return ProjectInfo(
                root=directory,
                name=directory.name,
                type="cpp",
                test_command="ctest",
                has_tests=True,
            )

        # C#
        csharp_files = list(directory.glob("*.csproj")) + list(directory.glob("*.sln"))
        if csharp_files:
            return ProjectInfo(
                root=directory,
                name=directory.name,
                type="csharp",
                test_command="dotnet test",
                has_tests=True,
            )

        return None

    def _detect_python_project(self, directory: Path, config_file: str) -> ProjectInfo:
        """Detect Python project details."""
        has_tests = (
            (directory / "tests").is_dir()
            or (directory / "test").is_dir()
            or any(directory.glob("test_*.py"))
        )

        # Detect test framework
        test_framework = None
        test_command = None

        if has_tests:
            # Check for pytest
            pyproject = directory / "pyproject.toml"
            if pyproject.exists():
                content = pyproject.read_text(encoding="utf-8", errors="replace")
                if "pytest" in content:
                    test_framework = "pytest"
                    test_command = "python -m pytest -v --tb=short"

            if not test_framework:
                # Default to pytest
                test_framework = "pytest"
                test_command = "python -m pytest -v --tb=short"

        return ProjectInfo(
            root=directory,
            name=directory.name,
            type="python",
            test_framework=test_framework,
            test_command=test_command,
            has_tests=has_tests,
        )

    def _detect_node_project(self, directory: Path) -> ProjectInfo:
        """Detect Node.js project details."""
        import json

        test_command = None
        has_tests = False

        try:
            pkg_json = directory / "package.json"
            if pkg_json.exists():
                pkg = json.loads(pkg_json.read_text(encoding="utf-8", errors="replace"))
                scripts = pkg.get("scripts", {})

                if "test" in scripts:
                    test_command = "npm test"
                    has_tests = True
                elif "vitest" in str(pkg.get("devDependencies", {})):
                    test_command = "npx vitest"
                    has_tests = True
                elif "jest" in str(pkg.get("devDependencies", {})):
                    test_command = "npx jest"
                    has_tests = True

        except (json.JSONDecodeError, OSError):
            pass

        return ProjectInfo(
            root=directory,
            name=directory.name,
            type="node",
            test_command=test_command,
            has_tests=has_tests,
        )

    def clear_cache(self) -> None:
        """Clear the discovery cache."""
        self._cache.clear()


def discover_files(cwd: Path, pattern: str = "*") -> DiscoveryResult:
    """Convenience function for file discovery.

    Args:
        cwd: Working directory
        pattern: Glob pattern to match

    Returns:
        DiscoveryResult with found files
    """
    discovery = FileDiscovery(cwd)
    return discovery.discover(pattern)


def discover_modules(cwd: Path) -> set[str]:
    """Convenience function to discover Python modules.

    Args:
        cwd: Working directory

    Returns:
        Set of importable module names
    """
    discovery = FileDiscovery(cwd)
    return discovery.discover_modules()
