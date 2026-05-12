"""Tests for stack-aware prompt construction (Bug 2/A1, A2, A3, A4, B7).

The model used to default to Python regardless of project stack because:
  - The system prompt's examples are all `pytest`/`*.py` (line ~142, ~170-183, ~710-721)
  - No detected-stack context was injected into the prompt

These tests pin the contract that:
  - `build_stack_context(cwd)` returns a section naming the detected stack
  - The full agent prompt incorporates stack-specific test/build commands
  - For greenfield directories, the prompt mandates asking before defaulting
  - A "detect-first" rule blocks FILE: actions before reading the manifest
  - A "verification gate" requires running the project's test command before claiming done
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


# ── Stack-context primitive ──────────────────────────────────────────────


class TestBuildStackContext:
    """`build_stack_context(cwd)` returns a markdown section describing the
    detected stack so the model knows what language/commands to use."""

    def test_detects_node_react_project(self, tmp_path):
        from sage.core.prompts import build_stack_context
        (tmp_path / "package.json").write_text(json.dumps({
            "name": "petsapp",
            "dependencies": {"react": "^18.0.0", "react-dom": "^18.0.0"},
            "devDependencies": {"jest": "^29.0.0", "vite": "^5.0.0"},
            "scripts": {"test": "jest", "build": "vite build", "dev": "vite"},
        }))
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "App.jsx").write_text("export default function App() { return null }\n")
        ctx = build_stack_context(tmp_path)
        assert "JavaScript" in ctx or "Node" in ctx
        # Must NOT advise pytest as the test command for a Node project
        assert "pytest" not in ctx.lower()

    def test_detects_python_project(self, tmp_path):
        from sage.core.prompts import build_stack_context
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "petsapp"\nversion = "0.1.0"\n'
        )
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "app.py").write_text("def main():\n    pass\n")
        ctx = build_stack_context(tmp_path)
        assert "Python" in ctx

    def test_detects_rust_project(self, tmp_path):
        from sage.core.prompts import build_stack_context
        (tmp_path / "Cargo.toml").write_text(
            '[package]\nname = "petsapp"\nversion = "0.1.0"\n'
        )
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.rs").write_text("fn main() {}\n")
        ctx = build_stack_context(tmp_path)
        assert "Rust" in ctx
        assert "cargo" in ctx.lower()

    def test_greenfield_directory_says_unknown(self, tmp_path):
        from sage.core.prompts import build_stack_context
        # Empty directory — no manifests
        ctx = build_stack_context(tmp_path)
        # Should NOT positively claim the stack IS Python or Node.
        # The phrase "Do NOT default to Python" is allowed — it's a guardrail.
        assert "Detected stack: Python" not in ctx
        assert "Detected stack: Node" not in ctx
        assert "Primary language: Python" not in ctx
        # Should explicitly say it's undetected and tell the model to ask
        assert any(
            phrase in ctx.lower()
            for phrase in ("unknown", "no manifest", "no project files", "ask the user", "undetected")
        )


# ── Full agent system prompt incorporates stack context ──────────────────


class TestAgentPromptIncorporatesStack:

    def test_node_project_prompt_mentions_npm(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "package.json").write_text(json.dumps({
            "name": "x", "scripts": {"test": "jest"},
            "dependencies": {"react": "^18.0.0"},
        }))
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # The rendered prompt for a Node project should mention npm/jest
        assert "npm" in prompt.lower() or "jest" in prompt.lower()

    def test_python_project_prompt_keeps_python_commands(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "x"\nversion = "0.1.0"\n'
        )
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "x.py").write_text("def f(): return 1\n")
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        assert "Python" in prompt

    def test_greenfield_prompt_demands_clarification(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # The prompt must tell the model to ASK before defaulting to Python
        lower = prompt.lower()
        assert (
            "ask the user" in lower
            or "do not default to python" in lower
            or "no manifest" in lower
            or "undetected" in lower
        )


# ── A3: Conditional TDD ──────────────────────────────────────────────────


class TestConditionalTDD:

    def test_greenfield_advises_spike_first(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        # Empty directory — no existing tests
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        lower = prompt.lower()
        # Should NOT mandate writing-failing-test-first as the only path
        assert "spike" in lower or "prototype" in lower or "working spike" in lower

    def test_project_with_existing_tests_keeps_tdd(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        # Project with an existing test suite — TDD discipline still applies
        (tmp_path / "package.json").write_text(json.dumps({
            "name": "x", "scripts": {"test": "jest"},
            "dependencies": {"react": "^18.0.0"},
            "devDependencies": {"jest": "^29.0.0"},
        }))
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "app.test.js").write_text(
            "test('it works', () => expect(1).toBe(1));\n"
        )
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # TDD discipline still expected when tests already exist
        assert "TDD" in prompt or "test-driven" in prompt.lower()


# ── A4: DETECT-FIRST rule ────────────────────────────────────────────────


class TestDetectFirstRule:

    def test_prompt_mandates_reading_manifest_before_file_writes(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "package.json").write_text("{}")
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        lower = prompt.lower()
        # Must explicitly require reading manifest before generating code
        assert (
            "read" in lower and "package.json" in lower
            or "detect" in lower and "before" in lower and "file:" in lower
        )


# ── B7: Verification gate ────────────────────────────────────────────────


class TestVerificationGate:

    def test_prompt_requires_running_tests_before_claiming_done(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "package.json").write_text(json.dumps({
            "name": "x", "scripts": {"test": "jest"},
            "devDependencies": {"jest": "^29.0.0"},
        }))
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        lower = prompt.lower()
        # Some explicit verification language must be present
        assert (
            ("before" in lower and "done" in lower and ("test" in lower or "verify" in lower))
            or "verification gate" in lower
            or "must run" in lower and "test" in lower
        )


# ── Strong integration tests: prompt is *consistent*, not contradictory ──


class TestPromptConsistency:
    """The original prompt template hardcodes pytest examples throughout.
    The stack-context section adds correct guidance, but if the surrounding
    template still shows `RUN: pytest` 17 times, the model will pattern-match
    on whichever is more frequent. These tests pin that the FULL rendered
    prompt is consistent with the detected stack — no contradictory examples."""

    def test_node_prompt_does_not_show_pytest_as_primary_test_command(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "package.json").write_text(json.dumps({
            "name": "x", "scripts": {"test": "jest"},
            "dependencies": {"react": "^18.0.0"},
            "devDependencies": {"jest": "^29.0.0"},
        }))
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # Count pytest references. A few is OK (historical context, edge-case
        # mentions). 10+ means the template is pattern-priming the model toward
        # Python even though the project is Node.
        pytest_count = prompt.lower().count("pytest")
        assert pytest_count < 5, (
            f"Node-project prompt mentions pytest {pytest_count} times — "
            "model will pattern-match on Python despite stack section. "
            "Template hardcoded pytest examples must be made stack-aware."
        )
        # And npm/jest should be at least as prominent as the test_cmd.
        assert (prompt.lower().count("npm") + prompt.lower().count("jest")) >= 2

    def test_python_prompt_does_not_show_jest_as_primary_test_command(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "x"\nversion = "0.1.0"\n'
            '[tool.pytest.ini_options]\ntestpaths = ["tests"]\n'
        )
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        jest_count = prompt.lower().count("jest")
        assert jest_count < 3, (
            f"Python-project prompt mentions jest {jest_count} times — "
            "should be Python-focused."
        )


class TestPolyglotCoverage:
    """Sage should recognize and emit correct commands for a wider set of
    languages than just Python + Node + Rust + Go."""

    def test_detects_csharp_dotnet_project(self, tmp_path):
        from sage.core.prompts import build_stack_context
        (tmp_path / "MyApp.csproj").write_text(
            '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
            '<TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>'
        )
        ctx = build_stack_context(tmp_path)
        assert "C#" in ctx or ".NET" in ctx
        assert "dotnet test" in ctx.lower()

    def test_detects_php_composer_project(self, tmp_path):
        from sage.core.prompts import build_stack_context
        (tmp_path / "composer.json").write_text(
            '{"name": "vendor/app", "require": {"php": ">=8.0"}}'
        )
        ctx = build_stack_context(tmp_path)
        assert "PHP" in ctx
        assert "composer" in ctx.lower() or "phpunit" in ctx.lower()

    def test_detects_swift_package(self, tmp_path):
        from sage.core.prompts import build_stack_context
        (tmp_path / "Package.swift").write_text(
            '// swift-tools-version:5.9\nimport PackageDescription\n'
            'let package = Package(name: "MyApp")\n'
        )
        ctx = build_stack_context(tmp_path)
        assert "Swift" in ctx
        assert "swift test" in ctx.lower() or "swift build" in ctx.lower()

    def test_detects_typescript_over_javascript(self, tmp_path):
        """When tsconfig.json is present, language should be TypeScript not JS."""
        import json
        from sage.core.prompts import build_stack_context
        (tmp_path / "package.json").write_text(json.dumps({
            "name": "x", "scripts": {"test": "jest"},
            "dependencies": {"react": "^18.0.0"},
            "devDependencies": {"typescript": "^5.0.0"},
        }))
        (tmp_path / "tsconfig.json").write_text('{"compilerOptions": {}}')
        ctx = build_stack_context(tmp_path)
        assert "TypeScript" in ctx


class TestStackContextPlacementMatters:
    """Stack guidance should appear EARLY in the prompt, before the long
    template body — recency-weighting in attention favors earlier content
    when there's contradiction later."""

    def test_stack_section_appears_in_first_third_of_prompt(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "package.json").write_text(json.dumps({
            "name": "x", "scripts": {"test": "jest"},
            "dependencies": {"react": "^18.0.0"},
        }))
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        stack_idx = prompt.find("# PROJECT STACK (DETECTED FROM CWD)")
        assert stack_idx >= 0, "stack section not in rendered prompt"
        # Stack section appears in first third
        assert stack_idx < len(prompt) // 3, (
            f"Stack section starts at char {stack_idx} of {len(prompt)} — "
            "should be earlier so the model sees it before contradicting examples."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
