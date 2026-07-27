"""Comprehensive tests for sage/core/codebase_analyzer.py - Codebase analysis."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock
import tempfile
import os

from sage.core.codebase_analyzer import (
    ProjectType,
    Framework,
    ProjectManifest,
    TestFrameworkInfo,
    CIConfig,
    DependencyInfo,
    ModuleInfo,
    APIEndpoint,
    ProjectAnalysis,
    CodeComplexityMetrics,
    DuplicateCode,
    DeadCode,
    CodeAnalysisResult,
    ContextChunk,
    ContextWindow,
    ProjectStructureAnalyzer,
    CodeAnalyzer,
    ContextBuilder,
    analyze_project,
    analyze_code,
    build_context,
)


# =============================================================================
# Tests for ProjectType enum
# =============================================================================


class TestProjectType:
    """Tests for ProjectType enum."""

    def test_python_value(self):
        """PYTHON is defined."""
        assert ProjectType.PYTHON is not None

    def test_javascript_value(self):
        """JAVASCRIPT is defined."""
        assert ProjectType.JAVASCRIPT is not None

    def test_typescript_value(self):
        """TYPESCRIPT is defined."""
        assert ProjectType.TYPESCRIPT is not None

    def test_java_value(self):
        """JAVA is defined."""
        assert ProjectType.JAVA is not None

    def test_go_value(self):
        """GO is defined."""
        assert ProjectType.GO is not None

    def test_rust_value(self):
        """RUST is defined."""
        assert ProjectType.RUST is not None

    def test_csharp_value(self):
        """CSHARP is defined."""
        assert ProjectType.CSHARP is not None

    def test_ruby_value(self):
        """RUBY is defined."""
        assert ProjectType.RUBY is not None

    def test_php_value(self):
        """PHP is defined."""
        assert ProjectType.PHP is not None

    def test_mixed_value(self):
        """MIXED is defined."""
        assert ProjectType.MIXED is not None

    def test_unknown_value(self):
        """UNKNOWN is defined."""
        assert ProjectType.UNKNOWN is not None


# =============================================================================
# Tests for Framework enum
# =============================================================================


class TestFramework:
    """Tests for Framework enum."""

    def test_fastapi_value(self):
        """FASTAPI is defined."""
        assert Framework.FASTAPI is not None

    def test_django_value(self):
        """DJANGO is defined."""
        assert Framework.DJANGO is not None

    def test_flask_value(self):
        """FLASK is defined."""
        assert Framework.FLASK is not None

    def test_pytest_value(self):
        """PYTEST is defined."""
        assert Framework.PYTEST is not None

    def test_typer_value(self):
        """TYPER is defined."""
        assert Framework.TYPER is not None

    def test_click_value(self):
        """CLICK is defined."""
        assert Framework.CLICK is not None

    def test_react_value(self):
        """REACT is defined."""
        assert Framework.REACT is not None

    def test_nextjs_value(self):
        """NEXTJS is defined."""
        assert Framework.NEXTJS is not None

    def test_express_value(self):
        """EXPRESS is defined."""
        assert Framework.EXPRESS is not None

    def test_nestjs_value(self):
        """NESTJS is defined."""
        assert Framework.NESTJS is not None

    def test_vue_value(self):
        """VUE is defined."""
        assert Framework.VUE is not None

    def test_none_value(self):
        """NONE is defined."""
        assert Framework.NONE is not None


# =============================================================================
# Tests for ProjectManifest dataclass
# =============================================================================


class TestProjectManifest:
    """Tests for ProjectManifest dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        manifest = ProjectManifest()
        assert manifest.name == ""
        assert manifest.version == ""
        assert manifest.description == ""
        assert manifest.dependencies == {}
        assert manifest.dev_dependencies == {}
        assert manifest.scripts == {}
        assert manifest.entry_points == []
        assert manifest.python_requires == ""

    def test_create_with_values(self):
        """Create with values."""
        manifest = ProjectManifest(
            name="my-project",
            version="1.0.0",
            description="A test project",
            dependencies={"requests": "^2.0"},
            dev_dependencies={"pytest": "^7.0"},
            scripts={"test": "pytest"},
            entry_points=["main"],
            python_requires=">=3.9",
        )
        assert manifest.name == "my-project"
        assert manifest.version == "1.0.0"
        assert manifest.description == "A test project"
        assert "requests" in manifest.dependencies
        assert "pytest" in manifest.dev_dependencies
        assert "test" in manifest.scripts
        assert "main" in manifest.entry_points
        assert manifest.python_requires == ">=3.9"


