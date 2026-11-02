"""Tests for IdempotencyRegistry — file persistence and locking."""

from __future__ import annotations

import json
import threading
from pathlib import Path

from agentic_devtools.orchestration.execution.idempotency import (
    IdempotencyRegistry,
    _compute_composite_key,
)


class TestIdempotencyRegistry:
    """Tests for IdempotencyRegistry read/write operations."""

    def test_check_returns_none_for_unknown_key(self, tmp_path: Path) -> None:
        """check() returns None when no entry exists."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        result = registry.check("tool_x", {"arg": "val"}, "node_a")
        assert result is None

    def test_record_and_check_roundtrip(self, tmp_path: Path) -> None:
        """record() persists and check() retrieves the entry."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        registry.record("tool_x", {"arg": "val"}, "node_a", '{"ok": true}')

        entry = registry.check("tool_x", {"arg": "val"}, "node_a")
        assert entry is not None
        assert entry.status == "success"
        assert entry.result_summary == '{"ok": true}'

    def test_different_args_produce_different_keys(self, tmp_path: Path) -> None:
        """Different args hash to different composite keys."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        registry.record("tool_x", {"arg": "a"}, "node_a", "result_a")
        registry.record("tool_x", {"arg": "b"}, "node_a", "result_b")

        entry_a = registry.check("tool_x", {"arg": "a"}, "node_a")
        entry_b = registry.check("tool_x", {"arg": "b"}, "node_a")
        assert entry_a is not None
        assert entry_b is not None
        assert entry_a.result_summary == "result_a"
        assert entry_b.result_summary == "result_b"

    def test_corrupt_file_graceful_degradation(self, tmp_path: Path) -> None:
        """Corrupt registry file produces warning and fresh start."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        # Write corrupt JSON
        registry.registry_path.write_text("not valid json{{{")

        # check should not raise
        result = registry.check("tool_x", {}, "node_a")
        assert result is None

        # record should overwrite corrupt file
        registry.record("tool_x", {}, "node_a", "result")
        entry = registry.check("tool_x", {}, "node_a")
        assert entry is not None

    def test_concurrent_writes(self, tmp_path: Path) -> None:
        """Two threads writing simultaneously don't corrupt the file."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        errors: list[Exception] = []

        def writer(tool_id: str) -> None:
            try:
                for i in range(10):
                    registry.record(tool_id, {"i": i}, "node_a", f"result_{i}")
            except Exception as e:
                errors.append(e)

        t1 = threading.Thread(target=writer, args=("tool_1",))
        t2 = threading.Thread(target=writer, args=("tool_2",))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert len(errors) == 0

        # Verify file is valid JSON
        content = registry.registry_path.read_text()
        data = json.loads(content)
        assert isinstance(data, dict)

    def test_composite_key_format(self) -> None:
        """Composite key follows the expected format."""
        key = _compute_composite_key("my_tool", {"a": 1}, "my_node", "run_123")
        parts = key.split(":")
        assert len(parts) == 4
        assert parts[0] == "my_tool"
        assert len(parts[1]) == 16  # sha256 hex truncated to 16 chars
        assert parts[2] == "my_node"
        assert parts[3] == "run_123"

    def test_composite_key_handles_non_serializable_args(self) -> None:
        """Composite key serialization falls back to string for unknown types."""
        key = _compute_composite_key("my_tool", {"path": Path("/tmp/demo")}, "my_node", "run_123")
        parts = key.split(":")
        assert len(parts) == 4
        assert len(parts[1]) == 16

    def test_non_dict_json_graceful_degradation(self, tmp_path: Path) -> None:
        """Non-dict JSON (e.g. a list) produces warning and fresh start."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        # Write valid JSON that is not a dict
        registry.registry_path.write_text("[]")

        # check should not raise
        result = registry.check("tool_x", {}, "node_a")
        assert result is None

        # record should overwrite with a valid dict
        registry.record("tool_x", {}, "node_a", "result")
        entry = registry.check("tool_x", {}, "node_a")
        assert entry is not None

    def test_result_summary_truncation(self, tmp_path: Path) -> None:
        """Long result summaries are truncated to 500 chars."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        long_result = "x" * 1000
        registry.record("tool", {}, "node", long_result)

        entry = registry.check("tool", {}, "node")
        assert entry is not None
        assert len(entry.result_summary) <= 500

    def test_check_non_dict_entry_value_treated_as_cache_miss(self, tmp_path: Path) -> None:
        """check() treats a non-dict entry value as a cache-miss with a warning."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        key = _compute_composite_key("tool_x", {}, "node_a", "run1")
        registry.registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry.registry_path.write_text(json.dumps({key: "not_a_dict"}))

        result = registry.check("tool_x", {}, "node_a")
        assert result is None

    def test_check_missing_fields_in_entry_treated_as_cache_miss(self, tmp_path: Path) -> None:
        """check() treats an entry dict with missing required fields as a cache-miss."""
        registry = IdempotencyRegistry(tmp_path, "run1")
        key = _compute_composite_key("tool_x", {}, "node_a", "run1")
        registry.registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry.registry_path.write_text(json.dumps({key: {"partial": "data"}}))

        result = registry.check("tool_x", {}, "node_a")
        assert result is None
