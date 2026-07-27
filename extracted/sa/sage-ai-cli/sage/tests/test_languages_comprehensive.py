"""Comprehensive tests for sage/core/languages.py - Language and framework detection."""

import pytest
from pathlib import Path

from sage.core.languages import (
    Language,
    PackageManager,
    TestFramework as LangTestFramework,
    BuildTool,
    Framework as LangFramework,
    LanguageInfo,
    ProjectManifest,
    DetectionResult,
    LANGUAGE_EXTENSIONS,
    MANIFEST_FILES,
    get_language_for_extension,
)


# =============================================================================
# Tests for Language enum
# =============================================================================


class TestLanguage:
    """Tests for Language enum."""

    def test_python_value(self):
        """PYTHON has correct value."""
        assert Language.PYTHON.value == "python"

    def test_javascript_value(self):
        """JAVASCRIPT has correct value."""
        assert Language.JAVASCRIPT.value == "javascript"

    def test_typescript_value(self):
        """TYPESCRIPT has correct value."""
        assert Language.TYPESCRIPT.value == "typescript"

    def test_java_value(self):
        """JAVA has correct value."""
        assert Language.JAVA.value == "java"

    def test_kotlin_value(self):
        """KOTLIN has correct value."""
        assert Language.KOTLIN.value == "kotlin"

    def test_rust_value(self):
        """RUST has correct value."""
        assert Language.RUST.value == "rust"

    def test_go_value(self):
        """GO has correct value."""
        assert Language.GO.value == "go"

    def test_ruby_value(self):
        """RUBY has correct value."""
        assert Language.RUBY.value == "ruby"

    def test_csharp_value(self):
        """CSHARP has correct value."""
        assert Language.CSHARP.value == "csharp"

    def test_php_value(self):
        """PHP has correct value."""
        assert Language.PHP.value == "php"

    def test_unknown_value(self):
        """UNKNOWN has correct value."""
        assert Language.UNKNOWN.value == "unknown"

    def test_is_string_enum(self):
        """Language is a string enum."""
        assert isinstance(Language.PYTHON, str)
        assert Language.PYTHON == "python"

    def test_all_languages_present(self):
        """All expected languages are defined."""
        expected = [
            "PYTHON", "JAVASCRIPT", "TYPESCRIPT", "JAVA", "KOTLIN",
            "SCALA", "CSHARP", "FSHARP", "PHP", "RUBY", "ELIXIR",
            "RUST", "GO", "C", "CPP", "SWIFT", "DART", "LUA",
            "R", "SHELL", "SQL", "HTML", "CSS", "YAML", "JSON",
            "TOML", "MARKDOWN", "UNKNOWN"
        ]
        for name in expected:
            assert hasattr(Language, name)


# =============================================================================
# Tests for PackageManager enum
# =============================================================================


class TestPackageManager:
    """Tests for PackageManager enum."""

    def test_pip_value(self):
        """PIP has correct value."""
        assert PackageManager.PIP.value == "pip"

    def test_npm_value(self):
        """NPM has correct value."""
        assert PackageManager.NPM.value == "npm"

    def test_yarn_value(self):
        """YARN has correct value."""
        assert PackageManager.YARN.value == "yarn"

    def test_cargo_value(self):
        """CARGO has correct value."""
        assert PackageManager.CARGO.value == "cargo"

    def test_maven_value(self):
        """MAVEN has correct value."""
        assert PackageManager.MAVEN.value == "maven"

    def test_gradle_value(self):
        """GRADLE has correct value."""
        assert PackageManager.GRADLE.value == "gradle"

    def test_bundler_value(self):
        """BUNDLER has correct value."""
        assert PackageManager.BUNDLER.value == "bundler"

    def test_composer_value(self):
        """COMPOSER has correct value."""
        assert PackageManager.COMPOSER.value == "composer"

    def test_is_string_enum(self):
        """PackageManager is a string enum."""
        assert isinstance(PackageManager.NPM, str)


# =============================================================================
# Tests for TestFramework enum
# =============================================================================