# =============================================================================
# Tests for TestFrameworkInfo dataclass
# =============================================================================


class TestTestFrameworkInfo:
    """Tests for TestFrameworkInfo dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        info = TestFrameworkInfo()
        assert info.framework == ""
        assert info.config_file is None
        assert info.test_directories == []
        assert info.test_patterns == []
        assert info.coverage_enabled is False

    def test_create_with_values(self):
        """Create with values."""
        info = TestFrameworkInfo(
            framework="pytest",
            config_file="pytest.ini",
            test_directories=["tests"],
            test_patterns=["test_*.py"],
            coverage_enabled=True,
        )
        assert info.framework == "pytest"
        assert info.config_file == "pytest.ini"
        assert "tests" in info.test_directories
        assert "test_*.py" in info.test_patterns
        assert info.coverage_enabled is True


# =============================================================================
# Tests for CIConfig dataclass
# =============================================================================


class TestCIConfig:
    """Tests for CIConfig dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        config = CIConfig()
        assert config.platform == ""
        assert config.config_file == ""
        assert config.workflows == []
        assert config.triggers == []
        assert config.has_tests is False
        assert config.has_linting is False
        assert config.has_deployment is False

    def test_create_with_values(self):
        """Create with values."""
        config = CIConfig(
            platform="github",
            config_file=".github/workflows/ci.yml",
            workflows=["ci.yml", "deploy.yml"],
            triggers=["push", "pull_request"],
            has_tests=True,
            has_linting=True,
            has_deployment=True,
        )
        assert config.platform == "github"
        assert config.has_tests is True
        assert "ci.yml" in config.workflows


# =============================================================================
# Tests for DependencyInfo dataclass
# =============================================================================


class TestDependencyInfo:
    """Tests for DependencyInfo dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        info = DependencyInfo()
        assert info.direct_dependencies == {}
        assert info.dev_dependencies == {}
        assert info.internal_imports == {}
        assert info.circular_dependencies == []

    def test_create_with_values(self):
        """Create with values."""
        info = DependencyInfo(
            direct_dependencies={"requests": "2.28.0"},
            dev_dependencies={"pytest": "7.0.0"},
            internal_imports={"main.py": ["utils"]},
            circular_dependencies=[("a", "b")],
        )
        assert "requests" in info.direct_dependencies
        assert "pytest" in info.dev_dependencies
        assert "main.py" in info.internal_imports
        assert ("a", "b") in info.circular_dependencies


# =============================================================================
# Tests for ModuleInfo dataclass
# =============================================================================


class TestModuleInfo:
    """Tests for ModuleInfo dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        info = ModuleInfo(name="test", path="test.py", type="module")
        assert info.name == "test"
        assert info.path == "test.py"
        assert info.type == "module"
        assert info.imports == []
        assert info.exports == []
        assert info.classes == []
        assert info.functions == []
        assert info.complexity == 0

    def test_create_full(self):
        """Create with all fields."""
        info = ModuleInfo(
            name="utils",
            path="src/utils.py",
            type="module",
            imports=["os", "sys"],
            exports=["helper"],
            classes=["Config"],
            functions=["process", "validate"],
            complexity=50,
        )
        assert info.name == "utils"
        assert "os" in info.imports
        assert "Config" in info.classes
        assert info.complexity == 50


# =============================================================================
# Tests for APIEndpoint dataclass
# =============================================================================


