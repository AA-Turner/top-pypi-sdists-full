"""Tests for resumable_node decorator — FR-002, FR-003, FR-010."""

from __future__ import annotations

from typing import Any

import pytest

from agentic_devtools.orchestration.node_status import NodeFailedError, NodeStatus, resumable_node


class TestResumableNode:
    """Tests for resumable_node skip/retry/status-write logic."""

    def test_skip_completed_node(self) -> None:
        """Completed node returns empty dict without executing."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            raise AssertionError("Should not be called")

        state = {"_node_statuses": {"my_node": NodeStatus(status="completed", attempt_count=1).to_dict()}}
        result = my_node(state)
        assert result == {}

    def test_retry_failed_node_within_budget(self) -> None:
        """Failed node with remaining budget re-executes."""
        call_count = {"n": 0}

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            call_count["n"] += 1
            return {"output": "success"}

        state = {
            "_node_statuses": {"my_node": NodeStatus(status="failed", attempt_count=1, error_summary="err").to_dict()}
        }
        result = my_node(state)
        assert call_count["n"] == 1
        assert result["_node_statuses"]["my_node"]["status"] == "completed"
        assert result["_node_statuses"]["my_node"]["attempt_count"] == 2

    def test_failed_permanent_when_budget_exhausted(self) -> None:
        """Node marked failed_permanent when retry budget exhausted."""

        @resumable_node("my_node", retry_budget=2)
        def my_node(state):
            raise AssertionError("Should not be called")

        # attempt_count=3 means initial + 2 retries (budget=2), so next is exhausted
        state = {
            "_node_statuses": {"my_node": NodeStatus(status="failed", attempt_count=3, error_summary="err").to_dict()}
        }
        with pytest.raises(NodeFailedError, match="Retry budget exhausted"):
            my_node(state)

    def test_records_completed_status_after_success(self) -> None:
        """Successful execution records completed status."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            return {"output": "done"}

        state: dict[str, Any] = {}
        result = my_node(state)
        assert result["_node_statuses"]["my_node"]["status"] == "completed"
        assert result["_node_statuses"]["my_node"]["attempt_count"] == 1
        assert result["_node_statuses"]["my_node"]["error_summary"] is None

    def test_records_failed_status_after_exception(self) -> None:
        """Exception records failed status and wraps in NodeFailedError."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            raise RuntimeError("something broke")

        state: dict[str, Any] = {}
        with pytest.raises(NodeFailedError) as exc_info:
            my_node(state)

        assert "something broke" in str(exc_info.value)
        update = exc_info.value.state_update
        assert update["_node_statuses"]["my_node"]["status"] == "failed"
        assert update["_node_statuses"]["my_node"]["attempt_count"] == 1
        assert "something broke" in update["_node_statuses"]["my_node"]["error_summary"]

    def test_increment_attempt_count_on_retry(self) -> None:
        """Attempt count increments on each retry."""

        @resumable_node("my_node", retry_budget=5)
        def my_node(state):
            return {"data": "ok"}

        state = {
            "_node_statuses": {"my_node": NodeStatus(status="failed", attempt_count=2, error_summary="err").to_dict()}
        }
        result = my_node(state)
        assert result["_node_statuses"]["my_node"]["attempt_count"] == 3

    def test_preserves_other_node_statuses(self) -> None:
        """Updating one node preserves other nodes' statuses."""

        @resumable_node("node_b", retry_budget=3)
        def node_b(state):
            return {"data": "ok"}

        state = {"_node_statuses": {"node_a": NodeStatus(status="completed", attempt_count=1).to_dict()}}
        result = node_b(state)
        assert result["_node_statuses"]["node_a"]["status"] == "completed"
        assert result["_node_statuses"]["node_b"]["status"] == "completed"

    def test_fresh_state_no_node_statuses(self) -> None:
        """Works correctly with no _node_statuses in state."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            return {"output": "first_run"}

        result = my_node({})
        assert result["_node_statuses"]["my_node"]["status"] == "completed"

    def test_non_dict_current_data_treated_as_fresh(self) -> None:
        """Non-dict value in _node_statuses is treated as no prior status."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            return {"output": "ran"}

        state = {"_node_statuses": {"my_node": "invalid_string_value"}}
        result = my_node(state)
        assert result["_node_statuses"]["my_node"]["status"] == "completed"
        assert result["_node_statuses"]["my_node"]["attempt_count"] == 1

    def test_non_dict_node_statuses_container_treated_as_empty(self) -> None:
        """Non-dict _node_statuses container is reset to empty so resume proceeds."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            return {"output": "ran"}

        # _node_statuses itself is a string rather than a dict — corruption scenario
        state = {"_node_statuses": "corrupted_value"}
        result = my_node(state)
        assert result["_node_statuses"]["my_node"]["status"] == "completed"
        assert result["_node_statuses"]["my_node"]["attempt_count"] == 1

    def test_list_node_statuses_container_treated_as_empty(self) -> None:
        """List-typed _node_statuses container is reset to empty so resume proceeds."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            return {"output": "ran"}

        state = {"_node_statuses": ["unexpected", "list"]}
        result = my_node(state)
        assert result["_node_statuses"]["my_node"]["status"] == "completed"

    def test_malformed_dict_current_data_treated_as_fresh(self) -> None:
        """Dict value that fails from_dict parsing is treated as no prior status."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            return {"output": "ran"}

        # Missing required 'status' key will cause from_dict to raise
        state = {"_node_statuses": {"my_node": {"invalid_key": "value"}}}
        result = my_node(state)
        assert result["_node_statuses"]["my_node"]["status"] == "completed"
        assert result["_node_statuses"]["my_node"]["attempt_count"] == 1

    def test_fn_returning_non_dict_uses_empty_dict(self) -> None:
        """Node function returning non-dict is treated as empty dict result."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            return None  # type: ignore[return-value]

        result = my_node({})
        assert result["_node_statuses"]["my_node"]["status"] == "completed"

    def test_node_failed_error_from_fn_is_reraised(self) -> None:
        """NodeFailedError raised by the fn is re-raised without wrapping."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            raise NodeFailedError("inner failure", state_update={"custom": "data"})

        with pytest.raises(NodeFailedError, match="inner failure") as exc_info:
            my_node({})
        assert exc_info.value.state_update == {"custom": "data"}

    def test_failed_permanent_raises_immediately_without_executing(self) -> None:
        """failed_permanent node raises NodeFailedError immediately without re-executing the body."""

        @resumable_node("my_node", retry_budget=5)
        def my_node(state):
            raise AssertionError("Should not be called — permanently failed node must not re-execute")

        state = {
            "_node_statuses": {
                "my_node": NodeStatus(
                    status="failed_permanent",
                    attempt_count=6,
                    error_summary="budget exhausted",
                ).to_dict()
            }
        }
        with pytest.raises(NodeFailedError, match="permanently failed"):
            my_node(state)

    def test_failed_permanent_preserves_existing_node_statuses(self) -> None:
        """failed_permanent short-circuit passes empty state_update so existing statuses are unchanged."""

        @resumable_node("my_node", retry_budget=3)
        def my_node(state):
            raise AssertionError("Should not be called")

        state = {
            "_node_statuses": {
                "other_node": NodeStatus(status="completed", attempt_count=1).to_dict(),
                "my_node": NodeStatus(
                    status="failed_permanent",
                    attempt_count=4,
                    error_summary="exhausted",
                ).to_dict(),
            }
        }
        with pytest.raises(NodeFailedError) as exc_info:
            my_node(state)
        # state_update must be empty — caller retains full _node_statuses from state
        assert exc_info.value.state_update == {}


class TestResumableNodeValidation:
    """Tests for fail-fast validation of resumable_node parameters."""

    def test_empty_node_name_raises(self) -> None:
        """Empty node_name raises ValueError at decoration time."""
        with pytest.raises(ValueError, match="node_name must be a non-empty"):

            @resumable_node("", retry_budget=3)
            def my_node(state):
                return {}

    def test_whitespace_only_node_name_raises(self) -> None:
        """Whitespace-only node_name raises ValueError at decoration time."""
        with pytest.raises(ValueError, match="node_name must be a non-empty"):

            @resumable_node("   ", retry_budget=3)
            def my_node(state):
                return {}

    def test_negative_retry_budget_raises(self) -> None:
        """Negative retry_budget raises ValueError at decoration time."""
        with pytest.raises(ValueError, match="retry_budget must be >= 0"):

            @resumable_node("my_node", retry_budget=-1)
            def my_node(state):
                return {}

    def test_zero_retry_budget_is_valid(self) -> None:
        """retry_budget=0 is a valid configuration (no retries allowed)."""

        @resumable_node("my_node", retry_budget=0)
        def my_node(state):
            return {"result": "ok"}

        result = my_node({})
        assert result["_node_statuses"]["my_node"]["status"] == "completed"