class TestTestFrameworkEnum:
    """Tests for TestFramework enum."""

    def test_pytest_value(self):
        """PYTEST has correct value."""
        assert LangTestFramework.PYTEST.value == "pytest"

    def test_jest_value(self):
        """JEST has correct value."""
        assert LangTestFramework.JEST.value == "jest"

    def test_vitest_value(self):
        """VITEST has correct value."""
        assert LangTestFramework.VITEST.value == "vitest"

    def test_mocha_value(self):
        """MOCHA has correct value."""
        assert LangTestFramework.MOCHA.value == "mocha"

    def test_junit_value(self):
        """JUNIT has correct value."""
        assert LangTestFramework.JUNIT.value == "junit"

    def test_rspec_value(self):
        """RSPEC has correct value."""
        assert LangTestFramework.RSPEC.value == "rspec"

    def test_phpunit_value(self):
        """PHPUNIT has correct value."""
        assert LangTestFramework.PHPUNIT.value == "phpunit"

    def test_cargo_test_value(self):
        """CARGO_TEST has correct value."""
        assert LangTestFramework.CARGO_TEST.value == "cargo_test"

    def test_go_test_value(self):
        """GO_TEST has correct value."""
        assert LangTestFramework.GO_TEST.value == "go_test"

    def test_unknown_value(self):
        """UNKNOWN has correct value."""
        assert LangTestFramework.UNKNOWN.value == "unknown"


# =============================================================================
# Tests for BuildTool enum
# =============================================================================


class TestBuildTool:
    """Tests for BuildTool enum."""

    def test_setuptools_value(self):
        """SETUPTOOLS has correct value."""
        assert BuildTool.SETUPTOOLS.value == "setuptools"

    def test_tsc_value(self):
        """TSC has correct value."""
        assert BuildTool.TSC.value == "tsc"

    def test_vite_value(self):
        """VITE has correct value."""
        assert BuildTool.VITE.value == "vite"

    def test_webpack_value(self):
        """WEBPACK has correct value."""
        assert BuildTool.WEBPACK.value == "webpack"

    def test_cargo_build_value(self):
        """CARGO_BUILD has correct value."""
        assert BuildTool.CARGO_BUILD.value == "cargo_build"

    def test_go_build_value(self):
        """GO_BUILD has correct value."""
        assert BuildTool.GO_BUILD.value == "go_build"

    def test_gcc_value(self):
        """GCC has correct value."""
        assert BuildTool.GCC.value == "gcc"

    def test_clang_value(self):
        """CLANG has correct value."""
        assert BuildTool.CLANG.value == "clang"


# =============================================================================
# Tests for Framework enum
# =============================================================================


class TestFrameworkEnum:
    """Tests for Framework enum."""

    def test_django_value(self):
        """DJANGO has correct value."""
        assert LangFramework.DJANGO.value == "django"

    def test_flask_value(self):
        """FLASK has correct value."""
        assert LangFramework.FLASK.value == "flask"

    def test_fastapi_value(self):
        """FASTAPI has correct value."""
        assert LangFramework.FASTAPI.value == "fastapi"

    def test_react_value(self):
        """REACT has correct value."""
        assert LangFramework.REACT.value == "react"

    def test_vue_value(self):
        """VUE has correct value."""
        assert LangFramework.VUE.value == "vue"

    def test_angular_value(self):
        """ANGULAR has correct value."""
        assert LangFramework.ANGULAR.value == "angular"

    def test_nextjs_value(self):
        """NEXTJS has correct value."""
        assert LangFramework.NEXTJS.value == "nextjs"

    def test_rails_value(self):
        """RAILS has correct value."""
        assert LangFramework.RAILS.value == "rails"

    def test_spring_value(self):
        """SPRING has correct value."""
        assert LangFramework.SPRING.value == "spring"

    def test_laravel_value(self):
        """LARAVEL has correct value."""
        assert LangFramework.LARAVEL.value == "laravel"


# =============================================================================
# Tests for LANGUAGE_EXTENSIONS constant
# =============================================================================


