"""Tests for token estimator fallback (#1006)."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from anteroom.services.token_estimator import (
    RequestTokenBreakdown,
    count_message_tokens,
    count_text_tokens,
    estimate_request_tokens,
    estimate_usage,
)


class TestCountMessageTokens:
    def test_single_message(self) -> None:
        msgs = [{"role": "user", "content": "Hello, world!"}]
        tokens = count_message_tokens(msgs)
        assert tokens > 0

    def test_empty_messages(self) -> None:
        assert count_message_tokens([]) == 0

    def test_multi_turn(self) -> None:
        msgs = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "What is 2+2?"},
            {"role": "assistant", "content": "4"},
        ]
        tokens = count_message_tokens(msgs)
        # 3 messages × 4 overhead + content tokens
        assert tokens > 12

    def test_message_with_tool_calls(self) -> None:
        msgs = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "read_file",
                            "arguments": '{"path": "/tmp/test.txt"}',
                        }
                    }
                ],
            }
        ]
        tokens = count_message_tokens(msgs)
        assert tokens > 4  # At least overhead + tool tokens

    def test_empty_content(self) -> None:
        msgs = [{"role": "user", "content": ""}]
        tokens = count_message_tokens(msgs)
        assert tokens == 4  # Just the overhead

    def test_list_content(self) -> None:
        msgs = [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}]
        tokens = count_message_tokens(msgs)
        assert tokens > 4


class TestCountTextTokens:
    def test_non_empty(self) -> None:
        assert count_text_tokens("Hello, world!") > 0

    def test_empty(self) -> None:
        assert count_text_tokens("") == 0

    def test_long_text(self) -> None:
        text = "The quick brown fox jumps over the lazy dog. " * 100
        tokens = count_text_tokens(text)
        assert tokens > 100


class TestEstimateUsage:
    def test_returns_all_fields(self) -> None:
        msgs = [{"role": "user", "content": "Hi"}]
        result = estimate_usage(msgs, "Hello!", "gpt-4o")
        assert "prompt_tokens" in result
        assert "completion_tokens" in result
        assert "total_tokens" in result
        assert result["model"] == "gpt-4o"
        assert result["estimated"] is True

    def test_total_is_sum(self) -> None:
        msgs = [{"role": "user", "content": "Hi"}]
        result = estimate_usage(msgs, "Hello!", "gpt-4o")
        assert result["total_tokens"] == result["prompt_tokens"] + result["completion_tokens"]

    def test_preserves_real_model_name(self) -> None:
        result = estimate_usage([], "", "our-openai-5.2")
        assert result["model"] == "our-openai-5.2"

    def test_custom_model_name_works(self) -> None:
        msgs = [{"role": "user", "content": "Hello"}]
        result = estimate_usage(msgs, "World", "custom-internal-v3")
        assert result["prompt_tokens"] > 0
        assert result["completion_tokens"] > 0
        assert result["model"] == "custom-internal-v3"

    def test_estimated_flag(self) -> None:
        result = estimate_usage([{"role": "user", "content": "x"}], "y", "m")
        assert result["estimated"] is True

    def test_empty_inputs(self) -> None:
        result = estimate_usage([], "", "model")
        assert result["prompt_tokens"] == 0
        assert result["completion_tokens"] == 0
        assert result["total_tokens"] == 0


class TestEstimateRequestTokens:
    """Tests for the shared full-request token accounting (#1339)."""

    def test_message_only_returns_correct_total(self) -> None:
        msgs = [{"role": "user", "content": "Hello, world!"}]
        breakdown = estimate_request_tokens(messages=msgs)
        assert breakdown.total == breakdown.message_tokens
        assert breakdown.system_prompt_tokens == 0
        assert breakdown.tool_schema_tokens == 0

    def test_with_system_prompt_increases_total(self) -> None:
        msgs = [{"role": "user", "content": "Hi"}]
        without = estimate_request_tokens(messages=msgs)
        with_sys = estimate_request_tokens(messages=msgs, system_prompt="You are a helpful assistant.")
        assert with_sys.total > without.total
        assert with_sys.system_prompt_tokens > 0
        assert with_sys.message_tokens == without.message_tokens

    def test_with_extra_system_prompt(self) -> None:
        msgs = [{"role": "user", "content": "Hi"}]
        breakdown = estimate_request_tokens(
            messages=msgs,
            system_prompt="Base prompt.",
            extra_system_prompt="Extra context with RAG results and instructions.",
        )
        assert breakdown.system_prompt_tokens > 0
        assert breakdown.total > breakdown.message_tokens

    def test_with_tool_schemas_increases_total(self) -> None:
        msgs = [{"role": "user", "content": "Hi"}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read a file from disk",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"],
                    },
                },
            }
        ]
        without = estimate_request_tokens(messages=msgs)
        with_tools = estimate_request_tokens(messages=msgs, tool_schemas=tools)
        assert with_tools.total > without.total
        assert with_tools.tool_schema_tokens > 0

    def test_undercount_regression(self) -> None:
        """Full-request estimate must exceed message-only count when overhead is present."""
        msgs = [{"role": "user", "content": "Write a function."}]
        system_prompt = "You are a senior Python developer. " * 20
        tools = [
            {
                "type": "function",
                "function": {
                    "name": f"tool_{i}",
                    "description": f"Tool number {i} does things",
                    "parameters": {"type": "object", "properties": {}},
                },
            }
            for i in range(10)
        ]
        message_only = count_message_tokens(msgs)
        full = estimate_request_tokens(messages=msgs, system_prompt=system_prompt, tool_schemas=tools)
        assert full.total > message_only + 200

    def test_breakdown_fields_sum_to_total(self) -> None:
        msgs = [{"role": "user", "content": "Hello"}]
        breakdown = estimate_request_tokens(
            messages=msgs,
            system_prompt="Be helpful.",
            tool_schemas=[{"type": "function", "function": {"name": "bash", "parameters": {}}}],
        )
        expected = breakdown.message_tokens + breakdown.system_prompt_tokens + breakdown.tool_schema_tokens
        assert breakdown.total == expected

    def test_empty_inputs(self) -> None:
        breakdown = estimate_request_tokens(messages=[])
        assert breakdown.total == 0
        assert breakdown.message_tokens == 0
        assert breakdown.system_prompt_tokens == 0
        assert breakdown.tool_schema_tokens == 0

    def test_returns_frozen_dataclass(self) -> None:
        breakdown = estimate_request_tokens(messages=[{"role": "user", "content": "x"}])
        assert isinstance(breakdown, RequestTokenBreakdown)
        with pytest.raises(AttributeError):
            breakdown.total = 999  # type: ignore[misc]


