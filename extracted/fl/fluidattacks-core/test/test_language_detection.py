"""Test cases for the improved language detection logic."""

from fluidattacks_core.filesystem import Language, _detect_languages_in_dir, _get_language_conflicts


def test_typescript_vs_javascript_conflict() -> None:
    """Test that TypeScript has priority over JavaScript."""
    # TypeScript + JavaScript files
    files = ["package.json", "tsconfig.json", "webpack.config.js", "src/index.ts"]
    result = _detect_languages_in_dir(files)

    assert Language.TypeScript in result
    assert Language.JavaScript not in result
    assert len(result) == 1


def test_kotlin_vs_java_conflict() -> None:
    """Test that Kotlin has priority over Java."""
    # Kotlin + Java files
    files = ["pom.xml", "build.gradle.kts", "settings.gradle.kts", "src/main/kotlin/App.kt"]
    result = _detect_languages_in_dir(files)

    assert Language.Kotlin in result
    assert Language.Java not in result
    assert len(result) == 1


def test_rust_vs_c_conflict() -> None:
    """Test that Rust has priority over C."""
    # Rust + C files
    files = ["Cargo.toml", "Cargo.lock", "main.c", "lib.h"]
    result = _detect_languages_in_dir(files)

    assert Language.Rust in result
    assert Language.C not in result
    assert len(result) == 1


def test_scala_vs_java_conflict() -> None:
    """Test that Scala has priority over Java."""
    # Scala + Java files
    files = ["pom.xml", "build.sbt", "project/build.properties", "src/main/scala/App.scala"]
    result = _detect_languages_in_dir(files)

    assert Language.Scala in result
    assert Language.Java not in result
    assert len(result) == 1


def test_dart_vs_javascript_conflict() -> None:
    """Test that Dart has priority over JavaScript."""
    # Dart + JavaScript files
    files = ["package.json", "pubspec.yaml", "pubspec.lock", "lib/main.dart"]
    result = _detect_languages_in_dir(files)

    assert Language.Dart in result
    assert Language.JavaScript not in result
    assert len(result) == 1


def test_pure_javascript_detection() -> None:
    """Test detection of pure JavaScript project (no TypeScript)."""
    files = ["package.json", "webpack.config.js", "babel.config.js", "src/index.js"]
    result = _detect_languages_in_dir(files)

    assert Language.JavaScript in result
    assert Language.TypeScript not in result
    assert len(result) == 1


def test_pure_typescript_detection() -> None:
    """Test detection of pure TypeScript project."""
    files = ["tsconfig.json", "tsconfig.app.json", "src/index.ts", "src/types.ts"]
    result = _detect_languages_in_dir(files)

    assert Language.TypeScript in result
    assert len(result) == 1


def test_multiple_non_conflicting_languages() -> None:
    """Test detection of multiple non-conflicting languages."""
    files = ["package.json", "tsconfig.json", "Cargo.toml", "go.mod", "pyproject.toml"]
    result = _detect_languages_in_dir(files)

    # Should detect all non-conflicting languages
    expected_languages = {Language.TypeScript, Language.Rust, Language.Go, Language.Python}
    assert set(result) == expected_languages


def test_python_high_confidence() -> None:
    """Test Python detection with multiple config files (high confidence)."""
    files = ["pyproject.toml", "requirements.txt", "setup.py", "tox.ini", "pytest.ini"]
    result = _detect_languages_in_dir(files)

    assert Language.Python in result
    assert len(result) == 1


def test_go_detection() -> None:
    """Test Go project detection."""
    files = ["go.mod", "go.sum", "main.go"]
    result = _detect_languages_in_dir(files)

    assert Language.Go in result
    assert len(result) == 1


def test_confidence_scoring_exact_vs_glob() -> None:
    """Test that exact matches have higher confidence than glob matches."""
    # Files that match both exact and glob patterns
    files = ["package.json", "webpack.config.js", "babel.config.js"]
    result = _detect_languages_in_dir(files)

    assert Language.JavaScript in result
    assert len(result) == 1


def test_empty_files_list() -> None:
    """Test detection with empty files list."""
    result = _detect_languages_in_dir([])
    assert result == []


def test_unknown_language_files() -> None:
    """Test detection with files that don't match any language."""
    files = ["random.txt", "unknown.xyz", "mystery.file"]
    result = _detect_languages_in_dir(files)
    assert result == []


def test_case_insensitive_detection() -> None:
    """Test that detection is case-insensitive."""
    files = ["PACKAGE.JSON", "TSCONFIG.JSON", "WEBPACK.CONFIG.JS"]
    result = _detect_languages_in_dir(files)

    assert Language.TypeScript in result
    assert Language.JavaScript not in result


def test_glob_pattern_matching() -> None:
    """Test glob pattern matching for configuration files."""
    files = ["tsconfig.app.json", "tsconfig.build.json", "tsconfig.test.json"]
    result = _detect_languages_in_dir(files)

    assert Language.TypeScript in result
    assert len(result) == 1


def test_java_spring_boot_detection() -> None:
    """Test Java Spring Boot project detection."""
    files = ["pom.xml", "application.yml", "application-dev.yml", "logback.xml"]
    result = _detect_languages_in_dir(files)

    assert Language.Java in result
    assert len(result) == 1


