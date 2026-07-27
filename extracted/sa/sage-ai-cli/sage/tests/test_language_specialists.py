"""Tests for per-language specialists (extension of D12).

In addition to the four domain specialists (frontend/backend/devops/data),
sage now ships language-specific specialists with idiom-level guidance:
PythonSpecialist (PEP 8, async, typing), TSSpecialist (type narrowing),
RustSpecialist (ownership, traits), GoSpecialist (interfaces),
JavaSpecialist (records/streams), CSharpSpecialist (LINQ/nullables).

Each per-language specialist's prompt should:
  - mention the language by name
  - cite specific idiomatic patterns the model should follow
  - tell the model what NOT to do (common anti-patterns)
"""

from __future__ import annotations

import pytest


class TestLanguageSpecialistRegistry:

    def test_includes_python_specialist(self):
        from sage.core.specialists import language_specialists
        domains = {s.domain for s in language_specialists()}
        assert "python" in domains

    def test_includes_typescript_specialist(self):
        from sage.core.specialists import language_specialists
        domains = {s.domain for s in language_specialists()}
        assert "typescript" in domains

    def test_includes_rust_specialist(self):
        from sage.core.specialists import language_specialists
        domains = {s.domain for s in language_specialists()}
        assert "rust" in domains

    def test_includes_go_specialist(self):
        from sage.core.specialists import language_specialists
        domains = {s.domain for s in language_specialists()}
        assert "go" in domains

    def test_includes_java_specialist(self):
        from sage.core.specialists import language_specialists
        domains = {s.domain for s in language_specialists()}
        assert "java" in domains

    def test_includes_csharp_specialist(self):
        from sage.core.specialists import language_specialists
        domains = {s.domain for s in language_specialists()}
        assert "csharp" in domains


class TestPythonSpecialistDepth:

    def test_mentions_pep8(self):
        from sage.core.specialists import language_specialists
        py = next(s for s in language_specialists() if s.domain == "python")
        assert "PEP 8" in py.system_prompt or "pep 8" in py.system_prompt.lower()

    def test_mentions_typing(self):
        from sage.core.specialists import language_specialists
        py = next(s for s in language_specialists() if s.domain == "python")
        assert "type" in py.system_prompt.lower()

    def test_anti_patterns_include_mutable_default_args(self):
        from sage.core.specialists import language_specialists
        py = next(s for s in language_specialists() if s.domain == "python")
        body = py.system_prompt.lower()
        assert "mutable default" in body or "default arg" in body


class TestTypeScriptSpecialistDepth:

    def test_mentions_any_avoidance(self):
        from sage.core.specialists import language_specialists
        ts = next(s for s in language_specialists() if s.domain == "typescript")
        body = ts.system_prompt.lower()
        assert "any" in body  # warn against using `any`
        assert "type" in body

    def test_mentions_strict_mode(self):
        from sage.core.specialists import language_specialists
        ts = next(s for s in language_specialists() if s.domain == "typescript")
        body = ts.system_prompt.lower()
        assert "strict" in body


class TestRustSpecialistDepth:

    def test_mentions_ownership(self):
        from sage.core.specialists import language_specialists
        rs = next(s for s in language_specialists() if s.domain == "rust")
        body = rs.system_prompt.lower()
        assert "ownership" in body or "borrow" in body

    def test_mentions_result_over_panic(self):
        from sage.core.specialists import language_specialists
        rs = next(s for s in language_specialists() if s.domain == "rust")
        body = rs.system_prompt.lower()
        # Avoid panic in library code; prefer Result/?
        assert "result" in body or "panic" in body


class TestGoSpecialistDepth:

    def test_mentions_error_handling(self):
        from sage.core.specialists import language_specialists
        go = next(s for s in language_specialists() if s.domain == "go")
        body = go.system_prompt.lower()
        assert "error" in body
        # Should mention "if err != nil" pattern or similar
        assert "if err" in body or "errors.Is" in body or "wrap" in body

    def test_mentions_interfaces(self):
        from sage.core.specialists import language_specialists
        go = next(s for s in language_specialists() if s.domain == "go")
        body = go.system_prompt.lower()
        assert "interface" in body


class TestPolyglotPickFromStack:
    """Engine helper: given a detected stack profile, pick the right
    language specialist."""

    def test_python_stack_picks_python_specialist(self, tmp_path):
        from sage.core.specialists import pick_language_specialist
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "x"\nversion = "0.1.0"\n'
        )
        from sage.core.prompts import _stack_profile
        profile = _stack_profile(tmp_path)
        spec = pick_language_specialist(profile)
        assert spec is not None
        assert spec.domain == "python"

    def test_node_ts_stack_picks_ts_specialist(self, tmp_path):
        import json as _json
        from sage.core.specialists import pick_language_specialist
        (tmp_path / "package.json").write_text(_json.dumps({
            "name": "x", "dependencies": {"react": "^18.0.0"},
            "devDependencies": {"typescript": "^5.0.0"},
        }))
        (tmp_path / "tsconfig.json").write_text('{"compilerOptions": {}}')
        from sage.core.prompts import _stack_profile
        profile = _stack_profile(tmp_path)
        spec = pick_language_specialist(profile)
        assert spec is not None
        assert spec.domain == "typescript"

    def test_unknown_stack_returns_none(self, tmp_path):
        from sage.core.specialists import pick_language_specialist
        from sage.core.prompts import _stack_profile
        profile = _stack_profile(tmp_path)
        spec = pick_language_specialist(profile)
        assert spec is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