class TestTiktokenFallback:
    def test_fallback_to_char_estimate(self) -> None:
        """When tiktoken import fails, falls back to len//4."""
        import anteroom.services.token_estimator as mod

        old = mod._encoding
        mod._encoding = None
        try:
            with patch.dict("sys.modules", {"tiktoken": None}):
                mod._encoding = None  # Reset cache
                # Force re-import failure
                with patch("builtins.__import__", side_effect=ImportError("no tiktoken")):
                    mod._encoding = None
                    result = estimate_usage(
                        [{"role": "user", "content": "Hello world"}],
                        "Response text here",
                        "model",
                    )
                    assert result["prompt_tokens"] > 0
                    assert result["completion_tokens"] > 0
        finally:
            mod._encoding = old


# ---------------------------------------------------------------------------
# merge_message_metadata
# ---------------------------------------------------------------------------


class TestMergeMessageMetadata:
    @pytest.fixture()
    def db(self) -> Any:
        from anteroom.db import init_db

        with tempfile.TemporaryDirectory() as td:
            conn = init_db(Path(td) / "test.db")
            yield conn
            conn.close()

    def _create_msg(self, db: Any, metadata: dict | None = None) -> str:
        from anteroom.services.storage import create_conversation, create_message

        conv = create_conversation(db, "test")
        msg = create_message(db, conv["id"], "assistant", "hello", metadata=metadata)
        return msg["id"]

    def test_merge_into_empty(self, db: Any) -> None:
        from anteroom.services.storage import merge_message_metadata

        msg_id = self._create_msg(db)
        merge_message_metadata(db, msg_id, {"usage_estimated": True})
        row = db.execute_fetchone("SELECT metadata FROM messages WHERE id = ?", (msg_id,))
        meta = json.loads(row["metadata"])
        assert meta["usage_estimated"] is True

    def test_merge_preserves_existing(self, db: Any) -> None:
        from anteroom.services.storage import merge_message_metadata

        msg_id = self._create_msg(db, metadata={"rag_sources": [{"id": "s1"}]})
        merge_message_metadata(db, msg_id, {"usage_estimated": True})
        row = db.execute_fetchone("SELECT metadata FROM messages WHERE id = ?", (msg_id,))
        meta = json.loads(row["metadata"])
        assert meta["usage_estimated"] is True
        assert meta["rag_sources"] == [{"id": "s1"}]

    def test_merge_overwrites_key(self, db: Any) -> None:
        from anteroom.services.storage import merge_message_metadata

        msg_id = self._create_msg(db, metadata={"usage_estimated": False})
        merge_message_metadata(db, msg_id, {"usage_estimated": True})
        row = db.execute_fetchone("SELECT metadata FROM messages WHERE id = ?", (msg_id,))
        meta = json.loads(row["metadata"])
        assert meta["usage_estimated"] is True

    def test_merge_nonexistent_message(self, db: Any) -> None:
        from anteroom.services.storage import merge_message_metadata

        merge_message_metadata(db, "nonexistent-id", {"key": "val"})
        # Should not raise
