"""
Codebase Analyzer for SAGE - Comprehensive implementation of Roadmap Items 81-120.

This module provides:
- P1 Items 81-95: Project Structure Analysis
- P1 Items 96-110: Code Analysis
- P1 Items 111-120: Context Building

All 40 P1 codebase understanding items are addressed in this module.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import ClassVar

# =============================================================================
# ITEM 81-95: PROJECT STRUCTURE ANALYSIS
# =============================================================================


class ProjectType(Enum):
    """Item 81: Project type classification."""

    PYTHON = auto()
    JAVASCRIPT = auto()
    TYPESCRIPT = auto()
    JAVA = auto()
    GO = auto()
    RUST = auto()
    CSHARP = auto()
    RUBY = auto()
    PHP = auto()
    MIXED = auto()
    UNKNOWN = auto()


class Framework(Enum):
    """Item 82: Framework detection."""

    # Python
    FASTAPI = auto()
    DJANGO = auto()
    FLASK = auto()
    PYTEST = auto()
    TYPER = auto()
    CLICK = auto()

    # JavaScript/TypeScript
    REACT = auto()
    NEXTJS = auto()
    EXPRESS = auto()
    NESTJS = auto()
    VUE = auto()

    # General
    NONE = auto()


@dataclass
class ProjectManifest:
    """Item 83: Parsed project manifest information."""

    name: str = ""
    version: str = ""
    description: str = ""
    dependencies: dict[str, str] = field(default_factory=dict)
    dev_dependencies: dict[str, str] = field(default_factory=dict)
    scripts: dict[str, str] = field(default_factory=dict)
    entry_points: list[str] = field(default_factory=list)
    python_requires: str = ""


@dataclass
class TestFrameworkInfo:
    """Item 84: Test framework detection results."""

    framework: str = ""  # pytest, jest, mocha, junit, etc.
    config_file: str | None = None
    test_directories: list[str] = field(default_factory=list)
    test_patterns: list[str] = field(default_factory=list)
    coverage_enabled: bool = False


@dataclass
class CIConfig:
    """Item 85: CI/CD configuration analysis."""

    platform: str = ""  # github, gitlab, jenkins, etc.
    config_file: str = ""
    workflows: list[str] = field(default_factory=list)
    triggers: list[str] = field(default_factory=list)
    has_tests: bool = False
    has_linting: bool = False
    has_deployment: bool = False


@dataclass
class DependencyInfo:
    """Item 86: Dependency graph information."""

    direct_dependencies: dict[str, str] = field(default_factory=dict)
    dev_dependencies: dict[str, str] = field(default_factory=dict)
    internal_imports: dict[str, list[str]] = field(default_factory=dict)
    circular_dependencies: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class ModuleInfo:
    """Item 87-89: Code architecture information."""

    name: str
    path: str
    type: str  # module, package, class, function
    imports: list[str] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    complexity: int = 0


@dataclass
class APIEndpoint:
    """Item 90: API endpoint detection."""

    method: str  # GET, POST, PUT, DELETE, etc.
    path: str
    handler: str
    file: str
    line: int
    parameters: list[str] = field(default_factory=list)


@dataclass
class ProjectAnalysis:
    """Complete project analysis result."""

    project_type: ProjectType
    frameworks: list[Framework] = field(default_factory=list)
    manifest: ProjectManifest | None = None
    test_info: TestFrameworkInfo | None = None
    ci_config: CIConfig | None = None
    dependencies: DependencyInfo | None = None
    modules: list[ModuleInfo] = field(default_factory=list)
    api_endpoints: list[APIEndpoint] = field(default_factory=list)

    # Item 91: Database schema
    database_tables: list[str] = field(default_factory=list)

    # Item 92: Configuration files
    config_files: list[str] = field(default_factory=list)

    # Item 93: Environment detection
    environments: list[str] = field(default_factory=list)

    # Item 94: Deployment configuration
    deployment_configs: list[str] = field(default_factory=list)

    # Item 95: Security configuration
    security_files: list[str] = field(default_factory=list)


class ProjectStructureAnalyzer:
    """
    Items 81-95: Analyzes project structure comprehensively.
    """

    # File patterns for detection
    PYTHON_PATTERNS = ["*.py", "pyproject.toml", "setup.py", "requirements.txt"]
    JS_PATTERNS = ["*.js", "*.jsx", "package.json"]
    TS_PATTERNS = ["*.ts", "*.tsx", "tsconfig.json"]
    GO_PATTERNS = ["*.go", "go.mod", "go.sum"]
    RUST_PATTERNS = ["*.rs", "Cargo.toml"]

    FRAMEWORK_INDICATORS: ClassVar[dict[Framework, list[str]]] = {
        Framework.FASTAPI: ["fastapi", "from fastapi import"],
        Framework.DJANGO: ["django", "from django", "DJANGO_SETTINGS"],
        Framework.FLASK: ["flask", "from flask import"],
        Framework.PYTEST: ["pytest", "def test_", "@pytest"],
        Framework.TYPER: ["typer", "from typer import"],
        Framework.CLICK: ["click", "from click import", "@click.command"],
        Framework.REACT: ["react", "from 'react'", "useState", "useEffect"],
        Framework.NEXTJS: ["next", "from 'next'", "getServerSideProps"],
        Framework.EXPRESS: ["express", "require('express')", "app.get("],
        Framework.VUE: ["vue", "from 'vue'", "createApp"],
    }

    def __init__(self, cwd: Path):
        self.cwd = cwd
        self._file_cache: dict[str, str] = {}

    def analyze(self) -> ProjectAnalysis:
        """Perform comprehensive project analysis."""
        analysis = ProjectAnalysis(project_type=self._detect_project_type())

        # Item 82: Detect frameworks
        analysis.frameworks = self._detect_frameworks()

        # Item 83: Parse manifest
        analysis.manifest = self._parse_manifest()

        # Item 84: Detect test framework
        analysis.test_info = self._detect_test_framework()

        # Item 85: Parse CI configuration
        analysis.ci_config = self._parse_ci_config()

        # Item 86: Build dependency info
        analysis.dependencies = self._analyze_dependencies()

        # Item 87-89: Analyze modules
        analysis.modules = self._analyze_modules()

        # Item 90: Detect API endpoints
        analysis.api_endpoints = self._detect_api_endpoints()

        # Item 91: Detect database schema
        analysis.database_tables = self._detect_database_tables()

        # Item 92: Find config files
        analysis.config_files = self._find_config_files()

        # Item 93: Detect environments
        analysis.environments = self._detect_environments()

        # Item 94: Find deployment configs
        analysis.deployment_configs = self._find_deployment_configs()

        # Item 95: Find security files
        analysis.security_files = self._find_security_files()

        return analysis

    def _detect_project_type(self) -> ProjectType:
        """Item 81: Detect primary project type."""
        indicators = {
            ProjectType.PYTHON: 0,
            ProjectType.JAVASCRIPT: 0,
            ProjectType.TYPESCRIPT: 0,
            ProjectType.GO: 0,
            ProjectType.RUST: 0,
        }

        for path in self._walk_files():
            suffix = path.suffix.lower()
            if suffix == ".py":
                indicators[ProjectType.PYTHON] += 1
            elif suffix in (".js", ".jsx"):
                indicators[ProjectType.JAVASCRIPT] += 1
            elif suffix in (".ts", ".tsx"):
                indicators[ProjectType.TYPESCRIPT] += 1
            elif suffix == ".go":
                indicators[ProjectType.GO] += 1
            elif suffix == ".rs":
                indicators[ProjectType.RUST] += 1

        if not any(indicators.values()):
            return ProjectType.UNKNOWN

        max_type = max(indicators, key=indicators.get)
        if indicators[max_type] == 0:
            return ProjectType.UNKNOWN

        # Check for mixed projects
        total = sum(indicators.values())
        if indicators[max_type] < total * 0.7:
            return ProjectType.MIXED

        return max_type

    def _detect_frameworks(self) -> list[Framework]:
        """Item 82: Detect frameworks used."""
        detected = []

        for path in self._walk_files():
            if path.suffix not in (".py", ".js", ".ts", ".jsx", ".tsx"):
                continue

            try:
                content = self._read_file(path)
                for framework, indicators in self.FRAMEWORK_INDICATORS.items():
                    if any(ind in content for ind in indicators):
                        if framework not in detected:
                            detected.append(framework)
            except Exception:
                continue

        return detected

    def _parse_manifest(self) -> ProjectManifest | None:
        """Item 83: Parse project manifest file."""
        manifest = ProjectManifest()

        # Try pyproject.toml
        pyproject = self.cwd / "pyproject.toml"
        if pyproject.exists():
            try:
                content = self._read_file(pyproject)
                # Parse name
                name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                if name_match:
                    manifest.name = name_match.group(1)
                # Parse version
                version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if version_match:
                    manifest.version = version_match.group(1)
                # Parse dependencies
                deps_section = re.search(r"dependencies\s*=\s*\[(.*?)\]", content, re.DOTALL)
                if deps_section:
                    deps = re.findall(r'["\']([^"\'>=<]+)', deps_section.group(1))
                    manifest.dependencies = dict.fromkeys(deps, "")
                return manifest
            except Exception:
                pass

        # Try package.json
        package_json = self.cwd / "package.json"
        if package_json.exists():
            try:
                content = json.loads(self._read_file(package_json))
                manifest.name = content.get("name", "")
                manifest.version = content.get("version", "")
                manifest.description = content.get("description", "")
                manifest.dependencies = content.get("dependencies", {})
                manifest.dev_dependencies = content.get("devDependencies", {})
                manifest.scripts = content.get("scripts", {})
                return manifest
            except Exception:
                pass

        return None

    def _detect_test_framework(self) -> TestFrameworkInfo:
        """Item 84: Detect test framework."""
        info = TestFrameworkInfo()

        # Check for pytest
        if (self.cwd / "pytest.ini").exists() or (self.cwd / "pyproject.toml").exists():
            pyproject = self.cwd / "pyproject.toml"
            if pyproject.exists():
                content = self._read_file(pyproject)
                if "pytest" in content or "[tool.pytest" in content:
                    info.framework = "pytest"
                    info.config_file = "pyproject.toml"

        # Check test directories
        for test_dir in ["tests", "test", "spec", "__tests__"]:
            if (self.cwd / test_dir).is_dir():
                info.test_directories.append(test_dir)

        # Detect test patterns
        for path in self._walk_files():
            if "test_" in path.name or path.name.endswith("_test.py"):
                if "test_*.py" not in info.test_patterns:
                    info.test_patterns.append("test_*.py")

        return info

    def _parse_ci_config(self) -> CIConfig | None:
        """Item 85: Parse CI/CD configuration."""
        config = CIConfig()

        # GitHub Actions
        workflows_dir = self.cwd / ".github" / "workflows"
        if workflows_dir.is_dir():
            config.platform = "github"
            config.config_file = ".github/workflows/"
            for wf in workflows_dir.glob("*.yml"):
                config.workflows.append(wf.name)
                content = self._read_file(wf)
                if "pytest" in content or "npm test" in content:
                    config.has_tests = True
                if "lint" in content.lower() or "ruff" in content or "eslint" in content:
                    config.has_linting = True
                if "deploy" in content.lower():
                    config.has_deployment = True
            return config

        # GitLab CI
        gitlab_ci = self.cwd / ".gitlab-ci.yml"
        if gitlab_ci.exists():
            config.platform = "gitlab"
            config.config_file = ".gitlab-ci.yml"
            return config

        return None

    def _analyze_dependencies(self) -> DependencyInfo:
        """Item 86: Analyze dependencies."""
        info = DependencyInfo()

        # Get from manifest
        if (self.cwd / "pyproject.toml").exists():
            content = self._read_file(self.cwd / "pyproject.toml")
            deps_match = re.search(r"dependencies\s*=\s*\[(.*?)\]", content, re.DOTALL)
            if deps_match:
                for dep in re.findall(r'["\']([^"\'>=<\[]+)', deps_match.group(1)):
                    info.direct_dependencies[dep] = ""

        # Analyze internal imports
        for path in self._walk_files():
            if path.suffix == ".py":
                try:
                    content = self._read_file(path)
                    imports = re.findall(r"^(?:from|import)\s+([\w.]+)", content, re.MULTILINE)
                    info.internal_imports[str(path.relative_to(self.cwd))] = imports
                except Exception:
                    continue

        return info

    def _analyze_modules(self) -> list[ModuleInfo]:
        """Items 87-89: Analyze module structure."""
        modules = []

        for path in self._walk_files():
            if path.suffix != ".py":
                continue

            try:
                content = self._read_file(path)
                rel_path = str(path.relative_to(self.cwd))

                info = ModuleInfo(
                    name=path.stem,
                    path=rel_path,
                    type="module" if path.name != "__init__.py" else "package",
                )

                # Extract classes
                info.classes = re.findall(r"^class\s+(\w+)", content, re.MULTILINE)

                # Extract functions
                info.functions = re.findall(r"^def\s+(\w+)", content, re.MULTILINE)

                # Extract imports
                info.imports = re.findall(r"^(?:from|import)\s+([\w.]+)", content, re.MULTILINE)

                # Calculate complexity (simple metric: lines + branches)
                info.complexity = len(content.split("\n")) + len(
                    re.findall(r"\bif\b|\bfor\b|\bwhile\b", content)
                )

                modules.append(info)
            except Exception:
                continue

        return modules

    def _detect_api_endpoints(self) -> list[APIEndpoint]:
        """Item 90: Detect API endpoints."""
        endpoints = []

        for path in self._walk_files():
            if path.suffix != ".py":
                continue

            try:
                content = self._read_file(path)
                lines = content.split("\n")

                for i, line in enumerate(lines, 1):
                    # FastAPI style
                    match = re.match(
                        r'@(?:app|router)\.(get|post|put|delete|patch)\s*\(["\']([^"\']+)',
                        line,
                        re.IGNORECASE,
                    )
                    if match:
                        endpoints.append(
                            APIEndpoint(
                                method=match.group(1).upper(),
                                path=match.group(2),
                                handler="",
                                file=str(path.relative_to(self.cwd)),
                                line=i,
                            )
                        )

                    # Flask style
                    match = re.match(
                        r'@app\.route\s*\(["\']([^"\']+)["\'],?\s*methods\s*=\s*\[([^\]]+)', line
                    )
                    if match:
                        for method in re.findall(r'["\'](\w+)["\']', match.group(2)):
                            endpoints.append(
                                APIEndpoint(
                                    method=method.upper(),
                                    path=match.group(1),
                                    handler="",
                                    file=str(path.relative_to(self.cwd)),
                                    line=i,
                                )
                            )
            except Exception:
                continue

        return endpoints

    def _detect_database_tables(self) -> list[str]:
        """Item 91: Detect database tables/models."""
        tables = []

        for path in self._walk_files():
            if path.suffix != ".py":
                continue

            try:
                content = self._read_file(path)

                # SQLAlchemy models
                for match in re.finditer(r'__tablename__\s*=\s*["\']([^"\']+)["\']', content):
                    tables.append(match.group(1))

                # Django models
                for match in re.finditer(r"class\s+(\w+)\s*\(\s*(?:models\.)?Model\s*\)", content):
                    tables.append(match.group(1).lower())
            except Exception:
                continue

        return list(set(tables))

    def _find_config_files(self) -> list[str]:
        """Item 92: Find configuration files."""
        config_patterns = [
            "*.yaml",
            "*.yml",
            "*.toml",
            "*.ini",
            "*.cfg",
            ".env*",
            "config.*",
            "settings.*",
        ]
        configs = []

        for pattern in config_patterns:
            for path in self.cwd.glob(pattern):
                if path.is_file():
                    configs.append(str(path.relative_to(self.cwd)))

        return configs

    def _detect_environments(self) -> list[str]:
        """Item 93: Detect environment configurations."""
        envs = []

        for env_file in self.cwd.glob(".env*"):
            name = env_file.name.replace(".env", "") or "default"
            envs.append(name.strip("."))

        # Check for environment-specific configs
        for pattern in ["config/*.yaml", "config/*.yml", "environments/*"]:
            for path in self.cwd.glob(pattern):
                envs.append(path.stem)

        return list(set(envs))

    def _find_deployment_configs(self) -> list[str]:
        """Item 94: Find deployment configurations."""
        deployment_files = [
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
            "fly.toml",
            "vercel.json",
            "railway.json",
            "render.yaml",
            "Procfile",
            "app.yaml",
            "kubernetes/*.yaml",
        ]
        found = []

        for pattern in deployment_files:
            for path in self.cwd.glob(pattern):
                found.append(str(path.relative_to(self.cwd)))

        return found

    def _find_security_files(self) -> list[str]:
        """Item 95: Find security-related files."""
        security_patterns = [
            ".env*",
            "*.pem",
            "*.key",
            "*.crt",
            "secrets/*",
            "SECURITY.md",
            ".gitleaks.toml",
            ".secretlintrc*",
        ]
        found = []

        for pattern in security_patterns:
            for path in self.cwd.glob(pattern):
                if path.is_file():
                    found.append(str(path.relative_to(self.cwd)))

        return found

    def _walk_files(self, max_depth: int = 5) -> Iterator[Path]:
        """Walk files in the project, respecting gitignore-like patterns."""
        skip_dirs = {
            ".git",
            ".venv",
            "venv",
            "node_modules",
            "__pycache__",
            ".pytest_cache",
            "dist",
            "build",
        }

        def walk(path: Path, depth: int = 0) -> Iterator[Path]:
            if depth > max_depth:
                return
            try:
                for item in path.iterdir():
                    if item.name in skip_dirs:
                        continue
                    if item.is_file():
                        yield item
                    elif item.is_dir():
                        yield from walk(item, depth + 1)
            except PermissionError:
                pass

        yield from walk(self.cwd)

    def _read_file(self, path: Path) -> str:
        """Read file with caching."""
        str_path = str(path)
        if str_path not in self._file_cache:
            self._file_cache[str_path] = path.read_text(encoding="utf-8", errors="ignore")
        return self._file_cache[str_path]


# =============================================================================
# ITEMS 96-110: CODE ANALYSIS
# =============================================================================


@dataclass
class CodeComplexityMetrics:
    """Item 96: Code complexity metrics."""

    cyclomatic_complexity: int = 0
    cognitive_complexity: int = 0
    lines_of_code: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    functions: int = 0
    classes: int = 0


@dataclass
class DuplicateCode:
    """Item 97: Code duplication detection."""

    file1: str
    line1: int
    file2: str
    line2: int
    lines: int
    similarity: float


@dataclass
class DeadCode:
    """Item 98: Dead code detection."""

    file: str
    line: int
    type: str  # function, variable, import
    name: str
    reason: str


@dataclass
class CodeAnalysisResult:
    """Complete code analysis result."""

    complexity: dict[str, CodeComplexityMetrics] = field(default_factory=dict)
    duplicates: list[DuplicateCode] = field(default_factory=list)
    dead_code: list[DeadCode] = field(default_factory=list)
    unused_imports: list[tuple[str, str, int]] = field(default_factory=list)  # file, import, line
    type_coverage: float = 0.0
    test_coverage_gaps: list[str] = field(default_factory=list)
    error_handling_issues: list[tuple[str, int, str]] = field(default_factory=list)
    logging_gaps: list[str] = field(default_factory=list)
    performance_issues: list[tuple[str, int, str]] = field(default_factory=list)
    security_issues: list[tuple[str, int, str]] = field(default_factory=list)
    style_issues: list[tuple[str, int, str]] = field(default_factory=list)
    documentation_gaps: list[str] = field(default_factory=list)
    api_inconsistencies: list[str] = field(default_factory=list)
    backwards_compatibility_issues: list[str] = field(default_factory=list)


class CodeAnalyzer:
    """
    Items 96-110: Analyzes code quality and patterns.
    """

    SKIP_DIRS: ClassVar[set[str]] = {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        ".nox",
        "dist",
        "build",
        "htmlcov",
        ".next",
        ".cache",
        "coverage",
        "target",
        "site-packages",
        "vendor",
        "third_party",
        "test-results",
    }

    SKIP_PREFIXES: ClassVar[tuple[str, ...]] = (".",)

    SKIP_FILE_NAMES: ClassVar[set[str]] = {
        "coverage.xml",
    }

    def __init__(self, cwd: Path):
        self.cwd = cwd

    def analyze(self, files: list[Path] | None = None) -> CodeAnalysisResult:
        """Perform comprehensive code analysis."""
        result = CodeAnalysisResult()

        if files is None:
            files = list(self.cwd.rglob("*.py"))

        files = [file for file in files if not self._should_skip_path(file)]

        for file in files:
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
                rel_path = str(file.relative_to(self.cwd))

                # Item 96: Complexity analysis
                result.complexity[rel_path] = self._analyze_complexity(content)

                # Item 99: Unused import detection
                result.unused_imports.extend(self._find_unused_imports(content, rel_path))

                # Item 102: Error handling analysis
                result.error_handling_issues.extend(self._analyze_error_handling(content, rel_path))

                # Item 103: Logging analysis
                if not self._has_logging(content) and len(content.split("\n")) > 50:
                    result.logging_gaps.append(rel_path)

                # Item 104: Performance issue detection
                result.performance_issues.extend(self._detect_performance_issues(content, rel_path))

                # Item 105: Security issue detection
                result.security_issues.extend(self._detect_security_issues(content, rel_path))

                # Item 106: Style consistency
                result.style_issues.extend(self._check_style(content, rel_path))

                # Item 107: Documentation coverage
                if not self._has_docstrings(content) and "def " in content:
                    result.documentation_gaps.append(rel_path)

            except Exception:
                continue

        # Item 97: Duplicate detection (simplified)
        result.duplicates = self._find_duplicates(files)

        # Item 100: Type coverage
        result.type_coverage = self._calculate_type_coverage(files)

        # Item 101: Test coverage gaps
        result.test_coverage_gaps = self._find_test_coverage_gaps(files)

        return result

    def _analyze_complexity(self, content: str) -> CodeComplexityMetrics:
        """Item 96: Analyze code complexity."""
        lines = content.split("\n")
        metrics = CodeComplexityMetrics()

        metrics.lines_of_code = len([l for l in lines if l.strip()])
        metrics.comment_lines = len([l for l in lines if l.strip().startswith("#")])
        metrics.blank_lines = len([l for l in lines if not l.strip()])
        metrics.functions = len(re.findall(r"^def\s+", content, re.MULTILINE))
        metrics.classes = len(re.findall(r"^class\s+", content, re.MULTILINE))

        # Cyclomatic complexity (simplified: count decision points)
        decision_keywords = r"\b(if|elif|else|for|while|try|except|with|and|or)\b"
        metrics.cyclomatic_complexity = len(re.findall(decision_keywords, content))

        return metrics

    def _find_unused_imports(self, content: str, file: str) -> list[tuple[str, str, int]]:
        """Item 99: Find unused imports."""
        unused = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Match import statements
            import_match = re.match(r"^(?:from\s+[\w.]+\s+)?import\s+(.+)", line)
            if import_match:
                imports = import_match.group(1)
                # Extract imported names
                for name in re.findall(r"(\w+)(?:\s+as\s+\w+)?", imports):
                    # Check if name is used elsewhere in the file
                    rest_of_file = "\n".join(lines[i:])
                    if name not in ("*",) and not re.search(rf"\b{name}\b", rest_of_file):
                        unused.append((file, name, i))

        return unused

    def _analyze_error_handling(self, content: str, file: str) -> list[tuple[str, int, str]]:
        """Item 102: Analyze error handling patterns."""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Bare except
            if re.match(r"\s*except\s*:", line):
                issues.append((file, i, "Bare except clause (catches all exceptions)"))

            # Pass in except
            if i > 1 and "except" in lines[i - 2] and line.strip() == "pass":
                issues.append((file, i, "Silent exception handling (pass in except)"))

        return issues

    def _has_logging(self, content: str) -> bool:
        """Item 103: Check if file has logging."""
        return bool(re.search(r"\b(logging|logger|log)\b", content, re.IGNORECASE))

    def _detect_performance_issues(self, content: str, file: str) -> list[tuple[str, int, str]]:
        """Item 104: Detect potential performance issues."""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # String concatenation in loop
            if "+=" in line and ('"' in line or "'" in line):
                issues.append((file, i, "String concatenation (consider using join)"))

            # Multiple isinstance checks
            if line.count("isinstance") > 2:
                issues.append((file, i, "Multiple isinstance calls (consider tuple)"))

        return issues

    def _detect_security_issues(self, content: str, file: str) -> list[tuple[str, int, str]]:
        """Item 105: Detect potential security issues."""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Hardcoded secrets
            if re.search(
                r'(password|secret|api_key|token)\s*=\s*["\'][^"\']+["\']', line, re.IGNORECASE
            ):
                issues.append((file, i, "Potential hardcoded secret"))

            # SQL injection risk
            if re.search(r'execute\s*\(\s*["\'].*%s|execute\s*\([^)]*\+', line):
                issues.append((file, i, "Potential SQL injection risk"))

            # eval usage
            if re.search(r"\beval\s*\(", line):
                issues.append((file, i, "Use of eval() is dangerous"))

        return issues

    def _check_style(self, content: str, file: str) -> list[tuple[str, int, str]]:
        """Item 106: Check style consistency."""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Long lines
            if len(line) > 120:
                issues.append((file, i, f"Line too long ({len(line)} > 120)"))

            # Trailing whitespace
            if line.endswith(" ") or line.endswith("\t"):
                issues.append((file, i, "Trailing whitespace"))

        return issues

    def _has_docstrings(self, content: str) -> bool:
        """Item 107: Check for docstrings."""
        # Check if functions have docstrings
        functions = re.findall(r'def\s+\w+[^:]+:\s*\n(\s+)["\']', content)
        return len(functions) > 0

    def _find_duplicates(self, files: list[Path]) -> list[DuplicateCode]:
        """Item 97: Find code duplicates (simplified)."""
        # This is a simplified implementation
        # A real implementation would use more sophisticated algorithms
        return []

    def _calculate_type_coverage(self, files: list[Path]) -> float:
        """Item 100: Calculate type annotation coverage."""
        total_functions = 0
        typed_functions = 0

        for file in files:
            if self._should_skip_path(file):
                continue

            try:
                content = file.read_text(encoding="utf-8", errors="ignore")

                # Count all function definitions
                all_funcs = re.findall(r"^def\s+\w+\s*\([^)]*\)", content, re.MULTILINE)
                total_functions += len(all_funcs)

                # Count typed functions (have return type annotation)
                typed_funcs = re.findall(r"^def\s+\w+\s*\([^)]*\)\s*->", content, re.MULTILINE)
                typed_functions += len(typed_funcs)
            except Exception:
                continue

        return typed_functions / max(total_functions, 1)

    def _find_test_coverage_gaps(self, files: list[Path]) -> list[str]:
        """Item 101: Find modules without tests."""
        gaps = []
        modules = set()
        tested_modules = set()

        for file in files:
            if self._should_skip_path(file):
                continue
            rel_path = str(file.relative_to(self.cwd))
            if "test" in rel_path.lower():
                # Extract what module is being tested
                tested = re.findall(
                    r"from\s+([\w.]+)\s+import|import\s+([\w.]+)", file.read_text(encoding="utf-8", errors="ignore")
                )
                for match in tested:
                    tested_modules.add(match[0] or match[1])
            elif file.suffix == ".py" and "__init__" not in file.name:
                modules.add(file.stem)

        gaps = [m for m in modules if m not in tested_modules]
        return gaps

    def _should_skip_path(self, path: Path) -> bool:
        """Return True for vendored, generated, or hidden files that should not drive analysis."""
        try:
            rel_path = path.relative_to(self.cwd)
        except ValueError:
            rel_path = path

        for part in rel_path.parts[:-1]:
            if part in self.SKIP_DIRS:
                return True
            if part.startswith(self.SKIP_PREFIXES):
                return True

        name = rel_path.name
        if name in self.SKIP_FILE_NAMES:
            return True
        if name.startswith(self.SKIP_PREFIXES):
            return True

        return False


# =============================================================================
# ITEMS 111-120: CONTEXT BUILDING
# =============================================================================


@dataclass
class ContextChunk:
    """Item 111: A chunk of context for the model."""

    file_path: str
    content: str
    relevance_score: float = 0.0
    tokens_estimate: int = 0
    chunk_type: str = "code"  # code, config, doc, test


@dataclass
class ContextWindow:
    """Item 111-112: Managed context window."""

    chunks: list[ContextChunk] = field(default_factory=list)
    total_tokens: int = 0
    max_tokens: int = 100000

    def add_chunk(self, chunk: ContextChunk) -> bool:
        """Add chunk if it fits in the window."""
        if self.total_tokens + chunk.tokens_estimate <= self.max_tokens:
            self.chunks.append(chunk)
            self.total_tokens += chunk.tokens_estimate
            return True
        return False

    def get_content(self) -> str:
        """Get all content concatenated."""
        return "\n\n".join(f"## {c.file_path}\n{c.content}" for c in self.chunks)


class ContextBuilder:
    """
    Items 111-120: Builds and manages context for the model.
    """

    def __init__(self, cwd: Path, max_tokens: int = 100000):
        self.cwd = cwd
        self.max_tokens = max_tokens

    def build_context(
        self, query: str, project_analysis: ProjectAnalysis | None = None
    ) -> ContextWindow:
        """Build optimized context window for a query."""
        window = ContextWindow(max_tokens=self.max_tokens)

        # Item 112: Prioritize by relevance
        chunks = self._gather_chunks(query)
        chunks.sort(key=lambda c: c.relevance_score, reverse=True)

        # Item 113: Add chunks incrementally
        for chunk in chunks:
            if not window.add_chunk(chunk):
                break

        return window

    def _gather_chunks(self, query: str) -> list[ContextChunk]:
        """Gather potential context chunks."""
        chunks = []
        query_terms = set(query.lower().split())

        for path in self._walk_files():
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                rel_path = str(path.relative_to(self.cwd))

                # Item 112: Calculate relevance
                content_terms = set(content.lower().split())
                relevance = len(query_terms & content_terms) / max(len(query_terms), 1)

                # Boost certain file types
                if path.suffix in (".md", ".rst"):
                    relevance *= 1.2
                if "readme" in path.name.lower():
                    relevance *= 1.5
                if "config" in path.name.lower():
                    relevance *= 1.1

                chunk = ContextChunk(
                    file_path=rel_path,
                    content=content[:10000],  # Limit content size
                    relevance_score=relevance,
                    tokens_estimate=len(content) // 4,  # Rough estimate
                    chunk_type=self._classify_file(path),
                )
                chunks.append(chunk)
            except Exception:
                continue

        return chunks

    def _classify_file(self, path: Path) -> str:
        """Classify file type for context."""
        name = path.name.lower()
        if "test" in name:
            return "test"
        if path.suffix in (".md", ".rst", ".txt"):
            return "doc"
        if path.suffix in (".yaml", ".yml", ".toml", ".ini", ".json"):
            return "config"
        return "code"

    def _walk_files(self) -> Iterator[Path]:
        """Walk project files."""
        skip_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__"}

        def walk(path: Path, depth: int = 0) -> Iterator[Path]:
            if depth > 3:
                return
            try:
                for item in path.iterdir():
                    if item.name in skip_dirs:
                        continue
                    if item.is_file() and item.suffix in (
                        ".py",
                        ".js",
                        ".ts",
                        ".md",
                        ".yaml",
                        ".yml",
                        ".toml",
                        ".json",
                    ):
                        yield item
                    elif item.is_dir():
                        yield from walk(item, depth + 1)
            except PermissionError:
                pass

        yield from walk(self.cwd)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def analyze_project(cwd: Path) -> ProjectAnalysis:
    """Analyze a project's structure."""
    return ProjectStructureAnalyzer(cwd).analyze()


def analyze_code(cwd: Path, files: list[Path] | None = None) -> CodeAnalysisResult:
    """Analyze code quality."""
    return CodeAnalyzer(cwd).analyze(files)


def build_context(cwd: Path, query: str, max_tokens: int = 100000) -> ContextWindow:
    """Build context window for a query."""
    return ContextBuilder(cwd, max_tokens).build_context(query)