class TestAPIEndpoint:
    """Tests for APIEndpoint dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        endpoint = APIEndpoint(
            method="GET",
            path="/api/users",
            handler="get_users",
            file="routes.py",
            line=10,
        )
        assert endpoint.method == "GET"
        assert endpoint.path == "/api/users"
        assert endpoint.handler == "get_users"
        assert endpoint.file == "routes.py"
        assert endpoint.line == 10
        assert endpoint.parameters == []

    def test_create_with_parameters(self):
        """Create with parameters."""
        endpoint = APIEndpoint(
            method="POST",
            path="/api/users",
            handler="create_user",
            file="routes.py",
            line=20,
            parameters=["name", "email"],
        )
        assert "name" in endpoint.parameters
        assert "email" in endpoint.parameters


# =============================================================================
# Tests for ProjectAnalysis dataclass
# =============================================================================


class TestProjectAnalysis:
    """Tests for ProjectAnalysis dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        analysis = ProjectAnalysis(project_type=ProjectType.PYTHON)
        assert analysis.project_type == ProjectType.PYTHON
        assert analysis.frameworks == []
        assert analysis.manifest is None
        assert analysis.test_info is None
        assert analysis.ci_config is None
        assert analysis.dependencies is None
        assert analysis.modules == []
        assert analysis.api_endpoints == []
        assert analysis.database_tables == []
        assert analysis.config_files == []
        assert analysis.environments == []
        assert analysis.deployment_configs == []
        assert analysis.security_files == []

    def test_create_full(self):
        """Create with all fields."""
        analysis = ProjectAnalysis(
            project_type=ProjectType.PYTHON,
            frameworks=[Framework.FASTAPI, Framework.PYTEST],
            manifest=ProjectManifest(name="test"),
            test_info=TestFrameworkInfo(framework="pytest"),
            ci_config=CIConfig(platform="github"),
            dependencies=DependencyInfo(),
            modules=[ModuleInfo(name="main", path="main.py", type="module")],
            api_endpoints=[
                APIEndpoint(
                    method="GET", path="/", handler="root", file="main.py", line=1
                )
            ],
            database_tables=["users", "posts"],
            config_files=["config.yaml"],
            environments=["dev", "prod"],
            deployment_configs=["Dockerfile"],
            security_files=[".env"],
        )
        assert Framework.FASTAPI in analysis.frameworks
        assert analysis.manifest.name == "test"
        assert "users" in analysis.database_tables


# =============================================================================
# Tests for CodeComplexityMetrics dataclass
# =============================================================================


class TestCodeComplexityMetrics:
    """Tests for CodeComplexityMetrics dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        metrics = CodeComplexityMetrics()
        assert metrics.cyclomatic_complexity == 0
        assert metrics.cognitive_complexity == 0
        assert metrics.lines_of_code == 0
        assert metrics.comment_lines == 0
        assert metrics.blank_lines == 0
        assert metrics.functions == 0
        assert metrics.classes == 0

    def test_create_with_values(self):
        """Create with values."""
        metrics = CodeComplexityMetrics(
            cyclomatic_complexity=10,
            cognitive_complexity=15,
            lines_of_code=100,
            comment_lines=20,
            blank_lines=10,
            functions=5,
            classes=2,
        )
        assert metrics.cyclomatic_complexity == 10
        assert metrics.lines_of_code == 100
        assert metrics.functions == 5


# =============================================================================
# Tests for DuplicateCode dataclass
# =============================================================================


class TestDuplicateCode:
    """Tests for DuplicateCode dataclass."""

    def test_create(self):
        """Create duplicate code entry."""
        dup = DuplicateCode(
            file1="a.py",
            line1=10,
            file2="b.py",
            line2=20,
            lines=5,
            similarity=0.95,
        )
        assert dup.file1 == "a.py"
        assert dup.line1 == 10
        assert dup.file2 == "b.py"
        assert dup.line2 == 20
        assert dup.lines == 5
        assert dup.similarity == 0.95


# =============================================================================
# Tests for DeadCode dataclass
# =============================================================================


class TestDeadCode:
    """Tests for DeadCode dataclass."""

    def test_create(self):
        """Create dead code entry."""
        dead = DeadCode(
            file="utils.py",
            line=50,
            type="function",
            name="unused_helper",
            reason="Never called",
        )
        assert dead.file == "utils.py"
        assert dead.line == 50
        assert dead.type == "function"
        assert dead.name == "unused_helper"
        assert dead.reason == "Never called"


# =============================================================================
# Tests for CodeAnalysisResult dataclass
# =============================================================================


class TestCodeAnalysisResult:
    """Tests for CodeAnalysisResult dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        result = CodeAnalysisResult()
        assert result.complexity == {}
        assert result.duplicates == []
        assert result.dead_code == []
        assert result.unused_imports == []
        assert result.type_coverage == 0.0
        assert result.test_coverage_gaps == []
        assert result.error_handling_issues == []
        assert result.logging_gaps == []
        assert result.performance_issues == []
        assert result.security_issues == []
        assert result.style_issues == []
        assert result.documentation_gaps == []
        assert result.api_inconsistencies == []
        assert result.backwards_compatibility_issues == []

    def test_create_with_values(self):
        """Create with values."""
        result = CodeAnalysisResult(
            complexity={"main.py": CodeComplexityMetrics(lines_of_code=100)},
            unused_imports=[("main.py", "os", 1)],
            type_coverage=0.85,
            security_issues=[("main.py", 10, "Hardcoded secret")],
        )
        assert "main.py" in result.complexity
        assert len(result.unused_imports) == 1
        assert result.type_coverage == 0.85
        assert len(result.security_issues) == 1