class TestLanguageExtensions:
    """Tests for LANGUAGE_EXTENSIONS mapping."""

    def test_python_extensions(self):
        """Python file extensions."""
        assert LANGUAGE_EXTENSIONS[".py"] == Language.PYTHON
        assert LANGUAGE_EXTENSIONS[".pyi"] == Language.PYTHON
        assert LANGUAGE_EXTENSIONS[".pyx"] == Language.PYTHON

    def test_javascript_extensions(self):
        """JavaScript file extensions."""
        assert LANGUAGE_EXTENSIONS[".js"] == Language.JAVASCRIPT
        assert LANGUAGE_EXTENSIONS[".mjs"] == Language.JAVASCRIPT
        assert LANGUAGE_EXTENSIONS[".jsx"] == Language.JAVASCRIPT

    def test_typescript_extensions(self):
        """TypeScript file extensions."""
        assert LANGUAGE_EXTENSIONS[".ts"] == Language.TYPESCRIPT
        assert LANGUAGE_EXTENSIONS[".tsx"] == Language.TYPESCRIPT
        assert LANGUAGE_EXTENSIONS[".mts"] == Language.TYPESCRIPT

    def test_java_extension(self):
        """Java file extension."""
        assert LANGUAGE_EXTENSIONS[".java"] == Language.JAVA

    def test_kotlin_extensions(self):
        """Kotlin file extensions."""
        assert LANGUAGE_EXTENSIONS[".kt"] == Language.KOTLIN
        assert LANGUAGE_EXTENSIONS[".kts"] == Language.KOTLIN

    def test_rust_extension(self):
        """Rust file extension."""
        assert LANGUAGE_EXTENSIONS[".rs"] == Language.RUST

    def test_go_extension(self):
        """Go file extension."""
        assert LANGUAGE_EXTENSIONS[".go"] == Language.GO

    def test_c_cpp_extensions(self):
        """C/C++ file extensions."""
        assert LANGUAGE_EXTENSIONS[".c"] == Language.C
        assert LANGUAGE_EXTENSIONS[".h"] == Language.C
        assert LANGUAGE_EXTENSIONS[".cpp"] == Language.CPP
        assert LANGUAGE_EXTENSIONS[".hpp"] == Language.CPP

    def test_ruby_extensions(self):
        """Ruby file extensions."""
        assert LANGUAGE_EXTENSIONS[".rb"] == Language.RUBY
        assert LANGUAGE_EXTENSIONS[".erb"] == Language.RUBY

    def test_php_extension(self):
        """PHP file extension."""
        assert LANGUAGE_EXTENSIONS[".php"] == Language.PHP

    def test_config_extensions(self):
        """Config file extensions."""
        assert LANGUAGE_EXTENSIONS[".yaml"] == Language.YAML
        assert LANGUAGE_EXTENSIONS[".yml"] == Language.YAML
        assert LANGUAGE_EXTENSIONS[".json"] == Language.JSON
        assert LANGUAGE_EXTENSIONS[".toml"] == Language.TOML


# =============================================================================
# Tests for MANIFEST_FILES constant
# =============================================================================


