"""Tests for ExecutionState TypedDict."""

from agentic_devtools.orchestration.execution.state import ExecutionState, NodeUpdateAlias


class TestExecutionState:
    def test_construction_empty(self) -> None:
        state: ExecutionState = {}
        assert isinstance(state, dict)

    def test_construction_with_status(self) -> None:
        state: ExecutionState = {"status": "active"}
        assert state["status"] == "active"

    def test_construction_with_error(self) -> None:
        state: ExecutionState = {"error": "something failed"}
        assert state["error"] == "something failed"

    def test_construction_with_none_error(self) -> None:
        state: ExecutionState = {"error": None}
        assert state["error"] is None

    def test_construction_with_retry_count(self) -> None:
        state: ExecutionState = {"retry_count": 3}
        assert state["retry_count"] == 3

    def test_all_fields(self) -> None:
        state: ExecutionState = {
            "status": "completed",
            "error": None,
            "retry_count": 0,
        }
        assert state["status"] == "completed"
        assert state["error"] is None
        assert state["retry_count"] == 0


class TestNodeUpdateAlias:
    def test_is_dict_type(self) -> None:
        update: NodeUpdateAlias = {"key": "value"}
        assert isinstance(update, dict)

    def test_supports_json_values(self) -> None:
        update: NodeUpdateAlias = {
            "str": "hello",
            "num": 42,
            "flag": True,
            "null": None,
            "list": [1, 2, 3],
            "nested": {"a": "b"},
        }
        assert len(update) == 6