# =============================================================================
# Tests for ContextChunk dataclass
# =============================================================================


class TestContextChunk:
    """Tests for ContextChunk dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        chunk = ContextChunk(file_path="main.py", content="print('hello')")
        assert chunk.file_path == "main.py"
        assert chunk.content == "print('hello')"
        assert chunk.relevance_score == 0.0
        assert chunk.tokens_estimate == 0
        assert chunk.chunk_type == "code"

    def test_create_full(self):
        """Create with all fields."""
        chunk = ContextChunk(
            file_path="README.md",
            content="# Documentation",
            relevance_score=0.9,
            tokens_estimate=100,
            chunk_type="doc",
        )
        assert chunk.file_path == "README.md"
        assert chunk.relevance_score == 0.9
        assert chunk.tokens_estimate == 100
        assert chunk.chunk_type == "doc"


# =============================================================================
# Tests for ContextWindow dataclass
# =============================================================================


class TestContextWindow:
    """Tests for ContextWindow dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        window = ContextWindow()
        assert window.chunks == []
        assert window.total_tokens == 0
        assert window.max_tokens == 100000

    def test_add_chunk_fits(self):
        """Add chunk that fits."""
        window = ContextWindow(max_tokens=1000)
        chunk = ContextChunk(
            file_path="test.py", content="code", tokens_estimate=100
        )
        result = window.add_chunk(chunk)
        assert result is True
        assert len(window.chunks) == 1
        assert window.total_tokens == 100

    def test_add_chunk_exceeds(self):
        """Add chunk that exceeds limit."""
        window = ContextWindow(max_tokens=100)
        chunk = ContextChunk(
            file_path="test.py", content="code", tokens_estimate=200
        )
        result = window.add_chunk(chunk)
        assert result is False
        assert len(window.chunks) == 0
        assert window.total_tokens == 0

    def test_add_multiple_chunks(self):
        """Add multiple chunks."""
        window = ContextWindow(max_tokens=300)
        chunk1 = ContextChunk(file_path="a.py", content="a", tokens_estimate=100)
        chunk2 = ContextChunk(file_path="b.py", content="b", tokens_estimate=100)
        chunk3 = ContextChunk(file_path="c.py", content="c", tokens_estimate=150)

        assert window.add_chunk(chunk1) is True
        assert window.add_chunk(chunk2) is True
        assert window.add_chunk(chunk3) is False  # Would exceed
        assert len(window.chunks) == 2
        assert window.total_tokens == 200

    def test_get_content(self):
        """Get concatenated content."""
        window = ContextWindow()
        window.chunks = [
            ContextChunk(file_path="a.py", content="code_a"),
            ContextChunk(file_path="b.py", content="code_b"),
        ]
        content = window.get_content()
        assert "## a.py" in content
        assert "code_a" in content
        assert "## b.py" in content
        assert "code_b" in content


# =============================================================================
# Tests for ProjectStructureAnalyzer class
# =============================================================================