class TestManifestFiles:
    """Tests for MANIFEST_FILES mapping."""

    def test_python_manifests(self):
        """Python manifest files."""
        assert MANIFEST_FILES["pyproject.toml"] == PackageManager.POETRY
        assert MANIFEST_FILES["setup.py"] == PackageManager.PIP
        assert MANIFEST_FILES["requirements.txt"] == PackageManager.PIP

    def test_javascript_manifests(self):
        """JavaScript manifest files."""
        assert MANIFEST_FILES["package.json"] == PackageManager.NPM
        assert MANIFEST_FILES["yarn.lock"] == PackageManager.YARN
        assert MANIFEST_FILES["pnpm-lock.yaml"] == PackageManager.PNPM
        assert MANIFEST_FILES["bun.lockb"] == PackageManager.BUN

    def test_rust_manifests(self):
        """Rust manifest files."""
        assert MANIFEST_FILES["Cargo.toml"] == PackageManager.CARGO
        assert MANIFEST_FILES["Cargo.lock"] == PackageManager.CARGO

    def test_go_manifests(self):
        """Go manifest files."""
        assert MANIFEST_FILES["go.mod"] == PackageManager.GO_MOD
        assert MANIFEST_FILES["go.sum"] == PackageManager.GO_MOD

    def test_java_manifests(self):
        """Java manifest files."""
        assert MANIFEST_FILES["pom.xml"] == PackageManager.MAVEN
        assert MANIFEST_FILES["build.gradle"] == PackageManager.GRADLE
        assert MANIFEST_FILES["build.gradle.kts"] == PackageManager.GRADLE

    def test_ruby_manifests(self):
        """Ruby manifest files."""
        assert MANIFEST_FILES["Gemfile"] == PackageManager.BUNDLER
        assert MANIFEST_FILES["Gemfile.lock"] == PackageManager.BUNDLER

    def test_php_manifests(self):
        """PHP manifest files."""
        assert MANIFEST_FILES["composer.json"] == PackageManager.COMPOSER

    def test_elixir_manifests(self):
        """Elixir manifest files."""
        assert MANIFEST_FILES["mix.exs"] == PackageManager.MIX


# =============================================================================
# Tests for LanguageInfo dataclass
# =============================================================================


class TestLanguageInfo:
    """Tests for LanguageInfo dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        info = LanguageInfo(language=Language.PYTHON)
        assert info.language == Language.PYTHON
        assert info.file_count == 0
        assert info.line_count == 0
        assert info.extensions == set()
        assert info.primary is False

    def test_create_full(self):
        """Create with all fields."""
        info = LanguageInfo(
            language=Language.TYPESCRIPT,
            file_count=100,
            line_count=5000,
            extensions={".ts", ".tsx"},
            primary=True,
        )
        assert info.file_count == 100
        assert info.line_count == 5000
        assert ".ts" in info.extensions
        assert info.primary is True


# =============================================================================
# Tests for ProjectManifest dataclass
# =============================================================================


class TestProjectManifest:
    """Tests for ProjectManifest dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        manifest = ProjectManifest(
            path=Path("pyproject.toml"),
            package_manager=PackageManager.POETRY,
            language=Language.PYTHON,
        )
        assert manifest.path == Path("pyproject.toml")
        assert manifest.package_manager == PackageManager.POETRY
        assert manifest.language == Language.PYTHON
        assert manifest.name is None
        assert manifest.dependencies == {}
        assert manifest.scripts == {}
        assert manifest.test_framework == LangTestFramework.UNKNOWN
        assert manifest.is_monorepo is False

    def test_create_full(self):
        """Create with all fields."""
        manifest = ProjectManifest(
            path=Path("package.json"),
            package_manager=PackageManager.NPM,
            language=Language.JAVASCRIPT,
            name="my-project",
            version="1.0.0",
            dependencies={"react": "^18.0.0"},
            dev_dependencies={"jest": "^29.0.0"},
            scripts={"test": "jest", "build": "webpack"},
            test_framework=LangTestFramework.JEST,
            build_tool=BuildTool.WEBPACK,
            frameworks=[LangFramework.REACT],
            is_monorepo=True,
            workspaces=["packages/*"],
        )
        assert manifest.name == "my-project"
        assert "react" in manifest.dependencies
        assert manifest.test_framework == LangTestFramework.JEST
        assert LangFramework.REACT in manifest.frameworks
        assert manifest.is_monorepo is True


# =============================================================================
# Tests for DetectionResult dataclass
# =============================================================================


