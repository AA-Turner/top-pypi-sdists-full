"""Tests for IdempotencyRegistry — _load_entries OSError and IdempotentToolWrapper edge cases."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from agentic_devtools.orchestration.execution.idempotency import (
    IdempotencyRegistry,
    IdempotentToolWrapper,
)


class TestIdempotencyRegistryLoadError:
    """Tests for _load_entries graceful degradation on OSError."""

    def test_invalid_run_id_raises_valueerror(self, tmp_path: Path) -> None:
        """Path-like run IDs are rejected before creating the registry path."""
        with pytest.raises(ValueError, match="run_id"):
            IdempotencyRegistry(tmp_path, "../escape")

    def test_load_entries_oserror_returns_empty(self, tmp_path: Path) -> None:
        """OSError during _load_entries returns empty dict."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        # Create the file then make it unreadable
        registry.registry_path.write_text('{"key": "value"}')
        registry.registry_path.chmod(0o000)

        try:
            # check should not raise, returns None
            result = registry.check("tool_x", {}, "node_a")
            assert result is None
        finally:
            # Restore permissions for cleanup
            registry.registry_path.chmod(0o644)

    def test_load_entries_empty_file_returns_empty(self, tmp_path: Path) -> None:
        """Empty registry file returns empty dict (no entries found)."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        # Write empty content
        registry.registry_path.write_text("   ")

        result = registry.check("tool_x", {}, "node_a")
        assert result is None


class TestIdempotentToolWrapperEdgeCases:
    """Tests for IdempotentToolWrapper — cached JSON result and serialization fallback."""

    def test_cached_json_result_is_deserialized(self, tmp_path: Path) -> None:
        """Cached JSON result (starting with '{') is deserialized."""
        inner = MagicMock()
        inner.invoke.return_value = {"status": "ok"}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        # First call records the JSON result
        wrapper.invoke("my_tool", key="val")

        # Second call should return deserialized dict
        result = wrapper.invoke("my_tool", key="val")
        assert isinstance(result, dict)
        assert result["status"] == "ok"

    def test_non_serializable_result_uses_str(self, tmp_path: Path) -> None:
        """Non-JSON-serializable result falls back to str()."""
        inner = MagicMock()
        # Return an object that can't be JSON serialized
        non_serializable = object()
        inner.invoke.return_value = non_serializable

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        # Should not raise
        result = wrapper.invoke("my_tool", key="val")
        assert result is non_serializable

        # Verify it was recorded with str() fallback
        entry = registry.check("my_tool", {"key": "val"}, "test_node")
        assert entry is not None
        assert "object at" in entry.result_summary

    def test_string_result_stored_directly(self, tmp_path: Path) -> None:
        """String results are stored directly (not JSON-dumped)."""
        inner = MagicMock()
        inner.invoke.return_value = "plain text result"

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        wrapper.invoke("my_tool", x="1")

        entry = registry.check("my_tool", {"x": "1"}, "test_node")
        assert entry is not None
        assert entry.result_summary == "plain text result"

        # Second call returns the plain string
        result = wrapper.invoke("my_tool", x="1")
        assert result == "plain text result"

    def test_oversized_string_result_is_non_cacheable(self, tmp_path: Path) -> None:
        """Oversized string results are treated as non-cacheable."""
        inner = MagicMock()
        long_text = "x" * 600
        inner.invoke.return_value = long_text

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        first = wrapper.invoke("my_tool", x="1")
        second = wrapper.invoke("my_tool", x="1")

        assert first == long_text
        assert second == long_text
        assert inner.invoke.call_count == 2
        entry = registry.check("my_tool", {"x": "1"}, "test_node")
        assert entry is not None
        assert entry.status == "error"

    def test_invalid_cached_json_falls_back_to_string(self, tmp_path: Path) -> None:
        """Invalid cached JSON summary is returned as plain string."""
        inner = MagicMock()
        inner.invoke.return_value = {"status": "ok"}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")
        wrapper.invoke("my_tool", key="val")

        content = json.loads(registry.registry_path.read_text())
        key = next(iter(content))
        content[key]["result_summary"] = "{invalid json"
        registry.registry_path.write_text(json.dumps(content))

        result = wrapper.invoke("my_tool", key="val")
        assert result == "{invalid json"

    def test_unknown_cached_result_encoding_falls_back_to_string(self, tmp_path: Path) -> None:
        """Unknown cached encoding returns raw summary without invoking inner again."""
        inner = MagicMock()
        inner.invoke.return_value = {"status": "ok"}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")
        wrapper.invoke("my_tool", key="val")

        content = json.loads(registry.registry_path.read_text())
        key = next(iter(content))
        content[key]["result_encoding"] = "mystery"
        content[key]["result_summary"] = "raw-value"
        registry.registry_path.write_text(json.dumps(content))

        result = wrapper.invoke("my_tool", key="val")
        assert result == "raw-value"
        assert inner.invoke.call_count == 1

    def test_record_oserror_does_not_fail_tool_result(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Registry write failures do not turn a successful tool call into a failure."""
        inner = MagicMock()
        inner.invoke.return_value = {"success": True, "data": "ok"}

        registry = IdempotencyRegistry(tmp_path, "run1")
        wrapper = IdempotentToolWrapper(inner, registry, "test_node")

        def raise_oserror(*args: object, **kwargs: object) -> object:
            raise OSError("disk full")

        with monkeypatch.context() as context:
            context.setattr("agentic_devtools.file_locking.locked_file", raise_oserror)
            result = wrapper.invoke("my_tool", key="val")

        assert result == {"success": True, "data": "ok"}
        assert inner.invoke.call_count == 1
        assert registry.check("my_tool", {"key": "val"}, "test_node") is None