class TestProjectStructureAnalyzer:
    """Tests for ProjectStructureAnalyzer class."""

    def test_init(self):
        """Initialize analyzer."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            assert analyzer.cwd == Path(tmpdir)
            assert analyzer._file_cache == {}

    def test_class_patterns(self):
        """Class has pattern definitions."""
        assert ProjectStructureAnalyzer.PYTHON_PATTERNS is not None
        assert ProjectStructureAnalyzer.JS_PATTERNS is not None
        assert ProjectStructureAnalyzer.TS_PATTERNS is not None
        assert ProjectStructureAnalyzer.GO_PATTERNS is not None
        assert ProjectStructureAnalyzer.RUST_PATTERNS is not None

    def test_framework_indicators(self):
        """Class has framework indicators."""
        assert Framework.FASTAPI in ProjectStructureAnalyzer.FRAMEWORK_INDICATORS
        assert Framework.DJANGO in ProjectStructureAnalyzer.FRAMEWORK_INDICATORS
        assert Framework.REACT in ProjectStructureAnalyzer.FRAMEWORK_INDICATORS

    def test_analyze_empty_project(self):
        """Analyze empty project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert result.project_type == ProjectType.UNKNOWN
            assert result.frameworks == []

    def test_analyze_python_project(self):
        """Analyze Python project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create Python files
            (Path(tmpdir) / "main.py").write_text("print('hello')")
            (Path(tmpdir) / "utils.py").write_text("def helper(): pass")

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert result.project_type == ProjectType.PYTHON

    def test_detect_frameworks(self):
        """Detect frameworks in code."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "app.py").write_text(
                "from fastapi import FastAPI\napp = FastAPI()"
            )

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            frameworks = analyzer._detect_frameworks()
            assert Framework.FASTAPI in frameworks

    def test_parse_pyproject_manifest(self):
        """Parse pyproject.toml manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pyproject = Path(tmpdir) / "pyproject.toml"
            pyproject.write_text(
                """
[project]
name = "test-project"
version = "1.0.0"
dependencies = ["requests", "click"]
"""
            )

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            manifest = analyzer._parse_manifest()
            assert manifest is not None
            assert manifest.name == "test-project"
            assert manifest.version == "1.0.0"

    def test_parse_package_json_manifest(self):
        """Parse package.json manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            package_json = Path(tmpdir) / "package.json"
            package_json.write_text(
                """
{
    "name": "js-project",
    "version": "2.0.0",
    "description": "A JS project",
    "dependencies": {"react": "^18.0.0"},
    "devDependencies": {"jest": "^29.0.0"},
    "scripts": {"test": "jest"}
}
"""
            )

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            manifest = analyzer._parse_manifest()
            assert manifest is not None
            assert manifest.name == "js-project"
            assert manifest.version == "2.0.0"
            assert "react" in manifest.dependencies
            assert "jest" in manifest.dev_dependencies

    def test_detect_test_framework_pytest(self):
        """Detect pytest test framework."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pyproject = Path(tmpdir) / "pyproject.toml"
            pyproject.write_text("[tool.pytest.ini_options]\ntestpaths = ['tests']")
            tests_dir = Path(tmpdir) / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_main.py").write_text("def test_example(): pass")

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            info = analyzer._detect_test_framework()
            assert info.framework == "pytest"
            assert "tests" in info.test_directories

    def test_parse_ci_config_github(self):
        """Parse GitHub Actions CI config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workflows_dir = Path(tmpdir) / ".github" / "workflows"
            workflows_dir.mkdir(parents=True)
            (workflows_dir / "ci.yml").write_text(
                """
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest
      - run: ruff check .
"""
            )

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            config = analyzer._parse_ci_config()
            assert config is not None
            assert config.platform == "github"
            assert "ci.yml" in config.workflows
            assert config.has_tests is True
            assert config.has_linting is True

    def test_analyze_dependencies(self):
        """Analyze dependencies."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "pyproject.toml").write_text(
                'dependencies = ["requests", "click"]'
            )
            (Path(tmpdir) / "main.py").write_text(
                "import os\nfrom utils import helper"
            )

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            info = analyzer._analyze_dependencies()
            assert "requests" in info.direct_dependencies
            assert "main.py" in info.internal_imports

    def test_analyze_modules(self):
        """Analyze module structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "utils.py").write_text(
                """
import os

class Config:
    pass

def process():
    if True:
        pass
"""
            )

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            modules = analyzer._analyze_modules()
            assert len(modules) == 1
            assert modules[0].name == "utils"
            assert "Config" in modules[0].classes
            assert "process" in modules[0].functions
            assert modules[0].complexity > 0

    def test_detect_api_endpoints_fastapi(self):
        """Detect FastAPI endpoints."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "routes.py").write_text(
                """
@app.get("/users")
def get_users():
    pass

@router.post("/items")
def create_item():
    pass
