import os
import shutil
import pytest
from pathlib import Path
from sage.core.discovery import FileDiscovery
from sage.core.install_verify import verify_project, DiscoveredProject
from sage.core.content_validator import validate_content
from sage.core.prompts import build_agent_system_prompt, _stack_profile



def test_detect_multi_language_projects(tmp_path):
    """Verify that FileDiscovery correctly detects Java, Kotlin, Ruby, Swift, Dart, C++, and C# projects."""
    discovery = FileDiscovery(tmp_path)
    
    # 1. Java (Maven)
    java_mvn = tmp_path / "java_mvn"
    java_mvn.mkdir()
    (java_mvn / "pom.xml").write_text("<project></project>")
    
    # 2. Kotlin (Gradle)
    kotlin_gradle = tmp_path / "kotlin_gradle"
    kotlin_gradle.mkdir()
    (kotlin_gradle / "build.gradle.kts").write_text("")
    
    # 3. Ruby
    ruby_proj = tmp_path / "ruby_proj"
    ruby_proj.mkdir()
    (ruby_proj / "Gemfile").write_text("")
    
    # 4. Swift
    swift_proj = tmp_path / "swift_proj"
    swift_proj.mkdir()
    (swift_proj / "Package.swift").write_text("")
    
    # 5. Dart
    dart_proj = tmp_path / "dart_proj"
    dart_proj.mkdir()
    (dart_proj / "pubspec.yaml").write_text("name: my_app")
    
    # 6. C++
    cpp_proj = tmp_path / "cpp_proj"
    cpp_proj.mkdir()
    (cpp_proj / "CMakeLists.txt").write_text("")
    
    # 7. C#
    csharp_proj = tmp_path / "csharp_proj"
    csharp_proj.mkdir()
    (csharp_proj / "myproj.csproj").write_text("")
    
    projects = discovery.discover_projects()
    types = {p.type for p in projects}
    
    assert "java" in types
    assert "kotlin" in types
    assert "ruby" in types
    assert "swift" in types
    assert "dart" in types
    assert "cpp" in types
    assert "csharp" in types


def test_new_language_verifiers(monkeypatch):
    """Each language verifier emits the right install/build steps AND refuses
    to report tests_ok=True for a project that has no tests.

    `shutil.which` is stubbed so the toolchain-detection branch is taken for
    every language even on a machine that lacks the SDK. The commands then
    really run against a non-existent directory and really fail — which is
    the honest outcome and what this test asserts. Nothing is mocked into
    reporting success.
    """
    from sage.core.install_verify import VerifyReport
    monkeypatch.setattr(shutil, "which", lambda cmd: f"/usr/bin/{cmd}")

    expectations = [
        ("swift", ("swift build",)),
        ("csharp", ("dotnet build",)),
        ("ruby", ("bundle install",)),
        ("dart", ("dart pub get", "flutter pub get")),
    ]
    for kind, expected_step_names in expectations:
        project = DiscoveredProject(kind=kind, root=Path("/tmp/does_not_exist_sage_probe"))
        steps = verify_project(project)
        report = VerifyReport(project=project, steps=steps)
        names = [s.name for s in steps]

        assert any(n in expected_step_names for n in names), (
            f"{kind}: expected one of {expected_step_names} in {names}"
        )
        # A directory that does not exist cannot have a passing test suite.
        assert report.tests_ok is False, (
            f"{kind}: tests_ok must be False for a non-existent project, "
            f"got steps={[(s.name, s.ok) for s in steps]}"
        )


def test_nested_github_path_validator():
    """Verify that validate_content rejects writing a .github folder inside a subdirectory."""
    # Root level is fine
    res_ok = validate_content(".github/workflows/ci.yml", "name: CI")
    assert res_ok.ok is True
    
    # Nested under backend/ is NOT fine
    res_nested = validate_content("backend/.github/workflows/ci.yml", "name: CI")
    assert res_nested.ok is False
    assert res_nested.signal == "nested_config"
    assert "All `.github` configuration folders must be placed at the project root" in res_nested.reason