def test_php_laravel_detection() -> None:
    """Test PHP Laravel project detection."""
    files = ["composer.json", "composer.lock", "artisan", "config/app.php"]
    result = _detect_languages_in_dir(files)

    assert Language.PHP in result
    assert len(result) == 1


def test_ruby_rails_detection() -> None:
    """Test Ruby Rails project detection."""
    files = ["Gemfile", "Gemfile.lock", "Rakefile", "config.ru", "database.yml"]
    result = _detect_languages_in_dir(files)

    assert Language.Ruby in result
    assert len(result) == 1


def test_csharp_dotnet_detection() -> None:
    """Test C# .NET project detection."""
    files = ["MyProject.sln", "MyProject.csproj", "packages.config", "appsettings.json"]
    result = _detect_languages_in_dir(files)

    assert Language.CSharp in result
    assert len(result) == 1


def test_swift_ios_detection() -> None:
    """Test Swift iOS project detection."""
    files = ["Package.swift", "Package.resolved", "Info.plist", "project.pbxproj"]
    result = _detect_languages_in_dir(files)

    assert Language.Swift in result
    assert len(result) == 1


# Language conflict tests
def test_typescript_conflicts() -> None:
    """Test TypeScript conflict detection."""
    conflicts = _get_language_conflicts(Language.TypeScript)
    assert Language.JavaScript in conflicts


def test_javascript_conflicts() -> None:
    """Test JavaScript conflict detection."""
    conflicts = _get_language_conflicts(Language.JavaScript)
    assert Language.TypeScript in conflicts
    assert Language.Dart in conflicts


def test_kotlin_conflicts() -> None:
    """Test Kotlin conflict detection."""
    conflicts = _get_language_conflicts(Language.Kotlin)
    assert Language.Java in conflicts
    assert Language.Scala in conflicts


def test_java_conflicts() -> None:
    """Test Java conflict detection."""
    conflicts = _get_language_conflicts(Language.Java)
    assert Language.Kotlin in conflicts
    assert Language.Scala in conflicts


def test_rust_conflicts() -> None:
    """Test Rust conflict detection."""
    conflicts = _get_language_conflicts(Language.Rust)
    assert Language.C in conflicts


def test_c_conflicts() -> None:
    """Test C conflict detection."""
    conflicts = _get_language_conflicts(Language.C)
    assert Language.Rust in conflicts


def test_scala_conflicts() -> None:
    """Test Scala conflict detection."""
    conflicts = _get_language_conflicts(Language.Scala)
    assert Language.Java in conflicts
    assert Language.Kotlin in conflicts


def test_dart_conflicts() -> None:
    """Test Dart conflict detection."""
    conflicts = _get_language_conflicts(Language.Dart)
    assert Language.JavaScript in conflicts


def test_python_no_conflicts() -> None:
    """Test that Python has no conflicts."""
    conflicts = _get_language_conflicts(Language.Python)
    assert conflicts == set()


def test_go_no_conflicts() -> None:
    """Test that Go has no conflicts."""
    conflicts = _get_language_conflicts(Language.Go)
    assert conflicts == set()


def test_php_no_conflicts() -> None:
    """Test that PHP has no conflicts."""
    conflicts = _get_language_conflicts(Language.PHP)
    assert conflicts == set()


def test_ruby_no_conflicts() -> None:
    """Test that Ruby has no conflicts."""
    conflicts = _get_language_conflicts(Language.Ruby)
    assert conflicts == set()


def test_csharp_no_conflicts() -> None:
    """Test that C# has no conflicts."""
    conflicts = _get_language_conflicts(Language.CSharp)
    assert conflicts == set()


def test_swift_no_conflicts() -> None:
    """Test that Swift has no conflicts."""
    conflicts = _get_language_conflicts(Language.Swift)
    assert conflicts == set()


# Edge cases tests
def test_mixed_case_filenames() -> None:
    """Test detection with mixed case filenames."""
    files = ["Package.json", "TSCONFIG.json", "webpack.CONFIG.js"]
    result = _detect_languages_in_dir(files)

    assert Language.TypeScript in result
    assert Language.JavaScript not in result


def test_duplicate_filenames() -> None:
    """Test detection with duplicate filenames."""
    files = ["package.json", "package.json", "tsconfig.json"]
    result = _detect_languages_in_dir(files)

    assert Language.TypeScript in result
    assert Language.JavaScript not in result


def test_very_long_filename_list() -> None:
    """Test detection with a very long list of files."""
    files = [f"file{i}.txt" for i in range(1000)] + ["package.json", "tsconfig.json"]
    result = _detect_languages_in_dir(files)

    assert Language.TypeScript in result
    assert Language.JavaScript not in result


def test_special_characters_in_filenames() -> None:
    """Test detection with special characters in filenames."""
    files = ["package.json", "tsconfig.json", "file with spaces.txt", "file-with-dashes.txt"]
    result = _detect_languages_in_dir(files)

    assert Language.TypeScript in result
    assert Language.JavaScript not in result


def test_unicode_filenames() -> None:
    """Test detection with unicode filenames."""
    files = ["package.json", "tsconfig.json", "файл.txt", "文件.txt"]
    result = _detect_languages_in_dir(files)

    assert Language.TypeScript in result
    assert Language.JavaScript not in result