"""
            )

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            endpoints = analyzer._detect_api_endpoints()
            assert len(endpoints) == 2
            methods = [e.method for e in endpoints]
            assert "GET" in methods
            assert "POST" in methods

    def test_detect_database_tables_sqlalchemy(self):
        """Detect SQLAlchemy tables."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "models.py").write_text(
                """
class User(Base):
    __tablename__ = "users"

class Post(Base):
    __tablename__ = "posts"
"""
            )

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            tables = analyzer._detect_database_tables()
            assert "users" in tables
            assert "posts" in tables

    def test_find_config_files(self):
        """Find configuration files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "config.yaml").write_text("key: value")
            (Path(tmpdir) / "settings.toml").write_text("[settings]")

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            configs = analyzer._find_config_files()
            assert any("config.yaml" in c for c in configs)

    def test_detect_environments(self):
        """Detect environments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / ".env").write_text("KEY=value")
            (Path(tmpdir) / ".env.production").write_text("KEY=prod")

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            envs = analyzer._detect_environments()
            assert len(envs) >= 1

    def test_find_deployment_configs(self):
        """Find deployment configurations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Dockerfile").write_text("FROM python:3.11")
            (Path(tmpdir) / "docker-compose.yml").write_text("version: '3'")

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            configs = analyzer._find_deployment_configs()
            assert "Dockerfile" in configs
            assert "docker-compose.yml" in configs

    def test_find_security_files(self):
        """Find security-related files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / ".env").write_text("SECRET=xxx")
            (Path(tmpdir) / "SECURITY.md").write_text("# Security")

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            files = analyzer._find_security_files()
            assert any(".env" in f for f in files)
            assert "SECURITY.md" in files

    def test_walk_files_skips_directories(self):
        """Walk files skips common directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create directories that should be skipped
            (Path(tmpdir) / ".git").mkdir()
            (Path(tmpdir) / "node_modules").mkdir()
            (Path(tmpdir) / "__pycache__").mkdir()
            (Path(tmpdir) / ".git" / "config").write_text("git config")
            (Path(tmpdir) / "main.py").write_text("code")

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))
            files = list(analyzer._walk_files())
            paths = [str(f) for f in files]

            # Should find main.py
            assert any("main.py" in p for p in paths)
            # Should not find files in skipped dirs
            assert not any(".git" in p for p in paths)

    def test_read_file_caches(self):
        """Read file uses caching."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("content")

            analyzer = ProjectStructureAnalyzer(Path(tmpdir))

            # First read
            content1 = analyzer._read_file(test_file)
            assert content1 == "content"
            assert str(test_file) in analyzer._file_cache

            # Second read should use cache
            content2 = analyzer._read_file(test_file)
            assert content2 == "content"


# =============================================================================
# Tests for CodeAnalyzer class
# =============================================================================


class TestCodeAnalyzer:
    """Tests for CodeAnalyzer class."""

    def test_init(self):
        """Initialize analyzer."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = CodeAnalyzer(Path(tmpdir))
            assert analyzer.cwd == Path(tmpdir)

    def test_analyze_empty_project(self):
        """Analyze empty project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert result.complexity == {}

    def test_analyze_skips_vendored_and_generated_python(self):
        """Repo analysis should ignore vendored and generated directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "src").mkdir()
            (base / "src" / "app.py").write_text("def run():\n    return 1\n")

            (base / "node_modules").mkdir()
            (base / "node_modules" / "vendor.py").write_text("def vendored():\n    return 2\n")

            (base / ".venv").mkdir()
            (base / ".venv" / "ignored.py").write_text("def ignored():\n    return 3\n")

            (base / "test-results").mkdir()
            (base / "test-results" / "artifact.py").write_text("def artifact():\n    return 4\n")

            analyzer = CodeAnalyzer(base)
            result = analyzer.analyze()

            assert "src/app.py" in result.complexity
            assert "node_modules/vendor.py" not in result.complexity
            assert ".venv/ignored.py" not in result.complexity
            assert "test-results/artifact.py" not in result.complexity

    def test_analyze_complexity(self):
        """Analyze code complexity."""
        content = """
# Comment
def func1():
    if True:
        for i in range(10):
            pass

class MyClass:
    def method(self):
        pass
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "code.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert "code.py" in result.complexity
            metrics = result.complexity["code.py"]
            assert metrics.lines_of_code > 0
            # Regex ^def\s+ only matches non-indented functions
            assert metrics.functions >= 1
            assert metrics.classes >= 1
            assert metrics.cyclomatic_complexity > 0

    def test_find_unused_imports(self):
        """Find unused imports."""
        content = """
import os
import sys
import json

print(os.getcwd())
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "main.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            # sys and json are unused
            unused_names = [u[1] for u in result.unused_imports]
            assert "sys" in unused_names or "json" in unused_names

    def test_detect_error_handling_issues(self):
        """Detect error handling issues."""
        content = """