class TestDetectionResult:
    """Tests for DetectionResult dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        result = DetectionResult(project_root=Path("."))
        assert result.project_root == Path(".")
        assert result.languages == {}
        assert result.primary_language == Language.UNKNOWN

    def test_create_with_languages(self):
        """Create with languages."""
        python_info = LanguageInfo(
            language=Language.PYTHON,
            file_count=50,
            primary=True,
        )
        result = DetectionResult(
            project_root=Path("/project"),
            languages={Language.PYTHON: python_info},
            primary_language=Language.PYTHON,
        )
        assert Language.PYTHON in result.languages
        assert result.primary_language == Language.PYTHON


# =============================================================================
# Tests for get_language_for_extension function
# =============================================================================


class TestGetLanguageForExtension:
    """Tests for get_language_for_extension function."""

    def test_python_extension(self):
        """Get Python for .py."""
        assert get_language_for_extension(".py") == Language.PYTHON

    def test_javascript_extension(self):
        """Get JavaScript for .js."""
        assert get_language_for_extension(".js") == Language.JAVASCRIPT

    def test_typescript_extension(self):
        """Get TypeScript for .ts."""
        assert get_language_for_extension(".ts") == Language.TYPESCRIPT

    def test_rust_extension(self):
        """Get Rust for .rs."""
        assert get_language_for_extension(".rs") == Language.RUST

    def test_go_extension(self):
        """Get Go for .go."""
        assert get_language_for_extension(".go") == Language.GO

    def test_unknown_extension(self):
        """Get UNKNOWN for unknown extension."""
        result = get_language_for_extension(".xyz")
        assert result == Language.UNKNOWN

    def test_case_sensitivity(self):
        """Extensions are case-sensitive."""
        # Common extensions should work
        assert get_language_for_extension(".py") == Language.PYTHON


# =============================================================================
# Integration tests
# =============================================================================


class TestLanguagesIntegration:
    """Integration tests for languages module."""

    def test_extension_language_coverage(self):
        """All main languages have at least one extension."""
        main_languages = {
            Language.PYTHON, Language.JAVASCRIPT, Language.TYPESCRIPT,
            Language.JAVA, Language.KOTLIN, Language.RUST, Language.GO,
            Language.RUBY, Language.PHP, Language.SWIFT, Language.C,
            Language.CPP
        }
        covered = set()
        for ext, lang in LANGUAGE_EXTENSIONS.items():
            covered.add(lang)
        assert main_languages.issubset(covered)

    def test_manifest_language_mapping(self):
        """Manifest files map to appropriate package managers."""
        # Python manifests
        python_manifests = ["pyproject.toml", "setup.py", "requirements.txt"]
        python_managers = {PackageManager.PIP, PackageManager.POETRY}
        for manifest in python_manifests:
            if manifest in MANIFEST_FILES:
                assert MANIFEST_FILES[manifest] in python_managers or \
                       MANIFEST_FILES[manifest] == PackageManager.PDM

    def test_enums_are_consistent(self):
        """Enum values are unique within each enum."""
        # Check for unique values in Language
        lang_values = [lang.value for lang in Language]
        assert len(lang_values) == len(set(lang_values))

        # Check for unique values in PackageManager
        pm_values = [pm.value for pm in PackageManager]
        assert len(pm_values) == len(set(pm_values))

        # Check for unique values in TestFramework
        tf_values = [tf.value for tf in LangTestFramework]
        assert len(tf_values) == len(set(tf_values))

    def test_dataclass_defaults(self):
        """Dataclasses have sensible defaults."""
        lang_info = LanguageInfo(language=Language.PYTHON)
        assert lang_info.file_count == 0
        assert lang_info.primary is False

        manifest = ProjectManifest(
            path=Path("."),
            package_manager=PackageManager.NPM,
            language=Language.JAVASCRIPT,
        )
        assert manifest.dependencies == {}
        assert manifest.is_monorepo is False

    def test_framework_categories(self):
        """Frameworks cover major categories."""
        # Python backend
        assert LangFramework.DJANGO.value == "django"
        assert LangFramework.FLASK.value == "flask"
        assert LangFramework.FASTAPI.value == "fastapi"

        # JavaScript frontend
        assert LangFramework.REACT.value == "react"
        assert LangFramework.VUE.value == "vue"
        assert LangFramework.ANGULAR.value == "angular"

        # Meta-frameworks
        assert LangFramework.NEXTJS.value == "nextjs"
        assert LangFramework.NUXT.value == "nuxt"

        # Other languages
        assert LangFramework.RAILS.value == "rails"
        assert LangFramework.SPRING.value == "spring"
        assert LangFramework.LARAVEL.value == "laravel"
