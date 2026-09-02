"""Tests for IdempotentToolWrapper."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from agentic_devtools.orchestration.execution.idempotency import (
    IdempotencyRegistry,
    IdempotentToolWrapper,
)


class TestIdempotentToolWrapper:
    """Tests for the idempotent tool invocation wrapper."""

    def test_first_call_invokes_inner_and_records(self, tmp_path: Path) -> None:
        """First call delegates to inner and records the result."""
        inner = MagicMock()
        inner.invoke.return_value = {"success": True, "data": "result"}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        result = wrapper.invoke("my_tool", arg1="val1")

        inner.invoke.assert_called_once_with("my_tool", arg1="val1")
        assert result == {"success": True, "data": "result"}

        # Verify recorded
        entry = registry.check("my_tool", {"arg1": "val1"}, "test_node")
        assert entry is not None

    def test_second_call_returns_cached(self, tmp_path: Path) -> None:
        """Second identical call returns cached result without invoking inner."""
        inner = MagicMock()
        inner.invoke.return_value = {"success": True}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        # First call
        wrapper.invoke("my_tool", key="val")
        # Second call — should not invoke inner again
        wrapper.invoke("my_tool", key="val")

        assert inner.invoke.call_count == 1

    def test_different_args_invoke_inner(self, tmp_path: Path) -> None:
        """Different args are not treated as cached."""
        inner = MagicMock()
        inner.invoke.return_value = {"ok": True}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        wrapper.invoke("my_tool", key="a")
        wrapper.invoke("my_tool", key="b")

        assert inner.invoke.call_count == 2

    def test_list_all_delegates(self, tmp_path: Path) -> None:
        """list_all() delegates to inner."""
        inner = MagicMock()
        inner.list_all.return_value = {"tool_a": "def"}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        assert wrapper.list_all() == {"tool_a": "def"}

    def test_get_categories_delegates(self, tmp_path: Path) -> None:
        """get_categories() delegates to inner."""
        inner = MagicMock()
        inner.get_categories.return_value = ["cat1"]

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        assert wrapper.get_categories() == ["cat1"]

    def test_failed_result_not_treated_as_cache_hit(self, tmp_path: Path) -> None:
        """A previously failed invocation is not short-circuited on retry."""
        inner = MagicMock()
        inner.invoke.return_value = {"success": False, "error": "timeout"}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        # First call — records with status="error"
        wrapper.invoke("my_tool", key="val")
        assert inner.invoke.call_count == 1

        # Second call — should NOT be short-circuited; inner must be called again
        wrapper.invoke("my_tool", key="val")
        assert inner.invoke.call_count == 2

    def test_failed_result_recorded_with_error_status(self, tmp_path: Path) -> None:
        """Tool results with success=False are recorded as status='error'."""
        inner = MagicMock()
        inner.invoke.return_value = {"success": False, "error": "something went wrong"}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        wrapper.invoke("my_tool", key="val")

        entry = registry.check("my_tool", {"key": "val"}, "test_node")
        assert entry is not None
        assert entry.status == "error"

    def test_successful_result_recorded_with_success_status(self, tmp_path: Path) -> None:
        """Tool results with success=True are recorded as status='success'."""
        inner = MagicMock()
        inner.invoke.return_value = {"success": True, "data": "ok"}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        wrapper.invoke("my_tool", key="val")

        entry = registry.check("my_tool", {"key": "val"}, "test_node")
        assert entry is not None
        assert entry.status == "success"

    def test_cached_plain_string_starting_with_brace_remains_string(self, tmp_path: Path) -> None:
        """A raw string payload must not be JSON-decoded on cache hit."""
        inner = MagicMock()
        inner.invoke.return_value = "{not-json-payload}"

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        first = wrapper.invoke("my_tool", key="val")
        second = wrapper.invoke("my_tool", key="val")

        assert first == "{not-json-payload}"
        assert second == "{not-json-payload}"
        assert isinstance(second, str)

    def test_cached_json_array_result_is_decoded_on_cache_hit(self, tmp_path: Path) -> None:
        """JSON array payloads round-trip back to list on cache hit."""
        inner = MagicMock()
        inner.invoke.return_value = [1, 2, 3]

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        first = wrapper.invoke("my_tool", key="val")
        second = wrapper.invoke("my_tool", key="val")

        assert first == [1, 2, 3]
        assert second == [1, 2, 3]
        assert isinstance(second, list)

    def test_large_json_result_not_cached_returns_original(self, tmp_path: Path) -> None:
        """Oversized JSON payloads return the original result and are not cached."""
        inner = MagicMock()
        inner.invoke.return_value = {"payload": "x" * 2000}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        first = wrapper.invoke("my_tool", key="val")
        second = wrapper.invoke("my_tool", key="val")

        # Both calls return the original dict, not a truncated string
        assert isinstance(first, dict)
        assert isinstance(second, dict)
        assert first == {"payload": "x" * 2000}
        assert second == {"payload": "x" * 2000}
        # Oversized results are non-cacheable, so inner is called each time
        assert inner.invoke.call_count == 2

        entry = registry.check("my_tool", {"key": "val"}, "test_node")
        assert entry is not None
        assert entry.result_encoding == "raw"
        assert len(entry.result_summary) == 500