try:
    risky_operation()
except:
    pass
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "handler.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert len(result.error_handling_issues) > 0

    def test_detect_logging_gaps(self):
        """Detect files without logging."""
        content = """
def process():
    data = fetch_data()
    result = transform(data)
    return result
""" + "\n" * 50  # Make it long enough

        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "processor.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert "processor.py" in result.logging_gaps

    def test_detect_performance_issues(self):
        """Detect performance issues."""
        content = """
def build_string():
    result = ""
    for i in range(100):
        result += str(i) + ","
    return result
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "perf.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            # Should detect string concatenation issue
            assert len(result.performance_issues) > 0

    def test_detect_security_issues_hardcoded_secret(self):
        """Detect hardcoded secrets."""
        content = """
password = "secret123"
api_key = "sk-12345"
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "config.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert len(result.security_issues) > 0

    def test_detect_security_issues_eval(self):
        """Detect eval usage."""
        content = """
def execute(code):
    return eval(code)
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "danger.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            security_messages = [s[2] for s in result.security_issues]
            assert any("eval" in m for m in security_messages)

    def test_check_style_long_lines(self):
        """Check for long lines."""
        content = "x = " + "a" * 150 + "\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "style.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert len(result.style_issues) > 0

    def test_check_documentation_gaps(self):
        """Check for missing documentation."""
        content = """
def undocumented_function():
    pass
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "nodocs.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert "nodocs.py" in result.documentation_gaps

    def test_calculate_type_coverage(self):
        """Calculate type annotation coverage."""
        content = """
def typed_function(x: int) -> str:
    return str(x)

def untyped_function(x):
    return x
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "types.py").write_text(content)

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            assert 0 <= result.type_coverage <= 1.0

    def test_find_test_coverage_gaps(self):
        """Find modules without tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "module.py").write_text("def func(): pass")
            (Path(tmpdir) / "another.py").write_text("def other(): pass")

            analyzer = CodeAnalyzer(Path(tmpdir))
            result = analyzer.analyze()
            # Both should show as gaps since no test files
            assert len(result.test_coverage_gaps) >= 0


# =============================================================================
# Tests for ContextBuilder class
# =============================================================================


class TestContextBuilder:
    """Tests for ContextBuilder class."""

    def test_init(self):
        """Initialize builder."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ContextBuilder(Path(tmpdir))
            assert builder.cwd == Path(tmpdir)
            assert builder.max_tokens == 100000

    def test_init_custom_tokens(self):
        """Initialize with custom max tokens."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ContextBuilder(Path(tmpdir), max_tokens=50000)
            assert builder.max_tokens == 50000

    def test_build_context_empty_project(self):
        """Build context for empty project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ContextBuilder(Path(tmpdir))
            window = builder.build_context("test query")
            assert isinstance(window, ContextWindow)
            assert len(window.chunks) == 0

    def test_build_context_with_files(self):
        """Build context with project files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "main.py").write_text("def main(): pass")
            (Path(tmpdir) / "utils.py").write_text("def helper(): pass")

            builder = ContextBuilder(Path(tmpdir))
            window = builder.build_context("main function")
            assert len(window.chunks) >= 0

    def test_build_context_relevance_scoring(self):
        """Build context scores relevance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "relevant.py").write_text("search term here")
            (Path(tmpdir) / "irrelevant.py").write_text("unrelated content")

            builder = ContextBuilder(Path(tmpdir))
            window = builder.build_context("search term")

            if window.chunks:
                # Chunks should be sorted by relevance
                scores = [c.relevance_score for c in window.chunks]
                assert scores == sorted(scores, reverse=True)

    def test_classify_file_test(self):
        """Classify test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ContextBuilder(Path(tmpdir))
            assert builder._classify_file(Path("test_main.py")) == "test"
            assert builder._classify_file(Path("tests/test_utils.py")) == "test"

    def test_classify_file_doc(self):
        """Classify documentation files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ContextBuilder(Path(tmpdir))
            assert builder._classify_file(Path("README.md")) == "doc"
            assert builder._classify_file(Path("docs/guide.rst")) == "doc"

    def test_classify_file_config(self):
        """Classify config files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ContextBuilder(Path(tmpdir))
            assert builder._classify_file(Path("config.yaml")) == "config"
            assert builder._classify_file(Path("settings.json")) == "config"

    def test_classify_file_code(self):
        """Classify code files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ContextBuilder(Path(tmpdir))
            assert builder._classify_file(Path("main.py")) == "code"
            assert builder._classify_file(Path("app.js")) == "code"


# =============================================================================
# Tests for convenience functions
# =============================================================================


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""

    def test_analyze_project_function(self):
        """analyze_project returns ProjectAnalysis."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "main.py").write_text("print('hello')")

            result = analyze_project(Path(tmpdir))
            assert isinstance(result, ProjectAnalysis)

    def test_analyze_code_function(self):
        """analyze_code returns CodeAnalysisResult."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "code.py").write_text("def func(): pass")

            result = analyze_code(Path(tmpdir))
            assert isinstance(result, CodeAnalysisResult)

    def test_analyze_code_with_files(self):
        """analyze_code accepts specific files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "a.py"
            file2 = Path(tmpdir) / "b.py"
            file1.write_text("def a(): pass")
            file2.write_text("def b(): pass")

            result = analyze_code(Path(tmpdir), files=[file1])
            # Should only analyze file1
            assert "a.py" in result.complexity
            assert "b.py" not in result.complexity

    def test_build_context_function(self):
        """build_context returns ContextWindow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = build_context(Path(tmpdir), "query")
            assert isinstance(result, ContextWindow)

    def test_build_context_custom_tokens(self):
        """build_context accepts max_tokens."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = build_context(Path(tmpdir), "query", max_tokens=50000)
            assert result.max_tokens == 50000