def test_prompt_enhancements_and_stack_profile(tmp_path):
    """Verify stack profile detection for C++ and Dart/Flutter and check system prompt instructions."""
    # 1. Test Dart/Flutter profile detection
    dart_dir = tmp_path / "dart_proj"
    dart_dir.mkdir()
    pubspec = dart_dir / "pubspec.yaml"
    pubspec.write_text("name: test_app\ndependencies:\n  flutter:\n    sdk: flutter")
    
    profile_dart = _stack_profile(dart_dir)
    assert profile_dart["name"] == "Flutter"
    assert profile_dart["language"] == "Dart"
    assert profile_dart["package_manager"] == "pub"
    assert profile_dart["test_cmd"] == "flutter test"
    
    # 2. Test CMake profile detection
    cpp_dir = tmp_path / "cpp_proj"
    cpp_dir.mkdir()
    (cpp_dir / "CMakeLists.txt").write_text("project(TestCpp)")
    
    profile_cpp = _stack_profile(cpp_dir)
    assert profile_cpp["name"] == "C++ (CMake)"
    assert profile_cpp["language"] == "C++"
    assert profile_cpp["package_manager"] == "cmake"
    assert profile_cpp["test_cmd"] == "ctest"
    
    # 3. Test Makefile profile detection
    make_dir = tmp_path / "make_proj"
    make_dir.mkdir()
    (make_dir / "Makefile").write_text("test:\n\tctest")
    
    profile_make = _stack_profile(make_dir)
    assert profile_make["name"] == "C++ (Make)"
    assert profile_make["language"] == "C++"
    assert profile_make["package_manager"] == "make"
    
    # 4. Check system prompt contains the Playbook Guidelines
    prompt_normal = build_agent_system_prompt(tmp_path, is_local=False)
    prompt_local = build_agent_system_prompt(tmp_path, is_local=True)
    
    # Check that both prompts contain the playbook guidelines
    for prompt in (prompt_normal, prompt_local):
        assert "PLAYBOOK GUIDELINES" in prompt
        assert "Zero-Stub Policy" in prompt
        assert "Template-Free Generation" in prompt
        assert "CI/CD and Infrastructure Scaffolding" in prompt
        assert "Self-Assessment Post-Mortem" in prompt
        assert "Root-Level Configuration Guardrails" in prompt


def test_bun_and_pythonpath_verification(tmp_path, monkeypatch):
    """Verify Bun detection and PYTHONPATH environment generation in verifiers."""
    monkeypatch.setattr(shutil, "which", lambda cmd: f"/usr/bin/{cmd}" if cmd in {"bun", "python", "pytest"} else None)

    # 1. Node/Bun project
    node_dir = tmp_path / "node_proj"
    node_dir.mkdir()
    (node_dir / "package.json").write_text('{"name": "test", "scripts": {"test": "bun test"}}')
    (node_dir / "bun.lockb").write_text("")
    # A real test file must exist for a test step to be emitted at all: the
    # verifier refuses to run (or claim) a suite that does not exist.
    (node_dir / "index.test.ts").write_text(
        'import { test, expect } from "bun:test";\n'
        'test("adds", () => { expect(1 + 1).toBe(2); });\n'
    )

    node_project = DiscoveredProject(kind="node", root=node_dir)
    steps = verify_project(node_project)
    
    assert any(s.name == "bun install" for s in steps)
    assert any(s.name == "bun test" for s in steps)

    # 2. Python project with nested app folder
    py_dir = tmp_path / "py_proj"
    py_dir.mkdir()
    (py_dir / "requirements.txt").write_text("")
    (py_dir / "app").mkdir()
    (py_dir / "app" / "main.py").write_text("")

    py_project = DiscoveredProject(kind="python", root=py_dir)
    steps = verify_project(py_project)

    assert len(steps) >= 4
    assert any(s.name == "python compile" for s in steps)
    assert any(s.name == "python import check" for s in steps)


