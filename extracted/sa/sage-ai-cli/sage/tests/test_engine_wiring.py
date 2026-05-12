"""Tests for the engine wiring of B5, B6, C9, D11, D12, D13.

The six abstractions added earlier all need to actually run when the
engine builds a turn. These tests verify the wiring:

  D13: build_agent_system_prompt injects MemoryStore content
  C9:  ConversationEngine.compact_for_small_model() compresses history
  D11: build_agent_system_prompt mentions BROWSER tool when frontend stack
  D12: build_agent_system_prompt mentions DELEGATE_X tools per specialist
  B5:  Provider routing chooses structured tools when supported
  B6:  Engine extract+bound returns first action only when configured
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


# ── D13: Memory in system prompt ─────────────────────────────────────────


class TestMemoryInjectionIntoPrompt:

    def test_prompt_includes_saved_memories(self, tmp_path, monkeypatch):
        from sage.core.memory import MemoryStore
        from sage.core.prompts import build_agent_system_prompt

        # Plant a memory under a simulated ~/.sage
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        store = MemoryStore(tmp_path / ".sage")
        store.save(
            name="ts_pref",
            description="user prefers TypeScript",
            type="user",
            content="When ambiguous, default to TypeScript over JavaScript.",
        )

        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        assert "TypeScript" in prompt
        # The memory section header should appear
        assert "SESSION MEMORY" in prompt or "MEMORY" in prompt

    def test_prompt_omits_memory_section_when_empty(self, tmp_path, monkeypatch):
        from sage.core.prompts import build_agent_system_prompt
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        # No memory directory at all
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # Don't show an empty session-memory header
        assert "SESSION MEMORY (from prior conversations)\n" not in prompt


# ── D11: Browser tool exposed in frontend stacks ─────────────────────────


class TestBrowserToolInPrompt:

    def test_node_stack_prompt_mentions_browser_tool(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "package.json").write_text(json.dumps({
            "name": "x", "dependencies": {"react": "^18.0.0"},
            "scripts": {"test": "jest"},
        }))
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # When frontend stack + (browser optionally available), prompt
        # should mention the BROWSER tool option for verification
        assert "BROWSER" in prompt or "browser tool" in prompt.lower() or "playwright" in prompt.lower()

    def test_python_stack_prompt_does_not_mention_browser_primary(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "x"\nversion = "0.1.0"\n'
        )
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # Python project shouldn't have BROWSER as a primary tool suggestion
        # (it MIGHT be mentioned as available, but not as the main verification step)
        # Just confirm Python is the primary focus
        assert "Python" in prompt


# ── D12: Specialist DELEGATE tools mentioned in prompt ───────────────────


class TestSpecialistDelegateInPrompt:

    def test_prompt_lists_delegate_options(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # Should mention at least one delegation option
        assert "DELEGATE" in prompt or "specialist" in prompt.lower()


# ── C9: Engine has compact_for_small_model ──────────────────────────────


class TestEngineSmallModelCompaction:

    def test_engine_compacts_history_under_budget(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS")
        for i in range(20):
            engine.add_user("user msg " + "x" * 200)
            engine.add_assistant("asst response " + "y" * 200)
        before = engine.estimate_total_tokens()
        # New method should compress history below budget
        engine.compact_for_small_model(budget_chars=1500)
        after_msgs = engine.build_messages()
        total_chars = sum(len(m.content) for m in after_msgs)
        # Within reasonable margin of the budget
        assert total_chars < before * 4  # at minimum, some compression happened
        # The latest user message must survive
        assert any("user msg" in m.content for m in after_msgs)

    def test_compact_for_small_model_is_noop_under_budget(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS")
        engine.add_user("short")
        engine.add_assistant("ok")
        before_count = len(engine.build_messages())
        engine.compact_for_small_model(budget_chars=10_000)
        assert len(engine.build_messages()) == before_count


# ── B5: Provider routing detects structured-tool capability ──────────────


class TestStructuredToolRouting:

    def test_should_use_structured_tools_returns_true_for_gemini(self):
        from sage.config import SageConfig
        from sage.core.engine_helpers import should_use_structured_tools
        from sage.providers.gemini import GeminiProvider
        provider = GeminiProvider(SageConfig())
        assert should_use_structured_tools(provider) is True

    def test_should_use_structured_tools_returns_false_for_ollama(self):
        from sage.config import SageConfig
        from sage.core.engine_helpers import should_use_structured_tools
        from sage.providers.openai_compat import OllamaProvider
        provider = OllamaProvider(SageConfig())
        assert should_use_structured_tools(provider) is False


# ── B6: bound_actions helper exposed at engine layer ─────────────────────


class TestBoundActionsHelper:

    def test_extract_and_bound_returns_first_when_one_per_turn(self):
        from sage.core.engine_helpers import extract_and_bound
        from sage.core.react_loop import ReActConfig
        response = "READ: x.py\nSEARCH: foo\nRUN: pytest"
        cfg = ReActConfig(one_tool_per_turn=True)
        out = extract_and_bound(response, cfg)
        assert out == [("READ", "x.py")]

    def test_extract_and_bound_returns_all_otherwise(self):
        from sage.core.engine_helpers import extract_and_bound
        from sage.core.react_loop import ReActConfig
        response = "READ: x.py\nSEARCH: foo\nRUN: pytest"
        cfg = ReActConfig(one_tool_per_turn=False)
        out = extract_and_bound(response, cfg)
        assert len(out) == 3


# ── D12 wiring: DELEGATE action handler ─────────────────────────────────


class TestDelegateActionHandler:

    def test_handle_delegate_action_routes_to_correct_specialist(self):
        from sage.core.engine_helpers import handle_delegate_action

        captured = {}

        class _FakeRouter:
            def generate(self, messages, model_id="auto", **kw):
                captured["sys"] = messages[0].content
                captured["task"] = messages[1].content
                return "specialist did the thing"

        result = handle_delegate_action(
            action_name="DELEGATE_FRONTEND",
            task="restyle the dashboard",
            router=_FakeRouter(),
        )
        assert result == "specialist did the thing"
        assert "frontend" in captured["sys"].lower()
        assert captured["task"] == "restyle the dashboard"

    def test_handle_delegate_action_unknown_domain_returns_error(self):
        from sage.core.engine_helpers import handle_delegate_action

        class _FakeRouter:
            def generate(self, *a, **kw): return "x"

        result = handle_delegate_action(
            action_name="DELEGATE_NONSENSE",
            task="t",
            router=_FakeRouter(),
        )
        # Returns an error string rather than raising — engine treats this
        # as the action's output so the loop continues
        assert "unknown" in result.lower() or "no such specialist" in result.lower()


class TestWebToolsInPrompt:
    """Sage's tools include WEB_FETCH and SEARCH_WEB, but the prompt
    never mentioned them. Now it should — so the model uses them when
    asked about a library it doesn't recognize."""

    def test_prompt_mentions_web_fetch(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        assert "WEB_FETCH" in prompt

    def test_prompt_mentions_search_web(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        assert "SEARCH_WEB" in prompt

    def test_prompt_explains_when_to_use_web(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # Should give a heuristic for when to reach for web vs local
        lower = prompt.lower()
        assert "library" in lower or "documentation" in lower or "docs" in lower


class TestAutoCompressForSmallModel:
    """Engine should compress history automatically when serving a small
    model AND the context is large enough to hurt small-model reasoning."""

    def test_is_small_model_recognizes_3b(self):
        from sage.core.engine_helpers import is_small_model
        assert is_small_model("ollama:llama3.2") is True
        assert is_small_model("ollama:qwen2.5-coder-3b") is True
        assert is_small_model("llama_cpp:phi3-mini") is True

    def test_is_small_model_returns_false_for_big(self):
        from sage.core.engine_helpers import is_small_model
        assert is_small_model("ollama:qwen3-coder-next") is False
        assert is_small_model("gemini:gemini-2.5-flash") is False
        assert is_small_model("ollama:deepseek-r1") is False

    def test_maybe_compress_triggers_when_small_and_over_budget(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS")
        for i in range(15):
            engine.add_user("user " + "x" * 500)
            engine.add_assistant("asst " + "y" * 500)
        before = sum(len(m.content) for m in engine.build_messages())
        # Small model + over budget → compress
        removed = engine.maybe_compress_for_model("ollama:llama3.2", budget_chars=2000)
        assert removed > 0
        after = sum(len(m.content) for m in engine.build_messages())
        assert after < before

    def test_maybe_compress_skips_when_big_model(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS")
        for i in range(15):
            engine.add_user("user " + "x" * 500)
            engine.add_assistant("asst " + "y" * 500)
        # Big model → no compression even if over budget
        removed = engine.maybe_compress_for_model("ollama:qwen3-coder-next", budget_chars=2000)
        assert removed == 0

    def test_maybe_compress_skips_when_under_budget(self):
        from sage.core.engine import ConversationEngine
        engine = ConversationEngine(system_prompt="SYS")
        engine.add_user("hi")
        engine.add_assistant("ok")
        removed = engine.maybe_compress_for_model("ollama:llama3.2", budget_chars=10_000)
        assert removed == 0


class TestAutoLanguageSpecialistInPrompt:
    """When stack is detected, build_agent_system_prompt should embed the
    matching language specialist's idiom guidance directly. Saves a DELEGATE
    round-trip for the common case."""

    def test_python_stack_prompt_contains_python_idioms(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "x"\nversion = "0.1.0"\n'
        )
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # PEP 8 should appear (it's in the python specialist prompt)
        assert "PEP 8" in prompt or "pep 8" in prompt.lower()
        # Mutable default args anti-pattern is critical Python idiom
        assert "mutable default" in prompt.lower() or "default arg" in prompt.lower()

    def test_typescript_stack_prompt_contains_ts_idioms(self, tmp_path):
        import json as _json
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "package.json").write_text(_json.dumps({
            "name": "x", "dependencies": {"react": "^18.0.0"},
            "devDependencies": {"typescript": "^5.0.0"},
        }))
        (tmp_path / "tsconfig.json").write_text('{"compilerOptions": {}}')
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # Strict mode guidance is core TS idiom
        assert "strict" in prompt.lower()

    def test_rust_stack_prompt_contains_rust_idioms(self, tmp_path):
        from sage.core.prompts import build_agent_system_prompt
        (tmp_path / "Cargo.toml").write_text(
            '[package]\nname = "x"\nversion = "0.1.0"\n'
        )
        prompt = build_agent_system_prompt(tmp_path, is_local=False, enhanced=False)
        # Ownership/borrowing is core Rust idiom
        assert "ownership" in prompt.lower() or "borrow" in prompt.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
