"""Coverage tests for pure helpers in sage/main.py.

Focuses on functions with no external-service dependencies — model ID parsing,
message dict/dataclass shimming, REPL arg parsing, runtime fallback selection.
External-system functions (LSP, Ollama HTTP probe, llama_cpp wheel install)
are tested via their explicit network/process paths only when feasible.
"""

from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest

from sage.config import SageConfig
from sage.cli_core import (
    _is_explicit_model_request,
    _should_lock_requested_model,
    _get_msg_content,
    _get_msg_role,
    _msg_to_dict,
    _parse_autoorg_repl_args,
    _pick_runtime_fallback,
    _model_capability_score,
    _autoorg_keyword_hits,
    _autoorg_response_requests_user_input,
)


class TestIsExplicitModelRequest:

    @pytest.mark.parametrize("model_id,expected", [
        ("ollama:llama3.2", True),
        ("openrouter:qwen/qwen3-coder:free", True),
        ("llama_cpp:Qwen2.5-7B", True),
        ("gemini:gemini-2.0-flash", True),
        ("gcs:something", True),
        # No colon → not explicit
        ("qwen3-coder", False),
        ("", False),
        # Colon but prefix unknown → not explicit
        ("unknownprovider:somemodel", False),
        # OpenRouter-style without provider prefix → not "explicit"
        ("qwen/qwen3-coder:free", False),
    ])
    def test_provider_qualified_ids(self, model_id, expected):
        assert _is_explicit_model_request(model_id) is expected


class TestShouldLockRequestedModel:

    def test_provider_prefixed_locks(self):
        assert _should_lock_requested_model("ollama:llama3.2", SageConfig()) is True

    def test_empty_string_does_not_lock(self):
        assert _should_lock_requested_model("", SageConfig()) is False

    def test_unknown_bare_name_does_not_lock(self):
        # No catalog entry, not in ollama or local registrations
        assert _should_lock_requested_model("zzz-totally-unknown", SageConfig()) is False

    def test_local_registered_model_locks(self):
        cfg = SageConfig(models={"my-gguf": {"path": "/tmp/x.gguf", "provider": "llama_cpp"}})
        assert _should_lock_requested_model("my-gguf", cfg) is True


class TestMessageShims:
    """Both dict and dataclass-style messages must work everywhere."""

    def test_get_content_from_dict(self):
        assert _get_msg_content({"role": "user", "content": "hi"}) == "hi"

    def test_get_content_from_dataclass(self):
        msg = MagicMock(content="hello", role="user")
        assert _get_msg_content(msg) == "hello"

    def test_get_content_missing_returns_empty(self):
        assert _get_msg_content(None) == ""
        assert _get_msg_content({}) == ""

    def test_get_role_from_dict(self):
        assert _get_msg_role({"role": "assistant"}) == "assistant"

    def test_get_role_from_dataclass(self):
        msg = MagicMock(role="system", content="x")
        assert _get_msg_role(msg) == "system"

    def test_get_role_missing_returns_empty(self):
        assert _get_msg_role(None) == ""
        assert _get_msg_role({}) == ""

    def test_msg_to_dict_passes_dict_through(self):
        d = {"role": "user", "content": "hi"}
        assert _msg_to_dict(d) is d

    def test_msg_to_dict_converts_dataclass(self):
        # MagicMock has both attrs — the function should pull them out
        from dataclasses import dataclass

        @dataclass
        class M:
            role: str
            content: str

        result = _msg_to_dict(M("user", "hi"))
        assert result == {"role": "user", "content": "hi"}

    def test_msg_to_dict_falls_back_for_unknown(self):
        assert _msg_to_dict(42) == {"role": "", "content": ""}


