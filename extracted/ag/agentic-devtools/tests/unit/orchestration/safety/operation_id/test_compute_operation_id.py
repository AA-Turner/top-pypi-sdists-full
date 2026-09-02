"""Tests for compute_operation_id() — FR-004, FR-006 deterministic hashing."""

from __future__ import annotations

from agentic_devtools.orchestration.safety.operation_id import compute_operation_id


class TestComputeOperationId:
    """Tests for operation ID computation."""

    def test_deterministic_for_same_inputs(self) -> None:
        id1 = compute_operation_id("node_x", "tool_a", {"key": "value"})
        id2 = compute_operation_id("node_x", "tool_a", {"key": "value"})
        assert id1 == id2

    def test_different_for_different_inputs(self) -> None:
        id1 = compute_operation_id("node_x", "tool_a", {"key": "value1"})
        id2 = compute_operation_id("node_x", "tool_a", {"key": "value2"})
        assert id1 != id2

    def test_different_for_different_tools(self) -> None:
        id1 = compute_operation_id("node_x", "tool_a", {"key": "value"})
        id2 = compute_operation_id("node_x", "tool_b", {"key": "value"})
        assert id1 != id2

    def test_different_for_different_node_names(self) -> None:
        """Same tool+inputs with different node_name produces distinct IDs (FR-006)."""
        id1 = compute_operation_id("node_a", "tool_x", {"key": "value"})
        id2 = compute_operation_id("node_b", "tool_x", {"key": "value"})
        assert id1 != id2

    def test_format_is_toolname_colon_hash(self) -> None:
        op_id = compute_operation_id("node", "my_tool", {"a": 1})
        assert op_id.startswith("my_tool:")
        hash_part = op_id.split(":")[1]
        assert len(hash_part) == 16
        # Should be hex
        int(hash_part, 16)

    def test_excludes_timestamp_fields_recursive(self) -> None:
        id1 = compute_operation_id("n", "t", {"data": {"timestamp": "2024-01-01", "val": 1}})
        id2 = compute_operation_id("n", "t", {"data": {"timestamp": "2025-12-31", "val": 1}})
        assert id1 == id2

    def test_excludes_created_at_fields(self) -> None:
        id1 = compute_operation_id("n", "t", {"created_at": "2024-01-01", "x": 1})
        id2 = compute_operation_id("n", "t", {"created_at": "2025-12-31", "x": 1})
        assert id1 == id2

    def test_excludes_updated_at_fields(self) -> None:
        id1 = compute_operation_id("n", "t", {"updated_at": "now", "x": 1})
        id2 = compute_operation_id("n", "t", {"updated_at": "later", "x": 1})
        assert id1 == id2

    def test_excludes_request_id_exact(self) -> None:
        id1 = compute_operation_id("n", "t", {"request_id": "abc", "x": 1})
        id2 = compute_operation_id("n", "t", {"request_id": "def", "x": 1})
        assert id1 == id2

    def test_per_tool_nondeterministic_dot_path(self) -> None:
        inputs = {"metadata": {"session_id": "xyz", "data": "stable"}}
        id1 = compute_operation_id("n", "t", inputs, ("metadata.session_id",))
        inputs2 = {"metadata": {"session_id": "abc", "data": "stable"}}
        id2 = compute_operation_id("n", "t", inputs2, ("metadata.session_id",))
        assert id1 == id2

    def test_missing_dot_path_skipped(self) -> None:
        inputs = {"x": 1}
        # Should not raise
        op_id = compute_operation_id("n", "t", inputs, ("nonexistent.path",))
        assert op_id.startswith("t:")

    def test_sensitive_keys_redacted(self) -> None:
        id1 = compute_operation_id("n", "t", {"token": "secret1", "x": 1})
        id2 = compute_operation_id("n", "t", {"token": "secret2", "x": 1})
        assert id1 == id2

    def test_empty_inputs(self) -> None:
        op_id = compute_operation_id("n", "tool", {})
        assert op_id.startswith("tool:")

    def test_nested_list_with_nondeterministic(self) -> None:
        inputs = {"items": [{"timestamp": "t1", "val": 1}, {"timestamp": "t2", "val": 2}]}
        id1 = compute_operation_id("n", "t", inputs)
        inputs2 = {"items": [{"timestamp": "t3", "val": 1}, {"timestamp": "t4", "val": 2}]}
        id2 = compute_operation_id("n", "t", inputs2)
        assert id1 == id2

    def test_hash_stability_across_calls(self) -> None:
        """Hash is stable across process restarts (deterministic)."""
        op_id = compute_operation_id("planning", "jira_comment", {"body": "hello"})
        # Same call should produce same result every time
        assert op_id == compute_operation_id("planning", "jira_comment", {"body": "hello"})

    def test_no_collision_from_ambiguous_node_name_delimiter(self) -> None:
        """node_name containing ':' must not collide with a different split of the same text.

        The JSON-array encoding means ('a', 'b:c') and ('a:b', 'c') produce distinct
        hashes, whereas a bare f-string join `f"{node_name}:{canonical}"` would
        potentially hash to the same bytes.
        """
        # canonical JSON of {"x": 1} is '{"x":1}'
        id1 = compute_operation_id("a", "tool", {"x": "b:c"})
        id2 = compute_operation_id("a:b", "tool", {"x": "c"})
        assert id1 != id2, "Different (node_name, inputs) pairs must produce distinct operation IDs"

    def test_empty_node_name_raises(self) -> None:
        """Empty node_name raises ValueError to prevent cross-node collision (FR-006)."""
        import pytest

        with pytest.raises(ValueError, match="node_name"):
            compute_operation_id("", "tool", {"x": 1})

    def test_whitespace_only_node_name_raises(self) -> None:
        """Whitespace-only node_name raises ValueError (FR-006)."""
        import pytest

        with pytest.raises(ValueError, match="node_name"):
            compute_operation_id("   ", "tool", {"x": 1})
