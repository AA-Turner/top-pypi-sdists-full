"""TDD tests for Tier 1 quality gates: T1, T3, T4, T12.

T1: Hard model-capability floor — refuse agentic tasks below 7B params
T3: Bounded regenerate context — only failing file + error tail + RAG, not full history
T4: Strict GBNF on tool-call turns — protocol grammar enforced by default
T12: Project-aware grammar — hallucinated imports become impossible
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest


# ════════════════════════════════════════════════════════════════════════
# T1: Model-capability floor
# ════════════════════════════════════════════════════════════════════════

def test_estimate_params_from_name_recognizes_common_sizes():
    from sage.core.model_floor import estimate_params_b
    # Bare numeric sizes
    assert estimate_params_b("llama3.2-3b") == pytest.approx(3.0)
    assert estimate_params_b("qwen2.5-coder-7b") == pytest.approx(7.0)
    assert estimate_params_b("llama3.3-70b") == pytest.approx(70.0)
    # MoE family / cloud-style names
    assert estimate_params_b("qwen3-coder-next") >= 30.0  # known cloud-tier coder
    # Tag suffix shouldn't matter
    assert estimate_params_b("ollama:llama3.2:latest") == pytest.approx(3.0)


def test_estimate_params_unknown_returns_none():
    from sage.core.model_floor import estimate_params_b
    assert estimate_params_b("totally-unknown-model") is None


def test_passes_floor_returns_true_when_at_or_above_7b():
    from sage.core.model_floor import passes_floor
    assert passes_floor("ollama:qwen2.5-coder-7b") is True
    assert passes_floor("ollama:qwen3-coder-next") is True
    assert passes_floor("llama_cpp:llama3.3-70b") is True


def test_passes_floor_returns_false_for_3b_models():
    from sage.core.model_floor import passes_floor
    assert passes_floor("ollama:llama3.2") is False
    assert passes_floor("llama_cpp:llama3.2-3b") is False


def test_passes_floor_unknown_models_default_to_pass():
    """Don't block users running custom or unknown models."""
    from sage.core.model_floor import passes_floor
    assert passes_floor("mystery-model") is True


def test_check_capability_returns_actionable_message_below_floor():
    from sage.core.model_floor import check_capability
    result = check_capability("ollama:llama3.2", task_kind="agentic")
    assert result.ok is False
    assert "qwen2.5-coder-7b" in result.suggestion or "7b" in result.suggestion.lower()
    assert "3" in result.detail   # param count mentioned


def test_check_capability_chat_kind_is_lenient():
    """Chat tasks (no tools) work fine on small models."""
    from sage.core.model_floor import check_capability
    result = check_capability("ollama:llama3.2", task_kind="chat")
    assert result.ok is True


# ════════════════════════════════════════════════════════════════════════
# T3: Bounded regenerate context
# ════════════════════════════════════════════════════════════════════════

def test_build_regenerate_prompt_drops_full_history():
    from sage.core.regenerate_context import build_regenerate_prompt
    prompt = build_regenerate_prompt(
        failing_file="src/server.js",
        failing_content="const x = 1\nconst y =\n",
        error_tail="SyntaxError: Unexpected end of input at line 3",
        rag_chunks=[],
        max_chars=4000,
    )
    # Must contain the failing file path + content + the error
    assert "src/server.js" in prompt
    assert "Unexpected end of input" in prompt
    assert "const x = 1" in prompt
    # Must NOT contain leftover planning markers
    assert "## TASK:" not in prompt
    assert "Plan ID:" not in prompt
    assert "## NEXT STEPS" not in prompt


def test_build_regenerate_prompt_truncates_oversized_input():
    from sage.core.regenerate_context import build_regenerate_prompt
    huge = "X" * 50_000
    prompt = build_regenerate_prompt(
        failing_file="src/big.py",
        failing_content=huge,
        error_tail="some error",
        rag_chunks=[],
        max_chars=2000,
    )
    assert len(prompt) <= 2500  # some overhead allowed for headers


def test_build_regenerate_prompt_includes_rag_when_present():
    from sage.core.regenerate_context import build_regenerate_prompt
    prompt = build_regenerate_prompt(
        failing_file="src/api.js",
        failing_content="import { db } from './db'",
        error_tail="Cannot find module './db'",
        rag_chunks=[("src/lib/database.js", "export const db = ...")],
        max_chars=4000,
    )
    assert "src/lib/database.js" in prompt
    assert "export const db" in prompt


def test_build_regenerate_prompt_strips_protocol_markers_from_error():
    """Defensive: even if the error tail itself echoes protocol noise, scrub it."""
    from sage.core.regenerate_context import build_regenerate_prompt
    polluted_error = (
        "SyntaxError\n## TASK: Build pets app\nPlan ID: plan_x\n"
        "## NEXT STEPS\n1. fix\n"
    )
    prompt = build_regenerate_prompt(
        failing_file="x.js", failing_content="x", error_tail=polluted_error,
        rag_chunks=[], max_chars=4000,
    )
    assert "## TASK:" not in prompt
    assert "Plan ID:" not in prompt


# ════════════════════════════════════════════════════════════════════════
# T4 + T12: Grammar enforcement (default + project-aware)
# ════════════════════════════════════════════════════════════════════════

def test_should_enforce_grammar_returns_true_for_tool_turns():
    from sage.core.grammar_default import should_enforce_grammar
    # A "make a code change" prompt should be tool-emitting
    assert should_enforce_grammar("Implement user authentication") is True
    assert should_enforce_grammar("Fix the bug in src/server.js") is True
    assert should_enforce_grammar("Add a new endpoint") is True


def test_should_enforce_grammar_returns_false_for_chat_turns():
    from sage.core.grammar_default import should_enforce_grammar
    assert should_enforce_grammar("What is OAuth?") is False
    assert should_enforce_grammar("Explain how React hooks work") is False
    assert should_enforce_grammar("Tell me about the file structure") is False


def test_get_combined_grammar_includes_protocol():
    from sage.core.grammar_default import get_combined_grammar_string
    combined = get_combined_grammar_string(project_root=None)
    # Must include the protocol grammar
    assert "FILE:" in combined or "file-block" in combined


def test_get_combined_grammar_with_project_includes_symbols(tmp_path):
    """When given a project dir, grammar should include only real symbols."""
    from sage.core.grammar_default import get_combined_grammar_string
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("")
    (tmp_path / "pkg" / "utils.py").write_text(
        "def real_function(): pass\nclass RealClass: pass\n"
    )
    combined = get_combined_grammar_string(project_root=tmp_path)
    assert "real_function" in combined
    assert "RealClass" in combined


def test_grammar_caches_per_project(tmp_path):
    """Re-calling for the same project should hit the cache."""
    from sage.core.grammar_default import get_combined_grammar_string, _cache
    _cache.clear()
    (tmp_path / "x.py").write_text("def f(): pass")
    a = get_combined_grammar_string(project_root=tmp_path)
    b = get_combined_grammar_string(project_root=tmp_path)
    assert a == b
    # Cache has one entry
    assert len(_cache) >= 1