class TestParseAutoorgReplArgs:

    def test_empty_args_returns_defaults(self):
        task, plan, dry, parallel = _parse_autoorg_repl_args("")
        assert task == "" and plan is False and dry is False and parallel is True

    def test_whitespace_only_returns_defaults(self):
        task, plan, dry, parallel = _parse_autoorg_repl_args("   ")
        assert task == "" and plan is False

    def test_parses_focus_text(self):
        task, plan, dry, parallel = _parse_autoorg_repl_args("build a todo app")
        assert task == "build a todo app"

    def test_plan_short_flag(self):
        task, plan, _, _ = _parse_autoorg_repl_args("-p add tests")
        assert plan is True
        assert task == "add tests"

    def test_plan_long_flag(self):
        _, plan, _, _ = _parse_autoorg_repl_args("--plan refactor x")
        assert plan is True

    def test_dry_run_flags(self):
        _, _, dry, _ = _parse_autoorg_repl_args("--dry-run task")
        assert dry is True
        _, _, dry, _ = _parse_autoorg_repl_args("-n task")
        assert dry is True

    def test_no_parallel_disables(self):
        _, _, _, parallel = _parse_autoorg_repl_args("--no-parallel task")
        assert parallel is False

    def test_parallel_explicit(self):
        _, _, _, parallel = _parse_autoorg_repl_args("--parallel task")
        assert parallel is True

    def test_invalid_quoting_raises(self):
        with pytest.raises(ValueError, match="Invalid quoting"):
            _parse_autoorg_repl_args('this is "unterminated')


class TestPickRuntimeFallback:

    def test_returns_none_when_nothing_configured(self):
        cfg = SageConfig(api_keys={})
        # No ollama running, no API keys
        with patch("httpx.get", side_effect=Exception("connection refused")):
            assert _pick_runtime_fallback(cfg) is None

    def test_prefers_ollama_when_available(self):
        cfg = SageConfig(api_keys={})
        fake_resp = MagicMock(status_code=200)
        fake_resp.json.return_value = {"models": [{"name": "llama3.2:latest"}]}
        with patch("httpx.get", return_value=fake_resp):
            assert _pick_runtime_fallback(cfg) == "ollama:llama3.2"

    def test_falls_through_to_gemini_when_keyed(self):
        cfg = SageConfig(api_keys={"gemini": "g-key"})
        with patch("httpx.get", side_effect=Exception("no ollama")):
            result = _pick_runtime_fallback(cfg)
        assert result is not None and result.startswith("gemini:")

    def test_groq_preferred_over_openrouter(self):
        # Both keys → first match wins by cloud_defaults order
        cfg = SageConfig(api_keys={"groq": "k1", "openrouter": "k2"})
        with patch("httpx.get", side_effect=Exception("no ollama")):
            result = _pick_runtime_fallback(cfg)
        assert result.startswith("groq:")


class TestModelCapabilityScore:
    """Heuristic scorer used to pick a better model when one is available."""

    def test_returns_an_int(self):
        from sage.providers.base import ModelInfo
        m = ModelInfo(id="some-model", provider="ollama", name="some-model", local=True)
        score = _model_capability_score(m)
        assert isinstance(score, int)

    def test_larger_size_scores_higher(self):
        from sage.providers.base import ModelInfo
        small = ModelInfo(id="m-1b", provider="ollama", name="m-1b", local=True)
        big = ModelInfo(id="m-70b", provider="ollama", name="m-70b", local=True)
        # The scorer keys off the visible size hint in the name/id
        assert _model_capability_score(big) >= _model_capability_score(small)


class TestAutoorgHelpers:

    def test_keyword_hits_returns_matching_labels(self):
        """Signature: keyword_map = {label: (kw, kw, ...)}. Returns labels whose
        ANY keyword appears (case-insensitive) in text."""
        result = _autoorg_keyword_hits(
            "Build a todo app with React and Postgres",
            {"todo_app": ("todo",),
             "frontend": ("react", "vue"),
             "rust_lang": ("rust",)},
        )
        assert "todo_app" in result
        assert "frontend" in result
        assert "rust_lang" not in result

    def test_keyword_hits_case_insensitive(self):
        result = _autoorg_keyword_hits("Build a TODO app", {"todo_app": ("todo",)})
        assert "todo_app" in result

    def test_keyword_hits_empty_input_returns_empty(self):
        assert _autoorg_keyword_hits("", {"x": ("y",)}) == []

    def test_response_user_input_detected(self):
        """Detects "do you want me to" + no blocker term + no tool output."""
        text = "Do you want me to update the schema?"
        assert _autoorg_response_requests_user_input(text) is True

    def test_response_blocker_term_skipped(self):
        """Asks for an API key — that's a legitimate blocker, NOT a premature question."""
        text = "Do you want me to add the API key to the config?"
        assert _autoorg_response_requests_user_input(text) is False

    def test_response_with_real_tool_output_skipped(self):
        text = "RUN: ls\nfile.txt\nDo you want me to continue?"
        assert _autoorg_response_requests_user_input(text) is False

    def test_response_no_question_phrase(self):
        text = "I completed the task."
        assert _autoorg_response_requests_user_input(text) is False