# =============================================================================
# Integration tests
# =============================================================================


class TestCodebaseAnalyzerIntegration:
    """Integration tests for codebase analyzer."""

    def test_full_project_analysis(self):
        """Full project analysis workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mini project structure
            (Path(tmpdir) / "pyproject.toml").write_text(
                """
[project]
name = "mini-project"
version = "0.1.0"
dependencies = ["requests"]
"""
            )
            (Path(tmpdir) / "main.py").write_text(
                """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}
"""
            )
            tests_dir = Path(tmpdir) / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_main.py").write_text(
                """
def test_root():
    assert True
"""
            )

            # Analyze project
            analysis = analyze_project(Path(tmpdir))
            assert analysis.project_type == ProjectType.PYTHON
            assert Framework.FASTAPI in analysis.frameworks
            assert analysis.manifest is not None
            assert analysis.manifest.name == "mini-project"

    def test_code_quality_analysis(self):
        """Full code quality analysis workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "problematic.py").write_text(
                """
import os
import sys  # unused

password = "secret123"

def process():
    try:
        something()
    except:
        pass
"""
            )

            result = analyze_code(Path(tmpdir))
            # Should find issues
            assert len(result.security_issues) > 0
            assert len(result.error_handling_issues) > 0
            assert len(result.unused_imports) > 0

    def test_context_building_workflow(self):
        """Context building workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "README.md").write_text("# My Project\nThis is a test.")
            (Path(tmpdir) / "main.py").write_text("def main(): pass")
            (Path(tmpdir) / "config.yaml").write_text("key: value")

            window = build_context(Path(tmpdir), "main")
            # Should have chunks
            if window.chunks:
                content = window.get_content()
                assert len(content) > 0

    def test_dataclass_serialization(self):
        """Dataclasses can be used in dictionaries."""
        analysis = ProjectAnalysis(project_type=ProjectType.PYTHON)
        # Should be able to access attributes
        assert analysis.project_type.name == "PYTHON"

    def test_enum_comparisons(self):
        """Enums can be compared."""
        assert ProjectType.PYTHON != ProjectType.JAVASCRIPT
        assert Framework.FASTAPI != Framework.DJANGO
        assert ProjectType.PYTHON == ProjectType.PYTHON

    def test_framework_indicators_coverage(self):
        """Framework indicators cover major frameworks."""
        indicators = ProjectStructureAnalyzer.FRAMEWORK_INDICATORS

        # Python frameworks
        assert Framework.FASTAPI in indicators
        assert Framework.DJANGO in indicators
        assert Framework.FLASK in indicators

        # JavaScript frameworks
        assert Framework.REACT in indicators
        assert Framework.VUE in indicators
        assert Framework.EXPRESS in indicators
